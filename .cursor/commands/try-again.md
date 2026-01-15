# /try-again - Retry with Adjustments

**Retries the last operation or command that failed, with intelligent adjustments based on what went wrong.**

---

## Purpose

This command makes the AI retry failed operations by:
1. **Identifying what failed** - Analyzes the last error, failed command, or unsuccessful operation
2. **Understanding the failure** - Examines error messages, logs, or context to understand why it failed
3. **Making adjustments** - Applies fixes, corrections, or alternative approaches
4. **Retrying intelligently** - Attempts again with improvements based on failure analysis
5. **Reporting results** - Shows what was fixed and whether the retry succeeded

**If the retry fails again, the AI will analyze why and suggest next steps.**

**Use when:**
- A command or operation just failed
- You want to retry something with fixes
- An error occurred and you want to try again
- A previous attempt didn't work as expected
- You need to re-attempt with adjustments

---

## Execution

**Command**: `/try-again` or `/retry` or `/redo`

**What the AI does:**
1. **Analyzes recent conversation** - Identifies the last failed operation, error, or unsuccessful attempt
2. **Examines the failure** - Reads error messages, checks logs, understands what went wrong
3. **Determines fixes** - Identifies what needs to be corrected or adjusted
4. **Applies corrections** - Makes necessary changes (code fixes, parameter adjustments, etc.)
5. **Retries the operation** - Executes again with the fixes applied
6. **Reports outcome** - Shows whether retry succeeded or what still needs fixing

**AI Actions:**
- Reviews conversation history for errors or failures
- Analyzes error messages and stack traces
- Checks relevant files or code that failed
- Identifies root cause of failure
- Applies fixes or adjustments
- Retries with corrected approach
- Reports success or continued issues

**If no failure found:**
- AI will ask what you want to retry
- Or you can specify the operation to retry

---

## What Gets Retried

### 1. Failed Commands
- ✅ Re-runs commands that failed
- ✅ Fixes command parameters or arguments
- ✅ Corrects file paths or options
- ✅ Adjusts execution context

### 2. Code Errors
- ✅ Fixes syntax errors
- ✅ Corrects import issues
- ✅ Resolves type mismatches
- ✅ Fixes logic errors

### 3. File Operations
- ✅ Retries file reads/writes that failed
- ✅ Fixes permission issues
- ✅ Corrects file paths
- ✅ Handles missing files

### 4. Script Execution
- ✅ Re-runs scripts with fixes
- ✅ Corrects script parameters
- ✅ Fixes dependencies
- ✅ Adjusts execution environment

### 5. API/Integration Calls
- ✅ Retries failed API calls
- ✅ Fixes authentication issues
- ✅ Corrects request parameters
- ✅ Handles network errors

---

## Retry Strategies

### 1. Error Analysis
- Reads error messages carefully
- Identifies specific failure points
- Understands error context
- Determines fixable vs. non-fixable errors

### 2. Fix Application
- Applies code corrections
- Adjusts parameters
- Fixes configuration issues
- Corrects file paths or references

### 3. Alternative Approaches
- Tries different methods if original fails
- Uses fallback options
- Applies workarounds
- Suggests alternative solutions

### 4. Incremental Retry
- Fixes one issue at a time
- Retries after each fix
- Builds up to complete solution
- Reports progress at each step

---

## Example Output

**Scenario**: PDF generation failed due to missing import

**User**: `/try-again`

**AI Response**:

```
🔄 RETRYING: PDF Generation

**Analysis:**
- Last operation: PDF generation from case file
- Error: `NameError: name 'Optional' is not defined`
- Location: `scripts/generate_case_pdf.py`, line 18
- Issue: Missing import for `Optional` from `typing` module

**Fix Applied:**
- Added `from typing import Optional` to imports
- File updated: `scripts/generate_case_pdf.py`

**Retrying...**
✅ PDF generated successfully: `_work_efforts/proof_cases/PROOF_CASE_...pdf`

**Result**: ✅ SUCCESS
The retry succeeded after fixing the missing import.
```

---

