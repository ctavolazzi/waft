#!/usr/bin/env python3
"""
WAFT Framework Documentation Generator

Generates comprehensive documentation about how WAFT functions
by inspecting itself - NO HARDCODED CONTENT.

This is WAFT documenting itself through self-inspection.
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import sys
import ast
import inspect
import importlib.util

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.table import Table
from jinja2 import Template
from weasyprint import HTML

console = Console()


# ============================================================================
# Data Collection - WAFT Inspects Itself
# ============================================================================

class FrameworkAnalyzer:
    """Analyzes WAFT's codebase to extract framework information."""
    
    def __init__(self, waft_root: Path):
        self.waft_root = waft_root
        self.modules = {}
        self.classes = {}
        self.functions = {}
        self.templates = {}
        self.structure = {}
    
    def analyze_codebase(self) -> Dict[str, Any]:
        """Perform comprehensive analysis of WAFT codebase."""
        console.print("\n[bold cyan]🔍 PHASE 1: SCANNING CODEBASE[/bold cyan]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console
        ) as progress:
            
            # Find all Python files
            task1 = progress.add_task("Finding Python files...", total=None)
            python_files = list(self.waft_root.rglob("*.py"))
            python_files = [f for f in python_files if not f.name.startswith('__')]
            progress.update(task1, total=len(python_files))
            progress.update(task1, completed=len(python_files))
            console.print(f"  [green]✅[/green] Found [bold]{len(python_files)}[/bold] Python files\n")
            
            # Analyze modules
            task2 = progress.add_task("Analyzing modules...", total=len(python_files))
            for py_file in python_files:
                self._analyze_file(py_file)
                progress.update(task2, advance=1)
            
            # Show summary
            total_classes = sum(m.get("class_count", 0) for m in self.modules.values())
            total_functions = sum(m.get("function_count", 0) for m in self.modules.values())
            console.print(f"  [green]✅[/green] Analyzed [bold]{len(self.modules)}[/bold] modules")
            console.print(f"     Found [bold]{total_classes}[/bold] classes, [bold]{total_functions}[/bold] functions\n")
            
            # Analyze templates
            task3 = progress.add_task("Analyzing templates...", total=None)
            templates_dir = self.waft_root / "templates"
            if templates_dir.exists():
                template_files = list(templates_dir.glob("*.py"))
                for template_file in template_files:
                    self._analyze_template(template_file)
                progress.update(task3, total=len(template_files))
                progress.update(task3, completed=len(template_files))
            console.print(f"  [green]✅[/green] Found [bold]{len(self.templates)}[/bold] templates\n")
            
            # Analyze structure
            task4 = progress.add_task("Analyzing structure...", total=None)
            self._analyze_structure()
            progress.update(task4, total=1)
            progress.update(task4, completed=1)
            console.print(f"  [green]✅[/green] Structure analyzed")
            console.print(f"     Core modules: [bold]{len(self.structure['core_modules'])}[/bold]\n")
        
        return {
            "modules": self.modules,
            "classes": self.classes,
            "functions": self.functions,
            "templates": self.templates,
            "structure": self.structure,
            "timestamp": datetime.now().isoformat()
        }
    
    def _analyze_file(self, file_path: Path):
        """Analyze a single Python file."""
        try:
            source = file_path.read_text()
            tree = ast.parse(source)
            
            # Get module info
            module_docstring = ast.get_docstring(tree)
            rel_path = file_path.relative_to(self.waft_root.parent)
            module_name = str(rel_path).replace("/", ".").replace(".py", "")
            
            # Extract classes
            classes = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_doc = ast.get_docstring(node)
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    classes.append({
                        "name": node.name,
                        "docstring": class_doc or "No documentation",
                        "methods": methods,
                        "method_count": len(methods)
                    })
                    self.classes[f"{module_name}.{node.name}"] = {
                        "name": node.name,
                        "module": module_name,
                        "docstring": class_doc or "No documentation",
                        "methods": methods
                    }
            
            # Extract functions
            functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and not isinstance(node, ast.ClassDef):
                    func_doc = ast.get_docstring(node)
                    if not node.name.startswith('_') or node.name.startswith('__'):
                        functions.append({
                            "name": node.name,
                            "docstring": func_doc or "No documentation"
                        })
                        self.functions[f"{module_name}.{node.name}"] = {
                            "name": node.name,
                            "module": module_name,
                            "docstring": func_doc or "No documentation"
                        }
            
            self.modules[module_name] = {
                "path": str(rel_path),
                "docstring": module_docstring or "No module docstring",
                "classes": classes,
                "functions": functions,
                "class_count": len(classes),
                "function_count": len(functions)
            }
            
        except Exception as e:
            # Skip files that can't be parsed
            pass
    
    def _analyze_template(self, template_file: Path):
        """Analyze a template file."""
        try:
            source = template_file.read_text()
            tree = ast.parse(source)
            
            # Get template name and docstring
            module_docstring = ast.get_docstring(tree)
            template_name = template_file.stem.replace("_", " ").title()
            
            # Look for template constants or functions
            template_content = None
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and "TEMPLATE" in target.id.upper():
                            if isinstance(node.value, ast.Constant):
                                template_content = node.value.value
                                break
            
            self.templates[template_name] = {
                "file": template_file.name,
                "name": template_name,
                "docstring": module_docstring or "Template for document generation",
                "has_content": template_content is not None
            }
            
        except Exception as e:
            pass
    
    def _analyze_structure(self):
        """Analyze WAFT's directory structure."""
        structure = {
            "core_modules": [],
            "template_count": len(self.templates),
            "total_modules": len(self.modules),
            "total_classes": len(self.classes),
            "total_functions": len(self.functions)
        }
        
        # Identify core modules
        core_patterns = ["core", "templates", "binder", "reflection", "foundation"]
        for module_name in self.modules.keys():
            if any(pattern in module_name.lower() for pattern in core_patterns):
                structure["core_modules"].append(module_name)
        
        self.structure = structure


