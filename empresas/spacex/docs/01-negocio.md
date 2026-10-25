# 01 — Negocio de SpaceX (SPCX): modelo, ventajas, competencia, riesgos y opcionalidad

**Fecha del análisis:** 2026-10-25 · **Último ejercicio fiscal auditado:** FY2025 (cerrado 31-dic-2025, publicado en el folleto de la OPV) · **Último trimestre:** 3T 2026 (cerrado 30-sep-2026)
**Alcance:** descriptivo. No contiene recomendaciones de compra o venta.

**Cómo se citan las fuentes.** Cada cifra lleva su ID de fuente y la sección o tabla. Los IDs (P = primaria SEC EDGAR, S = secundaria) están en [`../fuentes/fuentes.md`](../fuentes/fuentes.md), con URL y fecha de consulta (25-oct-2026). Los documentos base son el **folleto final 424B4 (P2)** y el **10-Q del 3T 2026 (P3)**.
- **SIN VERIFICAR**: no se pudo contrastar con ninguna fuente.
- **Inferencia**: deducción propia a partir de datos primarios; no la afirma la empresa.
- **Cálculo propio**: toda la aritmética (pesos, variaciones, importes implícitos) sale de [`scripts/fase1_segmentos.py`](../scripts/fase1_segmentos.py) y se copia de su salida.

**Advertencias previas.**
1. **Perímetro reexpresado.** SpaceX adquirió xAI (que ya incluía X/Twitter) el 2-feb-2026 como fusión entre entidades bajo control común (P3, Note 1). Por eso todas las cifras históricas, incluidas FY2023-FY2025 y 3T 2025, **incluyen xAI y X** como si siempre hubieran formado parte del grupo. Los crecimientos interanuales comparan el grupo combinado, no la "SpaceX" anterior.
2. **Cambio de nombre del segmento.** El segmento "AI" del folleto pasó a llamarse "Super Intelligence (SI)" en el 10-Q del 3T 2026, con el mismo contenido más Cursor (P3, Note 1). Aquí se usa AI para FY2025 y SI para 2026.
3. **Nota de transparencia.** Este documento lo redacta un modelo de Anthropic. Anthropic aparece en el folleto como cliente de los servicios de cómputo de SpaceX y como competidor del segmento AI (§1.4, §3, §4.3). Me limito a lo que publican los documentos de la SEC y señalo como inferencia lo que no está afirmado.

---

## 1. Modelo de negocio por segmento

SpaceX reporta **tres segmentos operativos y reportables**: Space, Connectivity y SI (P3, Note 18). El CEO (Musk) es el decisor operativo y evalúa cada segmento por su resultado operativo. No hay ingresos entre segmentos: los lanzamientos de satélites Starlink propios no generan ingreso en Space, sino que su coste se capitaliza en los satélites (P3, MD&A "Revenue - Space").

Correspondencia entre las líneas pedidas para el análisis y la segmentación oficial:

| Línea de negocio | Dónde la reporta SpaceX | ¿Ingreso propio publicado? |
|---|---|---|
| Lanzamiento Falcon 9 / Falcon Heavy | Space → *Launch Services* (y parte de *Launch & Development*) | Sí, como subtotal |
| Starship | Space (I+D) y Connectivity (despliega Starlink V3) | **No.** "To date, all Starship launches have been classified as internal" (P3, MD&A Key Business Metrics) |
| Dragon y contratos NASA (tripulación, carga, HLS) | Space → *Launch & Development* ("development of spacecraft and provision of launch and mission services for government agency space programs utilizing Falcon 9, Falcon Heavy, Starship, and Dragon", P3 MD&A) | No por separado (**SIN VERIFICAR** el importe de Dragon o de NASA) |
| Starlink consumo | Connectivity → *Consumer* | Sí |
| Starlink empresa y gobierno | Connectivity → *Enterprise & Government* | Sí, como subtotal conjunto |
| Starshield (defensa) | Connectivity → *Enterprise & Government* (contratos plurianuales reconocidos por avance de costes, P3 MD&A "Revenue - Connectivity") | No por separado (**SIN VERIFICAR**) |
| Directo al móvil (Starlink Mobile) | Connectivity → *Enterprise & Government*: "Enterprise & Government revenue includes revenue from Starlink Mobile service offerings" (P2 Note 3; P3 Note 3) | **Sí factura**, pero sin importe separado (**SIN VERIFICAR**) |
| X (publicidad) | SI → *Advertising* | Sí |
| Grok, Cursor, X Premium, API, datos, cloud | SI → *SI Solutions & Infrastructure* | Sí, como subtotal conjunto; Cursor aporta 608 M$ desde el 14-ago-2026 (P3 MD&A) |

### 1.1 Último ejercicio fiscal: FY2025 (auditado)

Fuente: P2, Note 3 de los estados anuales, "Revenue disaggregated by type and segment" (p. F-23); resultados por segmento en la tabla "Summary Consolidated Financial and Other Data" (p. 26-27) y en el Prospectus Summary (p. 4). Pesos, variaciones y márgenes: cálculo propio (script, bloque 1).

