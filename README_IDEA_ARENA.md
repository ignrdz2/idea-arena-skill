# /idea-arena: un embudo de ideas de tesis

`/idea-arena` adapta el torneo de `/arena` para generar y filtrar ideas de tesis de ingeniería en
modalidad emprendedurismo. Sub-agentes investigan problemas reales en Uruguay y LATAM, generan ideas
que citan esa evidencia, las filtran y las hacen pelear en un torneo con ataques de personas y un
juez ciego. Al final queda una shortlist de 5 a 8 ideas con el rastro de cada veredicto, 5 preguntas
para validar cada idea con gente del mercado y un guion de entrevista.

No elige la tesis por ustedes. Achica el espacio de búsqueda con evidencia verificable y les dice qué
validar primero.

## Antes del primer run

1. **Completá los placeholders.** `python skills/idea-arena/idea_arena.py doctor` lista cada
   `<<COMPLETAR>>` y `<<REVISAR>>` que falta (ver la lista al final de este archivo). Los agentes
   tratan un placeholder como "sin información", así que el pipeline corre igual, pero el encaje con
   el equipo se evalúa a ciegas hasta que lo completen.
2. **Calibrá el juez** con 3 ideas sobre las que ya tengas opinión (ver "Calibración").
3. **Corré el piloto** y mirá el resultado antes del run completo.
4. **Permisos.** Los sub-agentes usan WebSearch y WebFetch y escriben en `runs/`. Sin reglas de
   permiso, cada uso pide aprobación (cientos en un run completo). Opciones: aprobá "para esta
   sesión" cuando aparezca el primer pedido de cada herramienta y usá el modo aceptar ediciones
   (Shift+Tab), o agregá esto a `.claude/settings.local.json` del proyecto:

   ```json
   {
     "permissions": {
       "allow": [
         "WebSearch",
         "WebFetch",
         "Edit(runs/**)",
         "Bash(python skills/idea-arena/idea_arena.py:*)"
       ]
     }
   }
   ```

   Nada de esto lo configura el skill: es decisión de ustedes.

Requisitos: Claude Code y Python 3.8 o más nuevo, sin dependencias. En Windows el comando es
`python`; en macOS y Linux, `python3`. El comando `/idea-arena` ya está registrado en este proyecto
por `.claude/skills/idea-arena/SKILL.md`, que redirige a `skills/idea-arena/SKILL.md`. Abrí Claude
Code en la raíz del repo.

## Cómo correr el piloto

En Claude Code, desde la raíz del repo:

```
/idea-arena --pilot --dry-run      ver el plan: fases, llamadas, oleadas y tokens, sin gastar nada
/idea-arena --pilot                correr el piloto
```

El piloto usa 3 sectores (sorteados con la semilla, o los que pongas en `pilot.sectors`), 5
generadores de 2 ideas, un bracket de hasta 8 y una shortlist de 5: hasta 53 llamadas a
sub-agentes en unas 14 oleadas. Claude orquesta todo y al final te muestra la tabla de la shortlist.
El resultado queda en `runs/<YYYYMMDD-HHMM>/shortlist.md`.

Qué mirar en el piloto antes de pasar al run completo:
- `filter/reporte.md`: cuántas fichas se descartaron y por qué (muertas, bloqueadas, esquema), y
  cuántas ideas cayeron en cada filtro.
- Algunas fichas en `evidence/fichas.json`: si los hallazgos son concretos y las fuentes, buenas.
- Una página de idea en `ideas/` y un veredicto en `tournament/r1/`.
- El uso de tokens real en tu plan, para decidir si el run completo entra.

## Comandos

| en Claude Code | qué hace |
| --- | --- |
| `/idea-arena --dry-run` | el plan del run completo, sin escribir nada |
| `/idea-arena --pilot` | el piloto |
| `/idea-arena` | el run completo (pide confirmación antes de empezar) |
| `/idea-arena --seed 7` | misma semilla, mismo sorteo de sectores, IDs y cruces (no las mismas respuestas) |
| `/idea-arena calibrate` | calibrar el juez contra tu ranking |
| `/idea-arena deepen i007` | profundizar una idea: arquitectura, costos y competidores |
| `/idea-arena status` | dónde quedó el último run |
| `/idea-arena doctor` | placeholders pendientes y chequeos de consistencia |
| `/idea-arena audit` | confirma con git que nada cambió fuera de `runs/` |

La herramienta también se usa a mano: `python skills/idea-arena/idea_arena.py <comando>`, con
`plan`, `init`, `next`, `prompts`, `check`, `step`, `status`, `record`, `deepen`, `calibrate`,
`doctor` y `audit`. Si se corta la sesión a mitad de un run, `/idea-arena status` y después pedile a
Claude que siga: `next` retoma desde el disco.

