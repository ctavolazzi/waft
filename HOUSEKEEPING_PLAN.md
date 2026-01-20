# WAFT Housekeeping Plan

> **Comprehensive plan to organize the WAFT project with a clean README as the central table of contents**

Date: 2026-01-17
Status: Planning Phase

---

## 📋 Current State Analysis

### Root Directory Issues

**Current Problems:**
- **205 total items** in root directory
- **62 markdown files** scattered in root
- Large PDFs mixed with code
- Unclear organization
- Hard to navigate
- No clear "table of contents" structure

### What We Have

**Root Directory Contains:**
- Core project files (README, pyproject.toml, etc.)
- 62 loose markdown files
- Large PDFs (GPT-4 paper, research papers)
- LaTeX files and templates
- Multiple special directories (_pyrite, _experiments, etc.)
- Hidden config dirs (.cursor, .empirica, etc.)
- Archive directories

---

## 🎯 Housekeeping Goals

### Primary Objectives

1. **Clean README** as the primary table of contents
2. **Reduce root clutter** from 205 items to ~20-30 core items
3. **Organize documentation** into clear hierarchy
4. **Preserve all data** and functionality
5. **Improve discoverability** of features and resources

### Design Principles

- **Zero data loss**: Everything moved, nothing deleted
- **Logical grouping**: Related items together
- **Clear naming**: Obvious what goes where
- **Easy access**: Important things easy to find
- **Scalability**: System that works as project grows

---

## 📁 Proposed Directory Structure

### New Root Organization

```
waft/
├── README.md                    # Main table of contents
├── CHANGELOG.md                 # Version history
├── LICENSE                      # License file
├── CONTRIBUTING.md              # Contribution guide
├── pyproject.toml              # Project config
├── uv.lock                     # Dependencies
├── .python-version             # Python version
│
├── docs/                       # ALL DOCUMENTATION
│   ├── README.md               # Docs navigation
│   ├── DOCUMENTATION_INDEX.md  # Master index
│   ├── GETTING_STARTED.md      # Quick start
│   ├── ARCHITECTURE.md         # System design
│   ├── FAQ.md                  # Questions
│   ├── TROUBLESHOOTING.md      # Problem solving
│   ├── DEVELOPER_GUIDE.md      # Development
│   │
│   ├── api/                    # API reference
│   ├── guides/                 # User guides
│   ├── tutorials/              # Tutorials
│   ├── research/               # Research papers
│   ├── archive/                # Historical docs
│   └── assets/                 # Images, diagrams
│
├── src/                        # Source code
│   └── waft/                   # Main package
│
├── tests/                      # Test suite
│
├── examples/                   # Example projects
│
├── scripts/                    # Utility scripts
│
├── resources/                  # NON-CODE RESOURCES
│   ├── papers/                 # Research PDFs
│   ├── latex/                  # LaTeX templates
│   ├── data/                   # Data files
│   └── media/                  # Images, videos
│
├── archive/                    # ARCHIVED CONTENT
│   ├── old_docs/              # Deprecated docs
│   ├── experiments/           # Old experiments
│   └── legacy/                # Legacy code
│
├── _work_efforts/             # Development tracking
├── _pyrite/                   # Memory system
├── _integrations/             # Integrations
│
└── .github/                   # GitHub config
    ├── workflows/             # CI/CD
    └── ISSUE_TEMPLATE/        # Templates
```

---

## 🔄 File Migration Plan

### Phase 1: Create New Structure

**Create directories:**
```bash
# Documentation organization
mkdir -p docs/archive
mkdir -p docs/research
mkdir -p docs/assets

# Resources organization
mkdir -p resources/papers
mkdir -p resources/latex
mkdir -p resources/data
mkdir -p resources/media

# Archive organization
mkdir -p archive/old_docs
mkdir -p archive/experiments
mkdir -p archive/legacy
```

### Phase 2: Move Documentation Files

**Strategy**: Group by type and purpose

**Root markdown files to move:**

