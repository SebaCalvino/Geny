#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tektra Orchestrator (hard-fail proof)
- Intenta importar factories por nombre canónico.
- Si falla, busca *_factory.py por todo el repo y carga por ruta.
- Si aún falla, usa factories de respaldo para que el ciclo produzca output sí o sí.
- 3 ítems por ciclo: website + image + game.
"""

from __future__ import annotations
from pathlib import Path
import sys, importlib, importlib.util, logging, json, datetime as dt, traceback, re

ROOT = Path(__file__).parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("tektra")

# ---------------------------
# UTILIDADES
# ---------------------------
def today_folder() -> Path:
    d = dt.datetime.now().strftime("%Y-%m-%d")
    out = ROOT / "output" / d
    out.mkdir(parents=True, exist_ok=True)
    return out

def write_run_log(result: dict) -> None:
    out_dir = today_folder()
    log_path = out_dir / "run_log.json"
    try:
        if log_path.exists():
            prev = json.loads(log_path.read_text(encoding="utf-8"))
            if isinstance(prev, list):
                prev.append(result)
                log_path.write_text(json.dumps(prev, ensure_ascii=False, indent=2), encoding="utf-8")
            else:
                log_path.write_text(json.dumps([prev, result], ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            log_path.write_text(json.dumps([result], ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        log.warning("No se pudo escribir run_log.json: %s", e)

def _slug(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9\- ]+", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    return s or "item"

# ---------------------------
# CARGA INTELIGENTE DE FACTORIES
# ---------------------------
def _import_attr_by_module_name(mod_name: str, func_name: str):
    """importlib.import_module('pkg.mod'); getattr(func)."""
    try:
        mod = importlib.import_module(mod_name)
        return getattr(mod, func_name)
    except Exception as e:
        log.error("ERROR importando %s.%s: %s", mod_name, func_name, e)
        return None

def _import_attr_by_path(py_file: Path, func_name: str):
    """Carga un .py directo desde ruta usando importlib.util."""
    try:
        spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)  # type: ignore[attr-defined]
            return getattr(mod, func_name, None)
    except Exception as e:
        log.error("ERROR importando por ruta %s (%s)", py_file, e)
    return None

def _glob_first(patterns):
    for pat in patterns:
        found = list(ROOT.glob(pat))
        if found:
            return found[0]
    return None

def resolve_factory(func_name: str, canonical_module: str, search_patterns: list[str], fallback_callable):
    """
    Intenta cargar func_name desde:
    1) módulo canónico (p.ej. factories.web_factory)
    2) primer archivo que machee patrones (p.ej. **/*web*factory.py)
    3) fallback_callable si todo falla
    """
    # 1) Módulo canónico
    fn = _import_attr_by_module_name(canonical_module, func_name)
    if fn:
        log.info("Factory %s cargada desde módulo '%s'.", func_name, canonical_module)
        return fn, f"module:{canonical_module}"

    # 2) Búsqueda por patrones
    target = _glob_first(search_patterns)
    if target:
        fn = _import_attr_by_path(target, func_name)
        if fn:
            log.info("Factory %s cargada por ruta: %s", func_name, target)
            return fn, f"path:{target}"
        else:
            log.error("El archivo %s no expone la función %s.", target, func_name)

    # 3) Fallback
    log.warning("Usando FALLBACK para %s.", func_name)
    return fallback_callable, "fallback"

# ---------------------------
# FALLBACKS (si faltan tus factories reales)
# ---------------------------
def fallback_generate_site():
    out = today_folder() / f"web_{_slug('tektra-fallback')}_{dt.datetime.now().strftime('%H%M%S')}"
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text("""<!doctype html><html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tektra — Fallback Site</title>
<link rel="stylesheet" href="styles.css"></head><body>
<header class="c"><h1>Tektra — Fallback Site</h1></header>
<main class="c"><p>Este sitio fue generado por el fallback del orquestador porque no se encontraron factories web.</p></main>
<footer class="c"><small>Autogenerado • fallback</small></footer>
</body></html>""", encoding="utf-8")
    (out / "styles.css").write_text("""*{box-sizing:border-box}body{margin:0;background:#0b0b0f;color:#eaeaf2;font:16px/1.5 system-ui}
.c{max-width:900px;margin:auto;padding:16px}h1{color:#7a5cff}""", encoding="utf-8")
    (out / "metadata.json").write_text(json.dumps({"type":"website","fallback":True,"path":str(out)} ,indent=2), encoding="utf-8")
    return str(out)

def fallback_generate_image():
    from PIL import Image, ImageDraw, ImageFont  # si Pillow no está, requirements lo instala
    out = today_folder() / f"img_{_slug('tektra-fallback')}_{dt.datetime.now().strftime('%H%M%S')}"
    out.mkdir(parents=True, exist_ok=True)
    W,H=1200,630
    img = Image.new("RGB",(W,H),"#0b0b0f")
    d = ImageDraw.Draw(img)
    for y in range(H):
        t=y/(H-1)
        r=int((1-t)*11 + t*122); g=int((1-t)*11 + t*92); b=int((1-t)*15 + t*255)
        d.line([(0,y),(W,y)], fill=(r,g,b))
    txt="Tektra Fallback"
    try: font=ImageFont.load_default()
    except: font=None
    tw = d.textlength(txt, font=font)
    d.text(((W-tw)/2, H*0.45), txt, fill="#eaeaf2", font=font)
    p = out / "image.png"
    img.save(p, "PNG")
    (out / "metadata.json").write_text(json.dumps({"type":"image","fallback":True,"path":str(out)} ,indent=2), encoding="utf-8")
    return str(out)

def fallback_generate_game():
    out = today_folder() / f"game_{_slug('tektra-fallback')}_{dt.datetime.now().strftime('%H%M%S')}"
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text("""<!doctype html><html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tektra — Fallback Game</title>
<style>html,body{margin:0;background:#0b0b0f;color:#eaeaf2;font-family:system-ui}
#hud{position:fixed;top:8px;left:8px;background:#111a;border:1px solid #222;padding:8px 12px;border-radius:10px}
canvas{display:block;margin:auto;max-width:100vw;max-height:100vh}
button{background:#7a5cff;border:none;color:#fff;padding:6px 10px;border-radius:8px;cursor:pointer}</style>
</head><body>
<div id="hud">Puntos: <span id="score">0</span> · <button id="reset">Reiniciar</button></div>
<canvas id="c" width="720" height="420"></canvas>
<script>
const cvs=document.getElementById('c'),ctx=cvs.getContext('2d');let s=0,a=true,p={x:80,y:cvs.height/2,r:12,dy:0},o=[];
function sp(){const y=60+Math.random()*(cvs.height-120),r=8+Math.random()*10,v=2+Math.random()*3;o.push({x:cvs.width+20,y,r,v});}
document.getElementById('reset').onclick=()=>rt();window.addEventListener('keydown',e=>{if(e.code==='Space')p.dy-=4;if(e.code==='Enter'&&!a)rt();});
function rt(){o=[];s=0;a=true;p.y=cvs.height/2;p.dy=0;}
let t=0; (function L(){t++; if(a){if(t%50===0)sp(); p.dy*=0.98; p.y=Math.max(p.r,Math.min(cvs.height-p.r,p.y+p.dy)); o.forEach(k=>k.x-=k.v); o=o.filter(k=>k.x>-20);
for(const k of o){const dx=k.x-p.x,dy=k.y-p.y;if(Math.hypot(dx,dy)<k.r+p.r){a=false;break;} if(k.x<p.x && !k.s){k.s=true; s++; document.getElementById('score').textContent=s;}}}
ctx.clearRect(0,0,cvs.width,cvs.height);const g=ctx.createLinearGradient(0,0,0,cvs.height);g.addColorStop(0,'#0b0b0f');g.addColorStop(1,'#7a5cff');ctx.fillStyle=g;ctx.fillRect(0,0,cvs.width,cvs.height);
ctx.beginPath();ctx.fillStyle='#eaeaf2';ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();ctx.fillStyle='#111';o.forEach(k=>{ctx.beginPath();ctx.arc(k.x,k.y,k.r,0,Math.PI*2);ctx.fill();});
if(!a){ctx.fillStyle='#eaeaf2';ctx.fillText('Perdiste — Enter para reiniciar', cvs.width/2-110, cvs.height/2);} requestAnimationFrame(L);})();</script>
</body></html>""", encoding="utf-8")
    (out / "metadata.json").write_text(json.dumps({"type":"game","fallback":True,"path":str(out)} ,indent=2), encoding="utf-8")
    return str(out)

# ---------------------------
# RESOLVER LAS TRES FACTORIES
# ---------------------------
generate_site, source_site = resolve_factory(
    func_name="generate_site",
    canonical_module="factories.web_factory",
    search_patterns=["**/*web*factory.py", "**/*website*factory.py"],
    fallback_callable=fallback_generate_site,
)

generate_image, source_img = resolve_factory(
    func_name="generate_image",
    canonical_module="factories.image_factory",
    search_patterns=["**/*image*factory.py", "**/*images*factory.py", "**/*img*factory.py"],
    fallback_callable=fallback_generate_image,
)

