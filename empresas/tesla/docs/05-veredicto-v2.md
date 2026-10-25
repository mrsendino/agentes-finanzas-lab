# 05 — Veredicto de verificación v2 (Reality Checker, segunda verificación)

**Fecha:** 2026-10-25 · **Rol:** Fase 5, *Reality Checker*. Por defecto, el estado es NECESITA TRABAJO salvo prueba abrumadora en contra · **Objeto:** 01 v2, 02 v2, 03 v2 y 04 v2.1 · **Alcance:** comprobar que el análisis es internamente coherente, que cada cifra se puede rastrear hasta una fuente real y que las conclusiones se siguen de los números. **No es una recomendación de inversión.** Este documento no modifica 01-04. El veredicto v1 ([05-veredicto.md](05-veredicto.md)) se conserva sin cambios como histórico; la copia de v1 de todo el proyecto está en `versiones/v1/`.

**Scripts de esta fase:**

| Script | Qué hace |
|---|---|
| [`scripts/fase5_consistencia.py`](../scripts/fase5_consistencia.py) | Script de v1 con las **expectativas** actualizadas a v2 (registro v1 → v2 en su cabecera). No cambia ningún modelo. Re-ejecuta fase2/3/4 en copia temporal |
| [`scripts/fase5v2_cifras.py`](../scripts/fase5v2_cifras.py) | Nuevo. Compara **todas** las celdas numéricas de las tablas de 02 §2-§6 con `ratios.csv` y un catálogo de cifras del cuerpo de 01, 03 y 04 con la salida viva de fase3/fase4. Redondeo mitad hacia arriba sobre el valor completo |
| [`scripts/fase5v2_muestreo.py`](../scripts/fase5v2_muestreo.py) | Nuevo. Catálogo de 40 cifras v2 no sorteadas en v1. Semilla impresa: **20261025** |
| [`scripts/fase5v2_coherencia.py`](../scripts/fase5v2_coherencia.py) | Nuevo. Misma cifra en todas las fases y cifras de v1 que sobreviven en el cuerpo de v2 |

---

## 0. Veredicto

### **NECESITA TRABAJO (menor)** · Calificación: **B+** (v1: B−)

**Lo que está bien** (con evidencia):
- Los tres scripts se ejecutan con rc = 0. `ratios.csv` y `checks.csv` regenerados son **idénticos byte a byte** a los del proyecto; `data/` no se toca. `fase5_consistencia.py` con las expectativas v2: **0 MISMATCH** en 21 cifras clave.
- `fase5v2_cifras.py` comprueba **541 cifras**. **529 coinciden**, 6 difieren solo por doble redondeo y 3 son erróneas (§2).
- **De las 24 devoluciones de v1, 21 están RESUELTAS, 1 PARCIAL, 0 NO y 2 DISPUTADAS.** Las dos disputadas son W2 y W9, y en las dos la fase tenía razón (§3 y §6).
- Todas las afirmaciones nuevas de fuente primaria se confirman literalmente: nota de BPA, estados de patrimonio de 1T/2T/3T26, Form 4 de Musk, D&A TTM de 6.704 M$, FY2021, "top two" de Wood Mackenzie, 2.256.714 BEV de BYD y la cita del CFO de ~20.000 M$ (§4.1).
- Muestreo nuevo: **19 de 20** cifras pasan (§4.2).
- Se cumplen los criterios de v1 sobre el contenido: ninguna afirmación sin respaldo (6 en v1), ninguna crítica de 04 matemáticamente errónea, la justificación del ROIC es cierta y la línea de dilución está respaldada.

**Por qué no es APTO.** El criterio que fijé en v1 era 0 FAIL de fuente y 0 discordancias. No se cumple:
- **3 cifras no coinciden con la salida del script** y se repiten en 6 lugares. Son redondeos mal hechos (25,9 → 25,8 $; 25,5 → 25,4 $; +19,0 → +18,9 %).
- **1 FAIL de fuente:** la beta de 1,87 de MarketChameleon ya no aparece en la fuente, que hoy da 1,84 con "Data as of October 23, 2026".
- **6 celdas de 02** tienen doble redondeo. Una es titular: el margen operativo TTM, 3,4 % en tres documentos, es en realidad 3,35 %, es decir, 3,3 %.
- **2 referencias cruzadas de 02 desfasadas:** describen como vigentes 03 v1 y 01 v1, que ya se han corregido.

**Lo que no cambia:** ningún hallazgo mueve la conclusión ni su orden de magnitud. El efecto conjunto sobre el valor por acción del caso base es menor de 0,1 $. Es una ronda corta de limpieza, no un nuevo ciclo de análisis.

---

## 1. Re-ejecución de scripts y expectativas v1 → v2

