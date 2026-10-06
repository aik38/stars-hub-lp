'use strict';
(() => {
  const header = document.querySelector('.site-header');
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#site-nav');
  if (header && toggle && nav) {
    const closeMenu = (returnFocus = false) => {
      header.classList.remove('menu-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'メニューを開く');
      if (returnFocus) toggle.focus();
    };
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      header.classList.toggle('menu-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'メニューを閉じる' : 'メニューを開く');
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
    window.matchMedia('(min-width: 1200px)').addEventListener('change', () => closeMenu());
    const setScrolled = () => header.classList.toggle('is-scrolled', window.scrollY > 8);
    window.addEventListener('scroll', setScrolled, {passive: true});
    setScrolled();
  }
  document.querySelectorAll('.faq-question').forEach((button) => {
    const answer = document.getElementById(button.getAttribute('aria-controls'));
    const symbol = button.querySelector('.faq-symbol');
    if (!answer || !symbol) return;
    // Answers remain readable when JavaScript is unavailable.
    button.setAttribute('aria-expanded', 'false');
    answer.hidden = true;
    symbol.textContent = '+';
    button.addEventListener('click', () => {
      const open = button.getAttribute('aria-expanded') !== 'true';
      button.setAttribute('aria-expanded', String(open));
      answer.hidden = !open;
      symbol.textContent = open ? '−' : '+';
    });
  });
})();
