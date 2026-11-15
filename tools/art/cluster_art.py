"""Pass 3 revision: native-resolution, deliberately placed pixel clusters.

No noise, diffusion, or per-pixel lighting on characters. The approval sheet
passes these paintings through pixelize.py's shared palette/anchor finalizer.
Numbers below are indices into the unchanged shared 32-color palette.
"""
from PIL import Image, ImageDraw


class Clusters:
    def __init__(self, size, palette):
        self.im = Image.new('RGBA', size)
        self.d = ImageDraw.Draw(self.im)
        self.palette = palette

    def poly(self, points, color):
        self.d.polygon(points, fill=self.palette[color] + (255,))

    def rect(self, box, color):
        self.d.rectangle(box, fill=self.palette[color] + (255,))

    def line(self, points, color, width=1):
        self.d.line(points, fill=self.palette[color] + (255,), width=width)

    def dot(self, x, y, color):
        self.im.putpixel((x, y), self.palette[color] + (255,))


def dog(palette, finish, sitting=False):
    p = Clusters((38,46) if sitting else (50,42), palette)
    if not sitting:
        # Tail rises in a curved mid-wag; far legs precede the body.
        p.poly([(12,17),(7,16),(3,12),(1,7),(2,4),(4,9),(6,12),(13,13)],8)
        p.line([(2,6),(3,10),(6,14),(10,15)],10)
        p.poly([(20,25),(24,26),(25,31),(22,36),(22,38),(26,39),(26,40),(19,40),(19,36),(21,31)],6)
        p.poly([(37,24),(40,24),(43,29),(44,37),(47,39),(47,40),(42,40),(41,36),(40,30)],6)
        p.line([(42,30),(43,37),(45,39)],7)
        # Strong level back, tucked belly, deep chest and shoulder.
        p.poly([(10,16),(15,13),(29,13),(35,11),(40,14),(41,22),(38,29),(31,30),(27,26),(19,27),(15,30),(10,26)],8)
        p.poly([(11,16),(16,13),(29,13),(33,12),(32,16),(22,17),(16,19)],7)
        p.line([(12,17),(16,15),(27,15)],9)
        p.poly([(26,24),(32,25),(36,21),(38,23),(36,28),(31,29)],10)
        # Near hind leg has a defined thigh, hock, ankle and broad paw.
        p.poly([(12,22),(17,22),(19,26),(16,32),(12,36),(12,39),(16,40),(16,41),(8,41),(8,37),(12,30),(10,27)],8)
        p.poly([(12,23),(15,24),(16,27),(13,32),(10,36),(10,39),(12,39),(13,40),(9,40),(9,37),(13,29)],9)
        p.poly([(31,22),(36,23),(36,37),(39,39),(40,41),(33,41),(32,37)],8)
        p.poly([(31,23),(33,24),(34,36),(34,39),(37,40),(33,40),(32,36)],10)
        p.line([(11,40),(11,41)],6);p.line([(14,40),(14,41)],6)
        p.dot(36,41,6);p.dot(38,41,6)
        # Neck slopes into shoulder rather than perching on the back.
        p.poly([(30,20),(32,12),(34,9),(40,10),(42,18),(38,26),(34,26)],8)
        p.poly([(31,20),(34,14),(36,15),(35,23),(34,25)],9)
        hx,hy=34,5
    else:
        p.poly([(13,39),(7,38),(3,34),(1,29),(2,26),(4,30),(6,34),(12,35),(16,39)],8)
        p.line([(2,28),(3,32),(6,36),(10,37)],10)
        # Far rear paw and far straight foreleg stay visibly darker.
        p.poly([(16,33),(23,34),(22,41),(26,43),(26,44),(17,44)],6)
        p.poly([(28,23),(31,24),(31,41),(34,43),(34,44),(28,44),(27,39)],7)
        p.poly([(12,26),(20,21),(26,20),(29,28),(27,37),(23,42),(17,44),(10,43),(8,39),(8,32)],8)
        p.poly([(12,27),(19,23),(23,24),(21,29),(15,32),(12,37),(12,41),(10,40),(10,33)],9)
        p.poly([(14,34),(18,32),(22,34),(22,40),(25,42),(25,44),(15,44),(12,42),(12,38)],8)
        p.line([(15,35),(18,34),(20,36),(20,40),(18,42)],7)
        # Upright chest and two unbent front legs, with space between paws.
        p.poly([(23,16),(29,16),(31,24),(28,31),(25,34),(22,29),(20,24)],8)
        p.poly([(26,21),(29,22),(28,29),(26,32),(25,40),(27,43),(29,44),(23,44),(22,41),(23,31),(22,27)],10)
        p.line([(24,29),(24,40),(25,42)],11)
        p.dot(25,44,7);p.dot(27,44,7)
        hx,hy=24,7
    # Medium upright ears, broad skull and dark interiors.
    p.poly([(hx-3,hy+3),(hx-5,hy-4),(hx-3,hy-5),(hx+1,hy+1)],8)
    p.poly([(hx+4,hy+1),(hx+6,hy-5),(hx+8,hy-4),(hx+8,hy+5)],8)
    p.line([(hx-3,hy-2),(hx-2,hy+1)],5)
    p.line([(hx+6,hy-2),(hx+6,hy+2)],5)
    p.poly([(hx-3,hy+3),(hx,hy+1),(hx+6,hy+1),(hx+9,hy+4),(hx+9,hy+10),(hx+6,hy+14),(hx+1,hy+13),(hx-3,hy+9)],8)
    p.poly([(hx-2,hy+3),(hx+1,hy+2),(hx+5,hy+2),(hx+5,hy+4),(hx+1,hy+5),(hx-1,hy+8)],9)
    p.poly([(hx,hy+9),(hx+4,hy+9),(hx+5,hy+12),(hx+2,hy+12)],7)
    # Short, deep muzzle with a blunt vertical nose and a compact lower jaw.
    if sitting:
        p.poly([(hx+5,hy+6),(hx+10,hy+5),(hx+10,hy+9),(hx+7,hy+12),(hx+4,hy+11),(hx+3,hy+9)],5)
        p.line([(hx+6,hy+6),(hx+8,hy+6)],16)
        p.rect((hx+9,hy+5,hx+10,hy+7),4)
        p.line([(hx+6,hy+10),(hx+9,hy+9)],4)
        p.dot(hx+7,hy+11,25)
    else:
        p.poly([(hx+5,hy+8),(hx+10,hy+8),(hx+10,hy+13),(hx+6,hy+14),(hx+3,hy+11)],5)
        p.line([(hx+6,hy+9),(hx+8,hy+9)],16)
        p.rect((hx+9,hy+8,hx+10,hy+10),4)
        p.line([(hx+5,hy+12),(hx+9,hy+12)],4)
        p.dot(hx+8,hy+13,25)
    p.line([(hx+3,hy+5),(hx+6,hy+5)],6)
    p.rect((hx+4,hy+6,hx+6,hy+7),4)
    p.dot(hx+5,hy+7,9);p.dot(hx+5,hy+6,11)
    p.line([(hx-2,hy+14),(hx+2,hy+16),(hx+7,hy+14)],27,2)
    p.line([(hx-2,hy+13),(hx+2,hy+15),(hx+6,hy+13)],28)
    p.rect((hx+5,hy+14,hx+7,hy+16),29)
    p.dot(hx+6,hy+15,19)
    return finish(p.im,(40,48) if sitting else (52,44))


