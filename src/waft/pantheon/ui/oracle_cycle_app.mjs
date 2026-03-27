import React, { useEffect, useState } from "https://esm.sh/react@18.2.0";
import { createRoot } from "https://esm.sh/react-dom@18.2.0/client";
import htm from "https://esm.sh/htm@3.1.1";

const html = htm.bind(React.createElement);

function App() {
  const [objective, setObjective] = useState("Pantheon oracle cycle for current development focus");
  const [orderPrompt, setOrderPrompt] = useState("");
  const [riskPrompt, setRiskPrompt] = useState("");
  const [profileSoulId, setProfileSoulId] = useState("");
  const [profile, setProfile] = useState(null);
  const [profileLoading, setProfileLoading] = useState(false);
  const [runs, setRuns] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadRuns() {
    try {
      const res = await fetch("/api/pantheon/oracle-cycle/runs");
      if (!res.ok) throw new Error(`Failed to load runs (${res.status})`);
      const data = await res.json();
      setRuns(data);
      if (!selectedId && data.length) setSelectedId(data[0].run_id);
    } catch (e) {
      setError(String(e));
    }
  }

  async function loadRun(runId) {
    if (!runId) return;
    try {
      const res = await fetch(`/api/pantheon/oracle-cycle/runs/${runId}`);
      if (!res.ok) throw new Error(`Failed to load run ${runId} (${res.status})`);
      setSelected(await res.json());
    } catch (e) {
      setError(String(e));
      setSelected(null);
    }
  }

  async function runCycle() {
    setLoading(true);
    setError("");
    try {
      const payload = { objective };
      if (orderPrompt.trim()) payload.order_prompt = orderPrompt.trim();
      if (riskPrompt.trim()) payload.risk_prompt = riskPrompt.trim();
      const res = await fetch("/api/pantheon/oracle-cycle/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error(`Run failed (${res.status})`);
      const data = await res.json();
      await loadRuns();
      setSelectedId(data.run_id);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }

  async function loadProfile() {
    setProfileLoading(true);
    try {
      const params = new URLSearchParams();
      if (profileSoulId.trim()) params.set("soul_id", profileSoulId.trim());
      const query = params.toString();
      const res = await fetch(`/api/oracle/profile${query ? `?${query}` : ""}`);
      if (!res.ok) throw new Error(`Failed to load profile (${res.status})`);
      setProfile(await res.json());
    } catch (e) {
      setError(String(e));
      setProfile(null);
    } finally {
      setProfileLoading(false);
    }
  }

  useEffect(() => {
    loadRuns();
    loadProfile();
  }, []);

  useEffect(() => {
    loadRun(selectedId);
  }, [selectedId]);

  return html`
    <div className="wrap">
      <h1>Pantheon Oracle Cycle</h1>
      <p className="muted">Independent Pantheon UI for traceable oracle decisions and reasoning timeline.</p>
      ${error ? html`<div className="card" style=${{ borderColor: "#ef4444", color: "#991b1b" }}>${error}</div>` : null}
      <div className="layout">
        <section className="card">
          <h2>Run Cycle</h2>
          <div className="muted" style=${{ marginBottom: "8px" }}>
            <a href="/api/pantheon/oracle-cycle/ui/profile">Open dedicated Oracle profile</a>
          </div>
          <input value=${objective} onInput=${(e) => setObjective(e.target.value)} placeholder="Objective" />
          <textarea rows="3" value=${orderPrompt} onInput=${(e) => setOrderPrompt(e.target.value)} placeholder="Order prompt (optional)"></textarea>
          <textarea rows="3" value=${riskPrompt} onInput=${(e) => setRiskPrompt(e.target.value)} placeholder="Risk prompt (optional)"></textarea>
          <button onClick=${runCycle} disabled=${loading || !objective.trim()}>${loading ? "Running..." : "Run Oracle Cycle"}</button>
          <h3 style=${{ marginTop: "14px" }}>Oracle Profile</h3>
          <input value=${profileSoulId} onInput=${(e) => setProfileSoulId(e.target.value)} placeholder="Soul id (optional)" />
          <button onClick=${loadProfile} disabled=${profileLoading}>${profileLoading ? "Refreshing..." : "Refresh Profile"}</button>
          ${profile
            ? html`
              <div className="profile-card">
                <div><strong>${profile.oracle?.name || "The Oracle"}</strong> <span className="muted">(${profile.oracle?.type || "balanced"})</span></div>
                <div className="muted">${profile.oracle?.title || ""}</div>
                <div className="muted">epistemic ready: ${String(profile.epistemic?.ready)} | context: ${String(profile.epistemic?.has_context)}</div>
                <div className="muted">findings: ${profile.epistemic?.findings_count ?? 0} | unknowns: ${profile.epistemic?.unknowns_count ?? 0}</div>
                <div className="muted">soul: ${profile.reincarnation?.soul_id || "none"} | lifetimes: ${profile.reincarnation?.lifetimes_count ?? 0} | karma: ${profile.reincarnation?.total_karma ?? 0}</div>
              </div>
            `
            : html`<div className="muted">Profile not loaded.</div>`}
          <h3 style=${{ marginTop: "14px" }}>History</h3>
          ${runs.map((run) => html`
            <div key=${run.run_id} className=${`run-item ${selectedId === run.run_id ? "active" : ""}`} onClick=${() => setSelectedId(run.run_id)}>
              <div><strong>${run.objective}</strong></div>
              <div className="muted">${run.generated_at}</div>
              <span className=${`pill ${run.order_decision}`}>${run.order_decision}</span>
              <span className=${`pill ${run.risk_decision}`}>${run.risk_decision}</span>
            </div>
          `)}
        </section>
        <section className="card">
          ${selected
            ? html`
              <h2>Run ${selected.run_id}</h2>
              <p className="muted">${selected.objective}</p>
              <span className=${`pill ${selected.order_decision}`}>${selected.order_decision}</span>
              <span className=${`pill ${selected.risk_decision}`}>${selected.risk_decision}</span>
              <h3 style=${{ marginTop: "14px" }}>Decision Timeline</h3>
              <div className="timeline">
                ${(selected.timeline || []).map((node) => html`
                  <article key=${node.step} className="node">
                    <div><strong>${node.step}</strong> <span className=${`pill ${node.decision}`}>${node.decision}</span></div>
                    <div className="muted">Prompt</div>
                    <pre>${node.prompt}</pre>
                    <div className="muted">Reasoning</div>
                    <pre>${node.reasoning}</pre>
                    <details>
                      <summary>Recommendation</summary>
                      <pre>${node.recommendation}</pre>
                    </details>
                  </article>
                `)}
              </div>
            `
            : html`<p className="muted">Select a run from history to inspect its reasoning trace.</p>`}
        </section>
      </div>
    </div>
  `;
}

createRoot(document.getElementById("root")).render(html`<${App} />`);
