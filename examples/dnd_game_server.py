"""
D&D Game Web Server - FastAPI backend with HTML frontend

Serves an interactive D&D game in the browser.
"""

import sys
import json
import random
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from waft.core.dnd5e import (
    DnD5eCharacter,
    DnD5eStats,
    DnDRoller,
    DnD5eCombat,
    ArmorType
)

app = FastAPI(title="D&D Game Server")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory game state storage (in production, use a database)
game_states: Dict[str, Dict[str, Any]] = {}

# Quest system
QUESTS = {
    "goblin_hunt": {
        "id": "goblin_hunt",
        "name": "Goblin Hunt",
        "description": "Clear out the goblin infestation in the nearby cave",
        "objectives": ["defeat_goblin", "defeat_goblin", "defeat_goblin"],
        "rewards": {"xp": 150, "gold": 50},
        "status": "available"
    },
    "merchant_delivery": {
        "id": "merchant_delivery",
        "name": "Merchant's Delivery",
        "description": "Deliver goods to the next town",
        "objectives": ["explore", "reach_town"],
        "rewards": {"xp": 100, "gold": 75},
        "status": "available"
    },
    "ancient_ruins": {
        "id": "ancient_ruins",
        "name": "Explore Ancient Ruins",
        "description": "Investigate the mysterious ruins and discover their secrets",
        "objectives": ["explore_ruins", "defeat_guardian"],
        "rewards": {"xp": 200, "gold": 100, "item": "Ancient Artifact"},
        "status": "available"
    }
}


class CreateCharacterRequest(BaseModel):
    name: str


class GameActionRequest(BaseModel):
    game_id: str
    action: str
    data: Optional[Dict[str, Any]] = None


class ShopPurchaseRequest(BaseModel):
    game_id: str
    item_key: str


class CombatActionRequest(BaseModel):
    game_id: str
    action: str  # "attack", "flee", or "cast"
    spell_id: Optional[str] = None  # Required if action is "cast"


class QuestActionRequest(BaseModel):
    game_id: str
    quest_id: str
    action: str  # "accept", "complete", or "abandon"


# Shop items
SHOP_ITEMS = {
    "sword": {"name": "Longsword", "cost": 15, "type": "weapon", "damage": "1d8"},
    "dagger": {"name": "Dagger", "cost": 2, "type": "weapon", "damage": "1d4"},
    "shield": {"name": "Shield", "cost": 10, "type": "armor", "ac_bonus": 2},
    "leather": {"name": "Leather Armor", "cost": 10, "type": "armor", "ac": 11},
    "chain": {"name": "Chain Mail", "cost": 75, "type": "armor", "ac": 16},
    "potion": {"name": "Healing Potion", "cost": 50, "type": "consumable", "healing": "2d4+2"},
    "rations": {"name": "Rations (1 day)", "cost": 5, "type": "consumable"},
}

# Enemies
ENEMIES = {
    "goblin": {"name": "Goblin", "ac": 15, "hp": 7, "damage": "1d6", "xp": 50},
    "orc": {"name": "Orc", "ac": 13, "hp": 15, "damage": "1d12+3", "xp": 100},
    "skeleton": {"name": "Skeleton", "ac": 13, "hp": 13, "damage": "1d6+2", "xp": 50},
    "bandit": {"name": "Bandit", "ac": 12, "hp": 11, "damage": "1d6", "xp": 25},
    "wolf": {"name": "Wolf", "ac": 13, "hp": 11, "damage": "2d4+2", "xp": 50},
}

# Locations
LOCATIONS = {
    "town": {
        "name": "Town Square",
        "description": "A bustling town square with shops and taverns",
        "encounters": ["merchant", "guard", "citizen"],
        "enemies": ["bandit"],
        "shop_available": True
    },
    "forest": {
        "name": "Dark Forest",
        "description": "A mysterious forest filled with danger",
        "encounters": ["hermit", "ruins", "clearing"],
        "enemies": ["goblin", "wolf"],
        "shop_available": False
    },
    "cave": {
        "name": "Goblin Cave",
        "description": "A dark cave filled with goblins",
        "encounters": ["treasure", "goblin_camp"],
        "enemies": ["goblin", "orc"],
        "shop_available": False
    },
    "ruins": {
        "name": "Ancient Ruins",
        "description": "Mysterious ruins from a forgotten age",
        "encounters": ["artifact", "guardian", "puzzle"],
        "enemies": ["skeleton", "orc"],
        "shop_available": False
    }
}


