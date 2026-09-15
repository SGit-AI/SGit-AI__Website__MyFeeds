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

  // Recovered archive images. The generator emits them as <a class="rimg"> rather than
  // <img src>, because a declarative reference to a vault path 404s inside a sandboxed
  // vault frame before the bridge installs. Here we turn each into a real image: through
  // the bridge where one exists, directly otherwise. A failure leaves the link, which is
  // still a working way to see the picture.
  document.querySelectorAll('a.rimg[href]').forEach(function (a) {
    var href = a.getAttribute('href');
    var img = document.createElement('img');
    img.alt = a.getAttribute('data-alt') || '';
    img.loading = 'lazy';
    img.title = a.getAttribute('title') || '';
    img.className = 'rimg-loaded';
    img.addEventListener('error', function () {
      // Put the link back rather than leaving a broken image, which looks identical to
      // one that simply failed once.
      if (img.parentNode) img.parentNode.replaceChild(a, img);
    });
    function swap(src) {
      img.src = src;
      if (a.parentNode) a.parentNode.replaceChild(img, a);
    }
    var sg = window.sg;
    if (sg && typeof sg.objectUrl === 'function') {
      try { return Promise.resolve(sg.objectUrl(href)).then(swap).catch(function () { swap(href); }); }
      catch (e) { /* fall through */ }
    }
    if (sg && sg.vfs && typeof sg.vfs.readBytes === 'function') {
      try {
        return Promise.resolve(sg.vfs.readBytes(href)).then(function (bytes) {
          swap(URL.createObjectURL(new Blob([bytes])));
        }).catch(function () { swap(href); });
      } catch (e) { /* fall through */ }
    }
    swap(href);
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
