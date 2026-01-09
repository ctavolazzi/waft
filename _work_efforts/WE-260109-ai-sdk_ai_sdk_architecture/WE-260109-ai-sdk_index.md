---
id: WE-260109-ai-sdk
title: "AI SDK Architecture & Vision Alignment"
status: open
priority: CRITICAL
created: 2026-01-09T00:00:00.000Z
created_by: claude_audit
last_updated: 2026-01-09T00:00:00.000Z
branch: main
repository: waft
---

# WE-260109-ai-sdk: AI SDK Architecture & Vision Alignment

## Metadata
- **Created**: Thursday, January 9, 2026
- **Author**: Claude Audit System
- **Repository**: waft
- **Branch**: main
- **Priority**: CRITICAL

## Executive Summary

**CRITICAL REVELATION**: Waft is intended to become a **self-modifying AI SDK**, not just a Python meta-framework. This completely reframes the entire codebase audit.

### The Gap

**Current State**: 
- ✅ Foundation built (80%) - substrate, memory, managers
- ✅ Intelligence layer built (60%) - analytics, empirica, decision engine
- ✅ Personality layer built (90%) - TavernKeeper, gamification
- ❌ **Agent layer NOT built (0%)** ← THE CRITICAL GAP

**Vision**: Self-modifying AI SDK where agents can:
- Observe project state
- Make decisions using the decision engine
- Modify code safely
- Learn from experience
- Adapt behavior over time

## Component Reinterpretation

| Component | Audit Initially Saw | AI SDK Reality | Status |
|-----------|---------------------|----------------|--------|
| `_pyrite/` structure | File organization | Agent persistent memory | ✅ Built |
| Session analytics (473 LOC) | Unnecessary complexity | Training data pipeline | ✅ Built (data collection) |
| Empirica integration | Unclear dependency | Epistemic state tracking | ✅ Built |
| Decision matrix (800 LOC) | Over-engineered | AI reasoning framework | ✅ Built |
| TavernKeeper (1,014 LOC) | Scope creep | Agent personality engine | ✅ Built |
| 2 gamification systems | Redundant | Dual reward signals | ✅ Built |
| 5 context commands | Too many | Context primitives | ✅ Built |
| 3 task systems | Overlapping | Planning hierarchy | ✅ Built |
| **Agent Interface** | **Missing** | **Base Agent class** | ❌ **NOT BUILT** |
| **Self-Mod Engine** | **Missing** | **Code modification** | ❌ **NOT BUILT** |
| **Learning System** | **Missing** | **Adapt from experience** | ❌ **NOT BUILT** |

## The Real Problem

**Not**: "Too much scope"  
**But**: "Missing the core AI agent layer"

