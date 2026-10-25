#!/usr/bin/env python3
"""Fase 2 - Tesla (TSLA): ratios y crecimientos a partir de data/tesla_financials.csv.

Toda la aritmética del análisis se hace aquí (nada a mano).

Pasos:
1. Lee los valores brutos con su fuente.
2. Construye FY2025 a partir de fuentes primarias (9M2025 del 10-Q Q3 2025 + Q4-25 del deck P4)
   y lo contrasta con el valor de S1 (secundaria) y la reconciliación TTM de P4.
3. Construye TTM a Q3-2026 = FY2025 + 9M2026 - 9M2025 (flujos) / saldo a 30-sep-2026 (balances)
   y lo contrasta con los TTM que publica Tesla en P4.
4. Calcula márgenes, crecimientos, FCF, caja neta, créditos/beneficio operativo, ROIC aproximado.
5. Escribe data/ratios.csv y data/checks.csv.

v2 (2026-10-25, ronda de correcciones de 05-veredicto.md §5 Fase 2):
  - Añade D&A (depreciation, amortization and impairment) como flujo: FY2025 y TTM construidos
    y contrastados con la reconciliación EBITDA TTM de P4.
  - Añade la descomposición de acciones (portada / básica / diluida / emitidas 9M26) con controles.
  - Añade contraste de FY2021 con el deck Q4-2021 (cifras redondeadas a 0,1 B$).

Método ROIC (aproximación, declarada):
  NOPAT = beneficio operativo x (1 - 21 %)   [tipo federal EE. UU. normativo; se evita el tipo
          efectivo porque FY2023 incluye una liberación de provisión fiscal no recurrente]
  Capital invertido (A) = patrimonio neto accionistas + deuda total - caja e inversiones CP
  Capital invertido (B) = patrimonio neto accionistas + deuda total (sin restar caja)
  Se usa la media de saldo inicial y final cuando hay saldo inicial; FY2021 usa saldo final.
  La deuda incluye arrendamientos financieros y deuda sin recurso ligada a vehículos/solar
  (no separable con las fuentes leídas).
"""
import csv
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "data", "tesla_financials.csv")
OUT = os.path.join(BASE, "data", "ratios.csv")
CHK = os.path.join(BASE, "data", "checks.csv")

TAX_NORM = 0.21
YEARS = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025", "TTM_Q3_2026"]
FLOW = ["ingresos_totales", "auto_ventas", "creditos_regulatorios", "auto_leasing",
        "ingresos_automocion_total", "ingresos_energia", "ingresos_servicios_otros",
        "beneficio_bruto", "beneficio_operativo", "beneficio_neto_atrib_comunes",
        "flujo_caja_operativo", "capex", "sbc", "dya_amortizacion_deterioro"]
STOCK = ["caja_y_inversiones_cp", "deuda_corriente", "deuda_no_corriente",
         "patrimonio_neto_accionistas"]


