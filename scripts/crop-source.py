#!/usr/bin/env python3
"""
Stage 1 of 2 — lossless source preparation.

Reads assets/sources.json and turns the untouched originals in assets/originals/
into clean, lossless masters:

    assets/originals/  (never modified)
        -> assets/masters/    photographic masters, letterbox + overlay removed
        -> assets/brand/      logo art, pure black keyed to transparent
        -> assets/reference/  marketing flyers, for reference only, never shipped

Nothing here is resized or lossily compressed. Stage 2 (build-images.py) turns
these masters into the responsive AVIF/WebP/JPEG derivatives the site serves.

Usage:  python3 scripts/crop-source.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required:  python3 -m pip install --user Pillow")

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
MANIFEST = ASSETS / "sources.json"

MASTERS = ASSETS / "masters"
BRAND = ASSETS / "brand"
REFERENCE = ASSETS / "reference"

# Pixels at or below this value on every channel are treated as the logo's
# black backing plate and keyed to transparent. The logo art itself is white
# (#FEFEFE) and yellow (#F8B804), so there is a very wide margin here.
BLACK_KEY_THRESHOLD = 26


def load_manifest() -> dict:
    with MANIFEST.open(encoding="utf-8") as fh:
        return json.load(fh)


def open_source(rel: str) -> Image.Image:
    path = ASSETS / rel
    if not path.exists():
        sys.exit(f"Source not found: {path}")
    return Image.open(path)


def key_black_to_alpha(img: Image.Image) -> Image.Image:
    """Make the logo's solid black backing plate transparent.

    The site is entirely dark-surfaced, so a transparent logo lets the same
    asset sit on #0A0A0A, #141414 and photographic overlays without a visible
    rectangle. Alpha ramps smoothly over the threshold so antialiased edges on
    the logo artwork stay clean instead of going crunchy.
    """
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    t = BLACK_KEY_THRESHOLD
    for y in range(h):
        for x in range(w):
            r, g, b, _ = px[x, y]
            peak = max(r, g, b)
            if peak <= t:
                px[x, y] = (r, g, b, 0)
            elif peak <= t * 3:
                # Smooth ramp out of the keyed region.
                a = int(255 * (peak - t) / (t * 2))
                px[x, y] = (r, g, b, a)
    return img


def trim_transparent(img: Image.Image) -> Image.Image:
    bbox = img.getbbox()
    return img.crop(bbox) if bbox else img


def prep_photographic(key: str, spec: dict) -> Path | None:
    src = spec.get("file")
    if not src:
        return None
    img = open_source(src)
    crop = spec.get("crop")
    if crop:
        img = img.crop(tuple(crop))
    out = MASTERS / f"{key}.png"
    img.convert("RGB").save(out, "PNG", optimize=True)
    print(f"  master   {key:<22} {img.size[0]}x{img.size[1]}")
    return out


def prep_brand(key: str, spec: dict) -> Path | None:
    src = spec.get("file")
    if not src:
        return None
    img = open_source(src)
    crop = spec.get("crop")
    if crop:
        img = img.crop(tuple(crop))

    # As-supplied version, on its original black plate.
    on_black = BRAND / f"{key}-on-black.png"
    img.convert("RGB").save(on_black, "PNG", optimize=True)

    # Transparent version for use over the site's dark surfaces.
    alpha = trim_transparent(key_black_to_alpha(img))
    out = BRAND / f"{key}.png"
    alpha.save(out, "PNG", optimize=True)
    print(f"  brand    {key:<22} {alpha.size[0]}x{alpha.size[1]} (alpha) "
          f"+ {key}-on-black.png")
    return out


def prep_reference(key: str, spec: dict) -> None:
    src = spec.get("file")
    if not src:
        return
    img = open_source(src)
    crop = spec.get("crop")
    if crop:
        img = img.crop(tuple(crop))
    out = REFERENCE / f"{key}.png"
    img.convert("RGB").save(out, "PNG", optimize=True)
    print(f"  ref      {key:<22} {img.size[0]}x{img.size[1]}")


def main() -> int:
    data = load_manifest()
    for d in (MASTERS, BRAND, REFERENCE):
        d.mkdir(parents=True, exist_ok=True)

    print("Preparing lossless masters from untouched originals\n")

    print("Photographs and logos:")
    for key, spec in data["images"].items():
        if spec.get("alpha"):
            prep_brand(key, spec)
        else:
            prep_photographic(key, spec)

    print("\nMarketing flyers (reference only, never shipped):")
    for key, spec in data["reference_only"].items():
        if key.startswith("_"):
            continue
        prep_reference(key, spec)

    print("\nDone. Originals in assets/originals/ were not modified.")
    print("Next:  python3 scripts/build-images.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
