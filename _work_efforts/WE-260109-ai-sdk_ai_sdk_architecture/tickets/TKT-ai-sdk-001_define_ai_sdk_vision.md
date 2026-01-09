---
id: TKT-ai-sdk-001
parent: WE-260109-ai-sdk
title: "Define 'Self-Modifying AI SDK' vision document"
status: open
priority: CRITICAL
created: 2026-01-09T00:00:00.000Z
created_by: claude_audit
assigned_to: null
---

# TKT-ai-sdk-001: Define "Self-Modifying AI SDK" vision document

## Metadata
- **Created**: Thursday, January 9, 2026
- **Parent Work Effort**: WE-260109-ai-sdk
- **Author**: Claude Audit System
- **Priority**: CRITICAL
- **Estimated Effort**: 2 tickets (requires deep thinking)

## Description

Create comprehensive vision document that defines what "Waft as a self-modifying AI SDK" means. This document will guide ALL future development and reframe the entire codebase purpose.

## The Problem

**Current State**: Audit saw "meta-framework with scope creep"
**Actual Intent**: "Self-modifying AI SDK"
**Gap**: No documentation explains this vision

**Result**: Contributors (and AI auditors!) misunderstand the architecture. Features that support AI SDK look like unnecessary complexity.

## Acceptance Criteria

- [ ] `docs/AI_SDK_VISION.md` created
- [ ] Defines "self-modifying" clearly
- [ ] Defines "AI SDK" scope
- [ ] Explains target users
- [ ] Shows architecture layers
- [ ] Maps existing components to AI SDK roles
- [ ] Identifies missing components
- [ ] Provides roadmap to v1
- [ ] Includes concrete examples
- [ ] Team review and approval

## Vision Document Template

### Structure

```markdown
# Waft AI SDK Vision

## TL;DR (3 sentences)
[What? Who? Why?]

## The Problem We Solve
[What pain points do AI developers/researchers have?]

## What is "Self-Modifying"?
[Specific definition with examples]

## What is "AI SDK"?
[What capabilities does it provide?]

## Target Users
1. **AI Researchers** - [Use case]
2. **AI Developers** - [Use case]
3. **AI Agents** - [Use case - self-hosting]

## Architecture Overview
[4 layers: Foundation, Intelligence, Agent, Personality]

## Current Component Mapping
[How each existing component serves AI SDK]

## Missing Components
[What needs to be built]

## Safety & Constraints
[How self-modification is kept safe]

## Roadmap
- v0.1: Foundation (current)
- v0.5: Agent interface
- v1.0: Full self-modification
- v2.0: Multi-agent orchestration

## Examples
[Concrete code examples of agent using SDK]

## Comparison
[How Waft differs from LangChain, AutoGPT, etc.]
```

## Key Questions to Answer

### 1. What Does "Self-Modifying" Mean?

**Options to consider**:

**A. Code Self-Modification**:
```python
# Agent modifies its own source code
agent.modify_code(
    file="src/waft/core/decision_matrix.py",
    change="Add new decision methodology",
    reason="Learned WSM insufficient for multi-objective problems"
)
```

**B. Behavior Self-Modification**:
```python
# Agent modifies its decision parameters
agent.modify_behavior(
    parameter="decision_weights",
    new_value={"accuracy": 0.7, "speed": 0.3},
    reason="Learned to prioritize accuracy over speed"
)
```

**C. Prompt Self-Modification**:
```python
# Agent evolves its own prompts
agent.modify_prompt(
    prompt_id="code_review",
    new_template="Focus on security vulnerabilities...",
    reason="Security issues found in 80% of reviews"
)
```

**D. Architecture Self-Modification**:
```python
# Agent modifies its own architecture
agent.add_component(
    name="CachingLayer",
    reason="Repeated queries wasting time"
)
```

**Question**: Which types of self-modification does Waft support? All? Some?

### 2. What Are The Safety Constraints?

