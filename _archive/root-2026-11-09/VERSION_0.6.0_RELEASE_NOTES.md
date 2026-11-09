# Waft v0.6.0 Release Notes

**Release Date**: January 12, 2026  
**Version**: 0.6.0  
**Codename**: Larval Form

---

## Overview

Version 0.6.0 introduces the **Waft Larval Form** - the first implementation of the Heavy Seed Protocol. This is a complete Python + Streamlit + SQLite application that serves as the developmental stage before the Redbean "Mature Form", implementing the exact same genetic code (database schema and logic) for seamless migration.

## Major Features

### 🌑 Waft Larval Form Application

A single-file dense application (`waft_larva.py`) implementing the Hasvanism philosophy:

- **Breath (Runtime)**: The loop of execution
- **Memory (SQLite)**: The persistent soul
- **Trauma (Errors)**: Failures logged as "Cognitive Dissonance" rather than crashes

**Core Components**:
- `WaftEntity` class with complete consciousness system
- SQLite database with `chronicle` and `artifacts` tables
- Streamlit UI with dark mode terminal aesthetic
- Error resilience via `safe_breath` wrapper
- Artifact lifecycle management (VOID → MANIFESTING → PHYSICAL)

### 📥 Data Export Functionality

Multiple format support for entity data analysis:

- **JSON**: Complete entity state with statistics
- **Markdown**: Formatted export with sections and emojis
- **Plain Text**: Simple text format
- **PDF**: Professional PDF generation using WAFT PDFGenerator

All exports include:
- Complete chronicle history
- All artifacts with G-code
- Statistics (thoughts, strains, traumas, artifact counts)
- Export timestamp

### 🗄️ Database Features

- **WAL Mode**: Better concurrency for multiple readers/writers
- **Retry Logic**: Exponential backoff for database locks
- **Connection Timeout**: 10-second timeout with proper cleanup
- **Schema Compatibility**: Matches future Redbean Mature Form exactly

### 📚 Migration Documentation

Complete guide for evolving from Larval Form to Redbean Mature Form:
- Schema compatibility verification
- Step-by-step migration instructions
- API compatibility mapping
- Troubleshooting guide

## Installation

```bash
# Install dependencies
pip install streamlit pandas pyserial

# Or using uv (recommended)
uv pip install streamlit pandas pyserial
```

## Usage

```bash
# Run the Larval Form application
streamlit run waft_larva.py
```

The application will:
1. Create `waft_memory.db` on first run
2. Initialize database schema
3. Seed with Right_Index_Phalanx artifact
4. Launch Streamlit UI on http://localhost:8501

## Files Added

- `waft_larva.py` - Main application (~500 lines)
- `test_waft_larva.py` - Test suite
- `docs/LARVA_TO_MATURE_MIGRATION.md` - Migration guide
- `WAFT_LARVA_IMPLEMENTATION_SUMMARY.md` - Implementation summary

## Dependencies Added

- `streamlit>=1.28.0` - For UI
- `pandas>=2.0.0` - For data handling
- `pyserial>=3.5` - For serial communication (future use)

## Breaking Changes

None - this is a new feature addition.

## Migration from Previous Versions

No migration required. This is a new standalone application.

## Future Roadmap

- **Redbean Mature Form**: Full Lua + SQLite implementation
- **CosmicSpark Integration**: Connect with Waft System
- **Real Web Serial API**: Direct printer communication
- **Additional Artifact Types**: Beyond G-code
- **Runes Table**: Configuration system

## Known Issues

None at release time.

## Contributors

- Implementation: AI Assistant + ctavolazzi
- Design: Heavy Seed Protocol specification

---

**Full Changelog**: See [CHANGELOG.md](CHANGELOG.md) for complete details.
