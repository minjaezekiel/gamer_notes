/* =============================================================================
   codeblock.js — turns a plain <pre><code> into a lesson-grade code block.

   Adds: a language label, a filename, a copy button, line numbers, and
   highlighted lines. Plus small, dependency-free syntax colouring for the three
   languages this course uses.

   WHY WRITE OUR OWN HIGHLIGHTER instead of loading a library?
   Because lessons must work with the classroom Wi-Fi switched off. A CDN
   <script> tag is a lesson that fails on the one morning the network is down.
   This file is ~150 lines and good enough for teaching code.

   USAGE in a lesson page:

     <div class="code" data-lang="js" data-file="game.js" data-hl="4,7-9">
     <pre><code>... your code, with &lt; and &amp; escaped ...</code></pre>
     </div>

   Then include this file once at the end of the page. It upgrades every
   .code block automatically.
   ========================================================================== */

(function () {
  'use strict';

  /* Keyword lists. Deliberately short - only what the course actually uses, so
     a student is not distracted by colouring on words they have not met. */
  var KEYWORDS = {
    js: ['const', 'let', 'var', 'function', 'return', 'if', 'else', 'for', 'while',
         'break', 'continue', 'new', 'class', 'this', 'true', 'false', 'null',
         'undefined', 'of', 'in', 'typeof', 'import', 'export', 'default', 'switch',
         'case', 'try', 'catch', 'throw', 'async', 'await'],
    python: ['def', 'return', 'if', 'elif', 'else', 'for', 'while', 'break', 'continue',
             'import', 'from', 'as', 'class', 'self', 'True', 'False', 'None', 'and',
             'or', 'not', 'in', 'is', 'try', 'except', 'with', 'pass', 'global',
             'lambda', 'print', 'range', 'len'],
    cpp: ['int', 'float', 'double', 'char', 'bool', 'void', 'const', 'return', 'if',
          'else', 'for', 'while', 'do', 'break', 'continue', 'struct', 'class',
          'public', 'private', 'true', 'false', 'new', 'delete', 'using', 'namespace',
          'std', 'auto', 'unsigned', 'static', 'enum', 'switch', 'case', 'sizeof',
          'nullptr', 'this', 'include']
  };

  var ALIAS = {
    js: 'js', javascript: 'js', html: 'js', css: 'js',
    py: 'python', python: 'python',
    cpp: 'cpp', 'c++': 'cpp', c: 'cpp',
    bash: 'bash', sh: 'bash', text: null, txt: null, make: 'bash'
  };

  function escapeHtml(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  /* Highlight in ONE pass with an ordered alternation. Order matters a lot:
     comments and strings must be matched BEFORE anything else, otherwise a
     keyword inside a comment gets coloured as a keyword. That is the classic
     bug in hand-rolled highlighters. */
  function highlight(src, lang) {
    if (!lang) { return escapeHtml(src); }

    var kw = KEYWORDS[lang] || [];
    var parts = [];

    // 1. comments  2. strings  3. numbers  4. keywords
    var commentRe = lang === 'python' || lang === 'bash'
      ? '#[^\\n]*'
      : '\\/\\*[\\s\\S]*?\\*\\/|\\/\\/[^\\n]*';
    // In C++, a leading #include is a preprocessor directive, not a comment.
    var metaRe = lang === 'cpp' ? '^[ \\t]*#[a-z]+' : null;

    parts.push('(' + commentRe + ')');                                   // 1
    parts.push('("(?:\\\\.|[^"\\\\])*"|\'(?:\\\\.|[^\'\\\\])*\'|`(?:\\\\.|[^`\\\\])*`)'); // 2
    parts.push('(\\b0x[0-9a-fA-F]+\\b|\\b\\d+\\.?\\d*\\b)');             // 3
    parts.push(kw.length ? '(\\b(?:' + kw.join('|') + ')\\b)' : '()');   // 4
    parts.push(metaRe ? '(' + metaRe + ')' : '()');                      // 5

    var re = new RegExp(parts.join('|'), 'gm');
    var out = '';
    var last = 0;
    var m;
    while ((m = re.exec(src)) !== null) {
      // A zero-length match would loop forever. Guard against it.
      if (m[0] === '') { re.lastIndex++; continue; }
      out += escapeHtml(src.slice(last, m.index));
      var cls = m[1] ? 'tok-comment'
              : m[2] ? 'tok-string'
              : m[3] ? 'tok-number'
              : m[4] ? 'tok-keyword'
              : 'tok-meta';
      out += '<span class="' + cls + '">' + escapeHtml(m[0]) + '</span>';
      last = m.index + m[0].length;
    }
    out += escapeHtml(src.slice(last));
    return out;
  }

  /* "4,7-9" -> {4:true, 7:true, 8:true, 9:true} */
  function parseLines(spec) {
    var set = Object.create(null);
    if (!spec) { return set; }
    spec.split(',').forEach(function (chunk) {
      chunk = chunk.trim();
      if (!chunk) { return; }
      var dash = chunk.indexOf('-');
      if (dash > 0) {
        var a = parseInt(chunk.slice(0, dash), 10);
        var b = parseInt(chunk.slice(dash + 1), 10);
        for (var i = a; i <= b; i++) { set[i] = true; }
      } else {
        set[parseInt(chunk, 10)] = true;
      }
    });
    return set;
  }

  function upgrade(block) {
    if (block.dataset.ready === '1') { return; }
    var codeEl = block.querySelector('pre > code') || block.querySelector('pre');
    if (!codeEl) { return; }

    var raw = codeEl.textContent.replace(/\n+$/, '');
    var lang = ALIAS[(block.dataset.lang || '').toLowerCase()];
    var numbered = block.dataset.numbers !== 'off';
    var hl = parseLines(block.dataset.hl);

    /* ---- header ---- */
    if (block.dataset.lang || block.dataset.file) {
      var head = document.createElement('div');
      head.className = 'code-head';
      if (block.dataset.lang) {
        var l = document.createElement('span');
        l.className = 'code-lang';
        l.textContent = block.dataset.lang;
        head.appendChild(l);
      }
      if (block.dataset.file) {
        var f = document.createElement('span');
        f.className = 'code-file';
        f.textContent = block.dataset.file;
        head.appendChild(f);
      }
      var copy = document.createElement('button');
      copy.type = 'button';
      copy.className = 'code-copy';
      copy.textContent = 'Copy';
      copy.addEventListener('click', function () {
        navigator.clipboard.writeText(raw).then(function () {
          copy.textContent = 'Copied';
          setTimeout(function () { copy.textContent = 'Copy'; }, 1400);
        }, function () {
          copy.textContent = 'Press Ctrl+C';
        });
      });
      head.appendChild(copy);
      block.insertBefore(head, block.firstChild);
    }

    /* ---- body ---- */
    if (numbered) {
      var lines = raw.split('\n');
      var html = lines.map(function (line, i) {
        var n = i + 1;
        return '<span class="ln' + (hl[n] ? ' is-hl' : '') + '">' +
               '<span class="lnum">' + n + '</span>' +
               highlight(line, lang) +
               '</span>';
      }).join('\n');
      codeEl.innerHTML = html;
    } else {
      codeEl.innerHTML = highlight(raw, lang);
    }

    block.dataset.ready = '1';
  }

  function run() {
    document.querySelectorAll('.code').forEach(upgrade);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }

  window.CodeBlock = { upgrade: upgrade, run: run, highlight: highlight };
}());
