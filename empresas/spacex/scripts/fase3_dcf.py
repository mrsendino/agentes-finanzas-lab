#!/usr/bin/env python3
"""Fase 3 - SpaceX (SPCX): valoración por DCF (FCFF) por segmentos, escenarios, sensibilidad, DCF inverso y múltiplos.

Toda la aritmética se hace aquí. Los datos históricos NO se copian a mano: se leen de la Fase 2
(data/spacex_financials.csv vía fase2_ratios.load() y data/ratios.csv). Los datos de mercado (precio, tipo
libre de riesgo, ERP, betas y múltiplos de comparables) van en el diccionario MKT con su fuente y fecha.
La serie de cotizaciones para la beta de regresión se lee de data/precios_mercado_fase3.csv (Nasdaq.com).

Salida: data/dcf.xlsx (hojas Supuestos, Parametros, Esc_bajista, Esc_base, Esc_alcista, Sensibilidad,
DCF_inverso, Multiplos, Beta) y un resumen por pantalla. Las cifras de docs/03-valoracion.md se copian de esa salida.

Convenciones del modelo
- Año 0 = TTM a 30-sep-2026 (Fase 2). Años 1..10 = periodos de 12 meses desde oct-2026 (A1 = oct-26 a sep-27).
  El año 11 solo sirve para el valor terminal. Descuento a final de año.
- Por segmento (Space, Connectivity, SI) se proyecta un "run-rate" anualizado a fin de año (RR). Ingresos del año =
  w x RR(t-1) + (1 - w) x RR(t); w = 0,5 salvo SI en el año 1 de base/alcista (w = 0,25: la guía apunta a una subida
  concentrada en 4T26-1T27). RR0 = 3T26 x 4 en Connectivity y SI; en Space RR0 = TTM (ingresos trimestrales irregulares).
- Flujo libre para la empresa (FCFF) = EBITDA ajustado - SBC - impuestos - capex (variación de circulante = 0, supuesto).
  * La SBC se resta como coste real (equivale a pagarla en caja). Por eso NO se añade dilución futura por SBC.
  * Impuestos: 21 % sobre EBIT = EBITDA aj. - SBC - D&A, con compensación de pérdidas generadas desde el año 1.
    No se usan bases imponibles negativas previas (SIN VERIFICAR su importe).
- Capex, explícito por segmento (aquí está la normalización, no en el valor terminal):
  * Connectivity y SI: capex(t) = k x max(0, RR(t) - RR(t-1))  [crecimiento]  +  k x RR(t-1) / L  [reposición].
    k = capex por dólar de ingreso anual que aporta la capacidad nueva; L = vida útil. Cuando el crecimiento cae,
    el capex converge a k x (g + 1/L) x RR: esa es la normalización. k observado TTM se calcula en §1.
  * Space: capex / ingresos pasa linealmente del 116,6 % TTM al nivel normalizado del escenario en el año indicado
    (fin del desarrollo de Starship como infraestructura; SUPUESTO).
  * Año 1 de SI en el bajista: suelo de capex = compromisos no cancelables (P3, Note 16) aunque se pierda Customer B.
- D&A (solo afecta al impuesto): D&A 3T26 x 4 que se amortiza linealmente en L años + capex nuevo / L (medio año el
  primer año). Aproximación declarada.
- Valor terminal: FCFF del año 11 (mismas fórmulas, crecimiento g) / (WACC terminal - g).
- WACC: años 1-5 = WACC inicial; años 6-10 convergen linealmente al WACC terminal (beta a mitad de camino hacia 1).
- Valor de las acciones = EV + caja neta contable (Fase 2, 30-sep-2026) [- pago en caja pendiente a EchoStar en la
  base diluida]. Bases de acciones: portada 10-Q (A+B, no hay C), diluida (+ opciones/RSU + EchoStar) y sin las
  acciones restringidas de Musk (informativa).
"""
import csv
import math
import os
import shutil
import statistics
import subprocess
import sys
import tempfile

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import fase2_ratios as F2  # noqa: E402  (lee data/spacex_financials.csv; main() no se ejecuta al importar)

RATIOS = os.path.join(BASE, "data", "ratios.csv")
PRECIOS = os.path.join(BASE, "data", "precios_mercado_fase3.csv")
OUT_XLSX = os.path.join(BASE, "data", "dcf.xlsx")
f_m, f_p = F2.f_m, F2.f_p

# ---------------------------------------------------------------------------
# 1. Datos de Fase 2 (leídos, no copiados)
# ---------------------------------------------------------------------------
D, _, _ = F2.load()


def v(m, p="TTM_Q3_2026"):
    x = F2.g(D, m, p)
    assert x is not None, f"falta {m} {p} en spacex_financials.csv"
    return x


RAT = {}
with open(RATIOS, encoding="utf-8") as f:
    for row in csv.DictReader(f):
        RAT[(row["indicador"], row["periodo"])] = float(row["valor"])


def rat(ind, per):
    return RAT[(ind, per)]


SEGS = ("space", "connectivity", "si")
SEG_NOMBRE = {"space": "Space", "connectivity": "Connectivity", "si": "SI"}
REV0 = {s: v(f"ing_{s}") for s in SEGS}
REV_Q3 = {s: v(f"ing_{s}", "Q3_2026") for s in SEGS}
REV_Q3_25 = {s: v(f"ing_{s}", "Q3_2025") for s in SEGS}
EBITDA0 = {s: v(f"ebitda_aj_{s}") for s in SEGS}
CAPEX0 = {s: v(f"capex_{s}") for s in SEGS}
DA0 = {s: v(f"dya_{s}") for s in SEGS}
DA_Q3 = {s: v(f"dya_{s}", "Q3_2026") for s in SEGS}
SBC0 = {"space": v("sbc_space"), "connectivity": v("sbc_connectivity"),
        "si": v("sbc_si") + v("sbc_adquisiciones_si")}
SBC0_SI_ORD = v("sbc_si")
REV0_TOT = v("ingresos_totales")
assert abs(sum(REV0.values()) - REV0_TOT) < 1, "segmentos != total"
EBITDA0_TOT = v("ebitda_ajustado")
CAPEX0_TOT = v("capex")
FCO0 = v("flujo_caja_operativo")
FCF0 = rat("fcf", "TTM_Q3_2026")
EBIT0 = v("beneficio_operativo")
SBC0_TOT = rat("sbc_total", "TTM_Q3_2026")
CASH0 = rat("caja_y_valores", "9M2026")
DEBT0 = rat("deuda_contable", "9M2026")
NETCASH0 = CASH0 - DEBT0
assert abs(NETCASH0 + rat("deuda_neta_contable", "9M2026")) < 1
B_Q3 = rat("cliente_B_implicito", "Q3_2026")
B_RR0 = 4 * B_Q3
SI_SIN_B_NI_CURSOR_Q3 = rat("ing_si_sin_B_ni_cursor", "Q3_2026")
CURSOR_Q3 = v("ing_cursor", "Q3_2026")
CAPEX_SOBRE_ING_SPACE = {p: rat("capex_sobre_ingresos_space", p) for p in ("FY2023", "FY2024", "FY2025", "TTM_Q3_2026")}
M_EBITDA_SPACE_HIST = {p: v("ebitda_aj_space", p) / v("ing_space", p) for p in ("FY2023", "FY2024", "FY2025")}

# Acciones (Fase 2: portada del 10-Q 3T26, en acciones; opciones/RSU en M)
SH_A = v("acciones_A_portada_15oct2026", "9M2026") / 1e6
SH_B = v("acciones_B_portada_15oct2026", "9M2026") / 1e6
SH_C = v("acciones_clase_C", "9M2026")              # 0 tras la OPV (reclasificada a A)
SH_COVER = SH_A + SH_B + SH_C
OPC_RSU = v("opciones_vivas_clase_A", "9M2026") + v("opciones_vivas_clase_B", "9M2026") + v("rsu_vivas_clase_A", "9M2026")
PREMIOS_RENDIMIENTO = v("premios_rendimiento_no_cumplidos", "9M2026")

# Datos de Fase 1 / P2-P3 que no están en el CSV de Fase 2 (con fuente)
MUSK_RESTRINGIDAS = 1302.072285   # M acciones B: P2 "2026 Compensation Developments" / Note 21 F-60 (01 §4.1; 02 §7)
ECHOSTAR_ACC = 261.8              # M acciones A pendientes al cierre final del espectro (P3 MD&A; 01 §6.2, "≈")
ECHOSTAR_CAJA = 8500.0            # "hasta 8.500 M$" para deuda de EchoStar (P3 MD&A; 01 §1.3). SIN VERIFICAR si ya pagado
COMPROMISOS_NC = 37840.0          # compromisos no cancelables totales (P3 Note 16; 01 §4.5)
COMPROMISOS_2027 = 25569.0        # de ellos en 2027 (P3 Note 16; 01 §4.5)
CURSOR_SBC_PENDIENTE = 23376.0    # premios de Cursor pendientes de devengar (P3 Note 20; 01 §1.2)
CURSOR_VEST_ANIOS = 4             # SUPUESTO (SIN VERIFICAR): devengo lineal en 4 años
NAMEPLATE_GW = {"FY2025": 0.8, "Q3_2026": 1.7}   # P2 p. 27 y P3 Key Business Metrics (01 §1.1-1.2)
CAPEX_SI_9M26 = v("capex_si", "9M2026")
CAPEX_POR_W = CAPEX_SI_9M26 / ((NAMEPLATE_GW["Q3_2026"] - NAMEPLATE_GW["FY2025"]) * 1000)  # $/W (cota alta: incluye obra en curso)
CUPON_NOTES = 0.05855             # cupón medio ponderado de los 25.000 M$ SpaceX Notes (P9; 01 §6.1)

