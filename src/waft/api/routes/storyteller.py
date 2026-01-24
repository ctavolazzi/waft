"""
Storyteller API Routes - Dynamic Visual Novel
==============================================

API for the AI-powered storytelling engine.
Creates stories in real-time based on player actions.
"""

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel

from ...core.storyteller import GameState, get_storyteller

router = APIRouter(prefix="/story", tags=["storyteller"])

# Path to pixel art assets
ASSETS_DIR = Path(__file__).parent.parent.parent.parent.parent / "assets" / "pixellab" / "sprites"

# In-memory session storage (use Redis/DB in production)
_sessions: dict[str, GameState] = {}


class StartGameRequest(BaseModel):
    setting: str = "fantasy_tavern"  # fantasy_tavern, space_station, noir_city
    seed: int | None = None  # Optional world seed for reproducible generation


class ActionRequest(BaseModel):
    session_id: str
    action: str  # What the player does (can be free-form or a choice)


class GameResponse(BaseModel):
    session_id: str
    narrative: str
    speaker: str | None = None
    scene: str | None = None
    mood: str | None = None
    choices: list[str] = []
    state: dict  # Current game state
    world_seed: int | None = None  # World seed if procedural generation was used


@router.post("/start", response_model=GameResponse)
async def start_game(request: StartGameRequest):
    """Start a new storytelling session with optional procedural world generation."""
    storyteller = get_storyteller()
    state, response = storyteller.start_game(request.setting, seed=request.seed)

    # Store session
    _sessions[state.session_id] = state

    return GameResponse(
        session_id=state.session_id,
        narrative=response.get("narrative", ""),
        speaker=response.get("speaker"),
        scene=response.get("scene", state.location),
        mood=response.get("mood", state.mood),
        choices=response.get("choices", []),
        state=state.to_dict(),
        world_seed=state.world_seed,
    )


@router.post("/action", response_model=GameResponse)
async def take_action(request: ActionRequest):
    """Process a player action."""
    if request.session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    state = _sessions[request.session_id]
    storyteller = get_storyteller()

    response = storyteller.take_action(state, request.action)

    return GameResponse(
        session_id=state.session_id,
        narrative=response.get("narrative", ""),
        speaker=response.get("speaker"),
        scene=response.get("scene", state.location),
        mood=response.get("mood", state.mood),
        choices=response.get("choices", []),
        state=state.to_dict(),
        world_seed=state.world_seed,
    )


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """Get current session state."""
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    state = _sessions[session_id]
    return {"session_id": session_id, "state": state.to_dict()}


# ============================================================================
# World Generation Endpoints
# ============================================================================

@router.get("/world/{session_id}")
async def get_world(session_id: str):
    """Get the current world state for a session."""
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    state = _sessions[session_id]
    storyteller = get_storyteller()
    world_manager = storyteller.get_world_manager(session_id)

    if not world_manager:
        return {
            "session_id": session_id,
            "has_generated_world": False,
            "world_context": state.world_context if state.world_context else None,
        }

    return {
        "session_id": session_id,
        "has_generated_world": True,
        "world_seed": state.world_seed,
        "current_location": world_manager.state.current_location_id,
        "locations": {
            k: {"name": v.name, "type": v.location_type, "visited": v.visited}
            for k, v in world_manager.state.locations.items()
        },
        "known_npcs": [npc.short_description() for npc in world_manager.state.npcs.values()],
        "active_quests": world_manager.state.active_quests,
        "rumors": world_manager.state.rumors[:5],
    }


@router.get("/npcs/{session_id}")
async def get_npcs(session_id: str):
    """Get all known NPCs for a session."""
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    state = _sessions[session_id]
    storyteller = get_storyteller()
    world_manager = storyteller.get_world_manager(session_id)

    if not world_manager:
        # Fallback to basic character tracking
        return {
            "session_id": session_id,
            "characters_met": state.characters_met,
        }

    npcs = []
    for npc in world_manager.state.npcs.values():
        npcs.append({
            "name": npc.name,
            "race": npc.race,
            "occupation": npc.occupation,
            "description": npc.description(),
            "personality": npc.personality_traits,
            "is_staff": npc.is_staff,
        })

    return {
        "session_id": session_id,
        "npcs": npcs,
        "count": len(npcs),
    }