| Script | Resultado |
|---|---|
| `fase2_ratios.py` | rc=0; 94 filas (v1: 81, se añaden 13 sin cambiar ninguna celda de v1; comprobado celda a celda frente a `versiones/v1/data/ratios.csv`); **72 controles: 67 OK + 5 DISCREPANCIA**, como dice 02 §1.3 |
| `fase3_dcf.py` | rc=0; `dcf.xlsx` recalculado con LibreOffice: 0 errores de fórmula y **valores cacheados** idénticos a Python (VPA 10,401 / 24,610 / 55,756 $; diluidos 10,363 / 24,520 / 55,552 $). La observación de v1 "sin valores cacheados" queda resuelta |
| `fase4_opcionalidad.py` | rc=0; no escribe en `data/` |

**Expectativas cambiadas en `fase5_consistencia.py`** (solo valores esperados; los modelos no se tocan):

| Expectativa | v1 | v2 | Script v2 |
|---|---:|---:|---:|
| VPA base | 24,5 | **24,6** | 24,61 |
| VPA alcista | 54,9 | **55,8** | 55,76 |
| EV base | 61.040 | **61.353** | 61.353 |
| EBIT_10 central (04) | 147.561 | **147.527** | 147.527 |
| Controles fase2 | 50 + 5 | **67 + 5** | 67 + 5 |
| Año 1 base: D&A / energía / margen objetivo / FCFF | 7.408 / +12 % / 8,93 % / −5.039 | **6.704 / +8 % / 9,15 % / −5.700** | −5.700 (reconstrucción independiente) |
| Capex bruto año 1 | ~15.900 | **15.884** | 15.884 |
| Tabla 4.1 para interpolar W9 (10,6 % / 11,6 %) | 28,49 / 24,52 | **28,55 / 24,60** | — |
| W2 (texto) | SIN VERIFICAR | **doble cómputo real, resuelto** | — |
| Sin cambio | WACC 11,60 / 9,79 %; VPA bajista 10,4; TACC 36,1 / 27,8 %; 407,4 $; 198 $; 6,6 % | igual | igual |
| Nuevas en v2 | — | VPA diluidos 10,36 / 24,52 / 55,55; D&A 6.704; acciones totalmente diluidas 3.967,3; W9 +1,2 / +4,6 | todas OK |

**Resultado: 0 MISMATCH** (21 de 21).

---

## 2. Cifras de los documentos frente a la salida de los scripts

`python3 scripts/fase5v2_cifras.py`: **541 cifras**. En 02, todas las celdas numéricas de las tablas de §2-§6 (311). En 01, 03 y 04, un catálogo de 230 cifras del cuerpo (las tablas de §3, §4.1, §4.2, §4.3, §5 y §6.3 completas, la §7, el WACC, los rangos de 04, etc.).

| Documento | OK | Doble redondeo | **MISMATCH** |
|---|---:|---:|---:|
| 01 | 18 | 0 | **1** |
| 02 | 305 | 6 | 0 |
| 03 | 172 | 0 | **3** |
| 04 | 34 | 0 | **2** |
| **Total** | **529** | **6** | **6 (3 cifras distintas)** |

### 2.1 MISMATCH (cifra distinta de la que da el script)

| # | Dónde | Dice | Script | Causa |
|---|---|---|---|---|
| **M1** | 03 §4.3 (tabla W9), 03 §8 ("23,6-25,9 $") y 04 §4.1.3 ("24,6 → 25,9 $") | 25,9 $ | **25,848 → 25,8 $** | Doble redondeo (25,85 → 25,9). La diferencia "+1,2 $" sí es correcta. El registro de 04 v2 decía 25,8; el de v2.1 lo cambió a 25,9 |
| **M2** | 03 §6.3 (fila "Sin la SBC por encima de FY2024") y 04 §4.1.1 ("las mismas cifras que 03 v2 §6.3 (25,5 / 26,3 $)") | 25,5 $ | **25,446 → 25,4 $** | Doble redondeo (25,45 → 25,5). El "+0,8 $" y los 25,45 $ de 04 sí son correctos |
| **M3** | 01 §1.1 (Servicios y otros, var. FY25) | +19,0 % | **+18,95 % → +18,9 %** (12.530 / 10.534 − 1) | Heredado de v1. 02 da 18,9 %. En v1 lo clasifiqué como "redondeo" sin pedir corrección: fue un error mío (§6) |

### 2.2 Doble redondeo en 02 (coincide con `ratios.csv`, no con el valor exacto)

`ratios.csv` guarda los porcentajes con 4 decimales y 02 los vuelve a redondear a 1. En seis celdas eso cambia la última cifra:

| Celda de 02 | Dice | Exacto | Debería decir |
|---|---:|---:|---:|
| §3 margen operativo TTM (también 02 §0, 03 §7 y 04 §3.2) | 3,4 % | 3,347 % | **3,3 %** |
| §3 créditos / beneficio operativo FY24 | 39,1 % | 39,05 % | 39,0 % |
| §3 margen neto FY21 | 10,2 % | 10,254 % | 10,3 % |
| §3 crecimiento del beneficio operativo FY22 | 109,3 % | 109,35 % | 109,4 % |
| §2 crecimiento de los ingresos FY22 | 51,3 % | 51,35 % | 51,4 % |
| §4 SBC / ingresos FY24 | 2,1 % | 2,046 % | 2,0 % |

Ya estaban en v1. Mi "0 discordancias" de v1 cubría solo 12 cifras clave, no todas las celdas (§6). Ninguna afecta a un cálculo, porque los scripts usan los valores completos. La del margen operativo TTM es la única visible.

---

## 3. Trazabilidad de las devoluciones de v1

Estado: **RESUELTO** / **PARCIAL** / **NO** / **DISPUTADO** (la fase discrepó de 05 v1; se juzga con la evidencia).

| # | Devolución v1 (05 §5) | Lo que dice la fase que hizo | Verificación de Fase 5 v2 | Estado |
|---|---|---|---|---|
| 4-a | Retirar W3 / §4.1.2 (capex "pesimista") | Retirada; capex año 1 de 15.884 M$ | 04 §4.1.2 tachado; script: 15.884 = 9.180 + 6.704; reconstrucción independiente idéntica | **RESUELTO** |
| 4-b | Retirar W5 (Toyota) | Retirada; script §11 corregido | 04 W5 y script §11: "EV / (EV/Ventas) = ventas" | **RESUELTO** |
| 4-c | Retirar W1 (PER) | Retirada; 457x como alternativa | 04 W1; script §1 etiqueta 457x "no es una corrección" | **RESUELTO** |
| 4-d | Bajar W9 a "+4,5 $" | Midió +1,2 $ (solo WACC años 1-5) y +4,6 $ (desplazando también el terminal); considera coherente +1,2 | Script: +1,24 / +4,60 $. BETA_T = (1,0 + 1,31) / 2 = 1,155, sin beta de regresión: bajar también el WACC terminal contaría dos veces el ajuste. **La fase tiene razón; mi +4,5 era la cota superior** (§6). Queda M1 (25,9 → 25,8) | **DISPUTADO → a favor de la fase** |
| 4-e | W2: reformular como SIN VERIFICAR; no presentar 11,6 / 27,5 / 61,5 $ como corrección | v2: SIN VERIFICAR y VPA retirados. v2.1, con 02 §5.1: **doble cómputo real de ~286 M** | Fuentes verificadas (§4.1): 301 = básica 3.240 → diluida 3.541; ejercicio de 2018 de 303,96 − 17,53 = 286,43 M, restringidas por servicio hasta el 19-ene-2028, ya en la portada. La línea "portada + 301" contaba dos veces ~286 M. **Fase 2 tiene razón y yo me quedé corto** (§6). Los VPA de 04 v1 siguen retirados con razón (−11,0 % de acciones) | **DISPUTADO → a favor de Fase 2** |
| 2-a | Corregir la justificación del ROIC terminal | Texto: "por debajo" del 13,4 %; sensibilidad de 23,6 a 25,5 $ | Script §9 a: mínimo 13,4 %; 03 §2.2 dice "por debajo". Sensibilidad 23,64-25,47 $ OK | **RESUELTO** |
| 2-b | Quitar "techo de la dilución del plan del CEO" | Retirada; §6.5 corregida | 03 §3 y §6.5. La afirmación de v1 "solo recoge una parte" queda invertida, con evidencia (Form 4: 423,7 M en la portada) | **RESUELTO** |
| 2-c | Asimetría costes/ingresos y advertencia de intensidad de capital del software | §6.3 con 6 variantes; §5 con 3,0x | Contenido correcto y presentado como sensibilidad, no como corrección. **Una cifra mal redondeada** (M2: 25,5 → 25,4), que 04 copia | **PARCIAL** |
| 2-d | SpaceX fuera de la caja neta | §6.4: ~2.865 + 962 = 0,97 $/acción | P2 verificado: "presented within Other non-current assets"; plusvalía de 863; activos digitales de 962; other non-current assets de 12.599. ~2.865 es inferencia declarada | **RESUELTO** |
| 2-e | Guía de capex ~20.000 M$ y capex implícito | §2.1: 15.884 M$; 4T26 ~6.986; sin Terafab | T1 literal: "approximately $20 billion for the current year" | **RESUELTO** |
| 2-f | Mecanismo del margen base y del +12 % de energía | §2.3 medida; energía al 8 % y bajista al 0 % | Script §9 e/f reproduce las cifras (9,21 %, −21,6 %, 25,27 %, 8,90 %; +7,5 % GWh / −10,7 % ingreso por GWh). 1,20 × 0,90 = 1,08 | **RESUELTO** |
| 2-g | Advertir de la incoherencia del EV de TipRanks y de n = 2 | Notas ⁴ y ⁵, script | TipRanks re-leído: EV 1,23 bill. $ frente a capitalización de 1,53 bill. $. Aviso impreso por el script | **RESUELTO** |
| 2-h | Mismo denominador en las anclas de margen | `m_ex`, sin redondeo | Diff v1 → v2 de `fase3_dcf.py`: sin cambios no declarados | **RESUELTO** |
| 3-a | FAIL-1 / FAIL-2 (Wood Mackenzie) | "Dos primeros puestos, sin orden"; N1 | N1 re-leído: "retained the top two positions"; no ordena; BYD 3.º; Norteamérica y Europa como dice 01 | **RESUELTO** |
| 3-b | Propagar 02 §8.1 a 01 | 45.447 / 9.523 a la misma fecha; 1.165; 13.014; 787 atribuible | `fase5v2_cifras.py`: 18 de 19 cifras de 01 dependientes de 02 OK; la que falla es M3, que no estaba en la lista de v1 | **RESUELTO** |
| 3-c | Guía de capex en 01 | ~20.000 M$ con cita literal | T1 verificado | **RESUELTO** |
| 3-d | Matizar el margen de energía del 33,1 % | Nota ¹ | T1: "tariff refunds… warranty true-downs"; "20.4% to 33.1%" | **RESUELTO** |
| 3-e | Retirar las marcas "solo secundaria" confirmadas | Retiradas; se mantienen en el BB por línea, China y xAI | Correcto: 02 §1.2 no confirma esas tres | **RESUELTO** |
| 3-f | PER ~327x desfasado | "DESFASADO" | 01 §5 | **RESUELTO** |
| 3-g | BYD 2,26 M: ¿incluye PHEV? | HKEX: 2.256.714 BEV | HKEX verificado: BEV 2.256.714; PHEV 2.288.709; total NEV 4.602.436 | **RESUELTO** |
| 2·4-a | Nota de BPA: descomponer 301 y 713 | §5.1 y 9 controles | Fuentes verificadas (§4.1). El reparto 286 / 15 es una INFERENCIA declarada. La cancelación de las 96 M solo tiene fuente secundaria, que además no da la cifra (declarado) | **RESUELTO** |
| 2·4-b | D&A TTM en el CSV | 6.704 | P4: "TTM … 6,704"; trimestres 1.643 + 1.590 + 1.619 + 1.852 | **RESUELTO** |
| 2·4-c | Etiqueta `fuente_FY2025` | 8 filas | CSV: "Construido: 9M25 … + Q4-25 …" en las 8 filas | **RESUELTO** |
| 2·4-d | Re-verificar FY2021 | `Financial_Report.xlsx` accesible | WebFetch del xlsx: las 19 partidas coinciden (§4.1) | **RESUELTO** |

