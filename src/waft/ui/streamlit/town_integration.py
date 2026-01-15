"""
AI Town Integration for Streamlit UI.

Provides visualization and interaction for the AI Town system:
- Town overview with metrics
- 2D visualization of agent positions
- Active conversations viewer
- Agent details (personality, memories, relationships)
- Voting system interface
- Simulation controls
"""

import streamlit as st
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
import json
import pandas as pd

# Optional plotly for map visualization
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Import AI Town components
try:
    from waft.ai_town import TownWorld, TownAgent, TownVotingSystem
    from waft.ai_town.conversation import ConversationManager
    from waft.core.agent.state import AgentConfig
    TOWN_AVAILABLE = True
except ImportError as e:
    TOWN_AVAILABLE = False
    IMPORT_ERROR = str(e)


def render_town_page(project_path: Path):
    """Render the main AI Town page."""
    if not TOWN_AVAILABLE:
        st.error(f"AI Town system not available: {IMPORT_ERROR}")
        st.info("Please ensure all AI Town dependencies are installed.")
        return
    
    st.markdown('<div class="main-header">🏘️ AI Town</div>', unsafe_allow_html=True)
    
    # Initialize town in session state
    if 'town_world' not in st.session_state:
        st.session_state.town_world = None
        st.session_state.town_name = "WAFT AI Town"
        st.session_state.simulation_running = False
        st.session_state.simulation_paused = False
    
    # Sidebar controls
    with st.sidebar:
        st.header("🏘️ Town Controls")
        
        # Town creation/management
        if st.session_state.town_world is None:
            if st.button("🏗️ Create New Town", use_container_width=True):
                st.session_state.town_world = TownWorld(name=st.session_state.town_name)
                st.session_state.voting_system = TownVotingSystem(project_path=project_path)
                st.rerun()
        else:
            st.success("✅ Town Active")
            if st.button("🔄 Reset Town", use_container_width=True):
                st.session_state.town_world = None
                st.session_state.simulation_running = False
                st.rerun()
        
        st.markdown("---")
        
        # Agent management
        if st.session_state.town_world:
            st.subheader("👥 Agents")
            st.metric("Total Agents", len(st.session_state.town_world.agents))
            
            if st.button("➕ Add Agent", use_container_width=True):
                st.session_state.show_add_agent = True
            
            # List agents
            if st.session_state.town_world.agents:
                agent_names = [agent.name for agent in st.session_state.town_world.agents.values()]
                selected_agent = st.selectbox("View Agent", ["All"] + agent_names)
                if selected_agent != "All":
                    st.session_state.selected_agent = selected_agent
        
        st.markdown("---")
        
        # Simulation controls
        if st.session_state.town_world:
            st.subheader("⏱️ Simulation")
            
            if st.session_state.simulation_running:
                if st.button("⏸️ Pause", use_container_width=True):
                    st.session_state.simulation_paused = not st.session_state.simulation_paused
                    st.rerun()
                
                if st.button("⏹️ Stop", use_container_width=True):
                    st.session_state.simulation_running = False
                    st.session_state.simulation_paused = False
                    st.rerun()
            else:
                ticks = st.number_input("Ticks to Run", min_value=1, max_value=1000, value=10)
                tick_delay = st.slider("Tick Delay (seconds)", 0.0, 2.0, 0.1, 0.1)
                
                if st.button("▶️ Start Simulation", use_container_width=True):
                    st.session_state.simulation_running = True
                    st.session_state.simulation_ticks = ticks
                    st.session_state.simulation_delay = tick_delay
                    st.session_state.simulation_ticks_run = 0
                    st.rerun()
    
    # Main content
    if st.session_state.town_world is None:
        render_town_creation_page()
    else:
        # Tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview",
            "🗺️ Map",
            "💬 Conversations",
            "👤 Agents",
            "🗳️ Voting"
        ])
        
        with tab1:
            render_town_overview()
        
        with tab2:
            render_town_map()
        
        with tab3:
            render_conversations()
        
        with tab4:
            render_agents_view()
        
        with tab5:
            render_voting_interface()
        
        # Handle add agent modal
        if st.session_state.get('show_add_agent'):
            render_add_agent_modal()
        
        # Run simulation if requested
        if st.session_state.get('simulation_running') and not st.session_state.get('simulation_paused'):
            run_simulation_step()
    
    # Auto-refresh
    if st.session_state.town_world and st.session_state.get('auto_refresh', False):
        import time
        time.sleep(1)
        st.rerun()


