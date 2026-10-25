"""Fase 1 (Negocio) — SpaceX (SPCX): pesos de segmentos, crecimientos y cálculos auxiliares.

Todas las cifras de entrada se copian literalmente de fuentes primarias de SEC EDGAR
(ver empresas/spacex/fuentes/fuentes.md). Los IDs de fuente van en el comentario de cada bloque.
Importes en millones de USD salvo que se indique lo contrario.

Uso:  python empresas/spacex/scripts/fase1_segmentos.py
Solo imprime; no escribe ficheros.
"""


def pct(a, b):
    return 100.0 * a / b


def var(a, b):
    return 100.0 * (a / b - 1.0)


def linea(txt):
    print(txt)


# ---------------------------------------------------------------------------
# P2 = 424B4 (Prospectus 11-jun-2026), Note 3 de los estados anuales auditados (p. F-23):
# "Revenue disaggregated by type and segment", FY2025 / FY2024 / FY2023.
FY = {
    2025: {"Launch Services": 2576, "Launch & Development": 1510,
           "Consumer": 7208, "Enterprise & Government": 4179,
           "Advertising": 1844, "AI Solutions & Infrastructure": 1357},
    2024: {"Launch Services": 2584, "Launch & Development": 1212,
           "Consumer": 4830, "Enterprise & Government": 2769,
           "Advertising": 1728, "AI Solutions & Infrastructure": 892},
    2023: {"Launch Services": 1964, "Launch & Development": 1593,
           "Consumer": 2817, "Enterprise & Government": 1052,
           "Advertising": 2323, "AI Solutions & Infrastructure": 638},
}
SEG_FY = {2025: {"Space": 4086, "Connectivity": 11387, "AI": 3201, "Total": 18674},
          2024: {"Space": 3796, "Connectivity": 7599, "AI": 2620, "Total": 14015},
          2023: {"Space": 3557, "Connectivity": 3869, "AI": 2961, "Total": 10387}}
MAPA = {"Space": ["Launch Services", "Launch & Development"],
        "Connectivity": ["Consumer", "Enterprise & Government"],
        "AI": ["Advertising", "AI Solutions & Infrastructure"]}

# P2, Prospectus Summary (p. 4) y tabla "Summary Consolidated Financial and Other Data" (p. 26-27):
# resultado operativo y Segment Adjusted EBITDA FY2025 / FY2024.
OPINC_FY = {2025: {"Space": -657, "Connectivity": 4423, "AI": -6355, "Total": -2589},
            2024: {"Space": 21, "Connectivity": 2006, "AI": -1561}}
ADJ_FY = {2025: {"Space": 653, "Connectivity": 7168, "AI": -1237, "Total": 6584},
          2024: {"Space": 1154, "Connectivity": 3849, "AI": 347}}

# ---------------------------------------------------------------------------
# P3 = 10-Q 3T 2026 (acc. 0001628280-26-066880), Note 3 y Note 18; P5 = 8-K Ex. 99.1 (20-oct-2026).
Q3_26 = {"Launch Services": 1130, "Launch & Development": 637, "Consumer": 3121,
         "Enterprise & Government": 2127, "Advertising": 538, "SI Solutions & Infrastructure": 7022}
Q3_25 = {"Launch Services": 1000, "Launch & Development": 666, "Consumer": 1986,
         "Enterprise & Government": 1111, "Advertising": 454, "SI Solutions & Infrastructure": 359}
M9_26 = {"Launch Services": 2108, "Launch & Development": 1240, "Consumer": 7754,
         "Enterprise & Government": 5042, "Advertising": 1248, "SI Solutions & Infrastructure": 9691}
M9_25 = {"Launch Services": 2056, "Launch & Development": 1221, "Consumer": 5198,
         "Enterprise & Government": 2961, "Advertising": 1323, "SI Solutions & Infrastructure": 955}
SEG_Q = {"Q3_26": {"Space": 1767, "Connectivity": 5248, "SI": 7560, "Total": 14575},
         "Q3_25": {"Space": 1666, "Connectivity": 3097, "SI": 813, "Total": 5576},
         "9M_26": {"Space": 3348, "Connectivity": 12796, "SI": 10939, "Total": 27083},
         "9M_25": {"Space": 3277, "Connectivity": 8159, "SI": 2278, "Total": 13714}}
OPINC_Q = {"Q3_26": {"Space": -7, "Connectivity": 2367, "SI": 431, "Total": 2791},
           "9M_26": {"Space": -1211, "Connectivity": 5211, "SI": -3295, "Total": 705}}