**Critical for self-modification**:

```python
class SafetyConstraints:
    """Safety rules for self-modification."""

    # What can be modified?
    ALLOWED_FILES = ["src/waft/core/", "src/waft/agents/"]
    FORBIDDEN_FILES = ["src/waft/safety/", "src/waft/core/substrate.py"]

    # What operations allowed?
    ALLOWED_OPERATIONS = ["add_function", "modify_parameters", "add_logging"]
    FORBIDDEN_OPERATIONS = ["delete_safety_check", "modify_validation"]

    # Rollback requirement
    REQUIRE_ROLLBACK = True
    MAX_MODIFICATIONS_PER_SESSION = 10

    # Human approval required?
    REQUIRE_APPROVAL_FOR = ["architecture_changes", "safety_modifications"]
```

**Questions**:
- What can agents modify freely?
- What requires human approval?
- How do we prevent malicious self-modification?
- What's the rollback mechanism?

### 3. How Do Current Components Serve AI SDK?

**Must document mapping**:

| Component | Original Purpose | AI SDK Role |
|-----------|-----------------|-------------|
| **_pyrite** | Project organization | Agent persistent memory |
| **Session analytics** | Productivity tracking | Agent training data pipeline |
| **Empirica** | Epistemic tracking | Agent knowledge state |
| **Decision matrix** | Decision support | Agent reasoning framework |
| **Gamification** | Dev motivation | Agent reward signals (quantitative) |
| **TavernKeeper** | RPG mechanics | Agent personality engine (qualitative) |
| **5 context commands** | User commands | Agent context management primitives |
| **3 task systems** | Task management | Agent planning hierarchy |
| **Subprocess validation** | Security | Safe agent tool execution |

### 4. What Are The Missing Pieces?

**Core AI SDK Components Needed**:

1. **Agent Interface** (`src/waft/agents/agent.py`)
   - Base Agent class
   - Observe, Decide, Act, Reflect cycle
   - Memory integration
   - Learning integration

2. **Self-Modification Engine** (`src/waft/agents/self_modify.py`)
   - Propose modifications
   - Validate safety
   - Apply changes
   - Rollback mechanism

3. **Learning System** (`src/waft/agents/learning.py`)
   - Experience collection
   - Pattern analysis
   - Behavior updates

4. **Safety Layer** (`src/waft/agents/safety.py`)
   - Constraint enforcement
   - Approval workflows
   - Audit logging

5. **Examples** (`examples/agents/`)
   - Self-improving code reviewer
   - Adaptive test generator
   - Learning documentation agent

## Implementation Plan

### Step 1: Research & Reference

Review existing AI agent frameworks:
- **LangChain**: Agent framework, no self-modification
- **AutoGPT**: Autonomous agents, limited self-modification
- **MetaGPT**: Multi-agent, no self-modification
- **Voyager (MineCraft)**: Self-improving agent (closest)

**Question**: What does Waft provide that these don't?

### Step 2: Define Vision

Write comprehensive vision document answering all key questions.

### Step 3: Create Examples

Write concrete examples showing:
```python
# Example 1: Self-improving code reviewer
from waft.agents import WaftAgent

class CodeReviewerAgent(WaftAgent):
    """AI agent that reviews code and improves its own review criteria."""

    def review_code(self, code: str) -> Review:
        """Review code using decision matrix."""
        review = self.decide(
            problem="Code quality",
            alternatives=["approve", "request_changes", "reject"],
            criteria=self.review_criteria
        )
        return review

    def learn_from_feedback(self, feedback: str):
        """Modify review criteria based on human feedback."""
        if "missed security issue" in feedback:
            self.modify_behavior(
                parameter="review_criteria.security",
                new_weight=0.5,  # Increase security weight
                reason="Human feedback indicated security gaps"
            )

# Usage
agent = CodeReviewerAgent()
review = agent.review_code(code)
agent.learn_from_feedback("You missed a SQL injection vulnerability")
# Agent automatically adjusts to prioritize security
```

