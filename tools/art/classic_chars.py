"""Paint and verify the CLASSIC character set. Run with Pillow."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

ART = Path(__file__).resolve().parent
OUT = ART.parents[1] / 'assets' / 'classic'
PALETTE = {line.split()[0] for line in (ART / 'classic_palette.txt').read_text().splitlines() if line.startswith('#')}


class Sprite:
    def __init__(self, height, scale=1):
        self.height = round(height * scale)
        self.scale = scale
        self.y_scale = (self.height - 1) / (height - 1)
        self.image = Image.new('RGBA', (140, self.height))
        self.draw = ImageDraw.Draw(self.image)

    def poly(self, color, *points):
        assert '#' + color in PALETTE
        self.draw.polygon([(round(x * self.scale), round(y * self.y_scale))
                           for x, y in points], fill='#' + color)

    def box(self, color, x, y, right, bottom):
        self.poly(color, (x, y), (right, y), (right, bottom), (x, bottom))

    def finish(self):
        cropped = self.image.crop(self.image.getbbox())
        assert cropped.height == self.height
        return ImageOps.expand(cropped, (3, 0, 3, 0))


def person(role, scale=1):
    height = {'short': 92, 'kid': 76}.get(role, 108)
    s = Sprite(height, scale)
    # Draw successive hard-edged clusters on a shared figure grid.
    width = {'short': 1.22, 'tall': .79, 'kid': .83}.get(role, 1)

    def p(color, *coordinates):
        s.poly(color, *((round(50 + x * width), round(y * (height - 1) / 107))
                        for x, y in zip(coordinates[::2], coordinates[1::2])))

    def b(color, x, y, r, z):
        p(color, x, y, r, y, r, z, x, z)

    dark = '2a2a30'
    skin = {'wife': 'e8c0a0', 'kid': 'd9a880', 'pizza': 'a8744a'}.get(role, 'e0b090')
    shade = '8a5a30' if role == 'pizza' else 'a8744a'
    top, fold, light, pants = {
        'steve': ('f4f4f4', 'c0c4ca', 'ffffff', 'e8e8e8'),
        'wife': ('2a2a30', '1a1a1e', '3a3a40', '3a6aa0'),
        'kid': ('e8c33a', 'b09020', 'fff36a', '3a3a5a'),
        'short': ('2a2a2a', '1a1a1a', '3a3a40', '2a2a30'),
        'tall': ('3a3a5a', '2a2a40', '5a5a70', '3a3a5a'),
        'pizza': ('c0302a', 'a02a2a', 'e23b3b', '2a2a40'),
    }[role]
    # Back leg angles away from the front leg.
    p(dark, 12, 64, 27, 66, 23, 83, 12, 100, 14, 104, 13, 106, 0, 106, 0, 101, 8, 78)
    p(fold if role == 'steve' else pants, 13, 69, 23, 71, 20, 82, 10, 97, 4, 97)
    p(dark, 20, 64, 37, 64, 40, 79, 37, 99, 46, 101, 47, 107, 26, 107, 25, 101, 27, 83)
    p(pants, 22, 68, 35, 68, 38, 80, 34, 99, 28, 99, 29, 82)
    p(fold if role == 'steve' else light if role == 'wife' else '5a5a70',
      24, 73, 27, 75, 30, 82, 30, 92, 28, 86)
    if role == 'kid':
        p(skin, 30, 88, 36, 88, 34, 99, 28, 99)
        p(skin, 7, 92, 12, 92, 10, 98, 4, 98)
    shoe = '8a8e94' if role == 'steve' else '3a3a40'
    b(shoe, 28, 103, 44, 105)
    b(shoe, 2, 102, 11, 104)

    b(shade, 21, 25, 33, 39)
    p(dark, 12, 31, 31, 30, 39, 36, 42, 53, 39, 68, 33, 74, 16, 73, 9, 65, 7, 48)
    p(top, 13, 33, 30, 32, 37, 38, 40, 53, 36, 67, 31, 71, 17, 70, 11, 64, 9, 49)
    p(light, 13, 35, 25, 33, 17, 38, 11, 45, 11, 40)
    p(fold, 32, 47, 38, 52, 36, 65, 31, 70, 18, 69, 23, 65, 32, 64)
    if role == 'wife':
        p('3a6aa0', 14, 34, 18, 34, 22, 49, 32, 48, 33, 34, 36, 36,
          37, 60, 35, 68, 30, 73, 16, 70, 11, 64, 16, 48)
        b('5a8ac0', 21, 51, 30, 57)
        b('e0c070', 19, 47, 20, 49)
        b('e0c070', 32, 46, 33, 48)
        b('2d5fa8', 17, 64, 27, 66)
    elif role == 'short':
        for y in (43, 53, 63):
            b(light, 14, y, 35, y + 2)
    elif role == 'tall':
        p('5a5a70', 22, 33, 33, 34, 31, 41, 26, 43, 30, 47, 27, 60, 24, 46)
        b('9a9aa6', 28, 57, 29, 58)
        b('9a9aa6', 27, 64, 28, 65)
    elif role == 'pizza':
        p(light, 23, 33, 34, 35, 32, 40, 27, 36, 23, 39, 19, 35)
        b('e8d0a0', 32, 42, 36, 44)
    # Near sleeve, elbow crease and hand.
    if role == 'pizza':
        p(dark, 11, 37, 22, 40, 23, 53, 39, 54, 40, 61, 35, 64, 16, 62, 9, 56)
        p(top, 12, 39, 19, 41, 20, 54, 36, 56, 35, 61, 17, 60, 11, 55)
        b(skin, 33, 55, 40, 60)
        p('a02a2a', 33, 49, 61, 49, 65, 52, 64, 57, 35, 57, 31, 54)
        p('e8d0a0', 34, 50, 60, 50, 63, 52, 35, 52)
        b('d8b080', 36, 54, 63, 56)
    else:
        p(dark, 13, 38, 22, 39, 25, 47, 20, 58, 18, 69, 11, 71, 7, 66, 9, 55, 8, 47)
        p(top, 13, 40, 20, 41, 22, 47, 19, 54, 10, 54, 10, 46)
        p(skin if role in ('kid', 'wife') else fold,
          11, 55, 19, 55, 16, 66, 11, 67, 9, 64)
        p(skin if role != 'steve' else 'e8e8e8', 10, 64, 17, 65, 17, 69, 12, 70, 9, 67)
        b(shade if role != 'steve' else '9aa0a6', 13, 68, 15, 69)

    if role == 'steve':
        p('a01a1a', 8, 35, 13, 34, 12, 61, 9, 65, 3, 63, 2, 40)
        b('e23b3b', 4, 39, 7, 57)
        b('c0c4ca', 4, 59, 8, 63)
        p('2f8f50', 14, 31, 32, 31, 38, 37, 42, 51, 36, 54, 30, 51, 24, 55, 18, 51, 10, 55, 8, 49)
        p('46c46e', 15, 32, 32, 33, 36, 38, 39, 49, 35, 50, 30, 46, 24, 51, 19, 47, 12, 50, 11, 46)
        p('5aff8a', 14, 38, 13, 49, 18, 46, 23, 50, 29, 46, 35, 50, 39, 48, 40, 51,
          35, 53, 29, 49, 24, 54, 18, 50, 11, 53, 10, 50)
        b('1a5a30', 25, 37, 33, 43)
        b('7fe0a0', 26, 38, 27, 39)
        b('ffb030', 30, 38, 31, 39)
        helmet(p, b)
    else:
        head(p, b, role, skin, shade)
    return s.finish()


def helmet(p, b):
    p('5a7a9a', 17, 0, 34, 0, 42, 5, 46, 12, 46, 22, 41, 29, 34, 33,
      16, 33, 9, 27, 7, 20, 7, 11, 11, 4)
    p('cfe9ff', 17, 2, 34, 2, 40, 6, 44, 13, 44, 21, 39, 28, 33, 31, 17, 31, 11, 26, 9, 19, 9, 12, 13, 5)
    p('9ad4f5', 38, 6, 43, 13, 43, 21, 38, 27, 31, 29, 16, 29, 12, 25, 31, 25, 38, 20)
    p('d9a880', 20, 9, 32, 8, 36, 12, 36, 16, 40, 19, 37, 21, 37, 25, 31, 28, 21, 25, 17, 18)
    p('5a3e28', 17, 10, 22, 7, 32, 7, 36, 10, 35, 13, 30, 11, 24, 12, 22, 19, 18, 19)
    b('2a2a30', 33, 15, 34, 17)
    b('a8744a', 33, 22, 36, 23)
    p('ffffff', 13, 8, 18, 4, 23, 4, 23, 6, 18, 6, 14, 10, 12, 16, 10, 16)
    b('c0c4ca', 17, 29, 35, 31)


def head(p, b, role, skin, shade):
    p('3a2a20', 16, 7, 33, 6, 39, 11, 40, 17, 44, 21, 41, 24, 40, 29, 34, 32,
      24, 31, 17, 28, 13, 21, 13, 13)
    p(skin, 17, 9, 32, 8, 37, 12, 38, 18, 42, 21, 39, 23, 39, 28, 34, 30, 24, 29, 18, 27, 15, 20, 15, 13)
    p(shade, 17, 22, 21, 25, 28, 27, 38, 27, 34, 30, 24, 29, 18, 27)
    b('1a1a1a', 34, 17, 35, 19)
    b('6b4c38', 35, 25, 38, 25)
    if role == 'wife':
        p('c0508a', 11, 3, 16, 0, 23, 0, 26, 4, 24, 10, 15, 13, 10, 10)
        p('e0509a', 12, 3, 17, 1, 22, 1, 23, 4, 17, 7, 12, 7)
        p('e0509a', 13, 9, 21, 5, 32, 5, 39, 10, 38, 14, 29, 11, 25, 14, 21, 22, 16, 25, 12, 20)
        p('ff9ac0', 14, 10, 22, 7, 31, 7, 34, 9, 23, 9, 16, 13)
        b('3a3a40', 23, 15, 42, 17)
        b('3a3a40', 30, 17, 39, 22)
        b('cfe9ff', 32, 17, 37, 20)
        b('2a2a30', 35, 17, 36, 19)
        b('ff9ac0', 23, 15, 24, 16)
        b('ff9ac0', 39, 15, 40, 16)
    else:
        cap, edge, shine = {
            'kid': ('e0c070', '8a6a3a', 'ffe8a0'),
            'short': ('c03030', 'a02a2a', 'ff5a5a'),
            'tall': ('2a2a2a', '1a1a1a', '3a3a40'),
            'pizza': ('c0302a', 'a02a2a', 'e23b3b'),
        }[role]
        p('1a1a1a', 14, 8, 34, 9, 35, 15, 33, 18, 30, 14, 23, 14, 23, 19, 19, 17, 18, 24, 14, 22, 12, 16)
        p(edge, 11, 9, 14, 4, 21, 0, 31, 0, 37, 3, 40, 9, 47 if role != 'short' else 40,
          11, 46 if role != 'short' else 39, 14, 29, 13, 12, 14)
        p(cap, 13, 9, 17, 4, 22, 1, 30, 1, 35, 4, 38, 9, 33, 11, 14, 12)
        p(shine, 16, 7, 21, 3, 29, 2, 32, 4, 22, 5, 17, 8)
        if role in ('short', 'tall'):
            p('1a1a1a', 17, 16, 29, 15, 40, 16, 41, 20, 35, 23, 27, 21, 19, 22, 15, 20)
            b('e0b090', 31, 17, 37, 18)
            b('2a2a30', 35, 17, 36, 18)


def couch_steve(scale=1):
    s = Sprite(94, scale)
    p, b = s.poly, s.box
    p('2a2a30', (49, 59), (60, 63), (59, 82), (66, 85), (66, 90), (48, 90), (47, 85))
    p('9aa0a6', (52, 64), (57, 66), (56, 82), (50, 82))
    b('6a6e74', 50, 86, 64, 88)
    p('2a2a30', (25, 52), (45, 51), (63, 56), (69, 64), (66, 86), (77, 89), (77, 93),
      (55, 93), (54, 88), (55, 69), (41, 70), (26, 66), (21, 60))
    p('e8e8e8', (25, 55), (44, 53), (62, 58), (66, 64), (64, 85),
      (57, 85), (57, 67), (42, 67), (27, 64), (23, 59))
    p('c0c4ca', (32, 63), (51, 64), (59, 63), (57, 67), (42, 67))
    b('8a8e94', 57, 89, 75, 92)
    p('5a7a9a', (21, 28), (40, 28), (47, 34), (48, 47), (42, 58), (27, 61), (18, 57), (17, 44))
    p('f4f4f4', (22, 30), (40, 30), (45, 35), (46, 47), (40, 56), (25, 58), (20, 55), (19, 45))
    p('2f8f50', (21, 29), (40, 29), (46, 34), (46, 45), (35, 44), (28, 49), (17, 46), (17, 40))
    p('46c46e', (22, 31), (38, 30), (43, 34), (44, 41), (36, 40), (28, 45), (20, 43))
    p('5aff8a', (19, 43), (28, 46), (36, 42), (44, 43), (46, 46), (36, 45), (28, 49), (18, 46))
    p('5a7a9a', (25, 36), (35, 37), (40, 48), (54, 46), (58, 50), (54, 55), (34, 56), (28, 51), (23, 43))
    p('f4f4f4', (26, 38), (34, 39), (38, 50), (50, 48), (51, 53), (35, 54), (30, 50), (25, 42))
    p('e8b890', (50, 47), (55, 46), (59, 48), (57, 52), (51, 53))
    p('2a2a30', (52, 43), (58, 41), (65, 43), (65, 48), (61, 49), (57, 47), (53, 49))
    b('5a5a70', 55, 43, 62, 44)
    b('5aff8a', 62, 45, 63, 46)
    helmet(lambda c, *xy: p(c, *((x + 9, y) for x, y in zip(xy[::2], xy[1::2]))),
           lambda c, x, y, r, z: b(c, x + 9, y, r + 9, z))
    return s.finish()


def pizza_fall(scale=1):
    s = Sprite(36, scale)
    p, b = s.poly, s.box
    p('2a2a40', (61, 17), (77, 18), (92, 8), (105, 12), (109, 20), (100, 23),
      (94, 19), (77, 32), (58, 31))
    p('3a3a5a', (64, 19), (77, 21), (93, 11), (102, 14), (103, 18), (94, 15), (76, 28), (62, 28))
    p('2a2a30', (61, 24), (79, 24), (97, 29), (105, 28), (112, 31), (111, 35), (92, 35), (76, 33), (61, 34))
    p('3a3a5a', (63, 26), (78, 26), (95, 31), (95, 33), (76, 31), (61, 32))
    p('a02a2a', (24, 14), (35, 8), (50, 9), (66, 16), (68, 29), (62, 34), (39, 35), (25, 28))
    p('c0302a', (26, 15), (37, 10), (50, 11), (64, 17), (65, 28), (60, 32), (40, 32), (27, 27))
    p('e23b3b', (34, 13), (44, 11), (55, 14), (59, 17), (48, 15), (36, 16))
    p('3a2a20', (9, 5), (21, 5), (31, 12), (31, 22), (25, 27), (13, 26), (7, 22), (4, 15))
    p('a8744a', (8, 12), (17, 7), (23, 9), (30, 14), (29, 21), (24, 25), (15, 24), (8, 20), (5, 15))
    p('a02a2a', (1, 9), (7, 7), (8, 3), (16, 0), (26, 2), (30, 7), (30, 13), (22, 11), (9, 11), (1, 12))
    p('c0302a', (8, 7), (13, 2), (22, 2), (27, 5), (28, 9), (18, 8))
    b('1a1a1a', 10, 14, 12, 15)
    b('6b4c38', 10, 20, 14, 21)
    p('a02a2a', (32, 18), (39, 22), (32, 34), (18, 35), (16, 30), (27, 25))
    p('c0302a', (32, 20), (36, 22), (30, 31), (23, 32), (23, 29))
    p('a8744a', (16, 28), (23, 29), (23, 33), (17, 35), (12, 34), (12, 31))
    return s.finish()


def dog(pose, scale=1):
    s = Sprite({'stand': 61, 'sit': 61, 'sleep': 30, 'lap': 38}[pose], scale)
    p, b = s.poly, s.box
    base, edge, shadow, light = 'c98f4e', '5a3a22', '8a5a2e', 'd8a060'

    def shape(*points, fill=base):
        p(fill, *points)

    if pose == 'stand':
        shape((25, 43), (35, 43), (35, 51), (30, 55), (30, 58), (20, 58),
              (20, 54), (25, 50), fill=shadow)
        shape((60, 41), (69, 41), (66, 55), (71, 56), (70, 59), (60, 59), fill=shadow)
        shape((19, 30), (12, 28), (6, 22), (7, 15), (10, 19), (12, 23), (24, 27), fill=edge)
        shape((19, 28), (12, 26), (8, 22), (8, 18), (12, 24), (23, 28))
        shape((18, 28), (23, 23), (40, 23), (53, 21), (60, 20), (70, 29), (69, 40),
              (63, 50), (62, 56), (66, 57), (66, 60), (54, 60), (53, 56), (55, 44),
              (40, 45), (31, 42), (27, 48), (17, 56), (22, 57), (22, 60),
              (10, 60), (10, 54), (18, 45), (16, 39), fill=edge)
        shape((20, 30), (24, 25), (41, 25), (55, 23), (60, 23), (68, 30), (67, 39),
              (61, 49), (60, 56), (64, 58), (55, 58), (57, 42), (40, 43),
              (30, 40), (25, 47), (15, 56), (20, 58), (12, 58), (12, 55),
              (20, 46), (18, 39))
        shape((22, 29), (25, 26), (40, 26), (52, 23), (57, 24), (43, 29), (29, 29), (23, 33), fill=light)
        shape((38, 40), (51, 38), (57, 32), (64, 32), (65, 39), (59, 45), (55, 42), (41, 43), fill='d8b080')
        hx, hy = 57, 0
    elif pose == 'sit':
        shape((25, 51), (15, 55), (6, 54), (4, 49), (7, 49), (10, 52), (26, 47), fill=edge)
        shape((29, 49), (15, 54), (8, 52), (14, 53), (28, 47))
        shape((31, 26), (39, 20), (55, 22), (60, 33), (55, 45), (56, 54), (62, 56),
              (62, 60), (20, 60), (16, 56), (16, 47), (20, 39), (27, 35), fill=edge)
        shape((32, 28), (40, 22), (54, 24), (58, 33), (53, 45), (54, 55), (60, 57),
              (60, 58), (21, 58), (18, 55), (18, 47), (22, 40), (30, 36))
        shape((54, 29), (57, 33), (52, 45), (53, 55), (50, 57), (48, 54), (48, 43), (51, 37), fill='d8b080')
        shape((25, 44), (32, 41), (39, 44), (42, 49), (40, 54), (47, 56),
              (37, 56), (39, 50), (36, 46), (29, 44), fill=shadow)
        hx, hy = 39, 0
    elif pose == 'sleep':
        shape((12, 12), (20, 7), (39, 7), (49, 10), (57, 18), (59, 23), (55, 28),
              (43, 29), (17, 29), (8, 26), (6, 21), (8, 16), fill=edge)
        shape((13, 14), (21, 9), (38, 9), (48, 12), (54, 18), (57, 22), (53, 26),
              (42, 27), (17, 27), (10, 24), (8, 21), (10, 17))
        shape((14, 14), (22, 10), (37, 10), (43, 12), (24, 13), (16, 16), (12, 20), (10, 19), fill=light)
        shape((12, 21), (16, 24), (24, 25), (38, 23), (45, 23), (49, 26), (38, 27), (18, 27), (12, 25), fill=shadow)
        hx, hy = 38, 0
    else:
        shape((10, 26), (20, 19), (41, 21), (57, 19), (66, 21), (72, 29), (85, 30),
              (87, 34), (83, 37), (49, 37), (34, 34), (25, 35), (8, 35), (4, 32), fill=edge)
        shape((11, 28), (21, 21), (41, 23), (57, 21), (65, 23), (70, 31), (84, 32),
              (85, 34), (81, 35), (49, 35), (34, 32), (25, 33), (8, 33), (7, 32))
        shape((13, 27), (22, 22), (39, 24), (55, 22), (58, 25), (39, 27), (23, 25), (15, 29), fill=light)
        shape((40, 31), (51, 31), (62, 28), (68, 31), (81, 33), (77, 35), (52, 35), fill='d8b080')
        hx, hy = 60, 0

    def h(color, *points):
        p(color, *((hx + x, hy + y) for x, y in points))

    low = pose == 'sleep'
    h(edge, (0, 12), (0, 3), (3, 0), (8, 3), (12, 10), (16, 10), (19, 2),
      (22, 1), (24, 5), (24, 14), (26, 17), (34, 18), (35, 22), (31, 25),
      (25, 25), (20, 29), (8, 28), (2, 24), (-3, 18))
    h(base, (2, 12), (2, 4), (4, 2), (7, 5), (11, 12), (17, 12), (20, 4),
      (22, 3), (22, 15), (25, 18), (32, 19), (33, 22), (30, 23), (24, 23),
      (19, 27), (9, 26), (4, 23), (-1, 18))
    h(shadow, (3, 5), (4, 3), (8, 8), (9, 12), (5, 11))
    h(shadow, (19, 11), (21, 5), (22, 5), (22, 13))
    h(light, (2, 17), (8, 13), (15, 13), (19, 15), (9, 16), (6, 20), (2, 21))
    h('3a2a1a', (23, 18), (27, 18), (34, 19), (34, 22), (30, 24), (23, 23), (20, 21))
    h('1a1a1a', (31, 18), (34, 18), (35, 20), (34, 21), (31, 21))
    h('1a1a1a', (15, 16), (18, 17), (19, 16 if low else 18),
      (19, 18 if low else 20), (15, 18 if low else 20))
    if not low:
        b('ffe8a0', hx + 16, 16, hx + 16, 17)
    h('8a6aa8', (-2, 21), (3, 25), (9, 28), (8, 29 if low else 34), (2, 29 if low else 32), (-4, 25))
    h('c4a8e0', (-2, 22), (4, 27), (8, 28), (7, 29 if low else 32), (2, 29 if low else 30), (-3, 25))
    if not low:
        b('bfe64a', hx + 3, 28, hx + 6, 30)
    return s.finish()


def lamb(scale=1):
    s = Sprite(23, scale)
    p, b = s.poly, s.box
    p('c9b38f', (5, 7), (10, 4), (25, 4), (29, 6), (31, 2), (36, 0), (43, 3),
      (46, 7), (46, 13), (42, 17), (35, 17), (32, 14), (29, 19), (28, 22),
      (23, 22), (21, 19), (13, 19), (12, 22), (7, 22), (6, 17), (3, 14), (3, 10))
    p('f4f1e8', (6, 8), (11, 5), (25, 5), (30, 8), (31, 14), (27, 18),
      (27, 21), (24, 21), (23, 17), (12, 18), (11, 21), (8, 21), (8, 16), (4, 13))
    p('ffffff', (7, 8), (12, 6), (17, 7), (21, 6), (26, 7), (27, 9),
      (22, 8), (19, 10), (14, 8), (10, 10), (6, 10))
    p('e8e0d0', (30, 6), (33, 2), (38, 2), (43, 5), (45, 8), (45, 12), (41, 16), (35, 16), (32, 13))
    b('f4f1e8', 33, 4, 40, 7)
    b('2a2a30', 40, 7, 41, 8)
    b('e23b3b', 41, 12, 44, 12)
    b('e23b3b', 42, 13, 42, 13)
    return s.finish()


def contact_sheet(sprites):
    widths = [max(72, sprite.width + 12) for sprite in sprites.values()]
    floor = 144
    sheet = Image.new('RGB', (178 + sum(widths), 182), '#e4ddd0')
    d = ImageDraw.Draw(sheet)
    d.rectangle((0, floor, sheet.width - 1, floor + 11), fill='#8a8580')
    for x in range(0, sheet.width, 24):
        d.rectangle((x, floor, x + 1, floor + 11), fill='#76716c')
    d.text((10, 8), 'CLASSIC  /  CHARACTER SCALE', fill='#2a2a30')
    d.line((15, floor - 108, 15, floor), fill='#4a2a1a')
    for units in range(0, 55, 6):
        y = floor - 2 * units
        d.line((15, y, 22 if units % 18 == 0 else 19, y), fill='#4a2a1a')
    d.text((24, floor - 115), '54 units', fill='#2a2a30')
    d.rectangle((61, floor - 84, 84, floor - 1), fill='#6b4c38')
    d.rectangle((65, floor - 80, 80, floor - 5), fill='#7a5840')
    d.rectangle((79, floor - 44, 82, floor - 41), fill='#d9c27a')
    d.rectangle((95, floor - 112, 126, floor - 1), fill='#e8ecf0')
    d.rectangle((95, floor - 60, 126, floor - 59), fill='#b0b4b8')
    d.rectangle((121, floor - 96, 122, floor - 81), fill='#8a8580')
    d.rectangle((121, floor - 48, 122, floor - 33), fill='#8a8580')
    d.rectangle((134, floor - 48, 169, floor - 45), fill='#d8ab70')
    d.rectangle((134, floor - 44, 169, floor - 17), fill='#c79a5e')
    d.rectangle((130, floor - 60, 136, floor - 17), fill='#b98a52')
    d.rectangle((136, floor - 16, 140, floor - 9), fill='#2a2a30')
    d.rectangle((162, floor - 16, 166, floor - 9), fill='#2a2a30')
    for center, label, size in ((72, 'Door', '42u'), (111, 'Fridge', '56u'), (152, 'Seat', '24u')):
        d.text((center, 159), label, fill='#2a2a30', anchor='mt')
        d.text((center, 171), size, fill='#2a2a30', anchor='mt')
    left = 178
    for (name, sprite), width in zip(sprites.items(), widths):
        center = left + width // 2
        sheet.paste(sprite, (center - sprite.width // 2, floor - sprite.height), sprite)
        label = name.removesuffix('.png').replace('_', ' ')
        d.text((center, 162), label, fill='#2a2a30', anchor='mt')
        left += width
    return sheet.resize((sheet.width * 2, sheet.height * 2), Image.Resampling.NEAREST)


def main():
    sprites = {
        'steve_walk.png': person('steve'),
        'steve_couch.png': couch_steve(),
        'wife.png': person('wife'),
        'kid.png': person('kid'),
        'burglar_short.png': person('short'),
        'burglar_tall.png': person('tall'),
        'pizza_driver.png': person('pizza'),
        'pizza_driver_fall.png': pizza_fall(),
        **{f'simba_{pose}.png': dog(pose) for pose in ('stand', 'sit', 'sleep', 'lap')},
        'lamb_toy.png': lamb(),
    }
    expected_heights = (108, 94, 108, 76, 92, 108, 108, 36, 61, 61, 30, 38, 23)
    assert len(sprites) == len(expected_heights)
    OUT.mkdir(parents=True, exist_ok=True)
    for (name, sprite), height in zip(sprites.items(), expected_heights):
        path = OUT / name
        sprite.save(path)
        with Image.open(path) as saved:
            assert saved.mode == 'RGBA' and saved.height == height
            assert {alpha for _, alpha in saved.getchannel('A').getcolors(256)} == {0, 255}
            assert saved.getbbox() == (3, 0, saved.width - 3, height)
            assert all('#%02x%02x%02x' % (r, g, b) in PALETTE
                       for _, (r, g, b, a) in saved.getcolors(256) if a)
            print(f'{name:<22} {saved.width:>3} x {saved.height:>3}')
    sheet = contact_sheet(sprites)
    sheet.save(ART / 'sheet_classic_chars.png')
    print(f'Validated {len(sprites)} sprites and rendered the {sheet.width} x {sheet.height} contact sheet.')


if __name__ == '__main__':
    main()