**To docs/research/**:
- Gamification-Research.md
- ONE_PAGER_EVOLUTION_SYSTEM.md
- AI_NARRATIVE_GUIDE.md
- IRREFUTABLE_PROOF.md

**To docs/archive/**:
- REFACTORING_PLAN.md
- PR_DESCRIPTION.md
- PR_SUMMARY.md
- PDF_FORMATTING_IMPROVEMENTS_COMPLETE.md
- PDF_IMPROVEMENTS_SUMMARY.md
- PDF_LIBRARY_COMPARISON_SUMMARY.md
- PYRITE_IMPLEMENTATION_SUMMARY.md
- PYRITE_DEMO_AND_OBSTACLE_COURSE.md
- DEMO_TEMPLATE_README.md
- COMPREHENSIVE_ORCHESTRATION_PROMPT.md

**To docs/guides/** (create these):
- PDF_SUPERCUT_BINDER_README.md → PDF_BINDER_GUIDE.md
- PDF_GENERATOR_FILES_INVENTORY.md → PDF_FILES_REFERENCE.md

**To archive/old_docs/**:
- MAIN_GOAL.md
- "Claude Code WAFT Genesis Moment.md"
- "Mint Genesis.md"
- CREDITS.md

### Phase 3: Move Resource Files

**PDFs to resources/papers/**:
- GPT-4-Techincal-Report.pdf
- GPT-4-Techincal-Report_RECREATED.pdf
- GenerativeAgents-Simulacra2304.03442v2.pdf
- Code Generation Competition*.pdf
- DocumentBuilder_Evolution_Report.pdf

**LaTeX to resources/latex/**:
- Batch-Test-Document.tex
- LaTeX-Generator-Test.tex
- "Latex Source Code/" directory
- Latex Source Code.zip
- _temp_latex_templates/ → resources/latex/templates/

**Data files to resources/data/**:
- 18029100.json

### Phase 4: Consolidate Special Directories

**Keep in root (well-defined purpose):**
- _pyrite/ (memory system)
- _work_efforts/ (development tracking)
- _integrations/ (integration code)

**Move to archive/experiments/**:
- _experiments/
- _epic_run/
- _fracture/
- _genetics/
- _hidden/
- _probe_data/
- _science/
- _science_textbook/
- _standalone_tools/
- _temp/
- _notebook/
- _pantheon/
- _realms/

**Move to archive/legacy/**:
- Obsidian_Archive/
- NARRATIVE-WAFT/
- WAFT-Mac-Shortcuts-Research/
- WAFT-One-Pager-Feature-Research/
- WAFT-PDF-PNG-Conversion-Research/

---

## 📄 New README.md Structure

### Proposed Table of Contents Design

```markdown
# WAFT: The Evolutionary Code Laboratory

> A Python framework for directed evolution of self-modifying AI agents

[![Version](badge)](link) [![License](badge)](link) [![Docs](badge)](link)

**Don't just build agents. Breed them.**

---

## 🚀 Quick Start

[5-minute quick start section]

---

## 📚 Documentation

Complete documentation available at **[docs/DOCUMENTATION_INDEX.md](docs/DOCUMENTATION_INDEX.md)**

### Essential Guides
- **[Getting Started](docs/GETTING_STARTED.md)** - Your first WAFT laboratory
- **[Architecture](docs/ARCHITECTURE.md)** - System design and concepts
- **[API Reference](docs/api/API_INDEX.md)** - Complete API documentation
- **[FAQ](docs/FAQ.md)** - Frequently asked questions
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

### By Role
- **New Users** → [Getting Started Guide](docs/GETTING_STARTED.md)
- **Developers** → [Developer Guide](docs/DEVELOPER_GUIDE.md)
- **Researchers** → [Research Documentation](docs/research/)
- **Contributors** → [Contributing Guide](CONTRIBUTING.md)

---

## 🧬 Core Concepts

[Brief overview with links to detailed docs]

---

## 💻 Installation

[Installation section]

---

## 🎯 Features

[Feature overview with links]

---

## 📖 Project Organization

### Directory Structure
```
waft/
├── docs/              → All documentation
├── src/waft/          → Source code
├── tests/             → Test suite
├── examples/          → Example projects
├── resources/         → Papers, data, media
├── _pyrite/           → Memory system
└── _work_efforts/     → Development tracking
```

### Key Resources
- **Documentation**: [docs/](docs/)
- **Research Papers**: [resources/papers/](resources/papers/)
- **Examples**: [examples/](examples/)
- **API Reference**: [docs/api/](docs/api/)
- **Change Log**: [CHANGELOG.md](CHANGELOG.md)

---

## 🔬 Scientific Mission

[Brief mission statement with links]

---

## 🤝 Contributing

[Contributing section]

---

## 📊 Project Status

[Status badges and info]

---

## 📞 Support & Community

[Support links]

---

## 📜 License

MIT License - see [LICENSE](LICENSE)

---

## 🔗 Links

- **Documentation**: [docs/DOCUMENTATION_INDEX.md](docs/DOCUMENTATION_INDEX.md)
- **GitHub**: https://github.com/ctavolazzi/waft
- **Issues**: https://github.com/ctavolazzi/waft/issues
- **Discussions**: https://github.com/ctavolazzi/waft/discussions
```

---

## 🔧 Implementation Steps

### Step 1: Backup (Safety First)

```bash
# Create complete backup
git checkout -b backup-before-housekeeping
git add -A
git commit -m "Backup before housekeeping"
git push -u origin backup-before-housekeeping

# Create work branch
git checkout -b housekeeping/organize-root
```

### Step 2: Create Directory Structure

```bash
# Create all new directories
mkdir -p docs/{archive,research,assets}
mkdir -p resources/{papers,latex,data,media}
mkdir -p archive/{old_docs,experiments,legacy}
```

### Step 3: Move Files Systematically

**Use git mv to preserve history:**

```bash
# Research docs
git mv Gamification-Research.md docs/research/
git mv ONE_PAGER_EVOLUTION_SYSTEM.md docs/research/
git mv AI_NARRATIVE_GUIDE.md docs/research/

# Papers
git mv GPT-4-Techincal-Report.pdf resources/papers/
git mv GenerativeAgents-Simulacra2304.03442v2.pdf resources/papers/
# ... etc

# Archive old docs
git mv REFACTORING_PLAN.md docs/archive/
git mv PR_DESCRIPTION.md docs/archive/
# ... etc

# Move special directories
git mv _experiments archive/experiments/
git mv _epic_run archive/experiments/
# ... etc
```

### Step 4: Update README.md

```bash
# Edit README with new structure
# (We'll create the new version)
```

### Step 5: Create Navigation Files

```bash
# Create docs/README.md
# Create resources/README.md
# Create archive/README.md
```

### Step 6: Update Links

```bash
# Find all broken links
grep -r "\[.*\](.*\.md)" docs/

# Update references in code
# Update references in docs
```

### Step 7: Verify

```bash
# Check nothing broken
waft verify

# Run tests
pytest

# Check docs build
# (if applicable)
```

### Step 8: Commit & Push

```bash
git add -A
git commit -m "chore: Organize project structure and clean root directory"
git push -u origin housekeeping/organize-root
```

---

## 📋 Detailed File Inventory

### Files to Move

**Documentation (62 markdown files in root)**

Format: `source → destination`

```
# Research & Design
Gamification-Research.md → docs/research/gamification.md
ONE_PAGER_EVOLUTION_SYSTEM.md → docs/research/one_pager_system.md
AI_NARRATIVE_GUIDE.md → docs/research/narrative_guide.md
IRREFUTABLE_PROOF.md → docs/research/proof_of_concept.md

# Implementation Summaries (Archive)
REFACTORING_PLAN.md → docs/archive/refactoring_plan.md
PR_DESCRIPTION.md → docs/archive/pr_description.md
PR_SUMMARY.md → docs/archive/pr_summary.md
PYRITE_IMPLEMENTATION_SUMMARY.md → docs/archive/pyrite_summary.md
PYRITE_DEMO_AND_OBSTACLE_COURSE.md → docs/archive/pyrite_demo.md
PDF_FORMATTING_IMPROVEMENTS_COMPLETE.md → docs/archive/pdf_improvements.md
PDF_IMPROVEMENTS_SUMMARY.md → docs/archive/pdf_summary.md
PDF_LIBRARY_COMPARISON_SUMMARY.md → docs/archive/pdf_comparison.md

# Feature Documentation
PDF_SUPERCUT_BINDER_README.md → docs/guides/pdf_binder_guide.md
PDF_GENERATOR_FILES_INVENTORY.md → docs/reference/pdf_files.md

# Historical (Archive)
MAIN_GOAL.md → archive/old_docs/main_goal.md
CREDITS.md → archive/old_docs/credits.md
"Claude Code WAFT Genesis Moment.md" → archive/old_docs/genesis_moment.md
"Mint Genesis.md" → archive/old_docs/mint_genesis.md
DEMO_TEMPLATE_README.md → archive/old_docs/demo_template.md
COMPREHENSIVE_ORCHESTRATION_PROMPT.md → archive/old_docs/orchestration_prompt.md
```

**Resources (PDFs, LaTeX, Data)**

```
# Research Papers
GPT-4-Techincal-Report.pdf → resources/papers/gpt4_technical_report.pdf
GPT-4-Techincal-Report_RECREATED.pdf → resources/papers/gpt4_recreated.pdf
GenerativeAgents-Simulacra2304.03442v2.pdf → resources/papers/generative_agents.pdf
Code Generation Competition*.pdf → resources/papers/code_generation_competition.pdf
DocumentBuilder_Evolution_Report.pdf → resources/papers/document_builder_report.pdf

# LaTeX
Batch-Test-Document.tex → resources/latex/batch_test.tex
LaTeX-Generator-Test.tex → resources/latex/generator_test.tex
"Latex Source Code/" → resources/latex/source/
Latex Source Code.zip → resources/latex/source.zip
_temp_latex_templates/ → resources/latex/templates/

# Data
18029100.json → resources/data/18029100.json
```

**Directories to Archive**

```
# Experiments
_experiments/ → archive/experiments/experiments/
_epic_run/ → archive/experiments/epic_run/
_fracture/ → archive/experiments/fracture/
_genetics/ → archive/experiments/genetics/
_hidden/ → archive/experiments/hidden/
_probe_data/ → archive/experiments/probe_data/
_science/ → archive/experiments/science/
_science_textbook/ → archive/experiments/science_textbook/
_standalone_tools/ → archive/experiments/standalone_tools/
_temp/ → archive/experiments/temp/
_notebook/ → archive/experiments/notebook/
_pantheon/ → archive/experiments/pantheon/
_realms/ → archive/experiments/realms/

# Legacy
Obsidian_Archive/ → archive/legacy/obsidian_archive/
NARRATIVE-WAFT/ → archive/legacy/narrative_waft/
WAFT-Mac-Shortcuts-Research/ → archive/legacy/mac_shortcuts/
WAFT-One-Pager-Feature-Research/ → archive/legacy/one_pager_research/
WAFT-PDF-PNG-Conversion-Research/ → archive/legacy/pdf_conversion_research/
```

---

## ✅ Success Criteria

### Metrics

**Before Housekeeping:**
- Root items: 205
- Root .md files: 62
- Documentation scattered: Yes
- Navigation difficulty: High

**After Housekeeping:**
- Root items: ~25-30
- Root .md files: ~5 (README, CHANGELOG, CONTRIBUTING, LICENSE, etc.)
- Documentation organized: Yes
- Navigation difficulty: Low

### Validation Checklist

- [ ] Root directory has <30 items
- [ ] All docs in docs/ directory
- [ ] All resources in resources/ directory
- [ ] All archives in archive/ directory
- [ ] README.md is clean table of contents
- [ ] All links working
- [ ] No data lost
- [ ] Git history preserved
- [ ] Tests still pass
- [ ] Documentation builds
- [ ] Easy to find things

---

## 📊 Impact Analysis

### Benefits

1. **Improved Navigation**: Clear hierarchy, easy to find
2. **Better Onboarding**: New users can navigate easily
3. **Reduced Clutter**: Focus on what matters
4. **Scalability**: Structure supports growth
5. **Professionalism**: Clean, organized project
6. **Maintainability**: Easier to maintain

### Risks

1. **Broken Links**: Need to update references
2. **User Confusion**: Temporary during transition
3. **Merge Conflicts**: If others working on files
4. **Time Investment**: ~2-4 hours of work

### Mitigation

1. **Use git mv**: Preserves history
2. **Create README files**: Navigation in each dir
3. **Update all links**: Systematic link checking
4. **Communicate changes**: Document what moved where
5. **Backup first**: Safety branch

---

## 🚀 Execution Plan

### Timeline

**Phase 1: Preparation** (30 minutes)
- Create backup branch
- Create work branch
- Create new directory structure

**Phase 2: Migration** (1-2 hours)
- Move documentation files
- Move resource files
- Move archived content
- Update directory README files

**Phase 3: Updates** (1 hour)
- Rewrite root README.md
- Update links throughout project
- Create navigation files
- Update documentation index

**Phase 4: Validation** (30 minutes)
- Check all links
- Run tests
- Verify no data lost
- Test navigation

**Phase 5: Finalization** (15 minutes)
- Commit changes
- Push to remote
- Create PR
- Document changes

**Total Estimated Time**: 3-4 hours

---

## 📝 Next Steps

1. **Review this plan** - Confirm approach is good
2. **Get approval** - User confirms to proceed
3. **Execute Phase 1** - Backup and setup
4. **Execute systematically** - Follow plan step-by-step
5. **Validate thoroughly** - Ensure nothing broken
6. **Document completion** - Create summary report

---

## 🎯 Key Principles

Throughout execution:

1. **Safety First**: Always backup before changes
2. **Preserve History**: Use git mv, not delete/recreate
3. **No Data Loss**: Move everything, delete nothing
4. **Systematic Approach**: One phase at a time
5. **Validate Often**: Check as you go
6. **Document Changes**: Clear commit messages

---

**Ready to execute? This plan provides:**
- ✅ Clear before/after structure
- ✅ Detailed file inventory
- ✅ Step-by-step execution
- ✅ Safety measures
- ✅ Validation criteria
- ✅ Time estimates

**Outcome:** Clean, organized WAFT project with README as central table of contents.

---

*Plan created: 2026-01-17 | Status: Awaiting Approval*
