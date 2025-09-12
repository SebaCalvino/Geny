# factories/factory_games.py
from __future__ import annotations
from pathlib import Path
from datetime import datetime
import random, string

# ==========================================================
# Generador de 300+ variantes estéticas y minimalistas
# Mecánicas incluidas:
#   - snake, pong, memory, flappy, breakout, dodge, runner, aim
# Cada una se instancia con paletas, velocidades y tamaños aleatorios.
# ==========================================================

PALETTES = [
    ("#0EA5E9", "#22D3EE", "#F8FAFC", "#0F172A"),  # azul/aqua
    ("#22C55E", "#84CC16", "#F9FAFB", "#052E16"),  # verde
    ("#A78BFA", "#F0ABFC", "#FAF5FF", "#1F1147"),  # lila/rosa
    ("#F59E0B", "#EF4444", "#FFF7ED", "#220A00"),  # naranja/rojo
    ("#06B6D4", "#14B8A6", "#ECFEFF", "#022C22"),  # teal
    ("#FB7185", "#FDA4AF", "#FFF1F2", "#3B0A14"),  # coral
    ("#94A3B8", "#CBD5E1", "#F1F5F9", "#0F172A"),  # neutro frío
    ("#F472B6", "#C084FC", "#FAF5FF", "#1F2937"),  # magenta/lila
]

def pick_palette():
    return random.choice(PALETTES)

def slug(n=6):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=n))

def base_css(c1, c2, light, dark):
    # CSS compartido + variables de paleta
    return f"""
:root {{
  --c1:{c1}; --c2:{c2}; --bg:{light}; --fg:{dark};
}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0;background:var(--bg);color:var(--fg);
  font:16px/1.6 ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto}}
h1{{font-weight:700;letter-spacing:.3px;margin:16px 0 8px}}
.wrapper{{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px}}
canvas{{background:linear-gradient(135deg,var(--bg), #ffffff);border:4px solid var(--c1);
  border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.18)}}
.button{{padding:8px 12px;border-radius:10px;border:1px solid var(--c1);color:var(--c1);background:#fff;cursor:pointer}}
.badge{{display:inline-block;background:var(--c1);color:#fff;border-radius:999px;padding:4px 10px;font-size:.85rem}}
.footer{{position:fixed;bottom:8px;left:0;right:0;text-align:center;font-size:.9rem;opacity:.7}}
    """.strip()

def frame_html(title, css, body, script):
    return f"""<!doctype html>
<html lang="es">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<style>{css}</style>
<div class="wrapper">
  <h1>{title}</h1>
  {body}
</div>
<div class="footer">Hecho por Maker Bot • estética minimal</div>
<script>
{script}
</script>
</html>
"""

# ------------------------- Plantillas -------------------------

def game_snake(cfg):
    N = random.choice([18, 20, 22, 24])
    speed = random.choice([80, 90, 100, 110])
    c1, c2, light, dark = cfg["palette"]
    css = base_css(c1, c2, light, dark)
    body = f'<canvas id="cv" width="{N*20}" height="{N*20}"></canvas>'
    js = f"""
const N={N}, S=20;
const cvs=document.getElementById('cv'), ctx=cvs.getContext('2d');
let snake=[{{x:Math.floor(N/2),y:Math.floor(N/2)}}], dir={{x:1,y:0}};
let food={{x:0,y:0}}, alive=true, tick={speed};
function rnd(n){{return Math.floor(Math.random()*n)}}
function placeFood(){{while(true){{food={{x:rnd(N),y:rnd(N)}}; if(!snake.some(p=>p.x==food.x&&p.y==food.y)) return;}}}}
placeFood();
addEventListener('keydown',e=>{{
  const k=e.key.toLowerCase();
  if((k==='arrowup'||k==='w')&&dir.y!=1) dir={{x:0,y:-1}};
  if((k==='arrowdown'||k==='s')&&dir.y!=-1) dir={{x:0,y:1}};
  if((k==='arrowleft'||k==='a')&&dir.x!=1) dir={{x:-1,y:0}};
  if((k==='arrowright'||k==='d')&&dir.x!=-1) dir={{x:1,y:0}};
}});
function step(){{
  if(!alive) return;
  const h={{x:(snake[0].x+dir.x+N)%N, y:(snake[0].y+dir.y+N)%N}};
  if(snake.some(p=>p.x==h.x&&p.y==h.y)){{alive=false; return;}}
  snake.unshift(h);
  if(h.x==food.x&&h.y==food.y){{placeFood(); if(tick>60) tick-=4;}}
  else snake.pop();
  // draw
  ctx.clearRect(0,0,cvs.width,cvs.height);
  for(let i=0;i<N;i++) for(let j=0;j<N;j++){{ if((i+j)%2==0){{ctx.fillStyle='{light}'; ctx.globalAlpha=.6; ctx.fillRect(i*S,j*S,S,S); ctx.globalAlpha=1;}}}}
  ctx.fillStyle='{c1}'; snake.forEach(p=>ctx.fillRect(p.x*S,p.y*S,S,S));
  ctx.fillStyle='{c2}'; ctx.fillRect(food.x*S,food.y*S,S,S);
  setTimeout(step,tick);
}} step();
"""
    return frame_html("Snake", css, body, js)

