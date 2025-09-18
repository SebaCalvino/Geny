#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import random
import sys
from pathlib import Path

# --- Carga config ------------------------------------------------------------
DEFAULT_WEIGHTS = {"images": 0.4, "webs": 0.4, "games": 0.2}
DEFAULT_OUTPUT = "output"

try:
    import yaml
except ImportError:
    yaml = None

def load_config():
    cfg = {}
    cfg_path = Path("config.yaml")
    if yaml and cfg_path.exists():
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
    return cfg

# --- Logging simple ----------------------------------------------------------
def log(msg):
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg}")

# --- Factories (import dinámico con fallback) --------------------------------
def _import_factory(modname, funcname):
    try:
        mod = __import__(modname, fromlist=[funcname])
        return getattr(mod, funcname)
    except Exception as e:
        log(f"ERROR importando {modname}.{funcname}: {e}")
        return None

def choose_type(weights):
    keys = list(weights.keys())
    vals = list(weights.values())
    # random.choices devuelve lista; tomamos el único elemento
    return random.choices(keys, weights=vals, k=1)[0]

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def today_folder(base_dir):
    d = dt.datetime.now().strftime("%Y-%m-%d")
    return Path(base_dir) / d

def write_run_index(out_dir, items):
    idx = {
        "run_time": dt.datetime.now().isoformat(),
        "count": len(items),
        "items": items,
    }
    with open(out_dir / "index.json", "w", encoding="utf-8") as f:
        json.dump(idx, f, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=3, help="cuántos ítems generar en este run")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    cfg = load_config()
    weights = (cfg.get("weights") or DEFAULT_WEIGHTS)
    base_dir = (cfg.get("output", {}) or {}).get("base_dir", DEFAULT_OUTPUT)

    gen_web = _import_factory("factories.web_factory", "generate_site")
    gen_img = _import_factory("factories.image_factory", "generate_image")
    gen_game = _import_factory("factories.game_factory", "generate_game")

    if not any([gen_web, gen_img, gen_game]):
        log("No se pudieron cargar factories. Abort.")
        sys.exit(1)

    out_dir = today_folder(base_dir)
    ensure_dir(out_dir)

    generated = []
    counters = {"webs": 0, "images": 0, "games": 0}

    for i in range(args.count):
        kind = choose_type(weights)
        # Fallback si falta una factory: elegir otra al vuelo
        if kind == "webs" and not gen_web:
            kind = "images" if gen_img else "games"
        if kind == "images" and not gen_img:
            kind = "webs" if gen_web else "games"
        if kind == "games" and not gen_game:
            kind = "webs" if gen_web else "images"

        log(f"INFO: Generating {kind}...")

        if args.dry_run:
            path = f"{out_dir}/dry-run-{kind}-{i}"
        else:
            if kind == "webs":
                path = gen_web(out_dir)
            elif kind == "images":
                path = gen_img(out_dir)
            else:
                path = gen_game(out_dir)

        counters["webs" if kind=="webs" else kind] += 1
        generated.append({"type": kind, "path": str(path)})

    write_run_index(out_dir, generated)
    log(f"==== Run complete ====")
    log(f"Generated -> webs: {counters['webs']}, images: {counters['images']}, games: {counters['games']}")
    log(f"Output: {out_dir}")

if __name__ == "__main__":
    main()
