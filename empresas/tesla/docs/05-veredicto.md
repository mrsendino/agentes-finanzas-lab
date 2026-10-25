# 05 — Veredicto de verificación (Reality Checker)

**Fecha:** 2026-10-24 · **Rol:** Fase 5, *Reality Checker*. Por defecto, el estado es NECESITA TRABAJO salvo prueba abrumadora en contra · **Alcance:** comprobar que el análisis es internamente coherente, que cada cifra se puede rastrear hasta una fuente real y que las conclusiones están respaldadas por los números. **No es una recomendación de inversión.** Este documento no modifica 01-04.

**Scripts de esta fase:**

| Script | Qué hace |
|---|---|
| [`scripts/fase5_muestreo.py`](../scripts/fase5_muestreo.py) | Catálogo de 40 cifras extraídas de 01-04 con su fuente citada. Sorteo con semilla impresa (`20261024`): ronda 1 = 10 cifras; ronda 2 = 10 más |
| [`scripts/fase5_consistencia.py`](../scripts/fase5_consistencia.py) | Re-ejecuta fase2/3/4 en una copia temporal (no toca `data/`), compara su salida con las cifras de los documentos y re-calcula las críticas de Fase 4 |

---

## 0. Veredicto

### **NECESITA TRABAJO**

**Lo que está bien** (con evidencia):
- Los tres scripts se ejecutan sin errores y reproducen **todas** las cifras clave citadas en 02, 03 y 04. `ratios.csv` y `checks.csv` regenerados son **idénticos byte a byte** a los del proyecto.
- `dcf.xlsx`, recalculado en LibreOffice, da los mismos valores que Python (10,36 / 24,53 / 54,88 $; WACC 11,597 % y 9,788 %) y no tiene errores de fórmula.
- 20 de 20 cifras sorteadas coinciden con su fuente en el **valor**.

**Por qué no es APTO.** La puntuación perfecta en el muestreo era una señal de alarma, así que se buscaron fallos de forma dirigida. Aparecieron:
- **1 afirmación que la fuente no respalda** (01: "1.º integrador BESS según Wood Mackenzie").
- **Correcciones de Fase 2 que nunca llegaron a 01**: siguen ahí 5 cifras desfasadas o con fechas mezcladas.
- **Una afirmación falsa en 03 sobre sus propios supuestos**: "ROIC terminal del 12 %, dentro del rango 13-48 %".
- **Una línea de dilución en 03 sin base documental.**
- **Tres críticas de Fase 4 que no se sostienen** (W3/§4.1.2, W5, W1) y una sobredimensionada (W9). Si 03 se corrigiera siguiéndolas, empeoraría.

**Lo que NO cambia:** ningún hallazgo mueve el orden de magnitud de la conclusión de 03 y 04. El DCF del negocio reportado da decenas de dólares por acción frente a un precio de 372 $. Los defectos son de trazabilidad, de etiquetado y de coherencia del método, no de la conclusión central.

**Calificación realista:** B−. Es un primer ciclo sólido en datos y reproducibilidad, con una ronda de correcciones pendiente en 01, 03 y 04.

---

## 1. Re-ejecución de scripts

| Script | Resultado | Comparación con el documento |
|---|---|---|
| `fase2_ratios.py` | rc=0; 81 filas; 55 controles | `ratios.csv` y `checks.csv` **idénticos**. Controles: 50 OK + 5 DISCREPANCIA, como dice 02 §1.3. Las 5 discrepancias son las que se documentan en 02 §8 |
| `fase3_dcf.py` | rc=0 | Coinciden WACC (11,60 % / 9,79 %), VPA (10,4 / 24,5 / 54,9 $), EV y valor de las acciones por escenario, FCFF por año, las dos tablas de sensibilidad, el DCF inverso (TACC 61,8 / 43,7 / 36,1 / 31,3 / 27,8 / 25,1 %), la brecha (85,3-97,2 %) y los múltiplos (13,9x / 414x / 410x; 35,3 / 27,0 / 11,8 / 407,4 / 30,5 $) |
| `fase4_opcionalidad.py` | rc=0 | Coinciden EBIT necesario (134.680-271.287 M$; central 147.561 M$), flotas (6,1-18,4 M), combinaciones A/B/C (31.600 / 91.650 / 354.200 M$), probabilidades implícitas (42-49 %), rangos de §5, 198 $ (−47 %) y 6,6 % |

