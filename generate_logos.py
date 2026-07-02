#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera 5 variantes de logo profesional para Caza Lleida (coto de caza, Les Garrigues)
usando OpenRouter (Gemini 3 Pro Image, con fallback a Flash).
Salida en images/logos/. Solo libreria estandar.
"""
import os, json, base64, urllib.request, urllib.error, time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "images", "logos")
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
MODELS = [
    "google/gemini-3-pro-image-preview",
    "google/gemini-3.1-flash-image-preview",
    "google/gemini-2.5-flash-image",
]

def load_key():
    with open(os.path.join(HERE, ".env"), encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("OPENROUTER_API_KEY="):
                return line.split("=", 1)[1].strip()
    raise SystemExit("No OPENROUTER_API_KEY en .env")

KEY = load_key()

SPECS = [
    ("logo-1-emblema.png",
     "Professional vector logo design, square 1:1, for a hunting estate. A circular vintage "
     "emblem/seal badge. In the center, an elegant side silhouette of a wild rabbit framed by "
     "two crossed olive branches. Around the ring, clean serif lettering reading 'CAZA LLEIDA' "
     "across the top and 'LES GARRIGUES 1995' across the bottom. Two-color palette: deep forest "
     "green and golden ochre on a cream background. Flat, crisp, perfectly balanced, professional "
     "brand identity, sharp clean typography, no photographic texture, no gradients, no mockup."),

    ("logo-2-minimal.png",
     "Modern minimalist vector logo, square 1:1, for a hunting estate. A clean simple line-art "
     "silhouette of a thrush bird in flight above a single olive branch, paired with a refined "
     "sans-serif wordmark reading 'CAZA LLEIDA' and a small tagline 'Les Garrigues'. Monochrome "
     "deep green on a white background, elegant use of negative space, flat design, crisp vector, "
     "professional, sharp legible typography, no photographic texture, no gradients."),

    ("logo-3-grabado.png",
     "Premium logo in vintage engraving and woodcut style, square 1:1, for a hunting estate. A "
     "finely detailed rabbit illustration in line engraving inside a rounded badge with a thin "
     "double border, hunting heritage feel. Classic serif text reading 'CAZA LLEIDA' and below "
     "'COTO DE CAZA DESDE 1995'. Dark forest green ink on aged cream paper. Sophisticated, flat, "
     "vector-like, sharp clean typography, no gradients, no photographic mockup."),

    ("logo-4-monograma.png",
     "Elegant luxury monogram logo, square 1:1, for a hunting estate. The letters 'C' and 'L' "
     "interlocked with a slender olive leaf and a small feather, refined and upscale, with the "
     "words 'CAZA LLEIDA' in a thin elegant serif placed below. Gold and deep green on a dark "
     "charcoal-green background. Minimal, balanced, flat vector design, professional brand "
     "identity, sharp legible typography, no photographic texture."),

    ("logo-5-escudo.png",
     "Heraldic shield / coat-of-arms style logo, square 1:1, for a premium hunting estate aimed "
     "at French and Spanish hunters. A classic shield containing a red-legged partridge and an "
     "olive sprig, topped with a small ribbon banner reading 'CAZA LLEIDA' and a lower banner "
     "reading 'LES GARRIGUES'. Refined two-tone forest green and gold on cream. Traditional yet "
     "clean, flat vector emblem, crisp lines, sharp clean typography, no photographic texture."),
]

def generate(prompt, model):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image", "text"],
    }).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=body, method="POST")
    req.add_header("Authorization", "Bearer " + KEY)
    req.add_header("Content-Type", "application/json")
    req.add_header("HTTP-Referer", "https://cazalleida.com")
    req.add_header("X-Title", "Caza Lleida")
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.loads(r.read().decode("utf-8"))
    msg = data["choices"][0]["message"]
    imgs = msg.get("images") or []
    if not imgs:
        return None, (msg.get("content") or "")[:160]
    url = imgs[0]["image_url"]["url"]
    head, b64 = url.split(",", 1)
    ext = "jpg" if ("jpeg" in head or "jpg" in head) else ("webp" if "webp" in head else "png")
    return base64.b64decode(b64), ext

def main():
    os.makedirs(OUT, exist_ok=True)
    print(f"Salida: {OUT}\n")
    ok = 0
    for name, prompt in SPECS:
        for model in MODELS:
            try:
                print(f"-> {name:22s} | {model} ...", end=" ", flush=True)
                img, ext = generate(prompt, model)
                if img is None:
                    print(f"sin imagen ({ext!r}) -> otro modelo")
                    continue
                base = os.path.splitext(name)[0]
                path = os.path.join(OUT, base + "." + ext)
                with open(path, "wb") as f:
                    f.write(img)
                print(f"OK ({len(img)//1024} KB) -> {base}.{ext}")
                ok += 1
                break
            except urllib.error.HTTPError as e:
                print(f"HTTP {e.code}: {e.read().decode('utf-8','ignore')[:200]}")
            except Exception as e:
                print(f"ERROR: {e}")
            time.sleep(1)
    print(f"\nListo. {ok}/5 logos en {OUT}")

if __name__ == "__main__":
    main()
