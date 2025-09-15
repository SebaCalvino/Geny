import os
import sys
import json
import random
import shutil
import datetime as dt
from pathlib import Path

# -------- Config & util --------
ROOT = Path(__file__).parent.resolve()
OUTPUT = ROOT / "output"
CONFIG = ROOT / "config.yaml"

TZ = dt.timezone(dt.timedelta(hours=-3))  # UTC-3

def now_str():
    return dt.datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")

def today_slug():
    return dt.datetime.now(TZ).strftime("%Y-%m-%d")

def load_config():
    cfg = {
        "max_items_per_day": 6,
        "daily_budget_usd": 0,
        "weights": {"image": 0.4, "web": 0.4, "game": 0.2}
    }
    try:
        import yaml  # si no está, seguimos con defaults
        if CONFIG.exists():
            with open(CONFIG, "r", encoding="utf-8") as f:
                user_cfg = yaml.safe_load(f) or {}
                # merge plano
                for k, v in user_cfg.items():
                    cfg[k] = v
    except Exception:
        pass
    # normalizar pesos
    w = cfg["weights"]
    s = sum(w.values())
    if s <= 0:
        cfg["weights"] = {"image": 0.4, "web": 0.4, "game": 0.2}
    else:
        for k in list(w.keys()):
            w[k] = w[k]/s
    return cfg

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

def count_today_items(day_dir: Path):
    if not day_dir.exists():
        return 0
    # cuenta carpetas con prefijo img_/web_/game_
    n = 0
    for child in day_dir.iterdir():
        if child.is_dir() and (child.name.startswith(("img_", "web_", "game_"))):
            n += 1
    return n

def add_to_daily_changelog(day_dir: Path, line: str):
    cl = day_dir / "CHANGELOG.txt"
    prev = ""
    if cl.exists():
        prev = cl.read_text(encoding="utf-8")
    write_text(cl, (prev + line + "\n").strip() + "\n")

