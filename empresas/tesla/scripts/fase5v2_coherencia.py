"""Fase 5 v2 (segunda verificación) - coherencia entre fases y cifras de v1 que sobreviven en los documentos v2.

1. Misma cifra en 01-04 v2: PER, márgenes, acciones, caja/deuda y valores por acción. Imprime todas las apariciones
   (fuera de los «Registro de cambios») para comprobar que el valor es idéntico o está etiquetado.
2. Cifras propias de v1 (sustituidas en v2) que siguen apareciendo en el cuerpo de 01-04. Cada aparición se marca
   como ETIQUETADA si la misma línea la presenta como v1 / anterior / retirada / desfasada, y si no, como REVISAR.
No modifica nada. Uso: python3 scripts/fase5v2_coherencia.py

REGISTRO DE CAMBIOS v2 -> v3 (2026-10-25, tercera verificación):
  §1 FIG: margen operativo TTM busca también "3,3 % (TTM)" y "3,3 % TTM"; WACC inicial busca "11,55 %"; VPA con los
     valores v3 (10,41 / 24,65 / 55,88; diluidos 10,37 / 24,56 / 55,67); W9 con +4,4 $ / 29,1 $; asimetría 25,49 / 26,30.
  §2 STALE: se añaden las cifras de v2 que cambian en v3 (beta 1,86 -> 1,84, M1, M2, margen TTM, +19,0 %, "10-60 $"),
     y la etiqueta acepta "v2". La búsqueda sistemática de cifras v2 está en scripts/fase5v3_propagacion.py.
  §3 nuevo: referencias de 02 a 01 v1 / 03 v1 / 04 v1 (criterio de APTO de 05-veredicto-v2 §8): cada línea del cuerpo de
     02 que nombra "01-negocio.md", "03 §" o "04" se marca ETIQUETADA si dice v1 / resuelto / retirado, y REVISAR si no.
"""
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = ["01-negocio.md", "02-financieros.md", "03-valoracion.md", "04-tesis.md"]


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


def grep(rx):
    hits = []
    for d in DOCS:
        for i, l in B[d]:
            for m in re.finditer(rx, l):
                hits.append((d[:2], i, m.group(0), l))
    return hits


def h(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)


# ------------------------------------------------------------------------------------------------
h("1. Misma cifra en todas las fases (valores distintos encontrados por cifra)")
FIG = {
    "PER TSLA": r"(?:~|\b)\d{3}(?:,\d)?x\b",
    "Margen operativo TTM (3,4 / 3,3)": r"3,[34] % (?:TTM|\(TTM\))|3,[34] % de Tesla",
    "Margen sin créditos TTM": r"2,2[13]? %",
    "Margen operativo 3T26": r"2,6 %",
    "Acciones portada": r"3\.95[23](?:,\d+)? M|3\.952\.757\.946",
    "Acciones totalmente diluidas": r"3\.96[47](?:,\d)? M",
    "Caja + inversiones 30-sep-26": r"45\.4\d\d",
    "Deuda 30-sep-26": r"9\.523|8\.180|8\.376",
    "Caja neta": r"35\.9\d\d|35\.683",
    "VPA bajista": r"10,[34]\d? \$|10,[34]\d? /",
    "VPA base": r"24,[567]\d? \$|/ 24,[567]\d? /|~25 \$",
    "VPA alcista": r"5[456],\d+ \$|/ 5[456],\d+ \$|~56 \$",
    "Opcionalidad implícita $/acción": r"31[67]-362 \$|316,5-361,8",
    "Brecha % capitalización": r"8[45],\d-97,2 %|85-97 %|85 % y el 97 %|~93 %",
    "WACC inicial": r"11,6\d? %|11,5\d %",
    "ROIC TTM": r"5,5 %",
    "Capex 2026 guía": r"~?20\.000 M\$|>2[05]\.000",
    "D&A TTM": r"6\.704|7\.408",
    "SBC 3T26": r"1\.1[67]0|1\.165",
    "W9": r"\+1,2 \$|\+4,[456] \$|25,[89] \$|29,[012] \$",
    "Asimetría SBC/I+D": r"25,4\d? \$|25,5 \$|26,2\d? \$|26,3\d? \$",
}
for name, rx in FIG.items():
    hits = grep(rx)
    vals = sorted({x[2] for x in hits})
    print(f"\n[{name}] valores distintos: {vals}")
    for d, i, v, l in hits:
        print(f"   {d}:{i:<4} {v:<14} | {l.strip()[:150]}")

