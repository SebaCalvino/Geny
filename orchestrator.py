#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from pathlib import Path
import sys, importlib, importlib.util, logging, json, datetime as dt, traceback

ROOT = Path(__file__).parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("tektra")

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
            prev = json.loads(log_path.read_text(encoding="utf-8"))
            if isinstance(prev, list):
                prev.append(result)
                log_path.write_text(json.dumps(prev, ensure_ascii=False, indent=2), encoding="utf-8")
            else:
                log_path.write_text(json.dumps([prev, result], ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            log_path.write_text(json.dumps([result], ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        log.warning("No se pudo escribir run_log.json: %s", e)

def _import_attr_by_module_name(mod_name: str, func_name: str):
    try:
        mod = importlib.import_module(mod_name)
        return getattr(mod, func_name)
    except Exception as e:
        log.error("Import fallo: %s.%s -> %s", mod_name, func_name, e)
        return None

def _import_attr_by_path(py_file: Path, func_name: str):
    try:
        spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)  # type: ignore[attr-defined]
            return getattr(mod, func_name, None)
    except Exception as e:
        log.error("Import por ruta fallo: %s (%s)", py_file, e)
    return None

def _find_first(patterns: list[str]) -> Path | None:
    for pat in patterns:
        found = list(ROOT.glob(pat))
        if found:
            return found[0]
    return None

def load_factory(func_name: str, canonical_module: str, patterns: list[str]):
    # 1) intentar canonical
    fn = _import_attr_by_module_name(canonical_module, func_name)
    if fn:
        log.info("Factory %s desde módulo: %s", func_name, canonical_module)
        return fn

    # 2) intentar por ruta
    target = _find_first(patterns)
    if target:
        fn = _import_attr_by_path(target, func_name)
        if fn:
            log.info("Factory %s desde ruta: %s", func_name, target)
            return fn
        else:
            log.error("Archivo encontrado pero sin función %s: %s", func_name, target)

    # 3) SIN fallback: fallar
    msg = (f"No se encontró la factory requerida '{func_name}'. "
           f"Esperaba módulo '{canonical_module}' o alguno de: {patterns}")
    log.critical(msg)
    raise RuntimeError(msg)

# cargar factories reales (SIN fallback)
generate_site  = load_factory("generate_site",  "factories.web_factory",   ["**/factories/web_factory.py",   "**/*web*factory.py"])
generate_image = load_factory("generate_image", "factories.image_factory", ["**/factories/image_factory.py", "**/*image*factory.py", "**/*img*factory.py"])
generate_game  = load_factory("generate_game",  "factories.game_factory",  ["**/factories/game_factory.py",  "**/*game*factory.py"])

def main() -> None:
    summary = {"started_at": dt.datetime.utcnow().isoformat()+"Z", "items": [], "errors": []}

    def _safe(name, fn):
        item = {"type": name, "status": "ok"}
        try:
            result = fn()
            item["result"] = result if result is not None else "ok"
            log.info("Factory %s completada.", name)
        except Exception as e:
            item["status"] = "error"
            item["error"] = str(e)
            summary["errors"].append({"factory": name, "error": str(e), "traceback": traceback.format_exc()})
            log.error("Factory %s falló: %s", name, e)
        finally:
            summary["items"].append(item)

    _safe("website", generate_site)
    _safe("image",   generate_image)
    _safe("game",    generate_game)

    summary["finished_at"] = dt.datetime.utcnow().isoformat()+"Z"
    write_run_log(summary)

    if all(i["status"] == "error" for i in summary["items"]):
        log.error("Todas las factories fallaron.")
        sys.exit(2)
    log.info("Ciclo Tektra completado.")

if __name__ == "__main__":
    main()
