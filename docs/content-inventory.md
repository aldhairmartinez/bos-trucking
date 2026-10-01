# Content Inventory

Every fact on the site, where it came from, and what we deliberately refuse to claim.

Sources: **[W]** the live Wix site (`bostruckingsite.wixsite.com/mysite`),
**[F]** supplied marketing flyers, **[P]** visible in a supplied photograph.

---

## Verified

| Fact | Value | Source |
|---|---|---|
| Legal name | B.O.S. Trucking & Site, Inc. | W, F, logo |
| Phone / text | 239-900-6374 | W, F, P (gate sign, truck door) |
| Email | bostruckingsite@gmail.com | W, F |
| Yard address | 2604 Market St, Fort Myers, FL 33916 | W, F, P |
| USDOT | 1418170 | W, F, **P (truck door decal)** |
| Service area | Fort Myers · Lee County · Southwest Florida | W, F |
| Services | Material delivery · Tri-axle dump truck hauling · Truck parking & storage | W (three service cards) |
| Materials | Fill dirt · Topsoil · Screened sand · Crushed shell · Rock · Aggregate · Base rock · Screenings · #57 · #89 | W + F |
| Parking features | Secure lot · 24-hour access · Camera monitored · Organized / assigned spaces · On-site professional management · Monthly | W, F |
| Rates | $75 / $140 / $200 per month | F (rates flyer) + W (live Pricing Plans) |
| Pricing disclaimer | *"Rates are based on overall vehicle size. Final pricing, vehicle acceptance, and space assignment are subject to management discretion."* | F — **verbatim, never paraphrased** |
| Gate signage | "AUTHORIZED CLIENTS ONLY" | P |
| Equipment | Mack Granite tri-axle dump truck, unit 8 | P (door decal) |
| Customer types | Contractors · site crews · homeowners · businesses | W |
| Vehicle types parked | Commercial trucks · trailers · equipment · RVs · vehicles | W, F |
| Careers (not on site) | CDL Class A/B tri-axle dump driver · 30% load pay · part-time / on-call · local SWFL · home daily | F |

### Copy taken near-verbatim from the owner's own site

- *"Fill dirt, topsoil, screened sand, crushed shell, base rock, and aggregate delivered
  for your project."*
- *"Reliable tri-axle hauling for construction, site work, contractors, homeowners, and
  businesses across Lee County."*
- *"Secure 24/7-access parking for commercial trucks, trailers, equipment, RVs, and
  vehicles."*

Where we rewrote, it was for concision and reading level only — never to add a claim.

---

## Conflicts

### 1. Mid parking tier: 20–29 ft or 20–30 ft? 🟡 Needs the owner

| Source | Range |
|---|---|
| Rates flyer [F] | **20–29 FT** |
| Live site + live Pricing Plans [W] | **20–30 ft** |

**We used 20–30 ft**, matching what is actually billed in production. A vehicle at exactly
29–30 ft is currently ambiguous under the flyer's wording. Worth settling so the flyer and
the site agree.

### 2. "24-hour access" vs "24/7 access"

Both appear. We standardised on **"24-hour access"** — the wording on the gate sign and
the rates flyer — and avoid "24/7" so it never implies a staffed office.

### 3. Service count: two or three?

The original brief described two services. The live site presents **three** (hauling is
its own card) and hauling is a real revenue line. **We built three.** Flagged because it
departs from the brief.

### 4. Service-area naming

Flyers say "Southwest Florida"; the site says "Lee County". Not a conflict — we use both,
as the owner does.

---

## Deliberately NOT claimed

Nothing in this list appears anywhere on the site, because none of it is verified.

| Not claimed | Why |
|---|---|
| Testimonials, reviews, star ratings | None supplied. `aggregateRating` and `review` are **blocked by `scripts/check.py`** |
| Years in business, "family-owned since …" | No founding date verified |
| Business or office hours | Unknown. `openingHours` is **blocked by `check.py`** |
| Fleet size, number of trucks | Only one truck is evidenced |
| Certifications, insurance, bonding, licences | Nothing beyond USDOT 1418170 |
| Customer counts, loads delivered, lots filled | No data |
| Guarantees, response times, "same-day delivery" | No commitment confirmed |
| Additional locations | One yard evidenced |
| Additional services | Only the three the owner lists |
| Pricing beyond $75 / $140 / $200 | Nothing else published |
| Availability — "spaces available now" | Changes daily; the CTA asks visitors to check |
| Minimum delivery quantity, delivery radius | Unknown |

### Two phrases chosen carefully

**"Family-run out of 2604 Market St"** (hero) — "family-run" is an inference, not a
sourced fact. It is the one soft characterisation on the site. **Confirm or cut it
tomorrow.**

**"the same people who answer the phone are the people at the yard"** (About) — a
description of a single-yard owner-operated business, consistent with everything supplied,
but also worth confirming.

Everything else traces to a cited source above.

---

## Why the Pricing Plans page is a problem today

The live site has `/pricing-plans/plans-pricing` with three parking subscriptions, each
showing **"Add to Cart"** and **"Buy Now"**.

Wix's own documentation is unambiguous: the free plan cannot accept online payments, and
Wix Pricing Plans has **no offline-payment mode**. So every customer who taps "Buy Now"
dead-ends.

Our site therefore uses **Check Availability / Call / Text** for parking and takes no
payment at all. Fixing the live buttons is the first item in the tomorrow checklist.

---

## Current site, for reference

Single-page home + four legal pages + one Pricing Plans page. Verified from the live page
payload:

- `isPremium: false` → **free plan**
- `isResponsive: false` → **classic Wix Editor**, not Studio
- Wix ad banner and Wix favicon present; `*.wixsite.com` subdomain
- Installed apps: Pricing Plans, Members Area, Member Authentication, Checkout & Orders,
  Wix Forms, Wix Smart Chat, **Wix Bookings (unused)**
- `metaSiteId: 4dfd309b-404f-41e7-83e4-ae5298c959de`, site revision 58

**All four legal pages still use Wix default URLs** — `/blank`, `/blank-1`, `/blank-2`,
`/blank-3` for Privacy, Accessibility, Terms and Refund. Their titles and meta
descriptions are properly written, so someone did the SEO work and never fixed the slugs.
An easy win.

The site's own confirmation copy, worth reusing:

> *"Thank you. B.O.S. Trucking & Site received your request and will follow up as soon as
> possible."*

Footer links Yelp and Facebook — **we have no URLs for either.**