**Recuento: 24 devoluciones → 21 RESUELTO, 1 PARCIAL, 0 NO, 2 DISPUTADO** (las dos se resuelven a favor de la fase).

Otras observaciones de v1 que no estaban en la lista:
- `dcf.xlsx` sin valores cacheados: **resuelto**.
- W11 (energía en 01): **resuelto**.
- xAI: sigue SIN VERIFICAR en primaria, **declarado** en 01, 03 y 04.

---

## 4. Verificación de fuentes

### 4.1 Afirmaciones nuevas de fuente primaria (WebFetch, 25-oct-2026)

| Afirmación | Fuente | Lo que dice la fuente | Resultado |
|---|---|---|---|
| Básica 3.240 + "Stock-based awards" 301 = diluida 3.541 (3T26); 9M: 3.237 + 302 = 3.539; antidilutivas 17 / 11 M | 10-Q 3T26, nota de BPA | Idéntico | OK |
| "Restricted stock awards will be excluded from the computation of diluted weighted average shares until … earned" | 10-Q 3T26 | Literal | OK |
| Portada de 3.952.757.946 a 15-oct-2026 | 10-Q 3T26 | Literal | OK |
| Saldo 3.751 → 3.949 (30-jun) → 3.953; 202 M en 9M; 4 M en 3T | 10-Q 3T26, estado de patrimonio | Idéntico. El 10-Q de 3T26 no separa 1T y 2T | OK |
| 1T26: +4 M (3.751 → 3.755); básica 3.234 + 304 = 3.538; portada 3.755.723.871 | 10-Q 1T26 | Idéntico | OK |
| 2T26: +194 M, APIC de 322 M$, "equity incentive awards and acquisitions"; básica 3.237 + 303 = 3.540; portada 3.949.547.394 | 10-Q 2T26 | Idéntico | OK |
| Form 4 (16-jun-2026): 303.960.630 ejercidas a 23,34 $; 17.531.857 retenidas (F) a 404,66 $; 710.172.677 directas; vesting el 19-ene-2028; 423.743.904 restringidas del CEO 2025 con proxy irrevocable, vencimientos 2033/2035 | StockTitan (reproducción de un Form 4) | Idéntico. Además: 727.704.534 tras el ejercicio = 423,74 + 303,96, lo que cuadra al millar | OK (agregador de un formulario primario; calidad declarada en `nuevas_fase2_v2.md`) |
| Interim Award: 96.000.000 restringidas (3-ago-2025) | Form 4, PDF en ir.tesla.com | Literal; **sin** cláusula de cancelación | OK |
| Cancelación del Interim Award | Not a Tesla App | "that backup deal was forfeit once the 2018 deal cleared court proceedings". **No da la cifra de 96 M** (habla de un "$29 billion interim award") | OK como secundaria, **más débil de lo que sugiere 02**: la cifra de 96 M sale del Form 4 y la cancelación de la secundaria |
| D&A TTM de 6.704 M$ | Deck 3T26 (P4) | "Depreciation, amortization and impairment – TTM … 6,148 6,291 6,477 6,704"; trimestres "1,625 1,643 1,590 1,619 1,852" | OK |
| D&A 9M26 5.061 y 9M25 4.505 | 10-Q 3T26, flujos | Idéntico | OK |
| FY2021: 19 partidas | 10-K FY2022, `Financial_Report.xlsx` | Ingresos 53.823; ventas 44.125; créditos 1.465; leasing 1.642; energía 2.789; servicios 3.802; BB 13.606; BO 6.523; BN 5.519; FCO 11.497; capex −6.482; SBC 2.121; D&A 2.911; efectivo 17.576 + inversiones 131 = 17.707; deuda 1.589 + 5.245 = 6.834; patrimonio 30.189 | OK (deja de ser riesgo residual) |
| Wood Mackenzie: "top two" sin orden; BYD 3.º; Tesla 1.ª en Norteamérica; Sungrow 1.ª en Europa; top 3: 36 % → 30 %; 76 % | N1 | Literal; CATL no aparece | OK |
| BYD 2025: BEV 2.256.714; PHEV 2.288.709; comerciales 57.013; NEV 4.602.436 | HKEX, 1-ene-2026 | Idéntico ("unaudited") | OK |
| CFO: "approximately $20 billion for the current year"; "primarily from our cash flows from operations"; capacidad de endeudamiento de 30.000 M$ | T1 | Literal | OK |

