# Check Assumptions

**Identify all assumptions in the current conversation and attempt to prove them right or wrong using evidence.**

Analyzes the conversation history to extract implicit assumptions, then systematically validates each one using code analysis, file system checks, test results, Empirica epistemic state, and other available evidence sources.

**Use when:** Want to verify assumptions before proceeding, need to validate beliefs about the codebase, or want evidence-based confirmation of implicit assumptions.

---

## Purpose

This command provides:
- **Assumption Extraction**: Identifies implicit assumptions from conversation
- **Multi-Source Validation**: Uses multiple evidence sources to validate assumptions
- **Evidence-Based Conclusions**: Provides proof (or disproof) with traceable evidence
- **Risk Assessment**: Categorizes assumptions by risk level
- **Actionable Recommendations**: Suggests next steps based on validation results

---

## Philosophy

1. **Assumptions Are Everywhere**: Every statement contains implicit assumptions
2. **Evidence Over Belief**: Prove assumptions with evidence, not faith
3. **Multiple Validation Methods**: Use all available tools to validate
4. **Traceable Proof**: Every conclusion must have evidence
5. **Risk-Aware**: Critical assumptions need stronger validation
6. **Actionable**: Validation results should inform next steps

---

## Implementation

This command uses the `CheckAssumptionsManager` class from `src/waft/core/check_assumptions.py`.

**Python Implementation**: Available via `waft check-assumptions` CLI command or can be called directly by AI when executing this Cursor command.

---

## Execution Steps

### Step 1: Extract Assumptions from Conversation
**Purpose**: Identify all implicit assumptions in the current chat

**AI Action**: You (the AI) should analyze the conversation history yourself to extract assumptions. Look for:

**Actions**:
1. Analyze conversation history for assumption patterns:
   - Statements about how code works ("X assumes Y")
   - Beliefs about system state ("This should work because...")
   - Dependencies assumed ("Requires Z to be available")
   - Format expectations ("Data is in format X")
   - Behavioral assumptions ("Function returns Y")
   - Environmental assumptions ("System has X installed")
2. Extract explicit assumptions (user stated)
3. Extract implicit assumptions (inferred from context)
4. Categorize by type:
   - **Code assumptions**: About how code behaves
   - **Dependency assumptions**: About external dependencies
   - **Data assumptions**: About data formats/structures
   - **System assumptions**: About environment/configuration
   - **Behavioral assumptions**: About user/system behavior
5. Prioritize by risk (critical vs minor)

**Output**: List of assumptions with categories and risk levels

**Note**: After extracting assumptions, you can use `CheckAssumptionsManager` to validate them, or validate them yourself using the methods described in Step 2.

---

### Step 2: Gather Validation Evidence
**Purpose**: Collect evidence from multiple sources to validate assumptions

**AI Action**: Use available tools (read_file, grep, codebase_search, run_terminal_cmd) to gather evidence. You can also instantiate `CheckAssumptionsManager` and call `_gather_evidence_sources()` method.

**Actions**:
1. **Code Analysis**:
   - Search codebase for relevant code
   - Read source files mentioned
   - Check function signatures and implementations
   - Verify data structures and types
   - Check error handling
2. **File System Checks**:
   - Verify files exist
   - Check file contents
   - Verify directory structure
   - Check file permissions
3. **Test Results**:
   - Run relevant tests
   - Check test coverage
   - Review test results
   - Verify test assumptions
4. **Git History**:
   - Check recent commits
   - Review changes
   - Verify assumptions about history
5. **Empirica/Oracle** (if available):
   - Check epistemic state
   - Review logged findings
   - Check unknowns
   - Get Oracle guidance
6. **Scientific Method Tool** (if applicable):
   - Form hypothesis from assumption
   - Design test
   - Run experiment
   - Analyze results
7. **Documentation**:
   - Check README files
   - Review docs
   - Verify documented behavior
8. **External Dependencies**:
   - Check if tools/commands exist
   - Verify versions
   - Test availability

