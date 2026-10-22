"""Exporta documentación y catálogos del SIGEP para el proyecto web.

Genera:
  spec/reportes/<nombre>_spec.md|json   los 7 reportes en pulgadas
  spec/TABLAS.md                        catálogo de las 188 tablas
  catalogos/<tabla>.json                catálogos listos para consumir
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from vfp import read_dbf  # noqa: E402

BASE = Path(__file__).parent
FORMATOS = BASE / "oficial" / "Formatos"
SPEC = BASE / "spec"
DATA = Path(r"C:\sgp2021\Data")
FRU = 10000.0

TIPO = {1: "REPORTE", 5: "TEXTO", 6: "RECT", 7: "LINEA", 8: "CAMPO", 9: "BANDA",
        17: "IMAGEN", 18: "VAR", 23: "?", 25: "ENTORNO"}

# Catálogos que el proyecto web necesita
CATALOGOS = ["s3plan_c", "s3codigo", "s3relga", "s3ctas", "s3unidad", "s3moneda",
             "s3gastos", "s3recur", "s3sector", "s3funcion", "r_entidad",
             "s3et", "s3of", "s3ff", "s3ff_of", "s3claega", "s3claere",
             "s6bancos", "s7benef", "s3usrid", "s3parametros"]


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


def exportar_reportes() -> None:
    dest = SPEC / "reportes"
    dest.mkdir(exist_ok=True)
    for frx in sorted(FORMATOS.glob("*.frx")):
        _, rows = read_dbf(frx)
        rows = first_block(rows)
        objs = []
        for r in rows:
            ot = r.get("OBJTYPE")
            objs.append({
                "recno": r["_recno"], "tipo": TIPO.get(ot, f"obj{ot}"),
                "x": inch(r.get("HPOS")), "y": inch(r.get("VPOS")),
                "ancho": inch(r.get("WIDTH")), "alto": inch(r.get("HEIGHT")),
                "fuente": (r.get("FONTFACE") or "").strip(), "tam": r.get("FONTSIZE"),
                "alineacion": r.get("MODE"), "expr": (r.get("EXPR") or "").strip(),
            })
        (dest / f"{frx.stem}_spec.json").write_text(json.dumps(objs, ensure_ascii=False, indent=1), encoding="utf-8")
        lineas = [f"# `{frx.name}`", "", f"Objetos: {len(objs)} · medidas en pulgadas (FRU/10000)", "",
                  "| # | tipo | x | y | ancho | alto | fuente | tam | expresión |", "|---|---|---|---|---|---|---|---|---|"]
        for o in objs:
            if o["tipo"] == "ENTORNO":
                continue
            e = o["expr"].replace("|", "\\|").replace("\n", " ")[:120]
            lineas.append(f"| {o['recno']} | {o['tipo']} | {o['x'] or ''} | {o['y'] or ''} | {o['ancho'] or ''} | "
                          f"{o['alto'] or ''} | {o['fuente']} | {o['tam'] or ''} | `{e}` |")
        (dest / f"{frx.stem}_spec.md").write_text("\n".join(lineas), encoding="utf-8")
        print("  reporte:", frx.name, f"{len(objs)} objetos")


def exportar_tablas() -> None:
    tablas = sorted(DATA.glob("*.dbf"))
    lineas = ["# Catálogo de tablas del SIGEP (Data\\)", "",
              f"Tablas: {len(tablas)}", "",
              "| Tabla | Registros | Campos |", "|---|---|---|"]
    detalle = []
    for dbf in tablas:
        try:
            campos, rows = read_dbf(dbf)
        except Exception as e:
            lineas.append(f"| {dbf.stem} | error | {e} |")
            continue
        lineas.append(f"| `{dbf.stem}` | {len(rows)} | {len(campos)} |")
        detalle.append((dbf.stem, len(rows), campos))
    (SPEC / "TABLAS.md").write_text("\n".join(lineas), encoding="utf-8")

    det = ["# Diccionario de campos", ""]
    for nombre, n, campos in detalle:
        det.append(f"## `{nombre}` ({n} registros)")
        det.append("")
        det.append("| Campo | Tipo | Largo | Dec |")
        det.append("|---|---|---|---|")
        for c in campos:
            det.append(f"| `{c['name']}` | {c['type']} | {c['length']} | {c['dec']} |")
        det.append("")
    (SPEC / "DICCIONARIO_TABLAS.md").write_text("\n".join(det), encoding="utf-8")
    print(f"  tablas: {len(tablas)} -> TABLAS.md + DICCIONARIO_TABLAS.md")


def exportar_catalogos() -> None:
    dest = BASE / "catalogos"
    dest.mkdir(exist_ok=True)
    for nombre in CATALOGOS:
        dbf = DATA / f"{nombre}.dbf"
        if not dbf.exists():
            continue
        _, rows = read_dbf(dbf)
        limpio = [{k: v for k, v in r.items() if not k.startswith("_")} for r in rows]
        (dest / f"{nombre}.json").write_text(json.dumps(limpio, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  catálogo: {nombre}.json ({len(limpio)} filas)")


if __name__ == "__main__":
    print("reportes:")
    exportar_reportes()
    print("tablas:")
    exportar_tablas()
    print("catálogos:")
    exportar_catalogos()
    print("listo")