| Segmento / línea | Ingresos FY2025 (M$) | Peso | Var. vs FY2024 | Resultado operativo FY2025 (margen) | EBITDA ajustado FY2025 (margen) |
|---|---|---|---|---|---|
| **Space** | **4.086** | 21,9 % | +7,6 % (3.796) | −657 (−16,1 %) | 653 (16,0 %) |
| · Launch Services | 2.576 | 13,8 % | −0,3 % | — | — |
| · Launch & Development | 1.510 | 8,1 % | +24,6 % | — | — |
| **Connectivity** | **11.387** | 61,0 % | +49,8 % (7.599) | 4.423 (38,8 %) | 7.168 (62,9 %) |
| · Consumer | 7.208 | 38,6 % | +49,2 % | — | — |
| · Enterprise & Government | 4.179 | 22,4 % | +50,9 % | — | — |
| **AI** (xAI + X) | **3.201** | 17,1 % | +22,2 % (2.620) | −6.355 (−198,5 %) | −1.237 (−38,6 %) |
| · Advertising | 1.844 | 9,9 % | +6,7 % | — | — |
| · AI Solutions & Infrastructure | 1.357 | 7,3 % | +52,1 % | — | — |
| **Total** | **18.674** | 100 % | +33,2 % (14.015) | −2.589 (−13,9 %) | 6.584 (35,3 %) |

El EBITDA ajustado es una medida no GAAP: excluye amortizaciones, compensación en acciones, reestructuración y deterioros (P3, "Non-GAAP Financial Measures"). En FY2025 la diferencia con el resultado operativo es grande en los tres segmentos.

Datos operativos FY2025 (P2, MD&A Key Business Metrics y tabla de p. 26-27):
- **Lanzamientos Falcon:** 165, de ellos 43 para clientes y 122 internos (P2, nota (1) de p. 87). La tabla resumen da 170 "launches" porque suma también los vuelos de Starship.
- **Suscriptores Starlink (consumo):** 8,9 M a 31-dic-2025, frente a 4,4 M un año antes (+102,3 %, cálculo propio). **ARPU** de 81 $/mes, frente a 91 $ en FY2024 (−11,0 %).
- **Cómputo instalado ("nameplate compute draw"):** 0,8 GW a cierre de 2025 (P2, p. 27).
- **Capex FY2025:** Space 3.832 M$, Connectivity 4.178 M$, AI 12.727 M$ (P2, Prospectus Summary p. 4).
- **Backlog** a 31-dic-2025: 28.377 M$ (P2, Note 3).

**Lectura FY2025.** Starlink era ya el negocio principal: 61,0 % de los ingresos y el único segmento con resultado operativo positivo. Space crecía poco (+7,6 %) y daba pérdidas operativas por la I+D de Starship: 3.004 M$ en 2025 (P2, Prospectus Summary p. 4). El segmento AI perdía 6.355 M$ con 3.201 M$ de ingresos.

### 1.2 Último trimestre (3T 2026) y nueve meses de 2026

Fuente: P3, Note 3 ("Revenue disaggregated by type and segment") y Note 18 ("Segments"); contrastado con P5 (8-K Ex. 99.1), que coincide. Pesos, variaciones y márgenes: cálculo propio (script, bloque 2).

| Segmento / línea | 3T 2026 (M$) | Peso | Var. vs 3T 2025 | Margen operativo 3T26 | 9M 2026 (M$) | Peso 9M | Var. vs 9M 2025 |
|---|---|---|---|---|---|---|---|
| **Space** | **1.767** | 12,1 % | +6,1 % | −0,4 % (−7) | **3.348** | 12,4 % | +2,2 % |
| · Launch Services | 1.130 | 7,8 % | +13,0 % | | 2.108 | 7,8 % | +2,5 % |
| · Launch & Development | 637 | 4,4 % | −4,4 % | | 1.240 | 4,6 % | +1,6 % |
| **Connectivity** | **5.248** | 36,0 % | +69,5 % | 45,1 % (2.367) | **12.796** | 47,2 % | +56,8 % |
| · Consumer | 3.121 | 21,4 % | +57,2 % | | 7.754 | 28,6 % | +49,2 % |
| · Enterprise & Government | 2.127 | 14,6 % | +91,4 % | | 5.042 | 18,6 % | +70,3 % |
| **SI** | **7.560** | 51,9 % | +829,9 % | 5,7 % (431) | **10.939** | 40,4 % | +380,2 % |
| · Advertising | 538 | 3,7 % | +18,5 % | | 1.248 | 4,6 % | −5,7 % |
| · SI Solutions & Infrastructure | 7.022 | 48,2 % | +1856,0 % | | 9.691 | 35,8 % | +914,8 % |
| **Total** | **14.575** | 100 % | +161,4 % | 19,1 % (2.791) | **27.083** | 100 % | +97,5 % |

Otras cifras del trimestre (P3, salvo indicación):
- **Beneficio neto:** 4.404 M$ en 3T 2026 (−1.054 M$ en 3T 2025). Incluye 1.025 M$ de "other income", con una plusvalía no realizada de 561 M$ en The Boring Company (Note 8), y un beneficio fiscal de 390 M$. En 9M 2026, pérdida neta de 413 M$.
- **EBITDA ajustado:** 8.809 M$ (3T26) y 13.474 M$ (9M26). Por segmento en 3T26: Space 357, Connectivity 3.499, SI 4.953 (P3, Non-GAAP).
- **Capex 3T26:** 19.593 M$, de los que SI 16.444 (83,9 %, cálculo propio). En 9M26: 48.069 M$, de los que SI 39.995 (P3, Note 18). El capex del trimestre equivale al 134,4 % de los ingresos (cálculo propio).
- **Compensación en acciones ligada a adquisiciones:** 1.217 M$ en 3T26, toda en SI (Note 18). El valor de los premios de Cursor pendientes de devengar es de 23.376 M$ (Note 20).
- **Backlog:** 62.959 M$ a 30-sep-2026 (+121,9 % frente a dic-2025, cálculo propio); el 67 % se reconocería en un año (Note 3).

