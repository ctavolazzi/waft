---
name: Tech Debt Sentinel Implementation
overview: Build a Tech Debt Sentinel system that treats technical debt as "invasive species" in the WAFT ecosystem, with scanning, genetic tracking, evolutionary memory, and automated reporting using the V2 One-Pager Generator.
todos: []
---

# Tech Debt Sentinel Implementation Plan

## Overview

Build a comprehensive Tech Debt Sentinel system that treats technical debt items as "invasive species" in the WAFT ecosystem. The system will scan the codebase, convert debt signals into genetic material (DebtGenes), track evolution over time, and generate daily health briefings using the proven V2 One-Pager Generator.

## Architecture: "The Sentinel Protocol"

### Four Core Components

1. **The Scanner (Sensors)**: Crawls codebase for quantitative debt signals
2. **The Distiller (Digestion)**: Converts raw signals into DebtGenes with severity scores
3. **The Evolutionary Engine (Memory)**: Compares scans over time, tracks events
4. **The Reporter (Voice)**: Generates prose reports using V2 One-Pager Generator

## Implementation Details

### 1. Branch & Directory Structure

**Branch**: `feat/tech-debt-sentinel`

**Directory Structure**:

```
_maintenance/
  tech_debt_sentinel/
    __init__.py
    debt_genome.py          # DebtGene, DebtGenome classes
    scanner.py              # Codebase scanner
    distiller.py            # Signal-to-gene conversion
    evolutionary_engine.py  # Scan comparison & event tracking
    reporter.py             # Report generation
    scan_and_report.py      # Main CLI script
    registry.py             # Genome registry management
```

**Registry Location**: `_genetics/tech_debt/` (similar to styling genomes)

### 2. Core Components

#### 2.1 Debt Genome System (`debt_genome.py`)

**DebtGene** - Individual debt item as genetic material:

- `debt_type`: "todo", "fixme", "bloat", "complexity", "unused_import", "unused_dependency"
- `location`: File path and line number
- `content`: The actual debt item (comment text, function name, etc.)
- `severity_score`: 0.0-1.0 fitness score (inverse - higher = worse)
- `metrics`: Type-specific metrics (line_count, complexity_score, etc.)
- `genome_id`: SHA-256 hash (deterministic from type + location + content)
- `scientific_name`: Generated via LineagePoet taxonomy

**DebtGenome** - Collection of debt items with evolutionary tracking:

- `genome_id`: SHA-256 hash of all debt genes
- `debt_genes`: List[DebtGene]
- `generation`: Scan generation number (0 = first scan)
- `parent_id`: Previous scan's genome_id
- `lineage_path`: Full lineage of scans
- `fitness_score`: Overall debt health (0.0 = perfect, 1.0 = critical)
- `scientific_name`: Generated from genome_id
- `flight_recorder`: List[EvolutionaryEvent]
- `created_at`: Timestamp
- `scan_metadata`: Total files scanned, scan duration, etc.

**Inheritance Pattern**: Follow `StylingGenome` pattern from `src/waft/evolution/styling_genome.py`

#### 2.2 Scanner (`scanner.py`)

**Scanner Class** - Crawls codebase for debt signals:

**Detection Methods**:

1. **TODO/FIXME Comments** (Intentional Debt):

   - Regex: `#\s*(TODO|FIXME|XXX|HACK|NOTE|BUG):?\s*(.+)`
   - Extract comment text and location

2. **File Bloat** (Line Count Thresholds):

   - Conservative thresholds: 500 lines (warning), 1000 lines (critical)
   - Scan all `.py` files in `src/`
   - Track file path and line count

3. **Cyclomatic Complexity** (The Tangle):

   - Use `mccabe` library or simple heuristic (nested if/for/while counts)
   - Scan functions/methods
   - Threshold: complexity > 10 (warning), > 20 (critical)

4. **Unused Imports** (Dead Weight):

   - Use `ruff check --select F401` or similar
   - Track file and unused import names

