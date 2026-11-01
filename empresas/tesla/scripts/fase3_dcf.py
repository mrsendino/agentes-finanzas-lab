#!/usr/bin/env python3
"""Fase 3 - Tesla (TSLA): valoración por DCF (FCFF), escenarios, sensibilidad, DCF inverso y múltiplos.

Toda la aritmética se hace aquí. Punto de partida: cifras de Fase 2 (data/ratios.csv, TTM a 3T-2026 y FY2025).
Salida: data/dcf.xlsx (hojas Supuestos, Escenarios, Sensibilidad, DCF_inverso, Multiplos) y resumen por pantalla.

Convenciones del modelo
- Año 0 = TTM a 30-sep-2026 (Fase 2). Años 1..10 = periodos de 12 meses a partir de oct-2026.
  Descuento a final de año (convención conservadora frente a mitad de año; la diferencia es ~WACC/2).
- FCFF = EBIT x (1 - t) - reinversión neta.
  * EBIT es GAAP: ya descuenta la compensación en acciones (SBC). NO se suma de vuelta -> la SBC
    se trata como coste real (equivale a pagar en caja a los empleados).
  * Reinversión neta = capex - amortización + variación de circulante, modelada como
    max(% de ingresos [años 1-2, ola de capex], aumento de ingresos / ratio ventas-capital).
- Créditos regulatorios: margen ~100 % (supuesto de Fase 2); desaparecen en 3 años (ley OBBBA, Fase 1 §4).
- Valor terminal: FCFF_11 = NOPAT_11 x (1 - g / ROIC_terminal); TV = FCFF_11 / (WACC_terminal - g).
- WACC: años 1-5 = WACC inicial; años 6-10 convergen linealmente a un WACC de empresa madura.
- Valor de las acciones = valor de la empresa + caja neta (Fase 2, 30-sep-2026).

v2 (2026-10-25): ronda de correcciones tras 05-veredicto.md §5 (prioridad 2) y los datos nuevos de 02 v2:
- D&A TTM real de Fase 2 (6.704 M$) en lugar de 3T26 x 4 (7.408). El alias DA_TTM_APROX se mantiene porque
  scripts/fase4_opcionalidad.py lo importa; ahora vale 6.704.
- Anclas de margen calculadas sobre ingresos SIN créditos, el mismo denominador al que el modelo las aplica.
  Sin redondeo intermedio (v1 redondeaba el objetivo base a 3 decimales: 8,9 %, no 8,93 %).
- Línea de dilución: totalmente diluidas ~3.967 M (02 §5.1, fila acc_totalmente_diluidas_aprox) en lugar de
  portada + 301 M (doble cómputo de ~286 M).
- Energía: base 12 % -> 8 % y bajista 5 % -> 0 % (despliegues frente a ingreso por GWh; ver §9 del script).
- Bloques nuevos de control (§9): ROIC terminal, beta (W9), asimetría costes/ingresos de la opcionalidad,
  capex bruto implícito frente a la guía, mecanismo del margen base, energía, SpaceX y DCF inverso con
  ventas/capital de tipo software.

v3 (2026-10-25): ronda tras 05-veredicto-v2.md §8, prioridad 2:
- Beta de regresión: 1,84 y 1,84 (TipRanks y MarketChameleon re-consultadas el 25-oct-2026) en lugar de 1,85 y 1,87
  (FAIL-v2-1). Es el único cambio de modelo; se recalcula todo.
- §10 nueva: data/cifras_03_redondeo.csv con cada cifra del documento redondeada mitad hacia arriba (Decimal) desde el
  valor completo, al número de decimales con que se escribe en 03. El documento copia de ahí (M1/M2: doble redondeo).
"""
import csv
from decimal import Decimal, ROUND_HALF_UP
import os
import shutil
import statistics
import subprocess
import tempfile

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATIOS = os.path.join(BASE, "data", "ratios.csv")
OUT_XLSX = os.path.join(BASE, "data", "dcf.xlsx")

# ---------------------------------------------------------------------------
# 1. Datos de Fase 2
# ---------------------------------------------------------------------------
R = {}
with open(RATIOS, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        R[row["metrica"]] = row


def r(metric, period="TTM_Q3_2026"):
    v = R[metric][period]
    return float(v) if v not in ("", None) else None


REV0 = r("ingresos_totales")
AUTO0 = r("ingresos_automocion_total")
CRED0 = r("creditos_regulatorios")
AUTO_EX0 = AUTO0 - CRED0
ENER0 = r("ingresos_energia")
SERV0 = r("ingresos_servicios_otros")
EBIT0 = r("beneficio_operativo")
NI0 = r("beneficio_neto_atrib_comunes")
CAPEX0 = r("capex")
SBC0 = r("sbc")
CASH0 = r("caja_y_inversiones_cp")
DEBT0 = r("deuda_total")
NETCASH0 = r("caja_neta")
IC_A0 = r("capital_invertido_A_neto_caja")
IC_B0 = r("capital_invertido_B_bruto")
assert abs(AUTO_EX0 + CRED0 + ENER0 + SERV0 - REV0) < 1, "segmentos no cuadran"


def m_ex(period):
    """v2: margen operativo sin créditos sobre ingresos SIN créditos = (EBIT - créditos) / (ingresos - créditos).
    Es el mismo denominador al que run_dcf aplica el margen: EBIT = m x (ingresos - créditos) + créditos."""
    cr = r("creditos_regulatorios", period)
    return (r("beneficio_operativo", period) - cr) / (r("ingresos_totales", period) - cr)


M_EX0 = m_ex("TTM_Q3_2026")
M_EX0_V1 = r("margen_operativo_sin_creditos")  # v1: sobre ingresos totales (solo informativo)

# márgenes operativos sin créditos históricos (anclas de los escenarios), mismo denominador que el modelo
YEARS = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]
M_EX_HIST = {y: m_ex(y) for y in YEARS}
M_EX_AVG_21_24 = statistics.mean([M_EX_HIST[y] for y in ["FY2021", "FY2022", "FY2023", "FY2024"]])
M_EX_AVG_24_25 = statistics.mean([M_EX_HIST[y] for y in ["FY2024", "FY2025"]])
M_EX_MAX = max(M_EX_HIST.values())
# anclas v1 (sobre ingresos totales y redondeadas a 3 decimales, como en v1), solo para el registro de cambios
M_EX_HIST_V1 = {y: r("margen_operativo_sin_creditos", y) for y in YEARS}
ANCLAS_V1 = (round(statistics.mean([M_EX_HIST_V1[y] for y in ["FY2024", "FY2025"]]), 3),
             round(statistics.mean([M_EX_HIST_V1[y] for y in ["FY2021", "FY2022", "FY2023", "FY2024"]]), 3),
             round(max(M_EX_HIST_V1.values()), 3))

# Amortización (D&A) TTM: v2, dato de Fase 2 (fila dya_amortizacion_deterioro; P4, reconciliación EBITDA TTM).
DA_TTM = r("dya_amortizacion_deterioro")
DA_TTM_APROX = DA_TTM          # alias por compatibilidad con fase4_opcionalidad.py (v1 = 3T26 x 4)
DA_TTM_V1 = 1852.0 * 4         # v1: D&A 3T26 (P4) x 4 = 7.408, solo informativo
NET_CAPEX0 = CAPEX0 - DA_TTM
NET_CAPEX0_PCT = NET_CAPEX0 / REV0
SALES_TO_CAP_A = REV0 / IC_A0
SALES_TO_CAP_B = REV0 / IC_B0

# ---------------------------------------------------------------------------
# 2. Datos de mercado (fuente + fecha)
# ---------------------------------------------------------------------------
MKT = {
    "precio": (372.22, "USD", "Cierre 23-oct-2026. Benzinga (benzinga.com/quote/TSLA, 'Close' 372,22, -0,63 %) y MarketChameleon (marketchameleon.com/Overview/TSLA/Summary); GuruFocus 23-oct-2026 confirma 372,22"),
    "acciones_cover": (3952.757946, "M acciones", "10-Q 3T-2026 (P2, acc. 0001628280-26-066775), portada: 3.952.757.946 acciones en circulación a 15-oct-2026"),
    "acciones_diluidas_3T": (3541.0, "M acciones", "10-Q 3T-2026 (P2), cuenta de resultados: media ponderada diluida 3T-2026"),
    "acciones_basicas_3T": (3240.0, "M acciones", "10-Q 3T-2026 (P2), cuenta de resultados: media ponderada básica 3T-2026"),
    "rf": (0.0497, "%", "Bono EE. UU. 10 años 4,967 % (23-oct-2026, ~15:53 ET); cierre 22-oct 4,954 %. mortgagenewsdaily.com/treasury/10yr"),
    "erp": (0.0420, "%", "Damodaran, ERP implícito S&P 500 a 1-oct-2026 = 4,20 % (trailing 12m, payout ajustado). pages.stern.nyu.edu/~adamodar (home page)"),
    # v3 (FAIL-v2-1 de 05-veredicto-v2 §4.2): ambas re-consultadas el 25-oct-2026. v2 usaba 1,85 (TipRanks) y 1,87
    # (MarketChameleon); ninguna de las dos páginas muestra ya esos valores.
    "beta_reg_1": (1.84, "x", "TipRanks, estadísticas TSLA ('Beta 1.84'; dateModified de la página 24-oct-2026; consultado 25-oct-2026). Beta de regresión; ventana no indicada. v2: 1,85"),
    "beta_reg_2": (1.84, "x", "MarketChameleon, resumen TSLA ('TSLA has a beta of 1.84'; 'Data as of October 23, 2026'; consultado 25-oct-2026). Beta de regresión; ventana no indicada. v2: 1,87"),
    "beta_u_auto": (1.31, "x", "Damodaran, betas por sector EE. UU. (ene-2026): Auto & Truck, beta desapalancada corregida por caja 1,31 (33 empresas)"),
    "beta_u_mercado": (1.00, "x", "Por definición, beta media del mercado = 1"),
    "spread_deuda": (0.010, "%", "SUPUESTO (SIN VERIFICAR): diferencial de 100 pb sobre rf, coherente con rating grado de inversión bajo; no se ha consultado el rating vigente"),
    "tipo_imp": (0.21, "%", "Tipo federal EE. UU. normativo, mismo criterio que Fase 2 (§6)"),
    "mcap_terceros": (1.47e6, "M USD", "Capitalización publicada: 1,47 bill. $ (GuruFocus / Benzinga, 23-oct-2026) - solo contraste"),
}
PRICE = MKT["precio"][0]
SH = MKT["acciones_cover"][0]
# v2: acciones totalmente diluidas aprox. (02 §5.1). Portada (que ya incluye las 423,7 M restringidas del CEO 2025 y
# las ~286 M netas del ejercicio de 2018) + ~15 M de incentivos de empleados aún no emitidos. La división 286 / 15
# de las 301 M es una INFERENCIA de Fase 2 (el 10-Q no la desglosa).
SH_FD = r("acc_totalmente_diluidas_aprox")
SH_FD_CHECK = MKT["acciones_diluidas_3T"][0] + r("acc_restringidas_ceo2025")  # contraste: diluida 3T + CEO 2025
assert abs(SH_FD - SH_FD_CHECK) < 5, "acciones totalmente diluidas no cuadran con diluida 3T + CEO 2025"
SH_DIL_V1 = SH + (MKT["acciones_diluidas_3T"][0] - MKT["acciones_basicas_3T"][0])  # v1 (doble cómputo), informativo
RF, ERP, TAX = MKT["rf"][0], MKT["erp"][0], MKT["tipo_imp"][0]

