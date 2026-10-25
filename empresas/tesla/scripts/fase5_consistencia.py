"""Fase 5 (Reality Checker) - controles de consistencia entre fases y sobre las críticas de Fase 4.

1. Re-ejecuta fase2/fase3/fase4 en una copia temporal (no toca data/ del proyecto) y compara
   las cifras impresas con las citadas en los documentos.
2. Cifras citadas de forma distinta en distintos documentos.
3. Supuestos de Fase 3 frente a datos de Fase 2.
4. Re-cálculo de las críticas de Fase 4 (W1-W11, §4.1-4.2) que admiten comprobación numérica.
Uso: python3 scripts/fase5_consistencia.py

REGISTRO DE CAMBIOS v2 (2026-10-25, segunda verificación). Solo cambian VALORES ESPERADOS (lo que dicen los
documentos v2) y textos descriptivos; no se toca ningún modelo (fase2/3/4 se ejecutan tal cual, en copia temporal).
La versión v1 de este script está en versiones/v1/scripts/fase5_consistencia.py.
  §1 KEY (cifra esperada, v1 -> v2):
    WACC0               0.1160  -> 0.1160   (sin cambio)
    WACC_T              0.0979  -> 0.0979   (sin cambio)
    VPA bajista         10.4    -> 10.4     (sin cambio al decimal; 10,36 -> 10,40)
    VPA base            24.5    -> 24.6
    VPA alcista         54.9    -> 55.8
    EV base             61040   -> 61353
    TACC margen 20 %    36.1    -> 36.1     (sin cambio)
    TACC margen 30 %    27.8    -> 27.8     (sin cambio)
    Precio big tech     407.4   -> 407.4    (sin cambio)
    EBIT_10 central     147561  -> 147527
    Recorte 50 %        198     -> 198      (sin cambio)
    Margen 3T26 + I+D   6.6     -> 6.6      (sin cambio)
    + nuevas expectativas v2: VPA totalmente diluidos 10,36/24,52/55,55; D&A TTM 6.704; acciones FD 3.967,3;
      capex año 1 15.884; W9 +1,2/+4,6; 72 controles fase2 (67 OK + 5 DISCREPANCIA; v1: 55 = 50 + 5)
  §2 DIFS: estado v2 de cada discrepancia entre documentos (v1: 10 discrepancias abiertas).
  §3 reconstrucción independiente del año 1 (supuestos esperados de 03, v1 -> v2):
    D&A TTM 1.852 x 4 = 7.408 -> 6.704 (02 v2); energía año 1 +12 % -> +8 %; margen objetivo 0,0893 (sobre
    ingresos totales) -> media FY21-24 sobre ingresos sin créditos (9,15 %); margen de partida 2,21 % -> 2,23 %;
    FCFF año 1 esperado -5.039 -> -5.700
  §4 W9: puntos de la tabla 4.1 usados para interpolar {10,6 %: 28,49 ; 11,6 %: 24,52} -> {28,55 ; 24,60};
    W2: texto "SIN VERIFICAR en ambos sentidos" -> "doble cómputo real de ~286 M, resuelto en 03 v2" (02 §5.1).
"""
import csv
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def h(t):
    print("\n" + "=" * 90 + "\n" + t + "\n" + "=" * 90)


# ------------------------------------------------------------------------------------------
# 1. Re-ejecución de los scripts en copia temporal
# ------------------------------------------------------------------------------------------
h("1. Re-ejecución de scripts (copia temporal)")
tmp = tempfile.mkdtemp(prefix="fase5_")
for d in ("data", "scripts"):
    shutil.copytree(os.path.join(BASE, d), os.path.join(tmp, d))
OUT = {}
for s in ("fase2_ratios.py", "fase3_dcf.py", "fase4_opcionalidad.py"):
    p = subprocess.run([sys.executable, os.path.join(tmp, "scripts", s)], capture_output=True, text=True)
    OUT[s] = p.stdout
    print(f"{s}: rc={p.returncode} | {len(p.stdout.splitlines())} líneas")


def same_file(rel):
    with open(os.path.join(BASE, rel), "rb") as a, open(os.path.join(tmp, rel), "rb") as b:
        return a.read() == b.read()


print("ratios.csv idéntico al del proyecto:", same_file("data/ratios.csv"))
print("checks.csv idéntico al del proyecto:", same_file("data/checks.csv"))
n_ok = OUT["fase2_ratios.py"].count("[OK]")
n_disc = OUT["fase2_ratios.py"].count("[DISCREPANCIA]")
print(f"Controles fase2: {n_ok} OK + {n_disc} DISCREPANCIA (02 v2 §1.3 dice 67 + 5 = 72; v1: 50 + 5)")
print(f"  [{'OK' if (n_ok, n_disc) == (67, 5) else 'MISMATCH'}] recuento de controles fase2")