def render_town_creation_page():
    """Render page for creating a new town."""
    st.info("👋 Welcome to AI Town! Create a new town to get started.")
    
    st.subheader("Create New Town")
    
    town_name = st.text_input("Town Name", value="WAFT AI Town")
    
    if st.button("🏗️ Create Town", type="primary"):
        st.session_state.town_world = TownWorld(name=town_name)
        st.session_state.town_name = town_name
        st.session_state.voting_system = TownVotingSystem(project_path=Path.cwd())
        st.rerun()
    
    st.markdown("---")
    st.subheader("About AI Town")
    st.markdown("""
    AI Town is a virtual world where AI agents (Beings) live, chat, and socialize.
    
    **Features:**
    - 👥 Multiple agents with unique personalities
    - 💬 Agent-to-agent conversations
    - 🧠 Memory system for agents
    - 🗳️ Democratic voting system
    - 📊 Real-time visualization
    """)


def render_town_overview():
    """Render town overview with metrics."""
    town = st.session_state.town_world
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Agents", len(town.agents))
    
    with col2:
        active_convos = len([
            c for c in town.conversation_manager.conversations.values()
            if c.is_active()
        ])
        st.metric("Active Conversations", active_convos)
    
    with col3:
        st.metric("Total Conversations", len(town.conversation_manager.conversations))
    
    with col4:
        st.metric("Simulation Ticks", town.tick_count)
    
    st.markdown("---")
    
    # Town state summary
    state = town.get_state_summary()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Town Statistics")
        st.json({
            "Name": state["name"],
            "Tick Count": state["tick_count"],
            "Agent Count": state["agent_count"],
            "Active Conversations": state["active_conversations"],
            "Total Conversations": state["total_conversations"],
        })
    
    with col2:
        st.subheader("👥 Agent List")
        if town.agents:
            agent_data = []
            for agent in town.agents.values():
                agent_data.append({
                    "Name": agent.name,
                    "Position": f"({agent.position['x']:.1f}, {agent.position['y']:.1f})",
                    "In Conversation": "Yes" if agent.current_conversation else "No",
                    "Memories": len(agent.memories),
                })
            st.dataframe(pd.DataFrame(agent_data), use_container_width=True)
        else:
            st.info("No agents in town yet. Add agents using the sidebar.")
    
    # Auto-refresh toggle
    st.markdown("---")
    auto_refresh = st.checkbox("🔄 Auto-refresh (1 second)", value=st.session_state.get('auto_refresh', False))
    st.session_state.auto_refresh = auto_refresh


