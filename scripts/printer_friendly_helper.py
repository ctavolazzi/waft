#!/usr/bin/env python3
"""
Printer-Friendly PDF Helper
============================

Utility functions to convert HTML/CSS templates to printer-friendly
(black and white) versions. Removes colors, simplifies graphics,
and optimizes for black-and-white printing.

Usage:
    from scripts.printer_friendly_helper import convert_to_printer_friendly
    
    printer_friendly_css = convert_to_printer_friendly(original_css)
"""

import re
from typing import Dict, Tuple


def convert_css_to_printer_friendly(css: str) -> str:
    """
    Convert CSS to printer-friendly version (black and white only).
    
    Removes:
    - All color values (replaces with black/white/gray)
    - Colored backgrounds (replaces with white/light gray)
    - Colored borders (replaces with black)
    - Colored text (replaces with black)
    
    Args:
        css: Original CSS string
        
    Returns:
        Printer-friendly CSS string
    """
    # Color replacements: convert all colors to black/white/gray scale
    color_replacements = {
        # Red colors -> black
        r'#c00\b': '#000',
        r'#f00\b': '#000',
        r'#ff0000\b': '#000',
        r'color:\s*#c00': 'color: #000',
        r'color:\s*#f00': 'color: #000',
        r'color:\s*#ff0000': 'color: #000',
        
        # Orange/Yellow colors -> black
        r'#f90\b': '#000',
        r'#ff0\b': '#000',
        r'#ffff00\b': '#000',
        r'color:\s*#f90': 'color: #000',
        r'color:\s*#ff0': 'color: #000',
        
        # Blue colors -> black
        r'#06c\b': '#000',
        r'#3498db\b': '#000',
        r'color:\s*#06c': 'color: #000',
        r'color:\s*#3498db': 'color: #000',
        
        # Colored backgrounds -> white or light gray
        r'background:\s*#ffe\b': 'background: #fff',
        r'background:\s*#fff9f0\b': 'background: #fff',
        r'background:\s*#f0f8ff\b': 'background: #fff',
        r'background:\s*#f8f9fa\b': 'background: #f5f5f5',
        r'background:\s*#ff0\b': 'background: #fff',
        r'background:\s*#f5f5f5\b': 'background: #f5f5f5',  # Keep light gray
        
        # Colored borders -> black
        r'border.*:\s*\d+px\s+solid\s+#c00': lambda m: m.group(0).replace('#c00', '#000'),
        r'border.*:\s*\d+px\s+solid\s+#f90': lambda m: m.group(0).replace('#f90', '#000'),
        r'border.*:\s*\d+px\s+double\s+#[0-9a-fA-F]{3,6}': lambda m: m.group(0).split('#')[0] + '#000',
        r'border-left:\s*\d+px\s+solid\s+#06c': lambda m: m.group(0).replace('#06c', '#000'),
        
        # Remove background colors from colored boxes
        r'background:\s*#[0-9a-fA-F]{3,6}(?=\s*;)': '#fff',
    }
    
    result = css
    
    # Apply simple replacements
    for pattern, replacement in color_replacements.items():
        if callable(replacement):
            result = re.sub(pattern, replacement, result)
        else:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    
    # Convert all hex colors in color: properties to black
    result = re.sub(
        r'color:\s*#[0-9a-fA-F]{3,6}(?=\s*[;})])',
        'color: #000',
        result,
        flags=re.IGNORECASE
    )
    
    # Convert all hex colors in background: properties to white (except light grays)
    def replace_background(match):
        color = match.group(1).lower()
        # Keep light grays (#f0-f9 range)
        if color in ['#f0f0f0', '#f5f5f5', '#f9f9f9', '#fafafa']:
            return match.group(0)
        return f'background: #fff'
    
    result = re.sub(
        r'background:\s*(#[0-9a-fA-F]{3,6})(?=\s*[;})])',
        replace_background,
        result,
        flags=re.IGNORECASE
    )
    
    # Convert border colors to black
    result = re.sub(
        r'border(?:-[a-z]+)?:\s*\d+px\s+(?:solid|dashed|dotted)\s+(#[0-9a-fA-F]{3,6})(?=\s*[;})])',
        lambda m: m.group(0).replace(m.group(2), '#000'),
        result,
        flags=re.IGNORECASE
    )
    
    return result


def convert_html_template_to_printer_friendly(html_template: str) -> str:
    """
    Convert an HTML template to printer-friendly version.
    
    This function:
    1. Extracts CSS from <style> tags
    2. Converts CSS to printer-friendly
    3. Replaces colored elements with text labels
    4. Returns modified HTML
    
    Args:
        html_template: Original HTML template string
        
    Returns:
        Printer-friendly HTML template string
    """
    result = html_template
    
    # Extract and replace CSS in <style> tags
    def replace_style(match):
        css_content = match.group(1)
        printer_friendly_css = convert_css_to_printer_friendly(css_content)
        return f'<style>\n{printer_friendly_css}\n</style>'
    
    result = re.sub(
        r'<style>(.*?)</style>',
        replace_style,
        result,
        flags=re.DOTALL | re.IGNORECASE
    )
    
    # Replace emoji/symbol warnings with text labels
    result = result.replace('⚠ ', '[WARNING] ')
    result = result.replace('☐ ', '[ ] ')
    result = result.replace('☑ ', '[X] ')
    
    return result


def create_printer_friendly_field_guide_template() -> str:
    """
    Create a printer-friendly field guide template.
    
    Returns:
        Complete HTML template string for printer-friendly field guide
    """
    # This is the same template from generate_waft_field_guide_printer_friendly.py
    # but extracted as a reusable function
    from pathlib import Path
    template_file = Path(__file__).parent.parent / "examples" / "generate_waft_field_guide_printer_friendly.py"
    
    # Read the template from the file
    with open(template_file, 'r') as f:
        content = f.read()
        # Extract the PRINTER_FRIENDLY_TEMPLATE constant
        match = re.search(r'PRINTER_FRIENDLY_TEMPLATE = """(.*?)"""', content, re.DOTALL)
        if match:
            return match.group(1)
    
    # Fallback: return basic template
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
    <style>
        @page { size: letter; margin: 0.75in 0.5in; }
        body { font-family: Arial, sans-serif; font-size: 10pt; color: #000; }
        h2 { background: #000; color: #fff; padding: 0.1in; }
        .warning, .caution, .note { border: 2px solid #000; background: #fff; padding: 0.15in; }
    </style>
</head>
<body>
    <div class="cover">
        <h1>{{ title }}</h1>
        {% if subtitle %}<p>{{ subtitle }}</p>{% endif %}
    </div>
    {{ content | safe }}
</body>
</html>
"""


if __name__ == "__main__":
    # Test the conversion
    test_css = """
    .warning {
        border: 3px solid #c00;
        background: #ffe;
        color: #c00;
    }
    .note {
        border-left: 4px solid #06c;
        background: #f0f8ff;
        color: #06c;
    }
    """
    
    print("Original CSS:")
    print(test_css)
    print("\n" + "="*60 + "\n")
    print("Printer-Friendly CSS:")
    print(convert_css_to_printer_friendly(test_css))
