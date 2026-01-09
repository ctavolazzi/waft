# Waft: Self-Modifying AI SDK Vision

**Version**: 1.0  
**Date**: 2026-01-09  
**Status**: Foundation Document  
**Purpose**: Define the vision, architecture, and roadmap for Waft as a self-modifying AI SDK

---

## Executive Summary

**Waft is a self-modifying AI SDK that enables AI agents to observe, decide, act, and learn within Python projects.** Unlike traditional agent frameworks (LangChain, AutoGPT, MetaGPT), Waft provides agents with the ability to safely modify code, adapt behavior, and evolve project structure based on experience.

**Core Value Proposition**: Waft transforms AI agents from passive assistants into active project participants that can improve themselves and the projects they work on.

---

## What is "Self-Modifying"?

### Definition

**Self-modification** in Waft means AI agents can:

1. **Modify Code** - Safely edit Python files, add functions, refactor code
2. **Tune Parameters** - Adjust configuration, hyperparameters, and settings
3. **Evolve Prompts** - Optimize their own prompts based on outcomes
4. **Change Architecture** - Restructure projects, add modules, reorganize code
5. **Learn from Experience** - Adapt behavior based on session history and outcomes

### Types of Self-Modification

#### 1. Code Generation & Modification
- **What**: Agents can create, edit, and delete Python files
- **Example**: Agent adds a new API endpoint after analyzing usage patterns
- **Safety**: All changes validated, tested, and reversible

#### 2. Parameter Tuning
- **What**: Agents adjust configuration values, thresholds, and settings
- **Example**: Agent optimizes decision matrix weights based on historical outcomes
- **Safety**: Changes tracked, validated against constraints

#### 3. Prompt Evolution
- **What**: Agents refine their own prompts through iterative testing
- **Example**: Agent improves code generation prompts by analyzing success rates
- **Safety**: Prompt changes logged, A/B tested, rolled back if worse

#### 4. Architecture Changes
- **What**: Agents restructure project organization, add modules, refactor
- **Example**: Agent splits monolithic file into modules after detecting complexity
- **Safety**: Structural changes validated, dependencies checked

#### 5. Behavioral Adaptation
- **What**: Agents change decision-making logic based on experience
- **Example**: Agent learns to prefer certain refactoring patterns that work better
- **Safety**: Behavioral changes monitored, can be reverted

---

## Who Are the Users?

### Primary Users

1. **AI Researchers** - Building self-improving agent systems
   - Need: Framework for agent autonomy and learning
   - Use Case: Research into agent self-modification, meta-learning

2. **Developers Creating Self-Improving Systems** - Building production agents
   - Need: Safe, validated self-modification capabilities
   - Use Case: Agents that maintain and improve codebases autonomously

3. **AI Agents Themselves** - Self-hosting agents using Waft
   - Need: Direct API for self-modification
   - Use Case: Agents that use Waft to improve their own code

### Secondary Users

4. **DevOps Engineers** - Automating project maintenance
   - Need: Agents that can safely modify production code
   - Use Case: Automated dependency updates, security patches

5. **Code Review Systems** - Automated code improvement
   - Need: Agents that can propose and apply fixes
   - Use Case: Automated refactoring, bug fixes, optimization

---

## What Makes Waft Different?

### Comparison Matrix

| Feature | Waft | LangChain | AutoGPT | MetaGPT |
|--------|------|-----------|---------|---------|
| **Agent Framework** | ✅ | ✅ | ✅ | ✅ |
| **Self-Modification** | ✅ **Core** | ❌ | ⚠️ Limited | ❌ |
| **Safety Validation** | ✅ **Built-in** | ❌ | ⚠️ Basic | ❌ |
| **Learning System** | ✅ **Active** | ❌ | ⚠️ Passive | ❌ |
| **Project Integration** | ✅ **Native** | ⚠️ External | ⚠️ External | ⚠️ External |
| **Epistemic Tracking** | ✅ **Empirica** | ❌ | ❌ | ❌ |
| **Decision Engine** | ✅ **Built-in** | ❌ | ❌ | ❌ |
| **Gamification** | ✅ **TavernKeeper** | ❌ | ❌ | ❌ |

### Key Differentiators

1. **Native Self-Modification** - Not an add-on, but core to the framework
2. **Safety-First Design** - All modifications validated, tested, reversible
3. **Learning System** - Agents learn from experience, not just execute
4. **Project-Aware** - Deep integration with project structure and state
5. **Epistemic Tracking** - Built-in knowledge measurement (Empirica)
6. **Decision Framework** - Mathematical decision engine for agent reasoning
7. **Personality System** - Gamification and narrative (TavernKeeper) for agent identity

---

