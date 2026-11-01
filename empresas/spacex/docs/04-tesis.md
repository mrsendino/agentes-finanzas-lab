# 04 — Tesis alcista, tesis bajista y abogado del diablo (SPCX)

**Fecha del análisis:** 2026-10-28 · **Versión:** v1 · **Analista:** Fase 4 (rol *Investment Researcher*) · **Precio de referencia:** 147,49 $ (cierre del 23-oct-2026, M1; 03 §1)
**Alcance:** contrastar dos tesis con el mismo rigor, someter el caso base de la Fase 3 al abogado del diablo y definir qué datos confirmarían o refutarían cada escenario. **No es una recomendación.** No hay precio objetivo ni lenguaje de compra o venta: solo escenarios y rangos.

**Aviso de conflicto de interés.** Este documento lo redacta un modelo de Anthropic. El folleto (P2 p. 147) describe un contrato de cómputo de SpaceX con **Anthropic PBC**, y la Fase 1 infiere (**SIN VERIFICAR**) que el "Customer B" del 10-Q es Anthropic. El 10-Q no identifica a Customer B. Este documento se ciñe a lo que publican las fuentes, trata a Customer B solo por sus cifras publicadas y no usa ninguna información sobre Anthropic que no esté en esas fuentes.

**Archivos de esta fase**

| Archivo | Contenido |
|---|---|
| [`scripts/fase4_tesis.py`](../scripts/fase4_tesis.py) | Todas las cifras de este documento. **Importa** `fase3_dcf.py` (que lee los CSV de la Fase 2): los valores por escenario, el WACC, las acciones y el DCF inverso salen del modelo, no se copian. Las variantes del abogado del diablo son llamadas a `run_dcf()` y `base_var()` de la Fase 3. Para "capex al ritmo de la guía durante dos años" envuelve `proj_segment()` sin tocar sus fórmulas, con un control que reproduce el 21,40 $ de la Fase 3. 14 controles, todos OK. No escribe ficheros |
| [`fuentes/nuevas_fase4_v1.md`](../fuentes/nuevas_fase4_v1.md) | Fuente nueva S9 (resumen de la call del 3T26) y lista de datos de fases anteriores usados |

**Etiquetas:** **[SEC]** = documento presentado ante la SEC; **[CALL]** = dicho en la call del 3T26 según fuentes secundarias (S7, S9), sin transcripción verificada; **[SUPUESTO]** = hipótesis del modelo o de esta fase; **SIN VERIFICAR** = no se pudo contrastar. "vpa" = valor por acción en la base diluida de la Fase 3 (14.492,86 M de acciones). M$ = millones de dólares. Todas las cifras se copian de la salida de `fase4_tesis.py`.

---

## 0. Resumen

1. **Punto de partida.** El modelo de la Fase 3 da **0,61 $ / 25,27 $ / 99,74 $** por acción (bajista / base / alcista) frente a 147,49 $. Ni el alcista llega al precio (−32,4 %). El 86,7 % del EV del base es valor terminal.
2. **Dónde está el valor del base.** Valorando cada segmento por separado (aproximación, §1), **Connectivity aporta 18,06 $, SI 5,88 $ y Space −1,98 $**. El caso base es, sobre todo, un Starlink que sigue creciendo. En el alcista, SI pasa a 66,26 $: la discusión sobre el precio es una discusión sobre SI.
3. **Tesis alcista (5 argumentos, §2):** escala de SI con la guía [CALL], capex de crecimiento con k bajo, Connectivity, Starship y balance. Con los supuestos del alcista y tres ajustes favorables a la vez (WACC solo con betas de Damodaran, vida útil de 6 años y margen de SI del 3T26), el modelo llega a **145,13 $**, casi el precio.
4. **Tesis bajista (5 argumentos, §3):** concentración en Customer B, intensidad de capital, ARPU, pérdidas de Space y coste de la financiación y la SBC. Una combinación desfavorable pero no extrema (k observado, B no renueva, capex al ritmo de la guía y WACC de comparables) da **9,66 $**.
5. **Abogado del diablo (§5).** Los supuestos con más efecto en el base son **la intensidad de capital de SI** (k 1,62 → 14,83 $; k 2,14 → 0 $), **el margen de SI** (65,5 % del 3T26 → 40,33 $) y **el valor terminal** (sin él, 5,90 $). La beta de 1,112 es razonable dentro de un rango de 10,09-31,12 $. El tratamiento de Customer B **infravalora su riesgo**: su pérdida solo cuesta 0,68 $ si el margen del resto de SI sigue en el 50 %; con un margen del 30 % el base baja a 12,91 $. La base de acciones apenas importa si los 1.333 M de premios incluyen las acciones de Musk (25,22 $ frente a 23,15 $).
6. **El precio.** 147,49 $ es coherente con los fundamentales si se cumple **todo** el alcista (guía del 1T27, Customer B renovado, k de 0,90) **y** además el WACC baja al 7,97 % o se combinan varios ajustes favorables. Con la estructura del base hace falta un TACC de ingresos del 50,7 % durante 10 años (03 §6).

**Horizonte:** las señales de §4 se pueden comprobar entre el 8-K del 4T26 (previsto a principios de 2027, fecha SIN VERIFICAR) y el 10-Q del 3T27 (oct-nov 2027). La valoración se refiere a 10 años más valor terminal.
**Confianza:** **alta** en los datos históricos (primarios y cuadrados en 02); **media** en la mecánica del modelo; **baja** en cualquier punto de la senda futura de SI, porque depende de una guía secundaria, de un cliente rescindible con 90 días y de una intensidad de capital observada solo durante tres trimestres.

