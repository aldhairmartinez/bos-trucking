# Original Project Brief

The brief this project was built from, kept for reference so later decisions can be
checked against what was actually asked for.

> **Note:** this file was reconstructed from the original `Untitled` file in the
> repository root after it was removed during cleanup. The content is the brief as
> supplied; only the formatting differs.

Where the build departs from this brief, the departure is recorded and justified:

- **Three service cards instead of two** — the live Wix site presents three (hauling is
  its own card) and hauling is a real revenue line. See
  [`content-inventory.md`](content-inventory.md).
- **No payments of any kind** — superseded by a later instruction, since we do not know
  how the owner currently accepts payment. See [`payments.md`](payments.md).
- **Production path is GitHub → Cloudflare Workers**, with a Wix rebuild as the alternative,
  because our HTML cannot be deployed into a classic Wix Editor site. See
  [`deployment.md`](deployment.md) and [`wix-setup.md`](wix-setup.md).

---

## Project location

The project directory already exists at `~/Developer/bos-trucking`. Work inside it; do not
create a nested project. The existing Wix website is
https://bostruckingsite.wixsite.com/mysite

A folder of photos, logos, marketing graphics and flyers supplied by the business owner
was added.

Permission granted to: inspect all supplied assets; rename files using web-development
best practices; reorganise them into appropriate directories; create optimised copies;
convert copies to WebP or other appropriate web formats; resize and compress copies for
web performance.

**Important:** preserve the original source assets somewhere in the repository. Do not
destructively modify or delete the originals.

Use descriptive lowercase filenames (`bos-trucking-logo.png`,
`fort-myers-truck-parking.jpg`) instead of `IMG_0653.jpeg`.

## Primary goal

Build a significantly improved website for B.O.S. Trucking & Site, Inc. It should not feel
like a generic Wix template. It should visually feel like the B.O.S. brand, whose supplied
branding establishes a clear identity: **black, yellow/gold, white**.

Think: trucking, industrial, rugged, strong, bold, professional, Southwest Florida,
modern.

But: do not simply recreate the advertising flyers as web pages. Translate that aggressive
black/yellow trucking aesthetic into a polished modern website. The result should feel like
a legitimate established trucking/material/parking business website rather than a flyer
pasted onto a webpage.

## Design system

Build a small consistent design system around the existing brand. Primary background:
black / near-black. Primary accent: B.O.S. yellow/gold derived from the supplied branding.
Primary text: white / off-white. Secondary surfaces: dark charcoal / subtle grey.

Use yellow intentionally for CTAs, important headings, borders and accent lines, icons,
hover states, pricing highlights, and important business information. Avoid covering
everything in yellow. Use generous spacing and strong typography so the site still feels
modern.

The design can use visual elements inspired by the branding: strong geometric sections,
angular accents, subtle industrial styling, bold condensed headings, dark photo overlays,
yellow borders and lines, large photography.

Do not go overboard with animations. Do not make it look like a gaming website. Do not make
it look like a construction template purchased for $20. Keep it polished.

## Use the actual photos

The supplied photos are important to the website. Do not treat them merely as reference
material. Actually incorporate appropriate supplied images.

Potential uses: **hero** — one of the strongest real truck/material/property photographs
with a dark gradient overlay; **parking section** — the real B.O.S. parking lot and
property photographs; **material hauling** — the real B.O.S. dump truck photography;
**gallery** — a clean responsive gallery using selected real photographs; **about** —
relevant real property or equipment imagery; **branding** — the supplied B.O.S. logo.

Do not use generic stock photography when an appropriate real B.O.S. image exists. Do not
generate fake trucks, facilities, employees, equipment or customers. Marketing flyers can
inform the visual design and business information, but do not simply display every flyer as
a giant image — extract the useful information and build it natively into the website.

## Business information

Use the existing website and supplied assets as sources of truth.

- B.O.S. Trucking & Site, Inc.
- Phone / text: 239-900-6374
- Email: bostruckingsite@gmail.com
- Address: 2604 Market St., Fort Myers, FL 33916
- Service area: Fort Myers / Southwest Florida
- USDOT: 1418170

