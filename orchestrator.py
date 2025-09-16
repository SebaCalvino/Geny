import os
import sys
import json
import random
import shutil
import datetime as dt
from pathlib import Path

# ===================================
# Paths & Config base
# ===================================
ROOT = Path(__file__).parent.resolve()
OUTPUT = ROOT / "output"
CONFIG = ROOT / "config.yaml"
TZ = dt.timezone(dt.timedelta(hours=-3))  # UTC-3

def now_str():
    return dt.datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")

def today_slug():
    return dt.datetime.now(TZ).strftime("%Y-%m-%d")

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def write_text(path: Path, content: str):
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8")

def write_json(path: Path, data: dict):
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def safe_slug(text: str):
    out = "".join(c.lower() if c.isalnum() else "-" for c in text).strip("-")
    while "--" in out:
        out = out.replace("--", "-")
    return out[:60] or "item"

def load_config():
    cfg = {
        "max_items_per_day": 6,
        "daily_budget_usd": 0,
        "weights": {"image": 0.4, "web": 0.4, "game": 0.2}
    }
    try:
        import yaml
        if CONFIG.exists():
            with open(CONFIG, "r", encoding="utf-8") as f:
                user_cfg = yaml.safe_load(f) or {}
                for k, v in user_cfg.items():
                    cfg[k] = v
    except Exception:
        pass
    w = cfg["weights"]
    s = sum(w.values())
    if s <= 0:
        cfg["weights"] = {"image": 0.4, "web": 0.4, "game": 0.2}
    else:
        for k in list(w.keys()):
            w[k] = w[k] / s
    return cfg

def count_today_items(day_dir: Path):
    if not day_dir.exists():
        return 0
    n = 0
    for child in day_dir.iterdir():
        if child.is_dir() and child.name.startswith(("img_", "web_", "game_")):
            n += 1
    return n

def add_to_daily_changelog(day_dir: Path, line: str):
    cl = day_dir / "CHANGELOG.txt"
    prev = cl.read_text(encoding="utf-8") if cl.exists() else ""
    write_text(cl, (prev + line + "\n").strip() + "\n")

def update_root_index():
    lines = ["# Maker-Bot — Índice de salidas\n"]
    days = sorted([p for p in OUTPUT.iterdir() if p.is_dir()], reverse=True) if OUTPUT.exists() else []
    shown = 0
    for d in days:
        if shown >= 5:
            break
        cl = d / "CHANGELOG.txt"
        if not cl.exists():
            continue
        lines.append(f"## {d.name}")
        for li in reversed(cl.read_text(encoding='utf-8').splitlines()[-5:]):
            lines.append(f"- {li}")
            shown += 1
            if shown >= 5:
                break
    write_text(ROOT / "INDEX.md", "\n".join(lines) + "\n")

def write_auto_note(day_dir: Path, idea: str):
    note = f"# Auto note\n\nFecha: {dt.datetime.now(TZ).isoformat()}\n\nIdea: {idea}\n"
    write_text(day_dir / "AUTO_NOTE.md", note)

# ===================================
# BRAND & ASSETS HELPERS (nuevo)
# ===================================
def choose_theme():
    return random.choice([
        "joyeria", "viajes", "starwars", "cafe", "museo", "origami",
        "bookstore", "fitness", "cyberpunk", "estudio-foto"
    ])

def choose_palette(theme):
    bank = [
        {"bg":"#ffffff","muted":"#f3f5f7","text":"#1b1f24","accent":"#6b6ffb","accent2":"#0ea5e9"},
        {"bg":"#ffffff","muted":"#f6f7fb","text":"#0f172a","accent":"#a78bfa","accent2":"#6366f1"},
        {"bg":"#ffffff","muted":"#f7f7f2","text":"#1f2937","accent":"#10b981","accent2":"#34d399"},
        {"bg":"#ffffff","muted":"#f6f3f0","text":"#111827","accent":"#f59e0b","accent2":"#ef4444"},
        {"bg":"#ffffff","muted":"#eff6ff","text":"#0b1020","accent":"#38bdf8","accent2":"#22d3ee"},
    ]
    if theme in ("cyberpunk", "starwars"):
        return {"bg":"#ffffff","muted":"#eef2ff","text":"#0b1020","accent":"#7c3aed","accent2":"#06b6d4"}
    if theme in ("joyeria",):
        return {"bg":"#ffffff","muted":"#f8fafc","text":"#0f172a","accent":"#8b5cf6","accent2":"#f59e0b"}
    return random.choice(bank)

