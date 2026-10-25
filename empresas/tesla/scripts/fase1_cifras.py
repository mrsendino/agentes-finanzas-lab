"""Fase 1 (v3): cifras derivadas citadas en docs/01-negocio.md.

Recalcula cada porcentaje o cociente propio de 01 a partir de los importes que el propio
documento cita (con su fuente allí) y lo redondea UNA sola vez, con redondeo "half-up"
(Decimal), a los decimales que usa el documento. Imprime la cifra tal como debe aparecer
en 01 y la compara con la cifra publicada en 01; avisa si difieren.

No lee ni modifica data/. Uso: python empresas/tesla/scripts/fase1_cifras.py
"""
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import re
import sys

DOC = Path(__file__).resolve().parents[1] / "docs" / "01-negocio.md"


def r(x, d):
    q = Decimal(1).scaleb(-d) if d > 0 else Decimal(1)
    return Decimal(repr(x)).quantize(q, rounding=ROUND_HALF_UP)


def es(v, d, sign=False):
    s = f"{abs(v):,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if sign:
        s = ("+" if v > 0 else "−" if v < 0 else "") + s
    return s


def pct(a, b):
    return (a / b) * 100


def var(a, b):
    return (a / b - 1) * 100


# Importes (M$ salvo indicación) tal como los cita 01; fuente en 01 y en fuentes/.
SHARES_COVER = 3_952_757_946      # 10-Q 3T26 (P2), portada, a 15-oct-2026 (fuentes.md M3)
SHARES_CEO2025 = 423_743_904      # Form 4 16-jun-2026 (F4-1, nuevas_fase2_v2.md)
H1_26_REV = 78_669 - 28_046       # 9M26 (P2) − 3T26 (P4) = ingresos H1 2026

