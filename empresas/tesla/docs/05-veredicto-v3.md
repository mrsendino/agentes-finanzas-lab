# 05 — Veredicto de verificación v3 (Reality Checker, tercera verificación)

**Fecha:** 2026-10-25 · **Rol:** Fase 5, *Reality Checker*. Por defecto, el estado es NECESITA TRABAJO salvo prueba abrumadora en contra · **Objeto:** 01 v3, 02 v3, 03 v3 y 04 v3 (rama `correccion/tesla-v3`, commits `3f92860`, `fc813fb`, `e8b18e5` y `84af2f7`) · **Alcance:** comprobar que se han aplicado las devoluciones de [05-veredicto-v2.md](05-veredicto-v2.md) §8, que el cambio de beta de 03 se ha propagado entero y que se cumple el criterio de APTO fijado en v2 §8. **No es una recomendación de inversión.** Este documento no modifica 01-04 ni los veredictos anteriores ([05-veredicto.md](05-veredicto.md) y [05-veredicto-v2.md](05-veredicto-v2.md)).

**Scripts de esta fase:**

| Script | Qué hace |
|---|---|
| [`scripts/fase5_consistencia.py`](../scripts/fase5_consistencia.py) | Expectativas actualizadas a v3 (registro v2 → v3 en la cabecera). Re-ejecuta fase2/3/4 en copia temporal |
| [`scripts/fase5v2_cifras.py`](../scripts/fase5v2_cifras.py) | Mismo comprobador de v2, con las anclas corregidas, cobertura nueva y cálculo exacto de ROIC/ROE (registro v2 → v3 en la cabecera). Es el que ejecuta `herramientas/verificar.py` |
| [`scripts/fase5v2_coherencia.py`](../scripts/fase5v2_coherencia.py) | Añade las cifras de v2 sustituidas en v3 y una §3 nueva con las referencias de 02 a otras fases (registro en la cabecera) |
| [`scripts/fase5v3_propagacion.py`](../scripts/fase5v3_propagacion.py) | **Nuevo.** Ejecuta el modelo de 03 v3 dos veces, con la beta de v3 y con las betas de v2, y busca en 01-04 cada texto de cifra que cambia |
| [`scripts/fase5v3_muestreo.py`](../scripts/fase5v3_muestreo.py) | **Nuevo.** Catálogo de 29 cifras no sorteadas antes. Semilla **20261026** |

En esta consola Windows todos se ejecutan con `PYTHONIOENCODING=utf-8 PYTHONUTF8=1`. Ninguno escribe en `data/` ni en `docs/`; `fase3_dcf.py` solo se ejecuta en copias temporales.

---

## 0. Veredicto

### **NECESITA TRABAJO (mínimo: 1 cifra)** · Calificación: **A−** (v2: B+; v1: B−)

**Lo que está bien** (con evidencia):
- `fase5v2_cifras.py` comprueba **577 cifras**: **576 OK, 0 DOBLE REDONDEO, 1 MISMATCH, 0 NO ENCONTRADA**. En v2 eran 541 cifras con 6 DOBLE REDONDEO y 6 MISMATCH.
- `fase5_consistencia.py` con expectativas v3: **0 MISMATCH** (23 de 23). `ratios.csv`, `checks.csv`, `tablas_02_redondeo.csv` y `cifras_03_redondeo.csv` regenerados son **idénticos byte a byte** a los del proyecto.
- **La beta de 03 §1 es reproducible hoy en sus dos fuentes.** Lo comprobé con WebFetch el 25-oct-2026: MarketChameleon dice "TSLA has a beta of 1.84" ("Data as of October 23, 2026") y TipRanks dice "Beta 1.84" (página modificada el 24-oct-2026).
- **Devoluciones de v2: de 15, 12 RESUELTAS, 3 DISPUTADAS y 0 PARCIAL o NO.** En las tres disputas la fase tiene razón (§3).
- **La propagación de la beta es completa.** El modelo con las betas de v2 y el de v3 dan 156 textos de cifra distintos (122 en 03 y 34 en la §14 de fase4). Ninguno sobrevive en el cuerpo de 01-04 como vigente sin etiqueta (§5).
- **Muestreo con otra semilla (20261026):** 10 de 10 sin FAIL, con un matiz de redacción (§4.2). En una segunda ronda voluntaria, 9 de 10 pasan; la décima es un dato de mercado que ha cambiado desde la fecha citada.
- Los cambios de los modelos son solo los declarados. En `fase3_dcf.py` cambian únicamente las dos betas y se añade la §10, que es solo de salida. Las 485 fórmulas de `dcf.xlsx` son **idénticas** a las de v2, que se verificó con LibreOffice.

