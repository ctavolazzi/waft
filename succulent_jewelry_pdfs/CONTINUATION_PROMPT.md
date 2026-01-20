# Continuation Prompt for New Chat

## Project Context

I'm working on a **Succulent Jewelry PDF Generation System** - a complete system for creating professional PDF guides that complement my succulent jewelry casting videos. These guides will be sold on Gumroad.

## Current State

### ✅ Completed Features

1. **PDF Generation System**
   - Professional guide template with cover page, headers, footers
   - Poetry template for spoken word/video essays
   - All styling issues fixed (step numbers, tip shadows, bold formatting)

2. **Image API Integration**
   - **Pixabay**: Fully working, no API key needed (default key: `29486486-de7f8c25dff5fd83f7b7b41a0`)
   - **Pexels**: Implementation complete, needs API key in `.env` file
   - **Picsum**: Placeholder images for testing
   - Automatic fallback chain: Pixabay → Pexels → Picsum
   - Multiple size options (preview, webformat, large, fullHD, original)
   - Orientation filtering (horizontal, vertical, all)
   - Category filtering (Pixabay)
   - Color filtering (Pexels)

3. **Comprehensive Template**
   - `content/guides/comprehensive_template.md` - Complete reference template
   - `generated/guides/comprehensive_template.pdf` - 2.3MB PDF with all features
   - Demonstrates: procedures, tips, warnings, tables, code blocks, images

4. **Experiment Tools**
   - `scripts/compare_image_apis.py` - Full API comparison
   - `scripts/experiment_formats.py` - Format/size testing
   - `scripts/experiment_queries.py` - Query strategy testing
   - `scripts/create_visual_comparison.py` - Visual PDF comparisons
   - All results in `generated/experiments/`

5. **Security & Quality**
   - Path validation
   - HTML sanitization (bleach optional)
   - PDF quality validation
   - Error handling with fallbacks

6. **Configuration**
   - API keys load from `/Users/ctavolazzi/Code/active/waft/.env`
   - `.env` file is in `.gitignore`
   - Both `PIXABAY_API_KEY` and `PEXELS_API_KEY` supported

### 📁 Key Files

- **Templates**: `templates/guide_template.py` (main template)
- **Image APIs**: `scripts/image_api.py` (Pixabay, Pexels, Picsum)
- **Image Processing**: `scripts/add_images.py` (replaces placeholders)
- **PDF Generation**: `scripts/generate_guide.py` (single guide)
- **Batch Processing**: `scripts/batch_generate.py` (multiple guides)
- **Gumroad Prep**: `scripts/gumroad_prep.py` (metadata generation)

### 📊 Experiment Results

- **Pixabay**: 10/10 queries successful, 4,457+ images available
- **Pexels**: Ready (needs API key), professional photos with attribution
- **Best Practices**: Use "large" size (1280px) for PDFs, simple queries work best

### 🎯 Current Template

The `comprehensive_template.md` includes:
- Image API examples (Pixabay, Pexels, Picsum)
- Step-by-step procedures with numbered circles
- Tips, warnings, and cautions
- Tables
- Code examples
- Multiple image sizes
- Troubleshooting sections
- Resources and attribution

## What's Working

✅ PDF generation with WeasyPrint
✅ Image API integration (Pixabay working, Pexels ready)
✅ All styling fixed (no more asterisks, shadows, or rendering issues)
✅ Comprehensive template with all features
✅ Experiment tools for API comparison
✅ Security and validation
✅ Gumroad preparation tools

## Next Steps / Ideas

1. **Add Pexels API key** to `.env` to enable full comparison
2. **Create production guides** using the comprehensive template
3. **Implement photographer attribution** in PDFs (Pexels requirement)
4. **Batch generate** multiple guides from manifest
5. **Optimize image sizes** for different use cases
6. **Add more templates** for different guide types

## Quick Commands

```bash
# Add images to a guide
python scripts/add_images.py \
  --content content/guides/my_guide.md \
  --provider pixabay \
  --query "succulent" \
  --size large

# Generate PDF
python scripts/generate_guide.py \
  --content content/guides/my_guide.md \
  --title "My Guide" \
  --output generated/guides/

# Run experiments
python scripts/compare_image_apis.py
python scripts/experiment_formats.py
python scripts/experiment_queries.py
```

## Project Location

`/Users/ctavolazzi/Code/active/waft/succulent_jewelry_pdfs/`

## Key Learnings

- Pixabay works immediately, great for production
- Pexels needs API key but provides professional photos
- Use "large" size (1280px) for PDF quality
- Simple queries work best
- Step numbers and tips render correctly with current CSS fixes
- Bold text in steps needs post-processing (markdown doesn't process inside HTML divs)

---

**Ready to continue:** The system is fully functional. You can create new guides, run experiments, or enhance existing features.
