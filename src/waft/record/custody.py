"""The Logbook: a hash-chained, content-addressed record of what ran and what it produced.

Why it exists: a summary sentence ("4 pass") asks the reader to trust the author. A Logbook run does not. Every claim is
a record; every check and control names the executions it rests on; every execution keeps its raw output under its own
SHA-256; every record is hashed together with the hash of the record before it. Anyone can re-derive the hashes, the order,
every verdict and every tally with `verify`, or with `logbook/verify.mjs` (written from CUSTODY.md alone, sharing no code
with this module). Neither re-measures a claim: a balance's two numbers are what was recorded, and to test one you open the
bytes it was taken from.

Format (the full specification is CUSTODY.md):

    <run>/chain.jsonl          one JSON record per line, in order
    <run>/objects/ab/abcd...   raw bytes, named by their own SHA-256

A record is {"schema","run","seq","ts","kind","data","prev","hash"}. `hash` is the SHA-256 of the canonical JSON of the
record without `hash`. Canonical JSON = sorted keys, separators "," and ":", UTF-8, no NaN. Records contain only
integers, strings, booleans, null, arrays and objects. Floats are refused so that a verifier in any language agrees
byte for byte; fractions travel as decimal strings (see `dec`).

Limits, stated plainly: the chain is tamper-EVIDENT, not tamper-PROOF. Someone who rewrites every record and recomputes
every hash produces a chain that is internally consistent. What defeats that is an anchor: the head hash published
somewhere the forger cannot reach (a git commit, a log entry, a message). `verify(expect_head=...)` checks it.
"""
import contextlib
import dataclasses
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

from . import schemas

RECORD_SCHEMA = "fogsift.logbook.record/1"
ZERO = "0" * 64
KINDS = ("run.start", "exec", "check", "handoff", "reconcile", "control", "verdict", "note", "run.end")
CITES_COMMANDS = ("check", "control", "reconcile")   # kinds whose `evidence` lists the exec records they rest on (optional on reconcile)
CHECK_CLASSES = ("must", "should", "gap", "info")
DETERMINISM = ("exact", "semantic", "volatile")
MAX_CAPTURE = 4 * 1024 * 1024
MAX_INT = 2 ** 53

# ---------------------------------------------------------------- canonical form