## Component Mapping: Current State → AI SDK Role

### Foundation Layer (80% Complete)

| Component | Current State | AI SDK Role | Status |
|-----------|--------------|-------------|--------|
| **Substrate Manager** | Manages `uv` and `pyproject.toml` | Agent environment management | ✅ Built |
| **Memory Manager** | Manages `_pyrite/` structure | Agent persistent memory | ✅ Built |
| **GitHub Manager** | GitHub integration | Agent version control | ✅ Built |

### Intelligence Layer (60% Complete)

| Component | Current State | AI SDK Role | Status |
|-----------|--------------|-------------|--------|
| **Session Analytics** | Collects session data (SQLite) | Training data pipeline | ✅ Built (data collection) |
| **Empirica Manager** | Epistemic tracking | Agent knowledge measurement | ✅ Built |
| **Decision Matrix** | Weighted Sum Model (WSM) | Agent reasoning framework | ✅ Built |
| **Input Transformer** | Validates decision inputs | Agent input validation | ✅ Built |

### Personality Layer (90% Complete)

| Component | Current State | AI SDK Role | Status |
|-----------|--------------|-------------|--------|
| **Gamification Manager** | Integrity, Insight, Levels | Agent reward signals | ✅ Built |
| **TavernKeeper** | D&D 5e RPG mechanics | Agent personality engine | ✅ Built |
| **Narrator** | Procedural narratives | Agent storytelling | ✅ Built |

### Agent Layer (0% Complete) ← **THE GAP**

| Component | Current State | AI SDK Role | Status |
|-----------|--------------|-------------|--------|
| **Agent Interface** | ❌ Missing | Base Agent class | ❌ **NOT BUILT** |
| **Self-Mod Engine** | ❌ Missing | Safe code modification | ❌ **NOT BUILT** |
| **Learning System** | ⚠️ Data only | Agent adaptation | ❌ **NOT BUILT** |
| **Safety Validator** | ⚠️ Partial | Modification validation | ❌ **NOT BUILT** |

---

## Architecture: The Four-Layer Model

