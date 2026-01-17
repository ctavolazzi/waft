#!/usr/bin/env python3
"""
Catalog the Unicamp template with Librarian.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.waft.pantheon.library.librarian import Librarian
from src.waft.pantheon.library.record_catalog import RecordEntry
from datetime import datetime

# Initialize Librarian
project_path = Path(__file__).parent.parent.parent
librarian = Librarian(project_path=project_path)

# Create catalog entry for the template
template_entry = RecordEntry(
    record_id="template_unicamp_physics_report",
    record_type="template",
    source="waft_templates",
    path="templates/unicamp-physics-report/main.tex",
    category="latex_template",
    subcategory="academic_report",
    tags=["latex", "pdf", "academic", "brazilian", "portuguese", "physics", "lab-report", "unicamp"],
    metadata={
        "name": "Unicamp Physics Report",
        "wrapper": "src/waft/templates/latex/wrappers/unicamp_report.py",
        "function": "generate_unicamp_report",
        "description": "Brazilian Portuguese academic report template from Instituto de Física Gleb Wataghin, Unicamp",
        "category": "report",
        "source_repo": "unicamp-physics-report",
        "language": "pt-BR",
        "institution": "Unicamp",
        "created_at": datetime.now().isoformat()
    },
    created_at=datetime.now().isoformat()
)

# Add to catalog
librarian.catalog.add_entry(template_entry)
librarian.catalog.save()

print(f"✅ Cataloged template: {template_entry.record_id}")
print(f"   Path: {template_entry.path}")
print(f"   Tags: {', '.join(template_entry.tags)}")

# Have Scribe write a script
librarian.scribe.write_script(
    "Cataloged Unicamp Physics Report LaTeX template",
    {
        "action": "catalog_template",
        "template_id": template_entry.record_id,
        "template_name": "Unicamp Physics Report"
    }
)

print("✅ Scribe script written")
