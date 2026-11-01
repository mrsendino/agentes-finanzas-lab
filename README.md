# Agentes de finanzas — laboratorio

Práctica de orquestación multi-agente con [agency-agents](https://github.com/msitarzewski/agency-agents) y Claude Code:
cada empresa se analiza en 5 fases, cada fase la hace un subagente especializado y un Reality Checker
audita el resultado y devuelve el trabajo a la fase responsable.

> Ejercicio de aprendizaje. Nada de lo que hay aquí es una recomendación de inversión.

## Empresas analizadas

| Empresa | Estado | Último veredicto |
|---|---|---|
| [Tesla (TSLA)](empresas/tesla/docs) | v4, completo | APTO, nota A |
| [SpaceX (SPCX)](empresas/spacex/docs) | v1, fases 1-4 | Pendiente de fase 5 (Reality Checker) |
| [AMD (AMD)](empresas/amd/docs) | v1, fase 1 | Pendiente de fases 2-5 |

## Cómo funciona

```
Fase 1 Investment Researcher ─► Fase 2 Financial Analyst ─► Fase 3 Financial Analyst (DCF)
                                                                     │
Fase 5 Reality Checker ◄──────── Fase 4 Investment Researcher ◄──────┘
        │
        └─► devuelve correcciones a cada fase (ronda vN) ─► nueva verificación
```

Las reglas comunes de todos los agentes están en [CLAUDE.md](CLAUDE.md).

## Uso

```bash
pip install -r requirements.txt
python herramientas/verificar.py tesla      # recalcula y comprueba las cifras de los documentos
```

En Claude Code, dentro del repo:

- `/analizar-empresa NVDA` — lanza las 5 fases para una empresa nueva.
- `/ronda-correccion tesla` — aplica el último veredicto del Reality Checker.

## Lecciones aprendidas

- Los agentes se auditan bien entre sí, pero las correcciones no viajan hacia atrás solas: hace falta un
  registro de cambios por ronda.
- Ningún agente acierta siempre, tampoco el verificador. Las disputas las resuelve la fuente primaria.
- El fallo más frecuente es copiar cifras a mano entre documentos. Los documentos deben salir de los scripts.
