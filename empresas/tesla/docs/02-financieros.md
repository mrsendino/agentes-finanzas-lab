# 02 — Estados financieros de Tesla (TSLA): FY2021–FY2025 y TTM a 3T 2026

**Fecha del análisis:** 2026-10-24 · **Analista:** Fase 2 (rol *Financial Analyst*) · **Alcance:** solo datos históricos. Este documento no contiene previsiones, valoraciones ni recomendaciones.

**Archivos de esta fase:**

| Archivo | Contenido |
|---|---|
| [`data/tesla_financials.csv`](../data/tesla_financials.csv) | Datos brutos. Cada valor lleva su fuente en la columna `fuente_<periodo>` |
| [`scripts/fase2_ratios.py`](../scripts/fase2_ratios.py) | Script que hace todos los cálculos |
| [`data/ratios.csv`](../data/ratios.csv) | Salida con todos los ratios |
| [`data/checks.csv`](../data/checks.csv) | 55 controles de cuadre |

Todas las cifras de las tablas salen de `ratios.csv`. No se ha hecho ningún cálculo a mano.

---

## 0. Resumen ejecutivo: lo esencial

1. **Los ingresos se han estancado y su composición ha cambiado.**
   - Los ingresos crecieron un +51 % en 2022 y un +19 % en 2023, se quedaron planos en 2024 (+0,9 %) y cayeron en 2025 (−2,9 %), hasta 94.827 M$.
   - En los últimos doce meses a 3T 2026 vuelven a subir, hasta 103.570 M$ (los nueve primeros meses de 2026 crecen un +12,5 % sobre los de 2025).
   - Automoción ha pasado del 88 % al 72 % de los ingresos. Energía y Servicios ya suman ~28 %.
