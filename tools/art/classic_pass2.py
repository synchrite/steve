"""Rebuild CLASSIC pass 2 at 1.5 art pixels per game unit (Pillow and Node)."""
import json
import subprocess

from PIL import Image, ImageDraw

from classic_chars import ART, OUT, PALETTE, Sprite, dog, helmet, lamb, person, pizza_fall


def wife():
    s = Sprite(62)
    p, b = s.poly, s.box
    # Weight on the near leg, one foot set back and the far hand in a pocket.
    p('2a2a30', (9, 34), (20, 33), (25, 39), (24, 47), (22, 55),
      (28, 57), (29, 61), (17, 61), (16, 57), (17, 47), (14, 46),
      (10, 54), (9, 57), (11, 59), (4, 59), (2, 57), (6, 52), (7, 42))
    p('2d5fa8', (9, 37), (16, 37), (15, 46), (9, 54), (6, 55), (8, 47))
    p('3a6aa0', (13, 37), (21, 36), (23, 40), (22, 47), (20, 55),
      (18, 55), (19, 46), (15, 44), (11, 41))
    p('5a8ac0', (15, 42), (19, 43), (20, 47), (18, 52), (18, 46))
    b('5a8ac0', 17, 55, 21, 56)
    p('e8ecf0', (18, 57), (22, 57), (27, 58), (27, 59), (18, 59))
    b('b0b4b8', 4, 56, 8, 57)

    p('2a2a30', (9, 20), (15, 18), (22, 20), (25, 24), (27, 31),
      (23, 36), (24, 41), (17, 43), (8, 41), (7, 36), (5, 28), (6, 24))
    p('3a3a40', (8, 22), (13, 20), (18, 20), (15, 25), (10, 29), (7, 27))
    p('e8c0a0', (15, 16), (21, 17), (21, 21), (19, 23), (15, 21))
    p('3a6aa0', (9, 23), (11, 22), (15, 30), (20, 29), (20, 22), (22, 23),
      (24, 29), (22, 35), (22, 38), (18, 41), (10, 40), (9, 36), (11, 30))
    p('5a8ac0', (13, 31), (20, 31), (19, 34), (14, 35), (12, 33))
    b('e0c070', 12, 29, 12, 30)
    b('e0c070', 21, 28, 21, 29)
    p('e8b890', (24, 26), (25, 29), (25, 32), (22, 36), (20, 35), (22, 31))
    p('2a2a30', (7, 25), (11, 26), (12, 30), (11, 35), (15, 39), (14, 42),
      (11, 42), (7, 38), (6, 34))
    p('e8c0a0', (8, 30), (11, 31), (10, 35), (14, 39), (13, 41), (11, 40), (8, 37))
    b('3a3a40', 8, 27, 10, 29)

    # Loose swept fringe, high bun and curled strands around the ear.
    p('c0508a', (6, 3), (8, 1), (12, 0), (15, 1), (16, 4), (21, 4), (25, 7),
      (26, 11), (25, 14), (20, 17), (17, 18), (12, 23), (8, 22), (9, 18),
      (6, 19), (7, 14), (5, 11), (6, 8), (5, 6))
    p('e0509a', (7, 4), (10, 1), (13, 1), (15, 3), (13, 6), (8, 7))
    p('ff9ac0', (8, 4), (10, 2), (13, 2), (12, 4), (9, 5))
    p('a8744a', (14, 9), (22, 7), (24, 9), (25, 13), (28, 15),
      (26, 16), (26, 19), (22, 21), (18, 20), (15, 17), (12, 16), (12, 12))
    p('e8c0a0', (14, 10), (21, 8), (24, 10), (24, 13), (27, 15),
      (25, 16), (25, 18), (22, 20), (18, 19), (16, 16), (13, 15), (13, 13))
    p('e0509a', (7, 10), (12, 6), (17, 5), (21, 5), (25, 8), (24, 10),
      (21, 8), (18, 9), (15, 12), (12, 13), (11, 18), (9, 20), (9, 15), (7, 16))
    p('ff9ac0', (8, 10), (13, 7), (18, 6), (21, 6), (17, 8), (13, 9), (10, 12))
    b('e8b890', 19, 16, 20, 17)
    b('3a3a40', 14, 12, 19, 12)
    p('3a3a40', (19, 11), (24, 11), (25, 12), (25, 14), (24, 15), (20, 15), (19, 14))
    b('cfe9ff', 20, 12, 24, 14)
    b('2a2a30', 22, 12, 23, 14)
    b('ffffff', 22, 12, 22, 12)
    b('ff9ac0', 19, 11, 19, 11)
    p('c0508a', (21, 17), (24, 17), (23, 18), (22, 18))
    b('e0c070', 14, 16, 14, 16)
    return s.finish()


