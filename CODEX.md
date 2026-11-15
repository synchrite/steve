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
| `burglar_short.png` | 20 x 36 | not wired; Pass 3 exported | |
| `burglar_tall.png` | 16 x 48 | not wired; Pass 3 exported | |
| `car_lift.png` | 96 x 44 | not wired; Pass 3 exported | white compact car, side view |
| `lobby_shack.png` | 120 x 88 | not wired; Pass 3 exported | wooden beach shack on sand |
| `house_bg.png` | 1320 x 192 | not wired; Pass 3 exported | full house cross-section: living room, kitchen, bathroom, two bedrooms, garage, yard and lot |
| `tv_frame.png` | 624 x 284 | not wired; Pass 3 exported | TV bezel, screen area transparent |

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

## 3D and map textures

All files below are in `assets/tex/`. Exported, not wired; game-code integration
remains for Claude. Opaque textures retain exact UV bounds. Billboards face
front and use bottom-center anchors, with alpha restricted to 0 or 255.

| File | Size | Content / use |
|---|---|---|
| `tex_grass.png` | 64 x 64 | Seamless XY; olive grass clumps |
| `tex_sand.png` | 64 x 64 | Seamless XY; pale sand ripples |
| `tex_snow.png` | 64 x 64 | Seamless XY; cream-white snow and cool depressions |
| `tex_desert.png` | 64 x 64 | Seamless XY; warm ochre sand ridges |
| `tex_water0.png` | 64 x 64 | Seamless XY; blue-slate water, frame 0 |
| `tex_water1.png` | 64 x 64 | Seamless XY; shifted ripples, frame 1 |
| `tex_building.png` | 128 x 192 | Hit 2; red roof top quarter, siding, middle window, lower-right door |
| `tex_rock.png` | 128 x 128 | Hit 3; staggered stone blocks and cracks |
| `tex_cliff.png` | 128 x 256 | Hits 1/4; snow cap, cool fractured cliff face |
| `sky_day.png` | 1024 x 240 | Horizontal wrap; brighter blue-slate sky, layered cumulus pixel clouds |
| `sky_dusk.png` | 1024 x 240 | Horizontal wrap; purple-orange storm sky |
| `bb_tree.png` | 96 x 192 | Leafy clustered tree, exposed trunk |
| `bb_palm.png` | 96 x 192 | Splayed fronds, coconuts and curved trunk |
| `bb_bush.png` | 96 x 64 | Rounded leaf clumps |
| `bb_chest.png` | 64 x 48 | Gold loot chest, bands and latch |
| `bb_vend.png` | 64 x 112 | Red vending machine, glass display and collection slot |
| `bb_steve.png` | 64 x 96 | Original white astronaut, GREEN panel, clear bubble helmet, visible RED side pack pods |
| `bb_enemy.png` | 64 x 96 | Neutral gray/white player mask for runtime tinting |
| `bb_ally.png` | 64 x 96 | Identical neutral player mask for runtime tinting |
| `island_bg.png` | 1200 x 520 | Prep TV backdrop: ocean, sky, sand island and palms; no characters or shack |
| `map_island.png` | 2000 x 2000 | Generic map using genMap coast formula and biome layout |

2026-11-14 (3D and map textures): Read fpsRender(), drawTopDown(), genMap(),
islandWorld(), islandRender() and buildGrid() in the current index.html.
Created 21 original procedural Pillow paintings in the approved Pass 3
clean-cluster style via tools/art/textures3.py. Shared 36-color palette is
unchanged; material colors are its nearest blue-slate, olive, cream, ochre,
red and purple equivalents of the procedural rendering. Enemy/ally are an
explicit exception required for tinting: neutral RGB gray bands 48, 104,
172 and 228, with identical geometry and binary alpha. Steve follows the
owner's current GREEN chest / RED rocket-pack request over the older avatar
color description above. No borrowed character designs.

Every asset uses tools/art/pixelize.py: billboards use its existing outline,
palette and bottom-anchor finalizer; added surface_pixelize() for opaque
textures, preserving the entire UV rectangle without outlining or trimming.
Neutral masks receive grayscale band conversion after the shared finalizer.
Existing character exports and the approved lineup were not regenerated.