@router.post("/generate-location/{session_id}")
async def generate_location(session_id: str, location_type: str = "tavern"):
    """Generate a new location and connect it to the current world."""
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    storyteller = get_storyteller()
    world_manager = storyteller.get_world_manager(session_id)

    if not world_manager:
        raise HTTPException(status_code=400, detail="Session does not have procedural world generation enabled")

    # Generate new location connected to current
    current_location_id = world_manager.state.current_location_id
    new_location = world_manager.generate_location(
        location_type=location_type,
        connected_to=current_location_id,
    )

    return {
        "session_id": session_id,
        "new_location": {
            "id": new_location.id,
            "name": new_location.name,
            "type": new_location.location_type,
            "description": new_location.description,
        },
        "connected_to": current_location_id,
    }


@router.get("/sprites/{name}")
async def get_sprite(name: str):
    """Get a character sprite by name (grok, bard, stranger)."""
    # Sanitize name
    safe_name = name.lower().replace("..", "").replace("/", "")
    if not safe_name.endswith(".png"):
        safe_name = f"{safe_name}.png"

    sprite_path = ASSETS_DIR / safe_name
    if not sprite_path.exists():
        raise HTTPException(status_code=404, detail=f"Sprite '{name}' not found")

    return FileResponse(sprite_path, media_type="image/png")


# ============================================================================
# Visual Novel UI
# ============================================================================