**Resultado: 16 de 16 OK.** Una matización: la cancelación de las 96 M se apoya en una secundaria que no da la cifra.

**Observación sobre la inferencia 286 + 15 de 02 §5.1.** Es coherente con todos los datos. Pero la frase de 02 según la cual "el mismo papel lo jugaban las 304 M de opciones de 2018 (304 M de 'awards' en 1T26)" es imprecisa. Por el método de tesorería, 304 M de opciones a 23,34 $ con un precio medio de ~400 $ aportan ~286 M, no 304. Las 304 M de 1T26 serían por tanto ~286 + ~18 de empleados. Esto **refuerza** la lectura de que la parte de Musk son ~286 M antes y después del ejercicio, pero la redacción debe corregirse.

### 4.2 Muestreo aleatorio nuevo

`python3 scripts/fase5v2_muestreo.py` → **semilla 20261025**, con un catálogo de 40 cifras v2 que no se sortearon en v1 ni forman parte de §4.1.

**Ronda 1:**

| # | Cifra | Doc | Fuente | Lo que dice la fuente | Resultado |
|---|---|---|---|---|---|
| G28 | Millas sin supervisión "nearly two million", ×8 | 04 §2.2 | P4 | "nearly two million cumulative unsupervised miles"; "grew eightfold quarter over quarter" | OK |
| G25 | Waymo ~400.000 viajes pagados a la semana; >1 M a fin de 2026 | 04 | T3 | "about 400,000 paid rides per week"; "more than 1 million … by the end of this year" (12-feb-2026) | OK |
| G15 | Other income −592 / −535 / +590 / −117 | 02 §3 | P4 | (592) / (535) / 590 / (117) | OK |
| G13 | Deck Q4 2021: BN 5,5 B$; FCF 5,0; capex 6,5; efectivo 17,6 | 02 / checks | D21 | Literal en el texto (las tablas son imágenes) | OK |
| G29 | >75 % de entregas en Norteamérica con FSD de pago [CALL] | 04 §2.2 | T1 | "over 75% of deliveries in North America included a sign-up for paid FSD" (Taneja) | OK |
| G05 | BN 3T26: 787 atribuible / 804 total | 01 §1.2 | P4 | 787 / 804 | OK |
| G27 | 400 MW; Cortex 1 >105; Cortex 2 >120 | 04 §2.2 | P4 | Idéntico | OK |
| G24 | Cierre previo de 374,58 $ (22-oct) | 03 §1 | M2 | "closed at $374.58" el 22-oct-2026 | OK |
| G10 | BB FY25: automoción 12.361 (17,8 %), energía 3.802 (29,8 %) | 01 §1.1 | S1 | 12.361 (17,78 %), 3.802 (29,77 %) | OK |
| G39 | Ingresos FY23 96.773; BO FY24 7.076 | 02 | Deck Q4 2024 | Idéntico | OK |