**Discordancias entre script y documento: 0.** Las tres fases cumplen lo que dicen sobre su reproducibilidad.

**Observaciones menores de reproducibilidad:**
- `dcf.xlsx` se guarda **sin valores cacheados**: un visor que no recalcula muestra las celdas vacías. En Excel o LibreOffice se recalcula bien.
- Los scripts sobrescriben `data/` al ejecutarse. Por eso esta fase trabajó sobre una copia.
- En `tesla_financials.csv`, la columna `fuente_FY2025` sigue citando **S1 (secundaria)** en ingresos, SBC, etc. Sin embargo, 02 §1.2 dice que FY2025 está "confirmado con fuente primaria". El cuadre es real (11 de 11), pero la etiqueta del CSV no lo refleja.

---

## 2. Verificación de cifras al azar contra la fuente citada

Método: `python3 scripts/fase5_muestreo.py` (semilla 20261024, catálogo de 40 cifras). Cada cifra se contrastó con WebFetch sobre la URL que cita el documento.

### 2.1 Ronda 1

| # | Cifra | Doc | Fuente citada | Valor en la fuente | Resultado |
|---|---|---|---|---|---|
| F38 | Cybercab, capacidad ">125,000" | 01 §5 / 04 §2.2 | P4 | ">125,000" (tabla de capacidad, Cybercab, "Production") | OK |
| F12 | Provisión de garantías 10.138 M$ (8.075 M$) | 01 §4 | P2 | Accrued warranty, end of period: 10,138 (30-sep-26) y 8,075 (30-sep-25) | OK¹ |
| F05 | Créditos 3T26 113 M$ (3T25 417 M$) | 01 §1.2 | P4 | 113 / 417 | OK |
| F20 | Créditos FY2022 1.776 M$ | 02 §2 | 10-K FY2022 | No legible: el texto se corta en el Item 1A y Financial_Report.xlsx está bloqueado. **Contrastado en el R45 del 10-K FY2024** (columna 2022): 1,776 | OK² |
| F02 | Producción FY2025 1.654.667 | 01 §1.1 | P6 | 1,654,667 | OK |
| F13 | Compra de SpaceX 2.002 M$ en 1S26 | 01 §4 | P3 | "Purchase of SpaceX equity investment" 2,002 (6M-2026) | OK¹ |
| F34 | Beta desapalancada Auto & Truck 1,31 | 03 §1 | M6 | 1.31 (corregida por caja; 33 empresas; ene-2026) | OK |
| F04 | Ingresos 3T26 28.046 M$ | 01 §1.2 | P4 | 28,046 | OK |
| F06 | Margen bruto de energía 3T26 33,1 % (BB 954) | 01 §1.2 | P4 | Ingresos 2,881 y coste 1,927 → 954 / 33,1 % (derivado; P4 no publica el %) | OK |
| F11 | Ingresos 9M26 78.669 M$ (9M25 69.926 M$) | 01 §1.2 | P2 | 78,669 / 69,926 | OK |

¹ La cifra es correcta, pero la ubicación citada es imprecisa: F12 no está en la "Note 1" y F13 sale del estado de flujos, no de las "notas". No es un fallo.
² OK con una fuente primaria alternativa. **FY2021** (todas las partidas) **no se pudo verificar en esta fase.** Es un riesgo residual, no un defecto.

**10 de 10 → según la instrucción, se desconfía de la puntuación y se sortean 10 más.**

### 2.2 Ronda 2

