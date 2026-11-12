"""Make small copies of every image under <site>/media for the grid.

media/works/a.jpg -> media/works/t/a.jpg (1200px long edge). Originals are not touched.
Usage: python thumbs.py <site-folder>
"""
import pathlib, sys
from PIL import Image, ImageOps

LONG = 1200
EXTS = {'.jpg', '.jpeg', '.png', '.webp'}
media = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.') / 'media'
made = 0
for src in sorted(media.rglob('*')):
    if not src.is_file() or src.suffix.lower() not in EXTS or src.parent.name == 't':
        continue
    out = src.parent / 't' / src.name
    if out.exists():
        continue
    out.parent.mkdir(exist_ok=True)
    with Image.open(src) as im:
        icc = im.info.get('icc_profile')
        im = ImageOps.exif_transpose(im)
        im.thumbnail((LONG, LONG), Image.LANCZOS)
        kw = {'icc_profile': icc} if icc else {}
        ext = src.suffix.lower()
        if ext in ('.jpg', '.jpeg'):
            im.convert('RGB').save(out, 'JPEG', quality=88, subsampling=0, optimize=True, progressive=True, **kw)
        elif ext == '.webp':
            im.save(out, 'WEBP', quality=88, **kw)
        else:
            im.save(out, 'PNG', optimize=True, **kw)
    made += 1
print(f'thumbnails made: {made}')
