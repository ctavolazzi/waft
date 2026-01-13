"""
TavernKeeper Integration for Streamlit UI.
"""

import streamlit as st
from pathlib import Path
from typing import Optional
import json

# TavernKeeper import - may not be available
try:
    from waft.core.tavern_keeper import TavernKeeper
except ImportError:
    TavernKeeper = None
from .utils import display_error, display_success


def render_tavern_page(tavern_keeper: Optional[TavernKeeper]):
    """Render the TavernKeeper page."""
    st.markdown('<div class="main-header">🍺 TavernKeeper</div>', unsafe_allow_html=True)
    
    if not tavern_keeper:
        st.error("TavernKeeper is not available.")
        return
    
    # Tavern status
    st.subheader("Tavern Status")
    
    # Get chronicle
    chronicle_path = tavern_keeper.project_path / "_pyrite" / ".waft" / "chronicle.jsonl"
    
    if chronicle_path.exists():
        st.subheader("Recent Chronicle Entries")
        render_chronicle(chronicle_path)
    else:
        st.info("No chronicle entries yet.")
    
    st.markdown("---")
    
    # Dice roll simulator
    st.subheader("Dice Roll Simulator")
    
    with st.form("dice_roll_form"):
        ability = st.selectbox("Ability", ["STR", "DEX", "CON", "INT", "WIS", "CHA"])
        modifier = st.number_input("Modifier", value=0, step=1)
        dc = st.number_input("Difficulty Class (DC)", value=10, step=1)
        
        submitted = st.form_submit_button("Roll Dice")
        
        if submitted:
            # Simulate dice roll (simplified)
            import random
            roll = random.randint(1, 20)
            total = roll + modifier
            
            # Classify result
            if roll == 20:
                classification = "Critical Success"
                color = "green"
            elif roll == 1:
                classification = "Critical Failure"
                color = "red"
            elif total >= dc + 5:
                classification = "Superior"
                color = "blue"
            elif total >= dc:
                classification = "Success"
                color = "green"
            else:
                classification = "Failure"
                color = "red"
            
            st.markdown(f"**Roll**: {roll} + {modifier} = **{total}** (DC {dc})")
            st.markdown(f"**Result**: <span style='color:{color}'>{classification}</span>", unsafe_allow_html=True)


def render_chronicle(chronicle_path: Path):
    """Render chronicle entries."""
    try:
        entries = []
        with open(chronicle_path, 'r') as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))
        
        if entries:
            # Show most recent entries
            st.write(f"**Total entries**: {len(entries)}")
            
            # Display recent entries
            recent_entries = entries[-10:]  # Last 10 entries
            for entry in reversed(recent_entries):
                timestamp = entry.get('timestamp', 'Unknown')
                event_type = entry.get('type', 'Unknown')
                message = entry.get('message', '')
                
                st.text(f"[{timestamp}] {event_type}: {message}")
        else:
            st.info("No chronicle entries.")
    except Exception as e:
        st.error(f"Error reading chronicle: {e}")
