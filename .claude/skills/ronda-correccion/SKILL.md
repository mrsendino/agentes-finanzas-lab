---
name: ronda-correccion
description: Aplica el último veredicto del Reality Checker a un análisis existente, fase por fase, y lanza una nueva verificación. Úsala cuando el usuario pida corregir un análisis o escriba /ronda-correccion <empresa>.
---

# Ronda de corrección

Argumento: la empresa (p. ej. `tesla`). Carpeta: `empresas/<empresa>/`.

Actúa como **orquestador**: no corrijas tú. Cada fase la corrige su propio subagente.

## Pasos

1. **Prepara.** Localiza el último veredicto (`docs/05-veredicto*.md` con la versión más alta) y su
   lista de devoluciones por fase. Llama N a la nueva versión. Crea la rama `correccion/<empresa>-vN`.
2. **Ordena por dependencias.**
   - Primero, las fases de las que otras copian cifras: normalmente la 2 antes que la 3, y la 3 antes
     que la 4.
   - Las fases que solo tocan su propio documento pueden ir en paralelo.
3. **Delega en cada subagente.** Encárgale:
   - aplicar solo los puntos de su fase;
   - editar solo sus ficheros;
   - escribir las fuentes nuevas en `fuentes/nuevas_faseX_vN.md`;
   - añadir al final de su documento `## Registro de cambios vN`, con cada punto y lo que se cambió
     (o por qué no).
   Puede discrepar del veredicto solo con evidencia nueva.
4. **Propaga.** Si una corrección cambia cifras que usan otras fases, vuelve a lanzar esas fases para
   sincronizarlas, aunque el veredicto no las mencionara.
5. **Commit.** Uno por fase: `<empresa> faseN vN: <qué>`.
6. **Verifica de nuevo.** Pide al Reality Checker:
   - actualizar los valores esperados de sus comprobadores (nunca los modelos);
   - una tabla de trazabilidad (devolución → RESUELTO / PARCIAL / NO / DISPUTADO, con evidencia);
   - reconocer dónde se equivocó;
   - escribir `docs/05-veredicto-vN.md` sin tocar los veredictos anteriores.
7. **Cierra.** Ejecuta `python herramientas/verificar.py <empresa>`, resume al usuario el veredicto
   (nota antes y después) y ofrece abrir un PR.
