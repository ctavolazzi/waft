#!/usr/bin/env python3
"""
Create WAFT D&D Binder PDF using ReportLab

ReportLab is the industry standard for professional PDF generation.
Uses Platypus framework for automatic text flow and page breaks.
"""

from pathlib import Path
import markdown
import re
from datetime import datetime
from html import unescape

# ReportLab imports
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, PageTemplate, Frame, NextPageTemplate
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

def create_custom_styles():
    """Create custom paragraph styles for the binder."""
    styles = getSampleStyleSheet()
    
    # Cover page title
    styles.add(ParagraphStyle(
        name='CoverTitle',
        parent=styles['Heading1'],
        fontSize=48,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica',
        leading=56
    ))
    
    # Cover subtitle
    styles.add(ParagraphStyle(
        name='CoverSubtitle',
        parent=styles['Normal'],
        fontSize=24,
        textColor=colors.HexColor('#666666'),
        spaceAfter=40,
        alignment=TA_CENTER,
        fontStyle='italic'
    ))
    
    # Section divider
    styles.add(ParagraphStyle(
        name='SectionDivider',
        parent=styles['Heading1'],
        fontSize=36,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica',
        leading=42
    ))
    
    # H1 style
    styles.add(ParagraphStyle(
        name='CustomH1',
        parent=styles['Heading1'],
        fontSize=32,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=18,
        spaceBefore=36,
        fontName='Helvetica',
        leading=38
    ))
    
    # H2 style
    styles.add(ParagraphStyle(
        name='CustomH2',
        parent=styles['Heading2'],
        fontSize=22,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=24,
        fontName='Helvetica-Bold',
        leading=26,
        borderWidth=0,
        borderColor=colors.HexColor('#3498db'),
        borderPadding=0
    ))
    
    # H3 style
    styles.add(ParagraphStyle(
        name='CustomH3',
        parent=styles['Heading3'],
        fontSize=17,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=10,
        spaceBefore=18,
        fontName='Helvetica-Bold',
        leading=20
    ))
    
    # Body text with justification
    styles.add(ParagraphStyle(
        name='BodyJustified',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#2c2c2c'),
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leading=19,
        fontName='Times-Roman'
    ))
    
    # TOC styles
    styles.add(ParagraphStyle(
        name='TOCSection',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='TOCItem',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=4,
        leftIndent=20,
        bulletIndent=10,
        bulletText='•'
    ))
    
    return styles

def markdown_to_reportlab_story(markdown_content, styles):
    """Convert markdown to ReportLab story elements."""
    story = []
    
    # Convert markdown to HTML first
    html = markdown.markdown(
        markdown_content,
        extensions=['fenced_code', 'tables', 'nl2br', 'extra', 'codehilite']
    )
    html = unescape(html)
    
    # Simple HTML parsing (basic implementation)
    lines = html.split('\n')
    current_paragraph = []
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_paragraph:
                text = ' '.join(current_paragraph)
                if text:
                    story.append(Paragraph(text, styles['BodyJustified']))
                    story.append(Spacer(1, 0.12*inch))
                current_paragraph = []
            continue
        
        # Handle headers
        if line.startswith('<h1>'):
            if current_paragraph:
                text = ' '.join(current_paragraph)
                if text:
                    story.append(Paragraph(text, styles['BodyJustified']))
                current_paragraph = []
            text = re.sub(r'<[^>]+>', '', line)
            story.append(Paragraph(text, styles['CustomH1']))
            story.append(Spacer(1, 0.2*inch))
        elif line.startswith('<h2>'):
            if current_paragraph:
                text = ' '.join(current_paragraph)
                if text:
                    story.append(Paragraph(text, styles['BodyJustified']))
                current_paragraph = []
            text = re.sub(r'<[^>]+>', '', line)
            story.append(Paragraph(text, styles['CustomH2']))
            story.append(Spacer(1, 0.15*inch))
        elif line.startswith('<h3>'):
            if current_paragraph:
                text = ' '.join(current_paragraph)
                if text:
                    story.append(Paragraph(text, styles['BodyJustified']))
                current_paragraph = []
            text = re.sub(r'<[^>]+>', '', line)
            story.append(Paragraph(text, styles['CustomH3']))
            story.append(Spacer(1, 0.12*inch))
        # Handle tables (basic)
        elif line.startswith('<table>'):
            # Skip table parsing for now - would need more complex logic
            continue
        # Handle paragraphs
        elif line.startswith('<p>'):
            text = re.sub(r'<[^>]+>', '', line)
            text = text.strip()
            if text:
                current_paragraph.append(text)
        else:
            # Regular text
            text = re.sub(r'<[^>]+>', '', line)
            text = text.strip()
            if text:
                current_paragraph.append(text)
    
    # Add remaining paragraph
    if current_paragraph:
        text = ' '.join(current_paragraph)
        if text:
            story.append(Paragraph(text, styles['BodyJustified']))
    
    return story

