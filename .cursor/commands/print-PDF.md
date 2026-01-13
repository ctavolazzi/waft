# Print PDF

**Intelligently find and print the most relevant PDF, or create an evolved PDF using WAFT principles.**

The `/print-PDF` command uses intelligent discovery to find the most relevant PDF based on conversation context, active files, work efforts, and Oracle epistemic state. If no relevant PDF exists, it creates an evolved PDF using WAFT evolution principles.

**Use when:** You want to print a PDF related to your current work, or need a summary document created and printed.

---

## Purpose

Provides: Intelligent PDF discovery, evolved PDF creation, Oracle integration, WAFT evolution principles, automatic printing.

---

## Usage

### Basic Print

```
/print-PDF
```

Finds the most relevant PDF and prints it. If no relevant PDF exists, creates an evolved PDF and prints it.

### Force Create New PDF

```
/print-PDF --force-create
```

Forces creation of a new evolved PDF, even if a relevant PDF exists.

### Preview Only (Don't Print)

```
/print-PDF --no-print
```

Generates the PDF but doesn't print it. Useful for previewing before printing.

### Custom Style

```
/print-PDF --style premium
```

Creates PDF with specified style (clinical_standard, premium, professional).

---

## How It Works

### 1. PDF Discovery

The system searches for PDFs in:
- Current directory and subdirectories
- `_work_efforts/` directories
- `_pyrite/` directories
- `_science/` directories

PDFs are scored based on:
- **Recency** (0-40%): How recently the PDF was modified
- **Context Match** (0-30%): Filename/content matches conversation keywords
- **Work Effort Association** (0-20%): PDF is in an active work effort directory
- **Oracle Relevance** (0-10%): PDF aligns with current epistemic phase

### 2. PDF Evolution

If no relevant PDF is found (or relevance < 50%), the system creates an evolved PDF using:

**WAFT Principles:**
- **"Part within the whole"**: PDF reflects current context within larger project
- **"As above, so below"**: PDF structure mirrors epistemic state
- **Evolution**: PDF content evolves based on what system knows/doesn't know

**PDF Types:**
- `conversation_summary`: Summary of current conversation
- `project_status`: Project status report with epistemic state
- `oracle_insights`: Oracle insights and findings
- `work_effort`: Summary of active work efforts
- `hybrid`: Combines multiple sources

**Oracle Integration:**
- Uses Oracle epistemic phase to determine PDF type
- Incorporates Oracle insights and unknowns
- Logs PDF operations to Oracle

### 3. Printing

Once a PDF is found or created, it's printed to the default printer using:
- macOS: `lpr`
- Windows: `print`
- Linux: `lpr`

---

## Examples

### Example 1: Print Relevant PDF

```
/print-PDF
```

**Output:**
- Searches for relevant PDFs
- Finds PDF with 75% relevance
- Prints the PDF

### Example 2: Create and Print Evolved PDF

```
/print-PDF --force-create
```

**Output:**
- Creates new evolved PDF using WAFT principles
- Consults Oracle for epistemic state
- Generates PDF based on current phase
- Prints the PDF

### Example 3: Preview Before Printing

```
/print-PDF --no-print
```

**Output:**
- Creates or finds PDF
- Opens PDF for preview
- Does not print
- Shows path for manual printing

---

## Options

| Option | Description |
|--------|-------------|
| `--force-create` | Force creation of new PDF even if relevant one exists |
| `--no-print` | Generate but don't print (preview only) |
| `--style <style>` | PDF style: `clinical_standard` (default), `premium`, `professional` |
| `--path <path>` | Project path (default: current directory) |

---

## Integration

### Oracle Integration

The command integrates with TheOracle for epistemic intelligence:

- **Queries epistemic state** before PDF creation
- **Uses epistemic phase** to guide PDF type selection
- **Incorporates insights** into PDF content
- **Logs operations** as findings to Oracle

### WAFT Evolution

Uses WAFT evolution principles:

- **Part within the whole**: PDF reflects current work within project context
- **As above, so below**: PDF structure mirrors epistemic state
- **Evolution**: Content evolves based on knowledge and uncertainty

### Work Efforts

If active work efforts are detected, the PDF may include:
- Work effort summaries
- Related file references
- Progress tracking

---

## Related Commands

- `/pdf-me` - Generate PDF from markdown content
- `/waft-docs` - Generate WAFT documentation PDFs
- `/oracle` - Consult Oracle for epistemic insights

---

## Notes

- **No automatic printing**: This is the only command that prints PDFs automatically
- **Intelligent discovery**: Finds PDFs based on context, not just recency
- **Oracle required**: Full functionality requires Empirica to be initialized
- **Fallback behavior**: Works without Oracle, but with reduced intelligence

---

## Philosophy

The `/print-PDF` command embodies WAFT principles:

1. **Intelligence**: Uses context and Oracle to make smart decisions
2. **Evolution**: Creates PDFs that evolve with the project
3. **Integration**: Connects conversation, files, work efforts, and epistemic state
4. **Materialization**: Brings digital work into the physical world (printing)

---

**Status**: ✅ Available  
**Requires**: WAFT project, optional Oracle (Empirica)
