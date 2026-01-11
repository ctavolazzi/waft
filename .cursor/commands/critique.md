# /critique - Adversarial Plan Critique

**Critique plans in bad faith, assuming the worst - security flaws first, then unexamined assumptions, overengineering, oversight, and missed obviousness.**

Performs a hostile, adversarial review of implementation plans, assuming malicious intent, worst-case scenarios, and looking for all the ways things could catastrophically fail. Safety and security are the absolute priority.

**Use when:** Need a brutally honest, worst-case-scenario critique of a plan before implementation. Want to find security holes, unexamined assumptions, overengineering, and obvious oversights that could cause problems.

---

## Purpose

This command provides:
- **Security-First Analysis**: Find security vulnerabilities, attack vectors, and safety issues
- **Adversarial Review**: Assume worst-case scenarios and malicious intent
- **Assumption Detection**: Identify unexamined assumptions that could break everything
- **Overengineering Detection**: Find unnecessary complexity that adds risk
- **Oversight Detection**: Catch obvious things that were missed
- **Missed Obviousness**: Find things that should be obvious but weren't considered

---

## Philosophy

1. **Safety First**: Security and safety flaws are the absolute top priority
2. **Assume the Worst**: Assume malicious actors, worst-case scenarios, and catastrophic failures
3. **Bad Faith**: Look for problems, not solutions - find all the ways it could fail
4. **Adversarial**: Think like an attacker trying to break the system
5. **Brutal Honesty**: No sugar-coating - call out problems directly
6. **Miss Nothing**: If it's obvious, it should have been obvious - catch obvious oversights

---

## Execution Steps

### Step 1: Locate Plan

**Purpose**: Find the plan to critique

**Actions**:
1. Check if plan path provided as argument (e.g., `/critique plan:tech_debt_sentinel`)
2. Check for most recent plan in `~/.cursor/plans/` or `.cursor/plans/`
3. Check if plan content provided directly
4. If no plan found, ask user to specify

**Output**: Plan content loaded

---

### Step 2: Security-First Analysis (CRITICAL)

**Purpose**: Find security vulnerabilities and safety issues - THIS IS THE TOP PRIORITY

**Actions**:
1. **File System Security**:
   - Can the scanner read sensitive files? (`.env`, `secrets/`, `*.key`, `*.pem`)
   - Does it traverse symlinks? (symlink attacks)
   - Can it access files outside project directory? (path traversal)
   - Does it handle file permissions correctly?
   - Can it read git history? (secrets in history)

2. **Code Execution Security**:
   - Does it execute arbitrary code? (subprocess calls, eval, exec)
   - Can user input be injected into commands? (command injection)
   - Are external commands sanitized? (shell injection)
   - Does it use `subprocess.run(shell=True)`? (CRITICAL VULNERABILITY)

3. **Data Security**:
   - Does it store sensitive data? (API keys, tokens, passwords)
   - Are genome IDs deterministic? (can they leak information?)
   - Does it log sensitive information? (PII, secrets)
   - Are registry files world-readable? (information disclosure)

4. **Network Security**:
   - Does it make network requests? (SSRF vulnerabilities)
   - Are URLs validated? (malicious URLs)
   - Does it trust external data? (supply chain attacks)

5. **Dependency Security**:
   - Are dependencies pinned? (supply chain attacks)
   - Are vulnerable packages used? (known CVEs)
   - Does it add new dependencies? (attack surface increase)

6. **Access Control**:
   - Who can run the scanner? (privilege escalation)
   - Does it require elevated permissions? (unnecessary risk)
   - Can it modify files it shouldn't? (unauthorized writes)

7. **Input Validation**:
   - Are file paths validated? (path traversal)
   - Are user inputs sanitized? (injection attacks)
   - Are regex patterns safe? (ReDoS attacks)

**Output**: List of security vulnerabilities with severity (CRITICAL, HIGH, MEDIUM, LOW)

---

### Step 3: Unexamined Assumptions Analysis

**Purpose**: Find assumptions that could break everything if wrong

