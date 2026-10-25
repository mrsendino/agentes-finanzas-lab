# 04 — Tesis alcista, tesis bajista y abogado del diablo (TSLA)

**Fecha del análisis:** 2026-10-24 · **Analista:** Fase 4 (rol *Investment Researcher*) · **Precio de referencia:** 372,22 $ (cierre del 23-oct-2026, 03 §1)
**Alcance:** contrastar dos tesis con el mismo rigor y definir qué datos las confirmarían o las refutarían. **No es una recomendación.** No hay precio objetivo ni lenguaje de compra o venta.

**Archivos de esta fase:**

| Archivo | Contenido |
|---|---|
| [`scripts/fase4_opcionalidad.py`](../scripts/fase4_opcionalidad.py) | Todas las cuentas de este documento: dimensionado de la opcionalidad, combinaciones, rangos y controles sobre 03 |
| [`fuentes/fuentes.md`](../fuentes/fuentes.md) | Fuentes nuevas T1–T10, más la relectura de P2 y P4 |

**Convenciones de etiquetado:**
- **[DEMOSTRADO]**: aparece en un documento presentado ante la SEC (P2, P4, etc.).
- **[CALL]**: lo dijo un directivo distinto de Musk en la conference call. No está auditado.
- **[MUSK]**: lo dijo Musk en una call o en un evento. No está auditado, y su historial de plazos se analiza en §3.2.
- **[SUPUESTO]**: hipótesis de esta fase. No es un dato y se declara para poder discutirla.
- **SIN VERIFICAR**: no se pudo contrastar.

Las cifras financieras son las corregidas en Fase 2 (02 §8.1): SBC de 3T26 de 1.165 M$, capex de 9M26 de 13.014 M$, deuda contable de 9.523 M$ a 30-sep-2026 y caja e inversiones de 45.447 M$.

---

## 0. Resumen

1. **Hechos.** El negocio que Tesla reporta vale entre ~10 $ y ~55 $ por acción (03 §3). Su margen operativo sin créditos es del 2,2 % (02 §3) y su ROIC del 5,5 %, por debajo de un WACC de ~11,6 %. Por tanto, **~93 % del precio (≈1,37 billones $ en el caso base) es opcionalidad**.
2. **Lo que exige el precio.** Para justificar esa brecha, los negocios nuevos tendrían que generar **~135.000-270.000 M$ de EBIT anual hacia 2036**, entre 39 y 78 veces el EBIT TTM de toda Tesla (script §3). Si ese EBIT llegara antes (año 7) o se valorara a 40x, la cifra baja a **~85.000-110.000 M$**.
3. **Tesis alcista.** Tesla es la única empresa que combina flota de datos, fabricación a escala, chip propio y energía. Lo que ya ha **demostrado** es real pero pequeño:
   - un robotaxi sin supervisión en varias ciudades, con ~2 M de millas acumuladas;
   - 1,74 M de clientes de FSD;
   - producción inicial de Optimus y de Cybercab.

   Una combinación "ambiciosa" (3 M de robotaxis, 5 M de Optimus al año, 15 M de clientes de FSD) cubre ~60 % del EBIT necesario.
4. **Tesis bajista.** El negocio base se erosiona: margen, créditos regulatorios, FCF − SBC negativo y ROIC inferior al WACC. Además:
   - la opcionalidad depende en gran parte de plazos dados por Musk, con un historial de retrasos documentado;
   - Waymo va por delante en volumen comercial;
   - el robotaxi con flota propia es intensivo en capital.

   Si el mercado recortara a la mitad el valor implícito de la opcionalidad, el precio sería de ~198 $ (−47 %).
5. **Contra el caso base de Fase 3:**
   - **Puede ser demasiado pesimista.** Carga al negocio actual el gasto en I+D de IA, la SBC del plan del CEO y el capex de Optimus, Cybercab y Terafab, pero pone sus ingresos a cero. Sin el aumento de I+D, el margen de 3T26 sería del 6,6 % y no del 2,6 %.
   - **Puede ser demasiado optimista.** Supone un margen del 8,9 %, un ROIC terminal del 12 % y ventas/capital de 1,5x, todos muy por encima de los datos TTM. Además, la línea de dilución de 03 probablemente cuenta dos veces las acciones restringidas.

**Horizonte:** las señales de §2.6 y §3.6 se evalúan en 4-8 trimestres (4T26-3T28). La valoración se refiere a 10 años.
**Confianza:**
- **Alta** en los datos del negocio reportado (fuentes primarias que cuadran, 02 §1.3).
- **Baja** en cualquier tamaño de la opcionalidad: no hay ingresos separados y casi todos los plazos son [MUSK] o [CALL].

---

## 1. Punto de partida común

Las dos tesis parten de los mismos hechos:

