"""Fase 5 v3 (Reality Checker, tercera verificación) - propagación del cambio de beta (1,86 -> 1,84) en 01-04.

Idea: en lugar de una lista de cifras escrita a mano, se ejecuta el modelo de 03 v3 DOS veces en copias temporales:
  (a) tal cual (beta de regresión 1,84 y 1,84)            -> cifras vigentes v3
  (b) con las betas de v2 (1,85 y 1,87), nada más cambiado -> cifras que el documento v2 habría escrito
Se comparan las columnas «texto» de data/cifras_03_redondeo.csv (03) y la §14 de fase4_opcionalidad.py (04).
Cada cifra cuyo texto cambia (v2 -> v3) se busca en el CUERPO de 01-04 (sin «Registro de cambios»). Una aparición del
texto v2 es:
  ETIQUETADA  si la misma línea la presenta como v2 / anterior / versión previa, o
  REVISAR     si no (posible cifra v2 presentada como vigente).
Además busca una lista fija de valores v2 que no salen del CSV (WACC 11,60 %, betas 1,85 / 1,86 / 1,87, margen TTM 3,4 %).
No modifica data/ ni docs/. Uso: python scripts/fase5v3_propagacion.py [-v]
"""
import csv
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = ["01-negocio.md", "02-financieros.md", "03-valoracion.md", "04-tesis.md"]
ENV = dict(os.environ, DCF_NO_RECALC="1", PYTHONIOENCODING="utf-8", PYTHONUTF8="1")


def run_variant(betas):
    tmp = tempfile.mkdtemp(prefix="fase5v3_prop_")
    for d in ("data", "scripts"):
        shutil.copytree(os.path.join(BASE, d), os.path.join(tmp, d))
    p3 = os.path.join(tmp, "scripts", "fase3_dcf.py")
    if betas:
        src = open(p3, encoding="utf-8").read()
        n1 = src.count('"beta_reg_1": (1.84,')
        n2 = src.count('"beta_reg_2": (1.84,')
        assert n1 == 1 and n2 == 1, "no se encuentran las betas de 03 v3 en fase3_dcf.py"
        src = src.replace('"beta_reg_1": (1.84,', f'"beta_reg_1": ({betas[0]},').replace('"beta_reg_2": (1.84,', f'"beta_reg_2": ({betas[1]},')
        open(p3, "w", encoding="utf-8").write(src)
    subprocess.run([sys.executable, p3], cwd=tmp, env=ENV, capture_output=True, check=True)
    with open(os.path.join(tmp, "data", "cifras_03_redondeo.csv"), encoding="utf-8") as f:
        c03 = {r["clave"]: r["texto"] for r in csv.DictReader(f)}
    o4 = subprocess.run([sys.executable, os.path.join(tmp, "scripts", "fase4_opcionalidad.py")], cwd=tmp, env=ENV,
                        capture_output=True, text=True, encoding="utf-8", check=True).stdout
    c04 = {}
    if "14. Cifras que cita 04-tesis.md" in o4:
        for line in o4.split("14. Cifras que cita 04-tesis.md", 1)[1].splitlines():
            m = re.match(r"  (.{62}): (.*)$", line)
            if m:
                c04[m.group(1).strip()] = m.group(2)
    shutil.rmtree(tmp, ignore_errors=True)
    return c03, c04


v3_03, v3_04 = run_variant(None)
v2_03, v2_04 = run_variant((1.85, 1.87))

NUM = re.compile(r"−?\d[\d.]*,\d+|−?\d{1,3}(?:\.\d{3})+")


def nums(s):
    return NUM.findall(s)


pairs = []   # (origen, clave, texto v2, texto v3)
for k in v3_03:
    if v2_03.get(k) != v3_03[k]:
        pairs.append(("03", k, v2_03.get(k), v3_03[k]))
for k in v3_04:
    a, b = nums(v2_04.get(k, "")), nums(v3_04[k])
    for x, y in zip(a, b):
        if x != y:
            pairs.append(("04§14", k, x, y))

print(f"Cifras de 03 (cifras_03_redondeo.csv): {len(v3_03)}; cambian de texto con la beta: {sum(p[0] == '03' for p in pairs)}")
print(f"Cifras de la §14 de fase4: {len(v3_04)} líneas; números que cambian: {sum(p[0] != '03' for p in pairs)}")
if "-v" in sys.argv:
    for p in pairs:
        print("   ", " | ".join(str(x) for x in p))


def body_lines(doc):
    with open(os.path.join(BASE, "docs", doc), encoding="utf-8") as f:
        lines = f.read().splitlines()
    out = []
    for i, l in enumerate(lines, 1):
        if l.startswith("## Registro de cambios"):
            break
        out.append((i, l))
    return out


B = {d: body_lines(d) for d in DOCS}
LABEL = re.compile(r"v1|v2|anterior|antes|previ|era |eran |pasa de|pasaba|en lugar de|sustitu|retirad|desfasad|DESFASADO|"
                   r"con la beta de regresión de v2|frente a", re.I)

# Valores v2 a buscar: textos que cambian (solo los de >= 4 caracteres para evitar falsos positivos tipo "1,2")
targets = {}
for org, k, a, b in pairs:
    if a and len(a.replace("−", "")) >= 4 and a not in v3_03.values():
        targets.setdefault(a, set()).add(f"{org}:{k} -> {b}")
FIXED = {"11,60 %": "WACC inicial v2", "11,6 %": "WACC inicial v2 (1 dec.)", "1,86": "beta de regresión v2",
         "1,85": "beta TipRanks v2", "1,87": "beta MarketChameleon v2", "3,4 % (TTM": "margen operativo TTM v2",
         "3,4 %, ": "margen operativo TTM v2 (revisar contexto)", "+19,0 %": "servicios FY25 v2",
         "25,9 $": "M1 v2", "25,4 $": "M2 pedido en v2", "10-60 $": "saldo 04 v2"}
for t, what in FIXED.items():
    targets.setdefault(t, set()).add(what)

n_rev = n_lab = 0
print("\nApariciones de textos v2 en el cuerpo de 01-04 v3:")
for t, why in sorted(targets.items()):
    rx = re.compile(r"(?<![\d,.])" + re.escape(t) + (r"(?![\d]|,\d)" if t[-1].isdigit() else ""))
    for d in DOCS:
        for i, l in B[d]:
            if rx.search(l):
                tag = "ETIQUETADA" if LABEL.search(l) else "REVISAR"
                n_rev += tag == "REVISAR"
                n_lab += tag == "ETIQUETADA"
                print(f"  [{tag:10}] {d[:2]}:{i:<4} '{t}' ({'; '.join(sorted(why))[:70]}) | {l.strip()[:170]}")
print(f"\nTOTAL propagación: {len(targets)} textos v2 buscados; ETIQUETADA {n_lab}; REVISAR {n_rev}")
