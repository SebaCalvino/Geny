from flask import Flask, jsonify
import sqlite3, os

app = Flask(__name__)
DB = os.environ.get("STATUS_DB", "./log/status.db")

def q(sql, args=()):
    con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
    cur = con.cursor(); cur.execute(sql, args)
    rows = [dict(r) for r in cur.fetchall()]
    con.close(); return rows

@app.get("/novedades")
def novedades():
    rows = q("SELECT id, ts, kind, title, path, cost FROM items ORDER BY id DESC LIMIT 50")
    return jsonify(rows)

@app.get("/quehaces")
def quehaces():
    last = q("SELECT ts, kind, title FROM items ORDER BY id DESC LIMIT 1")
    return jsonify(last[0] if last else {"status":"inicializando"})
