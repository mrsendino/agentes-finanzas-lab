# 02 — Estados financieros de Tesla (TSLA): FY2021–FY2025 y TTM a 3T 2026

**Fecha del análisis:** 2026-10-24 · **Versión:** v3 (2026-10-25, correcciones pedidas en [05-veredicto-v2.md](05-veredicto-v2.md) §8, prioridad 1; ver «Registro de cambios v3» al final. v2: correcciones de [05-veredicto.md](05-veredicto.md) §5) · **Analista:** Fase 2 (rol *Financial Analyst*) · **Alcance:** solo datos históricos. Este documento no contiene previsiones, valoraciones ni recomendaciones.

**Archivos de esta fase:**

| Archivo | Contenido |
|---|---|
| [`data/tesla_financials.csv`](../data/tesla_financials.csv) | Datos brutos. Cada valor lleva su fuente en la columna `fuente_<periodo>` |
| [`scripts/fase2_ratios.py`](../scripts/fase2_ratios.py) | Script que hace todos los cálculos |
| [`data/ratios.csv`](../data/ratios.csv) | Salida con todos los ratios |
| [`data/checks.csv`](../data/checks.csv) | 72 controles de cuadre (55 en v1 + 17 en v2) |
| [`data/tablas_02_redondeo.csv`](../data/tablas_02_redondeo.csv) | (v3) Cada cifra de `ratios.csv` tal como se escribe en este documento: % a 1 decimal y M$ a 0, con redondeo mitad hacia arriba sobre el valor completo |
| [`fuentes/nuevas_fase2_v2.md`](../fuentes/nuevas_fase2_v2.md) | Fuentes nuevas de la v2 |

Todas las cifras de las tablas salen de `ratios.csv`. **v3:** se copian de `tablas_02_redondeo.csv`, que las redondea desde el valor completo y no desde `ratios.csv` ya redondeado, para evitar el doble redondeo. No se ha hecho ningún cálculo a mano.

---

## 0. Resumen ejecutivo: lo esencial

1. **Los ingresos se han estancado y su composición ha cambiado.**
   - Los ingresos crecieron un +51 % en 2022 y un +19 % en 2023, se quedaron planos en 2024 (+0,9 %) y cayeron en 2025 (−2,9 %), hasta 94.827 M$.
   - En los últimos doce meses a 3T 2026 vuelven a subir, hasta 103.570 M$ (los nueve primeros meses de 2026 crecen un +12,5 % sobre los de 2025).
   - Automoción ha pasado del 88 % al 72 % de los ingresos. Energía y Servicios ya suman ~28 %.
2. **La rentabilidad operativa se ha desplomado.**
   - El margen operativo pasó del 16,8 % (2022) al 4,6 % (2025) y al 3,3 % (TTM).
   - Sin créditos regulatorios, que son ingreso de margen casi total, el margen operativo es del **2,5 % en 2025** y del **2,2 % TTM**.
   - En 2025, los créditos equivalieron al **45,8 % del beneficio operativo**.
3. **El flujo de caja libre (FCF) aguanta, pero cada vez se lo come más el capex y la compensación en acciones (SBC).**
   - El FCF de 2025 fue de 6.220 M$, ayudado por un capex excepcionalmente bajo (8.527 M$).
   - En los TTM a 3T 2026, el capex sube a 15.407 M$ y el FCF baja a 3.303 M$.
   - Si se trata la SBC como coste (4.300 M$ TTM), el **FCF − SBC es negativo (−997 M$)**.
4. **El balance es muy sólido.**
   - Caja neta de 35.924 M$ (45.447 M$ de caja e inversiones frente a 9.523 M$ de deuda) a 30-sep-2026.
   - Es la principal fortaleza financiera y la que financia la fase actual de inversión.
5. **El rendimiento sobre el capital se ha erosionado.** El ROIC aproximado (método en §6) bajó del 48 % (2022) al 7,6 % (2025) y al 5,5 % (TTM), neto de caja. Hoy está probablemente por debajo de cualquier coste de capital razonable para TSLA. Esto es una lectura y no un cálculo de WACC, que no se ha hecho.

---

## 1. Fuentes y método

### 1.1 De dónde sale cada dato