**10 de 10.** Según la regla, se desconfía de la puntuación y se sortean 10 más.

**Ronda 2:**

| # | Cifra | Doc | Fuente | Lo que dice la fuente | Resultado |
|---|---|---|---|---|---|
| G23 | Other non-current assets 12.599 | 03 §6.4 (fuentes) | P2 | 12.599 (31-dic-25: 5.045) | OK |
| G35 | Toyota EV/EBITDA 9,46; PER 8,8 | 03 §7 | TipRanks | 9,46 / 8,8 (actualizado el 24-oct) | OK |
| G02 | Créditos 9M26 639 frente a 1.451 | 01 §1.2 | P2 | 639 / 1.451 | OK |
| G11 | 3T25: 3.224 + 100 = 3.324; básica 3.227 | 02 §5.1 / 04 §3.2 | 10-Q 3T25 | Idéntico ("awards" 299; diluida 3.526) | OK |
| G38 | Megafactory de Texas de 50 GWh | 03 / 04 | P4 | "planned capacity of 50 GWh" | OK |
| G37 | Megapack "almost sold out" en 2027 [MUSK] | 03 / 04 | T1 | "almost sold out of all Megapacks for 2027" | OK |
| G21 | Apple EV/Ventas 9,36; EV/EBITDA 26,97; PER 39,3 | 03 §7 | TipRanks | Idéntico (24-oct) | OK |
| G03 | Servicios 3T26 4.605 / 3.475; BB 734 | 01 §1.2 | P4 | Idéntico | OK |
| G12 | Portada del 10-K FY25: 3.752.431.984 | fuentes de 02 | P1 | Literal (23-ene-2026) | OK |
| **G19** | **Beta TSLA 1,87 (MarketChameleon, 23-oct)** | **03 §1** | **M8** | **"TSLA has a beta of 1.84"; "Data as of October 23, 2026"** | **FAIL-v2-1** |

**Resumen: 19 de 20.** Alcance de FAIL-v2-1:
- La fuente citada ya no respalda el 1,87. No es reproducible y no hay archivo de la página. La otra mitad de la media (TipRanks, 1,85) sí se confirma.
- Con 1,84, la beta de regresión pasa de 1,86 a 1,845, el WACC inicial de 11,60 % a 11,57 % y el VPA base de 24,61 $ a **24,64 $ (+0,03 $)**. Es inmaterial, pero una cifra que no se puede rastrear no pasa el control.

---

## 5. Coherencia entre fases en v2

`python3 scripts/fase5v2_coherencia.py`, con revisión manual de cada aparición:

