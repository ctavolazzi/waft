#!/usr/bin/env python3
"""
Evolve Research Simulation UI using WAFT Evolution System

Uses WAFT's component evolution and styling genome system to evolve
the web interface design through multiple generations.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.waft.evolution.document_evolution_engine import DocumentEvolutionEngine


def evolve_ui_design() -> dict[str, Any]:
    """Evolve UI design using WAFT evolution system."""

    print("🧬 Evolving UI Design with WAFT Evolution System...")

    # Initialize evolution engine
    evolution_engine = DocumentEvolutionEngine(
        project_path=project_root,
        weasyprint_available=True,
        max_iterations=5,
        default_allowed_pages=2,
        evolution_dir=project_root / "_genetics" / "ui_evolution",
        exploration_rate=0.3,  # 30% exploration
    )

    # UI design requirements as content
    ui_requirements = """
# Research Simulation UI Design Requirements

## Core Components

### 1. Header Section
- Title: "Research Simulation"
- Subtitle: "Demo Batching System - Interactive Research Platform"
- Visual: Clean, professional, scientific aesthetic

### 2. Input Form
- Permutations field (number input)
- Max Pages field (optional number input)
- Max File Size field (optional number input)
- Start button (prominent, clear call-to-action)

### 3. Status Display
- Ready state (initial)
- Running state (with loading indicator)
- Complete state (with success message and report link)
- Error state (with error message)

### 4. Visual Design Principles
- Modern, clean aesthetic
- Scientific/research theme
- High contrast for readability
- Responsive design
- Smooth transitions
- Professional color scheme

