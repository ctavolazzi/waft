---
name: Install and Integrate tldr Pages
overview: Install tldr client via pipx and integrate it into the WAFT project, potentially creating tldr pages for WAFT commands to provide simplified, example-driven command documentation.
todos:
  - id: install_tldr
    content: "Install tldr client via pipx: `pipx install tldr`"
    status: pending
  - id: verify_installation
    content: Verify tldr installation and test with example command
    status: pending
  - id: create_structure
    content: Create tldr-pages directory structure for local pages
    status: pending
  - id: create_waft_pages
    content: Create initial tldr pages for core WAFT commands (new, verify, sync, add, info, serve)
    status: pending
  - id: configure_tldr
    content: Configure tldr to use local pages directory via TLDR_PAGES_DIR
    status: pending
  - id: test_local_pages
    content: Test local tldr pages work correctly
    status: pending
  - id: document_setup
    content: Create docs/TLDR_SETUP.md with installation and usage instructions
    status: pending
  - id: update_readme
    content: Update README.md with tldr installation and usage section
    status: pending

category: hopes
confidence: 1.00
constellation_date: 2026-01-14
---

# Install and Integrate tldr Pages

## Overview

Install the tldr (simplified man pages) client and integrate it into the WAFT project. This will provide quick, example-driven command documentation that complements the existing `.cursor/commands/*.md` files.

## Current State

- WAFT has extensive command documentation in `.cursor/commands/` (70+ command files)
- Commands are documented in markdown format with detailed usage
- No tldr client currently installed
- No tldr pages structure exists

## Installation Steps

### 1. Install tldr Client

- Install via pipx (recommended method): `pipx install tldr`
- Verify installation: `tldr --version`
- Test with example: `tldr tar` (should show tar examples)

### 2. Create tldr Pages Structure

- Create directory: `tldr-pages/` or `docs/tldr/` in project root
- Follow tldr page format (markdown with specific structure)
- Structure: `tldr-pages/common/` for common commands, `tldr-pages/waft/` for WAFT-specific

### 3. Configure tldr to Use Local Pages

- Set `TLDR_PAGES_DIR` environment variable to point to local pages
- Or configure tldr to use both community and local pages
- Document configuration in project README or setup docs

### 4. Create Initial tldr Pages (Optional)

Convert key WAFT commands to tldr format:

- `waft new` - Create new project
- `waft verify` - Verify project structure
- `waft sync` - Sync dependencies
- `waft add` - Add dependency
- `waft info` - Show project info
- `waft serve` - Start web dashboard

## Files to Create/Modify

### New Files

- `tldr-pages/common/waft.md` - Main waft command examples
- `tldr-pages/common/waft-new.md` - waft new examples
- `tldr-pages/common/waft-verify.md` - waft verify examples
- `tldr-pages/common/waft-sync.md` - waft sync examples
- `tldr-pages/common/waft-add.md` - waft add examples
- `tldr-pages/common/waft-info.md` - waft info examples
- `tldr-pages/common/waft-serve.md` - waft serve examples
- `docs/TLDR_SETUP.md` - Setup and usage documentation

### Modified Files

- `README.md` - Add tldr installation and usage section
- `.cursor/rules/mcp-integration.mdc` or `AGENTS.md` - Document tldr integration (if relevant)

## tldr Page Format

Each tldr page follows this structure:

```markdown
# waft

Create and manage WAFT projects.

- Create a new project:
  waft new my_project

- Verify project structure:
  waft verify

- Sync dependencies:
  waft sync

- Add a dependency:
  waft add pytest

- Show project info:
  waft info

- Start web dashboard:
  waft serve
```

## Integration Options

### Option A: Local Pages Only

- Store tldr pages in project
- Configure tldr to use local pages directory
- Good for: Project-specific commands only

### Option B: Hybrid (Community + Local)

- Use community tldr pages for standard commands
- Use local pages for WAFT-specific commands
- Good for: Best of both worlds

### Option C: Contribute to Community

- Create tldr pages following community format
- Submit PR to tldr-pages repository
- Good for: Sharing with community

## Verification Steps

1. Install tldr: `pipx install tldr`
2. Test community pages: `tldr tar`
3. Configure local pages: Set `TLDR_PAGES_DIR`
4. Test local pages: `tldr waft`
5. Verify examples work: Run actual commands

## Documentation

Create `docs/TLDR_SETUP.md` with:

- Installation instructions
- Configuration steps
- How to use tldr with WAFT
- How to create new tldr pages
- Contributing guidelines

## Next Steps (Future)

- Convert more WAFT commands to tldr format
- Create tldr pages for Cursor commands (if applicable)
- Integrate tldr into help system
- Add tldr page generation to documentation workflow