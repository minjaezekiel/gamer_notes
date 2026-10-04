#!/usr/bin/env node
/* =============================================================================
   check_pages.js — verify every HTML page in the course actually works.

   Four checks:
     1. Standalone .js files parse            (node --check)
     2. Inline <script> blocks parse          (new Function, no execution)
     3. Each page LOADS IN REAL CHROME with no console errors and no uncaught
        exceptions, and any page calling Anim.sketch() really produced a canvas
        plus its controls. Headless Chrome reports page console output and
        uncaught errors on stderr as "INFO:CONSOLE" lines, which is what makes
        this check meaningful rather than cosmetic.
     4. Every relative link in .md and .html resolves to a real file.

   Usage:
     node tools/check_pages.js                  everything
     node tools/check_pages.js --quick          skip Chrome (fast)
     node tools/check_pages.js --only tilemap   only paths containing "tilemap"
     node tools/check_pages.js --jobs 8         Chrome parallelism (default 4)
   ========================================================================== */

'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');
const { execFileSync, spawn } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const argv = process.argv.slice(2);
const flag = (name, dflt) => { const i = argv.indexOf(name); return i >= 0 ? argv[i + 1] : dflt; };
const QUICK = argv.includes('--quick');
const ONLY = flag('--only', null);
const JOBS = Math.max(1, Number(flag('--jobs', 4)));

// templates/ holds {{PLACEHOLDER}} paths that only resolve once a lesson is
// scaffolded from them, so they are not checked here.
const SKIP_DIRS = new Set(['.git', 'node_modules', '__pycache__', '.build',
                           'handouts', 'templates']);

let fails = 0, checked = 0;
const rel = f => path.relative(ROOT, f);
const fail = (f, msg) => { fails++; console.log(`  FAIL  ${rel(f)}\n        ${msg}`); };
const ok = (f, note) => { console.log(`  ok    ${rel(f)}${note ? '  (' + note + ')' : ''}`); };

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.isDirectory()) { if (!SKIP_DIRS.has(e.name)) walk(path.join(dir, e.name), out); }
    else out.push(path.join(dir, e.name));
  }
  return out;
}
const allFiles = walk(ROOT);
const pick = ext => allFiles.filter(f => f.endsWith(ext) && (!ONLY || f.includes(ONLY))).sort();

/* ---- 1. standalone JS ---------------------------------------------------- */
console.log('\n== JavaScript files ==');
for (const f of pick('.js')) {
  if (f.includes(path.sep + 'tools' + path.sep)) continue;
  checked++;
  try { execFileSync(process.execPath, ['--check', f], { stdio: 'pipe' }); ok(f); }
  catch (e) { fail(f, String(e.stderr || e.message).split('\n').slice(0, 4).join('\n        ')); }
}

/* ---- 2. inline scripts --------------------------------------------------- */
console.log('\n== Inline scripts in HTML ==');
const htmlFiles = pick('.html');
for (const f of htmlFiles) {
  const src = fs.readFileSync(f, 'utf8');
  const blocks = [...src.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi)];
  if (!blocks.length) continue;
  checked++;
  let bad = null;
  blocks.forEach((b, i) => {
    if (bad) return;
    try { new Function(b[1]); } catch (e) { bad = `block ${i + 1}: ${e.message}`; }
  });
  bad ? fail(f, bad) : ok(f, `${blocks.length} inline block(s)`);
}

