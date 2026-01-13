"""
Good Morning - WAFT Morning Briefing Dashboard

Entry point to the WAFT ecosystem showing:
- Activity since 5 AM previous day (TheChronicler observations)
- Work efforts status with details
- System health
- Oracle insights
- Activity visualizations
- Quick actions

Run with: streamlit run good_morning.py --server.port 8507
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import json
import re

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

# Import WAFT systems
try:
    from waft.core.chronicler import TheChronicler
    from waft.core.empirica import EmpiricaManager
    from waft.core.gamification import GamificationManager
    from waft.brief import BriefDocument
    from waft.core.science.oracle import TheOracle
except ImportError as e:
    st.error(f"Failed to import WAFT modules: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Good Morning - WAFT",
    page_icon="🌅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .morning-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1, #FFA07A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .section-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 1rem;
        border-left: 5px solid #4ECDC4;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .genesis-badge {
        background-color: #28a745;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.875rem;
        display: inline-block;
        margin-right: 0.5rem;
    }
    .exodus-badge {
        background-color: #dc3545;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.875rem;
        display: inline-block;
        margin-right: 0.5rem;
    }
    .mutation-badge {
        background-color: #ffc107;
        color: black;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.875rem;
        display: inline-block;
        margin-right: 0.5rem;
    }
    .work-effort-card {
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 0.5rem;
        transition: box-shadow 0.2s;
    }
    .work-effort-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .status-active {
        color: #28a745;
        font-weight: bold;
    }
    .status-completed {
        color: #6c757d;
    }
    .insight-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def get_since_5am_yesterday() -> Tuple[datetime, datetime]:
    """Get datetime range from 5 AM yesterday to now."""
    now = datetime.now()
    today_5am = now.replace(hour=5, minute=0, second=0, microsecond=0)
    
    # If it's before 5 AM today, go back to 5 AM yesterday
    if now.hour < 5:
        yesterday_5am = (today_5am - timedelta(days=1))
        return yesterday_5am, now
    else:
        # It's after 5 AM today, so use today's 5 AM
        return today_5am, now


def parse_work_effort_metadata(we_dir: Path) -> Optional[Dict[str, Any]]:
    """Parse work effort metadata from index.md file."""
    index_file = we_dir / "index.md"
    if not index_file.exists():
        # Try WE-*-index.md pattern
        for file in we_dir.parent.glob(f"{we_dir.name}*index.md"):
            index_file = file
            break
    
    if not index_file.exists():
        return None
    
    try:
        content = index_file.read_text()
        
        # Parse YAML frontmatter
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        metadata = {}
        
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    metadata[key] = value
        
        # Extract title from content if not in frontmatter
        if 'title' not in metadata:
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if title_match:
                metadata['title'] = title_match.group(1)
        
        # Count tickets
        tickets_dir = we_dir / "tickets"
        ticket_count = 0
        if tickets_dir.exists():
            ticket_count = len(list(tickets_dir.glob("TKT-*.md")))
        
        metadata['ticket_count'] = ticket_count
        metadata['path'] = str(we_dir.relative_to(project_root))
        
        return metadata
    except Exception:
        return None


def get_chronicler_observations(project_path: Path, start: datetime, end: datetime) -> Dict[str, Any]:
    """Get observations from TheChronicler with hourly breakdown."""
    try:
        chronicler = TheChronicler(project_path)
        observations = chronicler.storage.get_observations(start, end)
        
        # Categorize
        genesis = [o for o in observations if o.get("event_type") == "genesis"]
        exodus = [o for o in observations if o.get("event_type") == "exodus"]
        mutations = [o for o in observations if o.get("event_type") == "mutation"]
        
        # Group by observer
        by_observer: Dict[str, List] = {}
        for obs in observations:
            observer = obs.get("observer", "unknown")
            if observer not in by_observer:
                by_observer[observer] = []
            by_observer[observer].append(obs)
        
        # Hourly breakdown for chart
        hourly_breakdown: Dict[int, Dict[str, int]] = {}
        for obs in observations:
            try:
                obs_time = datetime.fromisoformat(obs["timestamp"])
                hour = obs_time.hour
                if hour not in hourly_breakdown:
                    hourly_breakdown[hour] = {"genesis": 0, "exodus": 0, "mutation": 0}
                event_type = obs.get("event_type", "unknown")
                if event_type in hourly_breakdown[hour]:
                    hourly_breakdown[hour][event_type] += 1
            except (KeyError, ValueError):
                continue
        
        return {
            "total": len(observations),
            "genesis": genesis,
            "exodus": exodus,
            "mutations": mutations,
            "by_observer": by_observer,
            "net_change": len(genesis) - len(exodus),
            "hourly_breakdown": hourly_breakdown
        }
    except Exception as e:
        st.warning(f"Could not load Chronicler observations: {e}")
        return {
            "total": 0,
            "genesis": [],
            "exodus": [],
            "mutations": [],
            "by_observer": {},
            "net_change": 0,
            "hourly_breakdown": {}
        }


def get_work_efforts_summary(project_path: Path) -> Dict[str, Any]:
    """Get work efforts summary with detailed metadata."""
    work_efforts_dir = project_path / "_work_efforts"
    if not work_efforts_dir.exists():
        return {"total": 0, "active": 0, "recent": [], "detailed": []}
    
    work_efforts = []
    for item in work_efforts_dir.iterdir():
        if item.is_dir() and item.name.startswith("WE-"):
            metadata = parse_work_effort_metadata(item)
            if metadata:
                work_efforts.append(metadata)
            else:
                # Fallback if no metadata
                work_efforts.append({
                    "id": item.name,
                    "status": "unknown",
                    "path": str(item.relative_to(project_path)),
                    "ticket_count": 0
                })
    
    # Sort by created date (most recent first)
    work_efforts.sort(key=lambda x: x.get("created", ""), reverse=True)
    
    active = [we for we in work_efforts if we.get("status", "").lower() == "active"]
    
    return {
        "total": len(work_efforts),
        "active": len(active),
        "recent": work_efforts[:10],
        "detailed": work_efforts
    }


def get_system_health(project_path: Path) -> Dict[str, Any]:
    """Get system health metrics with details."""
    health = {
        "chronicler": {"available": False, "running": False},
        "empirica": {"available": False, "initialized": False},
        "oracle": {"available": False},
        "gamification": {"available": False}
    }
    
    # Check Chronicler
    try:
        chronicler = TheChronicler(project_path)
        health["chronicler"]["available"] = True
        stats = chronicler.get_stats()
        health["chronicler"]["running"] = stats.get("running", False)
        health["chronicler"]["stats"] = stats
    except Exception:
        pass
    
    # Check Empirica
    try:
        empirica = EmpiricaManager(project_path)
        health["empirica"]["available"] = True
        health["empirica"]["initialized"] = empirica.is_initialized()
    except Exception:
        pass
    
    # Check Oracle
    try:
        oracle = TheOracle(project_path)
        health["oracle"]["available"] = True
        epistemic_state = oracle.get_epistemic_state()
        health["oracle"]["state"] = epistemic_state
    except Exception:
        pass
    
    # Check Gamification
    try:
        gamification = GamificationManager(project_path)
        health["gamification"]["available"] = True
    except Exception:
        pass
    
    return health


def get_oracle_insights(project_path: Path) -> List[str]:
    """Get recent insights from Oracle."""
    try:
        oracle = TheOracle(project_path)
        state = oracle.get_epistemic_state()
        
        insights = []
        if state.get("initialized"):
            findings = state.get("findings", [])
            for finding in findings[:3]:  # Top 3
                if isinstance(finding, dict):
                    insights.append(finding.get("description", str(finding)))
                else:
                    insights.append(str(finding))
        
        return insights
    except Exception:
        return []


def main():
    """Main morning briefing dashboard."""
    project_path = Path.cwd()
    
    # Header
    st.markdown('<div class="morning-header">🌅 Good Morning</div>', unsafe_allow_html=True)
    
    # Get time range
    start_time, end_time = get_since_5am_yesterday()
    time_range_str = f"{start_time.strftime('%B %d, %Y %H:%M')} to {end_time.strftime('%B %d, %Y %H:%M')}"
    
    st.markdown(f"### Activity Since 5 AM: {time_range_str}")
    
    # Show loading state
    with st.spinner("Loading morning briefing..."):
        # Get data
        observations = get_chronicler_observations(project_path, start_time, end_time)
        work_efforts = get_work_efforts_summary(project_path)
        system_health = get_system_health(project_path)
        oracle_insights = get_oracle_insights(project_path)
    
    # Top metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Genesis Events", len(observations["genesis"]), delta=observations["net_change"])
    
    with col2:
        st.metric("Exodus Events", len(observations["exodus"]))
    
    with col3:
        st.metric("Mutations", len(observations["mutations"]))
    
    with col4:
        st.metric("Work Efforts", work_efforts["active"], delta=f"{work_efforts['total']} total")
    
    with col5:
        healthy_systems = sum(1 for k, v in system_health.items() if v.get("available", False))
        st.metric("System Health", f"{healthy_systems}/4", delta="systems available")
    
    st.divider()
    
    # Oracle Insights (if available)
    if oracle_insights:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("### 💡 Oracle Insights")
        for insight in oracle_insights:
            st.markdown(f"• {insight}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content in two columns
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Activity Summary with Chart
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Activity Summary")
        
        if observations["total"] > 0:
            # Activity by observer
            st.markdown("#### By Observer")
            for observer, obs_list in observations["by_observer"].items():
                genesis_count = sum(1 for o in obs_list if o.get("event_type") == "genesis")
                exodus_count = sum(1 for o in obs_list if o.get("event_type") == "exodus")
                mutation_count = sum(1 for o in obs_list if o.get("event_type") == "mutation")
                
                st.markdown(f"**{observer.title()}**: {genesis_count} genesis, {exodus_count} exodus, {mutation_count} mutations")
            
            # Hourly activity chart
            if observations["hourly_breakdown"]:
                st.markdown("#### Activity Over Time")
                chart_data = []
                for hour in sorted(observations["hourly_breakdown"].keys()):
                    data = observations["hourly_breakdown"][hour]
                    chart_data.append({
                        "Hour": f"{hour:02d}:00",
                        "Genesis": data["genesis"],
                        "Exodus": data["exodus"],
                        "Mutations": data["mutation"]
                    })
                
                if chart_data:
                    import pandas as pd
                    df = pd.DataFrame(chart_data)
                    st.bar_chart(df.set_index("Hour"))
            
            # Recent genesis events
            if observations["genesis"]:
                with st.expander(f"Recent Creations ({len(observations['genesis'])} total)", expanded=False):
                    for obs in observations["genesis"][:20]:
                        path = obs.get("path", "unknown")
                        timestamp = obs.get("timestamp", "")
                        try:
                            dt = datetime.fromisoformat(timestamp)
                            time_str = dt.strftime("%H:%M")
                        except:
                            time_str = ""
                        st.markdown(f"<span class='genesis-badge'>GENESIS</span> <small>{time_str}</small> {path}", unsafe_allow_html=True)
            
            # Recent exodus events
            if observations["exodus"]:
                with st.expander(f"Recent Deletions ({len(observations['exodus'])} total)", expanded=False):
                    for obs in observations["exodus"][:20]:
                        path = obs.get("path", "unknown")
                        timestamp = obs.get("timestamp", "")
                        try:
                            dt = datetime.fromisoformat(timestamp)
                            time_str = dt.strftime("%H:%M")
                        except:
                            time_str = ""
                        st.markdown(f"<span class='exodus-badge'>EXODUS</span> <small>{time_str}</small> {path}", unsafe_allow_html=True)
        else:
            st.info("No observations recorded since 5 AM. Start TheChronicler to begin monitoring.")
            if st.button("📖 Learn about TheChronicler"):
                st.info("Run: `waft chronicler` or `/chronicle start` to begin monitoring system activity.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Work Efforts with Details
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Work Efforts")
        
        if work_efforts["active"] > 0:
            st.markdown(f"**{work_efforts['active']} active** out of {work_efforts['total']} total")
            
            # Show active work efforts
            active_we = [we for we in work_efforts["recent"] if we.get("status", "").lower() == "active"]
            if active_we:
                st.markdown("#### Active Work Efforts")
                for we in active_we[:5]:
                    title = we.get("title", we.get("id", "Unknown"))
                    status = we.get("status", "unknown")
                    ticket_count = we.get("ticket_count", 0)
                    
                    status_class = "status-active" if status.lower() == "active" else "status-completed"
                    st.markdown(f"""
                    <div class="work-effort-card">
                        <strong>{title}</strong><br>
                        <small class="{status_class}">{status.upper()}</small> | 
                        <small>{ticket_count} tickets</small> | 
                        <small>{we.get('id', '')}</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No active work efforts found.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        # System Health with Details
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ System Health")
        
        for system, info in system_health.items():
            available = info.get("available", False)
            status_icon = "✅" if available else "❌"
            
            if system == "chronicler" and available:
                running = info.get("running", False)
                running_icon = "🟢" if running else "⚪"
                stats = info.get("stats", {})
                st.markdown(f"{status_icon} **{system.title()}**: {running_icon} {'Running' if running else 'Available'}")
                if stats:
                    st.caption(f"Today: {stats.get('genesis_count', 0)} genesis, {stats.get('exodus_count', 0)} exodus")
            elif system == "empirica" and available:
                initialized = info.get("initialized", False)
                init_icon = "✓" if initialized else "○"
                st.markdown(f"{status_icon} **{system.title()}**: {init_icon} {'Initialized' if initialized else 'Available'}")
            elif system == "oracle" and available:
                state = info.get("state", {})
                if state.get("initialized"):
                    st.markdown(f"{status_icon} **{system.title()}**: ✅ Active")
                else:
                    st.markdown(f"{status_icon} **{system.title()}**: Available")
            else:
                st.markdown(f"{status_icon} **{system.title()}**: {'Available' if available else 'Inactive'}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 🚀 Quick Actions")
        
        action_col1, action_col2 = st.columns(2)
        
        with action_col1:
            if st.button("📊 Generate Morning Brief PDF", use_container_width=True):
                try:
                    with st.spinner("Generating brief..."):
                        brief = BriefDocument(
                            title="Morning Brief",
                            subtitle=datetime.now().strftime("%B %d, %Y"),
                            doc_id=f"MB-{datetime.now().strftime('%Y%m%d')}",
                            include_system_status=True,
                            chat_context={
                                "current_task": "Morning briefing and planning",
                                "recent_topics": [
                                    f"{len(observations['genesis'])} genesis events",
                                    f"{len(observations['exodus'])} exodus events",
                                    f"{work_efforts['active']} active work efforts"
                                ],
                                "next_steps": [
                                    "Review activity since 5 AM",
                                    "Plan work session",
                                    "Continue active work efforts"
                                ]
                            }
                        )
                        brief_path = brief.generate()
                        st.success(f"✅ Morning brief generated!")
                        st.info(f"📄 {brief_path}")
                except Exception as e:
                    st.error(f"Error generating brief: {e}")
            
            if st.button("👁️ Start TheChronicler", use_container_width=True):
                st.code("waft chronicler", language="bash")
                st.info("Or use: `/chronicle start`")
        
        with action_col2:
            if st.button("📈 View Full Dashboard", use_container_width=True):
                st.code("streamlit run waft_dashboard.py", language="bash")
                st.info("Opens on port 8501")
            
            if st.button("🔄 Refresh Dashboard", use_container_width=True):
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # External Data Section
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 🌐 External Data")
        
        # Placeholder for external integrations
        st.info("💡 External data integration coming soon")
        st.markdown("""
        **Planned integrations:**
        - Weather API
        - Calendar events
        - News/updates
        - Custom data sources
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.divider()
    st.markdown(f"<div style='text-align: center; color: #666;'>WAFT Ecosystem Entry Point | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
