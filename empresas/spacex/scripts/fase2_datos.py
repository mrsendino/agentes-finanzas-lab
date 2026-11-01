#!/usr/bin/env python3
"""Fase 2 (Financieros) — SpaceX (SPCX): construye data/spacex_financials.csv.

Qué hace:
1. Recoge, como literales, las cifras leídas en las fuentes primarias de SEC EDGAR (sin aritmética):
     P2 = Folleto final 424(b)(4), acc. 0001628280-26-042639 (estados auditados FY2023-FY2025 y 1T 2026
          no auditado; cifras reexpresadas por la fusión con xAI/X bajo control común).
     P3 = 10-Q 3T 2026, acc. 0001628280-26-066880 (3T y 9M 2026 / 2025; balance a 30-sep-2026).
     P5 = 8-K 20-oct-2026, Ex. 99.1 (solo contraste).
     P6 = 10-Q 2T 2026, acc. 0001628280-26-052535 (2T y 6M 2026 / 2025).
   Páginas: número de folio impreso en el documento (en el 424B4, el folio de la página HTML de EDGAR;
   p. ej. "F-57"; en los 10-Q, el número al pie de página).
2. FY2021 y FY2022 se dejan VACÍOS y marcados "SIN VERIFICAR": el folleto solo incluye tres ejercicios
   auditados (FY2023-FY2025) y SpaceX no presentaba informes a la SEC antes de la OPV.
3. Calcula la columna TTM_Q3_2026 por script:
     flujos   -> FY2025 + 9M2026 - 9M2025
     saldos   -> saldo a 30-sep-2026 (columna 9M2026)
     % / otros -> no se calcula (vacío)
4. Escribe data/spacex_financials.csv (una columna de fuente por celda).

Convenciones: importes en millones de USD; acciones en millones salvo indicación; gastos en positivo
(p. ej. gastos_intereses = 1.945 significa un gasto de 1.945 M$); impuestos: positivo = gasto,
negativo = beneficio fiscal; otros_resultados_netos: positivo = ingreso. Capex = "Purchases of property,
plant, and equipment" del estado de flujos (coincide con la suma de capex por segmento de la nota de segmentos).

Uso:  python empresas/spacex/scripts/fase2_datos.py
"""
import csv
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "data", "spacex_financials.csv")

PERIODOS = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025",
            "Q1_2025", "Q2_2025", "6M2025", "Q3_2025", "9M2025",
            "Q1_2026", "Q2_2026", "6M2026", "Q3_2026", "9M2026", "TTM_Q3_2026"]

URL = {
    "P2": "https://www.sec.gov/Archives/edgar/data/1181412/000162828026042639/spaceexplorationtechnologi.htm",
    "P3": "https://www.sec.gov/Archives/edgar/data/1181412/000162828026066880/spcx-20260930.htm",
    "P5": "https://www.sec.gov/Archives/edgar/data/1181412/000162828026066482/spaceexplorationtechnologi.htm",
    "P6": "https://www.sec.gov/Archives/edgar/data/1181412/000162828026052535/spcx-20260630.htm",
}
DOC = {
    "P2": "P2 424B4 (acc. 0001628280-26-042639)",
    "P3": "P3 10-Q 3T26 (acc. 0001628280-26-066880)",
    "P5": "P5 8-K Ex.99.1 3T26 (acc. 0001628280-26-066482)",
    "P6": "P6 10-Q 2T26 (acc. 0001628280-26-052535)",
}


def S(doc, seccion, pagina):
    return f"{DOC[doc]}, {seccion}, p. {pagina}, {URL[doc]}"


SIN_FY21_22 = ("SIN VERIFICAR: no publicado. El folleto (P2) solo contiene FY2023-FY2025 auditados "
               "(índice de estados financieros, p. F-1) y SpaceX no presentaba informes a la SEC antes de la OPV")

# ---------------------------------------------------------------------------------------------
# Fuentes por tabla y periodo
SEG_P2_FY = {"FY2025": S("P2", "Note 19 Segments (tabla FY2025)", "F-57"),
             "FY2024": S("P2", "Note 19 Segments (tabla FY2024)", "F-58"),
             "FY2023": S("P2", "Note 19 Segments (tabla FY2023)", "F-58")}
SEG_Q = {"Q1_2026": S("P2", "Note de segmentos de los estados 1T26 no auditados (tabla 3M a 31-mar-2026)", "F-94"),
         "Q2_2026": S("P6", "Note 18 Segments (3M a 30-jun-2026)", "30"),
         "6M2026": S("P6", "Note 18 Segments (6M a 30-jun-2026)", "31"),
         "Q2_2025": S("P6", "Note 18 Segments (3M a 30-jun-2025)", "31"),
         "6M2025": S("P6", "Note 18 Segments (6M a 30-jun-2025)", "32"),
         "Q3_2026": S("P3", "Note 18 Segments (3M a 30-sep-2026)", "32"),
         "9M2026": S("P3", "Note 18 Segments (9M a 30-sep-2026)", "33"),
         "Q3_2025": S("P3", "Note 18 Segments (3M a 30-sep-2025)", "33"),
         "9M2025": S("P3", "Note 18 Segments (9M a 30-sep-2025)", "34")}
SEG = dict(SEG_P2_FY, **SEG_Q)
CAPEX_SRC = dict(SEG, **{"Q1_2025": S("P2", "Summary Historical Consolidated Financial and Operating Data, "
                                          "tabla 'Capital Expenditures' por segmento", "23")})
