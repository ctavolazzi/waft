# Deep Analyze

**Deep code analysis workflow - extract algorithms, patterns, and code structures from GitHub repositories.**

Performs comprehensive analysis of GitHub repositories by searching code, reading source files, extracting algorithms and patterns, and creating detailed analysis documents. Transforms repository exploration into actionable code patterns and reusable algorithms.

**Use when:** You need to deeply understand codebases, extract algorithms, identify patterns, or prepare code for integration into your project.

---

## Purpose

This command provides:
- **Code Search**: Semantic and exact code search across repositories
- **File Analysis**: Deep reading of source files and data structures
- **Algorithm Extraction**: Identifies and documents algorithms from code
- **Pattern Recognition**: Discovers code patterns and architectural structures
- **Documentation Generation**: Creates comprehensive analysis documents
- **Integration Planning**: Identifies opportunities for code reuse

---

## Philosophy

1. **Go Deep**: Read actual source code, not just READMEs
2. **Extract Algorithms**: Document formulas, calculations, and logic
3. **Find Patterns**: Identify reusable code patterns and structures
4. **Document Everything**: Create detailed analysis documents
5. **Actionable Output**: Generate code snippets ready for integration

---

## Execution Phases

### Deep Analyze 1.1: Repository Discovery
**Purpose**: Identify repositories to analyze

**Steps**:
1. Get list of GitHub URLs or repository identifiers
2. Extract owner/repo names from URLs
3. Verify repositories exist and are accessible
4. Prioritize repositories by relevance
5. Create work effort structure (if using work efforts system)

**Output**: List of repositories ready for analysis

---

### Deep Analyze 1.2: Code Search & Discovery
**Purpose**: Find relevant code files and patterns

**Steps**:
1. Search for key concepts (e.g., "game state", "character", "combat")
2. Search for algorithms (e.g., "dice roll", "stat calculation", "damage")
3. Search for data structures (e.g., "class", "spell", "monster")
4. Search for patterns (e.g., "state management", "inventory", "save system")
5. Use GitHub code search with `repo:owner/repo` syntax
6. Use web search for additional context and documentation

**Tools Used**:
- `mcp_github_search_code` - Search code across repositories
- `web_search` - Find documentation and context
- `mcp_github_list_commits` - Understand recent activity

**Output**: List of relevant files and code patterns found

---

### Deep Analyze 1.3: Source File Reading
**Purpose**: Read actual source code files

**Steps**:
1. Read key source files identified in search
2. Read data structure files (JSON, YAML, etc.)
3. Read configuration files
4. Read test files for usage examples
5. Use direct file access via GitHub API or curl
6. Read large files in chunks if needed

**Tools Used**:
- `mcp_github_get_file_contents` - Read files from GitHub
- `run_terminal_cmd` with `curl` - Direct file access
- `read_file` - Read local cached files

**Output**: Source code content for analysis

---

### Deep Analyze 1.4: Algorithm Extraction
**Purpose**: Extract algorithms and formulas from code

**Steps**:
1. Identify calculation functions
2. Extract formulas and equations
3. Document algorithm logic
4. Extract data transformation patterns
5. Identify state management algorithms
6. Extract validation and checking logic

**Key Algorithms to Look For**:
- Stat calculations (modifiers, bonuses)
- Dice rolling mechanics
- Combat calculations (attack, damage, AC)
- HP/MP calculations
- Save/load algorithms
- State serialization

**Output**: Documented algorithms with formulas and code examples

---

### Deep Analyze 1.5: Pattern Recognition
**Purpose**: Identify reusable code patterns

**Steps**:
1. Identify architectural patterns (MVC, adapter, factory)
2. Find data structure patterns (dataclasses, enums, dictionaries)
3. Discover state management patterns
4. Identify serialization patterns
5. Find error handling patterns
6. Discover testing patterns

**Patterns to Document**:
- State management (dataclass-based, property-based)
- Inventory systems (stacking, capacity)
- Save systems (checksums, versioning)
- Quest systems (objective tracking)
- Equipment systems (slot-based, stat aggregation)