def human(palette, finish, role='steve', seated=False):
    kid=role=='kid';wife=role=='wife'
    p=Clusters((30,46) if seated else ((12,30) if kid else (18,42)),palette)
    if kid:
        # Cap over blond side tufts, saturated yellow sleeved tee and shorts.
        p.poly([(3,21),(6,21),(5,27),(3,28),(2,27)],13)
        p.rect((8,22,10,27),14)
        p.rect((1,28,5,29),15);p.rect((8,28,11,29),15)
        p.line([(2,28),(4,28)],18);p.line([(9,28),(11,28)],18)
        p.poly([(2,19),(10,19),(10,23),(7,23),(6,21),(5,23),(2,23)],16)
        p.line([(3,20),(9,20)],17)
        p.poly([(3,10),(8,10),(10,13),(9,19),(2,19),(1,14)],32)
        p.line([(3,11),(6,11)],11)
        p.line([(9,14),(8,17),(9,18)],9)
        p.line([(2,18),(8,18)],8)
        p.poly([(1,14),(3,14),(3,18),(4,20),(2,21),(0,18)],14)
        p.poly([(9,14),(11,14),(11,18),(10,20),(8,19),(9,17)],13)
        p.poly([(2,11),(3,12),(3,15),(0,15),(0,13)],32)
        p.poly([(8,11),(10,12),(11,13),(11,15),(9,15)],32)
        p.line([(0,15),(2,15)],9);p.line([(9,15),(11,15)],9)
        p.poly([(2,2),(7,1),(10,3),(10,5),(11,6),(10,7),(9,7),(9,9),(6,11),(3,9),(1,6)],14)
        p.line([(7,4),(9,4)],7);p.dot(8,5,4);p.dot(10,6,13)
        p.line([(7,8),(8,8)],5)
        p.rect((1,3,3,6),9)
        p.line([(1,4),(2,4)],10)
        p.dot(9,4,9)
        p.poly([(1,3),(1,2),(3,0),(8,0),(10,2),(10,3)],16)
        p.line([(2,2),(4,1),(7,1)],17)
        p.line([(1,3),(11,3)],15)
        p.dot(3,6,13)
        return finish(p.im,(14,36))
    # Adults: 12px head / 42px height, relaxed asymmetric stance.
    if seated:
        p.poly([(5,26),(20,26),(24,29),(23,38),(27,43),(27,45),(21,45),(18,40),(18,33),(7,33)],16)
        p.poly([(7,29),(18,30),(18,35),(20,43),(23,44),(23,45),(17,45),(14,41),(12,34),(7,34)],17)
        p.line([(7,29),(16,30),(16,35)],18)
        p.line([(17,45),(23,45)],15);p.line([(22,44),(27,44)],15)
        cx=7;ty=14
    else:
        p.poly([(4,27),(9,27),(8,35),(5,39),(6,40),(7,41),(1,41),(1,39),(4,34)],16)
        p.poly([(9,27),(13,27),(13,38),(16,40),(16,41),(10,41),(9,37),(8,33)],17)
        p.line([(11,29),(11,37),(12,38)],18)
        p.line([(1,41),(6,41)],15);p.line([(10,41),(16,41)],15)
        cx=7;ty=14
    shirt=4 if wife else 21
    p.poly([(cx-3,ty),(cx+2,ty-1),(cx+6,ty+3),(cx+5,ty+13),(cx-4,ty+13),(cx-5,ty+6)],shirt)
    if not wife:
        # Large interlocking camo islands, plus hood, cuff and pocket seams.
        p.poly([(cx-4,ty+2),(cx-1,ty+1),(cx+1,ty+4),(cx-1,ty+6),(cx-4,ty+5)],22)
        p.poly([(cx+2,ty+1),(cx+5,ty+3),(cx+3,ty+5),(cx+1,ty+4)],19)
        p.poly([(cx-2,ty+7),(cx+1,ty+6),(cx+2,ty+9),(cx+4,ty+10),(cx+2,ty+12),(cx-1,ty+11)],20)
        p.poly([(cx-4,ty-1),(cx,ty-2),(cx+3,ty),(cx+1,ty+2),(cx-2,ty+1)],20)
        p.line([(cx-2,ty),(cx,ty+1),(cx+2,ty)],22)
        p.line([(cx,ty+3),(cx,ty+5)],10)
        p.line([(cx-3,ty+11),(cx,ty+12)],19)
        p.line([(cx-4,ty+13),(cx+4,ty+13)],19)
    else:
        p.line([(cx-3,ty),(cx-2,ty+7)],17,2)
        p.line([(cx+3,ty),(cx+3,ty+7)],17,2)
        p.rect((cx-2,ty+6,cx+4,ty+13),17)
        p.rect((cx,ty+8,cx+3,ty+10),16)
        p.line([(cx,ty+11),(cx+3,ty+11)],18)
        p.dot(cx-1,ty+6,10);p.dot(cx+3,ty+6,10)
    # Both arms have their own silhouette and visible hands.
    p.poly([(cx-4,ty+3),(cx-3,ty+6),(cx-4,ty+10),(cx-3,ty+13),(cx-5,ty+14),(cx-6,ty+10)],4 if wife else 20)
    p.rect((cx-5,ty+12,cx-3,ty+15),13);p.dot(cx-4,ty+12,14)
    if seated:
        p.poly([(cx+3,ty+3),(cx+6,ty+4),(cx+6,ty+9),(cx+12,ty+9),(cx+13,ty+12),(cx+4,ty+12),(cx+2,ty+8)],20)
        p.line([(cx+4,ty+4),(cx+5,ty+8),(cx+10,ty+10)],22)
        p.rect((cx+10,ty+10,cx+13,ty+12),14)
        p.poly([(cx+14,ty+8),(cx+19,ty+8),(cx+21,ty+10),(cx+20,ty+12),(cx+16,ty+11),(cx+13,ty+12)],4)
        p.dot(cx+16,ty+9,18);p.dot(cx+19,ty+9,30)
        p.rect((cx+12,ty+9,cx+14,ty+11),14)
    else:
        p.poly([(cx+4,ty+3),(cx+6,ty+5),(cx+6,ty+10),(cx+4,ty+12),(cx+2,ty+11),(cx+4,ty+8)],4 if wife else 20)
        p.rect((cx+2,ty+11,cx+4,ty+14),14)
        p.dot(cx+4,ty+13,12)
    p.rect((cx,11,cx+3,14),13)
    # Broad stylized face with brow, eye, nose and a separate mouth.
    p.poly([(cx-3,3),(cx+2,2),(cx+5,4),(cx+5,7),(cx+7,8),(cx+6,9),(cx+4,9),(cx+4,11),(cx+1,13),(cx-2,11),(cx-3,8)],13)
    p.poly([(cx-1,4),(cx+3,4),(cx+4,6),(cx+3,9),(cx+1,10),(cx-1,8)],14)
    p.line([(cx+2,5),(cx+4,5)],5);p.dot(cx+3,6,4)
    p.dot(cx+6,8,14);p.line([(cx+2,10),(cx+3,10)],5)
    if wife:
        p.poly([(cx-4,6),(cx-4,3),(cx-2,1),(cx+2,1),(cx+5,3),(cx+4,4),(cx,3),(cx-1,6),(cx-2,9)],24)
        p.line([(cx-3,3),(cx,2),(cx+2,2)],26)
        p.poly([(cx-5,2),(cx-5,0),(cx-2,0),(cx,2),(cx-1,4),(cx-4,4)],25)
        p.line([(cx-4,1),(cx-2,1)],26)
        p.line([(cx-2,6),(cx+1,6),(cx+2,5),(cx+5,5),(cx+5,8),(cx+2,8),(cx+1,6)],23)
        p.dot(cx+2,5,26);p.dot(cx+4,7,18)
    else:
        p.poly([(cx-4,7),(cx-4,3),(cx-2,0),(cx+2,0),(cx+4,2),(cx+5,4),(cx+1,3),(cx-1,4),(cx-1,7),(cx-2,8)],5)
        p.line([(cx-3,3),(cx-1,1),(cx+1,1)],6)
        p.line([(cx-2,9),(cx,11),(cx+2,12),(cx+4,10)],6)
        p.dot(cx+2,10,5)
    p.dot(cx-1,8,12)
    return finish(p.im,(32,48) if seated else (20,44))
