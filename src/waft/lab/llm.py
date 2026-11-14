"""A chat client for several OpenAI-compatible providers, with failover.

Ported from tavern-keeper-bot/llm.js (the Keeper's client, built for free tiers that
rate-limit hard and sometimes vanish), with three additions the lab needs: it reports
token usage, it counts calls against a budget, and it refuses provider addresses that the
Door Guy would not let anything else in WAFT talk to.

Providers come from the environment, never from a default, so the lab makes no network
call nobody asked for:

    WAFT_LLM_BASE_URL / WAFT_LLM_API_KEY / WAFT_LLM_MODEL        the primary
    WAFT_LLM_2_BASE_URL / WAFT_LLM_2_API_KEY / WAFT_LLM_2_MODEL  first fallback, up to WAFT_LLM_5_*

Any server that speaks /chat/completions works, including local ones: Ollama
(http://localhost:11434/v1) and llama.cpp (http://localhost:8080/v1) need no key.

A provider that answers 429 (or 5xx, or times out) is skipped for a cooldown so the next
call does not wait on it again. Cooling providers are still tried last, so a total outage
degrades to "keep trying", not "give up".
"""

from __future__ import annotations

import json
import os
import re
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from ipaddress import ip_address
from typing import Any
from urllib.parse import urlparse

import httpx

from ..core.door_guy import Bouncer

MAX_PROVIDERS = 5

COOLDOWN_RATE_LIMIT_DEFAULT = 60.0
COOLDOWN_RATE_LIMIT_MAX = 5 * 60.0
COOLDOWN_SERVER_ERROR = 30.0
COOLDOWN_BAD_CREDENTIALS = 10 * 60.0


class LLMError(Exception):
    """A call failed on every provider, or the client was set up wrongly."""


class BudgetSpent(LLMError):
    """The run's call budget is used up. Raised before the call is made."""


@dataclass
class _Failure(Exception):
    short: str
    status: int | None = None
    long: str = ""


@dataclass
class Provider:
    base_url: str
    model: str
    api_key: str = ""
    cool_until: float = 0.0
    json_mode_broken: bool = False

    def __post_init__(self) -> None:
        self.base_url = self.base_url.strip().rstrip("/")
        self.model = self.model.strip()
        self.api_key = (self.api_key or "").strip()

    @property
    def host(self) -> str:
        return urlparse(self.base_url).hostname or self.base_url

    @property
    def name(self) -> str:
        return f"{self.host}:{self.model}"


@dataclass
class Reply:
    text: str
    provider: str
    prompt_tokens: int = 0
    completion_tokens: int = 0


@dataclass
class Usage:
    calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    by_provider: dict[str, int] = field(default_factory=dict)


def check_provider_address(base_url: str) -> None:
    """Refuse addresses nothing in WAFT should send prompts to.

    A provider on this machine (a local model) is the one loopback destination allowed:
    whoever set the variable runs that server. Everything else goes past the Door Guy,
    which blocks cloud metadata endpoints, link-local and private ranges, and odd schemes.
    """
    parsed = urlparse(base_url)
    host = (parsed.hostname or "").lower()
    if parsed.scheme not in ("http", "https") or not host:
        raise LLMError(f"provider address {base_url!r} is not an http(s) URL")
    if host == "localhost":
        return
    try:
        if ip_address(host).is_loopback:
            return
    except ValueError:
        pass
    decision = Bouncer().inspect_url(base_url)
    if not decision.allowed:
        raise LLMError(f"provider address {base_url!r} was refused by the Door Guy ({decision.reason})")


