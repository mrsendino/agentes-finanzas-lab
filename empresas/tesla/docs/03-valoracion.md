# 03 — Valoración de Tesla (TSLA): DCF por escenarios, sensibilidad, DCF inverso y múltiplos

**Fecha del análisis:** 2026-10-24 · **Versión:** v3 (2026-10-25, correcciones pedidas en [05-veredicto-v2.md](05-veredicto-v2.md) §8, prioridad 2, y margen TTM de [02-financieros.md](02-financieros.md) v3; ver «Registro de cambios v3» al final. v2: correcciones de [05-veredicto.md](05-veredicto.md) §5) · **Analista:** Fase 3 (rol *Financial Analyst*) · **Precio de referencia:** 372,22 $ (cierre del 23-oct-2026)
**Alcance:** esto es una valoración, no una recomendación de compra o venta. Los resultados se dan como rangos y dependen de los supuestos declarados abajo.

**Archivos de esta fase:**

| Archivo | Contenido |
|---|---|
| [`scripts/fase3_dcf.py`](../scripts/fase3_dcf.py) | Todos los cálculos. Lee `data/ratios.csv` de Fase 2. La §9 del script (nueva en v2) contiene los controles que pidió el veredicto; la §10 (v3) escribe `cifras_03_redondeo.csv` |
| [`data/cifras_03_redondeo.csv`](../data/cifras_03_redondeo.csv) | (v3) Cada cifra de este documento con su valor completo y el texto tal como se escribe, redondeado **una sola vez** (mitad hacia arriba) desde el valor completo |
| [`data/dcf.xlsx`](../data/dcf.xlsx) | Hojas `Supuestos`, `Escenarios`, `Sensibilidad`, `DCF_inverso` y `Multiplos`. En `Supuestos` y `Escenarios` los inputs van en azul y el resto son fórmulas de Excel vivas. **v2:** el script lo recalcula con LibreOffice al guardarlo, así que el archivo ya lleva los valores cacheados. Los valores coinciden con Python y no hay errores de fórmula. **v3:** en el equipo de esta ronda no hay LibreOffice, así que el libro se guarda sin valores cacheados (las fórmulas son las mismas; se recalcula al abrirlo en Excel o LibreOffice) |
| [`fuentes/nuevas_fase3_v2.md`](../fuentes/nuevas_fase3_v2.md) | Fuentes nuevas o re-leídas en v2 |
| [`fuentes/nuevas_fase3_v3.md`](../fuentes/nuevas_fase3_v3.md) | (v3) Re-consulta de las dos betas de regresión |

No hay ningún cálculo hecho a mano en este documento: todas las cifras salen de la salida del script. **v3:** se copian de la columna `texto` de `data/cifras_03_redondeo.csv`, no redondeando a mano una cifra ya redondeada.

---

## 0. Resumen

1. **El DCF del negocio que Tesla reporta hoy no se acerca al precio.** Con supuestos que van desde un estancamiento hasta volver al mejor margen de su historia, el valor por acción queda entre **~10 $ y ~56 $**, con **~25 $ en el caso base**. El precio es de 372 $. Con la cifra de acciones totalmente diluidas (~3.967 M) los valores apenas cambian: 10,4 / 24,6 / 55,7 $.
2. **Entre el 85 % y el 97 % de la capitalización (1,47 billones $) no se explica** por los flujos de automoción, energía y servicios proyectados con los datos de Fase 1 y Fase 2. Esa diferencia es lo que el mercado paga por la opcionalidad: robotaxi, Optimus, FSD como software y cómputo de IA. Parte de ese importe corresponde a un gasto en esas iniciativas que el DCF ya carga al negocio actual (§6.3).
3. **Para justificar el precio con un DCF convencional** hace falta que los ingresos crezcan entre un **~28 % y un ~36 % anual durante 10 años**, es decir, que se multipliquen por 12 a 22 veces, con márgenes operativos del 20-30 %. Con la intensidad de capital de un negocio de software, la exigencia baja al ~26-32 % anual, que sigue siendo multiplicar los ingresos por 10 a 16 (§5). Nada parecido aparece en la historia reportada.
4. **Ni tocando el WACC ni el crecimiento terminal se cierra la brecha.** Con un WACC 3 puntos más bajo y un crecimiento terminal del 4 %, el caso base sube solo hasta ~51 $.
5. **Por múltiplos, Tesla cotiza a 13,9x EV/Ventas.** Esto se parece más a Nvidia (21x) o Apple (9,4x) que a los fabricantes de coches (~1x). Su EV/EBITDA (141x), su EV/EBIT (414x) y su PER (410x) no tienen comparación con ningún par.

**Qué cambia en v2 (detalle en el registro final).** El valor del caso base pasa de 24,5 $ a 24,6 $. Los cambios de supuestos se compensan entre sí: energía más baja, D&A real más baja (y por tanto más reinversión neta) y anclas de margen calculadas sobre el denominador correcto. La línea de dilución de v1 (portada + 301 M) contaba dos veces ~286 M de acciones y se sustituye por la cifra totalmente diluida de Fase 2.

**Qué cambia en v3.** Las dos betas de regresión se han vuelto a consultar y ambas dan hoy 1,84 (v2: 1,85 y 1,87). El WACC inicial baja de 11,60 % a 11,55 % y el caso base pasa de 24,61 $ a 24,65 $ (+0,04 $), que a un decimal es **24,7 $** (v2: 24,6 $). Ninguna conclusión cambia.

---

## 1. Inputs de mercado (con fuente y fecha)

