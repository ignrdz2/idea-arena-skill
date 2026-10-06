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

# idea-arena

Un embudo de ideas de tesis. Sub-agentes investigan problemas reales en Uruguay y LATAM, generan
ideas citando esa evidencia, las filtran y las hacen pelear en un torneo hasta dejar una shortlist
que el equipo valida con gente del mercado. Vos sos el orquestador: no investigás, no generás, no
atacás, no defendés y no juzgás. Nunca elegís una idea.

Los argumentos del usuario: `$ARGUMENTS`. Si ves ese texto literal o está vacío, usá los argumentos
que te pasó el acceso `/idea-arena` del proyecto; si tampoco hay, es un run completo sin semilla.

## La herramienta

Todo pasa por `idea_arena.py`, desde la raíz del repo (donde está `runs/`):

```bash
python skills/idea-arena/idea_arena.py <comando>
```

En macOS o Linux es `python3`. Abajo, `IA` quiere decir ese comando. La herramienta imprime el
comando exacto que sigue: copialo tal cual. El estado vive en `runs/<run>/state.json` y los comandos
lo encuentran por `runs/LATEST`.

## Paso 1: qué pidió el usuario

| argumento | qué hacés |
| --- | --- |
| `--dry-run` (con o sin `--pilot`) | `IA plan [--pilot] [--seed S]` y mostrale la salida. Nada más: no se escribe nada. |
| `--pilot` | run piloto: 3 sectores, unas 10 ideas, bracket de hasta 8. Seguí al paso 2. |
| nada, o solo `--seed S` | run completo. Seguí al paso 2. |
| `calibrate` | `IA calibrate`. Si se niega por placeholders, decile qué archivos completar y pará. Si arranca, andá al paso 4. |
| `deepen <id>` | `IA deepen <id>` sobre el último run (o `--run`), y andá al paso 4. |
| `status`, `doctor`, `audit` | corré `IA <comando>` y mostrale la salida. |

## Paso 2: antes de gastar

1. `IA doctor`. Si hay placeholders pendientes, decíselo en una línea (cuántos y dónde): los
   agentes los tratan como "sin información". Si hay problemas de configuración, pará y mostralos.
2. `IA plan [--pilot] [--seed S]`. Contale en una línea el tamaño: llamadas, oleadas y tokens
   estimados.
3. **Run completo:** pedí confirmación una vez antes de empezar (son más de 100 llamadas y millones
   de tokens). Si en `runs/` no hay ningún run piloto terminado, recomendá correr `--pilot` primero.
   **Piloto:** avisá el tamaño en una línea y arrancá.
4. Permisos: los sub-agentes usan WebSearch y WebFetch y escriben archivos en `runs/`. Sin reglas de
   permiso, cada uso pide aprobación. Sugerile permitir WebSearch y WebFetch para la sesión y usar el
   modo aceptar ediciones (Shift+Tab). No cambies su configuración vos.

## Paso 3: init

```bash
IA init [--pilot] [--seed S]
```

Crea `runs/<YYYYMMDD-HHMM>/` con una copia congelada de las entradas (constraints, config, rúbrica,
estrategias, personas, esquemas), reparte estrategias y sectores a los generadores y escribe
`runs/LATEST`.

## Paso 4: el loop

Siempre manejalo con `IA next`. Lee el estado del disco y te dice qué sigue:

- **`NEXT: <fase>`**: corré `IA prompts <fase>`, que escribe un brief por trabajo y los lista en
  oleadas. Lanzá **una oleada por vez**: un solo mensaje con una llamada al Agent tool por trabajo de
  esa oleada. Cada llamada:
  - `subagent_type`: `general-purpose`
  - `description`: `idea-arena <id del trabajo>`
  - `prompt`: `Leé <ruta del brief> y seguilo exactamente. Es tu brief completo.`
  - `model`: solo si `prompts` lo indica (sale de `models` en config.json).
  - `run_in_background`: false, si la herramienta tiene esa opción, para que la oleada vuelva junta.

  Esperá a que respondan todos los de la oleada antes de lanzar la siguiente. Después de la última,
  `IA next`.
- **`NEXT: step (<nombre>)`**: corré `IA step`. Es Python: verifica URLs, aplica filtros, la
  rúbrica, cierra rondas, escribe la shortlist. Después, `IA next`.
