"""Fit built-in image generations to static game geometry; never redraw the art.

Rebuild: python tools/art/generated_rooms.py. Raw PNGs are in rooms_src/.
BOX resampling integrates source pixel areas, then the shared finalizer snaps
to the 64-color palette without dithering. No game code is executed or edited.
"""
from pathlib import Path
import json, hashlib
from PIL import Image, ImageDraw, ImageOps
from pixelize import PAL, surface_pixelize

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'tools/art/rooms_src'
OUT=ROOT/'assets'
REGIONS=json.loads((SRC/'regions.json').read_text())
LAYOUT=json.loads((ROOT/'tools/art/house_layout.json').read_text())

def fit(name,size):
    im=Image.open(SRC/(name+'.png')).convert('RGB')
    # Explicit center crop to exact target aspect, followed by area downsampling.
    ratio=size[0]/size[1]
    if im.width/im.height>ratio:
        w=round(im.height*ratio);left=(im.width-w)//2
        box=(left,0,left+w,im.height)
    else:
        h=round(im.width/ratio);top=(im.height-h)//2
        box=(0,top,im.width,top+h)
    crops[name]={'source':im.size,'crop':box,'output':size}
    im=im.crop(box)
    # Registration landmarks measured on the raw generations: piecewise area
    # resampling puts the major furniture at the existing game footprints.
    grids={
        'living':([0,.574,.859,1],[0,80/152,122/152,1],
                  [0,.384,.699,.91,1],[0,46/96,72/96,92/96,1]),
        'kitchen':([0,1],[0,1],[0,.4,.65,.90,1],[0,.42,.73,.98,1]),
        'master':([0,1],[0,1],[0,.54,.93,1],[0,72/96,.99,1]),
        'kid':([0,.13,.82,1],[0,4/36,28/36,1],
               [0,.26,.49,.57,1],[0,30/96,45/96,56/96,1]),
        'cctv_couch':([0,.711,.973,1],[0,204/320,308/320,1],
                      [0,.123,.357,1],[0,44/220,108/220,1]),
        'cctv_kid':([0,.78,.98,1],[0,236/320,308/320,1],
                    [0,.13,.35,1],[0,30/220,78/220,1])}
    if name in grids:
        sx,dx,sy,dy=grids[name];registered=Image.new('RGB',size)
        for j in range(len(sy)-1):
            for i in range(len(sx)-1):
                sb=(round(sx[i]*im.width),round(sy[j]*im.height),
                    round(sx[i+1]*im.width),round(sy[j+1]*im.height))
                db=(round(dx[i]*size[0]),round(dy[j]*size[1]),
                    round(dx[i+1]*size[0]),round(dy[j+1]*size[1]))
                registered.paste(im.crop(sb).resize((db[2]-db[0],db[3]-db[1]),Image.Resampling.BOX),db[:2])
        im=registered
        crops[name]['registration_grid']={'source_x':sx,'target_x':dx,'source_y':sy,'target_y':dy}
    return surface_pixelize(im.resize(size,Image.Resampling.BOX),size)

def worldbox(box):
    x,y,r,b=box
    return (x*2,(y-138)*2,r*2,(b-138)*2)

def fill(im,box,color):
    x,y,r,b=box
    ImageDraw.Draw(im).rectangle((x,y,r-1,b-1),fill=color)

crops={}
old=Image.open(SRC/'house_before.png').convert('RGB')
house=old.copy()
for name,(left,right) in REGIONS.items():
    # Assert each interior wall field exists in the authoritative capture.
    if name in ('living','kitchen','bathroom','master','kid','garage'):
        assert any(r[:4]==[left,152,right-left,82] for r in LAYOUT['rects']),name
    house.paste(fit(name,((right-left)*2,192)),(left*2,0))

# Preserve exact structural beams/doorway strips from the captured geometry.
for box in [(152,150,156,234),(222,150,226,234),(262,150,266,234),
            (312,150,316,234),(352,150,358,234),(468,142,472,234),
            (0,138,468,152)]:
    b=worldbox(box);house.paste(old.crop(b),b[:2])

# Runtime footprints are authoritative, not approximate generated objects.
# TV screen and frame footprints are unchanged; nearby generated dressing stays.
for box in [(80,184,122,212),(320,168,344,183),(326,185,338,189)]:
    b=worldbox(box);house.paste(old.crop(b),b[:2])
# Empty, plain working surfaces, matching drawHouse() and prior protected zones.
plain=[((176,198,194,208),PAL[39]),((383,180,432,228),PAL[36]),
       ((520,204,660,234),PAL[37]),((398,156,438,180),PAL[11])]
for box,color in plain:fill(house,worldbox(box),color)
# Restore fixed stove, lift posts/resting platform and exact door silhouette.
for box in [(176,208,194,214),(380,180,383,234),(432,180,435,234),
            (382,228,434,230),(2,192,14,234)]:
    b=worldbox(box);house.paste(old.crop(b),b[:2])

images={'house_bg':house}
for kind in ['yard','stove','door','couch','bath','kid','wife']:
    name='cctv_'+kind;im=fit(name,(320,220))
    if kind=='couch':fill(im,(204,44,308,108),PAL[15])
    if kind=='kid':fill(im,(236,30,308,78),PAL[15])
    if kind=='stove':
        # The generated backsplash is already clear of objects in the pot zone.
        # Preserve its ceramic lighting; register only the fixed working surface.
        before=Image.open(SRC/(name+'_before.png'))
        im.paste(before.crop((60,116,260,144)),(60,116))
    if kind=='bath':fill(im,(124,44,196,68),PAL[11])
    images[name]=im

for name,im in images.items():
    assert im.size==((1320,192) if name=='house_bg' else (320,220))
    assert im.mode=='RGB' and set(im.getdata())<=set(PAL)
    im.save(OUT/(name+'.png'))

sheet=Image.new('RGB',(1360,850),PAL[0]);d=ImageDraw.Draw(sheet)
d.text((20,12),'IMAGE-GENERATED ORIGINAL 16-BIT ROOMS / 64 shared colors / area sampled',fill=PAL[3])
sheet.paste(house,(20,42))
for i,(name,im) in enumerate(list(images.items())[1:]):
    x=20+(i%4)*335;y=262+(i//4)*280
    d.text((x,y),name+' / 320 x 220',fill=PAL[3]);sheet.paste(im,(x,y+20))
sheet.save(ROOT/'tools/art/sheet_rooms.png')
(ROOT/'tools/art/rooms_crops.json').write_text(json.dumps(crops,indent=2)+'\n')
for box in [(82,186,120,208),(321,169,343,182)]:
    assert set(house.crop(worldbox(box)).getdata())=={PAL[15]}
for box,color in plain:assert set(house.crop(worldbox(box)).getdata())=={color}
for name,box in [('cctv_couch',(204,44,308,108)),('cctv_kid',(236,30,308,78))]:
    assert set(images[name].crop(box).getdata())=={PAL[15]},name
for f,digest in json.loads((SRC/'protected_hashes.json').read_text()).items():
    assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==digest,f
assert len(PAL)==64
print('PASS: eight exports, dimensions, opaque RGB, shared 64-color palette,')
print('layout wall fields, screens/working zones, index.html and frozen hashes.')
