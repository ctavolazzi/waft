#!/usr/bin/env python3
"""
Gemini-Powered Narrative Decision Making Engine
Integrates Google Gemini API for intelligent D&D storytelling and decision support

Adapted from AI-DnD project for WAFT integration.
"""

import os
import json
import logging
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from .env file
except ImportError:
    pass  # dotenv is optional

try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("⚠️ google-genai package not installed. Install with: pip install google-genai")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class NarrativeContext:
    """Context for narrative generation"""
    campaign_id: str
    session_id: str
    current_scene: str
    player_actions: List[str]
    npc_states: Dict[str, Any]
    world_state: Dict[str, Any]
    campaign_tone: str = "epic"
    difficulty_level: str = "medium"

@dataclass
class DecisionOption:
    """Represents a decision option with AI reasoning"""
    option: str
    reasoning: str
    consequences: List[str]
    probability_success: float
    risk_level: str
    alignment: str  # good, neutral, evil

@dataclass
class StoryBranch:
    """Represents a story branch with predicted outcomes"""
    branch_name: str
    description: str
    immediate_consequences: List[str]
    long_term_effects: List[str]
    character_impact: Dict[str, str]
    world_changes: List[str]

@dataclass
class NPCBehavior:
    """Represents AI-generated NPC behavior"""
    npc_name: str
    personality_traits: List[str]
    current_mood: str
    reaction: str
    dialogue_suggestions: List[str]
    action_recommendations: List[str]

