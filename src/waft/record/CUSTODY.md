# The Logbook: format and verification, version 1

This is the specification of the evidence the FogSift system produces. It is written so that someone who has never seen
the Python code can write a verifier from it. One has been written that way (`logbook/verify.mjs`, in Node, by an agent
that was given only this file), and the two implementations are compared on every tampered run in `tests/corpus.py`.
Where they disagreed, this file was wrong or one of them was; the commit history of this file shows which.

## What it is for

A summary ("4 pass") asks the reader to trust the author. A Logbook run does not. It keeps every command that was run
and its raw output; each check and control names the commands it rests on (`evidence[]`); a balance records its two values and
where each came from (a label, and optionally the commands); a handoff records the hash of the bytes the receiver read; and one rule turns
checks into a status. Each record is hashed together with the hash of the record before it, so a record cannot be changed,
removed or reordered without the chain showing it.

What verification **does not** check, stated here so nobody has to find it out: it does not re-measure a claim (a recorded
count is verified to be the recorded count, never that the count is true); it covers the parsed content of each record and
the bytes of each stored output, not the bytes of `chain.jsonl` itself (key order, whitespace, line endings and an extra
unreferenced object do not change the result; keep the files in git, or hash the file, if those bytes matter); and a balance
names its sources by label, and may (a balance) or must (a check or control) also list the commands it rests on; a balance
measured in-process from files cites none and leaves no raw bytes to open.

What a Logbook is **not**: tamper-proof. Whoever can rewrite every record and recompute every hash makes a chain that is
internally consistent. The defence is an **anchor**: the head hash written down somewhere the forger cannot reach (a git
commit, a log entry, a message to someone else). `expect_head` checks it. Section 7 shows both the attack and the defence.

## 1. Layout

```
<run>/chain.jsonl                one JSON record per line, in order, "\n" separated, UTF-8
<run>/objects/<h[0:2]>/<h>       raw bytes, named by their own lowercase hex SHA-256 <h>
```

Run directory names look like `20261025T170000Z-prove-a1b2`. The name is a label only; the `run` field inside the records
is authoritative.

## 2. Canonical JSON and hashing