# ------------------------------------------------------------------------------------------------
h("2. Cifras de v1 que siguen en el cuerpo de v2")
STALE = {  # cifra v1 (sustituida en v2) -> qué es
    r"24,53": "VPA base v1", r"54,88|54,9 \$": "VPA alcista v1", r"10-55 \$": "rango v1", r"8,93 %": "ancla base v1",
    r"7\.408": "D&A 3T x4 v1", r"7,7 %": "capex neto % v1", r"4\.25[34]": "acciones portada+301 v1",
    r"22,79|9,62|51,00": "VPA 'dilución' v1", r"61\.040": "EV base v1", r"5\.039|4\.428": "FCFF v1",
    r"147\.561|134\.680|271\.287": "EBIT_10 v1", r"110\.671|111\.502|83\.627": "sensibilidades v1",
    r"15\.883|8\.475": "capex año 1 v1", r"317-362": "opcionalidad v1", r"28,4-31,8|\+7,3 \$": "ajuste máx v1",
    r"4,43 %|6,58 %": "márgenes asimetría v1", r"238-271|764-889": "rangos §5 v1", r"45\.400": "caja 01 v1",
    r"13\.010": "capex 9M S2", r"1\.170": "SBC S2", r"2\.760": "I+D S2", r"~327x": "PER S11 (pre-resultados)",
    r">20\.000-25\.000": "guía capex mezclada v1", r"16-99": "rango §8 v1", r"~51 \$": "§0 v1", r"3,45 %|14,58 %|8,9 %\b": "anclas v1",
    r"\+4-10 \$": "W9 v1", r"457x": "PER alternativo", r"11,6 / 27,5 / 61,5": "VPA 04 v1 retirados",
    r"\+12 %": "energía base v1", r"\+4,5 \$|~\+4,5": "W9 de 05 v1", r"5 % \(v1|v1: 5 %": "energía bajista v1",
    r"12,3 M|18,4 M": "flotas (no cambian)", r"1,4 billones": "capitalización pre-resultados",
    # v3: cifras de v2 sustituidas en v3
    r"24,61": "VPA base v2", r"55,76": "VPA alcista v2", r"10,40 /": "VPA bajista v2", r"10,36 /|24,52|55,55": "VPA FD v2",
    r"11,60 % \(|WACC inicial del 11,60|11,6 %": "WACC inicial v2", r"61\.353": "EV base v2", r"147\.527": "EBIT_10 v2",
    r"25,9 \$": "M1 v2", r"25,45|26,25": "asimetría v2", r"29,2 \$|\+4,6 \$": "W9 desplazado v2", r"1,86\b": "beta regresión v2",
    r"3,4 % (?:TTM|\(TTM\))": "margen TTM v2", r"28,5-31,9|31,86": "ajuste máx v2", r"\+19,0 %": "servicios FY25 v2",
    r"10-60 \$": "saldo 04 v2", r"316,5": "opcionalidad alcista v2",
}
LABEL = re.compile(r"v1|v2|anterior|retirad|desfasad|DESFASADO|sustitu|antes|previ|en lugar de|no debe usarse|contraste|alternativ|v2\)|era|eran|pasa de|frente a 7\.408|no 7\.408|ya no", re.I)
n_rev = 0
for rx, what in STALE.items():
    for d, i, v, l in grep(rx):
        tag = "ETIQUETADA" if LABEL.search(l) else "REVISAR"
        n_rev += tag == "REVISAR"
        print(f"  [{tag:10}] {d}:{i:<4} {what:30} '{v}' | {l.strip()[:160]}")
print(f"\nApariciones sin etiqueta en la misma línea: {n_rev} (cada una se revisa a mano en 05-veredicto-v2 §4)")

# ------------------------------------------------------------------------------------------------
h("3. (v3) Referencias de 02 a otras fases presentadas como vigentes")
REF = re.compile(r"01-negocio\.md|01 §|\b03 §|\b03 v|\b04 §|\b04 v|03 \(|04 \(")
OKLAB = re.compile(r"v1|v2|resuelt|retirad|DESFASADO|desfasad|corregid", re.I)
n3 = 0
for i, l in B["02-financieros.md"]:
    if REF.search(l):
        tag = "ETIQUETADA" if OKLAB.search(l) else "REVISAR"
        n3 += tag == "REVISAR"
        print(f"  [{tag:10}] 02:{i:<4} | {l.strip()[:170]}")
print(f"\nReferencias de 02 sin etiqueta de versión: {n3} (revisión manual en 05-veredicto-v3 §5)")