5. **Unused Dependencies** (Dead Weight):

   - Compare `pyproject.toml` dependencies with actual imports
   - Track unused package names

**Output**: Raw signal dictionary with all detected items

#### 2.3 Distiller (`distiller.py`)

**Distiller Class** - Converts raw signals to DebtGenes:

**Severity Scoring Algorithm**:

- **TODO/FIXME**: Base 0.3, +0.1 per month old (max 0.8)
- **Bloat**: 0.4 (warning), 0.7 (critical)
- **Complexity**: 0.3 + (complexity - 10) * 0.02 (capped at 0.9)
- **Unused Import**: 0.2 (low severity)
- **Unused Dependency**: 0.3 (medium severity)

**Process**:

1. Convert each raw signal to DebtGene
2. Compute genome_id (SHA-256 of type + location + content)
3. Generate scientific name via LineagePoet
4. Assign severity score
5. Collect into DebtGenome

#### 2.4 Evolutionary Engine (`evolutionary_engine.py`)

**EvolutionaryEngine Class** - Compares scans and tracks events:

**Event Types** (extend `EvolutionaryEventType`):

- `DEBT_SPAWN`: New debt detected (invasive species detected)
- `DEBT_EXTINCTION`: Debt fixed (successful eradication)
- `DEBT_GROWTH`: Debt worsened (mutation detected)

**Comparison Logic**:

1. Load previous scan from registry
2. Compare current DebtGenome with previous
3. Identify:

   - New debt items (genome_id not in previous)
   - Fixed debt items (genome_id in previous, not in current)
   - Worsening debt (same genome_id, higher severity)

4. Create EvolutionaryEvent for each change
5. Update lineage tracking

**Registry Management**:

- Store scans in `_genetics/tech_debt/scans/`
- JSON format with genome_id as filename
- Index file: `_genetics/tech_debt/index.json`

#### 2.5 Reporter (`reporter.py`)

**Reporter Class** - Generates prose reports:

**Process**:

1. Use `ChatDistiller` to extract key insights from debt data
2. Create `DistilledChat` with:

   - Title: "Tech Debt Health Briefing - [Date]"
   - Ideas: Debt items as IdeaGenes (categorized by type)

3. Use `TwoPageGenerator` with `StylingGenome` to generate 2-page PDF
4. Output to `_work_efforts/one_pagers/tech_debt_[timestamp].pdf`

**Report Sections**:

- Executive Summary (overall fitness score)
- New Invasive Species (new debt)
- Successful Eradications (fixed debt)
- Mutations Detected (worsening debt)
- Species Registry (all current debt by type)

#### 2.6 Main CLI Script (`scan_and_report.py`)

**CLI Interface**:

```python
@click.command()
@click.option('--scan-only', is_flag=True, help='Only scan, do not generate report')
@click.option('--report-only', is_flag=True, help='Only generate report from last scan')
@click.option('--output', type=click.Path(), help='Custom output path for report')
def main(scan_only, report_only, output):
    """Scan codebase for tech debt and generate health briefing."""
```

**Workflow**:

1. Run scanner → raw signals
2. Run distiller → DebtGenome
3. Run evolutionary engine → compare with previous, track events
4. Save DebtGenome to registry
5. Run reporter → generate 2-page PDF (unless `--scan-only`)

### 3. Integration Points

#### 3.1 Genetic System Integration

**Use Existing Patterns**:

- Follow `StylingGenome` structure from `src/waft/evolution/styling_genome.py`
- Use `LineagePoet` from `src/waft/core/science/taxonomy.py`
- Use `EvolutionaryEvent` from `src/waft/core/agent/state.py`

**Extend Event Types**:

```python
# In src/waft/core/agent/state.py
class EvolutionaryEventType(str, Enum):
    # ... existing types ...
    DEBT_SPAWN = "debt_spawn"
    DEBT_EXTINCTION = "debt_extinction"
    DEBT_GROWTH = "debt_growth"
```

