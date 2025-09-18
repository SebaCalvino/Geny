#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tektra Orchestrator
- Corre 3 ítems por ciclo: 1 web, 1 imagen, 1 juego.
- Import robusto de factories tanto en local como en GitHub Actions.
- Logs claros y exit code != 0 si faltan factories críticas.
"""

from __future__ import annotations
from pathlib import Path
import sys
import importlib
import logging
import json
import datetime as dt
import traceback

# ---------------------------
# Bootstrap de rutas (CI safe)
# ---------------------------
ROOT = Path(__file__).parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
FACTORIES = ROOT / "factories"
if FACTORIES.exists() and str(FACTORIES) not in sys.path:
    sys.path.insert(0, str(FACTORIES))

# ---------------------------
# Logging
# ---------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("tektra")

def _import_factory(mod_name: str, func_name: str):
    """Carga segura de una factory y devuelve la función pedida o None."""
    try:
        mod = importlib.import_module(mod_name)
    except Exception as e:
        log.error("ERROR importando %s: %s", mod_name, e)
        return None
    try:
        fn = getattr(mod, func_name)
        return fn
    except AttributeError:
        log.error("El módulo %s no expone la función %s", mod_name, func_name)
        return None

# ---------------------------
# Imports de factories (API)
# ---------------------------
generate_site  = _import_factory("factories.web_factory",   "generate_site")
generate_image = _import_factory("factories.image_factory", "generate_image")
generate_game  = _import_factory("factories.game_factory",  "generate_game")

if not all([generate_site, generate_image, generate_game]):
    log.error("No se pudieron cargar factories. Abort.")
    sys.exit(1)

# ---------------------------
# Utilidades de salida
# ---------------------------
def today_folder() -> Path:
    d = dt.datetime.now().strftime("%Y-%m-%d")
    out = ROOT / "output" / d
    out.mkdir(parents=True, exist_ok=True)
    return out

def write_run_log(result: dict) -> None:
    out_dir = today_folder()
    log_path = out_dir / "run_log.json"
    try:
        if log_path.exists():
            previous = json.loads(log_path.read_text(encoding="utf-8"))
            if isinstance(previous, list):
                previous.append(result)
                log_path.write_text(json.dumps(previous, ensure_ascii=False, indent=2), encoding="utf-8")
            else:
                log_path.write_text(json.dumps([previous, result], ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            log_path.write_text(json.dumps([result], ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        log.warning("No se pudo escribir run_log.json: %s", e)

# ---------------------------
# Ejecución de un ciclo
# ---------------------------
def main() -> None:
    summary = {
        "started_at": dt.datetime.utcnow().isoformat() + "Z",
        "items": [],
        "errors": [],
    }

    def _safe_run(name: str, fn):
        item = {"type": name, "status": "ok"}
        try:
            # Cada factory debería encargarse de crear su carpeta/archivo
            # y devolver algún descriptor o ruta si es posible.
            result = fn()
            item["result"] = result if result is not None else "ok"
            log.info("Factory %s completada.", name)
        except Exception as e:
            item["status"] = "error"
            item["error"] = str(e)
            summary["errors"].append({
                "factory": name,
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            log.error("Factory %s falló: %s", name, e)
        finally:
            summary["items"].append(item)

    # 3 ítems por ciclo
    _safe_run("website", generate_site)
    _safe_run("image",   generate_image)
    _safe_run("game",    generate_game)

    summary["finished_at"] = dt.datetime.utcnow().isoformat() + "Z"
    write_run_log(summary)

    # Si todas fallaron, devolvemos error para que se note en CI.
    if all(i["status"] == "error" for i in summary["items"]):
        log.error("Todas las factories fallaron.")
        sys.exit(2)
    log.info("Ciclo Tektra completado.")

if __name__ == "__main__":
    main()
