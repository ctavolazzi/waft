# Consideration: Empirica TUI Dashboard Manual

Date: 2026-01-19

## Situation
User requested a PDF manual for the Empirica TUI Dashboard integration in WAFT. We also need to integrate the Empirica TUI dashboard into WAFT CLI (planned work) and document how to use the new command (`waft empirica monitor`).

## Options
1. Field guide PDF via WAFT templates (DocumentBuilder.field_guide)
   - Pros: Built-in template, consistent style, supports checklists/procedures
   - Cons: Requires HTML content assembly

2. Markdown-to-PDF via unified PDF class
   - Pros: Simpler content authoring
   - Cons: Less control over field guide styling

3. External PDF tooling
   - Pros: Flexible
   - Cons: Not aligned with WAFT standards

## Decision
Use the WAFT field guide template for an operational manual style. It matches the requested "manual" format and integrates warnings, checklists, and procedures.

## Next Steps
- Run Empirica preflight
- Execute /run-it workflow artifacts
- Generate the PDF manual using DocumentBuilder.field_guide
