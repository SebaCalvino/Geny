# factories/factory_websites.py
from __future__ import annotations
import random
import textwrap
from pathlib import Path
from datetime import datetime

# -----------------------------
# Temas con historias inventadas
# -----------------------------
THEMES = [
    {
        "name": "Luna & Brasa Joyería",
        "slug": "joyeria_luna_y_brasa",
        "tagline": "Piezas hechas a fuego lento y luz de luna.",
        "story": [
            "Luna & Brasa nació cuando Emilia, orfebre de tercera generación, encontró en una vieja caja los bocetos de su abuela. Allí estaban las curvas que más tarde darían forma a nuestra colección fundacional.",
            "Trabajamos con plata reciclada y oro ético. Cada pieza se forja en tandas pequeñas, numeradas y con trazabilidad. Preferimos la paciencia antes que la prisa."
        ],
        "sections": [
            ("Colecciones", "Anillos de sello, pendientes cóncavos y colgantes orgánicos inspirados en minerales."),
            ("Materiales", "Metales certificados, piedras recuperadas y empaques compostables."),
            ("Atelier", "Un taller abierto: visitas guiadas los sábados con demostraciones de microfusión.")
        ],
        "catalog_title": "Catálogo",
        "catalog_note": "Selección rotativa de piezas únicas. Las fotos son referenciales."
    },
    {
        "name": "Estudio Horizonte — Arquitectura",
        "slug": "estudio_horizonte",
        "tagline": "Arquitectura sobria para ciudades vivibles.",
        "story": [
            "Fundado por dos amigos de la facultad, Estudio Horizonte creció rehaciendo patios: descubrimos que un buen patio arregla media casa.",
            "Hoy lideramos proyectos de vivienda compacta y equipamientos culturales. Diseñamos con criterios de iluminación natural y mantenimiento simple."
        ],
        "sections": [
            ("Filosofía", "Espacios que envejecen bien: materiales nobles, huella ligera y flexibilidad."),
            ("Servicios", "Proyecto ejecutivo, dirección de obra y consultoría energética."),
            ("Premios", "Finalistas en Bienal Local 2023 por el Centro Barrial San Esteban.")
        ],
        "catalog_title": "Obras",
        "catalog_note": "Casos destacados y maquetas conceptuales."
    },
    {
        "name": "Café Bitácora",
        "slug": "cafe_bitacora",
        "tagline": "Historias, mapas y una extracción perfecta.",
        "story": [
            "Café Bitácora existe porque Sofi perdió un tren en Lisboa y ganó un tostador. Desde entonces, viajamos con cuadernos y volvemos con micro-lotes.",
            "Cada taza trae una ruta, una altitud y una anécdota. Los viernes leemos diarios de viaje abiertos al público."
        ],
        "sections": [
            ("Tostador", "Perfiles claros y medios, trazabilidad y compras directas."),
            ("La barra", "Filtros, espresso y cartas estacionales con mocktails de café."),
            ("Comunidad", "Círculos de lectura y trueque de postales.")
        ],
        "catalog_title": "Carta",
        "catalog_note": "Bebidas de temporada y granos disponibles en grano o molido."
    },
    {
        "name": "Museo de Arte Generativo",
        "slug": "museo_arte_generativo",
        "tagline": "Cuando el algoritmo sueña con lienzos.",
        "story": [
            "El Museo nació en un viejo galpón ferroviario. Programadores y artistas ocuparon el lugar para responder una pregunta: ¿cuándo una regla se convierte en estilo?",
            "Mostramos obras vivas: piezas que cambian con el clima, con el paso del tiempo o al ritmo de los visitantes."
        ],
        "sections": [
            ("Exhibiciones", "Colecciones temporales, residencias y jams de código abierto."),
            ("Educación", "Talleres introductorios a visuales, sonido y arte de datos."),
            ("Archivo", "Series históricas y catálogos descargables.")
        ],
        "catalog_title": "Galería",
        "catalog_note": "Imágenes generadas como placeholders estéticos."
    },
]

