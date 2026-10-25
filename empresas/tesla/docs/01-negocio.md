# 01 — Negocio de Tesla (TSLA): modelo, ventajas, competencia, riesgos y opcionalidad

**Fecha del análisis:** 2026-10-24 · **Revisión v2:** 2026-10-25 (correcciones del veredicto de Fase 5, ver *Registro de cambios v2* al final) · **Revisión v3:** 2026-10-25 (veredicto v2, ver *Registro de cambios v3* al final) · **Último ejercicio fiscal:** FY2025 (cerrado 31-dic-2025) · **Último trimestre:** Q3 2026 (cerrado 30-sep-2026)
**Alcance:** descriptivo. No contiene recomendaciones de compra o venta.

**Cómo se citan las fuentes.** Cada cifra lleva una etiqueta enlazada con este formato: documento, sección o tabla, y fecha. Los IDs (P = primaria, S = secundaria, M/T = fases 3 y 4) están detallados en `/fuentes/fuentes.md`. Las fuentes nuevas de la v2 (N1, N2) están en `/fuentes/nuevas_fase1_v2.md`.
- **SIN VERIFICAR**: no se pudo contrastar con ninguna fuente.
- **solo secundaria**: el dato procede únicamente de una fuente secundaria. El texto del 10-K FY2025 que devolvió la herramienta se corta en el Item 1A, antes del MD&A y de los estados financieros.
- **Cambio en v2:** Fase 2 reconstruyó FY2025 con fuente primaria (9M del 10-Q 3T 2025 + columna 4T del deck P4) y cuadró al dólar con S1 (11 de 11 controles; [02 §1.2](02-financieros.md)). Por eso se retiran las marcas "solo secundaria" de ingresos por línea, beneficio bruto total, beneficio operativo y beneficio neto de FY2025. **Se mantienen** donde esa confirmación no llega: el beneficio bruto por línea, la nota geográfica (China) y la inversión en xAI.

---

## 1. Modelo de negocio por segmento

Tesla reporta **dos segmentos contables**:
- **Automotive**, que incluye "Services and other".
- **Energy generation and storage**.

Por claridad, aquí se separan las tres líneas de ingreso.

### 1.1 Último ejercicio fiscal: FY2025

