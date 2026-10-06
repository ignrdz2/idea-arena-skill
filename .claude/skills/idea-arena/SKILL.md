---
name: idea-arena
description: >-
  Genera y filtra ideas de tesis de ingeniería (modalidad emprendedurismo) con
  un pipeline de sub-agentes basado en /arena: investigación por sector con
  evidencia cuyas URLs se verifican, generación con estrategias distintas,
  filtro duro, chequeo de alcance y deduplicación, un torneo de eliminación
  con ataques de personas y juez ciego, y una shortlist con preguntas de
  validación. Usalo cuando el usuario escriba /idea-arena, pida ideas de
  tesis con este pipeline, o quiera correr el piloto, el dry-run, la
  calibración del juez o la profundización de una idea.
argument-hint: "[--pilot] [--dry-run] [--seed S] | calibrate | deepen <id> | status | doctor | audit"
---

# idea-arena (acceso del proyecto)

Este archivo solo registra el comando `/idea-arena` en este proyecto. El skill completo, con su
herramienta, sus briefs y su configuración, vive en `skills/idea-arena/` de este repo, para que haya
una sola copia.

1. Leé `skills/idea-arena/SKILL.md` (ruta relativa a la raíz del repo, tu directorio de trabajo) y
   seguilo al pie de la letra.
2. Los argumentos que escribió el usuario son: `$ARGUMENTS`. Usalos donde ese archivo habla de los
   argumentos.
