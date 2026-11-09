# WAFT Housekeeping Plan V2 - Incremental & Safe

> **Revised plan incorporating adversarial feedback - incremental, automated, verified**

Date: 2026-01-17
Status: REVISED - Ready for Review
Version: 2.0 (Addresses all V1 critiques)

---

## 🎯 Response to Critiques

### Critique 1: "3-4 hours is laughable"
**VALID.** Original estimate was naive.

**Fix:**
- Broken into weekly phases over 3-4 weeks
- Each phase is 2-4 hours
- Testing and validation built into each phase
- Total realistic time: ~20-30 hours over a month

### Critique 2: "Zero data loss - famous last words"
**VALID.** Need verification, not promises.

**Fix:**
- Automated verification script (before/after checksums)
- Manifest file tracking every move
- Git history verification
- Automated link checker
- Test suite must pass after each phase

### Critique 3: "Archive death trap"
**PARTIALLY VALID.** But we need to preserve experiments.

**Fix:**
- Archive only truly deprecated content
- Add `archive/README.md` with clear criteria
- Monthly review of archive (is it needed?)
- If uncertain, DON'T archive - ask first
- Clear labeling: "Safe to delete after YYYY-MM-DD"

### Critique 4: "Why resources/ directory?"
**VALID.** PDFs shouldn't bloat git.

**Fix:**
- Move large PDFs to Git LFS
- External papers: link to external storage (Zenodo, arXiv)
- LaTeX templates: Keep if actively used, delete if not
- Resource dir only for frequently-accessed, medium-sized files

### Critique 5: "README rewrite red flag"
**VALID.** Need maintenance plan.

**Fix:**
- README has max 200 lines (enforced)
- Detailed content in docs/
- Auto-generated sections from metadata
- Weekly stale link checker (CI/CD)
- Clear ownership: documented in CONTRIBUTING.md

### Critique 6: "git mv not enough"
**VALID.** Need redirect strategy.

**Fix:**
- Document old → new path mappings
- Create redirect system for external links
- Use GitHub Pages with redirects
- Update all external documentation simultaneously
- Pin migration in issues for 30 days

### Critique 7: "Link updates - hand waving"
**VERY VALID.** Need concrete approach.

**Fix:**
- Automated link checker script (pre-written)
- Python script to update imports
- Grep for hardcoded paths
- Manual checklist for each file type
- CI/CD link validation

### Critique 8: "No rollback plan"
**CRITICAL MISS.** Need rollback.

**Fix:**
- Each phase has dedicated rollback branch
- Rollback script provided
- 48-hour validation period before next phase
- Can rollback any single phase independently
- Ongoing work merged AFTER phase complete

### Critique 9: "Impact analysis weak"
**VALID.** Need metrics.

**Fix:**
- Survey: "How hard is it to find X?" (before/after)
- Measure: Time to onboard new contributor
- Track: Navigation paths in docs
- Success criteria: 50% reduction in "where is X?" questions
- If metrics don't improve, rollback

### Critique 10: "One person's vision"
**FAIR POINT.** Need buy-in.

**Fix:**
- This plan is PROPOSAL, not decree
- Solicit feedback (issue template)
- 1-week comment period
- Vote on whether to proceed
- Option to do nothing is valid

---

## 🔄 REVISED APPROACH: Incremental Migration

### Core Principle: **ONE DIRECTORY AT A TIME**

No big bang. Each week, one focused change. Validate before moving on.

---

## 📅 Phase-by-Phase Plan

### **Phase 0: Preparation & Validation** (Week 0)

**Goals:**
- Set up automation
- Get team buy-in
- No actual moves yet

**Tasks:**
1. Create verification script
2. Create link checker
3. Document current state (manifest)
4. Solicit feedback on plan
5. Create rollback procedures

**Deliverables:**
- `scripts/verify_structure.py` - Checksums all files
- `scripts/check_links.py` - Validates all links
- `MANIFEST.md` - Current file inventory
- Rollback script template
- Issue for community feedback

**Success Criteria:**
- All scripts tested and working
- At least 3 people reviewed plan
- No blocking objections

**Time Estimate:** 4-6 hours

**Rollback:** N/A (nothing changed yet)

---

### **Phase 1: Move Large PDFs to Git LFS** (Week 1)

**Why First:** Highest value, lowest risk, immediate benefit

**Goals:**
- Reduce repo bloat
- No link updates needed (LFS is transparent)
- Easy to verify

**Tasks:**
1. Install Git LFS
2. Configure `.gitattributes` for PDFs
3. Move PDFs to LFS
4. Verify file sizes reduced
5. Test checkout on fresh clone

**Files to Move:**
```bash
git lfs track "*.pdf"
git add .gitattributes
git add *.pdf
git commit -m "chore: Move PDFs to Git LFS"
```