**Actions**:
1. **File System Assumptions**:
   - Assumes filesystem is writable? (read-only filesystems)
   - Assumes specific directory structure? (portability issues)
   - Assumes file encoding? (encoding errors)
   - Assumes file permissions? (permission denied)

2. **Dependency Assumptions**:
   - Assumes dependencies are installed? (missing deps)
   - Assumes specific versions? (version conflicts)
   - Assumes external tools exist? (missing binaries)
   - Assumes network access? (air-gapped systems)

3. **Environment Assumptions**:
   - Assumes Python version? (version compatibility)
   - Assumes OS type? (cross-platform issues)
   - Assumes locale settings? (encoding issues)
   - Assumes timezone? (timestamp issues)

4. **Data Assumptions**:
   - Assumes data format? (malformed data)
   - Assumes data size? (memory issues)
   - Assumes data encoding? (encoding errors)
   - Assumes data structure? (schema violations)

5. **Behavior Assumptions**:
   - Assumes functions return expected types? (type errors)
   - Assumes functions don't throw? (unhandled exceptions)
   - Assumes operations are atomic? (race conditions)
   - Assumes operations are idempotent? (side effects)

6. **User Assumptions**:
   - Assumes user has permissions? (access denied)
   - Assumes user understands output? (confusion)
   - Assumes user wants automation? (unwanted actions)

**Output**: List of unexamined assumptions with potential impact

---

### Step 4: Overengineering Detection

**Purpose**: Find unnecessary complexity that adds risk

**Actions**:
1. **Architecture Overengineering**:
   - Too many layers? (unnecessary abstraction)
   - Too many components? (coordination complexity)
   - Premature optimization? (YAGNI violations)
   - Over-abstraction? (indirection hell)

2. **Pattern Overengineering**:
   - Using patterns unnecessarily? (pattern abuse)
   - Too many design patterns? (pattern soup)
   - Over-engineered inheritance? (complex hierarchies)
   - Unnecessary frameworks? (dependency bloat)

3. **Data Overengineering**:
   - Over-complex data structures? (unnecessary complexity)
   - Over-normalized data? (query complexity)
   - Unnecessary serialization? (performance cost)
   - Over-engineered schemas? (maintenance burden)