# -----------------------------
# Paletas profesionales (c1/c2: gradiente, light: fondo, dark: texto)
# -----------------------------
PALETTES = [
    ("#0EA5E9", "#22D3EE", "#F8FAFC", "#0F172A"),  # azul/aqua
    ("#22C55E", "#84CC16", "#F9FAFB", "#052E16"),  # verde
    ("#A78BFA", "#F0ABFC", "#FAF5FF", "#1F1147"),  # lila/rosa
    ("#F59E0B", "#EF4444", "#FFF7ED", "#220A00"),  # naranja/rojo
    ("#06B6D4", "#14B8A6", "#ECFEFF", "#022C22"),  # teal
    ("#FB7185", "#FDA4AF", "#FFF1F2", "#3B0A14"),  # coral
]

def _g(a: str, b: str) -> str:
    return f"linear-gradient(135deg, {a} 0%, {b} 100%)"

def _wrap(s: str) -> str:
    return textwrap.dedent(s).strip() + "\n"

# -----------------------------
# CSS base (profesional & liviano)
# -----------------------------
BASE_CSS = _wrap("""
:root{
  --c1:#0EA5E9; --c2:#22D3EE; --light:#F8FAFC; --dark:#0F172A;
  --grad: linear-gradient(135deg, var(--c1) 0%, var(--c2) 100%);
  --radius: 16px; --shadow: 0 10px 30px rgba(0,0,0,.12);
}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--light);color:var(--dark);
  font:16px/1.65 ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Ubuntu}
a{color:var(--c1);text-decoration:none}
img{max-width:100%;display:block;border-radius:var(--radius);box-shadow:var(--shadow)}
.container{max-width:1120px;margin:0 auto;padding:0 20px}
nav{
  position:sticky;top:0;background:rgba(255,255,255,.8);
  border-bottom:1px solid rgba(0,0,0,.06); backdrop-filter:blur(8px); z-index:10
}
.navbar{display:flex;gap:16px;align-items:center;min-height:60px}
.brand{font-weight:800;color:var(--dark)}
.nav-spacer{flex:1}
.navbar a{padding:10px 12px;border-radius:12px}
.navbar a.active{background:rgba(0,0,0,.06)}
.btn{background:var(--c1);color:#fff;padding:10px 16px;border-radius:12px;box-shadow:var(--shadow)}
.btn.ghost{background:transparent;color:var(--c1);border:1px solid var(--c1)}
.hero{background:var(--grad);color:#fff;padding:72px 0; text-align:center; position:relative; overflow:hidden}
.hero h1{font-size:clamp(2.2rem,4.5vw,3.6rem);margin:0 0 10px}
.hero p{opacity:.95;margin:0 auto;max-width:820px}
.hero .bubble{position:absolute;border-radius:999px;background:rgba(255,255,255,.15);filter:blur(6px)}
.hero .b1{width:38vmin;height:38vmin;left:-12vmin;top:-12vmin}
.hero .b2{width:42vmin;height:42vmin;right:-14vmin;bottom:-14vmin}
main{padding:32px 0}
.grid{display:grid;gap:22px}
.grid.cards{grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
.card{background:#fff;padding:18px;border-radius:var(--radius);box-shadow:var(--shadow)}
.muted{color:#5b6270}
.section-title{margin:6px 0 8px}
.kpis{display:flex;gap:16px;flex-wrap:wrap}
.kpi{background:#fff;border-radius:12px;padding:12px 14px;box-shadow:var(--shadow)}
.gallery img{transition:transform .25s ease, box-shadow .25s ease}
.gallery img:hover{transform:translateY(-4px) scale(1.01);box-shadow:0 14px 36px rgba(0,0,0,.2)}
footer{margin-top:40px;border-top:1px solid rgba(0,0,0,.08);padding:24px 0;color:#4b5563}
footer .cols{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr))}
.small{font-size:.92rem}
input,textarea,select{
  width:100%;padding:12px;border-radius:12px;border:1px solid rgba(0,0,0,.15);background:#fff
}
form .row{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
.notice{display:inline-block;background:rgba(0,0,0,.06);padding:6px 10px;border-radius:999px;margin-right:8px}
""")

# -----------------------------
# Helper para escribir una página con override de paleta
# -----------------------------
def write_page(path: Path, html_body: str, palette: tuple[str,str,str,str]):
    c1, c2, light, dark = palette
    head = _wrap(f"""
    <!doctype html><html lang="es"><head>
      <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>{path.stem}</title>
      <link rel="stylesheet" href="styles.css" />
      <style>
        :root{{ --c1:{c1}; --c2:{c2}; --light:{light}; --dark:{dark}; --grad:{_g(c1,c2)}; }}
      </style>
    </head><body>
    """)
    tail = _wrap("</body></html>")
    path.write_text(head + html_body + tail, encoding="utf-8")