# -------- Generadores --------
def gen_epic_image(day_dir: Path):
    title = random.choice([
        "Nebulosa de Titanio", "Ciudad Cromo", "Catedral de Fotones",
        "Mareas Estelares", "Dunas Cuánticas"
    ])
    prompt = f"épicas imágenes | tema: {title}"
    slug = f"img_{safe_slug(title)}_{dt.datetime.now(TZ).strftime('%H%M%S')}"
    item_dir = day_dir / slug
    ensure_dir(item_dir)

    # metadata
    meta = {
        "type": "image",
        "title": title,
        "prompt": prompt,
        "seed": random.randint(0, 10_000_000),
        "created_at": now_str()
    }
    write_json(item_dir / "metadata.json", meta)

    # intenta PNG con Pillow, si no -> SVG puro
    try:
        from PIL import Image, ImageDraw, ImageFont
        w, h = 1280, 720
        img = Image.new("RGB", (w, h), (15, 16, 20))
        draw = ImageDraw.Draw(img)
        # fondo radial simple
        for r in range(0, max(w, h), 6):
            c = 15 + int(220 * (r/max(w, h)))
            draw.ellipse([(w//2 - r, h//2 - r), (w//2 + r, h//2 + r)], outline=(c, 30, 100))
        # texto
        text = title
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
        except Exception:
            font = ImageFont.load_default()
        tw, th = draw.textsize(text, font=font)
        draw.rectangle([(40, h-120), (40+tw+40, h-40)], fill=(0, 0, 0, 180))
        draw.text((60, h-110), text, fill=(240, 240, 255), font=font)
        img.save(item_dir / f"{slug}.png")
        preview = f"{slug}.png"
    except Exception:
        # SVG fallback
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

    # nota
    note = f"# Auto note\n\nFecha: {dt.datetime.now(TZ).isoformat()}\n\nIdea: {prompt}\n"
    write_text(item_dir / "NOTE.md", note)

    # index corto
    index_md = f"# {title}\n\nPreview: `{preview}`\n\nPrompt: {prompt}\n"
    write_text(item_dir / "README.md", index_md)

    add_to_daily_changelog(day_dir, f"IMAGE  — {title}  → {item_dir.relative_to(ROOT)}")
    return {"type": "image", "title": title, "path": str(item_dir.relative_to(ROOT))}

def gen_mini_web(day_dir: Path):
    theme = random.choice([
        ("Joyería Aurora", "joyeria", ["#0f172a", "#38bdf8", "#e2e8f0"]),
        ("Café Galáctico", "cafe", ["#1f2937", "#f59e0b", "#f3f4f6"]),
        ("Museo RetroTech", "museo", ["#111827", "#10b981", "#d1fae5"]),
        ("Estudio Origami", "origami", ["#0b1020", "#a78bfa", "#f5f3ff"]),
    ])
    title, key, palette = theme
    slug = f"web_{safe_slug(key)}_{dt.datetime.now(TZ).strftime('%H%M%S')}"
    item_dir = day_dir / slug
    ensure_dir(item_dir)

    colors = {"bg": palette[0], "accent": palette[1], "text": palette[2]}

    index_html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title}</title>
  <link rel="stylesheet" href="styles.css"/>
</head>
<body>
<header class="container">
  <h1>{title}</h1>
  <nav>
    <a href="index.html">Inicio</a>
    <a href="sobre.html">Sobre</a>
    <a href="galeria.html">Galería</a>
    <a href="contacto.html">Contacto</a>
  </nav>
</header>

<main class="container">
  <section class="hero">
    <h2>Artesanía con historia</h2>
    <p>Una micro-historia única para este sitio: piezas y relatos que viajan entre generaciones.</p>
    <button id="cta">Ver colección</button>
  </section>
</main>

<footer class="container">
  <small>© {dt.datetime.now(TZ).year} {title} — Hecho por Maker-Bot</small>
</footer>

<script src="script.js"></script>
</body>
</html>
"""
    styles_css = f"""*{{box-sizing:border-box}}html,body{{margin:0;padding:0;background:{colors['bg']};color:{colors['text']};font-family:system-ui,Segoe UI,Roboto,Ubuntu,Helvetica,Arial,sans-serif}}
.container{{max-width:1100px;margin:0 auto;padding:20px}}
header{{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #ffffff20}}
nav a{{color:{colors['text']};text-decoration:none;margin-left:14px;opacity:.9}}
nav a:hover{{color:{colors['accent']}}}
.hero{{padding:60px 0}}
button#cta{{background:{colors['accent']};color:#000;padding:12px 18px;border:none;border-radius:10px;cursor:pointer}}
button#cta:hover{{filter:brightness(1.1)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}}
.card{{background:#ffffff10;border:1px solid #ffffff20;padding:16px;border-radius:14px}}
img.responsive{{width:100%;height:auto;border-radius:12px}}
"""

    sobre_html = """<!doctype html><html lang="es"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>Sobre</title><link rel="stylesheet" href="styles.css"/></head><body><header class="container"><h1>Sobre</h1><nav><a href="index.html">Inicio</a><a href="sobre.html">Sobre</a><a href="galeria.html">Galería</a><a href="contacto.html">Contacto</a></nav></header><main class="container"><h2>Nuestra historia</h2><p>Nacimos de la curiosidad y del cuidado por los detalles. Cada proyecto es un pequeño universo.</p></main><footer class="container"><small>Hecho por Maker-Bot</small></footer></body></html>"""

    galeria_html = """<!doctype html><html lang="es"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>Galería</title><link rel="stylesheet" href="styles.css"/></head><body><header class="container"><h1>Galería</h1><nav><a href="index.html">Inicio</a><a href="sobre.html">Sobre</a><a href="galeria.html">Galería</a><a href="contacto.html">Contacto</a></nav></header><main class="container"><div class="grid"><div class="card"><img class="responsive" src="https://picsum.photos/seed/1/800/600" alt="img1"/></div><div class="card"><img class="responsive" src="https://picsum.photos/seed/2/800/600" alt="img2"/></div><div class="card"><img class="responsive" src="https://picsum.photos/seed/3/800/600" alt="img3"/></div></div></main><footer class="container"><small>Hecho por Maker-Bot</small></footer></body></html>"""

    contacto_html = """<!doctype html><html lang="es"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>Contacto</title><link rel="stylesheet" href="styles.css"/></head><body><header class="container"><h1>Contacto</h1><nav><a href="index.html">Inicio</a><a href="sobre.html">Sobre</a><a href="galeria.html">Galería</a><a href="contacto.html">Contacto</a></nav></header><main class="container"><form class="card"><label>Nombre<br/><input style="width:100%;padding:10px;border-radius:8px;border:1px solid #ffffff33;background:#00000020;color:white" placeholder="Tu nombre"/></label><br/><label>Mensaje<br/><textarea rows="5" style="width:100%;padding:10px;border-radius:8px;border:1px solid #ffffff33;background:#00000020;color:white" placeholder="Contanos..."></textarea></label><br/><button id="cta" type="button">Enviar</button></form></main><footer class="container"><small>Hecho por Maker-Bot</small></footer></body></html>"""

    script_js = """document.getElementById('cta')?.addEventListener('click',()=>{alert('¡Bienvenida/o a la colección!')})"""

    readme_md = f"""# {title}

Estructura base generada automáticamente por Maker-Bot.

- `index.html`, `sobre.html`, `galeria.html`, `contacto.html`
- `styles.css`, `script.js`

## Ver local
Abrí `index.html` en tu navegador.

## Publicación
Podés publicar rápido con GitHub Pages apuntando a esta carpeta.
"""

    write_text(item_dir / "index.html", index_html)
    write_text(item_dir / "styles.css", styles_css)
    write_text(item_dir / "sobre.html", sobre_html)
    write_text(item_dir / "galeria.html", galeria_html)
    write_text(item_dir / "contacto.html", contacto_html)
    write_text(item_dir / "script.js", script_js)
    write_text(item_dir / "README.md", readme_md)

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
function spawn() {{
  obs.push({{x: Math.random()*600+20, y:-20, s: 2+Math.random()*4}});
}}
setInterval(spawn, 600);
function loop() {{
  if(!running) return;
  cx.clearRect(0,0,cv.width,cv.height);
  // player
  player.x += player.vx;
  player.x = Math.max(0, Math.min(cv.width-player.w, player.x));
  cx.fillStyle = '#38bdf8';
  cx.fillRect(player.x, player.y, player.w, player.h);
  // obstacles
  cx.fillStyle = '#ef4444';
  for (let i=obs.length-1; i>=0; i--) {{
    const o = obs[i]; o.y += o.s;
    cx.fillRect(o.x, o.y, 14, 14);
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

# -------- Índices y notas --------
def update_root_index():
    # lista últimos 5 ítems globales
    lines = ["# Maker-Bot — Índice de salidas\n"]
    days = sorted([p for p in OUTPUT.iterdir() if p.is_dir()], reverse=True) if OUTPUT.exists() else []
    shown = 0
    for d in days:
        if shown >= 5: break
        if not d.exists(): continue
        cl = d / "CHANGELOG.txt"
        if not cl.exists(): continue
        lines.append(f"## {d.name}")
        for li in reversed(cl.read_text(encoding='utf-8').splitlines()[-5:]):
            lines.append(f"- {li}")
            shown += 1
            if shown >= 5: break
    write_text(ROOT / "INDEX.md", "\n".join(lines) + "\n")

def write_auto_note(day_dir: Path, idea: str):
    note = f"# Auto note\n\nFecha: {dt.datetime.now(TZ).isoformat()}\n\nIdea: {idea}\n"
    write_text(day_dir / "AUTO_NOTE.md", note)

# -------- Main --------
def main():
    cfg = load_config()
    day_dir = OUTPUT / today_slug()
    ensure_dir(day_dir)

    # conteo del día
    made = count_today_items(day_dir)
    if made >= cfg["max_items_per_day"]:
        write_auto_note(day_dir, "Límite diario alcanzado")
        update_root_index()
        print("Límite diario alcanzado. Nada que hacer.")
        return

    # pick tipo por pesos
    r = random.random()
    w = cfg["weights"]
    cuts = [w["image"], w["image"] + w["web"]]
    if r < cuts[0]:
        result = gen_epic_image(day_dir)
    elif r < cuts[1]:
        result = gen_mini_web(day_dir)
    else:
        result = gen_game(day_dir)

    # nota general del día
    write_auto_note(day_dir, f"{result['type']} generado — {result['title']}")
    update_root_index()

    # eco de estado en consola (para logs de Actions)
    print(f"[{now_str()}] Created: {result['type']} — {result['title']} @ {result['path']}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # log visible en Actions + guarda nota de error
        day_dir = OUTPUT / today_slug()
        ensure_dir(day_dir)
        write_text(day_dir / "ERROR.log", f"[{now_str()}] {repr(e)}\n")
        update_root_index()
        print("ERROR:", repr(e))
        sys.exit(1)
