# factories/factory_websites.py
from pathlib import Path
import random

def make_website(output_dir: Path, topic="agencia_de_viajes", style="neumorphism"):
    """
    Genera una landing en:
      output/<YYYY-MM-DD>/site_<topic>_<id>/index.html

    Devuelve: (title, path_str, cost, meta_dict)
    Usamos str(site_dir) (NO .relative_to()) para evitar errores de rutas en CI.
    """
    site_dir = output_dir / f"site_{topic}_{random.randint(0, 16**6):06x}"
    site_dir.mkdir(parents=True, exist_ok=True)

    html = f"""<!doctype html>
<html lang="es">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Landing — {topic}</title>
<style>
  :root {{
    --bg:#eef2f7; --fg:#1f2937; --card:#e6ecf3; --shadow:#cfd8e3;
  }}
  * {{ box-sizing:border-box }}
  body {{
    margin:0; min-height:100vh; display:grid; place-items:center;
    background:var(--bg); color:var(--fg);
    font-family:system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  }}
  .card {{
    width:min(900px,92vw); padding:32px; border-radius:20px; background:var(--card);
    box-shadow: 15px 15px 30px var(--shadow), -15px -15px 30px #fff;
  }}
  h1 {{ margin:0 0 8px; font-size:clamp(28px,4vw,40px) }}
  p {{ line-height:1.6; opacity:.9 }}
  .cta {{
    margin-top:18px; display:inline-block; padding:10px 16px; border-radius:12px;
    background:#111; color:#fff; text-decoration:none
  }}
</style>
<main class="card">
  <h1>{topic.title()} — {style}</h1>
  <p>Landing generada automáticamente por Maker Bot. Base lista para publicar.</p>
  <a class="cta" href="#" onclick="alert('¡Bienvenido!')">Quiero saber más</a>
</main>
</html>
"""
    (site_dir / "index.html").write_text(html, encoding="utf-8")

    # 👉 FIX: devolver string del directorio (nada de .relative_to(...))
    return f"Landing — {topic} ({style})", str(site_dir), 0.0, {"topic": topic, "style": style}