REV = {"FY2025": S("P2", "Note 3 Revenue, 'Revenue disaggregated by type and segment'", "F-22"),
       "FY2024": S("P2", "Note 3 Revenue, 'Revenue disaggregated by type and segment'", "F-22"),
       "FY2023": S("P2", "Note 3 Revenue, 'Revenue disaggregated by type and segment'", "F-22"),
       "Q1_2026": S("P2", "Note 3 Revenue de los estados 1T26, 'Revenue disaggregated by type and segment'", "F-71"),
       "Q1_2025": S("P2", "Note 3 Revenue de los estados 1T26, 'Revenue disaggregated by type and segment'", "F-71"),
       "Q2_2026": S("P6", "Note 3 Revenue, 'Revenue disaggregated by type and segment'", "13"),
       "6M2026": S("P6", "Note 3 Revenue, 'Revenue disaggregated by type and segment'", "13"),
       "Q2_2025": S("P6", "Note 3 Revenue, 'Revenue disaggregated by type and segment'", "13"),
       "6M2025": S("P6", "Note 3 Revenue, 'Revenue disaggregated by type and segment'", "13"),
       "Q3_2026": S("P3", "Note 3 Revenue, 'Revenue disaggregated by type and segment'", "13"),
       "9M2026": S("P3", "Note 3 Revenue, 'Revenue disaggregated by type and segment'", "13"),
       "Q3_2025": S("P3", "Note 3 Revenue, 'Revenue disaggregated by type and segment'", "13"),
       "9M2025": S("P3", "Note 3 Revenue, 'Revenue disaggregated by type and segment'", "13")}
IS = {"FY2025": S("P2", "Consolidated Statements of Operations", "F-5"),
      "FY2024": S("P2", "Consolidated Statements of Operations", "F-5"),
      "FY2023": S("P2", "Consolidated Statements of Operations", "F-5"),
      "Q1_2026": S("P2", "Note de segmentos 1T26 (costes, intereses, otros y BAI consolidados)", "F-94"),
      "Q2_2026": S("P6", "Consolidated Statements of Operations", "5"),
      "6M2026": S("P6", "Consolidated Statements of Operations", "5"),
      "Q2_2025": S("P6", "Consolidated Statements of Operations", "5"),
      "6M2025": S("P6", "Consolidated Statements of Operations", "5"),
      "Q3_2026": S("P3", "Consolidated Statements of Operations", "5"),
      "9M2026": S("P3", "Consolidated Statements of Operations", "5"),
      "Q3_2025": S("P3", "Consolidated Statements of Operations", "5"),
      "9M2025": S("P3", "Consolidated Statements of Operations", "5")}
NI_Q1 = S("P2", "MD&A Non-GAAP, conciliación Net income (loss) a Adjusted EBITDA", "119")
ADJ = {"FY2025": S("P2", "MD&A Non-GAAP, conciliación Net income (loss) a Adjusted EBITDA", "119"),
       "FY2024": S("P2", "MD&A Non-GAAP, conciliación Net income (loss) a Adjusted EBITDA", "119"),
       "FY2023": S("P2", "MD&A Non-GAAP, conciliación Net income (loss) a Adjusted EBITDA", "119"),
       "Q1_2026": S("P2", "MD&A Non-GAAP, conciliación Net income (loss) a Adjusted EBITDA", "119"),
       "Q1_2025": S("P2", "MD&A Non-GAAP, conciliación Net income (loss) a Adjusted EBITDA", "119"),
       "Q2_2026": S("P6", "MD&A Non-GAAP, conciliación Net loss a Adjusted EBITDA", "46"),
       "6M2026": S("P6", "MD&A Non-GAAP, conciliación Net loss a Adjusted EBITDA", "46"),
       "Q2_2025": S("P6", "MD&A Non-GAAP, conciliación Net loss a Adjusted EBITDA", "46"),
       "6M2025": S("P6", "MD&A Non-GAAP, conciliación Net loss a Adjusted EBITDA", "46"),
       "Q3_2026": S("P3", "MD&A Non-GAAP, conciliación Net income (loss) a Adjusted EBITDA", "50"),
       "9M2026": S("P3", "MD&A Non-GAAP, conciliación Net income (loss) a Adjusted EBITDA", "50"),
       "Q3_2025": S("P3", "MD&A Non-GAAP, conciliación Net income (loss) a Adjusted EBITDA", "50"),
       "9M2025": S("P3", "MD&A Non-GAAP, conciliación Net income (loss) a Adjusted EBITDA", "50")}
SADJ = {"FY2025": S("P2", "MD&A Non-GAAP, conciliación a Segment Adjusted EBITDA (FY2025)", "120"),
        "FY2024": S("P2", "MD&A Non-GAAP, conciliación a Segment Adjusted EBITDA (FY2024)", "121"),
        "FY2023": S("P2", "MD&A Non-GAAP, conciliación a Segment Adjusted EBITDA (FY2023)", "121"),
        "Q1_2026": S("P2", "MD&A Non-GAAP, conciliación a Segment Adjusted EBITDA (1T26)", "120"),
        "Q1_2025": S("P2", "MD&A Non-GAAP, conciliación a Segment Adjusted EBITDA (1T25)", "120"),
        "Q2_2026": S("P6", "MD&A Non-GAAP, conciliación a Segment Adjusted EBITDA (2T26)", "46"),
        "6M2026": S("P6", "MD&A Non-GAAP, conciliación a Segment Adjusted EBITDA (6M26)", "47"),
        "Q2_2025": S("P6", "MD&A Non-GAAP, conciliación a Segment Adjusted EBITDA (2T25)", "47"),
        "6M2025": S("P6", "MD&A Non-GAAP, conciliación a Segment Adjusted EBITDA (6M25)", "47"),
        "Q3_2026": S("P3", "MD&A Non-GAAP, conciliación a Segment Adjusted EBITDA (3T26)", "51"),
        "9M2026": S("P3", "MD&A Non-GAAP, conciliación a Segment Adjusted EBITDA (9M26)", "51"),
        "Q3_2025": S("P3", "MD&A Non-GAAP, conciliación a Segment Adjusted EBITDA (3T25)", "51"),
        "9M2025": S("P3", "MD&A Non-GAAP, conciliación a Segment Adjusted EBITDA (9M25)", "52")}
