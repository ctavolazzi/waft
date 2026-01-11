# Comprehensive Orchestration Prompt

**Purpose**: Complete workflow orchestration for deep project understanding, analysis, and strategic planning.

**Use when**: Starting a new major initiative, conducting comprehensive project review, or preparing for significant development work.

---

## Execution Sequence

Execute the following commands in order, using the output of each to inform the next:

### Phase 1: Orientation & Context Gathering

**1. `/spin-up`**
- Get oriented to the codebase quickly
- Check date/time accuracy
- Verify disk space
- Check MCP health
- Review git status across repos
- List active work efforts
- Read recent devlog history
- Summarize current state and changes

**2. `/consider`**
- Pause and analyze the current situation
- Identify available options for proceeding
- Evaluate trade-offs of different approaches
- Present recommendations with reasoning
- Consider: Should we do full engineering workflow? What's the best path forward?

### Phase 2: Deep Understanding & Visualization

**3. `/engineering`**
- Run complete engineering workflow:
  - **Spin-Up**: Get oriented (may overlap with step 1, that's fine)
  - **Explore**: Deep understanding of codebase structure, architecture, dependencies, patterns
  - **Draft Plan**: Create initial plan based on understanding
  - **Critique Plan**: Review and refine the plan
  - **Finalize Plan**: Lock in the final plan
  - **Begin**: Start implementation (or prepare to start)
- Use all available tools actively (Empirica, _pyrite, GitHub MCP, work-efforts, waft)
- Document findings in `_pyrite/active/` throughout
- Log findings via `waft finding log` and unknowns via `waft unknown log`

**4. `/visualize`**
- Create interactive browser dashboard
- Visualize current project state
- Show git status, active work, project health
- Generate standalone HTML file
- Open in browser for visual insight

### Phase 3: Analysis & Goal Setting

**5. `/analyze`**
- If Phase 1 data exists, analyze it
- If not, run Phase 1 first, then analyze
- Perform health analysis
- Identify issues and opportunities
- Analyze patterns and trends
- Generate insights and recommendations
- Create prioritized action plan
- Save comprehensive analysis report

**6. `/goal create "[Objective Name]"`
- Define the larger objective/goal
- Break it into actionable steps
- Set success criteria
- Link to work effort if applicable
- Document in goal tracking system

### Phase 4: Checkpoint & Execution Planning

**7. `/checkpoint`**
- Create situation report (SITREP)
- Recap conversation so far
- Document current state
- Update devlog
- Sync work efforts
- Create recovery point for future reference

**8. `/execute`**
- Gather all relevant context (git, files, work efforts, goals)
- Execute first set of probes to gather data:
  - Run diagnostic commands
  - Check system health
  - Verify assumptions
  - Test hypotheses
  - Collect evidence
- Use comprehensive awareness before taking action
- Document findings as you go

### Phase 5: Hypothesis Formation & Verification

**9. `/hypothesis`** (or form hypothesis manually if command doesn't exist)
- Based on data gathered, form testable hypotheses:
  - What do we think is happening?
  - What are our assumptions?
  - What needs to be tested?
- Document hypotheses clearly
- Identify what evidence would support/refute each

**10. `/verify`**
- Verify each hypothesis systematically
- Check claims against reality
- Document evidence for each verification
- Create traceable verification records
- Update hypotheses based on findings
- Mark verified/unverified/refuted hypotheses

### Phase 6: Reflection & Strategic Planning

**11. `/reflect`**
- Write reflective journal entry
- Reflect on:
  - What you're doing
  - What you're thinking
  - What you're learning
  - Patterns you notice
  - Questions you have
  - How you feel about the work
  - What you'd do differently
- Save to `_pyrite/journal/ai-journal.md`

**12. `/recap`**
- Create comprehensive conversation recap
- Extract key points, decisions, accomplishments
- Document open questions
- Identify next steps
- Save to `_work_efforts/SESSION_RECAP_YYYY-MM-DD.md`

**13. `/proceed`**
- Verify context and assumptions before proceeding
- Check for ambiguity
- Perform flight check
- Ask clarifying questions if needed
- Proceed with verified understanding

**14. `/decide`**
- Use decision matrix methodology
- If multiple paths forward, evaluate options:
  - Identify alternatives
  - Define evaluation criteria
  - Assign weights to criteria
  - Score each alternative
  - Calculate weighted scores
  - Present recommendations
- Use mathematical decision-making techniques
- Document decision process

---

## Expected Outputs

After completing this sequence, you should have:

1. **Orientation Complete**
   - Current state understood
   - Environment verified
   - Active work identified

2. **Deep Understanding**
   - Codebase structure mapped
   - Architecture understood
   - Patterns identified
   - Dependencies known

3. **Visual Insight**
   - Interactive dashboard created
   - Current state visualized
   - Relationships understood

4. **Analysis Complete**
   - Health assessed
   - Issues identified
   - Opportunities discovered
   - Action plan created

5. **Goal Defined**
   - Objective clear
   - Steps broken down
   - Success criteria set

6. **Checkpoint Created**
   - State documented
   - Recovery point established
   - Devlog updated

7. **Data Gathered**
   - Probes executed
   - Evidence collected
   - Assumptions tested

8. **Hypotheses Formed**
   - Testable hypotheses documented
   - Verification plan created

9. **Verification Complete**
   - Hypotheses verified/refuted
   - Evidence documented
   - Traces created

10. **Reflection Done**
    - Journal entry written
    - Learning captured
    - Patterns recognized

11. **Recap Complete**
    - Conversation summarized
    - Decisions documented
    - Next steps identified

12. **Context Verified**
    - Assumptions checked
    - Ambiguity resolved
    - Ready to proceed

13. **Decision Made**
    - Options evaluated
    - Recommendation provided
    - Path forward clear

---

## Documentation Locations

All outputs should be saved to:

- **Spin-up findings**: `_pyrite/active/YYYY-MM-DD_engineering_spinup.md`
- **Exploration findings**: `_pyrite/active/YYYY-MM-DD_exploration_*.md`
- **Analysis report**: `_pyrite/analyze/analyze-YYYY-MM-DD-HHMMSS.md`
- **Checkpoint**: `_work_efforts/CHECKPOINT_YYYY-MM-DD_[TOPIC].md`
- **Verification traces**: `_pyrite/standards/verification/traces/`
- **Journal entry**: `_pyrite/journal/ai-journal.md`
- **Recap**: `_work_efforts/SESSION_RECAP_YYYY-MM-DD.md`
- **Visualization**: `_pyrite/.waft/visualize-YYYY-MM-DD-HHMMSS.html`
- **Goals**: Goal tracking system
- **Work efforts**: `_work_efforts/` via MCP

---

## Integration Points

### Tool Usage Throughout

- **Empirica**: Create sessions, log findings/unknowns, preflight/postflight
- **_pyrite**: Document all findings in `_pyrite/active/`
- **GitHub MCP**: Extensive exploration, search patterns, check state
- **Work Efforts MCP**: Create/update work efforts and tickets
- **Waft Commands**: `waft info`, `waft verify`, `waft stats`, `waft finding log`
- **Git**: Frequent commits, status checks, history review

### Command Dependencies

- `/spin-up` → informs `/consider` and `/engineering`
- `/engineering` → creates data for `/analyze`
- `/analyze` → informs `/goal` creation
- `/execute` → gathers data for `/hypothesis`
- `/hypothesis` → guides `/verify` targets
- `/verify` → validates `/hypothesis`
- `/reflect` → captures learning from all phases
- `/recap` → summarizes entire sequence
- `/proceed` → verifies before `/decide`
- `/decide` → finalizes path forward

---

## Best Practices

1. **Use Tools Actively**: Don't just read, use Empirica, _pyrite, MCPs, waft
2. **Document As You Go**: Create files during each phase
3. **Log Findings**: Use `waft finding log` for discoveries
4. **Track Unknowns**: Use `waft unknown log` for gaps
5. **Commit Frequently**: Make incremental commits
6. **Update Tickets**: Keep work effort tickets updated
7. **Verify Often**: Run `waft verify` after changes
8. **Check Stats**: Use `waft stats` to track progress
9. **Be Thorough**: Complete each phase fully before moving on
10. **Stay Organized**: Use proper file naming and organization

---

## Error Handling

If any command fails:
- Document the failure
- Continue with remaining commands if possible
- Note what was skipped
- Provide summary of what completed vs. what failed
- Suggest remediation steps

---

## Time Estimates

- **Phase 1** (spin-up + consider): ~2-5 minutes
- **Phase 2** (engineering + visualize): ~15-30 minutes
- **Phase 3** (analyze + goal): ~5-10 minutes
- **Phase 4** (checkpoint + execute): ~5-10 minutes
- **Phase 5** (hypothesis + verify): ~10-15 minutes
- **Phase 6** (reflect + recap + proceed + decide): ~5-10 minutes

**Total**: ~45-80 minutes for complete orchestration

---

## Customization

This prompt can be customized:

- **Skip phases**: Remove phases not needed
- **Add phases**: Insert additional commands
- **Modify sequence**: Reorder based on needs
- **Focus areas**: Emphasize specific phases
- **Depth control**: Adjust detail level per phase

---

## Example Usage

```
User: [Paste this entire prompt]

AI: [Executes sequence, providing progress updates for each phase]

AI: ✅ Comprehensive Orchestration Complete
    - Orientation: ✓
    - Understanding: ✓
    - Visualization: ✓
    - Analysis: ✓
    - Goal: ✓
    - Checkpoint: ✓
    - Execution: ✓
    - Hypothesis: ✓
    - Verification: ✓
    - Reflection: ✓
    - Recap: ✓
    - Proceed: ✓
    - Decision: ✓
    
    📁 All outputs saved to documented locations
    🎯 Next steps: [Based on decision matrix results]
```

---

**This prompt orchestrates a complete workflow from orientation through decision-making, ensuring comprehensive understanding and strategic planning before action.**
