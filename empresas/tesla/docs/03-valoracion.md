# 03 — Valoración de Tesla (TSLA): DCF por escenarios, sensibilidad, DCF inverso y múltiplos

**Fecha del análisis:** 2026-10-24 · **Analista:** Fase 3 (rol *Financial Analyst*) · **Precio de referencia:** 372,22 $ (cierre del 23-oct-2026)
**Alcance:** esto es una valoración, no una recomendación de compra o venta. Los resultados se dan como rangos y dependen de los supuestos declarados abajo.

**Archivos de esta fase:**

| Archivo | Contenido |
|---|---|
| [`scripts/fase3_dcf.py`](../scripts/fase3_dcf.py) | Todos los cálculos. Lee `data/ratios.csv` de Fase 2 |
| [`data/dcf.xlsx`](../data/dcf.xlsx) | Hojas `Supuestos`, `Escenarios`, `Sensibilidad`, `DCF_inverso` y `Multiplos`. En `Supuestos` y `Escenarios` los inputs van en azul y el resto son fórmulas de Excel vivas. Recalculado con LibreOffice, el resultado coincide con Python y no hay errores |

No hay ningún cálculo hecho a mano en este documento: todas las cifras salen de la salida del script.

---

## 0. Resumen

1. **El DCF del negocio que Tesla reporta hoy no se acerca al precio.** Con supuestos que van desde un estancamiento hasta volver al mejor margen de su historia, el valor por acción queda entre **~10 $ y ~55 $**, con **~25 $ en el caso base**. El precio es de 372 $.
2. **Entre el 85 % y el 97 % de la capitalización (1,47 billones $) no se explica** por los flujos de automoción, energía y servicios proyectados con los datos de Fase 1 y Fase 2. Esa diferencia es lo que el mercado paga por la opcionalidad: robotaxi, Optimus, FSD como software y cómputo de IA.
3. **Para justificar el precio con un DCF convencional** hace falta que los ingresos crezcan entre un **~28 % y un ~36 % anual durante 10 años**, es decir, que se multipliquen por 12 a 22 veces, con márgenes operativos del 20-30 %. Nada parecido aparece en la historia reportada.
4. **Ni tocando el WACC ni el crecimiento terminal se cierra la brecha.** Con un WACC 3 puntos más bajo y un crecimiento terminal del 4 %, el caso base sube solo hasta ~51 $.
5. **Por múltiplos, Tesla cotiza a 13,9x EV/Ventas.** Esto se parece más a Nvidia (21x) o Apple (9,4x) que a los fabricantes de coches (~1x). Su EV/EBIT (414x) y su PER (410x) no tienen comparación con ningún par.

---

## 1. Inputs de mercado (con fuente y fecha)

