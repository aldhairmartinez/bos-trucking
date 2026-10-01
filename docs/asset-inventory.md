# Asset Inventory

Audit of all twelve supplied files, and exactly where each one is used.

---

## The headline finding

**Every supplied file is a 1290×2796 iPhone screenshot, not an original photo.** The real
image content is a band in the middle, framed by black letterbox bars, and several have
burned-in marketing overlays. After cropping, the usable content is:

| | Usable after cropping |
|---|---|
| Sunset lot panorama | 1290 × 470 (the rest is flyer overlay) |
| Mack dump truck | 1290 × 764 |
| Yard sign / parking gate | 1290 × 968 |
| Logo badge | 1057 × 976, **raster only — no vector** |

The site is built to look right at this resolution, and to **stop caring the moment real
originals arrive**. See [`swapping-images.md`](swapping-images.md).

**Ask the owner for:** the original camera files (AirDrop or an iCloud link, not
screenshots), and the logo as SVG / AI / EPS, or at minimum a transparent PNG ≥2000px.
That single request is the largest available quality upgrade.

---

## All twelve files

| File | Type | Content | Verdict |
|---|---|---|---|
| **IMG_0662** | **Logo** | Primary badge: hexagon, truck front, "B.O.S / TRUCKING & SITE / INC." on black | ⭐ **Primary logo.** Used everywhere |
| **IMG_0663** | Logo lockup | Horizontal badge + wordmark + "TRUCK PARKING & STORAGE" + feature bar | Footer, social card |
| **IMG_0661** | **Photo + overlay** | Golden-hour lot panorama: sunset, sleeper cab, palms, **real B.O.S. gate sign** | ⭐ **Desktop hero.** Overlays cropped off |
| **IMG_0653** | Flyer wrapping a **real photo** | White Mack Granite tri-axle dump truck at night. Door decal: B.O.S. badge, "BOS TRUCKING AND SITE INC · FORT MYERS, FL", **USDOT 1418170**, 239-900-6374, unit 8 | ⭐ **Verified B.O.S. equipment.** Mobile hero + material feature |
| **IMG_0658** | **Photo** | B.O.S. yard sign on wood fence; service trucks and a semi behind the gate | ⭐ About section + gallery |
| **IMG_0660** | **Photo** | Lot entrance through open gates, daytime: trailers, box truck, cars, oak | ⭐ Parking card + gallery |
| IMG_0656 | Photo (derivative) | **Same frame as IMG_0660**, pre-cropped to a wide band | Kept — the ready-made panoramic crop suits the full-width parking band |
| IMG_0659 | Flyer | PARKING RATES $75 / $140 / $200, feature icons, disclaimer | **Source of truth for rates.** Not displayed |
| IMG_0654 | Flyer | "B.O.S. MATERIAL HAULING IS OFFICIAL" | **AI-generated truck and landscape.** Facts used; imagery excluded |
| IMG_0657 | Flyer | "PARKING AVAILABLE" — navy / red / white, stock semi photography | **Off-brand palette + stock imagery. Excluded entirely** |
| IMG_0652 | Flyer | NOW HIRING CDL A/B tri-axle dump driver, 30% load pay, part-time / on-call, local SWFL, home daily | Careers facts only; not on the site |
| IMG_0655 | Flyer | **Pixel-identical duplicate of IMG_0652** | 🔁 Duplicate — archived only |

**Net usable photography: five real photographs** (one of which is a crop variant of
another), plus two logo assets.

---

## Usage map

Five real photographs. **Zero stock, zero AI, zero invented equipment.**

| Placement | Image | Why |
|---|---|---|
| Hero, ≥768px | `bos-lot-sunset-fort-myers` | Strongest photograph. Sunset, sleeper cab, palms, and the real B.O.S. gate sign — sells location, parking and trucking in one frame |
| Hero, <768px | `bos-mack-dump-truck-portrait` | The panorama cannot crop to portrait. This can, and it is the strongest brand image available |
| Header / footer / favicons / share card | `bos-logo-badge`, `bos-logo-horizontal` | The supplied logo |
| Service card — Material Delivery | `bos-mack-dump-truck` | Real, verified equipment |
| Service card — Tri-Axle Hauling | `bos-lot-sunset-fort-myers` | Yard and equipment in context |
| Service card — Truck Parking | `bos-parking-lot-gate` | Literally the product |
| Material Delivery feature | `bos-mack-dump-truck` | **The money shot.** The door decal is legible: B.O.S. badge, Fort Myers FL, USDOT 1418170. Proof of a real operation, not a template |
| Truck Parking backdrop | `bos-parking-lot-wide` | The real lot behind the rate cards, heavily scrimmed |
| About / Our Yard | `bos-yard-sign` | B.O.S. signage on the real fence. Establishes a physical, permanent business |
| Gallery (6 tiles) | All five photographs | **No flyers in the gallery** |

