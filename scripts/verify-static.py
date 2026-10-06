from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import json
import re

root = Path(__file__).resolve().parents[1]
routes = ['', 'contact-center/', 'cases/', 'pricing/', 'reputation/', 'contact/', 'privacy/', 'legal/', '404.html']

class Page(HTMLParser):
    def __init__(self, content):
        super().__init__()
        self.links = []
        self.ids = []
        self.headings = 0
        self.forms = 0
        self.feed(content)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'): self.ids.append(attrs['id'])
        if tag == 'h1': self.headings += 1
        if tag == 'form': self.forms += 1
        if tag in ['a', 'script', 'link', 'img']:
            url = attrs.get('href') or attrs.get('src')
            if url: self.links.append(url)

pages = {}
for route in routes:
    filename = root / (route + 'index.html' if route.endswith('/') or not route else route)
    content = filename.read_text()
    p = Page(content)
    assert p.headings == 1, f'{route}: h1'
    assert len(p.ids) == len(set(p.ids)), f'{route}: duplicate IDs'
    assert p.forms == 0, f'{route}: form'
    assert content.count('gtag/js?id=G-8S2N18S2YX') == 1, f'{route}: GA4'
    assert 'assets/site.css' not in content and 'assets/site.js' not in content, f'{route}: old assets'
    assert not re.search(r'3,300円|(?<!\d)3300(?!\d)|超過料金', content), f'{route}: obsolete pricing'
    pages[route] = p

checked = 0
for route, page in pages.items():
    for link in page.links:
        url = urlsplit(urljoin('https://killerword.info/' + route, link))
        if url.scheme not in ['http', 'https'] or url.netloc != 'killerword.info': continue
        filepath = root / unquote(url.path).lstrip('/')
        if url.path.endswith('/'): filepath /= 'index.html'
        assert filepath.is_file(), f'{route}: missing {link}'
        if url.fragment:
            assert unquote(url.fragment) in Page(filepath.read_text()).ids, f'{route}: anchor {link}'
        checked += 1

assert (root/'CNAME').read_text().strip() == 'killerword.info'
assert (root/'robots.txt').read_text().strip() == 'User-agent: *\nAllow: /\n\nSitemap: https://killerword.info/sitemap.xml'
assert (root/'sitemap.xml').read_text().count('<loc>') == 8
assert (root/'cases/index.html').read_text().count('class="case-item"') == 30
for route in ['index.html', 'pricing/index.html']:
    content = (root/route).read_text()
    for price in ['165,000円', '297,000円', '440,000円〜', '11,000円', '33,000円', '1案件 1,650円（税込）']:
        assert price in content, f'{route}: price {price}'
reputation = (root/'reputation/index.html').read_text()
for price in ['26,000円', '50,000円', '120,000円', '230,000円', '7,000円', '10,000円', '8,000円', '27,000円', '42,000円', '78,000円']:
    assert price in reputation, f'reputation: price {price}'
assert '初回100件は1店舗1回まで' in reputation
assert '料金は内容に応じてご案内します。' in reputation
print(json.dumps({'pages': len(pages), 'internalReferences': checked, 'cases':30, 'sitemapURLs':8, 'result':'PASS'}, ensure_ascii=False))