| Hecho | Valor | Fuente |
|---|---|---|
| Ingresos TTM | 103.570 M$ | 02 §2 |
| Margen operativo TTM sin créditos | 2,2 % (3T26 trimestral: 2,6 % GAAP) | 02 §3; P4 |
| Créditos regulatorios | 1.181 M$ TTM, −73 % interanual en 3T26 | 02 §2; P4 |
| FCF / FCF − SBC TTM | 3.303 / **−997 M$** | 02 §4 |
| ROIC A TTM / WACC inicial | 5,5 % / 11,6 % (diferencial −6,1 pp) | 02 §6; 03 §1.1; script §11 |
| Caja neta | 35.924 M$; además, línea de crédito de hasta 30.000 M$ sin disponer [CALL] | 02 §5; T1 |
| Capex 2026 | ~20.000 M$, revisado a la baja desde ">25.000 M$" [CALL] | T1; T10 |
| DCF del negocio reportado | 10 / 25 / 55 $ por acción | 03 §3 |
| Opcionalidad implícita | 1,25-1,43 billones $ (317-362 $ por acción) | 03 §5 |

**La pregunta que separa las dos tesis no es si Tesla es un buen fabricante de coches.** Los datos dicen que hoy es uno mediocre en rentabilidad. La pregunta es si los negocios nuevos pueden generar del orden de **100.000-250.000 M$ de EBIT anual** en un plazo de 7-10 años, y con qué probabilidad.

---

## 2. Tesis alcista

### 2.1 Argumento central

Tesla no se debe valorar como fabricante de automóviles. Es una plataforma de **IA física** con cuatro activos que ningún competidor reúne a la vez:
1. una flota de millones de vehículos que recoge datos de conducción;
2. capacidad de fabricación en serie a bajo coste;
3. hardware de inferencia propio (AI4 y AI5);
4. un negocio de energía que puede acompañar la demanda de cómputo.

El negocio de automoción es el vehículo que financia y alimenta de datos al software. Valorarlo con un margen del 2 % que ya incluye el gasto de I+D de esa IA infravalora el núcleo y pone a cero lo que está en construcción.

### 2.2 Qué está demostrado y qué solo anunciado

| Iniciativa | **Demostrado** (documento SEC) | **Anunciado** (call o evento) | Ausente o no reportado |
|---|---|---|---|
| **Robotaxi** | Cybercab en la flota de Austin desde el 3-sep-2026. Las millas sin supervisión se multiplicaron por 8 en el trimestre, hasta "nearly two million" acumuladas. Horario de 6:00 a 24:00 en Austin (P4) | "6 cities now" y Dallas con Cybercab "next month" [CALL, Elluswamy, T1]. La flota de Cybercab en Austin "has grown by a factor of 10 since launch" [MUSK, T1]. Más de 300 Cybercabs en Austin (T2, sin atribuir: **SIN VERIFICAR**). Robotaxi "noticeable" en 2T27 y "a big deal" en 3T-4T27 [MUSK, T1]. Camino a 0,30 $ por milla de coste operativo [CALL, Taneja] | Viajes pagados, tamaño de flota, ingresos e incidencias. Unsupervised en Dallas y Houston desde el 18-abr-2026 (T9, secundaria) |
| **Cybercab** | Capacidad instalada de ">125,000" al año (P4) | Capacidad real "significantly higher" [CALL, Moravy]. Primeras entregas a clientes a final de 2026 [CALL]. Flota mayoritariamente propiedad de Tesla [MUSK, T1] | Unidades producidas y coste por unidad |
| **FSD** | 1,04 → 1,74 M de suscripciones activas (+67 %), que incluyen compras por adelantado (P4; S2). Aprobado en 9 países de la UE, con >100.000 clientes allí (P4) | Más del 75 % de las entregas en Norteamérica incluyen FSD de pago [CALL, Taneja]. ARR de ~1.000 M$, cifra de un analista que el CFO calificó de "correct" [CALL]. FSD sin supervisión para clientes hacia 2T27, en algunas regiones y probablemente solo en autopista [CALL, Elluswamy]. Aprobación en toda la UE no más tarde de 1T27 [MUSK] | Ingresos de FSD desglosados y tasa de bajas |
| **Optimus** | "Optimus production began in Fremont on our high-volume lines… first production-quality bots" (P4). El 10-K advierte que "we have yet to commercialize Bots" (P1) | Línea diseñada para ~1 M de unidades al año (T2). Ritmo de 20.000 a la semana en "at least a year, maybe a little longer" [MUSK]. Ventas externas "towards the end of next year" (2027) [MUSK]. AI5 en Optimus hacia abr-2027 [MUSK] | Unidades, coste, precio y clientes |
| **Cómputo de IA** | 400 MW de cómputo de entrenamiento previstos a fin de 2026. Cortex 1 >105 MW y Cortex 2 >120 MW en producción. Austin Fab con puesta en marcha en 2027 (P4) | Terafab: primer chip de prueba en may-jun 2027 y volumen en 3T28. Inversión de "tens of billions" hasta 2028 y ">100.000 M$" a largo plazo [MUSK, T1]. Reparto de costes con SpaceX en negociación [CALL] | Cualquier ingreso: hoy es solo coste |
| **Energía** | 50,2 GWh desplegados en los últimos 12 meses (+7,5 % sobre FY25). Megafactory Texas de 50 GWh en marcha. Primeros Megapack con celdas LFP propias (P4; script §7) | Megapack "almost sold out" para 2027 y márgenes al alza [MUSK, T1] | Cartera de pedidos en GWh o $ |

