#!/usr/bin/env node
// Logbook verifier, written from CUSTODY.md (sections 2, 3, 5, 6) and the schemas in ../schemas.
// Usage: node logbook/verify.mjs <run_dir> [--expect-head <hex>] [--allow-open] [--schemas DIR]
// Prints one line of JSON. Exit 0 clean, 1 ok but not clean, 2 not ok.
// Dependencies: node:crypto, node:fs, node:path, node:url only.

import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ZERO64 = '0'.repeat(64);
const KIND_ORDER = ['run.start', 'exec', 'check', 'handoff', 'reconcile', 'control', 'verdict', 'note'];
const CITES_COMMANDS = ['check', 'control', 'reconcile'];   // kinds whose evidence[] lists the exec records they rest on
const ALL_KINDS = [...KIND_ORDER, 'run.end'];
const TWO53 = 2n ** 53n;
const MAX_DEPTH = 64;

// ---------------------------------------------------------------- strict JSON
// RFC 8259 grammar only. Reports (by throwing) any syntax error and any duplicate key.
// Remembers whether any number token was not an integer within +-2^53 (a "float").
// Objects are null-prototype so "__proto__" is an ordinary key.

class Parser {
  constructor(s) { this.s = s; this.i = 0; this.float = false; }
  fail() { throw new SyntaxError('json'); }
  ws() {
    const s = this.s;
    while (this.i < s.length) {
      const c = s.charCodeAt(this.i);
      if (c === 0x20 || c === 0x09 || c === 0x0a || c === 0x0d) this.i++; else break;
    }
  }
  value(depth) {
    this.ws();
    const s = this.s;
    if (this.i >= s.length) this.fail();
    const c = s[this.i];
    if (c === '{') return this.object(depth);
    if (c === '[') return this.array(depth);
    if (c === '"') return this.string();
    if (c === '-' || (c >= '0' && c <= '9')) return this.number();
    if (s.startsWith('true', this.i)) { this.i += 4; return true; }
    if (s.startsWith('false', this.i)) { this.i += 5; return false; }
    if (s.startsWith('null', this.i)) { this.i += 4; return null; }
    return this.fail();
  }
  object(depth) {
    if (depth + 1 > MAX_DEPTH) this.fail();   // this container is at depth+1
    const o = Object.create(null);
    this.i++; this.ws();
    if (this.s[this.i] === '}') { this.i++; return o; }
    for (;;) {
      this.ws();
      if (this.s[this.i] !== '"') this.fail();
      const k = this.string();
      if (k in o) this.fail();            // duplicate key (compared after unescaping)
      this.ws();
      if (this.s[this.i] !== ':') this.fail();
      this.i++;
      o[k] = this.value(depth + 1);
      this.ws();
      const c = this.s[this.i];
      if (c === ',') { this.i++; continue; }
      if (c === '}') { this.i++; return o; }
      this.fail();
    }
  }
  array(depth) {
    if (depth + 1 > MAX_DEPTH) this.fail();
    const a = [];
    this.i++; this.ws();
    if (this.s[this.i] === ']') { this.i++; return a; }
    for (;;) {
      a.push(this.value(depth + 1));
      this.ws();
      const c = this.s[this.i];
      if (c === ',') { this.i++; continue; }
      if (c === ']') { this.i++; return a; }
      this.fail();
    }
  }
  hex4(pos) {
    const h = this.s.slice(pos, pos + 4);
    if (!/^[0-9a-fA-F]{4}$/.test(h)) this.fail();
    return parseInt(h, 16);
  }
  string() {
    const s = this.s;
    this.i++; // opening quote
    let out = '';
    let chunk = this.i;
    for (;;) {
      if (this.i >= s.length) this.fail();
      const c = s.charCodeAt(this.i);
      if (c === 0x22) { out += s.slice(chunk, this.i); this.i++; return out; }
      if (c < 0x20) this.fail();
      if (c === 0x5c) {
        out += s.slice(chunk, this.i);
        this.i++;
        const e = s[this.i];
        switch (e) {
          case '"': out += '"'; break;
          case '\\': out += '\\'; break;
          case '/': out += '/'; break;
          case 'b': out += '\b'; break;
          case 'f': out += '\f'; break;
          case 'n': out += '\n'; break;
          case 'r': out += '\r'; break;
          case 't': out += '\t'; break;
          case 'u': {
            const cu = this.hex4(this.i + 1);
            if (cu >= 0xd800 && cu <= 0xdbff) {
              if (s[this.i + 5] !== '\\' || s[this.i + 6] !== 'u') this.fail();
              const lo = this.hex4(this.i + 7);
              if (lo < 0xdc00 || lo > 0xdfff) this.fail();
              out += String.fromCharCode(cu, lo);
              this.i += 10;
            } else if (cu >= 0xdc00 && cu <= 0xdfff) {
              this.fail();
            } else {
              out += String.fromCharCode(cu);
              this.i += 4;
            }
            break;
          }
          default: this.fail();
        }
        this.i++;
        chunk = this.i;
        continue;
      }
      this.i++;
    }
  }
  number() {
    const re = /-?(?:0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?/y;
    re.lastIndex = this.i;
    const m = re.exec(this.s);
    if (!m) this.fail();
    this.i = re.lastIndex;
    const tok = m[0];
    if (m[1] !== undefined || m[2] !== undefined) {
      this.float = true;
      return Number(tok);
    }
    const b = BigInt(tok);
    if (b > TWO53 || b < -TWO53) { this.float = true; return Number(tok); }
    return Number(b) + 0; // "-0" -> 0
  }
}

function parseLine(text) {
  const p = new Parser(text);
  const v = p.value(0);
  p.ws();
  if (p.i !== text.length) p.fail();
  return { v, fl: p.float };
}

// ------------------------------------------------------------------ canon
function cmpCodePoints(a, b) {
  const ia = a[Symbol.iterator](), ib = b[Symbol.iterator]();
  for (;;) {
    const x = ia.next(), y = ib.next();
    if (x.done && y.done) return 0;
    if (x.done) return -1;
    if (y.done) return 1;
    const cx = x.value.codePointAt(0), cy = y.value.codePointAt(0);
    if (cx !== cy) return cx < cy ? -1 : 1;
  }
}

function escStr(s) {
  let out = '"';
  for (const ch of s) {
    const c = ch.codePointAt(0);
    if (ch === '"') out += '\\"';
    else if (ch === '\\') out += '\\\\';
    else if (c === 0x08) out += '\\b';
    else if (c === 0x09) out += '\\t';
    else if (c === 0x0a) out += '\\n';
    else if (c === 0x0c) out += '\\f';
    else if (c === 0x0d) out += '\\r';
    else if (c < 0x20) out += '\\u00' + c.toString(16).padStart(2, '0');
    else out += ch;
  }
  return out + '"';
}

function canon(x, omitKey) {
  if (x === null) return 'null';
  switch (typeof x) {
    case 'boolean': return x ? 'true' : 'false';
    case 'number':
      if (!Number.isInteger(x)) throw new RangeError('non-integer');
      return Object.is(x, -0) ? '0' : String(x);
    case 'string': return escStr(x);
    case 'object': {
      if (Array.isArray(x)) return '[' + x.map((e) => canon(e)).join(',') + ']';
      const keys = Object.keys(x).filter((k) => k !== omitKey).sort(cmpCodePoints);
      return '{' + keys.map((k) => escStr(k) + ':' + canon(x[k])).join(',') + '}';
    }
    default: throw new TypeError('unsupported');
  }
}

const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');
const isObj = (x) => x !== null && typeof x === 'object' && !Array.isArray(x);
const has = (o, k) => Object.prototype.hasOwnProperty.call(o, k);
// same JSON type and same value (1 is not true, "1" is not 1)
function jeq(a, b) {
  try { return canon(a) === canon(b); } catch { return false; }
}

// ------------------------------------------------- schema validator (subset)
// type, enum, const, required, properties, additionalProperties, items, minItems,
// minimum, pattern. Anything else in a schema is ignored.

const patternCache = new Map();
function patternRe(p) {
  let re = patternCache.get(p);
  if (!re) { re = new RegExp('^(?:' + p + ')$'); patternCache.set(p, re); }
  return re;
}

function typeOk(t, v) {
  switch (t) {
    case 'object': return isObj(v);
    case 'array': return Array.isArray(v);
    case 'string': return typeof v === 'string';
    case 'integer': return typeof v === 'number' && Number.isInteger(v);
    case 'boolean': return typeof v === 'boolean';
    case 'null': return v === null;
    default: return false;
  }
}

function validate(schema, v) {
  if (has(schema, 'type')) {
    const ts = Array.isArray(schema.type) ? schema.type : [schema.type];
    if (!ts.some((t) => typeOk(t, v))) return false;
  }
  if (has(schema, 'enum') && !schema.enum.some((e) => jeq(e, v))) return false;
  if (has(schema, 'const') && !jeq(schema.const, v)) return false;
  if (typeof v === 'number' && has(schema, 'minimum') && v < schema.minimum) return false;
  if (typeof v === 'string' && has(schema, 'pattern') && !patternRe(schema.pattern).test(v)) return false;
  if (isObj(v)) {
    if (has(schema, 'required')) for (const k of schema.required) if (!has(v, k)) return false;
    const props = has(schema, 'properties') ? schema.properties : {};
    for (const k of Object.keys(props)) if (has(v, k) && !validate(props[k], v[k])) return false;
    if (has(schema, 'additionalProperties')) {
      for (const k of Object.keys(v)) if (!has(props, k) && !validate(schema.additionalProperties, v[k])) return false;
    }
  }
  if (Array.isArray(v)) {
    if (has(schema, 'minItems') && v.length < schema.minItems) return false;
    if (has(schema, 'items')) for (const e of v) if (!validate(schema.items, e)) return false;
  }
  return true;
}

function loadSchemas(dir) {
  const read = (f) => {
    const v = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
    if (!isObj(v)) throw new Error(f + ' is not a JSON object');
    return v;
  };
  const s = { envelope: read('envelope.json'), data: {} };
  for (const k of ALL_KINDS) s.data[k] = read('data.' + k + '.json');
  return s;
}

// R1 over the data of the cited check records
function r1(checks) {
  if (checks.length === 0) return 'skip';
  if (checks.some((c) => c.class === 'must' && c.ok === false)) return 'fail';
  if (checks.some((c) => (c.class === 'should' || c.class === 'gap') && c.ok === false)) return 'warn';
  return 'pass';
}

// ----------------------------------------------------------------- verify
function verify(runDir, expectHead, allowOpen, schemas) {
  const E = new Set(), F = new Set(), W = new Set();
  const add = (c) => (c[0] === 'E' ? E : c[0] === 'F' ? F : W).add(c);
  const recs = [];
  const flags = [];   // parallel to recs: value contained a float token
  let run = '';
  let head = '';

  const finish = () => {
    const codes = [...E].sort();
    const ok = codes.length === 0;
    const findings = [...F].sort();
    return {
      ok,
      clean: ok && findings.length === 0,
      run,
      records: recs.length,
      head,
      codes,
      finding_codes: findings,
      warning_codes: [...W].sort(),
    };
  };

  // V0
  let buf;
  try { buf = fs.readFileSync(path.join(runDir, 'chain.jsonl')); } catch { add('E_PARSE'); return finish(); }

  // V1
  const dec = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true });
  const pieces = [];
  {
    let start = 0;
    for (let k = 0; k < buf.length; k++) {
      if (buf[k] === 0x0a) { pieces.push(buf.subarray(start, k)); start = k + 1; }
    }
    pieces.push(buf.subarray(start));
  }
  for (const pb of pieces) {
    let text;
    try { text = dec.decode(pb); } catch { add('E_PARSE'); continue; }
    if (/^[ \t\r]*$/.test(text)) continue;
    try {
      const { v, fl } = parseLine(text);
      recs.push(v); flags.push(fl);
    } catch { add('E_PARSE'); }
  }
  run = isObj(recs[0]) && typeof recs[0].run === 'string' ? recs[0].run : '';

  // V2
  let prev = ZERO64;
  let lastTs = '';
  let ended = null;
  const kindCount = Object.fromEntries(ALL_KINDS.map((k) => [k, 0]));
  const envValid = recs.map(() => false);
  recs.forEach((rec, i) => {
    if (flags[i]) { add('E_FLOAT'); return; }
    if (!validate(schemas.envelope, rec)) { add('E_SCHEMA'); return; }
    envValid[i] = true;
    if (rec.run !== run) add('E_SCHEMA');
    if (rec.seq !== i) add('E_SEQ');
    if (rec.prev !== prev) add('E_PREV');
    if (sha256(Buffer.from(canon(rec, 'hash'), 'utf8')) !== rec.hash) add('E_HASH');
    prev = rec.hash;
    if (rec.ts < lastTs) add('E_ORDER');
    if (rec.ts > lastTs) lastTs = rec.ts;
    if (ended !== null) add('E_END');
    if (rec.kind === 'run.end') ended = i;
    if ((i === 0 && rec.kind !== 'run.start') || (i > 0 && rec.kind === 'run.start')) add('E_SCHEMA');
    kindCount[rec.kind]++;
  });

  // V3
  const valid = new Map();   // index -> record, for records whose data passed its schema
  recs.forEach((rec, i) => {
    if (!envValid[i]) return;
    if (validate(schemas.data[rec.kind], rec.data)) valid.set(i, rec); else add('E_SCHEMA');
  });
  const refTo = (n, kind, i) => {
    const r = valid.get(n);
    return r !== undefined && r.kind === kind && n < i ? r : null;
  };

  const referenced = new Set();
  const objFile = (h) => path.join(runDir, 'objects', h.slice(0, 2), h);
  const isFile = (p) => { try { return fs.statSync(p).isFile(); } catch { return false; } };
  const refCheck = (ref) => {
    const h = ref.sha256;
    referenced.add(h);
    const p = objFile(h);
    if (!isFile(p)) { add('E_OBJ_MISSING'); return; }
    let data;
    try { data = fs.readFileSync(p); } catch { add('E_OBJ_MISSING'); return; }
    if (sha256(data) !== h) { add('E_OBJ_HASH'); return; }
    if (data.length !== ref.bytes) add('E_OBJ_SIZE');
  };

  const tally = {};
  const cited = new Set();
  const indices = [...valid.keys()].sort((a, b) => a - b);
  for (const i of indices) {
    const rec = valid.get(i);
    const d = rec.data;
    if (CITES_COMMANDS.includes(rec.kind)) for (const e of d.evidence || []) if (!refTo(e, 'exec', i)) add('E_REF');
    switch (rec.kind) {
      case 'exec':
        refCheck(d.stdout);
        refCheck(d.stderr);
        break;
      case 'handoff': {
        refCheck(d.artifact);
        const same = d.consumer_saw === d.artifact.sha256;
        if (d.ok !== same) add('E_HANDOFF');
        if (!same) add('F_HANDOFF');
        for (const h of d.derived_from) {
          referenced.add(h);
          if (!isFile(objFile(h))) add('E_HANDOFF');
        }
        break;
      }
      case 'reconcile': {
        let same;
        if (typeof d.a === 'string' || typeof d.b === 'string') same = d.a === d.b;
        else {
          let diff = BigInt(d.a) - BigInt(d.b);
          if (diff < 0n) diff = -diff;
          same = diff <= BigInt(d.tolerance);
        }
        if (d.ok !== same) add('E_RECONCILE');
        if (!same) add('F_RECONCILE');
        break;
      }
      case 'control': {
        const same = d.expected === d.observed;
        if (d.ok !== same) add('E_CONTROL');
        if (!same) add('F_CONTROL');
        break;
      }
      case 'verdict': {
        const checks = [];
        for (const q of d.from) {
          const r = refTo(q, 'check', i);
          if (!r) add('E_REF'); else checks.push(r.data);
          if (cited.has(q)) add('E_REF');
          cited.add(q);
        }
        const want = r1(checks);
        if (d.status !== want) add('E_VERDICT');
        tally[want] = (tally[want] || 0) + 1;
        if (want === 'fail') add('F_VERDICT');
        break;
      }
      default: break; // run.start, note, run.end
    }
  }

  // V4
  if (ended === null) {
    if (!allowOpen) add('E_END');
  } else if (valid.has(ended)) {
    const d = valid.get(ended).data;
    if (d.records !== ended) add('E_END');
    const ck = Object.keys(d.counts).sort();
    const wantKeys = [...KIND_ORDER].sort();
    if (ck.length !== wantKeys.length || ck.some((k, j) => k !== wantKeys[j]) || KIND_ORDER.some((k) => d.counts[k] !== kindCount[k])) add('E_END');
    const vk = Object.keys(d.verdicts).sort();
    const tk = Object.keys(tally).sort();
    if (vk.length !== tk.length || vk.some((k, j) => k !== tk[j] || d.verdicts[k] !== tally[k])) add('E_END');
    if (d.ok !== !(F.has('F_HANDOFF') || F.has('F_RECONCILE') || F.has('F_CONTROL'))) add('E_END');
  }

  // V5
  try {
    const od = path.join(runDir, 'objects');
    for (const sub of fs.readdirSync(od)) {
      const sd = path.join(od, sub);
      let st;
      try { st = fs.statSync(sd); } catch { continue; }
      if (!st.isDirectory()) continue;
      for (const f of fs.readdirSync(sd)) {
        if (f.endsWith('.tmp')) continue;
        if (!isFile(path.join(sd, f))) continue;
        if (!referenced.has(f)) W.add('W_ORPHAN');
      }
    }
  } catch { /* no objects directory */ }

  // V6
  const last = recs.length ? recs[recs.length - 1] : undefined;
  head = isObj(last) && typeof last.hash === 'string' ? last.hash : '';
  if (expectHead !== undefined && expectHead !== head) add('E_HEAD');

  return finish();
}