### 5. User Experience
- Clear visual feedback
- Real-time status updates
- Intuitive form layout
- Accessible design
- Fast loading
- Mobile-friendly
"""

    # Generate evolved design using WAFT
    print("  📐 Generating evolved UI design...")

    result = evolution_engine.generate_one_pager(
        content=ui_requirements,
        title="Research Simulation UI - Evolved Design",
        allowed_pages=2,
        use_science_paper_structure=True,
        use_evolved_components=True,
        author="WAFT Evolution Engine",
    )

    print("  ✅ Generated evolved design")
    print(f"  📊 Fitness: {result.get('fitness', 'N/A')}")
    print(f"  📄 Pages: {result.get('page_count', 'N/A')}")

    # Extract design insights from evolved components
    design_insights = extract_design_insights(result)

    # Generate evolved HTML/CSS based on insights
    evolved_html = generate_evolved_html(design_insights)

    return {
        "evolved_design": result,
        "design_insights": design_insights,
        "evolved_html": evolved_html,
        "timestamp": datetime.now().isoformat(),
    }


def extract_design_insights(evolution_result: dict[str, Any]) -> dict[str, Any]:
    """Extract design insights from evolution result."""

    # Get fitness to determine evolution level
    fitness = evolution_result.get("fitness", {})
    if isinstance(fitness, dict):
        overall_fitness = fitness.get("overall", 0.7)
    else:
        overall_fitness = fitness if isinstance(fitness, (int, float)) else 0.7

    # Evolve colors based on fitness - higher fitness = more sophisticated palette
    if overall_fitness > 0.85:
        primary = "#6366f1"  # Indigo
        secondary = "#8b5cf6"  # Purple
        accent = "#ec4899"  # Pink accent
    elif overall_fitness > 0.75:
        primary = "#667eea"  # Purple-blue
        secondary = "#764ba2"  # Purple
        accent = "#f093fb"  # Light pink
    else:
        primary = "#667eea"  # Default purple
        secondary = "#764ba2"  # Default purple
        accent = "#f093fb"  # Default accent

    insights = {
        "color_scheme": {
            "primary": primary,
            "secondary": secondary,
            "accent": accent,
            "success": "#10b981",  # Emerald green
            "warning": "#f59e0b",  # Amber
            "error": "#ef4444",  # Red
            "background": "#f8fafc",  # Slate-50
            "text": "#1e293b",  # Slate-800
            "text_light": "#64748b",  # Slate-500
        },
        "typography": {
            "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            "heading_size": "32px",
            "body_size": "16px",
            "line_height": "1.6",
        },
        "spacing": {
            "container_padding": "40px",
            "form_group_margin": "20px",
            "button_padding": "16px",
            "border_radius": "12px",
        },
        "components": {
            "header": {"style": "gradient_background", "height": "auto", "padding": "40px"},
            "form": {
                "layout": "vertical",
                "input_style": "modern_bordered",
                "button_style": "gradient_prominent",
            },
            "status": {"style": "card_based", "animation": "smooth_transitions", "icons": True},
        },
        "animations": {
            "button_hover": "lift_effect",
            "status_change": "fade_in",
            "loading": "spinner",
        },
    }

    # Enhance based on evolution fitness
    fitness = evolution_result.get("fitness", {})
    if isinstance(fitness, dict):
        overall_fitness = fitness.get("overall", 0)
    else:
        overall_fitness = fitness if isinstance(fitness, (int, float)) else 0

    if overall_fitness > 0.8:
        insights["components"]["form"]["input_style"] = "enhanced_focus"
        insights["animations"]["button_hover"] = "enhanced_lift"

    return insights


def generate_evolved_html(design_insights: dict[str, Any]) -> str:
    """Generate evolved HTML/CSS based on design insights."""

    colors = design_insights["color_scheme"]
    typography = design_insights["typography"]
    spacing = design_insights["spacing"]
    components = design_insights["components"]
    animations = design_insights["animations"]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Simulation - Evolved UI</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: {typography["font_family"]};
            background: linear-gradient(135deg, {colors["primary"]} 0%, {colors["secondary"]} 100%);
            min-height: 100vh;
            padding: 20px;
            color: {colors["text"]};
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: {spacing["border_radius"]}px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, {colors["primary"]} 0%, {colors["secondary"]} 50%, {colors.get("accent", colors["secondary"])} 100%);
            color: white;
            padding: {components["header"]["padding"]};
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 8s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); opacity: 0.5; }}
            50% {{ transform: scale(1.1); opacity: 0.8; }}
        }}
        
        h1 {{
            font-size: {typography["heading_size"]};
            margin-bottom: 10px;
            font-weight: 700;
            position: relative;
            z-index: 1;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        
        .subtitle {{
            font-size: 18px;
            opacity: 0.95;
            margin-top: 8px;
            position: relative;
            z-index: 1;
        }}
        
        .refresh-button {{
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            background: rgba(255, 255, 255, 0.9);
            border: 2px solid {colors["primary"]};
            border-radius: 8px;
            color: {colors["primary"]};
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            z-index: 1000;
            font-size: 14px;
        }}
        
        .refresh-button:hover {{
            background: {colors["primary"]};
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(102, 126, 234, 0.3);
        }}
        
        .refresh-button:active {{
            transform: translateY(0);
        }}
        
        .content {{
            padding: {spacing["container_padding"]};
        }}
        
        .form-group {{
            margin-bottom: {spacing["form_group_margin"]};
        }}
        
        label {{
            display: block;
            margin-bottom: 8px;
            color: {colors["text"]};
            font-weight: 500;
            font-size: 15px;
        }}
        
        input[type="number"] {{
            width: 100%;
            padding: 14px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: {typography["body_size"]};
            transition: all 0.3s ease;
            font-family: {typography["font_family"]};
        }}
        
        input[type="number"]:focus {{
            outline: none;
            border-color: {colors["primary"]};
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            transform: translateY(-1px);
        }}
        
        .start-button {{
            width: 100%;
            padding: {spacing["button_padding"]};
            background: linear-gradient(135deg, {colors["primary"]} 0%, {colors["secondary"]} 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 25px;
            position: relative;
            overflow: hidden;
        }}
        
        .start-button::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }}
        
        .start-button:hover:not(:disabled)::before {{
            width: 300px;
            height: 300px;
        }}
        
        .start-button:hover:not(:disabled) {{
            transform: translateY(-3px);
            box-shadow: 0 12px 24px rgba(102, 126, 234, 0.4);
        }}
        
        .start-button:active:not(:disabled) {{
            transform: translateY(-1px);
        }}
        
        .start-button:disabled {{
            opacity: 0.7;
            cursor: not-allowed;
            transform: none;
        }}
        
        .status {{
            margin-top: 30px;
            padding: 25px;
            border-radius: 8px;
            display: none;
            animation: fadeIn 0.5s ease;
        }}
        
        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: translateY(10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .status.ready {{
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            border: 2px solid {colors["success"]};
            color: #155724;
            display: block;
        }}
        
        .status.running {{
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            border: 2px solid {colors["warning"]};
            color: #856404;
            display: block;
        }}
        
        .status.error {{
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            border: 2px solid {colors["error"]};
            color: #721c24;
            display: block;
        }}
        
        .status-content {{
            font-size: 16px;
            line-height: {typography["line_height"]};
        }}
        
        .status-content strong {{
            font-size: 18px;
            display: block;
            margin-bottom: 12px;
        }}
        
        .report-link {{
            display: inline-block;
            margin-top: 15px;
            padding: 14px 28px;
            background: {colors["success"]};
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
        }}
        
        .report-link:hover {{
            background: #218838;
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(40, 167, 69, 0.4);
        }}
        
        .loading {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 1s ease-in-out infinite;
            margin-right: 10px;
            vertical-align: middle;
        }}
        
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        
        .metric-card {{
            background: rgba(255, 255, 255, 0.9);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}
        
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: {colors["primary"]};
        }}
        
        .metric-label {{
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                margin: 10px;
            }}
            
            .header {{
                padding: 30px 20px;
            }}
            
            h1 {{
                font-size: 28px;
            }}
            
            .content {{
                padding: 30px 20px;
            }}
        }}
    </style>
</head>
<body>
    <button class="refresh-button" onclick="window.location.reload()" title="Refresh to see latest UI evolution">
        🔄 Refresh UI
    </button>
    <div class="container">
        <div class="header">
            <h1>🔬 Research Simulation</h1>
            <p class="subtitle">Demo Batching System - Interactive Research Platform</p>
        </div>
        
        <div class="content">
            <form id="simulationForm">
                <div class="form-group">
                    <label for="permutations">Number of Permutations:</label>
                    <input type="number" id="permutations" name="permutations" value="10" min="1" max="100" required>
                </div>
                
                <div class="form-group">
                    <label for="maxPages">Max Pages (optional):</label>
                    <input type="number" id="maxPages" name="maxPages" min="1" placeholder="Leave empty for no limit">
                </div>
                
                <div class="form-group">
                    <label for="maxFileSize">Max File Size MB (optional):</label>
                    <input type="number" id="maxFileSize" name="maxFileSize" min="0.1" step="0.1" placeholder="Leave empty for no limit">
                </div>
                
                <button type="submit" class="start-button" id="startButton">
                    🚀 Start Simulation
                </button>
            </form>
            
            <div id="status" class="status"></div>
        </div>
    </div>
    
    <script>
        const form = document.getElementById('simulationForm');
        const startButton = document.getElementById('startButton');
        const statusDiv = document.getElementById('status');
        
        form.addEventListener('submit', async (e) => {{
            e.preventDefault();
            
            const formData = new FormData(form);
            const config = {{
                permutations: parseInt(formData.get('permutations')),
                max_pages: formData.get('maxPages') ? parseInt(formData.get('maxPages')) : null,
                max_file_size_mb: formData.get('maxFileSize') ? parseFloat(formData.get('maxFileSize')) : null,
                demo_path: 'research_simulation'
            }};
            
            // Update UI
            startButton.disabled = true;
            startButton.innerHTML = '<span class="loading"></span>Running Simulation...';
            statusDiv.className = 'status running';
            statusDiv.innerHTML = '<div class="status-content"><strong>🔄 Simulation Running</strong><br>Please wait while we collect data and analyze results...</div>';
            
            try {{
                const response = await fetch('/api/run-simulation', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify(config)
                }});
                
                if (!response.ok) {{
                    throw new Error('Simulation failed');
                }}
                
                const result = await response.json();
                
                // Show ready status with metrics
                statusDiv.className = 'status ready';
                let statusHTML = '<div class="status-content">';
                statusHTML += '<strong>✅ Simulation Complete!</strong><br><br>';
                statusHTML += '<div class="metrics-grid">';
                statusHTML += `<div class="metric-card"><div class="metric-value">${{result.metrics.total_permutations}}</div><div class="metric-label">Permutations</div></div>`;
                statusHTML += `<div class="metric-card"><div class="metric-value">${{result.metrics.total_souls}}</div><div class="metric-label">Total Souls</div></div>`;
                statusHTML += `<div class="metric-card"><div class="metric-value">${{result.metrics.pdf_size_mb.toFixed(4)}}</div><div class="metric-label">PDF Size (MB)</div></div>`;
                statusHTML += `<div class="metric-card"><div class="metric-value">${{result.metrics.generation_time_seconds}}</div><div class="metric-label">Time (s)</div></div>`;
                statusHTML += '</div>';
                statusHTML += '<br><a href="/api/report" class="report-link" target="_blank">📄 View Research Report</a>';
                statusHTML += '</div>';
                statusDiv.innerHTML = statusHTML;
                
            }} catch (error) {{
                statusDiv.className = 'status error';
                statusDiv.innerHTML = `<div class="status-content"><strong>❌ Error</strong><br>${{error.message}}</div>`;
            }} finally {{
                startButton.disabled = false;
                startButton.innerHTML = '🚀 Start Simulation';
            }}
        }});
        
        // Poll for status on page load
        async function checkStatus() {{
            try {{
                const response = await fetch('/api/status');
                const status = await response.json();
                
                if (status.status === 'complete' && status.report) {{
                    statusDiv.className = 'status ready';
                    let statusHTML = '<div class="status-content">';
                    statusHTML += '<strong>✅ Research Complete!</strong><br><br>';
                    statusHTML += '<a href="/api/report" class="report-link" target="_blank">📄 View Research Report</a>';
                    statusHTML += '</div>';
                    statusDiv.innerHTML = statusHTML;
                }}
            }} catch (error) {{
                // Ignore errors on status check
            }}
        }}
        
        checkStatus();
    </script>
</body>
</html>
"""

    return html


