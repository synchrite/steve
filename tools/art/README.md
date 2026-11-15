# Pass 3 approval lineup

Run `python tools/art/pixelize.py` with Pillow installed to rebuild `lineup.png`.
Run `python tools/art/check_lineup.py` to check the palette, dimensions, binary
alpha, bottom-center anchors, four separate standing legs, exact nearest-neighbor
4x enlargement, and deterministic regeneration.

`cluster_art.py` contains the revised native-resolution character paintings:
explicit silhouettes, hard shading clusters, and placed material details.
`pixelize.py` owns the shared palette (64 colors, including sixteen additional generated-room material shades) and finalizer, retained
textured door/couch/lamb, and approval-sheet composition. These scripts save only
the lineup. The owner approved this lineup for step 2.

The older per-asset scripts are the previous pass; they are not called by this
lineup and should not be used to export the revised artwork.


## Approved sprite exports

Run `python tools/art/export_sprites.py` with Pillow installed to overwrite the
nine wired PNGs in `assets/` and rebuild `tools/art/sheet.png` at exact 4x.
The exporter calls the approved paintings directly, preserves seated Steve's
lineup adjustment without the couch, and defines the two new reclining dog
poses with the same cluster primitives and shared finalizer. It checks table
sizes, palette membership, binary alpha and bottom-center anchors before
saving. It does not regenerate or change the approved lineup.

## Image-generated room replacements

Run `python tools/art/generated_rooms.py` to rebuild `assets/house_bg.png`,
the seven `assets/cctv_*.png` files, and `sheet_rooms.png`. This supersedes
`rooms.py` for the current room art. Requires Pillow and the local ignored
`rooms_src/` folder, containing fifteen built-in imagegen originals and
the previous exports used for exact structural/runtime registration.
`rooms_prompts.json` records the prompt set; `rooms_crops.json` records each
source crop and target size. Generated artwork is center-cropped to the
target aspect and downscaled with BOX area sampling before shared palette
conversion. Exact wall strips, TV footprints, stove and lift registration
come from the previous exports; runtime working areas remain plain.
The script validates dimensions, RGB opacity, palette membership, captured
layout wall fields, working-zone colors and unchanged game/frozen hashes.

