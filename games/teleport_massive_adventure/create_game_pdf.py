#!/usr/bin/env python3
"""
Generate a PDF document for Teleport Massive: The Adventure
Includes game plan and screenshots
"""

import os
from pathlib import Path

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False
    print("reportlab not found, trying fpdf...")
    try:
        from fpdf import FPDF
        HAS_FPDF = True
    except ImportError:
        HAS_FPDF = False
        print("Neither reportlab nor fpdf found. Please install: pip install reportlab")

def create_pdf_with_reportlab(output_path, game_plan_path, screenshots_dir):
    """Create PDF using reportlab"""
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=36,
        textColor=colors.HexColor('#00aaff'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=20,
        textColor=colors.HexColor('#00ff88'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#00aaff'),
        spaceAfter=8,
        spaceBefore=8
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        leading=14,
        alignment=TA_JUSTIFY
    )
    
    # Title page
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("TELEPORT MASSIVE", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("The Adventure", heading_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(
        "<i>\"They said death was final. They must be wrong.\"</i>",
        ParagraphStyle('Quote', parent=styles['Normal'], fontSize=14, alignment=TA_CENTER, textColor=colors.grey)
    ))
    story.append(PageBreak())
    
    # Game Overview
    story.append(Paragraph("Game Overview", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    overview_text = """
    <b>Genre:</b> Cyberpunk Point-and-Click Adventure with Combat<br/>
    <b>Playtime:</b> 20-30 minutes<br/>
    <b>Endings:</b> 3 (Join, Escape, Destroy)<br/><br/>
    
    <b>Story:</b> Aziah, a lab technician at Teleport Massive Corp, discovers their colleague Maya has vanished into "The Between" - a glitch dimension between teleport jumps. Following her trail, Aziah uncovers the truth: The Dealer, a cosmic entity trapped in the corporation's systems, has been collecting souls. Maya beat him once. Can you?
    """
    story.append(Paragraph(overview_text, body_style))
    story.append(PageBreak())
    
    # Screenshots section
    story.append(Paragraph("Game Screenshots", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    screenshot_files = [
        ('lab_scene.png', 'Lab Scene - The starting area where Aziah begins their journey'),
        ('stats_hud_working.png', 'Stats HUD - Player interface showing health, XP, and level'),
        ('teleport_massive_scene_with_dealer.png', 'The Dealer Scene - Confrontation with the cosmic entity'),
        ('autoplayer_running.png', 'Auto Player - Automated gameplay demonstration')
    ]
    
    for img_file, caption in screenshot_files:
        img_path = os.path.join(screenshots_dir, img_file)
        if os.path.exists(img_path):
            story.append(Paragraph(f"<b>{caption}</b>", subheading_style))
            story.append(Spacer(1, 0.1*inch))
            
            # Add image (scale to fit page width)
            img = Image(img_path, width=6.5*inch, height=4.5*inch)
            story.append(img)
            story.append(Spacer(1, 0.3*inch))
        else:
            story.append(Paragraph(f"<i>Screenshot not found: {img_file}</i>", body_style))
            story.append(Spacer(1, 0.2*inch))
    
    story.append(PageBreak())
    
    # World Map
    story.append(Paragraph("World Map", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    map_text = """
    The game world consists of multiple interconnected areas:
    <br/><br/>
    <b>ACT 1: Discovery</b><br/>
    • Lab (Tutorial) - Starting area<br/>
    • Corridor - First combat encounter<br/>
    • Security Room - Mini-boss fight<br/>
    • Office - Story choice point<br/>
    • Storage - Resource gathering<br/>
    <br/>
    <b>ACT 2: Descent</b><br/>
    • Upper Corridor - Combat gauntlet<br/>
    • Archives - Major puzzle<br/>
    • Mainframe - Boss fight<br/>
    • Transit Hub - Final preparation<br/>
    <br/>
    <b>ACT 3: The Dealer</b><br/>
    • The Void - Final confrontation with three possible endings
    """
    story.append(Paragraph(map_text, body_style))
    story.append(PageBreak())
    
    # Key Features
    story.append(Paragraph("Key Features", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    features_text = """
    <b>Core Systems:</b><br/>
    • Stats System (HP, XP, Level progression)<br/>
    • Combat System with turn-based mechanics<br/>
    • Dialogue System with branching conversations<br/>
    • Inventory System for item management<br/>
    • The Dealer - Dynamic commentary system<br/>
    <br/>
    <b>Gameplay:</b><br/>
    • Point-and-click adventure mechanics<br/>
    • Combat encounters with various enemies<br/>
    • Puzzle-solving elements<br/>
    • Multiple endings based on player choices<br/>
    • Character progression through XP and leveling<br/>
    <br/>
    <b>Visual Style:</b><br/>
    • Pixel art aesthetic<br/>
    • Cyberpunk atmosphere<br/>
    • Dark, atmospheric environments<br/>
    • Dynamic UI with neon accents
    """
    story.append(Paragraph(features_text, body_style))
    story.append(PageBreak())
    
    # The Three Endings
    story.append(Paragraph("The Three Endings", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    endings_text = """
    <b>Ending 1: JOIN THE GAME</b><br/>
    Aziah takes a seat at the table. The Dealer smiles genuinely for the first time. "Finally. A partner. The game goes on." Aziah becomes the new observer, dealing cards to future players.<br/><br/>
    
    <b>Ending 2: ESCAPE THE BETWEEN</b><br/>
    A portal opens behind Aziah. The Dealer watches, resigned. "Go then. Maya did the same. Everyone leaves eventually." Aziah steps through, returns to the real world. The lab is empty. Maya's gone. But Aziah is free.<br/><br/>
    
    <b>Ending 3: FLIP THE TABLE</b><br/>
    Aziah approaches the table. The Dealer tenses. Aziah flips the Infinite Table. Everything shatters. The Dealer screams - then laughs, then cries. "You... you actually did it. I'm free. I'm finally free." Dr. Marcus Vale's human form flickers into existence. "Thank you. I'd forgotten what it felt like to end." The void collapses. Aziah wakes up in the lab. Maya is there. "You did it. You actually ended the game."<br/><br/>
    
    <i>This is the TRUE ENDING.</i>
    """
    story.append(Paragraph(endings_text, body_style))
    
    # Build PDF
    doc.build(story)
    print(f"PDF created successfully: {output_path}")

def create_pdf_with_fpdf(output_path, game_plan_path, screenshots_dir):
    """Create PDF using fpdf (fallback)"""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title page
    pdf.add_page()
    pdf.set_font('Arial', 'B', 24)
    pdf.set_text_color(0, 170, 255)  # #00aaff
    pdf.cell(0, 20, 'TELEPORT MASSIVE', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 18)
    pdf.set_text_color(0, 255, 136)  # #00ff88
    pdf.cell(0, 10, 'The Adventure', 0, 1, 'C')
    pdf.set_font('Arial', 'I', 12)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, '"They said death was final. They must be wrong."', 0, 1, 'C')
    
    # Game Overview
    pdf.add_page()
    pdf.set_font('Arial', 'B', 20)
    pdf.set_text_color(0, 255, 136)
    pdf.cell(0, 10, 'Game Overview', 0, 1, 'L')
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, 'Genre: Cyberpunk Point-and-Click Adventure with Combat', 0, 1, 'L')
    pdf.cell(0, 8, 'Playtime: 20-30 minutes', 0, 1, 'L')
    pdf.cell(0, 8, 'Endings: 3 (Join, Escape, Destroy)', 0, 1, 'L')
    pdf.ln(5)
    pdf.multi_cell(0, 6, 'Story: Aziah, a lab technician at Teleport Massive Corp, discovers their colleague Maya has vanished into "The Between" - a glitch dimension between teleport jumps. Following her trail, Aziah uncovers the truth: The Dealer, a cosmic entity trapped in the corporation\'s systems, has been collecting souls. Maya beat him once. Can you?', 0, 'L')
    
    # Screenshots
    screenshot_files = [
        ('lab_scene.png', 'Lab Scene - The starting area'),
        ('stats_hud_working.png', 'Stats HUD - Player interface'),
        ('teleport_massive_scene_with_dealer.png', 'The Dealer Scene'),
        ('autoplayer_running.png', 'Auto Player')
    ]
    
    for img_file, caption in screenshot_files:
        img_path = os.path.join(screenshots_dir, img_file)
        if os.path.exists(img_path):
            pdf.add_page()
            pdf.set_font('Arial', 'B', 14)
            pdf.set_text_color(0, 170, 255)
            pdf.cell(0, 10, caption, 0, 1, 'L')
            pdf.ln(5)
            try:
                pdf.image(img_path, x=10, y=pdf.get_y(), w=190)
            except Exception as e:
                pdf.cell(0, 10, f'Error loading image: {e}', 0, 1, 'L')
    
    pdf.output(output_path)
    print(f"PDF created successfully: {output_path}")

def main():
    base_dir = Path(__file__).parent
    screenshots_dir = base_dir / 'screenshots'
    game_plan_path = base_dir / 'GAME_PLAN.md'
    output_path = base_dir / 'Teleport_Massive_Game_Documentation.pdf'
    
    if not screenshots_dir.exists():
        print(f"Error: Screenshots directory not found: {screenshots_dir}")
        return
    
    if HAS_REPORTLAB:
        print("Using reportlab to create PDF...")
        create_pdf_with_reportlab(str(output_path), str(game_plan_path), str(screenshots_dir))
    elif HAS_FPDF:
        print("Using fpdf to create PDF...")
        create_pdf_with_fpdf(str(output_path), str(game_plan_path), str(screenshots_dir))
    else:
        print("Error: No PDF library available. Please install reportlab or fpdf:")
        print("  pip install reportlab")
        print("  or")
        print("  pip install fpdf2")

if __name__ == '__main__':
    main()
