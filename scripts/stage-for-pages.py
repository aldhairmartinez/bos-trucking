#!/usr/bin/env python3
"""
Stage public/ for GitHub Pages deployment at a sub-path.

WHY THIS EXISTS
---------------
The website is authored with root-absolute paths (`/css/base.css`, `/img/...`,
`/quote.html`). That is correct for the eventual production setup, where the
site is served from the root of its own domain.

A GitHub Pages *project* site is served from a sub-path instead:

    https://<user>.github.io/bos-trucking/

Under that prefix every root-absolute path resolves to the wrong place and 404s.

Rather than rewrite the site to relative paths -- which would be the wrong shape
for production and would have to be undone later -- this script produces a
*copy* of public/ adjusted for the sub-path. It runs in CI only. Nothing in the
repository is modified, so `public/` stays deployable at a domain root exactly
as it is today.

WHAT IT DOES
------------
1. Rewrites the placeholder production host to the real deployment URL, which
   fixes canonical links, Open Graph tags, JSON-LD, robots.txt and sitemap.xml.
2. Prefixes every root-absolute href/src/srcset/data-* path with the base path.
3. Optionally marks the whole deployment `noindex` -- the right default for a
   temporary review URL, so it cannot compete with the real site in search or
   create duplicate-content problems.
4. Writes `.nojekyll` so GitHub never tries to process the output as a Jekyll
   site.

It is idempotent: paths already carrying the base prefix are left alone.

USAGE
-----
    python3 scripts/stage-for-pages.py \
        --base /bos-trucking \
        --site-url https://aldhairmartinez.github.io/bos-trucking \
        --out _site \
        --noindex
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

# The placeholder host used throughout the source while no domain is connected.
PLACEHOLDER_HOST = "https://bostruckingsite.com"

TEXT_SUFFIXES = {".html", ".css", ".js", ".json", ".xml", ".txt", ".webmanifest", ".svg"}

# Attributes whose value is a single URL.
URL_ATTRS = ("href", "src", "data-lightbox-src", "content", "action")

NOINDEX_TAG = (
    '<meta name="robots" content="noindex, nofollow">\n'
    "<!-- Temporary review deployment: kept out of search engines so it cannot\n"
    "     compete with the live site or create duplicate-content issues.\n"
    "     Injected at deploy time by scripts/stage-for-pages.py --noindex. -->"
)


def rewrite_single_urls(text: str, base: str) -> str:
    """Prefix root-absolute single-URL attribute values with `base`."""
    attr_group = "|".join(re.escape(a) for a in URL_ATTRS)
    # Match attr="/path" but not protocol-relative "//host" and not an already
    # prefixed path.
    pattern = re.compile(
        rf'(?P<attr>{attr_group})="(?P<url>/(?!/)[^"]*)"',
        re.IGNORECASE,
    )

    def repl(m: re.Match) -> str:
        url = m.group("url")
        if url.startswith(base + "/") or url == base:
            return m.group(0)
        return f'{m.group("attr")}="{base}{url}"'

    return pattern.sub(repl, text)


def rewrite_srcsets(text: str, base: str) -> str:
    """Prefix every root-absolute candidate inside a srcset list."""
    pattern = re.compile(r'srcset="(?P<val>[^"]*)"', re.IGNORECASE)

    def repl(m: re.Match) -> str:
        out = []
        for candidate in m.group("val").split(","):
            candidate = candidate.strip()
            if not candidate:
                continue
            bits = candidate.split()
            url = bits[0]
            if url.startswith("/") and not url.startswith("//"):
                if not (url.startswith(base + "/") or url == base):
                    url = base + url
            out.append(" ".join([url, *bits[1:]]))
        return 'srcset="' + ", ".join(out) + '"'

    return pattern.sub(repl, text)


def inject_noindex(text: str) -> str:
    """Add robots noindex, replacing any existing robots meta tag."""
    existing = re.compile(
        r'[ \t]*<meta\s+name="robots"[^>]*>\n?', re.IGNORECASE
    )
    if existing.search(text):
        return existing.sub(NOINDEX_TAG + "\n", text, count=1)
    return re.sub(
        r"(<meta\s+charset=[^>]*>)",
        r"\1\n" + NOINDEX_TAG,
        text,
        count=1,
        flags=re.IGNORECASE,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="", help='Sub-path, e.g. "/bos-trucking". "" = domain root')
    ap.add_argument("--site-url", default="", help="Full public URL, no trailing slash")
    ap.add_argument("--out", default="_site", help="Output directory")
    ap.add_argument("--noindex", action="store_true", help="Mark the deployment noindex")
    args = ap.parse_args()

    base = args.base.rstrip("/")
    if base and not base.startswith("/"):
        base = "/" + base

    if not PUBLIC.is_dir():
        sys.exit(f"Missing site directory: {PUBLIC}")

    out = ROOT / args.out
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(PUBLIC, out)

    changed = 0
    for path in sorted(out.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue

        original = path.read_text(encoding="utf-8")
        text = original

        if args.site_url:
            text = text.replace(PLACEHOLDER_HOST, args.site_url.rstrip("/"))

        if base:
            text = rewrite_srcsets(text, base)
            text = rewrite_single_urls(text, base)

        if args.noindex and path.suffix.lower() == ".html":
            text = inject_noindex(text)

        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
            print(f"  rewrote {path.relative_to(out)}")

    if args.noindex:
        (out / "robots.txt").write_text(
            "# Temporary review deployment — intentionally not indexed.\n"
            "User-agent: *\nDisallow: /\n",
            encoding="utf-8",
        )
        print("  robots.txt -> Disallow: /  (review deployment)")

    (out / ".nojekyll").touch()

    print(f"\nStaged {out.relative_to(ROOT)}/  ({changed} file(s) rewritten)")
    print(f"  base path : {base or '(domain root)'}")
    print(f"  site URL  : {args.site_url or '(unchanged placeholder)'}")
    print(f"  noindex   : {'yes' if args.noindex else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
