"""Native-resolution material painting for the double-detail texture pass.
All marks are original, deterministic, hard-edged shared-palette clusters.
"""
import random, math
from PIL import Image, ImageDraw, ImageFont
from pixelize import PAL

def detail(name,im):
    im=im.convert('RGBA'); d=ImageDraw.Draw(im); w,h=im.size
    rng=random.Random(name); original=im.copy()
    def line(pts,c,width=1): d.line(pts,fill=PAL[c]+(255,),width=width)
    def box(b,c): d.rectangle(b,fill=PAL[c]+(255,))
    def ellipse(b,c): d.ellipse(b,fill=PAL[c]+(255,))
    def poly(p,c): d.polygon(p,fill=PAL[c]+(255,))
    if name.startswith('sky_'):
        dusk=name.endswith('dusk')
        # Keep the palette: use the bluest existing slate at zenith, cream at horizon.
        for y,c in [(0,17 if not dusk else 23),(96,18 if not dusk else 27),(164,0 if not dusk else 24),(211,11 if not dusk else 10)]:
            box((0,y,w-1,h-1),c)
        for boundary,c in [(96,18 if not dusk else 27),(164,0 if not dusk else 24),(211,11 if not dusk else 10)]:
            for yy in range(boundary-6,boundary+5):
                for xx in range(w):
                    if ((xx%4)*3+(yy%4)*5)%16 < (yy-boundary+6)*16//12:
                        box((xx,yy,xx,yy),c)
        for x,y,cw,ch in [(-56,126,190,47),(168,145,170,39),(405,112,218,63),(710,142,220,48),(968,126,190,47)]:
            for off in (-w,0,w):
                X=x+off
                for dx,dy,rw,rh in [(0,23,cw,24),(18,9,65,36),(57,0,83,51),(112,16,71,33)]:
                    ellipse((X+dx,y+dy,X+dx+rw,y+dy+rh),23 if dusk else 18)
                    ellipse((X+dx+2,y+dy,X+dx+rw-7,y+dy+rh-9),27 if dusk else 0)
                    ellipse((X+dx+4,y+dy,X+dx+rw-17,y+dy+rh-19),24 if dusk else 11)
                line([(X+14,y+42),(X+53,y+42),(X+63,y+38),(X+cw-18,y+38)],9 if dusk else 0,2)
        return im
    if name.startswith('tex_') and w==64:
        kind=name[4:]; frame=3 if kind=='water1' else 0
        for i in range(42):
            x=rng.randrange(64);y=rng.randrange(64)
            for ox in (-64,0,64):
                for oy in (-64,0,64):
                    X=x+ox+frame;Y=y+oy
                    if kind=='grass':
                        line([(X-2,Y+3),(X,Y-3),(X+1,Y+2)],21)
                        line([(X+1,Y+3),(X+4,Y-1)],22)
                        line([(X-2,Y+4),(X+3,Y+4)],19)
                        if i%9==0:
                            box((X,Y-4,X+1,Y-3),11);box((X-1,Y-3,X+2,Y-2),10);box((X,Y-3,X,Y-3),32)
                    elif kind.startswith('water'):
                        line([(X-7,Y+2),(X-3,Y+2),(X,Y),(X+6,Y)],17)
                        if i%3==0:
                            line([(X-4,Y),(X-1,Y),(X+1,Y-2),(X+5,Y-2)],18)
                            line([(X,Y-2),(X+2,Y-2)],0)
                    elif kind=='snow':
                        line([(X-4,Y+1),(X,Y-1),(X+4,Y)],18)
                        line([(X-3,Y-2),(X,Y-3),(X+2,Y-3)],11)
                        if i%5==0:line([(X,Y+3),(X+2,Y+4)],17)
                    else:
                        line([(X-6,Y+2),(X-2,Y),(X+4,Y),(X+7,Y-2)],9 if kind=='sand' else 7)
                        line([(X-5,Y),(X-1,Y-2),(X+4,Y-2)],11 if kind=='sand' else 10)
                        if i%6==0:
                            ellipse((X,Y+4,X+3,Y+6),31 if kind=='sand' else 6)
                            line([(X,Y+4),(X+1,Y+4)],0 if kind=='sand' else 9)
        return im
    if name in ('tex_building','tex_rock','tex_cliff'):
        if name=='tex_building':
            for y in range(58,h,16):
                for x in range(3,w-5,19):
                    # Grain kept on siding, away from window/door.
                    if 33<x<87 and 79<y<134 or x>87 and y>131:continue
                    line([(x,y+5),(x+5,y+4),(x+12,y+5)],7)
                    line([(x+2,y+3),(x+8,y+3)],10)
                    box((x,y+1,x,y+1),3)
            for y in range(5,47,12):
                for x in range(4,w,17):line([(x,y),(x+8,y)],8)
            for x in (43,75):line([(x,94),(x+4,90)],11)
            box((98,146,105,157),7);line([(99,147),(104,147)],9)
        else:
            for i in range(115 if name=='tex_cliff' else 85):
                x=rng.randrange(3,w-7);y=rng.randrange(68 if name=='tex_cliff' else 4,h-8)
                if original.getpixel((x,y))[:3] not in (PAL[1],PAL[18],PAL[17]):continue
                line([(x,y),(x+3,y+2),(x+2,y+5),(x+6,y+7)],15)
                line([(x-1,y),(x+2,y+2)],0)
                if i%3==0:line([(x+4,y+5),(x+7,y+5)],17)
            if name=='tex_cliff':
                for x in range(5,w-3,13):line([(x,24),(x+3,26),(x+4,33)],18)
        return im
    if name.startswith('bb_'):
        if name in ('bb_tree','bb_bush','bb_palm'):
            # Leaf veins and pointed overlapping leaf clusters, clipped to foliage.
            for y in range(4,h-3,6):
                for x in range(3,w-4,7):
                    if original.getpixel((x,y))[:3] not in (PAL[19],PAL[20],PAL[21],PAL[22]):continue
                    line([(x-2,y+1),(x,y-2),(x+3,y-1)],21)
                    line([(x,y),(x+2,y+1)],19)
                    if (x+y)%3==0:line([(x-1,y-2),(x+1,y-2)],22)
            for y in range(55,h-2,7):
                for x in range(20,w-12,5):
                    if original.getpixel((x,y))[:3] in (PAL[6],PAL[9]):line([(x,y),(x+1,y+3),(x,y+5)],7)
        elif name=='bb_chest':
            for y in (27,32,37):line([(9,y),(22,y-1),(41,y),(53,y-1)],7)
            for x in (15,47):
                for y in (17,29,39):box((x,y,x+1,y+1),11)
            line([(29,24),(33,24),(33,28)],6)
        elif name=='bb_vend':
            for y in (25,43):
                for x in (15,25,35):
                    box((x,y,x+4,y+4),30 if x==25 else 21)
                    line([(x,y),(x+3,y)],11)
            line([(14,19),(18,19),(14,32)],18)
            for y in (28,36,44,52):box((47,y,49,y+2),11)
            for x in range(13,43,4):line([(x,100),(x+1,100)],3)
            line([(16,84),(44,84)],1)
        else:
            for x in (21,39):
                line([(x,70),(x,83)],31);line([(x+1,72),(x+1,79)],11)
                for y in (76,80,84):line([(x,y),(x+5,y)],18)
            for x in (7,51):
                for y in (47,51,55):line([(x,y),(x+5,y)],17)
            line([(23,39),(40,39)],11);line([(24,60),(39,60)],31)
            box((25,48,28,49),11);box((34,48,36,49),29 if name=='bb_steve' else 18)
            line([(22,12),(24,8),(29,6)],11)
            line([(40,15),(42,21),(41,25)],0)
            if name=='bb_steve':
                for x in (2,59):
                    line([(x,41),(x,52)],25);line([(x,58),(x+2,58)],10)
                    box((x,61,x+2,64),15)
        # Details cannot grow the silhouette or introduce isolated transparent marks.
        im.putalpha(original.getchannel('A'))
        return im
    if name in ('island_bg','map_island'):
        if name=='island_bg':
            horizon=detail('sky_day',Image.new('RGBA',(1024,240))).resize((1200,230),Image.Resampling.NEAREST)
            im.paste(horizon,(0,0));d=ImageDraw.Draw(im);original=im.copy()
        # Material-aware fine clusters drawn on the final native canvas.
        for i in range(17000 if name=='map_island' else 1500):
            x=rng.randrange(4,w-8);y=rng.randrange(230 if name=='island_bg' else 4,h-7)
            c=original.getpixel((x,y))[:3]
            if c==PAL[20]:
                line([(x-1,y+2),(x,y-1),(x+2,y+1)],21)
                if i%11==0:box((x,y-2,x+1,y-2),10)
            elif c==PAL[16]:
                line([(x,y),(x+4,y),(x+6,y-1)],17)
                if i%5==0:line([(x+1,y-1),(x+3,y-1)],18)
            elif c in (PAL[10],PAL[2]):
                line([(x,y),(x+4,y),(x+6,y-1)],9)
                if i%7==0:box((x,y+2,x+1,y+3),31)
            elif c==PAL[0] and name=='map_island':line([(x,y),(x+3,y-1),(x+5,y-1)],18)
            elif c==PAL[19] and name=='map_island':line([(x,y),(x+2,y-2),(x+3,y)],21)
        return im
    return im

