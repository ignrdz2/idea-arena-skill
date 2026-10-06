# Plan: idea-arena

Estado: borrador para aprobación. Todavía no hay código escrito. Fecha: 2026-10-02.

## 0. Lo que encontré en el repo (y en qué difiere de tu descripción)

En lo esencial coincide: `/arena` corre un torneo de eliminación simple con ataque, defensa con
revisión y juez. Estas diferencias importan para el diseño:

1. **El juez no es del todo ciego y no alterna el orden.** No ve las cartas de estrategia, pero sí
   los IDs de competidor (`a017`), y el orden en que se le presentan las dos soluciones se sortea
   con una moneda en cada cruce (`pair_round`, bracket.py:326). No hay alternancia ni control del
   sesgo de posición.
2. **Los atacantes son los rivales.** En `/arena` cada competidor ataca la solución del otro con su
   propia carta. No hay personas de ataque.
3. **Todo vive en `.arena/`, que está en `.gitignore`.** Las rutas guardadas en `arena.json` son
   absolutas.
4. **Los pesos de la rúbrica están fijos en el código** (`WEIGHTS`, bracket.py:54), y un test
   verifica que coincidan con `rubric.md`. `decide()` y `collect()` usan esa constante global y
   desempatan por `correctness`. No se pueden reusar con otra rúbrica sin mutar el módulo.
5. **`bracket.py` imprime los comandos con `python3`.** En esta máquina `python3` es el alias de
   Microsoft Store y no funciona; el intérprete real es `python` (3.14.2). Esto también afecta al
   `/arena` original, que no toco.
6. **`skills/` no se descubre sola.** Claude Code solo registra skills en `.claude/skills/` del
   proyecto, en `~/.claude/skills/` o a través de un plugin. Crear `skills/idea-arena/` no te da
   `/idea-arena` por sí solo (ver D12).
7. **Un test existente recorre todo el repo buscando rayas largas** (`test_no_em_dashes_anywhere`,
   tests/test_bracket.py:393, caracteres U+2014 y U+2013). Si versionás `runs/` con texto generado
   por modelos, que usan esas rayas seguido, ese test empieza a fallar. Ver D11.
8. Línea base: `python -m unittest discover -s tests -v` da **27 tests, todos OK** (28,8 s).

## 1. Arquitectura

Pipeline en 5 fases. Igual que en `/arena`, el estado vive en un JSON en disco y la sesión principal
(el orquestador) maneja todo con `next`: lanza sub-agentes en oleadas de 10 y nunca lee fichas,
ideas ni veredictos. Los pasos determinísticos los hace Python, sin modelos.

```
F1  investigación (1 agente por sector)
F1b verificación de URLs (Python, HTTP)
F2  generación (agentes por estrategia x foco de sectores)
F3a filtro duro (Python)
F3b alcance viable en 2 semestres (agentes)
F3c deduplicación (Python + 1 agente)
F3d selección de hasta N (Python)
F4  torneo, por ronda:
      ataque (persona) -> verificación de la evidencia de los ataques (Python)
      -> defensa y revisión -> render y filtro duro de la idea revisada (Python)
      -> juez ciego -> collect -> advance
F5  ranking (Python) -> preguntas de validación (1 agente por idea) -> shortlist.md (Python)

Aparte: calibrate (el juez ordena tus 3 ideas), deepen <id> (profundización de una idea),
audit (lista cambios fuera de runs/ según git status)
```

### Archivos nuevos

