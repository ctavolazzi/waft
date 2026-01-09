# Verification Checks Catalog

**Purpose**: Catalog of all available verification checks with methods and expected outcomes.

**Last Updated**: 2026-01-07

---

## Check Categories

### 1. Environment Verification

#### Check: Date/Time Accuracy
- **ID**: `env-date-time`
- **Method**: Run `date` command
- **Expected**: Current date/time matches system
- **Evidence**: Command output with timestamp
- **Frequency**: Once per session or when time-sensitive

#### Check: Disk Space Availability
- **ID**: `env-disk-space`
- **Method**: Run `df -h . | tail -1`
- **Expected**: Sufficient space for operations
- **Evidence**: Available space, usage percentage
- **Frequency**: When performing large operations

#### Check: Working Directory
- **ID**: `env-working-dir`
- **Method**: Run `pwd`
- **Expected**: Correct project directory
- **Evidence**: Actual path vs expected
- **Frequency**: When context might have changed

---

### 2. Project State Verification

#### Check: Project Structure Validity
- **ID**: `project-structure`
- **Method**: Run `waft verify` (if waft project)
- **Expected**: Structure is valid
- **Evidence**: Integrity percentage, missing components
- **Frequency**: After structural changes

#### Check: Git Repository State
- **ID**: `git-state`
- **Method**: Run `git status`
- **Expected**: Repository exists and is accessible
- **Evidence**: Branch, uncommitted changes, commits ahead/behind
- **Frequency**: Before/after git operations

#### Check: Project Version
- **ID**: `project-version`
- **Method**: Read `pyproject.toml` or equivalent
- **Expected**: Version matches claims
- **Evidence**: Actual version vs claimed
- **Frequency**: When version is mentioned

---

### 3. Tool Availability Verification

#### Check: Required CLI Tools
- **ID**: `tools-cli`
- **Method**: Run `which <tool>` or `command -v <tool>`
- **Expected**: Tools are in PATH
- **Evidence**: Tool paths, versions
- **Frequency**: When tools are needed

#### Check: MCP Servers Operational
- **ID**: `tools-mcp`
- **Method**: Test MCP server availability
- **Expected**: Servers respond
- **Evidence**: Server status, errors
- **Frequency**: When MCP operations fail

#### Check: Runtime Versions
- **ID**: `tools-runtime`
- **Method**: Run `python --version`, `node --version`, etc.
- **Expected**: Versions match requirements
- **Evidence**: Actual versions vs required
- **Frequency**: When version compatibility matters

---

### 4. File/Directory Verification

#### Check: File Existence
- **ID**: `file-exists`
- **Method**: Run `test -f <path>` or `Path(path).exists()`
- **Expected**: Files exist at claimed locations
- **Evidence**: File existence, size, modification time
- **Frequency**: When files are referenced

#### Check: Directory Existence
- **ID**: `dir-exists`
- **Method**: Run `test -d <path>` or `Path(path).is_dir()`
- **Expected**: Directories exist
- **Evidence**: Directory existence, contents count
- **Frequency**: When directories are referenced

#### Check: File Content Matches
- **ID**: `file-content`
- **Method**: Read file and verify specific claims
- **Expected**: Content matches what was claimed
- **Evidence**: File content excerpts
- **Frequency**: When file content is claimed

---

### 5. Configuration Verification

#### Check: Configuration Values
- **ID**: `config-values`
- **Method**: Read config files (pyproject.toml, package.json, .env, etc.)
- **Expected**: Values match claims
- **Evidence**: Config file content
- **Frequency**: When config is mentioned

#### Check: Environment Variables
- **ID**: `config-env`
- **Method**: Check `os.getenv()` or `process.env`
- **Expected**: Variables set as claimed
- **Evidence**: Environment dump (sanitized)
- **Frequency**: When env vars are needed

---

### 6. Dependency Verification

#### Check: Dependencies Installed
- **ID**: `deps-installed`
- **Method**: Check lock files, package lists, or import tests
- **Expected**: Dependencies match claims
- **Evidence**: Dependency list
- **Frequency**: When dependencies are mentioned

#### Check: Dependency Versions
- **ID**: `deps-versions`
- **Method**: Check version pins in lock files
- **Expected**: Versions match claims
- **Evidence**: Version information
- **Frequency**: When versions matter

---

### 7. Work Effort Verification

#### Check: Active Work Efforts
- **ID**: `work-active`
- **Method**: Call `mcp_work-efforts_list_work_efforts` with status="active"
- **Expected**: Work efforts match claims
- **Evidence**: MCP response
- **Frequency**: When work efforts are mentioned

#### Check: Work Effort Details
- **ID**: `work-details`
- **Method**: Read work effort files or query MCP
- **Expected**: Details match claims
- **Evidence**: Work effort content
- **Frequency**: When specific work effort is referenced

---

### 8. GitHub State Verification

#### Check: Repository Exists
- **ID**: `github-repo`
- **Method**: Call `mcp_github_get_file_contents` or `gh repo view`
- **Expected**: Repository accessible
- **Evidence**: GitHub API response
- **Frequency**: When repository is mentioned

#### Check: Recent Commits
- **ID**: `github-commits`
- **Method**: Call `mcp_github_list_commits` (last 5-10)
- **Expected**: Commits match claims
- **Evidence**: GitHub API response
- **Frequency**: When commits are referenced

#### Check: Open Issues/PRs
- **ID**: `github-issues-prs`
- **Method**: Call `mcp_github_list_issues` and `mcp_github_list_pull_requests`
- **Expected**: Counts match claims
- **Evidence**: GitHub API response
- **Frequency**: When issues/PRs are mentioned

---

## Adding New Checks

To add a new check:

1. **Identify Need**: What needs verification?
2. **Design Method**: How can we verify it?
3. **Add Entry**: Add to this catalog
4. **Update Command**: Add to `.cursor/commands/verify.md`
5. **Test**: Run verification and document trace

---

## Check Priority

**High Priority** (verify frequently):
- Date/Time
- Working Directory
- Project Version
- File Existence

**Medium Priority** (verify when relevant):
- Git State
- Tool Availability
- Configuration Values
- Dependencies

**Low Priority** (verify on demand):
- MCP Servers
- Work Efforts
- GitHub State
- File Content

---

**This catalog grows as new verification needs are identified.**