CF = {"FY2025": S("P2", "Consolidated Statements of Cash Flows", "F-8"),
      "FY2024": S("P2", "Consolidated Statements of Cash Flows", "F-8"),
      "FY2023": S("P2", "Consolidated Statements of Cash Flows", "F-8"),
      "Q1_2026": S("P2", "Consolidated Statements of Cash Flows 1T26 (no auditado)", "F-67"),
      "Q1_2025": S("P2", "Consolidated Statements of Cash Flows 1T26 (no auditado)", "F-67"),
      "6M2026": S("P6", "Consolidated Statements of Cash Flows", "9"),
      "6M2025": S("P6", "Consolidated Statements of Cash Flows", "9"),
      "9M2026": S("P3", "Consolidated Statements of Cash Flows", "9"),
      "9M2025": S("P3", "Consolidated Statements of Cash Flows", "9")}
CF_SUP = {"FY2025": S("P2", "Consolidated Statements of Cash Flows, supplemental disclosures", "F-9"),
          "FY2024": S("P2", "Consolidated Statements of Cash Flows, supplemental disclosures", "F-9"),
          "FY2023": S("P2", "Consolidated Statements of Cash Flows, supplemental disclosures", "F-9"),
          "Q1_2026": S("P2", "Consolidated Statements of Cash Flows 1T26, supplemental", "F-68"),
          "9M2026": S("P3", "Consolidated Statements of Cash Flows, supplemental disclosures", "9"),
          "9M2025": S("P3", "Consolidated Statements of Cash Flows, supplemental disclosures", "9")}
BS = {"FY2025": S("P2", "Consolidated Balance Sheets (31-dic-2025)", "F-4"),
      "FY2024": S("P2", "Consolidated Balance Sheets (31-dic-2024)", "F-4"),
      "9M2026": S("P3", "Consolidated Balance Sheets (30-sep-2026)", "4")}
DEBT = {"FY2025": S("P2", "Note 10 Debt (31-dic-2025)", "F-29"),
        "FY2024": S("P2", "Note 10 Debt (31-dic-2024)", "F-29"),
        "9M2026": S("P3", "Note 9 Debt (30-sep-2026)", "17")}
SH_N12 = {"FY2024": S("P3", "Note 12, movimiento de acciones por clase (saldo 31-dic-2024)", "25"),
          "FY2025": S("P3", "Note 12, movimiento de acciones por clase (saldo 31-dic-2025)", "25"),
          "9M2025": S("P3", "Note 12, movimiento de acciones por clase (saldo 30-sep-2025)", "25"),
          "9M2026": S("P3", "Note 12, movimiento de acciones por clase (saldo 30-sep-2026)", "25")}
EPS = {"FY2025": S("P2", "Consolidated Statements of Operations (weighted average shares)", "F-5"),
       "FY2024": S("P2", "Consolidated Statements of Operations (weighted average shares)", "F-5"),
       "FY2023": S("P2", "Consolidated Statements of Operations (weighted average shares)", "F-5"),
       "Q1_2026": S("P2", "Summary Historical Consolidated Financial and Operating Data", "22"),
       "Q1_2025": S("P2", "Summary Historical Consolidated Financial and Operating Data", "22"),
       "Q2_2026": S("P6", "Consolidated Statements of Operations (weighted average shares)", "5"),
       "6M2026": S("P6", "Consolidated Statements of Operations (weighted average shares)", "5"),
       "Q2_2025": S("P6", "Consolidated Statements of Operations (weighted average shares)", "5"),
       "6M2025": S("P6", "Consolidated Statements of Operations (weighted average shares)", "5"),
       "Q3_2026": S("P3", "Consolidated Statements of Operations / Note 13 EPS", "5 y 27"),
       "9M2026": S("P3", "Consolidated Statements of Operations / Note 13 EPS", "5 y 27"),
       "Q3_2025": S("P3", "Consolidated Statements of Operations / Note 13 EPS", "5 y 27"),
       "9M2025": S("P3", "Consolidated Statements of Operations / Note 13 EPS", "5 y 27")}
CONC = {"FY2025": S("P2", "Note 3, Concentration of risk", "F-23"),
        "FY2024": S("P2", "Note 3, Concentration of risk", "F-23"),
        "FY2023": S("P2", "Note 3, Concentration of risk", "F-23"),
        "Q2_2026": S("P6", "Note 3, Concentration of risk", "14"),
        "6M2026": S("P6", "Note 3, Concentration of risk", "14"),
        "Q2_2025": S("P6", "Note 3, Concentration of risk", "14"),
        "6M2025": S("P6", "Note 3, Concentration of risk", "14"),
        "Q3_2026": S("P3", "Note 3, Concentration of risk", "13"),
        "9M2026": S("P3", "Note 3, Concentration of risk", "13"),
        "Q3_2025": S("P3", "Note 3, Concentration of risk", "13"),
        "9M2025": S("P3", "Note 3, Concentration of risk", "13")}
EQ9M26 = S("P3", "Consolidated Statements of Redeemable Convertible Preferred Stock and Shareholders' Equity (9M26)", "7")

ROWS = []   # (metrica, unidad, tipo, {periodo: (valor, fuente)}, nota)


def fila(metrica, unidad, tipo, valores, fuentes, nota=""):
    """valores: dict periodo -> número; fuentes: dict periodo -> texto (o texto único)."""
    d = {}
    for p, v in valores.items():
        src = fuentes if isinstance(fuentes, str) else fuentes[p]
        d[p] = (v, src)
    ROWS.append((metrica, unidad, tipo, d, nota))


def serie(*vals, periodos=("FY2023", "FY2024", "FY2025", "9M2025", "9M2026", "Q1_2026", "Q2_2026",
                           "Q3_2025", "Q3_2026")):
    return {p: v for p, v in zip(periodos, vals) if v is not None}


P9 = ("FY2023", "FY2024", "FY2025", "9M2025", "9M2026", "Q1_2026", "Q2_2026", "Q3_2025", "Q3_2026")
P_REV = P9 + ("Q1_2025", "Q2_2025", "6M2025", "6M2026")

