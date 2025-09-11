# factories/factory_games.py
from pathlib import Path
import random

def make_game(output_dir: Path):
    """
    Crea un mini Snake de una sola página en:
      output/<YYYY-MM-DD>/game_snake_<id>/index.html

    Devuelve: (title, path_str, cost, meta_dict)
    NOTA: devolvemos str(gdir) (no usamos .relative_to()) para evitar
    el ValueError de rutas en GitHub Actions.
    """
    gdir = output_dir / f"game_snake_{random.randint(0, 16**6):06x}"
    gdir.mkdir(parents=True, exist_ok=True)

    html = """<!doctype html>
<html lang="es">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Snake</title>
<style>
  html,body{height:100%;margin:0;background:#111;color:#eee;font-family:system-ui,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
  .wrap{height:100%;display:grid;place-items:center;gap:16px}
  canvas{image-rendering:pixelated;background:#000;box-shadow:0 0 0 3px #333, 0 0 30px #0f0 inset}
  .hud{display:flex;gap:12px;align-items:center;justify-content:center}
  .btn{padding:8px 12px;border:1px solid #444;background:#1a1a1a;color:#eee;cursor:pointer}
</style>
<div class="wrap">
  <canvas id="cv" width="400" height="400"></canvas>
  <div class="hud">
    <div>Score: <span id="score">0</span></div>
    <button class="btn" id="reset">Reiniciar</button>
  </div>
</div>
<script>
const cvs = document.getElementById('cv');
const ctx = cvs.getContext('2d');
const N = 20;                 // celdas por lado
const S = cvs.width / N;      // tamaño de celda
let snake, dir, food, score, tick, alive;

function rnd(max){ return Math.floor(Math.random()*max); }
function placeFood(){
  while(true){
    food = {x:rnd(N), y:rnd(N)};
    if(!snake.some(p=>p.x===food.x && p.y===food.y)) break;
  }
}
function reset(){
  snake = [{x:10,y:10}];
  dir = {x:1,y:0};
  score = 0;
  document.getElementById('score').textContent = score;
  placeFood();
  tick = 120;  // ms
  alive = true;
}
reset();

document.getElementById('reset').onclick = reset;

window.addEventListener('keydown', e=>{
  const k = e.key.toLowerCase();
  if(k==='arrowup'    || k==='w'){ if(dir.y!== 1) dir={x:0,y:-1}; }
  if(k==='arrowdown'  || k==='s'){ if(dir.y!==-1) dir={x:0,y: 1}; }
  if(k==='arrowleft'  || k==='a'){ if(dir.x!== 1) dir={x:-1,y:0}; }
  if(k==='arrowright' || k==='d'){ if(dir.x!==-1) dir={x: 1,y:0}; }
});

function step(){
  if(!alive) return;
  const head = {x: (snake[0].x + dir.x + N) % N, y: (snake[0].y + dir.y + N) % N};
  // choque con el cuerpo
  if(snake.some(p=>p.x===head.x && p.y===head.y)){ alive=false; return; }
  snake.unshift(head);

  // comer
  if(head.x===food.x && head.y===food.y){
    score++; document.getElementById('score').textContent = score;
    placeFood();
    if(tick>60) tick-=4; // acelera un poco
  }else{
    snake.pop();
  }

  // dibujar
  ctx.clearRect(0,0,cvs.width,cvs.height);
  // grid tenue
  ctx.fillStyle = '#020';
  for(let i=0;i<N;i++){ for(let j=0;j<N;j++){
    if((i+j)%2===0) ctx.fillRect(i*S, j*S, S, S);
  }}
  // comida
  ctx.fillStyle = '#f33';
  ctx.fillRect(food.x*S, food.y*S, S, S);
  // snake
  ctx.fillStyle = '#0f0';
  snake.forEach((p,i)=>{
    ctx.fillRect(p.x*S, p.y*S, S, S);
  });

  setTimeout(step, tick);
}
step();
</script>
</html>"""

    (gdir / "index.html").write_text(html, encoding="utf-8")

    # Devolvemos string del directorio (sin relative_to) para evitar errores en CI
    return "Juego — Snake", str(gdir), 0.0, {"type": "snake"}
