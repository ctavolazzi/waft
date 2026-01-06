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

1. **Project Structure Analysis**
   - Map directory structure and organization
   - Identify main entry points
   - Find configuration files
   - Locate test directories
   - Check for documentation structure

2. **Codebase Architecture**
   - Identify core modules/packages
   - Map component relationships
   - Understand data flow
   - Find integration points
   - Identify abstraction layers

3. **Dependency Analysis**
   - List external dependencies
   - Map internal dependencies
   - Identify circular dependencies (if any)
   - Understand dependency graph
   - Check for unused dependencies

4. **Pattern Discovery**
   - Identify coding patterns and conventions
   - Find design patterns in use
   - Understand naming conventions
   - Discover architectural patterns
   - Note any anti-patterns

5. **Key Functionality Mapping**
   - Locate main features/commands
   - Find critical paths
   - Identify core algorithms
   - Map user-facing functionality
   - Find extension points

6. **Documentation & Knowledge**
   - Read key documentation files
   - Check for architecture docs
   - Find API documentation
   - Locate design decisions
   - Review recent changes/commits

7. **Testing & Quality**
   - Understand test structure
   - Identify test coverage areas
   - Find test patterns
   - Check for quality tools/configs
   - Review test results if available

8. **Integration Points**
   - Find external integrations
   - Identify API boundaries
   - Map data sources/sinks
   - Understand plugin/extensibility points
   - Find configuration mechanisms

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

## Codebase Search Queries

Use semantic search to understand:

1. **"How does the main application entry point work?"**
2. **"What is the core architecture and how are components organized?"**
3. **"How do different modules interact with each other?"**
4. **"What are the main data structures and how is data passed around?"**
5. **"Where are configuration and settings managed?"**
6. **"How does error handling work across the codebase?"**
7. **"What patterns are used for logging and monitoring?"**
8. **"How are external dependencies integrated?"**

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
3. `draft plan` → Create initial plan based on understanding
4. `critique plan` → Review and refine plan
5. `finalize plan` → Lock in the plan
6. `begin` → Start implementation

**After explore, you should:**
- Understand the codebase structure
- Know where key functionality lives
- Understand component relationships
- Be ready to draft a plan

## Notes

- Use semantic search for understanding relationships
- Create diagrams when helpful (mermaid)
- Focus on understanding, not implementation
- Note patterns and conventions
- Identify areas that need deeper investigation
- Document assumptions that need validation

---

**Related:** See `PROJECT_STARTUP_PROCEDURE.md` for detailed exploration techniques.

