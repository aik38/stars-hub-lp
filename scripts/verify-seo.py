"""Audit technical SEO and, when supplied, preserve an exact Git baseline."""
from argparse import ArgumentParser
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import json
import re
import subprocess
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
origin = 'https://killerword.info/'
routes = ['', 'contact-center/', 'cases/', 'pricing/', 'reputation/', 'contact/', 'privacy/', 'legal/']


class SEOPage(HTMLParser):
    def __init__(self, content):
        super().__init__()
        self.tags = []
        self.jsonld = []
        self.script = None
        self.breadcrumb = []
        self.in_breadcrumb = False
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.script = []
        if 'breadcrumb' in attrs.get('class', '').split():
            self.in_breadcrumb = True

    def handle_data(self, data):
        if self.script is not None:
            self.script.append(data)
        if self.in_breadcrumb:
            self.breadcrumb.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self.script is not None:
            self.jsonld.append(json.loads(''.join(self.script)))
            self.script = None
        if tag == 'p':
            self.in_breadcrumb = False

    def attrs(self, tag):
        return [attrs for name, attrs in self.tags if name == tag]


parser = ArgumentParser()
parser.add_argument('--baseline-ref')
args = parser.parse_args()
types = []
preserved = []
pages = {}
for route in routes + ['404.html']:
    filename = route + 'index.html' if route != '404.html' else route
    content = (root / filename).read_text()
    page = SEOPage(content)
    pages[route] = page
    canonical = [a['href'] for a in page.attrs('link') if a.get('rel') == 'canonical']
    assert canonical == [origin + route], f'{route}: canonical'
    meta = {a.get('name') or a.get('property'): a.get('content') for a in page.attrs('meta')}
    assert meta['og:url'] == canonical[0], f'{route}: og:url'
    for name in ['og:image', 'twitter:image']:
        assert meta[name] == origin + 'assets/ogp.png', f'{route}: {name}'
    robots = meta.get('robots', 'index, follow').lower()
    assert ('noindex' in robots) == (route == '404.html'), f'{route}: robots'
    if route == '404.html':
        assert 'follow' in robots and 'nofollow' not in robots
    assert page.attrs('html')[0].get('lang') == 'ja', f'{route}: lang'
    for tag in ['header', 'main', 'footer']:
        assert len(page.attrs(tag)) == 1, f'{route}: {tag}'
    assert page.attrs('nav'), f'{route}: nav'
    assert all(a.get('type') == 'button' for a in page.attrs('button')), f'{route}: button type'
    assert all(a.get('href') for a in page.attrs('a')), f'{route}: anchor href'
    assert all(a.get('alt') for a in page.attrs('img')), f'{route}: image alt'
    ids = {a['id'] for _, a in page.tags if a.get('id')}
    for _, attrs in page.tags:
        for attribute in ['aria-controls', 'aria-labelledby', 'aria-describedby']:
            assert set(attrs.get(attribute, '').split()) <= ids, f'{route}: {attribute}'
    assert any('skip-link' in a.get('class', '').split() and a.get('href') == '#main' for a in page.attrs('a'))
    icons = [a['href'] for a in page.attrs('link') if a.get('rel') == 'icon']
    assert [urljoin(origin + route, icon) for icon in icons] == [origin + 'assets/favicon.svg']
    scripts = page.attrs('script')
    shared = [a for a in scripts if a.get('src', '').endswith('assets/top.js')]
    assert len(shared) == 1 and 'defer' in shared[0], f'{route}: deferred shared JS'
    assert sum('gtag/js?id=G-8S2N18S2YX' in a.get('src', '') for a in scripts) == 1, f'{route}: GA4'
    assert content.count("gtag('config', 'G-8S2N18S2YX')") == 1, f'{route}: GA4 config'
    preconnect = {a['href'] for a in page.attrs('link') if a.get('rel') == 'preconnect'}
    assert {'https://fonts.googleapis.com', 'https://fonts.gstatic.com'} <= preconnect

    if route == '404.html':
        assert page.jsonld == [], '404 must not receive public-page JSON-LD'
    else:
        assert len(page.jsonld) == 1, f'{route}: JSON-LD block count'
        data = page.jsonld[0]
        assert data['@context'] == 'https://schema.org'
        if not route:
            assert set(data) == {'@context', '@graph'}
            assert len(data['@graph']) == 2
            nodes = {node['@type']: node for node in data['@graph']}
            assert set(nodes) == {'WebSite', 'Organization'}
            for kind, node in nodes.items():
                assert node['name'] == 'STARS HUB' and node['alternateName'] == 'スターズハブ'
                assert node['url'] == origin
                assert node['@id'] == origin + ('#website' if kind == 'WebSite' else '#organization')
                allowed = {'@type', '@id', 'name', 'alternateName', 'url'}
                if kind == 'Organization':
                    allowed |= {'email', 'address'}
                    assert node['email'] == 'm-asakura@killerword.info'
                    address = node['address']
                    assert set(address) == {'@type', 'postalCode', 'addressRegion', 'addressLocality', 'streetAddress'}
                    assert address['@type'] == 'PostalAddress'
                    legal = (root / 'legal/index.html').read_text()
                    displayed = re.search(r'<dt>所在地</dt><dd>(.*?)</dd>', legal, re.S).group(1)
                    displayed = unescape(displayed.replace('<br>', '\n'))
                    structured = '〒' + address['postalCode'] + '\n' + address['addressRegion'] + address['addressLocality'] + address['streetAddress']
                    assert structured == displayed, 'Organization address differs from legal page'
                assert set(node) == allowed, f'{kind}: unrequested fields'
                types.append(kind)
        else:
            assert set(data) == {'@context', '@type', 'itemListElement'}
            assert data['@type'] == 'BreadcrumbList'
            names = ''.join(page.breadcrumb).strip().split(' / ')
            assert len(names) == 2
            expected = [{'@type': 'ListItem', 'position': position, 'name': name, 'item': origin if position == 1 else canonical[0]} for position, name in enumerate(names, 1)]
            assert data['itemListElement'] == expected, f'{route}: visible breadcrumb mismatch'
            types.append('BreadcrumbList')

    if args.baseline_ref:
        before = subprocess.check_output(['git', 'show', args.baseline_ref + ':' + filename], cwd=root, text=True)
        # Removing only the newly inserted head data must recover the exact file.
        without_jsonld = re.sub(r'\n<script type="application/ld\+json">\n.*?\n</script>\n', '', content, flags=re.S)
        assert without_jsonld == before, f'{route}: non-JSON-LD HTML changed'
        assert re.search(r'<body\b.*</body>', content, re.S).group() == re.search(r'<body\b.*</body>', before, re.S).group(), f'{route}: body changed'
        preserved.append(filename)

