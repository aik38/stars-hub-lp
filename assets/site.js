'use strict';
(() => {
  const header = document.querySelector('.site-header');
  const button = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#site-nav');
  if (!header || !button || !nav) return;
  document.documentElement.classList.add('js-ready');
  const closeMenu = (returnFocus = false) => {
    header.classList.remove('menu-open');
    button.setAttribute('aria-expanded', 'false');
    button.setAttribute('aria-label', 'メニューを開く');
    if (returnFocus) button.focus();
  };
  button.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') !== 'true';
    header.classList.toggle('menu-open', open);
    button.setAttribute('aria-expanded', String(open));
    button.setAttribute('aria-label', open ? 'メニューを閉じる' : 'メニューを開く');
  });
  nav.addEventListener('click', (event) => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && header.classList.contains('menu-open')) closeMenu(true);
  });
  document.addEventListener('click', (event) => {
    if (!header.contains(event.target)) closeMenu();
  });
  header.addEventListener('focusout', (event) => {
    if (!header.contains(event.relatedTarget)) closeMenu();
  });
  const desktop = window.matchMedia('(min-width: 1024px)');
  desktop.addEventListener('change', () => closeMenu());
})();
