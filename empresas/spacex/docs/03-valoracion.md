# 03 — Valoración de SpaceX (SPCX): DCF por segmentos, escenarios, sensibilidad, DCF inverso y múltiplos

**Fecha del análisis:** 2026-10-25 · **Versión:** v1 · **Analista:** Fase 3 (rol *Financial Analyst*) · **Precio de referencia:** 147,49 $ (cierre del viernes 23-oct-2026, Nasdaq)
**Alcance:** esto es una valoración, no una recomendación de compra o venta. Los resultados son rangos que dependen de los supuestos declarados abajo; cambian mucho si cambian esos supuestos.

**Archivos de esta fase**

| Archivo | Contenido |
|---|---|
| [`scripts/fase3_dcf.py`](../scripts/fase3_dcf.py) | Todos los cálculos. **Importa** `fase2_ratios.py` y lee `data/spacex_financials.csv` y `data/ratios.csv` de la Fase 2: ninguna cifra histórica está copiada a mano. Los datos de mercado van en el diccionario `MKT` y en `PEERS`, cada uno con su fuente y fecha |
| [`data/dcf.xlsx`](../data/dcf.xlsx) | Hojas `Supuestos`, `Parametros`, `Esc_bajista`, `Esc_base`, `Esc_alcista`, `Sensibilidad`, `DCF_inverso`, `Multiplos` y `Beta`. Inputs en azul. El WACC, el FCFF, el descuento, el valor terminal, el EV y el valor por acción son **fórmulas vivas**, con una columna "Python" al lado para contrastar. **No está recalculado:** LibreOffice no está instalado en este equipo, así que el libro se guardó sin valores en caché (un visor que no recalcula mostrará vacías las celdas con fórmula; Excel las calcula al abrir) |
| [`data/precios_mercado_fase3.csv`](../data/precios_mercado_fase3.csv) | Cierres diarios de SPCX, SPY y QQQ del 12-jun al 23-oct-2026 (Nasdaq.com), para la beta de regresión |
| [`fuentes/nuevas_fase3_v1.md`](../fuentes/nuevas_fase3_v1.md) | Fuentes nuevas de esta fase (M1, M2, D1, D2, S3-S8) |

Todas las cifras de este documento se copian de la salida de `fase3_dcf.py`. Ninguna está calculada a mano. "M$" = millones de dólares.

---

## 0. Resumen

1. **El DCF no llega al precio en ninguno de los tres escenarios.** Con la base de acciones diluida (14.492,86 M), el valor por acción es de **0,61 $ (bajista), 25,27 $ (base) y 99,74 $ (alcista)**, frente a 147,49 $. El alcista queda un −32,4 % por debajo del precio y el base un −82,9 %.
2. **El problema no es el EBITDA, es el capex.** El modelo hace explícita la normalización: en el caso base el capex pasa del 171,5 % de los ingresos (TTM) al 72,9 % en el año 1, al 33,6 % en el año 3 y al 23,8 % en el año 10. El FCFF es negativo en los años 1 y 2 (−39.596 y −15.288 M$) y positivo desde el año 3. Ni con esa normalización el flujo es suficiente: cada dólar de ingreso nuevo de SI necesita 1,25 $ de capex (supuesto base) y las GPU se reponen cada 5 años.
3. **Casi todo el valor está en el valor terminal:** el 86,7 % del EV en el base y el 77,3 % en el alcista. En el bajista el EV es negativo (−33.650 M$): el crecimiento de SI con su intensidad de capital observada destruye valor, y el valor de las acciones (8.861 M$) es poco más que la caja neta.
4. **Customer B pesa unos 5,20 $ por acción en el caso base** (el 20,6 % del valor base): si rescinde en el año 1 y SpaceX solo recoloca la mitad de su capacidad, el base pasa de 25,27 $ a 20,08 $.
5. **Para justificar 147,49 $** con la estructura del caso base, los ingresos del año 10 tendrían que ser de 1.935.372 M$ (TACC del 50,7 % en 10 años, frente al 22,7 % del base); o el WACC inicial tendría que bajar al 4,63 %, por debajo del tipo libre de riesgo. Ningún margen de SI (hasta el 95 %) ni ninguna intensidad de capital (hasta 0,05) cierra la brecha por sí sola. Por múltiplos de comparables, la suma de partes da entre 26,22 $ y 43,37 $ por acción.

---

## 1. Inputs de mercado (con fuente y fecha)

