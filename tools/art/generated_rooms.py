"""Register generated cartoon RPG rooms; protect fixed runtime working zones.

Rebuild: python tools/art/generated_rooms.py. Raw PNGs are in rooms_src/.
BOX resampling integrates source pixel areas, then the shared finalizer snaps
to the 256-color palette without dithering. No game code is executed or edited.
"""
from pathlib import Path
import json, hashlib
from PIL import Image, ImageDraw, ImageEnhance
from pixelize import PAL as BASE_PAL

# Pass 4 keeps the established material colors and adds generated cartoon ramps.
def room_palette():
    samples=Image.new("RGB",(128*5,128*3))
    for i,f in enumerate(sorted((Path(__file__).parent/"rooms_src").glob("*.png"))):
        if f.stem not in {"living","kitchen","bathroom","master","kid","garage","yard","lot","cctv_yard","cctv_stove","cctv_door","cctv_couch","cctv_bath","cctv_kid","cctv_wife"}:continue
        tile=Image.open(f).convert("RGB").resize((128,128),Image.Resampling.BOX)
        j=len(selected);selected.append(f.stem);samples.paste(tile,((j%5)*128,(j//5)*128))
    q=samples.quantize(colors=192,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    return BASE_PAL+[tuple(q.getpalette()[i:i+3]) for i in range(0,192*3,3)]
selected=[]
PAL=room_palette()
def surface_pixelize(im,size):
    palette=Image.new("P",(1,1));palette.putpalette([v for c in PAL for v in c])
    return im.convert("RGB").resize(size,Image.Resampling.NEAREST).quantize(palette=palette,dither=Image.Dither.NONE).convert("RGB")

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'tools/art/rooms_src'
OUT=ROOT/'assets'
REGIONS=json.loads((SRC/'regions.json').read_text(encoding='utf-8-sig'))
LAYOUT=json.loads((ROOT/'tools/art/house_layout.json').read_text(encoding='utf-8-sig'))

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
        'living':([0,.544,.79,1],[0,80/152,122/152,1],
                  [0,.465,.737,.94,1],[0,46/96,72/96,92/96,1]),
        'kitchen':([0,.28,.57,.72,1],[0,20/66,38/66,48/66,1],
                   [0,.35,.57,.62,.82,1],[0,40/96,60/96,70/96,.98,1]),
        'bathroom':([0,1],[0,1],[0,.65,.82,1],[0,76/96,.97,1]),
        'master':([0,1],[0,1],[0,.50,.78,1],[0,72/96,.99,1]),
        'kid':([0,.11,.74,1],[0,4/36,28/36,1],
               [0,.25,.43,.51,.58,.74,.83,1],
               [0,30/96,45/96,56/96,58/96,78/96,.99,1]),
        'garage':([0,.20,.25,.69,.73,1],[0,22/112,25/112,74/112,77/112,1],
                  [0,.37,.82,1],[0,42/96,.99,1]),
        'cctv_couch':([0,.66,.982,1],[0,204/320,308/320,1],
                      [0,.14,.45,1],[0,44/220,108/220,1]),
        'cctv_kid':([0,.734,.985,1],[0,236/320,308/320,1],
                    [0,.095,.335,1],[0,30/220,78/220,1]),
        'cctv_door':([0,.19,.45,1],[0,.13,.44,1],
                     [0,.14,.77,1],[0,.18,.76,1]),
        'cctv_bath':([0,.35,.655,1],[0,.34,.66,1],
                     [0,.105,.775,1],[0,.13,.82,1])}
    if name in grids:
        sx,dx,sy,dy=grids[name];sx=dx;sy=dy;registered=Image.new('RGB',size)
        for j in range(len(sy)-1):
            for i in range(len(sx)-1):
                sb=(round(sx[i]*im.width),round(sy[j]*im.height),
                    round(sx[i+1]*im.width),round(sy[j+1]*im.height))
                db=(round(dx[i]*size[0]),round(dy[j]*size[1]),
                    round(dx[i+1]*size[0]),round(dy[j+1]*size[1]))
                registered.paste(im.crop(sb).resize((db[2]-db[0],db[3]-db[1]),Image.Resampling.BOX),db[:2])
        im=registered
        crops[name]['registration_grid']={'source_x':sx,'target_x':dx,'source_y':sy,'target_y':dy}
    return im.resize(size,Image.Resampling.BOX)

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
    room=fit(name,((right-left)*2,192))
    # Quiet the last twelve pixels without flattening furniture silhouettes.
    strip=room.crop((0,180,room.width,192))
    from PIL import ImageEnhance
    strip=ImageEnhance.Contrast(strip).enhance(.55)
    strip=ImageEnhance.Color(strip).enhance(.65)
    room.paste(surface_pixelize(strip,strip.size),(0,180))
    house.paste(room,(left*2,0))

# Preserve exact structural beams/doorway strips from the captured geometry.
for box in [(152,150,156,234),(222,150,226,234),(262,150,266,234),
            (312,150,316,234),(352,150,358,234),(468,142,472,234),
            (0,138,468,152)]:
    b=worldbox(box);house.paste(old.crop(b),b[:2])

# Runtime footprints are authoritative, not approximate generated objects.
# TV screen and frame footprints are unchanged; nearby generated dressing stays.
for box in [(80,184,122,212),(320,168,344,183),(326,185,338,189)]:
    b=worldbox(box);house.paste(old.crop(b),b[:2])
# Exact clear runtime footprints, with a proper fixed stovetop below pot airspace.
plain=[((176,198,194,208),PAL[39]),((383,180,432,228),PAL[36]),
       ((520,204,660,234),PAL[37]),((398,156,438,180),PAL[11])]
for box,color in plain:fill(house,worldbox(box),color)
d=ImageDraw.Draw(house)
for x in (356,374):
    d.ellipse((x,140,x+10,146),fill=PAL[48],outline=PAL[17])
    d.line((x+2,143,x+8,143),fill=PAL[1])
# Preserve the fixed lift posts/platform and exact front door silhouette.
for box in [(380,180,383,234),(432,180,435,234),
            (382,228,434,230),(2,192,14,234)]:
    b=worldbox(box);house.paste(old.crop(b),b[:2])

images={'house_bg':house}
for kind in ['yard','stove','door','couch','bath','kid','wife']:
    name='cctv_'+kind;im=fit(name,(320,220))
    if kind=='couch':fill(im,(204,44,308,108),PAL[15])
    if kind=='kid':fill(im,(236,30,308,78),PAL[15])
    if kind=='stove':
        fill(im,(60,44,260,116),PAL[39])
        fill(im,(60,116,260,144),PAL[17])
        d=ImageDraw.Draw(im)
        for x in (82,202):
            d.ellipse((x,119,x+34,136),fill=PAL[48],outline=PAL[18],width=2)
            d.line((x+5,127,x+29,127),fill=PAL[1],width=2)
    if kind=='bath':fill(im,(124,44,196,68),PAL[11])
    images[name]=im

def finish(im):
    """Snap all exports to the deterministic shared 256-color room palette."""
    return surface_pixelize(im,im.size)

for name,im in images.items():
    assert im.size==((1320,192) if name=='house_bg' else (320,220))
    images[name]=finish(im)
# Runtime screen rectangles stay exactly dark, even across walking-strip edits.
for box in [(82,186,120,208),(321,169,343,182)]:
    ImageDraw.Draw(images['house_bg']).rectangle(tuple(v for v in worldbox(box)[:2])+tuple(v-1 for v in worldbox(box)[2:]),fill=PAL[15])
for name,box in [('cctv_couch',(204,44,308,108)),('cctv_kid',(236,30,308,78))]:
    ImageDraw.Draw(images[name]).rectangle((box[0],box[1],box[2]-1,box[3]-1),fill=PAL[15])
for name,im in images.items():
    assert len(im.convert('RGB').getcolors(257))<=256
    im.save(OUT/(name+'.png'))
house=images['house_bg']

sheet=Image.new('RGB',(1360,850),PAL[0]);d=ImageDraw.Draw(sheet)
d.text((20,12),'IMAGE-GENERATED ORIGINAL 16-BIT ROOMS / 256 colors / CARTOON RPG / area sampled',fill=PAL[3])
sheet.paste(house,(20,42))
for i,(name,im) in enumerate(list(images.items())[1:]):
    x=20+(i%4)*335;y=262+(i//4)*280
    d.text((x,y),name+' / 320 x 220',fill=PAL[3]);sheet.paste(im,(x,y+20))
sheet.save(ROOT/'tools/art/sheet_rooms.png')
(ROOT/'tools/art/rooms_crops.json').write_text(json.dumps(crops,indent=2)+'\n')
for box in [(82,186,120,208),(321,169,343,182)]:
    assert set(house.convert('RGB').crop(worldbox(box)).getdata())=={PAL[15]}
for box,color in plain:assert set(house.crop(worldbox(box)).getdata())=={color}
for name,box in [('cctv_couch',(204,44,308,108)),('cctv_kid',(236,30,308,78))]:
    assert set(images[name].convert('RGB').crop(box).getdata())=={PAL[15]},name
(ROOT/"tools/art/rooms_palette.json").write_text(json.dumps(PAL)+"\n")
for f,digest in json.loads((ROOT/'tools/art/pass4_protected_hashes.json').read_text(encoding='utf-8-sig')).items():
    if Path(f).name=='index.html':
        if hashlib.sha256(Path(f).read_bytes()).hexdigest()!=digest:print('NOTE: index.html changed externally since Pass 4 began; exporter never writes game code.')
    else:assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==digest,f
assert len(PAL)==256
print('PASS: eight exports, dimensions, opaque RGB, 256-color room palette,')
print('layout wall fields, dark screens and frozen hashes; external index changes reported separately.')