def canon(obj):
    """Canonical JSON bytes. The one serialisation every hash in this module is taken over."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def dec(x, places=4):
    """A fraction as a decimal string, because records may not hold floats: dec(0.95) == '0.95'."""
    s = f"{float(x):.{places}f}".rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"


def plainify(obj):
    """Make values safe for a record: floats become decimal strings, tuples become lists, anything odd becomes its repr."""
    if obj is None or isinstance(obj, (bool, int, str)):
        return obj
    if isinstance(obj, float):
        return dec(obj)
    if isinstance(obj, (list, tuple, set)):
        return [plainify(v) for v in (sorted(obj) if isinstance(obj, set) else obj)]
    if isinstance(obj, dict):
        return {str(k): plainify(v) for k, v in obj.items()}
    return repr(obj)


def plain_problems(obj, path="$"):
    """Where `obj` is not plain data (int, str, bool, None, list, dict with str keys)."""
    out = []
    if isinstance(obj, bool) or obj is None or isinstance(obj, str):
        return out
    if isinstance(obj, int):
        return [f"{path}: integer {obj} is beyond +-2^53 (use a string)"] if abs(obj) > MAX_INT else out
    if isinstance(obj, float):
        return [f"{path}: float {obj!r} (use dec())"]
    if isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            out += plain_problems(v, f"{path}[{i}]")
        return out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not isinstance(k, str):
                out.append(f"{path}: non-string key {k!r}")
            out += plain_problems(v, f"{path}.{k}")
        return out
    return [f"{path}: {type(obj).__name__} is not plain data"]


# ---------------------------------------------------------------- redaction

REDACT = [
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("api-key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("aws-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("bearer", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{20,}")),
    ("secret-assignment", re.compile(r"(?i)\b(api[_-]?key|secret|token|passwd|password)\b(\s*[:=]\s*)['\"]?[A-Za-z0-9/+_.=-]{12,}['\"]?")),
]


def redact(text):
    """Returns (clean text, number of redactions). Output is hashed AFTER redaction: a secret never enters the store."""
    n = 0
    for name, rx in REDACT:
        if name == "secret-assignment":
            text, k = rx.subn(lambda m: f"{m.group(1)}{m.group(2)}[REDACTED:{name}]", text)
        else:
            text, k = rx.subn(f"[REDACTED:{name}]", text)
        n += k
    return text, n


# ---------------------------------------------------------------- verdict rule (pure)

def rule_r1(checks, skipped=False):
    """R1, the only way a component or stage gets a status. `checks` are check-record data dicts.

    skip  : no checks. A subject with no evidence makes no claim, so it cannot pass.
    fail  : any `must` check not ok.
    warn  : any `should` or `gap` check not ok (a shipped defect, or something worth a human's look).
    pass  : otherwise. `info` checks never change the status.
    """
    if not checks:
        return "skip"
    if any(c["class"] == "must" and not c["ok"] for c in checks):
        return "fail"
    if any(c["class"] in ("should", "gap") and not c["ok"] for c in checks):
        return "warn"
    return "pass"


# ---------------------------------------------------------------- the active logbook (so tools can record without plumbing)

_ACTIVE = []
_LOCAL = threading.local()


def active():
    return _ACTIVE[-1] if _ACTIVE else None


@dataclasses.dataclass
class ExecResult:
    seq: int
    argv: list
    rc: int
    ms: int
    stdout: str
    stderr: str
    timed_out: bool = False
    stdout_ref: dict = None
    stderr_ref: dict = None

    @property
    def ok(self):
        return self.rc == 0

    @property
    def out(self):
        return self.stdout + self.stderr

    def tail(self, n=6):
        return "\n".join(self.out.strip().splitlines()[-n:])

    def json(self):
        s = self.stdout
        return json.loads(s[s.index("{"):]) if "{" in s else json.loads(s)


class LogbookError(Exception):
    pass


def _now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _git(args, cwd):
    try:
        p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=20)
        return p.stdout.strip() if p.returncode == 0 else ""
    except Exception:  # noqa: BLE001
        return ""


def collect_context(repo, pins_path=None):
    """The facts about where and on what a run happened. Read, not asserted."""
    repo = str(repo)
    head = _git(["rev-parse", "HEAD"], repo)
    dirty = [l for l in _git(["status", "--porcelain"], repo).splitlines() if l]
    ctx = {
        "git": {"head": head, "branch": _git(["rev-parse", "--abbrev-ref", "HEAD"], repo), "dirty_paths": len(dirty)},
        "host": {"platform": platform.platform(), "machine": platform.machine(), "python": platform.python_version(),
                 "cpus": os.cpu_count() or 0},
    }
    if pins_path and Path(pins_path).exists():
        raw = Path(pins_path).read_bytes()
        ctx["pins_sha256"] = sha256(raw)
        ctx["pins"] = json.loads(raw)["components"]
    return ctx


class Logbook:
    """One run's chain. Create with `Logbook.create`, read back with `Logbook.open`."""

    def __init__(self, path, run_id, writable, clock=None):
        self.path = Path(path)
        self.run_id = run_id
        self.writable = writable
        self.clock = clock or _now
        self.chain = self.path / "chain.jsonl"
        self.objects = self.path / "objects"
        self._lock = threading.RLock()
        self._seq = 0
        self._prev = ZERO
        self._closed = False
        self._records = []          # parsed records, in order
        self._scope = []            # stack of (component, first exec seq of the scope)
        self._pending = {}          # subject -> check seqs awaiting a verdict
        self._counts = {k: 0 for k in KINDS}
        self.last_verdict_seq = None

    # ------------------------------------------------------------ construction

    @classmethod
    def create(cls, root, *, label, scenario="", argv=None, repo=None, pins=None, meta=None, run_id=None, clock=None):
        clock = clock or _now
        slug = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")[:32] or "run"
        rid = run_id or f"{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}-{slug}-{os.urandom(2).hex()}"
        path = Path(root) / rid
        if path.exists():
            raise LogbookError(f"run {rid} already exists")
        (path / "objects").mkdir(parents=True)
        lb = cls(path, rid, True, clock)
        data = {"label": label, "scenario": scenario, "argv": [redact(a)[0] for a in (argv or sys.argv)],
                "api_version": "1", "meta": meta or {}}
        data.update(collect_context(repo or os.getcwd(), pins))
        lb.append("run.start", data)
        return lb

    @classmethod
    def open(cls, path):
        path = Path(path)
        lb = cls(path, path.name, False)
        for line in lb.chain.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                lb._records.append(r)
                lb._counts[r["kind"]] = lb._counts.get(r["kind"], 0) + 1
        if lb._records:
            lb.run_id = lb._records[0]["run"]
            lb._seq = len(lb._records)
            lb._prev = lb._records[-1]["hash"]
            lb._closed = lb._records[-1]["kind"] == "run.end"
        return lb

    # ------------------------------------------------------------ low level

    def put(self, data, name, *, media="text/plain", determinism="volatile"):
        """Store bytes by their SHA-256. Returns the reference records carry."""
        if determinism not in DETERMINISM:
            raise LogbookError(f"determinism must be one of {DETERMINISM}")
        if isinstance(data, str):
            data = data.encode("utf-8")
        h = sha256(data)
        if self.writable:
            d = self.objects / h[:2]
            d.mkdir(exist_ok=True)
            f = d / h
            if not f.exists():
                tmp = d / (h + ".tmp")
                tmp.write_bytes(data)
                os.replace(tmp, f)
        return {"name": name, "sha256": h, "bytes": len(data), "media": media, "determinism": determinism}

    def artifact(self, ref_or_sha):
        h = ref_or_sha["sha256"] if isinstance(ref_or_sha, dict) else ref_or_sha
        f = self.objects / h[:2] / h
        if not f.exists():
            raise LogbookError(f"object {h} is not in this logbook")
        return f.read_bytes()

    def append(self, kind, data):
        if not self.writable:
            raise LogbookError("this logbook was opened read-only")
        if kind not in KINDS:
            raise LogbookError(f"unknown record kind {kind!r}")
        with self._lock:
            if self._closed:
                raise LogbookError("the run is closed; open a new one")
            problems = plain_problems(data)
            if problems:
                raise LogbookError("record data must be plain (no floats): " + "; ".join(problems[:3]))
            bad_shape = schemas.validate(data, schemas.DATA[kind])
            if bad_shape:
                raise LogbookError(f"{kind} record does not match its schema: " + "; ".join(bad_shape[:3]))
            rec = {"schema": RECORD_SCHEMA, "run": self.run_id, "seq": self._seq, "ts": self.clock(), "kind": kind,
                   "data": data, "prev": self._prev}
            rec["hash"] = sha256(canon(rec))
            line = canon(rec).decode("utf-8")
            with open(self.chain, "a", encoding="utf-8") as f:
                f.write(line + "\n")
                f.flush()
                os.fsync(f.fileno())
            self._records.append(rec)
            self._counts[kind] += 1
            self._seq += 1
            self._prev = rec["hash"]
            if kind == "run.end":
                self._closed = True
            return rec["seq"]

    # ------------------------------------------------------------ scopes and activation

    @contextlib.contextmanager
    def activate(self):
        """While active, `fogsift.sh` and `fogsift.check` record here without being handed the logbook."""
        _ACTIVE.append(self)
        try:
            yield self
        finally:
            _ACTIVE.pop()

    @contextlib.contextmanager
    def scope(self, component):
        """Checks recorded inside a scope cite, by default, the executions made inside it."""
        self._scope.append([component, self._seq])
        try:
            yield self
        finally:
            self._scope.pop()

    @property
    def component(self):
        return self._scope[-1][0] if self._scope else None

    def _scope_execs(self):
        if not self._scope:
            return []
        start = self._scope[-1][1]
        return [r["seq"] for r in self._records[start:] if r["kind"] == "exec"]

    # ------------------------------------------------------------ the record kinds

    def exec(self, argv, *, cwd=None, env=None, isolate=False, timeout=300, stdin=None, purpose="", component=None):
        """Run a command and keep everything: argv, cwd, environment overlay, exit code, duration, redacted output."""
        argv = [str(a) for a in argv]
        base = {} if isolate else dict(os.environ)
        base.update({k: str(v) for k, v in (env or {}).items()})
        t0 = time.time()
        started = self.clock()
        timed_out = False
        try:
            p = subprocess.run(argv, cwd=cwd, env=base, capture_output=True, text=True, timeout=timeout, input=stdin)
            rc, so, se = p.returncode, p.stdout or "", p.stderr or ""
        except subprocess.TimeoutExpired as ex:
            timed_out = True
            rc = 124
            so = ex.stdout.decode("utf-8", "replace") if isinstance(ex.stdout, bytes) else (ex.stdout or "")
            se = (ex.stderr.decode("utf-8", "replace") if isinstance(ex.stderr, bytes) else (ex.stderr or "")) + f"\n[timed out after {timeout}s]"
        except FileNotFoundError as ex:
            rc, so, se = 127, "", str(ex)
        ms = int((time.time() - t0) * 1000)
        so, n1 = redact(so)
        se, n2 = redact(se)
        truncated = len(so) > MAX_CAPTURE or len(se) > MAX_CAPTURE
        so, se = so[:MAX_CAPTURE], se[:MAX_CAPTURE]
        so_ref = self.put(so, "stdout")
        se_ref = self.put(se, "stderr")
        shown_env = {k: redact(str(v))[0] for k, v in (env or {}).items()}
        seq = self.append("exec", {
            "argv": [redact(a)[0] for a in argv], "cwd": str(cwd) if cwd else "", "env_overlay": shown_env,
            "isolated": bool(isolate), "stdin_sha256": sha256(stdin.encode()) if stdin else "", "rc": rc, "ms": ms,
            "started": started, "timed_out": timed_out, "stdout": so_ref, "stderr": se_ref, "redactions": n1 + n2,
            "truncated": truncated, "purpose": purpose, "component": component or self.component or ""})
        return ExecResult(seq, argv, rc, ms, so, se, timed_out, so_ref, se_ref)

    def check(self, component, name, ok, *, cls="must", expected=None, observed=None, detail="", evidence=None):
        """One claim, with what was expected, what was observed, and the executions that bear on it."""
        if cls not in CHECK_CLASSES:
            raise LogbookError(f"check class must be one of {CHECK_CLASSES}")
        ev = list(evidence) if evidence is not None else self._scope_execs()
        seq = self.append("check", {"component": component, "name": name, "class": cls, "ok": bool(ok),
                                    "expected": expected, "observed": observed, "detail": detail, "evidence": ev})
        self._pending.setdefault(component, []).append(seq)
        return seq

    @property
    def next_seq(self):
        """The number the next record will get. Note it before a stage starts; hand it to settle() when the stage ends."""
        return self._seq

    def settle(self, subject, since):
        """Rule R1 reads checks only, so balances, controls and handoffs would otherwise not move a verdict. This adds one
        `must` check to `subject` saying whether every balance, control and handoff recorded since `since` held, with the
        failing record numbers. Returns its seq, or None if there was nothing to settle."""
        recs = [r for r in self._records[since:] if r["kind"] in ("reconcile", "control", "handoff")]
        if not recs:
            return None
        failed = [r["seq"] for r in recs if not r["data"]["ok"]]
        return self.check(subject, "every balance, control and handoff recorded in this stage held", not failed, cls="must", expected=len(recs),
                          observed={"held": len(recs) - len(failed), "of": len(recs), "failed_records": failed}, evidence=[])

    def conclude(self, subject, *, skipped_reason=""):
        """Derive and record the subject's status from its checks by rule R1. Returns the status."""
        seqs = self._pending.pop(subject, [])
        checks = [self._records[s]["data"] for s in seqs]
        status = rule_r1(checks)
        reasons = [f'{c["class"]}: {c["name"]}' for c in checks if not c["ok"] and c["class"] != "info"]
        if skipped_reason:
            reasons = [skipped_reason]
        self.last_verdict_seq = self.append("verdict", {"subject": subject, "status": status, "rule": "R1", "from": seqs, "reasons": reasons})
        return status

    def handoff(self, frm, to, artifact, *, schema, via="", consumer_saw="", derived_from=None, note=""):
        """Data moving from one tool to the next. `artifact` is a ref from put(). `consumer_saw` is the SHA-256 the
        receiving side computed over the bytes it actually read; the two must be equal."""
        ok = consumer_saw == artifact["sha256"]
        return self.append("handoff", {"from": frm, "to": to, "schema": schema, "via": via, "artifact": artifact,
                                       "consumer_saw": consumer_saw, "derived_from": sorted(derived_from or []),
                                       "ok": bool(ok), "note": note})

    def reconcile(self, name, a, b, *, a_source, b_source, tol=0, why="", basis=None, evidence=None):
        """Two measurements of one fact. Integers (within `tol`) or strings (equal). `basis` says what kind of comparison it is, so
        a reader can tell them apart: `independent` (two different means of measuring), `consistency` (one source read twice, or
        announced against done) or `expectation` (a measurement against a stated constant). Optional; older runs have none."""
        if isinstance(a, str) or isinstance(b, str):
            ok = a == b
        else:
            ok = abs(int(a) - int(b)) <= int(tol)
        data = {"name": name, "a": a, "a_source": a_source, "b": b, "b_source": b_source, "tolerance": int(tol), "ok": bool(ok), "why": why}
        if basis is not None:
            data["basis"] = basis
        if evidence is not None:               # the commands whose output the two values were read from; optional, never defaulted
            data["evidence"] = list(evidence)
        return self.append("reconcile", data)

    def control(self, name, *, planted, expected, observed, evidence=None):
        """A deliberate defect and the reaction it must provoke. ok means the reaction was the expected one."""
        ev = list(evidence) if evidence is not None else self._scope_execs()
        expected, observed = str(expected), str(observed)
        return self.append("control", {"name": name, "planted": planted, "expected": expected, "observed": observed,
                                       "ok": expected == observed, "evidence": ev})

    def note(self, text, tag="note"):
        return self.append("note", {"tag": tag, "text": text})

    def close(self):
        """Seal the run. Returns the head hash: the one string to publish, anchor and compare."""
        with self._lock:
            for subject, seqs in list(self._pending.items()):
                if seqs:
                    self.note(f"{len(seqs)} check(s) for {subject!r} were recorded but never concluded", tag="warning")
            first = self._records[0]
            tallies = {k: self._counts[k] for k in KINDS if k != "run.end"}
            verdicts = {}
            for r in self._records:
                if r["kind"] == "verdict":
                    verdicts[r["data"]["status"]] = verdicts.get(r["data"]["status"], 0) + 1
            seq = self.append("run.end", {"records": self._seq, "counts": tallies, "verdicts": verdicts,
                                          "started": first["ts"], "ok": all(
                                              r["data"].get("ok", True) for r in self._records if r["kind"] in ("reconcile", "control", "handoff"))})
            return self._records[seq]["hash"]

    # ------------------------------------------------------------ reading

    @property
    def head(self):
        return self._prev

    def records(self, kind=None):
        return [r for r in self._records if kind is None or r["kind"] == kind]

    def get(self, seq):
        return self._records[seq]


# ---------------------------------------------------------------- verification
#
# Two different questions, kept apart on purpose.
#   INTEGRITY  (codes E_*): is this the chain that was written? Hashes, order, objects, references, and whether every
#              derived flag (ok, status, counts) follows from the data it claims to summarise.
#   OUTCOME    (codes F_*): what do the honest records say happened? A balance that did not balance, a control that
#              provoked the wrong reaction, a handoff where the consumer read other bytes. These are true records of a
#              bad result, not tampering, so they do not break integrity. `clean` is integrity AND no failed outcome.

@dataclasses.dataclass
class VerifyReport:
    ok: bool            # integrity holds
    clean: bool         # integrity holds and no balance, control or handoff failed
    run: str
    records: int
    objects: int
    head: str
    problems: list      # integrity
    findings: list      # outcome
    warnings: list
    verdicts: dict

    def codes(self):
        return sorted({p["code"] for p in self.problems})

    def finding_codes(self):
        return sorted({p["code"] for p in self.findings})

    def as_dict(self):
        return dataclasses.asdict(self)


MAX_DEPTH = 64


def _check_value(v):
    """Reject what has no portable form: lone surrogates anywhere (keys included) and containers nested deeper than 64."""
    stack = [(v, 1)]
    while stack:
        x, d = stack.pop()
        if isinstance(x, str):
            if any("\ud800" <= ch <= "\udfff" for ch in x):
                raise ValueError("a lone surrogate cannot be written as UTF-8")
        elif isinstance(x, (list, dict)):
            if d > MAX_DEPTH:
                raise ValueError(f"nesting deeper than {MAX_DEPTH}")
            if isinstance(x, dict):
                stack.extend((k, d) for k in x)
                stack.extend((val, d + 1) for val in x.values())
            else:
                stack.extend((e, d + 1) for e in x)


def _loads(line):
    """Strict JSON: no NaN or Infinity, no duplicate object keys, no lone surrogates, nesting at most 64 deep."""
    def no_const(c):
        raise ValueError(f"{c} is not JSON")

    def no_dups(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                raise ValueError(f"duplicate key {k!r}")
            d[k] = v
        return d
    try:
        v = json.loads(line, parse_constant=no_const, object_pairs_hook=no_dups)
    except RecursionError:
        raise ValueError(f"nesting deeper than {MAX_DEPTH}") from None
    _check_value(v)
    return v


def verify(path, *, expect_head=None, allow_open=False):
    """Re-derive everything. Trusts nothing stored in the run: not its hashes, not its flags, not its verdicts.
    The procedure is CUSTODY.md section 5; this is one of two independent implementations of it."""
    path = Path(path)
    problems, findings, warnings = [], [], []

    def bad(code, seq, msg):
        problems.append({"code": code, "seq": seq, "msg": msg})

    def found(code, seq, msg):
        findings.append({"code": code, "seq": seq, "msg": msg})

    chain = path / "chain.jsonl"
    if not chain.exists():
        return VerifyReport(False, False, path.name, 0, 0, "", [{"code": "E_PARSE", "seq": -1, "msg": "no chain.jsonl"}], [], [], {})
    recs = []
    for n, raw in enumerate(chain.read_bytes().split(b"\n")):
        try:
            line = raw.decode("utf-8")
        except UnicodeDecodeError:
            bad("E_PARSE", n, f"line {n + 1} is not valid UTF-8")
            continue
        if not line.strip(" \t\r"):
            continue
        try:
            recs.append(_loads(line))
        except ValueError as ex:
            bad("E_PARSE", n, f"line {n + 1} is not JSON: {ex}")
    run = recs[0].get("run", "") if recs and isinstance(recs[0], dict) and isinstance(recs[0].get("run"), str) else ""
    prev, last_ts, ended = ZERO, "", None
    by_seq = {}                 # fully valid records only: the only ones anything may cite
    counts = {k: 0 for k in KINDS}
    seen_objs = set()
    # ---- V2: per record, envelope level
    usable = []                 # (position, record) for envelope-valid, float-free records
    for i, r in enumerate(recs):
        flo = plain_problems(r)
        if flo:
            bad("E_FLOAT", i, flo[0])       # a record holding a float has no defined canonical form: otherwise ignored
            continue
        env = schemas.validate(r, schemas.ENVELOPE)
        if env:
            bad("E_SCHEMA", i, "envelope: " + env[0])
            continue
        usable.append((i, r))
        if r["run"] != run:
            bad("E_SCHEMA", i, f"run {r['run']!r} differs from the run's {run!r}")
        if r["seq"] != i:
            bad("E_SEQ", i, f"record at position {i} says seq {r['seq']}")
        if r["prev"] != prev:
            bad("E_PREV", i, "prev does not equal the hash of the record before")
        if sha256(canon({k: v for k, v in r.items() if k != "hash"})) != r["hash"]:
            bad("E_HASH", i, "stored hash differs from the recomputed hash")
        prev = r["hash"]
        if r["ts"] < last_ts:
            bad("E_ORDER", i, "timestamp goes backwards")
        last_ts = max(last_ts, r["ts"])
        if ended is not None:
            bad("E_END", i, "record after run.end")
        if r["kind"] == "run.end":
            ended = i
        if i == 0 and r["kind"] != "run.start":
            bad("E_SCHEMA", 0, "first record is not run.start")
        if i > 0 and r["kind"] == "run.start":
            bad("E_SCHEMA", i, "second run.start")
        counts[r["kind"]] += 1

    def ref_ok(ref, seq, what):
        h = ref["sha256"]
        seen_objs.add(h)
        f = path / "objects" / h[:2] / h
        if not f.is_file():
            bad("E_OBJ_MISSING", seq, f"{what}: object {h[:12]} is missing")
            return
        data = f.read_bytes()
        if sha256(data) != h:
            bad("E_OBJ_HASH", seq, f"{what}: object {h[:12]} bytes do not hash to their name")
        elif len(data) != ref["bytes"]:
            bad("E_OBJ_SIZE", seq, f"{what}: object {h[:12]} is {len(data)} bytes, record says {ref['bytes']}")

    # ---- V3: data level. Pass one decides which records are fully valid (so later references can be judged).
    valid = {}
    for i, r in usable:
        errs = schemas.validate(r["data"], schemas.DATA[r["kind"]])
        if errs:
            bad("E_SCHEMA", i, f"{r['kind']} data: " + errs[0])
        else:
            valid[i] = r
    by_seq = valid
    verdict_from, verdicts, outcome_ok = set(), {}, True

    def earlier(items, seq, kind, what):
        for e in items:
            if e not in by_seq or by_seq[e]["kind"] != kind or e >= seq:
                bad("E_REF", seq, f"{what} {e} is not an earlier {kind} record")

    for i, r in sorted(valid.items()):
        k, d = r["kind"], r["data"]
        if k in CITES_COMMANDS:
            earlier(d.get("evidence", []), i, "exec", f"{k} evidence")
        if k == "exec":
            ref_ok(d["stdout"], i, "stdout")
            ref_ok(d["stderr"], i, "stderr")
        elif k == "handoff":
            ref_ok(d["artifact"], i, "handoff artifact")
            same = d["consumer_saw"] == d["artifact"]["sha256"]
            if d["ok"] != same:
                bad("E_HANDOFF", i, "ok flag disagrees with consumer_saw versus artifact")
            if not same:
                found("F_HANDOFF", i, f"{d['from']} -> {d['to']}: the consumer read different bytes than the producer made")
                outcome_ok = False
            for h in d["derived_from"]:
                seen_objs.add(h)
                if not (path / "objects" / h[:2] / h).is_file():
                    bad("E_HANDOFF", i, f"derived_from {h[:12]} is not an object in this run")
        elif k == "reconcile":
            a, b = d["a"], d["b"]
            same = (a == b) if (isinstance(a, str) or isinstance(b, str)) else abs(a - b) <= d["tolerance"]
            if same != d["ok"]:
                bad("E_RECONCILE", i, "ok flag disagrees with a, b and tolerance")
            if not same:
                found("F_RECONCILE", i, f"{d['name']}: {a!r} versus {b!r} (tolerance {d['tolerance']})")
                outcome_ok = False
        elif k == "control":
            same = d["expected"] == d["observed"]
            if same != d["ok"]:
                bad("E_CONTROL", i, "ok flag disagrees with expected versus observed")
            if not same:
                found("F_CONTROL", i, f"{d['name']}: expected {d['expected']!r}, observed {d['observed']!r}")
                outcome_ok = False
        elif k == "verdict":
            cks = []
            for q in d["from"]:
                if q not in by_seq or by_seq[q]["kind"] != "check" or q >= i:
                    bad("E_REF", i, f"verdict cites {q}, which is not an earlier check record")
                else:
                    cks.append(by_seq[q]["data"])
                if q in verdict_from:
                    bad("E_REF", i, f"check {q} is cited more than once")
                verdict_from.add(q)
            want = rule_r1(cks)
            if want != d["status"]:
                bad("E_VERDICT", i, f"{d['subject']}: recorded {d['status']!r}, rule R1 gives {want!r}")
            verdicts[want] = verdicts.get(want, 0) + 1
            if want == "fail":
                found("F_VERDICT", i, f"{d['subject']} failed: " + "; ".join(d["reasons"]))

    # ---- V4: the seal
    if ended is None:
        if not allow_open:
            bad("E_END", len(recs) - 1, "the run was never closed (no run.end)")
    elif ended in valid:
        d = valid[ended]["data"]
        expect = {k: counts[k] for k in KINDS if k != "run.end"}
        if d["records"] != ended or d["counts"] != expect:
            bad("E_END", ended, "run.end tallies do not match the chain")
        if d["verdicts"] != verdicts:
            bad("E_END", ended, "run.end verdict tally does not match the verdicts in the chain")
        if d["ok"] != outcome_ok:
            bad("E_END", ended, "run.end ok flag does not match the outcome of the balances, controls and handoffs")
    # ---- V5 / V6
    objdir = path / "objects"
    on_disk = {p.name for p in objdir.glob("*/*") if p.is_file() and not p.name.endswith(".tmp")} if objdir.is_dir() else set()
    for h in sorted(on_disk - seen_objs):
        warnings.append({"code": "W_ORPHAN", "seq": -1, "msg": f"object {h[:12]} is not referenced by any record"})
    head = recs[-1]["hash"] if recs and isinstance(recs[-1], dict) and isinstance(recs[-1].get("hash"), str) else ""
    if expect_head and head != expect_head:
        bad("E_HEAD", len(recs) - 1, f"head {head[:12]} is not the expected {expect_head[:12]}")
    return VerifyReport(not problems, not problems and not findings, run, len(recs), len(on_disk), head,
                        problems, findings, warnings, verdicts)
