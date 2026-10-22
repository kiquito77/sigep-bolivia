"""Editor de catálogos del SIGEP (tablas DBF de la copia SIGEP-REPLICA).

Permite listar, agregar, borrar y reactivar cuentas contables, partidas de gasto
y rubros de recurso, escribiendo directamente sobre las tablas FoxPro.

  python catalogo_tool.py listar cuentas --buscar banco
  python catalogo_tool.py agregar cuentas 11350 "Bancos - Cuenta Fiscal"
  python catalogo_tool.py borrar partidas 39990
  python catalogo_tool.py reactivar partidas 39990

Opcional: --datos "ruta\\a\\Data" para trabajar sobre otra copia de las tablas.

IMPORTANTE: después de cualquier cambio hay que abrir el SIGEP y ejecutar
"Mantenimiento -> Utilitarios -> Reindexar la base de datos" para que los
índices .CDX reconozcan los cambios.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from actualizar_2026 import cargar, escribir, guardar, leer, nuevo_registro  # noqa: E402

REPLICA_DATA = Path(r"E:\Programa ing inversa\SIGEP-REPLICA\Data")

TABLAS = {
    "cuentas": {"archivo": "s3plan_c.dbf", "clave": "CTA", "etiqueta": "plan de cuentas"},
    "partidas": {"archivo": "s3gastos.dbf", "clave": "GASTO", "etiqueta": "partidas de gasto"},
    "recursos": {"archivo": "s3recur.dbf", "clave": "RECURSO", "etiqueta": "rubros de recurso"},
}


def nivel_de(codigo: str) -> int:
    return 5 - (len(codigo) - len(codigo.rstrip("0")))


def tipo_de(codigo: str) -> str:
    return "N" if codigo.endswith("000") else "S"


def abrir(nombre: str, datos: Path) -> tuple[dict, dict]:
    if nombre not in TABLAS:
        raise SystemExit(f"tabla desconocida: {nombre}. Usar: {', '.join(TABLAS)}")
    meta = TABLAS[nombre]
    return cargar(datos / meta["archivo"]), meta


def buscar_reg(tabla: dict, clave: str, codigo: str):
    for r in tabla["registros"]:
        if leer(tabla, r, clave) == codigo:
            return r
    return None


def respaldar(tabla: dict) -> None:
    p = Path(tabla["path"])
    shutil.copy2(p, p.with_suffix(p.suffix + ".bak"))


def cmd_listar(args) -> None:
    tabla, meta = abrir(args.tabla, args.datos)
    clave = meta["clave"]
    q = (args.buscar or "").lower()
    n = 0
    for r in tabla["registros"]:
        borrado = r[0] == 0x2A
        if borrado and not args.incluir_borrados:
            continue
        cod, des = leer(tabla, r, clave), leer(tabla, r, "DES")
        if q and q not in cod.lower() and q not in des.lower():
            continue
        print(f"{cod:>7}  {des[:70]}{'   [BORRADO]' if borrado else ''}")
        n += 1
    print(f"\n{n} filas de {meta['etiqueta']}")


def cmd_agregar(args) -> None:
    tabla, meta = abrir(args.tabla, args.datos)
    clave, cod = meta["clave"], args.codigo.strip()
    if buscar_reg(tabla, clave, cod):
        raise SystemExit(f"el código {cod} ya existe (usar reactivar si está borrado)")
    campos = [c["nombre"].upper() for c in tabla["campos"]]
    reg = nuevo_registro(tabla)
    escribir(tabla, reg, clave, cod)
    escribir(tabla, reg, "DES", args.descripcion)
    if "TIPO" in campos:
        escribir(tabla, reg, "TIPO", args.tipo or tipo_de(cod))
    if "NIVEL" in campos:
        escribir(tabla, reg, "NIVEL", str(args.nivel or nivel_de(cod)))
    if "AUX" in campos:
        escribir(tabla, reg, "AUX", "N")
    respaldar(tabla)
    tabla["registros"].append(reg)
    guardar(tabla)
    print(f"agregado en {meta['etiqueta']}: {cod} · {args.descripcion}")
    print("Recordá reindexar en el SIGEP (Mantenimiento -> Utilitarios).")


def cmd_borrar(args) -> None:
    tabla, meta = abrir(args.tabla, args.datos)
    reg = buscar_reg(tabla, meta["clave"], args.codigo.strip())
    if not reg:
        raise SystemExit(f"no existe el código {args.codigo}")
    if reg[0] == 0x2A:
        print("ya estaba borrado")
        return
    respaldar(tabla)
    reg[0] = 0x2A
    guardar(tabla)
    print(f"borrado (marca de borrado) en {meta['etiqueta']}: {args.codigo}")
    print("Recordá reindexar en el SIGEP (Mantenimiento -> Utilitarios).")


def cmd_reactivar(args) -> None:
    tabla, meta = abrir(args.tabla, args.datos)
    reg = buscar_reg(tabla, meta["clave"], args.codigo.strip())
    if not reg:
        raise SystemExit(f"no existe el código {args.codigo}")
    if reg[0] != 0x2A:
        print("no estaba borrado")
        return
    respaldar(tabla)
    reg[0] = 0x20
    guardar(tabla)
    print(f"reactivado en {meta['etiqueta']}: {args.codigo}")
    print("Recordá reindexar en el SIGEP (Mantenimiento -> Utilitarios).")


def main() -> int:
    ap = argparse.ArgumentParser(description="Editor de catálogos del SIGEP")
    ap.add_argument("--datos", type=Path, default=REPLICA_DATA, help="carpeta Data del SIGEP")
    sub = ap.add_subparsers(dest="comando", required=True)

    p = sub.add_parser("listar", help="mostrar filas")
    p.add_argument("tabla", choices=list(TABLAS))
    p.add_argument("--buscar", default="")
    p.add_argument("--incluir-borrados", action="store_true")
    p.set_defaults(func=cmd_listar)

    p = sub.add_parser("agregar", help="agregar una fila")
    p.add_argument("tabla", choices=list(TABLAS))
    p.add_argument("codigo")
    p.add_argument("descripcion")
    p.add_argument("--tipo", default=None, choices=["N", "S"])
    p.add_argument("--nivel", type=int, default=None)
    p.set_defaults(func=cmd_agregar)

    for nombre, fn in (("borrar", cmd_borrar), ("reactivar", cmd_reactivar)):
        p = sub.add_parser(nombre)
        p.add_argument("tabla", choices=list(TABLAS))
        p.add_argument("codigo")
        p.set_defaults(func=fn)

    args = ap.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
