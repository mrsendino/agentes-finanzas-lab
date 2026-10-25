#!/usr/bin/env python3
"""
Fase 4 — Tesis alcista / bajista: dimensionado de la opcionalidad y controles de 03-valoracion.md.

Todos los números citados en docs/04-tesis.md salen de la salida de este script.
v2 (2026-10-25): ronda de correcciones tras 05-veredicto.md (W1, W2, W3/§4.1.2, W5, W9).
v2.1 (2026-10-25): sincronización con 02 v2 (§5.1, descomposición de acciones) y 03 v2. El modelo de Fase 3
(scripts/fase3_dcf.py) se importa AL PRINCIPIO, en una COPIA TEMPORAL de scripts/ y data/, y de él salen los valores
DCF por escenario (antes estaban copiados a mano de 03 v1), las acciones totalmente diluidas y las mediciones de §13.
No escribe nada en data/ del proyecto.
v3 (2026-10-25): sincronización con 03 v3 (beta de regresión 1,84 -> WACC inicial 11,55 %). Las tasas WACC0 y WACC_T se
toman del modelo importado (antes WACC0 = 0,1160 estaba copiado a mano de 03 v2). Nueva §14: imprime cada cifra que
04 copia, redondeada UNA sola vez (mitad hacia arriba, Decimal) desde el valor completo y con el formato del documento.
v4 (2026-10-25): M-v3-1 de 05-veredicto-v3.md. ROIC A TTM a precisión completa (antes 0.055 a mano) y las demás cifras
de 02/03 (precio, caja neta, ingresos, EBIT, créditos, BN, SBC, FCF, plan CEO, energía FY25) leídas de ratios.csv / del modelo.
Convenciones:
  * Cifras en M$ salvo que se indique.
  * DATO = cifra con fuente (ID entre corchetes, ver fuentes/fuentes.md).
  * SUPUESTO = hipótesis de trabajo de esta fase (no es un dato; se declara para poder discutirla).
  * MUSK = afirmación hecha solo por Musk/directivos en una call o evento, no auditada.
"""
import contextlib
import importlib.util
import io
import math
import os
import shutil
import tempfile
from decimal import Decimal, ROUND_HALF_UP

def pr(*a):
    print(*a)

def fmt(x, d=1, pct=False):
    """Redondeo único mitad hacia arriba sobre el valor completo; formato del documento (miles '.', decimales ',')."""
    v = Decimal(repr(x * 100 if pct else x)).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)
    s = f"{abs(v):,.{d}f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return ("−" if v < 0 else "") + s

def h(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)

# ---------------------------------------------------------------------------------------------
# 0. Modelo de Fase 3 v2 (importado en copia temporal) y datos de fases anteriores (DATO)
# ---------------------------------------------------------------------------------------------
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_tmp = tempfile.mkdtemp(prefix="fase4v21_")
for _d in ("data", "scripts"):
    shutil.copytree(os.path.join(BASE, _d), os.path.join(_tmp, _d))
_spec = importlib.util.spec_from_file_location("f3", os.path.join(_tmp, "scripts", "fase3_dcf.py"))
f3 = importlib.util.module_from_spec(_spec)
with contextlib.redirect_stdout(io.StringIO()):
    _spec.loader.exec_module(f3)          # ejecuta fase3 en la copia temporal (su Excel se escribe allí)
shutil.rmtree(_tmp, ignore_errors=True)