| Input | Valor | Fuente y fecha |
|---|---|---|
| **Precio SPCX** | **147,49 $** | Cierre del 23-oct-2026 (viernes; el 25-oct es domingo), según el histórico de **Nasdaq.com** (M1: open 147,93; máx. 149,75; mín. 144,085). Coincide con stockanalysis.com (S3) y digrin.com (S4). **No existe fuente SEC para una cotización**; el dato procede del propio mercado de cotización, que es lo más cercano a una fuente primaria. El 147,49 $ "a 25-oct" que aportó el orquestador (investing.com) es este mismo cierre; investing.com devolvió 404 |
| Tipo libre de riesgo | **5,00 %** | Treasury a 10 años, 23-oct-2026, U.S. Department of the Treasury, *Daily Treasury Par Yield Curve Rates* (M2, primaria). El de 30 años estaba en el 5,33 % |
| Prima de riesgo del mercado (ERP) | **4,20 %** | ERP implícito del S&P 500 a 1-oct-2026, variante "Trailing 12 month, with adjusted payout" (Damodaran, D1). Las otras variantes publicadas van del 3,30 % al 5,67 % |
| Coste de la deuda antes de impuestos | **5,855 %** | Cupón medio ponderado de los 25.000 M$ de SpaceX Notes 2031-2056 (P9, vía Fase 1 §6.1). Después de impuestos: 4,63 % |
| Tipo impositivo | 21 % | Tipo federal normativo de EE. UU. (**supuesto**). El tipo efectivo de SpaceX no es representativo porque tiene pérdidas |
| Caja + valores negociables | 89.855 M$ | Fase 2 (`ratios.csv`, P3 balance a 30-sep-2026) |
| Deuda contable (incl. arrendamientos financieros) | 38.844 M$ | Fase 2. Caja neta: **51.011 M$** |
| Capitalización (precio × acciones de portada) | 2.003.071 M$ | Cálculo. Contraste: 2,00 bill. $ según stockanalysis.com (S5) |
| EV de mercado | 1.952.060 M$ | Capitalización − caja neta. Contraste: 1,95 bill. $ (S5) |

### 1.1 Beta: qué se usa y por qué (SUPUESTO)

SPCX cotiza desde el 12-jun-2026: solo hay **92 rentabilidades diarias**. La regresión existe, pero no sirve como estimación del riesgo a largo plazo:

| Regresión diaria de SPCX (12-jun a 23-oct-2026; M1) | Beta | Error típico |
|---|---|---|
| Frente a SPY | 3,28 | 0,65 |
| Frente a QQQ | 1,83 | 0,35 |
| Frente a SPY, sin la primera semana tras la OPV | 2,77 | 0,61 |
| Ajuste de Blume (0,67 × 3,28 + 0,33) | 2,53 | — |

La volatilidad anualizada de SPCX en el periodo fue del 81,3 %, frente al 11,6 % de SPY. Con una ventana tan corta, la beta mezcla el efecto de la salida a bolsa, la liberación anticipada de *lock-ups* y noticias propias (resultados, Customer B); el error típico de ±0,65 lo confirma. **Por eso el modelo usa una beta *bottom-up*:** para cada segmento, la media de (a) la beta desapalancada del sector de Damodaran (ene-2026, D2) y (b) la mediana de las betas desapalancadas de comparables cotizados (beta a 5 años de stockanalysis.com, S6, desapalancada con Hamada al 21 %):

| Segmento | Damodaran (sector) | Comparables desapalancados | Beta usada | Peso (ingresos año 1, base) |
|---|---|---|---|---|
| Space | 0,870 (Aerospace/Defense) | 2,930 (RKLB; FLY no tiene beta publicada; n = 1) | 1,900 | 4,9 % |
| Connectivity | 0,390 (Telecom Wireless) | 1,069 (mediana de IRDM 0,62, VSAT 1,07, ASTS 2,35) | 0,730 | 28,0 % |
| SI | 1,105 (media de Software 1,25 y Computer Services 0,96) | 1,272 (mediana de NBIS 1,23 y ORCL 1,31; CRWV sin beta publicada) | 1,188 | 67,1 % |

Las ponderaciones son los ingresos de cada segmento en el año 1 del caso base (no dependen del WACC, así que no hay circularidad).

### 1.2 WACC

| Paso | Valor | Cómo se obtiene |
|---|---|---|
| Beta desapalancada ponderada | 1,095 | Tabla anterior |
| Deuda / capitalización | 1,94 % | 38.844 / 2.003.071 |
| **Beta inicial (reapalancada)** | **1,112** | Hamada |
| Coste del capital propio inicial | 9,67 % | 5,00 % + 1,112 × 4,20 % |
| Coste de la deuda después de impuestos | 4,63 % | 5,855 % × 0,79 |
| **WACC inicial (años 1-5)** | **9,57 %** | Deuda al 1,90 % del capital |
| Beta terminal | 1,056 | A mitad de camino hacia 1 (empresa madura) |
| **WACC terminal (años 6-10 en convergencia lineal; perpetuidad)** | **9,34 %** | — |

Alternativas (efecto en §5): solo betas de Damodaran → WACC inicial del 8,73 %; solo comparables → 10,42 %; beta de regresión con Blume → 15,40 %.

---

## 2. Acciones: qué base se usa para el valor por acción

| Base | Acciones (M) | Qué incluye | Uso |
|---|---|---|---|
| Portada del 10-Q (A + B; la clase C ya no existe) | 13.581,06 | A 8.246,54 + B 5.334,52 a 15-oct-2026 (Fase 2, P3 portada). **Incluye** las 1.302,07 M acciones B restringidas de Musk, que ya están emitidas y votan | Capitalización de mercado |
| **Diluida (principal)** | **14.492,86** | Portada + 650 M de opciones y RSU vivas (A 158, B 350, RSU 142; Fase 2, P3) + ≈261,8 M acciones A pendientes para EchoStar (P3 MD&A, vía Fase 1). Las opciones se suman enteras: los precios de ejercicio no se han verificado, así que no se aplica el método del tesoro (criterio conservador) | **Valor por acción de este documento** |
| Sin las restringidas de Musk (informativa) | 12.278,99 | Portada − 1.302,07 M. Esas acciones solo consolidan con hitos de capitalización **y** una colonia en Marte o centros de datos orbitales (P2, vía Fase 1 §4.1) | Muestra cuánto pesan si nunca consolidan |

