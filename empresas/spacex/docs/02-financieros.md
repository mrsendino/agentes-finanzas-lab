# 02 — Estados financieros de SpaceX (SPCX): FY2023–FY2025, 9M 2026 y TTM a 3T 2026

**Fecha del análisis:** 2026-10-25 · **Versión:** v1 · **Analista:** Fase 2 (rol *Financial Analyst*) · **Alcance:** solo datos históricos. No contiene previsiones, valoraciones ni recomendaciones de compra o venta.

**Archivos de esta fase**

| Archivo | Contenido |
|---|---|
| [`scripts/fase2_datos.py`](../scripts/fase2_datos.py) | Recoge las cifras leídas (literales, con su fuente por celda), calcula la columna TTM y escribe el CSV |
| [`data/spacex_financials.csv`](../data/spacex_financials.csv) | 115 métricas × 16 periodos (FY2021-FY2025, trimestres y acumulados 2025-2026, TTM). Columna `fuente_<periodo>` en cada celda: documento, sección o tabla, página y URL |
| [`scripts/fase2_ratios.py`](../scripts/fase2_ratios.py) | Ratios, controles de cuadre y análisis de Customer B y del capex de Space |
| [`data/ratios.csv`](../data/ratios.csv) | 518 ratios con su fórmula |
| [`data/checks.csv`](../data/checks.csv) | 450 controles de cuadre: 450 OK |
| [`fuentes/nuevas_fase2_v1.md`](../fuentes/nuevas_fase2_v1.md) | Secciones y páginas nuevas leídas en esta fase |

**Cómo se citan las fuentes.** Los IDs son los de [`fuentes.md`](../fuentes/fuentes.md):
- **P2**: folleto 424B4.
- **P3**: 10-Q del 3T 2026.
- **P5**: 8-K de resultados del 3T 2026.
- **P6**: 10-Q del 2T 2026.

La página es el folio impreso (ver la nota de criterio en `nuevas_fase2_v1.md`). Cuando una cifra de una tabla viene de varias fuentes, la fuente exacta de cada celda está en el CSV. Todas las cifras calculadas (márgenes, variaciones, TTM, implícitos) se copian de la salida de `fase2_ratios.py`. No se ha hecho ningún cálculo a mano.

**Etiquetas:** "Histórico" = dato publicado; "Cálculo" = aritmética del script sobre datos publicados; "Supuesto" = escenario propio, no es un dato; **SIN VERIFICAR** = no se pudo contrastar.

---

## 0. Resumen ejecutivo

1. **Ingresos.** Los ingresos se casi duplican: 18.674 M$ en FY2025 (+33,2 %) y 32.043 M$ en el TTM a 3T 2026. Los 9M 2026 suben un +97,5 %.
   - El salto es casi todo SI. Customer B (un único cliente de cloud) explica el 55,9 % del aumento interanual de ingresos del 3T26, si en el 3T25 no facturaba nada.
   - Sin Customer B, los ingresos del 3T26 habrían crecido un +71,2 %, frente al +161,4 % publicado.
2. **Rentabilidad: depende de cómo se mida.**
   - El EBITDA ajustado TTM es de 14.945 M$ (46,6 % de margen).
   - El resultado operativo TTM es de −668 M$ (−2,1 %) y el resultado neto TTM de −2.760 M$.
   - La diferencia (15.613 M$ TTM) son casi solo D&A y compensación en acciones (SBC). La SBC ya pesa el 14,8 % de los ingresos TTM.
3. **Flujo de caja libre muy negativo.**
   - Capex TTM: 54.960 M$, el 171,5 % de los ingresos, con un 81,2 % en SI.
   - FCF TTM = −39.198 M$ (FCO 15.762 M$ − capex 54.960 M$).
   - El negocio "heredado" de SpaceX (Space + Connectivity) está casi en equilibrio de caja operativa: EBITDA ajustado − capex de −436 M$ TTM. Connectivity genera +4.759 M$ y Space consume −5.195 M$.
4. **Balance.** Caja neta de 51.011 M$ a 30-sep-2026: 89.855 M$ de caja y valores negociables frente a 38.844 M$ de deuda contable.
   - Viene de la OPV (85.675 M$ netos) y de la emisión de bonos.
   - El 33,2 % de la deuda es con una parte vinculada (Valor Equity Partners).
5. **Dilución.** Las acciones en circulación subieron un +23,0 % en un año: de 11.042 M (como convertidas, a 30-sep-2025) a 13.579 M.
   - Aportan la OPV, Cursor y la emisión de las acciones B restringidas de Musk (1.000 M + 302,1 M según P2, F-60) (este último punto es una inferencia, §7).
   - Opciones y RSU vivas: un 4,8 % adicional.

---

## 1. Fuentes, perímetro y método

### 1.1 Periodos disponibles

