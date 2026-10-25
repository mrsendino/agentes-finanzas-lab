r"""Fase 5 v2 (Reality Checker, segunda verificación) - cifras de los documentos v2 frente a la salida de los scripts.

A. 02-financieros.md: TODAS las celdas numéricas de las tablas de §2-§6 se comparan con data/ratios.csv regenerado.
B. 01, 03 y 04: catálogo de cifras citadas en el cuerpo (sin «Registro de cambios»), cada una con la expresión
   regular que la localiza y el valor que dan fase2/fase3/fase4 ejecutados en una copia temporal.
Redondeo: mitad hacia arriba sobre el valor completo del script (no sobre un valor ya redondeado).
Resultado: OK / MISMATCH / NO ENCONTRADA. No modifica data/ ni docs/.
Uso: python3 scripts/fase5v2_cifras.py

REGISTRO DE CAMBIOS v2 -> v3 (2026-10-25, tercera verificación). No se toca ningún modelo; solo anclas (texto fijo que
rodea a la cifra en el documento), cobertura y cálculo del valor exacto. Los VALORES esperados siguen saliendo de la
ejecución viva de fase2/3/4, así que el cambio de beta de 03 v3 (1,86 -> 1,84) entra solo.
  Anclas que dependían de valores v2 y ya no existen en los documentos v3 (daban NO ENCONTRADA):
    03 §8   "23,6-(x) $ (coherente)"          -> "(x)-(y) $ (coherente)"; se comprueban los dos extremos
    04 §4.2.4 "**10,40 / (x) / 55,76 $**"     -> "**a / (x) / c $** con acciones de portada" (+ los 6 valores)
    04 §4.2.4 "**10,36 / 24,52 / (x) $**"     -> "con acciones de portada y **a / b / (x) $**"
    04 §4.1.1 "pasa de 24,61 $ a (x) $"       -> "pasa de [\d,]+ $ a (x) $" (+ el punto de partida 24,65)
    04 §4.1.1 "que 03 v2 §6.3 ((x) /"         -> "que 03 v\d §6.3 ((x) / (y) $)"
    04 §4.1.3 "(24,6 → (x) $)"                -> "((a) → (x) $)" (+ el punto de partida)
    04 §4.1.3 "+4,6 $** (→ (x) $)"            -> "**+(d) $** (→ (x) $) si se desplaza" (+ la diferencia y el WACC_T)
    04 §0   "24,6 $ a **(x)-(y) $** (script"  -> "de (a) $ a **(x)-(y) $** (script"
  Cobertura nueva (v3): beta de regresión de 03 §1 y §1.1; W9 desplazado +4,4 $ en 03 §4.3; margen operativo TTM 3,3 %
    en 02 §0, 03 §7 y 04 §3.2; diferencial ROIC A − WACC inicial en 04 §1; VPA a 1 decimal de 04 §0 y saldo; rango
    "10,4-55,9 $" del saldo de 04; VPA totalmente diluidos de 03 §0.
  Valor exacto (corrección de un punto ciego de v2): para ROIC A, ROIC B y ROE el comprobador usaba el valor de
    ratios.csv a 4 decimales; por eso no detectó en v2 el doble redondeo del ROIC B FY23 (12,145 % -> 12,2 %) que
    encontró Fase 2. Ahora se recalculan desde NOPAT y el capital medio, como fase2_ratios.py.
"""
import contextlib
import csv
import importlib.util
import io
import os
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
from decimal import Decimal, ROUND_HALF_UP

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = tempfile.mkdtemp(prefix="fase5v2_")
for d in ("data", "scripts"):
    shutil.copytree(os.path.join(BASE, d), os.path.join(TMP, d))
os.environ["DCF_NO_RECALC"] = "1"
subprocess.run([sys.executable, os.path.join(TMP, "scripts", "fase2_ratios.py")], capture_output=True, check=True)
with open(os.path.join(TMP, "data", "ratios.csv"), encoding="utf-8") as f:
    R = {r["metrica"]: r for r in csv.DictReader(f)}

_spec = importlib.util.spec_from_file_location("f3", os.path.join(TMP, "scripts", "fase3_dcf.py"))
f3 = importlib.util.module_from_spec(_spec)
with contextlib.redirect_stdout(io.StringIO()):
    _spec.loader.exec_module(f3)
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    G4 = runpy.run_path(os.path.join(TMP, "scripts", "fase4_opcionalidad.py"))
O4 = _buf.getvalue()


def rnd(x, d):
    q = Decimal(1).scaleb(-d)
    return float(Decimal(repr(x)).quantize(q, rounding=ROUND_HALF_UP))


def num(s):
    s = s.replace("**", "").replace("−", "-").replace("–", "-").strip()
    s = s.replace(".", "").replace(",", ".")
    return float(s)


def body(doc):
    with open(os.path.join(BASE, "docs", doc), encoding="utf-8") as f:
        t = f.read()
    i = t.find("## Registro de cambios")
    return t if i < 0 else t[:i]


RESULTS = []


def report(doc, desc, cited, expect, st):
    RESULTS.append((st, doc, desc, cited, expect))


# ------------------------------------------------------------------------------------------------
# A. 02: tablas completas frente a ratios.csv
# ------------------------------------------------------------------------------------------------
PER = {"FY2021": "FY2021", "FY2022": "FY2022", "FY2023": "FY2023", "FY2024": "FY2024", "FY2025": "FY2025",
       "TTM 3T26": "TTM_Q3_2026", "31-dic-21": "FY2021", "31-dic-22": "FY2022", "31-dic-23": "FY2023",
       "31-dic-24": "FY2024", "31-dic-25": "FY2025", "30-sep-26": "TTM_Q3_2026", "9M26 vs 9M25": "9M"}
