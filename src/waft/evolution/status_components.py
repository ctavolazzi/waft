"""
Status Components: Reusable PDF components for WAFT Kernel Status Reports

Provides specialized components for displaying:
- Epistemic State (moon phase, knowledge %, uncertainty %)
- Gamification Metrics (level, integrity, insight points)
- Flight Recorder Events (recent evolutionary events)
- Epistemic Phase Declaration
- System Health Metrics
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
import html

from .document_components import DocumentComponent, ComponentType, ComponentBuilder


# Add new component types for status elements
class StatusComponentType:
    """Status-specific component types."""
    EPISTEMIC_STATE = "epistemic_state"
    GAMIFICATION = "gamification"
    FLIGHT_RECORDER = "flight_recorder"
    EPISTEMIC_PHASE = "epistemic_phase"
    SYSTEM_HEALTH = "system_health"
    METRICS_TABLE = "metrics_table"
    PROGRESS_BAR = "progress_bar"
    STATUS_BADGES = "status_badges"


class StatusComponentBuilder:
    """Builder for status-specific PDF components."""
    
    @staticmethod
    def build_epistemic_state_component(epistemic_data: Dict[str, Any]) -> DocumentComponent:
        """
        Build epistemic state component with moon phase, knowledge, uncertainty.
        
        Args:
            epistemic_data: Dictionary with keys:
                - initialized: bool
                - moon_phase: str (emoji)
                - moon_phase_desc: str
                - knowledge_pct: Optional[float]
                - uncertainty_pct: Optional[float]
                - vectors: Dict (optional)
                - message: Optional[str] (error message if not initialized)
        
        Returns:
            DocumentComponent for epistemic state
        """
        if not epistemic_data.get("initialized", False):
            message = epistemic_data.get("message", "Empirica not initialized")
            body = f"<p><strong>Status:</strong> {html.escape(message)}</p>"
        else:
            moon_emoji = epistemic_data.get("moon_phase", "🌑")
            moon_desc = epistemic_data.get("moon_phase_desc", "Unknown")
            knowledge_pct = epistemic_data.get("knowledge_pct")
            uncertainty_pct = epistemic_data.get("uncertainty_pct")
            
            body = f"""
            <div class="epistemic-state">
                <div class="moon-phase">
                    <span class="moon-emoji">{moon_emoji}</span>
                    <span class="moon-desc">{html.escape(moon_desc)}</span>
                </div>
            """
            
            if knowledge_pct is not None:
                body += f'<p><strong>Knowledge:</strong> {knowledge_pct:.1f}%</p>'
            if uncertainty_pct is not None:
                body += f'<p><strong>Uncertainty:</strong> {uncertainty_pct:.1f}%</p>'
            
            body += "</div>"
        
        return DocumentComponent(
            component_type=ComponentType.SECTION,
            content={
                "title": "Epistemic State",
                "body": body
            },
            metadata={
                "level": 2,
                "component_subtype": StatusComponentType.EPISTEMIC_STATE
            },
            size_estimate=0.15,
            priority=0.9
        )
    
    @staticmethod
    def build_gamification_component(gamification_data: Dict[str, Any]) -> DocumentComponent:
        """
        Build gamification metrics component.
        
        Args:
            gamification_data: Dictionary with keys:
                - available: bool
                - level: int
                - integrity: float
                - insight: float
                - achievements: List[str]
                - achievements_count: int
                - message: Optional[str] (error message if not available)
        
        Returns:
            DocumentComponent for gamification
        """
        if not gamification_data.get("available", False):
            message = gamification_data.get("message", "Gamification data not available")
            body = f"<p><strong>Status:</strong> {html.escape(message)}</p>"
        else:
            level = gamification_data.get("level", 1)
            integrity = gamification_data.get("integrity", 100.0)
            insight = gamification_data.get("insight", 0.0)
            achievements_count = gamification_data.get("achievements_count", 0)
            
            body = f"""
            <table class="gamification-table">
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Character Level</td>
                    <td>{level}</td>
                </tr>
                <tr>
                    <td>Integrity Score</td>
                    <td>{integrity:.1f}%</td>
                </tr>
                <tr>
                    <td>Insight Points</td>
                    <td>{insight:.0f}</td>
                </tr>
                <tr>
                    <td>Achievements</td>
                    <td>{achievements_count}</td>
                </tr>
            </table>
            """
        
        return DocumentComponent(
            component_type=ComponentType.SECTION,
            content={
                "title": "Gamification",
                "body": body
            },
            metadata={
                "level": 2,
                "component_subtype": StatusComponentType.GAMIFICATION
            },
            size_estimate=0.12,
            priority=0.8
        )
    
    @staticmethod
    def build_flight_recorder_component(flight_events: List[Dict[str, Any]], limit: int = 5) -> DocumentComponent:
        """
        Build Flight Recorder events component.
        
        Args:
            flight_events: List of event dictionaries from TheObserver
            limit: Maximum number of events to display
        
        Returns:
            DocumentComponent for Flight Recorder events
        """
        if not flight_events:
            body = "<p>No recent events recorded.</p>"
        else:
            # Format events for display
            events_html = []
            for event in flight_events[-limit:]:
                event_type = event.get("event_type", "unknown")
                timestamp = event.get("timestamp", "unknown")
                genome_id = event.get("genome_id", "")
                
                # Format timestamp
                if isinstance(timestamp, str) and "T" in timestamp:
                    try:
                        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                        timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        pass
                
                # Truncate genome_id for display
                genome_display = genome_id[:8] + "..." if len(genome_id) > 8 else genome_id or "N/A"
                
                events_html.append(
                    f'<li><strong>{html.escape(event_type)}</strong> - '
                    f'Genome: {html.escape(genome_display)} - '
                    f'{html.escape(str(timestamp))}</li>'
                )
            
            body = f"""
            <p><strong>Recent Events:</strong> {len(flight_events)}</p>
            <ul class="flight-events">
                {''.join(events_html)}
            </ul>
            """
        
        return DocumentComponent(
            component_type=ComponentType.SECTION,
            content={
                "title": "Flight Recorder (Recent Events)",
                "body": body
            },
            metadata={
                "level": 2,
                "component_subtype": StatusComponentType.FLIGHT_RECORDER
            },
            size_estimate=0.20,
            priority=0.7
        )
    
    @staticmethod
    def build_epistemic_phase_component(phase: str) -> DocumentComponent:
        """
        Build epistemic phase declaration component.
        
        Args:
            phase: Epistemic phase string (e.g., "Data Gathering", "Synthesis", "Evolution")
        
        Returns:
            DocumentComponent for epistemic phase
        """
        body = f"""
        <div class="epistemic-phase">
            <p class="phase-badge">{html.escape(phase)}</p>
        </div>
        """
        
        return DocumentComponent(
            component_type=ComponentType.SECTION,
            content={
                "title": "Epistemic Phase",
                "body": body
            },
            metadata={
                "level": 2,
                "component_subtype": StatusComponentType.EPISTEMIC_PHASE
            },
            size_estimate=0.08,
            priority=1.0  # High priority - always show phase
        )
    
    @staticmethod
    def build_system_health_component(health_data: Dict[str, Any]) -> DocumentComponent:
        """
        Build system health metrics component.
        
        Args:
            health_data: Dictionary with keys:
                - pyrite_valid: bool
                - structure_valid: bool
                - lock_exists: bool
        
        Returns:
            DocumentComponent for system health
        """
        body = f"""
        <table class="health-table">
            <tr>
                <th>Component</th>
                <th>Status</th>
            </tr>
            <tr>
                <td>_pyrite Structure</td>
                <td>{'✅ Valid' if health_data.get('pyrite_valid') else '❌ Invalid'}</td>
            </tr>
            <tr>
                <td>Directory Structure</td>
                <td>{'✅ Valid' if health_data.get('structure_valid') else '❌ Invalid'}</td>
            </tr>
            <tr>
                <td>Dependency Lock</td>
                <td>{'✅ Present' if health_data.get('lock_exists') else '❌ Missing'}</td>
            </tr>
        </table>
        """
        
        return DocumentComponent(
            component_type=ComponentType.SECTION,
            content={
                "title": "System Health",
                "body": body
            },
            metadata={
                "level": 2,
                "component_subtype": StatusComponentType.SYSTEM_HEALTH
            },
            size_estimate=0.10,
            priority=0.8
        )
    
    @staticmethod
    def build_progress_bar_component(
        label: str,
        current: int,
        total: int,
        show_percentage: bool = True,
        show_fraction: bool = True
    ) -> DocumentComponent:
        """
        Build progress bar component (inspired by AI-DnD quest progress).
        
        Args:
            label: Progress label
            current: Current value
            total: Total/target value
            show_percentage: Show percentage text
            show_fraction: Show fraction text (e.g., "3/5")
        
        Returns:
            DocumentComponent for progress bar
        """
        if total <= 0:
            percentage = 0.0
        else:
            percentage = min((current / total) * 100, 100.0)
        
        progress_text_parts = []
        if show_fraction:
            progress_text_parts.append(f"{current}/{total}")
        if show_percentage:
            progress_text_parts.append(f"{percentage:.1f}%")
        progress_text = " - ".join(progress_text_parts) if progress_text_parts else ""
        
        body = f"""
        <div class="progress-container">
            <div class="progress-label">{html.escape(label)}</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {percentage}%"></div>
            </div>
            {f'<div class="progress-text">{progress_text}</div>' if progress_text else ''}
        </div>
        """
        
        return DocumentComponent(
            component_type=ComponentType.SECTION,
            content={
                "title": "",
                "body": body
            },
            metadata={
                "level": 3,
                "component_subtype": StatusComponentType.PROGRESS_BAR
            },
            size_estimate=0.08,
            priority=0.7
        )
    
    @staticmethod
    def build_status_badges_component(
        badges: List[Dict[str, str]],
        title: Optional[str] = None
    ) -> DocumentComponent:
        """
        Build status badges component (inspired by AI-DnD status effects).
        
        Args:
            badges: List of badge dicts with keys:
                - label: Badge text
                - status: "good", "warning", "error", or "info"
                - icon: Optional emoji/icon
            title: Optional section title
        
        Returns:
            DocumentComponent for status badges
        """
        badge_html = "".join([
            f'<span class="status-badge status-{html.escape(badge.get("status", "info"))}">'
            f'{badge.get("icon", "")} {html.escape(badge.get("label", ""))}'
            f'</span>'
            for badge in badges
        ])
        
        body = f'<div class="status-badges">{badge_html}</div>'
        
        return DocumentComponent(
            component_type=ComponentType.SECTION,
            content={
                "title": title or "",
                "body": body
            },
            metadata={
                "level": 3,
                "component_subtype": StatusComponentType.STATUS_BADGES
            },
            size_estimate=0.06,
            priority=0.6
        )
    
    @staticmethod
    def build_metrics_table_component(
        title: str,
        metrics: List[Dict[str, Any]],
        columns: List[str] = None
    ) -> DocumentComponent:
        """
        Build a generic metrics table component.
        
        Args:
            title: Table title
            metrics: List of metric dictionaries
            columns: Column names (auto-detected from first metric if None)
        
        Returns:
            DocumentComponent for metrics table
        """
        if not metrics:
            body = "<p>No metrics available.</p>"
        else:
            # Auto-detect columns if not provided
            if columns is None and metrics:
                columns = list(metrics[0].keys())
            
            if columns:
                # Build table header
                header = '<tr>' + ''.join(f'<th>{html.escape(str(col))}</th>' for col in columns) + '</tr>'
                
                # Build table rows
                rows = []
                for metric in metrics:
                    row = '<tr>' + ''.join(
                        f'<td>{html.escape(str(metric.get(col, "")))}</td>' for col in columns
                    ) + '</tr>'
                    rows.append(row)
                
                body = f"""
                <table class="metrics-table">
                    {header}
                    {''.join(rows)}
                </table>
                """
            else:
                body = "<p>No columns defined.</p>"
        
        return DocumentComponent(
            component_type=ComponentType.SECTION,
            content={
                "title": title,
                "body": body
            },
            metadata={
                "level": 2,
                "component_subtype": StatusComponentType.METRICS_TABLE
            },
            size_estimate=0.15,
            priority=0.7
        )


def create_status_components_from_status_dict(status: Dict[str, Any]) -> List[DocumentComponent]:
    """
    Create all status components from a complete status dictionary.
    
    Args:
        status: Complete status dictionary from check_status()
    
    Returns:
        List of DocumentComponent objects ready for PDF generation
    """
    builder = StatusComponentBuilder()
    components = []
    
    # 1. Epistemic Phase (high priority)
    epistemic_phase = status.get("epistemic_phase")
    if not epistemic_phase or epistemic_phase == "Unknown":
        # Try to determine from status
        try:
            import sys
            from pathlib import Path
            sys.path.insert(0, str(Path(__file__).parent.parent.parent))
            from scripts.waft_status import declare_epistemic_phase
            epistemic_phase = declare_epistemic_phase(status)
        except Exception:
            epistemic_phase = "Unknown"
    components.append(builder.build_epistemic_phase_component(epistemic_phase))
    
    # 2. Epistemic State
    epistemic_state = status.get("epistemic_state", {})
    components.append(builder.build_epistemic_state_component(epistemic_state))
    
    # 3. Gamification
    gamification_state = status.get("gamification_state", {})
    components.append(builder.build_gamification_component(gamification_state))
    
    # 4. Flight Recorder Events
    flight_events = status.get("flight_recorder_events", [])
    components.append(builder.build_flight_recorder_component(flight_events, limit=5))
    
    # 5. System Health
    project_health = status.get("project_health", {})
    components.append(builder.build_system_health_component(project_health))
    
    # 6. System Health Badges (enhanced display)
    if project_health:
        health_badges = []
        if project_health.get("pyrite_valid"):
            health_badges.append({"label": "Pyrite Valid", "status": "good", "icon": "✅"})
        else:
            health_badges.append({"label": "Pyrite Invalid", "status": "error", "icon": "❌"})
        
        if project_health.get("lock_exists"):
            health_badges.append({"label": "Lock File", "status": "good", "icon": "🔒"})
        else:
            health_badges.append({"label": "No Lock File", "status": "warning", "icon": "⚠️"})
        
        if project_health.get("structure_valid"):
            health_badges.append({"label": "Structure Valid", "status": "good", "icon": "📁"})
        else:
            health_badges.append({"label": "Structure Invalid", "status": "error", "icon": "📁"})
        
        if health_badges:
            components.append(builder.build_status_badges_component(health_badges, "System Health"))
    
    # 7. Epistemic Progress Bar (if initialized)
    epistemic_state = status.get("epistemic_state", {})
    if epistemic_state.get("initialized") and epistemic_state.get("knowledge_pct") is not None:
        knowledge_pct = epistemic_state.get("knowledge_pct", 0.0)
        components.append(builder.build_progress_bar_component(
            "Epistemic Knowledge",
            int(knowledge_pct),
            100,
            show_percentage=True,
            show_fraction=False
        ))
    
    return components
