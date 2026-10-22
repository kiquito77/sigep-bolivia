"""Muestra los controles de los formularios .scx del comprobante."""
import json
import pathlib

BASE = pathlib.Path(__file__).parent
forms = json.loads((BASE / "spec" / "formularios.json").read_text(encoding="utf-8"))

for name, data in forms.items():
    print(f"\n===== {name} ({data.get('registros')} registros) =====")
    for c in data.get("controles", []):
        partes = [f"{k}={v}" for k, v in c.items() if k not in ("n", "objtype", "objcode")]
        print("  ", " | ".join(partes)[:200])
