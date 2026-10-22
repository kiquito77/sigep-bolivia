"""Consultas rápidas sobre el resultado del escaneo."""
import json
import pathlib

P = pathlib.Path(__file__).parent / "spec"


def load(name):
    return json.loads((P / f"{name}.json").read_text(encoding="utf-8"))


t = load("tablas")
rows = [(k, v.get("registros", 0), len(v.get("campos", []))) for k, v in t.items() if "error" not in v]
rows.sort(key=lambda x: -x[1])
print("TOP 20 tablas por registros:")
for k, n, c in rows[:20]:
    print(f"  {k:30} {n:8} regs {c:3} campos")

print("\nTablas del comprobante:")
for k in sorted(t):
    low = k.lower()
    if any(s in low for s in ("cbte", "impri", "movga", "relga", "plan_c", "s3ctas", "unidad", "moneda", "codigo")):
        v = t[k]
        print(f"  {k:34} {v.get('registros'):6} regs {len(v.get('campos', [])):3} campos")