def game_pong(cfg):
    W,H=640,420
    c1,c2,light,dark=cfg["palette"]
    css=base_css(c1,c2,light,dark)
    body=f'<canvas id="cv" width="{W}" height="{H}"></canvas>'
    js=f"""
const cvs=document.getElementById('cv'),ctx=cvs.getContext('2d');
const user={{x:12,y:180,w:10,h:80,c:'{c1}'}}, com={{x:{W-22},y:180,w:10,h:80,c:'{c2}'}};
const ball={{x:{W//2},y:{H//2},r:8,vx:4,vy:3,c:'#facc15'}};
cvs.addEventListener('mousemove',e=>{{user.y=e.offsetY-user.h/2;}});
function draw(){{ctx.fillStyle='{light}';ctx.fillRect(0,0,cvs.width,cvs.height);
  [user,com].forEach(p=>{{ctx.fillStyle=p.c;ctx.fillRect(p.x,p.y,p.w,p.h);}});
  ctx.beginPath();ctx.fillStyle=ball.c;ctx.arc(ball.x,ball.y,ball.r,0,Math.PI*2);ctx.fill();}}
function update(){{ball.x+=ball.vx;ball.y+=ball.vy;
  if(ball.y<ball.r||ball.y>cvs.height-ball.r)ball.vy*=-1;
  com.y+=(ball.y-(com.y+com.h/2))*0.08;
  const hit=(p)=>ball.x+ball.r>p.x&&ball.x-ball.r<p.x+p.w&&ball.y+ball.r>p.y&&ball.y-ball.r<p.y+p.h;
  if(hit(user)||hit(com)) ball.vx*=-1;
  if(ball.x<0||ball.x>cvs.width) ball.x={W//2},ball.y={H//2};}}
setInterval(()=>{{update();draw();}},1000/60);
"""
    return frame_html("Pong", css, body, js)

def game_memory(cfg):
    c1,c2,light,dark=cfg["palette"]
    css=base_css(c1,c2,light,dark)+"""
.grid{display:grid;grid-template-columns:repeat(4,86px);gap:12px}
.card{width:86px;height:86px;background:#fff;border:2px solid var(--c1);
  border-radius:12px;display:flex;align-items:center;justify-content:center;
  box-shadow:0 6px 18px rgba(0,0,0,.12);font-size:32px;cursor:pointer}
.card.matched{background:var(--c1);color:#fff;border-color:var(--c2)}
"""
    body='<div class="grid" id="grid"></div>'
    js="""
const EMO=["🍎","🍊","🍋","🍓","🍇","🥥","🍍","🥝"];
let cards=[...EMO,...EMO].sort(()=>Math.random()-0.5);
const grid=document.getElementById('grid');
let first=null,lock=false,matched=0;
cards.forEach(sym=>{
  const el=document.createElement('div'); el.className='card'; el.textContent='?';
  el.onclick=()=>{
    if(lock||el.classList.contains('matched')||el===first) return;
    el.textContent=sym;
    if(!first){ first=el; return; }
    lock=true;
    if(first.textContent===el.textContent){
      first.classList.add('matched'); el.classList.add('matched'); matched+=2;
      first=null; lock=false; if(matched===cards.length) setTimeout(()=>alert('¡Ganaste!'),100);
    } else {
      setTimeout(()=>{ first.textContent='?'; el.textContent='?'; first=null; lock=false; }, 650);
    }
  };
  grid.appendChild(el);
});
"""
    return frame_html("Memory", css, body, js)

