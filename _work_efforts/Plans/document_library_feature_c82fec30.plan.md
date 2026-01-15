---
name: Document Library Feature
overview: Add a downloadable document library page to FogSift where users can browse and download PDF forms, templates, and worksheets organized by category.
todos:
  - id: create-documents-json
    content: Create content/documents.json with document metadata structure
    status: pending
  - id: create-library-html
    content: Create library.html page with category tabs and document cards
    status: pending
  - id: create-library-js
    content: Create js/library.js for category filtering
    status: pending
  - id: create-documents-folder
    content: Create documents/ folder structure with placeholder PDFs
    status: pending
  - id: update-navigation
    content: Add Library link to site navigation and footer
    status: pending
---

# Document Library Feature

## What We're Building

A new `/library.html` page with a browsable, filterable collection of downloadable PDFs (consulting forms, templates, framework worksheets). Uses the existing industrial badge aesthetic.

## Architecture

```mermaid
flowchart LR
    subgraph Files [New Files]
        HTML[library.html]
        JS[js/library.js]
        JSON[content/documents.json]
        DOCS[documents/pdfs]
    end
    
    subgraph Flow [User Flow]
        A[Visit Library] --> B[Browse by Category]
        B --> C[Click Download]
        C --> D[PDF Download]
    end
    
    JSON --> JS
    JS --> HTML
    DOCS --> D
```



## File Structure

```javascript
src/
  library.html              # New page
  js/library.js             # Category filtering logic
  content/documents.json    # Document metadata
  documents/                # PDF storage folder
    forms/
    templates/
    worksheets/
    guides/
```



## Key Implementation Details

1. **Page Design**: Card grid similar to pricing section, with category filter tabs at top
2. **Document Metadata** ([`content/documents.json`](src/content/documents.json)): Title, description, category, filename, file size
3. **Categories**: Forms, Templates, Worksheets, Guides
4. **Download**: Direct `<a href="documents/..." download>` links - no JavaScript required for actual download

## Starter Documents (Placeholders)

- Client Intake Form (Forms)
- Statement of Work Template (Templates)  
- Five Whys Worksheet (Worksheets)
- Diagnostic Process Guide (Guides)

## Navigation Update

Add "Library" link to nav in [`index.html`](src/index.html) and update footer links.

## Notes

- PDFs stored locally in repo (you'll add actual PDFs later)