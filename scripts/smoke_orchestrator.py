import runpy, sys
print("[smoke] importando orchestrator.py…")
ns = runpy.run_path("orchestrator.py")
print("[smoke] OK, no hay SyntaxError en orchestrator.py")

from factories.factory_websites import tpl_styles
css = tpl_styles({"bg":"#000","fg":"#fff","acc1":"#f00","acc2":"#0f0"})
assert ".hero" in css
print("[smoke] factory_websites OK")
