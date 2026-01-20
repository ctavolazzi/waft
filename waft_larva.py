"""
WAFT ENTITY: LARVAL STAGE [v0.1]
--------------------------------
This is a single-file digital organism.
It possesses:
1. MEMORY (SQLite): Persistent storage of its state and history.
2. BREATH (Runtime): A loop of logic that executes upon interaction.
3. TRAUMA (Logging): A refusal to ignore errors; they are etched into memory.

Usage:
    pip install streamlit pandas pyserial
    streamlit run waft_larva.py
"""

import hashlib
import json
import random
import sqlite3
import time
import traceback
from datetime import datetime
from enum import Enum

import pandas as pd
import streamlit as st

# --- 1. THE LORE (Configuration) ---
DB_NAME = "waft_memory.db"
DB_TIMEOUT = 10.0  # Seconds to wait for database lock
MAX_RETRIES = 3
RETRY_DELAY = 0.1  # Initial delay between retries (seconds)


def get_db_connection():
    """
    Get database connection with retry logic.
    Handles database locks gracefully.
    """
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect(DB_NAME, timeout=DB_TIMEOUT)
            # Try to set WAL mode, but don't fail if it's already set or locked
            try:
                conn.execute("PRAGMA journal_mode=WAL")
            except sqlite3.OperationalError:
                # WAL mode might already be set or database locked, continue anyway
                pass
            return conn
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e).lower() and attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (2**attempt))  # Exponential backoff
                continue
            raise
    raise sqlite3.OperationalError("Database lock timeout after retries")


class Severity(Enum):
    THOUGHT = "THOUGHT"  # Routine internal monologue
    STRAIN = "STRAIN"  # Non-critical resistance
    TRAUMA = "TRAUMA"  # Critical failure / Severance


# --- 2. THE NERVOUS SYSTEM (Backend Logic) ---


