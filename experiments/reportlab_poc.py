"""
ReportLab Proof of Concept - Clinical Standard

This demonstrates what Foundation V3 could look like with ReportLab backend
while maintaining the same block-based API from V2.
"""

try:
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, PageBreak,
        Table, TableStyle, KeepTogether
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from pathlib import Path
    from datetime import datetime

    print("=" * 80)
    print("REPORTLAB PROOF OF CONCEPT - Clinical Standard")
    print("=" * 80)

    # Create Clinical Standard styles (same as V2 spec)
    def create_clinical_styles():
        styles = getSampleStyleSheet()

        # Cover page title
        styles.add(ParagraphStyle(
            name='CoverTitle',
            parent=styles['Title'],
            fontName='Helvetica-Bold',
            fontSize=22,
            alignment=TA_CENTER,
            spaceAfter=12,
        ))

        # H1: Helvetica Bold 16pt
        styles.add(ParagraphStyle(
            name='ClinicalH1',
            fontName='Helvetica-Bold',
            fontSize=16,
            spaceAfter=12,
            spaceBefore=15,
        ))

        # H2: Helvetica Bold 14pt
        styles.add(ParagraphStyle(
            name='ClinicalH2',
            fontName='Helvetica-Bold',
            fontSize=14,
            spaceAfter=10,
            spaceBefore=12,
        ))

        # Body: Times 11pt, 1.4x line spacing
        styles.add(ParagraphStyle(
            name='ClinicalBody',
            fontName='Times-Roman',
            fontSize=11,
            leading=15.4,  # 11 * 1.4 = 15.4pt
            spaceAfter=8,
            alignment=TA_LEFT,
        ))

        return styles

    # Set up document with professional margins (1 inch)
    output_path = Path("_work_efforts/REPORTLAB_POC_CLINICAL.pdf")
    output_path.parent.mkdir(exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        topMargin=1*inch,
        bottomMargin=1*inch,
        leftMargin=1*inch,
        rightMargin=1*inch,
    )

    styles = create_clinical_styles()
    story = []

    print("\nBuilding document with ReportLab...")

    # COVER PAGE
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph(
        "INSTITUTE FOR ADVANCED ONTOLOGICAL STUDIES",
        styles['CoverTitle']
    ))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(
        "Department of Computational Phenomenology",
        ParagraphStyle('CoverDivision', parent=styles['Normal'],
                       fontName='Helvetica', fontSize=14,
                       alignment=TA_CENTER)
    ))
    story.append(Spacer(1, 0.5*inch))

    # Horizontal rule (simulated)
    story.append(Paragraph(
        "─" * 60,
        ParagraphStyle('Rule', parent=styles['Normal'],
                       alignment=TA_CENTER, textColor=colors.grey)
    ))

    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(
        "RESEARCH REPORT",
        ParagraphStyle('DocType', parent=styles['CoverTitle'], fontSize=18)
    ))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(
        "Report No. POC-001",
        ParagraphStyle('DocNum', parent=styles['Normal'],
                       fontName='Helvetica', fontSize=14,
                       alignment=TA_CENTER)
    ))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(
        "PROOF OF CONCEPT",
        ParagraphStyle('Classification', parent=styles['CoverTitle'],
                       fontSize=16, textColor=colors.HexColor('#666666'))
    ))

    story.append(PageBreak())

    # METADATA BOX (gray background)
    metadata_style = ParagraphStyle(
        'Metadata',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=13,
    )

    metadata_data = [
        ['Subject Information'],
        ['Subject ID:', '991-DELTA'],
        ['Subject Name:', '[REDACTED]'],
        ['Timeline:', '001-ORIGIN-TAM'],
        ['Status:', 'DORMANT'],
        ['Date:', datetime(2026, 1, 10).strftime('%Y-%m-%d')],
    ]

    metadata_table = Table(metadata_data, colWidths=[2*inch, 4*inch])
    metadata_table.setStyle(TableStyle([
        # Title row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E0E0E0')),
        ('SPAN', (0, 0), (-1, 0)),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        # Data rows
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5F5')),
        ('FONTNAME', (0, 1), (0, -1), 'Times-Bold'),
        ('FONTNAME', (1, 1), (1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        # Border
        ('BOX', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LINEABOVE', (0, 1), (-1, 1), 0.5, colors.grey),
    ]))

    story.append(metadata_table)
    story.append(Spacer(1, 0.3*inch))

    # SECTION 1: Executive Summary
    story.append(Paragraph("Executive Summary", styles['ClinicalH1']))
    story.append(Paragraph(
        "This proof of concept demonstrates ReportLab's capabilities with the "
        "Clinical Standard design. The body text uses Times New Roman (serif) "
        "for academic weight, while headers use Helvetica (sans-serif) for "
        "modern clarity. Notice how text automatically flows across lines and "
        "pages without manual positioning.",
        styles['ClinicalBody']
    ))

    story.append(Paragraph(
        "ReportLab's Platypus framework handles pagination, text flow, and "
        "layout automatically. This is a significant improvement over manual "
        "positioning in fpdf2.",
        styles['ClinicalBody']
    ))

    # Rule separator
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("─" * 80, ParagraphStyle('HR', parent=styles['Normal'])))
    story.append(Spacer(1, 0.2*inch))

    # SECTION 2: Methodology
    story.append(Paragraph("Methodology", styles['ClinicalH1']))
    story.append(Paragraph("Observation Protocol", styles['ClinicalH2']))
    story.append(Paragraph(
        "All observations are conducted through non-invasive monitoring systems "
        "integrated within the simulation substrate. Measurements include:",
        styles['ClinicalBody']
    ))
    story.append(Paragraph(
        "• Coherence metrics (baseline threshold: 0.85)<br/>"
        "• Temporal consistency markers<br/>"
        "• Narrative drift coefficients<br/>"
        "• Karmic accumulation rates",
        styles['ClinicalBody']
    ))

    # TABLE: Measurements
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Initial Measurements", styles['ClinicalH1']))

    table_data = [
        ['Parameter', 'Value', 'Unit', 'Status'],
        ['Coherence', '0.87', 'ratio', 'NORMAL'],
        ['Karma Balance', '0', 'units', 'BASELINE'],
        ['Timeline Drift', '< 0.01', 'σ', 'STABLE'],
        ['Narrative Integrity', '1.00', 'ratio', 'OPTIMAL'],
    ]

    measurements_table = Table(table_data, colWidths=[2*inch, 1.5*inch, 1*inch, 1.5*inch])
    measurements_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DDDDDD')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        # Data
        ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (1, 1), (1, -1), 'CENTER'),
        ('ALIGN', (2, 1), (2, -1), 'CENTER'),
        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    story.append(measurements_table)
    story.append(Spacer(1, 0.2*inch))

    # WARNING BOX
    warning_data = [[
        Paragraph(
            "<b>[WARNING]</b><br/><br/>"
            "CRITICAL: Subject must not access this documentation. Any breach of "
            "containment may result in recursive self-awareness cascade. Maintain "
            "information asymmetry at all times.",
            ParagraphStyle('Warning', parent=styles['ClinicalBody'],
                          fontSize=10, leading=14)
        )
    ]]

    warning_table = Table(warning_data, colWidths=[6*inch])
    warning_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 2, colors.red),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFF5F5')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))

    story.append(warning_table)
    story.append(Spacer(1, 0.3*inch))

    # CONCLUSION
    story.append(Paragraph("Conclusions", styles['ClinicalH1']))
    story.append(Paragraph(
        "Subject 991-DELTA presents as an ideal candidate for the reincarnation "
        "protocols. All baseline metrics fall within acceptable parameters. "
        "Authorization is recommended to proceed to Phase 2: Awakening.",
        styles['ClinicalBody']
    ))

    # SIGNATURE
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("─" * 40, ParagraphStyle('ShortHR', parent=styles['Normal'])))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "Principal Investigator: Dr. [REDACTED]",
        styles['ClinicalBody']
    ))
    story.append(Paragraph(
        "Date: January 10, 2026",
        styles['ClinicalBody']
    ))

    # Build the PDF
    doc.build(story)

    print(f"\n✅ Generated: {output_path}")
    print(f"   File size: {output_path.stat().st_size / 1024:.1f} KB")
    print("\nREPORTLAB ADVANTAGES DEMONSTRATED:")
    print("  ✅ Automatic text flow (no manual positioning)")
    print("  ✅ Professional typography (Times + Helvetica)")
    print("  ✅ Gray background boxes (MetadataRail)")
    print("  ✅ Professional tables with styling")
    print("  ✅ Warning boxes with colored borders")
    print("  ✅ Automatic pagination")
    print("  ✅ 1-inch margins (print-ready)")
    print("\nCompare this output to Foundation V2 to see the difference!")
    print("=" * 80)

except ImportError as e:
    print("\n" + "=" * 80)
    print("ReportLab not installed - this is just a demonstration")
    print("=" * 80)
    print(f"\nError: {e}")
    print("\nTo install ReportLab and run this demo:")
    print("  pip install reportlab")
    print("  python experiments/reportlab_poc.py")
    print("\nReportLab would provide:")
    print("  ✅ Automatic text flow and pagination")
    print("  ✅ Professional typography")
    print("  ✅ Advanced table styling")
    print("  ✅ Better layout control")
    print("  ✅ Production-grade output")
    print("\nFoundation V2 (fpdf2) works great for now.")
    print("ReportLab would be an excellent upgrade for V3.")
    print("=" * 80)