# ---------------------------------------------------------------------------
# 2. Datos de mercado (fuente + fecha)
# ---------------------------------------------------------------------------
MKT = {
    "precio": (147.49, "USD", "Cierre SPCX 23-oct-2026 (viernes; último cierre antes del 25-oct). Nasdaq.com, histórico "
               "(api.nasdaq.com/api/quote/SPCX/historical): close 147,49, open 147,93, máx 149,75, mín 144,085. "
               "Coincide con stockanalysis.com (147,49) y digrin.com. No es fuente SEC: dato de mercado del propio Nasdaq"),
    "rf": (0.0500, "%", "U.S. Treasury, Daily Treasury Par Yield Curve Rates, 10 Yr = 5,00 % el 23-oct-2026 "
           "(home.treasury.gov). 30 Yr = 5,33 %"),
    "erp": (0.0420, "%", "Damodaran, ERP implícito S&P 500 a 1-oct-2026 = 4,20 % ('Trailing 12 month, with adjusted payout'), "
            "pages.stern.nyu.edu/~adamodar (home page), consultado 25-oct-2026"),
    "tax": (0.21, "%", "Tipo federal EE. UU. normativo (SUPUESTO; tipo efectivo de SpaceX no representativo por pérdidas)"),
    "kd": (CUPON_NOTES, "%", "Cupón medio ponderado 5,855 % de los 25.000 M$ SpaceX Notes 2031-2056 (P9, 8-K jun-2026; 01 §6.1)"),
    # Guía de la dirección en la call del 3T26 (20-oct-2026): SOLO SECUNDARIA, SIN VERIFICAR contra transcripción
    "guia_ing_1T27_bajo": (33000.0, "M USD", "Earnings Whispers vía finviz.com/news/405179 (20-oct-2026): ingresos 1T27 33.000-37.000 M$. SECUNDARIA, SIN VERIFICAR"),
    "guia_ing_1T27_alto": (37000.0, "M USD", "Ídem"),
    "guia_capex_4T26_bajo": (35000.0, "M USD", "Ídem: capex 4T26 35.000-40.000 M$. SECUNDARIA, SIN VERIFICAR"),
    "guia_capex_4T26_alto": (40000.0, "M USD", "Ídem"),
}
PRICE = MKT["precio"][0]
RF, ERP, TAX, KD_PRE = MKT["rf"][0], MKT["erp"][0], MKT["tax"][0], MKT["kd"][0]

# Betas de Damodaran (EE. UU., ene-2026): beta desapalancada corregida por caja
DAMO = {
    "Aerospace/Defense": (0.87, 79), "Telecom (Wireless)": (0.39, 12), "Telecom. Services": (0.38, 39),
    "Software (System & Application)": (1.25, 309), "Computer Services": (0.96, 64), "Semiconductor": (1.50, 66),
}
DAMO_SRC = "Damodaran, Betas by Sector (US), datos ene-2026, pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html (consultado 25-oct-2026)"
DAMO_SEG = {"space": ["Aerospace/Defense"], "connectivity": ["Telecom (Wireless)"],
            "si": ["Software (System & Application)", "Computer Services"]}

# Comparables: stockanalysis.com /stocks/<t>/statistics, precio de cierre 23-oct-2026, página actualizada 25-oct-2026.
# (ticker, nombre, grupo/segmento, precio, mcap M$, EV M$, EV/Ventas, EV/EBITDA, EV/EBIT, PER, beta 5a, deuda M$)
# None = n/a en la fuente (EBITDA o beneficio negativos) o no publicado.
PEERS = [
    ("RKLB", "Rocket Lab", "space", 52.60, 31480, 29230, 38.00, None, None, None, 2.94, 133.69),
    ("FLY", "Firefly Aerospace", "space", 18.23, 3050, 2470, 8.61, None, None, None, None, None),
    ("IRDM", "Iridium", "connectivity", 44.40, 4710, 6800, 7.53, 17.25, 39.60, 29.14, 0.85, 2180),
    ("VSAT", "Viasat", "connectivity", 61.47, 8470, 13660, 2.95, 9.81, 132.48, None, 1.76, 6930),
    ("ASTS", "AST SpaceMobile", "connectivity", 39.79, 15480, 16190, 140.42, None, None, None, 2.71, 2990),
    ("CRWV", "CoreWeave", "si", 54.24, 29910, 75940, 10.01, 20.04, None, None, None, 51610),
    ("NBIS", "Nebius", "si", 158.74, 43510, 45660, 33.70, 176.99, None, 966.38, 1.46, 10200),
    ("ORCL", "Oracle", "si", 126.16, 382450, 514520, 7.17, 14.94, 20.92, 19.78, 1.77, 169140),
    ("MSFT", "Microsoft", "si", 524.51, 3900000, 3950000, 11.89, 20.32, 25.43, 29.22, 1.10, None),
]
PEERS_SRC = "stockanalysis.com/stocks/<ticker>/statistics, cierre 23-oct-2026 (página actualizada 25-oct-2026). SECUNDARIA"
SPCX_3RD = ("stockanalysis.com/stocks/spcx/statistics (23-oct-2026): capitalización 2,00 bill. $, EV 1,95 bill. $, "
            "EV/Ventas 60,93, EV/EBITDA 166,36 (con un EBITDA TTM de 11.740 M$, definición distinta del EBITDA ajustado)")

# ---------------------------------------------------------------------------
# 3. Mercado, acciones y beta
# ---------------------------------------------------------------------------
MCAP = PRICE * SH_COVER
EV_MKT = MCAP - NETCASH0
D_E = DEBT0 / MCAP
W_D = DEBT0 / (DEBT0 + MCAP)

SH_DIL = SH_COVER + OPC_RSU + ECHOSTAR_ACC           # base principal de valor por acción
SH_SIN_MUSK = SH_COVER - MUSK_RESTRINGIDAS           # informativa
SH_BASES = {"portada": SH_COVER, "diluida": SH_DIL, "sin_musk": SH_SIN_MUSK}
EQ_AJUSTE = {"portada": 0.0, "diluida": -ECHOSTAR_CAJA, "sin_musk": 0.0}

# 3.1 Beta de regresión de SPCX (informativa: ~4 meses de datos)
PX = []
with open(PRECIOS, encoding="utf-8") as f:
    for row in csv.DictReader(f):
        PX.append((row["fecha"], float(row["spcx_cierre"]), float(row["spy_cierre"]), float(row["qqq_cierre"])))
PX.sort()


def _beta(ys, xs):
    mx, my = statistics.mean(xs), statistics.mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    var = sum((x - mx) ** 2 for x in xs)
    b = cov / var
    resid = [y - my - b * (x - mx) for x, y in zip(xs, ys)]
    se = math.sqrt(sum(e * e for e in resid) / (len(xs) - 2) / var)
    return b, se


def _rets(i0=0):
    sel = PX[i0:]
    return ([sel[i][1] / sel[i - 1][1] - 1 for i in range(1, len(sel))],
            [sel[i][2] / sel[i - 1][2] - 1 for i in range(1, len(sel))],
            [sel[i][3] / sel[i - 1][3] - 1 for i in range(1, len(sel))])


R_SPCX, R_SPY, R_QQQ = _rets()
BETA_REG_SPY, SE_SPY = _beta(R_SPCX, R_SPY)
BETA_REG_QQQ, SE_QQQ = _beta(R_SPCX, R_QQQ)
R_SPCX5, R_SPY5, _ = _rets(5)                       # sin la primera semana (efecto salida a bolsa)
BETA_REG_SPY_X1S, SE_SPY_X1S = _beta(R_SPCX5, R_SPY5)
N_OBS = len(R_SPCX)
BETA_BLUME = 0.67 * BETA_REG_SPY + 0.33
VOL_SPCX = statistics.stdev(R_SPCX) * math.sqrt(252)
VOL_SPY = statistics.stdev(R_SPY) * math.sqrt(252)


# 3.2 Beta "bottom-up" por segmento: media de (a) Damodaran sector y (b) mediana de comparables desapalancados
def unlever(b, debt, mcap):
    return b / (1 + (1 - TAX) * debt / mcap)


PEER_BU = {p[0]: unlever(p[10], p[11], p[4]) for p in PEERS if p[10] is not None and p[11] is not None}
BU_SEG = {}
for s in SEGS:
    damo = statistics.mean(DAMO[k][0] for k in DAMO_SEG[s])
    peers = [PEER_BU[p[0]] for p in PEERS if p[2] == s and p[0] in PEER_BU]
    pm = statistics.median(peers)
    BU_SEG[s] = dict(damo=damo, peers=pm, n=len(peers), bu=(damo + pm) / 2)

N = 10
YEARS = list(range(1, N + 2))   # 1..11 (11 = año del valor terminal)


# ---------------------------------------------------------------------------
# 4. Supuestos por escenario
# ---------------------------------------------------------------------------
def k_observado(s, L):
    """k implícito TTM: capex TTM = k x (ΔRR 3T25->3T26 + RR 3T25 / L)."""
    rr0, rr_1 = 4 * REV_Q3[s], 4 * REV_Q3_25[s]
    return CAPEX0[s] / ((rr0 - rr_1) + rr_1 / L)


L_SEG = {"space": 10, "connectivity": 5, "si": 5}      # vidas útiles: SUPUESTO (SIN VERIFICAR políticas contables)
K_OBS = {s: k_observado(s, L_SEG[s]) for s in ("connectivity", "si")}
RR0 = {"space": REV0["space"], "connectivity": 4 * REV_Q3["connectivity"], "si": 4 * REV_Q3["si"]}
SI_SIN_B_RR0 = RR0["si"] - B_RR0
# Run-rate de SI que implica la guía de ingresos del 1T27 (grupo) si Space + Connectivity siguen al nivel del 3T26
OTROS_Q3 = REV_Q3["space"] + REV_Q3["connectivity"]
GUIA_SI_RR = {"bajo": 4 * (MKT["guia_ing_1T27_bajo"][0] - OTROS_Q3),
              "medio": 4 * ((MKT["guia_ing_1T27_bajo"][0] + MKT["guia_ing_1T27_alto"][0]) / 2 - OTROS_Q3)}

