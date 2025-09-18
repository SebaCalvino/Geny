import datetime as dt
import json
import os
import random
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

from .utils import sanitize_email, avatar_for, picsum

TEMPLATES = ["corporate", "portfolio", "store", "blog", "gallery"]

BASE_SECTIONS = ["hero", "features", "how", "gallery", "team", "contact"]

HTML_HEAD = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<link rel="stylesheet" href="styles.css" />
</head>
<body class="{template}">
<header class="site-header">
  <nav class="nav">
    <a href="index.html" class="brand">{brand}</a>
    <button class="nav-toggle" aria-label="Abrir menú">☰</button>
    <ul class="nav-links">
      <li><a href="index.html">Inicio</a></li>
      <li><a href="about.html">Nosotros</a></li>
      <li><a href="services.html">Servicios</a></li>
      <li><a href="gallery.html">Galería</a></li>
      <li><a href="contact.html">Contacto</a></li>
      <li><a class="nav-login" href="login.html">Login</a></li>
    </ul>
  </nav>
</header>
<main>
"""

HTML_FOOT = """
</main>
<footer class="site-footer">
  <p>© {year} {brand} — Hecho por Tektra</p>
</footer>
<script src="script.js"></script>
</body></html>
"""

SECTION_TPL = {
    "hero": lambda brand: f"""
<section class="sec hero">
  <div class="hero-text">
    <h1>{brand}</h1>
    <p>Inspiración, diseño y tecnología que no duerme.</p>
    <a class="btn" href="contact.html">Empezar</a>
  </div>
  <div class="hero-media">
    <img src="{picsum(1600, 900)}" alt="Hero principal" />
  </div>
</section>
""",
    "features": lambda _: f"""
<section class="sec features">
  <h2>Características</h2>
  <div class="grid3">
    <article><img src="{picsum(640, 420)}" alt="Feature 1"/><h3>Velocidad</h3><p>Entrega continua con calidad.</p></article>
    <article><img src="{picsum(640, 420)}" alt="Feature 2"/><h3>Diseño</h3><p>Paletas coherentes y layout responsivo.</p></article>
    <article><img src="{picsum(640, 420)}" alt="Feature 3"/><h3>Historia</h3><p>Narrativas únicas por proyecto.</p></article>
  </div>
</section>
""",
    "how": lambda _: f"""
<section class="sec how">
  <h2>Cómo funciona</h2>
  <ol class="steps">
    <li>Definimos el tema y paleta.</li>
    <li>Combinamos secciones y generamos contenido.</li>
    <li>Publicamos con assets y metadatos reproducibles.</li>
  </ol>
  <div class="row">
    <img src="{picsum(900, 600)}" alt="Proceso 1"/>
    <img src="{picsum(900, 600)}" alt="Proceso 2"/>
  </div>
</section>
""",
    "gallery": lambda _: f"""
<section class="sec gallery">
  <h2>Galería</h2>
  <div class="masonry">
    {"".join([f'<img src="{picsum(600, 400, i)}" alt="Shot {i}"/>' for i in range(1, 9)])}
  </div>
</section>
""",
    "team": lambda _: f"""
<section class="sec team">
  <h2>Equipo</h2>
  <div class="grid4">
    {"".join([f'<figure><img src="{picsum(320, 320, i)}" alt="Miembro {i}"/><figcaption>Miembro {i}</figcaption></figure>' for i in range(1,5)])}
  </div>
</section>
""",
    "contact": lambda _: f"""
<section class="sec contact">
  <h2>Contacto</h2>
  <p>¿Listo para crear? Envíanos un mensaje.</p>
  <form class="contact-form" action="#" method="post" aria-label="Formulario de contacto">
    <input type="text" name="name" placeholder="Tu nombre" required />
    <input type="email" name="email" placeholder="Tu email" required />
    <textarea name="message" rows="6" placeholder="Tu mensaje"></textarea>
    <button class="btn" type="submit">Enviar</button>
  </form>
  <div class="contact-cards">
    {{"".join([])}}
  </div>
