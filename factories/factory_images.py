# factories/factory_images.py
from pathlib import Path
import random

def make_images(output_dir: Path, n: int = 1):
    """
    Genera una imagen placeholder en:
      output/<YYYY-MM-DD>/img_<id>.svg

    Devuelve: (title, path_str, cost, meta_dict)
    NOTA: devolvemos str(img_path) (no usamos .relative_to()) para
    evitar ValueError de rutas en GitHub Actions.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    img_path = output_dir / f"img_{random.randint(0, 16**6):06x}.svg"
    hue = random.randint(0, 360)
    topic = random.choice(["neón", "galaxia", "geometría", "vaporwave", "orgánico"])

    svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1024' height='640'>
  <defs>
    <linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>
      <stop offset='0%'  stop-color='hsl({hue},90%,55%)'/>
      <stop offset='100%' stop-color='hsl({(hue+200)%360},90%,45%)'/>
    </linearGradient>
  </defs>
  <rect width='100%' height='100%' fill='url(#g)'/>
  <g fill='rgba(255,255,255,0.15)'>
    <circle cx='200' cy='160' r='120'/>
    <circle cx='540' cy='320' r='180'/>
    <circle cx='860' cy='220' r='140'/>
  </g>
  <text x='50%' y='90%' font-family='monospace' font-size='28'
        text-anchor='middle' fill='rgba(255,255,255,0.9)'>
    Maker Bot — {topic}
  </text>
</svg>"""
    img_path.write_text(svg, encoding="utf-8")

    # 🔧 cambio clave: devolver str(img_path) (nada de .relative_to(...))
    return "Imagen — placeholder", str(img_path), 0.0, {"format": "svg", "topic": topic, "hue": hue}