---

## 1. Punto de partida común (modelo de la Fase 3, importado)

| Hecho | Bajista | Base | Alcista | Fuente |
|---|---:|---:|---:|---|
| Valor por acción (diluida) | 0,61 $ | 25,27 $ | 99,74 $ | 03 §4.1; script §1 |
| Frente al precio de 147,49 $ | −99,6 % | −82,9 % | −32,4 % | script §1 |
| EV del modelo (M$) | −33.650 | 323.796 | 1.403.074 | 03 §4.1 |
| Valor terminal / EV | −57,0 % | 86,7 % | 77,3 % | 03 §4.1 |
| FCFF del año 1 (oct-26 a sep-27, M$) | −34.820 | −39.596 | −53.162 | script §1 |
| FCFF acumulado mínimo (M$) | −68.788 | −54.884 | −60.262 | 03 §4.1 |
| TACC de ingresos a 10 años | 11,7 % | 22,7 % | 32,5 % | 03 §3.5 |

Mercado: capitalización (portada) de 2.003.071 M$ y EV de 1.952.060 M$. WACC inicial 9,57 %, terminal 9,34 %, beta reapalancada 1,112 (03 §1.2).

**Valor por segmento (cálculo nuevo de esta fase, aproximado).** Cada segmento se descuenta con su FCFF y un impuesto del 21 % sobre su EBIT positivo, sin compensar pérdidas entre segmentos. Por eso la suma no coincide con el EV del modelo (318.335 frente a 323.796 M$ en el base).

| Segmento (vpa) | Bajista | Base | Alcista |
|---|---:|---:|---:|
| Space | −2,79 $ | −1,98 $ | −0,91 $ |
| Connectivity | 9,01 $ | 18,06 $ | 31,41 $ |
| SI | −10,41 $ | 5,88 $ | 66,26 $ |

**Lectura.** En el base, Connectivity (EV de 261.761 M$) explica la mayor parte del valor; SI aporta poco (85.228 M$) porque cada dólar de ingreso nuevo exige 1,25 $ de capex que se repone cada 5 años; y Space resta, porque el modelo no da ingresos comerciales a Starship. **La pregunta que separa las tesis es si SI es un negocio que crea valor (alcista: 66,26 $) o que lo destruye (bajista: −10,41 $).**

---

## 2. Tesis alcista

### 2.1 Argumento central

SpaceX es el único grupo que reúne lanzamiento reutilizable a escala, la mayor constelación de banda ancha y cómputo de IA de gigavatios. El TTM no describe el negocio actual: los ingresos de SI crecieron un +829,9 % en el 3T26 (02 §2) y el capex de 2026 es inversión en capacidad que todavía no factura. Si la guía se cumple, el run-rate de SI se triplica en dos trimestres y el capex por dólar de ingreso cae.

### 2.2 Cinco argumentos, cada uno con su cifra

| # | Argumento | Cifra | Fuente | Efecto medido en el modelo |
|---|---|---|---|---|
| A1 | **SI ya factura a escala y la guía apunta a otro salto** | RR de SI del 3T26: 30.240 M$. La guía de ingresos del 1T27 implica un RR de SI de **103.940-111.940 M$ (×3,44 a ×3,70)**; el objetivo de 100.000 M$ anualizados en dic-2026 implica 71.940 M$. Backlog de 62.959 M$. Margen EBITDA aj. de SI del 65,5 % en el 3T26 y margen incremental del 82,5 % (1T→3T26) | RR y márgenes: P3 vía 02 §4 y §9.2; guía: S7, S9 [CALL], **SIN VERIFICAR**; backlog: P3 Note 3 (01 §1.2) | Base con el 100 % del punto medio de la guía: **28,79 $**. Base con el margen objetivo de SI igual al del 3T26 (65,5 %): **40,33 $** |
| A2 | **El capex es de crecimiento, no de mantenimiento** | Capex de SI de 9M26 / aumento de capacidad (0,8 → 1,7 GW) = **44,4 $/W**. Con k = 0,90, eso equivale a 49,4 $ de ingreso anual por vatio, cerca de los ">50 $/W" citados en la call | P2 p. 27, P3 KBM (vía 03 §3.2); ">50 $/W": S7 [CALL], SIN VERIFICAR | Base con k de SI 0,90: **35,15 $**; con k 1,0: 32,33 $ |
| A3 | **Connectivity es un negocio probado y rentable** | Ingresos del 3T26: 5.248 M$ (+69,5 %). Margen EBITDA aj. del 66,7 %. EBITDA aj. − capex TTM: +4.759 M$. Suscriptores de consumo: 7,2 → 13,6 M (+88,9 %) | P3 vía 02 §2, §4; suscriptores: P3 KBM (01 §1.2) | Connectivity sola vale 18,06 $ en el base. Base con los supuestos de Connectivity del alcista: **36,64 $** |
| A4 | **Starship empieza a operar y el modelo le da valor negativo** | Primer vuelo orbital (Flight 14) con 26 satélites V3; contrato para una carga lunar con Starship; 18 misiones NSSL y 3 "Starfall" firmadas en el 3T26. Vuelos semanales de Starship en el 1S27 según Musk | P5 Business Highlights (01 §1.3, §4.6); vuelos semanales: S9 [CALL], SIN VERIFICAR | Space vale −1,98 $ en el base y −0,91 $ en el alcista. Base con los supuestos de Space del alcista: **26,16 $ (+0,88 $)**. El modelo no recoge Starship como negocio de lanzamiento comercial (03 §3.5) |
| A5 | **El balance financia la transición sin ampliar capital** | Caja + valores: 89.855 M$. Caja neta: 51.011 M$ = **3,52 $ por acción**. Sin vencimientos materiales hasta jul-2031 | P3 vía 02 §6 | El FCFF acumulado mínimo consume el 61,1 % (base) o el 67,1 % (alcista) de la caja: ninguno de los dos escenarios necesita ampliar capital (03 §4.1) |