map_island is intentionally GENERIC: genMap randomizes the 64 coast radii,
mountain X, lake coordinates, town positions/types, roads and tree placements
per match. This painting uses the same coast formula with a fixed seed,
center (500,500), roughly 440 coast radius, snowy north (y<250), southeast
desert, southwest swamp, mountain around (500,380), central lake and a river
running south. Representative towns/roads are scenery and must not be used
as exact current-match navigation or collision data. The circular raycaster
shore also differs from genMap's ragged top-down coast. North is at the top.

Preview: tools/art/sheet3.png (1320 x 1720), all 21 assets labeled; floor
samples repeat 2 x 2; small textures and billboards are enlarged with nearest
neighbor. Sky/backdrop previews are native size; map preview is reduced to
60%, and the original 1000 x 1000 export is authoritative. Visually reviewed
the sheet, including front-visible red pack pods and character-free backdrop.
Validation: tools/art/check_textures3.py passes dimensions, palette/grayscale
membership, opacity, binary sprite alpha, balanced bottom-center anchors,
exact opposing floor edges in X/Y, sky edges in X, distinct water frames,
identical tint masks and byte-identical regeneration of PNGs and sheet.
Rebuild with Pillow: python tools/art/textures3.py; validate with
python tools/art/check_textures3.py. This session used the existing Pillow
installation in C:/Users/synchrite/ComfyUI/venv/Scripts/python.exe.
No git commands run. No writes to index.html, frozen/, ref/, burglars,
car_lift, lobby_shack, house_bg or tv_frame. Integration preview in the game
is left for the game-code handoff because these filenames are not wired.


2026-11-14 (double-detail 3D texture pass): Rebuilt all 21 assets/tex PNGs
at the owner's requested doubled dimensions; updated the table above and
replaced tools/art/sheet3.png (1440 x 2300). Retained the shared 36-color
palette, original compositions and meanings. Added native-resolution grass
blades and tiny flowers, sand ripples and pebbles, snow facets, water crests,
siding grain/nails, roof detail, rock fractures, leaf veins, bark, chest grain
and rivets, vending products/buttons/vents, suit seams and helmet reflections.
Skies have richer multi-lobed cloud shapes and ordered band transitions;
day uses the brighter existing blue-slate with cream cloud highlights.
Backdrop has the revised day sky and fine beach/ocean detail. Map retains
its generic biome/coast layout with finer terrain marks at 2000 x 2000.
These are new material marks on larger rasterized shapes, not plain upscales.

Billboards occupy the full height, touch the bottom row and have exactly
one transparent column on each side. Steve keeps his white suit, green
chest panel, clear helmet and red rocket pack. Enemy and ally remain
identical neutral grayscale masks for runtime tinting. Every export passes
the shared pixelize.py finalizer; texture_detail.py adds the native marks.
Updated check_textures3.py passes all requested sizes, palette/grayscale,
opaque UV rectangles, binary alpha, full-canvas anchors, floor XY / sky X
edge equality, distinct water frames and byte-identical regeneration.
Visually reviewed the updated asset sheet. Rebuild and validate using the
same textures3.py and check_textures3.py commands documented above.
No git commands run. No writes to index.html, frozen/, ref/, burglars,
car_lift, lobby_shack, house_bg or tv_frame. Game integration was not changed.

## Lobby fighters

All 36 PNGs are in `assets/lobby/`, each **64 x 96**, facing right,
transparent with binary alpha, bottom-center anchored. Exported, not wired.
Original arcade-fighter designs; no borrowed game characters or logos.