## El pipeline

1. **Investigación.** Un agente por sector busca dolores concretos, ofertas laborales que revelan
   dolores, informes y competidores, y escribe fichas de evidencia (`briefs/01_investigacion.md`).
2. **Verificación (Python).** Pide cada URL por HTTP. Una URL que no existe descarta la ficha. Una
   URL que el sitio no deja leer a un script (LinkedIn y algunos portales) queda marcada como
   `bloqueada`: cuenta, vale menos, y una idea no puede apoyarse solo en fichas bloqueadas. Si la
   ficha trae una cita literal, Python la busca en la página.
3. **Generación.** Cada generador recibe una estrategia de arranque (`strategies.json`) y sus propios
   sectores foco (uno por generador cuando alcanzan), y escribe ideas de una página que citan fichas
   por ID (`briefs/02_generacion.md`). El problema central de cada idea sale de sus sectores.
4. **Filtro duro (Python).** Esquema completo, costo anual dentro del tope, ítems que suman el
   total, IDs citados que existen, mínimo de evidencia, evidencia de Uruguay o LATAM, y página de
   hasta 700 palabras. Un precio sin fuente verificada no descarta la idea: queda como estimación,
   con un aviso en la página para el juez, y cuenta para el tope igual.
5. **Alcance.** Un agente por lote de 3 ideas decide si el MVP entra en dos semestres: viable, viable
   con recorte o inviable. Solo "inviable" elimina.
6. **Deduplicación.** Similitud de texto en Python más un agente que agrupa casi-duplicados. Queda la
   idea de cada grupo con más evidencia verificada.
7. **Selección (Python).** Hasta 16 candidatas (8 en el piloto), repartidas por sector.
8. **Torneo.** Cada cruce: las dos ideas reciben ataques de la misma persona (cliente uruguayo,
   competidor, inversor, tutor; cambia por ronda), cada una se defiende y se revisa, y un juez ciego
   las puntúa con `rubric.md`. Python aplica la cuenta y la regla del fallo fatal.
9. **Shortlist.** Ranking, 5 preguntas de validación por idea (un agente por idea), guiones de
   entrevista y `shortlist.md`.

### La rúbrica y el fallo fatal

Evidencia de demanda 25, viabilidad con el presupuesto y el plazo 25, diferenciación 20, calidad del
business case 15, encaje con el equipo 10, valor académico 5. Un **fallo fatal** es violar una
restricción dura de `constraints.md` o sostener una afirmación central sin evidencia. El juez solo
puede marcarlo con una de esas dos categorías, y Python además marca como fatal una idea revisada que
rompe el filtro duro. Una idea con fallo fatal no le gana a una sin él, y una idea que perdió su
último cruce con fallo fatal no entra en la shortlist.

### El juez ciego y el orden

El juez ve "Idea X" e "Idea Y", nunca los IDs ni la estrategia con la que nació cada idea (eso queda
en `ideas/meta.json`, que ningún agente del torneo lee). Los IDs se asignan después de barajar. En
cada cruce va primero la idea que fue mostrada primero menos veces; si empatan, el orden alterna
cruce a cruce. Con los cruces que arma `bracket.py`, una idea puede igual quedar primera 3 veces más
que segunda (pasó en el 1,1% de 4.500 torneos simulados de 2 a 16 ideas). Si la calibración
muestra sesgo de posición, poné `tournament.judge_both_orders: true`: cada cruce se juzga en los dos
órdenes y se promedian los puntajes (un 20% más de llamadas en el torneo).

## Configuración (`skills/idea-arena/config.json`)