**Output**: Documented patterns with code examples

---

### Deep Analyze 1.6: Data Structure Analysis
**Purpose**: Understand data models and schemas

**Steps**:
1. Analyze JSON data structures
2. Identify entity relationships
3. Document field meanings and types
4. Extract validation rules
5. Identify data access patterns
6. Document data transformation flows

**Data Structures to Analyze**:
- Character/actor data models
- Spell/item/monster definitions
- Game state structures
- Inventory structures
- Quest/objective structures

**Output**: Documented data structures with schemas

---

### Deep Analyze 1.7: Integration Opportunity Identification
**Purpose**: Find code ready for reuse

**Steps**:
1. Identify direct code reuse opportunities
2. Find algorithms ready to implement
3. Identify libraries to integrate
4. Find data sources to reference
5. Identify patterns to adopt
6. Document integration priorities

**Integration Categories**:
- **High Priority**: Critical algorithms, core patterns
- **Medium Priority**: Supporting systems, utilities
- **Low Priority**: Reference implementations, examples

**Output**: Prioritized integration opportunities

---

### Deep Analyze 1.8: Documentation Generation
**Purpose**: Create comprehensive analysis documents

**Steps**:
1. Create main analysis document with all findings
2. Create algorithm reference document
3. Create pattern catalog
4. Create data structure documentation
5. Create integration guide
6. Create index/navigation document
7. Update work effort files (if using work efforts)

**Document Structure**:
- Executive summary
- Algorithms extracted (with code)
- Patterns identified (with examples)
- Data structures analyzed
- Integration opportunities
- Code snippets ready to use
- Next steps

**Output**: Comprehensive analysis documents

---

## Execution Flow

```
Deep Analyze 1.1: Repository Discovery
  ↓
Deep Analyze 1.2: Code Search & Discovery
  ↓
Deep Analyze 1.3: Source File Reading
  ↓
Deep Analyze 1.4: Algorithm Extraction
  ↓
Deep Analyze 1.5: Pattern Recognition
  ↓
Deep Analyze 1.6: Data Structure Analysis
  ↓
Deep Analyze 1.7: Integration Opportunity Identification
  ↓
Deep Analyze 1.8: Documentation Generation
  ↓
✅ Complete - Analysis documents generated
```

---

## What Gets Analyzed

### Algorithms
- Calculation functions
- Formulas and equations
- State transformations
- Validation logic
- Data processing

### Patterns
- Architectural patterns
- Design patterns
- Code organization patterns
- State management patterns
- Serialization patterns

### Data Structures
- Entity models
- Configuration schemas
- Data relationships
- Validation rules
- Access patterns

### Integration Opportunities
- Direct code reuse
- Algorithm implementations
- Library integrations
- Data source references
- Pattern adoptions

---

## Output Format

### Console Output

The command provides progress updates as it runs:

```
🔍 Deep Analyze: Code Analysis & Algorithm Extraction

Deep Analyze 1.1: Repository Discovery... ✓
  ✓ Identified 3 repositories to analyze
  ✓ Created work effort structure

Deep Analyze 1.2: Code Search & Discovery... ✓
  ✓ Found 15 relevant code files
  ✓ Identified 8 key algorithms
  ✓ Discovered 5 code patterns

Deep Analyze 1.3: Source File Reading... ✓
  ✓ Read 12 source files
  ✓ Analyzed 3 data structure files
  ✓ Reviewed 2 configuration files

Deep Analyze 1.4: Algorithm Extraction... ✓
  ✓ Extracted 6 algorithms:
    1. Ability modifier calculation
    2. Proficiency bonus lookup
    3. AC calculation
    4. HP calculation
    5. Attack roll mechanics
    6. Saving throw mechanics

Deep Analyze 1.5: Pattern Recognition... ✓
  ✓ Identified 5 patterns:
    1. StatsAdapter (4-stat to 6-stat conversion)
    2. CharacterState (dataclass-based state)
    3. InventoryState (stackable items)
    4. SaveSystem (JSON with checksums)
    5. QuestTracker (objective-based)

Deep Analyze 1.6: Data Structure Analysis... ✓
  ✓ Analyzed 4 data structures:
    1. Character data model
    2. Spell data structure
    3. Monster stat block
    4. Equipment definitions

Deep Analyze 1.7: Integration Opportunity Identification... ✓
  ✓ Found 8 integration opportunities:
    1. [HIGH] StatsAdapter pattern
    2. [HIGH] Ability modifier algorithm
    3. [MEDIUM] Save system pattern
    4. [MEDIUM] Inventory system
    5. [LOW] UI patterns

Deep Analyze 1.8: Documentation Generation... ✓
  📄 Main analysis: DEEP_CODE_ANALYSIS_YYYY-MM-DD_ALGORITHMS_AND_PATTERNS.md
  📄 Algorithm reference: [algorithm-doc.md]
  📄 Pattern catalog: [pattern-doc.md]
  📄 Integration guide: [integration-doc.md]
  📄 Index: ANALYSIS_INDEX.md

✅ Deep Analyze Complete - Analysis documents ready
   📁 Output folder: _work_efforts/[work-effort-id]/
   📄 Main document: DEEP_CODE_ANALYSIS_*.md
   🎯 Next steps: Review analysis and begin integration
```

### Analysis Documents

The command generates:

1. **Main Analysis Document** (`DEEP_CODE_ANALYSIS_YYYY-MM-DD_ALGORITHMS_AND_PATTERNS.md`)
   - Complete algorithm extraction
   - Code patterns with examples
   - Data structure analysis
   - Integration opportunities
   - Ready-to-use code snippets

2. **Algorithm Reference** (if separate)
   - Formulas and calculations
   - Implementation examples
   - Usage patterns

3. **Pattern Catalog** (if separate)
   - Pattern descriptions
   - Code examples
   - Integration guidance

4. **Data Structure Documentation** (if separate)
   - Schema definitions
   - Field descriptions
   - Relationship maps

5. **Integration Guide** (if separate)
   - Prioritized opportunities
   - Implementation steps
   - Code snippets

6. **Analysis Index** (`ANALYSIS_INDEX.md`)
   - Navigation guide
   - Quick reference
   - Document locations

---

## Use Cases

### 1. Repository Analysis
**Scenario**: Need to understand a GitHub repository deeply

**Example**:
```
User: "/deep-analyze"
User: "Analyze these repos: https://github.com/user/repo1, https://github.com/user/repo2"
```

**Output**: Complete code analysis with algorithms and patterns extracted

---

### 2. Algorithm Extraction
**Scenario**: Need to extract specific algorithms from code

**Example**:
```
User: "/deep-analyze"
User: "Find dice rolling and stat calculation algorithms in ctavolazzi/AI-DnD"
```

**Output**: Documented algorithms with formulas and code examples

---

### 3. Pattern Discovery
**Scenario**: Want to find reusable code patterns

**Example**:
```
User: "/deep-analyze"
User: "Find state management and inventory patterns in these repos"
```

**Output**: Pattern catalog with code examples and integration guidance

---

### 4. Integration Planning
**Scenario**: Planning to integrate code from other projects

**Example**:
```
User: "/deep-analyze"
User: "Analyze 5e-bits/5e-database for data structure integration"
```

**Output**: Integration guide with prioritized opportunities

---

### 5. Learning & Documentation
**Scenario**: Learning from well-written codebases

**Example**:
```
User: "/deep-analyze"
User: "Deep dive into foundryvtt/dnd5e to understand VTT patterns"
```

**Output**: Comprehensive analysis document for reference

---

## Integration with Other Commands

- **`/explore`**: General exploration (`/deep-analyze` is code-focused analysis)
- **`/analyze`**: Project analysis (`/deep-analyze` is external repository analysis)
- **`/consider`**: Qualitative analysis (`/deep-analyze` is code extraction)
- **`/study`**: Learning and research (`/deep-analyze` is algorithmic extraction)

