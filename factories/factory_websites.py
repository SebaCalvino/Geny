# factories/factory_websites.py
from __future__ import annotations
import random
import textwrap
from pathlib import Path
from datetime import datetime

THEMES = [
    ("Observatorio Cósmico", "Explora el cielo nocturno, constelaciones y eventos astronómicos."),
    ("Museo de Arte Generativo", "Exhibiciones creadas por algoritmos y humanos en colaboración."),
    ("Café de Viajeros", "Historias y mapas de viajeros alrededor del mundo."),
    ("Club de Jardinería Urbana", "Huertas en balcones, compost y vida verde en la ciudad."),
    ("Archivo de Robots Amistosos", "Catálogo de robots con hobbies y personalidades curiosas."),
    ("Festival de Cine Retro", "Proyecciones, afiches y crónicas de películas clásicas."),
    ("Laboratorio de Ideas Absurdas", "Prototipos imposibles que inspiran soluciones reales."),
    ("Santuario de Gatos Legendarios", "Mitos, historias y retratos de felinos heroicos."),
]

PALETTES = [
    ("#0ea5e9", "#22d3ee", "#e2e8f0", "#0f172a"),  # azul/aqua
    ("#22c55e", "#84cc16", "#f8fafc", "#052e16"),  # verde lima
    ("#a78bfa", "#f0abfc", "#faf5ff", "#1f1147"),  # lila/rosa
    ("#f59e0b", "#ef4444", "#fff7ed", "#220a00"),  # naranja/rojo
    ("#06b6d4", "#14b8a6", "#e6fffb", "#022c22"),  # teal
    ("#fb7185", "#fda4af", "#fff1f2", "#3b0a14"),  # coral
]

def _gradient(a: str, b: str) -> str:
    return f"linear-gradient(135deg, {a} 0%, {b} 100%)"

def _wrap(s: str) -> str:
    return textwrap.dedent(s).strip() + "\n"

