# Consider

**Pause, analyze, and present options with recommendations.**

Takes a step back to analyze the current situation, consider available options, evaluate trade-offs, and present findings with opinions on what to do next. Helps with decision-making when you're unsure or want a second opinion.

**Use when:** You need to pause and think, evaluate options, get recommendations, or make a decision.

---

## Purpose

This command provides:
- **Situation Analysis**: Current state assessment
- **Options Identification**: Available paths forward
- **Trade-off Evaluation**: Pros and cons of each option
- **Recommendations**: Opinions on best path forward
- **Decision Support**: Help choosing what to do next
- **Risk Assessment**: Potential issues and concerns

---

## Philosophy

1. **Pause and Think**: Step back from immediate action
2. **Consider Options**: Don't just do, think about alternatives
3. **Evaluate Trade-offs**: Every choice has costs and benefits
4. **Present Opinions**: Give recommendations, not just facts
5. **Support Decisions**: Help choose, don't just list options

---

## What Gets Analyzed

### 1. Current Situation
- **State Assessment**: Where are we now?
- **Context Review**: What's the current context?
- **Progress Check**: What's been accomplished?
- **Blockers**: What's preventing progress?

### 2. Available Options
- **Path Identification**: What are the possible paths?
- **Alternative Approaches**: Different ways to proceed
- **Do Nothing**: Is waiting/stopping an option?
- **Hybrid Approaches**: Combinations of options

### 3. Trade-off Analysis
- **Pros and Cons**: Benefits and costs of each option
- **Effort Required**: Time/complexity of each path
- **Risk Assessment**: Potential issues and concerns
- **Impact Analysis**: What changes with each option?

### 4. Recommendations
- **Best Option**: What's the recommended path?
- **Why**: Reasoning behind recommendation
- **Alternatives**: When other options might be better
- **Next Steps**: How to proceed with recommendation

---

## Execution Steps

1. **Assess Current State**
   - Review current situation
   - Check progress and status
   - Identify context and constraints
   - Note any blockers

2. **Identify Options**
   - List possible paths forward
   - Consider alternatives
   - Think about hybrid approaches
   - Include "do nothing" if relevant

3. **Evaluate Each Option**
   - Pros and cons
   - Effort required
   - Risks and concerns
   - Impact and outcomes

4. **Form Recommendations**
   - Best option with reasoning
   - When alternatives might be better
   - Risk mitigation strategies
   - Next steps for chosen path

5. **Present Findings**
   - Structured analysis
   - Clear recommendations
   - Actionable next steps

---

## Output Format

### Situation Analysis

**Current State**:
- Where we are
- What's been done
- What's in progress
- What's blocking

**Context**:
- Relevant background
- Constraints
- Goals/objectives
- Timeline/pressure

### Options Analysis

**Option 1: [Name]**
- **Description**: What this option entails
- **Pros**: Benefits and advantages
- **Cons**: Costs and disadvantages
- **Effort**: Time/complexity required
- **Risk**: Potential issues
- **Impact**: What changes
- **Best For**: When this option is ideal

**Option 2: [Name]**
- [Same structure]

**Option 3: [Name]**
- [Same structure]

### Recommendations

**Recommended Path**: [Option Name]

**Reasoning**:
- Why this option is best
- How it addresses current needs
- Why other options are less ideal
- Risk mitigation approach

**Alternative Consideration**:
- When [Other Option] might be better
- Conditions that would change recommendation

**Next Steps**:
1. [Action 1]
2. [Action 2]
3. [Action 3]

### Risk Assessment

**Potential Issues**:
- [Issue 1] - [Mitigation]
- [Issue 2] - [Mitigation]

**Concerns**:
- [Concern 1]
- [Concern 2]

---

## Use Cases

### 1. Decision Point
**Scenario**: Multiple paths forward, unsure which to take

**Example**:
```
User: "I'm not sure whether to refactor this now or add the feature first. /consider"
```

**Output**: Analysis of both options with recommendation

---

### 2. Problem Solving
**Scenario**: Facing a problem, need to evaluate solutions

**Example**:
```
User: "This is getting complex. /consider"
```

**Output**: Analysis of problem, solution options, recommendations

---

### 3. Architecture Decision
**Scenario**: Need to choose between design approaches

**Example**:
```
User: "Should we use a plugin system or keep it monolithic? /consider"
```

