# Fuentes nuevas — Fase 2 (Financieros), v1

Fecha de consulta: **2026-10-25**. Todos los documentos ya figuran en [`fuentes.md`](fuentes.md) con los mismos IDs (P2, P3, P5, P6). Lo nuevo de esta fase son las **secciones y páginas** leídas, que la fase 1 no había usado. No se ha usado ninguna fuente secundaria.

**Método de acceso.** Descarga directa del HTML de EDGAR (`curl`) y conversión a texto con un script propio. Los números de página se tomaron del folio impreso en cada página HTML: en el 424B4 son los folios "F-n" y los números del cuerpo; en los 10-Q, el número al pie de página. **Diferencia de criterio con la fase 1:** la fase 1 cita, por ejemplo, "Prospectus Summary p. 4", "tabla p. 26-27" y "Note 3 p. F-23". Con el folio impreso, esas tablas están en las p. 3, 22-24 y F-22 (desagregación de ingresos; la concentración de clientes sí está en F-23). Las cifras coinciden; solo cambia la referencia de página.

| ID | Documento | Secciones nuevas usadas en la fase 2 (página = folio impreso) | URL |
|---|---|---|---|
| P2 | Folleto 424(b)(4), acc. 0001628280-26-042639 | Balance F-4; cuenta de resultados F-5; patrimonio F-7; flujos de caja F-8 y suplementarios F-9; caja y caja restringida F-12; Note 3 desagregación de ingresos F-22 y concentración F-23; Note 10 Deuda F-29; Note 19 Segmentos F-57 (FY2025) y F-58 (FY2024, FY2023); flujos 1T26 F-67/F-68; Note 3 1T26 F-71; segmentos 1T26 F-94; Summary Historical Consolidated Financial and Operating Data p. 22-24; conciliaciones no GAAP p. 119 (EBITDA ajustado) y p. 120-121 (por segmento) | https://www.sec.gov/Archives/edgar/data/1181412/000162828026042639/spaceexplorationtechnologi.htm |
| P3 | 10-Q 3T 2026, acc. 0001628280-26-066880 | Portada p. 1; balance p. 4; resultados p. 5; patrimonio p. 7-8; flujos p. 9; Note 3 p. 13; Note 9 Deuda p. 17; Note 12 p. 25-26; Note 13 BPA p. 27; Note 18 Segmentos p. 32-34; MD&A SI p. 48; no GAAP p. 50-52 | https://www.sec.gov/Archives/edgar/data/1181412/000162828026066880/spcx-20260930.htm |
| P5 | 8-K 20-oct-2026, Ex. 99.1, acc. 0001628280-26-066482 | "Third Quarter Financial Highlights" p. 4 (ingresos, resultado operativo, EBITDA ajustado y capex por segmento del 3T26, 2T26, 3T25, 9M26 y 9M25). Solo contraste: coincide con P3/P6 | https://www.sec.gov/Archives/edgar/data/1181412/000162828026066482/spaceexplorationtechnologi.htm |
| P6 | 10-Q 2T 2026, acc. 0001628280-26-052535 | Resultados p. 5; flujos (6M) p. 9; Note 3 desagregación p. 13 y concentración p. 14; Note 18 Segmentos p. 30-32; no GAAP p. 46-47 | https://www.sec.gov/Archives/edgar/data/1181412/000162828026052535/spcx-20260630.htm |

**Fuentes buscadas y no disponibles**
- FY2021 y FY2022: el folleto solo incluye FY2023-FY2025 auditados (índice F-1). SpaceX no presentaba informes a la SEC antes de la OPV. **SIN VERIFICAR**; no se rellenan.
- Balance a 31-dic-2023 (salvo la caja de F-12) y a 30-sep-2025: no se publican en P2 ni en P3.
- 9M 2024: no publicado, así que no hay TTM del año anterior.