MCAP = PRICE * SH
EV_MKT = MCAP - NETCASH0
D_E = DEBT0 / MCAP
BETA_REG = (MKT["beta_reg_1"][0] + MKT["beta_reg_2"][0]) / 2
BETA_BU = MKT["beta_u_auto"][0] * (1 + (1 - TAX) * D_E)
BETA0 = (BETA_REG + BETA_BU) / 2  # mezcla declarada: 50 % regresión / 50 % sector
BETA_T = (MKT["beta_u_mercado"][0] + MKT["beta_u_auto"][0]) / 2  # empresa madura
KE0 = RF + BETA0 * ERP
KD = (RF + MKT["spread_deuda"][0]) * (1 - TAX)
W_D = DEBT0 / (DEBT0 + MCAP)
WACC0 = KE0 * (1 - W_D) + KD * W_D
KE_T = RF + BETA_T * ERP
WACC_T = KE_T * (1 - W_D) + KD * W_D

N = 10

# ---------------------------------------------------------------------------
# 3. Escenarios (supuestos explícitos)
# ---------------------------------------------------------------------------
SCEN = {
    "bajista": dict(
        g_auto=0.01, g_ener=0.00, g_serv=0.10,  # v2: energía 5 % -> 0 %
        m_obj=M_EX_AVG_24_25, anio_m=5,
        reinv_pct=NET_CAPEX0_PCT, stc=1.2, g_term=0.025, roic_term=None,  # None -> ROIC = WACC_T (sin creación de valor)
        cred=[CRED0 * 0.4, CRED0 * 0.1, 0.0],
        nota="Automoción estancada (ASP a la baja, BYD/chinos), Energía con compresión de margen, Servicios se modera. Margen operativo ~ media FY2024-25 sin créditos.",
    ),
    "base": dict(
        g_auto=0.04, g_ener=0.08, g_serv=0.15,  # v2: energía 12 % -> 8 %
        m_obj=M_EX_AVG_21_24, anio_m=5,
        reinv_pct=NET_CAPEX0_PCT, stc=1.5, g_term=0.03, roic_term=0.12,
        cred=[CRED0 * 0.4, CRED0 * 0.1, 0.0],
        nota="Recuperación moderada de volumen, Energía y Servicios siguen ganando peso. Margen operativo vuelve a la media FY2021-24 sin créditos.",
    ),
    "alcista": dict(
        g_auto=0.08, g_ener=0.20, g_serv=0.22,
        m_obj=M_EX_MAX, anio_m=5,
        reinv_pct=NET_CAPEX0_PCT, stc=2.0, g_term=0.035, roic_term=0.15,
        cred=[CRED0 * 0.4, CRED0 * 0.1, 0.0],
        nota="Vuelta a crecimiento de volumen, Energía retoma ritmo 2021-25, Servicios (incl. FSD) sigue al ritmo 9M26. Margen = máximo histórico sin créditos (FY2022). Sin robotaxi/Optimus explícitos.",
    ),
}


def wacc_path(w0, wt):
    """Años 1-5 = w0; años 6-10 convergen linealmente a wt."""
    return [w0 if t <= 5 else w0 + (wt - w0) * (t - 5) / 5 for t in range(1, N + 1)]


def growth_path(g5, gt):
    """Años 1-5 = g5; años 6-10 bajan linealmente hasta gt en el año 10."""
    return [g5 if t <= 5 else g5 + (gt - g5) * (t - 5) / 5 for t in range(1, N + 1)]


def margin_path(m0, m_obj, anio):
    return [m0 + (m_obj - m0) * min(t, anio) / anio for t in range(1, N + 1)]


def run_dcf(s, w0=WACC0, wt=WACC_T, g_term=None, shares=SH, m0=None):
    """m0 = margen de partida sin créditos; None -> M_EX0 global leído en tiempo de ejecución
    (fase4_opcionalidad.py modifica f3.M_EX0 para su sensibilidad)."""
    g_term = s["g_term"] if g_term is None else g_term
    ga = growth_path(s["g_auto"], g_term)
    ge = growth_path(s["g_ener"], g_term)
    gs = growth_path(s["g_serv"], g_term)
    mp = margin_path(M_EX0 if m0 is None else m0, s["m_obj"], s["anio_m"])
    wp = wacc_path(w0, wt)
    cred = (s["cred"] + [0.0] * N)[:N]
    auto, ener, serv = AUTO_EX0, ENER0, SERV0
    prev_rev = REV0
    df = 1.0
    rows = []
    pv_sum = 0.0
    for t in range(N):
        auto *= 1 + ga[t]
        ener *= 1 + ge[t]
        serv *= 1 + gs[t]
        rev = auto + ener + serv + cred[t]
        ebit = mp[t] * (rev - cred[t]) + cred[t]
        nopat = ebit * (1 - TAX)
        reinv_stc = (rev - prev_rev) / s["stc"]
        reinv = max(s["reinv_pct"] * rev, reinv_stc) if t < 2 else reinv_stc
        fcff = nopat - reinv
        df /= 1 + wp[t]
        pv = fcff * df
        pv_sum += pv
        rows.append(dict(t=t + 1, auto=auto, cred=cred[t], ener=ener, serv=serv, rev=rev, g_rev=rev / prev_rev - 1,
                         m=mp[t], ebit=ebit, nopat=nopat, reinv=reinv, fcff=fcff, wacc=wp[t], df=df, pv=pv))
        prev_rev = rev
    roic_t = s["roic_term"] if s["roic_term"] is not None else wt
    nopat11 = rows[-1]["nopat"] * (1 + g_term)
    fcff11 = nopat11 * (1 - g_term / roic_t)
    tv = fcff11 / (wt - g_term)
    pv_tv = tv * df
    ev = pv_sum + pv_tv
    eq = ev + NETCASH0
    return dict(rows=rows, pv_sum=pv_sum, tv=tv, pv_tv=pv_tv, ev=ev, eq=eq, vps=eq / shares,
                roic_t=roic_t, fcff11=fcff11, nopat11=nopat11, g_term=g_term, tv_share=pv_tv / ev)


RES = {k: run_dcf(s) for k, s in SCEN.items()}
RES_DIL = {k: run_dcf(s, shares=SH_FD)["vps"] for k, s in SCEN.items()}          # v2: totalmente diluidas
RES_DIL_V1 = {k: run_dcf(s, shares=SH_DIL_V1)["vps"] for k, s in SCEN.items()}   # v1 (doble cómputo), informativo

# ---------------------------------------------------------------------------
# 4. Sensibilidad (caso base): WACC inicial x crecimiento terminal (WACC terminal se desplaza igual)
# ---------------------------------------------------------------------------
W_GRID = [round(WACC0 + d, 4) for d in (-0.03, -0.02, -0.01, 0.0, 0.01, 0.02)]
G_GRID = [0.02, 0.025, 0.03, 0.035, 0.04]
SENS = [[run_dcf(SCEN["base"], w0=w, wt=WACC_T + (w - WACC0), g_term=g)["vps"] for g in G_GRID] for w in W_GRID]
# Sensibilidad adicional: margen objetivo x crecimiento años 1-5 (multiplicador sobre los tres segmentos)
M_GRID = [0.06, 0.09, 0.12, 0.15, 0.20, 0.25]
GM_GRID = [0.5, 1.0, 1.5, 2.0]


def base_variant(m_obj, gmult):
    s = dict(SCEN["base"])
    s.update(m_obj=m_obj, g_auto=s["g_auto"] * gmult, g_ener=s["g_ener"] * gmult, g_serv=s["g_serv"] * gmult)
    return run_dcf(s)["vps"]


SENS2 = [[base_variant(m, gm) for gm in GM_GRID] for m in M_GRID]

# ---------------------------------------------------------------------------
# 5. DCF inverso
# Modelo simplificado: ingresos totales crecen a una TACC uniforme c durante 10 años; margen operativo pasa
# linealmente del 2,2 % (TTM sin créditos) al margen terminal M en el año 10; créditos = 0; reinversión
# por ventas/capital (supuesto base 1,5) con suelo de capex en años 1-2; WACC base; g = 3 %;
# ROIC terminal = max(12 %, ROIC implícito del margen) -> no penaliza márgenes altos.
# ---------------------------------------------------------------------------
G_REV = SCEN["base"]["g_term"]
STC_REV = SCEN["base"]["stc"]


def reverse_value(c, M, stc=STC_REV, w0=WACC0, wt=WACC_T, g=G_REV, years_m=N):
    wp = wacc_path(w0, wt)
    rev_prev, df, pv = REV0, 1.0, 0.0
    nopat = 0.0
    for t in range(N):
        rev = rev_prev * (1 + c)
        m = M_EX0 + (M - M_EX0) * min(t + 1, years_m) / years_m
        nopat = rev * m * (1 - TAX)
        reinv = (rev - rev_prev) / stc
        if t < 2:
            reinv = max(reinv, NET_CAPEX0_PCT * rev)
        df /= 1 + wp[t]
        pv += (nopat - reinv) * df
        rev_prev = rev
    roic_t = max(SCEN["base"]["roic_term"], M * (1 - TAX) * stc)
    tv = nopat * (1 + g) * (1 - g / roic_t) / (wt - g)
    eq = pv + tv * df + NETCASH0
    return eq / SH, rev_prev


def solve(f, lo, hi, target, it=200):
    flo, fhi = f(lo) - target, f(hi) - target
    if flo * fhi > 0:
        return None
    for _ in range(it):
        mid = (lo + hi) / 2
        fm = f(mid) - target
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2


REV_MARGINS = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35]
REVERSE = []
for M in REV_MARGINS:
    c = solve(lambda x: reverse_value(x, M)[0], -0.05, 0.80, PRICE)
    rev10 = reverse_value(c, M)[1] if c is not None else None
    REVERSE.append(dict(M=M, c=c, rev10=rev10, ebit10=rev10 * M if rev10 else None))
# margen necesario con las TACC de los escenarios
CAGR_SCEN = {k: (v["rows"][-1]["rev"] / REV0) ** (1 / N) - 1 for k, v in RES.items()}
REVERSE_M = {}
for k, cg in CAGR_SCEN.items():
    REVERSE_M[k] = solve(lambda M: reverse_value(cg, M)[0], 0.0, 1.0, PRICE)
# Combinaciones "redondas": ¿qué precio justifican?
REV_COMBOS = [(c, M, reverse_value(c, M)[0]) for c in (0.10, 0.15, 0.20, 0.25) for M in (0.15, 0.20, 0.25, 0.30)]

# ---------------------------------------------------------------------------
# 6. Múltiplos
# ---------------------------------------------------------------------------
TSLA_EV_SALES = EV_MKT / REV0
TSLA_EV_EBIT = EV_MKT / EBIT0
EPS_DIL_TTM = NI0 / MKT["acciones_diluidas_3T"][0]  # aproximación: media diluida 3T como denominador TTM
TSLA_PE = PRICE / EPS_DIL_TTM
TSLA_PE_COVER = MCAP / NI0

