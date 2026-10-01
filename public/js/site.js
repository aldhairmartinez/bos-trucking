/* ==========================================================================
   SITE — mobile drawer, sticky header state, section reveal, nav highlight
   --------------------------------------------------------------------------
   Progressive enhancement only. With JS disabled the site is fully usable:
   the drawer is replaced by in-page anchors that still work, every section is
   visible, and Call / Text / Quote are plain links.
   ========================================================================== */
(function () {
  "use strict";

  document.documentElement.classList.remove("no-js");

  /* ---- Mobile drawer ---------------------------------------------------- */
  const toggle = document.querySelector("[data-nav-toggle]");
  const drawer = document.querySelector("[data-mobile-nav]");
  const closeBtn = document.querySelector("[data-nav-close]");

  if (toggle && drawer) {
    const FOCUSABLE =
      'a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])';
    let lastFocused = null;

    const open = () => {
      lastFocused = document.activeElement;
      drawer.classList.add("is-open");
      drawer.removeAttribute("aria-hidden");
      toggle.setAttribute("aria-expanded", "true");
      document.body.classList.add("nav-open");
      const first = drawer.querySelector(FOCUSABLE);
      if (first) first.focus();
    };

    const close = () => {
      drawer.classList.remove("is-open");
      drawer.setAttribute("aria-hidden", "true");
      toggle.setAttribute("aria-expanded", "false");
      document.body.classList.remove("nav-open");
      if (lastFocused) lastFocused.focus();
    };

    toggle.addEventListener("click", () =>
      drawer.classList.contains("is-open") ? close() : open()
    );
    if (closeBtn) closeBtn.addEventListener("click", close);

    // Tapping a drawer link navigates and closes.
    drawer.querySelectorAll("a[href]").forEach((a) =>
      a.addEventListener("click", close)
    );

    document.addEventListener("keydown", (e) => {
      if (!drawer.classList.contains("is-open")) return;

      if (e.key === "Escape") {
        e.preventDefault();
        close();
        return;
      }

      // Trap focus inside the drawer while it is open.
      if (e.key === "Tab") {
        const items = Array.from(drawer.querySelectorAll(FOCUSABLE)).filter(
          (el) => el.offsetParent !== null
        );
        if (!items.length) return;
        const first = items[0];
        const last = items[items.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    });

    // A resize into the desktop breakpoint should not leave the drawer open.
    const desktop = window.matchMedia("(min-width: 900px)");
    desktop.addEventListener("change", (e) => {
      if (e.matches && drawer.classList.contains("is-open")) close();
    });
  }

  /* ---- Sticky header state --------------------------------------------- */
  const header = document.querySelector(".site-header");
  if (header) {
    const sentinel = document.createElement("div");
    sentinel.setAttribute("aria-hidden", "true");
    sentinel.style.cssText = "position:absolute;top:0;height:1px;width:1px;";
    document.body.prepend(sentinel);

    if ("IntersectionObserver" in window) {
      new IntersectionObserver(
        ([entry]) => header.classList.toggle("is-stuck", !entry.isIntersecting),
        { threshold: 0 }
      ).observe(sentinel);
    }
  }

  /* ---- Section reveal --------------------------------------------------- */
  const reveals = document.querySelectorAll(".reveal");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (!reveals.length) {
    // nothing to do
  } else if (reduceMotion || !("IntersectionObserver" in window)) {
    reveals.forEach((el) => el.classList.add("is-visible"));
  } else {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target); // fires once, never re-animates
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.06 }
    );
    reveals.forEach((el) => io.observe(el));
  }

  /* ---- Active section in the desktop nav -------------------------------- */
  const sectionLinks = Array.from(
    document.querySelectorAll('.nav__link[href^="#"], .nav__link[href*="#"]')
  ).filter((a) => a.hash);

  if (sectionLinks.length && "IntersectionObserver" in window) {
    const byId = new Map();
    sectionLinks.forEach((a) => {
      const el = document.getElementById(a.hash.slice(1));
      if (el) byId.set(el, a);
    });

    if (byId.size) {
      const visible = new Set();
      const paint = () => {
        sectionLinks.forEach((a) => a.classList.remove("is-active"));
        // Highest section currently in the viewport wins.
        const top = Array.from(visible).sort(
          (a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top
        )[0];
        if (top && byId.get(top)) byId.get(top).classList.add("is-active");
      };

      const io = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) visible.add(entry.target);
            else visible.delete(entry.target);
          });
          paint();
        },
        { rootMargin: "-45% 0px -50% 0px" }
      );
      byId.forEach((_link, el) => io.observe(el));
    }
  }

  /* ---- Current year in the footer --------------------------------------- */
  document.querySelectorAll("[data-year]").forEach((el) => {
    el.textContent = String(new Date().getFullYear());
  });
})();
