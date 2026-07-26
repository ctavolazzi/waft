const { launch } = require('./cdp');
const PAGE = 'file://' + require('path').resolve(__dirname, '..', 'index.html');

const fs = require('fs');
fs.mkdirSync(require('path').join(__dirname, 'shots'), { recursive: true });
const SHOTS = [
  ['hero', null],
  ['substrate', '#substrate'],
  ['genomelab', '.genome-lab'],
  ['chamber', '.chamber'],
  ['cycle', '#cycle'],
  ['recorder', '#recorder'],
  ['memory', '.pyrite-grid'],
  ['pantheon', '.pantheon-grid'],
  ['table', '.table-widget'],
];

(async () => {
  const b = await launch({ width: 1440, height: 950 });
  try {
    await b.goto(PAGE);
    await b.eval(() => { document.documentElement.style.scrollBehavior = 'auto'; });
    // let every widget boot
    await b.eval(() => new Promise(done => {
      let y = 0;
      const step = () => {
        window.scrollTo(0, y);
        y += 400;
        if (y < document.documentElement.scrollHeight) setTimeout(step, 40);
        else { window.scrollTo(0, 0); setTimeout(done, 500); }
      };
      step();
    }));
    for (const [name, sel] of SHOTS) {
      if (sel) {
        await b.eval((s) => {
          const el = document.querySelector(s);
          const y = el.getBoundingClientRect().top + window.scrollY - 90;
          window.scrollTo(0, y);
        }, sel);
      } else {
        await b.eval(() => window.scrollTo(0, 0));
      }
      await b.sleep(1400);
      await b.screenshot(require('path').join(__dirname, 'shots', `${name}.png`));
      console.log('shot-' + name + '.png');
    }
    console.log('errors:', b.logs.length ? b.logs.join('\n') : 'NONE');
  } finally { await b.close(); }
})().catch(e => { console.error('FAIL:', e.message); process.exit(1); });
