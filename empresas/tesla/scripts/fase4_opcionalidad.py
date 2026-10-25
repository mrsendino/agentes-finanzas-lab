#!/usr/bin/env python3
"""
Fase 4 — Tesis alcista / bajista: dimensionado de la opcionalidad y controles de 03-valoracion.md.

Todos los números citados en docs/04-tesis.md salen de la salida de este script.
Convenciones:
  * Cifras en M$ salvo que se indique.
  * DATO = cifra con fuente (ID entre corchetes, ver fuentes/fuentes.md).
  * SUPUESTO = hipótesis de trabajo de esta fase (no es un dato; se declara para poder discutirla).
  * MUSK = afirmación hecha solo por Musk/directivos en una call o evento, no auditada.
"""
import math

def pr(*a):
    print(*a)

def h(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)

# ---------------------------------------------------------------------------------------------
# 0. Datos de fases anteriores (DATO)
# ---------------------------------------------------------------------------------------------
PRICE = 372.22                      # 03 §1 (M1)
SH_COVER = 3952.757946              # 10-Q 3T26 portada (P2/M3)
SH_DIL_3T = 3541.0                  # P2
SH_BAS_3T = 3240.0                  # P2
CEO_AWARD_SH = 423.7                # S10: acciones restringidas del plan 2025
MCAP = PRICE * SH_COVER
NETCASH = 35924.0                   # 02 §5
REV_TTM = 103570.0                  # 02 §2
EBIT_TTM = 3466.0                   # 02 §3
CRED_TTM = 1181.0                   # 02 §2
NI_TTM = 3218.0                     # 02 §3 (atribuible a comunes)
SBC_TTM = 4300.0                    # 02 §4
SBC_FY24 = 1999.0                   # 02 §4
FCF_TTM = 3303.0                    # 02 §4
ROIC_A_TTM = 0.055                  # 02 §6
WACC0 = 0.1160                      # 03 §1.1
WACC_T = 0.0979                     # 03 §1.1

EQ_DCF = {"bajista": 40940.0, "base": 96964.0, "alcista": 216931.0}   # 03 §3
VPS_DCF = {k: v / SH_COVER for k, v in EQ_DCF.items()}

# Trimestre 3T26 vs 3T25 (P4)
REV_Q3_26 = 28046.0
EBIT_Q3_26 = 718.0
RD_Q3_26 = 2761.0
RD_Q3_25 = 1630.0
OPEX_Q3_26 = 4776.0
OPEX_Q3_25 = 3430.0
CRED_Q3_26 = 113.0

# FSD (P4): suscripciones activas (M), 3T25..3T26
FSD_SUBS = [1.04, 1.10, 1.28, 1.48, 1.74]
FSD_ARR_ANALYST = 1000.0            # ~1.000 M$: estimación de un analista que el CFO calificó de "correct" (T1)

# Energía (P4/P6): despliegues GWh
STOR_FY25 = 46.7
STOR_Q = [12.5, 14.2, 8.8, 13.5, 13.7]  # 3T25..3T26
REV_ENERGY_FY25 = 12771.0

# Comparables robotaxi
WAYMO_RIDES_WEEK = 500_000          # abr-2026, Alphabet 1T26 vía T4 (solo secundaria)
WAYMO_RIDES_WEEK_FEB = 400_000      # feb-2026, T3
UBER_TRIPS_FY25 = 13_567.0          # M viajes, T5
UBER_GB_FY25 = 193_454.0            # M$, T5 (incluye Delivery)

h("1. Recuento de acciones y PER: ¿coherencia del denominador en 03-valoracion.md?")
pr(f"Capitalización (precio x acciones portada): {MCAP:,.0f} M$")
gap_cover_basic = SH_COVER - SH_BAS_3T
pr(f"Acciones portada - media básica 3T26: {gap_cover_basic:,.1f} M  (de ello, plan CEO 2025 restringido: {CEO_AWARD_SH} M)")
pr(f"Diferencia no explicada por el plan CEO: {gap_cover_basic - CEO_AWARD_SH:,.1f} M  -> SIN VERIFICAR (otras acciones restringidas / emitidas no vestidas)")
SH_EX_AWARD = SH_COVER - CEO_AWARD_SH
pr(f"Acciones portada sin el plan CEO (si estuviera incluido en la portada): {SH_EX_AWARD:,.1f} M")
for k in EQ_DCF:
    pr(f"  VPA {k:8s}: con portada {VPS_DCF[k]:6.2f} $ | sin acciones del plan CEO {EQ_DCF[k] / SH_EX_AWARD:6.2f} $ "
       f"| 03 añade además {SH_DIL_3T - SH_BAS_3T:.0f} M -> {EQ_DCF[k] / (SH_COVER + SH_DIL_3T - SH_BAS_3T):6.2f} $")
