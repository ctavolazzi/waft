"""
AI Storyteller - Dynamic Visual Novel Engine
=============================================

An AI-powered storytelling engine that generates narratives in real-time,
like a D&D Dungeon Master for visual novels.

The AI:
- Generates scene descriptions, dialogue, and events
- Responds dynamically to player actions (typed or chosen)
- Maintains world state (location, inventory, NPCs, mood)
- Creates coherent ongoing narratives
- Uses procedurally generated worlds (taverns, NPCs, dungeons)
"""

import json
import os
from dataclasses import dataclass, field
from uuid import uuid4

# Try to import LLM client - falls back to mock if not available
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# Try to import procedural generators
try:
    from .generators import WorldManager
    HAS_GENERATORS = True
except ImportError:
    HAS_GENERATORS = False


@dataclass
class GameState:
    """Current state of the game world. Simplified to essentials."""
    session_id: str = field(default_factory=lambda: str(uuid4()))

    # Core state
    location: str = "tavern"
    mood: str = "warm"  # warm, mysterious, tense, peaceful, danger
    inventory: list[str] = field(default_factory=list)
    gold: int = 10
    characters_met: list[str] = field(default_factory=list)

    # Narrative
    story_history: list[dict] = field(default_factory=list)
    turn_count: int = 0

    # Procedural world (optional - set when using generators)
    world_seed: int | None = None
    world_context: dict = field(default_factory=dict)  # Rich context from WorldManager

    def add_history(self, role: str, content: str):
        """Add to story history."""
        self.story_history.append({
            "role": role,
            "content": content,
            "turn": self.turn_count,
        })

    def get_context(self) -> str:
        """Get context summary for AI."""
        inv = ", ".join(self.inventory) if self.inventory else "nothing"
        chars = ", ".join(self.characters_met) if self.characters_met else "no one yet"
        recent = [h["content"][:80] for h in self.story_history[-4:]]

        base_context = f"""Location: {self.location} | Mood: {self.mood}
Inventory: {inv} | Gold: {self.gold}
Characters met: {chars}
Recent: {' -> '.join(recent) if recent else 'Just arrived'}"""

        # Add rich world context if available
        if self.world_context:
            wc = self.world_context
            npcs = wc.get("patrons", [])[:3]  # Top 3 NPCs
            npc_summaries = []
            for npc in npcs:
                if isinstance(npc, dict):
                    name = npc.get("name", "Unknown")
                    traits = npc.get("personality", [])[:2]
                    hook = npc.get("hook", "")
                    npc_summaries.append(f"{name} ({', '.join(traits)}){': ' + hook if hook else ''}")

            if npc_summaries:
                base_context += f"\nNPCs present: {'; '.join(npc_summaries)}"

            rumors = wc.get("rumors", [])[:2]
            if rumors:
                base_context += f"\nRumors: {' | '.join(rumors)}"

        return base_context

    def to_dict(self) -> dict:
        """Serialize for API."""
        return {
            "session_id": self.session_id,
            "location": self.location,
            "mood": self.mood,
            "inventory": self.inventory,
            "gold": self.gold,
            "characters_met": self.characters_met,
            "turn_count": self.turn_count,
            "world_seed": self.world_seed,
        }


# System prompt for the AI storyteller
STORYTELLER_PROMPT = """You are a D&D-style storyteller for an interactive visual novel. Be vivid, atmospheric, and responsive.

STYLE: 2-3 paragraphs. Use *italics* for thoughts, **bold** for important things. Create memorable NPCs.

RESPOND WITH JSON:
{
    "narrative": "Story text (2-3 paragraphs)...",
    "speaker": "NPC name or null",
    "scene": "tavern|forest|road|cave|castle|village|shop|battlefield",
    "mood": "warm|mysterious|tense|peaceful|danger",
    "choices": ["Choice 1", "Choice 2", "Choice 3"],
    "updates": {"location": "new place", "item": "+sword/-gold", "character": "Name"}
}

RULES: Never break character. React to anything the player tries. Create consequences. Be consistent."""