#### 3.2 V2 One-Pager Generator Integration

**Use Existing Components**:

- `ChatDistiller` from `src/waft/evolution/chat_distiller.py`
- `TwoPageGenerator` from `src/waft/evolution/two_page_generator.py`
- `StylingGenome` from `src/waft/evolution/styling_genome.py`

**Report Generation Flow**:

1. Convert DebtGenome → markdown text
2. Use ChatDistiller to extract ideas
3. Generate 2-page PDF with TwoPageGenerator

### 4. Dependencies

**New Dependencies** (add to `pyproject.toml`):

- `mccabe>=0.7.0` - Cyclomatic complexity analysis
- `ast-comments>=1.1.0` - Better comment parsing (optional)

**Existing Dependencies** (already available):

- `hashlib` - Genome ID generation
- `pathlib` - File operations
- `typer` or `click` - CLI interface
- `weasyprint` - PDF generation (via TwoPageGenerator)

### 5. File Locations

**New Files**:

- `_maintenance/tech_debt_sentinel/debt_genome.py`
- `_maintenance/tech_debt_sentinel/scanner.py`
- `_maintenance/tech_debt_sentinel/distiller.py`
- `_maintenance/tech_debt_sentinel/evolutionary_engine.py`
- `_maintenance/tech_debt_sentinel/reporter.py`
- `_maintenance/tech_debt_sentinel/registry.py`
- `_maintenance/tech_debt_sentinel/scan_and_report.py`
- `_maintenance/tech_debt_sentinel/__init__.py`

**Modified Files**:

- `src/waft/core/agent/state.py` - Add new event types

**Registry Location**:

- `_genetics/tech_debt/scans/` - Individual scan genomes
- `_genetics/tech_debt/index.json` - Scan registry index

**Output Location**:

- `_work_efforts/one_pagers/tech_debt_[timestamp].pdf` - Generated reports

### 6. Testing Strategy

**Unit Tests**:

- Test scanner detection for each debt type
- Test distiller severity scoring
- Test evolutionary engine comparison logic
- Test genome ID generation (deterministic)

**Integration Tests**:

- End-to-end scan → distiller → engine → reporter flow
- Registry persistence and retrieval
- Event tracking accuracy

### 7. Documentation

**Create**:

- `_work_efforts/TECH_DEBT_SENTINEL_DESIGN.md` - System design doc
- `docs/TECH_DEBT_SENTINEL.md` - User guide
- Update `README.md` with new feature

## Implementation Order

1. **Phase 1: Foundation**

   - Create branch `feat/tech-debt-sentinel`
   - Create directory structure
   - Implement `debt_genome.py` (DebtGene, DebtGenome)
   - Add new event types to `state.py`

2. **Phase 2: Scanner**

   - Implement `scanner.py` with all detection methods
   - Test each detection method independently
   - Verify detection accuracy

3. **Phase 3: Distiller & Registry**

   - Implement `distiller.py` with severity scoring
   - Implement `registry.py` for genome storage
   - Test genome persistence

4. **Phase 4: Evolutionary Engine**

   - Implement `evolutionary_engine.py` with comparison logic
   - Test event generation (SPAWN, EXTINCTION, GROWTH)
   - Verify lineage tracking

5. **Phase 5: Reporter**

   - Implement `reporter.py` using V2 One-Pager Generator
   - Test report generation
   - Verify 2-page constraint

6. **Phase 6: CLI Integration**

   - Implement `scan_and_report.py` CLI
   - Add to `pyproject.toml` scripts (optional)
   - Test end-to-end workflow

7. **Phase 7: Documentation & Polish**

   - Create design documentation
   - Create user guide
   - Update README
   - Add examples

## Success Criteria

- Scanner detects all 5 debt types accurately
- DebtGenes have deterministic genome IDs
- Scientific names generated via LineagePoet
- Evolutionary engine correctly identifies SPAWN, EXTINCTION, GROWTH events
- Reports ge