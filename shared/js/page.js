/* =============================================================================
   page.js — small per-page behaviour shared by every HTML page in the course.

   Right now that is just the light/dark override button. It lives in its own
   file so that no lesson page has to repeat it, and so that a teacher who wants
   to force one theme for a projector can change one place.
   ========================================================================== */

(function () {
  'use strict';

  var KEY = 'gdb-theme';

  /* Apply a saved preference as early as possible. Every storage access is
     wrapped: localStorage THROWS, not just returns null, in a private window or
     when site data is blocked, and an exception here would stop the rest of the
     page from running. */
  function saved() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function remember(v) {
    try { localStorage.setItem(KEY, v); } catch (e) { /* nothing we can do */ }
  }

  var pref = saved();
  if (pref === 'dark' || pref === 'light') {
    document.documentElement.setAttribute('data-theme', pref);
  }

  function build() {
    // A page can opt out by setting data-no-theme-toggle on <body>.
    if (document.body.hasAttribute('data-no-theme-toggle')) { return; }
    if (document.querySelector('.theme-toggle')) { return; }  // page made its own

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'theme-toggle';
    btn.textContent = 'Light / Dark';
    btn.title = 'Switch between light and dark colours';
    document.body.appendChild(btn);

    btn.addEventListener('click', function () {
      var now = document.documentElement.getAttribute('data-theme');
      // If nothing is forced yet, work out what the OS is currently giving us so
      // that the first click flips to the opposite of what the reader sees.
      if (!now) {
        now = window.matchMedia &&
              window.matchMedia('(prefers-color-scheme: dark)').matches
          ? 'dark' : 'light';
      }
      var next = now === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      remember(next);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
}());
