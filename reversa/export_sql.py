"""Documenta el acceso a datos y los mensajes de negocio de los .APP.

Filtra el ruido del motor de reportes de VFP (ReportBuilder/ReportOutput) y se queda
con lo que referencia tablas del SIGEP (s3..s7, r_*) o con mensajes en español.
"""
from __future__ import annotations

import json
import pathlib
import re

BASE = pathlib.Path(__file__).parent
spec = json.loads((BASE / "spec" / "cadenas.json").read_text(encoding="utf-8"))

TABLA = re.compile(r"\b(s[3-7][a-z0-9_]{2,}|r_[a-z0-9_]{2,})\b", re.I)
ACCION = re.compile(r"^\s*(SELECT|INSERT|UPDATE|DELETE|USE|APPEND|REPLACE|SEEK|LOCATE|SCATTER|GATHER|SET\s+ORDER|INDEX\s+ON)\b", re.I)
RUIDO = ("xsl:", "&#", "$FRUs", "VFP-", "concat(", "loBandRef", "THIS.", "m.l", "FRX_", "ObjType")
ESPANOL = re.compile(r"[áéíóúñÁÉÍÓÚÑ¿¡]|\b(el|la|los|las|de|para|del|por|con|no|se|que|Comprobante|Cuenta|Partida|Gasto|Recurso|Usuario|Error|Impresi)\b", re.I)


def limpia(s: str) -> str:
    return " ".join(s.split())


def main() -> None:
    salida = ["# Acceso a datos y mensajes por módulo", "",
              "Recuperado de las cadenas de los `.APP` sin ejecutar el programa.", ""]

    for mod, data in sorted(spec.items()):
        sql, msgs = [], []
        for s in data.get("sql", []):
            s = limpia(s)
            if any(r in s for r in RUIDO) or not ACCION.search(s):
                continue
            if TABLA.search(s):
                sql.append(s)
        for s in data.get("nombres", []):
            pass
        # mensajes: vienen del bloque completo de cadenas, no solo de 'sql'
        for s in data.get("sql", []):
            s = limpia(s)
            if len(s) < 18 or len(s) > 200 or any(r in s for r in RUIDO):
                continue
            if ACCION.search(s) or "=" in s or "select" in s.lower():
                continue
            if ESPANOL.search(s) and " " in s:
                msgs.append(s)

        sql = list(dict.fromkeys(sql))
        msgs = list(dict.fromkeys(msgs))
        if not sql and not msgs:
            continue
        salida.append(f"## `{mod}`")
        salida.append("")
        if sql:
            salida.append(f"### Sentencias sobre tablas SIGEP ({len(sql)})")
            salida.append("")
            for s in sql[:25]:
                salida.append(f"- `{s[:220]}`")
            salida.append("")
        if msgs:
            salida.append(f"### Mensajes / textos de la aplicación ({len(msgs)})")
            salida.append("")
            for s in msgs[:25]:
                salida.append(f"- {s[:180]}")
            salida.append("")

    (BASE / "spec" / "SQL_POR_MODULO.md").write_text("\n".join(salida), encoding="utf-8")
    print("escrito spec/SQL_POR_MODULO.md")


if __name__ == "__main__":
    main()