// ------------------------------------------------------------------- main
function main(argv) {
  let runDir;
  let expectHead;
  let allowOpen = false;
  let bad = false;
  let schemaDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', 'schemas');
  for (let k = 0; k < argv.length; k++) {
    const a = argv[k];
    if (a === '--expect-head') { expectHead = argv[++k]; if (expectHead === undefined) bad = true; }
    else if (a.startsWith('--expect-head=')) expectHead = a.slice('--expect-head='.length);
    else if (a === '--allow-open') allowOpen = true;
    else if (a === '--schemas') { schemaDir = argv[++k]; if (schemaDir === undefined) bad = true; }
    else if (a.startsWith('--schemas=')) schemaDir = a.slice('--schemas='.length);
    else if (runDir === undefined) runDir = a;
  }
  if (runDir === undefined || bad) {
    process.stderr.write('usage: node verify.mjs <run_dir> [--expect-head <hex>] [--allow-open] [--schemas DIR]\n');
    return 2;
  }
  let schemas;
  try { schemas = loadSchemas(schemaDir); } catch (e) {
    process.stderr.write('cannot load schemas from ' + schemaDir + ': ' + e.message + '\n');
    return 2;
  }
  let out;
  try { out = verify(runDir, expectHead, allowOpen, schemas); } catch (e) {
    // e.g. a schema whose pattern is not a valid regular expression: refuse rather than guess
    process.stderr.write('verification could not run: ' + e.message + '\n');
    return 2;
  }
  process.stdout.write(JSON.stringify(out) + '\n');
  return out.clean ? 0 : out.ok ? 1 : 2;
}

process.exitCode = main(process.argv.slice(2));
