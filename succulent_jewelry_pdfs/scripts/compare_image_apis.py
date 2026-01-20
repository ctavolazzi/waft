#!/usr/bin/env python3
"""
Image API Comparison Tool
=========================

Compare Pixabay and Pexels APIs with various queries and formats.
Generates comparison reports and test images.
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


def test_query(query: str, width: int = 800, height: int = 600, size: str = "large") -> dict:
    """
    Test a query on both APIs and return comparison data.

    Args:
        query: Search query
        width: Image width
        height: Image height
        size: Image size (for Pixabay)

    Returns:
        Comparison dictionary
    """
    results = {
        "query": query,
        "width": width,
        "height": height,
        "timestamp": datetime.now().isoformat(),
        "pixabay": {},
        "pexels": {},
    }

    # Test Pixabay
    print(f"  Testing Pixabay: '{query}'...")
    try:
        pixabay = PixabayAPI()
        pixabay_result = pixabay.search_images(
            query, per_page=3, min_width=width, min_height=height
        )

        if pixabay_result and pixabay_result.get("hits"):
            hits = pixabay_result["hits"]
            results["pixabay"] = {
                "status": "success",
                "total_hits": pixabay_result.get("totalHits", 0),
                "returned": len(hits),
                "images": [],
            }

            for i, hit in enumerate(hits[:3], 1):
                image_data = {
                    "id": hit.get("id"),
                    "tags": hit.get("tags", ""),
                    "urls": {
                        "preview": hit.get("previewURL", ""),
                        "webformat": hit.get("webformatURL", ""),
                        "large": hit.get("largeImageURL", ""),
                        "fullHD": hit.get("fullHDURL", ""),
                        "original": hit.get("imageURL", ""),
                    },
                    "dimensions": {
                        "width": hit.get("imageWidth", 0),
                        "height": hit.get("imageHeight", 0),
                    },
                    "views": hit.get("views", 0),
                    "downloads": hit.get("downloads", 0),
                }
                results["pixabay"]["images"].append(image_data)
        else:
            results["pixabay"] = {"status": "no_results", "error": "No images found"}
    except Exception as e:
        results["pixabay"] = {"status": "error", "error": str(e)}
        print(f"    ❌ Pixabay error: {e}")

    # Test Pexels
    print(f"  Testing Pexels: '{query}'...")
    try:
        pexels = PexelsAPI()
        pexels_result = pexels.search_photos(query, per_page=3)

        if pexels_result and pexels_result.get("photos"):
            photos = pexels_result["photos"]
            results["pexels"] = {
                "status": "success",
                "total_results": pexels_result.get("total_results", 0),
                "returned": len(photos),
                "images": [],
            }

            for i, photo in enumerate(photos[:3], 1):
                src = photo.get("src", {})
                image_data = {
                    "id": photo.get("id"),
                    "photographer": photo.get("photographer", ""),
                    "photographer_url": photo.get("photographer_url", ""),
                    "urls": {
                        "original": src.get("original", ""),
                        "large2x": src.get("large2x", ""),
                        "large": src.get("large", ""),
                        "medium": src.get("medium", ""),
                        "small": src.get("small", ""),
                        "portrait": src.get("portrait", ""),
                        "landscape": src.get("landscape", ""),
                        "tiny": src.get("tiny", ""),
                    },
                    "dimensions": {
                        "width": photo.get("width", 0),
                        "height": photo.get("height", 0),
                    },
                    "avg_color": photo.get("avg_color", ""),
                    "alt": photo.get("alt", ""),
                }
                results["pexels"]["images"].append(image_data)
        else:
            results["pexels"] = {"status": "no_results", "error": "No photos found"}
    except Exception as e:
        results["pexels"] = {"status": "error", "error": str(e)}
        print(f"    ❌ Pexels error: {e}")

    return results


def generate_comparison_report(results: list[dict], output_path: Path):
    """Generate a markdown comparison report."""

    report = f"""# Image API Comparison Report

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary

Tested {len(results)} queries across Pixabay and Pexels APIs.

