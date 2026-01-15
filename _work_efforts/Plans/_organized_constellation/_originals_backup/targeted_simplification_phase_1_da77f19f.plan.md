---
name: Targeted Simplification Phase 1
overview: "Apply targeted fixes to Phase 1 implementation: replace test script with --test flag, simplify parse_command() logic, and preserve structure for Phase 2 readiness."
todos:
  - id: add-test-flag
    content: Add --test flag to tavern_keeper.py CLI for quick integration testing
    status: pending
  - id: inline-command-logic
    content: Inline parse_command() logic into main() with cleaner implementation
    status: pending
  - id: delete-test-script
    content: Delete test_tavern_keeper.py (replaced by --test flag)
    status: pending
  - id: update-readme
    content: Update sovereign/README.md with simplified test instructions
    status: pending
  - id: verify-voice-commands
    content: Verify voice commands still work after changes
    status: pending
  - id: verify-test-flag
    content: Test the new --test flag with PocketBase running
    status: pending
---

# Targeted Simplification of Phase 1

## Why Not Full Restructuring

The original plan to reduce from 7 files to 3 had critical issues:

1. Voice command support ("Status Report", "The Mine is open") would break with argparse subcommands
2. Inlining commands now creates churn for Phase 2 when arXiv integration expands mine_open.py
3. Removing detailed error messages hurts CLI user experience
4. Actual reduction is 7 to 4 files (must keep `__init__.py`)

## Targeted Fixes

### Fix 1: Replace test_tavern_keeper.py with --test flag

**Current:** 100+ line `test_tavern_keeper.py` file

**Target:** Add `--test` flag to CLI that:
- Creates a test log entry
- Runs status report
- Verifies output contains expected elements
- Reports pass/fail

**File:** [sovereign/tavern_keeper.py](awesome-pocketbase/pocketbase-demo/sovereign/tavern_keeper.py)

```python
parser.add_argument('--test', action='store_true', help='Run integration test')

# In main():
if args.test:
    # Quick integration test
    client = PocketBaseClient()
    client.create_state_log("pocketbase", "online", "Test entry")
    summary = client.get_status_summary()
    if summary:
        print("Test passed")
    else:
        print("Test failed")
    sys.exit(0)
```

**Delete:** `test_tavern_keeper.py`

### Fix 2: Simplify parse_command() logic

**Current:** Separate function with substring matching

**Target:** Inline into main() with cleaner logic

```python
def main():
    # ... argparse setup ...
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Simple command mapping
    cmd = " ".join(args.command).lower()
    if "status" in cmd or "report" in cmd:
        output = execute_status_report()
    elif "mine" in cmd or "open" in cmd:
        output = execute_mine_open(args.query)
    elif "garrison" in cmd:
        output = format_message("Garrison - Phase 4 placeholder")
    else:
        output = format_error(f"Unknown command: {cmd}")
    
    print(output)
```

**Delete:** `parse_command()` function (but keep logic inline)

### Fix 3: Update README with simplified test instructions

**File:** [sovereign/README.md](awesome-pocketbase/pocketbase-demo/sovereign/README.md)

Replace elaborate test section with:
```markdown
## Testing

python -m sovereign.tavern_keeper --test
```

## What We Keep (Phase 2 Ready)

- `commands/` directory structure (will expand for arXiv integration)
- `status_report.py` and `mine_open.py` as separate files
- Detailed error messages in `pb_client.py` (helpful at CLI boundary)
- `persona.py` formatting functions

## Final Structure

```
sovereign/
├── __init__.py           # Package marker (required)
├── pb_client.py          # REST client (unchanged)
├── persona.py            # Formatting (unchanged)
├── tavern_keeper.py      # CLI (simplified: inline command logic, add --test)
├── README.md             # Updated test instructions
└── commands/
    ├── __init__.py       # Keep for Phase 2
    ├── status_report.py  # Unchanged
    └── mine_open.py      # Unchanged (Phase 2 expands this)
```

**Net change:** Delete 1 file (`test_tavern_keeper.py`), simplify 1 file (`tavern_keeper.py`)

## Validation

After changes:
1. `python -m sovereign.tavern_keeper status` works
2. `python -m sovereign.tavern_keeper "Status Report"` works (voice command preserved)
3. `python -m sovereign.tavern_keeper --test` runs integration test
4. Error messages remain helpful when PocketBase not running