"""
WAFT Dashboard - Complete Streamlit Interface

Launch with: streamlit run waft_dashboard.py
"""

import streamlit as st
from pathlib import Path

# Page config
st.set_page_config(
    page_title="WAFT Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🧬 WAFT Dashboard</div>', unsafe_allow_html=True)
st.markdown("**Wave Agent Framework & Tools - Evolution, Beings, and Visualization**")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("🎛️ Navigation")
    st.markdown("Select a tab above to explore WAFT")
    st.markdown("---")
    st.subheader("📚 Quick Links")
    st.markdown("- [Quickstart Guide](./EVOLUTION_QUICKSTART.md)")
    st.markdown("- [Evolution Concept](./evolution_visualization_idea.md)")
    st.markdown("---")
    st.caption("WAFT v0.9.4")

# Main tabs
tab1, tab2, tab3 = st.tabs([
    "🧬 Evolution Arena",
    "🏘️ AI Town", 
    "📊 Status & Logs"
])

with tab1:
    st.header("🧬 Evolution Arena")
    st.markdown("**Watch agents evolve through natural selection in real-time**")
    st.markdown("---")

    try:
        from src.waft.ui.streamlit.evolution_arena import render_evolution_arena
        render_evolution_arena()
    except Exception as e:
        st.error(f"Error loading Evolution Arena: {e}")
        st.info("Make sure you're running from the WAFT root directory")

with tab2:
    st.header("🏘️ AI Town")
    st.markdown("**Interactive simulation of agents in a virtual town**")
    st.markdown("---")

    try:
        from src.waft.ui.streamlit.town_integration import render_town_integration
        project_path = Path.cwd()
        render_town_integration(project_path)
    except Exception as e:
        st.error(f"Error loading AI Town: {e}")
        st.info("Make sure you're running from the WAFT root directory")

with tab3:
    st.header("📊 Status & Logs")
    st.markdown("**View evolution logs and system status**")
    st.markdown("---")

    project_path = Path.cwd()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📁 Flight Recorder")
        flight_recorder_path = project_path / "_pyrite" / "flight_recorder"

        if flight_recorder_path.exists():
            master_log = flight_recorder_path / "evolution_master.jsonl"
            if master_log.exists():
                with open(master_log) as f:
                    lines = f.readlines()
                st.metric("Total Evolution Events", len(lines))

                if lines:
                    st.write("**Recent Events:**")
                    import json
                    for line in lines[-3:]:
                        event = json.loads(line)
                        with st.expander(f"Gen {event.get('generation', '?')} - {event.get('timestamp', '')[:19]}"):
                            st.json(event)
            else:
                st.info("No evolution events yet. Run `waft evolve` to create some!")
        else:
            st.warning("Flight recorder directory not found")

    with col2:
        st.subheader("🏋️ Gym Logs")
        gym_logs_path = project_path / "_pyrite" / "gym_logs"

        if gym_logs_path.exists():
            log_files = list(gym_logs_path.glob("*.jsonl"))
            st.metric("Beings Evaluated", len(log_files))

            if log_files:
                st.write("**Recent Evaluations:**")
                latest_log = sorted(log_files, key=lambda p: p.stat().st_mtime, reverse=True)[0]
                st.write(f"**{latest_log.name}**")

                with open(latest_log) as f:
                    lines = f.readlines()
                    if lines:
                        import json
                        latest_eval = json.loads(lines[-1])
                        st.json(latest_eval)
        else:
            st.warning("Gym logs directory not found")

    st.markdown("---")
    st.subheader("👥 Beings")

    beings_path = project_path / "_hidden" / ".truth" / "beings"
    if beings_path.exists():
        beings = [d.name for d in beings_path.iterdir() if d.is_dir()]
        st.metric("Total Beings", len(beings))

        if beings:
            with st.expander(f"View All {len(beings)} Beings"):
                for being_id in sorted(beings, reverse=True):
                    st.code(being_id, language=None)
    else:
        st.info("No beings yet. Spawn some with the Evolution Arena!")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>"
    "WAFT v0.9.4 | 🧬 Don't just build agents. Breed them."
    "</div>",
    unsafe_allow_html=True
)
