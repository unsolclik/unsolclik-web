#!/usr/bin/env python3
"""Crea una galeria privada per a una família.

Ús:  python3 tools/nova-familia.py "Família Garcia" /ruta/a/les/fotos [--pick 20] [--dies 5]

- Redueix les fotos a 1400 px i hi posa la marca d'aigua unsolclik (vista prèvia).
- Les desa a fotos/families/<codi>/01.jpg, 02.jpg...
- Afegeix la família a families.js i t'escriu l'enllaç per enviar.
Requereix: pip install pillow
"""
import argparse, datetime, os, re, secrets, sys, unicodedata
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = os.path.join(ROOT, "marca", "logo-blanc.png")
SITE = "https://unsolclik.cat/"

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"^(familia|fam)\s+", "", s)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "familia"

def font(size):
    for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/Library/Fonts/Arial Bold.ttf",
              "C:/Windows/Fonts/arialbd.ttf"]:
        if os.path.exists(f): return ImageFont.truetype(f, size)
    return ImageFont.load_default()

def watermark(src, dst, logo):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im.thumbnail((1400, 1400), Image.LANCZOS)
    W, H = im.size; short = min(W, H)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # mosaic diagonal suau
    tw = int(short * .22); t = logo.resize((tw, int(tw * logo.height / logo.width)), Image.LANCZOS)
    a = t.split()[3].point(lambda v: int(v * .22)); t.putalpha(a)
    t = t.rotate(30, expand=True, resample=Image.BICUBIC)
    for y in range(-t.height, H + t.height, int(t.height * 1.9)):
        off = (y // int(t.height * 1.9)) % 2 * t.width // 2
        for x in range(-t.width + off, W + t.width, int(t.width * 1.5)):
            layer.alpha_composite(t, (x, y))
    # logo central
    cw = int(short * .62); c = logo.resize((cw, int(cw * logo.height / logo.width)), Image.LANCZOS)
    c.putalpha(c.split()[3].point(lambda v: int(v * .68)))
    layer.alpha_composite(c, ((W - c.width) // 2, (H - c.height) // 2))
    # text
    d = ImageDraw.Draw(layer); f = font(max(14, short // 48))
    txt = "VISTA PRÈVIA · unsolclik · L'ORIGINAL ES LLIURA SENSE MARQUES"
    tw2 = d.textlength(txt, font=f)
    d.text(((W - tw2) / 2, (H + c.height) / 2 + short * .03), txt, font=f, fill=(255, 255, 255, 190))
    out = Image.alpha_composite(im.convert("RGBA"), layer).convert("RGB")
    out.save(dst, quality=84, optimize=True, progressive=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nom"); ap.add_argument("carpeta")
    ap.add_argument("--pick", type=int, default=20); ap.add_argument("--dies", type=int, default=5)
    a = ap.parse_args()
    files = sorted(f for f in os.listdir(a.carpeta) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")))
    if not files: sys.exit("No hi ha fotos a la carpeta.")
    code = slug(a.nom) + "-" + secrets.token_hex(3)
    out = os.path.join(ROOT, "fotos", "families", code); os.makedirs(out)
    logo = Image.open(LOGO).convert("RGBA")
    names = []
    for i, f in enumerate(files, 1):
        n = f"{i:02d}.jpg"; watermark(os.path.join(a.carpeta, f), os.path.join(out, n), logo); names.append(n)
        print(f"  {n}  ←  {f}")
    deadline = (datetime.date.today() + datetime.timedelta(days=a.dies)).isoformat()
    entry = (f'\n  ,"{code}": {{\n    name: "{a.nom}",\n    pick: {a.pick},\n    deadline: "{deadline}",\n'
             f'    folder: "fotos/families/{code}",\n    photos: [{",".join(chr(34)+n+chr(34) for n in names)}]\n  }}')
    js = os.path.join(ROOT, "families.js"); s = open(js, encoding="utf-8").read()
    mark = "// NOVES FAMÍLIES A SOTA"
    s = s.replace(mark, mark + entry, 1); open(js, "w", encoding="utf-8").write(s)
    print(f"\n{len(names)} fotos. Data límit: {deadline}\nEnllaç per a la família:\n  {SITE}tria.html#{code}")

if __name__ == "__main__":
    main()
