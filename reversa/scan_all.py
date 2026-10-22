"""Escaneo del SIGEP oficial (C:\\sgp2021) para ingeniería inversa.

Extrae, solo en lectura:
  - esquema y conteo de todas las tablas .dbf
  - inventario de reportes .frx (objetos, expresiones, posiciones)
  - inventario de formularios .scx
  - cadenas de texto de los binarios .app/.exe/.fll (SQL, tablas, mensajes)

Salida: spec/*.json + spec/RESUMEN.md
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from vfp import parse_props, read_dbf  # noqa: E402

ROOT = Path(r"C:\sgp2021")
BASE = Path(__file__).parent
OUT = BASE / "spec"
OUT.mkdir(exist_ok=True)

STR_RE = re.compile(rb"[\x20-\x7e\xa0-\xff]{5,}")
SQL_RE = re.compile(r"\b(select|insert|update|delete|create table|append from|index on|seek|locate|scan)\b", re.I)
TABLA_RE = re.compile(r"\b([a-z_][a-z0-9_]{2,8})\.dbf\b", re.I)


def dec(b: bytes) -> str:
    return b.decode("cp1252", errors="replace")


# ---------------------------------------------------------------- tablas
def scan_tables() -> dict:
    res: dict = {}
    for dbf in sorted(ROOT.rglob("*.dbf")):
        try:
            fields, rows = read_dbf(dbf)
        except Exception as e:  # tabla corrupta o bloqueada
            res[str(dbf.relative_to(ROOT))] = {"error": str(e)}
            continue
        res[str(dbf.relative_to(ROOT))] = {
            "registros": len(rows),
            "campos": [{"n": f["name"], "t": f["type"], "l": f["length"], "d": f["dec"]} for f in fields],
        }
    return res


# ---------------------------------------------------------------- reportes
def scan_reports() -> dict:
    res: dict = {}
    for frx in sorted(ROOT.rglob("*.frx")):
        try:
            fields, rows = read_dbf(frx)
        except Exception as e:
            res[str(frx.relative_to(ROOT))] = {"error": str(e)}
            continue
        objs = []
        for r in rows:
            expr = (r.get("EXPR") or "").strip()
            name = (r.get("NAME") or "").strip()
            ot = r.get("OBJTYPE")
            oc = r.get("OBJCODE")
            entry = {
                "n": r["_recno"],
                "objtype": ot,
                "objcode": oc,
                "v": r.get("VPOS"),
                "h": r.get("HPOS"),
                "w": r.get("WIDTH"),
                "ht": r.get("HEIGHT"),
                "font": r.get("FONTFACE"),
                "size": r.get("FONTSIZE"),
                "style": r.get("FONTSTYLE"),
                "mode": r.get("MODE"),
                "expr": expr[:400],
            }
            if name and (ot == 25 or "DataSource" in name):
                entry["name"] = name[:1200]
            if ot == 1:
                entry["props"] = expr[:400]
            objs.append(entry)
        res[str(frx.relative_to(ROOT))] = {"registros": len(rows), "objetos": objs}
    return res


# ---------------------------------------------------------------- formularios
def scan_forms() -> dict:
    res: dict = {}
    for scx in sorted(ROOT.rglob("*.scx")):
        try:
            fields, rows = read_dbf(scx)
        except Exception as e:
            res[str(scx.relative_to(ROOT))] = {"error": str(e)}
            continue
        ctrls = []
        for r in rows:
            props = parse_props(r.get("NAME") or "")
            if not props:
                props = parse_props(r.get("EXPR") or "")
            entry = {
                "n": r["_recno"],
                "objtype": r.get("OBJTYPE"),
                "objcode": r.get("OBJCODE"),
                "class": r.get("CLASS") if "CLASS" in r else None,
                "caption": props.get("CAPTION"),
                "name": props.get("NAME"),
                "controlsource": props.get("CONTROLSOURCE"),
                "left": props.get("LEFT"),
                "top": props.get("TOP"),
                "width": props.get("WIDTH"),
                "height": props.get("HEIGHT"),
            }
            entry = {k: v for k, v in entry.items() if v not in (None, "")}
            if entry:
                ctrls.append(entry)
        res[str(scx.relative_to(ROOT))] = {"registros": len(rows), "controles": ctrls}
    return res


# ---------------------------------------------------------------- cadenas
def scan_strings() -> dict:
    res: dict = {}
    for p in sorted(list(ROOT.rglob("*.app")) + list(ROOT.rglob("*.exe")) + list(ROOT.rglob("*.fll"))):
        try:
            data = p.read_bytes()
        except Exception as e:
            res[p.name] = {"error": str(e)}
            continue
        if len(data) > 80 * 1024 * 1024:
            res[p.name] = {"omitido": "demasiado grande"}
            continue
        found = {dec(m) for m in STR_RE.findall(data)}
        found = {s for s in found if len(s) >= 5 and not s.startswith(("http://schemas", "Microsoft."))}
        sql = sorted(s for s in found if SQL_RE.search(s) and len(s) < 400)
        tablas = Counter(t.lower() for s in found for t in TABLA_RE.findall(s))
        simples = [s for s in found if len(s) <= 11 and re.fullmatch(r"[a-z_][a-z0-9_]{2,10}", s)]
        res[p.name] = {
            "bytes": len(data),
            "cadenas": len(found),
            "sql": sql[:1500],
            "tablas_dbf": dict(tablas.most_common(200)),
            "nombres": sorted(set(simples))[:3000],
        }
    return res


def resumen(tablas, reportes, formularios, cadenas) -> str:
    lines = ["# Resumen del escaneo de C:\\sgp2021", ""]
    lines.append(f"## Tablas: {len(tablas)}")
    vacias = [k for k, v in tablas.items() if v.get("registros") == 0]
    lines.append(f"- con datos: {len(tablas) - len(vacias)}; vacías: {len(vacias)}")
    lines.append("")
    lines.append(f"## Reportes: {len(reportes)}")
    for k, v in reportes.items():
        lines.append(f"- {k}: {v.get('registros', '?')} objetos")
    lines.append("")
    lines.append(f"## Formularios: {len(formularios)}")
    for k, v in formularios.items():
        lines.append(f"- {k}: {len(v.get('controles', []))} controles")
    lines.append("")
    lines.append(f"## Binarios: {len(cadenas)}")
    for k, v in cadenas.items():
        lines.append(f"- {k}: {v.get('cadenas', 0)} cadenas, {len(v.get('sql', []))} con SQL")
    return "\n".join(lines)


def main() -> int:
    print("escaneando tablas...", flush=True)
    tablas = scan_tables()
    print(f"  {len(tablas)} tablas", flush=True)
    print("escaneando reportes...", flush=True)
    reportes = scan_reports()
    print(f"  {len(reportes)} reportes", flush=True)
    print("escaneando formularios...", flush=True)
    formularios = scan_forms()
    print(f"  {len(formularios)} formularios", flush=True)
    print("extrayendo cadenas...", flush=True)
    cadenas = scan_strings()
    print(f"  {len(cadenas)} binarios", flush=True)

    for name, obj in (("tablas", tablas), ("reportes", reportes), ("formularios", formularios), ("cadenas", cadenas)):
        (OUT / f"{name}.json").write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "RESUMEN.md").write_text(resumen(tablas, reportes, formularios, cadenas), encoding="utf-8")
    print("listo ->", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
