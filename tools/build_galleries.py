#!/usr/bin/env python3
"""Generate an index.html gallery for every work folder listed in WORKS.

Images in each section are shown as a grid; any other files (PDF, DWG, AI, ...)
become download links. Run from anywhere: python3 tools/build_galleries.py
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES = {".jpg", ".jpeg", ".png", ".svg", ".webp"}
SKIP = {"index.html", ".DS_Store"}

# folder: (eyebrow, title, lead, [(subfolder or "", section title)])
WORKS = {
    "university/magazine-smart-home-living": (
        "Coursework · Artistic design of print editions · Oct – Dec 2024",
        "Smart Home Living — magazine",
        "A magazine about smart lighting, designed from scratch: hand sketches, four layout concepts, "
        "then the final 21-page layout built on a modular grid (calculated with my own grid calculator).",
        [("3-final", "Final layout"), ("2-concepts/concept-2", "Concept 2"), ("2-concepts/concept-3", "Concept 3"),
         ("2-concepts/concept-4", "Concept 4"), ("2-concepts/concept-5", "Concept 5"),
         ("1-sketches/sketch-1", "Sketch 1"), ("1-sketches/sketch-2", "Sketch 2"), ("1-sketches/sketch-3", "Sketch 3"),
         ("1-sketches/sketch-4", "Sketch 4"), ("1-sketches/sketch-5", "Sketch 5"), ("", "Files")],
    ),
    "university/posters": (
        "Graphic design · Dec 2024", "Posters & infographics",
        "Kharkiv metro maps redrawn as infographic posters, and a poster about Kyiv.", [("", "Posters")]),
    "university/print-finishing": (
        "Print finishing · Dec 2024", "Spot colors & embossing",
        "Labs on preparing artwork for three spot colors and embossing, plus a coursework poster. "
        "Previews are rendered from the original Illustrator files, which are included.",
        [("previews", "Previews"), ("", "Illustrator sources")]),
    "university/web-design-figma": (
        "Web design · Figma · Oct – Dec 2024", "Web design in Figma",
        "First page of a multi-page website, a pair of error pages and a poster.",
        [("site", "Multi-page website"), ("error-pages", "Error pages 400 / 404"), ("", "Poster")]),
    "university/advertising": (
        "Advertising · Sep 2024", "Social media ads",
        "A set of posts and stories for Instagram and Facebook for an electronics store.", [("", "Posts and stories")]),
    "university/patterns": (
        "Design · Sep 2024", "Patterns", "Three ornament studies.", [("", "Patterns")]),
    "university/logo-mst": (
        "Identity · Nov 2024", "Department logo",
        "Logo for the Media Systems and Technologies department of NURE.", [("", "Logo")]),
    "university/color-science": (
        "Color science · Mar – May 2025", "Color science labs",
        "Swatch studies, a color wheel, and the Hermann grid illusion prepared in RGB and CMYK with notes on each variant.",
        [("lab-5", "Lab 5 · Hermann grid illusion"), ("lab-4", "Lab 4 · color wheel"), ("swatches", "Swatch studies")]),
    "university/technical-mechanics": (
        "Technical mechanics · Apr 2025", "Technical mechanics",
        "A mechanical drawing in AutoCAD with its explanatory note.", [("", "Files")]),
    "college/computer-networks": (
        "Computer networks · works from 2022 – 2023", "Computer networks course",
        "From network hardware and TCP/IP to designing networks in Cisco Packet Tracer: an office LAN, wireless networks "
        "and a network project for a company. Screenshots below; full reports as PDF. "
        "Related: <a href='../network-security/'>network security lab</a>.",
        [("screenshots/lab-9", "Lab 9 · office LAN"), ("screenshots/lab-10", "Lab 10 · wireless network"),
         ("screenshots/lab-12", "Lab 12 · network equipment"), ("screenshots/practical-5", "Practical 5 · company network project"),
         ("reports", "Reports"), ("packet-tracer", "Packet Tracer file")]),
    "college/network-security": (
        "Network security · Feb 2024", "Network security",
        "Lab on building protected virtual networks with firewalls.", [("", "Report")]),
}

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Education</title>
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{up}assets/gallery.css">
</head>
<body>
<div class="wrap">
  <a class="back" href="{up}">← Education</a>
  <div class="eyebrow">{eyebrow}</div>
  <h1>{title}</h1>
  <p class="lead">{lead}</p>
{sections}
</div>
</body>
</html>
"""


def section(folder: Path, sub: str, heading: str) -> str:
    d = folder / sub if sub else folder
    if not d.is_dir():
        return ""
    files = sorted(p for p in d.iterdir() if p.is_file() and p.name not in SKIP and not p.name.startswith("."))
    if not files:
        return ""
    prefix = f"{sub}/" if sub else ""
    imgs = [f for f in files if f.suffix.lower() in IMAGES]
    other = [f for f in files if f.suffix.lower() not in IMAGES]
    out = [f"  <h2>{html.escape(heading)}</h2>"]
    if imgs:
        out.append('  <div class="grid">')
        for f in imgs:
            href = html.escape(prefix + f.name)
            out.append(f'    <a class="tile" href="{href}"><img src="{href}" alt="{html.escape(f.stem)}" loading="lazy"></a>')
        out.append("  </div>")
    if other:
        out.append('  <ul class="files">')
        for f in other:
            size = f.stat().st_size / 1024
            size_s = f"{size / 1024:.1f} MB" if size > 1024 else f"{size:.0f} KB"
            out.append(f'    <li><a href="{html.escape(prefix + f.name)}">{html.escape(f.name)}</a><span>{size_s}</span></li>')
        out.append("  </ul>")
    return "\n".join(out)


def main() -> None:
    for rel, (eyebrow, title, lead, sections) in WORKS.items():
        folder = ROOT / rel
        up = "../" * len(Path(rel).parts)
        body = "\n".join(s for s in (section(folder, sub, h) for sub, h in sections) if s)
        (folder / "index.html").write_text(
            PAGE.format(title=html.escape(title), eyebrow=html.escape(eyebrow), lead=lead, sections=body, up=up),
            encoding="utf-8")
        print("wrote", rel + "/index.html")


if __name__ == "__main__":
    main()
