#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera imagenes de referencia fotorrealistas para cazalleida.com
usando OpenRouter (Gemini 3 Pro Image, con fallback a Flash).
Solo libreria estandar: no hace falta instalar nada.
"""
import os, json, base64, urllib.request, urllib.error, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "images")
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

# Modelos en orden de preferencia (cae al siguiente si uno no devuelve imagen)
MODELS = [
    "google/gemini-3-pro-image-preview",
    "google/gemini-3.1-flash-image-preview",
    "google/gemini-2.5-flash-image",
]

def load_key():
    env = os.path.join(HERE, ".env")
    with open(env, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("OPENROUTER_API_KEY="):
                return line.split("=", 1)[1].strip()
    raise SystemExit("No se encontro OPENROUTER_API_KEY en .env")

KEY = load_key()

# (archivo, prompt) — fotografia profesional, sin texto ni marcas de agua
SPECS = [
    ("hero-bg.png",
     "Ultra-photorealistic wide cinematic landscape photograph, 16:9 aspect ratio, of the "
     "Les Garrigues countryside in Lleida, Catalonia, Spain: rolling low hills covered with "
     "old olive groves, Mediterranean scrubland and scattered pine trees, at golden sunrise "
     "with soft mist settling in the valleys, warm dawn light, dramatic soft sky. Shot on a "
     "full-frame DSLR, 35mm lens, high dynamic range, natural earthy colors, no people, no text, "
     "no watermark. Professional landscape travel photography."),

    ("conejo.png",
     "Ultra-photorealistic wildlife photograph of a wild European rabbit sitting alert in dry "
     "Mediterranean scrubland with low bushes and reddish soil, early morning golden light, "
     "shallow depth of field, razor-sharp eyes, fine natural fur detail. Telephoto 400mm lens, "
     "professional nature photography, no text, no watermark."),

    ("zorzal.png",
     "Ultra-photorealistic wildlife photograph of a song thrush perched on a gnarled olive tree "
     "branch with green and black olives, soft autumn morning light, smoothly blurred natural "
     "background, intricate feather detail, tack-sharp focus on the bird. Telephoto lens, "
     "professional bird photography, no text, no watermark."),

    ("perdiz.png",
     "Ultra-photorealistic wildlife photograph of a red-legged partridge standing among dry "
     "grass and golden stubble fields, warm low morning light, detailed plumage with red beak "
     "and legs, shallow depth of field. Telephoto nature photography, no text, no watermark."),

    ("paloma.png",
     "Ultra-photorealistic wildlife photograph of a wood pigeon perched among olive branches in "
     "soft warm light, fine feather detail, blurred green background. Professional bird "
     "photography, telephoto lens, no text, no watermark."),

    ("alojamiento.png",
     "Ultra-photorealistic photograph of a traditional Catalan stone country farmhouse (masia) "
     "in Les Garrigues, warm rustic exterior with old stone walls and wooden shutters, "
     "surrounded by olive trees, golden late afternoon light, cozy and inviting, professional "
     "architectural and travel photography, no people, no text, no watermark."),

    ("jornada.png",
     "Ultra-photorealistic atmospheric photograph at dawn of a hunter seen from behind walking "
     "with a brown pointer dog through long rows of olive trees in the Mediterranean countryside, "
     "wearing a flat cap and a green hunting vest, golden morning mist, elegant and respectful "
     "mood, cinematic warm light. Professional outdoor photography, no text, no watermark."),
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
        # algunos modelos devuelven la imagen como parte de content
        return None, (msg.get("content") or "")[:200]
    url = imgs[0]["image_url"]["url"]
    head, b64 = url.split(",", 1)
    ext = "png"
    if "jpeg" in head or "jpg" in head:
        ext = "jpg"
    elif "webp" in head:
        ext = "webp"
    return (base64.b64decode(b64), ext)

def main():
    os.makedirs(OUT, exist_ok=True)
    print(f"Carpeta de salida: {OUT}\n")
    ok, fail = 0, 0
    for name, prompt in SPECS:
        done = False
        for model in MODELS:
            try:
                print(f"-> {name:18s} | {model} ...", end=" ", flush=True)
                result, info = generate(prompt, model), None
                img, ext = result
                if img is None:
                    print(f"sin imagen (texto: {ext!r}) -> pruebo otro modelo")
                    continue
                base = os.path.splitext(name)[0]
                path = os.path.join(OUT, base + "." + ext)
                with open(path, "wb") as f:
                    f.write(img)
                kb = len(img) // 1024
                print(f"OK ({kb} KB) -> {base}.{ext}")
                ok += 1
                done = True
                break
            except urllib.error.HTTPError as e:
                err = e.read().decode("utf-8", "ignore")[:300]
                print(f"HTTP {e.code}: {err}")
            except Exception as e:
                print(f"ERROR: {e}")
            time.sleep(1)
        if not done:
            fail += 1
            print(f"   !! No se pudo generar {name}\n")
    print(f"\nListo. {ok} imagenes generadas, {fail} fallidas. En {OUT}")

if __name__ == "__main__":
    main()
