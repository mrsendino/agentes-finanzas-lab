# 01 — Negocio de AMD (Advanced Micro Devices, AMD): modelo, ventajas, competencia, riesgos y opcionalidad

**Fecha del análisis:** 2026-10-31 · **Último ejercicio fiscal:** FY2025 (cerrado el 27-dic-2025) · **Último trimestre con 10-Q:** Q2 2026 (cerrado el 27-jun-2026)
**Alcance:** descriptivo. No contiene recomendaciones de compra o venta.

**Aviso de calendario.** AMD publicará Q3 2026 el **3-nov-2026**, después de la fecha de este documento ([S5](https://ir.amd.com/news-events/press-releases/detail/1300/amd-to-report-fiscal-third-quarter-2026-financial-results), visto solo en resultados de búsqueda). Las cifras trimestrales de aquí son de Q2 2026; la única referencia a Q3 es la guía de la propia AMD.

**Cómo se citan las fuentes.** Cada cifra lleva un ID (P = primaria, S = secundaria) detallado en `/fuentes/fuentes.md`, con documento, sección y URL. Todos los porcentajes, sumas y ratios salen de `scripts/fase1_mezcla.py` (salida en `data/fase1_mezcla.csv`) y se copian tal cual, cambiando solo el punto decimal por coma.
- **SIN VERIFICAR**: no se pudo contrastar con ninguna fuente.
- **solo secundaria**: el dato procede únicamente de una fuente secundaria.

**Posible conflicto de interés.** Este documento lo redacta un modelo de IA (Claude) desarrollado por Anthropic. Anthropic es cliente de AMD (acuerdo de hasta 2 GW) y AMD se ha comprometido a invertir en ella (§5). Las cifras de ese acuerdo se toman solo de las fuentes de AMD (P16, P6) y no se valoran de forma distinta a los acuerdos con OpenAI o Meta.

---

## 1. Modelo de negocio por segmento

**La segmentación ha cambiado.** Desde Q1 2025, AMD reporta **tres segmentos**, no cuatro: Client y Gaming se fusionaron en un único segmento, **Client and Gaming**, y los datos anteriores se reexpresaron ([P1](https://www.sec.gov/Archives/edgar/data/2488/000000248826000018/amd-20251227.htm), Item 1 "Our Business" y Note 4). AMD sigue publicando por separado los **ingresos** de Client y de Gaming, pero **no su resultado operativo**. El 10-Q de Q2 2026 mantiene la misma estructura ([P2](https://www.sec.gov/Archives/edgar/data/2488/000000248826000123/amd-20260627.htm), Note 4).

| Segmento | Qué incluye (P1, Item 1) |
|---|---|
| **Data Center** | Aceleradores de IA (Instinct), CPU de servidor (EPYC), GPU, APU, DPU, tarjetas de red de IA (Pensando), FPGA y SoC adaptativos para centros de datos |
| **Client and Gaming** | CPU y APU de sobremesa y portátil (Ryzen), chipsets, GPU discretas (Radeon) y SoC semipersonalizados (consolas PlayStation 5 y Xbox Series, Steam Machine de Valve) |
| **Embedded** | CPU, APU, FPGA (procedentes de Xilinx), módulos SOM y SoC adaptativos para industria, automoción, defensa, comunicaciones, salud… |
| **All Other** (no es segmento) | Gastos que la dirección no asigna: amortización de intangibles de adquisiciones, SBC, costes de adquisición y reestructuración |

AMD es **fabless**: no tiene fábricas de obleas. Diseña y subcontrata la fabricación a TSMC (todo lo de 7 nm o menos), GlobalFoundries, UMC y Samsung, y el ensamblaje y test a terceros en China, Malasia y Taiwán (P1, Item 1 "Manufacturing" e Item 1A). Vende a hiperescaladores, OEM, ODM y distribuidores, en general **por pedido y sin compromisos mínimos de compra** (P1, Item 1 "Sales and Marketing").

### 1.1 Último ejercicio fiscal: FY2025

Fuente: [P1](https://www.sec.gov/Archives/edgar/data/2488/000000248826000018/amd-20251227.htm), Note 4 Segment Reporting (tabla de segmentos), contrastada con la tabla del Item 7. Porcentajes: `fase1_mezcla.py`.

| Segmento | Ingresos FY2025 (M$) | Peso en ingresos | Var. vs FY2024 | Resultado operativo FY2025 (M$) | Peso en res. op. de segmentos¹ | Margen op. del segmento |
|---|---|---|---|---|---|---|
| Data Center | 16.635 | 48,0 % | +32,2 % (12.579) | 3.603 | 46,8 % | 21,7 % |
| Client and Gaming | 14.550 | 42,0 % | +50,8 % (9.649) | 2.855 | 37,1 % | 19,6 % |
| · Client | 10.640 | 30,7 % | +50,8 % (7.054) | no publicado | — | — |
| · Gaming | 3.910 | 11,3 % | +50,7 % (2.595) | no publicado | — | — |
| Embedded | 3.454 | 10,0 % | −2,9 % (3.557) | 1.243 | 16,1 % | 36,0 % |
| All Other | — | — | — | −4.007 | — | (11,6 % de los ingresos) |
| **Total** | **34.639** | 100 % | **+34,3 %** (25.785) | **3.694** | — | **10,7 %** (GAAP) |

¹ Sobre la suma de los tres segmentos antes de All Other: 7.701 M$ (script).

Otros datos de FY2025:
- **Margen bruto GAAP:** 50 %. Incluye ~440 M$ netos de cargos de inventario por el control de exportación del MI308 a China: ~800 M$ en Q2 2025, de los que se revirtieron ~360 M$ en Q4 2025 (P1, Item 7 Overview).
- **Beneficio neto GAAP:** 4.335 M$; BPA diluido 2,65 $ (P1, cuenta de resultados). Incluye un **beneficio fiscal de 853 M$** por la liberación de posiciones fiscales inciertas (P1, Item 7 "Income Tax"), que no es recurrente.
- **No-GAAP (definición de AMD):** resultado operativo 7.768 M$, beneficio neto 6.831 M$, BPA 4,17 $ ([P5](https://www.sec.gov/Archives/edgar/data/2488/000000248826000014/q42025991.htm), tabla anual). Ver §4.6 para la diferencia con GAAP.
- **Flujo de caja operativo (operaciones continuadas):** 6.493 M$; **capex:** 974 M$. El FCF aproximado propio es 5.519 M$ (script; no es la cifra de FCF de AMD).
- **Caja e inversiones a corto plazo:** 10.600 M$ ("$10.6 billion"); **principal de deuda:** 3.300 M$ ("$3.3 billion") (P1, Item 7 Overview).
- **Plantilla:** ~31.000 empleados (P1, Item 1 "Human Capital").

**Ingresos por ubicación de facturación del cliente** (P1, Note 4; pesos del script): Estados Unidos 11.363 M$ (32,8 %), **China incl. Hong Kong 7.751 M$ (22,4 %)**, Taiwán 5.186 M$ (15,0 %), Singapur 4.284 M$ (12,4 %), otras regiones 6.055 M$ (17,5 %). Es la ubicación de **facturación**, no del usuario final: buena parte de lo facturado en Taiwán o China puede ser de ODM que ensamblan para clientes de otros países (lectura propia; AMD no da la cifra por usuario final, **SIN VERIFICAR**).

### 1.2 Último trimestre disponible: Q2 2026

Fuente: [P2](https://www.sec.gov/Archives/edgar/data/2488/000000248826000123/amd-20260627.htm), Note 4 Segment Reporting. Q1 2026 se obtiene como 6 meses menos Q2 (script); coincide con los 10.253 M$ de Q1 2026 de [P6](https://www.sec.gov/Archives/edgar/data/2488/000000248826000121/q22026991.htm).

| Segmento | Q2 2026 (M$) | Peso | Var. vs Q2 2025 | Var. vs Q1 2026 | Res. op. Q2 2026 (M$) | Peso en res. op. de segmentos² | Margen op. |
|---|---|---|---|---|---|---|---|
| Data Center | 6.718 | 58,2 % | +107,3 % (3.240) | +16,3 % (5.775) | 2.103 | 68,5 % | 31,3 % |
| Client and Gaming | 3.841 | 33,3 % | +6,1 % (3.621) | +6,5 % (3.605) | 582 | 19,0 % | 15,2 % |
| · Client | 3.062 | 26,5 % | +22,5 % (2.499) | +6,1 % (2.885) | — | — | — |
| · Gaming | 779 | 6,8 % | **−30,6 %** (1.122) | +8,2 % (720) | — | — | — |
| Embedded | 977 | 8,5 % | +18,6 % (824) | +11,9 % (873) | 386 | 12,6 % | 39,5 % |
| All Other | — | — | — | — | −1.081 | — | (9,4 % de los ingresos) |
| **Total** | **11.536** | 100 % | **+50,1 %** (7.685) | — | **1.990** | — | **17,3 %** |

² Sobre 3.071 M$ (script).

Cómo leer la comparación con Q2 2025: en ese trimestre Data Center tuvo un **resultado operativo de −155 M$** por el cargo del MI308 (P2, Item 2). El +107,3 % de ingresos es real, pero el salto de margen se compara con una base deprimida.

Otros datos de Q2 2026:
- **Margen bruto GAAP:** 54 %, frente al 40 % de Q2 2025 (P2, Item 2).
- **Beneficio neto GAAP:** 2.297 M$ (P2). Incluye **598 M$ de "otros ingresos"**, sobre todo plusvalías no realizadas de participaciones que empezaron a cotizar en el trimestre (P2, Item 2 "Other income"). No es recurrente.
- **No-GAAP:** resultado operativo 3.094 M$; margen bruto 56 % (P6).
- **6 meses de 2026:** flujo de caja operativo 5.321 M$, capex 1.197 M$ (P2, estado de flujos). FCF aproximado propio: 4.124 M$ (script).
- **Caja e inversiones a corto plazo a 27-jun-2026:** 13.100 M$ ("$13.1 billion"). **Deuda contable:** 875 M$ corrientes y 2.351 M$ no corrientes (P2, balance). Después del trimestre, AMD emitió **4.750 M$ en bonos** con vencimientos de 2029 a 2036 ([P14](https://www.sec.gov/Archives/edgar/data/2488/000119312526354029/d142696d8k.htm), 17-ago-2026).
- **Ventas por ingresos reconocidos a lo largo del tiempo** (productos a medida y servicios de desarrollo): ~4 % en Q2 2026, frente al 12 % de Q2 2025 (P2, nota de ingresos). Encaja con la caída de los ingresos semipersonalizados de consolas.
- **Guía de Q3 2026:** ingresos de ~13.000 M$ ± 300 M$ y margen bruto no-GAAP de ~56 % (P6, "Current Outlook"). Contra los 9.246 M$ de Q3 2025 (P5), el punto medio supone +40,6 % (script; AMD dice "approximately 41%").

**Lectura.** AMD ha pasado a ser, sobre todo, una empresa de centro de datos: Data Center aporta el 58,2 % de los ingresos y el 68,5 % del resultado operativo de los segmentos en Q2 2026, frente al 48,0 % y el 46,8 % de FY2025. Client crece por unidades (+34 % de unidades de procesadores en Q2 2026, con un precio medio −6 %; P2, Item 2). Gaming cae con fuerza por el ciclo de consolas. Embedded se recupera tras dos años de caída. AMD no separa en sus cuentas cuánto de Data Center es **GPU Instinct** y cuánto **CPU EPYC** (**SIN VERIFICAR**; ver §5).

---

## 2. Ventajas competitivas y sus límites

| Ventaja | Evidencia | Límites y durabilidad |
|---|---|---|
| **CPU x86 de servidor (EPYC)** | Cuota de unidades x86 de servidor del **34,5 %** en Q2 2026 según Mercury Research ([S3](https://basic-tutorials.com/news/cpu-market-share-q2-2026-amd-breaks-the-30-percent-mark-intel-loses-ground-across-the-board/), 24-ago-2026; **solo secundaria**). La cuota por **ingresos** (titulares de prensa hablan de ~46 %) queda **SIN VERIFICAR**: no se pudo abrir ninguna fuente. AMD tiene el objetivo de superar el 50 % de cuota de ingresos ([P17](https://ir.amd.com/news-events/press-releases/detail/1266/amd-unveils-strategy-to-lead-the-1-trillion-compute-market-and-accelerate-next-phase-of-growth)). La dirección dijo en Q1 2026 que espera un mercado de CPU de servidor de más de 120.000 M$ en 2030 ([S1](https://www.fool.com/earnings/call-transcripts/2026/05/06/amd-amd-q1-2026-earnings-call-transcript/), **solo secundaria**) | **Alta a medio plazo** frente a Intel, que ha perdido cuota durante años. **Límite:** el rival que más crece no es x86, sino Arm, incluidos los chips propios de los hiperescaladores. El 10-K reconoce que "some of our customers are internally developing their own data center microprocessor products" (P1, Item 1 "Competition") |
| **CPU de cliente (Ryzen)** | Client +50,8 % en FY2025, con +31 % de unidades y +15 % de precio medio (P1, Item 7). Cuota x86 del 34,9 % en sobremesa y del 28,9 % en portátil en Q2 2026 (S3, **solo secundaria**) | **Media.** Es un mercado cíclico y muy sensible al precio de la memoria: la dirección prevé menos envíos de PC en 2S 2026 por el coste de memoria y componentes (S1, **solo secundaria**). Intel sigue teniendo la mayoría del mercado. Los PC con Arm son una amenaza que el 10-K cita sin cuantificar |
| **GPU de centro de datos (Instinct) y ROCm** | Clientes que despliegan MI350 en 2025: "large hyperscale customers, OEMs and ODMs" (P1, Item 1). Acuerdos de hasta 6 GW con OpenAI y con Meta y de hasta 2 GW con Anthropic (§5). Helios, la plataforma rack-scale, se lanzó en Q2 2026 (P6). La pila de software abierta ROCm se presenta como alternativa a la de Nvidia (P1, Item 1) | **Por demostrar.** La ventaja de Nvidia en software y ecosistema no se mide en ningún documento de AMD; la madurez relativa de ROCm queda **SIN VERIFICAR**. Los grandes acuerdos llevan **warrants** de hasta 160 M de acciones cada uno: AMD ha tenido que **ceder capital para conseguir la demanda** (§5). Es una señal de interés del cliente y, a la vez, de que la posición de AMD no basta por sí sola |
| **Xilinx: FPGA y SoC adaptativos** | Adquirida en febrero de 2022 por **48.800 M$** de contraprestación total ([P15](https://www.sec.gov/Archives/edgar/data/2488/000000248823000047/amd-20221231.htm), nota de adquisiciones). Embedded tiene el mayor margen operativo del grupo: 36,0 % en FY2025 y 39,5 % en Q2 2026 (script). AMD aspira a más del 70 % de cuota de ingresos en computación adaptativa (P17) | **Alta en margen, baja en crecimiento.** Embedded pasó de 5.321 M$ en FY2023 a 3.454 M$ en FY2025 (P1, Note 4) por el exceso de inventario de sus clientes. Hoy es solo el 8,5 % de los ingresos. Compite con Altera, Lattice y Microsemi (P1, Item 1) |
| **Semipersonalizados (consolas)** | AMD dice ser "the market share leader in semi-custom game console products" (P1, Item 1 "Competition") | **Cíclica.** Gaming −30,6 % en Q2 2026 por la caída de los ingresos semipersonalizados (P2). La dirección esperaba que gaming cayera más de un 20 % en 2S 2026 frente a 1S (S1, **solo secundaria**) |
| **Modelo fabless con TSMC** | Acceso a los nodos más avanzados sin invertir en fábricas: capex de solo 974 M$ en FY2025, el 2,8 % de los ingresos (P1, flujos; % del script) | **Ventaja de capital, riesgo de suministro.** "We rely on TSMC for the production of all wafers for microprocessor and GPU products at 7 nanometer (nm) or smaller nodes" (P1, Item 1A). Ver §4.3 |
| **Adquisiciones de sistemas y software** | ZT Systems (marzo de 2025; 4.400 M$ de contraprestación total, P2 Note 5): AMD se quedó con el diseño y vendió la fabricación a Sanmina en octubre de 2025 por 2.400 M$ en efectivo, 1,2 M de acciones de Sanmina y hasta 450 M$ adicionales condicionados (P1, Item 7). Pensando (mayo de 2022; ~1.900 M$, P15) aporta DPU y tarjetas de red de IA. World Labs (anunciada el 28-sep-2026; ~8.200 M$ en acciones, [P9](https://www.sec.gov/Archives/edgar/data/2488/000000248826000182/amd-20260926.htm)) aporta modelos de "mundo" para robótica e IA física, y su cofundadora Fei-Fei Li se incorpora como EVP y chief scientist ([S4](https://techcrunch.com/2026/09/28/amd-will-acquire-fei-fei-lis-world-labs-for-8-2-billion/)) | **Por demostrar.** Estas compras construyen la oferta "full-stack" (CPU + GPU + red + rack + software) que necesita para competir con Nvidia. World Labs no tiene ingresos publicados y se paga con acciones (dilución, §6). Cierre previsto antes de fin de 2026, sujeto a aprobación regulatoria (S4) |

---

## 3. Competidores por segmento

| Segmento / producto | Competidores (P1, Item 1 "Competition", salvo indicación) | Datos |
|---|---|---|
| **GPU y aceleradores de centro de datos** | **Nvidia** (líder). Aceleradores propios de los clientes: "some of our customers are internally developing their own … accelerator products" (P1). ASIC a medida diseñados con terceros como Broadcom o Marvell: el 10-K los cita como competidores en Embedded, no en Data Center; su peso en IA queda **SIN VERIFICAR** en esta fase | Nvidia ingresó **215.938 M$** en su ejercicio FY2026 (cerrado el 25-ene-2026; [P10](https://data.sec.gov/api/xbrl/companyconcept/CIK0001045810/us-gaap/Revenues.json)), **6,23 veces** los ingresos totales de AMD en FY2025 (script). La cuota de AMD en GPU de IA: **SIN VERIFICAR** |
| **CPU de servidor** | **Intel**; CPU Arm de terceros y de los propios hiperescaladores (P1) | Intel ingresó 52.853 M$ en FY2025 ([P11](https://data.sec.gov/api/xbrl/companyconcept/CIK0000050863/us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax.json)), 1,53 veces AMD (script), pero con más negocios además de CPU. Cuota de AMD: 34,5 % de las unidades x86 de servidor (S3, **solo secundaria**) |
| **Redes de IA (DPU, NIC)** | Nvidia e Intel (P1) | Sin datos de cuota (**SIN VERIFICAR**) |
| **CPU de PC** | **Intel**; PC con Arm (P1). Qualcomm y Apple no se citan por su nombre en este apartado del 10-K | AMD: 34,9 % en sobremesa y 28,9 % en portátil (S3, **solo secundaria**) |
| **GPU discretas de PC** | **Nvidia** ("the discrete GPU market share leader") e Intel (P1) | — |
| **Consolas** | AMD es el líder en semipersonalizados de consola (P1) | — |
| **Embedded / FPGA** | Altera, Lattice, Microsemi; fabricantes de ASSP como Broadcom, Marvell, Analog Devices, Texas Instruments, NXP, Qualcomm y Nvidia; ASIC; Intel en CPU embebidas (P1) | — |

**Lectura.** AMD es el **segundo proveedor** en sus dos mercados principales: CPU x86, donde va ganando cuota, y GPU de IA, donde parte de muy atrás. En GPU de IA, Nvidia es más de seis veces más grande en ingresos totales. Además, el cliente más grande (el hiperescalador) es también un competidor potencial con chips propios.

---

## 4. Riesgos principales

### 4.1 Concentración de clientes (creciente)
- **Hoy:** ningún cliente superó el 10 % de los ingresos en FY2025 ni en FY2024. En FY2023, un cliente de Client and Gaming supuso el **18 %** (P1, Note 4). Su identidad no se publica (**SIN VERIFICAR**; por el tipo de segmento podría ser un fabricante de consolas, pero es una conjetura). Al cierre de FY2025, un cliente concentraba ~11 % de las cuentas por cobrar (P1, nota de concentración de crédito).
- **Mañana:** OpenAI y Meta han pedido cada uno hasta 6 GW y Anthropic hasta 2 GW (§5). Si se cumplen, **uno o dos clientes de IA superarán con facilidad el 10 %** de los ingresos (lectura propia). El 10-K ya lo advierte: "We depend on a small number of customers for a substantial portion of our business" (P1, Item 1A; repetido en P2).
- **Cancelaciones:** en general, los clientes pueden anular pedidos estándar más de 30 días antes del envío sin penalizaciones significativas (P1, Item 1A). Lo **vinculante** de los grandes acuerdos es solo el **primer GW** (§5).

### 4.2 Controles de exportación y China
- En FY2025, el **22,4 %** de los ingresos se facturó en China incl. Hong Kong (script con P1, Note 4).
- **MI308:** la licencia exigida desde abril de 2025 provocó ~800 M$ de cargos en Q2 2025. AMD obtuvo algunas licencias, empezó a enviar a finales de 2025 y revirtió ~360 M$ (P1, Item 7). Funcionarios de EE. UU. esperan cobrar **el 15 % de los ingresos** de esas ventas, pero no hay regulación publicada (P1, Item 7).
- **MI325:** licencias concedidas en febrero de 2026 para ciertos clientes chinos. Los envíos deben pasar primero una inspección en EE. UU. y pagar allí un **arancel del 25 %**. AMD no sabe si China permitirá su importación (P2, Item 1A).
- En la call de Q1 2026, la CFO dijo que los ingresos de China "no fueron materiales" (S1, **solo secundaria**).
- AMD tiene participaciones en joint ventures con THATIC (Hygon), incluidas en la Entity List desde 2019 (P3, Item 1A).

### 4.3 Suministro: TSMC, empaquetado, memoria y componentes de rack
- **TSMC** fabrica todas las obleas de CPU y GPU de 7 nm o menos (P1, Item 1A). Riesgo geopolítico en Taiwán y de capacidad en empaquetado avanzado: la cuantificación de esta última queda **SIN VERIFICAR** (AMD no publica su asignación de capacidad).
- **Compromisos de compra incondicionales:** **30.276 M$** a 27-jun-2026 (17.386 M$ para el resto de 2026), **2,48 veces** los ~12.200 M$ de fin de 2025 (script con P1, Item 7, y P2, Note 10). Incluyen obleas, sustratos, componentes y **capacidad de cómputo en la nube** contratada a proveedores cloud. Si la demanda se enfría, son costes fijos.
- **Rack-scale:** Helios depende de muchos componentes de terceros (memoria, red, refrigeración, integración). Si falta uno, se retrasan los envíos aunque los chips de AMD estén listos (P2, Item 1A, riesgo nuevo en 2026).
- **Memoria:** la dirección cita la inflación del coste de memoria como freno para PC y consolas (S1, **solo secundaria**).

### 4.4 Ciclicidad
Los semiconductores son cíclicos y el historial de AMD lo muestra:
- **Embedded:** −2,9 % en FY2025, tras caer de 5.321 M$ (FY2023) a 3.557 M$ (FY2024) (P1, Note 4).
- **Gaming:** de 6.212 M$ en FY2023 a 2.595 M$ en FY2024; de vuelta a 3.910 M$ en FY2025; −30,6 % en Q2 2026 (P1, P2).
- **Estacionalidad:** los ingresos suelen ser mayores en el segundo semestre (P1, Item 1 "Seasonality").
- El mayor riesgo cíclico es ahora **el gasto en infraestructura de IA**: concentrado en pocos clientes, financiado en parte con deuda y con capital de terceros, y del que depende el 58,2 % de los ingresos actuales (lectura propia).

### 4.5 Ejecución en IA
- **El calendario es exigente.** MI450 y Helios empiezan a enviarse en Q3 2026, con una rampa fuerte en Q4 2026 y en 2027 (S1, **solo secundaria**). AMD promete una cadencia anual de producto (P1, Item 1).
- **Los warrants son a la vez una prueba y una presión.** No se activa ningún tramo hasta que se entregue el primer GW. A 27-jun-2026 **no había ningún tramo consolidado** (P2, Note 11), lo que confirma que los envíos de MI450 a escala aún no habían empezado al cierre de Q2.
- **AMD está financiando parte de la demanda**, con cuatro mecanismos (P2, notas de compromisos y garantías; P16):
  - garantías sobre arrendamientos de centros de datos de "socios comerciales", con una exposición máxima de **4.100 M$** a plazos de hasta 15 años, que "may be issued in exchange for warrants";
  - compromisos de inversión de hasta **5.000 M$** contraídos después del 27-jun-2026. El 10-Q no nombra la contraparte, pero coincide con el compromiso de invertir hasta 5.000 M$ en Anthropic anunciado el 22-jul-2026 (P16). Que sean el mismo compromiso es probable, pero **SIN VERIFICAR**;
  - arrendamientos de centros de datos firmados y aún no iniciados por **4.500 M$**, más otros **9.500 M$** firmados después del trimestre;
  - compras de capacidad de cómputo en la nube (§4.3).

  Esta red de compromisos cruzados (AMD invierte en clientes, les avala alquileres, les cede warrants y les compra capacidad) aumenta el riesgo si el ciclo de IA se frena (lectura propia).

### 4.6 Contabilidad de adquisiciones: GAAP frente a no-GAAP
- **All Other** restó 4.007 M$ en FY2025, el 11,6 % de los ingresos: 2.254 M$ de **amortización de intangibles** y 1.638 M$ de **SBC** (P1, Note 4). Solo la amortización equivale al **61,0 % del resultado operativo GAAP** (script).
- El resultado operativo **no-GAAP** (7.768 M$) es **2,1 veces** el GAAP (3.694 M$), con una diferencia de 4.074 M$. En beneficio neto, la diferencia es de 2.496 M$ (script con P1 y P5).
- **Fondo de comercio + intangibles:** el **54,4 % del activo** a fin de 2025 y el **48,7 %** a 27-jun-2026 (script con P1 y P2). Proceden sobre todo de Xilinx, con 48.800 M$ de contraprestación (P15); el reparto exacto por adquisición queda **SIN VERIFICAR** en esta fase. AMD no registró deterioros en FY2025 (P1, Item 7, "Goodwill"), pero un deterioro es un riesgo listado (P2, Item 1A).
- **Lectura:** la amortización es un coste contable de compras pasadas, no un gasto de caja. **La SBC sí es un coste económico real** (§6), y el no-GAAP de AMD la excluye. La retribución variable de la dirección se mide en parte con BPA no-GAAP (§6).
- Los beneficios GAAP recientes incluyen partidas no recurrentes: 853 M$ de beneficio fiscal en FY2025 y 598 M$ de otros ingresos en Q2 2026 (§1).

---

## 5. Qué parte del valor depende de negocios que aún no generan ingresos significativos

**Contexto de mercado:** cotización y capitalización no consultadas en esta fase (**SIN VERIFICAR**; las calculará la Fase 3). Por eso esta sección no dice qué porcentaje del precio corresponde a cada negocio. Lo que sí se puede separar es **lo que ya factura** de **lo que son compromisos** y de **lo que son expectativas**.

### 5.1 Lo que ya factura (Q2 2026, P2)
- **Data Center: 6.718 M$ en el trimestre**, impulsado por "AMD EPYC processors and AMD Instinct MI350 Series GPUs" (P2, Item 2). **AMD no desglosa CPU y GPU**: cuánto de esa cifra es IA queda **SIN VERIFICAR**. Las GPU de 2025-1S 2026 son MI350/MI355; **la familia MI450, objeto de los grandes acuerdos, todavía no había generado ingresos a escala a 27-jun-2026** (ningún tramo de warrant consolidado; P2, Note 11).
- **Client, Gaming y Embedded: 4.818 M$** en el trimestre (3.841 + 977; suma del script). Es negocio maduro y cíclico.

### 5.2 Compromisos firmados (con su letra pequeña)

| Contraparte | Qué está firmado | Qué es vinculante | Contrapartida de AMD | Calendario | Fuente |
|---|---|---|---|---|---|
| **OpenAI** | Hasta 6 GW de GPU Instinct en varias generaciones; el 1.er GW con MI450 | **Solo el 1.er GW** ("binding commitment to purchase … the initial one (1) gigawatt") | Warrant de hasta **160 M de acciones** a 0,01 $. Se consolida por tramos ligados a GW comprados **y** a precios de la acción de AMD que escalan hasta **600 $** en el último tramo, más umbrales de "stock performance" y condiciones técnicas y comerciales antes de ejercerlo. Vence el 5-oct-2030 | Despliegue del 1.er GW desde 2S 2026 | [P7](https://www.sec.gov/Archives/edgar/data/2488/000119312525230895/d28189d8k.htm) (Item 1.01 y Ex. 99.1); P1 Note 12; P2 Note 11 |
| **Meta** | Hasta 6 GW; el 1.er GW con una **GPU personalizada basada en MI450** y CPU EPYC "Venice" | **Solo el 1.er GW "equivalente"** | Warrant de hasta **160 M de acciones** a 0,01 $, por tramos según GW comprados y precios de la acción hasta **600 $**; Meta debe cumplir condiciones técnicas y comerciales antes de ejercerlo. Vence el 23-feb-2031 | Envíos del 1.er GW desde 2S 2026 | [P8](https://www.sec.gov/Archives/edgar/data/2488/000000248826000045/amd-20260223.htm) |
| **Anthropic** | Hasta 2 GW de MI450 en racks Helios | No se publica que haya compromiso vinculante (**SIN VERIFICAR**) | **AMD invierte** hasta 5.000 M$ en Anthropic "in the future". La nota no menciona warrant | 1.er GW desde 1S 2027 | [P16](https://ir.amd.com/news-events/press-releases/detail/1292/amd-and-anthropic-announce-strategic-partnership-to-deploy-up-to-2-gigawatts-of-amd-instinct-mi450-series-gpus) |
| **Microsoft, Oracle y otros** | Despliegue de Helios en Azure; Oracle, HUMAIN, Cirrascale, Tensorwave, Vultr citados como clientes de Helios | Volúmenes no publicados (**SIN VERIFICAR**) | — | — | [P6](https://www.sec.gov/Archives/edgar/data/2488/000000248826000121/q22026991.htm), Recent Highlights |

**Dilución potencial de los warrants** (script, con 1.632.475.042 acciones en circulación a 29-jul-2026 según P2):
- Los dos warrants suman **320 M de acciones**, el **19,6 %** de las acciones en circulación.
- Si se ejercieran por completo, los nuevos titulares tendrían el **16,4 %** del capital ampliado.
- Cada warrant por separado equivale al 9,8 %.

Solo se consolidan si OpenAI y Meta compran hasta 6 GW cada uno **y** la acción sube hasta 600 $. Es decir, la dilución máxima llega solo en el escenario de más ingresos y más precio. Contablemente se registran como pasivo hasta que se cumplan las condiciones para clasificarlos como patrimonio (P2, Note 11).

**Lo que no se sabe:** cuántos ingresos supone un GW. AMD no publica precio por GW ni contenido por GW (**SIN VERIFICAR**; no se estima aquí). La única cifra de la empresa es cualitativa: la CFO dijo que el acuerdo con OpenAI "is expected to deliver tens of billions of dollars in revenue for AMD" (P7, Ex. 99.1), sin plazo concreto.

### 5.3 Expectativas de la dirección (no son compromisos)
- **Objetivos a 3-5 años del Analyst Day** (11-nov-2025, [P17](https://ir.amd.com/news-events/press-releases/detail/1266/amd-unveils-strategy-to-lead-the-1-trillion-compute-market-and-accelerate-next-phase-of-growth)):
  - crecimiento de ingresos >35 % anual (CAGR);
  - Data Center >60 %, e IA de centro de datos >80 %;
  - Client and Gaming y Embedded >10 %;
  - margen operativo no-GAAP >35 %;
  - **BPA no-GAAP >20 $**.
- **Lo que implican esos objetivos** (aritmética del script, no previsiones):
  - un 35 % anual sobre FY2025 llevaría los ingresos a **85.225 M$** en tres años o a **155.322 M$** en cinco;
  - un BPA de 20 $ es **4,8 veces** el BPA no-GAAP de FY2025 (4,17 $) y **7,55 veces** el GAAP (2,65 $).
- **Call de Q1 2026** (S1, **solo secundaria**): "tens of billions" de ingresos de IA de centro de datos en 2027.
- **Call de Q2 2026** (S2, **fuente de baja calidad**): crecimiento de servidor >80 % en 2S 2026 y Data Center más que duplicado en 2027. **Por verificar con la transcripción oficial**; no debe usarse como dato firme.
- **World Labs:** ~8.200 M$ en acciones por una empresa sin ingresos publicados (P9, S4). Es una apuesta de I+D en IA física.

**Conclusión de la sección.** La base que ya factura (Q2 2026 × 4 = 46.144 M$ anualizados, cifra orientativa del script) es sobre todo **EPYC + MI350 + PC**. Las expectativas que separan esa base de los objetivos del Analyst Day dependen de cuatro cosas que **aún no se han demostrado en ingresos**:
1. la rampa de MI450/Helios desde Q3-Q4 2026;
2. que OpenAI y Meta pasen del primer GW vinculante a varios GW opcionales;
3. que Anthropic y otros clientes conviertan intenciones en pedidos;
4. que la tecnología rack-scale funcione a escala.

**Hitos públicos a seguir:**
- la consolidación del **primer tramo** de cada warrant, que AMD tendrá que comunicar y que equivale a "primer GW entregado";
- el comentario de ingresos de IA en las calls, que no es una cifra auditada;
- la evolución de los compromisos incondicionales y de las garantías.

---

## 6. Gobierno corporativo

**Dirección y consejo** ([P4](https://www.sec.gov/Archives/edgar/data/2488/000119312526129057/d85856ddef14a.htm), DEF 14A 2026):
- **Lisa T. Su** es presidenta y CEO desde octubre de 2014 y **presidenta del consejo** (Chair) desde febrero de 2022. Los cargos de Chair y CEO no están separados. El contrapeso es una **consejera independiente principal**, Nora Denzel, en el consejo desde 2014 y en ese papel desde noviembre de 2022.
- El consejo propuso **8 candidatos** para la junta del 13-may-2026. Todos son independientes salvo Su, y se eligen cada año.
- **Cambios posteriores:**
  - Joe Householder se retiró el 19-ago-2026; KC McClure pasa a presidir la Comisión de Auditoría y Finanzas ([P13](https://www.sec.gov/Archives/edgar/data/2488/000000248826000163/amd-20260817.htm)). Si se ha cubierto su puesto: **SIN VERIFICAR**.
  - Con World Labs, Fei-Fei Li se incorporará como EVP y chief scientist (S4).
- Hay acceso de accionistas a la proxy: un 3 % del capital durante 3 años puede proponer candidatos al consejo (P4).

**Retribución ligada a objetivos:**
- **CEO, 2025:** retribución total de **55.161.779 $**, con una ratio de **341 a 1** frente al empleado mediano (161.780 $) (P4, "CEO Pay Ratio").
- **Bonus anual (EIP 2025):** 70 % objetivos financieros (40 % 1S / 60 % 2S) y 30 % hitos estratégicos (tape-outs, lanzamientos, comerciales…) (P4).
- **Incentivo a largo plazo (LTI) de agosto de 2026** ([P12](https://www.sec.gov/Archives/edgar/data/2488/000000248826000115/amd-20260626.htm)):
  - valor objetivo de **36 M$ para Su**, un **75 % en PRSU** y un 25 % en RSU;
  - las PRSU pagan entre el 0 % y el 200 % según el **TSR relativo frente a cada empresa del S&P 500** entre el 15-ago-2026 y el 15-ago-2029, con tope del 100 % si el TSR es negativo;
  - un **extra del 0 %, 25 % o 50 %** depende del **BPA no-GAAP de FY2028** comparado con el objetivo de FY2026;
  - máximo del 250 %.
- **Lectura:** la mayor parte del incentivo depende del **precio relativo de la acción**, lo que alinea a la dirección con el accionista. El componente de beneficio usa **BPA no-GAAP**, que excluye la SBC y la amortización (§4.6). Por eso no penaliza la dilución ni el precio pagado en adquisiciones como World Labs.
- **Participación de la CEO:** Su tenía **4.305.973 acciones** a 19-mar-2026 (P4, tabla de participaciones).

**Dilución por SBC y recompras:**

| Concepto | FY2025 | H1 2026 | Fuente |
|---|---|---|---|
| SBC (cuenta de resultados) | 1.638 M$ (4,7 % de los ingresos) | 990 M$ (Q2: 503 M$, 4,4 % de los ingresos) | P1 Note 12; P2 Note 11; % del script |
| Recompras del programa | 1.316 M$ (12 M de acciones) | 221 M$ (1,1 M de acciones) | P1 flujos y Note 12; P2 Note 11 |
| Recompras / SBC | **0,8x** | **0,22x** | Script |
| Recompras para retenciones fiscales | 607 M$ | 341 M$ | P1, P2 flujos |
| Acciones en circulación | 1.622 → 1.630 M (+0,49 %) | 1.630 → 1.632 M | P1 Note 12; P2 Note 11 |
| Autorización de recompra pendiente | 9.400 M$ | 9.200 M$ | P1, P2 |

**Lectura.** En 2025 las recompras **no compensaron del todo** la emisión por SBC y por la compra de ZT Systems (+9 M de acciones), y en 2026 las recompras casi se han detenido. Además:
- en mayo de 2026 se amplió el plan de acciones en **65 M de acciones**, hasta 153 M; quedan 107 M disponibles (P2, Note 11);
- vienen tres fuentes de dilución potencial: los **warrants** (hasta 320 M de acciones, §5.2), **World Labs** (~8.200 M$ en acciones; el número depende del precio de cierre, P9) y la SBC.

La dilución es un coste relevante para el accionista, y las métricas no-GAAP no lo recogen.

---

## Resumen de cifras SIN VERIFICAR o con fuente débil

| # | Dato | Estado |
|---|---|---|
| 1 | Reparto de Data Center entre GPU Instinct y CPU EPYC | SIN VERIFICAR (AMD no lo publica) |
| 2 | Ingresos por GW de los acuerdos de IA | SIN VERIFICAR (no publicado) |
| 3 | Cuota de AMD en GPU de IA | SIN VERIFICAR |
| 4 | Cuota de AMD por ingresos en CPU de servidor (~46 % según titulares) | SIN VERIFICAR (fuentes no accesibles) |
| 5 | Identidad del cliente del 18 % en FY2023 | SIN VERIFICAR |
| 6 | Ingresos por ubicación del usuario final (no de facturación) | SIN VERIFICAR |
| 7 | Compromiso vinculante en el acuerdo con Anthropic | SIN VERIFICAR |
| 8 | Volúmenes de Microsoft, Oracle y otros clientes de Helios | SIN VERIFICAR |
| 9 | Si el compromiso de inversión de 5.000 M$ del 10-Q es el de Anthropic | SIN VERIFICAR (probable) |
| 10 | Reparto de intangibles y fondo de comercio por adquisición | SIN VERIFICAR |
| 11 | Peso de ASIC a medida (Broadcom, Marvell) en aceleradores de IA | SIN VERIFICAR |
| 12 | Cuota en redes de IA (DPU/NIC) | SIN VERIFICAR |
| 13 | Madurez relativa de ROCm frente a la pila de Nvidia | SIN VERIFICAR |
| 14 | Capacidad de empaquetado avanzado asignada por TSMC | SIN VERIFICAR |
| 15 | Si se ha cubierto la vacante de Householder en el consejo | SIN VERIFICAR |
| 16 | Cotización y capitalización | SIN VERIFICAR (se deja para la Fase 3) |
| — | Comentarios de las calls de Q1 y Q2 2026 (S1, S2) y cuotas de Mercury (S3) | Solo secundaria; S2 de baja calidad |