def themed_brand(theme):
    year = dt.datetime.now(TZ).year
    presets = {
        "joyeria": {
            "name": random.choice(["Étoile", "Aurora & Oro", "Luz de Plata", "Catedral"]),
            "slogan": "El arte de capturar la luz",
            "story": [
                "Nacimos del brillo sutil de los metales nobles y del pulso de las manos artesanas.",
                "Cada pieza narra un encuentro: tiempo, materia y emoción.",
                "Diseñamos joyas para guardar instantes y volver a ellos cuando haga falta."
            ],
            "sections": ["Colecciones", "Taller", "Piezas únicas"],
        },
        "viajes": {
            "name": random.choice(["Nova Travels", "Ruta Azul", "Atlas & Cielos", "Horizonte"]),
            "slogan": "Historias que empiezan con un pasaje",
            "story": [
                "Creemos que viajar es la forma más honesta de aprender.",
                "Trazamos itinerarios con ritmo humano, con silencios y sorpresas.",
                "Tu próximo recuerdo inolvidable espera en la primera escala."
            ],
            "sections": ["Destinos", "Experiencias", "Guías"]
        },
        "starwars": {
            "name": random.choice(["KyberTech", "Outer Rim Tours", "Binary Suns", "Lothal Works"]),
            "slogan": "Una galaxia, muchas historias",
            "story": [
                "Exploramos mundos lejanos donde la tecnología y el mito conviven.",
                "Prototipamos artefactos imposibles y contamos relatos del hiperespacio.",
                "Que la estética te acompañe."
            ],
            "sections": ["Holocron", "Droid Lab", "Hiperespacio"]
        },
        "cafe": {
            "name": random.choice(["Café Galáctico", "Petricor", "Faro & Bruma", "Kahvé"]),
            "slogan": "Tazas que cuentan historias",
            "story": [
                "Tostamos micro-lotes con paciencia y obsesión por el detalle.",
                "Cada grano trae un paisaje, un clima y una comunidad.",
                "Servimos café y conversaciones memorables."
            ],
            "sections": ["Carta", "Tostaduría", "Historias"]
        },
        "museo": {
            "name": "Museo RetroTech",
            "slogan": "El futuro de ayer",
            "story": [
                "Un archivo vivo de circuitos, cátodos y ruidos bonitos.",
                "Curaduría de objetos que explican cómo llegamos aquí.",
                "La nostalgia bien diseñada también es pedagogía."
            ],
            "sections": ["Colección", "Exhibiciones", "Visitas"]
        },
        "origami": {
            "name": "Estudio Origami",
            "slogan": "Papel, paciencia y aire",
            "story": [
                "Doblamos historias hasta volverlas figuras que respiran.",
                "El papel es tiempo visible: cada pliegue es una decisión.",
                "Creamos piezas ligeras como una buena idea."
            ],
            "sections": ["Galería", "Talleres", "Encargos"]
        },
        "bookstore": {
            "name": "Babel Íntima",
            "slogan": "Librería de conversaciones interminables",
            "story": [
                "Una selección breve y feroz de textos relectibles.",
                "Leemos para encontrar metáforas eficientes.",
                "Pasa, hojea, quédate."
            ],
            "sections": ["Catálogo", "Recomendados", "Club"]
        },
        "fitness": {
            "name": "Kinesis Lab",
            "slogan": "Movimiento con propósito",
            "story": [
                "Entrenamos sin dogmas: ciencia, progreso y disfrute.",
                "Programas que se adaptan al cuerpo real, no al ideal.",
                "Tu mejor hábito empieza hoy."
            ],
            "sections": ["Planes", "Equipo", "Progreso"]
        },
        "cyberpunk": {
            "name": "Neón & Lluvia",
            "slogan": "Interfaces con estética de tormenta",
            "story": [
                "Diseñamos sistemas con alma de neón: claros en la noche.",
                "Hackería elegante, sin ruido innecesario.",
                "Software que te mira a los ojos."
            ],
            "sections": ["Proyectos", "Laboratorio", "Clientes"]
        },
        "estudio-foto": {
            "name": "Luz Errante",
            "slogan": "Retratos que recuerdan",
            "story": [
                "Nos obsesionan los silencios entre disparos.",
                "Hacemos retratos que envejecen con dignidad.",
                "La luz es nuestra lengua."
            ],
            "sections": ["Portfolio", "Sesiones", "Reserva"]
        },
    }
    data = presets.get(theme, presets["joyeria"])
    palette = choose_palette(theme)
    data.update({
        "theme": theme,
        "year": year,
        "palette": palette,
        "brand_slug": safe_slug(data["name"])
    })
    return data

