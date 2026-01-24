#!/usr/bin/env python3
"""
Git-Gud Digital Card Generator

Creates HTML cards from the Git-Gud card game data.
Can be extended for other card games (like Teleport Massive).
"""

import json
from pathlib import Path
from html import escape

# Git-Gud card definitions
GIT_GUD_CARDS = [
    {
        "name": "Introduce bug",
        "color": "#E74C3C",  # Red
        "rules": "Introduce a bug in another players repo. The other player must add 1 to their bugs.\n\nThe next Player can add the same card to add more bugs to the following Player"
    },
    {
        "name": "Merge",
        "color": "#9B59B6",  # Purple
        "rules": "You hand over one of your cards of choice to another player of choice."
    },
    {
        "name": "Fix bug",
        "color": "#3498DB",  # Blue
        "rules": "Guess a number from 1 to 6 roll a die, if you hit the number remove 2 bugs.\nIf your guess is off by one, remove 1 bug"
    },
    {
        "name": "Rebase",
        "color": "#27AE60",  # Green
        "rules": "You get a card at random of a player of choice."
    },
    {
        "name": "Squash commits",
        "color": "#E74C3C",  # Red
        "rules": "Remove one card of choice.\n\nTake one additional card."
    },
    {
        "name": "Commit",
        "color": "#F39C12",  # Orange
        "rules": "Guess even or uneven, roll a die, if your guess is correct, remove 1 bug, else add 2 bugs\n\nThis card also can be used to avoid \"Introduce bug\" if laid immediately without hesitation. This however invalidates the primary intention of this card."
    },
    {
        "name": "Retire repo",
        "color": "#9B59B6",  # Purple
        "rules": "You retire your repo. The next Player adds 1 to their bugs.\n\nThis card is not stackable."
    },
    {
        "name": "Pair programming",
        "color": "#27AE60",  # Green  
        "rules": "Together with a player of choice each roll a die. If the eye-count differs by more than 1 add 1 bug else remove 2 bugs"
    },
    {
        "name": "Clone repo",
        "color": "#1ABC9C",  # Cyan
        "rules": "You start from a fresh clone.\n\nRoll a die and the eye-count is the number of cards you can replace."
    }
]


def generate_card_html(card: dict, index: int) -> str:
    """Generate HTML for a single Git-Gud style card."""
    name = escape(card["name"])
    rules = escape(card["rules"]).replace("\n\n", "</p><p>").replace("\n", "<br>")
    color = card["color"]
    
    return f'''
    <div class="card" data-index="{index}">
        <div class="card-header" style="background-color: {color};">
            <h2>{name}</h2>
        </div>
        <div class="card-body">
            <p>{rules}</p>
        </div>
    </div>
    '''


def generate_deck_html(cards: list[dict], title: str = "Git Gud Cards") -> str:
    """Generate HTML page with all cards in a printable grid."""
    cards_html = '\n'.join(generate_card_html(card, i) for i, card in enumerate(cards))
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e;
            padding: 20px;
            min-height: 100vh;
        }}
        
        h1 {{
            color: #fff;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5rem;
        }}
        
        .deck-info {{
            color: #888;
            text-align: center;
            margin-bottom: 20px;
        }}
        
        .deck-container {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            max-width: 900px;
            margin: 0 auto;
        }}
        
        .card {{
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transition: transform 0.2s, box-shadow 0.2s;
            cursor: pointer;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        }}
        
        .card-header {{
            padding: 20px;
            text-align: center;
        }}
        
        .card-header h2 {{
            color: white;
            font-size: 1.4rem;
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}
        
        .card-body {{
            padding: 20px;
            min-height: 150px;
        }}
        
        .card-body p {{
            font-size: 0.9rem;
            line-height: 1.5;
            color: #333;
            margin-bottom: 10px;
        }}
        
        .card-body p:last-child {{
            margin-bottom: 0;
        }}
        
        /* Print styles for 3x3 card sheet */
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            h1, .deck-info {{
                display: none;
            }}
            
            .deck-container {{
                gap: 2mm;
                max-width: none;
                width: 100%;
            }}
            
            .card {{
                box-shadow: none;
                border: 1px solid #000;
                page-break-inside: avoid;
            }}
            
            .card:hover {{
                transform: none;
            }}
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .deck-container {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        
        @media (max-width: 480px) {{
            .deck-container {{
                grid-template-columns: 1fr;
            }}
        }}
        
        footer {{
            text-align: center;
            color: #666;
            margin-top: 40px;
            font-size: 0.9rem;
        }}
        
        footer a {{
            color: #3498DB;
        }}
    </style>
</head>
<body>
    <h1>🎮 {title}</h1>
    <p class="deck-info">9 unique cards • Print 12 copies for full 108-card deck • Click cards to flip</p>
    
    <div class="deck-container">
        {cards_html}
    </div>
    
    <footer>
        <p>Git Gud by Jeff Cigrand • CC BY-NC-SA 4.0</p>
        <p><a href="https://github.com/ctavolazzi/Git-Gud">View on GitHub</a></p>
    </footer>
    
    <script>
        // Simple card flip animation
        document.querySelectorAll('.card').forEach(card => {{
            card.addEventListener('click', () => {{
                card.style.transform = 'rotateY(360deg)';
                setTimeout(() => {{
                    card.style.transform = '';
                }}, 500);
            }});
        }});
    </script>
</body>
</html>
'''


def main():
    """Generate Git-Gud digital cards."""
    output_dir = Path(__file__).parent
    output_path = output_dir / "git_gud_digital.html"
    
    print("Generating Git-Gud digital cards...")
    print(f"Cards: {len(GIT_GUD_CARDS)}")
    
    html = generate_deck_html(GIT_GUD_CARDS, "Git Gud")
    output_path.write_text(html, encoding='utf-8')
    
    print(f"Generated: {output_path}")
    print(f"\nOpen in browser: file://{output_path.absolute()}")
    
    # Also export card data as JSON for other uses
    json_path = output_dir / "git_gud_cards.json"
    json_path.write_text(json.dumps(GIT_GUD_CARDS, indent=2), encoding='utf-8')
    print(f"Card data: {json_path}")


if __name__ == "__main__":
    main()