</section>
"""
}

SUBPAGES = ["about", "services", "gallery", "contact"]

CSS_BASE = r"""
:root { --bg:#0b0b12; --fg:#f5f6fb; --muted:#a7a9b5; --acc:#7c5cff; }
*{box-sizing:border-box} html,body{margin:0;padding:0;background:var(--bg);color:var(--fg);font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu}
a{color:var(--fg);text-decoration:none} img{display:block;max-width:100%;height:auto}
.site-header{position:sticky;top:0;background:#111;border-bottom:1px solid #222}
.nav{display:flex;align-items:center;justify-content:space-between;gap:1rem;max-width:1200px;margin:0 auto;padding:0.75rem 1rem}
.nav .brand{font-weight:800;letter-spacing:.5px}
.nav-links{display:flex;gap:1rem;list-style:none;margin:0;padding:0}
.nav-login{background:var(--acc);color:white;padding:.4rem .8rem;border-radius:.5rem}
.nav-toggle{display:none}
@media (max-width: 820px){
  .nav-toggle{display:block}
  .nav-links{display:none}
}
main{max-width:1200px;margin:0 auto;padding:1rem}
.sec{padding:2.5rem 0;border-bottom:1px dashed #2a2a35}
.hero{display:grid;grid-template-columns:1.1fr .9fr;gap:1.5rem;align-items:center}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem}
.masonry{columns:4;column-gap:1rem}
.masonry img{width:100%;margin:0 0 1rem;border-radius:.6rem}
.row{display:flex;gap:1rem;flex-wrap:wrap}
.btn{display:inline-block;background:var(--acc);color:#fff;padding:.7rem 1rem;border-radius:.6rem}
.site-footer{max-width:1200px;margin:0 auto;padding:2rem 1rem;color:var(--muted)}
.contact-form{display:grid;gap:.6rem;max-width:680px}
.card{background:#14141c;border:1px solid #222;border-radius:.8rem;padding:1rem}
@media (max-width: 820px){
  .hero{grid-template-columns:1fr}
  .grid3{grid-template-columns:1fr}
  .grid4{grid-template-columns:repeat(2,1fr)}
  .masonry{columns:2}
}
"""

JS_BASE = r"""
document.addEventListener('DOMContentLoaded', () => {
  const t = document.querySelector('.nav-toggle');
  const l = document.querySelector('.nav-links');
  if (t && l) t.addEventListener('click', ()=> l.style.display = (l.style.display==='flex'?'none':'flex'));
});
"""

LOGIN_HTML = """<!DOCTYPE html>
<html lang="es"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Login</title><link rel="stylesheet" href="styles.css"/>
</head><body>
<main style="max-width:420px;margin:10vh auto" class="card">
  <h1>Iniciar sesión</h1>
  <form onsubmit="event.preventDefault(); alert('Login demo');">
    <label>Email</label>
    <input type="email" required style="width:100%;padding:.6rem;margin:.2rem 0"/>
    <label>Contraseña</label>
    <input type="password" required style="width:100%;padding:.6rem;margin:.2rem 0"/>
    <button class="btn" type="submit" style="margin-top:.6rem">Entrar</button>
    <p style="color:#a7a9b5;margin-top:.8rem"><a href="#">¿Olvidaste tu contraseña?</a></p>
  </form>
</main>
</body></html>
"""

def _load_cfg():
    path = Path("config.yaml")
    if yaml and path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}

def _fake_contacts(n=3, cfg=None):
    cfg = cfg or {}
    pref = (cfg.get("contact_generation") or {}).get("preferred_domains")
    provider = (cfg.get("contact_generation") or {}).get("avatar_provider", "dicebear")
    names = ["Alex Ramos", "Dana López", "Kai Fernández", "Rocío Vega", "Luca Benítez"]
    random.shuffle(names)
    out = []
    for i in range(n):
        name = names[i % len(names)]
        first, last = (name.split()[0], name.split()[-1])
        raw_email = "hola@gmail.com"  # será saneado
        email = sanitize_email(raw_email, first, last, preferred_domains=pref)
        out.append({
            "name": name,
            "email": email,
            "avatar_url": avatar_for(name, provider=provider)
        })
    return out

def _write_page(dirpath, fname, title, brand, template, sections_html):
    html = HTML_HEAD.format(title=title, brand=brand, template=template)
    html += "\n".join(sections_html)
    html += HTML_FOOT.format(year=dt.datetime.now().year, brand=brand)
    (dirpath / fname).write_text(html, encoding="utf-8")

def generate_site(base_output_dir: Path):
    cfg = _load_cfg()
    min_sections = (cfg.get("web_generation") or {}).get("min_sections", 6)

    # Seleccionar template para diversidad real
    template = random.choice((cfg.get("web_generation") or {}).get("templates", TEMPLATES))
    brand = random.choice(["Nebula Forge", "Luna Atelier", "Voxel & Co.", "Atlas Studio", "Kite Labs"])
    site_slug = f"{brand.lower().replace(' ','-')}-{template}-{random.randint(1000,9999)}"

    site_dir = Path(base_output_dir) / site_slug
    site_dir.mkdir(parents=True, exist_ok=True)

    # Escribir CSS y JS
    (site_dir / "styles.css").write_text(CSS_BASE, encoding="utf-8")
    (site_dir / "script.js").write_text(JS_BASE, encoding="utf-8")
    (site_dir / "login.html").write_text(LOGIN_HTML, encoding="utf-8")

    # Secciones landing (mínimo 6) con muchas imágenes
    sections = BASE_SECTIONS.copy()
    random.shuffle(sections)
    sections = sections[:max(min_sections, len(BASE_SECTIONS))]
    parts = []
    for s in sections:
        parts.append(SECTION_TPL[s](brand))

    _write_page(site_dir, "index.html", f"{brand} — {template.title()}", brand, template, parts)

    # Subpáginas más largas y variadas
    for page in SUBPAGES:
        extra_imgs = "".join([f'<img src="{picsum(1280,720,i)}" alt="{page} {i}"/>' for i in range(4, 10)])
        section_big = f"""
<section class="sec">
  <h2>{page.title()}</h2>
  <p>Contenido extendido para {brand}. Esta sección incluye texto sustantivo,
  layout responsive y una cuadrícula rica en multimedia.</p>
  <div class="masonry">{extra_imgs}</div>
</section>"""
        _write_page(site_dir, f"{page}.html", f"{brand} — {page.title()}", brand, template, [section_big])

    # Contacto con tarjetas y avatars
    contacts = _fake_contacts(4, cfg)
    cards = []
    for c in contacts:
        cards.append(f"""
        <article class="card">
          <div style="display:flex;gap:1rem;align-items:center">
            <img src="{c['avatar_url']}" alt="Avatar {c['name']}" width="64" height="64"/>
            <div>
              <strong>{c['name']}</strong><br/>
              <a href="mailto:{c['email']}">{c['email']}</a>
            </div>
          </div>
        </article>""")
    contact_cards_html = "\n".join(cards)

    # Inyectar tarjetas al contact.html (append)
    contact_path = site_dir / "contact.html"
    appended = contact_path.read_text(encoding="utf-8").replace(
        '<div class="masonry">', f'<div class="contact-cards">{contact_cards_html}</div>\n<div class="masonry">'
    )
    contact_path.write_text(appended, encoding="utf-8")

    # Metadata reproducible
    meta = {
        "type": "web",
        "brand": brand,
        "template": template,
        "generated_at": dt.datetime.now().isoformat(),
        "contacts": contacts,
        "pages": ["index.html"] + [f"{p}.html" for p in SUBPAGES] + ["login.html"]
    }
    (site_dir / "metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    return site_dir