# ------------------------------------------------------------- Ingresos por línea y segmento
rev = {
    "ing_launch_services":      (1964, 2584, 2576, 2056, 2108, 330, 648, 1000, 1130, 566, 490, 1056, 978),
    "ing_launch_development":   (1593, 1212, 1510, 1221, 1240, 289, 314, 666, 637, 299, 256, 555, 603),
    "ing_space":                (3557, 3796, 4086, 3277, 3348, 619, 962, 1666, 1767, 865, 746, 1611, 1581),
    "ing_consumer":             (2817, 4830, 7208, 5198, 7754, 2148, 2485, 1986, 3121, 1492, 1721, 3213, 4633),
    "ing_enterprise_government": (1052, 2769, 4179, 2961, 5042, 1109, 1806, 1111, 2127, 983, 867, 1849, 2915),
    "ing_connectivity":         (3869, 7599, 11387, 8159, 12796, 3257, 4291, 3097, 5248, 2475, 2588, 5062, 7548),
    "ing_advertising":          (2323, 1728, 1844, 1323, 1248, 343, 367, 454, 538, 443, 426, 870, 710),
    "ing_si_solutions_infra":   (638, 892, 1357, 955, 9691, 475, 2194, 359, 7022, 284, 311, 595, 2669),
    "ing_si":                   (2961, 2620, 3201, 2278, 10939, 818, 2561, 813, 7560, 727, 737, 1465, 3379),
    "ingresos_totales":         (10387, 14015, 18674, 13714, 27083, 4694, 7814, 5576, 14575, 4067, 4071, 8138, 12508),
}
notas_rev = {
    "ing_si_solutions_infra": "'AI Solutions & Infrastructure' en P2/P6; 'SI Solutions & Infrastructure' en P3",
    "ing_si": "Segmento 'AI' en P2/P6, renombrado 'SI' (Super Intelligence) en P3; incluye Cursor desde 14-ago-2026",
    "ing_enterprise_government": "Incluye Starlink Mobile (nota (1) de la tabla)",
}
for k, v in rev.items():
    fila(k, "M USD", "flujo", dict(zip(P_REV, v)), REV, notas_rev.get(k, ""))
fila("ing_cursor", "M USD", "flujo", {"Q3_2026": 608, "9M2026": 608},
     S("P3", "MD&A Segment Results SI, 'Revenue'", "48"),
     "Ingresos de Cursor desde el cierre (14-ago-2026); misma cifra en P5 'Cursor Merger'. No es dato de control común")

# ------------------------------------------------------------- Resultados por segmento (nota de segmentos)
segrows = {
    "coste_ingresos_space":        (1669, 1541, 1352, 1104, 1045, 281, 329, 477, 435),
    "coste_ingresos_connectivity": (2786, 4768, 5921, 4271, 6079, 1651, 2060, 1657, 2368),
    "coste_ingresos_si":           (1655, 1687, 2178, 1574, 4237, 456, 1106, 571, 2675),
    "id_space":                    (1538, 1835, 3004, 2069, 3231, 930, 1076, 849, 1225),
    "id_connectivity":             (381, 453, 575, 406, 687, 205, 294, 141, 188),
    "id_si":                       (186, 1176, 5064, 3331, 7740, 2379, 2178, 1301, 3183),
    "opinc_space":                 (-1, 21, -657, -181, -1211, -662, -542, 259, -7),
    "opinc_connectivity":          (469, 2006, 4423, 3147, 5211, 1188, 1656, 1190, 2367),
    "opinc_si":                    (-3973, -1561, -6355, -4182, -3295, -2469, -1257, -1722, 431),
    "dya_space":                   (571, 637, 757, 572, 509, 166, 158, 264, 185),
    "dya_connectivity":            (884, 1508, 2376, 1706, 2574, 783, 805, 628, 986),
    "dya_si":                      (1180, 1679, 3568, 2506, 5851, 1493, 1885, 922, 2473),
    "sbc_space":                   (427, 472, 515, 383, 503, 145, 179, 151, 179),
    "sbc_connectivity":            (249, 296, 369, 270, 398, 116, 136, 105, 146),
    "sbc_si":                      (3, 16, 1063, 391, 1715, 378, 516, 94, 821),
}
for k, v in segrows.items():
    fila(k, "M USD", "flujo", dict(zip(P9, v)), SEG,
         "Gasto en positivo" if k.startswith(("coste", "id_")) else "")
# 6M y 1T/2T 2025 de los segmentos (solo resultado operativo, para controles)
for k, v in {"opinc_space": (-1204, -439, -369), "opinc_connectivity": (2844, 1956, 923),
             "opinc_si": (-3726, -2460, -1524)}.items():
    row = [r for r in ROWS if r[0] == k][0]
    for p, x in zip(("6M2026", "6M2025", "Q2_2025"), v):
        row[3][p] = (x, SEG[p])

fila("sbc_adquisiciones_si", "M USD", "flujo",
     {"FY2023": 0, "FY2024": 0, "FY2025": 0, "9M2025": 0, "9M2026": 1217, "Q1_2026": 0, "Q2_2026": 0,
      "Q3_2025": 0, "Q3_2026": 1217},
     dict(SEG, **{p: ADJ[p] + " (la partida no existe: 0)" for p in ("FY2023", "FY2024", "FY2025", "Q1_2026")},
          **{"Q2_2026": ADJ["Q2_2026"] + " (la partida no existe: 0)"}),
     "SBC ligada a adquisiciones (Cursor). Solo SI. Partida nueva en el 3T26; antes = 0")
fila("costes_adquisicion_si", "M USD", "flujo",
     {"FY2023": 0, "FY2024": 0, "FY2025": 0, "9M2025": 0, "9M2026": 8, "Q1_2026": 0, "Q2_2026": 0,
      "Q3_2025": 0, "Q3_2026": 8},
     {**{p: ADJ[p] + " (la partida no existe: 0)" for p in ("FY2023", "FY2024", "FY2025", "Q1_2026", "Q2_2026")},
      "9M2025": SADJ["9M2025"], "Q3_2025": SADJ["Q3_2025"], "9M2026": SADJ["9M2026"], "Q3_2026": SADJ["Q3_2026"]},
     "Acquisition-related costs (solo SI)")
fila("reestructuracion_si", "M USD", "flujo",
     dict(zip(P9, (237, 213, 487, 472, -6, -11, 2, 278, 3))), SEG, "Solo SI (X). Negativo = reversión")
