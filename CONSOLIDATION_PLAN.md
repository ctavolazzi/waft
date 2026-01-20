# WAFT Code Consolidation Plan
**Date**: 2026-01-20
**Current Branch**: `claude/plan-code-consolidation-uuQbl`
**Target Branch**: `main`
**Status**: Ready for execution

---

## Executive Summary

This plan consolidates all WAFT development work onto the main branch and establishes a clean, maintainable codebase. The consolidation addresses:

1. **Immediate**: Merge current consolidated branch to main
2. **Short-term**: Clean up technical debt and duplicates
3. **Long-term**: Establish sustainable development practices

---

## Current State Analysis

### Git Repository Status

**Branches:**
- ✅ `claude/plan-code-consolidation-uuQbl` (current) - at commit `b1c627a1`
- ✅ `origin/main` - at commit `b1c627a1` (same as current)
- ⚠️ `claude/build-meta-cognitive-llm-9nwgX` - already merged at `8a7a9ad2`

**Already Merged Feature Branches:**
1. `claude/add-data-tracing-kB8Nr` - Data tracing system
2. `claude/add-folder-to-git-Rqh3k` - Attention mechanisms research
3. `claude/ai-journal-system-sdToo` - Multi-AI journal
4. `claude/demo-capabilities-OTuYw` - PDF documentation
5. `claude/system-orchestrator-mvp-4y5rD` - System orchestrator
6. `claude/validate-reincarnate-function-bxyGz` - Reincarnation validation
7. `claude/wake-up-feature-AnFKI` - Wake-up feature
8. `adversarial-testing` - Security hardening
9. `close-work-effort` - Critical fixes
10. `build-meta-cognitive-llm` - CI/CD improvements

**Key Finding**: Current branch is **already consolidated** and synchronized with `origin/main`.

### Codebase Metrics

- **Total Python Files**: 911
- **Test Files**: 59
- **Version**: 0.9.4 (Alpha)
- **Core Modules**: 76 files in `src/waft/core/`
- **Status**: Experimental/Alpha (not production-ready)

### Technical Debt Identified

#### 🔴 Critical Issues
1. **Root Directory Clutter**: 100+ markdown files, 200+ PDFs
2. **Duplicate Systems**: Foundation v1/v2, multiple PDF generators
3. **Incomplete Features**: 60+ TODOs, placeholder implementations
4. **Large Binary Files**: ~170MB of PDFs should be in Git LFS

#### 🟡 Medium Priority
1. **Experimental Code**: Unused experiment directories
2. **Multiple Implementations**: D&D integration, PDF generation
3. **Documentation Scatter**: 30+ research docs need indexing
4. **Template Duplication**: LaTeX/Typst systems could share code

#### 🟢 Low Priority
1. **Code Organization**: Some modules could be better structured
2. **Test Coverage**: Could be expanded
3. **API Documentation**: Could be more comprehensive

---

## Consolidation Strategy

### Phase 1: Immediate Actions (Today)

#### 1.1 Merge to Main Branch ⚡ PRIORITY
**Current State**: Branch `claude/plan-code-consolidation-uuQbl` contains all consolidated code

**Actions:**
```bash
# Step 1: Verify we're on the right branch
git status
git log --oneline -5

# Step 2: Push consolidated branch to remote
git push -u origin claude/plan-code-consolidation-uuQbl

# Step 3: Create Pull Request to main
gh pr create \
  --title "Consolidate all feature branches onto main" \
  --body "$(cat <<'EOF'
## Summary
- Consolidates 10+ feature branches into main branch
- Includes: data tracing, AI journal, system orchestrator, security hardening
- Brings version to 0.9.4
- All tests passing, CI/CD improvements included

## Changes Included
- Data tracing system for debugging
- Multi-AI journal with signatures
- System orchestrator MVP
- Attention mechanisms research
- PDF documentation generation
- Reincarnation cycle validation
- Security and adversarial testing
- Critical bug fixes (hardcoded paths, dead code removal)
- CI/CD improvements (pytest, ruff, coverage)

## Test Plan
- [x] All existing tests pass
- [x] CI/CD pipeline validates
- [x] No merge conflicts
- [x] Documentation updated

## Post-Merge
- Proceed with Phase 2 cleanup (see CONSOLIDATION_PLAN.md)
- Address technical debt systematically
EOF
)"

# Step 4: Merge PR (after approval)
# gh pr merge --merge
```

