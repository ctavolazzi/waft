/* With prefers-reduced-motion: reduce, nothing should move, but every widget
   must still land on a readable finished state (not blank, not mid-animation). */
const { launch } = require('./cdp');
const PAGE = 'file://' + require('path').resolve(__dirname, '..', 'index.html');

const out = [];
const check = (n, pass, d) => { out.push(pass); console.log(`${pass ? ' PASS' : '*FAIL'}  ${n}${d ? '  — ' + d : ''}`); };

(async () => {
  const b = await launch({ width: 1440, height: 950 });
  try {
    await b.setMedia([{ name: 'prefers-reduced-motion', value: 'reduce' }]);
    await b.goto(PAGE);
    check('page reports reduced motion',
      await b.eval(() => matchMedia('(prefers-reduced-motion: reduce)').matches));

    await b.eval(() => {
      document.documentElement.style.scrollBehavior = 'auto';
      return new Promise(done => {
        let y = 0;
        const step = () => {
          window.scrollTo(0, y); y += 400;
          if (y < document.documentElement.scrollHeight) setTimeout(step, 40);
          else { window.scrollTo(0, 0); setTimeout(done, 900); }
        };
        step();
      });
    });

    const s = await b.eval(() => ({
      digest: document.getElementById('gl-current').textContent.length,
      chamberOpts: document.querySelectorAll('#ch-options .ch-opt').length,
      chamberArt: document.getElementById('ch-artifact').textContent.length,
      glitched: document.querySelectorAll('#ch-artifact .g.on').length,
      scaffold: document.querySelectorAll('#scaffold-tree li.in').length,
      phyloGrown: document.querySelectorAll('#fig-phylo .grown').length,
      stackUp: document.querySelectorAll('#fig-stack .layer.up').length,
      figLit: document.querySelectorAll('#fig-genome .lit').length,
      simRunning: document.getElementById('sim-status').textContent,
      simPop: document.getElementById('r-pop').textContent,
      dish: (() => { const c = document.getElementById('dish');
        const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
        let n = 0; for (let i = 3; i < d.length; i += 4) if (d[i] > 8) n++;
        return (n / (d.length / 4) * 100).toFixed(1) + '%'; })(),
    }));

    check('genome lab still shows a full digest', s.digest === 64);
    check('chamber still renders a fracture', s.chamberOpts === 3 && s.chamberArt > 20);
    check('artifact is NOT corrupting itself', s.glitched === 0, s.glitched + ' glitched chars');
    check('scaffold tree is fully written out', s.scaffold === 14, s.scaffold + '/14');
    // 11 branches + 8 live nodes + 3 death marks + 3 labels + 1 champion
    check('phylo tree is fully grown', s.phyloGrown === 26, s.phyloGrown + ' elements');
    check('stack is fully assembled', s.stackUp === 5, s.stackUp + '/5 layers');
    check('FIG 01 rests in its finished state', s.figLit >= 6, s.figLit + ' lit elements');
    check('simulation auto-pauses', s.simRunning.includes('PAUSED'), s.simRunning);
    check('dish still painted a population', parseFloat(s.dish) > 5 && s.simPop === '12', s.dish);

    console.log('\nerrors:', b.logs.length ? b.logs.join('\n') : 'NONE');
    const bad = out.filter(x => !x).length;
    console.log(`${out.length - bad}/${out.length} checks passed`);
    process.exitCode = bad ? 1 : 0;
  } finally { await b.close(); }
})().catch(e => { console.error('DRIVER FAIL:', e.message); process.exit(1); });
