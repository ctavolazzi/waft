# Spin-Up

Get oriented to the codebase quickly with comprehensive state understanding.

## Steps

1. **Date check:** Run `date`

2. **Disk space:** Run `du -sh /Users/ctavolazzi/Code`

3. **MCP health:** Run `python3 /Users/ctavolazzi/Code/.mcp-servers/mcp_diagnostic.py`

4. **Git status:** Find uncommitted changes across repos:
   ```bash
   for dir in /Users/ctavolazzi/Code/*/; do
     if [ -d "$dir/.git" ]; then
       name=$(basename "$dir")
       changes=$(cd "$dir" && git status -s 2>/dev/null | wc -l | tr -d ' ')
       if [ "$changes" -gt 0 ]; then
         echo "⚠️  $name: $changes uncommitted"
       fi
     fi
   done
   ```

5. **Read ROOT README.md:** Read the project root README.md to understand the project

6. **Read relevant docs/briefings/sitreps:**
   - Search for briefing files (`**/*briefing*.md`)
   - Search for sitrep files (`**/*sitrep*.md`)
   - Read any found files to understand current context

7. **Scan work efforts abstract/state:**
   - Look for work efforts abstract file (`**/work_efforts/**/*abstract*.md`)
   - Look for state documentation (`**/work_efforts/**/*state*.md`)
   - Read `_work_efforts/CURRENT_STATE_AND_DIRECTION.md` if it exists
   - Read any state-related files to understand project state

8. **Active work:** Call `list_work_efforts` (status: "active")

9. **Recent history:** Read last 50 lines of `_work_efforts/devlog/devlog.md` (or `_work_efforts/devlog.md`)

10. **Previous state:** Read latest `_spin_up/understanding_*.txt` file (if exists)

11. **Check assumptions:** 
    - Identify key assumptions from README, docs, and state files
    - Verify critical assumptions about project structure, dependencies, and current state
    - Document any unverified assumptions

12. **Summarize:** Report what changed, what's active, what's next, and current state understanding

## Output

Provide a concise summary:
- Environment status (disk, date)
- MCP health (X/11 servers)
- Git issues (uncommitted repos)
- Project understanding (from README and docs)
- Current state (from work efforts and state files)
- Active work efforts
- Key assumptions identified and verified
- What changed since last understanding
- Recommended next step

---

**Full procedure:** See `_spin_up/SPIN_UP_PROCEDURE.md` for deep diagnostics.