SH_OUT_SEP25 = 3324.0   # 10-Q 3T25, balance (T6)
SH_OUT_DEC25 = 3751.0   # 10-Q 3T26 (P2), balance
SH_OUT_SEP26 = 3953.0   # 10-Q 3T26 (P2), balance
ISSUED_9M26 = 202.0     # P2, estado de patrimonio: "Issuance of common stock for equity incentive awards and acquisitions"
pr(f"Acciones en balance: 30-sep-25 {SH_OUT_SEP25:,.0f} -> 31-dic-25 {SH_OUT_DEC25:,.0f} (+{SH_OUT_DEC25 - SH_OUT_SEP25:,.0f}) -> 30-sep-26 {SH_OUT_SEP26:,.0f} (+{SH_OUT_SEP26 - SH_OUT_DEC25:,.0f}; emitidas 9M26 según P2: {ISSUED_9M26:.0f})")
pr(f"Aumento total en 12 meses: {SH_OUT_SEP26 - SH_OUT_SEP25:,.0f} M ({SH_OUT_SEP26 / SH_OUT_SEP25 - 1:+.1%}) frente a media básica +{SH_BAS_3T - 3227:,.0f} M")
pr(f"Acciones en balance excluidas de la media básica 3T26: {SH_OUT_SEP26 - SH_BAS_3T:,.0f} M -> probablemente acciones restringidas emitidas no ganadas (SIN VERIFICAR la composición)")
pr("Implicación: la portada YA incluiría las acciones restringidas emitidas; sumar 301 M de 'stock-based awards' encima (03 §3) puede contar doble.")
pe_dil = PRICE / (NI_TTM / SH_DIL_3T)
pe_mcap = MCAP / NI_TTM
pr(f"PER 03 (precio / BPA con media diluida 3T): {pe_dil:,.0f}x | PER con capitalización / BN TTM (mismo denominador que el EV): {pe_mcap:,.0f}x")

h("2. ¿Carga el DCF al negocio actual los costes de la opcionalidad? (margen 'core' ajustado)")
d_rd = RD_Q3_26 - RD_Q3_25
ebit_q3_adj = EBIT_Q3_26 + d_rd
pr(f"I+D 3T26 - 3T25 = {d_rd:,.0f} M$ (Tesla lo atribuye a 'SI and other R&D projects', P4)")
pr(f"Margen operativo 3T26 GAAP: {EBIT_Q3_26 / REV_Q3_26:.1%} | sumando el incremento de I+D: {ebit_q3_adj / REV_Q3_26:.1%}")
pr(f"  ídem sin créditos: {(EBIT_Q3_26 - CRED_Q3_26) / (REV_Q3_26 - CRED_Q3_26):.1%} -> {(ebit_q3_adj - CRED_Q3_26) / (REV_Q3_26 - CRED_Q3_26):.1%}")
d_sbc = SBC_TTM - SBC_FY24
m_ex = (EBIT_TTM - CRED_TTM) / (REV_TTM - CRED_TTM)
m_ex_adj = (EBIT_TTM - CRED_TTM + d_sbc) / (REV_TTM - CRED_TTM)
pr(f"SBC TTM - SBC FY24 = {d_sbc:,.0f} M$ (coincide con el plan CEO 2025, P4)")
pr(f"Margen TTM sin créditos: {m_ex:.2%} | añadiendo de vuelta el exceso de SBC: {m_ex_adj:.2%}")
pr("Lectura: el punto de partida del DCF (2,21 %) incluye costes ligados a la opcionalidad cuyos ingresos el modelo pone a 0.")

