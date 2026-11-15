"""Original Pass 3 room paintings. Rebuild: python tools/art/rooms.py.

Static drawHouse rectangles are read, never rewritten. Coordinates stay in
buffer space until painting at 2x. Runtime objects/effects are excluded.
"""
from pathlib import Path
import re, math, hashlib
from PIL import Image, ImageDraw, ImageFont
from pixelize import PAL, surface_pixelize

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'assets'

def nearest(c):
    if isinstance(c,int): return PAL[c]
    c=c.lstrip('#'); c=c if len(c)==6 else ''.join(x*2 for x in c)
    mapped={'9ad4f5':17,'7aa0c8':17,'cfe4ec':18,'bcd4dc':18,'c8dce4':0,
            'f0e6c8':0,'f4e8a0':10,'d8cce4':28,'c8202a':30,'a01a1a':30,
            'e23b3b':30,'3a7bd5':17,'5f9f4a':21,'46c46e':21,
            'e8e8e8':0,'fff36a':10,'7d848c':1,'6c737b':16}
    if c in mapped:return PAL[mapped[c]]
    rgb=tuple(bytes.fromhex(c))
    return min(PAL,key=lambda p:sum((a-b)**2 for a,b in zip(p,rgb)))

class Room:
    def __init__(self,w=160,h=110,y0=0):
        self.im=Image.new('RGB',(w*2,h*2),PAL[4]); self.d=ImageDraw.Draw(self.im); self.y0=y0
    def box(self,x,y,w,h,c,texture=True):
        x,y,w,h=round(x*2),round((y-self.y0)*2),round(w*2),round(h*2)
        if w<=0 or h<=0:return
        col=nearest(c); self.d.rectangle((x,y,x+w-1,y+h-1),fill=col)
        if not texture or w<5 or h<5:return
        # Deliberate broken material strokes, never random single-pixel noise.
        ramps=[(3,6,7,2,9,10),(31,0,11),(15,16,17,18),(19,20,21,22),
               (23,27,28),(23,24,25,26),(30,),(4,5,1)]
        idx=PAL.index(col);ramp=next((r for r in ramps if idx in r),(idx,))
        pos=ramp.index(idx);shadow=PAL[ramp[max(0,pos-1)]];light=PAL[ramp[min(len(ramp)-1,pos+1)]]
        self.d.line((x,y,x+w-1,y),fill=light)
        self.d.line((x+w-1,y+1,x+w-1,y+h-1),fill=shadow)
        self.d.line((x,y+h-1,x+w-1,y+h-1),fill=shadow)
        if h>12 and w>8 and idx not in (17,18,28):
            step=17 if idx in (0,10,11,31) else 9
            for yy in range(y+5,y+h-2,step):
                for xx in range(x+3+(yy%3),x+w-3,23):
                    length=min(5+(xx+yy)%5,x+w-2-xx)
                    if length>0:self.d.line((xx,yy,xx+length,yy),fill=light)
    def line(self,pts,c,width=0.5):
        self.d.line([(round(x*2),round((y-self.y0)*2)) for x,y in pts],fill=nearest(c),width=max(1,round(width*2)))
    def poly(self,pts,c):self.d.polygon([(round(x*2),round((y-self.y0)*2)) for x,y in pts],fill=nearest(c))
    def wood(self,x,y,w,h,c=6):
        self.box(x,y,w,h,c)
        for yy in range(int(y+3),int(y+h-1),4):
            self.line([(x+1,yy),(x+w*.3,yy-.5),(x+w*.7,yy+.5),(x+w-2,yy)],7)
        if w>10:self.line([(x+w*.4,y+h*.4),(x+w*.55,y+h*.4-1),(x+w*.65,y+h*.4),(x+w*.5,y+h*.4+1),(x+w*.4,y+h*.4)],3)
    def frame(self,x,y,w,h):
        self.wood(x,y,w,h,3);self.box(x+1,y+1,w-2,h-2,10,False)
        self.box(x+2,y+2,w-4,h-4,17,False)
        self.poly([(x+2,y+h-2),(x+w*.45,y+h*.45),(x+w*.7,y+h*.7),(x+w-2,y+h*.4),(x+w-2,y+h-2)],21)
        self.box(x+3,y+3,2,2,11,False)
    def plant(self,x,y,s=1):
        self.box(x-2*s,y-4*s,4*s,4*s,7);self.line([(x,y-4*s),(x,y-12*s)],20,s*.5)
        for dx,dy in [(-3,-9),(1,-13),(-2,-15),(2,-7)]:
            self.poly([(x,y-6*s),(x+dx*s,y+dy*s),(x+(dx+2)*s,y+(dy-2)*s),(x+(dx+3)*s,y+dy*s)],21)
            self.line([(x+dx*s,y+dy*s),(x+(dx+2)*s,y+(dy-1)*s)],22)
    def shelf(self,x,y,w):
        self.wood(x,y,w,2,6);self.box(x+2,y+2,1,3,3);self.box(x+w-3,y+2,1,3,3)
        for i,c in enumerate([27,17,30,25,10]):
            self.box(x+2+i*2.5,y-5-(i%2),2,5+i%2,c)
    def rug(self,x,y,w,h,c=27):
        self.box(x,y,w,h,23,False);self.box(x+1,y+.5,w-2,h-1,c,False)
        for xx in range(int(x+3),int(x+w-2),4): self.line([(xx,y+1),(xx+1,y+h/2),(xx,y+h-1)],28)
    def wall(self,c,floor=1,fy=84):
        self.box(0,0,160,110,c);self.box(0,fy,160,110-fy,floor)
        self.box(0,fy-2,160,2,31)
        for yy in range(fy+8,110,9):
            self.line([(0,yy),(160,yy)],5)
            for xx in range((yy%3)*12,160,30):self.line([(xx,yy-8),(xx,yy)],5)
        self.poly([(0,0),(14,8),(14,fy),(0,fy+8)],31)
        self.line([(14,8),(14,fy)],1)
    def save(self,name):
        self.im=surface_pixelize(self.im,self.im.size);self.d=ImageDraw.Draw(self.im)
        self.im.save(OUT/(name+'.png'));return self.im

