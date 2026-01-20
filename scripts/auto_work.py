#!/usr/bin/env python3
"""
Auto Work - Autonomous work effort execution.

Thinks about work efforts, picks the best one, and executes it autonomously.
Uses Empirica gates for safety and decision support.
"""

import argparse
import json
import logging
import resource
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from scripts.show_me import get_work_efforts
from scripts.work_dashboard import (
    MAX_INDEX_FILE_SIZE,
    _validate_work_effort_path,
    analyze_work_effort_actions,
    find_index_file,
    get_recent_git_activity,
)

# Pantheon entities for decision support
try:
    from src.waft.pantheon import (
        Fae,
        GitHubGod,
        Judge,
        Librarian,
        Magistrate,
        MilitaryBrass,
        MissionControl,
        Storyteller,
        TestRunner,
        TheReasoner,
        TheVillage,
    )

    PANTHEON_AVAILABLE = True
except ImportError:
    PANTHEON_AVAILABLE = False
    Judge = None
    Magistrate = None
    TheReasoner = None
    GitHubGod = None
    Fae = None
    MissionControl = None
    TheVillage = None
    Storyteller = None
    Librarian = None
    MilitaryBrass = None
    TestRunner = None

# Decision support tools
try:
    from src.waft.core.decision_matrix import DecisionMatrix

    DECISION_MATRIX_AVAILABLE = True
except ImportError:
    DECISION_MATRIX_AVAILABLE = False
    DecisionMatrix = None

# Oracle for epistemic guidance
try:
    from src.waft.core.science.oracle import TheOracle

    ORACLE_AVAILABLE = True
except ImportError:
    ORACLE_AVAILABLE = False
    TheOracle = None

# Campfire for storytelling
try:
    from src.waft.core.campfire import TheCampfire

    CAMPFIRE_AVAILABLE = True
except ImportError:
    CAMPFIRE_AVAILABLE = False
    TheCampfire = None

# D&D Campaign and Quest PDF generation
try:
    from src.waft.core.dnd_scenario.quest_pdf_generator import QuestPDFGenerator
    from src.waft.core.dnd_scenario.scenario_orchestrator import ScenarioOrchestrator
    from src.waft.core.dnd_scenario.scenario_realm import ScenarioRealm

    DND_CAMPAIGN_AVAILABLE = True
except ImportError:
    DND_CAMPAIGN_AVAILABLE = False
    ScenarioRealm = None
    ScenarioOrchestrator = None
    QuestPDFGenerator = None

logger = logging.getLogger(__name__)


class AutoWorkLogger:
    """Dual logger: console + file + devlog integration."""

    def __init__(self, project_path: Path, verbose: bool = False):
        self.project_path = project_path
        self.verbose = verbose
        self.log_dir = project_path / "_work_efforts" / "auto_work_logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"auto_work_{timestamp}.log"

        # Initialize devlog manager
        self.devlog_manager = None
        try:
            from src.waft.core.devlog import DevlogManager

            self.devlog_manager = DevlogManager(project_path)
        except Exception as e:
            logger.warning(f"DevlogManager unavailable: {e}")

        # Buffer for summary
        self.summary_lines = []
        self.start_time = datetime.now()

    def log(self, message: str, flush: bool = True):
        """Log to both console and file."""
        # Print to console
        print(message, end="", flush=flush)

        # Write to file
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(message)
                if flush:
                    f.flush()
        except Exception as e:
            logger.error(f"Failed to write to log file: {e}")

        # Collect for summary
        if message.strip():
            self.summary_lines.append(message.strip())

    def write_summary_to_devlog(
        self,
        selected_we: dict | None = None,
        action: dict | None = None,
        success: bool = False,
    ):
        """Write summary entry to devlog."""
        if not self.devlog_manager:
            return

        duration = (datetime.now() - self.start_time).total_seconds()

        # Build summary content
        summary_parts = [
            f"Auto-Work execution completed in {duration:.1f}s",
            "",
            "## Process",
        ]

        # Add key steps
        for line in self.summary_lines[-20:]:  # Last 20 lines
            if any(
                keyword in line.lower()
                for keyword in ["scanning", "found", "selected", "action", "executing", "✅", "❌"]
            ):
                summary_parts.append(f"- {line}")

        if selected_we:
            summary_parts.extend(
                [
                    "",
                    "## Selected Work Effort",
                    f"- **ID**: {selected_we.get('id', 'unknown')}",
                    f"- **Title**: {selected_we.get('title', 'Unknown')}",
                    f"- **Status**: {selected_we.get('status', 'unknown')}",
                ]
            )

        if action:
            summary_parts.extend(
                [
                    "",
                    "## Action",
                    f"- **Label**: {action.get('label', 'Unknown')}",
                    f"- **Reason**: {action.get('reason', 'N/A')}",
                ]
            )

        summary_parts.extend(
            [
                "",
                "## Result",
                f"- **Status**: {'Success' if success else 'Failed'}",
                f"- **Log File**: `{self.log_file.relative_to(self.project_path)}`",
            ]
        )

        summary_content = "\n".join(summary_parts)

        try:
            self.devlog_manager.write_entry(
                content=summary_content,
                source=DevlogManager.SOURCE_SCRIPT,
                category=DevlogManager.CATEGORY_MAINTENANCE,
                title=f"Auto-Work: {selected_we.get('title', 'Work Effort Selection') if selected_we else 'Execution'}",
                metadata={
                    "work_effort_id": selected_we.get("id") if selected_we else None,
                    "action": action.get("label") if action else None,
                    "duration_seconds": duration,
                    "success": success,
                    "log_file": str(self.log_file.relative_to(self.project_path)),
                },
            )
        except Exception as e:
            logger.error(f"Failed to write to devlog: {e}")


