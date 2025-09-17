# -*- coding: utf-8 -*-
"""
Orchestrator — Websites overhaul (con --force)
NO toca tu esquema de output; la ruta viene por flag/env/settings/config.
"""

from __future__ import annotations
import os, sys, json, random, argparse, traceback, re
from pathlib import Path
from datetime import datetime

# -------------------------
# Carga opcional de config
# -------------------------
def _maybe_load_yaml_config() -> dict:
    try:
        import yaml  # type: ignore
    except Exception:
        return {}
    cfg_path = Path("config.yaml")
    if not cfg_path.exists():
        return {}
    try:
        return yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}

# -------------------------
# Resolución de parámetros
# -------------------------
def resolve_output_dir(cli_value: str | None) -> str:
    if cli_value:
        return cli_value
    env = os.getenv("OUTPUT_DIR")
    if env:
        return env
    try:
        import settings  # type: ignore
        if getattr(settings, "OUTPUT_DIR", None):
            return settings.OUTPUT_DIR  # type: ignore
    except Exception:
        pass
    cfg = _maybe_load_yaml_config()
    if isinstance(cfg, dict) and cfg.get("output_dir"):
        return str(cfg["output_dir"])
    raise SystemExit(
        "[orchestrator] ERROR: no se pudo resolver OUTPUT_DIR.\n"
        "Proveé --output-dir, env OUTPUT_DIR, settings.OUTPUT_DIR o config.yaml:output_dir"
    )

def resolve_site_title(cli_value: str | None) -> str:
    if cli_value:
        return cli_value
    return os.getenv("SITE_TITLE") or random.choice([
        "NébulaCare", "Clinia Nova", "VitalNimbus", "MediOrion",
        "PulsoDigital", "AuroraSalud", "Higia Cloud"
    ])

def resolve_palette_index(cli_value: str | None) -> int | None:
    if cli_value is not None:
        try:
            return int(cli_value)
        except ValueError:
            pass
    env = os.getenv("PALETTE_INDEX")
    if env is not None:
        try:
            return int(env)
        except ValueError:
            return None
    return None

# -------------------------
# Límite diario
# -------------------------
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

def _find_date_segment(path_str: str) -> str | None:
    for part in Path(path_str).parts:
        if DATE_RE.match(part):
            return part
    return None

def _count_outputs_in_day(output_root: Path) -> int:
    if not output_root.exists() or not output_root.is_dir():
        return 0
    return sum(1 for p in output_root.iterdir() if p.is_dir())

def exceeded_daily_limit(task: str, output_dir: str) -> tuple[bool, dict]:
    cfg = _maybe_load_yaml_config()
    info = {"max_items_per_day": None, "task_limit": None, "count_today": None, "date": None}

    date_seg = _find_date_segment(output_dir) or datetime.now().strftime("%Y-%m-%d")
    info["date"] = date_seg

    day_root = Path(output_dir)
    if day_root.name != date_seg:
        day_root = day_root.parent

    count_today = _count_outputs_in_day(day_root)
    info["count_today"] = count_today

    max_global = None
    if isinstance(cfg, dict) and isinstance(cfg.get("max_items_per_day"), int):
        max_global = int(cfg["max_items_per_day"])
        info["max_items_per_day"] = max_global

    task_limit = None
    if isinstance(cfg.get("per_task_limits"), dict):
        tl = cfg["per_task_limits"].get(task)
        if isinstance(tl, int):
            task_limit = int(tl)
            info["task_limit"] = task_limit

    if max_global is None and task_limit is None:
        return (False, info)

    exceeded = False
    if max_global is not None and count_today >= max_global:
        exceeded = True
    if task_limit is not None and count_today >= task_limit:
        exceeded = True

    return (exceeded, info)

# -------------------------
# Task: website
# -------------------------
from factories.factory_websites import generate_website

def task_website(output_dir: str, site_title: str, palette_index: int | None) -> dict:
    print(f"[orchestrator] task=website")
    print(f"[orchestrator] resolved output_dir={output_dir}")
    print(f"[orchestrator] site_title={site_title} palette_index={palette_index}")
    info = generate_website(output_dir=output_dir, site_title=site_title, palette_index=palette_index)
    print(f"feat(website): nueva mini-web {info['slug']} con paleta {info['palette_index']}, historia y datos ficticios reales")
    return info

# -------------------------
# Main CLI
# -------------------------
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Tektra Orchestrator — Websites overhaul")
    parser.add_argument("--task", choices=["website"], default="website")
    parser.add_argument("--output-dir", dest="output_dir")
    parser.add_argument("--site-title", dest="site_title")
    parser.add_argument("--palette-index", dest="palette_index")
    parser.add_argument("--force", action="store_true", help="Ignorar límites diarios")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    try:
        output_dir = resolve_output_dir(args.output_dir)
    except SystemExit as e:
        print(str(e), file=sys.stderr)
        return 2

    site_title = resolve_site_title(args.site_title)
    palette_index = resolve_palette_index(args.palette_index)

    if args.verbose:
        print(f"[orchestrator] argv={sys.argv}")
        print(f"[orchestrator] CWD={os.getcwd()}")
        print(f"[orchestrator] output_dir (raw)={output_dir}")

    if not args.force:
        exceeded, lim = exceeded_daily_limit(task=args.task, output_dir=output_dir)
        if args.verbose:
            print(f"[orchestrator] limit_check={lim}")
        if exceeded:
            print("[orchestrator] Límite diario alcanzado (agregá --force para ignorarlo).", file=sys.stderr)
            return 0
    else:
        print("[orchestrator] MODO FORZADO: ignorando límites diarios.")

    try:
        if args.task == "website":
            info = task_website(output_dir=output_dir, site_title=site_title, palette_index=palette_index)
            print(json.dumps({"ok": True, "output_dir": info["output_dir"], "slug": info["slug"]}, ensure_ascii=False))
            return 0
    except Exception as e:
        print("[orchestrator] ERROR durante la ejecución:", e, file=sys.stderr)
        traceback.print_exc()
        return 1

    print("[orchestrator] tarea no reconocida", file=sys.stderr)
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
