# Comprehensive Orchestration Prompt for Claude Code

**Copy and paste this entire prompt to Claude Code to execute a complete workflow orchestration.**

---

I'm glad we're working together. I want you to execute a comprehensive orchestration sequence to deeply understand this repository, analyze its current state, form hypotheses, and make strategic decisions.

Please execute the following commands in sequence, using the output of each to inform the next:

## Phase 1: Orientation & Context Gathering

**1. `/spin-up`**
Get oriented to the codebase quickly. Check date/time, disk space, MCP health, git status across repos, list active work efforts, read recent devlog history, and summarize current state and what's changed.

**2. `/consider`**
Pause and analyze the current situation. Identify available options for proceeding, evaluate trade-offs of different approaches, and present recommendations with reasoning. Consider: Should we do a full engineering workflow? What's the best path forward given what you've learned?

## Phase 2: Deep Understanding & Visualization

**3. `/engineering`**
Run the complete engineering workflow:
- **Spin-Up**: Get oriented (may overlap with step 1, that's fine - use the data you already have)
- **Explore**: Deep understanding of codebase structure, architecture, dependencies, patterns, functionality, documentation, testing, and integration points. Use GitHub MCP extensively for exploration. Document all findings in `_pyrite/active/` files. Log findings via `waft finding log` and unknowns via `waft unknown log`.
- **Draft Plan**: Create initial plan based on understanding
- **Critique Plan**: Review and refine the plan
- **Finalize Plan**: Lock in the final plan
- **Begin**: Start implementation (or prepare to start)

Use all available tools actively (Empirica, _pyrite, GitHub MCP, work-efforts, waft). Document findings throughout.

**4. `/visualize`**
Create an interactive browser dashboard to visualize current project state. Show git status, active work, project health. Generate standalone HTML file and open in browser for visual insight.

## Phase 3: Analysis & Goal Setting

**5. `/analyze`**
Analyze the data gathered. If Phase 1 data exists, analyze it. If not, run Phase 1 first, then analyze. Perform health analysis, identify issues and opportunities, analyze patterns and trends, generate insights and recommendations, and create a prioritized action plan. Save comprehensive analysis report.

**6. `/goal create "[Primary Objective]"`
Based on your analysis, define the larger objective/goal. Break it into actionable steps, set success criteria, and link to work effort if applicable. Document in goal tracking system.

## Phase 4: Checkpoint & Execution Planning

**7. `/checkpoint`**
Create a situation report (SITREP). Recap conversation so far, document current state, update devlog, sync work efforts, and create a recovery point for future reference.

**8. `/execute`**
Gather all relevant context (git, files, work efforts, goals), then execute your first set of probes to gather data:
- Run diagnostic commands
- Check system health
- Verify assumptions
- Test initial hypotheses
- Collect evidence
- Document findings as you go

Use comprehensive awareness before taking action.

## Phase 5: Hypothesis Formation & Verification

**9. Form Hypotheses**
Based on the data you've gathered, form testable hypotheses:
- What do we think is happening?
- What are our key assumptions?
- What needs to be tested?
- What would success look like?

Document hypotheses clearly. Identify what evidence would support or refute each.

**10. `/verify`**
Verify each hypothesis systematically. Check claims against reality, document evidence for each verification, create traceable verification records in `_pyrite/standards/verification/traces/`, update hypotheses based on findings, and mark verified/unverified/refuted hypotheses.

## Phase 6: Reflection & Strategic Planning

**11. `/reflect`**
Write a reflective journal entry. Reflect on:
- What you're doing
- What you're thinking
- What you're learning
- Patterns you notice
- Questions you have
- How you feel about the work
- What you'd do differently

Save to `_pyrite/journal/ai-journal.md`.

**12. `/recap`**
Create a comprehensive conversation recap. Extract key points, decisions, accomplishments. Document open questions, identify next steps. Save to `_work_efforts/SESSION_RECAP_YYYY-MM-DD.md`.

**13. `/proceed`**
Verify context and assumptions before proceeding. Check for ambiguity, perform flight check, ask clarifying questions if needed, then proceed with verified understanding.

**14. `/decide`**
Use decision matrix methodology. If multiple paths forward exist, evaluate options:
- Identify alternatives
- Define evaluation criteria
- Assign weights to criteria
- Score each alternative
- Calculate weighted scores
- Present recommendations with reasoning

Use mathematical decision-making techniques. Document the decision process.

---

## Expected Deliverables

After completing this sequence, provide:

1. **Summary of All Phases**: What was accomplished in each phase
2. **Key Findings**: Most important discoveries
3. **Hypotheses Status**: Which hypotheses were verified/refuted
4. **Decision Matrix Results**: What path forward was chosen and why
5. **Next Steps**: Clear, prioritized action items
6. **Documentation Map**: Where all outputs were saved

---

## Important Notes

- **Use tools actively**: Don't just read - use Empirica, _pyrite, GitHub MCP, work-efforts, waft commands
- **Document as you go**: Create files in `_pyrite/active/` during each phase
- **Log findings**: Use `waft finding log` for discoveries, `waft unknown log` for gaps
- **Commit frequently**: Make incremental commits with clear messages
- **Update tickets**: Keep work effort tickets updated with progress
- **Verify often**: Run `waft verify` after significant changes
- **Be thorough**: Complete each phase fully before moving on

---

**Begin execution now. Provide progress updates as you complete each phase, and a comprehensive summary at the end.**
