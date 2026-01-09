# Verify

**Lightweight diagnostic verification with traceable evidence.**

Runs through a reasonable set of troubleshooting and diagnostic steps to verify that information in the chat is correct. Each verifiable item is "traced" with documentation that can be referenced and incrementally updated as we learn new things.

**Use when:** You need to verify claims, check assumptions, or validate information before proceeding.

---

## Purpose

This command provides:
- **Verification** of individually verifiable information items
- **Traceable evidence** for each verification
- **Incremental documentation** that grows with feedback
- **Lightweight design** - non-exhaustive, evolves over time
- **Scientific approach** - document findings, recontextualize as needed

---

## Philosophy

1. **Verify, Don't Assume**: Check claims against reality
2. **Trace Everything**: Document evidence for each check
3. **Incremental Learning**: Build knowledge over time
4. **Lightweight**: Focus on what matters, not everything
5. **Evolve**: Add/remove checks based on feedback

---

## Verification Checks

### 1. Environment Verification

**Check**: Date and time accuracy
- **Method**: Run `date` command
- **Expected**: Current date/time matches system
- **Trace**: Document actual date/time, timezone
- **Evidence**: Command output

**Check**: Disk space availability
- **Method**: Run `df -h . | tail -1`
- **Expected**: Sufficient space for operations
- **Trace**: Document available space, usage percentage
- **Evidence**: Command output

**Check**: Working directory
- **Method**: Run `pwd`
- **Expected**: Correct project directory
- **Trace**: Document actual path vs expected
- **Evidence**: Command output

---

### 2. Project State Verification

**Check**: Project structure validity
- **Method**: Run `waft verify` (if waft project)
- **Expected**: Structure is valid
- **Trace**: Document integrity percentage, missing components
- **Evidence**: Command output

**Check**: Git repository state
- **Method**: Run `git status`
- **Expected**: Repository exists and is accessible
- **Trace**: Document branch, uncommitted changes count, commits ahead/behind
- **Evidence**: Command output

**Check**: Project version
- **Method**: Read `pyproject.toml` or `package.json` or equivalent
- **Expected**: Version matches claims
- **Trace**: Document actual version vs claimed version
- **Evidence**: File content

---

### 3. Tool Availability Verification

**Check**: Required CLI tools available
- **Method**: Run `which <tool>` or `command -v <tool>`
- **Expected**: Tools are in PATH
- **Trace**: Document tool paths, versions
- **Evidence**: Command output

**Check**: MCP servers operational
- **Method**: Test MCP server availability (if applicable)
- **Expected**: Servers respond
- **Trace**: Document server status, errors
- **Evidence**: MCP responses or errors

**Check**: Python/Node/etc. versions
- **Method**: Run `python --version`, `node --version`, etc.
- **Expected**: Versions match requirements
- **Trace**: Document actual versions vs required
- **Evidence**: Command output

---

### 4. File/Directory Verification

**Check**: Claimed files exist
- **Method**: Run `test -f <path>` or `Path(path).exists()`
- **Expected**: Files exist at claimed locations
- **Trace**: Document file existence, size, modification time
- **Evidence**: File metadata

**Check**: Claimed directories exist
- **Method**: Run `test -d <path>` or `Path(path).is_dir()`
- **Expected**: Directories exist
- **Trace**: Document directory existence, contents count
- **Evidence**: Directory listing

**Check**: File content matches claims
- **Method**: Read file and verify specific claims
- **Expected**: Content matches what was claimed
- **Trace**: Document actual content vs claimed
- **Evidence**: File content excerpts

---

### 5. Configuration Verification

**Check**: Configuration values
- **Method**: Read config files (pyproject.toml, package.json, .env, etc.)
- **Expected**: Values match claims
- **Trace**: Document actual values vs claimed
- **Evidence**: Config file content

**Check**: Environment variables
- **Method**: Check `os.getenv()` or `process.env`
- **Expected**: Variables set as claimed
- **Trace**: Document actual values (masked if sensitive)
- **Evidence**: Environment dump (sanitized)

---

### 6. Dependency Verification

**Check**: Dependencies installed
- **Method**: Check lock files, package lists, or import tests
- **Expected**: Dependencies match claims
- **Trace**: Document installed packages vs required
- **Evidence**: Dependency list

**Check**: Dependency versions
- **Method**: Check version pins in lock files
- **Expected**: Versions match claims
- **Trace**: Document actual versions vs claimed
- **Evidence**: Version information

---

### 7. Work Effort Verification

**Check**: Active work efforts
- **Method**: Call `mcp_work-efforts_list_work_efforts` with status="active"
- **Expected**: Work efforts match claims
- **Trace**: Document work effort IDs, titles, status
- **Evidence**: MCP response

**Check**: Work effort details
- **Method**: Read work effort files or query MCP
- **Expected**: Details match claims
- **Trace**: Document actual details vs claimed
- **Evidence**: Work effort content

