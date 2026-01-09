---
id: TKT-scope-001
parent: WE-260109-scope
title: "Define 3-sentence value proposition"
status: open
priority: CRITICAL
created: 2026-01-09T00:00:00.000Z
created_by: claude_audit
assigned_to: null
---

# TKT-scope-001: Define 3-sentence value proposition

## Metadata
- **Created**: Thursday, January 9, 2026
- **Parent Work Effort**: WE-260109-scope
- **Author**: Claude Audit System
- **Priority**: CRITICAL
- **Estimated Effort**: 1 ticket (but requires deep thinking and team discussion)

## Description

Write a clear, focused 3-sentence value proposition that answers:
1. What is Waft?
2. Who is it for?
3. Why should they use it?

This will guide ALL future decisions about features, scope, and direction.

## Current State

**No clear value proposition exists.**

README.md says:
> "Waft is an ambient, self-modifying meta-framework for Python projects. It orchestrates your development environment, memory structure, and optional AI agents to work seamlessly in the background."

**Problems with this**:
- ❌ "Ambient, self-modifying meta-framework" is jargon
- ❌ "Orchestrates" is vague
- ❌ Doesn't explain WHO should use it
- ❌ Doesn't explain WHY over alternatives
- ❌ No clear problem being solved

## Acceptance Criteria

- [ ] Value proposition is 3 sentences or less
- [ ] Uses clear, non-jargon language
- [ ] Answers: What? Who? Why?
- [ ] Differentiates from alternatives (cookiecutter, etc.)
- [ ] Team agrees on it
- [ ] Updated in README.md
- [ ] Updated in all documentation
- [ ] Used consistently in marketing/communication

## Examples to Learn From

### Good Value Propositions

**Docker**:
> "Docker makes it easy to build, ship, and run distributed applications. Package software into standardized units called containers. Works everywhere from laptop to cloud."

**Analysis**: Clear, specific, explains what/who/why

**Pytest**:
> "pytest makes it easy to write small, readable tests. Scales to support complex functional testing for applications and libraries. Used by thousands of projects."

**Analysis**: Explains benefit, scalability, social proof

**Poetry**:
> "Python packaging and dependency management made easy. One tool for managing dependencies, packaging, and publishing. Deterministic builds for reliable deployment."

**Analysis**: Solves specific problem, explains how, explains benefit

### Bad Value Propositions (Learn What NOT To Do)

**Bad Example 1**:
> "Synergize your development paradigm with our revolutionary meta-framework that leverages AI-powered orchestration for seamless integration."

**Problems**: All jargon, no substance, no clear benefit

**Bad Example 2**:
> "A tool for developers."

**Problems**: Too vague, no differentiation, no specific benefit

## Thought Process

### What Makes Waft Unique?

Let's analyze what Waft actually provides:

**Not Unique**:
- ❌ Project scaffolding (cookiecutter, copier)
- ❌ Dependency management (uv, poetry, pip-tools)
- ❌ Task running (make, just, invoke)

**Potentially Unique**:
- ✅ _pyrite memory structure (active/backlog/standards)
- ✅ Gamification for development (integrity/insight)
- ✅ RPG mechanics (unique but is it core?)
- ✅ Integration layer (ties uv + memory + gamification)

**Key Question**: Which of these is the CORE value?

### Proposed Value Propositions (To Evaluate)

**Option 1: Memory-Focused**
> "Waft organizes your development knowledge with the _pyrite memory structure. Keep active work, backlog, and standards in one place. Designed for solo developers and small teams who want persistent project context."

**Pros**: Focuses on unique feature (_pyrite)
**Cons**: Is memory structure enough of a value prop?

**Option 2: Gamification-Focused**
> "Waft makes development more engaging through gamification. Track project integrity and insight as you code. Get rewarded for good practices, penalized for technical debt."

**Pros**: Unique angle, addresses motivation
**Cons**: Gamification alone might not justify a framework

**Option 3: Integration-Focused**
> "Waft ties together Python development tools with persistent project memory. Wraps uv for dependencies, structures your knowledge in _pyrite, and tracks project health. For developers who want a cohesive meta-framework instead of scattered tools."

**Pros**: Explains the "meta-framework" concept clearly
**Cons**: Still somewhat vague about specific benefits

