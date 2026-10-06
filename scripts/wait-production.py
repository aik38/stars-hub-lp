"""Wait for the exact committed static assets to reach GitHub Pages."""
from pathlib import Path
from urllib.request import Request, urlopen
import hashlib
import os
import time

root = Path(__file__).resolve().parents[1]
routes = ['', 'contact-center/', 'cases/', 'pricing/', 'reputation/', 'contact/', 'privacy/', 'legal/', '404.html', 'assets/top.css', 'assets/details.css', 'assets/top.js', 'assets/favicon.svg', 'assets/ogp.png', 'robots.txt', 'sitemap.xml']
revision = os.environ.get('GITHUB_SHA', '20261007')
deadline = time.monotonic() + 240
remaining = set(routes)
while remaining and time.monotonic() < deadline:
    for route in sorted(remaining):
        filename = route + 'index.html' if not route or route.endswith('/') else route
        expected = hashlib.sha256((root/filename).read_bytes()).digest()
        try:
            request = Request('https://killerword.info/'+route+'?verification='+revision, headers={'Cache-Control':'no-cache'})
            with urlopen(request, timeout=10) as response:
                content = response.read()
                assert response.status == 200
            if hashlib.sha256(content).digest() == expected:
                remaining.remove(route)
                print('MATCH', route or '/', flush=True)
        except Exception as error:
            print('WAIT', route or '/', type(error).__name__, flush=True)
    if remaining: time.sleep(5)
assert not remaining, 'Production did not match committed files: '+repr(remaining)
print('Production matches all 16 committed pages/assets.', flush=True)
