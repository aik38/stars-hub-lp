#!/usr/bin/env python3
"""Validate approved facts, exact legal preservation, metadata and local links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re
import subprocess
import json
from build_site import ROOT, BASE, ROUTES, original

class Page(HTMLParser):
    def __init__(self, content):
        super().__init__(); self.nodes=[]; self.ids=[]; self.feed(content)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs); self.nodes.append((tag,attrs))
        if 'id' in attrs: self.ids.append(attrs['id'])
    def get(self, tag, **attrs):
        return [a for t,a in self.nodes if t==tag and all(a.get(k)==v for k,v in attrs.items())]

errors=[]; checks=0
def check(ok, message):
    global checks
    checks+=1
    if not ok: errors.append(message)

pages={p:Page((ROOT/p).read_text()) for p in ROUTES}
for path, p in pages.items():
    content=(ROOT/path).read_text(); before=original(path); old=Page(before)
    check(len(p.get('h1'))==1, f'{path}: h1 count')
    check(len(p.ids)==len(set(p.ids)), f'{path}: duplicate ids')
    check(p.get('html',lang='ja'), f'{path}: language')
    check('<meta charset="utf-8">' in content[:150], f'{path}: early charset')
    for selector in [('link',{'rel':'canonical'}),('meta',{'name':'description'}),('meta',{'property':'og:url'}),('meta',{'property':'og:title'}),('meta',{'name':'twitter:card'})]:
        tag,attrs=selector; check(p.get(tag,**attrs)==old.get(tag,**attrs),f'{path}: preserved {attrs}')
    ga=lambda s:re.findall(r'<script[^>]*>.*?</script>',s,re.S)[:2]
    check(ga(content)==ga(before),f'{path}: exact GA4 block')
    check(len(p.get('script',src='https://www.googletagmanager.com/gtag/js?id=G-8S2N18S2YX'))==1,f'{path}: GA4 loaded once')
    check('noindex' not in content,f'{path}: indexability preserved')
    for tag, attrs in p.nodes:
        if attrs.get('target')=='_blank': check('noopener' in attrs.get('rel',''),f'{path}: external target rel')
        for key in ('href','src'):
            if key not in attrs: continue
            url=urlsplit(attrs[key])
            if url.scheme or url.netloc: continue
            target=(ROOT/unquote(url.path.lstrip('/'))) if url.path.startswith('/') else (ROOT/path).parent/unquote(url.path)
            target=target.resolve()
            if target.is_dir(): target=target/'index.html'
            check(target.is_file(),f'{path}: missing target {attrs[key]}')
            if url.fragment and target.is_file() and target.suffix=='.html':
                other=Page(target.read_text())
                check(unquote(url.fragment) in other.ids,f'{path}: missing anchor {attrs[key]}')
    check('mailto:m-asakura@killerword.info' in content,f'{path}: email retained')
    check('https://lin.ee/X0mxy9O' in content,f'{path}: LINE retained')

for path in ['privacy/index.html','legal/index.html']:
    article=lambda s:re.search(r'<article\b.*?</article>',s,re.S).group()
    check(article((ROOT/path).read_text())==article(original(path)),f'{path}: legal article exact')
for path in ['CNAME','robots.txt','sitemap.xml','.nojekyll']:
    before=subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT)
    check((ROOT/path).read_bytes()==before,f'{path}: exact preservation')

home=(ROOT/'index.html').read_text()
hero=re.search(r'<section class="hero">.*?</section>',home,re.S).group()
check('165,000' not in hero,f'home: no price in hero')
check('すべての予約受付を、</span><span>ひとつに。' in hero,'home: H1 preserved')
check(home.count('<blockquote>')==7,'home: seven authorized voices')
for unwanted in ['アロマエステはメンズエステ等を含む業界上の呼称','その他予約型サービスには','上記のアロマエステ']:
    check(all(unwanted not in (ROOT/p).read_text() for p in ROUTES),f'no internal memo: {unwanted}')
for path in ['index.html','pricing/index.html']:
    c=(ROOT/path).read_text()
    for fact in ['165,000','297,000','440,000','50','100','150','11,000','33,000','3,300']:
        check(fact in c,f'{path}: required price {fact}')
for path in ['pricing/index.html','reputation/index.html']:
    c=(ROOT/path).read_text()
    for fact in ['27,500','52,800','126,500','242,000','7,700','11,000','9,900','29,700','49,500','88,000','22,000','33,000']:
        check(fact in c,f'{path}: supporting service price {fact}')
    check('法的な削除請求・発信者情報開示等の法律業務を行うサービスではありません。' in c,f'{path}: scope limit preserved')
for fact in ['181,500','176,000','予約に至らない問い合わせ','追加カウントなし','同じお客様が2件予約']:
    check(fact in (ROOT/'pricing/index.html').read_text(),f'pricing: counting definition / example {fact}')
for industry in ['アロマエステ','デリヘル','ホテヘル','ファッションヘルス','ソープ','その他予約型サービス','キャバクラ・ラウンジ','ガールズバー','ホストクラブ']:
    check(industry in home,f'home: industry {industry}')
check('この操作だけでは送信されません。' in (ROOT/'contact/index.html').read_text(),'contact: draft behavior clear')
check('localStorage' not in (ROOT/'assets/site.js').read_text(),'JS: no personal-data storage')
print(json.dumps({'checks':checks,'passed':checks-len(errors),'errors':errors},ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
