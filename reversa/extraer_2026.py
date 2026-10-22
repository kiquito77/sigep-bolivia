"""Extrae el Clasificador Presupuestario 2026 desde el PDF oficial del MEFP.

Secciones del PDF (1-based):
  - Recursos por rubros: páginas 22-50
  - Objeto del gasto:    páginas 51-96

Genera clasificador_2026.json con {gastos, recursos}.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pymupdf

PDF = Path(r"E:\Programa ing inversa\Proyecto Sigep\Nueva carpeta\Clasificadores_Presupuestarios_2026_0.pdf")
DESTINO = Path(__file__).parent / "clasificador_2026.json"

CODIGO = re.compile(r"^\s*(\d{5})\s*(.*)$")
SOLO_NUM = re.compile(r"^\s*\d{1,3}\s*$")
RANGO_RECURSOS = (22, 50)
RANGO_GASTOS = (51, 96)


def limpiar(txt: str) -> str:
    return " ".join(txt.replace("\u00a0", " ").split())


def extraer(pdf, desde: int, hasta: int) -> dict[str, str]:
    items: dict[str, str] = {}
    pendiente = None
    for pagina in range(desde - 1, hasta):
        for linea in pdf[pagina].get_text().splitlines():
            if SOLO_NUM.match(linea):
                continue
            m = CODIGO.match(linea)
            if m:
                codigo, resto = m.group(1), limpiar(m.group(2))
                if resto:
                    items.setdefault(codigo, resto)
                    pendiente = None
                else:
                    pendiente = codigo
                continue
            if pendiente:
                texto = limpiar(linea)
                if texto and len(texto) > 2:
                    items[pendiente] = texto
                    pendiente = None
    return {k: v for k, v in items.items() if v}


def tipos(codigos: list[str]) -> dict[str, str]:
    """'N' = agrupación con hijos, 'S' = partida imputable (misma regla que el SIGEP)."""
    conjunto = set(codigos)
    res = {}
    for c in codigos:
        hijos = [
            o for o in conjunto
            if o != c and len(o) == 5 and (
                (c.endswith("0000") and o[:1] == c[:1]) or
                (c.endswith("000") and o[:2] == c[:2]) or
                (c.endswith("00") and o[:3] == c[:3])
            )
        ]
        res[c] = "N" if hijos else "S"
    return res


def main() -> None:
    pdf = pymupdf.open(PDF)
    recursos = extraer(pdf, *RANGO_RECURSOS)
    gastos = extraer(pdf, *RANGO_GASTOS)
    tr, tg = tipos(list(recursos)), tipos(list(gastos))
    salida = {
        "gestion": 2026,
        "fuente": PDF.name,
        "gastos": [{"GASTO": k, "DES": v, "TIPO": tg[k]} for k, v in sorted(gastos.items())],
        "recursos": [{"RECURSO": k, "DES": v, "TIPO": tr[k]} for k, v in sorted(recursos.items())],
    }
    DESTINO.write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"gastos: {len(salida['gastos'])} ({(sum(1 for g in salida['gastos'] if g['TIPO']=='S'))} imputables)")
    print(f"recursos: {len(salida['recursos'])} ({(sum(1 for r in salida['recursos'] if r['TIPO']=='S'))} imputables)")
    print("escrito:", DESTINO)


if __name__ == "__main__":
    main()
