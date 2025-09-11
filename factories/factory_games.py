from pathlib import Path
import textwrap, uuid

def make_game(outdir: Path):
    gdir = outdir / f"game_snake_{str(uuid.uuid4())[:6]}"
    gdir.mkdir(parents=True, exist_ok=True)
    (gdir/"index.html").write_text(textwrap.dedent("""\
    <!doctype html><html lang="es"><meta charset="utf-8">
    <title>Snake</title><canvas id="c" width="400" height="400"></canvas>
    <style>body{display:grid;place-items:center;height:100vh;font-family:system-ui}</style>
    <script>
    const cv=document.getElementById('c'), ctx=cv.getContext('2d');
    let grid=20, vx=1, vy=0, snake=[{x:10,y:10}], apple={x:5,y:5};
    function rnd(){return Math.floor(Math.random()*20)}
    function tick(){
      const head={x:snake[0].x+vx, y:snake[0].y+vy};
      if(head.x<0) head.x=19; if(head.x>19) head.x=0; if(head.y<0) head.y=19; if(head.y>19) head.y=0;
      if(snake.some(s=>s.x===head.x&&s.y===head.y)) snake=[{x:10,y:10}], vx=1,vy=0;
      snake.unshift(head);
      if(head.x===apple.x && head.y===apple.y){ apple={x:rnd(),y:rnd()} } else { snake.pop() }
      ctx.clearRect(0,0,400,400);
      ctx.fillStyle="#222"; ctx.fillRect(0,0,400,400);
      ctx.fillStyle="#0f0"; snake.forEach(s=>ctx.fillRect(s.x*grid, s.y*grid, grid-2, grid-2));
      ctx.fillStyle="#f00"; ctx.fillRect(apple.x*grid, apple.y*grid, grid-2, grid-2);
    }
    document.addEventListener('keydown',e=>{
      if(e.key==='ArrowUp'&&vy!==1){vx=0;vy=-1}
      if(e.key==='ArrowDown'&&vy!==-1){vx=0;vy=1}
      if(e.key==='ArrowLeft'&&vx!==1){vx=-1;vy=0}
      if(e.key==='ArrowRight'&&vx!==-1){vx=1;vy=0}
    });
    setInterval(tick,120);
    </script></html>
    """), encoding="utf-8")
    return "Juego — Snake", gdir.relative_to(Path.cwd()), 0.00, {"type": "snake"}
