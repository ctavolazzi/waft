/* Drive every instrument the way a reader would, and assert the state it lands in. */
const { launch } = require('./cdp');
const PAGE = 'file://' + require('path').resolve(__dirname, '..', 'index.html');

const results = [];
const check = (name, pass, detail) => {
  results.push({ name, pass, detail });
  console.log(`${pass ? ' PASS' : '*FAIL'}  ${name}${detail ? '  — ' + detail : ''}`);
};

(async () => {
  const b = await launch({ width: 1440, height: 950 });
  try {
    await b.goto(PAGE);
    await b.eval(() => { document.documentElement.style.scrollBehavior = 'auto'; });

    /* ---------- GENOME LAB ---------- */
    await b.eval(() => document.querySelector('.genome-lab').scrollIntoView({ block: 'center' }));
    await b.sleep(500);
    const before = await b.eval(() => ({
      cur: document.getElementById('gl-current').textContent,
      par: document.getElementById('gl-parent').textContent,
      adopt: document.getElementById('gl-adopt').disabled,
    }));
    check('genome lab computes a 64-char digest', before.cur.length === 64, before.cur.slice(0, 16) + '…');
    check('genome lab starts identical to parent', before.cur === before.par && before.adopt === true);

    // mutate the organism
    await b.eval(() => {
      const ta = document.getElementById('gl-code');
      ta.value = ta.value.replace('0.7', '0.9');
      ta.dispatchEvent(new Event('input', { bubbles: true }));
    });
    await b.sleep(1100);
    const after = await b.eval(() => ({
      cur: document.getElementById('gl-current').textContent,
      status: document.getElementById('gl-status').textContent,
      cls: document.getElementById('gl-status').className,
      ticks: document.querySelectorAll('#gl-diffbar i.on').length,
      adopt: document.getElementById('gl-adopt').disabled,
    }));
    check('one edit produces a different genome', after.cur !== before.cur && after.cur.length === 64,
      after.cur.slice(0, 16) + '…');
    check('status flips to MUTATED', after.cls.includes('mutated'), after.status);
    check('byte-diff strip lights up', after.ticks > 0, after.ticks + '/32 bytes diverged');
    check('adopt button enables on mutation', after.adopt === false);

    // adopt: child becomes the new parent
    await b.eval(() => document.getElementById('gl-adopt').click());
    await b.sleep(900);
    const adopted = await b.eval(() => ({
      par: document.getElementById('gl-parent').textContent,
      cur: document.getElementById('gl-current').textContent,
      gen: document.getElementById('gl-gen').textContent,
      cls: document.getElementById('gl-status').className,
    }));
    check('adopt promotes child to parent', adopted.par === adopted.cur && adopted.cls.includes('same'));
    check('adopt advances the generation counter', adopted.gen === '1', 'gen ' + adopted.gen);

    // digest must match the real SHA-256 of the textarea contents
    const trusted = await b.eval(async () => {
      const t = document.getElementById('gl-code').value;
      const d = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(t));
      return [...new Uint8Array(d)].map(x => x.toString(16).padStart(2, '0')).join('');
    });
    check('displayed digest is the true SHA-256 of the source', trusted === adopted.cur);

    /* ---------- STABILIZATION CHAMBER ---------- */
    await b.eval(() => document.querySelector('.chamber').scrollIntoView({ block: 'center' }));
    await b.sleep(900);
    const ch0 = await b.eval(() => ({
      type: document.getElementById('ch-type').textContent,
      opts: document.querySelectorAll('#ch-options .ch-opt').length,
      art: document.getElementById('ch-artifact').textContent.length,
    }));
    check('chamber loads a fracture with options', ch0.opts === 3 && ch0.art > 20, ch0.type);

    // the artifact must actually be corrupting itself frame to frame
    const glitching = await b.eval(async () => {
      const el = document.getElementById('ch-artifact');
      const a = el.textContent;
      await new Promise(r => setTimeout(r, 400));
      return a !== el.textContent;
    });
    check('open fracture visibly corrupts the artifact', glitching);

    // answer round 1 correctly
    await b.eval(() => {
      const opts = [...document.querySelectorAll('#ch-options .ch-opt')];
      opts.find(o => o.textContent.includes('"efficiency"]}')).click();
    });
    await b.sleep(1000);
    const ch1 = await b.eval(() => ({
      energy: document.getElementById('ch-energy').textContent,
      sealed: document.getElementById('ch-artifact').className.includes('sealed'),
      right: document.querySelectorAll('#ch-options .ch-opt.right').length,
      feedback: document.getElementById('ch-feedback').textContent.slice(0, 30),
    }));
    check('correct answer seals the artifact', ch1.sealed && ch1.right === 1);
    check('correct answer pays scint energy', ch1.energy.startsWith('4'), ch1.energy);

    // round 2, answer wrong
    await b.sleep(2200);
    const r2 = await b.eval(() => document.getElementById('ch-round').textContent);
    check('chamber advances to the next fracture', r2 === '2 / 4', r2);
    await b.eval(() => {
      const opts = [...document.querySelectorAll('#ch-options .ch-opt')];
      opts.find(o => o.textContent.includes('Safety 0.40')).click();
    });
    await b.sleep(1100);
    const ch2 = await b.eval(() => ({
      integrity: document.getElementById('ch-integrity').textContent,
      wrong: document.querySelectorAll('#ch-options .ch-opt.wrong').length,
      barWidth: document.getElementById('ch-bar').style.width,
    }));
    check('wrong answer costs integrity', parseFloat(ch2.integrity) < 1,
      ch2.integrity + ' (bar ' + ch2.barWidth + ')');
    check('wrong option is marked', ch2.wrong === 1);

    /* ---------- SCAFFOLD ---------- */
    await b.eval(() => document.querySelector('.pyrite-grid').scrollIntoView({ block: 'center' }));
    await b.sleep(2600);
    const sc = await b.eval(() => ({
      lines: document.querySelectorAll('#scaffold-tree li').length,
      shown: document.querySelectorAll('#scaffold-tree li.in').length,
    }));
    check('scaffold streams the _pyrite tree', sc.lines === 14 && sc.shown > 4,
      sc.shown + '/' + sc.lines + ' lines revealed');

    /* ---------- THE TABLE (d20) ---------- */
    await b.eval(() => document.getElementById('d20').scrollIntoView({ block: 'center' }));
    await b.sleep(2400);
    const t1 = await b.eval(() => ({
      rows: document.querySelectorAll('#roll-log li').length,
      rolls: document.getElementById('k-rolls').textContent,
      face: document.getElementById('d20-num').textContent,
    }));
    check('d20 auto-rolls once on arrival', t1.rows >= 1 && t1.rolls === '1',
      'face ' + t1.face + ', ' + t1.rows + ' log row(s)');

    // the face must change mid-tumble
    const tumbles = await b.eval(async () => {
      const num = document.getElementById('d20-num');
      document.getElementById('d20').click();
      await new Promise(r => setTimeout(r, 120));
      const a = num.textContent;
      await new Promise(r => setTimeout(r, 200));
      const b2 = num.textContent;
      await new Promise(r => setTimeout(r, 1400));
      return { changed: a !== b2, settled: num.textContent, rolling: document.getElementById('d20').className };
    });
    check('die tumbles before settling', tumbles.changed, 'settled on ' + tumbles.settled);
    check('roll clears the rolling state', !tumbles.rolling.includes('rolling'));

    const t2 = await b.eval(() => ({
      rows: document.querySelectorAll('#roll-log li').length,
      rolls: document.getElementById('k-rolls').textContent,
      scint: document.getElementById('k-scint').textContent,
      last: (document.querySelector('#roll-log li') || {}).textContent || '',
    }));
    check('second roll appends to the quest log', t2.rolls === '2' && t2.rows === 2,
      t2.rolls + ' rolls, ' + t2.scint);
    check('log line carries a karma type',
      /ORDER|CHAOS|STABILIZATION|DESTRUCTION/.test(t2.last), t2.last.slice(0, 78));

    /* ---------- NAV ---------- */
    await b.eval(() => document.getElementById('pantheon').scrollIntoView({ block: 'start' }));
    await b.sleep(400);
    const nav = await b.eval(() => ({
      here: (document.querySelector('.topbar-nav a.here') || {}).textContent || 'none',
      progress: document.getElementById('progress').style.transform,
    }));
    check('nav highlights the section you are in', nav.here.includes('PANTHEON'), nav.here);
    check('read-progress rail tracks scroll', /scaleX\(0\.[3-9]/.test(nav.progress), nav.progress);

    console.log('\n--- console/page errors ---');
    console.log(b.logs.length ? b.logs.join('\n') : 'NONE');
    const failed = results.filter(r => !r.pass).length;
    console.log(`\n${results.length - failed}/${results.length} checks passed`);
    process.exitCode = failed || b.logs.length ? 1 : 0;
  } finally {
    await b.close();
  }
})().catch(e => { console.error('DRIVER FAIL:', e.message); process.exit(1); });