fila("deterioro_space", "M USD", "flujo", dict(zip(P9, (0, 24, 38, 29, 0, 0, 0, 0, 0))), SEG)
fila("deterioro_connectivity", "M USD", "flujo", dict(zip(P9, (0, 39, 0, 0, 0, 0, 0, 0, 0))), SEG)
fila("deterioro_si", "M USD", "flujo", dict(zip(P9, (3775, 0, 0, 0, 0, 0, 0, 0, 0))), SEG,
     "FY2023: deterioro de la marca Twitter")

# ------------------------------------------------------------- EBITDA ajustado por segmento (no GAAP)
P_ADJ = P9 + ("Q1_2025", "Q2_2025", "6M2025", "6M2026")
sadj = {"ebitda_aj_space":        (997, 1154, 653, 803, -199, -351, -205, 674, 357, 224, -93, 131, -556),
        "ebitda_aj_connectivity": (1602, 3849, 7168, 5123, 8183, 2087, 2597, 1923, 3499, 1618, 1583, 3200, 4684),
        "ebitda_aj_si":           (1222, 347, -1237, -813, 5490, -609, 1146, -428, 4953, -112, -276, -387, 537)}
for k, v in sadj.items():
    fila(k, "M USD", "flujo", dict(zip(P_ADJ, v)), SADJ, "Segment Adjusted EBITDA (no GAAP)")
fila("ebitda_ajustado", "M USD", "flujo",
     dict(zip(P_ADJ, (3821, 5350, 6584, 5113, 13474, 1127, 3538, 2169, 8809, 1730, 1214, 2944, 4665))), ADJ,
     "Adjusted EBITDA publicado (no GAAP). Desde 3T26 excluye además SBC de adquisiciones y costes de adquisición")

# ------------------------------------------------------------- Capex por segmento
P_CX = P9 + ("Q1_2025", "Q2_2025", "6M2025", "6M2026")
capex = {"capex_space":        (1497, 2032, 3832, 2818, 3832, 1052, 1174, 1113, 1606, 759, 946, 1705, 2226),
         "capex_connectivity": (2455, 3498, 4178, 2951, 4242, 1332, 1367, 1007, 1543, 814, 1130, 1944, 2699),
         "capex_si":           (463, 5633, 12727, 8077, 39995, 7723, 15828, 4760, 16444, 2567, 749, 3316, 23551)}
for k, v in capex.items():
    fila(k, "M USD", "flujo", dict(zip(P_CX, v)), CAPEX_SRC,
         "Capital expenditures por segmento (salida de caja, positivo). Q3_2025/Q3_2026 coinciden con P5 p. 4")

# ------------------------------------------------------------- Cuenta de resultados consolidada
P_IS = ("FY2023", "FY2024", "FY2025", "9M2025", "9M2026", "Q1_2026", "Q2_2026", "Q3_2025", "Q3_2026",
        "Q2_2025", "6M2025", "6M2026")
isrows = {
    "coste_ingresos":          (6110, 7996, 9451, 6949, 11361, 2388, 3495, 2705, 5478, 2282, 4244, 5883),
    "id_total":                (2105, 3464, 8643, 5806, 11658, 3514, 3548, 2291, 4596, 1958, 3515, 7062),
    "sga":                     (1665, 1813, 2644, 1674, 3365, 746, 912, 575, 1707, 606, 1099, 1658),
    "reestructuracion":        (237, 213, 487, 472, -6, -11, 2, 278, 3, 190, 194, -9),
    "deterioros":              (3775, 63, 38, 29, 0, 0, 0, 0, 0, 5, 29, 0),
    "costes_totales":          (13892, 13549, 21263, 14930, 26378, 6637, 7957, 5849, 11784, 5041, 9081, 14594),
    "beneficio_operativo":     (-3505, 466, -2589, -1216, 705, -1943, -143, -273, 2791, -970, -943, -2086),
    "gastos_intereses":        (1693, 1580, 1945, 1372, 1968, 664, 629, 514, 675, 411, 858, 1293),
    "ingresos_intereses":      (249, 371, 492, 370, 1426, 213, 340, 155, 873, 98, 215, 553),
    "otros_resultados_netos":  (-42, 985, -177, 342, -937, -1876, -86, 140, 1025, 413, 202, -1962),
    "bai":                     (-4991, 242, -4219, -1876, -774, -4270, -518, -492, 4014, -870, -1384, -4788),
    "impuestos":               (-363, -549, 718, 714, -361, 6, 23, 562, -390, 138, 152, 29),
    "beneficio_neto":          (-4628, 791, -4937, -2590, -413, -4276, -541, -1054, 4404, -1008, -1536, -4817),
}
for k, v in isrows.items():
    src = dict(IS)
    if k == "impuestos":
        src["Q1_2026"] = NI_Q1
    if k == "beneficio_neto":
        src["Q1_2026"] = NI_Q1
    fila(k, "M USD", "flujo", dict(zip(P_IS, v)), src,
         {"impuestos": "Positivo = gasto; negativo = beneficio fiscal",
          "otros_resultados_netos": "Positivo = ingreso. 3T26 incluye +561 M$ de plusvalía no realizada en The Boring Company (parte vinculada)",
          "gastos_intereses": "Gasto en positivo",
          "beneficio_operativo": "Income (loss) from operations = suma de los tres segmentos (no hay partida corporativa)"}.get(k, ""))
fila("beneficio_neto_atrib_comunes", "M USD", "flujo",
     {"FY2023": -4628, "FY2024": 18, "FY2025": -4937, "9M2025": -2590, "9M2026": -1084, "Q2_2026": -541,
      "Q3_2025": -1054, "Q3_2026": 4404},
     IS, "Básico. 9M26 incluye un dividendo implícito de 671 M$ por recompra de preferentes (P3 Note 13)")
fila("gastos_intereses_vinculadas", "M USD", "flujo",
     {"FY2025": 66, "FY2024": 0, "FY2023": 0, "9M2025": 0, "9M2026": 864, "Q3_2025": 0, "Q3_2026": 351},
     IS, "Intereses con partes vinculadas (Valor Equity Partners, failed sale-leaseback), incluidos en gastos_intereses")
