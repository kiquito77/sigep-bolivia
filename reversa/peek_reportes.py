"""Resumen geométrico de las 7 variantes del comprobante."""
import json
import pathlib

BASE = pathlib.Path(__file__).parent
D = BASE / "spec" / "reportes"

for p in sorted(D.glob("*_spec.json")):
    objs = json.loads(p.read_text(encoding="utf-8"))
    anchos = [o["x"] + o["ancho"] for o in objs if o.get("x") is not None and o.get("ancho")]
    altos = [o["y"] + o["alto"] for o in objs if o.get("y") is not None and o.get("alto")]
    bandas = [(o["recno"], o["alto"]) for o in objs if o["tipo"] == "BANDA"]
    fuentes = sorted({f"{o['fuente']} {o['tam']}" for o in objs if o.get("fuente")})
    print(f"\n== {p.stem.replace('_spec', '')} ==")
    print(f"   objetos={len(objs)}  ancho util={max(anchos):.3f}in  alto util={max(altos):.3f}in")
    print(f"   bandas (alto in): {[b[1] for b in bandas]}")
    print(f"   fuentes: {', '.join(fuentes)[:160]}")