| # | Cifra | Doc | Fuente citada | Valor en la fuente | Resultado |
|---|---|---|---|---|---|
| F29 | Opex 3T26 4.776 frente a 3.430; I+D 2.761 frente a 1.630 | 02 §3 | P4 | 4,776 / 3,430; 2,761 / 1,630 | OK |
| F17 | Integradores chinos con el 76 % del mercado BESS | 01 §3 | S9 | "76 %" (Wood Mackenzie, 2025); 8 de los 10 primeros son chinos | OK (cifra) — **ver FAIL-1** |
| F28 | Capex 9M26 13.014 M$ | 02 §4 | P2 | 13,014 | OK |
| F21 | Beneficio operativo FY2023 8.891 M$ | 02 §3 | Deck 4T24 | 8,891 | OK |
| F30 | D&A 3T26 1.852 M$ | 02 §4 / 03 §2.1 | P4 | 1,852 | OK |
| F37 | Acciones en balance a 31-dic-25: 3.751 M | 04 §3.2 | P2 | 3,751 | OK |
| F39 | Ingresos FY2025 94.827 M$ | 01 / 02 | S1 | 94,827 (Tabla 1.1) | OK |
| F35 | Viajes de Uber FY2025: 13.567 M | 04 §2.3 | T5 | 13,567 M | OK |
| F26 | Deuda a 30-sep-26: 9.523 (1.387 + 8.136) | 02 §5 | P2 | 1,387 + 8,136 | OK |
| F32 | Media diluida 3T26 3.541 M / básica 3.240 M | 03 §1 | P2 | 3,541 / 3,240 | OK |

### 2.3 Comprobaciones dirigidas (fuera del sorteo)

Como las 20 cifras pasaron, se buscó el fallo en las **afirmaciones** que acompañan a las cifras y en los datos de mercado.

| # | Afirmación | Doc | Fuente | Lo que dice la fuente | Resultado |
|---|---|---|---|---|---|
| **FAIL-1** | "**1.º** integrador BESS en 2025 según Wood Mackenzie" | 01 §2 | S9 | "Tesla and Sungrow retained the **top two** positions". **No dice quién es el primero** | **FAIL**: la fuente no respalda el "1.º" |
| **FAIL-2** | "Sungrow (**2.º** en el ranking de Wood Mackenzie)" | 01 §3 | S9 | Igual que la anterior: solo "top two" | **FAIL**: no respaldado |
| D-1 | "BYD vendió 2,26 M de VE frente a 1,64 M de Tesla" | 01 §3 | S7 | "2.26 million EVs". La fuente no aclara si incluye híbridos enchufables (BYD los vende) | Aviso: la comparación puede no ser homogénea |
| D-2 | "Aprobado en 9 países de la UE, con >100.000 clientes allí" | 04 §2.2 | P4 | "nine EU countries and used by over 100,000 customers" | OK (lectura razonable) |
| D-3 | Deuda principal de 8.180 M$ | 01 §2 | P1 | "$8.18 billion in aggregate principal amount of indebtedness" | OK (la cifra); el problema es de fechas (ver §3) |
| D-4 | Capex 2026 ">20.000" (S5), ">25.000" (S2), "~20.000" (T1) | 01 / 03 / 04 | S5, S2, T1 | Los tres verificados literalmente | OK; 01 y 03 están desfasados |
| D-5 | Margen de energía ayudado por "tariff refunds and warranty true-downs" | 04 | T1 | Confirmado | OK; 01 no lo matiza |
| D-6 | Precio 372,22 $ (23-oct), bono 4,967 %, ERP 4,20 % / 3,70 % | 03 §1 | M1, M4, M5 | Los tres confirmados | OK |
| D-7 | TSLA EV/Ventas de terceros 15,2 | 03 §7 | TipRanks | 15.21, pero la misma página da **EV 1,23 bill. $ con capitalización de 1,53 bill. $**: una diferencia de 300.000 M$ que no casa con una caja neta de ~36.000 M$ | **Dato de tercero internamente incoherente**, usado sin advertencia |
| D-8 | Toyota EV 418.590 M$ y EV/Ventas 1,45 | 03 / 04 | TipRanks | 418.59B / 1.45 (actualizado el 24-oct-26, no el 23) | OK (la fecha difiere un día) |
| D-9 | Waymo 500.000 viajes/semana; 14 colisiones; ">300 Cybercabs" | 04 | T4, T10, T2 | Confirmado tal como se etiqueta (secundaria / sin atribuir / sin registro primario) | OK, con las etiquetas correctas |
| D-10 | xAI: "confirmó una inversión de 2.000 M$" | 01 §4 | S6 | "Tesla confirmed a $2 billion investment in xAI". P2 **no lo menciona** | OK como secundaria; sigue sin confirmación primaria |