| clave | default | qué controla |
| --- | --- | --- |
| `infra_budget_usd` | 300 | tope duro del costo anual de infraestructura (restricción R1) |
| `infra_budget_target_usd` | 200 | objetivo cómodo: entre este valor y el tope, la idea es válida pero puntúa menos en viabilidad |
| `team` | 3 personas, 10 a 16 h/semana, 32 semanas | la capacidad de referencia para el chequeo de alcance |
| `sectors` | 10 sectores | un agente de investigación por sector. Agregá, sacá o renombrá |
| `research` | 6 a 15 fichas, fuentes de hasta 5 años | cuánta evidencia pide cada investigador |
| `evidence.on_blocked` | `keep_flagged` | `discard` descarta también las URLs bloqueadas |
| `evidence.excerpt_check` | `warn` | `discard` descarta fichas cuya cita literal no aparece en la página |
| `generation` | 10 agentes x 3 ideas | cuántas ideas nacen |
| `filter` | 2 fichas mínimo, 1 local, 700 palabras, lotes de 3 | el filtro duro y el chequeo de alcance |
| `selection.max_candidates` | 16 | tamaño del bracket |
| `tournament.persona_order` | cliente, competidor, inversor, tutor | qué persona ataca en cada ronda |
| `tournament.judge_both_orders` | false | juez doble, con el orden invertido |
| `tournament.attackers_can_search` | true | si atacantes y defensores pueden traer evidencia nueva de la web |
| `shortlist.size` | 8 | cuántas ideas van a la shortlist |
| `models` | todo `null` | modelo por fase; `null` es el de la sesión |
| `limits` | ver archivo | tope de llamadas por fase: `init` se niega si el plan lo supera |
| `pilot` | 3 sectores, 5x2 ideas, bracket 8, top 5 | lo que cambia con `--pilot` |
| `seed` | null | semilla fija para todos los runs; null es al azar (y queda registrada) |

Cada run guarda una copia congelada de la configuración en `runs/<run>/inputs/`, así que cambiar
`config.json` no altera runs anteriores.

## Cuánto cuesta en tokens

El skill es gratis; los tokens son de ustedes, y esto gasta muchos. Estimación gruesa, hasta que el
piloto la mida:

| modo | llamadas a sub-agentes | oleadas de 10 | tokens, a ojo |
| --- | --- | --- | --- |
| `--pilot` | hasta 53 | unas 14 | 1,1 a 2,6 millones |
| completo | hasta 114 | unas 19 | 2,5 a 6,2 millones |
| `calibrate` (3 ideas) | 6 | 1 | 0,1 a 0,3 millones |
| `deepen` | 3 por idea | 1 | 0,1 a 0,4 millones por idea |

La investigación es la fase más cara (los agentes leen páginas web enteras). Para gastar menos:
corré el piloto primero, poné `"sonnet"` en `models.research`, `models.attack` y `models.defend`
(dejá el juez con el modelo de la sesión), bajá `generation.agents` o `selection.max_candidates`
(con 8 candidatas el torneo baja de 75 a 35 llamadas). `/idea-arena --dry-run` recalcula todo antes de
gastar. En un plan de suscripción esto consume tu límite de uso: un run completo puede llevarse una
buena parte de una ventana. Tiempo, a ojo: el piloto, alrededor de una hora; el completo, de 2 a 4.

## Cómo editar `constraints.md`

`skills/idea-arena/constraints.md` es lo que todos los agentes leen. Tiene tres partes:

1. **Restricciones duras (R1 a R7).** Eliminan ideas y son las únicas que el juez puede citar como
   fallo fatal. Para agregar una, usá el ID siguiente con el formato `- **R8** (tema): texto`. Si le
   escribís `[A CONFIRMAR]`, el juez la trata como criterio blando hasta que saques la marca.
2. **Perfil del equipo.** Fortalezas, experiencia, intereses y horas de cada integrante, la tabla de
   contactos en industrias concretas y las preferencias. Los contactos importan: suben el encaje y
   habilitan ideas que necesitan datos de un socio (R7).
3. **Criterios blandos con pesos.** Si cambiás un peso, cambialo también en `rubric.md` y en
   `CRITERIA` de `ia_tournament.py`; un test verifica que los tres coincidan.

`{{infra_budget_usd}}` y los otros valores entre llaves se completan solos desde `config.json` en la
copia de cada run. No uses los caracteres de raya larga ni de semirraya en ningún archivo del repo:
un test los prohíbe (las salidas de los agentes se sanean solas).

## Calibración

Antes de gastar en un run completo, comprobá que el juez piensa parecido a ustedes:

1. Reemplazá los placeholders de `skills/idea-arena/calibration/ideas/idea_A.md`, `idea_B.md` e
   `idea_C.md` con tres ideas que ya conozcan y sobre las que tengan opinión. Mantené las secciones
   y poné links donde haya evidencia. Podés agregar más archivos.
2. Escribí tu orden en `skills/idea-arena/calibration/my_ranking.md`.
3. `/idea-arena calibrate`. El juez compara cada par en los dos órdenes (6 llamadas con 3 ideas).
4. Leé `runs/<run>/calibration_report.md`: acuerdo por pares con tu ranking, tau de Kendall,
   consistencia entre órdenes (sesgo de posición) y en qué criterios tu idea preferida puntuó menos.
   Ajustá pesos o anclas en `rubric.md` y repetí.

Con 3 ideas la señal es gruesa: un desacuerdo puede ser ruido. Usala para detectar desvíos grandes.

## Profundizar una idea

