"""
Being System Integration for Streamlit UI.
"""

import streamlit as st
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
import json

from waft.being import BeingSystem, Being
from .utils import display_error, display_success, format_json, load_json_file


def validate_skills_json(json_str: str) -> Dict[str, Any]:
    """
    Validate and parse skills JSON safely.
    
    Validates:
    - JSON format is valid
    - Size limits (10KB max)
    - Structure (must be dict)
    - Keys are strings
    - Values are numbers between 0 and 100
    
    Args:
        json_str: JSON string to validate
        
    Returns:
        Validated skills dictionary
        
    Raises:
        ValueError: If validation fails
    """
    if not json_str or json_str.strip() == "":
        return {}
    
    # Size limit: 10KB
    MAX_SIZE = 10 * 1024
    if len(json_str) > MAX_SIZE:
        raise ValueError(f"JSON too large: {len(json_str)} bytes (max {MAX_SIZE})")
    
    # Parse JSON
    try:
        skills = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")
    
    # Validate structure: must be dict
    if not isinstance(skills, dict):
        raise ValueError("Skills must be a dictionary")
    
    # Validate keys and values
    for key, value in skills.items():
        # Keys must be strings
        if not isinstance(key, str):
            raise ValueError(f"Skill key must be a string: {key}")
        
        # Values must be numbers
        if not isinstance(value, (int, float)):
            raise ValueError(f"Skill value must be a number: {key}={value}")
        
        # Values must be between 0 and 100
        if value < 0 or value > 100:
            raise ValueError(f"Skill value must be between 0 and 100: {key}={value}")
    
    return skills


def render_being_system_page(being_system: Optional[BeingSystem], project_path: Path):
    """Render the Being System page."""
    st.markdown('<div class="main-header">👤 Being System</div>', unsafe_allow_html=True)
    
    if not being_system:
        st.error("Being System is not available. Check project configuration.")
        return
    
    # Being list
    st.subheader("Beings")
    
    beings = list_beings(project_path)
    
    if beings:
        # Being selector
        being_ids = [b['being_id'] for b in beings]
        selected_id = st.selectbox("Select Being", being_ids)
        
        if selected_id:
            selected_being = next(b for b in beings if b['being_id'] == selected_id)
            render_being_details(being_system, selected_being['being_id'])
    else:
        st.info("No beings found. Spawn a new being to get started.")
    
    st.markdown("---")
    
    # Spawn new being
    st.subheader("Spawn New Being")
    
    with st.form("spawn_being_form"):
        reality_id = st.text_input("Reality ID", value="streamlit_ui_reality")
        parent_being_id = st.text_input("Parent Being ID (optional)", value="")
        initial_skills_json = st.text_area("Initial Skills (JSON, optional)", value="{}")
        
        submitted = st.form_submit_button("Spawn Being")
        
        if submitted:
            try:
                # Validate and parse skills JSON
                try:
                    initial_skills = validate_skills_json(initial_skills_json) if initial_skills_json else {}
                except ValueError as e:
                    display_error(str(e), "Invalid Skills JSON")
                    return
                
                # Validate reality_id (basic sanitization)
                if not reality_id or not isinstance(reality_id, str):
                    display_error("Reality ID must be a non-empty string", "Validation Error")
                    return
                
                # Sanitize reality_id (alphanumeric, underscore, hyphen only)
                import re
                if not re.match(r'^[a-zA-Z0-9_-]+$', reality_id):
                    display_error("Reality ID contains invalid characters. Use only letters, numbers, underscores, and hyphens.", "Validation Error")
                    return
                
                # Validate parent_being_id if provided
                parent_id = None
                if parent_being_id and parent_being_id.strip():
                    parent_id = parent_being_id.strip()
                    # Basic format validation (should match being ID pattern)
                    if not re.match(r'^being_\d{8}_[a-z0-9]{8}$', parent_id):
                        display_error("Invalid parent Being ID format", "Validation Error")
                        return
                
                being = being_system.spawn_being(
                    reality_id=reality_id,
                    parent_being_id=parent_id,
                    initial_skills=initial_skills
                )
                
                display_success(f"Being spawned: {being.being_id}")
                st.rerun()
            except Exception as e:
                display_error(str(e), "Failed to spawn being")


def render_being_details(being_system: BeingSystem, being_id: str):
    """Render details for a specific being."""
    try:
        being = being_system._load_being(being_id)
        
        # Basic info
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Being ID", being.being_id)
            st.metric("Reality", being.reality_id)
            st.metric("State", being.state.value)
        
        with col2:
            st.metric("Lifetimes", being.lifetimes)
            st.metric("Fitness", f"{being.fitness:.2f}")
            st.metric("Stamina", f"{being.stamina:.1f}/{being.stamina_max:.1f}")
        
        with col3:
            st.metric("Will to Live", f"{being.will_to_live:.1f}")
            st.metric("Decision Fatigue", f"{being.decision_fatigue}/{being.decision_quota_max}")
            st.metric("Personality", being.personality_type)
        
        st.markdown("---")
        
        # Skills
        st.subheader("Skills")
        if being.skills:
            skills_df = st.dataframe(
                {skill: [level] for skill, level in being.skills.items()},
                use_container_width=True
            )
        else:
            st.info("No skills yet.")
        
        st.markdown("---")
        
        # Ancestral chain
        st.subheader("Ancestral Chain")
        st.write(" → ".join(being.ancestral_chain))
        
        st.markdown("---")
        
        # Chronicle
        st.subheader("Chronicle")
        chronicle_path = project_path / "_hidden" / ".truth" / "beings" / being_id / "chronicle.jsonl"
        if chronicle_path.exists():
            render_chronicle(chronicle_path)
        else:
            st.info("No chronicle entries yet.")
        
    except Exception as e:
        display_error(str(e), "Failed to load being")


def render_chronicle(chronicle_path: Path):
    """Render being chronicle entries."""
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
                severity = entry.get('severity', 'INFO')
                message = entry.get('message', '')
                
                st.text(f"[{timestamp}] {severity}: {message}")
        else:
            st.info("No chronicle entries.")
    except Exception as e:
        st.error(f"Error reading chronicle: {e}")


def list_beings(project_path: Path) -> List[Dict[str, Any]]:
    """List all beings in the project."""
    beings = []
    beings_path = project_path / "_hidden" / ".truth" / "beings"
    
    if not beings_path.exists():
        return beings
    
    for being_dir in beings_path.iterdir():
        if being_dir.is_dir():
            being_file = being_dir / "being.json"
            if being_file.exists():
                being_data = load_json_file(being_file)
                if being_data:
                    beings.append({
                        'being_id': being_data.get('being_id', being_dir.name),
                        'reality_id': being_data.get('reality_id', 'unknown'),
                        'state': being_data.get('state', 'unknown'),
                        'created_at': being_data.get('created_at', 'unknown')
                    })
    
    # Sort by created_at (most recent first)
    beings.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return beings


def render_recent_beings(being_system: Optional[BeingSystem]):
    """Render recent beings widget."""
    if not being_system:
        st.info("Being System not available")
        return
    
    beings = list_beings(being_system.project_path)
    
    if beings:
        for being in beings[:5]:  # Show 5 most recent
            st.write(f"**{being['being_id']}**")
            st.caption(f"Reality: {being['reality_id']} | State: {being['state']}")
    else:
        st.info("No beings yet")


def render_spawn_being_modal(being_system: Optional[BeingSystem]):
    """Render spawn being modal (placeholder for future modal implementation)."""
    if being_system:
        st.info("Use the Being System page to spawn new beings.")