Métricas operativas (P3, MD&A Key Business Metrics; P5):

| Métrica | 3T 2026 | 3T 2025 | 9M 2026 | 9M 2025 |
|---|---|---|---|---|
| Lanzamientos Falcon (clientes / internos) | 33 (12 / 21) | 43 (15 / 28) | 110 (29 / 81) | 124 (36 / 88) |
| Lanzamientos Starship (todos internos) | 2 | 1 | 3 | 4 |
| Masa a órbita (t), de ella clientes | 476 (119) | 525 (111) | 1.517 (251) | 1.627 (274) |
| Suscriptores Starlink consumo (M, fin de periodo) | 13,6 | 7,2 | — | — |
| ARPU consumo ($/mes) | 69 | 83 | 67 | 84 |
| Cómputo instalado (GW) | 1,7 | 0,6 | — | — |

Los suscriptores crecen un +88,9 % y el ARPU baja un −16,9 % (cálculo propio; P3 da las mismas cifras). La empresa lo atribuye a la expansión internacional y a planes más baratos (P3, MD&A Connectivity). Los suscriptores de consumo **no incluyen** los clientes empresariales y gubernamentales con contrato negociado (aviación, marítimo, gobierno); P5 habla de "hundreds of thousands of additional enterprise subscribers" y de más de 3.800 aviones con Starlink.

**Lectura 3T 2026.** El trimestre cambió la composición del grupo:
- **SI pasó a ser el mayor segmento (51,9 %)**, por los contratos de cloud que empezaron en el 2T 2026 y por Cursor. Su margen operativo fue positivo (5,7 %) por primera vez en los datos publicados, a pesar de 1.217 M$ de compensación en acciones de adquisiciones.
- **Connectivity** sigue siendo el motor rentable: +69,5 % de ingresos y margen operativo del 45,1 %.
- **Space** está estancado en ingresos (+2,2 % en 9M) y en pérdidas por Starship. Hay menos lanzamientos para clientes (29 en 9M26 frente a 36) y SpaceX advierte que puede priorizar su propia carga frente a la de clientes (§4.6).

### 1.3 Descripción de cada negocio

**Space.** Falcon 9 (≈23 t a LEO en configuración desechable; ≈620 lanzamientos y >99 % de éxito a 31-mar-2026) y Falcon Heavy (≈64 t; 11 lanzamientos) (P2, Prospectus Summary). Los ingresos proceden de:
- *Launch Services*: contratos de precio fijo de 1 a 5 años, reconocidos en el lanzamiento.
- *Launch & Development*: contratos de precio fijo de 1 a 14 años para programas de agencias públicas, reconocidos por avance de costes (P3, MD&A).

SpaceX lanzó en 2025 11 de las 12 misiones NSSL (seguridad nacional) de carga media y pesada y las 5 misiones de tripulación y carga a la ISS para la NASA (P2, Prospectus Summary). Dragon ha llevado 78 tripulantes desde 2020 y más de 30 misiones de carga a la ISS (P2, Business). Starship es el sistema de aterrizaje lunar (HLS) de Artemis para la NASA (P2, Business). El importe de ese contrato no aparece en el texto revisado: **SIN VERIFICAR**. En el 3T 2026 SpaceX firmó 3 misiones más de tripulación a la ISS, 18 misiones NSSL, 3 misiones comerciales "Starfall" y un contrato para llevar una carga a la superficie lunar con Starship (P5, Space Business Highlights; importes no publicados).

**Connectivity.** Más de 11.100 satélites Starlink en LEO y servicio en 174 países y territorios a 30-sep-2026 (P3, MD&A Overview), frente a ≈9.600 satélites y 164 mercados a 31-mar-2026 (P2). Incluye:
- **Starlink Consumer Broadband**, con contratos generalmente mensuales.
- **Enterprise y Government Solutions**: aviación, marítimo, movilidad terrestre y gobiernos. Incluye **Starshield**, una red segura para seguridad nacional (observación terrestre, comunicaciones seguras y cargas alojadas) (P2, Business).
- **Starlink Mobile** (directo al móvil): ≈650 satélites V1 Mobile y ≈7,4 M de dispositivos únicos mensuales en ≈30 países a 31-mar-2026 (P2). Los contratos de móvil son plurianuales (1 a 5 años), aunque el cliente puede rescindirlos en general en cualquier momento (P3, MD&A).
- **Espectro:** compra de licencias AWS-4, H-Block y AWS-3 a EchoStar por ≈19.600 M$ (≈11.100 M$ en acciones Clase A a 42,40 $ y hasta 8.500 M$ para pagar deuda de EchoStar). La aprobó la FCC el 12-may-2026 y el cierre final se espera hacia el 30-nov-2027 (P3, MD&A "Spectrum Transaction"). El 8-oct-2026 se firmó además la compra de espectro de 800 MHz (cierre previsto en el 1S 2027; P5).

**SI (antes AI).** Cuatro piezas (P3, Note 1):
1. Infraestructura de cómputo propia (COLOSSUS y COLOSSUS II), con venta de capacidad a terceros (cloud).
2. El modelo Grok.
3. Cursor, plataforma de programación asistida, adquirida el 14-ago-2026.
4. La red social X (publicidad y suscripciones).

El folleto cita ≈550 M de usuarios activos mensuales en Grok y X a 31-mar-2026, de los que ≈117 M usaron funciones de Grok (P2, Prospectus Summary).

### 1.4 El contrato de cómputo que explica el salto del 3T 2026