SCEN = {
    "bajista": dict(
        g_term=0.025,
        space=dict(g1=0.00, gmid=[0.03] * 4, m_obj=0.05, anio_m=5, sbc_obj=0.10, capex_norm=0.50, anio_norm=6),
        connectivity=dict(g1=0.15, gmid=[0.08] * 4, m_obj=0.55, anio_m=3, sbc_obj=None, k=0.60),
        si=dict(b="rescinde", reventa_b=0.50, g1_sin_b=0.30, credito_guia=0.0, guia="bajo", w1=0.5,
                gmid=[0.20, 0.15, 0.12, 0.10], m_obj=0.30, anio_m=3, sbc_obj=0.10, k=round(K_OBS["si"], 2),
                suelo_capex1=COMPROMISOS_NC, recorte_b_a3=0.0),
        nota="Customer B rescinde en el año 1 (preaviso de 90 días) y su capacidad se recoloca al 50 %; sin crédito a la guía "
             "secundaria; Starlink se desacelera (ARPU a la baja); Starship no se monetiza fuera de Starlink; k de SI = observado TTM.",
    ),
    "base": dict(
        g_term=0.030,
        space=dict(g1=0.05, gmid=[0.10] * 4, m_obj=0.20, anio_m=5, sbc_obj=0.08, capex_norm=0.35, anio_norm=4),
        connectivity=dict(g1=0.30, gmid=[0.15] * 4, m_obj=0.62, anio_m=3, sbc_obj=None, k=round(K_OBS["connectivity"], 2)),
        si=dict(b="sigue", reventa_b=None, g1_sin_b=None, credito_guia=0.5, guia="bajo", w1=0.25,
                gmid=[0.30, 0.20, 0.15, 0.12], m_obj=0.50, anio_m=3, sbc_obj=0.07, k=1.25,
                suelo_capex1=None, recorte_b_a3=0.30),
        nota="Customer B sigue hasta mayo-2029 y renueva con un recorte de precio del 30 % (año 3); SI recibe el 50 % del aumento "
             "que implica el extremo bajo de la guía del 1T27; Starlink mantiene un crecimiento alto que se modera; margen de SI "
             "en línea con CoreWeave.",
    ),
    "alcista": dict(
        g_term=0.035,
        space=dict(g1=0.10, gmid=[0.25] * 4, m_obj=0.30, anio_m=5, sbc_obj=0.06, capex_norm=0.25, anio_norm=3),
        connectivity=dict(g1=0.40, gmid=[0.22] * 4, m_obj=0.65, anio_m=3, sbc_obj=None, k=0.40),
        si=dict(b="sigue", reventa_b=None, g1_sin_b=None, credito_guia=1.0, guia="medio", w1=0.25,
                gmid=[0.40, 0.30, 0.20, 0.15], m_obj=0.60, anio_m=3, sbc_obj=0.05, k=0.90,
                suelo_capex1=None, recorte_b_a3=0.0),
        nota="Se cumple el punto medio de la guía del 1T27; Customer B renueva sin recorte; Starship comercial y Starlink Mobile "
             "sostienen el crecimiento; k de SI coherente con >50 $/W de ingreso citado en la call (secundaria).",
    ),
}


def growth_path(g1, gmid, g_term):
    gs = [g1] + list(gmid)
    g5 = gs[4]
    for t in range(6, N + 1):
        gs.append(g5 + (g_term - g5) * (t - 5) / 5)
    gs.append(g_term)  # año 11
    return gs


def lin(x0, x1, t, anio):
    return x0 + (x1 - x0) * min(t, anio) / anio


def da_path(da_q3, capex, L):
    out = []
    for t in YEARS:
        old = 4 * da_q3 * max(0.0, 1 - (t - 1) / L)
        new = sum(capex[s - 1] / L for s in range(max(1, t - L + 1), t)) + capex[t - 1] / (2 * L)
        out.append(old + new)
    return out


def proj_segment(s, p, g_term):
    """Devuelve dict de listas (años 1..11) para un segmento."""
    rr_prev = RR0[s]
    rr, rev = [], []
    if s == "si":
        gs = growth_path(0.0, p["gmid"], g_term)
        for t in YEARS:
            if t == 1:
                if p["b"] == "rescinde":
                    r1 = SI_SIN_B_RR0 * (1 + p["g1_sin_b"]) + B_RR0 * p["reventa_b"]
                else:
                    r1 = RR0["si"] + p["credito_guia"] * (GUIA_SI_RR[p["guia"]] - RR0["si"])
                rr_t = r1
                w = p["w1"]
            else:
                rr_t = rr_prev * (1 + gs[t - 1])
                if t == 3 and p["recorte_b_a3"]:
                    rr_t -= p["recorte_b_a3"] * B_RR0
                w = 0.5
            rev.append(w * rr_prev + (1 - w) * rr_t)
            rr.append(rr_t)
            rr_prev = rr_t
    else:
        gs = growth_path(p["g1"], p["gmid"], g_term)
        for t in YEARS:
            rr_t = rr_prev * (1 + gs[t - 1])
            rev.append(0.5 * rr_prev + 0.5 * rr_t)
            rr.append(rr_t)
            rr_prev = rr_t
    m0 = EBITDA0[s] / REV0[s]
    marg = [lin(m0, p["m_obj"], t, p["anio_m"]) for t in YEARS]
    ebitda = [m * r for m, r in zip(marg, rev)]
    if s == "si":
        sbc0 = SBC0_SI_ORD / REV0[s]
        sbc_pct = [lin(sbc0, p["sbc_obj"], t, 5) for t in YEARS]
        sbc = [x * r + (CURSOR_SBC_PENDIENTE / CURSOR_VEST_ANIOS if t <= CURSOR_VEST_ANIOS else 0.0)
               for x, r, t in zip(sbc_pct, rev, YEARS)]
    else:
        sbc0 = SBC0[s] / REV0[s]
        obj = sbc0 if p["sbc_obj"] is None else p["sbc_obj"]
        sbc_pct = [lin(sbc0, obj, t, 5) for t in YEARS]
        sbc = [x * r for x, r in zip(sbc_pct, rev)]
    L = L_SEG[s]
    capex = []
    if s == "space":
        c0 = CAPEX0[s] / REV0[s]
        cp = [lin(c0, p["capex_norm"], t, p["anio_norm"]) for t in YEARS]
        capex = [c * r for c, r in zip(cp, rev)]
    else:
        k = p["k"]
        prev = RR0[s]
        for i, t in enumerate(YEARS):
            c = k * max(0.0, rr[i] - prev) + k * prev / L
            if s == "si" and t == 1 and p.get("suelo_capex1"):
                c = max(c, p["suelo_capex1"])
            capex.append(c)
            prev = rr[i]
    da = da_path(DA_Q3[s], capex, L)
    ebit = [e - b - d for e, b, d in zip(ebitda, sbc, da)]
    return dict(rr=rr, rev=rev, marg=marg, ebitda=ebitda, sbc=sbc, capex=capex, da=da, ebit=ebit,
                g=[rr[0] / RR0[s] - 1] + [rr[i] / rr[i - 1] - 1 for i in range(1, len(rr))])


def project(sc):
    segs = {s: proj_segment(s, sc[s], sc["g_term"]) for s in SEGS}
    tot = {k: [sum(segs[s][k][i] for s in SEGS) for i in range(len(YEARS))]
           for k in ("rev", "ebitda", "sbc", "capex", "da", "ebit")}
    nol, tax = 0.0, []
    for i, t in enumerate(YEARS):
        e = tot["ebit"][i]
        if t == 11:
            tax.append(TAX * max(0.0, e))      # perpetuidad: sin pérdidas pendientes (supuesto conservador)
            continue
        if e < 0:
            nol += -e
            tax.append(0.0)
        else:
            used = min(nol, e)
            nol -= used
            tax.append(TAX * (e - used))
    tot["tax"] = tax
    tot["fcff"] = [tot["ebitda"][i] - tot["sbc"][i] - tax[i] - tot["capex"][i] for i in range(len(YEARS))]
    return segs, tot


# ---------------------------------------------------------------------------
# 5. WACC (pesos de los segmentos = ingresos del año 1 del caso base)
# ---------------------------------------------------------------------------
_SEGS_B, _TOT_B = project(SCEN["base"])
W_SEG = {s: _SEGS_B[s]["rev"][0] / _TOT_B["rev"][0] for s in SEGS}
BETA_U = sum(W_SEG[s] * BU_SEG[s]["bu"] for s in SEGS)
BETA0 = BETA_U * (1 + (1 - TAX) * D_E)
BETA_T = (BETA0 + 1.0) / 2
KE0 = RF + BETA0 * ERP
KE_T = RF + BETA_T * ERP
KD = KD_PRE * (1 - TAX)
WACC0 = KE0 * (1 - W_D) + KD * W_D
WACC_T = KE_T * (1 - W_D) + KD * W_D
WACC_ALT = {lab: (RF + b * (1 + (1 - TAX) * D_E) * ERP) * (1 - W_D) + KD * W_D for lab, b in (
    ("solo Damodaran (ponderada)", sum(W_SEG[s] * BU_SEG[s]["damo"] for s in SEGS)),
    ("solo comparables (ponderada)", sum(W_SEG[s] * BU_SEG[s]["peers"] for s in SEGS)),
)}
WACC_ALT["regresión SPCX vs SPY (Blume)"] = (RF + BETA_BLUME * ERP) * (1 - W_D) + KD * W_D


def wacc_path(w0, wt):
    return [w0 if t <= 5 else w0 + (wt - w0) * (t - 5) / 5 for t in range(1, N + 1)]


def run_dcf(sc, w0=None, wt=None, g_term=None, base="diluida"):
    w0 = WACC0 if w0 is None else w0
    wt = WACC_T if wt is None else wt
    if g_term is not None:
        sc = dict(sc, g_term=g_term)
    segs, tot = project(sc)
    g = sc["g_term"]
    wp = wacc_path(w0, wt)
    df, dfs, pvs = 1.0, [], []
    for t in range(N):
        df /= 1 + wp[t]
        dfs.append(df)
        pvs.append(tot["fcff"][t] * df)
    fcff11 = tot["fcff"][N]
    tv = fcff11 / (wt - g)
    pv_tv = tv * dfs[-1]
    pv_sum = sum(pvs)
    ev = pv_sum + pv_tv
    out = dict(segs=segs, tot=tot, wp=wp, dfs=dfs, pvs=pvs, pv_sum=pv_sum, tv=tv, pv_tv=pv_tv, ev=ev,
               fcff11=fcff11, tv_share=pv_tv / ev if ev else None, g=g)
    for b, sh in SH_BASES.items():
        eq = ev + NETCASH0 + EQ_AJUSTE[b]
        out[f"eq_{b}"] = eq
        out[f"vps_{b}"] = eq / sh
    out["vps"] = out[f"vps_{base}"]
    # año en que el FCFF pasa a ser positivo y FCFF acumulado mínimo (necesidad de caja)
    cum, cmin, first_pos = 0.0, 0.0, None
    for t in range(N):
        cum += tot["fcff"][t]
        cmin = min(cmin, cum)
        if first_pos is None and tot["fcff"][t] > 0:
            first_pos = t + 1
    out["fcff_acum_min"], out["anio_fcff_pos"] = cmin, first_pos
    return out