def load():
    data = {}
    with open(SRC, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            data[r["metrica"]] = {k: (float(v) if v not in ("", None) else None)
                                  for k, v in r.items()
                                  if not k.startswith("fuente_") and k not in ("metrica", "unidad", "nota")}
    return data


def div(a, b):
    return None if a is None or b in (None, 0) else a / b


def sub(a, b):
    return None if a is None or b is None else a - b


def add(*xs):
    return None if any(x is None for x in xs) else sum(xs)


def main():
    raw = load()
    checks = []

    def chk(name, calc, ref, ref_src, tol=1.0):
        diff = sub(calc, ref)
        ok = diff is not None and abs(diff) <= tol
        checks.append({"control": name, "calculado": calc, "referencia": ref,
                       "fuente_referencia": ref_src, "diferencia": diff,
                       "resultado": "OK" if ok else ("SIN DATO" if diff is None else "DISCREPANCIA")})

    # ---- 1. Serie anual: FY2021-FY2024 directos; FY2025 = 9M2025 + Q4_2025 (primario)
    s = {m: {} for m in FLOW + STOCK + ["acciones_diluidas_media"]}
    for m in s:
        for y in ["FY2021", "FY2022", "FY2023", "FY2024"]:
            s[m][y] = raw[m][y]
    for m in FLOW:
        prim = add(raw[m]["9M2025"], raw[m]["Q4_2025"])
        s[m]["FY2025"] = prim
        if raw[m]["FY2025"] is not None:
            chk(f"{m} FY2025: 9M25(10-Q)+Q4-25(P4) vs valor fuente FY2025", prim, raw[m]["FY2025"],
                "S1 o reconciliación TTM de P4 (ver CSV)")
    for m in STOCK:
        s[m]["FY2025"] = raw[m]["FY2025"]
    s["acciones_diluidas_media"]["FY2025"] = None  # SIN VERIFICAR (media anual no sumable)

    # ---- 2. TTM a Q3-2026
    for m in FLOW:
        ttm = add(s[m]["FY2025"], raw[m]["9M2026"])
        ttm = sub(ttm, raw[m]["9M2025"]) if ttm is not None else None
        s[m]["TTM_Q3_2026"] = ttm
        if raw[m]["TTM_Q3_2026"] is not None:
            chk(f"{m} TTM Q3-26: FY25+9M26-9M25 vs TTM publicado P4", ttm, raw[m]["TTM_Q3_2026"], "P4 reconciliación TTM")
    for m in STOCK:
        s[m]["TTM_Q3_2026"] = raw[m]["9M2026"]
    s["acciones_diluidas_media"]["TTM_Q3_2026"] = None

    # ---- 3. Controles de coherencia interna
    for y in YEARS:
        seg = add(s["ingresos_automocion_total"][y], s["ingresos_energia"][y], s["ingresos_servicios_otros"][y])
        chk(f"{y}: suma segmentos = ingresos totales", seg, s["ingresos_totales"][y], "mismo CSV")
        if y not in ("FY2025", "TTM_Q3_2026"):
            auto = add(s["auto_ventas"][y], s["creditos_regulatorios"][y], s["auto_leasing"][y])
            chk(f"{y}: ventas+créditos+leasing = automoción total", auto, s["ingresos_automocion_total"][y], "mismo CSV")
    for y in ["FY2023", "FY2024", "FY2025", "TTM_Q3_2026"]:
        fcf = sub(s["flujo_caja_operativo"][y], s["capex"][y])
        if raw["fcf_reportado"][y] is not None:
            chk(f"{y}: FCF calculado vs FCF reportado por Tesla", fcf, raw["fcf_reportado"][y], "deck Tesla (ver CSV)")
    # caja FY2025 y 30-sep-2026 vs P4
    chk("Caja+inv. 31-dic-2025 (10-Q) vs P4", raw["caja_y_inversiones_cp"]["FY2025"], 44059, "P4 balance Q4-25")
    chk("Caja+inv. 30-sep-2026 (10-Q) vs 01-negocio.md (45.400 redondeado)", raw["caja_y_inversiones_cp"]["9M2026"], 45400, "01-negocio.md", tol=50)
    chk("Deuda total 31-dic-2025 (10-Q) vs S1 (8.376)", add(raw["deuda_corriente"]["FY2025"], raw["deuda_no_corriente"]["FY2025"]), 8376, "S1 Tabla 2.2")
    chk("Deuda total 31-dic-2024 (deck) vs S1 (8.213)", add(raw["deuda_corriente"]["FY2024"], raw["deuda_no_corriente"]["FY2024"]), 8213, "S1 Tabla 2.2")
    chk("Capex FY2024 deck (11.339) vs S1 (11.342)", raw["capex"]["FY2024"], 11342, "S1 Tabla 2.2")
    chk("Créditos FY2025 / FY2024 - 1 vs 01-negocio.md (-28 %)", div(s["creditos_regulatorios"]["FY2025"], s["creditos_regulatorios"]["FY2024"]) - 1, -0.28, "01-negocio.md", tol=0.01)
    chk("Créditos FY2025 / Benef. operativo FY2025 vs 01-negocio.md (46 %)", div(s["creditos_regulatorios"]["FY2025"], s["beneficio_operativo"]["FY2025"]), 0.46, "01-negocio.md", tol=0.005)

    # Controles con datos trimestrales leídos de los decks (entradas auxiliares, fuente indicada)
    D24 = "8-K Ex.99.1 Q4 2024, acc. 0001628280-25-002993"
    P4 = "8-K Ex.99.1 Q3 2026, acc. 0001628280-26-066738"
    q24 = {"ingresos_totales": [21301, 25500, 25182, 25707], "flujo_caja_operativo": [242, 3612, 6255, 4814],
           "capex": [2773, 2270, 3513, 2783], "sbc": [524, 439, 457, 579]}
    for m, q in q24.items():
        chk(f"FY2024 {m}: suma Q1-Q4 2024 ({D24}) vs FY", float(sum(q)), s[m]["FY2024"], D24)
    q326 = {"ingresos": 28046, "bb": 5494, "opex": 4776, "oi": 718, "fco": 6263, "capex": 4732, "fcf": 1531,
            "ni": 787, "cred": 113, "rd": 2761, "sbc": 1165}
    chk("Q3-26: BB - opex = benef. operativo (P4)", float(q326["bb"] - q326["opex"]), q326["oi"], P4)
    chk("Q3-26: FCO - capex = FCF (P4)", float(q326["fco"] - q326["capex"]), q326["fcf"], P4)
    chk("Q3-26 margen bruto vs 01-negocio.md (19,6 %)", q326["bb"] / q326["ingresos"], 0.196, "01-negocio.md", tol=0.0005)
    chk("Q3-26 margen operativo vs 01-negocio.md (2,6 %)", q326["oi"] / q326["ingresos"], 0.026, "01-negocio.md", tol=0.0005)
    chk("Q3-26 SBC P4 (1.165) vs 01-negocio.md/S2 (1.170)", float(q326["sbc"]), 1170, "01-negocio.md (S2 Electrek)")
    chk("Q3-26 I+D P4 (2.761) vs 01-negocio.md/S2 (2.760)", float(q326["rd"]), 2760, "01-negocio.md (S2 Electrek)")
    chk("Capex 9M2026 10-Q (13.014) vs 01-negocio.md/S2 (13.010)", raw["capex"]["9M2026"], 13010, "01-negocio.md (S2 Electrek)")
    chk("Deuda contable 31-dic-2025 (8.376) vs 'deuda principal' 01-negocio.md (8.180, P1 Item 1A)",
        add(raw["deuda_corriente"]["FY2025"], raw["deuda_no_corriente"]["FY2025"]), 8180, "01-negocio.md (P1 Item 1A)")
    chk("Crec. ingresos Q3-26 vs Q3-25 (P4: 28.046 vs 28.095)", 28046 / 28095 - 1, 0.0, "01-negocio.md (≈0 %)", tol=0.005)
    chk("Crec. benef. operativo Q3-26 vs Q3-25 (718 vs 1.624, P4)", 718 / 1624 - 1, -0.56, "01-negocio.md (−56 %)", tol=0.005)
    chk("Crec. créditos Q3-26 vs Q3-25 (113 vs 417, P4)", 113 / 417 - 1, -0.73, "01-negocio.md (−73 %)", tol=0.005)
    chk("Crec. energía Q3-26 vs Q3-25 (2.881 vs 3.415, P4)", 2881 / 3415 - 1, -0.16, "01-negocio.md (−16 %)", tol=0.005)
    chk("Crec. servicios Q3-26 vs Q3-25 (4.605 vs 3.475, P4)", 4605 / 3475 - 1, 0.33, "01-negocio.md (+33 %)", tol=0.006)
    chk("Crec. benef. neto FY2025 vs FY2024", div(s["beneficio_neto_atrib_comunes"]["FY2025"], s["beneficio_neto_atrib_comunes"]["FY2024"]) - 1, -0.46, "01-negocio.md (−46 %)", tol=0.006)
    # PER implícito (contraste con S11 en 01-negocio.md: ~327x). Precio 354,72 $ (S12, 16-oct-2026).
    eps_ttm_q2 = 0.39 + 0.24 + 0.13 + 0.32   # BPA diluido GAAP Q3-25..Q2-26 (P4)
    eps_ttm_q3 = 0.24 + 0.13 + 0.32 + 0.22   # BPA diluido GAAP Q4-25..Q3-26 (P4)
    chk("PER GAAP a 354,72 $ con BPA TTM a Q2-26 (P4) vs ~327x (S11)", 354.72 / eps_ttm_q2, 327, "01-negocio.md (S11)", tol=3)
    chk("PER GAAP a 354,72 $ con BPA TTM a Q3-26 (P4) — tras resultados", 354.72 / eps_ttm_q3, 327, "01-negocio.md (S11, previo a resultados)", tol=3)

    # ---- 3b. (v2) D&A trimestral P4 y FY2021 frente al deck Q4-2021
    chk("D&A 9M2026 (10-Q) = 1T+2T+3T 2026 de P4 (1.590+1.619+1.852)", raw["dya_amortizacion_deterioro"]["9M2026"], 1590.0 + 1619 + 1852, P4)
    chk("D&A TTM P4 = 4T25+1T26+2T26+3T26 (1.643+1.590+1.619+1.852)", raw["dya_amortizacion_deterioro"]["TTM_Q3_2026"], 1643.0 + 1590 + 1619 + 1852, P4)
    D21 = "8-K Ex.99.1 Q4 2021 Update, acc. 0001564590-22-002476 (texto, cifras en B$ redondeadas)"
    chk("FY2021 BN atribuible (10-K FY2022) vs deck Q4-2021 (5,5 B$)", raw["beneficio_neto_atrib_comunes"]["FY2021"], 5500, D21, tol=50)
    chk("FY2021 FCF (10-K FY2022) vs deck Q4-2021 (5,0 B$)", sub(raw["flujo_caja_operativo"]["FY2021"], raw["capex"]["FY2021"]), 5000, D21, tol=50)
    chk("FY2021 capex (10-K FY2022) vs deck Q4-2021 (6,5 B$)", raw["capex"]["FY2021"], 6500, D21, tol=50)
    chk("FY2021 efectivo (10-K FY2022: 17.576) vs deck Q4-2021 (17,6 B$)", 17576.0, 17600, D21, tol=50)

    # ---- 3c. (v2) Descomposición de acciones a 30-sep-2026 (M acciones)
    # Fuentes: P2 (10-Q 3T26) portada, nota de BPA y estado de patrimonio; 10-Q 1T26 y 2T26 (estado de
    # patrimonio); 10-Q 3T25; Form 4 de E. Musk de 17-jun-2026 (ejercicio de 303.960.630 opciones de 2018,
    # 17.531.857 retenidas, posesión directa posterior 710.172.677); Form 4 de 4-ago-2025 (96.000.000
    # acciones restringidas, CEO Interim Award). Ver fuentes/nuevas_fase2_v2.md.
    SHR = {"portada_15oct26": 3952.757946, "balance_31dic25": 3751.0, "balance_30sep25": 3324.0,
           "balance_30jun25": 3224.0, "emit_1T26": 4.0, "emit_2T26": 194.0, "emit_3T26": 4.0, "emit_9M26": 202.0,
           "balance_30sep26": 3953.0, "basica_3T26": 3240.0, "diluida_3T26": 3541.0, "awards_3T26": 301.0,
           "basica_1T26": 3234.0, "basica_2T26": 3237.0, "basica_3T25": 3227.0, "emit_3T25": 100.0,
           "ceo2025_restringidas": 423.743904, "op2018_ejercidas": 303.960630, "op2018_retenidas": 17.531857,
           "interim2025": 96.0, "musk_directas_tras_ejercicio": 710.172677}
    op2018_netas = SHR["op2018_ejercidas"] - SHR["op2018_retenidas"]
    restr_excl_basica = SHR["ceo2025_restringidas"] + op2018_netas
    chk("Acciones: 31-dic-25 + emitidas 9M26 = 30-sep-26 (P2)", SHR["balance_31dic25"] + SHR["emit_9M26"], SHR["balance_30sep26"], "P2 estado de patrimonio")
    chk("Acciones: emitidas 1T+2T+3T 2026 = 9M26 (10-Q 1T/2T/3T26)", SHR["emit_1T26"] + SHR["emit_2T26"] + SHR["emit_3T26"], SHR["emit_9M26"], "10-Q 1T26, 2T26, 3T26")
    chk("Acciones: básica + stock-based awards = diluida 3T26 (P2)", SHR["basica_3T26"] + SHR["awards_3T26"], SHR["diluida_3T26"], "P2 nota de BPA")
    chk("Acciones: directas de Musk = restringidas CEO 2025 + netas del ejercicio 2018 (Form 4)", restr_excl_basica, SHR["musk_directas_tras_ejercicio"], "Form 4 17-jun-2026", tol=0.001)
    chk("Acciones: emitidas 2T26 ≈ netas 2018 − Interim 2025 cancelada (+~4 empleados)", op2018_netas - SHR["interim2025"], SHR["emit_2T26"], "10-Q 2T26 / Form 4", tol=5)
    chk("Acciones: emitidas 4T25 (31-dic-25 − 30-sep-25) ≈ restringidas CEO 2025", SHR["balance_31dic25"] - SHR["balance_30sep25"], SHR["ceo2025_restringidas"], "10-Q 3T25 / P2 / Form 4", tol=5)
    chk("Acciones: emitidas 3T25 ≈ Interim Award 2025 (96 M)", SHR["emit_3T25"], SHR["interim2025"], "10-Q 3T25 / Form 4 ago-2025", tol=5)
    chk("Acciones: portada − básica 3T26 ≈ restringidas no ganadas (CEO 2025 + 2018 netas)", SHR["portada_15oct26"] - SHR["basica_3T26"], restr_excl_basica, "P2 / Form 4", tol=5)
    chk("Acciones: básica apenas varía 1T→3T26 pese a +194 M en 2T (restringidas fuera de la básica)", SHR["basica_3T26"] - SHR["basica_1T26"], SHR["emit_1T26"] + SHR["emit_3T26"], "10-Q 1T26 / 3T26", tol=5)

    # ---- 4. Ratios
    out = []

    def put(metric, unit, vals, method):
        out.append({"metrica": metric, "unidad": unit, **{y: vals.get(y) for y in YEARS}, "metodo": method})

    def series(m):
        return {y: s[m][y] for y in YEARS}

    for m in FLOW + STOCK + ["acciones_diluidas_media"]:
        put(m, "M USD" if m != "acciones_diluidas_media" else "M acciones", series(m),
            "Dato (FY2025 flujos = 9M25+Q4-25; TTM = FY25+9M26-9M25; balances a cierre)")

    debt = {y: add(s["deuda_corriente"][y], s["deuda_no_corriente"][y]) for y in YEARS}
    fcf = {y: sub(s["flujo_caja_operativo"][y], s["capex"][y]) for y in YEARS}
    ebit_ex_cred = {y: sub(s["beneficio_operativo"][y], s["creditos_regulatorios"][y]) for y in YEARS}
    put("deuda_total", "M USD", debt, "deuda corriente + no corriente (incl. arrend. financieros y deuda sin recurso)")
    put("caja_neta", "M USD", {y: sub(s["caja_y_inversiones_cp"][y], debt[y]) for y in YEARS}, "caja+inv. CP - deuda total")
    put("fcf", "M USD", fcf, "FCO - capex")
    put("fcf_menos_sbc", "M USD", {y: sub(fcf[y], s["sbc"][y]) for y in YEARS}, "FCF - SBC (SBC tratado como coste real)")
    put("beneficio_operativo_sin_creditos", "M USD", ebit_ex_cred, "benef. operativo - créditos regulatorios (créditos asumidos ~100 % margen)")

    da = series("dya_amortizacion_deterioro")
    put("capex_neto_de_dya", "M USD", {y: sub(s["capex"][y], da[y]) for y in YEARS}, "capex - D&A (D&A incluye deterioros)")
    put("ebitda_aprox", "M USD", {y: add(s["beneficio_operativo"][y], da[y]) for y in YEARS}, "benef. operativo + D&A (sin ajustar SBC; no es el EBITDA ajustado de Tesla)")
    rev = series("ingresos_totales")
    for name, m in [("margen_bruto", "beneficio_bruto"), ("margen_operativo", "beneficio_operativo"),
                    ("margen_neto", "beneficio_neto_atrib_comunes"), ("margen_fco", "flujo_caja_operativo"),
                    ("capex_sobre_ingresos", "capex"), ("sbc_sobre_ingresos", "sbc"),
                    ("dya_sobre_ingresos", "dya_amortizacion_deterioro")]:
        put(name, "%", {y: div(s[m][y], rev[y]) for y in YEARS}, f"{m} / ingresos totales")
    put("margen_fcf", "%", {y: div(fcf[y], rev[y]) for y in YEARS}, "FCF / ingresos totales")
    put("margen_operativo_sin_creditos", "%", {y: div(ebit_ex_cred[y], rev[y]) for y in YEARS}, "(benef. operativo - créditos) / ingresos")
    put("creditos_sobre_benef_operativo", "%", {y: div(s["creditos_regulatorios"][y], s["beneficio_operativo"][y]) for y in YEARS}, "créditos regulatorios / benef. operativo")
    put("creditos_sobre_benef_neto", "%", {y: div(s["creditos_regulatorios"][y], s["beneficio_neto_atrib_comunes"][y]) for y in YEARS}, "créditos regulatorios / benef. neto (antes de impuestos sobre créditos; orientativo)")
    put("capex_sobre_fco", "%", {y: div(s["capex"][y], s["flujo_caja_operativo"][y]) for y in YEARS}, "capex / FCO")
    for name, m in [("peso_automocion", "ingresos_automocion_total"), ("peso_energia", "ingresos_energia"),
                    ("peso_servicios", "ingresos_servicios_otros"), ("peso_creditos", "creditos_regulatorios")]:
        put(name, "%", {y: div(s[m][y], rev[y]) for y in YEARS}, f"{m} / ingresos totales")

    # Crecimientos interanuales (TTM vs FY2025 no es interanual: se calcula TTM vs TTM año anterior no disponible)
    for m in ["ingresos_totales", "ingresos_automocion_total", "creditos_regulatorios", "ingresos_energia",
              "ingresos_servicios_otros", "beneficio_bruto", "beneficio_operativo",
              "beneficio_neto_atrib_comunes", "flujo_caja_operativo", "capex", "sbc", "acciones_diluidas_media"]:
        g = {}
        for i, y in enumerate(YEARS[:-1]):
            g[y] = None if i == 0 else sub(div(s[m][y], s[m][YEARS[i - 1]]), 1)
        g["TTM_Q3_2026"] = None
        put("crec_" + m, "%", g, "variación interanual (FY vs FY anterior)")
    g = {y: None for y in YEARS}
    g["FY2025"] = sub(div(fcf["FY2025"], fcf["FY2024"]), 1)
    g["FY2022"] = sub(div(fcf["FY2022"], fcf["FY2021"]), 1)
    g["FY2023"] = sub(div(fcf["FY2023"], fcf["FY2022"]), 1)
    g["FY2024"] = sub(div(fcf["FY2024"], fcf["FY2023"]), 1)
    put("crec_fcf", "%", g, "variación interanual del FCF")

    # Crecimiento 9M2026 vs 9M2025 (comparable, primario) -> en columna TTM se deja aparte
    ytd = {}
    for m in ["ingresos_totales", "ingresos_automocion_total", "creditos_regulatorios", "ingresos_energia",
              "ingresos_servicios_otros", "beneficio_bruto", "beneficio_operativo", "beneficio_neto_atrib_comunes",
              "flujo_caja_operativo", "capex", "sbc"]:
        ytd[m] = sub(div(raw[m]["9M2026"], raw[m]["9M2025"]), 1)
    for m, v in ytd.items():
        put("crec_9M26_vs_9M25_" + m, "%", {"TTM_Q3_2026": v}, "9M2026 / 9M2025 - 1 (10-Q Q3 2026 vs 10-Q Q3 2025)")

    # CAGR FY2021-FY2025
    for m in ["ingresos_totales", "ingresos_energia", "ingresos_servicios_otros", "ingresos_automocion_total"]:
        put("cagr_21_25_" + m, "%", {"FY2025": (s[m]["FY2025"] / s[m]["FY2021"]) ** (1 / 4) - 1}, "CAGR 4 años FY2021->FY2025")

    # ROIC
    nopat = {y: None if s["beneficio_operativo"][y] is None else s["beneficio_operativo"][y] * (1 - TAX_NORM) for y in YEARS}
    ic_a = {y: sub(add(s["patrimonio_neto_accionistas"][y], debt[y]), s["caja_y_inversiones_cp"][y]) for y in YEARS}
    ic_b = {y: add(s["patrimonio_neto_accionistas"][y], debt[y]) for y in YEARS}
    prev = {"FY2021": None, "FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024"}
    # TTM: saldo inicial = 30-sep-2025
    ic_a_open_ttm = sub(add(raw["patrimonio_neto_accionistas"]["9M2025"], add(raw["deuda_corriente"]["9M2025"], raw["deuda_no_corriente"]["9M2025"])), raw["caja_y_inversiones_cp"]["9M2025"])
    ic_b_open_ttm = add(raw["patrimonio_neto_accionistas"]["9M2025"], add(raw["deuda_corriente"]["9M2025"], raw["deuda_no_corriente"]["9M2025"]))

    def avg(ic, y, open_ttm):
        if y == "TTM_Q3_2026":
            return (ic[y] + open_ttm) / 2
        p = prev[y]
        return ic[y] if p is None else (ic[y] + ic[p]) / 2

    put("nopat_21pct", "M USD", nopat, "benef. operativo x (1-0,21)")
    put("capital_invertido_A_neto_caja", "M USD", ic_a, "patrimonio + deuda - caja e inv. CP (saldo final)")
    put("capital_invertido_B_bruto", "M USD", ic_b, "patrimonio + deuda (saldo final)")
    put("roic_A_neto_caja", "%", {y: div(nopat[y], avg(ic_a, y, ic_a_open_ttm)) for y in YEARS}, "NOPAT / capital invertido A medio (FY2021: saldo final)")
    put("roic_B_bruto", "%", {y: div(nopat[y], avg(ic_b, y, ic_b_open_ttm)) for y in YEARS}, "NOPAT / capital invertido B medio (FY2021: saldo final)")
    put("roe", "%", {y: div(s["beneficio_neto_atrib_comunes"][y], avg({k: s["patrimonio_neto_accionistas"][k] for k in YEARS}, y, raw["patrimonio_neto_accionistas"]["9M2025"])) for y in YEARS}, "benef. neto / patrimonio medio")

    # Sensibilidad ROIC al tipo impositivo y variaciones acumuladas citadas en el documento
    for t in (0.15, 0.25):
        put(f"roic_A_tipo_{int(t*100)}pct", "%", {y: div(None if s["beneficio_operativo"][y] is None else s["beneficio_operativo"][y] * (1 - t), avg(ic_a, y, ic_a_open_ttm)) for y in YEARS}, f"sensibilidad: NOPAT con tipo {int(t*100)} %")
    put("var_acum_ventas_vehiculos_23_25", "%", {"FY2025": div(s["auto_ventas"]["FY2025"], s["auto_ventas"]["FY2023"]) - 1}, "venta vehículos FY2025/FY2023 - 1")
    put("multiplo_energia_21_25", "x", {"FY2025": div(s["ingresos_energia"]["FY2025"], s["ingresos_energia"]["FY2021"])}, "energía FY2025 / FY2021")
    put("var_patrimonio_22_3T26", "%", {"TTM_Q3_2026": div(s["patrimonio_neto_accionistas"]["TTM_Q3_2026"], s["patrimonio_neto_accionistas"]["FY2022"]) - 1}, "patrimonio 30-sep-26 / 31-dic-22 - 1")
    put("nopat_max_sobre_ttm", "x", {"TTM_Q3_2026": div(nopat["FY2022"], nopat["TTM_Q3_2026"])}, "NOPAT FY2022 / NOPAT TTM")
    put("var_caja_neta_9M26", "M USD", {"TTM_Q3_2026": sub(sub(s["caja_y_inversiones_cp"]["TTM_Q3_2026"], debt["TTM_Q3_2026"]), sub(s["caja_y_inversiones_cp"]["FY2025"], debt["FY2025"]))}, "caja neta 30-sep-26 - caja neta 31-dic-25")
    put("multiplo_caja_neta_21_3T26", "x", {"TTM_Q3_2026": div(sub(s["caja_y_inversiones_cp"]["TTM_Q3_2026"], debt["TTM_Q3_2026"]), sub(s["caja_y_inversiones_cp"]["FY2021"], debt["FY2021"]))}, "caja neta 30-sep-26 / 31-dic-21")
    put("var_sbc_24_ttm", "%", {"TTM_Q3_2026": div(s["sbc"]["TTM_Q3_2026"], s["sbc"]["FY2024"]) - 1}, "SBC TTM / FY2024 - 1")

    # (v2) Descomposición de acciones a 3T-2026 (M acciones; columna TTM_Q3_2026)
    put("acc_portada_15oct26", "M acciones", {"TTM_Q3_2026": SHR["portada_15oct26"]}, "portada 10-Q 3T26 (P2)")
    put("acc_basica_media_3T26", "M acciones", {"TTM_Q3_2026": SHR["basica_3T26"]}, "nota de BPA P2")
    put("acc_restringidas_ceo2025", "M acciones", {"TTM_Q3_2026": SHR["ceo2025_restringidas"]}, "Form 4: 423.743.904 restringidas; en portada, fuera de básica y de diluida (no 'ganadas')")
    put("acc_netas_ejercicio_2018", "M acciones", {"TTM_Q3_2026": op2018_netas}, "Form 4 17-jun-26: 303,96 ejercidas - 17,53 retenidas; en portada, fuera de básica; vesting por servicio 19-ene-2028")
    put("acc_residuo_portada_menos_basica", "M acciones", {"TTM_Q3_2026": SHR["portada_15oct26"] - SHR["basica_3T26"] - restr_excl_basica}, "portada - básica - restringidas: desfase media/saldo y emisiones de empleados")
    put("acc_stock_based_awards_3T26", "M acciones", {"TTM_Q3_2026": SHR["awards_3T26"]}, "diluida - básica (P2), método de tesorería")
    put("acc_awards_no_incluidos_en_portada_aprox", "M acciones", {"TTM_Q3_2026": SHR["awards_3T26"] - op2018_netas}, "INFERENCIA: 301 - acciones netas 2018 (ya en portada) = incentivos de empleados aún no emitidos")
    put("acc_doble_computo_portada_mas_301", "M acciones", {"TTM_Q3_2026": op2018_netas}, "INFERENCIA: parte de las 301 que ya está en la portada")
    put("acc_totalmente_diluidas_aprox", "M acciones", {"TTM_Q3_2026": SHR["portada_15oct26"] + SHR["awards_3T26"] - op2018_netas}, "portada + incentivos no emitidos (incluye las 423,7 M del CEO aún no ganadas)")

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["metrica", "unidad"] + YEARS + ["metodo"])
        w.writeheader()
        for r in out:
            w.writerow({k: (round(v, 4) if isinstance(v, float) and r["unidad"] == "%" else (round(v, 1) if isinstance(v, float) else v)) for k, v in r.items()})
    with open(CHK, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["control", "calculado", "referencia", "fuente_referencia", "diferencia", "resultado"])
        w.writeheader()
        for c in checks:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in c.items()})
    print(f"Escrito {OUT} ({len(out)} filas) y {CHK} ({len(checks)} controles)")
    for c in checks:
        print(f"  [{c['resultado']}] {c['control']}: calc={c['calculado']} ref={c['referencia']} dif={c['diferencia']}")


if __name__ == "__main__":
    main()
