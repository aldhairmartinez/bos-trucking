# Wix Platform Research & Setup

Researched against **official Wix documentation**, current as of this build. Historical
Velo workflows were not assumed.

---

## What the existing site actually is

Verified from the live page payload at `bostruckingsite.wixsite.com/mysite`, not guessed:

| | |
|---|---|
| Plan | **Free** — `"isPremium": false` |
| Editor | **Classic Wix Editor** — `"isResponsive": false` (not Wix Studio) |
| Domain | `*.wixsite.com` subdomain, Wix ad banner + Wix favicon present |
| metaSiteId | `4dfd309b-404f-41e7-83e4-ae5298c959de` |
| Site revision | 58 |
| Structure | 1 home page + 4 legal pages + 1 Pricing Plans page |
| Page URLs | `/blank`, `/blank-1`, `/blank-2`, `/blank-3` — **all Wix defaults** |
| Installed apps | Pricing Plans · Members Area · Member Authentication · Checkout & Orders · Wix Forms · Wix Smart Chat · **Wix Bookings (unused)** |

---

## 🔴 Three findings that shape everything

### 1. The live parking "Buy Now" buttons cannot take money

`/pricing-plans/plans-pricing` shows three parking subscriptions ($75 / $140 / $200
monthly) each with **"Add to Cart"** and **"Buy Now"**.

Per Wix: the free plan cannot accept online payments, and *"The manual (offline) payment
method is not available with Pricing Plans."* So there is no configuration in which those
buttons work today — every customer who taps one dead-ends.

**This is a live revenue and trust bug and the single most urgent fix.**

### 2. Git Integration & Wix CLI does not deploy our site, and costs the owner their editor

It version-controls **Velo page and backend code only** — not visual layout. Our HTML/CSS
cannot be shipped through it.

And from Wix's own setup guide: *"Once you connect your site to GitHub, your editor enters
read-only mode."* The owner would permanently lose visual editing of their own site.

Wix also warns that deleting the repo or revoking the Velo GitHub app *"may cause your
site's GitHub connection to stop working even if you restore the repo or reinstall the
app."*

**Do not connect GitHub from inside Wix.** It solves nothing we need and is close to
irreversible.

### 3. A classic Editor site cannot be migrated to Wix Studio

Wix: *"in order to transfer a Wix Editor site to the Studio Editor, you have to rebuild it
from scratch."*

A Studio **branch** of an Editor site is possible, but: it requires **Premium to create**,
a **Wix Studio plan to publish**, and *"The design of the site is not carried over."*

---

## Capability matrix

| Capability | Status for this site |
|---|---|
| Velo (still the current name) | ✅ Available on free sites, with quotas |
| Velo free-plan quotas | 1,000 data items · 1,000 collections · 4 indexes · 1,000 reads + 60 writes/min · 5s data timeout · 1 micro container (1 vCPU / 400 MB) · **60 backend req/min** · 14s backend timeout · 20 scheduled jobs, 1-hour minimum interval |
| Dev environments | Built-in code editor (Editor + Studio) · **Wix IDE** (Studio only) · local IDE via Wix CLI + GitHub (Editor or Studio) |
| Wix CLI prerequisites | Git · **Node ≥20.11** · npm/yarn · SSH key on GitHub. Incompatible with Velo Packages (npm packages are fine) |
| Backend / external APIs | Velo backend (`.web.js`), HTTP functions, `fetch` to third-party APIs, npm packages, Wix Data/CMS, Secrets Manager |
| Deploying our own HTML/CSS | ❌ **Not possible** in the classic Editor |
| Custom Code injection (Settings → Custom Code) | ❌ **Requires a connected domain** → unavailable on the free plan |
| Structured data (JSON-LD) | ✅ Per-page via SEO panel → Advanced SEO. **JSON-LD only, ≤5 markups, <7,000 chars** |
| Page titles / meta descriptions | ✅ SEO panel |
| Wix Forms | ✅ Installed. Submissions → Dashboard → Forms & Submissions + email to the account address. Works on free |
| Online payments | ❌ Requires a paid plan (lowest payment-capable tier found: Core, ~$29/mo — **verify current pricing**) |
| Custom domain | ❌ Requires Premium |
| Remove Wix ad banner / favicon | ❌ Requires Premium |
| Storage / bandwidth (free) | 500 MB / 1 GB — ample for us (full optimised image set is well under 10 MB) |

---

## Free-plan limitations that actually matter

| Limitation | Impact |
|---|---|
| **No online payments** | 🔴 Parking subscriptions cannot be collected. Blocks the main monetisation |
| **No custom domain** | 🔴 `bostruckingsite.wixsite.com/mysite` hurts credibility and local SEO, and blocks Custom Code |
| **Wix ad banner + Wix favicon** | 🟠 Undercuts "established business" on first impression |
| Custom Code needs a domain | 🟠 Use the per-page SEO panel for JSON-LD instead — works fine |
| Pricing Plans needs online payment | 🔴 No workaround on free |
| 500 MB / 1 GB | 🟡 Not a constraint for us |
| Velo quotas | 🟡 Irrelevant at this traffic level |

