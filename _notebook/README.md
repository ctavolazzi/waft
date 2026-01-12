# Self-Engineering Notebook

The system's "notebook" - where it journals findings, reflects on problems, and converts insights into actionable work.

## Structure

```
_notebook/
├── index.json                    # Index of all entries and reflections
├── entries/                      # Individual notebook entries
│   ├── entry_YYYYMMDD_HHMMSS_problem.json
│   ├── entry_YYYYMMDD_HHMMSS_diagnosis.json
│   └── ...
├── reflections/                  # Reflections on findings
│   └── reflection_YYYYMMDD_HHMMSS.json
└── actionables/                  # Created actionable items (work efforts, scenarios, quests)
    └── ...
```

## Entry Types

- **PROBLEM_DETECTED**: A problem was detected during execution
- **DIAGNOSIS**: Root cause analysis of a problem
- **SOLUTION_PROPOSED**: A solution was proposed
- **SOLUTION_IMPLEMENTED**: A solution was implemented
- **REFLECTION**: Reflection on findings
- **INSIGHT**: Key insight discovered
- **ITERATION**: Iteration cycle completed

## Actionable Types

The notebook can create:
- **WORK_EFFORT**: Work effort in `_work_efforts/`
- **SCENARIO**: D&D scenario in `examples/`
- **QUEST**: D&D quest in `src/gym/rpg/dungeons/`
- **TICKET**: Ticket in a work effort

## Usage

The notebook is automatically used by the self-engineering system:
1. Problems are journaled automatically when detected
2. Diagnoses are journaled when made
3. Reflections are created periodically
4. Actionable items are created from reflections

## Manual Access

```python
from waft.core.self_engineering import NotebookManager

notebook = NotebookManager(Path("_notebook"))

# Get all entries
entries = notebook.get_entries()

# Get reflections
reflections = notebook.get_reflections()

# Get entries by type
problems = notebook.get_entries(NotebookEntryType.PROBLEM_DETECTED)
```

---

**This is the system's memory of its own engineering process - the meta-game notebook.**
