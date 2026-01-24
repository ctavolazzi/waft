#!/usr/bin/env python3
"""
Technical Whitepaper Generator
Automates creation of evidence-backed technical analysis documents using Typst.

Usage:
    python whitepaper_generator.py init <project-name>
    python whitepaper_generator.py write-section <section-id>
    python whitepaper_generator.py compile-section <section-id>
    python whitepaper_generator.py compile-all
    python whitepaper_generator.py status
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import yaml


class WhitepaperGenerator:
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.config_file = project_dir / "whitepaper_config.yaml"
        self.sections_dir = project_dir / "sections"
        self.pdfs_dir = project_dir / "section_pdfs"
        self.template_dir = project_dir / "typst_template"
        
        # Only load config if it exists
        self.config = self.load_config() if self.config_file.exists() else None
    
    def load_config(self) -> Dict:
        """Load whitepaper configuration."""
        if not self.config_file.exists():
            raise FileNotFoundError(f"Config not found: {self.config_file}")
        
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def init_project(self, project_name: str):
        """Initialize a new whitepaper project."""
        print(f"🎬 Initializing whitepaper project: {project_name}")
        
        # Create directory structure
        self.project_dir.mkdir(parents=True, exist_ok=True)
        self.sections_dir.mkdir(exist_ok=True)
        self.pdfs_dir.mkdir(exist_ok=True)
        self.template_dir.mkdir(exist_ok=True)
        
        # Create default config
        default_config = {
            "title": project_name,
            "author": "Technical Analyst",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "version": "1.0",
            "sections": [
                {"id": "00_title_page", "title": "Title Page", "pages": 1, "required": True},
                {"id": "01_abstract", "title": "Abstract", "pages": 1, "required": True},
                {"id": "02_executive_summary", "title": "Executive Summary", "pages": 1, "required": True},
                {"id": "10_introduction", "title": "Introduction", "pages": 4, "required": True},
                {"id": "20_methodology", "title": "Methodology", "pages": 3, "required": True},
                {"id": "30_findings", "title": "Findings", "pages": 10, "required": True},
                {"id": "40_analysis", "title": "Analysis", "pages": 10, "required": True},
                {"id": "50_discussion", "title": "Discussion", "pages": 5, "required": True},
                {"id": "60_conclusion", "title": "Conclusion", "pages": 2, "required": True},
                {"id": "A0_appendix", "title": "Appendix", "pages": 5, "required": False},
            ],
            "styling": {
                "primary_color": "#1976d2",
                "success_color": "#4caf50",
                "warning_color": "#f57c00",
                "danger_color": "#d32f2f",
                "font_body": "New Computer Modern",
                "font_code": "JetBrains Mono",
            },
        }
        
        with open(self.config_file, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        
        # Create functions template
        self._create_functions_template()
        
        # Create main template
        self._create_main_template()
        
        # Create section stubs
        for section in default_config["sections"]:
            self._create_section_stub(section)
        
        print(f"✅ Project initialized at: {self.project_dir}")
        print(f"📄 Config: {self.config_file}")
        print(f"📁 Sections: {self.sections_dir}")
    
    def _create_functions_template(self):
        """Create the reusable functions file."""
        functions_file = self.project_dir / "whitepaper_functions.typ"
        
        content = '''// Reusable functions for technical whitepapers

// CALLOUT BOXES
#let callout(type: "info", title: none, body) = {
  let colors = (
    info: (bg: rgb("#e3f2fd"), border: rgb("#1976d2")),
    warning: (bg: rgb("#fff3e0"), border: rgb("#f57c00")),
    danger: (bg: rgb("#ffebee"), border: rgb("#d32f2f")),
    success: (bg: rgb("#e8f5e9"), border: rgb("#388e3c")),
    note: (bg: rgb("#f3e5f5"), border: rgb("#7b1fa2")),
  )
  
  let color = colors.at(type, default: colors.info)
  
  v(0.15in)
  block(
    fill: color.bg,
    stroke: 2pt + color.border,
    radius: 4pt,
    inset: 16pt,
    width: 100%,
    [
      #if title != none [
        #text(weight: "bold", size: 12pt, fill: color.border)[#title]
        #v(0.05in)
      ]
      #body
    ]
  )
  v(0.15in)
}

// EVIDENCE BOX
#let evidence(location, content) = {
  callout(
    type: "success",
    title: [📁 Evidence: #location],
    content
  )
}

// METRIC DISPLAY
#let metric(label, value, unit: "") = {
  block(
    fill: rgb("#f5f5f5"),
    stroke: 1pt + rgb("#1976d2"),
    radius: 4pt,
    inset: 12pt,
    [
      #text(size: 10pt, fill: rgb("#666666"))[#label]
      #v(0.05in)
      #text(size: 18pt, weight: "bold", fill: rgb("#1976d2"))[#value]
      #if unit != "" [
        #text(size: 12pt, fill: rgb("#666666"))[ #unit]
      ]
    ]
  )
}
'''
        
        with open(functions_file, 'w') as f:
            f.write(content)
    
    def _create_main_template(self):
        """Create the main compilation file template."""
        main_file = self.project_dir / "MAIN.typ"
        
        content = f'''// {self.config["title"]} - Main Compilation File
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge
#import "@preview/tablex:0.0.9": tablex, cellx, rowspanx, colspanx
#import "whitepaper_functions.typ": callout, evidence, metric

// GLOBAL SETTINGS
#set document(
  title: "{self.config["title"]}",
  author: "{self.config["author"]}",
  date: datetime(year: {datetime.now().year}, month: {datetime.now().month}, day: {datetime.now().day}),
)

#set page(
  paper: "us-letter",
  margin: (top: 1in, bottom: 1in, left: 1.25in, right: 1.25in),
)

#set text(
  font: "{self.config["styling"]["font_body"]}",
  size: 11pt,
  fill: rgb("#333333"),
)

#set par(justify: true, leading: 0.65em, spacing: 1em)
#set heading(numbering: "1.1")

// CODE BLOCK STYLING
#show raw.where(block: true): it => {{
  set text(font: "{self.config["styling"]["font_code"]}", size: 9pt)
  block(
    fill: rgb("#f5f5f5"),
    stroke: 1pt + rgb("#cccccc"),
    radius: 4pt,
    inset: 12pt,
    width: 100%,
    it
  )
}}

#show raw.where(block: false): it => {{
  box(
    fill: rgb("#f0f0f0"),
    outset: (x: 3pt, y: 2pt),
    radius: 2pt,
    text(font: "{self.config["styling"]["font_code"]}", size: 10pt, it)
  )
}}

// HEADING STYLING
#show heading.where(level: 1): it => {{
  pagebreak(weak: true)
  block(
    width: 100%,
    fill: rgb("{self.config["styling"]["primary_color"]}"),
    inset: 16pt,
    radius: 4pt,
    text(fill: white, size: 20pt, weight: "bold", it.body)
  )
  v(0.3in)
}}

#show heading.where(level: 2): it => {{
  v(0.2in)
  block(
    width: 100%,
    text(fill: rgb("{self.config["styling"]["primary_color"]}"), size: 16pt, weight: "bold")[
      #counter(heading).display() #it.body
    ]
  )
  line(length: 100%, stroke: 2pt + rgb("{self.config["styling"]["primary_color"]}"))
  v(0.1in)
}}

// FRONT MATTER (Roman numerals)
#set page(
  numbering: "i",
  header: none,
  footer: context [
    #line(length: 100%, stroke: 0.5pt + rgb("#cccccc"))
    #v(0.05in)
    #align(center)[#text(size: 10pt, fill: rgb("#666666"))[Page #counter(page).display("i")]]
  ],
)

#counter(page).update(1)

// Include front matter sections
'''
        
        # Add section includes
        for section in self.config["sections"]:
            if section.get("required", False):
                content += f'#include "sections/{section["id"]}.typ"\n'
        
        content += '''
// MAIN BODY (Arabic numerals)
#set page(
  numbering: "1",
  header: context [
    #text(size: 10pt, fill: rgb("#666666"))[
      ''' + self.config["title"] + '''
      #h(1fr)
      #counter(page).display("1")
    ]
    #v(0.05in)
    #line(length: 100%, stroke: 0.5pt + rgb("#cccccc"))
  ],
)

#counter(page).update(1)
'''
        
        with open(main_file, 'w') as f:
            f.write(content)
    
    def _create_section_stub(self, section: Dict):
        """Create a stub file for a section."""
        section_file = self.sections_dir / f'{section["id"]}.typ'
        
        content = f'''// {section["title"]}
// Pages: {section.get("pages", "TBD")}

#import "../whitepaper_functions.typ": callout, evidence, metric

= {section["title"]}

#callout(type: "note", title: "Section Status", [
  *Status:* Stub - To be written
  
  *Expected pages:* {section.get("pages", "TBD")}
])

// TODO: Write full section content
'''
        
        with open(section_file, 'w') as f:
            f.write(content)
    
    def compile_section(self, section_id: str) -> bool:
        """Compile a single section to PDF."""
        print(f"📄 Compiling section: {section_id}")
        
        section_file = self.sections_dir / f"{section_id}.typ"
        if not section_file.exists():
            print(f"❌ Section file not found: {section_file}")
            return False
        
        # Create standalone wrapper
        wrapper_file = self.pdfs_dir / f"{section_id}_standalone.typ"
        output_file = self.pdfs_dir / f"{section_id}.pdf"
        
        wrapper_content = f'''// Standalone wrapper for {section_id}
#import "../whitepaper_functions.typ": callout, evidence, metric
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge

#set document(title: "{self.config['title']} - {section_id}")
#set page(
  paper: "us-letter",
  margin: (x: 1.25in, y: 1in),
  numbering: "1",
)

#set text(font: "{self.config['styling']['font_body']}", size: 11pt)
#set par(justify: true)
#set heading(numbering: "1.1")

#show raw.where(block: true): it => {{
  set text(font: "{self.config['styling']['font_code']}", size: 9pt)
  block(fill: rgb("#f5f5f5"), stroke: 1pt + rgb("#cccccc"), radius: 4pt, inset: 12pt, width: 100%, it)
}}

#include "../sections/{section_id}.typ"
'''
        
        with open(wrapper_file, 'w') as f:
            f.write(wrapper_content)
        
        # Compile with typst
        try:
            result = subprocess.run(
                ["typst", "compile", str(wrapper_file), str(output_file)],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=60,
            )
            
            if result.returncode == 0:
                print(f"✅ Compiled: {output_file}")
                print(f"   Open with: open {output_file}")
                return True
            else:
                print(f"❌ Compilation failed:")
                print(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Compilation timed out")
            return False
        except FileNotFoundError:
            print("❌ Typst not found. Install with: brew install typst")
            return False
    
    def compile_all(self) -> bool:
        """Compile the complete whitepaper."""
        print(f"📚 Compiling complete whitepaper: {self.config['title']}")
        
        main_file = self.project_dir / "MAIN.typ"
        output_file = self.project_dir / f"{self.config['title'].replace(' ', '_')}_COMPLETE.pdf"
        
        try:
            result = subprocess.run(
                ["typst", "compile", str(main_file), str(output_file)],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=120,
            )
            
            if result.returncode == 0:
                print(f"✅ Complete whitepaper compiled: {output_file}")
                # Auto-open
                subprocess.run(["open", str(output_file)])
                return True
            else:
                print(f"❌ Compilation failed:")
                print(result.stderr[-2000:])  # Last 2000 chars
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Compilation timed out")
            return False
        except FileNotFoundError:
            print("❌ Typst not found. Install with: brew install typst")
            return False
    
    def status(self):
        """Show project status."""
        print(f"\n📊 Project Status: {self.config['title']}")
        print(f"{'='*60}")
        print(f"Author: {self.config['author']}")
        print(f"Version: {self.config['version']}")
        print(f"Date: {self.config['date']}")
        print(f"\n📁 Sections ({len(self.config['sections'])}):")
        
        total_pages = 0
        written = 0
        
        for section in self.config['sections']:
            section_file = self.sections_dir / f"{section['id']}.typ"
            pdf_file = self.pdfs_dir / f"{section['id']}.pdf"
            
            if section_file.exists():
                size = section_file.stat().st_size
                status = "✅ Written" if size > 500 else "📝 Stub"
                written += 1 if size > 500 else 0
            else:
                status = "❌ Missing"
            
            pdf_status = "📄" if pdf_file.exists() else "  "
            
            pages = section.get('pages', 0)
            total_pages += pages
            
            print(f"  {pdf_status} {status:12} | {section['id']:25} | {pages:2}p | {section['title']}")
        
        print(f"\n{'='*60}")
        print(f"Progress: {written}/{len(self.config['sections'])} sections written")
        print(f"Estimated pages: {total_pages}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    # Get project directory (current directory)
    project_dir = Path.cwd()
    
    if command == "init":
        if len(sys.argv) < 3:
            print("Usage: whitepaper_generator.py init <project-name>")
            sys.exit(1)
        
        project_name = sys.argv[2]
        # Don't instantiate generator until after init
        generator = WhitepaperGenerator.__new__(WhitepaperGenerator)
        generator.project_dir = project_dir
        generator.config_file = project_dir / "whitepaper_config.yaml"
        generator.sections_dir = project_dir / "sections"
        generator.pdfs_dir = project_dir / "section_pdfs"
        generator.template_dir = project_dir / "typst_template"
        generator.config = None
        generator.init_project(project_name)
        generator.config = generator.load_config()  # Load after creation
    
    elif command == "compile-section":
        if len(sys.argv) < 3:
            print("Usage: whitepaper_generator.py compile-section <section-id>")
            sys.exit(1)
        
        section_id = sys.argv[2]
        generator = WhitepaperGenerator(project_dir)
        generator.compile_section(section_id)
    
    elif command == "compile-all":
        generator = WhitepaperGenerator(project_dir)
        generator.compile_all()
    
    elif command == "status":
        generator = WhitepaperGenerator(project_dir)
        generator.status()
    
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