## Integration

This command works with:
- **All commands**: Can retry any failed command
- **Script execution**: Retries scripts with fixes
- **File operations**: Retries file operations with corrections
- **Code generation**: Retries code generation with fixes
- **Error handling**: Integrates with error analysis

---

## When to Use

**Use `/try-again` when**:
- ✅ A command just failed
- ✅ An operation didn't work as expected
- ✅ You see an error and want to retry with fixes
- ✅ A previous attempt needs adjustment
- ✅ You want to re-attempt something

**Don't use `/try-again` when**:
- ❌ The operation succeeded (no need to retry)
- ❌ You want to do something completely different
- ❌ The failure is intentional or expected
- ❌ You need to start from scratch (use original command)

---

## Retry Behavior

### Automatic Fixes
The AI will automatically:
- Fix syntax errors in code
- Add missing imports
- Correct file paths
- Adjust parameters
- Fix configuration issues

### Manual Intervention Required
The AI will ask for:
- User decisions on ambiguous fixes
- Confirmation for destructive operations
- Input for missing required information
- Approval for significant changes

### Retry Limits
- Will retry up to reasonable attempts
- Reports if retry keeps failing
- Suggests alternative approaches if retries fail
- Explains why retries aren't working if needed

---

## How It Works

When you use `/try-again`, the AI will:

1. **Review conversation** - Looks for the most recent error, failed command, or unsuccessful operation
2. **Analyze failure** - Examines error messages, stack traces, or failure context
3. **Identify root cause** - Determines what actually went wrong
4. **Apply fixes** - Makes necessary corrections to code, parameters, or approach
5. **Retry operation** - Executes again with fixes applied
6. **Report results** - Shows whether retry succeeded or what still needs attention

The AI does this **interactively in chat**, analyzing failures and applying fixes before retrying.

**This is an intelligent retry system that learns from failures and applies corrections.**

---

## Example Scenarios

### Scenario 1: Import Error
**Error**: `ImportError: No module named 'xyz'`  
**Fix**: Add missing import or install dependency  
**Retry**: Re-run with corrected imports

### Scenario 2: File Not Found
**Error**: `FileNotFoundError: 'path/to/file'`  
**Fix**: Correct file path or create missing file  
**Retry**: Re-run with correct path

### Scenario 3: Permission Error
**Error**: `PermissionError: [Errno 13] Permission denied`  
**Fix**: Check permissions or use alternative approach  
**Retry**: Re-run with permission fixes

### Scenario 4: Type Error
**Error**: `TypeError: expected str, got int`  
**Fix**: Convert types or adjust function calls  
**Retry**: Re-run with corrected types

### Scenario 5: Command Failure
**Error**: Command exited with non-zero status  
**Fix**: Correct command parameters or fix underlying issue  
**Retry**: Re-run command with fixes

---

## Success Criteria

**Retry succeeds when**:
- ✅ Original error is resolved
- ✅ Operation completes successfully
- ✅ Expected output is produced
- ✅ No new errors are introduced

**Retry needs more work when**:
- ⚠️ Different error occurs (needs new fix)
- ⚠️ Partial success (some issues remain)
- ⚠️ Requires user input or decision
- ⚠️ Needs alternative approach

---

## Error Handling

### If Retry Fails Again
- AI analyzes why retry failed
- Identifies if it's the same error or new issue
- Applies additional fixes if needed
- Suggests alternative approaches if retries keep failing

### If No Failure Found
- AI asks what you want to retry
- Or you can specify the operation explicitly
- AI helps identify what might need retrying

### If Fix Requires User Decision
- AI explains the issue
- Presents options for fixing
- Waits for your decision
- Applies your chosen fix

---

## Related Commands

- **`/prove-it`**: Prove claims (may retry if proof fails)
- **`/verify`**: Verify operations (may retry verification)
- **`/check-assumptions`**: Check assumptions (may retry checks)
- **`/improve`**: Improve code (may retry improvements)

---

**This command provides intelligent retry capability that learns from failures and applies corrections automatically.**

--- End Command ---
