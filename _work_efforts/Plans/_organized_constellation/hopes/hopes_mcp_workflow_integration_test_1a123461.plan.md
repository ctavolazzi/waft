---
name: MCP Workflow Integration Test
overview: Create a comprehensive test harness for the MCP workflow system with staged gates, run the test against localhost:5050, and generate a briefing document with pass/fail results at each checkpoint.
todos:
  - id: create-process-doc
    content: Create process document with stages, gates, and pass/fail criteria
    status: completed
  - id: start-server
    content: Start localhost:5050 dev server in background
    status: completed
    dependencies:
      - create-process-doc
  - id: gate-1-server
    content: "Gate 1: Verify server running with browser snapshot"
    status: completed
    dependencies:
      - start-server
  - id: mcp-discovery
    content: Test all 6 MCP servers and record availability
    status: completed
    dependencies:
      - gate-1-server
  - id: gate-2-mcp
    content: "Gate 2: Document MCP tool availability results"
    status: completed
    dependencies:
      - mcp-discovery
  - id: execute-workflow
    content: "Execute test workflow: create WE, tickets, task, verify"
    status: completed
    dependencies:
      - gate-2-mcp
  - id: gate-3-workflow
    content: "Gate 3: Verify workflow execution results"
    status: completed
    dependencies:
      - execute-workflow
  - id: generate-briefing
    content: Generate final briefing document with all findings
    status: completed
    dependencies:
      - gate-3-workflow
  - id: commit-results
    content: Commit all documentation to git
    status: completed
    dependencies:
      - generate-briefing

category: hopes
confidence: 0.79
constellation_date: 2026-01-14
---

# MCP Workflow Integration Test Plan

## Objective
Test the complete MCP tool orchestration workflow with defined stages, gates, and automated reporting. The test will verify that all MCP tools work together correctly on a real task.

## Architecture

```mermaid
flowchart TD
    subgraph phase1 [Phase 1: Setup]
        A1[Start localhost:5050] --> A2[Create Process Document]
        A2 --> A3[Gate 1: Server Running]
    end
    
    subgraph phase2 [Phase 2: MCP Discovery]
        B1[Test sequential-thinking] --> B2[Test memory]
        B2 --> B3[Test filesystem]
        B3 --> B4[Test docs-maintainer]
        B4 --> B5[Test browser]
        B5 --> B6[Test work-efforts]
        B6 --> B7[Gate 2: MCP Tools Available]
    end
    
    subgraph phase3 [Phase 3: Workflow Execution]
        C1[Create Work Effort] --> C2[Create Tickets]
        C2 --> C3[Execute Task]
        C3 --> C4[Verify with Browser]
        C4 --> C5[Update Tickets]
        C5 --> C6[Gate 3: Workflow Complete]
    end
    
    subgraph phase4 [Phase 4: Reporting]
        D1[Collect Gate Results] --> D2[Generate Briefing]
        D2 --> D3[Save to _docs]
    end
    
    phase1 --> phase2 --> phase3 --> phase4
```

## Deliverables

### 1. Process Document
Location: [`_docs/20-29_development/workflow_category/workflow.02_mcp_integration_test_process.md`](_docs/20-29_development/workflow_category/workflow.02_mcp_integration_test_process.md)

Contents:
- Expected workflow stages
- Gate definitions with pass/fail criteria
- Expected tool chain for each phase

### 2. Test Execution Log
Location: [`_docs/20-29_development/workflow_category/workflow.03_mcp_integration_test_results.md`](_docs/20-29_development/workflow_category/workflow.03_mcp_integration_test_results.md)

Contents:
- Timestamp for each gate
- Pass/Fail status with evidence
- Error messages if any
- Screenshots or snapshots where applicable

### 3. Briefing Document
Location: [`_docs/20-29_development/workflow_category/workflow.04_mcp_integration_briefing.md`](_docs/20-29_development/workflow_category/workflow.04_mcp_integration_briefing.md)

Contents:
- Executive summary
- Gate-by-gate results table
- Issues discovered
- Recommendations

## Gate Definitions

| Gate | Name | Pass Criteria |
|------|------|---------------|
| G1 | Server Running | localhost:5050 responds, browser snapshot shows fogsift homepage |
| G2 | MCP Discovery | All 6 MCP servers respond (sequential-thinking, memory, filesystem, docs-maintainer, browser, work-efforts) |
| G3 | Workflow Execution | Work effort created, tickets created, task executed, browser verified |
| G4 | Documentation | All 3 documents created and committed |

## Test Task
The test will execute a simple but complete workflow:
- Create a work effort for "Add test badge to homepage"
- Create 2 tickets: "Add badge HTML" and "Verify with browser"
- Execute the first ticket (add a small test element)
- Verify using browser tools
- Complete tickets and work effort
- Document results

## Key Files
- Server: `npm run dev` uses [`scripts/build.js`](scripts/build.js) and browser-sync on port 5050
- MCP Docs: [`_docs/20-29_development/workflow_category/workflow.01_mcp_work_efforts_system_v0_3_0.md`](_docs/20-29_development/workflow_category/workflow.01_mcp_work_efforts_system_v0_3_0.md)
- MCP Server: `/Users/ctavolazzi/Code/.mcp-servers/work-efforts/server.js`

## Execution Steps

1. **Create Process Document** - Define expected workflow with gates
2. **Start Server** - Run `npm run dev` in background
3. **Gate 1 Check** - Verify server running with browser snapshot
4. **MCP Discovery Loop** - Test each MCP tool, record results
5. **Gate 2 Check** - Summarize MCP availability
6. **Execute Workflow** - Run through work-effort creation flow
7. **Gate 3 Check** - Verify workflow completed
8. **Generate Briefing** - Compile all results
9. **Gate 4 Check** - Verify documentation created
10. **Commit Results** - Push to git

## Notes
- The work-efforts MCP server is installed but may not be visible to AI (known issue from earlier debugging)
- Test will document this as a finding if it occurs
- Browser tools will be used to verify visual changes on localhost:5050