"""Fase 5 v3 (tercera verificación) - muestreo aleatorio de cifras de 01-04 v3 para contrastar con su fuente.

Criterio de APTO de 05-veredicto-v2 §8: "un muestreo de 10 cifras con otra semilla, sin FAIL".
Catálogo v3 = (a) las 19 cifras del catálogo v2 (scripts/fase5v2_muestreo.py) que NO salieron en las dos rondas de la
semilla 20261025, más (b) 10 cifras de 01-04 que no estaban en ningún catálogo anterior (v1: fase5_muestreo.py; v2).
Se excluye la beta (G18; G19 ya salió en v2), que se verifica de forma dirigida en 05-veredicto-v3 §4.1.
Semilla por defecto: 20261026 (v1: 20261024; v2: 20261025). Ronda 1 = 10 cifras; si las 10 pasan, ronda 2 = 10 más.
Uso: python scripts/fase5v3_muestreo.py [semilla]
"""
import random
import sys

P1 = "https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm"
P2 = "https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066775/tsla-20260930.htm"
P4 = "https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm"
P6 = "https://www.sec.gov/Archives/edgar/data/1318605/000162828026000016/exhibit9914.htm"
D24 = "https://www.sec.gov/Archives/edgar/data/1318605/000162828025002993/exhibit991.htm"
R45 = "https://www.sec.gov/Archives/edgar/data/1318605/000162828025003063/R45.htm"
S1 = "https://sec-api.io/insights/financial-analysis-of-tesla-fy2025-and-the-first-half-of-2026"
S5 = "https://vectorshift.ai/research/companies/tesla/earnings/2025-q4"
S8 = "https://electrek.co/2026/05/13/byd-surpasses-tesla-energy-storage-bess-benchmark-2025/"
S10 = "https://www.meridiancp.com/insights/tesla-shareholders-approve-2025-ceo-performance-award/"
T1 = "https://www.fool.com/earnings/call-transcripts/2026/10/22/tesla-tsla-q3-2026-earnings-call-transcript/"
T5 = "https://secure.businesswire.com/news/home/20260204"   # URL completa en fuentes/fuentes.md (T5)
T7 = "https://www.cnbc.com/2019/04/22/elon-musk-says-tesla-robotaxis-will-hit-the-market-next-year.html"
T10 = "https://www.boerse-express.com/news/articles/tesla-fuenf-staedte-fuer-robotaxi-rollout-ausstehend-897971"
TR = "https://www.tipranks.com/stocks/{}/statistics"
M5 = "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm"
M6 = "https://pages.stern.nyu.edu/~adamodar/New%5FHome%5FPage/datafile/Betas.html"
GF = "https://www.gurufocus.com/news/9140534/tech-selloff-and-rising-oil-prices-pressure-markets-tesla-tsla-dips-amid-sector-weakness"

# (id, cifra, documento, fuente citada, URL)
CATALOGO = [
    # (a) restos del catálogo v2 no sorteados con la semilla 20261025
    ("G01", "Efectivo 17.853 + inversiones CP 27.594 a 30-sep-26", "01 §1.2 / 02 §8.1", "P2", P2),
    ("G04", "Automoción 3T26 20.560 / 3T25 21.205", "01 §1.2", "P4", P4),
    ("G06", "Benchmark: Tesla 2.ª con ~10 % frente a ~13 % de BYD", "01 §2", "S8", S8),
    ("G07", "Guía capex 2026 previa '>25.000 M$' (call 1T26)", "01 §2 / 03 §2.1", "T10", T10),
    ("G08", "China FY25 20.962 M$ (~22,1 %); 1S26 8.859 M$ (17,5 %)", "01 §3", "S1", S1),
    ("G09", "Plan CEO 2025 aprobado 6-nov-2025 con >75 % de los votos", "01 §4", "S10", S10),
    ("G14", "Provisión fiscal FY2023 −5.001 M$ y 4T23 −5.752 M$", "02 §3", "Deck Q4 2024", D24),
    ("G16", "Créditos regulatorios FY2024 2.763 M$", "02 §2", "R45 10-K FY2024", R45),
    ("G17", "Capex 2T26 5.789 M$", "02 §4", "P4", P4),
    ("G20", "Nvidia EV/Ventas 21,04; EV/EBITDA 31,43; PER 27,9", "03 §7", "M7", TR.format("nvda")),
    ("G22", "GM EV/Ventas 1,00; EV/EBITDA 9,99; PER 17,2", "03 §7", "M7", TR.format("gm")),
    ("G26", "Optimus 'production began in Fremont on our high-volume lines'", "04 §2.2 / 01 §5", "P4", P4),
    ("G30", "ARR FSD ~1.000 M$, CFO 'correct' [CALL]", "04 §2.2", "T1", T1),
    ("G31", "Musk 2019: '>1 million robotaxis on the road next year'", "04 §3.3", "T7", T7),
    ("G32", "Capacidad Shanghái >950.000", "01 §2", "P4", P4),
    ("G33", "Call 4T25: >500 vehículos robotaxi y 'dozens' de ciudades a fin de 2026", "01 §5", "S5", S5),
    ("G34", "SBC trimestral 3T26 1.165 M$ y P4 la vincula al 2025 CEO Performance Award", "02 §3 / 03 §6.3", "P4", P4),
    ("G36", "Elluswamy: Dallas con Cybercab 'next month' [CALL]", "04 §2.2", "T1", T1),
    ("G40", "Cybercab en la flota de Austin desde el 3-sep-2026; horario 6:00-24:00", "04 §2.2", "P4", P4),
    # (b) nuevas en el catálogo v3
    ("H01", "ERP implícito S&P 500 4,20 % a 1-oct-2026 (variante cash yield 3,70 %)", "03 §1", "M5", M5),
    ("H02", "PER TTM de TSLA 410,4 (GuruFocus, 23-oct-2026)", "03 §7", "GF", GF),
    ("H03", "Volkswagen (VWAGY) EV/Ventas 0,94; EV/EBITDA 6,27; PER 6,6", "03 §7", "M7", TR.format("vwagy")),
    ("H04", "BYD (BYDDY) EV/Ventas 1,00; EV/EBITDA 6,37; PER 25,2", "03 §7", "M7", TR.format("byddy")),
    ("H05", "Toyota (TM) EV/Ventas 1,45", "03 §7 / §5", "M7", TR.format("tm")),
    ("H06", "Almacenamiento desplegado FY2025 46,7 GWh; entregas FY2025 1.636.129", "03 §2.3 / 01 §1.1", "P6", P6),
    ("H07", "Gasto en I+D 3T26 2.761 M$ frente a 1.630 M$ en 3T25", "03 §6.3", "P4", P4),
    ("H08", "Ingresos de energía TTM 12.265 M$ (suma de trimestres)", "03 §2.1", "P4", P4),
    ("H09", "Capex TTM 15.407 M$", "03 §2.1", "P4", P4),
    ("H10", "Portada del 10-K FY25: acciones a 23-ene-2026 y deuda principal 8.180 M$ (Item 1A)", "01 §2 (nota)", "P1", P1),
]


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20261026
    rng = random.Random(seed)
    print(f"Semilla: {seed} | catálogo v3: {len(CATALOGO)} cifras")
    orden = rng.sample(CATALOGO, len(CATALOGO))
    for ronda, bloque in ((1, orden[:10]), (2, orden[10:20])):
        print(f"\n--- Ronda {ronda} ---")
        for c in bloque:
            print(" | ".join(c))


if __name__ == "__main__":
    main()