| Periodo | Fuente primaria | Notas |
|---|---|---|
| FY2021, FY2022 | — | **SIN VERIFICAR / vacío.** P2 solo incluye FY2023-FY2025 auditados (índice F-1), y SpaceX no informaba a la SEC antes de la OPV. No se rellena de memoria |
| FY2023-FY2025 | P2 (estados auditados, p. F-4 a F-60) | **Reexpresados**: incluyen xAI y X como si siempre hubieran formado parte del grupo (§1.2). Balance solo a 31-dic-2024 y 31-dic-2025; de 31-dic-2023 solo la caja (F-12) |
| 1T 2025, 1T 2026 | P2 (estados no auditados, p. F-63 a F-95; Summary p. 22-24; no GAAP p. 119-120) | No existe 10-Q del 1T26 (era anterior a la OPV) |
| 2T y 6M 2025-2026 | P6 | — |
| 3T y 9M 2025-2026; balance 30-sep-2026 | P3 | Contrastado con P5 p. 4: coincide |
| TTM a 3T 2026 | Cálculo (`fase2_datos.py`): flujos = FY2025 + 9M26 − 9M25; saldos = 30-sep-2026 | Comprobado de nuevo en `fase2_ratios.py` (controles "TTM …") |

### 1.2 El problema de la fusión con xAI para comparar periodos

- **Qué pasó.** SpaceX adquirió xAI (que ya contenía X/Twitter) el 2-feb-2026, por canje de acciones. Contablemente es una **reorganización entre entidades bajo control común**: Musk controlaba las tres sociedades.
- **Cómo se presenta.** Los estados se presentan como si el grupo siempre hubiera estado combinado, con los valores contables históricos y sin nuevo fondo de comercio (P2, Note 1, p. F-10).
- **Qué implica para el análisis:**
  - **No hay historia separada de la "SpaceX" anterior.** P2 lo dice expresamente: "separate financial statements of xAI and X are not provided" (Note 1, p. F-11). Los crecimientos publicados comparan el grupo combinado consigo mismo. No mezclan perímetros, pero tampoco permiten ver la SpaceX que existía antes.
  - **La mejor aproximación son los segmentos.** No hay partida corporativa: la suma de los tres segmentos es el total consolidado en todos los periodos (controles OK). Así, "SpaceX heredada" ≈ Space + Connectivity y "xAI + X" ≈ segmento AI/SI. Es una aproximación (**inferencia**): las operaciones entre las sociedades antes de la fusión se eliminaron en la consolidación (P2, F-10), y su efecto por segmento no se publica.
  - **Cursor (14-ago-2026) no es control común.** Es una adquisición normal: solo aporta desde el cierre, con 608 M$ de ingresos en el 3T26 (P3, MD&A p. 48). Es crecimiento **inorgánico** dentro de SI.
  - **La definición del EBITDA ajustado cambió en el 3T26.** Desde entonces excluye también la SBC ligada a adquisiciones (1.217 M$) y los costes de adquisición (8 M$) (P3, p. 50). En periodos anteriores esas partidas valen 0, así que la serie sigue siendo comparable en la práctica.
  - **Nombres de segmento.** "AI" en P2 y P6 pasa a llamarse "SI" en P3.

| Cálculo (`fase2_ratios.py` §10) | FY2023 | FY2024 | FY2025 | 9M2026 | TTM 3T26 |
|---|---|---|---|---|---|
| Heredada (Space + Connectivity): ingresos | 7.426 | 11.395 | 15.473 | 16.144 | 20.181 |
| Heredada: margen operativo | 6,3 % | 17,8 % | 24,3 % | 24,8 % | 23,8 % |
| Heredada: EBITDA aj. − capex | −1.353 | −527 | −189 | −90 | −436 |
| AI/SI: ingresos | 2.961 | 2.620 | 3.201 | 10.939 | 11.862 |
| AI/SI: resultado operativo | −3.973 | −1.561 | −6.355 | −3.295 | −5.468 |
| AI/SI: EBITDA aj. − capex | 759 | −5.286 | −13.964 | −34.505 | −39.579 |

Crecimiento de la parte heredada:
- FY2024/FY2023: +53,4 %.
- FY2025/FY2024: +35,8 %.
- 9M26/9M25: +41,2 %, frente al +97,5 % del grupo.

---

## 2. Ingresos por segmento (Histórico; crecimientos: Cálculo)

Fuentes: P2 Note 3 (p. F-22) para FY; P2 p. F-71 (1T); P6 p. 13 (2T y 6M); P3 p. 13 (3T y 9M).

| M$ | FY2023 | FY2024 | FY2025 | 9M2025 | 9M2026 | TTM 3T26 | Var. FY25/24 | Var. 9M26/25 | Var. 3T26/3T25 |
|---|---|---|---|---|---|---|---|---|---|
| **Space** | 3.557 | 3.796 | 4.086 | 3.277 | 3.348 | 4.157 | 7,6 % | 2,2 % | 6,1 % |
| · Launch Services | 1.964 | 2.584 | 2.576 | 2.056 | 2.108 | 2.628 | −0,3 % | 2,5 % | 13,0 % |
| · Launch & Development | 1.593 | 1.212 | 1.510 | 1.221 | 1.240 | 1.529 | 24,6 % | 1,6 % | −4,4 % |
| **Connectivity** | 3.869 | 7.599 | 11.387 | 8.159 | 12.796 | 16.024 | 49,8 % | 56,8 % | 69,5 % |
| · Consumer | 2.817 | 4.830 | 7.208 | 5.198 | 7.754 | 9.764 | 49,2 % | 49,2 % | 57,2 % |
| · Enterprise & Government | 1.052 | 2.769 | 4.179 | 2.961 | 5.042 | 6.260 | 50,9 % | 70,3 % | 91,4 % |
| **AI / SI** | 2.961 | 2.620 | 3.201 | 2.278 | 10.939 | 11.862 | 22,2 % | 380,2 % | 829,9 % |
| · Advertising | 2.323 | 1.728 | 1.844 | 1.323 | 1.248 | 1.769 | 6,7 % | −5,7 % | 18,5 % |
| · Solutions & Infrastructure | 638 | 892 | 1.357 | 955 | 9.691 | 10.093 | 52,1 % | 914,8 % | 1.856,0 % |
| **Total** | 10.387 | 14.015 | 18.674 | 13.714 | 27.083 | 32.043 | 33,2 % | 97,5 % | 161,4 % |