- **El contrato.** En mayo de 2026 SpaceX firmó "Cloud Services Agreements" con **Anthropic PBC** para dar acceso a ≈325.000 GPU NVIDIA en COLOSSUS y COLOSSUS II. El cliente "has agreed to pay us $1.25 billion per month through May 2029". Pasados los tres primeros meses, **cualquiera de las partes puede rescindirlo con 90 días de preaviso** (P2, Business "Compute Services Agreements with Third Parties", p. 147).
- **El cliente B.** El 10-Q no identifica a sus clientes. Informa de un "Customer B" del segmento SI que supuso el **34,5 % de los ingresos consolidados del 3T 2026** y el 24,2 % de los de 9M 2026 (P3, Note 3). Eso equivale a ≈5.028 M$ en el trimestre, ≈1.676 M$/mes y el 66,5 % de los ingresos de SI (cálculo propio, bloque 3).
- **Inferencia.** Customer B es muy probablemente Anthropic, pero **no está confirmado**: el importe implícito (≈1.676 M$/mes) supera los 1.250 M$/mes del contrato descrito. Puede deberse a contratos adicionales ("Signed additional cloud services agreements during the quarter", P5) o a otra composición. **SIN VERIFICAR**.
- **El resto de SI.** Sin Customer B ni Cursor, SI habría ingresado ≈1.924 M$ en el 3T 2026 (cálculo propio): X, Grok, API y otros clientes de cloud.

---

## 2. Ventajas competitivas y su durabilidad

| Ventaja | Evidencia | Durabilidad |
|---|---|---|
| **Reutilización y cadencia de lanzamiento** | >80 % de la masa puesta en órbita en el mundo cada año desde 2023 (afirmación de la empresa, P2 Summary). 165 lanzamientos Falcon en 2025, 157 con propulsor reutilizado; un primer escalón ha volado 34 veces (P2, MD&A y Summary). | **Alta** mientras Starship no tenga un rival reutilizable a escala. Las barreras de entrada que cita el propio folleto son el capital, las licencias y el historial (P2, Competition). La cadencia Falcon de 2026 baja (110 en 9M26 frente a 124) y la empresa espera que siga bajando a medida que entre Starship (P2, MD&A) |
| **Integración vertical lanzamiento-satélite** | El coste de lanzar Starlink se capitaliza al coste interno, sin margen de terceros (P3, MD&A). ≈75 % de los satélites activos maniobrables del mundo son de SpaceX (≈9.600 de ≈12.700 a 31-mar-2026; P2, Business, cifra de la empresa) | **Alta.** Es la base del margen operativo del 45,1 % de Connectivity en 3T26 (§1.2). La competencia LEO (Amazon LEO, OneWeb) depende en parte de lanzadores ajenos, a veces de la propia SpaceX (P2, Competition) |
| **Escala de Starlink** | 13,6 M de suscriptores de consumo (+88,9 %) y Enterprise & Government +91,4 % en 3T26 (P3) | **Media-alta.** El ARPU cae un −16,9 % interanual (P3). El crecimiento se apoya en mercados de menor renta y en planes más baratos, y la empresa espera que el ARPU siga bajando "over the next few years" (P2, MD&A Key Business Metrics) |
| **Relación con el gobierno de EE. UU.** | ≈1/5 de los ingresos de 2025 procede de agencias federales (P2, Risk Factors "supplying services to the U.S. government"). Es proveedor principal de NSSL y de las misiones a la ISS (§1.3) | **Media.** Es una fuente estable, pero los contratos pueden rescindirse unilateralmente "at the government's convenience" (P2) y dependen de la política. Ver el riesgo de persona clave y de relación política (§4.1) |
| **Cómputo de IA a gran escala** | 1,7 GW instalados a 30-sep-2026 (P3), primera empresa en desplegar un clúster de entrenamiento de un gigavatio según la propia compañía (P2 Summary). La capacidad ya se vende a terceros (§1.4) | **Baja-media.** Es una ventaja de capital y de velocidad, no de tecnología exclusiva: las GPU las vende NVIDIA a todos. El contrato principal se puede rescindir con 90 días de preaviso. SpaceX compite con hiperescaladores y con CoreWeave y Nebius (P2, Competition) |
| **Espectro para directo al móvil** | Compra de AWS-4/H-Block/AWS-3 a EchoStar (≈19.600 M$) y de 800 MHz (§1.3) | **Media-alta** si se completan los cierres. El espectro es escaso y regulado. Queda pendiente la segunda fase del cierre de EchoStar (previsto hacia nov-2027) |

---

## 3. Competidores por segmento

Fuente principal: P2, Business "Competition" (p. 220). El folleto no da cuotas de mercado de los rivales; las comparaciones cuantitativas con competidores quedan **SIN VERIFICAR** en esta fase.

- **Space (lanzamiento).**
  - Establecidos: United Launch Alliance (Boeing y Lockheed Martin), Arianespace y Northrop Grumman (Cygnus).
  - Emergentes: Blue Origin, "which has developed launch vehicles intended to compete with our Falcon 9", Rocket Lab (pequeña carga, en expansión a carga media), Firefly Aerospace y Relativity Space.
  - Agencias nacionales en sus propios mercados.
- **Connectivity, banda ancha** (consumo, empresa y gobierno).
  - Redes terrestres: Verizon, Comcast, AT&T, T-Mobile, Charter, Deutsche Telekom, Vodafone, Telefónica y otras.
  - Satélites GEO: EchoStar, SES, Telesat y Viasat.
  - Constelaciones LEO/MEO: **Amazon LEO**, Blue Origin TeraWave, Eutelsat OneWeb, Iridium NEXT y Telesat Lightspeed.
  - En gobierno, también los grandes contratistas de defensa.
