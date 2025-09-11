import random
from pathlib import Path

STYLES = ["neumorphism", "glassmorphism", "brutalist", "retro-grid"]

def make_website(outdir: Path):
    topic = random.choice(["agencia de viajes", "cafetería retro", "estudio de diseño", "museo virtual"])
    style = random.choice(STYLES)
    site_dir = outdir / f"site_{topic.replace(' ','_')}_{style}"
    site_dir.mkdir(parents=True, exist_ok=True)

    html = f"""<!doctype html>
<html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{topic.title()} — {style}</title>
<link rel="stylesheet" href="styles.css">
</head><body>
<header><h1>{topic.title()}</h1><p>Estilo: {style}</p></header>
<main>
<section class="hero"><h2>Bienvenido</h2><p>Demo generado automáticamente.</p></section>
<section class="grid" id="cards"></section>
</main>
<script src="script.js"></script>
</body></html>"""

    css = """body{font-family:system-ui;margin:0;padding:0}
header{padding:48px;text-align:center}
.hero{padding:32px;text-align:center}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;padding:24px}"""

    js = """const el=document.getElementById('cards');
for(let i=0;i<9;i++){
  const c=document.createElement('article');
  c.className='card';
  c.innerHTML=`<h3>Item ${i+1}</h3><p>Contenido generado.</p>`;
  el.appendChild(c);
}"""

    (site_dir/"index.html").write_text(html, encoding="utf-8")
    (site_dir/"styles.css").write_text(css, encoding="utf-8")
    (site_dir/"script.js").write_text(js, encoding="utf-8")

    return f"Landing — {topic} ({style})", site_dir.relative_to(Path.cwd()), 0.0, {"topic": topic, "style": style}
