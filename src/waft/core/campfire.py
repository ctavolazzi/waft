"""
TheCampfire - The Essence of Sitting Around a Campfire to Tell Stories

A self-contained full-stack application that embodies the warmth, community,
and magic of gathering around a campfire to share stories.

True Name: "Essence of Sitting Around a Campfire to Tell Stories"

Design Philosophy:
- Simple, warm, communal
- Event-driven storytelling
- Pure vanilla code with minimal dependencies
- Observer pattern for story events
- In-memory cache with JSON persistence
- Simple queue for story processing
"""

from pathlib import Path
from typing import Dict, Any, Optional, List, Callable, Set
from datetime import datetime
from collections import deque
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json as json_lib

# Minimal dependencies - only what's needed
try:
    from .science.oracle import TheOracle
    ORACLE_AVAILABLE = True
except (ImportError, RuntimeError):
    ORACLE_AVAILABLE = False

try:
    from .tavern_keeper import TavernKeeper, Narrator
    TAVERN_AVAILABLE = True
except ImportError:
    TAVERN_AVAILABLE = False

try:
    from ..evolution.storyteller import Storyteller
    STORYTELLER_AVAILABLE = True
except ImportError:
    STORYTELLER_AVAILABLE = False


class StoryEvent:
    """Simple event for story-related actions."""
    def __init__(self, event_type: str, story_id: str, data: Dict[str, Any]):
        self.event_type = event_type  # 'story_told', 'story_updated', 'story_deleted'
        self.story_id = story_id
        self.data = data
        self.timestamp = datetime.now().isoformat()


