#!/usr/bin/env python3
"""
Download LHC Team Photos from CERN Archives

Downloads photos from CERN archive URLs and saves them locally.
Handles both direct image URLs and HTML pages with embedded images.
"""

import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests

# Photo sources from research
PHOTO_SOURCES = {
    "evans_lyn": {
        "name": "Lyn Evans",
        "urls": [
            "https://cds.cern.ch/images/CERN-GE-0705011-01",
        ],
        "output": "evans_lyn.jpg",
    },
    "heuer_rolf_dieter": {
        "name": "Rolf-Dieter Heuer",
        "urls": [
            "https://cds.cern.ch/images/CERN-HI-0901002-07",
            "https://commons.wikimedia.org/wiki/File:Portrait_de_Rolf-Dieter_Heuer_2.jpg",
        ],
        "output": "heuer_rolf_dieter.jpg",
    },
    "aymar_robert": {
        "name": "Robert Aymar",
        "urls": [
            "https://home.cern/news/obituary/cern/robert-aymar-1936-2024",
        ],
        "output": "aymar_robert.jpg",
    },
}

OUTPUT_DIR = Path(__file__).parent / "lhc_team_photos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def is_image_url(url: str) -> bool:
    """Check if URL points directly to an image."""
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
    parsed = urlparse(url)
    path_lower = parsed.path.lower()
    return any(path_lower.endswith(ext) for ext in image_extensions)


def extract_image_from_cern_html(html_content: str, base_url: str) -> str | None:
    """Extract image URL from CERN HTML page."""
    # CERN archive pages often have images in various formats
    # Look for common patterns

    # Pattern 1: Direct image links in <img> tags
    img_pattern = r'<img[^>]+src=["\']([^"\']+\.(?:jpg|jpeg|png|gif))["\']'
    matches = re.findall(img_pattern, html_content, re.IGNORECASE)
    if matches:
        # Prefer larger images or specific archive images
        for match in matches:
            if "cern" in match.lower() or "archive" in match.lower():
                return urljoin(base_url, match)
        return urljoin(base_url, matches[0])

    # Pattern 2: Links to image files
    link_pattern = r'href=["\']([^"\']+\.(?:jpg|jpeg|png|gif))["\']'
    matches = re.findall(link_pattern, html_content, re.IGNORECASE)
    if matches:
        for match in matches:
            if "cern" in match.lower():
                return urljoin(base_url, match)
        return urljoin(base_url, matches[0])

    return None


def extract_wikimedia_image_url(page_url: str) -> str | None:
    """Extract direct image URL from Wikimedia Commons page."""
    try:
        # Wikimedia Commons API to get image URL
        # Extract filename from page URL
        filename_match = re.search(r"/File:([^/]+)$", page_url)
        if not filename_match:
            return None

        filename = filename_match.group(1)
        # URL encode the filename
        from urllib.parse import quote

        quote(filename, safe="")

        # Use Wikimedia API to get image URL
        api_url = "https://commons.wikimedia.org/w/api.php"
        params = {
            "action": "query",
            "titles": f"File:{filename}",
            "prop": "imageinfo",
            "iiprop": "url",
            "format": "json",
        }

        response = requests.get(api_url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        pages = data.get("query", {}).get("pages", {})
        for _page_id, page_data in pages.items():
            imageinfo = page_data.get("imageinfo", [])
            if imageinfo:
                return imageinfo[0].get("url")

        return None
    except Exception as e:
        print(f"  ⚠️  Error extracting Wikimedia image: {e}")
        return None


def download_image(url: str, output_path: Path) -> bool:
    """Download image from URL."""
    try:
        response = requests.get(url, timeout=30, stream=True)
        response.raise_for_status()

        # Check if it's actually an image
        content_type = response.headers.get("content-type", "").lower()
        if not content_type.startswith("image/"):
            print(f"  ⚠️  URL does not return an image (content-type: {content_type})")
            return False

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"  ✅ Downloaded: {output_path.name}")
        return True
    except Exception as e:
        print(f"  ❌ Failed to download {url}: {e}")
        return False


def download_cern_image(url: str, output_path: Path) -> bool:
    """Download image from CERN archive URL (may be HTML page or direct image)."""
    try:
        # First, try to fetch the URL
        response = requests.get(url, timeout=30, allow_redirects=True)
        response.raise_for_status()

        # Check if it's a direct image
        content_type = response.headers.get("content-type", "").lower()
        if content_type.startswith("image/"):
            # Direct image URL
            return download_image(url, output_path)

        # It's HTML, try to extract image URL
        print("  📄 URL is HTML page, extracting image...")
        image_url = extract_image_from_cern_html(response.text, url)

        if image_url:
            print(f"  🔗 Found image URL: {image_url}")
            return download_image(image_url, output_path)
        else:
            print("  ⚠️  Could not find image in HTML page")
            return False

    except Exception as e:
        print(f"  ❌ Error processing CERN URL {url}: {e}")
        return False


def download_wikimedia_image(page_url: str, output_path: Path) -> bool:
    """Download image from Wikimedia Commons page."""
    image_url = extract_wikimedia_image_url(page_url)
    if image_url:
        return download_image(image_url, output_path)
    return False


def main():
    """Main function to download all photos."""
    print("Downloading LHC Team Photos from CERN Archives\n")
    print(f"Output directory: {OUTPUT_DIR}\n")

    results = {}

    for person_id, info in PHOTO_SOURCES.items():
        print(f"📸 {info['name']}:")
        output_path = OUTPUT_DIR / info["output"]

        # Skip if already downloaded
        if output_path.exists():
            print(f"  ⏭️  Already exists: {output_path.name}")
            results[person_id] = {
                "status": "exists",
                "path": str(output_path.relative_to(OUTPUT_DIR.parent)),
            }
            continue

        success = False
        for url in info["urls"]:
            if "wikimedia" in url.lower() or "commons.wikimedia" in url.lower():
                print(f"  🔍 Trying Wikimedia: {url}")
                success = download_wikimedia_image(url, output_path)
            else:
                print(f"  🔍 Trying CERN archive: {url}")
                success = download_cern_image(url, output_path)

            if success:
                results[person_id] = {
                    "status": "downloaded",
                    "path": str(output_path.relative_to(OUTPUT_DIR.parent)),
                }
                break

        if not success:
            print(f"  ❌ Failed to download photo for {info['name']}")
            results[person_id] = {"status": "failed", "path": None}

        print()

    # Print summary
    print("=" * 60)
    print("Download Summary:")
    print("=" * 60)
    for person_id, result in results.items():
        status_icon = "✅" if result["status"] in ["downloaded", "exists"] else "❌"
        print(f"{status_icon} {person_id}: {result['status']}")
        if result["path"]:
            print(f"   Path: {result['path']}")

    return results


if __name__ == "__main__":
    main()