fila("perdida_extincion_deuda", "M USD", "flujo", {"9M2026": 1545, "9M2025": 0, "Q1_2026": 1526},
     {"9M2026": CF["9M2026"], "9M2025": CF["9M2025"], "Q1_2026": CF["Q1_2026"]},
     "Loss on debt extinguishment (dentro de otros_resultados_netos); 1T26 = 1.526")
fila("plusvalia_no_realizada_participadas", "M USD", "flujo", {"9M2026": 532, "9M2025": 0},
     CF, "Unrealized gain on investments in unconsolidated affiliates, net (positivo = ganancia). Boring Company")

# ------------------------------------------------------------- Partidas de la conciliación (consolidado)
fila("dya_total", "M USD", "flujo",
     dict(zip(P_ADJ, (2635, 3824, 6701, 4784, 8934, 2442, 2848, 1814, 3644, 1443, 1526, 2970, 5290))),
     dict(ADJ, **{"Q2_2025": SEG["Q2_2025"], "6M2025": CF["6M2025"], "6M2026": CF["6M2026"]}),
     "Depreciation and amortization")
fila("sbc_ordinaria_total", "M USD", "flujo",
     dict(zip(P_ADJ, (679, 784, 1947, 1044, 2616, 639, 831, 350, 1146, 232, 463, 694, 1470))),
     dict(ADJ, **{"Q2_2025": SEG["Q2_2025"], "6M2025": CF["6M2025"], "6M2026": CF["6M2026"]}),
     "SBC excluida la ligada a adquisiciones (desde 3T26 se presenta aparte)")
fila("sbc_flujo_caja", "M USD", "flujo",
     {"FY2023": 679, "FY2024": 784, "FY2025": 1947, "9M2025": 1044, "9M2026": 3833, "Q1_2026": 639,
      "6M2026": 1470, "6M2025": 694}, CF,
     "Share-based compensation en el estado de flujos (total, incluye la de adquisiciones)")
fila("sbc_capitalizada", "M USD", "flujo",
     {"FY2023": 108, "FY2024": 132, "FY2025": 154, "9M2025": 114, "9M2026": 160}, CF_SUP,
     "SBC capitalizada en PP&E (no pasa por resultados)")

# ------------------------------------------------------------- Flujos de caja
fila("flujo_caja_operativo", "M USD", "flujo",
     {"FY2023": 4520, "FY2024": 5776, "FY2025": 6785, "9M2025": 4120, "9M2026": 13097, "Q1_2026": 1047,
      "Q1_2025": 727, "6M2026": 3466, "6M2025": 351}, CF, "Net cash provided by operating activities")
fila("capex", "M USD", "flujo",
     {"FY2023": 4415, "FY2024": 11163, "FY2025": 20737, "9M2025": 13846, "9M2026": 48069, "Q1_2026": 10107,
      "Q1_2025": 4140, "6M2026": 28476, "6M2025": 6965}, CF,
     "Purchases of property, plant, and equipment (salida, positivo)")
fila("intereses_capitalizados", "M USD", "flujo",
     {"FY2023": 0, "FY2024": 0, "FY2025": 169, "9M2025": 96, "9M2026": 20, "6M2026": 20, "6M2025": 22}, CF,
     "Capitalized interest (salida de inversión, positivo)")
fila("reembolsos_producto", "M USD", "flujo",
     {"FY2023": 0, "FY2024": 0, "FY2025": 118, "9M2025": 0, "9M2026": 1372, "6M2026": 1195, "6M2025": 0}, CF,
     "Proceeds from product rebates (entrada de inversión, positivo)")
fila("ppe_financiado_otras_financiaciones", "M USD", "flujo",
     {"9M2026": 3921, "9M2025": 0, "Q1_2026": 2684}, CF_SUP,
     "Partida no monetaria: PP&E adquirido con 'other financings'. P2 no la muestra para FY2023-FY2025")
fila("ppe_en_cuentas_a_pagar", "M USD", "saldo",
     {"FY2023": 505, "FY2024": 2481, "FY2025": 7088, "9M2026": 11827}, CF_SUP,
     "Partida no monetaria: compras de PP&E pendientes de pago (saldo al cierre según la nota suplementaria)")
fila("intereses_pagados", "M USD", "flujo",
     {"FY2023": 1365, "FY2024": 1500, "FY2025": 1476, "9M2025": 695, "9M2026": 2078}, CF_SUP,
     "Interest, net of interest capitalized (caja)")
fila("recompras_acciones", "M USD", "flujo",
     {"FY2023": 170, "FY2024": 1021, "FY2025": 1125, "9M2025": 525, "9M2026": 4426}, CF,
     "Payments for repurchase of common and redeemable convertible preferred stock")
fila("impuestos_liquidacion_neta_sbc", "M USD", "flujo",
     {"FY2023": 211, "FY2024": 243, "FY2025": 496, "9M2025": 194, "9M2026": 559}, CF,
     "Taxes paid related to net share settlement of equity awards")
fila("opv_neta", "M USD", "flujo", {"9M2026": 85675, "9M2025": 0, "FY2025": 0}, CF,
     "Proceeds from IPO, net of underwriting commissions and offering costs")

# ------------------------------------------------------------- Balance
fila("caja", "M USD", "saldo", {"FY2023": 4620, "FY2024": 11385, "FY2025": 24747, "9M2026": 51294},
     dict(BS, FY2023=S("P2", "Note 2, tabla 'Cash and cash equivalents and restricted cash'", "F-12")),
     "Cash and cash equivalents (sin caja restringida). FY2023: única partida de balance disponible para 31-dic-2023")
fila("valores_negociables", "M USD", "saldo", {"FY2024": 800, "FY2025": 0, "9M2026": 38561}, BS,
     "Marketable securities (corto plazo). 31-dic-2023: SIN VERIFICAR (P2 no incluye balance de 2023)")