# (empresa, grupo, EV/Ventas, EV/EBITDA, EV/EBIT, PER, EV (M USD) , fuente/fecha). None = SIN VERIFICAR
PEERS = [
    ("Toyota (TM)", "Auto", 1.45, 9.46, 17.38, 8.8, 418590,
     "EV/Ventas, EV/EBITDA, PER, EV: TipRanks /stocks/tm/statistics (act. 23-oct-2026). EV/EBIT: roic.ai /quote/TM/statistics (datos a 30-jun-2026)"),
    ("BYD (BYDDY)", "Auto", 1.00, 6.37, 23.41, 25.2, 95920,
     "TipRanks /stocks/byddy/statistics (act. 15-oct-2026). EV/EBIT: roic.ai /quote/BYDDY/statistics (30-jun-2026; roic.ai muestra EV/EBIT = EV/EBITDA, dato dudoso)"),
    ("General Motors (GM)", "Auto", 1.00, 9.99, 94.91, 17.2, 167540,
     "TipRanks /stocks/gm/statistics (act. 23-oct-2026). EV/EBIT: roic.ai /quote/GM/statistics (30-jun-2026; distorsionado por cargos puntuales)"),
    ("Volkswagen (VWAGY)", "Auto", 0.94, 6.27, 7.92, 6.6, 310430,
     "TipRanks /stocks/vwagy/statistics (act. 24-oct-2026). EV/EBIT: roic.ai /quote/VWAGY/statistics (fecha no indicada; EV/EBIT = EV/EBITDA, dato dudoso)"),
    ("Apple (AAPL)", "Big tech", 9.36, 26.97, None, 39.3, 4200000,
     "TipRanks /stocks/aapl/statistics (act. 24-oct-2026). EV/EBIT SIN VERIFICAR"),
    ("Nvidia (NVDA)", "Big tech", 21.04, 31.43, None, 27.9, 4960000,
     "TipRanks /stocks/nvda/statistics (act. 23-oct-2026). EV/EBIT SIN VERIFICAR"),
    ("Microsoft (MSFT)", "Big tech", None, None, None, None, None,
     "SIN VERIFICAR: TipRanks (MSFT EE. UU.) no accesible; MarketScreener da estimaciones FY2026 (EV/Ventas 8,24; EV/EBIT 17,6; PER 20,8) con fecha no confirmada y capitalización aparentemente desfasada -> no se usan"),
]
TSLA_3RD = ("Tesla - terceros", "TipRanks (act. 23-oct-2026): EV/Ventas 15,21; EV/EBITDA 122,6; PER 327,5. roic.ai: EV/EBIT 342,45 (fecha no indicada). GuruFocus 23-oct-2026: PER TTM 410,39")


def med(group, idx):
    vals = [p[idx] for p in PEERS if p[1] == group and p[idx] is not None]
    return statistics.median(vals) if vals else None


MED = {g: {"ev_sales": med(g, 2), "ev_ebitda": med(g, 3), "ev_ebit": med(g, 4), "pe": med(g, 5)} for g in ("Auto", "Big tech")}


def implied_price_ev(mult, metric):
    return (mult * metric + NETCASH0) / SH


IMPLIED = {}
for g in MED:
    IMPLIED[g] = {
        "EV/Ventas": implied_price_ev(MED[g]["ev_sales"], REV0) if MED[g]["ev_sales"] else None,
        "EV/EBIT": implied_price_ev(MED[g]["ev_ebit"], EBIT0) if MED[g]["ev_ebit"] else None,
        "PER": MED[g]["pe"] * EPS_DIL_TTM if MED[g]["pe"] else None,
    }

TSLA_EBITDA0 = r("ebitda_aprox")                      # v2: EBIT + D&A TTM (Fase 2; sin ajustar SBC)
TSLA_EV_EBITDA = EV_MKT / TSLA_EBITDA0
TIPRANKS_TSLA_EV, TIPRANKS_TSLA_MCAP = 1.23e6, 1.53e6  # TipRanks TSLA (05 §2.3 D-7): EV y capitalización de la misma página
N_BIGTECH = sum(1 for p in PEERS if p[1] == "Big tech" and p[2] is not None)

# ---------------------------------------------------------------------------
# 9. Controles v2 (05-veredicto §5, prioridad 2; 02 v2; 04 v2)
# ---------------------------------------------------------------------------
B0 = RES["base"]