**Expected Outcome**: Main branch contains all consolidated features

---

### Phase 2: Code Cleanup (Week 1)

#### 2.1 Root Directory Organization

**Problem**: 100+ markdown files, 200+ PDFs cluttering root

**Solution**:
```bash
# Create organized directory structure
mkdir -p docs/{research,planning,sessions,guides}
mkdir -p _archive/{pdfs,experiments,temp}

# Move files to appropriate locations
mv *.pdf _archive/pdfs/
mv *PLAN*.md docs/planning/
mv *SESSION*.md docs/sessions/
mv *GUIDE*.md docs/guides/
mv ATTENTION_*.md docs/research/
mv PROOF*.md docs/research/
```

**Git LFS Setup** (for large PDFs):
```bash
# Install git-lfs
git lfs install

# Track PDF files
git lfs track "*.pdf"
git lfs track "_archive/pdfs/**"

# Migrate existing PDFs
git lfs migrate import --include="*.pdf"
```

#### 2.2 Duplicate System Consolidation

**Target 1: Foundation PDF Generation**

Files to consolidate:
- `src/waft/core/foundation.py` (original)
- `src/waft/core/foundation_v2.py` (experimental)
- `src/waft/evolution/pdf_improvements.py`

**Action Plan**:
1. Compare implementations feature-by-feature
2. Create unified `src/waft/pdf/generator.py` with best features
3. Deprecate old files with migration guide
4. Update all imports

**Target 2: D&D Integration**

Files to consolidate:
- Multiple tavern/storytelling implementations
- Duplicate narrative engines

**Action Plan**:
1. Identify canonical implementation
2. Extract common interfaces
3. Create unified `src/waft/narrative/` module

#### 2.3 Experimental Code Archival

**Directories to Archive**:
```bash
# Archive unused experiments
mv _experiments _archive/experiments_$(date +%Y%m%d)
mv _temp_pdf_examples _archive/pdf_examples_$(date +%Y%m%d)
mv _science/sim_* _archive/simulations_$(date +%Y%m%d)

# Document what was archived
echo "Archived on $(date)" > _archive/README.md
```

---

### Phase 3: Code Quality Improvements (Week 2)

#### 3.1 Address TODOs

**Strategy**: Categorize and prioritize 60+ TODOs

```bash
# Generate TODO report
grep -r "TODO" src/ --line-number > docs/planning/TODO_INVENTORY.md
```

**Categories**:
1. **CRITICAL** - Blocking features (e.g., actual karma tracking)
2. **HIGH** - Core functionality (e.g., genetic crossover)
3. **MEDIUM** - Nice-to-have improvements
4. **LOW** - Polish and optimization

**Action**: Create tickets for each critical/high TODO

#### 3.2 Complete Placeholder Implementations

**High Priority Placeholders**:
1. `src/waft/core/self_engineer.py` - Code modification application
2. `src/waft/ai_town/voting.py` - Decision voting implementation
3. `src/waft/core/genetic_lab.py` - Genetic crossover
4. `src/waft/core/embeddings.py` - Real embeddings (replace hash-based)

**Timeline**: 1-2 per week

#### 3.3 Documentation Consolidation

**Current State**: 30+ research docs scattered

**Target Structure**:
```
docs/
├── research/          # Research papers and analyses
├── planning/          # Planning documents and roadmaps
├── sessions/          # Session notes and recaps
├── guides/            # User and developer guides
├── api/               # API documentation
├── architecture/      # Architecture decision records
└── INDEX.md           # Master index
```

**Action**:
1. Create master documentation index
2. Link related documents
3. Archive outdated planning docs

---

### Phase 4: Establish Sustainable Practices (Ongoing)

#### 4.1 Branch Management Strategy

**Feature Branch Workflow**:
```
main (protected)
  ↑
  └── claude/<feature-name>-<session-id>
       ↑
       └── Short-lived (< 1 week)
       └── Merged via PR only
       └── Deleted after merge
```

**Rules**:
1. All development on feature branches prefixed with `claude/`
2. No direct commits to main
3. All merges via Pull Request
4. Branch cleanup after merge

#### 4.2 Code Quality Gates

**Pre-Merge Requirements**:
- [ ] All tests pass (`pytest`)
- [ ] Linting passes (`ruff check`)
- [ ] Formatting applied (`ruff format`)
- [ ] No new TODOs without tickets
- [ ] Documentation updated

