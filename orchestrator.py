import os, time, random, sqlite3, json, datetime
from pathlib import Path
import yaml

# fábricas
from factories.factory_images import make_images
from factories.factory_websites import make_website
from factories.factory_games import make_game

# -------- Config por defecto (fallback) --------
DEFAULT_CFG = {
    "mode": os.environ.get("MODE", "local"),
    "interval_minutes": 20,
    "daily_budget_usd": 1.5,
    "max_items_per_day": {"images": 6, "websites": 3, "games": 2},
    "random_weights": {"images": 0.5, "websites": 0.35, "games": 0.15},
    "providers": {"images": {"engine": "openai"}, "code": {"engine": "openai"}},
    "paths": {"output": "./output", "db": "./log/status.db"},
    "telegram": {"enabled": False}
}

PAUSE_FLAG = Path("./log/pause.flag")

# -------- Utilidades --------
def load_cfg():
    # 1) Permite override por variable de entorno CONFIG_PATH
    cfg_path = os.environ.get("CONFIG_PATH")
    if cfg_path and Path(cfg_path).is_file():
        with open(cfg_path, "r") as f:
            return {**DEFAULT_CFG, **yaml.safe_load(f)}
    # 2) Busca config local .yaml o .yml
    here = Path(__file__).parent
    for candidate in [here / "config.yaml", here / "config.yml", Path.cwd() / "config.yaml", Path.cwd() / "config.yml"]:
        if candidate.is_file():
            with open(candidate, "r") as f:
                return {**DEFAULT_CFG, **yaml.safe_load(f)}
    print("[warn] config no encontrada, usando DEFAULT_CFG")
    return DEFAULT_CFG

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
    weights = cfg["random_weights"]
    candidates = []
    if counters["images"] < cfg["max_items_per_day"]["images"]:
        candidates += ["images"] * int(weights["images"]*100)
    if counters["websites"] < cfg["max_items_per_day"]["websites"]:
        candidates += ["websites"] * int(weights["websites"]*100)
    if counters["games"] < cfg["max_items_per_day"]["games"]:
        candidates += ["games"] * int(weights["games"]*100)
    return random.choice(candidates) if candidates else None

# -------- Iteración única (para GitHub Actions) --------
def one_iteration(cfg):
    day = today_key()
    con = sqlite3.connect(cfg["paths"]["db"])
    counters = read_counters(con, day)

    # respetar pausa si existiera
    if PAUSE_FLAG.exists():
        con.close()
        print("[maker-bot] en pausa")
        return "paused"

    # límites de presupuesto
    if counters["cost"] >= cfg["daily_budget_usd"]:
        con.close()
        print("[maker-bot] presupuesto diario alcanzado")
        return "budget_exceeded"

    kind = pick_kind(cfg, counters)
    if not kind:
        con.close()
        print("[maker-bot] no hay candidatos por límites diarios")
        return "no_candidates"

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

# -------- Loop continuo (para uso local/servidor) --------
def main_loop():
    cfg = load_cfg()
    ensure_db(cfg["paths"]["db"])
    out_root = Path(cfg["paths"]["output"]); out_root.mkdir(parents=True, exist_ok=True)

    while True:
        if PAUSE_FLAG.exists():
            time.sleep(30)
            continue

        day = today_key()
        con = sqlite3.connect(cfg["paths"]["db"])
        counters = read_counters(con, day)

        if counters["cost"] >= cfg["daily_budget_usd"]:
            con.close(); time.sleep(60*15); continue

        kind = pick_kind(cfg, counters)
        if not kind:
            con.close(); time.sleep(60*30); continue

        today_dir = out_root / day
        today_dir.mkdir(exist_ok=True)

        try:
            if kind == "images":
                title, relpath, cost, meta = make_images(today_dir)
                counters["images"] += 1
            elif kind == "websites":
                title, relpath, cost, meta = make_website(today_dir)
                counters["websites"] += 1
            else:
                title, relpath, cost, meta = make_game(today_dir)
                counters["games"] += 1

            counters["cost"] += cost
            register_item(con, kind, title, str(relpath), cost, meta)
            write_counters(con, day, counters)

        except Exception as e:
            print("Error:", e)

        con.close()
        time.sleep(cfg["interval_minutes"]*60)

# -------- Entry point --------
if __name__ == "__main__":
    cfg = load_cfg()
    ensure_db(cfg["paths"]["db"])
    run_once = os.environ.get("RUN_ONCE") == "1" or cfg.get("mode") == "github_actions"
    if run_once:
        print(one_iteration(cfg))
    else:
        main_loop()