def mk_logo_svg(brand, palette):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="60">
  <defs>
    <linearGradient id="g" x1="0" x2="1">
      <stop offset="0%" stop-color="{palette['accent']}"/>
      <stop offset="100%" stop-color="{palette['accent2']}"/>
    </linearGradient>
  </defs>
  <circle cx="30" cy="30" r="18" fill="url(#g)"/>
  <rect x="24" y="14" width="12" height="32" rx="3" fill="#ffffff55"/>
  <text x="60" y="38" font-family="Poppins, Arial, sans-serif" font-weight="700" font-size="24" fill="{palette['text']}">{brand}</text>
</svg>'''

def make_asset_image(path: Path, size=(1200, 700), palette=None, label=""):
    ensure_dir(path.parent)
    palette = palette or {"bg":"#fff","muted":"#f3f5f7","accent":"#6b6ffb","accent2":"#0ea5e9","text":"#111"}
    try:
        from PIL import Image, ImageDraw, ImageFont
        w, h = size
        img = Image.new("RGB", size, (255, 255, 255))
        draw = ImageDraw.Draw(img)
        # Fondo
        def hex_to_rgb(hx):
            return tuple(int(hx.lstrip("#")[i:i+2], 16) for i in (0,2,4))
        draw.rectangle([0,0,w,h], fill=hex_to_rgb(palette["muted"]))
        # Diagonal
        draw.polygon([(0,int(h*0.6)), (int(w*0.55),0), (w,0), (w,int(h*0.4))], fill=hex_to_rgb(palette["accent"]))
        # Círculo
        draw.ellipse([w-240,40,w-40,240], fill=hex_to_rgb(palette["accent2"]))
        # Label
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", 42)
        except Exception:
            font = ImageFont.load_default()
        tw, th = draw.textsize(label, font=font)
        draw.text(((w-tw)//2,(h-th)//2), label, fill=hex_to_rgb(palette["text"]), font=font)
        img.save(path)
    except Exception:
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}" height="{size[1]}">
  <rect width="100%" height="100%" fill="{palette['muted']}"/>
  <polygon points="0,{int(size[1]*0.6)} {int(size[0]*0.55)},0 {size[0]},0 {size[0]},{int(size[1]*0.4)}" fill="{palette['accent']}"/>
  <circle cx="{size[0]-140}" cy="140" r="100" fill="{palette['accent2']}"/>
  <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"
        font-family="Poppins, Arial, sans-serif" font-size="42" fill="{palette['text']}">{label}</text>
</svg>'''
        write_text(path, svg)

