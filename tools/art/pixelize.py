"""Pass 3 approval lineup. Original pixel painting; no individual exports.

Run: python tools/art/pixelize.py (Pillow required).
Characters use explicit clean clusters in cluster_art.py; the retained props
use the original material painter below. Shared finalizer resizes,
quantizes without diffusion, thresholds alpha, adds tinted 1px silhouettes,
and centers the cropped result on its bottom anchor. Only lineup.png is saved.
The table's 44px Steve limit takes precedence over its approximate 46px scale.
"""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
HEX = (
    'e4ddd0','8a8580','c79a5e','4a2a1a',
    '302d32','554137','805735','a87340','c98f4e','dfa960','efd099',
    'fff0d5','b98468','d8a17d','efc39b',
    '293948','40576a','648092','93a8a5',
    '353c2d','505b3c','758052','9a9e6b',
    '69435c','a76080','d98ba3','efb4bc',
    '776080','b6a0c6','b6ce4c','b24943','b9ad98')
PAL = [tuple(bytes.fromhex(c)) for c in HEX]
BAYER = ((0,8,2,10),(12,4,14,6),(3,11,1,9),(15,7,13,5))
MATS = {'fur':(6,7,8,9,10),'cream':(31,0,11),'wood':(3,6,7,2,9),
        'couch':(6,7,2,9,10),'skin':(12,13,14),'denim':(15,16,17,18),
        'olive':(19,20,21,22),'dark':(4,5,16),'hair':(3,5,6,7),
        'pink':(23,24,25,26),'lilac':(23,27,28),'gold':(7,8,9,10)}