- **Puente de valor en la base diluida:** valor de las acciones = EV + caja neta (51.011 M$) − 8.500 M$ de pago en caja a EchoStar. Ese pago es "hasta 8.500 M$" según P3; **SIN VERIFICAR** si ya se hizo en el primer cierre. Se resta como pendiente porque se suman también las acciones pendientes.
- **No se suman los 1.333 M de "premios de rendimiento no cumplidos"** (Fase 2, P3 Note 13). **Inferencia:** esa cifra incluye casi seguro las 1.302,07 M acciones restringidas de Musk, que ya están en la portada; sumarlas sería contarlas dos veces.
- **No se suma dilución futura por SBC:** el modelo resta la SBC como un coste en caja (§3.1). Sumar además las acciones futuras sería contarla dos veces.
- Capitalización con la base diluida: 2.137.552 M$.

---

## 3. Estructura del modelo y supuestos

### 3.1 Mecánica

- **Año 0** = TTM a 3T26 (Fase 2): ingresos de 32.043 M$, EBITDA ajustado de 14.945 M$, SBC de 4.736 M$, capex de 54.960 M$ (171,5 % de los ingresos) y FCF de −39.198 M$. **Años 1-10** = periodos de 12 meses desde oct-2026 (A1 = oct-26 a sep-27). El año 11 solo sirve para el valor terminal. Descuento a final de año.
- **Ingresos por segmento** a partir de un *run-rate* anualizado (RR) a fin de cada año: ingresos del año = media del RR inicial y final. El RR de partida es el 3T26 × 4 en Connectivity (20.992 M$) y SI (30.240 M$), porque ambos crecen tan rápido que el TTM (16.024 y 11.862 M$) ya no describe el negocio actual. En Space se usa el TTM (4.157 M$), porque sus ingresos trimestrales son irregulares.
- **FCFF** = EBITDA ajustado − SBC − impuestos − capex. La variación de circulante se toma como cero (**supuesto**; en el TTM el FCO fue el 105,5 % del EBITDA ajustado, ayudado por anticipos de clientes, Fase 2 §5).
  - **La SBC se resta como coste real.** SI incluye además los 23.376 M$ de premios de Cursor pendientes de devengar (P3 Note 20), repartidos en 4 años (**supuesto**, SIN VERIFICAR el calendario).
  - **Impuestos:** 21 % del EBIT (EBITDA aj. − SBC − D&A), compensando las pérdidas que genere el propio modelo desde el año 1. No se usan bases imponibles negativas anteriores (SIN VERIFICAR su importe), lo que es conservador.
  - **D&A** (solo afecta al impuesto): la D&A del 3T26 × 4 se extingue linealmente en la vida útil del segmento y cada año de capex nuevo se amortiza en esa vida útil.
- **Valor terminal** = FCFF del año 11 / (WACC terminal − g). El FCFF del año 11 sale de las mismas fórmulas que los años 1-10, con el RR creciendo a g: la reinversión del valor terminal es coherente con el crecimiento, no un supuesto aparte.

### 3.2 Capex: cuándo y por qué se normaliza (no está escondido en el valor terminal)

**Connectivity y SI:** capex(t) = k × aumento del RR en el año (capacidad nueva) + k × RR(t−1) / L (reposición).
- **k** = dólares de capex por dólar de ingreso anual que aporta la capacidad. **L** = vida útil (5 años en ambos; **supuesto**, SIN VERIFICAR contra las políticas contables de P2).
- **k observado TTM** (capex TTM / [aumento del RR del 3T25 al 3T26 + RR del 3T25 / 5]): **0,494 en Connectivity y 1,615 en SI**. El de SI es una cota alta, porque parte del capex de 2026 es obra en curso para capacidad que aún no factura (la dirección habla de ~2,2 GW a fin de octubre y 2,5-3 GW a fin de año, S7, secundaria).
- **Contraste físico en SI:** el capex de SI de 9M26 dividido por el aumento de capacidad de 0,8 a 1,7 GW da **44,4 $ por vatio**. Con k = 1,615 eso equivale a 27,5 $ de ingreso anual por vatio; con k = 1,25 (base), a 35,6 $; con k = 0,90 (alcista), a 49,4 $, cerca de los ">50 $ por vatio" citados en la call (S7, secundaria, SIN VERIFICAR).
- **Por qué baja:** el capex/ingresos converge a k × (g + 1/L) cuando el crecimiento se frena. En SI base, con g = 3 % y L = 5 años, el capex del año 11 (perpetuidad) es el 28,3 % de los ingresos (§4.3). **La normalización depende de que el crecimiento del RR caiga**, no de un recorte arbitrario del capex.

**Space:** el capex/ingresos pasa linealmente del 116,6 % TTM a un nivel normalizado (50 % / 35 % / 25 %) en el año 6 / 4 / 3. **Supuesto:** el capex extraordinario corresponde a la infraestructura de Starship (Fase 2 §4) y se modera cuando Starship pasa a operación. Referencias: FY2023 42,1 %, FY2024 53,5 %, FY2025 93,8 %.

**Contraste con la guía (secundaria, SIN VERIFICAR):** la dirección habló de **35.000-40.000 M$ de capex solo en el 4T26** (S7). El capex del año 1 del modelo es de 46.633 / 62.864 / 87.767 M$ (bajista / base / alcista), es decir, el caso base supone que el capex de 2027 se frena con fuerza tras el 4T26. Si el capex de SI del año 1 siguiera al ritmo de esa guía (125.892 M$) sin más ingresos que los del base, el valor por acción bajaría a 21,40 $ (§5.2). Los compromisos no cancelables son de 37.840 M$, 25.569 M$ de ellos en 2027 (P3 Note 16, vía Fase 1): en el bajista se usan como suelo del capex de SI del año 1 aunque se pierda Customer B.

