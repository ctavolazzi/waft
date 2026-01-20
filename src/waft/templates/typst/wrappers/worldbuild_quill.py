"""
Worldbuilding Template with Quill (Quantum Circuit Diagrams)

Uses the quill package to create quantum circuit diagrams, magical energy flows,
and technical diagrams for sci-fi/fantasy worldbuilding.
"""

from pathlib import Path
from typing import Any

from ..compiler import TypstCompiler


def generate_worldbuild_quantum_circuit(
    title: str,
    content: str,
    output_path: Path,
    circuits: list[dict[str, Any]] | None = None,
    doc_id: str = "WB-QC-001",
    subtitle: str | None = None,
    classification: str = "INTERNAL",
    metadata: dict[str, Any] | None = None,
) -> Path:
    """
    Generate a worldbuilding document with quantum circuit diagrams using quill.

    Args:
        title: Document title
        content: Main content (Typst markup)
        output_path: Where to save PDF
        circuits: List of circuit definitions
            Format: [{"name": "...", "circuit": "...", "description": "..."}, ...]
        doc_id: Document ID
        subtitle: Optional subtitle
        classification: Security classification
        metadata: Additional metadata

    Returns:
        Path to generated PDF
    """
    # Build circuits section if provided
    circuits_section = ""
    if circuits:
        circuits_section = "\n== Quantum Circuit Diagrams\n\n"
        for circuit_data in circuits:
            circuit_name = circuit_data.get("name", "Circuit")
            circuit_code = circuit_data.get("circuit", "")
            description = circuit_data.get("description", "")

            # Escape circuit code properly for Typst
            # The circuit code should be inserted as-is since it's already Typst code
            circuits_section += f"""
=== {circuit_name}

{description}

#quantum-circuit(
{circuit_code}
)

"""

    # Build Typst content
    footer_notice_text = metadata.get("footer_notice", "") if metadata else ""
    subtitle_section = (
        f'\n            #v(0.1in)\n            #set text(size: 11pt, style: "italic")\n            {subtitle}'
        if subtitle
        else ""
    )
    classification_banner = (
        f"""#rect(
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
"""
        if classification
        else ""
    )
    footer_section = (
        f"""#v(0.3in)
#line(length: 100%, stroke: 1pt)
#v(0.1in)
#set text(size: 7pt, fill: rgb("#666"))
#align(center)[{footer_notice_text}]
"""
        if footer_notice_text
        else ""
    )

    typst_content = f"""#import "@preview/quill:0.7.2": *

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

            #v(0.25in)
        ]
    )
]

// Classification Banner
{classification_banner}
// Quantum Circuit Diagrams Section
{circuits_section}
// Main Content
{content}
// Footer Notice
{footer_section}
"""

    # Compile to PDF
    compiler = TypstCompiler()
    pdf_path = compiler.compile(typst_content=typst_content, output_path=output_path)

    return pdf_path


def generate_worldbuild_magical_circuit(
    title: str,
    content: str,
    output_path: Path,
    circuit_description: str,
    circuit_code: str,
    **kwargs,
) -> Path:
    """
    Generate a worldbuilding document with a magical/quantum energy circuit.

    Args:
        title: Document title
        content: Main content
        output_path: Output PDF path
        circuit_description: Description of the circuit
        circuit_code: Quill circuit code (e.g., "lstick($|0〉$), $H$, ctrl(1), targ()")
        **kwargs: Additional arguments passed to generate_worldbuild_quantum_circuit

    Returns:
        Path to generated PDF
    """
    circuits = [
        {
            "name": "Magical Energy Flow Circuit",
            "circuit": circuit_code,
            "description": circuit_description,
        }
    ]

    return generate_worldbuild_quantum_circuit(
        title=title, content=content, output_path=output_path, circuits=circuits, **kwargs
    )


def generate_worldbuild_tequila_circuit(
    title: str, content: str, output_path: Path, gates: list[dict[str, Any]], **kwargs
) -> Path:
    """
    Generate a worldbuilding document using Tequila model (instruction-driven).

    Args:
        title: Document title
        content: Main content
        output_path: Output PDF path
        gates: List of gate instructions
            Format: [{"type": "h", "qubit": 0}, {"type": "cx", "control": 0, "target": 1}, ...]
        **kwargs: Additional arguments

    Returns:
        Path to generated PDF
    """
    # Build Tequila circuit code
    gate_calls = []
    for gate in gates:
        gate_type = gate.get("type", "h")
        if gate_type == "h":
            gate_calls.append(f"tq.h({gate.get('qubit', 0)})")
        elif gate_type == "cx":
            gate_calls.append(f"tq.cx({gate.get('control', 0)}, {gate.get('target', 1)})")
        elif gate_type == "x":
            gate_calls.append(f"tq.x({gate.get('qubit', 0)})")
        elif gate_type == "z":
            gate_calls.append(f"tq.z({gate.get('qubit', 0)})")
        elif gate_type == "p":
            gate_calls.append(f"tq.p(${gate.get('phase', 'pi')}$, {gate.get('qubit', 0)})")
        # Add more gate types as needed

    circuit_code = "..tq.build(\n    " + ",\n    ".join(gate_calls) + "\n  )"

    circuits = [
        {
            "name": "Tequila Circuit",
            "circuit": circuit_code,
            "description": "Automatically laid out quantum circuit",
        }
    ]

    # Need to import tequila in the Typst content
    # This is a simplified version - full implementation would need to handle the import
    return generate_worldbuild_quantum_circuit(
        title=title, content=content, output_path=output_path, circuits=circuits, **kwargs
    )
