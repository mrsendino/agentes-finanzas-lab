"""Fase 5 (Reality Checker) - muestreo aleatorio de cifras para verificar contra su fuente citada.

Catálogo de cifras extraídas a mano de docs/01..04 con la fuente que el propio documento cita.
Se sortean 10 (ronda 1) y, si las 10 pasan, otras 10 distintas (ronda 2), con semilla impresa.
Uso: python3 scripts/fase5_muestreo.py [semilla]
"""
import random
import sys

P1 = "https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm"
P2 = "https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066775/tsla-20260930.htm"
P3 = "https://www.sec.gov/Archives/edgar/data/0001318605/000162828026049270/tsla-20260630.htm"
P4 = "https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm"
P6 = "https://www.sec.gov/Archives/edgar/data/1318605/000162828026000016/exhibit9914.htm"
K22 = "https://www.sec.gov/Archives/edgar/data/1318605/000095017023001409/tsla-20221231.htm"
D24 = "https://www.sec.gov/Archives/edgar/data/1318605/000162828025002993/exhibit991.htm"
R45 = "https://www.sec.gov/Archives/edgar/data/1318605/000162828025003063/R45.htm"
Q325 = "https://www.sec.gov/Archives/edgar/data/1318605/000162828025045968/tsla-20250930.htm"
S1 = "https://sec-api.io/insights/financial-analysis-of-tesla-fy2025-and-the-first-half-of-2026"
S2 = "https://electrek.co/2026/10/21/tesla-tsla-q3-2026-financial-results/"
S7 = "https://insideevs.com/news/783252/tesla-byd-global-sales-2025/"
S9 = "https://www.energy-storage.news/chinese-system-integrators-capture-76-of-global-bess-market-as-competition-intensifies/"
S10 = "https://www.meridiancp.com/insights/tesla-shareholders-approve-2025-ceo-performance-award/"
T5 = "https://secure.businesswire.com/news/home/20260204947622/en/Uber-Announces-Results-for-Fourth-Quarter-and-Full-Year-2025"
M4 = "https://www.mortgagenewsdaily.com/treasury/10yr"
M6 = "https://pages.stern.nyu.edu/~adamodar/New%5FHome%5FPage/datafile/Betas.html"

# (id, cifra, documento, fuente citada, URL)
CATALOGO = [
    ("F01", "Entregas FY2025 1.636.129", "01 §1.1", "P6", P6),
    ("F02", "Producción FY2025 1.654.667", "01 §1.1", "P6", P6),
    ("F03", "Almacenamiento FY2025 46,7 GWh", "01 §1.1", "P6", P6),
    ("F04", "Ingresos 3T26 28.046 M$", "01 §1.2", "P4", P4),
    ("F05", "Créditos regulatorios 3T26 113 M$ (3T25 417)", "01 §1.2", "P4", P4),
    ("F06", "Margen bruto energía 3T26 33,1 % (BB 954)", "01 §1.2", "P4", P4),
    ("F07", "FCF 3T26 1.531 M$ / capex 4.732 M$", "01 §1.2", "P4", P4),
    ("F08", "Entregas 3T26 486.532", "01 §1.2", "P4", P4),
    ("F09", "Suscripciones FSD activas 1,74 M (+67 %)", "01 §2", "P4", P4),
    ("F10", "Capacidad Shanghái >950.000", "01 §2", "P4", P4),
    ("F11", "Ingresos 9M26 78.669 M$ (9M25 69.926)", "01 §1.2", "P2", P2),
    ("F12", "Provisión de garantías 10.138 M$ (8.075)", "01 §4", "P2 Note 1", P2),
    ("F13", "Compra de SpaceX 2.002 M$ en 1S26", "01 §4", "P3", P3),
    ("F14", "Deuda principal 8.180 M$ a 31-dic-2025", "01 §2", "P1 Item 1A", P1),
    ("F15", "Plan CEO 2025: 423,7 M acciones, 12 tramos", "01 §4", "S10", S10),
    ("F16", "BYD 2,26 M VE en 2025", "01 §3", "S7", S7),
    ("F17", "Integradores chinos 76 % del mercado BESS", "01 §3", "S9", S9),
    ("F18", "I+D 3T26 2.760 M$ / SBC 1.170 M$", "01 §1.2", "S2", S2),
    ("F19", "Ingresos FY2021 53.823 M$", "02 §2", "10-K FY2022", K22),
    ("F20", "Créditos regulatorios FY2022 1.776 M$", "02 §2", "10-K FY2022", K22),
    ("F21", "Beneficio operativo FY2023 8.891 M$", "02 §3", "Deck Q4 2024", D24),
    ("F22", "Capex FY2024 11.339 M$", "02 §4", "Deck Q4 2024", D24),
    ("F23", "Créditos regulatorios FY2024 2.763 M$", "02 §2", "R45 10-K FY2024", R45),
    ("F24", "Ingresos 9M25 69.926 M$ / capex 9M25 6.134", "02 §1.1 (CSV)", "10-Q 3T25", Q325),
    ("F25", "Caja + inv. CP 30-sep-26 45.447 (17.853 + 27.594)", "02 §8.1", "P2", P2),
    ("F26", "Deuda total 30-sep-26 9.523 (1.387 + 8.136)", "02 §5", "P2", P2),
    ("F27", "Patrimonio neto 30-sep-26 89.289 M$", "02 §5", "P2", P2),
    ("F28", "Capex 9M26 13.014 M$", "02 §4", "P2", P2),
    ("F29", "Opex 3T26 4.776 vs 3.430; I+D 2.761 vs 1.630", "02 §3", "P4", P4),
    ("F30", "D&A 3T26 1.852 M$", "02 §4 / 03 §2.1", "P4", P4),
    ("F31", "Acciones portada 3.952.757.946", "03 §1", "P2", P2),
    ("F32", "Media diluida 3T26 3.541 M / básica 3.240 M", "03 §1", "P2", P2),
    ("F33", "Bono 10 años 4,967 %", "03 §1", "M4", M4),
    ("F34", "Beta desapalancada Auto & Truck 1,31", "03 §1", "M6", M6),
    ("F35", "Uber FY2025 13.567 M viajes", "04 §2.3", "T5", T5),
    ("F36", "SpaceX: plusvalía no realizada 863 M$ 9M26", "04 §3.3", "P2", P2),
    ("F37", "Acciones en balance 3.751 M a 31-dic-25", "04 §3.2", "P2", P2),
    ("F38", "Cybercab capacidad >125,000", "01 §5 / 04 §2.2", "P4", P4),
    ("F39", "Ingresos FY2025 94.827 M$", "01 §1.1 / 02", "S1", S1),
    ("F40", "Beneficio neto atribuible FY2025 3.794 M$", "01 §1.1", "S1", S1),
]


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20261024
    rng = random.Random(seed)
    print(f"Semilla: {seed} | catálogo: {len(CATALOGO)} cifras")
    orden = rng.sample(CATALOGO, len(CATALOGO))
    for ronda, bloque in ((1, orden[:10]), (2, orden[10:20])):
        print(f"\n--- Ronda {ronda} ---")
        for c in bloque:
            print(" | ".join(c))


if __name__ == "__main__":
    main()
