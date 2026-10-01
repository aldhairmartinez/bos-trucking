# Architecture

How this site is built, and why each decision was made.

---

## 1. The shape of the problem

B.O.S. Trucking & Site is a local service business with two customer decisions:

1. *"Can you deliver me a load of shell?"*
2. *"Can I park my trailer here, and what does it cost?"*

Both decisions end in the same action: **tapping 239-900-6374.** Most visitors will
arrive on a phone, from a Google search or a Facebook post, already half-decided.

That shapes everything. The site's job is to establish that B.O.S. is a real, permanent
operation with real trucks and a real yard, state the parking rates plainly, and put the
phone number within one tap from any scroll position. It is not a catalogue, not a
storefront, and not an app.

---

## 2. Stack

**Plain static HTML, CSS and vanilla JavaScript. No framework, no bundler, no build step
for markup.**

| Layer | Choice | Size |
|---|---|---|
| Markup | 7 hand-written HTML files | 11–54 KB each |
| Styles | 5 stylesheets, CSS custom properties | ~51 KB |
| Behaviour | 3 vanilla JS files | ~16 KB |
| Fonts | 4 self-hosted WOFF2 latin subsets | 78 KB |
| Images | AVIF → WebP → JPEG at 4 widths | one size fetched per slot |
| Image pipeline | Python 3 + Pillow (offline, dev only) | — |
| Dev server | Python standard library | — |

Total shell per page: **~150–197 KB**, and the site is fully functional with JavaScript
disabled.

### Why not a framework

Astro or Eleventy would save duplicating a header across seven files. In exchange they add
a build step, a `node_modules` tree, a lockfile, and dependency upkeep on a brochure site
that may be handed to someone else, or rebuilt by hand inside Wix within a week. The
duplication is the cheaper cost. React would be strictly worse: hydration JS for a page
whose main interaction is an `<a href="tel:">`.

The property that matters most here is **"open the folder and it works."**

### Why Python for the tooling

Pillow 12 encodes AVIF, WebP and JPEG natively, and Python 3 ships with macOS. So the
image pipeline, the dev server and the QA checker need **zero npm dependencies**.
`package.json` declares no dependencies at all — `npm` is only a familiar name for the
tasks.

---

## 3. Directory layout

```
assets/        SOURCE. Committed, never served.
  sources.json   the manifest — single source of truth for every image
  originals/     the 12 supplied files, byte-for-byte untouched
  masters/       lossless crops (generated)
  brand/         logo art with the black plate keyed out (generated)
  reference/     marketing flyers, for reference only (generated)

public/        THE WEBSITE. Serve this directory.
  *.html         7 pages
  css/           tokens · base · layout · components · image-focus (generated)
  js/            site · gallery · quote-form
  img/           responsive derivatives (generated)
  fonts/         4 WOFF2 subsets
  robots.txt · sitemap.xml · site.webmanifest · favicons

scripts/       TOOLING. Never served.
  crop-source.py   stage 1 — originals → lossless masters
  build-images.py  stage 2 — masters → responsive derivatives
  serve.py         local preview
  check.py         quality gate
```

The split is deliberate: `assets/` is what the owner gave us plus lossless intermediates,
`public/` is what a browser downloads. Nothing in `assets/` is ever reachable over HTTP.

---

## 4. The image pipeline

This is the most consequential part of the architecture, because **every supplied image
is temporary**. All twelve are 1290×2796 iPhone screenshots whose real content is a band
in the middle, several with burned-in marketing overlays. The owner's real originals are
expected later, and the design must not care.

```
assets/originals/           read-only, never modified
        │
        │  assets/sources.json  ← crop box, focal point, alt text, group
        ▼
scripts/crop-source.py      strip letterbox bars + flyer overlays, lossless
        │
        ├──▶ assets/masters/    photographic masters (PNG, lossless)
        ├──▶ assets/brand/      logos, black plate keyed to transparent
        └──▶ assets/reference/  flyers, reference only
        │
        ▼
scripts/build-images.py     resize + encode, NEVER upscales
        │
        ├──▶ public/img/**              AVIF + WebP + JPEG at 480/640/960/1280
        ├──▶ public/img/og/og-card.jpg  composed 1200×630 share card
        ├──▶ public/favicon-*.png       cut from the real badge logo
        └──▶ public/css/image-focus.css generated object-position rules
```

### Three properties make the swap trivial

**1. Stable logical IDs.** The HTML references
`/img/trucks/bos-mack-dump-truck-960.avif` — a name derived from the manifest key, not
from `IMG_0653.PNG`. Change the source file behind the key and every reference still
resolves.

**2. Never upscale.** `build-images.py` caps output width at the master's real width, so
today's ladder stops at 1280. The markup already asks for 1600 / 1920 / 2560 via
`srcset`; those rungs simply appear once a bigger source exists. No markup edit.

It also drops the source's own width as a top rung when it is within 5% of the highest
standard rung — a 1290 variant sitting next to 1280 buys nothing and costs a fifth of the
payload.

**3. Framing lives in the manifest, not the stylesheets.** Photos are served at their
natural cropped aspect ratio; containers set `aspect-ratio` and crop with
`object-fit: cover`. Each photo's focal point travels from `sources.json` into the
generated `public/css/image-focus.css` as an `object-position` rule.

> An earlier revision pre-cropped each photo to each container's aspect ratio in the
> pipeline. That discarded up to **45% of the pixel width** of sources that cannot spare
> it — the 2.74:1 sunset panorama became 705 px wide to fill a 3:2 card. Serving the
> natural aspect and cropping in CSS keeps every available pixel.

### Art direction