```
skills/idea-arena/
  SKILL.md               orquestación de /idea-arena: pasos, banderas, reglas del orquestador
  idea_arena.py          CLI y máquina de estados del pipeline
  ia_schema.py           validador stdlib (subconjunto de JSON Schema) y filtro duro
  ia_tournament.py       adaptador sobre skills/arena/bracket.py: personas, orden alternado,
                         decide de 6 criterios, fallo fatal
  ia_evidence.py         verificación HTTP de URLs, similitud léxica para dedup, saneo de texto
  config.json            parámetros: infra_budget_usd, sectores, N, topes por fase, piloto,
                         modelo por fase
  constraints.md         restricciones duras / perfil del equipo con placeholders /
                         criterios blandos con pesos
  rubric.md              6 criterios, anclas de 0 a 10, regla de fallo fatal, desempates
  strategies.json        5 estrategias de arranque para la generación
  personas.json          4 personas de ataque
  schemas/               ficha, idea, ataque, defensa y veredicto (.schema.json); también los
                         leen los agentes como especificación de formato
  briefs/                un archivo por brief: 01_investigacion, 02_generacion, 03_alcance,
                         03_dedup, 04_ataque, 04_defensa, 04_juez, 05_preguntas,
                         06_profundizar, 07_calibracion
  templates/guion_entrevista.md
  calibration/ideas/idea_A.md, idea_B.md, idea_C.md   (placeholders)
  calibration/my_ranking.md                            (placeholder)
tests/test_idea_arena.py
docs/PLAN.md             este archivo
README_IDEA_ARENA.md     en español
runs/README.md           explica la estructura de un run (y hace que runs/ exista en git)
```

No se modifica nada de `skills/arena/`, `tests/test_bracket.py`, `README.md`, `.gitignore` ni los
manifiestos del plugin. No hago commits.

### Estructura de un run

```
runs/20261002-1530/                 (si ya existe en ese minuto: 20261002-1530-2)
  state.json                        estado del pipeline, rutas relativas a la raíz del repo
  inputs/                           copia congelada de constraints, config efectivo, rubric,
                                    strategies y personas
  prompts/<fase>/<job>.md           el brief exacto que recibió cada sub-agente
  evidence/raw/<sector>.json        lo que escribió cada investigador
  evidence/fichas.json              fichas verificadas: las únicas que se pueden citar
  evidence/descartadas.json         fichas descartadas, con el motivo
  ideas/raw/<generador>.json        lo que escribió cada generador
  ideas/<id>.json, ideas/<id>.md    idea canónica (con meta) y su página de 1 hoja (sin meta)
  filter/                           alcance, dedup, selección y reporte del filtro
  tournament/bracket.json           estado compatible con bracket.py, más campos propios
  tournament/r<n>/                  ataques, defensas, ideas revisadas, veredictos
  shortlist.md                      el entregable para humanos
  shortlist/preguntas/, shortlist/guiones/
  deepen/<id>/                      profundizaciones
  scratch/                          espacio temporal de los sub-agentes
runs/LATEST                         puntero al último run
```

## 2. Qué reuso de bracket.py, qué cambia y por qué

### Reuso (import, sin copiar)

| Función de bracket.py | Para qué |
| --- | --- |
| `bracket_sizes` | tamaños por ronda y conteo de llamadas |
| `open_round`, `advance`, `record`, `current_round`, `find_match`, `rounds_played`, `alive_ids` | ciclo de vida del bracket: emparejar, byes (nunca dos al mismo mientras otro espera), eliminar, arrastrar la versión revisada al cruce siguiente, coronar |
| `plan_rows` | llamadas y oleadas del torneo (5 por cruce, igual que `/arena`) |
| `extract_json`, `fill` | parseo de veredictos y relleno de plantillas en una sola pasada |
| `ArenaError` | errores del bracket |

Las ideas ocupan el lugar de los agentes en el estado de bracket.py:
`agents["i007"] = {card, solution, alive, eliminated_in, eliminated_by, byes}` más campos propios.
`solution` apunta a la página renderizada de la idea (`.md`, sin meta), que es justo lo que lee el
juez. Para el emparejamiento, `card.reasoning.id` lleva el sector principal de la idea, así
`pair_round` prefiere cruzar ideas de sectores distintos y cada cruce compara alternativas reales.

### Cambia (código propio en ia_tournament.py)