# (a) ROIC terminal del caso base: sensibilidad y referencias de Fase 2
ROIC_A_HIST = {y: r("roic_A_neto_caja", y) for y in ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025", "TTM_Q3_2026"]}
ROIC_B_HIST = {y: r("roic_B_bruto", y) for y in ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025", "TTM_Q3_2026"]}
ROIC_GRID = [("igual al WACC terminal (sin creación de valor)", None), ("10 %", 0.10), ("12 % (base)", 0.12),
             ("13,4 % (mínimo ROIC A FY21-24, FY2024)", ROIC_A_HIST["FY2024"]), ("15 %", 0.15)]
ROIC_SENS = [(lab, v, run_dcf(dict(SCEN["base"], roic_term=v))["vps"]) for lab, v in ROIC_GRID]

# (b) W9: beta solo sectorial en los años 1-5 (coherente) o desplazando también el WACC terminal (como la tabla 4.1)
KE_SEC = RF + BETA_BU * ERP
WACC0_SEC = KE_SEC * (1 - W_D) + KD * W_D
W9_15 = run_dcf(SCEN["base"], w0=WACC0_SEC, wt=WACC_T)["vps"]
W9_SHIFT = run_dcf(SCEN["base"], w0=WACC0_SEC, wt=WACC_T + (WACC0_SEC - WACC0))["vps"]

# (c) Asimetría costes/ingresos de la opcionalidad (04 §4.1.1): sensibilidad, NO corrección
RD_Q3_26, RD_Q3_25 = 2761.0, 1630.0                      # P4: I+D 3T26 y 3T25 (02 §3)
SBC_FY24 = r("sbc", "FY2024")
D_RD_ANUAL = 4 * (RD_Q3_26 - RD_Q3_25)                   # I+D incremental 3T26 anualizada (x4): cota alta
D_SBC = SBC0 - SBC_FY24                                  # SBC TTM por encima de FY2024 (plan del CEO 2025, P4)
REV0_EX = REV0 - CRED0
M0_SBC = M_EX0 + D_SBC / REV0_EX
M0_RD = M_EX0 + D_RD_ANUAL / REV0_EX
M0_AMBOS = M_EX0 + (D_SBC + D_RD_ANUAL) / REV0_EX
_s_nofloor = dict(SCEN["base"], reinv_pct=0.0)            # sin suelo de capex en años 1-2: solo ventas/capital
ASYM = [
    ("Base v2 (todo cargado al negocio actual)", M_EX0, False),
    ("Margen de partida sin el exceso de SBC sobre FY2024", M0_SBC, False),
    ("Margen de partida sin la I+D incremental 3T26 x 4", M0_RD, False),
    ("Margen de partida sin SBC extra ni I+D incremental", M0_AMBOS, False),
    ("Sin suelo de capex en años 1-2 (ola de capex = opcionalidad)", M_EX0, True),
    ("Las tres cosas a la vez (cota superior)", M0_AMBOS, True),
]
ASYM_RES = [(lab, m0, nf, run_dcf(_s_nofloor if nf else SCEN["base"], m0=m0)["vps"]) for lab, m0, nf in ASYM]

# (d) Capex bruto implícito del año 1 frente a la guía (T1)
CAPEX_GUIA_2026 = 20000.0                                  # T1: CFO, call 3T26, "~20.000 M$" (revisado desde >25.000, T10)
CAPEX_9M26 = 13014.0                                       # P2 (02 §4)
CAPEX_Y1 = B0["rows"][0]["reinv"] + DA_TTM

# (e) Mecanismo del margen base: qué hace falta para pasar del margen TTM al objetivo en el año 5
GP0 = r("beneficio_bruto")
OPEX0 = GP0 - EBIT0                                        # gastos operativos TTM (I+D + SG&A + otros)
GM_EX0 = (GP0 - CRED0) / REV0_EX                           # margen bruto sin créditos TTM
OPEX_R0 = OPEX0 / REV0_EX
GM_EX_HIST = {y: (r("beneficio_bruto", y) - r("creditos_regulatorios", y)) / (r("ingresos_totales", y) - r("creditos_regulatorios", y)) for y in YEARS}
OPEX_R_HIST = {y: (r("beneficio_bruto", y) - r("beneficio_operativo", y)) / (r("ingresos_totales", y) - r("creditos_regulatorios", y)) for y in YEARS}
R5_EX = B0["rows"][4]["rev"] - B0["rows"][4]["cred"]
M_BASE = SCEN["base"]["m_obj"]
OPEX_R_NEEDED = GM_EX0 - M_BASE                            # con margen bruto constante
OPEX5_NEEDED = OPEX_R_NEEDED * R5_EX
GM_NEEDED = OPEX_R0 + M_BASE                               # con gastos operativos / ingresos constantes

# (f) Energía: volumen frente a ingreso por GWh
STOR_FY25 = 46.7                                           # P6/P7: almacenamiento desplegado FY2025 (01 §1.1)
STOR_Q = [14.2, 8.8, 13.5, 13.7]                           # P4: 4T25..3T26 (04 §2, script fase4 §7)
STOR_TTM = sum(STOR_Q)
ENER_FY25 = r("ingresos_energia", "FY2025")
G_ENER_TTM = ENER0 / ENER_FY25 - 1
G_GWH_TTM = STOR_TTM / STOR_FY25 - 1
G_PRECIO_GWH = (ENER0 / STOR_TTM) / (ENER_FY25 / STOR_FY25) - 1   # incluye solar y leasing: aproximación
G_ENER_9M = r("crec_9M26_vs_9M25_ingresos_energia")    # Fase 2: -5,7 %

# (g) Activos no operativos fuera de la caja neta (P2, re-leído por Fase 3 el 25-oct-2026)
SPACEX_COMPRA, SPACEX_PLUSV, DIGITAL = 2002.0, 863.0, 962.0  # P3 (compra 1S26); P2 (plusvalía no realizada 9M26; activos digitales)
SPACEX_FV_INF = SPACEX_COMPRA + SPACEX_PLUSV                 # INFERENCIA: P2 no publica el valor contable de SpaceX por separado
NO_OPER_PS = (SPACEX_FV_INF + DIGITAL) / SH

# (h) DCF inverso con ventas/capital de tipo software (04 §4.1.5): advertencia medida
STC_SW = 3.0
REVERSE_SW = []
for M in (0.20, 0.25, 0.30):
    c_sw = solve(lambda x: reverse_value(x, M, stc=STC_SW)[0], -0.05, 0.80, PRICE)
    REVERSE_SW.append((M, c_sw))

# ---------------------------------------------------------------------------
# 7. Excel
# ---------------------------------------------------------------------------
wb = Workbook()
BOLD = Font(bold=True)
HDR = PatternFill("solid", fgColor="DDEBF7")
INP = Font(color="0000FF")  # azul = input
PCT, NUM, USD = "0.00%", "#,##0", "#,##0.00"


def hdr(ws, row, values, col=1):
    for i, v in enumerate(values):
        c = ws.cell(row=row, column=col + i, value=v)
        c.font = BOLD
        c.fill = HDR


# --- Supuestos ---
ws = wb.active
ws.title = "Supuestos"
ws["A1"] = "Tesla (TSLA) - Fase 3 v3 - Supuestos de valoración (azul = input; negro = fórmula). Fecha: 2026-10-24; v2 y v3 2026-10-25"
ws["A1"].font = BOLD
hdr(ws, 3, ["Parámetro", "Valor", "Unidad", "Fuente / justificación"])
NAMES = {}
rowi = 4


def put(key, label, value, unit, src, fmt=None, formula=False):
    global rowi
    ws.cell(row=rowi, column=1, value=label)
    c = ws.cell(row=rowi, column=2, value=value)
    if not formula:
        c.font = INP
    if fmt:
        c.number_format = fmt
    ws.cell(row=rowi, column=3, value=unit)
    ws.cell(row=rowi, column=4, value=src)
    NAMES[key] = f"Supuestos!$B${rowi}"
    rowi += 1


ws.cell(row=rowi, column=1, value="MERCADO").font = BOLD; rowi += 1
put("precio", "Precio TSLA", PRICE, "USD", MKT["precio"][2], USD)
put("acc", "Acciones en circulación (portada 10-Q)", SH, "M", MKT["acciones_cover"][2], "#,##0.0")
put("acc_dil", "Media diluida 3T-2026", MKT["acciones_diluidas_3T"][0], "M", MKT["acciones_diluidas_3T"][2], NUM)
put("acc_bas", "Media básica 3T-2026", MKT["acciones_basicas_3T"][0], "M", MKT["acciones_basicas_3T"][2], NUM)
put("acc_fd", "Acciones totalmente diluidas aprox. (v2)", SH_FD, "M",
    "02 §5.1 (ratios.csv, acc_totalmente_diluidas_aprox): portada + ~15 M de incentivos no emitidos. Contraste: diluida 3T 3.541 + restringidas CEO 2025 423,7 = "
    f"{SH_FD_CHECK:,.1f}. El reparto 286 / 15 de las 301 M es INFERENCIA de Fase 2. Sustituye a portada + 301 M de v1 (doble cómputo de ~286 M)", "#,##0.0")
put("mcap", "Capitalización", f"={NAMES['precio'].split('!')[1]}*{NAMES['acc'].split('!')[1]}", "M USD", "Precio x acciones portada (calculado)", NUM, True)
put("rf", "Tipo libre de riesgo (10a EE. UU.)", RF, "%", MKT["rf"][2], PCT)
put("erp", "Prima de riesgo de mercado (ERP)", ERP, "%", MKT["erp"][2], PCT)
put("b1", "Beta regresión (TipRanks)", MKT["beta_reg_1"][0], "x", MKT["beta_reg_1"][2], "0.00")
put("b2", "Beta regresión (MarketChameleon)", MKT["beta_reg_2"][0], "x", MKT["beta_reg_2"][2], "0.00")
put("bu", "Beta desapalancada sector Auto & Truck", MKT["beta_u_auto"][0], "x", MKT["beta_u_auto"][2], "0.00")
put("spread", "Diferencial de la deuda", MKT["spread_deuda"][0], "%", MKT["spread_deuda"][2], PCT)
put("tax", "Tipo impositivo", TAX, "%", MKT["tipo_imp"][2], PCT)
rowi += 1
ws.cell(row=rowi, column=1, value="FASE 2 (TTM a 3T-2026, M USD)").font = BOLD; rowi += 1
put("rev0", "Ingresos TTM", REV0, "M USD", "ratios.csv (Fase 2)", NUM)
put("auto_ex0", "Automoción sin créditos TTM", AUTO_EX0, "M USD", "ratios.csv: automoción total - créditos", NUM)
put("cred0", "Créditos regulatorios TTM", CRED0, "M USD", "ratios.csv", NUM)
put("ener0", "Energía TTM", ENER0, "M USD", "ratios.csv", NUM)
put("serv0", "Servicios y otros TTM", SERV0, "M USD", "ratios.csv", NUM)
put("ebit0", "Beneficio operativo TTM (GAAP, ya neto de SBC)", EBIT0, "M USD", "ratios.csv", NUM)
put("m_ex0", "Margen operativo sin créditos TTM (sobre ingresos sin créditos)", M_EX0, "%",
    "ratios.csv: (beneficio operativo - créditos) / (ingresos - créditos). v2: mismo denominador al que se aplica el margen (v1: 2,21 % sobre ingresos totales)", PCT)
put("ni0", "Beneficio neto atribuible TTM", NI0, "M USD", "ratios.csv", NUM)
put("sbc0", "SBC TTM (informativo; ya incluida en EBIT)", SBC0, "M USD", "ratios.csv", NUM)
put("capex0", "Capex TTM", CAPEX0, "M USD", "ratios.csv", NUM)
put("da0", "Amortización, depreciación y deterioro TTM (v2)", DA_TTM, "M USD",
    "ratios.csv (dya_amortizacion_deterioro): P4, reconciliación EBITDA TTM 3T26. v1 usaba 3T26 x 4 = 7.408", NUM)
put("ebitda0", "EBITDA aprox. TTM (EBIT + D&A, sin ajustar SBC)", f"={NAMES['ebit0'].split('!')[1]}+{NAMES['da0'].split('!')[1]}", "M USD", "Calculado; coincide con ratios.csv ebitda_aprox (Fase 2)", NUM, True)
put("reinv_pct", "Capex neto / ingresos TTM (suelo reinversión años 1-2)", f"=({NAMES['capex0'].split('!')[1]}-{NAMES['da0'].split('!')[1]})/{NAMES['rev0'].split('!')[1]}", "%", "Calculado", PCT, True)
put("cash0", "Caja + inversiones CP (30-sep-2026)", CASH0, "M USD", "ratios.csv", NUM)
put("debt0", "Deuda total (30-sep-2026)", DEBT0, "M USD", "ratios.csv (incl. arrend. financieros y deuda sin recurso)", NUM)
put("netcash", "Caja neta", f"={NAMES['cash0'].split('!')[1]}-{NAMES['debt0'].split('!')[1]}", "M USD", "Calculado", NUM, True)
put("stc_hist_A", "Ventas / capital invertido A (TTM)", SALES_TO_CAP_A, "x", "ratios.csv: ingresos / capital invertido A", "0.00")
put("stc_hist_B", "Ventas / capital invertido B (TTM)", SALES_TO_CAP_B, "x", "ratios.csv: ingresos / capital invertido B", "0.00")
rowi += 1
ws.cell(row=rowi, column=1, value="WACC").font = BOLD; rowi += 1
c = lambda k: NAMES[k].split("!")[1]
put("de", "Deuda / capitalización", f"={c('debt0')}/{c('mcap')}", "%", "Calculado", PCT, True)
put("beta_reg", "Beta regresión media", f"=AVERAGE({c('b1')},{c('b2')})", "x", "Calculado", "0.00", True)
put("beta_bu", "Beta bottom-up reapalancada", f"={c('bu')}*(1+(1-{c('tax')})*{c('de')})", "x", "Hamada sobre beta sector", "0.00", True)
put("beta0", "Beta inicial (50 % regresión + 50 % sector)", f"=AVERAGE({c('beta_reg')},{c('beta_bu')})", "x", "Supuesto: la regresión refleja la volatilidad real de TSLA; el sector, el negocio subyacente", "0.00", True)
put("betaT", "Beta terminal (empresa madura)", f"=AVERAGE(1,{c('bu')})", "x", "Supuesto: punto medio entre mercado (1) y sector auto", "0.00", True)
put("ke0", "Coste del capital inicial", f"={c('rf')}+{c('beta0')}*{c('erp')}", "%", "CAPM", PCT, True)
put("keT", "Coste del capital terminal", f"={c('rf')}+{c('betaT')}*{c('erp')}", "%", "CAPM", PCT, True)
put("kd", "Coste de la deuda después de impuestos", f"=({c('rf')}+{c('spread')})*(1-{c('tax')})", "%", "Calculado", PCT, True)
put("wd", "Peso de la deuda", f"={c('debt0')}/({c('debt0')}+{c('mcap')})", "%", "Valor de mercado de la acción; deuda a valor contable", PCT, True)
put("wacc0", "WACC inicial (años 1-5)", f"={c('ke0')}*(1-{c('wd')})+{c('kd')}*{c('wd')}", "%", "Calculado", PCT, True)
put("waccT", "WACC terminal (año 10 y perpetuidad)", f"={c('keT')}*(1-{c('wd')})+{c('kd')}*{c('wd')}", "%", "Calculado; años 6-10 convergen linealmente", PCT, True)
rowi += 1
ws.cell(row=rowi, column=1, value="ESCENARIOS").font = BOLD; rowi += 1
hdr(ws, rowi, ["Supuesto", "Bajista", "Base", "Alcista", "Justificación"]); rowi += 1
SC_ROW = {}
scen_rows = [
    ("g_auto", "Crec. automoción sin créditos, años 1-5", PCT, "Fase 2: FY21-25 TACC 10,2 %; FY24 -6,5 %; FY25 -9,8 %; 9M26 +10,6 %; 3T26 -3 %"),
    ("g_ener", "Crec. energía, años 1-5", PCT, f"v2: 9M26 {G_ENER_9M:+.1%}; TTM vs FY25: GWh {G_GWH_TTM:+.1%}, ingreso/GWh {G_PRECIO_GWH:+.1%}. Bajista 0 % (precio compensa volumen); base 8 % (p. ej. +20 % GWh y -10 % ingreso/GWh); alcista 20 %"),
    ("g_serv", "Crec. servicios y otros, años 1-5", PCT, "Fase 2: FY21-25 TACC 34,7 %; 9M26 +41 %"),
    ("m_obj", "Margen operativo objetivo sin créditos (desde año 5)", PCT, "Bajista = media FY24-25; base = media FY21-24; alcista = máximo FY22. v2: (EBIT - créditos) / (ingresos - créditos), sin redondeo"),
    ("stc", "Ventas / capital (reinversión incremental)", "0.00", "Fase 2: ventas/capital A 1,94x y B 1,05x (TTM)"),
    ("g_term", "Crecimiento terminal", PCT, "Por debajo de rf nominal (4,97 %)"),
    ("roic_term", "ROIC terminal (vacío = WACC terminal)", PCT, "Bajista: = WACC terminal. Base 12 %: POR DEBAJO del mínimo FY21-24 del ROIC A (13,4 %, FY24) y por encima del FY25 (7,6 %) y TTM (5,5 %); diferencial de ~2,2 pp sobre el WACC terminal. Alcista 15 %: dentro de FY21-24 (13,4-48 %)"),
]
for key, label, fmt, just in scen_rows:
    ws.cell(row=rowi, column=1, value=label)
    for j, sk in enumerate(["bajista", "base", "alcista"]):
        v = SCEN[sk][key]
        cell = ws.cell(row=rowi, column=2 + j, value=v)
        cell.font = INP
        cell.number_format = fmt
    ws.cell(row=rowi, column=5, value=just)
    SC_ROW[key] = rowi
    rowi += 1
ws.cell(row=rowi, column=1, value="Créditos regulatorios años 1-3")
for j, sk in enumerate(["bajista", "base", "alcista"]):
    ws.cell(row=rowi, column=2 + j, value=" / ".join(f"{x:,.0f}" for x in SCEN[sk]["cred"]))
ws.cell(row=rowi, column=5, value="40 % / 10 % / 0 % del TTM: OBBBA restringe programas (Fase 1 §4; 3T26 -73 %)")
rowi += 1
for sk in ["bajista", "base", "alcista"]:
    ws.cell(row=rowi, column=1, value=f"Narrativa {sk}")
    ws.cell(row=rowi, column=2, value=SCEN[sk]["nota"])
    rowi += 1
ws.column_dimensions["A"].width = 52
ws.column_dimensions["B"].width = 16
ws.column_dimensions["C"].width = 12
ws.column_dimensions["D"].width = 14
ws.column_dimensions["E"].width = 60
SCOL = {"bajista": "B", "base": "C", "alcista": "D"}

# --- Escenarios (fórmulas) ---
ws2 = wb.create_sheet("Escenarios")
ws2["A1"] = "DCF FCFF por escenario (M USD). Crecimientos y márgenes por año = supuestos (azul); resto = fórmulas"
ws2["A1"].font = BOLD
r0 = 3
XL_CELLS = {}
for sk in ["bajista", "base", "alcista"]:
    s = SCEN[sk]
    res = RES[sk]
    ws2.cell(row=r0, column=1, value=f"ESCENARIO {sk.upper()}").font = BOLD
    hdr(ws2, r0 + 1, ["Año"] + list(range(0, N + 1)))
    labels = ["Crec. automoción sin créd.", "Automoción sin créditos", "Créditos regulatorios", "Crec. energía", "Energía",
              "Crec. servicios", "Servicios y otros", "Ingresos totales", "Crec. ingresos", "Margen op. sin créditos",
              "EBIT (GAAP, neto de SBC)", "NOPAT", "Reinversión neta", "FCFF", "WACC del año", "Factor de descuento", "VP FCFF"]
    rr = {lab: r0 + 2 + i for i, lab in enumerate(labels)}
    for lab, row in rr.items():
        ws2.cell(row=row, column=1, value=lab)
    col0 = 2  # año 0 en columna B
    L = lambda t: get_column_letter(col0 + t)
    sc = SCOL[sk]
    S = lambda k: f"Supuestos!${sc}${SC_ROW[k]}"
    # año 0
    ws2[f"{L(0)}{rr['Automoción sin créditos']}"] = f"={NAMES['auto_ex0']}"
    ws2[f"{L(0)}{rr['Créditos regulatorios']}"] = f"={NAMES['cred0']}"
    ws2[f"{L(0)}{rr['Energía']}"] = f"={NAMES['ener0']}"
    ws2[f"{L(0)}{rr['Servicios y otros']}"] = f"={NAMES['serv0']}"
    ws2[f"{L(0)}{rr['Ingresos totales']}"] = f"=SUM({L(0)}{rr['Automoción sin créditos']},{L(0)}{rr['Créditos regulatorios']},{L(0)}{rr['Energía']},{L(0)}{rr['Servicios y otros']})"
    ws2[f"{L(0)}{rr['Margen op. sin créditos']}"] = f"={NAMES['m_ex0']}"
    ws2[f"{L(0)}{rr['EBIT (GAAP, neto de SBC)']}"] = f"={NAMES['ebit0']}"
    for t in range(1, N + 1):
        row = res["rows"][t - 1]
        col, prv = L(t), L(t - 1)
        for lab, val in (("Crec. automoción sin créd.", growth_path(s["g_auto"], s["g_term"])[t - 1]),
                         ("Crec. energía", growth_path(s["g_ener"], s["g_term"])[t - 1]),
                         ("Crec. servicios", growth_path(s["g_serv"], s["g_term"])[t - 1]),
                         ("Margen op. sin créditos", row["m"]),
                         ("Créditos regulatorios", row["cred"])):
            cell = ws2[f"{col}{rr[lab]}"]
            cell.value = val
            cell.font = INP
        ws2[f"{col}{rr['Automoción sin créditos']}"] = f"={prv}{rr['Automoción sin créditos']}*(1+{col}{rr['Crec. automoción sin créd.']})"
        ws2[f"{col}{rr['Energía']}"] = f"={prv}{rr['Energía']}*(1+{col}{rr['Crec. energía']})"
        ws2[f"{col}{rr['Servicios y otros']}"] = f"={prv}{rr['Servicios y otros']}*(1+{col}{rr['Crec. servicios']})"
        ws2[f"{col}{rr['Ingresos totales']}"] = f"=SUM({col}{rr['Automoción sin créditos']},{col}{rr['Créditos regulatorios']},{col}{rr['Energía']},{col}{rr['Servicios y otros']})"
        ws2[f"{col}{rr['Crec. ingresos']}"] = f"={col}{rr['Ingresos totales']}/{prv}{rr['Ingresos totales']}-1"
        ws2[f"{col}{rr['EBIT (GAAP, neto de SBC)']}"] = f"={col}{rr['Margen op. sin créditos']}*({col}{rr['Ingresos totales']}-{col}{rr['Créditos regulatorios']})+{col}{rr['Créditos regulatorios']}"
        ws2[f"{col}{rr['NOPAT']}"] = f"={col}{rr['EBIT (GAAP, neto de SBC)']}*(1-{NAMES['tax']})"
        stc_f = f"({col}{rr['Ingresos totales']}-{prv}{rr['Ingresos totales']})/{S('stc')}"
        if t <= 2:
            ws2[f"{col}{rr['Reinversión neta']}"] = f"=MAX({NAMES['reinv_pct']}*{col}{rr['Ingresos totales']},{stc_f})"
        else:
            ws2[f"{col}{rr['Reinversión neta']}"] = f"={stc_f}"
        ws2[f"{col}{rr['FCFF']}"] = f"={col}{rr['NOPAT']}-{col}{rr['Reinversión neta']}"
        if t <= 5:
            ws2[f"{col}{rr['WACC del año']}"] = f"={NAMES['wacc0']}"
        else:
            ws2[f"{col}{rr['WACC del año']}"] = f"={NAMES['wacc0']}+({NAMES['waccT']}-{NAMES['wacc0']})*{t - 5}/5"
        prev_df = "1" if t == 1 else f"{prv}{rr['Factor de descuento']}"
        ws2[f"{col}{rr['Factor de descuento']}"] = f"={prev_df}/(1+{col}{rr['WACC del año']})"
        ws2[f"{col}{rr['VP FCFF']}"] = f"={col}{rr['FCFF']}*{col}{rr['Factor de descuento']}"
    for lab in rr:
        fmt = PCT if lab.startswith(("Crec", "Margen", "WACC")) else ("0.0000" if lab.startswith("Factor") else NUM)
        for t in range(0, N + 1):
            ws2[f"{L(t)}{rr[lab]}"].number_format = fmt
    # valor terminal y resultado
    rb = r0 + 2 + len(labels) + 1
    L10 = L(N)
    roic_ref = f"IF(ISBLANK({S('roic_term')}),{NAMES['waccT']},{S('roic_term')})"
    items = [
        ("NOPAT año 11", f"={L10}{rr['NOPAT']}*(1+{S('g_term')})", NUM),
        ("ROIC terminal", f"={roic_ref}", PCT),
        ("FCFF año 11 = NOPAT x (1 - g/ROIC)", f"=B{rb}*(1-{S('g_term')}/B{rb + 1})", NUM),
        ("Valor terminal (año 10)", f"=B{rb + 2}/({NAMES['waccT']}-{S('g_term')})", NUM),
        ("VP valor terminal", f"=B{rb + 3}*{L10}{rr['Factor de descuento']}", NUM),
        ("Suma VP FCFF años 1-10", f"=SUM({L(1)}{rr['VP FCFF']}:{L10}{rr['VP FCFF']})", NUM),
        ("Valor de la empresa (EV)", f"=B{rb + 4}+B{rb + 5}", NUM),
        ("% del EV en valor terminal", f"=B{rb + 4}/B{rb + 6}", PCT),
        ("+ Caja neta (30-sep-2026)", f"={NAMES['netcash']}", NUM),
        ("Valor de las acciones", f"=B{rb + 6}+B{rb + 8}", NUM),
        ("Valor por acción (USD)", f"=B{rb + 9}/{NAMES['acc']}", USD),
        ("Precio actual (USD)", f"={NAMES['precio']}", USD),
        ("Valor / precio - 1", f"=B{rb + 10}/B{rb + 11}-1", PCT),
        ("Valor por acción totalmente diluido (USD, v2)", f"=B{rb + 9}/{NAMES['acc_fd']}", USD),
    ]
    for i, (lab, f_, fmt) in enumerate(items):
        ws2.cell(row=rb + i, column=1, value=lab).font = BOLD if "acción" in lab else Font()
        cc = ws2.cell(row=rb + i, column=2, value=f_)
        cc.number_format = fmt
    XL_CELLS[sk] = f"B{rb + 10}"
    r0 = rb + len(items) + 2
ws2.column_dimensions["A"].width = 38
for col in range(2, N + 3):
    ws2.column_dimensions[get_column_letter(col)].width = 11

# --- Sensibilidad ---
ws3 = wb.create_sheet("Sensibilidad")
ws3["A1"] = "Caso base - valor por acción (USD). Filas: WACC inicial (el WACC terminal se desplaza lo mismo). Columnas: crecimiento terminal. Valores calculados por el script."
ws3["A1"].font = BOLD
hdr(ws3, 3, ["WACC inicial \\ g"] + G_GRID)
for i, w in enumerate(W_GRID):
    ws3.cell(row=4 + i, column=1, value=w).number_format = PCT
    for j, v in enumerate(SENS[i]):
        ws3.cell(row=4 + i, column=2 + j, value=round(v, 2)).number_format = USD
for j in range(len(G_GRID)):
    ws3.cell(row=3, column=2 + j).number_format = PCT
r_ = 4 + len(W_GRID) + 2
ws3.cell(row=r_, column=1, value="Caso base - valor por acción (USD). Filas: margen operativo objetivo. Columnas: multiplicador del crecimiento de los tres segmentos en años 1-5 (1,0 = base).").font = BOLD
hdr(ws3, r_ + 1, ["Margen \\ x crec."] + GM_GRID)
for i, m in enumerate(M_GRID):
    ws3.cell(row=r_ + 2 + i, column=1, value=m).number_format = PCT
    for j, v in enumerate(SENS2[i]):
        ws3.cell(row=r_ + 2 + i, column=2 + j, value=round(v, 2)).number_format = USD
ws3.cell(row=r_ + 3 + len(M_GRID), column=1, value=f"Precio actual: {PRICE} USD")
# v2: bloques de control (valores calculados por el script)
r_ = r_ + 5 + len(M_GRID)
ws3.cell(row=r_, column=1, value="v2 - ROIC terminal del caso base (VPA, USD)").font = BOLD
hdr(ws3, r_ + 1, ["ROIC terminal", "Valor", "VPA base"])
for i, (lab, v, vps) in enumerate(ROIC_SENS):
    ws3.cell(row=r_ + 2 + i, column=1, value=lab)
    ws3.cell(row=r_ + 2 + i, column=2, value=round(v if v is not None else WACC_T, 4)).number_format = PCT
    ws3.cell(row=r_ + 2 + i, column=3, value=round(vps, 2)).number_format = USD
r_ = r_ + 3 + len(ROIC_SENS)
ws3.cell(row=r_, column=1, value="v2 - W9: beta solo sectorial (VPA base, USD). El modelo mantiene la beta mezclada 50/50").font = BOLD
hdr(ws3, r_ + 1, ["Variante", "WACC inicial", "WACC terminal", "VPA base", "Diferencia"])
for i, (lab, w0_, wt_, v_) in enumerate((("Modelo (beta mezclada)", WACC0, WACC_T, B0["vps"]),
                                          ("Beta sectorial solo años 1-5 (coherente)", WACC0_SEC, WACC_T, W9_15),
                                          ("Beta sectorial y WACC terminal desplazado (como tabla 4.1)", WACC0_SEC, WACC_T + WACC0_SEC - WACC0, W9_SHIFT))):
    rr_ = r_ + 2 + i
    ws3.cell(row=rr_, column=1, value=lab)
    ws3.cell(row=rr_, column=2, value=round(w0_, 4)).number_format = PCT
    ws3.cell(row=rr_, column=3, value=round(wt_, 4)).number_format = PCT
    ws3.cell(row=rr_, column=4, value=round(v_, 2)).number_format = USD
    ws3.cell(row=rr_, column=5, value=round(v_ - B0["vps"], 2)).number_format = USD
r_ = r_ + 6
ws3.cell(row=r_, column=1, value="v2 - Asimetría costes/ingresos de la opcionalidad (sensibilidad, NO corrección; VPA base, USD)").font = BOLD
hdr(ws3, r_ + 1, ["Variante", "Margen de partida", "Suelo de capex años 1-2", "VPA base", "Diferencia"])
for i, (lab, m0, nf, vps) in enumerate(ASYM_RES):
    rr_ = r_ + 2 + i
    ws3.cell(row=rr_, column=1, value=lab)
    ws3.cell(row=rr_, column=2, value=round(m0, 4)).number_format = PCT
    ws3.cell(row=rr_, column=3, value="no" if nf else "sí")
    ws3.cell(row=rr_, column=4, value=round(vps, 2)).number_format = USD
    ws3.cell(row=rr_, column=5, value=round(vps - B0["vps"], 2)).number_format = USD
ws3.column_dimensions["A"].width = 62

# --- DCF inverso ---
ws4 = wb.create_sheet("DCF_inverso")
ws4["A1"] = ("DCF inverso: TACC de ingresos (10 años, uniforme) necesaria para justificar el precio actual, según el margen operativo "
             "alcanzado en el año 10. Supuestos fijos: WACC base, g 3 %, ventas/capital 1,5, impuesto 21 %, sin créditos.")
ws4["A1"].font = BOLD
hdr(ws4, 3, ["Margen operativo año 10", "TACC ingresos necesaria", "Ingresos año 10 (M USD)", "EBIT año 10 (M USD)", "Ingresos año 10 / TTM (x)"])
for i, d in enumerate(REVERSE):
    rw = 4 + i
    ws4.cell(row=rw, column=1, value=d["M"]).number_format = PCT
    if d["c"] is None:
        ws4.cell(row=rw, column=2, value="no alcanzable")
    else:
        ws4.cell(row=rw, column=2, value=round(d["c"], 4)).number_format = PCT
        ws4.cell(row=rw, column=3, value=f"={NAMES['rev0']}*(1+B{rw})^10").number_format = NUM
        ws4.cell(row=rw, column=4, value=f"=C{rw}*A{rw}").number_format = NUM
        ws4.cell(row=rw, column=5, value=f"=C{rw}/{NAMES['rev0']}").number_format = "0.0"
rw = 4 + len(REVERSE) + 2
ws4.cell(row=rw, column=1, value="Margen operativo año 10 necesario con la TACC de cada escenario").font = BOLD
hdr(ws4, rw + 1, ["Escenario", "TACC ingresos 10a", "Margen necesario"])
for i, (k, cg) in enumerate(CAGR_SCEN.items()):
    ws4.cell(row=rw + 2 + i, column=1, value=k)
    ws4.cell(row=rw + 2 + i, column=2, value=round(cg, 4)).number_format = PCT
    mm = REVERSE_M[k]
    ws4.cell(row=rw + 2 + i, column=3, value=round(mm, 4) if mm is not None else "no alcanzable (>100 %)")
    if mm is not None:
        ws4.cell(row=rw + 2 + i, column=3).number_format = PCT
rw = rw + 2 + len(CAGR_SCEN) + 1
ws4.cell(row=rw, column=1, value="Valor por acción (USD) para combinaciones TACC x margen año 10").font = BOLD
hdr(ws4, rw + 1, ["TACC \\ margen", 0.15, 0.20, 0.25, 0.30])
for i, cg in enumerate((0.10, 0.15, 0.20, 0.25)):
    ws4.cell(row=rw + 2 + i, column=1, value=cg).number_format = PCT
    for j, M in enumerate((0.15, 0.20, 0.25, 0.30)):
        v = [x[2] for x in REV_COMBOS if x[0] == cg and x[1] == M][0]
        ws4.cell(row=rw + 2 + i, column=2 + j, value=round(v, 2)).number_format = USD
rw = rw + 2 + 4 + 1
ws4.cell(row=rw, column=1, value="Valor implícito NO explicado por el DCF (capitalización - valor de las acciones del escenario)").font = BOLD
hdr(ws4, rw + 1, ["Escenario", "Valor acciones DCF (M USD)", "Capitalización (M USD)", "Diferencia (M USD)", "% de la capitalización"])
for i, k in enumerate(["bajista", "base", "alcista"]):
    rr_ = rw + 2 + i
    ws4.cell(row=rr_, column=1, value=k)
    ws4.cell(row=rr_, column=2, value=round(RES[k]["eq"], 0)).number_format = NUM
    ws4.cell(row=rr_, column=3, value=f"={NAMES['mcap']}").number_format = NUM
    ws4.cell(row=rr_, column=4, value=f"=C{rr_}-B{rr_}").number_format = NUM
    ws4.cell(row=rr_, column=5, value=f"=D{rr_}/C{rr_}").number_format = PCT
rw = rw + 2 + 3 + 1
ws4.cell(row=rw, column=1, value=f"v2 - Advertencia: con ventas/capital de tipo software ({STC_SW:.1f}x en lugar de {STC_REV:.1f}x), TACC necesaria").font = BOLD
hdr(ws4, rw + 1, ["Margen operativo año 10", f"TACC con {STC_REV:.1f}x", f"TACC con {STC_SW:.1f}x"])
for i, (M, c_sw) in enumerate(REVERSE_SW):
    base_c = [d["c"] for d in REVERSE if d["M"] == M][0]
    ws4.cell(row=rw + 2 + i, column=1, value=M).number_format = PCT
    ws4.cell(row=rw + 2 + i, column=2, value=round(base_c, 4)).number_format = PCT
    ws4.cell(row=rw + 2 + i, column=3, value=round(c_sw, 4) if c_sw is not None else "no alcanzable").number_format = PCT
ws4.column_dimensions["A"].width = 30
for col in "BCDE":
    ws4.column_dimensions[col].width = 24

# --- Múltiplos ---
ws5 = wb.create_sheet("Multiplos")
ws5["A1"] = "Múltiplos comparables (TTM salvo indicación). Vacío = SIN VERIFICAR. Datos de terceros con su fecha; TSLA calculado con datos de Fase 2 + precio."
ws5["A1"].font = BOLD
hdr(ws5, 3, ["Empresa", "Grupo", "EV/Ventas", "EV/EBITDA", "EV/EBIT", "PER", "EV (M USD)", "Ingresos implícitos (M USD) = EV / (EV/Ventas)", "Fuente / fecha"])
rw = 4
ws5.cell(row=rw, column=1, value="Tesla (calculado)").font = BOLD
ws5.cell(row=rw, column=2, value="TSLA")
ws5.cell(row=rw, column=3, value=f"=G{rw}/{NAMES['rev0']}").number_format = "0.0"
ws5.cell(row=rw, column=4, value=f"=G{rw}/{NAMES['ebitda0']}").number_format = "0.0"
ws5.cell(row=rw, column=5, value=f"=G{rw}/{NAMES['ebit0']}").number_format = "0.0"
ws5.cell(row=rw, column=6, value=f"={NAMES['precio']}/({NAMES['ni0']}/{NAMES['acc_dil']})").number_format = "0.0"
ws5.cell(row=rw, column=7, value=f"={NAMES['mcap']}-{NAMES['netcash']}").number_format = NUM
ws5.cell(row=rw, column=8, value=f"={NAMES['rev0']}").number_format = NUM
ws5.cell(row=rw, column=9, value="EV = capitalización (precio 23-oct x acciones portada) - caja neta Fase 2. PER = precio / (BN TTM / media diluida 3T). v2: EV/EBITDA con EBITDA aprox. de Fase 2 (EBIT + D&A TTM, sin ajustar SBC)")
rw += 1
ws5.cell(row=rw, column=1, value=TSLA_3RD[0])
ws5.cell(row=rw, column=2, value="TSLA")
ws5.cell(row=rw, column=3, value=15.21)
ws5.cell(row=rw, column=4, value=122.6)
ws5.cell(row=rw, column=5, value=342.45)
ws5.cell(row=rw, column=6, value=327.5)
ws5.cell(row=rw, column=9, value=TSLA_3RD[1] + (
    f" | v2 AVISO: la misma página de TipRanks da EV {TIPRANKS_TSLA_EV / 1e6:.2f} bill. $ con capitalización {TIPRANKS_TSLA_MCAP / 1e6:.2f} bill. $ "
    f"(diferencia {(TIPRANKS_TSLA_MCAP - TIPRANKS_TSLA_EV):,.0f} M$, frente a una caja neta de {NETCASH0:,.0f} M$): dato internamente incoherente, solo contraste"))
rw += 1
first_peer = rw
for p in PEERS:
    ws5.cell(row=rw, column=1, value=p[0])
    ws5.cell(row=rw, column=2, value=p[1])
    for j, idx in enumerate((2, 3, 4, 5)):
        v = p[idx]
        ws5.cell(row=rw, column=3 + j, value=v if v is not None else "SIN VERIFICAR")
    ws5.cell(row=rw, column=7, value=p[6] if p[6] is not None else "SIN VERIFICAR")
    if p[6] is not None and p[2] is not None:
        ws5.cell(row=rw, column=8, value=f"=G{rw}/C{rw}").number_format = NUM
    ws5.cell(row=rw, column=9, value=p[7])
    rw += 1
last_peer = rw - 1
rw += 1
GROUP_ROWS = {}
for i, p in enumerate(PEERS):
    GROUP_ROWS.setdefault(p[1], []).append(first_peer + i)
for g in ("Auto", "Big tech"):
    ws5.cell(row=rw, column=1, value=f"Mediana {g}").font = BOLD
    lo, hi = min(GROUP_ROWS[g]), max(GROUP_ROWS[g])  # filas contiguas por grupo; MEDIAN ignora texto
    for j, colL in enumerate("CDEF"):
        ws5.cell(row=rw, column=3 + j, value=f'=IFERROR(MEDIAN({colL}{lo}:{colL}{hi}),"SIN VERIFICAR")')
        ws5.cell(row=rw, column=3 + j).number_format = "0.00"
    rw += 1
# fórmulas matriciales: escribir también los valores calculados por Python como contraste
rw += 1
ws5.cell(row=rw, column=1, value="Precio implícito de TSLA aplicando la mediana del grupo (USD/acción; cálculo del script)").font = BOLD
rw += 1
hdr(ws5, rw, ["Grupo", "", "EV/Ventas", "", "EV/EBIT", "PER", "Medianas (script): EV/Ventas | EV/EBIT | PER"])
rw += 1
for g in ("Auto", "Big tech"):
    ws5.cell(row=rw, column=1, value=g)
    for col, key in ((3, "EV/Ventas"), (5, "EV/EBIT"), (6, "PER")):
        v = IMPLIED[g][key]
        ws5.cell(row=rw, column=col, value=round(v, 2) if v is not None else "SIN VERIFICAR")
    m = MED[g]
    ws5.cell(row=rw, column=7, value=" | ".join("SIN VERIFICAR" if m[k] is None else f"{m[k]:.2f}" for k in ("ev_sales", "ev_ebit", "pe")))
    rw += 1
ws5.cell(row=rw + 1, column=1, value=(f"v2 AVISO: la mediana big tech tiene n = {N_BIGTECH} (Apple y Nvidia; Microsoft SIN VERIFICAR). "
                                      "No es representativa: con dos datos, la mediana es su media aritmética."))
ws5.column_dimensions["A"].width = 24
ws5.column_dimensions["I"].width = 110
ws5.column_dimensions["H"].width = 22

wb.save(OUT_XLSX)


def recalc_xlsx(path):
    """v2: si LibreOffice está instalado, recalcula el libro y guarda los valores cacheados (05 §1: v1 se guardaba
    sin valores y un visor que no recalcula mostraba celdas vacías). Si falla, se queda el libro de openpyxl."""
    soffice = shutil.which("soffice")
    if not soffice or os.environ.get("DCF_NO_RECALC"):
        return "no recalculado (LibreOffice no disponible o DCF_NO_RECALC)"
    tmp = tempfile.mkdtemp(prefix="dcf_recalc_")
    try:
        subprocess.run([soffice, f"-env:UserInstallation=file://{tmp}/profile", "--headless", "--calc",
                        "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", tmp, path],
                       check=True, capture_output=True, timeout=180)
        out = os.path.join(tmp, os.path.basename(path))
        shutil.copyfile(out, path)
        return "recalculado con LibreOffice (valores cacheados)"
    except Exception as e:  # noqa: BLE001
        return f"no recalculado ({type(e).__name__})"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


RECALC = recalc_xlsx(OUT_XLSX)

# ---------------------------------------------------------------------------
# 8. Salida por pantalla
# ---------------------------------------------------------------------------
pr = print
pr("=== MERCADO Y WACC ===")
pr(f"Precio {PRICE:.2f} | acciones {SH:,.1f} M | capitalización {MCAP:,.0f} M$ | EV {EV_MKT:,.0f} M$ | caja neta {NETCASH0:,.0f}")
pr(f"D/E {D_E:.4f} | beta regresión {BETA_REG:.3f} | beta bottom-up {BETA_BU:.3f} | beta inicial {BETA0:.3f} | beta terminal {BETA_T:.3f}")
pr(f"Ke0 {KE0:.4f} | KeT {KE_T:.4f} | Kd(1-t) {KD:.4f} | wD {W_D:.4f} | WACC0 {WACC0:.4f} | WACC_T {WACC_T:.4f}")
for lab, b in (("solo regresión", BETA_REG), ("solo bottom-up", BETA_BU)):
    pr(f"WACC0 alternativo ({lab}, beta {b:.2f}): {(RF + b * ERP) * (1 - W_D) + KD * W_D:.4f}")
pr(f"Anclas margen sin créditos: media FY21-24 {M_EX_AVG_21_24:.4f} | media FY24-25 {M_EX_AVG_24_25:.4f} | máx {M_EX_MAX:.4f} | TTM {M_EX0:.4f}")
pr("  v2: sobre ingresos sin créditos, sin redondeo. Por año: " + ", ".join(f"{y} {M_EX_HIST[y]:.2%}" for y in YEARS))
pr(f"  v1 (sobre ingresos totales, redondeado a 3 decimales): bajista {ANCLAS_V1[0]:.3f} | base {ANCLAS_V1[1]:.3f} | alcista {ANCLAS_V1[2]:.3f} | TTM {M_EX0_V1:.4f}")
pr(f"D&A TTM {DA_TTM:,.0f} (v1 aprox 3T x 4: {DA_TTM_V1:,.0f}) | capex neto/ingresos TTM {NET_CAPEX0_PCT:.4f} | ventas/capital A {SALES_TO_CAP_A:.2f} B {SALES_TO_CAP_B:.2f}")
pr(f"Acciones: portada {SH:,.2f} | totalmente diluidas {SH_FD:,.1f} (contraste diluida 3T + CEO 2025 = {SH_FD_CHECK:,.1f}) | v1 portada + 301 = {SH_DIL_V1:,.1f}")
pr("\n=== ESCENARIOS ===")
for k, v in RES.items():
    last = v["rows"][-1]
    pr(f"{k:8s}: ingresos año10 {last['rev']:,.0f} (TACC {CAGR_SCEN[k]:.2%}) | EBIT10 {last['ebit']:,.0f} | FCFF10 {last['fcff']:,.0f} | "
       f"VP FCFF {v['pv_sum']:,.0f} | VP TV {v['pv_tv']:,.0f} ({v['tv_share']:.0%}) | EV {v['ev']:,.0f} | equity {v['eq']:,.0f} | "
       f"VPA {v['vps']:.2f} $ ({v['vps'] / PRICE - 1:+.0%}) | VPA totalmente diluido {RES_DIL[k]:.2f} (v1 portada+301: {RES_DIL_V1[k]:.2f})")
    pr("          FCFF por año: " + ", ".join(f"{x['fcff']:,.0f}" for x in v["rows"]))
pr("\n=== SENSIBILIDAD BASE (VPA) WACC0 x g ===")
pr("WACC0   " + "  ".join(f"g={g:.1%}" for g in G_GRID))
for w, row in zip(W_GRID, SENS):
    pr(f"{w:.2%}  " + "  ".join(f"{v:7.2f}" for v in row))
pr("\n=== SENSIBILIDAD BASE (VPA) margen x multiplicador crecimiento ===")
for m, row in zip(M_GRID, SENS2):
    pr(f"{m:.0%}  " + "  ".join(f"{v:7.2f}" for v in row))
pr("\n=== DCF INVERSO ===")
for d in REVERSE:
    if d["c"] is None:
        pr(f"Margen {d['M']:.0%}: no alcanzable")
    else:
        pr(f"Margen {d['M']:.0%}: TACC necesaria {d['c']:.2%} -> ingresos año10 {d['rev10']:,.0f} ({d['rev10'] / REV0:.1f}x TTM), EBIT10 {d['ebit10']:,.0f}")
for k, mm in REVERSE_M.items():
    pr(f"Con TACC {k} ({CAGR_SCEN[k]:.2%}): margen necesario {'no alcanzable' if mm is None else f'{mm:.2%}'}")
for k in RES:
    gap = MCAP - RES[k]["eq"]
    pr(f"Valor no explicado {k}: {gap:,.0f} M$ ({gap / MCAP:.1%} de la capitalización; {gap / SH:.2f} $/acción)")
pr("Combinaciones (TACC, margen, VPA): " + "; ".join(f"({c:.0%},{M:.0%}) {v:.0f}" for c, M, v in REV_COMBOS))
pr("\n=== MÚLTIPLOS ===")
pr(f"TSLA: EV/Ventas {TSLA_EV_SALES:.1f} | EV/EBIT {TSLA_EV_EBIT:.0f} | PER (BPA diluido aprox {EPS_DIL_TTM:.3f}) {TSLA_PE:.0f} | PER sobre acciones portada {TSLA_PE_COVER:.0f}")
pr(f"TSLA EV/EBITDA aprox (EBITDA Fase 2 {TSLA_EBITDA0:,.0f}, sin ajustar SBC): {TSLA_EV_EBITDA:.1f}")
pr(f"AVISO TipRanks TSLA: EV {TIPRANKS_TSLA_EV:,.0f} vs capitalización {TIPRANKS_TSLA_MCAP:,.0f} -> diferencia {TIPRANKS_TSLA_MCAP - TIPRANKS_TSLA_EV:,.0f} M$ "
   f"frente a caja neta {NETCASH0:,.0f} M$ (incoherente; {(TIPRANKS_TSLA_MCAP - TIPRANKS_TSLA_EV) / NETCASH0:.1f}x)")
pr(f"AVISO mediana big tech: n = {N_BIGTECH}")
for g in MED:
    pr(f"Mediana {g}: {MED[g]} -> precio implícito {IMPLIED[g]}")
for p in PEERS:
    if p[6] and p[2]:
        pr(f"  {p[0]}: ingresos implícitos {p[6] / p[2]:,.0f} M$")
pr("\n=== CIFRAS DE CONTEXTO CITADAS EN 03-valoracion.md ===")
pr(f"TACC ingresos FY23-25: {(r('ingresos_totales', 'FY2025') / r('ingresos_totales', 'FY2023')) ** 0.5 - 1:.2%}")
toyota_rev = PEERS[0][6] / PEERS[0][2]
for d in REVERSE:
    if d["M"] in (0.20, 0.25, 0.30):
        pr(f"Margen {d['M']:.0%}: ingresos año10 / ingresos Toyota = {d['rev10'] / toyota_rev:.1f}x | EBIT10 / EBIT TTM = {d['ebit10'] / EBIT0:.0f}x | margen / máx histórico = {d['M'] / M_EX_MAX:.1f}x | capital nuevo acumulado = {(d['rev10'] - REV0) / STC_REV:,.0f} M$")
pr(f"Capital por $ de ingreso incremental (base): {1 / SCEN['base']['stc']:.2f} $")
pr(f"Caja neta por acción: {NETCASH0 / SH:.2f} $")
pr(f"Acciones añadidas a la portada en la columna totalmente diluida: {SH_FD - SH:,.1f} M (v1: {SH_DIL_V1 - SH:,.0f} M)")

pr("\n=== CONTROLES v2 ===")
pr("(a) ROIC terminal base. ROIC A hist.: " + ", ".join(f"{y} {v:.1%}" for y, v in ROIC_A_HIST.items())
   + " | ROIC B: " + ", ".join(f"{y} {v:.1%}" for y, v in ROIC_B_HIST.items()))
pr(f"    mínimo ROIC A FY21-24 = {min(ROIC_A_HIST[y] for y in ['FY2021', 'FY2022', 'FY2023', 'FY2024']):.1%} ; WACC terminal {WACC_T:.2%} ; "
   f"diferencial del 12 % sobre WACC terminal {0.12 - WACC_T:+.2%}")
for lab, v, vps in ROIC_SENS:
    pr(f"    ROIC terminal {lab} ({(v if v is not None else WACC_T):.2%}): VPA base {vps:.2f} $ ({vps - B0['vps']:+.2f})")
pr(f"(b) W9 beta sectorial {BETA_BU:.2f} -> WACC0 {WACC0_SEC:.2%}: años 1-5 solo {W9_15:.2f} $ ({W9_15 - B0['vps']:+.2f}) | "
   f"desplazando también WACC terminal a {WACC_T + WACC0_SEC - WACC0:.2%}: {W9_SHIFT:.2f} $ ({W9_SHIFT - B0['vps']:+.2f}) | el modelo usa la beta mezclada")
pr(f"(c) Asimetría: I+D incremental 3T26 x4 {D_RD_ANUAL:,.0f} M$ ({D_RD_ANUAL / REV0_EX:.2%} de ingresos sin créditos); "
   f"SBC TTM - FY24 {D_SBC:,.0f} M$ ({D_SBC / REV0_EX:.2%})")
for lab, m0, nf, vps in ASYM_RES:
    pr(f"    {lab}: margen de partida {m0:.2%}, suelo capex {'no' if nf else 'sí'} -> VPA base {vps:.2f} $ ({vps - B0['vps']:+.2f})")
pr(f"(d) Capex bruto implícito año 1 (base) = reinversión {B0['rows'][0]['reinv']:,.0f} + D&A {DA_TTM:,.0f} = {CAPEX_Y1:,.0f} M$ ; "
   f"guía 2026 ~{CAPEX_GUIA_2026:,.0f} (T1) -> diferencia {CAPEX_GUIA_2026 - CAPEX_Y1:+,.0f} ; 4T26 implícito {CAPEX_GUIA_2026 - CAPEX_9M26:,.0f} ; sin Terafab")
pr(f"(e) Margen base {M_BASE:.2%}: margen bruto sin créditos TTM {GM_EX0:.2%} ; gastos operativos TTM {OPEX0:,.0f} M$ = {OPEX_R0:.2%} de ingresos sin créditos")
pr("    margen bruto sin créditos hist.: " + ", ".join(f"{y} {GM_EX_HIST[y]:.1%}" for y in YEARS)
   + " | opex/ingresos sin créd.: " + ", ".join(f"{y} {OPEX_R_HIST[y]:.1%}" for y in YEARS))
pr(f"    con margen bruto constante: opex/ingresos debe bajar a {OPEX_R_NEEDED:.2%} -> opex año 5 {OPEX5_NEEDED:,.0f} M$ ({OPEX5_NEEDED / OPEX0 - 1:+.1%} vs TTM; ingresos sin créd. año 5 {R5_EX:,.0f})")
pr(f"    con opex/ingresos constante: margen bruto sin créditos debe subir a {GM_NEEDED:.2%}")
pr(f"    margen de partida sin SBC extra ni I+D incremental: {M0_AMBOS:.2%} (frente al objetivo base {M_BASE:.2%})")
pr(f"(f) Energía: 9M26 {G_ENER_9M:+.1%} ; TTM vs FY25 ingresos {G_ENER_TTM:+.1%}, GWh {STOR_TTM:.1f} vs {STOR_FY25} ({G_GWH_TTM:+.1%}), ingreso/GWh {G_PRECIO_GWH:+.1%}")
pr(f"    ingreso/GWh FY25 {ENER_FY25 / STOR_FY25:,.1f} M$ ; TTM {ENER0 / STOR_TTM:,.1f} M$ (incluye solar y leasing: aproximación)")
pr(f"    combinaciones: +20 % GWh y -10 % ingreso/GWh = {1.2 * 0.9 - 1:+.1%} ; GWh TTM con ingreso/GWh TTM = {(1 + G_GWH_TTM) * (1 + G_PRECIO_GWH) - 1:+.1%}")
pr(f"(g) Fuera de la caja neta: SpaceX ~{SPACEX_FV_INF:,.0f} (inferencia: {SPACEX_COMPRA:,.0f} + {SPACEX_PLUSV:,.0f}) + activos digitales {DIGITAL:,.0f} "
   f"= {SPACEX_FV_INF + DIGITAL:,.0f} M$ = {NO_OPER_PS:.2f} $/acción")
pr("(h) DCF inverso con ventas/capital " + f"{STC_SW:.1f}x: " + "; ".join(
    f"margen {M:.0%} -> TACC {c_sw:.2%}" if c_sw is not None else f"margen {M:.0%} -> no alcanzable" for M, c_sw in REVERSE_SW))
pr(f"\nExcel escrito en {OUT_XLSX} ; {RECALC}")

# ---------------------------------------------------------------------------
# 10. v3: cifras del documento redondeadas UNA sola vez desde el valor completo (05-veredicto-v2 §2.1 M1/M2, §8 (e))
# Redondeo mitad hacia arriba con Decimal sobre repr(float) (no sobre una cifra ya redondeada a 2 decimales).
# 03-valoracion.md copia las cifras de la columna "texto" de data/cifras_03_redondeo.csv.
# ---------------------------------------------------------------------------
OUT_CIFRAS = os.path.join(BASE, "data", "cifras_03_redondeo.csv")


def red(x, d):
    """Redondeo mitad hacia arriba (en valor absoluto) a d decimales desde el valor completo."""
    q = Decimal(1).scaleb(-d) if d > 0 else Decimal(1)
    return Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP)


def txt(x, d):
    """Formato del documento: miles con punto, decimales con coma, signo menos tipográfico."""
    v = red(x, d)
    s_ = f"{abs(v):,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if v < 0 else "") + s_


CIFRAS = []


def cif(clave, seccion, valor, d, unidad=""):
    CIFRAS.append((clave, seccion, valor, d, unidad))


cif("beta_regresion", "§1 / §1.1", BETA_REG, 2, "x")
cif("beta_bottom_up", "§1.1", BETA_BU, 2, "x")
cif("beta_inicial", "§1.1", BETA0, 2, "x")
cif("beta_terminal", "§1.1", BETA_T, 2, "x")
cif("d_e", "§1.1", D_E * 100, 2, "%")
cif("w_d", "§1.1", W_D * 100, 2, "%")
cif("ke0", "§1.1", KE0 * 100, 2, "%")
cif("kd", "§1.1", KD * 100, 2, "%")
cif("wacc0", "§1.1 / §4", WACC0 * 100, 2, "%")
cif("wacc_t", "§1.1 / §2.2 / §4.3", WACC_T * 100, 2, "%")
for lab, b in (("solo_regresion", BETA_REG), ("solo_bottom_up", BETA_BU)):
    cif(f"wacc0_{lab}", "§1.1", ((RF + b * ERP) * (1 - W_D) + KD * W_D) * 100, 1, "%")
cif("roic12_menos_wacc_t", "§2.2", (0.12 - WACC_T) * 100, 1, "pp")
for k in ("bajista", "base", "alcista"):
    v = RES[k]
    last = v["rows"][-1]
    cif(f"{k}_ingresos_10", "§3", last["rev"], 0, "M$")
    cif(f"{k}_ebit_10", "§3", last["ebit"], 0, "M$")
    cif(f"{k}_vp_fcff", "§3", v["pv_sum"], 0, "M$")
    cif(f"{k}_vp_tv", "§3", v["pv_tv"], 0, "M$")
    cif(f"{k}_pct_tv", "§3", v["tv_share"] * 100, 0, "%")
    cif(f"{k}_ev", "§3", v["ev"], 0, "M$")
    cif(f"{k}_equity", "§3 / §5", v["eq"], 0, "M$")
    cif(f"{k}_vpa", "§0 / §3 / §8", v["vps"], 1, "$")
    cif(f"{k}_vpa_fd", "§0 / §3 / §8", RES_DIL[k], 1, "$")
    cif(f"{k}_vs_precio", "§3", (v["vps"] / PRICE - 1) * 100, 0, "%")
    gap = MCAP - v["eq"]
    cif(f"{k}_brecha", "§5", gap, 0, "M$")
    cif(f"{k}_brecha_pct", "§0 / §5", gap / MCAP * 100, 1, "%")
    cif(f"{k}_brecha_por_accion", "§5 / §6", gap / SH, 1, "$")
    cif(f"{k}_tacc_10", "§2.2", CAGR_SCEN[k] * 100, 1, "%")
for i, x in enumerate(B0["rows"]):
    cif(f"base_fcff_año{i + 1}", "§3", x["fcff"], 0, "M$")
for w, row in zip(W_GRID, SENS):
    for g, v in zip(G_GRID, row):
        cif(f"sens41_w{w * 100:.2f}_g{g * 100:.1f}", "§4.1", v, 1, "$")
for w in W_GRID:
    cif(f"sens41_fila_wacc_{w * 100:.2f}", "§4.1", w * 100, 2, "%")
for m, row in zip(M_GRID, SENS2):
    for gm, v in zip(GM_GRID, row):
        cif(f"sens42_m{m * 100:.0f}_x{gm}", "§4.2", v, 1, "$")
for lab, v, vps in ROIC_SENS:
    cif(f"roic_term_{lab.split(' ')[0]}", "§4.3 / §2.2 / §8", vps, 1, "$")
cif("w9_wacc0_sector", "§4.3", WACC0_SEC * 100, 2, "%")
cif("w9_vpa_años1_5", "§4.3 / §8", W9_15, 1, "$")
cif("w9_dif_años1_5", "§4.3", W9_15 - B0["vps"], 1, "$")
cif("w9_wacc_t_desplazado", "§4.3", (WACC_T + WACC0_SEC - WACC0) * 100, 2, "%")
cif("w9_vpa_desplazado", "§4.3 / §8", W9_SHIFT, 1, "$")
cif("w9_dif_desplazado", "§4.3", W9_SHIFT - B0["vps"], 1, "$")
for i, (lab, m0, nf, vps) in enumerate(ASYM_RES):
    cif(f"asim_{i}_vpa", "§6.3", vps, 1, "$")
    cif(f"asim_{i}_dif", "§6.3", vps - B0["vps"], 1, "$")
    cif(f"asim_{i}_margen0", "§6.3", m0 * 100, 2, "%")
for d in REVERSE:
    cif(f"inverso_m{d['M'] * 100:.0f}_tacc", "§5", d["c"] * 100, 1, "%")
    cif(f"inverso_m{d['M'] * 100:.0f}_ingresos10", "§5", d["rev10"], 0, "M$")
    cif(f"inverso_m{d['M'] * 100:.0f}_multiplo", "§5", d["rev10"] / REV0, 1, "x")
    cif(f"inverso_m{d['M'] * 100:.0f}_ebit10", "§5", d["ebit10"], 0, "M$")
for k, mm in REVERSE_M.items():
    if mm is not None:   # v3: con la beta 1,84, la TACC alcista justifica el precio con un margen de ~100 % (v2: ninguno)
        cif(f"inverso_margen_necesario_{k}", "§5", mm * 100, 1, "%")
for c_, M_, v in REV_COMBOS:
    cif(f"inverso_combo_c{c_ * 100:.0f}_m{M_ * 100:.0f}", "§5", v, 0, "$")
for M_, c_sw in REVERSE_SW:
    cif(f"inverso_sw_m{M_ * 100:.0f}_tacc", "§5", c_sw * 100, 1, "%")
    cif(f"inverso_sw_m{M_ * 100:.0f}_multiplo", "§5", (1 + c_sw) ** N, 1, "x")
for d in REVERSE:
    if d["M"] in (0.20, 0.25, 0.30):
        cif(f"inverso_m{d['M'] * 100:.0f}_vs_toyota", "§5", d["rev10"] / toyota_rev, 1, "x")
        cif(f"inverso_m{d['M'] * 100:.0f}_ebit_vs_ttm", "§5", d["ebit10"] / EBIT0, 0, "x")
        cif(f"inverso_m{d['M'] * 100:.0f}_capital_nuevo", "§5", (d["rev10"] - REV0) / STC_REV, 0, "M$")
cif("capex_y1", "§2.1", CAPEX_Y1, 0, "M$")
cif("reinv_y1", "§2.1", B0["rows"][0]["reinv"], 0, "M$")
cif("capex_y1_vs_guia", "§2.1", CAPEX_GUIA_2026 - CAPEX_Y1, 0, "M$")
cif("opex5_necesario", "§2.3", OPEX5_NEEDED, 0, "M$")
cif("opex5_vs_ttm", "§2.3", (OPEX5_NEEDED / OPEX0 - 1) * 100, 1, "%")
cif("tsla_ev_ventas", "§0 / §7", TSLA_EV_SALES, 1, "x")
cif("tsla_ev_ebitda", "§0 / §7", TSLA_EV_EBITDA, 0, "x")
cif("tsla_ev_ebit", "§0 / §7", TSLA_EV_EBIT, 0, "x")
cif("tsla_per", "§0 / §7", TSLA_PE, 0, "x")
cif("no_operativos_por_accion", "§6.4 / §8", NO_OPER_PS, 2, "$")

with open(OUT_CIFRAS, "w", newline="", encoding="utf-8") as f:
    w_ = csv.writer(f)
    w_.writerow(["clave", "seccion_03", "valor_completo", "decimales", "unidad", "texto"])
    for clave, sec, v, d, u in CIFRAS:
        w_.writerow([clave, sec, repr(float(v)), d, u, txt(v, d)])

# Aviso: cifras en las que redondear la salida a 2 decimales y luego a 1 daría otra cosa (el error de M1/M2)
_dobles = [(cl, v, d) for cl, _, v, d, _ in CIFRAS if d >= 1 and red(red(v, d + 1), d) != red(v, d)]
pr(f"\n=== CIFRAS DEL DOCUMENTO (v3, data/cifras_03_redondeo.csv: {len(CIFRAS)} cifras, redondeo único mitad hacia arriba) ===")
for cl, sec, v, d, u in CIFRAS:
    if not cl.startswith(("sens41_w", "sens42_", "inverso_combo", "base_fcff")):
        pr(f"  {cl:38s} {txt(v, d):>12s} {u}")
pr("  Cifras con riesgo de doble redondeo (re-redondear d+1 decimales daría otra cifra; usar el texto del CSV): "
   + ("; ".join(f"{cl} {txt(v, d)} (no {txt(red(v, d + 1), d + 1)} → {txt(red(red(v, d + 1), d), d)})" for cl, v, d in _dobles) or "ninguna"))
pr(f"Cifras escritas en {OUT_CIFRAS}")
