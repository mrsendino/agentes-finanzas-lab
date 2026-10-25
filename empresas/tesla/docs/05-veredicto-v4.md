# 05 — Veredicto de verificación v4 (Reality Checker, mini-ronda)

**Fecha:** 2026-10-25 · **Rol:** Fase 5, *Reality Checker*. Por defecto, el estado es NECESITA TRABAJO salvo prueba abrumadora en contra · **Objeto:** 04 v4 (rama `correccion/tesla-v4`, commit `49e6b94`), con 01-03 sin cambios desde v3 (`673dee4`) · **Alcance:** comprobar la devolución M-v3-1 de [05-veredicto-v3.md](05-veredicto-v3.md) §8, que el cambio de `fase4_opcionalidad.py` no altera ninguna otra cifra y que se cumple el criterio de APTO de v2 §8 / v3 §8. **No es una recomendación de inversión.** Este documento no modifica 01-04 ni los veredictos anteriores.

**Scripts de esta fase:** los mismos de v3, **sin cambios** (ninguna expectativa necesitaba actualizarse; ver §1). Se ejecutan con `PYTHONIOENCODING=utf-8 PYTHONUTF8=1`. Ninguno escribe en `data/` ni en `docs/`; `fase3_dcf.py` solo se ejecuta en copias temporales (el árbol de trabajo queda limpio tras todas las ejecuciones).

---

## 0. Veredicto

### **APTO** · Calificación: **A** (v3: A−; v2: B+; v1: B−)

**Lo que está bien** (con evidencia):
- `python herramientas/verificar.py tesla` → **"✓ Todo cuadra"**. `fase5v2_cifras.py`: **577 cifras: 577 OK, 0 DOBLE REDONDEO, 0 MISMATCH, 0 NO ENCONTRADA** (v3: 576 OK, 1 MISMATCH).
- **M-v3-1 resuelto.** 04 §1 dice "diferencial −6,0 pp". Valor exacto, recalculado por mí desde `tesla_financials.csv` con la fórmula de `fase2_ratios.py`: ROIC A TTM = 3.466 × 0,79 / ((53.365 + 46.025) / 2) = **5,50989 %**; WACC0 de `fase3_dcf.py` = **11,55480 %**; diferencial = **−6,0449 pp → −6,0 pp**.
- **El cambio del script no mueve ninguna otra cifra.** Ejecuté `fase4_opcionalidad.py` de v3 (worktree en `673dee4`) y de v4 (`49e6b94`): 228 líneas cada una y **solo 2 difieren**, las dos del diferencial (§11: "-6.1%" → "-6.0%"; §14: "−6,1 pp" → "−6,0 pp"). Coincide exactamente con lo que declara el registro v4 de 04.
- `fase5_consistencia.py`: **0 MISMATCH (23 de 23)**; `ratios.csv` y `checks.csv` regenerados idénticos a los del proyecto.
- El diff `correccion/tesla-v3..49e6b94` toca solo `docs/04-tesis.md` y `scripts/fase4_opcionalidad.py`. 01, 02, 03, `data/` y `fuentes/` no cambian.

**Matiz (no es devolución):** −6,0449 está a 0,005 pp del umbral de redondeo (−6,05). Es correcto hoy, pero cualquier cambio de inputs en 02 o 03 puede volver a moverlo a −6,1; como ahora se lee de su fuente, la §14 lo recogería sola.

---

## 1. Re-ejecución y expectativas v3 → v4