class StoryObserver:
    """Observer pattern for story events - simple callback system."""
    def __init__(self):
        self._listeners: Dict[str, Set[Callable]] = {}
    
    def subscribe(self, event_type: str, callback: Callable) -> None:
        """Subscribe to story events."""
        if event_type not in self._listeners:
            self._listeners[event_type] = set()
        self._listeners[event_type].add(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """Unsubscribe from story events."""
        if event_type in self._listeners:
            self._listeners[event_type].discard(callback)
    
    def notify(self, event: StoryEvent) -> None:
        """Notify all listeners of an event."""
        listeners = self._listeners.get(event.event_type, set())
        for callback in listeners:
            try:
                callback(event)
            except Exception:
                pass  # Graceful degradation


class StoryQueue:
    """Simple FIFO queue for story processing."""
    def __init__(self):
        self._queue = deque()
        self._lock = threading.Lock()
    
    def enqueue(self, story_data: Dict[str, Any]) -> None:
        """Add story to processing queue."""
        with self._lock:
            self._queue.append(story_data)
    
    def dequeue(self) -> Optional[Dict[str, Any]]:
        """Get next story from queue."""
        with self._lock:
            return self._queue.popleft() if self._queue else None
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        with self._lock:
            return len(self._queue) == 0
    
    def size(self) -> int:
        """Get queue size."""
        with self._lock:
            return len(self._queue)


class StoryCache:
    """Simple in-memory cache with LRU eviction for stories."""
    def __init__(self, max_size: int = 50):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._access_order: deque = deque(maxlen=max_size)
        self._max_size = max_size
        self._lock = threading.Lock()
    
    def get(self, story_id: str) -> Optional[Dict[str, Any]]:
        """Get story from cache."""
        with self._lock:
            if story_id in self._cache:
                # Move to end (most recently used)
                if story_id in self._access_order:
                    self._access_order.remove(story_id)
                self._access_order.append(story_id)
                return self._cache[story_id]
            return None
    
    def put(self, story_id: str, story: Dict[str, Any]) -> None:
        """Add story to cache."""
        with self._lock:
            # Evict oldest if at capacity
            if len(self._cache) >= self._max_size and story_id not in self._cache:
                if self._access_order:
                    oldest = self._access_order.popleft()
                    del self._cache[oldest]
            
            self._cache[story_id] = story
            if story_id in self._access_order:
                self._access_order.remove(story_id)
            self._access_order.append(story_id)
    
    def clear(self) -> None:
        """Clear cache."""
        with self._lock:
            self._cache.clear()
            self._access_order.clear()


class CampfireHandler(BaseHTTPRequestHandler):
    """HTTP handler for TheCampfire - serves stories and UI."""
    
    def __init__(self, campfire_instance, *args, **kwargs):
        self.campfire = campfire_instance
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == "/" or path == "/index.html":
            self._serve_html()
        elif path == "/campfire.css":
            self._serve_css()
        elif path == "/campfire.js":
            self._serve_js()
        elif path == "/api/stories":
            self._serve_stories_api()
        elif path.startswith("/api/stories/"):
            story_id = path.split("/")[-1]
            query = parse_qs(parsed.query)
            if "content" in query or parsed.query == "content":
                self._serve_story_content(story_id)
            else:
                self._serve_story_api(story_id)
        elif path == "/api/profile":
            self._serve_profile_api()
        elif path == "/api/user-data":
            self._serve_user_data_api()
        elif path == "/api/app-data":
            self._serve_app_data_api()
        elif path.startswith("/stories/") and path.endswith(".pdf"):
            self._serve_pdf(path)
        else:
            self._send_404()
    
    def do_POST(self):
        """Handle POST requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == "/api/stories":
            self._create_story()
        else:
            self._send_404()
    
    def _serve_html(self):
        """Serve the campfire HTML page."""
        html = self.campfire._get_html()
        self._send_response(200, "text/html", html.encode())
    
    def _serve_css(self):
        """Serve CSS."""
        css = self.campfire._get_css()
        self._send_response(200, "text/css", css.encode())
    
    def _serve_js(self):
        """Serve JavaScript."""
        js = self.campfire._get_js()
        self._send_response(200, "application/javascript", js.encode())
    
    def _serve_stories_api(self):
        """Serve stories list API."""
        limit = None
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        if "limit" in query:
            try:
                limit = int(query["limit"][0])
            except (ValueError, IndexError):
                pass
        
        stories = self.campfire.get_stories(limit=limit)
        response = {"stories": stories, "count": len(stories)}
        self._send_json(response)
    
    def _serve_story_api(self, story_id: str):
        """Serve single story API."""
        story = self.campfire.get_story(story_id)
        if story:
            self._send_json(story)
        else:
            self._send_404()
    
    def _serve_story_content(self, story_id: str):
        """Serve story content."""
        content = self.campfire.get_story_content(story_id)
        if content:
            self._send_json({"content": content})
        else:
            self._send_404()
    
    def _create_story(self):
        """Create a new story."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json_lib.loads(body.decode())
            
            result = self.campfire.gather_around_the_campfire(
                story_input=data.get("story", ""),
                title=data.get("title"),
                style=data.get("style", "premium"),
                narrative_style=data.get("narrative_style", "medium"),
                structure=data.get("structure", "linear"),
                include_oracle=data.get("include_oracle", True),
                save_story=True
            )
            self._send_json(result)
        except Exception as e:
            self._send_json({"error": str(e)}, status=500)
    
    def _serve_profile_api(self):
        """Serve user profile API."""
        profile = self.campfire.get_user_profile()
        self._send_json(profile)
    
    def _serve_user_data_api(self):
        """Serve user data API."""
        user_data = self.campfire.get_user_data()
        self._send_json(user_data)
    
    def _serve_app_data_api(self):
        """Serve app data API."""
        app_data = self.campfire.get_app_data()
        self._send_json(app_data)
    
    def _serve_pdf(self, pdf_path: str):
        """Serve PDF file."""
        # Extract story ID from path: /stories/story_20260112_120000.pdf
        story_id = pdf_path.split("/")[-1].replace(".pdf", "")
        story = self.campfire.get_story(story_id)
        
        if story and "pdf_path" in story:
            pdf_file = self.campfire.project_path / story["pdf_path"]
            if pdf_file.exists():
                try:
                    with open(pdf_file, "rb") as f:
                        pdf_data = f.read()
                    self._send_response(200, "application/pdf", pdf_data)
                    return
                except IOError:
                    pass
        
        # Fallback: try direct path
        # Use storage path resolver for PDF output
        from ..utils import resolve_output_path
        pdf_file = resolve_output_path(
            Path("_pyrite") / "campfire" / f"{story_id}.pdf",
            self.campfire.project_path
        )
        if pdf_file.exists():
            try:
                with open(pdf_file, "rb") as f:
                    pdf_data = f.read()
                self._send_response(200, "application/pdf", pdf_data)
                return
            except IOError:
                pass
        
        self._send_404()
    
    def _send_json(self, data: Dict[str, Any], status: int = 200):
        """Send JSON response."""
        json_str = json_lib.dumps(data, indent=2)
        self._send_response(status, "application/json", json_str.encode())
    
    def _send_response(self, status: int, content_type: str, data: bytes):
        """Send HTTP response."""
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)
    
    def _send_404(self):
        """Send 404 response."""
        self._send_response(404, "text/plain", b"Not Found")
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


