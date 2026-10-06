# runs/

Acá escribe /idea-arena, y solo acá. Cada run es una carpeta `runs/<YYYYMMDD-HHMM>/` (con `-2`,
`-3` si hay dos en el mismo minuto) y `runs/LATEST` apunta al último. Esta carpeta se versiona a
propósito: las fichas, las ideas y los veredictos son el registro de cómo se eligió la tesis.

## Qué hay en un run

```
state.json                      el estado del pipeline (rutas relativas a la raíz del repo)
inputs/                         copia congelada de constraints, config, rúbrica, estrategias, personas y esquemas
prompts/<fase>/<trabajo>.md     el brief exacto que recibió cada sub-agente
evidence/raw/<sector>.json      lo que escribió cada investigador
evidence/fichas.json            las fichas verificadas de la investigación
evidence/fichas_torneo.json     fichas nuevas que trajeron atacantes y defensores, verificadas
evidence/fichas_todas.json      todas juntas: es lo que leen los agentes
evidence/descartadas*.json      las fichas descartadas, con el motivo
evidence/urls.json              el resultado del chequeo HTTP de cada URL
ideas/raw/<generador>.json      lo que escribió cada generador
ideas/<id>.json, ideas/<id>.md  cada idea y su página de 1 hoja (la que leen los jueces)
ideas/meta.json                 de qué generador y estrategia salió cada idea (el juez no lo ve)
filter/                         filtro duro, alcance, duplicados, selección y reporte.md
tournament/bracket.json         el bracket (mismo formato que /arena, más campos propios)
tournament/r<n>/                ataques, defensas, ideas revisadas y veredictos de cada ronda
shortlist.md                    el resultado para humanos
shortlist/                      ranking, rastro de cada idea, preguntas y guiones de entrevista
deepen/<id>/                    profundizaciones pedidas con deepen
scratch/                        espacio temporal de los sub-agentes (no se versiona: ver runs/.gitignore)
```

Un run de calibración tiene `calibration/` y `calibration_report.md` en lugar de las fases.

## Antes de hacer commit

- `python skills/idea-arena/idea_arena.py audit` confirma que nada cambió fuera de `runs/`.
- Los briefs de `prompts/` tienen rutas absolutas de la máquina donde se corrió el run: las
  necesitan los agentes para leer y escribir archivos.
- Las salidas de los agentes se sanean solas: los caracteres de raya larga y semirraya se cambian
  por un guion común, porque un test del repo los prohíbe en todos los archivos.
