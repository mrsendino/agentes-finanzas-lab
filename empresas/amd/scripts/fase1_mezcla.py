"""Fase 1 (Negocio) - AMD: mezcla por segmentos, márgenes y otras proporciones.

Todas las cifras de entrada están en millones de USD (salvo acciones, en millones) y se copian
literalmente de las fuentes primarias indicadas en cada bloque (IDs de fuentes/fuentes.md).
El script solo hace aritmética; imprime los resultados y los guarda en data/fase1_mezcla.csv.

Uso:  python empresas/amd/scripts/fase1_mezcla.py
"""
import csv
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(BASE, "data", "fase1_mezcla.csv")

# --- P1: 10-K FY2025, Note 4 Segment Reporting y Item 7 (tabla por segmentos) -------------
FY25 = {
    "ingresos": {"Data Center": 16635, "Client": 10640, "Gaming": 3910,
                 "Client and Gaming": 14550, "Embedded": 3454},
    "total_ingresos": 34639,
    "res_op": {"Data Center": 3603, "Client and Gaming": 2855, "Embedded": 1243,
               "All Other": -4007},
    "total_res_op": 3694,
}
FY24 = {
    "ingresos": {"Data Center": 12579, "Client": 7054, "Gaming": 2595,
                 "Client and Gaming": 9649, "Embedded": 3557},
    "total_ingresos": 25785,
    "res_op": {"Data Center": 3482, "Client and Gaming": 1187, "Embedded": 1421,
               "All Other": -4190},
    "total_res_op": 1900,
}
# All Other FY2025 (P1, Note 4): amortización de intangibles y SBC
FY25_AMORT = 2254
FY25_SBC = 1638
# P1: geografía por ubicación de facturación (Note 4)
FY25_GEO = {"Estados Unidos": 11363, "China (incl. Hong Kong)": 7751, "Taiwán": 5186,
            "Singapur": 4284, "Otras regiones": 6055}
# P1: estado de flujos de caja; P5 (8-K Q4 2025 Ex. 99.1): no-GAAP
FY25_RECOMPRAS = 1316          # Repurchases of common stock
FY25_RETENCION = 607           # Stock repurchases for tax withholding
FY25_CFO_CONT = 6493           # Net cash provided by operating activities (continuing)
FY25_CAPEX = 974               # Purchases of property and equipment (continuing)
FY25_RES_OP_NONGAAP = 7768     # P5
FY25_BN_GAAP = 4335            # P1
FY25_BN_NONGAAP = 6831         # P5
# P1: balance a 27-dic-2025
FY25_GOODWILL = 25126
FY25_INTANG = 16705
FY25_ACTIVO = 76926

# --- P2: 10-Q Q2 2026 (trimestre a 27-jun-2026), Note 4 Segment Reporting ---------------
Q2_26 = {
    "ingresos": {"Data Center": 6718, "Client": 3062, "Gaming": 779,
                 "Client and Gaming": 3841, "Embedded": 977},
    "total_ingresos": 11536,
    "res_op": {"Data Center": 2103, "Client and Gaming": 582, "Embedded": 386,
               "All Other": -1081},
    "total_res_op": 1990,
}
Q2_25 = {
    "ingresos": {"Data Center": 3240, "Client": 2499, "Gaming": 1122,
                 "Client and Gaming": 3621, "Embedded": 824},
    "total_ingresos": 7685,
    "res_op": {"Data Center": -155, "Client and Gaming": 767, "Embedded": 275,
               "All Other": -1021},
    "total_res_op": -134,
}
H1_26 = {
    "ingresos": {"Data Center": 12493, "Client": 5947, "Gaming": 1499,
                 "Client and Gaming": 7446, "Embedded": 1850},
    "total_ingresos": 21789,
    "res_op": {"Data Center": 3702, "Client and Gaming": 1157, "Embedded": 724,
               "All Other": -2117},
    "total_res_op": 3466,
}
Q2_26_AMORT = 544              # P2 nota (1) de la tabla de segmentos
Q2_26_SBC = 503
Q2_26_RES_OP_NONGAAP = 3094    # P6 (8-K Q2 2026 Ex. 99.1)
Q2_26_GOODWILL = 25470         # P2 balance
Q2_26_INTANG = 15635
Q2_26_ACTIVO = 84464
H1_26_CFO = 5321               # P2 estado de flujos
H1_26_CAPEX = 1197
H1_26_RECOMPRAS = 221
H1_26_SBC = 990
COMPROMISOS_FY25 = 12200       # P1 Item 7 ("approximately $12.2 billion")
COMPROMISOS_Q2_26 = 30276      # P2 Note 10, tabla de compromisos incondicionales