Two major customer-facing areas:

**1. Material hauling / delivery** — marketing materials advertise bulk material delivery,
dirt, sand, rock, shell, aggregate, base rock, screenings, #57, #89.

**2. Truck parking & storage** — marketing materials advertise a secure lot, 24-hour
access, camera monitoring, organised parking, monthly parking.

Published parking rates: under 20 ft $75/month; 20–29 ft $140/month; 30 ft+ $200/month.

The supplied pricing advertisement states: *"Rates are based on overall vehicle size. Final
pricing, vehicle acceptance, and space assignment are subject to management discretion."*
Represent that disclaimer appropriately.

There is also recruiting material in the supplied assets. Treat careers/hiring as optional
content rather than a primary permanent website section unless the existing website
indicates otherwise.

**Do not invent:** testimonials, reviews, years in business, certifications, customer
numbers, guarantees, additional locations, additional services, pricing, availability, or
business claims.

## Website experience

Favour a clean local-business website with a strong conversion path.

**Header** — B.O.S. logo; navigation: Services, Material Delivery, Truck Parking, Gallery,
Contact; primary CTA: CALL / TEXT.

**Hero** — use a strong real B.O.S. photograph with a dark overlay so text remains
readable. Example hierarchy: "B.O.S. TRUCKING & SITE"; "Material Hauling & Secure Truck
Parking / Fort Myers & Southwest Florida"; primary CTA "CALL OR TEXT 239-900-6374";
secondary CTA "REQUEST A QUOTE"; small trust indicators such as Material Delivery, Secure
Parking, 24/7 Access. Do not blindly use this exact copy if it can be improved while
remaining factual.

**Services** — two prominent service cards: Material Hauling & Delivery; Truck Parking &
Storage. Use real imagery.

