"""
Document Binder System
======================

Assemble multiple documents into cohesive collections.
Create printable books, project binders, document collections.

Philosophy:
-----------
A binder is more than a PDF merger. It's a COLLECTION with:
- Consistent styling across documents
- Section dividers
- Table of contents
- Index
- Cover page
- Unified narrative

This is worldbuilding infrastructure. A binder tells a STORY through documents.

Example Use Cases:
-----------------
- PROJECT LIGHTCONE Master File (13 classified docs)
- WAFT System Documentation (architecture, APIs, guides)
- Company Annual Report (financials, operations, vision)
- Research Compilation (papers, data, conclusions)
- Training Manual (guides, procedures, references)
"""

import datetime
from dataclasses import dataclass, field
from pathlib import Path

from jinja2 import Template
from pypdf import PdfWriter
from weasyprint import HTML


@dataclass
class DocumentEntry:
    """A single document in the binder."""

    path: Path
    title: str
    section: str | None = None
    author: str | None = None
    date: str | None = None
    description: str | None = None

    def __post_init__(self):
        """Validate document exists."""
        if not self.path.exists():
            raise FileNotFoundError(f"Document not found: {self.path}")


@dataclass
class BinderSection:
    """A section in the binder (e.g., Tab 1: Doctrine)."""

    name: str
    description: str | None = None
    documents: list[DocumentEntry] = field(default_factory=list)
    color: str = "#2c3e50"  # Section color for divider

    def add_document(self, doc: DocumentEntry):
        """Add document to this section."""
        self.documents.append(doc)


class Binder:
    """
    Assemble multiple documents into a cohesive binder.

    A binder is a collection with structure:
    - Cover page
    - Table of contents
    - Section dividers
    - Documents
    - Index (optional)
    - Back matter (optional)

    Example:
        binder = Binder(
            title="PROJECT LIGHTCONE Master File",
            subtitle="Quantum Teleportation Documentation",
            classification="TOP SECRET // ORACLE EYES ONLY"
        )

        # Add sections
        tab1 = binder.add_section("Tab 1: Doctrine", color="#c00")
        tab2 = binder.add_section("Tab 2: Engineering", color="#06c")

        # Add documents
        tab1.add_document(DocumentEntry(
            path=Path("TM-VIS-001.pdf"),
            title="Light Cone Topology",
            author="Dr. Morrison"
        ))

        # Generate
        binder.generate(Path("LIGHTCONE_BINDER.pdf"))
    """

    def __init__(
        self,
        title: str,
        subtitle: str = None,
        classification: str = None,
        project_id: str = None,
        organization: str = None,
        date: str = None,
        version: str = "1.0",
        compiled_by: str = None,
        cover_style: str = "professional",  # professional, classified, academic, creative
    ):
        self.title = title
        self.subtitle = subtitle
        self.classification = classification
        self.project_id = project_id
        self.organization = organization
        self.date = date or datetime.date.today().strftime("%B %d, %Y")
        self.version = version
        self.compiled_by = compiled_by
        self.cover_style = cover_style

        self.sections: list[BinderSection] = []
        self.front_matter: list[Path] = []  # Additional front matter PDFs
        self.back_matter: list[Path] = []  # Additional back matter PDFs

    def add_section(
        self, name: str, description: str = None, color: str = "#2c3e50"
    ) -> BinderSection:
        """Add a section to the binder."""
        section = BinderSection(name=name, description=description, color=color)
        self.sections.append(section)
        return section

    def add_front_matter(self, pdf_path: Path):
        """Add PDF to front matter (before TOC)."""
        if not pdf_path.exists():
            raise FileNotFoundError(f"Front matter not found: {pdf_path}")
        self.front_matter.append(pdf_path)

    def add_back_matter(self, pdf_path: Path):
        """Add PDF to back matter (after all documents)."""
        if not pdf_path.exists():
            raise FileNotFoundError(f"Back matter not found: {pdf_path}")
        self.back_matter.append(pdf_path)

    def _generate_cover(self, output_dir: Path) -> Path:
        """Generate cover page."""

        if self.cover_style == "classified":
            template = self._get_classified_cover_template()
        elif self.cover_style == "academic":
            template = self._get_academic_cover_template()
        elif self.cover_style == "creative":
            template = self._get_creative_cover_template()
        else:  # professional
            template = self._get_professional_cover_template()

        html = Template(template).render(
            title=self.title,
            subtitle=self.subtitle,
            classification=self.classification,
            project_id=self.project_id,
            organization=self.organization,
            date=self.date,
            version=self.version,
            compiled_by=self.compiled_by,
            num_sections=len(self.sections),
            num_documents=sum(len(s.documents) for s in self.sections),
        )

        cover_path = output_dir / "binder_cover.pdf"
        HTML(string=html).write_pdf(cover_path)
        return cover_path

    def _generate_toc(self, output_dir: Path) -> Path:
        """Generate table of contents."""

        template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {
            size: letter;
            margin: 1in;
        }
        body {
            font-family: 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.5;
        }
        h1 {
            text-align: center;
            font-size: 24pt;
            margin-bottom: 0.5in;
            border-bottom: 3px solid #000;
            padding-bottom: 0.15in;
        }
        .section {
            margin-top: 0.3in;
            page-break-inside: avoid;
        }
        .section-name {
            font-size: 14pt;
            font-weight: bold;
            color: {{ section.color }};
            border-left: 4px solid {{ section.color }};
            padding-left: 0.1in;
            margin-bottom: 0.1in;
        }
        .section-description {
            font-size: 10pt;
            color: #666;
            font-style: italic;
            margin-left: 0.15in;
            margin-bottom: 0.1in;
        }
        .doc-list {
            margin-left: 0.3in;
        }
        .doc-entry {
            margin-bottom: 0.08in;
            display: flex;
            justify-content: space-between;
        }
        .doc-title {
            font-weight: bold;
        }
        .doc-meta {
            font-size: 9pt;
            color: #666;
            margin-left: 0.2in;
        }
    </style>
