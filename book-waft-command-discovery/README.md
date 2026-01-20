# WAFT Command Discovery Book

A comprehensive guide documenting the exploration of WAFT's command ecosystem and the evolution of a unified command dashboard.

## Quick Start

### Initialize Typst Book

```bash
# If using shiroa CLI
shiroa init book-waft-command-discovery

# Or manually with Typst
typst init @preview/shiroa:0.3.1 book-waft-command-discovery
```

### Build Book

```bash
cd book-waft-command-discovery
typst compile src/book.typ
```

### Serve for Preview

```bash
# If using shiroa CLI
shiroa serve

# Or use Typst's HTML export
typst compile --format html src/book.typ
```

## Book Structure

- **18 chapters** across **4 parts**
- **Part I**: Command Discovery Journey (5 chapters)
- **Part II**: UI Evolution Process (5 chapters)
- **Part III**: System Integration (4 chapters)
- **Part IV**: Lessons & Insights (4 chapters)

## Content Sources

- Chat context scan
- Design documents
- Technical requirements
- Wireframe HTML
- Generated artifacts
- Work effort documentation

## Templates Used

- `@preview/shiroa:0.3.1` - Book structure
- `@preview/owlbear:0.0.1` - D&D elements (optional)

## Output Formats

- HTML Book (interactive web book)
- PDF Book (print-ready)
- Static HTML (standalone files)
