# Art brief for Codex: Steve's Day Off

This folder is a fork of the game. `frozen/steves-day-off-v1.html` is the locked version and must not change. Work on `index.html` and `assets/`.

`index.html` already loads PNGs from `assets/` by file name. Each image that exists is drawn instead of the built-in rectangle art. A missing file falls back to the built-in art, so assets can be added one at a time.

## Rules

- Pixel art, hard edges, no anti-aliasing, transparent background (PNG with alpha).
- Draw at **native size** (the sizes below). The game renders a 320x240 buffer and scales it up 3x, so a 20-pixel-tall dog is 20 actual pixels.
- Anchor: the game places each sprite by **bottom-center** (feet on the floor). Leave no empty rows under the feet.
- Side view, facing **right**. The game mirrors sprites when a character faces left.
- Palette: warm and muted, close to the existing colors in `index.html` (`R(...)` calls show the hex values). Keep outlines dark brown or near-black, 1 px.
- Original designs only. Do not imitate characters from other games, films or brands.

## Characters and references

- **Simba**: tan pit/shepherd mix (#c98f4e), big upright ears with darker inner color, black muzzle, lilac woven collar with a lime-green buckle. Reference photos are in the conversation that produced this game; the owner can supply them.
- **Steve**: olive camo hoodie, short brown hair, light beard. Holds a game controller on the couch.
- **Wife**: pink hair in a bun, patterned glasses, denim overalls.
- **Kid**: yellow shirt, blond hair.
- **Burglars**: original bumbling pair. One short in a red beanie, one tall and lanky in a dark jacket.
- **Lamb toy**: off-white plush lamb, red mouth.

## Asset list

| File | Size (w x h) | Notes |
|---|---|---|
| `simba_stand.png` | 26 x 22 | walking pose, lamb toy not included |
| `simba_sit.png` | 20 x 24 | sitting, looking up, begging |
| `simba_sleep.png` | 28 x 12 | curled up asleep |
| `simba_lap.png` | 34 x 22 | lying across Steve's lap on the couch |
| `lamb_toy.png` | 12 x 10 | plush lamb |
| `steve_couch.png` | 16 x 24 | seated, side view, controller in hands |
| `steve_walk.png` | 10 x 22 | standing/walking |
| `wife.png` | 10 x 22 | standing |
| `kid.png` | 7 x 18 | standing |
| `burglar_short.png` | 10 x 18 | not wired yet |
| `burglar_tall.png` | 8 x 24 | not wired yet |
| `car_lift.png` | 48 x 22 | white compact car, side view, not wired yet |
| `lobby_shack.png` | 60 x 44 | wooden beach shack, not wired yet |
| `house_bg.png` | 660 x 96 | full house cross-section backdrop, not wired yet |
| `tv_frame.png` | 312 x 142 | TV bezel, not wired yet |

"Not wired yet" files load but the game does not draw them. Claude will hook them up once they exist.

## Checking your work

Open `index.html` through a local web server (images do not load from `file://` in some browsers), for example `python -m http.server` in this folder, then visit `http://localhost:8000`. Start a game and look for your sprite in the house view.