The hero uses two different photographs, because the wide sunset panorama (2.74:1) cannot
crop to a portrait phone screen:

- **≥768 px** — the sunset lot panorama, framed on the gate sign and the sleeper cab
- **<768 px** — the branded Mack tri-axle dump truck, portrait, framed on the cab

Handled with `<source media>` inside `<picture>`. Hero framing is therefore set per
breakpoint in `layout.css` rather than from one image's focal point.

---

## 5. CSS architecture

Four hand-written stylesheets plus one generated, loaded in cascade order:

| File | Role |
|---|---|
| `tokens.css` | Every colour, type size, space step, timing. The only place brand values are declared. |
| `base.css` | Reset, `@font-face`, element typography, focus, layout utilities, motion. |
| `layout.css` | Utility bar, header, nav, drawer, hero, footer, mobile action bar. |
| `components.css` | Buttons, cards, materials, pricing, gallery, lightbox, contact, forms. |
| `image-focus.css` | **Generated.** `object-position` per photo, from `sources.json`. |

No preprocessor, no utility framework, no CSS-in-JS. Custom properties cover the only
thing a preprocessor was needed for.

### Two bugs worth recording

**Grid `1fr` blowout.** `1fr` is shorthand for `minmax(auto, 1fr)`, so a track can never
shrink below its content's min-content width — it blows out past the container instead.
The pricing grid overflowed the viewport by 49 px at 620 px wide, because `$200` and
`/ MONTH` on one non-wrapping flex line gave each card a 210 px floor. Every fixed-count
grid now uses `minmax(0, 1fr)`, the price amount is allowed to wrap, and the three-up
breakpoint moved to 760 px — the width at which the cards genuinely fit.

**`<picture>` breaks percentage heights.** A `<picture>` is a format-selection wrapper,
but it still generates a box. At its default auto height, `height: 100%` on the `<img>`
inside resolves against *it*, not the real container — so cover images letterbox instead
of cropping. Service-card photos silently rendered with black bands. `base.css` now
stretches `<picture>` inside every `object-fit` container, with a comment listing them;
**add new object-fit containers to that list.**

Both were caught by measuring real rendered geometry in a browser, not by reading CSS.

---

## 6. JavaScript

Three files, all progressive enhancement. The site works without any of them.

**`site.js`** — drawer (focus trap, Escape, restores focus, closes on resize to
desktop), sticky-header state via `IntersectionObserver` on a sentinel, section reveal
(fires once, `unobserve`d, skipped entirely under `prefers-reduced-motion`), active-section
nav highlight, footer year.

**`gallery.js`** — lightbox. Tiles are real `<button>`s, so the gallery is keyboard
operable before this file loads. Focus trap, Escape, arrow-key paging, backdrop click,
focus restored to the opening tile.

**`quote-form.js`** — mode switch between Material Delivery and Truck Parking. Hidden
field sets get `disabled` as well as `hidden`, so their values never submit and they
leave the tab order. Mode is reflected in the URL (`?type=parking`) so "Check
Availability" deep-links straight into the parking fields. Validation uses native
constraint validation; the script only supplies readable messages, sets `aria-invalid`,
and moves focus to the first problem.

### Forms are honest about not being wired

No submission backend exists yet. Rather than appear to send and silently drop a real
customer's enquiry, submitting shows:

> **Preview mode.** Online form delivery is not connected yet. To reach B.O.S. right now,
> call or text 239-900-6374 or email bostruckingsite@gmail.com.

Wiring options in [`forms.md`](forms.md).

---

## 7. Accessibility

Built in, not retrofitted. Semantic landmarks, one `<h1>` per page, no skipped heading
levels, skip-to-content link, full keyboard operation, `:focus-visible` rings that are
never removed, real `<label for>` on every field, errors announced rather than coloured,
`prefers-reduced-motion` honoured, ≥44 px tap targets, descriptive alt text with `alt=""`
on decorative images, `aria-hidden` on icon SVGs paired with real text.

Contrast is measured, not estimated — every pair in [`design-system.md`](design-system.md)
clears WCAG AA, and the primary pairs run 9.6:1 to 19.8:1.

---

## 8. Quality gate

`scripts/check.py` runs ten check families over every page: asset existence, internal and
anchor links, image `alt` / `width` / `height` / loading strategy, heading structure,
form labelling, phone and email consistency (including `tel:`/`sms:` E.164 format), SEO
head tags and JSON-LD validity, accessibility invariants, hygiene markers, and payload
reporting.

It also enforces two project-specific rules:

- **No fabricated credibility in structured data.** `aggregateRating`, `review` and
  `openingHours` are rejected outright — we have no verified reviews or hours.
- **One phone number, one email.** Any other US-format number or address anywhere on a
  page is an error, which is how the placeholder `239-000-0000` got caught and removed.

Overflow is verified separately by driving headless Chrome over 7 pages × 27 viewport
widths (320–2560 px) and comparing `scrollWidth` to `clientWidth`. Current result: **189
checks, zero real overflow.**

Run `npm run check` before every commit.

---

## 9. Production

**Likely: GitHub → Cloudflare Pages → custom domain.** `public/` is already a valid
Pages site: no build command, output directory `public`. `serve.py` deliberately mimics
Pages' clean-URL and 404 behaviour so local review matches production.

**Alternative: rebuild by hand in the owner's classic Wix Editor**, using this site as
the design specification. Our HTML/CSS cannot be deployed *into* a classic Editor site;
see [`wix-setup.md`](wix-setup.md) for why, and [`deployment.md`](deployment.md) for both
paths costed.

Nothing is deployed and nothing is pushed.