# --- Warrants y adquisiciones (P2 Note 11; P7, P8; P9) ----------------------------------
ACCIONES_EN_CIRCULACION_29JUL26 = 1632.475042   # P2 portada: 1,632,475,042 acciones
WARRANT_OPENAI = 160.0                          # millones de acciones
WARRANT_META = 160.0
ACCIONES_FY25_FIN = 1630                        # P1 Note 12
ACCIONES_FY24_FIN = 1622

# --- Competidores (XBRL de sus 10-K; S-IDs en fuentes.md) -------------------------------
NVDA_FY26_INGRESOS = 215938    # P10: Nvidia, ejercicio cerrado 25-ene-2026
INTC_FY25_INGRESOS = 52853     # P11: Intel, ejercicio cerrado 27-dic-2025


def pct(a, b, dec=1):
    return round(100.0 * a / b, dec)


def var(nuevo, viejo, dec=1):
    return round(100.0 * (nuevo - viejo) / abs(viejo), dec)


filas = []


def add(bloque, concepto, valor, unidad, fuente):
    filas.append({"bloque": bloque, "concepto": concepto, "valor": valor,
                  "unidad": unidad, "fuente": fuente})
    print(f"{bloque:<28} {concepto:<62} {valor:>12} {unidad}")


def comprobar_sumas(p, nombre):
    s_ing = p["ingresos"]["Data Center"] + p["ingresos"]["Client and Gaming"] + p["ingresos"]["Embedded"]
    s_cg = p["ingresos"]["Client"] + p["ingresos"]["Gaming"]
    s_op = sum(p["res_op"].values())
    assert s_ing == p["total_ingresos"], f"{nombre}: ingresos no suman ({s_ing})"
    assert s_cg == p["ingresos"]["Client and Gaming"], f"{nombre}: Client+Gaming no suma"
    assert s_op == p["total_res_op"], f"{nombre}: resultado operativo no suma ({s_op})"
    add(nombre, "control: suma segmentos = total (ingresos y res. op.)", "OK", "", "script")


def mezcla(p, nombre, fuente):
    comprobar_sumas(p, nombre)
    for seg in ("Data Center", "Client", "Gaming", "Client and Gaming", "Embedded"):
        add(nombre, f"peso en ingresos: {seg}", pct(p["ingresos"][seg], p["total_ingresos"]), "%", fuente)
    seg_op_total = sum(v for k, v in p["res_op"].items() if k != "All Other")
    add(nombre, "suma res. op. de segmentos (antes de All Other)", seg_op_total, "M$", fuente)
    for seg in ("Data Center", "Client and Gaming", "Embedded"):
        add(nombre, f"peso en res. op. de segmentos: {seg}", pct(p["res_op"][seg], seg_op_total), "%", fuente)
        add(nombre, f"margen operativo de segmento: {seg}", pct(p["res_op"][seg], p["ingresos"][seg]), "%", fuente)
    add(nombre, "margen operativo GAAP total", pct(p["total_res_op"], p["total_ingresos"]), "%", fuente)
    add(nombre, "All Other / ingresos", pct(-p["res_op"]["All Other"], p["total_ingresos"]), "%", fuente)


print("=" * 110)
mezcla(FY25, "FY2025", "P1")
mezcla(FY24, "FY2024", "P1")
mezcla(Q2_26, "Q2 2026", "P2")
mezcla(Q2_25, "Q2 2025", "P2")
mezcla(H1_26, "H1 2026", "P2")

