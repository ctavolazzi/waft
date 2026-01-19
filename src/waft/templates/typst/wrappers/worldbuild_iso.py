"""
Worldbuilding Template with ISO 7010 Safety Symbols

Uses the typsium-iso-7010 package to add safety symbols and icons
to worldbuilding documents for enhanced visual communication.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from ..compiler import TypstCompiler


def generate_worldbuild_iso(
    title: str,
    content: str,
    output_path: Path,
    doc_id: str = "WB-001",
    subtitle: Optional[str] = None,
    classification: str = "INTERNAL",
    issued_by: Optional[str] = None,
    date: Optional[str] = None,
    safety_symbols: Optional[List[Dict[str, Any]]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Path:
    """
    Generate a worldbuilding document with ISO 7010 safety symbols.
    
    Args:
        title: Document title
        content: Main content (Typst markup)
        output_path: Where to save PDF
        doc_id: Document ID (e.g., "WB-001")
        subtitle: Optional subtitle
        classification: Security classification
        issued_by: Issuing organization
        date: Issue date (ISO format or "now")
        safety_symbols: List of safety symbols to include
            Format: [{"symbol": "warning", "label": "Hazard", "description": "..."}, ...]
        metadata: Additional metadata
        
    Returns:
        Path to generated PDF
    """
    if date is None or date == "now":
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Build safety symbols section if provided
    symbols_section = ""
    if safety_symbols:
        symbols_section = "\n== Safety Symbols\n\n"
        for symbol_data in safety_symbols:
            function_name = symbol_data.get("function", "warning-sign")
            code = symbol_data.get("code", 1)
            label = symbol_data.get("label", "")
            description = symbol_data.get("description", "")
            
            # Build function call - need to construct it carefully to avoid hyphen issues
            # Typst interprets hyphens in f-strings as subtraction, so build the call as a complete string
            func_call_line = f"#{function_name}({code}, height: 2cm)"
            symbols_section += f"""
#grid(
    columns: (1fr, 3fr),
    align: center,
    [
        {func_call_line}
    ],
    [
        *{label}*
        
        {description}
    ]
)

"""
    
    # Build Typst content - use double braces to escape in f-strings
    footer_notice_text = metadata.get("footer_notice", "") if metadata else ""
    
    # Build conditional sections
    subtitle_section = f'\n            #v(0.1in)\n            #set text(size: 11pt, style: "italic")\n            {subtitle}' if subtitle else ''
    issued_by_section = f'\n            #v(0.1in)\n            #set text(size: 9pt)\n            *Issued by:* {issued_by}\n            \n            #v(0.05in)\n            *Date:* {date}' if issued_by else ''
    classification_banner = f'''#rect(
    width: 100%,
    fill: rgb("#c00"),
    [
        #set text(fill: white, size: 11pt, weight: "bold")
        #align(center)[
            #v(0.1in)
            {classification}
            #v(0.1in)
        ]
    ]
)

#v(0.2in)
''' if classification else ''
    footer_section = f'''#v(0.3in)
#line(length: 100%, stroke: 1pt)
#v(0.1in)
#set text(size: 7pt, fill: rgb("#666"))
#align(center)[{footer_notice_text}]
''' if footer_notice_text else ''
    
    typst_content = f'''#import "@preview/typsium-iso-7010:0.1.0": *

#set page(
    paper: "us-letter",
    margin: (top: 0.6in, bottom: 0.5in, left: 0.5in, right: 0.5in),
    numbering: "1",
    header: [
        #set text(size: 8pt)
        #align(left)[{doc_id}]
        #align(right)[Page #counter(page)]
    ],
    footer: [
        #set text(size: 7pt, fill: rgb("#c00"))
        #align(center)[*{classification}*]
    ]
)

#set text(size: 10pt)
#set heading(numbering: "1.")
#show heading: set text(size: 1.2em)

// Document Header
#align(center)[
    #rect(
        width: 100%,
        height: auto,
        stroke: 3pt,
        [
            #v(0.25in)
            
            #set text(size: 10pt, weight: "bold")
            {doc_id}
            
            #v(0.1in)
            
            #set text(size: 18pt, weight: "bold")
            {title}
            {subtitle_section}
            {issued_by_section}
            
            #v(0.25in)
        ]
    )
]

// Classification Banner
{classification_banner}
// Safety Symbols Section
{symbols_section}
// Main Content
{content}
// Footer Notice
{footer_section}
'''
    
    # Compile to PDF
    compiler = TypstCompiler()
    pdf_path = compiler.compile(
        typst_content=typst_content,
        output_path=output_path
    )
    
    return pdf_path


def generate_worldbuild_with_symbols(
    title: str,
    content: str,
    output_path: Path,
    symbols: Optional[List[str]] = None,
    **kwargs
) -> Path:
    """
    Convenience function to generate worldbuilding document with common safety symbols.
    
    Args:
        title: Document title
        content: Main content
        output_path: Output PDF path
        symbols: List of symbol names to include (e.g., ["warning", "danger", "prohibition"])
        **kwargs: Additional arguments passed to generate_worldbuild_iso
        
    Returns:
        Path to generated PDF
    """
    # Map common symbol names to ISO 7010 symbols and function names
    # Based on typsium-iso-7010 package: available functions are warning-sign, fire-sign, emergency-sign
    symbol_map = {
        "warning": {"function": "warning-sign", "code": 1, "label": "General Warning", "description": "Warning of a general nature"},
        "danger": {"function": "warning-sign", "code": 2, "label": "Danger", "description": "Dangerous situation"},
        "prohibition": {"function": "warning-sign", "code": 1, "label": "Warning - Prohibited Area", "description": "Area where entry is prohibited"},
        "mandatory": {"function": "warning-sign", "code": 1, "label": "Warning - Required Action", "description": "Action is required in this area"},
        "emergency": {"function": "emergency-sign", "code": 1, "label": "Emergency Exit", "description": "Emergency exit/escape route"},
        "fire": {"function": "fire-sign", "code": 1, "label": "Fire Equipment", "description": "Location of fire-fighting equipment"},
        "first_aid": {"function": "emergency-sign", "code": 2, "label": "First Aid", "description": "First aid station or equipment"},
        "electric": {"function": "warning-sign", "code": 3, "label": "Electric Shock", "description": "Risk of electric shock"},
        "radiation": {"function": "warning-sign", "code": 4, "label": "Ionizing Radiation", "description": "Ionizing radiation hazard"},
        "biohazard": {"function": "warning-sign", "code": 5, "label": "Biological Hazard", "description": "Biological hazard"},
    }
    
    safety_symbols = []
    if symbols:
        for symbol_name in symbols:
            if symbol_name.lower() in symbol_map:
                safety_symbols.append(symbol_map[symbol_name.lower()])
            else:
                # Use as-is if not in map - try to guess function name
                function_name = symbol_name.lower().replace("_", "-") + "-sign"
                safety_symbols.append({
                    "function": function_name,
                    "code": 1,
                    "label": symbol_name.title(),
                    "description": f"{symbol_name.title()} symbol"
                })
    
    return generate_worldbuild_iso(
        title=title,
        content=content,
        output_path=output_path,
        safety_symbols=safety_symbols if safety_symbols else None,
        **kwargs
    )
