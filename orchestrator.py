import os, time, random, sqlite3, json, datetime
from pathlib import Path
from factories.factory_images import make_images
from factories.factory_websites import make_website
from factories.factory_games import make_game
import yaml

def load_cfg():
    with open("config.yaml", "r") as f: return yaml.safe_load(f)

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

def today_key(): return datetime.date.today().isoformat()

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

def main_loop():
    cfg = load_cfg()
    ensure_db(cfg["paths"]["db"])
    out_root = Path(cfg["paths"]["output"]); out_root.mkdir(parents=True, exist_ok=True)

    while True:
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

if __name__ == "__main__":
    main_loop()