```
┌─────────────────────────────────────────────────────────┐
│  Agent Layer (0%)                                        │  ← TO BE BUILT
│  ─────────────────────────────────────────────────────   │
│  • WaftAgent (base class)                                │
│  • SelfModificationEngine (safe code changes)            │
│  • LearningSystem (adapt from experience)               │
│  • SafetyValidator (modification validation)             │
├─────────────────────────────────────────────────────────┤
│  Personality Layer (90%)                                 │
│  ─────────────────────────────────────────────────────   │
│  • TavernKeeper (RPG mechanics, agent identity)          │
│  • GamificationManager (reward signals)                  │
│  • Narrator (procedural storytelling)                    │
├─────────────────────────────────────────────────────────┤
│  Intelligence Layer (60%)                                │
│  ─────────────────────────────────────────────────────   │
│  • SessionAnalytics (training data)                       │
│  • EmpiricaManager (epistemic tracking)                  │
│  • DecisionMatrix (reasoning framework)                  │
│  • InputTransformer (validation)                          │
├─────────────────────────────────────────────────────────┤
│  Foundation Layer (80%)                                  │
│  ─────────────────────────────────────────────────────   │
│  • SubstrateManager (environment)                        │
│  • MemoryManager (persistent state)                     │
│  • GitHubManager (version control)                       │
└─────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

#### Foundation Layer
- **Purpose**: Provide stable base for agents
- **Components**: Substrate, Memory, GitHub
- **Status**: 80% complete, needs minor enhancements

#### Intelligence Layer
- **Purpose**: Enable agent reasoning and learning
- **Components**: Analytics, Empirica, Decision Engine
- **Status**: 60% complete, needs learning system activation

#### Personality Layer
- **Purpose**: Give agents identity and motivation
- **Components**: TavernKeeper, Gamification, Narrator
- **Status**: 90% complete, mostly done

#### Agent Layer
- **Purpose**: Enable self-modification and autonomy
- **Components**: Agent Interface, Self-Mod Engine, Learning System
- **Status**: 0% complete, **THE CRITICAL GAP**

---

## Concrete Examples

### Example 1: Agent Self-Improvement

**Scenario**: Agent notices its code generation prompts are producing verbose code.

**Agent Actions**:
1. **Observe**: Analyzes session history, finds verbose code patterns
2. **Decide**: Uses decision matrix to evaluate prompt modification options
3. **Act**: Modifies its own prompt template to emphasize conciseness
4. **Reflect**: Tracks outcomes, measures improvement (lines of code, readability)
5. **Learn**: Updates prompt optimization strategy based on results

**Waft Components Used**:
- `SessionAnalytics` - Analyze historical patterns
- `DecisionMatrix` - Evaluate modification options
- `SelfModificationEngine` - Safely modify prompt file
- `LearningSystem` - Update optimization strategy
- `EmpiricaManager` - Track epistemic changes

### Example 2: Project Refactoring Agent

**Scenario**: Agent detects code complexity exceeding thresholds.

**Agent Actions**:
1. **Observe**: Scans codebase, identifies complex functions (>50 lines, high cyclomatic complexity)
2. **Decide**: Uses decision matrix to choose refactoring strategy (extract function vs. split module)
3. **Act**: Safely refactors code, splits functions, adds tests
4. **Reflect**: Verifies tests pass, measures complexity reduction
5. **Learn**: Updates refactoring preferences based on success rates

**Waft Components Used**:
- `MemoryManager` - Access project structure
- `DecisionMatrix` - Choose refactoring approach
- `SelfModificationEngine` - Modify code files safely
- `SessionAnalytics` - Track refactoring outcomes
- `TavernKeeper` - Narrative of refactoring quest

### Example 3: Dependency Management Agent

**Scenario**: Agent detects outdated dependencies with security vulnerabilities.

**Agent Actions**:
1. **Observe**: Scans `pyproject.toml`, checks vulnerability database
2. **Decide**: Evaluates update risk (breaking changes vs. security)
3. **Act**: Updates dependencies, runs tests, fixes breaking changes
4. **Reflect**: Verifies all tests pass, no regressions
5. **Learn**: Updates dependency update strategy (prefer minor updates, test major)

**Waft Components Used**:
- `SubstrateManager` - Manage dependencies
- `DecisionMatrix` - Evaluate update risks
- `SelfModificationEngine` - Update `pyproject.toml` safely
- `SessionAnalytics` - Track update success rates
- `GitHubManager` - Commit changes with descriptive messages

---

## Safety Model

### Safety Levels

#### Level 1: Read-Only (No Validation Required)
- **Operations**: Read files, query state, analyze code
- **Risk**: None
- **Validation**: None required
- **Example**: `agent.observe()` - Scan project structure

#### Level 2: Low-Risk Modifications (Basic Validation)
- **Operations**: Add comments, update documentation, create new files
- **Risk**: Low (non-functional changes)
- **Validation**: Syntax check, file existence
- **Example**: `agent.add_documentation()` - Add docstrings

#### Level 3: Medium-Risk Modifications (Test Validation)
- **Operations**: Refactor code, add functions, modify logic
- **Risk**: Medium (functional changes)
- **Validation**: Syntax check, tests must pass, no breaking changes
- **Example**: `agent.refactor_function()` - Extract function, run tests

#### Level 4: High-Risk Modifications (Human Approval)
- **Operations**: Delete files, change architecture, modify core logic
- **Risk**: High (structural changes)
- **Validation**: Full validation + human approval required
- **Example**: `agent.restructure_project()` - Split monolith, requires approval

### Safety Constraints

#### 1. Validation Pipeline
```
Modification Request
  ↓
Syntax Validation (AST parsing)
  ↓
Dependency Check (imports, references)
  ↓
Test Execution (if Level 3+)
  ↓
Safety Gate (Empirica CHECK)
  ↓
Approval (if Level 4)
  ↓
Apply Modification
  ↓
