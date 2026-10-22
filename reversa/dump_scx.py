"""Vuelca formularios VFP (.scx): clases, nombres, propiedades y métodos."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from vfp import parse_props, read_dbf  # noqa: E402

INTERESA = ("CAPTION", "CONTROLSOURCE", "NAME", "ROWSOURCE", "COLUMNCOUNT", "VISIBLE", "ENABLED")


def main() -> int:
    for arg in sys.argv[1:]:
        p = Path(arg)
        _, rows = read_dbf(p)
        print(f"\n######## {p.name} ({len(rows)} registros) ########")
        for r in rows:
            props = parse_props(r.get("PROPERTIES") or "")
            metodos = parse_props(r.get("METHODS") or "")
            clase = r.get("CLASS")
            if clase in ("dataenvironment", "form"):
                extra = props.get("CAPTION") or ""
                print(f"\n[{clase}] {r.get('OBJNAME')} {extra}")
                continue
            vals = {k: props[k] for k in INTERESA if k in props}
            met = [k for k in metodos if k.upper().endswith("METHOD") or k in ("CLICK", "INIT", "LOAD", "VALID", "WHEN")]
            print(f"  [{clase}] {r.get('OBJNAME')}: " + ", ".join(f"{k}={v}" for k, v in vals.items()) +
                  (f"  metodos={met}" if met else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