# -----------------------------
# Generador de SVG placeholder con gradiente
# -----------------------------
def svg_placeholder(a: str, b: str, label: str) -> str:
    return _wrap(f"""
    <svg viewBox="0 0 1200 800" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">
      <defs>
        <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="{a}"/>
          <stop offset="100%" stop-color="{b}"/>
        </linearGradient>
      </defs>
      <rect width="1200" height="800" fill="url(#g)"/>
      <circle cx="340" cy="270" r="120" fill="rgba(255,255,255,.25)"/>
      <circle cx="820" cy="290" r="160" fill="rgba(255,255,255,.18)"/>
      <circle cx="560" cy="470" r="220" fill="rgba(255,255,255,.12)"/>
      <text x="50%" y="92%" text-anchor="middle" font-family="ui-monospace, SFMono-Regular, Menlo, monospace"
            font-size="28" fill="white">{label}</text>
    </svg>
    """)

# -----------------------------
# Fábrica principal
# -----------------------------
def make_website(base_dir: Path, topic_dir: Path | None = None):
    """
    Crea un sitio profesional con 4 páginas: index, about, catalog/galería y contact.
    Cada página sobreescribe la paleta para alternar colores.
    """
    # Elegimos tema y definimos directorio
    theme = random.choice(THEMES)
    today = datetime.utcnow().strftime("%Y-%m-%d")
    site_dir = base_dir / today / f"site_{theme['slug']}_{hex(random.randrange(1<<16))[2:]}"
    assets = site_dir / "assets"
    site_dir.mkdir(parents=True, exist_ok=True)
    assets.mkdir(exist_ok=True)

    # CSS base único
    (site_dir / "styles.css").write_text(BASE_CSS, encoding="utf-8")

    # Paletas rotativas por página
    # (index, about, catalog, contact) — si hay más paletas, se ciclan
    palettes = random.sample(PALETTES, k=4)

    # ------------- NAV / HEADER / FOOTER compartidos -------------
    def header(active: str) -> str:
        return _wrap(f"""
        <nav>
          <div class="container navbar">
            <a class="brand" href="index.html">{theme['name']}</a>
            <div class="nav-spacer"></div>
            <a href="index.html" class="{ 'active' if active=='home' else '' }">Inicio</a>
            <a href="about.html" class="{ 'active' if active=='about' else '' }">Sobre</a>
            <a href="catalog.html" class="{ 'active' if active=='catalog' else '' }">{theme['catalog_title']}</a>
            <a href="contact.html" class="btn { '' if active!='contact' else '' }">Contacto</a>
          </div>
        </nav>
        """)

    def hero(title: str, subtitle: str) -> str:
        return _wrap(f"""
        <header class="hero">
          <div class="bubble b1"></div><div class="bubble b2"></div>
          <div class="container"><h1>{title}</h1><p>{subtitle}</p></div>
        </header>
        """)

    def footer() -> str:
        return _wrap(f"""
        <footer>
          <div class="container cols">
            <div>
              <strong>{theme['name']}</strong><br>
              <span class="small">© {datetime.utcnow().year} — Sitio generado por Maker Bot</span>
            </div>
            <div class="small">
              <div class="section-title"><strong>Secciones</strong></div>
              <a href="index.html">Inicio</a> · <a href="about.html">Sobre</a> ·
              <a href="catalog.html">{theme['catalog_title']}</a> · <a href="contact.html">Contacto</a>
            </div>
            <div class="small">
              <div class="section-title"><strong>Legal</strong></div>
              <span>Privacidad</span> · <span>Términos</span>
            </div>
          </div>
        </footer>
        """)

    # ------------- INDEX (Landing) -------------
    index_body = (
        header("home")
        + hero(theme["name"], theme["tagline"])
        + _wrap("""
        <main>
          <div class="container grid cards">
            <div class="card">
              <h3>Qué hacemos</h3>
              <p class="muted">Trabajamos con procesos cuidados y comunicación transparente. Nos gusta la sobriedad y los pequeños detalles.</p>
              <div class="kpis">
                <div class="kpi"><strong>10+ años</strong><br><span class="muted small">de oficio</span></div>
                <div class="kpi"><strong>100%</strong><br><span class="muted small">producción propia</span></div>
                <div class="kpi"><strong>0 drama</strong><br><span class="muted small">solo soluciones</span></div>
              </div>
            </div>
        """)
        + "".join(
            _wrap(f"""
            <div class="card">
              <h3>{title}</h3>
              <p class="muted">{desc}</p>
            </div>
            """)
            for (title, desc) in theme["sections"]
        )
        + _wrap(f"""
            <div class="card">
              <h3>Próximo paso</h3>
              <p class="muted">Conocé más sobre nuestra historia o pasá directo al {theme['catalog_title'].lower()}.</p>
              <a class="btn" href="about.html">Conocer la historia</a>
              <a class="btn ghost" href="catalog.html" style="margin-left:8px">Ver {theme['catalog_title']}</a>
            </div>
          </div>
        </main>
        """)
        + footer()
    )
    write_page(site_dir / "index.html", index_body, palettes[0])

    # ------------- ABOUT (Historia) -------------
    about_story = "".join(_wrap(f"<p class='muted'>{p}</p>") for p in theme["story"])
    about_body = (
        header("about")
        + hero("Nuestra historia", theme["tagline"])
        + _wrap(f"""
        <main>
          <div class="container grid cards">
            <div class="card">
              <h3>Cómo empezó</h3>
              {about_story}
            </div>
            <div class="card">
              <h3>Valores</h3>
              <ul class="muted">
                <li>Artesanía y criterio profesional</li>
                <li>Materiales honestos y trazables</li>
                <li>Relaciones a largo plazo</li>
              </ul>
            </div>
            <div class="card">
              <h3>Equipo</h3>
              <p class="muted">Pequeño, interdisciplinario y curioso. Nos movemos entre taller y calle.</p>
            </div>
          </div>
        </main>
        """)
        + footer()
    )
    write_page(site_dir / "about.html", about_body, palettes[1])

    # ------------- CATALOG / GALLERY -------------
    # Creamos 6 SVGs con distintas paletas para que se vea variado
    thumbs = []
    for i in range(6):
        a, b, _, _ = random.choice(PALETTES)
        label = f"{theme['catalog_title']} · #{i+1}"
        svg = svg_placeholder(a, b, label)
        p = assets / f"img_{i:02d}.svg"
        p.write_text(svg, encoding="utf-8")
        thumbs.append(p.name)

    cards = "\n".join(
        _wrap(f"""
        <a href="assets/{name}" class="card" style="padding:0">
          <img src="assets/{name}" alt="{theme['catalog_title']}">
        </a>
        """)
        for name in thumbs
    )

    catalog_body = (
        header("catalog")
        + hero(theme["catalog_title"], theme["catalog_note"])
        + _wrap(f"""
        <main>
          <div class="container grid gallery" style="grid-template-columns:repeat(auto-fit,minmax(280px,1fr))">
            {cards}
          </div>
        </main>
        """)
        + footer()
    )
    write_page(site_dir / "catalog.html", catalog_body, palettes[2])

    # ------------- CONTACT -------------
    contact_body = (
        header("contact")
        + hero("Contacto", "Escribinos: respondemos en menos de 24 horas hábiles.")
        + _wrap("""
        <main>
          <div class="container">
            <div class="card">
              <form onsubmit="event.preventDefault(); alert('¡Mensaje enviado! (demo)')">
                <div class="row">
                  <div>
                    <label>Nombre</label>
                    <input required placeholder="Tu nombre">
                  </div>
                  <div>
                    <label>Email</label>
                    <input type="email" required placeholder="vos@email.com">
                  </div>
                </div>
                <div style="margin-top:12px">
                  <label>Mensaje</label>
                  <textarea rows="6" required placeholder="Contanos en qué podemos ayudarte"></textarea>
                </div>
                <div style="margin-top:16px;display:flex;gap:10px">
                  <button class="btn" type="submit">Enviar</button>
                  <a class="btn ghost" href="index.html">Volver al inicio</a>
                </div>
              </form>
            </div>
          </div>
        </main>
        """)
        + footer()
    )
    write_page(site_dir / "contact.html", contact_body, palettes[3])

    # Resultado esperado por el orquestador
    title = f"Landing — {theme['name']}"
    relpath = site_dir.relative_to(Path.cwd())
    cost = 0.0
    meta = {
        "topic": theme["name"],
        "style": "clean+professional",
        "pages": 4,
        "palettes": palettes,
    }
    return title, relpath, cost, meta
