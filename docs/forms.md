# Forms

## Status: built, validated, **not wired to a backend**

Both forms render natively, validate accessibly, and then tell the visitor the truth:

> **Preview mode.** Online form delivery is not connected yet. To reach B.O.S. right now,
> call or text 239-900-6374 or email bostruckingsite@gmail.com.

That is deliberate. A form that silently swallows a real customer's enquiry is worse than
no form. The `<form action>` is `#`, and `quote-form.js` detects that and shows the notice
instead of pretending to send.

---

## Where the forms are

| Location | Purpose | Fields |
|---|---|---|
| `index.html` → `#contact` | Short intake, low friction | Name, Phone, mode-specific select, Details |
| `quote.html` | Full quote request | See the field spec below |

Both share one component (`public/js/quote-form.js`) and one submission target once wired.

---

## Field specification

### Shared

| Field | `name` | Type | Required | Notes |
|---|---|---|---|---|
| Request type | `requestType` | radio | yes | `material` \| `parking`. In a `<fieldset>` with a `<legend>` |
| Name | `name` | text | **yes** | `autocomplete="name"` |
| Phone | `phone` | tel | **yes** | `inputmode="tel"`, `autocomplete="tel"` |
| Email | `email` | email | no | `inputmode="email"`. Hint: "We will call or text first." |
| Notes | `notes` / `details` | textarea | no | Label swaps with the mode |
| Honeypot | `_hp` | text | no | Off-screen, `tabindex="-1"`. **Any value = discard** |

### Material delivery / hauling (`requestType=material`)

| Field | `name` | Type | Required | Options |
|---|---|---|---|---|
| Material needed | `material` | select | **yes** | Fill Dirt · Topsoil · Screened Sand · Crushed Shell · Rock · Aggregate · Base Rock · Screenings · #57 · #89 · Hauling only (no material) · Not sure — please advise |
| Delivery location | `deliveryLocation` | text | **yes** | `autocomplete="street-address"` |
| Quantity / load details | `quantity` | text | no | e.g. "2 tri-axle loads", "20 yards" |
| When needed | `materialDate` | date | no | |

### Truck parking (`requestType=parking`)

| Field | `name` | Type | Required | Options |
|---|---|---|---|---|
| Vehicle type | `vehicleType` | select | **yes** | Car · Pickup truck · Work truck · Box truck · Semi tractor · Semi trailer · Dump truck · Trailer (utility or enclosed) · RV or motorhome · Equipment · Other |
| Approximate length | `vehicleLength` | select | **yes** | Under 20 ft — $75/mo · 20–30 ft — $140/mo · 30 ft or more — $200/mo · Not sure |
| Desired start date | `startDate` | date | no | |

The length options show the matching rate, and the field carries the owner's verbatim
disclaimer as a hint.

---

## Behaviour

**Mode switching.** The inactive field set gets `hidden` **and** `disabled`, so its values
never submit and it leaves the tab order entirely.

**Deep linking.** Mode is read from and written to the URL as `?type=parking` or
`?type=material`. So "Check Availability" on the parking section opens the quote page with
the parking fields already showing. Links used:

- `/quote.html?type=material` — material delivery, tri-axle hauling
- `/quote.html?type=parking` — truck parking, trailer & RV storage

**Validation.** Native constraint validation does the checking. The script only supplies
readable messages, sets `aria-invalid`, wires `aria-describedby` to the error node, and
moves focus to the first problem. Errors are announced, not signalled by colour alone.
`novalidate` is set by JS, so with JS disabled the browser's own validation still works.

---

## Wiring it up

### Path A — Wix Forms *(if the site stays on Wix)*

Wix Forms is **already installed** and works on the free plan. Submissions land in
**Dashboard → Forms & Submissions**, with an email notification to the account address.

1. Dashboard → Forms → **+ New Form**
2. Recreate the fields above, matching labels and required flags
3. Use a single-select "What do you need?" field for `requestType` — this mirrors the
   existing site's "Select a service" control
4. Set the confirmation message to the owner's existing wording:
   *"Thank you. B.O.S. Trucking & Site received your request and will follow up as soon as
   possible."*
5. Settings → notification email → confirm it reaches the owner's inbox
6. **Send a real test submission and verify it arrives**

**Note:** Wix Forms cannot show/hide field groups conditionally the way our two-mode switch
does. Either build two separate forms, or use one form with all fields and mark the
mode-specific ones optional. Two forms is cleaner for the owner reading submissions.

### Path B — Cloudflare Worker + Resend *(if we host on Cloudflare Workers)*

This is the one case that needs a Worker script. Add `main` to `wrangler.jsonc` and a
handler that runs before assets for `/api/*` (`run_worker_first`), which:

1. Accept `POST`, parse the form body
2. Reject if `_hp` is non-empty (bot)
3. Validate `name` and `phone` server-side — never trust the client
4. Send via Resend (free tier covers this volume) to `bostruckingsite@gmail.com`
5. `302` to `/thank-you.html`

Then set `action="/api/quote"` on both forms and remove nothing else — `quote-form.js`
detects a real action and stops showing the preview notice.

Secrets go in Cloudflare → the Worker → Settings → Variables and Secrets, **never in Git**:

```
RESEND_API_KEY=<set in the Cloudflare dashboard>
QUOTE_TO_EMAIL=bostruckingsite@gmail.com
```

This needs a Resend account and an API key → **credentials, so we stop and ask.**

### Path C — Formspree *(fastest, zero code)*

Set `action="https://formspree.io/f/<id>"` on both forms. Free tier is 50 submissions a
month. Needs an account → **credentials, so we stop and ask.**

---

## Privacy

The form collects only what is needed to return a quote: name, phone, optional email, and
the job details the visitor chooses to type. No tracking, no analytics, no third-party
scripts, no cookies. `public/privacy-policy.html` states exactly this.

**No payment field appears on any form, ever.** See [`payments.md`](payments.md).

---

## Checklist before launch

- [ ] Backend wired (A, B or C)
- [ ] `action` points at the real endpoint on **both** `index.html` and `quote.html`
- [ ] Real test submission from a phone, received and readable
- [ ] Confirm which inbox receives it, and that someone checks it
- [ ] Confirm the thank-you page or message appears after a real submit
- [ ] Honeypot verified: fill `_hp` via devtools and confirm the submission is dropped
- [ ] Required-field errors announced by a screen reader
- [ ] `npm run check` still passes
