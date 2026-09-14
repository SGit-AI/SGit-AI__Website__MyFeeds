/* myfeeds.sgit.ai — progressive enhancement only.
   Contract: this file must never add content. Every page is complete and readable with
   JavaScript disabled; everything below is convenience. */
(function () {
  'use strict';

  // Mark the current page in the nav. Done here rather than in the generator so the
  // shell stays identical across pages and caches as one string.
  try {
    var here = location.pathname.replace(/index\.html$/, '').replace(/\/+$/, '') || '/';
    document.querySelectorAll('.site-nav a[href]').forEach(function (a) {
      var p = new URL(a.getAttribute('href'), location.href).pathname
        .replace(/index\.html$/, '').replace(/\/+$/, '') || '/';
      if (p === here) a.setAttribute('aria-current', 'page');
    });
  } catch (e) { /* nav highlighting is not worth an error */ }

  // Wrap any table that was authored without one, so narrow screens scroll the table
  // instead of the page.
  document.querySelectorAll('main table').forEach(function (t) {
    if (t.parentElement && t.parentElement.classList.contains('tablewrap')) return;
    var w = document.createElement('div');
    w.className = 'tablewrap';
    t.parentNode.insertBefore(w, t);
    w.appendChild(t);
  });

  // Anchor links on headings that carry an id.
  document.querySelectorAll('main h2[id], main h3[id]').forEach(function (h) {
    var a = document.createElement('a');
    a.href = '#' + h.id;
    a.className = 'anchor';
    a.setAttribute('aria-label', 'Link to this section');
    a.textContent = '#';
    a.style.cssText = 'border:0;opacity:0;margin-left:.4rem;font-weight:400;color:var(--dim2)';
    h.appendChild(a);
    h.addEventListener('mouseenter', function () { a.style.opacity = '.6'; });
    h.addEventListener('mouseleave', function () { a.style.opacity = '0'; });
  });
})();