class GeminiNarrativeEngine:
    """Main engine for Gemini-powered narrative decision making"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Gemini narrative engine"""
        if not GEMINI_AVAILABLE:
            logger.warning("⚠️ Gemini SDK not available. Install with: pip install google-genai")
            self.client = None
            self.api_key = None
            return
            
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')

        # Log API key status for debugging
        if self.api_key:
            logger.info(f"✅ Gemini API key loaded: {self.api_key[:10]}...")
        else:
            logger.warning("⚠️ No Gemini API key found - will use fallback mode")
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-3-pro-preview')
        self.thinking_level = self._validate_thinking_level(os.getenv('GEMINI_THINKING_LEVEL', 'high'))
        self.client = None
        
        if GEMINI_AVAILABLE:
            self.safety_settings = [
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE
                ),
            ]
        else:
            self.safety_settings = []

        if self.api_key and GEMINI_AVAILABLE:
            try:
                self.client = genai.Client(
                    api_key=self.api_key,
                    http_options={"api_version": "v1alpha"}
                )
                logger.info("✅ Gemini Narrative Engine initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Gemini client: {e}")
                self.client = None
        else:
            if not GEMINI_AVAILABLE:
                logger.warning("⚠️ Gemini SDK not installed, engine will use fallback mode")
            else:
                logger.warning("⚠️ No Gemini API key found, engine will use fallback mode")

    def is_available(self) -> bool:
        """Check if Gemini is available"""
        return self.client is not None and GEMINI_AVAILABLE

    async def generate_narrative_response(
        self,
        context: NarrativeContext,
        prompt: str,
        max_tokens: int = 1000,
        thinking_level: Optional[str] = None
    ) -> str:
        """Generate narrative response using Gemini"""
        if not self.is_available():
            raise RuntimeError("Gemini engine not available")

        try:
            # Build context-aware prompt
            full_prompt = self._build_narrative_prompt(context, prompt)

            # Generate response
            response_text = await asyncio.to_thread(
                self._generate_text,
                full_prompt,
                max_output_tokens=max_tokens,
                temperature=0.8,
                top_p=0.9,
                top_k=40,
                thinking_level=thinking_level
            )

            return response_text.strip()

        except Exception as e:
            logger.error(f"❌ Error generating narrative response: {e}")
            raise

    def generate_decision_matrix(
        self,
        context: NarrativeContext,
        decision_scenario: str,
        options: List[str],
        thinking_level: Optional[str] = None
    ) -> List[DecisionOption]:
        """Generate AI-powered decision matrix with reasoning"""
        if not self.is_available():
            raise RuntimeError("Gemini engine not available")

        try:
            prompt = f"""
            As an expert D&D Dungeon Master, analyze this decision scenario and provide AI reasoning for each option.

            Scenario: {decision_scenario}
            Campaign Tone: {context.campaign_tone}
            Difficulty: {context.difficulty_level}

            Available Options:
            {chr(10).join(f"{i+1}. {option}" for i, option in enumerate(options))}

            For each option, provide:
            1. Reasoning (why this choice makes sense)
            2. Consequences (what happens next)
            3. Success probability (0.0-1.0)
            4. Risk level (low/medium/high)
            5. Alignment (good/neutral/evil)

            Format as JSON array with fields: option, reasoning, consequences, probability_success, risk_level, alignment
            """

            response_text = self._generate_text(
                prompt,
                max_output_tokens=800,
                temperature=0.7,
                thinking_level=thinking_level
            )
            decision_data = json.loads(response_text)

            return [
                DecisionOption(
                    option=item['option'],
                    reasoning=item['reasoning'],
                    consequences=item['consequences'],
                    probability_success=float(item['probability_success']),
                    risk_level=item['risk_level'],
                    alignment=item['alignment']
                )
                for item in decision_data
            ]

        except Exception as e:
            logger.error(f"❌ Error generating decision matrix: {e}")
            # Return fallback options
            return [
                DecisionOption(
                    option=option,
                    reasoning="AI analysis unavailable",
                    consequences=["Unknown consequences"],
                    probability_success=0.5,
                    risk_level="medium",
                    alignment="neutral"
                )
                for option in options
            ]

    def generate_adaptive_story(
        self,
        context: NarrativeContext,
        story_element: str,
        thinking_level: Optional[str] = None
    ) -> str:
        """Generate adaptive story content based on campaign progression"""
        if not self.is_available():
            raise RuntimeError("Gemini engine not available")

        try:
            prompt = f"""
            As an expert D&D storyteller, create adaptive story content that evolves with the campaign.

            Story Element: {story_element}
            Campaign Tone: {context.campaign_tone}
            Difficulty: {context.difficulty_level}
            Player Actions: {', '.join(context.player_actions[-5:])}  # Last 5 actions
            World State: {json.dumps(context.world_state, indent=2)}

            Create engaging, adaptive content that:
            1. Builds on previous player actions
            2. Reflects the current world state
            3. Maintains campaign tone and difficulty
            4. Provides meaningful choices and consequences

            Return as narrative text (2-3 paragraphs).
            """

            response_text = self._generate_text(
                prompt,
                max_output_tokens=600,
                temperature=0.85,
                thinking_level=thinking_level
            )
            return response_text.strip()

        except Exception as e:
            logger.error(f"❌ Error generating adaptive story: {e}")
            return f"Story content for {story_element} is being prepared..."

    def generate_campaign_narrative(
        self,
        campaign_data: Dict[str, Any],
        thinking_level: Optional[str] = None
    ) -> str:
        """Generate narrative content for campaign PDF"""
        if not self.is_available():
            return self._fallback_campaign_narrative(campaign_data)

        try:
            prompt = f"""
            As an expert D&D storyteller, create engaging narrative content for a campaign PDF.

            Campaign Name: {campaign_data.get('name', 'Unknown Campaign')}
            Campaign Type: {campaign_data.get('type', 'Adventure')}
            Level Range: {campaign_data.get('level_range', '1-5')}
            Tone: {campaign_data.get('tone', 'epic')}
            Setting: {campaign_data.get('setting', 'Fantasy world')}

            Create 2-3 paragraphs of engaging narrative that:
            1. Sets the scene and atmosphere
            2. Introduces key themes and conflicts
            3. Hooks players into the adventure
            4. Maintains the campaign tone

            Write in a style suitable for a campaign book PDF.
            """

            response_text = self._generate_text(
                prompt,
                max_output_tokens=500,
                temperature=0.8,
                thinking_level=thinking_level
            )
            return response_text.strip()

        except Exception as e:
            logger.error(f"❌ Error generating campaign narrative: {e}")
            return self._fallback_campaign_narrative(campaign_data)

    def generate_character_description(
        self,
        character: Dict[str, Any],
        thinking_level: Optional[str] = None
    ) -> str:
        """Generate enhanced character description for PDF"""
        if not self.is_available():
            return self._fallback_character_description(character)

        try:
            prompt = f"""
            As an expert D&D character creator, write an engaging character description for a campaign PDF.

            Character Name: {character.get('name', 'Unknown')}
            Class: {character.get('class', 'Adventurer')}
            Race: {character.get('race', 'Human')}
            Level: {character.get('level', 1)}
            Background: {character.get('background', 'Unknown')}

            Create a vivid 2-3 sentence description that:
            1. Captures their appearance and personality
            2. Hints at their background and motivations
            3. Makes them memorable and interesting
            4. Fits the campaign tone

            Write in a style suitable for a campaign book PDF.
            """

            response_text = self._generate_text(
                prompt,
                max_output_tokens=200,
                temperature=0.8,
                thinking_level=thinking_level
            )
            return response_text.strip()

        except Exception as e:
            logger.error(f"❌ Error generating character description: {e}")
            return self._fallback_character_description(character)

    def _fallback_campaign_narrative(self, campaign_data: Dict[str, Any]) -> str:
        """Fallback narrative when Gemini unavailable"""
        name = campaign_data.get('name', 'this campaign')
        tone = campaign_data.get('tone', 'epic')
        return f"""
        Welcome to {name}, a {tone} adventure that will test your skills and resolve.
        The world is full of danger and opportunity, and your choices will shape the story.
        Prepare yourself for an unforgettable journey.
        """

    def _fallback_character_description(self, character: Dict[str, Any]) -> str:
        """Fallback character description when Gemini unavailable"""
        name = character.get('name', 'The character')
        char_class = character.get('class', 'adventurer')
        race = character.get('race', 'human')
        return f"{name} is a {race} {char_class} with a mysterious past and a bright future."

    def _build_narrative_prompt(self, context: NarrativeContext, prompt: str) -> str:
        """Build context-aware prompt for narrative generation"""
        return f"""
        You are an expert D&D Dungeon Master with deep knowledge of storytelling, character development, and game mechanics.

        CAMPAIGN CONTEXT:
        - Campaign ID: {context.campaign_id}
        - Session ID: {context.session_id}
        - Current Scene: {context.current_scene}
        - Campaign Tone: {context.campaign_tone}
        - Difficulty Level: {context.difficulty_level}

        RECENT PLAYER ACTIONS:
        {chr(10).join(f"- {action}" for action in context.player_actions[-3:])}

        NPC STATES:
        {json.dumps(context.npc_states, indent=2)}

        WORLD STATE:
        {json.dumps(context.world_state, indent=2)}

        PLAYER REQUEST:
        {prompt}

        Provide a compelling, immersive response that:
        1. Maintains narrative consistency
        2. Reflects the campaign tone and difficulty
        3. Builds on previous actions and world state
        4. Offers meaningful choices and consequences
        5. Enhances the overall storytelling experience

        Response:
        """

    def _generate_text(
        self,
        prompt: str,
        *,
        max_output_tokens: int = 600,
        temperature: float = 0.8,
        top_p: float = 0.9,
        top_k: int = 40,
        thinking_level: Optional[str] = None
    ) -> str:
        """Call Gemini and return concatenated text output."""
        if not self.is_available():
            raise RuntimeError("Gemini engine not available")

        level = self._validate_thinking_level(thinking_level) if thinking_level else self.thinking_level
        config_kwargs = {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": max_output_tokens,
            "safety_settings": self.safety_settings
        }
        if level:
            config_kwargs["thinking_level"] = level

        try:
            config = types.GenerateContentConfig(**config_kwargs)
        except Exception as e:
            # Fallback for older SDK versions that don't support thinking_level
            if "thinking_level" in config_kwargs:
                logger.warning(f"⚠️ 'thinking_level' not supported by installed SDK version: {e}")
                del config_kwargs["thinking_level"]
                config = types.GenerateContentConfig(**config_kwargs)
            else:
                raise e

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[prompt],
            config=config
        )

        return self._extract_text(response)

    def _extract_text(self, response: Any) -> str:
        """Extract plain text from a Gemini response."""
        if not response or not getattr(response, "candidates", None):
            raise ValueError("No candidates in Gemini response")

        text_parts: List[str] = []
        for candidate in response.candidates:
            content = getattr(candidate, "content", None)
            if not content or not getattr(content, "parts", None):
                continue
            for part in content.parts:
                if getattr(part, "text", None):
                    text_parts.append(part.text)

        if not text_parts:
            raise ValueError("No text parts in Gemini response")

        return "\n".join(text_parts).strip()

    def _validate_thinking_level(self, level: Optional[str]) -> Optional[str]:
        """Normalize and validate requested thinking level."""
        if level is None:
            return "high"

        normalized = str(level).lower().strip()
        allowed_levels = {"low", "high"}
        if normalized not in allowed_levels:
            logger.warning(f"⚠️ Invalid thinking level '{level}' provided. Falling back to 'high'.")
            return "high"
        return normalized

    def set_thinking_level(self, level: str) -> str:
        """Update the default thinking level for future generations."""
        self.thinking_level = self._validate_thinking_level(level)
        return self.thinking_level

    def get_engine_status(self) -> Dict[str, Any]:
        """Get current engine status and capabilities"""
        return {
            "engine_name": "Gemini Narrative Engine",
            "version": "1.0.0",
            "gemini_available": self.is_available(),
            "api_key_configured": bool(self.api_key),
            "model": self.model_name if self.is_available() else None,
            "thinking_level": self.thinking_level,
            "capabilities": [
                "narrative_generation",
                "decision_matrix",
                "story_branch_analysis",
                "npc_behavior_generation",
                "adaptive_storytelling",
                "campaign_narrative",
                "character_description"
            ],
            "timestamp": datetime.now().isoformat()
        }

# Global engine instance
narrative_engine = GeminiNarrativeEngine()

def get_narrative_engine() -> GeminiNarrativeEngine:
    """Get the global narrative engine instance"""
    return narrative_engine