- **Crecimiento FY2024/FY2023:** total +34,9 %, Space +6,7 %, Connectivity +96,4 %, AI −11,5 %.
- **Peso de cada segmento en los ingresos:**
  - FY2025: Space 21,9 %, Connectivity 61,0 %, AI 17,1 %.
  - TTM: 13,0 %, 50,0 % y 37,0 %.
  - 3T26: 12,1 %, 36,0 % y 51,9 %.
- **Space en el 1T26:** cayó un −28,4 % interanual (Launch Services −41,7 %). El 9M26 lo compensa en parte (+2,2 %).
- **TTM frente al TTM del año anterior:** SIN DATO, porque no se publica el 9M 2024.
- **4T 2025 implícito** (FY − 9M, cálculo): ingresos 4.960, Space 809, Connectivity 3.228, AI 923.

---

## 3. Cuenta de resultados consolidada

Fuentes:
- P2: cuenta de resultados F-5; no GAAP p. 119.
- P3: p. 5 y p. 50.
- P6: p. 5.

Márgenes: cálculo.

| M$ | FY2023 | FY2024 | FY2025 | 9M2025 | 9M2026 | TTM 3T26 | 3T2025 | 3T2026 |
|---|---|---|---|---|---|---|---|---|
| Ingresos | 10.387 | 14.015 | 18.674 | 13.714 | 27.083 | 32.043 | 5.576 | 14.575 |
| Margen bruto | 41,2 % | 42,9 % | 49,4 % | 49,3 % | 58,1 % | 56,7 % | 51,5 % | 62,4 % |
| I+D / ingresos | 20,3 % | 24,7 % | 46,3 % | 42,3 % | 43,0 % | 45,2 % | 41,1 % | 31,5 % |
| Resultado operativo | −3.505 | 466 | −2.589 | −1.216 | 705 | −668 | −273 | 2.791 |
| Margen operativo | −33,7 % | 3,3 % | −13,9 % | −8,9 % | 2,6 % | −2,1 % | −4,9 % | 19,1 % |
| Resultado neto | −4.628 | 791 | −4.937 | −2.590 | −413 | −2.760 | −1.054 | 4.404 |
| Margen neto | −44,6 % | 5,6 % | −26,4 % | −18,9 % | −1,5 % | −8,6 % | −18,9 % | 30,2 % |
| EBITDA ajustado (no GAAP) | 3.821 | 5.350 | 6.584 | 5.113 | 13.474 | 14.945 | 2.169 | 8.809 |
| Margen EBITDA aj. | 36,8 % | 38,2 % | 35,3 % | 37,3 % | 49,8 % | 46,6 % | 38,9 % | 60,4 % |

Partidas TTM (cálculo):
- Coste de ingresos 13.863; I+D 14.495; SG&A 4.335.
- Resultado operativo −668.
- Gastos financieros 2.541; ingresos financieros 1.548; otros resultados −1.456.
- Beneficio antes de impuestos −3.117; impuestos −357 (beneficio fiscal).
- Resultado neto −2.760.

Lectura:
- **El beneficio neto del 3T26 (4.404 M$) no es representativo del resultado recurrente.** Incluye 1.025 M$ de "otros resultados", de ellos 561 M$ de plusvalía no realizada en The Boring Company, que es parte vinculada (P3, p. 5), y un beneficio fiscal de 390 M$.
- **En sentido contrario, el 1T26 llevó −1.876 M$ de "otros resultados".** Incluyen 1.526 M$ de pérdida por cancelación de deuda (P2, p. F-67).
- **FY2023 incluye 3.775 M$ de deterioro** de la marca Twitter (P2, F-58).
- **El resultado neto atribuible a los accionistas comunes de 9M26 es −1.084 M$.** Incluye un dividendo implícito de 671 M$ por recompra de preferentes (P3, Note 13, p. 27).

### 3.1 Conciliación del EBITDA ajustado

Fuentes de los datos: P2 p. 119, P3 p. 50. La aritmética de la conciliación la rehace el script y cuadra en todos los periodos.

| M$ | FY2023 | FY2024 | FY2025 | 9M2025 | 9M2026 | TTM 3T26 |
|---|---|---|---|---|---|---|
| Resultado neto | −4.628 | 791 | −4.937 | −2.590 | −413 | −2.760 |
| + D&A | 2.635 | 3.824 | 6.701 | 4.784 | 8.934 | 10.851 |
| + SBC ordinaria | 679 | 784 | 1.947 | 1.044 | 2.616 | 3.519 |
| + SBC de adquisiciones | 0 | 0 | 0 | 0 | 1.217 | 1.217 |
| + Costes de adquisición | 0 | 0 | 0 | 0 | 8 | 8 |
| + Reestructuración | 237 | 213 | 487 | 472 | −6 | 9 |
| + Deterioros | 3.775 | 63 | 38 | 29 | 0 | 9 |
| + Gastos financieros | 1.693 | 1.580 | 1.945 | 1.372 | 1.968 | 2.541 |
| − Ingresos financieros | 249 | 371 | 492 | 370 | 1.426 | 1.548 |
| − Otros resultados (ingreso +) | −42 | 985 | −177 | 342 | −937 | −1.456 |
| + Impuestos | −363 | −549 | 718 | 714 | −361 | −357 |
| **= EBITDA ajustado** | **3.821** | **5.350** | **6.584** | **5.113** | **13.474** | **14.945** |
| EBITDA aj. − resultado operativo | 7.326 | 4.884 | 9.173 | 6.329 | 12.769 | 15.613 |
| Peso de la SBC en esa diferencia | 9,3 % | 16,1 % | 21,2 % | 16,5 % | 30,0 % | 30,3 % |

