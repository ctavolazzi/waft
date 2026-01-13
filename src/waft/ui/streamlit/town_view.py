"""
Integrated Town View - Complete WAFT Town Dashboard

Shows everything at once in a unified town-like interface:
- Beings walking around
- Work efforts as buildings/structures
- Empirica as knowledge centers
- Gamification as character stats
- TavernKeeper as the central tavern
- AI Town integrated
"""

import streamlit as st
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

# Import all integrations
from . import being_integration
from . import work_efforts_integration
from . import empirica_integration
from . import gamification_integration
from . import tavern_integration
from . import town_integration
from . import cli_integration
from .utils import display_error, display_success


def render_town_view(
    being_system,
    empirica_manager,
    gamification_manager,
    tavern_keeper,
    project_path: Path
):
    """Render the complete integrated town view."""
    
    st.markdown("""
    <style>
    .town-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .town-section {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 1rem;
        border: 2px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .town-building {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="town-header">🏘️ WAFT TOWN</div>', unsafe_allow_html=True)
    
    # Top row: System status and quick stats
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🌊 System", "🟢 Active")
    
    with col2:
        if being_system:
            beings_path = project_path / "_hidden" / ".truth" / "beings"
            being_count = len([d for d in beings_path.iterdir() if d.is_dir()]) if beings_path.exists() else 0
            st.metric("👤 Beings", being_count)
        else:
            st.metric("👤 Beings", "❌")
    
    with col3:
        if empirica_manager:
            st.metric("📊 Empirica", "✅")
        else:
            st.metric("📊 Empirica", "❌")
    
    with col4:
        if gamification_manager:
            st.metric("🎮 Level", gamification_manager.level)
        else:
            st.metric("🎮 Level", "❌")
    
    with col5:
        work_efforts_path = project_path / "_work_efforts"
        if work_efforts_path.exists():
            work_efforts = [d for d in work_efforts_path.iterdir() if d.is_dir() and d.name.startswith("WE-")]
            st.metric("📋 Work Efforts", len(work_efforts))
        else:
            st.metric("📋 Work Efforts", 0)
    
    st.markdown("---")
    
    # Main town layout: 3 columns
    left_col, center_col, right_col = st.columns([1, 2, 1])
    
    # LEFT COLUMN: Beings & Character Stats
    with left_col:
        st.markdown('<div class="town-section">', unsafe_allow_html=True)
        st.subheader("👤 Beings District")
        
        if being_system:
            beings_path = project_path / "_hidden" / ".truth" / "beings"
            if beings_path.exists():
                beings = [d.name for d in beings_path.iterdir() if d.is_dir()]
                if beings:
                    for being_id in beings[:5]:  # Show 5 most recent
                        st.markdown(f'<div class="town-building">👤 {being_id[:20]}...</div>', unsafe_allow_html=True)
                else:
                    st.info("No beings yet")
            else:
                st.info("Beings directory not found")
        else:
            st.error("Being System not available")
        
        st.markdown("---")
        
        # Character Stats (Gamification)
        st.subheader("🎮 Character Sheet")
        if gamification_manager:
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Level", gamification_manager.level)
                st.metric("Insight", f"{gamification_manager.insight:.1f}")
            with col_b:
                st.metric("XP", f"{gamification_manager.xp:.0f}")
                st.metric("Credits", f"{gamification_manager.credits:.0f}")
        else:
            st.info("Gamification not available")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # CENTER COLUMN: Main Town Square (Work Efforts, Empirica, Tavern)
    with center_col:
        # Work Efforts as Buildings
        st.markdown('<div class="town-section">', unsafe_allow_html=True)
        st.subheader("📋 Work Efforts Quarter")
        
        work_efforts_path = project_path / "_work_efforts"
        if work_efforts_path.exists():
            work_efforts = []
            for item in work_efforts_path.iterdir():
                if item.is_dir() and item.name.startswith("WE-"):
                    work_efforts.append({
                        'id': item.name,
                        'title': item.name.replace("WE-", "").replace("_", " ").title()
                    })
            
            if work_efforts:
                # Show work efforts as "buildings"
                for effort in work_efforts[:6]:  # Show 6 most recent
                    with st.expander(f"🏗️ {effort['id']}"):
                        st.write(f"**{effort['title']}**")
                        if st.button(f"View Details", key=f"view_{effort['id']}"):
                            st.session_state.selected_work_effort = effort['id']
            else:
                st.info("No work efforts yet")
        else:
            st.info("Work efforts directory not found")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Empirica Knowledge Center
        st.markdown('<div class="town-section">', unsafe_allow_html=True)
        st.subheader("📊 Empirica Knowledge Center")
        
        if empirica_manager:
            if empirica_manager.is_initialized():
                st.success("✅ Empirica Active")
                if st.button("📈 View Epistemic Dashboard"):
                    st.session_state.view_empirica = True
            else:
                st.warning("⚠️ Empirica not initialized")
        else:
            st.info("Empirica not available")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # TavernKeeper Central Tavern
        st.markdown('<div class="town-section">', unsafe_allow_html=True)
        st.subheader("🍺 The Tavern")
        
        if tavern_keeper:
            st.success("✅ Tavern Open")
            chronicle_path = project_path / "_pyrite" / ".waft" / "chronicles.json"
            if chronicle_path.exists():
                try:
                    with open(chronicle_path, 'r') as f:
                        chronicles = json.load(f)
                        if chronicles:
                            st.write(f"**Recent Events**: {len(chronicles)} entries")
                            # Show last 3 entries
                            for entry in list(chronicles.values())[-3:]:
                                if isinstance(entry, dict) and 'message' in entry:
                                    st.caption(f"📜 {entry.get('message', '')[:50]}...")
                except:
                    pass
        else:
            st.info("Tavern not available")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # RIGHT COLUMN: AI Town & Quick Actions
    with right_col:
        st.markdown('<div class="town-section">', unsafe_allow_html=True)
        st.subheader("🏘️ AI Town")
        
        # Check if AI Town is available
        try:
            from waft.ai_town import TownWorld
            if 'town_world' in st.session_state and st.session_state.town_world:
                town = st.session_state.town_world
                st.metric("Agents", len(town.agents))
                st.metric("Conversations", len([a for a in town.agents.values() if a.current_conversation]))
                if st.button("🗺️ View Town Map"):
                    st.session_state.view_town = True
            else:
                if st.button("🏗️ Create AI Town"):
                    st.session_state.town_world = TownWorld(name="WAFT AI Town")
                    st.rerun()
        except ImportError:
            st.info("AI Town not available")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick Actions
        st.markdown('<div class="town-section">', unsafe_allow_html=True)
        st.subheader("⚡ Quick Actions")
        
        if st.button("🆕 Spawn Being", use_container_width=True):
            st.session_state.spawn_being = True
        
        if st.button("📋 Create Work Effort", use_container_width=True):
            st.session_state.create_work_effort = True
        
        if st.button("⚙️ CLI Commands", use_container_width=True):
            st.session_state.view_cli = True
        
        if st.button("📊 Empirica Dashboard", use_container_width=True):
            st.session_state.view_empirica = True
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Bottom: Recent Activity Feed
    st.markdown("---")
    st.subheader("📰 Town Chronicle - Recent Activity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Recent Beings**")
        if being_system:
            beings_path = project_path / "_hidden" / ".truth" / "beings"
            if beings_path.exists():
                beings = sorted([d.name for d in beings_path.iterdir() if d.is_dir()], reverse=True)[:3]
                for being_id in beings:
                    st.caption(f"👤 {being_id}")
    
    with col2:
        st.write("**Recent Work Efforts**")
        work_efforts_path = project_path / "_work_efforts"
        if work_efforts_path.exists():
            work_efforts = sorted([d.name for d in work_efforts_path.iterdir() if d.is_dir() and d.name.startswith("WE-")], reverse=True)[:3]
            for effort_id in work_efforts:
                st.caption(f"📋 {effort_id}")
