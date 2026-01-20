"""
Image API Utilities
===================

Utilities for fetching images from public APIs (Picsum, Pexels, Pixabay) for use in PDFs.
"""

import logging
import os
import requests
from pathlib import Path
from typing import Optional, Dict
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def load_env_file(env_path: Optional[Path] = None) -> Dict[str, str]:
    """
    Load environment variables from .env file.
    
    Args:
        env_path: Path to .env file (defaults to parent directory)
    
    Returns:
        Dictionary of environment variables
    """
    if env_path is None:
        # Look for .env in parent directory (waft root)
        env_path = Path(__file__).parent.parent.parent / '.env'
    
    env_vars = {}
    if env_path.exists():
        try:
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        env_vars[key] = value
        except Exception as e:
            logger.debug(f"Could not load .env file: {e}")
    
    return env_vars


# Load .env file once at module import
_ENV_VARS = load_env_file()


class ImageAPI:
    """Base class for image API clients."""
    
    def get_image_url(self, width: int, height: int, **kwargs) -> str:
        """Get image URL from API."""
        raise NotImplementedError


class PicsumAPI(ImageAPI):
    """
    Picsum Photos API client.
    
    Simple placeholder images - perfect for testing and placeholders.
    https://picsum.photos/
    """
    
    BASE_URL = "https://picsum.photos"
    
    def get_image_url(
        self,
        width: int = 800,
        height: int = 600,
        image_id: Optional[int] = None,
        seed: Optional[str] = None,
        grayscale: bool = False,
        blur: Optional[int] = None
    ) -> str:
        """
        Get Picsum image URL.
        
        Args:
            width: Image width in pixels
            height: Image height in pixels
            image_id: Specific image ID (optional)
            seed: Seed for consistent random image (optional)
            grayscale: Convert to grayscale
            blur: Blur amount (1-10, optional)
        
        Returns:
            Image URL
        """
        # Build URL path
        if image_id is not None:
            path = f"/id/{image_id}/{width}/{height}"
        elif seed:
            path = f"/seed/{seed}/{width}/{height}"
        else:
            path = f"/{width}/{height}"
        
        # Build query parameters
        params = []
        if grayscale:
            params.append("grayscale")
        if blur is not None:
            if blur:
                params.append(f"blur={blur}")
            else:
                params.append("blur")
        
        url = f"{self.BASE_URL}{path}"
        if params:
            url += "?" + "&".join(params)
        
        return url
    
    def get_square_image(self, size: int = 600, **kwargs) -> str:
        """Get square image."""
        return self.get_image_url(width=size, height=size, **kwargs)


