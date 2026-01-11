# One-Pager Tool

**Purpose:** Create crystalized, printable 2-page (front/back) one-pagers from any content

---

## Philosophy

> "I'm an academic nerd scientist I like binders full of paper it's cool to me the physical constellation of crystallized knowledge inside spacetime through the refraction of light" - Christopher Tavolazzi

The One-Pager tool enables physical knowledge management by creating perfect 2-page printable documents from any content type.

---

## Features

### Multi-Format Support
- **Markdown**: Files or strings with full markdown syntax
- **Plain Text**: Simple text documents
- **Code Files**: Python, JavaScript, TypeScript, HTML, CSS, etc.
- **Structured Data**: JSON, YAML (converted to readable format)
- **Python Objects**: Dictionaries, lists (auto-converted to HTML)

### Intelligent Processing
- **Auto-Detection**: Detects content type automatically
- **Smart Condensation**: Long content intelligently condensed to fit 2 pages
- **Content Expansion**: Short content expanded with summary sections
- **Format Preservation**: Maintains structure (headers, lists, code blocks)

### Perfect 2-Page Output
- **Exact Constraint**: Always creates front/back of one sheet
- **Feedback Loop**: Automatically adjusts CSS to meet page count
- **Printer-Friendly**: Black and white, minimal ink usage
- **Binder-Ready**: Standard letter size, professional formatting

---

## Usage

### Global Cursor Command

```
/one-pager [content] [options]
```

**Examples:**
```
/one-pager file:README.md title:"README One-Pager"
/one-pager markdown:"# Title\n\nContent" title:"My Doc"
/one-pager json:'{"key": "value"}' title:"Config"
```

### Python API

```python
from waft import OnePager, create_one_pager

# From markdown
pager = OnePager.from_markdown("# Title\n\nContent", title="My Doc")
pager.generate()

# From file
pager = OnePager.from_file("README.md", title="README")
pager.generate()

# From dictionary
pager = OnePager.from_dict({"key": "value"}, title="Config")
pager.generate()

# Quick function
create_one_pager("# Title\n\nContent", title="My Doc")
```

### CLI Script

```bash
python3 scripts/create_one_pager.py file:README.md title:"README One-Pager"
python3 scripts/create_one_pager.py markdown:"# Title\n\nContent"
python3 scripts/create_one_pager.py json:'{"key": "value"}' title:"Config"
```

---

## Content Processing

### Markdown
- Headers (`#`, `##`, `###`)
- Lists (`-`, `*`)
- Code blocks (```)
- Bold/italic (`**`, `__`)
- Links (`[text](url)`)

### Code Files
- Syntax highlighting preserved
- Full code displayed
- File type indicated

### Structured Data (JSON/YAML)
- Nested structures converted to HTML
- Keys as headers
- Values as content
- Lists as bullet points

### Plain Text
- Paragraphs preserved
- Line breaks maintained
- Simple formatting

---

## Output Format

### File Location
All one-pagers saved to:
```
_work_efforts/one_pagers/[title]_[date].pdf
```

### Document Structure
- **Cover**: Title, subtitle, classification
- **Content**: Processed and formatted content
- **Footer**: Date, series number, issued by

### Styling
- **Printer-Friendly**: Black and white
- **Field Guide Style**: Professional, military-inspired
- **Compact Layout**: Optimized for 2 pages
- **Readable Fonts**: Arial/Helvetica, appropriate sizing

---

## Intelligent Condensation

For very long content (>2000 words), the tool:

1. **Preserves Structure**: Keeps all headers
2. **Keeps Key Sections**: First paragraph after each header
3. **Preserves Code**: All code blocks kept intact
4. **Maintains Lists**: Important lists preserved
5. **Truncates Excess**: Removes redundant paragraphs
6. **Adds Notice**: Indicates content was condensed

This ensures important information is preserved while fitting 2 pages.

---

## Use Cases

### Quick Reference
Create one-pagers from documentation for quick physical reference.

### Code Summaries
Print code files as reference sheets for offline study.

### Configuration Docs
Print config files for physical storage and backup.

### Meeting Notes
Convert notes to printable format for physical archives.

### Research Gists
Crystallize research findings into printable format.

### Binder Organization
Build physical knowledge constellation from digital content.

---

## Evolution Through Study Gym

The One-Pager tool was evolved using the Study Gym:

1. **Observed**: How different content types affect page count
2. **Hypothesized**: What strategies work for condensation/expansion
3. **Tested**: Various content types and lengths
4. **Analyzed**: What works best for 2-page constraint
5. **Concluded**: Optimal strategies for different content types

This scientific approach ensures the tool works well across diverse use cases.

---

## Integration with WAFT

The One-Pager tool integrates with:

- **DocumentBuilder**: Uses constraint-aware PDF generation
- **Study Gym**: Evolved through scientific method
- **Binder System**: Can be added to document collections
- **Global Commands**: Available via `/one-pager` command

---

## Example Workflow

```python
# 1. Create one-pager from markdown file
pager = OnePager.from_file("docs/GUIDE.md", title="Guide One-Pager")
pdf = pager.generate()

# 2. Check it's exactly 2 pages
from pypdf import PdfReader
reader = PdfReader(str(pdf))
assert len(reader.pages) == 2

# 3. Print and add to binder
# Physical knowledge constellation complete!
```

---

## Philosophy in Practice

The One-Pager tool embodies the philosophy of physical knowledge management:

- **Crystallization**: Digital content → Physical document
- **Constellation**: Multiple one-pagers → Binder collection
- **Spacetime**: Physical location in 3D space
- **Refraction**: Light reflecting off paper → Knowledge transfer

Each one-pager is a crystallized piece of knowledge, ready to be placed in your physical binder constellation.

---

**Created with ❤️ for academic nerds who love binders full of paper.**