`/idea-arena deepen i007` lanza 3 agentes sobre la última versión de la idea: un bosquejo de
arquitectura, un modelo de costos mes a mes con tres escenarios y fuentes de precios, y una tabla de
competidores. Las fuentes nuevas se verifican como cualquier ficha. Queda en
`runs/<run>/deepen/i007/`.

## Qué se versiona

Todo lo que escribe el pipeline está en `runs/<YYYYMMDD-HHMM>/`, y `runs/` no está en `.gitignore` a
propósito: fichas, ideas, veredictos y briefs son el registro de cómo eligieron la tesis.
`runs/README.md` describe cada archivo. El skill no hace commits. Antes de un commit,
`/idea-arena audit` confirma que nada cambió fuera de `runs/`. Los briefs de `prompts/` tienen rutas
absolutas de la máquina donde se corrió el run: los agentes las necesitan.

## La letra chica

- **Una URL que existe no prueba que diga lo que la ficha afirma.** Python verifica que la página
  exista y, si hay cita literal, que la cita esté. Que el hallazgo esté bien parafraseado lo chequean
  el juez y los atacantes. Revisen a mano las fichas de las ideas que les interesen.
- **Los jueces son Claude.** La shortlist es lo que sobrevivió a este torneo, no una verdad. Por eso
  muestra el rastro de cada veredicto, y por eso existen las preguntas de validación.
- **Más allá del puesto 2, el orden es ruidoso.** Dos ideas eliminadas en la misma ronda enfrentaron
  rivales distintos.
- **La misma semilla da el mismo sorteo, no las mismas ideas.** Los modelos no son deterministas.
- **Si el sector no tiene evidencia en la web, no hay ideas de ese sector.** Las ideas nacen de
  fichas; el conocimiento de ustedes entra por los contactos y los intereses en `constraints.md`.

## Placeholders que te toca completar

`/idea-arena doctor` los lista con número de línea. Hoy son:

**`skills/idea-arena/constraints.md`**
- Perfil técnico: el `<<REVISAR>>` sobre OpenAI. En tu descripción dice "Azure, AWS OpenAI";
  aclarar si es Azure OpenAI, OpenAI vía AWS u otra cosa.
- Capacidad: semanas efectivas por semestre según el calendario de la facultad (opcional).
- Integrantes 1, 2 y 3: nombre o rol, fortalezas técnicas propias, experiencia laboral, intereses y
  horas por semana si difieren de 10 a 16 (opcional).
- Tabla de contactos en industrias concretas: sector, organización, persona o rol, qué puede aportar
  y quién del equipo lo conoce (dos filas de ejemplo; agreguen las que tengan).
- Preferencias del equipo: sectores preferidos y sectores a evitar (opcionales, no eliminan ideas).

**`skills/idea-arena/calibration/`**
- `ideas/idea_A.md`, `ideas/idea_B.md`, `ideas/idea_C.md`: tres ideas reales sobre las que tengas
  opinión.
- `my_ranking.md`: tu orden de las tres.

## Archivos

```
skills/idea-arena/SKILL.md            la orquestación que sigue Claude
skills/idea-arena/idea_arena.py       la herramienta: máquina de estados del pipeline
skills/idea-arena/ia_tournament.py    el torneo, sobre skills/arena/bracket.py (importado, no copiado)
skills/idea-arena/ia_schema.py        validación, filtro duro y la página de 1 hoja
skills/idea-arena/ia_evidence.py      chequeo HTTP de URLs, similitud de texto, saneo
skills/idea-arena/config.json         los parámetros
skills/idea-arena/constraints.md      restricciones, perfil del equipo y criterios
skills/idea-arena/rubric.md           la rúbrica del juez
skills/idea-arena/strategies.json     las 5 estrategias de arranque
skills/idea-arena/personas.json       las 4 personas de ataque
skills/idea-arena/schemas/            los formatos de ficha, idea, ataque, defensa, veredicto...
skills/idea-arena/briefs/             un brief por fase: lo que recibe cada sub-agente
skills/idea-arena/templates/          la plantilla del guion de entrevista
skills/idea-arena/calibration/        tus ideas de calibración y tu ranking
.claude/skills/idea-arena/SKILL.md    registra /idea-arena en este proyecto
docs/PLAN.md                          el plan de diseño aprobado
tests/test_idea_arena.py              los tests
runs/                                 todo lo que escribe el pipeline
```

Tests, desde la raíz del repo: `python -m unittest discover -s tests -v`. Incluyen un piloto completo
por línea de comandos con sub-agentes y URLs simulados, que verifica que nada se escriba fuera de
`runs/`.