### 3.3 Customer B (34,5 % de los ingresos del 3T26; rescindible con 90 días)

- **Dato (Fase 2):** 5.028 M$ en el 3T26, que anualizados son **20.114 M$, el 66,5 % del RR de SI**. Sin B, el RR de SI es de 10.126 M$. Su identidad (la fase 1 infiere Anthropic) está **SIN VERIFICAR**. El contrato descrito en P2 (1.250 M$/mes hasta mayo de 2029) se puede rescindir con 90 días de preaviso.
- **Bajista:** B rescinde en el año 1. SpaceX recoloca su capacidad a la mitad del ingreso (**supuesto**: el cómputo se puede revender, pero no al mismo precio ni de inmediato). El resto de SI crece un 30 % en el año 1.
- **Base:** B sigue hasta mayo de 2029 y renueva con un **recorte de precio del 30 %** en el año 3 (−30 % × 20.114 M$ de RR), por la previsible bajada del precio del cómputo.
- **Alcista:** B renueva sin recorte.
- La sensibilidad de la §5.2 aísla su efecto dentro del caso base.

### 3.4 Guía del 1T27 (secundaria)

En la call del 3T26 la dirección habría dado una guía de **ingresos del 1T27 de 33.000-37.000 M$** para el grupo (S7, secundaria, **SIN VERIFICAR**: el 8-K P5 no la incluye). Si Space + Connectivity siguen al nivel del 3T26 (7.015 M$ por trimestre), eso implica un RR de SI de 103.940 M$ (extremo bajo) o 111.940 M$ (punto medio), frente a 30.240 M$ hoy. Al ser un dato secundario sin verificar, cada escenario le da un crédito distinto: **0 % en el bajista, 50 % del extremo bajo en el base, 100 % del punto medio en el alcista**.

### 3.5 Supuestos por escenario

| Supuesto | Bajista | Base | Alcista | Referencia (Fase 1 y 2) |
|---|---:|---:|---:|---|
| **Space**: crecimiento año 1 / años 2-5 | 0 % / 3 % | 5 % / 10 % | 10 % / 25 % | FY24 +6,7 %, FY25 +7,6 %, 9M26 +2,2 %. Alcista: Starship comercial (contrato lunar, Starfall; Fase 1 §1.3) |
| Space: margen EBITDA aj. en el año 5 (desde −8,4 % TTM) | 5 % | 20 % | 30 % | FY2023 28,0 %, FY2024 30,4 %, FY2025 16,0 % |
| Space: SBC / ingresos en el año 5 (15,3 % TTM) | 10 % | 8 % | 6 % | — |
| Space: capex normalizado / año en que se alcanza | 50 % / A6 | 35 % / A4 | 25 % / A3 | FY2023 42,1 %; TTM 116,6 % |
| **Connectivity**: crecimiento del RR año 1 / años 2-5 | 15 % / 8 % | 30 % / 15 % | 40 % / 22 % | Ingresos 3T26 +69,5 %, 9M26 +56,8 %, pero ARPU −16,9 % (Fase 1 §1.2) |
| Connectivity: margen EBITDA aj. en el año 3 (63,8 % TTM) | 55 % | 62 % | 65 % | 3T26 66,7 %; FY2025 62,9 % |
| Connectivity: k (L = 5) | 0,60 | 0,49 (observado) | 0,40 | k observado TTM 0,494 |
| **SI**: RR al final del año 1 | 23.221 | 67.090 | 111.940 | RR 3T26 30.240; ver §3.3-3.4 |
| SI: crecimiento del RR años 2-5 | 20/15/12/10 % | 30/20/15/12 % | 40/30/20/15 % | Dirección: ~13 GW de cómputo a fin de 2027 frente a 1,7 GW hoy (S7, secundaria) |
| SI: margen EBITDA aj. en el año 3 (42,7 % TTM; 65,5 % en el 3T26) | 30 % | 50 % | 60 % | CoreWeave: EBITDA 3.790 / ingresos 7.590 M$ TTM (S6). Fase 2 §9.2: sin B, el EBITDA de SI del 3T26 caería a −75 / 805 M$ |
| SI: SBC ordinaria / ingresos en el año 5 + Cursor | 10 % | 7 % | 5 % | + 5.844 M$/año de Cursor en los años 1-4 en los tres escenarios. SBC ordinaria de SI TTM: 20,1 % |
| SI: k (L = 5) | 1,62 (observado) | 1,25 | 0,90 | §3.2 |
| Customer B | Rescinde en A1 (recolocación 50 %) | Renueva en A3 con −30 % | Renueva sin recorte | §3.3 |
| Crecimiento terminal (g) | 2,5 % | 3,0 % | 3,5 % | Por debajo del tipo libre de riesgo (5,00 %) |
| **TACC de ingresos a 10 años (resultado)** | **11,7 %** | **22,7 %** | **32,5 %** | Ingresos del año 10: 96.993 / 248.713 / 533.131 M$ |

