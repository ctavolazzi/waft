# Image API Guide

Guide to using public image APIs (Picsum and Pexels in your PDF guides.

## Quick Start

### Picsum (Placeholder Images)

Picsum provides simple placeholder images - perfect for testing and placeholders.

**In your markdown:**
```markdown
![placeholder]
![placeholder:800:600]  # Custom size
```

**Process with:**
```bash
python scripts/add_images.py \
  --content content/guides/my_guide.md \
  --provider picsum
```

**Direct URL examples:**
- `https://picsum.photos/800/600` - Random 800x600 image
- `https://picsum.photos/600` - Square 600x600 image
- `https://picsum.photos/id/237/800/600` - Specific image (dog)
- `https://picsum.photos/seed/picsum/800/600` - Consistent random image
- `https://picsum.photos/800/600?grayscale` - Grayscale
- `https://picsum.photos/800/600?blur=2` - Blurred

### Pexels (Real Photos)

Pexels provides real, high-quality photos - perfect for professional guides.

**Setup:**
1. Get API key: https://www.pexels.com/api/
2. Set environment variable: `export PEXELS_API_KEY=your_key`

**In your markdown:**
```markdown
![placeholder:pexels:800:600]
```

**Process with:**
```bash
python scripts/add_images.py \
  --content content/guides/my_guide.md \
  --provider pexels \
  --query "succulent" \
  --pexels-api-key $PEXELS_API_KEY
```

## Usage in Templates

### In Markdown Content

Use placeholder syntax that gets replaced:

```markdown
## My Section

![placeholder:800:600]

<div class="image-caption">A beautiful succulent</div>
```

### In Python Code

```python
from scripts.image_api import get_placeholder_image, PicsumAPI, PexelsAPI

# Simple placeholder
url = get_placeholder_image(width=800, height=600, provider="picsum")

# Picsum with options
picsum = PicsumAPI()
url = picsum.get_image_url(
    width=800,
    height=600,
    image_id=237,  # Specific image
    grayscale=True,
    blur=2
)

# Pexels search
pexels = PexelsAPI(api_key="your_key")
url = pexels.get_image_url(
    width=800,
    height=600,
    query="succulent jewelry"
)
```

## Image Providers

### Picsum Photos

**Pros:**
- ✅ No API key required
- ✅ Fast and reliable
- ✅ Good for placeholders
- ✅ Many options (grayscale, blur, specific images)

**Cons:**
- ❌ Not real photos (placeholders)
- ❌ Limited control over content

**Best for:** Testing, placeholders, quick prototypes

**Documentation:** https://picsum.photos/

### Pexels

**Pros:**
- ✅ Real, high-quality photos
- ✅ Search by keyword
- ✅ Professional quality
- ✅ Free for commercial use

**Cons:**
- ❌ Requires API key
- ❌ Rate limits (200 requests/hour on free tier)
- ❌ Requires internet connection

**Best for:** Production guides, professional content

**Documentation:** https://www.pexels.com/api/

## Examples

### Example 1: Simple Placeholder

```markdown
# My Guide

![placeholder]

This is my guide content.
```

Process:
```bash
python scripts/add_images.py --content my_guide.md --provider picsum
```

Result:
```markdown
# My Guide

![Image](https://picsum.photos/800/600)

This is my guide content.
```

### Example 2: Custom Size

```markdown
![placeholder:1200:800]
```

Process:
```bash
python scripts/add_images.py --content my_guide.md --width 1200 --height 800
```

### Example 3: Pexels with Search

```markdown
![placeholder:pexels:800:600]
```

Process:
```bash
python scripts/add_images.py \
  --content my_guide.md \
  --provider pexels \
  --query "jewelry casting" \
  --pexels-api-key $PEXELS_API_KEY
```

### Example 4: Multiple Images

```markdown
## Section 1

![placeholder:800:600]

<div class="image-caption">First image</div>

## Section 2

![placeholder:pexels:800:600]

<div class="image-caption">Second image</div>
```

## Tips

1. **Use Picsum for testing** - Fast, no API key needed
2. **Use Pexels for production** - Real photos, professional quality
3. **Add captions** - Use `<div class="image-caption">` for image descriptions
4. **Optimize sizes** - Use appropriate dimensions (800x600 is good for PDFs)
5. **Cache images** - Consider downloading images locally for offline generation

## Troubleshooting

### Picsum not loading

- Check internet connection
- Verify URL format: `https://picsum.photos/800/600`
- Try different image ID: `https://picsum.photos/id/237/800/600`

### Pexels API errors

- Verify API key is set: `echo $PEXELS_API_KEY`
- Check rate limits (200/hour on free tier)
- Verify search query is valid
- Check API status: https://status.pexels.com/

### Images not appearing in PDF

- Verify image URLs are accessible
- Check WeasyPrint can access external URLs
- Consider downloading images locally first
- Check PDF generation logs for errors
