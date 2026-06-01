/* DFC Home Improvement — site interactions */
(function () {
  "use strict";
  var doc = document;

  /* ---------- header shrink on scroll ---------- */
  var header = doc.getElementById("siteHeader");
  function onScroll() {
    if (!header) return;
    header.classList.toggle("scrolled", window.scrollY > 24);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- mobile menu ---------- */
  var toggle = doc.getElementById("navToggle");
  var menu = doc.getElementById("mobileMenu");
  function setMenu(open) {
    if (!menu || !toggle) return;
    menu.classList.toggle("open", open);
    toggle.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    menu.setAttribute("aria-hidden", open ? "false" : "true");
    doc.body.classList.toggle("menu-open", open);
  }
  if (toggle) {
    toggle.addEventListener("click", function () {
      setMenu(!menu.classList.contains("open"));
    });
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { setMenu(false); });
    });
    doc.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setMenu(false);
    });
  }

  /* ---------- scroll reveal ---------- */
  var reveals = [].slice.call(doc.querySelectorAll(".reveal"));
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add("in");
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ---------- portfolio filter ---------- */
  var filters = doc.getElementById("filters");
  var gallery = doc.getElementById("gallery");
  if (filters && gallery) {
    var figs = [].slice.call(gallery.querySelectorAll("figure"));
    filters.addEventListener("click", function (e) {
      var btn = e.target.closest("button");
      if (!btn) return;
      var f = btn.getAttribute("data-filter");
      filters.querySelectorAll("button").forEach(function (b) {
        b.classList.toggle("active", b === btn);
      });
      figs.forEach(function (fig) {
        var show = f === "all" || fig.getAttribute("data-category") === f;
        fig.classList.toggle("is-hidden", !show);
      });
      // bigger, nicer presentation when a single category is selected
      gallery.classList.toggle("filtered", f !== "all");
    });
  }

  /* ---------- lightbox ---------- */
  var lb = doc.getElementById("lightbox");
  if (lb && gallery) {
    var lbImg = doc.getElementById("lbImg");
    var lbCap = doc.getElementById("lbCap");
    var current = -1;
    function visibleFigs() {
      return [].slice.call(gallery.querySelectorAll("figure")).filter(function (f) {
        return !f.classList.contains("is-hidden");
      });
    }
    function show(i) {
      var list = visibleFigs();
      if (!list.length) return;
      current = (i + list.length) % list.length;
      var fig = list[current];
      lbImg.src = fig.getAttribute("data-full");
      lbImg.alt = fig.getAttribute("data-proj") + " — " + fig.getAttribute("data-cat");
      lbCap.textContent = fig.getAttribute("data-proj") + " · " + fig.getAttribute("data-cat");
    }
    function open(i) { show(i); lb.classList.add("open"); lb.setAttribute("aria-hidden", "false"); doc.body.classList.add("menu-open"); }
    function close() { lb.classList.remove("open"); lb.setAttribute("aria-hidden", "true"); doc.body.classList.remove("menu-open"); }
    gallery.addEventListener("click", function (e) {
      var fig = e.target.closest("figure");
      if (!fig) return;
      var list = visibleFigs();
      open(list.indexOf(fig));
    });
    doc.getElementById("lbClose").addEventListener("click", close);
    doc.getElementById("lbNext").addEventListener("click", function () { show(current + 1); });
    doc.getElementById("lbPrev").addEventListener("click", function () { show(current - 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    doc.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") close();
      else if (e.key === "ArrowRight") show(current + 1);
      else if (e.key === "ArrowLeft") show(current - 1);
    });
  }

  /* ---------- contact form (graceful, no backend) ---------- */
  var form = doc.getElementById("leadForm");
  if (form && form.getAttribute("action").indexOf("your-form-id") !== -1) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var note = form.querySelector(".form-note");
      if (note) {
        note.innerHTML = "Thank you — to enable automatic delivery, connect this form to a service " +
          "(e.g. Formspree) or your CRM. For now, please call <a href='tel:+13012379555'>(301) 237-9555</a>.";
      }
    });
  }
})();
