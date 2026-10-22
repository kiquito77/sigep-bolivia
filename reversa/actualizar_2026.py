"""Actualiza los catálogos del SIGEP (copia SIGEP-REPLICA) al clasificador 2026.

Escribe directamente sobre las tablas DBF del sistema FoxPro:
  - s3gastos.dbf : partidas de gasto
  - s3recur.dbf  : rubros de recurso

Reglas:
  * agrega las partidas nuevas del clasificador 2026,
  * actualiza las denominaciones que cambiaron,
  * marca como borradas las partidas que el clasificador 2026 eliminó.

Los índices .CDX quedan desactualizados a propósito: después hay que ejecutar
"Mantenimiento -> Utilitarios -> Reindexar la base de datos" dentro del SIGEP.

Uso:
    python actualizar_2026.py            # simulación (no escribe nada)
    python actualizar_2026.py --aplicar  # escribe los cambios
"""
from __future__ import annotations

import argparse
import json
import shutil
import struct
from datetime import date
from pathlib import Path

REPLICA = Path(r"E:\Programa ing inversa\SIGEP-REPLICA")
DATA = REPLICA / "Data"
CLASIF_JSON = Path(__file__).parent / "clasificador_2026.json"
BACKUP = REPLICA / "_backup_catalogos_2026"


# --------------------------------------------------------------------- DBF
def cargar(path: Path) -> dict:
    data = path.read_bytes()
    nrec = struct.unpack_from("<I", data, 4)[0]
    hlen = struct.unpack_from("<H", data, 8)[0]
    rlen = struct.unpack_from("<H", data, 10)[0]
    campos, off = [], 32
    while off + 32 <= hlen and data[off] != 0x0D:
        raw = data[off:off + 32]
        campos.append({
            "nombre": raw[:11].split(b"\x00")[0].decode("cp1252"),
            "tipo": chr(raw[11]),
            "largo": raw[16],
            "dec": raw[17],
            "off": struct.unpack_from("<I", raw, 12)[0],
        })
        off += 32
    cabecera = bytearray(data[:hlen])
    registros = [bytearray(data[hlen + i * rlen: hlen + (i + 1) * rlen]) for i in range(nrec)]
    return {"path": path, "cabecera": cabecera, "campos": campos, "registros": registros, "rlen": rlen}


def leer(tabla: dict, reg: bytearray, campo: str) -> str:
    f = next(c for c in tabla["campos"] if c["nombre"].upper() == campo.upper())
    raw = reg[f["off"]: f["off"] + f["largo"]]
    return raw.decode("cp1252", errors="replace").strip()


def escribir(tabla: dict, reg: bytearray, campo: str, valor: str) -> None:
    f = next(c for c in tabla["campos"] if c["nombre"].upper() == campo.upper())
    texto = str(valor)
    if f["tipo"] == "C":
        raw = texto.encode("cp1252", errors="replace")[:f["largo"]].ljust(f["largo"], b" ")
    elif f["tipo"] == "N":
        raw = texto.rjust(f["largo"])[:f["largo"]].encode("cp1252", errors="replace")
    else:
        raw = texto.encode("cp1252", errors="replace")[:f["largo"]].ljust(f["largo"], b" ")
    reg[f["off"]: f["off"] + f["largo"]] = raw


def nuevo_registro(tabla: dict) -> bytearray:
    reg = bytearray(b" " * tabla["rlen"])
    reg[0] = 0x20
    return reg


def guardar(tabla: dict) -> None:
    hoy = date.today()
    tabla["cabecera"][1] = (hoy.year - 1900) & 0xFF
    tabla["cabecera"][2] = hoy.month
    tabla["cabecera"][3] = hoy.day
    struct.pack_into("<I", tabla["cabecera"], 4, len(tabla["registros"]))
    salida = bytes(tabla["cabecera"]) + b"".join(bytes(r) for r in tabla["registros"])
    if not salida.endswith(b"\x1a"):
        salida += b"\x1a"
    tabla["path"].write_bytes(salida)


# --------------------------------------------------------------------- lógica
def aplicar(tabla: dict, clave: str, catalogo: list[dict], nombre_campo: str, aplicar_cambios: bool):
    existentes: dict[str, list[bytearray]] = {}
    for reg in tabla["registros"]:
        cod = leer(tabla, reg, clave)
        existentes.setdefault(cod, []).append(reg)

    agregados = actualizados = borrados = 0
    for item in catalogo:
        cod = str(item[clave]).strip()
        des = str(item["DES"]).strip()
        tipo = str(item.get("TIPO", "S")).strip()
        if cod in existentes:
            reg = existentes[cod][0]
            if leer(tabla, reg, "DES") != des:
                actualizados += 1
                if aplicar_cambios:
                    escribir(tabla, reg, "DES", des)
            if "TIPO" in [c["nombre"].upper() for c in tabla["campos"]]:
                if leer(tabla, reg, "TIPO") != tipo:
                    if aplicar_cambios:
                        escribir(tabla, reg, "TIPO", tipo)
        else:
            agregados += 1
            if aplicar_cambios:
                reg = nuevo_registro(tabla)
                escribir(tabla, reg, clave, cod)
                escribir(tabla, reg, "DES", des)
                if "TIPO" in [c["nombre"].upper() for c in tabla["campos"]]:
                    escribir(tabla, reg, "TIPO", tipo)
                escribir(tabla, reg, "PR", "") if "PR" in [c["nombre"].upper() for c in tabla["campos"]] else None
                tabla["registros"].append(reg)
                existentes[cod] = [reg]

    vigentes = {str(i[clave]).strip() for i in catalogo}
    for cod, regs in existentes.items():
        if cod and cod not in vigentes:
            for reg in regs:
                if reg[0] != 0x2A:
                    borrados += 1
                    if aplicar_cambios:
                        reg[0] = 0x2A
    return agregados, actualizados, borrados


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    args = ap.parse_args()

    if not CLASIF_JSON.exists():
        raise SystemExit(f"falta el clasificador 2026: {CLASIF_JSON}")
    clasif = json.loads(CLASIF_JSON.read_text(encoding="utf-8"))

    if args.aplicar and not BACKUP.exists():
        BACKUP.mkdir()
        for f in ("s3gastos.dbf", "s3recur.dbf", "S3GASTOS.CDX", "S3RECUR.CDX"):
            p = DATA / f
            if p.exists():
                shutil.copy2(p, BACKUP / f)
        print("respaldo en:", BACKUP)

    for tabla_nombre, clave, catalogo in (
        ("s3gastos.dbf", "GASTO", clasif["gastos"]),
        ("s3recur.dbf", "RECURSO", clasif["recursos"]),
    ):
        t = cargar(DATA / tabla_nombre)
        antes = len(t["registros"])
        ag, ac, bo = aplicar(t, clave, catalogo, "DES", args.aplicar)
        print(f"{tabla_nombre}: {antes} registros | +{ag} nuevos, ~{ac} actualizados, -{bo} marcados borrados")
        if args.aplicar:
            guardar(t)
            print(f"  escrito: {len(t['registros'])} registros")

    if not args.aplicar:
        print("\nSIMULACIÓN: no se escribió nada. Usar --aplicar para guardar.")
    else:
        print("\nListo. Abrí el SIGEP y ejecutá: Mantenimiento -> Utilitarios -> Reindexar la base de datos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