# Q1 2026 derivado = H1 2026 - Q2 2026
Q1_26 = {
    "ingresos": {k: H1_26["ingresos"][k] - Q2_26["ingresos"][k] for k in H1_26["ingresos"]},
    "total_ingresos": H1_26["total_ingresos"] - Q2_26["total_ingresos"],
    "res_op": {k: H1_26["res_op"][k] - Q2_26["res_op"][k] for k in H1_26["res_op"]},
    "total_res_op": H1_26["total_res_op"] - Q2_26["total_res_op"],
}
for seg, v in Q1_26["ingresos"].items():
    add("Q1 2026 (derivado)", f"ingresos: {seg}", v, "M$", "P2 (H1 - Q2)")
add("Q1 2026 (derivado)", "ingresos totales", Q1_26["total_ingresos"], "M$", "P2 (H1 - Q2)")
for seg, v in Q1_26["res_op"].items():
    add("Q1 2026 (derivado)", f"res. op.: {seg}", v, "M$", "P2 (H1 - Q2)")

# Crecimientos
for seg in ("Data Center", "Client", "Gaming", "Client and Gaming", "Embedded"):
    add("Crecimiento", f"FY2025 vs FY2024: {seg}", var(FY25["ingresos"][seg], FY24["ingresos"][seg]), "%", "P1")
    add("Crecimiento", f"Q2 2026 vs Q2 2025: {seg}", var(Q2_26["ingresos"][seg], Q2_25["ingresos"][seg]), "%", "P2")
    add("Crecimiento", f"Q2 2026 vs Q1 2026: {seg}", var(Q2_26["ingresos"][seg], Q1_26["ingresos"][seg]), "%", "P2")
add("Crecimiento", "FY2025 vs FY2024: total", var(FY25["total_ingresos"], FY24["total_ingresos"]), "%", "P1")
add("Crecimiento", "Q2 2026 vs Q2 2025: total", var(Q2_26["total_ingresos"], Q2_25["total_ingresos"]), "%", "P2")

# Geografía FY2025
assert sum(FY25_GEO.values()) == FY25["total_ingresos"]
for reg, v in FY25_GEO.items():
    add("Geografía FY2025", f"peso en ingresos: {reg}", pct(v, FY25["total_ingresos"]), "%", "P1")

# GAAP vs no-GAAP
add("GAAP vs no-GAAP", "FY2025 amortización intangibles / res. op. GAAP", pct(FY25_AMORT, FY25["total_res_op"]), "%", "P1")
add("GAAP vs no-GAAP", "FY2025 SBC / ingresos", pct(FY25_SBC, FY25["total_ingresos"]), "%", "P1")
add("GAAP vs no-GAAP", "FY2025 res. op. no-GAAP - GAAP", FY25_RES_OP_NONGAAP - FY25["total_res_op"], "M$", "P1, P5")
add("GAAP vs no-GAAP", "FY2025 res. op. no-GAAP / GAAP", round(FY25_RES_OP_NONGAAP / FY25["total_res_op"], 2), "x", "P1, P5")
add("GAAP vs no-GAAP", "FY2025 beneficio neto no-GAAP - GAAP", FY25_BN_NONGAAP - FY25_BN_GAAP, "M$", "P1, P5")
add("GAAP vs no-GAAP", "Q2 2026 res. op. no-GAAP - GAAP", Q2_26_RES_OP_NONGAAP - Q2_26["total_res_op"], "M$", "P2, P6")
add("GAAP vs no-GAAP", "Q2 2026 SBC / ingresos", pct(Q2_26_SBC, Q2_26["total_ingresos"]), "%", "P2")
add("GAAP vs no-GAAP", "Q2 2026 amortización / ingresos", pct(Q2_26_AMORT, Q2_26["total_ingresos"]), "%", "P2")
add("Balance", "FY2025 (fondo de comercio + intangibles) / activo total", pct(FY25_GOODWILL + FY25_INTANG, FY25_ACTIVO), "%", "P1")
add("Balance", "Q2 2026 (fondo de comercio + intangibles) / activo total", pct(Q2_26_GOODWILL + Q2_26_INTANG, Q2_26_ACTIVO), "%", "P2")
add("Balance", "Compromisos incondicionales: Q2 2026 / FY2025", round(COMPROMISOS_Q2_26 / COMPROMISOS_FY25, 2), "x", "P1, P2")