class PixabayAPI(ImageAPI):
    """
    Pixabay API client.
    
    Royalty-free images and videos - perfect for professional guides.
    API key: 29486486-de7f8c25dff5fd83f7b7b41a0
    Documentation: https://pixabay.com/api/docs/
    """
    
    BASE_URL = "https://pixabay.com/api"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Pixabay API client.
        
        Args:
            api_key: Pixabay API key (optional, checks .env file, then env var, then defaults)
        """
        # Try: provided key -> .env file -> environment variable -> default
        self.api_key = (
            api_key or 
            _ENV_VARS.get('PIXABAY_API_KEY') or 
            os.getenv('PIXABAY_API_KEY') or 
            "29486486-de7f8c25dff5fd83f7b7b41a0"
        )
    
    def search_images(
        self,
        query: str,
            per_page: int = 3,  # Minimum is 3 per API docs
        page: int = 1,
        image_type: str = "photo",
        orientation: str = "horizontal",
        category: Optional[str] = None,
        min_width: int = 800,
        min_height: int = 600,
        safesearch: bool = True,
        order: str = "popular"
    ) -> Optional[Dict]:
        """
        Search for images on Pixabay.
        
        Args:
            query: Search query (e.g., "succulent", "jewelry")
            per_page: Number of results per page (3-200)
            page: Page number
            image_type: "all", "photo", "illustration", "vector"
            orientation: "all", "horizontal", "vertical"
            category: Filter by category (optional)
            min_width: Minimum image width
            min_height: Minimum image height
            safesearch: Safe search filter
            order: "popular" or "latest"
        
        Returns:
            API response dictionary or None if error
        """
        url = f"{self.BASE_URL}/"
        params = {
            "key": self.api_key,
            "q": query,
            "per_page": min(max(per_page, 3), 200),
            "page": page,
            "image_type": image_type,
            "orientation": orientation,
            "min_width": min_width,
            "min_height": min_height,
            "safesearch": "true" if safesearch else "false",
            "order": order
        }
        
        if category:
            params["category"] = category
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Pixabay API error: {e}")
            return None
    
    def get_image_url(
        self,
        width: int = 800,
        height: int = 600,
        query: str = "nature",
        size: str = "large",
        **kwargs
    ) -> str:
        """
        Get Pixabay image URL by searching.
        
        Args:
            width: Desired width (used for min_width filter)
            height: Desired height (used for min_height filter)
            query: Search query for image
            size: Image size to return ("preview", "webformat", "large", "fullHD", "image")
            **kwargs: Additional search parameters
        
        Returns:
            Image URL (or Picsum fallback if API fails)
        """
        result = self.search_images(
            query=query,
            per_page=1,
            min_width=width,
            min_height=height,
            **kwargs
        )
        
        if result and result.get('hits') and len(result['hits']) > 0:
            hit = result['hits'][0]
            
            # Choose URL based on size parameter
            if size == "preview":
                return hit.get('previewURL', '')
            elif size == "webformat":
                # Can modify _640 to _180, _340, _960
                url = hit.get('webformatURL', '')
                if width <= 180:
                    return url.replace('_640', '_180') if '_640' in url else url
                elif width <= 340:
                    return url.replace('_640', '_340') if '_640' in url else url
                elif width <= 960:
                    return url.replace('_640', '_960') if '_640' in url else url
                return url
            elif size == "large":
                return hit.get('largeImageURL', '')
            elif size == "fullHD":
                return hit.get('fullHDURL', hit.get('largeImageURL', ''))
            elif size == "image":
                return hit.get('imageURL', hit.get('largeImageURL', ''))
            else:
                # Default to large
                return hit.get('largeImageURL', hit.get('webformatURL', ''))
        
        # Fallback to Picsum if Pixabay fails
        logger.warning(f"Pixabay search failed for '{query}', using Picsum fallback")
        picsum = PicsumAPI()
        return picsum.get_image_url(width, height)


class PexelsAPI(ImageAPI):
    """
    Pexels API client.
    
    Real, high-quality photos - perfect for professional guides.
    Requires API key: https://www.pexels.com/api/
    """
    
    BASE_URL = "https://api.pexels.com/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Pexels API client.
        
        Args:
            api_key: Pexels API key (optional, checks .env file, then env var)
        """
        # Try: provided key -> .env file -> environment variable
        self.api_key = (
            api_key or 
            _ENV_VARS.get('PEXELS_API_KEY') or 
            os.getenv('PEXELS_API_KEY')
        )
        if not self.api_key:
            logger.warning(
                "Pexels API key not provided. "
                "Set PEXELS_API_KEY in .env file, environment variable, or pass api_key."
            )
    
    def search_photos(
        self,
        query: str,
        per_page: int = 1,
        page: int = 1,
        orientation: Optional[str] = None,
        size: Optional[str] = None,
        color: Optional[str] = None,
        locale: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Search for photos on Pexels.
        
        Args:
            query: Search query (e.g., "succulent", "jewelry")
            per_page: Number of results per page (1-80, default: 1)
            page: Page number (default: 1)
            orientation: "landscape", "portrait", or "square" (optional)
            size: "large" (24MP), "medium" (12MP), or "small" (4MP) (optional)
            color: Filter by color (optional)
            locale: Locale code (optional)
        
        Returns:
            API response dictionary or None if error
        """
        if not self.api_key:
            logger.error("Pexels API key required for search")
            return None
        
        url = f"{self.BASE_URL}/search"
        headers = {"Authorization": self.api_key}
        params = {
            "query": query,
            "per_page": min(max(per_page, 1), 80),  # API limit: 1-80
            "page": page
        }
        
        # Add optional parameters
        if orientation:
            params["orientation"] = orientation
        if size:
            params["size"] = size
        if color:
            params["color"] = color
        if locale:
            params["locale"] = locale
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Pexels API error: {e}")
            return None
    
    def get_image_url(
        self,
        width: int = 800,
        height: int = 600,
        query: str = "nature",
        **kwargs
    ) -> str:
        """
        Get Pexels image URL by searching.
        
        Args:
            width: Desired width
            height: Desired height
            query: Search query for image
            **kwargs: Additional search parameters
        
        Returns:
            Image URL (or Picsum fallback if API fails)
        """
        result = self.search_photos(query=query, per_page=1, **kwargs)
        
        if result and result.get('photos') and len(result['photos']) > 0:
            photo = result['photos'][0]
            # Get the best size based on requested dimensions
            src = photo.get('src', {})
            
            # Choose size based on width/height requirements
            if width >= 1200 or height >= 1200:
                return src.get('large2x') or src.get('original') or src.get('large', '')
            elif width >= 650 or height >= 650:
                return src.get('large') or src.get('original') or src.get('medium', '')
            elif width >= 350 or height >= 350:
                return src.get('medium') or src.get('large') or src.get('small', '')
            else:
                return src.get('small') or src.get('medium') or src.get('tiny', '')
        
        # Fallback to Picsum if Pexels fails
        logger.warning(f"Pexels search failed for '{query}', using Picsum fallback")
        picsum = PicsumAPI()
        return picsum.get_image_url(width, height)


def get_placeholder_image(
    width: int = 800,
    height: int = 600,
    provider: str = "picsum",
    fallback: bool = True,
    **kwargs
) -> str:
    """
    Get placeholder image URL from specified provider.
    
    Args:
        width: Image width
        height: Image height
        provider: "picsum", "pexels", or "pixabay"
        fallback: If True, try other providers if primary fails
        **kwargs: Provider-specific arguments
    
    Returns:
        Image URL
    """
    if provider.lower() == "pixabay":
        api_key = kwargs.pop('api_key', None)
        api = PixabayAPI(api_key=api_key)
        query = kwargs.pop('query', 'nature')
        size = kwargs.pop('size', 'large')
        url = api.get_image_url(width, height, query=query, size=size, **kwargs)
        # If fallback enabled and Pixabay failed (returned Picsum), try Pexels
        if fallback and url.startswith('https://picsum'):
            try:
                pexels_api = PexelsAPI()
                pexels_url = pexels_api.get_image_url(width, height, query=query, **kwargs)
                if pexels_url and not pexels_url.startswith('https://picsum'):
                    return pexels_url
            except:
                pass
        return url
    elif provider.lower() == "pexels":
        api_key = kwargs.pop('api_key', None)
        api = PexelsAPI(api_key=api_key)
        query = kwargs.pop('query', 'nature')
        url = api.get_image_url(width, height, query=query, **kwargs)
        # If fallback enabled and Pexels failed, try Pixabay
        if fallback and url.startswith('https://picsum'):
            try:
                pixabay_api = PixabayAPI()
                pixabay_url = pixabay_api.get_image_url(width, height, query=query, size='large', **kwargs)
                if pixabay_url and not pixabay_url.startswith('https://picsum'):
                    return pixabay_url
            except:
                pass
        return url
    else:
        # Default to Picsum
        api = PicsumAPI()
        return api.get_image_url(width, height, **kwargs)


def validate_image_url(url: str, timeout: int = 5) -> bool:
    """
    Validate that an image URL is accessible.
    
    Args:
        url: Image URL to validate
        timeout: Request timeout in seconds
    
    Returns:
        True if URL is accessible, False otherwise
    """
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        content_type = response.headers.get('content-type', '')
        return response.status_code == 200 and content_type.startswith('image/')
    except Exception as e:
        logger.warning(f"Image URL validation failed for {url}: {e}")
        return False


def download_image(url: str, output_path: Path, timeout: int = 30) -> bool:
    """
    Download image from URL to local file.
    
    Args:
        url: Image URL
        output_path: Where to save image
        timeout: Request timeout in seconds
    
    Returns:
        True if successful, False otherwise
    """
    try:
        response = requests.get(url, timeout=timeout, stream=True)
        response.raise_for_status()
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        logger.info(f"Downloaded image: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to download image from {url}: {e}")
        return False