def render_town_map():
    """Render 2D visualization of agent positions."""
    town = st.session_state.town_world
    
    if not town.agents:
        st.info("No agents in town. Add agents to see the map.")
        return
    
    if PLOTLY_AVAILABLE:
        # Use plotly for interactive map
        # Prepare agent data
        agent_positions = []
        agent_names = []
        agent_colors = []
        in_conversation = []
        
        # Color map for conversations
        conversation_colors = {}
        color_palette = px.colors.qualitative.Set3
        
        for agent in town.agents.values():
            agent_positions.append([agent.position['x'], agent.position['y']])
            agent_names.append(agent.name)
            
            # Color by conversation status
            if agent.current_conversation:
                conv_id = agent.current_conversation
                if conv_id not in conversation_colors:
                    conversation_colors[conv_id] = color_palette[len(conversation_colors) % len(color_palette)]
                agent_colors.append(conversation_colors[conv_id])
                in_conversation.append(True)
            else:
                agent_colors.append('#888888')  # Gray for agents not in conversation
                in_conversation.append(False)
        
        # Create scatter plot
        fig = go.Figure()
        
        # Plot agents
        for i, (pos, name, color, in_conv) in enumerate(zip(agent_positions, agent_names, agent_colors, in_conversation)):
            fig.add_trace(go.Scatter(
                x=[pos[0]],
                y=[pos[1]],
                mode='markers+text',
                marker=dict(
                    size=20,
                    color=color,
                    line=dict(width=2, color='white'),
                    symbol='circle' if not in_conv else 'star'
                ),
                text=name,
                textposition="top center",
                name=name,
                hovertemplate=f"<b>{name}</b><br>" +
                             f"Position: ({pos[0]:.1f}, {pos[1]:.1f})<br>" +
                             f"In Conversation: {'Yes' if in_conv else 'No'}<extra></extra>"
            ))
        
        # Draw lines between agents in conversation
        for conv_id, conversation in town.conversation_manager.conversations.items():
            if conversation.is_active() and len(conversation.participants) == 2:
                p1_id, p2_id = conversation.participants
                agent1 = town.agents.get(p1_id)
                agent2 = town.agents.get(p2_id)
                
                if agent1 and agent2:
                    fig.add_trace(go.Scatter(
                        x=[agent1.position['x'], agent2.position['x']],
                        y=[agent1.position['y'], agent2.position['y']],
                        mode='lines',
                        line=dict(color=conversation_colors.get(conv_id, '#888888'), width=2, dash='dash'),
                        showlegend=False,
                        hoverinfo='skip'
                    ))
        
        # Update layout
        fig.update_layout(
            title="🗺️ AI Town Map",
            xaxis_title="X Position",
            yaxis_title="Y Position",
            xaxis=dict(range=[0, 100]),
            yaxis=dict(range=[0, 100]),
            height=600,
            showlegend=False,
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Legend
        st.caption("💡 Stars indicate agents in conversation. Lines connect conversing agents.")
    else:
        # Fallback to simple table view
        st.info("Plotly not available. Install with: `pip install plotly` for interactive map visualization.")
        
        # Show agent positions in table
        agent_data = []
        for agent in town.agents.values():
            agent_data.append({
                "Name": agent.name,
                "X": f"{agent.position['x']:.1f}",
                "Y": f"{agent.position['y']:.1f}",
                "In Conversation": "Yes" if agent.current_conversation else "No",
            })
        
        st.dataframe(pd.DataFrame(agent_data), use_container_width=True)


def render_conversations():
    """Render active and past conversations."""
    town = st.session_state.town_world
    
    # Active conversations
    st.subheader("💬 Active Conversations")
    
    active_conversations = [
        c for c in town.conversation_manager.conversations.values()
        if c.is_active()
    ]
    
    if active_conversations:
        for conv in active_conversations:
            with st.expander(f"Conversation {conv.conversation_id[:8]}... ({len(conv.messages)} messages)"):
                # Participants
                participant_names = [
                    town.agents[p].name if p in town.agents else p
                    for p in conv.participants
                ]
                st.write(f"**Participants**: {', '.join(participant_names)}")
                
                # Messages
                st.write("**Messages:**")
                for msg in conv.messages[-10:]:  # Show last 10 messages
                    st.markdown(f"**{msg.agent_name}**: {msg.content}")
                
                # Duration
                duration = conv.get_duration()
                st.caption(f"Duration: {duration:.1f} seconds")
    else:
        st.info("No active conversations.")
    
    st.markdown("---")
    
    # Past conversations
    st.subheader("📜 Past Conversations")
    
    past_conversations = [
        c for c in town.conversation_manager.conversations.values()
        if not c.is_active()
    ]
    
    if past_conversations:
        # Show most recent first
        past_conversations.sort(key=lambda c: c.ended_at or 0, reverse=True)
        
        for conv in past_conversations[:10]:  # Show last 10
            with st.expander(f"Conversation {conv.conversation_id[:8]}... (Ended)"):
                participant_names = [
                    town.agents[p].name if p in town.agents else p
                    for p in conv.participants
                ]
                st.write(f"**Participants**: {', '.join(participant_names)}")
                st.write(f"**Messages**: {len(conv.messages)}")
                if conv.summary:
                    st.write(f"**Summary**: {conv.summary}")
    else:
        st.info("No past conversations.")


def render_agents_view():
    """Render detailed agent view."""
    town = st.session_state.town_world
    
    if not town.agents:
        st.info("No agents in town. Add agents using the sidebar.")
        return
    
    # Agent selector
    agent_names = [agent.name for agent in town.agents.values()]
    selected_name = st.selectbox("Select Agent", agent_names)
    
    if selected_name:
        # Find agent
        agent = None
        for a in town.agents.values():
            if a.name == selected_name:
                agent = a
                break
        
        if agent:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(f"👤 {agent.name}")
                
                # Basic info
                st.write(f"**Agent ID**: `{agent.state.agent_id[:8]}...`")
                st.write(f"**Position**: ({agent.position['x']:.1f}, {agent.position['y']:.1f})")
                st.write(f"**In Conversation**: {'Yes' if agent.current_conversation else 'No'}")
                
                # Personality
                st.markdown("---")
                st.subheader("🧠 Personality")
                personality_df = pd.DataFrame({
                    "Trait": ["Curiosity", "Sociability", "Energy"],
                    "Value": [
                        agent.personality.get("curiosity", 0),
                        agent.personality.get("sociability", 0),
                        agent.personality.get("energy", 0),
                    ]
                })
                st.bar_chart(personality_df.set_index("Trait"))
                
                # Relationships
                if agent.relationships:
                    st.markdown("---")
                    st.subheader("🤝 Relationships")
                    for other_id, score in agent.relationships.items():
                        other_agent = town.agents.get(other_id)
                        other_name = other_agent.name if other_agent else other_id[:8]
                        st.progress(score, text=f"{other_name}: {score:.2f}")
            
            with col2:
                # Memories
                st.subheader("🧠 Memories")
                if agent.memories:
                    for memory in agent.memories[-10:]:  # Show last 10
                        with st.expander(f"Memory {memory.get('conversation_id', 'unknown')[:8]}..."):
                            st.write(f"**Summary**: {memory.get('summary', 'No summary')}")
                            st.caption(f"Timestamp: {memory.get('timestamp', 'Unknown')}")
                else:
                    st.info("No memories yet.")
                
                # Current activity
                if agent.current_activity:
                    st.markdown("---")
                    st.subheader("🎯 Current Activity")
                    st.write(agent.current_activity)


def render_voting_interface():
    """Render voting system interface."""
    if 'voting_system' not in st.session_state:
        st.session_state.voting_system = TownVotingSystem(project_path=Path.cwd())
    
    voting_system = st.session_state.voting_system
    town = st.session_state.town_world
    
    st.subheader("🗳️ Town Voting System")
    
    # Voting stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Voting Records", "N/A")  # TODO: Get from voting system
    
    with col2:
        st.metric("Active Decisions", "N/A")
    
    with col3:
        st.metric("Town Beings", len(town.agents))
    
    st.markdown("---")
    
    # Create new decision
    st.subheader("📝 Create New Decision")
    
    with st.form("create_decision"):
        decision_title = st.text_input("Decision Title")
        decision_description = st.text_area("Description")
        decision_type = st.selectbox("Vote Type", ["binary", "multiple_choice", "ranked"])
        
        options = []
        if decision_type == "binary":
            options = ["Yes", "No"]
        elif decision_type == "multiple_choice":
            option_text = st.text_input("Options (comma-separated)", "Option A, Option B, Option C")
            options = [opt.strip() for opt in option_text.split(",")]
        
        submitted = st.form_submit_button("Create Decision")
        
        if submitted and decision_title:
            st.success(f"Decision '{decision_title}' created!")
            # TODO: Actually create decision using voting system
    
    st.markdown("---")
    
    # Recent votes
    st.subheader("📊 Recent Votes")
    st.info("Voting history will be displayed here.")


def render_add_agent_modal():
    """Render modal for adding a new agent."""
    st.subheader("➕ Add New Agent")
    
    with st.form("add_agent"):
        agent_name = st.text_input("Agent Name", value=f"Agent_{len(st.session_state.town_world.agents) + 1}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            curiosity = st.slider("Curiosity", 0.0, 1.0, 0.5, 0.1)
        with col2:
            sociability = st.slider("Sociability", 0.0, 1.0, 0.5, 0.1)
        with col3:
            energy = st.slider("Energy", 0.0, 1.0, 0.7, 0.1)
        
        col1, col2 = st.columns(2)
        with col1:
            pos_x = st.slider("Initial X Position", 0.0, 100.0, 50.0, 1.0)
        with col2:
            pos_y = st.slider("Initial Y Position", 0.0, 100.0, 50.0, 1.0)
        
        submitted = st.form_submit_button("Add Agent")
        cancel = st.form_submit_button("Cancel")
        
        if cancel:
            st.session_state.show_add_agent = False
            st.rerun()
        
        if submitted and agent_name:
            try:
                # Create agent config
                config = AgentConfig(
                    role="Town Resident",
                    goal="Live, chat, and socialize in the town",
                    tools=[],
                )
                
                # Create agent
                agent = TownAgent(
                    config=config,
                    project_path=Path.cwd(),
                    name=agent_name,
                    personality={
                        "curiosity": curiosity,
                        "sociability": sociability,
                        "energy": energy,
                    },
                    position={"x": pos_x, "y": pos_y}
                )
                
                # Add to town
                st.session_state.town_world.add_agent(agent)
                st.session_state.show_add_agent = False
                st.success(f"Agent '{agent_name}' added to town!")
                st.rerun()
            except Exception as e:
                st.error(f"Error adding agent: {e}")


def run_simulation_step():
    """Run one step of the simulation."""
    town = st.session_state.town_world
    
    if not town.agents:
        st.session_state.simulation_running = False
        return
    
    # Run a single tick (Streamlit-friendly approach)
    try:
        # Create new event loop for this tick
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(town.tick())
        loop.close()
        
        # Update tick counter
        ticks_run = st.session_state.get('simulation_ticks_run', 0) + 1
        st.session_state.simulation_ticks_run = ticks_run
        
        # Check if we've run all requested ticks
        total_ticks = st.session_state.get('simulation_ticks', 1)
        if ticks_run >= total_ticks:
            st.session_state.simulation_running = False
            st.session_state.simulation_ticks_run = 0
            st.success(f"Simulation complete! Ran {total_ticks} ticks.")
        
    except Exception as e:
        st.error(f"Simulation error: {e}")
        st.session_state.simulation_running = False
    
    # Auto-rerun if still running
    if st.session_state.get('simulation_running') and not st.session_state.get('simulation_paused'):
        import time
        delay = st.session_state.get('simulation_delay', 0.1)
        time.sleep(delay)
        st.rerun()
