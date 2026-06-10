const API_BASE = "/api";
let authToken = null;

async function jsonFetch(url, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (authToken) headers.Authorization = `Bearer ${authToken}`;
  const resp = await fetch(url, { ...options, headers });
  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`${resp.status} ${resp.statusText}: ${text}`);
  }
  return resp.json();
}

async function ensureHandshake() {
  if (authToken) return;
  const data = await jsonFetch(`${API_BASE}/auth/handshake`, {
    method: "POST",
    body: JSON.stringify({ client_name: "localhost-5050-dashboard", client_version: "0.1.0" })
  });
  authToken = data.token;
}

function renderSnapshot(payload) {
  const s = payload.summary || {};
  const container = document.getElementById("snapshot");
  container.innerHTML = `
    <p><span class="pill">branch</span> ${payload.state?.git?.branch || "unknown"}</p>
    <p><span class="pill">uncommitted</span> ${s.uncommitted_files ?? 0}</p>
    <p><span class="pill">integrity</span> ${Number(s.integrity || 0).toFixed(1)}%</p>
    <p><span class="pill">work efforts</span> ${s.work_efforts ?? 0}</p>
    <p><span class="pill">latest WE</span> ${payload.latest_work_effort_5050 || "none"}</p>
  `;
}

function renderTimeline(payload) {
  const timelineEl = document.getElementById("timeline");
  timelineEl.innerHTML = "";
  (payload.events || []).forEach((event) => {
    const node = document.createElement("div");
    node.className = "event";
    node.innerHTML = `
      <div><strong>${event.type}</strong> - ${event.name}</div>
      <div class="event-meta">${event.timestamp}</div>
      <div class="event-meta">${event.path}</div>
    `;
    timelineEl.appendChild(node);
  });
}

async function loadSession() {
  await ensureHandshake();
  const session = await jsonFetch(`${API_BASE}/5050/session`);
  renderSnapshot(session);
}

async function loadTimeline() {
  const timeline = await jsonFetch(`${API_BASE}/5050/timeline`);
  renderTimeline(timeline);
}

async function generateContinueCommand() {
  await ensureHandshake();
  const template = document.getElementById("templateSelect").value;
  const objective = document.getElementById("objectiveInput").value.trim();
  const payload = await jsonFetch(`${API_BASE}/5050/continue-command`, {
    method: "POST",
    body: JSON.stringify({ template, objective })
  });
  const output = document.getElementById("commandOutput");
  output.value = payload.command || "";
  return output.value;
}

async function generateReport() {
  await ensureHandshake();
  const title = document.getElementById("reportTitle").value;
  const notes = document.getElementById("reportNotes").value;
  const reportType = document.getElementById("reportType").value;
  const payload = await jsonFetch(`${API_BASE}/5050/report`, {
    method: "POST",
    body: JSON.stringify({
      title,
      notes,
      report_type: reportType,
      include_plan: true,
      include_timeline: true
    })
  });
  const reportLink = document.getElementById("reportLink");
  reportLink.href = `${API_BASE}/5050/file?path=${encodeURIComponent(payload.report_path)}`;
  reportLink.textContent = payload.report_path;
  reportLink.classList.remove("hidden");
}

async function generatePdf() {
  await ensureHandshake();
  const title = document.getElementById("reportTitle").value;
  const notes = document.getElementById("reportNotes").value;
  const reportType = document.getElementById("reportType").value;
  const payload = await jsonFetch(`${API_BASE}/5050/report/pdf`, {
    method: "POST",
    body: JSON.stringify({
      title,
      notes,
      report_type: reportType,
      include_plan: true,
      include_timeline: true
    })
  });
  const reportLink = document.getElementById("reportLink");
  reportLink.href = `${API_BASE}/5050/file?path=${encodeURIComponent(payload.report_path)}`;
  reportLink.textContent = payload.report_path;
  reportLink.classList.remove("hidden");

  const pdfLink = document.getElementById("pdfLink");
  pdfLink.href = `${API_BASE}/5050/file?path=${encodeURIComponent(payload.pdf_path)}`;
  pdfLink.textContent = payload.pdf_path;
  pdfLink.classList.remove("hidden");
}

