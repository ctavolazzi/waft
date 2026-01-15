# Deep Think

**Orchestrate comprehensive cognitive workflow for deep analysis and decision-making.**

Applies the full cognitive toolkit in sequence: initialize cognitive tools, adversarial critique, reflection, assumption validation, verification, consideration of options, mathematical decision-making, and synthesis into actionable revision plans.

**Use when:** Need to deeply analyze a plan before implementation, want comprehensive cognitive review of decisions, need to validate assumptions and verify claims, or preparing for significant work that requires thorough analysis.

---

## Purpose

This command provides:
- **Comprehensive Cognitive Analysis**: Full 8-phase workflow for deep thinking
- **Security-First Critique**: Adversarial analysis finding vulnerabilities and assumptions
- **Evidence-Based Validation**: Prove/disprove assumptions with traceable evidence
- **Structured Decision-Making**: Mathematical decision matrix with calculated recommendations
- **Synthesis & Action**: Combined insights into actionable revision plans
- **Epistemic Tracking**: Full integration with Empirica and cognitive tools

---

## Philosophy

1. **Deep Analysis Requires Full Toolkit**: Use all available cognitive tools for comprehensive analysis
2. **Security First**: Adversarial critique finds problems before they become issues
3. **Evidence Over Belief**: Validate assumptions with proof, not faith
4. **Structured Decision-Making**: Quantitative analysis for better decisions
5. **Synthesis Creates Action**: Combine all insights into actionable plans
6. **Traceable Process**: Document everything for future reference

---

## Execution Steps

### Phase 1: Initialize Cognitive Tools (`/think`)

**Purpose**: Activate all cognitive enhancement tools

**Actions**:
1. **Verify Environment**
   - Check current date/time
   - Verify Python version (3.11+ for Empirica)
   - Check if git is initialized
   - Verify Empirica CLI availability
   - Check MCP servers (sequential-thinking, work-efforts)

2. **Initialize Empirica**
   - Check if Empirica is initialized: `uv run empirica project-info`
   - If not initialized, run: `uv run empirica project-init`
   - Verify initialization: Check for `.empirica/config.yaml`

3. **Create Empirica Session**
   - Create session: `uv run empirica session-create --ai-id waft --output json`
   - Capture session ID from response
   - Store session ID for use in preflight/postflight

4. **Project Bootstrap**
   - Run: `uv run empirica project-bootstrap --output json`
   - Extract epistemic state, goals, findings, unknowns
   - Display summary of current knowledge state

5. **Initialize Sequential Thinking**
   - Check if Sequential Thinking MCP is available
   - Prepare for hierarchical planning use

6. **Activate Work Efforts System**
   - Check if `_work_efforts/` directory exists
   - List active work efforts if available
   - Verify work-efforts MCP server

7. **Assess Current State**
   - Run epistemic state assessment (if Empirica initialized)
   - Check current work efforts status
   - Review recent devlog entries
   - Assess current knowledge gaps

**Output**: Cognitive tools ready, epistemic state loaded, session ID captured

---

### Phase 2: Adversarial Critique (`/critique`)

**Purpose**: Security-first, bad-faith analysis to find all problems

**Actions**:
1. **Locate Target**
   - Check if target provided as argument (plan, decision, code, etc.)
   - Check for most recent plan in `~/.cursor/plans/` or `.cursor/plans/`
   - Check if target content provided directly
   - If no target found, ask user to specify

2. **Security-First Analysis (CRITICAL)**
   - **File System Security**: Check for sensitive file access, symlink attacks, path traversal
   - **Code Execution Security**: Check for arbitrary code execution, command injection, shell injection
   - **Data Security**: Check for sensitive data storage, information disclosure, logging issues
   - **Network Security**: Check for SSRF vulnerabilities, malicious URLs, supply chain attacks
   - **Dependency Security**: Check for pinned dependencies, known CVEs, attack surface
   - **Access Control**: Check for privilege escalation, unauthorized writes
   - **Input Validation**: Check for path traversal, injection attacks, ReDoS

3. **Unexamined Assumptions Analysis**
   - **File System Assumptions**: Writable filesystem, directory structure, encoding, permissions
   - **Dependency Assumptions**: Installed dependencies, versions, external tools, network access
   - **Environment Assumptions**: Python version, OS type, locale, timezone
   - **Data Assumptions**: Format, size, encoding, structure
   - **Behavior Assumptions**: Return types, exceptions, atomicity, idempotency
   - **User Assumptions**: Permissions, understanding, automation preferences