---

### 8. GitHub State Verification

**Check**: Repository exists
- **Method**: Call `mcp_github_get_file_contents` or `gh repo view`
- **Expected**: Repository accessible
- **Trace**: Document repository URL, visibility
- **Evidence**: GitHub API response

**Check**: Recent commits
- **Method**: Call `mcp_github_list_commits` (last 5-10)
- **Expected**: Commits match claims
- **Trace**: Document commit SHAs, messages, dates
- **Evidence**: GitHub API response

**Check**: Open issues/PRs
- **Method**: Call `mcp_github_list_issues` and `mcp_github_list_pull_requests`
- **Expected**: Counts match claims
- **Trace**: Document actual counts vs claimed
- **Evidence**: GitHub API response

---

## Trace Documentation Format

Each verification check should produce a trace document with:

```markdown
# Verification Trace: [Check Name]

**Date**: YYYY-MM-DD HH:MM:SS
**Check ID**: verify-XXXX
**Status**: ✅ Verified | ⚠️ Partial | ❌ Failed | ❓ Unknown

## Claim
[What was claimed or assumed]

## Verification Method
[How we checked it]

## Evidence
[Actual evidence - command output, file content, API response, etc.]

## Result
[What we found - matches claim, differs, or unknown]

## Notes
[Any additional context, edge cases, or observations]

## Next Verification
[When to re-verify or what to check next]
```

---

## Trace Storage

**Location**: `_pyrite/standards/verification/`

**Structure**:
```
_pyrite/standards/verification/
├── traces/
│   ├── YYYY-MM-DD_verify-XXXX_[check-name].md
│   └── ...
├── index.md  # Index of all traces
└── checks.md # Catalog of verification checks
```

**Naming Convention**:
- `YYYY-MM-DD_verify-XXXX_[check-name].md`
- Example: `2026-01-07_verify-0001_date-time.md`

---

## Execution Steps

1. **Identify Claims**: Review chat history for verifiable claims
2. **Select Checks**: Choose relevant verification checks
3. **Run Checks**: Execute verification methods
4. **Document Traces**: Create trace documents with evidence
5. **Update Index**: Add traces to index.md
6. **Report Results**: Summarize findings

---

## Output Format

### Summary Table

| Check | Status | Evidence | Trace |
|-------|--------|----------|-------|
| Date/Time | ✅ | `date` output | `verify-0001` |
| Disk Space | ✅ | `df` output | `verify-0002` |
| Project Version | ✅ | `pyproject.toml` | `verify-0003` |
| ... | ... | ... | ... |

### Detailed Report

For each check:
- **Status**: ✅ Verified | ⚠️ Partial | ❌ Failed | ❓ Unknown
- **Evidence**: Link to trace document
- **Notes**: Any important observations

---

## Incremental Updates

When re-verifying:
1. **Read Previous Trace**: Load existing trace document
2. **Compare**: Check if evidence has changed
3. **Update**: Add new verification with timestamp
4. **Document Changes**: Note what changed and why
5. **Update Index**: Mark trace as updated

**Trace Update Format**:
```markdown
## Verification History

### 2026-01-07 19:00:00 - Initial Verification
[Original evidence]

### 2026-01-07 20:30:00 - Re-verification
[New evidence]
**Changes**: [What changed]
**Context**: [Why we re-verified]
```

---

## Adding New Checks

To add a new verification check:

1. **Identify Need**: What information needs verification?
2. **Design Method**: How can we verify it?
3. **Add to Command**: Add check to this document
4. **Test**: Run verification and document trace
5. **Refine**: Improve based on feedback

**Check Template**:
```markdown
**Check**: [Check name]
- **Method**: [How to verify]
- **Expected**: [What we expect]
- **Trace**: [What to document]
- **Evidence**: [What evidence to capture]
```

---

## Best Practices

1. **Verify Before Acting**: Check claims before making decisions
2. **Document Evidence**: Always capture actual evidence
3. **Be Specific**: Clear check names and methods
4. **Update Traces**: Re-verify when context changes
5. **Learn from Failures**: Document why checks failed
6. **Keep Lightweight**: Don't over-verify, focus on what matters
7. **Evolve**: Add/remove checks based on feedback

---

## Example Usage

```markdown
User: "The project is at version 0.0.2"

AI: Running verification...
- Check: Project version
- Method: Read pyproject.toml
- Evidence: version = "0.0.2"
- Status: ✅ Verified
- Trace: verify-0003_project-version.md
```

---

## Related Commands

- `spin-up` - Quick orientation (may use verify internally)
- `explore` - Deep exploration (may verify findings)
- `engineering` - Full workflow (uses verify for validation)

---

**This command is designed to grow and evolve. Add checks as needed, remove ones that aren't useful, and refine based on feedback.**