**Resumen del punto 2:** 20 de 20 cifras OK en el valor. **2 FAIL** en afirmaciones (FAIL-1 y FAIL-2, ambas en 01) y 2 avisos de calidad de fuente (D-1 y D-7).

---

## 3. Coherencia entre fases

### 3.1 Misma cifra, distinto valor según el documento

Todas salen de `fase5_consistencia.py` §2. Fase 2 detectó estas diferencias en 02 §8.1, pero **01 nunca se corrigió**, y 01 sigue siendo el documento de referencia del negocio.

| Cifra | 01 | 02 / 03 / 04 | Problema |
|---|---|---|---|
| Caja + inversiones a 30-sep-26 | 45.400 | 45.447 | Redondeo; 01 sin actualizar |
| Deuda | 8.180 (principal a 31-dic-25) **junto a** caja a 30-sep-26 | 9.523 (contable, 30-sep-26) | **Fechas y conceptos mezclados** en la misma celda de 01 §2 |
| SBC 3T26 | 1.170 (S2) | 1.165 (P4) | 01 usa la secundaria aunque hay primaria |
| Capex 9M26 | 13.010 (S2) | 13.014 (P2) | Ídem |
| Beneficio neto 3T26 | 787 "GAAP" | 787 atribuible / 804 total | Etiqueta |
| Capex 2026 (guía) | ">20.000" y ">25.000" | 03: ">20.000-25.000"; 04: "~20.000" (T1, 22-oct) | 01 y 03 desfasados respecto a la call de 3T26 |
| PER de TSLA | ~327x | 02: 390x · 03: 410x · 04: 457x | **Cuatro PER** con precios y denominadores distintos. Ninguno está mal en sí mismo, pero no hay una definición única |
| Margen operativo sin créditos TTM | — | 02 / 03: 2,21 % (sobre ingresos totales) · script de 04: 2,23 % (sobre ingresos sin créditos) | Dos definiciones conviven |
| Marcas "solo secundaria" en FY2025 | Siguen en 01 | 02 D7: confirmadas con primaria | 01 sin actualizar |

### 3.2 Supuestos de Fase 3 frente a los datos de Fase 2

| Supuesto de 03 | Dato de Fase 2 | Valoración |
|---|---|---|
| ROIC terminal del 12 %, "dentro del rango del ROIC A de FY21-24 (13-48 %)" | Mínimo FY21-24 = **13,4 %** | **Afirmación falsa**: el 12 % está *por debajo* del rango. El número no es absurdo, pero la justificación escrita no es cierta. Además, el ROIC TTM es del 5,5 % |
| Margen objetivo base del 8,93 % (media FY21-24 sin créditos) | TTM del 2,21 % (×4,0) | Se puede defender como ancla histórica, pero la etiqueta "base" sugiere una centralidad que los datos de 2023-2026 no apoyan. Falta explicar el mecanismo |
| Anclas de margen | Calculadas como (EBIT − créditos) / ingresos **totales** | El modelo las aplica a ingresos **sin** créditos (`mp × (rev − cred) + cred`). Incoherencia menor, de pocas centésimas de punto |
| Energía +12 % anual (años 1-5) | 9M26: −5,7 %; 3T26: −16 % | 03 cita los datos negativos, pero se apoya en la TACC de 2021-25 (46 %). Es una justificación débil para un caso "base" |
| Reinversión de los años 1-2 del 7,7 % de los ingresos | Capex neto TTM: 15.407 − 7.408 | Coherente con Fase 2. La D&A TTM (3T × 4) es una aproximación declarada; Fase 2 no la recoge en el CSV |
| Ventas/capital de 1,5x | 1,94x (A) / 1,05x (B) | Dentro del rango declarado. OK |
| Caja neta de 35.924 M$; acciones de portada | 02 §5; P2 | OK |

### 3.3 ¿Son válidas las críticas de Fase 4 a 03-valoracion.md?