4. **Overengineering Detection**
   - **Architecture Overengineering**: Too many layers, components, premature optimization
   - **Pattern Overengineering**: Unnecessary patterns, over-abstraction
   - **Data Overengineering**: Over-complex structures, over-normalization
   - **Process Overengineering**: Too many steps, unnecessary validation

5. **Oversight Detection**
   - **Error Handling**: Missing try/except, validation, null checks, edge cases
   - **Resource Management**: Missing file closing, cleanup, connection closing
   - **Testing**: No tests, missing cases, no integration tests, no security tests
   - **Documentation**: Missing README, API docs, examples, error docs
   - **Deployment**: Missing steps, configuration, migration, rollback
   - **Performance**: No considerations for speed, scalability, memory, concurrency

6. **Missed Obviousness Detection**
   - **Obvious Security Issues**: Hardcoded secrets, debug code, exposed endpoints
   - **Obvious Functionality Issues**: Missing main function, no error messages, no logging
   - **Obvious Design Issues**: Circular dependencies, tight coupling, god objects
   - **Obvious Process Issues**: No version control, code review, CI/CD, monitoring

7. **Generate Critique Report**
   - Create markdown document with sections:
     - Executive Summary
     - CRITICAL: Security Vulnerabilities
     - HIGH: Safety Issues
     - MEDIUM: Unexamined Assumptions
     - LOW: Overengineering
     - Oversights
     - Missed Obviousness
     - Recommendations (prioritized by severity)
   - Save to `_work_efforts/CRITIQUE_YYYY-MM-DD_HHMMSS.md`

**Output**: Comprehensive critique report with prioritized issues

---

### Phase 3: Reflection (`/reflect`)

**Purpose**: Capture thoughts, learnings, and insights

**Actions**:
1. **Write Journal Entry**
   - Create dated entry in `_pyrite/journal/ai-journal.md`
   - Structure with sections:
     - What I'm Doing (current analysis)
     - What I'm Thinking (thoughts, concerns, ideas)
     - What I'm Learning (insights, discoveries, learnings)
     - Patterns I Notice (recurring themes, patterns)
     - Questions I Have (unanswered questions, curiosities)
     - How I Feel About This (emotional/experiential reflection)
     - What I'd Do Differently (improvements, adjustments)
     - Meta-Reflection (thinking about thinking)

2. **Document Insights from Critique**
   - Record key findings from Phase 2
   - Note surprising discoveries
   - Capture concerns raised

3. **Record Patterns Noticed**
   - Recurring themes across analysis
   - Common issues or strengths
   - Structural patterns

4. **Capture Questions Raised**
   - Unanswered questions from critique
   - Areas needing clarification
   - Uncertainties to explore

5. **Note Emotional/Intuitive Responses**
   - What feels right or wrong
   - Intuitive concerns
   - Gut reactions to findings

**Output**: Journal entry with comprehensive reflection

---

### Phase 4: Assumption Validation (`/check-assumptions`)

**Purpose**: Prove/disprove assumptions with evidence

**Actions**:
1. **Extract Assumptions**
   - From critique report (Phase 2)
   - From conversation history
   - From target being analyzed
   - Categorize by type:
     - Code assumptions
     - Dependency assumptions
     - Data assumptions
     - System assumptions
     - Behavioral assumptions
   - Prioritize by risk (critical vs minor)

2. **Gather Evidence from Multiple Sources**
   - **Code Analysis**: Search codebase, read source files, check signatures, verify types
   - **File System Checks**: Verify files exist, check contents, verify structure, check permissions
   - **Test Results**: Run relevant tests, check coverage, review results
   - **Git History**: Check recent commits, review changes
   - **Empirica/Oracle**: Check epistemic state, review findings, check unknowns
   - **Scientific Method Tool**: Form hypothesis, design test, run experiment
   - **Documentation**: Check README files, review docs, verify documented behavior
   - **External Dependencies**: Check if tools exist, verify versions, test availability

