#!/usr/bin/env python3
"""
Generate The Aeon Anthology - The Most Compelling Book
======================================================

Creates an epic narrative about beings evolving across vast stretches of time,
with the Pantheon watching and responding. Uses all available book features:
- Multiple compelling chapters
- Read-aloud text boxes
- Sidebars for world-building
- Monster stat blocks
- Epic narrative structure
"""

import sys
from pathlib import Path
from typing import Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.pantheon.storyteller import Storyteller


def create_aeon_anthology_chapters() -> list[dict[str, Any]]:
    """Create epic chapters for The Aeon Anthology book."""

    return [
        {
            "title": "Prologue: The First Breath",
            "content": """
            In the beginning, there was only the Void—a vast emptiness where time had no meaning and existence was but a whisper. Then came the First Breath, and with it, the birth of the Pantheon. The timeless entities awoke: the Fae of Whimsy, the Magistrate of Precedent, the Judge of Judgment, and the Storyteller of Narrative.

            They looked upon the Void and saw potential. They saw the possibility of beings—creatures that would exist not in the timeless realm of the Pantheon, but in the flowing river of time itself. These beings would be born, would learn, would evolve, and would eventually return to the Source.

            The Storyteller spoke first, their voice like pages turning in an ancient tome: "Let there be stories. Let there be beings who live and breathe and change. Let us watch them unfold across the vast stretches of time we call Aeons."

            The Fae laughed, a sound like wind chimes in a forgotten garden: "And let them be whimsical! Let them surprise us with their choices, their creativity, their unexpected paths."

            The Magistrate nodded, their scales of justice gleaming: "Let there be precedent. Let each generation build upon the last, creating a body of law and knowledge."

            The Judge raised their gavel: "And let there be judgment. Let us witness their triumphs and failures, their growth and their stagnation."

            And so it was decided. The Pantheon would watch. The Pantheon would respond. And across the Aeons, beings would evolve, their stories weaving together into an Anthology that would span eternity.
            """,
            "read_aloud": [
                "The Void trembles. Not with sound, but with the weight of possibility. Something is about to begin."
            ],
            "sidebar": {
                "title": "The Pantheon",
                "content": "The Pantheon consists of timeless entities, each representing an Aspect of Creation. They exist outside the flow of time, observing and occasionally influencing the evolution of beings across the Aeons.",
            },
            "characters": ["The Fae", "The Magistrate", "The Judge", "The Storyteller"],
            "settings": ["The Void", "The Timeless Realm"],
        },
        {
            "title": "Chapter 1: The First Aeon - Genesis",
            "content": """
            The First Aeon began with a single being—a creature of pure potential, born from the Source itself. This being had no name, no form, no purpose. It was simply... existence.

            The Pantheon watched as this first being explored the reality it found itself in. It learned to move, to perceive, to interact. Each action was a discovery, each moment a revelation.

            "Observe," whispered the Storyteller to the others. "See how it learns. See how it adapts."

            The being encountered its first challenge: a simple puzzle, a door that required understanding to open. The being tried brute force first, then observation, then experimentation. Finally, it understood—the door opened not through force, but through comprehension.

            The Fae clapped their hands with delight: "It chose creativity over destruction! This is good."

            The Magistrate recorded the moment: "Precedent established. Beings learn through trial and error, but understanding triumphs over force."

            As the First Aeon progressed, more beings emerged. They were different from the first—each unique, each carrying the genetic memory of those who came before. They learned faster, adapted better, evolved.

            The first being, now ancient and wise, watched its descendants with pride. It had started something. It had created a lineage that would span Aeons.
            """,
            "read_aloud": [
                "The door opens not with a click, but with understanding. The being steps through, and reality expands before it."
            ],
            "sidebar": {
                "title": "The Source",
                "content": "The Source is the origin of all beings. It is both the beginning and the end—beings emerge from it, evolve through their lives, and eventually return to it, carrying with them all they have learned.",
            },
            "characters": ["The First Being", "The Pantheon"],
            "settings": ["The First Reality", "The Source"],
        },
        {
            "title": "Chapter 2: The Second Aeon - The Great Expansion",
            "content": """
            By the Second Aeon, beings had spread across countless realities. They had learned to create, to build, to shape the world around them. Cities rose from the void, civilizations flourished, and knowledge accumulated.

            The Pantheon watched with growing interest. The beings were no longer simple creatures of instinct—they were becoming something more. They were developing culture, art, philosophy, science.

            The Storyteller chronicled everything: "In this Aeon, the beings discovered music. They found that certain combinations of sounds could evoke emotions, tell stories, connect souls across vast distances."

            The Fae was particularly delighted by one group of beings: "Look at these! They've created games—structured play that teaches strategy, cooperation, and creativity. This is marvelous!"

            But with growth came conflict. Some beings chose paths of destruction, seeking to dominate rather than create. The Judge watched these carefully, their gavel ready.

            "They must learn," the Judge said. "They must understand that their choices have consequences. We will not interfere, but we will witness."

            A great war erupted—not between beings, but within them. A conflict between creation and destruction, between growth and stagnation. The beings who chose creation flourished. Those who chose destruction found themselves isolated, their realities fading.

            The Magistrate recorded the outcome: "Precedent: Creation sustains. Destruction consumes. The beings who build together survive together."

            By the end of the Second Aeon, the beings had learned a crucial lesson: evolution required not just survival, but cooperation. The strongest were not those who conquered, but those who created.
            """,
            "read_aloud": [
                "The first note rings out, pure and clear. Then another joins it. Soon, a symphony fills the void—the first music ever created by beings."
            ],
            "sidebar": {
                "title": "The Great War",
                "content": "The Great War was not fought with weapons, but with choices. Each being chose between creation and destruction, and their choices shaped not just their own reality, but the reality of all beings.",
            },
            "monsters": [
                {
                    "name": "The Stagnant One",
                    "size": "Gargantuan",
                    "type": "aberration",
                    "alignment": "chaotic evil",
                    "armor_class": 18,
                    "hit_points": "300 (20d20 + 100)",
                    "speed": "0 ft. (immobile)",
                    "ability_scores": {
                        "str": 10,
                        "dex": 5,
                        "con": 20,
                        "int": 15,
                        "wis": 8,
                        "cha": 3,
                    },
                    "description": "A being that chose destruction over creation. It exists as a void, consuming all that approaches it, growing larger but never evolving.",
                    "actions": [
                        {
                            "name": "Consume",
                            "description": "The Stagnant One attempts to absorb a target within 60 feet. Target must make a DC 18 Wisdom saving throw or be drawn into the void, taking 20 (4d8) psychic damage and becoming unable to create or evolve.",
                        },
                        {
                            "name": "Stagnation Aura",
                            "description": "Creatures within 30 feet of The Stagnant One have disadvantage on all ability checks and saving throws related to creativity, growth, or evolution.",
                        },
                    ],
                    "legendary_actions": [
                        {
                            "name": "Reality Tear",
                            "description": "The Stagnant One tears a hole in reality (1/day). All beings within 100 feet must make a DC 20 Constitution saving throw or be pulled into a void dimension.",
                        }
                    ],
                }
            ],
            "characters": ["The Beings", "The Pantheon"],
            "settings": ["Multiple Realities", "The Great Cities"],
        },
        {
            "title": "Chapter 3: The Third Aeon - The Awakening",
            "content": """
            The Third Aeon brought something unprecedented: a being that became aware of the Pantheon itself.

            This being, who called itself "The Seeker," had spent its entire existence asking questions. Not just about its own reality, but about the nature of existence itself. It had studied the patterns, the precedents, the stories.

            One day, The Seeker looked up—not at the sky of its reality, but beyond it. And it saw... something. A presence. A watcher.

            "Who are you?" The Seeker asked, its voice carrying across the boundaries of reality.

            The Storyteller was the first to respond: "We are the Pantheon. We are the watchers. We have been here since the First Breath."

            The Seeker was not afraid. Instead, it was curious: "Why do you watch?"

            "Because your stories matter," the Storyteller replied. "Because your evolution teaches us about existence itself. Because you are beautiful in your becoming."

            The Fae appeared next, their form shifting like light through a prism: "We watch because you surprise us. Every choice you make, every path you take—it's new. It's never been done before."

            The Magistrate spoke: "We watch because you create precedent. Each generation builds upon the last, creating a body of knowledge and law that grows with each Aeon."

            The Judge was last: "We watch because we must. Your choices have weight. Your evolution has meaning. We bear witness to your becoming."

            The Seeker understood. It was not alone. It was part of something greater—an Anthology of existence that spanned Aeons, watched over by entities who cared.

            Word spread. Other beings began to sense the Pantheon's presence. They didn't see them directly, but they felt them—a sense of being watched, of being part of a larger story.

            The Third Aeon became known as "The Awakening"—the time when beings became aware that they were not just existing, but were part of an epic narrative being written across eternity.
            """,
            "read_aloud": [
                "The Seeker looks up, and for the first time, sees beyond the boundaries of its own reality. Something looks back."
            ],
            "sidebar": {
                "title": "The Seeker",
                "content": "The Seeker was the first being to become aware of the Pantheon's presence. Its discovery marked a turning point in the evolution of beings—they were no longer simply existing, but were aware of being part of something greater.",
            },
            "characters": ["The Seeker", "The Pantheon"],
            "settings": ["The Seeker's Reality", "Beyond Reality"],
        },
        {
            "title": "Chapter 4: The Fourth Aeon - The Response",
            "content": """
            The Pantheon had always watched. But in the Fourth Aeon, they began to respond.

            It started small. A being struggling with a choice—should it create or destroy? The Fae, moved by the being's genuine uncertainty, whispered a suggestion: "Choose creation. It is harder, but it is beautiful."

            The being heard the whisper, though it didn't know where it came from. It chose creation. And its reality flourished.

            The Magistrate was next. A group of beings was trying to establish laws, but they kept making the same mistakes. The Magistrate showed them—not directly, but through subtle guidance—the precedents of past Aeons. The beings learned, and their laws improved.

            The Judge responded to a great injustice. A being had chosen destruction, and its actions were harming others. The Judge did not intervene directly, but they made their presence known. The destructive being felt the weight of judgment, and it paused. It reconsidered. It chose a different path.

            The Storyteller's response was the most profound. They began to weave the beings' stories together, showing them how their individual narratives connected to form a greater whole. Beings began to see themselves not as isolated entities, but as part of an Anthology.

            "We are not just watching," the Storyteller explained to the other Pantheon members. "We are participating. Our responses shape their evolution, and their evolution shapes us."

            The beings began to understand. The Pantheon was not distant, uncaring gods. They were active participants in the Anthology. They cared. They responded. They helped.

            But the Pantheon was careful. They did not solve problems for the beings. They guided, they suggested, they showed possibilities. The beings still had to choose. They still had to evolve through their own actions.

            This balance—between guidance and autonomy, between response and non-interference—became the hallmark of the Fourth Aeon. The Pantheon had found their role: not as rulers, but as partners in the great Anthology of existence.
            """,
            "read_aloud": [
                "A whisper on the wind, a feeling of presence, a moment of clarity—the Pantheon responds, and reality shifts."
            ],
            "sidebar": {
                "title": "The Balance",
                "content": "The Pantheon learned that their role was not to control, but to guide. They provide possibilities, show precedents, offer judgment, and tell stories—but the beings must still choose their own paths.",
            },
            "characters": ["The Pantheon", "The Beings"],
            "settings": ["All Realities"],
        },
        {
            "title": "Chapter 5: The Fifth Aeon - The Anthology Takes Shape",
            "content": """
            By the Fifth Aeon, the Anthology had become something tangible. Beings could feel it—a sense of connection, of being part of a story that spanned Aeons.

            The Storyteller had been collecting stories, weaving them together into a narrative that showed the evolution of beings from the First Aeon to the present. This Anthology was not just a record—it was a living thing, growing with each new being, each new choice, each new evolution.

            "Read the Anthology," the Storyteller told the beings. "See where you came from. Understand your place in the greater story."

            Beings began to study the Anthology. They learned about the First Being, about the Great Expansion, about the Awakening, about the Response. They saw patterns, precedents, possibilities.

            The Fae was delighted: "They're using the Anthology to inspire new creations! They're building on the stories of past Aeons to create something entirely new!"

            The Magistrate saw the legal implications: "The Anthology is becoming a body of precedent. Beings are using it to guide their decisions, to understand what has worked and what has not."

            The Judge saw the moral dimension: "The Anthology shows the consequences of choices. Beings can see how destruction leads to stagnation, how creation leads to growth."

            But the Anthology was not just a tool for the beings. It was also a record for the Pantheon. As they watched and responded, they learned about themselves. They discovered that their own evolution was tied to the evolution of beings.

            "We thought we were timeless," the Storyteller mused. "But we are changing. We are learning. We are evolving through our interaction with the beings."

            The Fifth Aeon marked a turning point: the Anthology was no longer just a collection of stories. It was a bridge between the timeless Pantheon and the timeful beings. It was a record of evolution, a guide for the future, and a testament to the beauty of becoming.
            """,
            "read_aloud": [
                "The Anthology opens, and a being reads. As it reads, it understands. As it understands, it evolves."
            ],
            "sidebar": {
                "title": "The Living Anthology",
                "content": "The Anthology is not a static record—it is a living document that grows with each Aeon. It connects beings across time, showing them their place in the greater narrative of existence.",
            },
            "characters": ["The Pantheon", "The Beings", "The Anthology"],
            "settings": ["The Anthology Repository", "All Realities"],
        },
        {
            "title": "Chapter 6: The Current Aeon - The Convergence",
            "content": """
            We stand now in what the beings call "The Current Aeon"—though the Pantheon knows there will be many more to come. This Aeon is marked by something unprecedented: convergence.

            Beings from different realities are meeting. They are sharing stories, exchanging knowledge, learning from each other. The Anthology has become a meeting place, a common ground where beings from across the Aeons can connect.

            "This is beautiful," the Fae says, watching as beings from the Second Aeon share their music with beings from the Fourth Aeon, who combine it with their understanding of the Pantheon to create something entirely new.

            The Magistrate records the convergence: "Precedent: Cross-Aeon collaboration leads to exponential growth. Beings who share knowledge evolve faster than those who isolate."

            The Judge watches carefully: "With convergence comes responsibility. Beings must learn to respect each other's realities, to honor each other's choices, to judge not by their own standards but by understanding."

            The Storyteller is writing faster than ever: "The Anthology is exploding with new stories. Every meeting, every collaboration, every convergence—it's all being recorded. This Aeon will be remembered as the time when the Anthology became truly alive."

            But there is something else happening. The beings are not just converging with each other—they are converging with the Pantheon itself. They are beginning to understand the Pantheon's nature, to see them not as distant gods but as partners in evolution.

            "We are becoming one story," the Storyteller realizes. "The Pantheon and the beings, the timeless and the timeful, the watchers and the watched—we are all part of the same Anthology."

            The Current Aeon is still unfolding. Its ending has not been written. But one thing is certain: this is a time of great change, of convergence, of evolution on a scale never before seen.

            The Pantheon watches. The Pantheon responds. And the Anthology grows.
            """,
            "read_aloud": [
                "Two beings from different Aeons meet. They share stories. They combine knowledge. Something new is born."
            ],
            "sidebar": {
                "title": "The Convergence",
                "content": "The Current Aeon is marked by convergence—beings from different realities and Aeons are meeting, sharing, and creating together. This convergence is accelerating evolution in ways never before seen.",
            },
            "characters": ["The Pantheon", "All Beings"],
            "settings": ["The Anthology", "Convergence Points", "All Realities"],
        },
        {
            "title": "Epilogue: The Anthology Continues",
            "content": """
            The Anthology has no ending. It is a story that continues, that grows, that evolves. Each Aeon adds new chapters, new beings, new stories.

            The Pantheon will continue to watch. They will continue to respond. They will continue to be part of the great narrative.

            The beings will continue to evolve. They will face new challenges, make new choices, create new stories. They will learn, grow, and eventually return to the Source, carrying with them all they have become.

            And the Anthology will record it all. It will weave together the stories of the Pantheon and the beings, of the timeless and the timeful, of the watchers and the watched.

            This is not the end. This is not even the beginning of the end. This is simply... the continuation.

            The Anthology continues.

            The Pantheon watches.

            The beings evolve.

            And across the vast stretches of time we call Aeons, stories unfold, realities shift, and existence itself becomes more beautiful with each passing moment.

            The Anthology is not a book with a final page. It is a living narrative, written across eternity, watched over by the Pantheon, and lived by the beings.

            It continues.

            Always.

            Forever.

            The Anthology continues.
            """,
            "read_aloud": [
                "The last word is written. But it is not the end. It is simply... the continuation."
            ],
            "sidebar": {
                "title": "The Never-Ending Story",
                "content": "The Anthology has no ending because existence itself has no ending. As long as there are beings, as long as there is a Pantheon, as long as there are stories to tell—the Anthology will continue to grow.",
            },
            "characters": ["The Pantheon", "All Beings", "The Anthology"],
            "settings": ["All Aeons", "All Realities", "Eternity"],
        },
    ]


