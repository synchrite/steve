# Art brief for Codex: Steve's Day Off (16-bit pass)

This repo is a pixel-art game in one file, `index.html`. `frozen/steves-day-off-v1.html` is a locked earlier version: do not edit it. Your job is the art in `assets/`.

## Pass 3 (current): painted pixel textures, SNES / PS1 style

Pass 1 (flat pixel maps) was rejected, and Pass 2 (Blender) is on hold: Blender is not on this PC. Pass 3 does the art as hand-painted pixel textures, in the style of a SNES or early PS1 game (Earthbound, Secret of Mana, Chrono Trigger, PS1 sprite games). Do not copy any specific game's art.

**What "textured" means here**

- Every surface has texture, not flat fill: knit and seams on the hoodie, denim weave and stitching on overalls and jeans, fur clumps and strands on Simba, wood grain on the shack, fabric on the couch.
- Use 3 to 5 shades per material, a clear highlight from the top left, a cast shadow below, and ordered dithering for soft transitions (fur, fabric folds). No smooth gradients and no anti-aliasing.
- Volume: draw rounded forms with rim light and shadow, so figures look solid and not cut-out. The poses are natural, with weight on one leg and the head turned toward what they're doing. Simba has ears up and a wagging tail.
- Colors: snap to a shared 32-color palette built from the colors in `index.html` (wall cream #e4ddd0, floor gray #8a8580, couch tan #c79a5e, wood #4a2a1a, plus skin, fur and clothing tones), so sprites match the room.

**How**

Use whatever works best: image generation followed by a Pillow cleanup script, or procedural Pillow painting. Every sprite goes through one shared script, `tools/art/pixelize.py`. It:

1. downscales to the exact size
2. snaps to the palette
3. forces alpha to 0 or 255
4. adds a 1 px tinted outline
5. trims to the bottom-center anchor

**Scale (heights at 2x, bottom of sprite = floor)**

- door 84 px
- couch seat 28 px
- Steve 46 px
- wife 44 px
- kid 32 px
- Simba 30 px at the shoulder

The sprite sizes in the table are limits; fill them.

**Deliverable order**

1. First make `tools/art/lineup.png`: everyone side by side with a door and the couch, at 4x nearest-neighbor. Then stop and leave a note for the owner's approval.
2. Only after approval, export the individual sprites with the file names and sizes in the table below. Overwrite the rejected pass-1 PNGs.

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
- **Kid**: saturated yellow T-shirt with sleeves and shorts, warm light-medium tan skin a few steps darker than the adults, with matching shade and highlight; black hair visible below the cap in tufts over the ear, at the back of the neck, and a little forehead fringe; gender-ambiguous, about half Steve's height.
- **Burglars**: an original bumbling pair. One short and round in a red beanie and striped shirt; one tall and lanky in a dark jacket and flat cap.
- **Lamb toy**: off-white plush lamb with stubby legs and a red stitched mouth.

## Asset list

Sizes are width x height in pixels, already doubled for the 16-bit pass.

| File | Size | Status | Notes |
|---|---|---|---|
| `simba_stand.png` | 52 x 44 | wired; Pass 3 exported | walking pose, mouth empty |
| `simba_sit.png` | 40 x 48 | wired; Pass 3 exported | sitting, looking up, begging |
| `simba_sleep.png` | 56 x 24 | wired; Pass 3 exported | curled up asleep |
| `simba_lap.png` | 68 x 44 | wired; Pass 3 exported | lying across Steve's lap on the couch, looking at the TV |
| `lamb_toy.png` | 24 x 20 | wired; Pass 3 exported | plush lamb |
| `steve_couch.png` | 32 x 48 | wired; Pass 3 exported | seated side view, controller in hands, facing right toward the TV |
| `steve_walk.png` | 20 x 44 | wired; Pass 3 exported | standing |
| `wife.png` | 20 x 44 | wired; Pass 3 exported | standing |
| `kid.png` | 14 x 36 | wired; Pass 3 exported | standing |
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

2026-11-14 (Pass 3, step 1 only): Added tools/art/pixelize.py and
tools/art/lineup.png, an original procedural pixel-painted approval study.
The lineup shows Simba standing and sitting, walking Steve, seated Steve
holding a controller on the couch, wife, kid, and an off-white lamb toy,
alongside an 84px door and couch with its seat 28px above the floor.
Native sprites remain in memory; only the 1616 x 600 lineup is exported,
at exact 4x nearest-neighbor enlargement. Shared 32-color palette,
top-left material shading, ordered dithering, fur clumps, fabric weave,
denim seams, wood grain, tinted outlines, and floor shadows are included.
The shared pixelize() pipeline fits to the table limits, snaps the palette,
thresholds alpha, adds a tinted 1px outline, and bottom-centers each sprite.
Used the table's 44px Steve limit where the scale guidance says 46px.
Checked palette membership, binary alpha, bottom anchors, enlargement,
and visually inspected the final lineup. Simba reference photos informed
coat colors and build only; people and toy are original stylizations.
No individual sprites exported, no assets overwritten, no git commands run,
and no changes to index.html or frozen/.

Owner approval requested: please review tools/art/lineup.png for the Pass 3
art direction before any individual sprite exports (step 2).

2026-11-14 (Pass 3, revised approval lineup): Replaced the rejected lineup
with explicit native-resolution pixel clusters in tools/art/cluster_art.py.
Removed procedural grain from all characters; kept the existing 32-color
palette, textured couch, door and lamb, sheet dimensions and shared finalizer.
Simba's local photos informed her broad chest, stocky build and blocky muzzle.
Standing Simba now has four separated legs at ankle height, darker far legs,
defined paws, medium upright ears with dark interiors, a highlighted eye,
curved raised tail, and a lilac collar with lime buckle. Sitting Simba has
lowered haunches, straight forelegs and an upward begging expression.
People have larger heads, readable stylized faces, distinct arms/hands,
asymmetric stances, deliberate camo, pink bun/glasses/overalls, and a blond
kid with a yellow shirt, shorts and bare shins. Seated Steve holds a controller.
Updated pixelize.py; added check_lineup.py and reproduction notes in
tools/art/README.md. Validation passes palette membership, binary alpha,
sprite limits, balanced bottom anchors, four standing leg separations,
1616 x 600 exact 4x enlargement, and byte-identical regeneration. Visually
reviewed the final sheet. Only the approval lineup is exported; individual
assets remain pending owner approval. No git commands run; index.html,
assets/ and frozen/ were not edited. Reference photos remain local only.

2026-11-14 (targeted approval-lineup corrections): Updated the kid in
cluster_art.py with a blue baseball cap covering most of the blond hair,
small visible blond side tufts, a saturated yellow T-shirt with distinct
sleeves, and shorts. Kept the existing size and pixel-cluster style.
Shortened and squared off both Simba muzzles; lowered seated Steve into
the couch cushion by 4 native pixels while retaining his floor contact.
Re-rendered tools/art/lineup.png only; no individual assets exported.
Added one saturated yellow to the original palette (33 total), a narrow
exception to the 32-color brief to keep all existing material colors intact.
Updated the kid description above and palette-count validation/docs.
Visually reviewed the lineup; check_lineup.py passes dimensions, palette,
binary alpha, bottom-center anchors, four standing leg separations, exact
4x nearest-neighbor enlargement and byte-identical regeneration.
No git commands run; index.html, assets/ and frozen/ were not edited.

2026-11-14 (kid skin and hair refinement): Updated only the kid painting
in tools/art/cluster_art.py: warm light-medium tan skin, with coordinated
shadow #b27a54, base #c58f67 and highlight #dca77e added to the shared
palette (36 colors total). Black hair now shows below the cap over the ear,
at the nape and as a small forehead fringe. Kept the cap, yellow tee, shorts,
size and pixel-cluster style. Re-rendered tools/art/lineup.png; no individual
assets exported. Updated palette-count checks. No git commands run;
index.html and frozen/ were not touched.
Visually reviewed the result; check_lineup.py passes palette membership,
dimensions, binary alpha, anchors, exact 4x enlargement and deterministic
regeneration. Confirmed all eight non-kid paintings remain pixel-identical.

2026-11-14 (Pass 3, approved step 2): Owner approved the clean-cluster
lineup. Exported all nine wired assets over the rejected pass-1 PNGs using
tools/art/export_sprites.py and the same cluster_art.py / pixelize.py drawing
pipeline. Seven existing poses match the approved native drawing output
pixel for pixel. Seated Steve preserves the lineup's 4px shortened-leg
adjustment, bottom-centered within the required 32 x 48 canvas, with no couch.
Added original curled sleeping and reclining lap Simba poses with the same
clean clusters, palette, coat shading and collar; lap Simba reuses the exact
approved head painting and contains only the dog. All face right.
No existing character needed additional scaling beyond the approved pipeline;
new poses use its proportional nearest-neighbor fit within their table limits.
Kid retains the approved 32px visible height within its 36px canvas. Seated
Steve has 44px visible height within its 48px canvas. No proportions were
changed to fill unused transparent rows.
Exported tools/art/sheet.png (1104 x 872), showing all nine at exact 4x
nearest-neighbor. Visually inspected the sheet and checked every saved asset
for exact table dimensions, binary alpha, shared palette, floor contact and
balanced horizontal bounds. Verified the seven existing exports against their
approved drawing outputs and the sheet's exact 4x pixel replication.
The approved tools/art/lineup.png and original drawing code remain unchanged.
No git commands run; index.html and frozen/ were not touched. House-view
integration review remains for the game-code handoff; this step reviews the
requested exported asset sheet.