**Output**: Evidence collected from all sources

---

### Step 3: Validate Each Assumption
**Purpose**: Prove or disprove each assumption with evidence

**Actions**:
For each assumption:
1. **Match Evidence**: Find relevant evidence from Step 2
2. **Evaluate Evidence**:
   - **PROVEN**: Strong evidence supports assumption
   - **DISPROVEN**: Strong evidence contradicts assumption
   - **PARTIALLY PROVEN**: Some evidence supports, some contradicts
   - **INSUFFICIENT EVIDENCE**: Not enough evidence to determine
   - **NEEDS TESTING**: Requires experiment to validate
3. **Confidence Level**: Assign confidence (0.0-1.0)
4. **Evidence Summary**: List specific evidence points
5. **Risk Assessment**: Update risk based on validation

**Output**: Validation results for each assumption

---

### Step 4: Generate Validation Report
**Purpose**: Present findings with evidence and recommendations

**Actions**:
1. **Summary Table**: All assumptions with validation status
2. **Detailed Results**: For each assumption:
   - Assumption statement
   - Category and risk level
   - Validation status
   - Confidence level
   - Evidence summary
   - Specific evidence points
3. **Critical Findings**: Highlight critical assumptions
4. **Recommendations**: Next steps based on validation
5. **Evidence Traces**: Links to specific evidence sources

**Output**: Comprehensive validation report

---

### Step 5: Log Findings (Optional)
**Purpose**: Record validated assumptions for future reference

**Actions**:
1. If Empirica available:
   - Log proven assumptions as findings
   - Log disproven assumptions as findings
   - Log unknowns for assumptions needing testing
2. Update documentation if needed
3. Create assumption tracking file if desired

**Output**: Findings logged for future reference

---

## Assumption Categories

### Code Assumptions
- How functions/classes behave
- Return types and values
- Error handling behavior
- Side effects
- Performance characteristics

### Dependency Assumptions
- External tools available
- Library versions
- System dependencies
- Configuration requirements
- Network access

### Data Assumptions
- Data formats
- Data structures
- Data encoding
- Data size/limits
- Data validation

### System Assumptions
- Environment variables
- File system state
- Permissions
- Network connectivity
- Resource availability

### Behavioral Assumptions
- User behavior
- System behavior
- API behavior
- Integration behavior
- Workflow behavior

---

## Validation Methods

### 1. Code Analysis
- **Grep**: Search for patterns
- **Read Files**: Examine source code
- **Type Checking**: Verify types
- **Static Analysis**: Check code structure

### 2. File System Checks
- **File Existence**: `Path.exists()`
- **File Contents**: Read and analyze
- **Directory Structure**: Verify layout
- **Permissions**: Check access

### 3. Test Execution
- **Run Tests**: Execute relevant tests
- **Check Coverage**: Verify test coverage
- **Review Results**: Analyze test outcomes

### 4. Git Analysis
- **Recent Commits**: Check history
- **File Changes**: Review diffs
- **Branch State**: Verify branch

### 5. Empirica/Oracle
- **Epistemic State**: Check knowledge state
- **Findings**: Review logged findings
- **Unknowns**: Check knowledge gaps
- **Guidance**: Get Oracle recommendations

### 6. Scientific Method
- **Hypothesis**: Form testable hypothesis
- **Experiment**: Design and run test
- **Analysis**: Verify or refute

### 7. Documentation Review
- **README**: Check project docs
- **Code Comments**: Review inline docs
- **API Docs**: Check external docs

### 8. Runtime Checks
- **Command Availability**: Test if commands exist
- **Version Checks**: Verify versions
- **Connectivity**: Test network access

---

## Output Format

### Summary
```
🔍 Assumption Validation Report

Total Assumptions: 8
✅ Proven: 3
❌ Disproven: 1
⚠️ Partially Proven: 2
❓ Insufficient Evidence: 1
🧪 Needs Testing: 1

Critical Assumptions: 2
  ✅ 1 proven
  ❌ 1 disproven
```