| Línea | Ingresos FY2025 (M$) | Var. vs FY2024 | Margen bruto FY2025 | Fuente |
|---|---|---|---|---|
| Automoción total (venta + créditos + leasing) | 69.526 | −9,8 % (77.070) | 17,8 % (BB 12.361) | Ingresos: confirmados con fuente primaria ([02 §2](02-financieros.md)). BB por línea: [S1](https://sec-api.io/insights/financial-analysis-of-tesla-fy2025-and-the-first-half-of-2026), Tablas 1.1 y 2.3 (cita el 10-K FY2025, acc. 0001628280-26-003952), **solo secundaria** |
| · de ello, créditos regulatorios | 1.993 | −28 % (2.763) | ~100 % (sin coste asociado; supuesto) | Confirmado con fuente primaria ([02 §2](02-financieros.md): −27,9 %); también [S1](https://sec-api.io/insights/financial-analysis-of-tesla-fy2025-and-the-first-half-of-2026), Tabla 1.1, y [S6](https://carboncredits.com/tesla-reports-first-ever-annual-revenue-drop-in-2025-carbon-credit-sales-also-dip-28) |
| Energía (generación y almacenamiento) | 12.771 | +26,6 % (10.086) | 29,8 % (BB 3.802) | Ingresos: confirmados con fuente primaria ([02 §2](02-financieros.md)). Margen: [S1](https://sec-api.io/insights/financial-analysis-of-tesla-fy2025-and-the-first-half-of-2026), Tablas 1.1 y 1.2, y [S4](https://www.energy-storage.news/tesla-energy-storage-deployments-jumped-in-crucial-ai-transformation-year-company-expects-margin-compression-in-2026/) (2-feb-2026), **solo secundaria** |
| Servicios y otros (posventa, supercarga, seguros, usados, FSD de suscripción…) | 12.530 | +18,9 % (10.534) | ~7,4 % (BB ~931, **derivado**) | Ingresos: confirmados con fuente primaria ([02 §2](02-financieros.md)). El BB no aparece en el 10-K: se obtiene como segmento Automotive (13.292) menos automoción (12.361), ambos de S1. **Solo secundaria + cálculo propio** (ver 02 §8.3) |
| **Total** | **94.827** | −2,9 % (97.690) | **18,0 %** (BB 17.094) | Confirmado con fuente primaria ([02 §2 y §3](02-financieros.md)); también [S1](https://sec-api.io/insights/financial-analysis-of-tesla-fy2025-and-the-first-half-of-2026) y [S3](https://finance.yahoo.com/news/tesla-revenue-slips-2025-energy-163645200.html) (29-ene-2026) |

Otros datos de FY2025 (confirmados con fuente primaria en [02 §3](02-financieros.md); también S1 y S3):
- **Beneficio operativo:** 4.355 M$.
- **Beneficio neto atribuible:** 3.794 M$, un −46 % interanual.

Datos operativos de FY2025, según el [8-K Ex. 99.1 de entregas Q4 2025 (P6)](https://www.sec.gov/Archives/edgar/data/1318605/000162828026000016/exhibit9914.htm) del 2-ene-2026, confirmado en [Tesla IR (P7)](https://ir.tesla.com/press-release/tesla-fourth-quarter-2025-production-deliveries-deployments):
- **Entregas:** 1.636.129 vehículos.
- **Producción:** 1.654.667 vehículos.
- **Almacenamiento desplegado:** 46,7 GWh.

### 1.2 Último trimestre: Q3 2026

Fuente principal: [8-K Ex. 99.1 "Q3 2026 Update" (P4)](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm), Financial Summary, 21-oct-2026. Los ingresos se han contrastado con la cuenta de resultados del [10-Q Q3 2026 (P2)](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066775/tsla-20260930.htm), Item 1.

| Línea | Q3 2026 (M$) | Q3 2025 (M$) | Var. | Margen bruto Q3 2026 |
|---|---|---|---|---|
| Automoción total | 20.560 | 21.205 | −3 % | 18,5 % GAAP; 18,1 % sin créditos |
| · créditos regulatorios | 113 | 417 | −73 % | — |
| Energía | 2.881 | 3.415 | −16 % | 33,1 % (BB 954)¹ |
| Servicios y otros | 4.605 | 3.475 | +33 % | 15,9 % (BB 734) |
| **Total** | **28.046** | **28.095** | ≈0 % | **19,6 %** |

¹ **El 33,1 % no es un margen recurrente.** Es un cálculo propio (P4 publica ingresos y coste, no el porcentaje). En la call de 3T26, el CFO (Vaibhav Taneja) explicó que la subida desde el 20,4 % de 2T26 se debe "primarily" a "tariff refunds recognized in the quarter" y a "warranty true-downs resulting from alignment with our vendor on certain cell-related costs to be reimbursed by them" ([T1](https://www.fool.com/earnings/call-transcripts/2026/10/22/tesla-tsla-q3-2026-earnings-call-transcript/), 22-oct-2026). Nadie cuantificó esos efectos, así que el margen sin ellos queda **SIN VERIFICAR**. No debe extrapolarse.

Otras cifras del trimestre:
- **Beneficio operativo:** 718 M$ (−56 %), con un margen operativo del 2,6 % (P4).
- **Beneficio neto:** 787 M$ **atribuible a accionistas comunes**; 804 M$ de beneficio neto total, que incluye la parte de minoritarios (P4; [02 §8.1, D6](02-financieros.md)).
- **Flujo de caja libre (FCF):** 1.531 M$ (P4).
- **Capex:** 4.732 M$ (P4).
- **Caja e inversiones a 30-sep-2026:** 45.447 M$, es decir, 17.853 M$ de efectivo más 27.594 M$ de inversiones a corto plazo (P2).
- **Deuda y arrendamientos financieros a 30-sep-2026:** 9.523 M$, es decir, 1.387 M$ corrientes más 8.136 M$ no corrientes (P2). **Caja neta: 35.924 M$** ([02 §5](02-financieros.md)).
- **Entregas:** 486.532 (P4).
- **Almacenamiento desplegado:** 13,7 GWh (P4).

Datos de los nueve meses de 2026, según [P2](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066775/tsla-20260930.htm):
- **Ingresos:** 78.669 M$, frente a 69.926 M$ en los nueve meses de 2025.
- **Créditos regulatorios:** 639 M$, frente a 1.451 M$.
- **Capex:** 13.014 M$.

Gastos del trimestre, según P4 (estado de flujos y reconciliación de EBITDA; [02 §3-4](02-financieros.md)):
- **I+D:** 2.761 M$, frente a 1.630 M$ en Q3 2025 (+69 %).
- **Compensación en acciones (SBC):** 1.165 M$.

[S2](https://electrek.co/2026/10/21/tesla-tsla-q3-2026-financial-results/) (Electrek, 21-oct-2026) da 2.760 y 1.170 M$. La diferencia es de redondeo y prevalece P4.

**Lectura.** El crecimiento está ahora en **Servicios** y, hasta 2025, en **Energía**. La automoción, que aporta el ~73 % de los ingresos de Q3 2026 (20.560 de 28.046), está estancada. El margen operativo es estrecho porque el gasto en IA e I+D crece mucho más deprisa que el beneficio bruto. El margen de Energía del trimestre está inflado por efectos puntuales (nota ¹).

---

## 2. Ventajas competitivas y su durabilidad

| Ventaja | Evidencia | Durabilidad |
|---|---|---|
| **Escala y coste en fabricación de VE** | Margen bruto de automoción sin créditos del 18,1 % en Q3 2026 ([P4](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm)). Capacidad instalada en Shanghái de >950.000 unidades/año (P4, tabla de capacidad) | **Media-baja.** BYD vende más VE de batería (§3) y la presión en precios es explícita: Tesla cita un "lower vehicle ASP" en Q3 2026 (P4) |
| **Datos de flota y software (FSD)** | 1,74 M de suscripciones activas a FSD (Supervised), +67 % interanual ([P4](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm)). Según [S2](https://electrek.co/2026/10/21/tesla-tsla-q3-2026-financial-results/), la cifra incluye compras por adelantado | **Media.** Es una ventaja real en datos, pero no se ha demostrado aún que sea monetizable a escala |
| **Energía (Megapack) y relación con utilities** | Según Wood Mackenzie, **Tesla y Sungrow ocupan los dos primeros puestos** mundiales de integradores BESS en 2025, por tercer año seguido. La nota de prensa **no dice cuál de los dos es el primero** ([N1](https://www.woodmac.com/press-releases/2026-bess-market-share-chinese-integrators-76-percent-global-dominance-2025/), 29-jun-2026; recogida por [S9](https://www.energy-storage.news/chinese-system-integrators-capture-76-of-global-bess-market-as-competition-intensifies/), 7-jul-2026). Tesla sí es la primera en Norteamérica (N1). Con otra metodología, Benchmark la sitúa 2.ª, con ~10 % de cuota frente al ~13 % de BYD ([S8](https://electrek.co/2026/05/13/byd-surpasses-tesla-energy-storage-bess-benchmark-2025/), 13-may-2026) | **Media-baja.** Los integradores chinos suman el 76 % del mercado y la cuota de los tres primeros cayó del 36 % al 30 % entre 2024 y 2025 (N1). La propia Tesla anticipó compresión de margen en 2026 ([S4](https://www.energy-storage.news/tesla-energy-storage-deployments-jumped-in-crucial-ai-transformation-year-company-expects-margin-compression-in-2026/)). El margen del 33,1 % de Q3 2026 no lo contradice, porque incluye efectos puntuales (§1.2, nota ¹) |
| **Red de supercarga y servicios** | Servicios y otros crece un +33 % en Q3 2026 con un margen bruto del 15,9 % ([P4](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm)) | **Media.** Es una base instalada recurrente, pero la apertura de la red a otras marcas diluye la exclusividad (cualitativo) |
| **Balance** | A **30-sep-2026**: 45.447 M$ de caja e inversiones y 9.523 M$ de deuda y arrendamientos financieros contables. Caja neta de 35.924 M$ ([P2](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066775/tsla-20260930.htm); [02 §5](02-financieros.md)). Además, Tesla tiene una capacidad de endeudamiento de hasta 30.000 M$ que no prevé disponer en 2026 [CALL, [T1](https://www.fool.com/earnings/call-transcripts/2026/10/22/tesla-tsla-q3-2026-earnings-call-transcript/)]. *Nota:* los 8.180 M$ que cita el 10-K son el **principal nominal a 31-dic-2025**, sin arrendamientos ([P1](https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm), Item 1A). Es otro concepto y otra fecha, así que no se compara con la caja de septiembre | **Alta** a corto plazo. **Capex 2026: ~20.000 M$**, según la guía revisada por el CFO en la call de Q3 2026: "We're revising our CapEx guidance to be approximately $20 billion for the current year" ([T1](https://www.fool.com/earnings/call-transcripts/2026/10/22/tesla-tsla-q3-2026-earnings-call-transcript/), 22-oct-2026). Sustituye a las guías anteriores: ">20.000 M$" en la call de Q4 2025 ([S5](https://vectorshift.ai/research/companies/tesla/earnings/2025-q4)) y ">25.000 M$" en la de Q1 2026 ([T10](https://www.boerse-express.com/news/articles/tesla-fuenf-staedte-fuer-robotaxi-rollout-ausstehend-897971); recogida por S2). Con 13.014 M$ gastados en 9M (P2), el Q4 implícito es de ~7.000 M$. El CFO prevé financiarlo "primarily from our cash flows from operations" (T1). No incluye la Terafab, para la que Musk habla de "tens of billions" hasta 2028 [MUSK, T1] |

---

## 3. Competidores principales

- **BYD.** En 2025 vendió **2.256.714 turismos eléctricos de batería (BEV)**, según su comunicado a la bolsa de Hong Kong del 1-ene-2026 ([N2](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0101/2026010100423.pdf)). Esa es la cifra de "2,26 M de VE" de [S7](https://insideevs.com/news/783252/tesla-byd-global-sales-2025/) (InsideEVs): **solo BEV, sin híbridos enchufables**. Si se suman sus 2.288.709 híbridos enchufables (PHEV) y 57.013 vehículos comerciales, el total NEV es de 4.602.436 (N2). Así, la comparación con las 1.636.129 entregas de Tesla (P6) es homogénea en tecnología, BEV contra BEV. Queda un matiz: BYD informa de "ventas" (incluye exportaciones) y Tesla de "entregas". BYD también superó a Tesla en almacenamiento: >60 GWh frente a 46,7 GWh ([S8](https://electrek.co/2026/05/13/byd-surpasses-tesla-energy-storage-bess-benchmark-2025/)). Es el competidor más directo, porque compite en coste, integración vertical de baterías y ambos negocios.
- **Fabricantes chinos de VE** (Geely, Xiaomi, Li Auto, Xpeng, NIO…). La cuota de Tesla en China baja: China pasó de aportar ~22,1 % de los ingresos en FY2025 (20.962 M$) a un 17,5 % en H1 2026 (8.859 M$) ([S1](https://sec-api.io/insights/financial-analysis-of-tesla-fy2025-and-the-first-half-of-2026), Tabla 1.6, que cita el 10-Q Q2 2026). **Solo secundaria**: la nota geográfica no apareció en la parte de P2/P3 que pude leer, y Fase 2 tampoco la confirmó (02 §1.2). No hay cifras verificadas de cada rival chino: **SIN VERIFICAR**.
- **Fabricantes tradicionales** (VW, GM, Ford, Hyundai-Kia, Toyota…). El 10-K no nombra competidores concretos. Advierte de que "many of our competitors have significantly more or better-established resources" y de posibles "price reductions" y "loss of market share" ([P1](https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm), Item 1A). Su relevancia actual es más como compradores de créditos regulatorios que como rivales en VE.
- **Almacenamiento de energía.** Sungrow comparte con Tesla los dos primeros puestos del ranking de Wood Mackenzie, sin orden público entre ambos, y es la primera en Europa. BYD es 3.ª tras subir cinco puestos ([N1](https://www.woodmac.com/press-releases/2026-bess-market-share-chinese-integrators-76-percent-global-dominance-2025/)). CATL es proveedor de celdas y no figura en el ranking de integradores ([S9](https://www.energy-storage.news/chinese-system-integrators-capture-76-of-global-bess-market-as-competition-intensifies/)). Ocho de los diez primeros integradores son chinos (N1, S9). Una fuente secundaria que pone a Sungrow 1.ª y a Tesla 2.ª contradice a N1 en el resto del ranking y se ha descartado (ver `fuentes/nuevas_fase1_v2.md`).
- **Robotaxi** (Waymo y otros) y **robots humanoides**: no tengo métricas verificadas de estos rivales en esta fase (**SIN VERIFICAR**; 04 §2 recoge datos de Waymo con sus etiquetas).

---

## 4. Riesgos principales

1. **Dependencia de Elon Musk (persona clave).** El 10-K dice que Tesla es "highly dependent on the services of Elon Musk", que Musk "does not devote his full time and attention to Tesla" y que ocupa cargos en otras compañías como SpaceX ([P1](https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm), Item 1A). Hay además vínculos financieros entre las empresas de Musk:
   - Tesla compró participaciones de SpaceX por 2.002 M$ en H1 2026 ([P3](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026049270/tsla-20260630.htm), estado de flujos: "Purchase of SpaceX equity investment").
   - Confirmó una inversión de 2.000 M$ en xAI ([S6](https://carboncredits.com/tesla-reports-first-ever-annual-revenue-drop-in-2025-carbon-credit-sales-also-dip-28), dato **solo secundaria**; P2 no lo menciona).
   - Plan de retribución de 2025, aprobado el 6-nov-2025 con >75 % de los votos emitidos: 423,7 M de acciones restringidas en 12 tramos. Equivalen al 12,0 % del capital previo a la emisión (3.529.014.042 acciones: portada menos las 423.743.904 del plan) y al 10,7 % de las 3.952.757.946 acciones de la portada del [10-Q 3T 2026 (P2)](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066775/tsla-20260930.htm) a 15-oct-2026, que ya las incluye ([02 §5.1](02-financieros.md); Form 4 de jun-2026; cálculo en `scripts/fase1_cifras.py`). Están ligadas, ligados a capitalizaciones de hasta 8,5 billones $ y a hitos operativos ([S10](https://www.meridiancp.com/insights/tesla-shareholders-approve-2025-ceo-performance-award/)). Los hitos son 1 M de robots, 1 M de robotaxis y 10 M de suscripciones FSD, y condicionan las prioridades de la gestión.
2. **Dependencia de los créditos regulatorios.** En FY2025 los créditos fueron 1.993 M$, equivalentes al **46 % del beneficio operativo** (4.355 M$; cálculo propio, 45,8 % en [02 §3](02-financieros.md)). En Q3 2026 cayeron a 113 M$, un −73 % ([P4](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm)). El 10-K atribuye esta caída a la ley OBBBA, que "restricted certain regulatory credit programs" y eliminó el crédito fiscal al consumidor de VE ([P1](https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm), Item 1). Este ingreso de margen casi total está desapareciendo.
3. **Presión de precios.** Tesla cita un "lower vehicle average selling price" en Q3 2026 ([P4](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm)). Los ingresos de automoción cayeron un −9,8 % en FY2025 ([02 §2](02-financieros.md)). En energía, Tesla prevé compresión de margen por "increased low-cost competition" y aranceles ([S4](https://www.energy-storage.news/tesla-energy-storage-deployments-jumped-in-crucial-ai-transformation-year-company-expects-margin-compression-in-2026/)). En Q3 2026 los ingresos de Energía cayeron un −16 %, "partially due to tariff-related customer refunds" (P4). El margen de ese trimestre se apoyó en efectos puntuales (§1.2, nota ¹).
4. **Exposición a China.** China supone ~22 % de los ingresos de FY2025 (S1, **solo secundaria**). Shanghái es la mayor planta del grupo, con >950.000 unidades de capacidad (P4). El 10-K señala tres riesgos ([P1](https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm), Item 1A):
   - aranceles y represalias comerciales;
   - cambios en los acuerdos comerciales "such as those with China";
   - riesgo de inundación en Gigafactory Shanghai.
5. **Ejecución y cadena de suministro.** La propia Tesla dice que "battery availability continued to be the limiting factor in increasing auto volumes" en Q3 2026 (P4). La provisión de garantías subió a 10.138 M$, frente a 8.075 M$ un año antes ([P2](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066775/tsla-20260930.htm), tabla de "Accrued warranty, end of period").
6. **Intensidad de capital y márgenes.** El margen operativo fue del 2,6 % en Q3 2026 (P4), con un capex 2026 de ~20.000 M$, más del doble que los 8.527 M$ de FY2025 (§2; T1; [02 §4](02-financieros.md)). Si los nuevos negocios se retrasan, el retorno sobre ese capex se aplaza.

---

## 5. Qué parte de la valoración depende de negocios sin ingresos significativos

**Contexto de mercado** (datos del 16-oct-2026, **anteriores a los resultados de Q3 2026**; los vigentes están en [03-valoracion.md §1](03-valoracion.md)):
- **Capitalización:** ~1,4 billones $ ([S11](https://pepperstone.com/en/insights/market-analysis/equities/tesla-q3-2026-earnings-preview) y [S12](https://tradethepool.com/pre-market-prep/tesla-stock-price-before-q3-earnings-what-will-move-it/), cotización de 354,72 $ a 16-oct-2026).
- **PER de los últimos doce meses:** ~327x según S11. **DESFASADO**: S11 lo calculó antes de publicarse Q3 2026, con el BPA TTM hasta Q2 2026 ([02 §8.1, D5](02-financieros.md)). No debe usarse. El PER vigente y su definición están en [03-valoracion.md §7](03-valoracion.md). Los documentos usan definiciones de PER distintas ([05 §3.1](05-veredicto.md)).

**Cálculo ilustrativo propio (no procede de ninguna fuente).** Supongamos que el negocio actual valiera 30 veces el beneficio neto de FY2025 (3.794 M$). Eso daría ~114.000 M$, es decir, **menos del 10 % de la capitalización**. La conclusión se mantiene con la capitalización posterior a resultados de 03 §1. Con cualquier múltiplo razonable, la mayor parte del precio descuenta negocios que hoy no aportan ingresos materiales y separados en las cuentas. Pepperstone (S11) atribuye al robotaxi ~30 % de su propio valor objetivo. Es una opinión de un tercero, no un dato.

**Lo que Tesla ha reportado de hecho:**

| Iniciativa | Lo reportado por Tesla | ¿Ingresos separados? |
|---|---|---|
| **FSD (Supervised)** | 1,74 M de suscripciones activas en Q3 2026 ([P4](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm)). Aprobado en 9 países de la UE (P4). Tesla insiste en que "does not make the vehicle autonomous" (P4) | No. Se registra dentro de automoción y servicios; Tesla no desglosa su importe (**SIN VERIFICAR**) |
| **Robotaxi** | Lanzado en junio de 2025 con Model Y ([P1](https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm), Item 1). "Nearly two million cumulative unsupervised miles" y horario en Austin de 6:00 a 24:00 (P4, Q3 2026). Tesla no da número de vehículos ni de ciudades. En la call de Q4 2025, Musk habló de >500 vehículos y "dozens" de ciudades a final de 2026 ([S5](https://vectorshift.ai/research/companies/tesla/earnings/2025-q4); es una declaración, no un dato auditado) | No |
| **Cybercab** | En la call de Q4 2025 se previó iniciar la producción en abril de 2026 (S5). En Q3 2026 Tesla informa de que empezó su despliegue en la flota de Austin y de una capacidad instalada de ">125,000" unidades (P4). Volumen producido: **SIN VERIFICAR** (no se publica) | No |
| **Optimus (robot humanoide)** | "Optimus production began in Fremont on our high-volume lines" (P4, Q3 2026). El 10-K dice: "we have yet to commercialize Bots… there is no guarantee this business will be successful" ([P1](https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm), Item 1A). No se informa de unidades, ventas externas ni ingresos | No |
| **Cómputo de IA y chips** | Objetivo de 400 MW de cómputo de entrenamiento a final de 2026; puesta en marcha de equipos en la Austin Fab en 2027 (P4) | No; por ahora es solo coste (capex e I+D) |

**Conclusión de la sección.** Los nuevos negocios ya consumen recursos visibles, pero Tesla no les asigna ingresos propios en sus cuentas. Lo que consumen:
- **I+D:** 2.761 M$ en Q3 2026, un +69 % interanual (P4).
- **Capex:** 13.014 M$ en los nueve meses de 2026 ([P2](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066775/tsla-20260930.htm)), con una guía de ~20.000 M$ para el año completo (T1).

La señal más tangible de monetización es el número de suscripciones a FSD, y su definición incluye compras por adelantado (S2). Los hitos de los que depende la valoración (escala del robotaxi sin supervisión, unidades de Optimus vendidas, producción de Cybercab) **no tienen todavía una métrica pública** que permita seguirlos trimestre a trimestre. Eso es en sí mismo un riesgo de la tesis.

---

## Registro de cambios v2

Fecha: 2026-10-25. Origen: [05-veredicto.md](05-veredicto.md) §2.3, §3.1 y §5 (prioridad 3, Fase 1), y [02-financieros.md §8.1](02-financieros.md). Fuentes nuevas en `fuentes/nuevas_fase1_v2.md`. `fuentes/fuentes.md` no se ha modificado.

| Ítem del veredicto | Dónde | Cambio |
|---|---|---|
| **FAIL-1** "1.º integrador BESS según Wood Mackenzie" | §2, fila Energía | Sustituido por "Tesla y Sungrow ocupan los dos primeros puestos, sin orden público", con la nota de prensa de Wood Mackenzie como fuente primaria (N1), que tampoco ordena el 1.º y el 2.º. Se añade el liderazgo en Norteamérica (N1) y la caída de cuota de los tres primeros. Se mantiene Benchmark 2.º (S8) |
| **FAIL-2** "Sungrow 2.º" | §3, Almacenamiento | Sustituido por "comparte los dos primeros puestos; 1.ª en Europa" (N1). BYD 3.º confirmado en N1. Se documenta y descarta la fuente secundaria (SolarQuarter) que daba Sungrow 1.º y Tesla 2.º, porque contradice a N1 |
| 02 D4 · caja 45.400 | §1.2, §2 | 45.447 M$ (17.853 + 27.594; P2) |
| 02 D3 · deuda y caja con fechas mezcladas | §1.2, §2 | Caja 45.447 y deuda contable 9.523 (1.387 + 8.136), **ambas a 30-sep-2026**; caja neta 35.924 (02 §5). Los 8.180 M$ quedan como nota aparte: principal nominal a 31-dic-2025, sin arrendamientos |
| 02 D1 · SBC 1.170 (S2) | §1.2 | 1.165 M$ (P4). S2 queda como contraste. También la I+D: 2.761 (P4) en vez de 2.760 (S2) |
| 02 D2 · capex 9M 13.010 (S2) | §1.2, §5 | 13.014 M$ (P2) |
| 02 D6 · "beneficio neto GAAP 787" | §1.2 | "787 M$ atribuible a accionistas comunes; 804 M$ total" (P4) |
| 02 D7 · marcas "solo secundaria" en FY2025 | Leyenda, §1.1, §4.3 | Retiradas de ingresos por línea, créditos, BB total, beneficio operativo y beneficio neto FY2025, que ahora remiten a 02. **Se mantienen** en el BB por línea (automoción, energía, servicios), la nota geográfica de China y xAI, porque 02 §1.2 no los confirma |
| D-4 / 3(c) · guía de capex 2026 | §2 Balance, §4.6, §5 | ~20.000 M$ según el CFO en la call de 3T26, con cita literal ([T1](https://www.fool.com/earnings/call-transcripts/2026/10/22/tesla-tsla-q3-2026-earnings-call-transcript/), re-verificada el 25-oct-2026). Las guías anteriores (S5 >20.000; T10/S2 >25.000) se marcan como sustituidas. Se añaden el Q4 implícito (~7.000 M$), la línea de crédito de 30.000 M$ y la exclusión de la Terafab |
| D-5 / W11 · margen de Energía del 33,1 % | §1.2 nota ¹, §2, §4.3 | Matizado: incluye devoluciones arancelarias y ajustes de garantía reembolsados por el proveedor, según el CFO (T1). Sube desde el 20,4 % de 2T26. El efecto no está cuantificado: **SIN VERIFICAR**. No debe extrapolarse |
| 02 D5 / 3(f) · PER ~327x | §5 | Marcado como **DESFASADO** (anterior a los resultados de 3T26). Remite a 03 §7 para la cifra vigente y a 05 §3.1 por las distintas definiciones. No se calcula un PER nuevo. La capitalización y el precio también se etiquetan como previos a resultados |
| D-1 / 3(g) · BYD 2,26 M | §3, §2 | Aclarado con el comunicado de BYD a la HKEX (N2): 2.256.714 son **turismos BEV, sin PHEV**. El total NEV es 4.602.436 (BEV + 2.288.709 PHEV + 57.013 comerciales). La comparación con Tesla es homogénea (BEV), con el matiz ventas frente a entregas |
| Nota ¹ de 05 §2.1 (ubicaciones imprecisas, no FAIL) | §4.1, §4.5 | SpaceX: "notas" → "estado de flujos" (P3). Garantías: "Note 1" → tabla "Accrued warranty" (P2) |
| Resumen y cifras de cabecera | Cabecera | **01 no tiene un resumen de 5 líneas** (no lo tenía en la v1), así que no hay nada que armonizar. La cabecera solo lleva fechas: se añade la fecha de la v2. La "Lectura" de §1.2 se completa con el matiz del margen de Energía |

---

## Registro de cambios v3

Fecha: 2026-10-25. Origen: [05-veredicto-v2.md](05-veredicto-v2.md) §2.1 (M3), §5 (observaciones cosméticas) y §8 (prioridad 3, Fase 1). Todas las cifras derivadas de 01 se recalculan ahora en `scripts/fase1_cifras.py`, con un único redondeo half-up. No hay fuentes nuevas: no se crea `fuentes/nuevas_fase1_v3.md`.

| Ítem del veredicto | Dónde | Cambio |
|---|---|---|
| **M3** · Servicios y otros, var. FY25 | §1.1 | **+19,0 % → +18,9 %** (12.530 / 10.534 − 1 = 18,9482 %; salida de `fase1_cifras.py`). Coincide con 02 |
| M3 · revisar otros porcentajes con el mismo problema | Todo 01 | `fase1_cifras.py` recalcula 33 cifras derivadas de 01 (variaciones, márgenes, pesos, cocientes de §1.1, §1.2, §3, §4 y §5). **Ninguna otra difiere** del valor publicado. Casos límite comprobados: China H1 2026 = 17,5000 % (8.859 / 50.623); créditos / BO FY25 = 45,76 % (45,8 % en la referencia a 02 y "46 %" en el texto, ambos correctos). No se recalculan los márgenes de automoción de 3T26 (18,5 % / 18,1 %) ni el +67 % de FSD, porque 01 no cita sus numeradores y denominadores: vienen literales de P4 |
| §5 cosmético · "423,7 M (~12 % del capital)" sin base | §4.1 | Se indica la base: **12,0 %** del capital previo a la emisión (3.529.014.042 = 3.952.757.946 − 423.743.904) y **10,7 %** de la portada del 10-Q 3T26 (3.952.757.946 a 15-oct-2026, que ya incluye las acciones del plan según 02 §5.1). Cálculo en `fase1_cifras.py`. Matiz: "capital previo" se define como portada menos el plan, no como la cifra de una fecha concreta anterior a la emisión, porque entre ambas fechas hubo otros movimientos (p. ej. el ejercicio de opciones de 2018) |
| Cabecera | Cabecera | Añadida la fecha de la revisión v3 |
