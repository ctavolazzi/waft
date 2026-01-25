# Journal Entry: {{CHARACTER_NAME}}

> **Type**: {{TYPE}} (Internal / External)
> **Date**: {{ENTRY_DATE}}
> **Timeline**: [[Timelines/{{TIMELINE}}]]
> **Following**: [[Scenes/{{SCENE_REFERENCE}}]]

---

## Context

**Location**: [[Locations/{{LOCATION}}]]
**Emotional State**: {{EMOTIONAL_STATE}}
**Physical State**: {{PHYSICAL_STATE}}

---

{{#if TYPE == "Internal"}}

## Internal Entry

> *What {{CHARACTER_NAME}} truly thinks, feels, and knows*

### Stream of Consciousness

{{STREAM_OF_CONSCIOUSNESS}}

### True Feelings About Recent Events

{{TRUE_FEELINGS}}

### Hidden Motivations Active

- {{MOTIVATION_1}}
- {{MOTIVATION_2}}

### Secrets Being Kept

| Secret | From Whom | Why |
|--------|-----------|-----|
| {{SECRET_1}} | [[Characters/{{FROM_1}}]] | {{WHY_1}} |
| {{SECRET_2}} | [[Characters/{{FROM_2}}]] | {{WHY_2}} |

### Internal Conflicts

{{INTERNAL_CONFLICTS}}

### What They Really Think About:

**[[Characters/{{CHAR_1}}]]**:
> {{THOUGHTS_ON_CHAR_1}}

**[[Characters/{{CHAR_2}}]]**:
> {{THOUGHTS_ON_CHAR_2}}

### Plans & Intentions

- Immediate: {{IMMEDIATE_PLANS}}
- Long-term: {{LONG_TERM_PLANS}}
- Contingencies: {{CONTINGENCIES}}

### Fears Surfacing

{{FEARS}}

### Hopes

{{HOPES}}

{{/if}}

---

{{#if TYPE == "External"}}

## External Record

> *Observable behavior - what others could witness*

### Actions Taken

| Time | Action | Witnesses |
|------|--------|-----------|
| {{TIME_1}} | {{ACTION_1}} | {{WITNESS_1}} |
| {{TIME_2}} | {{ACTION_2}} | {{WITNESS_2}} |

### Dialogue Spoken

```
{{CHARACTER_NAME}}: "{{DIALOGUE_1}}"

{{CHARACTER_NAME}}: "{{DIALOGUE_2}}"
```

### Non-Verbal Behavior

- Body Language: {{BODY_LANGUAGE}}
- Facial Expressions: {{FACIAL}}
- Tone of Voice: {{TONE}}
- Micro-expressions: {{MICRO}}

### What Others Could Infer

> Based on observable behavior, what might others conclude?

- [[Characters/{{OBSERVER_1}}]] might think: {{INFERENCE_1}}
- [[Characters/{{OBSERVER_2}}]] might think: {{INFERENCE_2}}

### Discrepancies

> Where external behavior differs from internal state:

| External Presentation | Internal Reality |
|----------------------|------------------|
| {{EXTERNAL_1}} | {{INTERNAL_1}} |
| {{EXTERNAL_2}} | {{INTERNAL_2}} |

{{/if}}

---

## State Tracking

### Knowledge State After This Entry

**Knows**:
- {{KNOWS_1}}

**Believes**:
- {{BELIEVES_1}}

**Suspects**:
- {{SUSPECTS_1}}

**Doesn't Know**:
- {{DOESNT_KNOW_1}}

### Relationship State Changes

| Character | Previous State | Current State | Cause |
|-----------|---------------|---------------|-------|
| [[Characters/{{REL_1}}]] | {{PREV_STATE_1}} | {{CURR_STATE_1}} | {{CAUSE_1}} |

---

## Continuity Notes

### References Events
- [[Events/{{EVENT_1}}]]

### Sets Up
- [[Scenes/{{FUTURE_SCENE}}]]

---

## Orchestrator Notes

{{ORCHESTRATOR_NOTES}}

---

*Tags: #journal #{{TYPE_TAG}} #{{CHARACTER_TAG}}*
