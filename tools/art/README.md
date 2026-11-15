# Pass 3 approval lineup

Run `python tools/art/pixelize.py` with Pillow installed to rebuild `lineup.png`.
Run `python tools/art/check_lineup.py` to check the palette, dimensions, binary
alpha, bottom-center anchors, four separate standing legs, exact nearest-neighbor
4x enlargement, and deterministic regeneration.

`cluster_art.py` contains the revised native-resolution character paintings:
explicit silhouettes, hard shading clusters, and placed material details.
`pixelize.py` owns the shared palette (33 colors: the original 32 plus saturated tee yellow) and finalizer, retained
textured door/couch/lamb, and approval-sheet composition. These scripts save only
the lineup. Character sprites remain in memory pending owner approval.

The older per-asset scripts are the previous pass; they are not called by this
lineup and should not be used to export the revised artwork.
