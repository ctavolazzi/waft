#!/usr/bin/env python3
"""
Test script for Unicamp Physics Report template.
"""

from pathlib import Path
from src.waft.templates.latex.wrappers.unicamp_report import generate_unicamp_report

# Test output directory
output_dir = Path(__file__).parent / "test_output"
output_dir.mkdir(exist_ok=True)

# Test data
test_report = generate_unicamp_report(
    title="Relatório I",
    content="# Test Report\n\nThis is a test of the Unicamp template.",
    output_path=output_dir / "test_report.pdf",
    professor="Prof. Dr. Flávio Caldas da Cruz",
    authors=[
        "Caroline Guimarães 155006",
        "Lucas Rodrigues Contador 156406",
        "Giovanne Lucas Dias Pereira Mariano 173317"
    ],
    course="Física Experimental IV",
    abstract="Este relatório apresenta os resultados do experimento realizado...",
    introduction="O propósito deste experimento é...",
    methodology="Os equipamentos utilizados foram...",
    results="Os resultados obtidos mostram que...",
    discussion="A análise dos resultados indica que...",
    conclusion="Concluímos que...",
    figures=[
        {
            "path": "frog.jpg",
            "caption": "This is a test figure",
            "label": "fig:test",
            "width": "0.3"
        }
    ]
)

print(f"✅ Report generated: {test_report}")
