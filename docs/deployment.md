# Deployment

**Nothing has been deployed. Nothing has been pushed to GitHub.** Both require explicit
approval.

---

## Likely production path

```
GitHub  →  Cloudflare Pages  →  custom domain
```

This is the recommended route. `public/` is already a valid Cloudflare Pages site:

| Setting | Value |
|---|---|
| Framework preset | **None** |
| Build command | *(leave empty)* |
| Build output directory | `public` |
| Root directory | *(repository root)* |

No build step, no `node_modules`, no environment variables. Cloudflare serves the files.

**Why this path**

- **100% design fidelity** — it ships exactly what you reviewed locally
- **Free** — Cloudflare Pages' free tier is unmetered bandwidth for a site this size; a
  domain is roughly $10/year
- **Fast** — global CDN, automatic HTTPS, HTTP/3, Brotli
- **Real responsive control** — no separate mobile editor to maintain
- **Git-native** — every change is a reviewable commit; push to deploy; instant rollback
- Removes the Wix ad banner and the `wixsite.com` subdomain at a fraction of Wix Premium

**The cost**: the owner loses the Wix visual editor. Content changes go through this repo.
For a site whose content is a phone number, three rates and ten material names, that is
usually the right trade — but it is **the owner's call, not ours.**

`scripts/serve.py` deliberately mimics Pages' clean-URL and 404 behaviour, so `/quote`
resolves and unknown paths serve the branded `404.html` with a real 404 status. What you
review locally is what ships.

---

## Alternative: rebuild by hand in the owner's Wix Editor

Use this site as the design specification and reproduce it inside the existing classic
Wix Editor.

**Why you might choose it**

- **Free**, no new accounts, no migration
- The owner keeps the visual editor and full control
- Nothing about the existing Wix setup (Forms, Members, Pricing Plans) has to move

**The cost**

- **~70% design fidelity.** The classic Editor is absolute-position with a **separate
  mobile editor**, so mobile-first work has to be laid out twice, and CSS effects
  (gradients, hairlines, clipped corners, hover states) are approximated at best
- Half a day of manual rebuilding, and it drifts from this repo over time
- Keeps the Wix ad banner and the `wixsite.com` subdomain unless upgraded

Step-by-step in [`wix-setup.md`](wix-setup.md). Copy to paste in
[`copy-deck.md`](copy-deck.md) — **never retype the pricing disclaimer.**

---

## Rejected options, and why

| Option | Verdict |
|---|---|
| **Git Integration & Wix CLI** | ❌ Version-controls Velo code only — cannot deploy our HTML. And *"your editor enters read-only mode"*, permanently costing the owner visual editing. Solves nothing we need. |
| **Full-page HTML iframe embed in Wix** | ❌ Sandboxed iframe: invisible to Google, broken mobile sizing, no real SEO. A trap. |
| **Wix Studio rebuild** | ❌ for now. A classic Editor site cannot be migrated — only rebuilt. A Studio branch needs **Premium to create** and a **Studio plan to publish**, and carries no design over. Only sensible if upgrading anyway. |

---

## Before going live anywhere

The repo currently uses `https://bostruckingsite.com` as a placeholder host. Replace it
with the real domain in:

- `public/robots.txt` — the `Sitemap:` line
- `public/sitemap.xml` — every `<loc>`
- every `<link rel="canonical">` (7 pages)
- every `og:image` and `og:url` (index, quote)
- the `LocalBusiness` JSON-LD in `public/index.html` (`@id`, `url`, `image`, `logo`)

Then:

- [ ] `npm run check` passes
- [ ] Forms are wired and a real test submission arrives — see [`forms.md`](forms.md)
- [ ] Tap-to-call and tap-to-text tested **on a real phone**, not an emulator
- [ ] Legal pages replaced with the owner's approved Wix text (ours are marked
      placeholders)
- [ ] Sitemap submitted in Google Search Console
- [ ] Google Business Profile name / address / phone match the site exactly
- [ ] Keep the Wix site live until the new one is verified, then 301 or retire it

---

## Rollback

**Cloudflare Pages** — every push is a numbered deployment. Dashboard → Deployments →
*Rollback*. Instant, no rebuild.

**Wix** — Site → Site History → restore the `pre-redesign-<date>` version. Create that
restore point *before* making any edit.

---

## Cost summary

| Path | Setup | Ongoing |
|---|---|---|
| GitHub → Cloudflare Pages + domain | Free | **~$10/year** (domain only) |
| Wix rebuild, stay on free | Free | **$0** — keeps ad banner, no custom domain |
| Wix rebuild + Premium | Free | **~$17–29/month**, varies — verify current Wix pricing |
| Wix Studio rebuild | Premium required | Wix Studio plan |

Accepting online payments adds cost under **every** path — see [`payments.md`](payments.md).