2. **La rentabilidad operativa se ha desplomado.**
   - El margen operativo pasó del 16,8 % (2022) al 4,6 % (2025) y al 3,4 % (TTM).
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
| FY2021, FY2022 | [10-K FY2022](https://www.sec.gov/Archives/edgar/data/1318605/000095017023001409/tsla-20221231.htm), acc. 0000950170-23-001409 ([Financial_Report.xlsx](https://www.sec.gov/Archives/edgar/data/1318605/000095017023001409/Financial_Report.xlsx)) | Estados consolidados auditados |
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

De los 55 controles, **50 están OK**. Cubren:
- suma de segmentos = ingresos totales;
- ventas + créditos + leasing = automoción;
- FCO − capex = FCF publicado (FY2023, FY2024, FY2025 y TTM);
- suma de los cuatro trimestres de 2024 = FY2024;
- beneficio bruto − gastos operativos = beneficio operativo en 3T 2026.

Las 5 discrepancias se explican en §8.

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
| Ingresos totales | 51,3 % | 18,8 % | 0,9 % | −2,9 % | 12,5 % |
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
- automoción: 10,2 %;
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
| **Margen operativo** | 12,1 % | 16,8 % | 9,2 % | 7,2 % | 4,6 % | 3,4 % |
| Beneficio operativo sin créditos | 5.058 | 11.880 | 7.101 | 4.313 | 2.362 | 2.285 |
| **Margen operativo sin créditos** | 9,4 % | 14,6 % | 7,3 % | 4,4 % | 2,5 % | 2,2 % |
| **Créditos / beneficio operativo** | 22,5 % | 13,0 % | 20,1 % | 39,1 % | 45,8 % | 34,1 % |
| Beneficio neto atribuible a comunes | 5.519 | 12.556 | 14.997 | 7.091 | 3.794 | 3.218 |
| **Margen neto** | 10,2 % | 15,4 % | 15,5 % | 7,3 % | 4,0 % | 3,1 % |
| Crecimiento del beneficio operativo | — | 109,3 % | −34,9 % | −20,4 % | −38,5 % | 9M: −30,2 % |
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
| SBC / ingresos | 3,9 % | 1,9 % | 1,9 % | 2,1 % | 3,0 % | 4,2 % |
| **FCF − SBC** | 2.894 | 6.006 | 2.546 | 1.585 | 3.395 | **−997** |

**Qué cambió y por qué:**
- **El FCO resiste mejor que el beneficio.** En TTM llega a 18.710 M$, máximo de la serie, mientras el beneficio operativo cae. Dos motivos:
  - Las partidas sin salida de caja son grandes y crecientes: la amortización de 3T 2026 es de 1.852 M$ (P4) y la SBC de 1.165 M$.
  - Influye también el circulante, pero no se ha desglosado (**SIN VERIFICAR**).
- **El capex de 2025 fue anormalmente bajo** (−24,8 % interanual), lo que infla el FCF de 2025 (+73,6 %). En 2026 se dispara: 13.014 M$ en 9M, un +112 % (10-Q 3T 2026), con 5.789 M$ solo en 2T 2026 (P4). Tesla lo atribuye a inversión en "SI, robotics and energy" (P4). Por eso el FCF de 2025 **no es una base representativa** para extrapolar.
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
  - 2025–2026: las medias diluidas suben a 3.523 M (9M 2025) y 3.539 M (9M 2026).
  - Tendencia hacia delante: el plan del CEO de 2025 prevé hasta 423,7 M de acciones restringidas (S10, 01-negocio.md), es decir, ~12 % de dilución potencial si se cumplen los hitos. La media diluida de los trimestres aún no refleja ese impacto.

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
| **ROIC B (bruto)** | 13,9 % | 25,4 % | 12,2 % | 7,5 % | 4,0 % | 2,9 % |
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

### 8.1 Discrepancias frente a 01-negocio.md (Fase 1)

| # | Dato | 01-negocio.md | Dato primario de Fase 2 | Valoración |
|---|---|---|---|---|
| D1 | SBC 3T 2026 | 1.170 M$ (S2, Electrek) | **1.165 M$** (P4, estado de flujos y reconciliación EBITDA) | Diferencia menor (−5 M$). S2 redondea o usa otra partida. Prevalece P4 |
| D2 | Capex 9M 2026 | 13.010 M$ (S2) | **13.014 M$** (10-Q 3T 2026) | Redondeo de S2. Prevalece el 10-Q |
| D3 | Deuda a 31-dic-2025 | "8.180 M$ de deuda principal" (P1, Item 1A) | **8.376 M$** de deuda y arrendamientos financieros contables (10-Q 3T 2026 y P4) | No es un error, sino **dos conceptos distintos**: principal nominal frente a valor contable que incluye arrendamientos financieros. Fase 1 los presenta como "deuda" sin matizar. Además, en §2 de 01-negocio.md compara caja a 30-sep-2026 (45.400) con deuda a 31-dic-2025: **fechas mezcladas**. A 30-sep-2026 la deuda contable es de 9.523 M$ |
| D4 | Caja e inversiones 3T 2026 | 45.400 M$ | **45.447 M$** (10-Q: 17.853 de efectivo + 27.594 de inversiones a corto plazo) | Redondeo. Correcto en sustancia |
| D5 | PER de ~327x (S11) | ~327x | Con el BPA GAAP TTM hasta 2T 2026 (1,08 $, P4) sale 328x. Con el BPA TTM hasta 3T 2026 (0,91 $), **390x** | El ~327x de S11 era previo a los resultados del 3T. Con el último BPA, el PER al mismo precio de 354,72 $ es ~390x. Fase 1 no está mal, pero el dato ya está **desfasado** |
| D6 | "Beneficio neto GAAP 3T 2026: 787 M$" | 787 | 787 es el atribuible a comunes. El beneficio neto total es de 804 M$ (P4) | Etiqueta imprecisa, no error de cifra |
| D7 | Cifras FY2025 marcadas como "solo secundaria" (S1) | Solo secundaria | **Confirmadas con fuente primaria** (9M 10-Q + 4T deck 8-K, cuadre al dólar) | Mejora de calidad: pueden dejar de marcarse como "solo secundaria" |
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

---

*Reproducibilidad:* `python3 scripts/fase2_ratios.py` regenera `data/ratios.csv` y `data/checks.csv` a partir de `data/tesla_financials.csv`.