### 2.3 Qué tiene que ser verdad para la tesis alcista

1. Que los ingresos del 1T27 estén en la guía (≥ 33.000 M$) y que el salto venga de **varios** clientes de cloud, no solo de Customer B.
2. Que la intensidad de capital de SI baje a k ≈ 0,90 (≈49 $ de ingreso por vatio), frente al 1,615 observado en el TTM.
3. Que el margen EBITDA aj. de SI se sostenga en el 60 % o más cuando el precio del cómputo baje y venza la primera generación de GPU.
4. Que Customer B renueve en 2029 sin recorte de precio.
5. Que Connectivity siga creciendo al 22 % anual en los años 2-5 a pesar de la caída del ARPU.

### 2.4 Debilidades de la propia tesis alcista (reconocidas)

- **Aun con todo lo anterior, el modelo da 99,74 $**, un 32,4 % por debajo del precio. Para llegar a 147,49 $ hace falta además un WACC inicial del 7,97 % o una combinación de ajustes favorables (§6).
- **A1 descansa en datos secundarios.** La guía y el objetivo de 100.000 M$ no están en ningún documento SEC (S7, S9).
- **A2 y A1 son difíciles de cumplir a la vez:** la guía de capex del 4T26 (35.000-40.000 M$) y los 13 GW a fin de 2027 [CALL] implican un capex muy superior al del alcista (§5.1).
- **El margen del 3T26 (65,5 %) es de un solo trimestre** y depende de Customer B (02 §9.2).

### 2.5 Rango de la tesis alcista

Entre **99,74 $** (alcista de la Fase 3) y **145,13 $** (alcista con WACC solo de Damodaran, vida útil de 6 años y margen de SI del 3T26; script §6).

---

## 3. Tesis bajista

### 3.1 Argumento central

El salto del 3T26 descansa en un cliente que puede irse con 90 días de preaviso, en un negocio (alquiler de GPU) sin ventaja tecnológica propia y con una intensidad de capital que hoy destruye caja: 171,5 % de capex sobre ingresos y un FCF de −39.198 M$ en el TTM. El negocio que sí funciona (Connectivity) vale una fracción del precio y su ARPU cae. El control de Musk y las operaciones vinculadas añaden un riesgo de reparto de valor que el DCF no recoge.

### 3.2 Cinco argumentos, cada uno con su cifra

| # | Argumento | Cifra | Fuente | Efecto medido en el modelo |
|---|---|---|---|---|
| B1 | **SI depende de un cliente rescindible** | Customer B: 5.028 M$ en el 3T26, el **34,5 %** de los ingresos (A + B: 51,1 %). RR de 20.114 M$ = **66,5 % del RR de SI**. Factura 1.676 M$/mes, frente a los 1.250 M$/mes del contrato descrito en P2: hay 426 M$/mes sin contrato documentado. Rescindible con 90 días | P3 Note 3 vía 02 §9; contrato: P2 p. 147 (01 §1.4) | B rescinde en el año 1 (variante de 03): **20,08 $**. Si además el margen de SI baja al 40 % / 30 %: **16,50 $ / 12,91 $** |
| B2 | **La intensidad de capital destruye valor** | Capex TTM: 54.960 M$ = 171,5 % de los ingresos. FCF TTM: −39.198 M$. k observado de SI: 1,615. Guía de capex del 4T26: 35.000-40.000 M$, el 63,7-72,8 % del capex TTM en un trimestre | P3 vía 02 §5; k: 03 §3.2; guía: S7, S9 [CALL], SIN VERIFICAR | Base con k observado: **14,83 $**. Capex de SI al ritmo de la guía en el año 1: 21,40 $; en los años 1 y 2: **17,19 $** |
| B3 | **Starlink crece bajando precios** | ARPU de consumo: 83 → 69 $/mes (−16,9 %) en un año; FY2024 → FY2025: 91 → 81 $ (−11,0 %). La empresa espera que siga bajando "over the next few years". Competidores LEO con financiación propia (Amazon LEO) | P3 y P2 MD&A Key Business Metrics (01 §1.2, §2, §3) | Connectivity sostiene el base (18,06 $). Base con los supuestos de Connectivity del bajista: **16,67 $ (−8,60 $)** |
| B4 | **Space pierde dinero y crece poco** | Margen operativo TTM: −40,6 %. I+D / ingresos TTM: 100,2 %. Ingresos 9M26: +2,2 %. Menos lanzamientos para clientes (29 frente a 36 en 9M) y prioridad a la carga propia | P3 vía 02 §4; lanzamientos y riesgo: P3 KBM y P2 Risk Factors (01 §1.2, §4.6) | Space vale −1,98 $ en el base. Base con los supuestos de Space del bajista: **24,57 $ (−0,71 $)** |
| B5 | **La financiación y la SBC trasladan valor fuera del accionista minoritario** | SBC TTM: 4.736 M$ = 14,8 % de los ingresos. Premios de Cursor pendientes: 23.376 M$ = 1,61 $ por acción (sin descontar). Deuda con Valor (parte vinculada): 12.897 M$ = 33,2 % de la deuda, con un coste anualizado del **10,9 %** en el 3T26 frente al cupón del 5,855 % de los Notes | P3 vía 02 §6-7; Cursor: P3 Note 20 (01 §1.2); tipo: cálculo de esta fase (§7) | El FCFF acumulado mínimo consume el 76,6 % de la caja en el bajista; quedarían 21.067 M$ |

