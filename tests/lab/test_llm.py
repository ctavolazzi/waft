"""The provider client: failover, cooldowns, JSON mode, budget, and what it refuses to talk to.

Ported from tavern-keeper-bot/test/llm.test.js. These prove the failover logic against
scripted providers and an injected clock; they say nothing about any real provider.
"""

import json

import httpx
import pytest

from waft.lab.llm import (
    COOLDOWN_RATE_LIMIT_MAX,
    BudgetSpent,
    LLMClient,
    LLMError,
    Provider,
    check_provider_address,
    load_providers,
    parse_json_loose,
    strip_thinking,
)

MESSAGES = [{"role": "user", "content": "hi"}]


def ok(text="hello", usage=None):
    body = {"choices": [{"message": {"content": text}}]}
    if usage:
        body["usage"] = usage
    return httpx.Response(200, json=body)


class Net:
    """Scripted providers, keyed by host. Each value is a function(request, nth_call) -> Response (or raises)."""

    def __init__(self, **hosts):
        self.hosts = hosts
        self.calls = []

    def transport(self):
        def handler(request):
            host = request.url.host.split(".")[0]
            n = sum(1 for h, _ in self.calls if h == host)
            self.calls.append((host, request))
            return self.hosts[host](request, n)

        return httpx.MockTransport(handler)

    def hosts_called(self):
        return [h for h, _ in self.calls]


class Clock:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t


def client(net, clock=None, names=("a", "b"), **kw):
    providers = [Provider(base_url=f"https://{n}.test/v1", model=f"model-{n}", api_key=f"key-{n}") for n in names]
    return LLMClient(providers, transport=net.transport(), now=clock or Clock(), **kw)


def test_the_first_provider_answers():
    net = Net(a=lambda r, n: ok("from a", {"prompt_tokens": 7, "completion_tokens": 3}), b=lambda r, n: ok("from b"))
    c = client(net)

    reply = c.chat(MESSAGES)

    assert (reply.text, reply.provider) == ("from a", "a.test:model-a")
    assert net.hosts_called() == ["a"]
    assert (c.usage.calls, c.usage.prompt_tokens, c.usage.completion_tokens) == (1, 7, 3)
    sent = json.loads(net.calls[0][1].content)
    assert sent["model"] == "model-a" and sent["messages"] == MESSAGES
    assert net.calls[0][1].headers["authorization"] == "Bearer key-a"


@pytest.mark.parametrize("status", [429, 500, 503, 408])
def test_it_fails_over_and_skips_the_failed_provider_next_time(status):
    net = Net(a=lambda r, n: httpx.Response(status, text="no"), b=lambda r, n: ok("from b"))
    c = client(net)

    assert c.chat(MESSAGES).text == "from b"
    assert c.chat(MESSAGES).text == "from b"
    assert net.hosts_called() == ["a", "b", "b"]  # a is cooling, so it is not asked the second time


def test_a_network_error_and_a_timeout_fail_over():
    def boom(request, n):
        raise httpx.ConnectError("refused")

    def slow(request, n):
        raise httpx.ReadTimeout("too slow")

    assert client(Net(a=boom, b=lambda r, n: ok("b"))).chat(MESSAGES).text == "b"
    assert client(Net(a=slow, b=lambda r, n: ok("b"))).chat(MESSAGES).text == "b"


def test_a_cooled_provider_comes_back_and_retry_after_is_capped():
    clock = Clock()
    net = Net(a=lambda r, n: httpx.Response(429, headers={"retry-after": "86400"}) if n == 0 else ok("a again"),
              b=lambda r, n: ok("b"))
    c = client(net, clock)

    assert c.chat(MESSAGES).text == "b"
    clock.t += COOLDOWN_RATE_LIMIT_MAX - 1
    assert c.chat(MESSAGES).text == "b"  # still cooling: a day was asked for, five minutes is the cap
    clock.t += 2
    assert c.chat(MESSAGES).text == "a again"


def test_cooling_providers_are_still_tried_last():
    net = Net(a=lambda r, n: httpx.Response(500) if n == 0 else ok("a recovered"), b=lambda r, n: httpx.Response(500))
    c = client(net)

    with pytest.raises(LLMError, match="All 2 LLM providers failed"):
        c.chat(MESSAGES)
    assert c.chat(MESSAGES).text == "a recovered"  # both are cooling, yet the call still goes out
    assert c.last_error is None


def test_a_bad_request_does_not_cool_the_provider():
    net = Net(a=lambda r, n: httpx.Response(400, text="bad") if n == 0 else ok("a"), b=lambda r, n: ok("b"))
    c = client(net)

    assert c.chat(MESSAGES).text == "b"
    assert c.chat(MESSAGES).text == "a"  # a 400 is about the request, not the provider


