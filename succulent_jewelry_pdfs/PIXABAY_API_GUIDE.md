# Pixabay API Integration Guide

**API Key**: `29486486-de7f8c25dff5fd83f7b7b41a0`  
**Documentation**: https://pixabay.com/api/docs/

## Overview

Pixabay provides royalty-free images perfect for professional PDF guides. The API is now integrated into the succulent jewelry PDF system.

## Features

- ✅ **Royalty-free images** - Safe for commercial use
- ✅ **High-quality photos** - Multiple size options
- ✅ **Search by keyword** - Find relevant images
- ✅ **No API key needed** - Key already configured
- ✅ **Rate limit**: 100 requests per 60 seconds

## Usage

### In Markdown Content

Use placeholder syntax that gets replaced:

```markdown
![placeholder:pixabay:800:600]
```

Or use the add_images script:

```bash
python scripts/add_images.py \
  --content content/guides/my_guide.md \
  --provider pixabay \
  --query "succulent plant" \
  --width 800 \
  --height 600
```

### In Python Code

```python
from scripts.image_api import PixabayAPI

api = PixabayAPI()

# Search for images
result = api.search_images(
    query="succulent plant",
    per_page=3,
    min_width=800,
    min_height=600
)

# Get image URL
url = api.get_image_url(
    width=800,
    height=600,
    query="succulent",
    size="large"  # Options: preview, webformat, large, fullHD, image
)
```

## Image Sizes

Pixabay provides multiple image sizes:

- **preview**: 150px max (previewURL)
- **webformat**: 640px max (webformatURL) - can modify to _180, _340, _960
- **large**: 1280px max (largeImageURL) - **Recommended for PDFs**
- **fullHD**: 1920px max (fullHDURL)
- **image**: Original resolution (imageURL)

## Search Parameters

### Basic Search

```python
api.search_images(
    query="succulent",
    per_page=3,
    image_type="photo",  # "all", "photo", "illustration", "vector"
    orientation="horizontal",  # "all", "horizontal", "vertical"
    min_width=800,
    min_height=600,
    safesearch=True,
    order="popular"  # "popular" or "latest"
)
```

### Category Filter

Available categories:
- backgrounds, fashion, nature, science, education
- feelings, health, people, religion, places
- animals, industry, computer, food, sports
- transportation, travel, buildings, business, music

```python
api.search_images(
    query="plant",
    category="nature",
    per_page=5
)
```

## Example Queries for Succulent Guides

- `"succulent plant"` - General succulents
- `"succulent varieties"` - Different types
- `"succulent garden"` - Garden arrangements
- `"plant care"` - Care instructions
- `"handmade jewelry"` - Jewelry making
- `"indoor plants"` - Indoor setups

## Response Format

```json
{
  "total": 4692,
  "totalHits": 500,
  "hits": [
    {
      "id": 195893,
      "largeImageURL": "https://pixabay.com/get/...",
      "webformatURL": "https://pixabay.com/get/...",
      "tags": "succulent, plant, nature",
      "views": 7671,
      "downloads": 6439,
      "likes": 5
    }
  ]
}
```

## Best Practices

1. **Use large images for PDFs** - Set `size="large"` for best quality
2. **Cache results** - API requires 24-hour caching
3. **Respect rate limits** - 100 requests per 60 seconds
4. **Use specific queries** - Better results with specific terms
5. **Download for production** - Hotlinking not allowed for permanent use

## Attribution

**Important**: When displaying search results, show users where images are from. For PDFs, this is typically handled in the credits/attribution section.

## Comparison with Other APIs

| Feature | Pixabay | Pexels | Picsum |
|---------|---------|--------|--------|
| Real Photos | ✅ | ✅ | ❌ |
| API Key | ✅ (provided) | ✅ (needed) | ❌ |
| Free | ✅ | ✅ | ✅ |
| Commercial Use | ✅ | ✅ | ✅ |
| Search | ✅ | ✅ | ❌ |
| Rate Limit | 100/min | 200/hour | None |

## Troubleshooting

### 400 Bad Request
- Check query encoding (use URL encoding)
- Verify parameter values are valid
- Some queries may not return results

### No Results
- Try broader search terms
- Remove min_width/min_height filters
- Check spelling

### Rate Limit
- Wait 60 seconds between batches
- Cache results for 24 hours
- Use fewer requests per operation

## Integration Status

✅ PixabayAPI class added to `scripts/image_api.py`  
✅ `get_placeholder_image()` supports pixabay  
✅ `add_images.py` script supports pixabay  
✅ API key configured  
✅ Succulent care guide updated with Pixabay images
