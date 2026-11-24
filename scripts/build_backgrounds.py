"""Create text-free backgrounds from existing client photos, without an AI API.

The crops exclude poster headlines and retain the client's original photography.
Original downloads are never modified. Pillow is only needed to rebuild assets.
"""
import json
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / 'static' / 'website' / 'images'
DESTINATION = IMAGES / 'backgrounds'
DESTINATION.mkdir(parents=True, exist_ok=True)
SIZE = (2048, 1152)


def texture():
    with Image.open(IMAGES / 'linktree' / '02-profile-background.jpg') as image:
        base = ImageOps.fit(image.convert('RGB'), SIZE)
    # Original site purple gently tints the client's charcoal texture.
    return Image.blend(base, Image.new('RGB', SIZE, '#24122b'), .32)


def photo_crop(filename, box, dimensions, centering=(.5, .25)):
    with Image.open(IMAGES / filename) as image:
        return ImageOps.fit(image.convert('RGB').crop(box), dimensions, method=Image.Resampling.LANCZOS, centering=centering)


def place_photo(canvas, photo, x, fade_left=150, fade_right=0):
    mask = Image.new('L', photo.size, 255)
    values = []
    for position in range(photo.width):
        left = min(1, position / fade_left) if fade_left else 1
        right = min(1, (photo.width - 1 - position) / fade_right) if fade_right else 1
        values.append(round(255 * min(left, right)))
    strip = Image.new('L', (photo.width, 1))
    strip.putdata(values)
    mask = strip.resize(photo.size)
    canvas.paste(photo, (x, 0), mask)


specs = [
    {'name': 'hero', 'source': 'treava-hero.jpeg', 'box': (560, 0, 1280, 920), 'centering': (.5, .15)},
    {'name': 'about', 'source': 'treava-about.jpeg', 'box': (588, 40, 1024, 820), 'centering': (.55, .12)},
    {'name': 'book', 'source': 'treava-book.jpeg', 'box': (0, 0, 640, 710), 'centering': (.5, .25)},
]
manifest = []
for spec in specs:
    canvas = texture()
    photo = photo_crop(spec['source'], spec['box'], (1120, SIZE[1]), spec['centering'])
    place_photo(canvas, photo, SIZE[0] - photo.width)
    output = DESTINATION / (spec['name'] + '-bg.webp')
    canvas.save(output, 'WEBP', quality=88, method=6)
    manifest.append({'file': str(output.relative_to(ROOT)).replace('\\', '/'), 'source': spec['source'], 'crop': spec['box'], 'width': SIZE[0], 'height': SIZE[1], 'bytes': output.stat().st_size})

canvas = texture()
guide_source = 'linktree/18-creating-multiple-streams-behind-the-chair-listing.jpg'
plant = photo_crop(guide_source, (0, 0, 420, 1380), (690, SIZE[1]), (.5, .25))
chair = photo_crop(guide_source, (1590, 0, 2000, 1410), (860, SIZE[1]), (.5, .45))
place_photo(canvas, plant, 0, fade_left=0, fade_right=190)
place_photo(canvas, chair, SIZE[0] - chair.width, fade_left=190)
output = DESTINATION / 'guides-bg.webp'
canvas.save(output, 'WEBP', quality=88, method=6)
manifest.append({'file': str(output.relative_to(ROOT)).replace('\\', '/'), 'source': guide_source, 'crops': [(0, 0, 420, 1380), (1590, 0, 2000, 1410)], 'width': SIZE[0], 'height': SIZE[1], 'bytes': output.stat().st_size})
(ROOT / 'reference' / 'background-assets.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')

# Keep an inspection sheet alongside the provenance manifest.
preview_size = (1024, 576)
sheet = Image.new('RGB', (preview_size[0], len(manifest) * preview_size[1]), '#24122b')
for index, asset in enumerate(manifest):
    with Image.open(ROOT / asset['file']) as image:
        thumbnail = image.resize(preview_size, Image.Resampling.LANCZOS)
    sheet.paste(thumbnail, (0, index * preview_size[1]))
sheet.save(ROOT / 'reference' / 'background-contact-sheet.jpg', quality=92)
print(json.dumps(manifest, indent=2))