RES = {k: run_dcf(s) for k, s in SCEN.items()}

# ---------------------------------------------------------------------------
# 6. Sensibilidades
# ---------------------------------------------------------------------------
W_GRID = [WACC0 + d for d in (-0.02, -0.01, 0.0, 0.01, 0.02, 0.03)]
G_GRID = [0.02, 0.025, 0.03, 0.035, 0.04]
SENS = {k: [[run_dcf(SCEN[k], w0=w, wt=WACC_T + (w - WACC0), g_term=g)["vps"] for g in G_GRID] for w in W_GRID]
        for k in SCEN}


def base_var(**mods):
    sc = {k: (dict(v_) if isinstance(v_, dict) else v_) for k, v_ in SCEN["base"].items()}
    for path, val in mods.items():
        seg, key = path.split("__")
        sc[seg][key] = val
    return sc


# Customer B y otros motores (caso base)
B_SENS = [
    ("Base", run_dcf(SCEN["base"])["vps"]),
    ("Base, pero Customer B rescinde en el año 1 (recolocación 50 %)",
     run_dcf(base_var(si__b="rescinde", si__reventa_b=0.5, si__g1_sin_b=0.30, si__credito_guia=0.0, si__w1=0.5,
                      si__suelo_capex1=COMPROMISOS_NC, si__recorte_b_a3=0.0))["vps"]),
    None,  # se rellena abajo (B rescinde, pero se mantiene el resto del aumento de la guía)
    ("Base sin crédito a la guía secundaria (B sigue)", run_dcf(base_var(si__credito_guia=0.0, si__w1=0.5))["vps"]),
    ("Base sin recorte de precio de B en la renovación", run_dcf(base_var(si__recorte_b_a3=0.0))["vps"]),
    ("Base con recorte de B del 60 % en la renovación", run_dcf(base_var(si__recorte_b_a3=0.60))["vps"]),
]


# "B rescinde pero el resto de la guía se cumple al 50 %": RR1 = (RR de la guía con 50 %) - B + 50 % de recolocación
def _rr1_b_rescinde_guia():
    rr1_base = RR0["si"] + 0.5 * (GUIA_SI_RR["bajo"] - RR0["si"])
    return rr1_base - B_RR0 * (1 - 0.5)


_sc = base_var(si__credito_guia=0.0, si__recorte_b_a3=0.0)
_sc["si"]["credito_guia"] = (_rr1_b_rescinde_guia() - RR0["si"]) / (GUIA_SI_RR["bajo"] - RR0["si"])
B_SENS[2] = ("Base, Customer B rescinde en el año 1 pero el resto del aumento de la guía (50 %) se mantiene",
             run_dcf(_sc)["vps"])
B_VALOR_BASE = B_SENS[0][1] - B_SENS[1][1]

DRIVERS = [
    ("k de SI = 1,0 / 1,25 (base) / k observado TTM", [run_dcf(base_var(si__k=x))["vps"] for x in (1.0, 1.25, round(K_OBS["si"], 2))]),
    ("Margen EBITDA aj. objetivo SI = 40 % / 50 % / 60 %", [run_dcf(base_var(si__m_obj=x))["vps"] for x in (0.40, 0.50, 0.60)]),
    ("Crédito a la guía del 1T27 = 0 % / 50 % / 100 % (extremo bajo)", [run_dcf(base_var(si__credito_guia=x, si__w1=(0.5 if x == 0 else 0.25)))["vps"] for x in (0.0, 0.5, 1.0)]),
    ("Crecimiento SI años 2-5 x 0,5 / x 1 / x 1,5", [run_dcf(base_var(si__gmid=[g * x for g in SCEN["base"]["si"]["gmid"]]))["vps"] for x in (0.5, 1.0, 1.5)]),
    ("Margen EBITDA aj. objetivo Connectivity = 55 % / 62 % / 65 %", [run_dcf(base_var(connectivity__m_obj=x))["vps"] for x in (0.55, 0.62, 0.65)]),
    ("Capex normalizado Space = 50 % / 35 % / 25 % de ingresos", [run_dcf(base_var(space__capex_norm=x))["vps"] for x in (0.50, 0.35, 0.25)]),
]
# Capex del año 1 al ritmo de la guía del 4T26 (punto medio x 4, parte de SI = peso de SI en el capex del 3T26),
# sin más ingresos que los del caso base
SI_PESO_CAPEX_Q3 = v("capex_si", "Q3_2026") / (v("capex_space", "Q3_2026") + v("capex_connectivity", "Q3_2026") + v("capex_si", "Q3_2026"))
CAPEX_SI_A1_GUIA = 4 * (MKT["guia_capex_4T26_bajo"][0] + MKT["guia_capex_4T26_alto"][0]) / 2 * SI_PESO_CAPEX_Q3
VPS_CAPEX_GUIA = run_dcf(base_var(si__suelo_capex1=CAPEX_SI_A1_GUIA))["vps"]
# Bajista con disciplina de capital: SI deja de crecer tras el año 1 (solo reposición)
VPS_BAJISTA_SIN_CREC_SI = run_dcf(dict(SCEN["bajista"], si=dict(SCEN["bajista"]["si"], gmid=[0.0] * 4)))["vps"]
# WACC alternativos sobre el caso base (WACC terminal desplazado igual)
WACC_ALT_VPS = {lab: run_dcf(SCEN["base"], w0=w, wt=WACC_T + (w - WACC0))["vps"] for lab, w in WACC_ALT.items()}
# Vida útil de SI (afecta a reposición y D&A)
_L_ORIG = L_SEG["si"]
L_SENS = []
for L in (4, 5, 6):
    L_SEG["si"] = L
    L_SENS.append((L, run_dcf(SCEN["base"])["vps"]))
L_SEG["si"] = _L_ORIG

# ---------------------------------------------------------------------------
# 7. DCF inverso (sobre la base diluida)
# ---------------------------------------------------------------------------
def solve(fun, lo, hi, target, it=200):
    flo, fhi = fun(lo) - target, fun(hi) - target
    if flo * fhi > 0:
        return None
    for _ in range(it):
        mid = (lo + hi) / 2
        fm = fun(mid) - target
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2


def _scale_growth(x):
    sc = base_var()
    for s in SEGS:
        sc[s]["gmid"] = [g * x for g in SCEN["base"][s]["gmid"]]
    return sc


REV_LAMBDA = solve(lambda x: run_dcf(_scale_growth(x))["vps"], 0.0, 5.0, PRICE)
REV_LAMBDA_RES = run_dcf(_scale_growth(REV_LAMBDA)) if REV_LAMBDA else None
REV_MARGIN_SI = solve(lambda m: run_dcf(base_var(si__m_obj=m))["vps"], 0.0, 0.95, PRICE)
REV_K_SI = solve(lambda k: run_dcf(base_var(si__k=k))["vps"], 0.05, 3.0, PRICE)
REV_GUIA = solve(lambda c: run_dcf(base_var(si__credito_guia=c))["vps"], 0.0, 5.0, PRICE)
REV_WACC_LO = WACC0 - WACC_T + SCEN["base"]["g_term"] + 0.0025   # el WACC terminal desplazado debe quedar > g
REV_WACC = solve(lambda w: run_dcf(SCEN["base"], w0=w, wt=WACC_T + (w - WACC0))["vps"], REV_WACC_LO, 0.20, PRICE)
REV_EXTREMOS = {
    "margen SI 95 %": run_dcf(base_var(si__m_obj=0.95))["vps"],
    "k SI 0,05": run_dcf(base_var(si__k=0.05))["vps"],
    "crédito guía x5": run_dcf(base_var(si__credito_guia=5.0))["vps"],
    f"WACC0 {f_p(REV_WACC_LO, 2)} (mínimo con WACC_T > g)": run_dcf(SCEN["base"], w0=REV_WACC_LO, wt=WACC_T + (REV_WACC_LO - WACC0))["vps"],
}


def _scale_growth_bull(x):
    sc = {k: (dict(v_) if isinstance(v_, dict) else v_) for k, v_ in SCEN["alcista"].items()}
    for s in SEGS:
        sc[s]["gmid"] = [g * x for g in SCEN["alcista"][s]["gmid"]]
    return sc


REV_LAMBDA_BULL = solve(lambda x: run_dcf(_scale_growth_bull(x))["vps"], 0.0, 5.0, PRICE)
REV_LAMBDA_BULL_RES = run_dcf(_scale_growth_bull(REV_LAMBDA_BULL)) if REV_LAMBDA_BULL else None
REV_MARGIN_SI_BULL = solve(lambda m: run_dcf(dict(SCEN["alcista"], si=dict(SCEN["alcista"]["si"], m_obj=m)))["vps"], 0.0, 0.95, PRICE)


def _cagr(res, key="rev"):
    return (res["tot"][key][N - 1] / REV0_TOT) ** (1 / N) - 1


CAGR = {k: _cagr(r_) for k, r_ in RES.items()}

# ---------------------------------------------------------------------------
# 8. Múltiplos
# ---------------------------------------------------------------------------
RR0_TOT = sum(RR0.values())
EBITDA_Q3 = v("ebitda_ajustado", "Q3_2026")
SPCX_MULT = {
    "EV/Ventas TTM": EV_MKT / REV0_TOT,
    "EV/Ventas 3T26 x 4": EV_MKT / (4 * v("ingresos_totales", "Q3_2026")),
    "EV/EBITDA aj. TTM": EV_MKT / EBITDA0_TOT,
    "EV/EBITDA aj. 3T26 x 4": EV_MKT / (4 * EBITDA_Q3),
    "EV/(EBITDA aj. - SBC) TTM": EV_MKT / (EBITDA0_TOT - SBC0_TOT),
    "EV/EBIT TTM": None if EBIT0 <= 0 else EV_MKT / EBIT0,
    "Capitalización / FCF TTM": None if FCF0 <= 0 else MCAP / FCF0,
}


def med(seg, idx):
    vals = [p[idx] for p in PEERS if p[2] == seg and p[idx] is not None]
    return (statistics.median(vals), len(vals)) if vals else (None, 0)


MED = {s: {"ev_sales": med(s, 6), "ev_ebitda": med(s, 7)} for s in SEGS}
# Suma de partes por múltiplos: EV/Ventas TTM de cada grupo x ingresos TTM del segmento; EV/EBITDA donde hay mediana
SOTP_SALES = {s: MED[s]["ev_sales"][0] * REV0[s] for s in SEGS}
SOTP_SALES_RR = {s: MED[s]["ev_sales"][0] * RR0[s] for s in SEGS}
SOTP_EBITDA = {s: (MED[s]["ev_ebitda"][0] * EBITDA0[s] if MED[s]["ev_ebitda"][0] and EBITDA0[s] > 0 else None) for s in SEGS}