def get_memory_usage_mb() -> float:
    """Get current memory usage in MB."""
    try:
        # Get RSS (Resident Set Size) in KB, convert to MB
        usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        # On macOS, ru_maxrss is in bytes; on Linux it's in KB
        if sys.platform == "darwin":
            return usage / 1024 / 1024  # Convert bytes to MB
        else:
            return usage / 1024  # Convert KB to MB
    except Exception:
        return 0.0


def print_progress(message: str, verbose: bool = False, memory: bool = False, logger_instance=None):
    """Print progress message with optional memory info."""
    if memory:
        mem_mb = get_memory_usage_mb()
        msg = f"  {message} [Memory: {mem_mb:.1f} MB]"
    else:
        msg = f"  {message}"

    if logger_instance:
        logger_instance.log(msg + "\n", flush=True)
    else:
        print(msg)
        if verbose:
            sys.stdout.flush()


def calculate_work_effort_priority(
    work_effort: dict, project_path: Path, empirica_manager=None, pantheon_entities=None
) -> float:
    """
    Calculate priority score for a work effort (higher = more important).

    Uses Empirica epistemic state to inform priority when available.

    Factors:
    - Status (active > paused > open > completed)
    - Priority level (CRITICAL > HIGH > MEDIUM > LOW)
    - Recent activity (recent commits = higher priority)
    - Content indicators (TODOs, FIXMEs = higher priority)
    - Empirica epistemic state (uncertainty, engagement, completion)
    - Oracle guidance (if available)
    """
    score = 0.0

    # Status weighting (active work is most important)
    status = work_effort.get("status", "open").lower()
    status_weights = {
        "active": 100.0,
        "paused": 50.0,
        "open": 30.0,
        "completed": 0.0,
    }
    score += status_weights.get(status, 0.0)

    # Skip completed work efforts
    if status == "completed":
        return 0.0

    # Priority level weighting
    priority = work_effort.get("priority", "MEDIUM").upper()
    priority_weights = {
        "CRITICAL": 50.0,
        "HIGH": 30.0,
        "MEDIUM": 15.0,
        "LOW": 5.0,
    }
    score += priority_weights.get(priority, 15.0)

    # EMPIRICA: Use epistemic state to adjust priority (non-blocking)
    if empirica_manager and empirica_manager.is_initialized():
        try:
            # Use Empirica's check_submit for lightweight priority guidance
            # (Oracle requires full initialization which can be slow)
            we_id = work_effort.get("id", "")
            we_title = work_effort.get("title", "")

            # Quick Empirica gate check for priority adjustment
            gate_result = empirica_manager.check_submit(
                {
                    "type": "work_effort_priority_assessment",
                    "scope": "low",  # Low scope for quick response
                    "description": f"Assess priority for {we_id}: {we_title}",
                    "work_effort_id": we_id,
                    "work_effort_status": status,
                    "work_effort_priority": priority,
                }
            )

            # Gate results can inform priority adjustments
            if gate_result == "PROCEED":
                # High confidence - boost priority slightly
                score += 10.0
            elif gate_result == "HALT":
                # Requires attention - boost priority more
                score += 20.0
            elif gate_result == "BRANCH":
                # Needs investigation - moderate boost
                score += 15.0
            # REVISE or None - no adjustment

        except Exception as e:
            logger.debug(f"Empirica priority guidance unavailable: {e}, using base scoring")
            # Continue with base scoring if Empirica unavailable

    # Analyze content for indicators
    we_id = work_effort.get("id", "")
    we_path = work_effort.get("path", "")
    we_dir = project_path / we_path

    if _validate_work_effort_path(we_dir, project_path):
        index_file = find_index_file(we_dir, we_id)
        if index_file:
            try:
                # SECURITY: Check file size before reading
                if index_file.stat().st_size > MAX_INDEX_FILE_SIZE:
                    logger.warning(
                        f"Index file too large for {we_id}: {index_file.stat().st_size} bytes"
                    )
                else:
                    content = index_file.read_text(encoding="utf-8").lower()

                    # TODOs and FIXMEs indicate work needed
                    if "todo" in content:
                        score += 20.0
                    if "fixme" in content:
                        score += 25.0
                    if "bug" in content or "error" in content:
                        score += 15.0

            except Exception as e:
                logger.warning(f"Error reading content for {we_id}: {e}")

        # Recent git activity indicates active work (with error handling)
        try:
            git_activity = get_recent_git_activity(we_dir, days=7)
            if git_activity:
                score += min(len(git_activity) * 5.0, 20.0)  # Cap at 20
        except Exception as e:
            logger.warning(f"Error getting git activity for {we_id}: {e}")
            # Continue without git activity score

    # PANTHEON: Use Judge and Magistrate to inform priority
    if pantheon_entities and PANTHEON_AVAILABLE:
        try:
            judge = pantheon_entities.get("judge")
            magistrate = pantheon_entities.get("magistrate")
            github_god = pantheon_entities.get("github_god")

            we_id = work_effort.get("id", "")
            we_title = work_effort.get("title", "")

            # Judge evaluates work effort readiness
            if judge:
                try:
                    judgment = judge.evaluate_claim(
                        claim=f"Work effort {we_id} ({we_title}) is ready for autonomous execution",
                        category="work_efforts",
                        tags=["autonomous", "execution"],
                    )

                    # Adjust score based on judgment
                    if judgment.verdict.value == "PROVEN" and judgment.confidence > 0.7:
                        score += 15.0  # High confidence it's ready
                    elif judgment.verdict.value == "DISPROVEN" and judgment.confidence > 0.7:
                        score -= 10.0  # High confidence it's NOT ready
                    elif judgment.verdict.value == "PROBABLE" and judgment.confidence > 0.6:
                        score += 8.0  # Likely ready
                except Exception as e:
                    logger.debug(f"Judge evaluation unavailable: {e}")

            # Magistrate searches for precedents (similar work efforts)
            if magistrate:
                try:
                    precedents = magistrate.search_precedents(we_title or we_id)
                    if precedents:
                        # If similar work efforts exist, check their outcomes
                        proven_count = sum(
                            1 for p in precedents[:3] if p.confidence and p.confidence > 0.7
                        )
                        if proven_count > 0:
                            score += 5.0 * proven_count  # Boost if precedents suggest success
                except Exception as e:
                    logger.debug(f"Magistrate search unavailable: {e}")

            # Librarian searches knowledge base for related work
            librarian = pantheon_entities.get("librarian")
            if librarian:
                try:
                    # Search for related records in the library
                    related_records = librarian.search(we_title or we_id, limit=3)
                    if related_records:
                        # Boost if work effort is referenced in knowledge base
                        score += 3.0 * len(
                            related_records
                        )  # Small boost for knowledge base presence
                except Exception as e:
                    logger.debug(f"Librarian search unavailable: {e}")

            # GitHubGod provides repository context
            if github_god:
                try:
                    repo_state = github_god.get_repository_state()
                    # If work effort branch matches current branch, boost priority
                    we_branch = work_effort.get("branch", "")
                    if we_branch and repo_state.get("current_branch") == we_branch:
                        score += 10.0  # Working on same branch
                except Exception as e:
                    logger.debug(f"GitHubGod state unavailable: {e}")

        except Exception as e:
            logger.debug(f"Pantheon priority adjustment unavailable: {e}")

    return score


