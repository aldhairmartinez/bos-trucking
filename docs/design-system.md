# Design System

Every value here is declared once in [`public/css/tokens.css`](../public/css/tokens.css).
Change it there and it propagates everywhere.

---

## Palette

The brand yellow is **sampled from the supplied logo artwork**
(`assets/originals/IMG_0662.PNG`), not guessed. The marketing flyers drift between
`#E8B004` and `#FCD014`; the logo is treated as the authority.

| Token | Hex | Role |
|---|---|---|
| `--bos-black` | `#0A0A0A` | Page background |
| `--bos-black-pure` | `#000000` | Logo plate, footer floor |
| `--bos-surface-1` | `#141414` | Cards, panels |
| `--bos-surface-2` | `#1C1C1C` | Inputs, raised rows |
| `--bos-surface-3` | `#232323` | Hover on raised rows |
| `--bos-hairline` | `#2A2A2A` | Dividers, card borders |
| `--bos-hairline-strong` | `#3A3A3A` | Stronger borders, toggles |
| **`--bos-yellow`** | **`#F8B804`** | **Primary accent — from the logo** |
| `--bos-yellow-bright` | `#FFC933` | Hover, focus ring |
| `--bos-yellow-deep` | `#C98A00` | Pressed, disclaimer edge |
| `--bos-yellow-ink` | `#8A6200` | Yellow-family text on white (print/email) |
| `--bos-white` | `#FFFFFF` | Headings |
| `--bos-text` | `#F5F5F4` | Body |
| `--bos-text-muted` | `#B5B5B0` | Secondary, captions |
| `--bos-text-faint` | `#8A8A86` | Fine print |
| `--bos-on-yellow` | `#0A0A0A` | Text on yellow |

### Measured contrast

Computed with the WCAG 2.1 relative-luminance formula, not estimated.

| Pair | Ratio | Level |
|---|---|---|
| `--bos-white` on `--bos-black` | **19.80:1** | AAA |
| `--bos-text` on `--bos-black` | **18.15:1** | AAA |
| `--bos-yellow-bright` on `--bos-black` | **12.87:1** | AAA |
| `--bos-yellow` on `--bos-black` | **11.17:1** | AAA |
| `--bos-on-yellow` on `--bos-yellow` *(primary button)* | **11.17:1** | AAA |
| `--bos-yellow` on `--bos-surface-1` | **10.21:1** | AAA |
| `--bos-text-muted` on `--bos-black` | **9.62:1** | AAA |
| `--bos-text-faint` on `--bos-black` | **5.71:1** | AA |
| `--bos-yellow-ink` on white | **5.49:1** | AA |

Every pair used on the site clears AA. The primary UI pairs clear AAA.

### The yellow discipline

Yellow is reserved for:

- **one** primary action per viewport
- section eyebrow labels and the 56×3 rule beneath a heading
- icon strokes
- the three price figures
- card hover edges and focus rings
- the one full-bleed call/text callout band

Headings stay white. Body stays off-white. Cards stay charcoal. The point is for yellow
to read as scarce and deliberate rather than decorative.

**Deliberately avoided:** diagonal stripe backgrounds, diamond-plate or metal textures,
distressed grunge overlays, drop-shadowed outlined display type, neon glow, tyre-tread
dividers. Those are what make the source flyers read as flyers.

---

## Typography

| Role | Face | Spec |
|---|---|---|
| Display / H1–H2 | **Barlow Condensed 700** | UPPERCASE, `letter-spacing: .005em`, `line-height: .94` |
| Section eyebrow | Barlow Condensed 600 | UPPERCASE, 13px, `letter-spacing: .14em`, yellow |
| Subhead / H3 | Barlow Condensed 700 | UPPERCASE, `line-height: 1.15` |
| Card subhead / H4 | **Inter 600** | Sentence case |
| Body / UI | **Inter 400 / 600** | 17px, `line-height: 1.65`, `max-width: 68ch` |
| Prices | Barlow Condensed 700 | `font-variant-numeric: tabular-nums` |