### Excluded from the site

| File | Reason |
|---|---|
| IMG_0654 | AI-generated truck and landscape — would misrepresent the fleet |
| IMG_0657 | Navy/red/white palette (off-brand) and stock semi photography |
| IMG_0659, IMG_0652 | Flyers. Information extracted and rebuilt natively instead |
| IMG_0655 | Exact duplicate |

Information from the flyers *is* used — rates, the verbatim disclaimer, the materials
list, USDOT. Only the imagery is excluded.

---

## Crop boxes

All coordinates are in **original 1290×2796 source pixels** and live in
[`assets/sources.json`](../assets/sources.json), which is the single source of truth.

| Logical ID | Source | Crop `[l, t, r, b]` | Result |
|---|---|---|---|
| `bos-logo-badge` | IMG_0662 | `132, 904, 1189, 1880` | 1057×976, black keyed to transparent |
| `bos-logo-horizontal` | IMG_0663 | `40, 1161, 1271, 1666` | 1231×505, black keyed to transparent |
| `bos-lot-sunset-fort-myers` | IMG_0661 | `0, 1155, 1290, 1625` | 1290×470 — **all flyer overlays removed** |
| `bos-mack-dump-truck` | IMG_0653 | `0, 1020, 1290, 1784` | 1290×764 — flyer type excluded |
| `bos-mack-dump-truck-portrait` | IMG_0653 | `150, 1020, 761, 1784` | 611×764, framed on grille and cab |
| `bos-parking-lot-gate` | IMG_0660 | `0, 914, 1290, 1882` | 1290×968 |
| `bos-parking-lot-wide` | IMG_0656 | `0, 1060, 1290, 1736` | 1290×676 |
| `bos-yard-sign` | IMG_0658 | `0, 914, 1290, 1882` | 1290×968 |

For `bos-lot-sunset-fort-myers` the crop removes the top headline band, the feature strip,
the bottom-right phone box and the bottom address bar. **The B.O.S. sign on the gate is a
real physical sign in the photograph and is kept.**

> During the build, two crop boxes were initially recorded in post-letterbox coordinates
> rather than original-source coordinates, which produced near-blank output. Both are
> corrected above. When adding a crop, measure against the **untouched original**.

---

## Logo transparency

The supplied logo art sits on a solid black plate. `crop-source.py` keys pure black to
transparent with a smooth alpha ramp, so the same asset sits cleanly on `#0A0A0A`,
`#141414` and over photography without a visible rectangle.

Both versions are produced:

- `assets/brand/bos-logo-badge.png` — transparent, used on the site
- `assets/brand/bos-logo-badge-on-black.png` — as supplied, for reference

The keying is safe here because the artwork is white (`#FEFEFE`) and yellow (`#F8B804`)
with a very wide margin above the threshold, and because every surface on the site is
dark. **A vector logo would make this step unnecessary.**

---

## Output

```
public/img/
  brand/      bos-logo-badge-{120,180,240,360,480}.{png,webp}
              bos-logo-horizontal-{120,180,240,360,480}.{png,webp}
  hero/       bos-lot-sunset-fort-myers-{480,640,960,1280}.{avif,webp,jpg}
  trucks/     bos-mack-dump-truck-{480,640,960,1280}.{avif,webp,jpg}
              bos-mack-dump-truck-portrait-{480,611}.{avif,webp,jpg}
  parking/    bos-parking-lot-gate-{480,640,960,1280}.{avif,webp,jpg}
              bos-parking-lot-wide-{480,640,960,1280}.{avif,webp,jpg}
  property/   bos-yard-sign-{480,640,960,1280}.{avif,webp,jpg}
  og/         og-card.jpg  (1200×630, composed from the horizontal lockup)
```

**~7 MB on disk across 8 logical images.** The browser fetches one size and one format per
slot, so a real page load is a small fraction of that. The ladder stops at 1280 because
the pipeline never upscales; the 1600 / 1920 / 2560 rungs the markup already requests will
appear automatically once real originals land.
