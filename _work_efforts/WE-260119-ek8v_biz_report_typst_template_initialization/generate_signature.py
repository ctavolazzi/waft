#!/usr/bin/env python3
"""
Signature Generator for WAFT Pitch Packet
Generates signature images using cursive fonts for document signing.

Usage:
    python generate_signature.py "Claude" --output claude_signature.png
    python generate_signature.py "ctavolazzi" --output human_signature.png --color "#1a1a2e"
"""

import argparse
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Pillow not installed. Run: pip install Pillow")

# Common cursive/signature fonts (system fonts)
SIGNATURE_FONTS = [
    # macOS cursive fonts
    "Snell Roundhand",
    "Zapfino",
    "Bradley Hand",
    "Brush Script MT",
    "Lucida Handwriting",
    "Apple Chancery",
    # Cross-platform fallbacks
    "Segoe Script",
    "Comic Sans MS",
    "Georgia",
]

def find_font(size: int = 72):
    """Find an available cursive font on the system."""
    for font_name in SIGNATURE_FONTS:
        try:
            return ImageFont.truetype(font_name, size)
        except (OSError, IOError):
            continue
    # Fallback to default
    return ImageFont.load_default()

def generate_signature(
    name: str,
    output_path: str = "signature.png",
    font_size: int = 72,
    color: str = "#000080",  # Navy blue (traditional signature color)
    bg_color: str = None,  # Transparent by default
    padding: int = 20,
):
    """Generate a signature image from a name."""
    if not HAS_PIL:
        print("ERROR: Pillow required. Install with: pip install Pillow")
        return None
    
    # Parse color
    if color.startswith("#"):
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        text_color = (r, g, b, 255)
    else:
        text_color = color
    
    # Get font
    font = find_font(font_size)
    
    # Calculate text size
    dummy_img = Image.new("RGBA", (1, 1))
    dummy_draw = ImageDraw.Draw(dummy_img)
    bbox = dummy_draw.textbbox((0, 0), name, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Create image with padding
    width = text_width + (padding * 2)
    height = text_height + (padding * 2)
    
    if bg_color:
        if bg_color.startswith("#"):
            r = int(bg_color[1:3], 16)
            g = int(bg_color[3:5], 16)
            b = int(bg_color[5:7], 16)
            background = (r, g, b, 255)
        else:
            background = bg_color
    else:
        background = (255, 255, 255, 0)  # Transparent
    
    img = Image.new("RGBA", (width, height), background)
    draw = ImageDraw.Draw(img)
    
    # Draw signature text
    x = padding - bbox[0]
    y = padding - bbox[1]
    draw.text((x, y), name, font=font, fill=text_color)
    
    # Save
    output = Path(output_path)
    img.save(output, "PNG")
    print(f"✅ Signature saved to: {output}")
    return output

def generate_ai_signature(
    ai_name: str = "Claude",
    output_path: str = "ai_signature.png",
):
    """Generate a signature for an AI system."""
    # AI signatures use a distinct style
    return generate_signature(
        name=f"~ {ai_name} ~",
        output_path=output_path,
        font_size=60,
        color="#4a5568",  # Gray (indicates non-human)
        padding=30,
    )

def main():
    parser = argparse.ArgumentParser(description="Generate signature images")
    parser.add_argument("name", help="Name to sign")
    parser.add_argument("--output", "-o", default="signature.png", help="Output file path")
    parser.add_argument("--size", "-s", type=int, default=72, help="Font size")
    parser.add_argument("--color", "-c", default="#000080", help="Text color (hex)")
    parser.add_argument("--bg", "-b", default=None, help="Background color (hex, default transparent)")
    parser.add_argument("--ai", action="store_true", help="Generate AI-style signature")
    
    args = parser.parse_args()
    
    if args.ai:
        generate_ai_signature(args.name, args.output)
    else:
        generate_signature(
            name=args.name,
            output_path=args.output,
            font_size=args.size,
            color=args.color,
            bg_color=args.bg,
        )

if __name__ == "__main__":
    main()