def load_providers(
    env: Mapping[str, str] | None = None, warn: Callable[[str], None] = lambda _msg: None
) -> list[Provider]:
    """Read the provider list from the environment. Incomplete entries are reported and skipped."""
    env = os.environ if env is None else env
    providers: list[Provider] = []

    for n in range(1, MAX_PROVIDERS + 1):
        prefix = "WAFT_LLM_" if n == 1 else f"WAFT_LLM_{n}_"
        base, key, model = (env.get(prefix + part, "") for part in ("BASE_URL", "API_KEY", "MODEL"))
        if not base and not key and not model:
            continue
        if not base or not model:
            warn(f"{prefix}* is incomplete (it needs {prefix}BASE_URL and {prefix}MODEL); ignoring it")
            continue
        check_provider_address(base)
        providers.append(Provider(base_url=base, model=model, api_key=key))
    return providers


_THINK = re.compile(r"<think>[\s\S]*?</think>", re.IGNORECASE)
_FENCE = re.compile(r"```(?:json)?\s*([\s\S]*?)```", re.IGNORECASE)


def strip_thinking(text: str) -> str:
    """Models that think out loud put their reasoning in <think> tags. It is never the answer."""
    return _THINK.sub("", text).strip()


def parse_json_loose(text: Any) -> Any:
    """Parse model output that is JSON, a fenced JSON block, or one object or array inside prose.

    Small and free models do not always honour "JSON only". Raises ValueError when there
    is no JSON value to find.
    """
    s = str(text if text is not None else "").strip()
    try:
        return json.loads(s)
    except ValueError:
        pass
    fenced = _FENCE.search(s)
    if fenced:
        try:
            return json.loads(fenced.group(1).strip())
        except ValueError:
            pass
    candidates = []
    for opener, closer in (("{", "}"), ("[", "]")):
        start, end = s.find(opener), s.rfind(closer)
        if start != -1 and end > start:
            candidates.append((start, s[start : end + 1]))
    for _start, chunk in sorted(candidates):
        try:
            return json.loads(chunk)
        except ValueError:
            continue
    raise ValueError("no JSON value found in model output")


def _cooldown_for(status: int, retry_after: str | None) -> float:
    if status == 429:
        try:
            seconds = float(retry_after) if retry_after is not None else 0.0
        except ValueError:
            seconds = 0.0
        wait = seconds if seconds > 0 else COOLDOWN_RATE_LIMIT_DEFAULT
        return min(wait, COOLDOWN_RATE_LIMIT_MAX)
    if status in (401, 403, 404):
        return COOLDOWN_BAD_CREDENTIALS
    if status == 408 or status >= 500:
        return COOLDOWN_SERVER_ERROR
    return 0.0  # 400 and friends are about this request, not the provider


