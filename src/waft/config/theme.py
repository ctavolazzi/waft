"""Visual theme constants for Waft CLI output.

Centralizes all emoji and color definitions to ensure consistency
and make updates easier.
"""


class Emoji:
    """Emoji constants used throughout the CLI."""

    # Brand
    WAFT = "🌊"

    # Actions
    DICE = "🎲"
    SPARKLES = "✨"
    SUCCESS = "🎉"
    STAR = "⭐"

    # Resources
    INTEGRITY = "💎"
    INSIGHT = "✨"  # Same as SPARKLES
    CREDITS = "💰"

    # Status
    CHECK = "✅"
    WARNING = "⚠️"
    ERROR = "❌"
    INFO = "ℹ️"

    # Science
    MICROSCOPE = "🔬"
    TELESCOPE = "🔭"
    DNA = "🧬"

    # Game
    SWORD = "⚔️"
    SHIELD = "🛡️"
    SCROLL = "📜"
    BOOK = "📖"


class Color:
    """Rich console color constants."""

    # Status colors
    SUCCESS = "green"
    ERROR = "red"
    WARNING = "yellow"
    INFO = "cyan"

    # Emphasis
    TITLE = "bold cyan"
    SUBTITLE = "bold"
    DIM = "dim"
    HIGHLIGHT = "bold yellow"

    # Data types
    NUMBER = "cyan"
    STRING = "green"
    BOOLEAN = "magenta"

    # UI elements
    BORDER = "blue"
    HEADER = "bold white"
    FOOTER = "dim white"


class Style:
    """Additional styling constants."""

    # Box styles for panels
    PANEL_BORDER = "rounded"
    TABLE_BORDER = "simple"

    # Text formatting
    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"