generate_game, source_game = resolve_factory(
    func_name="generate_game",
    canonical_module="factories.game_factory",
    search_patterns=["**/*game*factory.py", "**/*games*factory.py"],
    fallback_callable=fallback_generate_game,
)

log.info("Sources -> site:%s | image:%s | game:%s", source_site, source_img, source_game)

# ---------------------------
# EJECUCIÓN DEL CICLO
# ---------------------------
def main() -> None:
    summary = {"started_at": dt.datetime.utcnow().isoformat()+"Z", "items": [], "errors": []}

    def _safe_run(name: str, fn):
        item = {"type": name, "status": "ok"}
        try:
            result = fn()
            item["result"] = result if result is not None else "ok"
            log.info("Factory %s completada.", name)
        except Exception as e:
            item["status"] = "error"
            item["error"] = str(e)
            summary["errors"].append({"factory": name, "error": str(e), "traceback": traceback.format_exc()})
            log.error("Factory %s falló: %s", name, e)
        finally:
            summary["items"].append(item)

    _safe_run("website", generate_site)
    _safe_run("image",   generate_image)
    _safe_run("game",    generate_game)

    summary["finished_at"] = dt.datetime.utcnow().isoformat()+"Z"
    write_run_log(summary)

    if all(i["status"] == "error" for i in summary["items"]):
        log.error("Todas las factories fallaron.")
        sys.exit(2)
    log.info("Ciclo Tektra completado.")

if __name__ == "__main__":
    main()
