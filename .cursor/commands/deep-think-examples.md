# Deep Think: Usage Examples

**Examples and use cases for the `/deep-think` command.**

This document provides practical examples of using `/deep-think` for various scenarios.

---

## Example 1: Analyzing Implementation Plan

**Scenario**: You've created a plan for implementing a new feature and want comprehensive analysis before starting.

```
User: "/deep-think plan:feature_authentication"

AI: [Executes 8-phase workflow]

Phase 1: Initializing cognitive tools...
✅ Empirica initialized
✅ Sequential thinking ready
✅ Project context loaded

Phase 2: Adversarial critique...
🔴 CRITICAL: No input validation on user credentials
⚠️ HIGH: Assumes OAuth library is available
⚠️ MEDIUM: Missing error handling for network failures

Phase 3: Reflection...
📝 Documented insights about security-first approach

Phase 4: Assumption validation...
✅ PROVEN: OAuth library is installed (verified in pyproject.toml)
❌ DISPROVEN: Input validation exists (checked code, missing)

Phase 5: Verification...
✅ Verified: Project structure supports authentication
✅ Verified: Required dependencies available

Phase 6: Consider options...
Option 1: Proceed with plan (fix issues as found)
Option 2: Revise plan (add validation, error handling)
Option 3: Create proof-of-concept first

Phase 7: Decision matrix...
Recommended: Option 2 (Revise plan)
Score: 8.5/10
Reasoning: Addresses security issues before implementation

Phase 8: Synthesis...
📋 Revision Plan:
1. Add input validation section (CRITICAL)
2. Add error handling for network failures (HIGH)
3. Verify OAuth library integration (MEDIUM)
4. Create proof-of-concept for complex flows (LOW)

✅ Analysis complete. Revision plan created.
```

---

## Example 2: Framework Selection Decision

**Scenario**: Choosing between FastAPI and Flask for a new API project.

```
User: "/deep-think decision:api_framework"

AI: [Executes workflow focusing on decision-making]

Phase 1: Cognitive tools initialized
Phase 2: Critique of current decision process...
⚠️ Assumption: Performance is the only criterion
⚠️ Missing: Team experience consideration

Phase 3: Reflection...
📝 Noted: Decision seems rushed, need more criteria

Phase 4: Assumption validation...
✅ PROVEN: FastAPI is faster (benchmarks verified)
❌ DISPROVEN: Team only knows Flask (team survey shows Flask experience)

Phase 5: Verification...
✅ Verified: Both frameworks available
✅ Verified: Project requirements documented

Phase 6: Consider options...
Option 1: FastAPI (performance, modern)
Option 2: Flask (team familiarity, ecosystem)
Option 3: Hybrid (FastAPI for new, Flask for existing)

Phase 7: Decision matrix...
Criteria: Performance (0.3), Team Experience (0.4), Ecosystem (0.2), Learning Curve (0.1)

FastAPI: 7.2/10
Flask: 7.8/10
Hybrid: 6.5/10

Recommended: Flask (Score: 7.8)
Reasoning: Team experience outweighs performance gains for this project

Phase 8: Synthesis...
📋 Decision: Use Flask
📋 Rationale: Team familiarity critical for project success
📋 Action: Document decision, proceed with Flask
```

---

## Example 3: Code Review Deep Analysis

**Scenario**: Reviewing a complex refactoring PR before merging.

```
User: "/deep-think code:refactor_persistence_layer"

AI: [Executes workflow for code analysis]

Phase 1: Cognitive tools ready
Phase 2: Security critique...
🔴 CRITICAL: SQL injection risk in query builder
⚠️ HIGH: No transaction rollback on errors
⚠️ MEDIUM: Missing connection pooling limits

Phase 3: Reflection...
📝 Noted: Refactoring is comprehensive but risky

Phase 4: Assumption validation...
✅ PROVEN: Database schema supports new queries
❌ DISPROVEN: Tests cover all edge cases (coverage: 65%)

Phase 5: Verification...
✅ Verified: Database migrations tested
❌ Failed: Integration tests missing for error scenarios

Phase 6: Consider options...
Option 1: Merge as-is (risky)
Option 2: Request changes (add tests, fix security)
Option 3: Merge to feature branch, test more

Phase 7: Decision matrix...
Recommended: Option 2 (Request changes)
Score: 9.0/10
Reasoning: Security issues must be fixed before merge

Phase 8: Synthesis...
📋 Action Plan:
1. Fix SQL injection vulnerability (CRITICAL)
2. Add transaction rollback handling (HIGH)
3. Increase test coverage to 90%+ (HIGH)
4. Add integration tests for error scenarios (MEDIUM)
5. Add connection pooling limits (MEDIUM)

✅ Review complete. Changes requested.
```

---

## Example 4: Architecture Decision

