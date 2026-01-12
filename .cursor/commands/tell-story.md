# Tell Story

**Generate a narrative PDF from story input using TheOracle, Storyteller, and TavernKeeper.**

Creates a beautifully formatted PDF story enriched with epistemic insights from TheOracle and narrative elements from TavernKeeper.

**Use when:** You want to convert text input into a professional narrative PDF with insights and storytelling elements.

---

## Purpose

Provides: story input processing, Oracle insights integration, narrative generation, PDF creation, automatic opening.

---

## Usage

### Basic Usage

```
/tell-story "Your story text here"
```

Generate a PDF from story text with default settings.

### With Title

```
/tell-story "Your story" --title "My Story"
```

Specify a custom title for the PDF.

### With Style Options

```
/tell-story "Your story" --style premium --narrative medium --structure three_act
```

Customize PDF style, narrative complexity, and story structure.

### Skip Oracle

```
/tell-story "Your story" --no-oracle
```

Generate PDF without Oracle insights (faster, no Empirica required).

### Custom Output Path

```
/tell-story "Your story" --output "my_story.pdf"
```

Specify where to save the PDF.

---

## What It Does

1. **Initializes TavernKeeper** - Sets up narrative system
2. **Consults TheOracle** (optional) - Gets epistemic insights about the story
3. **Creates Storyteller** - Processes input into narrative structure
4. **Generates PDF** - Creates formatted PDF with premium styling
5. **Opens PDF** - Automatically opens for viewing/printing
6. **Logs to TavernKeeper** - Records story generation in adventure journal

---

## Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--title` | `-t` | PDF title | Auto-generated |
| `--style` | `-s` | PDF style (premium/clinical_standard/professional) | premium |
| `--narrative` | `-n` | Narrative style (simple/medium) | medium |
| `--structure` | | Story structure (linear/three_act) | linear |
| `--path` | `-p` | Project path | Current directory |
| `--no-oracle` | | Skip Oracle insights | false |
| `--output` | `-o` | Output PDF path | Auto-generated |

---

## Examples

### Example 1: Simple Story

```
/tell-story "Once upon a time, there was a developer who discovered the power of epistemic intelligence."
```

**Output:**
- PDF with story text
- Oracle insights (if Empirica initialized)
- TavernKeeper narrative elements
- Automatically opened PDF

### Example 2: Complex Story with Custom Title

```
/tell-story "Long story text here..." --title "The Developer's Journey" --style premium --narrative medium
```

**Output:**
- Custom titled PDF
- Premium styling
- Medium complexity narrative
- Oracle insights integrated

### Example 3: Quick Generation (No Oracle)

```
/tell-story "Quick story" --no-oracle --output "quick.pdf"
```

**Output:**
- Fast generation (no Empirica required)
- Custom output path
- No Oracle insights section

---

## Integration

- **TheOracle**: Provides epistemic insights and recommendations
- **Storyteller**: Converts input to narrative prose
- **TavernKeeper**: Adds narrative elements and logs to adventure journal
- **PDFGenerator**: Creates formatted PDF output
- **Empirica**: Tracks story generation as epistemic event (if initialized)

---

## When to Use

**Use `/tell-story` when**:
- ✅ Want to convert text to professional PDF
- ✅ Need narrative structure and formatting
- ✅ Want epistemic insights about the story
- ✅ Need automatic PDF opening for printing
- ✅ Want story logged to TavernKeeper journal

**Don't use `/tell-story` when**:
- ❌ Need simple text-to-PDF (use PDFGenerator directly)
- ❌ Don't want narrative processing (use simpler tools)
- ❌ Need scientific paper format (use ScientificPDFGenerator)

---

## Output Format

The generated PDF includes:
- **Story Content**: Your input text, formatted as narrative
- **Oracle Insights** (if enabled): Epistemic phase, knowledge coverage, recommendations, findings
- **Narrative Structure**: Organized with chapters/sections based on structure type
- **Premium Styling**: Elegant typography and formatting

---

**This command orchestrates TheOracle, Storyteller, and TavernKeeper to create beautiful narrative PDFs from your story input.**

--- End Command ---