def select_best_work_effort(
    work_efforts: list[dict], project_path: Path, empirica_manager=None, pantheon_entities=None
) -> dict | None:
    """
    Analyze work efforts and select the best one to work on.

    Uses Empirica for epistemic assessment and decision support.

    Returns the work effort with highest priority score, or None if none available.

    SECURITY: Validates work effort IDs and paths before selection.
    """
    if not work_efforts:
        return None

    # EMPIRICA: Pre-flight epistemic assessment
    if empirica_manager and empirica_manager.is_initialized():
        try:
            # Log that we're about to make a selection decision
            empirica_manager.log_finding(
                finding=f"Analyzing {len(work_efforts)} work efforts for autonomous selection",
                impact=0.5,
            )
        except Exception as e:
            logger.debug(f"Empirica logging unavailable: {e}")

    # Calculate priority for each work effort
    scored_efforts = []
    total = len(work_efforts)
    for idx, we in enumerate(work_efforts, 1):
        if logger.isEnabledFor(logging.DEBUG):
            we_id = we.get("id", "unknown")
            logger.debug(f"Calculating priority for {we_id} ({idx}/{total})")
        # SECURITY: Validate work effort ID format
        we_id = we.get("id", "")
        if not we_id or not _validate_work_effort_id(we_id):
            logger.warning(f"Invalid work effort ID format: {we_id}")
            continue

        # SECURITY: Validate work effort path
        we_path = we.get("path", "")
        if we_path:
            we_dir = project_path / we_path
            if not _validate_work_effort_path(we_dir, project_path):
                logger.warning(f"Invalid work effort path: {we_path}")
                continue

        # Use Empirica and Pantheon-informed priority calculation
        score = calculate_work_effort_priority(
            we, project_path, empirica_manager, pantheon_entities
        )
        if score > 0:  # Only consider non-completed work
            scored_efforts.append((score, we))

    if not scored_efforts:
        return None

    # Sort by score (highest first)
    scored_efforts.sort(key=lambda x: x[0], reverse=True)

    # EMPIRICA: Use Empirica gate for final decision support if multiple high-scoring options
    selected = scored_efforts[0][1]
    if len(scored_efforts) > 1 and empirica_manager and empirica_manager.is_initialized():
        top_score = scored_efforts[0][0]
        second_score = scored_efforts[1][0]

        # If scores are close (within 10%), ask Empirica for guidance
        if top_score > 0 and (top_score - second_score) / top_score < 0.1:
            try:
                top_we = scored_efforts[0][1]
                second_we = scored_efforts[1][1]

                # Use Empirica check_submit for decision support (lighter than Oracle)
                decision_gate = empirica_manager.check_submit(
                    {
                        "type": "work_effort_selection",
                        "scope": "medium",
                        "description": f"Choose between {top_we.get('id')} (score: {top_score:.1f}) and {second_we.get('id')} (score: {second_score:.1f})",
                        "option_1": top_we.get("id"),
                        "option_2": second_we.get("id"),
                        "scores": {"option_1": top_score, "option_2": second_score},
                    }
                )

                # Empirica can suggest alternative if it has guidance
                # BRANCH might indicate second option needs investigation
                if decision_gate == "BRANCH" and second_we.get("id"):
                    logger.info(
                        f"Empirica suggests investigating {second_we.get('id')} - considering override"
                    )
                    # Don't override automatically, but log for awareness

            except Exception as e:
                logger.debug(f"Empirica decision support unavailable: {e}, using highest score")

    # PANTHEON: Use Judge and Decision Matrix for final selection validation
    if selected and pantheon_entities and PANTHEON_AVAILABLE:
        try:
            judge = pantheon_entities.get("judge")
            if judge:
                # Judge validates the selection
                judgment = judge.evaluate_claim(
                    claim=f"Work effort {selected.get('id')} is the best choice for autonomous execution",
                    category="work_efforts",
                    tags=["selection", "autonomous"],
                )

                # If Judge strongly disagrees, log warning
                if judgment.verdict.value == "DISPROVEN" and judgment.confidence > 0.8:
                    logger.warning(
                        f"Judge DISPROVES selection of {selected.get('id')} (confidence: {judgment.confidence:.2f})"
                    )
                    # Don't override, but log for awareness

            # Fae provides creative/whimsical perspective (for creative work efforts)
            fae = pantheon_entities.get("fae")
            if fae and len(scored_efforts) > 1:
                try:
                    # Check if any work effort matches active quests
                    active_quests = fae.list_quests(status="active")
                    if active_quests:
                        # If selected work effort aligns with a quest, boost slightly
                        we_title_lower = selected.get("title", "").lower()
                        for quest in active_quests[:3]:
                            if (
                                quest.name.lower() in we_title_lower
                                or we_title_lower in quest.name.lower()
                            ):
                                logger.info(
                                    f"Fae blessing: Selected work effort aligns with quest '{quest.name}'"
                                )
                                break
                except Exception as e:
                    logger.debug(f"Fae quest check unavailable: {e}")

            # MissionControl provides operational context
            mission_control = pantheon_entities.get("mission_control")
            if mission_control:
                try:
                    # Check if work effort is part of an active mission
                    registry = mission_control.registry_file
                    if registry.exists():
                        registry_data = json.loads(registry.read_text())
                        monitored = registry_data.get("missions_monitored", [])
                        we_id = selected.get("id", "")
                        if any(we_id in str(m) for m in monitored):
                            logger.info(
                                f"MissionControl: Work effort {we_id} is part of monitored mission"
                            )
                except Exception as e:
                    logger.debug(f"MissionControl check unavailable: {e}")

        except Exception as e:
            logger.debug(f"Pantheon selection validation unavailable: {e}")

    return selected