h("3. ¿Cuánto EBIT tendría que generar la opcionalidad en el año 10? (orden de magnitud)")
pr("Método: brecha de valor G (03 §5) = VP de la opcionalidad. Valor en año 10 = múltiplo x NOPAT_10.")
pr("NOPAT_10 = G x (1+r)^10 / múltiplo ; EBIT_10 = NOPAT_10 / 0,79. Ignora el capital a invertir (favorece a la tesis alcista).")
GAP = {k: MCAP - v for k, v in EQ_DCF.items()}
req = {}
for k, G in GAP.items():
    for r in (WACC_T, WACC0):
        for mult in (20, 30):
            nopat10 = G * (1 + r) ** 10 / mult
            ebit10 = nopat10 / 0.79
            req[(k, r, mult)] = ebit10
            pr(f"  brecha {k:8s} {G:,.0f} | r={r:.2%} | {mult}x NOPAT -> EBIT_10 necesario {ebit10:,.0f} M$ "
               f"({ebit10 / EBIT_TTM:,.0f}x EBIT TTM)")
for mult, yr in ((40, 10), (30, 7), (40, 7)):
    e = GAP["base"] * (1 + WACC_T) ** yr / mult / 0.79
    pr(f"  sensibilidad: brecha base | r={WACC_T:.2%} | {mult}x NOPAT en el año {yr} -> EBIT necesario {e:,.0f} M$")
EBIT_REQ_LO = min(req.values())
EBIT_REQ_HI = max(req.values())
EBIT_REQ_MID = req[("base", WACC_T, 30)]
pr(f"Rango EBIT_10 necesario de la opcionalidad: {EBIT_REQ_LO:,.0f} - {EBIT_REQ_HI:,.0f} M$ ; referencia central (base, r={WACC_T:.2%}, 30x): {EBIT_REQ_MID:,.0f} M$")

h("4. Robotaxi: economía por vehículo (SUPUESTOS) y flota necesaria")
# SUPUESTOS declarados
RT_CASES = {
    # nombre: (millas pagadas/vehículo/año, precio $/milla, margen EBIT)
    "prudente":  (40_000, 1.00, 0.20),
    "central":   (50_000, 0.80, 0.30),
    "ambicioso": (60_000, 1.00, 0.40),
}
TRIP_MILES = 5.0         # SUPUESTO: milla media por viaje
CYBERCAB_COST = 30_000   # SUPUESTO ($/vehículo); Musk ha hablado de <30.000 $ -> MUSK / SIN VERIFICAR
for n, (mi, p, m) in RT_CASES.items():
    rev_v = mi * p
    ebit_v = rev_v * m
    pr(f"  {n:9s}: ingresos/vehículo {rev_v:,.0f} $ | EBIT/vehículo {ebit_v:,.0f} $")
    for fleet_m in (1, 3, 10):
        ebit = fleet_m * 1e6 * ebit_v / 1e6
        trips = fleet_m * 1e6 * mi / TRIP_MILES / 1e6
        pr(f"     flota {fleet_m:>2} M -> ingresos {fleet_m * rev_v:,.0f} M$ ; EBIT {ebit:,.0f} M$ ; "
           f"viajes {trips:,.0f} M/año = {trips / UBER_TRIPS_FY25:.1f}x viajes Uber FY25 ; capital flota {fleet_m * CYBERCAB_COST / 1e3:,.0f} mil M$")
    need = EBIT_REQ_MID / (ebit_v / 1e6) / 1e6
    pr(f"     flota necesaria para cubrir el 100 % del EBIT_10 central ({EBIT_REQ_MID:,.0f} M$): {need:,.1f} M vehículos")
    pr(f"     flota necesaria para cubrir el 50 %: {need / 2:,.1f} M vehículos")
RT_MILES_CUM = 2.0  # M millas sin supervisión acumuladas a 30-sep-26 (P4)
for p_ in (1.0, 2.0):
    pr(f"Ingresos acumulados máximos del robotaxi a {p_:.2f} $/milla sobre {RT_MILES_CUM} M millas (si todas fueran pagadas): {RT_MILES_CUM * p_:,.1f} M$ = {RT_MILES_CUM * p_ / REV_TTM:.4%} de los ingresos TTM")
