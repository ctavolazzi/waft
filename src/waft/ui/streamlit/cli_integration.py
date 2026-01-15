"""
CLI Commands Integration for Streamlit UI.
"""

import streamlit as st
from pathlib import Path
from typing import Dict, Any

from .utils import run_cli_command, display_error, display_success, format_json


def render_cli_commands_page(project_path: Path):
    """Render the CLI Commands page."""
    st.markdown('<div class="main-header">⚙️ CLI Commands</div>', unsafe_allow_html=True)
    
    # Command categories
    st.subheader("Command Categories")
    
    category = st.radio(
        "Select Category",
        ["Project Management", "Evolution", "Empirica", "Gamification", "Custom Command"]
    )
    
    st.markdown("---")
    
    if category == "Project Management":
        render_project_management_commands(project_path)
    elif category == "Evolution":
        render_evolution_commands(project_path)
    elif category == "Empirica":
        render_empirica_commands(project_path)
    elif category == "Gamification":
        render_gamification_commands(project_path)
    elif category == "Custom Command":
        render_custom_command(project_path)


def render_project_management_commands(project_path: Path):
    """Render project management commands."""
    st.subheader("Project Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Verify Project", use_container_width=True):
            result = run_cli_command("waft verify", project_path)
            display_command_result(result)
        
        if st.button("Project Info", use_container_width=True):
            result = run_cli_command("waft info", project_path)
            display_command_result(result)
    
    with col2:
        if st.button("Sync Dependencies", use_container_width=True):
            result = run_cli_command("waft sync", project_path)
            display_command_result(result)
        
        if st.button("Status", use_container_width=True):
            result = run_cli_command("waft status", project_path)
            display_command_result(result)


def render_evolution_commands(project_path: Path):
    """Render evolution commands."""
    st.subheader("Evolution")
    
    st.info("Evolution commands require additional parameters. Use the CLI directly.")
    
    st.code("waft evolve --agent <name>")
    st.code("waft spawn --agent <name> --mutation <file>")
    st.code("waft eval --agent <name>")


def render_empirica_commands(project_path: Path):
    """Render Empirica commands."""
    st.subheader("Empirica")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Session Status", use_container_width=True):
            result = run_cli_command("waft session status", project_path)
            display_command_result(result)
        
        if st.button("Assess State", use_container_width=True):
            result = run_cli_command("waft assess", project_path)
            display_command_result(result)
    
    with col2:
        if st.button("Check Gate", use_container_width=True):
            result = run_cli_command("waft check", project_path)
            display_command_result(result)


def render_gamification_commands(project_path: Path):
    """Render gamification commands."""
    st.subheader("Gamification")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Dashboard", use_container_width=True):
            result = run_cli_command("waft dashboard", project_path)
            display_command_result(result)
        
        if st.button("Stats", use_container_width=True):
            result = run_cli_command("waft stats", project_path)
            display_command_result(result)
    
    with col2:
        if st.button("Character Sheet", use_container_width=True):
            result = run_cli_command("waft character", project_path)
            display_command_result(result)
        
        if st.button("Chronicle", use_container_width=True):
            result = run_cli_command("waft chronicle", project_path)
            display_command_result(result)


def render_custom_command(project_path: Path):
    """Render custom command input."""
    st.subheader("Custom Command")
    
    command = st.text_input("Enter WAFT command", placeholder="waft verify")
    
    if st.button("Execute Command"):
        if command:
            if command.startswith("waft "):
                result = run_cli_command(command, project_path)
                display_command_result(result)
            else:
                st.warning("Commands must start with 'waft '")
        else:
            st.warning("Please enter a command")


def display_command_result(result: Dict[str, Any]):
    """Display command execution result."""
    if result['success']:
        if result['output']:
            st.success("Command executed successfully")
            st.code(result['output'], language='text')
        else:
            st.success("Command executed successfully (no output)")
    else:
        st.error("Command failed")
        if result['error']:
            st.code(result['error'], language='text')
        if result['output']:
            st.code(result['output'], language='text')