/* ---- 3. real Chrome load, N pages at a time ------------------------------ */
function chromeCheck(file, profileDir) {
  return new Promise(resolve => {
    const base = path.basename(file, '.html');
    const domPath = path.join(profileDir, base + '.dom');
    const logPath = path.join(profileDir, base + '.log');
    const fdOut = fs.openSync(domPath, 'w');
    const fdErr = fs.openSync(logPath, 'w');
    const child = spawn(CHROME, [
      '--headless', '--disable-gpu', '--no-sandbox', '--no-first-run',
      // Each page gets its own profile dir so parallel Chromes do not fight.
      '--user-data-dir=' + path.join(profileDir, base),
      '--enable-logging=stderr', '--v=1',
      '--virtual-time-budget=2500',
      '--dump-dom', 'file://' + file
    ], { stdio: ['ignore', fdOut, fdErr] });

    const timer = setTimeout(() => child.kill('SIGKILL'), 45000);
    child.on('close', () => {
      clearTimeout(timer);
      try { fs.closeSync(fdOut); } catch (e) {}
      try { fs.closeSync(fdErr); } catch (e) {}
      const dom = fs.existsSync(domPath) ? fs.readFileSync(domPath, 'utf8') : '';
      const log = fs.existsSync(logPath) ? fs.readFileSync(logPath, 'utf8') : '';
      const src = fs.readFileSync(file, 'utf8');

      if (!dom.trim()) { return resolve({ file, err: 'Chrome returned an empty DOM' }); }

      // Page console output and uncaught exceptions. macOS GPU / display-link
      // noise is about the host, not the page, so it is not matched here.
      const noisy = log.split('\n').filter(l => /INFO:CONSOLE|WARNING:CONSOLE|Uncaught/.test(l));
      if (noisy.length) {
        return resolve({ file, err: 'console output on load:\n        ' +
          noisy.slice(0, 4).map(s => s.trim()).join('\n        ') });
      }

      if (/Anim\.sketch\s*\(/.test(src)) {
        // A sketch with an update() animates and so must offer play + step +
        // reset. A purely interactive one has nothing to step, and needs only
        // reset. See docs/COURSE_SPEC.md section 10.
        const animates = /\n\s*update:\s*function/.test(src);
        const need = animates ? 3 : 1;
        const btns = (dom.match(/anim-btn/g) || []).length;
        if (!dom.includes('anim-canvas')) {
          return resolve({ file, err: 'calls Anim.sketch() but rendered no .anim-canvas' });
        }
        if (btns < need) {
          return resolve({ file, err: `only ${btns} control button(s); ` +
            (animates ? 'this sketch animates, so it needs play/step/reset'
                      : 'expected at least a Reset button') });
        }
        return resolve({ file, note: `canvas + ${btns} controls` });
      }
      resolve({ file, note: null });
    });
  });
}

async function runChrome() {
  if (QUICK) return;
  if (!fs.existsSync(CHROME)) {
    console.log('\n== Chrome load ==\n  SKIPPED: Chrome not found at ' + CHROME);
    return;
  }
  console.log(`\n== Chrome load (console errors + sketch init), ${JOBS} at a time ==`);
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'gdb-chrome-'));
  const queue = htmlFiles.slice();
  const results = [];
  async function worker() {
    while (queue.length) {
      const f = queue.shift();
      results.push(await chromeCheck(f, profile));
    }
  }
  await Promise.all(Array.from({ length: Math.min(JOBS, queue.length) }, worker));
  results.sort((a, b) => a.file.localeCompare(b.file));
  for (const r of results) {
    checked++;
    r.err ? fail(r.file, r.err) : ok(r.file, r.note);
  }
  fs.rmSync(profile, { recursive: true, force: true });
}

/* ---- 4. relative links --------------------------------------------------- */
function checkLinks() {
  console.log('\n== Relative links ==');
  const targets = [];
  for (const f of [...htmlFiles, ...pick('.md')]) {
    const src = fs.readFileSync(f, 'utf8');
    const dir = path.dirname(f);
    const found = [];
    if (f.endsWith('.html')) {
      for (const m of src.matchAll(/(?:href|src)\s*=\s*"([^"]+)"/g)) found.push(m[1]);
    } else {
      // Strip fenced code blocks and inline code spans first. A link inside one
      // is an EXAMPLE being shown to the reader (often written from a different
      // folder's point of view), not a link this file actually makes.
      const prose = src
        .replace(/```[\s\S]*?```/g, '')
        .replace(/`[^`\n]*`/g, '');
      for (const m of prose.matchAll(/\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g)) found.push(m[1]);
    }
    for (const raw of found) {
      if (/^(https?:|mailto:|#|data:|javascript:)/i.test(raw)) continue;
      const clean = raw.split('#')[0].split('?')[0];
      if (!clean) continue;
      targets.push({ from: f, target: path.resolve(dir, clean) });
    }
  }
  let broken = 0;
  for (const { from, target } of targets) {
    if (!fs.existsSync(target)) { broken++; fail(from, 'broken link -> ' + rel(target)); }
  }
  if (!broken) console.log(`  ok    all ${targets.length} relative links resolve`);
  return targets.length;
}

(async () => {
  await runChrome();
  const nLinks = checkLinks();
  console.log('\n' + '-'.repeat(62));
  console.log(fails === 0
    ? `PASS  ${checked} checks, ${nLinks} links, no problems found.`
    : `FAIL  ${fails} problem(s) found across ${checked} checks.`);
  process.exit(fails === 0 ? 0 : 1);
})();
