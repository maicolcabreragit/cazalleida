#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el PDF de la plantilla en blanco."""
import base64, os, subprocess

ROOT     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "autorizacion-caza-conejo-PLANTILLA.html")
LOGO     = os.path.join(ROOT, "images", "logo-cazalleida-sm.png")
BUILD    = os.path.join(ROOT, "build_pdf")
OUTDIR   = os.path.join(ROOT, "pdfs")
CHROME   = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

os.makedirs(BUILD, exist_ok=True)
os.makedirs(OUTDIR, exist_ok=True)

# Leer plantilla y embeber logo en base64
with open(TEMPLATE, "r", encoding="utf-8") as f:
    html = f.read()
with open(LOGO, "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

html = html.replace('src="images/logo-cazalleida.png"',
                    'src="data:image/png;base64,%s"' % b64)
html = html.replace('<div class="barra">',
                    '<div class="barra" style="display:none">')

tmp_html = os.path.join(BUILD, "00-PLANTILLA-EN-BLANCO.html")
out_pdf  = os.path.join(OUTDIR, "00-PLANTILLA-EN-BLANCO.pdf")

with open(tmp_html, "w", encoding="utf-8") as f:
    f.write(html)

file_url = "file:///" + tmp_html.replace("\\", "/")

cmd = [
    CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
    "--disable-dev-shm-usage",
    "--user-data-dir=" + os.path.join(os.environ.get("TEMP", "C:\\Temp"), "chrome-pdf-profile"),
    "--no-pdf-header-footer",
    "--run-all-compositor-stages-before-draw",
    "--virtual-time-budget=2000",
    "--print-to-pdf=" + out_pdf,
    file_url,
]
subprocess.run(cmd, check=True, capture_output=True, timeout=60)
print("OK:", out_pdf)
print("Tamaño:", os.path.getsize(out_pdf), "bytes")
