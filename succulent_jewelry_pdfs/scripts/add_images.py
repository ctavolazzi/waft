#!/usr/bin/env python3
"""
Add Images to Content
=====================

Utility script to add placeholder images from Picsum, Pexels, or Pixabay to markdown content.

Usage:
    python scripts/add_images.py \
        --content content/guides/my_guide.md \
        --provider pixabay \
        --query "succulent" \
        --width 800 \
        --height 600
"""

import argparse
import logging
import re
import sys
from pathlib import Path

# Add paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
succulent_pdfs_root = Path(__file__).parent.parent
sys.path.insert(0, str(succulent_pdfs_root))

from scripts.image_api import get_placeholder_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_image_placeholder(
    content: str, provider: str = "picsum", width: int = 800, height: int = 600, **kwargs
) -> str:
    """
    Add image placeholders to markdown content.

    Replaces `![placeholder]` with actual image URLs.

    Args:
        content: Markdown content
        provider: "picsum" or "pexels"
        width: Image width
        height: Image height
        **kwargs: Additional provider arguments

    Returns:
        Content with image URLs added
    """
    # Pattern to match ![placeholder] or ![placeholder:provider:width:height]
    # Handles: ![placeholder], ![placeholder:800:600], ![placeholder:pixabay:800:600]
    pattern = r"!\[placeholder(?::([^:\]]+))?(?::(\d+))?(?::(\d+))?\]"

    def replace_placeholder(match):
        # Extract groups: provider, width, height
        provider_override = match.group(1) or provider
        width_override = int(match.group(2)) if match.group(2) else width
        height_override = int(match.group(3)) if match.group(3) else height

        # Determine if first group is provider or width
        # If it's not a number and not empty, it's a provider
        if match.group(1) and not match.group(1).isdigit():
            provider_override = match.group(1)
            width_override = int(match.group(2)) if match.group(2) else width
            height_override = int(match.group(3)) if match.group(3) else height
        elif match.group(1) and match.group(1).isdigit():
            # First group is width, no provider specified
            provider_override = provider
            width_override = int(match.group(1))
            height_override = int(match.group(2)) if match.group(2) else height

        # Filter kwargs based on provider
        provider_kwargs = {}
        if provider_override in ["pexels", "pixabay"]:
            provider_kwargs = kwargs  # Pexels and Pixabay support query, size, etc.
        # Picsum doesn't support query, so we don't pass it

        image_url = get_placeholder_image(
            width=width_override,
            height=height_override,
            provider=provider_override,
            **provider_kwargs,
        )

        return f"![Image]({image_url})"

    return re.sub(pattern, replace_placeholder, content)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Add placeholder images to markdown content")
    parser.add_argument("--content", type=Path, required=True, help="Path to markdown content file")
    parser.add_argument(
        "--provider",
        choices=["picsum", "pexels", "pixabay"],
        default="picsum",
        help="Image provider (default: picsum)",
    )
    parser.add_argument(
        "--width", type=int, default=800, help="Image width in pixels (default: 800)"
    )
    parser.add_argument(
        "--height", type=int, default=600, help="Image height in pixels (default: 600)"
    )
    parser.add_argument(
        "--query", type=str, help='Search query for Pexels/Pixabay (e.g., "succulent", "jewelry")'
    )
    parser.add_argument(
        "--output", type=Path, default=None, help="Output file (default: overwrite input)"
    )
    parser.add_argument(
        "--pexels-api-key", type=str, help="Pexels API key (or set PEXELS_API_KEY env var)"
    )
    parser.add_argument(
        "--size",
        type=str,
        choices=["preview", "webformat", "large", "fullHD", "image"],
        default="large",
        help="Image size for Pixabay (default: large)",
    )

    args = parser.parse_args()

    # Read content
    if not args.content.exists():
        print(f"Error: Content file not found: {args.content}")
        sys.exit(1)

    content = args.content.read_text(encoding="utf-8")

    # Prepare kwargs for image API
    kwargs = {}
    if args.provider in ["pexels", "pixabay"]:
        if args.provider == "pexels" and args.pexels_api_key:
            kwargs["api_key"] = args.pexels_api_key
        if args.query:
            kwargs["query"] = args.query
        if args.provider == "pixabay":
            kwargs["size"] = args.size  # Use specified size (default: large)

    # Add images
    updated_content = add_image_placeholder(
        content, provider=args.provider, width=args.width, height=args.height, **kwargs
    )

    # Write output
    output_path = args.output or args.content
    output_path.write_text(updated_content, encoding="utf-8")

    print(f"✅ Updated content: {output_path}")
    print(f"   Provider: {args.provider}")
    print(f"   Size: {args.width}x{args.height}")


if __name__ == "__main__":
    main()
