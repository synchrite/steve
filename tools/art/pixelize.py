"""Pass 3 approval lineup. Original pixel painting; no individual exports.

Run: python tools/art/pixelize.py (Pillow required).
All shapes are painted at native sprite resolution. Shared finalizer resizes,
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
    p=Paint((52,48) if sitting else (54,46))
    if sitting:
        p.poly([(5,38),(1,32),(2,27),(5,33),(12,36),(18,39),(17,43),(8,42)],'fur')
        p.oval((11,24,32,43),'fur');p.oval((12,32,25,44),'fur')
        p.poly([(25,19),(33,20),(34,39),(38,43),(31,44),(28,37),(27,29)],'cream')
        p.poly([(23,22),(28,24),(27,39),(30,43),(24,44),(22,36)],'fur')
        hx,hy=26,10
    else:
        p.poly([(12,23),(5,21),(2,14),(3,9),(5,13),(6,18),(15,19)],'fur')
        p.poly([(17,28),(21,29),(19,37),(15,42),(10,42),(15,36)],'fur',3)
        p.poly([(36,27),(39,25),(40,38),(45,41),(39,42),(36,35)],'fur',3)
        p.oval((9,13,39,31),'fur');p.poly([(18,28),(30,25),(39,22),(36,30),(23,33)],'cream')
        p.poly([(13,26),(19,28),(16,37),(17,41),(13,43),(9,42),(12,37)],'fur')
        p.poly([(30,25),(36,23),(36,39),(40,41),(39,43),(33,43),(32,35)],'fur')
        hx,hy=34,6
    p.poly([(hx-8,hy+16),(hx-5,hy+6),(hx+4,hy+5),(hx+8,hy+17),(hx+2,hy+22)],'fur')
    p.poly([(hx-5,hy+5),(hx-7,hy-6),(hx-3,hy-4),(hx+1,hy+5)],'fur')
    p.poly([(hx+3,hy+4),(hx+7,hy-5),(hx+9,hy-4),(hx+7,hy+8)],'fur')
    p.line([(hx-5,hy-3),(hx-3,hy+3)],6);p.line([(hx+7,hy-2),(hx+5,hy+4)],6)
    p.oval((hx-5,hy+3,hx+8,hy+15),'fur')
    p.poly([(hx+3,hy+10),(hx+10,hy+11),(hx+12,hy+14),(hx+9,hy+17),(hx+2,hy+16),(hx,hy+13)],'dark')
    p.line([(hx+10,hy+12),(hx+12,hy+12)],4,2);p.dot(hx+5,hy+8,5);p.dot(hx+6,hy+8,10)
    p.line([(hx-6,hy+18),(hx+1,hy+21),(hx+7,hy+18)],27,3)
    p.line([(hx-5,hy+17),(hx+2,hy+20),(hx+6,hy+18)],28)
    for x,y in [(hx-4,hy+18),(hx,hy+20),(hx+4,hy+19)]:p.dot(x,y,23)
    p.solid('rectangle',(hx+4,hy+18,hx+6,hy+20),29)
    for x,y in [(15,22),(19,23),(24,19),(28,24)] if not sitting else [(15,31),(18,34),(23,28)]:
        p.line([(x,y),(x+2,y+1)],9);p.dot(x+1,y+2,7)
    return pixelize(p.im,(40,48) if sitting else (52,44))

def human(role='steve',seated=False):
    size=(32,48) if seated else ((14,36) if role=='kid' else (20,44))
    p=Paint(size);kid=role=='kid';wife=role=='wife';ox=0
    # Native heights: kid 32px, adults fill their table limits.
    top=4 if kid else 1;cx=8 if not seated else 11
    if kid:cx=6
    heady=top+4; torsoy=top+13; bottom=size[1]-2
    if seated:
        p.poly([(6,27),(21,27),(25,31),(24,40),(29,44),(28,46),(21,45),(19,34),(7,34)],'denim')
        p.poly([(10,31),(20,32),(19,41),(23,45),(18,46),(14,42),(13,36),(7,35)],'denim',2)
    else:
        p.poly([(cx-4,torsoy+10),(cx+1,torsoy+11),(cx, bottom-5),(cx-3,bottom-1),(cx-6,bottom-1),(cx-4,bottom-7)],'denim')
        p.poly([(cx+1,torsoy+10),(cx+5,torsoy+10),(cx+5,bottom-3),(cx+8,bottom-1),(cx+7,bottom),(cx+2,bottom),(cx,bottom-9)],'denim',2)
    shirt='dark' if wife else ('gold' if kid else 'olive')
    p.poly([(cx-4,torsoy-2),(cx+3,torsoy-3),(cx+6,torsoy+2),(cx+5,torsoy+12),(cx-4,torsoy+12),(cx-6,torsoy+5)],shirt)
    if not kid and not wife:
        p.poly([(cx-4,torsoy-3),(cx+1,torsoy-4),(cx+4,torsoy),(cx,torsoy+2),(cx-4,torsoy)],'olive')
        p.line([(cx,torsoy),(cx+1,torsoy+7)],19);p.dot(cx+2,torsoy+3,10)
        p.line([(cx-3,torsoy+9),(cx+2,torsoy+9)],19)
    if wife:
        p.line([(cx-3,torsoy-2),(cx-2,torsoy+5)],17,2);p.line([(cx+3,torsoy-2),(cx+3,torsoy+5)],17,2)
        p.rect((cx-3,torsoy+4,cx+4,torsoy+12),'denim');p.dot(cx-2,torsoy+4,10);p.dot(cx+3,torsoy+4,10)
        p.line([(cx-1,torsoy+7),(cx+2,torsoy+7),(cx+2,torsoy+9),(cx,torsoy+10)],18)
    if seated:
        p.poly([(cx+2,torsoy+1),(cx+5,torsoy+2),(cx+6,torsoy+9),(cx+12,torsoy+9),(cx+13,torsoy+12),(cx+4,torsoy+12),(cx+1,torsoy+7)],shirt)
        p.rect((cx+11,torsoy+9,cx+15,torsoy+12),'skin');p.oval((cx+13,torsoy+7,cx+19,torsoy+11),'dark');p.dot(cx+15,torsoy+8,18);p.dot(cx+18,torsoy+9,30)
    else:
        p.poly([(cx+3,torsoy),(cx+6,torsoy+3),(cx+5,torsoy+10),(cx+2,torsoy+9)],shirt)
        p.oval((cx+2,torsoy+9,cx+5,torsoy+13),'skin')
    p.rect((cx,heady+7,cx+3,heady+11),'skin')
    p.poly([(cx-3,heady),(cx+3,heady-1),(cx+5,heady+2),(cx+5,heady+4),(cx+7,heady+5),(cx+6,heady+6),(cx+4,heady+6),(cx+4,heady+9),(cx,heady+10),(cx-3,heady+6)],'skin')
    hair='pink' if wife else ('gold' if kid else 'hair')
    p.poly([(cx-4,heady+3),(cx-4,heady),(cx-2,heady-3),(cx+3,heady-3),(cx+5,heady),(cx+4,heady+1),(cx,heady),(cx-1,heady+4),(cx-2,heady+6)],hair)
    if wife:
        p.oval((cx-5,top-1,cx+1,top+4),'pink');p.line([(cx-4,heady+3),(cx+6,heady+3),(cx+6,heady+6),(cx+2,heady+6),(cx+1,heady+3)],23)
        p.dot(cx+2,heady+3,26);p.dot(cx+5,heady+5,10)
    elif not kid:
        p.line([(cx-1,heady+7),(cx+1,heady+9),(cx+4,heady+8)],6);p.dot(cx+3,heady+7,5)
    p.dot(cx+4,heady+3,4)
    if not seated:
        p.line([(cx-6,bottom),(cx-2,bottom),(cx-1,bottom-1)],4);p.line([(cx+2,bottom),(cx+7,bottom)],4)
        p.dot(cx+3,bottom-2,18)
    return pixelize(p.im,size)

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
    d.text((10,7),'STEVE\'S DAY OFF / PASS 3 / MATERIAL & SCALE STUDY',fill=PAL[3],font=font)
    d.text((10,20),'ORIGINAL PIXEL PAINTING / TOP-LEFT LIGHT / 32 COLORS',fill=PAL[6],font=font)
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