- **Connectivity, Starlink Mobile:** AST SpaceMobile, Lynk, Globalstar y Skylo.
- **SI.**
  - Modelos: OpenAI, Anthropic, Google, Meta, Microsoft y modelos de código abierto.
  - Redes sociales: Threads, Reddit y TikTok.
  - Cloud de IA: CoreWeave, Nebius e hiperescaladores.
  - Cursor compite en herramientas de programación; el folleto no nombra rivales concretos de Cursor (**SIN VERIFICAR**).

Hay una particularidad: varios competidores de Connectivity son a la vez **clientes de lanzamiento** de SpaceX (P2, Competition). Y el principal cliente de cloud (§1.4) es también un competidor directo de Grok.

---

## 4. Riesgos principales

### 4.1 Gobierno corporativo y control de Musk
- **Doble clase de acciones.** Clase A, 1 voto por acción, cotizada. Clase B, **10 votos por acción**, no cotizada. Las dos votan juntas, pero la Clase B elige por separado el **51 % del consejo** (P2, portada y Security Ownership nota 8).
- **El voto de Musk.**
  - Tras la OPV, Musk controla ≈**82,4 %** del voto según la portada del folleto (P2). La tabla de beneficiarios da un **84,4 %** porque incluye 350 M de opciones ejercitables en 60 días; el cálculo propio reproduce ese 84,4 % (bloque 5).
  - Su **participación económica** es de ≈47,8 % en base SEC, con opciones, y del 46,4 % sin ellas (cálculo propio). El 13G de Musk declara 6.418.547.515 acciones beneficiarias, un 48,4 % de la Clase A "as-converted" (P7).
  - A 15-oct-2026, si sus tenencias no han cambiado desde el 13G, tendría ≈**86,1 % del voto** y ≈97,8 % de la Clase B emitida (estimación propia con las acciones de la portada de P3). **SIN VERIFICAR**: no hay *proxy* posterior a la OPV.
- **"Controlled company".** SpaceX usa las exenciones de Nasdaq a ciertos requisitos de gobierno corporativo (P2, portada).
- **Paquete de acciones restringidas de Musk:** 1.302.072.285 acciones Clase B, que **Musk puede votar ya** aunque no estén consolidadas (P2, "2026 Compensation Developments").
  - 1.000 M se conceden en 15 tramos ligados a hitos de capitalización. Cada tramo exige además "the Company's establishment of a permanent human colony on Mars with at least one million inhabitants".
  - Las otras 302.072.285 se ligan a 12 tramos de capitalización, entre 1,065 y 6,565 billones $, y a centros de datos fuera de la Tierra "capable of delivering 100 terawatts of compute per year".
  - Los hitos no financieros hacen improbable la consolidación en un horizonte normal de inversión. Mientras tanto, los votos de esas acciones refuerzan el control.
- **Derechos de los accionistas limitados (ley de Texas).**
  - Para presentar una demanda derivada hace falta el **3 % del capital**, unos 53.000 M$ al precio de la OPV (P2, Risk Factors).
  - Los estatutos prohíben las demandas colectivas en disputas internas, que deben ir de forma individual o por arbitraje (P2, Risk Factors "Forum Selection Bylaw").
  - El propio folleto advierte que una cláusula similar ya fue impugnada en otra empresa de Texas.
- **Dedicación parcial.** Musk "does not devote his full time and attention to our businesses" (P2, Risk Factors). Es CEO de Tesla y tiene ≈20 % de su capital (P2, Related Person Transactions).
- **Exposición política y regulatoria por la persona.** El folleto cita el embargo de activos de Starlink en Brasil por hechos relativos a una empresa "only affiliated with Mr. Musk". Reconoce que puede sufrir "adverse actions from governmental actors" por actos de sus consejeros o accionistas (P2, Risk Factors).

### 4.2 Partes vinculadas (Tesla, xAI/X, Valor, The Boring Company)
- **Valor Equity Partners.** Su fundador, Antonio Gracias, es consejero de SpaceX.
  - Tres arrendamientos de equipos de cómputo con pagos totales de 6.986, 6.633 y 6.587 M$, garantizados por SpaceX (P2, Related Person Transactions).
  - Contablemente son *failed sale-leasebacks*: 12.897 M$ de deuda a 30-sep-2026, el **33,2 % de la deuda y arrendamientos contables** (38.844 M$), y 864 M$ de intereses en 9M26 (P3, Notes 9 y 17; cálculo propio, bloque 8).
  - Es la principal relación con partes vinculadas por importe.
- **Tesla.**
  - SpaceX compró Megapacks a Tesla por 480 M$ en 9M26 (P3, Note 17). En 2025 xAI compró bienes y servicios a Tesla por 506 M$ (P2).
  - Tesla tenía 18.990.195 acciones Clase A de SpaceX (<1 %) (P2).
  - **Nuevo en el 3T 2026:** el consejo de SpaceX formó un comité especial "to evaluate a potential combination between SpaceX and Tesla, Inc."; Tesla formó otro. No hay decisión, y cualquier operación requeriría la aprobación "of our controlling shareholder" (P3, MD&A).
  - Una fusión entre dos sociedades controladas por la misma persona plantea un conflicto de interés evidente en la fijación del precio. Su efecto en el valor es imposible de estimar hoy (**SIN VERIFICAR**).