| Fighter | Files | Design |
|---|---|---|
| Steve | `fighter_steve_0.png`, `fighter_steve_1.png`, `fighter_steve_2.png`, `fighter_steve_3.png`, `fighter_steve_dance0.png`, `fighter_steve_dance1.png` | White astronaut suit, green control panel, bubble helmet, red rocket pack; four-frame idle bounce and two dance poses |
| Bront | `fighter_bront_idle0.png`, `fighter_bront_idle1.png`, `fighter_bront_dance0.png`, `fighter_bront_dance1.png`, `fighter_bront_shoot0.png` | Massive dockyard brawler, ochre work vest, wrapped fists, slate cargo trousers |
| Serein | `fighter_serein_idle0.png`, `fighter_serein_idle1.png`, `fighter_serein_dance0.png`, `fighter_serein_dance1.png`, `fighter_serein_shoot0.png` | Lean kicker, asymmetric cream training tunic, diagonal bindings and split trousers |
| Vesper | `fighter_vesper_idle0.png`, `fighter_vesper_idle1.png`, `fighter_vesper_dance0.png`, `fighter_vesper_dance1.png`, `fighter_vesper_shoot0.png` | Angular cyber ninja, segmented armor, plum tabard and lime visor |
| Solaro | `fighter_solaro_idle0.png`, `fighter_solaro_idle1.png`, `fighter_solaro_dance0.png`, `fighter_solaro_dance1.png`, `fighter_solaro_shoot0.png` | Muscular wrestler, original asymmetric sunburst mask, zigzag tights and wrist cuffs |
| Rivet | `fighter_rivet_idle0.png`, `fighter_rivet_idle1.png`, `fighter_rivet_dance0.png`, `fighter_rivet_dance1.png`, `fighter_rivet_shoot0.png` | Wiry punk, pink mohawk, studded vest, patched trousers and chain belt |
| Orion | `fighter_orion_idle0.png`, `fighter_orion_idle1.png`, `fighter_orion_dance0.png`, `fighter_orion_dance1.png`, `fighter_orion_shoot0.png` | Space cowboy, angular wide-brim hat, scarf, frontier jacket and armored chaps |

### Dated handoff — 2026-11-14

Read AGENTS.md, this brief, and drawTV()'s prep-lobby code. Created the
original fighter studies with the built-in imagegen tool, then finalized
through the existing shared tools/art/pixelize.py pipeline. Preserved the
shared 36-color palette, hard pixel edges, tinted outlines and top-left
light. Steve follows the current owner's GREEN panel / RED pack instruction.
Each rival has two idles, two dances and one upward-aiming toy-blaster pose
with a contrasting safety muzzle. Steve's idle loop uses a restrained
0/1/2/1-pixel upper-body compression with fixed floor contact.

Preview: tools/art/sheet_lobby.png, exact 3x nearest-neighbor (1512 x 2703).
Visually reviewed the full roster sheet. All 36 exports pass exact dimensions,
shared palette membership, binary alpha and balanced bottom-center bounds.
Sources and exact generation prompts: tools/art/lobby_sources/ (prompts.json).
Reproduce final exports: python tools/art/lobby_fighters.py (Pillow required).
Exact filename manifest: tools/art/lobby_manifest.json.

No git commands run. No changes to index.html, frozen/, assets/tex/, burglar
sprites, car_lift, lobby_shack, house_bg or tv_frame. Game wiring and in-game
animation review remain for Claude; these assets are intentionally unwired.

2026-11-14 (remaining six, approved Pass 3): Exported all six remaining
assets at their exact table sizes. Original clean-cluster paintings with
the unchanged shared 36-color palette and pixelize.py pipeline. Burglars
face right: short/round with red beanie and stripes, tall/lanky with dark
jacket and flat cap. White compact car faces right; wooden shack on sand.

Read drawHouse and drawTV. House uses source daylight room/furniture/lot
coordinates including GX=200, at 2x with world origin (0,144); native floor
y=180. Off-palette CSS colors use approved palette equivalents; exact CSS
RGB values cannot coexist with the unchanged palette. Material families
are preserved. House uses surface_pixelize to retain the full layout.
TV asset origin corresponds to game (4,0). Screen cutout is exactly
(12,12,600,260), fully transparent, matching TX=10/TY=6/TW=300/TH=130.
Its alpha mask survives surface_pixelize without trimming or expansion.
Other four sprites use the standard palette/outline/bottom-anchor finalizer.

