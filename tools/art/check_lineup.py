"""Validate the approval-only art pipeline; never export to assets/."""
from hashlib import sha256
from PIL import Image
from pixelize import PAL, ROOT, dog, human, couch, door, lamb, main


def check():
    sprites = {
        'stand': (dog(), (52,44)), 'sit': (dog(True), (40,48)),
        'steve': (human(), (20,44)), 'wife': (human('wife'), (20,44)),
        'kid': (human('kid'), (14,36)),
        'seated': (human(seated=True), (32,48)),
        'door': (door(), (40,84)), 'couch': (couch(), (84,44)),
        'lamb': (lamb(), (24,20)),
    }
    for name, (im, size) in sprites.items():
        assert im.size == size, name
        box = im.getbbox()
        assert box[3] == size[1], name
        assert abs(box[0] - (size[0] - box[2])) <= 1, name
        assert set(im.getchannel('A').tobytes()) == {0,255}, name
        colors = {rgb[:3] for rgb in im.getdata() if rgb[3]}
        assert colors <= set(PAL), name
        print(f'{name}: {size}, visible height {box[3]-box[1]}, {len(colors)} colors')
    # At ankle height the standing pose must have four separated legs.
    stand = sprites['stand'][0]
    row = [stand.getpixel((x,38))[3] != 0 for x in range(stand.width)]
    runs = sum(v and (x == 0 or not row[x-1]) for x,v in enumerate(row))
    assert runs == 4, f'Expected four separate legs at ankle height; got {runs}'
    before = sha256((ROOT/'lineup.png').read_bytes()).hexdigest()
    main()
    assert sha256((ROOT/'lineup.png').read_bytes()).hexdigest() == before
    im = Image.open(ROOT/'lineup.png').convert('RGBA')
    assert im.size == (1616,600)
    assert len(im.getcolors()) <= 32
    assert set(im.getchannel('A').tobytes()) == {255}
    native = im.resize((404,150), Image.Resampling.NEAREST)
    assert native.resize(im.size, Image.Resampling.NEAREST).tobytes() == im.tobytes()
    print('PASS: four separate legs; exact palette, binary alpha, anchors, 4x and reproducible PNG.')


if __name__ == '__main__':
    check()