**Por qué no es APTO.** El criterio que fijé en v2 §8 era 0 MISMATCH en `fase5v2_cifras.py`, y queda 1:
- **M-v3-1 (04 §1, tabla de hechos):** "ROIC A TTM / WACC inicial | 5,5 % / 11,55 % (diferencial **−6,1 pp**)". El valor exacto es 5,510 % − 11,555 % = **−6,04 pp → −6,0 pp**.
- **Causa:** `fase4_opcionalidad.py` usa `ROIC_A_TTM = 0.055`, una constante copiada a mano de 02 a un decimal. Es el mismo patrón que v3 corrigió para `WACC0`: 0,055 − 0,11555 = −6,05 → −6,1. Es un doble redondeo.
- **No es un error heredado:** en v2 la cifra era correcta (5,51 − 11,60 = −6,09 → −6,1). Aparece por el cambio de WACC. Lo detecta la cobertura nueva del comprobador.

**Lo que no cambia:** ninguna conclusión. El caso base pasa de 24,61 $ a 24,65 $ (24,7 $ a un decimal) y el rango del negocio reportado sigue en 10-56 $ frente a 372,22 $. La corrección que falta es una celda de 04 y una línea del script de Fase 4.

---

## 1. Re-ejecución de scripts y expectativas v2 → v3

| Script | Resultado |
|---|---|
| `fase2_ratios.py` | rc = 0. 109 filas (v2: 94): se añaden 15 y **ninguna fila de v2 cambia de valor** más allá del redondeo (comprobado celda a celda frente a `c9a0e31`). Controles: **72 = 67 OK + 5 DISCREPANCIA**. Las filas % pasan a 6 decimales, salvo 3 a 4 decimales que usa fase3 |
| `fase3_dcf.py` | rc = 0. VPA **10,41 / 24,65 / 55,88 $**; diluidos **10,37 / 24,56 / 55,67 $**. WACC inicial **11,5548 % → 11,55 %** (no 11,56: el script avisa del riesgo de doble redondeo) |
| `fase4_opcionalidad.py` | rc = 0. EBIT_10 central **147.484 M$**. WACC0 y WACC_T salen ahora de `f3` |
| `fase1_cifras.py` (nuevo) | rc = 0. Recalcula 33 cifras de 01: **3 de 3 comprobaciones en el documento OK**; +18,9 %, 12,0 % y 10,7 % |

**Expectativas cambiadas en `fase5_consistencia.py`** (solo valores esperados):

| Expectativa | v2 | **v3** | Script v3 |
|---|---:|---:|---:|
| WACC inicial | 11,60 % | **11,55 %** | 0,1155 |
| VPA bajista / base / alcista (1 dec.) | 10,4 / 24,6 / 55,8 | **10,4 / 24,7 / 55,9** | 10,41 / 24,65 / 55,88 |
| VPA totalmente diluidos | 10,36 / 24,52 / 55,55 | **10,37 / 24,56 / 55,67** | igual |
| EV base | 61.353 | **61.526** | 61.526 |
| TACC con margen del 20 % | 36,1 % | **36,0 %** | 36,04 % |
| EBIT_10 central (04) | 147.527 | **147.484** | 147.484 |
| W9 desplazando el terminal | +4,6 $ | **+4,4 $** | +4,41 |
| Tabla 4.1 para interpolar W9 | 10,6 % / 11,6 % → 28,55 / 24,60 | **10,55 % / 11,55 % → 28,6 / 24,7** | interpolación 29,0 $ (+4,3) |
| Sin cambio | WACC_T 9,79 %; TACC 30 % 27,8; 407,4 $; 198 $; 6,6 %; D&A 6.704; 3.967,3 M; capex año 1 15.884; W9 +1,2 $; FCFF año 1 −5.700 | igual | igual |

Ajuste técnico: la comparación usa tolerancia + 1e-9, porque el script imprime 24,65 y |24,7 − 24,65| = 0,05 en coma flotante. **Resultado: 0 MISMATCH.**

### 1.1 `dcf.xlsx` sin valores cacheados (regresión frente a v2)

- **Hecho:** el libro de v3 tiene 485 fórmulas y **0 valores cacheados**, porque en este equipo no hay LibreOffice. Lo comprobé: no hay `soffice` en el PATH ni en `C:\Program Files\LibreOffice`.
- **Evidencia de que no hay error de modelo:** comparé celda a celda el libro de v2 (`c9a0e31`) con el de v3. Las **485 fórmulas son idénticas**. Cambian solo los inputs (B13 1,85 → 1,84 y B14 1,87 → 1,84), sus textos de fuente y las tablas estáticas que escribe Python (sensibilidades, DCF inverso). El libro de v2 sí se recalculó con LibreOffice, con 0 errores y valores iguales a los de Python. Por eso, con las mismas fórmulas, el de v3 debería dar lo mismo que Python al abrirlo.
- **Valoración:** CLAUDE.md lo permite, y 03 lo declara en su tabla de archivos. **No bloquea.** Pero es una regresión de usabilidad real: cualquier lectura sin recalcular (`openpyxl data_only=True`, pandas, una vista previa) devuelve celdas vacías. **Recomendación** (no es devolución): recalcular el libro en un equipo con LibreOffice antes del merge, o decirlo en el PR.