def sheet_detail(images,path):
    im=Image.new('RGB',(1440,2300),PAL[0]);d=ImageDraw.Draw(im);font=ImageFont.load_default()
    def label(x,y,s):d.text((x,y),s,font=font,fill=PAL[3])
    def paste(name,x,y,scale=1):
        art=images[name].convert('RGBA')
        if scale!=1:art=art.resize((round(art.width*scale),round(art.height*scale)),Image.Resampling.NEAREST)
        for yy in range(y,y+art.height,8):
            for xx in range(x,x+art.width,8):d.rectangle((xx,yy,xx+7,yy+7),fill=PAL[31 if (xx//8+yy//8)%2 else 18])
        im.paste(art,(x,y),art)
    label(20,15,"STEVE'S DAY OFF / DOUBLE-DETAIL 16-BIT TEXTURES / NATIVE MATERIAL MARKS")
    for i,n in enumerate(['tex_grass','tex_sand','tex_snow','tex_desert','tex_water0','tex_water1']):
        x=20+i*230;label(x,48,n+' 64x64 / 2x2 repeat')
        for a in range(2):
            for b in range(2):paste(n,x+a*64,70+b*64)
    for i,n in enumerate(['tex_building','tex_rock','tex_cliff']):label(20+i*160,220,n);paste(n,20+i*160,242)
    for i,n in enumerate(['bb_tree','bb_palm','bb_bush','bb_chest','bb_vend','bb_steve','bb_enemy','bb_ally']):
        x=520+i%4*220;y=220+i//4*250;label(x,y,n+' '+str(images[n].size));paste(n,x,y+24)
    for i,n in enumerate(['sky_day','sky_dusk']):label(20,750+i*275,n+' 1024x240 / native size');paste(n,20,770+i*275)
    label(20,1300,'island_bg 1200x520 / native size');paste('island_bg',20,1320)
    label(20,1870,'map_island 2000x2000 / preview 20%; exported PNG is authoritative');paste('map_island',20,1890,.2)
    label(460,1910,'Shared palette unchanged. No antialiasing or semitransparency.')
    label(460,1940,'Enemy / ally identical grayscale tint masks; Steve green panel / red pack.')
    label(460,1970,'Map is generic scenery: match coast and points of interest randomize.')
    for i,c in enumerate(PAL):d.rectangle((460+i%18*24,2020+i//18*24,481+i%18*24,2041+i//18*24),fill=c)
    im.save(path)