def game_flappy(cfg):
    W,H=420,520
    c1,c2,light,dark=cfg["palette"]
    gap=random.choice([110,130,150])
    css=base_css(c1,c2,light,dark)
    body=f'<canvas id="cv" width="{W}" height="{H}"></canvas><button class="button" id="btn">Saltar</button>'
    js=f"""
const c=document.getElementById('cv'),ctx=c.getContext('2d'),btn=document.getElementById('btn');
let y={H//2}, v=0, g=0.7, pipes=[{{x:{W},y: -Math.random()*150}}], gap={gap};
function jump(){{v=-10;}} addEventListener('keydown',jump); btn.onclick=jump;
function draw(){{ctx.fillStyle='{light}';ctx.fillRect(0,0,c.width,c.height);
  ctx.fillStyle='{c1}'; ctx.fillRect(80,y,24,24);
  for(let i=0;i<pipes.length;i++){{const p=pipes[i];
    ctx.fillStyle='{c2}'; ctx.fillRect(p.x,p.y,50,220);
    ctx.fillRect(p.x,p.y+220+gap,50,c.height);
    p.x-=2; if(p.x==220)pipes.push({{x:c.width,y:-Math.random()*150}});
  }}
}}
function step(){{v+=g;y+=v; if(y>c.height-24) location.reload();
  const p=pipes[0]; if(p && 80+24>=p.x && 80<=p.x+50 && (y<=p.y+220 || y+24>=p.y+220+gap)) location.reload();
  draw(); requestAnimationFrame(step);}}
step();
"""
    return frame_html("Flappy Block", css, body, js)

def game_breakout(cfg):
    c1,c2,light,dark=cfg["palette"]
    W,H=600,420; cols=8; rows=5
    css=base_css(c1,c2,light,dark)
    body=f'<canvas id="cv" width="{W}" height="{H}"></canvas>'
    js=f"""
const cvs=document.getElementById('cv'),ctx=cvs.getContext('2d');
const P={{x:{W//2-40},y:{H-24},w:80,h:10}}, B={{x:{W//2},y:{H//2},r:7,vx:3,vy:-3}};
let bricks=[];
for(let r=0;r<{rows};r++) for(let c=0;c<{cols};c++) bricks.push({{x:20+c*70,y:40+r*22,w:60,h:12,alive:true}});
addEventListener('mousemove',e=>{{P.x=e.offsetX-P.w/2}});
function draw(){{ctx.fillStyle='{light}';ctx.fillRect(0,0,cvs.width,cvs.height);
  ctx.fillStyle='{c1}';ctx.fillRect(P.x,P.y,P.w,P.h);
  ctx.beginPath();ctx.fillStyle='{c2}';ctx.arc(B.x,B.y,B.r,0,Math.PI*2);ctx.fill();
  bricks.forEach(b=>{{if(b.alive){{ctx.fillStyle='#{random.randrange(0x100000,0xFFFFFF):06x}';ctx.fillRect(b.x,b.y,b.w,b.h);}}}});
}}
function update(){{B.x+=B.vx;B.y+=B.vy; if(B.x<0||B.x>cvs.width)B.vx*=-1; if(B.y<0)B.vy*=-1;
  if(B.y>cvs.height) location.reload();
  if(B.x>B.x-B.r && B.x>P.x && B.x<P.x+P.w && B.y+B.r>P.y) B.vy*=-1;
  bricks.forEach(b=>{{if(!b.alive)return; if(B.x>B.x-B.r && B.x>b.x && B.x<b.x+b.w && B.y>b.y && B.y<b.y+b.h){{b.alive=false;B.vy*=-1;}}}});
}}
setInterval(()=>{{update();draw();}},1000/60);
"""
    return frame_html("Breakout", css, body, js)

def game_dodge(cfg):
    W,H=420,540
    c1,c2,light,dark=cfg["palette"]
    speed=random.choice([2,3,4])
    css=base_css(c1,c2,light,dark)
    body=f'<canvas id="cv" width="{W}" height="{H}"></canvas>'
    js=f"""
const cvs=document.getElementById('cv'),ctx=cvs.getContext('2d');
let x={W//2}, y={H-60}; let bullets=[];
addEventListener('mousemove',e=>{{x=e.offsetX}});
setInterval(()=>bullets.push({{x:Math.random()*cvs.width,y:-10}}),450);
function step(){{ctx.fillStyle='{light}';ctx.fillRect(0,0,cvs.width,cvs.height);
  ctx.fillStyle='{c1}'; ctx.fillRect(x-12,y,24,24);
  bullets.forEach(b=>{{ctx.fillStyle='{c2}';ctx.fillRect(b.x,b.y,8,16); b.y+={speed};
    if(b.x>x-12 && b.x<x+12 && b.y+16>y && b.y<y+24) location.reload();
  }});
  requestAnimationFrame(step);
}} step();
"""
    return frame_html("Dodge", css, body, js)