Se evalúa cada crítica. "¿Corregir 03?" indica si 03 tiene que cambiar por esa crítica.

| Crítica de 04 | ¿Válida? | Evidencia de Fase 5 | ¿Corregir 03? |
|---|---|---|---|
| §4.1.1 Asimetría: el DCF carga los costes de IA, la SBC del plan y el capex de las iniciativas, pero pone sus ingresos a 0 | **Sí, conceptualmente.** La cifra de 6,6 % es aritméticamente correcta (2,6 % + 1.131 / 28.046). Atribuir toda la I+D incremental y toda la SBC extra a la opcionalidad es, en cambio, una inferencia de 04 | Script de 04 §2 reproducido | **Sí**, en el texto. 03 §6 debe reconocer que la "opcionalidad implícita" incluye en parte el valor de un gasto que ya está en el EBIT. No hace falta cambiar el modelo |
| §4.1.2 / W3 El capex de 2026 está sobreestimado, lo que hace el DCF "pesimista" | **No.** El modelo **no usa** la cifra de ">20.000-25.000 M$": usa el 7,7 % de los ingresos. El capex bruto implícito del año 1 del caso base es de ~15.900 M$ (reinversión de 8.475 + D&A de 7.408), **por debajo** de la guía revisada de ~20.000 M$ | `fase5_consistencia.py` §3 (FCFF del año 1 reconstruido: −5.037 frente a −5.039 en 03) | Solo el texto: actualizar la cita de la guía a ~20.000 M$ (T1). **El modelo no es pesimista en capex**; si acaso es ligero, porque la Terafab ("tens of billions" hasta 2028) no está |
| §4.1.3 / W9 Beta mezclada; con la beta sectorial, el WACC sería ~10,5 % | **Parcialmente.** El argumento de coherencia es válido, pero el efecto está exagerado: con WACC del 10,46 %, el VPA base es de ~29 $ (**+4,5 $**), no "+4-10 $" | Interpolación de la tabla 4.1 | Opcional: añadir el escenario de beta sectorial. La conclusión no cambia |
| §4.1.4 / W8 SpaceX está fuera de la caja neta | **Sí.** P2: "presented within Other non-current assets", a valor razonable. Compra de 2.002 + 863 de plusvalía 9M26 (el valor contable exacto no se leyó). Digital assets: 962 M$ | P2 verificado | **Sí:** 03 §6 debe pasar de "no verificado" a "fuera de la caja neta, ~0,7-1 $ por acción". xAI sigue SIN VERIFICAR en primaria |
| §4.1.5 El DCF inverso aplica intensidad de capital industrial también al software | **Sí**, como advertencia | — | Sí: añadir la advertencia en 03 §5 |
| §4.2.1 / W6 Un margen del 8,93 % es un supuesto alcista disfrazado de base | **Discutible, pero razonable.** Es la media histórica declarada, no un número inventado. La crítica sobre el mecanismo es válida | §3.2 de este documento | Sí: justificar el mecanismo o renombrar el escenario |
| §4.2.2 ROIC del 12 % y ventas/capital de 1,5x por encima de los datos | **Sí**, y además 03 justifica el 12 % con un rango que no lo contiene (§3.2) | `fase5_consistencia.py` §3 | **Sí** (alta prioridad: es una afirmación falsa) |
| §4.2.3 / W7 Energía +12 % incoherente con 2026 | **Sí, parcialmente** | 9M26 −5,7 % | Sí: reforzar la justificación o bajar el supuesto |
| §4.2.4 / W2 La línea de dilución de 301 M cuenta dos veces | **Sin verificar en ambos sentidos.** 713 M (portada − básica) y 301 M (diluida − básica) son conceptos distintos: acciones emitidas excluidas del BPA básico frente al efecto dilutivo por método de tesorería. Si las 301 M proceden de acciones restringidas ya emitidas, hay duplicación; si son opciones o RSU no emitidas, no la hay. Nadie leyó la nota de BPA del 10-Q | P2: 202 M emitidas en 9M26 ("equity incentive awards and acquisitions"); 3.751 → 3.953 | **Sí**, pero no como propone 04. 03 no tiene base para llamar a las 301 M "techo de la dilución del plan del CEO". Los VPA "corregidos" de 04 (11,6 / 27,5 / 61,5 $) **excluyen acciones emitidas legalmente** y tampoco deben presentarse como corrección |
| W1 PER de 410x frente a 457x | **No es un error de 03.** 410x es la convención estándar (BPA diluido) y coincide con GuruFocus (410,4x). 457x es una métrica alternativa | Script de 03 | No. Solo, opcionalmente, armonizar la definición del PER entre documentos (§3.1) |
| W4 D&A 3T × 4 | **Sí** (aproximación declarada; dirección correcta) | — | Baja prioridad: pedir la D&A TTM a Fase 2 |
| W5 "Ingresos de Toyota mal citados" | **No.** 03 §5 ya dice "implícitos en su EV/Ventas". Además, el argumento de 04 es **matemáticamente erróneo**: EV / (EV/Ventas) = Ventas, así que la deuda de la financiera se cancela y no "infla" la cifra | `fase5_consistencia.py` §4 | No |
| W10 03 usa bien las cifras corregidas | Sí | — | — |
| W11 El margen de energía de 3T26 tiene efectos puntuales | **Sí** (T1 verificado) | — | No afecta a 03; **corregir 01 §1.2** |

