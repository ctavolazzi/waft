"""
Evolving Story Demo - Demonstrate story evolution with WAFT agents.

Shows how stories evolve over time through agent-directed narrative decisions.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.core.agent import AgentConfig
from src.waft.core.agent.story_director import StoryDirector
from src.waft.evolution.evolving_story import EvolvingStory


async def main():
    """Run evolving story demo."""
    print("=" * 80)
    print("Evolving Story Demo - WAFT Auto-Directed Narrative")
    print("=" * 80)
    print()

    # Initial story seed
    seed_text = """
    Alice discovered a mysterious door in her basement. The door was old and wooden,
    with strange symbols carved into its surface. She had never noticed it before,
    despite living in the house for years. Curiosity overcame caution, and she reached
    for the handle. The door creaked open, revealing darkness beyond.
    """

    print("📖 Initial Story Seed:")
    print(seed_text.strip())
    print()

    # Create evolving story from seed
    print("🌱 Creating evolving story from seed...")
    story = EvolvingStory.from_seed(seed_text=seed_text, title="The Basement Door")

    print(f"✅ Story created: {story.story_id}")
    print(f"   Title: {story.title}")
    print(f"   Characters: {len(story.state.characters)}")
    print(f"   Initial events: {len(story.state.timeline)}")
    print()

    # Create story director agent
    print("🎭 Creating Story Director agent...")
    director = StoryDirector(
        config=AgentConfig(
            role="Story Director",
            goal="Guide narrative evolution with compelling plot developments",
            backstory="A creative agent that makes narrative decisions to evolve stories",
        ),
        project_path=Path.cwd(),
        story=story,
    )

    print(f"✅ Director created: {director.state.agent_id}")
    print()

    # Evolve story over multiple generations
    num_generations = 5
    print(f"🔄 Evolving story over {num_generations} generations...")
    print()

    for generation in range(num_generations):
        print(f"--- Generation {generation + 1} ---")

        # Run OODA cycle
        try:
            decision = await director.evolve_story()

            print(f"✅ Decision made: {decision.decision_type.value}")
            print(f"   Description: {decision.description}")
            if decision.character:
                print(f"   Character: {decision.character}")
            print(f"   Confidence: {decision.confidence:.2f}")
            print()

            # Generate PDF snapshot
            pdf_path = story.generate_pdf(generation=story.state.generation, open_pdf=False)
            print(f"📄 PDF generated: {pdf_path}")
            print()

            # Save state
            state_path = story.save_state()
            print(f"💾 State saved: {state_path}")
            print()

        except Exception as e:
            print(f"❌ Error in generation {generation + 1}: {e}")
            import traceback

            traceback.print_exc()
            break

    # Final summary
    print("=" * 80)
    print("📊 Final Story Summary")
    print("=" * 80)
    print(story.get_summary())
    print()
    print(f"📈 Evolution History: {len(story.evolution_history)} decisions")
    print(f"🎯 Coherence Score: {story.state.coherence_score:.2f}")
    print(f"👥 Characters: {', '.join(story.state.characters.keys())}")
    print(f"📝 Total Events: {len(story.state.timeline)}")
    print()
    print("✅ Demo complete!")
    print(f"   Story directory: _stories/{story.story_id}/")
    print("   Check the PDFs to see how the story evolved!")


if __name__ == "__main__":
    asyncio.run(main())