def house():
    p=Room(660,96,138)
    lines=(ROOT/'index.html').read_text(encoding='utf-8').splitlines()
    # Explicit static source selection. No JS execution, state or effect baking.
    selected=list(range(1233,1243))+[1247,1248,1249,1250,1254,1255,1256,1257,1262,1263,1264,1265,1266,1267,1268,1269,1270,1271,1273,1276,1277,1278,1281,1289,1290,1292,1295,1296,1297,1298,1299]
    # Fail visibly if game edits shift these static source lines. Never bake
    # runtime fire, smoke, car, repairbot, turret, trap or board status into art.
    assert 'R(156,HY+2,66' in lines[1254]
    assert 'R(158,HY+2,112' in lines[1276]
    env={'HY':150,'FLOOR':234,'GX':200,'ly':0,'fh':22}
    for n in selected:
        line=lines[n-1]
        # Only straight-line static calls; generated loops are painted below.
        if 'for(' in line:line=line.split('for(')[0]
        if 'if(run)' in line:line=line.split('if(run)')[0]
        for m in re.finditer(r'R\(([^;]*?)\);',line):
            args=m.group(1).split(',')
            if len(args)!=5:continue
            try:coords=[eval(a,{'__builtins__':{}},env) for a in args[:4]]
            except (NameError,SyntaxError):continue
            colors=re.findall(r"'#([0-9a-fA-F]+)'",args[4])
            if not colors:continue
            coords[0]+=200 if n>=1276 else 0
            p.box(*coords,colors[-1])
    # Readable wall finishes and trim, limited to unobstructed upper wall zones.
    for x0,x1,c in [(0,152,31),(156,222,10),(266,312,28),(316,352,10)]:
        for xx in range(x0+4,x1-2,8):
            p.line([(xx,155),(xx,159)],c)
    for xx in range(359,470,7):p.line([(xx,153),(xx,233)],16)
    # Garage corrugation must sit behind its fixtures: restore static fixtures.
    for n in [1281,1289,1290]:
        line=lines[n-1].split('if(run)')[0]
        for m in re.finditer(r'R\(([^;]*?)\);',line):
            args=m.group(1).split(',')
            try:a=[eval(v,{'__builtins__':{}},env) for v in args[:4]]
            except (NameError,SyntaxError):continue
            colors=re.findall(r"'#([0-9a-f]+)'",args[-1]);a[0]+=200
            if colors:p.box(*a,colors[-1])
    # Lower bathroom tile field.
    for xx in range(226,262,6):
        for yy in range(190,213,6):p.box(xx,yy,5.5,5.5,18 if (xx+yy)%12 else 0)
    # Static fireplace grille and cold logs; live flames are left to the game.
    for xx in range(89,113,6):p.box(xx,215,1,16,4,False)
    p.wood(92,226,18,3,3);p.wood(94,224,6,2,5)
    # TV footprints and Xbox exactly match drawHouse, screens fully dark.
    p.box(80,184,42,26,4);p.box(82,186,38,22,15,False);p.box(99,210,4,2,4,False)
    p.box(320,168,24,15,4);p.box(321,169,22,13,15,False)
    p.box(326,185,12,4,4);p.box(327,186,4,1,16,False)
    # Bunk bedding seams, pillows, rail, and ladder within original footprints.
    for yy in [194,212]:
        p.line([(320,yy+1),(341,yy+1)],18 if yy==212 else 26)
        p.box(320,yy,5,2,11)
    p.line([(339,198),(339,232)],6);p.line([(342,198),(342,232)],3)
    for yy in range(200,233,5):p.line([(339,yy),(342,yy)],7)
    # Original still-life dressing in negative space.
    p.frame(18,168,12,15);p.frame(112,163,14,13)
    p.shelf(76,164,27);p.plant(145,205,.8)
    p.line([(122,209),(125,211),(125,213)],4)
    p.line([(338,189),(340,191),(340,193)],4)
    p.shelf(192,166,9);p.plant(198,207,.55)
    p.box(160,186,40,15,31)
    for xx in range(160,200,5):p.line([(xx,186),(xx,201)],0)
    for yy in [191,196,201]:p.line([(160,yy),(200,yy)],0)
    p.box(160,202,9,11,18);p.box(161,203,7,2,11)
    p.line([(166,202),(166,198),(169,198),(169,200)],18,1)
    p.box(193,203,4,10,6);p.line([(194,203),(192,198)],3);p.line([(196,203),(197,197)],3)
    p.box(243,198,10,2,6);p.box(245,200,6,9,25)
    p.line([(246,202),(250,202)],26)
    p.frame(297,170,9,12);p.shelf(270,193,22)
    p.rug(274,230,26,3,27)
    p.frame(347,169,4,10)
    p.shelf(442,184,23)
    # Tool board, hand tools, cable loop, vise: fixed workshop fixtures.
    p.box(441,192,24,11,6)
    for xx in range(443,464,3):
        for yy in [194,198,201]:p.box(xx,yy,.5,.5,3,False)
    for xx in [444,449,454,459]:
        p.line([(xx,194),(xx,200)],18,1);p.line([(xx-1,194),(xx+1,194)],18)
    p.line([(435,183),(438,187),(438,199),(434,202),(431,198),(431,188),(435,183)],4,1)
    p.box(441,211,4,3,18);p.box(442,208,2,3,16)
    # Lift has no car/platform motion baked in: empty stationary posts and base.
    for xx in [380,432]:
        p.box(xx,180,3,54,30);p.box(xx,181,1,51,25,False)
        p.box(xx-1,232,5,2,4)
    p.box(382,228,52,2,16)
    # Lot fence, trees and parked inventory. No arriving car, gate or visitors.
    for xx in range(520,660,10):p.line([(xx,204),(xx,232)],18)
    for xx in range(520,660,5):p.line([(xx,205),(min(xx+20,660),231)],18)
    p.box(487,212,2,22,18);p.box(487,212,10,1,18)
    for yy in range(214,232,4):p.line([(489,yy),(496,yy+3)],18)
    p.wood(496,138,4,22,3)
    p.plant(483,232,.75)
    for xx in range(474,660,9):p.line([(xx,233),(xx+2,231)],21)
    for i,(xx,col) in enumerate([(526,0),(552,16),(578,29),(604,4),(630,30)]):
        p.box(xx,222,22,9,col);p.box(xx+4,217,12,5,col)
        p.box(xx+6,218,8,3,15,False)
        p.box(xx+2,230,4,3,4);p.box(xx+15,230,4,3,4)
        p.line([(xx+4,225),(xx+19,225)],31)
        if i%2==0:p.box(xx+8,213,6,3,10)
        else:p.box(xx+3,214,15,4,col)
    p.box(504,220,16,10,30);p.box(507,215,10,5,30);p.box(512,212,5,3,8)
    return p.save('house_bg')