---

## 2. Cifras de los documentos frente a la salida de los scripts

`fase5v2_cifras.py` (catálogo ampliado en v3; las cifras esperadas salen siempre de la ejecución viva de fase2/3/4):

| Documento | OK | Doble redondeo | **MISMATCH** | No encontrada |
|---|---:|---:|---:|---:|
| 01 | 19 | 0 | 0 | 0 |
| 02 | 312 | 0 | 0 | 0 |
| 03 | 189 | 0 | 0 | 0 |
| 04 | 56 | 0 | **1** | 0 |
| **Total** | **576** | **0** | **1** | **0** |

**Antes de actualizar el catálogo**, con los documentos v3 el resultado era 532 OK, 0 doble redondeo, 0 MISMATCH y **9 NO ENCONTRADA**:
- 8 en 04 y 1 en 03 (§8). Sus anclas contenían valores de v2, como "10,40 / … / 55,76" o "(24,6 → ".
- Con las anclas nuevas, las 9 dan OK: 24,65; 55,67; 25,49; 25,5; 25,8; 29,1; 28,5; 31,7; y 25,8 en 03 §8.
- Fase 4 lo anticipó correctamente en su registro.

**Cobertura añadida en v3** (36 cifras):
- beta de regresión en 03 §1 y §1.1 (1,84 / 1,84 / 1,84);
- W9 desplazado (+4,4 $ y 29,1 $; WACC_T 8,70 %) en 03 y 04;
- margen operativo TTM 3,3 % en 02 §0, 03 §7 y 04 §3.2;
- los seis VPA de 04 §4.2.4;
- los puntos de partida de 04 (24,65 / 24,7 $);
- el rango del saldo (10,4-55,9 $);
- el ROIC terminal de 04 §4.2.2 (23,7-25,5 $);
- WACC 11,55 % en 04 §0, §1 y §2.3;
- el diferencial ROIC − WACC en 04 §1 (M-v3-1).

**Corrección de un punto ciego de v2.** Para ROIC A, ROIC B y ROE, el comprobador comparaba con `ratios.csv` a 4 decimales y no con el valor exacto. Por eso en v2 no vi el ROIC B FY23 (12,145 % escrito 12,2 %), que sí encontró Fase 2. Ahora se recalculan desde el NOPAT y el capital medio, con la misma fórmula que `fase2_ratios.py`. Las 312 celdas de 02 dan OK, también el 12,1 %.

### 2.1 MISMATCH

| # | Dónde | Dice | Exacto | Causa |
|---|---|---|---|---|
| **M-v3-1** | 04 §1 (tabla de hechos) | −6,1 pp | **−6,04 → −6,0 pp** | `ROIC_A_TTM = 0.055` copiado a mano (02 §6 a un decimal) en `fase4_opcionalidad.py`. El registro v3 de 04 dice "−6,05 a 2 decimales; sin cambios a 1 decimal", pero ese −6,05 sale de la constante redondeada; con el valor completo (5,510 %, de `ratios.csv` y del capital medio) es −6,04 |

---

## 3. Trazabilidad de las devoluciones de v2 (05-veredicto-v2 §8)

Estado: **RESUELTO** / **PARCIAL** / **NO** / **DISPUTADO** (la fase discrepó de 05 v2; se juzga con la evidencia).

