# Explore

Deep dive into codebase structure, architecture, and relationships.

**Use after:** `spin-up` (get oriented first)
**Use before:** `draft plan` (understand before planning)

## Purpose

While `spin-up` gives you the current state and status, `explore` helps you understand:
- How the codebase is structured
- How components interact
- What patterns and conventions exist
- Where key functionality lives
- What dependencies and relationships exist

## Steps

**CRITICAL**: Use the tools at your disposal during exploration:
- **Empirica**: Create sessions, log findings/unknowns, track epistemic state
- **_pyrite**: Document discoveries in `_pyrite/active/` as you explore
- **MCP Servers**: Use work-efforts, docs-maintainer, github, memory, etc.
- **Waft Commands**: Use `waft info`, `waft verify`, `waft stats` to understand project state
- **Git**: Review history, understand evolution, find patterns

1. **Project Structure Analysis**
   - Map directory structure and organization
   - Identify main entry points
   - Find configuration files
   - Locate test directories
   - Check for documentation structure
   - **Use**: `waft info`, `waft verify`, file system exploration
   - **Document**: Findings in `_pyrite/active/YYYY-MM-DD_exploration_structure.md`
   - **Log**: "Discovered project structure: X directories, Y main entry points" via `waft finding log`

2. **Codebase Architecture**
   - Identify core modules/packages
   - Map component relationships
   - Understand data flow
   - Find integration points
   - Identify abstraction layers
   - **Use**: Semantic codebase search, code reading, dependency analysis
   - **Document**: Architecture diagram/notes in `_pyrite/active/`
   - **Log**: "Identified core components: X, Y, Z" via `waft finding log`
   - **Use MCP**: `mcp_docs-maintainer_search_docs` to find architecture docs

3. **Dependency Analysis**
   - List external dependencies
   - Map internal dependencies
   - Identify circular dependencies (if any)
   - Understand dependency graph
   - Check for unused dependencies
   - **Use**: `pyproject.toml` analysis, import tracing, `waft info`
   - **Log**: "Found X external dependencies, Y internal modules" via `waft finding log`
   - **Use MCP**: `mcp_github_search_code` to find dependency usage patterns

4. **Pattern Discovery**
   - Identify coding patterns and conventions
   - Find design patterns in use
   - Understand naming conventions
   - Discover architectural patterns
   - Note any anti-patterns
   - **Use**: Codebase search, pattern matching, code review
   - **Document**: Patterns found in `_pyrite/active/`
   - **Log**: "Discovered pattern: X used in Y places" via `waft finding log`
   - **Use MCP**: `mcp_memory_create_entities` to track patterns as knowledge

5. **Key Functionality Mapping**
   - Locate main features/commands
   - Find critical paths
   - Identify core algorithms
   - Map user-facing functionality
   - Find extension points
   - **Use**: `waft --help`, command exploration, entry point analysis
   - **Document**: Feature map in `_pyrite/active/`
   - **Log**: "Mapped X features, Y commands, Z extension points" via `waft finding log`
   - **Use MCP**: `mcp_work-efforts_list_work_efforts` to see what's being worked on

6. **Documentation & Knowledge**
   - Read key documentation files
   - Check for architecture docs
   - Find API documentation
   - Locate design decisions
   - Review recent changes/commits
   - **Use**: `mcp_docs-maintainer_search_docs`, `mcp_github_get_file_contents`
   - **Use**: `waft info` to see project state
   - **Document**: Key docs found in `_pyrite/active/`
   - **Log**: "Found X docs, Y design decisions" via `waft finding log`
   - **Use MCP**: `mcp_memory_search_nodes` to find related knowledge

7. **Testing & Quality**
   - Understand test structure
   - Identify test coverage areas
   - Find test patterns
   - Check for quality tools/configs
   - Review test results if available
   - **Use**: Run `waft verify`, check test directories, run tests
   - **Use**: `uv run pytest tests/ -v` to see test structure
   - **Document**: Test findings in `_pyrite/active/`
   - **Log**: "Test structure: X tests, Y coverage areas" via `waft finding log`

8. **Integration Points**
   - Find external integrations
   - Identify API boundaries
   - Map data sources/sinks
   - Understand plugin/extensibility points
   - Find configuration mechanisms
   - **Use**: Codebase search for "integration", "api", "plugin"
   - **Use MCP**: `mcp_github_search_code` to find integration code
   - **Document**: Integration map in `_pyrite/active/`
   - **Log**: "Found X integrations, Y API boundaries" via `waft finding log`