# v4 (M-v3-1): las cifras de 02 y 03 ya no se copian a mano; se leen de data/ratios.csv (vía f3.r, que lo carga del
# modelo importado) o del propio modelo de Fase 3. Los asserts comprueban que coinciden con los valores de v3.
PRICE = f3.PRICE                    # 03 §1 (M1): 372,22
SH_COVER = 3952.757946              # 10-Q 3T26 portada (P2/M3); se comprueba contra 03 abajo
SH_DIL_3T = 3541.0                  # P2
SH_BAS_3T = 3240.0                  # P2
CEO_AWARD_SH = f3.r("acc_restringidas_ceo2025")   # 02 §5.1 (Form 4 jun-2026: 423.743.904 restringidas del plan CEO 2025)
EX2018_NET_SH = 286.43              # Form 4 16-jun-2026: 303,96 ejercidas - 17,53 retenidas (02 §5.1 lo da a 1 decimal)
assert fmt(EX2018_NET_SH, 1) == fmt(f3.r("acc_netas_ejercicio_2018"), 1), "ejercicio 2018 neto distinto de 02 §5.1"
SH_FD = f3.SH_FD                    # 03 v2 / 02 §5.1: totalmente diluidas aprox. (portada + ~15 M de empleados)
assert abs(SH_COVER - f3.SH) < 1e-6, "acciones de portada distintas de las de 03"
MCAP = PRICE * SH_COVER
NETCASH = f3.r("caja_neta")                       # 02 §5 (ratios.csv)
REV_TTM = f3.r("ingresos_totales")                # 02 §2
EBIT_TTM = f3.r("beneficio_operativo")            # 02 §3
CRED_TTM = f3.r("creditos_regulatorios")          # 02 §2
NI_TTM = f3.r("beneficio_neto_atrib_comunes")     # 02 §3 (atribuible a comunes)
SBC_TTM = f3.r("sbc")                             # 02 §4
SBC_FY24 = f3.r("sbc", "FY2024")                  # 02 §4 (ratios.csv, FY2024)
FCF_TTM = f3.r("fcf")                             # 02 §4
_v3 = {"PRICE": (PRICE, 372.22), "CEO": (CEO_AWARD_SH, 423.7), "NETCASH": (NETCASH, 35924.0), "REV": (REV_TTM, 103570.0),
       "EBIT": (EBIT_TTM, 3466.0), "CRED": (CRED_TTM, 1181.0), "NI": (NI_TTM, 3218.0), "SBC": (SBC_TTM, 4300.0), "FCF": (FCF_TTM, 3303.0), "SBC24": (SBC_FY24, 1999.0)}
for _k, (_a, _b) in _v3.items():
    assert abs(_a - _b) < 1e-9, f"{_k}: {_a} distinto del valor de v3 {_b}"

# ROIC A TTM a precisión completa (M-v3-1; v3: ROIC_A_TTM = 0.055 copiado a mano de 02 §6 a un decimal).
# Misma fórmula que fase2_ratios.py: NOPAT (beneficio operativo x (1 - 0,21)) / capital invertido A medio
# (saldo 30-sep-2026 de ratios.csv y saldo 30-sep-2025 de tesla_financials.csv). ratios.csv guarda el ratio a 4 decimales.
_s2 = importlib.util.spec_from_file_location("f2", os.path.join(BASE, "scripts", "fase2_ratios.py"))
f2 = importlib.util.module_from_spec(_s2)
_s2.loader.exec_module(f2)          # solo define funciones y constantes (main() va bajo __main__); no escribe nada
_raw = f2.load()
_ic_open = (_raw["patrimonio_neto_accionistas"]["9M2025"] + _raw["deuda_corriente"]["9M2025"]
            + _raw["deuda_no_corriente"]["9M2025"] - _raw["caja_y_inversiones_cp"]["9M2025"])
_ic_close = f3.r("capital_invertido_A_neto_caja")
ROIC_A_TTM = EBIT_TTM * (1 - f2.TAX_NORM) / ((_ic_close + _ic_open) / 2)   # 02 §6
assert round(ROIC_A_TTM, 4) == f3.r("roic_A_neto_caja"), "ROIC A TTM distinto de ratios.csv"
WACC0 = f3.WACC0                    # 03 v3 §1.1 (11,55 %; v2: 0,1160 copiado a mano)
WACC_T = f3.WACC_T                  # 03 v3 §1.1 (9,79 %)

EQ_DCF_V1 = {"bajista": 40940.0, "base": 96964.0, "alcista": 216931.0}   # 03 v1 §3 (solo para el registro de cambios)
EQ_DCF = {k: f3.RES[k]["eq"] for k in ("bajista", "base", "alcista")}       # 03 v3 §3, desde el modelo importado
VPS_DCF = {k: v / SH_COVER for k, v in EQ_DCF.items()}
VPS_FD = {k: v / SH_FD for k, v in EQ_DCF.items()}

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
REV_ENERGY_FY25 = f3.r("ingresos_energia", "FY2025")   # 02 (ratios.csv, FY2025); v4: antes 12771.0 a mano
assert REV_ENERGY_FY25 == 12771.0

