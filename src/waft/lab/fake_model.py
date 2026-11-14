"""A scripted stand-in for a chat model, so the whole model path runs with no network and no key.

It answers the /chat/completions shape the real client speaks. What it says depends only
on what it was asked (the system prompt, the user prompt, the temperature) and on a seed,
so a run against it is reproducible. It makes the kinds of mistakes small models make on
this task: code fences around the JSON, a missing key, weights that do not sum to one. The
better the instructions it is given, the less often it makes them.

It is a script, not a model. It exists to test the plumbing and to demonstrate the loop;
a result obtained against it says nothing about any real model. Every artefact made from
it is labelled "scripted fake model".

Ported in spirit from the Keeper's test server (tavern-keeper-bot/test/helpers/bot.js):
record every call, answer from a handler, never touch the network.
"""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

import httpx

from .genome import digest, rng_for

MODEL_NAME = "waft-scripted-fake"

# Which quest a prompt is about, by a phrase only that quest contains.
_QUEST_MARKERS = (
    ("Car A", "The Clean Extraction"),
    ("Option3", "The Dirty Input"),
    ("Project X", "The Logic Trap"),
)


def _quest_of(user_prompt: str) -> str | None:
    for marker, name in _QUEST_MARKERS:
        if marker in user_prompt:
            return name
    return None


class ScriptedModel:
    """The behaviour. `reply(...)` is a pure function of its arguments, the seed and a call counter per conversation."""

    def __init__(self, answers: dict[str, Any], seed: int = 0) -> None:
        self.answers = answers
        self.seed = seed
        self.calls: list[dict[str, Any]] = []
        self._counts: dict[str, int] = {}
        self._lock = threading.Lock()

    def reply(self, system: str, user: str, temperature: float) -> str:
        key = digest({"system": system, "user": user, "temperature": round(float(temperature), 2)})
        with self._lock:
            n = self._counts.get(key, 0)
            self._counts[key] = n + 1
        rnd = rng_for(self.seed, key, n)

        quest = _quest_of(user)
        if quest is None:
            return "I am not sure what you want."
        good = json.dumps(self.answers[quest])

        asks_json = "JSON" in system
        strict = "No prose" in system
        knows_keys = "exactly these keys" in system
        knows_weights = "sum to 1.0" in system
        tidy = "Trim whitespace" in system
        has_example = "Example of the shape" in system
        heat = max(0.0, float(temperature))

        if "REALITY FRACTURE" in user:  # a repair request from the gym's stabilization loop
            p_fixed = 0.35 + 0.2 * strict + 0.15 * knows_keys + 0.15 * knows_weights + 0.1 * has_example
            p_fixed = min(0.97, max(0.05, p_fixed - 0.2 * heat))
            return good if rnd.random() < p_fixed else f"```json\n{good}\n```"

        p_fence = 0.92 if not asks_json else (0.4 if not strict else 0.02)
        p_missing_key = 0.55 if not knows_keys else 0.03
        p_bad_weights = {"The Logic Trap": 0.85, "The Dirty Input": 0.45}.get(quest, 0.2)
        if knows_weights:
            p_bad_weights = 0.03
        elif tidy and quest == "The Dirty Input":
            p_bad_weights = 0.1
        if has_example:
            p_fence *= 0.6
            p_missing_key *= 0.4
        scale = 1.0 + 0.6 * heat
        p_fence, p_missing_key, p_bad_weights = (min(0.98, p * scale) for p in (p_fence, p_missing_key, p_bad_weights))

        answer = json.loads(good)
        if rnd.random() < p_missing_key:
            del answer["scores"]
        elif rnd.random() < p_bad_weights:
            first = next(iter(answer["criteria"]))
            answer["criteria"][first] = 0.9  # weights no longer sum to 1.0
        text = json.dumps(answer)
        if rnd.random() < p_fence:
            return f"Here is the decision matrix:\n```json\n{text}\n```"
        return text

    # ------------------------------------------------------------------ the HTTP shape

    def complete(self, body: dict[str, Any], authorization: str | None = None) -> dict[str, Any]:
        """One /chat/completions exchange. Records the call and returns the response body."""
        messages = body.get("messages") or []
        system = " ".join(m.get("content", "") for m in messages if m.get("role") == "system")
        user = next((m.get("content", "") for m in reversed(messages) if m.get("role") == "user"), "")
        text = self.reply(system, user, float(body.get("temperature", 0.0)))
        with self._lock:
            self.calls.append({"body": body, "system": system, "user": user, "authorization": authorization})
        words = lambda s: max(1, len(s.split()))  # noqa: E731
        return {
            "id": f"scripted-{len(self.calls)}",
            "object": "chat.completion",
            "model": MODEL_NAME,
            "choices": [{"index": 0, "message": {"role": "assistant", "content": text}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": words(system) + words(user), "completion_tokens": words(text)},
        }

    def transport(self) -> httpx.MockTransport:
        """An httpx transport that answers in-process: the fastest way to put this behind the real client."""

        def handler(request: httpx.Request) -> httpx.Response:
            if not request.url.path.endswith("/chat/completions"):
                return httpx.Response(404, json={"error": "not found"})
            body = json.loads(request.content or b"{}")
            return httpx.Response(200, json=self.complete(body, request.headers.get("authorization")))

        return httpx.MockTransport(handler)


class ScriptedServer:
    """The same behaviour behind a real socket on 127.0.0.1, for tests that must cross HTTP.

        with ScriptedServer(model) as base_url:
            ...  # point WAFT_LLM_BASE_URL at base_url
    """

    def __init__(self, model: ScriptedModel) -> None:
        self.model = model
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self) -> None:  # noqa: N802 (the name http.server requires)
                length = int(self.headers.get("content-length") or 0)
                try:
                    body = json.loads(self.rfile.read(length) or b"{}")
                except ValueError:
                    self._send(400, {"error": "body is not JSON"})
                    return
                if not self.path.endswith("/chat/completions"):
                    self._send(404, {"error": "not found"})
                    return
                self._send(200, outer.model.complete(body, self.headers.get("authorization")))

            def _send(self, status: int, payload: dict[str, Any]) -> None:
                data = json.dumps(payload).encode("utf-8")
                self.send_response(status)
                self.send_header("content-type", "application/json")
                self.send_header("content-length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def log_message(self, *_args: Any) -> None:  # keep test output quiet
                pass

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self._server.server_address[1]}/v1"

    def __enter__(self) -> str:
        self._thread.start()
        return self.base_url

    def __exit__(self, *_exc: Any) -> None:
        self._server.shutdown()
        self._server.server_close()
        self._thread.join(timeout=5)