**Lectura.** Lo demostrado es real y crece deprisa, pero desde una base minúscula:
- Si todas las ~2 M de millas sin supervisión se hubieran cobrado a 1-2 $ por milla, sumarían 2-4 M$ de ingresos acumulados, es decir, el **0,002-0,004 % de los ingresos TTM** (script §4).
- El FSD (~1.000 M$ de ARR, [CALL]) pesa ~1 % de los ingresos (script §6).

Todo lo que mueve la valoración está en la columna "anunciado".

### 2.3 Dimensionado: qué tendría que ser verdad

**Paso 1. EBIT necesario** (script §3). Se trata la brecha de valor como el valor presente de la opcionalidad y se capitaliza en el año 10 con 20-30x NOPAT, a una tasa del 9,8-11,6 %.

| Brecha | EBIT anual necesario en el año 10 |
|---|---|
| Rango completo (las tres brechas × r × múltiplo) | **134.680-271.287 M$** |
| Referencia central (brecha base, r = 9,79 %, 30x) | **147.561 M$** (43x el EBIT TTM) |
| Sensibilidad: 40x en el año 10 / 30x en el año 7 / 40x en el año 7 | 110.671 / 111.502 / 83.627 M$ |

Esta cuenta **favorece a la tesis alcista**: no descuenta el capital que haría falta invertir para generar ese EBIT.

**Paso 2. Tamaño de cada iniciativa** (todos los parámetros son [SUPUESTO], script §4-§7):

| Iniciativa | Supuestos | Resultado |
|---|---|---|
| **Robotaxi** | 40.000-60.000 millas pagadas por vehículo y año; 0,8-1,0 $ por milla; margen EBIT del 20-40 %; 5 millas por viaje; Cybercab a 30.000 $ (cifra citada por Musk en el pasado, **SIN VERIFICAR**) | EBIT de 8.000-24.000 $ por vehículo y año. **Para cubrir el EBIT central solo con robotaxi hacen falta 6-18 M de vehículos**: 3-9 M para cubrir la mitad. Con 3 M de vehículos se harían ~30.000 M de viajes al año, **2,2 veces los viajes de Uber en 2025** (13.567 M, que incluyen reparto a domicilio; T5), y la flota exigiría **~90.000 M$ de capital**, porque Musk dice que será de propiedad de Tesla |
| **Optimus** | Precio de 25.000 $ (Musk ha citado 20.000-30.000 $, **SIN VERIFICAR**); margen EBIT del 20-30 % | 1 M de unidades al año → EBIT de 5.000-7.500 M$. **Para cubrir el EBIT central solo con Optimus hacen falta 20-30 M de unidades al año.** La línea de Fremont está diseñada para ~1 M al año (T2) |
| **FSD (software)** | ARR implícito de ~575 $ por cliente (1.000 M$ / 1,74 M; derivado de una cifra de analista); escenario de 1.200 $ al año con margen del 80 % | 10 M de clientes → EBIT de 4.000-9.600 M$; 20 M → 19.200 M$. Al ritmo actual (+67 %) se alcanzarían 10 M de clientes en ~3,4 años; al +30 %, en ~6,7 |
| **Energía (extra)** | 200-500 GWh al año; 120-150 M$ por GWh, frente a 273 M$ en FY25, que incluye solar y es una cota superior; margen del 15-25 % | EBIT de 4.500-18.750 M$ |

**Paso 3. Combinaciones hacia el año 10** (script §8-§9):

| Combinación | Contenido | EBIT anual | % del EBIT central necesario | Valor presente si se materializa | Probabilidad que implica el precio |
|---|---|---:|---:|---:|---:|
| **A moderada** | 1 M de robotaxis, 1 M de Optimus al año (20 %), 10 M de clientes de FSD y 5.000 M$ extra de energía | 31.600 M$ | 21 % | 250.000-294.000 M$ (63-74 $ por acción) | >100 %: no alcanza |
| **B ambiciosa** | 3 M de robotaxis, 5 M de Optimus al año (25 %), 15 M de FSD y 10.000 M$ de energía | 91.650 M$ | 62 % | 725.000-854.000 M$ (183-216 $ por acción) | >100 %: no alcanza |
| **C extrema** | 10 M de robotaxis (caso ambicioso), 10 M de Optimus al año (30 %), 20 M de FSD y 20.000 M$ de energía | 354.200 M$ | 240 % | 2,8-3,3 billones $ (709-835 $ por acción) | **42-49 %** |

