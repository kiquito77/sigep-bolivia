# Actualizar y editar los catálogos del SIGEP (copia `SIGEP-REPLICA`)

Herramientas para modificar las tablas FoxPro directamente, sin abrir Visual FoxPro.

## 1. Actualizar al clasificador 2026

```bash
python extraer_2026.py            # regenera clasificador_2026.json desde el PDF del MEFP
python actualizar_2026.py          # simulación: muestra qué cambiaría
python actualizar_2026.py --aplicar  # escribe en SIGEP-REPLICA\Data
```

Qué hace sobre `E:\Programa ing inversa\SIGEP-REPLICA\Data`:

| Tabla | Cambios aplicados |
|---|---|
| `s3gastos.dbf` | +9 partidas nuevas, 124 denominaciones actualizadas, 2 marcadas como borradas |
| `s3recur.dbf` | 79 denominaciones actualizadas |

Antes de escribir guarda un respaldo en `SIGEP-REPLICA\_backup_catalogos_2026`
(`s3gastos.dbf`, `s3recur.dbf` y sus `.CDX`).

## 2. Agregar, borrar o reactivar ítems

```bash
python catalogo_tool.py listar cuentas --buscar banco
python catalogo_tool.py agregar cuentas 11375 "Bancos - Cuenta Fiscal 2026"
python catalogo_tool.py borrar partidas 39990
python catalogo_tool.py reactivar partidas 39990
```

Tablas disponibles: `cuentas` (plan de cuentas), `partidas` (gastos), `recursos` (rubros).

Al agregar una cuenta, el nivel se calcula solo (5 − ceros finales) y el tipo `N`/`S`
se deduce del código. El borrado es **lógico**: marca el registro como borrado, no lo elimina,
igual que hace el SIGEP.

## 3. Paso obligatorio después de cualquier cambio

Los índices `.CDX` no se actualizan desde Python. Al terminar hay que abrir el SIGEP y ejecutar:

**Mantenimiento → Utilitarios → Reindexar la base de datos**

Esa utilidad existe en el sistema oficial (está documentada en el manual, página
`MANTENIMIENTO_UTILITARIOS1.htm`). Hasta hacerlo, las búsquedas por código pueden no
encontrar los ítems nuevos.

## 4. Si algo sale mal

Restaurar el respaldo sobre `SIGEP-REPLICA\Data`:

```
copy _backup_catalogos_2026\* Data\ /Y
```

y reindexar de nuevo.