| Qué | Por qué |
| --- | --- |
| `decide` propio, 6 criterios con los pesos de la rúbrica | `bracket.decide` usa la constante global `WEIGHTS` de 5 criterios y desempata por `correctness`, que acá no existe |
| Fallo fatal = fatal del juez con categoría válida, **o** fatal determinístico de Python | el juez solo puede marcar fatal citando `restriccion_dura:<R-id>` o `afirmacion_sin_evidencia:<cita>`. Además, si la idea revisada rompe el filtro duro (costo sobre el tope, ID inexistente, esquema roto), es fatal diga lo que diga el juez |
| Orden de presentación al juez | `pair_round` sortea a/b con una moneda. Encima agrego `first`: va primero la idea que fue mostrada primero menos veces; si empatan, alterna según la paridad del cruce. El juez ve "Idea X" e "Idea Y", nunca los IDs |
| Personas de ataque, y quién ataca | en `/arena` ataca el rival con su carta. Acá ataca un agente neutral con una persona. Las dos ideas de un cruce reciben la misma persona (comparación justa), elegida entre las que ninguna de las dos enfrentó todavía. En un bracket de 16 (4 rondas) con 4 personas, la campeona enfrentó a las 4 |
| `collect`, `phase_jobs`, `render_job`, `next_action`, estado en disco | otras fases y archivos, briefs en archivos propios, JSON en vez de markdown, `runs/` en vez de `.arena/`, rutas relativas |
| Comando impreso: `python` en Windows, `python3` en el resto | `python3` no funciona en esta máquina |

### D1. ¿Importar o copiar bracket.py?

**Importo** `skills/arena/bracket.py` con `importlib`, por ruta relativa al propio archivo y sin
tocar `sys.path`, con `sys.dont_write_bytecode = True` para no dejar `__pycache__` en
`skills/arena/`.

- A favor: una sola fuente para la mecánica de eliminación, que ya tiene 27 tests (incluido un
  torneo de 100 por CLI). Cumple tu regla de no modificar `/arena`: es una dependencia de solo
  lectura, y solo uso funciones públicas (sin guion bajo).
- En contra: si alguien actualiza bracket.py desde upstream y cambia esas funciones, idea-arena se
  puede romper. Mitigación: tests que fijan el contrato (tamaños de bracket idénticos, byes, que
  `advance` arrastre la versión revisada).
- En contra: idea-arena no se puede instalar sola copiando su carpeta; necesita `skills/arena/` al
  lado. Con el shim de D12 no es problema, porque todo vive en este repo.

Alternativas descartadas:
- **Copiar bracket.py tal cual** dentro de idea-arena: dos copias que derivan, y un test de checksum
  para detectar la deriva deja el mismo acoplamiento que importar.
- **Copiar y adaptar** (fork completo): unas 1.200 líneas duplicadas para usar unas 150.
- **Importar y pisar `B.WEIGHTS`** en tiempo de ejecución: muta estado global y rompe
  `test_weights_match_the_rubric` cuando las dos suites corren en el mismo proceso.

## 3. Las fases en detalle

### F1 Investigación

- Un sub-agente por sector (`config.json > sectors`; 10 por defecto). Brief:
  `briefs/01_investigacion.md`. Lee el `constraints.md` del run.
- Busca problemas concretos en Uruguay/LATAM: prensa, informes, ofertas laborales que revelen
  dolores, competidores y sus huecos. El brief da tipos de fuente con ejemplos, no obligatorios.
- Escribe `evidence/raw/<sector>.json`: una lista de fichas con `id` (`F-<sector>-NNN`), `sector`,
  `hallazgo` (parafraseado, 1 o 2 oraciones), `source_url`, `source_title`, `source_date`,
  `source_type` (enum), `geografia`, `confianza` (alta, media, baja) y `retrieved_at`. Agrego dos
  campos opcionales: `extracto` (cita literal de hasta 30 palabras, para verificar) y `competidor`
  (nombre, si la ficha habla de un competidor).
- Regla del brief: solo hay ficha de páginas que el agente abrió con WebFetch en esa sesión. Si no
  la pudo abrir, no hay ficha.

### F1b Verificación (Python, sin modelos)

- Esquema completo e IDs únicos.
- Cada `source_url` se pide por HTTP (urllib, con timeout y user agent). Resultado: `ok` (2xx),
  `muerta` (404, 410, DNS, 5xx) o `bloqueada` (401, 403, 429, 999).
- `muerta` se descarta siempre. `bloqueada` se descarta por defecto (tu regla dura); se puede
  cambiar con `evidence.on_blocked` (ver pregunta abierta 1).
- Si hay `extracto` y la página respondió `ok`, se busca el extracto en el texto normalizado. Si no
  aparece: advertencia y confianza baja (`evidence.excerpt_check: "warn"`), sin descarte, porque
  las páginas armadas con JavaScript darían falsos negativos.