| Cifra | Valores en 01-04 v2 | Valoración |
|---|---|---|
| PER | 03 / 04: **410x** (estándar; GuruFocus 410,4x) · 02: 390x (D5, a 354,72 $, etiquetado) · 01: ~327x **DESFASADO** · 457x solo como "alternativa" en 04 · 327,5 en "terceros" (TipRanks re-leído) | **Coherente con etiquetas** |
| Margen operativo TTM | 3,4 % en 02, 03 y 04 | **Igual en todas, pero mal redondeado** (3,35 % → 3,3 %; §2.2) |
| Margen sin créditos TTM | 02: 2,2 % (sobre ingresos totales) · 03 / 04: 2,23 % (sobre ingresos sin créditos) | Dos definiciones **declaradas** (03 §2.1) |
| Acciones | Portada: 3.952,76 / 3.952,8 / 3.953 M · totalmente diluidas: 3.967,3 M · contraste: 3.964,7 M | Coherente. Menor: 03 da +14,5 M y `ratios.csv` +14,6 M por redondeo de la fila de entrada |
| Caja / deuda / caja neta a 30-sep-26 | 45.447 / 9.523 / 35.924 en 01-04. Los 8.180 solo en la nota de 01 como principal a 31-dic-25 | **Coherente**. 45.400 solo sobrevive en la tabla 02 §8.1 (ver E2) |
| VPA | 10,40 / 24,61 / 55,76 $ (portada) y 10,36 / 24,52 / 55,55 $ (totalmente diluidas), redondeados igual en 03 y 04 | **Coherente**. Cosmético: 04 §4 (saldo) dice "10-60 $ (10,4-55,8 $)" y el resto, "10-56 $" |
| Opcionalidad / brecha | 316-362 $ y 85,0-97,2 % en 03 y 04 | Coherente |
| W9 / asimetría | +1,2 / +4,6 $ coherentes; **25,9 y 25,5 erróneos** en 03 y 04 | Ver M1 y M2 |

**Cifras de v1 en el cuerpo de v2:** 34 apariciones. 21 están etiquetadas como v1, retiradas o desfasadas en la misma línea. 13 se revisan a mano: 8 son comparaciones v1 → v2 explícitas o falsos positivos (por ejemplo, el "7,7 %" dentro de "87,7 %"). Las otras 5 son referencias desfasadas reales:
- **E1 (02 §5.1, "Consecuencia para la disputa W2"):** "Las 4.254 M de 03 … sobrestiman" y "03 §6.4 ('el modelo solo recoge una parte') queda invertido" se presentan en presente. 03 v2 ya retiró la línea y corrigió la frase, ahora en §6.5.
- **E2 (02 §8.1, D1-D6, y etiquetas de `checks.csv`):** describen 01 como si siguiera con 45.400, 1.170, 13.010, deuda con fechas mezcladas y "787 GAAP". 01 v2 ya lo corrigió. Los 5 controles "DISCREPANCIA" comparan con valores de **01 v1** etiquetados como "01-negocio.md".

Además, dos observaciones cosméticas:
- 01 §4.1 "423,7 M (~12 % del capital)": es el 12,0 % del capital previo a la emisión, pero el 10,7 % de la portada actual. Hay que indicar la base.
- 04 "10-60 $" frente a "10-56 $".

---

## 6. Dónde me equivoqué en v1

1. **W9.** Di "+4,5 $" como el efecto de la beta sectorial y pedí a Fase 4 que "bajara W9 a +4,5". Ese número sale de interpolar la tabla 4.1, que desplaza también el WACC terminal. Como la beta terminal de 03 (1,155) no contiene la beta de regresión, eso cuenta el ajuste dos veces. **El efecto coherente es +1,2 $**: 03 y 04 tienen razón y mi cifra era la cota superior. En v1 sobrestimé el efecto unas 3,7 veces.
2. **W2.** Lo dejé "SIN VERIFICAR en ambos sentidos". La hipótesis correcta estaba en mi texto ("si las 301 M proceden de acciones restringidas ya emitidas, hay duplicación"), pero no la investigué. Los datos estaban al alcance: tenía delante las 202 M emitidas en 9M26 y no busqué el ejercicio de 2018 de junio de 2026, que es un Form 4 público. **Fase 2 demostró que el doble cómputo era real (~286 M, el 95 % de la línea).** Además, mi caracterización de las 301 M como "opciones, RSU y acciones restringidas no ganadas" ayudó a que 04 v2 concluyera por error que el mecanismo de doble cómputo "pierde su base", cosa que 04 v2.1 tuvo que deshacer. La dirección de 04 v1 era correcta; su mecanismo y su corrección no lo eran (mi crítica a sus VPA sigue en pie: −11,0 % de acciones).
3. **"Discordancias entre script y documento: 0".** Era cierto solo para las ~12 cifras clave que comprobé. Las 6 celdas con doble redondeo de 02 (§2.2) y el +19,0 % de 01 (M3) **ya estaban en v1** y no las detecté. Al +19,0 % lo llamé "redondeo", cuando es un redondeo mal hecho (18,95 % → 18,9 %).
4. **BYD (D-1).** Era un aviso legítimo, pero la comparación resultó homogénea (solo BEV). No era un error del documento.

---

## 7. Comparación v1 → v2

