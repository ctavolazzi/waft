= Document Generation

WAFT provides multiple commands for generating various types of documents. This chapter explores `/one-pager`, `/worldbuild`, and `/tell-story` commands.

== The `/one-pager` Command

Creates crystalized, printable 2-page (front/back) one-pagers from any content type.

=== Purpose

Perfect for academic nerds who love physical binders full of paper. Creates perfect 2-page printable documents from:
- Markdown files/text
- Plain text
- Code files
- JSON/YAML data
- Python dictionaries
- HTML content

=== Features

- Automatic format detection
- Smart content processing
- Exact 2-page constraint
- Printer-friendly (black and white)
- Intelligent expansion/condensation
- Briefing mode available

=== Usage

```bash
/one-pager file:README.md title:"README One-Pager"
/one-pager --briefing title:"Session Briefing"
```

== The `/worldbuild` Command

Creates compelling worldbuilding documents (fantasy or factual) with Foundation/TM formatting elements.

=== Purpose

Perfect for:
- Fantasy worldbuilding (lore, characters, locations)
- Factual documentation (reports, manuals, guides)
- SCP-style documentation
- Corporate reports

=== Formatting Elements

- KeyValueBlock (metadata, parameters)
- WarningBlock (severity levels)
- SignatureBlock (authorization)
- SectionHeader (hierarchical)
- Summary boxes
- Tables
- Log blocks

== The `/tell-story` Command

Generates narrative PDFs from story input using TheOracle, Storyteller, and TavernKeeper.

=== Purpose

Creates beautifully formatted PDF stories enriched with:
- Epistemic insights from TheOracle
- Narrative elements from TavernKeeper
- Professional PDF styling

=== Features

- Story input processing
- Oracle insights integration
- Narrative generation
- PDF creation
- Automatic opening

== Integration

All document generation commands integrate with:
- PDF generation system
- Template system
- Work efforts tracking
- File system organization

== Key Takeaways

- WAFT provides diverse document generation options
- Multiple formats supported (PDF, HTML, Markdown)
- Professional styling built-in
- Integration with project systems
