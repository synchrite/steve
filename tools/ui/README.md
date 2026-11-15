# PDA and tips UI pass

The game remains self-contained in `index.html`; no additional JavaScript loads
are needed. `assets/ui/tips/` contains twelve original imagegen icons finalized
at 64 x 64 with the existing shared palette. `tips_sheet.png` is a 3x contact
sheet. `finalize_tips.py` reproduces the exports from the local generated-image
paths recorded in `tips_sources.json` (Pillow required).

Validation:

```
node tools/ui/check_static.cjs
node --check tools/ui/preview/extracted-script.js
node tools/ui/check_pda.cjs
```

The static checks exercise actual extracted phone-scroll and scaling functions.
The browser check starts a local server and headless Chrome, starts both graphics
modes at 1280x720, 1920x1080, 800x600 and 844x390, checks viewport bounds, exercises
phone zoom/scroll and tips state, and saves screenshots plus results under the
ignored `preview/` directory. Chrome must be installed at the path in the script.

In the authoring environment, syntax, scroll unit checks, scale mathematics and
asset checks passed. Browser validation could not run: Chrome's Mojo/Crashpad IPC
creation returned Access denied, and the Computer Use native pipe was unavailable.
The automated browser checks and a visual review of those layouts remain pending.
No gameplay rules were changed. Room and lobby work was left to the concurrent job.
