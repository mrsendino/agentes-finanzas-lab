"""Fase 5 v2 (segunda verificación) - muestreo aleatorio de cifras de los documentos v2 para contrastar con su fuente.

Catálogo NUEVO: cifras citadas en 01-04 v2 que (a) no se sortearon en v1 (scripts/fase5_muestreo.py, semilla 20261024)
y (b) no están entre las comprobaciones dirigidas de esta ronda (02 §5.1, D&A TTM, FY2021, Wood Mackenzie, BYD HKEX,
capex del CFO). Ronda 1 = 10 cifras; si las 10 pasan, ronda 2 = 10 más. Semilla impresa.
Uso: python3 scripts/fase5v2_muestreo.py [semilla]
"""
import random
import sys

P1 = "https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm"
P2 = "https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066775/tsla-20260930.htm"
P4 = "https://www.sec.gov/Archives/edgar/data/0001318605/000162828026066738/exhibit9914.htm"
D24 = "https://www.sec.gov/Archives/edgar/data/1318605/000162828025002993/exhibit991.htm"
D21 = "https://www.sec.gov/Archives/edgar/data/1318605/000156459022002476/tsla-ex991_209.htm"
R45 = "https://www.sec.gov/Archives/edgar/data/1318605/000162828025003063/R45.htm"
Q325 = "https://www.sec.gov/Archives/edgar/data/1318605/000162828025045968/tsla-20250930.htm"
S1 = "https://sec-api.io/insights/financial-analysis-of-tesla-fy2025-and-the-first-half-of-2026"
S5 = "https://vectorshift.ai/research/companies/tesla/earnings/2025-q4"
S8 = "https://electrek.co/2026/05/13/byd-surpasses-tesla-energy-storage-bess-benchmark-2025/"
S10 = "https://www.meridiancp.com/insights/tesla-shareholders-approve-2025-ceo-performance-award/"
T1 = "https://www.fool.com/earnings/call-transcripts/2026/10/22/tesla-tsla-q3-2026-earnings-call-transcript/"
T3 = "https://amp.claimsjournal.com/news/national/2026/02/12/335668.htm"
T7 = "https://www.cnbc.com/2019/04/22/elon-musk-says-tesla-robotaxis-will-hit-the-market-next-year.html"
T10 = "https://www.boerse-express.com/news/articles/tesla-fuenf-staedte-fuer-robotaxi-rollout-ausstehend-897971"
TR = "https://www.tipranks.com/stocks/{}/statistics"
MC = "https://marketchameleon.com/Overview/TSLA/Summary/"
HG = "https://www.heygotrade.com/en/us-stock/tsla/"

