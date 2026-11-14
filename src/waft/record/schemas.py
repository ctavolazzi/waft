"""JSON Schemas for every Logbook record, and the small validator that applies them.

These schemas are NORMATIVE: CUSTODY.md says a record whose `data` does not validate against the schema for its kind is
malformed (E_SCHEMA), and the writer (`Logbook.append`) refuses to write one. They are exported to `schemas/*.json` so a
verifier in another language can load them; tests/test_schemas.py proves the exported files equal these definitions.

The validator implements exactly this subset of JSON Schema (so that two implementations cannot differ on a keyword
neither supports):

    type            "object" "array" "string" "integer" "boolean" "null", or a list of them. A bool is NOT an integer.
    enum            instance equals one of the listed values (same JSON type and value)
    const           instance equals the value
    required        every listed key is present in an object
    properties      each listed key that is present validates against its schema
    additionalProperties   a schema: every key NOT in `properties` validates against it (a boolean is not supported)
    items           every array element validates against the schema
    minItems        arrays have at least this many elements
    minimum         integers are at least this
    pattern         the WHOLE string matches the regular expression (anchored at both ends); patterns here use only
                    [0-9a-f] style classes, {n} repeats and literals, so Python and ECMAScript agree
"""
import re

HEX64 = "[0-9a-f]{64}"
TS = "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z"
KINDS = ("run.start", "exec", "check", "handoff", "reconcile", "control", "verdict", "note", "run.end")

S = {"type": "string"}
I = {"type": "integer"}
I0 = {"type": "integer", "minimum": 0}
B = {"type": "boolean"}
STRS = {"type": "array", "items": S}
SEQS = {"type": "array", "items": I0}
REF = {"type": "object", "required": ["name", "sha256", "bytes", "media", "determinism"],
       "properties": {"name": S, "sha256": {"type": "string", "pattern": HEX64}, "bytes": I0, "media": S,
                      "determinism": {"enum": ["exact", "semantic", "volatile"]}}}


def obj(required, **props):
    return {"type": "object", "required": list(required), "properties": props}


ENVELOPE = obj(["schema", "run", "seq", "ts", "kind", "data", "prev", "hash"],
               schema={"const": "fogsift.logbook.record/1"}, run=S, seq=I0, ts={"type": "string", "pattern": TS},
               kind={"enum": list(KINDS)}, data={"type": "object"},
               prev={"type": "string", "pattern": HEX64}, hash={"type": "string", "pattern": HEX64})

DATA = {
    "run.start": obj(["label", "scenario", "argv", "api_version", "meta", "git", "host"],
                     label=S, scenario=S, argv=STRS, api_version=S, meta={"type": "object"},
                     git=obj(["head", "branch", "dirty_paths"], head=S, branch=S, dirty_paths=I0),
                     host=obj(["platform", "machine", "python", "cpus"], platform=S, machine=S, python=S, cpus=I0),
                     pins={"type": "object"}, pins_sha256={"type": "string", "pattern": HEX64}),
    "exec": obj(["argv", "cwd", "env_overlay", "isolated", "stdin_sha256", "rc", "ms", "started", "timed_out", "stdout",
                 "stderr", "redactions", "truncated", "purpose", "component"],
                argv=STRS, cwd=S, env_overlay={"type": "object", "additionalProperties": S}, isolated=B, stdin_sha256=S,
                rc=I, ms=I0, started=S, timed_out=B, stdout=REF, stderr=REF, redactions=I0, truncated=B, purpose=S, component=S),
    "check": obj(["component", "name", "class", "ok", "expected", "observed", "detail", "evidence"],
                 component=S, name=S, **{"class": {"enum": ["must", "should", "gap", "info"]}}, ok=B, expected={}, observed={},
                 detail=S, evidence=SEQS),
    "handoff": obj(["from", "to", "schema", "via", "artifact", "consumer_saw", "derived_from", "ok", "note"],
                   **{"from": S}, to=S, schema=S, via=S, artifact=REF, consumer_saw=S,
                   derived_from={"type": "array", "items": {"type": "string", "pattern": HEX64}}, ok=B, note=S),
    "reconcile": obj(["name", "a", "a_source", "b", "b_source", "tolerance", "ok", "why"],
                     name=S, a={"type": ["integer", "string"]}, a_source=S, b={"type": ["integer", "string"]}, b_source=S,
                     tolerance=I0, ok=B, why=S, basis={"enum": ["independent", "consistency", "expectation"]}, evidence=SEQS),
    "control": obj(["name", "planted", "expected", "observed", "ok", "evidence"],
                   name=S, planted=S, expected=S, observed=S, ok=B, evidence=SEQS),
    "verdict": obj(["subject", "status", "rule", "from", "reasons"],
                   subject=S, status={"enum": ["pass", "warn", "fail", "skip"]}, rule={"const": "R1"}, **{"from": SEQS}, reasons=STRS),
    "note": obj(["tag", "text"], tag=S, text=S),
    "run.end": obj(["records", "counts", "verdicts", "started", "ok"],
                   records=I0, counts={"type": "object", "additionalProperties": I0}, verdicts={"type": "object", "additionalProperties": I0},
                   started=S, ok=B),
}

