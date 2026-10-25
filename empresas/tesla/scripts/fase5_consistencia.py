"""Fase 5 (Reality Checker) - controles de consistencia entre fases y sobre las críticas de Fase 4.

1. Re-ejecuta fase2/fase3/fase4 en una copia temporal (no toca data/ del proyecto) y compara
   las cifras impresas con las citadas en los documentos.
2. Cifras citadas de forma distinta en distintos documentos.
3. Supuestos de Fase 3 frente a datos de Fase 2.
4. Re-cálculo de las críticas de Fase 4 (W1-W11, §4.1-4.2) que admiten comprobación numérica.
Uso: python3 scripts/fase5_consistencia.py
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
print(f"Controles fase2: {n_ok} OK + {n_disc} DISCREPANCIA (02 §1.3 dice 50 + 5)")

# Cifras clave: (descripción, regex sobre la salida, valor citado en docs)
o3, o4 = OUT["fase3_dcf.py"], OUT["fase4_opcionalidad.py"]
KEY = [
    ("WACC0 (03 §1.1: 11,60 %)", o3, r"WACC0 ([\d.]+) \|", 0.1160, 1e-4),
    ("WACC_T (03: 9,79 %)", o3, r"WACC_T ([\d.]+)", 0.0979, 1e-4),
    ("VPA bajista (03: 10,4)", o3, r"bajista : .*?VPA ([\d.]+)", 10.4, 0.05),
    ("VPA base (03: 24,5)", o3, r"base    : .*?VPA ([\d.]+)", 24.5, 0.05),
    ("VPA alcista (03: 54,9)", o3, r"alcista : .*?VPA ([\d.]+)", 54.9, 0.05),
    ("EV base (03: 61.040)", o3, r"base    : .*?\| EV ([\d,]+)", 61040, 1),
    ("TACC margen 20 % (03: 36,1 %)", o3, r"Margen 20%: TACC necesaria ([\d.]+)%", 36.1, 0.05),
    ("TACC margen 30 % (03: 27,8 %)", o3, r"Margen 30%: TACC necesaria ([\d.]+)%", 27.8, 0.05),
    ("Precio implícito big tech EV/Ventas (03: 407,4)", o3, r"Mediana Big tech.*?'EV/Ventas': ([\d.]+)", 407.4, 0.05),
    ("EBIT_10 central (04: 147.561)", o4, r"referencia central .*?: ([\d,]+) M\$", 147561, 1),
    ("Recorte 50 % opcionalidad (04: 198 $)", o4, r"recortara a la mitad .*?: (\d+) \$", 198, 0.5),
    ("Margen 3T26 + I+D incremental (04: 6,6 %)", o4, r"sumando el incremento de I\+D: ([\d.]+)%", 6.6, 0.05),
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
h("2. Misma cifra, valores distintos según el documento")
DIFS = [
    ("Caja + inversiones 30-sep-26", "01: 45.400", "02/03/04: 45.447", "01 sin corregir (redondeo)"),
    ("Deuda", "01 §2: 8.180 (principal, 31-dic-25) junto a caja 30-sep-26", "02: 8.376 (31-dic-25) / 9.523 (30-sep-26)", "01 mezcla fechas y conceptos; sin corregir"),
    ("SBC 3T26", "01: 1.170 (S2)", "02/04: 1.165 (P4)", "01 sin corregir"),
    ("Capex 9M26", "01: 13.010 (S2)", "02/04: 13.014 (P2)", "01 sin corregir"),
    ("I+D 3T26", "01: 2.760 (S2)", "02/04: 2.761 (P4)", "redondeo"),
    ("Beneficio neto 3T26", "01: 787 'GAAP'", "02: 787 atribuible / 804 total", "etiqueta"),
    ("PER TSLA", "01: ~327x (S11, 354,72 $)", "02: 390x (354,72 $, BPA 0,91) | 03: 410x (372,22 $, media diluida) | 04: 457x (portada)", "4 PER distintos sin definición única"),
    ("Capitalización", "01: ~1,4 bill. (16-oct)", "03: 1,47 bill. (23-oct)", "fechas distintas, declarado"),
    ("Capex 2026 (guía)", "01: >20.000 (S5) y >25.000 (S2)", "03: '>20.000-25.000' | 04: ~20.000 (T1)", "01/03 desfasados; ver §3"),
    ("Servicios FY25 vs FY24", "01: +19,0 %", "02: +18,9 %", "redondeo"),
]
for d in DIFS:
    print("  - " + " | ".join(d))

REV_TTM, EBIT_TTM, CRED_TTM = 103570.0, 3466.0, 1181.0
m02 = (EBIT_TTM - CRED_TTM) / REV_TTM
m04 = (EBIT_TTM - CRED_TTM) / (REV_TTM - CRED_TTM)
print(f"  - Margen operativo sin créditos TTM: 02/03 = (EBIT-créd)/ingresos = {m02:.2%} ; 04 script = (EBIT-créd)/(ingresos-créd) = {m04:.2%} -> dos definiciones")
print("    03 calcula las anclas (8,93 %, 3,45 %, 14,58 %) sobre ingresos totales pero las aplica a ingresos sin créditos (run_dcf: mp*(rev-cred)+cred): incoherencia menor")

# ------------------------------------------------------------------------------------------
# 3. Supuestos de Fase 3 frente a datos de Fase 2
# ------------------------------------------------------------------------------------------
h("3. Supuestos de Fase 3 vs datos de Fase 2")
R = {}
with open(os.path.join(BASE, "data", "ratios.csv"), encoding="utf-8") as f:
    for row in csv.DictReader(f):
        R[row["metrica"]] = row
roic_a = [float(R["roic_A_neto_caja"][y]) for y in ("FY2021", "FY2022", "FY2023", "FY2024")]
print(f"ROIC A FY21-24: min {min(roic_a):.1%} max {max(roic_a):.1%} -> ROIC terminal base 12 % {'DENTRO' if min(roic_a) <= 0.12 <= max(roic_a) else 'FUERA (por debajo)'} del rango; 03 §2.2 dice 'dentro del rango'")
print(f"Margen sin créditos TTM {float(R['margen_operativo_sin_creditos']['TTM_Q3_2026']):.2%} -> base 8,93 % = x{0.0893 / float(R['margen_operativo_sin_creditos']['TTM_Q3_2026']):.1f}")
print(f"Energía 9M26 vs 9M25: {float(R['crec_9M26_vs_9M25_ingresos_energia']['TTM_Q3_2026']):.1%} -> supuesto base +12 %/año (03 cita el dato, lo justifica con TACC 46 %)")

# Capex implícito del año 1 del caso base (reconstrucción independiente de run_dcf)
AUTO_EX0 = float(R["ingresos_automocion_total"]["TTM_Q3_2026"]) - CRED_TTM
ENER0 = float(R["ingresos_energia"]["TTM_Q3_2026"])
SERV0 = float(R["ingresos_servicios_otros"]["TTM_Q3_2026"])
rev1 = AUTO_EX0 * 1.04 + ENER0 * 1.12 + SERV0 * 1.15 + CRED_TTM * 0.4
capex0 = float(R["capex"]["TTM_Q3_2026"])
da = 1852.0 * 4
reinv_pct = (capex0 - da) / REV_TTM
reinv1 = max(reinv_pct * rev1, (rev1 - REV_TTM) / 1.5)
m1 = m02 + (0.0893 - m02) / 5
ebit1 = m1 * (rev1 - CRED_TTM * 0.4) + CRED_TTM * 0.4
fcff1 = ebit1 * 0.79 - reinv1
print(f"Año 1 base: ingresos {rev1:,.0f} | reinversión neta {reinv1:,.0f} | FCFF {fcff1:,.0f} (03: -5.039)")
print(f"Capex bruto implícito año 1 = reinversión + D&A aprox = {reinv1 + da:,.0f} M$ (sin circulante)")
print("  -> por DEBAJO de la guía revisada ~20.000 M$ (T1). 03 cita '>20.000-25.000' en el texto pero el modelo NO usa esa cifra:")
print("     la crítica de 04 (§4.1.2 / W3: 'capex sobreestimado, pesimista') no se sostiene numéricamente.")

# ------------------------------------------------------------------------------------------
# 4. Críticas de Fase 4 con comprobación numérica
# ------------------------------------------------------------------------------------------
h("4. Críticas de Fase 4")
# W5: Toyota
ev_tm, evs_tm = 418590.0, 1.45
print(f"W5 Toyota: ingresos implícitos = EV/(EV/Ventas) = {ev_tm / evs_tm:,.0f}. 03 §5 ya dice 'implícitos en su EV/Ventas'.")
print("    El argumento de 04 de que la deuda de la financiera 'infla' esta cifra es erróneo: EV/(EV/Ventas) = Ventas, la deuda se cancela.")
# W9 / 4.1.3: efecto de la beta sectorial
sens = {0.106: 28.49, 0.116: 24.52}
print(f"W9 beta: WACC solo sector 10,46 % -> por interpolación de la tabla 4.1 (g=3 %) VPA ≈ {24.52 + (28.49 - 24.52) * (0.116 - 0.1046) / 0.01:.1f} $ (+{(28.49 - 24.52) * (0.116 - 0.1046) / 0.01:.1f} $). 04 dice '+4-10 $': el techo de 10 $ corresponde a WACC 9,6 %, no a la beta sectorial")
# W1: PER
price, ni, sh_dil, sh_cov = 372.22, 3218.0, 3541.0, 3952.757946
print(f"W1 PER: precio/(BN/diluida) = {price / (ni / sh_dil):.0f}x ; capitalización/BN = {price * sh_cov / ni:.0f}x ; GuruFocus 410,4x -> 03 usa la convención estándar; 457x es alternativa, no corrección")
# W2 / 4.2.4: dilución
print("W2 dilución: portada 3.953 - básica 3.240 = 713 M (acciones en circulación excluidas del BPA básico).")
print("    Diluida - básica = 301 M: efecto dilutivo (método de tesorería) de opciones, RSU y acciones restringidas no ganadas; composición no leída.")
print("    Si las 301 M proceden de acciones restringidas ya emitidas -> sumar a la portada duplica (tesis de 04); si proceden de opciones/RSU no emitidas -> no duplica.")
print("    -> W2 queda SIN VERIFICAR en ambos sentidos; los VPA 11,6/27,5/61,5 $ de 04 excluyen acciones legalmente emitidas y no deben presentarse como 'corrección'.")
print("    -> Lo que sí es error en 03: etiquetar las 301 M como 'techo de la dilución del plan del CEO' sin evidencia.")

shutil.rmtree(tmp, ignore_errors=True)