- URLs repetidas entre sectores se fusionan. Todo descarte queda en `descartadas.json` con motivo.

### F2 Generación

- Agentes = estrategia x foco de sectores, asignados con semilla. Los sectores se reparten en un
  grupo por agente (o uno por sector, si hay menos sectores que agentes): por defecto 10 agentes,
  un sector cada uno, 3 ideas cada uno: 30 ideas. Todos leen todas las fichas, pero el problema
  central de cada idea sale de fichas de su foco. (Antes cada agente tenía la mitad de los
  sectores, y en el piloto todos tenían todos: convergían en los mismos 2 o 3 problemas.)
- `strategies.json`: partir de un dolor, partir de una capacidad técnica del equipo, segmento
  desatendido, localizar un producto extranjero exitoso, invertir lo que hace un incumbente.
- Formato fijo (JSON): `titulo`, `problema`, `usuario`, `solucion`, `mvp` (`semestre_1` y
  `semestre_2`, alineados a las 2 entregas), `stack`, `costo_infra` (`items` con `concepto`,
  `usd_anual`, `supuesto` y `fuente_precio_url`, más `total_anual_usd`), `competidores` (`nombre`,
  `evidencia_ids`, `hueco`), `monetizacion`, `riesgos`, `supuestos`, `evidencias` (IDs). Python le
  agrega `meta` (`estrategia`, `generador`, `foco`), que el juez no ve.
- Python asigna los IDs canónicos (`i001`, ...) después de barajar con semilla, para que el ID no
  delate generador ni estrategia, y renderiza la página de 1 hoja (`<id>.md`, sin `meta`). Al pie
  de la página, Python agrega la tabla de fichas citadas (hallazgo, fuente, fecha, URL) sacada de
  `fichas.json`, no de lo que escribió el generador: así el juez compara lo que la idea afirma con
  lo que la ficha dice de verdad.

### F3 Filtro y deduplicación

- **Duro (Python):** esquema completo; `costo_infra.total_anual_usd <= infra_budget_usd` y la suma
  de los ítems coincide; cada ítem de costo con supuesto y, si se pudo abrir, fuente de precio (URL
  verificada igual que las fichas). Un ítem sin fuente, o con una que no se pudo verificar, es una
  estimación: aviso `costo_estimado` en la página, que no descarta ni es fatal; todos los IDs
  citados existen en `fichas.json`; al menos
  `min_evidence_per_idea` fichas (2 por defecto) y al menos 1 con geografía Uruguay o LATAM; cada
  competidor cita una ficha; la página tiene hasta `idea_max_words` palabras (700 por defecto, sin
  contar la tabla de evidencia).
- **Alcance (agentes):** un agente por lote de 3 ideas (`filter.scope_batch`), que juzga cada idea
  por separado: horas estimadas del MVP contra la capacidad del equipo (horas por semana de
  `constraints.md`) y dependencias que el equipo no controla (datos, socios, permisos). Salida:
  `viable` (sí o no), motivo concreto y recorte sugerido. Un "no" elimina, con el motivo en el
  reporte.
- **Dedup:** primero similitud léxica en Python (n-gramas sin tildes ni palabras vacías, umbral
  configurable). Después 1 agente que ve título, usuario, problema y solución de las sobrevivientes
  y propone grupos de casi-duplicados; Python valida que cada ID aparezca una sola vez. De cada
  grupo queda la idea con más fichas verificadas distintas (desempate con semilla). Los grupos
  quedan en el reporte.
- **Selección a N** (16 por defecto): round-robin por sector principal, para no perder diversidad;
  dentro de cada sector, primero las que tienen más fichas verificadas, pero una por tema antes que
  la segunda de cualquier tema. Un tema agrupa ideas cuyo problema cita casi las mismas fichas
  (solapamiento de Jaccard de al menos `filter.theme_overlap`, 0.5 por defecto).

### F4 Torneo

- Por cruce: 2 ataques (la misma persona para las dos ideas), 2 defensas y 1 juez = 5 llamadas,
  igual que `/arena`. Con `tournament.judge_both_orders: true` se suma un segundo juez con el orden
  invertido: se promedian los puntajes por criterio y fatal es la unión de los dos.
