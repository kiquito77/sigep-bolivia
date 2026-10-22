"""Busca la definición de FRUs (unidad de reporte de VFP) en las cadenas."""
import json
import pathlib
import re

BASE = pathlib.Path(__file__).parent
spec = json.loads((BASE / "spec" / "cadenas.json").read_text(encoding="utf-8"))

pat = re.compile(r"FRU|frxrecno|bandlabel|VFPFRXLayoutObject", re.I)
for mod, data in spec.items():
    hits = [s for s in data.get("sql", []) if "$FRUs" in s or "FRUs" in s]
    hits += [s for s in data.get("nombres", []) if "FRU" in s]
    if not hits:
        continue
    print(f"\n== {mod} ==")
    for s in dict.fromkeys(hits):
        if "FRUs" in s and ("variable" in s or "select" in s.lower()):
            print("  ", s[:300])