**Scenario**: Deciding between microservices and monolith for new system.

```
User: "/deep-think decision:architecture_pattern"

AI: [Executes comprehensive analysis]

Phase 1: Tools initialized, context loaded
Phase 2: Critique...
⚠️ Assumption: Microservices always better for scale
⚠️ Missing: Team size consideration
⚠️ Missing: Operational complexity analysis

Phase 3: Reflection...
📝 Pattern: Premature optimization detected

Phase 4: Assumption validation...
❌ DISPROVEN: Microservices needed for scale (current load: 100 req/s)
✅ PROVEN: Team is small (5 developers, verified)

Phase 5: Verification...
✅ Verified: Current system is monolith
✅ Verified: Team has monolith experience
❌ Unknown: Future scaling requirements

Phase 6: Consider options...
Option 1: Monolith (simple, team knows it)
Option 2: Microservices (future-proof, complex)
Option 3: Modular monolith (middle ground)

Phase 7: Decision matrix...
Criteria: Complexity (0.3), Team Experience (0.3), Future Scale (0.2), Time to Market (0.2)

Monolith: 8.5/10
Microservices: 5.2/10
Modular Monolith: 7.8/10

Recommended: Monolith (Score: 8.5)
Reasoning: Team experience and simplicity outweigh future concerns

Phase 8: Synthesis...
📋 Decision: Start with monolith
📋 Rationale: YAGNI principle, optimize when needed
📋 Future: Plan migration path if scale requires it
📋 Action: Document decision, proceed with monolith
```

---

## Example 5: Feature Priority Analysis

**Scenario**: Multiple features requested, need to prioritize.

```
User: "/deep-think decision:feature_priority"

AI: [Analyzes feature requests]

Phase 1: Cognitive tools ready
Phase 2: Critique of prioritization process...
⚠️ Missing: User value quantification
⚠️ Missing: Technical debt consideration

Phase 3: Reflection...
📝 Noted: Need data-driven prioritization

Phase 4: Assumption validation...
✅ PROVEN: User requests tracked (verified in issue tracker)
❌ DISPROVEN: All features equally important (user votes show clear winners)

Phase 5: Verification...
✅ Verified: Feature requests documented
✅ Verified: Technical debt quantified

Phase 6: Consider options...
Option 1: Build all features (not feasible)
Option 2: Prioritize by user votes
Option 3: Prioritize by business value + technical debt

Phase 7: Decision matrix...
Features: Auth (9.2), Search (7.8), Analytics (6.5), Themes (5.1)

Recommended Order:
1. Auth (CRITICAL - security)
2. Search (HIGH - user value)
3. Analytics (MEDIUM - nice to have)
4. Themes (LOW - cosmetic)

Phase 8: Synthesis...
📋 Priority Plan:
1. Auth system (Week 1-2)
2. Search functionality (Week 3-4)
3. Analytics dashboard (Week 5-6)
4. Theme system (Week 7-8)

✅ Prioritization complete. Roadmap created.
```

---

## Best Practices

### When to Use `/deep-think`

✅ **Use for**:
- Important implementation plans
- Architecture decisions
- Security-critical code reviews
- Feature prioritization
- Framework/library selection
- Major refactoring decisions

❌ **Don't use for**:
- Quick decisions (use `/consider` or `/decide` alone)
- Simple problems (individual commands suffice)
- Time-constrained situations (workflow takes 30-60 minutes)

### Workflow Tips

1. **Be Specific**: Provide clear target (plan name, decision context)
2. **Allow Time**: Full workflow takes 30-60 minutes
3. **Review All Phases**: Each phase provides valuable insights
4. **Act on Findings**: Use revision plan to improve target
5. **Iterate**: Can run multiple times as target evolves

### Integration Tips

- Use with `/think` first if cognitive tools not initialized
- Follow up with `/checkpoint` to document decisions
- Use `/verify` for quick checks between deep analyses
- Combine with `/reflect` for ongoing learning

---

## Output Locations

All `/deep-think` outputs are saved to:

- **Critique Reports**: `_work_efforts/CRITIQUE_YYYY-MM-DD_HHMMSS.md`
- **Reflection Entries**: `_pyrite/journal/ai-journal.md`
- **Assumption Validation**: `_work_efforts/ASSUMPTIONS_VALIDATION_YYYY-MM-DD_HHMMSS.md`
- **Verification Traces**: `_pyrite/standards/verification/traces/`
- **Synthesis Reports**: `_work_efforts/DEEP_THINK_ANALYSIS_YYYY-MM-DD_HHMMSS.md`
- **Revised Plans**: `.cursor/plans/` (if analyzing plans)

---

**These examples demonstrate the comprehensive cognitive workflow in action, showing how `/deep-think` provides thorough analysis, validation, and decision support for complex problems.**