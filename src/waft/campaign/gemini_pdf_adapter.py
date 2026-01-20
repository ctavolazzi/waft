#!/usr/bin/env python3
"""
Gemini PDF Adapter
Bridge between Gemini narrative engine and WAFT PDF generation system
"""

import logging
from typing import Any

from .gemini_narrative_engine import GeminiNarrativeEngine, NarrativeContext, get_narrative_engine

logger = logging.getLogger(__name__)


class GeminiPDFAdapter:
    """Adapter to integrate Gemini narrative engine with PDF generation"""

    def __init__(self, engine: GeminiNarrativeEngine | None = None):
        """Initialize the adapter with a Gemini engine"""
        self.engine = engine or get_narrative_engine()
        self.enabled = self.engine.is_available()

        if self.enabled:
            logger.info("✅ Gemini PDF Adapter initialized with Gemini engine")
        else:
            logger.warning("⚠️ Gemini PDF Adapter initialized in fallback mode (no Gemini API)")

    async def enhance_campaign_narrative(
        self, campaign_data: dict[str, Any], use_gemini: bool = True
    ) -> str:
        """
        Generate AI-enhanced narrative for campaign PDF

        Args:
            campaign_data: Dictionary with campaign information
                - name: Campaign name
                - type: Campaign type
                - level_range: Level range (e.g., "1-5")
                - tone: Campaign tone (epic, dark, mystery, etc.)
                - setting: Campaign setting
            use_gemini: Whether to use Gemini (if available)

        Returns:
            Enhanced narrative text for PDF
        """
        if use_gemini and self.enabled:
            try:
                narrative = self.engine.generate_campaign_narrative(campaign_data)
                logger.info("✅ Generated Gemini-enhanced campaign narrative")
                return narrative
            except Exception as e:
                logger.warning(f"⚠️ Gemini narrative generation failed: {e}, using fallback")
                return self.engine._fallback_campaign_narrative(campaign_data)
        else:
            return self.engine._fallback_campaign_narrative(campaign_data)

    async def enhance_character_description(
        self, character: dict[str, Any], use_gemini: bool = True
    ) -> str:
        """
        Generate AI-enhanced character description for PDF

        Args:
            character: Dictionary with character information
                - name: Character name
                - class: Character class
                - race: Character race
                - level: Character level
                - background: Character background
            use_gemini: Whether to use Gemini (if available)

        Returns:
            Enhanced character description for PDF
        """
        if use_gemini and self.enabled:
            try:
                description = self.engine.generate_character_description(character)
                logger.info(
                    f"✅ Generated Gemini-enhanced description for {character.get('name', 'character')}"
                )
                return description
            except Exception as e:
                logger.warning(f"⚠️ Gemini character description failed: {e}, using fallback")
                return self.engine._fallback_character_description(character)
        else:
            return self.engine._fallback_character_description(character)

    async def generate_story_chapter(
        self,
        chapter_data: dict[str, Any],
        context: NarrativeContext | None = None,
        use_gemini: bool = True,
    ) -> str:
        """
        Generate AI-powered story chapter content for PDF

        Args:
            chapter_data: Dictionary with chapter information
                - title: Chapter title
                - events: List of events in chapter
                - characters: List of characters involved
                - location: Chapter location
            context: Optional NarrativeContext for richer generation
            use_gemini: Whether to use Gemini (if available)

        Returns:
            Story chapter content for PDF
        """
        if use_gemini and self.enabled and context:
            try:
                story_element = f"Chapter: {chapter_data.get('title', 'Unknown')}\n"
                story_element += f"Location: {chapter_data.get('location', 'Unknown')}\n"
                story_element += f"Events: {', '.join(chapter_data.get('events', []))}"

                narrative = self.engine.generate_adaptive_story(context, story_element)
                logger.info(
                    f"✅ Generated Gemini-enhanced story chapter: {chapter_data.get('title', 'Unknown')}"
                )
                return narrative
            except Exception as e:
                logger.warning(f"⚠️ Gemini story chapter generation failed: {e}, using fallback")
                return self._fallback_story_chapter(chapter_data)
        else:
            return self._fallback_story_chapter(chapter_data)

    def _fallback_story_chapter(self, chapter_data: dict[str, Any]) -> str:
        """Fallback story chapter when Gemini unavailable"""
        title = chapter_data.get("title", "Chapter")
        location = chapter_data.get("location", "the adventure")
        events = chapter_data.get("events", [])

        content = f"## {title}\n\n"
        content += f"This chapter takes place in {location}.\n\n"

        if events:
            content += "Key events:\n"
            for event in events:
                content += f"- {event}\n"

        return content

    def enhance_campaign_content(
        self, campaign_content: dict[str, Any], use_gemini: bool = True
    ) -> dict[str, Any]:
        """
        Enhance entire campaign content dictionary with Gemini-generated narratives

        Args:
            campaign_content: Dictionary with campaign content
                - campaign: Campaign metadata
                - characters: List of character dictionaries
                - chapters: List of chapter dictionaries (optional)
            use_gemini: Whether to use Gemini (if available)

        Returns:
            Enhanced campaign content dictionary
        """
        enhanced = campaign_content.copy()

        # Enhance campaign narrative
        if "campaign" in enhanced:
            enhanced["campaign"]["narrative"] = (
                self.engine.generate_campaign_narrative(enhanced["campaign"])
                if (use_gemini and self.enabled)
                else self.engine._fallback_campaign_narrative(enhanced["campaign"])
            )

        # Enhance character descriptions
        if "characters" in enhanced:
            for character in enhanced["characters"]:
                character["description"] = (
                    self.engine.generate_character_description(character)
                    if (use_gemini and self.enabled)
                    else self.engine._fallback_character_description(character)
                )

        # Enhance chapters if provided
        if "chapters" in enhanced and use_gemini and self.enabled:
            # Note: This would require NarrativeContext, which would need to be built
            # from campaign state. For now, we'll enhance with basic narrative.
            for chapter in enhanced["chapters"]:
                if "narrative" not in chapter:
                    chapter["narrative"] = self._fallback_story_chapter(chapter)

        return enhanced

    def is_available(self) -> bool:
        """Check if Gemini enhancement is available"""
        return self.enabled

    def get_status(self) -> dict[str, Any]:
        """Get adapter status"""
        return {
            "adapter_name": "Gemini PDF Adapter",
            "enabled": self.enabled,
            "engine_status": self.engine.get_engine_status() if self.enabled else None,
            "capabilities": [
                "campaign_narrative_enhancement",
                "character_description_enhancement",
                "story_chapter_generation",
                "full_campaign_enhancement",
            ],
        }