No se modelan como negocios separados el cómputo orbital, la Luna/Marte, Starlink Mobile a gran escala ni una posible fusión con Tesla (Fase 1 §5): no tienen ingresos ni métricas públicas. Solo entran a través de los crecimientos del alcista.

---

## 4. Resultados por escenario

### 4.1 Valor por acción frente al precio

| | Bajista | Base | Alcista |
|---|---:|---:|---:|
| VA de los FCFF de los años 1-10 (M$) | −52.847 | 42.987 | 318.069 |
| VA del valor terminal (M$) | 19.197 | 280.809 | 1.085.004 |
| **EV (M$)** | **−33.650** | **323.796** | **1.403.074** |
| **% del EV que viene del valor terminal** | −57,0 % (EV negativo) | **86,7 %** | **77,3 %** |
| Valor de las acciones, base diluida (M$) | 8.861 | 366.307 | 1.445.585 |
| **Valor por acción, base diluida** | **0,61 $** | **25,27 $** | **99,74 $** |
| Valor por acción, base portada | 1,28 $ | 27,60 $ | 107,07 $ |
| Valor por acción, sin restringidas de Musk | 1,41 $ | 30,52 $ | 118,42 $ |
| Frente al precio (147,49 $), base diluida | −99,6 % | −82,9 % | −32,4 % |
| Primer año con FCFF positivo | A7 | A3 | A3 |
| FCFF acumulado mínimo (necesidad de financiación) | −68.788 | −54.884 | −60.262 |

- El EV de mercado (1.952.060 M$) es 1,39 veces el EV del alcista y 6,03 veces el del base.
- **Necesidad de caja.** El FCFF acumulado mínimo consume el 61,1 % (base), el 67,1 % (alcista) y el 76,6 % (bajista) de los 89.855 M$ de caja y valores negociables a 30-sep-2026. Quedarían 34.971 / 29.593 / 21.067 M$, antes de vencimientos de deuda (no hay vencimientos materiales hasta 2031, Fase 2 §6). El modelo no necesita ampliar capital, pero gasta la mayor parte de la caja de la OPV.

### 4.2 Caso base: la senda del FCFF (M$)

| Año | Ingresos | EBITDA aj. | SBC | Impuestos | Capex | Capex / ingresos | FCFF | VA |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| TTM (histórico) | 32.043 | 14.945 | 4.736 | — | 54.960 | 171,5 % | −39.198 (FCF) | — |
| A1 | 86.279 | 41.271 | 17.309 | 694 | 62.864 | 72,9 % | −39.596 | −36.136 |
| A2 | 111.073 | 55.205 | 18.796 | 1.612 | 50.085 | 45,1 % | −15.288 | −12.734 |
| A3 | 131.700 | 67.813 | 18.823 | 2.936 | 44.241 | 33,6 % | 1.814 | 1.379 |
| A4 | 150.366 | 77.860 | 17.776 | 3.906 | 51.279 | 34,1 % | 4.899 | 3.398 |
| A5 | 170.942 | 88.995 | 10.288 | 6.232 | 54.621 | 32,0 % | 17.854 | 11.303 |
| A6 | 190.911 | 99.544 | 11.453 | 8.952 | 57.911 | 30,3 % | 21.229 | 12.271 |
| A7 | 209.542 | 109.392 | 12.538 | 10.336 | 60.165 | 28,7 % | 26.353 | 13.913 |
| A8 | 225.945 | 118.060 | 13.494 | 11.218 | 61.203 | 27,1 % | 32.145 | 15.508 |
| A9 | 239.258 | 125.084 | 14.272 | 12.111 | 60.908 | 25,5 % | 37.793 | 16.667 |
| A10 | 248.713 | 130.050 | 14.831 | 12.793 | 59.242 | 23,8 % | 43.184 | 17.418 |
| A11 (terminal) | 256.174 | 133.952 | 15.276 | 13.492 | 61.019 | 23,8 % | 44.165 | — |

El valor terminal del base es de 696.221 M$ (FCFF del año 11 de 44.165 M$ / (9,34 % − 3,0 %)).

### 4.3 Capex / ingresos por segmento (normalización explícita)

| Segmento y escenario | TTM | A1 | A3 | A5 | A10 | A11 (perpetuidad) |
|---|---:|---:|---:|---:|---:|---:|
| Space, bajista | 116,6 % | 105,5 % | 83,3 % | 61,1 % | 50,0 % | 50,0 % |
| Space, base | 116,6 % | 96,2 % | 55,4 % | 35,0 % | 35,0 % | 35,0 % |
| Space, alcista | 116,6 % | 86,0 % | 25,0 % | 25,0 % | 25,0 % | 25,0 % |
| Connectivity, bajista | 34,1 % | 19,5 % | 16,2 % | 16,2 % | 13,3 % | 13,3 % |
| Connectivity, base | 34,1 % | 21,3 % | 16,0 % | 16,0 % | 11,1 % | 11,1 % |
| Connectivity, alcista | 34,1 % | 20,0 % | 15,1 % | 15,1 % | 9,2 % | 9,2 % |
| SI, bajista | 376,4 % | 141,6 % | 52,7 % | 46,3 % | 36,0 % | 36,0 % |
| SI, base | 376,4 % | 92,6 % | 38,8 % | 37,7 % | 28,3 % | 28,3 % |
| SI, alcista | 376,4 % | 86,3 % | 39,1 % | 29,3 % | 20,8 % | 20,8 % |

