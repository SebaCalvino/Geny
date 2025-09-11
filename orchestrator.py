import os, time, random, sqlite3, json, datetime
from pathlib import Path

# --- YAML opcional (si no está instalado, seguimos con defaults) ---
try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

# ---------------------- CONFIG DEFAULT ----------------------
DEFAULT_CFG = {
    "mode": os.environ.get("MODE", "local"),
    "interval_minutes": 20,
    "daily_budget_usd": 1.5,
    "max_items_per_day": {"images": 6, "websites": 3, "games": 2},
    "random_weights": {"images": 0.5, "websites": 0.35, "games": 0.15},
    "paths": {"output": "./output", "db": "./log/status.db"},
}
PAUSE_FLAG = Path("./log/pause.flag")

# ---------------------- CARGA CONFIG ------------------------
def load_cfg():
    cfg = dict(DEFAULT_CFG)
    # CONFIG_PATH por env
    cfg_path = os.environ.get("CONFIG_PATH")
    candidates = []
    if cfg_path:
        candidates.append(Path(cfg_path))
    here = Path(__file__).parent
    candidates += [here / "config.yaml", here / "config.yml", Path.cwd() / "config.yaml", Path.cwd() / "config.yml"]
    for p in candidates:
        if p.is_file() and yaml:
            try:
                data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
                cfg.update(data)
                print(f"[maker-bot] usando config: {p}")
                break
            except Exception as e:
                print(f"[warn] no pude leer {p}: {e}")
    return cfg

# ---------------------- IMPORTS PEREZOSOS -------------------
# Si falla importar las factories, usamos backups mínimos para no romper el workflow.
def _safe_factories():
    try:
        from factories.factory_images import make_images  # type: ignore
    except Exception as e:
        print(f"[warn] factory_images no disponible: {e}")
        def make_images(outdir: Path):
            outdir.mkdir(parents=True, exist_ok=True)
            img = outdir / "img_placeholder.png"
            img.write_bytes(b"")  # PNG vacío
            return "Imagen épica — placeholder", img.relative_to(Path.cwd()), 0.0, {"prompt": "placeholder"}
    try:
        from factories.factory_websites import make_website  # type: ignore
    except Exception as e:
        print(f"[warn] factory_websites no disponible: {e}")
        def make_website(outdir: Path):
            site = outdir / "site_placeholder"; site.mkdir(parents=True, exist_ok=True)
            (site/"index.html").write_text("<!doctype html><meta charset='utf-8'><h1>Placeholder</h1>", encoding="utf-8")
            return "Landing — placeholder", site.relative_to(Path.cwd()), 0.0, {"style":"placeholder"}
    try:
        from factories.factory_games import make_game  # type: ignore
    except Exception as e:
        print(f"[warn] factory_games no disponible: {e}")
        def make_game(outdir: Path):
            g = outdir / "game_snake_placeholder"; g.mkdir(parents=True, exist_ok=True)
            (g/"index.html").write_text("<!doctype html><meta charset='utf-8'><h1>Snake Placeholder</h1>", encoding="utf-8")
            return "Juego — Snake (placeholder)", g.relative_to(Path.cwd()), 0.0, {"type":"snake"}
    return make_images, make_website, make_game

make_images, make_website, make_game = _safe_factories()

# ---------------------- DB HELPERS --------------------------
def ensure_db(db_path):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT, kind TEXT, title TEXT, path TEXT, cost REAL DEFAULT 0.0, meta TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS counters (
        day TEXT PRIMARY KEY, cost REAL, images INT, websites INT, games INT
    )""")
    con.commit(); con.close()

def today_key():
    return datetime.date.today().isoformat()

def read_counters(con, day):
    cur = con.cursor()
    cur.execute("SELECT cost, images, websites, games FROM counters WHERE day=?", (day,))
    row = cur.fetchone()
    return {"cost": row[0], "images": row[1], "websites": row[2], "games": row[3]} if row else {"cost":0.0,"images":0,"websites":0,"games":0}

def write_counters(con, day, c):
    cur = con.cursor()
    cur.execute("INSERT OR REPLACE INTO counters(day,cost,images,websites,games) VALUES(?,?,?,?,?)",
                (day, c["cost"], c["images"], c["websites"], c["games"]))
    con.commit()

def register_item(con, kind, title, path, cost=0.0, meta=None):
    cur = con.cursor()
    cur.execute("INSERT INTO items(ts,kind,title,path,cost,meta) VALUES(?,?,?,?,?,?)",
                (datetime.datetime.now().isoformat(), kind, title, path, cost, json.dumps(meta or {})))
    con.commit()

def pick_kind(cfg, counters):
    w = cfg["random_weights"]
    cand = []
    if counters["images"] < cfg["max_items_per_day"]["images"]:
        cand += ["images"] * int(w["images"]*100)
    if counters["websites"] < cfg["max_items_per_day"]["websites"]:
        cand += ["websites"] * int(w["websites"]*100)
    if counters["games"] < cfg["max_items_per_day"]["games"]:
        cand += ["games"] * int(w["games"]*100)
    return random.choice(cand) if cand else None

# ---------------------- UNA ITERACIÓN -----------------------
def one_iteration(cfg):
    day = today_key()
    con = sqlite3.connect(cfg["paths"]["db"])
    counters = read_counters(con, day)

    if PAUSE_FLAG.exists():
        con.close(); print("[maker-bot] pausa activa"); return "paused"
    if counters["cost"] >= cfg["daily_budget_usd"]:
        con.close(); print("[maker-bot] presupuesto alcanzado"); return "budget_exceeded"

    kind = pick_kind(cfg, counters)
    if not kind:
        con.close(); print("[maker-bot] límites diarios alcanzados"); return "no_candidates"

    out_root = Path(cfg["paths"]["output"]); out_root.mkdir(parents=True, exist_ok=True)
    today_dir = out_root / day; today_dir.mkdir(exist_ok=True)

    try:
        if kind == "images":
            title, relpath, cost, meta = make_images(today_dir); counters["images"] += 1
        elif kind == "websites":
            title, relpath, cost, meta = make_website(today_dir); counters["websites"] += 1
        else:
            title, relpath, cost, meta = make_game(today_dir); counters["games"] += 1
        counters["cost"] += cost
        register_item(con, kind, title, str(relpath), cost, meta)
        write_counters(con, day, counters)
        print(f"[maker-bot] created: {kind} -> {relpath}")
    finally:
        con.close()
    return f"ok:{kind}"

# ---------------------- LOOP CONTINUO -----------------------
def main_loop(cfg):
    ensure_db(cfg["paths"]["db"])
    out_root = Path(cfg["paths"]["output"]); out_root.mkdir(parents=True, exist_ok=True)
    while True:
        one_iteration(cfg)
        time.sleep(cfg["interval_minutes"]*60)

# ---------------------- ENTRY POINT ------------------------
if __name__ == "__main__":
    cfg = load_cfg()
    ensure_db(cfg["paths"]["db"])
    run_once = os.environ.get("RUN_ONCE") == "1" or cfg.get("mode") == "github_actions"
    if run_once:
        print(one_iteration(cfg))
    else:
        main_loop(cfg)