4. **Process Overengineering**:
   - Too many steps? (friction)
   - Unnecessary validation? (over-validation)
   - Over-engineered workflows? (complexity)
   - Unnecessary automation? (automation for automation's sake)

**Output**: List of overengineering issues with complexity cost

---

### Step 5: Oversight Detection

**Purpose**: Catch obvious things that were missed

**Actions**:
1. **Error Handling Oversights**:
   - Missing try/except blocks? (unhandled exceptions)
   - Missing validation? (invalid input handling)
   - Missing null checks? (NoneType errors)
   - Missing edge case handling? (boundary conditions)

2. **Resource Management Oversights**:
   - Missing file closing? (resource leaks)
   - Missing cleanup? (temporary files)
   - Missing connection closing? (connection leaks)
   - Missing memory management? (memory leaks)

3. **Testing Oversights**:
   - No tests mentioned? (untested code)
   - Missing test cases? (incomplete coverage)
   - No integration tests? (integration issues)
   - No security tests? (security blind spots)

4. **Documentation Oversights**:
   - Missing README? (usage unclear)
   - Missing API docs? (integration unclear)
   - Missing examples? (usage unclear)
   - Missing error docs? (troubleshooting unclear)

5. **Deployment Oversights**:
   - Missing deployment steps? (deployment unclear)
   - Missing configuration? (config unclear)
   - Missing migration steps? (migration unclear)
   - Missing rollback plan? (recovery unclear)

6. **Performance Oversights**:
   - No performance considerations? (slow code)
   - No scalability considerations? (doesn't scale)
   - No memory considerations? (memory issues)
   - No concurrency considerations? (race conditions)

**Output**: List of oversights with impact

---

### Step 6: Missed Obviousness Detection

**Purpose**: Find things that should be obvious but weren't considered

**Actions**:
1. **Obvious Security Issues**:
   - Hardcoded secrets? (obvious security flaw)
   - Debug code in production? (obvious vulnerability)
   - Exposed admin endpoints? (obvious attack vector)
   - No authentication? (obvious access control issue)

2. **Obvious Functionality Issues**:
   - Missing main function? (obvious entry point issue)
   - No error messages? (obvious UX issue)
   - No logging? (obvious debugging issue)
   - No configuration? (obvious flexibility issue)

3. **Obvious Design Issues**:
   - Circular dependencies? (obvious architecture issue)
   - Tight coupling? (obvious maintainability issue)
   - No separation of concerns? (obvious design issue)
   - God objects? (obvious design smell)

4. **Obvious Process Issues**:
   - No version control? (obvious process issue)
   - No code review? (obvious quality issue)
   - No CI/CD? (obvious automation issue)
   - No monitoring? (obvious observability issue)

**Output**: List of missed obviousness issues

---

### Step 7: Additional Adversarial Analysis

**Purpose**: Find additional ways things could fail

**Actions**:
1. **Failure Modes**:
   - What happens if disk is full? (disk space)
   - What happens if network is down? (network dependency)
   - What happens if process is killed? (cleanup)
   - What happens if system is under load? (performance)

2. **Attack Vectors**:
   - Can attacker control input? (input validation)
   - Can attacker control output? (output encoding)
   - Can attacker control timing? (race conditions)
   - Can attacker control resources? (DoS attacks)

3. **Edge Cases**:
   - Empty inputs? (empty handling)
   - Extremely large inputs? (size limits)
   - Malformed inputs? (parsing errors)
   - Concurrent access? (race conditions)

4. **Integration Issues**:
   - Breaking changes? (compatibility)
   - Version conflicts? (dependency hell)
   - API changes? (integration breaks)
   - Data migration? (data loss)

**Output**: Additional adversarial findings

---

### Step 8: Generate Critique Report

**Purpose**: Create comprehensive critique report

**Actions**:
1. Generate markdown document with sections:
   - **Executive Summary**: Overall critique assessment
   - **CRITICAL: Security Vulnerabilities**: Security flaws (TOP PRIORITY)
   - **HIGH: Safety Issues**: Safety concerns
   - **MEDIUM: Unexamined Assumptions**: Assumptions that could break things
   - **LOW: Overengineering**: Unnecessary complexity
   - **Oversights**: Obvious things that were missed
   - **Missed Obviousness**: Things that should be obvious
   - **Additional Adversarial Findings**: Other ways things could fail
   - **Recommendations**: What needs to be fixed (prioritized by severity)

2. Save to `_work_efforts/` directory
3. Use timestamped filename: `CRITIQUE_YYYY-MM-DD_HHMMSS.md`

**Output**: Complete critique report

---

### Step 9: Display Summary

**Purpose**: Show critique summary in console

**Actions**:
1. Display security vulnerabilities (CRITICAL first)
2. Show assumption count and impact
3. Highlight overengineering issues
4. List oversights
5. Show missed obviousness
6. Provide file location

**Output**: Console summary

---

## What Gets Critiqued

### Security Vulnerabilities (TOP PRIORITY)
- File system access issues
- Code execution vulnerabilities
- Data security problems
- Network security issues
- Dependency vulnerabilities
- Access control problems
- Input validation issues

### Unexamined Assumptions
- File system assumptions
- Dependency assumptions
- Environment assumptions
- Data assumptions
- Behavior assumptions
- User assumptions

### Overengineering
- Architecture complexity
- Pattern abuse
- Data overengineering
- Process overengineering

### Oversights
- Error handling gaps
- Resource management issues
- Testing gaps
- Documentation gaps
- Deployment issues
- Performance considerations

### Missed Obviousness
- Obvious security issues
- Obvious functionality issues
- Obvious design issues
- Obvious process issues

---

## Output Format

### Console Output

```
🔴 CRITIQUE: Adversarial Plan Analysis

⚠️  CRITICAL SECURITY VULNERABILITIES: 3
   - Scanner can read .env files (CRITICAL)
   - subprocess.run(shell=True) allows command injection (CRITICAL)
   - Registry files world-readable (CRITICAL)

🔴 HIGH SAFETY ISSUES: 2
   - No input validation on file paths
   - No error handling for missing dependencies

⚠️  UNEXAMINED ASSUMPTIONS: 8
   - Assumes filesystem is writable
   - Assumes Python 3.10+ available
   - Assumes mccabe library installed
   - ...

⚠️  OVERENGINEERING: 4
   - Unnecessary abstraction layers
   - Over-complex genome system for simple debt tracking
   - ...

⚠️  OVERSIGHTS: 6
   - No error handling for file I/O
   - No tests mentioned
   - Missing cleanup for temporary files
   - ...

⚠️  MISSED OBVIOUSNESS: 3
   - No authentication/authorization
   - No rate limiting
   - No input size limits

📄 Critique saved: _work_efforts/CRITIQUE_2026-01-11_144500.md
```

### Critique Report

The document includes:

```markdown
# Adversarial Plan Critique

**Date**: 2026-01-11
**Time**: 14:45:00
**Plan**: Tech Debt Sentinel Implementation
**Critique Mode**: Bad Faith / Adversarial

---

## Executive Summary

**CRITICAL Security Vulnerabilities**: 3
**HIGH Safety Issues**: 2
**MEDIUM Unexamined Assumptions**: 8
**LOW Overengineering**: 4
**Oversights**: 6
**Missed Obviousness**: 3

**Overall Assessment**: This plan has CRITICAL security vulnerabilities that must be addressed before any implementation. Multiple unexamined assumptions could cause catastrophic failures. Significant overengineering adds unnecessary risk.

---

## 🔴 CRITICAL: Security Vulnerabilities

### 1. Scanner Can Read Sensitive Files (CRITICAL)
**Issue**: The scanner crawls `src/` directory but doesn't exclude sensitive files.
**Attack Vector**: Scanner could read `.env`, `secrets/`, `*.key`, `*.pem` files
**Impact**: Secrets could be exposed in debt reports or logged
**Severity**: CRITICAL
**Fix Required**: 
- Add explicit exclusion list for sensitive file patterns
- Validate file paths before reading
- Never scan files outside project root
- Sanitize file paths in output

### 2. Command Injection via subprocess.run(shell=True) (CRITICAL)
**Issue**: Using `ruff check --select F401` via subprocess without proper sanitization
**Attack Vector**: If file paths contain shell metacharacters, command injection possible
**Impact**: Arbitrary code execution
**Severity**: CRITICAL
**Fix Required**:
- Never use `shell=True`
- Use `subprocess.run([...], shell=False)` with list of arguments
- Validate and sanitize all inputs to subprocess calls
- Use `shlex.quote()` if shell is absolutely necessary

### 3. Registry Files World-Readable (CRITICAL)
**Issue**: Genome registry stored in `_genetics/tech_debt/` with default permissions
**Attack Vector**: Other users/processes could read debt genome data
**Impact**: Information disclosure, potential data leakage
**Severity**: CRITICAL
**Fix Required**:
- Set restrictive file permissions (0600 for files, 0700 for directories)
- Validate registry location is within project
- Never store sensitive data in registry
- Add access control checks

---

## 🔴 HIGH: Safety Issues

### 1. No Input Validation on File Paths
**Issue**: File paths from scanner not validated before use
**Impact**: Path traversal attacks, reading files outside project
**Severity**: HIGH
**Fix Required**: Validate all file paths, reject paths with `..`, absolute paths outside project

### 2. No Error Handling for Missing Dependencies
**Issue**: Assumes `mccabe` and other dependencies are installed
**Impact**: Runtime crashes, poor user experience
**Severity**: HIGH
**Fix Required**: Check for dependencies, provide clear error messages, graceful degradation

---

## ⚠️ MEDIUM: Unexamined Assumptions

### 1. Assumes Filesystem is Writable
**Issue**: Registry writes assume filesystem is writable
**Impact**: Crashes on read-only filesystems (containers, CI/CD)
**Severity**: MEDIUM
**Fix Required**: Check filesystem permissions, provide read-only mode

### 2. Assumes Python 3.10+ Available
**Issue**: Uses Python 3.10+ features without version check
**Impact**: Crashes on older Python versions
**Severity**: MEDIUM
**Fix Required**: Check Python version, provide clear error messages

### 3. Assumes mccabe Library Installed
**Issue**: Uses mccabe for complexity analysis without checking
**Impact**: Runtime errors if not installed
**Severity**: MEDIUM
**Fix Required**: Check for library, provide fallback or clear error

[... more assumptions ...]

---

## ⚠️ LOW: Overengineering

### 1. Unnecessary Genome System for Simple Debt Tracking
**Issue**: Full genetic system (genome IDs, scientific names, lineage) for simple debt items
**Impact**: Unnecessary complexity, maintenance burden, potential bugs
**Severity**: LOW
**Fix Consideration**: Could use simpler data structure (dict/list) for debt items

### 2. Over-Complex Abstraction Layers
**Issue**: Too many layers (Scanner → Distiller → Engine → Reporter)
**Impact**: Harder to debug, more coordination complexity
**Severity**: LOW
**Fix Consideration**: Could combine some layers for simplicity

[... more overengineering ...]

---

## ⚠️ Oversights

### 1. No Error Handling for File I/O
**Issue**: File operations don't handle IOError, PermissionError
**Impact**: Crashes on file system errors
**Severity**: MEDIUM
**Fix Required**: Add try/except blocks, handle all file I/O errors

### 2. No Tests Mentioned
**Issue**: Plan doesn't mention testing strategy
**Impact**: Untested code, potential bugs
**Severity**: MEDIUM
**Fix Required**: Add unit tests, integration tests, security tests

### 3. Missing Cleanup for Temporary Files
**Issue**: No cleanup mentioned for temporary files created during scanning
**Impact**: Disk space leaks, temporary file accumulation
**Severity**: LOW
**Fix Required**: Add cleanup, use context managers

[... more oversights ...]

---

## ⚠️ Missed Obviousness

### 1. No Authentication/Authorization
**Issue**: No mention of who can run scanner, what they can scan
**Impact**: Unauthorized access, information disclosure
**Severity**: MEDIUM
**Fix Required**: Add access control, validate user permissions

### 2. No Rate Limiting
**Issue**: Scanner could be run repeatedly, causing resource exhaustion
**Impact**: DoS attacks, resource exhaustion
**Severity**: LOW
**Fix Consideration**: Add rate limiting, resource limits

### 3. No Input Size Limits
**Issue**: No limits on file sizes or number of files scanned
**Impact**: Memory exhaustion, DoS attacks
**Severity**: MEDIUM
**Fix Required**: Add size limits, streaming for large files

---

## Additional Adversarial Findings

### Failure Modes
- **Disk Full**: What happens if disk fills up during registry write? (No handling)
- **Network Down**: What if external dependencies unavailable? (No fallback)
- **Process Killed**: What if process killed mid-scan? (No cleanup)
- **System Under Load**: What if system is under heavy load? (No throttling)

### Attack Vectors
- **Path Traversal**: File paths with `../` could escape project directory
- **Command Injection**: Unsanitized subprocess calls
- **Resource Exhaustion**: No limits on scan size or duration
- **Information Disclosure**: Sensitive data in reports or logs

### Edge Cases
- **Empty Codebase**: What if `src/` is empty? (No handling)
- **Symlinks**: What if symlinks point outside project? (No validation)
- **Concurrent Scans**: What if multiple scans run simultaneously? (Race conditions)
- **Malformed Files**: What if Python files are malformed? (Parser errors)

---

## Recommendations (Prioritized)

### Priority 1: CRITICAL - Fix Immediately
1. **Add File Exclusion List**: Exclude `.env`, `secrets/`, `*.key`, `*.pem` from scanning
2. **Fix subprocess Calls**: Remove `shell=True`, use list arguments, validate inputs
3. **Set File Permissions**: Set restrictive permissions on registry files (0600/0700)
4. **Add Path Validation**: Validate all file paths, reject traversal attempts

### Priority 2: HIGH - Fix Before Implementation
5. **Add Input Validation**: Validate all inputs, sanitize file paths
6. **Add Dependency Checks**: Check for required dependencies, provide clear errors
7. **Add Error Handling**: Handle all file I/O errors, network errors, etc.

### Priority 3: MEDIUM - Fix During Implementation
8. **Add Tests**: Unit tests, integration tests, security tests
9. **Add Documentation**: README, API docs, examples, error handling docs
10. **Add Access Control**: Validate user permissions, add authentication if needed

### Priority 4: LOW - Consider for Future
11. **Simplify Architecture**: Consider if genome system is necessary
12. **Add Rate Limiting**: Prevent resource exhaustion
13. **Add Monitoring**: Logging, metrics, observability

---

## Conclusion

This plan has **CRITICAL security vulnerabilities** that must be addressed before any code is written. The scanner can read sensitive files, subprocess calls are vulnerable to command injection, and registry files are world-readable. These are not minor issues - they are **show-stoppers**.

Additionally, there are multiple unexamined assumptions that could cause catastrophic failures, significant overengineering that adds unnecessary risk, and obvious oversights that should have been caught.

**Recommendation**: Do not proceed with implementation until all CRITICAL and HIGH priority issues are addressed. The security vulnerabilities alone make this plan unsafe to implement as-is.

---

**This critique assumes the worst and looks for all the ways things could fail. Address these issues before implementation.**
```

---

## Usage Examples

### Critique Most Recent Plan
```
/critique
```

### Critique Specific Plan
```
/critique plan:tech_debt_sentinel
/critique file:~/.cursor/plans/tech_debt_sentinel_implementation_b6b514e8.plan.md
```

### Critique Plan Content Directly
```
/critique content:"[plan markdown content]"
```

---

## Integration with Other Commands

- **`/audit`**: Conversation quality (`/critique` is plan security/design analysis)
- **`/verify`**: Technical verification (`/critique` is adversarial security review)
- **`/consider`**: Decision support (`/critique` is hostile plan review)

---

## When to Use

**Use `/critique` when**:
- ✅ Have an implementation plan and want security review
- ✅ Need adversarial analysis before coding
- ✅ Want to find all the ways things could fail
- ✅ Need worst-case-scenario analysis
- ✅ Want brutal honesty about plan flaws
- ✅ Need security-first review

**Don't use `/critique` when**:
- ❌ Need constructive feedback (use `/audit`)
- ❌ Need technical verification (use `/verify`)
- ❌ Need decision support (use `/consider`)
- ❌ Want positive reinforcement (this is not that command)

---

## Technical Details

### Data Sources

Critique analyzes:
- Plan document content
- Implementation details
- Architecture decisions
- Security considerations
- Dependencies and integrations
- Error handling approach
- Testing strategy

### Output Location

- **Default**: `_work_efforts/CRITIQUE_YYYY-MM-DD_HHMMSS.md`
- **Custom**: Can specify output path if needed

### Format

- **Markdown**: Easy to read and edit
- **Structured**: Clear sections prioritized by severity
- **Timestamped**: Unique filename per critique
- **Actionable**: Prioritized recommendations with fixes

---

## Example Workflow

```
User: [Creates implementation plan]
User: "/critique plan:tech_debt_sentinel"

AI: [Analyzes plan adversarially]
AI: [Finds security vulnerabilities]
AI: [Identifies assumptions]
AI: [Detects overengineering]
AI: [Finds oversights]
AI: [Generates critique report]

AI: 🔴 CRITIQUE Complete
    ⚠️  CRITICAL: 3 security vulnerabilities found
    🔴 HIGH: 2 safety issues
    ⚠️  MEDIUM: 8 unexamined assumptions
    📄 Saved: _work_efforts/CRITIQUE_2026-01-11_144500.md

User: [Reviews critique]
User: [Fixes CRITICAL issues]
User: [Proceeds with implementation]
```

---

**This command provides adversarial, security-first critique of plans - perfect for finding vulnerabilities, assumptions, and oversights before implementation.**

---

End Command ---
