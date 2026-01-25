# Open Threads

> **Status Dashboard**
> Active: {{ACTIVE_COUNT}} | Dormant: {{DORMANT_COUNT}} | Resolved: {{RESOLVED_COUNT}}
> **Last Updated**: {{LAST_UPDATED}}

---

## What is a Thread?

A **thread** is any narrative element that:
- Has been introduced but not resolved
- Creates expectation in the reader
- Must be addressed before story ends (or deliberately left open)

---

## Active Threads

### Critical (Must Resolve)

#### T-001: {{THREAD_1_NAME}}
| Field | Value |
|-------|-------|
| **Introduced** | [[Scenes/{{INTRO_1}}]] |
| **Description** | {{THREAD_1_DESC}} |
| **Stakes** | {{STAKES_1}} |
| **Target Resolution** | [[Scenes/{{TARGET_1}}]] |
| **Dependencies** | {{DEPS_1}} |

**Resolution Options:**
1. {{OPTION_1A}}
2. {{OPTION_1B}}
3. {{OPTION_1C}}

---

#### T-002: {{THREAD_2_NAME}}
| Field | Value |
|-------|-------|
| **Introduced** | [[Scenes/{{INTRO_2}}]] |
| **Description** | {{THREAD_2_DESC}} |
| **Stakes** | {{STAKES_2}} |
| **Target Resolution** | [[Scenes/{{TARGET_2}}]] |
| **Dependencies** | {{DEPS_2}} |

---

### Important (Should Resolve)

#### T-003: {{THREAD_3_NAME}}
| Field | Value |
|-------|-------|
| **Introduced** | [[Scenes/{{INTRO_3}}]] |
| **Description** | {{THREAD_3_DESC}} |
| **Stakes** | {{STAKES_3}} |
| **Target Resolution** | Flexible |

---

### Minor (Can Resolve or Leave Open)

| Thread ID | Name | Introduced | Status |
|-----------|------|------------|--------|
| T-004 | {{MINOR_1}} | [[Scenes/{{M_INTRO_1}}]] | Active |
| T-005 | {{MINOR_2}} | [[Scenes/{{M_INTRO_2}}]] | Active |

---

## Dormant Threads

> Introduced but not currently active - may resurface

| Thread ID | Name | Last Touched | Wake Condition |
|-----------|------|--------------|----------------|
| T-010 | {{DORMANT_1}} | [[Scenes/{{D_LAST_1}}]] | {{WAKE_1}} |
| T-011 | {{DORMANT_2}} | [[Scenes/{{D_LAST_2}}]] | {{WAKE_2}} |

---

## Resolved Threads

| Thread ID | Name | Resolution Scene | Outcome |
|-----------|------|------------------|---------|
| T-100 | {{RESOLVED_1}} | [[Scenes/{{R_SCENE_1}}]] | {{OUTCOME_1}} |
| T-101 | {{RESOLVED_2}} | [[Scenes/{{R_SCENE_2}}]] | {{OUTCOME_2}} |

---

## Thread Relationships

### Dependencies
```
T-001 ──────> T-003 (T-003 cannot resolve until T-001 does)
    │
    └──────> T-002 (T-002 outcome affects T-001)
```

### Conflicts
> Threads that cannot both resolve favorably

| Thread A | Thread B | Conflict |
|----------|----------|----------|
| T-001 | T-004 | {{CONFLICT_DESC}} |

---

## Chekhov's Guns

> Elements introduced that MUST pay off

| Element | Introduced | Expected Payoff | Scene |
|---------|------------|-----------------|-------|
| [[Artifacts/{{GUN_1}}]] | [[Scenes/{{G_INTRO_1}}]] | {{PAYOFF_1}} | [[Scenes/{{G_PAY_1}}]] |
| {{GUN_2}} | [[Scenes/{{G_INTRO_2}}]] | {{PAYOFF_2}} | TBD |

---

## Promises to Reader

> Implicit contracts with the reader

| Promise | Made When | Must Deliver |
|---------|-----------|--------------|
| {{PROMISE_1}} | [[Scenes/{{P_SCENE_1}}]] | {{DELIVER_1}} |
| {{PROMISE_2}} | [[Scenes/{{P_SCENE_2}}]] | {{DELIVER_2}} |

---

## Thread Health Check

### Threads at Risk
> Threads that might be forgotten or unresolvable

| Thread | Risk | Mitigation |
|--------|------|------------|
| T-{{RISK_1}} | {{RISK_DESC_1}} | {{MIT_1}} |

### Threads Needing Attention
> Haven't been touched in a while

| Thread | Last Touched | Chapters Since |
|--------|--------------|----------------|
| T-{{STALE_1}} | [[Scenes/{{S_LAST_1}}]] | {{CHAPTERS_1}} |

---

## Next Actions

### Before Next Chapter
- [ ] Touch thread T-{{TOUCH_1}}
- [ ] Advance thread T-{{ADVANCE_1}}
- [ ] Plant seed for T-{{PLANT_1}}

### Before Midpoint
- [ ] Resolve T-{{MID_1}}
- [ ] Complicate T-{{MID_2}}

### Before Climax
- [ ] All critical threads must be convergent
- [ ] Dormant threads: wake or confirm dormancy intentional

---

*Threads are the promises we make. Broken promises break trust.*