ADJ_Q = {"Q3_26": {"Space": 357, "Connectivity": 3499, "SI": 4953, "Total": 8809},
         "9M_26": {"Space": -199, "Connectivity": 8183, "SI": 5490, "Total": 13474}}
CAPEX = {"Q3_26": {"Space": 1606, "Connectivity": 1543, "SI": 16444, "Total": 19593},
         "9M_26": {"Space": 3832, "Connectivity": 4242, "SI": 39995, "Total": 48069}}
CURSOR_REV_Q3 = 608          # P3 MD&A / P5: ingresos de Cursor desde el 14-ago-2026
MAPA_Q = {"Space": ["Launch Services", "Launch & Development"],
          "Connectivity": ["Consumer", "Enterprise & Government"],
          "SI": ["Advertising", "SI Solutions & Infrastructure"]}

# Concentración de clientes: P2 Note 3 (FY) y P3 Note 3 (3T y 9M 2026), % de ingresos consolidados.
CUST = {"FY2025 Customer A": (20.9, 18674), "FY2024 Customer A": (24.2, 14015),
        "Q3_26 Customer A": (16.6, 14575), "Q3_26 Customer B": (34.5, 14575),
        "9M_26 Customer A": (17.3, 27083), "9M_26 Customer B": (24.2, 27083)}
ANTHROPIC_MENSUAL = 1250     # P2, Business / Prospectus Summary: "$1.25 billion per month through May 2029"

# Métricas operativas (P2 Summary p. 26-27; P3 MD&A Key Business Metrics).
SUBS = {"dic-2024": 4.4, "dic-2025": 8.9, "sep-2025": 7.2, "sep-2026": 13.6}   # millones
ARPU = {"FY2024": 91, "FY2025": 81, "Q3_25": 83, "Q3_26": 69}                # $/mes

# ---------------------------------------------------------------------------
# Capital: P2 (portada, "Security Ownership", "The Offering"); P4 = 8-K 15-jun-2026; P3 portada.
IPO_ACC = 638_888_888          # P4 (incluye green shoe 83.333.333)
IPO_PRECIO = 135.00
IPO_NETO = 85675               # P3 Note 1
A_POST = 7_488_063_555         # P2 Security Ownership: Clase A tras la oferta (sin green shoe), base 1-may-2026
B_POST = 5_602_790_410         # P2 idem Clase B
GREENSHOE = 83_333_333
MUSK_A = 849_494_440           # P2 tabla de beneficiarios
MUSK_B = 5_569_053_075         # P2 (incluye 1.302.072.285 restringidas y 350.000.000 opciones ejercitables)
MUSK_OPC_B = 350_000_000
A_OCT = 8_246_541_218          # P3 portada, a 15-oct-2026
B_OCT = 5_334_522_491

# P7 = Schedule 13G de Elon Musk (acc. 0001104659-26-095936, evento 30-jun-2026).
MUSK13G_TOTAL = 6_418_547_515
MUSK13G_B_TRUSTS = 3_916_980_790   # Clase B en trusts
MUSK13G_B_RESTR = 1_302_072_285    # Clase B restringida (votable, no consolidada)

# P3 balance a 30-sep-2026 y MD&A (Debt Agreements); Note 9/17 (Valor, failed sale-leaseback).
CAJA = 51294
VALORES = 38561
DEUDA_PRINCIPAL = 38006
DEUDA_CONT = {"corriente": 2698, "no corriente": 36146}
VALOR_DEUDA = {"corriente": 2181, "no corriente": 10716}
BACKLOG = 62959
BACKLOG_DIC25 = 28377              # P2 Note 3

# Opcionalidad (cálculo ilustrativo, ver docs/01 §5).
MULT_ILUSTR = 30


