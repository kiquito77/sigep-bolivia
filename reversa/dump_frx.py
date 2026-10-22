"""Vuelca el layout de un reporte VFP (.frx) de forma legible.

OBJTYPE: 1=encabezado del reporte, 8=objeto (texto/campo/línea/rect),
9=banda, 10=? , 5=?
Posiciones en twips (1440 twips = 1 pulgada).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from vfp import parse_props, read_dbf  # noqa: E402

TW = 1440.0


def inches(v):
    if v is None:
        return ""
    return f"{float(v) / TW:.3f}"


def one_line(s: str, n: int = 100) -> str:
    return " ".join((s or "").split())[:n]


def main() -> int:
    path = sys.argv[1]
    fields, rows = read_dbf(path)
    print(f"== {Path(path).name}: {len(rows)} registros ==")
    band = None
    for row in rows:
        ot = row.get("OBJTYPE")
        oc = row.get("OBJCODE")
        expr = row.get("EXPR") or ""
        props = parse_props(expr) if expr else {}
        vpos, hpos = row.get("VPOS"), row.get("HPOS")
        w, h = row.get("WIDTH"), row.get("HEIGHT")
        font = f"{row.get('FONTFACE') or ''} {row.get('FONTSIZE') or ''}"
        if ot == 1:
            print(f"\n# REPORTE  ancho={inches(w)}in  alto={inches(h)}in  reso={row.get('RESOID')}")
            if props:
                print("   props:", one_line(expr, 300))
        elif ot == 9:
            band = f"banda[{oc}] v={inches(vpos)} h={inches(h)}"
            print(f"\n=== BANDA objcode={oc} v={inches(vpos)}in alto={inches(h)}in ===")
            if expr:
                print("    expr:", one_line(expr, 200))
        elif ot == 8:
            kind = []
            if row.get("TAG"): kind.append("campo")
            print(
                f"  [{row['_recno']:3}] code={oc} v={inches(vpos):>7} h={inches(hpos):>7} "
                f"w={inches(w):>6} h={inches(h):>6} {font:<22} "
                f"{' '.join(kind):<6} {one_line(expr, 90)!r}"
            )
        else:
            print(f"  [{row['_recno']:3}] OBJTYPE={ot} code={oc} v={inches(vpos)} h={inches(hpos)} {one_line(expr, 80)!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
