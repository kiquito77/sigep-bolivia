"""Detalle: códigos de transacción, unidad, comprobantes reales y SQL del módulo."""
import json
import pathlib
import re
import sys

BASE = pathlib.Path(__file__).parent
sys.path.insert(0, str(BASE))
from vfp import read_dbf  # noqa: E402

DATA = pathlib.Path(r"C:\sgp2021\Data")

print("===== s3codigo (momentos) =====")
_, rows = read_dbf(DATA / "s3codigo.dbf")
for r in rows:
    print(f"  {r['CODTR']:3} {r['DES']:32} tipo={r['T_COD']:4} bits={r['BITS']}")

print("\n===== s3unidad =====")
_, rows = read_dbf(DATA / "s3unidad.dbf")
for r in rows:
    print({k: v for k, v in r.items() if not k.startswith("_") and v not in (None, "")})

print("\n===== s3cbte (13 comprobantes) =====")
_, rows = read_dbf(DATA / "s3cbte.dbf")
for r in rows:
    print(f"  {r['CBTE']} {r['FECHA']} codtr={r['CODTR']:>2} estado={r['ESTADO']} borr={r['BORRADOR']} "
          f"tdbb={r['TDBB']:>14} thbb={r['THBB']:>14} ufv={r['UFV']} | {r['BENE'][:40]}")

print("\n===== s3movga: lineas del comprobante 1 =====")
_, rows = read_dbf(DATA / "s3movga.dbf")
for r in rows:
    if r["CBTE"] == "0000001":
        print(f"  L{r['LINEA']:>3} AP={r['AP']} G={r['GASTO']} FF={r['FF']} OF={r['OF']} ET={r['ET']} "
              f"OEC={r['OEC']} D={r['DBB']} H={r['HBB']}")

print("\n===== SQL / sentencias en pr_cbte.APP =====")
spec = json.loads((BASE / "spec" / "cadenas.json").read_text(encoding="utf-8"))
data = spec.get("pr_cbte.APP", {})
sql = data.get("sql", [])
print(f"total con SQL: {len(sql)}")
vistos = set()
for s in sql:
    key = s.upper()[:60]
    if key in vistos:
        continue
    vistos.add(key)
    print("  ", s[:220])

print("\n===== tablas .dbf referenciadas por pr_cbte.APP =====")
for k, v in sorted(data.get("tablas_dbf", {}).items(), key=lambda kv: -kv[1])[:30]:
    print(f"  {k}.dbf  x{v}")

print("\n===== tipos de archivo fuente presentes =====")
from collections import Counter
c = Counter(p.suffix.lower() for p in pathlib.Path(r"C:\sgp2021").rglob("*") if p.is_file())
for ext, n in c.most_common(25):
    print(f"  {ext or '(sin ext)':12} {n}")