Preview: tools/art/sheet2.png, five assets at exact 4x nearest-neighbor,
house at 1x. Visually reviewed; dimensions, palette membership, binary
alpha, sprite anchors and TV cutout pass. Rebuild: node
tools/art/house_capture.cjs then tools/art/remaining_assets.py with Python
from C:/Users/synchrite/ComfyUI/venv/Scripts/python.exe (Pillow installed).
Six remain unwired for Claude. No git commands run; index.html, frozen/,
lineup and previous assets were not edited.

## Room backgrounds - 2026-11-14

| File in assets/ | Size | Content |
|---|---|---|
| house_bg.png | 1320 x 192 | Full house cross-section, kitchen, bathroom, adult bedroom, kid bunk bed and Xbox, garage with empty lift, craft corner, work board/bench, yard and parked lot inventory |
| cctv_yard.png | 320 x 220 | Garage exterior, lawn, fixed base fence |
| cctv_stove.png | 320 x 220 | Kitchen counters and unlit stove |
| cctv_door.png | 320 x 220 | Front door from inside; code door framing, interior cream wall |
| cctv_couch.png | 320 x 220 | Empty living room couch and dark TV, shared Simba/Steve view |
| cctv_bath.png | 320 x 220 | Tiled bathroom, central door, toilet and vanity |
| cctv_kid.png | 320 x 220 | Bunk bed, dark wall TV and Xbox |
| cctv_wife.png | 320 x 220 | Empty craft corner, table, materials, storage |

### Notes from Codex - 2026-11-14

Created eight original opaque Pillow pixel paintings using the unchanged shared
36-color palette and pixelize.py surface_pixelize() finalizer. Read AGENTS.md,
CODEX.md, drawHouse(), drawCU(), the approved lineup and existing art. Main house
fixtures are extracted from static drawHouse rectangles, with GX=200 applied
for global garage/yard coordinates. Place house_bg at buffer (0,138), scale 0.5;
it ends immediately before FLOOR=234. Source colors use shared material shades:
sky is slate blue, red is brick red within the approved palette. Added material
strokes, wood grain, tiles, rugs, pictures, plants, shelves, cables and tools.
Close-ups preserve principal code framing with additional room dressing.

Preview: tools/art/sheet_rooms.png (all eight assets at native export size).
Rebuild: python tools/art/rooms.py (Pillow required). Exact dimensions, opaque
RGB, palette membership and four dark TV screen rectangles pass validation.
Visually reviewed the contact sheet. No characters, visitors, animated cooking
pot/effects, fireplace flames, moving car, arriving vehicle, job marks, upgrades,
scanlines, timestamps or blinking indicators are baked in. Empty lift includes
fixed posts and resting platform; runtime owns moving elements. Exported, not
wired: game integration remains for Claude. No git commands run. No edits to
index.html, frozen/, ref/, approved lineup or existing character sprites.

### Notes from Codex - 2026-11-14 (rich 16-bit room repaint)

Rebuilt assets/house_bg.png (1320 x 192) and all seven cctv_*.png room
backgrounds (320 x 220), plus tools/art/sheet_rooms.png. Original procedural
Pillow pixel paintings; no tiles, characters or imagery copied from any game.
Read AGENTS.md, this brief, house_layout.json, drawHouse() and drawCU().
Retained the room order, wall X coordinates, door positions, existing furniture
rectangles and runtime alignment. Added floor planes with staggered grain and
receding courses, ceramic tile highlights, baseboards, layered crown molding,
darker ceiling/corner bands, inset doorway shadows, furniture contact shadows,
striped/floral wallpaper, bordered patterned rugs, upholstered cushion seams,
book spines, clocks, lamps, dithered sunlight parallelograms and warm light pools.
Kitchen has jars, pans and a hanging towel; bathroom has mirror glints and
bottles; kid room has an original rocket poster, toys and gaming chair; craft
corner has supplies and a laundry basket. Garage retains the empty lift, tool
pegboard, workbench and toolbox, with tire stacks and oil stains outside the
lift. Yard includes flowers, mailbox and distant garden layers.