LAB = {  # (sección, etiqueta) -> (métrica, tipo)  tipo: M = M$, P = %, G = crecimiento (crec_*)
    (2, "Ingresos totales"): ("ingresos_totales", "M"), (2, "Automoción (incl. créditos y leasing)"): ("ingresos_automocion_total", "M"),
    (2, "Venta de vehículos"): ("auto_ventas", "M"), (2, "Créditos regulatorios"): ("creditos_regulatorios", "M"),
    (2, "Leasing"): ("auto_leasing", "M"), (2, "Energía (generación y almacenamiento)"): ("ingresos_energia", "M"),
    (2, "Servicios y otros"): ("ingresos_servicios_otros", "M"),
    (2.1, "Ingresos totales"): ("ingresos_totales", "G"), (2.1, "Automoción"): ("ingresos_automocion_total", "G"),
    (2.1, "Créditos regulatorios"): ("creditos_regulatorios", "G"), (2.1, "Energía"): ("ingresos_energia", "G"),
    (2.1, "Servicios y otros"): ("ingresos_servicios_otros", "G"),
    (2.2, "Automoción"): ("peso_automocion", "P"), (2.2, "Energía"): ("peso_energia", "P"),
    (2.2, "Servicios y otros"): ("peso_servicios", "P"), (2.2, "Créditos regulatorios"): ("peso_creditos", "P"),
    (3, "Beneficio bruto"): ("beneficio_bruto", "M"), (3, "Margen bruto"): ("margen_bruto", "P"),
    (3, "Beneficio operativo"): ("beneficio_operativo", "M"), (3, "Margen operativo"): ("margen_operativo", "P"),
    (3, "Beneficio operativo sin créditos"): ("beneficio_operativo_sin_creditos", "M"),
    (3, "Margen operativo sin créditos"): ("margen_operativo_sin_creditos", "P"),
    (3, "Créditos / beneficio operativo"): ("creditos_sobre_benef_operativo", "P"),
    (3, "Beneficio neto atribuible a comunes"): ("beneficio_neto_atrib_comunes", "M"), (3, "Margen neto"): ("margen_neto", "P"),
    (3, "Crecimiento del beneficio operativo"): ("beneficio_operativo", "G"),
    (3, "Crecimiento del beneficio neto"): ("beneficio_neto_atrib_comunes", "G"),
    (4, "Flujo de caja operativo (FCO)"): ("flujo_caja_operativo", "M"), (4, "FCO / ingresos"): ("margen_fco", "P"),
    (4, "Capex"): ("capex", "M"), (4, "Capex / ingresos"): ("capex_sobre_ingresos", "P"), (4, "Capex / FCO"): ("capex_sobre_fco", "P"),
    (4, "FCF (FCO − capex)"): ("fcf", "M"), (4, "Margen FCF"): ("margen_fcf", "P"), (4, "SBC"): ("sbc", "M"),
    (4, "SBC / ingresos"): ("sbc_sobre_ingresos", "P"), (4, "FCF − SBC"): ("fcf_menos_sbc", "M"),
    (4, "D&A (amortización, depreciación y deterioro) — v2"): ("dya_amortizacion_deterioro", "M"),
    (4, "D&A / ingresos — v2"): ("dya_sobre_ingresos", "P"), (4, "Capex − D&A (capex neto) — v2"): ("capex_neto_de_dya", "M"),
    (4, "EBIT + D&A (EBITDA aprox., sin ajustar SBC) — v2"): ("ebitda_aprox", "M"),
    (5, "Caja + inversiones a corto plazo"): ("caja_y_inversiones_cp", "M"),
    (5, "Deuda y arrendamientos financieros, corriente"): ("deuda_corriente", "M"),
    (5, "Deuda y arrendamientos financieros, no corriente"): ("deuda_no_corriente", "M"),
    (5, "Deuda total"): ("deuda_total", "M"), (5, "Caja neta"): ("caja_neta", "M"),
    (5, "Patrimonio neto de los accionistas"): ("patrimonio_neto_accionistas", "M"),
    (6, "NOPAT (M$)"): ("nopat_21pct", "M"), (6, "Capital invertido A, saldo final (M$)"): ("capital_invertido_A_neto_caja", "M"),
    (6, "Capital invertido B, saldo final (M$)"): ("capital_invertido_B_bruto", "M"),
    (6, "ROIC A (neto de caja)"): ("roic_A_neto_caja", "P"), (6, "ROIC B (bruto)"): ("roic_B_bruto", "P"),
    (6, "ROE (beneficio neto / patrimonio medio)"): ("roe", "P"),
}
# valores exactos para porcentajes (evita el doble redondeo del CSV, que guarda 4 decimales)
RAW = {}
with open(os.path.join(TMP, "data", "tesla_financials.csv"), encoding="utf-8") as f:
    for row in csv.DictReader(f):
        RAW[row["metrica"]] = row


def roic_exact(metric, per):
    """v3: ROIC A / ROIC B / ROE con la misma fórmula que fase2_ratios.py, desde importes (sin redondear el %)."""
    prev = {"FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024"}
    raw9 = lambda m: float(RAW[m]["9M2025"])
    if metric == "roe":
        num_, ic, open_ = float(R["beneficio_neto_atrib_comunes"][per]), "patrimonio_neto_accionistas", raw9("patrimonio_neto_accionistas")
    else:
        num_ = float(R["beneficio_operativo"][per]) * 0.79
        ic = "capital_invertido_A_neto_caja" if metric == "roic_A_neto_caja" else "capital_invertido_B_bruto"
        open_ = raw9("patrimonio_neto_accionistas") + raw9("deuda_corriente") + raw9("deuda_no_corriente") - \
            (raw9("caja_y_inversiones_cp") if metric == "roic_A_neto_caja" else 0.0)
    end = float(R[ic][per])
    if per == "TTM_Q3_2026":
        return num_ / ((end + open_) / 2)
    if per == "FY2021":
        return num_ / end
    return num_ / ((end + float(R[ic][prev[per]])) / 2)


def pct_exact(metric, per, kind):
    """Recalcula el % con los importes del CSV de ratios (sin redondear), cuando la fórmula es directa."""
    rv = lambda m, p: float(R[m][p])
    try:
        if kind == "G":
            if per == "9M":
                a, b = float(RAW[metric]["9M2026"]), float(RAW[metric]["9M2025"])
                return a / b - 1
            prev = {"FY2022": "FY2021", "FY2023": "FY2022", "FY2024": "FY2023", "FY2025": "FY2024"}[per]
            return rv(metric, per) / rv(metric, prev) - 1
        num_den = {
            "peso_automocion": ("ingresos_automocion_total", "ingresos_totales"), "peso_energia": ("ingresos_energia", "ingresos_totales"),
            "peso_servicios": ("ingresos_servicios_otros", "ingresos_totales"), "peso_creditos": ("creditos_regulatorios", "ingresos_totales"),
            "margen_bruto": ("beneficio_bruto", "ingresos_totales"), "margen_operativo": ("beneficio_operativo", "ingresos_totales"),
            "margen_operativo_sin_creditos": ("beneficio_operativo_sin_creditos", "ingresos_totales"),
            "creditos_sobre_benef_operativo": ("creditos_regulatorios", "beneficio_operativo"),
            "margen_neto": ("beneficio_neto_atrib_comunes", "ingresos_totales"), "margen_fco": ("flujo_caja_operativo", "ingresos_totales"),
            "capex_sobre_ingresos": ("capex", "ingresos_totales"), "capex_sobre_fco": ("capex", "flujo_caja_operativo"),
            "margen_fcf": ("fcf", "ingresos_totales"), "sbc_sobre_ingresos": ("sbc", "ingresos_totales"),
            "dya_sobre_ingresos": ("dya_amortizacion_deterioro", "ingresos_totales"),
        }
        if metric in num_den:
            n, d = num_den[metric]
            return rv(n, per) / rv(d, per)
        if metric in ("roic_A_neto_caja", "roic_B_bruto", "roe"):   # v3: exacto, no el CSV a 4 decimales
            return roic_exact(metric, per)
    except (KeyError, ValueError, ZeroDivisionError):
        pass
    return float(R[metric][per])