def roll_ability_score() -> int:
    """Roll 4d6, drop lowest."""
    rolls = [DnDRoller.roll("1d6") for _ in range(4)]
    rolls.sort(reverse=True)
    return sum(rolls[:3])


def create_character(name: str) -> DnD5eCharacter:
    """Create a character with rolled stats."""
    strength = roll_ability_score()
    dexterity = roll_ability_score()
    constitution = roll_ability_score()
    intelligence = roll_ability_score()
    wisdom = roll_ability_score()
    charisma = roll_ability_score()
    
    con_mod = DnD5eStats.ability_modifier(constitution)
    hit_die = 10
    max_hp = hit_die + con_mod
    
    return DnD5eCharacter(
        name=name,
        level=1,
        char_class="fighter",
        hit_die=hit_die,
        strength=strength,
        dexterity=dexterity,
        constitution=constitution,
        intelligence=intelligence,
        wisdom=wisdom,
        charisma=charisma,
        hp=max_hp,
        max_hp=max_hp,
        armor_type=ArmorType.NONE,
        proficient_saves=["STR", "CON"],
        proficient_skills=["Athletics", "Perception"],
    )


@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Serve the main game HTML."""
    html_path = Path(__file__).parent / "dnd_game_ui.html"
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text())
    else:
        return HTMLResponse(content="<h1>D&D Game UI not found</h1>")


@app.post("/api/create-character")
async def create_character_endpoint(request: CreateCharacterRequest):
    """Create a new character and game state."""
    character = create_character(request.name)
    
    game_id = f"game_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    
    game_state = {
        "game_id": game_id,
        "character": character.to_dict(),
            "gold": 50,
            "inventory": [],
            "story_log": [],
            "encounters_completed": 0,
            "combat_state": None,  # Current combat encounter
            "active_quests": [],  # List of active quest IDs
            "completed_quests": [],  # List of completed quest IDs
            "quest_progress": {},  # Quest ID -> progress dict
        }
    
    game_states[game_id] = game_state
    
    return JSONResponse({
        "game_id": game_id,
        "character": character.to_dict(),
        "gold": 50,
        "inventory": [],
    })


@app.get("/api/game/{game_id}")
async def get_game_state(game_id: str):
    """Get current game state."""
    if game_id not in game_states:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return JSONResponse(game_states[game_id])


@app.post("/api/game/action")
async def game_action(request: GameActionRequest):
    """Perform a game action."""
    if request.game_id not in game_states:
        raise HTTPException(status_code=404, detail="Game not found")
    
    state = game_states[request.game_id]
    char_data = state["character"]
    character = DnD5eCharacter.from_dict(char_data)
    
    result = {"success": True, "message": "", "data": {}}
    
    if request.action == "explore":
        story_options = [
            "You discover an ancient ruin with mysterious markings.",
            "You find a hidden path leading into the forest.",
            "A traveling merchant approaches you with a quest.",
            "You stumble upon a bandit camp in the distance.",
            "An old hermit offers you wisdom and a small trinket.",
        ]
        story = random.choice(story_options)
        state["story_log"].append(story)
        
        gold_found = random.randint(1, 10)
        state["gold"] += gold_found
        
        result["message"] = story
        result["data"] = {"gold_found": gold_found, "gold": state["gold"]}
        
        # Check if encounter should happen
        if "bandit" in story.lower() or "ruin" in story.lower():
            result["data"]["encounter"] = True
        
        # Update quest progress for exploration objectives
        if "active_quests" in state and state["active_quests"]:
            for quest_id in state["active_quests"]:
                if quest_id in state.get("quest_progress", {}):
                    progress = state["quest_progress"][quest_id]
                    objectives = progress.get("objectives", [])
                    completed = progress.get("objectives_completed", [])
                    
                    if "explore" in objectives and "explore" not in completed:
                        completed.append("explore")
                        progress["objectives_completed"] = completed
                    
                    if "explore_ruins" in objectives and "ruin" in story.lower() and "explore_ruins" not in completed:
                        completed.append("explore_ruins")
                        progress["objectives_completed"] = completed
    
    elif request.action == "rest":
        healing = DnDRoller.roll("1d8") + character.con_modifier
        old_hp = character.hp
        DnD5eCombat.apply_healing(character, healing)
        hp_gained = character.hp - old_hp
        state["character"] = character.to_dict()
        
        result["message"] = f"Restored {hp_gained} HP"
        result["data"] = {"hp_gained": hp_gained, "hp": character.hp, "max_hp": character.max_hp}
    
    elif request.action == "start-combat":
        enemy_type = request.data.get("enemy_type") if request.data else None
        if not enemy_type:
            enemy_type = random.choice(list(ENEMIES.keys()))
        
        enemy = ENEMIES[enemy_type].copy()
        enemy["current_hp"] = enemy["hp"]
        
        state["combat_state"] = {
            "enemy": enemy,
            "round": 1,
        }
        
        result["message"] = f"Combat started with {enemy['name']}"
        result["data"] = {"enemy": enemy, "character": character.to_dict()}
    
    game_states[request.game_id] = state
    return JSONResponse(result)


@app.post("/api/shop/purchase")
async def shop_purchase(request: ShopPurchaseRequest):
    """Purchase an item from the shop."""
    if request.game_id not in game_states:
        raise HTTPException(status_code=404, detail="Game not found")
    
    state = game_states[request.game_id]
    
    if request.item_key not in SHOP_ITEMS:
        raise HTTPException(status_code=400, detail="Item not found")
    
    item = SHOP_ITEMS[request.item_key]
    
    if state["gold"] < item["cost"]:
        raise HTTPException(status_code=400, detail="Not enough gold")
    
    state["gold"] -= item["cost"]
    state["inventory"].append(item["name"])
    
    # Apply equipment
    char_data = state["character"]
    character = DnD5eCharacter.from_dict(char_data)
    
    if item["type"] == "weapon":
        character.equipped_weapon = item["name"]
    elif item["type"] == "armor":
        if "ac" in item:
            character.armor_type = ArmorType.MEDIUM if item["ac"] >= 14 else ArmorType.LIGHT
            character.armor_base = item["ac"]
        elif "ac_bonus" in item:
            character.armor_base += item["ac_bonus"]
        character.equipped_armor = item["name"]
    
    state["character"] = character.to_dict()
    game_states[request.game_id] = state
    
    return JSONResponse({
        "success": True,
        "message": f"Purchased {item['name']}",
        "gold": state["gold"],
        "character": character.to_dict(),
    })


@app.get("/api/shop/items")
async def get_shop_items():
    """Get shop items list."""
    return JSONResponse({"items": SHOP_ITEMS})


@app.get("/api/spells")
async def get_spells():
    """Get available spells."""
    return JSONResponse({"spells": SPELLS})


@app.get("/api/locations")
async def get_locations():
    """Get available locations."""
    return JSONResponse({"locations": LOCATIONS})


@app.get("/api/game/{game_id}/inventory")
async def get_inventory(game_id: str):
    """Get detailed inventory."""
    if game_id not in game_states:
        raise HTTPException(status_code=404, detail="Game not found")
    
    state = game_states[game_id]
    inventory = state.get("inventory", [])
    
    # Build detailed inventory
    detailed = []
    for item_name in inventory:
        # Find item details
        item_details = None
        for key, item in SHOP_ITEMS.items():
            if item["name"] == item_name:
                item_details = item.copy()
                item_details["key"] = key
                break
        
        if not item_details:
            item_details = {"name": item_name, "type": "unknown"}
        
        detailed.append(item_details)
    
    return JSONResponse({"inventory": detailed})


@app.post("/api/game/{game_id}/save")
async def save_game(game_id: str):
    """Save game to file."""
    if game_id not in game_states:
        raise HTTPException(status_code=404, detail="Game not found")
    
    state = game_states[game_id]
    save_dir = Path(__file__).parent / "saves"
    save_dir.mkdir(exist_ok=True)
    
    save_file = save_dir / f"{game_id}.json"
    save_file.write_text(json.dumps(state, indent=2))
    
    return JSONResponse({
        "success": True,
        "message": "Game saved successfully",
        "save_file": str(save_file)
    })


@app.get("/api/saves")
async def list_saves():
    """List all saved games."""
    save_dir = Path(__file__).parent / "saves"
    save_dir.mkdir(exist_ok=True)
    
    saves = []
    for save_file in save_dir.glob("*.json"):
        try:
            data = json.loads(save_file.read_text())
            saves.append({
                "game_id": data.get("game_id", save_file.stem),
                "character_name": data.get("character", {}).get("name", "Unknown"),
                "level": data.get("character", {}).get("level", 1),
                "saved_at": save_file.stat().st_mtime
            })
        except:
            continue
    
    saves.sort(key=lambda x: x["saved_at"], reverse=True)
    return JSONResponse({"saves": saves})


@app.post("/api/game/{game_id}/load")
async def load_game(game_id: str):
    """Load game from file."""
    save_dir = Path(__file__).parent / "saves"
    save_file = save_dir / f"{game_id}.json"
    
    if not save_file.exists():
        raise HTTPException(status_code=404, detail="Save file not found")
    
    try:
        state = json.loads(save_file.read_text())
        game_states[game_id] = state
        return JSONResponse({
            "success": True,
            "message": "Game loaded successfully",
            "game_state": state
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading game: {e}")


@app.get("/api/quests")
async def get_quests():
    """Get available quests."""
    return JSONResponse({"quests": QUESTS})


@app.get("/api/game/{game_id}/quests")
async def get_game_quests(game_id: str):
    """Get quests for a specific game."""
    if game_id not in game_states:
        raise HTTPException(status_code=404, detail="Game not found")
    
    state = game_states[game_id]
    active_quests = [QUESTS[qid] for qid in state.get("active_quests", []) if qid in QUESTS]
    available_quests = [q for q in QUESTS.values() if q["id"] not in state.get("completed_quests", []) and q["id"] not in state.get("active_quests", [])]
    
    return JSONResponse({
        "active": active_quests,
        "available": available_quests,
        "completed": state.get("completed_quests", [])
    })


@app.post("/api/quest/action")
async def quest_action(request: QuestActionRequest):
    """Perform a quest action (accept, complete, abandon)."""
    if request.game_id not in game_states:
        raise HTTPException(status_code=404, detail="Game not found")
    
    if request.quest_id not in QUESTS:
        raise HTTPException(status_code=404, detail="Quest not found")
    
    state = game_states[request.game_id]
    quest = QUESTS[request.quest_id]
    
    if request.action == "accept":
        if request.quest_id in state.get("active_quests", []):
            raise HTTPException(status_code=400, detail="Quest already active")
        if request.quest_id in state.get("completed_quests", []):
            raise HTTPException(status_code=400, detail="Quest already completed")
        
        if "active_quests" not in state:
            state["active_quests"] = []
        state["active_quests"].append(request.quest_id)
        
        if "quest_progress" not in state:
            state["quest_progress"] = {}
        state["quest_progress"][request.quest_id] = {
            "objectives_completed": [],
            "objectives": quest["objectives"].copy()
        }
        
        game_states[request.game_id] = state
        
        return JSONResponse({
            "success": True,
            "message": f"Quest '{quest['name']}' accepted!",
            "quest": quest
        })
    
    elif request.action == "complete":
        if request.quest_id not in state.get("active_quests", []):
            raise HTTPException(status_code=400, detail="Quest not active")
        
        progress = state["quest_progress"].get(request.quest_id, {})
        objectives = progress.get("objectives", quest["objectives"])
        completed = progress.get("objectives_completed", [])
        
        if len(completed) < len(objectives):
            return JSONResponse({
                "success": False,
                "message": f"Quest not complete. {len(completed)}/{len(objectives)} objectives done."
            })
        
        # Give rewards
        rewards = quest["rewards"]
        state["gold"] += rewards.get("gold", 0)
        
        # Remove from active, add to completed
        state["active_quests"].remove(request.quest_id)
        if "completed_quests" not in state:
            state["completed_quests"] = []
        state["completed_quests"].append(request.quest_id)
        
        # Add item if reward has one
        if "item" in rewards:
            state["inventory"].append(rewards["item"])
        
        game_states[request.game_id] = state
        
        return JSONResponse({
            "success": True,
            "message": f"Quest '{quest['name']}' completed!",
            "rewards": rewards
        })
    
    elif request.action == "abandon":
        if request.quest_id not in state.get("active_quests", []):
            raise HTTPException(status_code=400, detail="Quest not active")
        
        state["active_quests"].remove(request.quest_id)
        if request.quest_id in state.get("quest_progress", {}):
            del state["quest_progress"][request.quest_id]
        
        game_states[request.game_id] = state
        
        return JSONResponse({
            "success": True,
            "message": f"Quest '{quest['name']}' abandoned."
        })
    
    else:
        raise HTTPException(status_code=400, detail="Invalid action")


@app.post("/api/combat/action")
async def combat_action(request: CombatActionRequest):
    """Perform a combat action."""
    if request.game_id not in game_states:
        raise HTTPException(status_code=404, detail="Game not found")
    
    state = game_states[request.game_id]
    
    if not state.get("combat_state"):
        raise HTTPException(status_code=400, detail="No active combat")
    
    char_data = state["character"]
    character = DnD5eCharacter.from_dict(char_data)
    combat = state["combat_state"]
    enemy = combat["enemy"]
    
    result = {
        "success": True,
        "round": combat["round"],
        "player_action": request.action,
        "player_result": {},
        "enemy_result": {},
        "combat_over": False,
        "victory": False,
    }
    
    # Player turn
    if request.action == "attack":
        attack_mod = character.str_modifier + character.proficiency_bonus
        hit, critical = DnD5eCombat.make_attack_roll(attack_mod, enemy["ac"])
        
        if hit:
            if character.equipped_weapon:
                if "sword" in character.equipped_weapon.lower():
                    damage_dice = "1d8"
                elif "dagger" in character.equipped_weapon.lower():
                    damage_dice = "1d4"
                else:
                    damage_dice = "1d6"
            else:
                damage_dice = "1d4"
            
            damage = DnDRoller.roll_damage(damage_dice) + character.str_modifier
            
            if critical:
                damage *= 2
                result["player_result"]["critical"] = True
            
            enemy["current_hp"] -= damage
            result["player_result"]["hit"] = True
            result["player_result"]["damage"] = damage
        else:
            result["player_result"]["hit"] = False
    
    elif request.action == "flee":
        flee_roll = DnDRoller.roll("1d20") + character.dex_modifier
        if flee_roll >= 15:
            state["combat_state"] = None
            result["combat_over"] = True
            result["victory"] = False
            result["message"] = "You successfully fled!"
            game_states[request.game_id] = state
            return JSONResponse(result)
        else:
            result["player_result"]["fled"] = False
    
    # Enemy turn (if still alive)
    if enemy["current_hp"] > 0 and not result["combat_over"]:
        enemy_attack = DnDRoller.roll("1d20") + 2
        if enemy_attack >= character.ac:
            enemy_damage = DnDRoller.roll_damage(enemy["damage"])
            DnD5eCombat.apply_damage(character, enemy_damage)
            result["enemy_result"]["hit"] = True
            result["enemy_result"]["damage"] = enemy_damage
        else:
            result["enemy_result"]["hit"] = False
    
    # Check victory/defeat
    if enemy["current_hp"] <= 0:
        state["combat_state"] = None
        result["combat_over"] = True
        result["victory"] = True
        
        xp_gain = enemy["xp"]
        gold_gain = random.randint(5, 15)
        state["gold"] += gold_gain
        state["encounters_completed"] += 1
        
        # Update quest progress
        if "active_quests" in state and state["active_quests"]:
            for quest_id in state["active_quests"]:
                if quest_id in state.get("quest_progress", {}):
                    progress = state["quest_progress"][quest_id]
                    objectives = progress.get("objectives", [])
                    completed = progress.get("objectives_completed", [])
                    
                    # Check if this enemy type matches quest objective
                    if "defeat_goblin" in objectives and enemy_type == "goblin" and "defeat_goblin" not in completed:
                        completed.append("defeat_goblin")
                        progress["objectives_completed"] = completed
                    elif "defeat_guardian" in objectives and enemy_type in ["skeleton", "orc"] and "defeat_guardian" not in completed:
                        completed.append("defeat_guardian")
                        progress["objectives_completed"] = completed
        
        # Simple leveling (every 3 encounters)
        if state["encounters_completed"] % 3 == 0:
            character.level += 1
            hp_gain = DnDRoller.roll(f"1d{character.hit_die}") + character.con_modifier
            character.max_hp += hp_gain
            character.hp += hp_gain
            result["level_up"] = True
            result["new_level"] = character.level
            result["hp_gained"] = hp_gain
        
        result["xp_gain"] = xp_gain
        result["gold_gain"] = gold_gain
        result["message"] = f"Victory! Gained {xp_gain} XP and {gold_gain} gp"
    
    elif character.hp <= 0:
        state["combat_state"] = None
        result["combat_over"] = True
        result["victory"] = False
        result["message"] = "You have been defeated!"
    
    else:
        combat["round"] += 1
    
    state["character"] = character.to_dict()
    state["combat_state"] = combat if not result["combat_over"] else None
    game_states[request.game_id] = state
    
    result["character"] = character.to_dict()
    result["enemy"] = enemy
    
    return JSONResponse(result)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
