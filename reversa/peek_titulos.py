"""Identifica cada variante por sus textos fijos (título, etiquetas)."""
import json
import pathlib
import re

BASE = pathlib.Path(__file__).parent
D = BASE / "spec" / "reportes"

for p in sorted(D.glob("*_spec.json")):
    objs = json.loads(p.read_text(encoding="utf-8"))
    fijos = []
    for o in objs:
        e = o.get("expr") or ""
        m = re.match(r'^"([^"]{6,90})"$', e.strip())
        if m:
            fijos.append(m.group(1))
    print(f"\n== {p.stem.replace('_spec', '')} ==")
    for f in fijos[:14]:
        print("    ", f)
