#!/usr/bin/env python3
"""
Image API Format Experiments
============================

Test different image formats, sizes, and orientations from both APIs.
Generates comparison visualizations.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
succulent_pdfs_root = Path(__file__).parent.parent
sys.path.insert(0, str(succulent_pdfs_root))

from scripts.image_api import PexelsAPI, PixabayAPI


def test_image_sizes(api_name: str, query: str = "succulent") -> dict:
    """Test different image sizes from an API."""
    results = {"api": api_name, "query": query, "sizes": {}}

    if api_name == "pixabay":
        api = PixabayAPI()
        result = api.search_images(query, per_page=1, min_width=800, min_height=600)

        if result and result.get("hits"):
            hit = result["hits"][0]
            results["sizes"] = {
                "preview": {
                    "url": hit.get("previewURL", ""),
                    "dimensions": f"{hit.get('previewWidth', 0)}x{hit.get('previewHeight', 0)}",
                },
                "webformat": {
                    "url": hit.get("webformatURL", ""),
                    "dimensions": f"{hit.get('webformatWidth', 0)}x{hit.get('webformatHeight', 0)}",
                },
                "large": {"url": hit.get("largeImageURL", ""), "dimensions": "1280px max"},
                "fullHD": {"url": hit.get("fullHDURL", ""), "dimensions": "1920px max"},
                "original": {
                    "url": hit.get("imageURL", ""),
                    "dimensions": f"{hit.get('imageWidth', 0)}x{hit.get('imageHeight', 0)}",
                },
            }

    elif api_name == "pexels":
        api = PexelsAPI()
        result = api.search_photos(query, per_page=1)

        if result and result.get("photos"):
            photo = result["photos"][0]
            src = photo.get("src", {})
            results["sizes"] = {
                "tiny": {"url": src.get("tiny", ""), "dimensions": "200x280"},
                "small": {"url": src.get("small", ""), "dimensions": "130px height"},
                "medium": {"url": src.get("medium", ""), "dimensions": "350px height"},
                "large": {"url": src.get("large", ""), "dimensions": "650px height"},
                "large2x": {"url": src.get("large2x", ""), "dimensions": "1300px height"},
                "original": {
                    "url": src.get("original", ""),
                    "dimensions": f"{photo.get('width', 0)}x{photo.get('height', 0)}",
                },
                "portrait": {"url": src.get("portrait", ""), "dimensions": "1200x800"},
                "landscape": {"url": src.get("landscape", ""), "dimensions": "1200x627"},
            }

    return results


def test_orientations(api_name: str, query: str = "succulent") -> dict:
    """Test different orientations."""
    results = {"api": api_name, "query": query, "orientations": {}}

    if api_name == "pixabay":
        api = PixabayAPI()
        for orientation in ["all", "horizontal", "vertical"]:
            result = api.search_images(query, per_page=1, orientation=orientation)
            if result and result.get("hits"):
                hit = result["hits"][0]
                results["orientations"][orientation] = {
                    "url": hit.get("largeImageURL", ""),
                    "dimensions": f"{hit.get('imageWidth', 0)}x{hit.get('imageHeight', 0)}",
                    "is_horizontal": hit.get("imageWidth", 0) > hit.get("imageHeight", 0),
                }

    elif api_name == "pexels":
        api = PexelsAPI()
        for orientation in ["landscape", "portrait", "square"]:
            result = api.search_photos(query, per_page=1, orientation=orientation)
            if result and result.get("photos"):
                photo = result["photos"][0]
                src = photo.get("src", {})
                results["orientations"][orientation] = {
                    "url": src.get("large", ""),
                    "dimensions": f"{photo.get('width', 0)}x{photo.get('height', 0)}",
                    "is_horizontal": photo.get("width", 0) > photo.get("height", 0),
                }

    return results


def test_categories(api_name: str) -> dict:
    """Test category filtering (Pixabay only)."""
    results = {"api": api_name, "categories": {}}

    if api_name == "pixabay":
        api = PixabayAPI()
        categories = ["nature", "animals", "backgrounds", "fashion", "food"]

        for category in categories:
            result = api.search_images("plant", per_page=1, category=category)
            if result and result.get("hits"):
                hit = result["hits"][0]
                results["categories"][category] = {
                    "total": result.get("totalHits", 0),
                    "sample_url": hit.get("largeImageURL", ""),
                    "tags": hit.get("tags", "")[:50],
                }

    return results


def test_colors(api_name: str) -> dict:
    """Test color filtering (Pexels only)."""
    results = {"api": api_name, "colors": {}}

    if api_name == "pexels":
        api = PexelsAPI()
        colors = ["green", "blue", "red", "yellow", "brown"]

        for color in colors:
            result = api.search_photos("nature", per_page=1, color=color)
            if result and result.get("photos"):
                photo = result["photos"][0]
                src = photo.get("src", {})
                results["colors"][color] = {
                    "total": result.get("total_results", 0),
                    "sample_url": src.get("large", ""),
                    "avg_color": photo.get("avg_color", ""),
                    "photographer": photo.get("photographer", ""),
                }

    return results


def generate_format_comparison_report(experiments: dict, output_path: Path):
    """Generate markdown report comparing formats."""

    report = f"""# Image API Format Comparison

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Overview

This report compares image formats, sizes, and features available from Pixabay and Pexels APIs.