Appended twelve room/material shades to pixelize.py's shared palette, keeping
all existing entries and indices (48 total). Drawing remains at exact native
resolution, using hard colour clusters and selective ordered Bayer dithering;
no blur, antialiasing, semi-transparent pixels or smooth gradients. All assets
pass the shared surface_pixelize() finalizer. Existing character, lobby and
3D assets were not regenerated. New colour hex values, in index order 36..47:
#65534b #957b61 #bdab89 #d6c6a5 #f5dfa9 #47352e #a57a50 #b88859
#cbb78e #abc1ba #54705b #814a43.

Rebuild: python tools/art/rooms.py (Pillow required). Added room_detail.py for
the reusable material, depth, light and dressing pass. Corrected the old room
exporter's stale drawHouse line selections to the current static fixture lines;
added source-line guards so subsequent shifts fail visibly. Runtime fire,
smoke, moving car, repairbot, turret, traps and board status are excluded.
Four TV screens remain uniformly dark. The painter explicitly protects the
stove working area, lift interior and parked lot area from decorative overlays.

Visually reviewed the final native-size contact sheet. Validation passed exact
dimensions, opaque RGB, shared palette membership, four dark screen rectangles,
fixed wall coordinates against house_layout.json, protected-zone pixel checks,
and byte-identical regeneration of all eight exports and the contact sheet.
No git commands run. No writes to index.html, frozen/ or ref/. Game code and
wiring remain unchanged; no live in-game review was performed for this repaint.


### Notes from Codex - 2026-11-14 (image-generated room replacement)

Used the built-in image generation tool for fifteen separate original sources:
living room, kitchen, bathroom, master bedroom, kid bedroom, garage, yard, lot,
and all seven CCTV views. Raw generations are saved locally in the ignored
tools/art/rooms_src/ directory. These generated raster paintings replace the
rejected procedural room art, adding floral wallpaper, dense shelves, carved
wood, textiles, ceramics, layered gardens and strong warm sunbeams. Original
designs; no particular game's imagery was copied or requested.

Replaced assets/house_bg.png at 1320 x 192, all seven assets/cctv_*.png at
320 x 220, and tools/art/sheet_rooms.png. Added generated_rooms.py for exact
aspect crops, BOX area downsampling, measured furniture registration grids,
shared palette conversion and compositing. Wall fields are checked against
house_layout.json; drawHouse() and drawCU() were read. Captured structural
strips, door and TV footprints remain registered. Stove working surfaces,
empty lift, blank work board and empty lot car spots are protected for runtime
drawing. CCTV screens remain uniformly dark. No people, moving cars, flames,
timestamps or scanlines were baked into the art. Set dressing follows each
generated camera view; no live in-game review was performed.

Expanded the shared palette from 48 to the authorized 64 colors, retaining all
existing entries/indices. Added #211b22 #38251e #603b26 #956138 #ce9959 #f7d98a
#fff6d9 #a34832 #693d39 #c56e53 #315664 #528d9b #82b7c2 #304b38 #58804c #a9b776.
Fixed surface quantizer padding to repeat a valid palette entry instead of
admitting unintended pure black. No existing sprites or textures regenerated.
Prompt set: tools/art/rooms_prompts.json. Crop/registration manifest:
tools/art/rooms_crops.json. Rebuild with Pillow:
python tools/art/generated_rooms.py (requires the local raw-source directory).

Visually inspected the final contact sheet. Checks pass exact dimensions,
opaque RGB, shared palette membership, captured wall fields, four dark screens,
plain working zones and unchanged SHA-256 hashes for index.html and every file
in frozen/. No git commands run. No edits to index.html, frozen/ or ref/.


### Notes from Codex - 2026-11-14 (Pass 4 RPG)

