"""Original Pass 3 clean-cluster paintings. Rebuild: python tools/art/remaining_assets.py.

House coordinates are captured read-only with node tools/art/house_capture.cjs.
The shared palette is authoritative: source CSS colors use nearest palette tones.
TV uses the shared surface quantizer, retaining exact UV/alpha bounds.
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont
from pixelize import PAL, pixelize, surface_pixelize
from cluster_art import Clusters
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT.parent.parent/'assets'
SIZES={'burglar_short':(20,36),'burglar_tall':(16,48),'car_lift':(96,44),'lobby_shack':(120,88),'house_bg':(1320,192),'tv_frame':(624,284)}

def surface(source,size):
    im=surface_pixelize(source,size).convert('RGBA')
    # Pillow's 256-entry palette pads the 36 approved entries with black.
    # Resolve any padded entry to the closest actual approved material tone.
    replacement={c:min(PAL,key=lambda p:sum((a-b)**2 for a,b in zip(c,p))) for c in set(im.convert('RGB').getdata()) if c not in PAL}
    if replacement:im.putdata([replacement.get(c[:3],c[:3])+(c[3],) for c in im.getdata()])
    return im

def burglar(tall=False):
    p=Clusters((14,46) if tall else (18,34),PAL)
    if tall:
        p.poly([(4,25),(11,25),(11,36),(9,42),(13,44),(13,45),(7,45),(6,35),(4,42),(6,44),(6,45),(0,45),(1,40),(2,31)],15)
        p.line([(4,29),(4,36),(2,42)],17)
        p.poly([(3,12),(9,11),(11,17),(11,27),(2,28),(1,21)],4)
        p.poly([(3,13),(5,14),(5,24),(2,25),(2,18)],16)
        p.line([(8,14),(7,17),(9,24)],5);p.dot(8,22,31)
        p.poly([(8,15),(10,16),(10,23),(12,26),(10,28),(8,25),(7,19)],16)
        p.rect((10,26,12,29),13);p.dot(12,27,14)
        p.poly([(4,3),(10,3),(10,6),(13,7),(13,9),(10,9),(10,12),(6,12),(4,9)],13)
        p.line([(6,4),(9,4),(9,6)],14);p.dot(10,7,4)
        p.line([(10,10),(12,10)],5)
        p.poly([(2,4),(3,1),(7,0),(10,1),(11,4),(13,4),(13,5),(2,5)],15)
        p.line([(4,1),(8,1),(10,3)],17)
    else:
        p.poly([(3,24),(14,24),(13,30),(16,32),(16,33),(10,33),(8,28),(6,31),(8,32),(8,33),(1,33),(2,29)],15)
        p.line([(4,26),(4,30),(3,31)],17)
        p.poly([(5,11),(12,11),(15,15),(16,23),(13,27),(5,27),(1,23),(1,17)],0)
        p.poly([(12,14),(15,16),(16,23),(13,26),(11,25)],31)
        for y in (15,19,23):p.rect((2,y,13,y+1),15)
        p.poly([(5,13),(7,15),(6,21),(9,23),(8,26),(4,25),(3,21),(3,16)],0)
        p.line([(4,15),(4,20)],11);p.rect((7,23,10,26),13);p.dot(10,24,14)
        p.poly([(6,3),(12,3),(13,6),(16,7),(16,9),(13,9),(12,12),(7,12),(5,8)],13)
        p.rect((7,4,10,7),14);p.dot(12,7,4);p.line([(13,10),(15,10)],5)
        p.poly([(4,5),(4,2),(7,0),(11,0),(13,2),(13,5)],30)
        p.line([(6,2),(10,1)],25);p.rect((4,5,13,6),23)
    return pixelize(p.im,SIZES['burglar_tall' if tall else 'burglar_short'])

def car():
    p=Clusters((94,42),PAL)
    p.poly([(5,24),(10,19),(20,18),(30,5),(58,4),(72,17),(87,20),(92,25),(92,33),(5,33)],0)
    p.poly([(9,28),(88,28),(88,34),(5,34),(4,30)],31)
    p.poly([(22,18),(32,7),(57,6),(68,17)],15)
    p.poly([(25,16),(33,8),(43,8),(43,17),(25,17)],17)
    p.poly([(47,8),(56,8),(65,17),(47,17)],17)
    p.line([(28,15),(34,9),(40,9)],18);p.line([(49,9),(55,9),(59,13)],18)
    p.line([(9,21),(20,20),(72,20),(86,23)],11)
    p.line([(45,20),(45,30),(64,30),(66,22)],1);p.rect((50,21,55,22),15)
    p.rect((3,23,7,27),30);p.rect((87,24,92,27),11);p.rect((89,30,93,32),16)
    p.rect((67,17,73,19),15)
    for x in (21,74):
        p.d.ellipse((x-8,26,x+8,41),fill=PAL[4]+(255,))
        p.d.ellipse((x-5,29,x+5,38),fill=PAL[16]+(255,))
        p.d.ellipse((x-3,30,x+3,36),fill=PAL[18]+(255,))
        p.rect((x-1,32,x+1,35),1);p.dot(x-2,31,11)
    return pixelize(p.im,SIZES['car_lift'])

def shack():
    p=Clusters((118,86),PAL)
    p.poly([(1,78),(15,73),(101,72),(116,79),(117,85),(0,85)],10)
    p.poly([(12,80),(36,77),(100,77),(107,81),(83,83),(23,83)],2)
    p.rect((18,27,99,77),7);p.rect((91,29,99,77),6)
    for y in range(31,76,8):
        p.line([(19,y),(90,y)],9);p.line([(19,y+6),(98,y+6)],6)
        for x in range(24,89,23):p.line([(x,y+3),(x+10,y+3),(x+13,y+2)],8)
    p.rect((19,28,23,77),2);p.rect((94,28,98,77),6)
    p.poly([(6,30),(24,8),(83,1),(110,26),(111,31)],3)
    p.poly([(10,27),(26,10),(81,4),(105,26)],6)
    for y,a,b in [(11,29,81),(16,24,87),(21,18,95),(26,13,103)]:
        p.line([(a,y),(b,y-3)],7,2);p.line([(a+4,y+1),(b,y-2)],5)
    p.line([(7,29),(109,28)],9,2)
    p.rect((62,38,86,77),3);p.rect((65,40,83,76),6)
    p.line([(66,41),(66,74)],8);p.line([(73,42),(73,75)],3);p.rect((79,56,81,58),10)
    p.rect((29,38,55,59),3);p.rect((32,41,52,55),15)
    p.rect((33,42,40,53),17);p.rect((44,42,51,53),16)
    p.line([(34,43),(38,43),(34,48)],18);p.rect((41,41,43,55),2)
    p.rect((27,57,57,60),9);p.rect((60,77,89,80),6)
    for x,y in [(8,81),(32,84),(104,80),(112,83)]:p.line([(x,y),(x+3,y)],11)
    return pixelize(p.im,SIZES['lobby_shack'])

def house():
    layout=json.loads((ROOT/'house_layout.json').read_text())
    im=Image.new('RGB',(1320,192),PAL[4]);d=ImageDraw.Draw(im)
    # Exact original rectangles; y=144 is top beam, FLOOR=234 -> native y=180.
    for x,y,w,h,c in layout['rects']:
        if w<=0 or h<=0:continue
        box=(round(x*2),round((y-144)*2),round((x+w)*2)-1,round((y+h-144)*2)-1)
        if box[2]<0 or box[0]>=1320 or box[3]<0 or box[1]>=192:continue
        # Keep the source material families when its CSS tone is outside PAL.
        semantic={'#9ad4f5':18,'#cfe4ec':18,'#bcd4dc':18,'#c8dce4':18,
                  '#7d848c':1,'#6c737b':16,'#cfc6b6':31,'#f0e6c8':0,
                  '#d8cce4':28,'#f4e8a0':10,'#5f9f4a':21}
        d.rectangle(box,fill=PAL[semantic[c]] if c in semantic else c)
    for line in layout['lines']:
        if len(line)>1:d.line([(round(x*2),round((y-144)*2)) for x,y in line],fill=PAL[18],width=1)
    im=surface(im,(1320,192))
    # Sparse intentional seams within the source's material regions, no noise.
    d=ImageDraw.Draw(im)
    for a,b in [(320,398),(140,172),(232,260)]:
        for y in (151,160,169):
            d.line((a,y,b,y),fill=PAL[6])
    # Couch upholstery stitch clusters stay inside the source couch silhouette.
    for x in range(54,110,8):d.line((x,139,x+3,139),fill=PAL[9])
    return im

def tv():
    # drawTV bezel starts at (TX-6,TY-6)=(4,0). 2x cutout=(12,12,600,260).
    im=Image.new('RGBA',(624,284),PAL[4]+(255,));d=ImageDraw.Draw(im)
    d.rectangle((1,1,622,2),fill=PAL[16]);d.line((1,3,1,281),fill=PAL[16])
    d.rectangle((6,6,617,277),outline=PAL[15],width=2)
    d.line((10,10,613,10),fill=PAL[1]);d.line((10,10,10,273),fill=PAL[16])
    d.line((612,12,612,272),fill=PAL[3]);d.line((12,272,612,272),fill=PAL[3])
    for x in range(550,600,5):d.line((x,278,x+2,278),fill=PAL[16])
    d.rectangle((311,277,314,279),fill=PAL[29]);d.rectangle((12,12,611,271),fill=(0,0,0,0))
    alpha=im.getchannel('A');im=surface(im,im.size);im.putalpha(alpha)
    return im

def build():
    sprites={'burglar_short':burglar(),'burglar_tall':burglar(True),'car_lift':car(),'lobby_shack':shack(),'house_bg':house(),'tv_frame':tv()}
    sheet=Image.new('RGBA',(2544,1820),PAL[0]+(255,));d=ImageDraw.Draw(sheet);font=ImageFont.load_default_imagefont()
    slots={'burglar_short':(24,55),'burglar_tall':(150,55),'car_lift':(270,55),'lobby_shack':(710,55),'house_bg':(24,485),'tv_frame':(24,670)}
    # House native preview below the prop row, TV takes a full 4x row beneath.
    slots['burglar_tall']=(180,55);slots['car_lift']=(350,55);slots['lobby_shack']=(800,55)
    slots['house_bg']=(24,445);slots['tv_frame']=(24,680)
    d.text((24,14),'PASS 3 / REMAINING SIX / SHARED 36-COLOR PALETTE',font=font,fill=PAL[3])
    for name,im in sprites.items():
        assert im.size==SIZES[name]
        assert set(im.getchannel('A').getdata())<={0,255}
        assert all(c[:3] in PAL for c in im.getdata() if c[3])
        if name not in ('house_bg','tv_frame'):
            box=im.getbbox();assert box[3]==im.height and abs(box[0]-(im.width-box[2]))<=1
        im.save(ASSETS/(name+'.png'))
        x,y=slots[name];scale=1 if name=='house_bg' else 4
        d.text((x,y-17),f'{name} / {im.width}x{im.height} / {scale}x',font=font,fill=PAL[3])
        preview=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
        # Checker visible through all transparent pixels, especially the TV screen.
        for yy in range(y,y+preview.height,16):
            for xx in range(x,x+preview.width,16):
                d.rectangle((xx,yy,min(xx+15,x+preview.width-1),min(yy+15,y+preview.height-1)),fill=PAL[31 if ((xx-x)//16+(yy-y)//16)%2 else 0])
        sheet.alpha_composite(preview,(x,y))
    assert sprites['tv_frame'].crop((12,12,612,272)).getchannel('A').getextrema()==(0,0)
    sheet.save(ROOT/'sheet2.png')
    print('Six assets validated: exact sizes, shared palette, binary alpha, sprite anchors, exact TV cutout. sheet2.png: 2544x1820.')
    return sprites,sheet

if __name__=='__main__':build()
