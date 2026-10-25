# Fuentes nuevas o re-consultadas — Fase 3, ronda v3

Fecha de consulta: 2026-10-25 (WebFetch). Origen: FAIL-v2-1 de [05-veredicto-v2.md](../docs/05-veredicto-v2.md) §4.2 (G19).

| ID | Fuente | URL | Qué dice (literal) | Fecha del dato | Uso en 03 v3 |
|---|---|---|---|---|---|
| M8 (re-consultada) | MarketChameleon, resumen TSLA | https://marketchameleon.com/Overview/TSLA/Summary/ | "TSLA has a beta of 1.84, meaning it tends to be more sensitive to market movements." La página da "Data as of October 23, 2026" en el bloque de cifras clave (no junto a la beta) y un cierre de 372,22 $ del 23-oct-2026 | 23-oct-2026 | Beta de regresión 2 = **1,84** (v2: 1,87, que ya no aparece) |
| TipRanks (re-consultada) | TipRanks, estadísticas TSLA | https://www.tipranks.com/stocks/tsla/statistics | "Stock Price Statistics — Beta 1.84". No hay ningún 1,85 en la página. Metadatos JSON-LD: "dateModified": "Oct 24, 2026" | 24-oct-2026 (modificación de la página) | Beta de regresión 1 = **1,84** (v2: 1,85, que ya no aparece) |

**Notas:**
- Ninguna de las dos páginas indica la ventana ni la frecuencia de la regresión, y ninguna guarda versiones anteriores. Por eso una beta citada de estas fuentes solo se puede reproducir mientras la página no se actualice. Ambas son fuentes secundarias.
- El veredicto v2 daba la cifra de TipRanks (1,85) como confirmada. En la consulta de esta ronda, la página da 1,84 (dos lecturas el 25-oct-2026). Se usa el valor actual de las dos fuentes, por el mismo criterio que pide FAIL-v2-1.
- Desfase de fechas: la beta de TipRanks lleva fecha del 24-oct y el precio de referencia es del 23-oct. Una beta de regresión de varios años no cambia de forma material en un día, así que se acepta el desfase.