**Lectura.** La SBC es un coste económico real que se paga en acciones (§7). En el 3T26 supone el 39,3 % de la distancia entre el EBITDA ajustado y el resultado operativo. Medir la rentabilidad por EBITDA ajustado deja fuera una parte creciente de los costes.

---

## 4. Rentabilidad por segmento (Histórico; márgenes: Cálculo)

Fuentes:
- P2 Note 19 (F-57/F-58); P2 F-94 (1T26).
- P6 Note 18 (p. 30-31).
- P3 Note 18 (p. 32-34).
- EBITDA ajustado por segmento: P2 p. 120-121, P6 p. 46-47, P3 p. 51-52.

El CODM evalúa los segmentos por su resultado operativo y **no usa activos ni pasivos por segmento** (P3, Note 18). Por eso no se puede calcular el ROIC por segmento. Se usa "EBITDA ajustado − capex" como aproximación a la caja que genera cada segmento antes de impuestos y circulante.

| Segmento | Periodo | Ingresos | Margen bruto | Resultado op. (margen) | EBITDA aj. (margen) | I+D / ingresos | Capex (/ ingresos) | EBITDA aj. − capex |
|---|---|---|---|---|---|---|---|---|
| Space | FY2023 | 3.557 | 53,1 % | −1 (−0,0 %) | 997 (28,0 %) | 43,2 % | 1.497 (42,1 %) | −500 |
| Space | FY2024 | 3.796 | 59,4 % | 21 (0,6 %) | 1.154 (30,4 %) | 48,3 % | 2.032 (53,5 %) | −878 |
| Space | FY2025 | 4.086 | 66,9 % | −657 (−16,1 %) | 653 (16,0 %) | 73,5 % | 3.832 (93,8 %) | −3.179 |
| Space | 9M2026 | 3.348 | 68,8 % | −1.211 (−36,2 %) | −199 (−5,9 %) | 96,5 % | 3.832 (114,5 %) | −4.031 |
| Space | TTM | 4.157 | 68,9 % | −1.687 (−40,6 %) | −349 (−8,4 %) | 100,2 % | 4.846 (116,6 %) | −5.195 |
| Connectivity | FY2023 | 3.869 | 28,0 % | 469 (12,1 %) | 1.602 (41,4 %) | 9,8 % | 2.455 (63,5 %) | −853 |
| Connectivity | FY2024 | 7.599 | 37,3 % | 2.006 (26,4 %) | 3.849 (50,7 %) | 6,0 % | 3.498 (46,0 %) | 351 |
| Connectivity | FY2025 | 11.387 | 48,0 % | 4.423 (38,8 %) | 7.168 (62,9 %) | 5,0 % | 4.178 (36,7 %) | 2.990 |
| Connectivity | 9M2026 | 12.796 | 52,5 % | 5.211 (40,7 %) | 8.183 (63,9 %) | 5,4 % | 4.242 (33,2 %) | 3.941 |
| Connectivity | TTM | 16.024 | 51,8 % | 6.487 (40,5 %) | 10.228 (63,8 %) | 5,3 % | 5.469 (34,1 %) | 4.759 |
| AI/SI | FY2023 | 2.961 | 44,1 % | −3.973 (−134,2 %) | 1.222 (41,3 %) | 6,3 % | 463 (15,6 %) | 759 |
| AI/SI | FY2024 | 2.620 | 35,6 % | −1.561 (−59,6 %) | 347 (13,2 %) | 44,9 % | 5.633 (215,0 %) | −5.286 |
| AI/SI | FY2025 | 3.201 | 32,0 % | −6.355 (−198,5 %) | −1.237 (−38,6 %) | 158,2 % | 12.727 (397,6 %) | −13.964 |
| AI/SI | 9M2026 | 10.939 | 61,3 % | −3.295 (−30,1 %) | 5.490 (50,2 %) | 70,8 % | 39.995 (365,6 %) | −34.505 |
| AI/SI | TTM | 11.862 | 59,2 % | −5.468 (−46,1 %) | 5.066 (42,7 %) | 79,9 % | 44.645 (376,4 %) | −39.579 |

Trimestres 2026 (cálculo, misma fuente):

| Segmento | Ingresos 1T / 2T / 3T | Margen operativo 1T / 2T / 3T | Margen EBITDA aj. 1T / 2T / 3T |
|---|---|---|---|
| Space | 619 / 962 / 1.767 | −106,9 % / −56,3 % / −0,4 % | −56,7 % / −21,3 % / 20,2 % |
| Connectivity | 3.257 / 4.291 / 5.248 | 36,5 % / 38,6 % / 45,1 % | 64,1 % / 60,5 % / 66,7 % |
| SI | 818 / 2.561 / 7.560 | −301,8 % / −49,1 % / 5,7 % | −74,4 % / 44,7 % / 65,5 % |

