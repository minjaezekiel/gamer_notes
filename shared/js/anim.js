/* =============================================================================
   anim.js — a tiny teaching-animation library for the Game Dev Bootcamp.

   WHY THIS FILE EXISTS
   Every concept visualizer in this course needs the same four things:
     play, pause, STEP-ONE-FRAME, and reset.
   The step button is the most important teaching tool in this whole repository.
   It is how a student actually sees that a game is not continuous motion but a
   sequence of separate, discrete moments - a flipbook being turned.
   Writing that machinery once here keeps each visualizer around 100 lines
   instead of 500.

   NO DEPENDENCIES. NO BUILD STEP. NO INTERNET REQUIRED.
   Open any visualizer by double-clicking the .html file.

   HOW YOU USE IT (see shared/visualizers/*.html for real examples)

     Anim.sketch({
       mount: '#demo',             // where to build the widget
       width: 640, height: 360,    // logical drawing size (not pixels on screen)
       fps: 60,                    // how long one "frame" is worth: 1/60 s
       state() {                   // called at start and on every reset
         return { x: 0, speed: 120 };
       },
       update(s, dt, api) {        // advance the world by dt seconds
         s.x += s.speed * dt;
       },
       draw(s, g, api) {           // paint one frame
         g.clear();
         g.circle(s.x, 180, 20, g.color.accent);
       }
     });

   The object you return from state() is yours. anim.js never touches it.
   ========================================================================== */