# Cifras clave: (descripción, regex sobre la salida, valor citado en docs v2, tolerancia). v1 -> v2 en el docstring.
o3, o4 = OUT["fase3_dcf.py"], OUT["fase4_opcionalidad.py"]
KEY = [
    ("WACC0 (03 §1.1: 11,60 %)", o3, r"WACC0 ([\d.]+) \|", 0.1160, 1e-4),
    ("WACC_T (03: 9,79 %)", o3, r"WACC_T ([\d.]+)", 0.0979, 1e-4),
    ("VPA bajista (03 v2: 10,4; v1 10,4)", o3, r"bajista : .*?VPA ([\d.]+)", 10.4, 0.05),
    ("VPA base (03 v2: 24,6; v1 24,5)", o3, r"base    : .*?VPA ([\d.]+)", 24.6, 0.05),
    ("VPA alcista (03 v2: 55,8; v1 54,9)", o3, r"alcista : .*?VPA ([\d.]+)", 55.8, 0.05),
    ("EV base (03 v2: 61.353; v1 61.040)", o3, r"base    : .*?\| EV ([\d,]+)", 61353, 1),
    ("TACC margen 20 % (03: 36,1 %)", o3, r"Margen 20%: TACC necesaria ([\d.]+)%", 36.1, 0.05),
    ("TACC margen 30 % (03: 27,8 %)", o3, r"Margen 30%: TACC necesaria ([\d.]+)%", 27.8, 0.05),
    ("Precio implícito big tech EV/Ventas (03: 407,4)", o3, r"Mediana Big tech.*?'EV/Ventas': ([\d.]+)", 407.4, 0.05),
    ("EBIT_10 central (04 v2.1: 147.527; v1 147.561)", o4, r"referencia central .*?: ([\d,]+) M\$", 147527, 1),
    ("Recorte 50 % opcionalidad (04: 198 $)", o4, r"recortara a la mitad .*?: (\d+) \$", 198, 0.5),
    ("Margen 3T26 + I+D incremental (04: 6,6 %)", o4, r"sumando el incremento de I\+D: ([\d.]+)%", 6.6, 0.05),
    # nuevas expectativas v2
    ("VPA bajista totalmente diluido (03 v2: 10,36)", o3, r"bajista : .*?VPA totalmente diluido ([\d.]+)", 10.36, 0.005),
    ("VPA base totalmente diluido (03 v2: 24,52)", o3, r"base    : .*?VPA totalmente diluido ([\d.]+)", 24.52, 0.005),
    ("VPA alcista totalmente diluido (03 v2: 55,55)", o3, r"alcista : .*?VPA totalmente diluido ([\d.]+)", 55.55, 0.005),
    ("D&A TTM (02 v2 / 03 v2: 6.704)", o3, r"D&A TTM ([\d,]+) \(", 6704, 0.5),
    ("Acciones totalmente diluidas (03 v2: 3.967,3)", o3, r"totalmente diluidas ([\d,.]+) \(contraste", 3967.3, 0.05),
    ("Capex bruto año 1 (03/04 v2: 15.884)", o3, r"Capex bruto implícito año 1 \(base\) = .*?= ([\d,]+) M\$", 15884, 0.5),
    ("W9 solo años 1-5 (03/04 v2: +1,2 $)", o3, r"años 1-5 solo [\d.]+ \$ \(\+([\d.]+)\)", 1.2, 0.05),
    ("W9 desplazando terminal (03/04 v2: +4,6 $)", o3, r"terminal a [\d.]+%: [\d.]+ \$ \(\+([\d.]+)\)", 4.6, 0.05),
]
for desc, txt, rx, cited, tol in KEY:
    m = re.search(rx, txt)
    v = float(m.group(1).replace(",", "")) if m else None
    if cited is None:
        print(f"  [INFO] {desc}: {v}")
        continue
    st = "OK" if v is not None and abs(v - cited) <= tol else "MISMATCH"
    print(f"  [{st}] {desc}: script={v}")