async function copyContinueCommand() {
  const command = (await generateContinueCommand()).trim();
  if (!command) return;
  await navigator.clipboard.writeText(command);
  alert("Command copied. Paste into Cursor chat and run.");
}

async function refreshAll() {
  try {
    await Promise.all([loadSession(), loadTimeline(), generateContinueCommand()]);
  } catch (err) {
    console.error(err);
    alert(`Dashboard refresh failed: ${err.message}`);
  }
}

// ========== Self-Explorer Panel ==========

let explorerPollId = null;

async function startExplorer() {
  await ensureHandshake();
  const data = await jsonFetch(`${API_BASE}/self-explorer/start`, {
    method: "POST",
    body: JSON.stringify({ max_steps: 20 })
  });
  updateExplorerUI(data);
  if (!explorerPollId) explorerPollId = setInterval(pollExplorer, 2000);
}

async function stopExplorer() {
  await jsonFetch(`${API_BASE}/self-explorer/stop`, { method: "POST" });
}

async function nudgeExplorer() {
  const msg = document.getElementById("nudgeInput").value.trim();
  if (!msg) return;
  await jsonFetch(`${API_BASE}/self-explorer/nudge`, {
    method: "POST",
    body: JSON.stringify({ message: msg })
  });
  document.getElementById("nudgeInput").value = "";
}

async function pollExplorer() {
  try {
    const [status, journal] = await Promise.all([
      jsonFetch(`${API_BASE}/self-explorer/status`),
      jsonFetch(`${API_BASE}/self-explorer/journal?limit=30`)
    ]);
    updateExplorerUI(status);
    renderJournal(journal.entries);
    if (!status.running && explorerPollId) {
      clearInterval(explorerPollId);
      explorerPollId = null;
    }
  } catch (e) {
    // Server not running or explorer not initialized — silent
  }
}

function updateExplorerUI(status) {
  const badge = document.getElementById("explorerBadge");
  if (status.running) {
    badge.textContent = "running";
    badge.style.background = "#0a0";
  } else if (status.step_count > 0) {
    badge.textContent = "stopped";
    badge.style.background = "#a50";
  } else {
    badge.textContent = "offline";
    badge.style.background = "#555";
  }
  const stats = document.getElementById("explorerStats");
  stats.innerHTML = [
    `<span class="pill">step ${status.step_count || 0}</span>`,
    `<span class="pill">files ${status.files_explored || 0}</span>`,
    `<span class="pill">docs ${status.docs_written || 0}</span>`,
    `<span class="pill">journal ${status.journal_entries || 0}</span>`,
    status.current_file ? `<span class="pill">${status.current_file}</span>` : "",
    status.scientific_name ? `<span class="pill">${status.scientific_name}</span>` : "",
  ].join(" ");
}

function renderJournal(entries) {
  const el = document.getElementById("explorerJournal");
  const wasAtBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 40;
  el.innerHTML = entries.map(e => {
    const ts = e.timestamp ? e.timestamp.split("T")[1]?.slice(0, 8) : "";
    const type = e.type || "?";
    const content = e.content || e.observation || e.message || JSON.stringify(e).slice(0, 200);
    const file = e.file ? ` [${e.file}]` : "";
    const color = type === "Musing" ? "#ff0" : type === "Reflection" ? "#0ff" : "#0f0";
    return `<span style="color:${color}">[${ts}] ${type}${file}</span>\n${content}\n`;
  }).join("\n");
  if (wasAtBottom) el.scrollTop = el.scrollHeight;
}

document.getElementById("startExplorerBtn").addEventListener("click", startExplorer);
document.getElementById("stopExplorerBtn").addEventListener("click", stopExplorer);
document.getElementById("nudgeBtn").addEventListener("click", nudgeExplorer);

// Poll once on load to pick up running state
pollExplorer();

// ========== Original Dashboard ==========

document.getElementById("refreshBtn").addEventListener("click", refreshAll);
document.getElementById("continueBtn").addEventListener("click", copyContinueCommand);
document.getElementById("generateReportBtn").addEventListener("click", generateReport);
document.getElementById("generatePdfBtn").addEventListener("click", generatePdf);
document.getElementById("printBtn").addEventListener("click", () => window.print());
document.getElementById("templateSelect").addEventListener("change", generateContinueCommand);

refreshAll();