## Commands

```bash
# Project structure
find . -type d -name "__pycache__" -prune -o -type f -print | head -50
tree -L 3 -I '__pycache__|*.pyc|.git' 2>/dev/null || find . -maxdepth 3 -type d | head -30

# Entry points
find . -name "main.py" -o -name "__main__.py" -o -name "cli.py" | head -10
grep -r "if __name__" --include="*.py" | head -10

# Configuration files
find . -name "*.toml" -o -name "*.yaml" -o -name "*.yml" -o -name "*.json" | grep -v node_modules | head -20

# Dependencies
grep -r "^import\|^from" --include="*.py" | head -50
cat pyproject.toml | grep -A 20 "\[project\]" | grep -E "dependencies|requires"

# Test structure
find tests -type f -name "*.py" 2>/dev/null | head -20
find . -name "conftest.py" -o -name "pytest.ini" -o -name "setup.cfg"

# Documentation
find . -name "README*.md" -o -name "ARCHITECTURE*.md" -o -name "DESIGN*.md" | head -10
ls -lt *.md _work_efforts/*.md 2>/dev/null | head -10

# Recent changes
git log --oneline --graph -20
git log --stat -5
```

## Active Tool Usage During Exploration

### Empirica (Epistemic Tracking)

**Before starting exploration:**
```bash
# Create session for exploration
waft session create --ai-id waft --type exploration

# Submit preflight assessment
# (Use EmpiricaManager or waft commands if available)
```

**During exploration:**
```bash
# Log discoveries as you find them
waft finding log "Discovered X architecture pattern" --impact 0.7
waft finding log "Found Y integration points" --impact 0.6
waft unknown log "Need to investigate Z component"

# Check epistemic state
waft assess
waft stats
```

**After exploration:**
```bash
# Submit postflight assessment
# Document what you learned
waft finding log "Exploration complete: understood X, Y, Z" --impact 0.8
```

### _pyrite (Memory Layer)

**Create exploration documents as you go:**
- `_pyrite/active/YYYY-MM-DD_exploration_structure.md` - Project structure findings
- `_pyrite/active/YYYY-MM-DD_exploration_architecture.md` - Architecture discoveries
- `_pyrite/active/YYYY-MM-DD_exploration_patterns.md` - Patterns found
- `_pyrite/active/YYYY-MM-DD_exploration_integrations.md` - Integration points

**Use MemoryManager programmatically:**
```python
from waft.core.memory import MemoryManager
memory = MemoryManager(project_path)
# Add files to active/ as you discover things
# Organize findings in _pyrite structure
```

### MCP Servers

**Work Efforts MCP:**
- `mcp_work-efforts_list_work_efforts` - See what's being worked on
- `mcp_work-efforts_list_tickets` - Understand current priorities
- `mcp_work-efforts_search_work_efforts` - Find related work

**Docs Maintainer MCP:**
- `mcp_docs-maintainer_search_docs` - Find relevant documentation
- `mcp_docs-maintainer_check_health` - Understand doc state

**GitHub MCP:**
- `mcp_github_search_code` - Find code patterns
- `mcp_github_get_file_contents` - Read key files
- `mcp_github_list_commits` - Understand evolution

**Memory MCP:**
- `mcp_memory_search_nodes` - Find related knowledge
- `mcp_memory_create_entities` - Track discoveries
- `mcp_memory_create_relations` - Map relationships

**Filesystem MCP:**
- `mcp_filesystem_directory_tree` - Visualize structure
- `mcp_filesystem_search_files` - Find files by pattern

### Waft Commands

**Use waft to understand the project:**
```bash
waft info          # Project information
waft verify        # Check structure health
waft stats         # Gamification state
waft level         # Level progress
waft achievements  # Unlocked achievements
```

**Use waft to explore:**
- Run `waft --help` to see all commands
- Try commands in test projects
- Use `waft demo.py` to see capabilities

## Codebase Search Queries

Use semantic search to understand:

1. **"How does the main application entry point work?"**
   - **Log finding**: "Main entry point: X, handles Y"
   - **Document**: In `_pyrite/active/`

2. **"What is the core architecture and how are components organized?"**
   - **Create entities**: Use `mcp_memory_create_entities` for components
   - **Create relations**: Use `mcp_memory_create_relations` for relationships
   - **Log finding**: "Architecture: X pattern, Y components"

3. **"How do different modules interact with each other?"**
   - **Document**: Interaction map in `_pyrite/active/`
   - **Log finding**: "Module interactions: X → Y → Z"