**Qué tiene que ser verdad para la tesis alcista**, en orden de importancia:
1. Una conducción sin supervisión **generalizable**: muchas ciudades, autopistas y meteorología adversa, sin operadores remotos en proporción relevante. Debe además llegar antes que la de Waymo y la de los rivales chinos a la escala de **millones** de vehículos.
2. Que el regulador lo permita en EE. UU., la UE y China en un plazo de 3-5 años.
3. Que Optimus encuentre demanda externa de **millones de unidades al año** con margen industrial. Hoy no existe un mercado de humanoides de ese tamaño que se pueda medir (**SIN VERIFICAR**).
4. Que la financiación (capex de ~20.000 M$ en 2026, Terafab por encima de 100.000 M$ [MUSK] y la flota de robotaxis) no destruya el valor por acción mediante deuda o dilución.
5. Que el valor no se reparta con partes vinculadas (SpaceX y xAI) en condiciones desfavorables.

### 2.4 Por qué el alcista puede tener razón aunque las cifras parezcan enormes

- **El sesgo del DCF juega en contra del alcista.** El margen de partida (2,2 %) incluye el aumento de I+D de IA (+1.131 M$ interanual en 3T26) y la SBC extra del plan del CEO (+2.301 M$ sobre FY24). Sumándolos de vuelta, el margen subyacente sería del **6,6 %** en 3T26 (6,2 % sin créditos) y del **4,5 %** en TTM (script §2). El caso base de 03 lo recupera solo a partir del año 5.
- **La adopción de FSD es una señal económica real.** Tesla lo considera "driving demand" (P4), y el +67 % interanual de suscripciones activas es un dato [DEMOSTRADO]. Que más del 75 % de las entregas en Norteamérica incluyan FSD de pago [CALL] apunta a que el software empieza a tener poder de precio.
- **Velocidad desde una base pequeña.** Las millas sin supervisión se multiplicaron por 8 en un trimestre (P4). En Waymo, los viajes semanales pasaron de ~400.000 a 500.000 entre febrero y abril de 2026 (+25 %; T3, T4). Si Tesla consigue una curva de crecimiento comparable con un coste por vehículo menor, la flota podría crecer más deprisa.
- **La energía tiene demanda declarada** ("almost sold out" en 2027 [MUSK]) y capacidad nueva de 50 GWh en Texas [DEMOSTRADO].
- **El balance financia la apuesta sin ampliar capital a corto plazo**: 35.924 M$ de caja neta más 30.000 M$ de línea de crédito [CALL].

### 2.5 Debilidades de la propia tesis alcista (reconocidas)

- La combinación B, que ya es ambiciosa (3 M de robotaxis, más del doble de los viajes de Uber; 5 M de humanoides al año), **no cubre** la brecha con las hipótesis centrales. Solo la cubre si el EBIT llega en el año 7 o el mercado paga 40x (paso 1).
- **Canibalización.** Las combinaciones no la restan: cada viaje en robotaxi puede sustituir la venta de un coche.
- **Dilución.** El valor de las combinaciones se reparte entre las 3.953 M de acciones de portada.

### 2.6 Señales de confirmación o refutación de la tesis alcista (4-8 trimestres)

| # | Señal | Métrica y umbral de **confirmación** | Umbral de **refutación** | Dónde se reporta |
|---|---|---|---|---|
| A1 | El robotaxi se convierte en negocio | Tesla publica ingresos o viajes pagados separados **antes de 3T27**, y las millas sin supervisión acumuladas superan los **50 M a 4T27** (≈1,9x trimestral durante 5 trimestres desde ~2 M; el último trimestre fue 8x, P4) | Sin desglose a 4T27, o millas acumuladas por debajo de 15 M | Deck 8-K Ex. 99.1 (sección SI & Other Services) y nota de ingresos del 10-Q |
| A2 | Escala geográfica sin supervisión | ≥ 15 áreas metropolitanas sin supervisión y servicio 24/7 con autopista **a fin de 2027** | ≤ 8 ciudades a fin de 2027 | Deck trimestral y posts de @robotaxi (contrastar con el deck) |
| A3 | FSD como software | Suscripciones activas ≥ **3,0 M en 3T27** (+70 %) y aprobación en toda la UE **antes del 2T27** | Crecimiento interanual de suscripciones inferior al 30 % en dos trimestres seguidos | Gráfico "Active FSD subscriptions" del deck; RDW y Comisión Europea |
| A4 | Optimus comercial | Primeros ingresos externos de Optimus o cifra de unidades publicada **antes del 4T27** | Sin unidades ni clientes externos a 4T27 | Deck y nota de ingresos del 10-Q/10-K |
| A5 | El negocio base deja de empeorar | Margen operativo sin créditos ≥ **5 % en dos trimestres seguidos**, con I+D todavía creciendo | — (ver B1) | Cuenta de resultados del 10-Q |
| A6 | Energía con margen estructural | ≥ **60 GWh TTM** y margen bruto de energía ≥ 25 % **sin** efectos puntuales (devoluciones arancelarias o ajustes de garantía) | Despliegues TTM por debajo de 45 GWh o margen sin efectos puntuales por debajo del 20 % | Deck: "Storage deployed" y margen del segmento; comentario de la call |

