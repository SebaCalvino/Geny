import datetime as dt
from pathlib import Path

GAME_HTML = """<!DOCTYPE html>
<html lang="es"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Orbit Runner — Tektra</title>
<style>
  body{margin:0;background:#0b0b12;color:#f5f6fb;font-family:system-ui}
  canvas{display:block;margin:4vh auto;border:1px solid #222;background:#111}
  .hud{max-width:820px;margin:0 auto;display:flex;justify-content:space-between;padding:1rem}
  .btn{background:#7c5cff;color:#fff;padding:.5rem .9rem;border-radius:.5rem;text-decoration:none}
</style>
</head><body>
<div class="hud">
  <div>Puntuación: <span id="score">0</span></div>
  <a class="btn" href="#" onclick="resetGame();return false;">Reiniciar</a>
</div>
<canvas id="cv" width="720" height="480" aria-label="Juego simple"></canvas>
<script>
const cv = document.getElementById('cv');
const cx = cv.getContext('2d');
let t=0, score=0, alive=true, px=360, py=380, vx=0;

document.addEventListener('keydown', e=>{
  if(e.key==='ArrowLeft') vx=-4;
  if(e.key==='ArrowRight') vx=4;
});
document.addEventListener('keyup', e=>{
  if(e.key==='ArrowLeft' || e.key==='ArrowRight') vx=0;
});

function resetGame(){
  t=0; score=0; alive=true; px=360; py=380; vx=0;
}
function spawnEnemy(i){
  const r = 80 + 40*Math.sin((t+i)*0.5);
  const cx0 = 360, cy0 = 220;
  const ang = (t*0.02 + i)*1.2;
  return {x: cx0 + Math.cos(ang)*r, y: cy0 + Math.sin(ang)*r, r: 10+5*((i%3)==0)};
}
function loop(){
  requestAnimationFrame(loop);
  t++;
  cx.clearRect(0,0,cv.width,cv.height);

  // Player
  px += vx;
  px = Math.max(20, Math.min(cv.width-20, px));
  cx.fillStyle = '#7c5cff';
  cx.beginPath(); cx.arc(px, py, 12, 0, Math.PI*2); cx.fill();

  // Enemies
  let hit=false;
  for(let i=0;i<20;i++){
    const e=spawnEnemy(i);
    cx.fillStyle = '#a7a9b5';
    cx.beginPath(); cx.arc(e.x, e.y, e.r, 0, Math.PI*2); cx.fill();
    const dx=px-e.x, dy=py-e.y;
    if(Math.hypot(dx,dy) < (12+e.r)) hit=true;
  }
  if(!hit && alive){ score++; document.getElementById('score').textContent=score; }
  if(hit) alive=false;
  if(!alive){
    cx.fillStyle='#fff'; cx.fillText('Perdiste — Reinicia', 280, 240);
  }
}
loop();
</script>
</body></html>
"""

def generate_game(base_output_dir: Path):
    folder = Path(base_output_dir) / f"game_orbit_runner_{dt.datetime.now().strftime('%H%M%S')}"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "index.html").write_text(GAME_HTML, encoding="utf-8")
    return folder
