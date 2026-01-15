---
name: Waft CLI Enhancement via GitHub
overview: ""
todos: []

category: hopes
confidence: 0.87
constellation_date: 2026-01-14
---

# Waft CLI Enhancement via GitHub Learning Journey

## Overview

This plan will enhance and refactor the waft CLI while using GitHub features extensively to document the process. Each enhancement will be tracked through commits, PRs, GitHub Actions, Projects, and the Wiki.

## Phase 1: GitHub Repository Setup

### 1.1 Repository Configuration

- **File**: Check current git remote configuration
- **Action**: Set up proper `waft` repository on GitHub (https://github.com/ctavolazzi/waft)
- **GitHub Feature**: Initial repository setup
- **Learning**: Repository creation, remote configuration, initial commit strategy

### 1.2 Repository Structure

- **Files**: `.github/` directory structure
- **Actions**: 
- Create `.github/ISSUE_TEMPLATE/` for bug reports and feature requests
- Create `.github/PULL_REQUEST_TEMPLATE.md` for PR standardization
- Set up branch protection rules (via GitHub UI)
- **GitHub Feature**: Issue templates, PR templates
- **Learning**: GitHub repository best practices

## Phase 2: GitHub Actions CI/CD Enhancement

### 2.1 Enhance Existing CI Workflow

- **File**: `.github/workflows/ci.yml` (currently in templates, needs to exist in waft repo)
- **Actions**:
- Add comprehensive test matrix (Python 3.10, 3.11, 3.12)
- Add linting with ruff
- Add type checking (if we add mypy)
- Add security scanning
- Add code coverage reporting
- **GitHub Feature**: GitHub Actions workflows
- **Learning**: CI/CD pipelines, matrix builds, artifact management

### 2.2 Release Automation

- **File**: `.github/workflows/release.yml` (new)
- **Actions**:
- Automated version bumping
- Automated changelog generation
- Automated release creation
- Automated package publishing (if applicable)
- **GitHub Feature**: Releases, GitHub Actions automation
- **Learning**: Release management, semantic versioning

## Phase 3: CLI Enhancement - New Features

### 3.1 GitHub Integration Commands

- **File**: `src/waft/main.py`, `src/waft/core/github.py` (new)
- **New Commands**:
- `waft github init` - Initialize GitHub repository for project
- `waft github status` - Show GitHub repository status
- `waft github create-pr` - Create a pull request (interactive)
- `waft github sync` - Sync local changes with GitHub
- **GitHub Feature**: GitHub API integration, PRs
- **Learning**: GitHub API, authentication, PR workflows
- **Implementation**: Use PyGithub or GitHub CLI integration

### 3.2 Enhanced Project Management

- **File**: `src/waft/main.py`, `src/waft/core/project.py` (new)
- **New Commands**:
- `waft project create` - Enhanced project creation with GitHub integration
- `waft project migrate` - Migrate existing projects to waft structure
- `waft project health` - Health check with scoring
- **GitHub Feature**: Project management
- **Learning**: Project organization

### 3.3 Documentation Commands

- **File**: `src/waft/main.py`, `src/waft/core/docs.py` (new)
- **New Commands**:
- `waft docs generate` - Generate documentation
- `waft docs publish` - Publish to GitHub Wiki
- `waft docs sync` - Sync local docs with Wiki
- **GitHub Feature**: Wiki integration
- **Learning**: GitHub Wiki, documentation workflows

## Phase 4: CLI Refactoring

### 4.1 Code Structure Improvements

- **Files**: 
- `src/waft/main.py` - Split into command modules
- `src/waft/commands/` (new directory)
    - `__init__.py`
    - `new.py`
    - `verify.py`
    - `github.py`
    - `project.py`
    - `docs.py`
- **Actions**:
- Extract commands into separate modules
- Improve error handling
- Add comprehensive logging
- Add configuration management
- **GitHub Feature**: Commits with proper messages
- **Learning**: Code organization, maintainability

### 4.2 Testing Infrastructure

- **Files**: 
- `tests/` directory (new)
- `tests/test_commands.py`
- `tests/test_core.py`
- `tests/test_github.py`
- `pytest.ini` or `pyproject.toml` test config
- **Actions**:
- Add pytest test suite
- Add integration tests
- Add GitHub API mocking for tests
- **GitHub Feature**: Test results in Actions
- **Learning**: Testing best practices, CI integration

### 4.3 Error Handling & Validation

- **Files**: `src/waft/core/errors.py` (new), update all command files
- **Actions**:
- Create custom exception hierarchy
- Add input validation
- Improve error messages
- Add retry logic for network operations
- **GitHub Feature**: Error tracking via Issues
- **Learning**: Error handling patterns

## Phase 5: GitHub Projects & Organization

### 5.1 Project Board Setup

- **Action**: Create GitHub Project board
- **Structure**:
- Columns: Backlog, In Progress, Review, Done
- Link issues and PRs to project
- Use automation for status updates
- **GitHub Feature**: GitHub Projects
- **Learning**: Project management with GitHub Projects

### 5.2 Issue Management

- **Files**: `.github/ISSUE_TEMPLATE/` (from Phase 1)
- **Actions**:
- Create issues for each enhancement
- Link issues to project board
- Use labels for categorization
- Create milestones for phases
- **GitHub Feature**: Issues, Labels, Milestones
- **Learning**: Issue tracking, project planning

## Phase 6: Documentation & Wiki

### 6.1 Wiki Setup

- **Action**: Initialize GitHub Wiki
- **Content**:
- Architecture documentation
- Command reference
- Development guide
- Contributing guide
- GitHub workflow guide (meta-documentation)
- **GitHub Feature**: Wiki
- **Learning**: Wiki organization, documentation practices

### 6.2 Wiki Automation

- **File**: `src/waft/core/docs.py` (from Phase 3.3)
- **Actions**:
- Auto-generate command docs from code
- Sync documentation to Wiki
- Version control for Wiki (via git)
- **GitHub Feature**: Wiki API integration
- **Learning**: Documentation automation

## Phase 7: Pull Request Workflow

### 7.1 PR Strategy

- **Action**: Create feature branches for each enhancement
- **Workflow**:

1. Create branch: `feature/github-integration`
2. Make changes
3. Create PR with template
4. Run CI checks
5. Review process
6. Merge with squash/merge commit

- **GitHub Feature**: PRs, branch protection, reviews
- **Learning**: PR workflows, code review process

### 7.2 PR Templates & Automation

- **File**: `.github/PULL_REQUEST_TEMPLATE.md`
- **Actions**:
- Create comprehensive PR template
- Add PR automation (auto-assign, labels)
- Add PR checks (linting, tests)
- **GitHub Feature**: PR templates, automation
- **Learning**: PR best practices

## Implementation Strategy

### Commit Strategy

- **Conventional Commits**: Use conventional commit format
- `feat:` for new features
- `refactor:` for refactoring
- `fix:` for bug fixes
- `docs:` for documentation
- `test:` for tests
- `chore:` for maintenance
- **Small, focused commits**: One logical change per commit
- **Descriptive messages**: Clear, actionable commit messages

### Branch Strategy

- **Main branch**: `main` (protected)
- **Feature branches**: `feature/<name>`
- **Fix branches**: `fix/<name>`
- **Release branches**: `release/<version>` (if needed)

### PR Process

1. Create feature branch from `main`
2. Make changes with descriptive commits
3. Push branch and create PR
4. PR triggers CI checks
5. Address review feedback
6. Merge after approval

## Files to Create/Modify

### New Files

- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/feature_request.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/workflows/release.yml`
- `src/waft/core/github.py`
- `src/waft/core/project.py`
- `src/waft/core/docs.py`
- `src/waft/core/errors.py`
- `src/waft/commands/__init__.py`
- `src/waft/commands/new.py`
- `src/waft/commands/verify.py`
- `src/waft/commands/github.py`