# Agentes de finanzas — laboratorio

Proyecto de práctica con los agentes de [agency-agents](https://github.com/msitarzewski/agency-agents):
análisis de empresas cotizadas en fases, cada una hecha por un subagente distinto y auditada por el
Reality Checker. Es un ejercicio de aprendizaje, no asesoramiento de inversión.

## Estructura

- `.claude/agents/` — subagentes del proyecto (copiados del repo agency-agents).
- `.claude/skills/` — flujos reutilizables: `analizar-empresa` y `ronda-correccion`.
- `empresas/<ticker>/` — un análisis por empresa:
  - `docs/` — 01-negocio, 02-financieros, 03-valoracion, 04-tesis, 05-veredicto(-vN).
  - `data/` — CSV y Excel generados por los scripts.
  - `scripts/` — todos los cálculos (`faseN_*.py`).
  - `fuentes/` — registro de fuentes.
- `herramientas/verificar.py` — ejecuta los scripts de una empresa y falla si hay cifras que no cuadran.

## Fases y agentes

| Fase | Agente | Entrega |
|---|---|---|
| 1 Negocio | Investment Researcher | `docs/01-negocio.md`, `fuentes/fuentes.md` |
| 2 Financieros | Financial Analyst | `data/<ticker>_financials.csv`, `scripts/fase2_*.py`, `docs/02-financieros.md` |
| 3 Valoración | Financial Analyst | `scripts/fase3_dcf.py`, `data/dcf.xlsx`, `docs/03-valoracion.md` |
| 4 Tesis | Investment Researcher | `docs/04-tesis.md`, `scripts/fase4_*.py` |
| 5 Verificación | Reality Checker | `docs/05-veredicto*.md`, `scripts/fase5*.py` |

La sesión principal actúa como **orquestador**: delega cada fase en su subagente y no hace el trabajo ella misma.

## Reglas para todos los agentes

1. **Fuentes:** cada cifra lleva su fuente (documento, sección o tabla, URL y fecha). Preferir fuentes
   primarias (SEC EDGAR, informes de la empresa). Lo que no se pueda verificar se marca `SIN VERIFICAR`;
   nunca se rellena de memoria.
2. **Cálculos:** toda la aritmética va en scripts de `scripts/`, nunca a mano. Las cifras de los documentos
   se copian de la salida de los scripts, sin redondear dos veces.
3. **Traspasos:** cada fase lee las entregas anteriores antes de empezar. Si encuentra un error en una fase
   anterior, lo documenta y **no edita los documentos de otra fase**: lo devuelve al orquestador.
4. **Correcciones:** cada ronda de corrección añade al final del documento una sección
   `## Registro de cambios vN` con cada punto del veredicto y lo que se cambió (o por qué no). Discrepar
   del veredicto está permitido solo con evidencia nueva.
5. **Fuentes nuevas en rondas paralelas:** cada agente escribe en `fuentes/nuevas_faseN_vN.md`, nunca en
   `fuentes.md` a la vez que otro.
6. **Idioma:** documentos en español. Nada de lenguaje de compra o venta: escenarios y rangos.

## Git

- Una rama por ronda de trabajo: `analisis/<ticker>`, `correccion/<ticker>-vN`.
- Un commit por fase, con el mensaje `<ticker> faseN: <qué>`.
- El veredicto del Reality Checker va en la descripción del PR.
- Antes de cada commit con cifras: `python herramientas/verificar.py <ticker>`.

## Entorno

- Python 3.11+ con `pip install -r requirements.txt`.
- `fase3_dcf.py` recalcula el Excel con LibreOffice si está instalado; si no, guarda el Excel sin
  recalcular (o exporta `DCF_NO_RECALC=1`).