"""

    # Size comparison
    if "sizes" in experiments:
        report += "## Image Size Options\n\n"

        for api_name, size_data in experiments["sizes"].items():
            report += f"### {api_name.upper()}\n\n"
            report += f'**Query:** "{size_data.get("query", "N/A")}"\n\n'

            sizes = size_data.get("sizes", {})
            report += "| Size | Dimensions | URL Preview |\n"
            report += "|------|------------|-------------|\n"

            for size_name, size_info in sizes.items():
                url = size_info.get("url", "")
                dims = size_info.get("dimensions", "N/A")
                url_preview = url[:60] + "..." if len(url) > 60 else url
                report += f"| {size_name} | {dims} | `{url_preview}` |\n"

            report += "\n"

    # Orientation comparison
    if "orientations" in experiments:
        report += "## Orientation Options\n\n"

        for api_name, orient_data in experiments["orientations"].items():
            report += f"### {api_name.upper()}\n\n"
            report += f'**Query:** "{orient_data.get("query", "N/A")}"\n\n'

            orientations = orient_data.get("orientations", {})
            for orient_name, orient_info in orientations.items():
                report += f"#### {orient_name}\n\n"
                report += f"- **Dimensions:** {orient_info.get('dimensions', 'N/A')}\n"
                report += f"- **Is Horizontal:** {orient_info.get('is_horizontal', False)}\n"
                if orient_info.get("url"):
                    report += f"![{orient_name}]({orient_info['url']})\n\n"

    # Category/Color filters
    if "categories" in experiments:
        report += "## Category Filtering (Pixabay)\n\n"
        for api_name, cat_data in experiments["categories"].items():
            if cat_data.get("categories"):
                report += f"### {api_name.upper()}\n\n"
                report += "| Category | Total Results | Sample Tags |\n"
                report += "|----------|---------------|-------------|\n"
                for cat_name, cat_info in cat_data["categories"].items():
                    report += f"| {cat_name} | {cat_info.get('total', 0):,} | {cat_info.get('tags', 'N/A')[:40]} |\n"
                report += "\n"

    if "colors" in experiments:
        report += "## Color Filtering (Pexels)\n\n"
        for api_name, color_data in experiments["colors"].items():
            if color_data.get("colors"):
                report += f"### {api_name.upper()}\n\n"
                report += "| Color | Total Results | Avg Color | Photographer |\n"
                report += "|-------|---------------|-----------|--------------|\n"
                for color_name, color_info in color_data["colors"].items():
                    report += f"| {color_name} | {color_info.get('total', 0):,} | {color_info.get('avg_color', 'N/A')} | {color_info.get('photographer', 'N/A')} |\n"
                report += "\n"

    output_path.write_text(report, encoding="utf-8")
    print(f"✅ Format comparison report saved: {output_path}")


def main():
    """Run format experiments."""

    print("🔬 Image API Format Experiments\n")

    experiments = {}

    # Test 1: Image Sizes
    print("1. Testing image sizes...")
    experiments["sizes"] = {}

    print("   Pixabay sizes...")
    pixabay_sizes = test_image_sizes("pixabay", "succulent")
    experiments["sizes"]["pixabay"] = pixabay_sizes

    print("   Pexels sizes...")
    try:
        pexels_sizes = test_image_sizes("pexels", "succulent")
        experiments["sizes"]["pexels"] = pexels_sizes
    except Exception as e:
        print(f"   ⚠️  Pexels failed: {e}")
        experiments["sizes"]["pexels"] = {"error": str(e)}

    # Test 2: Orientations
    print("\n2. Testing orientations...")
    experiments["orientations"] = {}

    print("   Pixabay orientations...")
    pixabay_orient = test_orientations("pixabay", "succulent")
    experiments["orientations"]["pixabay"] = pixabay_orient

    print("   Pexels orientations...")
    try:
        pexels_orient = test_orientations("pexels", "succulent")
        experiments["orientations"]["pexels"] = pexels_orient
    except Exception as e:
        print(f"   ⚠️  Pexels failed: {e}")
        experiments["orientations"]["pexels"] = {"error": str(e)}

    # Test 3: Categories (Pixabay)
    print("\n3. Testing categories (Pixabay)...")
    pixabay_cats = test_categories("pixabay")
    experiments["categories"] = {"pixabay": pixabay_cats}

    # Test 4: Colors (Pexels)
    print("\n4. Testing color filters (Pexels)...")
    try:
        pexels_colors = test_colors("pexels")
        experiments["colors"] = {"pexels": pexels_colors}
    except Exception as e:
        print(f"   ⚠️  Pexels failed: {e}")
        experiments["colors"] = {"pexels": {"error": str(e)}}

    # Save results
    from pathlib import Path as PathLib

    script_dir = PathLib(__file__).parent
    output_dir = script_dir.parent / "generated" / "experiments"
    output_dir.mkdir(parents=True, exist_ok=True)

    # JSON data
    json_path = output_dir / "format_experiments.json"
    json_path.write_text(json.dumps(experiments, indent=2), encoding="utf-8")
    print(f"\n✅ JSON data saved: {json_path}")

    # Markdown report
    report_path = output_dir / "format_comparison_report.md"
    generate_format_comparison_report(experiments, report_path)

    print(f"\n✅ Experiments complete! Check {output_dir} for results.")


if __name__ == "__main__":
    main()