**Balance:** de 15 críticas, 8 son válidas total o parcialmente y obligan a corregir 03. 3 son inválidas (W3/§4.1.2, W5, W1). 1 está exagerada (W9). 1 está sin verificar en los dos sentidos (W2). **04 tiene que corregir sus críticas inválidas** antes de que 03 actúe sobre ellas.

---

## 4. Cifras sin fuente, fuentes que no respaldan la afirmación y datos que parecen inventados

**Fuentes que no respaldan lo que se afirma:**
1. **01 §2:** "1.º integrador BESS según Wood Mackenzie" (FAIL-1).
2. **01 §3:** "Sungrow 2.º" (FAIL-2).
3. **03 §2.2:** "ROIC terminal dentro del rango 13-48 %" (el 12 % no está dentro).
4. **03 §3:** las 301 M como "techo de la dilución del plan del CEO" (sin fuente que vincule ambas cifras).
5. **04 W5:** el razonamiento de que la deuda de la financiera "infla" los ingresos implícitos de Toyota es erróneo.
6. **04 §4.1.2:** dice que el capex del modelo está sobreestimado, pero el modelo no usa esa cifra.

**Cifras sin fuente primaria o sin fuente** (casi todas ya etiquetadas por las propias fases; se listan para que no se olviden):
- El diferencial de la deuda del 1 % (03; declarado e inmaterial).
- El precio de Optimus de 20.000-30.000 $ y el coste del Cybercab de 30.000 $ (04; etiquetados [SUPUESTO] / SIN VERIFICAR, pero con una sensibilidad alta en la flota de 90.000 M$).
- Los parámetros del robotaxi: millas por vehículo, 0,8-1,0 $ por milla, 5 millas por viaje (04; etiquetados [SUPUESTO]).
- ">300 Cybercabs" (T2, sin atribuir; etiquetado).
- La inversión en xAI de 2.000 M$ (solo S6; etiquetado).
- La media anual de acciones diluidas de FY2025 (02; SIN VERIFICAR).
- Las cifras de FY2021 (02): **no se pudieron re-verificar en esta fase**, porque el 10-K FY2022 se corta antes del Item 8 y `Financial_Report.xlsx` y las páginas R de ese 10-K no son accesibles.

**Calidad de fuentes de terceros:**
- El EV de TSLA en TipRanks (1,23 bill. $) frente a su capitalización (1,53 bill. $) es incoherente: el 15,2x de EV/Ventas de "terceros" en 03 §7 no es fiable.
- La mediana del grupo big tech tiene **n = 2** (Microsoft SIN VERIFICAR). Es la única fila de 03 que "reproduce el precio" (407 $), y con dos comparables no es representativa.
- BYD 2,26 M de "VE" puede incluir híbridos enchufables.