- **xAI y X.** Se incorporaron en febrero de 2026 por canje de acciones entre sociedades del mismo controlador (Advertencias previas, punto 1). Traen litigios y regulación propios (§4.4).
- **The Boring Company** (controlada por Musk). SpaceX registra su participación a valor razonable: plusvalía de 561 M$ en 3T26 (P3, Note 8). Ese resultado no es operativo y depende de rondas privadas de otra empresa de Musk.
- **Otras operaciones menores** con Musk: seguridad personal, aviones y alquileres (P2).
- **Control interno de estas operaciones.** Se aprobó una política para que el comité de auditoría revise las operaciones vinculadas (P2). Con el control de Musk, ese comité es el principal contrapeso.

### 4.3 Concentración de clientes
- **Customer A** supuso el 20,9 % de los ingresos de FY2025 (≈3.903 M$, cálculo propio), el 24,2 % en FY2024 y el 16,6 % en 3T26. Tiene ingresos en los tres segmentos (P2 y P3, Note 3).
- **Inferencia:** es el gobierno federal de EE. UU. tratado como un solo cliente, porque el folleto dice que "approximately one-fifth of our revenue was attributable to agencies within the U.S. federal government" en 2025 (P2, Risk Factors). **No confirmado**.
- **Customer B** supuso el 34,5 % en 3T26 (§1.4). Customer A + B suman el **51,1 % de los ingresos del 3T 2026** (cálculo propio).
- **El riesgo del 3T 2026.** El salto de ingresos y de margen depende de un contrato rescindible con 90 días de preaviso. Un cliente que además es competidor puede preferir su propia infraestructura. Así lo reconoce el factor de riesgo añadido en el 10-Q del 2T: "a significant portion of our AI infrastructure revenue is concentrated in a small number of customers" (P6, Part II Item 1A).
- **Concentración de cobro.** A 30-sep-2026 un solo cliente suponía el 27,7 % de las cuentas a cobrar (P3, Note 3).

### 4.4 Regulación y litigios
- **Litigios de X y Grok** (P3, Note 16):
  - Multa de la Comisión Europea de 120 M€ por la DSA, recurrida.
  - Demandas colectivas en EE. UU. por imágenes sexuales no consentidas generadas con Grok; el fiscal general de Virginia ha notificado posibles acciones (19-oct-2026).
  - Acciones colectivas por GDPR en Países Bajos.
  - Un veredicto de patentes de 105 M$ más 67 M$ de intereses, recurrido.
  - Demanda de NAACP por las turbinas de gas que alimentan COLOSSUS II.
  - Provisión total por litigios: 350 M$. Para el resto, la empresa "is not currently able to estimate the reasonably possible loss" (P3).
- **Espectro, órbita y lanzamiento.** Dependen de licencias de la FCC, la FAA e internacionales; las operaciones de espectro están condicionadas a aprobaciones (P3, MD&A).
- **Contratación pública.** Sujeta a FAR/DFARS y a rescisión a conveniencia del gobierno (P2, Business "Government Contracts").

### 4.5 Intensidad de capital y financiación
- **Capex y caja.** El capex de 9M26 fue de 48.069 M$, el 177,5 % de los ingresos (cálculo propio), con un flujo operativo de 13.097 M$ (P3, MD&A Cash Flows). La diferencia se financió con la OPV (85.675 M$ netos) y con bonos (25.000 M$) (§6).
- **Balance a 30-sep-2026:** 89.855 M$ en caja y valores negociables y 38.006 M$ de deuda principal (P3; cálculo propio).
- **Compromisos no cancelables:** 37.840 M$, de ellos 25.569 M$ en 2027 (P3, Note 16).
- **Dilución por compensación en acciones:** 2.616 M$ ordinaria más 1.217 M$ de adquisiciones en 9M26 (P3). Además, las adquisiciones pagadas con acciones (Cursor y EchoStar) aumentan el número de acciones (§6.2).

### 4.6 Ejecución de Starship y conflicto de capacidad
- **Coste de Starship.** La I+D de Space subió un +56,2 % en 9M26 hasta 3.231 M$, sobre todo por Starship (P3, MD&A). El primer vuelo orbital, Flight 14, desplegó 26 satélites Starlink V3 (P5).
- **Conflicto de capacidad.** SpaceX "may prioritize our own launch payloads over additional U.S. government contracts or third-party customers" para sus objetivos de cómputo orbital, lo que "may limit revenue growth in our Space segment" y "could invite litigation from customers or competitors" (P2, Risk Factors).

---

## 5. Qué parte del valor depende de negocios que aún no generan ingresos

**Lo que SpaceX dice de su mercado.** Estima un mercado potencial cuantificable de **28,5 billones $**: 370.000 M$ en Space, 1,6 billones $ en Connectivity y 26,5 billones $ en AI, de los que 22,7 billones $ son "enterprise applications" (P2, Prospectus Summary). Es una estimación de la empresa, no un dato. La empresa excluye expresamente de esa cifra las iniciativas "with uncertain timing and scale" (P2, Business).

**Lo que ya factura y lo que no:**

