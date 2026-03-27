import React, { useEffect, useState } from "https://esm.sh/react@18.2.0";
import { createRoot } from "https://esm.sh/react-dom@18.2.0/client";
import htm from "https://esm.sh/htm@3.1.1";

const html = htm.bind(React.createElement);

function App() {
  const [soulId, setSoulId] = useState("");
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadProfile() {
    setLoading(true);
    setError("");
    try {
      const params = new URLSearchParams();
      if (soulId.trim()) params.set("soul_id", soulId.trim());
      const query = params.toString();
      const res = await fetch(`/api/oracle/profile${query ? `?${query}` : ""}`);
      if (!res.ok) throw new Error(`Failed to load profile (${res.status})`);
      setProfile(await res.json());
    } catch (e) {
      setError(String(e));
      setProfile(null);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadProfile();
  }, []);

  return html`
    <div className="wrap">
      <h1>Oracle Profile</h1>
      <p className="muted">Dedicated profile surface for personality, epistemic readiness, and reincarnation summary.</p>
      <p className="muted"><a href="/api/pantheon/oracle-cycle/ui">Back to Oracle Cycle</a></p>
      ${error ? html`<div className="card" style=${{ borderColor: "#ef4444", color: "#991b1b" }}>${error}</div>` : null}
      <section className="card">
        <h2>Load Profile</h2>
        <input value=${soulId} onInput=${(e) => setSoulId(e.target.value)} placeholder="Soul id (optional)" />
        <button onClick=${loadProfile} disabled=${loading}>${loading ? "Refreshing..." : "Refresh Profile"}</button>
      </section>
      ${profile
        ? html`
          <section className="card">
            <h2>${profile.oracle?.name || "The Oracle"}</h2>
            <p className="muted">${profile.oracle?.title || ""} (${profile.oracle?.type || "balanced"})</p>
            <pre>${JSON.stringify(profile.oracle || {}, null, 2)}</pre>
          </section>
          <section className="card">
            <h2>Epistemic Snapshot</h2>
            <pre>${JSON.stringify(profile.epistemic || {}, null, 2)}</pre>
          </section>
          <section className="card">
            <h2>Reincarnation Summary</h2>
            <pre>${JSON.stringify(profile.reincarnation || {}, null, 2)}</pre>
          </section>
        `
        : html`<div className="card muted">Profile not loaded.</div>`}
    </div>
  `;
}

createRoot(document.getElementById("root")).render(html`<${App} />`);
