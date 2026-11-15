"""Original clean-cluster raycaster art. Run from any directory; Pillow only.

Shared palette/finalizers: pixelize.py. Floors are painted on a torus, skies
wrap in X. Map follows genMap's formula with fixed representative positions;
it is scenery, never a replacement for randomized collision/POI coordinates.
"""
from pathlib import Path
import math
import random
import json
from PIL import Image, ImageDraw, ImageFont
from pixelize import PAL, pixelize, surface_pixelize

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'assets/tex'
ART=ROOT/'tools/art'
IMAGES={}

class ScaledDraw:
    """Rasterize the composition at twice the coordinate density."""
    def __init__(self,im): self.d=ImageDraw.Draw(im)
    def shape(self,kind,xy,**kw):
        if isinstance(xy[0],(tuple,list)): xy=[(round(x*2),round(y*2)) for x,y in xy]
        else: xy=tuple(round(v*2) for v in xy)
        if 'width' in kw: kw['width']*=2
        getattr(self.d,kind)(xy,**kw)
    def rectangle(self,xy,**kw): self.shape('rectangle',xy,**kw)
    def polygon(self,xy,**kw): self.shape('polygon',xy,**kw)
    def ellipse(self,xy,**kw): self.shape('ellipse',xy,**kw)
    def line(self,xy,**kw): self.shape('line',xy,**kw)


def canvas(size, color=None):
    im=Image.new('RGBA',(size[0]*2,size[1]*2), PAL[color]+(255,) if color is not None else (0,0,0,0))
    return im, ScaledDraw(im)

def rect(d,box,c): d.rectangle(box,fill=PAL[c])
def poly(d,pts,c): d.polygon(pts,fill=PAL[c])
def line(d,pts,c,w=1): d.line(pts,fill=PAL[c],width=w)
def oval(d,box,c): d.ellipse(box,fill=PAL[c])

def save(name,im,sprite=False,neutral=False):
    from texture_detail import detail
    im=detail(name,im)
    if sprite:
        im=pixelize(im,im.size)
        # Owner requests full canvases, including naturally narrow objects.
        body=im.crop(im.getbbox())
        out=Image.new('RGBA',im.size)
        out.paste(body.resize((im.width-2,im.height),Image.Resampling.NEAREST),(1,0))
        im=out
    else: im=surface_pixelize(im,im.size)
    if name.startswith('tex_') and im.size==(64,64):
        for y in range(im.height): im.putpixel((im.width-1,y),im.getpixel((0,y)))
        for x in range(im.width): im.putpixel((x,im.height-1),im.getpixel((x,0)))
    if name.startswith('sky_'):
        for y in range(im.height): im.putpixel((im.width-1,y),im.getpixel((0,y)))
    if neutral:
        # Tint masks require R=G=B. Four luminance bands, same geometry/alpha.
        alpha=im.getchannel('A')
        levels=(48,104,172,228)
        gray=im.convert('L').point(lambda v:min(levels,key=lambda n:abs(n-v)))
        im=Image.merge('RGBA',(gray,gray,gray,alpha))
    im.save(OUT/(name+'.png'))
    IMAGES[name]=im

def tile(kind,frame=0):
    ramps={'grass':(20,19,21,22),'sand':(10,2,9,11),'snow':(0,18,31,11),
           'desert':(2,7,9,10),'water':(16,15,17,18)}
    base,shade,light,glint=ramps[kind]
    im,d=canvas((32,32),base)
    # Each deliberate cluster is stamped on a torus, including across edges.
    for x,y,k in [(0,3,0),(11,0,1),(23,7,2),(6,15,3),(19,23,4),(30,29,5)]:
        for dx in (-32,0,32):
            for dy in (-32,0,32):
                X=x+dx;Y=y+dy
                if kind=='grass':
                    poly(d,[(X-3,Y+2),(X-1,Y),(X+3,Y),(X+5,Y+2),(X+2,Y+4),(X-2,Y+4)],shade)
                    line(d,[(X-2,Y+1),(X,Y-2),(X+1,Y+1),(X+3,Y-1)],light)
                    line(d,[(X+1,Y+4),(X+2,Y+2),(X+4,Y+3)],light)
                elif kind=='water':
                    X+=frame*3
                    line(d,[(X-5,Y+2),(X-2,Y+2),(X,Y),(X+6,Y)],shade,2)
                    line(d,[(X-3,Y-1),(X+2,Y-1),(X+4,Y-3),(X+8,Y-3)],light)
                    if k%2==0:line(d,[(X,Y-2),(X+3,Y-2)],glint)
                else:
                    poly(d,[(X-4,Y),(X-1,Y-2),(X+3,Y-2),(X+6,Y),(X+3,Y+2),(X-2,Y+2)],shade)
                    line(d,[(X-3,Y-1),(X,Y-3),(X+4,Y-3)],light)
                    if kind=='snow':line(d,[(X-2,Y-4),(X+1,Y-4)],glint)
                    elif kind=='desert':line(d,[(X-6,Y+5),(X+2,Y+5),(X+5,Y+3)],light)
    # Duplicate boundary samples guarantee exact opposing-edge equality.
    for y in range(64):im.putpixel((63,y),im.getpixel((0,y)))
    for x in range(64):im.putpixel((x,63),im.getpixel((x,0)))
    return im

