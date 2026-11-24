"""Create a visual inventory of downloaded public client artwork."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[1]
records = json.loads((ROOT / 'reference' / 'linktree-images.json').read_text(encoding='utf-8'))
records = [record for record in records if 'file' in record]
cell_width, cell_height, columns = 260, 300, 5
sheet = Image.new('RGB', (columns * cell_width, ((len(records) + columns - 1) // columns) * cell_height), '#ebe6ef')
draw = ImageDraw.Draw(sheet)
for index, record in enumerate(records):
    x, y = (index % columns) * cell_width, (index // columns) * cell_height
    with Image.open(ROOT / record['file']) as image:
        thumbnail = ImageOps.contain(image.convert('RGB'), (240, 248))
    sheet.paste(thumbnail, (x + (cell_width - thumbnail.width) // 2, y + 6))
    draw.text((x + 10, y + 258), Path(record['file']).stem[:34], fill='#24122b')
    draw.text((x + 10, y + 276), f"{record['width']} x {record['height']}", fill='#625468')
output = ROOT / 'reference' / 'linktree-contact-sheet.jpg'
sheet.save(output, quality=92)
print(output)
