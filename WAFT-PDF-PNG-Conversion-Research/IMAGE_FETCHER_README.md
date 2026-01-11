# Image Fetcher - Free Stock Photo Integration

**Purpose**: Download and cache free stock photos for use in test documents

## Features

- ✅ **Free API**: Uses Pexels (no auth required for basic usage)
- ✅ **Local Caching**: Downloads images once, reuses from cache
- ✅ **Lightweight**: Pure Python, only requires `requests` and `PIL`
- ✅ **Automatic**: Integrated into test suite

## Usage

### Basic Usage

```python
from image_fetcher import ImageFetcher

# Initialize fetcher
fetcher = ImageFetcher(cache_dir="images_cache")

# Get an image (downloads and caches)
image_path = fetcher.get_image("nature", width=800, height=600)
# Returns: Path to local cached image file
```

### Create Test Document with Photo

```python
from image_fetcher import create_test_image_with_photo

# Create PDF or PNG with embedded stock photo
output_path = Path("test_document.pdf")
create_test_image_with_photo(
    output_path,
    query="technology",  # Search term
    width=2550,  # 8.5" at 300 DPI
    height=3300  # 11" at 300 DPI
)
```

### Get Multiple Images

```python
queries = ["nature", "technology", "business", "abstract"]
images = fetcher.get_multiple_images(queries, width=800, height=600)
# Returns: List of image paths
```

## Cache Management

Images are cached in `images_cache/` directory:
- **Metadata**: `metadata.json` tracks all cached images
- **Files**: Images stored as `{hash}.jpg`
- **Automatic**: Same query + size = same cached file

### Clear Old Cache

```python
fetcher.clear_cache(older_than_days=30)  # Remove images older than 30 days
```

## API Providers

### Pexels (Default)
- **Free**: No API key required for basic usage
- **Rate Limits**: Generous (200/hour with key, limited without)
- **Quality**: High-quality photos
- **Get API Key**: https://www.pexels.com/api/ (optional)

### Unsplash (Fallback)
- **Free**: No auth required
- **Format**: `https://source.unsplash.com/{width}x{height}/?{query}`
- **Note**: Source API is deprecated but still works

## Cache Structure

```
images_cache/
├── metadata.json          # Cache index
├── {hash1}.jpg           # Cached image 1
├── {hash2}.jpg           # Cached image 2
└── ...
```

## Integration with Test Suite

The test suite automatically uses stock photos when available:

1. **Phase 1 (PDF→PNG)**: Creates PDF with stock photo
2. **Phase 2 (PNG→PDF)**: Uses cached photos from Phase 1
3. **Fallback**: If photo fetch fails, uses generated graphics

## Example Queries

- `"nature"` - Nature/landscape photos
- `"technology"` - Tech/computer photos
- `"business"` - Business/office photos
- `"abstract"` - Abstract/artistic photos
- `"people"` - People/portrait photos

## Benefits

1. **Real Photos**: Test with actual photos, not just graphics
2. **Local Storage**: No repeated downloads
3. **Free**: No API costs
4. **Lightweight**: Minimal dependencies
5. **Automatic**: Integrated into test workflow

## Requirements

- `requests` - For API calls
- `PIL/Pillow` - For image processing (already in WAFT dependencies)

## Notes

- First run downloads images (may take a few seconds)
- Subsequent runs use cached images (instant)
- Cache persists between test runs
- Images are automatically resized to requested dimensions