def make_website(base_dir: Path, topic_dir: Path | None = None):
    """
    Crea un mini-sitio estético con 4+ páginas y CSS.
    Devuelve: (titulo, relative_path, costo_estimado, meta)
    """
    # --- tema + paleta ---
    theme_title, theme_desc = random.choice(THEMES)
    c1, c2, light, dark = random.choice(PALETTES)
    grad = _gradient(c1, c2)

    # --- carpeta de salida ---
    today = datetime.utcnow().strftime("%Y-%m-%d")
    slug = (
        theme_title.lower()
        .replace(" ", "_")
        .replace("á", "a").replace("é", "e").replace("í", "i")
        .replace("ó", "o").replace("ú", "u").replace("ñ", "n")
    )
    site_dir = (base_dir / today / f"site_{slug}_{hex(random.randrange(1<<16))[2:]}")
    site_dir.mkdir(parents=True, exist_ok=True)
    assets = site_dir / "assets"
    assets.mkdir(exist_ok=True)

    # --- CSS principal ---
    css = _wrap(f"""
    :root {{
      --c1: {c1};
      --c2: {c2};
      --light: {light};
      --dark: {dark};
      --grad: {grad};
      --radius: 18px;
      --shadow: 0 10px 30px rgba(0,0,0,.15);
    }}
    * {{ box-sizing:border-box; }}
    html,body {{ margin:0; padding:0; color:var(--dark); background: var(--light); font: 16px/1.6 ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto; }}
    a {{ color: var(--c1); text-decoration: none; }}
    img {{ max-width: 100%; display:block; border-radius: var(--radius); box-shadow: var(--shadow); }}
    header.hero {{
      background: var(--grad);
      color:white;
      padding: 72px 24px;
      text-align:center;
      position:relative;
      overflow:hidden;
    }}
    .hero h1 {{ font-size: clamp(2.2rem, 5vw, 3.6rem); margin:0 0 .25rem; letter-spacing: .5px; }}
    .hero p {{ opacity:.95; margin: 0 auto; max-width: 800px; }}
    .bubble {{ position:absolute; width:40vmin; height:40vmin; border-radius:50%; background: rgba(255,255,255,.15); filter: blur(8px); }}
    .b1 {{ left:-10vmin; top:-10vmin; }}
    .b2 {{ right:-12vmin; bottom:-12vmin; }}
    nav {{
      position: sticky; top:0; background:rgba(255,255,255,.75);
      backdrop-filter: blur(8px); border-bottom:1px solid rgba(0,0,0,.06);
    }}
    .nav-wrap {{ max-width:1100px; margin:0 auto; display:flex; gap:16px; align-items:center; padding:10px 16px; }}
    .brand {{ font-weight:800; color:var(--dark); }}
    .spacer {{ flex:1; }}
    .btn {{ padding:10px 14px; border-radius:12px; background:var(--c1); color:white; box-shadow:var(--shadow); }}
    main {{ max-width:1100px; margin: 32px auto; padding: 0 16px; }}
    .grid {{ display:grid; grid-template-columns: repeat(auto-fit,minmax(240px,1fr)); gap:20px; }}
    .card {{ background:white; padding:18px; border-radius:var(--radius); box-shadow:var(--shadow); }}
    .muted {{ color: #5b6270; }}
    footer {{ border-top:1px solid rgba(0,0,0,.08); margin-top:48px; padding: 24px; text-align:center; color:#4b5563; }}
    .pill {{ display:inline-block; padding:6px 10px; border-radius:999px; background:rgba(0,0,0,.06); margin-right:8px; }}
    .gallery img {{ transition: transform .25s ease, box-shadow .25s ease; }}
    .gallery img:hover {{ transform: translateY(-4px) scale(1.01); box-shadow: 0 14px 36px rgba(0,0,0,.2); }}
    .cta {{ margin:28px 0; background: white; padding: 18px; border-radius: var(--radius); display:flex; gap:16px; align-items:center; box-shadow: var(--shadow); }}
    .cta strong {{ font-size: 1.05rem; }}
    .notice {{ background: rgba(255,255,255,.6); padding:10px 12px; border-radius: 12px; display:inline-block; }}
    """)

    (site_dir / "styles.css").write_text(css, encoding="utf-8")

    # --- Fragmentos compartidos ---
    def nav(active: str) -> str:
        return _wrap(f"""
        <nav>
          <div class="nav-wrap">
            <a class="brand" href="index.html">{theme_title}</a>
            <span class="spacer"></span>
            <a href="index.html" {'style="font-weight:700;"' if active=='home' else ''}>Inicio</a>
            <a href="about.html" {'style="font-weight:700;"' if active=='about' else ''}>Sobre</a>
            <a href="gallery.html" {'style="font-weight:700;"' if active=='gallery' else ''}>Galería</a>
            <a href="contact.html" class="btn">Contacto</a>
          </div>
        </nav>
        """)

    def hero(title: str, subtitle: str) -> str:
        return _wrap(f"""
        <header class="hero">
          <div class="bubble b1"></div>
          <div class="bubble b2"></div>
          <h1>{title}</h1>
          <p>{subtitle}</p>
        </header>
        """)

    def footer() -> str:
        return _wrap("""
        <footer>
          <div>Hecho con ❤ por Maker Bot — mini-sitio generado automáticamente.</div>
        </footer>
        """)

    def page(s: str) -> str:
        return _wrap(f"<!doctype html><html lang='es'><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><link rel='stylesheet' href='styles.css'><title>{theme_title}</title><body>{s}</body></html>")

    # --- INDEX ---
    index_html = page(
        nav("home")
        + hero(theme_title, theme_desc)
        + _wrap("""
          <main>
            <div class="cta">
              <div class="notice">Nuevo</div>
              <strong>Explorá las secciones</strong>
              <span class="spacer"></span>
              <a class="btn" href="gallery.html">Ver Galería</a>
            </div>
            <div class="grid">
              <div class="card">
                <h3>Qué vas a encontrar</h3>
                <p class="muted">Contenido curado, pequeñas historias y elementos visuales que invitan a la curiosidad.</p>
                <span class="pill">Diseño</span><span class="pill">Historia</span><span class="pill">Rarezas</span>
              </div>
              <div class="card">
                <h3>Estética</h3>
                <p class="muted">Paletas suaves, sombras agradables y un toque de gradiente para no olvidar que la vida necesita color.</p>
              </div>
              <div class="card">
                <h3>Accesible</h3>
                <p class="muted">Ligero, responsive y sin dependencias externas. Abre rápido en cualquier dispositivo.</p>
              </div>
            </div>
          </main>
        """)
        + footer()
    )
    (site_dir / "index.html").write_text(index_html, encoding="utf-8")

    # --- ABOUT ---
    about_html = page(
        nav("about")
        + hero("Acerca de este sitio", "Un ejercicio creativo: contenido inventado pero verosímil.")
        + _wrap(f"""
          <main>
            <div class="grid">
              <div class="card">
                <h3>Concepto</h3>
                <p class="muted">“{theme_title}” nace como un tema al azar dentro de una colección de sitios experimentales. {theme_desc}</p>
              </div>
              <div class="card">
                <h3>Cómo se generó</h3>
                <p class="muted">Este sitio fue construido por un bot que compone HTML + CSS simple, con componentes reutilizables.</p>
              </div>
              <div class="card">
                <h3>Licencia</h3>
                <p class="muted">El contenido de ejemplo es libre para aprender, clonar y modificar. Úsalo como plantilla.</p>
              </div>
            </div>
          </main>
        """)
        + footer()
    )
    (site_dir / "about.html").write_text(about_html, encoding="utf-8")

    # --- GALLERY (con SVGs generados) ---
    def svg_placeholder(color_a: str, color_b: str) -> str:
        return _wrap(f"""
        <svg viewBox="0 0 1200 800" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="placeholder">
          <defs>
            <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="{color_a}"/>
              <stop offset="100%" stop-color="{color_b}"/>
            </linearGradient>
          </defs>
          <rect width="1200" height="800" fill="url(#g)"/>
          <circle cx="320" cy="260" r="120" fill="rgba(255,255,255,.25)"/>
          <circle cx="820" cy="280" r="160" fill="rgba(255,255,255,.18)"/>
          <circle cx="560" cy="460" r="220" fill="rgba(255,255,255,.12)"/>
          <text x="50%" y="92%" text-anchor="middle" font-family="monospace" font-size="28" fill="white">Maker Bot — {theme_title.lower()}</text>
        </svg>
        """)

    svgs = []
    for n in range(6):
        aa, bb = random.choice(PALETTES)[:2]
        svg = svg_placeholder(aa, bb)
        p = assets / f"ph_{n}.svg"
        p.write_text(svg, encoding="utf-8")
        svgs.append(p.name)

    gallery_items = "\n".join([f"<a href='assets/{name}'><img src='assets/{name}' alt='img'></a>" for name in svgs])

    gallery_html = page(
        nav("gallery")
        + hero("Galería", "Imágenes vectoriales suaves, generadas al vuelo como placeholders estéticos.")
        + _wrap(f"""
          <main>
            <div class="grid gallery">
              {gallery_items}
            </div>
          </main>
        """)
        + footer()
    )
    (site_dir / "gallery.html").write_text(gallery_html, encoding="utf-8")

    # --- CONTACT ---
    contact_html = page(
        nav("contact")
        + hero("Contacto", "¿Te gustó el estilo? Mandanos señales de humo digitales.")
        + _wrap("""
          <main>
            <div class="card">
              <form class="grid" onsubmit="event.preventDefault(); alert('¡Mensaje enviado! (demo)')">
                <div class="card" style="grid-column: 1/-1; background:transparent; box-shadow:none; padding:0">
                  <label>Nombre</label><br/>
                  <input style="width:100%; padding:12px; border-radius:12px; border:1px solid rgba(0,0,0,.15)">
                </div>
                <div class="card" style="grid-column: 1/-1; background:transparent; box-shadow:none; padding:0">
                  <label>Email</label><br/>
                  <input type="email" style="width:100%; padding:12px; border-radius:12px; border:1px solid rgba(0,0,0,.15)">
                </div>
                <div class="card" style="grid-column: 1/-1; background:transparent; box-shadow:none; padding:0">
                  <label>Mensaje</label><br/>
                  <textarea rows="5" style="width:100%; padding:12px; border-radius:12px; border:1px solid rgba(0,0,0,.15)"></textarea>
                </div>
                <div style="grid-column: 1/-1">
                  <button class="btn" type="submit">Enviar</button>
                </div>
              </form>
            </div>
          </main>
        """)
        + footer()
    )
    (site_dir / "contact.html").write_text(contact_html, encoding="utf-8")

    # --- EXTRA: /notes.html con tips breves ---
    notes_html = page(
        nav("none")
        + hero("Notas & Créditos", "Pequeños apuntes de estilo y componentes.")
        + _wrap("""
          <main>
            <div class="grid">
              <div class="card">
                <h3>Componentes</h3>
                <ul class="muted">
                  <li>Hero con burbujas translúcidas</li>
                  <li>Cards con sombra suave</li>
                  <li>Galería responsive</li>
                  <li>Nav sticky con blur</li>
                </ul>
              </div>
              <div class="card">
                <h3>CSS</h3>
                <p class="muted">Una sola hoja <code>styles.css</code> con variables, grid y utilidades mínimas.</p>
              </div>
              <div class="card">
                <h3>Extender</h3>
                <p class="muted">Agregá un blog, dark mode alternando <code>--light</code>/<code>--dark</code> o integra imágenes IA.</p>
              </div>
            </div>
          </main>
        """)
        + footer()
    )
    (site_dir / "notes.html").write_text(notes_html, encoding="utf-8")

    # --- Resultado (mantener contrato con orchestrator) ---
    title = f"Landing — {theme_title}"
    relpath = site_dir.relative_to(Path.cwd())
    cost = 0.0
    meta = {"topic": theme_title, "style": "neumorphism+gradient", "pages": 5}
    return title, relpath, cost, meta
