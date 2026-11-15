"""Export approved Pass 3 paintings at native resolution; no lineup changes."""
from PIL import Image, ImageDraw, ImageFont
from pixelize import PAL, ROOT, pixelize, dog, human, lamb
from cluster_art import Clusters, dog as paint_dog


def reclining(sleeping=False):
    p = Clusters((54,22) if sleeping else (66,42), PAL)
    if sleeping:
        # Rounded back, tucked haunch and curled tail surround the resting head.
        p.poly([(3,12),(5,7),(12,3),(24,2),(34,5),(39,10),(43,15),(42,20),(12,21),(5,18)],8)
        p.poly([(5,10),(10,5),(23,3),(31,5),(28,7),(16,6),(10,9)],9)
        p.poly([(6,13),(11,11),(17,12),(21,16),(32,18),(35,21),(12,21),(5,18)],7)
        p.poly([(3,12),(6,14),(7,17),(14,19),(23,18),(27,19),(24,21),(12,21),(5,19),(2,16)],8)
        p.line([(5,14),(7,17),(13,18),(20,18)],10)
        p.poly([(31,12),(38,11),(44,15),(45,19),(39,21),(28,20),(25,18)],10)
        # Folded ears and a closed right-facing eye, muzzle resting on paws.
        p.poly([(31,13),(30,7),(33,6),(37,10),(40,9),(44,12),(45,16),(42,19),(34,18),(30,16)],8)
        p.poly([(31,8),(34,9),(35,12),(32,12)],5)
        p.line([(35,11),(38,10),(40,11)],9)
        p.line([(38,13),(39,14),(41,13)],5)
        p.poly([(41,15),(48,15),(49,17),(48,19),(42,19),(39,17)],5)
        p.rect((47,15,49,16),4)
        p.line([(42,18),(46,18)],4)
        p.line([(29,16),(32,18),(35,18)],27)
        p.dot(34,18,29)
        p.line([(39,20),(43,20)],7)
    else:
        # Long relaxed torso; tucked rear legs and forepaws drape over a lap.
        p.poly([(12,26),(7,25),(3,21),(2,17),(4,18),(7,22),(14,23)],8)
        p.line([(3,19),(6,23),(10,24)],10)
        p.poly([(9,28),(13,22),(22,20),(37,21),(46,24),(49,30),(44,34),(20,34),(12,32)],8)
        p.poly([(12,25),(18,21),(29,21),(36,22),(34,24),(22,24),(16,27)],9)
        p.poly([(14,29),(22,27),(28,29),(28,32),(21,34),(13,32)],7)
        p.line([(15,29),(20,28),(24,30)],8)
        p.poly([(29,30),(41,28),(47,31),(51,35),(58,36),(60,39),(51,40),(44,35),(34,34)],7)
        p.poly([(39,27),(44,27),(48,31),(48,35),(54,38),(56,40),(48,41),(43,37),(41,33)],10)
        p.line([(43,30),(44,35),(49,39)],11)
        p.dot(51,40,7); p.dot(54,40,7)
        p.poly([(40,28),(42,18),(45,13),(51,15),(53,23),(49,31),(44,32)],8)
        p.poly([(42,26),(44,20),(46,21),(46,28),(44,30)],9)
        # Reuse the exact approved upright ears, face, muzzle and collar.
        raw = paint_dog(PAL, lambda im, size: im)
        p.im.alpha_composite(raw.crop((29,0,46,23)), (42,3))
    return pixelize(p.im, (56,24) if sleeping else (68,44))


def seated():
    approved = human(seated=True)
    out = Image.new('RGBA',(32,48))
    out.alpha_composite(approved.crop((0,0,32,38)),(0,4))
    out.alpha_composite(approved.crop((0,42,32,48)),(0,42))
    box = out.getbbox()
    cropped = out.crop(box)
    out = Image.new('RGBA',(32,48))
    out.alpha_composite(cropped,((32-cropped.width)//2,48-cropped.height))
    return out


def main():
    sprites = {
        'simba_stand': dog(), 'simba_sit': dog(True),
        'simba_sleep': reclining(True), 'simba_lap': reclining(),
        'lamb_toy': lamb(), 'steve_couch': seated(),
        'steve_walk': human(), 'wife': human('wife'), 'kid': human('kid'),
    }
    sizes = [(52,44),(40,48),(56,24),(68,44),(24,20),(32,48),(20,44),(20,44),(14,36)]
    sheet = Image.new('RGB',(276,218),PAL[0])
    d = ImageDraw.Draw(sheet)
    font = ImageFont.load_default_imagefont()
    for i, ((name, sprite), size) in enumerate(zip(sprites.items(),sizes)):
        assert sprite.size == size, name
        box = sprite.getbbox()
        assert box[3] == size[1], name
        assert abs(box[0]-(size[0]-box[2])) <= 1, name
        assert set(sprite.getchannel('A').tobytes()) == {0,255}, name
        assert {c[:3] for c in sprite.getdata() if c[3]} <= set(PAL), name
        sprite.save(ROOT.parent.parent/'assets'/f'{name}.png')
        x = (i%3)*92; y = (i//3)*72
        d.line((x+3,y+53,x+88,y+53),fill=PAL[31])
        sheet.paste(sprite,(x+(92-size[0])//2,y+54-size[1]),sprite)
        d.text((x+3,y+58),name,fill=PAL[3],font=font)
        print(f'{name}: {size}, bounds {box}, binary alpha, palette, bottom-center OK')
    sheet.resize((1104,872),Image.Resampling.NEAREST).save(ROOT/'sheet.png')


if __name__ == '__main__':
    main()