def _validate_work_effort_id(we_id: str) -> bool:
    """
    Validate work effort ID format (WE-YYMMDD-xxxx).

    SECURITY: Prevents injection via malformed IDs.
    """
    import re

    if not we_id or not isinstance(we_id, str):
        return False
    pattern = r"^WE-\d{6}-[a-z0-9]{4}$"
    return bool(re.match(pattern, we_id))


def get_work_effort_action(work_effort: dict, project_path: Path) -> dict | None:
    """
    Get the best action to take on a work effort.

    Returns the highest priority action, or None if no actions available.
    """
    actions = analyze_work_effort_actions(work_effort, project_path)
    if not actions:
        return None

    # Sort by priority (high > medium > low)
    priority_order = {"high": 3, "medium": 2, "low": 1}
    actions.sort(
        key=lambda a: priority_order.get(a.get("priority", "medium").lower(), 0), reverse=True
    )

    return actions[0]


def execute_work_effort_action(
    work_effort: dict,
    action: dict,
    project_path: Path,
    empirica_manager=None,
    pantheon_entities=None,
    campfire_available: bool = False,
    dnd_campaign=None,
) -> dict[str, Any]:
    """
    Execute an action on a work effort.

    SECURITY: Validates action type and sanitizes command before execution.
    Uses Empirica gates for safety.

    Returns execution result with the command to execute in Cursor.
    The actual execution happens in the Cursor AI context.
    """
    action_type = action.get("action", "")
    command = action.get("command", "")
    we_id = work_effort.get("id", "")
    we_path = work_effort.get("path", "")

    # SECURITY: Whitelist allowed action types
    ALLOWED_ACTIONS = {
        "status_transition",
        "add_progress",
        "review",
        "review_todos",
        "fix_issues",
        "review_changes",
    }

    if action_type not in ALLOWED_ACTIONS:
        logger.error(f"Invalid action type: {action_type}")
        return {
            "success": False,
            "error": f"Action type '{action_type}' not in whitelist",
        }

    # SECURITY: Validate work effort ID format
    if not _validate_work_effort_id(we_id):
        logger.error(f"Invalid work effort ID format: {we_id}")
        return {
            "success": False,
            "error": f"Invalid work effort ID format: {we_id}",
        }

    # SECURITY: Sanitize command (use parameterized template instead of f-string)
    # Command is already constructed in work_dashboard.py, but we validate it here
    if not command or len(command) > 500:  # Reasonable limit
        logger.error("Invalid command: too long or empty")
        return {
            "success": False,
            "error": "Command validation failed",
        }

    logger.info(f"Preparing action: {action_type} on {we_id}")
    logger.info(f"Command: {command}")

    # PANTHEON: TheReasoner creates reasoning trace for this decision
    trace_id = None
    if pantheon_entities and PANTHEON_AVAILABLE:
        try:
            reasoner = pantheon_entities.get("reasoner")
            if reasoner:
                trace_id = reasoner.create_trace(
                    decision=f"Execute {action_type} on work effort {we_id}",
                    reasoning=f"Selected work effort {we_id} ({work_effort.get('title', 'Unknown')}) with action '{action.get('label', action_type)}'. Reason: {action.get('reason', 'No reason provided')}",
                    context={
                        "work_effort_id": we_id,
                        "work_effort_title": work_effort.get("title", ""),
                        "work_effort_status": work_effort.get("status", ""),
                        "work_effort_priority": work_effort.get("priority", "MEDIUM"),
                        "action_type": action_type,
                        "action_label": action.get("label", ""),
                        "action_priority": action.get("priority", "medium"),
                        "command_preview": command[:100] if command else "",
                    },
                    outcome="Pending execution",
                )
                logger.debug(f"Reasoner trace created: {trace_id}")
        except Exception as e:
            logger.debug(f"Reasoner trace creation unavailable: {e}")

    # PANTHEON: Judge evaluates action safety
    if pantheon_entities and PANTHEON_AVAILABLE:
        try:
            judge = pantheon_entities.get("judge")
            if judge:
                judgment = judge.evaluate_claim(
                    claim=f"Action '{action_type}' on work effort {we_id} is safe to execute autonomously",
                    category="work_efforts",
                    tags=["autonomous", "execution", "safety"],
                )

                # If Judge strongly disagrees, treat as HALT
                if judgment.verdict.value == "DISPROVEN" and judgment.confidence > 0.9:
                    return {
                        "success": False,
                        "error": f"Judge DISPROVES action safety (confidence: {judgment.confidence:.2f}): {judgment.reasoning[:200]}",
                        "gate_result": "HALT",
                        "judge_verdict": "DISPROVEN",
                    }
        except Exception as e:
            logger.debug(f"Judge action evaluation unavailable: {e}")

    # EMPIRICA: Check with safety gate before execution
    if empirica_manager and empirica_manager.is_initialized():
        try:
            gate_result = empirica_manager.check_submit(
                {
                    "type": "auto_work_execution",
                    "scope": "high" if action.get("priority", "medium") == "high" else "medium",
                    "description": f"Execute {action_type} on work effort {we_id}",
                    "work_effort_id": we_id,
                    "action_type": action_type,
                    "command": command[:100],  # Include command preview (truncated)
                }
            )

            if gate_result == "HALT":
                # Log the halt decision
                try:
                    empirica_manager.log_finding(
                        finding=f"Execution HALTED by Empirica gate for {we_id} ({action_type}) - requires human approval",
                        impact=0.9,
                    )
                except Exception:
                    pass

                return {
                    "success": False,
                    "error": "Empirica gate: Operation requires human approval",
                    "gate_result": "HALT",
                }
            elif gate_result == "BRANCH":
                try:
                    empirica_manager.log_finding(
                        finding=f"Execution BRANCHED by Empirica gate for {we_id} ({action_type}) - investigation needed",
                        impact=0.8,
                    )
                except Exception:
                    pass

                return {
                    "success": False,
                    "error": "Empirica gate: Need investigation before execution",
                    "gate_result": "BRANCH",
                }
            elif gate_result == "REVISE":
                try:
                    empirica_manager.log_finding(
                        finding=f"Execution REVISED by Empirica gate for {we_id} ({action_type}) - approach needs revision",
                        impact=0.7,
                    )
                except Exception:
                    pass

                return {
                    "success": False,
                    "error": "Empirica gate: Approach needs revision",
                    "gate_result": "REVISE",
                }
            # PROCEED - log that we're proceeding
            elif gate_result == "PROCEED":
                try:
                    empirica_manager.log_finding(
                        finding=f"Execution PROCEEDED by Empirica gate for {we_id} ({action_type})",
                        impact=0.6,
                    )
                except Exception:
                    pass
            # None (Empirica unavailable) - continue silently
        except Exception as e:
            logger.warning(f"Empirica gate check failed: {e}, proceeding without gate")
            # Continue without gate if Empirica unavailable

    # PANTHEON: Update reasoning trace with execution result
    if trace_id and pantheon_entities and PANTHEON_AVAILABLE:
        try:
            reasoner = pantheon_entities.get("reasoner")
            if reasoner:
                # Update trace with execution instruction
                trace = reasoner.get_trace(trace_id)
                if trace:
                    trace["outcome"] = f"Execution instruction prepared: {command[:100]}..."
                    trace_file = reasoner.reasoner_path / "traces" / f"{trace_id}.json"
                    trace_file.write_text(json.dumps(trace, indent=2))
        except Exception as e:
            logger.debug(f"Reasoner trace update unavailable: {e}")

    # Build result with story information if available
    result = {
        "success": True,
        "work_effort_id": we_id,
        "work_effort_path": we_path,
        "work_effort_title": work_effort.get("title", ""),
        "action": action_type,
        "action_label": action.get("label", ""),
        "command": command,
        "context": {
            "reason": action.get("reason", ""),
            "priority": action.get("priority", "medium"),
        },
    }

    # Add story information if story was told
    if result.get("success") and campfire_available and CAMPFIRE_AVAILABLE:
        try:
            campfire = TheCampfire(project_path=project_path)

            # Create story about the work effort and action
            story_input = f"""## Work Effort: {work_effort.get("title", we_id)}

**Work Effort ID**: {we_id}
**Status**: {work_effort.get("status", "unknown")}
**Priority**: {work_effort.get("priority", "MEDIUM")}

### Action Taken

**Type**: {action_type}
**Label**: {action.get("label", "No label")}
**Reason**: {action.get("reason", "No reason provided")}

### Execution Instruction

{command}

### Context

This autonomous work execution was guided by:
- Empirica epistemic tracking
- Pantheon entities (Judge, Magistrate, TheReasoner, GitHubGod)
- Comprehensive safety gates and validation

The system selected this work effort from multiple candidates based on priority scoring, precedent analysis, and epistemic state assessment.
"""

            # Tell the story around the campfire
            story_result = campfire.gather_around_the_campfire(
                story_input=story_input,
                title=f"Autonomous Work: {work_effort.get('title', we_id)[:50]}",
                style="premium",
                narrative_style="medium",
                structure="linear",
                include_oracle=True,  # Include Oracle insights
                save_story=True,
            )

            # Add story metadata to result
            result["story"] = {
                "story_id": story_result.get("story", {}).get("id"),
                "pdf_path": story_result.get("pdf_path"),
                "title": story_result.get("story", {}).get("title"),
            }

            # Log that a story was told
            if empirica_manager and empirica_manager.is_initialized():
                try:
                    empirica_manager.log_finding(
                        finding=f"Story told around the campfire about work effort {we_id}",
                        impact=0.5,
                    )
                except Exception:
                    pass

            logger.info(
                f"Campfire story told: {story_result.get('story', {}).get('id', 'unknown')}"
            )

        except Exception as e:
            logger.debug(f"Campfire storytelling unavailable: {e}")
            # Don't fail execution if storytelling fails

    # D&D CAMPAIGN: Run a scenario and generate quest PDF
    if result.get("success") and dnd_campaign and DND_CAMPAIGN_AVAILABLE:
        try:
            orchestrator = dnd_campaign.get("orchestrator")
            quest_generator = dnd_campaign.get("quest_generator")

            if orchestrator and quest_generator:
                # Run a scenario (encounter, explore, or lore)
                import random

                scenario_modes = ["encounter", "explore", "lore"]
                scenario_mode = random.choice(scenario_modes)

                logger.info(f"Running D&D scenario: {scenario_mode}")

                # Run scenario
                scenario_result = orchestrator.run_scenario(mode=scenario_mode)

                # Generate quest markdown from scenario
                quest_markdown = _generate_quest_markdown_from_scenario(
                    scenario_result, work_effort, action
                )

                # Generate quest PDF using Typst
                quest_title = f"Quest: {work_effort.get('title', we_id)[:50]}"
                quest_pdf = quest_generator.generate_quest_pdf(
                    quest_markdown=quest_markdown,
                    quest_title=quest_title,
                    template="wenyuan-campaign",  # Use wenyuan-campaign template
                )

                if quest_pdf:
                    result["quest_pdf"] = {
                        "path": str(quest_pdf),
                        "scenario_mode": scenario_mode,
                        "scenario_result": scenario_result,
                    }

                    # Log quest generation
                    if empirica_manager and empirica_manager.is_initialized():
                        try:
                            empirica_manager.log_finding(
                                finding=f"D&D quest PDF generated: {quest_title} (scenario: {scenario_mode})",
                                impact=0.6,
                            )
                        except Exception:
                            pass

                    logger.info(f"Quest PDF generated: {quest_pdf}")

        except Exception as e:
            logger.debug(f"D&D campaign scenario unavailable: {e}")
            # Don't fail execution if campaign fails

    return result