**Success Criteria:**
- Repo size reduction > 10MB
- All PDFs accessible
- Fresh clone works
- No broken links

**Time Estimate:** 2 hours

**Rollback Plan:**
```bash
git lfs untrack "*.pdf"
git restore .gitattributes
```

---

### **Phase 2: Archive Obvious Experiments** (Week 2)

**Why Second:** Clear wins, low controversy

**Goals:**
- Move clearly-unused experiment dirs
- Document what was moved and why

**Directories to Archive:**
```
_temp/          → archive/experiments/temp/
_hidden/        → archive/experiments/hidden/
_probe_data/    → archive/experiments/probe_data/
```

**Tasks:**
1. Create `archive/experiments/README.md` explaining criteria
2. Use `git mv` for each directory
3. Update any broken imports (automated check)
4. Add deprecation notice
5. Run test suite

**Verification:**
- `scripts/verify_structure.py` passes
- Test suite passes
- No errors in Python imports

**Success Criteria:**
- 3 directories moved
- Zero broken imports
- Tests green

**Time Estimate:** 3 hours

**Rollback Plan:**
```bash
git mv archive/experiments/temp _temp
git mv archive/experiments/hidden _hidden
git mv archive/experiments/probe_data _probe_data
```

---

### **Phase 3: Consolidate Research Docs** (Week 3)

**Why Third:** Documentation moves are safer than code

**Goals:**
- Move research markdown files to docs/research/
- Preserve git history
- Update links

**Files to Move:**
```
Gamification-Research.md → docs/research/gamification.md
ONE_PAGER_EVOLUTION_SYSTEM.md → docs/research/one_pager.md
AI_NARRATIVE_GUIDE.md → docs/research/narrative.md
IRREFUTABLE_PROOF.md → docs/research/proof_of_concept.md
```

**Tasks:**
1. Use `git mv` for each file
2. Run link checker
3. Update broken links (scripted where possible)
4. Update README references
5. Test all documentation builds

**Verification Script:**
```python
# scripts/check_doc_links.py
import re
import pathlib

def check_all_links():
    broken = []
    for md_file in pathlib.Path('docs').rglob('*.md'):
        content = md_file.read_text()
        links = re.findall(r'\[.*?\]\((.*?\.md)\)', content)
        for link in links:
            target = (md_file.parent / link).resolve()
            if not target.exists():
                broken.append((md_file, link))
    return broken
```

**Success Criteria:**
- All research docs in docs/research/
- Zero broken links (verified)
- Git history intact

**Time Estimate:** 4 hours

**Rollback Plan:**
```bash
git mv docs/research/gamification.md Gamification-Research.md
# ... etc
```

---

### **Phase 4: Create Resources Directory** (Week 4)

**Goals:**
- Organize LaTeX templates
- Move data files
- Clear documentation

**Structure:**
```
resources/
├── README.md          # What goes here and why
├── latex/
│   ├── templates/     # Active templates
│   └── examples/      # Example outputs
└── data/
    └── samples/       # Sample data files
```

**Tasks:**
1. Create directory structure
2. Move LaTeX files (if actively used)
3. Move data files (if needed)
4. Update import paths
5. Document structure

**Success Criteria:**
- Clear organization
- All imports working
- README explains purpose

**Time Estimate:** 3 hours

**Rollback Plan:**
```bash
git mv resources/latex/* ./
git mv resources/data/* ./
rm -rf resources/
```

---

### **Phase 5: Archive Historical Docs** (Week 5)

**Goals:**
- Move completed/outdated documentation
- Preserve history
- Clear current docs

**Files to Archive:**
```
REFACTORING_PLAN.md → docs/archive/refactoring_plan.md
PR_DESCRIPTION.md → docs/archive/pr_description.md
PDF_IMPROVEMENTS_SUMMARY.md → docs/archive/pdf_summary.md
PYRITE_IMPLEMENTATION_SUMMARY.md → docs/archive/pyrite_summary.md
```

**Tasks:**
1. Review each file (is it truly historical?)
2. Add date archived to filename
3. Update archive/README.md index
4. Move files
5. Update references

**Success Criteria:**
- Only active docs in docs/
- Historical context preserved
- Clear archive index

**Time Estimate:** 3 hours

**Rollback Plan:**
```bash
git mv docs/archive/*.md ./
```

---

### **Phase 6: README Rewrite** (Week 6)

**Goals:**
- Clean, focused README
- Table of contents
- Max 200 lines

**Structure:**
```markdown
# WAFT [50 lines max]
- Tagline
- Quick start
- Core concepts

## Documentation [50 lines max]
- Links to main docs
- By role navigation

## Project Organization [50 lines max]
- Directory structure
- Key resources

## Links & Support [50 lines max]
- Essential links only
```