| Iniciativa | Estado según los documentos | ¿Ingresos propios publicados? |
|---|---|---|
| **Starship comercial** | Primer vuelo orbital con carga (Starlink V3) en 3T26 (P5). "To date, all Starship launches have been classified as internal" (P3). Ya existe un contrato para llevar una carga a la Luna (P5, sin importe) | **No.** P5 lo llama "first revenue-generating Starship mission", pero ese ingreso es de Starlink (Connectivity), no de un cliente de lanzamiento |
| **HLS / Artemis (NASA)** | Starship es el HLS de la NASA (P2) | Parte de *Launch & Development* sin desglose (**SIN VERIFICAR**) |
| **Directo al móvil** | Factura dentro de Enterprise & Government. ≈7,4 M de dispositivos únicos mensuales a 31-mar-2026 (P2). El folleto estima un mercado de 740.000 M$ (P2) | Sí factura, pero **sin importe separado** (**SIN VERIFICAR**) |
| **Cómputo orbital (centros de datos en el espacio)** | "We expect to begin deploying our orbital AI compute satellites as early as 2028" (P2, Summary). Objetivo de 100 GW citado entre los retos (P2) | **No** |
| **Base lunar y Marte** | Objetivos de la misión y condición del paquete de acciones de Musk (§4.1) | **No** |
| **Fabricación de chips de IA, "human augmentation"** | Citados como iniciativas con "unproven technologies or technologies that do not exist" (P2, Our Challenges) | **No** |

**Cálculo ilustrativo propio (no procede de ninguna fuente; script, bloque 6).** Al precio de la OPV (135 $) y con 13.174.187.298 acciones tras la oferta y el green shoe, la capitalización era de ≈**1.778.515 M$**. Con datos de 1-may-2026, sin opciones ni RSU y sin las acciones emitidas después (Cursor). La cotización vigente queda para la Fase 3. Esa capitalización equivale a:
- **95,2 veces** los ingresos de FY2025, y 30,5 veces los del 3T 2026 anualizados.
- Si los negocios que ya generan beneficio de forma recurrente (Space + Connectivity) valieran **30 veces** su EBITDA ajustado de FY2025, sumarían ≈234.630 M$, el **13,2 %** de esa capitalización.
- Si se anualiza el EBITDA ajustado del 3T 2026 (×4) y se aplican 30 veces, se llega a ≈1.057.080 M$, el 59,4 %. Pero si se resta todo el ingreso del Customer B, rescindible con 90 días de preaviso, se baja al 25,5 %.

**Conclusión de la sección.** Con los datos auditados de FY2025, la mayor parte del precio de salida descontaba negocios sin ingresos separados o todavía no materiales: cómputo de IA a escala, Starship comercial, directo al móvil a gran escala, cómputo orbital y Luna/Marte. El 3T 2026 reduce esa dependencia **si** el ingreso de cloud resulta duradero. Hoy depende de pocos clientes con contratos cortos de rescindir. Ninguna de las iniciativas a largo plazo (cómputo orbital, Luna, Marte) tiene todavía una métrica pública que permita seguirla trimestre a trimestre. Starship sí la tiene en parte: vuelos y masa a órbita (P3).

---

## 6. Estado tras la OPV

