"""Download public client artwork referenced by the saved Linktree page data."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import re
from urllib.parse import urlparse, urlunparse
from urllib.request import Request, urlopen

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / 'static' / 'website' / 'images' / 'linktree'
DESTINATION.mkdir(parents=True, exist_ok=True)
data = json.loads((ROOT / 'reference' / 'linktree-data.json').read_text(encoding='utf-8'))
props = data['props']['pageProps']
candidates = {}


def add(url, label):
    if not url or not isinstance(url, str) or not url.startswith('https://'):
        return
    parsed = urlparse(url)
    if parsed.hostname == 'ugc.production.linktr.ee':
        url = urlunparse(parsed._replace(query=''))
    candidates.setdefault(url, label)


add(props.get('customAvatar'), 'treava-profile')
add(props.get('account', {}).get('theme', {}).get('background', {}).get('imageUrl'), 'profile-background')
for index, link in enumerate(props.get('links', [])):
    label = link.get('title') or 'link-' + str(index)
    add(link.get('thumbnail'), label)
    add((link.get('modifiers') or {}).get('thumbnailUrl'), label)
    add(((link.get('context') or {}).get('listing') or {}).get('imageUrl'), label + '-listing')
    add((link.get('metaData') or {}).get('image'), label + '-preview')


def download(item):
    index, (url, label) = item
    slug = re.sub(r'[^a-z0-9]+', '-', label.lower()).strip('-')[:70] or 'artwork'
    stem = f'{index:02d}-{slug}'
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urlopen(request, timeout=35) as response:
            content = response.read()
        scratch = DESTINATION / (stem + '.download')
        scratch.write_bytes(content)
        with Image.open(scratch) as image:
            extension = {'JPEG': '.jpg', 'PNG': '.png', 'WEBP': '.webp', 'GIF': '.gif'}.get(image.format, '.png')
            width, height = image.size
        output = scratch.with_suffix(extension)
        scratch.rename(output)
        return {'label': label, 'url': url, 'file': str(output.relative_to(ROOT)).replace('\\', '/'), 'width': width, 'height': height, 'bytes': len(content)}
    except Exception as error:
        return {'label': label, 'url': url, 'error': str(error)}


records = []
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(download, item) for item in enumerate(candidates.items(), start=1)]
    for future in as_completed(futures):
        record = future.result()
        records.append(record)
        print(json.dumps({key: record[key] for key in record if key != 'url'}), flush=True)
records.sort(key=lambda item: item.get('file', item['label']))
(ROOT / 'reference' / 'linktree-images.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
failures = sum('error' in record for record in records)
print(f'Downloaded {len(records) - failures} of {len(records)} public client images; {failures} failures.')
raise SystemExit(1 if failures else 0)
