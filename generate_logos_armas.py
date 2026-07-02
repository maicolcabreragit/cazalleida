#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5 variantes de logo MAS para Caza Lleida, con escopeta / equipo de caza
(cartuchos, perro de muestra, cuerno de caza). OpenRouter Gemini 3 Pro Image.
Salida: images/logos/  (logo-6 .. logo-10)
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
    ("logo-6-escopetas.png",
     "Professional vector logo, square 1:1, for a small-game hunting estate. A circular vintage "
     "sporting emblem with two classic engraved side-by-side break-action sporting shotguns "
     "crossed behind a sitting wild rabbit in the center, framed by olive branches. Clean serif "
     "text around the ring reading 'CAZA LLEIDA' on top and 'LES GARRIGUES 1995' on the bottom. "
     "Two-color deep forest green and golden ochre on a cream background. Flat, crisp, balanced "
     "sporting crest, sharp clean typography, tasteful, no photographic texture, no gradients."),

    ("logo-7-cartuchos.png",
     "Modern professional vector badge logo, square 1:1, for a hunting estate. Two shotgun "
     "cartridges (shotshells) crossed in an X with a small olive sprig, inside a clean rounded "
     "badge. Sans-serif wordmark 'CAZA LLEIDA' and tagline 'Les Garrigues'. Deep green and warm "
     "gold on a cream background. Flat, crisp, sharp legible typography, modern sporting brand "
     "identity, no photographic texture, no gradients."),

    ("logo-8-cuerno.png",
     "Elegant minimalist vector logo, square 1:1, for a hunting estate. A classic coiled hunting "
     "horn intertwined with an olive branch, refined line-art, paired with a thin elegant serif "
     "wordmark 'CAZA LLEIDA' and 'Les Garrigues'. Monochrome deep forest green on cream, premium "
     "and clean, flat vector, sharp typography, generous negative space, no photographic texture."),

    ("logo-9-perro.png",
     "Vintage circular emblem vector logo, square 1:1, for a small-game hunting estate. Silhouette "
     "of an elegant pointer dog on point beside a classic break-action shotgun standing upright, "
     "framed in a ring with a rope border. Serif text 'CAZA LLEIDA' on top and 'COTO DE CAZA' on "
     "the bottom. Deep forest green and gold on cream. Flat, crisp sporting crest, sharp clean "
     "typography, tasteful, no photographic texture."),

    ("logo-10-minimal-escopeta.png",
     "Modern minimalist vector logo, square 1:1, for a hunting estate. A single classic "
     "side-by-side shotgun crossed with an olive branch in clean simple line-art, above a refined "
     "sans-serif wordmark 'CAZA LLEIDA' with a small tagline 'Les Garrigues'. Monochrome deep "
     "green on a white background, elegant negative space, flat crisp vector, sharp legible "
     "typography, tasteful sporting emblem, no photographic texture."),
]

def generate(prompt, model):
    body = json.dumps({"model": model,
                       "messages": [{"role": "user", "content": prompt}],
                       "modalities": ["image", "text"]}).encode("utf-8")
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
                print(f"-> {name:26s} | {model} ...", end=" ", flush=True)
                img, ext = generate(prompt, model)
                if img is None:
                    print(f"sin imagen ({ext!r}) -> otro modelo")
                    continue
                base = os.path.splitext(name)[0]
                with open(os.path.join(OUT, base + "." + ext), "wb") as f:
                    f.write(img)
                print(f"OK ({len(img)//1024} KB) -> {base}.{ext}")
                ok += 1
                break
            except urllib.error.HTTPError as e:
                print(f"HTTP {e.code}: {e.read().decode('utf-8','ignore')[:200]}")
            except Exception as e:
                print(f"ERROR: {e}")
            time.sleep(1)
    print(f"\nListo. {ok}/5 logos con arma/equipo en {OUT}")

if __name__ == "__main__":
    main()
