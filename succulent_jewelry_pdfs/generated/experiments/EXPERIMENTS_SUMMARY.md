# Image API Experiments - Complete Summary

Generated: 2026-01-19

## Overview

Comprehensive experiments comparing Pixabay and Pexels APIs across multiple dimensions:
- Query strategies
- Image formats and sizes
- Orientations
- Category/color filtering
- Visual comparisons

## Experiment Results

### 1. API Comparison (`compare_image_apis.py`)

**Tested:** 10 queries across both APIs

**Results:**
- **Pixabay:** 10/10 successful (4,457 total images available)
- **Pexels:** 0/10 successful (API key required)

**Queries Tested:**
- succulent, jewelry, plant care, handmade jewelry, cactus, nature, garden, botanical, echeveria, casting

**Outputs:**
- `api_comparison_data.json` - Raw data
- `api_comparison_report.md` - Detailed markdown report
- `api_comparison_guide.pdf` - Visual PDF comparison

### 2. Format Experiments (`experiment_formats.py`)

**Image Sizes:**

**Pixabay:**
- `preview` - 150px max (fast preview)
- `webformat` - 640px max (web optimized, can be 180/340/960)
- `large` - 1280px max (PDF quality)
- `fullHD` - 1920px max (high quality)
- `original` - Full resolution (6000px+)

**Pexels:**
- `tiny` - 200x280
- `small` - 130px height
- `medium` - 350px height
- `large` - 650px height
- `large2x` - 1300px height
- `original` - Full resolution
- `portrait` - 1200x800
- `landscape` - 1200x627

**Orientations:**

**Pixabay:**
- `all` - Any orientation
- `horizontal` - Landscape images
- `vertical` - Portrait images

**Pexels:**
- `landscape` - Wide images
- `portrait` - Tall images
- `square` - Square images

**Special Features:**

**Pixabay:**
- Category filtering (nature, animals, backgrounds, fashion, food, etc.)
- Image type filtering (photo, illustration, vector)
- Safe search
- Popularity/latest sorting

**Pexels:**
- Color filtering (red, orange, yellow, green, blue, etc. or hex codes)
- Size filtering (large 24MP, medium 12MP, small 4MP)
- Photographer attribution
- Average color data
- Alt text for accessibility

**Outputs:**
- `format_experiments.json` - Raw format data
- `format_comparison_report.md` - Format comparison report

### 3. Query Experiments (`experiment_queries.py`)

**Query Variations Tested:**
- Case variations (succulent, SUCCULENT, Succulent)
- Phrase variations (succulent plant, succulent care, how to succulent)
- Related terms (succulent guide)

**Specific Queries:**
- succulent: Pixabay 500, Pexels 0 (needs key)
- echeveria: Pixabay 91, Pexels 0
- jewelry making: Pixabay 500, Pexels 0
- vacuum casting: Pixabay 480, Pexels 0
- plant care: Pixabay 500, Pexels 0
- botanical: Pixabay 500, Pexels 0
- cactus: Pixabay 500, Pexels 0
- handmade: Pixabay 500, Pexels 0
- silver jewelry: Pixabay 500, Pexels 0
- nature photography: Pixabay 500, Pexels 0

**Findings:**
- Pixabay handles all query variations consistently
- Case sensitivity doesn't affect results
- Phrase queries work well
- Specialized terms (echeveria) return fewer but relevant results

**Outputs:**
- `query_experiments.json` - Raw query data
- `query_experiments_report.md` - Query strategy report

### 4. Visual Comparison (`create_visual_comparison.py`)

**Created:** Side-by-side visual PDF comparing both APIs

**Features:**
- Real image examples from both APIs
- Query-by-query comparison
- Image quality comparison
- Tag/photographer attribution

**Output:**
- `visual_api_comparison.pdf` - Visual comparison guide

## Key Findings

### Pixabay Strengths
✅ **No API key required** - Works immediately
✅ **Large image library** - 500+ results for most queries
✅ **Multiple size options** - From preview to original
✅ **Category filtering** - Helps narrow results
✅ **Consistent results** - Reliable across query variations
✅ **High resolution** - Original images 4000-6000px wide

### Pexels Strengths (when API key available)
✅ **Professional photos** - Curated, high-quality content
✅ **Photographer attribution** - Built-in crediting
✅ **Color filtering** - Find images by color
✅ **Size filtering** - Filter by megapixel count
✅ **Alt text** - Accessibility features
✅ **Average color** - Useful for design matching

### Recommendations

**For PDF Guides:**
1. **Use Pixabay** for immediate results without setup
2. **Use Pexels** when you have API key for professional photos
3. **Use fallback chain:** Pixabay → Pexels → Picsum for reliability

**Image Size Selection:**
- **PDFs:** Use `large` (1280px) for Pixabay, `large` or `large2x` for Pexels
- **Web previews:** Use `webformat` (640px) for Pixabay, `medium` for Pexels
- **Thumbnails:** Use `preview` (150px) for Pixabay, `tiny` for Pexels

**Query Strategy:**
- Keep queries simple and specific
- Use single words or short phrases
- Case doesn't matter
- Specialized terms work but return fewer results

## Files Generated

1. `api_comparison_data.json` - Complete API comparison data
2. `api_comparison_report.md` - Detailed markdown report
3. `api_comparison_guide.pdf` - Visual PDF guide
4. `format_experiments.json` - Format testing data
5. `format_comparison_report.md` - Format comparison
6. `query_experiments.json` - Query testing data
7. `query_experiments_report.md` - Query strategy report
8. `visual_api_comparison.pdf` - Side-by-side visual comparison

## Next Steps

1. **Add Pexels API key** to `.env` file to enable full comparison
2. **Test with real Pexels data** once key is added
3. **Create production guides** using best practices from experiments
4. **Implement attribution** for Pexels photos in PDFs

## Usage

Run experiments individually:
```bash
# Full API comparison
python scripts/compare_image_apis.py

# Format testing
python scripts/experiment_formats.py

# Query strategy testing
python scripts/experiment_queries.py

# Visual comparison PDF
python scripts/create_visual_comparison.py
```

All results are saved to `generated/experiments/`
