/* Minimal Chrome DevTools Protocol driver — no npm deps, Node 22 native WebSocket.
   Launches headless Chrome, exposes eval/screenshot, collects console + page errors. */
const { spawn } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function launch({ port, width = 1440, height = 900 } = {}) {
  // a fixed port silently reconnects to a leftover browser from a previous run,
  // whose window may be occluded — every animation then reads as frozen
  if (!port) port = 10000 + Math.floor(Math.random() * 40000);
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'waft-cdp-'));
  const proc = spawn(CHROME, [
    '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
    '--hide-scrollbars', '--force-device-scale-factor=1', '--allow-file-access-from-files',
    // keep rAF + timers running: a backgrounded renderer silently freezes
    // every animation and stops IntersectionObserver from ever firing
    '--disable-background-timer-throttling', '--disable-renderer-backgrounding',
    '--disable-backgrounding-occluded-windows', '--disable-features=CalculateNativeWinOcclusion',
    `--user-data-dir=${profile}`, `--remote-debugging-port=${port}`,
    `--window-size=${width},${height}`, 'about:blank',
  ], { stdio: ['ignore', 'ignore', 'ignore'], detached: true });

  let target = null;
  for (let i = 0; i < 60 && !target; i++) {
    await sleep(250);
    try {
      const list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
      target = list.find(t => t.type === 'page' && t.webSocketDebuggerUrl);
    } catch (_) { /* not up yet */ }
  }
  if (!target) { proc.kill(); throw new Error('Chrome did not expose a debug target'); }

  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((res, rej) => {
    ws.addEventListener('open', res, { once: true });
    ws.addEventListener('error', rej, { once: true });
  });

  let seq = 0;
  const pending = new Map();
  const events = [];
  const waiters = [];

  ws.addEventListener('message', (m) => {
    const msg = JSON.parse(m.data);
    if (msg.id != null) {
      const p = pending.get(msg.id);
      if (!p) return;
      pending.delete(msg.id);
      msg.error ? p.rej(new Error(msg.error.message)) : p.res(msg.result);
      return;
    }
    events.push(msg);
    for (let i = waiters.length - 1; i >= 0; i--) {
      if (waiters[i].match(msg)) { waiters[i].res(msg); waiters.splice(i, 1); }
    }
  });

  const send = (method, params = {}) => new Promise((res, rej) => {
    const id = ++seq;
    pending.set(id, { res, rej });
    ws.send(JSON.stringify({ id, method, params }));
  });

  const waitFor = (method, timeout = 30000) => new Promise((res, rej) => {
    const hit = events.find(e => e.method === method);
    if (hit) return res(hit);
    const w = { match: e => e.method === method, res };
    waiters.push(w);
    setTimeout(() => {
      const i = waiters.indexOf(w);
      if (i >= 0) { waiters.splice(i, 1); rej(new Error('timeout waiting for ' + method)); }
    }, timeout);
  });

  const logs = [];
  await send('Runtime.enable');
  await send('Page.enable');
  await send('Log.enable');
  // force the page to count as focused+visible so rAF and IntersectionObserver run
  try { await send('Emulation.setFocusEmulationEnabled', { enabled: true }); } catch (_) {}
  try { await send('Page.setWebLifecycleState', { state: 'active' }); } catch (_) {}
  ws.addEventListener('message', (m) => {
    const msg = JSON.parse(m.data);
    if (msg.method === 'Runtime.exceptionThrown') {
      const d = msg.params.exceptionDetails;
      logs.push(`PAGE_ERROR: ${d.exception?.description || d.text} @${d.lineNumber}:${d.columnNumber}`);
    }
    if (msg.method === 'Runtime.consoleAPICalled' && ['error', 'warning'].includes(msg.params.type)) {
      logs.push(`CONSOLE_${msg.params.type.toUpperCase()}: ` +
        msg.params.args.map(a => a.description || a.value).join(' '));
    }
    if (msg.method === 'Log.entryAdded' && ['error', 'warning'].includes(msg.params.entry.level)) {
      logs.push(`LOG_${msg.params.entry.level.toUpperCase()}: ${msg.params.entry.text}`);
    }
  });

  return {
    logs,
    async goto(url) {
      const loaded = waitFor('Page.loadEventFired');
      await send('Page.navigate', { url });
      await loaded;
      await sleep(400);
    },
    async eval(fn, ...args) {
      const expr = `(${fn.toString()}).apply(null, ${JSON.stringify(args)})`;
      const r = await send('Runtime.evaluate', {
        expression: expr, awaitPromise: true, returnByValue: true,
      });
      if (r.exceptionDetails) {
        throw new Error('eval threw: ' + (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
      }
      return r.result.value;
    },
    async screenshot(file, { fullPage = false } = {}) {
      const params = { format: 'png' };
      if (fullPage) params.captureBeyondViewport = true;
      const r = await send('Page.captureScreenshot', params);
      fs.writeFileSync(file, Buffer.from(r.data, 'base64'));
      return file;
    },
    async setMedia(features) {
      await send('Emulation.setEmulatedMedia', { features });
    },
    async setSize(width, height) {
      await send('Emulation.setDeviceMetricsOverride', {
        width, height, deviceScaleFactor: 1, mobile: false,
      });
    },
    sleep,
    async close() {
      try { ws.close(); } catch (_) {}
      // kill the whole group: Chrome forks helpers that keep the port bound
      try { process.kill(-proc.pid, 'SIGKILL'); } catch (_) { try { proc.kill('SIGKILL'); } catch (_) {} }
      await sleep(300);
      try { fs.rmSync(profile, { recursive: true, force: true }); } catch (_) {}
    },
  };
}

module.exports = { launch, sleep };