Lectura:
- **Connectivity** es el único segmento que genera caja después de su capex. Su margen operativo pasó del 12,1 % (FY2023) al 40,5 % (TTM).
- **Space** gasta en I+D lo mismo que ingresa: 100,2 % de los ingresos TTM. La empresa atribuye 3.004 M$ de la I+D de FY2025 a Starship (P2, p. 3). Space pasó de resultado operativo nulo en FY2023-FY2024 a −1.687 M$ TTM.
- **SI** tiene margen operativo positivo por primera vez en el 3T26 (5,7 %), con 1.217 M$ de SBC de Cursor en ese trimestre. Su capex TTM (44.645 M$) equivale al 376,4 % de sus ingresos.

---

## 5. Flujo de caja, capex y FCF

Fuentes:
- P2: estado de flujos F-8/F-9 y 1T26 F-67/F-68.
- P6: flujos 6M, p. 9.
- P3: flujos 9M, p. 9.

FCF = flujo de caja operativo (FCO) − compras de inmovilizado material (capex) (cálculo). El capex del estado de flujos coincide con la suma del capex por segmento en todos los periodos (controles OK).

| M$ | FY2023 | FY2024 | FY2025 | 9M2025 | 9M2026 | TTM 3T26 |
|---|---|---|---|---|---|---|
| FCO | 4.520 | 5.776 | 6.785 | 4.120 | 13.097 | 15.762 |
| Capex | 4.415 | 11.163 | 20.737 | 13.846 | 48.069 | 54.960 |
| **FCF** | **105** | **−5.387** | **−13.952** | **−9.726** | **−34.972** | **−39.198** |
| Margen FCF | 1,0 % | −38,4 % | −74,7 % | −70,9 % | −129,1 % | −122,3 % |
| FCF − SBC | −574 | −6.171 | −15.899 | −10.770 | −38.805 | −43.934 |
| Capex / ingresos | 42,5 % | 79,7 % | 111,0 % | 101,0 % | 177,5 % | 171,5 % |
| Capex / D&A | 1,7x | 2,9x | 3,1x | 2,9x | 5,4x | 5,1x |
| FCO / EBITDA aj. | 118,3 % | 108,0 % | 103,1 % | 80,6 % | 97,2 % | 105,5 % |

**FCF trimestral** (cálculo; los trimestres no publicados se obtienen por diferencia de acumulados):

| | 1T25 | 2T25 | 3T25 | 4T25 | 1T26 | 2T26 | 3T26 |
|---|---|---|---|---|---|---|---|
| FCO | 727 | −376 | 3.769 | 2.665 | 1.047 | 2.419 | 9.631 |
| Capex | 4.140 | 2.825 | 6.881 | 6.891 | 10.107 | 18.369 | 19.593 |
| FCF | −3.413 | −3.201 | −3.112 | −4.226 | −9.060 | −15.950 | −9.962 |

(El capex del 3T25 calculado como 9M − 6M da 6.881. La suma de segmentos publicada da 6.880; la diferencia es de redondeo.)

**Capex por segmento:**
- 9M26: Space 3.832 (8,0 %), Connectivity 4.242 (8,8 %), SI 39.995 (83,2 %).
- TTM: Space 4.846 (8,8 %), Connectivity 5.469 (10,0 %), SI 44.645 (81,2 %).

Crecimiento del capex:

| | Total | Space | Connectivity | AI/SI |
|---|---|---|---|---|
| FY2024/FY2023 | 152,8 % | 35,7 % | 42,5 % | 1.116,6 % |
| FY2025/FY2024 | 85,8 % | 88,6 % | 19,4 % | 125,9 % |
| 9M2026/9M2025 | 247,2 % | 36,0 % | 43,7 % | 395,2 % |

**Matices que empeoran la lectura del FCF:**
- **Capex ampliado de 9M26.** Si se descuentan los intereses capitalizados (20) y el PP&E adquirido con "other financings" (3.921, partida no monetaria), y se suman los reembolsos de producto cobrados (1.372), el FCF de 9M26 sería de −37.541 M$ (cálculo; partidas de P3 p. 9).
- **Capex pendiente de pago.** El PP&E pendiente de pago creció: 505 (dic-23), 2.481 (dic-24), 7.088 (dic-25) y 11.827 (sep-26) (P2 F-9, P3 p. 9). Es capex ya comprometido que todavía no ha salido de caja.
- **El FCO de 9M26 se apoya en anticipos de clientes.** Incluye +4.922 M$ de ingresos diferidos (cobros por adelantado) y −2.882 M$ de aumento de cuentas a cobrar (P3, p. 9).

---

## 6. Caja, deuda y deuda neta

Fuentes:
- Balance: P2 F-4, P3 p. 4.
- Deuda: P2 Note 10 (F-29), P3 Note 9 (p. 17).

Ratios: cálculo. Deuda contable = "debt and finance leases" corriente + no corriente.

