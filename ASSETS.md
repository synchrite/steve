# Graphics modes and asset tracking

The game has one look per graphics mode. Every visible element is listed here with what each mode uses for it. Update this file in the same commit whenever an asset is added, replaced, wired or retired.

## Modes

| Mode | Code value (`GFX`) | What it is | Status |
|---|---|---|---|
| CLASSIC | `classic` | The original look: everything drawn in code with flat rectangles at 1x (320 or 480 x 240 buffer). No image files. | Complete. Never change it. |
| RPG | `16` | Cartoony, blocky pixel art at 2x buffer resolution, drawn by Codex (passes 3 and 4). Falls back to CLASSIC drawing for anything without a file. | In progress |
| REAL (planned) | not wired | Late-90s realistic 32-bit look. First room concepts are kept locally in `tools/art/rooms_src_real/` and `tools/art/rooms_prompts_real.json`. Possibly Blender later. | Concept only |

Rule for new modes: a mode gets its own asset folder (`assets/<mode>/...`) and its own column below. A mode never edits another mode's files. Anything a mode does not provide falls back to the previous mode, and that fallback is listed as "falls back".

## Element table

Status key: **replaced** = the mode has its own art and it is drawn. **loaded, not drawn** = the file exists and loads but no code draws it yet. **falls back** = the mode shows the CLASSIC drawing. **missing** = no file yet.

| Element | CLASSIC | RPG file | RPG status |
|---|---|---|---|
| House rooms (living room, kitchen, bath, bedrooms) | code rects | `assets/house_bg.png` | replaced |
| Lot / garage / yard | code rects | `assets/house_bg.png` (right part) | replaced; lot cars are baked into the image |
| CCTV views (7) | code rects | `assets/cctv_{yard,stove,door,couch,bath,kid,wife}.png` | replaced |
| Steve on couch / walking | code rects | `steve_couch.png`, `steve_walk.png` | replaced |
| Wife, kid | code rects | `wife.png`, `kid.png` | replaced |
| Simba (lap, sleep, sit, stand) | code rects | `simba_*.png` | replaced |
| Lamb toy | code rects | `lamb_toy.png` | replaced |
| Burglars | code rects | `burglar_short.png`, `burglar_tall.png` | loaded, not drawn |
| Car on the lift | code rects | `car_lift.png` | loaded, not drawn |
| TV set (frame around the game screen) | code rects | `tv_frame.png` | loaded, not drawn (the TV looks the same in both modes) |
| Pizza driver, lawn statue, porch | code rects | none | falls back |
| TV game: top-down map | code (`genMap`) | `tex/map_island.png` | loaded, not drawn (map is randomized each match) |
| TV game: lobby island backdrop | code rects | `tex/island_bg.png` | replaced |
| TV game: lobby shack | code rects | `lobby_shack.png` | replaced |
| TV game: lobby players | code rects | `lobby/fighter_*.png` (6 players + Steve) | replaced; 8 more in pass 4 |
| TV game: top-down players, loot, weapons, effects | code rects | none | falls back |
| TV game: 3D views (floor, walls, sky) | flat colours | `tex/tex_*.png`, `tex/sky_*.png`, `tex/tex_water*.png` | replaced |
| TV game: 3D billboards (trees, bushes, chests, vending) | code | `tex/bb_*.png` | replaced |
| TV game: 3D people | textured boxes from `charAtlas` (code) | none | falls back; still low-poly and primitive |
| HUD, meters, buttons, READY button | code | none (READY is restyled per mode in code) | partly styled per mode |
| Stats deck (hi-fi, Zune, docked phone, handheld) | HTML/CSS | none | same in all modes |
| Phone skin | original HTML/CSS phone | mode CSS: `body.gfx-rpg #phone` | replaced: original grey-green STEVE PAD, notepad strip, LCD and rounded pen-friendly controls; CLASSIC unchanged |
| Tips instruction art (12 cards) | `assets/ui/tips/{tv,combos,pickaxe,shop,phone,pizza,skills,bills,simba,house,stats,graphics}.png` | same files | replaced: original generated 64 x 64 icons, shared palette, nearest-neighbor display |
| Item shop, menus, tips guide | HTML/CSS | shared HTML/CSS | shared `--ui` scale with canvas, phone, CCTV and stats deck; tips setting stored in `steveUI` |

## Known gaps in RPG mode

- TV set, burglars and car lift have files but are not drawn yet.
- 3D people are still primitive boxes. 3D views were stretched; since this change they are cropped to the TV's shape instead.
- Top-down TV game sprites and all new features (weapons, drops, pizza driver, statue) have no RPG art.
