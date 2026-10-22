# 🏛️ SISTEMA SIGEP - CONTABILIDAD GUBERNAMENTAL Y PRESUPUESTOS (BOLIVIA)

Carpeta del Proyecto: `E:\Programa ing inversa\Proyecto Sigep`

---

## ⚡ ¿Cómo iniciar el sistema?

Simplemente haz doble clic en:
👉 **`INICIAR_SIGEP.bat`**

Se abrirá automáticamente en tu navegador web:
🌐 **`http://localhost:8000`**

*(También puedes hacer doble clic directamente sobre `index.html` si deseas abrirlo de forma instantánea sin servidor).*

---

## 🎯 Lo que tienes en esta aplicación:

1. **Ventana de Registro idéntica a tu captura ("quiero que sea así"):**
   - Barra superior azul: `Unidad : 001`, `Cbte : ...`, `Moneda : BBS`, `Código : [Momento]` (incluyendo el código **15 - Ingreso Devengado - Percibido**, **09 - GCT**, etc.).
   - Campos de cabecera: `Depositante`, `Fecha`, `Doc. de Respaldo`, `Dólar`, `UFV`.
   - Grilla con las columnas exactas:
     `AP` | `Gasto` | `Recurso` | `FF` | `OF` | `ET` | `CTA` | `Aux` | `Oec` | `Debe (Bs.)` | `Haber (Bs.)`
   - Panel inferior con información en tiempo real de la línea activa:
     `Linea No`, `Apertura`, `Gas/Rec`, `Oec`, `Cuenta`, `Auxiliar` y cuadro para la glosa/descripción.
   - Botones oficiales: `💾 Grabar`, `❌ Cancelar`, `👁️ Ver Cbte Oficial` y `🖨️ Imprimir Cbte (F8)`.
   - Atajos de teclado reales:
     - `[F4]` Elimina fila activa
     - `[CTRL+F4]` Limpia fila activa
     - `[CTRL+N]` Inserta 1 línea
     - `[F3]` Inserta varias líneas
     - `[F8]` Imprime el comprobante oficial

2. **Comprobante de Contabilidad para Imprimir (idéntico a la primera foto):**
   - Encabezado: *1814 - GM - GOBIERNO AUTÓNOMO MUNICIPAL DE SAN JOAQUÍN*, Dirección, Unidad Ejecutora, Fecha, Cbte No.
   - Tabla con separadores oficiales `..........PRESUPUESTO..........` y `.........CONTABILIDAD.........`.
   - Columnas: `CODIGO PRESUP.`, `PART. PRESUP.`, `CODIGO CONTABLE`, `CHEQUE NUMERO`, `L`, `DESCRIPCION DE LAS CUENTAS`, `D/H`, `PARCIALES`, `DEBE`, `HABER`.
   - Fila de `TOTALES`, nota legal `(A)`, monto en letras (`Son: ... Bs.`), Beneficiario, Descripción de la transacción y las 5 casillas de firmas `SIGEPMV` | `ELABORADO POR`, `REVISADO`, `APROBADO` x3.
   - Ajustado a hoja Carta (Letter) para imprimir directamente o guardar en PDF sin que se corte.

3. **Ejercicios de Clase y Casos Prácticos en el menú superior:**
   - **Ejercicio 1 (Del apunte manuscrito):** Venta de servicios, formularios (Bs. 200), carátulas municipales (Bs. 2000) y timbres (Bs. 700) por Bs. 2,900 en momento *Devengado de Recursos*.
   - **Ejercicio 2:** Ingreso Devengado - Percibido (Código 15) directo en caja por venta de valores.
   - **Ejercicio 3 (Comprobante San Joaquín):** Compra al contado de papelería, limpieza y útiles con cheque de Banco Unión por Bs. 18,000 (Código 09 - GCT / C-D-P).

4. **Catálogos Oficiales de Bolivia ya cargados:**
   - 492 Partidas de Gasto (10000 a 90000) del Clasificador Presupuestario 2026.
   - 341 Rubros de Recurso (10000 a 30000).
   - Plan General de Cuentas Contables del Sector Público MEFP (Manual de Cuentas).