# (etiqueta, valor sin redondear, decimales, con signo, cifra publicada en 01 v2)
ITEMS = [
    # §1.1 FY2025
    ("§1.1 Automoción FY25 var (69.526 / 77.070)", var(69526, 77070), 1, True, "−9,8"),
    ("§1.1 Créditos FY25 var (1.993 / 2.763)", var(1993, 2763), 0, True, "−28"),
    ("§1.1 Energía FY25 var (12.771 / 10.086)", var(12771, 10086), 1, True, "+26,6"),
    ("§1.1 Servicios FY25 var (12.530 / 10.534)", var(12530, 10534), 1, True, "+19,0"),
    ("§1.1 Total FY25 var (94.827 / 97.690)", var(94827, 97690), 1, True, "−2,9"),
    ("§1.1 Margen automoción FY25 (12.361 / 69.526)", pct(12361, 69526), 1, False, "17,8"),
    ("§1.1 Margen energía FY25 (3.802 / 12.771)", pct(3802, 12771), 1, False, "29,8"),
    ("§1.1 BB servicios FY25 derivado (13.292 − 12.361), M$", 13292 - 12361, 0, False, "931"),
    ("§1.1 Margen servicios FY25 (931 / 12.530)", pct(13292 - 12361, 12530), 1, False, "7,4"),
    ("§1.1 Margen bruto total FY25 (17.094 / 94.827)", pct(17094, 94827), 1, False, "18,0"),
    ("§1.1 BN atribuible FY25 var (3.794 / 7.091)", var(3794, 7091), 0, True, "−46"),
    # §1.2 Q3 2026
    ("§1.2 Automoción 3T var (20.560 / 21.205)", var(20560, 21205), 0, True, "−3"),
    ("§1.2 Créditos 3T var (113 / 417)", var(113, 417), 0, True, "−73"),
    ("§1.2 Energía 3T var (2.881 / 3.415)", var(2881, 3415), 0, True, "−16"),
    ("§1.2 Servicios 3T var (4.605 / 3.475)", var(4605, 3475), 0, True, "+33"),
    ("§1.2 Total 3T var (28.046 / 28.095)", var(28046, 28095), 1, True, "≈0 (−0,2)"),
    ("§1.2 Margen energía 3T (954 / 2.881)", pct(954, 2881), 1, False, "33,1"),
    ("§1.2 Margen servicios 3T (734 / 4.605)", pct(734, 4605), 1, False, "15,9"),
    ("§1.2 Margen bruto total 3T (5.494 / 28.046)", pct(5494, 28046), 1, False, "19,6"),
    ("§1.2 BO 3T var (718 / 1.624)", var(718, 1624), 0, True, "−56"),
    ("§1.2 Margen operativo 3T (718 / 28.046)", pct(718, 28046), 1, False, "2,6"),
    ("§1.2 I+D 3T var (2.761 / 1.630)", var(2761, 1630), 0, True, "+69"),
    ("§1.2 Caja neta (45.447 − 9.523), M$", 45447 - 9523, 0, False, "35.924"),
    ("§1.2 Peso automoción 3T (20.560 / 28.046)", pct(20560, 28046), 0, False, "~73"),
    # §3 / §4
    ("§3 China FY25 (20.962 / 94.827)", pct(20962, 94827), 1, False, "~22,1"),
    ("§3 China H1 26 (8.859 / (78.669 − 28.046))", pct(8859, H1_26_REV), 1, False, "17,5"),
    ("§4.2 Créditos / BO FY25 (1.993 / 4.355)", pct(1993, 4355), 1, False, "45,8 (46 en texto)"),
    ("§4.2 Créditos / BO FY25, entero", pct(1993, 4355), 0, False, "46"),
    ("§4.6 Capex 2026 / FY25 (20.000 / 8.527), veces", 20000 / 8527, 2, False, "más del doble"),
    # §4.1 plan del CEO 2025: base del porcentaje (veredicto v2 §5)
    ("§4.1 Acciones previas a la emisión (portada − 423.743.904)", SHARES_COVER - SHARES_CEO2025, 0, False, "(nueva)"),
    ("§4.1 Plan CEO / capital previo a la emisión", pct(SHARES_CEO2025, SHARES_COVER - SHARES_CEO2025), 1, False, "~12"),
    ("§4.1 Plan CEO / portada 15-oct-2026", pct(SHARES_CEO2025, SHARES_COVER), 1, False, "(nueva)"),
    # §5 ilustrativo
    ("§5 Ilustrativo 30 × 3.794, M$", 30 * 3794, 0, False, "~114.000"),
]


def main():
    print(f"{'Cifra':<62} {'sin redondear':>16} {'en 01':>10}  publicada v2")
    for label, val, d, sign, pub in ITEMS:
        out = es(r(val, d), d, sign)
        print(f"{label:<62} {val:>16.4f} {out:>10}  {pub}")

    # Comprobación contra el documento: patrones de las cifras corregidas en v3.
    text = DOC.read_text(encoding="utf-8")
    body = text.split("## Registro de cambios v2")[0]
    checks = [
        ("Servicios FY25 var", r"12\.530 \| \+([\d,]+) %", es(r(var(12530, 10534), 1), 1)),
        ("Plan CEO / previo", r"([\d,]+) % del capital previo a la emisión",
         es(r(pct(SHARES_CEO2025, SHARES_COVER - SHARES_CEO2025), 1), 1)),
        ("Plan CEO / portada", r"([\d,]+) % de las 3\.952\.757\.946",
         es(r(pct(SHARES_CEO2025, SHARES_COVER), 1), 1)),
    ]
    bad = 0
    print("\nComprobación en 01-negocio.md:")
    for name, rx, exp in checks:
        m = re.search(rx, body)
        got = m.group(1) if m else None
        st = "OK" if got == exp else ("NO ENCONTRADA" if got is None else "MISMATCH")
        bad += st != "OK"
        print(f"  {st:<14} {name}: doc={got} script={exp}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