# Other documents the system exchanges (the API's request and response bodies) are in api_schemas.py.


def _is(inst, t):
    if t == "object":
        return isinstance(inst, dict)
    if t == "array":
        return isinstance(inst, list)
    if t == "string":
        return isinstance(inst, str)
    if t == "integer":
        return isinstance(inst, int) and not isinstance(inst, bool)
    if t == "boolean":
        return isinstance(inst, bool)
    if t == "null":
        return inst is None
    raise ValueError(f"unsupported type {t!r}")


def _same(a, b):
    """JSON equality: same type and value (so 1 is not true)."""
    if isinstance(a, bool) != isinstance(b, bool):
        return False
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_same(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b))
    return type(a) is type(b) and a == b


def validate(inst, schema, path="$"):
    """Returns a list of error strings; empty means valid."""
    errs = []
    if "type" in schema:
        ts = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_is(inst, t) for t in ts):
            return [f"{path}: expected {'/'.join(ts)}"]
    if "const" in schema and not _same(inst, schema["const"]):
        errs.append(f"{path}: must equal {schema['const']!r}")
    if "enum" in schema and not any(_same(inst, v) for v in schema["enum"]):
        errs.append(f"{path}: must be one of {schema['enum']}")
    if "pattern" in schema and isinstance(inst, str) and not re.fullmatch(schema["pattern"], inst):
        errs.append(f"{path}: does not match {schema['pattern']}")
    if "minimum" in schema and _is(inst, "integer") and inst < schema["minimum"]:
        errs.append(f"{path}: below {schema['minimum']}")
    if isinstance(inst, dict):
        for k in schema.get("required", []):
            if k not in inst:
                errs.append(f"{path}: missing {k}")
        props = schema.get("properties", {})
        for k, sub in props.items():
            if k in inst:
                errs += validate(inst[k], sub, f"{path}.{k}")
        extra = schema.get("additionalProperties")
        if isinstance(extra, dict):
            for k, v in inst.items():
                if k not in props:
                    errs += validate(v, extra, f"{path}.{k}")
    if isinstance(inst, list):
        if "minItems" in schema and len(inst) < schema["minItems"]:
            errs.append(f"{path}: fewer than {schema['minItems']} items")
        if "items" in schema:
            for i, v in enumerate(inst):
                errs += validate(v, schema["items"], f"{path}[{i}]")
    return errs


def all_schemas():
    """name -> schema, as exported to schemas/*.json"""
    out = {"envelope": ENVELOPE}
    out.update({f"data.{k}": v for k, v in DATA.items()})
    out["ref"] = REF
    return out
