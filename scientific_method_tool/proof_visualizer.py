#!/usr/bin/env python3
"""
Streamlit App: Visualize Multiple Proof Experiments

Shows all proof experiments side-by-side for comparison.
"""

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Page config
st.set_page_config(
    page_title="Scientific Method Tool - Proof Visualizer", page_icon="🔬", layout="wide"
)

# Title
st.title("🔬 Scientific Method Tool - Proof Visualizer")
st.markdown("**Multiple proof experiments compared side-by-side**")

# Load proof data
proof_storage = Path("scientific_method_tool/proof_experiments")
summary_file = proof_storage / "proof_summary.json"

if not summary_file.exists():
    st.error(f"❌ Proof summary not found at: {summary_file}")
    st.info("Run `python3 scientific_method_tool/run_multiple_proofs.py` first")
    st.stop()

# Load summary
with open(summary_file) as f:
    summary_data = json.load(f)

proofs = summary_data.get("proofs", [])
total_proofs = summary_data.get("total_proofs", 0)

# Sidebar
st.sidebar.header("📊 Overview")
st.sidebar.metric("Total Proofs", total_proofs)
st.sidebar.metric("Verified", sum(1 for p in proofs if p["analysis"]["verified"]))
st.sidebar.metric(
    "Average Confidence",
    f"{sum(p['analysis']['confidence'] for p in proofs) / len(proofs):.1%}" if proofs else "N/A",
)

# Main content
if not proofs:
    st.warning("No proof experiments found")
    st.stop()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(
    ["📈 Overview", "🔬 Experiments", "📊 Data Comparison", "📁 Files"]
)

with tab1:
    st.header("Proof Experiments Overview")

    # Summary table
    df = pd.DataFrame(
        [
            {
                "Proof ID": p["proof_id"],
                "Experiment ID": p["experiment_id"][:12] + "...",
                "Verified": "✅" if p["analysis"]["verified"] else "❌",
                "Confidence": f"{p['analysis']['confidence']:.1%}",
                "Data Series": len(p["data_series"]),
                "State Changed": p["initial_state_hash"] != p["final_state_hash"],
            }
            for p in proofs
        ]
    )

    st.dataframe(df, use_container_width=True)

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        # Confidence chart
        fig = px.bar(
            x=[f"Proof #{p['proof_id']}" for p in proofs],
            y=[p["analysis"]["confidence"] for p in proofs],
            title="Confidence by Proof",
            labels={"x": "Proof", "y": "Confidence"},
        )
        fig.update_layout(yaxis_tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Verification status
        verified_count = sum(1 for p in proofs if p["analysis"]["verified"])
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=["Verified", "Not Verified"],
                    values=[verified_count, len(proofs) - verified_count],
                    hole=0.3,
                )
            ]
        )
        fig.update_layout(title="Verification Status")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Individual Experiments")

    selected_proof = st.selectbox(
        "Select Proof to View", range(1, len(proofs) + 1), format_func=lambda x: f"Proof #{x}"
    )

    proof = proofs[selected_proof - 1]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📋 Experiment Info")
        st.write(f"**Experiment ID:** `{proof['experiment_id']}`")
        st.write(f"**Timestamp:** {proof['timestamp']}")
        st.write(f"**Initial State Hash:** `{proof['initial_state_hash']}`")
        st.write(f"**Final State Hash:** `{proof['final_state_hash']}`")
        st.write(
            f"**State Changed:** {'✅ Yes' if proof['initial_state_hash'] != proof['final_state_hash'] else '❌ No'}"
        )

    with col2:
        st.subheader("🔬 Analysis")
        st.write(f"**Verified:** {'✅ Yes' if proof['analysis']['verified'] else '❌ No'}")
        st.write(f"**Confidence:** {proof['analysis']['confidence']:.2%}")
        st.write(f"**Conclusions:** {proof['analysis']['conclusions_count']}")

    st.subheader("📊 Results")
    st.json(proof["results"])

    st.subheader("📈 Data Series")
    for name, series_data in proof["data_series"].items():
        with st.expander(f"Series: {name}"):
            st.write(f"**Data Points:** {series_data['count']}")
            st.write(f"**Values:** {series_data['values']}")

            # Chart
            if len(series_data["values"]) > 1:
                fig = px.line(
                    y=series_data["values"],
                    title=f"{name} Over Time",
                    labels={"y": name, "x": "Time"},
                )
                st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Data Comparison Across Proofs")

    # Collect all data series
    all_series = {}
    for proof in proofs:
        for name, series_data in proof["data_series"].items():
            if name not in all_series:
                all_series[name] = []
            all_series[name].append(
                {
                    "proof_id": proof["proof_id"],
                    "values": series_data["values"],
                    "count": series_data["count"],
                }
            )

    # Show comparison for each series
    for series_name, series_data in all_series.items():
        st.subheader(f"Series: {series_name}")

        # Create comparison chart
        fig = go.Figure()

        for data in series_data:
            proof_id = data["proof_id"]
            values = data["values"]

            if len(values) > 1:
                fig.add_trace(
                    go.Scatter(
                        y=values,
                        mode="lines+markers",
                        name=f"Proof #{proof_id}",
                        line=dict(width=2),
                    )
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        y=values, mode="markers", name=f"Proof #{proof_id}", marker=dict(size=10)
                    )
                )

        fig.update_layout(
            title=f"{series_name} Comparison Across Proofs",
            xaxis_title="Time Step",
            yaxis_title=series_name,
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Summary table
        df = pd.DataFrame(
            [
                {
                    "Proof ID": d["proof_id"],
                    "Data Points": d["count"],
                    "First Value": d["values"][0] if d["values"] else None,
                    "Last Value": d["values"][-1] if d["values"] else None,
                    "Change": d["values"][-1] - d["values"][0] if len(d["values"]) > 1 else None,
                }
                for d in series_data
            ]
        )
        st.dataframe(df, use_container_width=True)

with tab4:
    st.header("File Structure")

    st.subheader("📁 Storage Location")
    st.code(str(proof_storage.absolute()))

    # File counts
    experiments_dir = proof_storage / "experiments"
    states_dir = proof_storage / "states"
    data_dir = proof_storage / "data"

    col1, col2, col3 = st.columns(3)

    with col1:
        exp_files = list(experiments_dir.glob("*.json")) if experiments_dir.exists() else []
        st.metric("Experiment Files", len(exp_files))
        if exp_files:
            with st.expander("View Files"):
                for f in sorted(exp_files)[:10]:
                    st.text(f.name)
                if len(exp_files) > 10:
                    st.text(f"... and {len(exp_files) - 10} more")

    with col2:
        state_files = list(states_dir.glob("*.json")) if states_dir.exists() else []
        st.metric("State Files", len(state_files))
        if state_files:
            with st.expander("View Files"):
                for f in sorted(state_files)[:10]:
                    st.text(f.name)
                if len(state_files) > 10:
                    st.text(f"... and {len(state_files) - 10} more")

    with col3:
        data_files = list(data_dir.glob("*.json")) if data_dir.exists() else []
        st.metric("Data Files", len(data_files))
        if data_files:
            with st.expander("View Files"):
                for f in sorted(data_files)[:10]:
                    st.text(f.name)
                if len(data_files) > 10:
                    st.text(f"... and {len(data_files) - 10} more")

    # Summary file
    st.subheader("📄 Summary File")
    st.json(summary_data)

# Footer
st.markdown("---")
st.markdown("**Scientific Method Tool** - Proof Visualization")
st.caption(f"Last updated: {summary_data.get('timestamp', 'Unknown')}")