def save_evolved_ui(evolved_html: str, output_path: Path):
    """Save evolved UI to file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(evolved_html, encoding="utf-8")
    print(f"  ✅ Saved evolved UI to: {output_path}")


def main():
    """Main function to evolve UI."""
    print("🧬 WAFT UI Evolution System")
    print("=" * 50)

    # Evolve UI design
    evolution_result = evolve_ui_design()

    # Save evolved HTML
    output_path = project_root / "scripts" / "evolved_ui.html"
    save_evolved_ui(evolution_result["evolved_html"], output_path)

    # Update the server to use evolved UI
    update_server_with_evolved_ui(evolution_result["evolved_html"])

    print("\n✅ UI Evolution Complete!")
    print(f"📄 Evolved UI saved to: {output_path}")
    print("🔄 Server updated with evolved UI")
    print("\n🚀 Restart the server to see the evolved UI!")


def update_server_with_evolved_ui(evolved_html: str):
    """Update research_simulation_server.py with evolved UI."""
    server_path = project_root / "scripts" / "research_simulation_server.py"

    # Read current server file
    server_content = server_path.read_text(encoding="utf-8")

    # Find the HTML content section
    start_marker = 'html_content = """'
    end_marker = '"""'

    start_idx = server_content.find(start_marker)
    if start_idx == -1:
        print("  ⚠️  Could not find HTML content marker")
        return

    # Find the end of the HTML string
    html_start = start_idx + len(start_marker)
    html_end = server_content.find(end_marker, html_start)

    if html_end == -1:
        print("  ⚠️  Could not find end of HTML content")
        return

    # Replace HTML content
    new_content = server_content[:html_start] + evolved_html + server_content[html_end:]

    # Write back
    server_path.write_text(new_content, encoding="utf-8")
    print("  ✅ Updated server with evolved UI")


if __name__ == "__main__":
    main()