class TheCampfire:
    """
    TheCampfire - The Essence of Sitting Around a Campfire to Tell Stories
    
    A self-contained full-stack application that creates a warm, communal
    space for storytelling. Embodies the magic of gathering around a fire
    to share stories.
    
    True Name: "Essence of Sitting Around a Campfire to Tell Stories"
    """
    
    def __init__(
        self,
        project_path: Path,
        port: int = 5000,
        host: str = "localhost"
    ):
        """
        Initialize TheCampfire.
        
        Args:
            project_path: Path to project root
            port: HTTP server port (default: 5000 per spec)
            host: HTTP server host
        """
        self.project_path = Path(project_path)
        self.port = port
        self.host = host
        # Use storage path resolver for augmented content (routes to external drive if available)
        from ..utils import get_storage_path
        stories_rel = Path("_pyrite") / "campfire"
        self.stories_dir = get_storage_path(stories_rel, self.project_path)
        self.stories_dir.mkdir(parents=True, exist_ok=True)
        self.stories_index = self.stories_dir / "stories_index.json"
        
        # Core data structures
        self._stories: List[Dict[str, Any]] = []
        self._cache = StoryCache(max_size=50)
        self._queue = StoryQueue()
        self._observer = StoryObserver()
        
        # Initialize components (graceful degradation)
        self.oracle = None
        self.oracle_available = False
        if ORACLE_AVAILABLE:
            try:
                self.oracle = TheOracle(self.project_path)
                self.oracle_available = True
            except (RuntimeError, ImportError):
                pass
        
        self.tavern = None
        self.narrator = None
        if TAVERN_AVAILABLE:
            try:
                self.tavern = TavernKeeper(self.project_path)
                self.narrator = Narrator(self.tavern)
            except Exception:
                pass
        
        # Load stories
        self._load_stories()
        
        # Start story processing thread
        self._processing = False
        self._process_thread = None
    
    def _load_stories(self) -> None:
        """Load stories from disk."""
        if self.stories_index.exists():
            try:
                with open(self.stories_index, 'r') as f:
                    self._stories = json.load(f)
                    # Populate cache
                    for story in self._stories[-50:]:  # Cache most recent 50
                        self._cache.put(story.get("id"), story)
            except (json.JSONDecodeError, IOError):
                self._stories = []
        else:
            self._stories = []
    
    def _save_stories(self) -> None:
        """Save stories to disk."""
        try:
            with open(self.stories_index, 'w') as f:
                json.dump(self._stories, f, indent=2)
        except IOError:
            pass  # Graceful degradation
    
    def gather_around_the_campfire(
        self,
        story_input: str,
        title: Optional[str] = None,
        style: str = "premium",
        narrative_style: str = "medium",
        structure: str = "linear",
        include_oracle: bool = True,
        save_story: bool = True
    ) -> Dict[str, Any]:
        """
        Gather around the campfire to tell a story.
        
        The heart of TheCampfire - where stories come to life.
        """
        timestamp = datetime.now()
        story_id = f"story_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        
        # Generate title
        if not title:
            first_line = story_input.split('\n')[0].strip()
            title = first_line[:50] if len(first_line) > 50 else first_line
            if not title:
                title = "Untitled Story"
        
        # Queue story for processing
        story_data = {
            "id": story_id,
            "title": title,
            "story_input": story_input,
            "style": style,
            "narrative_style": narrative_style,
            "structure": structure,
            "include_oracle": include_oracle,
            "save_story": save_story,
            "timestamp": timestamp
        }
        
        self._queue.enqueue(story_data)
        
        # Process immediately (simple synchronous for now)
        return self._process_story(story_data)
    
    def _process_story(self, story_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a story - generate PDF, get insights, save."""
        story_id = story_data["id"]
        story_input = story_data["story_input"]
        title = story_data["title"]
        
        # Get Oracle insights
        oracle_insights = None
        if story_data["include_oracle"] and self.oracle_available:
            try:
                state = self.oracle.get_epistemic_state()
                if state.get("initialized"):
                    guidance = self.oracle.provide_guidance(
                        f"Generate narrative insights for this story: {story_input[:200]}..."
                    )
                    oracle_insights = {
                        "phase": guidance.get("epistemic_phase", "Unknown"),
                        "coverage": guidance.get("knowledge_coverage", 0.0),
                        "recommendation": guidance.get("recommendation", ""),
                        "findings": self.oracle.get_insights(limit=3),
                    }
                    self.oracle.log_insight(
                        f"Story told around the campfire: {title}",
                        impact=0.4
                    )
            except Exception:
                pass
        
        # Enhance story
        enhanced_story = story_input
        if oracle_insights:
            insights_section = f"\n\n---\n\n## Oracle Insights\n\n"
            insights_section += f"**Epistemic Phase:** {oracle_insights['phase']}\n\n"
            insights_section += f"**Knowledge Coverage:** {oracle_insights['coverage']:.0%}\n\n"
            if oracle_insights.get('recommendation'):
                insights_section += f"**Recommendation:** {oracle_insights['recommendation']}\n\n"
            if oracle_insights.get('findings'):
                insights_section += "**Recent Findings:**\n\n"
                for finding in oracle_insights['findings']:
                    finding_text = str(finding) if isinstance(finding, dict) else finding
                    insights_section += f"- {finding_text}\n\n"
            enhanced_story = story_input + insights_section
        
        # Generate PDF if Storyteller available
        pdf_path = None
        if STORYTELLER_AVAILABLE:
            try:
                storyteller = Storyteller(
                    input_data=enhanced_story,
                    narrative_style=story_data["narrative_style"],
                    story_structure=story_data["structure"],
                    pdf_style=story_data["style"],
                    narrator=self.narrator
                )
                # Use storage path resolver for PDF output
                from ..utils import resolve_output_path
                pdf_file = resolve_output_path(
                    Path("_pyrite") / "campfire" / f"{story_id}.pdf",
                    self.project_path
                )
                pdf_path = storyteller.tell_story(
                    output_path=pdf_file,
                    title=title,
                    open_pdf=False
                )
                pdf_path = str(pdf_path.relative_to(self.project_path))
            except Exception:
                pass
        
        # Create story metadata
        story_metadata = {
            "id": story_id,
            "title": title,
            "created_at": story_data["timestamp"].isoformat(),
            "pdf_path": pdf_path,
            "style": story_data["style"],
            "narrative_style": story_data["narrative_style"],
            "structure": story_data["structure"],
            "oracle_insights": oracle_insights,
            "preview": story_input[:200] + "..." if len(story_input) > 200 else story_input,
            "word_count": len(story_input.split()),
        }
        
        # Save story
        if story_data["save_story"]:
            content_path = self.stories_dir / f"{story_id}.md"
            try:
                with open(content_path, 'w') as f:
                    f.write(f"# {title}\n\n")
                    f.write(f"**Created:** {story_data['timestamp'].isoformat()}\n\n")
                    f.write("---\n\n")
                    f.write(enhanced_story)
                story_metadata["content_path"] = str(content_path.relative_to(self.project_path))
            except IOError:
                pass
            
            self._stories.append(story_metadata)
            self._cache.put(story_id, story_metadata)
            self._save_stories()
        
        # Notify observers
        event = StoryEvent("story_told", story_id, story_metadata)
        self._observer.notify(event)
        
        # Log to TavernKeeper
        if self.narrator:
            try:
                self.narrator.observe(
                    f"Story told around the campfire: {title}",
                    context={"story_id": story_id, "pdf_path": pdf_path},
                    mood="delighted",
                    source="ai"
                )
            except Exception:
                pass
        
        return {
            "success": True,
            "story": story_metadata,
            "pdf_path": pdf_path,
            "oracle_insights": oracle_insights
        }
    
    def get_stories(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get all stories, sorted by creation date (newest first)."""
        self._load_stories()  # Refresh from disk
        stories = sorted(
            self._stories,
            key=lambda x: x.get("created_at", ""),
            reverse=True
        )
        if limit:
            stories = stories[:limit]
        return stories
    
    def get_story(self, story_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific story (checks cache first)."""
        # Check cache
        story = self._cache.get(story_id)
        if story:
            return story
        
        # Check disk
        self._load_stories()
        for s in self._stories:
            if s.get("id") == story_id:
                self._cache.put(story_id, s)
                return s
        return None
    
    def get_story_content(self, story_id: str) -> Optional[str]:
        """Get full story content."""
        story = self.get_story(story_id)
        if not story:
            return None
        
        content_path = story.get("content_path")
        if not content_path:
            return None
        
        full_path = self.project_path / content_path
        if not full_path.exists():
            return None
        
        try:
            with open(full_path, 'r') as f:
                return f.read()
        except IOError:
            return None
    
    def get_user_profile(self) -> Dict[str, Any]:
        """Get user profile data."""
        self._load_stories()
        
        # For now, use all stories as "user" stories (single-user mode)
        # In multi-user mode, would filter by user_id
        user_stories = self._stories
        
        if not user_stories:
            return {
                "user_id": "default_user",
                "name": "Storyteller",
                "story_count": 0,
                "total_word_count": 0,
                "first_story_date": None,
                "preferred_style": None
            }
        
        # Calculate profile from stories
        total_words = sum(s.get("word_count", 0) for s in user_stories)
        styles = [s.get("style", "premium") for s in user_stories]
        preferred_style = max(set(styles), key=styles.count) if styles else "premium"
        
        first_story = min(user_stories, key=lambda x: x.get("created_at", ""))
        
        return {
            "user_id": "default_user",
            "name": "Storyteller",
            "story_count": len(user_stories),
            "total_word_count": total_words,
            "first_story_date": first_story.get("created_at"),
            "preferred_style": preferred_style,
            "average_word_count": total_words // len(user_stories) if user_stories else 0
        }
    
    def get_user_data(self) -> Dict[str, Any]:
        """Get user's story data."""
        self._load_stories()
        
        # All stories are user stories in single-user mode
        user_stories = sorted(
            self._stories,
            key=lambda x: x.get("created_at", ""),
            reverse=True
        )
        
        total_words = sum(s.get("word_count", 0) for s in user_stories)
        styles_used = list(set(s.get("style", "premium") for s in user_stories))
        
        return {
            "stories": user_stories,
            "story_count": len(user_stories),
            "total_word_count": total_words,
            "average_word_count": total_words // len(user_stories) if user_stories else 0,
            "styles_used": styles_used,
            "timeline": [
                {
                    "date": s.get("created_at", ""),
                    "title": s.get("title", ""),
                    "word_count": s.get("word_count", 0)
                }
                for s in user_stories
            ]
        }
    
    def get_app_data(self) -> Dict[str, Any]:
        """Get app-wide data and statistics."""
        self._load_stories()
        
        all_stories = self._stories
        total_words = sum(s.get("word_count", 0) for s in all_stories)
        
        # Recent stories (last 10)
        recent_stories = sorted(
            all_stories,
            key=lambda x: x.get("created_at", ""),
            reverse=True
        )[:10]
        
        # Most active styles
        styles = [s.get("style", "premium") for s in all_stories]
        style_counts = {}
        for style in styles:
            style_counts[style] = style_counts.get(style, 0) + 1
        
        return {
            "total_stories": len(all_stories),
            "total_words": total_words,
            "active_users": 1,  # Single-user mode for now
            "recent_stories": recent_stories,
            "popular_styles": dict(sorted(style_counts.items(), key=lambda x: x[1], reverse=True)),
            "average_story_length": total_words // len(all_stories) if all_stories else 0,
            "stories_today": len([s for s in all_stories if s.get("created_at", "").startswith(datetime.now().strftime("%Y-%m-%d"))])
        }
    
    def subscribe(self, event_type: str, callback: Callable) -> None:
        """Subscribe to story events."""
        self._observer.subscribe(event_type, callback)
    
    def serve(self) -> None:
        """Start the campfire server - gather around!"""
        # Create handler class that has access to campfire instance
        campfire_instance = self
        
        class Handler(CampfireHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(campfire_instance, *args, **kwargs)
        
        server = HTTPServer((self.host, self.port), Handler)
        
        print(f"\n🔥 TheCampfire is burning")
        print(f"📍 Gather around: http://{self.host}:{self.port}")
        print(f"📖 Stories await...")
        print(f"\nPress Ctrl+C to extinguish the fire\n")
        
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🔥 TheCampfire is extinguished. Until next time...\n")
            server.shutdown()
    
    def _get_html(self) -> str:
        """Generate the campfire HTML page."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 TheCampfire - Gather Around to Tell Stories</title>
    <link rel="stylesheet" href="/campfire.css">
</head>
<body>
    <div class="campfire-container">
        <header class="campfire-header">
            <h1>🔥 TheCampfire</h1>
            <p class="subtitle">Gather around to tell stories</p>
        </header>
        
        <main class="campfire-main">
            <!-- User Profile Section -->
            <section class="profile-section" id="profileSection">
                <h2>Your Profile</h2>
                <div class="profile-card" id="profileCard">
                    <div class="loading">Loading profile...</div>
                </div>
            </section>
            
            <!-- User Data Section -->
            <section class="user-data-section" id="userDataSection">
                <h2>Your Stories</h2>
                <div class="user-stats" id="userStats">
                    <div class="loading">Loading your data...</div>
                </div>
                <div class="stories-container" id="userStoriesContainer">
                    <div class="loading">Loading your stories...</div>
                </div>
            </section>
            
            <!-- App Data Section -->
            <section class="app-data-section" id="appDataSection">
                <h2>Community Campfire</h2>
                <div class="app-stats" id="appStats">
                    <div class="loading">Loading app data...</div>
                </div>
            </section>
            
            <!-- Story Creation Form -->
            <div class="story-form-container" id="formContainer">
                <button class="toggle-form-btn" onclick="toggleForm()">+ Tell a Story</button>
                <form id="storyForm" class="story-form hidden">
                    <h2>Share Your Story</h2>
                    <input type="text" id="storyTitle" placeholder="Story Title (optional)" />
                    <textarea id="storyText" placeholder="Once upon a time..." rows="10" required></textarea>
                    <div class="form-options">
                        <select id="storyStyle">
                            <option value="premium">Premium</option>
                            <option value="clinical_standard">Clinical Standard</option>
                            <option value="professional">Professional</option>
                        </select>
                        <select id="narrativeStyle">
                            <option value="medium">Medium</option>
                            <option value="simple">Simple</option>
                        </select>
                        <select id="storyStructure">
                            <option value="linear">Linear</option>
                            <option value="three_act">Three Act</option>
                        </select>
                        <label>
                            <input type="checkbox" id="includeOracle" checked />
                            Include Oracle Insights
                        </label>
                    </div>
                    <button type="submit" class="submit-btn">Tell Story Around the Fire</button>
                </form>
            </div>
            
            <!-- All Stories Display -->
            <section class="all-stories-section" id="allStoriesSection">
                <h2>All Stories</h2>
                <div class="stories-container" id="storiesContainer">
                    <div class="loading">Loading stories...</div>
                </div>
            </section>
        </main>
    </div>
    <script src="/campfire.js"></script>
</body>
</html>"""
    
    def _get_css(self) -> str:
        """Generate campfire-themed CSS."""
        return """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Georgia', 'Times New Roman', serif;
    background: linear-gradient(135deg, #1a0a0a 0%, #2d1b0e 50%, #1a0a0a 100%);
    color: #f4e4bc;
    min-height: 100vh;
    padding: 20px;
}

.campfire-container {
    max-width: 1200px;
    margin: 0 auto;
}

.campfire-header {
    text-align: center;
    margin-bottom: 40px;
    padding: 30px;
    background: rgba(139, 69, 19, 0.2);
    border-radius: 15px;
    border: 2px solid rgba(255, 140, 0, 0.3);
    box-shadow: 0 0 30px rgba(255, 140, 0, 0.2);
}

.campfire-header h1 {
    font-size: 3.5em;
    margin-bottom: 10px;
    text-shadow: 0 0 20px rgba(255, 140, 0, 0.8), 0 0 40px rgba(255, 69, 0, 0.4);
    animation: flicker 3s infinite;
}

@keyframes flicker {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.9; }
}

.subtitle {
    font-size: 1.3em;
    font-style: italic;
    color: #d4a574;
}

.story-form-container {
    margin-bottom: 40px;
}

.toggle-form-btn {
    width: 100%;
    padding: 15px;
    font-size: 1.2em;
    background: linear-gradient(135deg, #ff8c00, #ff6b00);
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s;
    box-shadow: 0 4px 15px rgba(255, 140, 0, 0.3);
}

.toggle-form-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 140, 0, 0.5);
}

.story-form {
    margin-top: 20px;
    padding: 30px;
    background: rgba(45, 27, 14, 0.6);
    border-radius: 15px;
    border: 2px solid rgba(255, 140, 0, 0.2);
}

.story-form.hidden {
    display: none;
}

.story-form h2 {
    margin-bottom: 20px;
    color: #ff8c00;
}

.story-form input,
.story-form textarea,
.story-form select {
    width: 100%;
    padding: 12px;
    margin-bottom: 15px;
    background: rgba(26, 10, 10, 0.8);
    border: 1px solid rgba(255, 140, 0, 0.3);
    border-radius: 8px;
    color: #f4e4bc;
    font-family: inherit;
    font-size: 1em;
}

.story-form textarea {
    resize: vertical;
    min-height: 150px;
}

.form-options {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
    margin-bottom: 15px;
}

.form-options label {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
}

.submit-btn {
    width: 100%;
    padding: 15px;
    font-size: 1.1em;
    background: linear-gradient(135deg, #ff6b00, #ff4500);
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s;
}

.submit-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 69, 0, 0.5);
}

.stories-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 25px;
}

.story-card {
    background: rgba(45, 27, 14, 0.7);
    border: 2px solid rgba(255, 140, 0, 0.3);
    border-radius: 15px;
    padding: 25px;
    transition: all 0.3s;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.story-card:hover {
    transform: translateY(-5px);
    border-color: rgba(255, 140, 0, 0.6);
    box-shadow: 0 8px 25px rgba(255, 140, 0, 0.3);
}

.story-card h3 {
    color: #ff8c00;
    margin-bottom: 10px;
    font-size: 1.4em;
}

.story-meta {
    font-size: 0.9em;
    color: #d4a574;
    margin-bottom: 15px;
}

.story-preview {
    color: #f4e4bc;
    line-height: 1.6;
    margin-bottom: 15px;
}

.story-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 15px;
}

.badge {
    padding: 5px 10px;
    background: rgba(255, 140, 0, 0.2);
    border-radius: 5px;
    font-size: 0.85em;
    color: #ff8c00;
}

.oracle-badge {
    background: rgba(138, 43, 226, 0.2);
    color: #ba55d3;
}

.story-actions {
    display: flex;
    gap: 10px;
}

.btn {
    flex: 1;
    padding: 10px;
    background: rgba(255, 140, 0, 0.3);
    border: 1px solid rgba(255, 140, 0, 0.5);
    border-radius: 8px;
    color: #ff8c00;
    cursor: pointer;
    text-decoration: none;
    text-align: center;
    transition: all 0.3s;
    font-weight: bold;
}

.btn:hover {
    background: rgba(255, 140, 0, 0.5);
    transform: translateY(-2px);
}

.loading {
    text-align: center;
    padding: 40px;
    color: #d4a574;
    font-size: 1.2em;
}

.error {
    background: rgba(220, 20, 60, 0.3);
    border: 2px solid rgba(220, 20, 60, 0.5);
    border-radius: 10px;
    padding: 20px;
    color: #ff6b6b;
    margin-bottom: 20px;
}

/* Profile Section */
.profile-section, .user-data-section, .app-data-section, .all-stories-section {
    margin-bottom: 40px;
    padding: 30px;
    background: rgba(45, 27, 14, 0.5);
    border-radius: 15px;
    border: 2px solid rgba(255, 140, 0, 0.2);
}

.profile-section h2, .user-data-section h2, .app-data-section h2, .all-stories-section h2 {
    color: #ff8c00;
    margin-bottom: 20px;
    font-size: 2em;
}

.profile-card {
    background: rgba(26, 10, 10, 0.6);
    border-radius: 10px;
    padding: 25px;
}

.profile-info h3 {
    color: #ff8c00;
    font-size: 1.5em;
    margin-bottom: 20px;
}

.profile-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
}

.stat {
    display: flex;
    flex-direction: column;
    padding: 15px;
    background: rgba(45, 27, 14, 0.6);
    border-radius: 8px;
    border: 1px solid rgba(255, 140, 0, 0.2);
}

.stat-label {
    font-size: 0.9em;
    color: #d4a574;
    margin-bottom: 5px;
}

.stat-value {
    font-size: 1.3em;
    color: #ff8c00;
    font-weight: bold;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.stat-card {
    background: rgba(26, 10, 10, 0.6);
    border: 2px solid rgba(255, 140, 0, 0.3);
    border-radius: 10px;
    padding: 20px;
    text-align: center;
}

.stat-card .stat-label {
    font-size: 0.9em;
    color: #d4a574;
    margin-bottom: 10px;
}

.stat-card .stat-value {
    font-size: 2em;
    color: #ff8c00;
    font-weight: bold;
}

.recent-stories {
    margin-top: 30px;
}

.recent-stories h3 {
    color: #ff8c00;
    margin-bottom: 20px;
}"""
    
    def _get_js(self) -> str:
        """Generate campfire JavaScript."""
        return """// TheCampfire - Vanilla JavaScript
const API_BASE = '/api';

let stories = [];
let userProfile = null;
let userData = null;
let appData = null;

// Toggle form
function toggleForm() {
    const form = document.getElementById('storyForm');
    const btn = document.querySelector('.toggle-form-btn');
    form.classList.toggle('hidden');
    btn.textContent = form.classList.contains('hidden') ? '+ Tell a Story' : 'Cancel';
}

// Load user profile
async function loadProfile() {
    const container = document.getElementById('profileCard');
    try {
        const response = await fetch(`${API_BASE}/profile`);
        userProfile = await response.json();
        renderProfile();
    } catch (error) {
        container.innerHTML = `<div class="error">Error loading profile: ${error.message}</div>`;
    }
}

// Render user profile
function renderProfile() {
    const container = document.getElementById('profileCard');
    if (!userProfile) return;
    
    container.innerHTML = `
        <div class="profile-info">
            <h3>${escapeHtml(userProfile.name)}</h3>
            <div class="profile-stats">
                <div class="stat">
                    <span class="stat-label">Stories Told</span>
                    <span class="stat-value">${userProfile.story_count}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Total Words</span>
                    <span class="stat-value">${userProfile.total_word_count.toLocaleString()}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Preferred Style</span>
                    <span class="stat-value">${escapeHtml(userProfile.preferred_style || 'N/A')}</span>
                </div>
                ${userProfile.first_story_date ? `
                    <div class="stat">
                        <span class="stat-label">First Story</span>
                        <span class="stat-value">${formatDate(userProfile.first_story_date)}</span>
                    </div>
                ` : ''}
            </div>
        </div>
    `;
}

// Load user data
async function loadUserData() {
    const statsContainer = document.getElementById('userStats');
    const storiesContainer = document.getElementById('userStoriesContainer');
    
    try {
        const response = await fetch(`${API_BASE}/user-data`);
        userData = await response.json();
        renderUserStats();
        renderUserStories();
    } catch (error) {
        statsContainer.innerHTML = `<div class="error">Error loading user data: ${error.message}</div>`;
    }
}

// Render user stats
function renderUserStats() {
    const container = document.getElementById('userStats');
    if (!userData) return;
    
    container.innerHTML = `
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Your Stories</div>
                <div class="stat-value">${userData.story_count}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Words</div>
                <div class="stat-value">${userData.total_word_count.toLocaleString()}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Length</div>
                <div class="stat-value">${userData.average_word_count} words</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Styles Used</div>
                <div class="stat-value">${userData.styles_used.length}</div>
            </div>
        </div>
    `;
}

// Render user stories
function renderUserStories() {
    const container = document.getElementById('userStoriesContainer');
    if (!userData || !userData.stories) return;
    
    if (userData.stories.length === 0) {
        container.innerHTML = '<div class="loading">No stories yet. Tell your first story!</div>';
        return;
    }
    
    container.innerHTML = userData.stories.map(story => createStoryCard(story)).join('');
}

// Load app data
async function loadAppData() {
    const container = document.getElementById('appStats');
    try {
        const response = await fetch(`${API_BASE}/app-data`);
        appData = await response.json();
        renderAppStats();
    } catch (error) {
        container.innerHTML = `<div class="error">Error loading app data: ${error.message}</div>`;
    }
}

// Render app stats
function renderAppStats() {
    const container = document.getElementById('appStats');
    if (!appData) return;
    
    container.innerHTML = `
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Stories</div>
                <div class="stat-value">${appData.total_stories}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Words</div>
                <div class="stat-value">${appData.total_words.toLocaleString()}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Stories Today</div>
                <div class="stat-value">${appData.stories_today}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Length</div>
                <div class="stat-value">${appData.average_story_length} words</div>
            </div>
        </div>
        ${appData.recent_stories && appData.recent_stories.length > 0 ? `
            <div class="recent-stories">
                <h3>Recent Community Stories</h3>
                <div class="stories-container">
                    ${appData.recent_stories.map(story => createStoryCard(story)).join('')}
                </div>
            </div>
        ` : ''}
    `;
}

// Create story card HTML
function createStoryCard(story) {
    return `
        <div class="story-card">
            <h3>${escapeHtml(story.title)}</h3>
            <div class="story-meta">${formatDate(story.created_at)} • ${story.word_count} words</div>
            <div class="story-preview">${escapeHtml(story.preview)}</div>
            ${story.oracle_insights ? `
                <div class="story-badges">
                    <span class="badge oracle-badge">🔮 ${story.oracle_insights.phase}</span>
                </div>
            ` : ''}
            <div class="story-badges">
                <span class="badge">${story.style}</span>
                <span class="badge">${story.narrative_style}</span>
            </div>
            <div class="story-actions">
                ${story.pdf_path ? `<a href="/stories/${story.id}.pdf" target="_blank" class="btn">📄 View PDF</a>` : ''}
            </div>
        </div>
    `;
}

// Load stories
async function loadStories() {
    const container = document.getElementById('storiesContainer');
    container.innerHTML = '<div class="loading">Loading stories...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/stories`);
        const data = await response.json();
        stories = data.stories || [];
        renderStories();
    } catch (error) {
        container.innerHTML = `<div class="error">Error loading stories: ${error.message}</div>`;
    }
}

// Render stories
function renderStories() {
    const container = document.getElementById('storiesContainer');
    
    if (stories.length === 0) {
        container.innerHTML = '<div class="loading">No stories yet. Be the first to tell one!</div>';
        return;
    }
    
    container.innerHTML = stories.map(story => createStoryCard(story)).join('');
}

// Submit story
document.getElementById('storyForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        story: document.getElementById('storyText').value,
        title: document.getElementById('storyTitle').value || null,
        style: document.getElementById('storyStyle').value,
        narrative_style: document.getElementById('narrativeStyle').value,
        structure: document.getElementById('storyStructure').value,
        include_oracle: document.getElementById('includeOracle').checked
    };
    
    if (!formData.story.trim()) {
        alert('Please enter a story!');
        return;
    }
    
    const submitBtn = document.querySelector('.submit-btn');
    submitBtn.textContent = 'Telling Story...';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE}/stories`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Reset form
            document.getElementById('storyForm').reset();
            toggleForm();
            
            // Reload all data
            await Promise.all([
                loadStories(),
                loadProfile(),
                loadUserData(),
                loadAppData()
            ]);
            
            // Open PDF if available
            if (result.pdf_path) {
                window.open(`/stories/${result.story.id}.pdf`, '_blank');
            }
        } else {
            alert('Error: ' + (result.error || 'Failed to create story'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        submitBtn.textContent = 'Tell Story Around the Fire';
        submitBtn.disabled = false;
    }
});

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Load all data on page load
async function loadAll() {
    await Promise.all([
        loadProfile(),
        loadUserData(),
        loadAppData(),
        loadStories()
    ]);
}

loadAll();

// Auto-refresh every 30 seconds
setInterval(() => {
    loadAll();
}, 30000);"""