| Script | Resultado v4 |
|---|---|
| `fase4_opcionalidad.py` | rc = 0. Salida idéntica a v3 salvo las 2 líneas del diferencial. Los nuevos `assert` (precio, caja neta, ingresos, EBIT, créditos, BN, SBC TTM y FY24, FCF, plan CEO, energía FY25, ROIC a 4 decimales frente a `ratios.csv`, ejercicio 2018 a 1 decimal frente a 02) pasan |
| `fase5v2_cifras.py` | 577 / 577 OK. La cifra de M-v3-1 se compara con `(ROIC exacto − f3.WACC0) × 100` calculado por el comprobador, no con un número fijo |
| `fase5_consistencia.py` | 0 MISMATCH (23) |
| `fase5v2_coherencia.py` | Igual que v3: 8 apariciones sin etiqueta (falsos positivos ya revisados en v3 §5) y 7 referencias de 02 sin versión (6 neutras + la cosmética de 02 §1.2) |
| `fase5v3_propagacion.py` | Igual que v3: 90 textos buscados, 10 ETIQUETADA, 7 REVISAR (los mismos 7 falsos positivos) |

**Expectativas:** ninguna cambia. Las de `fase5v2_cifras.py` salen de la ejecución viva y las de `fase5_consistencia.py` no dependen del diferencial. Por eso no hay registro v3 → v4 en las cabeceras de los comprobadores.

**Revisión del cambio de Fase 4.** `ROIC_A_TTM` se calcula con la misma fórmula que `fase2_ratios.py` (importa solo `load()` y `TAX_NORM`; `main()` va bajo `__main__` y no escribe nada, comprobado con `git status` limpio). Las demás constantes se leen de `ratios.csv` vía `f3.r` con un `assert` frente a los valores de v3: el script fallará de forma visible si 02 cambia, en vez de usar un valor desactualizado. Es el comportamiento correcto.

---

## 2. Trazabilidad de las devoluciones de v3 (05-veredicto-v3 §8)

| # | Devolución v3 | Lo que hizo la fase | Verificación de Fase 5 v4 | Estado |
|---|---|---|---|---|
| **M-v3-1** (prio. 1, Fase 4) | ROIC A TTM a precisión completa en el script y −6,0 pp en 04 §1 | ROIC calculado desde NOPAT / capital medio; 04 §1 "−6,0 pp"; registro v4 corrige la afirmación errónea del registro v3 sin reescribirlo | Diferencial exacto −6,0449 → −6,0 ✓; catálogo OK; salida v3 vs v4: solo 2 líneas cambian ✓ | **RESUELTO** |
| Opc. Fase 1 | G33 (01 §5): ">500 vehículos" era la flota de enero de 2026 | Sin cambios (fuera de la mini-ronda) | 01 no cambia | **NO** (opcional) |
| Opc. Fase 2 | 02 §1.2: "marcadas como 'solo secundaria'" → indicar que 01 v2 retiró las marcas | Sin cambios | `fase5v2_coherencia.py` §3 sigue marcando 02:60 | **NO** (opcional, cosmético) |
| Opc. Fase 3 | Copia fechada de las páginas de mercado en `fuentes/` | Sin cambios | No hay archivo nuevo en `fuentes/`. WebFetch hoy: MarketChameleon "TSLA has a beta of 1.84" ("Data as of October 23, 2026"); TipRanks "Beta 1.84" (`dateModified` 24-oct-2026) | **NO** (opcional) |
| Opc. Orquestador | Recalcular `dcf.xlsx` o decirlo en el PR; `verificar.py` debería tratar NO ENCONTRADA > 0 como fallo | Sin cambios | `dcf.xlsx`: 485 fórmulas, **0 valores cacheados**; sigue sin LibreOffice (`soffice` no está en el PATH ni en `C:\Program Files\LibreOffice`). `verificar.py` sin cambios | **NO** (opcional) |

**Recuento:** la única devolución obligatoria está **RESUELTA**; las 4 opcionales siguen abiertas y ninguna afecta a cifras.

---

## 3. Criterio de APTO (v2 §8 / v3 §8)

