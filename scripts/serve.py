#!/usr/bin/env python3
"""
Local preview server for the B.O.S. Trucking & Site website.

Plain static files, no build step. Uses only the Python standard library, so
`npm install` is never required just to look at the site.

    python3 scripts/serve.py            # http://localhost:8080
    python3 scripts/serve.py 3000       # pick a port

Adds two things the bare http.server lacks:
  * Correct MIME types for .avif, .webp and .woff2 (older Pythons guess wrong,
    which silently breaks AVIF delivery and web fonts).
  * Clean URLs -- /quote serves public/quote.html, and unknown paths serve
    404.html with a real 404 status. This matches how Cloudflare Pages behaves,
    so what you review locally is what ships.
"""

from __future__ import annotations

import os
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "public"

EXTRA_TYPES = {
    ".avif": "image/avif",
    ".webp": "image/webp",
    ".woff2": "font/woff2",
    ".webmanifest": "application/manifest+json",
    ".svg": "image/svg+xml",
    ".json": "application/json",
}


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map, **EXTRA_TYPES}

    def send_response(self, code, message=None):
        super().send_response(code, message)
        # No caching locally, so design iterations show up on reload.
        self.send_header("Cache-Control", "no-store, must-revalidate")

    def translate_path(self, path: str) -> str:
        resolved = super().translate_path(path)
        p = Path(resolved)
        # Clean URL: /quote -> /quote.html
        if not p.exists() and not p.suffix:
            candidate = p.with_suffix(".html")
            if candidate.is_file():
                return str(candidate)
        return resolved

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            page = ROOT / "404.html"
            if page.is_file():
                body = page.read_bytes()
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                if self.command != "HEAD":
                    self.wfile.write(body)
                return
        super().send_error(code, message, explain)

    def log_message(self, fmt, *args):
        status = args[1] if len(args) > 1 else ""
        if status.startswith(("4", "5")):
            sys.stderr.write(f"  {status}  {args[0]}\n")


def main() -> int:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    if not ROOT.is_dir():
        sys.exit(f"Missing site directory: {ROOT}")
    os.chdir(ROOT)

    server = ThreadingHTTPServer(("127.0.0.1", port), partial(Handler, directory=str(ROOT)))
    print("\n  B.O.S. Trucking & Site — local preview")
    print(f"  http://localhost:{port}\n")
    print(f"  serving {ROOT}")
    print("  Ctrl+C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  stopped\n")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