def cctv(kind):
    p=Room()
    if kind=='yard':
        p.box(0,0,160,70,17);p.box(0,70,160,40,21)
        for x,y,w in [(8,10,28),(65,18,23),(120,9,30)]:
            p.box(x,y,w,5,0);p.box(x+5,y-3,w-10,4,11)
        p.box(0,30,24,40,1)
        for yy in range(32,70,5):p.line([(0,yy),(24,yy)],16)
        p.box(4,38,14,12,15);p.box(5,39,12,1,18)
        p.box(70,44,3,30,18);p.box(128,44,3,30,18);p.box(70,44,60,2,18)
        for xx in range(70,130,6):
            p.line([(xx,46),(min(xx+24,130),70)],18)
            p.line([(xx,70),(min(xx+24,130),46)],18)
        for yy in range(75,110,7):
            for xx in range(3+(yy%4),160,12):p.line([(xx,yy),(xx+2,yy-2),(xx+3,yy)],20)
        p.plant(34,80,1.5)
        p.box(3,86,34,16,1);p.line([(5,90),(31,90)],31)
    elif kind=='stove':
        p.wall(10,6,70)
        p.box(18,10,124,44,0)
        for xx in range(18,142,10):p.line([(xx,10),(xx,54)],31)
        for yy in range(10,55,8):p.line([(18,yy),(142,yy)],31)
        p.box(30,62,100,10,4);p.box(40,58,20,4,16);p.box(100,58,20,4,16)
        for xx in [40,100]:
            for dx in [2,7,12]:p.line([(xx+dx,59),(xx+dx+2,61)],18)
        # Pot/steam omitted: these belong to the animated stove state.
        for xx in [20,64,108]:
            p.wood(xx,76,36,32,6);p.box(xx+4,80,28,23,7);p.box(xx+23,83,5,1,10)
        p.shelf(17,17,26);p.shelf(116,17,28)
        p.box(9,54,12,8,6);p.line([(11,54),(9,39)],3,1);p.line([(16,54),(19,40)],18,1)
        p.plant(146,63,.9)
    elif kind=='door':
        p.wall(0,1,80);p.wood(18,18,54,66,3);p.wood(20,20,50,64,6);p.wood(24,24,42,58,7)
        for yy,hh in [(27,21),(56,21)]:
            p.wood(28,yy,34,hh,6);p.line([(30,yy+2),(60,yy+2)],9)
        p.box(60,52,4,4,10);p.frame(94,23,24,24);p.shelf(89,62,42)
        p.plant(142,83,1.6);p.rug(27,88,57,13,20)
        p.wood(89,76,40,4);p.box(92,80,3,20,3);p.box(122,80,3,20,3)
        for xx in [92,103,114]:p.box(xx,70,8,6,31)
    elif kind=='couch':
        p.wall(0,1,86);p.frame(27,16,27,20);p.shelf(65,20,26)
        p.box(100,20,56,36,4);p.box(102,22,52,32,15,False)
        p.line([(127,56),(127,63),(142,63),(142,65)],4,1)
        p.wood(98,65,60,21,3);p.box(117,68,26,15,4);p.wood(121,78,18,3,5)
        for xx in [119,124,129,134,139]:p.line([(xx,69),(xx,81)],16)
        p.box(10,60,80,28,2);p.box(6,48,14,40,7);p.box(78,63,14,25,7)
        for xx in [22,48]:
            p.box(xx,59,25,6,9);p.line([(xx,67),(xx,84)],7)
            p.line([(xx+2,69),(xx+19,69)],10)
        p.box(11,88,5,5,3);p.box(82,88,5,5,3)
        p.rug(30,98,91,10,27);p.wood(55,91,58,4,6)
        p.box(59,95,3,12,3);p.box(106,95,3,12,3);p.box(72,86,8,5,11)
        p.plant(94,65,.9)
    elif kind=='bath':
        p.wall(18,17,80)
        for xx in range(16,160,10):
            for yy in range(0,80,10):p.box(xx+1,yy+1,8,8,0 if (xx+yy)%20 else 18)
        p.wood(54,14,52,76,6);p.wood(58,18,44,68,7);p.box(94,50,4,4,10)
        p.box(62,22,36,12,11);p.line([(67,27),(92,27)],5);p.line([(73,30),(86,30)],5)
        p.box(119,47,30,29,0);p.box(119,45,30,5,11)
        p.box(122,15,24,24,31);p.box(124,17,20,20,17)
        p.line([(130,45),(130,39),(136,39),(136,42)],18,1)
        p.box(24,60,14,18,11);p.box(20,76,23,9,0);p.box(25,85,13,10,0)
        p.rug(59,96,44,9,17);p.box(113,59,3,14,25)
    elif kind=='kid':
        p.wall(10,2,86)
        p.box(10,50,60,14,17);p.box(10,30,60,6,30);p.box(10,26,4,40,3);p.box(66,26,4,40,3)
        p.box(15,29,14,3,11);p.box(15,49,14,4,11)
        for yy in [33,54]:p.line([(31,yy),(64,yy)],18)
        p.line([(56,36),(56,85)],6,1.5);p.line([(63,36),(63,85)],3,1.5)
        for yy in range(39,85,7):p.line([(56,yy),(63,yy)],7,1)
        # Added wall TV/Xbox on right, leaving the character's center clear.
        p.box(116,13,40,28,4);p.box(118,15,36,24,15,False)
        p.wood(116,47,40,3);p.box(125,43,21,4,4);p.box(127,44,5,1,16)
        p.line([(145,47),(149,51),(149,59)],4)
        p.shelf(80,17,25);p.frame(80,26,19,14)
        p.rug(79,94,57,12,20);p.box(30,88,10,10,21);p.box(46,90,8,8,25)
        for xx in [32,36]:p.box(xx,87,2,1,22)
    elif kind=='wife':
        p.wall(10,31,84);p.box(14,10,38,45,6)
        for xx in range(17,51,4):
            for yy in range(13,55,4):p.box(xx,yy,.5,.5,3,False)
        p.frame(24,17,18,16);p.shelf(98,24,48)
        p.box(96,64,50,6,7);p.wood(96,65,50,5,6)
        p.box(100,70,4,30,3);p.box(138,70,4,30,3)
        p.box(100,54,10,10,25);p.box(116,56,14,8,17);p.box(134,52,8,12,10)
        for xx in [102,106]:p.line([(xx,55),(xx,62)],26)
        p.box(115,58,16,3,18);p.box(114,61,20,2,0)
        p.line([(132,61),(128,52),(131,47)],4)
        p.wood(19,61,29,30,6);p.box(21,64,25,8,7);p.box(21,75,25,13,7)
        p.box(30,67,6,1,10);p.plant(24,61,.8)
        p.rug(55,96,75,10,27);p.shelf(57,25,30)
        p.box(64,38,17,16,0);p.line([(66,43),(78,43)],25);p.line([(66,47),(76,47)],17)
    return p.save('cctv_'+kind)

