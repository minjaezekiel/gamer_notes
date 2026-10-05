/* ===========================================================================
   main.js — runs both versions and prints what each one does.

   Why dynamic import() rather than a normal import line: a module that throws
   while it is being evaluated takes the whole page down with it, and the error
   cannot be caught. `await import(...)` loads it at a moment of our choosing and
   hands us a rejected promise instead, which CAN be caught. That is the only
   reason this page can show you the failure instead of just suffering it.
   ======================================================================== */
const out = document.getElementById("out");

function report(title, body, good) {
  const box = document.createElement("div");
  box.className = good ? "ok" : "bad";
  box.innerHTML = "<h3>" + title + "</h3><pre>" + body + "</pre>";
  out.appendChild(box);
}

/* ---- the broken pair ---- */
try {
  const game = await import("./broken-game.js");
  report("broken-game.js — loaded with no error?", game.start(), true);
} catch (err) {
  report("broken-game.js — failed",
         err.name + ": " + err.message +
         "\n\nNotice what the message does NOT say. It does not mention" +
         "\ncircular imports. It talks about a value that is not ready yet," +
         "\nand it points at broken-hud.js - the file that was waiting, not" +
         "\nthe file that caused it. That indirection is why these bugs are" +
         "\nunpleasant to track down.", false);
}

/* ---- the fixed pair ---- */
try {
  const game = await import("./fixed-game.js");
  report("fixed-game.js — works", game.start() +
         "\n\nOne arrow deleted. fixed-hud.js now imports nothing, so there is" +
         "\nno loop left to go wrong.", true);
} catch (err) {
  report("fixed-game.js — failed", err.name + ": " + err.message, false);
}