| Periodo | Fuente primaria | Notas |
|---|---|---|
| FY2021, FY2022 | [10-K FY2022](https://www.sec.gov/Archives/edgar/data/1318605/000095017023001409/tsla-20221231.htm), acc. 0000950170-23-001409 ([Financial_Report.xlsx](https://www.sec.gov/Archives/edgar/data/1318605/000095017023001409/Financial_Report.xlsx)) | Estados consolidados auditados. **v2: re-verificado** el 25-oct-2026: las 19 partidas de FY2021 (y las de FY2022) del CSV coinciden con el `Financial_Report.xlsx`; contraste adicional redondeado con el [deck Q4 2021](https://www.sec.gov/Archives/edgar/data/1318605/000156459022002476/tsla-ex991_209.htm) |
| FY2023, FY2024 | [8-K Ex. 99.1 "Q4 2024 Update"](https://www.sec.gov/Archives/edgar/data/1318605/000162828025002993/exhibit991.htm), acc. 0001628280-25-002993, columnas anuales | Desglose de automoción (ventas/créditos/leasing) del [10-K FY2024, R45](https://www.sec.gov/Archives/edgar/data/1318605/000162828025003063/R45.htm), acc. 0001628280-25-003063 |
| FY2025, flujos | **Construido**: 9M 2025 del [10-Q 3T 2025](https://www.sec.gov/Archives/edgar/data/1318605/000162828025045968/tsla-20250930.htm) (acc. 0001628280-25-045968) + columna Q4-25 del [deck 3T 2026 (P4)](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm) (acc. 0001628280-26-066738) | Ver §1.2 |
| FY2025, balance | Columna 31-dic-2025 del [10-Q 3T 2026 (P2)](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066775/tsla-20260930.htm), acc. 0001628280-26-066775 | Coincide con P4 |
| 9M 2026 y 30-sep-2026 | 10-Q 3T 2026 (P2) | — |
| TTM a 3T 2026 | Calculado en el script: flujos = FY2025 + 9M26 − 9M25; balance = 30-sep-2026 | Contrastado con la reconciliación TTM de P4 |

### 1.2 Por qué FY2025 se construye y no se lee directamente del 10-K

El texto del [10-K FY2025](https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm) (acc. 0001628280-26-003952) se corta en el Item 1A, a ~124.000 caracteres. Lo mismo ocurre con su [PDF en ir.tesla.com](https://ir.tesla.com/_flysystem/s3/sec/000162828026003952/tsla-20251231-gen.pdf). La API XBRL de `data.sec.gov` y el Ex. 99.1 del 8-K de 28-ene-2026 no estaban en la lista de URLs permitidas.

Por eso se reconstruyó FY2025 como 9M (10-Q) + 4T (deck). Esta reconstrucción **cuadra al dólar** con todas las cifras anuales disponibles: los totales de S1 (que cita el 10-K) y la reconciliación TTM a Q4-25 que publica Tesla en P4. Son 11 de 11 controles OK. En consecuencia:

- **Las cifras FY2025 de 01-negocio.md marcadas como "solo secundaria" quedan confirmadas con fuente primaria** (10-Q + deck 8-K): ingresos por línea, beneficio bruto, beneficio operativo, beneficio neto, FCO, capex, FCF y SBC.
- Siguen sin poder leerse en el 10-K FY2025: la media anual de acciones diluidas, el desglose del margen bruto por línea y la nota geográfica.

### 1.3 Controles de cuadre ([`checks.csv`](../data/checks.csv))

De los 72 controles, **67 están OK** (v1: 50 de 55). Cubren:
- suma de segmentos = ingresos totales;
- ventas + créditos + leasing = automoción;
- FCO − capex = FCF publicado (FY2023, FY2024, FY2025 y TTM);
- suma de los cuatro trimestres de 2024 = FY2024;
- beneficio bruto − gastos operativos = beneficio operativo en 3T 2026;
- (v2) D&A: FY2025 construido y TTM frente a la reconciliación EBITDA de P4, y 9M26 frente a la suma de trimestres;
- (v2) FY2021 frente al deck Q4 2021;
- (v2) descomposición de acciones (§5.1).

Las 5 discrepancias se explican en §8. Comparan el dato primario con S1, S2, S11 y P1 Item 1A. Cuatro de esas referencias son las cifras que citaba 01 v1 (etiqueta "… / 01 v1" en `checks.csv`), y 01 v2 ya adoptó la cifra primaria.

---

## 2. Ingresos y mezcla de negocio

| Métrica (M$) | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | TTM 3T26 |
|---|---:|---:|---:|---:|---:|---:|
| **Ingresos totales** | 53.823 | 81.462 | 96.773 | 97.690 | 94.827 | 103.570 |
| Automoción (incl. créditos y leasing) | 47.232 | 71.462 | 82.419 | 77.070 | 69.526 | 75.003 |
| · Venta de vehículos | 44.125 | 67.210 | 78.509 | 72.480 | 65.821 | 72.323 |
| · Créditos regulatorios | 1.465 | 1.776 | 1.790 | 2.763 | 1.993 | 1.181 |
| · Leasing | 1.642 | 2.476 | 2.120 | 1.827 | 1.712 | 1.499 |
| Energía (generación y almacenamiento) | 2.789 | 3.909 | 6.035 | 10.086 | 12.771 | 12.265 |
| Servicios y otros | 3.802 | 6.091 | 8.319 | 10.534 | 12.530 | 16.302 |

| Crecimiento interanual | FY2022 | FY2023 | FY2024 | FY2025 | 9M26 vs 9M25 |
|---|---:|---:|---:|---:|---:|
| Ingresos totales | 51,4 % | 18,8 % | 0,9 % | −2,9 % | 12,5 % |
| Automoción | 51,3 % | 15,3 % | −6,5 % | −9,8 % | 10,6 % |
| Créditos regulatorios | 21,2 % | 0,8 % | 54,4 % | −27,9 % | −56,0 % |
| Energía | 40,2 % | 54,4 % | 67,1 % | 26,6 % | −5,7 % |
| Servicios y otros | 60,2 % | 36,6 % | 26,6 % | 18,9 % | 41,2 % |

| Peso sobre ingresos | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | TTM 3T26 |
|---|---:|---:|---:|---:|---:|---:|
| Automoción | 87,8 % | 87,7 % | 85,2 % | 78,9 % | 73,3 % | 72,4 % |
| Energía | 5,2 % | 4,8 % | 6,2 % | 10,3 % | 13,5 % | 11,8 % |
| Servicios y otros | 7,1 % | 7,5 % | 8,6 % | 10,8 % | 13,2 % | 15,7 % |
| Créditos regulatorios | 2,7 % | 2,2 % | 1,8 % | 2,8 % | 2,1 % | 1,1 % |

Tasas de crecimiento anual compuesto (CAGR) FY2021→FY2025:
- ingresos totales: 15,2 %;
- automoción: 10,1 %;
- energía: 46,3 %;
- servicios: 34,7 %.

**Qué cambió y por qué:**
- **2021-2022: expansión de volumen.** La automoción creció un +51 % en 2022 y un +15 % en 2023.
- **2023-2025: la automoción retrocede.** Las ventas de vehículos caen de 78.509 M$ a 65.821 M$ (−16 % acumulado). En 3T 2026 Tesla atribuye el estancamiento a un "lower vehicle average selling price (ASP)" y a la "decrease in vehicle deliveries" ([P4](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm)). El repunte de 9M 2026 (+10,6 % en automoción) se concentra en el primer semestre, porque 3T 2026 frente a 3T 2025 ya es −3 % (P4). No se ha leído el desglose de 1S 2025 que explicaría la base de comparación: **SIN VERIFICAR**.
- **Energía multiplica sus ingresos por 4,6 entre 2021 y 2025, pero en 2026 se da la vuelta**: −5,7 % en 9M y −16 % en 3T. Tesla lo explica como "partially due to tariff-related customer refunds" (P4). Ya en febrero de 2026 había anticipado compresión de margen ([S4](https://www.energy-storage.news/tesla-energy-storage-deployments-jumped-in-crucial-ai-transformation-year-company-expects-margin-compression-in-2026/)).
- **Servicios y otros es hoy el motor de crecimiento**: +41 % en 9M 2026. El deck no desglosa qué partidas lo impulsan (posventa, supercarga, seguros, usados, FSD). Ese desglose queda **SIN VERIFICAR**.
- **Los créditos regulatorios alcanzaron su máximo en 2024 (2.763 M$) y se están hundiendo** (1.181 M$ TTM). El 10-K FY2025 lo vincula a la ley OBBBA, que "restricted certain regulatory credit programs" ([P1](https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm), Item 1, ya citado en 01-negocio.md).

---

## 3. Márgenes y beneficios

| Métrica (M$) | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | TTM 3T26 |
|---|---:|---:|---:|---:|---:|---:|
| Beneficio bruto | 13.606 | 20.853 | 17.660 | 17.450 | 17.094 | 19.974 |
| **Margen bruto** | 25,3 % | 25,6 % | 18,2 % | 17,9 % | 18,0 % | 19,3 % |
| Beneficio operativo | 6.523 | 13.656 | 8.891 | 7.076 | 4.355 | 3.466 |
| **Margen operativo** | 12,1 % | 16,8 % | 9,2 % | 7,2 % | 4,6 % | 3,3 % |
| Beneficio operativo sin créditos | 5.058 | 11.880 | 7.101 | 4.313 | 2.362 | 2.285 |
| **Margen operativo sin créditos** | 9,4 % | 14,6 % | 7,3 % | 4,4 % | 2,5 % | 2,2 % |
| **Créditos / beneficio operativo** | 22,5 % | 13,0 % | 20,1 % | 39,0 % | 45,8 % | 34,1 % |
| Beneficio neto atribuible a comunes | 5.519 | 12.556 | 14.997 | 7.091 | 3.794 | 3.218 |
| **Margen neto** | 10,3 % | 15,4 % | 15,5 % | 7,3 % | 4,0 % | 3,1 % |
| Crecimiento del beneficio operativo | — | 109,4 % | −34,9 % | −20,4 % | −38,5 % | 9M: −30,2 % |
| Crecimiento del beneficio neto | — | 127,5 % | 19,4 % | −52,7 % | −46,5 % | 9M: −19,5 % |

**Qué cambió y por qué:**
- **Margen bruto.** Cae de ~25 % a ~18 % en 2023, coincidiendo con la caída del ASP (cualitativo, ver 01-negocio.md §4.3). Desde entonces se estabiliza, y en TTM sube al 19,3 % gracias a Servicios y a un "improved vehicle region and product mix" (P4).
- **Beneficio operativo.** Cae durante tres años seguidos aunque el beneficio bruto se mantiene plano. La causa son los gastos operativos: en 3T 2026 suman 4.776 M$, frente a 3.430 M$ en 3T 2025 (P4). Tesla lo explica así: "increase in operating expenses driven by SI and other R&D projects, SBC (including 2025 CEO Performance Award) and SG&A" (P4). La I+D de 3T 2026 fue de 2.761 M$, frente a 1.630 M$ un año antes (P4).
- **Créditos regulatorios.** Sostienen el beneficio operativo. Asumiendo que su margen es ~100 %, sin ellos el margen operativo de 2025 habría sido del 2,5 %. La ratio créditos / beneficio operativo baja en TTM (34 %) solo porque los créditos caen más deprisa que el beneficio. El negocio subyacente no mejora: el margen sin créditos es del 2,2 %.
- **Beneficio neto de FY2023 (14.997 M$).** Está inflado por un beneficio fiscal no recurrente: la provisión fiscal de FY2023 es de −5.001 M$ y la de 4T 2023 de −5.752 M$ ([deck Q4 2024](https://www.sec.gov/Archives/edgar/data/1318605/000162828025002993/exhibit991.htm)). **No es comparable** y su "crecimiento" del +19 % es engañoso. El beneficio operativo de ese año cayó un −35 %.
- **En 2026 el beneficio neto supera al operativo** (9M: 2.378 frente a 2.057 M$). Lo explica un ingreso por intereses de ~430-450 M$ por trimestre (P4) y una partida "Other income (expense)" muy volátil: −592 M$ (4T 2025), −535 M$ (1T 2026), +590 M$ (2T 2026) y −117 M$ (3T 2026) (P4). La naturaleza de esa partida queda **SIN VERIFICAR** porque la nota del 10-Q no se leyó.

---

## 4. Flujo de caja, capex y compensación en acciones

| Métrica (M$) | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | TTM 3T26 |
|---|---:|---:|---:|---:|---:|---:|
| Flujo de caja operativo (FCO) | 11.497 | 14.724 | 13.256 | 14.923 | 14.747 | 18.710 |
| FCO / ingresos | 21,4 % | 18,1 % | 13,7 % | 15,3 % | 15,6 % | 18,1 % |
| Capex | 6.482 | 7.158 | 8.898 | 11.339 | 8.527 | 15.407 |
| Capex / ingresos | 12,0 % | 8,8 % | 9,2 % | 11,6 % | 9,0 % | 14,9 % |
| Capex / FCO | 56,4 % | 48,6 % | 67,1 % | 76,0 % | 57,8 % | 82,3 % |
| **FCF (FCO − capex)** | 5.015 | 7.566 | 4.358 | 3.584 | 6.220 | 3.303 |
| **Margen FCF** | 9,3 % | 9,3 % | 4,5 % | 3,7 % | 6,6 % | 3,2 % |
| SBC | 2.121 | 1.560 | 1.812 | 1.999 | 2.825 | 4.300 |
| SBC / ingresos | 3,9 % | 1,9 % | 1,9 % | 2,0 % | 3,0 % | 4,2 % |
| **FCF − SBC** | 2.894 | 6.006 | 2.546 | 1.585 | 3.395 | **−997** |
| D&A (amortización, depreciación y deterioro) — v2 | 2.911 | 3.747 | 4.667 | 5.368 | 6.148 | **6.704** |
| D&A / ingresos — v2 | 5,4 % | 4,6 % | 4,8 % | 5,5 % | 6,5 % | 6,5 % |
| Capex − D&A (capex neto) — v2 | 3.571 | 3.411 | 4.231 | 5.971 | 2.379 | 8.703 |
| EBIT + D&A (EBITDA aprox., sin ajustar SBC) — v2 | 9.434 | 17.403 | 13.558 | 12.444 | 10.503 | 10.170 |

Fuentes de la D&A: FY2021-22, 10-K FY2022 (`Financial_Report.xlsx`, estado de flujos); FY2023-25 y TTM, reconciliación EBITDA TTM de [P4](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm) (columnas 4T23, 4T24, 4T25 y 3T26). El script reconstruye FY2025 (9M25 4.505 + 4T25 1.643) y TTM (+ 9M26 5.061 − 9M25 4.505) y cuadran al dólar con P4.

**Nota para Fase 3:** la D&A TTM real es **6.704 M$**, no 7.408 M$ (3T26 × 4). La aproximación sobrestimaba la D&A en 704 M$ (+10,5 %), porque 3T26 (1.852) es el trimestre más alto. Con la cifra real, el capex neto TTM es de **8.703 M$** (8,4 % de los ingresos), no ~8.000 M$.

**Qué cambió y por qué:**
- **El FCO resiste mejor que el beneficio.** En TTM llega a 18.710 M$, máximo de la serie, mientras el beneficio operativo cae. Dos motivos:
  - Las partidas sin salida de caja son grandes y crecientes: la D&A TTM es de 6.704 M$ (1.852 M$ solo en 3T 2026, P4) y la SBC TTM de 4.300 M$ (1.165 M$ en 3T 2026).
  - Influye también el circulante, pero no se ha desglosado (**SIN VERIFICAR**).
- **El capex de 2025 fue anormalmente bajo** (−24,8 % interanual), lo que infla el FCF de 2025 (+73,5 %). En 2026 se dispara: 13.014 M$ en 9M, un +112 % (10-Q 3T 2026), con 5.789 M$ solo en 2T 2026 (P4). Tesla lo atribuye a inversión en "SI, robotics and energy" (P4). Por eso el FCF de 2025 **no es una base representativa** para extrapolar.
- **La SBC se multiplica por más de dos** (+115 %): de 1.999 M$ en FY2024 a 4.300 M$ TTM. Coincide con el plan de retribución del CEO de 2025 (P4, y S10 en 01-negocio.md). Si se trata como coste real, la empresa ya no genera caja libre en TTM (−997 M$). Es el indicador de mayor deterioro de este bloque.

---

## 5. Balance: caja, deuda y acciones

| Métrica (M$, saldo a cierre) | 31-dic-21 | 31-dic-22 | 31-dic-23 | 31-dic-24 | 31-dic-25 | 30-sep-26 |
|---|---:|---:|---:|---:|---:|---:|
| Caja + inversiones a corto plazo | 17.707 | 22.185 | 29.094 | 36.563 | 44.059 | 45.447 |
| Deuda y arrendamientos financieros, corriente | 1.589 | 1.502 | 2.373 | 2.456 | 1.640 | 1.387 |
| Deuda y arrendamientos financieros, no corriente | 5.245 | 1.597 | 2.857 | 5.757 | 6.736 | 8.136 |
| **Deuda total** | 6.834 | 3.099 | 5.230 | 8.213 | 8.376 | 9.523 |
| **Caja neta** | 10.873 | 19.086 | 23.864 | 28.350 | 35.683 | 35.924 |
| Patrimonio neto de los accionistas | 30.189 | 44.704 | 62.634 | 72.913 | 82.137 | 89.289 |
| Acciones diluidas (media del año, M) | 3.386 | 3.475 | 3.485 | 3.498 | **SIN VERIFICAR** | 9M26: 3.539 |

**Lectura:**
- La caja neta se ha más que triplicado desde 2021. En 2026 se ha estancado (+241 M$ en 9 meses), porque el FCF del año se ha ido en capex y en otras partidas de inversión. Una de ellas es la compra de participaciones de SpaceX por 2.002 M$ en el primer semestre (P3, citado en 01-negocio.md).
- **Definición de deuda:** incluye arrendamientos financieros y la deuda sin recurso ligada a vehículos y a energía solar. Con las fuentes leídas **no se puede separar**. Ver §8.
- **Dilución:**
  - 2021–2024: muy moderada, +0,3-0,4 % anual tras 2022, con cifras ajustadas por el split 3x1 de 2022.
  - 2025–2026: las medias diluidas suben a 3.523 M (9M 2025) y 3.539 M (9M 2026). Pero las **acciones en circulación legal** saltan de 3.324 M (30-sep-25) a 3.953 M (30-sep-26), +18,9 %. Las medias no lo reflejan porque esas acciones son restringidas y aún no "ganadas". Detalle en §5.1.

### 5.1 Descomposición de las acciones a 3T 2026 (v2)

Fuentes: portada, nota de BPA y estado de patrimonio de los 10-Q 1T, 2T y 3T 2026 y 3T 2025; Form 4 de Elon Musk (16-jun-2026 y 3-ago-2025). Detalle y calidad de cada una en [`fuentes/nuevas_fase2_v2.md`](../fuentes/nuevas_fase2_v2.md). Cálculo: filas `acc_*` de `ratios.csv` y controles "Acciones: …" de `checks.csv` (9 de 9 OK).

**Datos leídos:**

| Concepto (M acciones) | Valor | Fuente |
|---|---:|---|
| Portada 10-Q 3T26 (15-oct-2026) | 3.952,76 | P2 |
| Saldo en balance 31-dic-25 → 30-sep-26 | 3.751 → 3.953 | P2, estado de patrimonio |
| Emitidas 1T / 2T / 3T 2026 | 4 / 194 / 4 (= 202) | 10-Q 1T26, 2T26, 3T26 |
| Media básica 3T26 | 3.240 | P2, nota de BPA |
| "Add: Stock-based awards" 3T26 | 301 | P2, nota de BPA |
| Media diluida 3T26 | 3.541 | P2, nota de BPA |
| 2025 CEO Performance Award: acciones restringidas | 423,74 | Form 4 (jun-2026): 423.743.904, con acuerdo de voto, vencen 2033/2035 |
| Ejercicio de opciones de 2018 (16-jun-2026): ejercidas − retenidas | 303,96 − 17,53 = **286,43** | Form 4: liquidación neta; acciones con vesting por servicio el 19-ene-2028 |
| Posesión directa de Musk tras el ejercicio | 710,17 = 423,74 + 286,43 (exacto) | Form 4 |
| 2025 CEO Interim Award (3-ago-2025) | 96,0 restringidas | Form 4 ago-2025 |

**Política contable citada por el 10-Q:** "Restricted stock awards will be excluded from the computation of diluted weighted average shares until the shares have been deemed to be earned" (P2). El 10-Q no dice en texto que se excluyan de la básica, pero los números lo demuestran: la media básica solo pasa de 3.234 (1T26) a 3.240 (3T26) pese a las 194 M emitidas en 2T26, y en 3T25 (3.227) tampoco recoge las 100 M emitidas en el trimestre.

**(a) Diferencia diluida − básica: 301 M.** Es la línea "stock-based awards", calculada por el método de tesorería. El 10-Q **no la desglosa**. Lectura (INFERENCIA, coherente con todos los datos):
- ~**286 M** son las acciones netas del ejercicio de 2018. Están emitidas, pero restringidas por servicio hasta ene-2028: fuera de la básica, dentro de la diluida. Antes del ejercicio (jun-2026), ese papel lo jugaban las 303,96 M de opciones de 2018, pero por el método de tesorería no aportaban 304 M a la diluida. Con un precio de ejercicio de 23,34 $ y un precio medio de ~400 $, aportaban **~286,2 M** (283,7-288,2 M con precios de 350-450 $; filas `acc_op2018_tesoreria_px*`). Las 304 M de "awards" de 1T26 serían, por tanto, ~286 M de Musk + **~17,8 M de empleados** (15,8-20,3 M; filas `acc_awards_1T26_resto_empleados_px*`). El precio medio de 1T26 es un supuesto (**SIN VERIFICAR**). La lectura queda reforzada: la parte de Musk son ~286 M antes y después del ejercicio, y la de empleados es de ~15-18 M.
- ~**15 M** son incentivos de empleados (RSU y opciones) aún no emitidos.
- Las **423,7 M del CEO 2025 no están** en la diluida: son por objetivos y no se han "ganado".

**(b) Diferencia portada − básica: 712,8 M.**
- 423,7 M: restringidas del plan del CEO 2025 (emitidas en 4T25: el saldo sube 427 M ese trimestre).
- 286,4 M: acciones netas del ejercicio de 2018 (jun-2026).
- 2,6 M: residuo por desfase entre media y saldo, y emisiones corrientes de empleados.

**(c) Las 202 M emitidas en 9M26:**
- 1T26: 4 M y 3T26: 4 M → emisiones corrientes de empleados.
- 2T26: 194 M ≈ +286,4 M (ejercicio de 2018) − 96,0 M (cancelación del Interim Award 2025) + ~3,6 M de empleados. El APIC de la línea es de solo 322 M$, coherente con una liquidación neta sin caja y no con una adquisición pagada en acciones. La cifra de 96 M sale del Form 4 de ago-2025, que no menciona ninguna cancelación. **La cancelación solo la recoge una fuente secundaria** (Not a Tesla App: "that backup deal was forfeit once the 2018 deal cleared court proceedings"), que además **no da la cifra de 96 M**: habla de un "$29 billion interim award". Que lo cancelado sean exactamente las 96 M es una inferencia del cuadre, no un dato. El resto del cuadre (190,4 frente a 194) es aritmético.

**¿Dónde están las 423,7 M del plan del CEO 2025?** **En la portada, sí** (emitidas legalmente en 4T25, con derecho de voto cedido por proxy). **En la media básica, no. En la diluida, no** (no "ganadas").

**Consecuencia para la disputa W2 (03 frente a 04):**
- 03 calcula el valor por acción sobre la portada (3.952,76 M). Esa cifra **ya incluye** las 423,7 M del CEO 2025 y las 286,4 M de 2018.
- La línea de "dilución adicional" de **03 v1** sumaba las 301 M encima. **Era un doble cómputo real de ~286 M** (el 95 % de la línea). Solo ~15 M son incrementales. *Resuelto en 03 v2* (§3): la línea se sustituye por la cifra totalmente diluida de esta sección.
- Cifra totalmente diluida aproximada: **~3.967 M** (portada + ~15 M). Contraste: diluida 3T26 + restringidas CEO 2025 = 3.541 + 423,7 = 3.964,7 M; la diferencia de ~3 M es el desfase de saldos.
- Las 4.254 M de **03 v1** (portada + 301) sobrestimaban las acciones un 7,2 % frente a la cifra totalmente diluida (fila `acc_portada_mas_301_sobre_fd`). Los VPA "corregidos" de **04 v1**, sobre la media diluida (3.541 M), las subestimaban un 10,7 % (fila `acc_diluida_media_sobre_fd`), porque excluyen las 423,7 M ya emitidas. Las dos líneas están retiradas en 03 v2 y 04 v2.1.
- No se analiza aquí qué cifra debe usar el DCF: es decisión de Fase 3. Desde los datos, **la portada (3.953 M) ya es el techo razonable** para el plan del CEO. La frase de **03 v1** §6.4 ("el modelo solo recoge una parte") quedaba invertida. *Resuelto en 03 v2* (§6.5), que dice que la portada ya recoge entera la dilución del CEO.

---

## 6. Rentabilidad sobre el capital (ROIC aproximado)

**Método declarado.**
- **NOPAT** = beneficio operativo × (1 − 21 %). Se usa el tipo federal normativo de EE. UU. y no el tipo efectivo, porque el de FY2023 está distorsionado por el beneficio fiscal.
- **Capital invertido A** = patrimonio neto + deuda total − caja e inversiones a corto plazo.
- **Capital invertido B** = patrimonio neto + deuda total, sin restar la caja.
- Se usa la media de los saldos inicial y final. FY2021 usa solo el saldo final, y el TTM usa la media entre 30-sep-2025 y 30-sep-2026.
- Es una aproximación: no ajusta arrendamientos operativos, fondo de comercio ni el exceso de caja operativa mínima.

| Métrica | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | TTM 3T26 |
|---|---:|---:|---:|---:|---:|---:|
| NOPAT (M$) | 5.153 | 10.788 | 7.024 | 5.590 | 3.440 | 2.738 |
| Capital invertido A, saldo final (M$) | 19.316 | 25.618 | 38.770 | 44.563 | 46.454 | 53.365 |
| Capital invertido B, saldo final (M$) | 37.023 | 47.803 | 67.864 | 81.126 | 90.513 | 98.812 |
| **ROIC A (neto de caja)** | 26,7 % | 48,0 % | 21,8 % | 13,4 % | 7,6 % | 5,5 % |
| **ROIC B (bruto)** | 13,9 % | 25,4 % | 12,1 % | 7,5 % | 4,0 % | 2,9 % |
| ROE (beneficio neto / patrimonio medio) | 18,3 % | 33,5 % | 27,9 % | 10,5 % | 4,9 % | 3,8 % |

**Lectura.** El capital invertido sigue creciendo (patrimonio +99,7 % entre 31-dic-2022 y 30-sep-2026) mientras el NOPAT se ha dividido entre 3,9 desde su máximo de FY2022. Por cualquiera de las dos definiciones, el ROIC actual (3-6 %) es inferior al que justificaría por sí solo el negocio existente.

**Sensibilidad.**
- Con un tipo impositivo del 15 % o del 25 % en vez del 21 %, el ROIC A del TTM pasaría a 5,9 % o 5,2 % (filas `roic_A_tipo_*` del script). El orden de magnitud no cambia.
- La conclusión sí depende de la definición de capital. El ROIC A trata la caja como "no invertida"; con 45.000 M$ de caja, la diferencia entre A y B es de casi el doble.

---

## 7. Datos del trimestre 3T 2026 (deck P4)

Cuadran entre sí:
- beneficio bruto 5.494 − gastos operativos 4.776 = beneficio operativo 718;
- FCO 6.263 − capex 4.732 = FCF 1.531.

Ratios del trimestre:
- **Margen bruto:** 19,6 %.
- **Margen operativo:** 2,6 %.
- **Variaciones frente a 3T 2025:** ingresos ≈0 %, beneficio operativo −56 %, créditos −73 %, energía −16 %, servicios +33 %.

Todos coinciden con 01-negocio.md (ver los controles en `checks.csv`).

---

## 8. Calidad del dato y discrepancias

### 8.1 Discrepancias frente a 01-negocio.md v1 (Fase 1)

**Estado v3:** D1-D6 son discrepancias con **01 v1** y están **resueltas en 01 v2** (registro de cambios v2 de 01: 1.165, 13.014, caja y deuda a 30-sep-2026 con los 8.180 M$ como nota aparte, 45.447, PER marcado DESFASADO y 787 atribuible / 804 total). D7 también está incorporada en 01 v2. La tabla se conserva como histórico. Los controles de `checks.csv` siguen dando DISCREPANCIA porque comparan el dato primario con la fuente secundaria (S2, S11) o con otro concepto (P1 Item 1A), no con 01 v2.

| # | Dato | 01-negocio.md v1 | Dato primario de Fase 2 | Valoración |
|---|---|---|---|---|
| D1 | SBC 3T 2026 | 1.170 M$ (S2, Electrek) | **1.165 M$** (P4, estado de flujos y reconciliación EBITDA) | Diferencia menor (−5 M$). S2 redondea o usa otra partida. Prevalece P4. **Resuelto en 01 v2** (cifra de 01 v1) |
| D2 | Capex 9M 2026 | 13.010 M$ (S2) | **13.014 M$** (10-Q 3T 2026) | Redondeo de S2. Prevalece el 10-Q. **Resuelto en 01 v2** (cifra de 01 v1) |
| D3 | Deuda a 31-dic-2025 | "8.180 M$ de deuda principal" (P1, Item 1A) | **8.376 M$** de deuda y arrendamientos financieros contables (10-Q 3T 2026 y P4) | No es un error, sino **dos conceptos distintos**: principal nominal frente a valor contable que incluye arrendamientos financieros. Fase 1 los presenta como "deuda" sin matizar. Además, en §2 de 01-negocio.md compara caja a 30-sep-2026 (45.400) con deuda a 31-dic-2025: **fechas mezcladas**. A 30-sep-2026 la deuda contable es de 9.523 M$. **Resuelto en 01 v2** (cifra de 01 v1) |
| D4 | Caja e inversiones 3T 2026 | 45.400 M$ | **45.447 M$** (10-Q: 17.853 de efectivo + 27.594 de inversiones a corto plazo) | Redondeo. Correcto en sustancia. **Resuelto en 01 v2** (cifra de 01 v1) |
| D5 | PER de ~327x (S11) | ~327x | Con el BPA GAAP TTM hasta 2T 2026 (1,08 $, P4) sale 328x. Con el BPA TTM hasta 3T 2026 (0,91 $), **390x** | El ~327x de S11 era previo a los resultados del 3T. Con el último BPA, el PER al mismo precio de 354,72 $ es ~390x. Fase 1 no está mal, pero el dato ya está **desfasado**. **Resuelto en 01 v2** (cifra de 01 v1) |
| D6 | "Beneficio neto GAAP 3T 2026: 787 M$" | 787 | 787 es el atribuible a comunes. El beneficio neto total es de 804 M$ (P4) | Etiqueta imprecisa, no error de cifra. **Resuelto en 01 v2** (cifra de 01 v1) |
| D7 | Cifras FY2025 marcadas como "solo secundaria" (S1) | Solo secundaria | **Confirmadas con fuente primaria** (9M 10-Q + 4T deck 8-K, cuadre al dólar) | Mejora de calidad: pueden dejar de marcarse como "solo secundaria". **Resuelto en 01 v2** (cifra de 01 v1) |
| D8 | Créditos FY2025: −28 % y 46 % del beneficio operativo | −28 % / 46 % | −27,9 % / 45,8 % | Coinciden (redondeo) |

### 8.2 Otras incidencias de calidad del dato

- **Capex FY2024: 11.339 M$ (deck) frente a 11.342 M$ (S1).** La diferencia de 3 M$ es coherente con que S1 sume las compras de sistemas solares.
- **Cambio de definición del capex.** Desde 1T 2025, el capex de Tesla "is presented inclusive of purchases of energy generation and storage systems" (P4). En FY2021 y FY2022 se usan las compras de PP&E sin esa partida (32 y 5 M$ respectivamente). Es inmaterial, pero rompe la homogeneidad de la serie.
- **FY2025 y TTM se construyen por suma y resta de periodos.** Es correcto para flujos, pero no para la media de acciones diluidas, que se deja en blanco.
- **El beneficio neto de FY2023 no es comparable** por el beneficio fiscal no recurrente (§3).
- **La deuda incluye deuda sin recurso** de vehículos y energía solar. No se pudo separar porque no se leyó la nota de deuda del 10-K.
- **Créditos regulatorios con margen de ~100 %.** Es un supuesto (Tesla no publica su coste). Si tuvieran algún coste, el "beneficio operativo sin créditos" estaría ligeramente infravalorado.
- **Fuentes inaccesibles:**
  - la API XBRL `data.sec.gov` y las páginas R*.htm del 10-K FY2025 y FY2024 (salvo R45 de FY2024);
  - (v2) el índice, las R*.htm y el `Financial_Report.xlsx` del 10-Q 3T 2026; la nota de compensación en acciones de ese 10-Q (el texto se corta antes);
  - el Ex. 99.1 de 4T 2025;
  - el deck de 4T 2022, con sus tablas en imagen.
  - El texto del 10-K FY2025, FY2023 y FY2024 se corta antes del Item 7/8.

### 8.3 Partidas SIN VERIFICAR

1. Media anual de acciones diluidas de FY2025, y por tanto la media TTM.
2. Deuda total excluyendo la deuda sin recurso de vehículos y solar: no separable.
3. Margen bruto por línea (automoción, servicios) en FY2021-FY2024. No forma parte del CSV. El margen de servicios de FY2025 que da 01-negocio.md sigue siendo un derivado de S1.
4. Naturaleza de "Other income (expense), net" en 2025-2026, de signo muy volátil.
5. Desglose del crecimiento de Servicios y otros (FSD, seguros, supercarga, usados).
6. Desglose del circulante que explica la diferencia entre FCO y beneficio en 2026.
7. (v2) Desglose de las 301 M de "stock-based awards" (286 M del ejercicio de 2018 + ~15 M de empleados es una INFERENCIA; el 10-Q no lo desglosa).
8. (v2) Cancelación de las 96 M del CEO Interim Award 2025: solo fuente secundaria, que no da la cifra (v3). La cifra de 96 M sale del Form 4.
9. (v3) Precio medio de TSLA en 1T26 que usa el método de tesorería de §5.1 (a): ~400 $ como supuesto, con un rango de 350-450 $.

---

*Reproducibilidad:* `python3 scripts/fase2_ratios.py` regenera `data/ratios.csv` y `data/checks.csv` a partir de `data/tesla_financials.csv`.

---

## Registro de cambios v2

Fecha: 2026-10-25. Origen: [05-veredicto.md](05-veredicto.md) §5, prioridad 4 (Fase 2), y observaciones de §1, §2.1, §3.2, §3.3 (W2, W4) y §4. Archivos tocados: `data/tesla_financials.csv`, `scripts/fase2_ratios.py`, este documento y el nuevo `fuentes/nuevas_fase2_v2.md` (`fuentes/fuentes.md` no se toca). La v1 del CSV queda guardada fuera del proyecto, solo como copia de trabajo.

| Punto del veredicto | Qué cambió |
|---|---|
| §5 4(a) / §3.3 W2: descomponer las 301 M (diluida − básica) y las 713 M (portada − básica) leyendo la nota de BPA | Leída la nota de BPA del 10-Q 3T26 (básica 3.240, +301 "stock-based awards", diluida 3.541; política de exclusión de acciones restringidas hasta que se "ganan"), junto con los estados de patrimonio de los 10-Q 1T/2T/3T26 y 3T25 y los Form 4 de Musk. Nueva **§5.1**. Resultado: 713 M = 423,7 (CEO 2025) + 286,4 (ejercicio 2018) + 2,6 de residuo; 301 M ≈ 286 (ejercicio 2018, INFERENCIA) + ~15 (empleados); 202 M = 4 + 194 + 4, con 194 ≈ 286,4 − 96 (Interim cancelado, solo fuente secundaria) + ~4. **Las 423,7 M están en la portada, no en la básica ni en la diluida.** **W2 es un doble cómputo real de ~286 M** en la línea de dilución de 03. Script: 9 controles nuevos "Acciones: …" (todos OK) y 9 filas `acc_*` en `ratios.csv` |
| §5 4(b) / §3.2 y W4: D&A TTM en el CSV | Nueva fila `dya_amortizacion_deterioro` en el CSV (FY2021-FY2025, 9M25, 4T25, 9M26, TTM), con fuente en cada celda. Se trata como flujo en el script (FY2025 y TTM construidos y contrastados con P4: OK). **D&A TTM = 6.704 M$** (frente a 7.408 M$ = 3T × 4 usado por 03). Nuevas filas `capex_neto_de_dya` (TTM 8.703), `ebitda_aprox` (TTM 10.170) y `dya_sobre_ingresos` (6,5 %). Tabla de §4 ampliada |
| §5 4(c) / §1: etiqueta `fuente_FY2025` que citaba S1 | En las 8 filas donde la etiqueta era "S1 sec-api.io (secundaria…)", ahora dice: "Construido: 9M25 (10-Q 3T25) + Q4-25 (P4); el valor de esta celda es S1 sec-api.io (cita 10-K FY2025), solo como contraste". El valor numérico no cambia (es el que usa el control de cuadre); el script ya calculaba FY2025 con datos primarios |
| §5 4(d) / §2.1 nota ² y §4: re-verificar FY2021 | El `Financial_Report.xlsx` del 10-K FY2022 **sí fue accesible** en esta ronda. Las 19 partidas de FY2021 del CSV (y las de FY2022) coinciden exactamente. Etiquetas `fuente_FY2021`/`fuente_FY2022` marcadas "[re-verificado 25-oct-2026 vía WebFetch, v2]". Contraste adicional con el deck Q4 2021 (beneficio neto, FCF, capex y efectivo redondeados: 4 controles OK). **FY2021 deja de ser riesgo residual** |
| §2.1 F20 (créditos FY2022 no legibles en el 10-K FY2022) | Resuelto: 1.776 leído directamente en el `Financial_Report.xlsx` del 10-K FY2022 |
| §1.3 y cabecera | Recuento de controles actualizado: 72 controles, 67 OK; las 5 discrepancias son las mismas de v1 (§8) |
| §8.2 / §8.3 | Añadidas las fuentes no accesibles de esta ronda y dos partidas SIN VERIFICAR nuevas (desglose exacto de las 301 M; cancelación de las 96 M del Interim Award) |

**Lo que no cambia:** ninguna cifra existente del CSV ni de las tablas §2-§7 de v1. Todas las filas de `ratios.csv` de v1 se mantienen con el mismo valor (se añaden 13 filas, de 81 a 94).

**Pendiente para otras fases (no aplicado aquí):** Fase 3 debe sustituir `DA_TTM_APROX` (7.408) por 6.704 y revisar la línea `SH_DIL_MAX` (portada + 301) a la luz de §5.1. Fase 4 debe reformular W2.

---

## Registro de cambios v3

Fecha: 2026-10-25. Origen: [05-veredicto-v2.md](05-veredicto-v2.md) §8, prioridad 1 (Fase 2), con §2.2, §4.1 ("Observación sobre la inferencia 286 + 15") y §5 (E1, E2). Archivos tocados: `scripts/fase2_ratios.py`, `data/ratios.csv`, `data/checks.csv`, el nuevo `data/tablas_02_redondeo.csv` y este documento. `data/tesla_financials.csv` no cambia. No hay fuentes nuevas, así que no se crea `fuentes/nuevas_fase2_v3.md`.

| Punto del veredicto | Qué cambió |
|---|---|
| **(a)** % de las tablas calculados desde el valor completo, no desde `ratios.csv` a 4 decimales | El script genera `data/tablas_02_redondeo.csv` (% a 1 decimal, M$ a 0, redondeo mitad hacia arriba con `Decimal` sobre el valor completo) e imprime las celdas en las que re-redondear el CSV daría otra cifra. Corregidas las 6 celdas del veredicto: margen operativo TTM **3,4 → 3,3 %** (también en §0), créditos / BO FY24 39,1 → 39,0 %, margen neto FY21 10,2 → 10,3 %, crecimiento BO FY22 109,3 → 109,4 %, crecimiento de ingresos FY22 51,3 → 51,4 %, SBC / ingresos FY24 2,1 → 2,0 %. **Otros casos del mismo tipo que encontró el script:** ROIC B FY23 **12,2 → 12,1 %** (12,145 %), CAGR de automoción 10,2 → 10,1 % (§2) y crecimiento del FCF FY25 +73,6 → +73,5 % (§4). El crecimiento de la SBC FY22 (−26,4 %) no se cita en 02. Además, las filas % de `ratios.csv` pasan a 6 decimales, para que el ROIC B FY23 también salga bien a quien redondee desde el CSV. Excepción: `roic_A_neto_caja`, `margen_operativo_sin_creditos` y `crec_9M26_vs_9M25_ingresos_energia` siguen con 4, porque `fase3_dcf.py` las usa en cálculos y Fase 2 no debe cambiar sus resultados (comprobado: la salida de fase3 es idéntica salvo la línea informativa del ROIC B FY23, que pasa a 12,1 %). Se añaden 15 filas a `ratios.csv` (de 94 a 109) para cifras del texto: capex neto / ingresos (8,4 %), D&A aproximada +10,5 % / 704 M$, dilución legal +18,9 %, cuadres de §5.1 y método de tesorería. Ninguna fila de v2 cambia de valor. El script también fuerza la salida en UTF-8, porque en consolas Windows (cp1252) fallaba al imprimir "≈" y hacía caer `fase5v2_cifras.py` si se ejecutaba sin `PYTHONIOENCODING` |
| **(b)** E1: §5.1 presentaba las 4.254 M y "03 §6.4" como vigentes | Ahora se presentan como **03 v1**, resuelto en 03 v2 (§3 y §6.5). Los "~7 %" y "~10 %" se sustituyen por cifras del script: 7,2 % y 10,7 % (filas `acc_portada_mas_301_sobre_fd` y `acc_diluida_media_sobre_fd`). Los VPA de 04 v1 se marcan como retirados |
| **(c)** E2: D1-D6 de §8.1 y etiquetas de `checks.csv` | §8.1 lleva una nota de estado y cada fila D1-D7 dice "**Resuelto en 01 v2**". La columna pasa a llamarse "01-negocio.md v1". En `checks.csv`, los cuatro controles DISCREPANCIA que citaban 01 ahora dicen "S2 / 01 v1 (S2 Electrek)" (SBC y capex 9M), "P1 Item 1A / 01 v1" (deuda) y "S11 / 01 v1" (PER). **Discrepancia parcial con el veredicto, con evidencia del propio `checks.csv`:** de los 5 controles, el de capex FY2024 (11.339 frente a 11.342) compara con S1 Tabla 2.2 y nunca con 01, así que conserva su etiqueta. Al PER y a la deuda no les corresponde "S2" porque su fuente es S11 y P1. Los controles siguen en DISCREPANCIA (67 OK + 5) porque comparan con la fuente secundaria, no con 01 v2 |
| **(d)** Frase de 1T26 y secundaria de la cancelación | §5.1 (a): por el método de tesorería, las 303,96 M de opciones de 2018 aportaban ~286,2 M a ~400 $ (283,7-288,2 M entre 350 y 450 $). Las 304 M de "awards" de 1T26 son ~286 M de Musk + ~17,8 M de empleados (15,8-20,3 M). El precio medio de 1T26 queda **SIN VERIFICAR** (§8.3, punto 9). §5.1 (c) y §8.3 (8): la cifra de 96 M sale del Form 4. La secundaria (Not a Tesla App) solo recoge la cancelación y **no da la cifra**: habla de un "$29 billion interim award" |

**Cifras que cambian y que otras fases copian:** margen operativo TTM **3,4 % → 3,3 %** (03 §7 y 04 §3.2, según 05-veredicto-v2 §5). Las demás cifras corregidas no aparecen en 01, 03 ni 04, según el catálogo de `fase5v2_cifras.py` y una búsqueda en esos documentos. Las cifras de 02 que usa Fase 3 (importes, acciones totalmente diluidas 3.967,3 M, D&A 6.704 M$) no cambian.
