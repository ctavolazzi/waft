# Verify Command Creation

**Date**: 2026-01-07 19:05 PST  
**Work**: Create `/verify` command for Cursor  
**Status**: ✅ Complete

---

## Summary

Created a lightweight, traceable verification command system that allows incremental documentation of verifiable information with scientific rigor.

---

## What Was Created

### 1. Command File
- **Location**: `.cursor/commands/verify.md`
- **Purpose**: Defines verification workflow and checks
- **Features**:
  - 8 categories of verification checks
  - Trace documentation format
  - Incremental update system
  - Lightweight, non-exhaustive design

### 2. Trace Storage System
- **Location**: `_pyrite/standards/verification/`
- **Structure**:
  - `index.md` - Central index of all traces
  - `checks.md` - Catalog of verification checks
  - `traces/` - Individual trace documents

### 3. Initial Trace
- **Location**: `traces/2026-01-07_verify-0001_date-time.md`
- **Purpose**: Example trace for date/time verification
- **Status**: ✅ Verified

---

## Key Features

### Verification Checks (8 Categories)

1. **Environment Verification**
   - Date/Time accuracy
   - Disk space availability
   - Working directory

2. **Project State Verification**
   - Project structure validity
   - Git repository state
   - Project version

3. **Tool Availability Verification**
   - Required CLI tools
   - MCP servers operational
   - Runtime versions

4. **File/Directory Verification**
   - File existence
   - Directory existence
   - File content matches

5. **Configuration Verification**
   - Configuration values
   - Environment variables

6. **Dependency Verification**
   - Dependencies installed
   - Dependency versions

7. **Work Effort Verification**
   - Active work efforts
   - Work effort details

8. **GitHub State Verification**
   - Repository exists
   - Recent commits
   - Open issues/PRs

### Trace Documentation Format

Each trace includes:
- **Claim**: What was claimed or assumed
- **Verification Method**: How we checked it
- **Evidence**: Actual evidence (command output, file content, etc.)
- **Result**: What we found
- **Notes**: Additional context
- **Next Verification**: When to re-verify

### Incremental Updates

Traces can be updated over time with:
- Verification history
- Change tracking
- Context documentation
- Re-verification triggers

---

## Design Principles

1. **Verify, Don't Assume**: Check claims against reality
2. **Trace Everything**: Document evidence for each check
3. **Incremental Learning**: Build knowledge over time
4. **Lightweight**: Focus on what matters, not everything
5. **Evolve**: Add/remove checks based on feedback

---

## Usage

When information needs verification:

1. **Identify Claims**: Review chat for verifiable claims
2. **Select Checks**: Choose relevant verification checks
3. **Run Checks**: Execute verification methods
4. **Document Traces**: Create trace documents with evidence
5. **Update Index**: Add traces to index.md
6. **Report Results**: Summarize findings

---

## Example Trace

```
# Verification Trace: Date/Time Accuracy

**Date**: 2026-01-07 19:05:00 PST
**Check ID**: verify-0001
**Status**: ✅ Verified

## Claim
The current date and time should be accurate.

## Verification Method
Run `date` command

## Evidence
Wed Jan  7 19:05:00 PST 2026

## Result
✅ Verified: Date and time are accurate
```

---

## Next Steps

1. **Use the Command**: Run `/verify` when information needs verification
2. **Add Checks**: Add new verification checks as needs arise
3. **Update Traces**: Re-verify and update traces as context changes
4. **Refine System**: Improve based on feedback and usage

---

## Files Created

- `.cursor/commands/verify.md` - Command definition
- `_pyrite/standards/verification/index.md` - Trace index
- `_pyrite/standards/verification/checks.md` - Checks catalog
- `_pyrite/standards/verification/traces/2026-01-07_verify-0001_date-time.md` - Example trace

---

**Status**: ✅ Complete - Ready for use
