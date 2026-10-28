#!/usr/bin/env python3
"""Fase 4 - SpaceX (SPCX): cifras de la tesis alcista, la tesis bajista, las señales, el abogado del diablo,
el DCF inverso ampliado y el gobierno corporativo.

Todas las cifras de docs/04-tesis.md salen de la salida de este script.
- IMPORTA el modelo de la Fase 3 (scripts/fase3_dcf.py), que a su vez lee los CSV de la Fase 2. No copia cifras del
  modelo: los valores por escenario, el WACC, las acciones y el DCF inverso se toman de los objetos de fase3_dcf.
- Importar fase3_dcf NO escribe nada (su Excel solo se genera en su main()). Este script tampoco escribe ficheros.
- Los pocos datos que no están en los CSV de la Fase 2 ni en el modelo (ARPU, suscriptores, 13 GW, objetivo de
  100.000 M$...) van en el bloque DATOS con su fuente (IDs de fuentes/fuentes.md, nuevas_fase3_v1.md y
  nuevas_fase4_v1.md).
- Para la variante "capex al ritmo de la guía durante dos años" se envuelve fase3_dcf.proj_segment SIN cambiar sus
  fórmulas: se impone un suelo al capex de SI en los años indicados y se recalculan la D&A y el EBIT con las
  propias funciones de la Fase 3 (da_path). Un control comprueba que sin suelos el resultado es idéntico y que con
  el suelo solo en el año 1 se reproduce el 21,40 $ de la Fase 3.
Convenciones: M$ = millones de dólares; "vpa" = valor por acción en la base diluida de la Fase 3 (14.492,86 M).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fase3_dcf as f3  # noqa: E402

f_m, f_p = f3.f_m, f3.f_p
v, rat = f3.v, f3.rat
SC = f3.SCEN
BASE_VPS = f3.RES["base"]["vps"]
CHECKS = []


def chk(n, ok):
    CHECKS.append((n, bool(ok)))


def pr(*a):
    print(*a)


def h(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)


def usd(x, d=2):
    return f_m(x, d) + " $"


def vps(sc, **kw):
    return f3.run_dcf(sc, **kw)["vps"]


def wacc_from(beta_u=None, erp=None, rf=None, beta0=None):
    """WACC inicial y terminal con la mecánica de la Fase 3 (Hamada, beta terminal a mitad de camino hacia 1)."""
    erp = f3.ERP if erp is None else erp
    rf = f3.RF if rf is None else rf
    b0 = beta0 if beta0 is not None else (f3.BETA0 if beta_u is None else beta_u * (1 + (1 - f3.TAX) * f3.D_E))
    bt = (b0 + 1.0) / 2
    w0 = (rf + b0 * erp) * (1 - f3.W_D) + f3.KD * f3.W_D
    wt = (rf + bt * erp) * (1 - f3.W_D) + f3.KD * f3.W_D
    return w0, wt


# ---------------------------------------------------------------------------------------------
# DATOS que no están en los CSV de la Fase 2 ni en el modelo (con fuente)
# ---------------------------------------------------------------------------------------------
ARPU = {"3T25": 83.0, "3T26": 69.0, "9M26": 67.0, "FY2024": 91.0, "FY2025": 81.0}  # $/mes, P3 MD&A KBM y P2 (01 §1.1-1.2)
SUBS = {"3T25": 7.2, "3T26": 13.6}           # M suscriptores consumo, P3 MD&A KBM (01 §1.2)
BACKLOG_3T26 = v("backlog", "9M2026") if f3.F2.g(f3.D, "backlog", "9M2026") else 62959.0  # P3 Note 3 (01 §1.2)
GW_3T26 = f3.NAMEPLATE_GW["Q3_2026"]          # 1,7 GW (P3 KBM)
GW_FIN_2027 = 13.0                            # "~13 GW a fin de 2027": S7 y S9 (secundarias, SIN VERIFICAR)
GW_FIN_2026 = (2.5, 3.0)                      # 2,5-3 GW a fin de 2026: S7 y S9 (secundarias, SIN VERIFICAR)
OBJ_RR_DIC26 = 100000.0                       # 100.000 M$ de ingresos anualizados (dic-2026 x 12): S9 (secundaria, SIN VERIFICAR)
CONTRATO_P2_MES = 1250.0                      # M$/mes hasta mayo-2029 (P2 p. 147; 01 §1.4)
B_PCT_3T26 = 0.345                            # P3 Note 3 (01 §1.4; 02 §9)
A_PCT_3T26 = 0.166                            # P3 Note 3 (01 §4.3)
VOTO_MUSK_P2 = 0.824                          # P2 portada (01 §4.1)
VOTO_MUSK_EST = 0.861                         # estimación de la Fase 1 (SIN VERIFICAR, 01 §4.1)
PREMIOS_NO_CUMPLIDOS = f3.PREMIOS_RENDIMIENTO  # 1.333 M (P3 Note 13, vía CSV de la Fase 2)
APERTURA_12JUN_M1 = 150.00                    # Nasdaq.com histórico (M1, nuevas_fase3_v1.md)
APERTURA_12JUN_S1 = 160.00                    # S1 (Fase 1 §6.1)
CIERRE_12JUN = f3.PX[0][1]                    # data/precios_mercado_fase3.csv (M1)
INT_VINC_Q3 = v("gastos_intereses_vinculadas", "Q3_2026")   # P3 p. 5 (vía Fase 2)
INT_VINC_9M = v("gastos_intereses_vinculadas", "9M2026")
DEUDA_VINC = rat("deuda_vinculada", "9M2026")              # 12.897 (P3 Notes 9 y 17, vía Fase 2)
CURSOR_SBC = f3.CURSOR_SBC_PENDIENTE

# ---------------------------------------------------------------------------------------------
# Envoltorio de proj_segment: suelos de capex de SI por año (índice 0 = año 1)
# ---------------------------------------------------------------------------------------------
_orig_proj = f3.proj_segment


def _proj_suelos(s, p, g_term):
    out = _orig_proj(s, p, g_term)
    suelos = p.get("_suelos") if s == "si" else None
    if suelos:
        cap = list(out["capex"])
        for i, x in suelos.items():
            cap[i] = max(cap[i], x)
        da = f3.da_path(f3.DA_Q3[s], cap, f3.L_SEG[s])
        out = dict(out, capex=cap, da=da, ebit=[e - b - d for e, b, d in zip(out["ebitda"], out["sbc"], da)])
    return out


f3.proj_segment = _proj_suelos
chk("envoltorio sin suelos = base de la Fase 3", abs(vps(SC["base"]) - BASE_VPS) < 1e-9)


def bv(**mods):
    """base_var de la Fase 3 que admite además '_suelos'."""
    sc = f3.base_var(**{k: x for k, x in mods.items() if k != "suelos"})
    if "suelos" in mods:
        sc["si"]["_suelos"] = mods["suelos"]
    return sc


chk("suelo A1 con el envoltorio = VPS_CAPEX_GUIA de la Fase 3",
    abs(vps(bv(suelos={0: f3.CAPEX_SI_A1_GUIA})) - f3.VPS_CAPEX_GUIA) < 1e-6)


def with_L(L, fun):
    old = f3.L_SEG["si"]
    f3.L_SEG["si"] = L
    try:
        return fun()
    finally:
        f3.L_SEG["si"] = old


# ---------------------------------------------------------------------------------------------
# Valor por segmento (aproximación: impuesto del 21 % sobre el EBIT positivo del segmento, sin compensar pérdidas)
# ---------------------------------------------------------------------------------------------
def seg_values(res):
    out = {}
    g = res["g"]
    for s in f3.SEGS:
        sg = res["segs"][s]
        fc = [sg["ebitda"][i] - sg["sbc"][i] - sg["capex"][i] - f3.TAX * max(0.0, sg["ebit"][i]) for i in range(len(f3.YEARS))]
        pv = sum(fc[t] * res["dfs"][t] for t in range(f3.N))
        tv = fc[f3.N] / (f3.WACC_T - g) * res["dfs"][-1]
        out[s] = dict(pv=pv, tv=tv, ev=pv + tv, vps=(pv + tv) / f3.SH_DIL)
    return out


# =============================================================================================
h("1. PUNTO DE PARTIDA (modelo de la Fase 3)")
R = f3.RES
for k in ("bajista", "base", "alcista"):
    r = R[k]
    pr(f"{k}: vpa {usd(r['vps'])} | frente al precio {f_p(r['vps'] / f3.PRICE - 1)} | EV {f_m(r['ev'])} | VT/EV {f_p(r['tv_share'])} | "
       f"FCFF A1 {f_m(r['tot']['fcff'][0])} | FCFF acum. mín. {f_m(r['fcff_acum_min'])} | TACC ingresos {f_p(f3.CAGR[k])}")
pr(f"Precio {usd(f3.PRICE)} | capitalización portada {f_m(f3.MCAP)} | EV mercado {f_m(f3.EV_MKT)} | WACC0 {f_p(f3.WACC0, 2)} | "
   f"WACC_T {f_p(f3.WACC_T, 2)} | beta0 {f_m(f3.BETA0, 3)} | acciones diluidas {f_m(f3.SH_DIL, 2)}")
SEGV = {k: seg_values(R[k]) for k in R}
for k in ("bajista", "base", "alcista"):
    sv = SEGV[k]
    tot = sum(x["ev"] for x in sv.values())
    pr(f"Valor por segmento ({k}, aprox. sin compensar pérdidas entre segmentos): " +
       " | ".join(f"{f3.SEG_NOMBRE[s]} EV {f_m(sv[s]['ev'])} = {usd(sv[s]['vps'])}" for s in f3.SEGS) +
       f" | suma {f_m(tot)} frente a EV del modelo {f_m(R[k]['ev'])}")

# =============================================================================================
h("2. TESIS ALCISTA: cifras de cada argumento")
# A1 SI: escala
RR_SI0 = f3.RR0["si"]
RR_OBJ_SI = OBJ_RR_DIC26 - 4 * f3.OTROS_Q3
pr(f"A1 RR SI 3T26 {f_m(RR_SI0)} | RR SI que implica la guía 1T27: bajo {f_m(f3.GUIA_SI_RR['bajo'])} (x{f_m(f3.GUIA_SI_RR['bajo'] / RR_SI0, 2)}), "
   f"medio {f_m(f3.GUIA_SI_RR['medio'])} (x{f_m(f3.GUIA_SI_RR['medio'] / RR_SI0, 2)}) | objetivo 100.000 M$ anualizados en dic-2026 -> RR SI "
   f"{f_m(RR_OBJ_SI)} si Space+Connectivity siguen al nivel del 3T26 ({f_m(f3.OTROS_Q3)} por trimestre)")
pr(f"   Backlog 3T26 {f_m(BACKLOG_3T26)} | margen EBITDA aj. SI 3T26 {f_p(rat('margen_ebitda_aj_si', 'Q3_2026'))} | margen incremental 1T->3T26 "
   f"{f_p(rat('margen_incremental_ebitda_aj_si', 'Q1_2026->Q3_2026'))}")
V_GUIA_MEDIO = vps(f3.base_var(si__credito_guia=1.0, si__guia="medio"))
V_M655 = vps(f3.base_var(si__m_obj=rat("margen_ebitda_aj_si", "Q3_2026")))
pr(f"   Base con el 100 % del punto medio de la guía: {usd(V_GUIA_MEDIO)} | base con margen SI objetivo = 3T26 "
   f"({f_p(rat('margen_ebitda_aj_si', 'Q3_2026'))}): {usd(V_M655)}")
# A2 Capex de crecimiento
V_K09 = vps(f3.base_var(si__k=0.90))
V_K10 = vps(f3.base_var(si__k=1.0))
ING_W = {k_: f3.CAPEX_POR_W / k_ for k_ in (0.90, 1.0, 1.25, round(f3.K_OBS["si"], 2))}
pr(f"A2 Capex SI 9M26 / aumento de GW = {f_m(f3.CAPEX_POR_W, 1)} $/W | ingreso anual por vatio que implica k: " +
   " | ".join(f"k {f_m(k_, 2)} -> {f_m(x, 1)} $/W" for k_, x in ING_W.items()))
pr(f"   Base con k SI 0,90 (el del alcista): {usd(V_K09)} | k 1,0: {usd(V_K10)} | alcista {usd(R['alcista']['vps'])}")
# A3 Connectivity
CON = "connectivity"
pr(f"A3 Connectivity: ingresos 3T26 {f_m(f3.REV_Q3[CON])} ({f_p(rat('crec_ing_connectivity', 'Q3_2026/Q3_2025'))} interanual) | margen EBITDA aj. 3T26 "
   f"{f_p(rat('margen_ebitda_aj_connectivity', 'Q3_2026'))} | EBITDA aj. - capex TTM {f_m(rat('ebitda_aj_menos_capex_connectivity', 'TTM_Q3_2026'))} | "
   f"suscriptores {f_m(SUBS['3T25'], 1)} -> {f_m(SUBS['3T26'], 1)} M ({f_p(SUBS['3T26'] / SUBS['3T25'] - 1)})")
V_CON_ALC = vps(f3.base_var(connectivity__g1=SC["alcista"][CON]["g1"], connectivity__gmid=SC["alcista"][CON]["gmid"],
                            connectivity__m_obj=SC["alcista"][CON]["m_obj"], connectivity__k=SC["alcista"][CON]["k"]))
pr(f"   Valor de Connectivity sola (base) {f_m(SEGV['base'][CON]['ev'])} = {usd(SEGV['base'][CON]['vps'])} | base con Connectivity del alcista: {usd(V_CON_ALC)}")
# A4 Space / Starship
V_SP_ALC = vps(f3.base_var(space__g1=SC["alcista"]["space"]["g1"], space__gmid=SC["alcista"]["space"]["gmid"],
                           space__m_obj=SC["alcista"]["space"]["m_obj"], space__capex_norm=SC["alcista"]["space"]["capex_norm"],
                           space__anio_norm=SC["alcista"]["space"]["anio_norm"], space__sbc_obj=SC["alcista"]["space"]["sbc_obj"]))
pr(f"A4 Space: valor de Space solo (base) {f_m(SEGV['base']['space']['ev'])} = {usd(SEGV['base']['space']['vps'])}; (alcista) "
   f"{f_m(SEGV['alcista']['space']['ev'])} = {usd(SEGV['alcista']['space']['vps'])} | base con Space del alcista: {usd(V_SP_ALC)} "
   f"({'+' if V_SP_ALC >= BASE_VPS else ''}{f_m(V_SP_ALC - BASE_VPS, 2)} $)")
# A5 Balance
CAJA_NETA_ACC = f3.NETCASH0 / f3.SH_DIL
pr(f"A5 Caja + valores {f_m(f3.CASH0)} | caja neta {f_m(f3.NETCASH0)} = {usd(CAJA_NETA_ACC)} por acción diluida | FCFF acumulado mínimo: " +
   " | ".join(f"{k} {f_m(R[k]['fcff_acum_min'])} ({f_p(-R[k]['fcff_acum_min'] / f3.CASH0)} de la caja)" for k in R))

# =============================================================================================
h("3. TESIS BAJISTA: cifras de cada argumento")
B_RR = f3.B_RR0
B_MES = f3.B_Q3 / 3
pr(f"B1 Customer B 3T26 {f_m(f3.B_Q3)} M$ ({f_p(B_PCT_3T26)} de los ingresos; A+B {f_p(B_PCT_3T26 + A_PCT_3T26)}) | RR {f_m(B_RR)} = "
   f"{f_p(B_RR / RR_SI0)} del RR de SI | {f_m(B_MES)} M$/mes frente a {f_m(CONTRATO_P2_MES)} del contrato de P2 (exceso {f_m(B_MES - CONTRATO_P2_MES)} M$/mes)")
B_SIN_GUIA = f3.B_SENS[3][1]
B_RESC = f3.B_SENS[1][1]
B_RESC_SIN_SUELO = vps(f3.base_var(si__b="rescinde", si__reventa_b=0.5, si__g1_sin_b=0.30, si__credito_guia=0.0, si__w1=0.5,
                                   si__suelo_capex1=None, si__recorte_b_a3=0.0))
pr(f"   Descomposición de los {f_m(f3.B_VALOR_BASE, 2)} $ de la Fase 3: base {usd(BASE_VPS)} -> sin crédito a la guía {usd(B_SIN_GUIA)} "
   f"({f_m(B_SIN_GUIA - BASE_VPS, 2)}) -> B rescinde sin suelo de capex {usd(B_RESC_SIN_SUELO)} ({f_m(B_RESC_SIN_SUELO - B_SIN_GUIA, 2)}) -> "
   f"con suelo de compromisos {usd(B_RESC)} ({f_m(B_RESC - B_RESC_SIN_SUELO, 2)})")
pr(f"   Bajista {usd(R['bajista']['vps'])} = {f_p(R['bajista']['vps'] / f3.PRICE - 1)} frente al precio")
V_KOBS = f3.DRIVERS[0][1][2]
CAPEX_A1 = {k: R[k]["tot"]["capex"][0] for k in R}
pr(f"B2 Capex TTM {f_m(f3.CAPEX0_TOT)} = {f_p(f3.CAPEX0_TOT / f3.REV0_TOT)} de los ingresos | FCF TTM {f_m(f3.FCF0)} | k SI observado "
   f"{f_m(f3.K_OBS['si'], 3)} -> base {usd(V_KOBS)} | capex SI A1 al ritmo de la guía -> {usd(f3.VPS_CAPEX_GUIA)}")
V_CON_BAJ = vps(f3.base_var(connectivity__g1=SC["bajista"][CON]["g1"], connectivity__gmid=SC["bajista"][CON]["gmid"],
                            connectivity__m_obj=SC["bajista"][CON]["m_obj"], connectivity__k=SC["bajista"][CON]["k"]))
pr(f"B3 ARPU {f_m(ARPU['3T25'], 0)} -> {f_m(ARPU['3T26'], 0)} $/mes ({f_p(ARPU['3T26'] / ARPU['3T25'] - 1)}); FY2024 {f_m(ARPU['FY2024'], 0)} -> "
   f"FY2025 {f_m(ARPU['FY2025'], 0)} ({f_p(ARPU['FY2025'] / ARPU['FY2024'] - 1)}) | base con Connectivity del bajista: {usd(V_CON_BAJ)} "
   f"({f_m(V_CON_BAJ - BASE_VPS, 2)} $)")
V_SP_BAJ = vps(f3.base_var(space__g1=SC["bajista"]["space"]["g1"], space__gmid=SC["bajista"]["space"]["gmid"],
                           space__m_obj=SC["bajista"]["space"]["m_obj"], space__capex_norm=SC["bajista"]["space"]["capex_norm"],
                           space__anio_norm=SC["bajista"]["space"]["anio_norm"], space__sbc_obj=SC["bajista"]["space"]["sbc_obj"]))
pr(f"B4 Space: margen operativo TTM {f_p(rat('margen_operativo_space', 'TTM_Q3_2026'))} | I+D/ingresos TTM {f_p(rat('id_sobre_ingresos_space', 'TTM_Q3_2026'))} | "
   f"ingresos 9M26 {f_p(rat('crec_ing_space', '9M2026/9M2025'))} | base con Space del bajista: {usd(V_SP_BAJ)} ({f_m(V_SP_BAJ - BASE_VPS, 2)} $) | "
   f"Space solo en el base {usd(SEGV['base']['space']['vps'])}")
INT_ANUAL_Q3 = 4 * INT_VINC_Q3 / DEUDA_VINC
pr(f"B5 SBC TTM {f_m(f3.SBC0_TOT)} = {f_p(rat('sbc_sobre_ingresos', 'TTM_Q3_2026'))} de los ingresos | Cursor pendiente {f_m(CURSOR_SBC)} = "
   f"{usd(CURSOR_SBC / f3.SH_DIL)} por acción diluida (sin descontar) | intereses con Valor 3T26 x 4 / deuda vinculada = {f_p(INT_ANUAL_Q3)} "
   f"frente al cupón {f_p(f3.CUPON_NOTES, 3)} de los Notes")

# =============================================================================================
h("4. SEÑALES: umbrales por escenario")
for k in ("bajista", "base", "alcista"):
    g1 = SC[k][CON]["g1"]
    q4 = f3.REV_Q3[CON] * (1 + g1) ** 0.25
    q7 = f3.REV_Q3[CON] * (1 + g1)
    pr(f"S-Conn {k}: ingresos Connectivity 4T26 ~{f_m(q4)} | 3T27 ~{f_m(q7)} (3T26 x (1+g1)^(q/4); g1 {f_p(g1, 0)})")
ARPU_Q_RITMO = ARPU["3T26"] * (ARPU["3T26"] / ARPU["3T25"]) ** 0.25
pr(f"S-ARPU: ARPU 4T26 si sigue el ritmo interanual de {f_p(ARPU['3T26'] / ARPU['3T25'] - 1)}: {f_m(ARPU_Q_RITMO, 1)} $/mes (3T26 {f_m(ARPU['3T26'], 0)}; 9M26 {f_m(ARPU['9M26'], 0)})")
Q1_27 = {}
for k in ("bajista", "base", "alcista"):
    rr1_si = R[k]["segs"]["si"]["rr"][0]
    con = f3.REV_Q3[CON] * (1 + SC[k][CON]["g1"]) ** 0.5
    sp = f3.REV0["space"] / 4 * (1 + SC[k]["space"]["g1"]) ** 0.5
    Q1_27[k] = rr1_si / 4 + con + sp
    pr(f"S-1T27 {k}: SI ~{f_m(rr1_si / 4)} (RR fin A1 {f_m(rr1_si)} / 4) + Connectivity ~{f_m(con)} + Space ~{f_m(sp)} = grupo ~{f_m(Q1_27[k])}")
pr(f"   Guía 1T27 (S7/S9): {f_m(f3.MKT['guia_ing_1T27_bajo'][0])}-{f_m(f3.MKT['guia_ing_1T27_alto'][0])}")
pr(f"S-B: B 3T26 {f_m(f3.B_Q3)} | mitad {f_m(f3.B_Q3 / 2)} | % de B si los ingresos del trimestre llegan a 33.000 y B no cambia: {f_p(f3.B_Q3 / f3.MKT['guia_ing_1T27_bajo'][0])} | "
   f"% si llegan al 1T27 del base: {f_p(f3.B_Q3 / Q1_27['base'])}")
CAPEX_Q3 = sum(v(f'capex_{s}', 'Q3_2026') for s in f3.SEGS)  # 19.593 (P3 Note 18, vía Fase 2)
GUIA_CAPEX_MED = (f3.MKT["guia_capex_4T26_bajo"][0] + f3.MKT["guia_capex_4T26_alto"][0]) / 2
for k in ("bajista", "base", "alcista"):
    resto = CAPEX_A1[k] - GUIA_CAPEX_MED
    pr(f"S-Capex {k}: capex A1 (oct-26 a sep-27) {f_m(CAPEX_A1[k])} | si el 4T26 es {f_m(GUIA_CAPEX_MED)}, quedan {f_m(resto)} para 1T-3T27 = "
       f"{f_m(resto / 3)} por trimestre (3T26: {f_m(CAPEX_Q3)}; {f_p(resto / 3 / CAPEX_Q3 - 1)})")
for k in ("bajista", "base", "alcista"):
    m = R[k]["segs"]["si"]["marg"]
    pr(f"S-Margen SI {k}: A1 {f_p(m[0])} | A3 {f_p(m[2])}")
for k in ("bajista", "base", "alcista"):
    pr(f"S-Caja {k}: caja + valores a fin de A1 ~{f_m(f3.CASH0 + R[k]['tot']['fcff'][0])} (sin intereses, financiación ni pago a EchoStar) | "
       f"mínimo {f_m(f3.CASH0 + R[k]['fcff_acum_min'])}")
pr("S-Vida útil (10-K): " + " | ".join(f"L = {L} -> {usd(x)}" for L, x in f3.L_SENS))
for k in ("bajista", "base", "alcista"):
    sp = R[k]["segs"]["space"]
    pr(f"S-Space {k}: crecimiento A1 {f_p(SC[k]['space']['g1'], 0)} y A2-A5 {f_p(SC[k]['space']['gmid'][0], 0)} | margen EBITDA aj. A5 {f_p(sp['marg'][4])}")
pr(f"S-100.000 M$: dic-2026 x 12 >= 100.000 equivale a ingresos de diciembre >= {f_m(OBJ_RR_DIC26 / 12)}; trimestre 4T26 de referencia {f_m(OBJ_RR_DIC26 / 4)} "
   f"si el ritmo fuese uniforme (3T26: {f_m(v('ingresos_totales', 'Q3_2026'))})")

# =============================================================================================
h("5. ABOGADO DEL DIABLO contra el caso base")
# 5.1 Capex
base = R["base"]
pr(f"5.1 Capex A1 base {f_m(CAPEX_A1['base'])}; capex SI A1 {f_m(base['segs']['si']['capex'][0])} frente a SI TTM {f_m(f3.CAPEX0['si'])}")
V_GUIA_2A = vps(bv(suelos={0: f3.CAPEX_SI_A1_GUIA, 1: f3.CAPEX_SI_A1_GUIA}))
pr(f"    Capex SI al ritmo de la guía ({f_m(f3.CAPEX_SI_A1_GUIA)}/año) en A1: {usd(f3.VPS_CAPEX_GUIA)} | en A1 y A2: {usd(V_GUIA_2A)} (mismos ingresos)")
CAPEX_13GW = (GW_FIN_2027 - GW_3T26) * 1000 * f3.CAPEX_POR_W
RW_ACT = RR_SI0 / (GW_3T26 * 1000)
pr(f"    13 GW a fin de 2027: {f_m(GW_FIN_2027 - GW_3T26, 1)} GW nuevos x {f_m(f3.CAPEX_POR_W, 1)} $/W = {f_m(CAPEX_13GW)} M$ de capex "
   f"({f_m(CAPEX_13GW / f3.CASH0, 1)} veces la caja + valores; {f_m(CAPEX_13GW / CAPEX_A1['base'], 1)} veces el capex A1 base)")
pr(f"    Ingreso de SI por vatio instalado hoy: RR SI / GW = {f_m(RW_ACT, 1)} $/W; RR SI con 13 GW a ese ritmo {f_m(RW_ACT * GW_FIN_2027 * 1000)} | "
   f"a 35,6 $/W (k 1,25) {f_m(ING_W[1.25] * GW_FIN_2027 * 1000)} | RR SI fin A1: base {f_m(base['segs']['si']['rr'][0])}, alcista {f_m(R['alcista']['segs']['si']['rr'][0])}")
# 5.2 k
K_ACT = f3.CAPEX_POR_W / RW_ACT
V_K_ACT = vps(f3.base_var(si__k=K_ACT))
K_GRID = [0.90, 1.0, 1.25, 1.5, round(f3.K_OBS["si"], 2), 2.0]
pr(f"5.2 k implícito con el ingreso por vatio actual: {f_m(K_ACT, 2)} -> base {usd(V_K_ACT)} | rejilla: " +
   " | ".join(f"k {f_m(k_, 2)} -> {usd(vps(f3.base_var(si__k=k_)))}" for k_ in K_GRID))
K_BE = f3.solve(lambda k_: vps(f3.base_var(si__k=k_)), 0.05, 3.0, 0.0)
pr(f"    k que lleva el base a 0 $: {f_m(K_BE, 2) if K_BE else 'sin solución en 0,05-3'}")
# 5.3 WACC / beta
alt = {}
for lab, kw in (("ERP 3,30 % (mín. D1)", dict(erp=0.0330)), ("ERP 5,67 % (máx. D1)", dict(erp=0.0567)),
                ("rf 5,33 % (30 años, M2)", dict(rf=0.0533)),
                ("beta regresión QQQ 1,83 (sin Blume)", dict(beta0=f3.BETA_REG_QQQ)),
                ("beta regresión SPY sin 1.ª semana 2,77", dict(beta0=f3.BETA_REG_SPY_X1S)),
                ("beta 1,0 (mercado)", dict(beta0=1.0))):
    w0, wt = wacc_from(**kw)
    alt[lab] = (w0, wt, vps(SC["base"], w0=w0, wt=wt))
    pr(f"5.3 {lab}: WACC0 {f_p(w0, 2)} / WACC_T {f_p(wt, 2)} -> base {usd(alt[lab][2])}")
for lab, w in f3.WACC_ALT.items():
    pr(f"    Fase 3 {lab}: WACC0 {f_p(w, 2)} -> {usd(f3.WACC_ALT_VPS[lab])}")
pr(f"    Peso de SI en la beta (ingresos A1 base): {f_p(f3.W_SEG['si'])}; beta desapalancada SI {f_m(f3.BU_SEG['si']['bu'], 3)} "
   f"(Damodaran {f_m(f3.BU_SEG['si']['damo'], 3)}, comparables {f_m(f3.BU_SEG['si']['peers'], 3)}, n = {f3.BU_SEG['si']['n']})")
# 5.4 Customer B
V_B_NO_RENUEVA = vps(f3.base_var(si__recorte_b_a3=1.0))
V_B_RENUEVA_50 = vps(f3.base_var(si__recorte_b_a3=0.5))
pr(f"5.4 B no renueva en A3 (sin recolocación): {usd(V_B_NO_RENUEVA)} | renueva con -50 %: {usd(V_B_RENUEVA_50)} | sin recorte {usd(f3.B_SENS[4][1])}")
for p in (0.25, 0.5):
    pr(f"    Ponderado con probabilidad de rescisión en A1 de {f_p(p, 0)}: {usd((1 - p) * BASE_VPS + p * B_RESC)}")
pr(f"    B rescinde pero se mantiene el resto de la guía (Fase 3): {usd(f3.B_SENS[2][1])} ({f_m(f3.B_SENS[2][1] - BASE_VPS, 2)} $)")
_RESC = dict(si__b="rescinde", si__reventa_b=0.5, si__g1_sin_b=0.30, si__credito_guia=0.0, si__w1=0.5,
             si__suelo_capex1=f3.COMPROMISOS_NC, si__recorte_b_a3=0.0)
for m_ in (0.40, 0.30):
    pr(f"    B rescinde en A1 (variante de 03) y además el margen objetivo de SI baja al {f_p(m_, 0)}: {usd(vps(f3.base_var(**_RESC, si__m_obj=m_)))}")
chk("variante _RESC reproduce 20,08 $", abs(vps(f3.base_var(**_RESC)) - B_RESC) < 1e-9)
# 5.5 Valor terminal
TV_EBITDA11 = base["tv"] / base["tot"]["ebitda"][f3.N]
TV_EBITDA10 = base["tv"] / base["tot"]["ebitda"][f3.N - 1]
TV_FCFF = base["tv"] / base["fcff11"]
pr(f"5.5 VT base {f_m(base['tv'])} = {f_m(TV_EBITDA10, 2)}x EBITDA aj. A10 ({f_m(base['tot']['ebitda'][f3.N - 1])}) = {f_m(TV_EBITDA11, 2)}x EBITDA A11 = "
   f"{f_m(TV_FCFF, 1)}x FCFF A11 | VA años 1-10 {f_m(base['pv_sum'])}")
V_SIN_VT = (base["pv_sum"] + f3.NETCASH0 + f3.EQ_AJUSTE["diluida"]) / f3.SH_DIL
pr(f"    vpa sin valor terminal: {usd(V_SIN_VT)} | parte del EV de mercado que no cubren los FCFF A1-A10 del base: {f_p(1 - base['pv_sum'] / f3.EV_MKT)}")


def vps_exit(res, m):
    ev = res["pv_sum"] + m * res["tot"]["ebitda"][f3.N - 1] * res["dfs"][-1]
    return (ev + f3.NETCASH0 + f3.EQ_AJUSTE["diluida"]) / f3.SH_DIL


MED_CON = f3.MED["connectivity"]["ev_ebitda"][0]
MED_SI = f3.MED["si"]["ev_ebitda"][0]
EXITS = [("Gordon implícito", TV_EBITDA10), ("10x", 10.0), (f"mediana Connectivity {f_m(MED_CON, 2)}x", MED_CON),
         (f"mediana SI {f_m(MED_SI, 2)}x", MED_SI)]
pr("    Valor de salida en A10 = múltiplo x EBITDA aj. A10: " + " | ".join(f"{lab} -> {usd(vps_exit(base, m))}" for lab, m in EXITS))
M_PRECIO = f3.solve(lambda m: vps_exit(base, m), 0.0, 500.0, f3.PRICE)
pr(f"    Múltiplo de salida en A10 que lleva el base a {usd(f3.PRICE)}: {f_m(M_PRECIO, 1)}x | en el alcista: "
   f"{f_m(f3.solve(lambda m: vps_exit(R['alcista'], m), 0.0, 500.0, f3.PRICE), 1)}x (Gordon alcista {f_m(R['alcista']['tv'] / R['alcista']['tot']['ebitda'][f3.N - 1], 2)}x)")
# 5.6 Base de acciones
EQ = base["eq_diluida"]
SH_1333 = f3.SH_DIL + PREMIOS_NO_CUMPLIDOS
SH_31 = f3.SH_DIL + (PREMIOS_NO_CUMPLIDOS - f3.MUSK_RESTRINGIDAS)
SH_SIN_M = f3.SH_DIL - f3.MUSK_RESTRINGIDAS
pr(f"5.6 Acciones: diluida {f_m(f3.SH_DIL, 2)} -> {usd(EQ / f3.SH_DIL)} | + {f_m(PREMIOS_NO_CUMPLIDOS, 0)} M premios ({f_m(SH_1333, 2)}): {usd(EQ / SH_1333)} | "
   f"+ solo {f_m(PREMIOS_NO_CUMPLIDOS - f3.MUSK_RESTRINGIDAS, 2)} M (si los 1.333 incluyen las de Musk): {usd(EQ / SH_31)} | diluida sin las restringidas de Musk "
   f"({f_m(SH_SIN_M, 2)}): {usd((EQ) / SH_SIN_M)}")
DIL2_A = (f3.OPC_RSU + PREMIOS_NO_CUMPLIDOS + f3.ECHOSTAR_ACC) / v("acciones_ordinarias_total", "9M2026")
DIL2_B = (f3.OPC_RSU + PREMIOS_NO_CUMPLIDOS - f3.MUSK_RESTRINGIDAS + f3.ECHOSTAR_ACC) / v("acciones_ordinarias_total", "9M2026")
pr(f"    Dilución potencial sobre {f_m(v('acciones_ordinarias_total', '9M2026'), 0)} M (30-sep): con los 1.333 enteros {f_p(DIL2_A)} | sin las 1.302,07 de Musk ya emitidas {f_p(DIL2_B)}")
# 5.7 Combinaciones
w0_d = f3.WACC_ALT["solo Damodaran (ponderada)"]
w0_c = f3.WACC_ALT["solo comparables (ponderada)"]
V_UP = with_L(6, lambda: vps(f3.base_var(si__credito_guia=1.0, si__guia="medio"), w0=w0_d, wt=f3.WACC_T + (w0_d - f3.WACC0)))
V_DOWN = vps(bv(si__k=round(f3.K_OBS["si"], 2), si__recorte_b_a3=1.0, suelos={0: f3.CAPEX_SI_A1_GUIA}),
             w0=w0_c, wt=f3.WACC_T + (w0_c - f3.WACC0))
pr(f"5.7 Combinación al alza (guía 100 % punto medio + L 6 + WACC solo Damodaran): {usd(V_UP)}")
pr(f"    Combinación a la baja (k observado + B no renueva en A3 + capex SI A1 al ritmo de la guía + WACC solo comparables): {usd(V_DOWN)}")

V_RESC_M = {m_: vps(f3.base_var(**_RESC, si__m_obj=m_)) for m_ in (0.40, 0.30)}
pr("5.8 Pérdida frente al precio: " + " | ".join(f"{lab} {usd(x)} -> {f_p(x / f3.PRICE - 1)}" for lab, x in (
    ("combinación a la baja", V_DOWN), ("k observado", V_KOBS), ("bajista", R["bajista"]["vps"]))))
pr("    Efecto desde el base de B rescinde + margen SI: " + " | ".join(f"{f_p(m_, 0)} -> {f_m(x - BASE_VPS, 2)} $" for m_, x in V_RESC_M.items()))
MSFT_ING_TTM = 331840.0   # M$, stockanalysis.com (S6), citado en 03 §6
pr(f"    Ingresos A10 del alcista ampliado / ingresos TTM de Microsoft: {f_m(f3.REV_LAMBDA_BULL_RES['tot']['rev'][f3.N - 1] / MSFT_ING_TTM, 2)}x")

# =============================================================================================
h("6. QUÉ TENDRÍA QUE PASAR PARA 147,49 $ (DCF inverso de la Fase 3 y combinaciones)")
pr(f"Fase 3: crecimiento x{f_m(f3.REV_LAMBDA, 3)} -> ingresos A10 {f_m(f3.REV_LAMBDA_RES['tot']['rev'][f3.N - 1])} (TACC {f_p(f3._cagr(f3.REV_LAMBDA_RES))}) | "
   f"WACC0 {f_p(f3.REV_WACC, 2)} | desde el alcista x{f_m(f3.REV_LAMBDA_BULL, 3)} -> {f_m(f3.REV_LAMBDA_BULL_RES['tot']['rev'][f3.N - 1])} | margen SI alcista "
   f"{f_p(f3.REV_MARGIN_SI_BULL)}")
lo_b = f3.WACC0 - f3.WACC_T + SC["alcista"]["g_term"] + 0.0025
W_BULL = f3.solve(lambda w: vps(SC["alcista"], w0=w, wt=f3.WACC_T + (w - f3.WACC0)), lo_b, 0.20, f3.PRICE)
_KE_BULL = (W_BULL - f3.KD * f3.W_D) / (1 - f3.W_D)
pr(f"Alcista: WACC0 que iguala el precio {f_p(W_BULL, 2)} (coste del capital {f_p(_KE_BULL, 2)}; beta0 implícita con rf y ERP de 03: "
   f"{f_m((_KE_BULL - f3.RF) / f3.ERP, 3)}; WACC terminal desplazado igual)")
V_BULL_D = vps(SC["alcista"], w0=w0_d, wt=f3.WACC_T + (w0_d - f3.WACC0))
V_BULL_L6 = with_L(6, lambda: vps(SC["alcista"]))
V_BULL_L6_D = with_L(6, lambda: vps(SC["alcista"], w0=w0_d, wt=f3.WACC_T + (w0_d - f3.WACC0)))
SC_BULL_M = dict(SC["alcista"], si=dict(SC["alcista"]["si"], m_obj=rat("margen_ebitda_aj_si", "Q3_2026")))
V_BULL_M = vps(SC_BULL_M)
V_BULL_ALL = with_L(6, lambda: vps(SC_BULL_M, w0=w0_d, wt=f3.WACC_T + (w0_d - f3.WACC0)))
pr(f"Alcista + WACC solo Damodaran: {usd(V_BULL_D)} | alcista + L 6: {usd(V_BULL_L6)} | alcista + L 6 + Damodaran: {usd(V_BULL_L6_D)} | "
   f"alcista con margen SI del 3T26: {usd(V_BULL_M)} | las tres cosas a la vez: {usd(V_BULL_ALL)}")
REV_A10_BULL = R["alcista"]["tot"]["rev"][f3.N - 1]
pr(f"Ingresos A10: alcista {f_m(REV_A10_BULL)} | x{f_m(f3.REV_LAMBDA_BULL, 3)} del alcista {f_m(f3.REV_LAMBDA_BULL_RES['tot']['rev'][f3.N - 1])}")

# =============================================================================================
h("7. GOBIERNO CORPORATIVO Y PARTES VINCULADAS")
pr(f"Voto de Musk: {f_p(VOTO_MUSK_P2)} (P2) / ~{f_p(VOTO_MUSK_EST)} (estimación 01, SIN VERIFICAR) | acciones B restringidas {f_m(f3.MUSK_RESTRINGIDAS, 2)} M = "
   f"{f_p(f3.MUSK_RESTRINGIDAS / f3.SH_COVER)} de la portada")
EXCESO_VALOR = (INT_ANUAL_Q3 - f3.CUPON_NOTES) * DEUDA_VINC
pr(f"Valor: intereses 3T26 {f_m(INT_VINC_Q3)} | 9M26 {f_m(INT_VINC_9M)} | deuda {f_m(DEUDA_VINC)} ({f_p(rat('peso_deuda_vinculada', '9M2026'))}) | "
   f"tipo anualizado 3T26 {f_p(INT_ANUAL_Q3)} | sobrecoste frente al cupón de los Notes {f_m(EXCESO_VALOR)} M$/año = {usd(EXCESO_VALOR / f3.SH_DIL, 3)} por acción y año")
for pct in (0.05, 0.10):
    pr(f"Fusión con Tesla: transferir un {f_p(pct, 0)} del valor de SpaceX en la relación de canje = {f_m(pct * f3.MCAP)} M$ a precio de mercado "
       f"({usd(pct * f3.PRICE)} por acción) | {usd(pct * BASE_VPS)} por acción sobre el base")

# =============================================================================================
h("8. PUNTOS PENDIENTES DE FASES ANTERIORES")
pr(f"Apertura 12-jun-2026: M1 {usd(APERTURA_12JUN_M1)} frente a S1 {usd(APERTURA_12JUN_S1)} (01 §6.1); cierre M1 {usd(CIERRE_12JUN)} | "
   f"diferencia {f_p(APERTURA_12JUN_S1 / APERTURA_12JUN_M1 - 1)}; rentabilidad del primer día sobre la OPV (135 $): apertura {f_p(APERTURA_12JUN_M1 / 135 - 1)}, "
   f"cierre {f_p(CIERRE_12JUN / 135 - 1)}")
pr(f"Premios: 1.333 M (P3 Note 13) - 1.302,07 M de Musk = {f_m(PREMIOS_NO_CUMPLIDOS - f3.MUSK_RESTRINGIDAS, 2)} M; dilución potencial 02 §7 "
   f"{f_p(DIL2_A)} frente a {f_p(DIL2_B)}")

# =============================================================================================
h("9. CONTROLES")
chk("vpa base de la Fase 3 = 25,27 $ (03 §4.1)", f_m(BASE_VPS, 2) == "25,27")
chk("vpa bajista / alcista = 0,61 / 99,74 $", f_m(R["bajista"]["vps"], 2) == "0,61" and f_m(R["alcista"]["vps"], 2) == "99,74")
chk("VT/EV base = 86,7 %", f_p(R["base"]["tv_share"]) == "86,7 %")
chk("beta0 = 1,112", f_m(f3.BETA0, 3) == "1,112")
chk("descomposición de B suma el total", abs((B_SIN_GUIA - BASE_VPS) + (B_RESC_SIN_SUELO - B_SIN_GUIA) + (B_RESC - B_RESC_SIN_SUELO) + f3.B_VALOR_BASE) < 1e-9)
chk("wacc_from() reproduce el WACC de la Fase 3", abs(wacc_from()[0] - f3.WACC0) < 1e-12 and abs(wacc_from()[1] - f3.WACC_T) < 1e-12)
chk("wacc_from(beta0=Blume) reproduce WACC0 Blume de la Fase 3",
    abs(wacc_from(beta0=f3.BETA_BLUME)[0] - f3.WACC_ALT["regresión SPCX vs SPY (Blume)"]) < 1e-12)
chk("salida a múltiplo Gordon implícito = vpa base", abs(vps_exit(base, TV_EBITDA10) - BASE_VPS) < 1e-9)
chk("L_SEG restaurado", f3.L_SEG["si"] == 5)
chk("envoltorio: base sigue igual al final", abs(vps(SC["base"]) - BASE_VPS) < 1e-9)
chk("13 GW > 1,7 GW", GW_FIN_2027 > GW_3T26)
for n_, ok in CHECKS:
    pr(f"  {'OK' if ok else 'FALLO'} {n_}")
assert all(ok for _, ok in CHECKS), [n_ for n_, ok in CHECKS if not ok]
pr(f"TOTAL controles {len(CHECKS)}: OK {sum(ok for _, ok in CHECKS)}")