EXACT_M = {"nopat_21pct": lambda p: float(R["beneficio_operativo"][p]) * 0.79}
t02 = body("02-financieros.md")
sec, sub, header = None, 0, None
for line in t02.splitlines():
    m = re.match(r"## (\d+)\.", line)
    if m:
        sec, sub, header = int(m.group(1)), 0, None
        continue
    if not line.startswith("|"):
        header = None
        continue
    if sec not in (2, 3, 4, 5, 6) or line.startswith("|---"):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if header is None:
        header = cells
        sub = 0.1 if (sec == 2 and cells[0].startswith("Crecimiento")) else 0.2 if (sec == 2 and cells[0].startswith("Peso")) else 0
        continue
    lab = cells[0].replace("**", "").lstrip("· ").strip()
    key = (sec + sub, lab)
    if key not in LAB:
        continue
    metric, kind = LAB[key]
    for hcell, val in zip(header[1:], cells[1:]):
        per = PER.get(hcell.replace("**", ""))
        if per is None or val in ("—", "") or "SIN VERIFICAR" in val:
            continue
        v = val.replace("9M: ", "")
        if kind == "G" and per != "9M" and metric in ("beneficio_operativo", "beneficio_neto_atrib_comunes") and hcell == "TTM 3T26":
            per = "9M"
        if per == "9M" and kind != "G":
            continue
        cited = num(v.replace("%", ""))
        if kind == "M":
            exact = EXACT_M.get(metric, lambda p: float(R[metric][p]))(per)
            exp, exp_csv = rnd(exact, 0), rnd(float(R[metric][per]), 0)
        else:
            exp = rnd(pct_exact(metric, per, kind) * 100, 1)
            csvm = ("crec_9M26_vs_9M25_" + metric, "TTM_Q3_2026") if (kind == "G" and per == "9M") else \
                   (("crec_" + metric, per) if kind == "G" else (metric, per))
            exp_csv = float(f"{float(R[csvm[0]][csvm[1]]) * 100:.1f}")  # como lo formatea la fase (Python, sobre el CSV)
        if abs(cited - exp) < 1e-9:
            st = "OK"
        elif abs(cited - exp_csv) < 1e-9:
            st = "DOBLE REDONDEO"   # coincide con ratios.csv (4 decimales) pero no con el valor exacto
        else:
            st = "MISMATCH"
        report("02", f"§{sec} {lab} [{hcell}]", val, exp, st)

# ------------------------------------------------------------------------------------------------
# B. Catálogo 01, 03, 04
# ------------------------------------------------------------------------------------------------
RES = {k: v["vps"] for k, v in f3.RES.items()}
B0 = f3.RES["base"]


def o4(rx, cast=float):
    m = re.search(rx, O4)
    return cast(m.group(1).replace(",", "")) if m else None


