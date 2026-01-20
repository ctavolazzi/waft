# Complete Template Guide

## Overview

The `comprehensive_template.md` demonstrates all features available in the Succulent Jewelry PDF system. Use it as a reference when creating your own guides.

## Quick Start

1. **Copy the template:**
   ```bash
   cp content/guides/comprehensive_template.md content/guides/my_new_guide.md
   ```

2. **Edit your content:**
   - Replace placeholder text with your actual content
   - Add your own images or use placeholders
   - Customize sections as needed

3. **Add images:**
   ```bash
   python scripts/add_images.py \
     --content content/guides/my_new_guide.md \
     --provider pixabay \
     --query "your-topic" \
     --size large
   ```

4. **Generate PDF:**
   ```bash
   python scripts/generate_guide.py \
     --content content/guides/my_new_guide.md \
     --title "Your Guide Title" \
     --output generated/guides/
   ```

## Features Demonstrated

### ✅ Image APIs
- **Pixabay**: No API key, immediate results
- **Pexels**: Professional photos (requires API key)
- **Picsum**: Placeholder images for testing
- Automatic fallback chain
- Multiple size options

### ✅ Formatting
- Headers (H1, H2, H3)
- Bold, italic, code formatting
- Ordered and unordered lists
- Tables with styling
- Code blocks with syntax highlighting

### ✅ Interactive Elements
- **Pro Tips**: Green boxes with light bulb icons
- **Warnings**: Red boxes for critical information
- **Cautions**: Orange boxes for careful attention
- **Procedures**: Numbered step circles

### ✅ Image Features
- Multiple image sizes
- Image captions
- Photographer attribution (Pexels)
- Image credits footer

### ✅ Professional Features
- Cover page with series number
- Page headers and footers
- Gumroad integration
- Resources section
- Troubleshooting tables

## Template Sections

1. **Introduction** - Overview and purpose
2. **Image API Integration** - Examples of all three APIs
3. **Formatting Features** - Text, lists, headers
4. **Step-by-Step Procedures** - Numbered steps
5. **Tips and Warnings** - Callout boxes
6. **Tables** - Data organization
7. **Code Examples** - Technical instructions
8. **Image Examples** - Different sizes and sequences
9. **Advanced Features** - Combined elements
10. **Troubleshooting** - Problem-solving
11. **Resources** - Links and references
12. **Best Practices** - Quality guidelines
13. **Conclusion** - Wrap-up

## Customization Tips

### Change Image Provider
Replace `![placeholder:pixabay:800:600]` with:
- `![placeholder:pexels:800:600]` for Pexels
- `![placeholder:picsum:800:600]` for Picsum
- `![placeholder:800:600]` for default (Picsum)

### Adjust Image Sizes
- `![placeholder:1200:800]` - Large format
- `![placeholder:800:600]` - Standard
- `![placeholder:600:400]` - Small format

### Modify Procedures
Copy the procedure div structure and adjust step content:
```markdown
<div class="procedure">
<div class="step">
<strong>Your step title</strong> - Your step description
</div>
</div>
```

### Add Tips/Warnings
```markdown
<div class="tip">
<div class="tip-title">Your Tip Title</div>
Your tip content here.
</div>
```

## Best Practices from Experiments

Based on our API experiments:

1. **Use Pixabay for immediate results** - No setup required
2. **Use "large" size for PDFs** - 1280px provides excellent quality
3. **Keep queries simple** - Single words or short phrases work best
4. **Add captions to all images** - Provides context
5. **Include attribution** - Required for Pexels, good practice for all

## Example Workflow

```bash
# 1. Create your guide
cp content/guides/comprehensive_template.md content/guides/my_guide.md

# 2. Edit content (use your editor)
# ... edit my_guide.md ...

# 3. Add images from Pixabay
python scripts/add_images.py \
  --content content/guides/my_guide.md \
  --provider pixabay \
  --query "succulent" \
  --size large

# 4. Generate PDF
python scripts/generate_guide.py \
  --content content/guides/my_guide.md \
  --title "My Succulent Guide" \
  --subtitle "A Complete Reference" \
  --output generated/guides/

# 5. Check output
open generated/guides/my_guide.pdf
```

## File Locations

- **Template**: `content/guides/comprehensive_template.md`
- **Generated PDF**: `generated/guides/comprehensive_template.pdf`
- **This Guide**: `TEMPLATE_GUIDE.md`

## Next Steps

1. Review the comprehensive template PDF
2. Copy sections you need for your guide
3. Customize content for your topic
4. Add images using the image API tools
5. Generate your professional PDF guide

---

*For more information, see the main README.md and experiment results in `generated/experiments/`*
