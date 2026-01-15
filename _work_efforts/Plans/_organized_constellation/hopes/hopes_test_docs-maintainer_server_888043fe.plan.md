---
name: Test docs-maintainer Server
overview: Test the docs-maintainer MCP server to verify all 7 tools are functioning correctly by running the existing test suite and performing manual tool invocations.
todos:
  - id: run-test-suite
    content: Run .mcp-servers/test-all-tools.mjs and review results
    status: completed
  - id: test-initialize
    content: Test initialize_docs tool
    status: completed
  - id: test-create
    content: Test create_doc tool
    status: completed
  - id: test-search-health
    content: Test search_docs and check_health tools
    status: completed
  - id: cleanup
    content: Clean up test artifacts
    status: completed

category: hopes
confidence: 0.67
constellation_date: 2026-01-14
---

# Test docs-maintainer MCP Server

## Approach

Run the existing MCP test suite and verify the docs-maintainer tools work correctly.

## Steps

### 1. Run Existing Test Suite

Execute the test script at [`.mcp-servers/test-all-tools.mjs`](.mcp-servers/test-all-tools.mjs) which tests all MCP servers.Note: The README indicates docs-maintainer currently has "0 tests (manual)" so this will just verify connectivity.

### 2. Manual Tool Verification

Test each tool using the MCP tool calls available in this session:

- `initialize_docs` - Create `_docs` in a test directory
- `create_doc` - Create a sample document
- `update_doc` - Modify the document
- `search_docs` - Search for the document
- `check_health` - Run health check
- `rebuild_indices` - Rebuild all indexes
- `link_work_effort` - Link to a work effort (if `_work_efforts` exists)

### 3. Cleanup

Remove any test artifacts created during verification.

## Test Location