CAT = [
    # (doc, descripción, regex con un grupo numérico, valor exacto, decimales)
    # --- 01 (cifras que dependen de 02) ---
    ("01-negocio.md", "Caja + inv 30-sep-26", r"Caja e inversiones a 30-sep-2026:\*\* ([\d.]+)", float(R["caja_y_inversiones_cp"]["TTM_Q3_2026"]), 0),
    ("01-negocio.md", "Deuda 30-sep-26", r"Deuda y arrendamientos financieros a 30-sep-2026:\*\* ([\d.]+)", float(R["deuda_total"]["TTM_Q3_2026"]), 0),
    ("01-negocio.md", "Caja neta", r"Caja neta: ([\d.]+) M\$\*\*", float(R["caja_neta"]["TTM_Q3_2026"]), 0),
    ("01-negocio.md", "Ingresos FY25", r"\*\*Total\*\* \| \*\*([\d.]+)\*\*", float(R["ingresos_totales"]["FY2025"]), 0),
    ("01-negocio.md", "Automoción FY25 var", r"69\.526 \| (−[\d,]+) %", (69526 / 77070 - 1) * 100, 1),
    ("01-negocio.md", "Energía FY25 var", r"12\.771 \| \+([\d,]+) %", float(RAW["ingresos_energia"]["FY2025"]) / float(RAW["ingresos_energia"]["FY2024"]) * 100 - 100, 1),
    ("01-negocio.md", "Servicios FY25 var", r"12\.530 \| \+([\d,]+) %", (12530 / 10534 - 1) * 100, 1),
    ("01-negocio.md", "Total FY25 var", r"\*\*94\.827\*\* \| (−[\d,]+) %", (94827 / 97690 - 1) * 100, 1),
    ("01-negocio.md", "Margen bruto FY25", r"\*\*([\d,]+) %\*\* \(BB 17\.094\)", float(RAW["beneficio_bruto"]["FY2025"]) / 94827 * 100, 1),
    ("01-negocio.md", "BO FY25", r"Beneficio operativo:\*\* ([\d.]+) M\$", float(R["beneficio_operativo"]["FY2025"]), 0),
    ("01-negocio.md", "BN FY25", r"Beneficio neto atribuible:\*\* ([\d.]+) M\$", float(R["beneficio_neto_atrib_comunes"]["FY2025"]), 0),
    ("01-negocio.md", "BN FY25 var", r"3\.794 M\$, un (−\d+) %", (3794 / 7091 - 1) * 100, 0),
    ("01-negocio.md", "Créditos/BO FY25 (02: 45,8)", r"cálculo propio, ([\d,]+) % en \[02", 1993 / 4355 * 100, 1),
    ("01-negocio.md", "Capex FY25 (§4.6)", r"más del doble que los ([\d.]+) M\$ de FY2025", float(R["capex"]["FY2025"]), 0),
    ("01-negocio.md", "Peso automoción 3T26", r"aporta el ~(\d+) % de los ingresos de Q3 2026", 20560 / 28046 * 100, 0),
    ("01-negocio.md", "Margen energía 3T26", r"Energía \| 2\.881 \| 3\.415 \| −16 % \| ([\d,]+) %", 954 / 2881 * 100, 1),
    ("01-negocio.md", "Margen bruto 3T26", r"≈0 % \| \*\*([\d,]+) %\*\*", 5494 / 28046 * 100, 1),
    ("01-negocio.md", "Q4 capex implícito", r"el Q4 implícito es de ~([\d.]+) M\$", 20000 - 13014, -3),
    ("02-financieros.md", "§0 margen operativo TTM (v3)", r"y al ([\d,]+) % \(TTM\)", float(R["beneficio_operativo"]["TTM_Q3_2026"]) / float(R["ingresos_totales"]["TTM_Q3_2026"]) * 100, 1),
    ("01-negocio.md", "Ilustrativo 30x BN FY25", r"Eso daría ~([\d.]+) M\$", 30 * 3794, -3),
    # --- 03 ---
    ("03-valoracion.md", "Capitalización", r"\*\*([\d.]+) M\$\*\* \| Calculada como precio", f3.MCAP, 0),
    ("03-valoracion.md", "EV mercado", r"Valor de la empresa \(EV\) de mercado \| ([\d.]+) M\$", f3.EV_MKT, 0),
    ("03-valoracion.md", "D/E", r"Deuda / capitalización \| ([\d,]+) %", f3.D_E * 100, 2),
    ("03-valoracion.md", "Beta bottom-up", r"reapalancada \| ([\d,]+) \|", f3.BETA_BU, 2),
    ("03-valoracion.md", "Beta inicial", r"\*\*Beta inicial\*\* \| \*\*([\d,]+)\*\*", f3.BETA0, 2),
    ("03-valoracion.md", "Ke0", r"Coste del capital propio inicial \| ([\d,]+) %", f3.KE0 * 100, 2),
    ("03-valoracion.md", "Kd", r"después de impuestos \| ([\d,]+) %", f3.KD * 100, 2),
    ("03-valoracion.md", "wD", r"Deuda al ([\d,]+) % del capital", f3.W_D * 100, 2),
    ("03-valoracion.md", "WACC0", r"\*\*WACC inicial \(años 1-5\)\*\* \| \*\*([\d,]+) %", f3.WACC0 * 100, 2),
    ("03-valoracion.md", "Beta terminal", r"Beta terminal \| ([\d,]+) \|", f3.BETA_T, 2),
    ("03-valoracion.md", "WACC_T", r"perpetuidad\)\*\* \| \*\*([\d,]+) %", f3.WACC_T * 100, 2),
    ("03-valoracion.md", "WACC solo regresión", r"WACC inicial a ~([\d,]+) %", (f3.RF + f3.BETA_REG * f3.ERP) * (1 - f3.W_D) * 100 + f3.KD * f3.W_D * 100, 1),
    ("03-valoracion.md", "Margen TTM sin créd", r"\*\*Margen operativo sin créditos del ([\d,]+) %\*\*", f3.M_EX0 * 100, 2),
    ("03-valoracion.md", "Auto ex créd", r"automoción sin créditos \(([\d.]+)\)", f3.AUTO_EX0, 0),
    ("03-valoracion.md", "Capex neto %", r"\*\*([\d,]+) % de los ingresos\*\*, que es el capex neto", f3.NET_CAPEX0_PCT * 100, 2),
    ("03-valoracion.md", "Capex año 1", r"año 1 del caso base es de \*\*([\d.]+) M\$\*\*", f3.CAPEX_Y1, 0),
    ("03-valoracion.md", "Reinversión año 1", r"\*\*: ([\d.]+) M\$ de reinversión neta", B0["rows"][0]["reinv"], 0),
    ("03-valoracion.md", "Diferencia con guía", r"Queda \*\*([\d.]+) M\$ por debajo", 20000 - f3.CAPEX_Y1, 0),
    ("03-valoracion.md", "4T26 implícito", r"la guía implica ~([\d.]+) M\$ en 4T26", 20000 - 13014, 0),
    ("03-valoracion.md", "Ancla bajista", r"\*\*([\d,]+) %\*\* \| \*\*9,15 %\*\*", f3.M_EX_AVG_24_25 * 100, 2),
    ("03-valoracion.md", "Ancla base", r"\| \*\*([\d,]+) %\*\* \| \*\*14,91 %\*\*", f3.M_EX_AVG_21_24 * 100, 2),
    ("03-valoracion.md", "Ancla alcista", r"\*\*9,15 %\*\* \| \*\*([\d,]+) %\*\*", f3.M_EX_MAX * 100, 2),
    ("03-valoracion.md", "TACC bajista", r"\*\*TACC resultante de los ingresos a 10 años\*\* \| \*\*([\d,]+) %", f3.CAGR_SCEN["bajista"] * 100, 1),
    ("03-valoracion.md", "TACC base", r"\*\*TACC resultante.*?\| \*\*[\d,]+ %\*\* \| \*\*([\d,]+) %", f3.CAGR_SCEN["base"] * 100, 1),
    ("03-valoracion.md", "TACC alcista", r"\*\*TACC resultante.*?\| \*\*[\d,]+ %\*\* \| \*\*[\d,]+ %\*\* \| \*\*([\d,]+) %", f3.CAGR_SCEN["alcista"] * 100, 1),
    ("03-valoracion.md", "Opex TTM %", r"constante, que los gastos operativos bajen como % de los ingresos \| ([\d,]+) %", f3.OPEX_R0 * 100, 2),
    ("03-valoracion.md", "Opex necesario %", r"\| \*\*([\d,]+) %\*\*: un gasto operativo", f3.OPEX_R_NEEDED * 100, 2),
    ("03-valoracion.md", "Opex año 5", r"un gasto operativo de ([\d.]+) M\$ en el año 5", f3.OPEX5_NEEDED, 0),
    ("03-valoracion.md", "Ingresos ex año 5", r"ingresos un 37 % mayores \(([\d.]+) M\$", f3.R5_EX, 0),
    ("03-valoracion.md", "MB necesario", r"\| 18,35 % \| \*\*([\d,]+) %\*\*", f3.GM_NEEDED * 100, 2),
    ("03-valoracion.md", "MB TTM ex", r"margen bruto sin créditos \| ([\d,]+) %", f3.GM_EX0 * 100, 2),
    ("03-valoracion.md", "Margen limpio", r"\| 2,23 % \| \*\*([\d,]+) %\*\*, casi el mismo", f3.M0_AMBOS * 100, 2),
]
for k, nm in (("bajista", "Bajista"), ("base", r"\*\*Base \(media FY21-24\)\*\*"), ("alcista", "Alcista")):
    r_ = f3.RES[k]
    pre = rf"\| {nm} \| "
    CAT += [
        ("03-valoracion.md", f"§3 {k} ingresos año 10", pre + r"([\d.]+)", r_["rows"][-1]["rev"], 0),
        ("03-valoracion.md", f"§3 {k} EBIT año 10", pre + r"[\d.]+ \| ([\d.]+)", r_["rows"][-1]["ebit"], 0),
        ("03-valoracion.md", f"§3 {k} VP FCFF", pre + r"[\d.]+ \| [\d.]+ \| (−?[\d.]+)", r_["pv_sum"], 0),
        ("03-valoracion.md", f"§3 {k} VP TV", pre + r"[\d.]+ \| [\d.]+ \| −?[\d.]+ \| ([\d.]+)", r_["pv_tv"], 0),
        ("03-valoracion.md", f"§3 {k} %TV", pre + r"(?:[^|]+\|){4} (\d+) %", r_["tv_share"] * 100, 0),
        ("03-valoracion.md", f"§3 {k} EV", pre + r"(?:[^|]+\|){5} ([\d.]+)", r_["ev"], 0),
        ("03-valoracion.md", f"§3 {k} equity", pre + r"(?:[^|]+\|){6} ([\d.]+)", r_["eq"], 0),
        ("03-valoracion.md", f"§3 {k} VPA portada", pre + r"(?:[^|]+\|){7} \*\*([\d,]+) \$", r_["vps"], 1),
        ("03-valoracion.md", f"§3 {k} VPA FD", pre + r"(?:[^|]+\|){8} ([\d,]+) \$", f3.RES_DIL[k], 1),
        ("03-valoracion.md", f"§3 {k} vs precio", pre + r"(?:[^|]+\|){9} (−\d+) %", (r_["vps"] / f3.PRICE - 1) * 100, 0),
    ]