def _generate_quest_markdown_from_scenario(
    scenario_result: dict[str, Any], work_effort: dict[str, Any], action: dict[str, Any]
) -> str:
    """
    Generate quest markdown from scenario result.

    Args:
        scenario_result: Result from scenario orchestrator
        work_effort: Work effort data
        action: Action data

    Returns:
        Quest markdown content
    """
    mode = scenario_result.get("mode", "unknown")
    we_id = work_effort.get("id", "Unknown")
    we_title = work_effort.get("title", "Unknown Quest")

    markdown = f"""# {we_title}

**Quest ID**: {we_id}
**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Scenario Type**: {mode.title()}

## Quest Overview

This quest was generated as part of autonomous work effort execution. The system selected this work effort and executed an action, then ran a D&D scenario to create this quest document.

### Work Effort Details

- **Work Effort ID**: {we_id}
- **Status**: {work_effort.get("status", "unknown")}
- **Priority**: {work_effort.get("priority", "MEDIUM")}
- **Action Taken**: {action.get("label", action.get("action", "Unknown"))}

## Scenario Details

"""

    if mode == "encounter":
        encounter = scenario_result.get("encounter", {})
        markdown += f"""### Combat Encounter

**Encounter Name**: {encounter.get("name", "Unknown Threat")}
**Difficulty**: {encounter.get("difficulty", "medium")}
**Rounds**: {scenario_result.get("rounds", "N/A")}
**Party HP**: {scenario_result.get("party_hp", "N/A")} / {scenario_result.get("party_max_hp", "N/A")}

#### Encounter Description

{encounter.get("description", "A challenging encounter awaits the party.")}

#### Rewards

- **Experience Gained**: {scenario_result.get("xp_gain", 0)} XP
- **Level Ups**: {len(scenario_result.get("level_ups", []))} party members leveled up

"""
    elif mode == "explore":
        location = scenario_result.get("location", "Unknown Location")
        markdown += f"""### Exploration

**Location Discovered**: {location}

The party explored {location} and discovered new areas of the realm. This location has been added to the world lore.

#### Discovery Details

- **Discovered By**: Party members
- **Lore Entry**: {scenario_result.get("lore_file", "N/A")}

"""
    elif mode == "lore":
        lore_type = scenario_result.get("lore_type", "unknown")
        lore_name = scenario_result.get("lore_name", "Unknown")
        markdown += f"""### Lore Building

**Lore Type**: {lore_type.title()}
**Lore Name**: {lore_name}

The party encountered new lore about the realm, expanding the world's history and knowledge.

#### Lore Details

- **Category**: {lore_type}
- **Entry Name**: {lore_name}
- **Lore File**: {scenario_result.get("lore_file", "N/A")}

"""

    markdown += """
## Quest Context

This quest was created as part of the autonomous work execution system, which:
- Analyzed multiple work efforts
- Selected the best one using priority scoring
- Executed an action to advance the work
- Ran a D&D scenario to create this quest document

The quest represents both the technical work (work effort execution) and the narrative adventure (D&D scenario) that emerged from it.

---

*Generated by WAFT Auto-Work System with D&D Campaign Integration*
"""

    return markdown