fila("deuda_y_arrendamientos_corriente", "M USD", "saldo", {"FY2024": 372, "FY2025": 928, "9M2026": 2698}, BS,
     "Debt and finance leases, current (valor contable)")
fila("deuda_y_arrendamientos_no_corriente", "M USD", "saldo", {"FY2024": 13421, "FY2025": 21968, "9M2026": 36146}, BS,
     "Debt and finance leases, net of current (valor contable)")
fila("deuda_principal", "M USD", "saldo", {"FY2024": 12621, "FY2025": 22049, "9M2026": 38006}, DEBT,
     "Total debt, principal (sin arrendamientos financieros). 30-sep-2026: 25.000 SpaceX Notes + 27 X Notes + 12.979 other financings")
fila("arrendamiento_financiero", "M USD", "saldo", {"FY2024": 1531, "FY2025": 1237, "9M2026": 983}, DEBT,
     "Finance lease liability")
fila("costes_financiacion_pendientes", "M USD", "saldo", {"FY2024": 359, "FY2025": 390, "9M2026": 145}, DEBT,
     "Unamortized deferred financing costs")
fila("deuda_vinculada_corriente", "M USD", "saldo", {"FY2024": 0, "FY2025": 455, "9M2026": 2181}, BS,
     "Parte vinculada (Valor Equity Partners) incluida en deuda_y_arrendamientos_corriente")
fila("deuda_vinculada_no_corriente", "M USD", "saldo", {"FY2024": 0, "FY2025": 4052, "9M2026": 10716}, BS,
     "Parte vinculada (Valor Equity Partners) incluida en deuda_y_arrendamientos_no_corriente")
fila("patrimonio_neto", "M USD", "saldo", {"FY2024": 4863, "FY2025": 2573, "9M2026": 176768}, BS,
     "Total shareholders' equity")
fila("preferentes_convertibles_importe", "M USD", "saldo", {"FY2024": 20941, "FY2025": 38752, "9M2026": 0}, BS,
     "Redeemable convertible preferred stock (fuera del patrimonio neto); convertidas en la OPV")
fila("activo_total", "M USD", "saldo", {"FY2024": 57062, "FY2025": 92079, "9M2026": 254045}, BS)
fila("inmovilizado_material_neto", "M USD", "saldo", {"FY2024": 21147, "FY2025": 42602, "9M2026": 89483}, BS)
fila("fondo_comercio", "M USD", "saldo", {"FY2024": 11129, "FY2025": 11809, "9M2026": 48423}, BS)
fila("ingresos_diferidos_corriente", "M USD", "saldo", {"FY2024": 5498, "FY2025": 6111, "9M2026": 10784}, BS)
fila("ingresos_diferidos_no_corriente", "M USD", "saldo", {"FY2024": 4681, "FY2025": 6005, "9M2026": 6736}, BS)
fila("ingresos_diferidos_total_publicado", "M USD", "saldo", {"FY2025": 12116, "9M2026": 17520},
     {"FY2025": S("P2", "Note 3, Deferred revenue", "F-22"),
      "9M2026": CONC["9M2026"].replace("Concentration of risk", "Deferred revenue")},
     "Total publicado en la Note 3 (solo para contraste)")

# ------------------------------------------------------------- Acciones (millones)
fila("acciones_clase_A", "M acciones", "saldo", {"FY2024": 1832, "FY2025": 1952, "9M2025": 1887, "9M2026": 8240}, SH_N12,
     "Saldo al cierre. P2 balance (p. F-4) da 1.954 en circulación a 31-dic-2025 (diferencia de 2 M, ver doc §7)")
fila("acciones_clase_B", "M acciones", "saldo", {"FY2024": 768, "FY2025": 643, "9M2025": 694, "9M2026": 5339}, SH_N12,
     "10 votos por acción. P2 y P3 balance dan 644 a 31-dic-2025")
fila("acciones_clase_C", "M acciones", "saldo", {"FY2024": 423, "FY2025": 484, "9M2025": 460, "9M2026": 0}, SH_N12,
     "Sin voto; reclasificada a Clase A en la OPV. P2 balance da 421 (dic-24) y 482 (dic-25)")
fila("acciones_ordinarias_total", "M acciones", "saldo", {"FY2024": 3023, "FY2025": 3079, "9M2025": 3041, "9M2026": 13579},
     {"FY2024": S("P2", "Statement of Shareholders' Equity, columna Common Stock Shares", "F-7"),
      "FY2025": S("P2", "Statement of Shareholders' Equity, columna Common Stock Shares", "F-7"),
      "9M2025": S("P3", "Statement of Shareholders' Equity (9M25)", "8"),
      "9M2026": EQ9M26}, "Total publicado (no suma propia)")
fila("preferentes_convertibles_acciones", "M acciones", "saldo",
     {"FY2024": 1748, "FY2025": 2046, "9M2025": 1893, "9M2026": 0},
     {"FY2024": BS["FY2024"], "FY2025": BS["FY2025"], "9M2025": S("P3", "Statement of Shareholders' Equity (9M25)", "8"),
      "9M2026": BS["9M2026"]}, "Acciones preferentes (no ordinarias); ratios de conversión distintos por serie")
fila("preferentes_xai_como_convertidas", "M acciones", "saldo", {"9M2025": 1241},
     S("P3", "Note 13 EPS, valores potencialmente dilutivos excluidos (as-converted, 30-sep-2025)", "27"))
fila("preferentes_spacex_como_convertidas", "M acciones", "saldo", {"9M2025": 6760},
     S("P3", "Note 13 EPS, valores potencialmente dilutivos excluidos (as-converted, 30-sep-2025)", "27"))
fila("sbc_potencialmente_dilutiva_excluida", "M acciones", "saldo", {"9M2025": 648, "9M2026": 19},
     S("P3", "Note 13 EPS, valores potencialmente dilutivos excluidos (as-converted)", "27"))
fila("premios_rendimiento_no_cumplidos", "M acciones", "saldo", {"9M2025": 14, "9M2026": 1333},
     S("P3", "Note 13 EPS (premios con condiciones de rendimiento/mercado no cumplidas)", "27"))
