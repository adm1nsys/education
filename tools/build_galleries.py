#!/usr/bin/env python3
"""Generate an index.html gallery for every work folder listed in WORKS.

Images in each section are shown as a grid; any other files (PDF, DWG, AI, ...)
become download links. Texts are (German, English) pairs: German is written into
the page, English goes into data-en / data-en-html for assets/lang.js.
Run from anywhere: python3 tools/build_galleries.py
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES = {".jpg", ".jpeg", ".png", ".svg", ".webp"}
SKIP = {"index.html", ".DS_Store"}

# folder: (eyebrow, title, lead, [(subfolder or "", section title)]) — every text a (de, en) pair
WORKS = {
    "university/magazine-smart-home-living": (
        ("Kursarbeit · Künstlerische Gestaltung von Druckerzeugnissen · Okt – Dez 2024",
         "Coursework · Artistic design of print editions · Oct – Dec 2024"),
        ("Smart Home Living — Magazin", "Smart Home Living — magazine"),
        ("Ein Magazin über smarte Beleuchtung, von Grund auf gestaltet: Handskizzen, vier Layoutkonzepte und das finale "
         "20-seitige Layout auf einem Gestaltungsraster (berechnet mit meinem eigenen Rasterrechner).",
         "A magazine about smart lighting, designed from scratch: hand sketches, four layout concepts, "
         "then the final 20-page layout built on a modular grid (calculated with my own grid calculator)."),
        [("3-final", ("Finales Layout", "Final layout")),
         ("2-concepts/concept-2", ("Konzept 2", "Concept 2")), ("2-concepts/concept-3", ("Konzept 3", "Concept 3")),
         ("2-concepts/concept-4", ("Konzept 4", "Concept 4")), ("2-concepts/concept-5", ("Konzept 5", "Concept 5")),
         ("1-sketches/sketch-1", ("Skizze 1", "Sketch 1")), ("1-sketches/sketch-2", ("Skizze 2", "Sketch 2")),
         ("1-sketches/sketch-3", ("Skizze 3", "Sketch 3")), ("1-sketches/sketch-4", ("Skizze 4", "Sketch 4")),
         ("1-sketches/sketch-5", ("Skizze 5", "Sketch 5")), ("", ("Dateien", "Files"))],
    ),
    "university/posters": (
        ("Grafikdesign · Dez 2024", "Graphic design · Dec 2024"), ("Plakate & Infografiken", "Posters & infographics"),
        ("Charkiwer U-Bahn-Pläne als Infografik-Plakate neu gezeichnet und ein Plakat über Kyjiw.",
         "Kharkiv metro maps redrawn as infographic posters, and a poster about Kyiv."),
        [("", ("Plakate", "Posters"))]),
    "university/print-finishing": (
        ("Druckveredelung · Dez 2024", "Print finishing · Dec 2024"), ("Sonderfarben & Prägung", "Spot colors & embossing"),
        ("Labore zur Vorbereitung von Druckvorlagen für drei Sonderfarben und Prägung sowie ein Plakat aus der Kursarbeit. "
         "Die Vorschauen sind aus den Original-Illustrator-Dateien gerendert, die ebenfalls enthalten sind.",
         "Labs on preparing artwork for three spot colors and embossing, plus a coursework poster. "
         "Previews are rendered from the original Illustrator files, which are included."),
        [("previews", ("Vorschau", "Previews")), ("", ("Illustrator-Dateien", "Illustrator sources"))]),
    "university/web-design-figma": (
        ("Webdesign · Figma · Okt – Dez 2024", "Web design · Figma · Oct – Dec 2024"), ("Webdesign in Figma", "Web design in Figma"),
        ("Startseite einer mehrseitigen Website, zwei Fehlerseiten und ein Plakat.",
         "First page of a multi-page website, a pair of error pages and a poster."),
        [("site", ("Mehrseitige Website", "Multi-page website")), ("error-pages", ("Fehlerseiten 400 / 404", "Error pages 400 / 404")),
         ("", ("Plakat", "Poster"))]),
    "university/advertising": (
        ("Werbung · Sep 2024", "Advertising · Sep 2024"), ("Social-Media-Werbung", "Social media ads"),
        ("Posts und Stories für Instagram und Facebook für einen Elektronikhändler.",
         "A set of posts and stories for Instagram and Facebook for an electronics store."),
        [("", ("Posts und Stories", "Posts and stories"))]),
    "university/patterns": (
        ("Design · Sep 2024", "Design · Sep 2024"), ("Muster", "Patterns"),
        ("Drei Ornamentstudien.", "Three ornament studies."), [("", ("Muster", "Patterns"))]),
    "university/logo-mst": (
        ("Identity · Nov 2024", "Identity · Nov 2024"), ("Logo des Lehrstuhls", "Department logo"),
        ("Logo für den Lehrstuhl Mediensysteme und -technologien der NURE.", "Logo for the Media Systems and Technologies department of NURE."),
        [("", ("Logo", "Logo"))]),
    "university/color-science": (
        ("Farblehre · Mär – Mai 2025", "Color science · Mar – May 2025"), ("Labore Farblehre", "Color science labs"),
        ("Farbmusterstudien, ein Farbkreis und die Hermann-Gitter-Täuschung in RGB und CMYK, mit Anmerkungen zu jeder Variante.",
         "Swatch studies, a color wheel, and the Hermann grid illusion prepared in RGB and CMYK with notes on each variant."),
        [("lab-5", ("Labor 5 · Hermann-Gitter", "Lab 5 · Hermann grid illusion")), ("lab-4", ("Labor 4 · Farbkreis", "Lab 4 · color wheel")),
         ("swatches", ("Farbmusterstudien", "Swatch studies"))]),
    "university/technical-mechanics": (
        ("Technische Mechanik · Apr 2025", "Technical mechanics · Apr 2025"), ("Technische Mechanik", "Technical mechanics"),
        ("Eine technische Zeichnung in AutoCAD mit Erläuterung.", "A mechanical drawing in AutoCAD with its explanatory note."),
        [("", ("Dateien", "Files"))]),
    "college/computer-networks": (
        ("Computernetze · Arbeiten aus 2022 – 2023", "Computer networks · works from 2022 – 2023"),
        ("Kurs Computernetze", "Computer networks course"),
        ("Von Netzwerkhardware und TCP/IP bis zur Netzplanung in Cisco Packet Tracer: ein Büro-LAN, WLANs und ein "
         "Netzwerkprojekt für ein Unternehmen. Unten Screenshots, die vollständigen Berichte als PDF. "
         "Siehe auch: <a href='../network-security/'>Labor Netzwerksicherheit</a>.",
         "From network hardware and TCP/IP to designing networks in Cisco Packet Tracer: an office LAN, wireless networks "
         "and a network project for a company. Screenshots below; full reports as PDF. "
         "Related: <a href='../network-security/'>network security lab</a>."),
        [("screenshots/lab-9", ("Labor 9 · Büro-LAN", "Lab 9 · office LAN")),
         ("screenshots/lab-10", ("Labor 10 · WLAN", "Lab 10 · wireless network")),
         ("screenshots/lab-12", ("Labor 12 · Netzwerkgeräte", "Lab 12 · network equipment")),
         ("screenshots/practical-5", ("Übung 5 · Netzwerkprojekt für ein Unternehmen", "Practical 5 · company network project")),
         ("reports", ("Berichte", "Reports")), ("packet-tracer", ("Packet-Tracer-Datei", "Packet Tracer file"))]),
    "college/network-security": (
        ("Netzwerksicherheit · Feb 2024", "Network security · Feb 2024"), ("Netzwerksicherheit", "Network security"),
        ("Labor zum Aufbau geschützter virtueller Netze mit Firewalls.", "Lab on building protected virtual networks with firewalls."),
        [("", ("Bericht", "Report"))]),
}

PAGE = """<!doctype html>
<html lang="de" data-title-en="{title_en} · Education">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_de} · Ausbildung</title>
<link rel="icon" href="{up}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500&family=Roboto:wght@400;500&display=swap">
<link rel="stylesheet" href="{up}assets/gallery.css">
</head>
<body>
<div class="wrap page">
  <a class="back" href="{up}" data-en="← Overview">← Übersicht</a>
  {eyebrow}
  {title}
  {lead}
{sections}
</div>
<script src="{up}assets/lang.js"></script>
</body>
</html>
"""


def t(tag, pair, cls="", markup=False):
    de, en = pair
    c = f' class="{cls}"' if cls else ""
    attr = "data-en-html" if markup else "data-en"
    return f'<{tag}{c} {attr}="{html.escape(en, quote=True)}">{de if markup else html.escape(de)}</{tag}>'


def section(folder: Path, sub: str, heading) -> str:
    d = folder / sub if sub else folder
    if not d.is_dir():
        return ""
    files = sorted(p for p in d.iterdir() if p.is_file() and p.name not in SKIP and not p.name.startswith("."))
    if not files:
        return ""
    prefix = f"{sub}/" if sub else ""
    imgs = [f for f in files if f.suffix.lower() in IMAGES]
    other = [f for f in files if f.suffix.lower() not in IMAGES]
    out = ["  " + t("h2", heading)]
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
        (folder / "index.html").write_text(PAGE.format(
            title_de=html.escape(title[0]), title_en=html.escape(title[1], quote=True),
            eyebrow=t("div", eyebrow, "eyebrow"), title=t("h1", title), lead=t("p", lead, "lead", markup=True),
            sections=body, up=up), encoding="utf-8")
        print("wrote", rel + "/index.html")


if __name__ == "__main__":
    main()