class LLMClient:
    """Calls the providers in order and fails over. One instance per run; it keeps the tally."""

    def __init__(
        self,
        providers: list[Provider],
        *,
        transport: httpx.BaseTransport | None = None,
        now: Callable[[], float] = time.monotonic,
        timeout: float = 30.0,
        max_calls: int | None = None,
        warn: Callable[[str], None] = lambda _msg: None,
    ) -> None:
        if not providers:
            raise LLMError(
                "no model provider is configured: set WAFT_LLM_BASE_URL and WAFT_LLM_MODEL "
                "(and WAFT_LLM_API_KEY if the provider needs one)"
            )
        self._providers = providers
        self._now = now
        self._timeout = timeout
        self._warn = warn
        self._http = httpx.Client(transport=transport, timeout=timeout)
        self.max_calls = max_calls
        self.usage = Usage()
        self.last_error: str | None = None

    def close(self) -> None:
        self._http.close()

    def describe(self) -> list[dict[str, Any]]:
        """Who this client talks to. Never includes a key."""
        return [{"name": p.name, "model": p.model, "has_key": bool(p.api_key)} for p in self._providers]

    # ------------------------------------------------------------------ one provider, one call

    def _post(self, p: Provider, body: dict[str, Any]) -> httpx.Response:
        headers = {"Content-Type": "application/json"}
        if p.api_key:
            headers["Authorization"] = f"Bearer {p.api_key}"
        return self._http.post(f"{p.base_url}/chat/completions", headers=headers, json=body)

    def _attempt(
        self,
        p: Provider,
        messages: list[dict[str, str]],
        max_tokens: int,
        temperature: float,
        response_format: dict[str, Any] | None,
        allow_empty: bool,
    ) -> Reply:
        body: dict[str, Any] = {
            "model": p.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if response_format and not p.json_mode_broken:
            body["response_format"] = response_format

        try:
            res = self._post(p, body)
            # Some providers reject JSON mode outright. Retry once without it, and only
            # stop asking for it if that retry actually works.
            if res.status_code == 400 and "response_format" in body:
                del body["response_format"]
                retry = self._post(p, body)
                if retry.is_success:
                    p.json_mode_broken = True
                res = retry
        except httpx.TimeoutException:
            p.cool_until = self._now() + COOLDOWN_SERVER_ERROR
            raise _Failure(short=f"timed out after {self._timeout:g}s") from None
        except httpx.HTTPError as err:
            p.cool_until = self._now() + COOLDOWN_SERVER_ERROR
            raise _Failure(short=f"network error: {err}") from None

        if not res.is_success:
            text = res.text
            p.cool_until = self._now() + _cooldown_for(res.status_code, res.headers.get("retry-after"))
            raise _Failure(short=f"{res.status_code} {text[:120]}", status=res.status_code, long=text[:300])

        try:
            data = res.json()
            choice = (data.get("choices") or [{}])[0]
            content = (choice.get("message") or {}).get("content") or ""
        except (ValueError, AttributeError, IndexError, TypeError):
            p.cool_until = self._now() + COOLDOWN_SERVER_ERROR
            raise _Failure(short="response was not the expected JSON") from None

        text = strip_thinking(str(content).strip())
        if not text and not allow_empty:
            raise _Failure(short="empty reply")
        usage = data.get("usage") or {}
        return Reply(
            text=text,
            provider=p.name,
            prompt_tokens=int(usage.get("prompt_tokens") or 0),
            completion_tokens=int(usage.get("completion_tokens") or 0),
        )

    # ------------------------------------------------------------------ the call the lab makes

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        max_tokens: int = 400,
        temperature: float = 0.8,
        response_format: dict[str, Any] | None = None,
        allow_empty: bool = False,
    ) -> Reply:
        """`allow_empty` is for reachability probes: an empty reply still proves the provider answered."""
        if self.max_calls is not None and self.usage.calls >= self.max_calls:
            raise BudgetSpent(f"the call budget of {self.max_calls} is spent")
        self.usage.calls += 1

        t = self._now()
        ready = [p for p in self._providers if p.cool_until <= t]
        cooling = sorted((p for p in self._providers if p.cool_until > t), key=lambda p: p.cool_until)
        order = ready + cooling

        failures: list[tuple[Provider, _Failure]] = []
        for i, p in enumerate(order):
            try:
                reply = self._attempt(p, messages, max_tokens, temperature, response_format, allow_empty)
            except _Failure as failure:
                failures.append((p, failure))
                self.last_error = " | ".join(f"{fp.name}: {ff.short}" for fp, ff in failures)
                if i + 1 < len(order):
                    self._warn(f"{p.name} failed ({failure.short}); trying {order[i + 1].name}")
                continue
            self.last_error = None  # a success clears the last error
            self.usage.prompt_tokens += reply.prompt_tokens
            self.usage.completion_tokens += reply.completion_tokens
            self.usage.by_provider[reply.provider] = self.usage.by_provider.get(reply.provider, 0) + 1
            return reply

        if len(failures) == 1:
            failure = failures[0][1]
            if failure.status:
                raise LLMError(f"LLM error {failure.status}: {failure.long or failure.short}")
            raise LLMError(f"LLM error: {failure.short}")
        raise LLMError(f"All {len(failures)} LLM providers failed: {self.last_error}")