fila("opciones_vivas_clase_A", "M acciones", "saldo", {"9M2026": 158},
     S("P3", "Note 12, 'Reserve for Unissued Shares'", "26"))
fila("opciones_vivas_clase_B", "M acciones", "saldo", {"9M2026": 350},
     S("P3", "Note 12, 'Reserve for Unissued Shares'", "26"))
fila("rsu_vivas_clase_A", "M acciones", "saldo", {"9M2026": 142},
     S("P3", "Note 12, 'Reserve for Unissued Shares'", "26"))
fila("acciones_A_portada_15oct2026", "acciones", "otro", {"9M2026": 8246541218}, S("P3", "Portada", "1"),
     "A 15-oct-2026 (número exacto)")
fila("acciones_B_portada_15oct2026", "acciones", "otro", {"9M2026": 5334522491}, S("P3", "Portada", "1"),
     "A 15-oct-2026 (número exacto)")
# Movimiento de acciones ordinarias en 9M26 (P3, estado de patrimonio)
for k, v, n in (("acc_emitidas_opv_9M26", 639, "Issuance of common stock in connection with IPO"),
                ("acc_emitidas_netas_9M26", 1381, "Common stock issued, net of tax withholding (Clase B 1.306 según Note 12)"),
                ("acc_conversion_pref_xai_9M26", 1424, "Conversion of redeemable convertible preferred stock pursuant to xAI Merger"),
                ("acc_recompra_xai_9M26", -25, "Repurchase of common stock pursuant to xAI Merger"),
                ("acc_conversion_pref_9M26", 6728, "Conversion of redeemable convertible preferred stock to common stock"),
                ("acc_recompra_9M26", -41, "Repurchase of common and redeemable convertible preferred stock"),
                ("acc_combinaciones_negocio_9M26", 394, "Transfer of equity in business combinations (Cursor y Mesh)")):
    fila(k, "M acciones", "otro", {"9M2026": v}, EQ9M26, n)
fila("acciones_ponderadas_basicas", "M acciones", "otro",
     {"FY2023": 2759, "FY2024": 2848, "FY2025": 2926, "9M2025": 2915, "9M2026": 7274, "Q1_2026": 3884,
      "Q2_2026": 5864, "Q3_2025": 2941, "Q3_2026": 11942}, EPS, "Media ponderada básica")
fila("acciones_ponderadas_diluidas", "M acciones", "otro",
     {"FY2023": 2759, "FY2024": 9956, "FY2025": 2926, "9M2025": 2915, "9M2026": 7274, "Q1_2026": 3884,
      "Q2_2026": 5864, "Q3_2025": 2941, "Q3_2026": 12475}, EPS, "Media ponderada diluida")
fila("acciones_ponderadas_pro_forma_FY2025", "M acciones", "otro", {"FY2025": 9649},
     S("P2", "Summary, cálculo pro forma de BPA (conversión de preferentes al 1-ene-2025)", "23"))

# ------------------------------------------------------------- Concentración de clientes (% ingresos)
fila("cliente_A_pct", "%", "pct",
     {"FY2023": 25.2, "FY2024": 24.2, "FY2025": 20.9, "9M2025": 21.6, "9M2026": 17.3, "Q2_2026": 18.3,
      "6M2026": 17.9, "Q2_2025": 16.7, "6M2025": 19.9, "Q3_2025": 23.9, "Q3_2026": 16.6}, CONC,
     "Customer A: ingresos en los tres segmentos. Identidad no revelada (inferencia de la fase 1: gobierno federal de EE. UU., SIN VERIFICAR)")
fila("cliente_B_pct", "%", "pct",
     {"9M2026": 24.2, "Q2_2026": 19.5, "6M2026": 12.2, "Q3_2026": 34.5}, CONC,
     "Customer B: solo segmento SI. '<10 %' (no revelado) en FY2023-FY2025, 2025 y 1T26. Identidad no revelada "
     "(inferencia de la fase 1: Anthropic, SIN VERIFICAR)")
fila("cuentas_cobrar_cliente_principal_pct", "%", "pct", {"9M2026": 27.7}, CONC["9M2026"],
     "Un cliente = 27,7 % de cuentas a cobrar a 30-sep-2026 (no identificado)")
fila("backlog", "M USD", "saldo", {"FY2025": 28377, "9M2026": 62959, "6M2026": 47461},
     {"FY2025": CONC["FY2025"], "9M2026": CONC["9M2026"], "6M2026": S("P6", "Note 3, Backlog", "14")},
     "Cartera de pedidos")

# ---------------------------------------------------------------------------------------------
FLOW_TTM_FUENTE = "Calculado en scripts/fase2_datos.py: FY2025 + 9M2026 - 9M2025 (fuentes en esas columnas)"
SALDO_TTM_FUENTE = "Saldo a 30-sep-2026 (columna 9M2026)"


def main():
    rows_out = []
    for metrica, unidad, tipo, d, nota in ROWS:
        if tipo == "flujo" and all(p in d for p in ("FY2025", "9M2026", "9M2025")):
            d["TTM_Q3_2026"] = (d["FY2025"][0] + d["9M2026"][0] - d["9M2025"][0], FLOW_TTM_FUENTE)
        elif tipo == "saldo" and "9M2026" in d:
            d["TTM_Q3_2026"] = (d["9M2026"][0], SALDO_TTM_FUENTE)
        r = {"metrica": metrica, "unidad": unidad, "tipo": tipo}
        for p in PERIODOS:
            if p in ("FY2021", "FY2022"):
                r[p], r["fuente_" + p] = "", SIN_FY21_22
            elif p in d:
                r[p], r["fuente_" + p] = d[p][0], d[p][1]
            else:
                r[p], r["fuente_" + p] = "", ""
        r["nota"] = nota
        rows_out.append(r)
    cols = ["metrica", "unidad", "tipo"] + [x for p in PERIODOS for x in (p, "fuente_" + p)] + ["nota"]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows_out)
    print(f"Escrito {OUT}: {len(rows_out)} métricas x {len(PERIODOS)} periodos")


if __name__ == "__main__":
    main()
