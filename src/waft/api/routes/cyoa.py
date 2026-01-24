"""
CYOA API Routes - Choose Your Own Adventure
============================================

REST API for the CYOA story engine.
Serves stories and provides a web-based player UI.
"""

from pathlib import Path
from typing import Any

import markdown
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from ...core.cyoa import Choice, Page, Story, load_all_stories, load_story

router = APIRouter(prefix="/cyoa", tags=["cyoa"])


# ============================================================================
# Pydantic Schemas
# ============================================================================


class ChoiceResponse(BaseModel):
    """A choice option."""
    text: str
    path: str


class PageResponse(BaseModel):
    """A story page."""
    id: str
    title: str
    content_html: str
    content_md: str
    choices: list[ChoiceResponse]
    is_ending: bool
    # Visual novel fields
    scene: str | None = None
    speaker: str | None = None
    mood: str | None = None
    portrait: str | None = None


class StoryMetaResponse(BaseModel):
    """Story metadata (without full content)."""
    name: str
    start_page: str
    page_count: int
    ending_count: int


class StoryListResponse(BaseModel):
    """List of available stories."""
    stories: list[StoryMetaResponse]
    total: int


class StoryGraphResponse(BaseModel):
    """Story graph for visualization."""
    name: str
    nodes: list[dict[str, Any]]
    edges: list[dict[str, Any]]


class ValidationResponse(BaseModel):
    """Story validation result."""
    valid: bool
    errors: list[str]


# ============================================================================
# Helper Functions
# ============================================================================


def get_stories_dir(request: Request) -> Path:
    """Get the stories directory for the current project."""
    project_path: Path = request.app.state.project_path
    return project_path / "_stories"


def page_to_response(page: Page) -> PageResponse:
    """Convert Page to response model."""
    # Convert Markdown to HTML
    md = markdown.Markdown(extensions=["extra", "smarty", "nl2br"])
    content_html = md.convert(page.content)

    return PageResponse(
        id=page.id,
        title=page.title,
        content_html=content_html,
        content_md=page.content,
        choices=[ChoiceResponse(text=c.text, path=c.path) for c in page.choices],
        is_ending=page.is_ending,
        scene=page.scene,
        speaker=page.speaker,
        mood=page.mood,
        portrait=page.portrait,
    )


def story_to_meta(story: Story) -> StoryMetaResponse:
    """Convert Story to metadata response."""
    ending_count = sum(1 for p in story.pages.values() if p.is_ending)
    return StoryMetaResponse(
        name=story.name,
        start_page=story.start_page,
        page_count=len(story.pages),
        ending_count=ending_count,
    )


# ============================================================================
# API Endpoints
# ============================================================================


@router.get("", response_model=StoryListResponse)
async def list_stories(request: Request):
    """
    List all available stories.

    Returns metadata for each story found in the _stories directory.
    """
    stories_dir = get_stories_dir(request)
    stories = load_all_stories(stories_dir)

    return StoryListResponse(
        stories=[story_to_meta(s) for s in stories.values()],
        total=len(stories),
    )


# ============================================================================
# Web Player UI (must be before /{story_name} catch-all)
# ============================================================================


