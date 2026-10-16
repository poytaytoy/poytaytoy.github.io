"""Check required pages, feeds, canonical URLs, and local generated links."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

root = Path('public').resolve()
origin = 'https://poytaytoy.github.io'
required = ['index.html', 'about/index.html', 'projects/index.html',
            'posts/index.html', 'posts/welcome/index.html', '404.html',
            'index.xml', 'sitemap.xml', 'robots.txt']
for name in required:
    assert (root / name).is_file(), f'Missing {name}'
for name in ['index.xml', 'sitemap.xml']:
    ET.parse(root / name)

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.canonical = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ['href', 'src']:
            if key in attrs:
                self.links.append(attrs[key])
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical = attrs.get('href')

pages = list(root.rglob('*.html'))
for path in pages:
    page = Page()
    page.feed(path.read_text(encoding='utf-8'))
    if path.name != '404.html':
        assert page.canonical and page.canonical.startswith(origin + '/'), f'Bad canonical: {path}'
    for link in page.links:
        url = urlsplit(link)
        if url.scheme and url.scheme not in ['http', 'https']:
            continue
        if url.netloc and url.netloc != 'poytaytoy.github.io':
            continue
        if not url.path:
            continue
        target = (root / unquote(url.path).lstrip('/')) if url.path.startswith('/') else (path.parent / unquote(url.path))
        assert target.is_file() or (target / 'index.html').is_file(), f'Broken link in {path}: {link}'
print(f'Checked {len(pages)} HTML pages, required routes, XML feeds, canonical URLs, and local links.')