"""

    for result in results:
        query = result["query"]
        report += f'## Query: "{query}"\n\n'
        report += f"**Dimensions:** {result['width']}x{result['height']}\n\n"

        # Pixabay results
        report += "### Pixabay\n\n"
        pixabay = result.get("pixabay", {})
        if pixabay.get("status") == "success":
            report += "- **Status:** ✅ Success\n"
            report += f"- **Total Available:** {pixabay.get('total_hits', 0):,}\n"
            report += f"- **Returned:** {pixabay.get('returned', 0)}\n\n"

            for i, img in enumerate(pixabay.get("images", [])[:3], 1):
                report += f"#### Image {i}\n\n"
                report += f"- **ID:** {img.get('id')}\n"
                report += f"- **Tags:** {img.get('tags', 'N/A')}\n"
                report += f"- **Dimensions:** {img.get('dimensions', {}).get('width', 0)}x{img.get('dimensions', {}).get('height', 0)}\n"
                report += f"- **Views:** {img.get('views', 0):,}\n"
                report += f"- **Downloads:** {img.get('downloads', 0):,}\n\n"

                urls = img.get("urls", {})
                if urls.get("large"):
                    report += f"![Pixabay {i}]({urls['large']})\n\n"
                report += "**URLs:**\n"
                report += f"- Large: {urls.get('large', 'N/A')[:80]}...\n"
                report += f"- Full HD: {urls.get('fullHD', 'N/A')[:80]}...\n\n"
        else:
            report += f"- **Status:** ❌ {pixabay.get('status', 'unknown')}\n"
            report += f"- **Error:** {pixabay.get('error', 'Unknown error')}\n\n"

        # Pexels results
        report += "### Pexels\n\n"
        pexels = result.get("pexels", {})
        if pexels.get("status") == "success":
            report += "- **Status:** ✅ Success\n"
            report += f"- **Total Available:** {pexels.get('total_results', 0):,}\n"
            report += f"- **Returned:** {pexels.get('returned', 0)}\n\n"

            for i, img in enumerate(pexels.get("images", [])[:3], 1):
                report += f"#### Image {i}\n\n"
                report += f"- **ID:** {img.get('id')}\n"
                report += f"- **Photographer:** [{img.get('photographer', 'N/A')}]({img.get('photographer_url', '#')})\n"
                report += f"- **Dimensions:** {img.get('dimensions', {}).get('width', 0)}x{img.get('dimensions', {}).get('height', 0)}\n"
                report += f"- **Alt Text:** {img.get('alt', 'N/A')}\n"
                report += f"- **Avg Color:** {img.get('avg_color', 'N/A')}\n\n"

                urls = img.get("urls", {})
                if urls.get("large"):
                    report += f"![Pexels {i}]({urls['large']})\n\n"
                report += "**URLs:**\n"
                report += f"- Large: {urls.get('large', 'N/A')[:80]}...\n"
                report += f"- Large 2x: {urls.get('large2x', 'N/A')[:80]}...\n"
                report += f"- Original: {urls.get('original', 'N/A')[:80]}...\n\n"
        else:
            report += f"- **Status:** ❌ {pexels.get('status', 'unknown')}\n"
            report += f"- **Error:** {pexels.get('error', 'Unknown error')}\n\n"

        report += "---\n\n"

    output_path.write_text(report, encoding="utf-8")
    print(f"✅ Report saved: {output_path}")


def generate_test_guide(results: list[dict], output_path: Path):
    """Generate a test PDF guide comparing APIs."""

    content = f"""# Image API Comparison Guide

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

This guide compares image results from Pixabay and Pexels APIs across various queries.