**Tasks:**
1. Draft new README
2. Get feedback
3. Replace old README
4. Update badges
5. Validate all links

**Success Criteria:**
- < 200 lines
- All links work
- Clear navigation
- Professional appearance

**Time Estimate:** 4 hours

**Rollback Plan:**
```bash
git restore README.md
```

---

### **Phase 7: Final Cleanup** (Week 7)

**Goals:**
- Move remaining loose files
- Final verification
- Celebrate

**Tasks:**
1. Review root directory
2. Move any remaining clutter
3. Run full verification suite
4. Update all documentation
5. Create migration summary

**Success Criteria:**
- Root has < 30 items
- All tests pass
- All links work
- Team satisfied

**Time Estimate:** 3 hours

---

## 🛡️ Safety Measures

### Before EVERY Phase

```bash
# 1. Create phase branch
git checkout -b housekeeping/phase-N

# 2. Run verification
python scripts/verify_structure.py > pre-phase-N.txt

# 3. Run link checker
python scripts/check_links.py > pre-links-N.txt

# 4. Run tests
pytest
```

### After EVERY Phase

```bash
# 1. Run verification
python scripts/verify_structure.py > post-phase-N.txt

# 2. Compare
diff pre-phase-N.txt post-phase-N.txt

# 3. Check links
python scripts/check_links.py > post-links-N.txt

# 4. Run tests
pytest

# 5. If all pass, merge
git checkout main
git merge housekeeping/phase-N

# 6. Wait 48 hours, gather feedback

# 7. If issues, rollback
git revert <commit>
```

---

## 📊 Success Metrics

### Quantitative

- Root directory items: 205 → < 30
- Time to find common files: Measure before/after
- Broken links: 0
- Test failures: 0
- Repo size: Reduced by > 10MB

### Qualitative

- New contributor onboarding time (survey)
- Team satisfaction (poll)
- "Where is X?" questions reduced

### Required for Success

- At least 2/3 metrics improved
- Zero regressions
- Team approval

---

## 🚨 Stop Conditions

**STOP immediately if:**

1. **Tests fail** - Rollback phase
2. **Critical path broken** - Rollback phase
3. **Team objects** - Pause for discussion
4. **Data loss detected** - STOP ALL, investigate
5. **More than 2 hours over estimate** - Reassess

**Phase success requires:**
- All tests passing
- All links working
- Verification script passing
- No team objections

---

## 🔧 Automation Scripts

### 1. Verification Script

```python
#!/usr/bin/env python3
"""
Verify project structure integrity.
Usage: python scripts/verify_structure.py
"""
import hashlib
import pathlib
import json

def checksum_file(filepath):
    """Generate SHA-256 checksum of file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def scan_project():
    """Scan all files and generate manifest."""
    manifest = {}
    for filepath in pathlib.Path('.').rglob('*'):
        if filepath.is_file() and not filepath.match('.git/*'):
            manifest[str(filepath)] = checksum_file(filepath)
    return manifest

def verify(baseline_file='manifest.json'):
    """Verify against baseline."""
    with open(baseline_file) as f:
        baseline = json.load(f)

    current = scan_project()

    missing = set(baseline.keys()) - set(current.keys())
    added = set(current.keys()) - set(baseline.keys())
    changed = {k for k in set(baseline.keys()) & set(current.keys())
               if baseline[k] != current[k]}

    print(f"Missing files: {len(missing)}")
    print(f"Added files: {len(added)}")
    print(f"Changed files: {len(changed)}")

    if missing:
        print("\nMISSING FILES:")
        for f in missing:
            print(f"  - {f}")

    return len(missing) == 0

if __name__ == '__main__':
    import sys

    if '--create-baseline' in sys.argv:
        manifest = scan_project()
        with open('manifest.json', 'w') as f:
            json.dump(manifest, f, indent=2)
        print("Baseline created: manifest.json")
    else:
        success = verify()
        sys.exit(0 if success else 1)
```

### 2. Link Checker Script