Barlow Condensed is the closest open-source match to the logo's heavy squarish condensed
sans while staying modern rather than monster-truck. Inter carries the body because it is
the most legible small-text face on dark backgrounds.

Both are **self-hosted WOFF2 latin subsets** — four faces, 78 KB total, no Google Fonts
CDN request. The two most critical are preloaded.

Sizes are fluid via `clamp()`, so there are no typography breakpoints:

```css
--fs-h1:    clamp(2.625rem, 6.4vw + 1rem, 5.25rem);
--fs-h2:    clamp(2rem,     3.4vw + 1rem, 3.25rem);
--fs-h3:    clamp(1.375rem, 1.2vw + 1.1rem, 1.75rem);
--fs-price: clamp(2.5rem,   3.4vw + 1.6rem, 3.5rem);
```

> **To verify in Wix:** whether Barlow Condensed and Inter are in the Wix font picker,
> and whether custom font upload is premium-gated. If unavailable, substitute from Wix's
> library and record the swap here.

---

## Space, shape, motion

4px base scale, `--s-1` (4px) through `--s-10` (128px).
Section rhythm: `--section-y: clamp(3.5rem, 7vw, 8rem)`.
Gutter: `clamp(1.25rem, 4vw, 3rem)`. Container: 1200px. Measure: 68ch.

Radii are nearly square — 2–4px — because the brand is industrial. The one shape flourish
is `--clip-corner: 10px`, a clipped bottom-right corner on price cards echoing the logo
hexagon.

Motion budget, deliberately small:

- section fade-up on entry: 320ms, 12px, **fires once**, then `unobserve`d
- button / card / link hover transitions: 120–180ms
- lightbox open/close

Nothing else animates on scroll. `prefers-reduced-motion: reduce` disables all of it.

---

## Components

| Component | Notes |
|---|---|
| `.btn--primary` | Black on brand yellow. The signature CTA, 11.17:1. |
| `.btn--secondary` | Yellow-edged outline on a dark scrim, for use over photography. |
| `.btn--ghost` | Quietest option; hairline border that turns yellow on hover. |
| `.btn--phone` | Shows the number itself, stacked under a small "Call or Text" label. The number *is* the call to action. |
| `.service-card` | Photo at 3:2, charcoal body, 4px yellow edge sliding in on hover. |
| `.material` | Chip with a 3px yellow left edge. Ten materials, no invented descriptions. |
| `.price-card` | Yellow top rule, clipped corner, tabular numerals, yellow price. |
| `.disclaimer` | Deep-yellow left edge + info icon. Carries the owner's verbatim wording. |
| `.gallery` | 2-col on phones; 6-col editorial grid from 760px. Tiles are real `<button>`s. |
| `.contact-card` | Oversized tap target. On a phone these are the most important elements on the site. |
| `.callout` | The one inverted band — black on yellow — for the call/text prompt. |
| `.action-bar` | Fixed bottom Call / Text / Quote. Call is primary and shows the full number. |

### Focus

```css
--ring: 3px solid var(--bos-yellow-bright);   /* 12.87:1 on black */
--ring-offset: 2px;
```

Applied via `:focus-visible` on every interactive element. `outline: none` appears exactly
once, on `:focus`, immediately paired with the `:focus-visible` replacement —
`scripts/check.py` fails the build if that pairing is ever broken.

---

## Two CSS traps worth remembering

**Grid `1fr` blowout.** `1fr` means `minmax(auto, 1fr)`, so a track can never shrink below
its content's min-content width — it overflows the container instead. The pricing grid
pushed the page 49px wider than a 620px viewport. Every fixed-count grid now uses
`minmax(0, 1fr)`.

**`<picture>` breaks percentage heights.** A `<picture>` still generates a box, and at auto
height `height: 100%` on the `<img>` resolves against *it*, so cover images letterbox
instead of cropping. `base.css` stretches `<picture>` inside every `object-fit` container
and lists them in a comment — **add new object-fit containers to that list.**
