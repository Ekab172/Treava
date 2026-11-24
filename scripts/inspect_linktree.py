"""Inspect the public Linktree source saved in reference/linktree.html."""
from html.parser import HTMLParser
import json
from pathlib import Path


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_data = False
        self.json_text = ''
        self.images = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'script' and attrs.get('id') == '__NEXT_DATA__':
            self.in_data = True
        if tag == 'img':
            self.images.append({key: attrs[key] for key in ('src', 'alt') if key in attrs})

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_data = False

    def handle_data(self, data):
        if self.in_data:
            self.json_text += data


parser = PageParser()
parser.feed(Path('reference/linktree.html').read_text(encoding='utf-8-sig'))
data = json.loads(parser.json_text) if parser.json_text else {}
Path('reference/linktree-data.json').write_text(json.dumps(data, indent=2), encoding='utf-8')
print('Data keys:', list(data))
print('Page props keys:', list(data.get('props', {}).get('pageProps', {})))
print('Rendered images:')
print(json.dumps(parser.images, indent=2))


def inspect(value, path=''):
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, str) and item.startswith(('https://', 'http://')):
                if not any(s in key.lower() for s in ('video', 'analytic', 'webhook')):
                    print(path + '.' + key, item)
            elif isinstance(item, (dict, list)):
                inspect(item, path + '.' + key)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            inspect(item, path + '[' + str(index) + ']')


inspect(data.get('props', {}).get('pageProps', {}))