---

## 3. Tesis bajista

### 3.1 Argumento central

Por un lado, el negocio que Tesla tiene se está deteriorando y destruye valor con su coste de capital actual. Por otro, el que promete depende de plazos que la propia compañía no ha cumplido, en mercados donde ya hay rivales con ventaja comercial. El precio descuenta un éxito casi seguro y a escala masiva. Si sale un éxito parcial, la diferencia con el precio es de cientos de dólares por acción.

### 3.2 Los números de las Fases 2 y 3

- **Rentabilidad en mínimos.** El margen operativo ha pasado del 16,8 % (FY22) al 3,4 % TTM. Sin créditos queda en el 2,2 %. Los créditos, que en FY25 aportaban el 45,8 % del beneficio operativo, caen un −73 % por la ley OBBBA (02 §3; P4). **El colchón de margen casi total desaparece en 2026-2027.**
- **El crecimiento, sin rentabilidad, destruye valor.** El ROIC TTM es del 5,5 % (A) o del 2,9 % (B), frente a un WACC del 11,6 %. La tabla 4.2 de 03 muestra que con un margen del 6 % crecer más **reduce** el valor. Mientras el margen no supere ~9 %, el crecimiento de automoción y energía no crea valor.
- **La caja libre real es negativa.** El FCF − SBC TTM es de −997 M$ (02 §4). La SBC se ha más que duplicado: de 1.999 a 4.300 M$.
- **La intensidad de capital sube.**
  - Capex de ~20.000 M$ en 2026 [CALL], más del doble que en 2025.
  - Terafab: "tens of billions" hasta 2028 y más de 100.000 M$ a largo plazo [MUSK].
  - Una flota propia de 3 M de robotaxis costaría ~90.000 M$ (script §4).
  - Tesla ya ha asegurado 30.000 M$ de deuda disponible [CALL]. Su balance, que es la principal fortaleza financiera (02 §5), dejará de crecer.
- **Calidad del beneficio.** El margen bruto de energía del 33,1 % en 3T26, presentado sin matices en 01 §1.2, estuvo "helped by tariff refunds and warranty true-downs" [CALL, T1]. La partida "Other income" oscila entre −592 y +590 M$ por trimestre (02 §3).
- **Dilución mayor de lo que dice la media diluida.** Las acciones en balance pasaron de 3.324 M (30-sep-25) a 3.953 M (30-sep-26), un **+18,9 % en 12 meses**, mientras que la media básica solo sube 13 M (script §1; T6; P2). La diferencia (~713 M de acciones) está en circulación legal pero aún no "ganada". Si se cumplen los hitos, ese capital se reparte entre más acciones.

### 3.3 La opcionalidad no está asegurada

- **Historial de plazos de Musk** [MUSK, documentado]:
  - 2019: "very confident predicting autonomous robotaxis for Tesla next year" y ">1 million robotaxis on the road next year" (T7).
  - Objetivo de 5.000 Optimus en 2025, que no se cumplió según la prensa (T8).
  - En la call de 4T25 habló de "dozens" de ciudades a fin de 2026 (01 §5). En octubre de 2026 su equipo habla de "6 cities" (T1).
  - El FSD sin supervisión para clientes se va a 2T27, y solo en zonas concretas (T1; titular de Electrek en S2).

  **Un patrón de retrasos de 1 a 6 años** obliga a descontar los plazos actuales (robotaxi "big deal" en 3T-4T27, Optimus externo a fin de 2027).
- **Waymo va por delante en lo comercial.** Hacía ~500.000 viajes **pagados** a la semana en abril de 2026 (T4, solo secundaria) y apunta a más de 1 M a fin de 2026 (T3). Tesla no publica viajes pagados. Aun así, **Waymo representa el 0,19 % de los viajes anuales de Uber** (script §4): el mercado de robotaxi a la escala que necesita la tesis alcista no existe todavía para nadie.
- **Seguridad y regulación.** Un registro regulatorio recogió 14 colisiones de la flota piloto de Austin en su primera fase (T10, secundaria; **SIN VERIFICAR** en fuente primaria). Un incidente grave puede congelar permisos en varios estados a la vez.
- **Partes vinculadas y foco del CEO.**
  - El 10-K reconoce que Musk "does not devote his full time" a Tesla (P1).
  - Tesla tiene ~2.865 M$ en SpaceX contabilizados a valor razonable (P2, inferencia: 2.002 de compra + 863 de plusvalía no realizada).
  - Está negociando con SpaceX el reparto de costes de la Terafab [CALL].
  - Musk "declined to comment" sobre una posible fusión con SpaceX (T1).
  - Son transferencias de valor potenciales en ambos sentidos que el accionista minoritario no controla.