Rollback Point Created
```

#### 2. Rollback System
- **Automatic Rollback**: If tests fail after modification
- **Manual Rollback**: Agent can rollback to any previous state
- **Rollback Points**: Created before every modification
- **Storage**: Git commits + Waft rollback metadata

#### 3. Approval Gates
- **PROCEED**: Safe to continue autonomously (Level 1-2)
- **BRANCH**: Need investigation before proceeding (Level 3, uncertain)
- **HALT**: Requires human approval (Level 4)
- **REVISE**: Approach needs revision (safety check failed)

#### 4. Modification Boundaries
- **What Agents CAN Modify**:
  - Code files in `src/`
  - Configuration files (`pyproject.toml`, `.env.example`)
  - Documentation files
  - Test files

- **What Agents CANNOT Modify**:
  - Git history (`.git/`)
  - Waft core (`src/waft/` in Waft itself)
  - Lock files without validation (`uv.lock`)
  - System files outside project

---

## Roadmap to v1.0

### Phase 1: Vision & Design (Current)
- ✅ **Complete**: Vision document (this document)
- ⏳ **Next**: Design Agent Interface (TKT-ai-sdk-002)
- ⏳ **Next**: Design Self-Modification Engine (TKT-ai-sdk-003)
- ⏳ **Next**: Design Learning System (TKT-ai-sdk-004)

**Timeline**: 2-3 weeks  
**Deliverable**: Complete architecture design

### Phase 2: Core Agent Layer (v0.1.0)
- ⏳ **Build**: `WaftAgent` base class
- ⏳ **Build**: Basic `observe()` / `decide()` / `act()` / `reflect()` cycle
- ⏳ **Build**: Project state observation
- ⏳ **Build**: Integration with Decision Matrix

**Timeline**: 4-6 weeks  
**Deliverable**: Agents can observe and make decisions

### Phase 3: Self-Modification Engine (v0.2.0)
- ⏳ **Build**: `SelfModificationEngine` class
- ⏳ **Build**: Safety validation pipeline
- ⏳ **Build**: Rollback system
- ⏳ **Build**: Code modification primitives (add/remove/edit functions)

**Timeline**: 6-8 weeks  
**Deliverable**: Agents can safely modify code

### Phase 4: Learning System (v0.3.0)
- ⏳ **Build**: `LearningSystem` class
- ⏳ **Build**: Outcome analysis from Session Analytics
- ⏳ **Build**: Prompt optimization
- ⏳ **Build**: Behavioral adaptation

**Timeline**: 6-8 weeks  
**Deliverable**: Agents learn from experience

### Phase 5: Integration & Polish (v0.4.0)
- ⏳ **Integrate**: Agent layer with all existing components
- ⏳ **Enhance**: TavernKeeper integration (agent narratives)
- ⏳ **Enhance**: Empirica integration (agent epistemic tracking)
- ⏳ **Build**: Example agents (refactoring, testing, documentation)

**Timeline**: 4-6 weeks  
**Deliverable**: Complete integrated system

### Phase 6: Production Ready (v1.0.0)
- ⏳ **Security**: Security audit and hardening
- ⏳ **Testing**: Comprehensive test suite
- ⏳ **Documentation**: Complete API docs, tutorials
- ⏳ **Examples**: Production-ready example agents
- ⏳ **Performance**: Optimization and profiling

**Timeline**: 4-6 weeks  
**Deliverable**: Production-ready AI SDK

**Total Timeline**: 26-37 weeks (~6-9 months)

---

## Key Questions Answered

### 1. What type of self-modification?
**Answer**: All of the above (code, parameters, prompts, architecture, behavior). Waft supports the full spectrum of self-modification, with appropriate safety constraints for each type.

### 2. Who are the users?
**Answer**: Primary users are AI researchers, developers building self-improving systems, and AI agents themselves. Secondary users include DevOps engineers and code review systems.

### 3. What makes Waft different?
**Answer**: Native self-modification (not an add-on), safety-first design, active learning system, deep project integration, epistemic tracking, decision framework, and personality system. No other framework combines all these capabilities.

### 4. What's the safety model?
**Answer**: Four-tier safety model (Read-Only, Low-Risk, Medium-Risk, High-Risk) with validation pipeline, rollback system, approval gates (PROCEED/BRANCH/HALT/REVISE), and clear modification boundaries. All modifications are validated, tested, and reversible.

---

## Success Criteria

### Technical Success
- [ ] Agents can observe project state
- [ ] Agents can make decisions using Decision Matrix
- [ ] Agents can safely modify code (all safety levels)
- [ ] Agents can learn from experience
- [ ] All modifications are validated and reversible
- [ ] Integration with all existing components (Empirica, TavernKeeper, etc.)

### User Success
- [ ] Researchers can build self-improving agents
- [ ] Developers can deploy production agents
- [ ] Agents can use Waft to improve themselves
- [ ] Clear documentation and examples
- [ ] Safety model is trusted and proven

### Business Success
- [ ] Waft is recognized as the leading self-modifying AI SDK
- [ ] Active community of agent developers
- [ ] Production deployments in real projects
- [ ] Research papers citing Waft

---

## Next Steps

1. **Immediate**: Review and approve this vision document
2. **Next**: Design Agent Interface (TKT-ai-sdk-002)
3. **Parallel**: Execute Security Fixes (WE-260109-sec1) - critical for agent safety
4. **Then**: Design Self-Modification Engine (TKT-ai-sdk-003)
5. **Finally**: Design Learning System (TKT-ai-sdk-004)

---

## Conclusion

Waft is positioned to become the **first production-ready self-modifying AI SDK**. With 80% of the foundation already built, the critical gap is the Agent Layer. This vision document provides the roadmap to bridge that gap and realize Waft's full potential.

**The future of AI agents is self-modification. Waft will make it safe, validated, and production-ready.**

---

**Document Status**: ✅ Complete  
**Next Action**: Design Agent Interface (TKT-ai-sdk-002)  
**Blocking**: None (this document unblocks all AI SDK work)