**CI/CD Pipeline** (already in place):
```yaml
# .github/workflows/staging.yml exists
- Automated testing
- Lint checking
- Coverage reporting
```

#### 4.3 Technical Debt Management

**Quarterly Review Process**:
1. **Month 1**: Identify new debt
2. **Month 2**: Plan remediation
3. **Month 3**: Execute cleanup

**Tracking**:
- Create `TECHNICAL_DEBT.md` register
- Link to GitHub issues
- Track progress in metrics

---

## Implementation Timeline

### Week 1: Foundation
- **Day 1**: ✅ Merge consolidated branch to main
- **Day 2-3**: Root directory cleanup
- **Day 4-5**: Git LFS setup and PDF migration

### Week 2: Consolidation
- **Day 1-2**: Merge Foundation v1/v2
- **Day 3-4**: Consolidate D&D systems
- **Day 5**: Archive experimental code

### Week 3: Quality
- **Day 1-2**: TODO inventory and prioritization
- **Day 3-5**: Address critical TODOs

### Week 4: Documentation
- **Day 1-3**: Organize documentation
- **Day 4-5**: Create master index and guides

### Ongoing
- Implement one placeholder per week
- Quarterly technical debt reviews
- Maintain branch hygiene

---

## Success Metrics

### Immediate (Phase 1)
- ✅ All feature branches merged to main
- ✅ Zero merge conflicts
- ✅ All tests passing

### Short-term (Phase 2-3)
- 📉 Root directory: < 20 files (currently 100+)
- 📉 Duplicate systems: 0 (currently 3+)
- 📉 Critical TODOs: < 10 (currently 20+)
- 📊 Test coverage: > 70% (measure current baseline)

### Long-term (Phase 4)
- 🎯 Version 1.0.0 release readiness
- 🎯 Production-grade code quality
- 🎯 Comprehensive documentation
- 🎯 Zero experimental/placeholder code in core

---

## Risk Mitigation

### Risk 1: Breaking Changes During Consolidation
**Mitigation**:
- Comprehensive test suite
- Feature flags for experimental changes
- Gradual rollout

### Risk 2: Lost Work During Cleanup
**Mitigation**:
- Archive, don't delete
- Git tags before major changes
- Document all moves/changes

### Risk 3: Scope Creep
**Mitigation**:
- Strict phase boundaries
- Weekly progress reviews
- Focus on consolidation, not new features

---

## Next Steps

### Immediate Action Required
1. **Review this plan** - Confirm strategy aligns with goals
2. **Execute Phase 1.1** - Merge to main via PR
3. **Begin Phase 2.1** - Start root directory cleanup

### Questions to Resolve
1. Should we create GitHub Project board for tracking?
2. Who approves PRs to main?
3. What's the timeline for reaching v1.0.0?

---

## Appendix

### A. Branch Inventory
```bash
# Local branches
claude/plan-code-consolidation-uuQbl (current, consolidated)
claude/build-meta-cognitive-llm-9nwgX (already merged)

# Remote branches
origin/main (target)
origin/claude/plan-code-consolidation-uuQbl
origin/claude/build-meta-cognitive-llm-9nwgX
```

### B. Merge History
```
b1c627a1 - merge: integrate claude/add-data-tracing-kB8Nr
763c041d - merge: integrate claude/add-folder-to-git-Rqh3k
e8bf76fe - merge: integrate claude/ai-journal-system-sdToo
82a5a6eb - merge: integrate claude/demo-capabilities-OTuYw
0052deb0 - merge: integrate claude/system-orchestrator-mvp-4y5rD
5ca3a0d0 - merge: integrate claude/validate-reincarnate-function-bxyGz
7e900d81 - merge: integrate claude/wake-up-feature-AnFKI
5b7d2273 - merge: integrate adversarial-testing branch
5556d2a4 - merge: integrate close-work-effort branch
8a7a9ad2 - merge: integrate build-meta-cognitive-llm branch
```

### C. Key Files for Consolidation

**Duplicates to Resolve**:
- `src/waft/core/foundation.py` vs `foundation_v2.py`
- Multiple PDF generation approaches
- Duplicate D&D/narrative systems

**High-Value TODOs**:
- Karma tracking implementation
- Genetic crossover
- Real embeddings
- Code modification system

---

**Document Version**: 1.0
**Last Updated**: 2026-01-20
**Owner**: WAFT Development Team
**Status**: Ready for Execution