waymo_y = WAYMO_RIDES_WEEK * 52 / 1e6
pr(f"Waymo: {WAYMO_RIDES_WEEK:,} viajes/semana (abr-26) = {waymo_y:,.0f} M/año = {waymo_y / UBER_TRIPS_FY25:.2%} de los viajes de Uber FY25")
pr(f"Waymo feb->abr 2026: {WAYMO_RIDES_WEEK / WAYMO_RIDES_WEEK_FEB - 1:+.0%}")
pr(f"Uber: reservas brutas / viaje FY25 = {UBER_GB_FY25 / UBER_TRIPS_FY25:.2f} $ (incluye Delivery)")

h("5. Optimus: unidades necesarias (SUPUESTOS)")
OPT_PRICE = 25_000       # SUPUESTO (Musk ha citado 20-30 k$: MUSK / SIN VERIFICAR)
for m in (0.20, 0.30):
    for units_m in (1, 5, 10):
        ebit = units_m * 1e6 * OPT_PRICE * m / 1e6
        pr(f"  margen {m:.0%} | {units_m:>2} M unid./año -> ingresos {units_m * OPT_PRICE / 1e3:,.0f} mil M$ ; EBIT {ebit:,.0f} M$")
    need = EBIT_REQ_MID * 1e6 / (OPT_PRICE * m) / 1e6
    pr(f"  margen {m:.0%}: unidades/año para cubrir el 100 % del EBIT_10 central: {need:,.1f} M")
LINE_CAP = 1.0           # M/año: diseño de la línea de Fremont (T1/T2, Tesla en la call)
RAMP = 20_000 * 52 / 1e6
pr(f"Línea Fremont diseñada para ~{LINE_CAP:.0f} M/año (call); 20.000/semana (MUSK, 'al menos un año') = {RAMP:.2f} M/año")

h("6. FSD como software")
growth_yoy = FSD_SUBS[-1] / FSD_SUBS[0] - 1
pr(f"Suscripciones activas 3T25->3T26: {FSD_SUBS[0]} -> {FSD_SUBS[-1]} M ({growth_yoy:+.0%})")
arpu = FSD_ARR_ANALYST / FSD_SUBS[-1]
pr(f"ARR ~{FSD_ARR_ANALYST:,.0f} M$ / {FSD_SUBS[-1]} M = {arpu:,.0f} $/cliente/año (derivado de una estimación de analista)")
for g in (growth_yoy, 0.30):
    yrs = math.log(10 / FSD_SUBS[-1]) / math.log(1 + g)
    pr(f"  años hasta 10 M (hito del plan CEO) creciendo al {g:.0%}: {yrs:.1f}")
for subs, price, m in ((10, arpu, 0.7), (10, 1200, 0.8), (20, 1200, 0.8)):
    pr(f"  {subs} M clientes x {price:,.0f} $/año x margen {m:.0%} -> EBIT {subs * price * m:,.0f} M$")
pr(f"Peso actual del ARR FSD sobre ingresos TTM: {FSD_ARR_ANALYST / REV_TTM:.1%}")

h("7. Energía")
rev_per_gwh = REV_ENERGY_FY25 / STOR_FY25
pr(f"Ingresos Energía FY25 / GWh desplegados = {rev_per_gwh:,.0f} M$/GWh (incluye solar: cota superior)")
ttm_gwh = sum(STOR_Q[1:])
pr(f"GWh TTM 4T25-3T26: {ttm_gwh:.1f} vs FY25 {STOR_FY25}: {ttm_gwh / STOR_FY25 - 1:+.1%}")
for gwh, p, m in ((200, 150, 0.15), (500, 120, 0.15), (500, 150, 0.25)):
    pr(f"  {gwh} GWh/año x {p} M$/GWh x margen EBIT {m:.0%} -> ingresos {gwh * p:,.0f} ; EBIT {gwh * p * m:,.0f} M$")