All the infrastructure is there, but there's no:
1. **Agent base class** - No way for AI agents to use Waft
2. **Self-modification engine** - No safe code modification capabilities
3. **Learning system** - No adaptation from experience (session analytics collects but doesn't learn)
4. **Safety constraints** - No validation for self-modification
5. **Examples** - No concrete agent implementations

## Work Effort Scope

This work effort will:
1. Define the AI SDK vision document (what "self-modifying" means)
2. Design the Agent interface (base class, lifecycle, capabilities)
3. Design the self-modification engine (safe code changes, rollback)
4. Design the learning system (how agents adapt from experience)
5. Map existing components to AI SDK roles
6. Identify implementation gaps
7. Create roadmap to v1.0

## Success Criteria

- [ ] Vision document written and approved
- [ ] Agent interface designed and documented
- [ ] Self-modification engine architecture designed
- [ ] Learning system architecture designed
- [ ] Component mapping complete
- [ ] Gap analysis complete
- [ ] Implementation roadmap created

## Related Work Efforts

- **WE-260109-sec1**: Security fixes (CRITICAL for AI agents executing code)
- **WE-260109-arch**: Architecture refactoring (organize for agent primitives)
- **WE-260109-scope**: Scope definition (reframed by AI SDK vision)

## Notes

This work effort BLOCKS all other strategic work. Without the AI SDK vision document, features continue to look like scope creep when they're actually foundational AI SDK components.

**Key Question**: What does "self-modifying" mean specifically?
- Code generation/modification?
- Parameter tuning?
- Prompt evolution?
- Architecture changes?
- All of the above?

**Answer Required**: Before proceeding with implementation.

## Current vs Intended State

### Current Perception (From Audit)
**Audit saw**: "Python project meta-framework with confusing scope"
- 29 commands (too many!)
- 2 gamification systems (redundant!)
- 3 task management systems (overlapping!)
- Session analytics (why?)
- Decision matrix (scope creep?)
- Empirica integration (unclear purpose?)

**Grade Given**: D+ (scope explosion)

### Reframed Through AI SDK Lens

If Waft is a **self-modifying AI SDK**, suddenly everything makes sense:

| Component | Audit Saw | AI SDK Purpose |
|-----------|-----------|----------------|
| **_pyrite structure** | File organization | **Persistent AI memory** (active/backlog/standards) |
| **Session analytics** | Unnecessary complexity | **Training data collection** for AI improvement |
| **Empirica integration** | Unclear value | **Epistemic tracking** for AI learning |
| **Decision matrix** | Over-engineered | **AI decision-making** framework |
| **Gamification (2 systems)** | Redundant | **Reward/feedback** mechanisms for AI behavior |
| **TavernKeeper RPG** | Scope creep | **Narrative feedback** for AI agent personas |
| **Context commands (5)** | Too many | **AI context management** primitives |
| **Goal/Workflow (3 systems)** | Overlapping | **AI task planning** components |
| **Subprocess validation** | Security issue | **Safe AI tool execution** |

**New Grade**: **Incomplete but directionally correct** → Potential **A** with AI SDK implementation

## Critical Questions

### 1. What Does "Self-Modifying AI SDK" Mean?

**Needs Definition**:
- [ ] Self-modifying in what way? (Code generation? Prompt evolution? Architecture changes?)
- [ ] AI SDK for what? (Building AI agents? Training systems? Autonomous coding?)
- [ ] Who uses it? (AI researchers? App developers? AI agents themselves?)
- [ ] What does "self-modifying" modify? (Its own code? Agent behavior? Decision logic?)

### 2. What's Built vs What's Needed?

**Already Built** (Foundation):
- ✅ Persistent memory (_pyrite)
- ✅ Session tracking (analytics)
- ✅ Epistemic tracking (Empirica)
- ✅ Decision framework (decision_matrix)
- ✅ Feedback systems (gamification × 2)
- ✅ Subprocess safety (partial)

**Missing** (AI SDK Core):
- ❌ Agent interface/API
- ❌ Self-modification engine
- ❌ Learning/adaptation system
- ❌ Code generation/modification capabilities
- ❌ Agent orchestration
- ❌ Prompt evolution system
- ❌ Safety constraints for self-modification
- ❌ Rollback/versioning for changes

### 3. How Does Current Code Serve AI SDK Vision?

**Re-evaluation Needed**:
- Is TavernKeeper (1,014 LOC) a **personality engine** for AI agents?
- Are the 5 context commands **AI context management primitives**?
- Is session analytics the **training data pipeline**?
- Is the decision matrix the **AI reasoning engine**?

## Tickets

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| TKT-ai-sdk-001 | Define "Self-Modifying AI SDK" vision document | open | CRITICAL |
| TKT-ai-sdk-002 | Map existing components to AI SDK architecture | open | CRITICAL |
| TKT-ai-sdk-003 | Identify missing AI SDK core components | open | HIGH |
| TKT-ai-sdk-004 | Design agent interface and API | open | HIGH |
| TKT-ai-sdk-005 | Design self-modification engine | open | HIGH |
| TKT-ai-sdk-006 | Implement learning/adaptation system | open | MEDIUM |
| TKT-ai-sdk-007 | Add safety constraints for self-modification | open | HIGH |

## The New Lens: AI SDK Component Analysis

### Component Re-evaluation

#### _pyrite Memory Structure
**Original Audit**: "File organization for projects"
**AI SDK Lens**: **Persistent vector memory for AI agents**
- `active/` = Agent working memory
- `backlog/` = Agent task queue
- `standards/` = Agent learned patterns/rules

**Status**: ✅ Good foundation, needs AI-specific enhancements

#### Session Analytics (473 LOC)
**Original Audit**: "Over-engineered for meta-framework"
**AI SDK Lens**: **Training data collection pipeline**
- Tracks: files created/modified, lines changed, commands executed
- SQLite storage: Perfect for ML training data
- Prompt signatures: Track what works/doesn't work

**Status**: ✅ Excellent for AI SDK, needs expansion

#### Empirica Integration
**Original Audit**: "Unclear external dependency"
**AI SDK Lens**: **Epistemic state tracking for AI learning**
- Tracks what agent knows/doesn't know
- Safety gates (PROCEED/HALT/BRANCH/REVISE)
- Trajectory projection

**Status**: ✅ Critical for safe AI, keep

#### Decision Matrix (800 LOC)
**Original Audit**: "Over-engineered weighted sum"
**AI SDK Lens**: **AI decision-making framework**
- Structured decision process
- Sensitivity analysis (robust decisions)
- Explainable reasoning

**Status**: ✅ Good start, needs expansion to multiple methodologies

#### Gamification × 2 (1,317 LOC)
**Original Audit**: "Redundant systems"
**AI SDK Lens**: **Dual-layer reward system**
- **GamificationManager** (303 LOC): Quantitative feedback (integrity/insight scores)
- **TavernKeeper** (1,014 LOC): Qualitative feedback (narrative, persona, chronicles)

**Status**: ⚠️ Both useful, but need integration as reward signals for AI learning

#### TavernKeeper RPG (1,014 LOC)
**Original Audit**: "Scope creep, make it a plugin"
**AI SDK Lens**: **Agent personality and narrative feedback system**
- D&D stats = Agent personality dimensions
- Chronicles = Agent memory/learning log
- Dice rolls = Stochastic behavior modeling
- Quests = Agent goal structures

**Status**: ✅ Unique differentiator! Keep in core as **agent persona engine**

#### 5 Context Commands
**Original Audit**: "Too many overlapping commands"
**AI SDK Lens**: **AI context management primitives**
- `checkout` = Load historical agent state
- `resume` = Continue from interruption
- `continue` = Proceed with current context
- `proceed` = Move to next phase
- `reflect` = Meta-cognition checkpoint

**Status**: ⚠️ Each serves different AI context need, but names confusing

#### 3 Task Management Systems
**Original Audit**: "Overlapping, consolidate"
**AI SDK Lens**: **Agent planning hierarchy**
- **GoalManager**: High-level strategic planning
- **WorkflowManager**: Tactical execution sequences
- **ComposeManager**: Natural language → action translation

**Status**: ⚠️ Valid hierarchy, but needs clearer integration

## Proposed AI SDK Architecture

### Layer 1: Foundation (Current - Mostly Built)
```
[Substrate] → uv environment management
[Memory] → _pyrite persistent storage
[Subprocess] → Safe tool execution
[Templates] → Project scaffolding
```
**Status**: ✅ 80% complete, needs security hardening

### Layer 2: Intelligence (Current - Partially Built)
```
[Analytics] → Training data collection
[Empirica] → Epistemic state tracking
[Decision] → Reasoning framework
[Gamification] → Reward signals
```
**Status**: ⚠️ 60% complete, needs integration

### Layer 3: Agent (Missing - Needs Build)
```
[Agent Interface] → API for AI agent interaction
[Self-Modification] → Code/behavior evolution engine
[Learning] → Adaptation from experience
[Safety] → Constraints and rollback
```
**Status**: ❌ 0% complete, critical gap

### Layer 4: Personality (Current - Built but Misunderstood)
```
[TavernKeeper] → Agent persona and narrative
[Chronicles] → Agent memory/experience log
[Quests] → Goal structure and tracking
```
**Status**: ✅ 90% complete, needs framing as AI component

## The Missing Piece: Agent Core

### What's Not Built Yet

**1. Agent Interface**
```python
class WaftAgent:
    """Self-modifying AI agent using Waft infrastructure."""

    def __init__(self, persona: TavernKeeper, memory: MemoryManager):
        self.persona = persona
        self.memory = memory
        self.analytics = SessionAnalytics()
        self.empirica = EmpiricaManager()

    def observe(self, context: str) -> None:
        """Agent observes environment, logs to memory."""
        pass

    def decide(self, options: List[str]) -> str:
        """Agent makes decision using decision framework."""
        pass

    def act(self, action: str) -> Result:
        """Agent executes action, tracks results."""
        pass

    def reflect(self) -> Insights:
        """Agent reflects on actions, learns."""
        pass

    def modify_self(self, improvement: str) -> bool:
        """Agent modifies its own behavior (with safety checks)."""
        pass
```

**2. Self-Modification Engine**
```python
class SelfModificationEngine:
    """Safe self-modification with rollback."""

    def propose_modification(self, code: str) -> Proposal:
        """Agent proposes code change."""
        pass

    def validate_safety(self, proposal: Proposal) -> bool:
        """Check safety constraints."""
        pass

    def apply_modification(self, proposal: Proposal) -> Result:
        """Apply modification with versioning."""
        pass

    def rollback(self, version: str) -> bool:
        """Rollback to previous version."""
        pass
```

**3. Learning System**
```python
class LearningSystem:
    """Learn from experience and improve."""

    def collect_experience(self, session: SessionRecord) -> Experience:
        """Collect training data from session."""
        pass

    def analyze_patterns(self, experiences: List[Experience]) -> Patterns:
        """Identify what works/doesn't work."""
        pass

    def update_behavior(self, patterns: Patterns) -> None:
        """Update agent behavior based on learning."""
        pass
```

## Immediate Actions Required

### 1. Vision Document (CRITICAL)

Create `docs/AI_SDK_VISION.md` that defines:
- What "self-modifying AI SDK" means specifically
- Who the users are (AI researchers? Developers? Agents?)
- What problems it solves
- How self-modification works safely
- Architecture overview
- Roadmap to AI SDK v1

### 2. Component Mapping (CRITICAL)

Document how EVERY current component serves the AI SDK:
- _pyrite → Agent memory
- Session analytics → Training data
- Empirica → Epistemic tracking
- Decision matrix → Reasoning engine
- Gamification → Reward signals
- TavernKeeper → Personality engine
- Commands → Agent primitives

### 3. Gap Analysis (HIGH)

Identify and prioritize missing components:
1. Agent interface (API)
2. Self-modification engine
3. Learning system
4. Safety constraints
5. Agent orchestration

## Impact on Previous Audit

### Security (WE-260109-sec1)
**Status**: **Still CRITICAL**
- Subprocess validation MORE important for AI (agents executing code)
- Input validation CRITICAL (AI-generated input can be malicious)
- Hardcoded paths still break portability

**Action**: Proceed with sec1, but frame as "Safe AI tool execution"

### Architecture (WE-260109-arch)
**Status**: **Still HIGH**, but different framing
- main.py split still needed, but organize by AI SDK layers
- Logging MORE important (AI needs observability)

**Action**: Proceed with arch, reorganize as:
```
commands/
├── foundation.py   # substrate, memory
├── intelligence.py # analytics, empirica, decision
├── agent.py        # agent interface (NEW)
└── personality.py  # tavern, gamification
```

### Scope (WE-260109-scope)
**Status**: **COMPLETELY CHANGED**
- TavernKeeper is NOT scope creep → It's the **personality engine**
- Multiple gamification systems → **Dual reward signals** (quantitative + narrative)
- 5 context commands → **AI context primitives** (need better names)
- 3 task systems → **Agent planning hierarchy** (need integration)

**Action**: Reframe scope as "What's needed for AI SDK v1?" not "What's unnecessary?"

## The New Value Proposition

**Before** (Meta-framework):
> "Waft organizes Python projects with persistent memory and gamification."

**After** (AI SDK):
> "Waft is a self-modifying AI SDK. AI agents use _pyrite for persistent memory, session analytics for learning, decision frameworks for reasoning, and TavernKeeper for personality. Agents safely modify their own behavior based on experience."

**Target Users**:
- AI researchers building autonomous agents
- Developers creating self-improving AI systems
- AI agents themselves (self-hosting)

## Success Criteria

- [ ] **Vision document** defines self-modifying AI SDK clearly
- [ ] **Component map** shows how current code serves AI SDK
- [ ] **Agent interface** designed and documented
- [ ] **Self-modification engine** designed with safety
- [ ] **Learning system** designed
- [ ] **All existing features** reframed through AI lens
- [ ] **README** explains AI SDK vision
- [ ] **Examples** show agent self-modification

## Related Work Efforts

**Depends On**:
- WE-260109-sec1 (security MORE critical for AI)

**Changes**:
- WE-260109-scope (reframe: not "reduce scope", but "organize for AI SDK")
- WE-260109-arch (reorganize by AI SDK layers)

**New Priority**:
- **WE-260109-ai-sdk** (this work effort) becomes HIGHEST priority

## The Bottom Line

**Everything changes with this context.**

What looked like:
- ❌ Scope creep → ✅ AI SDK foundation
- ❌ Over-engineering → ✅ Thoughtful AI infrastructure
- ❌ Confusing features → ✅ Agent primitives
- ❌ D+ quality → ✅ Incomplete but directionally correct

**The Real Issue**: The codebase is building AI SDK components, but **the AI SDK itself (Agent, Self-Modification, Learning) isn't built yet**.

**The Fix**: Not to cut features, but to **complete the AI SDK** and **document the vision** so the architecture makes sense.

---

**Next Steps**: Define the AI SDK vision document, then reassess all work efforts through this lens.