# Comparables robotaxi
WAYMO_RIDES_WEEK = 500_000          # abr-2026, Alphabet 1T26 vía T4 (solo secundaria)
WAYMO_RIDES_WEEK_FEB = 400_000      # feb-2026, T3
UBER_TRIPS_FY25 = 13_567.0          # M viajes, T5
UBER_GB_FY25 = 193_454.0            # M$, T5 (incluye Delivery)

h("1. Recuento de acciones y PER (W1, W2 — v2.1: W2 reformulado con 02 §5.1)")
pr(f"Capitalización (precio x acciones portada): {MCAP:,.0f} M$")
gap_cover_basic = SH_COVER - SH_BAS_3T
SH_OUT_SEP25 = 3324.0   # 10-Q 3T25, balance (T6)
SH_OUT_DEC25 = 3751.0   # 10-Q 3T26 (P2), balance
SH_OUT_SEP26 = 3953.0   # 10-Q 3T26 (P2), balance
ISSUED_9M26 = 202.0     # P2, estado de patrimonio: "Issuance of common stock for equity incentive awards and acquisitions"
pr(f"Acciones en balance: 30-sep-25 {SH_OUT_SEP25:,.0f} -> 31-dic-25 {SH_OUT_DEC25:,.0f} (+{SH_OUT_DEC25 - SH_OUT_SEP25:,.0f}) -> 30-sep-26 {SH_OUT_SEP26:,.0f} (+{SH_OUT_SEP26 - SH_OUT_DEC25:,.0f}; emitidas 9M26 según P2: {ISSUED_9M26:.0f})")
pr(f"Aumento total en 12 meses: {SH_OUT_SEP26 - SH_OUT_SEP25:,.0f} M ({SH_OUT_SEP26 / SH_OUT_SEP25 - 1:+.1%}) frente a media básica +{SH_BAS_3T - 3227:,.0f} M")
# 02 §5.1 (v2): descomposición con nota de BPA, estados de patrimonio y Form 4
resid = gap_cover_basic - CEO_AWARD_SH - EX2018_NET_SH
pr(f"Portada - media básica 3T26 = {gap_cover_basic:,.1f} M = plan CEO 2025 {CEO_AWARD_SH} + ejercicio 2018 neto {EX2018_NET_SH} + residuo {resid:,.1f} (02 §5.1)")
emp = (SH_DIL_3T - SH_BAS_3T) - EX2018_NET_SH
pr(f"Diluida - básica 3T26 = {SH_DIL_3T - SH_BAS_3T:.0f} M ('Stock-based awards', P2) ≈ ejercicio 2018 neto {EX2018_NET_SH:.0f} + empleados ~{emp:.0f} M "
   "(INFERENCIA de 02 §5.1: el 10-Q no desglosa la línea)")
pr("Plan CEO 2025 (423,7 M): en la portada SÍ; en la básica NO; en la diluida NO (no 'ganadas', nota de BPA P2).")
sh_v1_line = SH_COVER + SH_DIL_3T - SH_BAS_3T
pr(f"W2: la línea de 03 v1 (portada + 301 = {sh_v1_line:,.1f} M) contaba DOS VECES ~{EX2018_NET_SH:.0f} M (ya en la portada) "
   f"-> sobrestimaba las acciones un {sh_v1_line / SH_FD - 1:+.1%} frente a las totalmente diluidas")
pr(f"    03 v2 usa totalmente diluidas = {SH_FD:,.1f} M (portada + {SH_FD - SH_COVER:,.1f}); contraste diluida 3T + CEO 2025 = {SH_DIL_3T + CEO_AWARD_SH:,.1f} M")
SH_EX_AWARD = SH_COVER - CEO_AWARD_SH
pr(f"    Denominador de los VPA 'corregidos' de 04 v1 (portada - plan CEO = {SH_EX_AWARD:,.1f} M): {SH_EX_AWARD / SH_FD - 1:+.1%} frente a las "
   f"totalmente diluidas (02 §5.1: ~-10 % medido sobre la media diluida {SH_DIL_3T:,.0f}: {SH_DIL_3T / SH_FD - 1:+.1%}) -> INFRACONTABAN acciones")