Replaced house_bg and all seven CCTV rooms with original built-in imagegen
cartoon RPG art, BOX-downsampled and snapped to a deterministic 256-color
room palette. Retained layout walls, screen footprints, clear stove pot
airspace, lift bay and car spaces; painted fixed unlit burners and quieted
the walking strip. Raw sources: tools/art/rooms_src/ (ignored); exact prompts
in rooms_prompts.json and registration in rooms_crops.json.
Added Hoops, Narc, Jug, Neonpunk, Glitch, Rollerqueen, Dad and Sunny: five
64x96 frames each, binary alpha, tinted outlines, bottom-center floor anchors.
New fighter prompts/sources and palette are retained; all 36 prior sprites
are byte-identical. Updated 76-file manifest and both preview sheets.
Rebuild: python tools/art/generated_rooms.py; python tools/art/lobby_fighters.py.
Validate: python tools/art/check_pass4.py. Visually reviewed both sheets.
This art pass made no writes to index.html, frozen/, ref/ or the realistic-mode
archive. index.html changed externally during the pass; its initial hash
snapshot is retained and validation reports it separately.
No commit or push. Initial pull was blocked by existing unstaged changes.

### Notes from Codex - 2026-11-14 (PDA and tips UI)

Followed tools/art/brief_ui_pda.txt: added mode body classes and an original
CSS STEVE PAD skin for RPG, keeping the CLASSIC phone appearance. One --ui
factor now sizes the canvas, phone, CCTV, top controls, stats deck, shop and
menus. Phone re-renders preserve independent inbox/view scroll and follow new
messages only when already at the bottom. Zoom stays open until an outside tap;
scroll gestures and existing controls do not activate touch zoom.

Added the persistent ? TIPS toggle and twelve-card instructions dialog, with
12 original imagegen pixel icons in assets/ui/tips/, finalized through the
existing shared surface_pixelize pipeline without editing it. Replaced fixed
phone/TV/3D help with contextual hover/first-touch tips, shown once per session
with tips off and repeatable with tips on. Updated ASSETS.md. Preview and
reproduction/check scripts are isolated under tools/ui/.

Validation: extracted script passes node --check; actual scroll functions pass
inbox, independent-view, thread-position and bottom-follow unit checks; shared
scale mathematics fits all four requested viewports and both canvas aspects.
All 12 art files exist and their contact sheet was visually reviewed. Live
browser startup/console and viewport screenshot tests remain UNVERIFIED:
Chrome exits with Access denied creating Mojo/Crashpad IPC, and Computer Use
reports its native pipe unavailable. Run node tools/ui/check_pda.cjs on a host
where Chrome can launch. Initial git pull --rebase was blocked by existing
unstaged concurrent art changes. No commit or push; no edits to room/lobby art,
frozen/, ref/, or gameplay rules.


## Themes

### Notes from Codex - 2026-11-15

Completed the 60-file interface in tools/art/brief_themes.txt for all five
theme folders: 300 required PNG exports, none missing. Classic remains code
drawn. Read ASSETS.md, CODEX.md, house_layout.json, rooms_crops.json and the
lobby manifest before authoring. No writes to index.html, frozen/ or ref/.

| Theme | Required exports | Art / reuse | Palette ceiling |
|---|---:|---|---:|
| 16bit | 60 | Retained Pass 3 art, completed missing props/icons, space-ranger Steve poses | 64 |
| rpg | 60 | Retained eight Pass 4 rooms; 52 files copied byte for byte from 16bit | 256 |
| gritty | 60 | New original arcade paintings, neon, graffiti, grime, harsh shadows | 128 |
| modern | 60 | New original stylized painterly art, rich materials and warm lighting | 256 |
| halloween | 60 | 14 decorated modern variants; 46 files copied byte for byte from modern | 256 |

Used built-in image generation for 154 separate original sources, followed
by area downsampling and palette snapping through pixelize.py finalizers.
Sources: tools/art/theme_sources/. Prompts/references: theme_jobs.json;
successful astronaut retries: theme_retry_jobs.json. Original Pass 3/4 inputs
are preserved in theme_original/ so rebuilding never requantizes old exports.
Steve follows the current space-ranger identity (white suit, green panel,
clear helmet, red pack), overriding the older house-hoodie description above.
Kid retains the cap, black hair and darker tan skin; Simba remains a tan dog.
No real-person face references or borrowed game characters were used.