for i, w in enumerate(f3.W_GRID):
    lab = f"{w * 100:.2f}".replace(".", ",") + " %"
    for j, g in enumerate(f3.G_GRID):
        CAT.append(("03-valoracion.md", f"§4.1 WACC {lab} g {g:.1%}",
                    rf"\| \**{re.escape(lab)}\** \|" + r"(?: \**[\d,]+\** \|){" + str(j) + r"} \**([\d,]+)\**", f3.SENS[i][j], 1))
for i, mg in enumerate(f3.M_GRID):
    for j, gm in enumerate(f3.GM_GRID):
        CAT.append(("03-valoracion.md", f"§4.2 margen {mg:.0%} x{gm}",
                    rf"\| {int(mg * 100)} % \|" + r"(?: [\d,]+ \|){" + str(j) + r"} ([\d,]+)", f3.SENS2[i][j], 1))
CAT += [
    ("03-valoracion.md", "§4.3 ROIC=WACC", r"\| Valor por acción \| ([\d,]+) \$", f3.ROIC_SENS[0][2], 1),
    ("03-valoracion.md", "§4.3 ROIC 10 %", r"\| Valor por acción \| [\d,]+ \$ \| ([\d,]+) \$", f3.ROIC_SENS[1][2], 1),
    ("03-valoracion.md", "§4.3 ROIC 13,4 %", r"\| Valor por acción \| [\d,]+ \$ \| [\d,]+ \$ \| \*\*[\d,]+ \$\*\* \| ([\d,]+) \$", f3.ROIC_SENS[3][2], 1),
    ("03-valoracion.md", "§4.3 ROIC 15 %", r"\| Valor por acción \| [\d,]+ \$ \| [\d,]+ \$ \| \*\*[\d,]+ \$\*\* \| [\d,]+ \$ \| ([\d,]+) \$", f3.ROIC_SENS[4][2], 1),
    ("03-valoracion.md", "§4.3 W9 VPA solo años 1-5", r"solo en los años 1-5 \| [\d,]+ % \| [\d,]+ % \| ([\d,]+) \$", f3.W9_15, 1),
    ("03-valoracion.md", "§4.3 W9 dif", r"solo en los años 1-5 \|.*?\*\*\+([\d,]+) \$\*\*", f3.W9_15 - f3.RES["base"]["vps"], 1),
    ("03-valoracion.md", "§4.3 W9 desplazado VPA", r"como la tabla 4.1\) \| [\d,]+ % \| [\d,]+ % \| ([\d,]+) \$", f3.W9_SHIFT, 1),
    ("03-valoracion.md", "§4.3 W9 WACC sector", r"solo en los años 1-5 \| ([\d,]+) %", f3.WACC0_SEC * 100, 2),
    ("03-valoracion.md", "§4.3 W9 WACC_T desplazado", r"como la tabla 4.1\) \| [\d,]+ % \| ([\d,]+) %", (f3.WACC_T + f3.WACC0_SEC - f3.WACC0) * 100, 2),
    ("03-valoracion.md", "§8 rango ROIC/beta suelo", r"\| ([\d,]+)-[\d,]+ \$ \(coherente\)", f3.ROIC_SENS[0][2], 1),   # v3: ancla sin valores
    ("03-valoracion.md", "§8 rango ROIC/beta techo", r"\| [\d,]+-([\d,]+) \$ \(coherente\)", f3.W9_15, 1),
    ("03-valoracion.md", "§8 hasta (W9 desplazado)", r"\(coherente\); hasta ([\d,]+) \$", f3.W9_SHIFT, 1),
    # --- v3: cobertura nueva en 03 ---
    ("03-valoracion.md", "§1 beta de regresión (fuente 1)", r"Beta de regresión — \*\*v3\*\* \| ([\d,]+) y", f3.MKT["beta_reg_1"][0], 2),
    ("03-valoracion.md", "§1 beta de regresión (fuente 2)", r"Beta de regresión — \*\*v3\*\* \| [\d,]+ y ([\d,]+)", f3.MKT["beta_reg_2"][0], 2),
    ("03-valoracion.md", "§1 beta de regresión (media)", r"Beta de regresión — \*\*v3\*\* \| [\d,]+ y [\d,]+ → \*\*([\d,]+)\*\*", f3.BETA_REG, 2),
    ("03-valoracion.md", "§1.1 beta de regresión en la mezcla", r"Media al 50 % de la regresión \(([\d,]+)\)", f3.BETA_REG, 2),
    ("03-valoracion.md", "§4.3 W9 desplazado dif", r"como la tabla 4.1\) \|[^|]*\|[^|]*\|[^|]*\| \+([\d,]+) \$", f3.W9_SHIFT - f3.RES["base"]["vps"], 1),
    ("03-valoracion.md", "§4.3 VPA modelo", r"\*\*Modelo \(beta mezclada 50/50\)\*\* \|[^|]*\|[^|]*\| \*\*([\d,]+) \$", f3.RES["base"]["vps"], 1),
    ("03-valoracion.md", "§7 margen operativo TTM", r"varias veces el ([\d,]+) % de Tesla", float(R["beneficio_operativo"]["TTM_Q3_2026"]) / float(R["ingresos_totales"]["TTM_Q3_2026"]) * 100, 1),
    ("03-valoracion.md", "§0 VPA FD bajista", r"los valores apenas cambian: ([\d,]+) /", f3.RES_DIL["bajista"], 1),
    ("03-valoracion.md", "§0 VPA FD base", r"los valores apenas cambian: [\d,]+ / ([\d,]+) /", f3.RES_DIL["base"], 1),
    ("03-valoracion.md", "§0 VPA FD alcista", r"los valores apenas cambian: [\d,]+ / [\d,]+ / ([\d,]+) \$", f3.RES_DIL["alcista"], 1),
    ("03-valoracion.md", "§0 v3 base a 1 decimal", r"que a un decimal es \*\*([\d,]+) \$\*\*", f3.RES["base"]["vps"], 1),
    ("03-valoracion.md", "§8 VPA FD base", r"con acciones totalmente diluidas, 10-56 \$ \(base ([\d,]+) \$\)", f3.RES_DIL["base"], 1),
]
for idx, (lab, m0, nf, v) in enumerate(f3.ASYM_RES[1:], start=1):
    rx_lab = ["Sin la SBC por encima de FY2024", "Sin la I\\+D incremental de 3T26", "Sin ninguna de las dos",
              "Sin suelo de capex", "\\*\\*Las tres cosas a la vez"][idx - 1]
    CAT.append(("03-valoracion.md", f"§6.3 {lab[:40]} margen de partida", rx_lab + r"[^|]*\| \**([\d,]+) %\**", m0 * 100, 2))
    CAT.append(("03-valoracion.md", f"§6.3 {lab[:40]} VPA", rx_lab + r"[^|]*\|[^|]*\|[^|]*\| \**([\d,]+) \$", v, 1))
    CAT.append(("03-valoracion.md", f"§6.3 {lab[:40]} diferencia", rx_lab + r"[^|]*\|[^|]*\|[^|]*\|[^|]*\| \**\+([\d,]+) \$", v - f3.RES["base"]["vps"], 1))