**Material hauling** — present available materials cleanly (dirt, sand, rock, shell,
aggregate, base rock, screenings, #57, #89). CTA: REQUEST DELIVERY QUOTE. Use an actual
supplied B.O.S. truck image prominently.

**Truck parking** — highlight secure lot, 24-hour access, camera monitoring, monthly
parking. Pricing: under 20 ft $75/month; 20–29 ft $140/month; 30 ft+ $200/month. CTA:
CHECK AVAILABILITY. Include the pricing/acceptance disclaimer. Use actual parking-lot
photography.

**Gallery** — a responsive gallery using the best supplied real photos, prioritising
trucks, property, parking lot, material hauling and recognisable B.O.S. branding. Do not
fill the gallery with marketing flyers.

**Contact** — make contacting the business extremely easy: phone/text 239-900-6374; email
bostruckingsite@gmail.com; address 2604 Market St., Fort Myers, FL 33916; request-quote
form.

**Footer** — logo, navigation, phone, email, address, USDOT 1418170 if appropriate.

## Mobile experience

Mobile is extremely important. This is a local service business and many visitors will
arrive from a phone. Design mobile-first. Consider a persistent bottom mobile action bar:
CALL, TEXT, QUOTE. Use proper `tel:` and `sms:` links. Calling or texting B.O.S. should
take one tap.

## Quote request

Create a clean quote experience supporting:

**Material delivery** — name, phone, email, material needed, delivery location,
quantity/details, additional notes.

**Truck parking** — name, phone, email, vehicle type, approximate vehicle length, desired
start date, additional notes.

Keep this simple. Plan how Wix will receive, store and send these submissions once we have
access.

## Payments

Do not implement payments yet. Create `docs/payments.md`. Research what is currently
possible using Wix's free plan. A possible future architecture: website → parking/payment
CTA → hosted payment checkout → Stripe or another PCI-compliant provider → success /
confirmation. Never collect, store, process or log raw credit-card numbers ourselves.

## Wix

We do not have access to the owner's Wix account today; access is expected later. Research
the current Wix developer ecosystem using official Wix documentation, and determine:
current Velo capabilities; Wix Studio capabilities; Wix CLI / local development; Git and
GitHub support; backend capabilities; custom frontend capabilities; external API support;
free-plan limitations; forms; deployment workflow; existing Wix Editor vs Wix Studio
implications; what we can build locally today; what can actually transfer into the owner's
existing Wix site; what may need to be recreated inside Wix; what requires Wix
credentials.

Do not assume historical Wix/Velo workflows are still correct. If the plan is technically
wrong, say so before implementing it.

## Local preview

The site must be viewable and interactive locally today. Create a local implementation
that runs locally, looks like the eventual website, uses the real assets, is responsive,
and lets us iterate on the design before touching Wix. Keep the stack simple. This is not
a SaaS application. Do not introduce unnecessary frameworks or infrastructure.

## SEO

Implement sensible local SEO using verified facts. Relevant concepts: B.O.S. Trucking &
Site, Fort Myers, Southwest Florida, truck parking, truck storage, secure truck parking,
material delivery, bulk material delivery, dirt, sand, rock, shell, aggregate. Use semantic
HTML, good page titles, meta descriptions, heading hierarchy, alt text, and structured data
if appropriate. Do not keyword-stuff.

## Performance

Optimise supplied images for web delivery. Preserve originals. Generate appropriately
sized derivatives. Use WebP/AVIF where appropriate while maintaining compatibility. Use
responsive image techniques where appropriate. Lazy-load below-the-fold images. Do not
serve a 5 MB photograph when a 300 KB optimised version is sufficient.

## Accessibility

Use semantic HTML, keyboard navigation, visible focus states, proper form labels, good
colour contrast, meaningful alt text, and accessible buttons and links. Black/yellow
branding must remain readable and accessible.

## Project structure

Use the current directory. Files and folders may be reorganised according to development
best practices. At minimum create `README.md` and `docs/` containing `architecture.md`,
`wix-setup.md`, `deployment.md` and `payments.md`. Organise all supplied imagery properly.
Preserve originals.

## Git / GitHub

Initialise this existing directory as a Git repository if necessary. The repository will
eventually be pushed to the owner's GitHub account and may eventually be public. Assume
everything committed could become public. Create an appropriate `.gitignore` excluding
`.env`, secrets, credentials, API keys, tokens, Wix secrets, Stripe secrets,
`node_modules`, unnecessary build artifacts, and OS/editor junk. Create `.env.example`
only if needed, containing placeholders only.

Before committing: inspect `git status`, inspect `git diff`, check for secrets, check for
accidental private files.

**Do not push to GitHub. Do not create a GitHub repository.** Wait for explicit approval.

## Documentation

`README.md` should document the business, website architecture, local development, asset
organisation, Wix integration, deployment, security, and future payment integration.
Include a simple Mermaid architecture diagram. Create a prominent
**TOMORROW: WIX DEPLOYMENT** checklist telling us exactly what to do once logged into the
owner's Wix account.

## Working style

Work autonomously. Do not ask questions answerable by inspecting the existing website, the
supplied assets, or official Wix documentation.

Prefer, in order: professional design, simplicity, mobile-first, performance,
maintainability, Wix-native where practical, free where practical, GitHub-friendly.

Stop before anything requiring credentials, payment, Wix account access, GitHub
authentication, destructive external changes, or irreversible actions.

## First task — plan before code

Before writing implementation code: inspect every supplied asset; inventory and categorise
the images; identify duplicates or low-quality assets; identify the strongest candidates
for logo, hero, material hauling, truck parking and gallery; inspect the existing Wix
website; research current official Wix developer documentation; inventory verified business
information; identify uncertain or conflicting information; propose the site information
architecture; propose the visual/design system; give the proposed black/yellow/white
palette including hex values derived from the supplied branding where practical; propose
typography; propose the technical architecture; explain how the local implementation will
transfer to Wix; explain free-Wix limitations; show the proposed project structure; explain
how the supplied assets will be reorganised and renamed; state exactly which images will be
used and where. Then stop, and do not write implementation code until the plan is approved.