h("8. Combinaciones alcistas (año ~10) frente al EBIT necesario")
COMBOS = {
    # robotaxi (flota M, caso) ; optimus (M unid, margen) ; FSD (M clientes, $/año, margen) ; energía extra EBIT
    "A moderada":  ((1, "central"), (1, 0.20), (10, 1200, 0.8), 5000),
    "B ambiciosa": ((3, "central"), (5, 0.25), (15, 1200, 0.8), 10000),
    "C extrema":   ((10, "ambicioso"), (10, 0.30), (20, 1200, 0.8), 20000),
}
COMBO_EBIT = {}
for n, ((fl, case), (ou, om), (fs, fp, fm), en) in COMBOS.items():
    mi, p, m = RT_CASES[case]
    e_rt = fl * mi * p * m
    e_op = ou * OPT_PRICE * om
    e_fsd = fs * fp * fm
    tot = e_rt + e_op + e_fsd + en
    COMBO_EBIT[n] = tot
    pr(f"  {n:12s}: robotaxi {e_rt:,.0f} + Optimus {e_op:,.0f} + FSD {e_fsd:,.0f} + energía extra {en:,.0f} = {tot:,.0f} M$ "
       f"-> {tot / EBIT_REQ_MID:.0%} del EBIT_10 central ; {tot / EBIT_REQ_LO:.0%} del mínimo ; {tot / EBIT_REQ_HI:.0%} del máximo")

h("9. VP de cada combinación si se materializa, probabilidad implícita y valor por acción")
PV_SUCCESS = {}
for n, e in COMBO_EBIT.items():
    for r in (WACC_T, WACC0):
        pv = e * 0.79 * 30 / (1 + r) ** 10
        PV_SUCCESS[(n, r)] = pv
        p_impl = GAP["base"] / pv
        pr(f"  {n:12s} r={r:.2%} 30x NOPAT: VP {pv:,.0f} M$ ({pv / SH_COVER:,.0f} $/acc.) ; probabilidad implícita en el precio (brecha base) {p_impl:.0%}")

h("10. Rangos por escenario (valor por acción, $)")
base_core = VPS_DCF["base"]
pr(f"Negocio reportado (03): bajista {VPS_DCF['bajista']:.1f} | base {base_core:.1f} | alcista {VPS_DCF['alcista']:.1f}")
for n in COMBOS:
    for P in (0.10, 0.25, 0.50):
        lo = base_core + P * PV_SUCCESS[(n, WACC0)] / SH_COVER
        hi = base_core + P * PV_SUCCESS[(n, WACC_T)] / SH_COVER
        pr(f"  base + {P:.0%} x combinación {n:12s}: {lo:,.0f} - {hi:,.0f} $")
for n in COMBOS:
    lo = VPS_DCF["alcista"] + PV_SUCCESS[(n, WACC0)] / SH_COVER
    hi = VPS_DCF["alcista"] + PV_SUCCESS[(n, WACC_T)] / SH_COVER
    pr(f"  alcista + combinación {n} materializada al 100 %: {lo:,.0f} - {hi:,.0f} $")
# Dilución del plan CEO si se materializa la opcionalidad (los hitos están ligados a ella)
dil_factor = SH_COVER / (SH_COVER + CEO_AWARD_SH)
pr(f"Si las acciones del plan CEO NO estuvieran en la portada y vestasen: factor {dil_factor:.3f} (-{1 - dil_factor:.1%}) sobre los valores con éxito")
for k, v in VPS_DCF.items():
    pr(f"Caída hasta el VPA DCF {k}: {v / PRICE - 1:+.0%}")
half = base_core + 0.5 * (PRICE - base_core)
pr(f"Precio si el mercado recortara a la mitad el valor implícito de la opcionalidad (base): {half:,.0f} $ ({half / PRICE - 1:+.0%})")

h("11. Otros controles sobre 03-valoracion.md")
toyota_rev_03 = 418590 / 1.45
pr(f"'Ingresos Toyota' de 03 = EV / (EV/Ventas) = {toyota_rev_03:,.0f} M$ -> derivado, no reportado; el EV de Toyota incluye deuda de su financiera")
pr(f"Capex 2026: 03 usa '>20.000-25.000 M$'; el CFO lo revisó a ~20.000 M$ en la call 3T26 (T1). 9M26 = 13.014 -> 4T26 implícito ~{20000 - 13014:,.0f} M$")
pr(f"ROIC A TTM {ROIC_A_TTM:.1%} vs WACC inicial {WACC0:.1%}: diferencial {ROIC_A_TTM - WACC0:+.1%}")
pr(f"FCF - SBC TTM: {FCF_TTM - SBC_TTM:,.0f} M$")

h("12. Umbral de la señal A1")
q_growth = (50 / RT_MILES_CUM) ** (1 / 5)
pr(f"De {RT_MILES_CUM} M a 50 M millas acumuladas en 5 trimestres (3T26->4T27): crecimiento trimestral necesario {q_growth:.2f}x")