def _vps_from_ev(ev):
    return (ev + NETCASH0 + EQ_AJUSTE["diluida"]) / SH_DIL


SOTP = {
    "EV/Ventas TTM": sum(SOTP_SALES.values()),
    "EV/Ventas run-rate (3T26 x 4; Space TTM)": sum(SOTP_SALES_RR.values()),
}
SOTP_EBITDA_MIX = sum((SOTP_EBITDA[s] if SOTP_EBITDA[s] is not None else SOTP_SALES[s]) for s in SEGS)
SOTP["EV/EBITDA aj. TTM (Space por EV/Ventas)"] = SOTP_EBITDA_MIX

# Controles internos
CHECKS = []


def chk(nombre, ok):
    CHECKS.append((nombre, ok))


chk("segmentos TTM suman el total", abs(sum(REV0.values()) - REV0_TOT) < 1)
chk("capex TTM segmentos = capex consolidado", abs(sum(CAPEX0.values()) - CAPEX0_TOT) < 2)
chk("EBITDA aj. TTM segmentos = consolidado", abs(sum(EBITDA0.values()) - EBITDA0_TOT) < 2)
chk("acciones portada A+B = 13.581,06 M (Fase 1/2)", abs(SH_COVER - 13581.063709) < 0.001)
chk("orden de escenarios bajista < base < alcista", RES["bajista"]["vps"] < RES["base"]["vps"] < RES["alcista"]["vps"])
chk("WACC terminal > g en todos los escenarios", all(WACC_T > s["g_term"] for s in SCEN.values()))
chk("g terminal < tipo libre de riesgo", all(s["g_term"] < RF for s in SCEN.values()))
chk("sensibilidad: valor central = base", abs(SENS["base"][2][2] - RES["base"]["vps"]) < 1e-9)
chk("FCFF año 1 TTM-coherente: capex SI año 1 base >= 0", RES["base"]["segs"]["si"]["capex"][0] > 0)
for _k, _r in RES.items():
    chk(f"EV = VA años 1-10 + VA terminal ({_k})", abs(_r["pv_sum"] + _r["pv_tv"] - _r["ev"]) < 1e-6)
assert all(ok for _, ok in CHECKS), [n for n, ok in CHECKS if not ok]