def main():
    """Main entry point for autonomous work execution."""
    # Flush immediately so user sees we're starting
    sys.stdout.flush()
    sys.stderr.flush()

    parser = argparse.ArgumentParser(description="Autonomous Work Effort Execution")
    parser.add_argument(
        "--path", type=str, default=".", help="Project path (default: current directory)"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done without executing"
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    project_path = Path(args.path).resolve()

    # Initialize logger (console + file + devlog)
    auto_logger = AutoWorkLogger(project_path, verbose=args.verbose)
    auto_logger.log("\n🤔 Thinking about work efforts...\n", flush=True)

    # EMPIRICA: Initialize Empirica manager early for use throughout
    print("🔬 Initializing Empirica...", end="", flush=True)
    empirica_manager = None
    try:
        from src.waft.core.empirica import EmpiricaManager

        empirica_manager = EmpiricaManager(project_path)
        if empirica_manager.is_initialized():
            auto_logger.log(" ✅ Active\n", flush=True)
            # Log that we're starting autonomous work
            try:
                empirica_manager.log_finding(
                    finding=f"Starting autonomous work effort selection (dry_run={args.dry_run})",
                    impact=0.7,
                )
            except Exception:
                pass  # Graceful degradation
        else:
            auto_logger.log(" ⚠️  Not initialized\n", flush=True)
    except Exception as e:
        auto_logger.log(f" ⚠️  Failed: {e}\n", flush=True)
        logger.warning(f"Empirica initialization failed: {e}, continuing without it")

    # PANTHEON: Initialize Pantheon entities for decision support
    pantheon_entities = {}
    if PANTHEON_AVAILABLE:
        try:
            auto_logger.log("⚡ Pantheon", end="", flush=True)

            # Initialize core entities (required)
            auto_logger.log(" → Magistrate", end="", flush=True)
            magistrate = Magistrate(project_path=project_path)
            auto_logger.log(" ✅", end="", flush=True)

            auto_logger.log(" → Judge", end="", flush=True)
            judge = Judge(project_path=project_path, magistrate=magistrate)
            auto_logger.log(" ✅", end="", flush=True)

            auto_logger.log(" → TheReasoner", end="", flush=True)
            reasoner = TheReasoner(project_path=project_path)
            auto_logger.log(" ✅", end="", flush=True)

            auto_logger.log(" → GitHubGod", end="", flush=True)
            github_god = GitHubGod(project_path=project_path)
            auto_logger.log(" ✅\n", flush=True)

            pantheon_entities = {
                "magistrate": magistrate,
                "judge": judge,
                "reasoner": reasoner,
                "github_god": github_god,
            }

            # Initialize optional entities (graceful degradation)
            try:
                auto_logger.log("  → Fae", end="", flush=True)
                fae = Fae(project_path=project_path)
                pantheon_entities["fae"] = fae
                auto_logger.log(" ✅\n", flush=True)
            except Exception as e:
                auto_logger.log(f" ⚠️  ({str(e)[:30]})\n", flush=True)

            try:
                auto_logger.log("  → MissionControl", end="", flush=True)
                mission_control = MissionControl(project_path=project_path)
                pantheon_entities["mission_control"] = mission_control
                auto_logger.log(" ✅\n", flush=True)
            except Exception as e:
                auto_logger.log(f" ⚠️  ({str(e)[:30]})\n", flush=True)

            try:
                auto_logger.log("  → Librarian", end="", flush=True)
                librarian = Librarian(project_path=project_path)
                pantheon_entities["librarian"] = librarian
                auto_logger.log(" ✅\n", flush=True)
            except Exception as e:
                auto_logger.log(f" ⚠️  ({str(e)[:30]})\n", flush=True)

            mem_mb = get_memory_usage_mb()
            auto_logger.log(f"  [Memory: {mem_mb:.1f} MB]\n", flush=True)

        except Exception as e:
            auto_logger.log(f" ⚠️  Failed: {e}\n", flush=True)
            logger.warning(f"Pantheon initialization failed: {e}, continuing without Pantheon")
            pantheon_entities = {}
    else:
        auto_logger.log("⚠️  Pantheon: Not available\n", flush=True)

    # CAMPFIRE: Initialize Campfire for storytelling
    auto_logger.log("🔥 Campfire", end="", flush=True)
    campfire_available = False
    if CAMPFIRE_AVAILABLE:
        try:
            campfire = TheCampfire(project_path=project_path)
            campfire_available = True
            auto_logger.log(" ✅\n", flush=True)
        except Exception as e:
            auto_logger.log(f" ⚠️  ({e})\n", flush=True)
            logger.debug(f"Campfire initialization failed: {e}, continuing without storytelling")
    else:
        auto_logger.log(" ⚠️  Not available\n", flush=True)

    # D&D CAMPAIGN: Initialize D&D campaign system
    auto_logger.log("⚔️  D&D Campaign", end="", flush=True)
    dnd_campaign = None
    if DND_CAMPAIGN_AVAILABLE:
        try:
            scenario_realm = ScenarioRealm(project_path=project_path)
            scenario_orchestrator = ScenarioOrchestrator(scenario_realm)
            quest_pdf_generator = QuestPDFGenerator(project_path=project_path)
            dnd_campaign = {
                "realm": scenario_realm,
                "orchestrator": scenario_orchestrator,
                "quest_generator": quest_pdf_generator,
            }
            status = "Typst ✅" if quest_pdf_generator.typst_available else "Typst ⚠️"
            auto_logger.log(f" ✅ ({status})\n", flush=True)
        except Exception as e:
            auto_logger.log(f" ⚠️  ({e})\n", flush=True)
            logger.warning(f"D&D Campaign initialization failed: {e}, continuing without campaign")
            dnd_campaign = None
    else:
        auto_logger.log(" ⚠️  Not available\n", flush=True)

    # Get all work efforts
    auto_logger.log("📂 Scanning work efforts...", end="", flush=True)
    work_efforts = get_work_efforts(project_path, days_back=0, verbose=args.verbose)  # Get all
    auto_logger.log(f" Found {len(work_efforts)} work effort(s)\n", flush=True)

    if not work_efforts:
        auto_logger.log("❌ No work efforts found.\n", flush=True)
        auto_logger.write_summary_to_devlog(success=False)
        return 1

    # Filter to actionable work efforts (not completed)
    auto_logger.log("🔍 Filtering actionable...", end="", flush=True)
    actionable = [we for we in work_efforts if we.get("status", "open").lower() != "completed"]
    auto_logger.log(f" {len(actionable)} actionable\n", flush=True)

    if not actionable:
        auto_logger.log("❌ No actionable work efforts found (all completed).\n", flush=True)
        auto_logger.write_summary_to_devlog(success=False)
        return 1

    # Select best work effort (with Empirica and Pantheon support)
    auto_logger.log(
        f"🎯 Calculating priorities for {len(actionable)} work effort(s)...", end="", flush=True
    )
    selected = select_best_work_effort(
        actionable, project_path, empirica_manager, pantheon_entities
    )
    auto_logger.log(" Done\n", flush=True)

    if not selected:
        auto_logger.log("❌ Could not select a work effort.\n", flush=True)
        auto_logger.write_summary_to_devlog(success=False)
        return 1

    we_id = selected.get("id", "unknown")
    we_title = selected.get("title", "Unknown")
    we_status = selected.get("status", "unknown")

    print(f"✅ Selected: {we_id}", flush=True)
    print(f"   Title: {we_title}", flush=True)
    print(f"   Status: {we_status}\n", flush=True)

    # EMPIRICA: Log selection decision
    if empirica_manager and empirica_manager.is_initialized():
        try:
            empirica_manager.log_finding(
                finding=f"Selected work effort {selected.get('id')} ({selected.get('title', 'Unknown')}) for autonomous execution",
                impact=0.8,
            )
        except Exception:
            pass

    # Get best action for this work effort
    auto_logger.log("🔍 Analyzing actions...", end="", flush=True)
    action = get_work_effort_action(selected, project_path)
    auto_logger.log(" Done\n", flush=True)

    if not action:
        auto_logger.log("❌ No actions available for this work effort.\n", flush=True)
        auto_logger.write_summary_to_devlog(selected_we=selected, success=False)
        return 1

    action_label = action.get("label", "Unknown")
    action_reason = action.get("reason", "")
    action_command = action.get("command", "")

    auto_logger.log(f"✅ Best action: {action_label}\n", flush=True)
    auto_logger.log(f"   Reason: {action_reason}\n", flush=True)
    auto_logger.log(f"   Command: {action_command}\n\n", flush=True)

    if args.dry_run:
        auto_logger.log("🔍 DRY RUN - Would execute:\n", flush=True)
        auto_logger.log(f"   {action_command}\n\n", flush=True)
        auto_logger.write_summary_to_devlog(selected_we=selected, action=action, success=True)
        return 0

    # Prepare the action (with error handling)
    auto_logger.log("🚀 Executing action...\n", flush=True)
    try:
        result = execute_work_effort_action(
            selected,
            action,
            project_path,
            empirica_manager,
            pantheon_entities,
            campfire_available=campfire_available,
            dnd_campaign=dnd_campaign,
        )
    except Exception as e:
        logger.error(f"Error executing action: {e}")
        auto_logger.log(f"❌ Execution error: {e}\n", flush=True)
        auto_logger.write_summary_to_devlog(selected_we=selected, action=action, success=False)
        return 1

    if result.get("success"):
        # Output JSON for Cursor AI to parse and execute
        output = {
            "selected_work_effort": {
                "id": result.get("work_effort_id"),
                "title": result.get("work_effort_title"),
                "path": result.get("work_effort_path"),
            },
            "action": {
                "type": result.get("action"),
                "label": result.get("action_label"),
                "command": result.get("command"),
                "context": result.get("context", {}),
            },
            "execution_instruction": result.get("command"),
        }

        auto_logger.log("✅ Work effort and action selected!\n", flush=True)
        auto_logger.log("=" * 60 + "\n", flush=True)
        auto_logger.log("AUTO-WORK RESULT (JSON):\n", flush=True)
        auto_logger.log("=" * 60 + "\n", flush=True)
        auto_logger.log(json.dumps(output, indent=2) + "\n", flush=True)
        auto_logger.log("=" * 60 + "\n", flush=True)
        auto_logger.log("\n🚀 EXECUTING NOW...\n", flush=True)
        auto_logger.log("=" * 60 + "\n", flush=True)
        auto_logger.log("EXECUTION INSTRUCTION:\n", flush=True)
        auto_logger.log("=" * 60 + "\n", flush=True)
        auto_logger.log(result.get("command", "") + "\n", flush=True)
        auto_logger.log("=" * 60 + "\n", flush=True)
        auto_logger.log("\n💡 Cursor AI: Execute the command above now.\n", flush=True)

        # Write summary to devlog
        auto_logger.write_summary_to_devlog(selected_we=selected, action=action, success=True)

        return 0
    else:
        error = result.get("error", "Unknown error")
        gate_result = result.get("gate_result")
        if gate_result:
            auto_logger.log(f"⚠️  Empirica Gate: {gate_result}\n", flush=True)
            auto_logger.log(f"   {error}\n\n", flush=True)
            auto_logger.log(
                "💡 This action requires human approval or investigation before execution.\n",
                flush=True,
            )
        else:
            auto_logger.log(f"❌ Failed: {error}\n", flush=True)

        auto_logger.write_summary_to_devlog(selected_we=selected, action=action, success=False)
        return 1


if __name__ == "__main__":
    exit(main())