**The cheapest meaningful upgrade is a custom domain plus ad removal.** That alone fixes
the three credibility items, short of payments.

---

## What transfers from our build

| Artifact | Transfers? | How |
|---|---|---|
| Optimised images | ✅ Direct | Upload `public/img/**` to Wix Media Manager |
| All copy | ✅ Direct | Paste from [`copy-deck.md`](copy-deck.md) |
| Palette hexes | ✅ Direct | Wix site colour palette slots |
| Page titles / meta descriptions | ✅ Direct | SEO panel |
| JSON-LD structured data | ✅ Direct | SEO panel → Advanced SEO (≤5 markups, <7,000 chars) |
| Typography | ⚠️ Conditional | Only if Barlow Condensed + Inter are in Wix's font picker, or upload is available |
| Sticky mobile Call/Text/Quote bar | ⚠️ Partial | Wix has a built-in mobile Action Bar; less refined than ours |
| Layout and spacing | ❌ Rebuilt by hand | Classic Editor is absolute-position with a **separate mobile editor** — lay out twice |
| CSS effects (gradients, hairlines, clipped corners, hover states) | ❌ Approximated | Editor design controls only |
| Forms | ❌ Rebuilt | Recreate field-for-field from [`forms.md`](forms.md) |
| Our HTML/CSS/JS as files | ❌ **Not possible** | Full-page HTML embeds are sandboxed iframes: invisible to Google, broken mobile sizing. **Not recommended** |

So under a Wix rebuild, our local build's job is to be an **unambiguous, approved design
specification**, so the Wix work is mechanical execution rather than design-by-committee
in a slow editor.

---

## Tomorrow's click-paths

### Save a restore point first

Site → **Site History** → name a version `pre-redesign-<date>`. Before any edit.

### Fix the page URLs

Pages & Menu → ⋯ next to each page → **SEO basics** → URL slug:

| From | To |
|---|---|
| `/blank` | `/privacy-policy` |
| `/blank-1` | `/accessibility-statement` |
| `/blank-2` | `/terms-and-conditions` |
| `/blank-3` | `/refund-policy` |

Then Marketing & SEO → **URL Redirect Manager** → add a 301 from each old slug.

### Neutralise the broken payment buttons

Either unpublish `/pricing-plans/plans-pricing`, or edit each plan's button to
**"Check Availability"** pointing at the quote form. Do this before anything cosmetic.

### Remove the unused app

Apps → **Wix Bookings** → Delete. Installed but unused.

### Verify form delivery

Dashboard → **Forms & Submissions**. Submit a test from the live site and confirm the
notification lands in the owner's inbox. Note which address it goes to.

### Add structured data

Pages & Menu → Home → ⋯ → SEO basics → **Advanced SEO** → **Structured Data Markup** →
*+ Add New Markup*. Paste the `LocalBusiness` block from `public/index.html`.
JSON-LD only, maximum 5 markups per page, under 7,000 characters.

### Set the palette

Site Design → Colours. Use `#0A0A0A`, `#141414`, `#F8B804`, `#FFFFFF`, `#B5B5B0` — see
[`design-system.md`](design-system.md).

### Check the fonts

Site Design → Text Themes. Look for **Barlow Condensed** and **Inter**. If absent,
substitute from Wix's library and record the swap in `design-system.md`. Custom font
upload may be premium-gated — verify, do not assume.

### Lay out mobile separately

Top bar → mobile icon. The classic Editor keeps a **distinct mobile layout**; desktop work
does not carry over. Enable the mobile **Action Bar** with Call / Text / Quote.

---

## Sources

- [Development Environments](https://dev.wix.com/docs/develop-websites/articles/get-started/development-environments)
- [Setting Up Git Integration & Wix CLI](https://dev.wix.com/docs/develop-websites/articles/workspace-tools/developer-tools/git-integration-wix-cli-for-sites/setting-up-git-integration-wix-cli-for-sites)
- [Using Velo with a Free Wix Site](https://dev.wix.com/docs/develop-websites/articles/coding-with-velo/premium-plans/using-velo-with-a-free-wix-site)
- [Pricing Plans: Setting Up Payments](https://support.wix.com/en/article/pricing-plans-setting-up-payments)
- [Rebuilding Your Site in the Studio Editor](https://support.wix.com/en/article/wix-editor-rebuilding-your-site-in-the-studio-editor)
- [Studio Branches of Wix Editor Sites](https://support.wix.com/en/article/studio-editor-about-studio-branches)
- [Embedding Custom Code](https://support.wix.com/en/article/embedding-custom-code-to-your-site)
- [Adding Structured Data Markup](https://support.wix.com/en/article/adding-structured-data-markup-to-your-sites-pages-2546962)
- [About Storage and Bandwidth](https://support.wix.com/en/article/about-storage-and-bandwidth)
- [Building a Website for Free](https://support.wix.com/en/article/building-a-website-for-free)
