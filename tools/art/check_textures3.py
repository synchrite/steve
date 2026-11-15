"""Check exported texture UVs, dimensions, colors, alpha and sprite anchors."""
from pathlib import Path
import hashlib
from PIL import Image
from pixelize import PAL
import textures3

SIZES={**{f'tex_{k}':(32,32) for k in ['grass','sand','snow','desert','water0','water1']},
 'tex_building':(64,96),'tex_rock':(64,64),'tex_cliff':(64,128),
 'sky_day':(512,120),'sky_dusk':(512,120),'bb_tree':(48,96),
 'bb_palm':(48,96),'bb_bush':(48,32),'bb_chest':(32,24),
 'bb_vend':(32,56),'bb_steve':(32,48),'bb_enemy':(32,48),
 'bb_ally':(32,48),'island_bg':(600,260),'map_island':(1000,1000)}

def check():
    for name,size in SIZES.items():
        im=Image.open(textures3.OUT/(name+'.png')).convert('RGBA')
        assert im.size==size,(name,im.size)
        alpha=set(im.getchannel('A').getdata())
        if name.startswith('bb_'):
            assert alpha=={0,255},name
            box=im.getbbox();assert box[3]==size[1],name
            assert abs(box[0]-(size[0]-box[2]))<=1,name
        else:assert alpha=={255},name
        colors={p[:3] for p in im.getdata() if p[3]}
        if name in ('bb_enemy','bb_ally'):
            assert all(r==g==b and r in (48,104,172,228) for r,g,b in colors),name
        else:assert colors<=set(PAL),name
        if name in ('sky_day','sky_dusk') or name.startswith('tex_') and size==(32,32):
            assert list(im.crop((0,0,1,size[1])).getdata())==list(im.crop((size[0]-1,0,size[0],size[1])).getdata()),name
        if name.startswith('tex_') and size==(32,32):
            assert list(im.crop((0,0,size[0],1)).getdata())==list(im.crop((0,size[1]-1,size[0],size[1])).getdata()),name
    assert (textures3.OUT/'bb_enemy.png').read_bytes()==(textures3.OUT/'bb_ally.png').read_bytes()
    assert (textures3.OUT/'tex_water0.png').read_bytes()!=(textures3.OUT/'tex_water1.png').read_bytes()
    paths=[textures3.OUT/(n+'.png') for n in SIZES]+[textures3.ART/'sheet3.png']
    before={p:hashlib.sha256(p.read_bytes()).digest() for p in paths}
    textures3.main()
    assert all(hashlib.sha256(p.read_bytes()).digest()==h for p,h in before.items())
    print('PASS: 21 PNGs; exact sizes, palette/grayscale, opacity, binary alpha, bottom-center anchors, floor XY / sky X seams, distinct water frames, deterministic regeneration.')

if __name__=='__main__':check()
