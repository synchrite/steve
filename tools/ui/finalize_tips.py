"""Finalize original imagegen icons using the repo's shared palette pipeline."""
from pathlib import Path
import json, sys
from PIL import Image, ImageDraw
sys.path.insert(0,str(Path('tools/art').resolve()))
from pixelize import surface_pixelize
sources=json.loads(Path('tools/ui/tips_sources.json').read_text())
dest=Path('assets/ui/tips');dest.mkdir(parents=True,exist_ok=True)
sheet=Image.new('RGB',(4*192,3*212),'#302d32');d=ImageDraw.Draw(sheet)
for i,(name,source) in enumerate(sources.items()):
    # Deliberate small raster, palette snap, then exact nearest-neighbor display.
    im=Image.open(source).convert('RGB').resize((64,64),Image.Resampling.NEAREST)
    im=surface_pixelize(im,(64,64));im.save(dest/(name+'.png'))
    x=(i%4)*192;y=(i//4)*212
    sheet.paste(im.resize((192,192),Image.Resampling.NEAREST),(x,y));d.text((x+6,y+196),name,fill='#fff0d5')
sheet.save('tools/ui/tips_sheet.png')
print('12 original icons finalized at 64 x 64 using shared palette.')
