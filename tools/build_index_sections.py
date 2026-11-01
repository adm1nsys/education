#!/usr/bin/env python3
"""Rebuild the College and University sections of index.html from the data below.

Live demos open in a new tab; gallery pages inside this site open in place.
Run from anywhere: python3 tools/build_index_sections.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = "https://github.com/adm1nsys/student-works/tree/main/"
NEW_TAB = ' target="_blank" rel="noopener"'


def card(path, img, date, title, text, tags, links, shot="", featured=False, badge=None, orig=None, card_id=None, demo=False):
    """links: list of (label, href, opens_demo)"""
    tag_html = "".join(f'<span class="tag">{t}</span>' for t in tags)
    link_html = "".join(f'<a href="{h}"{NEW_TAB if d else ""}>{n}</a>' for n, h, d in links)
    link_html += f'<a href="{SRC}{path}"{NEW_TAB}>Source</a>'
    head = f'<span class="badge">{badge}</span>' if badge else f'<span class="date">{date}</span>'
    orig_html = f'\n          <div class="orig">{orig}</div>' if orig else ""
    cls = "card featured" if featured else "card"
    id_attr = f' id="{card_id}"' if card_id else ""
    shot_cls = f"shot {shot}".strip()
    return f'''      <article class="{cls}"{id_attr}>
        <a class="{shot_cls}" href="{path}/"{NEW_TAB if demo else ""}><img src="assets/previews/{img}" alt="{title}" loading="lazy"></a>
        <div class="body">
          {head}
          <h3>{title}</h3>{orig_html}
          <p>{text}</p>
          <div class="tags">{tag_html}</div>
          <div class="links">{link_html}</div>
        </div>
      </article>'''


def group(label, cards):
    return f'    <h3 class="group">{label}</h3>\n    <div class="grid">\n' + "\n\n".join(cards) + "\n    </div>"


C, U = "college/", "university/"

COLLEGE = [
    group("Projects", [
        card(C + "2024-diploma-micromouse", "diploma.jpg", "", "Micromouse maze editor",
             "A web page for building mazes for Micromouse robot competitions. The 16×16 field is split into 16 sectors; "
             "the generator picks a prepared 4×4 block for each one and assembles a full maze. Mazes can be drawn by hand, "
             "exported to JSON and imported back.",
             ["JavaScript", "jQuery", "JSON", "HTML/CSS"],
             [("Open generator", C + "2024-diploma-micromouse/", True), ("Draw a maze", C + "2024-diploma-micromouse/draw.html", True),
              ("Defence slides", C + "2024-diploma-micromouse/docs/presentation.pdf", True)],
             featured=True, badge="Diploma project · June 2024", orig="«Сторінка для створення лабіринтів»", card_id="diploma", demo=True),
        card(C + "2023-numeralogic", "numeralogic.jpg", "COURSEWORK · OCT – DEC 2023", "NumeraLogic",
             "Android calculator built in MIT App Inventor, plus its download site. The video shows the install flow on a real phone.",
             ["Android", "App Inventor", "HTML/CSS"],
             [("Watch demo", C + "2023-numeralogic/media/demo.mp4", True), ("Explanatory note", C + "2023-numeralogic/docs/explanatory-note.pdf", True),
              ("App Inventor source", C + "2023-numeralogic/app-inventor/NumeraLogic.aia", False)],
             shot="phone", demo=True),
    ]),
    group("Networks & systems", [
        card(C + "computer-networks", "computer-networks.jpg", "COMPUTER NETWORKS · 2022 – 2023", "Computer networks course",
             "Network hardware, TCP/IP, then designing networks in Cisco Packet Tracer: an office LAN, wireless networks, "
             "and a network project for a company. Reports, screenshots and a Packet Tracer file.",
             ["Cisco Packet Tracer", "TCP/IP", "LAN", "Wi-Fi"], [("Open", C + "computer-networks/", False), ("Security lab", C + "network-security/", False)]),
        card(C + "electronics", "electronics.jpg", "ELECTRONICS · 2022 – 2023", "Circuit design labs",
             "Logic gates, multiplexers and flip-flops simulated in Multisim, plus a PCB layout from practical training.",
             ["Multisim", "Sprint-Layout", "Digital logic"], [("Open", C + "electronics/", False)], shot="contain"),
    ]),
    group("Web programming", [
        card(C + "web-programming", "web-programming.jpg", "WEB PROGRAMMING · SEP 2023 – APR 2024", "Web programming course",
             "A year of classwork in one site: tables, layouts, forms with PHP, calculators, the 15-puzzle, jQuery, Vue and a "
             "multi-language page. Git history includes the in-class snapshots.",
             ["HTML/CSS", "JavaScript", "jQuery", "Vue", "PHP"],
             [("Open", C + "web-programming/", True), ("15-puzzle", C + "web-programming/15.html", True)], demo=True),
        card(C + "2023-calculator", "calculator.jpg", "FIRST LABS · FEB – DEC 2023", "First web labs",
             "Where it started: a title page for lab reports, lists, forms, a first JavaScript calculator and the “about me” page.",
             ["HTML", "CSS", "JavaScript"],
             [("Calculator", C + "2023-calculator/", True), ("Form", C + "2023-form/", True), ("List", C + "2023-list/", True),
              ("Title page", C + "2023-lab-title/", True), ("About me", C + "2023-about-me/", True)], demo=True),
    ]),
]

UNIVERSITY = [
    group("Spring 2025", [
        card(U + "technical-mechanics", "technical-mechanics.jpg", "TECHNICAL MECHANICS · APR 2025", "Technical mechanics",
             "A mechanical drawing in AutoCAD with a full explanatory note.", ["AutoCAD", "DWG"], [("Open", U + "technical-mechanics/", False)], shot="contain"),
        card(U + "color-science", "color-science.jpg", "COLOR SCIENCE · MAR – MAY 2025", "Color science labs",
             "Hermann grid illusion prepared for RGB and CMYK, a color wheel and swatch studies.", ["Illustrator", "RGB/CMYK"], [("Open", U + "color-science/", False)]),
        card(U + "raster-imaging", "raster-imaging.jpg", "RASTER IMAGING · MAR 2025", "Raster imaging labs",
             "Scanned halftone and screen-ruling measurements.", ["Scanning", "Halftone"], [("Open", U + "raster-imaging/", False)]),
    ]),
    group("Autumn 2024", [
        card(U + "magazine-smart-home-living", "magazine.jpg", "", "Smart Home Living",
             "A magazine about smart lighting: hand sketches, four layout concepts, final layout on a modular grid — the grid "
             "was calculated with my own tool below.",
             ["Illustrator", "Figma", "Layout", "Print"],
             [("Look inside", U + "magazine-smart-home-living/", False), ("PDF", U + "magazine-smart-home-living/smart-home-living.pdf", True)],
             featured=True, badge="Coursework · Dec 2024", orig="«Художнє оформлення поліграфічних видань»"),
        card(U + "grid-calculator", "grid-calculator.jpg", "TOOL · NOV 2024", "Modular grid calculator",
             "Built for the magazine above: enter page size, columns, rows and gutters — get the module size.",
             ["JavaScript", "Layout"], [("Open", U + "grid-calculator/", True)], demo=True),
        card(U + "print-finishing", "print-finishing.jpg", "PRINT FINISHING · DEC 2024", "Spot colors & embossing",
             "Artwork prepared for three spot colors and embossing, and an art prize poster.", ["Illustrator", "Prepress"], [("Open", U + "print-finishing/", False)], shot="contain"),
        card(U + "posters", "posters.jpg", "GRAPHIC DESIGN · DEC 2024", "Posters & infographics",
             "Kharkiv metro maps as infographic posters, and a poster about Kyiv.", ["Illustrator", "Infographics"], [("Open", U + "posters/", False)], shot="contain"),
        card(U + "web-design-figma", "web-design-figma.jpg", "WEB DESIGN · OCT – DEC 2024", "Web design in Figma",
             "First page of a multi-page site, 400 / 404 error pages and a poster.", ["Figma", "UI"], [("Open", U + "web-design-figma/", False)]),
        card(U + "logo-mst", "logo-mst.jpg", "IDENTITY · NOV 2024", "Department logo",
             "Logo for the Media Systems and Technologies department.", ["Illustrator", "Identity"], [("Open", U + "logo-mst/", False)], shot="contain"),
        card(U + "type-design", "type-design.jpg", "TYPE DESIGN · SEP 2024", "Modified Courier New",
             "First type-design lab in FontLab: editing glyphs of an existing typeface.", ["FontLab", "TTF"], [("Specimen", U + "type-design/specimen.html", True)]),
        card(U + "advertising", "advertising.jpg", "ADVERTISING · SEP 2024", "Social media ads",
             "Posts and stories for Instagram and Facebook.", ["Figma", "Social"], [("Open", U + "advertising/", False)]),
        card(U + "patterns", "patterns.jpg", "DESIGN · SEP 2024", "Patterns", "Three ornament studies.", ["Illustrator"], [("Open", U + "patterns/", False)], shot="contain"),
    ]),
    group("Spring 2024", [
        card(U + "sticker-pack", "sticker-pack.jpg", "DESIGN · MAR 2024", "Sticker pack",
             "A sticker series drawn in Illustrator, with a poster, QR code and download page.", ["Illustrator", "Figma", "HTML"],
             [("Poster", U + "sticker-pack/Pack/Artboard%201.pdf", True), ("Download page", U + "sticker-pack/", True)], demo=True),
    ]),
    group("Autumn 2023 – Spring 2024", [
        card(U + "engineering-graphics", "eg-main.jpg", "ENGINEERING GRAPHICS · OCT 2023 – JUN 2024", "AutoCAD drawings",
             "Two semesters of engineering graphics: labs, calculation-graphic tasks, tests and the exam — every sheet as PDF and original DWG.",
             ["AutoCAD", "DWG"], [("All drawings", U + "engineering-graphics/", False)], shot="contain"),
    ]),
]


def section(sid, eyebrow, title, desc, groups):
    return f'''  <section class="block" id="{sid}">
    <div class="block-head">
      <div class="eyebrow">{eyebrow}</div>
      <h2>{title}</h2>
      <p>{desc}</p>
    </div>
''' + "\n\n".join(groups) + "\n  </section>"


def main() -> None:
    p = ROOT / "index.html"
    s = p.read_text(encoding="utf-8")
    college = section("college", "College · works from 2022 – 2024", "Kharkiv Professional College of Information Technologies",
                      "Separate structural unit of the National Aerospace University “Kharkiv Aviation Institute”. Specialty 172 "
                      "Telecommunications and Radio Engineering. Groups МЗ-21 → МЗ-31.", COLLEGE)
    university = section("university", "University · works from 2023 – 2025", "Kharkiv National University of Radio Electronics",
                         "Publishing and printing, group ВПВПС-23-2. Layout, print production, color, type and engineering graphics.", UNIVERSITY)
    s = re.sub(r'  <section class="block" id="college">.*?\n  </section>', lambda m: college, s, count=1, flags=re.S)
    s = re.sub(r'  <section class="block" id="university">.*?\n  </section>', lambda m: university, s, count=1, flags=re.S)
    p.write_text(s, encoding="utf-8")
    print("cards:", s.count("<article"))


if __name__ == "__main__":
    main()