def walls():
    im,d=canvas((64,96),2)
    for y in range(25,96,8):
        rect(d,(0,y,63,y+1),6);line(d,[(0,y+2),(63,y+2)],10)
        for x in (5,29,53):line(d,[(x,y+4),(x+6,y+4)],9)
    rect(d,(0,0,63,23),30)
    for y in range(0,24,6):
        line(d,[(0,y+5),(63,y+5)],3)
        for x in range(-8,70,16):line(d,[(x+(y//6%2)*8,y),(x+(y//6%2)*8,y+4)],7)
        line(d,[(0,y),(63,y)],8)
    rect(d,(0,24,63,27),3);line(d,[(0,24),(63,24)],10)
    rect(d,(18,42,41,64),6);rect(d,(20,44,39,60),15);rect(d,(21,45,37,58),17)
    poly(d,[(21,45),(31,45),(21,55)],18);line(d,[(29,44),(29,60)],0,2)
    line(d,[(20,52),(39,52)],0);rect(d,(17,62,42,65),10)
    rect(d,(45,67,57,95),3);rect(d,(47,69,55,94),6)
    rect(d,(48,72,53,82),7);line(d,[(48,87),(53,87),(53,93)],3);rect(d,(53,84,54,85),10)
    save('tex_building',im)
    im,d=canvas((64,64),1)
    for row,y in enumerate(range(-4,64,16)):
        for x in range(-32,64,32):
            x+=16*(row%2)
            poly(d,[(x+1,y+2),(x+27,y),(x+31,y+4),(x+29,y+14),(x+3,y+15)],18)
            poly(d,[(x+4,y+11),(x+23,y+10),(x+29,y+4),(x+29,y+14),(x+3,y+15)],1)
            line(d,[(x+3,y+3),(x+24,y+2)],0)
            line(d,[(x+17,y+4),(x+14,y+7),(x+16,y+9)],17)
    save('tex_rock',im)
    im,d=canvas((64,128),1)
    for x in range(-8,64,16):
        poly(d,[(x,19),(x+11,13),(x+16,42),(x+10,75),(x+17,106),(x+13,127),(x,127),(x+4,78)],18)
        poly(d,[(x+10,34),(x+16,43),(x+10,76),(x+17,106),(x+13,127),(x+7,127),(x+9,105),(x+4,77)],17)
        line(d,[(x+1,48),(x+6,54),(x+3,67)],0)
        line(d,[(x+4,93),(x+10,97),(x+7,109)],15)
    for y in (45,81,114):line(d,[(0,y),(18,y-4),(35,y+3),(51,y-2),(63,y)],1,2)
    poly(d,[(0,0),(63,0),(63,22),(55,19),(51,29),(45,25),(41,33),(35,21),(28,24),(23,32),(16,23),(10,29),(6,20),(0,23)],0)
    poly(d,[(0,0),(63,0),(63,13),(54,10),(46,18),(35,12),(26,18),(17,12),(7,18),(0,14)],11)
    line(d,[(0,24),(6,22),(10,31),(16,25),(23,34),(28,26)],17)
    save('tex_cliff',im)

def sky(dusk=False):
    im,d=canvas((512,120),23 if dusk else 16)
    bands=[(0,29,23),(30,55,27),(56,80,24),(81,100,9),(101,119,10)] if dusk else [(0,34,16),(35,70,17),(71,100,18),(101,119,0)]
    for a,b,c in bands:rect(d,(0,a,511,b),c)
    # Sparse ordered transition steps, all hard pixels.
    for a,b,c in bands[1:]:
        for x in range(0,512,4):rect(d,(x,a-2,x+1,a-1),c)
    for x,y,w in [(-20,87,68),(80,96,74),(207,83,87),(350,97,94),(470,87,68)]:
        for off in (-512,0,512):
            X=x+off
            pts=[(X,y+10),(X+7,y+10),(X+7,y+4),(X+18,y+4),(X+18,y),(X+35,y),(X+35,y+3),(X+w-14,y+3),(X+w-14,y+8),(X+w,y+8),(X+w,y+16),(X,y+16)]
            poly(d,pts,23 if dusk else 18)
            poly(d,[(X+3,y+8),(X+12,y+8),(X+12,y+2),(X+30,y+2),(X+30,y+5),(X+w-17,y+5),(X+w-17,y+10),(X+w-3,y+10),(X+w-3,y+12),(X+3,y+12)],27 if dusk else 11)

    return im

def foliage(kind):
    size=(48,32) if kind=='bush' else (48,96)
    im,d=canvas(size)
    if kind=='palm':
        poly(d,[(19,95),(21,69),(25,42),(24,25),(29,24),(31,44),(27,71),(28,95)],6)
        line(d,[(23,91),(24,67),(28,44),(27,28)],9,2)
        for y in range(42,94,8):line(d,[(23,y),(27,y+2)],3)
        for pts in [[(26,27),(11,17),(1,22),(8,10),(20,11),(27,22)],[(26,26),(11,28),(1,43),(4,29),(15,21)],[(26,26),(28,8),(38,1),(33,15)],[(27,25),(40,12),(47,18),(38,18)],[(27,25),(43,27),(47,43),(39,33)],[(27,26),(27,38),(18,50),(21,35)]]:
            poly(d,pts,20);line(d,[pts[0],pts[1],pts[2]],21)
        oval(d,(22,25,27,31),3);oval(d,(28,26,32,32),7)
    else:
        if kind=='tree':
            poly(d,[(17,95),(21,70),(19,43),(29,43),(28,72),(33,95)],6)
            line(d,[(22,90),(24,67),(23,45)],9,2)
            line(d,[(25,73),(33,61),(36,48)],3,3)
            lobes=[(3,19,30,49),(13,3,37,34),(23,20,45,53),(7,35,35,62)]
        else:lobes=[(2,11,24,30),(10,1,32,24),(25,9,45,30)]
        for x0,y0,x1,y1 in lobes:
            oval(d,(x0,y0,x1,y1),19);oval(d,(x0+1,y0+1,x1-3,y1-5),20)
            poly(d,[(x0+3,y0+8),(x0+6,y0+4),(x0+14,y0+3),(x0+16,y0+8),(x0+11,y0+9),(x0+9,y0+13),(x0+3,y0+12)],21)
            line(d,[(x0+6,y0+5),(x0+11,y0+4)],22)
            line(d,[(x1-9,y1-6),(x1-5,y1-8),(x1-4,y1-12)],19)
    return im

def props():
    im,d=canvas((32,24))
    poly(d,[(2,22),(2,7),(6,2),(25,2),(29,7),(29,22)],6)
    rect(d,(3,9,28,21),8);rect(d,(3,8,28,11),10)
    poly(d,[(3,7),(7,3),(24,3),(27,7)],9);line(d,[(6,4),(23,4)],11)
    for x in (7,23):rect(d,(x,5,x+2,21),10);line(d,[(x+2,12),(x+2,20)],7)
    rect(d,(14,10,18,15),7);rect(d,(14,10,17,13),11);rect(d,(16,12,16,14),3)
    line(d,[(4,20),(27,20)],6);save('bb_chest',im,True)
    im,d=canvas((32,56));rect(d,(3,1,28,54),30);rect(d,(4,2,26,6),0)
    rect(d,(5,8,21,33),15);rect(d,(6,9,20,30),16)
    for y in (11,20):
        for x in (7,12,17):rect(d,(x,y,x+2,y+6),18);rect(d,(x,y,x+2,y+1),11)
        line(d,[(6,y+8),(20,y+8)],17)
    rect(d,(23,12,25,16),10);rect(d,(23,20,25,22),3)
    rect(d,(7,39,24,47),3);rect(d,(8,40,23,42),4);line(d,[(7,48),(24,48)],8)
    line(d,[(4,8),(4,52)],25);rect(d,(25,34,28,53),23)
    rect(d,(4,53,8,55),4);rect(d,(23,53,27,55),4);save('bb_vend',im,True)

def person(steve=False):
    im,d=canvas((32,48))
    # Original rounded astronaut proportions, symmetric front-facing stance.
    if steve:
        rect(d,(3,18,7,34),30);rect(d,(24,18,28,34),30)
        line(d,[(4,19),(4,30)],25);rect(d,(3,32,7,36),17);rect(d,(24,32,28,36),17)
    rect(d,(9,31,14,45),18);rect(d,(18,31,23,45),1)
    rect(d,(9,32,12,43),0);rect(d,(18,32,21,43),0)
    rect(d,(7,44,14,47),16);rect(d,(18,44,25,47),16)
    line(d,[(8,44),(13,44)],0);line(d,[(19,44),(24,44)],0)
    poly(d,[(8,17),(23,17),(26,23),(24,33),(8,33),(6,23)],18)
    rect(d,(9,18,22,31),0);line(d,[(10,18),(20,18)],11)
    poly(d,[(5,19),(8,20),(8,31),(6,35),(2,34),(2,28)],0)
    poly(d,[(24,20),(27,19),(30,28),(30,34),(26,35),(24,31)],18)
    line(d,[(3,27),(7,28)],17);line(d,[(25,28),(29,27)],17)
    rect(d,(2,33,6,36),16);rect(d,(26,33,30,36),16)
    rect(d,(9,31,23,33),17);rect(d,(14,31,18,33),0)
    oval(d,(7,0,24,19),18);oval(d,(8,1,23,17),0)
    oval(d,(9,2,22,15),16);oval(d,(10,3,21,14),17)
    # Clear bubble: visible face, cool glass edge and hard white reflections.
    if steve:
        oval(d,(12,6,20,14),13);rect(d,(12,6,20,8),6)
        rect(d,(13,10,13,11),3);rect(d,(18,10,18,11),3);line(d,[(15,13),(17,13)],12)
    else:rect(d,(11,7,20,12),18);rect(d,(12,8,19,10),1)
    line(d,[(10,7),(10,5),(12,3),(16,3)],11);line(d,[(21,9),(21,12)],18)
    rect(d,(11,21,20,28),20 if steve else 16)
    rect(d,(12,22,18,25),21 if steve else 17)
    line(d,[(12,22),(17,22)],22 if steve else 18)
    rect(d,(12,27,13,27),11);rect(d,(17,27,18,27),11)
    if steve:
        # Pack pods project beyond the arms, so the red remains readable front-on.
        rect(d,(0,19,2,29),30);rect(d,(29,19,31,29),30)
        line(d,[(0,20),(0,27)],25);rect(d,(0,30,2,33),17);rect(d,(29,30,31,33),17)
    return im

def backdrop():
    im=sky().resize((1200,520),Image.Resampling.NEAREST).convert('RGBA');d=ScaledDraw(im)
    for x,y in [(35,76),(245,60),(470,83)]:
        rect(d,(x,y+5,x+63,y+11),18);rect(d,(x+11,y,x+44,y+8),0)
        line(d,[(x+14,y),(x+39,y)],11,2)
    rect(d,(0,115,599,259),16)
    for y in range(124,260,11):
        for x in range((y*3)%43-35,600,67):line(d,[(x,y),(x+26,y)],17)
    oval(d,(83,161,524,242),18);oval(d,(91,155,515,233),10)
    poly(d,[(100,204),(137,173),(220,159),(352,159),(444,176),(505,206),(449,220),(202,222)],2)
    poly(d,[(145,191),(194,171),(340,168),(424,184),(443,200),(346,208),(205,205)],10)
    line(d,[(114,209),(159,218),(249,223),(393,221),(469,209)],11,2)
    for x,y in [(182,104),(365,113),(423,128)]:
        palm=foliage('palm');im.alpha_composite(palm,(x*2,y*2))
    return im

def matchmap():
    # Native painting at half resolution, exact 2x clusters in exported map.
    im,d=canvas((500,500),16);rng=random.Random(314)
    coast=[440+math.sin(a*.7)*18+math.sin(a*1.9)*10+rng.uniform(-6,6) for a in range(64)]
    def shore(scale):return [(round((500+math.cos(a/64*math.tau)*r*scale)/2),round((500+math.sin(a/64*math.tau)*r*scale)/2)) for a,r in enumerate(coast)]
    poly(d,shore(1.04),17);poly(d,shore(1),10);poly(d,shore(.96),20)
    mask=Image.new('1',im.size);ScaledDraw(mask).polygon(shore(.96),fill=1)
    land,ld=canvas((500,500),20)
    rect(ld,(0,0,499,124),0)
    poly(ld,[(310,500),(310,330),(500,280),(500,500)],2)
    oval(ld,(45,310,195,420),19)
    # Small ordered material clusters, no random single-pixel noise.
    for y in range(14,488,13):
        for x in range(10+(y//13%2)*7,490,19):
            if y<122:c=18
            elif x>310 and y>330-(x-310)*.263:c=9
            elif ((x-120)/75)**2+((y-365)/55)**2<1:c=20
            else:c=21
            line(ld,[(x,y+1),(x+2,y),(x+5,y)],c)
    for i in range(24):
        x=rng.randrange(65,177);y=rng.randrange(330,400);oval(ld,(x,y,x+8,y+4),16)
    im.paste(land,(0,0),mask);d=ScaledDraw(im)
    # Mountain at (500,380), within actual +/-60 X variation.
    for r,c in [(45,21),(34,1),(24,18),(15,0),(7,11)]:
        oval(d,(250-r*1.3,190-r,250+r*1.3,190+r),c)
    poly(d,[(228,188),(245,152),(256,151),(270,181),(257,175),(251,181),(245,170),(237,190)],0)
    # Cubic river follows the generation code's control points.
    pts=[]
    for k in range(101):
        t=k/100;s=1-t
        x=s**3*250+3*s*s*t*190+3*s*t*t*290+t**3*270
        y=s**3*210+3*s*s*t*250+3*s*t*t*280+t**3*490
        pts.append((round(x),round(y)))
    line(d,pts,10,7);line(d,pts,17,4)
    oval(d,(226,240,274,274),10);oval(d,(229,243,271,271),17)
    line(d,[(235,249),(243,247),(253,247)],18)
    towns=[(110,190,'suburb'),(175,305,'farm'),(310,245,'warehouse'),(350,360,'resort'),(365,150,'suburb'),(200,105,'warehouse')]
    road=[(x,y+12) for x,y,k in towns]
    road.sort(key=lambda p:math.atan2(p[1]-250,p[0]-250));road.append(road[0])
    line(d,road,4,5);line(d,road,1,3)
    line(d,[(110,202),(250,282),(350,372)],4,5);line(d,[(110,202),(250,282),(350,372)],1,3)
    for x,y,k in towns:
        rect(d,(x-23,y-15,x+23,y+15),21 if k=='suburb' else 2)
        if k=='suburb':
            for a in range(4):
                for b in range(2):
                    X=x-20+a*11;Y=y-13+b*15
                    rect(d,(X,Y,X+7,Y+6),0);rect(d,(X,Y,X+7,Y+2),30);rect(d,(X+3,Y+4,X+4,Y+6),6)
            line(d,[(x-22,y),(x+22,y)],1,2)
        elif k=='warehouse':
            for a in range(3):
                X=x-20+a*14;rect(d,(X,y-12,X+11,y+3),18);rect(d,(X,y-12,X+11,y-10),17);rect(d,(X+3,y-1,X+8,y+3),4)
                rect(d,(X,y+7,X+7,y+10),30 if a%2 else 16)
        elif k=='farm':
            for a in range(6):rect(d,(x-22,y-14+a*5,x+7,y-11+a*5),7 if a%2 else 9)
            rect(d,(x+10,y-12,x+22,y-2),30);rect(d,(x+10,y-12,x+22,y-10),3)
        else:
            rect(d,(x-10,y-5,x+10,y+7),17)
            rect(d,(x-18,y-12,x-3,y-7),11);rect(d,(x+4,y-12,x+19,y-7),11)
            for a in range(4):rect(d,(x-17+a*10,y+10,x-15+a*10,y+12),25 if a%2 else 10)
    for i in range(320):
        x=rng.randrange(48,452);y=rng.randrange(48,452)
        if not mask.getpixel((x*2,y*2)) or y<130 or x>310 and y>300:continue
        if any(abs(x-X)<30 and abs(y-Y)<24 for X,Y,k in towns):continue
        if math.hypot(x-250,y-190)<62 or math.hypot(x-250,y-257)<34:continue
        if any(math.hypot(x-X,y-Y)<7 for X,Y in pts):continue
        oval(d,(x-3,y-2,x+4,y+4),19);oval(d,(x-3,y-4,x+3,y+2),20);line(d,[(x-2,y-3),(x,y-4),(x+1,y-3)],21)
    return im.resize((2000,2000),Image.Resampling.NEAREST)

def sheet():
    from texture_detail import sheet_detail
    sheet_detail(IMAGES,ART/'sheet3.png')


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for kind in ('grass','sand','snow','desert'):save('tex_'+kind,tile(kind))
    for frame in (0,1):save('tex_water'+str(frame),tile('water',frame))
    walls()
    for dusk in (False,True):save('sky_dusk' if dusk else 'sky_day',sky(dusk))
    for kind in ('tree','palm','bush'):save('bb_'+kind,foliage(kind),True)
    props();save('bb_steve',person(True),True)
    for kind in ('enemy','ally'):save('bb_'+kind,person(),True,True)
    save('island_bg',backdrop());save('map_island',matchmap());sheet()
    print(json.dumps({n:list(im.size) for n,im in IMAGES.items()},indent=2))

if __name__=='__main__':main()