def seated_steve():
    s = Sprite(43)
    p, b = s.poly, s.box
    # Feet are tucked onto the cushion as Steve leans into the controller.
    p('2a2a30', (11, 30), (24, 30), (33, 33), (35, 38), (43, 38), (45, 42),
      (12, 42), (8, 40), (8, 35))
    p('c0c4ca', (23, 34), (32, 34), (34, 39), (39, 39), (40, 41), (19, 41))
    p('e8e8e8', (12, 34), (23, 33), (31, 35), (30, 38), (24, 39), (18, 41),
      (12, 40), (10, 38))
    b('8a8e94', 37, 39, 42, 41)
    p('5a7a9a', (10, 17), (21, 16), (28, 20), (28, 28), (24, 34),
      (16, 37), (9, 35), (7, 30), (7, 23))
    p('f4f4f4', (11, 18), (21, 18), (26, 21), (26, 28), (23, 33), (16, 35), (10, 34), (9, 29))
    p('2f8f50', (10, 18), (22, 17), (27, 21), (28, 27), (22, 26), (16, 29), (7, 27), (8, 22))
    p('46c46e', (11, 19), (22, 19), (26, 22), (26, 24), (21, 23), (16, 26), (9, 25))
    p('5aff8a', (8, 25), (16, 27), (21, 25), (27, 26), (27, 27), (21, 26), (16, 29), (8, 27))
    p('5a7a9a', (13, 22), (19, 22), (23, 28), (32, 27), (34, 30), (31, 33), (19, 33), (14, 29))
    p('f4f4f4', (14, 23), (18, 23), (22, 30), (29, 29), (29, 31), (20, 32), (16, 29))
    p('e8b890', (29, 28), (32, 27), (34, 29), (32, 31), (29, 31))
    p('2a2a30', (31, 26), (34, 24), (39, 25), (40, 28), (37, 29), (34, 28), (32, 29))
    b('5aff8a', 37, 26, 37, 26)

    def helmet_cluster(color, *points):
        p(color, *((round(x * 0.61 + 2), round(y * 0.61))
                   for x, y in zip(points[::2], points[1::2])))

    def helmet_box(color, x, y, right, bottom):
        helmet_cluster(color, x, y, right, y, right, bottom, x, bottom)

    helmet(helmet_cluster, helmet_box)
    return s.finish()


def native(value):
    # Round half up to keep neighboring world rectangles on shared edges.
    return (3 * value + 1) // 2


def house():
    captured = subprocess.check_output(['node', str(ART / 'capture_classic_pass2.cjs')])
    image = Image.new('RGB', (990, 144), '#9ad4f5')
    draw = ImageDraw.Draw(image)

    def rect(x, y, w, h, color):
        draw.rectangle((native(x), native(y - 138), native(x + w) - 1,
                        native(y + h - 138) - 1), fill=color)

    for entry in json.loads(captured):
        if entry[0] == 'gate':
            gx = entry[1]
            rect(gx + 287, 212, 2, 22, '#9aa0a6')
            rect(gx + 287, 212, 10, 1, '#9aa0a6')
            for i in range(0, 22, 4):
                draw.line((native(gx + 288), native(74 + i), native(gx + 296),
                           min(143, native(78 + i))), fill='#d2d7dc')
            continue
        x, y, w, h, color = entry
        if (x, y, w, h) == (2, 192, 12, 42):
            rect(2, 184, 12, 50, '#4a2a1a')
            rect(3, 185, 10, 49, '#6b4c38')
            rect(4, 187, 8, 45, '#7a5840')
            rect(5, 190, 6, 19, '#6b4c38')
            rect(6, 191, 4, 17, '#7a5840')
            rect(5, 216, 6, 13, '#6b4c38')
            rect(6, 217, 4, 11, '#7a5840')
        elif (x, y, w, h) != (4, 194, 8, 38):
            if x in (152, 222, 262, 312, 352) and y in (200, 204, 206) and color == '#3a2a20':
                rect(x, 184, w, 50, color)
                rect(x + 1, 185, w - 2, 49, '#6b4c38')
            else:
                rect(x, y, w, h, color)

    # Trim stays on the ceiling line. Interior walls retain their registered widths.
    rect(0, 145, 470, 1, '#6a5444')
    rect(0, 146, 470, 4, '#4a3a30')
    for x, end in ((0, 152), (156, 222), (226, 262), (266, 312), (316, 352)):
        rect(x, 232, end - x, 1, '#cfc6b6')
    rect(24, 214, 2, 12, '#8a6a4a')
    rect(31, 220, 24, 1, '#b98a52')
    rect(161, 218, 38, 1, '#6b4a2f')
    rect(398, 156, 40, 1, '#5a5f66')
    rect(398, 179, 40, 1, '#5a5f66')
    rect(244, 229, 16, 1, '#bcd4dc')
    rect(280, 174, 12, 8, '#9ad4f5')
    rect(280, 180, 12, 2, '#5f9f4a')
    rect(319, 198, 1, 14, '#a02a2a')
    for y in (200, 205, 210):
        rect(319, y, 4, 1, '#5a3a2a')
    for x in (381, 433):
        rect(x, 181, 1, 52, '#e23b3b')
    # The source tree began above the strip. Register its trunk at the original x
    # and fit the canopy within the exported sky.
    rect(496, 166, 4, 66, '#3b2a1a')
    rect(495, 144, 7, 5, '#2f5a34')
    rect(490, 149, 17, 8, '#2f5a34')
    rect(484, 157, 28, 11, '#2f5a34')
    rect(488, 165, 21, 7, '#2f5a34')
    rect(491, 153, 10, 5, '#5f9f4a')
    rect(487, 159, 12, 4, '#5f9f4a')
    rect(498, 233, 162, 1, '#8a8580')
    # Lot sign lettering and restrained side-panel accents on the five parked cars.
    draw.text((native(565), native(12)), 'STEVE\'S AUTO', fill='#4a2a1a', anchor='mt')
    for x, highlight in zip((526, 552, 578, 604, 630),
                            ('#f4f4f4', '#3a7bd5', '#d0e870', '#5a5f66', '#e23b3b')):
        rect(x + 2, 223, 16, 1, highlight)
        rect(x + 20, 224, 2, 2, '#ffe8a0')
    return image


