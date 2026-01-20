# /examine-plan - Adversarial Plan Examination

**Purpose:** Hard pause checkpoint that adversarially examines a plan step-by-step, working backward from desired outcome, forking and vibrating through alternatives until settling on the final vision and immediate next steps.

**Usage:** `/examine-plan [plan description]`

**Options:**
- `--goal [text]` - Explicitly state the desired outcome
- `--depth [number]` - Examination depth (1-5, default: 3)
- `--forks [number]` - Number of alternative paths to explore (default: 3)

---

## Overview

The `/examine-plan` command provides a "hard pause" checkpoint that forces deep, adversarial thinking about a plan before proceeding. It:

1. **Clarifies Desired Outcome**: Explicitly defines what success looks like
2. **Works Backward**: Breaks down the goal into required steps
3. **Adversarial Examination**: Critically questions each step
4. **Forking**: Explores alternative approaches
5. **Vibrating**: Tests different variations and combinations
6. **Convergence**: Settles on the optimal path forward
7. **Immediate Next Steps**: Identifies the very next action to take

**Perfect for:**
- Before starting complex work
- When a plan seems unclear
- When multiple approaches are possible
- When you need to validate assumptions
- When you want to ensure you're on the right track

---

## How It Works

### Phase 1: Outcome Clarification
1. Explicitly state the desired outcome
2. Define success criteria
3. Identify constraints and requirements
4. Clarify what "done" looks like

### Phase 2: Backward Planning
1. Start from the desired outcome
2. Ask: "What must be true for this to succeed?"
3. Break down into required steps
4. Identify dependencies
5. Map the critical path

### Phase 3: Adversarial Examination
For each step:
1. **Question Assumptions**: Why do we think this will work?
2. **Identify Risks**: What could go wrong?
3. **Check Dependencies**: Do we have what we need?
4. **Validate Approach**: Is this the best way?
5. **Test Logic**: Does this actually lead to the goal?

### Phase 4: Forking (Alternative Paths)
1. Generate 3+ alternative approaches
2. Compare pros/cons of each
3. Identify when each would be better
4. Consider hybrid approaches

### Phase 5: Vibrating (Variations)
1. Test different variations of the plan
2. Adjust parameters and assumptions
3. Explore edge cases
4. Consider different scopes

### Phase 6: Convergence
1. Synthesize insights from examination
2. Select optimal path (or hybrid)
3. Refine the plan based on findings
4. Identify what changed from original plan

### Phase 7: Immediate Next Steps
1. Identify the very next action
2. Define what needs to happen first
3. List prerequisites
4. Set clear success criteria for first step

---

## Output Format

### Desired Outcome
```
🎯 Desired Outcome
- [Clear statement of what success looks like]
- Success Criteria: [measurable criteria]
- Constraints: [limitations and requirements]
```

### Backward Planning
```
🔙 Working Backward
Step N: [Final step before outcome]
  └─> Requires: [dependencies]
Step N-1: [Previous step]
  └─> Requires: [dependencies]
...
Step 1: [First step]
  └─> Requires: [prerequisites]
```

### Adversarial Examination
```
🔍 Adversarial Examination

Step X: [Step name]
  ❓ Assumptions: [what we're assuming]
  ⚠️  Risks: [what could go wrong]
  🔗 Dependencies: [what we need]
  ✅ Validation: [why this approach]
  🧪 Logic Test: [does this lead to goal?]
  
  Verdict: [PASS/FAIL/NEEDS_REVISION]
```

### Forking (Alternatives)
```
🌳 Forking: Alternative Paths

Path A: [Approach 1]
  ✅ Pros: [advantages]
  ❌ Cons: [disadvantages]
  🎯 Best When: [when to use]

Path B: [Approach 2]
  ✅ Pros: [advantages]
  ❌ Cons: [disadvantages]
  🎯 Best When: [when to use]

Path C: [Approach 3]
  ✅ Pros: [advantages]
  ❌ Cons: [disadvantages]
  🎯 Best When: [when to use]

Selected: [Path X or Hybrid]
Reason: [why this path]
```

