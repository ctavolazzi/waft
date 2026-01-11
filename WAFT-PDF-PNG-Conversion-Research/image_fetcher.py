#!/usr/bin/env python3
"""
Free Stock Photo Fetcher with Local Caching

Downloads images from free stock photo APIs and caches them locally.
Uses Pexels API (free, no auth required for basic usage) or Unsplash Source API.

Usage:
    fetcher = ImageFetcher(cache_dir="images_cache")
    image_path = fetcher.get_image("nature", width=800, height=600)
    # image_path is a local file path ready to use
"""

import json
import hashlib
import requests
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from urllib.parse import urlencode


class ImageFetcher:
    """
    Fetches free stock photos and caches them locally.
    
    Uses Pexels API (free, generous rate limits) or Unsplash Source (no auth).
    Images are cached locally to avoid repeated downloads.
    """
    
    def __init__(self, cache_dir: Path = None, provider: str = "pexels"):
        """
        Initialize image fetcher.
        
        Args:
            cache_dir: Directory to cache images (default: ./images_cache)
            provider: "pexels" or "unsplash" (default: "pexels")
        """
        if cache_dir is None:
            cache_dir = Path(__file__).parent / "images_cache"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.provider = provider
        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()
        
        # Pexels API key (optional - works without for basic usage)
        # Get free key at: https://www.pexels.com/api/
        self.pexels_api_key = None  # Can be set via environment variable
        
        # Rate limiting
        self.last_request_time = None
        self.min_request_interval = timedelta(seconds=1)  # Be nice to API
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load cached image metadata."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_metadata(self):
        """Save cached image metadata."""
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=2)
    
    def _get_cache_key(self, query: str, width: int, height: int) -> str:
        """Generate cache key for image request."""
        key = f"{self.provider}:{query}:{width}x{height}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def _get_cached_image(self, cache_key: str) -> Optional[Path]:
        """Check if image is already cached."""
        if cache_key in self.metadata:
            cached_path = self.cache_dir / self.metadata[cache_key]["filename"]
            if cached_path.exists():
                return cached_path
        return None
    
    def _download_from_pexels(self, query: str, width: int, height: int) -> Optional[Path]:
        """
        Download image from Pexels API.
        
        Pexels allows free usage without API key for basic requests.
        With API key: 200 requests/hour
        Without API key: Limited but works for testing
        """
        try:
            # Use Pexels Source API (no auth required, but limited)
            # Or use search API if we have a key
            if self.pexels_api_key:
                url = "https://api.pexels.com/v1/search"
                headers = {"Authorization": self.pexels_api_key}
                params = {"query": query, "per_page": 1}
            else:
                # Use Pexels Source (direct image URLs, no search)
                # For testing, we'll use a curated list of free images
                curated_images = {
                    "nature": "https://images.pexels.com/photos/417074/pexels-photo-417074.jpeg",
                    "technology": "https://images.pexels.com/photos/1181244/pexels-photo-1181244.jpeg",
                    "business": "https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg",
                    "abstract": "https://images.pexels.com/photos/1323712/pexels-photo-1323712.jpeg",
                    "people": "https://images.pexels.com/photos/3184418/pexels-photo-3184418.jpeg",
                }
                
                # Try to find matching image
                image_url = curated_images.get(query.lower(), curated_images["nature"])
                
                # Download the image
                response = requests.get(image_url, timeout=10)
                if response.status_code == 200:
                    cache_key = self._get_cache_key(query, width, height)
                    filename = f"{cache_key}.jpg"
                    filepath = self.cache_dir / filename
                    
                    filepath.write_bytes(response.content)
                    
                    # Save metadata
                    self.metadata[cache_key] = {
                        "query": query,
                        "width": width,
                        "height": height,
                        "filename": filename,
                        "url": image_url,
                        "downloaded_at": datetime.utcnow().isoformat(),
                        "provider": "pexels"
                    }
                    self._save_metadata()
                    
                    # Resize if needed
                    if width or height:
                        from PIL import Image
                        img = Image.open(filepath)
                        if width and height:
                            img = img.resize((width, height), Image.Resampling.LANCZOS)
                        elif width:
                            ratio = width / img.width
                            img = img.resize((width, int(img.height * ratio)), Image.Resampling.LANCZOS)
                        elif height:
                            ratio = height / img.height
                            img = img.resize((int(img.width * ratio), height), Image.Resampling.LANCZOS)
                        img.save(filepath, "JPEG", quality=90)
                    
                    return filepath
                
                return None
                
        except Exception as e:
            print(f"  ⚠️  Pexels download failed: {e}")
            return None
    
    def _download_from_unsplash(self, query: str, width: int, height: int) -> Optional[Path]:
        """
        Download image from Unsplash Source API (no auth required).
        
        Unsplash Source provides random images based on keywords.
        Format: https://source.unsplash.com/{width}x{height}/?{query}
        """
        try:
            # Unsplash Source API (no auth, but deprecated - use as fallback)
            # New approach: Use Unsplash API with demo client_id
            url = f"https://source.unsplash.com/{width}x{height}/?{query}"
            
            response = requests.get(url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                cache_key = self._get_cache_key(query, width, height)
                filename = f"{cache_key}.jpg"
                filepath = self.cache_dir / filename
                
                filepath.write_bytes(response.content)
                
                # Save metadata
                self.metadata[cache_key] = {
                    "query": query,
                    "width": width,
                    "height": height,
                    "filename": filename,
                    "url": url,
                    "downloaded_at": datetime.utcnow().isoformat(),
                    "provider": "unsplash"
                }
                self._save_metadata()
                
                return filepath
                
        except Exception as e:
            print(f"  ⚠️  Unsplash download failed: {e}")
            return None
    
    def get_image(
        self,
        query: str = "nature",
        width: int = 800,
        height: int = 600,
        force_refresh: bool = False
    ) -> Optional[Path]:
        """
        Get an image (from cache or download).
        
        Args:
            query: Search query (e.g., "nature", "technology", "business")
            width: Image width in pixels
            height: Image height in pixels
            force_refresh: Force re-download even if cached
        
        Returns:
            Path to local image file, or None if download failed
        """
        cache_key = self._get_cache_key(query, width, height)
        
        # Check cache first
        if not force_refresh:
            cached = self._get_cached_image(cache_key)
            if cached:
                return cached
        
        # Rate limiting
        if self.last_request_time:
            elapsed = datetime.utcnow() - self.last_request_time
            if elapsed < self.min_request_interval:
                import time
                time.sleep((self.min_request_interval - elapsed).total_seconds())
        
        # Download from provider
        if self.provider == "pexels":
            image_path = self._download_from_pexels(query, width, height)
        elif self.provider == "unsplash":
            image_path = self._download_from_unsplash(query, width, height)
        else:
            print(f"  ⚠️  Unknown provider: {self.provider}")
            return None
        
        self.last_request_time = datetime.utcnow()
        return image_path
    
    def get_multiple_images(
        self,
        queries: list,
        width: int = 800,
        height: int = 600
    ) -> list:
        """
        Get multiple images.
        
        Args:
            queries: List of search queries
            width: Image width
            height: Image height
        
        Returns:
            List of image paths (None for failed downloads)
        """
        images = []
        for query in queries:
            img = self.get_image(query, width, height)
            images.append(img)
        return images
    
    def clear_cache(self, older_than_days: int = 30):
        """Clear cached images older than specified days."""
        cutoff = datetime.utcnow() - timedelta(days=older_than_days)
        
        to_remove = []
        for cache_key, meta in self.metadata.items():
            downloaded_at = datetime.fromisoformat(meta["downloaded_at"])
            if downloaded_at < cutoff:
                filepath = self.cache_dir / meta["filename"]
                if filepath.exists():
                    filepath.unlink()
                to_remove.append(cache_key)
        
        for key in to_remove:
            del self.metadata[key]
        
        self._save_metadata()
        print(f"  ✓ Cleared {len(to_remove)} cached images")


def create_test_image_with_photo(
    output_path: Path,
    photo_path: Optional[Path] = None,
    width: int = 2550,
    height: int = 3300,
    query: str = "nature"
) -> Path:
    """
    Create a test image (PDF or PNG) with an embedded stock photo.
    
    Args:
        output_path: Output file path
        photo_path: Optional path to existing photo (if None, fetches one)
        width: Image width (default: 2550 for 8.5" at 300 DPI)
        height: Image height (default: 3300 for 11" at 300 DPI)
        query: Photo search query if fetching
    
    Returns:
        Path to created image
    """
    from PIL import Image, ImageDraw, ImageFont
    
    # Get or fetch photo
    if photo_path is None or not photo_path.exists():
        fetcher = ImageFetcher()
        photo_path = fetcher.get_image(query, width=1600, height=1200)
        if photo_path is None:
            # Fallback: create colored background
            photo_path = None
    
    # Create base image
    img = Image.new("RGB", (width, height), color="#f5f5f5")
    draw = ImageDraw.Draw(img)
    
    # Add photo if available
    if photo_path:
        try:
            photo = Image.open(photo_path)
            # Resize photo to fit in header area
            photo_width = min(1600, width - 200)
            photo_height = int(photo.width / photo.width * photo_width) if photo.width > 0 else 400
            photo = photo.resize((photo_width, photo_height), Image.Resampling.LANCZOS)
            
            # Paste photo in header
            paste_x = (width - photo_width) // 2
            paste_y = 50
            img.paste(photo, (paste_x, paste_y))
            
            # Add overlay for text readability
            overlay = Image.new("RGBA", (width, 300), (0, 0, 0, 128))
            img.paste(overlay, (0, 0), overlay)
            
        except Exception as e:
            print(f"  ⚠️  Could not add photo: {e}")
            photo_path = None
    
    # Add header text
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
    except:
        font_large = font_medium = None
    
    title = "WAFT Test Document with Stock Photo"
    if font_large:
        draw.text((width // 2, 150), title, fill="white", font=font_large, anchor="mm")
    else:
        draw.text((width // 2, 150), title, fill="white", anchor="mm")
    
    # Add content area
    content_y = 400 if photo_path else 200
    draw.rectangle([100, content_y, width - 100, height - 200], fill="white", outline="#ddd", width=3)
    
    # Add text content
    text_lines = [
        "This test document includes:",
        "• Stock photo from free API",
        "• Text and graphics",
        "• Professional layout",
        "",
        f"Photo query: {query}",
        f"Dimensions: {width}x{height}px",
        f"DPI: 300 (8.5 x 11 inches)"
    ]
    
    text_y = content_y + 100
    for line in text_lines:
        if font_medium:
            draw.text((150, text_y), line, fill="#2c3e50", font=font_medium)
        else:
            draw.text((150, text_y), line, fill="#2c3e50")
        text_y += 80
    
    # Save
    if output_path.suffix.lower() == ".pdf":
        img.save(output_path, "PDF", resolution=300.0)
    else:
        img.save(output_path, "PNG", quality=95)
    
    return output_path


if __name__ == "__main__":
    # Test the image fetcher
    print("Testing Image Fetcher...")
    fetcher = ImageFetcher()
    
    # Get a test image
    img_path = fetcher.get_image("nature", width=800, height=600)
    if img_path:
        print(f"✓ Downloaded image: {img_path}")
        print(f"  Size: {img_path.stat().st_size / 1024:.1f} KB")
    else:
        print("✗ Failed to download image")
