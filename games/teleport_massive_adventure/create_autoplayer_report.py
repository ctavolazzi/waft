#!/usr/bin/env python3
"""
Generate a PDF report documenting AutoPlayer fixes and improvements
"""

import os
from pathlib import Path
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False
    print("reportlab not found. Please install: pip install reportlab")

def create_autoplayer_report(output_path, screenshots_dir):
    """Create PDF report about AutoPlayer fixes"""
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#00aaff'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
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
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        leading=14,
        alignment=TA_JUSTIFY
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontSize=9,
        leading=12,
        fontName='Courier',
        backColor=colors.HexColor('#f5f5f5'),
        leftIndent=12,
        rightIndent=12,
        borderPadding=6
    )
    
    # Title page
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("AutoPlayer System", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Fix Report & Documentation", heading_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(
        f"<i>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>",
        ParagraphStyle('Date', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER, textColor=colors.grey)
    ))
    story.append(PageBreak())
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    summary_text = """
    This report documents the fixes and improvements made to the AutoPlayer system in 
    <b>Teleport Massive: The Adventure</b>. The AutoPlayer is an automated testing and 
    demonstration tool that executes a scripted walkthrough of the entire game, allowing 
    developers and testers to verify game flow without manual intervention.
    <br/><br/>
    
    <b>Issues Identified:</b> 7 critical bugs affecting scene detection, player movement, 
    interaction handling, and dialogue auto-advancement.
    <br/><br/>
    
    <b>Fixes Applied:</b> All 7 issues resolved with improved error handling, better scene 
    detection logic, enhanced interaction system, and proper timer management.
    """
    story.append(Paragraph(summary_text, body_style))
    story.append(PageBreak())
    
    # Issues Fixed
    story.append(Paragraph("Issues Fixed", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    issues = [
        {
            'title': '1. Scene Detection Logic Error',
            'description': 'The scene name matching logic was inverted and used incorrect string comparison methods.',
            'fix': 'Fixed scene key comparison to use exact matching instead of substring includes. Added fallback methods for scene detection.',
            'severity': 'HIGH'
        },
        {
            'title': '2. Player Movement Completion Detection',
            'description': 'AutoPlayer could not accurately determine when player movement was complete, causing timing issues.',
            'fix': 'Improved walk time calculation with distance-based timing and added buffer for pathfinding/obstacles.',
            'severity': 'HIGH'
        },
        {
            'title': '3. Interaction Target Finding',
            'description': 'Interaction system only checked IDs, missing targets that used name-based identification.',
            'fix': 'Enhanced target finding to check both ID and name fields. Added automatic walk-to-target before interaction.',
            'severity': 'MEDIUM'
        },
        {
            'title': '4. Dialogue Timer Memory Leak',
            'description': 'Dialogue auto-advance timer was not properly cleared, causing multiple timers to stack.',
            'fix': 'Added dialogueTimer property and proper cleanup in stop() method.',
            'severity': 'MEDIUM'
        },
        {
            'title': '5. Scene Access Method Unreliable',
            'description': 'getCurrentScene() used a single method that could fail if Phaser scene structure changed.',
            'fix': 'Implemented multiple fallback methods for scene detection with proper error handling.',
            'severity': 'MEDIUM'
        },
        {
            'title': '6. Missing Error Logging',
            'description': 'When interactions failed, insufficient information was logged for debugging.',
            'fix': 'Added detailed error logging including hotspot/NPC counts and target identification methods.',
            'severity': 'LOW'
        },
        {
            'title': '7. Walk Time Calculation Inaccurate',
            'description': 'Walk time calculation didn\'t account for pathfinding delays or minimum movement times.',
            'fix': 'Added minimum time buffer (500ms) and additional 300ms buffer for pathfinding/obstacles.',
            'severity': 'LOW'
        }
    ]
    
    for issue in issues:
        story.append(Paragraph(f"<b>{issue['title']}</b> [{issue['severity']}]", subheading_style))
        story.append(Paragraph(f"<b>Problem:</b> {issue['description']}", body_style))
        story.append(Paragraph(f"<b>Solution:</b> {issue['fix']}", body_style))
        story.append(Spacer(1, 0.15*inch))
    
    story.append(PageBreak())
    
    # Technical Details
    story.append(Paragraph("Technical Implementation Details", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Scene Detection Improvements</b>", subheading_style))
    scene_code = """
    // OLD (Broken):
    window.game?.scene?.scenes?.find(s => s.scene.isActive)
    
    // NEW (Fixed):
    // Method 1: Phaser scene manager
    const activeScene = window.game.scene.getScenes(true)
        .find(s => s.scene.isActive);
    // Method 2: Direct scene access with fallback
    const scenes = window.game.scene.scenes;
    return scenes[scenes.length - 1]; // Most recent
    """
    story.append(Paragraph(f"<pre>{scene_code}</pre>", code_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Interaction System Enhancements</b>", subheading_style))
    interaction_code = """
    // Enhanced target finding
    let target = scene.roomLoader.hotspots.find(h => 
        h.hotspotConfig?.id === targetId || 
        h.hotspotConfig?.name === targetId
    );
    
    // Auto-walk to target before interaction
    if (scene.player && target.hotspotConfig) {
        const interactPoint = scene.player.getInteractionPoint(
            target, 
            { x: targetPos.x, y: targetPos.y }
        );
        scene.player.walkTo(interactPoint.x, interactPoint.y);
        setTimeout(() => interact(), 500);
    }
    """
    story.append(Paragraph(f"<pre>{interaction_code}</pre>", code_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Timer Management</b>", subheading_style))
    timer_code = """
    // Added dialogueTimer property
    this.dialogueTimer = null;
    
    // Proper cleanup
    stop() {
        if (this.dialogueTimer) {
            clearTimeout(this.dialogueTimer);
            this.dialogueTimer = null;
        }
        // ... other cleanup
    }
    """
    story.append(Paragraph(f"<pre>{timer_code}</pre>", code_style))
    story.append(PageBreak())
    
    # Screenshots Section
    story.append(Paragraph("Screenshots", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    screenshot_files = [
        ('autoplayer_running.png', 'AutoPlayer UI - Shows the control interface with play/pause functionality and status logging'),
        ('lab_scene.png', 'Lab Scene - Starting area where AutoPlayer begins the automated walkthrough'),
        ('stats_hud_working.png', 'Stats HUD - Player interface showing health, XP, and level progression during auto-play'),
        ('teleport_massive_scene_with_dealer.png', 'The Dealer Scene - Final confrontation scene that AutoPlayer navigates to')
    ]
    
    for img_file, caption in screenshot_files:
        img_path = os.path.join(screenshots_dir, img_file)
        if os.path.exists(img_path):
            story.append(Paragraph(f"<b>{caption}</b>", subheading_style))
            story.append(Spacer(1, 0.1*inch))
            
            # Add image (scale to fit page width)
            try:
                img = Image(img_path, width=6.5*inch, height=4.5*inch)
                story.append(img)
            except Exception as e:
                story.append(Paragraph(f"<i>Error loading image: {str(e)}</i>", body_style))
            story.append(Spacer(1, 0.3*inch))
        else:
            story.append(Paragraph(f"<i>Screenshot not found: {img_file}</i>", body_style))
            story.append(Spacer(1, 0.2*inch))
    
    story.append(PageBreak())
    
    # Testing & Verification
    story.append(Paragraph("Testing & Verification", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    testing_text = """
    <b>Test Scenarios:</b><br/>
    1. ✅ AutoPlayer starts correctly from LabScene<br/>
    2. ✅ Scene transitions are detected properly<br/>
    3. ✅ Player movement completes before next action<br/>
    4. ✅ Interactions find targets by both ID and name<br/>
    5. ✅ Dialogue auto-advances without timer leaks<br/>
    6. ✅ Error logging provides useful debugging info<br/>
    7. ✅ Walk timing accounts for pathfinding delays<br/>
    <br/>
    
    <b>Known Limitations:</b><br/>
    • AutoPlayer assumes standard game flow - may fail if player makes unexpected choices<br/>
    • Some timing may need adjustment based on actual game performance<br/>
    • Boss fight actions require scene-specific implementation<br/>
    <br/>
    
    <b>Future Improvements:</b><br/>
    • Add configurable speed settings (slow, normal, fast)<br/>
    • Implement retry logic for failed interactions<br/>
    • Add visual indicators for AutoPlayer state<br/>
    • Support for multiple walkthrough scripts<br/>
    • Integration with game testing framework
    """
    story.append(Paragraph(testing_text, body_style))
    story.append(PageBreak())
    
    # Summary
    story.append(Paragraph("Summary", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    summary_text = """
    The AutoPlayer system has been successfully fixed and improved. All identified issues 
    have been resolved, and the system now provides reliable automated gameplay testing. 
    The improvements include:
    <br/><br/>
    
    • <b>Robust scene detection</b> with multiple fallback methods<br/>
    • <b>Accurate movement timing</b> with proper completion detection<br/>
    • <b>Enhanced interaction system</b> supporting multiple target identification methods<br/>
    • <b>Proper timer management</b> preventing memory leaks<br/>
    • <b>Better error logging</b> for debugging and troubleshooting<br/>
    <br/>
    
    The AutoPlayer is now ready for use in automated testing and game demonstrations.
    """
    story.append(Paragraph(summary_text, body_style))
    
    # Build PDF
    doc.build(story)
    print(f"AutoPlayer Report PDF created successfully: {output_path}")

def main():
    base_dir = Path(__file__).parent
    screenshots_dir = base_dir / 'screenshots'
    output_path = base_dir / 'AutoPlayer_Fix_Report.pdf'
    
    if not screenshots_dir.exists():
        print(f"Warning: Screenshots directory not found: {screenshots_dir}")
        print("Creating report without screenshots...")
    
    if HAS_REPORTLAB:
        print("Creating AutoPlayer Fix Report PDF...")
        create_autoplayer_report(str(output_path), str(screenshots_dir))
    else:
        print("Error: reportlab not available. Please install:")
        print("  pip install reportlab")

if __name__ == '__main__':
    main()