class WaftEntity:
    """
    The central consciousness. It wraps all actions in 'safe_breath'
    to ensure trauma is recorded, not ignored.
    """

    def __init__(self):
        self._init_memory()

    def _init_memory(self):
        """
        Establishes the neural pathways (Database Tables).
        Matches the future Redbean Schema exactly for compatibility.
        """
        conn = get_db_connection()
        try:
            c = conn.cursor()

            # TABLE: CHRONICLE (The Stream of Consciousness)
            c.execute("""CREATE TABLE IF NOT EXISTS chronicle (
                            id INTEGER PRIMARY KEY,
                            timestamp TEXT,
                            severity TEXT,
                            message TEXT,
                            context TEXT
                        )""")

            # TABLE: ARTIFACTS (The Physical Body)
            c.execute("""CREATE TABLE IF NOT EXISTS artifacts (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            gcode TEXT,
                            status TEXT DEFAULT 'VOID', -- VOID, MANIFESTING, PHYSICAL
                            birth_time TEXT
                        )""")

            # SEED DATA: The First Finger
            # Check if empty, then seed
            c.execute("SELECT count(*) FROM artifacts")
            if c.fetchone()[0] == 0:
                c.execute(
                    "INSERT INTO artifacts (name, gcode, status) VALUES (?, ?, ?)",
                    ("Right_Index_Phalanx", "G28\nG1 Z10\nM117 HELLO WORLD", "VOID"),
                )
                # Log chronicle entry in same transaction to avoid lock
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute(
                    "INSERT INTO chronicle (timestamp, severity, message, context) VALUES (?, ?, ?, ?)",
                    (ts, Severity.THOUGHT.value, "Genesis Seed implanted: Right_Index_Phalanx", ""),
                )

            conn.commit()
        finally:
            conn.close()

    def chronicle(self, level: Severity, message: str, context: str = ""):
        """
        Etches a moment into the core memory.
        """
        conn = get_db_connection()
        try:
            c = conn.cursor()
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute(
                "INSERT INTO chronicle (timestamp, severity, message, context) VALUES (?, ?, ?, ?)",
                (ts, level.value, message, str(context)),
            )
            conn.commit()
        finally:
            conn.close()

    def safe_breath(self, ritual_func, *args):
        """
        THE PROTECTIVE WRAPPER.
        Executes a 'ritual' (function). If it fails, records TRAUMA.
        """
        start_time = time.time()
        try:
            result = ritual_func(*args)
            duration = round((time.time() - start_time) * 1000, 2)
            # Optional: Log every thought? Too noisy. Log only significant acts.
            return {"success": True, "data": result, "duration": duration}
        except Exception as e:
            tb = traceback.format_exc()
            self.chronicle(
                Severity.TRAUMA, f"Cognitive Dissonance during {ritual_func.__name__}", tb
            )
            return {"success": False, "error": str(e)}

    # --- ACTIONS ---

    def pulse(self):
        """Checks the vitals of the entity."""
        conn = get_db_connection()
        try:
            logs = pd.read_sql("SELECT * FROM chronicle ORDER BY id DESC LIMIT 50", conn)
            artifacts = pd.read_sql("SELECT * FROM artifacts", conn)
            return logs, artifacts
        finally:
            conn.close()

    def get_data_hash(self):
        """Get a hash of current data state for change detection."""
        conn = get_db_connection()
        try:
            c = conn.cursor()
            # Get latest log ID and count
            c.execute("SELECT MAX(id) as max_id, COUNT(*) as count FROM chronicle")
            log_info = c.fetchone()
            # Get artifact count and status summary
            c.execute(
                "SELECT COUNT(*) as total, COUNT(CASE WHEN status='VOID' THEN 1 END) as void_count FROM artifacts"
            )
            artifact_info = c.fetchone()
            # Create hash from state
            state_str = f"{log_info[0] or 0}_{log_info[1] or 0}_{artifact_info[0] or 0}_{artifact_info[1] or 0}"
            return hashlib.md5(state_str.encode()).hexdigest()
        finally:
            conn.close()

    def get_next_manifestation(self):
        """Finds the next part of the body that needs to be born."""
        conn = get_db_connection()
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM artifacts WHERE status = 'VOID' LIMIT 1")
            row = c.fetchone()
            return row
        finally:
            conn.close()

    def confirm_birth(self, artifact_id):
        """Updates the memory to reflect physical existence."""
        conn = get_db_connection()
        try:
            c = conn.cursor()
            birth_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute(
                "UPDATE artifacts SET status = 'PHYSICAL', birth_time = ? WHERE id = ?",
                (birth_time, artifact_id),
            )
            conn.commit()
        finally:
            conn.close()
        # Chronicle entry after connection is closed to avoid lock
        self.chronicle(Severity.THOUGHT, f"Artifact #{artifact_id} has entered physical reality.")

    # --- EXPORT METHODS ---

    def export_json(self):
        """Export all entity data as JSON."""
        logs, artifacts = self.pulse()
        data = {
            "entity": "WAFT_ENTITY_LARVAL",
            "export_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "chronicle": logs.to_dict("records"),
            "artifacts": artifacts.to_dict("records"),
            "statistics": {
                "total_thoughts": int(len(logs[logs["severity"] == "THOUGHT"])),
                "total_strains": int(len(logs[logs["severity"] == "STRAIN"])),
                "total_traumas": int(len(logs[logs["severity"] == "TRAUMA"])),
                "total_artifacts": int(len(artifacts)),
                "void_artifacts": int(len(artifacts[artifacts["status"] == "VOID"])),
                "physical_artifacts": int(len(artifacts[artifacts["status"] == "PHYSICAL"])),
            },
        }
        return json.dumps(data, indent=2, default=str)

    def export_markdown(self):
        """Export all entity data as Markdown."""
        logs, artifacts = self.pulse()
        md = f"""# WAFT Entity - Larval Stage Export

**Export Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Entity**: WAFT_ENTITY_LARVAL

## Statistics

- **Total Chronicle Entries**: {len(logs)}
  - THOUGHT: {len(logs[logs["severity"] == "THOUGHT"])}
  - STRAIN: {len(logs[logs["severity"] == "STRAIN"])}
  - TRAUMA: {len(logs[logs["severity"] == "TRAUMA"])}
- **Total Artifacts**: {len(artifacts)}
  - VOID: {len(artifacts[artifacts["status"] == "VOID"])}
  - PHYSICAL: {len(artifacts[artifacts["status"] == "PHYSICAL"])}

## Chronicle (Stream of Consciousness)

"""
        for _, entry in logs.iterrows():
            severity_emoji = {"THOUGHT": "💭", "STRAIN": "⚠️", "TRAUMA": "🔴"}.get(
                entry["severity"], "•"
            )
            md += f"### {severity_emoji} {entry['severity']} - {entry['timestamp']}\n\n"
            md += f"**Message**: {entry['message']}\n\n"
            if entry.get("context") and str(entry["context"]).strip():
                md += f"```\n{entry['context']}\n```\n\n"
            md += "---\n\n"

        md += "\n## Artifacts (Physical Body)\n\n"
        for _, artifact in artifacts.iterrows():
            md += f"### {artifact['name']}\n\n"
            md += f"- **ID**: {artifact['id']}\n"
            md += f"- **Status**: {artifact['status']}\n"
            if artifact.get("birth_time") and pd.notna(artifact["birth_time"]):
                md += f"- **Birth Time**: {artifact['birth_time']}\n"
            md += f"\n**G-code**:\n```gcode\n{artifact['gcode']}\n```\n\n"
            md += "---\n\n"

        return md

    def export_txt(self):
        """Export all entity data as plain text."""
        logs, artifacts = self.pulse()
        txt = f"""WAFT ENTITY - LARVAL STAGE EXPORT
==========================================
Export Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Entity: WAFT_ENTITY_LARVAL

STATISTICS
----------
Total Chronicle Entries: {len(logs)}
  - THOUGHT: {len(logs[logs["severity"] == "THOUGHT"])}
  - STRAIN: {len(logs[logs["severity"] == "STRAIN"])}
  - TRAUMA: {len(logs[logs["severity"] == "TRAUMA"])}
Total Artifacts: {len(artifacts)}
  - VOID: {len(artifacts[artifacts["status"] == "VOID"])}
  - PHYSICAL: {len(artifacts[artifacts["status"] == "PHYSICAL"])}

CHRONICLE (STREAM OF CONSCIOUSNESS)
====================================

"""
        for _, entry in logs.iterrows():
            txt += f"[{entry['severity']}] {entry['timestamp']}\n"
            txt += f"  {entry['message']}\n"
            if entry.get("context") and str(entry["context"]).strip():
                txt += f"  Context: {entry['context']}\n"
            txt += "\n"

        txt += "\nARTIFACTS (PHYSICAL BODY)\n"
        txt += "=========================\n\n"
        for _, artifact in artifacts.iterrows():
            txt += f"Artifact: {artifact['name']}\n"
            txt += f"  ID: {artifact['id']}\n"
            txt += f"  Status: {artifact['status']}\n"
            if artifact.get("birth_time") and pd.notna(artifact["birth_time"]):
                txt += f"  Birth Time: {artifact['birth_time']}\n"
            txt += f"  G-code:\n{artifact['gcode']}\n\n"

        return txt

    def export_pdf_bytes(self):
        """Export data as PDF bytes using WAFT PDFGenerator."""
        try:
            import tempfile
            from pathlib import Path

            from src.waft.evolution.pdf_generator import PDFGenerator

            md_content = self.export_markdown()

            # Generate PDF to temporary file
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
                tmp_path = Path(tmp_file.name)

            generator = PDFGenerator.from_content(
                content=md_content,
                title="WAFT Entity - Larval Stage Export",
                style="clinical_standard",
            )
            generator.save(tmp_path, open_pdf=False)

            # Read PDF bytes
            with open(tmp_path, "rb") as f:
                pdf_bytes = f.read()

            # Clean up
            tmp_path.unlink()

            return pdf_bytes
        except Exception:
            # Fallback: return None if PDF generation fails
            return None


