'use strict';
(() => {
  const header = document.querySelector('.site-header');
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#site-nav');
  const sticky = document.querySelector('.mobile-cta');
  const narrow = window.matchMedia('(max-width: 767px)');
  const compact = window.matchMedia('(max-width: 1023px)');
  document.documentElement.classList.add('js-ready');
  const visibleCTAs = new Set();
  const updateSticky = () => {
    if (!sticky) return;
    sticky.hidden = !narrow.matches || visibleCTAs.size > 0 || header.classList.contains('menu-open');
    document.body.classList.toggle('has-mobile-cta', narrow.matches);
  };
  const closeMenu = (returnFocus = false) => {
    header.classList.remove('menu-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'メニューを開く');
    if (returnFocus) toggle.focus();
    updateSticky();
  };
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    header.classList.toggle('menu-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'メニューを閉じる' : 'メニューを開く');
    updateSticky();
  });
  nav.addEventListener('click', (event) => { if (event.target.closest('a')) closeMenu(); });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && header.classList.contains('menu-open')) closeMenu(true);
  });
  document.addEventListener('click', (event) => { if (!header.contains(event.target)) closeMenu(); });
  header.addEventListener('focusout', (event) => { if (!header.contains(event.relatedTarget)) closeMenu(); });
  compact.addEventListener('change', () => closeMenu());
  narrow.addEventListener('change', updateSticky);
  if (sticky && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) visibleCTAs.add(entry.target);
        else visibleCTAs.delete(entry.target);
      });
      updateSticky();
    }, { threshold: 0, rootMargin: '-82px 0px 0px 0px' });
    document.querySelectorAll('main .button-primary').forEach((a) => observer.observe(a));
  }
  updateSticky();
  const form = document.querySelector('#contact-form');
  if (form) form.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const body = [
      `店舗名・会社名：${data.get('store') || ''}`,
      `ご担当者名：${data.get('name') || ''}`,
      `希望するサービス：${data.get('service') || ''}`,
      '', 'ご相談内容：', data.get('message') || '',
    ].join('\r\n');
    // No network submission, storage, or personal-data analytics events.
    window.location.href = 'mailto:m-asakura@killerword.info?subject=' + encodeURIComponent('STARS HUB 導入・サービスのご相談') + '&body=' + encodeURIComponent(body);
  });
  const copy = document.querySelector('[data-copy-email]');
  if (copy) copy.addEventListener('click', async () => {
    const status = document.querySelector('.copy-status');
    try {
      await navigator.clipboard.writeText(copy.dataset.copyEmail);
      status.textContent = 'メールアドレスをコピーしました。';
    } catch (_) {
      status.textContent = '上のメールアドレスを選択してコピーしてください。';
    }
  });
})();