pr("VPA por escenario con el modelo de 03 (v3):")
for k in EQ_DCF:
    pr(f"  VPA {k:8s}: portada {VPS_DCF[k]:6.2f} $ | totalmente diluidas {VPS_FD[k]:6.2f} $ "
       f"| [03 v1: portada {EQ_DCF_V1[k] / SH_COVER:6.2f} $ ; portada + 301 {EQ_DCF_V1[k] / sh_v1_line:6.2f} $ ; "
       f"04 v1 RETIRADO {EQ_DCF_V1[k] / SH_EX_AWARD:6.2f} $]")
pe_dil = PRICE / (NI_TTM / SH_DIL_3T)
pe_mcap = MCAP / NI_TTM
pr(f"PER convención estándar (precio / BPA diluido TTM aprox.): {pe_dil:,.0f}x  <- el de 03; coincide con GuruFocus 410,4x (05 §3.3)")
pr(f"Métrica alternativa (capitalización con acciones de portada / BN TTM): {pe_mcap:,.0f}x  <- no es una corrección (W1 retirada)")

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
pr(f"Lectura: el punto de partida del DCF ({f3.M_EX0:.2%}, 03 v3) incluye costes ligados a la opcionalidad cuyos ingresos el modelo pone a 0.")

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
pr(f"Plan CEO: sus {CEO_AWARD_SH} M ya están en la portada (02 §5.1) -> no hay dilución adicional sobre estos valores. "
   f"Con acciones totalmente diluidas ({SH_FD:,.1f} M) todos los valores con opcionalidad bajan un {SH_COVER / SH_FD - 1:.1%}")
for k, v in VPS_DCF.items():
    pr(f"Caída hasta el VPA DCF {k}: {v / PRICE - 1:+.0%}")
half = base_core + 0.5 * (PRICE - base_core)
pr(f"Precio si el mercado recortara a la mitad el valor implícito de la opcionalidad (base): {half:,.0f} $ ({half / PRICE - 1:+.0%})")

h("11. Otros controles sobre 03-valoracion.md")
toyota_rev_03 = 418590 / 1.45
pr(f"'Ingresos Toyota' de 03 = EV / (EV/Ventas) = {toyota_rev_03:,.0f} M$ = ventas (el EV se cancela: la deuda de la financiera no afecta a esta cifra).")
pr("  03 §5 ya la presenta como 'implícita en su EV/Ventas' -> W5 v1 RETIRADA (05 §3.3).")
pr(f"Capex 2026: el texto de 03 cita '>20.000-25.000 M$'; el CFO lo revisó a ~20.000 M$ en la call 3T26 (T1). 9M26 = 13.014 -> 4T26 implícito ~{20000 - 13014:,.0f} M$")
pr("  El MODELO de 03 no usa esa cifra (usa reinversión = % de ingresos): ver §13 para el capex implícito.")
pr(f"ROIC A TTM {ROIC_A_TTM:.1%} vs WACC inicial {WACC0:.1%}: diferencial {ROIC_A_TTM - WACC0:+.1%}")
pr(f"FCF - SBC TTM: {FCF_TTM - SBC_TTM:,.0f} M$")

h("12. Umbral de la señal A1")
q_growth = (50 / RT_MILES_CUM) ** (1 / 5)
pr(f"De {RT_MILES_CUM} M a 50 M millas acumuladas en 5 trimestres (3T26->4T27): crecimiento trimestral necesario {q_growth:.2f}x")

h("13. Controles medidos con el modelo de Fase 3 (W3 / §4.1.2, W9 / §4.1.3, asimetría §4.1.1) — v3, modelo de 03 v3")
b0 = f3.run_dcf(f3.SCEN["base"])
pr(f"Reproducción del caso base de 03 v3: VPA {b0['vps']:.2f} $ (03 v3: 24,65) | WACC0 {f3.WACC0:.2%} | WACC_T {f3.WACC_T:.2%}")
assert abs(b0["vps"] - VPS_DCF["base"]) < 1e-9

# W3 / §4.1.2: capex implícito del año 1
y1 = b0["rows"][0]
capex_y1 = y1["reinv"] + f3.DA_TTM_APROX
pr(f"W3: año 1 base -> reinversión neta {y1['reinv']:,.0f} + D&A TTM (02 v2) {f3.DA_TTM_APROX:,.0f} = capex bruto implícito {capex_y1:,.0f} M$ "
   f"(FCFF año 1 {y1['fcff']:,.0f})")