# ---------------------------------------------------------------------------
# 9. Excel
# ---------------------------------------------------------------------------
def build_xlsx():
    wb = Workbook()
    BOLD = Font(bold=True)
    INP = Font(color="0000FF")
    HDR = PatternFill("solid", fgColor="DDEBF7")
    NUM, PCT, USD = "#,##0;-#,##0", "0.00%", "#,##0.00"
    names = {}

    ws = wb.active
    ws.title = "Supuestos"
    ws.append(["SpaceX (SPCX) - Fase 3, supuestos. Azul = input; negro = fórmula. Fuentes en la columna D."])
    ws["A1"].font = BOLD
    ws.append(["Concepto", "Valor", "Unidad", "Fuente"])
    for c in ws[2]:
        c.font, c.fill = BOLD, HDR
    row = [3]

    def put(key, label, value, unit, src, fmt=None, formula=False):
        r_ = row[0]
        ws.cell(row=r_, column=1, value=label)
        c = ws.cell(row=r_, column=2, value=value)
        if not formula:
            c.font = INP
        if fmt:
            c.number_format = fmt
        ws.cell(row=r_, column=3, value=unit)
        ws.cell(row=r_, column=4, value=src)
        names[key] = f"$B${r_}"
        row[0] += 1

    def sec(t):
        ws.cell(row=row[0], column=1, value=t).font = BOLD
        row[0] += 1

    n = lambda k: names[k]  # noqa: E731
    sec("MERCADO")
    put("precio", "Precio SPCX (cierre 23-oct-2026)", PRICE, "USD", MKT["precio"][2], USD)
    put("shA", "Acciones Clase A (portada 10-Q, 15-oct-2026)", SH_A, "M", "data/spacex_financials.csv (P3 portada)", "#,##0.00")
    put("shB", "Acciones Clase B (portada 10-Q, 15-oct-2026)", SH_B, "M", "data/spacex_financials.csv (P3 portada)", "#,##0.00")
    put("shC", "Acciones Clase C (30-sep-2026)", SH_C, "M", "data/spacex_financials.csv (P3 balance): eliminada tras la OPV", "#,##0.00")
    put("sh", "Acciones totales portada (A+B+C)", f"={n('shA')}+{n('shB')}+{n('shC')}", "M", "Calculado", "#,##0.00", True)
    put("opc", "Opciones + RSU vivas (A 158, B 350, RSU 142)", OPC_RSU, "M", "data/spacex_financials.csv (P3 Note 12/13)", "#,##0")
    put("echo_acc", "Acciones A pendientes para EchoStar", ECHOSTAR_ACC, "M", "P3 MD&A 'Spectrum Transaction' (01 §6.2, ≈261,8 M)", "#,##0.0")
    put("echo_caja", "Pago en caja pendiente a EchoStar (hasta)", ECHOSTAR_CAJA, "M USD", "P3 MD&A (01 §1.3). SIN VERIFICAR si ya se pagó: supuesto pendiente", NUM)
    put("musk", "Acciones B restringidas de Musk (incluidas en portada)", MUSK_RESTRINGIDAS, "M", "P2 Note 21 F-60 / 2026 Compensation Developments", "#,##0.00")
    put("sh_dil", "Acciones base diluida (principal)", f"={n('sh')}+{n('opc')}+{n('echo_acc')}", "M", "Portada + opciones/RSU (sin método del tesoro: precios de ejercicio SIN VERIFICAR) + EchoStar", "#,##0.00", True)
    put("sh_sm", "Acciones sin restringidas de Musk (informativa)", f"={n('sh')}-{n('musk')}", "M", "Portada - 1.302,07 M", "#,##0.00", True)
    put("mcap", "Capitalización (precio x portada)", f"={n('precio')}*{n('sh')}", "M USD", "Calculado", NUM, True)
    put("rf", "Tipo libre de riesgo (Treasury 10 años)", RF, "%", MKT["rf"][2], PCT)
    put("erp", "Prima de riesgo de mercado", ERP, "%", MKT["erp"][2], PCT)
    put("tax", "Tipo impositivo", TAX, "%", MKT["tax"][2], PCT)
    put("kd_pre", "Coste de la deuda antes de impuestos", KD_PRE, "%", MKT["kd"][2], PCT)
    sec("FASE 2 (M USD; TTM a 3T26 y saldos a 30-sep-2026)")
    put("rev0", "Ingresos TTM", REV0_TOT, "M USD", "data/spacex_financials.csv", NUM)
    put("ebitda0", "EBITDA ajustado TTM", EBITDA0_TOT, "M USD", "data/spacex_financials.csv", NUM)
    put("sbc0", "SBC TTM (ordinaria + adquisiciones)", SBC0_TOT, "M USD", "data/ratios.csv", NUM)
    put("capex0", "Capex TTM", CAPEX0_TOT, "M USD", "data/spacex_financials.csv", NUM)
    put("fcf0", "FCF TTM (FCO - capex)", FCF0, "M USD", "data/ratios.csv", NUM)
    put("cash", "Caja + valores negociables", CASH0, "M USD", "data/ratios.csv (P3 balance)", NUM)
    put("debt", "Deuda contable (incl. arrendamientos financieros)", DEBT0, "M USD", "data/ratios.csv (P3 balance)", NUM)
    put("netcash", "Caja neta", f"={n('cash')}-{n('debt')}", "M USD", "Calculado", NUM, True)
    put("ev_mkt", "EV de mercado", f"={n('mcap')}-{n('netcash')}", "M USD", "Calculado", NUM, True)
    for s in SEGS:
        put(f"rev0_{s}", f"Ingresos TTM {SEG_NOMBRE[s]}", REV0[s], "M USD", "data/spacex_financials.csv", NUM)
        put(f"rr0_{s}", f"Run-rate inicial {SEG_NOMBRE[s]} ({'TTM' if s == 'space' else '3T26 x 4'})", RR0[s], "M USD", "Calculado en el script", NUM)
    put("b_rr0", "Customer B, 3T26 x 4 (implícito)", B_RR0, "M USD", "data/ratios.csv cliente_B_implicito 3T26 x 4", NUM)
    sec("WACC")
    for s in SEGS:
        put(f"bu_{s}", f"Beta desapalancada {SEG_NOMBRE[s]} (media Damodaran / comparables)", BU_SEG[s]["bu"], "x", "Hoja Beta", "0.000")
        put(f"w_{s}", f"Peso {SEG_NOMBRE[s]} (ingresos año 1, base)", W_SEG[s], "%", "Calculado en el script", PCT)
    put("de", "Deuda / capitalización", f"={n('debt')}/{n('mcap')}", "%", "Calculado", PCT, True)
    put("bu", "Beta desapalancada ponderada", f"={n('bu_space')}*{n('w_space')}+{n('bu_connectivity')}*{n('w_connectivity')}+{n('bu_si')}*{n('w_si')}", "x", "Calculado", "0.000", True)
    put("b0", "Beta reapalancada inicial", f"={n('bu')}*(1+(1-{n('tax')})*{n('de')})", "x", "Hamada", "0.000", True)
    put("bt", "Beta terminal", f"=({n('b0')}+1)/2", "x", "Mitad de camino hacia 1", "0.000", True)
    put("wd", "Peso de la deuda", f"={n('debt')}/({n('debt')}+{n('mcap')})", "%", "Calculado", PCT, True)
    put("kd", "Kd después de impuestos", f"={n('kd_pre')}*(1-{n('tax')})", "%", "Calculado", PCT, True)
    put("ke0", "Ke inicial", f"={n('rf')}+{n('b0')}*{n('erp')}", "%", "CAPM", PCT, True)
    put("wacc0", "WACC inicial (años 1-5)", f"={n('ke0')}*(1-{n('wd')})+{n('kd')}*{n('wd')}", "%", "Calculado", PCT, True)
    put("waccT", "WACC terminal", f"=({n('rf')}+{n('bt')}*{n('erp')})*(1-{n('wd')})+{n('kd')}*{n('wd')}", "%", "Calculado", PCT, True)
    put("wacc0_py", "WACC inicial (valor Python, control)", WACC0, "%", "Salida del script", PCT)
    put("waccT_py", "WACC terminal (valor Python, control)", WACC_T, "%", "Salida del script", PCT)
    ws.column_dimensions["A"].width = 58
    ws.column_dimensions["B"].width = 16
    ws.column_dimensions["D"].width = 110

    # Parámetros
    wp_ = wb.create_sheet("Parametros")
    wp_.append(["Parámetro", "Bajista", "Base", "Alcista"])
    for c in wp_[1]:
        c.font, c.fill = BOLD, HDR
    for s in SEGS:
        keys = sorted({k for sc in SCEN.values() for k in sc[s]})
        for k in keys:
            wp_.append([f"{SEG_NOMBRE[s]}.{k}"] + [str(SCEN[e][s].get(k)) for e in ("bajista", "base", "alcista")])
    wp_.append(["g terminal"] + [SCEN[e]["g_term"] for e in ("bajista", "base", "alcista")])
    wp_.append(["Nota"] + [SCEN[e]["nota"] for e in ("bajista", "base", "alcista")])
    wp_.column_dimensions["A"].width = 32
    for col in "BCD":
        wp_.column_dimensions[col].width = 40

    # Escenarios: filas anuales (valores del script) + descuento y valor con fórmulas vivas
    for esc, r_ in RES.items():
        w = wb.create_sheet(f"Esc_{esc}")
        w.append([f"Escenario {esc} (M USD). Filas 3-n: valores del script; descuento y valor: fórmulas"])
        w["A1"].font = BOLD
        w.append(["Concepto"] + [f"A{t}" for t in YEARS])
        for c in w[2]:
            c.font, c.fill = BOLD, HDR
        rows_idx = {}

        def addrow(label, vals, fmt=NUM, key=None):
            w.append([label] + list(vals))
            ri = w.max_row
            for j in range(2, len(vals) + 2):
                w.cell(row=ri, column=j).number_format = fmt
            if key:
                rows_idx[key] = ri

        for s in SEGS:
            sg = r_["segs"][s]
            addrow(f"{SEG_NOMBRE[s]}: run-rate fin de año", sg["rr"])
            addrow(f"{SEG_NOMBRE[s]}: crecimiento run-rate", sg["g"], PCT)
            addrow(f"{SEG_NOMBRE[s]}: ingresos", sg["rev"])
            addrow(f"{SEG_NOMBRE[s]}: margen EBITDA aj.", sg["marg"], PCT)
            addrow(f"{SEG_NOMBRE[s]}: EBITDA aj.", sg["ebitda"])
            addrow(f"{SEG_NOMBRE[s]}: SBC", sg["sbc"])
            addrow(f"{SEG_NOMBRE[s]}: capex", sg["capex"])
            addrow(f"{SEG_NOMBRE[s]}: capex / ingresos", [c / x for c, x in zip(sg["capex"], sg["rev"])], PCT)
            addrow(f"{SEG_NOMBRE[s]}: D&A", sg["da"])
        t_ = r_["tot"]
        addrow("TOTAL ingresos", t_["rev"], key="rev")
        addrow("TOTAL EBITDA aj.", t_["ebitda"], key="ebitda")
        addrow("TOTAL SBC", t_["sbc"], key="sbc")
        addrow("TOTAL D&A", t_["da"])
        addrow("TOTAL EBIT (EBITDA - SBC - D&A)", t_["ebit"])
        addrow("Impuestos", t_["tax"], key="tax")
        addrow("TOTAL capex", t_["capex"], key="capex")
        addrow("Capex / ingresos", [c / x for c, x in zip(t_["capex"], t_["rev"])], PCT)
        # FCFF como fórmula
        w.append(["FCFF (fórmula)"] + [f"={col}{rows_idx['ebitda']}-{col}{rows_idx['sbc']}-{col}{rows_idx['tax']}-{col}{rows_idx['capex']}"
                                       for col in [w.cell(row=1, column=j).column_letter for j in range(2, N + 3)]])
        fr = w.max_row
        w.append(["FCFF (Python, control)"] + t_["fcff"])
        w.append(["WACC del año"] + r_["wp"])
        wr = w.max_row
        for j in range(2, N + 2):
            w.cell(row=wr, column=j).number_format = PCT
        cols = [w.cell(row=1, column=j).column_letter for j in range(2, N + 3)]
        w.append(["Factor de descuento"] + [f"=1/(1+{cols[0]}{wr})"] + [f"={cols[j - 1]}{wr + 1}/(1+{cols[j]}{wr})" for j in range(1, N)])
        dr = w.max_row
        w.append(["VA del FCFF"] + [f"={cols[j]}{fr}*{cols[j]}{dr}" for j in range(N)])
        pr_ = w.max_row
        w.append([])
        last = cols[N - 1]
        ycol = cols[N]   # año 11
        items = [
            ("Suma VA años 1-10", f"=SUM({cols[0]}{pr_}:{last}{pr_})", r_["pv_sum"]),
            ("g terminal", r_["g"], r_["g"]),
            ("WACC terminal", f"=Supuestos!{names['waccT']}", WACC_T),
            ("Valor terminal (FCFF A11 / (WACC_T - g))", None, r_["tv"]),
            ("VA del valor terminal", None, r_["pv_tv"]),
            ("EV", None, r_["ev"]),
            ("% del EV en el valor terminal", None, r_["tv_share"]),
            ("Caja neta", f"=Supuestos!{names['netcash']}", NETCASH0),
            ("Ajuste EchoStar (base diluida)", f"=-Supuestos!{names['echo_caja']}", -ECHOSTAR_CAJA),
            ("Valor acciones (base diluida)", None, r_["eq_diluida"]),
            ("Valor por acción, base diluida", None, r_["vps_diluida"]),
            ("Valor por acción, portada", None, r_["vps_portada"]),
            ("Valor por acción, sin restringidas Musk", None, r_["vps_sin_musk"]),
            ("Precio SPCX", f"=Supuestos!{names['precio']}", PRICE),
        ]
        w.append(["Concepto", "Fórmula", "Python"])
        base_r = w.max_row + 1
        for i, (lab, frm, py) in enumerate(items):
            w.append([lab, frm, py])
        R = lambda lab: base_r + [x[0] for x in items].index(lab)  # noqa: E731
        w.cell(row=R("Valor terminal (FCFF A11 / (WACC_T - g))"), column=2, value=f"={ycol}{fr}/(B{R('WACC terminal')}-B{R('g terminal')})")
        w.cell(row=R("VA del valor terminal"), column=2, value=f"=B{R('Valor terminal (FCFF A11 / (WACC_T - g))')}*{last}{dr}")
        w.cell(row=R("EV"), column=2, value=f"=B{R('Suma VA años 1-10')}+B{R('VA del valor terminal')}")
        w.cell(row=R("% del EV en el valor terminal"), column=2, value=f"=B{R('VA del valor terminal')}/B{R('EV')}")
        w.cell(row=R("Valor acciones (base diluida)"), column=2, value=f"=B{R('EV')}+B{R('Caja neta')}+B{R('Ajuste EchoStar (base diluida)')}")
        w.cell(row=R("Valor por acción, base diluida"), column=2, value=f"=B{R('Valor acciones (base diluida)')}/Supuestos!{names['sh_dil']}")
        w.cell(row=R("Valor por acción, portada"), column=2, value=f"=(B{R('EV')}+B{R('Caja neta')})/Supuestos!{names['sh']}")
        w.cell(row=R("Valor por acción, sin restringidas Musk"), column=2, value=f"=(B{R('EV')}+B{R('Caja neta')})/Supuestos!{names['sh_sm']}")
        w.column_dimensions["A"].width = 44

    # Sensibilidad
    wsn = wb.create_sheet("Sensibilidad")
    for esc in SCEN:
        wsn.append([f"{esc}: valor por acción (base diluida) - WACC inicial (filas; el terminal se desplaza igual) x g (columnas)"])
        wsn.append(["WACC0 \\ g"] + G_GRID)
        for w_, rowv in zip(W_GRID, SENS[esc]):
            wsn.append([w_] + rowv)
        wsn.append([])
    wsn.append(["Customer B y otros motores (caso base)"])
    for lab, val in B_SENS:
        wsn.append([lab, val])
    wsn.append([])
    for lab, vals in DRIVERS:
        wsn.append([lab] + vals)
    for L, val in L_SENS:
        wsn.append([f"Vida útil SI = {L} años", val])
    wsn.append(["Base con capex SI año 1 al ritmo de la guía 4T26", VPS_CAPEX_GUIA])
    wsn.append(["Bajista con SI sin crecimiento tras el año 1", VPS_BAJISTA_SIN_CREC_SI])
    for lab, val in WACC_ALT_VPS.items():
        wsn.append([f"Base con WACC0 alternativo ({lab})", val])
    wsn.column_dimensions["A"].width = 80

    # DCF inverso
    wi = wb.create_sheet("DCF_inverso")
    wi.append(["Pregunta (precio objetivo = precio SPCX, base diluida)", "Valor que lo iguala", "Base"])
    wi.append(["Multiplicador del crecimiento de los años 2-5 (todos los segmentos)", REV_LAMBDA, 1.0])
    if REV_LAMBDA_RES:
        wi.append(["  Ingresos año 10 con ese multiplicador (M USD)", REV_LAMBDA_RES["tot"]["rev"][N - 1], RES["base"]["tot"]["rev"][N - 1]])
        wi.append(["  TACC ingresos 10 años", _cagr(REV_LAMBDA_RES), CAGR["base"]])
    wi.append(["Margen EBITDA aj. objetivo de SI", REV_MARGIN_SI if REV_MARGIN_SI else "sin solución", SCEN["base"]["si"]["m_obj"]])
    wi.append(["k de SI (capex por $ de ingreso anual)", REV_K_SI if REV_K_SI else "sin solución", SCEN["base"]["si"]["k"]])
    wi.append(["Crédito a la guía del 1T27 (1 = extremo bajo completo)", REV_GUIA if REV_GUIA else "sin solución", SCEN["base"]["si"]["credito_guia"]])
    wi.append(["WACC inicial (terminal desplazado igual)", REV_WACC if REV_WACC else "sin solución", WACC0])
    for lab, val in REV_EXTREMOS.items():
        wi.append([f"Valor por acción en el extremo: {lab}", val])
    wi.append(["Alcista: multiplicador del crecimiento años 2-5", REV_LAMBDA_BULL, 1.0])
    if REV_LAMBDA_BULL_RES:
        wi.append(["  Ingresos año 10 (M USD)", REV_LAMBDA_BULL_RES["tot"]["rev"][N - 1], RES["alcista"]["tot"]["rev"][N - 1]])
    wi.append(["Alcista: margen EBITDA aj. objetivo de SI", REV_MARGIN_SI_BULL if REV_MARGIN_SI_BULL else "sin solución", SCEN["alcista"]["si"]["m_obj"]])
    wi.column_dimensions["A"].width = 70

    # Múltiplos
    wm = wb.create_sheet("Multiplos")
    wm.append(["Ticker", "Nombre", "Grupo", "Precio", "Capitalización M$", "EV M$", "EV/Ventas", "EV/EBITDA", "EV/EBIT", "PER", "Beta 5a", "Deuda M$", "Fuente"])
    for c in wm[1]:
        c.font, c.fill = BOLD, HDR
    for p in PEERS:
        wm.append(list(p) + [PEERS_SRC])
    wm.append([])
    wm.append(["SPCX", "Múltiplo", "Valor"])
    for k_, val in SPCX_MULT.items():
        wm.append(["SPCX", k_, val if val is not None else "n/s (denominador negativo)"])
    wm.append(["SPCX terceros", SPCX_3RD])
    wm.append([])
    wm.append(["Suma de partes por múltiplos", "EV M$", "Valor por acción (diluida)"])
    for k_, ev in SOTP.items():
        wm.append([k_, ev, _vps_from_ev(ev)])

    # Beta
    wb_ = wb.create_sheet("Beta")
    wb_.append(["Comparable", "Segmento", "Beta 5a (regresión)", "Deuda M$", "Capitalización M$", "Beta desapalancada"])
    for p in PEERS:
        if p[0] in PEER_BU:
            wb_.append([p[0], p[2], p[10], p[11], p[4], PEER_BU[p[0]]])
    wb_.append([])
    wb_.append(["Sector Damodaran", "Beta desapalancada corregida por caja", "N.º empresas", DAMO_SRC])
    for k_, (b, n_) in DAMO.items():
        wb_.append([k_, b, n_])
    wb_.append([])
    wb_.append(["Segmento", "Damodaran (media)", "Mediana comparables", "N.º comparables", "Beta usada", "Peso"])
    for s in SEGS:
        wb_.append([SEG_NOMBRE[s], BU_SEG[s]["damo"], BU_SEG[s]["peers"], BU_SEG[s]["n"], BU_SEG[s]["bu"], W_SEG[s]])
    wb_.append([])
    wb_.append(["Regresión SPCX (diaria, informativa)", "Beta", "Error típico", "Observaciones"])
    wb_.append(["vs SPY", BETA_REG_SPY, SE_SPY, N_OBS])
    wb_.append(["vs QQQ", BETA_REG_QQQ, SE_QQQ, N_OBS])
    wb_.append(["vs SPY sin la primera semana", BETA_REG_SPY_X1S, SE_SPY_X1S, N_OBS - 5])
    wb_.append(["Blume (0,67 x SPY + 0,33)", BETA_BLUME])
    wb_.append(["Fuente precios", "data/precios_mercado_fase3.csv (Nasdaq.com, 12-jun a 23-oct-2026)"])

    wb.save(OUT_XLSX)