4. **"What are the main data structures and how is data passed around?"**
   - **Log finding**: "Data flow: X structure, Y transformations"
   - **Document**: Data flow diagram

5. **"Where are configuration and settings managed?"**
   - **Use**: `mcp_filesystem_search_files` for config files
   - **Log finding**: "Config: X files, Y locations"

6. **"How does error handling work across the codebase?"**
   - **Use**: `mcp_github_search_code` for error handling patterns
   - **Log finding**: "Error handling: X pattern used in Y places"

7. **"What patterns are used for logging and monitoring?"**
   - **Document**: Patterns in `_pyrite/active/`
   - **Log finding**: "Logging pattern: X"

8. **"How are external dependencies integrated?"**
   - **Use**: `mcp_github_search_code` for integration code
   - **Log finding**: "Integrations: X services, Y APIs"

## Output Format

Provide a structured exploration report:

### 1. Project Structure
- Directory organization
- Main entry points
- Configuration locations
- Test structure

### 2. Architecture Overview
- Core components
- Component relationships (diagram if helpful)
- Data flow
- Integration points

### 3. Dependencies
- External dependencies (key ones)
- Internal dependency graph
- Critical dependencies

### 4. Patterns & Conventions
- Coding patterns observed
- Naming conventions
- Architectural patterns
- Design decisions

### 5. Key Functionality
- Main features/commands
- Critical paths
- Core algorithms
- Extension points

### 6. Integration Points
- External services/APIs
- Plugin systems
- Configuration mechanisms
- Data sources/sinks

### 7. Testing & Quality
- Test structure
- Coverage areas
- Quality tools
- Test patterns

### 8. Documentation
- Key docs found
- Architecture decisions
- API documentation
- Design rationale

### 9. Insights & Observations
- Interesting patterns
- Potential issues
- Areas of complexity
- Opportunities for improvement

### 10. Questions & Unknowns
- What needs clarification
- Areas requiring deeper investigation
- Assumptions that need validation

## Integration with Workflow

**Sequence:**
1. `spin-up` → Get oriented (status, active work, recent changes)
2. `explore` → Understand structure and architecture ← **YOU ARE HERE**
   - **Use Empirica**: Create session, log findings/unknowns
   - **Use _pyrite**: Document discoveries as you explore
   - **Use MCPs**: Search docs, find code, track work
   - **Use waft**: Verify structure, check stats, understand project
3. `draft plan` → Create initial plan based on understanding
4. `critique plan` → Review and refine plan
5. `finalize plan` → Lock in the plan
6. `begin` → Start implementation

**After explore, you should:**
- Understand the codebase structure
- Know where key functionality lives
- Understand component relationships
- Have findings logged in Empirica
- Have discoveries documented in `_pyrite/active/`
- Have used MCPs to gather information
- Be ready to draft a plan

## Tool Usage Checklist

As you explore, actively use:

- [ ] **Empirica**: Created session, logged findings, tracked unknowns
- [ ] **_pyrite**: Created exploration docs in `_pyrite/active/`
- [ ] **MCP work-efforts**: Checked active work, searched related efforts
- [ ] **MCP docs-maintainer**: Searched documentation, checked health
- [ ] **MCP github**: Searched code, read files, reviewed commits
- [ ] **MCP memory**: Created entities/relations for discoveries
- [ ] **MCP filesystem**: Explored structure, found files
- [ ] **Waft commands**: Used `waft info`, `waft verify`, `waft stats`
- [ ] **Git**: Reviewed history, understood evolution
- [ ] **Semantic search**: Asked questions, found relationships

## Notes

- **Actively use tools** - Don't just read code, use Empirica, _pyrite, MCPs
- **Document as you go** - Create `_pyrite/active/` files during exploration
- **Log findings** - Use `waft finding log` for discoveries
- **Track unknowns** - Use `waft unknown log` for gaps
- **Use semantic search** - For understanding relationships
- **Create diagrams** - When helpful (mermaid)
- **Focus on understanding** - Not implementation yet
- **Note patterns** - And conventions
- **Identify areas** - That need deeper investigation
- **Document assumptions** - That need validation
- **Use MCPs proactively** - Don't wait, use them to gather information
- **Check work efforts** - Understand what's being worked on
- **Review documentation** - Use docs-maintainer MCP
- **Explore code** - Use github MCP to search and read
- **Track knowledge** - Use memory MCP for entities and relations

---

**Related:** See `PROJECT_STARTUP_PROCEDURE.md` for detailed exploration techniques.

