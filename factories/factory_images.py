# -*- coding: utf-8 -*-
from pathlib import Path
import datetime as dt
import json
import re

ROOT = Path(__file__).resolve().parents[1]

def _slug(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9\- ]+", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    return s or "image"

def _today_dir() -> Path:
    d = dt.datetime.now().strftime("%Y-%m-%d")
    p = ROOT / "output" / d
    p.mkdir(parents=True, exist_ok=True)
    return p

def _save_png_fallback_svg(path: Path, text: str):
    # Si PIL no está disponible por alguna razón, dejamos un SVG válido.
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630">
  <defs>
    <linearGradient id="g" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#0b0b0f"/>
      <stop offset="100%" stop-color="#7a5cff"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#g)"/>
  <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"
        fill="#eaeaf2" font-family="system-ui,Segoe UI,Roboto" font-size="42">{text}</text>
</svg>
"""
    path.with_suffix(".svg").write_text(svg, encoding="utf-8")

def generate_image():
    """
    Genera una imagen PNG (o SVG fallback) + metadata.json
    en output/<YYYY-MM-DD>/img_<slug>_<timestamp>/
    Devuelve la ruta creada (string).
    """
    title = "Nebula Frame — Tektra"
    slug = _slug(title)
    stamp = dt.datetime.now().strftime("%H%M%S")
    out = _today_dir() / f"img_{slug}_{stamp}"
    out.mkdir(parents=True, exist_ok=True)

    prompt = ("Epic cosmic gradient background, subtle nebula glow, "
              "clean futuristic vibe, palette #0b0b0f #7a5cff #eaeaf2, "
              "noise texture minimal, soft vignette, 1200x630.")

    # Intentamos crear PNG con Pillow; si no, guardamos SVG
    try:
        from PIL import Image, ImageDraw, ImageFont
        W, H = 1200, 630
        img = Image.new("RGB", (W, H), "#0b0b0f")
        draw = ImageDraw.Draw(img)

        # Degradé simple manual
        for y in range(H):
            t = y / (H - 1)
            # Interpolación entre #0b0b0f y #7a5cff
            r = int((1 - t) * 11 + t * 122)
            g = int((1 - t) * 11 + t * 92)
            b = int((1 - t) * 15 + t * 255)
            draw.line([(0, y), (W, y)], fill=(r, g, b))

        # Texto
        text = "Tektra"
        try:
            # sin fuentes externas en runner; usamos default
            font = ImageFont.load_default()
        except Exception:
            font = None
        tw, th = draw.textlength(text, font=font), 14
        draw.text(((W - tw) / 2, (H - th) / 2), text, fill="#eaeaf2", font=font)

        img_path = out / f"img_{slug}.png"
        img.save(img_path, "PNG")
    except Exception:
        img_path = out / f"img_{slug}.png"  # solo por consistencia en metadata
        _save_png_fallback_svg(img_path, "Tektra")

    meta = {
        "type": "image",
        "title": title,
        "created_at": dt.datetime.now().isoformat(),
        "path": str(out),
        "prompt": prompt,
        "palette": ["#0b0b0f", "#7a5cff", "#eaeaf2"],
        "files": [f for f in [img_path.name, img_path.with_suffix('.svg').name if img_path.with_suffix('.svg').exists() else None] if f]
    }
    (out / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(out)
