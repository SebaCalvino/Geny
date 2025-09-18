import datetime as dt
import json
from pathlib import Path

# Genera una imagen placeholder SVG (sin depender de APIs) + metadata con prompt
SVG_TPL = """<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2b2d42"/>
      <stop offset="100%" stop-color="#7c5cff"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#g)"/>
  <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"
        font-family="system-ui" font-size="42" fill="#ffffff" opacity="0.9">
    Tektra — Epic Placeholder
  </text>
</svg>
"""

def generate_image(base_output_dir: Path, w=1600, h=900):
    folder = Path(base_output_dir) / f"img_{dt.datetime.now().strftime('%H%M%S')}"
    folder.mkdir(parents=True, exist_ok=True)
    svg_path = folder / "image.svg"
    svg_path.write_text(SVG_TPL.format(w=w, h=h), encoding="utf-8")

    prompt = ("Crea una imagen épica y futurista con estética espacial, "
              "iluminación dramática, composición cinematográfica y contraste alto. "
              "Usa paletas profundas con acentos violeta y blanco; agrega detalles "
              "geométricos y neón sutil. — tektra")

    meta = {
        "type": "image",
        "generated_at": dt.datetime.now().isoformat(),
        "files": ["image.svg"],
        "prompt": prompt,
        "seed": None
    }
    (folder / "metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return folder
