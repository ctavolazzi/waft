"""
Creative Example: Poker Story Generator

Generate dramatic poker scenes with narrative context.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.templates.typst.poker import PokerGame


def dramatic_showdown():
    """Create a dramatic poker showdown scene."""
    print("🎭 Generating dramatic poker showdown...")

    game = PokerGame("The Final Showdown", card_format="large")

    # The villain - confident with pocket aces
    game.add_player("The Count", ["AS", "AD"])

    # The hero - underdog with pocket kings
    game.add_player("The Hero", ["KS", "KD"])

    # Dramatic community cards
    game.set_community_cards(["AC", "KH", "QC", "10S", "9H"])

    # Add narrative
    game.add_content("""
== The Final Showdown

The smoke-filled room fell silent as the final cards were dealt.
The Count smiled confidently, knowing he held the best starting hand
in poker - pocket aces. But The Hero remained stoic, calculating
the odds, reading the tells.

*Pre-Flop*: The Count raised aggressively. The Hero called, sensing
something in the Count's demeanor.

*The Flop*: AC, KH, QC - The Count's smile widened. He had top set.
But The Hero saw opportunity - a straight draw, and the king gave
him a pair.

*The Turn*: 10S - The Hero's heart raced. He now had a straight!
But the Count still had the best hand with three aces.

*The River*: 9H - The Hero's straight was complete, but the Count
still had the winning hand with four aces!

The Count pushed all his chips forward with a triumphant laugh.
The Hero, knowing the odds were against him, made the call anyway.
Sometimes, poker is about more than just the cards.

*Outcome*: The Count wins with four aces - the second-best possible
hand in poker. The Hero's straight was strong, but not strong enough.
    """)

    game.include_rules()
    output = game.generate(Path("_temp_pdf_examples/poker_story_showdown.pdf"))
    print(f"✅ Generated: {output}")
    return output


def historical_recreation():
    """Recreate a famous historical poker hand."""
    print("📜 Generating historical hand recreation...")

    game = PokerGame("WSOP 2003: Moneymaker vs Farha", card_format="medium")

    # Chris Moneymaker (amateur)
    game.add_player("Chris Moneymaker", ["5S", "4D"])

    # Sam Farha (pro)
    game.add_player("Sam Farha", ["JS", "10H"])

    # The famous board
    game.set_community_cards(["4S", "5H", "QS", "7S", "KS"])

    game.add_content("""
== The Hand That Changed Poker

This is the hand that launched the poker boom. Chris Moneymaker,
an amateur accountant from Tennessee, faced off against professional
Sam Farha in the 2003 WSOP Main Event final table.

*The Situation*: Moneymaker was the underdog, but he played with
fearless aggression. Farha, the experienced pro, tried to outplay
the amateur.

*The Bluff*: With 5S-4D, Moneymaker made a massive all-in bluff on
the river. Farha, holding JS-10H with a pair of jacks, had to make
a decision for his tournament life.

*The Call*: Farha folded, and Moneymaker won the pot. This hand
became legendary, showing that amateurs could compete with pros.

*The Impact*: Moneymaker went on to win the Main Event, and the
poker boom began. Online poker exploded, and millions of new players
entered the game.
    """)

    output = game.generate(Path("_temp_pdf_examples/poker_historical.pdf"))
    print(f"✅ Generated: {output}")
    return output


def hand_quiz():
    """Create a poker hand quiz."""
    print("📝 Generating poker hand quiz...")

    # Question 1: What's the best hand?
    game1 = PokerGame("Quiz: What's the Best Hand?", card_format="small")
    game1.add_player("Hand A", ["AS", "KS", "QS", "JS", "10S"])  # Royal flush
    game1.add_player("Hand B", ["AS", "AD", "AH", "AC", "KD"])  # Four aces
    game1.add_player("Hand C", ["KS", "KD", "KH", "KC", "QS"])  # Four kings
    game1.add_content("""
== Question 1: What's the Best Hand?

Compare these three hands. Which one wins?

*Answer*: Hand A wins with a Royal Flush - the best possible hand
in poker. Even though Hand B has four aces (the second-best hand),
a Royal Flush always beats four of a kind.
    """)
    game1.generate(Path("_temp_pdf_examples/poker_quiz_1.pdf"))

    # Question 2: What should you do?
    game2 = PokerGame("Quiz: What Should You Do?", card_format="medium")
    game2.add_player("You", ["AS", "KH"])
    # Show card backs for unknown villain cards using "back" identifier
    game2.add_player("Villain (Unknown)", ["back", "back"])
    game2.set_community_cards(["AC", "AD", "AH", "KS", "QS"])
    game2.add_content("""
== Question 2: What Should You Do?

You have AS-KH. The board is AC-AD-AH-KS-QS.

You have four aces - the second-best possible hand! The only hand
that beats you is a Royal Flush (10S-JS-QS-KS-AS).

Villain goes all-in. What should you do?

*Answer*: You should call! You have an extremely strong hand.
The only way you lose is if villain has the one specific hand
that beats you. This is an easy call.
    """)
    game2.generate(Path("_temp_pdf_examples/poker_quiz_2.pdf"))

    print("✅ Generated quiz PDFs")
    return [
        Path("_temp_pdf_examples/poker_quiz_1.pdf"),
        Path("_temp_pdf_examples/poker_quiz_2.pdf"),
    ]


def tournament_final_table():
    """Create a tournament final table visualization."""
    print("🏆 Generating tournament final table...")

    game = PokerGame("WSOP Final Table", card_format="medium")

    # Final table players
    game.add_player("Chip Leader", ["AS", "KH"])
    game.add_player("Short Stack", ["QD", "JD"])
    game.add_player("Middle Stack", ["10C", "9C"])
    game.add_player("Aggressive Player", ["2S", "3H"])

    game.set_community_cards(["AC", "AD", "AH", "KS", "QS"])

    game.add_content("""
== Final Table Action

*Chip Leader*: Playing tight, waiting for good spots
*Short Stack*: Desperate, looking for any opportunity
*Middle Stack*: Balanced approach, picking spots carefully
*Aggressive Player*: Pushing the action, building pots

*The Hand*: Chip Leader raises with AS-KH. Short Stack shoves
all-in with QD-JD. Middle Stack folds. Aggressive Player folds.
Chip Leader calls.

*The Board*: AC-AD-AH-KS-QS

*Result*: Chip Leader wins with four aces, eliminating Short Stack.
The final table continues with three players remaining.
    """)

    output = game.generate(Path("_temp_pdf_examples/poker_tournament.pdf"))
    print(f"✅ Generated: {output}")
    return output


def main():
    """Generate all creative examples."""
    print("=" * 60)
    print("🎴 Creative Poker Visualization Examples")
    print("=" * 60)
    print()

    dramatic_showdown()
    print()

    historical_recreation()
    print()

    hand_quiz()
    print()

    tournament_final_table()
    print()

    print("=" * 60)
    print("✅ All creative examples generated!")
    print("=" * 60)
    print()
    print("📚 See CREATIVE_IDEAS_POKER.md for more ideas")


if __name__ == "__main__":
    main()
