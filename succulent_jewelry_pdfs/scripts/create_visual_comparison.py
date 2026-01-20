#!/usr/bin/env python3
"""
Visual Comparison Generator
===========================

Create a visual PDF comparing Pixabay and Pexels results side-by-side.
"""

import re
import sys
from pathlib import Path

# Add paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
succulent_pdfs_root = Path(__file__).parent.parent
sys.path.insert(0, str(succulent_pdfs_root))

from markdown import markdown
from templates.guide_template import generate_guide

from scripts.image_api import PexelsAPI, PixabayAPI


def create_comparison_guide():
    """Create a visual comparison guide."""

    # Test queries
    queries = ["succulent", "jewelry", "nature", "garden"]

    content = """# Pixabay vs Pexels: Visual Comparison

This guide visually compares image results from Pixabay and Pexels APIs across different queries.

"""

    pixabay = PixabayAPI()

    for query in queries:
        content += f'## Query: "{query}"\n\n'

        # Pixabay results
        content += "### Pixabay Results\n\n"
        try:
            result = pixabay.search_images(query, per_page=3, min_width=800, min_height=600)
            if result and result.get("hits"):
                content += f"**Total Available:** {result.get('totalHits', 0):,} images\n\n"

                for i, hit in enumerate(result["hits"][:3], 1):
                    large_url = hit.get("largeImageURL", "")
                    if large_url:
                        content += f"![Pixabay {query} {i}]({large_url})\n\n"
                        content += f'<div class="image-caption">Pixabay Image {i}: {hit.get("tags", "")[:60]}</div>\n\n'
        except Exception as e:
            content += f"*Error: {e}*\n\n"

        # Pexels results (will show placeholder if no API key)
        content += "### Pexels Results\n\n"
        try:
            pexels = PexelsAPI()
            result = pexels.search_photos(query, per_page=3)
            if result and result.get("photos"):
                content += f"**Total Available:** {result.get('total_results', 0):,} photos\n\n"

                for i, photo in enumerate(result["photos"][:3], 1):
                    src = photo.get("src", {})
                    large_url = src.get("large", "")
                    if large_url:
                        content += f"![Pexels {query} {i}]({large_url})\n\n"
                        photographer = photo.get("photographer", "Unknown")
                        photographer_url = photo.get("photographer_url", "#")
                        content += f'<div class="image-caption">Pexels Image {i}: Photo by <a href="{photographer_url}">{photographer}</a> on Pexels</div>\n\n'
            else:
                content += "*Pexels API key required. Add PEXELS_API_KEY to .env file.*\n\n"
        except Exception as e:
            content += f"*Pexels unavailable: {e}*\n\n"

        content += "---\n\n"

    # Convert to HTML
    html_content = markdown(content, extensions=["extra", "codehilite"])

    # Fix bold in step divs
    def fix_step_bold(html):
        def process_step(match):
            step_html = match.group(1)
            step_html = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", step_html)
            return f'<div class="step">\n{step_html}\n</div>'

        pattern = r'<div class="step">\n(.*?)\n</div>'
        return re.sub(pattern, process_step, html, flags=re.DOTALL)

    html_content = fix_step_bold(html_content)

    # Generate PDF
    from pathlib import Path as PathLib

    script_dir = PathLib(__file__).parent
    output_dir = script_dir.parent / "generated" / "experiments"
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = output_dir / "visual_api_comparison.pdf"
    generate_guide(
        title="Pixabay vs Pexels: Visual Comparison",
        content=html_content,
        output_path=pdf_path,
        series="EXPERIMENT",
        number="EXP-002",
        subtitle="Side-by-Side Image Comparison",
        author="Succulent Jewelry",
        include_gumroad_link=False,
    )

    print(f"✅ Visual comparison PDF generated: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    print("🎨 Creating visual comparison PDF...\n")
    pdf_path = create_comparison_guide()
    print(f"\n✅ Complete! Open: {pdf_path}")