from room_detail import install
install(Room, nearest)

def main():
    images={'house_bg':house()}
    for kind in ['yard','stove','door','couch','bath','kid','wife']:images['cctv_'+kind]=cctv(kind)
    sheet=Image.new('RGB',(1360,1040),PAL[0]);d=ImageDraw.Draw(sheet)
    d.text((20,12),'ORIGINAL 16-BIT INTERIORS / layered materials, warm light and fixed gameplay geometry',fill=PAL[3])
    d.text((20,37),'house_bg / global buffer x 0..660, y 138..234 / garage GX=200',fill=PAL[3])
    sheet.paste(images['house_bg'],(20,58))
    for i,(name,im) in enumerate(list(images.items())[1:]):
        x=20+(i%4)*335;y=280+(i//4)*350
        d.text((x,y),name+' / 320 x 220',fill=PAL[3]);sheet.paste(im,(x,y+22))
    d.text((20,996),'Original Pillow cluster painting / shared 48-color palette / opaque backgrounds / no baked CCTV overlays',fill=PAL[3])
    sheet.save(ROOT/'tools/art/sheet_rooms.png')
    for name,im in images.items():
        expected=(1320,192) if name=='house_bg' else (320,220)
        assert im.size==expected,(name,im.size)
        assert set(im.getdata())<=set(PAL),name
        print(name,im.size,'palette / dimensions / opacity OK')
    for name,box in [('house_bg',(164,96,240,140)),('house_bg',(642,62,686,88)),('cctv_couch',(204,44,308,108)),('cctv_kid',(236,30,308,78))]:
        assert set(images[name].crop(box).getdata())=={PAL[15]},(name,'screen not dark')
    print('Four dark TV screen regions verified.')

if __name__=='__main__':main()