pr(f"    Guía revisada ~20.000 M$ (T1): el modelo queda {20000 - capex_y1:,.0f} M$ POR DEBAJO -> no es pesimista en capex; si acaso, ligero")
pr("    (y no incluye la Terafab: 'tens of billions' hasta 2028 [MUSK, T1]). W3 / §4.1.2 v1 RETIRADA.")

# W9 / §4.1.3: beta solo sectorial en los años 1-5 (WACC terminal sin cambios)
ke_sec = f3.RF + f3.BETA_BU * f3.ERP
w0_sec = ke_sec * (1 - f3.W_D) + f3.KD * f3.W_D
v_sec = f3.run_dcf(f3.SCEN["base"], w0=w0_sec, wt=f3.WACC_T)["vps"]
v_sec_shift = f3.run_dcf(f3.SCEN["base"], w0=w0_sec, wt=f3.WACC_T + (w0_sec - f3.WACC0))["vps"]
pr(f"W9: beta sectorial {f3.BETA_BU:.2f} -> WACC0 {w0_sec:.2%} (03: {f3.WACC0:.2%})")
pr(f"    VPA base con WACC terminal sin cambios: {v_sec:.2f} $ ({v_sec - b0['vps']:+.2f} $)")
pr(f"    VPA base desplazando también el WACC terminal (como la tabla 4.1 de 03): {v_sec_shift:.2f} $ ({v_sec_shift - b0['vps']:+.2f} $)")
_ig = f3.G_GRID.index(0.03)
_v116, _v106 = f3.SENS[f3.W_GRID.index(round(f3.WACC0, 4))][_ig], f3.SENS[f3.W_GRID.index(round(f3.WACC0 - 0.01, 4))][_ig]
pr(f"    Interpolación lineal de la tabla 4.1 de 03 v3 (método de 05 §3.3): {_v116 + (_v106 - _v116) * (f3.WACC0 - w0_sec) / 0.01:.1f} $")
pr(f"    Contraste con 03 v3 §4.3: {f3.W9_15:.2f} $ / {f3.W9_SHIFT:.2f} $")

# §4.1.1: sensibilidad del margen de partida (no es corrección: la SBC es un coste real)
m0_03 = f3.M_EX0
# v2.1: denominador = ingresos SIN créditos (f3.REV0_EX), el mismo al que 03 v2 aplica el margen (antes f3.REV0)
m0_adj_sbc = m0_03 + d_sbc / f3.REV0_EX
m0_adj_rd = m0_03 + 4 * d_rd / f3.REV0_EX
for lab, m0 in (("+ exceso de SBC sobre FY24", m0_adj_sbc), ("+ I+D incremental 3T26 x 4", m0_adj_rd)):
    f3.M_EX0 = m0
    v = f3.run_dcf(f3.SCEN["base"])["vps"]
    v2 = f3.run_dcf(f3.SCEN["base"], w0=w0_sec, wt=f3.WACC_T)["vps"]
    pr(f"§4.1.1 sensibilidad: margen de partida {m0_03:.2%} -> {m0:.2%} ({lab}): VPA base {v:.2f} $ ({v - b0['vps']:+.2f}) ; "
       f"junto con beta sectorial {v2:.2f} $ ({v2 - b0['vps']:+.2f})")
f3.M_EX0 = m0_03
pr(f"    Contraste con 03 v3 §6.3 (script §9 c): " + " | ".join(f"{v:.2f} $" for _, _, _, v in f3.ASYM_RES[1:3]))
SPACEX_FV = 2002.0 + 863.0   # P2: compra + plusvalía no realizada 9M26 (inferencia del valor contable)
DIGITAL = 962.0              # P2
pr(f"W8: SpaceX (~{SPACEX_FV:,.0f}) + activos digitales ({DIGITAL:,.0f}) fuera de la caja neta = {(SPACEX_FV + DIGITAL) / SH_COVER:.2f} $/acción")
# Suma de los ajustes hacia arriba de §4.1 que se pueden medir (beta sectorial + margen de partida sin I+D incremental + W8)
f3.M_EX0 = m0_adj_rd
up_lo = f3.run_dcf(f3.SCEN["base"], w0=w0_sec, wt=f3.WACC_T)["vps"] + (SPACEX_FV + DIGITAL) / SH_COVER
up_hi = f3.run_dcf(f3.SCEN["base"], w0=w0_sec, wt=f3.WACC_T + (w0_sec - f3.WACC0))["vps"] + (SPACEX_FV + DIGITAL) / SH_COVER
f3.M_EX0 = m0_03
pr(f"Ajuste máximo medido hacia arriba (§4.1: beta sectorial + margen de partida sin I+D incremental + W8): VPA base {up_lo:.2f} - {up_hi:.2f} $ "
   f"({up_lo - b0["vps"]:+.2f} a {up_hi - b0["vps"]:+.2f} $) ; el capex (W3) ya no suma")

