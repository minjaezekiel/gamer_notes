# Putting your game online

Your game is a single `.html` file with nothing else attached — no images, no sound files, no
libraries. That makes it unusually easy to share.

## The quickest way: send the file

Email or message the `.html` file to someone. They double-click it and it plays. That is genuinely
all. It works offline, on any computer, with no installation.

This is worth appreciating: almost nothing else you build will be this easy to give away.

## Putting it on the web

### GitHub Pages (free, permanent)

1. Make a free account at github.com.
2. Create a new **public** repository.
3. Upload your `.html` file and rename it `index.html`.
4. Go to **Settings → Pages**, and under "Branch" choose `main`, then Save.
5. Wait about a minute. Your game is at `https://yourname.github.io/your-repo-name/`

### itch.io (free, and it is where small games live)

1. Make an account at itch.io.
2. **Upload new project**, set "Kind of project" to **HTML**.
3. Zip your `.html` file (renamed `index.html`) and upload the zip.
4. Tick **"This file will be played in the browser"**.
5. Set the viewport to match your canvas — 640 × 480 for Breakout.

itch.io is the better choice if you want anyone to actually find it.

## Before you share it

- [ ] Does it work if you open it on a different computer?
- [ ] Does it work with the Wi-Fi switched off? (It should — if not, you have a link to something
      external that you did not mean to add.)
- [ ] Does it start sensibly without instructions, or does the first screen explain the controls?
- [ ] Have you put your name on it?
- [ ] Is there a way to restart without reloading the page?

## A note on making it bigger

Once your game needs images and sound files, you can no longer send a single file and some of this
gets harder. That is one of the things the intermediate level deals with.