| M$ | 31-dic-2024 | 31-dic-2025 | 30-sep-2026 |
|---|---|---|---|
| Caja + valores negociables | 12.185 | 24.747 | 89.855 |
| Deuda contable | 13.793 | 22.896 | 38.844 |
| · Principal de deuda | 12.621 | 22.049 | 38.006 |
| · Arrendamiento financiero | 1.531 | 1.237 | 983 |
| Deuda neta contable (negativo = caja neta) | 1.608 | −1.851 | −51.011 |
| Deuda neta por principal | 1.967 | −1.461 | −50.866 |
| Deuda con parte vinculada (Valor) | 0 (0,0 %) | 4.507 (19,7 %) | 12.897 (33,2 %) |
| Deuda neta / EBITDA aj. (FY o TTM) | 0,30x | −0,28x | −3,41x |
| EBITDA aj. / gastos financieros (FY o TTM) | 3,4x | 3,4x | 5,9x |

- **Composición de la deuda a 30-sep-2026** (P3, Note 9):
  - 25.000 M$ de SpaceX Notes, con vencimientos de 2031 a 2056.
  - 27 M$ de bonos de X.
  - 12.979 M$ de "other financings", que incluyen la financiación de Valor.
  - La empresa indica que no hay vencimientos materiales de principal hasta el 15-jul-2031 (P3, MD&A p. 52).
- **Deuda a 31-dic-2025** (P2, F-29): era sobre todo deuda heredada de X y xAI, con préstamos B-1/B-3 y bonos al 12,5 %. Se refinanció en 2026, con 1.545 M$ de pérdida por cancelación en 9M26 (P3, p. 9).
- **Intereses con Valor** (parte vinculada): 864 M$ en 9M26 y 351 M$ en el 3T26 (P3, p. 5).
- **Balance a 31-dic-2023:** solo se conoce la caja (4.620 M$, P2 F-12). Los valores negociables y la deuda a esa fecha quedan **SIN VERIFICAR** (P2 no incluye ese balance).

---

## 7. Acciones, compensación en acciones y dilución

Fuentes:
- P3: Note 12 (p. 25-26), Note 13 (p. 27), patrimonio (p. 7-8) y portada.
- P2: F-4 y F-7.

Acciones en millones.

| Fecha | Clase A | Clase B (10 votos) | Clase C | Total ordinarias | Preferentes convertibles |
|---|---|---|---|---|---|
| 31-dic-2024 | 1.832 | 768 | 423 | 3.023 | 1.748 |
| 30-sep-2025 | 1.887 | 694 | 460 | 3.041 | 1.893 |
| 31-dic-2025 | 1.952 | 643 | 484 | 3.079 | 2.046 |
| 30-sep-2026 | 8.240 | 5.339 | 0 | 13.579 | 0 |
| 15-oct-2026 (portada P3) | 8.246,54 | 5.334,52 | — | 13.581,06 | — |

**Movimiento en 9M26** (P3 p. 7; el script comprueba que cuadra hasta las 13.579 M):
- Conversiones de preferentes: 8.152 M.
- Emisiones netas de recompras: 2.348 M, de ellas OPV 639, "common stock issued, net" 1.381, combinaciones de negocio (Cursor y Mesh) 394 y recompras −66.

**Dilución** (cálculo):
- **Interanual.** Las acciones pasaron de 11.042 M (base "como convertidas" a 30-sep-2025: 3.041 ordinarias + 1.241 de preferentes de xAI + 6.760 de preferentes de SpaceX) a 13.579 M a 30-sep-2026: **+23,0 %**.
- **Emisiones netas de 9M26: 21,3 %** de esa base.
  - Unos 1.302 M serían las acciones B restringidas de Musk. Es una **inferencia**: la Note 12 asigna 1.306 M de "issued, net" a la Clase B, y el paquete de Musk es de 1.000 M + 302,1 M de acciones B (P2, Note 21, F-60; el script usa 1.302,07 M, cifra exacta de P2 citada en la fase 1).
  - Sin ellas, las emisiones netas serían del **9,5 %**. Esas acciones ya votan, pero no consolidan sin hitos de capitalización y no financieros (P2, F-60).
- **Dilución potencial pendiente.** 650 M de opciones (A 158, B 350) y RSU (142), un 4,8 % de las acciones en circulación. Además hay 1.333 M de premios con condiciones de rendimiento no cumplidas (P3, Note 13) y ≈261,8 M de acciones A pendientes para EchoStar (dato de la fase 1, P3 MD&A).
- **Media ponderada básica del 3T26:** 11.942 M (diluida 12.475 M), frente a 2.941 M en el 3T25. No es comparable, porque en 2025 las preferentes no estaban convertidas. Para FY2025, la cifra pro forma con la conversión de preferentes es de 9.649 M (P2, p. 23).

| SBC (M$) | FY2023 | FY2024 | FY2025 | 9M2025 | 9M2026 | TTM 3T26 |
|---|---|---|---|---|---|---|
| Ordinaria + de adquisiciones | 679 | 784 | 1.947 | 1.044 | 3.833 | 4.736 |
| % de ingresos | 6,5 % | 5,6 % | 10,4 % | 7,6 % | 14,2 % | 14,8 % |
| % del FCO | 15,0 % | 13,6 % | 28,7 % | 25,3 % | 29,3 % | 30,0 % |

Además se capitalizó SBC en el inmovilizado: 154 M$ en FY2025 y 160 M$ en 9M26 (P2 F-9, P3 p. 9). Los premios de Cursor pendientes de devengar suman 23.376 M$ (fase 1, P3 Note 20): son SBC futura ya comprometida.

---

