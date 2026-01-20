# UI Technical Requirements

**Date**: 2026-01-19  
**Work Effort**: WE-260119-7och

## Components Needed

### 1. Header
- Project title: "Succulent Jewelry PDF System"
- Subtitle: Brief description
- Navigation links

### 2. Dashboard Stats Section
- Total PDFs generated
- Total size
- Last generation date
- Templates available
- Scripts status

### 3. PDF Gallery
- Grid layout
- PDF cards with:
  - Thumbnail/preview
  - Title
  - Date
  - Size
  - Quick actions (view, download)

### 4. Quick Actions Panel
- Generate new guide button
- Batch generate button
- Prepare for Gumroad button
- View templates button

### 5. System Status Panel
- Templates available
- Scripts available
- Config status
- Dependencies status

### 6. Work Efforts Section
- Current work effort link
- Improvement analysis link
- Progress tracking

### 7. Footer
- Links to documentation
- Project info

## Data Sources

### Static Data (from filesystem)
- Generated PDFs: `generated/guides/*.pdf`
- Templates: `templates/*.py`
- Scripts: `scripts/*.py`
- Config: `config/*.json`
- Content: `content/guides/*.md`

### Dynamic Data (to be generated)
- PDF metadata (extract from files)
- Stats (count, size, dates)
- System status

## Layout Structure

```
┌─────────────────────────────────────┐
│ Header (Title, Nav)                 │
├─────────────────────────────────────┤
│ Dashboard Stats (4 cards)           │
├─────────────────────────────────────┤
│ PDF Gallery (grid)                  │
│  [PDF] [PDF] [PDF]                  │
│  [PDF] [PDF]                        │
├─────────────────────────────────────┤
│ Quick Actions | System Status       │
│ (buttons)     | (status list)       │
├─────────────────────────────────────┤
│ Work Efforts Section                │
├─────────────────────────────────────┤
│ Footer                              │
└─────────────────────────────────────┘
```

## Styling

- Clean, modern design
- Succulent/jewelry theme colors (greens, earth tones)
- Card-based layout
- Responsive grid
- Professional but approachable

## Interactions

- Click PDF card → Open PDF
- Click generate → Show form/modal
- Hover effects on cards
- Smooth transitions