(function (global) {
  'use strict';

  /* --------------------------------------------------------------------------
     THEME
     Colours are read from CSS custom properties so a visualizer automatically
     matches light mode, dark mode, and the printed page. If the stylesheet is
     missing (someone opened a visualizer on its own) we fall back to literals,
     so a visualizer is never invisible.
     ----------------------------------------------------------------------- */
  var FALLBACK = {
    bg:      '#ffffff',
    ink:     '#1b1f24',
    muted:   '#6b7480',
    grid:    '#e3e7ec',
    accent:  '#2f6fed',
    accent2: '#e8590c',
    good:    '#2b8a3e',
    bad:     '#c92a2a',
    warn:    '#f08c00',
    panel:   '#f4f6f8'
  };

  function readTheme(el) {
    var cs = global.getComputedStyle(el);
    var out = {};
    Object.keys(FALLBACK).forEach(function (k) {
      var v = cs.getPropertyValue('--anim-' + k).trim();
      out[k] = v || FALLBACK[k];
    });
    return out;
  }

  /* --------------------------------------------------------------------------
     DRAWING HELPERS
     A thin wrapper over the 2D context. Two reasons for it:
       1. Visualizer code reads like what it draws: g.arrow(...) not twelve
          lines of moveTo/lineTo/rotate.
       2. Everything is drawn in LOGICAL coordinates. A sketch declared as
          640x360 always draws in a 640x360 space, whatever size the canvas
          actually ends up on screen. So visualizers survive being projected
          onto a classroom screen or squeezed onto a phone.
     ----------------------------------------------------------------------- */
  function makeGraphics(ctx, w, h, theme) {
    var g = {
      ctx: ctx,
      width: w,
      height: h,
      color: theme,

      clear: function (c) {
        ctx.save();
        ctx.fillStyle = c || theme.bg;
        ctx.fillRect(0, 0, w, h);
        ctx.restore();
        return g;
      },

      rect: function (x, y, rw, rh, c) {
        ctx.fillStyle = c || theme.ink;
        ctx.fillRect(x, y, rw, rh);
        return g;
      },

      strokeRect: function (x, y, rw, rh, c, lw) {
        ctx.strokeStyle = c || theme.ink;
        ctx.lineWidth = lw == null ? 2 : lw;
        ctx.strokeRect(x, y, rw, rh);
        return g;
      },

      circle: function (x, y, r, c) {
        ctx.beginPath();
        ctx.arc(x, y, r, 0, Math.PI * 2);
        ctx.fillStyle = c || theme.ink;
        ctx.fill();
        return g;
      },

      ring: function (x, y, r, c, lw) {
        ctx.beginPath();
        ctx.arc(x, y, r, 0, Math.PI * 2);
        ctx.strokeStyle = c || theme.ink;
        ctx.lineWidth = lw == null ? 2 : lw;
        ctx.stroke();
        return g;
      },

      line: function (x1, y1, x2, y2, c, lw) {
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.strokeStyle = c || theme.ink;
        ctx.lineWidth = lw == null ? 2 : lw;
        ctx.stroke();
        return g;
      },

      dashed: function (x1, y1, x2, y2, c, lw, pattern) {
        ctx.save();
        ctx.setLineDash(pattern || [6, 6]);
        g.line(x1, y1, x2, y2, c, lw);
        ctx.restore();
        return g;
      },

      /* An arrow is how we draw a vector. Students meet these constantly, so
         the head is sized in proportion to the line and never looks spindly on
         a projector. */
      arrow: function (x1, y1, x2, y2, c, lw) {
        var width = lw == null ? 3 : lw;
        var head = Math.max(8, width * 3.2);
        var dx = x2 - x1, dy = y2 - y1;
        var len = Math.sqrt(dx * dx + dy * dy);
        if (len < 0.001) { return g; }           // zero-length vector: nothing to draw
        var ux = dx / len, uy = dy / len;        // unit vector along the arrow
        // Stop the shaft short so it does not poke through the head.
        var sx = x2 - ux * head * 0.85, sy = y2 - uy * head * 0.85;
        g.line(x1, y1, sx, sy, c, width);
        ctx.beginPath();
        ctx.moveTo(x2, y2);
        ctx.lineTo(x2 - ux * head + -uy * head * 0.45, y2 - uy * head + ux * head * 0.45);
        ctx.lineTo(x2 - ux * head - -uy * head * 0.45, y2 - uy * head - ux * head * 0.45);
        ctx.closePath();
        ctx.fillStyle = c || theme.ink;
        ctx.fill();
        return g;
      },

      text: function (str, x, y, opt) {
        opt = opt || {};
        var size = opt.size || 16;
        var weight = opt.bold ? '700' : '400';
        ctx.font = weight + ' ' + size + 'px ' + (opt.mono
          ? 'ui-monospace, SFMono-Regular, Menlo, Consolas, monospace'
          : 'system-ui, -apple-system, Segoe UI, Roboto, sans-serif');
        ctx.fillStyle = opt.color || theme.ink;
        ctx.textAlign = opt.align || 'left';
        ctx.textBaseline = opt.baseline || 'alphabetic';
        ctx.fillText(str, x, y);
        return g;
      },

      /* A label with a solid plate behind it, so text stays readable when it
         lands on top of something busy. */
      badge: function (str, x, y, opt) {
        opt = opt || {};
        var size = opt.size || 14;
        ctx.font = (opt.bold ? '700 ' : '400 ') + size + 'px system-ui, sans-serif';
        var padX = 8, padY = 5;
        var tw = ctx.measureText(str).width;
        var bw = tw + padX * 2, bh = size + padY * 2;
        var bx = opt.align === 'center' ? x - bw / 2 : x;
        g.rect(bx, y - bh, bw, bh, opt.bg || theme.panel);
        g.strokeRect(bx, y - bh, bw, bh, opt.border || theme.grid, 1);
        g.text(str, bx + padX, y - padY - 2, {
          size: size, bold: opt.bold, color: opt.color || theme.ink
        });
        return g;
      },

      grid: function (step, c) {
        step = step || 40;
        ctx.save();
        ctx.strokeStyle = c || theme.grid;
        ctx.lineWidth = 1;
        for (var x = 0; x <= w; x += step) {
          ctx.beginPath(); ctx.moveTo(x + 0.5, 0); ctx.lineTo(x + 0.5, h); ctx.stroke();
        }
        for (var y = 0; y <= h; y += step) {
          ctx.beginPath(); ctx.moveTo(0, y + 0.5); ctx.lineTo(w, y + 0.5); ctx.stroke();
        }
        ctx.restore();
        return g;
      },

      /* A rounded panel used to group things on screen. */
      panel: function (x, y, pw, ph, c, r) {
        r = r == null ? 10 : r;
        ctx.beginPath();
        ctx.moveTo(x + r, y);
        ctx.arcTo(x + pw, y, x + pw, y + ph, r);
        ctx.arcTo(x + pw, y + ph, x, y + ph, r);
        ctx.arcTo(x, y + ph, x, y, r);
        ctx.arcTo(x, y, x + pw, y, r);
        ctx.closePath();
        ctx.fillStyle = c || theme.panel;
        ctx.fill();
        return g;
      },

      save:    function () { ctx.save(); return g; },
      restore: function () { ctx.restore(); return g; },
      alpha:   function (a) { ctx.globalAlpha = a; return g; }
    };
    return g;
  }

  /* --------------------------------------------------------------------------
     THE SKETCH
     ----------------------------------------------------------------------- */
  function sketch(cfg) {
    var W = cfg.width || 640;
    var H = cfg.height || 360;
    var FPS = cfg.fps || 60;
    var STEP = 1 / FPS;                     // seconds in one logical frame
    var fixedStep = cfg.fixedStep !== false; // default: advance in whole frames

    var host = typeof cfg.mount === 'string'
      ? document.querySelector(cfg.mount)
      : cfg.mount;
    if (!host) {
      console.error('anim.js: mount target not found:', cfg.mount);
      return null;
    }

    /* ---- build the DOM -------------------------------------------------- */
    host.classList.add('anim');
    host.innerHTML = '';

    var stage = document.createElement('div');
    stage.className = 'anim-stage';

    var canvas = document.createElement('canvas');
    canvas.className = 'anim-canvas';
    stage.appendChild(canvas);
    host.appendChild(stage);

    var bar = document.createElement('div');
    bar.className = 'anim-controls';
    host.appendChild(bar);

    var theme = readTheme(host);
    var ctx = canvas.getContext('2d');

    function button(label, title, cls) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'anim-btn' + (cls ? ' ' + cls : '');
      b.textContent = label;
      b.title = title;
      b.setAttribute('aria-label', title);
      bar.appendChild(b);
      return b;
    }

    var wanted = cfg.controls || ['play', 'step', 'reset', 'speed'];
    var has = function (name) { return wanted.indexOf(name) !== -1; };

    var btnPlay  = has('play')  ? button('▶ Play', 'Play or pause the animation', 'anim-btn-primary') : null;
    var btnStep  = has('step')  ? button('⏭ Step 1 frame', 'Advance exactly one frame, then stop') : null;
    var btnReset = has('reset') ? button('↺ Reset', 'Put everything back to the start') : null;

    var speedWrap = null, speedInput = null, speedOut = null;
    if (has('speed')) {
      speedWrap = document.createElement('label');
      speedWrap.className = 'anim-speed';
      speedWrap.innerHTML = '<span>Speed</span>';
      speedInput = document.createElement('input');
      speedInput.type = 'range';
      speedInput.min = '0.1'; speedInput.max = '2'; speedInput.step = '0.1';
      speedInput.value = String(cfg.speed == null ? 1 : cfg.speed);
      speedOut = document.createElement('output');
      speedOut.textContent = Number(speedInput.value).toFixed(1) + '×';
      speedWrap.appendChild(speedInput);
      speedWrap.appendChild(speedOut);
      bar.appendChild(speedWrap);
    }

    var counter = null;
    if (cfg.showFrameCount !== false) {
      counter = document.createElement('span');
      counter.className = 'anim-counter';
      counter.setAttribute('aria-live', 'off');
      bar.appendChild(counter);
    }

    /* Slot for a visualizer's own extra controls (checkboxes, buttons). */
    var extras = document.createElement('div');
    extras.className = 'anim-extras';
    host.appendChild(extras);

    /* A caption line a visualizer can write explanations into. */
    var caption = document.createElement('p');
    caption.className = 'anim-caption';
    caption.hidden = true;
    host.appendChild(caption);

    /* ---- sizing ---------------------------------------------------------
       The canvas keeps the sketch's aspect ratio and fills the width it is
       given. We draw in logical units and let a transform do the scaling, so
       nothing in a visualizer ever has to think about pixels or screen size.
       -------------------------------------------------------------------- */
    var scale = 1;
    function resize() {
      var cssW = Math.max(200, stage.clientWidth || W);
      var cssH = cssW * (H / W);
      var dpr = global.devicePixelRatio || 1;
      canvas.style.width = cssW + 'px';
      canvas.style.height = cssH + 'px';
      canvas.width = Math.round(cssW * dpr);
      canvas.height = Math.round(cssH * dpr);
      scale = (cssW / W) * dpr;
      render();
    }

    /* ---- state ---------------------------------------------------------- */
    var state, frame = 0, simTime = 0, playing = false, lastReal = 0, carry = 0;
    var handles = Object.create(null);
    var dragging = null;

    var api = {
      get frame()   { return frame; },
      get time()    { return simTime; },
      get playing() { return playing; },
      get state()   { return state; },
      width: W, height: H, fps: FPS, step: STEP,
      theme: theme,
      extras: extras,

      play:  function () { setPlaying(true); },
      pause: function () { setPlaying(false); },
      reset: function () { doReset(); },
      stepOnce: function () { doStep(); },
      redraw: function () { render(); },

      /* Write a line of explanation under the canvas. Visualizers use this to
         narrate what just happened, which matters for a student reading alone
         without the teacher talking over it. */
      say: function (html) {
        caption.hidden = !html;
        caption.innerHTML = html || '';
      },

      /* A draggable point. Call it from draw(); it returns the current
         position and paints itself. Letting a student drag two boxes together
         to watch a collision test flip from false to true teaches more than
         any paragraph about it. */
      handle: function (name, x, y, opt) {
        opt = opt || {};
        var hd = handles[name];
        if (!hd) {
          hd = handles[name] = { x: x, y: y, r: opt.r || 11 };
        }
        hd.r = opt.r || hd.r;
        hd.label = opt.label;
        if (opt.hidden) { return hd; }
        var c = opt.color || theme.accent2;
        var gg = currentG;
        gg.circle(hd.x, hd.y, hd.r, c);
        gg.ring(hd.x, hd.y, hd.r + 3, c, 1.5);
        if (opt.label) {
          gg.text(opt.label, hd.x, hd.y - hd.r - 8,
            { size: 13, bold: true, align: 'center', color: c });
        }
        return hd;
      },

      /* Add a checkbox to the extras row. */
      toggle: function (label, initial, onChange) {
        var l = document.createElement('label');
        l.className = 'anim-toggle';
        var cb = document.createElement('input');
        cb.type = 'checkbox';
        cb.checked = !!initial;
        l.appendChild(cb);
        l.appendChild(document.createTextNode(' ' + label));
        extras.appendChild(l);
        cb.addEventListener('change', function () {
          if (onChange) { onChange(cb.checked); }
          render();
        });
        return { get checked() { return cb.checked; }, el: cb };
      },

      /* Add a labelled slider to the extras row. */
      slider: function (label, min, max, value, stepSize, onChange) {
        var l = document.createElement('label');
        l.className = 'anim-slider';
        var span = document.createElement('span');
        span.textContent = label;
        var inp = document.createElement('input');
        inp.type = 'range';
        inp.min = String(min); inp.max = String(max);
        inp.step = String(stepSize || 1); inp.value = String(value);
        var out = document.createElement('output');
        out.textContent = String(value);
        l.appendChild(span); l.appendChild(inp); l.appendChild(out);
        extras.appendChild(l);
        inp.addEventListener('input', function () {
          out.textContent = inp.value;
          if (onChange) { onChange(Number(inp.value)); }
          render();
        });
        return { get value() { return Number(inp.value); }, el: inp };
      },

      /* Add a plain button to the extras row. */
      button: function (label, onClick) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'anim-btn';
        b.textContent = label;
        extras.appendChild(b);
        b.addEventListener('click', function () { onClick(); render(); });
        return b;
      }
    };

    var currentG = makeGraphics(ctx, W, H, theme);

    /* ---- the loop ------------------------------------------------------- */
    function setPlaying(on) {
      playing = on;
      if (btnPlay) {
        btnPlay.textContent = on ? '⏸ Pause' : '▶ Play';
        btnPlay.title = on ? 'Pause the animation' : 'Play the animation';
      }
      if (on) {
        lastReal = 0;
        carry = 0;
        global.requestAnimationFrame(tick);
      }
    }

    function advance(dt) {
      if (cfg.update) { cfg.update(state, dt, api); }
      simTime += dt;
      frame += 1;
    }

    function doStep() {
      setPlaying(false);
      advance(STEP);
      render();
    }

    function doReset() {
      setPlaying(false);
      frame = 0;
      simTime = 0;
      carry = 0;
      state = cfg.state ? cfg.state(api) : {};
      // Draggable handles go back to wherever draw() first put them.
      handles = Object.create(null);
      if (cfg.onReset) { cfg.onReset(state, api); }
      render();
    }

    function tick(now) {
      if (!playing) { return; }
      if (!lastReal) { lastReal = now; }
      var real = (now - lastReal) / 1000;
      lastReal = now;
      // A tab left in the background can hand us a huge gap. Clamping stops
      // the world teleporting when the student comes back to it.
      if (real > 0.25) { real = 0.25; }
      var speed = speedInput ? Number(speedInput.value) : (cfg.speed == null ? 1 : cfg.speed);

      if (fixedStep) {
        carry += real * speed;
        var guard = 0;
        while (carry >= STEP && guard < 240) { advance(STEP); carry -= STEP; guard++; }
      } else {
        // Variable dt, which is what a real browser game gets. The delta-time
        // visualizer needs this to be honest about what actually happens.
        advance(real * speed);
      }
      render();
      global.requestAnimationFrame(tick);
    }

    function render() {
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.setTransform(scale, 0, 0, scale, 0, 0);
      currentG = makeGraphics(ctx, W, H, theme);
      if (cfg.draw) { cfg.draw(state, currentG, api); }
      if (counter) {
        counter.textContent = 'frame ' + frame + '  ·  ' + simTime.toFixed(2) + ' s';
      }
    }

    /* ---- input ---------------------------------------------------------- */
    function toLogical(ev) {
      var r = canvas.getBoundingClientRect();
      return {
        x: (ev.clientX - r.left) * (W / r.width),
        y: (ev.clientY - r.top) * (H / r.height)
      };
    }

    canvas.addEventListener('pointerdown', function (ev) {
      var p = toLogical(ev);
      var best = null, bestD = Infinity;
      Object.keys(handles).forEach(function (k) {
        var hd = handles[k];
        var d = Math.hypot(hd.x - p.x, hd.y - p.y);
        // A generous grab radius: fingers and projector mice are imprecise.
        if (d < hd.r + 14 && d < bestD) { best = hd; bestD = d; }
      });
      if (best) {
        dragging = best;
        canvas.setPointerCapture(ev.pointerId);
        canvas.classList.add('is-grabbing');
        ev.preventDefault();
      }
    });

    canvas.addEventListener('pointermove', function (ev) {
      if (!dragging) { return; }
      var p = toLogical(ev);
      dragging.x = Math.max(0, Math.min(W, p.x));
      dragging.y = Math.max(0, Math.min(H, p.y));
      render();
    });

    function endDrag() {
      dragging = null;
      canvas.classList.remove('is-grabbing');
    }
    canvas.addEventListener('pointerup', endDrag);
    canvas.addEventListener('pointercancel', endDrag);

    if (btnPlay)  { btnPlay.addEventListener('click', function () { setPlaying(!playing); }); }
    if (btnStep)  { btnStep.addEventListener('click', doStep); }
    if (btnReset) { btnReset.addEventListener('click', doReset); }
    if (speedInput) {
      speedInput.addEventListener('input', function () {
        speedOut.textContent = Number(speedInput.value).toFixed(1) + '×';
      });
    }

    /* Keyboard: space plays/pauses, right-arrow steps, R resets. Teachers
       drive these from the back of the room with a presenter remote. */
    host.tabIndex = 0;
    host.addEventListener('keydown', function (ev) {
      if (ev.target.tagName === 'INPUT') { return; }
      if (ev.key === ' ') { ev.preventDefault(); setPlaying(!playing); }
      else if (ev.key === 'ArrowRight') { ev.preventDefault(); doStep(); }
      else if (ev.key === 'r' || ev.key === 'R') { ev.preventDefault(); doReset(); }
    });

    if (global.ResizeObserver) {
      new global.ResizeObserver(resize).observe(stage);
    } else {
      global.addEventListener('resize', resize);
    }

    /* Re-read colours if the OS flips between light and dark mid-lesson. */
    if (global.matchMedia) {
      var mq = global.matchMedia('(prefers-color-scheme: dark)');
      if (mq.addEventListener) {
        mq.addEventListener('change', function () {
          theme = readTheme(host);
          api.theme = theme;
          render();
        });
      }
    }

    doReset();
    resize();
    if (cfg.autoplay) { setPlaying(true); }

    return api;
  }

  /* --------------------------------------------------------------------------
     SMALL MATHS HELPERS
     Named so that a student reading a visualizer learns the vocabulary.
     ----------------------------------------------------------------------- */
  var util = {
    clamp: function (v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); },
    lerp: function (a, b, t) { return a + (b - a) * t; },
    dist: function (x1, y1, x2, y2) { return Math.hypot(x2 - x1, y2 - y1); },
    /* Axis-Aligned Bounding Box overlap: the single most used test in 2D games. */
    aabb: function (a, b) {
      return a.x < b.x + b.w && a.x + a.w > b.x &&
             a.y < b.y + b.h && a.y + a.h > b.y;
    },
    rand: function (lo, hi) { return lo + Math.random() * (hi - lo); },
    /* Degrees are friendlier than radians for a 13-year-old. */
    deg: function (r) { return r * 180 / Math.PI; },
    rad: function (d) { return d * Math.PI / 180; }
  };

  global.Anim = { sketch: sketch, util: util, FALLBACK: FALLBACK };
}(window));