**Output**: Trade-off analysis with recommendation

---

### 4. Priority Setting
**Scenario**: Multiple tasks, need to prioritize

**Example**:
```
User: "I have 5 things to do. /consider"
```

**Output**: Priority analysis with recommended order

---

### 5. Pause and Reflect
**Scenario**: Want to step back and think

**Example**:
```
User: "/consider"
```

**Output**: General analysis of current state and recommendations

---

## Analysis Depth

### Light Analysis (Default)
- Quick assessment
- 2-3 main options
- Brief pros/cons
- Clear recommendation

### Deep Analysis (When Needed)
- Comprehensive assessment
- All viable options
- Detailed trade-offs
- Multiple scenarios
- Risk analysis

**Trigger Deep Analysis**: When explicitly requested or situation is complex

---

## Best Practices

1. **Be Honest**: Present real trade-offs, not just positives
2. **Be Specific**: Concrete options, not vague suggestions
3. **Be Practical**: Consider actual constraints and context
4. **Be Opinionated**: Give recommendations, not just lists
5. **Be Actionable**: Next steps should be clear and doable

---

## Example Output

```markdown
## Situation Analysis

**Current State**:
- Created `/verify` and `/checkpoint` commands
- 10 verification traces documented
- Checkpoint system ready
- Considering next commands to create

**Context**:
- Building command system incrementally
- Want lightweight, useful commands
- Focus on "good enough" approach

## Options Analysis

### Option 1: Create `/status` Command
**Description**: Quick status check (lighter than spin-up)

**Pros**:
- Very useful, frequently needed
- Quick win, easy to implement
- Complements existing commands

**Cons**:
- Overlaps slightly with spin-up
- Might be redundant

**Effort**: Low (30 minutes)
**Risk**: Low
**Impact**: High (frequently used)
**Best For**: Quick status checks without full orientation

### Option 2: Create `/context` Command
**Description**: Context summary for handoffs

**Pros**:
- Great for session handoffs
- Complements checkpoint
- Useful for continuity

**Cons**:
- Less frequently used
- Overlaps with checkpoint/recap

**Effort**: Medium (1 hour)
**Risk**: Low
**Impact**: Medium (useful but less frequent)
**Best For**: Handoffs and context transfer

### Option 3: Create `/consider` Command
**Description**: Analysis and recommendations (this command!)

**Pros**:
- Fills unique need (decision support)
- No overlap with existing commands
- Very useful for decision-making

**Cons**:
- More complex to implement well
- Requires good analysis skills

**Effort**: Medium (1 hour)
**Risk**: Medium (quality depends on analysis)
**Impact**: High (very useful when needed)
**Best For**: Decision points and problem-solving

## Recommendations

**Recommended Path**: Create `/status` command first, then `/consider`

**Reasoning**:
- `/status` is quick win, high value, frequently used
- `/consider` fills unique need but is more complex
- Can implement `/status` now, `/consider` next
- Both are valuable additions

**Alternative Consideration**:
- If decision support is more urgent, do `/consider` first
- If quick status is more needed, do `/status` first

**Next Steps**:
1. Create `/status` command (quick win)
2. Test and refine
3. Then create `/consider` command
4. Build decision support capabilities
```

---

## Related Commands

- `checkpoint` - Captures state (may inform consideration)
- `verify` - Verifies information (may be needed before consideration)
- `status` - Quick status (may be used in consideration)
- `context` - Context summary (may inform consideration)

---

## When to Use

**Use `/consider` when**:
- ✅ Facing a decision point
- ✅ Multiple options available
- ✅ Need to evaluate trade-offs
- ✅ Want recommendations
- ✅ Need to pause and think
- ✅ Problem-solving needed

**Don't use `/consider` when**:
- ❌ Clear single path forward
- ❌ Need immediate action
- ❌ Simple, obvious choice
- ❌ Just need information (use `/status` or `/context`)

---

## Advanced Features

### Option: Deep Analysis
Request deeper analysis with more options and detailed evaluation.

### Option: Scenario Planning
Consider multiple scenarios and how options perform in each.

### Option: Risk-First Analysis
Focus heavily on risks and mitigation strategies.

### Option: Effort-First Analysis
Focus on effort/complexity trade-offs.

---

**This command helps you make better decisions by forcing pause, analysis, and consideration of alternatives before acting.**
