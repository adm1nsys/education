#!/usr/bin/env python3
"""Fail if a page of the showcase site links to a local file that does not exist.

Only the site's own pages are checked (the main page and the gallery pages); the student
works themselves are kept as they were submitted. Run: python3 tools/check_links.py
"""
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_PREFIXES = ("http:", "https:", "mailto:", "data:", "javascript:")
# pages written for the site, not the original coursework
SITE_PAGES = ["index.html", "university/engineering-graphics/index.html"]


def gallery_pages():
    sys.path.insert(0, str(ROOT / "tools"))
    from build_galleries import WORKS  # noqa: E402
    return [f"{rel}/index.html" for rel in WORKS]


def main() -> int:
    broken = 0
    for rel in SITE_PAGES + gallery_pages():
        page = ROOT / rel
        for link in re.findall(r'(?:href|src)="([^"#]+)"', page.read_text(encoding="utf-8")):
            if link.startswith(SKIP_PREFIXES):
                continue
            target = (page.parent / urllib.parse.unquote(link.split("?")[0])).resolve()
            if link.endswith("/"):
                target /= "index.html"
            if not target.exists():
                print(f"broken link in {rel}: {link}")
                broken += 1
    print(f"checked {len(SITE_PAGES) + len(gallery_pages())} pages, {broken} broken links")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