| Input | Valor | Fuente y fecha |
|---|---|---|
| Precio TSLA | **372,22 $** | Cierre del 23-oct-2026 (−0,63 %), según [Benzinga](https://www.benzinga.com/quote/TSLA) (campo "Close") y [MarketChameleon](https://marketchameleon.com/Overview/TSLA/Summary/). Coincide con [GuruFocus, 23-oct-2026](https://www.gurufocus.com/news/9140534/tech-selloff-and-rising-oil-prices-pressure-markets-tesla-tsla-dips-amid-sector-weakness). El cierre previo, 374,58 $ el 22-oct, figura en [heygotrade](https://www.heygotrade.com/en/us-stock/tsla/) |
| Acciones en circulación | **3.952,76 M** | Portada del [10-Q 3T 2026 (P2)](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066775/tsla-20260930.htm): 3.952.757.946 acciones a 15-oct-2026. Según 02 §5.1, **ya incluye** las 423,7 M restringidas del plan del CEO 2025 y las ~286,4 M netas del ejercicio de opciones de 2018 |
| Acciones totalmente diluidas (aprox.) — v2 | **3.967,3 M** | 02 §5.1 (fila `acc_totalmente_diluidas_aprox` de `ratios.csv`): portada + ~15 M de incentivos de empleados aún no emitidos. Contraste: media diluida 3T26 + restringidas del CEO 2025 = 3.541 + 423,7 = 3.964,7 M (el script comprueba que la diferencia es menor de 5 M). Ver advertencias en §3 |
| Media ponderada diluida y básica de 3T 2026 | 3.541 M y 3.240 M | P2, nota de BPA |
| Capitalización | **1.471.296 M$** | Calculada como precio × acciones de portada. Contraste: 1,47 billones $ según GuruFocus y Benzinga (23-oct-2026) |
| Caja neta | **35.924 M$** | Fase 2, saldo a 30-sep-2026 (45.447 de caja − 9.523 de deuda). **No incluye** la participación en SpaceX ni los activos digitales (§6.4) |
| Valor de la empresa (EV) de mercado | 1.435.372 M$ | Calculado como capitalización − caja neta |
| Tipo libre de riesgo (bono a 10 años de EE. UU.) | **4,97 %** | 4,967 % el 23-oct-2026, ~15:53 ET; cierre del 22-oct en 4,954 %. Fuente: [Mortgage News Daily](https://www.mortgagenewsdaily.com/treasury/10yr) |
| Prima de riesgo del mercado (ERP) | **4,20 %** | ERP implícito del S&P 500 a 1-oct-2026, "trailing 12 month, with adjusted payout", según la [página de Damodaran](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm). La variante con rendimiento en efectivo de los últimos doce meses da 3,70 % |
| Beta de regresión — **v3** | 1,84 y 1,84 → **1,84** | [TipRanks](https://www.tipranks.com/stocks/tsla/statistics) ("Beta 1.84"; fecha de modificación de la página 24-oct-2026) y [MarketChameleon](https://marketchameleon.com/Overview/TSLA/Summary/) ("TSLA has a beta of 1.84"; "Data as of October 23, 2026"). Ambas consultadas el 25-oct-2026 (`fuentes/nuevas_fase3_v3.md`). Ninguna de las dos fuentes indica la ventana de cálculo. v2 citaba 1,85 y 1,87, que ya no aparecen en ninguna de las dos páginas |
| Beta del sector, desapalancada | **1,31** | [Damodaran, betas por sector de EE. UU.](https://pages.stern.nyu.edu/~adamodar/New%5FHome%5FPage/datafile/Betas.html) (ene-2026): Auto & Truck, 33 empresas, corregida por caja |
| Diferencial de la deuda sobre el tipo libre de riesgo | 1,0 % | **SIN VERIFICAR.** Es un supuesto: no se consultó el rating vigente. Su efecto es inmaterial, porque la deuda pesa un 0,6 % del capital |
| Tipo impositivo | 21 % | Tipo federal de EE. UU., con el mismo criterio que Fase 2 (§6) |

### 1.1 WACC

| Paso | Valor | Cómo se obtiene |
|---|---|---|
| Deuda / capitalización | 0,65 % | 9.523 / 1.471.296 |
| Beta *bottom-up* reapalancada | 1,32 | 1,31 × (1 + 0,79 × D/E) |
| **Beta inicial** | **1,58** | Media al 50 % de la regresión (1,84) y la *bottom-up* (1,32). La regresión refleja la volatilidad real de la acción; la del sector, el negocio que genera los flujos que se descuentan |
| Coste del capital propio inicial | 11,60 % | 4,97 % + 1,58 × 4,20 % |
| Coste de la deuda después de impuestos | 4,72 % | (4,97 % + 1 %) × 0,79 |
| **WACC inicial (años 1-5)** | **11,55 %** | Deuda al 0,64 % del capital |
| Beta terminal | 1,16 | Punto medio entre el mercado (1,0) y el sector del automóvil (1,31) |
| **WACC terminal (años 6-10 en convergencia lineal; perpetuidad)** | **9,79 %** | — |

Usar solo la beta de regresión (1,84) subiría el WACC inicial a ~12,6 %. Usar solo la del sector lo bajaría a ~10,5 %. El efecto de esta segunda opción sobre el valor se mide en la §4.3 (W9).

---

## 2. Estructura del modelo y supuestos

### 2.1 Mecánica

- **Año 0** = últimos doce meses (TTM) a 3T 2026, de Fase 2: ingresos de 103.570 M$ y beneficio operativo de 3.466 M$. **Margen operativo sin créditos del 2,23 %**, calculado como (beneficio operativo − créditos) / (ingresos − créditos). La v1 usaba el 2,21 % de Fase 2, calculado sobre ingresos totales; ver §2.2 sobre el denominador. La proyección cubre 10 años y descuenta a final de cada año, lo que es conservador frente a descontar a mitad de año.
- **Ingresos por segmento**: automoción sin créditos (73.822), energía (12.265), servicios y otros (16.302) y créditos regulatorios (1.181). Cada segmento sigue su propia senda de crecimiento: constante en los años 1-5 y con un descenso lineal hasta el crecimiento terminal en el año 10.
- **Créditos regulatorios**: 40 %, 10 % y 0 % del importe TTM en los años 1, 2 y 3, y nada después. La ley OBBBA restringe estos programas (Fase 1 §4) y en 3T 2026 ya cayeron un −73 %. Se les asigna un margen de ~100 %, igual que en Fase 2.
- **Margen operativo sin créditos**: pasa linealmente del 2,23 % TTM al margen objetivo del escenario en el año 5 y se mantiene después. Se aplica sobre los ingresos **sin** créditos: EBIT = margen × (ingresos − créditos) + créditos.
- **FCFF** = EBIT × (1 − 21 %) − reinversión neta.
  - **La compensación en acciones (SBC) se trata como un coste real.** El EBIT GAAP ya la descuenta (4.300 M$ TTM, el 4,2 % de los ingresos) y **no se suma de vuelta**. Equivale a suponer que Tesla pagara esa retribución en efectivo. El valor por acción se calcula sobre las 3.953 M de acciones de portada, que ya incluyen las acciones restringidas del plan del CEO 2025 y las del ejercicio de 2018. La tabla de la §3 añade una columna con las acciones totalmente diluidas (~3.967 M).
  - **Reinversión neta** (capex − amortización + circulante):
    - En los años 1-2 es el máximo entre (a) el **8,40 % de los ingresos**, que es el capex neto TTM: capex de 15.407 M$ menos la **amortización, depreciación y deterioro TTM de 6.704 M$** (Fase 2 v2, reconciliación EBITDA de P4), y (b) el aumento de ingresos dividido por el ratio ventas/capital.
    - Desde el año 3 es solo el aumento de ingresos dividido por el ratio ventas/capital.
    - Referencias de Fase 2 para ese ratio: **1,94x** sobre el capital invertido neto de caja (A) y **1,05x** sobre el capital bruto (B).
  - **Capex frente a la guía de la empresa.** El CFO revisó el capex de 2026 a **~20.000 M$** en la call de 3T26 ([T1](https://www.fool.com/earnings/call-transcripts/2026/10/22/tesla-tsla-q3-2026-earnings-call-transcript/), 22-oct-2026), a la baja desde ">25.000 M$" (T10, call de 1T26). **El modelo no usa esa cifra**, porque modela la reinversión como porcentaje de los ingresos. El capex bruto que implica el año 1 del caso base es de **15.884 M$**: 9.180 M$ de reinversión neta más 6.704 M$ de D&A. Queda **4.116 M$ por debajo** de la guía. Hay que tener en cuenta dos matices:
    - El año 1 del modelo va de oct-2026 a sep-2027 y la guía es del año natural 2026. Con 13.014 M$ ya invertidos en 9M26 (P2), la guía implica ~6.986 M$ en 4T26.
    - El modelo **no incluye la Terafab**: "tens of billions" hasta 2028 y ">100.000 M$" a largo plazo, según Musk (T1).
    Por tanto, el modelo no es pesimista en capex; si acaso, es ligero. Mantener la D&A TTM constante en el año 1 es una aproximación, porque la D&A está subiendo (1.852 M$ en 3T26).
- **Valor terminal** = NOPAT₁₁ × (1 − g / ROIC terminal) / (WACC terminal − g). Así la reinversión es coherente con el crecimiento: no se puede crecer en perpetuidad sin reinvertir.
- **Valor de las acciones** = EV + 35.924 M$ de caja neta.

### 2.2 Supuestos por escenario y su justificación

| Supuesto | Bajista | Base (media FY21-24) | Alcista | Justificación (datos de Fase 1 y Fase 2) |
|---|---:|---:|---:|---|
| Crecimiento de automoción sin créditos, años 1-5 | 1 % | 4 % | 8 % | TACC FY21-25: 10,2 %. FY24: −6,5 %. FY25: −9,8 %. 9M26: +10,6 %, pero 3T26 −3 % y un "lower ASP" (P4). BYD vende más VE (Fase 1 §3). El 8 % alcista supone una recuperación de volumen sostenida sin volver a 2021-22 |
| Crecimiento de energía, años 1-5 — **v2** | **0 %** (v1: 5 %) | **8 %** (v1: 12 %) | 20 % | Ver §2.3. 9M26: −5,7 %; 3T26: −16 %; TTM frente a FY25: −4,0 %. Los GWh desplegados crecen (+7,5 %) pero el ingreso por GWh cae (−10,7 %) |
| Crecimiento de servicios y otros, años 1-5 | 10 % | 15 % | 22 % | TACC FY21-25: 34,7 %; 9M26: +41 %. Es la línea que más crece, pero sin desglose (SIN VERIFICAR en Fase 2) y con un margen bruto del 15,9 % |
| **TACC resultante de los ingresos a 10 años** | **2,5 %** | **5,5 %** | **9,8 %** | Salida del modelo. Las TACC históricas FY21-25 fueron del 15,2 % en total, pero del −1,0 % anual entre FY23 y FY25 |
| **Margen operativo objetivo sin créditos (desde el año 5)** — **v2** | **3,54 %** | **9,15 %** | **14,91 %** | Bajista = media FY24-25. Base = media FY21-24. Alcista = máximo histórico (FY22). **v2:** todos calculados como (EBIT − créditos) / (ingresos − créditos), el mismo denominador al que se aplican, y sin redondeo intermedio. Por año: 9,66 % (FY21), 14,91 % (FY22), 7,48 % (FY23), 4,54 % (FY24), 2,54 % (FY25); TTM 2,23 %. El mecanismo del caso base se explica en §2.3 |
| Ventas / capital incremental | 1,2x | 1,5x | 2,0x | Entre el 1,05x (B) y el 1,94x (A) de Fase 2. El alcista supone más eficiencia que la actual |
| Crecimiento terminal (g) | 2,5 % | 3,0 % | 3,5 % | Siempre por debajo del tipo libre de riesgo nominal (4,97 %). **No se usa g para meter la opcionalidad** (ver §6) |
| ROIC terminal — **v2: justificación corregida** | = WACC (9,8 %) | 12 % | 15 % | **Bajista:** el crecimiento no crea valor. **Base, 12 %:** está **por debajo** del rango del ROIC A de FY21-24 (13,4-48,0 %; mínimo en FY24, Fase 2 §6) y **por encima** del ROIC A de FY25 (7,6 %) y del TTM (5,5 %). Supone un diferencial modesto de 2,2 puntos sobre el WACC terminal (9,79 %) para una empresa madura con ventaja de escala. Es un punto intermedio entre el ROIC de hoy y el peor año de 2021-24, no un valor "dentro del rango histórico". **Alcista, 15 %:** sí está dentro de ese rango, cerca de su parte baja. Sensibilidad en §4.3: de 23,7 $ (ROIC = WACC) a 25,5 $ (15 %) en el caso base |
| Robotaxi, Optimus, cómputo de IA | 0 | 0 | 0 | No tienen ingresos separados ni métricas públicas (Fase 1 §5). Se tratan aparte, en la §6 |

**Nota sobre el escenario alcista.** No es un escenario optimista sobre la tesis completa de Tesla. Es el escenario optimista **del negocio que se reporta hoy**: los tres segmentos crecen con fuerza y el margen vuelve a su máximo. Lo que el mercado descuenta más allá de eso se trata explícitamente en la §5 y la §6.

### 2.3 Por qué el caso base usa un margen del 9,15 % y un +8 % en energía (v2)

**"Base" no significa "extrapolación de 2023-26".** Es la vuelta a la media de FY21-24. Los datos de 2023 a 2026 muestran un margen que **cae** (7,5 % → 4,5 % → 2,5 % → 2,2 %), así que el caso base supone que esa tendencia se da la vuelta. Desde v2 la columna se rotula «Base (media FY21-24)» para que no sugiera una centralidad que los datos recientes no apoyan. Lo que este caso exige es lo siguiente (script §9 e):

| Para pasar del 2,23 % TTM al 9,15 % en el año 5 hace falta… | Dato TTM | Exigencia | Referencia histórica |
|---|---:|---:|---|
| …con margen bruto sin créditos constante, que los gastos operativos bajen como % de los ingresos | 16,12 % (16.508 M$) | **9,21 %**: un gasto operativo de 12.948 M$ en el año 5, **−21,6 % en términos absolutos** con ingresos un 37 % mayores (140.626 M$ sin créditos) | Mínimo FY21-25: 9,0 % (FY22) |
| …o, con gastos operativos / ingresos constantes, que suba el margen bruto sin créditos | 18,35 % | **25,27 %** | Máximo FY21-25: 23,9 % (FY22): **no se ha alcanzado nunca** |
| …o una combinación: el margen de partida sin la SBC extra del plan del CEO (+2.301 M$ sobre FY24) ni la I+D incremental de 3T26 anualizada (+4.524 M$) | 2,23 % | **8,90 %**, casi el mismo margen objetivo | Ver §6.3 |

**Mecanismo implícito.** El 9,15 % equivale aproximadamente a suponer que el aumento de gasto de 2025-26 en I+D de IA y en SBC del plan del CEO **deja de pesar sobre el negocio actual**. Puede ocurrir de dos formas: que ese gasto se estabilice mientras crecen los ingresos, o que lo financien ingresos de negocios nuevos que este DCF no modela. Lo otro que llevaría al 9,15 %, un margen bruto del 25 %, no tiene precedente en la serie. Es un supuesto exigente, no neutral. La tabla 4.2 da su sensibilidad: con un margen objetivo del 6 %, el caso base vale ~16 $.

**Energía.** La v1 justificaba el +12 % con la TACC de 2021-25 (46 %), pero los datos de 2026 van en contra. Los datos son estos (script §9 f; GWh de P4/P6, ingresos de Fase 2):

| | FY2025 | TTM 3T26 | Variación |
|---|---:|---:|---:|
| Ingresos de energía (M$) | 12.771 | 12.265 | −4,0 % |
| Almacenamiento desplegado (GWh) | 46,7 | 50,2 | +7,5 % |
| Ingreso por GWh (M$; incluye solar y leasing, aproximación) | 273,5 | 244,3 | −10,7 % |

El volumen crece, pero el precio cae más deprisa. Tesla ya anunció compresión de margen por "low-cost competition" (S4), y el 76 % del mercado está en manos de integradores chinos (S9). Por eso, en v2:
- **Base, +8 %:** por ejemplo, +20 % anual de GWh (la Megafactory de Texas añade 50 GWh de capacidad, tanto como los despliegues TTM; 04 §2) con una caída del ingreso por GWh del −10 % anual, la misma de los últimos 12 meses. O bien +8 % de volumen con precio estable.
- **Bajista, 0 %:** el precio compensa el volumen. Con las tasas TTM (+7,5 % y −10,7 %), el resultado sería −4,0 % anual: el 0 % sigue siendo más benigno que la tendencia actual.
- **Alcista, +20 %:** sin cambios. Exige que el volumen crezca ~30 % anual con una caída de precio moderada. Megapack "almost sold out" en 2027 es una declaración de Musk (T1), no un dato.

---

## 3. Resultados por escenario

| Escenario | Ingresos año 10 (M$) | EBIT año 10 (M$) | VP FCFF años 1-10 | VP del valor terminal | % del EV en el valor terminal | EV (M$) | Valor de las acciones (M$) | **Valor por acción (portada, 3.952,8 M)** | Valor por acción (totalmente diluidas, 3.967,3 M) | vs. precio (372,22 $) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Bajista | 132.730 | 4.704 | −8.452 | 13.676 | 262 %¹ | 5.225 | 41.149 | **10,4 $** | 10,4 $ | −97 % |
| **Base (media FY21-24)** | 176.762 | 16.169 | 10.438 | 51.088 | 83 % | 61.526 | 97.450 | **24,7 $** | 24,6 $ | −93 % |
| Alcista | 263.026 | 39.213 | 47.558 | 137.390 | 74 % | 184.948 | 220.872 | **55,9 $** | 55,7 $ | −85 % |

¹ En el bajista los FCFF de los años 1-10 suman un valor presente negativo, por la ola de capex y un margen que apenas se recupera. Por eso el valor terminal supera el 100 % del EV. Casi todo el valor de este escenario es la caja neta: 35.924 M$, unos 9,1 $ por acción.

**Rango de valor por acción del negocio reportado: ~10 $ a ~56 $; caso base ~25 $.**

**Acciones: por qué la columna diluida apenas se mueve (v2).** La línea de v1 sumaba las 301 M de diferencia entre la media diluida y la básica de 3T26 a las acciones de portada (4.254 M en total). Fase 2 (02 §5.1) demuestra que eso es un **doble cómputo de ~286 M**: esas acciones son las netas del ejercicio de 2018, ya emitidas y ya dentro de la portada. La v1 llamaba a esa línea "techo de la dilución del plan del CEO", pero ninguna fuente vincula las 301 M con ese plan. **Esa etiqueta se retira.** La v2 usa la cifra totalmente diluida de Fase 2:
- **3.967,3 M** = portada (3.952,8 M) + ~15 M de incentivos de empleados aún no emitidos.
- Contraste: 3.541 M (diluida 3T26) + 423,7 M (restringidas del CEO 2025) = 3.964,7 M. La diferencia de ~3 M es desfase entre media y saldo.

Advertencias que 02 §5.1 declara y que aquí se mantienen:
- El reparto de las 301 M en ~286 M (ejercicio de 2018) y ~15 M (empleados) es una **INFERENCIA**: el 10-Q no desglosa la línea "stock-based awards".
- La cancelación de las 96 M del *Interim Award* de 2025, que entra en el cuadre de las 202 M emitidas en 9M26, **solo la confirma una fuente secundaria**.
- Las 423,7 M del plan del CEO 2025 están en la portada (emitidas legalmente), pero **no "ganadas"**: si no se cumplen los hitos, se cancelan. Ver §6.5.

Con todo ello, la portada ya es casi la cifra totalmente diluida: la diferencia es de 14,5 M de acciones, un 0,4 %.

**FCFF del caso base por año (M$):** −5.700, −5.071, 1.245, 2.552, 4.118, 4.928, 5.877, 6.951, 8.119 y 9.341. Los dos primeros años son negativos y reflejan lo que ya se ve en el TTM: el FCF menos la SBC es de −997 M$ (Fase 2 §4). Son más negativos que en v1 (−5.039 y −4.428) porque, con la D&A real, el capex neto TTM pasa del 7,7 % al 8,4 % de los ingresos.

---

## 4. Sensibilidad (caso base)

### 4.1 WACC inicial × crecimiento terminal (valor por acción, $)

El WACC terminal se desplaza lo mismo que el inicial.

| WACC inicial \ g | 2,0 % | 2,5 % | 3,0 % | 3,5 % | 4,0 % |
|---|---:|---:|---:|---:|---:|
| 8,55 % | 38,8 | 40,8 | 43,2 | 46,4 | 50,7 |
| 9,55 % | 32,1 | 33,1 | 34,4 | 35,9 | 37,8 |
| 10,55 % | 27,5 | 28,0 | 28,6 | 29,4 | 30,3 |
| **11,55 %** | 24,0 | 24,3 | **24,7** | 25,0 | 25,5 |
| 12,55 % | 21,5 | 21,6 | 21,8 | 21,9 | 22,1 |
| 13,55 % | 19,4 | 19,5 | 19,6 | 19,6 | 19,7 |

### 4.2 Margen operativo objetivo × multiplicador del crecimiento de los años 1-5 (valor por acción, $)

| Margen \ crecimiento × | 0,5x | 1,0x (base) | 1,5x | 2,0x |
|---|---:|---:|---:|---:|
| 6 % | 16,3 | 16,4 | 16,3 | 16,0 |
| 9 % | 22,8 | 24,3 | 26,1 | 28,2 |
| 12 % | 29,2 | 32,2 | 35,8 | 40,5 |
| 15 % | 35,6 | 40,1 | 45,6 | 52,7 |
| 20 % | 46,4 | 53,2 | 61,9 | 73,2 |
| 25 % | 57,1 | 66,4 | 78,3 | 93,6 |

### 4.3 ROIC terminal y beta (v2)

**ROIC terminal del caso base** (resto de supuestos sin cambios):

| ROIC terminal | Igual al WACC terminal (9,79 %) | 10 % | **12 % (base)** | 13,4 % (mínimo FY21-24) | 15 % |
|---|---:|---:|---:|---:|---:|
| Valor por acción | 23,7 $ | 23,8 $ | **24,7 $** | 25,1 $ | 25,5 $ |

Que la justificación de v1 fuera incorrecta no cambia el resultado: entre "sin creación de valor" y el 15 % hay menos de 2 $.

**W9: beta solo sectorial.** El argumento de coherencia de Fase 4 es válido: los flujos que se descuentan son los de un negocio industrial, y la beta de regresión mide la volatilidad de una acción que cotiza la opcionalidad. Hay dos formas de aplicarlo, con efectos distintos:

| Variante | WACC años 1-5 | WACC terminal | VPA base | Diferencia |
|---|---:|---:|---:|---:|
| **Modelo (beta mezclada 50/50)** | 11,55 % | 9,79 % | **24,7 $** | — |
| Beta sectorial (1,32) solo en los años 1-5 | 10,46 % | 9,79 % | 25,8 $ | **+1,2 $** |
| Beta sectorial y WACC terminal desplazado lo mismo (como la tabla 4.1) | 10,46 % | 8,70 % | 29,1 $ | +4,4 $ |

**El modelo mantiene la beta mezclada.** La variante coherente es la segunda, **+1,2 $**. La beta terminal (1,16) ya es una beta de empresa madura que no incluye la de regresión, así que bajar también el WACC terminal contaría dos veces el mismo ajuste. La tercera fila (+4,4 $) es la cota superior; es lo que medía Fase 4 (+4,6 $ con la beta de regresión de v2, 1,86) y está cerca de los ~+4,5 $ de 05.

**Lectura:**
- **El margen es la variable dominante.** Con márgenes bajos, crecer más que en el caso base **destruye** valor (fila del 6 %: 16,4 $ con 1,0x, 16,0 $ con 2,0x), porque cada dólar de ingresos nuevos exige ~0,67 $ de capital y rinde menos que el WACC.
- **El WACC, g, la beta y el ROIC terminal mueven el resultado en unidades o decenas de dólares, no en cientos.** Ninguna combinación razonable de las tablas pasa de ~100 $ por acción.
- **La conclusión es robusta.** El valor del negocio reportado está un orden de magnitud por debajo del precio. Cambios del 15 % en cualquier supuesto no lo alteran.

---

## 5. DCF inverso: ¿qué tiene que creerse el mercado para justificar el precio actual?

**Planteamiento.** Se busca qué TACC uniforme de los ingresos durante 10 años iguala el valor por acción a 372,22 $, para cada margen operativo alcanzado en el año 10. Supuestos fijos:
- WACC base;
- g = 3 %;
- ventas/capital de 1,5x;
- impuesto del 21 %;
- sin créditos;
- ROIC terminal = máx(12 %, ROIC implícito del margen).

| Margen operativo en el año 10 | **TACC necesaria de los ingresos** | Ingresos en el año 10 (M$) | Múltiplo sobre el TTM | EBIT en el año 10 (M$) |
|---|---:|---:|---:|---:|
| 10 % | 61,7 % | 12.671.686 | 122,3x | 1.267.169 |
| 15 % | 43,7 % | 3.878.013 | 37,4x | 581.702 |
| **20 %** | **36,0 %** | **2.248.629** | **21,7x** | 449.726 |
| **25 %** | **31,3 %** | **1.571.868** | **15,2x** | 392.967 |
| **30 %** | **27,8 %** | **1.202.840** | **11,6x** | 360.852 |
| 35 % | 25,1 % | 971.115 | 9,4x | 339.890 |

Con las TACC de los escenarios bajista y base (2,5 % y 5,5 %) **no existe ningún margen, ni siquiera del 100 %, que justifique el precio.** Con la del alcista (9,8 %) haría falta un margen operativo del **100,0 %** en el año 10, es decir, que no hubiera ningún coste (v3; con la beta de v2 tampoco bastaba el 100 %).

**Valor por acción ($) para combinaciones redondas de TACC y margen en el año 10:**

| TACC \ margen | 15 % | 20 % | 25 % | 30 % |
|---|---:|---:|---:|---:|
| 10 % | 46 | 66 | 86 | 105 |
| 15 % | 61 | 91 | 120 | 150 |
| 20 % | 82 | 126 | 170 | 214 |
| 25 % | 111 | 176 | 240 | 305 |

**Advertencia: intensidad de capital del software (v2, 04 §4.1.5).** El DCF inverso aplica a todo el crecimiento la intensidad de capital de un negocio industrial (1,5 $ de ventas por cada dólar invertido). Si una parte grande de los ingresos futuros fuera software (FSD) o servicios de flota con menos capital por dólar de ventas, la exigencia bajaría. Medido con ventas/capital de **3,0x** (script §9 h):

| Margen en el año 10 | TACC necesaria con 1,5x | TACC necesaria con 3,0x | Múltiplo de los ingresos en 10 años con 3,0x |
|---|---:|---:|---:|
| 20 % | 36,0 % | 32,2 % | 16,4x |
| 25 % | 31,3 % | 28,6 % | 12,4x |
| 30 % | 27,8 % | 25,8 % | 9,9x |

La exigencia baja en 2-4 puntos de TACC, pero sigue siendo multiplicar los ingresos por 10 a 16 en una década.

### Respuesta explícita

Para que 372 $ sea un valor razonable con un DCF, el mercado tiene que creer **algo equivalente a esto**: que Tesla pase de 104.000 M$ a **~1,2-2,3 billones $ de ingresos en 10 años** (una TACC del 28-36 %; del ~26-32 % con intensidad de capital de software) con **márgenes operativos del 20-30 %**. Eso es un EBIT de ~360.000-450.000 M$ en el año 10, entre **100 y 130 veces el beneficio operativo de hoy** (3.466 M$).

Puestas en contexto con los datos de las fases anteriores:
- Son ingresos de **4 a 8 veces los de Toyota** (~289.000 M$, implícitos en su EV/Ventas, §7) y superiores a los de cualquier empresa industrial actual.
- Exigen un margen de **1,3 a 2,0 veces el máximo histórico** de Tesla sin créditos (14,9 % en FY2022, sobre ingresos sin créditos).
- Exigen invertir en ese tiempo **~0,7-1,4 billones $ de capital nuevo**, con 1,5 $ de ventas por cada dólar.

Ninguna combinación de los negocios actuales llega a eso: automoción, energía y servicios suman hoy unos 104.000 M$ y crecen a un ritmo de un dígito o de un dígito bajo. **El precio solo se sostiene si una parte muy grande de esos ingresos futuros procede de negocios que hoy no reportan ingresos**: robotaxi y Cybercab, Optimus, FSD como software de alto margen y cómputo de IA. Esa opcionalidad tendría que monetizarse además con márgenes de tipo software.

Medido de otra forma, la parte del precio que el DCF del negocio reportado no explica es:

| Escenario | Valor de las acciones DCF (M$) | Diferencia con la capitalización (M$) | % de la capitalización | $ por acción |
|---|---:|---:|---:|---:|
| Bajista | 41.149 | 1.430.147 | 97,2 % | 361,8 |
| Base | 97.450 | 1.373.846 | 93,4 % | 347,6 |
| Alcista | 220.872 | 1.250.423 | 85,0 % | 316,3 |

Este resultado es coherente con el cálculo ilustrativo de Fase 1 §5, que estimaba en "menos del 10 % de la capitalización" el peso del negocio actual.

---

## 6. Lo que este DCF no puede capturar (y por qué no se esconde en el crecimiento terminal)

### 6.1 La opcionalidad no está en el modelo, a propósito

Robotaxi, Cybercab, Optimus y el cómputo de IA:
- **no tienen ingresos separados** en las cuentas;
- **no tienen métricas públicas de volumen**: Tesla no publica el número de vehículos ni de ciudades del robotaxi, ni las unidades de Optimus o de Cybercab (Fase 1 §5).

Proyectar sus flujos exigiría inventar a la vez la cuota de mercado, el precio, el coste y el calendario. No hay ningún dato de Fase 1 o Fase 2 que ancle esas cifras.

### 6.2 Por qué no se mete en g

La alternativa habitual es subir el crecimiento terminal hasta que el DCF "cuadre". Eso es incorrecto por tres motivos:
- g por encima del tipo libre de riesgo (4,97 %) implica que la empresa acaba siendo más grande que la economía;
- la tabla de la §4.1 demuestra que, incluso con g = 4 % y un WACC 3 puntos más bajo, el caso base no pasa de ~51 $;
- mezclar opcionalidad y negocio maduro en un solo número oculta lo que se está suponiendo.

Por eso aquí se separan: **valor del negocio reportado (10-56 $)** más una **opcionalidad implícita (~316-362 $ por acción)** que el mercado asigna.

### 6.3 Asimetría costes/ingresos de la opcionalidad (v2)

**El problema (04 §4.1.1, válido según 05 §3.3).** El DCF pone a cero los ingresos de las iniciativas nuevas, pero **carga al negocio actual tres costes que son, al menos en parte, de esas iniciativas**:
- **la I+D de IA**: la I+D de 3T26 fue de 2.761 M$, frente a 1.630 M$ en 3T25 (P4). Tesla atribuye el aumento a "SI and other R&D projects";
- **la SBC del plan del CEO 2025**: la SBC TTM es de 4.300 M$, 2.301 M$ más que en FY2024 (Fase 2 §4; P4 la vincula al "2025 CEO Performance Award");
- **el capex de los proyectos nuevos**: el suelo de reinversión de los años 1-2 (8,4 % de los ingresos) recoge la ola de capex de 2026, atribuida a "SI, robotics and energy" (P4).

En consecuencia, la "opcionalidad implícita" de 316-362 $ por acción **no es solo el valor de unos ingresos futuros**. Incluye también el valor que el mercado asigna a un gasto que ya se está haciendo y que este DCF resta del negocio actual.

**Cuánto pesa, medido** (caso base, script §9 c). Es una **sensibilidad, no una corrección**: la SBC y la I+D son costes reales y el caso base los mantiene. Atribuir todo el aumento a la opcionalidad es una cota alta, y la I+D incremental de un solo trimestre multiplicada por 4 también lo es.

| Variante del caso base | Margen de partida (año 0) | Suelo de capex en años 1-2 | VPA base | Diferencia |
|---|---:|:---:|---:|---:|
| **Base v3 (todo cargado al negocio actual)** | 2,23 % | sí | **24,7 $** | — |
| Sin la SBC por encima de FY2024 (+2.301 M$, 2,25 % de los ingresos sin créditos) | 4,48 % | sí | 25,5 $ | +0,8 $ |
| Sin la I+D incremental de 3T26 anualizada (+4.524 M$, 4,42 %) | 6,65 % | sí | 26,3 $ | +1,6 $ |
| Sin ninguna de las dos | 8,90 % | sí | 27,1 $ | +2,5 $ |
| Sin suelo de capex: la ola de capex de 2026 se atribuye a la opcionalidad | 2,23 % | no | 27,0 $ | +2,3 $ |
| **Las tres cosas a la vez (cota superior)** | 8,90 % | no | **29,4 $** | **+4,8 $** |

**Lectura:**
- **El efecto en el valor es pequeño**, como mucho +4,8 $. La razón es que el caso base ya converge al margen objetivo del 9,15 % en el año 5: el ajuste solo cambia la senda de los años 1-4 y el suelo de capex de los años 1-2.
- **La consecuencia relevante es cualitativa.** El margen de partida "limpio" (8,90 %) es casi el margen objetivo del caso base (9,15 %). Es decir, **el caso base equivale a suponer que, a partir del año 5, el negocio actual deja de soportar el coste de la opcionalidad** (§2.3).
- **La asimetría tiene un reverso.** El modelo tampoco carga la Terafab ("tens of billions" hasta 2028, T1), así que, en capex, el sesgo del DCF hacia el negocio actual es ligero, no pesimista (§2.1).

### 6.4 Activos no operativos fuera de la caja neta (v2)

- **SpaceX.** La participación está en "Other non-current assets", a valor razonable (P2: "The equity investment is presented within Other non-current assets on our consolidated balance sheet"; opción de valor razonable según ASC 825). **No está en la caja neta** de 35.924 M$. El 10-Q no publica su valor contable por separado. Por inferencia (compra de 2.002 M$ en 1S26 según P3, más una plusvalía no realizada de 863 M$ en 9M26 según el estado de flujos de P2), son **~2.865 M$**.
- **Activos digitales**: 962 M$ a valor razonable (P2), tampoco en la caja neta.
- **En total, ~3.827 M$, es decir, 0,97 $ por acción** (script §9 g), que el valor de las acciones del DCF **no incluye**. Es inmaterial para la conclusión.
- **xAI**: la inversión de 2.000 M$ sigue **SIN VERIFICAR** en fuente primaria. La parte del 10-Q leída en esta fase no la menciona, y la nota de partes vinculadas no se pudo leer (el texto se corta). Solo la respalda una fuente secundaria (S6, Fase 1 §4).

### 6.5 Otras limitaciones

- **Plan del CEO 2025 (423,7 M de acciones).** La v1 decía que "el modelo solo recoge una parte" de esta dilución. Con 02 §5.1 la afirmación queda **invertida**: las 423,7 M ya están en la portada sobre la que se calcula el valor por acción, aunque solo se "ganan" si se cumplen hitos ligados a la opcionalidad. En un DCF que **no** incluye la opcionalidad, contar todas esas acciones es un criterio prudente: si los hitos no se cumplen, se cancelan y el valor por acción del negocio reportado sería algo mayor. No se calcula esa cifra como corrección, por las advertencias de inferencia de §3.
- La **D&A TTM** ya es el dato real de Fase 2 (6.704 M$). Mantenerla constante en el año 1 es una aproximación (§2.1).
- La **deuda** incluye deuda sin recurso que no se puede separar (Fase 2 §8).
- El **diferencial de la deuda** es un supuesto, aunque inmaterial.
- Las **betas de regresión** no indican su ventana de cálculo.
- **No se modela el circulante por separado**: va incluido en el ratio ventas/capital.

### 6.6 Cómo debería valorarse esa opcionalidad (no se hace en esta fase)

Lo adecuado sería un enfoque de probabilidades por escenarios o de opciones reales para cada iniciativa. Para cada una habría que fijar:
- el tamaño de mercado;
- la cuota;
- el margen;
- el calendario;
- la probabilidad de éxito;
- el capital necesario.

Como orden de magnitud, que sale directamente de la tabla de la §5: con la probabilidad P de que la opcionalidad se materialice, el resultado tendría que valer ~1,3-1,4 billones $ / P en valor presente. Con P = 50 %, serían ~2,7 billones $ de VP solo en nuevos negocios. Este cálculo es una lectura de la tabla, no un supuesto del modelo. Fase 4 desarrolla este enfoque.

---

## 7. Múltiplos frente a comparables

| Empresa | Grupo | EV/Ventas | EV/EBITDA | EV/EBIT | PER | Fuente y fecha |
|---|---|---:|---:|---:|---:|---|
| **Tesla (calculado)** | — | **13,9** | **141** | **414** | **410** | EV = 1.435.372 M$ (§1). Ingresos, EBIT y beneficio neto TTM de Fase 2. **v2:** EV/EBITDA con el EBITDA aproximado de Fase 2 (EBIT + D&A TTM = 10.170 M$, sin ajustar la SBC). PER = precio / (beneficio neto TTM / media diluida de 3T) |
| Tesla (terceros)⁴ | — | 15,2 | 122,6 | 342,5 | 327,5 | [TipRanks](https://www.tipranks.com/stocks/tsla/statistics) (23-oct-2026) y [roic.ai](https://www.roic.ai/quote/TSLA/statistics) (EV/EBIT, sin fecha). [GuruFocus](https://www.gurufocus.com/news/9140534/tech-selloff-and-rising-oil-prices-pressure-markets-tesla-tsla-dips-amid-sector-weakness): PER TTM de 410,4 (23-oct-2026) |
| Toyota (TM) | Auto | 1,45 | 9,46 | 17,4 | 8,8 | [TipRanks](https://www.tipranks.com/stocks/tm/statistics) (23-oct-2026); EV/EBIT de [roic.ai](https://roic.ai/quote/TM/statistics) (30-jun-2026) |
| BYD (BYDDY) | Auto | 1,00 | 6,37 | 23,4² | 25,2 | [TipRanks](https://www.tipranks.com/stocks/byddy/statistics) (15-oct-2026); [roic.ai](https://www.roic.ai/quote/BYDDY/statistics) (30-jun-2026) |
| General Motors | Auto | 1,00 | 9,99 | 94,9³ | 17,2 | [TipRanks](https://www.tipranks.com/stocks/gm/statistics) (23-oct-2026); [roic.ai](https://www.roic.ai/quote/GM/statistics) (30-jun-2026) |
| Volkswagen (VWAGY) | Auto | 0,94 | 6,27 | 7,9² | 6,6 | [TipRanks](https://www.tipranks.com/stocks/vwagy/statistics) (24-oct-2026); [roic.ai](https://www.roic.ai/quote/VWAGY/statistics) (sin fecha) |
| Apple | Big tech | 9,36 | 26,97 | **SIN VERIFICAR** | 39,3 | [TipRanks](https://www.tipranks.com/stocks/aapl/statistics) (24-oct-2026) |
| Nvidia | Big tech | 21,04 | 31,43 | **SIN VERIFICAR** | 27,9 | [TipRanks](https://www.tipranks.com/stocks/nvda/statistics) (23-oct-2026) |
| Microsoft | Big tech | **SIN VERIFICAR** | **SIN VERIFICAR** | **SIN VERIFICAR** | **SIN VERIFICAR** | La página de TipRanks de EE. UU. no era accesible. MarketScreener daba estimaciones de FY2026, pero con fecha y capitalización no confirmadas, y no se usan |

² roic.ai muestra el mismo valor para EV/EBIT y EV/EBITDA en BYD y VW: el dato es dudoso.
³ El EV/EBIT de GM está distorsionado por cargos puntuales, a juzgar por la diferencia con su EV/EBITDA de ~10x. No se ha verificado.
⁴ **v2, dato de tercero internamente incoherente (05 §2.3, D-7).** La misma página de TipRanks da para TSLA un EV de 1,23 billones $ y una capitalización de 1,53 billones $. La diferencia (300.000 M$) es 8,4 veces la caja neta real (35.924 M$), y la capitalización tampoco coincide con la de §1 (1,47 billones $). El 15,2x de EV/Ventas de esta fila **no es fiable**: se deja solo como referencia y no se usa en ningún cálculo. La cifra que vale es la calculada (13,9x).

**Advertencias de comparabilidad:**
- Las fechas no son homogéneas: los datos de TipRanks son de oct-2026 y los de roic.ai son de 30-jun-2026.
- Los EV de los fabricantes tradicionales (GM, VW, Toyota) incluyen deuda de sus financieras de crédito, lo que infla su EV/Ventas frente a Tesla.
- El PER de los pares de TipRanks no siempre indica si es TTM.
- El EV/EBITDA de Tesla (141x) usa un EBITDA aproximado sin ajustar la SBC. No es el "Adjusted EBITDA" que publica Tesla, así que no es comparable una a una con el 122,6x de TipRanks.

**Medianas y precio implícito de TSLA** (aplicando la mediana a los ingresos, el EBIT y el BPA TTM de Tesla, más la caja neta):

| Grupo | Mediana EV/Ventas | Mediana EV/EBIT | Mediana PER | Precio por EV/Ventas | Precio por EV/EBIT | Precio por PER |
|---|---:|---:|---:|---:|---:|---:|
| Auto (4) | 1,00 | 20,4 | 13,0 | 35,3 $ | 27,0 $ | 11,8 $ |
| Big tech (**n = 2**)⁵ | 15,2 | SIN VERIFICAR | 33,6 | 407,4 $ | SIN VERIFICAR | 30,5 $ |

⁵ **v2: la mediana big tech tiene solo dos datos** (Apple y Nvidia; Microsoft SIN VERIFICAR). Con n = 2, la "mediana" es simplemente la media de Apple (9,4x) y Nvidia (21,0x). **No es representativa**, y es justo la única fila que "reproduce" el precio (407 $). No debe leerse como una valoración por comparables, sino como una ilustración de lo que hace falta suponer.

**Lectura:**
- **Como fabricante de automóviles**, los múltiplos dan **~12-35 $**, en línea con el DCF.
- **Solo el EV/Ventas de las grandes tecnológicas reproduce el precio** (~407 $), con una muestra de dos empresas. Ese múltiplo lo justifican márgenes operativos que en Apple y Nvidia son de varias veces el 3,3 % de Tesla (margen operativo TTM, 02 v3). Con el PER de esas mismas tecnológicas, Tesla valdría ~31 $.
- El mercado valora a Tesla por sus ingresos **como si ya tuviera márgenes de software**, mientras que por beneficio la valora como un fabricante de coches en su peor momento de márgenes.

---

## 8. Conclusión en rangos (sin recomendación)

| Enfoque | Rango del valor por acción |
|---|---|
| DCF del negocio reportado, del bajista al alcista | **10-56 $** (base ~25 $); con acciones totalmente diluidas, 10-56 $ (base 24,6 $) |
| Sensibilidad del caso base, WACC 8,55-13,55 % × g 2-4 % | 19-51 $ |
| Sensibilidad del caso base, margen 6-25 % × crecimiento 0,5-2x | 16-94 $ |
| Sensibilidad del caso base, ROIC terminal (WACC-15 %) y beta sectorial | 23,7-25,8 $ (coherente); hasta 29,1 $ si se baja también el WACC terminal |
| Asimetría costes/ingresos de la opcionalidad (cota superior) | hasta 29 $ (base +4,8 $) |
| Activos fuera de la caja neta (SpaceX y activos digitales) | +0,97 $ sobre cualquiera de las cifras anteriores |
| Múltiplos de fabricantes de automóviles | 12-35 $ |
| Múltiplos de big tech (EV/Ventas frente a PER; n = 2, no representativo) | 31-407 $ |
| **Precio de mercado** | **372,22 $** |

El precio actual **no es explicable** por los flujos del negocio que Tesla reporta hoy, ni siquiera con supuestos que devuelven sus márgenes al máximo histórico. Es una **apuesta sobre negocios todavía sin ingresos** (robotaxi, Optimus, IA) por un importe implícito de **~1,25-1,43 billones $**, que incluye en parte el valor de un gasto que ya se está haciendo (§6.3).

Si esa apuesta está justificada o no depende de variables que hoy no tienen métrica pública (Fase 1 §5), y queda fuera de lo que este DCF puede afirmar. Los hitos que la harían verificable son estos:
- ingresos separados por robotaxi;
- unidades de Optimus vendidas fuera de Tesla;
- margen operativo sin créditos por encima del 10 %;
- ingresos de FSD desglosados.

---

*Reproducibilidad:* `python3 scripts/fase3_dcf.py` regenera `data/dcf.xlsx` (y lo recalcula con LibreOffice si está instalado; `DCF_NO_RECALC=1` lo evita) e imprime todos los resultados de este documento. Los IDs de fuente M1-M10 están en `fuentes/fuentes.md`; las fuentes nuevas o re-leídas en v2, en `fuentes/nuevas_fase3_v2.md`, y en v3, en `fuentes/nuevas_fase3_v3.md`. Desde v3, las cifras del texto se copian de `data/cifras_03_redondeo.csv`.

---

## Registro de cambios v2

**Fecha:** 2026-10-25 · **Origen:** [05-veredicto.md](05-veredicto.md) §5, prioridad 2 (Fase 3), y §3.2-§3.3; datos nuevos de [02-financieros.md](02-financieros.md) v2 (§4 y §5.1); medición de W9 en [04-tesis.md](04-tesis.md) v2 · **Archivos tocados:** `docs/03-valoracion.md`, `scripts/fase3_dcf.py`, `data/dcf.xlsx` y el archivo nuevo `fuentes/nuevas_fase3_v2.md`. `fuentes/fuentes.md` no se toca.

**Valores por acción v1 → v2:**

| Escenario | v1 (portada) | **v2 (portada)** | v1 "dilución" (portada + 301 M) | **v2 totalmente diluidas (3.967 M)** |
|---|---:|---:|---:|---:|
| Bajista | 10,36 $ | **10,40 $** | 9,62 $ | **10,36 $** |
| Base | 24,53 $ | **24,61 $** | 22,79 $ | **24,52 $** |
| Alcista | 54,88 $ | **55,76 $** | 51,00 $ | **55,55 $** |

DCF inverso (TACC necesaria con márgenes del 20 / 25 / 30 %): **36,1 / 31,3 / 27,8 % en v1 y en v2** (variaciones de centésimas). Con ventas/capital de 3,0x (nuevo en v2): 32,3 / 28,6 / 25,8 %.

| Punto | Qué cambió |
|---|---|
| **05 §5 2(a)** ROIC terminal "dentro del rango 13-48 %" (falso: mínimo 13,4 %) | Se mantiene el 12 %, con la justificación corregida en §2.2: está **por debajo** del mínimo FY21-24 (13,4 %, FY24) y por encima del FY25 (7,6 %) y del TTM (5,5 %), con un diferencial de 2,2 puntos sobre el WACC terminal. Nueva sensibilidad en §4.3 (23,6-25,5 $). La justificación del alcista (15 %, dentro del rango) también se precisa. La misma corrección se hace en la hoja `Supuestos` |
| **05 §5 2(b)** Etiqueta "techo de la dilución del plan del CEO" | **Retirada.** §3 reescrita. §6.5 corrige la afirmación de v1 de que el modelo "solo recoge una parte" de la dilución del CEO: ya la recoge entera en la portada |
| **02 §5.1 / W2** Línea portada + 301 M (`SH_DIL_MAX`, 4.253,8 M) con doble cómputo de ~286 M | Sustituida por `SH_FD` = 3.967,3 M (fila `acc_totalmente_diluidas_aprox` de `ratios.csv`), con contraste en el script: 3.541 + 423,7 = 3.964,7 (diferencia menor de 5 M, comprobada con `assert`). Nueva columna en la tabla de §3, fila `acc_fd` en `Supuestos` y fila de VPA diluido en `Escenarios`. Se mantienen las advertencias de 02 §5.1: el reparto 286 / 15 es INFERENCIA y la cancelación de las 96 M solo tiene fuente secundaria |
| **05 §5 2(c)** Asimetría costes/ingresos (04 §4.1.1) y advertencia de intensidad de capital del software (04 §4.1.5) | Nueva **§6.3**, con 6 variantes medidas (script §9 c): de +0,8 $ a +4,8 $ (cota superior 29,4 $). Presentada como sensibilidad, no como corrección. Nueva advertencia en §5, con el DCF inverso a 3,0x de ventas/capital (script §9 h) |
| **05 §5 2(d) / W8** SpaceX "no verificado" | Nueva **§6.4**: SpaceX fuera de la caja neta (texto de P2 re-leído por Fase 3 el 25-oct-2026), ~2.865 M$ por inferencia + 962 M$ de activos digitales = **0,97 $/acción** (script §9 g). xAI sigue SIN VERIFICAR en primaria |
| **05 §5 2(e) / W3** Guía de capex ">20.000-25.000 M$" desfasada | §2.1: guía actualizada a **~20.000 M$** (CFO, T1). Capex bruto implícito del año 1 = 9.180 + 6.704 = **15.884 M$**, 4.116 M$ por debajo de la guía y sin Terafab (script §9 d). Se aclara que el año 1 del modelo no es el año natural. W3 no cambia el modelo (05: crítica inválida) |
| **05 §5 2(f) / W6** Margen base del 8,93 % | Nueva **§2.3** con el mecanismo medido (script §9 e): con margen bruto constante, el gasto operativo tendría que bajar un 21,6 % en términos absolutos; con opex/ingresos constante, el margen bruto tendría que llegar al 25,3 % (máximo histórico, 23,9 %). El margen de partida sin SBC extra ni I+D incremental (8,90 %) es casi el objetivo. Columna rotulada «Base (media FY21-24)». El valor cambia al 9,15 % por la corrección (h), no por esta |
| **05 §5 2(f) / W7** Energía +12 % frente a 9M26 −5,7 % | **Cambiado:** base 12 % → **8 %** y bajista 5 % → **0 %** (alcista 20 % sin cambios). Justificación en §2.3 con volumen frente a ingreso por GWh (+7,5 % y −10,7 % TTM frente a FY25; script §9 f). El bajista se baja para mantener el orden entre escenarios |
| **05 §5 2(g)** EV de TipRanks para TSLA y mediana big tech con n = 2 | Notas ⁴ y ⁵ en §7, aviso en la conclusión (§8) y en la hoja `Multiplos`. La salida del script imprime los dos avisos |
| **05 §5 2(h)** Anclas de margen con denominador distinto del de aplicación | Las anclas y el margen TTM se calculan ahora como (EBIT − créditos) / (ingresos − créditos) en el script (función `m_ex`). Además se elimina el redondeo a 3 decimales de v1 (que hacía que el modelo usara un 8,9 % mientras el texto decía 8,93 %). Anclas v1 → v2: 3,5 % → 3,54 %; 8,9 % → 9,15 %; 14,6 % → 14,91 %; TTM 2,21 % → 2,23 % |
| **02 v2 / W4** D&A TTM ≈ 3T26 × 4 (7.408 M$) | Sustituida por **6.704 M$** (fila `dya_amortizacion_deterioro` de `ratios.csv`). El capex neto TTM pasa del 7,72 % al 8,40 % de los ingresos, y los FCFF de los años 1-2 bajan. El nombre `DA_TTM_APROX` se mantiene como alias (= 6.704) porque `fase4_opcionalidad.py` lo importa. Retirada la limitación "D&A aproximada" de §6. Nuevo EV/EBITDA de TSLA (141x) en §7 |
| **W9** (04 v2: +1,2 $ y +4,6 $) | §4.3: las dos cifras, medidas de nuevo con el modelo v2 (+1,24 $ y +4,60 $; script §9 b). **El modelo usa la beta mezclada 50/50.** La variante coherente de beta sectorial es +1,2 $ (solo años 1-5); +4,6 $ es la cota superior |
| 05 §1: `dcf.xlsx` sin valores cacheados | El script recalcula el libro con LibreOffice al guardarlo (si está instalado). Comprobado: 0 errores de fórmula, 485 fórmulas, y VPA, EV, WACC y EBITDA idénticos a Python |
| Cifras derivadas | Actualizadas desde la salida del script: tablas 3, 4.1, 4.2 y 5, brecha (85,0-97,2 %; 316,5-361,8 $/acción), opcionalidad implícita (~316-362 $), rangos de §8 ("~50 $" en lugar de "~51 $"; 16-93 $ en lugar de 16-99 $), margen del DCF inverso frente al máximo histórico (1,3-2,0x) |

**No aplicado, por decisión de 05 (críticas inválidas):**
- **W1** (PER de 410x frente a 457x): 410x es la convención estándar. Sin cambios.
- **W3 como cambio de valoración**: el modelo no usa la cifra de la guía. Solo se actualiza el texto (fila 2(e)).
- **W5** (ingresos de Toyota): el argumento de 04 v1 es matemáticamente erróneo. Sin cambios.
- **VPA "corregidos" de 04 v1** (11,6 / 27,5 / 61,5 $ sobre la media diluida): no se usan, porque excluyen acciones emitidas legalmente (05 §3.3; 04 v2 los retiró).

**Efecto en otras fases (no modificadas aquí):** `fase4_opcionalidad.py` §13 importa este modelo. Con v2, sus cifras se mueven en décimas: capex del año 1, 15.883 → 15.884 M$; sensibilidad de §4.1.1, 25,44 / 26,24 $ (sigue redondeando a 25,4 / 26,2); ajuste máximo, 28,5-31,8 $ (04 dice 28,4-31,8). Las expectativas de `fase5_consistencia.py` siguen siendo los valores de v1 y darán diferencias en los VPA (por ejemplo, alcista 54,9 → 55,8).

---

## Registro de cambios v3

**Fecha:** 2026-10-25 · **Origen:** [05-veredicto-v2.md](05-veredicto-v2.md) §8, prioridad 2 (Fase 3), con §2.1 (M1, M2) y §4.2 (FAIL-v2-1); «Registro de cambios v3» de [02-financieros.md](02-financieros.md) · **Archivos tocados:** `docs/03-valoracion.md`, `scripts/fase3_dcf.py`, `data/dcf.xlsx`, el archivo nuevo `data/cifras_03_redondeo.csv` y el archivo nuevo `fuentes/nuevas_fase3_v3.md`. `fuentes/fuentes.md` no se toca.

| Punto | Qué cambió |
|---|---|
| **(a) M1** W9 "25,9 $" (25,848) | §4.3 (tabla W9): **25,8 $**. §8: "23,6-25,9 $" pasa a "**23,7-25,8 $**". El 25,8 no cambia con la beta nueva (la variante W9 usa solo la beta sectorial, 25,848 $). El extremo bajo pasa de 23,6 a **23,7 $** por el cambio de beta del punto (c): el ROIC terminal = WACC da ahora 23,680 $ (v2: 23,639). La diferencia "+1,2 $" se mantiene (+1,19) |
| **(b) M2** §6.3 "Sin la SBC por encima de FY2024" 25,5 $ (25,446) | Con el modelo v2, la cifra correcta era 25,4 $ y el veredicto tenía razón. **Con el modelo v3 (punto c), el valor completo es 25,490 $, que da 25,5 $**: la cifra del documento vuelve a coincidir con el script, ahora sin doble redondeo (`asim_1_vpa` en `cifras_03_redondeo.csv`). La diferencia sigue en +0,8 $ (+0,84). **Fase 4 debe copiar 25,5 $, no 25,4** (ver la lista de cifras de abajo) |
| **(c) FAIL-v2-1** Beta de MarketChameleon 1,87 no reproducible | **Re-consultadas las dos fuentes el 25-oct-2026** (`fuentes/nuevas_fase3_v3.md`). MarketChameleon da 1,84 ("Data as of October 23, 2026"). **TipRanks también da hoy 1,84** (fecha de modificación de la página: 24-oct-2026; no aparece ningún 1,85), así que la otra mitad de la media tampoco es ya reproducible. **Decisión:** se citan los valores actuales de ambas, 1,84 y 1,84, y no se retira la beta de regresión, para no cambiar el criterio de mezcla 50/50 declarado en §1.1 y discutido en W9. Es el único cambio de modelo de esta ronda, y todo se recalcula desde el script: beta de regresión 1,86 → **1,84**; beta inicial 1,59 → **1,58**; Ke inicial 11,64 % → **11,60 %**; WACC inicial 11,60 % → **11,55 %** (el WACC terminal no cambia: 9,79 %); VPA base 24,61 → **24,65 $** (+0,04 $; a un decimal, 24,6 → **24,7 $**). El veredicto estimaba +0,03 $ cambiando solo MarketChameleon; con las dos fuentes en 1,84, el efecto es de +0,04 $. Actualizadas §0, §1, §1.1, §2.2, §3, §4.1 (las filas de la tabla pasan a 8,55-13,55 %, porque la rejilla es el WACC base ± 1-3 puntos), §4.2, §4.3, §5, §6.2, §6.3 y §8. **Una frase de §5 cambia de sentido:** con la TACC alcista (9,8 %), un margen del 100,0 % basta ahora para justificar el precio (372,22 $, justo en el límite); en v2 no bastaba. La conclusión no cambia: haría falta un negocio sin costes |
| **(d)** Margen operativo TTM 3,4 % → 3,3 % (02 v3) | §7, lectura de múltiplos: "varias veces el 3,3 % de Tesla (margen operativo TTM, 02 v3)". 03 no cita en ningún otro sitio el margen operativo TTM total; el margen sin créditos (2,23 %) no cambia |
| **(e)** Evitar el doble redondeo | Nueva §10 del script: escribe `data/cifras_03_redondeo.csv` (220 cifras con clave, sección de 03, valor completo, decimales, unidad y texto). El texto se redondea **una sola vez**, mitad hacia arriba con `Decimal`, desde el valor completo, con el número de decimales y el formato del documento (miles con punto y decimales con coma). El script también imprime las cifras y avisa de las que saldrían distintas si se volviera a redondear una salida a d+1 decimales: hoy son 10, entre ellas W9 (25,85 → 25,8, no 25,9), el WACC inicial (11,555 → 11,55, no 11,56) y la cota superior de §6.3 (29,45 → 29,4). Todas las cifras de 03 que cambian en esta ronda se han copiado de ese CSV |

**Cifras de 03 que cambian en v3 (antiguas → nuevas), para que Fase 4 las sincronice:**

| Dónde en 03 | v2 | **v3** |
|---|---:|---:|
| §1 / §1.1 beta de regresión (fuentes) | 1,85 y 1,87 → 1,86 | **1,84 y 1,84 → 1,84** |
| §1.1 beta inicial | 1,59 | **1,58** |
| §1.1 Ke inicial | 11,64 % | **11,60 %** |
| §1.1 WACC inicial (y fila base de 4.1, W9 "Modelo") | 11,60 % | **11,55 %** |
| §1.1 WACC solo con beta de regresión | ~12,7 % | **~12,6 %** |
| §3 VPA base (portada) / totalmente diluido | 24,6 / 24,5 $ | **24,7 / 24,6 $** (24,654 / 24,563) |
| §3 VPA alcista (portada) / totalmente diluido | 55,8 / 55,6 $ | **55,9 / 55,7 $** (55,878 / 55,673) |
| §3 VPA bajista | 10,4 / 10,4 $ | sin cambios |
| §3 bajista: VP FCFF / VP TV / % TV / EV / acciones | −8.451 / 13.641 / 263 % / 5.190 / 41.114 | **−8.452 / 13.676 / 262 % / 5.225 / 41.149** |
| §3 base: VP FCFF / VP TV / EV / acciones | 10.399 / 50.954 / 61.353 / 97.277 | **10.438 / 51.088 / 61.526 / 97.450** |
| §3 alcista: VP FCFF / VP TV / EV / acciones | 47.438 / 137.030 / 184.468 / 220.392 | **47.558 / 137.390 / 184.948 / 220.872** |
| §0 VPA totalmente diluidos | 10,4 / 24,5 / 55,6 $ | **10,4 / 24,6 / 55,7 $** |
| §0 punto 4 y §6.2: máximo de la tabla 4.1 | ~50 $ | **~51 $** (50,69) |
| §4.1 tabla | filas 8,60-13,60 % | **filas 8,55-13,55 %**; esquina 50,4 → **50,7**; celda base 24,6 → **24,7** (resto en la tabla) |
| §4.2 tabla | 16,3 … 93,4 | 6 %: 16,3 / 16,4 / 16,3 / 16,0; 9 %: 22,8 / 24,3 / 26,1 / 28,2; 12 %: 29,2 / 32,2 / 35,8 / 40,5; 15 %: 35,6 / 40,1 / 45,6 / 52,7; 20 %: 46,4 / 53,2 / 61,9 / 73,2; 25 %: 57,1 / 66,4 / 78,3 / **93,6** |
| §4.3 ROIC terminal = WACC / 10 % / 12 % / 13,4 % / 15 % | 23,6 / 23,8 / 24,6 / 25,1 / 25,5 $ | **23,7** / 23,8 / **24,7** / 25,1 / 25,5 $ |
| §4.3 W9 beta sectorial años 1-5 | 25,9 $ (+1,2) | **25,8 $ (+1,2)** |
| §4.3 W9 con WACC terminal desplazado | 8,65 % · 29,2 $ · +4,6 $ | **8,70 % · 29,1 $ · +4,4 $** |
| §5 TACC necesaria con 10 / 15 / 20 / 25 / 30 / 35 % | 61,8 / 43,7 / 36,1 / 31,3 / 27,8 / 25,1 % | **61,7** / 43,7 / **36,0** / 31,3 / 27,8 / 25,1 % |
| §5 ingresos del año 10 (10 / 15 / 20 / 25 / 30 / 35 %) | 12.711.646 / 3.889.508 / 2.255.182 / 1.576.411 / 1.206.301 / 973.900 | **12.671.686 / 3.878.013 / 2.248.629 / 1.571.868 / 1.202.840 / 971.115** |
| §5 múltiplo sobre el TTM (10 / 15 / 20 %) | 122,7x / 37,6x / 21,8x | **122,3x / 37,4x / 21,7x** (25 / 30 / 35 %: 15,2x / 11,6x / 9,4x sin cambios) |
| §5 EBIT del año 10 (10 / 15 / 20 / 25 / 30 / 35 %) | 1.271.165 / 583.426 / 451.036 / 394.103 / 361.890 / 340.865 | **1.267.169 / 581.702 / 449.726 / 392.967 / 360.852 / 339.890** |
| §5 TACC con ventas/capital de 3,0x (20 %) | 32,3 % | **32,2 %** (25 % y 30 %: 28,6 / 25,8 %, sin cambios) |
| §5 margen necesario con la TACC alcista | no alcanzable | **100,0 %** |
| §5 combinaciones TACC × margen | (10,25) 85; (20,15) 81; (20,20) 125; (20,25) 169; (20,30) 213; (25,15) 110; (25,20) 175; (25,30) 304 | **86; 82; 126; 170; 214; 111; 176; 305** (resto igual) |
| §5 brecha bajista / base / alcista (M$) | 1.430.182 / 1.374.019 / 1.250.904 | **1.430.147 / 1.373.846 / 1.250.423** |
| §5 brecha alcista por acción | 316,5 $ | **316,3 $** (el rango "~316-362 $" y el 85,0-97,2 % no cambian) |
| §6.3 base / sin SBC extra / sin suelo de capex | 24,6 / 25,5 (debía ser 25,4) / 26,9 $ | **24,7 / 25,5 / 27,0 $** (diferencias +0,8 / +2,3 sin cambios; resto de filas sin cambios: 26,3 / 27,1 / 29,4 $ y +1,6 / +2,5 / +4,8 $) |
| §7 margen operativo TTM | 3,4 % | **3,3 %** |
| §8 sensibilidad WACC × g | WACC 8,6-13,6 % · 19-50 $ | **WACC 8,55-13,55 % · 19-51 $** |
| §8 sensibilidad margen × crecimiento | 16-93 $ | **16-94 $** |
| §8 ROIC terminal y beta sectorial | 23,6-25,9 $; hasta 29,2 $ | **23,7-25,8 $; hasta 29,1 $** |
| §8 DCF con acciones totalmente diluidas, base | 24,5 $ | **24,6 $** |

No cambian: los rangos "~10-~56 $" y "~25 $" del caso base, el 85-97 % de brecha, los ~1,25-1,43 billones $, las TACC "~28-36 %" y "~26-32 %", los múltiplos de TSLA (13,9x / 141x / 414x / 410x), los +0,97 $ de activos no operativos, el capex del año 1 (15.884 M$) y la §2.3.

**Para Fase 4 (no se modifica aquí):** el veredicto le pide "(25,4 / 26,3 $)" en §4.1.1. Con 03 v3 debe ser **(25,5 / 26,3 $)**, y "24,6 → 25,8 $" en §4.1.3 pasa a **"24,7 → 25,8 $"**. `fase4_opcionalidad.py` importa este script, así que sus salidas también se moverán ligeramente.

**Para el Reality Checker:** las expectativas de `fase5_consistencia.py` (WACC 11,60 %, VPA 24,6…) corresponden al modelo v2.

**Limitación:** en el equipo de esta ronda no hay LibreOffice, así que `data/dcf.xlsx` se ha regenerado **sin valores cacheados**. Las fórmulas son las mismas que en v2 y se recalculan al abrir el libro. Para recuperar la caché (arreglo de v2, 05 §1) hay que volver a ejecutar `fase3_dcf.py` en un equipo con LibreOffice.
