# GitHub Project Installation Exploration Template

**Status**: ✅ Template Ready  
**Created**: 2026-01-11  
**Purpose**: Template for exploring and documenting GitHub project installations

---

## Quick Start

### For Each New Project:

1. **Copy this template**:
   ```bash
   cp -r WE-260111-6vzd_github_project_installation_exploration_template \
        WE-YYMMDD-xxxx_[project_name]_installation_exploration
   ```

2. **Update the work effort ID**:
   - Rename folder to new ID
   - Update `WE-260111-6vzd_index.md` → `WE-YYMMDD-xxxx_index.md`
   - Update frontmatter ID in index file

3. **Fill in project information**:
   - Replace `[PROJECT_NAME]` with actual project name
   - Replace `[GITHUB_URL]` with actual GitHub URL
   - Update `INSTALLATION_EXPLORATION.md` with project details

4. **Start exploration**:
   - Follow the process in `INSTALLATION_EXPLORATION.md`
   - Track progress in `tools/work_effort_tracker.md`
   - Document findings as you go

---

## What's Included

### Core Files
- **`WE-260111-6vzd_index.md`** - Work effort index (update ID and title)
- **`INSTALLATION_EXPLORATION.md`** - Installation exploration template
- **`README.md`** - This file

### Tool Bag (`tools/`)
- **`work_effort_tracker.md`** - Progress tracking
- **`verification_checklist.md`** - Verification checklist
- **`README.md`** - Tool bag documentation

---

## Exploration Process

1. **Initial Analysis** - Read README, identify stack, note installation steps
2. **Environment Setup** - Check requirements, install dependencies
3. **Installation Attempt** - Follow instructions, document steps
4. **Verification** - Test installation, verify functionality
5. **Documentation** - Complete exploration document, update tracker

---

## Template Customization

### When Cloning for a New Project:

1. **Update placeholders**:
   - `[PROJECT_NAME]` → Actual project name
   - `[GITHUB_URL]` → Actual GitHub URL
   - `[OWNER]` → Repository owner
   - `[REPO_NAME]` → Repository name

2. **Customize for project type**:
   - Node.js projects: Focus on npm/yarn setup
   - Python projects: Focus on pip/conda setup
   - Rust projects: Focus on cargo setup
   - Docker projects: Focus on Docker setup

3. **Add project-specific sections**:
   - Configuration requirements
   - Environment variables
   - Database setup (if applicable)
   - API keys (if applicable)

---

## Example Usage

```bash
# Clone template for a new project
cp -r WE-260111-6vzd_github_project_installation_exploration_template \
     WE-260111-abc1_fastapi_project_installation_exploration

# Update files
cd WE-260111-abc1_fastapi_project_installation_exploration
# Edit WE-260111-abc1_index.md (update ID, title, project info)
# Edit INSTALLATION_EXPLORATION.md (fill in project details)

# Start exploration
# Follow INSTALLATION_EXPLORATION.md process
```

---

## Tips

- **Document as you go** - Don't wait until the end
- **Capture error messages** - Screenshots or copy-paste
- **Note solutions** - Even if you find them elsewhere
- **Test thoroughly** - Verify installation actually works
- **Update tracker** - Keep progress visible

---

**This template is ready to use. Clone it for each new project you want to explore!**
