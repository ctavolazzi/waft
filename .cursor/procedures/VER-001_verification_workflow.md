# Procedure: Verification Workflow

**Shortcode**: VER-001  
**Category**: Verification  
**Created**: 2026-01-10  
**Updated**: 2026-01-10  
**Status**: Active  
**Aliases**: `/verify-workflow`

---

## Description

Comprehensive verification workflow that runs diagnostic verification checks, creates traceable evidence, and documents findings incrementally.

---

## Use When

- Need to verify claims or assumptions
- Want to validate information
- Need traceable evidence
- Want to check project state
- Need diagnostic verification

---

## Prerequisites

- Project is a git repository
- Working directory is project root
- Claims or assumptions to verify

---

## Steps

### Step 1: Identify Claims
**Actions**:
1. Review conversation for verifiable claims
2. List assumptions made
3. Identify information to verify
4. Prioritize verification checks

**Output**: List of claims to verify

---

### Step 2: Run Verification Checks
**Execute**: `/verify`

**Checks**:
1. Environment verification (date, disk, directory)
2. Project state verification (structure, git, version)
3. Tool availability verification (CLI tools, MCP servers, versions)
4. File/directory verification (existence, content)
5. Configuration verification (config values, env vars)
6. Dependency verification (installed, versions)
7. Work effort verification (active, details)
8. GitHub state verification (repo, commits, issues/PRs)

**Output**: Verification traces for each check

---

### Step 3: Document Traces
**Actions**:
1. Create trace documents
2. Document evidence
3. Update verification index
4. Link related traces

**Output**: Verification traces in `_pyrite/standards/verification/traces/`

---

### Step 4: Review Results
**Actions**:
1. Review verification results
2. Identify verified vs. unverified claims
3. Note discrepancies
4. Plan follow-up verifications

**Output**: Understanding of verification status

---

## Expected Output

After completion:
- ✅ All claims verified or documented as unverified
- ✅ Verification traces created
- ✅ Evidence documented
- ✅ Verification index updated
- ✅ Results reviewed

---

## Notes

- Verification is lightweight and non-exhaustive
- Traces are incrementally updated
- Focus on what matters, not everything
- Document evidence clearly

---

## Related Procedures

- **ORC-001**: Comprehensive Orchestration (includes verification)
- **ANL-001**: Data Analysis Workflow (may use verification)

---

**Procedure Created**: 2026-01-10  
**Last Updated**: 2026-01-10