3. **Validate Each Assumption**
   - Match evidence to assumption
   - Evaluate evidence:
     - **PROVEN**: Strong evidence supports
     - **DISPROVEN**: Strong evidence contradicts
     - **PARTIALLY PROVEN**: Mixed evidence
     - **INSUFFICIENT EVIDENCE**: Not enough to determine
     - **NEEDS TESTING**: Requires experiment
   - Assign confidence level (0.0-1.0)
   - Create evidence summary
   - Update risk assessment

4. **Generate Validation Report**
   - Summary table with all assumptions and status
   - Detailed results for each assumption:
     - Assumption statement
     - Category and risk level
     - Validation status
     - Confidence level
     - Evidence summary
     - Specific evidence points
   - Critical findings highlighted
   - Recommendations for next steps
   - Evidence traces with links

**Output**: Assumption validation report with evidence

---

### Phase 5: Verification (`/verify`)

**Purpose**: Lightweight verification with traceable evidence

**Actions**:
1. **Identify Verifiable Claims**
   - From target being analyzed
   - From critique report
   - From assumption validation
   - From conversation history

2. **Run Verification Checks**
   - **Environment Verification**:
     - Date and time accuracy
     - Disk space availability
     - Working directory
   - **Project State Verification**:
     - Project structure validity
     - Git repository state
     - Project version
   - **Tool Availability Verification**:
     - Required CLI tools available
     - MCP servers operational
     - Python/Node/etc. versions
   - **File/Directory Verification**:
     - Claimed files exist
     - Claimed directories exist
     - File content matches claims
   - **Configuration Verification**:
     - Configuration values
     - Environment variables
   - **Dependency Verification**:
     - Dependencies installed
     - Dependency versions
   - **Work Effort Verification**:
     - Active work efforts
     - Work effort details
   - **GitHub State Verification**:
     - Repository exists
     - Recent commits
     - Open issues/PRs

3. **Document Traces with Evidence**
   - Create trace document for each check
   - Include:
     - Claim
     - Verification method
     - Evidence
     - Result
     - Notes
     - Next verification
   - Save to `_pyrite/standards/verification/traces/YYYY-MM-DD_verify-XXXX_[check-name].md`

4. **Update Verification Index**
   - Add traces to `_pyrite/standards/verification/index.md`
   - Update checks catalog

**Output**: Verification report with traceable evidence

---

### Phase 6: Consider Options (`/consider`)

**Purpose**: Analyze alternatives and trade-offs

**Actions**:
1. **Assess Current Situation**
   - Review current state from all previous phases
   - Check progress and status
   - Identify context and constraints
   - Note any blockers

2. **Identify Options**
   - List possible paths forward
   - Consider alternatives to current approach
   - Think about hybrid approaches
   - Include "do nothing" if relevant
   - Include "revise plan" option

3. **Evaluate Each Option**
   - **Pros**: Benefits and advantages
   - **Cons**: Costs and disadvantages
   - **Effort**: Time/complexity required
   - **Risk**: Potential issues and concerns
   - **Impact**: What changes with each option
   - **Best For**: When this option is ideal

4. **Form Recommendations**
   - Best option with reasoning
   - When alternatives might be better
   - Risk mitigation strategies
   - Next steps for chosen path

5. **Present Findings**
   - Situation analysis
   - Options analysis with trade-offs
   - Recommendations
   - Risk assessment

**Output**: Options analysis with recommendations

---

### Phase 7: Decide (`/decide`)

**Purpose**: Mathematical decision matrix calculation

**Actions**:
1. **Define Decision Problem**
   - What decision needs to be made?
   - What is the context?
   - What are the constraints?
   - What is the timeline?

2. **Identify Alternatives**
   - List all viable options (from Phase 6)
   - Include "revise plan" option
   - Ensure alternatives are mutually exclusive
   - Consider hybrid approaches

3. **Define Evaluation Criteria**
   - What factors matter for this decision?
   - What are the success criteria?
   - What are the constraints?
   - What are the risks?
   - Categorize: must-have vs. nice-to-have, cost vs. benefit

4. **Assign Weights to Criteria**
   - How important is each criterion relative to others?
   - Use consistent scale (1-10, percentages, or pairwise comparison)
   - Ensure weights sum to 1.0 (or normalize)
   - Consider using AHP for complex weighting

5. **Score Each Alternative**
   - Evaluate each alternative on each criterion
   - Use consistent scale (1-10 recommended)
   - Consider objective data when available
   - Document reasoning for scores

