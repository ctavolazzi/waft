# Sanity Check Results: TOML Parsing Assumption Test

**Date**: 2026-01-04
**Purpose**: Objective test of TOML parsing assumption to verify understanding
**Status**: ✅ COMPLETE

---

## Objective

Test our assumption that the regex-based TOML parsing in `SubstrateManager.get_project_info()` correctly handles all TOML field formats.

**Why**: We assumed the parsing worked correctly, but objective testing reveals actual limitations.

---

## Test Cases

### Test Code
```python
from src.waft.core.substrate import SubstrateManager
from pathlib import Path
import tempfile

test_cases = [
    ("Simple", 'name = "simple"', "simple"),
    ("Single quotes", "name = 'single'", "single"),
    ("With spaces", 'name = "with spaces"', "with spaces"),
    ("Escaped quotes", 'name = "with\\"escaped\\"quotes"', 'with"escaped"quotes'),
    ("Multiline (triple quotes)", 'name = """multi\nline"""', None),
    ("No quotes", "name = no_quotes", "no_quotes"),
    ("Comments", '# comment\nname = "test"', "test"),
    ("Whitespace", '  name  =  "test"  ', "test"),
]
```

---

## Results

### ✅ Passed (6/8)

1. **Simple** - `name = "simple"` → `"simple"` ✅
2. **Single quotes** - `name = 'single'` → `"single"` ✅
3. **With spaces** - `name = "with spaces"` → `"with spaces"` ✅
4. **Multiline (triple quotes)** - `name = """multi\nline"""` → Handled ✅
5. **Comments** - `# comment\nname = "test"` → `"test"` ✅
6. **Whitespace** - `  name  =  "test"  ` → `"test"` ✅

### ❌ Failed (2/8)

1. **Escaped quotes** - `name = "with\"escaped\"quotes"`
   - **Expected**: `'with"escaped"quotes'`
   - **Actual**: Regex doesn't handle `\"` correctly
   - **Issue**: Regex pattern doesn't account for escaped quotes within quoted strings

2. **No quotes** - `name = no_quotes`
   - **Expected**: `"no_quotes"`
   - **Actual**: Regex requires quotes, but TOML allows unquoted strings
   - **Issue**: TOML spec allows unquoted strings (bare keys/values), but our regex assumes quotes

---

## Key Findings

### 1. Assumption Was Incomplete

We assumed the regex-based parsing handled all TOML formats, but testing revealed:
- **2 failure cases** we weren't aware of
- **Edge cases** that need handling
- **Limitations** in the current approach

### 2. TOML Specification Compliance

The TOML specification allows:
- **Unquoted strings** (bare keys/values): `name = value`
- **Escaped quotes**: `name = "with\"quotes"`
- **Triple-quoted strings**: `name = """multi\nline"""`

Our current regex handles most cases but not all.

---

## Recommendations

### Option 1: Use Proper TOML Parser (Recommended)

**Python 3.11+**:
```python
import tomllib

with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)
    name = data["project"]["name"]
```

**Python < 3.11**:
```python
import tomli

with open("pyproject.toml", "rb") as f:
    data = tomli.load(f)
    name = data["project"]["name"]
```

**Benefits**:
- ✅ Full TOML spec compliance
- ✅ Handles all edge cases
- ✅ Standard library (3.11+) or well-maintained library
- ✅ No regex maintenance burden

### Option 2: Improve Regex

Update regex to handle:
- Escaped quotes: `\"` within quoted strings
- Unquoted strings: Bare keys/values without quotes

**Drawbacks**:
- ⚠️ More complex regex
- ⚠️ Still may miss edge cases
- ⚠️ Maintenance burden

### Option 3: Document Limitation

Keep current approach but document:
- What formats are supported
- What formats are not supported
- When to use proper TOML parser

**Use Case**: If regex is "good enough" for current needs, document limitations.

---

## Impact Assessment

### Current Impact: **Low**

- Most `pyproject.toml` files use simple quoted strings
- Edge cases (escaped quotes, no quotes) are rare in practice
- Current implementation works for 75% of cases (6/8)

### Future Impact: **Medium**

- If projects start using unquoted strings, parsing will fail
- If projects use escaped quotes, parsing will fail
- May cause confusion when parsing fails silently

---

## Action Items

1. ✅ **Documented limitations** - This document
2. ⏳ **Decide on approach** - Parser vs improved regex vs documentation
3. ⏳ **Implement solution** - If needed
4. ⏳ **Add tests** - Prevent regressions

---

## Related Documents

- `PROJECT_STARTUP_PROCESS.md` - Mentions this sanity check
- `SESSION_RECAP_2026-01-04.md` - Session recap with test details
- `SESSION_RECAP_2026-01-05.md` - Abbreviated recap
- `CHECKPOINT_2026-01-04_EMPIRICA.md` - Checkpoint document
- `EMPIRICA_INTEGRATION.md` - Integration guide

---

## Conclusion

**Status**: ✅ **Test Complete**

The sanity check successfully identified limitations in our TOML parsing assumption. We now have objective evidence of what works and what doesn't, enabling informed decisions about improvements.

**Key Learning**: Objective testing reveals real limitations that assumptions hide.

---

**Test Completed**: 2026-01-04
**Document Created**: 2026-01-05
**Status**: ✅ COMPLETE