**Lectura.** La mayor parte de la caída del ratio en el año 1 de SI no es menos capex en dólares, sino más ingresos: el capex de SI del año 1 en el base (53.622 M$) supera el TTM (44.645 M$), pero los ingresos de SI suben a 57.878 M$. En el bajista, en cambio, el capex de SI del año 1 (37.840 M$, el suelo de compromisos) se queda con solo 26.731 M$ de ingresos.

### 4.4 Ingresos y márgenes por segmento (M$)

| | Bajista A1 / A5 / A10 | Base A1 / A5 / A10 | Alcista A1 / A5 / A10 |
|---|---|---|---|
| Space | 4.157 / 4.611 / 5.280 | 4.261 / 6.100 / 8.341 | 4.365 / 10.047 / 19.286 |
| Connectivity | 22.566 / 31.627 / 40.795 | 24.141 / 44.617 / 68.302 | 25.190 / 59.236 / 106.771 |
| SI | 26.731 / 37.685 / 50.918 | 57.878 / 120.226 / 172.070 | 91.515 / 262.813 / 407.075 |
| Margen EBITDA aj. SI, A1 → A5 | 38,5 % → 30,0 % | 45,1 % → 50,0 % | 48,5 % → 60,0 % |

---

## 5. Sensibilidad

### 5.1 WACC inicial × crecimiento terminal (valor por acción, base diluida; el WACC terminal se desplaza lo mismo)

**Caso base**

| WACC inicial \ g | 2,0 % | 2,5 % | 3,0 % | 3,5 % | 4,0 % |
|---|---:|---:|---:|---:|---:|
| 7,57 % | 34,98 | 37,59 | 40,80 | 44,83 | 50,08 |
| 8,57 % | 28,00 | 29,61 | 31,53 | 33,83 | 36,67 |
| **9,57 %** | 23,01 | 24,06 | **25,27** | 26,70 | 28,39 |
| 10,57 % | 19,28 | 19,99 | 20,80 | 21,73 | 22,79 |
| 11,57 % | 16,42 | 16,91 | 17,46 | 18,08 | 18,79 |
| 12,57 % | 14,15 | 14,50 | 14,89 | 15,32 | 15,80 |

**Alcista**

| WACC inicial \ g | 2,0 % | 2,5 % | 3,0 % | 3,5 % | 4,0 % |
|---|---:|---:|---:|---:|---:|
| 7,57 % | 125,51 | 136,05 | 149,01 | 165,34 | 186,55 |
| 8,57 % | 101,14 | 107,90 | 115,93 | 125,61 | 137,51 |
| **9,57 %** | 83,64 | 88,22 | 93,53 | **99,74** | 107,12 |
| 10,57 % | 70,52 | 73,76 | 77,44 | 81,66 | 86,54 |
| 11,57 % | 60,38 | 62,74 | 65,38 | 68,36 | 71,74 |
| 12,57 % | 52,33 | 54,10 | 56,05 | 58,22 | 60,64 |

**Bajista:** entre −0,18 $ y 1,54 $ en toda la tabla (detalle en `dcf.xlsx`, hoja `Sensibilidad`).

Lectura: el precio solo aparece en la esquina del alcista con WACC inicial del 7,57 % y g ≥ 3,0 % (149,01 $ a 186,55 $). Con WACC 2 puntos por debajo y g del 4 %, el base llega a 50,08 $.

### 5.2 Customer B y los demás motores (caso base, valor por acción diluido)

| Variante | Valor por acción |
|---|---:|
| Base | 25,27 |
| Customer B rescinde en el año 1 (recolocación 50 %; sin crédito a la guía; suelo de capex) | 20,08 |
| Customer B rescinde en el año 1, pero se mantiene el resto del aumento de la guía (50 %) | 24,80 |
| Sin crédito a la guía secundaria del 1T27 (B sigue) | 22,39 |
| B renueva sin recorte de precio | 25,58 |
| B renueva con un recorte del 60 % | 24,97 |
| **Valor que depende de que B no rescinda (base − rescisión)** | **5,20 (20,6 % del base)** |

| Motor (bajo / base / alto) | Valor por acción |
|---|---|
| k de SI = 1,0 / 1,25 / 1,62 (observado) | 32,33 / 25,27 / 14,83 |
| Margen EBITDA aj. objetivo de SI = 40 % / 50 % / 60 % | 15,57 / 25,27 / 34,98 |
| Vida útil de SI = 4 / 5 / 6 años | 18,87 / 25,27 / 29,51 |
| Crédito a la guía del 1T27 = 0 % / 50 % / 100 % (extremo bajo) | 22,39 / 25,27 / 28,16 |
| Crecimiento de SI años 2-5 × 0,5 / × 1 / × 1,5 | 23,40 / 25,27 / 27,99 |
| Margen EBITDA aj. objetivo de Connectivity = 55 % / 62 % / 65 % | 22,62 / 25,27 / 26,41 |
| Capex normalizado de Space = 50 % / 35 % / 25 % | 24,49 / 25,27 / 25,80 |
| Capex de SI del año 1 al ritmo de la guía del 4T26 (125.892 M$), mismos ingresos | 21,40 |
| WACC inicial: solo Damodaran 8,73 % / solo comparables 10,42 % / regresión con Blume 15,40 % | 30,40 / 21,41 / 10,09 |
| Bajista con SI sin crecimiento tras el año 1 (solo reposición) | 4,40 (frente a 0,61) |

