"""
Pet card generator using Teleport Massive Card Game rendering utilities.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from waft.being import BeingState

from .pet_being import PetBeing, pet_realm_path

project_root = Path(__file__).resolve().parents[3]
tmcg_root = project_root / "_realms" / "teleport_massive_cardgame" / "src"
if tmcg_root.exists() and str(tmcg_root) not in sys.path:
    sys.path.insert(0, str(tmcg_root))

from tmcg.generators.art_generator import ArtGenerator, ArtStyle
from tmcg.generators.card_generator import CardGenerator
from tmcg.models.card import FrameColor, Rarity
from tmcg.renderers.html_renderer import HTMLRenderer


class PetCardGenerator:
    def __init__(self, project_path: Path | None = None):
        self.project_path = Path(project_path or project_root)
        self.cards_dir = pet_realm_path(self.project_path) / "cards"
        self.cards_dir.mkdir(parents=True, exist_ok=True)
        self.art_dir = self.cards_dir / "art"
        self.art_generator = ArtGenerator(self.art_dir)
        self.card_generator = CardGenerator(art_dir=self.art_dir)
        self.renderer = HTMLRenderer()

    def _build_card(
        self,
        *,
        name: str,
        type_line: str,
        abilities: str,
        flavor_text: str,
        rarity: Rarity,
        frame_color: FrameColor,
        art_description: str | None = None,
        art_style: ArtStyle | None = None,
    ) -> tuple[Any, list[dict[str, Any]]]:
        card = self.card_generator.from_dict(
            {
                "name": name,
                "type_line": type_line,
                "abilities": abilities,
                "flavor_text": flavor_text,
                "rarity": rarity.value,
                "frame_color": frame_color.value,
                "set_code": "PET",
            }
        )

        art_requests: list[dict[str, Any]] = []
        if art_description and art_style and not self.art_generator.has_art(card.name):
            request = self.art_generator.create_request(
                card_name=card.name, description=art_description, style=art_style
            )
            art_requests.append(
                {
                    "card_name": request.card_name,
                    "description": request.description,
                    "style": request.style.value,
                    "size": request.size.value,
                    "n_directions": request.n_directions,
                    "view": request.view,
                    "detail": request.detail,
                    "shading": request.shading,
                    "outline": request.outline,
                }
            )

        return card, art_requests

    def generate_cards_for_pet(self, pet: PetBeing) -> dict[str, Any]:
        cards = []
        art_requests: list[dict[str, Any]] = []

        memory_cards = len(pet.memories) // 10
        for index in range(memory_cards):
            card, requests = self._build_card(
                name=f"{pet.display_name} Memory {index + 1}",
                type_line="Memory - Pet",
                abilities=f"A milestone memory at {((index + 1) * 10)} experiences.",
                flavor_text="The past hums softly in the present.",
                rarity=Rarity.COMMON,
                frame_color=FrameColor.BLUE,
                art_description="A glowing memory orb with gentle light",
                art_style=ArtStyle.OBJECT,
            )
            cards.append(card)
            art_requests.extend(requests)

        for skill_name in pet.skills.keys():
            card, requests = self._build_card(
                name=f"{pet.display_name} Skill: {skill_name.title()}",
                type_line="Skill - Pet",
                abilities=f"{pet.display_name} has learned {skill_name}.",
                flavor_text="Practice turns instinct into mastery.",
                rarity=Rarity.UNCOMMON,
                frame_color=FrameColor.GREEN,
                art_description=f"A pet learning {skill_name} in a bright scene",
                art_style=ArtStyle.CHARACTER,
            )
            cards.append(card)
            art_requests.extend(requests)

        for lesson in pet.lessons_learned:
            lesson_title = lesson.get("title") or lesson.get("summary") or "Lesson Learned"
            card, requests = self._build_card(
                name=f"{pet.display_name} Achievement",
                type_line="Achievement - Pet",
                abilities=lesson_title,
                flavor_text="Growth is the quiet reward of persistence.",
                rarity=Rarity.RARE,
                frame_color=FrameColor.MULTICOLOR,
                art_description="A triumphant pet with a sparkling badge",
                art_style=ArtStyle.CHARACTER,
            )
            cards.append(card)
            art_requests.extend(requests)

        if pet.state == BeingState.DEAD:
            card, requests = self._build_card(
                name=f"{pet.display_name} Death",
                type_line="Death - Pet",
                abilities="The end of a cherished cycle.",
                flavor_text="Even endings echo with meaning.",
                rarity=Rarity.MYTHIC,
                frame_color=FrameColor.BLACK,
                art_description="A soft ghostly silhouette fading into starlight",
                art_style=ArtStyle.LANDSCAPE,
            )
            cards.append(card)
            art_requests.extend(requests)

        if pet.lifetimes > 1:
            card, requests = self._build_card(
                name=f"{pet.display_name} Reborn",
                type_line="Reincarnation - Pet",
                abilities="A new beginning forged by karma.",
                flavor_text="The story continues, brighter than before.",
                rarity=Rarity.MYTHIC,
                frame_color=FrameColor.WHITE,
                art_description="A reborn pet emerging from glowing light",
                art_style=ArtStyle.CHARACTER,
            )
            cards.append(card)
            art_requests.extend(requests)

        html_path = None
        if cards:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            html_path = self.renderer.render_cards_to_file(
                cards,
                self.cards_dir / f"{pet.being_id}_{timestamp}.html",
                title=f"{pet.display_name} Life Story",
            )

        return {
            "cards": [card.model_dump() for card in cards],
            "html_path": str(html_path) if html_path else None,
            "art_requests": art_requests,
        }