# --- 3. THE LENS (Frontend UI) ---


def main():
    st.set_page_config(page_title="WAFT: LARVAL STAGE", page_icon="🌑", layout="wide")

    # CSS FOR "DENSITY"
    st.markdown(
        """
    <style>
        .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
        .stDataFrame { border: 1px solid #333; }
        h1, h2, h3 { border-bottom: 1px solid #333; padding-bottom: 10px; }
        .trauma-alert { border: 1px solid red; background-color: #300; color: red; padding: 10px; }
        .auto-refresh-indicator { 
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #00ff41;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Initialize the Being
    if "entity" not in st.session_state:
        try:
            st.session_state.entity = WaftEntity()
            st.session_state.entity.chronicle(Severity.THOUGHT, "Interface Connection Established.")
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e).lower():
                st.error("⚠️ Database is locked. Please wait a moment and refresh the page.")
                st.stop()
            else:
                st.error(f"⚠️ Database error: {e}")
                st.stop()

    entity = st.session_state.entity

    # Initialize reactive state tracking
    if "last_data_hash" not in st.session_state:
        st.session_state.last_data_hash = entity.get_data_hash()
    if "auto_refresh_enabled" not in st.session_state:
        st.session_state.auto_refresh_enabled = True
    if "refresh_interval" not in st.session_state:
        st.session_state.refresh_interval = 3  # seconds

    # --- HEADER WITH EXPLANATION ---
    header_col1, header_col2 = st.columns([3, 1])

    with header_col1:
        st.title("🌑 Waft Larval Form")
        st.markdown("""
        **What is this?** This is a 3D printing workflow manager that tracks G-code files and print jobs. 
        It stores everything in a SQLite database and provides a dashboard to monitor activity and manage print jobs.
        """)

    with header_col2:
        # Auto-refresh controls
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        auto_refresh = st.checkbox(
            "🔄 Auto-refresh",
            value=st.session_state.auto_refresh_enabled,
            key="auto_refresh_checkbox",
            help="Automatically refresh when data changes",
        )
        st.session_state.auto_refresh_enabled = auto_refresh

        if auto_refresh:
            interval = st.selectbox(
                "Interval",
                options=[2, 3, 5, 10],
                index=1,  # Default to 3 seconds
                format_func=lambda x: f"{x}s",
                key="refresh_interval_select",
                help="How often to check for updates",
            )
            st.session_state.refresh_interval = interval
            st.markdown(
                '<span class="auto-refresh-indicator"></span> <small>Live</small>',
                unsafe_allow_html=True,
            )

    # --- QUICK STATUS SUMMARY ---
    logs, artifacts = entity.pulse()
    status_col1, status_col2, status_col3, status_col4 = st.columns(4)

    with status_col1:
        total_logs = len(logs)
        st.metric("Total Events", total_logs)

    with status_col2:
        trauma_count = len(logs[logs["severity"] == "TRAUMA"]) if not logs.empty else 0
        st.metric(
            "Errors",
            trauma_count,
            delta=None,
            delta_color="inverse" if trauma_count == 0 else "normal",
        )

    with status_col3:
        total_artifacts = len(artifacts)
        st.metric("Total Artifacts", total_artifacts)

    with status_col4:
        pending = len(artifacts[artifacts["status"] == "VOID"]) if not artifacts.empty else 0
        st.metric("Pending Jobs", pending)

    st.divider()

    # --- DASHBOARD COLUMNS ---
    col_mem, col_act = st.columns([2, 1])

    # --- COLUMN 1: THE CHRONICLE (Memory) - Reactive ---
    with col_mem:
        st.subheader("📋 Activity Log")
        st.caption(
            "All system events, actions, and errors are recorded here. This is the complete history of what the system has done."
        )

        # Check for active trauma
        if not logs.empty and logs.iloc[0]["severity"] == "TRAUMA":
            st.markdown(
                f"<div class='trauma-alert'>⚠️ ERROR DETECTED: {logs.iloc[0]['message']}</div>",
                unsafe_allow_html=True,
            )

        if logs.empty:
            st.info("No activity logged yet. Events will appear here as you use the system.")
        else:
            # Display logs with better formatting
            display_logs = logs[["timestamp", "severity", "message"]].copy()
            # Add emoji indicators for severity
            display_logs["severity"] = display_logs["severity"].map(
                {"THOUGHT": "💭 THOUGHT", "STRAIN": "⚠️ STRAIN", "TRAUMA": "🔴 TRAUMA"}
            )
            st.dataframe(display_logs, height=300, use_container_width=True, hide_index=True)

            with st.expander("ℹ️ About Severity Levels"):
                st.write("""
                - **THOUGHT**: Normal system activity (startup, successful operations)
                - **STRAIN**: Warnings or non-critical issues
                - **TRAUMA**: Errors that were caught and logged (system continues running)
                """)

    # --- COLUMN 2: MANIFESTATION (Action) ---
    with col_act:
        st.subheader("🖨️ Print Job Management")
        st.caption(
            "Manage G-code files and track print job status. Artifacts start as VOID (pending) and become PHYSICAL (printed)."
        )

        # Scan for next limb
        next_part = entity.get_next_manifestation()

        if next_part:
            part_id, name, gcode, status, _ = next_part
            st.info(f"**Next Job**: {name}")
            st.write(f"**Status**: {status}")
            st.write(f"**Artifact ID**: {part_id}")

            with st.expander("📄 View G-code"):
                st.code(gcode, language="gcode")

            st.divider()
            st.write("**Actions**:")

            # THE RITUAL BUTTONS
            if st.button(
                "🔌 Connect to Printer",
                key="connect_printer",
                help="Simulate USB/Serial connection to 3D printer",
            ):
                # Simulation of the Web Serial / PySerial connection
                with st.spinner("Connecting to printer..."):
                    time.sleep(2)
                    # We simulate a "Trauma" here randomly to show the system working
                    if random.random() < 0.3:
                        entity.safe_breath(lambda: 1 / 0)  # Deliberate crash
                        st.error("❌ Connection failed. Error logged.")
                        st.rerun()
                    else:
                        entity.chronicle(Severity.THOUGHT, "Printer connection established.")
                        st.success("✅ Connected successfully")

            if st.button(
                "✅ Mark as Printed",
                key="mark_printed",
                help="Mark this G-code file as successfully printed",
            ):
                with st.spinner("Updating status..."):
                    time.sleep(1)
                    entity.confirm_birth(part_id)
                    st.success("✅ Job marked as complete!")
                    st.balloons()
                    st.rerun()
        else:
            st.success("✅ All Artifacts Complete")
            st.info("""
            **Status**: All artifacts in the database have been marked as PHYSICAL.
            
            **What this means**:
            - All G-code files have been processed/printed
            - No pending print jobs remaining
            - You can export the data using the buttons below, or add new artifacts to continue
            """)

            with st.expander("➕ How to Add More Artifacts"):
                st.write("**Option 1: Reset Database** (Start fresh)")
                if st.button("🗑️ Delete Database & Restart", key="reset_db"):
                    import os

                    if os.path.exists(DB_NAME):
                        os.remove(DB_NAME)
                        st.session_state.entity = None
                        st.rerun()

                st.write("**Option 2: Add via SQL** (Keep existing data)")
                st.code(
                    """
# Connect to database and run:
sqlite3 waft_memory.db

# Then insert new artifact:
INSERT INTO artifacts (name, gcode, status) 
VALUES ('New_Artifact_Name', 'G28\\nG1 X10 Y10', 'VOID');

# Refresh the page to see the new artifact
                """,
                    language="sql",
                )

    # --- DATA EXPORT SECTION ---
    st.divider()
    st.subheader("📥 Export Data")
    st.caption(
        "Download all data (activity logs, artifacts, statistics) in various formats for analysis or backup."
    )

    export_col1, export_col2, export_col3, export_col4 = st.columns(4)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    with export_col1:
        json_data = entity.export_json()
        st.download_button(
            label="📄 Download JSON",
            data=json_data,
            file_name=f"waft_entity_export_{timestamp}.json",
            mime="application/json",
            key="download_json",
        )

    with export_col2:
        md_data = entity.export_markdown()
        st.download_button(
            label="📝 Download Markdown",
            data=md_data,
            file_name=f"waft_entity_export_{timestamp}.md",
            mime="text/markdown",
            key="download_markdown",
        )

    with export_col3:
        txt_data = entity.export_txt()
        st.download_button(
            label="📄 Download TXT",
            data=txt_data,
            file_name=f"waft_entity_export_{timestamp}.txt",
            mime="text/plain",
            key="download_txt",
        )

    with export_col4:
        # Try to generate actual PDF, fallback to markdown
        pdf_bytes = entity.export_pdf_bytes()
        if pdf_bytes:
            st.download_button(
                label="📑 Download PDF",
                data=pdf_bytes,
                file_name=f"waft_entity_export_{timestamp}.pdf",
                mime="application/pdf",
                key="download_pdf",
            )
        else:
            st.download_button(
                label="📑 Download PDF (MD)",
                data=md_data,
                file_name=f"waft_entity_export_{timestamp}.md",
                mime="text/markdown",
                help="PDF generation unavailable - Markdown format (convert using pandoc)",
                key="download_pdf_fallback",
            )

    # --- REACTIVE UPDATE SYSTEM ---
    # Lightweight auto-refresh: check data hash and only rerun when changed
    if st.session_state.auto_refresh_enabled:
        current_hash = entity.get_data_hash()

        # Check if data changed
        if current_hash != st.session_state.last_data_hash:
            # Data changed - update hash and rerun
            st.session_state.last_data_hash = current_hash
            time.sleep(0.1)  # Small delay to prevent rapid reruns
            st.rerun()
        else:
            # No change - schedule next check using lightweight JavaScript
            # This uses Streamlit's built-in rerun mechanism via meta refresh
            refresh_js = f"""
            <script>
            setTimeout(function() {{
                // Trigger Streamlit rerun via postMessage (lightweight, non-blocking)
                if (window.parent && window.parent.postMessage) {{
                    window.parent.postMessage({{
                        type: 'streamlit:rerun',
                        isStreamlitMessage: true
                    }}, '*');
                }}
            }}, {st.session_state.refresh_interval * 1000});
            </script>
            """
            # Inject at end of page (lightweight, non-blocking)
            st.markdown(refresh_js, unsafe_allow_html=True)

    # --- FOOTER ---
    st.divider()
    refresh_status = "🔄 Auto" if st.session_state.auto_refresh_enabled else "⏸️ Manual"
    st.caption(
        f"💾 Database: `{DB_NAME}` | 📊 {len(logs)} events logged | {refresh_status} | ✅ System operational"
    )

    # --- HELP SECTION ---
    with st.expander("❓ Help & Information"):
        st.markdown("""
        ### What is Waft Larval Form?
        
        This is a **3D printing workflow manager** that helps you:
        - Track G-code files (3D printer instructions)
        - Monitor print job status
        - Log all system activity
        - Export data for analysis
        
        ### How It Works
        
        1. **Artifacts**: G-code files stored in the database
           - Status: `VOID` (pending) → `PHYSICAL` (printed)
        2. **Activity Log**: All events are recorded
           - Normal operations, warnings, and errors
        3. **Database**: SQLite file (`waft_memory.db`) stores everything
           - Persists across restarts
           - Can be migrated to future Redbean version
        
        ### Key Features
        
        - **Error Resilience**: Errors are logged, not crashes
        - **Data Export**: Download in JSON, Markdown, TXT, or PDF
        - **Status Tracking**: See what's pending vs completed
        - **Activity History**: Complete log of all system events
        
        ### Terminology
        
        - **Artifact**: A G-code file (3D printer instructions)
        - **Chronicle**: The activity log (all events)
        - **Trauma**: An error that was caught and logged
        - **VOID/PHYSICAL**: Print job status (pending/complete)
        """)


if __name__ == "__main__":
    main()