### 3.3 Qué tiene que ser verdad para la tesis bajista

1. Que Customer B rescinda o renegocie a la baja antes de 2029, o que su sustitución llegue con márgenes menores.
2. Que el capex del 4T26 y de 2027 se mantenga cerca de la guía sin que los ingresos de SI la sigan (k ≥ 1,6).
3. Que el ARPU siga cayendo y el crecimiento de Connectivity baje del 15 % en 2027.
4. Que Starship no genere ingresos de lanzamiento de terceros antes de 2028.
5. Que la combinación con Tesla u otras operaciones vinculadas se hagan en términos desfavorables para los accionistas de la Clase A.

### 3.4 Debilidades de la propia tesis bajista (reconocidas)

- **El bajista (0,61 $) es casi la caja neta.** Supone a la vez que B se va, que el resto de SI crece con k = 1,62 y margen del 30 % y que Space no mejora. Es un escenario de cola, no central.
- **Si el capital es tan improductivo, la dirección puede frenarlo.** En el bajista, dejar de crecer en SI tras el año 1 sube el valor de 0,61 $ a 4,40 $ (03 §5.2).
- **Connectivity es un negocio real** con EBITDA − capex positivo, y el ARPU cae en parte por expansión a mercados nuevos (01 §1.2), no solo por presión competitiva.
- **El 3T26 sí demuestra demanda**: 1,7 GW instalados y contratos adicionales firmados en el trimestre (P5).

### 3.5 Pérdida potencial cuantificada

Frente al precio de 147,49 $ (script §5.8): **−93,5 %** con la combinación desfavorable de §5.7 (9,66 $), **−89,9 %** con el k observado de SI (14,83 $) y **−99,6 %** en el bajista de la Fase 3 (0,61 $). Incluso el alcista queda un −32,4 % por debajo (§1).

---

## 4. Señales observables (umbral, documento, escenario)

Los umbrales salen del modelo (script §4). Los trimestres intermedios se interpolan como 3T26 × (1 + g₁)^(q/4) **[SUPUESTO de esta fase]**. **No existe 10-Q del 4T**: el 4T26 se publicará en el 8-K de resultados y en el **primer 10-K (FY2026)**, con fecha límite inferida del 31-mar-2027 (01 §6.4, SIN VERIFICAR).

| # | Señal | Dónde y cuándo | Umbral bajista | Umbral base | Umbral alcista | Qué hace con los escenarios |
|---|---|---|---|---|---|---|
| S1 | **Ingresos de SI y del grupo en el 1T27** frente a la guía | 8-K y 10-Q del 1T27 (abr-may 2027, fecha SIN VERIFICAR) | Grupo ≈ 12.472 M$ (SI ≈ 5.805) | Grupo ≈ 23.821 M$ (SI ≈ 16.772) | Grupo ≈ 35.284 M$ (SI ≈ 27.985); guía 33.000-37.000 | ≥ 33.000 M$ refuerza el alcista y hace el base demasiado bajo; < 20.000 M$ debilita base y alcista |
| S2 | **Customer B en dólares** (% de Note 3 × ingresos) | 10-K FY2026 (Note de concentración) y 10-Q 1T27 | < 2.514 M$/trimestre (mitad del 3T26), deja de revelarse (< 10 %) o hay 8-K de rescisión | ≈ 5.028 M$/trimestre | ≈ 5.028 M$ y otros clientes ≥ 10 % | Mirar el importe, no el %: si los ingresos llegan a 33.000 M$ y B no cambia, su peso cae al 15,2 % sin que haya pérdida. Por debajo de 2.514 M$ se activa el bajista |
| S3 | **Capex del 4T26 y del 1T27** frente a la guía de 35.000-40.000 M$ | 8-K 4T26 / 10-K FY2026; 10-Q 1T27 | Capex 4T26 ≥ 35.000 y 1T27 ≥ 19.593 sin que S1 llegue a la guía (k sube) | Si el 4T26 es 37.500, el base exige **8.455 M$/trimestre** en 1T-3T27 (−56,8 % frente al 3T26) | El alcista admite 16.756 M$/trimestre | Capex alto **con** S1 en guía es coherente con el alcista; capex alto **sin** S1 refuerza el bajista (k observado → 14,83 $) |
| S4 | **Ingresos de Connectivity** | 8-K 4T26; 10-Q 3T27 (oct-nov 2027) | 4T26 ≈ 5.435 / 3T27 ≈ 6.035 M$ | 4T26 ≈ 5.604 / 3T27 ≈ 6.822 M$ | 4T26 ≈ 5.709 / 3T27 ≈ 7.347 M$ | El 4T26 separa poco los escenarios; el 3T27 sí. Por debajo de 6.035 M$ en el 3T27, Connectivity va por debajo del bajista |
| S5 | **ARPU de consumo de Starlink** | 10-K FY2026 (KBM) y 8-K 4T26 | ARPU 4T26 < 65,9 $/mes (sigue el ritmo de −16,9 % anual) **y** S4 por debajo del base | 66-69 $/mes con suscriptores creciendo | ≥ 69 $/mes (se estabiliza) | Refuerza o debilita la Connectivity del base (18,06 $ de los 25,27 $) |
| S6 | **Margen EBITDA aj. de SI** | 10-Q trimestrales de 2027 (no GAAP por segmento) | < 38,5 % (A1 del bajista) dos trimestres seguidos | 45,1 % en A1 → 50 % en A3 | ≥ 48,5 % en A1 → 60 % en A3 | Margen objetivo de SI del 40 / 50 / 60 % → 15,57 / 25,27 / 34,98 $ (03 §5.2) |
| S7 | **Primer 10-K: vida útil de los equipos de cómputo, bases imponibles negativas y concentración anual** | 10-K FY2026 (hasta ~31-mar-2027, SIN VERIFICAR) | Vida útil de 4 años → 18,87 $ | 5 años → 25,27 $ | 6 años → 29,51 $ | La vida útil es un supuesto de 03 sin verificar; el 10-K la fija |
| S8 | **Starship comercial** | 10-Q/10-K, KBM ("all Starship launches have been classified as internal") | Ningún lanzamiento de Starship clasificado como externo a 4T27 y Space 9M27 < +3 % | Space +5 % en A1, +10 % anual en A2-A5 | Primer lanzamiento externo antes de 4T27 y Space ≥ +10 % en A1 | Efecto pequeño en el modelo (−0,71 $ a +0,88 $), pero es la única métrica pública de la opcionalidad de Space |
| S9 | **Caja + valores negociables** | 10-Q 3T27 (saldo a 30-sep-2027) | < 34.971 M$ antes del año 3 (por debajo del mínimo del base) o ampliación de capital / deuda nueva relevante (8-K) | ≈ 50.259 M$ (89.855 + FCFF A1, sin intereses ni EchoStar) | ≈ 36.693 M$ con ingresos en guía | Una ampliación de capital antes de 2028 indicaría un FCF peor que en los tres escenarios |
| S10 | **Objetivo de 100.000 M$ anualizados en dic-2026** [CALL] | 8-K 4T26 (no se publica el mes; solo el trimestre) | 4T26 < 20.000 M$ | — | 4T26 ≥ 25.000 M$ (ritmo uniforme del objetivo; 3T26: 14.575 M$) | Señal débil por el desfase mes/trimestre; refuerza o debilita S1 |
| S11 | **Capacidad instalada (GW)** | 10-K FY2026 y 10-Q 2027 (KBM "nameplate compute") | Crecen los GW pero no los ingresos de SI | — | 2,5-3 GW a fin de 2026 [CALL] **con** ingresos de SI que los acompañen | Ver §5.1: los 13 GW de fin de 2027 [CALL] no caben en ningún escenario |
| S12 | **Combinación con Tesla** | 8-K (acuerdo de fusión, Item 1.01) o MD&A del 10-K | Acuerdo sin voto separado de los accionistas minoritarios ni *fairness opinion* independiente | — | Cancelación del proceso o canje con mayoría de minoritarios | Gobierno corporativo (§7); el DCF no lo recoge |
| S13 | **Fin del lock-up de Musk (366 días)** | Form 4 y Form 144 desde ~jun-2027 (fecha inferida de P2, SIN VERIFICAR) | Ventas relevantes de Musk o de consejeros | — | Sin ventas | Señal de alineación de intereses, no de valor |

