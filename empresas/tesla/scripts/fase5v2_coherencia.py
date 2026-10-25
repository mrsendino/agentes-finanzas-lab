"""Fase 5 v2 (segunda verificación) - coherencia entre fases y cifras de v1 que sobreviven en los documentos v2.

1. Misma cifra en 01-04 v2: PER, márgenes, acciones, caja/deuda y valores por acción. Imprime todas las apariciones
   (fuera de los «Registro de cambios») para comprobar que el valor es idéntico o está etiquetado.
2. Cifras propias de v1 (sustituidas en v2) que siguen apareciendo en el cuerpo de 01-04. Cada aparición se marca
   como ETIQUETADA si la misma línea la presenta como v1 / anterior / retirada / desfasada, y si no, como REVISAR.
No modifica nada. Uso: python3 scripts/fase5v2_coherencia.py
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
    "Margen operativo TTM (3,4 / 3,3)": r"3,[34] % (?:TTM|\(TTM\))",
    "Margen sin créditos TTM": r"2,2[13]? %",
    "Margen operativo 3T26": r"2,6 %",
    "Acciones portada": r"3\.95[23](?:,\d+)? M|3\.952\.757\.946",
    "Acciones totalmente diluidas": r"3\.96[47](?:,\d)? M",
    "Caja + inversiones 30-sep-26": r"45\.4\d\d",
    "Deuda 30-sep-26": r"9\.523|8\.180|8\.376",
    "Caja neta": r"35\.9\d\d|35\.683",
    "VPA bajista": r"10,[34]\d? \$|10,[34]\d? /",
    "VPA base": r"24,[56]\d? \$|/ 24,[56]\d? /|~25 \$",
    "VPA alcista": r"5[456],\d+ \$|/ 5[456],\d+ \$|~56 \$",
    "Opcionalidad implícita $/acción": r"31[67]-362 \$|316,5-361,8",
    "Brecha % capitalización": r"8[45],\d-97,2 %|85-97 %|85 % y el 97 %|~93 %",
    "WACC inicial": r"11,6\d? %",
    "ROIC TTM": r"5,5 %",
    "Capex 2026 guía": r"~?20\.000 M\$|>2[05]\.000",
    "D&A TTM": r"6\.704|7\.408",
    "SBC 3T26": r"1\.1[67]0|1\.165",
    "W9": r"\+1,2 \$|\+4,[56] \$|25,[89] \$|29,[12] \$",
    "Asimetría SBC/I+D": r"25,4\d? \$|25,5 \$|26,2\d? \$|26,3 \$",
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
}
LABEL = re.compile(r"v1|anterior|retirad|desfasad|DESFASADO|sustitu|antes|previ|en lugar de|no debe usarse|contraste|alternativ|v2\)|era|eran|pasa de|frente a 7\.408|no 7\.408|ya no", re.I)
n_rev = 0
for rx, what in STALE.items():
    for d, i, v, l in grep(rx):
        tag = "ETIQUETADA" if LABEL.search(l) else "REVISAR"
        n_rev += tag == "REVISAR"
        print(f"  [{tag:10}] {d}:{i:<4} {what:30} '{v}' | {l.strip()[:160]}")
print(f"\nApariciones sin etiqueta en la misma línea: {n_rev} (cada una se revisa a mano en 05-veredicto-v2 §4)")
