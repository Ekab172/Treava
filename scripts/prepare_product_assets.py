"""Optimize complete client product artwork and prepare the arched-frame portrait.

Source images are retained untouched. Product images keep their complete covers;
only the decorative portrait is cropped to the original mirror proportions.
Requires Pillow only when rebuilding assets.
"""
import json
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "static" / "website" / "images"
OUTPUT = IMAGES / "products"
OUTPUT.mkdir(parents=True, exist_ok=True)

PRODUCTS = [
    ("linktree/13-purchase-my-new-book-today.png", "book-cover.webp"),
    ("linktree/18-creating-multiple-streams-behind-the-chair-listing.jpg", "multiple-streams.webp"),
    ("linktree/19-creating-pillars-of-success.jpg", "pillars-of-success.webp"),
    ("linktree/21-evolving-for-the-salon-creative.jpg", "evolving.webp"),
]

manifest = []
for source, filename in PRODUCTS:
    with Image.open(IMAGES / source) as original:
        image = ImageOps.exif_transpose(original).convert("RGB")
        source_size = image.size
        if image.width > 560:
            height = round(image.height * 560 / image.width)
            image = image.resize((560, height), Image.Resampling.LANCZOS)
        destination = OUTPUT / filename
        image.save(destination, "WEBP", quality=88, method=6)
        manifest.append({
            "file": str(destination.relative_to(ROOT)).replace("\\", "/"),
            "source": source,
            "source_width": source_size[0],
            "source_height": source_size[1],
            "width": image.width,
            "height": image.height,
            "bytes": destination.stat().st_size,
            "cropped": False,
        })

portrait_source = "treava-hero.jpeg"
portrait_crop = (560, 0, 1280, 920)
with Image.open(IMAGES / portrait_source) as original:
    portrait = ImageOps.fit(
        ImageOps.exif_transpose(original).convert("RGB").crop(portrait_crop),
        (660, 924),
        method=Image.Resampling.LANCZOS,
        centering=(.5, .15),
    )
    destination = OUTPUT / "hero-portrait.webp"
    portrait.save(destination, "WEBP", quality=88, method=6)
    manifest.append({
        "file": str(destination.relative_to(ROOT)).replace("\\", "/"),
        "source": portrait_source,
        "crop": portrait_crop,
        "centering": [.5, .15],
        "width": portrait.width,
        "height": portrait.height,
        "bytes": destination.stat().st_size,
        "cropped": True,
    })

manifest_path = ROOT / "reference" / "product-assets.json"
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print(json.dumps(manifest, indent=2))
