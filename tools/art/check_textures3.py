"""Check exported texture UVs, dimensions, colors, alpha and sprite anchors."""
from pathlib import Path
import hashlib
from PIL import Image
from pixelize import PAL
import textures3

SIZES={**{f'tex_{k}':(64,64) for k in ['grass','sand','snow','desert','water0','water1']},
 'tex_building':(128,192),'tex_rock':(128,128),'tex_cliff':(128,256),
 'sky_day':(1024,240),'sky_dusk':(1024,240),'bb_tree':(96,192),
 'bb_palm':(96,192),'bb_bush':(96,64),'bb_chest':(64,48),
 'bb_vend':(64,112),'bb_steve':(64,96),'bb_enemy':(64,96),
 'bb_ally':(64,96),'island_bg':(1200,520),'map_island':(2000,2000)}

def check():
    for name,size in SIZES.items():
        im=Image.open(textures3.OUT/(name+'.png')).convert('RGBA')
        assert im.size==size,(name,im.size)
        alpha=set(im.getchannel('A').getdata())
        if name.startswith('bb_'):
            assert alpha=={0,255},name
            box=im.getbbox();assert box==(1,0,size[0]-1,size[1]),(name,box)
            assert abs(box[0]-(size[0]-box[2]))<=1,name
        else:assert alpha=={255},name
        colors={p[:3] for p in im.getdata() if p[3]}
        if name in ('bb_enemy','bb_ally'):
            assert all(r==g==b and r in (48,104,172,228) for r,g,b in colors),name
        else:assert colors<=set(PAL),name
        if name in ('sky_day','sky_dusk') or name.startswith('tex_') and size==(64,64):
            assert list(im.crop((0,0,1,size[1])).getdata())==list(im.crop((size[0]-1,0,size[0],size[1])).getdata()),name
        if name.startswith('tex_') and size==(64,64):
            assert list(im.crop((0,0,size[0],1)).getdata())==list(im.crop((0,size[1]-1,size[0],size[1])).getdata()),name
    assert (textures3.OUT/'bb_enemy.png').read_bytes()==(textures3.OUT/'bb_ally.png').read_bytes()
    assert (textures3.OUT/'tex_water0.png').read_bytes()!=(textures3.OUT/'tex_water1.png').read_bytes()
    paths=[textures3.OUT/(n+'.png') for n in SIZES]+[textures3.ART/'sheet3.png']
    before={p:hashlib.sha256(p.read_bytes()).digest() for p in paths}
    textures3.main()
    assert all(hashlib.sha256(p.read_bytes()).digest()==h for p,h in before.items())
    print('PASS: 21 PNGs; exact sizes, palette/grayscale, opacity, binary alpha, bottom-center anchors, floor XY / sky X seams, distinct water frames, deterministic regeneration.')

if __name__=='__main__':check()