def recalc_xlsx(path):
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice or os.environ.get("DCF_NO_RECALC"):
        return "no recalculado (LibreOffice no disponible o DCF_NO_RECALC)"
    tmp = tempfile.mkdtemp(prefix="dcf_recalc_")
    try:
        subprocess.run([soffice, f"-env:UserInstallation=file:///{tmp.replace(os.sep, '/')}/profile", "--headless", "--calc",
                        "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", tmp, path],
                       check=True, capture_output=True, timeout=180)
        shutil.copyfile(os.path.join(tmp, os.path.basename(path)), path)
        return "recalculado con LibreOffice (valores cacheados)"
    except Exception as e:  # noqa: BLE001
        return f"no recalculado ({type(e).__name__})"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------------------
# 10. Salida por pantalla
# ---------------------------------------------------------------------------
def fx(x, dec=1):
    return "n/s" if x is None else f_m(x, dec) + "x"


def main():
    build_xlsx()
    recalc = recalc_xlsx(OUT_XLSX)
    pr = print
    pr("=== 1. DATOS DE PARTIDA (Fase 2) ===")
    pr(f"Ingresos TTM {f_m(REV0_TOT)} | EBITDA aj. TTM {f_m(EBITDA0_TOT)} | SBC TTM {f_m(SBC0_TOT)} | EBIT TTM {f_m(EBIT0)} | "
       f"FCO {f_m(FCO0)} | capex {f_m(CAPEX0_TOT)} ({f_p(CAPEX0_TOT / REV0_TOT)}) | FCF {f_m(FCF0)}")
    for s in SEGS:
        pr(f"  {SEG_NOMBRE[s]}: ingresos TTM {f_m(REV0[s])} | 3T26 {f_m(REV_Q3[s])} | 3T25 {f_m(REV_Q3_25[s])} | RR0 {f_m(RR0[s])} | "
           f"margen EBITDA aj. TTM {f_p(EBITDA0[s] / REV0[s])} | SBC/ingresos TTM {f_p(SBC0[s] / REV0[s])} | capex TTM {f_m(CAPEX0[s])} "
           f"({f_p(CAPEX0[s] / REV0[s])}) | D&A 3T26 x 4 {f_m(4 * DA_Q3[s])}")
    pr(f"Customer B 3T26 {f_m(B_Q3)} -> RR {f_m(B_RR0)} ({f_p(B_RR0 / RR0['si'])} del RR de SI); SI sin B RR {f_m(SI_SIN_B_RR0)}; "
       f"SI sin B ni Cursor 3T26 {f_m(SI_SIN_B_NI_CURSOR_Q3)}; Cursor 3T26 {f_m(CURSOR_Q3)}")
    pr(f"k observado TTM (L={L_SEG['connectivity']}): Connectivity {f_m(K_OBS['connectivity'], 3)} | SI {f_m(K_OBS['si'], 3)}")
    pr(f"Capex SI 9M26 / aumento de capacidad (0,8 -> 1,7 GW) = {f_m(CAPEX_POR_W, 1)} $/W; ingreso anual por W implícito: "
       f"k observado {f_m(CAPEX_POR_W / K_OBS['si'], 1)} | k=1,25 {f_m(CAPEX_POR_W / 1.25, 1)} | k=0,90 {f_m(CAPEX_POR_W / 0.90, 1)} $/W")
    pr(f"Guía 1T27 (secundaria): RR de SI implícito extremo bajo {f_m(GUIA_SI_RR['bajo'])} | punto medio {f_m(GUIA_SI_RR['medio'])} "
       f"(Space + Connectivity 3T26 = {f_m(OTROS_Q3)})")
    pr(f"Capex Space/ingresos: FY2023 {f_p(CAPEX_SOBRE_ING_SPACE['FY2023'])} | FY2024 {f_p(CAPEX_SOBRE_ING_SPACE['FY2024'])} | "
       f"FY2025 {f_p(CAPEX_SOBRE_ING_SPACE['FY2025'])} | TTM {f_p(CAPEX_SOBRE_ING_SPACE['TTM_Q3_2026'])}. Margen EBITDA aj. Space: "
       + " | ".join(f"{k} {f_p(x)}" for k, x in M_EBITDA_SPACE_HIST.items()))

    pr("\n=== 2. MERCADO, ACCIONES Y WACC ===")
    pr(f"Precio {f_m(PRICE, 2)} | acciones portada {f_m(SH_COVER, 2)} M (A {f_m(SH_A, 2)} + B {f_m(SH_B, 2)} + C {f_m(SH_C, 0)}) | "
       f"diluida {f_m(SH_DIL, 2)} M (+opciones/RSU {f_m(OPC_RSU)} + EchoStar {f_m(ECHOSTAR_ACC, 1)}) | sin restringidas Musk {f_m(SH_SIN_MUSK, 2)} M | "
       f"premios de rendimiento no cumplidos {f_m(PREMIOS_RENDIMIENTO)} M (no se suman)")
    pr(f"Capitalización {f_m(MCAP)} | capitalización diluida {f_m(PRICE * SH_DIL)} | caja {f_m(CASH0)} | deuda {f_m(DEBT0)} | "
       f"caja neta {f_m(NETCASH0)} | EV mercado {f_m(EV_MKT)} | D/E {f_p(D_E, 2)} | peso deuda {f_p(W_D, 2)}")
    pr(f"Regresión diaria SPCX ({N_OBS} obs., 12-jun a 23-oct-2026): beta vs SPY {f_m(BETA_REG_SPY, 2)} (e.t. {f_m(SE_SPY, 2)}) | "
       f"vs QQQ {f_m(BETA_REG_QQQ, 2)} (e.t. {f_m(SE_QQQ, 2)}) | vs SPY sin 1.ª semana {f_m(BETA_REG_SPY_X1S, 2)} (e.t. {f_m(SE_SPY_X1S, 2)}) | "
       f"Blume {f_m(BETA_BLUME, 2)} | volatilidad anualizada SPCX {f_p(VOL_SPCX)} vs SPY {f_p(VOL_SPY)}")
    for t, bu in PEER_BU.items():
        p = next(x for x in PEERS if x[0] == t)
        pr(f"  {t}: beta {f_m(p[10], 2)} -> desapalancada {f_m(bu, 2)} (D/E {f_p(p[11] / p[4], 1)})")
    for s in SEGS:
        b = BU_SEG[s]
        pr(f"  {SEG_NOMBRE[s]}: Damodaran {f_m(b['damo'], 3)} | mediana comparables {f_m(b['peers'], 3)} (n={b['n']}) | "
           f"beta usada {f_m(b['bu'], 3)} | peso {f_p(W_SEG[s])}")
    pr(f"Beta desapalancada ponderada {f_m(BETA_U, 3)} | beta inicial {f_m(BETA0, 3)} | beta terminal {f_m(BETA_T, 3)}")
    pr(f"Ke0 {f_p(KE0, 2)} | KeT {f_p(KE_T, 2)} | Kd después de impuestos {f_p(KD, 2)} | WACC0 {f_p(WACC0, 2)} | WACC_T {f_p(WACC_T, 2)}")
    for lab, w in WACC_ALT.items():
        pr(f"  WACC0 alternativo ({lab}): {f_p(w, 2)}")

    pr("\n=== 3. ESCENARIOS (valor por acción; base diluida salvo indicación) ===")
    for k, r_ in RES.items():
        t_ = r_["tot"]
        pr(f"--- {k.upper()} --- EV {f_m(r_['ev'])} | VA años 1-10 {f_m(r_['pv_sum'])} | VA terminal {f_m(r_['pv_tv'])} "
           f"({f_p(r_['tv_share'])} del EV) | valor terminal {f_m(r_['tv'])} | FCFF A11 {f_m(r_['fcff11'])} | g {f_p(r_['g'])}")
        pr(f"    Valor acciones diluida {f_m(r_['eq_diluida'])} | VPS diluida {f_m(r_['vps_diluida'], 2)} | portada {f_m(r_['vps_portada'], 2)} | "
           f"sin Musk {f_m(r_['vps_sin_musk'], 2)} | vs precio {f_p(r_['vps_diluida'] / PRICE - 1)} | "
           f"TACC ingresos 10 años {f_p(CAGR[k])} | ingresos A10 {f_m(t_['rev'][N - 1])} | "
           f"primer año FCFF > 0: {r_['anio_fcff_pos']} | FCFF acumulado mínimo {f_m(r_['fcff_acum_min'])}")
        pr("    Año | ingresos | EBITDA aj. | SBC | impuestos | capex | capex/ingr. | FCFF | VA")
        for i, t in enumerate(YEARS):
            pv = f_m(r_["pvs"][i]) if t <= N else "(terminal)"
            pr(f"    A{t} | {f_m(t_['rev'][i])} | {f_m(t_['ebitda'][i])} | {f_m(t_['sbc'][i])} | {f_m(t_['tax'][i])} | "
               f"{f_m(t_['capex'][i])} | {f_p(t_['capex'][i] / t_['rev'][i])} | {f_m(t_['fcff'][i])} | {pv}")
        for s in SEGS:
            sg = r_["segs"][s]
            pr(f"    {SEG_NOMBRE[s]}: ingresos A1 {f_m(sg['rev'][0])} | A5 {f_m(sg['rev'][4])} | A10 {f_m(sg['rev'][9])} | "
               f"RR A1 {f_m(sg['rr'][0])} | margen A1 {f_p(sg['marg'][0])} -> A5 {f_p(sg['marg'][4])} | "
               f"capex A1 {f_m(sg['capex'][0])} ({f_p(sg['capex'][0] / sg['rev'][0])}) | A3 {f_p(sg['capex'][2] / sg['rev'][2])} | "
               f"A5 {f_p(sg['capex'][4] / sg['rev'][4])} | A10 {f_p(sg['capex'][9] / sg['rev'][9])} | A11 {f_p(sg['capex'][10] / sg['rev'][10])} | "
               f"SBC A1 {f_m(sg['sbc'][0])}")
        cx1 = t_["capex"][0]
        pr(f"    Capex total A1 {f_m(cx1)} frente a guía 4T26 {f_m(MKT['guia_capex_4T26_bajo'][0])}-{f_m(MKT['guia_capex_4T26_alto'][0])} "
           f"(un solo trimestre) y compromisos no cancelables {f_m(COMPROMISOS_NC)} (2027: {f_m(COMPROMISOS_2027)})")
    pr(f"Rango: bajista {f_m(RES['bajista']['vps'], 2)} | base {f_m(RES['base']['vps'], 2)} | alcista {f_m(RES['alcista']['vps'], 2)} | precio {f_m(PRICE, 2)}")

    pr("\n=== 4. SENSIBILIDAD WACC0 x g (valor por acción, base diluida) ===")
    for k in SCEN:
        pr(f"[{k}] WACC0 \\ g: " + " | ".join(f_p(g) for g in G_GRID))
        for w, rowv in zip(W_GRID, SENS[k]):
            pr(f"  {f_p(w, 2)}: " + " | ".join(f_m(x, 2) for x in rowv))
    pr("Customer B y motores (base):")
    for lab, val in B_SENS:
        pr(f"  {lab}: {f_m(val, 2)}")
    pr(f"  Valor por acción que depende de que Customer B no rescinda (base - base con rescisión): {f_m(B_VALOR_BASE, 2)} "
       f"({f_p(B_VALOR_BASE / RES['base']['vps'])} del base)")
    for lab, vals in DRIVERS:
        pr(f"  {lab}: " + " / ".join(f_m(x, 2) for x in vals))
    pr("  Vida útil SI 4 / 5 / 6 años: " + " / ".join(f_m(val, 2) for _, val in L_SENS))
    pr(f"  Base con capex de SI del año 1 al ritmo de la guía 4T26 (punto medio x 4 x {f_p(SI_PESO_CAPEX_Q3)} = {f_m(CAPEX_SI_A1_GUIA)}): "
       f"{f_m(VPS_CAPEX_GUIA, 2)}")
    pr(f"  Bajista con SI sin crecimiento tras el año 1 (solo reposición): {f_m(VPS_BAJISTA_SIN_CREC_SI, 2)}")
    for lab, val in WACC_ALT_VPS.items():
        pr(f"  Base con WACC0 alternativo ({lab}, {f_p(WACC_ALT[lab], 2)}): {f_m(val, 2)}")

    pr("\n=== 5. DCF INVERSO (precio = {} $, base diluida) ===".format(f_m(PRICE, 2)))
    if REV_LAMBDA:
        pr(f"Multiplicador del crecimiento años 2-5 (todos los segmentos): {f_m(REV_LAMBDA, 3)} -> ingresos A10 "
           f"{f_m(REV_LAMBDA_RES['tot']['rev'][N - 1])} (base {f_m(RES['base']['tot']['rev'][N - 1])}), TACC 10 años {f_p(_cagr(REV_LAMBDA_RES))}"
           f" (base {f_p(CAGR['base'])}); SI A10 {f_m(REV_LAMBDA_RES['segs']['si']['rev'][N - 1])}")
    pr(f"Margen EBITDA aj. objetivo de SI necesario: {f_p(REV_MARGIN_SI) if REV_MARGIN_SI else 'sin solución en 0-95 %'}")
    pr(f"k de SI necesario: {f_m(REV_K_SI, 3) if REV_K_SI else 'sin solución en 0,05-3'}")
    pr(f"Crédito a la guía 1T27 necesario: {f_m(REV_GUIA, 3) if REV_GUIA else 'sin solución en 0-5'}")
    pr(f"WACC inicial necesario: {f_p(REV_WACC, 2) if REV_WACC else 'sin solución entre ' + f_p(REV_WACC_LO, 2) + ' y 20 %'}")
    for lab, val in REV_EXTREMOS.items():
        pr(f"  Valor por acción en el extremo ({lab}): {f_m(val, 2)}")
    if REV_LAMBDA_BULL:
        rb = REV_LAMBDA_BULL_RES
        pr(f"Sobre el ALCISTA: multiplicador del crecimiento años 2-5 {f_m(REV_LAMBDA_BULL, 3)} -> ingresos A10 {f_m(rb['tot']['rev'][N - 1])}, "
           f"TACC 10 años {f_p(_cagr(rb))}; SI A10 {f_m(rb['segs']['si']['rev'][N - 1])}; Connectivity A10 {f_m(rb['segs']['connectivity']['rev'][N - 1])}")
    pr(f"Sobre el ALCISTA: margen EBITDA aj. objetivo de SI necesario {f_p(REV_MARGIN_SI_BULL) if REV_MARGIN_SI_BULL else 'sin solución en 0-95 %'}")

    pr("\n=== 6. MÚLTIPLOS ===")
    for k, val in SPCX_MULT.items():
        pr(f"SPCX {k}: {fx(val)}")
    for s in SEGS:
        pr(f"  Mediana {SEG_NOMBRE[s]}: EV/Ventas {fx(MED[s]['ev_sales'][0], 2)} (n={MED[s]['ev_sales'][1]}) | "
           f"EV/EBITDA {fx(MED[s]['ev_ebitda'][0], 2)} (n={MED[s]['ev_ebitda'][1]}) | SOTP ventas TTM {f_m(SOTP_SALES[s])} | "
           f"ventas RR {f_m(SOTP_SALES_RR[s])} | EBITDA {f_m(SOTP_EBITDA[s]) if SOTP_EBITDA[s] is not None else 'n/s'}")
    for k, ev in SOTP.items():
        pr(f"  Suma de partes {k}: EV {f_m(ev)} -> {f_m(_vps_from_ev(ev), 2)} $/acción (diluida) | {f_p(ev / EV_MKT)} del EV de mercado")

    pr("\n=== 7. CIFRAS AUXILIARES DEL DOCUMENTO ===")
    pr(f"Efecto por acción (base diluida) si el pago a EchoStar ya se hizo: +{f_m(ECHOSTAR_CAJA / SH_DIL, 2)} $")
    pr(f"EV de mercado / EV alcista: {fx(EV_MKT / RES['alcista']['ev'], 2)} | EV de mercado / EV base: {fx(EV_MKT / RES['base']['ev'], 2)}")
    pr(f"Guía capex 4T26 / capex TTM: {f_p(MKT['guia_capex_4T26_bajo'][0] / CAPEX0_TOT)} - {f_p(MKT['guia_capex_4T26_alto'][0] / CAPEX0_TOT)}")
    pr(f"SBC de Cursor por año (años 1-{CURSOR_VEST_ANIOS}): {f_m(CURSOR_SBC_PENDIENTE / CURSOR_VEST_ANIOS)} | SBC ordinaria SI / ingresos SI TTM: "
       f"{f_p(SBC0_SI_ORD / REV0['si'])}")
    for k, r_ in RES.items():
        pr(f"FCFF acumulado mínimo {k}: {f_m(r_['fcff_acum_min'])} = {f_p(-r_['fcff_acum_min'] / CASH0)} de la caja + valores "
           f"({f_m(CASH0)}); caja que quedaría: {f_m(CASH0 + r_['fcff_acum_min'])}")

    pr("\n=== 8. CONTROLES ===")
    for nme, ok in CHECKS:
        pr(f"  {'OK' if ok else 'FALLO'} {nme}")
    pr(f"Excel: {OUT_XLSX} ({recalc})")


if __name__ == "__main__":
    main()