---

## When to Use

**Use `/deep-analyze` when**:
- ✅ Need to extract algorithms from code
- ✅ Want to identify reusable patterns
- ✅ Planning code integration
- ✅ Need to understand data structures
- ✅ Want documented code analysis
- ✅ Preparing for implementation

**Don't use `/deep-analyze` when**:
- ❌ Just need high-level overview (use `/explore`)
- ❌ Need quick status check (use `/checkpoint`)
- ❌ Analyzing your own project (use `/analyze`)
- ❌ Just browsing code (use GitHub directly)

---

## Technical Details

### Tools Used

**GitHub MCP**:
- `mcp_github_search_code` - Search code with queries
- `mcp_github_get_file_contents` - Read source files
- `mcp_github_list_commits` - Understand activity
- `mcp_github_list_issues` - Check project state

**Web Search**:
- Find documentation
- Discover related projects
- Understand context

**File Operations**:
- `read_file` - Read local/cached files
- `run_terminal_cmd` with `curl` - Direct file access
- `grep` - Search file contents

### Analysis Methods

- **Code Search**: Semantic and exact pattern matching
- **Algorithm Extraction**: Formula identification and documentation
- **Pattern Recognition**: Structural pattern analysis
- **Data Structure Analysis**: Schema extraction and documentation
- **Integration Planning**: Priority-based opportunity identification

### Performance

- **Total Time**: ~30-120 seconds (depending on repository size)
- **Code Search**: ~5-15 seconds per repository
- **File Reading**: ~10-30 seconds
- **Analysis**: ~10-40 seconds
- **Documentation**: ~5-15 seconds

### Error Handling

- **Repository Not Found**: Skip with warning, continue with others
- **File Access Errors**: Use alternative methods (curl, web search)
- **Rate Limits**: Wait and retry, or use alternative access
- **Large Files**: Read in chunks, summarize if too large
- **Analysis Errors**: Continue with available data, mark incomplete sections

---

## Example Workflow

```
User: "/deep-analyze"
User: "Analyze ctavolazzi/AI-DnD, 5e-bits/5e-database, foundryvtt/dnd5e"

AI: [Runs all 8 phases sequentially]

AI: ✅ Deep Analyze Complete
    - Repositories: 3 analyzed
    - Algorithms: 6 extracted
    - Patterns: 5 identified
    - Data Structures: 4 analyzed
    - Integration Opportunities: 8 found
    - Documents: 5 created
    - Main Document: DEEP_CODE_ANALYSIS_2026-01-11_ALGORITHMS_AND_PATTERNS.md

User: [Reviews analysis documents, begins integration]
```

---

## Advanced Features

### Focus Areas
Can focus on specific areas:
```bash
/deep-analyze --focus algorithms    # Algorithm extraction only
/deep-analyze --focus patterns      # Pattern recognition only
/deep-analyze --focus data          # Data structure analysis only
```

### Repository Filtering
Can filter by repository:
```bash
/deep-analyze --repo ctavolazzi/AI-DnD    # Single repository
/deep-analyze --priority high             # High priority repos only
```

### Output Customization
- ✅ Documents automatically saved to work effort directory
- ✅ Can export to JSON for programmatic use
- ✅ Can generate code snippets in specific format
- ✅ Can create integration templates

---

## Command Template Usage

When executing this command, provide:

1. **Repository List**: GitHub URLs or owner/repo names
2. **Focus Areas** (optional): Algorithms, patterns, data structures
3. **Output Location** (optional): Work effort directory or custom path

**Example**:
```
/deep-analyze
Analyze these repositories:
- https://github.com/ctavolazzi/AI-DnD
- https://github.com/5e-bits/5e-database
- https://github.com/foundryvtt/dnd5e

Focus on: algorithms and patterns
Output to: _work_efforts/WE-260111-jpw1_dnd5e_ai_exploration_initiative/
```

---

**This command transforms repository exploration into actionable algorithms and patterns - perfect for code integration and learning from well-written codebases.**
