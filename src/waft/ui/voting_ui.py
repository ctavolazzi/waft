"""
WAFT Town Voting System UI
==========================

Streamlit UI for the WAFT Town voting system and TheCouncil court system.

Features:
- Vote casting interface
- Voting results display
- Court proceedings viewer
- Court document generation
- Council member management
- Voting history tracking
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

# Database setup
DB_PATH = Path("_hidden/.truth/voting_system.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def init_database():
    """Initialize voting system database."""
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    # Votes table
    c.execute("""CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vote_id TEXT UNIQUE NOT NULL,
        decision_id TEXT NOT NULL,
        voter_id TEXT NOT NULL,
        vote_choice TEXT NOT NULL,
        reasoning TEXT,
        timestamp TEXT NOT NULL,
        status TEXT DEFAULT 'active'
    )""")

    # Decisions table
    c.execute("""CREATE TABLE IF NOT EXISTS decisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        decision_id TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        options TEXT NOT NULL,  -- JSON array
        decision_type TEXT NOT NULL,  -- binary, multiple_choice, ranked
        status TEXT DEFAULT 'open',  -- open, closed, resolved
        created_at TEXT NOT NULL,
        resolved_at TEXT
    )""")

    # Council members table
    c.execute("""CREATE TABLE IF NOT EXISTS council_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        status TEXT DEFAULT 'active',
        joined_at TEXT NOT NULL
    )""")

    # Court proceedings table
    c.execute("""CREATE TABLE IF NOT EXISTS court_proceedings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proceeding_id TEXT UNIQUE NOT NULL,
        case_id TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        timestamp TEXT NOT NULL,
        status TEXT DEFAULT 'active'
    )""")

    conn.commit()
    conn.close()


def get_db_connection():
    """Get database connection."""
    return sqlite3.connect(str(DB_PATH))


def create_decision(
    decision_id: str, title: str, description: str, options: list[str], decision_type: str
):
    """Create a new decision."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """INSERT INTO decisions
                 (decision_id, title, description, options, decision_type, created_at)
                 VALUES (?, ?, ?, ?, ?, ?)""",
        (
            decision_id,
            title,
            description,
            json.dumps(options),
            decision_type,
            datetime.now().isoformat(),
        ),
    )
    conn.commit()
    conn.close()


def cast_vote(vote_id: str, decision_id: str, voter_id: str, vote_choice: str, reasoning: str = ""):
    """Cast a vote."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """INSERT INTO votes
                 (vote_id, decision_id, voter_id, vote_choice, reasoning, timestamp)
                 VALUES (?, ?, ?, ?, ?, ?)""",
        (vote_id, decision_id, voter_id, vote_choice, reasoning, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def get_votes_for_decision(decision_id: str) -> list[dict[str, Any]]:
    """Get all votes for a decision."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """SELECT vote_id, voter_id, vote_choice, reasoning, timestamp
                 FROM votes WHERE decision_id = ? AND status = 'active' """,
        (decision_id,),
    )
    rows = c.fetchall()
    conn.close()

    return [
        {
            "vote_id": row[0],
            "voter_id": row[1],
            "vote_choice": row[2],
            "reasoning": row[3],
            "timestamp": row[4],
        }
        for row in rows
    ]


def get_decision_results(decision_id: str) -> dict[str, Any]:
    """Calculate voting results for a decision."""
    votes = get_votes_for_decision(decision_id)

    if not votes:
        return {"total_votes": 0, "results": {}, "winner": None}

    # Count votes
    vote_counts = {}
    for vote in votes:
        choice = vote["vote_choice"]
        vote_counts[choice] = vote_counts.get(choice, 0) + 1

    # Find winner (majority)
    total = len(votes)
    winner = max(vote_counts.items(), key=lambda x: x[1]) if vote_counts else None

    return {
        "total_votes": total,
        "results": vote_counts,
        "winner": winner[0] if winner else None,
        "winner_votes": winner[1] if winner else 0,
        "votes": votes,
    }


def get_all_decisions() -> list[dict[str, Any]]:
    """Get all decisions."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT decision_id, title, description, options, decision_type, status, created_at
                 FROM decisions ORDER BY created_at DESC""")
    rows = c.fetchall()
    conn.close()

    return [
        {
            "decision_id": row[0],
            "title": row[1],
            "description": row[2],
            "options": json.loads(row[3]),
            "decision_type": row[4],
            "status": row[5],
            "created_at": row[6],
        }
        for row in rows
    ]


def add_council_member(member_id: str, name: str, role: str):
    """Add a council member."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """INSERT OR REPLACE INTO council_members
                 (member_id, name, role, joined_at)
                 VALUES (?, ?, ?, ?)""",
        (member_id, name, role, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def get_council_members() -> list[dict[str, Any]]:
    """Get all council members."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT member_id, name, role, status, joined_at
                 FROM council_members WHERE status = 'active' ORDER BY joined_at""")
    rows = c.fetchall()
    conn.close()

    return [
        {"member_id": row[0], "name": row[1], "role": row[2], "status": row[3], "joined_at": row[4]}
        for row in rows
    ]


def main():
    """Main Streamlit application."""
    st.set_page_config(page_title="WAFT Town Voting System", page_icon="⚖️", layout="wide")

    # Initialize database
    init_database()

    # Header
    st.title("⚖️ WAFT Town Court - TheCouncil")
    st.markdown("**Voting System and Court Proceedings**")

    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Navigation",
        [
            "🏠 Dashboard",
            "🗳️ Cast Vote",
            "📊 Voting Results",
            "👥 Council Members",
            "📜 Court Proceedings",
            "📄 Generate Document",
        ],
    )

    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "🗳️ Cast Vote":
        show_cast_vote()
    elif page == "📊 Voting Results":
        show_voting_results()
    elif page == "👥 Council Members":
        show_council_members()
    elif page == "📜 Court Proceedings":
        show_court_proceedings()
    elif page == "📄 Generate Document":
        show_generate_document()


def show_dashboard():
    """Show dashboard."""
    st.header("Dashboard")

    decisions = get_all_decisions()
    council_members = get_council_members()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Decisions", len(decisions))

    with col2:
        active_decisions = len([d for d in decisions if d["status"] == "open"])
        st.metric("Active Decisions", active_decisions)

    with col3:
        st.metric("Council Members", len(council_members))

    st.subheader("Recent Decisions")
    if decisions:
        for decision in decisions[:5]:
            with st.expander(f"{decision['title']} ({decision['status']})"):
                st.write(decision["description"])
                st.write(f"**Type:** {decision['decision_type']}")
                st.write(f"**Options:** {', '.join(decision['options'])}")
                st.write(f"**Created:** {decision['created_at']}")
    else:
        st.info("No decisions yet. Create one in the 'Cast Vote' section.")


def show_cast_vote():
    """Show vote casting interface."""
    st.header("Cast Vote")

    # Create new decision
    with st.expander("Create New Decision", expanded=False):
        decision_title = st.text_input("Decision Title")
        decision_desc = st.text_area("Description")
        decision_type = st.selectbox("Decision Type", ["binary", "multiple_choice", "ranked"])

        num_options = st.number_input("Number of Options", min_value=2, max_value=10, value=2)
        options = []
        for i in range(num_options):
            option = st.text_input(f"Option {i + 1}", key=f"option_{i}")
            if option:
                options.append(option)

        if st.button("Create Decision"):
            if decision_title and len(options) >= 2:
                decision_id = f"decision_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                create_decision(decision_id, decision_title, decision_desc, options, decision_type)
                st.success(f"Decision '{decision_title}' created!")
                st.rerun()
            else:
                st.error("Please provide a title and at least 2 options.")

    # Cast vote on existing decision
    st.subheader("Vote on Existing Decision")
    decisions = [d for d in get_all_decisions() if d["status"] == "open"]

    if decisions:
        selected_decision = st.selectbox(
            "Select Decision", decisions, format_func=lambda x: x["title"]
        )

        if selected_decision:
            st.write(f"**Description:** {selected_decision['description']}")
            st.write(f"**Type:** {selected_decision['decision_type']}")

            voter_id = st.text_input("Your ID (Voter ID)")
            vote_choice = st.selectbox("Your Vote", selected_decision["options"])
            reasoning = st.text_area("Reasoning (optional)")

            if st.button("Cast Vote"):
                if voter_id:
                    vote_id = (
                        f"vote_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(voter_id) % 10000}"
                    )
                    cast_vote(
                        vote_id, selected_decision["decision_id"], voter_id, vote_choice, reasoning
                    )
                    st.success("Vote cast successfully!")
                    st.rerun()
                else:
                    st.error("Please provide a voter ID.")
    else:
        st.info("No open decisions available. Create one above.")


def show_voting_results():
    """Show voting results."""
    st.header("Voting Results")

    decisions = get_all_decisions()

    if not decisions:
        st.info("No decisions yet.")
        return

    selected_decision = st.selectbox(
        "Select Decision", decisions, format_func=lambda x: f"{x['title']} ({x['status']})"
    )

    if selected_decision:
        results = get_decision_results(selected_decision["decision_id"])

        st.subheader(selected_decision["title"])
        st.write(selected_decision["description"])

        if results["total_votes"] > 0:
            st.metric("Total Votes", results["total_votes"])

            if results["winner"]:
                st.success(f"**Winner:** {results['winner']} ({results['winner_votes']} votes)")

            # Results chart
            if results["results"]:
                df = pd.DataFrame(
                    [{"Option": k, "Votes": v} for k, v in results["results"].items()]
                )
                st.bar_chart(df.set_index("Option"))

            # Individual votes
            st.subheader("Individual Votes")
            votes_df = pd.DataFrame(results["votes"])
            if not votes_df.empty:
                st.dataframe(
                    votes_df[["voter_id", "vote_choice", "reasoning", "timestamp"]],
                    use_container_width=True,
                )
        else:
            st.info("No votes cast yet for this decision.")


def show_council_members():
    """Show council members management."""
    st.header("Council Members")

    # Add new member
    with st.expander("Add Council Member", expanded=False):
        member_id = st.text_input("Member ID")
        member_name = st.text_input("Name")
        member_role = st.selectbox(
            "Role", ["Chief Justice", "Justice", "Court Clerk", "Council Member"]
        )

        if st.button("Add Member"):
            if member_id and member_name:
                add_council_member(member_id, member_name, member_role)
                st.success(f"Member '{member_name}' added!")
                st.rerun()
            else:
                st.error("Please provide both ID and name.")

    # List members
    members = get_council_members()
    if members:
        st.subheader("Active Council Members")
        for member in members:
            st.write(f"**{member['name']}** - {member['role']} (ID: {member['member_id']})")
            st.write(f"Joined: {member['joined_at']}")
            st.divider()
    else:
        st.info("No council members yet. Add one above.")


def create_court_proceeding(proceeding_id: str, case_id: str, title: str, description: str):
    """Create a new court proceeding."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """INSERT INTO court_proceedings
                 (proceeding_id, case_id, title, description, timestamp, status)
                 VALUES (?, ?, ?, ?, ?, ?)""",
        (proceeding_id, case_id, title, description, datetime.now().isoformat(), "active"),
    )
    conn.commit()
    conn.close()


def get_court_proceedings() -> list[dict[str, Any]]:
    """Get all court proceedings."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT proceeding_id, case_id, title, description, timestamp, status
                 FROM court_proceedings ORDER BY timestamp DESC""")
    rows = c.fetchall()
    conn.close()

    return [
        {
            "proceeding_id": row[0],
            "case_id": row[1],
            "title": row[2],
            "description": row[3],
            "timestamp": row[4],
            "status": row[5],
        }
        for row in rows
    ]


def show_court_proceedings():
    """Show court proceedings."""
    st.header("Court Proceedings")

    # Create new proceeding
    with st.expander("Create New Court Proceeding", expanded=False):
        case_id = st.text_input("Case ID")
        proceeding_title = st.text_input("Proceeding Title")
        proceeding_desc = st.text_area("Description")

        if st.button("Create Proceeding"):
            if case_id and proceeding_title:
                proceeding_id = f"proceeding_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                create_court_proceeding(proceeding_id, case_id, proceeding_title, proceeding_desc)
                st.success(f"Proceeding '{proceeding_title}' created!")
                st.rerun()
            else:
                st.error("Please provide both Case ID and Title.")

    # List proceedings
    st.subheader("Court Proceedings")
    proceedings = get_court_proceedings()

    if proceedings:
        for proceeding in proceedings:
            with st.expander(f"{proceeding['title']} (Case: {proceeding['case_id']})"):
                st.write(f"**Case ID:** {proceeding['case_id']}")
                st.write(f"**Description:** {proceeding['description']}")
                st.write(f"**Status:** {proceeding['status']}")
                st.write(f"**Date:** {proceeding['timestamp']}")
    else:
        st.info("No court proceedings yet. Create one above.")


def show_generate_document():
    """Show court document generation."""
    st.header("Generate Court Document")

    # Get available data for document
    decisions = get_all_decisions()
    council_members = get_council_members()
    proceedings = get_court_proceedings()

    # Document type selection
    doc_type = st.selectbox(
        "Document Type", ["Court Resolution", "Voting Record", "Council Meeting", "Custom Document"]
    )

    # Document details
    doc_title = st.text_input(
        "Document Title", value=f"{doc_type} - {datetime.now().strftime('%Y-%m-%d')}"
    )
    doc_id = st.text_input("Document ID", value=f"COURT-{datetime.now().strftime('%Y%m%d')}")

    # Content selection
    st.subheader("Include in Document")
    include_decisions = st.checkbox("Include Recent Decisions", value=True)
    include_votes = st.checkbox("Include Voting Results", value=True)
    include_council = st.checkbox("Include Council Members", value=True)
    include_proceedings = st.checkbox("Include Court Proceedings", value=True)

    # Custom content
    custom_content = st.text_area(
        "Additional Content (HTML)", height=200, help="Add custom HTML content for the document"
    )

    if st.button("Generate Document"):
        try:
            # Build document content
            content_parts = []

            if include_council and council_members:
                content_parts.append("<h2>COUNCIL MEMBERS</h2>")
                content_parts.append("<div class='council-section'>")
                content_parts.append("<div class='council-title'>TheCouncil</div>")
                for member in council_members:
                    content_parts.append("<div class='council-member'>")
                    content_parts.append(
                        f"<span class='council-role'>{member['role']}:</span> {member['name']}"
                    )
                    content_parts.append("</div>")
                content_parts.append("</div>")

            if include_decisions and decisions:
                content_parts.append("<h2>RECENT DECISIONS</h2>")
                for decision in decisions[:5]:
                    content_parts.append(f"<h3>{decision['title']}</h3>")
                    content_parts.append(f"<p class='legal-text'>{decision['description']}</p>")
                    content_parts.append(f"<p><strong>Status:</strong> {decision['status']}</p>")
                    content_parts.append(
                        f"<p><strong>Created:</strong> {decision['created_at']}</p>"
                    )

            if include_votes and decisions:
                content_parts.append("<h2>VOTING RESULTS</h2>")
                for decision in decisions[:3]:
                    results = get_decision_results(decision["decision_id"])
                    if results["total_votes"] > 0:
                        content_parts.append(f"<h3>{decision['title']}</h3>")
                        content_parts.append(
                            f"<p><strong>Total Votes:</strong> {results['total_votes']}</p>"
                        )
                        if results["winner"]:
                            content_parts.append(
                                f"<p><strong>Winner:</strong> {results['winner']} ({results['winner_votes']} votes)</p>"
                            )

            if include_proceedings and proceedings:
                content_parts.append("<h2>COURT PROCEEDINGS</h2>")
                for proceeding in proceedings[:5]:
                    content_parts.append("<div class='proceeding-entry'>")
                    content_parts.append(
                        f"<div class='proceeding-time'>{proceeding['timestamp']}</div>"
                    )
                    content_parts.append(f"<h3>{proceeding['title']}</h3>")
                    content_parts.append(
                        f"<p class='proceeding-text'>{proceeding['description']}</p>"
                    )
                    content_parts.append("</div>")

            if custom_content:
                content_parts.append(custom_content)

            content = "\n".join(content_parts)

            # Generate PDF
            from pathlib import Path

            from waft.templates.waft_town import generate_waft_town_document

            output_dir = Path.home() / "Desktop"
            output_path = output_dir / f"{doc_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

            generate_waft_town_document(
                title=doc_title,
                content=content,
                output_path=output_path,
                doc_id=doc_id,
                date=datetime.now().strftime("%B %d, %Y"),
            )

            st.success(f"Document generated: {output_path.name}")
            st.info(f"Saved to: {output_path}")

            # Option to open
            if st.button("Open Document"):
                import subprocess

                subprocess.run(["open", str(output_path)])

            # Option to print
            if st.button("Print Document"):
                import subprocess

                subprocess.run(["lpr", str(output_path)])
                st.success("Document sent to printer!")

        except Exception as e:
            st.error(f"Error generating document: {str(e)}")
            st.exception(e)


if __name__ == "__main__":
    main()
