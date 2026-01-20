# Oracle Empirica Workflow Integration

The Oracle now follows the **Empirica 5-Step Workflow** to eliminate confabulation and maximize learning.

## The Empirica Workflow

```
1. PREFLIGHT → 2. INVESTIGATE → 3. CHECK → 4. ACT → 5. POSTFLIGHT
```

## Step-by-Step Process

### Step 1: PREFLIGHT 📊
**Purpose:** Assess current epistemic state

**What TheOracle Does:**
- Retrieves current epistemic state from Empirica
- Calculates KNOW and UNCERTAINTY levels
- Determines if investigation is required
- Submits preflight assessment to Empirica

**Output:**
```
KNOW: 0.45 (Low)
UNCERTAINTY: 0.70 (High)
→ INVESTIGATE REQUIRED
```

**Implementation:**
```python
preflight_result = self._empirica_preflight(question)
# Returns: {"know": 0.45, "uncertainty": 0.70, "investigate_required": True, ...}
```

---

### Step 2: INVESTIGATE 🔍
**Purpose:** Reduce uncertainty by logging findings and reviewing past experiences

**What TheOracle Does:**
- **Reflects** on past similar consultations (searches memory)
- Reviews relevant insights from journal
- Analyzes learned patterns for current phase
- Tracks epistemic trajectory (improving/declining/clarifying)
- Logs findings and unknowns to Empirica (via `log_insight()`, `log_unknown()`)

**Output:**
```
💭 Reflection: Found 3 relevant past experiences. 2 relevant insights available. 
   5 learned patterns for Synthesis phase. Epistemic trajectory: improving.
```

**Implementation:**
```python
reflection = self._reflect_on_question(question)
# This searches memory, reviews patterns, analyzes trajectory
```

**Empirica Commands Used:**
- `empirica finding-log "Uses PKCE"` - Logs discoveries
- `empirica unknown-log "Refresh flow?"` - Logs knowledge gaps

---

### Step 3: CHECK ✅
**Purpose:** Decision gate based on findings and remaining unknowns

**What TheOracle Does:**
- Calculates confidence based on findings vs unknowns
- Considers uncertainty level
- Submits CHECK gate to Empirica
- Gets decision: PROCEED | HALT | BRANCH | REVISE

**Output:**
```
CONFIDENCE: 0.85
→ DECISION: PROCEED
```

**Implementation:**
```python
check_result = self._empirica_check(question, findings, unknowns, uncertainty)
# Returns: {"confidence": 0.85, "decision": "PROCEED", ...}
```

**Empirica Command Used:**
- `empirica check-submit` - Decision gate assessment

**Decision Logic:**
- **PROCEED**: Confidence ≥ 0.7 AND uncertainty < 0.3
- **HALT**: Confidence < 0.3 OR uncertainty > 0.7
- **BRANCH**: More unknowns than findings (needs investigation)
- **REVISE**: Otherwise (needs refinement)

---

### Step 4: ACT 🎯
**Purpose:** Execute with precision - generate recommendation

**What TheOracle Does:**
- Generates recommendation based on:
  - Epistemic phase
  - Knowledge coverage
  - Findings and unknowns
  - Reflection insights
  - Check decision
  - Learned patterns from memory
- Applies personality styling
- Incorporates check decision into recommendation text

**Output:**
```
[PROCEED] Focus on collecting data and observations. 
High uncertainty suggests need for more information.
Confidence: 85%. Safe to proceed.
```

**Implementation:**
```python
recommendation = self._generate_recommendation(
    phase, coverage, unknowns, uncertainty,
    reflection=reflection,
    check_result=check_result
)
```

**Recommendation Prefixes:**
- `[PROCEED]` - Safe to proceed
- `[HALT]` - Requires human approval
- `[BRANCH]` - Investigation needed first
- `[REVISE]` - Approach needs refinement

---

### Step 5: POSTFLIGHT 📈
**Purpose:** Measure learning deltas and verify calibration

**What TheOracle Does:**
- Calculates learning deltas (knowledge change, uncertainty change)
- Submits postflight assessment to Empirica
- Logs consultation to journal (for memory tracking)
- Tracks that guidance was provided

**Output:**
```
DELTA: +0.40 Knowledge
UNCERTAINTY: -0.55
```

**Implementation:**
```python
postflight_result = self._empirica_postflight(preflight_result, check_result, response)
# Returns: {"knowledge_delta": 0.0, "uncertainty_delta": 0.0, "guidance_provided": True, ...}
```

**Empirica Command Used:**
- `empirica postflight-submit` - Measure learning

---

## Complete Workflow Example

When you run `waft oracle "What should we focus on next?"`:

```
📊 Preflight: KNOW=45% (Low), UNCERTAINTY=70% (High)
   → INVESTIGATE REQUIRED

💭 Reflection: Found 3 relevant past experiences. 2 relevant insights available. 
   5 learned patterns for Synthesis phase. Epistemic trajectory: improving.
   (3 relevant past experiences considered)

✅ Check: CONFIDENCE=85%, DECISION=PROCEED

[PROCEED] Reflecting on past experiences: Feature implemented successfully, Tests caught bugs early. 
Focus on collecting data and observations. High uncertainty suggests need for more information.
Confidence: 85%. Safe to proceed.

📈 Postflight: Guidance provided, learning tracked
```

---

## Integration with Oracle Systems

### Journal & Memory
- **Consultations logged** after postflight
- **Reflection insights** stored in memory
- **Patterns learned** from each workflow execution

### Personality
- **Personality styling** applied to recommendations
- **Trait expressions** used in check decisions
- **Communication style** reflected in output

### Empirica
- **Preflight/postflight** submitted to Empirica
- **Findings/unknowns** logged via Empirica
- **Check gates** use Empirica's decision system
- **Session continuity** maintained across consultations

---

## Benefits

1. **Eliminates Confabulation** - Every recommendation is based on verified epistemic state
2. **Maximizes Learning** - Explicit tracking of knowledge changes
3. **Decision Transparency** - Clear PROCEED/HALT/BRANCH/REVISE decisions
4. **Memory Integration** - Past experiences inform current guidance
5. **Calibration** - Postflight measures actual learning vs expected

---

## Technical Details

### Preflight Vectors
```python
{
    "engagement": 0.8,
    "foundation": {
        "know": 0.45,
        "do": 0.7,
        "context": 0.5
    },
    "uncertainty": 0.70
}
```

### Check Decision Logic
```python
confidence = (findings_count * 0.1) * (1.0 - uncertainty)

if confidence >= 0.7 and uncertainty < 0.3:
    decision = "PROCEED"
elif confidence < 0.3 or uncertainty > 0.7:
    decision = "HALT"
elif unknowns_count > findings_count:
    decision = "BRANCH"
else:
    decision = "REVISE"
```

### Postflight Deltas
```python
knowledge_delta = postflight_know - preflight_know
uncertainty_delta = postflight_uncertainty - preflight_uncertainty
```

---

## See Also

- [Oracle Journal & Memory System](ORACLE_JOURNAL_MEMORY.md)
- [Oracle Personality System](ORACLE_PERSONALITY.md)
- [Empirica Integration](../_work_efforts/EMPIRICA_INTEGRATION.md)