# ------------------------------------------------------------------------------------------
# 2. Cifras citadas de forma distinta en distintos documentos
# ------------------------------------------------------------------------------------------
h("2. Misma cifra, valores distintos según el documento (estado v2; detalle en scripts/fase5v2_coherencia.py)")
DIFS = [  # (cifra, estado v1, estado v2 esperado, valoración)
    ("Caja + inversiones 30-sep-26", "01: 45.400", "01/02/03/04: 45.447", "corregido en 01 v2"),
    ("Deuda", "01 §2: 8.180 junto a caja 30-sep-26", "01/02/03/04: 9.523 (30-sep-26); 8.180 solo como nota de principal a 31-dic-25", "corregido en 01 v2"),
    ("SBC 3T26", "01: 1.170 (S2)", "01/02/04: 1.165 (P4); 1.170 solo como contraste S2", "corregido"),
    ("Capex 9M26", "01: 13.010 (S2)", "01/02/03/04: 13.014 (P2)", "corregido"),
    ("I+D 3T26", "01: 2.760 (S2)", "01/02/03/04: 2.761 (P4)", "corregido"),
    ("Beneficio neto 3T26", "01: 787 'GAAP'", "01: 787 atribuible / 804 total", "corregido"),
    ("PER TSLA", "01 ~327x | 02 390x | 03 410x | 04 457x", "01 ~327x DESFASADO | 02 390x (D5, 354,72 $) | 03/04 410x estándar; 457x alternativa", "sigue sin definición única fuera de 03/04; aceptable con etiquetas"),
    ("Capitalización", "01: ~1,4 bill. (16-oct)", "01 etiquetada 'anterior a resultados' | 03: 1,47 bill. (23-oct)", "declarado"),
    ("Capex 2026 (guía)", "01 >20.000 y >25.000 | 03 '>20.000-25.000'", "01/03/04: ~20.000 (T1)", "corregido"),
    ("Servicios FY25 vs FY24", "01: +19,0 %", "01: +19,0 % | 02: +18,9 %", "redondeo (12.530/10.534-1 = 18,95 %); sigue"),
    ("Margen sin créditos TTM", "02 2,21 % | 04 script 2,23 %", "02 2,2 % (ingresos totales) | 03/04 2,23 % (ingresos sin créditos)", "dos definiciones, ya declaradas en 03 §2.1"),
]
for d in DIFS:
    print("  - " + " | ".join(d))

REV_TTM, EBIT_TTM, CRED_TTM = 103570.0, 3466.0, 1181.0
m02 = (EBIT_TTM - CRED_TTM) / REV_TTM
m04 = (EBIT_TTM - CRED_TTM) / (REV_TTM - CRED_TTM)
print(f"  - Margen operativo sin créditos TTM: 02 = (EBIT-créd)/ingresos = {m02:.2%} ; 03 v2 / 04 = (EBIT-créd)/(ingresos-créd) = {m04:.2%}")
print("    v2: 03 calcula ahora las anclas con el mismo denominador al que las aplica (m_ex). Ver §3.")

# ------------------------------------------------------------------------------------------
# 3. Supuestos de Fase 3 frente a datos de Fase 2
# ------------------------------------------------------------------------------------------
h("3. Supuestos de Fase 3 vs datos de Fase 2")
R = {}
with open(os.path.join(BASE, "data", "ratios.csv"), encoding="utf-8") as f:
    for row in csv.DictReader(f):
        R[row["metrica"]] = row
roic_a = [float(R["roic_A_neto_caja"][y]) for y in ("FY2021", "FY2022", "FY2023", "FY2024")]
print(f"ROIC A FY21-24: min {min(roic_a):.1%} max {max(roic_a):.1%} -> ROIC terminal base 12 % {'DENTRO' if min(roic_a) <= 0.12 <= max(roic_a) else 'FUERA (por debajo)'} del rango; 03 v2 §2.2 dice 'por debajo del rango' (v1 decía 'dentro')")


def m_ex_csv(y):  # margen sin créditos sobre ingresos sin créditos, reconstruido desde ratios.csv (no importa 03)
    cr = float(R["creditos_regulatorios"][y])
    return (float(R["beneficio_operativo"][y]) - cr) / (float(R["ingresos_totales"][y]) - cr)


M_OBJ_BASE = sum(m_ex_csv(y) for y in ("FY2021", "FY2022", "FY2023", "FY2024")) / 4   # esperado v2: 9,15 % (v1: 0,0893)
m0 = m_ex_csv("TTM_Q3_2026")                                                         # esperado v2: 2,23 % (v1: 2,21 %)
print(f"Margen sin créditos TTM {m0:.2%} -> base {M_OBJ_BASE:.2%} = x{M_OBJ_BASE / m0:.1f} (03 v2 / 04 v2.1: 9,15 %, x4,1)")
print(f"Energía 9M26 vs 9M25: {float(R['crec_9M26_vs_9M25_ingresos_energia']['TTM_Q3_2026']):.1%} -> supuesto base v2 +8 %/año (v1: +12 %)")