h("14. Cifras que cita 04-tesis.md (v3): redondeo ÚNICO mitad hacia arriba sobre el valor completo, formato del documento")
pr("Copiar al documento SOLO desde esta sección (miles con '.', decimales con ','). Nunca re-redondear una cifra de arriba.")
SENS_EBIT = {(mult, yr): GAP["base"] * (1 + WACC_T) ** yr / mult / 0.79 for mult, yr in ((40, 10), (30, 7), (40, 7))}
cifras = [
    ("WACC inicial (03) / terminal", f"{fmt(WACC0, 2, True)} % / {fmt(WACC_T, 2, True)} %"),
    ("ROIC A TTM - WACC inicial (pp)", f"{fmt(ROIC_A_TTM - WACC0, 1, True)} pp"),
    ("Beta de regresión / inicial / sectorial (03)", f"{fmt(f3.BETA_REG, 2)} / {fmt(f3.BETA0, 2)} / {fmt(f3.BETA_BU, 2)}"),
    ("VPA DCF portada bajista / base / alcista (2 dec.)", " / ".join(fmt(VPS_DCF[k], 2) for k in EQ_DCF) + " $"),
    ("VPA DCF portada (1 dec.)", " / ".join(fmt(VPS_DCF[k], 1) for k in EQ_DCF) + " $"),
    ("VPA DCF totalmente diluidas (2 dec.)", " / ".join(fmt(VPS_FD[k], 2) for k in EQ_DCF) + " $"),
    ("VPA DCF totalmente diluidas (1 dec.)", " / ".join(fmt(VPS_FD[k], 1) for k in EQ_DCF) + " $"),
    ("Negocio reportado (0 dec.)", f"{fmt(VPS_DCF['bajista'], 0)}-{fmt(VPS_DCF['alcista'], 0)} $"),
    ("Opcionalidad / precio (base)", f"{fmt(GAP['base'] / MCAP, 1, True)} % ; {fmt(GAP['base'] / 1e6, 2)} billones $"),
    ("Opcionalidad por acción alcista-bajista", f"{fmt(GAP['alcista'] / SH_COVER, 1)}-{fmt(GAP['bajista'] / SH_COVER, 1)} $"),
    ("EBIT_10 necesario: rango", f"{fmt(EBIT_REQ_LO, 0)}-{fmt(EBIT_REQ_HI, 0)} M$ ({fmt(EBIT_REQ_LO / EBIT_TTM, 0)}x-{fmt(EBIT_REQ_HI / EBIT_TTM, 0)}x EBIT TTM)"),
    ("EBIT_10 necesario: central", f"{fmt(EBIT_REQ_MID, 0)} M$ ({fmt(EBIT_REQ_MID / EBIT_TTM, 0)}x EBIT TTM)"),
    ("Sensibilidad 40x año 10 / 30x año 7 / 40x año 7", " / ".join(fmt(v, 0) for v in SENS_EBIT.values()) + " M$"),
]
for n, e in COMBO_EBIT.items():
    pv_lo, pv_hi = PV_SUCCESS[(n, WACC0)], PV_SUCCESS[(n, WACC_T)]
    cifras.append((f"Combinación {n}: EBIT ; % central ; VP ; $/acc ; prob. implícita",
                   f"{fmt(e, 0)} M$ ; {fmt(e / EBIT_REQ_MID, 0, True)} % ; {fmt(pv_lo, 0)}-{fmt(pv_hi, 0)} M$ ; "
                   f"{fmt(pv_lo / SH_COVER, 0)}-{fmt(pv_hi / SH_COVER, 0)} $ ; {fmt(GAP['base'] / pv_hi, 1, True)}-{fmt(GAP['base'] / pv_lo, 1, True)} %"))
