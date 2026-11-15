"""Original native-pixel interior painting, in fixed rooms.py coordinate space.
No sampled game art, blur, antialiasing or stochastic texture. 48 shared colours.
"""
import math
from PIL import Image, ImageDraw
from pixelize import PAL, BAYER


def install(Room, nearest):
    old_box, old_save = Room.box, Room.save

    def box(self,x,y,w,h,c,texture=True):
        # Ground-contact shadows are painted before the corresponding object.
        footprints = {(10,60,80,28),(6,48,14,40),(98,65,60,21),
                      (55,91,58,4),(89,76,40,4),(119,47,30,29),
                      (19,61,29,30),(96,64,50,6),(24,212,36,14),
                      (70,212,62,22),(160,218,40,16),(270,218,34,10)}
        if texture and (x,y,w,h) in footprints:
            ground=min(y+h,234 if self.y0 else 108)
            self.poly([(x,ground-1),(x+w,ground-1),(x+w+4,ground+2),(x+2,ground+3)],41)
        old_box(self,x,y,w,h,c,False)
        if not texture or w<2 or h<2:return
        X,Y,W,H=round(x*2),round((y-self.y0)*2),round(w*2),round(h*2)
        col=nearest(c); idx=PAL.index(col)
        ramps=[(41,3,6,42,7,43,2,9,10),(36,37,38,39,0,11),
               (15,16,17,18,45,11),(19,20,46,21,22),
               (23,27,28,26),(23,24,25,26),(41,47,30,34,9),
               (4,36,1,18,0)]
        ramp=next((r for r in ramps if idx in r),(idx,));n=ramp.index(idx)
        shade=PAL[ramp[max(0,n-1)]]; deep=PAL[ramp[max(0,n-2)]]
        light=PAL[ramp[min(len(ramp)-1,n+1)]]
        d=self.d
        # Hand-defined bevel bands: upper-left light, bottom and right occlusion.
        d.line((X,Y,X+W-1,Y),fill=light)
        d.line((X,Y,X,Y+H-1),fill=light)
        if W>5 and H>5:
            d.rectangle((X+W-3,Y+2,X+W-1,Y+H-1),fill=shade)
            d.rectangle((X+2,Y+H-3,X+W-1,Y+H-1),fill=deep)
            # Intentional material clusters. Wood has long broken contour grain.
            if idx in (3,6,7,2,9,42,43):
                for yy in range(Y+4,Y+H-3,6):
                    for xx in range(X+3+(yy//6%3)*7,X+W-4,27):
                        end=min(X+W-4,xx+17)
                        d.line([(xx,yy),(min(xx+4,end),yy-1),(end,yy)],fill=shade)
                        if end-xx>8:d.line((xx+2,yy+1,end-3,yy+1),fill=light)
            elif idx in (2,25,27,28):
                for yy in range(Y+3,Y+H-3,4):
                    for xx in range(X+3+(yy%3),X+W-3,6):
                        d.line((xx,yy,xx+1,yy),fill=light)
        # House rooms: floor is inserted before all fixtures, without moving walls.
        if self.y0==138 and h==82 and w>=30:
            floor(self,x,218,w,234-218,'tile' if x==226 else 'stone' if x==358 else 'wood')
            if x!=358:wallpaper(self,x,y,w,64,idx)
            trim(self,x,y,w,218)
        if self.y0==138 and x==470 and w==200 and h==102:
            # Exterior distance layers stop above the parked-car footprint.
            landscape(self,472,185,188,20)
            for cx,cy,cw in [(476,163,27),(524,174,36),(606,166,31)]:
                self.poly([(cx,cy+3),(cx+3,cy+1),(cx+8,cy+1),(cx+11,cy-2),(cx+18,cy-2),(cx+21,cy+1),(cx+cw,cy+1),(cx+cw,cy+4),(cx,cy+4)],18)
                self.line([(cx+6,cy+1),(cx+15,cy+1)],0)
    Room.box=box

    def wallpaper(p,x,y,w,h,c):
        # Small stripes and paired floral diamonds, kept to the wall plane.
        for xx in range(int(x+3),int(x+w-2),6):
            p.line([(xx,y+3),(xx,y+h-1)],39 if c in (0,10,31) else 27 if c==28 else 18,.5)
            for yy in range(int(y+9),int(y+h-3),13):
                ink=38 if c in (0,10,31) else 23 if c==28 else 16
                p.line([(xx+2,yy-1),(xx+3,yy-2),(xx+4,yy-1),(xx+3,yy+1),(xx+2,yy-1)],ink)
    def trim(p,x,y,w,fy):
        p.box(x,y,w,3,36,False);p.box(x,y+3,w,1,38,False)
        p.box(x,y+4,w,.5,11,False)
        p.box(x,fy-4,w,1,36,False);p.box(x,fy-3,w,2,38,False)
        p.box(x,fy-1,w,.5,11,False)
        p.box(x,fy,w,2,41,False)
        p.box(x,y+5,1,fy-y-5,37,False)
        p.box(x+w-2,y+5,2,fy-y-5,37,False)
    def floor(p,x,y,w,h,kind='wood'):
        p.box(x,y,w,h,37 if kind=='wood' else 16,False)
        # Increasing row heights and diverging seams create a shallow floor plane.
        yy=y; row=0
        while yy<y+h:
            rh=min(3+row*1.5,y+h-yy)
            if rh<=0:break
            step=18+row*5
            for i,xx in enumerate(range(int(x-30+(row%2)*12),int(x+w),int(step))):
                a=max(x,xx); b=min(x+w,xx+step-.5)
                if b<=a:continue
                col=([6,42,7,43][(i+row)%4] if kind=='wood' else [17,18,45,1][(i+row)%4])
                p.box(a,yy,b-a,rh-.5,col,False)
                p.line([(a,yy),(b,yy)],9 if kind=='wood' else 0)
                if kind=='wood' and b-a>6:
                    p.line([(a+2,yy+1),(a+5,yy+.5),(b-2,yy+1)],6)
                    if rh>4:p.line([(a+3,yy+3),(b-3,yy+3)],43)
            yy+=rh;row+=1
        p.box(x,y,w,1,36,False)
    def wall(self,c,floor_col=1,fy=84):
        self.box(0,0,160,fy,c,False)
        wallpaper(self,14,0,146,fy-3,c)
        floor(self,0,fy,160,110-fy,'tile' if c==18 else 'wood')
        trim(self,0,0,160,fy)
        self.poly([(0,0),(14,8),(14,fy),(0,fy+8)],37)
        for yy in range(10,fy-4,11):self.line([(1,yy),(12,yy+4)],38)
        self.line([(14,8),(14,fy)],36)
        self.line([(13,9),(13,fy)],39)
    Room.wall=wall

    def wood(self,x,y,w,h,c=6):
        self.box(x,y,w,h,c)
        # Sparse oval knots and split highlights, all within the same footprint.
        if w>12 and h>8:
            kx=x+w*.36;ky=y+h*.58
            self.line([(kx-2,ky),(kx,ky-1),(kx+3,ky),(kx,ky+1),(kx-2,ky)],3)
            self.line([(kx-1,ky+2),(kx+4,ky+2)],43)
    Room.wood=wood
    def rug(self,x,y,w,h,c=27):
        self.box(x,y,w,h,41,False)
        self.box(x+.5,y+.5,w-1,h-1,10,False)
        self.box(x+1.5,y+1,w-3,h-2,c,False)
        self.box(x+3,y+2,w-6,h-4,23 if c==27 else 19,False)
        for xx in range(int(x+5),int(x+w-4),7):
            self.line([(xx,y+h/2),(xx+2,y+2),(xx+4,y+h/2),(xx+2,y+h-2),(xx,y+h/2)],28 if c==27 else 22)
        for xx in range(int(x+1),int(x+w),3):
            self.line([(xx,y),(xx,y+.5)],11)
            self.line([(xx,y+h-1),(xx,y+h-.5)],38)
    Room.rug=rug
    def shelf(self,x,y,w):
        self.box(x+.5,y+2,w,2,36,False);self.wood(x,y,w,2,6)
        self.box(x+2,y+2,1,3,3);self.box(x+w-3,y+2,1,3,3)
        xx=x+2; i=0
        while xx<x+w-3:
            ww=[1.5,2,1,2.5][i%4]; hh=[6,8,5,7,6][i%5]
            cc=[30,17,20,27,7,25,31][i%7]
            self.box(xx,y-hh,ww,hh,cc)
            self.line([(xx+.5,y-hh+1),(xx+ww-.5,y-hh+1)],10)
            self.line([(xx+.5,y-2),(xx+ww-.5,y-2)],38)
            xx+=ww+.5;i+=1
    Room.shelf=shelf

    def shaft(p,pts):
        mask=Image.new('1',p.im.size);md=ImageDraw.Draw(mask)
        md.polygon([(round(x*2),round((y-p.y0)*2)) for x,y in pts],fill=1)
        pix=p.im.load();mp=mask.load();bounds=mask.getbbox()
        if not bounds:return
        for yy in range(bounds[1],bounds[3]):
            for xx in range(bounds[0],bounds[2]):
                if mp[xx,yy] and BAYER[yy%4][xx%4]<12:
                    old=pix[xx,yy]
                    light={PAL[6]:PAL[7],PAL[42]:PAL[43],PAL[7]:PAL[2],PAL[43]:PAL[9],PAL[37]:PAL[38],PAL[17]:PAL[18],PAL[18]:PAL[45]}
                    pix[xx,yy]=light.get(old,old)
    def glow(p,x,y,r):
        # Three hard elliptical dither bands; never soft alpha or blur.
        for radius,color,phase in [(r,39,4),(r*.7,40,3),(r*.4,10,2)]:
            for yy in range(round((y-radius*.7-p.y0)*2),round((y+radius*.7-p.y0)*2)):
                for xx in range(round((x-radius)*2),round((x+radius)*2)):
                    if 0<=xx<p.im.width and 0<=yy<p.im.height and ((xx/2-x)/radius)**2+((yy/2+p.y0-y)/(radius*.7))**2<1 and BAYER[yy%4][xx%4]<16//phase:
                        p.im.putpixel((xx,yy),PAL[color])
    def lamp(p,x,y,s=1):
        glow(p,x,y-6*s,12*s)
        p.box(x-.5*s,y-9*s,1*s,9*s,3)
        p.box(x-3*s,y-1*s,6*s,1*s,6)
        p.poly([(x-3*s,y-14*s),(x+3*s,y-14*s),(x+5*s,y-8*s),(x-5*s,y-8*s)],10)
        p.line([(x-3*s,y-14*s),(x+3*s,y-14*s)],11)
        p.line([(x-4*s,y-8*s),(x+4*s,y-8*s)],7)
    def clock(p,x,y,s=1):
        p.d.ellipse((round((x-5*s)*2),round((y-5*s-p.y0)*2),round((x+5*s)*2),round((y+5*s-p.y0)*2)),fill=PAL[3])
        p.d.ellipse((round((x-4*s)*2),round((y-4*s-p.y0)*2),round((x+4*s)*2),round((y+4*s-p.y0)*2)),fill=PAL[10])
        p.line([(x,y-3*s),(x,y),(x+2*s,y+1*s)],3)
        for dx,dy in [(0,-3),(3,0),(0,3),(-3,0)]:p.box(x+dx*s,y+dy*s,.5,.5,3,False)
    def window(p,x,y,w,h):
        p.wood(x,y,w,h,3);p.box(x+1,y+1,w-2,h-2,17,False)
        p.poly([(x+1,y+h-1),(x+w*.4,y+h*.55),(x+w*.65,y+h*.7),(x+w-1,y+h*.4),(x+w-1,y+h-1)],46)
        p.box(x+2,y+2,w-4,2,18,False)
        p.box(x+w/2-1,y+1,1.5,h-1,0)
        p.box(x+1,y+h*.5,w-2,1,0)
        p.wood(x-1,y+h,w+2,2,39)
        # Pleated side curtains remain within the original window rectangle.
        for dx in [0,1.5,w-3,w-1.5]:p.box(x+dx,y,1.5,h*.75,39 if dx%3 else 0)
    def basket(p,x,y,w=12,h=10):
        p.box(x,y,w,h,6);p.box(x+1,y+1,w-2,h-2,38)
        for yy in range(int(y+2),int(y+h-1),2):p.line([(x+1,yy),(x+w-2,yy)],7)
        for xx in range(int(x+2),int(x+w-1),3):p.line([(xx,y+1),(xx,y+h-2)],10)
        p.poly([(x+1,y),(x+2,y-3),(x+5,y-2),(x+7,y-4),(x+w-2,y),(x+1,y)],28)
    def cushion(p,x,y,w,h):
        p.poly([(x+1,y),(x+w-2,y),(x+w,y+2),(x+w,y+h-2),(x+w-2,y+h),(x+1,y+h),(x,y+h-2),(x,y+2)],6)
        p.poly([(x+1,y+2),(x+2,y+1),(x+w-3,y+1),(x+w-1,y+3),(x+w-1,y+h-2),(x+2,y+h-1),(x+1,y+h-3)],2)
        p.line([(x+2,y+1),(x+w-3,y+1),(x+w-2,y+2)],10)
        p.line([(x+1,y+h-2),(x+w-2,y+h-2)],6)
        p.line([(x+1,y+1),(x+2,y+3)],9)
        for yy in range(int(y+4),int(y+h-3),3):
            for xx in range(int(x+3+(yy%2)),int(x+w-3),5):p.line([(xx,yy),(xx+.5,yy)],43)
        if w>10:
            p.line([(x+w/2-1,y+h/2-1),(x+w/2,y+h/2),(x+w/2+1,y+h/2-1)],7)
            p.box(x+w/2,y+h/2,1,.5,10,False)
    def landscape(p,x,y,w,h):
        # Distant original garden silhouettes, painted behind fences/inventory.
        p.poly([(x,y+h),(x,y+h*.6),(x+w*.18,y+h*.3),(x+w*.35,y+h*.55),(x+w*.57,y+h*.18),(x+w*.8,y+h*.5),(x+w,y+h*.35),(x+w,y+h)],46)
        for xx in range(int(x+4),int(x+w),13):
            yy=y+h*.5+((xx//13)%3)*2
            p.poly([(xx-5,yy+8),(xx-4,yy+1),(xx,yy-5),(xx+5,yy),(xx+7,yy+8)],20)
            p.poly([(xx-4,yy+1),(xx,yy-5),(xx+3,yy),(xx+1,yy+4)],21)
            p.line([(xx-2,yy),(xx,yy-2),(xx+2,yy)],22)
    def pool(p,x,y,w,h):
        mask=Image.new('1',p.im.size)
        ImageDraw.Draw(mask).ellipse((round((x-w)*2),round((y-h-p.y0)*2),round((x+w)*2),round((y+h-p.y0)*2)),fill=1)
        mp=mask.load();pix=p.im.load();bounds=mask.getbbox()
        if not bounds:return
        light={PAL[6]:PAL[7],PAL[42]:PAL[43],PAL[7]:PAL[2],PAL[43]:PAL[9],PAL[37]:PAL[38],PAL[17]:PAL[18],PAL[18]:PAL[45]}
        for yy in range(bounds[1],bounds[3]):
            for xx in range(bounds[0],bounds[2]):
                if mp[xx,yy] and BAYER[yy%4][xx%4]<10:pix[xx,yy]=light.get(pix[xx,yy],pix[xx,yy])
    def details(p,name):
        if name=='house_bg':
            # Exact existing window bounds, screens and furniture stay untouched.
            window(p,40,162,26,20);window(p,164,164,24,18);window(p,278,172,16,12)
            shaft(p,[(40,219),(65,219),(79,233),(52,233)])
            shaft(p,[(164,219),(178,219),(189,233),(172,233)])
            # Existing couch cushion and furniture faces, bounded by source rectangles.
            cushion(p,30,213,12,12);cushion(p,43,214,12,11)
            p.line([(23,205),(28,205),(28,222)],10)
            clock(p,132,171,1)
            p.shelf(5,185,29);p.shelf(5,175,27)
            lamp(p,140,205,.65)
            pool(p,140,231,10,3)
            # Pan rail and jars, outside the stove's runtime bounding region.
            p.line([(191,175),(201,175)],3)
            for xx in [192,198]:
                p.line([(xx,175),(xx,179)],18)
                p.box(xx-1,179,3,4,16);p.line([(xx,180),(xx+1,180)],18)
            for xx,cc in [(161,25),(166,21),(171,10)]:
                p.box(xx,209,3,5,cc);p.box(xx,208,3,1,3)
            p.box(195,220,3,10,0);p.line([(196,221),(196,229)],25)
            # Mirror and miniature bathroom bottles in fixed vanity area.
            p.wood(236,176,14,16,31);p.box(237,177,12,14,17)
            p.line([(238,186),(246,178)],45);p.line([(242,189),(248,183)],18)
            for xx,cc in [(245,25),(249,21)]:p.box(xx,215,2,3,cc);p.box(xx+.5,214,1,1,11)
            basket(p,293,222,7,8)
            lamp(p,307,206,.36)
            pool(p,307,230,4,2)
            p.line([(281,219),(300,219)],28)
            for xx in range(282,301,4):p.line([(xx,220),(xx+1,226)],27)
            # Kid poster inside existing wall decoration footprint.
            p.box(347,169,4,10,17);p.poly([(347,177),(349,171),(351,177)],10)
            # Garage dressing sits outside x380..435 lift rectangle.
            for yy in [223,227,231]:
                p.box(459,yy,7,3,4);p.line([(460,yy),(465,yy)],16)
                p.line([(461,yy+1),(464,yy+1)],36)
            p.poly([(442,231),(446,229),(451,230),(453,233),(441,233)],36)
            p.line([(447,232),(450,231)],16)
            # Fixed mailbox and flowers occupy yard, never the lot car region.
            p.wood(477,218,1,14,6);p.box(474,214,7,5,17)
            p.box(475,214,5,1,18);p.box(480,212,1,4,30)
            for xx in [473,481,484,501]:
                p.line([(xx,233),(xx,228)],20)
                p.box(xx-1,227,3,2,25);p.box(xx,227,1,1,10)
            return
        kind=name[5:]
        if kind=='yard':
            landscape(p,25,47,135,23)
            # Restore the fixed fence over the garden, retaining exact post positions.
            p.box(70,44,3,30,18);p.box(128,44,3,30,18);p.box(70,44,60,2,18)
            for xx in range(70,130,6):
                p.line([(xx,46),(min(xx+24,130),70)],18)
                p.line([(xx,70),(min(xx+24,130),46)],18)
            # Lawn clumps with foreground depth and flower beds along the siding.
            for yy in range(73,110,5):
                for xx in range((yy%3)*5,160,13):
                    p.line([(xx,yy+2),(xx+1,yy-1),(xx+2,yy+1),(xx+4,yy-2)],20)
                    p.line([(xx+2,yy),(xx+3,yy-1)],22)
            for xx in [5,11,17,23,29,38,45,52]:
                p.line([(xx,77),(xx,72)],46)
                p.box(xx-1,70,3,2,25 if xx%2 else 10)
                p.box(xx,70,1,1,11)
            p.wood(47,66,2,15,6);p.box(43,59,12,7,17)
            p.box(44,59,9,1,18);p.box(54,56,1,7,30)
            p.line([(44,63),(49,63)],3)
            return
        if kind=='couch':
            # Seam shading uses the exact original couch envelope.
            for xx in [21,47,73]:cushion(p,xx,61,16 if xx==73 else 24,25)
            p.line([(8,50),(17,50),(17,85)],10)
            cushion(p,24,62,14,12);cushion(p,60,62,14,11)
            clock(p,83,41,1)
            window(p,16,3,40,10)
            shaft(p,[(16,90),(42,90),(62,108),(33,108)])
            lamp(p,96,58,.65)
            pool(p,94,94,16,4)
            # Shelf recesses filled with varied spines, no furniture footprint change.
            p.shelf(101,83,14);p.shelf(145,83,11)
            p.line([(98,86),(156,86)],41)
        elif kind=='door':
            # Deep jamb is fully contained in its existing 18..72 doorway bounds.
            p.box(18,18,3,66,41);p.box(21,20,1,62,10)
            p.box(20,82,50,2,41);p.line([(21,83),(68,83)],9)
            clock(p,139,24,1.2)
            window(p,16,2,42,11)
            shaft(p,[(16,84),(35,84),(54,109),(31,109)])
            lamp(p,123,75,.8)
            pool(p,128,102,18,5)
            basket(p,145,92,12,14)
        elif kind=='stove':
            # Stovetop (30..130,58..72) and central pot/effect area stay clear.
            p.line([(18,37),(39,37)],3)
            for xx in [22,31]:
                p.line([(xx,37),(xx,41)],18)
                p.d.ellipse((int((xx-3)*2),84,int((xx+3)*2),98),fill=PAL[16])
                p.line([(xx-2,43),(xx+1,43)],18)
            for xx,cc in [(119,25),(126,20),(133,10)]:
                p.box(xx,49,5,9,cc);p.box(xx,48,5,2,3)
                p.box(xx+1,52,3,3,0)
            p.box(92,81,8,20,0);p.line([(94,83),(94,99)],30)
            p.line([(98,83),(98,99)],25)
            for xx in [24,68,112]:
                p.box(xx,80,28,1,10);p.box(xx,102,28,1,3)
            p.box(15,5,130,3,36,False)
            # Warm under-shelf light with ceramic highlights on side backsplash.
            p.box(19,19,23,1,10,False);p.box(117,19,25,1,10,False)
            for yy in range(21,35):
                for xx in range(19,40):
                    if (xx+yy)%4==0:p.box(xx,yy,.5,.5,40,False)
        elif kind=='bath':
            # Ceramic diagonal glints and inset mirror, all within existing fixtures.
            p.box(122,15,24,24,36);p.box(124,17,20,20,17)
            p.poly([(125,31),(138,18),(142,18),(125,35)],45)
            p.line([(130,35),(142,23)],18)
            p.box(54,14,3,76,41);p.line([(57,18),(57,88)],10)
            p.box(59,36,41,1,6);p.box(59,82,41,1,3)
            for xx,cc in [(120,25),(126,21),(140,17)]:
                p.box(xx,41,4,5,cc);p.box(xx+1,39,2,2,0)
            p.box(114,61,2,11,28);p.line([(114,69),(115,69)],26)
            p.d.ellipse((44,154,80,168),fill=PAL[18])
            p.d.ellipse((48,156,76,163),fill=PAL[15])
            p.line([(121,73),(146,73)],18)
            pool(p,134,88,15,5)
        elif kind=='kid':
            window(p,18,4,43,16)
            shaft(p,[(15,87),(41,87),(63,109),(31,109)])
            for yy in [31,51]:
                p.box(30,yy,24,3,30 if yy==31 else 17)
                for xx in range(32,54,7):p.box(xx,yy+1,2,1,10)
            # Original moon/rocket poster inside the previous framed picture.
            p.box(81,27,17,12,15);p.poly([(86,37),(90,29),(93,37)],10)
            p.box(89,31,2,2,17);p.box(94,29,1,1,11)
            # Gaming chair behind the runtime kid, clear of the TV and toys.
            p.box(140,65,13,19,15);p.box(143,66,7,16,27)
            p.line([(141,66),(141,80)],18)
            p.box(138,83,17,4,16);p.box(145,87,2,9,4)
            p.line([(139,97),(152,97)],4,1);p.box(138,97,3,2,4);p.box(151,97,3,2,4)
            for xx,cc in [(31,21),(47,25)]:
                p.box(xx+1,91,5,4,cc);p.box(xx+2,92,1,1,11)
            p.box(19,87,7,4,30);p.box(20,91,2,2,4);p.box(24,91,2,2,4)
        elif kind=='wife':
            window(p,58,2,31,15)
            shaft(p,[(42,86),(68,86),(92,109),(61,109)])
            basket(p,149,91,10,16)
            lamp(p,138,52,.85)
            pool(p,137,94,17,5)
            p.line([(17,13),(48,13)],10)
            for xx in [18,45]:
                p.line([(xx,25),(xx,44)],16)
                p.line([(xx-2,29),(xx+2,29)],18)
            for xx,cc in [(101,25),(107,17),(119,21),(132,10)]:
                p.box(xx,58,2,6,cc);p.line([(xx+1,58),(xx+1,62)],11)
            p.line([(22,72),(45,72)],3)
            p.line([(22,87),(45,87)],3)

    def save(self,name):
        # Decorative lighting cannot touch runtime screens or working zones.
        zones={'house_bg':[(82,186,120,208),(321,169,343,182),
                           (176,198,194,214),(383,180,432,228),
                           (520,204,660,234)],
               'cctv_couch':[(102,22,154,54)],
               'cctv_kid':[(118,15,154,39)],
               'cctv_stove':[(30,22,130,72)]}.get(name,[])
        zones=[tuple(round(v*2) if i%2==0 else round((v-self.y0)*2) for i,v in enumerate(b)) for b in zones]
        original=[self.im.crop(b) for b in zones]
        details(self,name)
        for b,im in zip(zones,original):self.im.paste(im,b[:2])
        assert all(self.im.crop(b).tobytes()==im.tobytes() for b,im in zip(zones,original)),name
        return old_save(self,name)
    Room.save=save