- **Ataque** (`briefs/04_ataque.md`): JSON con hasta 7 ataques, severidad FATAL, MAJOR o MINOR, y
  en cada ataque `evidencia` (IDs) o `tipo: "opinion"`. Puede buscar en la web si
  `tournament.attackers_can_search` (sí por defecto); la evidencia nueva va como ficha con el mismo
  esquema y pasa por la misma verificación. Python reetiqueta como opinión cualquier ataque que
  cite IDs inexistentes o fichas descartadas.
- **Defensa** (`briefs/04_defensa.md`): CONCEDE, PARCIAL o REBUT por ataque, después de chequear el
  ataque contra las fichas, la idea y las restricciones (en el piloto, con solo CONCEDE o REBUT y
  "conceder puntúa mejor", las defensas concedieron todo), y la idea revisada completa
  (JSON, sin meta). Python le devuelve la meta, la pasa por el filtro duro y la renderiza. Si el
  JSON revisado no valida, se mantiene la versión anterior y queda anotado.
- **Juez** (`briefs/04_juez.md`): lee rúbrica, constraints, las dos páginas como Idea X e Idea Y,
  los ataques y las defensas. Puntúa los 6 criterios de 0 a 10, `fatal` con `fatal_motivo`,
  `standing` y `survived`. Python decide: una idea sin fatal le gana a una con fatal; si las dos o
  ninguna lo tienen, gana el total ponderado. Desempates: menos ataques en pie, después más
  evidencia de demanda, después más viabilidad, después la elección del juez.
- **Rúbrica:** evidencia de demanda 25, viabilidad con ese presupuesto y plazo 25, diferenciación
  20, calidad del business case 15, encaje con el equipo 10, valor académico 5. Un test verifica
  que los pesos coincidan entre `rubric.md`, `constraints.md` y el código.
- **Personas** (`personas.json`): inversor escéptico, tutor académico, cliente real de una empresa
  uruguaya, competidor.
- **Ceguera:** nadie en el torneo (atacante, defensor, juez) ve la estrategia de origen ni el
  generador. Un test verifica que ningún brief del torneo ni página renderizada contenga IDs o
  nombres de `strategies.json`.

### F5 Humano en el circuito

- Ranking (Python): campeona; finalista; después por ronda de eliminación y, dentro de la misma
  ronda, por el total que sacó en el cruce que perdió. Top `shortlist_size` (8 en completo, 5 en
  piloto). `shortlist.md` aclara que, más allá del puesto 2, el orden de una eliminación simple es
  ruidoso.
- 1 agente por idea del top: 5 preguntas para validar con gente del mercado, sacadas de los ataques
  que quedaron en pie y de los supuestos. Preguntas sobre comportamiento pasado, no hipotéticas.
- Python arma `shortlist.md`: por idea, resumen, costo, evidencias, rastro de veredictos (ronda,
  rival, persona, puntajes, motivo, ataques en pie), las 5 preguntas y el link a su guion de
  entrevista (`templates/guion_entrevista.md` completado con los datos de la idea).
- `deepen <id>`: funcional, no stub. Escribe 3 briefs (bosquejo de arquitectura, modelo de costos
  con fuentes y escenarios, tabla de competidores con evidencia nueva verificada); las salidas van
  a `runs/<run>/deepen/<id>/` y el orquestador lanza los agentes.

## 4. Modos de control

| Modo | Qué hace |
| --- | --- |
| `--pilot` | 3 sectores (`pilot.sectors`; vacío = 3 al azar con semilla, queda registrado), 5 generadores x 2 ideas = 10 ideas, bracket de hasta 8, shortlist de 5 |
| `--dry-run` | imprime el plan, las fases, las llamadas máximas por fase, las oleadas y si algún tope se excede. No escribe nada, no llama modelos ni red |
| Topes | `limits` en config.json, uno por fase. `init` se niega si el plan los supera, y `prompts` nunca emite más trabajos que el tope. Los reintentos se cuentan aparte (máximo 1 por trabajo, como en `/arena`) |
| Modelo por fase | `models` en config.json; `null` = el modelo de la sesión. Si ponés `"sonnet"` para investigación o ataques, el orquestador lo pasa en la llamada al Agent tool. Es la palanca principal de costo |

## 5. Calibración del juez