**Lectura.** Los motores más fuertes son la intensidad de capital de SI (k), su margen y la vida útil de las GPU, más que el crecimiento: con k = 1,25 y L = 5, crecer más en SI añade poco valor (× 1,5 en el crecimiento solo sube el base de 25,27 $ a 27,99 $). En el bajista, frenar el crecimiento de SI **aumenta** el valor (de 0,61 $ a 4,40 $): con un k de 1,62 y un margen del 30 %, crecer destruye valor.

---

## 6. DCF inverso: qué descuenta el precio de 147,49 $

| Pregunta (todo lo demás como en el caso base, base diluida) | Respuesta |
|---|---|
| ¿Cuánto tendría que crecer todo (multiplicador del crecimiento de los años 2-5 de los tres segmentos)? | **× 3,868**: ingresos del año 10 de **1.935.372 M$** (base 248.713), TACC a 10 años del **50,7 %** (base 22,7 %), con SI en 1.408.576 M$ en el año 10 |
| ¿Qué margen EBITDA aj. de SI? | **Ninguno basta**: incluso con un 95 % el valor es de 68,93 $ |
| ¿Qué intensidad de capital de SI (k)? | **Ninguna basta**: incluso con k = 0,05 el valor es de 59,14 $ |
| ¿Cuánto crédito a la guía del 1T27? | **Ninguno basta**: con 5 veces el aumento del extremo bajo el valor es de 51,26 $ |
| ¿Qué WACC inicial (WACC terminal desplazado igual)? | **4,63 %**, por debajo del tipo libre de riesgo del 5,00 %. Con el mínimo técnico (3,48 %) el valor sería de 880,70 $: la valoración es muy convexa a tasas bajas |
| Partiendo del **alcista**: ¿cuánto más crecimiento? | **× 1,414**: ingresos del año 10 de 825.281 M$ (TACC del 38,4 %), con SI en 627.457 M$ y Connectivity en 166.301 M$ |
| Partiendo del **alcista**: ¿qué margen EBITDA aj. de SI? | **80,2 %** (frente al 60 % del alcista y al 65,5 % del 3T26) |

**Lectura.** El precio no se explica por un único supuesto. Con la estructura del alcista (guía del 1T27 cumplida, Customer B renovado y k de 0,90), hace falta además un margen de SI del 80,2 % o multiplicar por 1,414 el crecimiento de los años 2-5, que lleve los ingresos a 825.281 M$ en 10 años. Como referencia, Microsoft ingresa 331.840 M$ TTM (S6).

---

## 7. Múltiplos frente a comparables

Fuente de todos los comparables: stockanalysis.com, cierre del 23-oct-2026 (S6, **secundaria**; múltiplos TTM calculados por el proveedor y **SIN VERIFICAR** contra los 10-Q de cada empresa).

| Comparable | Grupo | Precio ($) | EV (M$) | EV/Ventas | EV/EBITDA | EV/EBIT | PER |
|---|---|---:|---:|---:|---:|---:|---:|
| Rocket Lab (RKLB) | Lanzamiento | 52,60 | 29.230 | 38,00 | n/s | n/s | n/s |
| Firefly Aerospace (FLY) | Lanzamiento | 18,23 | 2.470 | 8,61 | n/s | n/s | n/s |
| Iridium (IRDM) | Satélites | 44,40 | 6.800 | 7,53 | 17,25 | 39,60 | 29,14 |
| Viasat (VSAT) | Satélites | 61,47 | 13.660 | 2,95 | 9,81 | 132,48 | n/s |
| AST SpaceMobile (ASTS) | Satélites | 39,79 | 16.190 | 140,42 | n/s | n/s | n/s |
| CoreWeave (CRWV) | Nube/IA | 54,24 | 75.940 | 10,01 | 20,04 | n/s | n/s |
| Nebius (NBIS) | Nube/IA | 158,74 | 45.660 | 33,70 | 176,99 | n/s | 966,38 |
| Oracle (ORCL) | Nube/IA | 126,16 | 514.520 | 7,17 | 14,94 | 20,92 | 19,78 |
| Microsoft (MSFT) | Nube/IA | 524,51 | 3.950.000 | 11,89 | 20,32 | 25,43 | 29,22 |

n/s = no significativo (EBITDA o beneficio negativos).

**SPCX (cálculo con los datos de Fase 2 y el precio del 23-oct):**

| Múltiplo | SPCX |
|---|---:|
| EV/Ventas TTM | 60,9x |
| EV/Ventas 3T26 × 4 | 33,5x |
| EV/EBITDA aj. TTM | 130,6x |
| EV/EBITDA aj. 3T26 × 4 | 55,4x |
| EV/(EBITDA aj. − SBC) TTM | 191,2x |
| EV/EBIT, PER, capitalización/FCF | n/s (resultado operativo, neto y FCF TTM negativos) |

Contraste: stockanalysis.com da 60,93x de EV/Ventas y 166,36x de EV/EBITDA, con un EBITDA de 11.740 M$ que no es el EBITDA ajustado de la empresa (S5).

**Suma de partes con las medianas de cada grupo:**

| Mediana aplicada | Space | Connectivity | SI | EV total (M$) | Valor por acción (diluida) | % del EV de mercado |
|---|---|---|---|---:|---:|---:|
| EV/Ventas TTM (23,30x / 7,53x / 10,95x) | 96.879 | 120.661 | 129.889 | 347.429 | 26,91 $ | 17,8 % |
| EV/Ventas sobre run-rate (Space TTM; Connectivity y SI 3T26 × 4) | 96.879 | 158.070 | 331.128 | 586.077 | 43,37 $ | 30,0 % |
| EV/EBITDA aj. TTM (Connectivity 13,53x, SI 20,18x; Space por EV/Ventas) | 96.879 | 138.385 | 102.232 | 337.496 | 26,22 $ | 17,3 % |

