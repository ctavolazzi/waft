---
name: Simplify Tavern Keeper CLI
overview: "Refactor the Phase 1 implementation to align with minimal coding style: inline commands, remove redundant parsing, simplify error handling, and reduce file count."
todos:
  - id: inline-commands
    content: Inline execute_status_report() and execute_mine_open() into tavern_keeper.py
    status: pending
  - id: remove-commands-dir
    content: Delete commands/ directory and all files within
    status: pending
  - id: simplify-parsing
    content: Remove parse_command(), use argparse subcommands directly
    status: pending
  - id: simplify-error-handling
    content: Simplify pb_client._authenticate() to let exceptions bubble up
    status: pending
  - id: simplify-test
    content: Replace test_tavern_keeper.py with simple README instructions or minimal smoke test
    status: pending
  - id: update-readme
    content: Update sovereign/README.md to reflect simplified structure
    status: pending
  - id: verify-cli
    content: Test CLI commands still work after simplification
    status: pending

category: dreads
confidence: 0.78
constellation_date: 2026-01-14
---

# Simplify Tavern Keeper CLI Implementation

## Current Issues (Overengineering)

1. **Redundant command parsing**: Both `argparse` and custom `parse_command()` function
2. **Premature file splitting**: Separate `commands/` directory with only 2 commands (one is placeholder)
3. **Over-specific error handling**: Catching specific exception types and re-raising with custom messages
4. **Unnecessary test script**: 100+ line test file when simple manual test would suffice

## Simplification Strategy

### 1. Consolidate Files

- **Merge** `commands/status_report.py` and `commands/mine_open.py` into `tavern_keeper.py`
- **Remove** `commands/` directory entirely
- **Keep** `pb_client.py` and `persona.py` as separate modules (reused logic)

### 2. Simplify Command Parsing

- **Remove** `parse_command()` function
- **Use** `argparse` subcommands directly for `status`, `mine`, `garrison`
- **Support** voice commands via argparse aliases or simple string matching in main()

### 3. Simplify Error Handling

- **Remove** specific exception catching in `pb_client._authenticate()`
- **Let** exceptions bubble up naturally
- **Format** errors only at CLI boundary in `main()`

### 4. Simplify Test Script

- **Replace** `test_tavern_keeper.py` with simple inline test instructions in README
- **Or** reduce to minimal smoke test (< 20 lines)

## Files to Modify

### `sovereign/tavern_keeper.py`

- Inline `execute_status_report()` and `execute_mine_open()` functions
- Remove `parse_command()` function
- Use argparse subcommands
- Simplify error handling (catch-all at boundary)

### `sovereign/pb_client.py`

- Simplify `_authenticate()` to let exceptions bubble up
- Remove specific exception handling (ConnectionError, TimeoutError, etc.)
- Keep basic `raise_for_status()` only

### `sovereign/commands/` (DELETE)

- Delete `commands/status_report.py`
- Delete `commands/mine_open.py`
- Delete `commands/__init__.py`
- Remove directory

### `test_tavern_keeper.py` (OPTIONAL)

- Either delete entirely and add test instructions to README
- Or reduce to minimal smoke test

### `sovereign/README.md`

- Update to reflect simplified structure
- Add simple manual test instructions

## Target Structure

```javascript
sovereign/
├── __init__.py
├── pb_client.py          # REST client (simplified error handling)
├── persona.py            # Formatting (unchanged)
└── tavern_keeper.py      # CLI with inlined commands
```



## Code Changes

### `tavern_keeper.py` - Use argparse subcommands

```python
parser = argparse.ArgumentParser(...)
subparsers = parser.add_subparsers(dest='command')

# Status command
status_parser = subparsers.add_parser('status', aliases=['report'])
# Mine command  
mine_parser = subparsers.add_parser('mine', aliases=['open'])
mine_parser.add_argument('--query', help='Research query')
# Garrison command
garrison_parser = subparsers.add_parser('garrison')
```



### `pb_client.py` - Simplified auth

```python
def _authenticate(self) -> None:
    url = f"{self.base_url}/api/admins/auth-with-password"
    response = self.session.post(url, json={...}, timeout=5)
    response.raise_for_status()
    self.token = response.json().get("token")
    self.session.headers.update({"Authorization": f"Bearer {self.token}"})
```



## Benefits

- **Reduced complexity**: 3 files instead of 7
- **Less abstraction**: Commands inlined where used
- **Simpler error handling**: Exceptions bubble naturally
- **Easier maintenance**: Fewer files to navigate
- **Aligns with coding style**: Minimal abstractions, inline logic

## Validation

After simplification:

1. Verify CLI still works: `python -m sovereign.tavern_keeper status`
2. Verify voice commands work: `python -m sovereign.tavern_keeper "Status Report"`