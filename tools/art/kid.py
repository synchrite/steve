"""Original hand-placed 16-bit sprite. Light enters from upper left.
Run with Python and Pillow from any directory. Dots are transparent.
Every map character represents exactly one output pixel; no scaling.
"""
from pathlib import Path
from PIL import Image

SIZE = (14, 36)
PALETTE = {'o': '#4c3d38', 's': '#bc8059', 't': '#dfa37a', 'h': '#f3c297', 'l': '#ffdfb5', 'a': '#94712d', 'b': '#d6ad38', 'c': '#f1cf57', 'd': '#ffe88a', 'j': '#3e6975', 'J': '#6b99a0', 'L': '#a4c5bd', 'x': '#3a4751', 'g': '#d0d2bb', 'r': '#ae7b32', 'R': '#ebc56a'}
PIXELS = """
...ooooo......
..orRRRRo.....
..oRRRRRro....
.orRRRRRrro...
.orRRRrhhho...
.orRrrhhhho...
..orrhhhoho...
..orhhhhhoho..
..ohhhhhhlhho.
..othhhhhhllo.
...othhhhtoo..
....othtto....
..obdchhhbo...
.obddccccbo...
.obdccccccbo..
.obdccbcccbo..
.obdccbccbbo..
.ohhccbccbto..
.ohhccbccbho..
.othccbccbho..
.othccbccbto..
.oobccbccboo..
..obcccccbbo..
..obcccccbo...
..ojJJJJJjo...
..ojJLJJJjo...
..ojJJjjJjo...
..ojJjoojJo...
..ojJjo.ojJo..
..ojJjo.ojJo..
..othho.othho.
..othho.othho.
..oxxxo.oxxxo.
..oxgxo.oxgxo.
.oxxxxooxxxxo.
.oooooooooooo.
""".strip().splitlines()

assert len(PIXELS) == SIZE[1]
assert all(len(row) == SIZE[0] for row in PIXELS)
image = Image.new("RGBA", SIZE, (0, 0, 0, 0))
for y, row in enumerate(PIXELS):
    for x, symbol in enumerate(row):
        if symbol != ".":
            color = PALETTE[symbol].lstrip("#")
            image.putpixel((x, y), tuple(int(color[i:i+2], 16) for i in (0, 2, 4)) + (255,))
output = Path(__file__).resolve().parents[2] / "assets" / "kid.png"
image.save(output)
with Image.open(output) as check:
    assert check.size == SIZE
    assert set(check.getchannel("A").getdata()) <= {0, 255}
    box = check.getbbox()
    assert box[3] == SIZE[1], "Empty rows beneath anchor"
    assert abs(box[0] - (SIZE[0] - box[2])) <= 1, "Unbalanced anchor"
    assert len(check.getcolors()) <= 17
print(f"{output.name}: {SIZE}, binary alpha, balanced bottom anchor verified")
