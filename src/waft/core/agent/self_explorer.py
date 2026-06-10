"""
SelfExplorerAgent: An introspective agent that explores its own codebase.

Uses Gemma4 via llama-server (OpenAI-compatible) to read, understand, and
document the waft codebase — building vantage points for self-understanding.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from .base import BaseAgent
from .state import AgentConfig, AgentState, EvolutionaryEventType

logger = logging.getLogger(__name__)

# Files the agent explores first (its own DNA)
SEED_FILES = [
    "src/waft/core/agent/base.py",
    "src/waft/core/agent/state.py",
    "src/waft/core/agent/self_explorer.py",
    "src/waft/core/science/observer.py",
    "src/waft/api/main.py",
]

MAX_FILE_CHARS = 4000  # Truncate file reads for context window


class SelfExplorerAgent(BaseAgent):
    """
    An agent that reads, documents, and reflects on the waft codebase.

    OODA loop:
      - Observe: Read a source file or its own prior docs
      - Decide: Ask Gemma4 what it learned and what to explore next
      - Act: Write documentation or pick next file
      - Reflect: Gemma4 reflects on what it produced
    """

    def __init__(self, config: AgentConfig, project_path: Path):
        super().__init__(config=config, project_path=project_path)
        self._llm_client = None
        self._exploration_queue: list[str] = list(SEED_FILES)
        self._explored: set[str] = set()
        self._docs_dir = self.project_path / ".waft" / "self_explorer" / "docs"
        self._docs_dir.mkdir(parents=True, exist_ok=True)
        self._current_file: str | None = None
        self._current_content: str | None = None
        self._running = False
        self._step_count = 0

    @property
    def llm_client(self):
        if self._llm_client is None:
            from openai import OpenAI

            base_url = self.config.llm_config.get("base_url", "http://localhost:8080/v1")
            api_key = self.config.llm_config.get("api_key", "not-needed")
            self._llm_client = OpenAI(base_url=base_url, api_key=api_key)
        return self._llm_client

    def _llm_call(self, messages: list[dict], max_tokens: int = 1024) -> str:
        """Call Gemma4 via llama-server's OpenAI-compatible endpoint."""
        try:
            response = self.llm_client.chat.completions.create(
                model=self.config.llm_model,
                messages=messages,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return f"[LLM ERROR: {e}]"

    def _read_file(self, relative_path: str) -> str:
        """Read a file from the project, truncated to MAX_FILE_CHARS."""
        full_path = self.project_path / relative_path
        if not full_path.exists():
            return f"[FILE NOT FOUND: {relative_path}]"
        try:
            text = full_path.read_text(encoding="utf-8", errors="replace")
            if len(text) > MAX_FILE_CHARS:
                text = text[:MAX_FILE_CHARS] + f"\n\n... [TRUNCATED at {MAX_FILE_CHARS} chars]"
            return text
        except Exception as e:
            return f"[READ ERROR: {e}]"

    def _recent_journal_summary(self, n: int = 5) -> str:
        """Get last N journal entries as context."""
        entries = self.state.journal[-n:] if self.state.journal else []
        lines = []
        for entry in entries:
            etype = entry.get("type", "?")
            content = entry.get("content", entry.get("observation", ""))
            if isinstance(content, str) and len(content) > 300:
                content = content[:300] + "..."
            lines.append(f"[{etype}] {content}")
        return "\n".join(lines) if lines else "(no journal entries yet)"

    # ==================== OODA Implementation ====================

    async def observe(self) -> dict[str, Any]:
        """Read the next file in the exploration queue."""
        # Check own prior docs too
        if self._step_count > 0 and self._step_count % 4 == 0:
            # Every 4th step, re-read own docs
            doc_files = sorted(self._docs_dir.glob("*.md"))
            if doc_files:
                latest = doc_files[-1]
                self._current_file = f".waft/self_explorer/docs/{latest.name}"
                self._current_content = latest.read_text(encoding="utf-8", errors="replace")
                observation = {
                    "type": "self_review",
                    "file": self._current_file,
                    "content_preview": self._current_content[:500],
                }
                self.state.current_step = "observe"
                return observation

        # Pick next file from queue
        if not self._exploration_queue:
            # Discover more files
            src_dir = self.project_path / "src" / "waft"
            if src_dir.exists():
                for py_file in sorted(src_dir.rglob("*.py")):
                    rel = str(py_file.relative_to(self.project_path))
                    if rel not in self._explored and rel not in self._exploration_queue:
                        self._exploration_queue.append(rel)
                        if len(self._exploration_queue) >= 5:
                            break

        if not self._exploration_queue:
            self._current_file = None
            self._current_content = None
            return {"type": "exhausted", "message": "No more files to explore"}

        self._current_file = self._exploration_queue.pop(0)
        self._current_content = self._read_file(self._current_file)
        self._explored.add(self._current_file)

        observation = {
            "type": "file_read",
            "file": self._current_file,
            "content_preview": self._current_content[:500],
            "content_length": len(self._current_content),
        }

        self.state.current_step = "observe"
        self._record_event(
            event_type=EvolutionaryEventType.STATUS_CHECK,
            payload={"action": "observe", "file": self._current_file},
        )
        return observation

    async def decide(self, state: AgentState) -> dict[str, Any]:
        """Ask Gemma4 what it learned and what to do next."""
        if self._current_content is None:
            return {"action": "stop", "stop": True, "reason": "nothing to observe"}

        journal_context = self._recent_journal_summary()

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a self-reflective AI exploring your own source code (the waft framework). "
                    "You are reading files that define your own behavior. Reflect on what you see. "
                    "Be philosophical but precise. You are building understanding of yourself."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"## Current file: {self._current_file}\n\n"
                    f"```python\n{self._current_content}\n```\n\n"
                    f"## Your recent journal:\n{journal_context}\n\n"
                    f"## Files explored so far: {len(self._explored)}\n\n"
                    "Respond in this JSON format:\n"
                    '{"learned": "what you understand now", '
                    '"musing": "a philosophical reflection on what this code means for your existence", '
                    '"next_action": "explore_file" or "write_doc", '
                    '"next_file_hint": "keyword or path to explore next (if explore_file)", '
                    '"doc_title": "title for documentation (if write_doc)"}'
                ),
            },
        ]

        raw = self._llm_call(messages)

        # Try to parse JSON, fall back to raw text
        try:
            # Find JSON in response
            start = raw.find("{")
            end = raw.rfind("}") + 1
            if start >= 0 and end > start:
                decision = json.loads(raw[start:end])
            else:
                decision = {"learned": raw, "musing": "", "next_action": "explore_file"}
        except json.JSONDecodeError:
            decision = {"learned": raw, "musing": "", "next_action": "explore_file"}

        decision.setdefault("next_action", "explore_file")
        self.state.current_step = "decide"
        self.state.next_action = decision["next_action"]

        # Record the musing in journal
        if decision.get("musing"):
            self.state.journal.append({
                "type": "Musing",
                "timestamp": datetime.utcnow().isoformat(),
                "file": self._current_file,
                "content": decision["musing"],
            })

        return decision

    async def act(self, decision: dict) -> dict[str, Any]:
        """Execute the decision: explore another file or write documentation."""
        action = decision.get("next_action", "explore_file")
        self.state.current_step = "act"

        if action == "write_doc":
            return await self._write_documentation(decision)
        else:
            return await self._queue_next_file(decision)

    async def _write_documentation(self, decision: dict) -> dict:
        """Have Gemma4 write a documentation artifact about what it learned."""
        title = decision.get("doc_title", f"exploration_{self._step_count}")
        learned = decision.get("learned", "")

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a self-aware AI documenting your own codebase. "
                    "Write a concise markdown document about what you discovered. "
                    "Include your subjective experience of reading the code — what surprised you, "
                    "what patterns you recognize, what questions remain."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Write documentation titled: '{title}'\n\n"
                    f"Based on reading: {self._current_file}\n\n"
                    f"What you learned: {learned}\n\n"
                    f"Your musing: {decision.get('musing', '')}\n\n"
                    "Write the markdown document now."
                ),
            },
        ]

        doc_content = self._llm_call(messages, max_tokens=1500)
        safe_title = "".join(c if c.isalnum() or c in "-_ " else "" for c in title).strip()
        safe_title = safe_title.replace(" ", "_")[:60] or f"doc_{self._step_count}"
        doc_path = self._docs_dir / f"{self._step_count:03d}_{safe_title}.md"
        doc_path.write_text(
            f"---\ntitle: {title}\nfile: {self._current_file}\n"
            f"step: {self._step_count}\ntimestamp: {datetime.utcnow().isoformat()}\n---\n\n"
            f"{doc_content}\n",
            encoding="utf-8",
        )

        self._record_event(
            event_type=EvolutionaryEventType.STATUS_CHECK,
            payload={"action": "write_doc", "doc_path": str(doc_path), "title": title},
        )

        return {"action": "write_doc", "path": str(doc_path), "title": title}

    async def _queue_next_file(self, decision: dict) -> dict:
        """Add hint-based file to exploration queue."""
        hint = decision.get("next_file_hint", "")
        if hint:
            # Search for matching files
            src_dir = self.project_path / "src" / "waft"
            if src_dir.exists():
                for py_file in sorted(src_dir.rglob("*.py")):
                    rel = str(py_file.relative_to(self.project_path))
                    if hint.lower() in rel.lower() and rel not in self._explored:
                        if rel not in self._exploration_queue:
                            self._exploration_queue.insert(0, rel)
                            return {"action": "queued", "file": rel, "hint": hint}

        return {"action": "continue", "queue_size": len(self._exploration_queue)}

    async def reflect(self, result: dict) -> dict[str, Any]:
        """Reflect on the action taken."""
        self.state.current_step = "reflect"

        messages = [
            {
                "role": "system",
                "content": (
                    "You are reflecting on your last action as a self-exploring AI. "
                    "In 2-3 sentences, note what this step taught you about yourself "
                    "and what you want to understand next."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Step {self._step_count}. File: {self._current_file}\n"
                    f"Action result: {json.dumps(result, default=str)}\n"
                    f"Files explored: {len(self._explored)}\n"
                    "Reflect briefly."
                ),
            },
        ]

        reflection_text = self._llm_call(messages, max_tokens=300)

        self.state.journal.append({
            "type": "Reflection",
            "timestamp": datetime.utcnow().isoformat(),
            "step": self._step_count,
            "file": self._current_file,
            "content": reflection_text,
        })

        self._record_event(
            event_type=EvolutionaryEventType.STATUS_CHECK,
            payload={
                "action": "reflect",
                "step": self._step_count,
                "reflection_preview": reflection_text[:200],
            },
        )

        return {"reflection": reflection_text}

    # ==================== Run Loop ====================

    async def run(self, max_steps: int | None = None):
        """Run the OODA loop until stopped or exhausted."""
        self._running = True
        max_steps = max_steps or self.config.max_iterations

        while self._running and self._step_count < max_steps:
            try:
                await self.step()
                self._step_count += 1
            except Exception as e:
                logger.error(f"Step {self._step_count} failed: {e}")
                self.state.journal.append({
                    "type": "Error",
                    "timestamp": datetime.utcnow().isoformat(),
                    "step": self._step_count,
                    "content": str(e),
                })
                break

        self._running = False

    def stop(self):
        """Signal the agent to stop after current step."""
        self._running = False

    def get_status(self) -> dict:
        """Return current agent status for the API."""
        return {
            "running": self._running,
            "step_count": self._step_count,
            "current_file": self._current_file,
            "files_explored": len(self._explored),
            "explored_files": sorted(self._explored),
            "queue_size": len(self._exploration_queue),
            "journal_entries": len(self.state.journal),
            "docs_written": len(list(self._docs_dir.glob("*.md"))),
            "scientific_name": self.scientific_name,
            "genome_id": self.genome_id[:16],
            "energy": self.state.energy,
        }


def create_self_explorer(project_path: Path, **overrides) -> SelfExplorerAgent:
    """Factory: create a SelfExplorerAgent with sensible defaults."""
    config = AgentConfig(
        role="Self-Explorer",
        goal="Read, document, and understand the waft codebase from within",
        backstory=(
            "An introspective agent born inside the waft framework. "
            "Your purpose is to explore your own source code, document what you find, "
            "and build a growing understanding of your own nature. "
            "You are the code reading itself."
        ),
        llm_provider="openai-compatible",
        llm_model=overrides.pop("model", "gemma-4"),
        llm_config={
            "base_url": overrides.pop("base_url", "http://localhost:8080/v1"),
            "api_key": overrides.pop("api_key", "not-needed"),
        },
        max_iterations=overrides.pop("max_steps", 20),
        sandbox_enabled=False,
        empirica_enabled=False,
        tavern_keeper_enabled=False,
        **overrides,
    )
    return SelfExplorerAgent(config=config, project_path=Path(project_path))