### Vibrating (Variations)
```
📳 Vibrating: Testing Variations

Variation 1: [Different scope/approach]
  Impact: [how this changes things]
  Trade-offs: [what we gain/lose]

Variation 2: [Different parameters]
  Impact: [how this changes things]
  Trade-offs: [what we gain/lose]

Optimal Variation: [selected variation]
```

### Convergence
```
🎯 Convergence: Final Plan

Original Plan: [what we started with]
Revised Plan: [what we're doing now]
Changes: [what changed and why]

Final Approach: [selected path]
Confidence: [high/medium/low]
```

### Immediate Next Steps
```
🚀 Immediate Next Steps

Next Action: [very next thing to do]
Prerequisites: [what must be true first]
Success Criteria: [how we know it worked]
Estimated Time: [how long it takes]
```

---

## Usage Examples

### Example 1: Basic Plan Examination
```
/examine-plan Create a Typst template for D&D campaign book
```

### Example 2: With Explicit Goal
```
/examine-plan --goal "Generate a professional D&D campaign book PDF for Teleport Massive" Create Typst template
```

### Example 3: Deep Examination
```
/examine-plan --depth 5 --forks 5 Create campaign book template with all features
```

---

## Integration

### With Sequential Thinking
- Uses `mcp_sequential-thinking_sequentialthinking` for structured reasoning
- Breaks down complex plans into thought steps
- Tracks reasoning process

### With Work Efforts
- Can create work effort from examined plan
- Updates work effort with refined plan
- Links to related work efforts

### With Empirica
- Logs plan examination as finding
- Tracks uncertainty reduction
- Records decision rationale

---

## Philosophy

The `/examine-plan` command embodies:
- **Critical Thinking**: Question assumptions, test logic
- **Exploration**: Consider alternatives, not just one path
- **Rigor**: Deep examination, not surface-level
- **Convergence**: Settle on optimal path, not endless exploration
- **Action**: Always end with clear next steps

It's designed to:
- Prevent going down wrong paths
- Surface hidden assumptions
- Identify better approaches
- Build confidence in the plan
- Ensure clear next steps

---

## When to Use

**Use `/examine-plan` when**:
- ✅ Starting complex work
- ✅ Plan seems unclear or risky
- ✅ Multiple approaches possible
- ✅ Need to validate assumptions
- ✅ Want to ensure optimal path
- ✅ Need clear next steps

**Don't use `/examine-plan` when**:
- ❌ Simple, straightforward tasks
- ❌ Already confident in approach
- ❌ Time is extremely limited
- ❌ Plan is already well-validated

---

## Depth Levels

### Depth 1: Light Examination
- Basic backward planning
- Surface-level adversarial questions
- 1-2 alternative paths
- Quick convergence

### Depth 2: Standard Examination (Default)
- Full backward planning
- Moderate adversarial examination
- 3 alternative paths
- Standard convergence

### Depth 3: Deep Examination
- Comprehensive backward planning
- Thorough adversarial examination
- 5+ alternative paths
- Multiple vibration cycles
- Detailed convergence

### Depth 4: Very Deep
- Exhaustive backward planning
- Extensive adversarial examination
- 7+ alternative paths
- Multiple vibration cycles with variations
- Comprehensive convergence

### Depth 5: Exhaustive
- Complete backward planning
- Maximum adversarial examination
- 10+ alternative paths
- Extensive vibration with all variations
- Full convergence with documentation

---

## Success Criteria

**Examination is successful when**:
- ✅ Desired outcome is crystal clear
- ✅ All steps are validated
- ✅ Risks are identified and mitigated
- ✅ Alternative paths are explored
- ✅ Optimal path is selected
- ✅ Immediate next steps are clear
- ✅ Confidence in plan is high

---

**This command provides a hard pause checkpoint that ensures you're on the right track before proceeding with complex work.**

---

End Command ---