def game_runner(cfg):
    W,H=640,240
    c1,c2,light,dark=cfg["palette"]
    css=base_css(c1,c2,light,dark)
    body=f'<canvas id="cv" width="{W}" height="{H}"></canvas><button class="button" id="j">Saltar</button>'
    js="""
const c=document.getElementById('cv'),ctx=c.getContext('2d'),btn=document.getElementById('j');
let x=50,y=190,v=0,g=0.8,obs=[],t=0;
function jump(){ if(y>=190) v=-12; } addEventListener('keydown',jump); btn.onclick=jump;
function loop(){ t++; if(t%80==0) obs.push({x:c.width,y:190-20*(Math.random()<.3),w:16,h:20+(Math.random()<.3)*20});
  v+=g;y+=v;if(y>190){y=190;v=0}
  ctx.fillStyle="#fff";ctx.fillRect(0,0,c.width,c.height);
  ctx.fillStyle="#ddd";ctx.fillRect(0,210,c.width,2);
  ctx.fillStyle="#0ea5e9";ctx.fillRect(x,y,22,22);
  ctx.fillStyle="#ef4444"; obs.forEach(o=>{o.x-=4;ctx.fillRect(o.x,o.y,o.w,o.h);
    if(x<o.x+o.w&&x+22>o.x&&y<o.y+o.h&&y+22>o.y) location.reload();
  });
  requestAnimationFrame(loop);
} loop();
"""
    return frame_html("Runner", css, body, js)

def game_aim(cfg):
    c1,c2,light,dark=cfg["palette"]
    size=random.choice([440,520,600])
    css=base_css(c1,c2,light,dark)
    body=f'<canvas id="cv" width="{size}" height="{size}"></canvas><div><span class="badge" id="score">0</span></div>'
    js=f"""
const c=document.getElementById('cv'),ctx=c.getContext('2d'),sc=document.getElementById('score');
let x=100,y=100,r=14,score=0;
function rnd(n){{return Math.floor(Math.random()*n)}}
function place(){{x=rnd(c.width-2*r)+r;y=rnd(c.height-2*r)+r;}}
place();
c.addEventListener('click',e=>{{
  const rect=c.getBoundingClientRect(); const mx=e.clientX-rect.left, my=e.clientY-rect.top;
  if(Math.hypot(mx-x,my-y)<=r){{score++; sc.textContent=score; place();}}
}});
function loop(){{ctx.fillStyle='{light}';ctx.fillRect(0,0,c.width,c.height);
  ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fillStyle='{c1}';ctx.fill(); requestAnimationFrame(loop);}}
loop();
"""
    return frame_html("Aim Trainer", css, body, js)

MECHANICS = [
    game_snake, game_pong, game_memory, game_flappy,
    game_breakout, game_dodge, game_runner, game_aim
]

# ------------------------- Fábrica principal -------------------------

def make_game(base_dir: Path, topic_dir: Path | None = None):
    """
    Devuelve un juego aleatorio, con parámetros y paleta aleatoria.
    El espacio de combinaciones supera las 300 variantes únicas.
    """
    mech = random.choice(MECHANICS)
    palette = pick_palette()
    cfg = {"palette": palette, "seed": random.randrange(1<<30)}

    # Construcción de carpeta de salida
    today = datetime.utcnow().strftime("%Y-%m-%d")
    mech_name = mech.__name__.replace("game_", "")
    gdir = base_dir / today / f"game_{mech_name}_{slug()}"
    gdir.mkdir(parents=True, exist_ok=True)

    # HTML final
    html = mech(cfg)
    (gdir / "index.html").write_text(html, encoding="utf-8")

    title_map = {
        "snake": "Juego — Snake",
        "pong": "Juego — Pong",
        "memory": "Juego — Memory",
        "flappy": "Juego — Flappy Block",
        "breakout": "Juego — Breakout",
        "dodge": "Juego — Dodge",
        "runner": "Juego — Runner",
        "aim": "Juego — Aim Trainer",
    }
    title = title_map.get(mech_name, f"Juego — {mech_name.capitalize()}")
    # ¡IMPORTANTE! No usamos relative_to para evitar errores en CI
    relpath = str(gdir)
    cost = 0.0
    meta = {
        "mechanic": mech_name,
        "palette": palette,
        "seed": cfg["seed"]
    }
    return title, relpath, cost, meta
