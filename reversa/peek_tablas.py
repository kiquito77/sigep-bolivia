"""Detalle de tablas clave y SQL del módulo de comprobantes."""
import json
import pathlib
import sys

BASE = pathlib.Path(__file__).parent
sys.path.insert(0, str(BASE))
from vfp import read_dbf  # noqa: E402

DATA = pathlib.Path(r"C:\sgp2021\Data")
spec = json.loads((BASE / "spec" / "tablas.json").read_text(encoding="utf-8"))

CLAVE = ["s3cbte.dbf", "s3movga.dbf", "s3relga.dbf", "s3ctas.dbf", "s3plan_c.dbf",
         "s3codigo.dbf", "s3unidad.dbf", "s3moneda.dbf", "s6cbte_bene.dbf"]

for nombre in CLAVE:
    info = spec.get(f"Data\\{nombre}")
    if not info or "error" in info:
        print(f"!! {nombre} no disponible")
        continue
    print(f"\n===== {nombre}  ({info['registros']} registros) =====")
    for c in info["campos"]:
        print(f"   {c['n']:12} {c['t']}{c['l']}.{c['d']}")
    try:
        _, rows = read_dbf(DATA / nombre)
    except Exception as e:
        print("   (no se pudo leer contenido:", e, ")")
        continue
    for r in rows[:3]:
        vals = {k: v for k, v in r.items() if not k.startswith("_") and v not in (None, "")}
        print("   >", vals)