for n in COMBOS:
    for P in (0.25, 0.50):
        lo = base_core + P * PV_SUCCESS[(n, WACC0)] / SH_COVER
        hi = base_core + P * PV_SUCCESS[(n, WACC_T)] / SH_COVER
        cifras.append((f"Base + {P:.0%} x {n}", f"{fmt(lo, 0)}-{fmt(hi, 0)} $ (frente al precio: {fmt(hi / PRICE - 1, 0, True)} % a {fmt(lo / PRICE - 1, 0, True)} %)"))
    lo = VPS_DCF["alcista"] + PV_SUCCESS[(n, WACC0)] / SH_COVER
    hi = VPS_DCF["alcista"] + PV_SUCCESS[(n, WACC_T)] / SH_COVER
    cifras.append((f"Alcista + {n} al 100 %", f"{fmt(lo, 0)}-{fmt(hi, 0)} $"))
cifras += [
    ("Recorte a la mitad de la opcionalidad", f"{fmt(half, 1)} $ ({fmt(half / PRICE - 1, 0, True)} %)"),
    ("Caída hasta el VPA DCF bajista / base / alcista", " / ".join(fmt(VPS_DCF[k] / PRICE - 1, 0, True) + " %" for k in EQ_DCF)),
    ("Base - bajista (lado optimista del saldo)", f"−{fmt(VPS_DCF['base'] - VPS_DCF['bajista'], 0)} $"),
    ("Efecto neto en el caso base frente a 03 v1 (24,53 $)", f"{fmt(VPS_DCF['base'] - EQ_DCF_V1['base'] / SH_COVER, 2)} $ "
     f"({fmt(EQ_DCF_V1['base'] / SH_COVER, 2)} → {fmt(VPS_DCF['base'], 2)} $)"),
    ("W9 beta sectorial, WACC años 1-5", f"{fmt(v_sec, 1)} $ (+{fmt(v_sec - b0['vps'], 1)} $) ; 2 dec.: {fmt(v_sec, 2)} $"),
    ("W9 con WACC terminal desplazado", f"{fmt(v_sec_shift, 1)} $ (+{fmt(v_sec_shift - b0['vps'], 1)} $) ; 2 dec.: {fmt(v_sec_shift, 2)} $ ; "
     f"WACC_T {fmt(WACC_T + (w0_sec - f3.WACC0), 2, True)} %"),
    ("W9 interpolación de la tabla 4.1 de 03", f"{fmt(_v116 + (_v106 - _v116) * (f3.WACC0 - w0_sec) / 0.01, 1)} $"),
    ("§4.1.1 margen sin SBC extra / sin I+D incr.", f"{fmt(m0_adj_sbc, 2, True)} % / {fmt(m0_adj_rd, 2, True)} %"),
    ("§4.1.1 VPA sin SBC extra / sin I+D incr. (2 dec.)", f"{fmt(f3.ASYM_RES[1][3], 2)} / {fmt(f3.ASYM_RES[2][3], 2)} $"),
    ("§4.1.1 VPA sin SBC extra / sin I+D incr. (1 dec.)", f"{fmt(f3.ASYM_RES[1][3], 1)} / {fmt(f3.ASYM_RES[2][3], 1)} $"),
    ("Ajuste máximo hacia arriba", f"{fmt(up_lo, 1)}-{fmt(up_hi, 1)} $ (+{fmt(up_lo - b0['vps'], 1)} a +{fmt(up_hi - b0['vps'], 1)} $) ; 2 dec.: "
     f"{fmt(up_lo, 2)}-{fmt(up_hi, 2)} $"),
    ("Capex bruto implícito año 1 (reinv. + D&A) / bajo la guía", f"{fmt(capex_y1, 0)} M$ ({fmt(y1['reinv'], 0)} + {fmt(f3.DA_TTM_APROX, 0)}) / {fmt(20000 - capex_y1, 0)} M$"),
    ("SpaceX + activos digitales por acción", f"{fmt((SPACEX_FV + DIGITAL) / SH_COVER, 2)} $"),
    ("Valores con acciones totalmente diluidas: caída", f"{fmt(SH_COVER / SH_FD - 1, 1, True)} %"),
]
for k, v in cifras:
    pr(f"  {k:62s}: {v}")