for row in f3.REVERSE:
    M, cagr, rev10 = row["M"], row["c"], row["rev10"]
    lab = f"{int(round(M * 100))} %"
    CAT.append(("03-valoracion.md", f"§5 TACC margen {lab}", rf"\| \**{lab}\** \| \**([\d,]+) %", cagr * 100, 1))
    CAT.append(("03-valoracion.md", f"§5 ingresos año 10 margen {lab}", rf"\| \**{lab}\** \| \**[\d,]+ %\** \| \**([\d.]+)\**", rev10, 0))
for k in ("bajista", "base", "alcista"):
    gap = f3.MCAP - f3.RES[k]["eq"]
    nm = k.capitalize()
    CAT += [("03-valoracion.md", f"§5 brecha {k} M$", rf"\| {nm} \| [\d.]+ \| ([\d.]+) \|", gap, 0),
            ("03-valoracion.md", f"§5 brecha {k} %", rf"\| {nm} \| [\d.]+ \| [\d.]+ \| ([\d,]+) %", gap / f3.MCAP * 100, 1),
            ("03-valoracion.md", f"§5 brecha {k} $", rf"\| {nm} \| [\d.]+ \| [\d.]+ \| [\d,]+ % \| ([\d,]+) \|", gap / f3.SH, 1)]
