---
name: Fix MCP Folder Name
overview: Update the MCP work-efforts server to use `_work_efforts` instead of `_work_efforts_` as the default folder name, making it consistent with fogsift and the README documentation.
todos:
  - id: fix-server
    content: Update server.js to use _work_efforts (3 occurrences + comment)
    status: completed
  - id: verify-fix
    content: Test list_work_efforts returns fogsift work efforts
    status: completed
---

# Fix MCP Work-Efforts Folder Name

## Problem

The MCP work-efforts server uses `_work_efforts_` (with trailing underscore) but:
- fogsift uses `_work_efforts` (no trailing underscore)
- The README documentation says `_work_efforts`
- This mismatch causes `list_work_efforts` to return "No work efforts found"

## Solution

Update 3 occurrences in [`/Users/ctavolazzi/Code/.mcp-servers/work-efforts/server.js`](/Users/ctavolazzi/Code/.mcp-servers/work-efforts/server.js):

| Line | Change |
|------|--------|
| 357 | `'_work_efforts_'` → `'_work_efforts'` |
| 435 | `'_work_efforts_'` → `'_work_efforts'` |
| 631 | `'_work_efforts_'` → `'_work_efforts'` |

Also update the documentation comment at line 12.

## Verification

After fix, run:
```
mcp_work-efforts_list_work_efforts(repo_path="/Users/ctavolazzi/Code/fogsift")
```

Should return the 4 work efforts instead of "No work efforts found".