### Step 4: Architecture Diagram

Create visual architecture showing:
```
┌─────────────────────────────────────────────────────────┐
│                     WAFT AI SDK                         │
├─────────────────────────────────────────────────────────┤
│  Layer 4: PERSONALITY                                   │
│  [TavernKeeper] [Chronicles] [Quests]                   │
├─────────────────────────────────────────────────────────┤
│  Layer 3: AGENT (Missing - To Be Built)                 │
│  [Agent Interface] [Self-Modification] [Learning]       │
├─────────────────────────────────────────────────────────┤
│  Layer 2: INTELLIGENCE                                  │
│  [Analytics] [Empirica] [Decision] [Gamification]       │
├─────────────────────────────────────────────────────────┤
│  Layer 1: FOUNDATION                                    │
│  [Substrate] [Memory] [Subprocess] [Templates]          │
└─────────────────────────────────────────────────────────┘
```

### Step 5: Roadmap

Define concrete milestones:

**v0.1** (Current):
- ✅ Foundation layer complete
- ✅ Intelligence layer 60% complete
- ✅ Personality layer complete
- ❌ Agent layer 0%

**v0.5** (Next - 3 months):
- [ ] Agent interface designed and implemented
- [ ] Basic self-modification (behavior parameters)
- [ ] Simple learning from session analytics
- [ ] 2-3 example agents

**v1.0** (AI SDK GA - 6 months):
- [ ] Full self-modification capabilities
- [ ] Advanced learning system
- [ ] Safety constraints enforced
- [ ] Multi-agent support
- [ ] Documentation complete

**v2.0** (Advanced - 12 months):
- [ ] Multi-agent orchestration
- [ ] Distributed agents
- [ ] Advanced self-modification (code generation)
- [ ] Agent marketplace

## Files to Create

**New Files**:
- `docs/AI_SDK_VISION.md` (comprehensive vision)
- `docs/AI_SDK_ARCHITECTURE.md` (technical architecture)
- `docs/AI_SDK_EXAMPLES.md` (code examples)
- `docs/AI_SDK_SAFETY.md` (safety constraints)
- `docs/AI_SDK_COMPARISON.md` (vs other frameworks)
- `examples/agents/self_improving_reviewer.py` (example agent)

**Modified Files**:
- `README.md` (update to reflect AI SDK vision)
- `pyproject.toml` (update description)
- `_work_efforts/WE-260109-scope_scope_definition/` (reframe scope)

## Success Metrics

**Clarity**:
- [ ] Anyone reading vision doc understands what Waft is
- [ ] Current component purposes are clear
- [ ] Roadmap to AI SDK v1 is concrete
- [ ] Examples show self-modification in action

**Team Alignment**:
- [ ] All team members understand AI SDK vision
- [ ] All agree on scope (what's in/out)
- [ ] All agree on safety constraints

**External Validation**:
- [ ] 3-5 AI researchers understand the vision
- [ ] Can differentiate from LangChain/AutoGPT
- [ ] See value in self-modification capabilities

## Related Issues

- **WE-260109-scope**: Now needs complete reframe (not "reduce", but "organize for AI SDK")
- **WE-260109-arch**: Architecture should align with AI SDK layers
- **WE-260109-sec1**: Security even MORE critical for AI agents
- **Audit misunderstanding**: Entire audit needs reinterpretation through AI lens

## Commits

- (populated as work progresses)

## Notes

This is the MOST CRITICAL ticket. Without a clear AI SDK vision document, all development is directionless and features appear as "scope creep" when they're actually foundational AI components.

This single document will:
1. Reframe the entire codebase purpose
2. Justify all "confusing" features
3. Guide future development
4. Help with fundraising/partnerships
5. Attract contributors who understand AI SDK goals

**Do not proceed with any major development until this is complete.**