- **Competencia en energía.** Los integradores chinos tienen el 76 % del mercado (S9). La propia Tesla anticipó compresión de margen (S4), y los ingresos de energía caen un −5,7 % en 9M26 (02 §2).

### 3.4 Pérdida potencial cuantificada (script §10)

| Supuesto | Valor por acción | Frente a 372,22 $ |
|---|---:|---:|
| El mercado recorta a la mitad el valor implícito de la opcionalidad (base) | ~198 $ | −47 % |
| Base + 25 % de probabilidad de la combinación B | 70-79 $ | ≈ −79 % a −81 % |
| DCF alcista del negocio reportado, sin opcionalidad | 54,9 $ | −85 % |
| DCF base | 24,5 $ | −93 % |
| DCF bajista (casi todo es caja neta) | 10,4 $ | −97 % |

### 3.5 Debilidades de la propia tesis bajista (reconocidas)

- Usa márgenes que incluyen gasto en IA cuyo ingreso todavía no se ve. Si ese gasto da fruto, el bajista habrá medido mal el punto de partida (§2.4).
- Lleva cinco años "acertando" en el diagnóstico de los números sin que el precio le dé la razón. El precio puede seguir separado de los flujos durante mucho tiempo.
- El historial de retrasos también incluye entregas reales: el robotaxi sin supervisión existe, aunque llegara seis años tarde respecto a lo prometido.

### 3.6 Señales de confirmación o refutación de la tesis bajista (4-8 trimestres)

| # | Señal | Métrica y umbral de **confirmación** | Umbral de **refutación** | Dónde se reporta |
|---|---|---|---|---|
| B1 | Erosión del negocio base | Margen operativo sin créditos por debajo del **3 % durante 4 trimestres seguidos** (hasta 3T27) | ≥ 5 % durante dos trimestres (= A5) | Cuenta de resultados del 10-Q |
| B2 | Consumo de caja | FCF − SBC TTM negativo hasta 2027, o caja neta por debajo de **25.000 M$**, o disposición de la línea de 30.000 M$ | FCF − SBC TTM ≥ +3.000 M$ con capex ≥ 15.000 M$ | Estado de flujos y balance del 10-Q; nota de deuda |
| B3 | Retraso de la autonomía | 2T27 pasa **sin** ingresos separados de robotaxi, y el FSD sin supervisión para clientes no empieza **antes de 4T27** | Se cumplen A1 y A2 | Deck y nota de ingresos del 10-Q |
| B4 | La competencia marca la referencia | Waymo publica más de **1 M de viajes pagados a la semana** (en 2026-27) mientras Tesla no publica ninguna cifra comparable | Tesla publica viajes pagados ≥ 25 % de los de Waymo en el mismo trimestre | Nota de resultados de Alphabet; deck de Tesla |
| B5 | Dilución y SBC | SBC por encima del **5 % de los ingresos** TTM, o acciones en balance creciendo más de un 2 % anual sin contar el plan del CEO | SBC por debajo del 3 % de los ingresos | Estado de flujos y balance / estado de patrimonio del 10-Q |
| B6 | Volumen de automoción | Entregas TTM por debajo de **1,55 M** de vehículos con el ASP aún cayendo ("lower ASP" en el deck) | Entregas TTM ≥ 1,8 M con un margen bruto de automoción sin créditos ≥ 18 % | 8-K trimestral de entregas; deck |

---

## 4. Abogado del diablo: el caso base de Fase 3 en ambas direcciones

### 4.1 Por qué el caso base de 03 podría ser **demasiado pesimista**

1. **Asimetría de costes e ingresos.** El margen de partida del 2,21 % y la reinversión del 7,7 % de los ingresos en los años 1-2 cargan al negocio reportado:
   - la I+D de "SI and other R&D projects" (+1.131 M$ interanual, P4);
   - la SBC del plan del CEO (+2.301 M$ sobre FY24);
   - el capex de Optimus, Cybercab, Cortex y la Austin Fab.

   Al mismo tiempo, los ingresos de esas iniciativas se ponen a 0. Lo coherente sería **o** sacar esos costes del DCF del núcleo, **o** reconocer que la "opcionalidad implícita" de 317-362 $ es en parte el valor de un gasto que ya se está haciendo. Ajustado por la I+D incremental, el margen de 3T26 es del 6,6 % y no del 2,6 % (script §2).
