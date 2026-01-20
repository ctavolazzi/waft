#!/usr/bin/env python3
"""
Generate Guide PDF
==================

Generate a single guide PDF from markdown/HTML content with full security,
error handling, and validation.

Usage:
    python scripts/generate_guide.py \
        --content content/guides/jewelry_casting_basics.md \
        --title "Vacuum Casting Basics" \
        --topic "jewelry" \
        --output generated/guides/
"""

import sys
import argparse
import json
import logging
from pathlib import Path
from typing import Optional

# Add project root to path (WAFT root)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Add succulent_jewelry_pdfs to path
succulent_pdfs_root = Path(__file__).parent.parent
sys.path.insert(0, str(succulent_pdfs_root))

# Import WAFT PDF system
try:
    from src.waft import PDF
except ImportError:
    print("Error: WAFT PDF system not found. Make sure you're running from the project root.")
    sys.exit(1)

# Import local modules
from templates.guide_template import generate_guide
from scripts.security import validate_path, sanitize_content, validate_metadata
from scripts.validation import validate_pdf_quality
from scripts.resource_manager import create_temp_dir

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Project root for this system
SUCCULENT_PDFS_ROOT = Path(__file__).parent.parent


def load_config() -> dict:
    """Load configuration from config file."""
    config_path = SUCCULENT_PDFS_ROOT / 'config' / 'guide_config.json'
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load config: {e}")
    return {
        'series': 'SUCCULENT JEWELRY GUIDE',
        'default_style': 'field_guide',
        'printer_friendly': False,
        'include_gumroad_link': True,
        'author': 'Your Name',
        'default_topics': ['jewelry', 'succulents', 'music', 'casting'],
        'max_content_size_mb': 10,
        'project_root': str(SUCCULENT_PDFS_ROOT)
    }


def generate_pdf_safe(
    content_path: Path,
    output_path: Path,
    title: str,
    topic: Optional[str] = None,
    subtitle: Optional[str] = None,
    author: Optional[str] = None,
    config: Optional[dict] = None
) -> bool:
    """
    Generate PDF with comprehensive error handling and security.

    Args:
        content_path: Path to content file
        output_path: Path to output PDF
        title: Document title
        topic: Topic (optional)
        subtitle: Optional subtitle
        author: Optional author
        config: Configuration dictionary

    Returns:
        True if successful, False otherwise
    """
    if config is None:
        config = load_config()

    project_root = Path(config.get('project_root', SUCCULENT_PDFS_ROOT))
    max_size = config.get('max_content_size_mb', 10) * 1024 * 1024
    allowed_topics = config.get('default_topics', [])

    try:
        # Validate paths (CRITICAL security)
        logger.info(f"Validating paths...")
        validated_content_path = validate_path(content_path, project_root)
        validated_output_path = validate_path(output_path.parent, project_root)
        output_path = validated_output_path / output_path.name

        # Validate metadata
        logger.info(f"Validating metadata...")
        metadata = validate_metadata(title, topic, allowed_topics)
        title = metadata['title']

        # Read content
        logger.info(f"Reading content from {validated_content_path}...")
        if not validated_content_path.exists():
            logger.error(f"Content file not found: {validated_content_path}")
            print(f"Error: Content file not found: {validated_content_path}")
            return False

        content = validated_content_path.read_text(encoding='utf-8')

        # Sanitize content (CRITICAL security)
        logger.info("Sanitizing content...")
        sanitized = sanitize_content(content, max_size=max_size)

        # Post-process: Fix markdown bold syntax in step divs (markdown doesn't process inside HTML)
        import re
        def fix_step_bold(html):
            def process_step(match):
                step_html = match.group(1)
                # Replace **text** with <strong>text</strong>
                step_html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', step_html)
                return f'<div class="step">\n{step_html}\n</div>'
            pattern = r'<div class="step">\n(.*?)\n</div>'
            return re.sub(pattern, process_step, html, flags=re.DOTALL)
        
        sanitized = fix_step_bold(sanitized)

        # Generate PDF
        logger.info("Generating PDF...")
        generate_guide(
            title=title,
            content=sanitized,
            output_path=output_path,
            series=config.get('series', 'SUCCULENT JEWELRY GUIDE'),
            number=config.get('number', 'GUIDE-001'),
            subtitle=subtitle,
            author=author or config.get('author'),
            include_gumroad_link=config.get('include_gumroad_link', True)
        )

        # Validate output quality
        logger.info("Validating PDF quality...")
        validation = validate_pdf_quality(output_path)
        if not validation['valid']:
            logger.warning(f"PDF validation issues: {validation['errors']}")
            print(f"Warning: PDF validation issues: {', '.join(validation['errors'])}")
        else:
            logger.info(f"PDF validated successfully: {validation['page_count']} pages, "
                       f"checksum: {validation['checksum'][:16]}...")

        logger.info(f"PDF generated successfully: {output_path}")
        print(f"✅ PDF generated: {output_path}")
        return True

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"Error: File not found - {e}")
        return False

    except PermissionError as e:
        logger.error(f"Permission denied: {e}")
        print(f"Error: Permission denied - check file permissions")
        return False

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        print(f"Error: {e}")
        return False

    except Exception as e:
        logger.exception(f"PDF generation failed: {e}")
        print(f"Error: PDF generation failed - {e}")
        # Fallback: save markdown
        try:
            fallback_path = output_path.with_suffix('.md')
            fallback_path.write_text(content)
            logger.info(f"Saved fallback markdown: {fallback_path}")
            print(f"Note: Saved markdown fallback: {fallback_path}")
        except Exception:
            pass
        return False


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Generate a guide PDF from markdown/HTML content'
    )
    parser.add_argument(
        '--content',
        type=Path,
        required=True,
        help='Path to content file (markdown or HTML)'
    )
    parser.add_argument(
        '--title',
        type=str,
        required=True,
        help='Document title'
    )
    parser.add_argument(
        '--topic',
        type=str,
        help='Topic (must be in allowed topics list)'
    )
    parser.add_argument(
        '--subtitle',
        type=str,
        help='Optional subtitle'
    )
    parser.add_argument(
        '--author',
        type=str,
        help='Optional author name'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=None,
        help='Output directory (default: generated/guides/)'
    )
    parser.add_argument(
        '--output-file',
        type=Path,
        default=None,
        help='Output file path (overrides --output)'
    )

    args = parser.parse_args()

    # Determine output path
    if args.output_file:
        output_path = args.output_file
    else:
        output_dir = args.output or (SUCCULENT_PDFS_ROOT / 'generated' / 'guides')
        # Generate filename from title
        safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in args.title)
        safe_title = safe_title.replace(' ', '_').lower()
        output_path = output_dir / f"{safe_title}.pdf"

    # Load config
    config = load_config()

    # Generate PDF
    success = generate_pdf_safe(
        content_path=args.content,
        output_path=output_path,
        title=args.title,
        topic=args.topic,
        subtitle=args.subtitle,
        author=args.author,
        config=config
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