**Option 4: Developer Experience-Focused**
> "Waft improves your Python development experience with structure and gamification. Organize project knowledge in _pyrite, manage dependencies with uv, track project health with integrity metrics. A lightweight meta-layer that makes development more engaging."

**Pros**: Benefits-focused, explains all core features
**Cons**: Maybe trying to say too much

**Option 5: Problem-Solution-Focused**
> "Tired of scattered project knowledge and boring development workflows? Waft provides the _pyrite memory structure for persistent context and gamification for engaging feedback. Turn your Python project into an adventure."

**Pros**: Starts with problem, emotional appeal
**Cons**: "Adventure" might be too whimsical for some users

## Team Discussion Template

Use this template for team discussion:

```markdown
# Waft Value Proposition Workshop

## Part 1: What Problem Do We Solve?

What pain points do Python developers have that Waft addresses?

1. ___________________________________
2. ___________________________________
3. ___________________________________

## Part 2: Who Is Our User?

Describe our ideal user:
- Experience level: _______________
- Team size: _______________
- Use case: _______________
- Pain points: _______________

## Part 3: What Makes Us Different?

How is Waft different from:
- cookiecutter: _______________
- poetry: _______________
- just/make: _______________
- plain Python: _______________

## Part 4: Our Value Proposition

**Sentence 1 (What)**: Waft is _____________________

**Sentence 2 (Who/How)**: It ______________________

**Sentence 3 (Why)**: This helps developers __________

## Part 5: Validation

Test your value proposition:

- [ ] Can you explain it to a Python developer in 30 seconds?
- [ ] Does it clearly differentiate from alternatives?
- [ ] Would someone understand what they get?
- [ ] Does it avoid jargon?
- [ ] Is it specific enough to be meaningful?
- [ ] Is it broad enough to allow growth?
```

## Implementation Plan

### Step 1: Team Workshop

- [ ] Schedule 60-90 minute meeting
- [ ] Review audit findings
- [ ] Discuss proposed options
- [ ] Draft value proposition collaboratively
- [ ] Test with outsiders (5-second rule: can they understand it in 5 seconds?)

### Step 2: Refine

- [ ] Get feedback from 3-5 Python developers (not on team)
- [ ] Refine based on feedback
- [ ] Ensure it's clear, specific, compelling

### Step 3: Document

- [ ] Update README.md (top of file)
- [ ] Update pyproject.toml description
- [ ] Update docs/
- [ ] Update any marketing materials

### Step 4: Align Codebase

- [ ] Verify features align with value prop
- [ ] Remove/plugin features that don't align
- [ ] Prioritize features that strengthen value prop

## Testing The Value Proposition

**The 5-Second Test**:
Show your value proposition to someone for 5 seconds, then ask:
- What does Waft do?
- Who is it for?
- Why would you use it?

If they can't answer, revise.

**The Elevator Pitch Test**:
Can you explain Waft compellingly in 30 seconds using just the value proposition?

**The Differentiation Test**:
Can someone explain how Waft differs from cookiecutter or poetry?

## Files to Change

- `README.md` (top section)
- `pyproject.toml` (description field)
- `docs/index.md` or main docs page
- `_work_efforts/HOW_TO_EXPLAIN_WAFT.md` (if exists)

## Success Metrics

**Clarity**:
- [ ] 5/5 test subjects understand what Waft does
- [ ] 5/5 can explain who it's for
- [ ] 5/5 can differentiate from alternatives

**Team Alignment**:
- [ ] All team members can recite value prop
- [ ] All agree on scope implications
- [ ] All commit to focusing on core value

**Documentation**:
- [ ] Consistent across all materials
- [ ] Used in all external communication

## Related Issues

- WE-260109-scope: Parent work effort
- TKT-scope-002: Consolidate gamification (depends on knowing if it's core)
- TKT-scope-004: Core vs Plugin (depends on value prop)
- Audit: "SWOT Analysis" - Weaknesses section

## Example Output

**After completing this ticket**:

README.md:
```markdown
# Waft - [Value Prop Sentence 1]

[Value Prop Sentence 2]. [Value Prop Sentence 3].

## Quick Start
...
```

## Commits

- (populated as work progresses)

## Notes

This ticket seems simple ("just write 3 sentences") but it's the most important strategic work for Waft.

Get this right, and all other decisions become easier. Get this wrong, and the project will continue to lack focus and direction.

Take the time to get it right. Test it. Refine it. This is worth multiple hours of discussion.
