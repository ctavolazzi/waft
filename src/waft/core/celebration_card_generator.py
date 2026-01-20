"""
Celebration Card Generator - One-Page Creative Celebration PDFs

Creates beautiful, certificate-style one-page celebration cards with:
- Large celebratory typography
- Visual decorative elements
- Colorful, joyful design
- Guaranteed single-page output
"""

from datetime import datetime
from html import escape
from pathlib import Path

from weasyprint import HTML


class CelebrationCardGenerator:
    """Generates one-page celebration cards with creative design."""

    def __init__(self):
        """Initialize the celebration card generator."""
        pass

    def generate(
        self,
        achievement: str,
        message: str | None = None,
        output_path: Path | None = None,
        timestamp: str | None = None,
    ) -> Path:
        """
        Generate a one-page celebration card PDF.

        Args:
            achievement: What was accomplished
            message: Optional celebration message
            output_path: Where to save the PDF
            timestamp: Optional timestamp (defaults to now)

        Returns:
            Path to generated PDF
        """
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if message is None:
            message = "This is a moment worth celebrating! Take time to acknowledge this achievement and feel the joy of success."

        # Generate HTML with creative design
        html_content = self._create_celebration_html(achievement, message, timestamp)

        # Generate PDF
        if output_path is None:
            safe_achievement = "".join(
                c if c.isalnum() or c in (" ", "-", "_") else "" for c in achievement
            )
            safe_achievement = safe_achievement.replace(" ", "_")[:40]
            timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = Path(
                f"_pyrite/celebrations/celebration_{safe_achievement}_{timestamp_file}.pdf"
            )

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate PDF with WeasyPrint
        HTML(string=html_content).write_pdf(
            str(output_path), presentational_hints=True, optimize_images=True
        )

        return output_path

    def _create_celebration_html(self, achievement: str, message: str, timestamp: str) -> str:
        """Create HTML for celebration card with creative design."""

        # Escape HTML and split message into paragraphs if needed
        achievement_escaped = escape(achievement)
        message_escaped = escape(message)
        message_paragraphs = [p.strip() for p in message_escaped.split("\n\n") if p.strip()]
        if not message_paragraphs:
            message_paragraphs = [message_escaped]

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>🎉 Celebration: {achievement} 🎉</title>
    <style>
        @page {{
            size: letter;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            width: 100%;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-family: 'Georgia', 'Times New Roman', serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px;
            position: relative;
            overflow: hidden;
        }}
        
        /* Decorative corner elements */
        body::before,
        body::after {{
            content: '🎉';
            position: absolute;
            font-size: 80px;
            opacity: 0.15;
            z-index: 0;
        }}
        
        body::before {{
            top: 20px;
            left: 20px;
        }}
        
        body::after {{
            bottom: 20px;
            right: 20px;
            transform: rotate(180deg);
        }}
        
        /* Main card container */
        .celebration-card {{
            background: #ffffff;
            border-radius: 20px;
            padding: 60px 50px;
            max-width: 700px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            position: relative;
            z-index: 1;
            border: 8px solid #ffd700;
            border-style: double;
        }}
        
        /* Decorative border pattern */
        .celebration-card::before {{
            content: '';
            position: absolute;
            top: -4px;
            left: -4px;
            right: -4px;
            bottom: -4px;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #ffe66d, #ff6b6b);
            border-radius: 20px;
            z-index: -1;
            opacity: 0.3;
        }}
        
        /* Celebration emoji header */
        .celebration-emoji {{
            text-align: center;
            font-size: 80px;
            line-height: 1;
            margin-bottom: 20px;
            animation: bounce 2s infinite;
        }}
        
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
        }}
        
        /* Main title */
        .celebration-title {{
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
            line-height: 1.2;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        /* Achievement text */
        .achievement-text {{
            text-align: center;
            font-size: 28px;
            color: #667eea;
            font-weight: 600;
            margin-bottom: 40px;
            line-height: 1.3;
            padding: 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            border-left: 6px solid #667eea;
        }}
        
        /* Message section */
        .celebration-message {{
            font-size: 18px;
            line-height: 1.8;
            color: #34495e;
            text-align: center;
            margin-bottom: 40px;
        }}
        
        .celebration-message p {{
            margin-bottom: 15px;
        }}
        
        .celebration-message p:last-child {{
            margin-bottom: 0;
        }}
        
        /* Decorative divider */
        .divider {{
            text-align: center;
            font-size: 30px;
            color: #ffd700;
            margin: 30px 0;
            line-height: 1;
        }}
        
        /* Timestamp */
        .timestamp {{
            text-align: center;
            font-size: 14px;
            color: #7f8c8d;
            font-style: italic;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px dashed #bdc3c7;
        }}
        
        /* Signature line */
        .signature {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #ecf0f1;
        }}
        
        .signature-text {{
            font-size: 16px;
            color: #95a5a6;
            font-style: italic;
        }}
        
        /* Decorative stars */
        .stars {{
            text-align: center;
            font-size: 24px;
            color: #ffd700;
            margin: 20px 0;
            letter-spacing: 10px;
        }}
        
        /* Responsive adjustments for PDF */
        @media print {{
            body {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }}
            
            .celebration-card {{
                page-break-inside: avoid;
                break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="corner-emoji top-left">🎉</div>
    <div class="corner-emoji bottom-right">🎉</div>
    
    <div class="celebration-card">
        <div class="celebration-emoji">🎉</div>
        
        <div class="celebration-title">CELEBRATION</div>
        
        <div class="stars">✦ ✦ ✦</div>
        
        <div class="achievement-text">{achievement_escaped}</div>
        
        <div class="divider">━━━━━━━━━━━━━━━━━━━━</div>
        
        <div class="celebration-message">
            {"".join(f"<p>{paragraph}</p>" for paragraph in message_paragraphs)}
        </div>
        
        <div class="divider">━━━━━━━━━━━━━━━━━━━━</div>
        
        <div class="stars">✦ ✦ ✦</div>
        
        <div class="signature">
            <div class="signature-text">Generated with WAFT Celebration System</div>
        </div>
        
        <div class="timestamp">
            {timestamp}
        </div>
    </div>
</body>
</html>"""

        return html