# Capex implícito del año 1 del caso base (reconstrucción independiente de run_dcf, con los supuestos declarados en 03 v2)
AUTO_EX0 = float(R["ingresos_automocion_total"]["TTM_Q3_2026"]) - CRED_TTM
ENER0 = float(R["ingresos_energia"]["TTM_Q3_2026"])
SERV0 = float(R["ingresos_servicios_otros"]["TTM_Q3_2026"])
rev1 = AUTO_EX0 * 1.04 + ENER0 * 1.08 + SERV0 * 1.15 + CRED_TTM * 0.4          # v1: energía x1,12
capex0 = float(R["capex"]["TTM_Q3_2026"])
da = float(R["dya_amortizacion_deterioro"]["TTM_Q3_2026"])                        # v2: 6.704 (v1: 1.852 x 4 = 7.408)
reinv_pct = (capex0 - da) / REV_TTM
reinv1 = max(reinv_pct * rev1, (rev1 - REV_TTM) / 1.5)
m1 = m0 + (M_OBJ_BASE - m0) / 5
ebit1 = m1 * (rev1 - CRED_TTM * 0.4) + CRED_TTM * 0.4
fcff1 = ebit1 * 0.79 - reinv1
st = "OK" if abs(fcff1 - (-5700)) <= 1 else "MISMATCH"
print(f"  [{st}] Año 1 base: ingresos {rev1:,.0f} | reinversión neta {reinv1:,.0f} | FCFF {fcff1:,.0f} (03 v2: -5.700; v1: -5.039)")
st = "OK" if abs(reinv1 + da - 15884) <= 1 else "MISMATCH"
print(f"  [{st}] Capex bruto implícito año 1 = reinversión + D&A TTM = {reinv1 + da:,.0f} M$ (03/04 v2: 15.884; v1 ~15.900)")
print("  -> por DEBAJO de la guía revisada ~20.000 M$ (T1); el modelo no usa la guía. W3 retirada en 04 v2 (sin cambio de criterio).")

# ------------------------------------------------------------------------------------------
# 4. Críticas de Fase 4 con comprobación numérica
# ------------------------------------------------------------------------------------------
h("4. Críticas de Fase 4")
# W5: Toyota
ev_tm, evs_tm = 418590.0, 1.45
print(f"W5 Toyota: ingresos implícitos = EV/(EV/Ventas) = {ev_tm / evs_tm:,.0f}. 03 §5 ya dice 'implícitos en su EV/Ventas'.")
print("    El argumento de 04 de que la deuda de la financiera 'infla' esta cifra es erróneo: EV/(EV/Ventas) = Ventas, la deuda se cancela.")
# W9 / 4.1.3: efecto de la beta sectorial
sens = {0.106: 28.55, 0.116: 24.60}   # v2: tabla 4.1 de 03 v2 (v1: 28.49 / 24.52)
d_int = (sens[0.106] - sens[0.116]) * (0.116 - 0.1046) / 0.01
print(f"W9 beta: interpolación de la tabla 4.1 v2 (g=3 %) VPA ≈ {sens[0.116] + d_int:.1f} $ (+{d_int:.1f} $). Esta interpolación desplaza también el WACC terminal")
print("    (la tabla 4.1 lo hace): es la cota superior (+4,6 $ medido). 03/04 v2 miden +1,2 $ cambiando solo los años 1-5: ver regex KEY. 05 v1 (+4,5 $) era la cota, no el efecto coherente")
# W1: PER
price, ni, sh_dil, sh_cov = 372.22, 3218.0, 3541.0, 3952.757946
print(f"W1 PER: precio/(BN/diluida) = {price / (ni / sh_dil):.0f}x ; capitalización/BN = {price * sh_cov / ni:.0f}x ; GuruFocus 410,4x -> 03 usa la convención estándar; 457x es alternativa, no corrección")
# W2 / 4.2.4: dilución
acc = {k: float(R[k]["TTM_Q3_2026"]) for k in ("acc_portada_15oct26", "acc_basica_media_3T26", "acc_restringidas_ceo2025",
                                                "acc_netas_ejercicio_2018", "acc_stock_based_awards_3T26", "acc_totalmente_diluidas_aprox")}
print(f"W2 dilución (v2, 02 §5.1): portada {acc['acc_portada_15oct26']:,.1f} - básica {acc['acc_basica_media_3T26']:,.0f} = "
      f"{acc['acc_portada_15oct26'] - acc['acc_basica_media_3T26']:.1f} M = CEO 2025 {acc['acc_restringidas_ceo2025']} + 2018 neto {acc['acc_netas_ejercicio_2018']} + residuo")
print(f"    301 M (diluida - básica) ≈ {acc['acc_netas_ejercicio_2018']} (2018, ya en portada) + ~{acc['acc_stock_based_awards_3T26'] - acc['acc_netas_ejercicio_2018']:.1f} -> "
      f"portada + 301 contaba dos veces ~286 M (v1 de 05: SIN VERIFICAR; v2: doble cómputo real, INFERENCIA bien apoyada)")
print(f"    03 v2 usa {acc['acc_totalmente_diluidas_aprox']:,.1f} M; VPA 'corregidos' de 04 v1 (11,6/27,5/61,5 $) siguen retirados (excluían 423,7 M emitidas)")

shutil.rmtree(tmp, ignore_errors=True)