| Indicador | v1 (24-oct) | **v2 (25-oct)** |
|---|---|---|
| Afirmaciones que la fuente no respalda | 6 (FAIL-1, FAIL-2, ROIC, "techo de dilución", W5, W3) | **0** |
| FAIL de fuente en el muestreo | 0 de 20 en valor (+2 FAIL dirigidos) | **1 de 20** (beta de MarketChameleon; inmaterial) |
| Cifras de 01 desfasadas frente a 02 | 5 | **0** (+1 redondeo heredado, M3) |
| Críticas de 04 inválidas o exageradas | 3 + 1 | **0** |
| `fase5_consistencia.py` | 0 MISMATCH (12 cifras) | **0 MISMATCH (21 cifras, expectativas v2)** |
| Cifras de documento comprobadas contra el script | ~40 | **541**: 529 OK, 6 doble redondeo, 6 MISMATCH (3 cifras) |
| Controles de cuadre de Fase 2 | 50 / 55 | **67 / 72** |
| FY2021 | Sin verificar | **Verificado** (19 partidas) |
| `dcf.xlsx` | Sin valores cacheados | **Con caché**, idéntico a Python |
| Dilución | Disputa abierta | **Resuelta**: totalmente diluidas 3.967,3 M; portada + 301 era un doble cómputo |
| Valor por acción del negocio reportado | 10,36 / 24,53 / 54,88 $ | **10,40 / 24,61 / 55,76 $** (diluidas: 10,36 / 24,52 / 55,55) |
| Opcionalidad implícita | 317-362 $ por acción | **316-362 $** |
| Conclusión (orden de magnitud) | Decenas de $ frente a 372 $ | **Sin cambios** |
| Calificación | B− | **B+** |

---

## 8. Devoluciones restantes

| Prio. | Fase | Qué corregir | Por qué |
|---|---|---|---|
| **1** | **Fase 2** | (a) Calcular los % de las tablas desde los valores completos y no desde `ratios.csv` a 4 decimales: margen operativo TTM **3,3 %**, 39,0 %, 10,3 %, 109,4 %, 51,4 %, 2,0 % (§2.2). (b) E1: en §5.1, presentar las 4.254 M y la frase de "03 §6.4" como **03 v1, resuelto en 03 v2 (§3 y §6.5)**. (c) E2: marcar D1-D6 de §8.1 como resueltos en 01 v2 y cambiar las etiquetas de los 5 controles de `checks.csv` a "S2 / 01 v1". (d) Precisar la frase de 1T26 (304 M de "awards" ≈ ~286 de Musk por método de tesorería + ~18 de empleados) y que la secundaria de la cancelación no da la cifra de 96 M | (a) cambia una cifra titular que 03 y 04 copian; por eso va antes que ellas |
| **2** | **Fase 3** | (a) M1: 25,9 → **25,8 $** en §4.3 y §8 ("23,6-25,8 $"). (b) M2: 25,5 → **25,4 $** en §6.3. (c) FAIL-v2-1: volver a citar la beta de MarketChameleon con fecha y valor actuales (1,84), o retirarla; efecto de +0,03 $. (d) Recoger el 3,3 % de Fase 2 en §7. (e) Para evitar que se repita: generar las cifras del documento desde la salida a 1 decimal del script, no redondeando a mano un valor ya redondeado a 2 decimales | Cifras que no coinciden con el script y una fuente que no reproduce el dato |
| **3** | **Fase 4** | Propagar M1 (§4.1.3: "24,6 → 25,8 $") y M2 (§4.1.1: "(25,4 / 26,3 $)"); el 3,3 % en §3.2; "10-60 $" → "10-56 $" en el saldo | Copias de las cifras de 03 y 02 |
| **3** | **Fase 1** | M3: Servicios FY25 **+18,9 %**. Indicar la base del "~12 % del capital" del plan del CEO | Cifra distinta de 02; precisión |

**Criterio para pasar a APTO en la siguiente revisión** (comprobable con los scripts de esta fase):
- `python3 scripts/fase5v2_cifras.py` → **0 MISMATCH y 0 DOBLE REDONDEO**.
- `python3 scripts/fase5_consistencia.py` → 0 MISMATCH.
- La beta citada en 03 §1 reproducible en su fuente.
- `python3 scripts/fase5v2_coherencia.py` → sin referencias de 02 a contenido de v1 presentado como vigente.
- Un muestreo de 10 cifras con otra semilla, sin FAIL.

Es una ronda de limpieza de unas pocas horas. No hace falta un tercer ciclo de análisis.

---

*Reproducibilidad:* `python3 scripts/fase5_consistencia.py`, `python3 scripts/fase5v2_cifras.py [-v]`, `python3 scripts/fase5v2_muestreo.py [semilla]` y `python3 scripts/fase5v2_coherencia.py`. Ninguno escribe en `data/` ni en `docs/`. La verificación contra fuentes se hizo con WebFetch el 25-oct-2026 sobre las URL de `fuentes/fuentes.md` y `fuentes/nuevas_fase*_v2.md`.