- `calibration/ideas/idea_A.md`, `idea_B.md`, `idea_C.md`: plantilla con las mismas secciones que la
  página de 1 hoja y marcadores `<<COMPLETAR>>`. Como no tienen fichas, los links que pongas en el
  texto cuentan como evidencia para el juez de calibración.
- `calibration/my_ranking.md`: tu orden (lista numerada) y, si querés, una línea de por qué.
- `calibrate` se niega a correr si quedan `<<COMPLETAR>>`. Juega todos los pares en los dos órdenes
  (3 ideas = 6 llamadas). Reporte en `runs/<run>/calibration_report.md`: acuerdo por pares con tu
  ranking (x de 3), tau de Kendall, consistencia entre órdenes (sesgo de posición) y puntajes por
  criterio, para ver qué criterio produce el desacuerdo.

## 6. Otras decisiones

| # | Decisión | Alternativa descartada, y por qué |
| --- | --- | --- |
| D2 | Archivos editables (constraints, config, calibration) dentro de `skills/idea-arena/` | En la raíz del repo: se mezclan con los del skill original |
| D3 | Rutas relativas en el estado y los datos; absolutas solo en los briefs, porque el Read de los agentes las necesita | Absolutas en todo, como `/arena`: lo versionado tendría `C:\Users\ignrd\...` y se rompe al clonar en otra máquina |
| D4 | El agente abre la URL y además Python la verifica por HTTP | Confiar en que el agente dice que la abrió: no es verificable |
| D5 | IDs canónicos después de barajar, meta oculta, tabla de evidencia armada por Python | Que el generador escriba la tabla: puede parafrasear mal la ficha |
| D6 | Atacantes = personas neutrales, la misma persona para ambas ideas del cruce | Que ataque la idea rival como en `/arena`: una idea no tiene autor con incentivo. Las 4 personas en cada cruce: 11 llamadas por cruce en vez de 5 |
| D7 | Orden determinístico (menos veces primero) y etiquetas X/Y; juez doble opcional | Moneda como en `/arena`: balancea solo en promedio. Juez doble siempre: +20% de llamadas |
| D8 | Fatal con categoría obligatoria, más fatal determinístico | Fatal libre: el juez podría marcar fatal por gusto |
| D9 | Dedup léxico más 1 agente | Solo léxico: no detecta la misma idea con otras palabras. Solo agente: no es reproducible |
| D10 | Textos para personas en español; código y comentarios en inglés con formato `%` como bracket.py; claves JSON en español sin tildes | Todo en español: rompe el estilo del código existente |
| D11 | Sanear rayas largas (U+2014, U+2013) en toda salida del pipeline y pedir en los briefs que no se usen | Excluir `runs/` del test existente: es modificar la suite de `/arena` y necesita tu OK |
| D12 | Shim de unas 10 líneas en `.claude/skills/idea-arena/SKILL.md` que manda a leer `skills/idea-arena/SKILL.md`: da `/idea-arena` en este proyecto sin duplicar nada | Copiar a `~/.claude/skills/`: queda global y hay que copiar también `arena/`. Plugin: el comando queda `/arena-skill:idea-arena` |
| D13 | 4 módulos chicos | Un solo archivo de unas 2.000 líneas: más difícil de testear por partes |
| D14 | Solo biblioteca estándar, sintaxis compatible con Python 3.8 | Es la convención del repo |

### Cómo evito sesgar hacia una idea

- Ningún brief menciona ideas, productos ni dominios de ejemplo. Los sectores salen de config.json.
- Las estrategias son formas de buscar, no temas. "Partir de una capacidad técnica" tira hacia IA y
  datos por el perfil del equipo; lo compensan las otras 4 estrategias, y el encaje con el equipo
  pesa solo 10.
- El juez no ve estrategia ni generador, y los IDs se asignan después de barajar.

## 7. Estimación de llamadas a sub-agentes

