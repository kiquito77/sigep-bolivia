"""SQL y nombres de tablas detectados en los módulos .APP."""
import json
import pathlib

BASE = pathlib.Path(__file__).parent
spec = json.loads((BASE / "spec" / "cadenas.json").read_text(encoding="utf-8"))

for mod in ("pr_cbte.APP", "jconta.APP"):
    data = spec.get(mod, {})
    print(f"\n######## {mod}: {data.get('cadenas', 0)} cadenas ########")
    sql = data.get("sql", [])
    vistos = set()
    for s in sql:
        key = " ".join(s.upper().split())[:70]
        if key in vistos:
            continue
        vistos.add(key)
        if len(key) > 8:
            print("  ", s[:240])
    print(f"\n-- tablas .dbf referenciadas ({mod}) --")
    for k, v in sorted(data.get("tablas_dbf", {}).items(), key=lambda kv: -kv[1])[:40]:
        print(f"   {k}.dbf x{v}")