xml = ET.parse(root / 'sitemap.xml')
namespace = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
assert xml.getroot().tag == namespace + 'urlset'
assert [el.text for el in xml.findall('.//' + namespace + 'loc')] == [origin + route for route in routes]
assert len(xml.findall(namespace + 'url')) == 8
assert all(set(el.tag for el in item) == {namespace + 'loc'} for item in xml.getroot())
assert (root / 'robots.txt').read_text().strip() == 'User-agent: *\nAllow: /\n\nSitemap: https://killerword.info/sitemap.xml'
assert (root / 'CNAME').read_text().strip() == 'killerword.info'
assets = []
if args.baseline_ref:
    assets = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', args.baseline_ref, 'assets/'], cwd=root, text=True).splitlines()
    for filename in assets + ['robots.txt', 'sitemap.xml', 'CNAME']:
        assert (root / filename).read_bytes() == subprocess.check_output(['git', 'show', args.baseline_ref + ':' + filename], cwd=root), f'{filename}: preserved asset changed'
print(json.dumps({'result': 'PASS', 'publicPages': 8, 'canonical': 9, 'sitemapURLs': 8, '404Noindex': True, 'jsonld': {kind: types.count(kind) for kind in ['WebSite', 'Organization', 'BreadcrumbList']}, 'baseline': args.baseline_ref, 'unchangedHTMLOutsideJSONLD': len(preserved), 'unchangedAssets': len(assets)}, ensure_ascii=False))