### 6.1 La salida a bolsa
- **Registro:** S-1 del 20-may-2026 (P1), enmiendas S-1/A del 1-jun y 3-jun-2026 (P1b) y declaración de efectividad el 11-jun-2026 (P14; P3 Part II Item 2).
- **Precio:** **135,00 $ por acción Clase A** (P2, portada). El folleto final es del 11-jun-2026.
- **Primer día de cotización:** 12-jun-2026, con apertura a 160 $ ([S1](https://www.merceradvisors.com/?p=55047), **solo secundaria**). Cierre de la operación: **15-jun-2026** (P4).
- **Mercados:** Nasdaq y Nasdaq Texas, ticker **SPCX**. También hubo oferta pública en Australia, Canadá, el EEE, Japón, Suiza y Reino Unido (P4).
- **Tamaño:** 555.555.555 acciones más la opción de sobreasignación de 83.333.333, ejercida completa: **638.888.888 acciones** (P4).
- **Importes:** bruto de ≈86.250 M$ (cálculo propio) y **neto de 85.675 M$**, tras 575 M$ de comisiones y gastos (P3, Note 1).
- **Uso de los fondos:** infraestructura de cómputo de IA, lanzadores y constelaciones (P4).
- **Split previo:** 5 por 1 en mayo de 2026 (P3, Note 1).
- **Bonos:** el 26-jun-2026 SpaceX emitió **25.000 M$** en cinco tramos con vencimientos de 2031 a 2056 y un cupón medio ponderado del 5,855 %, para devolver el préstamo puente (P9; P3 MD&A).
- **Lock-up:** 180 días con liberaciones anticipadas desde el 3T 2026; para Musk, **366 días** sin liberación anticipada (P2, Shares Eligible for Future Sale). Hay además un lock-up ampliado para algunos accionistas hasta la publicación de los resultados del 2T 2027 (P2).
- **Cotización vigente:** fuera del alcance de la Fase 1 y **SIN VERIFICAR**. Hay dos referencias primarias puntuales: la acción valía 141,29 $ al cierre de la fusión de Cursor (14-ago-2026; P3, Note 20), y Gwynne Shotwell vendió 12.500 acciones a 151,1515 $ el 22-sep-2026 (P12). Según S1, el máximo fue de 225,64 $ el 16-jun-2026 y la acción estaba en ≈113,50 $ a finales de julio (**solo secundaria**).

### 6.2 Acciones en circulación por clase

| Fecha y fuente | Clase A | Clase B (10 votos) | Clase C | Total |
|---|---|---|---|---|
| Tras la OPV, sin green shoe (base 1-may-2026; P2, Security Ownership) | 7.488.063.555 | 5.602.790.410 | eliminada (reclasificada a A) | 13.090.853.965 |
| 30-sep-2026 (P3, balance; en millones) | 8.240 | 5.339 | — | 13.579 |
| **15-oct-2026 (P3, portada)** | **8.246.541.218** | **5.334.522.491** | — | **13.581.063.709** |

Notas:
- La Clase B suponía el 39,3 % del capital y el **86,6 % de los votos** a 15-oct-2026 (cálculo propio).
- En el 3T 2026 se convirtieron 230 M de acciones de Clase B en Clase A (P3, Note 12).
- **Cursor.** Su fusión emitió 389.289.254 acciones Clase A más 1.752.426 por RSU consolidadas (P8). De ellas, solo 271 M cuentan como precio de compra (42.500 M$ a 141,29 $); el resto se trata como compensación en acciones (P3, Note 20). No es una contradicción, sino una diferencia de tratamiento contable.
- **Pendiente de emitir:** ≈261,8 M de acciones Clase A para EchoStar al cierre final del espectro (P3, MD&A).
- **Socios principales con 13G** (evento 30-jun-2026): Musk (P7), Google/Alphabet con 551.189.500 acciones, un 7,2 % de la Clase A (P13), Founders Fund II y Antonio Gracias (P13, no leídos en detalle).

### 6.3 Adquisiciones desde la OPV
- **Mesh Optical** (transceptores ópticos): cerrada el 6-jul-2026 por 249 M$ en acciones (P3, Note 20).
- **Cursor (Anysphere):** cerrada el 14-ago-2026, con un valor implícito de 60.000 M$ y un precio de compra contable de 42.500 M$ (P3, Note 20; P8). El fondo de comercio pasó de 11.809 M$ a 48.423 M$ entre dic-2025 y sep-2026 (P3, balance).

### 6.4 Documentos periódicos: qué existe y qué no (P14, consultado el 25-oct-2026)

| Documento | ¿Existe? | Detalle |
|---|---|---|
| S-1, S-1/A y 424B4 | **Sí** | 20-may, 1-jun y 3-jun-2026; 424B4 del 12-jun-2026. Contienen FY2023-FY2025 auditados y el 1T 2026 sin auditar |
| 10-Q del 1T 2026 | **No** | Era anterior a la OPV; el 1T 2026 aparece solo en el folleto (P2) |
| **10-Q del 2T 2026** | **Sí** | 4-ago-2026 (P6) |
| **10-Q del 3T 2026** | **Sí** | 22-oct-2026 (P3) |
| 8-K de resultados | **Sí** | 4-ago-2026 (2T) y 20-oct-2026 (3T, P5). Los resultados se divulgan por la web y por la cuenta @SpaceX en X, no por agencias (P4, Item 7.01) |
| **10-K** | **No** | Todavía no hay informe anual como cotizada. El primero cubrirá FY2026. Fecha esperada: hasta 90 días después del 31-dic-2026, porque la portada de P3 marca "non-accelerated filer"; es una inferencia sobre el plazo legal, **SIN VERIFICAR** |
| **Proxy (DEF 14A)** y junta anual | **No** | No hay *proxy* tras la OPV, así que no hay datos actualizados de voto ni de retribución más allá del folleto |
| Form 3/4, 13G, 144 y S-8 | **Sí** | Ver P7, P12 y P13. Hay S-8 del 12-jun, 4-ago (dos) y 22-oct-2026 |
| Transcripción de la *call* del 3T 2026 | No consultada | Disponible según P5 en ir.spacex.com. Sus declaraciones no se usan en 01 |

---

## 7. Contradicciones entre fuentes y datos SIN VERIFICAR

**Contradicciones o diferencias detectadas (todas explicables):**
1. **Voto de Musk: 82,4 % frente a 84,4 %** (P2, portada frente a la tabla de beneficiarios). La tabla incluye 350 M de opciones ejercitables; el cálculo propio reproduce el 84,4 %.
2. **Lanzamientos de 2025: 165 frente a 170** (P2). 165 son lanzamientos Falcon; 170 incluye los vuelos de Starship.
3. **"First revenue-generating Starship mission"** (P5) **frente a "all Starship launches have been classified as internal"** (P3). No hay ingreso de lanzamiento: el ingreso es de Starlink.
4. **Customer B ≈1.676 M$/mes frente a los 1.250 M$/mes del contrato con Anthropic** (P3 frente a P2). La identidad del cliente no está confirmada; puede haber contratos adicionales.
5. **Cursor: 389,3 M de acciones emitidas** (P8) **frente a 271 M como precio de compra** (P3). La diferencia es la parte tratada como compensación en acciones.
6. **Coincidencia a revisar en la Fase 2:** el capex de Space de 9M 2026 (3.832 M$, P3 Note 18 y P5) es idéntico al capex de Space de FY2025 (3.832 M$, P2 Summary p. 4). Puede ser una coincidencia, pero conviene contrastarlo con la nota de segmentos de los estados anuales de P2.
7. **Cambio de nombre de la métrica de suscriptores.** "Starlink Subscribers" (P2) pasó a llamarse "Starlink consumer subscribers" (P3), con la misma definición, y el segmento AI pasó a llamarse SI. No son contradicciones, pero hay que tenerlo en cuenta al comparar periodos.

**SIN VERIFICAR:**
- Los ingresos separados de Dragon, de los contratos con la NASA (incluido el HLS), de Starshield y de Starlink Mobile. SpaceX no los desglosa.
- La identidad de Customer A (inferencia: gobierno federal de EE. UU.) y de Customer B (inferencia: Anthropic).
- El voto y la participación actuales de Musk tras el 30-jun-2026: la estimación del 86,1 % supone tenencias sin cambios.
- La cotización y la capitalización vigentes, pendientes para la Fase 3.
- El efecto de una posible combinación con Tesla.
- Las cuotas de mercado de los competidores.
- La fecha límite del primer 10-K.