- **`STUCK`**: un juez falló tres veces. Decíselo al usuario con la ruta que imprime. No decidas el
  cruce vos: `IA record` es solo para cuando el usuario lo pide.
- **`DONE`**: paso 5.

Salidas que faltan: si después de una oleada `next` vuelve a pedir la misma fase, relanzá solo los
trabajos que `prompts` lista como pendientes, una vez. Si vuelven a faltar, escribí la línea
`NO OUTPUT` en cada archivo de salida que falte (`IA check <fase>` los lista) y seguí. Excepción:
nunca escribas NO OUTPUT para un juez (`judge`, `calibrate`); un juez que falla se relanza.
Salidas ilegibles: las aparta Python solo (`.invalido1`, `.invalido2`) y `next` te manda a
relanzarlas; el segundo fallo pasa a NO OUTPUT automáticamente donde hay un plan B.

Por qué oleadas: Claude Code corre como mucho 10 herramientas a la vez por defecto
(`CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY`). Si el usuario lo subió, que cambie `wave` en config.json.

Después de cada `step` que cierra una ronda del torneo, decile una línea al usuario, por ejemplo
"Ronda 2 de 4 cerrada: quedan 4 de 16 ideas". Nada más: no pegues ideas, ataques ni veredictos.

## Paso 5: el resultado

1. Leé la sección "Resumen" de `runs/<run>/shortlist.md` (es el único archivo de resultados que
   leés) y dale al usuario la tabla: puesto, idea, resultado en el torneo y costo.
2. Decile dónde está todo: `shortlist.md` (con el rastro de veredictos y las 5 preguntas por idea),
   `shortlist/guiones/` y `filter/reporte.md`.
3. Corré `IA audit` y decile el resultado. Si algo cambió fuera de `runs/`, decíselo claro.
4. Ofrecé los siguientes pasos: `/idea-arena deepen <id>` para una idea del top, y la calibración
   (`/idea-arena calibrate`) si todavía no la corrió.

En una calibración, el resultado es `runs/<run>/calibration_report.md`: dale el acuerdo con su
ranking, el tau de Kendall y la sección "Cómo usar esto".

## Reglas del orquestador

- No competís, no atacás, no juzgás y no elegís ganadores. `step` aplica la rúbrica a lo que
  escribieron los jueces.
- Cada brief lo arma `prompts` desde los archivos de `briefs/`. Nunca edites un brief ni agregues
  una pista en la llamada de un agente.
- No leas fichas, ideas, ataques ni veredictos durante el run. `next`, `status` y la salida de `step`
  son todo lo que necesitás.
- Todo se escribe dentro de `runs/<run>/`. Vos tampoco escribís fuera de ahí, salvo NO OUTPUT en las
  salidas que faltan. No hagas commits.
- Si se compacta tu contexto: `IA status` y después `IA next`.
- Si el usuario dice que pares, parás. `IA next` retoma más tarde.

## Las fases

| fase | quién | qué produce | brief |
| --- | --- | --- | --- |
| research | 1 agente por sector | fichas de evidencia con URL abierta | `briefs/01_investigacion.md` |
| (step verify) | Python | pide cada URL por HTTP: descarta las muertas, marca las bloqueadas | |
| generate | agentes por estrategia y foco | ideas de 1 página que citan fichas | `briefs/02_generacion.md` |
| (step ingest) | Python | IDs a ciegas, filtro duro (costo, citas, evidencia local) | |
| scope | 1 agente por lote | viable, viable con recorte o inviable en 2 semestres | `briefs/03_alcance.md` |
| dedup | 1 agente | grupos de casi-duplicados | `briefs/03_dedup.md` |
| (step select) | Python | un representante por grupo, hasta N por diversidad de sector y de tema, bracket | |
| attack | 1 por idea y persona | ataques con evidencia o marcados como opinión | `briefs/04_ataque.md` |
| defend | 1 por idea | respuestas y la idea revisada | `briefs/04_defensa.md` |
| judge | 1 por cruce (2 con juez doble) | veredicto ciego sobre Idea X e Idea Y | `briefs/04_juez.md` |
| questions | 1 por idea del top | 5 preguntas para validar con el mercado | `briefs/05_preguntas.md` |
| deepen | 3 por idea pedida | arquitectura, costos, competidores | `briefs/06_profundizar_*.md` |
| calibrate | 2 por par de ideas | veredictos sobre tus ideas de calibración | `briefs/07_calibracion.md` |
