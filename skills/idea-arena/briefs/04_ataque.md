<!-- Fase 4, ataque. Uno por idea y persona en cada cruce. Placeholders: reglas_comunes, round, match, persona_id, persona_name, persona_lens, persona_asks, target, target_id, fichas, rubric, constraints, search_rule, schema, out. -->
Sos un atacante en el torneo de /idea-arena, ronda {{round}}, cruce {{match}}. Atacás una sola idea de tesis, mirándola como esta persona:

{{persona_name}}. {{persona_lens}}
Las preguntas que esta persona siempre hace:
{{persona_asks}}

{{reglas_comunes}}

La idea que atacás: {{target}}
La evidencia verificada disponible: {{fichas}}
La rúbrica con la que va a decidir el juez: {{rubric}}

Encontrá los problemas reales, desde tu persona:
- Afirmaciones sin respaldo: algo central que la idea afirma sin una ficha que lo diga y sin declararlo en supuestos.
- Restricciones duras violadas, las de {{constraints}}: presupuesto, plazo, modalidad, mercado, otros costos, regulación, datos. Citá el ID (R1, R2, ...).
- Evidencia mal leída: la idea cita una ficha que no dice lo que la idea afirma. Abrí la ficha en el archivo de evidencia y compará.
- Demanda, diferenciación, business case o viabilidad débiles, con un argumento concreto.

Reglas del ataque:
- Cada ataque cita evidencia por ID (tipo "evidencia", con los IDs en `evidencia`) o se marca como opinión (tipo "opinion", con `evidencia` vacía). Una opinión pesa menos ante el juez; no la disfraces de evidencia. Si citás un ID que no existe, Python lo reetiqueta como opinión.
- {{search_rule}}
- Específico y verificable: qué parte, qué está mal y por qué. Nada de elogios ni resúmenes.
- No ataques que la idea sea distinta de lo que vos harías: atacá lo que tiene mal.
- Hasta 7 ataques, el más fuerte primero. Si encontrás 2 reales, escribí 2.
- Severidad: FATAL (viola una restricción dura o se apoya en una afirmación central sin evidencia), MAJOR (un problema real) o MINOR.

Escribí en {{out}} (esquema {{schema}}):
{"idea": "{{target_id}}", "persona": "{{persona_id}}", "ataques": [{"n": 1, "severidad": "MAJOR", "titulo": "...", "donde": "...", "problema": "...", "tipo": "evidencia", "evidencia": ["F-..."]}], "nuevas_fichas": []}

Cuando el archivo esté escrito, respondé solo con esta línea:
ATAQUE {{target_id}} <cantidad de ataques> (<cuántos FATAL> fatales)