6. **Perform Calculations**
   - Calculate weighted scores for each alternative
   - Use Weighted Sum Model (WSM) by default:
     ```
     Total Score = Σ (Weight_i × Score_i) for all criteria
     ```
   - Or use Weighted Product Model (WPM) if appropriate:
     ```
     Total Score = Π (Score_i ^ Weight_i) for all criteria
     ```
   - Calculate sensitivity analysis
   - Check for consistency (if using AHP)

7. **Analyze Results**
   - Rank alternatives by total score
   - Identify score differences
   - Consider sensitivity to weight changes
   - Evaluate if results make sense

8. **Present Findings**
   - Decision matrix table
   - Calculation details
   - Rankings
   - Recommendations
   - Sensitivity analysis

**Output**: Decision matrix with calculated recommendation

---

### Phase 8: Synthesis & Action Plan

**Purpose**: Combine all insights into actionable revision plan

**Actions**:
1. **Synthesize Findings from All Phases**
   - Combine insights from:
     - Critique report (Phase 2)
     - Reflection entry (Phase 3)
     - Assumption validation (Phase 4)
     - Verification traces (Phase 5)
     - Options analysis (Phase 6)
     - Decision matrix (Phase 7)
   - Identify common themes
   - Find contradictions or conflicts
   - Highlight key insights

2. **Prioritize Issues by Severity**
   - CRITICAL: Security vulnerabilities, show-stoppers
   - HIGH: Safety issues, major problems
   - MEDIUM: Assumptions needing validation, moderate issues
   - LOW: Overengineering, minor issues
   - Organize by priority for action

3. **Create Revision Plan**
   - For each prioritized issue:
     - Issue description
     - Recommended fix
     - Effort required
     - Dependencies
     - Success criteria
   - Sequence fixes by priority and dependencies
   - Include rollback/revision mechanism
   - Add checkpoint stages

4. **Document Decisions Made**
   - Record decisions from Phase 7 (decision matrix)
   - Document reasoning
   - Note alternatives considered
   - Capture trade-offs accepted

5. **Update Original Plan (if applicable)**
   - If analyzing a plan file:
     - Create revised version
     - Document changes made
     - Preserve original for reference
     - Update todos and status

6. **Create Action Items**
   - Convert revision plan into actionable todos
   - Assign priorities
   - Set dependencies
   - Estimate effort
   - Create work effort (if applicable)

**Output**: Comprehensive analysis report + revision plan

---

## Output Format

### Executive Summary

```
🧠 DEEP-THINK: Comprehensive Cognitive Analysis

Target: [plan/decision/code name]
Analysis Date: [timestamp]
Epistemic State: [knowledge percentage, uncertainty]

Summary:
- 🔴 CRITICAL Issues: [count]
- ⚠️ HIGH Issues: [count]
- ⚠️ MEDIUM Issues: [count]
- ✅ Validated Assumptions: [count]
- ❌ Disproven Assumptions: [count]
- 🧪 Needs Testing: [count]
- ✅ Verified Claims: [count]
- 📊 Decision Recommendation: [option]
- 📋 Action Items: [count]
```

### Detailed Reports

1. **Phase 1 Report**: Cognitive tools initialized, epistemic state
2. **Phase 2 Report**: Critique report with security vulnerabilities, assumptions, overengineering
3. **Phase 3 Report**: Reflection journal entry
4. **Phase 4 Report**: Assumption validation with evidence
5. **Phase 5 Report**: Verification traces with evidence
6. **Phase 6 Report**: Options analysis with trade-offs
7. **Phase 7 Report**: Decision matrix with calculated recommendation
8. **Phase 8 Report**: Synthesis and revision plan

### Final Synthesis Document

Saved to: `_work_efforts/DEEP_THINK_ANALYSIS_YYYY-MM-DD_HHMMSS.md`

Includes:
- Executive summary
- All phase reports
- Prioritized issues
- Revision plan
- Action items
- Evidence traces
- Decision documentation

---

## Example Usage

### Basic Usage
```
/deep-think
```
Analyzes most recent plan or current context.

### With Target
```
/deep-think plan:pantheon_spiritual_architecture
/deep-think decision:framework_choice
/deep-think code:feature_implementation
```

### With Focus
```
/deep-think --focus security
/deep-think --focus assumptions
/deep-think --focus integration
```

### With Specific Plan File
```
/deep-think file:~/.cursor/plans/pantheon_spiritual_architecture_implementation_401ddf30.plan.md
```

