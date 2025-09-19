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
    return s or "game"

def _today_dir() -> Path:
    d = dt.datetime.now().strftime("%Y-%m-%d")
    p = ROOT / "output" / d
    p.mkdir(parents=True, exist_ok=True)
    return p

def generate_game():
    """
    Genera un juego simple (index.html con canvas + JS embebido)
    en output/<YYYY-MM-DD>/game_<slug>_<timestamp>/
    Devuelve la ruta creada (string).
    """
    title = "Tektra — Orb Runner"
    slug = _slug(title)
    stamp = dt.datetime.now().strftime("%H%M%S")
    out = _today_dir() / f"game_{slug}_{stamp}"
    out.mkdir(parents=True, exist_ok=True)

    html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<style>
  html,body{{margin:0;height:100%;background:#0b0b0f;color:#eaeaf2;font-family:system-ui,Segoe UI,Roboto}}
  #hud{{position:fixed;top:8px;left:8px;background:#111a;border:1px solid #222;padding:8px 12px;border-radius:10px}}
  canvas{{display:block;margin:auto;max-width:100vw;max-height:100vh}}
  button{{background:#7a5cff;border:none;color:#fff;padding:6px 10px;border-radius:8px;cursor:pointer}}
</style>
</head>
<body>
<div id="hud">Puntos: <span id="score">0</span> · <button id="reset">Reiniciar</button></div>
<canvas id="c" width="720" height="420"></canvas>
<script>
const cvs = document.getElementById('c');
const ctx = cvs.getContext('2d');
const scoreEl = document.getElementById('score');
const resetBtn = document.getElementById('reset');

let player={{x:80,y:cvs.height/2,r:12,dy:0}};
let orbs=[];
let score=0, alive=true, t=0;

function spawn(){
  const y = 60 + Math.random()*(cvs.height-120);
  const r = 8 + Math.random()*10;
  const v = 2 + Math.random()*3;
  orbs.push({x:cvs.width+20,y,r,v});
}

function loop(){
  t++;
  if(alive){ 
    if(t%50===0) spawn();
    player.dy *= 0.98;
    player.y += player.dy;
    player.y = Math.max(player.r, Math.min(cvs.height-player.r, player.y));
    orbs.forEach(o=>o.x-=o.v);
    orbs = orbs.filter(o=>o.x>-20);
    // colisiones
    for(const o of orbs){
      const dx = o.x-player.x, dy=o.y-player.y;
      if(Math.hypot(dx,dy) < o.r+player.r){ alive=false; break; }
      if(o.x<player.x && !o.scored){ o.scored=true; score++; scoreEl.textContent=score; }
    }
  }

  // render
  ctx.clearRect(0,0,cvs.width,cvs.height);
  // fondo gradiente
  const g=ctx.createLinearGradient(0,0,0,cvs.height);
  g.addColorStop(0,'#0b0b0f'); g.addColorStop(1,'#7a5cff');
  ctx.fillStyle=g; ctx.fillRect(0,0,cvs.width,cvs.height);

  // player
  ctx.beginPath(); ctx.fillStyle='#eaeaf2';
  ctx.arc(player.x,player.y,player.r,0,Math.PI*2); ctx.fill();

  // orbs
  ctx.fillStyle='#111';
  orbs.forEach(o=>{{ctx.beginPath();ctx.arc(o.x,o.y,o.r,0,Math.PI*2);ctx.fill();}});

  if(!alive){ ctx.fillStyle='#eaeaf2'; ctx.fillText('Perdiste — Enter para reiniciar', cvs.width/2-110, cvs.height/2); }
  requestAnimationFrame(loop);
}

window.addEventListener('keydown',e=>{{
  if(e.code==='Space') player.dy -= 4;
  if(e.code==='Enter' && !alive) restart();
}});
resetBtn.onclick = ()=>restart();

function restart(){{
  orbs=[]; score=0; scoreEl.textContent=0; alive=true; player.y=cvs.height/2; player.dy=0; t=0;
}}

loop();
</script>
</body>
</html>
"""
    (out / "index.html").write_text(html, encoding="utf-8")

    meta = {
        "type": "game",
        "title": title,
        "created_at": dt.datetime.now().isoformat(),
        "path": str(out),
        "controls": "Barra espaciadora para subir. Enter o botón para reiniciar.",
        "win_condition": "Superar tantos orbes como sea posible (score)."
    }
    (out / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(out)