| # | Devolución v2 | Lo que dice la fase | Verificación de Fase 5 v3 | Estado |
|---|---|---|---|---|
| 2-a | % de las tablas desde el valor completo: 3,3 / 39,0 / 10,3 / 109,4 / 51,4 / 2,0 % | Las 6 corregidas, más 3 que encontró el script: ROIC B FY23 12,1 %, CAGR de automoción 10,1 % y crecimiento del FCF FY25 +73,5 %. Nuevo `tablas_02_redondeo.csv` | 312 de 312 celdas de 02 OK, 0 doble redondeo. El CSV regenerado es idéntico. 02 §0 dice "3,3 % (TTM)" | **RESUELTO** |
| 2-b | E1: las 4.254 M y "03 §6.4" como vigentes | Presentadas como **03 v1**; 7,2 % y 10,7 % desde el script | 02 l. 238: "Las 4.254 M de **03 v1** … sobrestimaban un 7,2 %"; filas `acc_portada_mas_301_sobre_fd` y `acc_diluida_media_sobre_fd` | **RESUELTO** |
| 2-c | E2: D1-D6 resueltos y etiquetas de los **5** controles de `checks.csv` a "S2 / 01 v1" | D1-D7 dicen "Resuelto en 01 v2". **Discrepa en parte:** solo 4 controles citaban 01; el de capex FY2024 compara con S1 Tabla 2.2; al PER y a la deuda no les corresponde "S2" | `git show c9a0e31:…/checks.csv`: el control de capex FY2024 dice "S1 Tabla 2.2", **nunca citó 01**. Las etiquetas nuevas ("S2 / 01 v1", "P1 Item 1A / 01 v1", "S11 / 01 v1") son más exactas que mi propuesta. **La fase tiene razón; mi "5 controles … S2" era incorrecto** (§6) | **DISPUTADO → a favor de Fase 2** |
| 2-d | Frase de 1T26 (método de tesorería) y secundaria de la cancelación | ~286,2 M (283,7-288,2 M entre 350 y 450 $) + ~17,8 M de empleados; precio medio SIN VERIFICAR; la secundaria no da la cifra de 96 M | 303,96 × (1 − 23,34 / 400) = 286,22 M ✓. 02 §8.3 (8) lo declara | **RESUELTO** |
| 3-a | M1: 25,9 → 25,8 $ en §4.3 y §8 | §4.3: 25,8 $; §8: "23,7-25,8 $". El extremo bajo pasa a 23,7 por la beta | W9_15 = 25,848 → 25,8 ✓; ROIC = WACC → 23,680 → 23,7 ✓ (catálogo, las dos anclas) | **RESUELTO** |
| 3-b | M2: 25,5 → 25,4 $ en §6.3 | **Discrepa con evidencia nueva:** con la beta de v3, la variante vale 25,490 $ → 25,5 $ | Modelo v3: `ASYM_RES[1]` = 25,4904 → **25,5** ✓. Con las betas de v2 (variante de `fase5v3_propagacion.py`) da 25,446 → 25,4. Mi petición era correcta para el modelo de v2, pero **la invalidó mi propia devolución 3-c**, que cambia los inputs. 25,5 es lo correcto hoy | **DISPUTADO → a favor de Fase 3** |
| 3-c | FAIL-v2-1: volver a citar la beta de MarketChameleon o retirarla | Las dos fuentes re-consultadas: 1,84 y 1,84 (`nuevas_fase3_v3.md`) | WebFetch (25-oct-2026): MarketChameleon "TSLA has a beta of 1.84"; "Data as of October 23, 2026" ✓. TipRanks "Beta 1.84", modificada el 24-oct-2026 ✓. `fase3_dcf.py`: solo cambian `beta_reg_1` y `beta_reg_2` | **RESUELTO** |
| 3-d | Recoger el 3,3 % en §7 | "varias veces el 3,3 % de Tesla (… 02 v3)" | Catálogo: 3,347 % → 3,3 ✓ | **RESUELTO** |
| 3-e | Generar las cifras del documento desde la salida del script con un solo redondeo | §10 nueva: `cifras_03_redondeo.csv` (220 cifras, `Decimal`, mitad hacia arriba); 03 copia de la columna `texto` | El CSV regenerado es idéntico. 189 cifras de 03 OK. El script avisa además de las cifras con riesgo de doble redondeo (p. ej. 11,5548 → 11,55, no 11,56) | **RESUELTO** |
| 4-a | Propagar M1 (§4.1.3: "24,6 → 25,8 $") | "24,7 → 25,8 $" (el caso base nuevo es 24,654) | Catálogo: 24,7 ✓, 25,8 ✓, +1,2 ✓ (1,19; no 25,8 − 24,7 = 1,1: redondeo único, bien explicado por 04) | **RESUELTO** |
| 4-b | Propagar M2 (§4.1.1: "(25,4 / 26,3 $)") | Mantiene 25,5 / 26,3, como 03 v3 | Igual que 3-b; además 25,49 / 26,30 $ a 2 decimales ✓ | **DISPUTADO → a favor de Fase 4** |
| 4-c | 3,3 % en §3.2 | "al 3,3 % TTM (02 v3)" | Catálogo ✓ | **RESUELTO** |
| 4-d | "10-60 $" → "10-56 $" en el saldo | "10-56 $ por acción (10,4-55,9 $ en 03 v3)" | Catálogo: 10,4 ✓, 55,9 ✓. No queda ningún "10-60 $" (`fase5v3_propagacion.py`) | **RESUELTO** |
| 1-a | M3: Servicios FY25 +18,9 % | +18,9 % (18,9482 %), con `fase1_cifras.py` | Catálogo y `fase1_cifras.py` ✓. Coincide con 02 | **RESUELTO** |
| 1-b | Base del "~12 % del capital" | 12,0 % del capital previo (3.529.014.042) y 10,7 % de la portada | 423.743.904 / 3.529.014.042 = 12,007 % ✓; / 3.952.757.946 = 10,720 % ✓ | **RESUELTO** |

**Recuento: 15 devoluciones → 12 RESUELTO, 0 PARCIAL, 0 NO, 3 DISPUTADO** (las tres a favor de la fase: 2-c, 3-b y 4-b).

