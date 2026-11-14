# Art brief for Codex: Steve's Day Off (16-bit pass)

This repo is a pixel-art game in one file, `index.html`. `frozen/steves-day-off-v1.html` is a locked earlier version: do not edit it. Your job is the art in `assets/`.

## Pass 2 (current): build in 3D, render, then pixelize

The first pass (hand-placed pixel maps) was rejected by the owner: too flat and stiff, wrong scale, clashed with the scene, and the characters didn't read as themselves. Pass 2 replaces it.

**Method**

1. In Blender, model each character as a simple, chunky low-poly figure (toy-like proportions, big readable silhouettes). Use flat colors per material, not textures.
2. Light with one warm key light from the top left and a soft fill. Use a toon/flat shader with 3 shading steps so it pixelizes cleanly.
3. Render with an **orthographic side camera**, transparent background, at 8x the final size (for example 320 x 384 for a 40 x 48 sprite), facing right.
4. Downscale to the final size with nearest-neighbor or area sampling, then snap every pixel to a shared palette (see below), force alpha to 0 or 255, and add a 1 px outline tinted toward the neighboring color. Keep this step in a script (`tools/art/pixelize.py`) so every sprite goes through the same pipeline.
5. Pose each character naturally (weight on one leg, slight lean, head tilted toward what they're doing). Simba especially needs life: ears up, tail mid-wag, looking up at Steve when begging.

**Scale (fixes "wrong size")**

Size everything against the house. The floor line is the bottom of each sprite, and these are the in-game heights at 2x: a door is 84 px, the couch seat is 28 px off the floor, the coffee table is 22 px. Steve standing should be about 46 px (just over half a door), the wife about 44, the kid about 32, Simba standing about 30 at the shoulder. Render a single "lineup" image with everyone next to a door and the couch, and check proportions before exporting individual sprites.

**Matching the scene (fixes "doesn't match")**

Use one shared 32-color palette for all characters, built from the colors already in `index.html` (wall cream #e4ddd0, floor gray #8a8580, couch tan #c79a5e, wood brown #4a2a1a, plus skin, fur and clothing tones). Every sprite is snapped to that palette, so characters and room share the same colors.

**Likeness (fixes "characters look off")**

Work from the photos in `ref/` for Simba (stocky tan pit/shepherd mix, big upright ears, black muzzle, lilac collar with lime buckle). People are stylized and original; match hair, clothing and build, not faces.

**Deliverables:** the same file names and sizes as the table below, plus `tools/art/lineup.png` (everyone side by side with a door and the couch) for the owner to approve before anything is wired in. Keep the `.blend` file in `art-src/` (Git LFS if over a few MB).

## Target look

16-bit console era: richer than the current blocky art, still clearly pixel art.

- **Detail:** every sprite is drawn at **2x** the game's base grid (sizes below). The game shows each of your pixels at 1.5 screen pixels.
- **Color:** up to about 16 colors per sprite, including the outline. Use 2 to 4 shades per material (skin, fabric, fur, metal) with a consistent light source from the top left.
- **Outlines:** 1 px, dark and tinted toward the color they border (dark brown around tan fur, deep blue around blue fabric). No pure black outlines except on very dark objects.
- **Shading:** hard-edged shading, light ordered dithering is fine on large surfaces. No anti-aliasing, no gradients, no blur, no semi-transparent edges.
- **Background:** transparent PNG (alpha 0 or 255 only).
- **Facing:** side view, facing **right**. The game mirrors sprites for left.
- **Anchor:** the game places sprites by **bottom-center** (feet on the floor). No empty rows below the feet; keep empty columns balanced left and right.
- **Originality:** original designs only. Do not imitate characters from other games, films, toys or brands. Steve's in-game avatar is an original astronaut (white suit, blue chest panel, clear bubble helmet, orange-and-silver rocket pack). Keep it that way.

## Characters

Reference photos are in `ref/` (local only, not committed). Use them for colors and proportions. Do not draw real people's faces from the photos; stylize everyone.

- **Simba**: tan pit/shepherd mix. Fur base #c98f4e with lighter belly and darker back. Big upright ears with darker insides, black muzzle, warm brown eyes. Lilac woven collar with a lime-green buckle.
- **Steve**: olive camo hoodie, short brown hair, light beard, jeans. Holds a game controller on the couch.
- **Wife**: pink hair in a bun, patterned glasses, denim overalls over a black shirt.
- **Kid**: yellow shirt, blond hair, about half Steve's height.
- **Burglars**: an original bumbling pair. One short and round in a red beanie and striped shirt; one tall and lanky in a dark jacket and flat cap.
- **Lamb toy**: off-white plush lamb with stubby legs and a red stitched mouth.

## Asset list

Sizes are width x height in pixels, already doubled for the 16-bit pass.

| File | Size | Status | Notes |
|---|---|---|---|
| `simba_stand.png` | 52 x 44 | wired | walking pose, mouth empty |
| `simba_sit.png` | 40 x 48 | wired | sitting, looking up, begging |
| `simba_sleep.png` | 56 x 24 | wired | curled up asleep |
| `simba_lap.png` | 68 x 44 | wired | lying across Steve's lap on the couch, looking at the TV |
| `lamb_toy.png` | 24 x 20 | wired | plush lamb |
| `steve_couch.png` | 32 x 48 | wired | seated side view, controller in hands, facing right toward the TV |
| `steve_walk.png` | 20 x 44 | wired | standing |
| `wife.png` | 20 x 44 | wired | standing |
| `kid.png` | 14 x 36 | wired | standing |
| `burglar_short.png` | 20 x 36 | not wired | |
| `burglar_tall.png` | 16 x 48 | not wired | |
| `car_lift.png` | 96 x 44 | not wired | white compact car, side view |
| `lobby_shack.png` | 120 x 88 | not wired | wooden beach shack on sand |
| `house_bg.png` | 1320 x 192 | not wired | full house cross-section: living room, kitchen, bathroom, two bedrooms, garage, yard and lot |
| `tv_frame.png` | 624 x 284 | not wired | TV bezel, screen area transparent |

"Wired" files show up in the game as soon as they exist in `assets/`. "Not wired" files load, but Claude still has to hook them up.

Work in this order: Simba (all four), Steve (couch, walk), wife, kid, lamb toy, then the rest.

## Checking your work

Run a local web server in this folder (`python -m http.server`), open `http://localhost:8000`, start a game, and look for the sprite in the house view. Missing files fall back to the old art, so you can check one at a time.

## Handing back

Commit each finished asset on its own with a short message (`Add simba_sit.png (16-bit)`), then `git pull --rebase` and `git push`. Note anything unfinished or any question for the owner at the bottom of this file under "Notes from Codex".

## Notes from Codex

2026-11-14: Created all nine wired PNGs in the requested order, with one
self-contained Pillow character-map script per sprite under tools/art/.
Simba's tan coat, dark muzzle, build and collar were informed by the local
reference photos. All nine pass exact dimensions, binary alpha (0/255),
palette limit, balanced horizontal bounds and bottom-row anchor checks;
reviewed together at 4x nearest-neighbor enlargement. Original designs.
No changes to index.html or frozen/; no push attempted.

Unfinished handoff: this session cannot write .git/FETCH_HEAD or
.git/index.lock (Permission denied), so the initial pull, all nine individual
asset commits, and this status commit could not be completed. Files remain
unstaged for the owner's agent to commit individually. The local HTTP server
started, but the browser preview failed because the Computer Use native pipe
is unavailable, so the house-view visual check remains outstanding.
