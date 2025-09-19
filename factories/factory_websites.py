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
    return s or "site"

def _today_dir() -> Path:
    d = dt.datetime.now().strftime("%Y-%m-%d")
    p = ROOT / "output" / d
    p.mkdir(parents=True, exist_ok=True)
    return p

def generate_site():
    """
    Genera una mini-web coherente (index.html, styles.css, script.js, README.md)
    en output/<YYYY-MM-DD>/web_<slug>_<timestamp>/
    Devuelve la ruta creada (string).
    """
    title = "Tektra — Nebula Studio"
    slug = _slug(title)
    stamp = dt.datetime.now().strftime("%H%M%S")
    out = _today_dir() / f"web_{slug}_{stamp}"
    out.mkdir(parents=True, exist_ok=True)

    # index.html
    (out / "index.html").write_text(f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content="Micro-sitio generado automáticamente por Tektra." />
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <header class="container">
    <h1>{title}</h1>
    <nav>
      <a href="#intro">Intro</a>
      <a href="#features">Features</a>
      <a href="#gallery">Galería</a>
    </nav>
  </header>

  <main class="container">
    <section id="intro">
      <h2>Un taller cósmico siempre encendido</h2>
      <p>Mini-sitio autogenerado con narrativa simple, paleta sobria y layout responsive.</p>
    </section>

    <section id="features" class="grid">
      <article>
        <h3>Paleta</h3>
        <p>#0b0b0f · #7a5cff · #eaeaf2</p>
      </article>
      <article>
        <h3>Navegación</h3>
        <p>Header fijo, enlaces ancla, tipografía del sistema.</p>
      </article>
      <article>
        <h3>Historia</h3>
        <p>Un estudio ficticio que diseña interfaces nebulosas para humanos reales.</p>
      </article>
    </section>

    <section id="gallery">
      <h2>Galería</h2>
      <div class="cards">
        <div class="card">Componente A</div>
        <div class="card">Componente B</div>
        <div class="card">Componente C</div>
      </div>
    </section>
  </main>

  <footer class="container">
    <small>Generado por Tektra · {dt.datetime.now().date()}</small>
  </footer>

  <script src="script.js"></script>
</body>
</html>
""", encoding="utf-8")

    # styles.css
    (out / "styles.css").write_text("""*{box-sizing:border-box}body{margin:0;background:#0b0b0f;color:#eaeaf2;font:16px/1.5 system-ui,Segoe UI,Roboto,Ubuntu,'Helvetica Neue',Arial}
.container{max-width:980px;margin:auto;padding:16px}
header{position:sticky;top:0;background:#0b0b0fdd;backdrop-filter:saturate(140%) blur(6px);border-bottom:1px solid #222}
nav a{color:#7a5cff;margin-right:16px;text-decoration:none}
h1{font-size:28px;margin:8px 0}
h2{font-size:22px;margin:20px 0 8px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}
.card{border:1px solid #222;padding:16px;border-radius:12px;background:#111}
@media (max-width:600px){h1{font-size:22px}}
""", encoding="utf-8")

    # script.js
    (out / "script.js").write_text("""document.addEventListener('DOMContentLoaded',()=>{
  const cards=[...document.querySelectorAll('.card')];
  cards.forEach((c,i)=>c.addEventListener('click',()=>alert('Card '+(i+1))));
});
""", encoding="utf-8")

    # README.md
    (out / "README.md").write_text(f"""# {title}
Sitio generado automáticamente por Tektra.

## Ver local