| Fase | Completo (defaults) | Piloto | Notas |
| --- | --- | --- | --- |
| F1 investigación | 10 | 3 | la más cara en tokens: lee páginas web |
| F1b verificación | 0 | 0 | Python; unas 100 a 150 URLs en completo |
| F2 generación | 10 (30 ideas) | 5 (10 ideas) | |
| F3 filtro duro | 0 | 0 | Python |
| F3 alcance | hasta 10 | hasta 4 | 1 cada 3 ideas que pasan el filtro duro |
| F3 dedup | 1 | 1 | |
| F4 torneo | 75 (16 ideas, 15 cruces, 4 rondas) | 35 (8 ideas, 7 cruces, 3 rondas) | +15 o +7 con juez doble |
| F5 preguntas | 8 | 5 | |
| **Total** | **hasta 114** | **hasta 53** | |
| Oleadas de 10 | unas 19 | unas 14 | |
| Calibración | 6 | | aparte |
| Profundizar | 3 por idea | | aparte |

Tokens, a ojo (los medimos de verdad con el piloto): investigación con web, 60k a 200k por agente;
generación, 30k a 60k; cada llamada del torneo, 15k a 50k (el juez lee más). Run completo: del
orden de 3 a 6 millones de tokens. Piloto: del orden de 1 a 2,5 millones. En un plan de suscripción
eso consume límite de uso; por API, depende del modelo que pongas en cada fase. Tiempo, también a
ojo: piloto alrededor de 1 hora, completo de 2 a 4 horas.

## 8. Permisos que van a necesitar los sub-agentes

No toco tu configuración. Hoy no hay `.claude/settings.json` en el proyecto y tu
`~/.claude/settings.json` no tiene reglas de permisos, así que todo esto va a pedir aprobación una
por una:

| Permiso | Quién | Por qué |
| --- | --- | --- |
| `WebSearch` | investigación, ataques, profundizar | buscar fuentes |
| `WebFetch` | investigación, ataques, defensas, generación (precios), profundizar | abrir cada URL citada: es la regla dura |
| `Write` y `Edit` en `runs/**`, o el modo aceptar ediciones (Shift+Tab) | todos | cada sub-agente escribe 1 o 2 archivos |
| `Bash(python skills/idea-arena/idea_arena.py:*)` | el orquestador | los pasos de Python |
| Red saliente para Python (urllib) | el orquestador, en la verificación | el chequeo HTTP corre dentro de ese mismo comando |

Si querés, te paso el bloque exacto para `.claude/settings.local.json` y lo agregás vos, o me decís
que lo agregue yo.

## 9. Tests (tests/test_idea_arena.py, solo stdlib)

- **Esquemas:** fichas e ideas válidas pasan; campos faltantes, enum inválido, URL mal formada y
  fecha inválida fallan.
- **Filtro duro:** costo sobre el tope, suma que no cierra, ID inexistente, sin evidencia local,
  competidor sin ficha, página demasiado larga.
- **Verificación de URLs** con un fetcher falso (sin red): muerta se descarta, bloqueada según la
  config, extracto ausente advierte.
- **Regla de fallo fatal:** sin fatal le gana a fatal aunque tenga menos puntos; fatal sin categoría
  válida se ignora (con nota); el fatal determinístico pisa al juez; ambos fatales, deciden los
  totales; desempates.
- **Alternancia del juez:** en la ronda 1 el orden alterna cruce a cruce; nunca va primero la idea
  que ya fue mostrada primero más veces; en torneos simulados (varios tamaños y semillas) el
  desbalance por idea queda acotado; el brief del juez pone a `first` como Idea X; con juez doble,
  el segundo brief está invertido.
- **Ceguera:** ningún brief del torneo ni página renderizada contiene meta ni nombres o IDs de
  estrategias.
- **Contrato con bracket.py:** tamaños de bracket y llamadas del torneo iguales a los de `/arena`;
  byes y arrastre de la versión revisada.
- **Nada fuera de runs/:** pipeline piloto completo por CLI con sub-agentes falsos en una raíz
  temporal; foto del árbol antes y después: todo archivo nuevo o modificado está bajo `runs/`, y
  `skills/` no cambia. Además: `--dry-run` no escribe nada, y `runs/` no está ignorado por git.
- Topes, dedup, selección, métricas de calibración (acuerdo por pares y Kendall) y saneo de rayas.
- Al terminar corro las dos suites: las 27 originales tienen que seguir pasando.

## 10. Preguntas abiertas para resolver al aprobar

1. **URLs bloqueadas.** LinkedIn y varios portales de empleo responden 403 o 999 a los scripts.
   ¿Las descarto (tu regla, mi default) o las conservo marcadas como `bloqueada`, sin que puedan ser
   la única evidencia de demanda de una idea? Propongo decidirlo con los números del piloto, que
   reporta cuántas se descartaron por este motivo.