| Input | Valor | Fuente y fecha |
|---|---|---|
| Precio TSLA | **372,22 $** | Cierre del 23-oct-2026 (−0,63 %), según [Benzinga](https://www.benzinga.com/quote/TSLA) (campo "Close") y [MarketChameleon](https://marketchameleon.com/Overview/TSLA/Summary/). Coincide con [GuruFocus, 23-oct-2026](https://www.gurufocus.com/news/9140534/tech-selloff-and-rising-oil-prices-pressure-markets-tesla-tsla-dips-amid-sector-weakness). El cierre previo, 374,58 $ el 22-oct, figura en [heygotrade](https://www.heygotrade.com/en/us-stock/tsla/) |
| Acciones en circulación | **3.952,76 M** | Portada del [10-Q 3T 2026 (P2)](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066775/tsla-20260930.htm): 3.952.757.946 acciones a 15-oct-2026 |
| Media ponderada diluida y básica de 3T 2026 | 3.541 M y 3.240 M | P2, cuenta de resultados |
| Capitalización | **1.471.296 M$** | Calculada como precio × acciones de portada. Contraste: 1,47 billones $ según GuruFocus y Benzinga (23-oct-2026) |
| Caja neta | **35.924 M$** | Fase 2, saldo a 30-sep-2026 (45.447 de caja − 9.523 de deuda) |
| Valor de la empresa (EV) de mercado | 1.435.372 M$ | Calculado como capitalización − caja neta |
| Tipo libre de riesgo (bono a 10 años de EE. UU.) | **4,97 %** | 4,967 % el 23-oct-2026, ~15:53 ET; cierre del 22-oct en 4,954 %. Fuente: [Mortgage News Daily](https://www.mortgagenewsdaily.com/treasury/10yr) |
| Prima de riesgo del mercado (ERP) | **4,20 %** | ERP implícito del S&P 500 a 1-oct-2026, "trailing 12 month, with adjusted payout", según la [página de Damodaran](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm). La variante con rendimiento en efectivo de los últimos doce meses da 3,70 % |
| Beta de regresión | 1,85 y 1,87 → **1,86** | [TipRanks](https://www.tipranks.com/stocks/tsla/statistics) (actualizado 23-oct-2026) y [MarketChameleon](https://marketchameleon.com/Overview/TSLA/Summary/) (23-oct-2026). Ninguna de las dos fuentes indica la ventana de cálculo |
| Beta del sector, desapalancada | **1,31** | [Damodaran, betas por sector de EE. UU.](https://pages.stern.nyu.edu/~adamodar/New%5FHome%5FPage/datafile/Betas.html) (ene-2026): Auto & Truck, 33 empresas, corregida por caja |
| Diferencial de la deuda sobre el tipo libre de riesgo | 1,0 % | **SIN VERIFICAR.** Es un supuesto: no se consultó el rating vigente. Su efecto es inmaterial, porque la deuda pesa un 0,6 % del capital |
| Tipo impositivo | 21 % | Tipo federal de EE. UU., con el mismo criterio que Fase 2 (§6) |

### 1.1 WACC

| Paso | Valor | Cómo se obtiene |
|---|---|---|
| Deuda / capitalización | 0,65 % | 9.523 / 1.471.296 |
| Beta *bottom-up* reapalancada | 1,32 | 1,31 × (1 + 0,79 × D/E) |
| **Beta inicial** | **1,59** | Media al 50 % de la regresión (1,86) y la *bottom-up* (1,32). La regresión refleja la volatilidad real de la acción; la del sector, el negocio que genera los flujos que se descuentan |
| Coste del capital propio inicial | 11,64 % | 4,97 % + 1,59 × 4,20 % |
| Coste de la deuda después de impuestos | 4,72 % | (4,97 % + 1 %) × 0,79 |
| **WACC inicial (años 1-5)** | **11,60 %** | Deuda al 0,64 % del capital |
| Beta terminal | 1,16 | Punto medio entre el mercado (1,0) y el sector del automóvil (1,31) |
| **WACC terminal (años 6-10 en convergencia lineal; perpetuidad)** | **9,79 %** | — |

Usar solo la beta de regresión (1,86) subiría el WACC inicial a ~12,7 %. Usar solo la del sector lo bajaría a ~10,5 %. En la §4 se ve que ninguno de los dos extremos cambia la conclusión.

---

## 2. Estructura del modelo y supuestos

### 2.1 Mecánica

- **Año 0** = últimos doce meses (TTM) a 3T 2026, de Fase 2: ingresos de 103.570 M$, beneficio operativo de 3.466 M$ y margen sin créditos del 2,21 %. La proyección cubre 10 años y descuenta a final de cada año, lo que es conservador frente a descontar a mitad de año.
- **Ingresos por segmento**: automoción sin créditos (73.822), energía (12.265), servicios y otros (16.302) y créditos regulatorios (1.181). Cada segmento sigue su propia senda de crecimiento: constante en los años 1-5 y con un descenso lineal hasta el crecimiento terminal en el año 10.
- **Créditos regulatorios**: 40 %, 10 % y 0 % del importe TTM en los años 1, 2 y 3, y nada después. La ley OBBBA restringe estos programas (Fase 1 §4) y en 3T 2026 ya cayeron un −73 %. Se les asigna un margen de ~100 %, igual que en Fase 2.
- **Margen operativo sin créditos**: pasa linealmente del 2,21 % TTM al margen objetivo del escenario en el año 5 y se mantiene después.
- **FCFF** = EBIT × (1 − 21 %) − reinversión neta.
  - **La compensación en acciones (SBC) se trata como un coste real.** El EBIT GAAP ya la descuenta (4.300 M$ TTM, el 4,2 % de los ingresos) y **no se suma de vuelta**. Equivale a suponer que Tesla pagara esa retribución en efectivo. Además, el valor por acción se calcula sobre las 3.953 M de acciones de portada, que es una cifra mayor que la media diluida de 3T (3.541 M). La tabla de la §3 añade una línea con la dilución adicional que supondría el plan del CEO.
  - **Reinversión neta** (capex − amortización + circulante):
    - En los años 1-2 es el máximo entre (a) el **7,7 % de los ingresos**, que es el capex neto TTM: capex de 15.407 M$ menos una amortización aproximada de 7.408 M$ (D&A de 3T 2026, 1.852 M$, multiplicada por 4). Esto recoge la ola de capex de 2026 (">20.000-25.000 M$", Fase 1 §2), y (b) el aumento de ingresos dividido por el ratio ventas/capital.
    - Desde el año 3 es solo el aumento de ingresos dividido por el ratio ventas/capital.
    - Referencias de Fase 2 para ese ratio: **1,94x** sobre el capital invertido neto de caja (A) y **1,05x** sobre el capital bruto (B).
- **Valor terminal** = NOPAT₁₁ × (1 − g / ROIC terminal) / (WACC terminal − g). Así la reinversión es coherente con el crecimiento: no se puede crecer en perpetuidad sin reinvertir.
- **Valor de las acciones** = EV + 35.924 M$ de caja neta.

### 2.2 Supuestos por escenario y su justificación

| Supuesto | Bajista | Base | Alcista | Justificación (datos de Fase 1 y Fase 2) |
|---|---:|---:|---:|---|
| Crecimiento de automoción sin créditos, años 1-5 | 1 % | 4 % | 8 % | TACC FY21-25: 10,2 %. FY24: −6,5 %. FY25: −9,8 %. 9M26: +10,6 %, pero 3T26 −3 % y un "lower ASP" (P4). BYD vende más VE (Fase 1 §3). El 8 % alcista supone una recuperación de volumen sostenida sin volver a 2021-22 |
| Crecimiento de energía, años 1-5 | 5 % | 12 % | 20 % | TACC FY21-25: 46 %. Pero 9M26 −5,7 %, 3T26 −16 % y compresión de margen anunciada por "low-cost competition" (S4). Los integradores chinos tienen el 76 % del mercado (S9) |
| Crecimiento de servicios y otros, años 1-5 | 10 % | 15 % | 22 % | TACC FY21-25: 34,7 %; 9M26: +41 %. Es la línea que más crece, pero sin desglose (SIN VERIFICAR en Fase 2) y con un margen bruto del 15,9 % |
| **TACC resultante de los ingresos a 10 años** | **2,9 %** | **5,9 %** | **9,8 %** | Salida del modelo. Las TACC históricas FY21-25 fueron del 15,2 % en total, pero del −1,0 % anual entre FY23 y FY25 |
| **Margen operativo objetivo sin créditos (desde el año 5)** | **3,45 %** | **8,93 %** | **14,58 %** | Bajista = media FY24-25. Base = media FY21-24. Alcista = máximo histórico (FY22). Todos sin créditos (Fase 2 §3). El margen TTM es del 2,21 % |
| Ventas / capital incremental | 1,2x | 1,5x | 2,0x | Entre el 1,05x (B) y el 1,94x (A) de Fase 2. El alcista supone más eficiencia que la actual |
| Crecimiento terminal (g) | 2,5 % | 3,0 % | 3,5 % | Siempre por debajo del tipo libre de riesgo nominal (4,97 %). **No se usa g para meter la opcionalidad** (ver §6) |
| ROIC terminal | = WACC (9,8 %) | 12 % | 15 % | Bajista: el crecimiento no crea valor. Base y alcista: dentro del rango del ROIC A de FY21-24 (13-48 %, Fase 2 §6). El ROIC TTM es del 5,5 % (A) y el 2,9 % (B) |
| Robotaxi, Optimus, cómputo de IA | 0 | 0 | 0 | No tienen ingresos separados ni métricas públicas (Fase 1 §5). Se tratan aparte, en la §6 |

**Nota sobre el escenario alcista.** No es un escenario optimista sobre la tesis completa de Tesla. Es el escenario optimista **del negocio que se reporta hoy**: los tres segmentos crecen con fuerza y el margen vuelve a su máximo. Lo que el mercado descuenta más allá de eso se trata explícitamente en la §5 y la §6.

---

## 3. Resultados por escenario

| Escenario | Ingresos año 10 (M$) | EBIT año 10 (M$) | VP FCFF años 1-10 | VP del valor terminal | % del EV en el valor terminal | EV (M$) | Valor de las acciones (M$) | **Valor por acción** | vs. precio (372,22 $) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Bajista | 138.109 | 4.834 | −9.002 | 14.017 | 279 %¹ | 5.016 | 40.940 | **10,4 $** | −97 % |
| **Base** | 183.483 | 16.330 | 9.577 | 51.463 | 84 % | 61.040 | 96.964 | **24,5 $** | −93 % |
| Alcista | 263.026 | 38.402 | 46.813 | 134.194 | 74 % | 181.007 | 216.931 | **54,9 $** | −85 % |

¹ En el bajista los FCFF de los años 1-10 suman un valor presente negativo, por la ola de capex y un margen que apenas se recupera. Por eso el valor terminal supera el 100 % del EV. Casi todo el valor de este escenario es la caja neta: 35.924 M$, unos 9,1 $ por acción.

**Rango de valor por acción del negocio reportado: ~10 $ a ~55 $; caso base ~25 $.**

**Dilución adicional.** Si se suman las ~301 M de acciones de diferencia entre la media diluida y la básica de 3T 2026, como techo ilustrativo de la dilución del plan del CEO, los valores bajan a 9,6 $, 22,8 $ y 51,0 $.

**FCFF del caso base por año (M$):** −5.039, −4.428, 712, 1.943, 3.442, 4.326, 5.385, 6.600, 7.935 y 9.338. Los dos primeros años son negativos y reflejan lo que ya se ve en el TTM: el FCF menos la SBC es de −997 M$ (Fase 2 §4).

---

## 4. Sensibilidad (caso base)

### 4.1 WACC inicial × crecimiento terminal (valor por acción, $)

El WACC terminal se desplaza lo mismo que el inicial.

| WACC inicial \ g | 2,0 % | 2,5 % | 3,0 % | 3,5 % | 4,0 % |
|---|---:|---:|---:|---:|---:|
| 8,60 % | 38,7 | 40,6 | 43,1 | 46,2 | 50,5 |
| 9,60 % | 32,0 | 33,0 | 34,2 | 35,7 | 37,6 |
| 10,60 % | 27,3 | 27,9 | 28,5 | 29,2 | 30,1 |
| **11,60 %** | 23,9 | 24,2 | **24,5** | 24,9 | 25,3 |
| 12,60 % | 21,3 | 21,5 | 21,6 | 21,8 | 22,0 |
| 13,60 % | 19,3 | 19,4 | 19,4 | 19,5 | 19,5 |

### 4.2 Margen operativo objetivo × multiplicador del crecimiento de los años 1-5 (valor por acción, $)

| Margen \ crecimiento × | 0,5x | 1,0x (base) | 1,5x | 2,0x |
|---|---:|---:|---:|---:|
| 6 % | 16,6 | 16,7 | 16,5 | 16,1 |
| 9 % | 23,1 | 24,8 | 26,8 | 29,2 |
| 12 % | 29,7 | 32,9 | 37,1 | 42,3 |
| 15 % | 36,2 | 41,1 | 47,4 | 55,4 |
| 20 % | 47,1 | 54,6 | 64,5 | 77,2 |
| 25 % | 57,9 | 68,2 | 81,6 | 99,0 |

**Lectura:**
- **El margen es la variable dominante.** Con márgenes bajos, crecer más **destruye** valor (fila del 6 %), porque cada dólar de ingresos nuevos exige ~0,67 $ de capital y rinde menos que el WACC.
- **El WACC y g mueven el resultado en decenas de dólares, no en cientos.** Ninguna combinación razonable de las dos tablas pasa de ~100 $ por acción.
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
| 10 % | 61,8 % | 12.715.761 | 122,8x | 1.271.576 |
| 15 % | 43,7 % | 3.890.191 | 37,6x | 583.529 |
| **20 %** | **36,1 %** | **2.255.489** | **21,8x** | 451.098 |
| **25 %** | **31,3 %** | **1.576.594** | **15,2x** | 394.149 |
| **30 %** | **27,8 %** | **1.206.426** | **11,6x** | 361.928 |
| 35 % | 25,1 % | 973.992 | 9,4x | 340.897 |

Con las TACC de los tres escenarios (2,9 %, 5,9 % y 9,8 %) **no existe ningún margen, ni siquiera del 100 %, que justifique el precio.**

**Valor por acción ($) para combinaciones redondas de TACC y margen en el año 10:**

| TACC \ margen | 15 % | 20 % | 25 % | 30 % |
|---|---:|---:|---:|---:|
| 10 % | 47 | 66 | 86 | 105 |
| 15 % | 61 | 91 | 120 | 150 |
| 20 % | 81 | 125 | 169 | 213 |
| 25 % | 110 | 175 | 240 | 304 |

### Respuesta explícita

Para que 372 $ sea un valor razonable con un DCF, el mercado tiene que creer **algo equivalente a esto**: que Tesla pase de 104.000 M$ a **~1,2-2,3 billones $ de ingresos en 10 años** (una TACC del 28-36 %) con **márgenes operativos del 20-30 %**. Eso es un EBIT de ~360.000-450.000 M$ en el año 10, entre **100 y 130 veces el beneficio operativo de hoy** (3.466 M$).

Puestas en contexto con los datos de las fases anteriores:
- Son ingresos de **4 a 8 veces los de Toyota** (~289.000 M$, implícitos en su EV/Ventas, §7) y superiores a los de cualquier empresa industrial actual.
- Exigen un margen de **1,4 a 2,1 veces el máximo histórico** de Tesla sin créditos (14,6 % en FY2022).
- Exigen invertir en ese tiempo **~0,7-1,4 billones $ de capital nuevo**, con 1,5 $ de ventas por cada dólar.

Ninguna combinación de los negocios actuales llega a eso: automoción, energía y servicios suman hoy unos 104.000 M$ y crecen a un ritmo de un dígito o de un dígito bajo. **El precio solo se sostiene si una parte muy grande de esos ingresos futuros procede de negocios que hoy no reportan ingresos**: robotaxi y Cybercab, Optimus, FSD como software de alto margen y cómputo de IA. Esa opcionalidad tendría que monetizarse además con márgenes de tipo software.

Medido de otra forma, la parte del precio que el DCF del negocio reportado no explica es:

| Escenario | Valor de las acciones DCF (M$) | Diferencia con la capitalización (M$) | % de la capitalización | $ por acción |
|---|---:|---:|---:|---:|
| Bajista | 40.940 | 1.430.356 | 97,2 % | 361,9 |
| Base | 96.964 | 1.374.332 | 93,4 % | 347,7 |
| Alcista | 216.931 | 1.254.364 | 85,3 % | 317,3 |

Este resultado es coherente con el cálculo ilustrativo de Fase 1 §5, que estimaba en "menos del 10 % de la capitalización" el peso del negocio actual.

---

## 6. Lo que este DCF no puede capturar (y por qué no se esconde en el crecimiento terminal)

**1. La opcionalidad no está en el modelo, a propósito.** Robotaxi, Cybercab, Optimus y el cómputo de IA:
- **no tienen ingresos separados** en las cuentas;
- **no tienen métricas públicas de volumen**: Tesla no publica el número de vehículos ni de ciudades del robotaxi, ni las unidades de Optimus o de Cybercab (Fase 1 §5).

Proyectar sus flujos exigiría inventar a la vez la cuota de mercado, el precio, el coste y el calendario. No hay ningún dato de Fase 1 o Fase 2 que ancle esas cifras.

**2. Por qué no se mete en g.** La alternativa habitual es subir el crecimiento terminal hasta que el DCF "cuadre". Eso es incorrecto por tres motivos:
- g por encima del tipo libre de riesgo (4,97 %) implica que la empresa acaba siendo más grande que la economía;
- la tabla de la §4.1 demuestra que, incluso con g = 4 % y un WACC 3 puntos más bajo, el caso base no pasa de 51 $;
- mezclar opcionalidad y negocio maduro en un solo número oculta lo que se está suponiendo.

Por eso aquí se separan: **valor del negocio reportado (10-55 $)** más una **opcionalidad implícita (~317-362 $ por acción)** que el mercado asigna.

**3. Cómo debería valorarse esa opcionalidad (no se hace en esta fase).** Lo adecuado sería un enfoque de probabilidades por escenarios o de opciones reales para cada iniciativa. Para cada una habría que fijar:
- el tamaño de mercado;
- la cuota;
- el margen;
- el calendario;
- la probabilidad de éxito;
- el capital necesario.

Como orden de magnitud, que sale directamente de la tabla de la §5: con la probabilidad P de que la opcionalidad se materialice, el resultado tendría que valer ~1,3-1,4 billones $ / P en valor presente. Con P = 50 %, serían ~2,7 billones $ de VP solo en nuevos negocios. Este cálculo es una lectura de la tabla, no un supuesto del modelo.

**4. Otras limitaciones:**
- La **dilución del plan del CEO** (hasta 423,7 M de acciones si se cumplen los hitos, Fase 1 §4) está ligada justo al éxito de la opcionalidad. Si la opcionalidad funciona, el valor se reparte entre más acciones; el modelo solo recoge una parte (la línea de dilución de la §3).
- La **amortización TTM** es una aproximación (3T × 4); el CSV de Fase 2 no la recoge.
- La **deuda** incluye deuda sin recurso que no se puede separar (Fase 2 §8).
- El **diferencial de la deuda** es un supuesto, aunque inmaterial.
- Las **betas de regresión** no indican su ventana de cálculo.
- **No se modela el circulante por separado**: va incluido en el ratio ventas/capital.
- Las **inversiones en SpaceX y xAI** (2.002 M$ y 2.000 M$, Fase 1 §4) están dentro de la caja neta o fuera de ella según cómo se contabilicen. Esa clasificación **no se ha verificado** y su impacto es de ~1 $ por acción.

---

## 7. Múltiplos frente a comparables

| Empresa | Grupo | EV/Ventas | EV/EBITDA | EV/EBIT | PER | Fuente y fecha |
|---|---|---:|---:|---:|---:|---|
| **Tesla (calculado)** | — | **13,9** | — | **414** | **410** | EV = 1.435.372 M$ (§1). Ingresos, EBIT y beneficio neto TTM de Fase 2. PER = precio / (beneficio neto TTM / media diluida de 3T) |
| Tesla (terceros) | — | 15,2 | 122,6 | 342,5 | 327,5 | [TipRanks](https://www.tipranks.com/stocks/tsla/statistics) (23-oct-2026) y [roic.ai](https://www.roic.ai/quote/TSLA/statistics) (EV/EBIT, sin fecha). [GuruFocus](https://www.gurufocus.com/news/9140534/tech-selloff-and-rising-oil-prices-pressure-markets-tesla-tsla-dips-amid-sector-weakness): PER TTM de 410,4 (23-oct-2026) |
| Toyota (TM) | Auto | 1,45 | 9,46 | 17,4 | 8,8 | [TipRanks](https://www.tipranks.com/stocks/tm/statistics) (23-oct-2026); EV/EBIT de [roic.ai](https://roic.ai/quote/TM/statistics) (30-jun-2026) |
| BYD (BYDDY) | Auto | 1,00 | 6,37 | 23,4² | 25,2 | [TipRanks](https://www.tipranks.com/stocks/byddy/statistics) (15-oct-2026); [roic.ai](https://www.roic.ai/quote/BYDDY/statistics) (30-jun-2026) |
| General Motors | Auto | 1,00 | 9,99 | 94,9³ | 17,2 | [TipRanks](https://www.tipranks.com/stocks/gm/statistics) (23-oct-2026); [roic.ai](https://www.roic.ai/quote/GM/statistics) (30-jun-2026) |
| Volkswagen (VWAGY) | Auto | 0,94 | 6,27 | 7,9² | 6,6 | [TipRanks](https://www.tipranks.com/stocks/vwagy/statistics) (24-oct-2026); [roic.ai](https://www.roic.ai/quote/VWAGY/statistics) (sin fecha) |
| Apple | Big tech | 9,36 | 26,97 | **SIN VERIFICAR** | 39,3 | [TipRanks](https://www.tipranks.com/stocks/aapl/statistics) (24-oct-2026) |
| Nvidia | Big tech | 21,04 | 31,43 | **SIN VERIFICAR** | 27,9 | [TipRanks](https://www.tipranks.com/stocks/nvda/statistics) (23-oct-2026) |
| Microsoft | Big tech | **SIN VERIFICAR** | **SIN VERIFICAR** | **SIN VERIFICAR** | **SIN VERIFICAR** | La página de TipRanks de EE. UU. no era accesible. MarketScreener daba estimaciones de FY2026, pero con fecha y capitalización no confirmadas, y no se usan |

² roic.ai muestra el mismo valor para EV/EBIT y EV/EBITDA en BYD y VW: el dato es dudoso.
³ El EV/EBIT de GM está distorsionado por cargos puntuales, a juzgar por la diferencia con su EV/EBITDA de ~10x. No se ha verificado.

**Advertencias de comparabilidad:**
- Las fechas no son homogéneas: los datos de TipRanks son de oct-2026 y los de roic.ai son de 30-jun-2026.
- Los EV de los fabricantes tradicionales (GM, VW, Toyota) incluyen deuda de sus financieras de crédito, lo que infla su EV/Ventas frente a Tesla.
- El PER de los pares de TipRanks no siempre indica si es TTM.

**Medianas y precio implícito de TSLA** (aplicando la mediana a los ingresos, el EBIT y el BPA TTM de Tesla, más la caja neta):

| Grupo | Mediana EV/Ventas | Mediana EV/EBIT | Mediana PER | Precio por EV/Ventas | Precio por EV/EBIT | Precio por PER |
|---|---:|---:|---:|---:|---:|---:|
| Auto (4) | 1,00 | 20,4 | 13,0 | 35,3 $ | 27,0 $ | 11,8 $ |
| Big tech (2) | 15,2 | SIN VERIFICAR | 33,6 | 407,4 $ | SIN VERIFICAR | 30,5 $ |

**Lectura:**
- **Como fabricante de automóviles**, los múltiplos dan **~12-35 $**, en línea con el DCF.
- **Solo el EV/Ventas de las grandes tecnológicas reproduce el precio** (~407 $). Pero ese múltiplo lo justifican márgenes operativos que en Apple y Nvidia son de varias veces el 3,4 % de Tesla. Con el PER de esas mismas tecnológicas, Tesla valdría ~31 $.
- El mercado valora a Tesla por sus ingresos **como si ya tuviera márgenes de software**, mientras que por beneficio la valora como un fabricante de coches en su peor momento de márgenes.

---

## 8. Conclusión en rangos (sin recomendación)

| Enfoque | Rango del valor por acción |
|---|---|
| DCF del negocio reportado, del bajista al alcista | **10-55 $** (base ~25 $) |
| Sensibilidad del caso base, WACC 8,6-13,6 % × g 2-4 % | 19-51 $ |
| Sensibilidad del caso base, margen 6-25 % × crecimiento 0,5-2x | 16-99 $ |
| Múltiplos de fabricantes de automóviles | 12-35 $ |
| Múltiplos de big tech (EV/Ventas frente a PER) | 31-407 $ |
| **Precio de mercado** | **372,22 $** |

El precio actual **no es explicable** por los flujos del negocio que Tesla reporta hoy, ni siquiera con supuestos que devuelven sus márgenes al máximo histórico. Es una **apuesta sobre negocios todavía sin ingresos** (robotaxi, Optimus, IA) por un importe implícito de **~1,25-1,43 billones $**.

Si esa apuesta está justificada o no depende de variables que hoy no tienen métrica pública (Fase 1 §5), y queda fuera de lo que este DCF puede afirmar. Los hitos que la harían verificable son estos:
- ingresos separados por robotaxi;
- unidades de Optimus vendidas fuera de Tesla;
- margen operativo sin créditos por encima del 10 %;
- ingresos de FSD desglosados.

---

*Reproducibilidad:* `python3 scripts/fase3_dcf.py` regenera `data/dcf.xlsx` e imprime todos los resultados de este documento. Los nuevos IDs de fuente (M1-M10) están en `fuentes/fuentes.md`.
