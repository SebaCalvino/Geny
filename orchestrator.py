from __future__ import annotations
import json, random
from datetime import datetime
from pathlib import Path

TODAY = datetime.now().strftime("%Y-%m-%d")
ROOT = Path(__file__).parent
OUT = ROOT / "output" / TODAY
OUT.mkdir(parents=True, exist_ok=True)

def write_changelog(item):
    log = ROOT / "output" / "changelog.json"
    data = []
    if log.exists():
        try:
            data = json.loads(log.read_text(encoding="utf-8"))
        except Exception:
            data = []
    data.insert(0, item)
    log.write_text(json.dumps(data[:200], ensure_ascii=False, indent=2), encoding="utf-8")

def update_index():
    idx = ROOT / "output" / "index.md"
    lines = ["# Maker Bot — Outputs\n"]
    for day in sorted((ROOT / "output").glob("*"), reverse=True):
        if not day.is_dir() or day.name == "assets":
            continue
        lines.append(f"## {day.name}")
        for p in sorted(day.iterdir()):
            rel = p.relative_to(ROOT)
            lines.append(f"- {p.name} → `{rel.as_posix()}`")
        lines.append("")
    idx.write_text("\n".join(lines), encoding="utf-8")

def create_min_artifact():
    txt = OUT / f"note_{datetime.now().strftime('%H%M%S')}.md"
    txt.write_text(
        f"# Auto note\n\nFecha: {datetime.now().isoformat()}\n\nIdea: {random.choice(['épicas imágenes','mini-web','juego simple'])}\n",
        encoding="utf-8",
    )
    write_changelog({
        "type": "note",
        "title": txt.name,
        "path": str(txt.relative_to(ROOT)),
        "ts": datetime.now().isoformat()
    })

if __name__ == "__main__":
    create_min_artifact()
    update_index()
    print("OK - output en", OUT)