def create_cover_page(styles):
    """Create cover page elements."""
    story = []
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("WAFT", styles['CoverTitle']))
    story.append(Paragraph("D&D Binder", styles['CoverSubtitle']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Complete Reference Guide", styles['Normal']))
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("Version 1.0 | 2026-01-12", styles['Normal']))
    story.append(PageBreak())
    return story

def create_toc(styles):
    """Create table of contents."""
    story = []
    story.append(Paragraph("Table of Contents", styles['Heading1']))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Part I: Game Rules", styles['TOCSection']))
    story.append(Paragraph("Introduction & Quick Start", styles['TOCItem']))
    story.append(Paragraph("Character Creation", styles['TOCItem']))
    story.append(Paragraph("D&D 5e Mechanics", styles['TOCItem']))
    story.append(Paragraph("Spell System", styles['TOCItem']))
    story.append(Paragraph("Quest System", styles['TOCItem']))
    story.append(Paragraph("Karma System", styles['TOCItem']))
    story.append(Paragraph("Scint Economy", styles['TOCItem']))
    story.append(Paragraph("Game Flow", styles['TOCItem']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Part II: Character Sheet", styles['TOCSection']))
    story.append(Paragraph("Fillable Character Sheet", styles['TOCItem']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Part III: Quest Tracking", styles['TOCSection']))
    story.append(Paragraph("Quest Sheet Template", styles['TOCItem']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Part IV: Quick Reference", styles['TOCSection']))
    story.append(Paragraph("Ability Scores Reference", styles['TOCItem']))
    story.append(Paragraph("Spell Slots Reference", styles['TOCItem']))
    story.append(Paragraph("Karma Types & Evolution Paths", styles['TOCItem']))
    story.append(Paragraph("Scint Sources & Costs", styles['TOCItem']))
    story.append(Paragraph("Quest Types & Encounter Types", styles['TOCItem']))
    story.append(Paragraph("Difficulty Levels & Rewards", styles['TOCItem']))
    story.append(PageBreak())
    
    return story

def create_character_sheet(styles):
    """Create character sheet section."""
    story = []
    story.append(PageBreak())
    story.append(Paragraph("Part II: Character Sheet", styles['SectionDivider']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Fillable Character Sheet", styles['CustomH2']))
    story.append(Spacer(1, 0.2*inch))
    
    # Character info table
    char_info_data = [
        ['Character Name', 'Scientific Name'],
        ['', ''],
        ['Being ID', 'Level'],
        ['', '']
    ]
    char_info_table = Table(char_info_data, colWidths=[3*inch, 3*inch])
    char_info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(char_info_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Ability scores
    story.append(Paragraph("Ability Scores", styles['CustomH3']))
    ability_data = [
        ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'],
        ['10', '12', '14', '16', '14', '12'],
        ['+0', '+1', '+2', '+3', '+2', '+1']
    ]
    ability_table = Table(ability_data, colWidths=[1*inch]*6)
    ability_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, 1), 18),
        ('FONTSIZE', (0, 2), (-1, 2), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(ability_table)
    story.append(PageBreak())
    
    return story

def create_quest_sheet(styles):
    """Create quest sheet section."""
    story = []
    story.append(PageBreak())
    story.append(Paragraph("Part III: Quest Tracking", styles['SectionDivider']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Quest Sheet Template", styles['CustomH2']))
    story.append(Spacer(1, 0.2*inch))
    
    # Quest info
    quest_data = [
        ['Quest Name', 'Quest Type'],
        ['', ''],
        ['Quest ID / Cycle', 'Date Started'],
        ['', '']
    ]
    quest_table = Table(quest_data, colWidths=[3*inch, 3*inch])
    quest_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(quest_table)
    story.append(PageBreak())
    
    return story

def create_quick_reference(styles):
    """Create quick reference tables."""
    story = []
    story.append(PageBreak())
    story.append(Paragraph("Part IV: Quick Reference", styles['SectionDivider']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Essential Reference Tables", styles['CustomH2']))
    story.append(Spacer(1, 0.2*inch))
    
    # Ability Scores table
    story.append(Paragraph("Ability Scores Quick Reference", styles['CustomH2']))
    ability_ref_data = [
        ['Ability', 'Base Score', 'Modifier', 'Use Case'],
        ['Strength (STR)', '8-15', '-1 to +2', 'Physical tasks'],
        ['Dexterity (DEX)', '10-16', '0 to +3', 'AC, initiative'],
        ['Constitution (CON)', '12-16', '+1 to +3', 'HP, saving throws'],
        ['Intelligence (INT)', '14-18', '+2 to +4', 'Spellcasting, logic'],
        ['Wisdom (WIS)', '12-16', '+1 to +3', 'Perception, insight'],
        ['Charisma (CHA)', '10-14', '0 to +2', 'Social interactions'],
    ]
    ability_ref_table = Table(ability_ref_data, colWidths=[1.5*inch, 1*inch, 1*inch, 2.5*inch])
    ability_ref_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
    ]))
    story.append(ability_ref_table)
    story.append(Spacer(1, 0.3*inch))
    
    return story

def main():
    """Generate WAFT D&D Binder PDF using ReportLab."""
    
    # Read game rules
    rules_file = Path("WAFT_GAME_RULES.md")
    if not rules_file.exists():
        print(f"❌ Error: {rules_file} not found")
        return
    
    markdown_content = rules_file.read_text()
    
    # Get desktop path
    desktop_path = Path.home() / "Desktop"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = desktop_path / f"WAFT_DnD_Binder_REPORTLAB_{timestamp}.pdf"
    
    print("📚 Creating WAFT D&D Binder with ReportLab...")
    print("   ✨ Industry-standard PDF generation")
    print("   📑 Automatic text flow and pagination")
    print("   📊 Professional tables and layouts")
    
    # Create document
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Create styles
    styles = create_custom_styles()
    
    # Build story
    story = []
    
    # Cover page
    story.extend(create_cover_page(styles))
    
    # Table of contents
    story.extend(create_toc(styles))
    
    # Part I: Game Rules
    story.append(PageBreak())
    story.append(Paragraph("Part I: Game Rules", styles['SectionDivider']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("The Complete WAFT Game Rules", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Convert markdown to story (simplified - full implementation would parse HTML properly)
    game_rules_story = markdown_to_reportlab_story(markdown_content, styles)
    story.extend(game_rules_story)
    
    # Part II: Character Sheet
    story.extend(create_character_sheet(styles))
    
    # Part III: Quest Sheet
    story.extend(create_quest_sheet(styles))
    
    # Part IV: Quick Reference
    story.extend(create_quick_reference(styles))
    
    # Build PDF
    doc.build(story)
    
    # Open the PDF
    import subprocess
    import platform
    system = platform.system()
    if system == "Darwin":  # macOS
        subprocess.run(["open", str(output_path)], check=False)
    elif system == "Windows":
        subprocess.run(["start", str(output_path)], shell=True, check=False)
    else:  # Linux
        subprocess.run(["xdg-open", str(output_path)], check=False)
    
    print(f"✅ D&D Binder created: {output_path}")
    print(f"📖 Opening ReportLab version on desktop...")
    print(f"   📚 Generated with ReportLab Platypus framework")
    
    return output_path

if __name__ == "__main__":
    main()