def main():
    linea("=== 1. FY2025 / FY2024 / FY2023 por segmento (P2, Note 3) ===")
    for año in (2025, 2024, 2023):
        tot = sum(FY[año].values())
        assert tot == SEG_FY[año]["Total"], (año, tot)
        for seg, subl in MAPA.items():
            s = sum(FY[año][x] for x in subl)
            assert s == SEG_FY[año][seg], (año, seg, s)
    for seg in ("Space", "Connectivity", "AI"):
        r25, r24, r23 = SEG_FY[2025][seg], SEG_FY[2024][seg], SEG_FY[2023][seg]
        linea(f"{seg:14s} FY25 {r25:6d}  peso {pct(r25, 18674):5.1f}%  var25/24 {var(r25, r24):+6.1f}%  "
              f"var24/23 {var(r24, r23):+6.1f}%  margen op FY25 {pct(OPINC_FY[2025][seg], r25):+7.1f}%  "
              f"margen EBITDA aj. FY25 {pct(ADJ_FY[2025][seg], r25):+6.1f}%")
    linea(f"{'Total':14s} FY25 {18674:6d}  var25/24 {var(18674, 14015):+6.1f}%  var24/23 {var(14015, 10387):+6.1f}%  "
          f"margen op {pct(-2589, 18674):+6.1f}%  margen EBITDA aj. {pct(6584, 18674):+6.1f}%")
    for k in FY[2025]:
        linea(f"  · {k:30s} FY25 {FY[2025][k]:6d}  peso total {pct(FY[2025][k], 18674):5.1f}%  "
              f"var25/24 {var(FY[2025][k], FY[2024][k]):+6.1f}%")

    linea("\n=== 2. 3T 2026 y 9M 2026 por segmento (P3, Note 3 y Note 18) ===")
    for per, d, base in (("Q3_26", Q3_26, "Q3_25"), ("9M_26", M9_26, "9M_25")):
        prev = Q3_25 if per == "Q3_26" else M9_25
        tot = SEG_Q[per]["Total"]
        assert sum(d.values()) == tot, per
        assert sum(prev.values()) == SEG_Q[base]["Total"], base
        for seg, subl in MAPA_Q.items():
            assert sum(d[x] for x in subl) == SEG_Q[per][seg], (per, seg)
            r, rp = SEG_Q[per][seg], SEG_Q[base][seg]
            linea(f"{per} {seg:13s} {r:6d}  peso {pct(r, tot):5.1f}%  var a/a {var(r, rp):+7.1f}%  "
                  f"margen op {pct(OPINC_Q[per][seg], r):+7.1f}%  margen EBITDA aj. {pct(ADJ_Q[per][seg], r):+6.1f}%  "
                  f"capex/ingresos {pct(CAPEX[per][seg], r):6.1f}%")
        linea(f"{per} Total        {tot:6d}  var a/a {var(tot, SEG_Q[base]['Total']):+7.1f}%  "
              f"margen op {pct(OPINC_Q[per]['Total'], tot):+6.1f}%  capex/ingresos {pct(CAPEX[per]['Total'], tot):6.1f}%  "
              f"peso capex SI {pct(CAPEX[per]['SI'], CAPEX[per]['Total']):5.1f}%")
        for k in d:
            linea(f"  · {k:30s} {d[k]:6d}  peso total {pct(d[k], tot):5.1f}%  var a/a {var(d[k], prev[k]):+7.1f}%")

    linea("\n=== 3. Concentración de clientes (importes implícitos, cálculo propio) ===")
    for k, (p, rev) in CUST.items():
        linea(f"{k:20s} {p:5.1f}% de {rev:6d} = {p / 100 * rev:8.0f} M$")
    b_q3 = 34.5 / 100 * 14575
    linea(f"Customer B 3T26 / 3 meses = {b_q3 / 3:7.0f} M$/mes (contrato Anthropic en P2: {ANTHROPIC_MENSUAL} M$/mes)")
    linea(f"Customer B 3T26 como % de ingresos SI 3T26 = {pct(b_q3, 7560):5.1f}%")
    linea(f"SI 3T26 sin Customer B ni Cursor = {7560 - b_q3 - CURSOR_REV_Q3:7.0f} M$")
    linea(f"Customer A + B 3T26 = {16.6 + 34.5:5.1f}% de ingresos consolidados")

    linea("\n=== 4. Métricas Starlink ===")
    linea(f"Suscriptores consumo sep-26 vs sep-25: {var(SUBS['sep-2026'], SUBS['sep-2025']):+6.1f}%")
    linea(f"Suscriptores dic-25 vs dic-24: {var(SUBS['dic-2025'], SUBS['dic-2024']):+6.1f}%")
    linea(f"ARPU 3T26 vs 3T25: {var(ARPU['Q3_26'], ARPU['Q3_25']):+6.1f}%  ARPU FY25 vs FY24: {var(ARPU['FY2025'], ARPU['FY2024']):+6.1f}%")

    linea("\n=== 5. OPV y estructura de capital ===")
    bruto = IPO_ACC * IPO_PRECIO / 1e6
    linea(f"OPV bruta {bruto:,.0f} M$; neta (P3) {IPO_NETO:,} M$; costes implícitos {bruto - IPO_NETO:,.0f} M$")
    musk_eco = MUSK_A + MUSK_B
    den_ben = A_POST + B_POST + MUSK_OPC_B
    linea(f"Musk % económico post-OPV (base SEC, con 350 M opciones): {pct(musk_eco, den_ben):5.1f}%")
    linea(f"Musk % económico post-OPV (sin opciones en num. ni den.): {pct(musk_eco - MUSK_OPC_B, A_POST + B_POST):5.1f}%")
    votos_musk = MUSK_A + 10 * MUSK_B
    votos_tot = A_POST + 10 * (B_POST + MUSK_OPC_B)
    linea(f"Musk % voto post-OPV (base SEC, con opciones): {pct(votos_musk, votos_tot):5.1f}%  (tabla P2: 84,4 %)")
    votos_oct = A_OCT + 10 * B_OCT
    linea(f"Acciones a 15-oct-2026: A {A_OCT:,} + B {B_OCT:,} = {A_OCT + B_OCT:,}")
    linea(f"Peso de la Clase B en los votos a 15-oct-2026: {pct(10 * B_OCT, votos_oct):5.1f}%; "
          f"en el capital: {pct(B_OCT, A_OCT + B_OCT):5.1f}%")
    acc_ipo = A_POST + GREENSHOE + B_POST
    cap_ipo = acc_ipo * IPO_PRECIO / 1e6
    linea(f"Acciones post-OPV con green shoe (base 1-may-2026): {acc_ipo:,}; capitalización al precio de OPV: {cap_ipo:,.0f} M$")

    linea("\n=== 6. Opcionalidad: cálculo ilustrativo (no procede de ninguna fuente) ===")
    linea(f"Capitalización OPV / ingresos FY25 = {cap_ipo / 18674:5.1f}x;  / (ingresos 3T26 x4) = {cap_ipo / (14575 * 4):5.1f}x")
    base_fy = (ADJ_FY[2025]["Space"] + ADJ_FY[2025]["Connectivity"]) * MULT_ILUSTR
    linea(f"{MULT_ILUSTR}x EBITDA aj. FY25 de Space+Connectivity = {base_fy:,.0f} M$ = {pct(base_fy, cap_ipo):4.1f}% de la cap. OPV")
    base_cx = ADJ_FY[2025]["Connectivity"] * MULT_ILUSTR
    linea(f"{MULT_ILUSTR}x EBITDA aj. FY25 de Connectivity = {base_cx:,.0f} M$ = {pct(base_cx, cap_ipo):4.1f}% de la cap. OPV")
    run = ADJ_Q["Q3_26"]["Total"] * 4 * MULT_ILUSTR
    linea(f"{MULT_ILUSTR}x (EBITDA aj. 3T26 x4) = {run:,.0f} M$ = {pct(run, cap_ipo):4.1f}% de la cap. OPV")
    run_sin_b = (ADJ_Q["Q3_26"]["Total"] - b_q3) * 4 * MULT_ILUSTR
    linea(f"Idem restando todo el ingreso del Customer B como si fuera EBITDA: {run_sin_b:,.0f} M$ = "
          f"{pct(run_sin_b, cap_ipo):4.1f}% de la cap. OPV")

    linea("\n=== 7. Control de Musk tras la OPV (13G) y estimación a 15-oct-2026 ===")
    musk_b_emit = MUSK13G_B_TRUSTS + MUSK13G_B_RESTR
    musk_a_13g = MUSK13G_TOTAL - musk_b_emit - MUSK_OPC_B
    linea(f"13G: Clase B emitida de Musk {musk_b_emit:,}; Clase A {musk_a_13g:,}; opciones B {MUSK_OPC_B:,}")
    linea(f"Clase B de Musk / Clase B total a 15-oct-2026: {pct(musk_b_emit, B_OCT):5.1f}%")
    v_musk = musk_a_13g + 10 * musk_b_emit
    linea(f"Voto estimado de Musk a 15-oct-2026 (supone tenencias del 13G sin cambios, sin opciones): "
          f"{pct(v_musk, A_OCT + 10 * B_OCT):5.1f}%")
    linea(f"% económico estimado a 15-oct-2026 (mismo supuesto): {pct(musk_a_13g + musk_b_emit, A_OCT + B_OCT):5.1f}%")

    linea("\n=== 8. Balance 30-sep-2026 (P3) ===")
    linea(f"Caja + valores negociables = {CAJA + VALORES:,} M$; deuda principal {DEUDA_PRINCIPAL:,} M$")
    linea(f"Deuda y arrendamientos contables = {sum(DEUDA_CONT.values()):,} M$; de ello Valor (parte vinculada) "
          f"{sum(VALOR_DEUDA.values()):,} M$ = {pct(sum(VALOR_DEUDA.values()), sum(DEUDA_CONT.values())):4.1f}%")
    linea(f"Backlog sep-26 vs dic-25: {var(BACKLOG, BACKLOG_DIC25):+6.1f}%")


if __name__ == "__main__":
    main()