## 8. Punto de la fase 1 (a): el capex de Space de 9M26 es igual al de FY2025

**Comprobado: la cifra es correcta y la coincidencia es aritmética, no un error de copia.**

| Space, capex (M$) | 1T | 2T | 3T | 4T | Acumulado |
|---|---|---|---|---|---|
| 2025 | 759 (P2 p. 23) | 946 (P6 p. 31) | 1.113 (P3 p. 33) | 1.014 (implícito: FY − 9M) | FY2025 = 3.832 (P2 F-57) |
| 2026 | 1.052 (P2 F-94) | 1.174 (P6 p. 30) | 1.606 (P3 p. 32) | — | 9M2026 = 3.832 (P3 p. 33; P5 p. 4) |

- **Las series trimestrales son distintas y suman lo publicado.** La suma 1T+2T+3T de 2026 da 3.832, que también publica P5. El 9M25 publicado (2.818) más el 4T25 implícito dan el FY2025 de 3.832.
- **Por tanto, los nueve meses de 2026 igualan por casualidad los doce meses de 2025.**
- **La comparación correcta es a igual periodo:** capex de Space 9M26/9M25 = **+36,0 %**. TTM = 4.846 M$.

---

## 9. Punto de la fase 1 (b): Customer B y el segmento SI

**Datos** (P3 y P6, Note 3):
- Customer B supuso el 19,5 % de los ingresos del 2T26, el 12,2 % de 6M26, el 34,5 % del 3T26 y el 24,2 % de 9M26.
- En todos los periodos anteriores estuvo por debajo del 10 %, y por eso no se revela.
- Solo factura en SI. Su identidad no se publica (la fase 1 infiere que es Anthropic: **SIN VERIFICAR**).

**Importes implícitos** (cálculo; % × ingresos consolidados; los % están redondeados a 0,1 pp, con un margen de ±27 M$):

| | 1T26 (6M − 2T) | 2T26 | 3T26 | 9M26 |
|---|---|---|---|---|
| Customer B (M$) | 2 | 1.524 | 5.028 | 6.554 |
| % de ingresos de SI | — | 59,5 % | 66,5 % | 59,9 % |
| % de SI Solutions & Infrastructure | — | 69,4 % | 71,6 % | 67,6 % |

- **El ingreso empieza en el 2T26.** En el 1T26 es prácticamente cero, lo que encaja con un contrato firmado en mayo de 2026.
- **Ritmo mensual del 3T26:** 1.676 M$/mes, frente a los 1.250 M$/mes del contrato descrito en P2. La diferencia ya la señaló la fase 1; P5 menciona contratos adicionales.

### 9.1 Qué parte del crecimiento depende de Customer B

Customer B estaba por debajo del 10 % de los ingresos en 2025. Por eso se dan dos cotas para su ingreso en el periodo anterior: 0, o el máximo posible.

| Cálculo | 3T26 vs 3T25 | 9M26 vs 9M25 |
|---|---|---|
| Aumento de ingresos de SI | 6.747 | 8.661 |
| Aumento de ingresos consolidados | 8.999 | 13.369 |
| Customer B en el periodo previo (rango) | 0 a 558 | 0 a 1.371 |
| % del aumento de SI explicado por B (B previo = 0 / máximo) | 74,5 % / 66,3 % | 75,7 % / 59,8 % |
| % del aumento consolidado explicado por B (ídem) | 55,9 % / 49,7 % | 49,0 % / 38,8 % |
| Ingresos consolidados sin B: crecimiento (B previo = 0) | 71,2 % (publicado 161,4 %) | 49,7 % (publicado 97,5 %) |
| SI sin B ni Cursor | 1.924 (813 en el 3T25: +136,6 %) | 3.777 (2.278 en 9M25: +65,8 %) |

- **Sin Customer B ni Cursor, SI sigue creciendo.** Lo explican Grok, X Premium, la API y otros clientes de cloud. Pero ese resto es pequeño: 1.924 M$ en el 3T26.
- **La cota inferior del crecimiento del resto de SI** (+136,6 % en el 3T) supone que Customer B no facturaba nada en el 3T25. Si facturaba algo, el crecimiento del resto sería mayor.

### 9.2 Qué parte del margen de SI depende de Customer B

**Histórico y cálculo, del 1T26 al 3T26:**
- Los ingresos de SI suben 6.742 M$. De ellos, 5.026 son de Customer B (74,5 %) y 608 de Cursor.
- El EBITDA ajustado de SI sube 5.562 M$: un **margen incremental del 82,5 %**.
- El resultado operativo sube 2.900 M$ (43,0 %).
- El coste de ingresos sube 2.219 M$: margen bruto incremental del 67,1 %.

SpaceX no publica el coste asociado a cada cliente. La siguiente tabla es un **escenario (Supuesto, no dato)**: qué quedaría del 3T26 si desapareciera el ingreso de Customer B, según el margen que se perdería con él.

| Margen perdido (supuesto) | SI resultado op. | SI EBITDA aj. | Grupo resultado op. | Grupo EBITDA aj. | Margen EBITDA aj. del grupo |
|---|---|---|---|---|---|
| 100 % | −4.597 | −75 | −2.237 | 3.781 | 39,6 % |
| 82,5 % (incremental observado) | −3.717 | 805 | −1.357 | 4.661 | 48,8 % |
| 75 % | −3.340 | 1.182 | −980 | 5.038 | 52,8 % |
| 50 % | −2.083 | 2.439 | 277 | 6.295 | 65,9 % |
| *Publicado 3T26* | *431* | *4.953* | *2.791* | *8.809* | *60,4 %* |

