"""Finalize original generated lobby sprite studies through shared pixelize()."""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont
from pixelize import pixelize, PAL

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent.parent/'assets'/'lobby'
NAMES=['steve','bront','serein','vesper','solaro','rivet','orion']
NEW_NAMES=['hoops','narc','jug','neonpunk','glitch','rollerqueen','dad','sunny']

def frames(name):
    return ['0','1','2','3','dance0','dance1'] if name=='steve' else ['idle0','idle1','dance0','dance1','shoot0']

def split(im,n):
    # Locate transparent gutters around each figure, near the expected cell cuts.
    a=im.getchannel('A').point(lambda x:255 if x>=128 else 0)
    counts=[sum(a.crop((x,0,x+1,im.height)).getdata())//255 for x in range(im.width)]
    cuts=[0]
    for i in range(1,n):
        center=im.width*i/n
        lo=max(cuts[-1]+1,int(center-im.width/n*.24));hi=min(im.width,int(center+im.width/n*.24))
        cuts.append(min(range(lo,hi),key=lambda x:(counts[x],abs(x-center))))
    cuts.append(im.width)
    return [im.crop((cuts[i],0,cuts[i+1],im.height)) for i in range(n)]

def legacy_main():
    OUT.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(6*82+12,7*125+26),'#e4ddd0')
    d=ImageDraw.Draw(sheet);font=ImageFont.load_default()
    d.text((8,7),'ORIGINAL LOBBY FIGHTERS / 64x96 / TOP-LEFT LIGHT',fill='#302d32',font=font)
    manifest=[]
    for row,name in enumerate(NAMES):
        src=Image.open(ROOT/'lobby_sources'/f'{name}.png').convert('RGBA')
        # Pad with a valid color: Pillow otherwise considers unused black slots.
        palette=Image.new('P',(1,1))
        palette.putpalette([v for c in (PAL+[PAL[0]]*(256-len(PAL))) for v in c])
        alpha=src.getchannel('A')
        src=src.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA')
        src.putalpha(alpha)
        poses=split(src,len(frames(name)))
        steve_idle=None
        for col,(frame,pose) in enumerate(zip(frames(name),poses)):
            sprite=pixelize(pose,(64,96))
            if name=='steve' and col<4:
                # Lock anatomy and equipment across the bounce; compress the
                # upper body by 0/1/2/1 pixels while boots retain floor contact.
                if col==0:steve_idle=sprite.copy()
                else:
                    amount=[0,1,2,1][col]
                    sprite=Image.new('RGBA',(64,96))
                    upper=steve_idle.crop((0,0,64,72)).resize((64,72-amount),Image.Resampling.NEAREST)
                    sprite.paste(upper,(0,amount))
                    sprite.paste(steve_idle.crop((0,72,64,96)),(0,72))
                    if col==3:
                        # One-pixel glove relaxation on the returning beat.
                        glove=sprite.crop((15,49,24,57))
                        sprite.paste(glove,(16,49),glove)
            path=OUT/f'fighter_{name}_{frame}.png';sprite.save(path)
            x=12+col*82;y=29+row*125
            d.rectangle((x-2,y-2,x+65,y+96),fill='#648092')
            sheet.paste(sprite,(x,y),sprite)
            d.text((x,y+100),f'{name}/{frame}',fill='#302d32',font=font)
            assert sprite.size==(64,96)
            assert set(sprite.getchannel('A').getdata())<={0,255}
            box=sprite.getbbox();assert box[3]==96 and abs(box[0]-(64-box[2]))<=1
            assert all(p[:3] in PAL for p in sprite.getdata() if p[3])
            manifest.append(path.name)
    sheet.resize((sheet.width*3,sheet.height*3),Image.Resampling.NEAREST).save(ROOT/'sheet_lobby.png')
    print(f'{len(manifest)} PNGs: exact 64x96, binary alpha, shared palette, balanced bottom anchors; sheet exact 3x.')
    (ROOT/'lobby_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

def main():
    # Preserve all 36 approved originals byte-for-byte; only finalize new studies.
    import pixelize as shared
    samples=Image.new('RGB',(256*len(NEW_NAMES),256),'#302d32')
    for i,name in enumerate(NEW_NAMES):
        src=Image.open(ROOT/'lobby_sources'/f'{name}.png').convert('RGBA')
        tile=Image.new('RGB',src.size,'#302d32');tile.paste(src,mask=src.getchannel('A'))
        samples.paste(tile.resize((256,256),Image.Resampling.BOX),(i*256,0))
    q=samples.quantize(colors=192,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    palette=PAL+[tuple(q.getpalette()[i:i+3]) for i in range(0,576,3)]
    shared.PAL=palette
    for name in NEW_NAMES:
        src=Image.open(ROOT/'lobby_sources'/f'{name}.png').convert('RGBA')
        for frame,pose in zip(frames(name),split(src,5)):
            sprite=shared.pixelize(pose,(64,96))
            # Discard tiny isolated generation flecks, keeping deliberate clusters.
            pixels=sprite.load();seen=set()
            for yy in range(96):
                for xx in range(64):
                    if (xx,yy) in seen or not pixels[xx,yy][3]:continue
                    stack=[(xx,yy)];component=[];seen.add((xx,yy))
                    while stack:
                        x,y=stack.pop();component.append((x,y))
                        for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                            if 0<=nx<64 and 0<=ny<96 and (nx,ny) not in seen and pixels[nx,ny][3]:
                                seen.add((nx,ny));stack.append((nx,ny))
                    if len(component)<(40 if name=='jug' else 8):
                        for x,y in component:pixels[x,y]=(0,0,0,0)
            crop=sprite.crop(sprite.getbbox());sprite=Image.new('RGBA',(64,96))
            sprite.paste(crop,((64-crop.width)//2,96-crop.height))
            sprite.save(OUT/f'fighter_{name}_{frame}.png')
    names=NAMES+NEW_NAMES
    sheet=Image.new('RGB',(504,len(names)*125+26),'#e4ddd0');d=ImageDraw.Draw(sheet)
    d.text((8,7),'ORIGINAL RPG LOBBY FIGHTERS / 64x96 / PASS 4',fill='#302d32')
    manifest=[]
    for row,name in enumerate(names):
        for col,frame in enumerate(frames(name)):
            path=OUT/f'fighter_{name}_{frame}.png';sprite=Image.open(path).convert('RGBA')
            assert sprite.size==(64,96)
            assert set(sprite.getchannel('A').getdata())<={0,255}
            box=sprite.getbbox();assert box[3]==96 and abs(box[0]-(64-box[2]))<=1
            assert all(p[:3] in palette for p in sprite.getdata() if p[3])
            x=12+col*82;y=29+row*125
            d.rectangle((x-2,y-2,x+65,y+96),fill='#648092');sheet.paste(sprite,(x,y),sprite)
            d.text((x,y+99),name,fill='#302d32');d.text((x,y+111),frame,fill='#302d32');manifest.append(path.name)
    sheet.resize((sheet.width*3,sheet.height*3),Image.Resampling.NEAREST).save(ROOT/'sheet_lobby.png')
    (ROOT/'lobby_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (ROOT/'lobby_palette_pass4.json').write_text(json.dumps(palette)+'\n')
    print('PASS:',len(manifest),'sprites; exact size, palette, binary alpha, balanced floor anchors.')

if __name__=='__main__':main()