CAT += [
    ("03-valoracion.md", "§7 EV/Ventas", r"\*\*Tesla \(calculado\)\*\* \| — \| \*\*([\d,]+)\*\*", f3.EV_MKT / f3.REV0, 1),
    ("03-valoracion.md", "§7 EV/EBITDA", r"\*\*Tesla \(calculado\)\*\* \| — \| \*\*[\d,]+\*\* \| \*\*([\d,]+)\*\*", f3.TSLA_EV_EBITDA, 0),
    ("03-valoracion.md", "§7 EV/EBIT", r"\*\*Tesla \(calculado\)\*\* \| — (?:\| \*\*[\d,]+\*\* ){2}\| \*\*([\d,]+)\*\*", f3.EV_MKT / f3.EBIT0, 0),
    ("03-valoracion.md", "§7 PER", r"\*\*Tesla \(calculado\)\*\* \| — (?:\| \*\*[\d,]+\*\* ){3}\| \*\*([\d,]+)\*\*", f3.PRICE / (f3.NI0 / 3541), 0),
    ("03-valoracion.md", "§6.4 $/acción", r"es decir, ([\d,]+) \$ por acción\*\*", (2865 + 962) / f3.SH, 2),
    ("03-valoracion.md", "§3 caja/acción", r"unos ([\d,]+) \$ por acción", f3.NETCASH0 / f3.SH, 1),
    ("03-valoracion.md", "§3 dif acciones", r"la diferencia es de ([\d,]+) M de acciones", f3.SH_FD - f3.SH, 1),
    ("03-valoracion.md", "§0 ~50 $", r"el caso base sube solo hasta ~(\d+) \$", f3.SENS[0][-1], 0),
    ("03-valoracion.md", "§5 ingresos Toyota", r"Toyota\*\* \(~([\d.]+) M\$", 418590 / 1.45, -3),
    ("03-valoracion.md", "§2.3 energía GWh var", r"\| Almacenamiento desplegado \(GWh\) \| 46,7 \| 50,2 \| \+([\d,]+) %", (50.2 / 46.7 - 1) * 100, 1),
    ("03-valoracion.md", "§2.3 ingreso/GWh FY25", r"aproximación\) \| ([\d,]+) \|", 12771 / 46.7, 1),
    ("03-valoracion.md", "§2.3 ingreso/GWh TTM", r"aproximación\) \| [\d,]+ \| ([\d,]+) \|", 12265 / 50.2, 1),
    ("03-valoracion.md", "§2.3 ingreso/GWh var", r"aproximación\) \| [\d,]+ \| [\d,]+ \| (−[\d,]+) %", (12265 / 50.2) / (12771 / 46.7) * 100 - 100, 1),
]
# --- 04 ---
EQ = {k: f3.RES[k]["vps"] for k in ("bajista", "base", "alcista")}
ROIC_A_TTM_EXACT = roic_exact("roic_A_neto_caja", "TTM_Q3_2026")   # v3: 04 §1 usa 0,055 copiado (02 a 1 decimal)
CAT += [
    ("04-tesis.md", "§1 DCF portada", r"\| DCF del negocio reportado \| ([\d,]+) / ", EQ["bajista"], 1),
    ("04-tesis.md", "§1 DCF base", r"\| DCF del negocio reportado \| [\d,]+ / ([\d,]+)", EQ["base"], 1),
    ("04-tesis.md", "§1 DCF alcista", r"\| DCF del negocio reportado \| [\d,]+ / [\d,]+ / ([\d,]+)", EQ["alcista"], 1),
    # v3: anclas sin valores v2 (antes "**10,40 / (x) / 55,76 $**" y "**10,36 / 24,52 / (x) $**")
    ("04-tesis.md", "§4.2.4 VPA portada bajista", r"\*\*([\d,]+) / [\d,]+ / [\d,]+ \$\*\* con acciones de portada", EQ["bajista"], 2),
    ("04-tesis.md", "§4.2.4 VPA portada base", r"\*\*[\d,]+ / ([\d,]+) / [\d,]+ \$\*\* con acciones de portada", EQ["base"], 2),
    ("04-tesis.md", "§4.2.4 VPA portada alcista", r"\*\*[\d,]+ / [\d,]+ / ([\d,]+) \$\*\* con acciones de portada", EQ["alcista"], 2),
    ("04-tesis.md", "§4.2.4 VPA FD bajista", r"con acciones de portada y \*\*([\d,]+) / [\d,]+ / [\d,]+ \$\*\*", f3.RES_DIL["bajista"], 2),
    ("04-tesis.md", "§4.2.4 VPA FD base", r"con acciones de portada y \*\*[\d,]+ / ([\d,]+) / [\d,]+ \$\*\*", f3.RES_DIL["base"], 2),
    ("04-tesis.md", "§4.2.4 VPA FD alcista", r"con acciones de portada y \*\*[\d,]+ / [\d,]+ / ([\d,]+) \$\*\*", f3.RES_DIL["alcista"], 2),
    ("04-tesis.md", "§2.3 EBIT central", r"\*\*([\d.]+) M\$\*\* \(43x", o4(r"referencia central .*?: ([\d,]+) M\$"), 0),
    ("04-tesis.md", "§2.3 rango bajo", r"\*\*([\d.]+)-[\d.]+ M\$\*\*", o4(r"necesario de la opcionalidad: ([\d,]+) -"), 0),
    ("04-tesis.md", "§2.3 rango alto", r"\*\*[\d.]+-([\d.]+) M\$\*\*", o4(r"necesario de la opcionalidad: [\d,]+ - ([\d,]+)"), 0),
    ("04-tesis.md", "§2.3 40x año 10", r"40x en el año 7 \| ([\d.]+) /", o4(r"40x NOPAT en el año 10 -> EBIT necesario ([\d,]+)"), 0),
    ("04-tesis.md", "§2.3 30x año 7", r"40x en el año 7 \| [\d.]+ / ([\d.]+) /", o4(r"30x NOPAT en el año 7 -> EBIT necesario ([\d,]+)"), 0),
    ("04-tesis.md", "§2.3 40x año 7", r"40x en el año 7 \| [\d.]+ / [\d.]+ / ([\d.]+)", o4(r"40x NOPAT en el año 7 -> EBIT necesario ([\d,]+)"), 0),
    ("04-tesis.md", "§4.1.1 VPA de partida", r"el caso base pasa de ([\d,]+) \$ a [\d,]+ \$ o", EQ["base"], 2),
    ("04-tesis.md", "§4.1.1 VPA SBC", r"el caso base pasa de [\d,]+ \$ a ([\d,]+) \$", f3.ASYM_RES[1][3], 2),
    ("04-tesis.md", "§4.1.1 VPA I+D", r"a [\d,]+ \$ o ([\d,]+) \$", f3.ASYM_RES[2][3], 2),
    ("04-tesis.md", "§4.1.1 cita de 03 §6.3 (SBC)", r"las mismas cifras que 03 v\d §6.3 \(([\d,]+) /", f3.ASYM_RES[1][3], 1),
    ("04-tesis.md", "§4.1.1 cita de 03 §6.3 (I+D)", r"las mismas cifras que 03 v\d §6.3 \([\d,]+ / ([\d,]+) \$\)", f3.ASYM_RES[2][3], 1),
    ("04-tesis.md", "§4.1.3 W9 punto de partida", r"\(([\d,]+) → [\d,]+ \$\) si solo cambia", EQ["base"], 1),
    ("04-tesis.md", "§4.1.3 W9 VPA 1-5", r"\([\d,]+ → ([\d,]+) \$\) si solo cambia", f3.W9_15, 1),
    ("04-tesis.md", "§4.1.3 W9 dif 1-5", r"\*\*\+([\d,]+) \$\*\* por acción \([\d,]+ →", f3.W9_15 - EQ["base"], 1),
    ("04-tesis.md", "§4.1.3 W9 desplazado dif", r"\*\*\+([\d,]+) \$\*\* \(→ [\d,]+ \$\) si se desplaza", f3.W9_SHIFT - EQ["base"], 1),
    ("04-tesis.md", "§4.1.3 W9 desplazado", r"\*\*\+[\d,]+ \$\*\* \(→ ([\d,]+) \$\) si se desplaza", f3.W9_SHIFT, 1),
    ("04-tesis.md", "§4.1.3 W9 WACC_T desplazado", r"si se desplaza también el WACC terminal \(al ([\d,]+) %\)", (f3.WACC_T + f3.WACC0_SEC - f3.WACC0) * 100, 2),
    ("04-tesis.md", "§4.1.3 interpolación", r"\((\d+,\d) \$ interpolando", o4(r"método de 05 §3.3\): ([\d.]+) \$"), 1),
    ("04-tesis.md", "§0 ajuste máx punto de partida", r"sube el caso base de ([\d,]+) \$ a \*\*[\d,]+-[\d,]+ \$\*\* \(script", EQ["base"], 1),
    ("04-tesis.md", "§0 ajuste máx bajo", r"de [\d,]+ \$ a \*\*([\d,]+)-[\d,]+ \$\*\* \(script", G4["up_lo"], 1),
    ("04-tesis.md", "§0 ajuste máx alto", r"de [\d,]+ \$ a \*\*[\d,]+-([\d,]+) \$\*\* \(script", G4["up_hi"], 1),
    # --- v3: cobertura nueva en 04 ---
    ("04-tesis.md", "§0 base a 1 decimal", r"\(03 v\d §3; base ([\d,]+) \$\)", EQ["base"], 1),
    ("04-tesis.md", "§0 WACC inicial", r"por debajo de un WACC inicial del ([\d,]+) %", f3.WACC0 * 100, 2),
    ("04-tesis.md", "§1 WACC inicial", r"\| ROIC A TTM / WACC inicial \| [\d,]+ % / ([\d,]+) %", f3.WACC0 * 100, 2),
    ("04-tesis.md", "§1 diferencial ROIC A − WACC0 (pp)", r"\(diferencial (−[\d,]+) pp\)", (ROIC_A_TTM_EXACT - f3.WACC0) * 100, 1),
    ("04-tesis.md", "§2.3 tasa alta", r"a una tasa del [\d,]+-([\d,]+) % \(WACC terminal e inicial", f3.WACC0 * 100, 2),
    ("04-tesis.md", "§3.2 margen operativo TTM", r"al ([\d,]+) % TTM \(02 v3\)", float(R["beneficio_operativo"]["TTM_Q3_2026"]) / float(R["ingresos_totales"]["TTM_Q3_2026"]) * 100, 1),
    ("04-tesis.md", "Saldo rango bajo", r"\(([\d,]+)-[\d,]+ \$ en 03 v3\)", EQ["bajista"], 1),
    ("04-tesis.md", "Saldo rango alto", r"\([\d,]+-([\d,]+) \$ en 03 v3\)", EQ["alcista"], 1),
    ("04-tesis.md", "§4.2.2 ROIC terminal suelo", r"midió su efecto: ([\d,]+)-[\d,]+ \$", f3.ROIC_SENS[0][2], 1),
    ("04-tesis.md", "§4.2.2 ROIC terminal techo", r"midió su efecto: [\d,]+-([\d,]+) \$", f3.ROIC_SENS[4][2], 1),
    ("04-tesis.md", "Saldo +bajo", r"\*\*\+([\d,]+) a \+[\d,]+ \$\*\* \(script §13", G4["up_lo"] - EQ["base"], 1),
    ("04-tesis.md", "Saldo +alto", r"\*\*\+[\d,]+ a \+([\d,]+) \$\*\* \(script §13", G4["up_hi"] - EQ["base"], 1),
    ("04-tesis.md", "Saldo efecto neto", r"el efecto neto en el caso base es de \+([\d,]+) \$", EQ["base"] - 24.53, 2),
    ("04-tesis.md", "§4.2.4 sobrestimación v1", r"Sobrestimaba las acciones un \+([\d,]+) %", (f3.SH_DIL_V1 / f3.SH_FD - 1) * 100, 1),
    ("04-tesis.md", "§4.2.4 infracontaba", r"Infracontaban las acciones un −([\d,]+) %", (1 - (f3.SH - 423.743904) / f3.SH_FD) * 100, 1),
    ("04-tesis.md", "§3.2 +18,9 %", r"un \*\*\+([\d,]+) % en 12 meses\*\*", (3953 / 3324 - 1) * 100, 1),
    ("04-tesis.md", "§2.4 margen 6,6", r"el margen subyacente sería del \*\*([\d,]+) %\*\* en 3T26", (718 + 1131) / 28046 * 100, 1),
    ("04-tesis.md", "§2.4 margen TTM 4,5", r"y del \*\*([\d,]+) %\*\* en TTM", (f3.M_EX0 + f3.D_SBC / f3.REV0_EX) * 100, 1),
    ("04-tesis.md", "§3.4 recorte", r"recorta a la mitad el valor implícito de la opcionalidad \(base\) \| ~(\d+) \$", o4(r"recortara a la mitad .*?: (\d+) \$"), 0),
    ("04-tesis.md", "§4.1.4 SpaceX $/acc", r"En total, \*\*([\d,]+) \$ por acción\*\*", (2865 + 962) / f3.SH, 2),
]
for lab, rx in (("negocio reportado bajo", r"de bajista a alcista \| (\d+)-\d+ \$"), ("negocio reportado alto", r"de bajista a alcista \| \d+-(\d+) \$")):
    CAT.append(("04-tesis.md", f"§5 {lab}", rx, EQ["bajista"] if "bajo" in lab else EQ["alcista"], 0))
