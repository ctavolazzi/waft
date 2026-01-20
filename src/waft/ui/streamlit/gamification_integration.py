"""
Gamification Integration for Streamlit UI.
"""

import streamlit as st

from waft.core.gamification import GamificationManager


def render_gamification_page(gamification_manager: GamificationManager | None):
    """Render the Gamification page."""
    st.markdown('<div class="main-header">🎮 Gamification</div>', unsafe_allow_html=True)

    if not gamification_manager:
        st.error("Gamification Manager is not available.")
        return

    # Character sheet
    st.subheader("Character Sheet")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Level", gamification_manager.level)

    with col2:
        st.metric("Integrity", f"{gamification_manager.integrity:.1f}%")

    with col3:
        st.metric("Insight", f"{gamification_manager.insight:.1f}")

    with col4:
        next_level_xp = gamification_manager.next_level_xp
        st.metric("Next Level XP", f"{next_level_xp:.0f}")

    st.markdown("---")

    # Level progress
    st.subheader("Level Progress")

    progress = gamification_manager.level_progress_pct
    st.progress(progress / 100.0)
    st.caption(f"{progress:.1f}% to next level")

    st.markdown("---")

    # Achievements
    st.subheader("Achievements")

    achievements = gamification_manager.achievements

    if achievements:
        for achievement in achievements:
            st.write(f"🏆 **{achievement.get('name', 'Unknown')}**")
            if achievement.get("description"):
                st.caption(achievement["description"])
    else:
        st.info("No achievements yet.")

    st.markdown("---")

    # History
    st.subheader("Recent History")

    history = gamification_manager.history

    if history:
        # Show last 10 entries
        for entry in history[-10:]:
            timestamp = entry.get("timestamp", "Unknown")
            event = entry.get("event", "Unknown")
            st.text(f"[{timestamp}] {event}")
    else:
        st.info("No history yet.")

    st.markdown("---")

    # Raw data (for debugging)
    with st.expander("Raw Data"):
        st.json(gamification_manager._data)