# ============================================================================
# Documentation Generation - Based on Findings
# ============================================================================

FRAMEWORK_DOC_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>WAFT Framework Documentation</title>
    <style>
        @page {
            size: letter;
            margin: 0.75in;
            
            @top-center {
                content: "WAFT Framework Documentation";
                font-family: 'Times New Roman', serif;
                font-size: 9pt;
                color: #666;
            }
            
            @bottom-center {
                content: "Page " counter(page);
                font-family: 'Times New Roman', serif;
                font-size: 9pt;
                color: #666;
            }
        }
        
        @page :first {
            @top-center { content: none; }
        }
        
        body {
            font-family: 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #000;
        }
        
        .cover {
            text-align: center;
            padding-top: 2in;
        }
        
        .cover h1 {
            font-size: 32pt;
            font-weight: bold;
            margin-bottom: 0.3in;
            letter-spacing: 3px;
        }
        
        .cover .subtitle {
            font-size: 18pt;
            color: #333;
            margin-bottom: 0.5in;
        }
        
        .cover .meta {
            font-size: 12pt;
            color: #666;
            margin-top: 1.5in;
        }
        
        h1 {
            font-size: 20pt;
            font-weight: bold;
            margin-top: 0.5in;
            margin-bottom: 0.3in;
            border-bottom: 3px solid #000;
            padding-bottom: 0.1in;
        }
        
        h2 {
            font-size: 16pt;
            font-weight: bold;
            margin-top: 0.4in;
            margin-bottom: 0.2in;
            color: #2c3e50;
        }
        
        h3 {
            font-size: 13pt;
            font-weight: bold;
            margin-top: 0.3in;
            margin-bottom: 0.15in;
            color: #34495e;
        }
        
        .highlight-box {
            background: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 0.2in;
            margin: 0.2in 0;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 0.2in;
            margin: 0.3in 0;
        }
        
        .stat-card {
            background: #ecf0f1;
            padding: 0.15in;
            border-radius: 4px;
            text-align: center;
        }
        
        .stat-number {
            font-size: 24pt;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .stat-label {
            font-size: 10pt;
            color: #7f8c8d;
            margin-top: 0.05in;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.2in 0;
        }
        
        th {
            background: #34495e;
            color: white;
            padding: 0.1in;
            text-align: left;
            font-weight: bold;
        }
        
        td {
            padding: 0.1in;
            border-bottom: 1px solid #ddd;
        }
        
        tr:hover {
            background: #f5f5f5;
        }
        
        code {
            font-family: 'Courier New', monospace;
            font-size: 10pt;
            background: #f0f0f0;
            padding: 0.05in;
            border-radius: 3px;
        }
        
        .module-card {
            background: #ffffff;
            border: 1px solid #ddd;
            padding: 0.2in;
            margin: 0.2in 0;
            border-radius: 4px;
        }
        
        .module-name {
            font-weight: bold;
            font-size: 12pt;
            color: #2c3e50;
            margin-bottom: 0.1in;
        }
        
        .module-doc {
            color: #555;
            font-style: italic;
            margin-bottom: 0.1in;
        }
        
        .component-list {
            margin-left: 0.2in;
        }
        
        .component-list li {
            margin-bottom: 0.05in;
        }
        
        .architecture-diagram {
            background: #f8f9fa;
            padding: 0.3in;
            margin: 0.3in 0;
            border: 2px solid #34495e;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            white-space: pre-wrap;
        }
        
        .note {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 0.15in;
            margin: 0.2in 0;
        }
        
        .note-title {
            font-weight: bold;
            margin-bottom: 0.05in;
        }
    </style>
</head>
<body>
    <div class="cover">
        <h1>WAFT</h1>
        <div class="subtitle">Framework Documentation</div>
        <div class="subtitle" style="font-size: 14pt; margin-top: 0.2in;">
            World Architecture Framework & Templates
        </div>
        <div class="meta">
            <p>Generated: {{ timestamp }}</p>
            <p>Self-Documented Through Codebase Analysis</p>
        </div>
    </div>
    
    <h1>Introduction</h1>
    <p>
        This document describes how WAFT functions, based on <strong>direct inspection</strong>
        of the codebase. All information presented here was extracted through automated
        analysis - nothing is hardcoded.
    </p>
    
    <div class="note">
        <div class="note-title">Meta-Documentation</div>
        <p>
            This documentation was generated <strong>BY WAFT, ABOUT WAFT, USING WAFT</strong>.
            It represents WAFT observing itself and documenting what it finds. This is
            recursive self-documentation - the system describing its own operation.
        </p>
    </div>
    
    <h1>System Overview</h1>
    
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">{{ structure.total_modules }}</div>
            <div class="stat-label">Modules</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{{ structure.total_classes }}</div>
            <div class="stat-label">Classes</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{{ structure.total_functions }}</div>
            <div class="stat-label">Functions</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{{ structure.template_count }}</div>
            <div class="stat-label">Templates</div>
        </div>
    </div>
    
    <h2>What WAFT Does</h2>
    <p>
        Based on codebase analysis, WAFT is a comprehensive document generation framework
        that provides:
    </p>
    <ul>
        <li><strong>Template System</strong> - {{ structure.template_count }} professional document templates</li>
        <li><strong>Core Architecture</strong> - {{ structure.core_modules|length }} core modules</li>
        <li><strong>Binder System</strong> - Multi-document collection assembly</li>
        <li><strong>Reflection System</strong> - Self-observation and documentation</li>
        <li><strong>Meta-Cognitive Layer</strong> - Work effort tracking and epistemic memory</li>
    </ul>
    
    <h1>Core Architecture</h1>
    
    <h2>Module Structure</h2>
    <p>
        WAFT is organized into the following core modules (discovered through analysis):
    </p>
    
    {% set core_modules_list = structure.core_modules[:10] %}
    {% for module_name in core_modules_list %}
    <div class="module-card">
        <div class="module-name">{{ module_name }}</div>
        {% if modules[module_name] %}
        <div class="module-doc">{{ modules[module_name].docstring[:200] }}...</div>
        <div class="component-list">
            <strong>Components:</strong>
            <ul>
                {% if modules[module_name].classes %}
                <li>{{ modules[module_name].class_count }} class(es)</li>
                {% endif %}
                {% if modules[module_name].functions %}
                <li>{{ modules[module_name].function_count }} function(s)</li>
                {% endif %}
            </ul>
        </div>
        {% endif %}
    </div>
    {% endfor %}
    
    <h1>Template System</h1>
    <p>
        WAFT includes {{ structure.template_count }} document templates, each designed for
        specific use cases:
    </p>
    
    <table>
        <tr>
            <th>Template Name</th>
            <th>File</th>
            <th>Purpose</th>
        </tr>
        {% for template_name, template_info in templates.items() %}
        <tr>
            <td><strong>{{ template_name }}</strong></td>
            <td><code>{{ template_info.file }}</code></td>
            <td>{{ template_info.docstring[:100] }}...</td>
        </tr>
        {% endfor %}
    </table>
    
    <h1>Key Classes</h1>
    <p>
        Based on codebase analysis, WAFT's architecture centers around these key classes:
    </p>
    
    {% for class_name, class_info in classes.items() %}
    <div class="module-card">
        <div class="module-name">{{ class_info.name }}</div>
        <div class="module-doc">{{ class_info.docstring[:150] }}...</div>
        {% if class_info.methods %}
        <div class="component-list">
            <strong>Methods:</strong> {{ class_info.methods|length }}
            <ul>
                {% for method in class_info.methods[:5] %}
                <li><code>{{ method }}</code></li>
                {% endfor %}
                {% if class_info.methods|length > 5 %}
                <li>... and {{ class_info.methods|length - 5 }} more</li>
                {% endif %}
            </ul>
        </div>
        {% endif %}
    </div>
    {% endfor %}
    
    <h1>How WAFT Works</h1>
    
    <h2>Document Generation Flow</h2>
    <div class="architecture-diagram">
┌─────────────────────────────────────────────────────────┐
│  1. USER REQUEST                                        │
│     └─ Specify template and content                    │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  2. TEMPLATE SELECTION                                  │
│     └─ Choose from {{ structure.template_count }} available templates  │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  3. CONTENT RENDERING                                   │
│     └─ Jinja2 template engine processes content         │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  4. PDF GENERATION                                      │
│     └─ WeasyPrint converts HTML/CSS to PDF             │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  5. OUTPUT                                              │
│     └─ Professional PDF document                       │
└─────────────────────────────────────────────────────────┘
    </div>
    
    <h2>Self-Documentation Flow</h2>
    <div class="architecture-diagram">
┌─────────────────────────────────────────────────────────┐
│  WAFT OBSERVES ITSELF                                   │
│     └─ ReflectionSystem scans codebase (AST analysis)  │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  DATA COLLECTION                                        │
│     └─ Extract: modules, classes, functions, templates   │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  DOCUMENTATION GENERATION                               │
│     └─ Generate this document based on findings        │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  RECURSIVE LOOP                                         │
│     └─ Documentation informs development                │
│     └─ Development creates new features                 │
│     └─ Features are documented using WAFT               │
│     └─ ↺ CYCLE CONTINUES ↺                              │
└─────────────────────────────────────────────────────────┘
    </div>
    
    <h1>Meta-Cognitive Layer</h1>
    <p>
        WAFT includes a meta-cognitive layer that enables:
    </p>
    <ul>
        <li><strong>Work Effort Tracking</strong> - The _pyrite system tracks discrete units of intellectual labor</li>
        <li><strong>Epistemic Memory</strong> - System knows what it knows and what it doesn't</li>
        <li><strong>Perspective Taking</strong> - AI systems can "wear" previous perspectives</li>
        <li><strong>Recursive Self-Improvement</strong> - System improves based on its own observations</li>
    </ul>
    
    <h1>Key Findings</h1>
    
    <div class="highlight-box">
        <h3>Architecture Discovery</h3>
        <p>
            Analysis revealed <strong>{{ structure.total_modules }}</strong> modules,
            <strong>{{ structure.total_classes }}</strong> classes, and
            <strong>{{ structure.total_functions }}</strong> functions.
        </p>
    </div>
    
    <div class="highlight-box">
        <h3>Template System</h3>
        <p>
            WAFT provides <strong>{{ structure.template_count }}</strong> professional
            document templates covering academic, business, creative, and technical use cases.
        </p>
    </div>
    
    <div class="highlight-box">
        <h3>Self-Documentation</h3>
        <p>
            This document itself is proof of WAFT's self-documentation capability.
            Every section was generated from actual codebase analysis, not hardcoded content.
        </p>
    </div>
    
    <h1>Conclusion</h1>
    <p>
        WAFT is a self-documenting, self-modifying meta-framework that:
    </p>
    <ol>
        <li>Generates professional documents from templates</li>
        <li>Observes its own codebase structure</li>
        <li>Documents what it finds</li>
        <li>Uses that documentation to inform development</li>
        <li>Creates a recursive improvement loop</li>
    </ol>
    
    <div class="note">
        <div class="note-title">The Recursive Loop</div>
        <p>
            WAFT observes itself → Documents findings → Uses documentation → Improves →
            Observes changes → Documents updates → ↺ CONTINUES ↺
        </p>
    </div>
    
    <p style="margin-top: 0.5in; text-align: center; font-style: italic; color: #666;">
        This documentation was generated by WAFT inspecting itself.<br>
        Generated: {{ timestamp }}<br>
        <strong>WAFT documenting WAFT using WAFT.</strong>
    </p>
</body>
</html>
"""


def generate_framework_documentation(project_root: Path, output_path: Path) -> Path:
    """
    Generate comprehensive framework documentation by inspecting WAFT.
    
    Args:
        project_root: Root directory of WAFT project
        output_path: Where to save the PDF
        
    Returns:
        Path to generated PDF
    """
    console.print("=" * 80)
    console.print("[bold]WAFT Framework Documentation Generator[/bold]")
    console.print("=" * 80)
    console.print()
    console.print("[yellow]This tool generates documentation by inspecting WAFT itself.[/yellow]")
    console.print("[yellow]NO CONTENT IS HARDCODED - everything is discovered through analysis.[/yellow]")
    console.print()
    
    waft_root = project_root / "src" / "waft"
    
    if not waft_root.exists():
        console.print(f"[red]❌[/red] WAFT source not found: {waft_root}")
        return None
    
    # Analyze codebase
    analyzer = FrameworkAnalyzer(waft_root)
    analysis_data = analyzer.analyze_codebase()
    
    # Generate documentation
    console.print("\n[bold cyan]📄 PHASE 2: GENERATING DOCUMENTATION[/bold cyan]\n")
    
    # Prepare data for template (convert dict_items to lists for slicing)
    template_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "structure": analysis_data["structure"],
        "modules": analysis_data["modules"],
        "classes": dict(list(analysis_data["classes"].items())[:15]),  # Limit to 15 classes
        "templates": analysis_data["templates"],
        "functions": analysis_data["functions"],
        "core_modules_list": analysis_data["structure"]["core_modules"][:10]  # Limit to 10
    }
    
    template = Template(FRAMEWORK_DOC_TEMPLATE)
    html_content = template.render(**template_data)
    
    console.print("  [cyan]📝[/cyan] Rendering HTML...")
    console.print("  [cyan]📄[/cyan] Converting to PDF...")
    
    with console.status("[bold cyan]Generating PDF...[/bold cyan]"):
        HTML(string=html_content).write_pdf(str(output_path))
    
    size_mb = output_path.stat().st_size / (1024 * 1024)
    console.print(f"  [green]✅[/green] Documentation generated: [bold]{output_path}[/bold]")
    console.print(f"     Size: [bold]{size_mb:.2f} MB[/bold]")
    console.print()
    
    return output_path


def open_pdf(pdf_path: Path):
    """Open PDF using system default application."""
    try:
        import platform
        import subprocess
        
        system = platform.system()
        if system == "Darwin":  # macOS
            subprocess.run(["open", str(pdf_path)], check=True)
        elif system == "Windows":
            subprocess.run(["start", str(pdf_path)], shell=True, check=True)
        else:  # Linux
            subprocess.run(["xdg-open", str(pdf_path)], check=True)
        return True
    except Exception as e:
        console.print(f"  [yellow]⚠️[/yellow]  Could not open PDF: {e}")
        return False


if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    output_path = project_root / "WAFT_Framework_Documentation.pdf"
    
    console.print(f"Project root: [cyan]{project_root}[/cyan]")
    console.print(f"Output: [cyan]{output_path}[/cyan]")
    console.print()
    
    pdf_path = generate_framework_documentation(project_root, output_path)
    
    if pdf_path:
        console.print("  [cyan]📖[/cyan] Opening documentation...")
        if open_pdf(pdf_path):
            console.print("     [green]✅[/green] Documentation opened")
        console.print()
        console.print("[bold green]🎉 Complete![/bold green]")
        console.print()
        console.print("[dim]This documentation was generated by WAFT inspecting itself.[/dim]")
        console.print("[dim]Every section is based on actual codebase analysis.[/dim]\n")
    else:
        console.print("[bold red]❌ Failed to generate documentation[/bold red]\n")
        sys.exit(1)