# Caja y recompras vs SBC
add("Caja", "FY2025 FCF aprox. (CFO continuadas - capex continuadas)", FY25_CFO_CONT - FY25_CAPEX, "M$", "P1")
add("Caja", "H1 2026 FCF aprox. (CFO - capex)", H1_26_CFO - H1_26_CAPEX, "M$", "P2")
add("Dilución", "FY2025 recompras programa / SBC", round(FY25_RECOMPRAS / FY25_SBC, 2), "x", "P1")
add("Dilución", "H1 2026 recompras programa / SBC", round(H1_26_RECOMPRAS / H1_26_SBC, 2), "x", "P2")
add("Dilución", "Acciones en circulación: var. FY2025 vs FY2024", var(ACCIONES_FY25_FIN, ACCIONES_FY24_FIN, 2), "%", "P1")

# Warrants
w = WARRANT_OPENAI + WARRANT_META
add("Warrants", "acciones máximas de warrants OpenAI + Meta", w, "M acc.", "P2, P7, P8")
add("Warrants", "warrants / acciones en circulación (29-jul-2026)", pct(w, ACCIONES_EN_CIRCULACION_29JUL26), "%", "P2")
add("Warrants", "warrants / acciones tras ejercicio total (dilución)", pct(w, ACCIONES_EN_CIRCULACION_29JUL26 + w), "%", "P2")
add("Warrants", "un warrant (160 M) / acciones en circulación", pct(WARRANT_OPENAI, ACCIONES_EN_CIRCULACION_29JUL26), "%", "P2")

# Competidores (escala)
add("Competidores", "Ingresos Nvidia FY2026 / ingresos AMD FY2025", round(NVDA_FY26_INGRESOS / FY25["total_ingresos"], 2), "x", "P10, P1")
add("Competidores", "Ingresos Intel FY2025 / ingresos AMD FY2025", round(INTC_FY25_INGRESOS / FY25["total_ingresos"], 2), "x", "P11, P1")

# Objetivos y guía (P17 Analyst Day; P5 BPA no-GAAP FY2025; P6 guía Q3 2026)
BPA_NONGAAP_FY25 = 4.17
BPA_GAAP_FY25 = 2.65
BPA_OBJETIVO = 20.0            # "exceeding $20", horizonte 3-5 años
GUIA_Q3_26 = 13000             # "approximately $13 billion, plus or minus $300 million"
Q3_25_INGRESOS = 9246          # P5 (tabla trimestral, columna Q3 2025)
add("Objetivos", "BPA objetivo (>20 $) / BPA no-GAAP FY2025", round(BPA_OBJETIVO / BPA_NONGAAP_FY25, 2), "x", "P17, P5")
add("Objetivos", "BPA objetivo (>20 $) / BPA GAAP FY2025", round(BPA_OBJETIVO / BPA_GAAP_FY25, 2), "x", "P17, P1")
add("Objetivos", "Guía Q3 2026 (punto medio) vs Q3 2025", var(GUIA_Q3_26, Q3_25_INGRESOS), "%", "P6, P5")
add("Objetivos", "Ingresos FY2025 x 1,35^3 (objetivo >35% CAGR, 3 años)", round(FY25["total_ingresos"] * 1.35 ** 3), "M$", "P17, P1")
add("Objetivos", "Ingresos FY2025 x 1,35^5 (objetivo >35% CAGR, 5 años)", round(FY25["total_ingresos"] * 1.35 ** 5), "M$", "P17, P1")

add("Caja", "FY2025 capex / ingresos", pct(FY25_CAPEX, FY25["total_ingresos"]), "%", "P1")
add("Q2 2026", "ingresos fuera de Data Center (Client and Gaming + Embedded)",
    Q2_26["ingresos"]["Client and Gaming"] + Q2_26["ingresos"]["Embedded"], "M$", "P2")
add("Q2 2026", "ingresos anualizados (Q2 x 4, orientativo)", Q2_26["total_ingresos"] * 4, "M$", "P2")

os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
with open(SALIDA, "w", newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, fieldnames=["bloque", "concepto", "valor", "unidad", "fuente"])
    wr.writeheader()
    wr.writerows(filas)
print("=" * 110)
print(f"Guardado: {os.path.relpath(SALIDA, os.path.dirname(BASE))}")