| Criterio | Resultado v4 |
|---|---|
| Cifras: 0 MISMATCH / 0 DOBLE REDONDEO / 0 NO ENCONTRADA | **577 / 577 OK** ✓ |
| Consistencia: 0 MISMATCH | **0 de 23** ✓ |
| Coherencia entre fases (sin cifras sustituidas vigentes sin etiqueta) | ✓ (igual que v3; el −6,1 que queda en 04 es la fila del registro v3, histórica y corregida en el registro v4) |
| Beta de 03 §1 reproducible | ✓ 1,84 / 1,84 (WebFetch 25-oct-2026) |
| `verificar.py tesla` | **"✓ Todo cuadra"** ✓ |

**`dcf.xlsx` sin valores cacheados (revaloración).** Sigue igual que en v3: las 485 fórmulas no han cambiado (este ciclo no toca `fase3_dcf.py` ni el libro). No bloquea, porque CLAUDE.md lo permite y 03 lo declara. Pero para el merge mantengo la recomendación: **decirlo en la descripción del PR** ("abrir en Excel/LibreOffice para recalcular; lecturas con `data_only=True` devuelven celdas vacías") o recalcularlo en un equipo con LibreOffice.

---

## 4. Dónde me equivoqué en v3

1. **Ofrecí una corrección que reintroducía el defecto.** En §8 propuse "leer el ROIC A TTM de `ratios.csv` (`roic_A_neto_caja`) **o** calcularlo". `ratios.csv` guarda ese ratio a 4 decimales (0,0551): leerlo de ahí es otro redondeo intermedio, el mismo patrón que criticaba. Aquí el resultado habría sido igual (−6,0448), pero por casualidad. Fase 4 lo vio y eligió la precisión completa con un `assert` frente a la fila de 4 decimales. Debí pedir solo el cálculo completo.
2. **Subestimé el alcance del cambio.** Dije que la corrección era "una celda de 04 y una línea del script". Fase 4 sustituyó además 11 constantes copiadas a mano. Es un cambio mejor que el que pedí; lo he verificado comparando las dos salidas completas, no fiándome del registro.

---

## 5. Comparación v3 → v4

| Indicador | v3 | **v4** |
|---|---|---|
| Cifras contra el script | 577: 576 OK, 1 MISMATCH | **577: 577 OK** |
| `fase5_consistencia.py` | 0 MISMATCH (23) | **0 MISMATCH (23)** |
| Diferencial ROIC A − WACC inicial (04 §1) | −6,1 pp | **−6,0 pp** |
| Constantes de 02/03 copiadas a mano en fase4 | ROIC, precio, caja, ingresos, EBIT, créditos, BN, SBC, FCF, plan CEO, energía | **Leídas de su fuente con `assert`** (queda el ejercicio 2018, justificado) |
| `dcf.xlsx` | Sin caché | **Sin caché** (igual) |
| Opcionales abiertos | 4 | **4** |
| Conclusión | Negocio reportado ~10-56 $ frente a 372,22 $ | **Sin cambios** |
| Calificación | A− | **A** |

**Por qué A y no más:** `dcf.xlsx` sigue sin valores cacheados; los datos de mercado (beta, múltiplos de TipRanks) no tienen copia archivada y el PER de Nvidia ya no se reproduce (v3 §4.2); quedan dos matices de redacción (G33 en 01 y 02 §1.2); y `verificar.py` no trata NO ENCONTRADA como fallo.

**Por qué sube de A−:** se cumple entero el criterio de APTO, y la causa del último error (constantes copiadas a mano en Fase 4) se ha eliminado, no solo el síntoma.

---

*Reproducibilidad:* `python herramientas/verificar.py tesla`, `python scripts/fase5_consistencia.py`, `python scripts/fase5v2_cifras.py [-v]`, `python scripts/fase5v2_coherencia.py` y `python scripts/fase5v3_propagacion.py`, con `PYTHONIOENCODING=utf-8 PYTHONUTF8=1`. La comparación v3/v4 de `fase4_opcionalidad.py` se hizo con dos worktrees (`673dee4` y `49e6b94`) y `diff` de la salida estándar. Sin fuentes nuevas de Fase 5: no se crea `fuentes/nuevas_fase5_v4.md`.
