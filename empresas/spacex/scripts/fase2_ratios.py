#!/usr/bin/env python3
"""Fase 2 (Financieros) — SpaceX (SPCX): ratios, controles de cuadre y análisis de dependencias.

Lee data/spacex_financials.csv (generado por fase2_datos.py) y:
1. Controles de cuadre (data/checks.csv): líneas = segmento, segmentos = total, Q1+Q2 = 6M, 6M+Q3 = 9M,
   conciliaciones de EBITDA ajustado (consolidada y por segmento), cuenta de resultados, deuda,
   acciones por clase y su movimiento en 9M26, TTM recalculado. Si alguno falla, termina con código 1.
2. Ratios (data/ratios.csv): crecimiento, márgenes, FCF, intensidad de capex, deuda neta, rentabilidad
   por segmento, dilución y trimestres implícitos (4T25, 2T26, 3T26 de flujos de caja).
3. Puntos de contraste de la fase 1:
   a) capex de Space 9M26 = capex de Space FY2025 (3.832 M$): descomposición trimestral.
   b) Customer B: importes implícitos, peso en el crecimiento y en el margen de SI, escenarios.
4. Comparabilidad por la fusión con xAI (control común): "SpaceX heredada" (Space + Connectivity)
   frente al segmento AI/SI.

Todas las cifras de docs/02-financieros.md se copian de la salida impresa de este script.
Formato de salida: miles con punto, decimales con coma (como en el documento).

Uso:  python empresas/spacex/scripts/fase2_ratios.py
"""
import csv
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "data", "spacex_financials.csv")
OUT = os.path.join(BASE, "data", "ratios.csv")
CHK = os.path.join(BASE, "data", "checks.csv")

# Tolerancia para sumas de trimestres: cada periodo se publica redondeado a M$ por separado
# (P2, P6, P3); en 2025 aparecen diferencias de 1-2 M$. Se listan en la salida como REDONDEO.
TOL_TRIM = 2.0
SEGS = ("space", "connectivity", "si")
LINEAS = {"space": ("ing_launch_services", "ing_launch_development"),
          "connectivity": ("ing_consumer", "ing_enterprise_government"),
          "si": ("ing_advertising", "ing_si_solutions_infra")}


# ----------------------------------------------------------------------------- utilidades
def load():
    data, tipos = {}, {}
    with open(SRC, encoding="utf-8") as f:
        rd = csv.DictReader(f)
        periodos = [c for c in rd.fieldnames if c not in ("metrica", "unidad", "tipo", "nota")
                    and not c.startswith("fuente_")]
        for r in rd:
            data[r["metrica"]] = {p: (float(r[p]) if r[p] not in ("", None) else None) for p in periodos}
            tipos[r["metrica"]] = r["tipo"]
    return data, tipos, periodos


def g(d, m, p):
    return d.get(m, {}).get(p)


def add(*xs):
    return None if any(x is None for x in xs) else sum(xs)


def sub(a, b):
    return None if a is None or b is None else a - b


def div(a, b):
    return None if a is None or b in (None, 0) else a / b


def es_num(x):
    return x is not None


def f_m(x, dec=0):
    """Importe con miles '.' y decimales ','."""
    if x is None:
        return "SIN DATO"
    s = f"{x:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def f_p(x, dec=1):
    """Porcentaje a partir de un cociente (0,353 -> '35,3 %')."""
    if x is None:
        return "SIN DATO"
    return f_m(100 * x, dec) + " %"


def f_x(x, dec=1):
    return "SIN DATO" if x is None else f_m(x, dec) + "x"