2. **D12.** ¿Te sirve que cree `.claude/skills/idea-arena/SKILL.md` (el shim) para tener
   `/idea-arena` en este proyecto?
3. **D11.** ¿Saneo las rayas largas en las salidas (mi propuesta) o preferís que excluya `runs/` del
   test existente?
4. **Tope de costo.** Pongo `infra_budget_usd: 300` como tope duro, y 200 como objetivo cómodo
   dentro del criterio de viabilidad. ¿Va?
5. **Briefs versionados.** `runs/<run>/prompts/` lleva rutas absolutas de tu máquina (las necesita
   el Read de los agentes) y ocupa bastante. ¿Se versionan igual o los saco del run?
6. **Capacidad del equipo.** El chequeo de alcance necesita horas por semana por persona. Queda
   como placeholder en constraints.md; si me das un número ahora, lo pongo de default.
7. **Restricciones derivadas.** Además de lo que me diste, propongo dos restricciones duras marcadas
   `[A CONFIRMAR]`: que el MVP no requiera una licencia regulatoria imposible de conseguir en el
   plazo (por ejemplo, operar como entidad financiera o certificar un dispositivo médico), y que no
   dependa de datos a los que el equipo no tiene acceso legal sin un socio ya identificado. Mientras
   lleven la marca, el juez las trata como criterio blando y no como fallo fatal.

## 11. Respuestas y cambios durante la implementación

Respuestas aprobadas el 2026-10-02:

1. URLs bloqueadas: se conservan marcadas como `bloqueada` (`evidence.on_blocked: "keep_flagged"`).
   Una idea apoyada solo en fichas bloqueadas no pasa el filtro duro.
2. Se creó el shim `.claude/skills/idea-arena/SKILL.md`.
3. Las rayas largas se sanean en toda salida del pipeline. El test existente no se tocó.
4. `infra_budget_usd: 300` como tope duro y `infra_budget_target_usd: 200` como objetivo.
5. Briefs versionados: se quedan en `runs/<run>/prompts/` con rutas absolutas. Son el registro de
   qué recibió cada agente y pesan poco, porque referencian archivos en vez de copiarlos.
6. Capacidad: 10 a 16 horas por semana por persona (`team` en config.json). El chequeo de alcance
   solo declara inviable lo que claramente no entra; ante la duda, "viable con recorte".
7. R6 (regulación) y R7 (datos) quedaron como restricciones duras confirmadas.

Cambios respecto del plan, encontrados al implementar y probar:

- URLs repetidas: se descartan solo dentro del mismo sector. Entre sectores se conservan, porque una
  misma fuente puede respaldar hallazgos distintos.
- Shortlist: una idea que perdió su último cruce con un fallo fatal verificado no entra (queda en
  `shortlist/ranking.json`, marcada). Sin esto, una idea con fallo fatal y puntaje alto quedaba
  arriba entre las eliminadas de su ronda.
- Personas: una persona por ronda, la misma para todos los cruces de la ronda. Elegir "la que
  ninguna de las dos enfrentó" cruce por cruce no garantiza que la campeona enfrente a las 4; por
  ronda sí.
- Orden de presentación: el invariante se cumple siempre, pero con los cruces de `bracket.py` una
  idea puede quedar con 3 apariciones más como primera que como segunda (1,1% de 4.500 torneos
  simulados de 2 a 16 ideas). Probé un segundo desempate (la última posición) y no mejoró. La
  neutralización completa es `judge_both_orders`.
- Salidas ilegibles: Python las aparta como `.invalido1`; al segundo fallo escribe NO OUTPUT donde
  hay plan B (sin ataques, versión anterior de la idea, sin fichas). Un juez nunca cae en NO OUTPUT:
  al tercer fallo el run queda STUCK y lo decide una persona con `record`.
- Comandos extra: `doctor` (placeholders y consistencia), `audit` (git status contra la foto tomada
  en `init`) y `record` (decidir un cruce a mano, solo si lo pide el usuario).
- La salida de la herramienta se fuerza a UTF-8 para que las tildes no se rompan en Windows.