**Cómo juzgo las dos discrepancias:**
- **M2 = 25,5.** La fase tiene razón con evidencia reproducible. Ejecuté el mismo `fase3_dcf.py` v3 con las betas de v2 y da 25,446 $ (25,4); con las de v3 da 25,490 $ (25,5). La diferencia se explica entera por el cambio de beta que yo pedí. No es un error de redondeo.
- **Etiquetas de `checks.csv`.** La fase tiene razón: el control de capex FY2024 nunca comparó con 01. Mi propuesta habría puesto una etiqueta falsa en un control correcto.

---

## 4. Verificación de fuentes

### 4.1 Beta (criterio de APTO: "la beta citada en 03 §1 reproducible en su fuente")

| Fuente | Lo que dice hoy (WebFetch, 25-oct-2026) | 03 v3 §1 | Resultado |
|---|---|---|---|
| [MarketChameleon](https://marketchameleon.com/Overview/TSLA/Summary/) | "TSLA has a beta of 1.84"; "Data as of October 23, 2026"; cierre de 372,22 $ el 23-oct | 1,84 | **OK** |
| [TipRanks](https://www.tipranks.com/stocks/tsla/statistics) | "Beta 1.84"; `dateModified` 24-oct-2026 | 1,84 | **OK** |

La media de 1,84 entra en el modelo (`BETA_REG = 1,84`, `BETA0 = 1,58`) y en la hoja `Supuestos` de `dcf.xlsx` (B13 = B14 = 1,84). **Criterio cumplido.**

### 4.2 Muestreo aleatorio con otra semilla

`python scripts/fase5v3_muestreo.py` → **semilla 20261026**. El catálogo tiene 29 cifras: las 19 del catálogo v2 que no salieron con la semilla 20261025, sin la beta (G19), más 10 nuevas.

**Ronda 1 (la que exige el criterio):**

| # | Cifra | Doc | Fuente | Lo que dice la fuente | Resultado |
|---|---|---|---|---|---|
| G07 | Guía de capex 2026 previa ">25.000 M$" (call 1T26) | 03 §2.1 | T10 | "Investitionsausgaben 2026 auf über 25 Milliarden Dollar" (26-abr-2026) | OK |
| H07 | I+D 3T26 2.761 frente a 1.630 M$ | 01 §1.2 / 03 §6.3 | P4 | 2.761 / 1.630; "SI and other R&D projects" (dentro de la frase sobre los gastos operativos) | OK |
| G16 | Créditos regulatorios FY2024 2.763 M$ | 02 §2 | R45 | 2.763 (FY23: 1.790; FY22: 1.776) | OK |
| H03 | VW EV/Ventas 0,94; EV/EBITDA 6,27; PER 6,6 | 03 §7 | TipRanks | 0,94 / 6,27 / 6,6 (modificada el 25-oct) | OK |
| G08 | China FY25 20.962 M$ (~22,1 %); 1S26 8.859 M$ (17,5 %) | 01 §3 | S1 | "China … was $20,962m in 2025"; tabla: China 8.608 → 8.859; "China 22.1% and 17.5%" | OK |
| G33 | Call 4T25: >500 vehículos y "dozens" de ciudades a fin de 2026 | 01 §5 | S5 | "well over 500 **at this point**"; "dozens of major cities by the end of the year" | **OK con matiz**: los >500 eran la flota de enero de 2026, no un objetivo para fin de año. La frase de 01 ("habló de >500 vehículos y 'dozens' de ciudades a final de 2026") aplica la fecha a las dos cifras |
| G30 | ARR de FSD ~1.000 M$, CFO "correct" | 04 §2.2 | T1 | Taneja: "Yes. I think the numbers which you shared are correct" (estimación de Ferragu, ~1.000 M$) | OK (04 ya lo marca [CALL]) |
| G36 | Elluswamy: Dallas con Cybercab "next month"; "6 cities now" | 04 §2.2 | T1 | "next month, we'll be launching in Dallas"; "we do 6 cities now" | OK |
| G06 | Benchmark: Tesla 2.ª con ~10 % frente al ~13 % de BYD | 01 §2 | S8 | BYD 13 %, Tesla 10 %, Sungrow 9 % | OK |
| G01 | Efectivo 17.853 + inversiones a corto plazo 27.594 | 01 §1.2 | P2 | 17.853 / 27.594 | OK |

**10 de 10 sin FAIL** (1 matiz de redacción). Criterio cumplido. Según mi propia regla, desconfío de una ronda perfecta y sorteo 10 más.

**Ronda 2 (voluntaria):**

| # | Cifra | Doc | Fuente | Lo que dice la fuente | Resultado |
|---|---|---|---|---|---|
| H04 | BYD EV/Ventas 1,00; EV/EBITDA 6,37; PER 25,2 | 03 §7 | TipRanks | 1,00 / 6,37 / 25,2 | OK |
| G26 | "Optimus production began in Fremont on our high-volume lines" | 04 / 01 | P4 | Literal | OK |
| G22 | GM 1,00 / 9,99 / 17,2 | 03 §7 | TipRanks | Idéntico | OK |
| G34 | SBC 3T26 1.165 M$ vinculada al 2025 CEO Performance Award | 02 / 03 | P4 | 1.165; "SBC (including 2025 CEO Performance Award)" | OK |
| H10 | Portada del 10-K FY25 3.752.431.984 (23-ene-2026); principal 8.180 M$ | 01 §2 | P1 | Literal; "$8.18 billion in aggregate principal amount of indebtedness" | OK |
| H05 | Toyota EV/Ventas 1,45 (EV 418,59 bill. $) | 03 §5 / §7 | TipRanks | 1,45; EV 418,59 bill. $; 9,46; 8,8 | OK |
| **G20** | **Nvidia EV/Ventas 21,04; EV/EBITDA 31,43; PER 27,9 (23-oct)** | **03 §7** | **TipRanks** | **21,04 / 31,43 / PER 26,5** (página modificada el 25-oct) | **NO REPRODUCIBLE HOY** (el PER) |
| H06 | Entregas FY25 1.636.129; almacenamiento 46,7 GWh | 01 / 03 §2.3 | P6 | Literal | OK |
| H08 | Energía TTM 12.265 M$ | 03 §2.1 | P4 | 3.837 + 2.408 + 3.139 + 2.881 = 12.265 | OK |
| G09 | Plan del CEO aprobado el 6-nov-2025 con >75 % | 01 §4 | S10 | Literal | OK |

**Ronda 2: 9 de 10.** G20 es el mismo fenómeno que la beta en v2: una página de cotizaciones que se actualiza a diario. El PER de Nvidia era 27,9 en la fecha citada (23-oct) y hoy es 26,5. Archive.org no tiene captura cercana (la última es del 15-sep-2026), así que no se puede comprobar en ningún sentido.
- **Efecto:** la mediana del PER big tech pasaría de 33,6 a 32,9, y el precio implícito por PER de ~30,5 $ a ~29,9 $. **Inmaterial**, y en la fila que 03 ya declara "no representativa" (n = 2).
- **Calificación:** con el estándar de v2 sería un FAIL. Con el criterio corregido de §6.3 es un dato fechado que no se puede reproducir, no un error del documento. **No lo convierto en devolución.**

---

## 5. Propagación de la beta y coherencia entre fases

**`fase5v3_propagacion.py`.** Ejecuta `fase3_dcf.py` v3 y `fase4_opcionalidad.py` v3 dos veces en copias temporales, con las betas de v3 (1,84 / 1,84) y con las de v2 (1,85 / 1,87):
- cambian **122 de 220** textos de `cifras_03_redondeo.csv` y **34** números de la §14 de fase4;
- de esos textos, se buscan en el cuerpo de 01-04 los **90** que tienen 4 o más caracteres, más una lista fija: 11,60 %, 11,6 %, 1,85, 1,86, 1,87, "3,4 % (TTM", +19,0 %, 25,9 $, 25,4 $ y "10-60 $";
- **10 apariciones están ETIQUETADAS** como v2 o anteriores, por ejemplo "El WACC inicial baja de 11,60 % a 11,55 %" en 03 §0 o "con la beta de regresión de v2, 1,86" en 03 §4.3;
- **7 se marcan REVISAR, y las 7 son falsos positivos** revisados a mano:

| Aparición | Por qué no es una cifra v2 vigente |
|---|---|
| 03 §1.1 "Coste del capital propio inicial 11,60 %" | Es el Ke de **v3**: 4,97 + 1,58 × 4,20 = 11,60 % (en v2 era 11,64 %). Coincide por casualidad con el WACC de v2 |
| 02 §4 "Capex / ingresos … 11,6 %" (FY2024) | Otra métrica |
| 01 §1.2 / 01 §4 / 03 §2.2 "15,9" | Margen bruto de servicios de 3T26 y otra columna; no es la sensibilidad 4.2 |
| 02 §6 "ROIC B FY22 25,4 %" | Otra métrica |
| 02 §2 "energía: 46,3 %" | CAGR de energía |

**No queda ningún 11,60 % (WACC), 24,61, 55,76, 10,40 /, 24,52, 55,55, 61.353, 147.527, 25,9 $, 29,2 $, +4,6 $, 3,4 % TTM ni "10-60 $" vigente sin etiqueta en 01-04.** La única cifra mal propagada es M-v3-1. No la detecta este script porque no es un texto de v2 que sobreviva, sino una cifra recalculada con un input redondeado.

**`fase5v2_coherencia.py` v3:**
- §1: el margen operativo TTM es **3,3 % en 02, 03 y 04**; el WACC inicial, **11,55 %** en 03 y 04; los VPA, idénticos en 03 y 04 (10,41 / 24,65 / 55,88 y 10,37 / 24,56 / 55,67).
- §2: 8 apariciones sin etiqueta en la misma línea, todas falsos positivos o contrastes declarados. Ejemplos: "87,7 %" contiene "7,7 %"; 01 §1.2 cita S2 (2.760 / 1.170) como contraste con "prevalece P4"; "~51 $" es el valor v3 de la sensibilidad; "~0,7-1,4 billones $" es capital nuevo, no capitalización.
- **§3 (criterio de APTO: referencias de 02 a v1 presentadas como vigentes):** 7 líneas de 02 nombran otras fases sin etiqueta de versión. 6 son referencias neutras o ciertas: secciones de 01 citadas como contexto, y "Todos coinciden con 01-negocio.md" para el 3T26, que es cierto. **1 es cosmética:** 02 §1.2 dice "Las cifras FY2025 de 01-negocio.md marcadas como 'solo secundaria' quedan confirmadas". El dato es correcto, pero 01 v2 ya retiró esas marcas. E1 y E2, las dos que pedí, están resueltas. **Criterio cumplido**; la cosmética queda como opcional.

**Observación sobre 03 §5.** Con la beta nueva aparece "con la TACC alcista haría falta un margen del **100,0 %**". El valor exacto es 99,9991 %: el precio se alcanza justo en el borde del intervalo de búsqueda [0, 1], y con la beta de v2 no se alcanzaba. 03 lo presenta bien ("es decir, que no hubiera ningún coste"; "con la beta de v2 tampoco bastaba el 100 %"). La conclusión es la misma, pero es un resultado en el filo que se movería con cualquier input.

---

## 6. Dónde me equivoqué en v2

1. **Etiquetas de `checks.csv` (E2).** Escribí que "los 5 controles DISCREPANCIA comparan con valores de 01 v1" y pedí ponerles "S2 / 01 v1" a los cinco. **Falso para uno:** el de capex FY2024 (11.339 frente a 11.342) siempre comparó con S1 Tabla 2.2. Además, "S2" no es la fuente del PER (S11) ni de la deuda (P1). No abrí `checks.csv` fila a fila antes de redactar la devolución. Fase 2 lo hizo y tenía razón.
2. **Un punto ciego de mi comprobador.** Dije que `fase5v2_cifras.py` comparaba "todas las celdas numéricas" de 02 §2-§6 con el valor exacto. Para ROIC A, ROIC B y ROE usaba en realidad el valor de `ratios.csv` a 4 decimales, que es justo el defecto que yo criticaba. Por eso no vi el ROIC B FY23 (12,145 % → 12,2 %), que encontró Fase 2 con su script. Tampoco cubría las cifras del texto de 02 (CAGR de automoción y crecimiento del FCF FY25), también corregidas por Fase 2. Además, el comprobador no trata NO ENCONTRADA como fallo: tras las ediciones de v3, 9 cifras quedaron sin comprobar y `verificar.py` habría seguido diciendo "Todo cuadra" si no hubiera habido otro error.
3. **La beta como "FAIL de fuente" y el criterio de "reproducible en su fuente".** Llamé FAIL a una cotización de una página que cambia a diario y pedí que fuera reproducible. Hoy el PER de Nvidia de esa misma familia de páginas tampoco se reproduce (§4.2). En v2 di además por "confirmada" la beta de 1,85 de TipRanks, que hoy da 1,84; no puedo saber si cambió entre el 23 y el 25 de octubre o si la leí mal. **El criterio correcto** para datos de mercado es un valor con fecha y una copia archivada (captura guardada en `fuentes/` o en archive.org). Que la página diga lo mismo días después no es un buen control.
4. **El alcance del cambio de beta y el orden de mis devoluciones.** Estimé el efecto de la beta en "+0,03 $" (solo MarketChameleon a 1,84). Con las dos fuentes en 1,84 es +0,04 $, que basta para que el caso base pase de 24,6 a 24,7 $ a un decimal, W9 desplazado de +4,6 a +4,4 $ y M2 de 25,4 a 25,5 $. Cambian 122 de 220 cifras de 03. Lo llamé "inmaterial", y en valor lo es, pero no previ cuántas cifras movería. Además, pedí a la vez 3-b (escribir 25,4) y 3-c (cambiar la beta), y la segunda invalidaba la primera. Debí pedir "recalcular después de (c) y copiar del script", no un número concreto.

---

## 7. Comparación v2 → v3

| Indicador | v2 (25-oct) | **v3 (25-oct)** |
|---|---|---|
| Cifras comprobadas contra el script | 541: 529 OK, 6 doble redondeo, 6 MISMATCH (3 cifras) | **577: 576 OK, 0 doble redondeo, 1 MISMATCH, 0 no encontradas** |
| `fase5_consistencia.py` | 0 MISMATCH (21) | **0 MISMATCH (23)** |
| Beta reproducible en sus fuentes | No (1,87 → 1,84) | **Sí (1,84 / 1,84)** |
| Muestreo (ronda del criterio) | 19 de 20 (FAIL: beta) | **10 de 10** (1 matiz); ronda extra 9 de 10 (dato de mercado vivo) |
| Referencias de 02 a v1 como vigentes | 2 (E1, E2) | **0** (1 cosmética) |
| Devoluciones de la ronda anterior | 24 → 21 / 1 / 0 / 2 | **15 → 12 RESUELTO / 0 PARCIAL / 0 NO / 3 DISPUTADO** |
| Cifras v2 de la beta vigentes sin etiqueta | — | **0** de 156 textos que cambian |
| Margen operativo TTM | 3,4 % (mal redondeado) | **3,3 %** en 02, 03 y 04 |
| `dcf.xlsx` | Con caché, idéntico a Python | **Sin caché** (sin LibreOffice); fórmulas idénticas a v2 |
| WACC inicial | 11,60 % | **11,55 %** |
| Valor por acción del negocio reportado | 10,40 / 24,61 / 55,76 $ (diluidas: 10,36 / 24,52 / 55,55) | **10,41 / 24,65 / 55,88 $** (diluidas: 10,37 / 24,56 / 55,67) |
| Opcionalidad implícita | 316-362 $ por acción | **316-362 $** (316,3-361,8) |
| Conclusión (orden de magnitud) | Decenas de $ frente a 372 $ | **Sin cambios** |
| Calificación | B+ | **A−** |

**Por qué A− y no A:**
- queda 1 cifra que no coincide con el script, y aparece en la tabla de hechos de 04;
- `dcf.xlsx` vuelve a no tener caché;
- dos cifras de mercado (beta y PER de Nvidia) no tienen copia archivada;
- quedan dos matices de redacción (G33 en 01 y 02 §1.2).

**Por qué sube de B+:**
- se cumplen todos los demás puntos del criterio de v2;
- las tres disputas se resolvieron con evidencia reproducible;
- los tres scripts nuevos o reforzados (`fase1_cifras.py`, `tablas_02_redondeo.csv` y `cifras_03_redondeo.csv`) eliminan la causa del doble redondeo en 01, 02 y 03.

---

## 8. Devoluciones restantes

| Prio. | Fase | Qué corregir | Por qué |
|---|---|---|---|
| **1** | **Fase 4** | M-v3-1: en `fase4_opcionalidad.py`, leer el ROIC A TTM de `ratios.csv` (`roic_A_neto_caja`, TTM_Q3_2026) o calcularlo desde el NOPAT y el capital medio, en lugar de `ROIC_A_TTM = 0.055`. Copiar de la §14 el diferencial nuevo en 04 §1: **−6,0 pp** | Es la única cifra que no coincide con el script. Mismo patrón que WACC0 en v2.1 |
| Opcional | Fase 1 | G33 (01 §5): los ">500 vehículos" eran la flota de enero de 2026 ("well over 500 at this point"); el objetivo de fin de 2026 son solo los "dozens" de ciudades | Precisión de la fecha; la cifra es correcta |
| Opcional | Fase 2 | 02 §1.2: "Las cifras FY2025 de 01-negocio.md marcadas como 'solo secundaria'" → indicar que 01 v2 ya retiró las marcas | Cosmético, del mismo tipo que E2 |
| Opcional | Fase 3 | Archivar una copia fechada de las páginas de mercado (beta, múltiplos de TipRanks) en `fuentes/`, o enlazar una captura de archive.org. El PER de Nvidia ya no se reproduce (26,5 frente a 27,9) | Que los datos de mercado se puedan verificar (§6.3) |
| Opcional | Orquestador | Recalcular `dcf.xlsx` con LibreOffice antes del merge, o decir en el PR que va sin valores cacheados | Regresión de usabilidad, no de modelo (§1.1) |

**Criterio para pasar a APTO:** `python herramientas/verificar.py tesla` → "Todo cuadra" (0 MISMATCH y 0 DOBLE REDONDEO con el catálogo v3). Basta con corregir M-v3-1, y no hace falta otra ronda completa. Bastaría con que Fase 4 lo corrija y yo vuelva a ejecutar los scripts. Recomiendo además, al orquestador y no como condición, que `verificar.py` trate como fallo una línea TOTAL con NO ENCONTRADA > 0 (§6.2).

---

*Reproducibilidad:* `python scripts/fase5_consistencia.py`, `python scripts/fase5v2_cifras.py [-v]`, `python scripts/fase5v2_coherencia.py`, `python scripts/fase5v3_propagacion.py [-v]` y `python scripts/fase5v3_muestreo.py [semilla]`, con `PYTHONIOENCODING=utf-8 PYTHONUTF8=1` en Windows. Ninguno escribe en `data/` ni en `docs/`. La verificación contra fuentes se hizo con WebFetch el 25-oct-2026 sobre las URL de `fuentes/fuentes.md` y `fuentes/nuevas_fase*_v*.md`. Las cifras en dólares de China (S1) se leyeron del HTML descargado de la página, porque WebFetch solo devolvía los porcentajes. No hay fuentes nuevas de Fase 5, así que no se crea `fuentes/nuevas_fase5_v3.md`.
