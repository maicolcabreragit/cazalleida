#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera un PDF A4 por cada cazador a partir de la plantilla HTML."""
import base64, os, re, subprocess, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "autorizacion-caza-conejo.html")
LOGO = os.path.join(ROOT, "images", "logo-cazalleida-sm.png")
BUILD = os.path.join(ROOT, "build_pdf")
OUTDIR = os.path.join(ROOT, "pdfs")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# (numero, nombre, dni)  ── DNI del nº30 sin "(And)"
CAZADORES = [
    (1, "Benito Gili Florensa", "40898319H"),
    (2, "Juan Francisco de la Cruz Sanchez Plana", "40876029S"),
    (3, "Ferran Galcerà Solé", "47936701-D"),
    (4, "Miquel Galcerà Altés", "78575149-L"),
    (5, "Enric Cabré Solá", "40834218H"),
    (6, "Antonio Sunalla Raimat", "40838458A"),
    (7, "Jordi Sans Pascuet", "40841054T"),
    (8, "Josep Cots Pelegri", "40847530J"),
    (9, "Francisco Zarza Garcia", "39699060W"),
    (10, "Victor Manuel Zarza Garcia", "39699767L"),
    (11, "Yeray Zarza Callejón", "49316079P"),
    (12, "Miquel Angel Rodriguez", "46719456Q"),
    (13, "Miquel Jaldo Pelegrino", "46518981D"),
    (14, "Miquel Jaldo Delpino", "49288378E"),
    (15, "Jesus Jaldo Pelegrina", "46537187E"),
    (16, "Emilio Useno Castno", "37323935H"),
    (17, "Jose Bernal Marnenda", "43500907-H"),
    (18, "Abel Bernal Galvez", "53033535C"),
    (19, "Diego Jose Galena Quisano", "39473017-A"),
    (20, "José A. Galcera Gea", "39728517L"),
    (21, "Juan Antonio Fdez. Suarez", "39675622R"),
    (22, "Sebastian Hervás Soriano", "39854673C"),
    (23, "Adrian Fdez Izquierdo", "49647703H"),
    (24, "Llorenç Ruiz Sala", "34758374S"),
    (25, "Jose A. Rodriguez Sanchez", "43499011P"),
    (26, "Juan Corominas de Dios", "77260203Y"),
    (27, "Inga Ermolova", "47918378V"),
    (28, "Manuel Castillo Lopez", "4498318P"),
    (29, "Carlos Castillo Leon", "77795483F"),
    (30, "Joaquin Feixo Fannagoldo", "06643116"),
    (31, "Ramón Vidal Sabaté", "40880798T"),
    (32, "Jordi Vidal García", "39938597V"),
    (33, "Jorge Vidal Miró", "39874279F"),
    (34, "Josep María Reves", "78050679H"),
    (35, "Sergio Valera Guerrero", "39888316Z"),
    (36, "Iker Valera Gisbert", "39940528Q"),
    (37, "Juan Varela Ortiz", "25912415V"),
    (38, "Sebastian Altemir Riba", "53332504N"),
    (39, "Sebastia Ros Barbera", "40864924L"),
    (40, "Adriá Ros Pujol", "78089599E"),
    (41, "Francesc Sánchez Besora", "46723855E"),
]


def slug(txt):
    txt = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode()
    txt = re.sub(r"[^A-Za-z0-9]+", "-", txt).strip("-")
    return txt


def build_template():
    with open(TEMPLATE, "r", encoding="utf-8") as f:
        html = f.read()
    # Embed logo as base64 data URI so headless chrome always loads it
    with open(LOGO, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    html = html.replace(
        'src="images/logo-cazalleida.png"',
        'src="data:image/png;base64,%s"' % b64,
    )
    # Hide the toolbar/button in generated files
    html = html.replace(
        '<div class="barra">',
        '<div class="barra" style="display:none">',
    )
    return html


def render(html, name, dni, out_pdf):
    doc = html
    doc = re.sub(
        r'(<span class="valor" data-field="nombre">)[^<]*(</span>)',
        lambda m: m.group(1) + name + m.group(2),
        doc,
    )
    doc = re.sub(
        r'(<span class="valor" data-field="dni">)[^<]*(</span>)',
        lambda m: m.group(1) + dni + m.group(2),
        doc,
    )
    tmp_html = os.path.join(BUILD, os.path.basename(out_pdf).replace(".pdf", ".html"))
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(doc)
    cmd = [
        CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--disable-dev-shm-usage",
        "--user-data-dir=" + os.path.join(os.environ.get("TEMP", "C:\\Temp"), "chrome-pdf-profile"),
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=2000",
        "--print-to-pdf=" + out_pdf,
        "file://" + tmp_html,
    ]
    subprocess.run(cmd, check=True, capture_output=True, timeout=60)


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(OUTDIR, exist_ok=True)
    html = build_template()
    items = CAZADORES
    if only == "test":
        items = CAZADORES[:1]
    for num, nombre, dni in items:
        fname = "%02d-%s.pdf" % (num, slug(nombre))
        out = os.path.join(OUTDIR, fname)
        render(html, nombre, dni, out)
        print("OK", fname)
    print("TOTAL", len(items))


if __name__ == "__main__":
    main()
