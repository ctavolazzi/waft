#!/usr/bin/env python3
"""
Gumroad Preparation Script
==========================

Prepare PDFs for Gumroad upload by generating metadata, descriptions, and upload checklists.

Usage:
    python scripts/gumroad_prep.py --pdf-dir generated/guides/
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path (WAFT root)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Add succulent_jewelry_pdfs to path
succulent_pdfs_root = Path(__file__).parent.parent
sys.path.insert(0, str(succulent_pdfs_root))

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

SUCCULENT_PDFS_ROOT = Path(__file__).parent.parent


def load_gumroad_config() -> dict:
    """Load Gumroad metadata template."""
    config_path = SUCCULENT_PDFS_ROOT / "config" / "gumroad_metadata.json"
    if config_path.exists():
        try:
            with open(config_path) as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load Gumroad config: {e}")

    return {
        "title_template": "{title} - Succulent Jewelry Guide",
        "description_template": "A helpful guide about {topic}...",
        "tags": ["jewelry", "succulents", "how-to"],
        "pricing_tiers": {"basic": 5.00, "premium": 10.00},
    }


def extract_title_from_filename(pdf_path: Path) -> str:
    """Extract title from PDF filename."""
    name = pdf_path.stem
    # Convert snake_case or kebab-case to Title Case
    title = name.replace("_", " ").replace("-", " ")
    return title.title()


def generate_product_description(
    title: str, topic: str | None = None, config: dict | None = None
) -> str:
    """Generate product description from template."""
    if config is None:
        config = load_gumroad_config()

    template = config.get("description_template", "A helpful guide about {topic}.")

    description = template.format(
        title=title, topic=topic or "succulent jewelry", date=datetime.now().strftime("%Y-%m-%d")
    )

    return description


def generate_product_metadata(
    pdf_path: Path, title: str | None = None, topic: str | None = None
) -> dict:
    """Generate Gumroad product metadata for a PDF."""
    if title is None:
        title = extract_title_from_filename(pdf_path)

    config = load_gumroad_config()

    # Generate product title
    product_title = config.get("title_template", "{title}").format(title=title)

    # Generate description
    description = generate_product_description(title, topic, config)

    # Get file size
    file_size = pdf_path.stat().st_size if pdf_path.exists() else 0
    file_size_mb = file_size / (1024 * 1024)

    metadata = {
        "title": product_title,
        "description": description,
        "tags": config.get("tags", []),
        "file": str(pdf_path.name),
        "file_size_mb": round(file_size_mb, 2),
        "pricing": config.get("pricing_tiers", {}),
        "created": datetime.now().isoformat(),
    }

    if topic:
        metadata["topic"] = topic
        if topic not in metadata["tags"]:
            metadata["tags"].append(topic)

    return metadata


def prepare_gumroad_products(pdf_dir: Path, output_file: Path | None = None) -> dict:
    """
    Prepare all PDFs in directory for Gumroad upload.

    Args:
        pdf_dir: Directory containing PDFs
        output_file: Optional output file for products JSON

    Returns:
        Dictionary with all product metadata
    """
    if not pdf_dir.exists():
        raise FileNotFoundError(f"PDF directory not found: {pdf_dir}")

    pdf_files = list(pdf_dir.glob("*.pdf"))

    if not pdf_files:
        logger.warning(f"No PDF files found in {pdf_dir}")
        return {"products": [], "total": 0}

    products = []

    for pdf_path in sorted(pdf_files):
        logger.info(f"Processing: {pdf_path.name}")

        # Try to extract metadata from filename or use defaults
        title = extract_title_from_filename(pdf_path)
        topic = None  # Could be extracted from filename or metadata file

        metadata = generate_product_metadata(pdf_path, title, topic)
        products.append(metadata)

    result = {"products": products, "total": len(products), "generated": datetime.now().isoformat()}

    # Save to file
    if output_file is None:
        output_file = pdf_dir / "gumroad_products.json"

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)

    logger.info(f"Saved product metadata to: {output_file}")

    # Generate individual product description files
    descriptions_dir = pdf_dir / "gumroad_descriptions"
    descriptions_dir.mkdir(exist_ok=True)

    for product in products:
        desc_file = descriptions_dir / f"{Path(product['file']).stem}_description.txt"
        with open(desc_file, "w") as f:
            f.write(f"Title: {product['title']}\n\n")
            f.write(f"Description:\n{product['description']}\n\n")
            f.write(f"Tags: {', '.join(product['tags'])}\n")
            f.write(f"File: {product['file']}\n")
            f.write(f"Size: {product['file_size_mb']} MB\n")

    # Generate upload checklist
    checklist_file = pdf_dir / "gumroad_upload_checklist.md"
    with open(checklist_file, "w") as f:
        f.write("# Gumroad Upload Checklist\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total Products: {len(products)}\n\n")
        f.write("## Products to Upload\n\n")

        for i, product in enumerate(products, 1):
            f.write(f"### {i}. {product['title']}\n\n")
            f.write(f"- [ ] Upload file: `{product['file']}`\n")
            f.write(f"- [ ] Set title: `{product['title']}`\n")
            f.write("- [ ] Set description:\n")
            f.write("  ```\n")
            f.write(f"  {product['description']}\n")
            f.write("  ```\n")
            f.write(f"- [ ] Set tags: {', '.join(product['tags'])}\n")
            f.write(f"- [ ] Set price: ${product['pricing'].get('basic', 5.00):.2f}\n")
            f.write(f"- [ ] Verify file size: {product['file_size_mb']} MB\n")
            f.write("\n")

    logger.info(f"Generated upload checklist: {checklist_file}")

    return result


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Prepare PDFs for Gumroad upload")
    parser.add_argument(
        "--pdf-dir",
        type=Path,
        default=SUCCULENT_PDFS_ROOT / "generated" / "guides",
        help="Directory containing PDFs (default: generated/guides/)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output file for products JSON (default: pdf-dir/gumroad_products.json)",
    )

    args = parser.parse_args()

    try:
        result = prepare_gumroad_products(args.pdf_dir, args.output)

        print(f"\n{'=' * 60}")
        print("Gumroad Preparation Complete")
        print(f"{'=' * 60}")
        print(f"Products prepared: {result['total']}")
        print(f"Output file: {args.output or args.pdf_dir / 'gumroad_products.json'}")
        print(f"Checklist: {args.pdf_dir / 'gumroad_upload_checklist.md'}")
        print(f"{'=' * 60}\n")

        sys.exit(0)

    except Exception as e:
        logger.exception("Gumroad preparation failed")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
