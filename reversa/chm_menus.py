"""Extrae el árbol de menús del manual oficial del SINCON (CHM) a markdown."""
from __future__ import annotations

import html
import re
from pathlib import Path

BASE = Path(r"E:\Programa ing inversa\Proyecto Sigep\reversa\chm\Sincon2011")
HHC = BASE / "Manual_del_Usuario.hhc"
SALIDA = BASE.parent.parent / "MENUS_OFICIALES.md"

NAME = re.compile(r'name="Name"\s+value="([^"]*)"', re.I)
LOCAL = re.compile(r'name="Local"\s+value="([^"]*)"', re.I)


def main() -> None:
    lineas = HHC.read_text(encoding="cp1252", errors="replace").splitlines()
    nivel = 0
    dentro = False
    nombre = archivo = ""
    salida = ["# Estructura de menús del SINCON / SIGEP (manual oficial)", ""]
    total = 0

    for linea in lineas:
        s = linea.strip().lower()
        if s.startswith("<ul>"):
            nivel += 1
            continue
        if s.startswith("</ul>"):
            nivel = max(0, nivel - 1)
            continue
        if s.startswith("<li>"):
            dentro, nombre, archivo = True, "", ""
            continue
        m = NAME.search(linea)
        if dentro and m:
            nombre = html.unescape(m.group(1)).strip()
        m = LOCAL.search(linea)
        if dentro and m:
            archivo = m.group(1).strip()
        if s.startswith("</object>") and dentro:
            if nombre:
                sangria = "  " * max(0, nivel - 1)
                link = f"  `{archivo}`" if archivo else ""
                salida.append(f"{sangria}- **{nombre}**{link}")
                total += 1
            dentro = False

    SALIDA.write_text("\n".join(salida), encoding="utf-8")
    print("escrito:", SALIDA, "| entradas:", total)


if __name__ == "__main__":
    main()
