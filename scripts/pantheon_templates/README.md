# Pantheon UI Templates

Multiple template versions of the Pantheon web interface, each with a different aesthetic and use case.

## Generated Files

### 1. Improved Base Version
**File:** `pantheon_improved.html`

**Improvements:**
- ✅ Enhanced visual design with better gradients and animations
- ✅ Search functionality - filter gods by name, title, description, or abilities
- ✅ Status filtering - filter by Active/Dormant
- ✅ Better hover effects and transitions
- ✅ Improved typography and spacing
- ✅ Responsive design improvements
- ✅ Shimmer animations on card borders
- ✅ Better color contrast and readability

**Features:**
- Real-time search
- Status filters
- Smooth animations
- Modern card design
- Better mobile support

### 2. D&D Character Sheet Template
**Files:** `pantheon_dnd_character_sheet.html` + `.pdf`

**Style:**
- Parchment/cream background (#f4e8d0)
- Medieval serif typography (Times New Roman)
- Decorative borders (double borders)
- Fantasy color palette (browns, golds, deep reds)
- Stat block styling
- Two-column grid layout

**Best for:**
- Printing for D&D sessions
- Fantasy-themed presentations
- Character sheet aesthetic

### 3. Field Guide Template
**Files:** `pantheon_field_guide.html` + `.pdf`

**Style:**
- Military field manual aesthetic
- Two-column layout
- Courier New monospace for headers
- Black borders and boxes
- Practical, rugged design
- Equipment checklist style

**Best for:**
- Operational documentation
- Quick reference guides
- Field manual style

### 4. Academic Paper Template
**Files:** `pantheon_academic_paper.html` + `.pdf`

**Style:**
- Academic paper format
- Times New Roman serif
- Abstract section
- Numbered sections
- Formal typography
- Research paper aesthetic

**Best for:**
- Academic presentations
- Research documentation
- Formal reports

### 5. Lab Notes Template
**Files:** `pantheon_lab_notes.html` + `.pdf`

**Style:**
- Grid paper background
- Courier New monospace font
- Dated entries
- Observation format
- Data tables
- Laboratory notebook aesthetic

**Best for:**
- Scientific documentation
- Experiment logs
- Research notes

## Usage

### View HTML Versions
```bash
# Open improved version
open scripts/pantheon_web_improved.html

# Open template versions
open scripts/pantheon_templates/pantheon_dnd_character_sheet.html
open scripts/pantheon_templates/pantheon_field_guide.html
open scripts/pantheon_templates/pantheon_academic_paper.html
open scripts/pantheon_templates/pantheon_lab_notes.html
```

### View PDF Versions
```bash
# All PDFs are in the templates directory
open scripts/pantheon_templates/*.pdf
```

### Regenerate Templates
```bash
python3 scripts/generate_pantheon_templates.py
```

## Improvements Made

### Visual Enhancements
1. **Better Gradients**: More sophisticated background gradients with animation
2. **Card Design**: Enhanced shadows, borders, and hover effects
3. **Typography**: Improved font sizes, weights, and spacing
4. **Color Scheme**: Better contrast and color harmony
5. **Animations**: Smooth transitions and shimmer effects

### Functional Enhancements
1. **Search**: Real-time search across all god data
2. **Filtering**: Status-based filtering (All/Active/Dormant)
3. **Responsive**: Better mobile and tablet support
4. **Accessibility**: Improved contrast and readability

### Template Variants
1. **D&D Style**: Perfect for fantasy/RPG contexts
2. **Field Guide**: Operational manual aesthetic
3. **Academic**: Research paper format
4. **Lab Notes**: Scientific notebook style

## Next Steps

Potential future enhancements:
- Live data loading from `_pantheon/` directory
- Click-through details for each god
- Real-time status updates
- Integration with `waft serve` dashboard
- Export to different formats
- Print-friendly versions

## Files Generated

```
scripts/pantheon_templates/
├── pantheon_improved.html
├── pantheon_dnd_character_sheet.html
├── pantheon_dnd_character_sheet.pdf
├── pantheon_field_guide.html
├── pantheon_field_guide.pdf
├── pantheon_academic_paper.html
├── pantheon_academic_paper.pdf
├── pantheon_lab_notes.html
├── pantheon_lab_notes.pdf
└── README.md (this file)
```

All templates use the same Pantheon data but present it in different styles for different use cases.