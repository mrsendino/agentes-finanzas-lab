---
name: analizar-empresa
description: Lanza el análisis en 5 fases de una empresa cotizada con los subagentes del proyecto (Investment Researcher, Financial Analyst, Reality Checker). Úsala cuando el usuario pida analizar una empresa nueva o escriba /analizar-empresa <ticker>.
---

# Analizar una empresa

Argumento: el ticker o nombre de la empresa (p. ej. `NVDA`). Carpeta: `empresas/<ticker en minúsculas>/`.

Actúa como **orquestador**: no hagas el análisis tú. Delega cada fase en el subagente indicado, pásale
las rutas de las entregas anteriores y las reglas de `CLAUDE.md`. Usa `empresas/tesla/` como ejemplo
de formato y nivel de detalle, no como fuente de datos.

## Antes de empezar

1. Crea la rama `analisis/<ticker>` desde `main`.
2. Crea `empresas/<ticker>/{docs,data,scripts,fuentes}`.

## Fases

1. **Investment Researcher** → `docs/01-negocio.md` y `fuentes/fuentes.md`: modelo de negocio por
   segmentos, ventajas competitivas, competidores y riesgos; qué parte del valor depende de negocios
   que aún no generan ingresos.
2. **Financial Analyst** → `data/<ticker>_financials.csv`, `scripts/fase2_ratios.py` y
   `docs/02-financieros.md`: últimos 5 ejercicios y TTM, con fuente por celda. Si una cifra contradice
   la fase 1, dilo explícitamente.
3. **Financial Analyst** → `scripts/fase3_dcf.py`, `data/dcf.xlsx` y `docs/03-valoracion.md`: DCF con
   3 escenarios, sensibilidad WACC × crecimiento terminal, DCF inverso y múltiplos frente a
   comparables.
4. **Investment Researcher** → `docs/04-tesis.md`: tesis alcista y bajista con la misma profundidad,
   señales observables con umbral y abogado del diablo contra el caso base de la fase 3. Sus scripts
   deben importar el modelo de la fase 3, no copiar cifras.
5. **Reality Checker** → `docs/05-veredicto.md` y `scripts/fase5_cifras.py`: un comprobador que cruce
   cada cifra de los documentos con la salida de los scripts (con una línea final
   `TOTAL: ... MISMATCH n ...`), una muestra aleatoria de 10 cifras contra su fuente (10 más si pasan
   todas) y el veredicto APTO / NECESITA TRABAJO con la lista de devoluciones por fase.

## Después de cada fase

- Commit con el mensaje `<ticker> faseN: <resumen>`.
- Para y enséñale al usuario un resumen de 5 líneas. Espera su OK antes de seguir, salvo que haya pedido
  hacerlo todo seguido.

## Al terminar

- Ejecuta `python herramientas/verificar.py <ticker>`.
- Añade la empresa a la tabla del `README.md`.
- Ofrece abrir un PR con el veredicto en la descripción.