</head>
<body>
    <h1>Table of Contents</h1>

    {% for section in sections %}
    <div class="section">
        <div class="section-name" style="color: {{ section.color }}; border-left-color: {{ section.color }};">
            {{ section.name }}
        </div>
        {% if section.description %}
        <div class="section-description">{{ section.description }}</div>
        {% endif %}
        <div class="doc-list">
            {% for doc in section.documents %}
            <div class="doc-entry">
                <div>
                    <span class="doc-title">{{ doc.title }}</span>
                    {% if doc.author or doc.date %}
                    <span class="doc-meta">
                        {% if doc.author %}{{ doc.author }}{% endif %}
                        {% if doc.author and doc.date %} | {% endif %}
                        {% if doc.date %}{{ doc.date }}{% endif %}
                    </span>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    {% endfor %}
</body>
</html>
        """

        html = Template(template).render(sections=self.sections)
        toc_path = output_dir / "binder_toc.pdf"
        HTML(string=html).write_pdf(toc_path)
        return toc_path

    def _generate_section_divider(self, section: BinderSection, output_dir: Path) -> Path:
        """Generate section divider page."""

        template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {
            size: letter;
            margin: 0;
            background: {{ section.color }};
        }
        body {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            color: #fff;
            font-family: 'Arial Black', sans-serif;
        }
        .content {
            text-align: center;
        }
        .section-name {
            font-size: 48pt;
            font-weight: bold;
            text-transform: uppercase;
            margin-bottom: 0.3in;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        }
        .section-description {
            font-size: 18pt;
            font-family: 'Georgia', serif;
            font-style: italic;
            font-weight: normal;
        }
    </style>
</head>
<body>
    <div class="content">
        <div class="section-name">{{ section.name }}</div>
        {% if section.description %}
        <div class="section-description">{{ section.description }}</div>
        {% endif %}
    </div>
</body>
</html>
        """

        html = Template(template).render(section=section)
        divider_path = output_dir / f"divider_{section.name.replace(' ', '_')}.pdf"
        HTML(string=html).write_pdf(divider_path)
        return divider_path

    def generate(self, output_path: Path, include_dividers: bool = True) -> Path:
        """
        Generate the complete binder.

        Args:
            output_path: Where to save the binder PDF
            include_dividers: Include section divider pages

        Returns:
            Path to generated binder
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_dir = output_path.parent / ".binder_temp"
        temp_dir.mkdir(exist_ok=True)

        try:
            merger = PdfWriter()

            # 1. Cover page
            print("Generating cover page...")
            cover = self._generate_cover(temp_dir)
            merger.append(str(cover))

            # 2. Front matter
            for fm in self.front_matter:
                print(f"Adding front matter: {fm.name}")
                merger.append(str(fm))

            # 3. Table of contents
            print("Generating table of contents...")
            toc = self._generate_toc(temp_dir)
            merger.append(str(toc))

            # 4. Sections and documents
            for section in self.sections:
                # Section divider
                if include_dividers:
                    print(f"Generating divider: {section.name}")
                    divider = self._generate_section_divider(section, temp_dir)
                    merger.append(str(divider))

                # Documents in section
                for doc in section.documents:
                    print(f"Adding document: {doc.title}")
                    merger.append(str(doc.path))

            # 5. Back matter
            for bm in self.back_matter:
                print(f"Adding back matter: {bm.name}")
                merger.append(str(bm))

            # Write final binder
            print(f"Writing binder to {output_path}")
            with open(output_path, "wb") as f:
                merger.write(f)

            print(f"✓ Binder generated: {output_path.name}")
            print(f"  Size: {output_path.stat().st_size:,} bytes")
            print(f"  Sections: {len(self.sections)}")
            print(f"  Documents: {sum(len(s.documents) for s in self.sections)}")

            return output_path

        finally:
            # Cleanup temp files
            import shutil

            if temp_dir.exists():
                shutil.rmtree(temp_dir)

    def _get_professional_cover_template(self) -> str:
        """Professional cover template."""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page { size: letter; margin: 0; }
        body {
            margin: 0;
            padding: 1.5in 1in;
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .header {
            border-bottom: 3px solid #fff;
            padding-bottom: 0.3in;
        }
        .title {
            font-size: 42pt;
            font-weight: bold;
            margin-bottom: 0.2in;
            line-height: 1.2;
        }
        .subtitle {
            font-size: 20pt;
            font-weight: 300;
        }
        .meta {
            font-size: 14pt;
            line-height: 1.8;
        }
        .footer {
            border-top: 2px solid #fff;
            padding-top: 0.2in;
            font-size: 11pt;
        }
    </style>
</head>
<body>
    <div class="header">
        {% if project_id %}<div>{{ project_id }}</div>{% endif %}
        {% if organization %}<div style="font-size: 14pt; margin-top: 0.1in;">{{ organization }}</div>{% endif %}
    </div>
    <div>
        <div class="title">{{ title }}</div>
        {% if subtitle %}<div class="subtitle">{{ subtitle }}</div>{% endif %}
    </div>
    <div class="meta">
        <div>Version {{ version }}</div>
        <div>{{ date }}</div>
        {% if compiled_by %}<div>Compiled by {{ compiled_by }}</div>{% endif %}
        <div style="margin-top: 0.2in;">{{ num_sections }} Sections | {{ num_documents }} Documents</div>
    </div>
    <div class="footer">
        {% if classification %}<div>{{ classification }}</div>{% endif %}
    </div>
</body>
</html>
        """

    def _get_classified_cover_template(self) -> str:
        """Classified document cover template."""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page { size: letter; margin: 0; }
        body {
            margin: 0;
            padding: 0;
            font-family: 'Courier New', monospace;
            background: #000;
            color: #0f0;
            height: 100vh;
        }
        .classification-top {
            background: #f00;
            color: #fff;
            text-align: center;
            padding: 0.2in;
            font-weight: bold;
            font-size: 16pt;
        }
        .content {
            padding: 1.5in 1in;
            border: 5px solid #f00;
            margin: 0.5in;
            height: calc(100vh - 3in);
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .title {
            font-size: 32pt;
            font-weight: bold;
            text-align: center;
            margin-bottom: 0.5in;
            text-transform: uppercase;
        }
        .meta {
            text-align: center;
            font-size: 14pt;
            line-height: 2;
        }
        .warning {
            border: 3px solid #f00;
            background: #300;
            color: #f00;
            padding: 0.2in;
            margin-top: 0.5in;
            text-align: center;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="classification-top">{{ classification or 'CLASSIFIED' }}</div>
    <div class="content">
        <div class="title">{{ title }}</div>
        {% if subtitle %}<div style="text-align: center; font-size: 16pt; margin-bottom: 0.3in;">{{ subtitle }}</div>{% endif %}
        <div class="meta">
            {% if project_id %}<div>{{ project_id }}</div>{% endif %}
            {% if organization %}<div>{{ organization }}</div>{% endif %}
            <div>{{ date }}</div>
            <div>VERSION {{ version }}</div>
        </div>
        <div class="warning">
            UNAUTHORIZED ACCESS PROHIBITED<br>
            {{ num_sections }} SECTIONS | {{ num_documents }} DOCUMENTS
        </div>
    </div>
</body>
</html>
        """

    def _get_academic_cover_template(self) -> str:
        """Academic cover template."""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page { size: letter; margin: 1in; }
        body {
            font-family: 'Times New Roman', serif;
            text-align: center;
            padding-top: 2.5in;
        }
        .title {
            font-size: 24pt;
            font-weight: bold;
            margin-bottom: 0.3in;
        }
        .subtitle {
            font-size: 16pt;
            margin-bottom: 0.5in;
        }
        .meta {
            font-size: 12pt;
            line-height: 2;
            margin-top: 1in;
        }
        .organization {
            margin-top: 0.5in;
            font-size: 14pt;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="title">{{ title }}</div>
    {% if subtitle %}<div class="subtitle">{{ subtitle }}</div>{% endif %}
    <div class="meta">
        {% if compiled_by %}<div>{{ compiled_by }}</div>{% endif %}
        {% if organization %}<div class="organization">{{ organization }}</div>{% endif %}
        <div>{{ date }}</div>
        <div>Version {{ version }}</div>
    </div>
</body>
</html>
        """

    def _get_creative_cover_template(self) -> str:
        """Creative cover template."""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page { size: letter; margin: 0; }
        body {
            margin: 0;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
            background-size: 400% 400%;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Georgia', serif;
        }
        .content {
            background: rgba(255,255,255,0.95);
            padding: 1in;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 6in;
        }
        .title {
            font-size: 36pt;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 0.3in;
        }
        .subtitle {
            font-size: 18pt;
            color: #7f8c8d;
            margin-bottom: 0.5in;
        }
        .meta {
            font-size: 12pt;
            color: #95a5a6;
            line-height: 1.8;
        }
    </style>
</head>
<body>
    <div class="content">
        <div class="title">{{ title }}</div>
        {% if subtitle %}<div class="subtitle">{{ subtitle }}</div>{% endif %}
        <div class="meta">
            <div>{{ date }}</div>
            {% if compiled_by %}<div>{{ compiled_by }}</div>{% endif %}
            <div style="margin-top: 0.3in; font-weight: bold;">
                {{ num_sections }} Sections | {{ num_documents }} Documents
            </div>
        </div>
    </div>
</body>
</html>
        """