`canon(x)` is the UTF-8 encoding of the JSON text of `x` with: object keys sorted by Unicode code point, no whitespace
(`","` and `":"` as separators), strings escaped only where JSON requires it (`"` `\` and control characters below
U+0020; `\b \t \n \f \r` for the five that have short forms, `\u00xx` in lowercase hex for the rest), non-ASCII
characters written as themselves, and no `NaN` or infinity.

`sha256(bytes)` is the lowercase hex SHA-256.

**Records contain no floating-point numbers.** The only numbers allowed are integers written without `.`, `e` or `E`
whose magnitude is at most 2^53, so every language reads them exactly. A number token that is anything else (`1.0`, `1e5`,
`0.5`, 2^60) is reported as `E_FLOAT`. A fraction travels as a decimal string (`"0.95"`); the Python helper is `dec()`.

**Strict JSON.** All of the following are `E_PARSE` (and the line is dropped, V1):

- `NaN`, `Infinity` and `-Infinity`;
- a duplicate key within one object (keys are compared after unescaping, so `"a"` and `"\u0061"` are the same key);
- a byte order mark outside a string (a U+FEFF *inside* a string is an ordinary character), invalid UTF-8 (overlong
  forms, encoded surrogates and values above U+10FFFF are invalid), and any other syntax error;
- a lone surrogate, written as an escape such as `\ud800` anywhere, keys included, because it has no UTF-8 form;
- containers nested too deeply: the top-level value is at depth 1 and every array or object inside a container adds
  one (scalars add nothing); a container at depth 65 is an error. (Real records are about 6 deep.)

`-0` is the integer 0 and is canonicalised as `0`.

## 3. The record

```json
{"schema":"fogsift.logbook.record/1","run":"<run id>","seq":0,"ts":"2026-10-25T17:00:00Z","kind":"run.start",
 "data":{...},"prev":"<64 zeros for seq 0, else the hash of the previous record>","hash":"<see below>"}
```

`hash = sha256(canon(record without the "hash" field))`.

`ts` is UTC in the form `YYYY-MM-DDTHH:MM:SSZ`; timestamps never go backwards (compared as strings).

An **artifact reference** (`ref`) is `{"name":str,"sha256":hex,"bytes":int,"media":str,"determinism":"exact"|"semantic"|"volatile"}`.
The bytes live at `objects/<sha256[0:2]>/<sha256>` and must hash to their own name and be exactly `bytes` long.

### Kinds and their schemas

The JSON Schemas in `schemas/` are **normative**: `schemas/envelope.json` for the record, `schemas/data.<kind>.json` for each
kind's `data`, and `schemas/ref.json` for artifact references. The table below summarises them. The validator
implements exactly this subset of JSON Schema and nothing else: `type` (`object`, `array`, `string`, `integer`,
`boolean`, `null`, or a list of them; a boolean is **not** an integer), `enum`, `const` (both: same JSON type and value, so
`1` is not `true`), `required`, `properties`, `additionalProperties` (a schema applied to every key not in `properties`),
`items`, `minItems`, `minimum`, and `pattern` (the whole string must match; the patterns use only literals, `[0-9a-f]`
classes and `{n}` repeats). Keys not mentioned in a schema are allowed. A verifier loads `envelope.json` and the nine
`data.<kind>.json` files; each is self-contained (the artifact reference is written out inside them; `ref.json` is only a
convenience copy of it). A verifier that cannot load a schema must refuse to run (print an error, exit 2) rather than
guess. Keywords outside the subset are ignored.

| kind | `data` fields | meaning |
|---|---|---|
| `run.start` | `label`, `scenario`, `argv[]`, `api_version`, `meta{}`, `git{head,branch,dirty_paths}`, `host{platform,machine,python,cpus}`, optional `pins{}` and `pins_sha256` | where and on what the run happened. Always `seq` 0, once |
| `exec` | `argv[]`, `cwd`, `env_overlay{}`, `isolated`, `stdin_sha256`, `rc`, `ms`, `started`, `timed_out`, `stdout` ref, `stderr` ref, `redactions`, `truncated`, `purpose`, `component` | one command and everything it printed |
| `check` | `component`, `name`, `class` (`must`,`should`,`gap`,`info`), `ok`, `expected`, `observed`, `detail`, `evidence[]` (positions of earlier `exec` records) | one claim, with what was expected and what was seen |
| `handoff` | `from`, `to`, `schema`, `via`, `artifact` ref, `consumer_saw`, `derived_from[]` (sha256s), `ok`, `note` | data passing from one tool to the next. `consumer_saw` is the SHA-256 the receiving side computed over the bytes it read |
| `reconcile` | `name`, `a`, `a_source`, `b`, `b_source`, `tolerance`, `ok`, `why`, optional `basis` (`independent`, `consistency`, `expectation`), optional `evidence[]` | two measurements of one fact. `basis` says what kind: two different means of measuring, one source read twice or announced against done, or a measurement against a stated constant. `evidence[]`, when present, lists the earlier `exec` records the values were read from. Verifiers ignore `basis` beyond its schema |
| `control` | `name`, `planted`, `expected`, `observed`, `ok`, `evidence[]` | a deliberate defect, and the reaction it must provoke |
| `verdict` | `subject`, `status` (`pass`,`warn`,`fail`,`skip`), `rule` (`"R1"`), `from[]` (positions of earlier `check` records), `reasons[]` | the status of a component or stage, derived by rule R1 |
| `note` | `tag`, `text` | something a human should read (a skip, a warning, a disclosure) |
| `run.end` | `records`, `counts{kind:int}`, `verdicts{status:int}`, `started`, `ok` | the seal. Always last, once |

Secrets never enter the store: output is passed through a redactor before it is hashed, and the number of replacements is
recorded in `redactions`.

### Rule R1 (how a status is made)

Given the `data` of the `check` records a verdict cites:

1. no checks: `skip` (no evidence, no claim, so it cannot pass)
2. any check with `class` `must` and `ok` false: `fail`
3. else any check with `class` `should` or `gap` and `ok` false: `warn`
4. else `pass`. (`info` checks never change a status.)

`gap` means a known defect shipped in a tool: the check passes when the defect is gone, so a closed gap shows up as a
change, not as silence.

## 4. Two questions, kept apart

- **Integrity** (codes `E_*`): is this the chain that was written, and does every flag in it follow from the data it
  summarises? `ok` means no `E_*`.
- **Outcome** (codes `F_*`): what do the honest records say happened? A balance that did not balance is a true record of
  a bad result, not tampering. `clean` means `ok` and no `F_*`.

## 5. Verification procedure

Input: a run directory; optionally `expect_head` and `allow_open`. Output: the lists below, the head, `run` (see V1)
and `records` (the number of values that survived V1).

**V0.** If `chain.jsonl` does not exist, is not a regular file or cannot be read: `E_PARSE`, stop (not ok). A missing `objects/`
directory is not an error by itself (references into it are then missing). Symbolic links are followed.

**V1. Parse.** Read the file as bytes and split on byte `0x0A`. For each piece: if it is not valid UTF-8, `E_PARSE` and drop it;
if it is empty or contains only spaces, tabs and carriage returns, skip it silently; otherwise parse it as strict JSON
(section 2), and on any error `E_PARSE` and drop it. `recs` is the list of surviving values; **`i` below is an index into
`recs` and is the only meaning of "position" or "record N" in this document.** `run` is `recs[0].run` if `recs[0]` is an
object whose `run` is a string, else `""`.

**V2. Per record, in order.** State: running `prev` (64 zeros), `lastTs` (empty string), `ended` (unset), and a count per
kind.

1. *Floats.* If the value contains anywhere a number token that is not an integer within +-2^53: `E_FLOAT`, and the record
   is **ignored entirely** (the rest of V2 and all of V3 are skipped; it does not change `prev`, `lastTs`, `ended` or the
   counts; it still occupies position `i`).
2. *Envelope.* Validate the value against `schemas/envelope.json`. If invalid: `E_SCHEMA`, and the record is ignored
   entirely, as in step 1. Otherwise the record is *envelope-valid*.
3. `E_SCHEMA` if `run` differs from the run's. `E_SEQ` if `seq != i`. `E_PREV` if `prev` is not the running `prev`. `E_HASH` if
   `sha256(canon(record without hash)) != hash`.
4. Set running `prev` to the record's stored `hash`.
5. `E_ORDER` if `ts < lastTs` (string comparison); then `lastTs = max(lastTs, ts)`.
6. `E_END` if `ended` is set. If this record's kind is `run.end`, set `ended = i`.
7. `E_SCHEMA` if `i == 0` and the kind is not `run.start`, or `i > 0` and the kind is `run.start`.
8. Add one to the count of this record's kind. (Counts cover every envelope-valid record in the file, valid data or not.)

**V3. Data.** For each envelope-valid record validate `data` against the schema for its kind. If invalid: `E_SCHEMA`, and the
record is **not citable** and gets no further checks. Otherwise the record is *valid* and joins the registry. A reference
"to record N" below means the valid record at index N, which must be of the stated kind and earlier than the citing one;
anything else is `E_REF`. Then, for each valid record in order:

- `exec`: *ref-check* `stdout` and `stderr`.
- *ref-check(ref)*: remember `ref.sha256` as referenced. `E_OBJ_MISSING` if there is no regular file `objects/<sha256[0:2]>/<sha256>` (a directory there counts as missing).
  Else `E_OBJ_HASH` if its bytes do not hash to the name; else `E_OBJ_SIZE` if its length is not `ref.bytes`.
- `check`, `control` and `reconcile`: every `evidence` entry (a `reconcile` may have none, and the field may be absent) must reference an earlier `exec` (`E_REF`).
- `handoff`: *ref-check* `artifact`. `same = (consumer_saw == artifact.sha256)`. `E_HANDOFF` if `ok != same`. If not `same`:
  outcome `F_HANDOFF`. For every `derived_from` hash: remember it as referenced, and `E_HANDOFF` if no regular file
  `objects/<h[0:2]>/<h>` exists (whether or not `same`).
- `reconcile`: if `a` or `b` is a string, `same = (a == b)` (a string never equals an integer); else `same = |a - b| <= tolerance`.
  `E_RECONCILE` if `ok != same`. If not `same`: outcome `F_RECONCILE`.
- `control`: `same = (expected == observed)` (both are strings). `E_CONTROL` if `ok != same`. If not `same`: outcome `F_CONTROL`.
  Every `evidence` entry must reference an earlier `exec` (`E_REF`).
- `verdict`: for every entry `q` of `from`, in order: if `q` does not reference an earlier valid `check`, `E_REF` (and the
  entry takes no part in R1); and if `q` has already been cited, by this verdict earlier in its own list or by any earlier
  verdict, `E_REF`; then mark `q` as cited (every entry is marked, valid or not; an entry already cited that does reference a valid
  earlier check still takes part in R1). `want = R1(the data of the entries that did reference a check)`. `E_VERDICT` if
  `status != want`. Add one to the tally for `want` (the recomputed status, not the stored one). If `want` is `fail`:
  outcome `F_VERDICT`.
- `run.start`, `note`, `run.end`: nothing further.

**V4. The seal.** If `ended` is unset: `E_END`, unless `allow_open`. Otherwise, if the record at `ended` is valid:
`E_END` if `data.records != ended`; or `data.counts` is not exactly the object with the eight keys `run.start exec check handoff
reconcile control verdict note`, each equal to its count from V2 (zeros included); or `data.verdicts` is not exactly the
tally from V3 (only statuses that occurred, no zeros); or `data.ok` differs from "no `F_HANDOFF`, `F_RECONCILE` or `F_CONTROL` was found"
(`F_VERDICT` does not count).

**V5. Objects.** The referenced set is every `ref.sha256` that a ref-check looked at plus every `derived_from` hash of a valid
`handoff`. Every regular file at `objects/*/*` (any shard directory; ignoring names that end `.tmp`) whose file name is not in the
referenced set is a warning `W_ORPHAN`. Warnings never affect `ok` or `clean`.

**V6. Anchor.** The head is the stored `hash` of the last value in `recs`, or `""` if there is none or it is not an object with a
string `hash`. If `expect_head` is given and differs (exact string comparison): `E_HEAD`.

`ok` = no `E_*`. `clean` = `ok` and no `F_*`. `finding_codes` lists the distinct `F_*` codes found.

## 6. Codes

| code | meaning |
|---|---|
| `E_PARSE` | a line is not JSON, or there is no chain |
| `E_SCHEMA` | missing envelope field, wrong schema/kind/run, wrong first/second record, or a malformed record |
| `E_SEQ` | a record's `seq` is not its position (a record was deleted, inserted or reordered) |
| `E_PREV` | a record does not point at the hash of the one before it |
| `E_HASH` | a record's content does not match its hash |
| `E_FLOAT` | a floating-point number in a record |
| `E_ORDER` | timestamps run backwards |
| `E_END` | missing, early or inconsistent `run.end` (including records after it) |
| `E_OBJ_MISSING` / `E_OBJ_HASH` / `E_OBJ_SIZE` | a referenced output is gone, altered, or the wrong length |
| `E_REF` | evidence or a verdict cites something it may not |
| `E_HANDOFF` / `E_RECONCILE` / `E_CONTROL` | a derived flag disagrees with the data it summarises, or lineage names an absent object |
| `E_VERDICT` | a verdict is not what rule R1 gives for its checks |
| `E_HEAD` | the head is not the anchored one |
| `F_HANDOFF` / `F_RECONCILE` / `F_CONTROL` / `F_VERDICT` | outcome: honest records of a failed handoff, balance, control, or a failing component |
| `W_ORPHAN` | an object nothing refers to |

## 7. The attack that needs an anchor

`tests/corpus.py` contains 43 named tampers (a flipped byte, an edited record, a deleted record, a forger who re-chains
everything and flips a must-check, a wrong type, a duplicated key, ...), and the corpus has 45 cases: the valid run, those 43, and one
honest bad outcome. All but one are caught by the chain alone. The exception is the **perfect
forgery**: change an observed value and recompute every later hash. The result is internally consistent, so `verify`
accepts it, and the test asserts that it does. It fails only against the anchored head:

```
verify(run)                         -> ok
verify(run, expect_head=<anchor>)   -> E_HEAD
```

So the head hash of a published run is written to `sessions/LOG.md` and `STATE.md` in a commit other than the one that
adds the run, and again in `logbook/HEADS.txt`. A reader should compare the head they computed with the one in the log.

## 8. Determinism classes (for reproduction)

Every artifact reference says how it should behave when the same scenario is run again on another machine:

- `exact`: the bytes must be identical (a seeded, offline computation).
- `semantic`: identical after the producer's volatile fields (ids, dates, paths) are removed; `fogsift repro` compares the
  normalised form.
- `volatile`: informational (timings, raw tool output).

## 9. Writing a verifier

You need SHA-256, a strict JSON parser that lets you see the raw number tokens and duplicate keys, the canonical form in
section 2, and the schemas in `schemas/`. The reference implementations are `fogsift_api/custody.py` (`verify`, standard
library only) and `logbook/verify.mjs` (Node, no dependencies, written from this file by an agent that had not seen the Python).

To test yours, generate the cases and the expected answers with `python3 fogsift.py corpus OUT_DIR`: it writes `case-NN/`
directories (shuffled, with neutral names) and `expected.json` mapping each to the `ok`, `clean` and code sets the reference
verifier reports, plain and with the corpus head as `expect_head`. Then run `python3 tests/crosscheck_fuzz.py`, which
applies hundreds of random corruptions and requires the two verifiers to agree on every one.