def sheet(background, sprites):
    # Separate snapshots keep alternate poses readable without moving them to other rooms.
    snapshots = (
        ('AT HOME', [('steve_couch', 36, 210), ('lamb_toy', 128, 234),
                     ('kid', 333, 226), ('wife', 369, 234)]),
        ('WALKING AND DELIVERY', [('pizza_driver', 13, 234), ('simba_stand', 87, 234),
                                  ('steve_walk', 185, 234), ('burglar_short', 487, 234),
                                  ('burglar_tall', 511, 234)]),
        ('DOORSTEP AND REST', [('pizza_driver_fall', 15, 234), ('simba_lap', 42, 212),
                              ('simba_sit', 73, 234), ('simba_sleep', 112, 234)]),
    )
    porch_margin = 36
    preview = Image.new('RGB', (background.width + porch_margin, 174 * len(snapshots)), '#2a2a30')
    draw = ImageDraw.Draw(preview)
    for i, (title, placements) in enumerate(snapshots):
        top = i * 174
        draw.text((8, top + 4), title, fill='#f4f1e8')
        draw.rectangle((0, top + 20, porch_margin - 1, top + 163), fill='#9ad4f5')
        preview.paste(background, (porch_margin, top + 20))
        draw.rectangle((0, top + 164, preview.width - 1, top + 171), fill='#8a8580')
        draw.rectangle((porch_margin + native(470), top + 164, preview.width - 1, top + 171), fill='#5f9f4a')
        for name, x, y in placements:
            sprite = sprites[name]
            preview.paste(sprite, (porch_margin + native(x) - sprite.width // 2,
                                  top + 20 + native(y - 138) - sprite.height), sprite)
    return preview


def main():
    sprites = {
        'steve_walk': person('steve', 66 / 108),
        'steve_couch': seated_steve(),
        'wife': wife(),
        'kid': person('kid', 47 / 76),
        'burglar_short': person('short', 57 / 92),
        'burglar_tall': person('tall', 66 / 108),
        'pizza_driver': person('pizza', 66 / 108),
        'pizza_driver_fall': pizza_fall(22 / 36),
        'simba_stand': dog('stand', 34 / 61),
        'simba_sit': dog('sit', 34 / 61),
        'simba_sleep': dog('sleep', 17 / 30),
        'simba_lap': dog('lap', 21 / 38),
        'lamb_toy': lamb(14 / 23),
    }
    expected = (66, 43, 62, 47, 57, 66, 66, 22, 34, 34, 17, 21, 14)
    assert len(sprites) == len(expected)
    for (name, sprite), height in zip(sprites.items(), expected):
        assert sprite.mode == 'RGBA' and sprite.height == height, name
        assert {alpha for _, alpha in sprite.getchannel('A').getcolors(256)} == {0, 255}, name
        assert sprite.getbbox() == (3, 0, sprite.width - 3, height), name
        assert all('#%02x%02x%02x' % (r, g, b) in PALETTE
                   for _, (r, g, b, a) in sprite.getcolors(256) if a), name
    background = house()
    assert background.size == (990, 144) and background.mode == 'RGB'
    preview = sheet(background, sprites)

    OUT.mkdir(parents=True, exist_ok=True)
    for name, sprite in sprites.items():
        sprite.save(OUT / f'{name}.png')
        print(f'{name:<20} {sprite.width:>2} x {sprite.height:>2}')
    background.save(OUT / 'house_bg.png')
    preview.save(ART / 'sheet_classic_v2.png')
    print(f'House: {background.width} x {background.height}. Contact sheet: {preview.width} x {preview.height}.')
    print(f'Validated {len(sprites)} sprites for height, CLASSIC palette, hard alpha and centered bottom anchors.')


if __name__ == '__main__':
    main()
