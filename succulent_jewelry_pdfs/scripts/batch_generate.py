#!/usr/bin/env python3
"""
Batch Generate Guides
=====================

Generate multiple guide PDFs from a manifest file.

Usage:
    python scripts/batch_generate.py --manifest manifest.json
"""

import sys
import argparse
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional

# Add project root to path (WAFT root)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Add succulent_jewelry_pdfs to path
succulent_pdfs_root = Path(__file__).parent.parent
sys.path.insert(0, str(succulent_pdfs_root))

from scripts.generate_guide import generate_pdf_safe, load_config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

SUCCULENT_PDFS_ROOT = Path(__file__).parent.parent


def load_manifest(manifest_path: Path) -> List[Dict]:
    """
    Load manifest file (JSON or CSV).

    Args:
        manifest_path: Path to manifest file

    Returns:
        List of guide metadata dictionaries
    """
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest file not found: {manifest_path}")

    if manifest_path.suffix == '.json':
        with open(manifest_path, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'guides' in data:
                return data['guides']
            else:
                raise ValueError("Manifest JSON must be a list or object with 'guides' key")
    else:
        # CSV support could be added here
        raise ValueError(f"Unsupported manifest format: {manifest_path.suffix}")


def batch_generate(manifest_path: Path, output_dir: Optional[Path] = None) -> Dict:
    """
    Generate multiple PDFs from manifest.

    Args:
        manifest_path: Path to manifest file
        output_dir: Output directory (default: generated/guides/)

    Returns:
        Dictionary with results:
        {
            'total': int,
            'success': int,
            'failed': int,
            'results': list
        }
    """
    if output_dir is None:
        output_dir = SUCCULENT_PDFS_ROOT / 'generated' / 'guides'

    output_dir.mkdir(parents=True, exist_ok=True)

    # Load manifest
    logger.info(f"Loading manifest: {manifest_path}")
    guides = load_manifest(manifest_path)

    # Load config
    config = load_config()

    # Process each guide
    results = {
        'total': len(guides),
        'success': 0,
        'failed': 0,
        'results': []
    }

    for i, guide_data in enumerate(guides, 1):
        logger.info(f"Processing guide {i}/{len(guides)}: {guide_data.get('title', 'Unknown')}")

        try:
            # Extract guide data
            content_path = Path(guide_data['content'])
            title = guide_data['title']
            topic = guide_data.get('topic')
            subtitle = guide_data.get('subtitle')
            author = guide_data.get('author')

            # Generate output filename
            safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in title)
            safe_title = safe_title.replace(' ', '_').lower()
            output_path = output_dir / f"{safe_title}.pdf"

            # Generate PDF
            success = generate_pdf_safe(
                content_path=content_path,
                output_path=output_path,
                title=title,
                topic=topic,
                subtitle=subtitle,
                author=author,
                config=config
            )

            if success:
                results['success'] += 1
                results['results'].append({
                    'title': title,
                    'status': 'success',
                    'output': str(output_path)
                })
            else:
                results['failed'] += 1
                results['results'].append({
                    'title': title,
                    'status': 'failed',
                    'error': 'Generation failed'
                })

        except Exception as e:
            logger.exception(f"Failed to process guide: {guide_data.get('title', 'Unknown')}")
            results['failed'] += 1
            results['results'].append({
                'title': guide_data.get('title', 'Unknown'),
                'status': 'error',
                'error': str(e)
            })

    return results


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Batch generate guide PDFs from manifest file'
    )
    parser.add_argument(
        '--manifest',
        type=Path,
        required=True,
        help='Path to manifest file (JSON)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=None,
        help='Output directory (default: generated/guides/)'
    )

    args = parser.parse_args()

    try:
        results = batch_generate(args.manifest, args.output)

        # Print summary
        print(f"\n{'='*60}")
        print(f"Batch Generation Summary")
        print(f"{'='*60}")
        print(f"Total:   {results['total']}")
        print(f"Success: {results['success']}")
        print(f"Failed:  {results['failed']}")
        print(f"{'='*60}\n")

        # Print failed guides
        if results['failed'] > 0:
            print("Failed guides:")
            for result in results['results']:
                if result['status'] != 'success':
                    print(f"  - {result['title']}: {result.get('error', 'Unknown error')}")

        sys.exit(0 if results['failed'] == 0 else 1)

    except Exception as e:
        logger.exception("Batch generation failed")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