**Nada parece inventado.** Todas las cifras muestreadas existen en su fuente con el valor citado. Los problemas son de interpretación (rankings, rangos y etiquetas), no de fabricación.

---

## 5. Lista priorizada de devoluciones

| Prio. | Fase | Qué corregir | Por qué |
|---|---|---|---|
| **1** | **Fase 4** | Retirar o corregir W3 / §4.1.2 (capex "pesimista"), W5 (Toyota) y W1 (PER), y bajar W9 a "+4,5 $". Reformular W2 y §4.2.4 como **SIN VERIFICAR**: no presentar 11,6 / 27,5 / 61,5 $ como corrección | Son críticas inválidas o exageradas. Si 03 las aplica tal cual, empeora. Tiene que ir antes que la Fase 3 |
| **2** | **Fase 3** | (a) Corregir la justificación del ROIC terminal (12 % < 13,4 %): cambiar el texto o el valor. (b) Quitar la etiqueta "techo de dilución del plan del CEO" de las 301 M hasta tener la nota de BPA. (c) Añadir en §6 la asimetría costes/ingresos de la opcionalidad (04 §4.1.1) y la advertencia sobre la intensidad de capital del software en el DCF inverso. (d) Actualizar §6: SpaceX fuera de la caja neta (P2). (e) Actualizar la guía de capex a ~20.000 M$ (T1) y decir explícitamente que el modelo implica ~15.900 M$ en el año 1, sin Terafab. (f) Justificar el mecanismo del margen base del 8,93 % y el +12 % de energía, o renombrar el escenario. (g) Advertir de la incoherencia del EV de TipRanks para TSLA y de que la mediana big tech tiene n = 2. (h) Usar el mismo denominador al calcular las anclas de margen y al aplicarlas | (a) y (b) son afirmaciones sin respaldo; (c)-(h) son coherencia de método y trazabilidad. Ninguna cambia el orden de magnitud |
| **3** | **Fase 1** | (a) FAIL-1 y FAIL-2: sustituir "1.º" y "Sungrow 2.º" por "Tesla y Sungrow ocupan los dos primeros puestos" (S9) o "2.º según Benchmark" (S8). (b) Propagar las correcciones de 02 §8.1: caja 45.447 y deuda 9.523 **a la misma fecha**; SBC 1.165; capex 9M 13.014; 787 = atribuible. (c) Actualizar la guía de capex 2026 a ~20.000 M$ (T1). (d) Matizar el margen de energía del 33,1 % (devoluciones arancelarias y ajustes de garantía, T1). (e) Retirar las marcas "solo secundaria" que 02 D7 confirmó. (f) Marcar como desfasado el PER de ~327x. (g) Aclarar si las 2,26 M de BYD incluyen híbridos enchufables | 01 es el documento que más se cita y es el único con FAIL de fuente |
| **4** | **Fase 2** | (a) Leer la nota de BPA y patrimonio del 10-Q 3T26 para descomponer las 301 M (diluida − básica) y las 713 M (portada − básica). (b) Añadir la D&A TTM al CSV para que 03 no use 3T × 4. (c) Cambiar la etiqueta `fuente_FY2025` del CSV a "construido 9M 10-Q + 4T P4 (S1 como contraste)". (d) Si es posible, re-verificar FY2021 con una fuente primaria accesible | (a) desbloquea la disputa W2 entre 03 y 04; (b) y (c) son trazabilidad; (d) es riesgo residual |

**Criterio para pasar a APTO en la siguiente revisión:**
- 0 FAIL de fuente.
- 0 cifras desfasadas en 01 frente a 02.
- La justificación del ROIC de 03 es cierta.
- La línea de dilución de 03 está respaldada por la nota de BPA, o se ha retirado.
- 04 sin críticas matemáticamente erróneas.
- Re-ejecución de `fase5_consistencia.py` sin MISMATCH.
- Un nuevo muestreo de 20 cifras con otra semilla.

---

*Reproducibilidad:* `python3 scripts/fase5_muestreo.py [semilla]` y `python3 scripts/fase5_consistencia.py`. La verificación contra fuentes se hizo con WebFetch el 24-oct-2026 sobre las URL listadas en `fuentes/fuentes.md`.