Lectura:
- **El margen operativo positivo de SI en el 3T26 (431 M$) depende de Customer B** en cualquier escenario razonable. Con un margen perdido de solo el 50 %, SI volvería a −2.083 M$.
- **También el resultado operativo positivo del grupo en el 3T26 (2.791 M$) depende de él.** Solo se mantiene positivo si el margen perdido es del 50 % o menos.
- **SI aporta el 56,2 % del EBITDA ajustado del grupo en el 3T26**, frente a −609 M$ en el 1T26.
- **La palanca es muy fuerte por el capex.** La depreciación del capex de SI sigue corriendo aunque el cliente se vaya. Y el contrato descrito en P2 se puede rescindir con 90 días de preaviso tras los tres primeros meses (fase 1, §1.4).
- **Concentración conjunta.** Customer A supuso 2.419 M$ en el 3T26 (implícito) y 3.903 M$ en FY2025. Customer A + B = 51,1 % de los ingresos del 3T26.

---

## 10. Diferencias con la fase 1 y entre fuentes

**Con la fase 1** (no se han editado sus documentos; se comunica al orquestador):
1. **Capex de Space 9M26 = FY2025.** La fase 1 lo dejó abierto (§7, punto 6). **Resuelto:** es una coincidencia aritmética entre acumulados (§8). No hay error en P3 ni en P5.
2. **Referencias de página del 424B4.** La fase 1 cita "Prospectus Summary p. 4", "tabla p. 26-27" y "Note 3 p. F-23" para las cifras por segmento y la desagregación. Con el folio impreso del documento:
   - el resumen por segmento está en la p. 3;
   - la tabla "Summary Historical Consolidated Financial and Operating Data", en las p. 22-24;
   - la desagregación de ingresos, en la p. F-22 (la concentración de clientes sí está en F-23).
   **Las cifras coinciden todas.** Solo cambian las páginas; probablemente la fase 1 usó la numeración del visor.
3. **Sin contradicciones de cifras.** Todas las cifras de la fase 1 contrastadas aquí coinciden con la fase 2:
   - ingresos, resultado operativo y EBITDA ajustado por segmento de FY2025, 3T26 y 9M26;
   - capex por segmento y deuda principal (38.006);
   - peso de Valor (33,2 %) y Customer B 3T26 (5.028 M$; 1.676 M$/mes);
   - SI sin B ni Cursor (1.924) y SBC de 9M26 (2.616 + 1.217).

**Entre fuentes primarias** (diferencias pequeñas, sin efecto en los ratios):
4. **Acciones a 31-dic-2025 por clase:**
   - El balance de P2 (F-4) da A 1.954 / B 644 / C 482, que suman 3.080.
   - La Note 12 de P3 da A 1.952 / B 643 / C 484, con un total de 3.079, igual al estado de patrimonio.
   - A 31-dic-2024, la clase C es 421 en P2 y 423 en P3.
   - Se usan las cifras de la Note 12 de P3 porque cuadran con el movimiento de 9M26. La diferencia es de ≤2 M de acciones.
5. **Redondeos trimestrales de 2025.** Al sumar los trimestres de 2025 publicados en documentos distintos (P2 para el 1T, P6 para el 2T y 6M, P3 para el 3T y 9M) aparecen diferencias de 1-2 M$ en 17 controles. Ejemplos: EBITDA ajustado de Space, 6M + 3T = 805 frente a 803 publicado; ingresos de Consumer, 5.199 frente a 5.198. Se aceptan con una tolerancia de 2 M$ y están listados en la salida del script y en `checks.csv`. En 2026 todas las sumas cuadran exactas.

---

## 11. SIN VERIFICAR y limitaciones

- **FY2021 y FY2022:** no publicados (P2 solo da tres ejercicios auditados). Las columnas están vacías y marcadas en el CSV.
- **Balances:** 31-dic-2023 (salvo la caja) y 30-sep-2025 no publicados. Por eso no hay deuda neta de esas fechas ni crecimiento interanual del balance.
- **TTM del año anterior:** no hay 9M 2024, así que no se puede calcular el crecimiento TTM sobre TTM.
- **Customer B:**
  - su identidad (inferencia de la fase 1: Anthropic);
  - su ingreso antes del 2T26 (solo se sabe que era <10 %);
  - su coste y margen reales: los escenarios del §9.2 son supuestos.
- **Customer A:** identidad no revelada (inferencia de la fase 1: gobierno federal de EE. UU.).
- **Acciones restringidas de Musk:** que las 1.302 M estén dentro de "common stock issued, net" de 9M26 es una inferencia (§7).
- **PP&E financiado con "other financings" en FY2023-FY2025:** P2 no lo muestra, así que el FCF ampliado solo se calcula para 9M26.
- **Activos por segmento:** no se publican, y por eso no hay ROIC por segmento.
- **Historia separada de SpaceX, xAI y X antes de la fusión:** no publicada. La "SpaceX heredada" del §1.2 es una aproximación por segmentos.
- **Trimestres implícitos:** 4T25, 2T25 y 3T25 de flujos, y 2T26 y 3T26 de flujos, se obtienen por diferencia de acumulados. No son cifras publicadas.
