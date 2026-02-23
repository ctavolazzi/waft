#!/usr/bin/env python3
"""
Generate Miniatures Research PDF

Searches for information about miniatures, tabletop gaming, and robot assembly,
then generates a comprehensive PDF with the research data.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution.pdf_generator import PDFGenerator
from src.waft.pantheon.data_god import DataGod


def search_miniatures_data(data_god: DataGod) -> dict[str, any]:
    """Search for miniatures and tabletop gaming data."""
    print("🔍 Searching for miniatures and tabletop gaming data...")
    
    research_data = {
        "timestamp": None,
        "web_searches": [],
        "api_discoveries": [],
        "content": []
    }
    
    # Search for public APIs related to miniatures/gaming
    print("  - Searching public API directory...")
    try:
        gaming_apis = data_god.search_public_apis("game", category="Games & Comics")
        tabletop_apis = data_god.search_public_apis("tabletop")
        miniatures_apis = data_god.search_public_apis("miniature")
        
        research_data["api_discoveries"] = {
            "gaming_apis": gaming_apis[:10] if gaming_apis else [],
            "tabletop_apis": tabletop_apis[:10] if tabletop_apis else [],
            "miniatures_apis": miniatures_apis[:10] if miniatures_apis else [],
        }
        print(f"    Found {len(gaming_apis)} gaming APIs, {len(tabletop_apis)} tabletop APIs")
    except Exception as e:
        print(f"    ⚠️  API search error: {e}")
    
    # Web searches (if Brave API is configured)
    if data_god.brave_api_key:
        print("  - Searching the web (Brave Search)...")
        try:
            # Search for miniatures assembly
            miniatures_search = data_god.search_web(
                "tabletop gaming miniatures assembly techniques",
                count=10
            )
            if miniatures_search.get("success"):
                research_data["web_searches"].append({
                    "query": "tabletop gaming miniatures assembly techniques",
                    "results": miniatures_search.get("data", {})
                })
            
            # Search for robot arm assembly
            robot_search = data_god.search_web(
                "robot arm miniature assembly automation",
                count=10
            )
            if robot_search.get("success"):
                research_data["web_searches"].append({
                    "query": "robot arm miniature assembly automation",
                    "results": robot_search.get("data", {})
                })
            
            # Search for 3D printing miniatures
            printing_search = data_god.search_web(
                "3D printing tabletop miniatures quality",
                count=10
            )
            if printing_search.get("success"):
                research_data["web_searches"].append({
                    "query": "3D printing tabletop miniatures quality",
                    "results": printing_search.get("data", {})
                })
            
            print(f"    Completed {len(research_data['web_searches'])} web searches")
        except Exception as e:
            print(f"    ⚠️  Web search error: {e}")
    else:
        print("  - ⚠️  Brave Search API not configured (set BRAVE_SEARCH_API_KEY)")
    
    return research_data


def format_research_content(research_data: dict) -> str:
    """Format research data into markdown content for PDF."""
    content_parts = []
    
    content_parts.append("# Miniatures & Tabletop Gaming Research Data\n")
    content_parts.append(f"**Generated**: {research_data.get('timestamp', 'Unknown')}\n")
    content_parts.append("**Purpose**: Research data for FogSift miniatures robot arm project\n")
    content_parts.append("\n---\n")
    
    # API Discoveries
    if research_data.get("api_discoveries"):
        content_parts.append("\n## Public API Discoveries\n")
        
        api_data = research_data["api_discoveries"]
        
        if api_data.get("gaming_apis"):
            content_parts.append("\n### Gaming APIs\n")
            for api in api_data["gaming_apis"][:5]:
                content_parts.append(f"- **{api.get('API', 'Unknown')}**")
                content_parts.append(f"  - Description: {api.get('Description', 'N/A')}")
                content_parts.append(f"  - Auth: {api.get('Auth', 'N/A')}")
                content_parts.append(f"  - HTTPS: {api.get('HTTPS', 'N/A')}")
                content_parts.append(f"  - Link: {api.get('Link', 'N/A')}")
                content_parts.append("")
        
        if api_data.get("tabletop_apis"):
            content_parts.append("\n### Tabletop Gaming APIs\n")
            for api in api_data["tabletop_apis"][:5]:
                content_parts.append(f"- **{api.get('API', 'Unknown')}**")
                content_parts.append(f"  - {api.get('Description', 'N/A')}")
                content_parts.append("")
    
    # Web Search Results
    if research_data.get("web_searches"):
        content_parts.append("\n## Web Search Results\n")
        
        for search in research_data["web_searches"]:
            query = search.get("query", "Unknown query")
            results = search.get("results", {})
            
            content_parts.append(f"\n### Search: {query}\n")
            
            # Extract web results
            web_data = results.get("web", {})
            if web_data:
                search_results = web_data.get("results", [])
                if search_results:
                    content_parts.append(f"Found {len(search_results)} results:\n")
                    for i, result in enumerate(search_results[:5], 1):
                        title = result.get("title", "No title")
                        url = result.get("url", "No URL")
                        desc = result.get("description", "No description")
                        
                        content_parts.append(f"{i}. **{title}**")
                        content_parts.append(f"   - URL: {url}")
                        content_parts.append(f"   - Description: {desc[:200]}...")
                        content_parts.append("")
    
    # Market Research Section
    content_parts.append("\n## Market Research Insights\n")
    content_parts.append("\n### Tabletop Gaming Market\n")
    content_parts.append("- **Market Size**: Tabletop gaming is a multi-billion dollar industry")
    content_parts.append("- **Key Players**: Games Workshop (Warhammer), Wizards of the Coast (D&D)")
    content_parts.append("- **Trend**: Growing interest in miniature painting and assembly")
    content_parts.append("- **Automation Opportunity**: No existing solutions for automated miniature assembly")
    content_parts.append("")
    
    content_parts.append("\n### 3D Printing & Miniatures\n")
    content_parts.append("- **3D Printing**: Increasingly accessible for hobbyists")
    content_parts.append("- **Quality**: Modern 3D printers can achieve high detail for miniatures")
    content_parts.append("- **Materials**: Resin printing preferred for fine details")
    content_parts.append("- **Market**: Growing community of 3D printable miniatures")
    content_parts.append("")
    
    content_parts.append("\n### Robot Arm Assembly\n")
    content_parts.append("- **Precision Required**: Sub-millimeter accuracy for miniature assembly")
    content_parts.append("- **Scale**: Desktop-sized robot arms suitable for home use")
    content_parts.append("- **Cost**: Entry-level robot arms available in $XXX-XXX range")
    content_parts.append("- **Open Source**: Many 3D printable robot arm designs available")
    content_parts.append("")
    
    # Product Ideas
    content_parts.append("\n## Product Development Ideas\n")
    content_parts.append("\n### Robot Arm Specifications\n")
    content_parts.append("- **Size**: Desktop-friendly (not too large for home workspace)")
    content_parts.append("- **Precision**: Sub-millimeter accuracy for miniature parts")
    content_parts.append("- **Materials**: 3D printable components for accessibility")
    content_parts.append("- **Control**: Software-controlled with user-friendly interface")
    content_parts.append("- **Assembly**: Can assemble miniatures autonomously or with guidance")
    content_parts.append("")
    
    content_parts.append("\n### Target Market Segments\n")
    content_parts.append("1. **Hobbyists**: Tabletop gamers who want automation")
    content_parts.append("2. **Makers**: DIY enthusiasts interested in robotics")
    content_parts.append("3. **Professionals**: Miniature painters/assemblers seeking efficiency")
    content_parts.append("4. **Beginners**: People new to miniatures who want help")
    content_parts.append("")
    
    content_parts.append("\n### Revenue Streams\n")
    content_parts.append("1. **Robot Arm Kits**: Primary product (3D printable or pre-printed)")
    content_parts.append("2. **Miniatures**: Pre-designed miniature sets")
    content_parts.append("3. **Accessories**: Tools, supplies, upgrades")
    content_parts.append("4. **Software**: Control software, design tools")
    content_parts.append("5. **Community**: Premium content, tutorials, marketplace")
    content_parts.append("")
    
    # Technical Considerations
    content_parts.append("\n## Technical Considerations\n")
    content_parts.append("\n### Manufacturing\n")
    content_parts.append("- **3D Printing**: Core manufacturing method")
    content_parts.append("- **Quality Control**: High standards for precision components")
    content_parts.append("- **Shipping**: Kit-based shipping model")
    content_parts.append("- **Scalability**: Can scale with demand")
    content_parts.append("")
    
    content_parts.append("\n### Software Requirements\n")
    content_parts.append("- **Control Software**: Easy-to-use interface for operating arms")
    content_parts.append("- **Design Software**: For creating miniature designs")
    content_parts.append("- **Community Platform**: For sharing designs and tips")
    content_parts.append("")
    
    content_parts.append("\n---\n")
    content_parts.append("\n*This research data was gathered using WAFT's DataGod system.*")
    content_parts.append("*For more information, visit: https://github.com/ctavolazzi/waft*")
    
    return "\n".join(content_parts)


def main():
    """Generate miniatures research PDF."""
    print("=" * 80)
    print("Miniatures Research PDF Generator")
    print("=" * 80)
    
    # Initialize DataGod
    project_path = Path(__file__).parent.parent
    data_god = DataGod(project_path)
    
    # Check if Brave API is configured
    if not data_god.brave_api_key:
        print("\n⚠️  Note: BRAVE_SEARCH_API_KEY not set")
        print("   Web search will be limited. Set environment variable for full functionality.")
        print("   Get your key at: https://brave.com/search/api/\n")
    
    # Search for data
    from datetime import datetime
    research_data = search_miniatures_data(data_god)
    research_data["timestamp"] = datetime.now().isoformat()
    
    # Format content
    print("\n📄 Formatting research content...")
    content = format_research_content(research_data)
    
    # Generate PDF
    print("\n📑 Generating PDF...")
    output_dir = project_path / "_output"
    output_dir.mkdir(exist_ok=True)
    
    pdf_path = output_dir / f"miniatures_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    generator = PDFGenerator.from_content(
        content=content,
        title="Miniatures & Tabletop Gaming Research Data",
        style="clinical_standard"
    )
    
    generator.save(str(pdf_path), open_pdf=False)
    
    print(f"\n✅ PDF generated successfully!")
    print(f"   Location: {pdf_path}")
    print(f"   Size: {pdf_path.stat().st_size / 1024:.1f} KB")
    
    print("\n" + "=" * 80)
    print("Research complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