def test_json_mode_is_dropped_only_where_it_does_not_work():
    def a(request, n):
        return httpx.Response(400, text="no json mode") if "response_format" in json.loads(request.content) else ok('{"x":1}')

    net = Net(a=a, b=lambda r, n: ok("b"))
    c = client(net)

    assert c.chat(MESSAGES, response_format={"type": "json_object"}).text == '{"x":1}'
    assert c.chat(MESSAGES, response_format={"type": "json_object"}).text == '{"x":1}'
    bodies = [json.loads(r.content) for _h, r in net.calls]
    assert ["response_format" in b for b in bodies] == [True, False, False]  # remembered after the retry worked


def test_an_empty_reply_fails_over_unless_it_is_a_probe():
    net = Net(a=lambda r, n: ok("   "), b=lambda r, n: ok("b"))
    assert client(net).chat(MESSAGES).text == "b"

    probe = client(Net(a=lambda r, n: ok(""), b=lambda r, n: ok("b")))
    assert probe.chat(MESSAGES, allow_empty=True).text == ""


def test_a_body_that_is_not_the_expected_json_fails_over():
    net = Net(a=lambda r, n: httpx.Response(200, text="<html>oops</html>"), b=lambda r, n: ok("b"))
    assert client(net).chat(MESSAGES).text == "b"


def test_thinking_is_never_the_answer():
    assert strip_thinking("<think>plan the reply</think>\nthe reply") == "the reply"
    net = Net(a=lambda r, n: ok("<think>hmm</think>"), b=lambda r, n: ok("b"))
    assert client(net).chat(MESSAGES).text == "b"  # only thinking is an empty reply


def test_one_provider_failing_reports_its_status():
    with pytest.raises(LLMError, match="LLM error 401"):
        client(Net(a=lambda r, n: httpx.Response(401, text="bad key")), names=("a",)).chat(MESSAGES)


def test_the_budget_stops_calls_before_they_are_made():
    net = Net(a=lambda r, n: ok("a"))
    c = client(net, names=("a",), max_calls=2)

    c.chat(MESSAGES)
    c.chat(MESSAGES)
    with pytest.raises(BudgetSpent):
        c.chat(MESSAGES)
    assert len(net.calls) == 2


def test_describe_never_shows_a_key():
    c = client(Net(a=lambda r, n: ok()), names=("a",))
    described = json.dumps(c.describe())
    assert "key-a" not in described
    assert c.describe() == [{"name": "a.test:model-a", "model": "model-a", "has_key": True}]


def test_a_keyless_provider_sends_no_authorization_header():
    net = Net(a=lambda r, n: ok())
    LLMClient([Provider(base_url="https://a.test/v1", model="m")], transport=net.transport()).chat(MESSAGES)
    assert "authorization" not in net.calls[0][1].headers


def test_no_provider_is_an_error_that_says_what_to_set():
    with pytest.raises(LLMError, match="WAFT_LLM_BASE_URL"):
        LLMClient([])


def test_providers_come_from_the_environment_and_incomplete_ones_are_skipped():
    warnings = []
    env = {
        "WAFT_LLM_BASE_URL": "http://localhost:11434/v1/", "WAFT_LLM_MODEL": " llama3.2 ",
        "WAFT_LLM_2_BASE_URL": "https://api.example.com/v1", "WAFT_LLM_2_MODEL": "big", "WAFT_LLM_2_API_KEY": "sk-x",
        "WAFT_LLM_3_API_KEY": "orphan",
    }
    providers = load_providers(env, warn=warnings.append)

    assert [(p.base_url, p.model, bool(p.api_key)) for p in providers] == [
        ("http://localhost:11434/v1", "llama3.2", False),
        ("https://api.example.com/v1", "big", True),
    ]
    assert len(warnings) == 1 and "WAFT_LLM_3_" in warnings[0]
    assert load_providers({}) == []


@pytest.mark.parametrize("url", [
    "http://169.254.169.254/latest",        # cloud metadata
    "http://metadata.google.internal/v1",
    "http://10.0.0.8/v1",                   # a private network
    "ftp://example.com/v1",
    "not a url",
])
def test_addresses_the_door_guy_would_refuse_are_refused(url):
    with pytest.raises(LLMError):
        check_provider_address(url)


@pytest.mark.parametrize("url", ["http://localhost:11434/v1", "http://127.0.0.1:8080/v1", "https://api.example.com/v1"])
def test_a_local_model_and_a_public_host_are_allowed(url):
    check_provider_address(url)


@pytest.mark.parametrize("text,expected", [
    ('{"a": 1}', {"a": 1}),
    ('```json\n{"a": 1}\n```', {"a": 1}),
    ('Sure! Here it is:\n{"a": {"b": [1, 2]}}\nHope that helps.', {"a": {"b": [1, 2]}}),
    ('The braces {like these} are prose.\n```json\n{"a": 1}\n```', {"a": 1}),
    ("[1, 2, 3]", [1, 2, 3]),
    ("The ranking is [3, 1, 2] as asked.", [3, 1, 2]),
])
def test_loose_json_parsing(text, expected):
    assert parse_json_loose(text) == expected


@pytest.mark.parametrize("text", ["", "no json here", "{broken", None])
def test_loose_json_parsing_raises_when_there_is_nothing(text):
    with pytest.raises(ValueError):
        parse_json_loose(text)