```python
#!/usr/bin/env python3
"""
Check all markdown links.
Usage: python scripts/check_links.py
"""
import re
import pathlib
from urllib.parse import urlparse

def extract_links(content):
    """Extract markdown links."""
    # [text](url) format
    return re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)

def check_file_links(md_file):
    """Check all links in a markdown file."""
    content = md_file.read_text()
    links = extract_links(content)
    broken = []

    for text, link in links:
        # Skip external URLs
        if link.startswith(('http://', 'https://', 'mailto:')):
            continue

        # Handle anchors
        if link.startswith('#'):
            continue

        # Check local file links
        target = (md_file.parent / link).resolve()
        if not target.exists():
            broken.append((md_file, link))

    return broken

def check_all_links():
    """Check all markdown files."""
    all_broken = []
    for md_file in pathlib.Path('.').rglob('*.md'):
        if '.git' in str(md_file):
            continue
        broken = check_file_links(md_file)
        all_broken.extend(broken)

    return all_broken

if __name__ == '__main__':
    broken = check_all_links()

    if broken:
        print(f"Found {len(broken)} broken links:\n")
        for filepath, link in broken:
            print(f"{filepath}: {link}")
        exit(1)
    else:
        print("All links valid!")
        exit(0)
```

### 3. Rollback Script Template

```bash
#!/bin/bash
# Rollback script for Phase N

set -e

echo "Rolling back Phase N..."

# Restore files
git checkout HEAD~1 -- <files changed in phase>

# Or revert commit
# git revert <commit-hash>

# Run verification
python scripts/verify_structure.py
python scripts/check_links.py
pytest

echo "Rollback complete. Verify manually."
```

---

## 📋 Phase Checklist Template

**Copy for each phase:**

```markdown
## Phase N: [Name]

### Pre-Phase
- [ ] Create branch: housekeeping/phase-N
- [ ] Run verify_structure.py (save output)
- [ ] Run check_links.py (save output)
- [ ] Run pytest (confirm green)
- [ ] Review plan with team

### Execution
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3
- [ ] ...

### Post-Phase
- [ ] Run verify_structure.py (compare)
- [ ] Run check_links.py (all passing)
- [ ] Run pytest (all passing)
- [ ] Manual spot check
- [ ] Merge to main
- [ ] Wait 48 hours
- [ ] Gather feedback
- [ ] If issues: rollback
- [ ] If success: proceed to next phase

### Rollback (if needed)
- [ ] Run rollback script
- [ ] Verify restoration
- [ ] Document issue
- [ ] Revise plan
```

---

## 🎯 Decision Framework

### Should We Proceed?

**YES if:**
- Team approves (majority)
- Scripts are working
- We have 7 weeks to dedicate
- Risk tolerance is appropriate

**NO if:**
- Team objects
- Higher priority work exists
- Timeline too aggressive
- Current structure "good enough"

**DEFER if:**
- Need more automation
- Want to test on branch first
- Unsure about structure
- Want external feedback

---

## 📞 Communication Plan

### Week Before Phase 1
- [ ] Post plan to team
- [ ] Open RFC issue
- [ ] Solicit feedback
- [ ] Revise based on input

### During Each Phase
- [ ] Post phase start announcement
- [ ] Daily standup updates
- [ ] Post completion summary
- [ ] Request testing help

### After Completion
- [ ] Migration summary document
- [ ] Before/after metrics
- [ ] Lessons learned
- [ ] Thank contributors

---

## 🏁 Summary: V2 vs V1

### What Changed

| Aspect | V1 (Original) | V2 (Revised) |
|--------|---------------|--------------|
| **Timeline** | 3-4 hours | 7 weeks, ~25 hours total |
| **Approach** | Big bang | Incremental, one phase/week |
| **Verification** | Manual | Automated scripts |
| **Rollback** | "We have a backup" | Script per phase |
| **Metrics** | None | Quantitative + qualitative |
| **Risk** | High | Low (each phase isolated) |
| **Buy-in** | Assumed | Explicit approval process |
| **Link updates** | Hand-waving | Automated checker |
| **Data loss prevention** | Promises | Checksums + verification |
| **Stop conditions** | None | Explicit criteria |

### Why This is Better

1. **Incremental** - Can stop anytime
2. **Reversible** - Each phase can rollback
3. **Automated** - Scripts verify correctness
4. **Measured** - Metrics prove value
5. **Safe** - Stop conditions prevent damage
6. **Realistic** - Honest time estimates
7. **Democratic** - Team approval required

---

## ✅ Approval Needed

**This plan requires approval for:**

1. **Overall approach** - Do we want to do this at all?
2. **Timeline** - Is 7 weeks acceptable?
3. **Phase order** - Does the sequence make sense?
4. **Success criteria** - Are metrics appropriate?
5. **Resource allocation** - Can we dedicate ~25 hours?

**How to approve:**

- [ ] Review full plan
- [ ] Run scripts in test environment
- [ ] Discuss with team
- [ ] Vote: Proceed / Revise / Reject

---

**This plan is DEFENSIVE, INCREMENTAL, and SAFE.**

**It addresses all critiques while achieving the same goal.**

**Ready for review and approval.**

---

*Plan V2 created: 2026-01-17*
*Incorporates feedback from adversarial critique*
*Status: Awaiting approval to proceed with Phase 0*