# ----------------------------------------------------------------------------- main
def main():
    d, tipos, periodos = load()
    checks, ratios = [], []

    def chk(nombre, calc, ref, ref_src, tol=0.5):
        dif = sub(calc, ref)
        ok = dif is not None and abs(dif) <= tol
        checks.append({"control": nombre, "calculado": calc, "referencia": ref, "fuente_referencia": ref_src,
                       "diferencia": dif, "tolerancia": tol,
                       "resultado": "OK" if ok else ("SIN DATO" if dif is None else "DISCREPANCIA")})

    def rat(ind, per, val, unidad, formula):
        ratios.append({"indicador": ind, "periodo": per,
                       "valor": None if val is None else round(val, 6), "unidad": unidad, "formula": formula})
        return val

    P_ALL = [p for p in periodos if p not in ("FY2021", "FY2022")]

    # ============================================================ 1. CONTROLES
    for p in P_ALL:
        for seg, (a, b) in LINEAS.items():
            if es_num(g(d, a, p)) and es_num(g(d, "ing_" + seg, p)):
                chk(f"{p}: {a} + {b} = ing_{seg}", add(g(d, a, p), g(d, b, p)), g(d, "ing_" + seg, p), "CSV")
        if es_num(g(d, "ing_space", p)):
            chk(f"{p}: ingresos segmentos = ingresos_totales",
                add(*(g(d, "ing_" + s, p) for s in SEGS)), g(d, "ingresos_totales", p), "CSV")
        for base, tot in (("opinc_", "beneficio_operativo"), ("dya_", "dya_total"), ("sbc_", "sbc_ordinaria_total"),
                          ("ebitda_aj_", "ebitda_ajustado"), ("coste_ingresos_", "coste_ingresos"), ("id_", "id_total")):
            vals = [g(d, base + s, p) for s in SEGS]
            if all(es_num(v) for v in vals) and es_num(g(d, tot, p)):
                chk(f"{p}: suma segmentos {base}* = {tot}", sum(vals), g(d, tot, p), "CSV")
        vals = [g(d, "capex_" + s, p) for s in SEGS]
        if all(es_num(v) for v in vals) and es_num(g(d, "capex", p)):
            chk(f"{p}: suma capex por segmento = capex (estado de flujos)", sum(vals), g(d, "capex", p), "CSV")
        # cuenta de resultados
        if es_num(g(d, "costes_totales", p)):
            chk(f"{p}: coste+I+D+SG&A+reestr.+deterioro = costes_totales",
                add(g(d, "coste_ingresos", p), g(d, "id_total", p), g(d, "sga", p), g(d, "reestructuracion", p),
                    g(d, "deterioros", p)), g(d, "costes_totales", p), "CSV")
            chk(f"{p}: ingresos - costes_totales = beneficio_operativo",
                sub(g(d, "ingresos_totales", p), g(d, "costes_totales", p)), g(d, "beneficio_operativo", p), "CSV")
        if es_num(g(d, "bai", p)):
            chk(f"{p}: operativo - intereses + ingresos financieros + otros = BAI",
                add(g(d, "beneficio_operativo", p), -g(d, "gastos_intereses", p), g(d, "ingresos_intereses", p),
                    g(d, "otros_resultados_netos", p)), g(d, "bai", p), "CSV")
        if es_num(g(d, "impuestos", p)) and es_num(g(d, "bai", p)):
            chk(f"{p}: BAI - impuestos = beneficio_neto", sub(g(d, "bai", p), g(d, "impuestos", p)),
                g(d, "beneficio_neto", p), "CSV")
        # conciliación consolidada beneficio neto -> EBITDA ajustado
        comp = ("dya_total", "sbc_ordinaria_total", "sbc_adquisiciones_si", "costes_adquisicion_si",
                "reestructuracion", "deterioros", "gastos_intereses", "impuestos")
        if all(es_num(g(d, m, p)) for m in comp + ("beneficio_neto", "ingresos_intereses", "otros_resultados_netos",
                                                    "ebitda_ajustado")):
            calc = (g(d, "beneficio_neto", p) + sum(g(d, m, p) for m in comp)
                    - g(d, "ingresos_intereses", p) - g(d, "otros_resultados_netos", p))
            chk(f"{p}: conciliación beneficio neto -> EBITDA ajustado", calc, g(d, "ebitda_ajustado", p),
                "P2 p. 119 / P6 p. 46 / P3 p. 50")
        # conciliación por segmento
        for s in SEGS:
            extra = [g(d, "reestructuracion_si", p), g(d, "sbc_adquisiciones_si", p),
                     g(d, "costes_adquisicion_si", p)] if s == "si" else []
            parts = [g(d, "opinc_" + s, p), g(d, "dya_" + s, p), g(d, "sbc_" + s, p), g(d, "deterioro_" + s, p)] + extra
            if all(es_num(x) for x in parts) and es_num(g(d, "ebitda_aj_" + s, p)):
                chk(f"{p}: conciliación segmento {s} -> EBITDA ajustado", sum(parts), g(d, "ebitda_aj_" + s, p),
                    "P2 p. 120-121 / P3 p. 51-52")
    # Q1 + Q2 = 6M ; 6M + Q3 = 9M ; Q1+Q2+Q3 = 9M
    for m in d:
        if tipos[m] != "flujo":
            continue
        for y in ("2025", "2026"):
            q1, q2, h1, q3, m9 = (g(d, m, f"Q1_{y}"), g(d, m, f"Q2_{y}"), g(d, m, f"6M{y}"),
                                  g(d, m, f"Q3_{y}"), g(d, m, f"9M{y}"))
            if es_num(q1) and es_num(q2) and es_num(h1):
                chk(f"{m} {y}: Q1 + Q2 = 6M", q1 + q2, h1, "CSV", tol=TOL_TRIM)
            if es_num(h1) and es_num(q3) and es_num(m9):
                chk(f"{m} {y}: 6M + Q3 = 9M", h1 + q3, m9, "CSV", tol=TOL_TRIM)
            elif not es_num(h1) and es_num(q1) and es_num(q2) and es_num(q3) and es_num(m9):
                chk(f"{m} {y}: Q1 + Q2 + Q3 = 9M", q1 + q2 + q3, m9, "CSV", tol=TOL_TRIM)
    # SBC del estado de flujos = ordinaria + adquisiciones
    for p in ("FY2023", "FY2024", "FY2025", "9M2025", "9M2026", "Q1_2026"):
        chk(f"{p}: sbc_flujo_caja = sbc ordinaria + sbc adquisiciones",
            add(g(d, "sbc_ordinaria_total", p), g(d, "sbc_adquisiciones_si", p)), g(d, "sbc_flujo_caja", p), "CSV")
    # capex 3T = 9M - 6M (consolidado) frente a la suma de segmentos del 3T
    chk("Q3_2026: capex 9M - 6M = suma capex segmentos 3T",
        sub(g(d, "capex", "9M2026"), g(d, "capex", "6M2026")),
        add(*(g(d, "capex_" + s, "Q3_2026") for s in SEGS)), "P5 p. 4 da 19.593")
    # deuda
    for p in ("FY2024", "FY2025", "9M2026"):
        chk(f"{p}: deuda contable (corr. + no corr.) = principal + arrend. - costes pendientes",
            add(g(d, "deuda_y_arrendamientos_corriente", p), g(d, "deuda_y_arrendamientos_no_corriente", p)),
            add(g(d, "deuda_principal", p), g(d, "arrendamiento_financiero", p), -g(d, "costes_financiacion_pendientes", p)),
            "P2 Note 10 / P3 Note 9")
    for p in ("FY2025", "9M2026"):
        chk(f"{p}: ingresos diferidos corr. + no corr. = total publicado",
            add(g(d, "ingresos_diferidos_corriente", p), g(d, "ingresos_diferidos_no_corriente", p)),
            g(d, "ingresos_diferidos_total_publicado", p), "P2/P3 Note 3")
    # acciones
    for p in ("FY2024", "FY2025", "9M2025", "9M2026"):
        chk(f"{p}: acciones A + B + C = total ordinarias",
            add(g(d, "acciones_clase_A", p), g(d, "acciones_clase_B", p), g(d, "acciones_clase_C", p)),
            g(d, "acciones_ordinarias_total", p), "P3 Note 12 / estado de patrimonio", tol=1.0)
    movs = ("acc_emitidas_opv_9M26", "acc_emitidas_netas_9M26", "acc_conversion_pref_xai_9M26", "acc_recompra_xai_9M26",
            "acc_conversion_pref_9M26", "acc_recompra_9M26", "acc_combinaciones_negocio_9M26")
    chk("9M2026: acciones 31-dic-2025 + movimientos = 30-sep-2026",
        g(d, "acciones_ordinarias_total", "FY2025") + sum(g(d, m, "9M2026") for m in movs),
        g(d, "acciones_ordinarias_total", "9M2026"), "P3 p. 7")
    # TTM recalculado
    for m in d:
        if tipos[m] == "flujo" and es_num(g(d, m, "TTM_Q3_2026")):
            chk(f"TTM {m} = FY2025 + 9M2026 - 9M2025",
                g(d, m, "FY2025") + g(d, m, "9M2026") - g(d, m, "9M2025"), g(d, m, "TTM_Q3_2026"), "CSV")

    # Customer B (consistencia de porcentajes redondeados a 0,1 pp)
    rev = lambda p: g(d, "ingresos_totales", p)  # noqa: E731
    pctB = lambda p: g(d, "cliente_B_pct", p) / 100  # noqa: E731
    B = {p: pctB(p) * rev(p) for p in ("Q2_2026", "6M2026", "Q3_2026", "9M2026")}
    tolB = 0.0005 * (rev("6M2026") + rev("Q3_2026") + rev("9M2026"))
    chk("Customer B: implícito 6M26 + 3T26 = implícito 9M26 (tolerancia por redondeo de %)",
        B["6M2026"] + B["Q3_2026"], B["9M2026"], "P3/P6 Note 3", tol=tolB)

    n_ok = sum(c["resultado"] == "OK" for c in checks)
    n_bad = sum(c["resultado"] == "DISCREPANCIA" for c in checks)
    n_sd = sum(c["resultado"] == "SIN DATO" for c in checks)

    # ============================================================ 2. RATIOS
    P_R = ("FY2023", "FY2024", "FY2025", "TTM_Q3_2026", "9M2025", "9M2026", "Q1_2026", "Q2_2026",
           "Q3_2025", "Q3_2026")
    comparables = (("FY2024", "FY2023"), ("FY2025", "FY2024"), ("9M2026", "9M2025"), ("Q3_2026", "Q3_2025"),
                   ("Q2_2026", "Q2_2025"), ("Q1_2026", "Q1_2025"))
    print("=" * 100)
    print("FASE 2 — SpaceX: ratios y controles (cifras en M$ salvo indicación)")
    print("=" * 100)

    print("\n--- 1. Ingresos y crecimiento ---")
    for m in ("ingresos_totales", "ing_space", "ing_launch_services", "ing_launch_development", "ing_connectivity",
              "ing_consumer", "ing_enterprise_government", "ing_si", "ing_advertising", "ing_si_solutions_infra"):
        vals = "  ".join(f"{p} {f_m(g(d, m, p))}" for p in ("FY2023", "FY2024", "FY2025", "9M2025", "9M2026", "TTM_Q3_2026"))
        crec = "  ".join(f"{a}/{b} {f_p(rat('crec_' + m, a + '/' + b, sub(div(g(d, m, a), g(d, m, b)), 1), '%', f'{m} {a}/{b} - 1'))}"
                         for a, b in comparables if es_num(g(d, m, b)))
        print(f"{m:27s} {vals}\n{'':27s} crecimiento: {crec}")
    print("TTM vs TTM del año anterior: SIN DATO (no hay 9M2024 publicado)")
    for p in P_R:
        tot = rev(p)
        if es_num(tot):
            pesos = "  ".join(f"{s} {f_p(rat('peso_' + s, p, div(g(d, 'ing_' + s, p), tot), '%', f'ing_{s}/ingresos_totales'))}"
                              for s in SEGS)
            print(f"Peso en ingresos {p:12s}: {pesos}")

    print("\n--- 2. Cuenta de resultados: márgenes consolidados ---")
    for p in P_R:
        r = rev(p)
        if not es_num(r):
            continue
        mb = rat("margen_bruto", p, div(sub(r, g(d, "coste_ingresos", p)), r), "%", "(ingresos - coste_ingresos)/ingresos")
        mo = rat("margen_operativo", p, div(g(d, "beneficio_operativo", p), r), "%", "beneficio_operativo/ingresos")
        mn = rat("margen_neto", p, div(g(d, "beneficio_neto", p), r), "%", "beneficio_neto/ingresos")
        me = rat("margen_ebitda_aj", p, div(g(d, "ebitda_ajustado", p), r), "%", "ebitda_ajustado/ingresos")
        idr = rat("id_sobre_ingresos", p, div(g(d, "id_total", p), r), "%", "id_total/ingresos")
        sbct = add(g(d, "sbc_ordinaria_total", p), g(d, "sbc_adquisiciones_si", p))
        sb = rat("sbc_sobre_ingresos", p, div(sbct, r), "%", "(sbc ordinaria + sbc adquisiciones)/ingresos")
        print(f"{p:12s} ingresos {f_m(r):>7s} | bruto {f_p(mb):>8s} | operativo {f_m(g(d, 'beneficio_operativo', p)):>7s} "
              f"({f_p(mo)}) | neto {f_m(g(d, 'beneficio_neto', p)):>7s} ({f_p(mn)}) | EBITDA aj. "
              f"{f_m(g(d, 'ebitda_ajustado', p)):>7s} ({f_p(me)}) | I+D/ing {f_p(idr)} | SBC {f_m(sbct)} ({f_p(sb)})")
    ttm_items = ("coste_ingresos", "id_total", "sga", "reestructuracion", "deterioros", "beneficio_operativo",
                 "gastos_intereses", "ingresos_intereses", "otros_resultados_netos", "bai", "impuestos",
                 "beneficio_neto", "dya_total", "sbc_ordinaria_total", "sbc_adquisiciones_si", "ebitda_ajustado",
                 "flujo_caja_operativo", "capex")
    print("TTM_Q3_2026 (FY2025 + 9M2026 - 9M2025): " +
          "; ".join(f"{m} {f_m(g(d, m, 'TTM_Q3_2026'))}" for m in ttm_items))

    print("\n--- 3. Conciliación EBITDA ajustado (beneficio neto -> EBITDA ajustado) ---")
    for p in ("FY2023", "FY2024", "FY2025", "9M2025", "9M2026", "Q3_2025", "Q3_2026", "TTM_Q3_2026"):
        partes = [("beneficio neto", g(d, "beneficio_neto", p)), ("+ D&A", g(d, "dya_total", p)),
                  ("+ SBC", g(d, "sbc_ordinaria_total", p)), ("+ SBC adquis.", g(d, "sbc_adquisiciones_si", p)),
                  ("+ costes adquis.", g(d, "costes_adquisicion_si", p)), ("+ reestr.", g(d, "reestructuracion", p)),
                  ("+ deterioros", g(d, "deterioros", p)), ("+ gastos financ.", g(d, "gastos_intereses", p)),
                  ("- ingresos financ.", g(d, "ingresos_intereses", p)),
                  ("- otros resultados", g(d, "otros_resultados_netos", p)), ("+ impuestos", g(d, "impuestos", p)),
                  ("= EBITDA aj.", g(d, "ebitda_ajustado", p))]
        print(f"{p:12s} " + " | ".join(f"{n} {f_m(v)}" for n, v in partes))
        dya_sbc = add(g(d, "dya_total", p), g(d, "sbc_ordinaria_total", p), g(d, "sbc_adquisiciones_si", p))
        rat("ebitda_aj_menos_operativo", p, sub(g(d, "ebitda_ajustado", p), g(d, "beneficio_operativo", p)), "M USD",
            "ebitda_ajustado - beneficio_operativo")
        rat("peso_sbc_en_ajustes", p, div(add(g(d, "sbc_ordinaria_total", p), g(d, "sbc_adquisiciones_si", p)),
                                          sub(g(d, "ebitda_ajustado", p), g(d, "beneficio_operativo", p))), "%",
            "SBC total / (EBITDA aj. - operativo)")
        print(f"{'':12s} EBITDA aj. - resultado operativo = {f_m(sub(g(d, 'ebitda_ajustado', p), g(d, 'beneficio_operativo', p)))}"
              f"; de ello D&A + SBC = {f_m(dya_sbc)}; peso de la SBC en los ajustes = "
              f"{f_p(div(add(g(d, 'sbc_ordinaria_total', p), g(d, 'sbc_adquisiciones_si', p)), sub(g(d, 'ebitda_ajustado', p), g(d, 'beneficio_operativo', p))))}")

    print("\n--- 4. Rentabilidad por segmento ---")
    for s in SEGS:
        for p in P_R:
            r = g(d, "ing_" + s, p)
            if not es_num(r):
                continue
            mb = rat(f"margen_bruto_{s}", p, div(sub(r, g(d, "coste_ingresos_" + s, p)), r), "%", f"(ing - coste)/ing {s}")
            mo = rat(f"margen_operativo_{s}", p, div(g(d, "opinc_" + s, p), r), "%", f"opinc_{s}/ing_{s}")
            me = rat(f"margen_ebitda_aj_{s}", p, div(g(d, "ebitda_aj_" + s, p), r), "%", f"ebitda_aj_{s}/ing_{s}")
            ci = rat(f"capex_sobre_ingresos_{s}", p, div(g(d, "capex_" + s, p), r), "%", f"capex_{s}/ing_{s}")
            ec = rat(f"ebitda_aj_menos_capex_{s}", p, sub(g(d, "ebitda_aj_" + s, p), g(d, "capex_" + s, p)), "M USD",
                     f"ebitda_aj_{s} - capex_{s}")
            idr = rat(f"id_sobre_ingresos_{s}", p, div(g(d, "id_" + s, p), r), "%", f"id_{s}/ing_{s}")
            print(f"{s:12s} {p:12s} ing {f_m(r):>7s} | bruto {f_p(mb):>9s} | op {f_m(g(d, 'opinc_' + s, p)):>7s} "
                  f"({f_p(mo):>9s}) | EBITDA aj {f_m(g(d, 'ebitda_aj_' + s, p)):>7s} ({f_p(me):>9s}) | I+D/ing {f_p(idr):>8s} "
                  f"| capex {f_m(g(d, 'capex_' + s, p)):>7s} ({f_p(ci):>9s}) | EBITDA aj - capex {f_m(ec):>8s}")

    print("\n--- 5. Flujo de caja, capex y FCF ---")
    # Trimestres implícitos
    imp = {}
    for m in ("flujo_caja_operativo", "capex"):
        imp[(m, "Q2_2026")] = sub(g(d, m, "6M2026"), g(d, m, "Q1_2026"))
        imp[(m, "Q3_2026")] = sub(g(d, m, "9M2026"), g(d, m, "6M2026"))
        imp[(m, "Q2_2025")] = sub(g(d, m, "6M2025"), g(d, m, "Q1_2025"))
        imp[(m, "Q3_2025")] = sub(g(d, m, "9M2025"), g(d, m, "6M2025"))
        imp[(m, "Q4_2025")] = sub(g(d, m, "FY2025"), g(d, m, "9M2025"))
        for k, v in list(imp.items()):
            if k[0] == m:
                rat(m + "_implicito", k[1], v, "M USD", "diferencia de acumulados")
    for p in ("FY2023", "FY2024", "FY2025", "9M2025", "9M2026", "TTM_Q3_2026"):
        fco, cx, r = g(d, "flujo_caja_operativo", p), g(d, "capex", p), rev(p)
        sbct = add(g(d, "sbc_ordinaria_total", p), g(d, "sbc_adquisiciones_si", p))
        fcf = rat("fcf", p, sub(fco, cx), "M USD", "flujo_caja_operativo - capex")
        rat("margen_fcf", p, div(fcf, r), "%", "fcf/ingresos")
        rat("fcf_menos_sbc", p, sub(fcf, sbct), "M USD", "fcf - sbc total")
        rat("capex_sobre_ingresos", p, div(cx, r), "%", "capex/ingresos")
        rat("capex_sobre_dya", p, div(cx, g(d, "dya_total", p)), "x", "capex/dya_total")
        rat("fco_sobre_ebitda_aj", p, div(fco, g(d, "ebitda_ajustado", p)), "%", "flujo_caja_operativo/ebitda_ajustado")
        print(f"{p:12s} FCO {f_m(fco):>7s} | capex {f_m(cx):>7s} | FCF {f_m(fcf):>8s} (margen {f_p(div(fcf, r))}) | "
              f"FCF - SBC {f_m(sub(fcf, sbct)):>8s} | capex/ingresos {f_p(div(cx, r))} | capex/D&A {f_x(div(cx, g(d, 'dya_total', p)))}"
              f" | FCO/EBITDA aj {f_p(div(fco, g(d, 'ebitda_ajustado', p)))}")
    for q in ("Q1_2025", "Q2_2025", "Q3_2025", "Q4_2025", "Q1_2026", "Q2_2026", "Q3_2026"):
        fco = g(d, "flujo_caja_operativo", q) if es_num(g(d, "flujo_caja_operativo", q)) else imp.get(("flujo_caja_operativo", q))
        cx = g(d, "capex", q) if es_num(g(d, "capex", q)) else imp.get(("capex", q))
        rat("fcf_trimestral", q, sub(fco, cx), "M USD", "FCO - capex (trimestre; implícito si no se publica)")
        print(f"Trimestre {q}: FCO {f_m(fco):>7s} | capex {f_m(cx):>7s} | FCF {f_m(sub(fco, cx)):>8s}")
    p = "9M2026"
    fcf_amp = (g(d, "flujo_caja_operativo", p) - g(d, "capex", p) - g(d, "intereses_capitalizados", p)
               + g(d, "reembolsos_producto", p) - g(d, "ppe_financiado_otras_financiaciones", p))
    rat("fcf_ampliado", p, fcf_amp, "M USD", "FCO - capex - intereses capitalizados + reembolsos - PP&E financiado")
    print(f"9M2026 FCF ampliado (FCO - capex - int. capitalizados {f_m(g(d, 'intereses_capitalizados', p))} + reembolsos "
          f"{f_m(g(d, 'reembolsos_producto', p))} - PP&E financiado {f_m(g(d, 'ppe_financiado_otras_financiaciones', p))}) = {f_m(fcf_amp)}")
    print(f"Capex pendiente de pago (PP&E en cuentas a pagar): 31-dic-2023 {f_m(g(d, 'ppe_en_cuentas_a_pagar', 'FY2023'))}, "
          f"31-dic-2024 {f_m(g(d, 'ppe_en_cuentas_a_pagar', 'FY2024'))}, 31-dic-2025 {f_m(g(d, 'ppe_en_cuentas_a_pagar', 'FY2025'))}, "
          f"30-sep-2026 {f_m(g(d, 'ppe_en_cuentas_a_pagar', '9M2026'))}")
    print(f"Capex 9M26 por segmento: " + ", ".join(
        f"{s} {f_m(g(d, 'capex_' + s, p))} ({f_p(div(g(d, 'capex_' + s, p), g(d, 'capex', p)))})" for s in SEGS))
    print(f"Capex TTM por segmento: " + ", ".join(
        f"{s} {f_m(g(d, 'capex_' + s, 'TTM_Q3_2026'))} ({f_p(div(g(d, 'capex_' + s, 'TTM_Q3_2026'), g(d, 'capex', 'TTM_Q3_2026')))})" for s in SEGS))
    for a, b in (("FY2024", "FY2023"), ("FY2025", "FY2024"), ("9M2026", "9M2025")):
        print(f"Crecimiento capex {a}/{b}: total {f_p(sub(div(g(d, 'capex', a), g(d, 'capex', b)), 1))}; " + ", ".join(
            f"{s} {f_p(rat('crec_capex_' + s, a + '/' + b, sub(div(g(d, 'capex_' + s, a), g(d, 'capex_' + s, b)), 1), '%', 'capex a/b - 1'))}"
            for s in SEGS))
    print(f"Variación de capital circulante 9M26 que explica parte del FCO: ingresos diferidos +4.922 y cuentas a cobrar "
          f"-2.882 son partidas leídas (P3 p. 9), no cálculos.")

    print("\n--- 6. Caja, deuda y deuda neta ---")
    for p in ("FY2024", "FY2025", "9M2026"):
        caja = add(g(d, "caja", p), g(d, "valores_negociables", p))
        deuda = add(g(d, "deuda_y_arrendamientos_corriente", p), g(d, "deuda_y_arrendamientos_no_corriente", p))
        dn = rat("deuda_neta_contable", p, sub(deuda, caja), "M USD", "deuda contable (incl. arrend. financ.) - caja - valores")
        dnp = rat("deuda_neta_principal", p, sub(add(g(d, "deuda_principal", p), g(d, "arrendamiento_financiero", p)), caja),
                  "M USD", "principal + arrend. financiero - caja - valores")
        vinc = add(g(d, "deuda_vinculada_corriente", p), g(d, "deuda_vinculada_no_corriente", p))
        pv = rat("peso_deuda_vinculada", p, div(vinc, deuda), "%", "deuda vinculada (Valor)/deuda contable")
        ebitda_ref = g(d, "ebitda_ajustado", "TTM_Q3_2026" if p == "9M2026" else p)
        ratio = rat("deuda_neta_sobre_ebitda_aj", p, div(dn, ebitda_ref), "x", "deuda neta contable / EBITDA aj. (FY o TTM)")
        int_ref = g(d, "gastos_intereses", "TTM_Q3_2026" if p == "9M2026" else p)
        cob = rat("cobertura_intereses_ebitda_aj", p, div(ebitda_ref, int_ref), "x", "EBITDA aj. / gastos por intereses (FY o TTM)")
        rat("caja_y_valores", p, caja, "M USD", "caja + valores negociables")
        rat("deuda_contable", p, deuda, "M USD", "deuda y arrendamientos corriente + no corriente")
        rat("deuda_vinculada", p, vinc, "M USD", "deuda vinculada corriente + no corriente")
        print(f"{p:8s} caja+valores {f_m(caja):>7s} | deuda contable {f_m(deuda):>7s} (principal {f_m(g(d, 'deuda_principal', p))} + "
              f"arrend. {f_m(g(d, 'arrendamiento_financiero', p))}) | deuda neta contable {f_m(dn):>8s} | deuda neta principal "
              f"{f_m(dnp):>8s} | deuda vinculada {f_m(vinc)} ({f_p(pv)}) | deuda neta/EBITDA aj {f_x(ratio, 2)} | "
              f"EBITDA aj/intereses {f_x(cob)}")
    print("(deuda neta negativa = caja neta; para 30-sep-2026 el EBITDA aj. y los intereses son TTM)")

    print("\n--- 7. Acciones, SBC y dilución ---")
    for p in ("FY2024", "FY2025", "9M2025", "9M2026"):
        print(f"{p:8s} A {f_m(g(d, 'acciones_clase_A', p))} | B {f_m(g(d, 'acciones_clase_B', p))} | C "
              f"{f_m(g(d, 'acciones_clase_C', p))} | total ordinarias {f_m(g(d, 'acciones_ordinarias_total', p))} | preferentes "
              f"{f_m(g(d, 'preferentes_convertibles_acciones', p))}")
    base_conv = add(g(d, "acciones_ordinarias_total", "9M2025"), g(d, "preferentes_xai_como_convertidas", "9M2025"),
                    g(d, "preferentes_spacex_como_convertidas", "9M2025"))
    fin = g(d, "acciones_ordinarias_total", "9M2026")
    dil_a = rat("dilucion_interanual_como_convertidas", "30-sep-2025->30-sep-2026", sub(div(fin, base_conv), 1), "%",
                "acciones 30-sep-2026 / (ordinarias + preferentes como convertidas a 30-sep-2025) - 1")
    print(f"Base como convertidas 30-sep-2025 = {f_m(base_conv)} (ordinarias {f_m(g(d, 'acciones_ordinarias_total', '9M2025'))} + "
          f"pref. xAI {f_m(g(d, 'preferentes_xai_como_convertidas', '9M2025'))} + pref. SpaceX "
          f"{f_m(g(d, 'preferentes_spacex_como_convertidas', '9M2025'))}); 30-sep-2026 = {f_m(fin)} -> variación {f_p(dil_a)}")
    nuevas = sum(g(d, m, "9M2026") for m in ("acc_emitidas_opv_9M26", "acc_emitidas_netas_9M26",
                                              "acc_combinaciones_negocio_9M26", "acc_recompra_xai_9M26", "acc_recompra_9M26"))
    conv = g(d, "acc_conversion_pref_xai_9M26", "9M2026") + g(d, "acc_conversion_pref_9M26", "9M2026")
    print(f"Movimiento 9M26: conversiones de preferentes {f_m(conv)}; emisiones netas de recompras {f_m(nuevas)} "
          f"(OPV {f_m(g(d, 'acc_emitidas_opv_9M26', '9M2026'))}, emitidas netas {f_m(g(d, 'acc_emitidas_netas_9M26', '9M2026'))}, "
          f"combinaciones {f_m(g(d, 'acc_combinaciones_negocio_9M26', '9M2026'))}, recompras "
          f"{f_m(g(d, 'acc_recompra_xai_9M26', '9M2026') + g(d, 'acc_recompra_9M26', '9M2026'))})")
    rat("emisiones_netas_9M26_sobre_base_convertida", "9M2026", div(nuevas, base_conv), "%", "emisiones netas 9M26 / base como convertidas")
    sin_musk = nuevas - 1302.072285
    rat("emisiones_netas_9M26_sin_restringidas_musk", "9M2026", div(sin_musk, base_conv), "%",
        "(emisiones netas - 1.302,07 M acciones B restringidas de Musk) / base")
    print(f"Emisiones netas 9M26 / base como convertidas = {f_p(div(nuevas, base_conv))}; sin las 1.302,07 M acciones B "
          f"restringidas de Musk (supuesto: incluidas en 'emitidas netas', ver doc) = {f_p(div(sin_musk, base_conv))}")
    pot = add(g(d, "opciones_vivas_clase_A", "9M2026"), g(d, "opciones_vivas_clase_B", "9M2026"), g(d, "rsu_vivas_clase_A", "9M2026"))
    rat("dilucion_potencial_opciones_rsu", "9M2026", div(pot, fin), "%", "(opciones A + B + RSU)/acciones 30-sep-2026")
    print(f"Dilución potencial por opciones y RSU vivas a 30-sep-2026: {f_m(pot)} M acciones = {f_p(div(pot, fin))} de las "
          f"{f_m(fin)} M en circulación (además, 1.333 M de premios con condiciones de rendimiento no cumplidas, P3 Note 13)")
    portada = (g(d, "acciones_A_portada_15oct2026", "9M2026") + g(d, "acciones_B_portada_15oct2026", "9M2026")) / 1e6
    print(f"Acciones a 15-oct-2026 (portada P3): {f_m(portada, 2)} M; variación frente a 30-sep-2026 {f_m(portada - fin, 2)} M")
    for p in ("FY2023", "FY2024", "FY2025", "9M2025", "9M2026", "TTM_Q3_2026"):
        sbct = add(g(d, "sbc_ordinaria_total", p), g(d, "sbc_adquisiciones_si", p))
        print(f"SBC {p:12s} ordinaria {f_m(g(d, 'sbc_ordinaria_total', p))} + adquisiciones {f_m(g(d, 'sbc_adquisiciones_si', p))} "
              f"= {f_m(sbct)} ({f_p(div(sbct, rev(p)))} de ingresos; {f_p(div(sbct, g(d, 'flujo_caja_operativo', p)))} del FCO)")
        rat("sbc_total", p, sbct, "M USD", "sbc ordinaria + adquisiciones")
        rat("sbc_sobre_fco", p, div(sbct, g(d, "flujo_caja_operativo", p)), "%", "sbc total / FCO")

    print("\n--- 8. Punto fase 1 (a): capex de Space 9M26 = capex de Space FY2025 ---")
    cs = lambda p: g(d, "capex_space", p)  # noqa: E731
    q4_25 = sub(cs("FY2025"), cs("9M2025"))
    q3_25 = sub(cs("9M2025"), cs("6M2025"))
    rat("capex_space_implicito", "Q4_2025", q4_25, "M USD", "FY2025 - 9M2025")
    print(f"FY2025 (P2 F-57): 1T25 {f_m(cs('Q1_2025'))} + 2T25 {f_m(cs('Q2_2025'))} + 3T25 {f_m(cs('Q3_2025'))} + 4T25 implícito "
          f"{f_m(q4_25)} = {f_m(add(cs('Q1_2025'), cs('Q2_2025'), cs('Q3_2025'), q4_25))} (publicado {f_m(cs('FY2025'))})")
    print(f"9M2026 (P3 p. 33): 1T26 {f_m(cs('Q1_2026'))} + 2T26 {f_m(cs('Q2_2026'))} + 3T26 {f_m(cs('Q3_2026'))} = "
          f"{f_m(add(cs('Q1_2026'), cs('Q2_2026'), cs('Q3_2026')))} (publicado {f_m(cs('9M2026'))})")
    print(f"9M2025 publicado {f_m(cs('9M2025'))}; 3T25 desde 9M-6M = {f_m(q3_25)} (publicado {f_m(cs('Q3_2025'))})")
    print(f"Comparación a igual periodo: capex Space 9M26/9M25 = {f_p(sub(div(cs('9M2026'), cs('9M2025')), 1))}; "
          f"TTM = {f_m(g(d, 'capex_space', 'TTM_Q3_2026'))}")
    igual = cs("9M2026") == cs("FY2025")
    print(f"¿9M26 == FY2025? {'Sí' if igual else 'No'}; ¿la serie trimestral es distinta? "
          f"{'Sí' if (cs('Q1_2026'), cs('Q2_2026'), cs('Q3_2026')) != (cs('Q1_2025'), cs('Q2_2025'), cs('Q3_2025')) else 'No'} "
          f"-> coincidencia aritmética entre acumulados, no copia de la cifra")

    print("\n--- 9. Punto fase 1 (b): Customer B y el segmento SI ---")
    B_Q1 = B["6M2026"] - B["Q2_2026"]
    for k, v in (("Q1_2026 (6M - 2T)", B_Q1), ("Q2_2026", B["Q2_2026"]), ("6M2026", B["6M2026"]),
                 ("Q3_2026", B["Q3_2026"]), ("9M2026", B["9M2026"])):
        rat("cliente_B_implicito", k, v, "M USD", "% Customer B x ingresos consolidados")
    print(f"Ingresos implícitos de Customer B: 1T26 {f_m(B_Q1)} | 2T26 {f_m(B['Q2_2026'])} | 3T26 {f_m(B['Q3_2026'])} | "
          f"6M26 {f_m(B['6M2026'])} | 9M26 {f_m(B['9M2026'])} (tolerancia de redondeo ±{f_m(tolB)})")
    print(f"Customer B 3T26 / 3 = {f_m(B['Q3_2026'] / 3)} M$/mes")
    for p in ("Q2_2026", "Q3_2026", "9M2026"):
        print(f"Customer B {p}: {f_p(div(B[p], g(d, 'ing_si', p)))} de ingresos SI; {f_p(div(B[p], g(d, 'ing_si_solutions_infra', p)))} "
              f"de SI Solutions & Infrastructure")
        rat("cliente_B_sobre_ingresos_si", p, div(B[p], g(d, "ing_si", p)), "%", "B implícito / ing_si")
    cursor = g(d, "ing_cursor", "Q3_2026")
    for p, pb in (("Q3_2026", "Q3_2025"), ("9M2026", "9M2025")):
        dsi = g(d, "ing_si", p) - g(d, "ing_si", pb)
        dtot = rev(p) - rev(pb)
        b_prev_max = min(0.10 * rev(pb), g(d, "ing_si", pb))
        print(f"{p} vs {pb}: aumento ingresos SI {f_m(dsi)}; aumento consolidado {f_m(dtot)}; Customer B {f_m(B[p])}; "
              f"Cursor {f_m(cursor)}")
        print(f"   Customer B en {pb} < 10 % de ingresos (no revelado): entre 0 y {f_m(b_prev_max)}")
        for etiqueta, bprev in (("si B en el periodo previo = 0", 0.0), ("si B previo = máximo posible", b_prev_max)):
            sb = rat("peso_cliente_B_en_crecimiento_si", f"{p} ({etiqueta})", div(B[p] - bprev, dsi), "%",
                     "(B - B previo)/aumento ingresos SI")
            st = rat("peso_cliente_B_en_crecimiento_total", f"{p} ({etiqueta})", div(B[p] - bprev, dtot), "%",
                     "(B - B previo)/aumento ingresos consolidados")
            print(f"   {etiqueta}: B explica {f_p(sb)} del aumento de SI y {f_p(st)} del aumento consolidado")
        resto = g(d, "ing_si", p) - B[p] - cursor
        resto_prev = g(d, "ing_si", pb)
        rat("ing_si_sin_B_ni_cursor", p, resto, "M USD", "ing_si - B implícito - Cursor")
        print(f"   SI sin Customer B ni Cursor: {f_m(resto)} frente a {f_m(resto_prev)} en {pb} (SI total del periodo previo; "
              f"cota superior si B previo = 0) -> variación {f_p(sub(div(resto, resto_prev), 1))}; con B previo máximo "
              f"la base sería {f_m(resto_prev - b_prev_max)} -> {f_p(sub(div(resto, resto_prev - b_prev_max), 1))}")
        tot_sin = rev(p) - B[p]
        print(f"   Ingresos consolidados sin Customer B: {f_m(tot_sin)} -> crecimiento {f_p(sub(div(tot_sin, rev(pb)), 1))} "
              f"(publicado con B: {f_p(sub(div(rev(p), rev(pb)), 1))})")
        rat("crec_ingresos_sin_cliente_B", p, sub(div(tot_sin, rev(pb)), 1), "%", "(ingresos - B)/ingresos previos - 1 (B previo=0)")
    # margen incremental de SI 1T26 -> 3T26
    d_rev = g(d, "ing_si", "Q3_2026") - g(d, "ing_si", "Q1_2026")
    d_ebitda = g(d, "ebitda_aj_si", "Q3_2026") - g(d, "ebitda_aj_si", "Q1_2026")
    d_op = g(d, "opinc_si", "Q3_2026") - g(d, "opinc_si", "Q1_2026")
    d_cor = g(d, "coste_ingresos_si", "Q3_2026") - g(d, "coste_ingresos_si", "Q1_2026")
    d_b = B["Q3_2026"] - B_Q1
    m_inc = rat("margen_incremental_ebitda_aj_si", "Q1_2026->Q3_2026", div(d_ebitda, d_rev), "%", "ΔEBITDA aj SI/Δingresos SI")
    rat("margen_incremental_operativo_si", "Q1_2026->Q3_2026", div(d_op, d_rev), "%", "Δopinc SI/Δingresos SI")
    rat("margen_incremental_bruto_si", "Q1_2026->Q3_2026", div(d_rev - d_cor, d_rev), "%", "(Δingresos - Δcoste)/Δingresos SI")
    print(f"SI 1T26 -> 3T26: Δingresos {f_m(d_rev)} (de ellos Customer B {f_m(d_b)} = {f_p(div(d_b, d_rev))}, Cursor {f_m(cursor)}); "
          f"ΔEBITDA aj {f_m(d_ebitda)} (margen incremental {f_p(m_inc)}); Δresultado operativo {f_m(d_op)} "
          f"({f_p(div(d_op, d_rev))}); Δcoste de ingresos {f_m(d_cor)} (margen bruto incremental {f_p(div(d_rev - d_cor, d_rev))})")
    print("Escenarios (SUPUESTOS, no datos): margen incremental que se perdería si desapareciera el ingreso de Customer B del 3T26")
    print(f"{'margen supuesto':>16s} | {'SI op. sin B':>12s} | {'SI EBITDA aj sin B':>18s} | {'grupo op. sin B':>15s} | "
          f"{'grupo EBITDA aj sin B':>21s} | {'margen EBITDA aj grupo':>22s}")
    for etiqueta, mg in (("100 %", 1.0), (f"{f_p(m_inc)} (obs.)", m_inc), ("75 %", 0.75), ("50 %", 0.50)):
        perd = B["Q3_2026"] * mg
        si_op = g(d, "opinc_si", "Q3_2026") - perd
        si_eb = g(d, "ebitda_aj_si", "Q3_2026") - perd
        gr_op = g(d, "beneficio_operativo", "Q3_2026") - perd
        gr_eb = g(d, "ebitda_ajustado", "Q3_2026") - perd
        mgr = div(gr_eb, rev("Q3_2026") - B["Q3_2026"])
        rat("escenario_sin_B_si_operativo", f"Q3_2026 margen {etiqueta}", si_op, "M USD", "opinc_si - B x margen supuesto")
        rat("escenario_sin_B_si_ebitda_aj", f"Q3_2026 margen {etiqueta}", si_eb, "M USD", "ebitda_aj_si - B x margen supuesto")
        rat("escenario_sin_B_grupo_ebitda_aj", f"Q3_2026 margen {etiqueta}", gr_eb, "M USD", "ebitda_ajustado - B x margen")
        print(f"{etiqueta:>16s} | {f_m(si_op):>12s} | {f_m(si_eb):>18s} | {f_m(gr_op):>15s} | {f_m(gr_eb):>21s} | {f_p(mgr):>22s}")
    print(f"Referencia 3T26 publicado: SI operativo {f_m(g(d, 'opinc_si', 'Q3_2026'))}, SI EBITDA aj {f_m(g(d, 'ebitda_aj_si', 'Q3_2026'))}, "
          f"grupo operativo {f_m(g(d, 'beneficio_operativo', 'Q3_2026'))}, grupo EBITDA aj {f_m(g(d, 'ebitda_ajustado', 'Q3_2026'))} "
          f"({f_p(div(g(d, 'ebitda_ajustado', 'Q3_2026'), rev('Q3_2026')))})")
    print(f"Peso de SI en el EBITDA aj. del grupo 3T26: {f_p(div(g(d, 'ebitda_aj_si', 'Q3_2026'), g(d, 'ebitda_ajustado', 'Q3_2026')))}; "
          f"en 1T26: {f_m(g(d, 'ebitda_aj_si', 'Q1_2026'))} de {f_m(g(d, 'ebitda_ajustado', 'Q1_2026'))}")
    print(f"Customer A implícito 3T26 = {f_m(g(d, 'cliente_A_pct', 'Q3_2026') / 100 * rev('Q3_2026'))}; FY2025 = "
          f"{f_m(g(d, 'cliente_A_pct', 'FY2025') / 100 * rev('FY2025'))}; A + B 3T26 = "
          f"{f_m(g(d, 'cliente_A_pct', 'Q3_2026') + g(d, 'cliente_B_pct', 'Q3_2026'), 1)} % de ingresos")

    print("\n--- 10. Comparabilidad por la fusión con xAI: 'SpaceX heredada' (Space + Connectivity) vs AI/SI ---")
    for p in ("FY2023", "FY2024", "FY2025", "9M2025", "9M2026", "TTM_Q3_2026", "Q3_2025", "Q3_2026"):
        r_h = add(g(d, "ing_space", p), g(d, "ing_connectivity", p))
        o_h = add(g(d, "opinc_space", p), g(d, "opinc_connectivity", p))
        e_h = add(g(d, "ebitda_aj_space", p), g(d, "ebitda_aj_connectivity", p))
        c_h = add(g(d, "capex_space", p), g(d, "capex_connectivity", p))
        rat("ing_heredada", p, r_h, "M USD", "ing_space + ing_connectivity")
        rat("margen_operativo_heredada", p, div(o_h, r_h), "%", "(opinc space + connectivity)/(ing space + connectivity)")
        rat("ebitda_aj_menos_capex_heredada", p, sub(e_h, c_h), "M USD", "EBITDA aj - capex (space + connectivity)")
        print(f"{p:12s} heredada: ingresos {f_m(r_h):>7s} | op {f_m(o_h):>6s} ({f_p(div(o_h, r_h))}) | EBITDA aj {f_m(e_h):>6s} "
              f"({f_p(div(e_h, r_h))}) | capex {f_m(c_h):>6s} | EBITDA aj - capex {f_m(sub(e_h, c_h)):>7s} || AI/SI: ingresos "
              f"{f_m(g(d, 'ing_si', p)):>6s} | op {f_m(g(d, 'opinc_si', p)):>6s} | EBITDA aj {f_m(g(d, 'ebitda_aj_si', p)):>6s} | "
              f"capex {f_m(g(d, 'capex_si', p)):>6s} | EBITDA aj - capex {f_m(sub(g(d, 'ebitda_aj_si', p), g(d, 'capex_si', p))):>7s}")
    for a, b in (("FY2024", "FY2023"), ("FY2025", "FY2024"), ("9M2026", "9M2025")):
        rh_a = add(g(d, "ing_space", a), g(d, "ing_connectivity", a))
        rh_b = add(g(d, "ing_space", b), g(d, "ing_connectivity", b))
        print(f"Crecimiento {a}/{b}: heredada {f_p(sub(div(rh_a, rh_b), 1))} | AI/SI {f_p(sub(div(g(d, 'ing_si', a), g(d, 'ing_si', b)), 1))} "
              f"| grupo {f_p(sub(div(rev(a), rev(b)), 1))}")

    print("\n--- 11. Trimestres implícitos 4T2025 (FY2025 - 9M2025) ---")
    for m in ("ingresos_totales", "ing_space", "ing_connectivity", "ing_si", "beneficio_operativo", "ebitda_ajustado",
              "beneficio_neto", "flujo_caja_operativo", "capex"):
        v = sub(g(d, m, "FY2025"), g(d, m, "9M2025"))
        rat(m + "_implicito", "Q4_2025", v, "M USD", "FY2025 - 9M2025")
        print(f"{m:22s} 4T25 {f_m(v)}")

    # ============================================================ salida
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["indicador", "periodo", "valor", "unidad", "formula"])
        w.writeheader()
        w.writerows(ratios)
    with open(CHK, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["control", "calculado", "referencia", "fuente_referencia", "diferencia",
                                          "tolerancia", "resultado"])
        w.writeheader()
        w.writerows(checks)
    print("\n--- Controles ---")
    for c in checks:
        if c["resultado"] == "OK" and c["diferencia"]:
            print(f"  REDONDEO (dentro de tolerancia {c['tolerancia']}): {c['control']} (calc {f_m(c['calculado'])} vs ref "
                  f"{f_m(c['referencia'])}, dif {f_m(c['diferencia'])})")
        if c["resultado"] != "OK":
            print(f"  {c['resultado']}: {c['control']} (calc {c['calculado']} vs ref {c['referencia']})")
    print(f"Ratios escritos: {len(ratios)} -> {OUT}")
    print(f"CONTROLES: {len(checks)} | OK {n_ok} | DISCREPANCIA {n_bad} | SIN DATO {n_sd} -> {CHK}")
    if n_bad or n_sd:
        sys.exit(1)


if __name__ == "__main__":
    main()