for lab, key in (("modesta", "base \\+ 50% x combinación A moderada"), ("relevante", "base \\+ 50% x combinación B ambiciosa"),
                 ("ambicioso asegurado", "alcista \\+ combinación B ambiciosa materializada al 100 %"),
                 ("extremo probable", "base \\+ 50% x combinación C extrema"), ("extremo asegurado", "alcista \\+ combinación C extrema materializada al 100 %")):
    lo = o4(key + r"\s*: (\d+) -")
    hi = o4(key + r"\s*: \d+ - (\d+)")
    CAT.append(("04-tesis.md", f"§5 {lab}", {"modesta": r"combinación A \(1 M de robotaxis.*?\| (\d+)-(\d+) \$",
                                              "relevante": r"combinación B \(3 M de robotaxis.*?\| (\d+)-(\d+) \$",
                                              "ambicioso asegurado": r"combinación B al 100 % \| (\d+)-(\d+) \$",
                                              "extremo probable": r"combinación C \(10 M de robotaxis.*?\| (\d+)-(\d+) \$",
                                              "extremo asegurado": r"combinación C al 100 % \| (\d+)-(\d+) \$"}[lab], (lo, hi), "pair"))

ANCHOR = {"§4.2": "### 4.2", "§5 ": "## 5. DCF inverso", "§4.3": "### 4.3", "§4.1 ": "### 4.1", "§6.3": "### 6.3"}
for doc, desc, rx, val, dec in CAT:
    t = body(doc)
    if doc.startswith("03"):
        for pref, anc in ANCHOR.items():
            if desc.startswith(pref) and anc in t:
                t = t[t.index(anc):]
                break
    m = re.search(rx, t)
    if not m:
        report(doc[:2], desc, "—", val, "NO ENCONTRADA")
        continue
    if dec == "pair":
        cited = (num(m.group(1)), num(m.group(2)))
        st = "OK" if cited == (float(val[0]), float(val[1])) else "MISMATCH"
        report(doc[:2], desc, f"{m.group(1)}-{m.group(2)}", val, st)
        continue
    cited = num(m.group(1))
    exp = rnd(val, dec) if dec >= 0 else round(val, dec)
    st = "OK" if abs(cited - exp) < 1e-9 else "MISMATCH"
    report(doc[:2], desc, m.group(1), exp, st)

# ------------------------------------------------------------------------------------------------
print(f"{'estado':13} | doc | cifra | citado | script")
for st, doc, desc, cited, exp in RESULTS:
    if st != "OK":
        print(f"{st:13} | {doc} | {desc} | {cited} | {exp}")
from collections import Counter
c = Counter((r[1], r[0]) for r in RESULTS)
print("\nResumen por documento:")
for doc in ("01", "02", "03", "04"):
    print(f"  {doc}: " + ", ".join(f"{st} {c[(doc, st)]}" for st in ("OK", "DOBLE REDONDEO", "MISMATCH", "NO ENCONTRADA")))
print(f"TOTAL: {len(RESULTS)} cifras comprobadas; " + ", ".join(f"{st} {sum(1 for r in RESULTS if r[0] == st)}" for st in ("OK", "DOBLE REDONDEO", "MISMATCH", "NO ENCONTRADA")))
if "-v" in sys.argv:
    for st, doc, desc, cited, exp in RESULTS:
        print(f"  {st:3} {doc} {desc}: {cited} vs {exp}")
shutil.rmtree(TMP, ignore_errors=True)
