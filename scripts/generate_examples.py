#!/usr/bin/env python3
"""
Generate Example Outputs: PDFs, HTML, Examples

Creates tangible outputs the user can actually see and use.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from rich.console import Console
from rich.panel import Panel

console = Console()

def generate_pdf_examples():
    """Generate PDF examples from templates."""
    console.print("\n[bold cyan]📄 Generating PDF Examples...[/bold cyan]\n")
    
    output_dir = project_root / "_examples_output"
    output_dir.mkdir(exist_ok=True)
    
    # 1. Unicamp Report PDF
    try:
        from src.waft.templates.latex.wrappers.unicamp_report import generate_unicamp_report
        
        pdf_path = generate_unicamp_report(
            title="Relatório I",
            content="# Introdução\n\nEste é um exemplo de relatório gerado automaticamente pelo sistema WAFT.",
            output_path=output_dir / "unicamp_report_example.pdf",
            professor="Prof. Dr. Flávio Caldas da Cruz",
            authors=[
                "Caroline Guimarães 155006",
                "Lucas Rodrigues Contador 156406",
                "Giovanne Lucas Dias Pereira Mariano 173317"
            ],
            course="Física Experimental IV",
            abstract="Este relatório demonstra a integração do template Unicamp com o sistema WAFT. O template foi integrado usando o LaTeXTemplateRegistry e catalogado com o Librarian.",
            introduction="Este relatório apresenta um exemplo de uso do template LaTeX da Unicamp. O template foi integrado ao sistema WAFT e pode ser usado para gerar relatórios acadêmicos em português brasileiro.",
            methodology="A metodologia utilizada foi a integração do template através de um wrapper Python que utiliza Jinja2 para preencher variáveis no template LaTeX.",
            results="Os resultados mostram que o template foi integrado com sucesso e pode gerar PDFs corretamente.",
            discussion="A discussão dos resultados indica que o sistema está funcionando conforme esperado.",
            conclusion="Concluímos que a integração foi bem-sucedida e o template está pronto para uso."
        )
        console.print(f"✅ [green]PDF gerado:[/green] {pdf_path}")
    except Exception as e:
        console.print(f"❌ [red]Erro ao gerar PDF Unicamp:[/red] {e}")
    
    # 2. Newsletter PDF (from improved template)
    try:
        from src.waft.templates.latex.compiler import LaTeXCompiler
        
        newsletter_tex = project_root / "_work_efforts" / "WE-260116-7e6g_latex_newsletter_template_improvements" / "newsletter_template_improved.tex"
        if newsletter_tex.exists():
            compiler = LaTeXCompiler(compiler="pdflatex")
            pdf_path = compiler.compile_file(
                newsletter_tex,
                output_dir / "newsletter_example.pdf",
                runs=2
            )
            console.print(f"✅ [green]PDF gerado:[/green] {pdf_path}")
    except Exception as e:
        console.print(f"⚠️  [yellow]Newsletter PDF:[/yellow] {e}")

def generate_html_dashboard():
    """Generate HTML dashboard showing current state."""
    console.print("\n[bold cyan]🌐 Generating HTML Dashboard...[/bold cyan]\n")
    
    output_dir = project_root / "_examples_output"
    output_dir.mkdir(exist_ok=True)
    
    try:
        from src.waft.templates.latex.registry import get_latex_registry
        from src.waft.pantheon.library.librarian import Librarian
        
        # Get data
        registry = get_latex_registry()
        templates = registry.list_templates()
        
        librarian = Librarian(project_path=project_root)
        catalog_summary = librarian.generate_summary()
        
        # Get work efforts
        work_efforts = []
        we_dir = project_root / "_work_efforts"
        if we_dir.exists():
            today_pattern = datetime.now().strftime("%y%m%d")
            for item in we_dir.iterdir():
                if item.is_dir() and item.name.startswith("WE-") and today_pattern in item.name:
                    index_file = item / f"{item.name}_index.md"
                    if index_file.exists():
                        content = index_file.read_text()
                        title = item.name
                        if "title:" in content:
                            for line in content.split("\n"):
                                if line.startswith("title:"):
                                    title = line.split(":", 1)[1].strip().strip('"')
                                    break
                        status = "active"
                        if "status: completed" in content.lower():
                            status = "completed"
                        work_efforts.append({"id": item.name, "title": title, "status": status})
        
        # Generate HTML
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WAFT Session Dashboard - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            color: #666;
            font-size: 1.1em;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .card h2 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .template-item, .work-effort-item {{
            padding: 12px;
            margin: 8px 0;
            background: #f8f9fa;
            border-radius: 6px;
            border-left: 4px solid #667eea;
        }}
        
        .template-item strong {{
            color: #667eea;
        }}
        
        .work-effort-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .status {{
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: bold;
        }}
        
        .status.completed {{
            background: #d4edda;
            color: #155724;
        }}
        
        .status.active {{
            background: #d1ecf1;
            color: #0c5460;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        
        .stat {{
            text-align: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: white;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 WAFT Session Dashboard</h1>
            <div class="subtitle">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
        
        <div class="grid">
            <!-- Templates Card -->
            <div class="card">
                <h2>📄 LaTeX Templates</h2>
                <div class="stats">
                    <div class="stat">
                        <div class="stat-value">{len(templates)}</div>
                        <div class="stat-label">Templates</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">{len(set(t.category for t in templates))}</div>
                        <div class="stat-label">Categories</div>
                    </div>
                </div>
                <div style="max-height: 400px; overflow-y: auto; margin-top: 20px;">
                    {"".join(f'''
                    <div class="template-item">
                        <strong>{t.name}</strong><br>
                        <small>Category: {t.category} | Tags: {", ".join(t.tags[:3])}</small>
                    </div>
                    ''' for t in templates[:10])}
                </div>
            </div>
            
            <!-- Work Efforts Card -->
            <div class="card">
                <h2>📋 Work Efforts (Today)</h2>
                <div class="stats">
                    <div class="stat">
                        <div class="stat-value">{len(work_efforts)}</div>
                        <div class="stat-label">Today</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">{sum(1 for w in work_efforts if w['status'] == 'completed')}</div>
                        <div class="stat-label">Completed</div>
                    </div>
                </div>
                <div style="max-height: 400px; overflow-y: auto; margin-top: 20px;">
                    {"".join(f'''
                    <div class="work-effort-item">
                        <div>
                            <strong>{w['title']}</strong><br>
                            <small>{w['id']}</small>
                        </div>
                        <span class="status {w['status']}">{w['status']}</span>
                    </div>
                    ''' for w in work_efforts[:10]) if work_efforts else '<p style="color: #666;">No work efforts from today</p>'}
                </div>
            </div>
            
            <!-- Catalog Card -->
            <div class="card">
                <h2>📚 Librarian Catalog</h2>
                <div class="stats">
                    <div class="stat">
                        <div class="stat-value">{catalog_summary.get('total_records', 0)}</div>
                        <div class="stat-label">Records</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">{len(catalog_summary.get('by_type', {}))}</div>
                        <div class="stat-label">Types</div>
                    </div>
                </div>
                <div style="margin-top: 20px;">
                    <h3 style="font-size: 1.1em; margin-bottom: 10px; color: #666;">By Type:</h3>
                    {"".join(f'<div class="template-item"><strong>{k}:</strong> {v}</div>' for k, v in catalog_summary.get('by_type', {}).items())}
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>WAFT Framework - Session Dashboard</p>
            <p>Generated automatically from current system state</p>
        </div>
    </div>
</body>
</html>
"""
        
        html_path = output_dir / "dashboard.html"
        html_path.write_text(html_content, encoding="utf-8")
        console.print(f"✅ [green]HTML Dashboard gerado:[/green] {html_path}")
        console.print(f"   [dim]Abra no navegador: file://{html_path.absolute()}[/dim]")
        
    except Exception as e:
        console.print(f"❌ [red]Erro ao gerar HTML:[/red] {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main entry point."""
    console.print(Panel.fit(
        "[bold cyan]🎨 Gerando Exemplos Visuais[/bold cyan]\n\n"
        "Criando PDFs, HTML e exemplos que você pode ver e usar!",
        border_style="cyan"
    ))
    
    # Generate PDFs
    generate_pdf_examples()
    
    # Generate HTML
    generate_html_dashboard()
    
    output_dir = project_root / "_examples_output"
    console.print(f"\n[bold green]✅ Exemplos gerados em:[/bold green] {output_dir.absolute()}")
    console.print(f"\n[bold]Arquivos criados:[/bold]")
    for file in sorted(output_dir.glob("*")):
        if file.is_file():
            size = file.stat().st_size / 1024  # KB
            console.print(f"  📄 {file.name} ({size:.1f} KB)")

if __name__ == "__main__":
    main()