**Lectura.** Las medianas de los comparables llevan a valores de 26-43 $ por acción, en el mismo orden que el DCF base y alcista. Para llegar al precio con múltiplos haría falta aplicar a todo el grupo un múltiplo como el de Nebius (33,70x ventas) o el de ASTS (140,42x), que cotizan crecimiento futuro, no el negocio actual. La mediana de lanzamiento (23,30x) ya es generosa para Space, porque descansa en Rocket Lab (38,00x).

---

## 8. Diferencias y contradicciones con las fases 1 y 2

No se han editado los documentos de otras fases. Se comunica al orquestador:

1. **Apertura del primer día de cotización.** La Fase 1 (§6.1, fuente secundaria S1) dice que SPCX abrió a **160 $** el 12-jun-2026. El histórico de Nasdaq (M1) da una **apertura de 150,00 $** y un cierre de 160,95 $. Probablemente S1 confundió el cierre con la apertura. Conviene corregir 01 §6.1.
2. **S2 de la Fase 1 queda verificada.** El cierre de 162,57 $ del 9-oct-2026, que la Fase 1 marcó SIN VERIFICAR, coincide con Nasdaq (M1) y stockanalysis.com (S3).
3. **Fecha del precio del orquestador.** El 147,49 $ "a 25-oct-2026" es el cierre del viernes 23-oct-2026 (el 25-oct es domingo).
4. **Premios de rendimiento no cumplidos (1.333 M, 02 §7) y acciones restringidas de Musk (1.302,07 M).** La Fase 2 los presenta como dilución potencial adicional. **Inferencia:** los 1.333 M incluyen casi con seguridad las 1.302,07 M de Musk, que ya están en las acciones en circulación (02 §7 lo infiere). Si es así, no son dilución adicional. Conviene que la Fase 2 lo aclare con la Note 13 de P3.
5. **Guía de la dirección no recogida.** Ni la Fase 1 ni la Fase 2 citan la guía de la call del 3T26 (capex del 4T26 de 35.000-40.000 M$ e ingresos del 1T27 de 33.000-37.000 M$; S7, secundaria). Si se confirma, el capex del 4T26 por sí solo equivaldría al 63,7-72,8 % del capex TTM (54.960 M$), lo que cambia la lectura del FCF de 02 §5. No es una contradicción de cifras, sino un dato nuevo que debería verificarse con la transcripción.
6. **Capitalización de la Fase 1 §5 (cálculo ilustrativo).** Usa 13.174 M acciones a 135 $ con datos de 1-may-2026. Esta fase usa 13.581,06 M (portada a 15-oct) y 147,49 $. No es un error, solo un cambio de fecha.
7. **Sin contradicciones de cifras con la Fase 2.** Todas las cifras históricas del modelo se leen de sus ficheros y el script comprueba que los segmentos suman el total (ingresos, EBITDA ajustado y capex) y que la portada suma 13.581,06 M de acciones.

---

## 9. SIN VERIFICAR y limitaciones

- **Precio:** el dato es del mercado de cotización (Nasdaq.com), no de un documento SEC. Contrastado con dos secundarias.
- **Guía de la call del 3T26** (ingresos del 1T27, capex del 4T26, capacidad en GW, ">50 $/W"): solo secundaria (S7, S8). Afecta al caso base (crédito del 50 %) y al alcista.
- **Betas:** la de regresión de SPCX no es fiable con 92 observaciones. Las betas de los comparables son de un proveedor secundario. Space tiene un solo comparable con beta (RKLB), y la beta *bottom-up* elegida es un **supuesto**.
- **Múltiplos de los comparables:** secundarios, no reconstruidos desde sus 10-Q.
- **Customer B:** identidad (inferencia: Anthropic), coste y margen reales, y probabilidad de rescisión. La recolocación del 50 % y el recorte del 30 % en la renovación son supuestos.
- **Vidas útiles** (5 años en Connectivity y SI, 10 en Space) y **calendario de devengo de Cursor** (4 años): supuestos no contrastados con las notas contables de P2/P3.
- **EchoStar:** si los 8.500 M$ en caja ya se pagaron en el primer cierre, el valor por acción de la base diluida sube 0,59 $. El precio del espectro de 800 MHz (cierre previsto en el 1S27) no se ha publicado y no se incluye.
- **Bases imponibles negativas previas:** no se usan (importe SIN VERIFICAR); el modelo es algo conservador en impuestos.
- **Opciones:** se cuentan enteras, sin precios de ejercicio (SIN VERIFICAR).
- **Participaciones no operativas** (The Boring Company a valor razonable, Fase 1 §4.2): no se suman por falta de importe publicado.
- **Circulante:** se supone neutro. Los anticipos de clientes (+4.922 M$ en 9M26, Fase 2) podrían revertir si Customer B rescinde.
- **No se modelan:** cómputo orbital, Luna/Marte, Starlink Mobile como negocio separado ni la posible combinación con Tesla.
- **Excel sin recalcular:** LibreOffice no está instalado. Las fórmulas son correctas en Excel, pero el archivo no lleva valores en caché.

