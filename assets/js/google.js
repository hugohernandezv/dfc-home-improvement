/* Homepage Google rating pill + reviews slider.
 * Data comes from /api/google (the dfc-api service), which caches DFC's
 * Google Places rating, review count and 5-star reviews. The pill ships with
 * the last known numbers baked in; the slider stays hidden unless live data
 * arrives, so nothing breaks if the API is unavailable. */
(function () {
  var pill = document.querySelector('[data-google-rating]');
  var rail = document.querySelector('[data-review-rail]');
  var track = rail && rail.querySelector('[data-rr-track]');

  var G = '<svg class="rr-g" viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.2-.1-2.3-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-7.9l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.2-.1-2.3-.4-3.5z"/></svg>';

  function esc(t) {
    return String(t).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function card(r) {
    var initial = esc((r.author || '?').trim().charAt(0).toUpperCase());
    var avatar = r.photo
      ? '<img class="rr-avatar" src="' + esc(r.photo) + '" alt="" loading="lazy" referrerpolicy="no-referrer">'
      : '<span class="rr-avatar rr-avatar--letter" aria-hidden="true">' + initial + '</span>';
    return '<article class="rr-card">' +
      '<header class="rr-head">' + avatar +
        '<div class="rr-who"><div class="rr-name">' + esc(r.author) + '</div>' +
        '<div class="rr-when">' + esc(r.when) + '</div></div>' + G +
      '</header>' +
      '<div class="rr-stars" aria-label="5 out of 5 stars">★★★★★</div>' +
      '<p class="rr-text">' + esc(r.text) + '</p>' +
      '<a class="rr-more" href="' + esc(r.link) + '" target="_blank" rel="noopener">Read on Google</a>' +
    '</article>';
  }

  function slider() {
    var prev = rail.querySelector('[data-rr-prev]');
    var next = rail.querySelector('[data-rr-next]');
    function step() {
      var c = track.querySelector('.rr-card');
      return c ? c.getBoundingClientRect().width + 18 : 320;
    }
    function go(dir) {
      var max = track.scrollWidth - track.clientWidth - 2;
      if (dir > 0 && track.scrollLeft >= max) track.scrollTo({ left: 0, behavior: 'smooth' });
      else if (dir < 0 && track.scrollLeft <= 2) track.scrollTo({ left: max, behavior: 'smooth' });
      else track.scrollBy({ left: dir * step(), behavior: 'smooth' });
    }
    prev.addEventListener('click', function () { go(-1); });
    next.addEventListener('click', function () { go(1); });

    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) return;
    var paused = false, timer = setInterval(function () { if (!paused && !document.hidden) go(1); }, 6000);
    ['mouseenter', 'focusin', 'touchstart'].forEach(function (e) {
      rail.addEventListener(e, function () { paused = true; }, { passive: true });
    });
    ['mouseleave', 'focusout'].forEach(function (e) {
      rail.addEventListener(e, function () { paused = false; });
    });
    window.addEventListener('pagehide', function () { clearInterval(timer); });
  }

  fetch('/api/google', { headers: { Accept: 'application/json' } })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (d) {
      if (!d) return;
      if (pill && d.rating && d.count) {
        var rt = pill.querySelector('[data-gr-rating]'), ct = pill.querySelector('[data-gr-count]');
        if (rt) rt.textContent = Number(d.rating).toFixed(1);
        if (ct) ct.textContent = d.count;
        pill.setAttribute('aria-label', 'Rated ' + Number(d.rating).toFixed(1) + ' out of 5 from ' + d.count + ' Google reviews');
      }
      if (rail && track && d.reviews && d.reviews.length) {
        track.innerHTML = d.reviews.map(card).join('');
        rail.hidden = false;
        slider();
      }
    })
    .catch(function () {});
})();