---

## 5. Abogado del diablo contra el caso base de la Fase 3

### 5.1 Normalización del capex: el base supone que el capex se desploma en 2027

- El base pone un capex de **62.864 M$ en el año 1** (oct-26 a sep-27). Si el 4T26 es el punto medio de la guía (37.500 M$), quedan **8.455 M$ por trimestre** para 1T-3T27: un **−56,8 %** frente al 3T26 (19.593 M$). Esa caída no la anuncia nadie.
- Al mismo tiempo, el base solo da el 50 % del extremo bajo de la guía de ingresos. **Es incoherente con la guía en las dos direcciones:** toma poco del aumento de ingresos y casi nada del aumento de capex.
- **Efecto:** capex de SI al ritmo de la guía (125.892 M$/año) en el año 1 → 21,40 $ (03); en los años 1 y 2 → **17,19 $**, con los mismos ingresos.
- **Los 13 GW de fin de 2027 [CALL, SIN VERIFICAR].** A 44,4 $/W, los 11,3 GW nuevos exigirían **502.159 M$ de capex**: 5,6 veces la caja y valores y 8,0 veces el capex del año 1 del base. Con el ingreso por vatio actual (RR de SI / GW = 17,8 $/W), 13 GW darían un RR de SI de 231.247 M$; a 35,6 $/W (k = 1,25), 462.164 M$. El RR de SI a fin del año 1 es de 67.090 M$ en el base y 111.940 M$ en el alcista. **Si la cifra de 13 GW es real, ningún escenario de la Fase 3 la recoge**: o el capex es muy superior (con financiación externa) o el coste por vatio baja mucho. El 44,4 $/W es una cota alta (incluye obra en curso, 03 §3.2).

### 5.2 k de SI: el supuesto con más peso

| k de SI | 0,90 | 1,00 | 1,25 (base) | 1,50 | 1,62 (observado) | 2,00 | 2,50 (implícito hoy) |
|---|---:|---:|---:|---:|---:|---:|---:|
| vpa base | 35,15 $ | 32,33 $ | 25,27 $ | 18,22 $ | 14,83 $ | 4,11 $ | −10,09 $ |

- **k que lleva el base a 0 $: 2,14.**
- El "k implícito hoy" (2,50) divide el capex por vatio (44,4 $/W) entre el ingreso de SI por vatio instalado (17,8 $/W). Es una cota alta: incluye la capacidad para el entrenamiento propio de Grok y la obra en curso. Pero muestra que el 1,25 del base supone que el ingreso por vatio se duplica respecto al actual.

### 5.3 WACC y beta de 1,112

