"""
Empirica Integration for Streamlit UI.
"""

import streamlit as st
from pathlib import Path
from typing import Optional, Dict, Any
import json

from waft.core.empirica import EmpiricaManager
from .utils import display_error, display_success, format_json


def render_empirica_page(empirica_manager: Optional[EmpiricaManager], project_path: Path):
    """Render the Empirica page."""
    st.markdown('<div class="main-header">📊 Empirica Dashboard</div>', unsafe_allow_html=True)
    
    if not empirica_manager:
        st.error("Empirica Manager is not available.")
        return
    
    # Status
    st.subheader("Status")
    
    is_initialized = empirica_manager.is_initialized()
    
    col1, col2 = st.columns(2)
    
    with col1:
        status = "✅ Initialized" if is_initialized else "⚠️ Not Initialized"
        st.metric("Empirica Status", status)
    
    with col2:
        if not is_initialized:
            if st.button("Initialize Empirica"):
                try:
                    empirica_manager.initialize()
                    display_success("Empirica initialized successfully")
                    st.rerun()
                except Exception as e:
                    display_error(str(e), "Failed to initialize Empirica")
    
    if not is_initialized:
        st.info("Initialize Empirica to start tracking epistemic state.")
        return
    
    st.markdown("---")
    
    # Session management
    st.subheader("Sessions")
    
    # Create new session
    with st.form("create_session_form"):
        ai_id = st.text_input("AI ID", value="waft")
        session_type = st.selectbox("Session Type", ["development", "research", "debugging", "other"])
        
        submitted = st.form_submit_button("Create Session")
        
        if submitted:
            try:
                session_id = empirica_manager.create_session(ai_id=ai_id, session_type=session_type)
                display_success(f"Session created: {session_id}")
                st.session_state.current_session_id = session_id
            except Exception as e:
                display_error(str(e), "Failed to create session")
    
    st.markdown("---")
    
    # Epistemic vectors
    st.subheader("Epistemic Vectors")
    st.info("Use the CLI or API to submit preflight/postflight assessments.")
    
    # Project bootstrap
    st.markdown("---")
    st.subheader("Project Bootstrap")
    
    if st.button("Load Project Context"):
        try:
            context = empirica_manager.project_bootstrap()
            if context:
                st.json(context)
                display_success("Project context loaded")
            else:
                st.info("No project context available.")
        except Exception as e:
            display_error(str(e), "Failed to load project context")
    
    st.markdown("---")
    
    # Findings and Unknowns
    st.subheader("Findings & Unknowns")
    st.info("Use the CLI to log findings and unknowns:")
    st.code("waft finding log 'Your finding' --impact 0.7")
    st.code("waft unknown log 'Your unknown'")


def render_epistemic_dashboard(empirica_manager: Optional[EmpiricaManager]):
    """Render epistemic dashboard widget."""
    if not empirica_manager or not empirica_manager.is_initialized():
        st.info("Empirica not initialized")
        return
    
    st.info("Epistemic dashboard - use CLI for detailed views")
