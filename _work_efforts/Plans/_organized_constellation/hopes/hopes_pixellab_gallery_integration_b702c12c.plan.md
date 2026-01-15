---
name: PixelLab Gallery Integration
overview: Integrate the local pixellab client from the Code directory to pre-generate pixel art images and display them in a gallery section on the portfolio site.
todos:
  - id: copy_client_files
    content: Copy pixellab_client.py and config.py from Code directory to project root
    status: completed
  - id: create_scripts_dir
    content: Create scripts/ directory and generate_gallery.py script
    status: completed
  - id: create_assets_structure
    content: Create assets/gallery/images/ directory structure
    status: completed
  - id: implement_generation_script
    content: Implement generate_gallery.py with image generation and PNG conversion logic
    status: completed
  - id: add_gallery_section
    content: Add gallery section to index.html with VGA-Cinematic styling
    status: completed
  - id: setup_dependencies
    content: Create scripts/requirements.txt and .env.example
    status: completed
  - id: update_gitignore
    content: Update .gitignore to exclude .env but include generated images
    status: completed

category: hopes
confidence: 1.00
constellation_date: 2026-01-14
---

# PixelLab Gallery Integration Plan

## Overview

Add a pixel art gallery to the portfolio site by integrating the pixellab client from `/Users/ctavolazzi/Code/_personal_sandbox_CJT01/projects/api-testing-framework/`. Images will be pre-generated using the Python client and displayed in a new gallery section.

## Architecture

```
ctavolazzi.github.io/
├── scripts/
│   ├── generate_gallery.py      # Script to generate pixel art images
│   └── requirements.txt          # Python dependencies
├── assets/
│   └── gallery/                   # Generated pixel art images
│       ├── images/                # PNG files
│       └── metadata.json          # Image descriptions and metadata
├── pixellab_client.py             # Copied from Code directory
├── config.py                      # Copied from Code directory (simplified)
└── index.html                     # Updated with gallery section
```

## Implementation Steps

### 1. Copy Required Files

- Copy `pixellab_client.py` from `_personal_sandbox_CJT01/projects/api-testing-framework/`
- Copy `config.py` from same location (or create simplified version)
- Create `scripts/generate_gallery.py` for image generation

### 2. Create Image Generation Script

Create `scripts/generate_gallery.py` that:

- Uses `pixellab_client.PixelLabClient` to generate images
- Generates a curated set of pixel art images (e.g., 6-12 images)
- Saves images as PNG files in `assets/gallery/images/`
- Creates `metadata.json` with descriptions and generation info
- Handles base64-to-PNG conversion from API responses

### 3. Add Gallery Section to Portfolio

Update `index.html`:

- Add new section after projects or in a dedicated area
- Display images in a grid layout matching the VGA-Cinematic aesthetic
- Include image descriptions from metadata
- Use existing card/panel styling for consistency

### 4. Dependencies and Setup

- Create `scripts/requirements.txt` with minimal dependencies:
  - `requests>=2.31.0`
  - `python-dotenv>=1.0.0`
  - `Pillow>=10.0.0` (for image processing)
- Add `.env.example` with `PIXELLAB_API_KEY` placeholder
- Update `.gitignore` to exclude `.env` but include generated images

### 5. Generation Workflow

- Run `python scripts/generate_gallery.py` locally to generate images
- Commit generated images to repo (they're part of the static site)
- Images are served directly from GitHub Pages
- Re-run generation script when new images are needed

## Technical Considerations

### Simplified Config

Since this is a simple use case, `config.py` can be simplified to:

- Always use LIVE mode (no mock/fixture system needed)
- Remove component override logic (not needed for single-purpose script)

### Image Storage

- Store images as PNG files in `assets/gallery/images/`
- Use descriptive filenames: `wizard_64x64.png`, `knight_128x128.png`
- Keep metadata in JSON for easy frontend consumption

### Gallery Design

- Match existing VGA-Cinematic aesthetic
- Use terminal-style borders and dithering effects
- Grid layout with hover effects
- Responsive design for mobile

## Files to Create/Modify

1. **New Files:**

   - `scripts/generate_gallery.py`
   - `scripts/requirements.txt`
   - `pixellab_client.py` (copied)
   - `config.py` (copied, simplified)
   - `assets/gallery/images/.gitkeep`
   - `.env.example`

2. **Modified Files:**

   - `index.html` (add gallery section)
   - `.gitignore` (add `.env`, keep `assets/gallery/`)

## Usage

```bash
# Setup
cd /Users/ctavolazzi/Code/ctavolazzi.github.io
pip install -r scripts/requirements.txt
cp .env.example .env
# Edit .env and add PIXELLAB_API_KEY

# Generate images
python scripts/generate_gallery.py

# Commit and push
git add assets/gallery/
git commit -m "Add pixel art gallery"
git push
```

## Next Steps After Implementation

- Generate initial set of images
- Test gallery display on portfolio
- Consider add