| Variante (resto como en 03) | WACC inicial / terminal | vpa base |
|---|---|---:|
| ERP 3,30 % (mínimo publicado por Damodaran, D1) | 8,59 % / 8,41 % | 31,12 $ |
| Fase 3: solo betas de Damodaran | 8,73 % | 30,40 $ |
| Beta 1,0 (mercado) | 9,11 % / 9,11 % | 26,91 $ |
| **Base (beta 1,112)** | **9,57 % / 9,34 %** | **25,27 $** |
| rf 5,33 % (Treasury a 30 años, M2) | 9,90 % / 9,67 % | 23,67 $ |
| Fase 3: solo comparables | 10,42 % | 21,41 $ |
| ERP 5,67 % (máximo publicado, D1) | 11,18 % / 10,87 % | 18,85 $ |
| Beta de regresión frente a QQQ, 1,83 (sin Blume) | 12,54 % / 10,83 % | 17,46 $ |
| Beta de regresión frente a SPY sin la 1.ª semana, 2,77 | 16,42 % / 12,77 % | 11,49 $ |
| Fase 3: regresión frente a SPY con Blume (2,53) | 15,40 % | 10,09 $ |

**Lectura.** La beta *bottom-up* pondera SI al 67,1 % con una beta desapalancada de 1,188 (media de Damodaran 1,105 y comparables 1,272, n = 2; CoreWeave sin beta publicada). Para un negocio de alquiler de GPU con un cliente del 66,5 % de sus ingresos, una beta de software es probablemente baja. Pero el mercado ha tratado a SPCX con betas de 1,8-3,3 en cuatro meses (03 §1.1), lo que llevaría el base a 10-17 $. **El WACC no explica la distancia al precio en ninguna dirección razonable:** el mínimo de la tabla da 31,12 $.

### 5.4 Customer B: el modelo infravalora su riesgo

- **Los 5,20 $ "de Customer B" de la Fase 3 mezclan tres efectos** (script §3): quitar el crédito a la guía (−2,89 $), la rescisión de B en sí (−0,68 $) y el suelo de capex por compromisos (−1,63 $). Si B rescinde pero el resto de la guía se cumple, el base solo baja a 24,80 $ (−0,48 $).
- **Por qué pesa tan poco:** en el modelo, perder B reduce también la reposición de capex (k × RR / L) y el resto de SI mantiene el margen objetivo del 50 %. Pero la Fase 2 (§9.2) muestra que **sin B el EBITDA aj. de SI del 3T26 caería a entre −75 y 805 M$**. Si B rescinde y el margen objetivo de SI baja al 40 % / 30 %, el base pasa a **16,50 $ / 12,91 $**.
- **Probabilidad.** El base da a B un 100 % de continuidad hasta 2029. Ponderando la rescisión en el año 1 con un 25 % / 50 %: 23,98 $ / 22,68 $ (con el efecto infravalorado de la Fase 3).
- **Renovación en 2029:** sin renovación ni recolocación, 24,40 $; con −50 %, 25,07 $; sin recorte, 25,58 $.
- **426 M$/mes sin contrato documentado:** Customer B factura 1.676 M$/mes y el contrato de P2 es de 1.250 M$/mes. La diferencia puede ser de contratos adicionales (P5) con plazos desconocidos (SIN VERIFICAR).

### 5.5 Peso del valor terminal (86,7 %)

- El valor terminal del base (696.221 M$) equivale a **5,35 veces el EBITDA aj. del año 10** (130.050 M$) y a 15,8 veces el FCFF del año 11. **No es agresivo en múltiplo**: pesa mucho porque los FCFF de los años 1-2 son muy negativos (VA de los años 1-10: 42.987 M$).
- **Sin valor terminal, el base vale 5,90 $.** Los FCFF de los años 1-10 del base no cubren el **97,8 %** del EV de mercado.
- **Valor de salida con múltiplos de mercado en el año 10** (múltiplo × EBITDA aj. A10): 10x → 42,09 $; mediana de Connectivity (13,53x) → 54,87 $; mediana de SI (20,18x) → 78,94 $.
- **Múltiplo de salida que lleva al precio:** 39,1x en el base; **13,8x en el alcista** (su Gordon implícito es de 8,42x).
- **Lectura.** El abogado del diablo aquí juega **a favor** del precio: el Gordon con WACC del 9,34 % y g del 3 % es más conservador que los múltiplos actuales del sector. Con el alcista y un múltiplo de salida de 13,8x (por debajo de la mediana de Connectivity) se llega al precio. La pregunta es si en 2036 un negocio con capex del 24 % de los ingresos merece los múltiplos de hoy.

### 5.6 Base de acciones

| Base | Acciones (M) | vpa base |
|---|---:|---:|
| Diluida de 03 | 14.492,86 | 25,27 $ |
| + los 1.333 M de premios no cumplidos (P3 Note 13) | 15.825,86 | 23,15 $ |
| + solo 30,93 M (si los 1.333 incluyen las 1.302,07 M de Musk ya emitidas) | — | 25,22 $ |
| Diluida sin las restringidas de Musk | 13.190,79 | 27,77 $ |

**Lectura.** La base de acciones mueve el valor entre 23,15 $ y 27,77 $: poco frente al resto de supuestos. El criterio de la Fase 3 (no sumar los 1.333 M) es el correcto si se confirma que incluyen las acciones de Musk (§9, punto 2).

### 5.7 Combinaciones

- **Al alza** (100 % del punto medio de la guía + vida útil de 6 años + WACC solo Damodaran): **43,86 $**.
- **A la baja** (k observado + B no renueva en el año 3 + capex de SI del año 1 al ritmo de la guía + WACC solo comparables): **9,66 $**.
- **Rango del base razonable: 9,66-43,86 $.** Los dos extremos quedan por debajo del precio.