class Storyteller:
    """AI-powered storyteller engine with procedural world generation."""

    def __init__(self, api_key: str | None = None, use_generators: bool = True):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = None
        self.use_generators = use_generators and HAS_GENERATORS

        # World managers keyed by session_id
        self._world_managers: dict[str, "WorldManager"] = {}

        if HAS_OPENAI and self.api_key:
            self.client = OpenAI(api_key=self.api_key)

    def get_world_manager(self, session_id: str) -> "WorldManager | None":
        """Get the world manager for a session."""
        return self._world_managers.get(session_id)

    def _generate_world_response(self, state: GameState, action: str = "") -> dict:
        """Generate response using procedural world context."""
        wc = state.world_context
        if not wc:
            return self._mock_response(state, action)

        # Get tavern info
        tavern_name = wc.get("location", "The Tavern")
        mood = wc.get("mood", "warm")

        # Find relevant NPC based on action
        npcs = wc.get("patrons", []) + wc.get("staff", [])
        speaker = None
        narrative = ""

        action_lower = action.lower()

        # Match action to NPCs
        for npc in npcs:
            if not isinstance(npc, dict):
                continue
            npc_name = npc.get("name", "").lower()
            occupation = npc.get("occupation", "").lower()
            if npc_name in action_lower or occupation in action_lower:
                speaker = npc
                break

        # If talking to bartender
        if speaker and "bartender" in speaker.get("occupation", "").lower():
            traits = speaker.get("personality", ["gruff"])
            name = speaker.get("name", "The bartender")
            rumors = wc.get("rumors", ["Strange things have been happening lately."])

            narrative = f'**{name}** leans forward, wiping a glass. '
            if "gruff" in traits:
                narrative += f'*"What\'ll it be?"* they ask, eyes appraising you.\n\n'
            else:
                narrative += f'*"Welcome, traveler. What brings you to {tavern_name}?"*\n\n'

            if rumors:
                narrative += f'After a moment, they add in a lower voice: *"{rumors[0]}"*'

            return {
                "narrative": narrative,
                "speaker": name,
                "scene": "tavern",
                "mood": mood,
                "choices": ["Ask about the rumor", "Order a drink", "Ask about the other patrons"],
                "updates": {"character": name},
            }

        # If talking to a patron
        if speaker:
            name = speaker.get("name", "The stranger")
            traits = speaker.get("personality", ["quiet"])
            secret = speaker.get("secret", "")
            hook = speaker.get("hook", "")

            trait_desc = traits[0] if traits else "mysterious"
            narrative = f'You approach **{name}**, who seems {trait_desc}.\n\n'

            if "nervous" in traits:
                narrative += f'They glance at the door before speaking. *"You\'re not one of them, are you?"*\n\n'
            elif "friendly" in traits:
                narrative += f'*"Ah, a new face! Sit, sit. Let me tell you a story..."*\n\n'
            else:
                narrative += f'They study you carefully. *"What do you want?"*\n\n'

            if hook:
                narrative += f'*Something about them suggests they {hook}.*'

            return {
                "narrative": narrative,
                "speaker": name,
                "scene": "tavern",
                "mood": mood,
                "choices": ["Ask what's troubling them", "Offer to help", "Back away slowly"],
                "updates": {"character": name},
            }

        # Default tavern scene with world context
        atmosphere = wc.get("atmosphere", {})
        sounds = atmosphere.get("sounds", ["quiet murmurs"])
        smells = atmosphere.get("smells", ["ale"])
        sights = atmosphere.get("sights", ["worn wooden tables"])

        # Build immersive description
        narrative = f'**{tavern_name}** buzzes with life. '
        narrative += f'You notice {sights[0] if sights else "the usual tavern fixtures"}. '
        narrative += f'The air carries the scent of {smells[0] if smells else "ale"}, '
        narrative += f'and you hear {sounds[0] if sounds else "quiet conversation"}.\n\n'

        # Mention interesting NPCs
        if npcs:
            bartender = next((n for n in npcs if isinstance(n, dict) and "bartender" in n.get("occupation", "").lower()), None)
            patrons = [n for n in npcs if isinstance(n, dict) and n.get("occupation", "") != "bartender"][:2]

            if bartender:
                narrative += f'The bartender, **{bartender.get("name")}**, catches your eye with a knowing nod.\n\n'

            if patrons:
                patron = patrons[0]
                desc = patron.get("description", "")[:100] if isinstance(patron.get("description"), str) else ""
                narrative += f'In the corner sits **{patron.get("name")}**, {patron.get("occupation", "a stranger")}. '
                if "nervous" in patron.get("personality", []):
                    narrative += '*They keep glancing at the door.*'

        choices = []
        if npcs:
            if bartender:
                choices.append(f"Approach {bartender.get('name', 'the bartender')}")
            if patrons:
                choices.append(f"Investigate {patrons[0].get('name', 'the stranger')}")
        choices.append("Check the notice board")

        return {
            "narrative": narrative,
            "speaker": None,
            "scene": "tavern",
            "mood": mood,
            "choices": choices,
            "updates": {},
        }

    def _mock_response(self, state: GameState, action: str = "") -> dict:
        """Generate a mock response when no LLM is available."""
        # Contextual mock responses
        if "bartender" in action.lower() or "grok" in action.lower():
            return {
                "narrative": "**Grok** leans forward, his tusks gleaming in the firelight. *\"You look like someone with a story to tell,\"* he rumbles, sliding a drink across the bar.\n\n*\"Or maybe someone looking for one? Strange things been happening at the old mill. Folk going missing. Might be worth your time... if you've got the nerve.\"*",
                "speaker": "Grok",
                "scene": "tavern",
                "mood": "mysterious",
                "choices": ["Ask about the mill", "Ask about the missing folk", "Order another drink"],
                "updates": {"character": "Grok"},
            }
        elif "hooded" in action.lower() or "figure" in action.lower() or "stranger" in action.lower():
            return {
                "narrative": "You approach the shadowed corner. The hooded figure looks up, revealing eyes that shimmer with an unnatural silver light. *\"I've been waiting for someone like you,\"* they whisper.\n\nA leather pouch slides across the table, jingling with coins—and something else that *moves*.\n\n*\"There's a crypt beneath the old mill. Bring me what you find there, and I'll make you wealthy beyond imagination.\"*",
                "speaker": "The Stranger",
                "scene": "tavern",
                "mood": "mysterious",
                "choices": ["Accept the quest", "Ask for more details", "Politely decline"],
                "updates": {"character": "The Stranger"},
            }

        # Default by location
        defaults = {
            "tavern": {
                "narrative": "The tavern buzzes with life. A bard strums a melancholy tune near the fire. The bartender, a half-orc named **Grok**, catches your eye with a knowing nod.\n\nIn the darkest corner sits a *hooded figure*, nursing a drink that glows faintly blue.\n\n*What draws your attention?*",
                "speaker": None,
                "scene": "tavern",
                "mood": "warm",
                "choices": ["Approach the bartender", "Investigate the hooded figure", "Check the notice board"],
            },
            "forest": {
                "narrative": "Ancient trees tower above you, filtering light into dancing green patterns. The forest whispers with hidden life.\n\n*The path splits ahead. One way is well-traveled, the other overgrown and mysterious.*",
                "speaker": None,
                "scene": "forest",
                "mood": "mysterious",
                "choices": ["Take the main path", "Explore the overgrown trail", "Climb a tree to look around"],
            },
            "cave": {
                "narrative": "Darkness presses in around you. Your torch flickers, casting dancing shadows on damp stone walls. *Something skitters in the darkness ahead.*",
                "speaker": None,
                "scene": "cave",
                "mood": "danger",
                "choices": ["Proceed carefully", "Call out", "Turn back"],
            },
        }

        base = defaults.get(state.location, defaults["tavern"])
        return {**base, "updates": {}}

    def start_game(self, setting: str = "fantasy_tavern", seed: int | None = None) -> tuple[GameState, dict]:
        """Start a new game session with optional procedural world generation."""
        state = GameState()

        # Try to use procedural generators for richer world
        if self.use_generators and setting == "fantasy_tavern":
            return self._start_game_with_generators(state, seed)

        # Fallback to static settings
        settings = {
            "fantasy_tavern": ("tavern", "warm", "A fantasy tavern with adventurers, a mysterious hooded figure, and rumors of trouble at the old mill"),
            "space_station": ("station_hub", "tense", "A space station orbiting a dying star, factions in conflict, someone important was just murdered"),
            "noir_city": ("office", "mysterious", "A rainy noir city, corrupt cops, you're a private detective and a dame with trouble just walked in"),
        }

        state.location, state.mood, world_context = settings.get(setting, settings["fantasy_tavern"])

        # Generate opening scene
        messages = [
            {"role": "system", "content": STORYTELLER_PROMPT},
            {"role": "user", "content": f"Start a new story. Setting: {world_context}. The player just arrived. Create an atmospheric opening."},
        ]

        response = self._call_llm(messages, state)
        self._apply_updates(state, response.get("updates", {}))
        state.add_history("narrator", response.get("narrative", ""))

        return state, response

    def _start_game_with_generators(self, state: GameState, seed: int | None = None) -> tuple[GameState, dict]:
        """Start game using procedural world generators."""
        from .generators import WorldManager

        # Create world manager
        world_manager = WorldManager(seed=seed)
        world_state, opening_context = world_manager.generate_starting_world("fantasy_tavern")

        # Store world manager
        self._world_managers[state.session_id] = world_manager

        # Update game state with world info
        state.world_seed = world_manager.seed
        state.world_context = opening_context
        state.location = opening_context.get("location", "tavern")
        state.mood = opening_context.get("mood", "warm")

        # Build rich context for AI
        world_prompt = self._build_world_prompt(opening_context)

        # Generate opening scene with rich context
        messages = [
            {"role": "system", "content": STORYTELLER_PROMPT},
            {"role": "system", "content": world_prompt},
            {"role": "user", "content": "The player just arrived at the tavern. Create an atmospheric opening that introduces the location, hints at interesting NPCs, and sets up potential adventure hooks."},
        ]

        response = self._call_llm(messages, state)

        # If LLM not available, use world-aware mock
        if not response.get("narrative"):
            response = self._generate_world_response(state)

        self._apply_updates(state, response.get("updates", {}))
        state.add_history("narrator", response.get("narrative", ""))

        return state, response

    def _build_world_prompt(self, context: dict) -> str:
        """Build a detailed world context prompt for the AI."""
        parts = []

        parts.append(f"LOCATION: {context.get('location', 'A tavern')}")
        parts.append(f"TYPE: {context.get('type', 'village_tavern')}")
        parts.append(f"MOOD: {context.get('mood', 'warm')}")

        # Description
        if context.get("description"):
            parts.append(f"\nDESCRIPTION: {context['description']}")

        # Bartender
        bartender = context.get("bartender")
        if bartender:
            parts.append(f"\nBARTENDER: {bartender.get('name')} - {bartender.get('description', '')}")

        # Featured patron
        patron = context.get("featured_patron")
        if patron:
            parts.append(f"\nINTERESTING PATRON: {patron.get('name')} - {patron.get('description', '')}")
            if patron.get("hook"):
                parts.append(f"  This patron {patron['hook']}.")
            if patron.get("secret"):
                parts.append(f"  SECRET (reveal gradually): {patron['secret']}")

        # Other patrons (brief)
        patrons = context.get("patrons", [])
        if patrons:
            patron_list = [f"{p.get('name', 'Unknown')} ({p.get('occupation', 'patron')})" for p in patrons[:3] if isinstance(p, dict)]
            if patron_list:
                parts.append(f"\nOTHER PATRONS: {', '.join(patron_list)}")

        # Atmosphere
        atmosphere = context.get("atmosphere", {})
        if atmosphere:
            parts.append(f"\nATMOSPHERE:")
            if atmosphere.get("sounds"):
                parts.append(f"  Sounds: {', '.join(atmosphere['sounds'][:2])}")
            if atmosphere.get("smells"):
                parts.append(f"  Smells: {', '.join(atmosphere['smells'][:2])}")
            if atmosphere.get("sights"):
                parts.append(f"  Sights: {', '.join(atmosphere['sights'][:2])}")

        # Rumors
        rumors = context.get("rumors", [])
        if rumors:
            parts.append(f"\nRUMORS (plot hooks to mention naturally):")
            for rumor in rumors[:2]:
                parts.append(f"  - {rumor}")

        # Nearby locations
        nearby = context.get("nearby_places", [])
        if nearby:
            parts.append(f"\nNEARBY PLACES (can be mentioned): {', '.join(nearby[:3])}")

        return "\n".join(parts)

    def take_action(self, state: GameState, action: str) -> dict:
        """Process a player action and generate response."""
        state.turn_count += 1
        state.add_history("player", action)

        # Build messages with context
        messages = [
            {"role": "system", "content": STORYTELLER_PROMPT},
        ]

        # Add world context if available
        if state.world_context:
            world_prompt = self._build_world_prompt(state.world_context)
            messages.append({"role": "system", "content": world_prompt})

        messages.append({"role": "system", "content": state.get_context()})

        # Add recent story history (last 6 exchanges)
        for h in state.story_history[-6:]:
            role = "assistant" if h["role"] == "narrator" else "user"
            messages.append({"role": role, "content": h["content"]})

        messages.append({"role": "user", "content": f"Player: {action}"})

        response = self._call_llm(messages, state, action)
        self._apply_updates(state, response.get("updates", {}))
        state.add_history("narrator", response.get("narrative", ""))

        if response.get("mood"):
            state.mood = response["mood"]

        return response

    def _call_llm(self, messages: list[dict], state: GameState, action: str = "") -> dict:
        """Call the LLM and parse response."""
        if not self.client:
            # Use world-aware mock if world context available
            if state.world_context:
                return self._generate_world_response(state, action)
            return self._mock_response(state, action)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.8,
                max_tokens=800,
                response_format={"type": "json_object"},
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"LLM error: {e}")
            # Use world-aware mock if world context available
            if state.world_context:
                return self._generate_world_response(state, action)
            return self._mock_response(state, action)

    def _apply_updates(self, state: GameState, updates: dict):
        """Apply state changes from AI response."""
        if not updates:
            return

        if updates.get("location"):
            state.location = updates["location"]

        # Handle item changes: "+sword" adds, "-gold" removes
        if updates.get("item"):
            item = updates["item"]
            if item.startswith("+"):
                state.inventory.append(item[1:])
            elif item.startswith("-") and item[1:] in state.inventory:
                state.inventory.remove(item[1:])
            else:
                state.inventory.append(item)

        if updates.get("gold"):
            state.gold += int(updates["gold"])

        if updates.get("character") and updates["character"] not in state.characters_met:
            state.characters_met.append(updates["character"])


# Singleton for easy access
_storyteller: Storyteller | None = None

def get_storyteller() -> Storyteller:
    """Get or create the storyteller instance."""
    global _storyteller
    if _storyteller is None:
        _storyteller = Storyteller()
    return _storyteller
