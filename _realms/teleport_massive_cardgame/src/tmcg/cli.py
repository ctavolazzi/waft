"""
CLI for Teleport Massive Card Game.

Usage:
    tmcg generate --input data/cards.csv --output output/deck.html
    tmcg preview --input data/cards.csv
    tmcg stats --input data/cards.csv
    tmcg list-art --art-dir assets/art
"""

import argparse
import sys
from pathlib import Path

from .generators.card_generator import CardGenerator
from .generators.deck_builder import DeckBuilder
from .generators.art_generator import ArtGenerator, ArtStyle, ArtSize
from .renderers.html_renderer import HTMLRenderer


def cmd_generate(args):
    """Generate HTML from card data."""
    input_path = Path(args.input)
    output_path = Path(args.output)
    art_dir = Path(args.art_dir) if args.art_dir else None
    
    print(f"Loading cards from: {input_path}")
    
    builder = DeckBuilder(art_dir=art_dir)
    deck = (builder
        .name(args.name or input_path.stem)
        .load_file(input_path)
        .build())
    
    if art_dir:
        print(f"Loading art from: {art_dir}")
        deck = builder.with_art(art_dir).build()
    
    print(f"Loaded {deck.size} cards ({len(deck.unique_cards_list)} unique)")
    
    renderer = HTMLRenderer(include_stats=not args.no_stats)
    renderer.render_deck_to_file(deck, output_path)
    
    print(f"Generated: {output_path}")
    print(f"Open: file://{output_path.absolute()}")


def cmd_preview(args):
    """Preview deck in terminal."""
    input_path = Path(args.input)
    
    builder = DeckBuilder()
    deck = builder.load_file(input_path).build()
    
    print(f"\n{deck.name}")
    print("=" * 40)
    print(f"Total: {deck.size} cards ({len(deck.unique_cards_list)} unique)")
    print()
    
    stats = deck.stats
    print("Statistics:")
    print(f"  Creatures: {stats.creatures}")
    print(f"  Spells: {stats.spells}")
    print(f"  Lands: {stats.lands}")
    print(f"  Artifacts: {stats.artifacts}")
    print(f"  Avg CMC: {stats.average_cmc}")
    print()
    
    print("Cards:")
    for card in deck.unique_cards_list:
        count = deck.card_counts[card.name]
        print(f"  {count}x {card}")
    print()


def cmd_stats(args):
    """Show deck statistics."""
    input_path = Path(args.input)
    
    builder = DeckBuilder()
    deck = builder.load_file(input_path).build()
    stats = deck.stats
    
    print(f"\nDeck Statistics: {deck.name}")
    print("=" * 40)
    print(f"Total Cards: {stats.total_cards}")
    print(f"Unique Cards: {stats.unique_cards}")
    print()
    print("By Type:")
    print(f"  Creatures: {stats.creatures}")
    print(f"  Spells: {stats.spells}")
    print(f"  Lands: {stats.lands}")
    print(f"  Artifacts: {stats.artifacts}")
    print()
    print("By Rarity:")
    for rarity, count in sorted(stats.rarity_distribution.items()):
        print(f"  {rarity.capitalize()}: {count}")
    print()
    print(f"Average CMC: {stats.average_cmc}")
    print()
    print("Mana Curve:")
    for cmc, count in stats.cmc_curve.items():
        bar = "█" * count
        print(f"  {cmc}: {bar} ({count})")
    print()
    
    # Validation
    is_valid, errors = deck.is_valid()
    if is_valid:
        print("✅ Deck is valid")
    else:
        print("❌ Deck validation errors:")
        for error in errors:
            print(f"  - {error}")


def cmd_list_art(args):
    """List available art files."""
    art_dir = Path(args.art_dir)
    
    if not art_dir.exists():
        print(f"Art directory not found: {art_dir}")
        sys.exit(1)
    
    generator = ArtGenerator(art_dir)
    stats = generator.get_art_stats()
    
    print(f"\nArt Directory: {art_dir}")
    print("=" * 40)
    print(f"Total Files: {stats['total_files']}")
    print(f"Total Size: {stats['total_size_kb']} KB")
    print()
    print("Available Art:")
    for name in sorted(generator.list_available_art()):
        print(f"  ✓ {name}")


def cmd_art_request(args):
    """Generate art request for PixelLab."""
    art_dir = Path(args.art_dir) if args.art_dir else Path("assets/art")
    generator = ArtGenerator(art_dir)
    
    style = ArtStyle(args.style) if args.style else ArtStyle.CHARACTER
    size = ArtSize(int(args.size)) if args.size else ArtSize.LARGE
    
    request = generator.create_request(
        card_name=args.name,
        description=args.description,
        style=style,
        size=size,
    )
    
    params = generator.get_pixellab_params(request)
    
    print(f"\nPixelLab Request for: {args.name}")
    print("=" * 40)
    print(f"Style: {style.value}")
    print(f"Size: {size.value}px")
    print()
    print("Parameters:")
    for key, value in params.items():
        print(f"  {key}: {value}")
    print()
    print("Use these parameters with PixelLab MCP tools:")
    if style == ArtStyle.CHARACTER:
        print("  Tool: user-pixellab-create_character")
    else:
        print("  Tool: user-pixellab-create_map_object")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="tmcg",
        description="Teleport Massive Card Game CLI"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate HTML from card data")
    gen_parser.add_argument("--input", "-i", required=True, help="Input file (CSV/JSON)")
    gen_parser.add_argument("--output", "-o", default="deck.html", help="Output HTML file")
    gen_parser.add_argument("--art-dir", "-a", help="Directory containing art files")
    gen_parser.add_argument("--name", "-n", help="Deck name")
    gen_parser.add_argument("--no-stats", action="store_true", help="Don't include stats")
    gen_parser.set_defaults(func=cmd_generate)
    
    # Preview command
    preview_parser = subparsers.add_parser("preview", help="Preview deck in terminal")
    preview_parser.add_argument("--input", "-i", required=True, help="Input file")
    preview_parser.set_defaults(func=cmd_preview)
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show deck statistics")
    stats_parser.add_argument("--input", "-i", required=True, help="Input file")
    stats_parser.set_defaults(func=cmd_stats)
    
    # List art command
    art_parser = subparsers.add_parser("list-art", help="List available art")
    art_parser.add_argument("--art-dir", "-a", default="assets/art", help="Art directory")
    art_parser.set_defaults(func=cmd_list_art)
    
    # Art request command
    req_parser = subparsers.add_parser("art-request", help="Generate PixelLab request")
    req_parser.add_argument("--name", "-n", required=True, help="Card name")
    req_parser.add_argument("--description", "-d", required=True, help="Art description")
    req_parser.add_argument("--style", "-s", choices=["character", "object", "spell", "landscape"])
    req_parser.add_argument("--size", choices=["32", "48", "64", "96"], default="64")
    req_parser.add_argument("--art-dir", "-a", help="Art directory")
    req_parser.set_defaults(func=cmd_art_request)
    
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
