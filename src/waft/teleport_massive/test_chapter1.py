#!/usr/bin/env python3
"""
Test script for Teleport Massive Writer

Generates Chapter 1 to verify the system works.
"""

from pathlib import Path
from .engine import TMWriter
from .config import StoryConfig, ConfigPresets


def generate_chapter_1():
    """Generate the introductory chapter of Teleport Massive."""

    print("=" * 70)
    print("TELEPORT MASSIVE WRITER - Chapter 1 Test")
    print("=" * 70)

    # Create writer with classic preset
    print("\n[1] Initializing writer with classic TM preset...")
    writer = TMWriter.create("classic_tm", seed=42)

    print(f"    Config: {writer.config.tone.value}, {writer.config.narrative_style.value}")
    print(f"    Protagonist: {writer.config.protagonist}")
    print(f"    Footnotes: {writer.config.enable_footnotes}")
    print(f"    Meta-narrative: {writer.config.enable_meta_narrative}")

    # Initialize world
    print("\n[2] Initializing story world...")
    initial_state = writer.initialize()

    print(f"    Characters loaded: {len(initial_state.characters)}")
    print(f"    Factions active: {len(initial_state.factions)}")
    print(f"    Locations available: {len(initial_state.locations)}")
    print(f"    Open threads: {len(initial_state.open_threads)}")
    print(f"    State hash: {initial_state.state_hash}")

    # Generate Chapter 1
    print("\n[3] Generating Chapter 1...")
    scenes = writer.generate_chapter(1)

    print(f"    Scenes generated: {len(scenes)}")

    # Display each scene
    for scene in scenes:
        print(f"\n    --- Scene {scene.chapter}.{scene.scene_number}: {scene.title} ---")
        print(f"    POV: {scene.pov_character}")
        print(f"    Location: {scene.location}")
        print(f"    Characters: {', '.join(scene.characters_present)}")
        print(f"    Word count: {scene.word_count}")

    # Show current state
    print("\n[4] Final state after Chapter 1...")
    final_state = writer.get_current_state()
    print(f"    Chapter: {final_state.current_chapter}")
    print(f"    Scene: {final_state.current_scene}")
    print(f"    State hash: {final_state.state_hash}")
    print(f"    Parent hash: {final_state.parent_hash}")

    # Show history
    print("\n[5] State history...")
    history = writer.get_history()
    print(f"    Total states: {len(history)}")
    for i, state in enumerate(history[:5]):
        print(f"    [{i}] ch{state.current_chapter}:sc{state.current_scene} - {state.state_hash[:8]}")

    # Stats
    print("\n[6] Writer stats...")
    stats = writer.stats()
    print(f"    Store objects: {stats['store']['total_objects']}")
    print(f"    Storage size: {stats['store']['storage_mb']} MB")

    # Output first scene content
    print("\n" + "=" * 70)
    print("CHAPTER 1, SCENE 1 CONTENT:")
    print("=" * 70)
    print(scenes[0].content)

    print("\n" + "=" * 70)
    print("TEST COMPLETE - Chapter 1 generated successfully!")
    print("=" * 70)

    return scenes


def main():
    """Run the test."""
    scenes = generate_chapter_1()
    return scenes


if __name__ == "__main__":
    main()
