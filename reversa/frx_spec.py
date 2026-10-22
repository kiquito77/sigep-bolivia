"""Genera la especificación legible de un reporte VFP (.frx) en pulgadas.

Salida: <nombre>_spec.md y <nombre>_spec.json junto al .frx.
FRU = 1/10000 pulgada (constante $FRUs de VFP 9).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from vfp import read_dbf  # noqa: E402

FRU = 10000.0


def inch(v):
    return None if v is None else round(float(v) / FRU, 3)


def first_block(rows):
    out, visto = [], 0
    for r in rows:
        if r.get("OBJTYPE") == 1:
            visto += 1
            if visto > 1:
                break
        out.append(r)
    return out


TIPO = {1: "REPORTE", 5: "TEXTO", 6: "RECTANGULO", 7: "LINEA/RECT", 8: "CAMPO", 9: "BANDA",
        17: "IMAGEN", 18: "VARIABLE", 23: "?", 25: "ENTORNO"}


def main() -> int:
    src = Path(sys.argv[1])
    _, rows = read_dbf(src)
    rows = first_block(rows)

    objs = []
    for r in rows:
        ot = r.get("OBJTYPE")
        expr = (r.get("EXPR") or "").strip()
        objs.append({
            "recno": r["_recno"],
            "tipo": TIPO.get(ot, f"obj{ot}"),
            "objtype": ot,
            "objcode": r.get("OBJCODE"),
            "v_in": inch(r.get("VPOS")),
            "h_in": inch(r.get("HPOS")),
            "w_in": inch(r.get("WIDTH")),
            "alto_in": inch(r.get("HEIGHT")),
            "fuente": (r.get("FONTFACE") or "").strip(),
            "tam": r.get("FONTSIZE"),
            "estilo": r.get("FONTSTYLE"),
            "alineacion": r.get("MODE"),
            "expr": expr,
        })

    base = src.with_name(src.stem + "_spec")
    base.with_suffix(".json").write_text(json.dumps(objs, ensure_ascii=False, indent=1), encoding="utf-8")

    lines = [f"# Reporte `{src.name}`", "",
             f"Objetos: {len(objs)}  ·  Unidad: FRU (1/10000 in) convertida a pulgadas", "",
             "| # | tipo | x in | y in | ancho in | alto in | fuente | tam | expresión |",
             "|---|------|------|------|----------|---------|--------|-----|-----------|"]
    for o in objs:
        if o["tipo"] == "ENTORNO":
            continue
        expr = o["expr"].replace("|", "\\|").replace("\n", " ")[:110]
        lines.append(
            f"| {o['recno']} | {o['tipo']} | {o['h_in'] or ''} | {o['v_in'] or ''} | {o['w_in'] or ''} | "
            f"{o['alto_in'] or ''} | {o['fuente']} | {o['tam'] or ''} | `{expr}` |"
        )
    base.with_suffix(".md").write_text("\n".join(lines), encoding="utf-8")
    print("escrito:", base.with_suffix(".md"))
    print("escrito:", base.with_suffix(".json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
