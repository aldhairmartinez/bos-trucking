/* ==========================================================================
   GALLERY LIGHTBOX
   --------------------------------------------------------------------------
   Each gallery tile is a real <button>, so the gallery is fully keyboard
   operable before this file loads. The lightbox traps focus, closes on Escape
   or backdrop click, supports arrow-key paging, and restores focus to the tile
   that opened it.
   ========================================================================== */
(function () {
  "use strict";

  const gallery = document.querySelector("[data-gallery]");
  const box = document.querySelector("[data-lightbox]");
  if (!gallery || !box) return;

  const items = Array.from(gallery.querySelectorAll("[data-lightbox-src]"));
  if (!items.length) return;

  const img = box.querySelector("[data-lightbox-img]");
  const caption = box.querySelector("[data-lightbox-caption]");
  const counter = box.querySelector("[data-lightbox-counter]");
  const closeBtn = box.querySelector("[data-lightbox-close]");
  const prevBtn = box.querySelector("[data-lightbox-prev]");
  const nextBtn = box.querySelector("[data-lightbox-next]");

  let index = 0;
  let opener = null;

  function render(i) {
    index = (i + items.length) % items.length;
    const tile = items[index];
    img.src = tile.dataset.lightboxSrc;
    img.alt = tile.dataset.lightboxAlt || "";
    caption.textContent = tile.dataset.lightboxAlt || "";
    counter.textContent = `${index + 1} / ${items.length}`;
  }

  function open(i, trigger) {
    opener = trigger || document.activeElement;
    render(i);
    box.classList.add("is-open");
    box.removeAttribute("aria-hidden");
    document.body.classList.add("nav-open"); // reuse the scroll lock
    closeBtn.focus();
  }

  function close() {
    box.classList.remove("is-open");
    box.setAttribute("aria-hidden", "true");
    document.body.classList.remove("nav-open");
    img.src = "";
    if (opener) opener.focus();
  }

  items.forEach((tile, i) =>
    tile.addEventListener("click", () => open(i, tile))
  );

  closeBtn.addEventListener("click", close);
  prevBtn.addEventListener("click", () => render(index - 1));
  nextBtn.addEventListener("click", () => render(index + 1));

  // Clicking the backdrop (but not the image) closes.
  box.addEventListener("click", (e) => {
    if (e.target === box) close();
  });

  document.addEventListener("keydown", (e) => {
    if (!box.classList.contains("is-open")) return;

    switch (e.key) {
      case "Escape":
        e.preventDefault();
        close();
        break;
      case "ArrowLeft":
        e.preventDefault();
        render(index - 1);
        break;
      case "ArrowRight":
        e.preventDefault();
        render(index + 1);
        break;
      case "Tab": {
        const focusable = [closeBtn, prevBtn, nextBtn];
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
        break;
      }
      default:
        break;
    }
  });
})();