"""

    for result in results:
        query = result["query"]
        content += f'## Query: "{query}"\n\n'

        # Pixabay section
        pixabay = result.get("pixabay", {})
        if pixabay.get("status") == "success" and pixabay.get("images"):
            content += "### Pixabay Results\n\n"
            content += f"**Total Available:** {pixabay.get('total_hits', 0):,} images\n\n"

            for i, img in enumerate(pixabay.get("images", [])[:2], 1):
                urls = img.get("urls", {})
                if urls.get("large"):
                    content += f"![Pixabay {query} {i}]({urls['large']})\n\n"
                    content += f'<div class="image-caption">Pixabay Image {i}: {img.get("tags", "")[:50]}</div>\n\n'

        # Pexels section
        pexels = result.get("pexels", {})
        if pexels.get("status") == "success" and pexels.get("images"):
            content += "### Pexels Results\n\n"
            content += f"**Total Available:** {pexels.get('total_results', 0):,} photos\n\n"

            for i, img in enumerate(pexels.get("images", [])[:2], 1):
                urls = img.get("urls", {})
                if urls.get("large"):
                    content += f"![Pexels {query} {i}]({urls['large']})\n\n"
                    content += f'<div class="image-caption">Pexels Image {i}: Photo by {img.get("photographer", "Unknown")}</div>\n\n'

        content += "---\n\n"

    output_path.write_text(content, encoding="utf-8")
    print(f"✅ Test guide content saved: {output_path}")


def main():
    """Main comparison function."""

    # Test queries relevant to succulent jewelry
    test_queries = [
        "succulent",
        "jewelry",
        "plant care",
        "handmade jewelry",
        "cactus",
        "nature",
        "garden",
        "botanical",
        "echeveria",
        "casting",
    ]

    print("🔬 Image API Comparison Experiment\n")
    print(f"Testing {len(test_queries)} queries on both APIs...\n")

    results = []

    for query in test_queries:
        print(f"Testing: '{query}'")
        result = test_query(query, width=800, height=600, size="large")
        results.append(result)

        # Print quick summary
        pixabay_status = result["pixabay"].get("status", "unknown")
        pexels_status = result["pexels"].get("status", "unknown")
        print(f"  Pixabay: {pixabay_status}, Pexels: {pexels_status}\n")

    # Generate outputs
    script_dir = Path(__file__).parent
    output_dir = script_dir.parent / "generated" / "experiments"
    output_dir.mkdir(parents=True, exist_ok=True)

    # JSON data
    json_path = output_dir / "api_comparison_data.json"
    json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"✅ JSON data saved: {json_path}")

    # Markdown report
    report_path = output_dir / "api_comparison_report.md"
    generate_comparison_report(results, report_path)

    # Test guide content
    guide_path = output_dir / "api_comparison_guide.md"
    generate_test_guide(results, guide_path)

    # Generate PDF from guide
    print("\n📄 Generating PDF comparison guide...")
    try:
        import sys

        sys.path.insert(0, str(script_dir.parent.parent))

        import re

        from markdown import markdown
        from templates.guide_template import generate_guide

        md_content = guide_path.read_text()
        html_content = markdown(md_content, extensions=["extra", "codehilite"])

        # Fix bold in step divs
        def fix_step_bold(html):
            def process_step(match):
                step_html = match.group(1)
                step_html = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", step_html)
                return f'<div class="step">\n{step_html}\n</div>'

            pattern = r'<div class="step">\n(.*?)\n</div>'
            return re.sub(pattern, process_step, html, flags=re.DOTALL)

        html_content = fix_step_bold(html_content)

        pdf_path = output_dir / "api_comparison_guide.pdf"
        generate_guide(
            title="Image API Comparison Guide",
            content=html_content,
            output_path=pdf_path,
            series="EXPERIMENT",
            number="EXP-001",
            subtitle="Pixabay vs Pexels",
            author="Succulent Jewelry",
            include_gumroad_link=False,
        )
        print(f"✅ PDF guide generated: {pdf_path}")
    except Exception as e:
        print(f"⚠️  Could not generate PDF: {e}")

    # Summary statistics
    print("\n📊 Summary Statistics:\n")

    pixabay_success = sum(1 for r in results if r["pixabay"].get("status") == "success")
    pexels_success = sum(1 for r in results if r["pexels"].get("status") == "success")

    total_pixabay = sum(
        r["pixabay"].get("total_hits", 0)
        for r in results
        if r["pixabay"].get("status") == "success"
    )
    total_pexels = sum(
        r["pexels"].get("total_results", 0)
        for r in results
        if r["pexels"].get("status") == "success"
    )

    print("Pixabay:")
    print(f"  Successful queries: {pixabay_success}/{len(results)}")
    print(f"  Total images available: {total_pixabay:,}")

    print("\nPexels:")
    print(f"  Successful queries: {pexels_success}/{len(results)}")
    print(f"  Total photos available: {total_pexels:,}")

    print(f"\n✅ Experiment complete! Check {output_dir} for results.")


if __name__ == "__main__":
    main()