Modern/Halloween share a palette and restrained ordered surface dithering.
Required sprites have binary alpha, tinted outlines and bottom-center floor
anchors. Opaque textures retain UV bounds; floors wrap in XY, skies in X.
Enemy/ally billboards are identical neutral grayscale tint masks. House
wall/door/lift strips and runtime working areas remain registered. Four TV
screen rectangles stay uniformly dark; bezels retain the exact transparent
(12,12)-(612,272) opening. Removed white exterior letterboxing from generated
wide house/sky sources. Halloween keeps its lower walk strip readable.

Inventory: tools/art/themes_manifest.json, with the requested status strings.
Its 77 additional existing 16bit lobby/map entries are retained legacy files,
outside the requested 60-file interface; no new fighter animation pass was
requested. Previews: tools/art/sheet_theme_<theme>.png for all five themes.
Visually reviewed every sheet; corrected sky padding and TV-screen dithering.
All 300 required files pass dimensions, palette ceilings, binary alpha,
anchors, opacity, seams, dark screens, TV holes, reuse contracts, neutral
masks, distinct water frames and frozen-file integrity checks.

Rebuild: python tools/art/build_themes.py
Validate: python tools/art/check_themes.py
Workflow: tools/art/THEMES.md. Byte-reproduction report:
tools/art/themes_reproducibility.json (300 assets, five sheets, two manifests).
Game wiring and live in-game review remain with the concurrent game-code
task. Initial pull was blocked by pre-existing unstaged changes. No commit
or push, as requested. Existing CODEX.md bytes/encoding were preserved;
this section was appended as ASCII because the file contains legacy bytes.

### Notes from Codex - 2026-11-15 (16-BIT v2)

Reworked the 60 required assets/16bit exports under brief_16bit_v2.txt.
Captured the current CLASSIC drawHouse geometry with a read-only JS recorder;
repainted house and CCTV surfaces in CLASSIC material families with inset
bevels, seams and broken texture clusters. Reworked character material hues
and enlarged visible bounds while preserving bottom-center floor contact.
Painted new white-suit Steve poses with green panel/poncho and red side pack.
Terrain and UV fixtures use CLASSIC raycaster material colours. All five
island_bg images now have green land with a sand rim; their 16-BIT composition
follows the drawTV ellipse proportions. Only these four explicitly requested
island files were changed outside the 16bit theme.

Regenerated sheet_theme_16bit.png and refreshed themes_manifest.json while
preserving valid status strings and legacy entries. Sources/reproduction:
tools/art/16BIT_V2.md, classic_v2_capture.cjs, remaster_16bit_v2.py and the
one-time v2_original snapshots. Per-image palettes and SHA-256 export evidence
are in v2_palettes.json and v2_validation.json. Independent checks in
check_16bit_v2.py pass all 60 dimensions, <=64 colours, binary alpha, 39 sprite
anchors, terrain/sky seams, bezel alpha, identical neutral tint masks, five
green islands, byte-identical rebuild and unchanged other-theme exports
against the previous export inventory (except the four island exceptions).
Visually inspected the exported contact sheet. Chrome launch failed EPERM;
live house/CCTV/lobby screenshots remain UNVERIFIED. Game source changed
externally during this pass; the final capture was refreshed and rebuilt.
This art script never writes index.html, frozen/, ref/ or other theme files
besides the four named islands. No commit or push. Initial pull failed because
.git/FETCH_HEAD is not writable in this session.

Unresolved exact-colour requirement: CLASSIC's house exceeds the requested
64-colour cap even before extra shading (the current capture contains 91
relevant base colours). The export currently retains 56 exact dominant base
colours plus same-hue shading; some minor accents are approximated. It does
not meet an exact match for EVERY CLASSIC colour. Owner question: should the
house-only palette cap increase, or should a reduced CLASSIC palette be
approved? The current 64-colour approximation is retained for review.