### 5.8 Saldo del abogado del diablo

El base puede ser **demasiado optimista** en k, en el margen de SI sin Customer B y en el capex de 2027; puede ser **demasiado pesimista** en el crédito a la guía, en el margen de SI del 3T26 y en el valor terminal frente a múltiplos de mercado. Los efectos medidos van de 9,66 $ a 43,86 $ en combinación. **Ningún ajuste aislado razonable del base acerca el valor al precio**; solo lo hacen combinaciones sobre el alcista (§6).

---

## 6. Qué tendría que pasar para que 147,49 $ fuese coherente con los fundamentales

Del DCF inverso de la Fase 3 (03 §6) y de combinaciones nuevas sobre el alcista (script §6):

| Camino | Qué exige | vpa |
|---|---|---:|
| Base con más crecimiento (03) | Crecimiento de los años 2-5 × 3,868: ingresos de 1.935.372 M$ en el año 10 (TACC del 50,7 %) | 147,49 $ |
| Base con menor WACC (03) | WACC inicial del 4,63 %, por debajo del tipo libre de riesgo | 147,49 $ |
| Alcista con más crecimiento (03) | × 1,414: ingresos de 825.281 M$ en el año 10 (alcista: 533.131) | 147,49 $ |
| Alcista con más margen de SI (03) | Margen EBITDA aj. de SI del 80,2 % | 147,49 $ |
| **Alcista con menor WACC** | WACC inicial del **7,97 %** (coste del capital del 8,03 %; beta implícita de 0,722 con el rf y el ERP de 03) | 147,49 $ |
| Alcista + WACC solo Damodaran | — | 120,88 $ |
| Alcista + vida útil de 6 años | — | 107,03 $ |
| Alcista + margen de SI del 3T26 (65,5 %) | — | 112,76 $ |
| Alcista + L 6 + Damodaran | — | 129,60 $ |
| **Alcista + las tres cosas** | — | **145,13 $** |
| Alcista con salida a 13,8x EBITDA en el año 10 (§5.5) | — | 147,49 $ |

**Lectura.** El precio es coherente con un mundo en el que se cumple **todo** el alcista —guía del 1T27, Customer B renovado sin recorte, k de 0,90, Connectivity al 22 % anual, Space al 25 %— **y además** uno de estos: un coste de capital propio del ~8 % (beta de ~0,72, menor que la de Connectivity y SI por separado), un margen de SI cerca del 80 %, o una combinación de margen del 3T26, GPU de 6 años y betas de Damodaran. Como referencia, los 825.281 M$ de ingresos del año 10 del alcista ampliado son **2,49 veces** los ingresos TTM de Microsoft (331.840 M$, S6 vía 03 §6; script §5.8). **Para la tesis alcista, el precio no deja margen de error; para la bajista, descuenta un escenario que no ha mostrado todavía ni un trimestre de ingresos a ese ritmo.**

---

## 7. Gobierno corporativo y conflicto de interés

| Factor | Dato | Fuente | Efecto en la tesis |
|---|---|---|---|
| **Control de Musk** | 82,4 % del voto tras la OPV; ≈86,1 % a 15-oct-2026 (estimación, SIN VERIFICAR). Clase B con 10 votos que elige el 51 % del consejo. "Controlled company" con exenciones de Nasdaq | P2 portada; 01 §4.1 | Las decisiones de capex (13 GW), de combinación con Tesla y de reparto de capacidad entre clientes y uso propio no dependen de los minoritarios |
| **Acciones restringidas de Musk** | 1.302,07 M de acciones B (9,6 % de la portada) que votan ya y solo consolidan con una colonia en Marte de 1 M de habitantes o 100 TW de cómputo fuera de la Tierra, además de hitos de capitalización | P2 "2026 Compensation Developments"; 01 §4.1 | Refuerzan el control sin coste económico hoy. Incentivo declarado: capitalización y objetivos de largo plazo, no FCF |
| **Financiación con Valor Equity Partners** (consejero: Antonio Gracias) | Deuda de 12.897 M$ (33,2 % del total), garantizada por SpaceX. Intereses de 351 M$ en el 3T26 y 864 M$ en 9M26. **Coste anualizado del 3T26: 10,9 %** frente al 5,855 % de los Notes: sobrecoste de **649 M$ al año** (0,045 $ por acción y año) | P3 Notes 9 y 17 vía 02 §6; cálculo de esta fase (aproximación: el saldo cambió durante el trimestre y la contabilidad de *failed sale-leaseback* puede incluir componentes distintos del interés) | Poco valor por acción, pero es la mayor operación vinculada y su coste es casi el doble que el de la deuda de mercado |
| **Combinación con Tesla** | Comités especiales en SpaceX y en Tesla; sin términos acordados; requeriría la aprobación "of our controlling shareholder" | P3 MD&A (01 §4.2); S9 [CALL] | Musk tiene ≈20 % de Tesla (P2) y ≈47,8 % del capital de SpaceX (01 §4.1): sus incentivos en la relación de canje no coinciden con los de los minoritarios de ninguna de las dos. Transferir un 5 % / 10 % del valor de SpaceX en el canje equivale a **100.154 / 200.307 M$** a precio de mercado (7,37 / 14,75 $ por acción), o a 1,26 / 2,53 $ sobre el base |
| **Otras vinculadas** | Megapacks de Tesla por 480 M$ (9M26); plusvalía de 561 M$ en The Boring Company (3T26) | P3 Notes 8 y 17 (01 §4.2) | La plusvalía de Boring infla el beneficio neto del 3T26; el modelo no la usa |
| **Derechos de los minoritarios** | Demanda derivada solo con el 3 % del capital (ley de Texas); arbitraje individual obligatorio | P2 Risk Factors (01 §4.1) | Limita el contrapeso en una operación vinculada mal valorada |
| **Dedicación** | Musk "does not devote his full time and attention to our businesses"; también es CEO de Tesla | P2 Risk Factors | Riesgo de persona clave y de conflicto en la asignación de capacidad (cómputo, lanzamientos) entre sus empresas |