class Paint:
    def __init__(self,size): self.im=Image.new('RGBA',size); self.d=ImageDraw.Draw(self.im)
    def solid(self,kind,coords,c,width=1):
        f=getattr(self.d,kind)
        if kind=='line': f(coords,fill=PAL[c],width=width)
        else: f(coords,fill=PAL[c])
    def shape(self,kind,coords,mat,phase=0):
        mask=Image.new('L',self.im.size);d=ImageDraw.Draw(mask);getattr(d,kind)(coords,fill=255)
        box=mask.getbbox()
        if not box:return
        x0,y0,x1,y1=box; ramp=MATS[mat]; pix=mask.load()
        for y in range(y0,y1):
            for x in range(x0,x1):
                if not pix[x,y]:continue
                u=(x-x0)/max(1,x1-x0-1);v=(y-y0)/max(1,y1-y0-1)
                # Discrete light bands with ordered transitions, no gradients in output.
                light=0.92-0.46*u-0.38*v
                if mat=='fur':
                    clump=((x//3+2*(y//2)+phase)%7)
                    light+=0.13 if clump in (0,1) else (-0.10 if clump==5 else 0)
                elif mat in ('denim','olive','couch','lilac'):
                    light+=0.10 if (x+2*y+phase)%5==0 else -0.04
                    if mat=='olive' and (x//3+y//3)%4==1:light-=0.25
                elif mat=='wood':
                    light+=0.15 if (x+int(2*math.sin(y/7)))%7==0 else -0.06
                elif mat=='cream':light+=0.18 if (x+2*y)%5<2 else -0.08
                n=max(0,min(len(ramp)-1,light*(len(ramp)-1)))
                idx=int(n)+(BAYER[y%4][x%4]/16 < n-int(n))
                self.im.putpixel((x,y),PAL[ramp[min(idx,len(ramp)-1)]]+(255,))
    def poly(self,pts,m,phase=0): self.shape('polygon',pts,m,phase)
    def oval(self,box,m,phase=0): self.shape('ellipse',box,m,phase)
    def rect(self,box,m,phase=0): self.shape('rectangle',box,m,phase)
    def line(self,pts,c,w=1):self.solid('line',pts,c,w)
    def dot(self,x,y,c):self.im.putpixel((x,y),PAL[c]+(255,))

def pixelize(source,size):
    """Shared non-antialiased size/palette/alpha/outline/bottom-center pipeline.

    Fit within an inset so the subsequently added outline never exceeds size.
    Accepts a Pillow image; returns an RGBA image, never writes a sprite.
    """
    src=source.convert('RGBA');box=src.getbbox()
    if not box:raise ValueError('Empty artwork')
    src=src.crop(box);w,h=size
    scale=min((w-2)/src.width,(h-2)/src.height)
    src=src.resize((max(1,round(src.width*scale)),max(1,round(src.height*scale))),Image.Resampling.NEAREST)
    alpha=src.getchannel('A').point(lambda a:255 if a>=128 else 0)
    palette=Image.new('P',(1,1));palette.putpalette([v for c in PAL for v in c]+[0]*(768-len(PAL)*3))
    src=src.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');src.putalpha(alpha)
    out=Image.new('RGBA',(src.width+2,src.height+2));out.paste(src,(1,1))
    for y in range(out.height):
        for x in range(out.width):
            if out.getpixel((x,y))[3]:continue
            neighbors=[src.getpixel((xx-1,yy-1)) for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)) if 1<=xx<=src.width and 1<=yy<=src.height and src.getpixel((xx-1,yy-1))[3]]
            if neighbors:
                c=neighbors[0][:3]
                # Brown, blue, olive or plum tinted outlines, all in the palette.
                tint=15 if c[2]>c[0]*1.05 else (19 if c[1]>c[0]*1.03 else (23 if c[2]>c[1]*1.1 else 3))
                out.putpixel((x,y),PAL[tint]+(255,))
    out=out.crop(out.getbbox());result=Image.new('RGBA',size);result.paste(out,((w-out.width)//2,h-out.height))
    assert result.getbbox()[3]==h
    assert abs(result.getbbox()[0]-(w-result.getbbox()[2]))<=1
    assert set(result.getchannel('A').getdata())<={0,255}
    assert all(c[:3] in PAL for c in result.getdata() if c[3])
    return result

def dog(sitting=False):
    from cluster_art import dog as paint_dog
    return paint_dog(PAL, pixelize, sitting)


def human(role='steve', seated=False):
    from cluster_art import human as paint_human
    return paint_human(PAL, pixelize, role, seated)

def lamb():
    p=Paint((24,20));p.oval((2,5,17,15),'cream')
    for box in [(3,12,6,18),(12,12,15,18)]:p.oval(box,'cream')
    p.oval((15,4,21,13),'cream');p.oval((12,3,17,7),'cream');p.oval((19,2,22,6),'cream');p.dot(20,8,4)
    p.line([(18,11),(20,12),(22,10)],30);p.dot(19,11,30)
    for x,y in [(5,7),(8,5),(11,8),(6,11),(13,12)]:p.line([(x,y+1),(x,y),(x+2,y),(x+2,y+1)],31)
    return pixelize(p.im,(24,20))

def door():
    p=Paint((40,84));p.rect((1,1,38,83),'wood');p.rect((5,4,34,82),'wood',2)
    for box in [(8,8,30,33),(8,40,30,73)]:
        p.solid('rectangle',box,3);a,b,c,d=box;p.rect((a+2,b+2,c-2,d-2),'wood');p.line([(a+1,d-1),(c-1,d-1),(c-1,b+1)],6)
    p.line([(3,2),(36,2)],10);p.line([(3,3),(3,82)],9);p.oval((30,37,33,40),'gold');p.dot(31,37,11)
    return pixelize(p.im,(40,84))

def couch():
    p=Paint((84,44));p.rect((8,37,13,43),'wood');p.rect((69,37,74,43),'wood')
    p.oval((4,0,79,29),'couch');p.rect((6,9,77,31),'couch')
    for a,b in [(10,32),(34,55),(57,74)]:
        p.rect((a,5,b,24),'couch');p.line([(a,7),(a,23),(b,23)],7);p.line([(a+1,6),(b-1,6)],10)
    p.rect((8,25,75,37),'couch')
    for a,b in [(10,33),(35,56),(58,73)]:
        p.rect((a,16,b,27),'couch');p.line([(a,16),(b,16)],10);p.line([(a,27),(b,27)],6)
    p.oval((1,16,12,35),'couch');p.oval((73,16,82,35),'couch');p.line([(4,19),(9,19)],10);p.line([(75,19),(79,19)],10)
    p.line([(12,34),(72,34)],7)
    return pixelize(p.im,(84,44))

def main():
    # Approval sheet only. No paths in assets/ are opened for writing.
    sheet=Image.new('RGBA',(404,150),PAL[0]+(255,));d=ImageDraw.Draw(sheet)
    font=ImageFont.load_default_imagefont()
    d.text((10,7),'STEVE\'S DAY OFF / PASS 3 / CLEAN CLUSTER STUDY',fill=PAL[3],font=font)
    d.text((10,20),'DELIBERATE CLUSTERS / TOP-LEFT LIGHT / 32 COLORS',fill=PAL[6],font=font)
    floor=119;d.rectangle((0,floor,403,149),fill=PAL[1]);d.line((0,floor,403,floor),fill=PAL[31]);d.line((0,floor-2,403,floor-2),fill=PAL[31])
    items=[('DOOR',door(),11),('STAND',dog(),61),('SIT',dog(True),121),('STEVE',human(),172),('WIFE',human('wife'),210),('KID',human('kid'),247),('COUCH / STEVE',couch(),288),('LAMB',lamb(),265)]
    for label,sprite,x in items:
        if label=='LAMB': continue
        w,h=sprite.size;d.ellipse((x+2,floor-2,x+w-2,floor+2),fill=PAL[31]);sheet.alpha_composite(sprite,(x,floor-h))
        d.text((x,127),label,fill=PAL[3],font=font)
    # Seated Steve's shoes meet the same floor. Couch seat is 28px above floor.
    sheet.alpha_composite(human(seated=True),(314,floor-48))
    toy=lamb();sheet.alpha_composite(toy,(264,floor-20));d.text((260,138),'LAMB',fill=PAL[3],font=font)
    # Palette strip makes shared material constraints directly reviewable.
    for i,c in enumerate(PAL):d.rectangle((10+i*4,140,13+i*4,144),fill=c)
    # Labels also snap to the exact shared palette, eliminating font AA.
    palette=Image.new('P',(1,1));palette.putpalette([v for c in PAL for v in c]+[0]*(768-len(PAL)*3))
    sheet=sheet.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA')
    output=sheet.resize((1616,600),Image.Resampling.NEAREST);output.save(ROOT/'lineup.png')
    assert len(output.getcolors(100000))<=32
    assert set(output.getchannel('A').getdata())=={255}
    assert output.resize(sheet.size,Image.Resampling.NEAREST).resize(output.size,Image.Resampling.NEAREST).tobytes()==output.tobytes()
    print('lineup.png: 1616x600, exact 4x nearest-neighbor, <=32 colors, binary alpha; anchors verified.')

if __name__=='__main__':main()