PLAYER_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>WAFT - Visual Novel</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-deep: #05050a;
            --text-primary: #f0f0f5;
            --text-dialogue: #ffffff;
            --accent: #c9a227;
            --accent-glow: #e6c347;
            --dialogue-bg: rgba(8, 8, 16, 0.94);
            --nameplate-bg: rgba(201, 162, 39, 0.9);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        html, body { height: 100%; overflow: hidden; }

        body {
            font-family: 'Crimson Text', Georgia, serif;
            background: var(--bg-deep);
            color: var(--text-primary);
        }

        /* ============ TITLE SCREEN ============ */
        #title-screen {
            position: fixed;
            inset: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: linear-gradient(180deg, #0a0a15 0%, #151525 50%, #0a0a15 100%);
            z-index: 100;
            transition: opacity 0.8s ease, visibility 0.8s;
        }

        #title-screen.hidden { opacity: 0; visibility: hidden; }

        .title-logo {
            font-family: 'Cinzel', serif;
            font-size: 5rem;
            font-weight: 700;
            letter-spacing: 0.4em;
            background: linear-gradient(135deg, var(--accent) 0%, #fff 50%, var(--accent) 100%);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shimmer 3s ease-in-out infinite;
            text-shadow: 0 0 60px rgba(201, 162, 39, 0.5);
            margin-bottom: 0.5rem;
        }

        @keyframes shimmer {
            0%, 100% { background-position: 0% center; }
            50% { background-position: 200% center; }
        }

        .title-tagline {
            font-family: 'Cinzel', serif;
            font-size: 1rem;
            letter-spacing: 0.5em;
            color: rgba(255,255,255,0.4);
            text-transform: uppercase;
            margin-bottom: 4rem;
        }

        .story-select { display: flex; flex-direction: column; gap: 1rem; width: 100%; max-width: 400px; padding: 0 2rem; }

        .story-btn {
            background: linear-gradient(135deg, rgba(30,30,50,0.8), rgba(20,20,35,0.9));
            border: 1px solid rgba(201, 162, 39, 0.3);
            border-radius: 4px;
            padding: 1.2rem 1.5rem;
            color: var(--text-primary);
            font-family: 'Cinzel', serif;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: left;
        }

        .story-btn:hover {
            background: linear-gradient(135deg, rgba(201, 162, 39, 0.2), rgba(201, 162, 39, 0.1));
            border-color: var(--accent);
            transform: translateX(10px);
            box-shadow: 0 0 30px rgba(201, 162, 39, 0.2);
        }

        .story-btn .meta { font-family: 'Crimson Text', serif; font-size: 0.85rem; color: rgba(255,255,255,0.4); margin-top: 0.3rem; }

        /* ============ VN GAME SCREEN ============ */
        #vn-screen { position: fixed; inset: 0; display: none; }
        #vn-screen.active { display: block; }

        .scene-bg { position: absolute; inset: 0; background-size: cover; background-position: center; transition: opacity 1s ease; }

        /* Scene backgrounds */
        .scene-tavern {
            background: radial-gradient(ellipse at 30% 70%, rgba(255, 140, 50, 0.25) 0%, transparent 50%),
                        radial-gradient(ellipse at 70% 80%, rgba(255, 100, 30, 0.2) 0%, transparent 40%),
                        linear-gradient(180deg, #1a0f08 0%, #2d1810 40%, #1a0f08 100%);
        }
        .scene-tavern::before {
            content: ''; position: absolute; inset: 0;
            background-image: repeating-linear-gradient(90deg, transparent, transparent 80px, rgba(60,40,20,0.3) 80px, rgba(60,40,20,0.3) 82px),
                              repeating-linear-gradient(0deg, transparent, transparent 30px, rgba(40,25,15,0.2) 30px, rgba(40,25,15,0.2) 32px);
            opacity: 0.5;
        }

        .scene-tavern_dark {
            background: radial-gradient(ellipse at 80% 90%, rgba(100, 50, 200, 0.15) 0%, transparent 40%),
                        radial-gradient(ellipse at 20% 70%, rgba(255, 100, 30, 0.1) 0%, transparent 50%),
                        linear-gradient(180deg, #0a0510 0%, #150d18 40%, #0a0510 100%);
        }

        .scene-night_road {
            background: radial-gradient(ellipse at 50% 20%, rgba(100, 120, 180, 0.15) 0%, transparent 50%),
                        radial-gradient(ellipse at 50% 100%, rgba(20, 30, 50, 0.8) 0%, transparent 60%),
                        linear-gradient(180deg, #0a0f1a 0%, #151d2e 50%, #0a0a12 100%);
        }

        .scene-mill_interior {
            background: radial-gradient(ellipse at 50% 50%, rgba(50, 200, 100, 0.2) 0%, transparent 50%),
                        linear-gradient(180deg, #0a0a08 0%, #12120f 50%, #080808 100%);
        }

        .scene-crypt {
            background: radial-gradient(ellipse at 50% 80%, rgba(100, 200, 150, 0.1) 0%, transparent 40%),
                        linear-gradient(180deg, #050508 0%, #0a0a10 50%, #030305 100%);
        }

        .scene-forest {
            background: radial-gradient(ellipse at 30% 30%, rgba(50, 150, 80, 0.15) 0%, transparent 50%),
                        radial-gradient(ellipse at 70% 60%, rgba(30, 100, 60, 0.1) 0%, transparent 40%),
                        linear-gradient(180deg, #0a1510 0%, #0d1a12 50%, #050a08 100%);
        }

        /* Mood overlays */
        .mood-overlay { position: absolute; inset: 0; pointer-events: none; transition: opacity 1s ease; }
        .mood-warm .mood-overlay { background: radial-gradient(ellipse at 50% 100%, rgba(255, 150, 50, 0.1) 0%, transparent 60%); }
        .mood-mysterious .mood-overlay { background: radial-gradient(ellipse at 50% 50%, rgba(100, 50, 200, 0.08) 0%, transparent 70%); animation: pulse-m 4s ease-in-out infinite; }
        @keyframes pulse-m { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
        .mood-ominous .mood-overlay { background: linear-gradient(180deg, rgba(0,0,0,0.3) 0%, transparent 30%, transparent 70%, rgba(0,0,0,0.4) 100%); }
        .mood-danger .mood-overlay { background: radial-gradient(ellipse at 50% 50%, rgba(200, 50, 50, 0.05) 0%, transparent 60%); animation: pulse-d 2s ease-in-out infinite; }
        @keyframes pulse-d { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }
        .mood-supernatural .mood-overlay { background: radial-gradient(ellipse at 50% 50%, rgba(50, 200, 150, 0.1) 0%, transparent 50%); animation: pulse-s 3s ease-in-out infinite; }
        @keyframes pulse-s { 0%, 100% { opacity: 0.5; transform: scale(1); } 50% { opacity: 1; transform: scale(1.02); } }

        /* Particles */
        .particles { position: absolute; inset: 0; overflow: hidden; pointer-events: none; }
        .particle { position: absolute; width: 2px; height: 2px; background: var(--accent); border-radius: 50%; opacity: 0; animation: float-up 12s ease-in-out infinite; }
        @keyframes float-up { 0% { opacity: 0; transform: translateY(100vh) scale(0); } 10% { opacity: 0.6; } 90% { opacity: 0.3; } 100% { opacity: 0; transform: translateY(-20vh) scale(1); } }

        .vignette { position: absolute; inset: 0; background: radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.7) 100%); pointer-events: none; }

        /* Dialogue */
        .dialogue-container { position: absolute; bottom: 0; left: 0; right: 0; padding: 0 2rem 2rem; }
        .dialogue-box {
            background: var(--dialogue-bg);
            border: 1px solid rgba(201, 162, 39, 0.3);
            border-radius: 8px;
            padding: 1.5rem 2rem 1.8rem;
            max-width: 900px;
            margin: 0 auto;
            position: relative;
            backdrop-filter: blur(10px);
        }

        .nameplate {
            position: absolute; top: -18px; left: 24px;
            background: linear-gradient(135deg, var(--accent), var(--accent-glow));
            color: #000;
            font-family: 'Cinzel', serif;
            font-size: 0.9rem;
            font-weight: 600;
            padding: 0.4rem 1.2rem;
            border-radius: 4px;
            letter-spacing: 0.1em;
            box-shadow: 0 4px 15px rgba(201, 162, 39, 0.4);
        }

        .dialogue-title { font-family: 'Cinzel', serif; font-size: 1.3rem; color: var(--accent); margin-bottom: 1rem; display: none; }
        .dialogue-title.visible { display: block; }

        .dialogue-text { font-size: 1.25rem; line-height: 1.8; color: var(--text-dialogue); min-height: 80px; }
        .dialogue-text p { margin-bottom: 0.8rem; }
        .dialogue-text p:last-child { margin-bottom: 0; }
        .dialogue-text strong { color: var(--accent); }
        .dialogue-text em { color: rgba(255,255,255,0.7); }

        .cursor { display: inline-block; width: 2px; height: 1.2em; background: var(--accent); margin-left: 2px; animation: blink 1s step-end infinite; vertical-align: text-bottom; }
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

        .click-indicator { position: absolute; bottom: 12px; right: 20px; font-size: 0.8rem; color: rgba(255,255,255,0.3); animation: bounce 2s ease-in-out infinite; }
        @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }

        /* Choices */
        .choices-container { position: absolute; bottom: 0; left: 0; right: 0; padding: 2rem; display: none; }
        .choices-container.visible { display: block; }
        .choices-box { background: var(--dialogue-bg); border: 1px solid rgba(201, 162, 39, 0.3); border-radius: 8px; padding: 1.5rem; max-width: 700px; margin: 0 auto; backdrop-filter: blur(10px); }
        .choices-title { font-family: 'Cinzel', serif; font-size: 0.9rem; color: rgba(255,255,255,0.5); letter-spacing: 0.2em; text-transform: uppercase; text-align: center; margin-bottom: 1rem; }
        .choices { display: flex; flex-direction: column; gap: 0.8rem; }

        .choice-btn {
            background: rgba(30, 30, 50, 0.8);
            border: 1px solid rgba(201, 162, 39, 0.2);
            border-left: 3px solid transparent;
            border-radius: 4px;
            padding: 1rem 1.2rem;
            color: var(--text-primary);
            font-family: 'Crimson Text', serif;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: left;
        }
        .choice-btn:hover { background: rgba(201, 162, 39, 0.15); border-color: var(--accent); border-left-color: var(--accent); transform: translateX(8px); color: #fff; }

        /* Ending */
        .ending-overlay { position: absolute; inset: 0; background: rgba(0,0,0,0.85); display: none; align-items: center; justify-content: center; flex-direction: column; animation: fadeIn 1s ease; }
        .ending-overlay.visible { display: flex; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

        .ending-text { font-family: 'Cinzel', serif; font-size: 4rem; background: linear-gradient(135deg, var(--accent), #fff, var(--accent)); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: shimmer 3s ease-in-out infinite; margin-bottom: 2rem; }
        .ending-subtitle { color: rgba(255,255,255,0.5); font-size: 1.2rem; margin-bottom: 3rem; }
        .ending-actions { display: flex; gap: 1rem; }

        .ending-btn { font-family: 'Cinzel', serif; font-size: 0.9rem; letter-spacing: 0.1em; padding: 0.8rem 2rem; border-radius: 4px; cursor: pointer; transition: all 0.3s ease; text-transform: uppercase; }
        .ending-btn.primary { background: linear-gradient(135deg, var(--accent), var(--accent-glow)); color: #000; border: none; }
        .ending-btn.secondary { background: transparent; color: var(--text-primary); border: 1px solid rgba(255,255,255,0.3); }
        .ending-btn:hover { transform: translateY(-3px); box-shadow: 0 10px 30px rgba(201, 162, 39, 0.3); }

        /* Nav */
        .vn-nav { position: absolute; top: 1rem; left: 1rem; right: 1rem; display: flex; justify-content: space-between; align-items: center; z-index: 10; }
        .nav-btn { background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); color: rgba(255,255,255,0.6); font-family: 'Cinzel', serif; font-size: 0.75rem; letter-spacing: 0.1em; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; transition: all 0.3s ease; text-transform: uppercase; }
        .nav-btn:hover { background: rgba(201, 162, 39, 0.2); border-color: var(--accent); color: var(--accent); }

        .story-progress { display: flex; gap: 0.5rem; align-items: center; }
        .progress-dot { width: 8px; height: 8px; border-radius: 50%; background: rgba(255,255,255,0.2); transition: all 0.3s ease; }
        .progress-dot.active { background: var(--accent); box-shadow: 0 0 10px var(--accent); }

        /* Transitions */
        .scene-transition { position: absolute; inset: 0; background: #000; opacity: 0; pointer-events: none; transition: opacity 0.5s ease; z-index: 50; }
        .scene-transition.active { opacity: 1; }

        @media (max-width: 768px) {
            .title-logo { font-size: 3rem; }
            .dialogue-box { padding: 1.2rem 1.5rem; }
            .dialogue-text { font-size: 1.1rem; }
            .nameplate { font-size: 0.8rem; }
            .choice-btn { padding: 0.8rem 1rem; font-size: 1rem; }
        }
    </style>
</head>
<body>
    <div id="title-screen">
        <h1 class="title-logo">WAFT</h1>
        <p class="title-tagline">Stories That Flow</p>
        <div id="story-list" class="story-select"><div style="color: rgba(255,255,255,0.4); text-align: center;">Loading tales...</div></div>
    </div>

    <div id="vn-screen">
        <div id="scene-bg" class="scene-bg scene-tavern"></div>
        <div class="mood-overlay"></div>
        <div class="particles" id="particles"></div>
        <div class="vignette"></div>
        <div id="scene-transition" class="scene-transition"></div>

        <div class="vn-nav">
            <button class="nav-btn" onclick="backToTitle()">Menu</button>
            <div class="story-progress" id="progress-dots"></div>
            <button class="nav-btn" onclick="toggleAuto()" id="auto-btn">Auto: Off</button>
        </div>

        <div class="dialogue-container" id="dialogue-container">
            <div class="dialogue-box">
                <div class="nameplate" id="nameplate" style="display:none;"></div>
                <h3 class="dialogue-title" id="dialogue-title"></h3>
                <div class="dialogue-text" id="dialogue-text"></div>
                <div class="click-indicator">Click to continue...</div>
            </div>
        </div>

        <div class="choices-container" id="choices-container">
            <div class="choices-box">
                <div class="choices-title">What will you do?</div>
                <div class="choices" id="choices"></div>
            </div>
        </div>

        <div class="ending-overlay" id="ending-overlay">
            <h2 class="ending-text">Fin</h2>
            <p class="ending-subtitle" id="ending-subtitle">Your tale has reached its conclusion.</p>
            <div class="ending-actions">
                <button class="ending-btn primary" onclick="restartStory()">Read Again</button>
                <button class="ending-btn secondary" onclick="backToTitle()">New Story</button>
            </div>
        </div>
    </div>

    <script>
        const API_BASE = '/api/cyoa';
        let currentStory = null, currentPage = null, history = [], isTyping = false, autoMode = false, typewriterTimeout = null;

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

        async function loadStories() {
            try {
                const res = await fetch(API_BASE);
                const data = await res.json();
                renderStoryList(data.stories);
            } catch (e) { document.getElementById('story-list').innerHTML = '<div style="color:#ef4444;">Could not load stories.</div>'; }
        }

        function renderStoryList(stories) {
            const c = document.getElementById('story-list');
            if (stories.length === 0) { c.innerHTML = '<div style="color:rgba(255,255,255,0.4);">No stories in _stories/</div>'; return; }
            c.innerHTML = stories.map(s => {
                const name = s.name.replace(/_/g, ' ').replace(/-/g, ' ');
                const cap = name.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
                return '<button class="story-btn" onclick="startStory(\\'' + s.name + '\\')">' + cap + '<div class="meta">' + s.page_count + ' pages &bull; ' + s.ending_count + ' endings</div></button>';
            }).join('');
        }

        async function startStory(name) {
            currentStory = name; history = [];
            document.getElementById('title-screen').classList.add('hidden');
            setTimeout(() => { document.getElementById('vn-screen').classList.add('active'); createParticles(); }, 400);
            const res = await fetch(API_BASE + '/' + name);
            const story = await res.json();
            await loadPage(story.start_page);
        }

        async function loadPage(pageId) {
            const t = document.getElementById('scene-transition'); t.classList.add('active');
            await new Promise(r => setTimeout(r, 500));
            try {
                const res = await fetch(API_BASE + '/' + currentStory + '/pages/' + pageId);
                currentPage = await res.json();
                history.push(currentPage.title);
                updateScene(currentPage.scene, currentPage.mood);
                updateProgress();
                t.classList.remove('active');
                await new Promise(r => setTimeout(r, 300));
                currentPage.is_ending ? showEnding() : showDialogue();
            } catch (e) { t.classList.remove('active'); alert('Failed to load page.'); }
        }

        function updateScene(scene, mood) {
            const bg = document.getElementById('scene-bg'), vn = document.getElementById('vn-screen');
            bg.className = 'scene-bg'; vn.className = 'active';
            bg.classList.add('scene-' + (scene || 'tavern'));
            if (mood) vn.classList.add('mood-' + mood);
        }

        function updateProgress() {
            const c = document.getElementById('progress-dots'), dots = Math.min(history.length, 10);
            c.innerHTML = '';
            for (let i = 0; i < dots; i++) { const d = document.createElement('div'); d.className = 'progress-dot' + (i === dots - 1 ? ' active' : ''); c.appendChild(d); }
        }

        function showDialogue() {
            document.getElementById('dialogue-container').style.display = 'block';
            document.getElementById('choices-container').classList.remove('visible');
            document.getElementById('ending-overlay').classList.remove('visible');

            const np = document.getElementById('nameplate');
            if (currentPage.speaker) { np.textContent = currentPage.speaker; np.style.display = 'block'; } else { np.style.display = 'none'; }

            const t = document.getElementById('dialogue-title');
            if (!currentPage.speaker && currentPage.title) { t.textContent = currentPage.title; t.classList.add('visible'); } else { t.classList.remove('visible'); }

            typewriterEffect(currentPage.content_html);
        }

        function typewriterEffect(html) {
            const c = document.getElementById('dialogue-text'); c.innerHTML = ''; isTyping = true;
            const temp = document.createElement('div'); temp.innerHTML = html;
            const text = temp.textContent || temp.innerText;
            let i = 0;
            function type() {
                if (i < text.length) { c.innerHTML = html.substring(0, findHtmlIndex(html, i)) + '<span class="cursor"></span>'; i++; typewriterTimeout = setTimeout(type, 25); }
                else { c.innerHTML = html; isTyping = false; if (currentPage.choices && currentPage.choices.length > 0) setTimeout(showChoices, 500); }
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
                document.getElementById('dialogue-text').innerHTML = currentPage.content_html;
                isTyping = false;
                if (currentPage.choices && currentPage.choices.length > 0) setTimeout(showChoices, 200);
            }
        }

        function showChoices() {
            document.getElementById('dialogue-container').style.display = 'none';
            document.getElementById('choices-container').classList.add('visible');
            document.getElementById('choices').innerHTML = currentPage.choices.map(c => '<button class="choice-btn" onclick="loadPage(\\'' + c.path + '\\')">' + c.text + '</button>').join('');
        }

        function showEnding() {
            document.getElementById('dialogue-container').style.display = 'block';
            document.getElementById('choices-container').classList.remove('visible');
            document.getElementById('nameplate').style.display = 'none';
            const t = document.getElementById('dialogue-title'); t.textContent = currentPage.title; t.classList.add('visible');
            document.getElementById('dialogue-text').innerHTML = currentPage.content_html;
            setTimeout(() => { document.getElementById('dialogue-container').style.display = 'none'; document.getElementById('ending-overlay').classList.add('visible'); }, 3000);
        }

        function restartStory() { if (currentStory) { document.getElementById('ending-overlay').classList.remove('visible'); history = []; loadPage('start'); } }
        function backToTitle() { document.getElementById('vn-screen').classList.remove('active'); document.getElementById('ending-overlay').classList.remove('visible'); document.getElementById('title-screen').classList.remove('hidden'); currentStory = null; currentPage = null; history = []; }
        function toggleAuto() { autoMode = !autoMode; document.getElementById('auto-btn').textContent = 'Auto: ' + (autoMode ? 'On' : 'Off'); }

        document.addEventListener('click', e => { if (isTyping && !e.target.closest('button')) skipTypewriter(); });
        document.addEventListener('keydown', e => { if (e.code === 'Space' || e.code === 'Enter') { if (isTyping) skipTypewriter(); } if (e.code === 'Escape') backToTitle(); });

        loadStories();
    </script>
</body>
</html>
"""


@router.get("/play", response_class=HTMLResponse)
async def play_cyoa():
    """Serve the CYOA web player UI."""
    return HTMLResponse(content=PLAYER_HTML)


# ============================================================================
# Story API Endpoints
# ============================================================================


@router.get("/{story_name}", response_model=StoryMetaResponse)
async def get_story(story_name: str, request: Request):
    """
    Get metadata for a specific story.
    """
    stories_dir = get_stories_dir(request)
    story_path = stories_dir / story_name

    if not story_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Story not found: {story_name}",
        )

    story = load_story(story_path)
    return story_to_meta(story)


@router.get("/{story_name}/validate", response_model=ValidationResponse)
async def validate_story(story_name: str, request: Request):
    """
    Validate a story's integrity.

    Checks that all choice paths point to valid pages.
    """
    stories_dir = get_stories_dir(request)
    story_path = stories_dir / story_name

    if not story_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Story not found: {story_name}",
        )

    story = load_story(story_path)
    errors = story.validate()

    return ValidationResponse(valid=len(errors) == 0, errors=errors)


@router.get("/{story_name}/graph", response_model=StoryGraphResponse)
async def get_story_graph(story_name: str, request: Request):
    """
    Get the story as a graph for visualization.

    Returns nodes (pages) and edges (choices).
    """
    stories_dir = get_stories_dir(request)
    story_path = stories_dir / story_name

    if not story_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Story not found: {story_name}",
        )

    story = load_story(story_path)
    graph = story.get_graph()

    return StoryGraphResponse(name=story.name, **graph)


@router.get("/{story_name}/pages/{page_id}", response_model=PageResponse)
async def get_page(story_name: str, page_id: str, request: Request):
    """
    Get a specific page from a story.

    Returns the page content as HTML and Markdown, plus available choices.
    """
    stories_dir = get_stories_dir(request)
    story_path = stories_dir / story_name

    if not story_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Story not found: {story_name}",
        )

    story = load_story(story_path)
    page = story.get_page(page_id)

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Page not found: {page_id}",
        )

    return page_to_response(page)