### Detailed Results
```
Assumption 1: "The `uv` command is available"
Category: Dependency
Risk: Critical
Status: ✅ PROVEN
Confidence: 1.0

Evidence:
  ✅ Command exists: `which uv` returns /usr/local/bin/uv
  ✅ Version check: uv 0.6.3 installed
  ✅ Test execution: `uv --version` succeeds
  ✅ Code usage: SubstrateManager uses `uv` successfully

Recommendation: Assumption is valid, proceed with confidence.
```

### Critical Findings
```
⚠️ CRITICAL ASSUMPTION DISPROVEN

Assumption: "TOML parsing handles escaped quotes correctly"
Status: ❌ DISPROVEN
Confidence: 0.9

Evidence:
  ❌ Test case failed: Escaped quotes not handled
  ❌ Code analysis: Regex pattern doesn't match `\"`
  ✅ Documentation: Limitation documented in ASSUMPTIONS_AND_TESTS.md

Impact: HIGH - Could cause parsing failures
Recommendation: Use proper TOML parser (tomllib/tomli) or document limitation
```

### Recommendations
```
📋 Next Steps

1. HIGH PRIORITY: Fix TOML parsing for escaped quotes
   - Use tomllib (Python 3.11+) or tomli
   - Update SubstrateManager.parse_toml_field()

2. MEDIUM PRIORITY: Test assumption about file permissions
   - Run experiment with read-only filesystem
   - Document behavior

3. LOW PRIORITY: Document proven assumptions
   - Add to ASSUMPTIONS_AND_TESTS.md
   - Update README if needed
```

---

## Usage Examples

### Basic Usage
```
/check-assumptions
```
Validates all assumptions found in current conversation.

### Focus on Specific Area
```
/check-assumptions --focus code
/check-assumptions --focus dependencies
/check-assumptions --focus data
```
Validates assumptions in specific category.

### Critical Only
```
/check-assumptions --critical
```
Only validates critical assumptions.

### With Testing
```
/check-assumptions --test
```
Runs experiments for assumptions that need testing.

### Detailed Evidence
```
/check-assumptions --verbose
```
Shows detailed evidence traces for each assumption.

---

## Integration

- **`/proceed`**: Verifies assumptions before proceeding (check-assumptions is more comprehensive)
- **`/verify`**: Post-action verification (check-assumptions is pre/post validation)
- **`/oracle`**: Uses epistemic state for validation (check-assumptions uses Oracle + more)
- **`/critique`**: Finds unexamined assumptions (check-assumptions validates them)
- **`/hypothesis`**: Forms testable hypotheses (check-assumptions can use this)

---

## When to Use

**Use `/check-assumptions` when**:
- ✅ About to make significant changes
- ✅ Need to verify beliefs about codebase
- ✅ Want evidence-based validation
- ✅ Need to prove/disprove assumptions
- ✅ Want comprehensive assumption audit
- ✅ Preparing for risky operations
- ✅ Debugging unexpected behavior

**Don't use `/check-assumptions` when**:
- ❌ Need quick context check (use `/proceed`)
- ❌ Need pure reflection (use `/reflect`)
- ❌ Need status snapshot (use `/checkpoint`)
- ❌ Already validated everything (just proceed)

---

## Validation Confidence Levels

- **1.0 (PROVEN)**: Strong evidence, no contradictions
- **0.8-0.9 (LIKELY)**: Strong evidence, minor contradictions
- **0.6-0.7 (PROBABLE)**: Moderate evidence, some support
- **0.4-0.5 (UNCERTAIN)**: Mixed evidence, unclear
- **0.2-0.3 (UNLIKELY)**: Weak evidence, mostly contradicts
- **0.0-0.1 (DISPROVEN)**: Strong evidence contradicts

---

**This command systematically identifies and validates assumptions using evidence from multiple sources, providing proof (or disproof) with traceable evidence.**
