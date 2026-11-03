#!/usr/bin/env python3
"""Rebuild the College and University sections of index.html from the data below.

Every visible text is a (German, English) pair: German is written into the page,
English goes into data-en for assets/lang.js. Live demos open in a new tab;
gallery pages inside this site open in place.
Run from anywhere: python3 tools/build_index_sections.py
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = "https://github.com/adm1nsys/education/tree/main/"
NEW_TAB = ' target="_blank" rel="noopener"'


def t(tag, pair, cls=""):
    """Element with German content and its English twin in data-en."""
    de, en = pair
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c} data-en="{html.escape(en, quote=True)}">{de}</{tag}>'


def card(path, img, date, title, text, tags, links, shot="", featured=False, badge=None, orig=None, card_id=None, demo=False):
    """title is shared by both languages when given as a plain string; links: (pair, href, opens_demo)"""
    title = title if isinstance(title, tuple) else (title, title)
    tag_html = "".join(f'<span class="tag">{x}</span>' for x in tags)
    link_html = "".join(
        f'<a href="{h}"{NEW_TAB if d else ""} data-en="{html.escape(n[1], quote=True)}">{n[0]}</a>' for n, h, d in links)
    link_html += f'<a href="{SRC}{path}"{NEW_TAB} data-en="Source">Quellcode</a>'
    head = t("span", badge, "badge") if badge else t("span", date, "date")
    orig_html = f'\n          <div class="orig">{orig}</div>' if orig else ""
    cls = "card featured" if featured else "card"
    id_attr = f' id="{card_id}"' if card_id else ""
    shot_cls = f"shot {shot}".strip()
    return f'''      <article class="{cls}"{id_attr}>
        <a class="{shot_cls}" href="{path}/"{NEW_TAB if demo else ""}><img src="assets/previews/{img}" alt="{html.escape(title[1])}" loading="lazy"></a>
        <div class="body">
          {head}
          {t("h3", title)}{orig_html}
          {t("p", text)}
          <div class="tags">{tag_html}</div>
          <div class="links">{link_html}</div>
        </div>
      </article>'''


def group(label, cards):
    return f'    {t("h3", label, "group")}\n    <div class="grid">\n' + "\n\n".join(cards) + "\n    </div>"


C, U = "college/", "university/"
OPEN = ("Öffnen", "Open")

COLLEGE = [
    group(("Projekte", "Projects"), [
        card(C + "2024-diploma-micromouse", "diploma.jpg", None, ("Labyrinth-Editor für Micromouse", "Micromouse maze editor"),
             ("Eine Webanwendung zum Erstellen von Labyrinthen für Micromouse-Roboterwettbewerbe. Das 16×16-Feld ist in 16 Sektoren "
              "geteilt; der Generator wählt für jeden einen vorbereiteten 4×4-Block und setzt daraus ein vollständiges Labyrinth "
              "zusammen. Labyrinthe lassen sich auch von Hand zeichnen, als JSON exportieren und wieder importieren.",
              "A web page for building mazes for Micromouse robot competitions. The 16×16 field is split into 16 sectors; "
              "the generator picks a prepared 4×4 block for each one and assembles a full maze. Mazes can be drawn by hand, "
              "exported to JSON and imported back."),
             ["JavaScript", "jQuery", "JSON", "HTML/CSS"],
             [(("Generator öffnen", "Open generator"), C + "2024-diploma-micromouse/", True),
              (("Labyrinth zeichnen", "Draw a maze"), C + "2024-diploma-micromouse/draw.html", True)],
             featured=True, badge=("Abschlussprojekt · Juni 2024", "Diploma project · June 2024"),
             orig="«Сторінка для створення лабіринтів»", card_id="diploma", demo=True),
        card(C + "2023-numeralogic", "numeralogic.jpg", ("KURSARBEIT · OKT – DEZ 2023", "COURSEWORK · OCT – DEC 2023"), "NumeraLogic",
             ("Android-Taschenrechner in MIT App Inventor, dazu eine Download-Seite. Das Video zeigt die Installation auf einem echten Smartphone.",
              "Android calculator built in MIT App Inventor, plus its download site. The video shows the install flow on a real phone."),
             ["Android", "App Inventor", "HTML/CSS"],
             [(("Demo ansehen", "Watch demo"), C + "2023-numeralogic/media/demo.mp4", True),
              (("Erläuterung (PDF)", "Explanatory note"), C + "2023-numeralogic/docs/explanatory-note.pdf", True),
              (("App-Inventor-Quelle", "App Inventor source"), C + "2023-numeralogic/app-inventor/NumeraLogic.aia", False)],
             shot="phone", demo=True),
    ]),
    group(("Netzwerke & Systeme", "Networks & systems"), [
        card(C + "computer-networks", "computer-networks.jpg", ("COMPUTERNETZE · 2022 – 2023", "COMPUTER NETWORKS · 2022 – 2023"),
             ("Kurs Computernetze", "Computer networks course"),
             ("Netzwerkhardware und TCP/IP, dann Netzplanung in Cisco Packet Tracer: ein Büro-LAN, WLANs und ein Netzwerkprojekt "
              "für ein Unternehmen. Berichte, Screenshots und eine Packet-Tracer-Datei.",
              "Network hardware, TCP/IP, then designing networks in Cisco Packet Tracer: an office LAN, wireless networks, "
              "and a network project for a company. Reports, screenshots and a Packet Tracer file."),
             ["Cisco Packet Tracer", "TCP/IP", "LAN", "WLAN"],
             [(OPEN, C + "computer-networks/", False), (("Labor Netzwerksicherheit", "Security lab"), C + "network-security/", False)]),
    ]),
    group(("Webprogrammierung", "Web programming"), [
        card(C + "web-programming", "web-programming.jpg", ("WEBPROGRAMMIERUNG · SEP 2023 – APR 2024", "WEB PROGRAMMING · SEP 2023 – APR 2024"),
             ("Kurs Webprogrammierung", "Web programming course"),
             ("Ein Jahr Unterricht auf einer Website: Tabellen, Layouts, Formulare mit PHP, Rechner, das 15er-Puzzle, jQuery, Vue "
              "und eine mehrsprachige Seite. Die Git-Historie enthält die Stände aus dem Unterricht.",
              "A year of classwork in one site: tables, layouts, forms with PHP, calculators, the 15-puzzle, jQuery, Vue and a "
              "multi-language page. Git history includes the in-class snapshots."),
             ["HTML/CSS", "JavaScript", "jQuery", "Vue", "PHP"],
             [(OPEN, C + "web-programming/", True), (("15er-Puzzle", "15-puzzle"), C + "web-programming/15.html", True)], demo=True),
        card(C + "2023-calculator", "calculator.jpg", ("ERSTES LABOR · MAI 2023", "FIRST LAB · MAY 2023"),
             ("Erster JavaScript-Rechner", "First JavaScript calculator"),
             ("Hier fing es an: meine erste JavaScript-Laborarbeit, ein Rechner mit eigenem Design.",
              "Where it started: my first JavaScript lab, a calculator with its own design."),
             ["JavaScript", "CSS"], [(OPEN, C + "2023-calculator/", True)], demo=True),
    ]),
]

UNIVERSITY = [
    group(("AutoCAD & technisches Zeichnen", "AutoCAD & technical drawing"), [
        card(U + "engineering-graphics", "eg-main.jpg", None, ("Ingenieurgrafik in AutoCAD", "Engineering graphics in AutoCAD"),
             ("Zwei Semester technisches Zeichnen: Projektionen, Schnitte und 3D-Modelle von Bauteilen, Belegaufgaben, Tests und "
              "die Prüfung — jedes Blatt als PDF und Original-DWG. Der Herbstkurs war Teil des Projekts HHN-DITO II der Hochschule Heilbronn.",
              "Two semesters of technical drawing: projections, sections and 3D models of parts, calculation-graphic tasks, "
              "tests and the exam — every sheet as PDF and original DWG. The autumn course was part of the HHN-DITO II "
              "project of Heilbronn University of Applied Sciences."),
             ["AutoCAD", "DWG", "3D", ("Technisches Zeichnen")],
             [(("Alle Zeichnungen", "All drawings"), U + "engineering-graphics/", False),
              (("Zertifikat", "Certificate"), U + "engineering-graphics/certificate-hhn-daad.pdf", True)],
             shot="contain", featured=True, badge=("Zwei Semester · Sep 2023 – Jun 2024", "Two semesters · Sep 2023 – Jun 2024"), card_id="autocad"),
        card(U + "engineering-graphics", "certificate.jpg", ("ZERTIFIKAT · APR 2024", "CERTIFICATE · APR 2024"),
             ("Teilnahmezertifikat", "Certificate of participation"),
             ("51-stündiger Kurs „Engineering and Computer Graphics“ (Sep – Dez 2023) im Projekt HHN-DITO II der Hochschule "
              "Heilbronn, gefördert vom DAAD aus Mitteln des Bundesministeriums für Bildung und Forschung.",
              "51-hour course “Engineering and Computer Graphics” (Sep – Dec 2023) within the HHN-DITO II project of "
              "Heilbronn University of Applied Sciences, funded by the DAAD and the German Federal Ministry of Education and Research."),
             ["DAAD", "Hochschule Heilbronn", "BMBF"],
             [(("Zertifikat öffnen", "Open certificate"), U + "engineering-graphics/certificate-hhn-daad.pdf", True)], shot="cert", card_id="certificate"),
        card(U + "technical-mechanics", "technical-mechanics.jpg", ("TECHNISCHE MECHANIK · APR 2025", "TECHNICAL MECHANICS · APR 2025"),
             ("Technische Mechanik", "Technical mechanics"),
             ("Eine technische Zeichnung in AutoCAD mit vollständiger Erläuterung.", "A mechanical drawing in AutoCAD with a full explanatory note."),
             ["AutoCAD", "DWG"], [(OPEN, U + "technical-mechanics/", False)], shot="contain"),
    ]),
    group(("Layout & Druck", "Layout & print"), [
        card(U + "magazine-smart-home-living", "magazine.jpg", None, "Smart Home Living",
             ("Ein Magazin über smarte Beleuchtung: Handskizzen, vier Layoutkonzepte, finales Layout auf einem Gestaltungsraster — "
              "das Raster habe ich mit meinem eigenen Rechner (unten) berechnet.",
              "A magazine about smart lighting: hand sketches, four layout concepts, final layout on a modular grid — the grid "
              "was calculated with my own tool below."),
             ["Illustrator", "Figma", "Layout", "Print"],
             [(("Durchblättern", "Look inside"), U + "magazine-smart-home-living/", False),
              (("PDF", "PDF"), U + "magazine-smart-home-living/smart-home-living.pdf", True)],
             featured=True, badge=("Kursarbeit · Dez 2024", "Coursework · Dec 2024"), orig="«Художнє оформлення поліграфічних видань»"),
        card(U + "grid-calculator", "grid-calculator.jpg", ("WERKZEUG · NOV 2024", "TOOL · NOV 2024"),
             ("Rasterrechner", "Modular grid calculator"),
             ("Für das Magazin oben gebaut: Seitenformat, Spalten, Zeilen und Abstände eingeben — Modulgröße erhalten.",
              "Built for the magazine above: enter page size, columns, rows and gutters — get the module size."),
             ["JavaScript", "Layout"], [(OPEN, U + "grid-calculator/", True)], demo=True),
        card(U + "print-finishing", "print-finishing.jpg", ("DRUCKVEREDELUNG · DEZ 2024", "PRINT FINISHING · DEC 2024"),
             ("Sonderfarben & Prägung", "Spot colors & embossing"),
             ("Druckvorlagen für drei Sonderfarben und Prägung sowie ein Plakat für einen Kunstpreis.",
              "Artwork prepared for three spot colors and embossing, and an art prize poster."),
             ["Illustrator", "Prepress"], [(OPEN, U + "print-finishing/", False)], shot="contain"),
        card(U + "color-science", "color-science.jpg", ("FARBLEHRE · MÄR – MAI 2025", "COLOR SCIENCE · MAR – MAY 2025"),
             ("Labore Farblehre", "Color science labs"),
             ("Hermann-Gitter-Täuschung für RGB und CMYK aufbereitet, ein Farbkreis und Farbmusterstudien.",
              "Hermann grid illusion prepared for RGB and CMYK, a color wheel and swatch studies."),
             ["Illustrator", "RGB/CMYK"], [(OPEN, U + "color-science/", False)]),
        card(U + "posters", "posters.jpg", ("GRAFIKDESIGN · DEZ 2024", "GRAPHIC DESIGN · DEC 2024"),
             ("Plakate & Infografiken", "Posters & infographics"),
             ("Charkiwer U-Bahn-Pläne als Infografik-Plakate und ein Plakat über Kyjiw.",
              "Kharkiv metro maps as infographic posters, and a poster about Kyiv."),
             ["Illustrator", "Infografik"], [(OPEN, U + "posters/", False)], shot="contain"),
    ]),
    group(("Design", "Design"), [
        card(U + "web-design-figma", "web-design-figma.jpg", ("WEBDESIGN · OKT – DEZ 2024", "WEB DESIGN · OCT – DEC 2024"),
             ("Webdesign in Figma", "Web design in Figma"),
             ("Startseite einer mehrseitigen Website, Fehlerseiten 400 / 404 und ein Plakat.",
              "First page of a multi-page site, 400 / 404 error pages and a poster."),
             ["Figma", "UI"], [(OPEN, U + "web-design-figma/", False)]),
        card(U + "logo-mst", "logo-mst.jpg", ("IDENTITY · NOV 2024", "IDENTITY · NOV 2024"),
             ("Logo des Lehrstuhls", "Department logo"),
             ("Logo für den Lehrstuhl Mediensysteme und -technologien.", "Logo for the Media Systems and Technologies department."),
             ["Illustrator", "Identity"], [(OPEN, U + "logo-mst/", False)], shot="contain"),
        card(U + "advertising", "advertising.jpg", ("WERBUNG · SEP 2024", "ADVERTISING · SEP 2024"),
             ("Social-Media-Werbung", "Social media ads"),
             ("Posts und Stories für Instagram und Facebook.", "Posts and stories for Instagram and Facebook."),
             ["Figma", "Social"], [(OPEN, U + "advertising/", False)]),
        card(U + "sticker-pack", "sticker-pack.jpg", ("DESIGN · MÄR 2024", "DESIGN · MAR 2024"),
             ("Sticker-Set", "Sticker pack"),
             ("Eine in Illustrator gezeichnete Sticker-Serie mit Plakat, QR-Code und Download-Seite.",
              "A sticker series drawn in Illustrator, with a poster, QR code and download page."),
             ["Illustrator", "Figma", "HTML"],
             [(("Plakat", "Poster"), U + "sticker-pack/Pack/Artboard%201.pdf", True),
              (("Download-Seite", "Download page"), U + "sticker-pack/", True)], demo=True),
        card(U + "patterns", "patterns.jpg", ("DESIGN · SEP 2024", "DESIGN · SEP 2024"),
             ("Muster", "Patterns"), ("Drei Ornamentstudien.", "Three ornament studies."),
             ["Illustrator"], [(OPEN, U + "patterns/", False)], shot="contain"),
    ]),
]


CHEVRON = ('<svg class="icon icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
           'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>')


def section(sid, eyebrow, title, desc, groups):
    """One collapsible section of the kit page: the institution in the summary, its works inside."""
    return f'''      <details class="card fold works" id="{sid}" open>
        <summary><span>{t("span", eyebrow, "eyebrow")}{t("span", title, "fold-title")}</span>{CHEVRON}</summary>
        <div class="fold-body">
          {t("p", desc, "block-desc")}
''' + "\n\n".join(groups) + "\n        </div>\n      </details>"


def main() -> None:
    p = ROOT / "index.html"
    s = p.read_text(encoding="utf-8")
    college = section(
        "college", ("Kolleg · ausgewählte Arbeiten 2022 – 2024", "College · selected works 2022 – 2024"),
        ("Fachkolleg für Informationstechnologien Charkiw", "Kharkiv Professional College of Information Technologies"),
        ("Struktureinheit der Nationalen Luft- und Raumfahrtuniversität „Charkiwer Luftfahrtinstitut“. Fachrichtung 172 "
         "Telekommunikation und Funktechnik. Gruppen МЗ-21 → МЗ-31.",
         "Separate structural unit of the National Aerospace University “Kharkiv Aviation Institute”. Specialty 172 "
         "Telecommunications and Radio Engineering. Groups МЗ-21 → МЗ-31."), COLLEGE)
    university = section(
        "university", ("Universität · ausgewählte Arbeiten 2023 – 2025", "University · selected works 2023 – 2025"),
        ("Nationale Universität für Radioelektronik Charkiw", "Kharkiv National University of Radio Electronics"),
        ("Verlagswesen und Druck, Gruppe ВПВПС-23-2. Layout, Druckproduktion, Farbe, Typografie und Ingenieurgrafik.",
         "Publishing and printing, group ВПВПС-23-2. Layout, print production, color, type and engineering graphics."), UNIVERSITY)
    s = re.sub(r'      <details class="card fold works" id="college".*?\n      </details>', lambda m: college, s, count=1, flags=re.S)
    s = re.sub(r'      <details class="card fold works" id="university".*?\n      </details>', lambda m: university, s, count=1, flags=re.S)
    p.write_text(s, encoding="utf-8")
    print("cards:", s.count("<article"))


if __name__ == "__main__":
    main()