**Cómo entra en la tesis.** El gobierno corporativo no cambia el DCF, pero cambia **a quién llega** el valor. Para la tesis alcista, el control de Musk es la condición de la ejecución rápida (de 0,6 a 1,7 GW de cómputo entre el 3T25 y el 3T26, P3 KBM). Para la bajista, es el canal por el que el valor puede salir hacia partes vinculadas (Valor, Tesla) sin voto efectivo de los minoritarios. La señal S12 (§4) es la que decidirá cuál de las dos lecturas pesa más.

---

## 8. Datos SIN VERIFICAR usados en esta fase

- **Guía de la call del 3T26** (capex del 4T26, ingresos del 1T27, 2,5-3 GW a fin de 2026, 13 GW a fin de 2027, ">50 $/W", objetivo de 100.000 M$ anualizados en dic-2026, vuelos semanales de Starship en el 1S27): solo fuentes secundarias (S7, S8, S9). Coinciden entre sí, pero **no hay transcripción ni documento SEC**.
- **Identidad de Customer B** (inferencia de 01: Anthropic) y el origen de los 426 M$/mes por encima del contrato de P2.
- **Vida útil** de los equipos de cómputo (5 años en el modelo).
- **Fechas** del 8-K del 4T26, del primer 10-K (≈31-mar-2027) y del fin del lock-up de Musk (≈jun-2027).
- **Voto actual de Musk** (≈86,1 %): no hay *proxy* posterior a la OPV.
- **Coste de la financiación de Valor** (10,9 %): aproximación con el saldo de cierre.
- **Interpolación trimestral** de los umbrales de §4: supuesto de esta fase, no del modelo.
- **Valor por segmento** de §1: aproximación (impuesto por segmento sin compensar pérdidas).

---

## 9. Devoluciones a fases anteriores

No se han editado documentos de otras fases. Se comunica al orquestador:

1. **Fase 1 §6.1 — apertura del primer día** (pendiente de 03 §8.1). Fase 1 dice 160 $ (S1, secundaria). Nasdaq (M1) da **150,00 $ de apertura** y 160,95 $ de cierre; la diferencia es del 6,7 %. Sobre el precio de la OPV (135 $), la apertura supuso un +11,1 % y el cierre un +19,2 %. Conviene corregir 01 §6.1.
2. **Fase 2 §0 y §7 — posible doble cómputo de los premios de Musk** (pendiente de 03 §8.4). La Fase 2 presenta los 1.333 M de "premios con condiciones de rendimiento no cumplidas" como dilución potencial **adicional**. Si incluyen las 1.302,07 M acciones restringidas de Musk, que ya están en circulación, la dilución potencial pendiente (opciones y RSU + premios + EchoStar, sobre 13.579 M) baja del **16,5 % al 6,9 %**. En valor, 23,15 $ frente a 25,22 $ por acción en el base. La Fase 2 debería confirmarlo con la Note 13 de P3.
3. **Guía de la call del 3T26** (pendiente de 03 §8.5). Esta fase encontró una tercera fuente secundaria (S9, MarketBeat) que coincide con S7 en capex e ingresos y añade el objetivo de 100.000 M$ y los 13 GW atribuidos a Musk. **Sigue SIN VERIFICAR** contra la transcripción.
4. **Fase 3 §0 punto 4 y §5.2 — "Customer B pesa 5,20 $".** La cifra mezcla tres efectos: quitar el crédito a la guía (−2,89 $), la rescisión en sí (−0,68 $) y el suelo de capex (−1,63 $). Además, la variante de rescisión mantiene el margen objetivo de SI en el 50 %, mientras que 02 §9.2 muestra que sin B el EBITDA de SI del 3T26 caería a −75/805 M$. Con margen del 40 % / 30 %, el efecto desde el base sería de −8,78 / −12,36 $ (vpa de 16,50 / 12,91 $; script §5.8). Se propone a 03 presentar la descomposición y la variante con margen.
5. **Fase 3 §3.2 y §3.4 — coherencia del capex del año 1 con la guía.** Con la guía del 4T26, el base exige un capex de 8.455 M$ por trimestre en 1T-3T27 (−56,8 % frente al 3T26), y los 13 GW [CALL] implicarían 502.159 M$. No es un error de cifras, pero el base toma el 50 % de la guía de ingresos y casi nada de la de capex. Se propone a 03 una variante con el capex de la guía en dos años (17,19 $).
6. **Fase 3 §4.1 — base "sin restringidas de Musk".** Resta las acciones de Musk a la base de portada (sin opciones ni EchoStar) pero usa el valor de las acciones de la base sin ajuste de EchoStar; el resultado (30,52 $) no es comparable con la base diluida. Restando las de Musk a la base diluida se obtienen 27,77 $. Es una cifra informativa; no afecta a los escenarios.
7. **Orquestador — "ARPU de Starlink en el 10-Q del 4T26".** No habrá 10-Q del 4T: el 4T26 se publicará en el 8-K de resultados y en el primer 10-K (01 §6.4). Las señales de §4 lo reflejan.

---

## Registro de cambios v1

Primera versión. Sin veredicto previo.
