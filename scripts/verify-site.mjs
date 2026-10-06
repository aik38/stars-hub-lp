import { chromium } from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';

const base = process.env.SITE_BASE_URL || 'http://127.0.0.1:8000/';
const routes = ['', 'contact-center/', 'cases/', 'pricing/', 'reputation/', 'contact/', 'privacy/', 'legal/', '404.html'];
const widths = [1440, 1024, 768, 390, 360];
const output = process.env.VERIFICATION_OUTPUT || 'verification-output';
await fs.mkdir(output, { recursive: true });
const browser = await chromium.launch({ headless: true });
const records = [];
const failures = [];
const responses = [];
try {
  for (const width of widths) {
    const context = await browser.newContext({ viewport: { width, height: 1000 } });
    // Keep checks from sending artificial traffic to GA4. The exact GA4 source
    // and config remain in the page and are checked below.
    await context.route(/googletagmanager\.com|google-analytics\.com/, route => route.fulfill({ status: 200, body: '' }));
    const page = await context.newPage();
    for (const route of routes) {
      const errors = [];
      const onError = error => errors.push(error.message);
      page.on('pageerror', onError);
      const response = await page.goto(new URL(route, base).href, { waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts.ready);
      const record = await page.evaluate(() => {
        const visible = el => !!el.getClientRects().length && getComputedStyle(el).visibility !== 'hidden';
        const overflow = [...document.body.querySelectorAll('*')].filter(el => visible(el) && !el.closest('.skip-link')).filter(el => {
          const box = el.getBoundingClientRect();
          return box.width && (box.left < -1 || box.right > innerWidth + 1);
        }).map(el => ({ tag: el.tagName, class: el.className, text: el.textContent.trim().slice(0, 80) }));
        const targets = [...document.querySelectorAll('.button,.menu-toggle,.footer-nav a,.site-nav a,.faq-question,.case-index a,.section-index a')].filter(visible);
        const additional = document.querySelector('.price-additional p');
        const initial = document.querySelector('.price-notes > div:first-child p');
        const fees = [...document.querySelectorAll('.service-fees')].map(list => ({
          label: list.getAttribute('aria-label'),
          rows: [...list.children].map(row => [row.querySelector('dt').textContent.trim(), row.querySelector('dd').textContent.trim()])
        }));
        return {
          pricing: {
            additional: additional?.textContent.trim(),
            additionalSize: additional && parseFloat(getComputedStyle(additional).fontSize),
            additionalColor: additional && getComputedStyle(additional).color,
            initialSize: initial && parseFloat(getComputedStyle(initial).fontSize),
            fees,
            headings: [...document.querySelectorAll('main h2')].map(el => el.textContent.trim()),
            profileParent: document.querySelector('.service-menu-heading:last-of-type')?.closest('article')?.querySelector('h3')?.textContent.trim(),
            supportLink: document.querySelector('#support-pricing > .container > a')?.getAttribute('href'),
            growthExternal: document.querySelector('#growth a[href="https://kuchikomi-stars.com/"]')?.getAttribute('href'),
            firstStoreNote: document.querySelector('#risk .service-fee-note')?.textContent.trim(),
            monitoring: [...document.querySelectorAll('#risk .detail-row')].find(row => row.querySelector('h3')?.textContent === '投稿モニタリング')?.textContent.trim()
          },
          viewport: innerWidth, scrollWidth: document.documentElement.scrollWidth, overflow,
          h1: [...document.querySelectorAll('h1')].map(el => el.textContent.trim()),
          title: document.title, description: document.querySelector('meta[name=description]')?.content,
          canonical: document.querySelector('link[rel=canonical]')?.href,
          ogURL: document.querySelector('meta[property="og:url"]')?.content,
          ogTitle: document.querySelector('meta[property="og:title"]')?.content,
          ogDescription: document.querySelector('meta[property="og:description"]')?.content,
          ogImage: document.querySelector('meta[property="og:image"]')?.content,
          twitter: ['card','title','description','image'].map(name => document.querySelector(`meta[name="twitter:${name}"]`)?.content),
          ga4: [...document.scripts].filter(el => el.src.includes('gtag/js?id=G-8S2N18S2YX')).length,
          ga4Config: [...document.scripts].some(el => el.textContent.includes("gtag('config', 'G-8S2N18S2YX')")),
          forms: document.forms.length, css: [...document.querySelectorAll('link[rel=stylesheet]')].map(el => new URL(el.href).pathname),
          font: getComputedStyle(document.body).fontFamily,
          shortTargets: targets.filter(el => el.getBoundingClientRect().height < 43).map(el => el.textContent.trim()),
          cases: document.querySelectorAll('.case-item').length,
          robots: document.querySelector('meta[name=robots]')?.content || 'index, follow'
        };
      });
      record.route = route || '/';
      record.status = response.status();
      record.errors = errors;
      const checks = {
        http: response.status() === 200,
        width: record.viewport === width && record.scrollWidth <= width && !record.overflow.length,
        heading: record.h1.length === 1,
        metadata: !!record.title && !!record.description && !!record.ogTitle && !!record.ogDescription && record.twitter.every(Boolean),
        canonical: record.canonical === `https://killerword.info/${route}` && record.ogURL === record.canonical,
        ga4: record.ga4 === 1 && record.ga4Config,
        noForm: record.forms === 0,
        style: record.css.includes('/assets/top.css') && !record.css.includes('/assets/site.css') && record.font.includes('Noto Sans JP'),
        targets: !record.shortTargets.length,
        cases: route !== 'cases/' || record.cases === 30,
        errors: !errors.length,
        indexing: route === '404.html' ? record.robots.includes('noindex') : !record.robots.includes('noindex')
      };
      if (route === '' || route === 'pricing/') {
        checks.additionalFee = record.pricing.additional === '規定件数を超える場合：1案件 1,650円（税込）';
        checks.feeHierarchy = record.pricing.additionalSize < record.pricing.initialSize && record.pricing.additionalColor === 'rgb(75, 81, 88)';
      }
      if (route === 'pricing/') {
        const expected = [
          ['媒体・求人コンテンツ制作', '10件 26,000円〜'], ['プロフィール文章作成', '7,000円〜'], ['クチコミスターズ', 'サービス・料金を見る→'],
          ['掲示板対策', '初回100件 8,000円〜'], ['投稿モニタリング', '料金は内容に応じてご案内']
        ];
        checks.supportSummary = JSON.stringify(record.pricing.fees.flatMap(list => list.rows)) === JSON.stringify(expected) && record.pricing.supportLink === '/reputation/';
        const headings = record.pricing.headings;
        const support = headings.indexOf('集客支援・リスク対策の料金');
        checks.supportPosition = support === headings.indexOf('複数店舗・受付量が多い場合') + 1 && support + 1 === headings.indexOf('料金についてのよくある質問');
      }
      if (route === 'reputation/') {
        const expected = [
          { label: '媒体・求人コンテンツ制作の料金', rows: [['10件','26,000円'],['20件','50,000円'],['50件','120,000円'],['100件','230,000円']] },
          { label: 'プロフィール文章作成の料金', rows: [['標準 600〜900字','7,000円'],['ロング 1,200字＋キャッチコピー3本','10,000円']] },
          { label: '掲示板対策の料金', rows: [['初回100件','8,000円'],['300件','27,000円'],['500件','42,000円'],['1,000件','78,000円']] }
        ];
        checks.serviceFees = JSON.stringify(record.pricing.fees) === JSON.stringify(expected);
        checks.serviceStructure = record.pricing.profileParent === '媒体・求人コンテンツ制作' && record.pricing.growthExternal === 'https://kuchikomi-stars.com/' && record.pricing.firstStoreNote === '初回100件は1店舗1回まで' && record.pricing.monitoring.includes('料金は内容に応じてご案内します。') && !/\d+円/.test(record.pricing.monitoring);
      }
      if (width < 1200) {
        const toggle = page.locator('.menu-toggle');
        await toggle.click();
        checks.menuOpen = await toggle.getAttribute('aria-expanded') === 'true' && await page.locator('#site-nav').isVisible();
        await page.keyboard.press('Escape');
        checks.menuEscape = await toggle.getAttribute('aria-expanded') === 'false';
        await toggle.click();
        await page.locator('#site-nav a[href="/pricing/"],#site-nav a[href="pricing/"]').click();
        checks.menuLink = new URL(page.url()).pathname === '/pricing/' && await page.locator('.menu-toggle').getAttribute('aria-expanded') === 'false';
        await page.goto(new URL(route, base).href, { waitUntil: 'networkidle' });
      }
      const buttons = await page.locator('.faq-question').all();
      for (const button of buttons) {
        await button.click();
        const answer = page.locator('#' + await button.getAttribute('aria-controls'));
        checks.faq = checks.faq !== false && await answer.isVisible() && await button.getAttribute('aria-expanded') === 'true';
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), 'FAQ overflow');
        await button.click();
      }
      await page.keyboard.press('Control+Home');
      await page.screenshot({ path: path.join(output, `${route.replaceAll('/','-') || 'top'}-${width}.png`), fullPage: true });
      record.checks = checks;
      record.pass = Object.values(checks).every(Boolean);
      records.push(record);
      if (!record.pass) failures.push(record);
      console.log(`${record.pass ? 'PASS' : 'FAIL'} ${route || '/'} ${width}px ${JSON.stringify(checks)}`);
      page.off('pageerror', onError);
    }
    await context.close();
  }
  const request = await browser.newContext();
  for (const route of [...routes, 'assets/top.css', 'assets/details.css', 'assets/top.js', 'assets/favicon.svg', 'assets/ogp.png', 'robots.txt', 'sitemap.xml']) {
    const response = await request.request.get(new URL(route, base).href);
    responses.push({ route: route || '/', status: response.status() });
    assert.equal(response.status(), 200, `HTTP ${route}`);
  }
  if (process.env.SITE_BASE_URL?.startsWith('https:')) {
    const response = await request.request.get(new URL('missing-page-verification-20261007/', base).href);
    assert.equal(response.status(), 404, 'custom 404 status');
    assert((await response.text()).includes('トップページへ戻る'), 'custom 404 body');
    responses.push({ route: 'missing-page-verification-20261007/', status: response.status() });
  }
  await request.close();
  const noJS = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 390, height: 1000 } });
  const p = await noJS.newPage();
  for (const route of ['', 'pricing/']) {
    await p.goto(new URL(route, base).href);
    assert(await p.locator('.faq-answer').first().isVisible(), 'FAQ without JS');
    assert(await p.locator('.menu-toggle').isVisible(), 'mobile header without JS');
    // Contact action stays visible without JS; full navigation stays available
    // through the common footer, as on the preserved top.
    assert(await p.locator('.header-actions a').isVisible(), 'mobile contact without JS');
  }
  await noJS.close();
} finally {
  await fs.writeFile(path.join(output, 'results.json'), JSON.stringify({ base, checkedAt: new Date().toISOString(), total: records.length, passed: records.filter(r => r.pass).length, failures, responses, records }, null, 2));
  await browser.close();
}
assert.equal(records.length, 45);
assert.equal(failures.length, 0, 'Responsive checks failed');