# ===================================
# Generadores
# ===================================
def gen_epic_image(day_dir: Path):
    title = random.choice([
        "Nebulosa de Titanio", "Ciudad Cromo", "Catedral de Fotones",
        "Mareas Estelares", "Dunas Cuánticas"
    ])
    prompt = f"épicas imágenes | tema: {title}"
    slug = f"img_{safe_slug(title)}_{dt.datetime.now(TZ).strftime('%H%M%S')}"
    item_dir = day_dir / slug
    ensure_dir(item_dir)

    meta = {
        "type": "image",
        "title": title,
        "prompt": prompt,
        "seed": random.randint(0, 10_000_000),
        "created_at": now_str()
    }
    write_json(item_dir / "metadata.json", meta)

    try:
        from PIL import Image, ImageDraw, ImageFont
        w, h = 1280, 720
        img = Image.new("RGB", (w, h), (15, 16, 20))
        draw = ImageDraw.Draw(img)
        for r in range(0, max(w, h), 6):
            c = 15 + int(220 * (r/max(w, h)))
            draw.ellipse([(w//2 - r, h//2 - r), (w//2 + r, h//2 + r)], outline=(c, 30, 100))
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
        except Exception:
            font = ImageFont.load_default()
        text = title
        tw, th = draw.textsize(text, font=font)
        draw.rectangle([(40, h-120), (40+tw+40, h-40)], fill=(0, 0, 0, 180))
        draw.text((60, h-110), text, fill=(240, 240, 255), font=font)
        img.save(item_dir / f"{slug}.png")
        preview = f"{slug}.png"
    except Exception:
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0f1014"/>
      <stop offset="100%" stop-color="#502a9e"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#g)"/>
  <circle cx="980" cy="140" r="220" fill="#ffffff10"/>
  <text x="60" y="660" font-size="64" font-family="Verdana" fill="#eaeaff">{title}</text>
</svg>"""
        write_text(item_dir / f"{slug}.svg", svg)
        preview = f"{slug}.svg"

    note = f"# Auto note\n\nFecha: {dt.datetime.now(TZ).isoformat()}\n\nIdea: {prompt}\n"
    write_text(item_dir / "NOTE.md", note)
    write_text(item_dir / "README.md", f"# {title}\n\nPreview: `{preview}`\n\nPrompt: {prompt}\n")
    add_to_daily_changelog(day_dir, f"IMAGE  — {title}  → {item_dir.relative_to(ROOT)}")
    return {"type": "image", "title": title, "path": str(item_dir.relative_to(ROOT))}

def gen_mini_web(day_dir: Path):
    theme = choose_theme()
    brand = themed_brand(theme)
    title = brand["name"]
    slug = f"web_{safe_slug(title)}_{dt.datetime.now(TZ).strftime('%H%M%S')}"
    item_dir = day_dir / slug
    assets = item_dir / "assets"
    ensure_dir(assets)

    # Assets: logo + imágenes
    write_text(assets / "logo.svg", mk_logo_svg(brand["name"], brand["palette"]))
    make_asset_image(assets / "hero.png",  (1440, 720), brand["palette"], label=brand["slogan"])
    make_asset_image(assets / "card1.png", (800,  560), brand["palette"], label=brand["sections"][0])
    make_asset_image(assets / "card2.png", (800,  560), brand["palette"], label=brand["sections"][1])
    make_asset_image(assets / "card3.png", (800,  560), brand["palette"], label=brand["sections"][2])

    contact = {
        "email": f"hola@{brand['brand_slug']}.site",
        "phone": "+54 9 11 2345 6789",
        "address": "Av. Libertador 1234, CABA, Buenos Aires",
        "instagram": f"https://instagram.com/{brand['brand_slug']}",
        "twitter":   f"https://x.com/{brand['brand_slug']}",
        "facebook":  f"https://facebook.com/{brand['brand_slug']}",
    }

    css = f""":root{{
  --bg: {brand['palette']['bg']};
  --muted: {brand['palette']['muted']};
  --text: {brand['palette']['text']};
  --accent: {brand['palette']['accent']};
  --accent2: {brand['palette']['accent2']};
}}
*{{box-sizing:border-box}}html,body{{margin:0;padding:0;background:var(--bg);color:var(--text);}}
body{{font-family: 'Poppins', system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, sans-serif; line-height:1.6}}
.container{{max-width:1160px;margin:0 auto;padding:24px}}
header.nav{{background:var(--muted);border-bottom:1px solid #e5e7eb}}
header.nav .wrap{{display:flex;align-items:center;gap:24px;justify-content:space-between}}
nav a{{text-decoration:none;color:var(--text);margin-left:16px;opacity:.85}}
nav a:hover{{color:var(--accent)}}
.hero{{display:grid;grid-template-columns:1.2fr 1fr;gap:28px;align-items:center;padding:48px 0;border-bottom:1px solid #eee}}
.hero h1{{font-size:48px;line-height:1.1;margin:0}}
.hero p.lead{{font-size:18px;opacity:.9}}
.btn{{display:inline-block;background:var(--accent);color:#fff;padding:12px 18px;border-radius:12px;text-decoration:none}}
.btn:hover{{filter:brightness(1.05)}}
.grid-3{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
.card{{background:var(--muted);border:1px solid #eef2f7;border-radius:16px;overflow:hidden}}
.card img{{width:100%;height:auto;display:block}}
.card .pad{{padding:16px}}
.section{{padding:56px 0}}
.section h2{{margin-top:0;font-size:28px}}
.footer{{background:var(--muted);border-top:1px solid #e5e7eb;margin-top:56px}}
.footer .cols{{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}}
.small{{font-size:14px;opacity:.8}}
.badge{{background:var(--accent2);color:#fff;padding:4px 10px;border-radius:999px;font-size:12px}}
hr.sep{{border:0;height:1px;background:#eceff3;margin:32px 0}}
"""

    head_common = f"""<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{title} — {brand['slogan']}</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css"/>"""

    header_html = f"""<header class="nav">
  <div class="container wrap">
    <div style="display:flex;gap:12px;align-items:center">
      <img src="assets/logo.svg" alt="{title}" width="120" height="36"/>
    </div>
    <nav>
      <a href="index.html">Inicio</a>
      <a href="galeria.html">{brand['sections'][0]}</a>
      <a href="productos.html">{brand['sections'][1]}</a>
      <a href="contacto.html">Contacto</a>
    </nav>
  </div>
</header>"""

    footer_html = f"""<footer class="footer">
  <div class="container">
    <div class="cols">
      <div>
        <h3>Enlaces</h3>
        <div class="small">
          <div><a href="index.html">Inicio</a></div>
          <div><a href="galeria.html">{brand['sections'][0]}</a></div>
          <div><a href="productos.html">{brand['sections'][1]}</a></div>
          <div><a href="contacto.html">Contacto</a></div>
        </div>
      </div>
      <div>
        <h3>Redes Sociales</h3>
        <div class="small">
          <div><a href="{contact['instagram']}">Instagram</a></div>
          <div><a href="{contact['facebook']}">Facebook</a></div>
          <div><a href="{contact['twitter']}">X / Twitter</a></div>
        </div>
      </div>
      <div>
        <h3>Contacto</h3>
        <div class="small">
          <div>{contact['email']}</div>
          <div>{contact['phone']}</div>
          <div>{contact['address']}</div>
        </div>
      </div>
    </div>
    <hr class="sep"/>
    <div class="small">© {brand['year']} {title} — Hecho por Maker-Bot</div>
  </div>
</footer>"""

    index_html = f"""<!doctype html>
<html lang="es"><head>{head_common}</head>
<body>
{header_html}
<main class="container">
  <section class="hero">
    <div>
      <span class="badge">{brand['slogan']}</span>
      <h1>{title}</h1>
      <p class="lead">{brand['story'][0]}</p>
      <p>{brand['story'][1]}</p>
      <a class="btn" href="productos.html">Ver más</a>
    </div>
    <div>
      <img src="assets/hero.png" alt="Hero {title}" />
    </div>
  </section>

  <section class="section">
    <h2>{brand['sections'][0]}</h2>
    <div class="grid-3">
      <div class="card">
        <img src="assets/card1.png" alt="{brand['sections'][0]} 1"/>
        <div class="pad">
          <h3>{brand['sections'][0]} — A</h3>
          <p>{brand['story'][2]}</p>
        </div>
      </div>
      <div class="card">
        <img src="assets/card2.png" alt="{brand['sections'][1]} 1"/>
        <div class="pad">
          <h3>{brand['sections'][1]} — B</h3>
          <p>Pequeñas decisiones que construyen identidad.</p>
        </div>
      </div>
      <div class="card">
        <img src="assets/card3.png" alt="{brand['sections'][2]} 1"/>
        <div class="pad">
          <h3>{brand['sections'][2]} — C</h3>
          <p>Diseños que cuentan y no gritan.</p>
        </div>
      </div>
    </div>
  </section>
</main>
{footer_html}
</body></html>
"""

    galeria_html = f"""<!doctype html>
<html lang="es"><head>{head_common}</head>
<body>
{header_html}
<main class="container">
  <section class="section">
    <h2>{brand['sections'][0]}</h2>
    <p class="small">Una selección curada con la misma paciencia con la que se hace lo que ves.</p>
    <div class="grid-3">
      <div class="card"><img src="assets/card1.png" alt="galeria 1"><div class="pad"><strong>Serie I</strong><p>{brand['story'][1]}</p></div></div>
      <div class="card"><img src="assets/card2.png" alt="galeria 2"><div class="pad"><strong>Serie II</strong><p>Texturas que invitan a tocar.</p></div></div>
      <div class="card"><img src="assets/card3.png" alt="galeria 3"><div class="pad"><strong>Serie III</strong><p>Una coreografía de luz y forma.</p></div></div>
    </div>
  </section>
</main>
{footer_html}
</body></html>
"""

    productos_html = f"""<!doctype html>
<html lang="es"><head>{head_common}</head>
<body>
{header_html}
<main class="container">
  <section class="section">
    <h2>{brand['sections'][1]}</h2>
    <p>Lo que hacemos cuando tenemos un buen día de trabajo.</p>
    <div class="grid-3">
      <div class="card"><img src="assets/card1.png" alt="p1"><div class="pad"><h3>Opción A</h3><p>{brand['story'][0]}</p><a class="btn" href="contacto.html">Consultar</a></div></div>
      <div class="card"><img src="assets/card2.png" alt="p2"><div class="pad"><h3>Opción B</h3><p>{brand['story'][2]}</p><a class="btn" href="contacto.html">Reservar</a></div></div>
      <div class="card"><img src="assets/card3.png" alt="p3"><div class="pad"><h3>Opción C</h3><p>Ediciones limitadas. Amor por el detalle.</p><a class="btn" href="contacto.html">Saber más</a></div></div>
    </div>
  </section>
</main>
{footer_html}
</body></html>
"""

    contacto_html = f"""<!doctype html>
<html lang="es"><head>{head_common}</head>
<body>
{header_html}
<main class="container">
  <section class="section">
    <h2>Contacto</h2>
    <p class="small">Escribinos, contanos tu idea y construyamos algo con sentido.</p>
    <div class="grid-3">
      <div class="card"><div class="pad"><h3>Email</h3><p>{contact['email']}</p></div></div>
      <div class="card"><div class="pad"><h3>Teléfono</h3><p>{contact['phone']}</p></div></div>
      <div class="card"><div class="pad"><h3>Dirección</h3><p>{contact['address']}</p></div></div>
    </div>
    <hr class="sep"/>
    <form class="card" style="max-width:680px">
      <div class="pad">
        <label>Nombre<br/><input style="width:100%;padding:12px;border:1px solid #e5e7eb;border-radius:10px"/></label><br/><br/>
        <label>Mensaje<br/><textarea rows="6" style="width:100%;padding:12px;border:1px solid #e5e7eb;border-radius:10px"></textarea></label><br/><br/>
        <button class="btn" type="button">Enviar</button>
      </div>
    </form>
  </section>
</main>
{footer_html}
</body></html>
"""

    write_text(item_dir / "styles.css", css)
    write_text(item_dir / "index.html", index_html)
    write_text(item_dir / "galeria.html", galeria_html)
    write_text(item_dir / "productos.html", productos_html)
    write_text(item_dir / "contacto.html", contacto_html)

    readme_md = f"""# {title}

**Slogan:** {brand['slogan']}

## Historia
- {brand['story'][0]}
- {brand['story'][1]}
- {brand['story'][2]}

## Paleta
- bg: {brand['palette']['bg']}
- muted: {brand['palette']['muted']}
- text: {brand['palette']['text']}
- accent: {brand['palette']['accent']}
- accent2: {brand['palette']['accent2']}
"""
    write_text(item_dir / "README.md", readme_md)
    write_json(item_dir / "brand.json", {"brand": brand, "contact": contact})

    add_to_daily_changelog(day_dir, f"WEB    — {title}  → {item_dir.relative_to(ROOT)}")
    return {"type": "web", "title": title, "path": str(item_dir.relative_to(ROOT))}

def gen_game(day_dir: Path):
    title = random.choice(["Dodge Squares", "Photon Runner", "Orb Catcher"])
    slug = f"game_{safe_slug(title)}_{dt.datetime.now(TZ).strftime('%H%M%S')}"
    item_dir = day_dir / slug
    ensure_dir(item_dir)

    game_html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{title}</title>
<style>
  html,body{{margin:0;background:#0f1014;color:#e5e7eb;font-family:system-ui}}
  .wrap{{display:flex;flex-direction:column;align-items:center;gap:10px;padding:20px}}
  canvas{{background:#111827;border:1px solid #ffffff22;border-radius:12px}}
  .hud{{display:flex;gap:16px;align-items:center}}
  button{{padding:8px 12px;border-radius:10px;border:0;background:#38bdf8;color:#111827;cursor:pointer}}
</style></head>
<body>
<div class="wrap">
  <h1>{title}</h1>
  <div class="hud"><div>Puntaje: <span id="score">0</span></div><button id="start">Reiniciar</button></div>
  <canvas id="c" width="640" height="400"></canvas>
  <small>Usá ← → para moverte. Evitá los cuadrados. Llega a 100 para ganar.</small>
</div>
<script>
const cv = document.getElementById('c'), cx = cv.getContext('2d');
let player = {{x: 320, y: 360, w: 40, h: 20, vx:0}};
let obs = [], score = 0, running = true;
function spawn() {{ obs.push({{x: Math.random()*600+20, y:-20, s: 2+Math.random()*4}}); }}
setInterval(spawn, 600);
function loop() {{
  if(!running) return;
  cx.clearRect(0,0,cv.width,cv.height);
  player.x += player.vx;
  player.x = Math.max(0, Math.min(cv.width-player.w, player.x));
  cx.fillStyle = '#38bdf8'; cx.fillRect(player.x, player.y, player.w, player.h);
  cx.fillStyle = '#ef4444';
  for (let i=obs.length-1; i>=0; i--) {{
    const o = obs[i]; o.y += o.s; cx.fillRect(o.x, o.y, 14, 14);
    if (o.y > cv.height+20) {{ obs.splice(i,1); score++; }}
    if (o.x < player.x+player.w && o.x+14 > player.x && o.y < player.y+player.h && o.y+14 > player.y) {{
      running = false; alert('Perdiste. Puntaje: '+score);
    }}
  }}
  document.getElementById('score').textContent = score;
  if (score >= 100) {{ running = false; alert('¡Ganaste!'); }}
  requestAnimationFrame(loop);
}}
loop();
addEventListener('keydown', e=>{{ if(e.key==='ArrowLeft') player.vx=-6; if(e.key==='ArrowRight') player.vx=6; }});
addEventListener('keyup', e=>{{ if(e.key==='ArrowLeft' || e.key==='ArrowRight') player.vx=0; }});
document.getElementById('start').onclick=()=>{{ location.reload(); }};
</script>
</body></html>"""
    write_text(item_dir / "index.html", game_html)
    add_to_daily_changelog(day_dir, f"GAME   — {title}  → {item_dir.relative_to(ROOT)}")
    return {"type": "game", "title": title, "path": str(item_dir.relative_to(ROOT))}

# ===================================
# Main
# ===================================
def main():
    cfg = load_config()
    day_dir = OUTPUT / today_slug()
    ensure_dir(day_dir)

    made = count_today_items(day_dir)
    if made >= cfg["max_items_per_day"]:
        write_auto_note(day_dir, "Límite diario alcanzado")
        update_root_index()
        print("Límite diario alcanzado. Nada que hacer.")
        return

    r = random.random()
    w = cfg["weights"]
    cuts = [w["image"], w["image"] + w["web"]]
    if r < cuts[0]:
        result = gen_epic_image(day_dir)
    elif r < cuts[1]:
        result = gen_mini_web(day_dir)
    else:
        result = gen_game(day_dir)

    write_auto_note(day_dir, f"{result['type']} generado — {result['title']}")
    update_root_index()
    print(f"[{now_str()}] Created: {result['type']} — {result['title']} @ {result['path']}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        day_dir = OUTPUT / today_slug()
        ensure_dir(day_dir)
        write_text(day_dir / "ERROR.log", f"[{now_str()}] {repr(e)}\n")
        update_root_index()
        print("ERROR:", repr(e))
        sys.exit(1)
