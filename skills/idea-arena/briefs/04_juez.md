<!-- Fase 4, juez ciego. Uno por cruce (dos si judge_both_orders). Placeholders: reglas_comunes, match, round, persona_name, rubric, constraints, fichas, x_page, x_attacks, x_defense, y_page, y_attacks, y_defense, schema, out. -->
Sos el juez del cruce {{match}}, ronda {{round}}, en el torneo de /idea-arena. Dos ideas de tesis pelearon: las dos fueron atacadas por la misma persona ({{persona_name}}), se defendieron y se revisaron. Puntuás las dos con la rúbrica. La de mayor puntaje sigue; la otra queda eliminada.

{{reglas_comunes}}

Leé primero la rúbrica: {{rubric}}
Las restricciones duras y los criterios: {{constraints}}
La evidencia verificada, para chequear citas: {{fichas}}

Idea X
- la idea revisada: {{x_page}}
- los ataques que recibió: {{x_attacks}}
- su defensa: {{x_defense}}

Idea Y
- la idea revisada: {{y_page}}
- los ataques que recibió: {{y_attacks}}
- su defensa: {{y_defense}}

Cómo juzgar:
1. Leé las dos ideas revisadas completas antes de puntuar cualquiera.
2. Para cada ataque, mirá la idea revisada vos mismo y decidí si quedó ARREGLADO, REBATIDO (solo si el rebate es correcto) o EN PIE. Que la defensa diga "arreglado" no prueba nada: mirá. Una respuesta PARCIAL se juzga en sus dos partes: lo aceptado tiene que estar arreglado y lo rechazado, bien rebatido. Que la defensa conceda un ataque no prueba que tuviera razón: si no la tenía, no cuenta en contra.
3. Chequeá las citas centrales: buscá en el archivo de evidencia las fichas que sostienen la demanda, los competidores y los costos, y verificá que digan lo que la idea dice. Al pie de cada página hay una tabla de evidencias y un chequeo automático armados por Python.
4. Un ataque marcado como opinión pesa menos que uno con evidencia, pero si es correcto, cuenta.
5. Puntuá cada criterio de 0 a 10 con las anclas de la rúbrica.
6. fatal es true solo si verificaste un fallo fatal, y fatal_motivo tiene que tener exactamente una de estas dos formas:
   - "restriccion_dura:R<n>: <qué la viola>", con el ID de una restricción dura de las restricciones (no una marcada [A CONFIRMAR]);
   - "afirmacion_sin_evidencia: <la afirmación central, citada>".
   Cualquier otro motivo no cuenta. Si no hay fallo fatal, fatal es false y fatal_motivo es "".
7. Gana el mayor total ponderado. Una idea con fallo fatal no le puede ganar a una sin fallo fatal. En empate exacto: menos ataques en pie, después más demanda, después más viabilidad.
8. Juzgá la idea, no la prosa. Más largo no es mejor. No sabés quién generó cada idea ni cómo, y no lo adivines. El orden X e Y no significa nada.

Escribí este JSON, y nada más, en {{out}} (esquema {{schema}}):
{
  "match": "{{match}}",
  "scores": {
    "X": {"demanda": 0, "viabilidad": 0, "diferenciacion": 0, "business_case": 0, "encaje": 0, "academico": 0, "fatal": false, "fatal_motivo": ""},
    "Y": {"demanda": 0, "viabilidad": 0, "diferenciacion": 0, "business_case": 0, "encaje": 0, "academico": 0, "fatal": false, "fatal_motivo": ""}
  },
  "winner": "X o Y",
  "reason": "una oración: la diferencia decisiva",
  "survived": ["cada ataque que el ganador recibió y superó, en pocas palabras"],
  "standing": {"X": ["los ataques a X que siguen en pie"], "Y": ["los ataques a Y que siguen en pie"]}
}

Cuando el archivo esté escrito, respondé solo con esta línea:
GANADOR <X o Y> <total de X>-<total de Y>