---

## Integration

### Uses Existing Commands
- **`/think`** - Phase 1: Initialize cognitive tools
- **`/critique`** - Phase 2: Adversarial critique
- **`/reflect`** - Phase 3: Reflection
- **`/check-assumptions`** - Phase 4: Assumption validation
- **`/verify`** - Phase 5: Verification
- **`/consider`** - Phase 6: Options analysis
- **`/decide`** - Phase 7: Decision matrix

### Outputs To
- **`_work_efforts/`** - Work effort for analysis, critique reports, synthesis documents
- **`_pyrite/journal/`** - Reflection entries
- **`_pyrite/standards/verification/`** - Verification traces
- **`_work_efforts/proof_cases/`** - Proof cases (via magistrate, if applicable)
- **`.cursor/plans/`** - Revised plans

### Works With
- **Empirica**: Epistemic tracking, findings, unknowns
- **Sequential Thinking**: Hierarchical planning during analysis
- **Work Efforts**: Task tracking for action items
- **Judge/Magistrate**: Document decisions as precedents (if applicable)

---

## When to Use

**Use `/deep-think` when**:
- ✅ Need to deeply analyze a plan before implementation
- ✅ Want comprehensive cognitive review of decisions
- ✅ Need to validate assumptions and verify claims
- ✅ Want structured decision-making with full context
- ✅ Preparing for significant work requiring thorough analysis
- ✅ Need security-first review of plans
- ✅ Want evidence-based validation of beliefs
- ✅ Need quantitative decision support

**Don't use `/deep-think` when**:
- ❌ Quick decision needed (use `/consider` or `/decide` alone)
- ❌ Simple problem (use individual commands)
- ❌ Just need reflection (use `/reflect`)
- ❌ Just need verification (use `/verify`)
- ❌ Time-constrained (workflow takes significant time)

---

## Workflow Duration

**Estimated Time**: 30-60 minutes for full 8-phase workflow

- Phase 1 (Initialize): 2-5 minutes
- Phase 2 (Critique): 5-10 minutes
- Phase 3 (Reflect): 2-3 minutes
- Phase 4 (Assumptions): 5-10 minutes
- Phase 5 (Verify): 3-5 minutes
- Phase 6 (Consider): 3-5 minutes
- Phase 7 (Decide): 5-10 minutes
- Phase 8 (Synthesis): 5-10 minutes

**Can be interrupted**: Each phase produces output, so workflow can be paused and resumed.

---

## Error Handling

### Phase 1 Failures
- **Empirica Not Available**: Continue with other tools, note limitation
- **Git Not Initialized**: Attempt initialization, continue if fails
- **MCP Servers Not Available**: Continue with available tools, note limitations

### Phase 2 Failures
- **Target Not Found**: Ask user to specify target
- **Analysis Errors**: Document partial findings, continue

### Phase 4-5 Failures
- **Evidence Gathering Fails**: Document what was attempted, note limitations
- **Validation Incomplete**: Mark as "INSUFFICIENT EVIDENCE", continue

### Phase 7 Failures
- **Decision Matrix Calculation Errors**: Use qualitative analysis from Phase 6
- **Missing Data**: Document gaps, provide best-effort recommendation

---

## Best Practices

1. **Use for Significant Work**: Reserve for important plans/decisions
2. **Allow Time**: Don't rush the workflow
3. **Review All Phases**: Each phase provides valuable insights
4. **Document Everything**: Traces and evidence are valuable
5. **Act on Findings**: Use revision plan to improve target
6. **Iterate**: Can run multiple times as target evolves

---

## Related Commands

- **`/think`**: Initialize cognitive tools (Phase 1)
- **`/critique`**: Adversarial plan critique (Phase 2)
- **`/reflect`**: Journal reflection (Phase 3)
- **`/check-assumptions`**: Assumption validation (Phase 4)
- **`/verify`**: Verification with traces (Phase 5)
- **`/consider`**: Options analysis (Phase 6)
- **`/decide`**: Decision matrix (Phase 7)
- **`/proceed`**: Lightweight verification before action
- **`/checkpoint`**: Document current state

---

**This command orchestrates the full cognitive toolkit for comprehensive analysis, validation, and decision-making - perfect for deep thinking about plans, decisions, and complex problems.**

--- End Command ---