'use strict';
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const assert = require('node:assert/strict');
const { chromium } = require(process.env.PW_MODULE || 'playwright');
const root = path.resolve(__dirname, '..');
const output = path.join(root, 'docs/redesign');
fs.mkdirSync(output, { recursive: true });
const routes = ['/', '/contact-center/', '/pricing/', '/reputation/', '/contact/', '/privacy/', '/legal/', '/404.html'];
const widths = [1440, 1024, 768, 390, 360];
const mime = { '.html':'text/html; charset=utf-8', '.css':'text/css', '.js':'text/javascript', '.svg':'image/svg+xml', '.png':'image/png', '.xml':'application/xml', '.txt':'text/plain' };
const server = http.createServer((req, res) => {
  let file = path.resolve(root, '.' + decodeURIComponent(new URL(req.url, 'http://local').pathname));
  if (!file.startsWith(root + path.sep) && file !== root) { res.writeHead(403); return res.end(); }
  let status = 200;
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
  if (!fs.existsSync(file) || !fs.statSync(file).isFile()) { file = path.join(root, '404.html'); status = 404; }
  res.writeHead(status, {'Content-Type': mime[path.extname(file)] || 'application/octet-stream'});
  res.end(fs.readFileSync(file));
});
const tick = page => page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
async function audit(page) {
  return page.evaluate(() => {
    const visible = e => e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden';
    const nodes = [...document.body.querySelectorAll('*')].filter(e => visible(e) && !e.closest('.hero-visual') && !e.matches('.skip-link'));
    const outside = nodes.filter(e => { const r=e.getBoundingClientRect(); return r.width>0 && (r.left < -1 || r.right > innerWidth+1); }).map(e=>({tag:e.tagName,cls:e.className,text:e.textContent.slice(0,60)}));
    const clipped = nodes.filter(e=>e.clientWidth>0 && ['hidden','clip'].includes(getComputedStyle(e).overflowX) && e.scrollWidth>e.clientWidth+1).map(e=>({tag:e.tagName,cls:e.className}));
    const sticky = document.querySelector('.mobile-cta');
    const ctaVisible = sticky && visible(sticky);
    return { width:innerWidth, scrollWidth:document.documentElement.scrollWidth, outside, clipped, h1:document.querySelectorAll('h1').length, css:document.styleSheets.length, js:document.documentElement.classList.contains('js-ready'), ga4:[...document.scripts].filter(s=>s.src.includes('googletagmanager.com/gtag/js?id=G-8S2N18S2YX')).length, canonical:document.querySelector('link[rel=canonical]')?.href, mobileCTA:!!ctaVisible, paddingBottom:parseFloat(getComputedStyle(document.body).paddingBottom), ctaHeight:ctaVisible?sticky.getBoundingClientRect().height:0, images:[...document.images].map(e=>({src:e.getAttribute('src'),loaded:e.complete&&e.naturalWidth>0})), prices:[...document.querySelectorAll('.plan-row')].map(e=>e.innerText), forms:document.querySelectorAll('form').length };
  });
}
async function main() {
  await new Promise(resolve => server.listen(4173, '127.0.0.1', resolve));
  const base = 'http://127.0.0.1:4173';
  const browser = await chromium.launch({ headless:true });
  const context = await browser.newContext({ viewport:{width:1440,height:900}, reducedMotion:'reduce' });
  // Test requests must not inflate the production GA4 property.
  await context.route('**/googletagmanager.com/**', route => route.abort());
  const page = await context.newPage();
  const exceptions=[]; page.on('pageerror', e=>exceptions.push(e.message));
  const results=[];
  for (const width of widths) {
    await page.setViewportSize({width,height:900});
    for (const route of routes) {
      const response=await page.goto(base+route,{waitUntil:'load'}); await tick(page);
      assert.equal(response.status(),200,route);
      const r=await audit(page); r.path=route;
      assert.equal(r.width,width);
      assert.ok(r.scrollWidth<=width+1,JSON.stringify(r));
      assert.deepEqual(r.outside,[],JSON.stringify(r));
      assert.deepEqual(r.clipped,[],JSON.stringify(r));
      assert.equal(r.h1,1); assert.ok(r.css); assert.ok(r.js); assert.equal(r.ga4,1);
      assert.equal(r.canonical,'https://killerword.info'+route);
      assert.ok(r.images.every(e=>e.loaded));
      assert.ok(!r.mobileCTA||r.paddingBottom>=r.ctaHeight);
      if(route==='/'||route==='/pricing/')assert.equal(r.prices.length,3);
      if(width===1440||width===390){
        const name=route==='/'?'home':route.replaceAll('/','').replace('.html','');
        await page.screenshot({path:path.join(output,`${name}-${width}.png`)});
        if(route==='/')await page.screenshot({path:path.join(output,`home-full-${width}.png`),fullPage:true});
      }
      const details=page.locator('details').first();
      if(await details.count()){
        const summary=details.locator('summary');await summary.focus();await summary.press('Enter');
        assert.equal(await details.getAttribute('open'),'');await summary.press('Enter');
        assert.equal(await details.getAttribute('open'),null);r.faqKeyboard=true;
      }
      if(width<1024){
        await page.getByRole('button',{name:'メニューを開く',exact:true}).click();
        assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'),'true');
        assert.equal(await page.locator('#site-nav').isVisible(),true);
        await page.keyboard.press('Escape');assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'),'false');r.menuKeyboard=true;
      }
      if(width<768&&route!=='/contact/'){
        const consult=page.locator('main .button-primary').last();
        if(await consult.count()){
          await consult.scrollIntoViewIfNeeded();await tick(page);
          assert.equal(await page.locator('.mobile-cta').isVisible(),false,'inline CTA must hide sticky CTA');
        }
        await page.evaluate(()=>scrollTo(0,document.body.scrollHeight));await tick(page);
        const bottom=await audit(page);assert.ok(!bottom.mobileCTA||bottom.paddingBottom>=bottom.ctaHeight);r.stickyCTA=true;
      }
      r.pass=true;results.push(r);
      console.log('PASS',width,route);
    }
  }
  // Verify actual route changes through the shared navigation and footer.
  await page.setViewportSize({width:390,height:900});await page.goto(base+'/');await tick(page);
  await page.getByRole('button',{name:'メニューを開く',exact:true}).click();
  await page.locator('#site-nav').getByRole('link',{name:'料金',exact:true}).click();
  assert.equal(new URL(page.url()).pathname,'/pricing/');
  await page.locator('footer').getByRole('link',{name:'導入について相談する',exact:true}).click();
  assert.equal(new URL(page.url()).pathname,'/contact/');
  for(const id of ['store','name','service','message']){
    assert.equal(await page.locator(`label[for=${id}]`).count(),1);
    assert.equal(await page.locator('#'+id).isVisible(),true);
  }
  await page.getByRole('button',{name:'アドレスをコピー',exact:true}).click();
  await page.getByRole('status').filter({hasText:'メールアドレスをコピーしました。'}).waitFor({state:'visible'});
  await page.locator('footer').getByRole('link',{name:'プライバシーポリシー',exact:true}).click();
  assert.equal(new URL(page.url()).pathname,'/privacy/');
  await page.locator('footer').getByRole('link',{name:'運営者情報',exact:true}).click();
  assert.equal(new URL(page.url()).pathname,'/legal/');
  const missing=await page.goto(base+'/missing/route/');assert.equal(missing.status(),404);await tick(page);
  assert.ok((await audit(page)).js,'nested 404 assets must load');
  await page.getByRole('link',{name:'トップページへ',exact:true}).click();assert.equal(new URL(page.url()).pathname,'/');
  const noJS=[];
  const plain=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:900}});
  await plain.route('**/googletagmanager.com/**',route=>route.abort());const plainPage=await plain.newPage();
  for(const route of routes){await plainPage.goto(base+route);assert.ok(await plainPage.locator('#site-nav').isVisible());assert.equal(await plainPage.locator('h1').count(),1);if(route==='/contact/')assert.equal(await plainPage.locator('#contact-form').isVisible(),false);noJS.push({path:route,pass:true})}
  await plain.close();
  // Render the exact brand composition at the required sharing-image size.
  await page.setViewportSize({width:1440,height:900});await page.goto(base+'/docs/ogp-preview.html');
  await page.locator('.image').screenshot({path:path.join(root,'assets/ogp.png')});
  assert.deepEqual(exceptions,[]);
  const report={sourceCommit:process.env.SOURCE_SHA||null,date:new Date().toISOString(),total:results.length,passed:results.filter(r=>r.pass).length,failures:[],results,noJS,routeTransitions:true,nested404:true,emailCopy:true,analyticsRequestsBlockedForTests:true,ogp:{width:1200,height:630}};
  fs.writeFileSync(path.join(output,'results.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({total:report.total,passed:report.passed,noJS:noJS.length,routeTransitions:true,nested404:true,emailCopy:true}));
  await browser.close();server.close();
}
main().catch(e=>{console.error(e);server.close();process.exit(1)});
