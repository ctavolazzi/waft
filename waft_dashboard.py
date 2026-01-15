"""
WAFT Dashboard - Comprehensive Streamlit UI

A unified interface for all WAFT systems:
- CLI commands
- Being system
- Work efforts
- Empirica
- Gamification
- TavernKeeper
- AI Town

Run with: streamlit run waft_dashboard.py
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

# Import WAFT systems
from waft.being import BeingSystem
from waft.core.empirica import EmpiricaManager
from waft.core.gamification import GamificationManager
from waft.core.memory import MemoryManager
from waft.core.tavern_keeper import TavernKeeper

# Import UI modules
try:
    from waft.ui.streamlit import cli_integration
    from waft.ui.streamlit import being_integration
    from waft.ui.streamlit import work_efforts_integration
    from waft.ui.streamlit import empirica_integration
    from waft.ui.streamlit import gamification_integration
    from waft.ui.streamlit import tavern_integration
    from waft.ui.streamlit import town_integration
    from waft.ui.streamlit import town_view
    from waft.ui.streamlit import utils
except ImportError as e:
    st.error(f"Failed to import UI modules: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="WAFT Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .status-good {
        color: #28a745;
        font-weight: bold;
    }
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'project_path' not in st.session_state:
        st.session_state.project_path = Path.cwd()
    
    if 'being_system' not in st.session_state:
        try:
            st.session_state.being_system = BeingSystem(project_path=st.session_state.project_path)
        except Exception as e:
            st.session_state.being_system = None
            st.session_state.being_error = str(e)
    
    if 'empirica_manager' not in st.session_state:
        try:
            st.session_state.empirica_manager = EmpiricaManager(project_path=st.session_state.project_path)
        except Exception as e:
            st.session_state.empirica_manager = None
    
    if 'gamification_manager' not in st.session_state:
        try:
            st.session_state.gamification_manager = GamificationManager(project_path=st.session_state.project_path)
        except Exception as e:
            st.session_state.gamification_manager = None
    
    if 'memory_manager' not in st.session_state:
        try:
            st.session_state.memory_manager = MemoryManager(project_path=st.session_state.project_path)
        except Exception as e:
            st.session_state.memory_manager = None
    
    if 'tavern_keeper' not in st.session_state:
        try:
            if TavernKeeper:
                st.session_state.tavern_keeper = TavernKeeper(project_path=st.session_state.project_path)
            else:
                st.session_state.tavern_keeper = None
        except Exception as e:
            st.session_state.tavern_keeper = None


def render_sidebar():
    """Render sidebar navigation."""
    st.sidebar.title("🌊 WAFT Dashboard")
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "👤 Being System",
            "📋 Work Efforts",
            "📊 Empirica",
            "🎮 Gamification",
            "🍺 TavernKeeper",
            "🏘️ AI Town",
            "⚙️ CLI Commands",
            "⚙️ Settings"
        ]
    )
    
    st.sidebar.markdown("---")
    
    # Quick stats
    st.sidebar.subheader("Quick Stats")
    
    # Being count
    if st.session_state.being_system:
        try:
            beings_path = st.session_state.project_path / "_hidden" / ".truth" / "beings"
            if beings_path.exists():
                being_count = len([d for d in beings_path.iterdir() if d.is_dir()])
                st.sidebar.metric("Beings", being_count)
        except:
            pass
    
    # Gamification stats
    if st.session_state.gamification_manager:
        try:
            st.sidebar.metric("Level", st.session_state.gamification_manager.level)
            st.sidebar.metric("Insight", f"{st.session_state.gamification_manager.insight:.1f}")
        except:
            pass
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Project**: `{st.session_state.project_path.name}`")
    st.sidebar.markdown(f"**Time**: {datetime.now().strftime('%H:%M:%S')}")
    
    return page


def render_dashboard():
    """Render main dashboard page."""
    st.markdown('<div class="main-header">🏠 WAFT Dashboard</div>', unsafe_allow_html=True)
    
    # Status overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("System Status", "🟢 Operational")
    
    with col2:
        if st.session_state.being_system:
            st.metric("Being System", "✅ Active")
        else:
            st.metric("Being System", "❌ Error")
    
    with col3:
        if st.session_state.empirica_manager:
            init_status = "✅" if st.session_state.empirica_manager.is_initialized() else "⚠️"
            st.metric("Empirica", init_status)
        else:
            st.metric("Empirica", "❌ Error")
    
    with col4:
        if st.session_state.gamification_manager:
            st.metric("Gamification", "✅ Active")
        else:
            st.metric("Gamification", "❌ Error")
    
    st.markdown("---")
    
    # Recent activity
    st.subheader("Recent Activity")
    
    # Work efforts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Recent Work Efforts")
        work_efforts_integration.render_recent_work_efforts(st.session_state.project_path)
    
    with col2:
        st.subheader("👤 Recent Beings")
        being_integration.render_recent_beings(st.session_state.being_system)
    
    # Quick actions
    st.markdown("---")
    st.subheader("Quick Actions")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("🆕 Spawn New Being", use_container_width=True):
            st.session_state.spawn_being = True
    
    with action_col2:
        if st.button("📋 Create Work Effort", use_container_width=True):
            st.session_state.create_work_effort = True
    
    with action_col3:
        if st.button("📊 View Empirica Dashboard", use_container_width=True):
            st.session_state.view_empirica = True


def main():
    """Main application entry point."""
    initialize_session_state()
    page = render_sidebar()
    
    # Route to appropriate page
    if page == "🏘️ Town View":
        town_view.render_town_view(
            st.session_state.being_system,
            st.session_state.empirica_manager,
            st.session_state.gamification_manager,
            st.session_state.tavern_keeper,
            st.session_state.project_path
        )
    elif page == "🏠 Dashboard":
        render_dashboard()
    elif page == "👤 Being System":
        being_integration.render_being_system_page(st.session_state.being_system, st.session_state.project_path)
    elif page == "📋 Work Efforts":
        work_efforts_integration.render_work_efforts_page(st.session_state.project_path)
    elif page == "📊 Empirica":
        empirica_integration.render_empirica_page(st.session_state.empirica_manager, st.session_state.project_path)
    elif page == "🎮 Gamification":
        gamification_integration.render_gamification_page(st.session_state.gamification_manager)
    elif page == "🍺 TavernKeeper":
        tavern_integration.render_tavern_page(st.session_state.tavern_keeper)
    elif page == "🏘️ AI Town":
        town_integration.render_town_page(st.session_state.project_path)
    elif page == "⚙️ CLI Commands":
        cli_integration.render_cli_commands_page(st.session_state.project_path)
    elif page == "⚙️ Settings":
        render_settings_page()
    
    # Handle modal actions
    if st.session_state.get('spawn_being'):
        being_integration.render_spawn_being_modal(st.session_state.being_system)
    
    if st.session_state.get('create_work_effort'):
        work_efforts_integration.render_create_work_effort_modal(st.session_state.project_path)


def render_settings_page():
    """Render settings page."""
    st.markdown('<div class="main-header">⚙️ Settings</div>', unsafe_allow_html=True)
    
    st.subheader("Project Configuration")
    st.text_input("Project Path", value=str(st.session_state.project_path), disabled=True)
    
    st.subheader("System Status")
    
    systems = [
        ("Being System", st.session_state.being_system),
        ("Empirica Manager", st.session_state.empirica_manager),
        ("Gamification Manager", st.session_state.gamification_manager),
        ("Memory Manager", st.session_state.memory_manager),
        ("TavernKeeper", st.session_state.tavern_keeper),
    ]
    
    for name, system in systems:
        status = "✅ Active" if system else "❌ Not Available"
        st.write(f"**{name}**: {status}")


if __name__ == "__main__":
    main()
