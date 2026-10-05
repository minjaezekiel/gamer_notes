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
const http = require('http');
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
                           'handouts', 'templates',
                           /* tools/.venv holds pygame-ce for the verification
                              scripts. It ships thousands of files, including
                              pygame's own HTML docs, and none of it is course
                              content. */
                           '.venv']);

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
  // HTML comments are stripped first. Several lesson files explain script tags
  // INSIDE a comment, and the word <script> in prose would otherwise be read as
  // the start of a real block, making the following English into "JavaScript".
  const src = fs.readFileSync(f, 'utf8').replace(/<!--[\s\S]*?-->/g, '');
  const blocks = [...src.matchAll(/<script((?![^>]*\bsrc=)[^>]*)>([\s\S]*?)<\/script>/gi)];
  if (!blocks.length) continue;
  checked++;
  let bad = null;
  blocks.forEach((b, i) => {
    if (bad) return;
    const isModule = /type\s*=\s*["']module["']/.test(b[1]);
    try {
      if (isModule) {
        // new Function() refuses `import`, so a module block goes through
        // node --check instead, which accepts module syntax.
        const tmp = path.join(os.tmpdir(), 'gdb-mod-' + process.pid + '-' + i + '.mjs');
        fs.writeFileSync(tmp, b[2]);
        try { execFileSync(process.execPath, ['--check', tmp], { stdio: 'pipe' }); }
        finally { fs.rmSync(tmp, { force: true }); }
      } else {
        new Function(b[2]);
      }
    } catch (e) {
      const msg = (e.stderr ? e.stderr.toString() : e.message)
        .split('\n').filter(l => /Error|\^/.test(l)).slice(0, 2).join(' ').trim();
      bad = `block ${i + 1}: ${msg || e.message}`;
    }
  });
  bad ? fail(f, bad) : ok(f, `${blocks.length} inline block(s)`);
}

/* ---- a local static server, for ES module pages --------------------------
   A browser refuses to `import` across a file:// URL: each local file counts
   as its own origin, so the import is blocked as a cross-origin request. That
   is not a bug in the lesson, it is the security model, and it means any page
   using <script type="module"> has to be SERVED to be tested honestly.

   So: if any page uses modules, we start a 40-line static server here and load
   those pages over http://127.0.0.1. Everything else still loads from file://,
   because that is how a student will open it.
   ---------------------------------------------------------------------- */
const MIME = {
  '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.md': 'text/plain', '.txt': 'text/plain'
};

function startServer() {
  return new Promise(resolve => {
    const server = http.createServer((req, res) => {
      const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/, '');
      const full = path.resolve(ROOT, rel);
      // Never serve anything outside the repository.
      if (!full.startsWith(ROOT) || !fs.existsSync(full) || fs.statSync(full).isDirectory()) {
        res.writeHead(404); return res.end('not found');
      }
      res.writeHead(200, { 'Content-Type': MIME[path.extname(full)] || 'application/octet-stream' });
      fs.createReadStream(full).pipe(res);
    });
    server.listen(0, '127.0.0.1', () => resolve({
      port: server.address().port,
      close: () => server.close()
    }));
  });
}

const usesModules = file => /<script[^>]+type\s*=\s*["']module["']/.test(fs.readFileSync(file, 'utf8'));

function pageUrl(file, port) {
  /* ?selftest=N asks anim.js to step N frames on load, then flip every toggle
     and push every slider to both ends. Without it, loading a page only proves
     the first frame drew - a crash on frame 40, or one that needs a slider at
     its minimum, would go unseen. See the SELF TEST block in shared/js/anim.js. */
  const q = /Anim\.sketch\s*\(/.test(fs.readFileSync(file, 'utf8')) ? '?selftest=90' : '';
  if (port && usesModules(file)) {
    return 'http://127.0.0.1:' + port + '/' +
           path.relative(ROOT, file).split(path.sep).map(encodeURIComponent).join('/') + q;
  }
  return 'file://' + file + q;
}

/* ---- 3. real Chrome load, N pages at a time ------------------------------ */
function chromeCheck(file, profileDir, port) {
  return new Promise(resolve => {
    // Two examples can both be called index.html, so the scratch file name is
    // built from the whole relative path rather than just the basename.
    const base = rel(file).replace(/[^A-Za-z0-9]+/g, '_');
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
      '--dump-dom', pageUrl(file, port)
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
      const noisy = log.split('\n')
        .filter(l => /INFO:CONSOLE|WARNING:CONSOLE|ERROR:CONSOLE|Uncaught/.test(l));
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
  const modulePages = htmlFiles.filter(usesModules);
  const srv = modulePages.length ? await startServer() : null;
  console.log(`\n== Chrome load (console errors + sketch init), ${JOBS} at a time ==`);
  if (srv) {
    console.log(`  ${modulePages.length} page(s) use ES modules and are served over ` +
                `http://127.0.0.1:${srv.port} — file:// cannot import.`);
  }
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'gdb-chrome-'));
  const queue = htmlFiles.slice();
  const results = [];
  async function worker() {
    while (queue.length) {
      const f = queue.shift();
      results.push(await chromeCheck(f, profile, srv ? srv.port : null));
    }
  }
  await Promise.all(Array.from({ length: Math.min(JOBS, queue.length) }, worker));
  results.sort((a, b) => a.file.localeCompare(b.file));
  for (const r of results) {
    checked++;
    const note = [r.note, srv && usesModules(r.file) ? 'served' : null]
      .filter(Boolean).join(', ');
    r.err ? fail(r.file, r.err) : ok(r.file, note || null);
  }
  fs.rmSync(profile, { recursive: true, force: true });
  if (srv) { srv.close(); }
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