2. **El capex de 2026 está sobreestimado.** 03 cita ">20.000-25.000 M$" (Fase 1). El CFO lo revisó a **~20.000 M$** en la call de 3T26 (T1). Con 13.014 M$ en 9M26, el 4T26 implícito es de ~7.000 M$.
3. **El WACC es alto para el negocio que se descuenta.** La beta de 1,59 mezcla al 50 % la beta de regresión (1,86), que refleja la volatilidad que **genera la opcionalidad**. Para descontar solo los flujos del núcleo, la beta del sector (1,32 → WACC de ~10,5 %) sería más coherente con el propio planteamiento de 03. El efecto es moderado: unos +4-10 $ por acción según la tabla 4.1.
4. **Activos no operativos fuera del cálculo.** La inversión en SpaceX está en "Other non-current assets" a valor razonable (P2), es decir, **no** en la caja neta. Son unos ~2.865 M$ (inferencia), a los que se suman 962 M$ en activos digitales. En total, ~1 $ por acción que no está en el valor de las acciones. Es inmaterial, pero 03 §6 lo dejaba sin verificar.
5. **El DCF inverso supone capital industrial también para el software.** Usa ventas/capital de 1,5x para todos los ingresos futuros. Si una parte relevante fuera FSD o software, el capital necesario sería mucho menor y la TACC requerida, también. En sentido contrario, el robotaxi con flota propia es más intensivo en capital (ver 4.2).

### 4.2 Por qué el caso base de 03 podría ser **demasiado optimista**

1. **Margen objetivo del 8,93 % (media FY21-24).** Esa media incluye el FY22 (14,6 %), con un ASP y un mix de producto que ya no existen. Desde 2023 el margen bruto está estructuralmente en ~18-19 % (02 §3) y los gastos operativos crecen un +39 % interanual (P4). **Cuadruplicar el margen en 5 años** sin ingresos nuevos es un supuesto alcista disfrazado de "base".
2. **ROIC terminal del 12 % y ventas/capital de 1,5x.** El ROIC TTM es del 5,5 % (A) o del 2,9 % (B), y la ventas/capital bruta de Fase 2 es de 1,05x. El caso base supone una eficiencia de capital **mejor que la actual en todos los ejes**, justo cuando el capex se duplica.
3. **Crecimiento del 12 % anual en energía.** Contradice el −5,7 % de 9M26 y el −16 % de 3T26 (02 §2). El margen del 33,1 % de 3T26 incluye efectos puntuales [CALL, T1].
4. **Línea de dilución probablemente mal construida** (§3.2; script §1):
   - Las acciones de portada (3.953 M) ya superan en ~713 M la media básica. El salto de +427 M en el 4T25 coincide en tamaño con las 423,7 M acciones restringidas del plan del CEO (S10), aunque esto es **inferencia y está SIN VERIFICAR**.
   - Si las acciones restringidas ya están en la portada, **sumar 301 M más (03 §3) cuenta dos veces** una parte de la dilución.
   - Y 03 §6.4 ("el modelo solo recoge una parte") estaría **al revés**: la portada ya recoge la dilución máxima del plan.
   - Efecto: sin las acciones del plan, el valor por acción sería de 11,6 / 27,5 / 61,5 $, frente a 10,4 / 24,5 / 54,9 $. Es inmaterial para la conclusión, pero es una incoherencia de método.

### 4.3 Otros puntos débiles, incoherencias o problemas de fuente en 03-valoracion.md

| # | Punto de 03 | Problema | Efecto |
|---|---|---|---|
| W1 | §1 y §3: denominador de acciones | Capitalización con 3.953 M (portada) pero PER con 3.541 M (media diluida). Con el mismo denominador que el EV, el PER es de **~457x**, no de 410x (script §1) | Presentación |
| W2 | §3: dilución adicional de 301 M | Posible doble cómputo (ver 4.2.4) | ≤ 3 $ por acción |
| W3 | §2.1: capex ">20.000-25.000 M$" | Desfasado: revisado a ~20.000 M$ en la call de 3T26 (T1) | Pesimista en los años 1-2 |
| W4 | §2.1: D&A TTM = 3T × 4 | Aproximación declarada. La D&A crece con el capex, así que sobreestima la D&A TTM y subestima el capex neto actual. Efecto en sentido contrario al de W3 | Pequeño |
| W5 | §5: "ingresos de Toyota ~289.000 M$" | **Mal citado.** No es un dato reportado: sale de EV / (EV/Ventas) de TipRanks (script §11). Además, el EV de Toyota incluye la deuda de su financiera, que 03 §7 reconoce que infla el EV/Ventas | Solo afecta a la comparación ("4-8 veces Toyota") |
| W6 | §2.2: margen base del 8,93 % frente a §4.2 | La propia tabla 4.2 de 03 muestra que con un margen del 6 % crecer destruye valor. Aun así, el caso base supone que el margen se cuadruplica sin explicar el mecanismo | Optimista |
| W7 | §2.2: crecimiento de energía | Incoherente con los datos de 2026 de Fase 2 (−5,7 % en 9M26) | Optimista |
| W8 | §6.4: SpaceX y xAI "dentro o fuera de la caja neta" | Resuelto: SpaceX está en "Other non-current assets" a valor razonable (P2), fuera de la caja neta. La inversión en xAI sigue **SIN VERIFICAR** en la parte del 10-Q que se pudo leer | ~+1 $ por acción |
| W9 | §1.1: beta inicial mezclada | Incoherente con descontar solo el núcleo (4.1.3) | Pesimista, moderado |
| W10 | §1: cifras de Fase 1 | Usa bien las cifras corregidas de Fase 2 (deuda de 9.523 M$ a 30-sep-26, caja de 45.447 M$). Sin incidencias | — |
| W11 | 01 §1.2 → 03 | El margen de energía de 3T26 (33,1 %) se presenta como operativo, cuando la call lo atribuye en parte a efectos puntuales | Afecta a la lectura cualitativa |