PLAYER_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>WAFT - AI Storyteller</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-deep: #05050a;
            --text-primary: #f0f0f5;
            --text-dialogue: #ffffff;
            --accent: #c9a227;
            --accent-glow: #e6c347;
            --dialogue-bg: rgba(8, 8, 16, 0.94);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        html, body { height: 100%; overflow: hidden; }

        body {
            font-family: 'Crimson Text', Georgia, serif;
            background: var(--bg-deep);
            color: var(--text-primary);
        }

        /* Title Screen */
        #title-screen {
            position: fixed; inset: 0;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            background: linear-gradient(180deg, #0a0a15 0%, #151525 50%, #0a0a15 100%);
            z-index: 100;
            transition: opacity 0.8s ease, visibility 0.8s;
        }
        #title-screen.hidden { opacity: 0; visibility: hidden; }

        .title-logo {
            font-family: 'Cinzel', serif;
            font-size: 5rem; font-weight: 700; letter-spacing: 0.4em;
            background: linear-gradient(135deg, var(--accent) 0%, #fff 50%, var(--accent) 100%);
            background-size: 200% auto;
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            animation: shimmer 3s ease-in-out infinite;
            margin-bottom: 0.5rem;
        }
        @keyframes shimmer { 0%, 100% { background-position: 0% center; } 50% { background-position: 200% center; } }

        .title-tagline {
            font-family: 'Cinzel', serif;
            font-size: 1rem; letter-spacing: 0.5em;
            color: rgba(255,255,255,0.4);
            text-transform: uppercase;
            margin-bottom: 3rem;
        }

        .setting-select { display: flex; flex-direction: column; gap: 1rem; width: 100%; max-width: 400px; padding: 0 2rem; }

        .setting-btn {
            background: linear-gradient(135deg, rgba(30,30,50,0.8), rgba(20,20,35,0.9));
            border: 1px solid rgba(201, 162, 39, 0.3);
            border-radius: 4px; padding: 1.2rem 1.5rem;
            color: var(--text-primary);
            font-family: 'Cinzel', serif; font-size: 1.1rem;
            cursor: pointer; transition: all 0.3s ease; text-align: left;
        }
        .setting-btn:hover {
            background: linear-gradient(135deg, rgba(201, 162, 39, 0.2), rgba(201, 162, 39, 0.1));
            border-color: var(--accent); transform: translateX(10px);
        }
        .setting-btn .desc { font-family: 'Crimson Text', serif; font-size: 0.9rem; color: rgba(255,255,255,0.4); margin-top: 0.3rem; }

        /* Game Screen */
        #game-screen { position: fixed; inset: 0; display: none; }
        #game-screen.active { display: block; }

        /* Scenes */
        .scene-bg { position: absolute; inset: 0; transition: all 1s ease; }

        .scene-tavern { background: radial-gradient(ellipse at 30% 70%, rgba(255, 140, 50, 0.25) 0%, transparent 50%), radial-gradient(ellipse at 70% 80%, rgba(255, 100, 30, 0.2) 0%, transparent 40%), linear-gradient(180deg, #1a0f08 0%, #2d1810 40%, #1a0f08 100%); }
        .scene-forest { background: radial-gradient(ellipse at 30% 30%, rgba(50, 150, 80, 0.15) 0%, transparent 50%), linear-gradient(180deg, #0a1510 0%, #0d1a12 50%, #050a08 100%); }
        .scene-road { background: radial-gradient(ellipse at 50% 20%, rgba(100, 120, 180, 0.15) 0%, transparent 50%), linear-gradient(180deg, #0a0f1a 0%, #151d2e 50%, #0a0a12 100%); }
        .scene-cave { background: radial-gradient(ellipse at 50% 80%, rgba(100, 80, 60, 0.1) 0%, transparent 40%), linear-gradient(180deg, #050505 0%, #0a0808 50%, #030303 100%); }
        .scene-castle { background: radial-gradient(ellipse at 50% 30%, rgba(100, 100, 150, 0.1) 0%, transparent 50%), linear-gradient(180deg, #0a0a15 0%, #15152a 50%, #0a0a10 100%); }
        .scene-village { background: radial-gradient(ellipse at 60% 70%, rgba(200, 150, 100, 0.15) 0%, transparent 50%), linear-gradient(180deg, #1a1510 0%, #252015 50%, #0f0d0a 100%); }
        .scene-shop { background: radial-gradient(ellipse at 50% 60%, rgba(255, 200, 100, 0.15) 0%, transparent 50%), linear-gradient(180deg, #15100a 0%, #201810 50%, #0a0805 100%); }
        .scene-battlefield { background: radial-gradient(ellipse at 50% 50%, rgba(200, 50, 50, 0.1) 0%, transparent 60%), linear-gradient(180deg, #0a0505 0%, #150808 50%, #050303 100%); }
        .scene-station_hub { background: radial-gradient(ellipse at 50% 50%, rgba(100, 150, 255, 0.1) 0%, transparent 50%), linear-gradient(180deg, #05080a 0%, #0a1015 50%, #030508 100%); }
        .scene-office { background: radial-gradient(ellipse at 30% 70%, rgba(100, 80, 60, 0.15) 0%, transparent 50%), linear-gradient(180deg, #0a0808 0%, #151010 50%, #050505 100%); }

        /* Mood overlays */
        .mood-overlay { position: absolute; inset: 0; pointer-events: none; transition: all 1s ease; }
        .mood-warm .mood-overlay { background: radial-gradient(ellipse at 50% 100%, rgba(255, 150, 50, 0.1) 0%, transparent 60%); }
        .mood-mysterious .mood-overlay { background: radial-gradient(ellipse at 50% 50%, rgba(100, 50, 200, 0.08) 0%, transparent 70%); }
        .mood-tense .mood-overlay { background: linear-gradient(180deg, rgba(0,0,0,0.2) 0%, transparent 30%, transparent 70%, rgba(0,0,0,0.3) 100%); }
        .mood-peaceful .mood-overlay { background: radial-gradient(ellipse at 50% 30%, rgba(100, 200, 255, 0.05) 0%, transparent 60%); }
        .mood-danger .mood-overlay { background: radial-gradient(ellipse at 50% 50%, rgba(200, 50, 50, 0.08) 0%, transparent 60%); animation: pulse-danger 2s ease-in-out infinite; }
        @keyframes pulse-danger { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
        .mood-romantic .mood-overlay { background: radial-gradient(ellipse at 50% 50%, rgba(255, 100, 150, 0.05) 0%, transparent 60%); }
        .mood-sad .mood-overlay { background: linear-gradient(180deg, rgba(50, 50, 100, 0.1) 0%, transparent 50%); }
        .mood-excited .mood-overlay { background: radial-gradient(ellipse at 50% 50%, rgba(255, 200, 50, 0.08) 0%, transparent 60%); }

        .vignette { position: absolute; inset: 0; background: radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.7) 100%); pointer-events: none; }

        /* Particles */
        .particles { position: absolute; inset: 0; overflow: hidden; pointer-events: none; }
        .particle { position: absolute; width: 2px; height: 2px; background: var(--accent); border-radius: 50%; opacity: 0; animation: float-up 12s ease-in-out infinite; }
        @keyframes float-up { 0% { opacity: 0; transform: translateY(100vh) scale(0); } 10% { opacity: 0.6; } 90% { opacity: 0.3; } 100% { opacity: 0; transform: translateY(-20vh) scale(1); } }

        /* Nav */
        .vn-nav { position: absolute; top: 1rem; left: 1rem; right: 1rem; display: flex; justify-content: space-between; align-items: center; z-index: 10; }
        .nav-btn { background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); color: rgba(255,255,255,0.6); font-family: 'Cinzel', serif; font-size: 0.75rem; letter-spacing: 0.1em; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; transition: all 0.3s ease; text-transform: uppercase; }
        .nav-btn:hover { background: rgba(201, 162, 39, 0.2); border-color: var(--accent); color: var(--accent); }

        .status-bar { display: flex; gap: 1rem; font-size: 0.8rem; color: rgba(255,255,255,0.5); }
        .status-bar span { background: rgba(0,0,0,0.5); padding: 0.3rem 0.8rem; border-radius: 4px; }

        /* Dialogue */
        .dialogue-container { position: absolute; bottom: 0; left: 0; right: 0; padding: 0 2rem 2rem; transition: bottom 0.3s ease; }
        .dialogue-container.with-choices { bottom: 220px; }
        .dialogue-box {
            background: var(--dialogue-bg);
            border: 1px solid rgba(201, 162, 39, 0.3);
            border-radius: 8px;
            padding: 1.5rem 2rem 1.8rem;
            max-width: 900px; margin: 0 auto;
            position: relative;
            backdrop-filter: blur(10px);
        }

        .nameplate {
            position: absolute; top: -18px; left: 24px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: #000; font-family: 'Cinzel', serif; font-size: 0.9rem; font-weight: 600;
            padding: 0.4rem 1.2rem; border-radius: 4px; letter-spacing: 0.1em;
        }

        /* Character sprites */
        .speaker-sprite {
            position: absolute;
            bottom: 100%; left: 50px;
            width: 128px; height: 128px;
            image-rendering: pixelated;
            transform: translateY(20px);
            opacity: 0;
            transition: all 0.4s ease;
            filter: drop-shadow(0 4px 12px rgba(0,0,0,0.6));
        }
        .speaker-sprite.visible { transform: translateY(0); opacity: 1; }

        .dialogue-text { font-size: 1.2rem; line-height: 1.8; color: var(--text-dialogue); min-height: 60px; }
        .dialogue-text p { margin-bottom: 0.8rem; }
        .dialogue-text strong { color: var(--accent); }
        .dialogue-text em { color: rgba(255,255,255,0.7); font-style: italic; }

        .cursor { display: inline-block; width: 2px; height: 1.2em; background: var(--accent); margin-left: 2px; animation: blink 1s step-end infinite; vertical-align: text-bottom; }
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

        /* Input area */
        .input-area { position: absolute; bottom: 0; left: 0; right: 0; padding: 1rem 2rem 2rem; display: none; }
        .input-area.visible { display: block; }

        .input-box {
            background: var(--dialogue-bg);
            border: 1px solid rgba(201, 162, 39, 0.3);
            border-radius: 8px; padding: 1.5rem;
            max-width: 800px; margin: 0 auto;
            backdrop-filter: blur(10px);
        }

        .choices { display: flex; flex-direction: column; gap: 0.6rem; margin-bottom: 1rem; }
        .choice-btn {
            background: rgba(30, 30, 50, 0.8);
            border: 1px solid rgba(201, 162, 39, 0.2);
            border-left: 3px solid transparent;
            border-radius: 4px; padding: 0.8rem 1rem;
            color: var(--text-primary);
            font-family: 'Crimson Text', serif; font-size: 1rem;
            cursor: pointer; transition: all 0.3s ease; text-align: left;
        }
        .choice-btn:hover { background: rgba(201, 162, 39, 0.15); border-color: var(--accent); border-left-color: var(--accent); transform: translateX(8px); color: #fff; }

        .or-divider { text-align: center; color: rgba(255,255,255,0.3); font-size: 0.8rem; margin: 1rem 0; text-transform: uppercase; letter-spacing: 0.2em; }

        .custom-input {
            display: flex; gap: 0.5rem;
        }
        .custom-input input {
            flex: 1;
            background: rgba(20, 20, 35, 0.8);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 4px; padding: 0.8rem 1rem;
            color: var(--text-primary);
            font-family: 'Crimson Text', serif; font-size: 1rem;
        }
        .custom-input input:focus { outline: none; border-color: var(--accent); }
        .custom-input input::placeholder { color: rgba(255,255,255,0.3); }

        .custom-input button {
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            border: none; border-radius: 4px; padding: 0.8rem 1.5rem;
            color: #000; font-family: 'Cinzel', serif; font-size: 0.9rem;
            cursor: pointer; transition: all 0.3s ease;
        }
        .custom-input button:hover { transform: translateY(-2px); box-shadow: 0 5px 20px rgba(201, 162, 39, 0.3); }
        .custom-input button:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

        /* Loading */
        .loading { display: none; align-items: center; justify-content: center; gap: 0.5rem; color: rgba(255,255,255,0.5); padding: 1rem; }
        .loading.visible { display: flex; }
        .loading-dot { width: 8px; height: 8px; background: var(--accent); border-radius: 50%; animation: loading-bounce 1.4s ease-in-out infinite; }
        .loading-dot:nth-child(1) { animation-delay: 0s; }
        .loading-dot:nth-child(2) { animation-delay: 0.2s; }
        .loading-dot:nth-child(3) { animation-delay: 0.4s; }
        @keyframes loading-bounce { 0%, 80%, 100% { transform: scale(0.6); opacity: 0.5; } 40% { transform: scale(1); opacity: 1; } }

        /* Transitions */
        .scene-transition { position: absolute; inset: 0; background: #000; opacity: 0; pointer-events: none; transition: opacity 0.5s ease; z-index: 50; }
        .scene-transition.active { opacity: 1; }

        @media (max-width: 768px) {
            .title-logo { font-size: 3rem; }
            .dialogue-box { padding: 1.2rem 1.5rem; }
            .dialogue-text { font-size: 1rem; }
            .choice-btn { padding: 0.7rem 0.8rem; font-size: 0.95rem; }
        }
    </style>
</head>
<body>
    <div id="title-screen">
        <h1 class="title-logo">WAFT</h1>
        <p class="title-tagline">AI Storyteller</p>
        <div class="setting-select">
            <button class="setting-btn" onclick="startGame('fantasy_tavern')">
                Fantasy Tavern
                <div class="desc">Magic, mystery, and adventure await</div>
            </button>
            <button class="setting-btn" onclick="startGame('space_station')">
                Space Station
                <div class="desc">Sci-fi intrigue among the stars</div>
            </button>
            <button class="setting-btn" onclick="startGame('noir_city')">
                Noir Detective
                <div class="desc">Rain-soaked streets and dark secrets</div>
            </button>
        </div>
    </div>

    <div id="game-screen">
        <div id="scene-bg" class="scene-bg scene-tavern"></div>
        <div class="mood-overlay"></div>
        <div class="particles" id="particles"></div>
        <div class="vignette"></div>
        <div id="scene-transition" class="scene-transition"></div>

        <div class="vn-nav">
            <button class="nav-btn" onclick="backToTitle()">Menu</button>
            <div class="status-bar">
                <span id="status-location">Tavern</span>
                <span id="status-gold">Gold: 10</span>
            </div>
        </div>

        <div class="dialogue-container" id="dialogue-container">
            <div class="dialogue-box">
                <img class="speaker-sprite" id="speaker-sprite" src="" alt="" />
                <div class="nameplate" id="nameplate" style="display:none;"></div>
                <div class="dialogue-text" id="dialogue-text"></div>
            </div>
        </div>

        <div class="input-area" id="input-area">
            <div class="input-box">
                <div class="choices" id="choices"></div>
                <div class="or-divider">or type your own action</div>
                <div class="custom-input">
                    <input type="text" id="custom-action" placeholder="What do you do?" />
                    <button onclick="submitAction()" id="submit-btn">Do It</button>
                </div>
            </div>
        </div>

        <div class="loading" id="loading">
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <span>The story unfolds...</span>
        </div>
    </div>

    <script>
        const API_BASE = '/api/story';
        let sessionId = null;
        let gameState = null;
        let isTyping = false;
        let typewriterTimeout = null;

        function createParticles() {
            const c = document.getElementById('particles'); c.innerHTML = '';
            for (let i = 0; i < 15; i++) {
                const p = document.createElement('div'); p.className = 'particle';
                p.style.left = Math.random() * 100 + '%';
                p.style.animationDelay = Math.random() * 12 + 's';
                p.style.animationDuration = (10 + Math.random() * 8) + 's';
                c.appendChild(p);
            }
        }

        async function startGame(setting) {
            document.getElementById('title-screen').classList.add('hidden');
            document.getElementById('game-screen').classList.add('active');
            createParticles();
            showLoading(true);

            try {
                const res = await fetch(API_BASE + '/start', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({setting: setting, player_name: 'Traveler'})
                });
                const data = await res.json();

                sessionId = data.session_id;
                gameState = data.state;

                updateScene(data.scene, data.mood);
                updateStatus();
                showLoading(false);
                showNarrative(data.narrative, data.speaker, data.choices);
            } catch (e) {
                console.error(e);
                showLoading(false);
                document.getElementById('dialogue-text').innerHTML = '<p style="color:#ef4444;">Failed to start game. Check console for errors.</p>';
            }
        }

        async function submitAction(choiceText = null) {
            const input = document.getElementById('custom-action');
            const action = choiceText || input.value.trim();

            if (!action) return;

            input.value = '';
            document.getElementById('input-area').classList.remove('visible');
            document.getElementById('dialogue-container').classList.remove('with-choices');
            showLoading(true);

            try {
                const res = await fetch(API_BASE + '/action', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({session_id: sessionId, action: action})
                });
                const data = await res.json();

                gameState = data.state;

                // Scene transition if location changed
                const transition = document.getElementById('scene-transition');
                if (data.scene && data.scene !== getCurrentScene()) {
                    transition.classList.add('active');
                    await new Promise(r => setTimeout(r, 500));
                }

                updateScene(data.scene, data.mood);
                updateStatus();

                transition.classList.remove('active');
                await new Promise(r => setTimeout(r, 300));

                showLoading(false);
                showNarrative(data.narrative, data.speaker, data.choices);
            } catch (e) {
                console.error(e);
                showLoading(false);
            }
        }

        function getCurrentScene() {
            const bg = document.getElementById('scene-bg');
            const classes = Array.from(bg.classList);
            const sceneClass = classes.find(c => c.startsWith('scene-') && c !== 'scene-bg');
            return sceneClass ? sceneClass.replace('scene-', '') : 'tavern';
        }

        function updateScene(scene, mood) {
            const bg = document.getElementById('scene-bg');
            const game = document.getElementById('game-screen');

            bg.className = 'scene-bg';
            game.className = 'active';

            bg.classList.add('scene-' + (scene || 'tavern'));
            if (mood) game.classList.add('mood-' + mood);
        }

        function updateStatus() {
            if (!gameState) return;
            document.getElementById('status-location').textContent = capitalize(gameState.location || 'Unknown');
            document.getElementById('status-gold').textContent = 'Gold: ' + (gameState.gold || 0);
        }

        function capitalize(s) { return s.charAt(0).toUpperCase() + s.slice(1).replace(/_/g, ' '); }

        function showLoading(show) {
            document.getElementById('loading').classList.toggle('visible', show);
            document.getElementById('dialogue-container').style.display = show ? 'none' : 'block';
        }

        // Sprite mapping: speaker name -> sprite filename
        const SPEAKER_SPRITES = {
            'grok': 'grok',
            'the stranger': 'stranger',
            'stranger': 'stranger',
            'bard': 'bard',
            'tavern bard': 'bard',
        };

        function showNarrative(text, speaker, choices) {
            document.getElementById('dialogue-container').style.display = 'block';

            const np = document.getElementById('nameplate');
            const sprite = document.getElementById('speaker-sprite');

            if (speaker) {
                np.textContent = speaker;
                np.style.display = 'block';

                // Show character sprite if available
                const spriteKey = speaker.toLowerCase();
                const spriteFile = SPEAKER_SPRITES[spriteKey];
                if (spriteFile) {
                    sprite.src = '/api/story/sprites/' + spriteFile;
                    sprite.classList.add('visible');
                } else {
                    sprite.classList.remove('visible');
                }
            } else {
                np.style.display = 'none';
                sprite.classList.remove('visible');
            }

            // Convert markdown-ish to HTML
            let html = text
                .replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>')
                .replace(/\\*(.+?)\\*/g, '<em>$1</em>')
                .split('\\n\\n').map(p => '<p>' + p + '</p>').join('');

            typewriterEffect(html, () => {
                showChoices(choices || []);
            });
        }

        function typewriterEffect(html, callback) {
            const c = document.getElementById('dialogue-text');
            c.innerHTML = '';
            isTyping = true;

            const temp = document.createElement('div'); temp.innerHTML = html;
            const text = temp.textContent || temp.innerText;
            let i = 0;

            function type() {
                if (i < text.length) {
                    c.innerHTML = html.substring(0, findHtmlIndex(html, i)) + '<span class="cursor"></span>';
                    i++;
                    typewriterTimeout = setTimeout(type, 20);
                } else {
                    c.innerHTML = html;
                    isTyping = false;
                    if (callback) callback();
                }
            }
            type();
        }

        function findHtmlIndex(html, textIndex) {
            let tc = 0, inTag = false;
            for (let i = 0; i < html.length; i++) {
                if (html[i] === '<') inTag = true;
                else if (html[i] === '>') inTag = false;
                else if (!inTag) { tc++; if (tc > textIndex) return i; }
            }
            return html.length;
        }

        function skipTypewriter() {
            if (isTyping && typewriterTimeout) {
                clearTimeout(typewriterTimeout);
                // Just show full text
                isTyping = false;
            }
        }

        function showChoices(choices) {
            const container = document.getElementById('choices');
            container.innerHTML = choices.map(c =>
                '<button class="choice-btn" onclick="submitAction(\\'' + c.replace(/'/g, "\\\\'") + '\\')">' + c + '</button>'
            ).join('');

            // Move dialogue up to make room for choices
            document.getElementById('dialogue-container').classList.add('with-choices');
            document.getElementById('input-area').classList.add('visible');
            document.getElementById('custom-action').focus();
        }

        function backToTitle() {
            document.getElementById('game-screen').classList.remove('active');
            document.getElementById('title-screen').classList.remove('hidden');
            sessionId = null;
            gameState = null;
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', e => {
            if (e.code === 'Enter' && document.activeElement.id === 'custom-action') {
                submitAction();
            }
            if (e.code === 'Escape') {
                backToTitle();
            }
            if (e.code === 'Space' && isTyping) {
                skipTypewriter();
            }
        });

        // Click to skip typewriter
        document.getElementById('dialogue-container').addEventListener('click', () => {
            if (isTyping) skipTypewriter();
        });
    </script>
</body>
</html>
"""


@router.get("/play", response_class=HTMLResponse)
async def play_storyteller():
    """Serve the AI storyteller visual novel UI."""
    return HTMLResponse(content=PLAYER_HTML)