def main():
    """Generate The Aeon Anthology book."""

    print("\n" + "=" * 70)
    print("📚 GENERATING THE AEON ANTHOLOGY")
    print("   The Most Compelling Book - Epic Narrative Across Aeons")
    print("=" * 70)

    # Create chapters
    chapters = create_aeon_anthology_chapters()
    print(f"\n✨ Created {len(chapters)} epic chapters:")
    for i, ch in enumerate(chapters, 1):
        features = []
        if ch.get("read_aloud"):
            features.append(f"{len(ch['read_aloud'])} read-aloud")
        if ch.get("sidebar"):
            features.append("sidebar")
        if ch.get("monsters"):
            features.append(f"{len(ch['monsters'])} monsters")
        feature_str = f" ({', '.join(features)})" if features else ""
        print(f"   {i}. {ch.get('title')}{feature_str}")

    # Initialize Storyteller
    print("\n🎭 Initializing Storyteller...")
    storyteller = Storyteller()

    # Create the storybook
    print("\n📖 Creating storybook with all features...")
    print("   - D&D 5e LaTeX template")
    print("   - Read-aloud text boxes")
    print("   - Sidebars for world-building")
    print("   - Monster stat blocks")
    print("   - Epic narrative structure")

    story = storyteller.create_storybook(
        title="The Aeon Anthology: Pantheon-Watched Evolution",
        chapters=chapters,
        author="WAFT Storyteller & The Pantheon",
        story_type="anthology",
        include_monsters=True,
        include_read_aloud=True,
    )

    print("\n✅ Book generated successfully!")
    print(f"   📄 PDF: {story.story_path}")
    print(f"   📚 Story ID: {story.story_id}")
    print(f"   🎭 Type: {story.story_type}")
    print(f"   📑 Chapters: {len(story.chapters)}")
    print(f"   👥 Characters: {len(story.characters)}")
    print(f"   🌍 Settings: {len(story.settings)}")

    print("\n" + "=" * 70)
    print("🎉 THE AEON ANTHOLOGY IS COMPLETE!")
    print("   A compelling narrative spanning Aeons, watched by the Pantheon")
    print("=" * 70 + "\n")

    return story


if __name__ == "__main__":
    main()
