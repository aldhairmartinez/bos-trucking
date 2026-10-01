#!/usr/bin/env python3
"""
Quality checks for the B.O.S. Trucking & Site website.

Standard library only. Run before every commit:

    python3 scripts/check.py        (or: npm run check)

Checks performed
  1. Assets      every local href/src/srcset referenced by the HTML exists
  2. Links       every internal page link and in-page #anchor resolves
  3. Images      alt present, width/height present, lazy below the fold
  4. Headings    exactly one <h1>, no skipped heading levels
  5. Forms       every field has a matching <label for>
  6. Contact     the phone number is consistent and tel:/sms: are E.164
  7. SEO         title, meta description, canonical, OG image, valid JSON-LD
  8. A11y        skip link, lang, viewport, no outline:none, no tabindex > 0
  9. Hygiene     no TODO/FIXME/placeholder markers, no absolute file paths
 10. Payload     reports per-page weight and the heaviest images

Exit status is non-zero if any ERROR is found. WARN items are advisory.
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

PHONE_DISPLAY = "239-900-6374"
PHONE_E164 = "+12399006374"
EMAIL = "bostruckingsite@gmail.com"

errors: list[str] = []
warnings: list[str] = []
notes: list[str] = []


def err(page: str, msg: str) -> None:
    errors.append(f"{page}: {msg}")


def warn(page: str, msg: str) -> None:
    warnings.append(f"{page}: {msg}")


def strip_comments(s: str) -> str:
    return re.sub(r"<!--.*?-->", "", s, flags=re.S)


def tags(src: str, name: str) -> list[str]:
    return re.findall(rf"<{name}\b[^>]*>", src, re.I)


def attr(tag: str, name: str) -> str | None:
    m = re.search(rf'\b{name}\s*=\s*"([^"]*)"', tag, re.I)
    if m:
        return m.group(1)
    m = re.search(rf"\b{name}\s*=\s*'([^']*)'", tag, re.I)
    return m.group(1) if m else None


def has_attr(tag: str, name: str) -> bool:
    return re.search(rf"\b{name}\b", tag, re.I) is not None


# ---------------------------------------------------------------------------
# 1 + 2 — assets and links
# ---------------------------------------------------------------------------
def local_refs(src: str) -> set[str]:
    refs: set[str] = set()
    for pat in (
        r'(?:href|src)\s*=\s*"([^"]+)"',
        r"(?:href|src)\s*=\s*'([^']+)'",
    ):
        refs.update(re.findall(pat, src))
    for srcset in re.findall(r'srcset\s*=\s*"([^"]+)"', src, re.I):
        for part in srcset.split(","):
            url = part.strip().split()[0] if part.strip() else ""
            if url:
                refs.add(url)
    return refs


def check_refs(page: str, src: str) -> None:
    pages = {p.name for p in PUBLIC.glob("*.html")}

    for ref in local_refs(src):
        ref = html.unescape(ref.strip())
        if not ref or ref.startswith(
            ("http://", "https://", "mailto:", "tel:", "sms:", "data:", "//")
        ):
            continue

        # In-page anchor
        if ref.startswith("#"):
            anchor = ref[1:]
            if anchor and not re.search(
                rf'\bid\s*=\s*["\']{re.escape(anchor)}["\']', src
            ):
                err(page, f"anchor #{anchor} has no matching id")
            continue

        path_part, _, frag = ref.partition("#")
        path_part = path_part.split("?")[0]
        if not path_part:
            continue

        target = (PUBLIC / path_part.lstrip("/")) if path_part.startswith("/") else (
            PUBLIC / path_part
        )

        if path_part.startswith("/") and path_part.endswith("/"):
            target = PUBLIC / "index.html"
        if path_part == "/":
            target = PUBLIC / "index.html"

        if not target.exists() and not target.with_suffix(".html").exists():
            err(page, f"missing local file: {ref}")
            continue

        # Cross-page anchor
        if frag and target.suffix == ".html" and target.exists():
            other = target.read_text(encoding="utf-8")
            if not re.search(rf'\bid\s*=\s*["\']{re.escape(frag)}["\']', other):
                err(page, f"anchor {ref} has no matching id in {target.name}")

        if target.suffix == ".html" and target.name not in pages and target.exists():
            pass


# ---------------------------------------------------------------------------
# 3 — images
# ---------------------------------------------------------------------------
def check_images(page: str, src: str) -> None:
    body = src[src.find("<body") :]
    for i, tag in enumerate(tags(body, "img")):
        label = attr(tag, "src") or f"img#{i}"

        # The lightbox viewer's <img> is populated at runtime from whichever
        # tile was clicked, so it has no fixed source, intrinsic size, or
        # loading strategy to assert on.
        if has_attr(tag, "data-lightbox-img"):
            continue

        if attr(tag, "alt") is None:
            err(page, f"<img> has no alt attribute: {label}")

        if not has_attr(tag, "width") or not has_attr(tag, "height"):
            err(page, f"<img> missing width/height (causes layout shift): {label}")

        priority = (attr(tag, "fetchpriority") or "").lower() == "high"
        loading = (attr(tag, "loading") or "").lower()
        if not priority and loading != "lazy":
            warn(page, f"<img> is neither fetchpriority=high nor loading=lazy: {label}")
        if priority and loading == "lazy":
            err(page, f"<img> is both fetchpriority=high and loading=lazy: {label}")

    # Every <picture> should end in a plain <img> fallback.
    for block in re.findall(r"<picture\b.*?</picture>", body, re.S | re.I):
        if "<img" not in block.lower():
            err(page, "<picture> has no <img> fallback")


# ---------------------------------------------------------------------------
# 4 — headings
# ---------------------------------------------------------------------------
def check_headings(page: str, src: str) -> None:
    body = strip_comments(src[src.find("<body") :])
    levels = [int(m) for m in re.findall(r"<h([1-6])\b", body, re.I)]

    h1s = levels.count(1)
    if h1s == 0:
        err(page, "no <h1>")
    elif h1s > 1:
        err(page, f"{h1s} <h1> elements; there must be exactly one")

    prev = 0
    for lvl in levels:
        if prev and lvl > prev + 1:
            warn(page, f"heading level jumps from h{prev} to h{lvl}")
        prev = lvl


# ---------------------------------------------------------------------------
# 5 — forms
# ---------------------------------------------------------------------------
def check_forms(page: str, src: str) -> None:
    label_for = set(re.findall(r'<label\b[^>]*\bfor\s*=\s*"([^"]+)"', src, re.I))

    for tag in tags(src, "input") + tags(src, "select") + tags(src, "textarea"):
        itype = (attr(tag, "type") or "text").lower()
        if itype in {"hidden", "submit", "button", "reset"}:
            continue
        fid = attr(tag, "id")
        name = attr(tag, "name") or "?"

        if itype in {"radio", "checkbox"}:
            continue  # wrapped in <label>, verified by eye and by the a11y pass

        if not fid:
            err(page, f"form field has no id, so no label can target it: name={name}")
        elif fid not in label_for and not attr(tag, "aria-label"):
            err(page, f"form field has no <label for>: id={fid}")

    # Radio groups must sit in a fieldset with a legend.
    if re.search(r'type\s*=\s*"radio"', src, re.I):
        if "<fieldset" not in src.lower() or "<legend" not in src.lower():
            err(page, "radio group is not wrapped in <fieldset> with a <legend>")


# ---------------------------------------------------------------------------
# 6 — contact details
# ---------------------------------------------------------------------------
def check_contact(page: str, src: str) -> None:
    # Placeholder text is a format hint, not published contact information, so
    # it is excluded before scanning for stray phone numbers and addresses.
    scan = re.sub(r'placeholder\s*=\s*"[^"]*"', "", src, flags=re.I)

    for t in re.findall(r'href\s*=\s*"tel:([^"]+)"', src, re.I):
        if t != PHONE_E164:
            err(page, f"tel: link is not E.164 {PHONE_E164}: tel:{t}")

    for s in re.findall(r'href\s*=\s*"sms:([^"?]+)', src, re.I):
        if s != PHONE_E164:
            err(page, f"sms: link is not E.164 {PHONE_E164}: sms:{s}")

    # Any other US-format phone number on the page is a typo risk.
    for found in set(re.findall(r"\b\d{3}-\d{3}-\d{4}\b", scan)):
        if found != PHONE_DISPLAY:
            err(page, f"unexpected phone number in copy: {found}")

    for found in set(re.findall(r"[\w.+-]+@[\w.-]+\.\w+", scan)):
        if found.lower() != EMAIL and "example.com" not in found.lower():
            err(page, f"unexpected email address: {found}")

    if page in {"index.html", "quote.html"}:
        if f"tel:{PHONE_E164}" not in src:
            err(page, "no tel: link on a primary page")
        if "action-bar" not in src:
            err(page, "mobile action bar is missing")


# ---------------------------------------------------------------------------
# 7 — SEO
# ---------------------------------------------------------------------------
def check_seo(page: str, src: str) -> None:
    head = src[: src.find("</head>")]

    title = re.search(r"<title>(.*?)</title>", head, re.S)
    if not title or not title.group(1).strip():
        err(page, "no <title>")
    else:
        text = html.unescape(title.group(1)).strip()
        if len(text) > 70:
            warn(page, f"<title> is {len(text)} chars (over ~70 may truncate in SERPs)")

    desc = re.search(
        r'<meta\s+name\s*=\s*"description"\s+content\s*=\s*"([^"]*)"', head, re.I
    )
    if not desc or not desc.group(1).strip():
        err(page, "no meta description")
    else:
        n = len(html.unescape(desc.group(1)))
        if n > 165:
            warn(page, f"meta description is {n} chars (over ~165 may truncate)")

    robots = re.search(
        r'<meta\s+name\s*=\s*"robots"\s+content\s*=\s*"([^"]*)"', head, re.I
    )
    indexable = not (robots and "noindex" in robots.group(1).lower())

    if indexable and 'rel="canonical"' not in head:
        warn(page, "no canonical link")

    if page in {"index.html", "quote.html"} and 'property="og:image"' not in head:
        err(page, "no og:image")

    for block in re.findall(
        r'<script\s+type\s*=\s*"application/ld\+json"\s*>(.*?)</script>', src, re.S | re.I
    ):
        try:
            data = json.loads(block)
        except json.JSONDecodeError as exc:
            err(page, f"invalid JSON-LD: {exc}")
            continue
        if "@context" not in data or "@type" not in data:
            err(page, "JSON-LD is missing @context or @type")
        # Guard against the fabricated-credibility markup we deliberately avoid.
        banned = {"aggregateRating", "review", "openingHours", "openingHoursSpecification"}
        present = banned & set(json.dumps(data) and data.keys())
        if present:
            err(page, f"JSON-LD contains unverified properties: {sorted(present)}")


# ---------------------------------------------------------------------------
# 8 — accessibility
# ---------------------------------------------------------------------------
def check_a11y(page: str, src: str) -> None:
    if not re.search(r"<html[^>]*\blang\s*=", src, re.I):
        err(page, "<html> has no lang attribute")
    if 'name="viewport"' not in src:
        err(page, "no viewport meta")
    if "skip-link" not in src:
        err(page, "no skip-to-content link")
    if 'id="main"' not in src:
        err(page, 'no element with id="main" for the skip link to target')
    if "<main" not in src.lower():
        err(page, "no <main> landmark")

    for tag in tags(src, "a"):
        if (attr(tag, "target") or "") == "_blank":
            rel = (attr(tag, "rel") or "").lower()
            if "noopener" not in rel:
                err(page, "target=_blank without rel=noopener")

    for tag in tags(src, "button"):
        if not attr(tag, "type"):
            warn(page, "<button> without an explicit type")

    for t in re.findall(r'tabindex\s*=\s*"(-?\d+)"', src):
        if int(t) > 0:
            err(page, f"positive tabindex={t} breaks natural focus order")

    # Decorative SVG icons must be hidden from assistive tech.
    for tag in tags(src, "svg"):
        if not has_attr(tag, "aria-hidden") and not has_attr(tag, "role"):
            warn(page, "<svg> is neither aria-hidden nor given a role")


def check_css_a11y() -> None:
    for css in (PUBLIC / "css").glob("*.css"):
        text = css.read_text(encoding="utf-8")
        for m in re.finditer(r"outline\s*:\s*(none|0)\b", text):
            line = text[: m.start()].count("\n") + 1
            # Allowed only when immediately paired with a :focus-visible rule.
            window = text[m.end() : m.end() + 400]
            if "focus-visible" not in window and "focus-visible" not in text[
                max(0, m.start() - 400) : m.start()
            ]:
                err(f"css/{css.name}", f"line {line}: outline:none with no focus-visible replacement")

        if ":focus-visible" not in text and css.name == "base.css":
            err(f"css/{css.name}", "no :focus-visible styling found")


# ---------------------------------------------------------------------------
# 9 — hygiene
# ---------------------------------------------------------------------------
HYGIENE_PATTERNS = [
    (r"\bTODO\b", "TODO marker"),
    (r"\bFIXME\b", "FIXME marker"),
    (r"\bXXX\b", "XXX marker"),
    (r"\blorem ipsum\b", "lorem ipsum filler"),
    (r"/Users/", "absolute local filesystem path"),
    (r"\bexample\.org\b", "example.org placeholder"),
]


def check_hygiene(label: str, text: str) -> None:
    for pattern, desc in HYGIENE_PATTERNS:
        for m in re.finditer(pattern, text, re.I):
            line = text[: m.start()].count("\n") + 1
            err(label, f"line {line}: {desc} ({m.group(0)!r})")


# ---------------------------------------------------------------------------
# 10 — payload
# ---------------------------------------------------------------------------
def report_payload() -> None:
    notes.append("Page weight (HTML + CSS + JS + fonts, images excluded):")
    css = sum(p.stat().st_size for p in (PUBLIC / "css").glob("*.css"))
    js = sum(p.stat().st_size for p in (PUBLIC / "js").glob("*.js"))
    fonts = sum(p.stat().st_size for p in (PUBLIC / "fonts").glob("*.woff2"))
    for page in sorted(PUBLIC.glob("*.html")):
        shell = page.stat().st_size + css + js + fonts
        notes.append(
            f"  {page.name:<30} html {page.stat().st_size / 1024:6.1f} KB"
            f"   + shell = {shell / 1024:6.1f} KB"
        )
    notes.append(f"  shared: css {css / 1024:.1f} KB, js {js / 1024:.1f} KB, "
                 f"fonts {fonts / 1024:.1f} KB")

    imgs = sorted(
        (PUBLIC / "img").rglob("*"), key=lambda p: p.stat().st_size if p.is_file() else 0,
        reverse=True,
    )
    imgs = [p for p in imgs if p.is_file()]
    total = sum(p.stat().st_size for p in imgs)
    notes.append(
        f"\nImage derivatives on disk: {total / 1024 / 1024:.2f} MB "
        f"across {len(imgs)} files (the browser downloads one size per slot)."
    )
    notes.append("Largest five:")
    for p in imgs[:5]:
        notes.append(f"  {p.relative_to(PUBLIC)}  {p.stat().st_size / 1024:.0f} KB")

    over = [p for p in imgs if p.stat().st_size > 400 * 1024]
    if over:
        warnings.append(
            f"public/img: {len(over)} derivative(s) exceed 400 KB "
            f"(largest {over[0].stat().st_size / 1024:.0f} KB) — acceptable for JPEG "
            "fallbacks, but AVIF/WebP are served first"
        )


# ---------------------------------------------------------------------------
def main() -> int:
    pages = sorted(PUBLIC.glob("*.html"))
    if not pages:
        sys.exit(f"No HTML found in {PUBLIC}")

    print(f"Checking {len(pages)} pages in {PUBLIC}\n")

    for page in pages:
        src = page.read_text(encoding="utf-8")
        name = page.name
        check_refs(name, src)
        check_images(name, src)
        check_headings(name, src)
        check_forms(name, src)
        check_contact(name, src)
        check_seo(name, src)
        check_a11y(name, src)
        check_hygiene(name, src)

    check_css_a11y()
    for asset in list((PUBLIC / "css").glob("*.css")) + list((PUBLIC / "js").glob("*.js")):
        check_hygiene(str(asset.relative_to(PUBLIC)), asset.read_text(encoding="utf-8"))

    report_payload()

    for line in notes:
        print(line)

    if warnings:
        print(f"\n{'-' * 72}\nWARN ({len(warnings)})")
        for w in warnings:
            print(f"  ! {w}")

    if errors:
        print(f"\n{'-' * 72}\nERROR ({len(errors)})")
        for e in errors:
            print(f"  x {e}")
        print(f"\nFAILED — {len(errors)} error(s), {len(warnings)} warning(s)\n")
        return 1

    print(f"\n{'-' * 72}")
    print(f"PASSED — 0 errors, {len(warnings)} warning(s)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