# (id, cifra, documento, fuente citada, URL)
CATALOGO = [
    ("G01", "Efectivo 17.853 + inversiones CP 27.594 a 30-sep-26", "01 §1.2 / 02 §8.1", "P2", P2),
    ("G02", "Créditos 9M26 639 M$ frente a 1.451 M$ en 9M25", "01 §1.2", "P2", P2),
    ("G03", "Servicios y otros 3T26 4.605 / 3T25 3.475; BB 734", "01 §1.2", "P4", P4),
    ("G04", "Automoción 3T26 20.560 / 3T25 21.205", "01 §1.2", "P4", P4),
    ("G05", "Beneficio neto 3T26: 787 atribuible / 804 total", "01 §1.2", "P4", P4),
    ("G06", "Benchmark: Tesla 2.ª con ~10 % frente a ~13 % de BYD", "01 §2", "S8", S8),
    ("G07", "Guía capex 2026 previa '>25.000 M$' (call 1T26)", "01 §2 / 03 §2.1", "T10", T10),
    ("G08", "China FY25 20.962 M$ (~22,1 %); 1S26 8.859 M$ (17,5 %)", "01 §3", "S1", S1),
    ("G09", "Plan CEO 2025 aprobado 6-nov-2025 con >75 % de los votos", "01 §4", "S10", S10),
    ("G10", "BB FY25 automoción 12.361 (17,8 %), energía 3.802 (29,8 %)", "01 §1.1", "S1", S1),
    ("G11", "3T25: saldo 3.224 + 100 emitidas = 3.324 M; básica 3.227 M", "02 §5.1 / 04 §3.2", "10-Q 3T25", Q325),
    ("G12", "Portada 10-K FY25: 3.752.431.984 acciones a 23-ene-2026", "fuentes/nuevas_fase2_v2", "P1", P1),
    ("G13", "Deck Q4 2021: BN 5,5 B$, FCF 5,0 B$, capex 6,5 B$, efectivo 17,6 B$", "02 §1.1 / checks", "D21", D21),
    ("G14", "Provisión fiscal FY2023 −5.001 M$ y 4T23 −5.752 M$", "02 §3", "Deck Q4 2024", D24),
    ("G15", "Other income −592 (4T25), −535 (1T26), +590 (2T26), −117 (3T26)", "02 §3", "P4", P4),
    ("G16", "Créditos regulatorios FY2024 2.763 M$", "02 §2", "R45 10-K FY2024", R45),
    ("G17", "Capex 2T26 5.789 M$", "02 §4", "P4", P4),
    ("G18", "Beta TSLA 1,85 (TipRanks)", "03 §1", "M7", TR.format("tsla")),
    ("G19", "Beta TSLA 1,87 (MarketChameleon)", "03 §1", "M8", MC),
    ("G20", "Nvidia EV/Ventas 21,04; EV/EBITDA 31,43; PER 27,9", "03 §7", "M7", TR.format("nvda")),
    ("G21", "Apple EV/Ventas 9,36; EV/EBITDA 26,97; PER 39,3", "03 §7", "M7", TR.format("aapl")),
    ("G22", "GM EV/Ventas 1,00; EV/EBITDA 9,99; PER 17,2", "03 §7", "M7", TR.format("gm")),
    ("G23", "Other non-current assets 12.599 M$ a 30-sep-26", "fuentes/nuevas_fase3_v2 (03 §6.4)", "P2", P2),
    ("G24", "Cierre previo 374,58 $ (22-oct-2026)", "03 §1", "M2", HG),
    ("G25", "Waymo ~400.000 viajes pagados/semana (feb-2026); objetivo >1 M a fin de 2026", "04 §2.4 / §3.3", "T3", T3),
    ("G26", "Optimus 'production began in Fremont on our high-volume lines'", "04 §2.2 / 01 §5", "P4", P4),
    ("G27", "Cómputo: 400 MW a fin de 2026; Cortex 1 >105 MW, Cortex 2 >120 MW", "04 §2.2", "P4", P4),
    ("G28", "Millas sin supervisión 'nearly two million', x8 en el trimestre", "04 §2.2", "P4", P4),
    ("G29", ">75 % de entregas en Norteamérica con FSD de pago [CALL]", "04 §2.2", "T1", T1),
    ("G30", "ARR FSD ~1.000 M$, CFO 'correct' [CALL]", "04 §2.2", "T1", T1),
    ("G31", "Musk 2019: '>1 million robotaxis on the road next year'", "04 §3.3", "T7", T7),
    ("G32", "Capacidad Shanghái >950.000", "01 §2", "P4", P4),
    ("G33", "Call 4T25: >500 vehículos robotaxi y 'dozens' de ciudades a fin de 2026", "01 §5", "S5", S5),
    ("G34", "SBC trimestral 3T26 1.165 M$ y P4 la vincula al 2025 CEO Performance Award", "02 §3 / 03 §6.3", "P4", P4),
    ("G35", "Toyota EV/EBITDA 9,46; PER 8,8", "03 §7", "M7", TR.format("tm")),
    ("G36", "Elluswamy: Dallas con Cybercab 'next month' [CALL]", "04 §2.2", "T1", T1),
    ("G37", "Musk: Megapack 'almost sold out' para 2027 [MUSK]", "03 §2.3 / 04 §2.2", "T1", T1),
    ("G38", "Megafactory de Texas: 50 GWh", "03 §2.3 / 04 §2.2", "P4", P4),
    ("G39", "Ingresos FY2023 96.773 M$; BO FY2024 7.076 M$", "02 §2-3", "Deck Q4 2024", D24),
    ("G40", "Cybercab en la flota de Austin desde el 3-sep-2026; horario 6:00-24:00", "04 §2.2", "P4", P4),
]


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20261025
    rng = random.Random(seed)
    print(f"Semilla: {seed} | catálogo v2: {len(CATALOGO)} cifras")
    orden = rng.sample(CATALOGO, len(CATALOGO))
    for ronda, bloque in ((1, orden[:10]), (2, orden[10:20])):
        print(f"\n--- Ronda {ronda} ---")
        for c in bloque:
            print(" | ".join(c))


if __name__ == "__main__":
    main()