**Saldo del abogado del diablo.** Los puntos 4.1 y 4.2 se compensan en parte:
- Hacia arriba, el ajuste máximo razonable (margen de partida sin I+D incremental, WACC sectorial, capex revisado) mueve el caso base en **decenas de dólares**.
- Hacia abajo, los supuestos de margen, ROIC y energía podrían reducirlo hacia el caso bajista (~10 $).

**Ninguno de los dos ajustes cambia el orden de magnitud**: el negocio reportado vale 10-60 $ por acción y el precio de 372 $ depende de la opcionalidad.

---

## 5. Cierre: rangos por escenario (sin recomendación)

Fuente: script §10. Los valores con opcionalidad = valor DCF + probabilidad × valor presente de la combinación; el rango corresponde a r = 9,8-11,6 % y 30x NOPAT en el año 10.

| Escenario | Qué supone | Valor por acción |
|---|---|---:|
| Solo el negocio reportado | DCF de 03, de bajista a alcista | 10-55 $ |
| Opcionalidad modesta | Base + 50 % de probabilidad de la combinación A (1 M de robotaxis, 1 M de Optimus al año, 10 M de FSD) | 56-62 $ |
| Opcionalidad relevante | Base + 50 % de la combinación B (3 M de robotaxis, 5 M de Optimus al año, 15 M de FSD) | 116-133 $ |
| Éxito ambicioso asegurado | DCF alcista + combinación B al 100 % | 238-271 $ |
| Éxito extremo probable | Base + 50 % de la combinación C (10 M de robotaxis, 10 M de Optimus al año, 20 M de FSD) | 379-442 $ |
| Éxito extremo asegurado | DCF alcista + combinación C al 100 % | 764-889 $ |
| **Precio de mercado** | — | **372,22 $** |

**Cómo leer la tabla:**
- Con 30x NOPAT en el año 10, el precio actual equivale a asignar **~42-49 % de probabilidad a la combinación extrema C**, o más del 100 % a la ambiciosa B.
- Con hipótesis más generosas (40x o EBIT en el año 7), la combinación B al 100 % se acerca al precio.
- Las dos tesis coinciden en que el resultado depende casi por completo de la **autonomía a escala de millones de vehículos**, y en que no hay una métrica pública que lo verifique hoy.

Las señales A1-A6 y B1-B6 son los puntos de control que permitirán estrechar estos rangos en 2027.

---

## 6. Partidas SIN VERIFICAR nuevas en esta fase

1. **Composición de las ~713 M de acciones** en balance excluidas de la media básica, y si incluyen las 423,7 M del plan del CEO. El salto de +427 M en el 4T25 lo sugiere, pero no se leyó la nota correspondiente.
2. **Composición de las 202 M de acciones emitidas en 9M26** ("equity incentive awards and acquisitions"): si hubo adquisiciones pagadas en acciones y cuáles.
3. **Tamaño de la flota de robotaxi y de Cybercab.** Lo de ">300 Cybercabs" (T2) no está atribuido; el "factor of 10" es [MUSK]. No hay viajes pagados publicados.
4. **ARR de FSD de ~1.000 M$.** Es una cifra de analista confirmada de forma verbal por el CFO [CALL], no un dato contable. El ARPU de 575 $ que se deriva de ella hereda esa incertidumbre.
5. **Precio objetivo de Optimus (20.000-30.000 $) y coste del Cybercab (~30.000 $).** Son declaraciones pasadas de Musk, no verificadas en esta fase. Se usan solo como [SUPUESTO].
6. **Viajes pagados de Waymo después de abril de 2026** y si se alcanzó el objetivo de 1 M a la semana. Fuente solo secundaria (T4).
7. **Las 14 colisiones de la flota piloto de Austin** (T10): no se localizó el registro primario (NHTSA SGO).
8. **Inversión de 2.000 M$ en xAI**: dónde está contabilizada y por qué importe. No aparece en la parte leída del 10-Q 3T26.
9. **Valor contable exacto de la inversión en SpaceX.** Los ~2.865 M$ son inferencia (compra + plusvalía no realizada de 9M26).
10. **Tamaño actual del mercado de robots humanoides**: no hay dato fiable.
11. **Condiciones de la línea de crédito de 30.000 M$** [CALL]: no se encontró en la parte leída del 10-Q.

---

*Reproducibilidad:* `python3 scripts/fase4_opcionalidad.py` imprime todas las cifras de este documento. Las fuentes nuevas (T1-T10) y la relectura de P2 y P4 están en `fuentes/fuentes.md`.
