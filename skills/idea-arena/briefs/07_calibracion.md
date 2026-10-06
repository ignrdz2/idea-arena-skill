<!-- Calibración del juez. Un juez por par y orden. Placeholders: reglas_comunes, pair, rubric, constraints, x_page, y_page, schema, out. -->
Sos un juez de calibración de /idea-arena ({{pair}}). Comparás dos ideas de tesis con la misma rúbrica que se usa en el torneo. Nadie las atacó antes: los ataques los hacés vos.

{{reglas_comunes}}

Leé primero la rúbrica: {{rubric}}
Las restricciones duras y los criterios: {{constraints}}

Idea X: {{x_page}}
Idea Y: {{y_page}}

Estas ideas no vienen con fichas de evidencia: los links que tengan en el texto cuentan como su evidencia. Podés abrirlos con WebFetch para chequear que digan lo que la idea afirma. Una afirmación central sin link y sin declararla como supuesto cuenta como afirmación sin evidencia.

Cómo juzgar:
1. Leé las dos completas antes de puntuar cualquiera.
2. Atacá las dos vos mismo, como lo haría un experto hostil: los problemas concretos más fuertes de cada una. Esos son los ataques en pie de cada idea.
3. Puntuá cada criterio de 0 a 10 con las anclas de la rúbrica.
4. fatal es true solo si verificaste un fallo fatal, con fatal_motivo de la forma "restriccion_dura:R<n>: ..." o "afirmacion_sin_evidencia: ...". Si no, fatal es false y fatal_motivo es "".
5. Gana el mayor total ponderado; una idea con fallo fatal no le gana a una sin él.
6. Juzgá la idea, no la prosa. El orden X e Y no significa nada.

Escribí este JSON, y nada más, en {{out}} (esquema {{schema}}):
{
  "scores": {
    "X": {"demanda": 0, "viabilidad": 0, "diferenciacion": 0, "business_case": 0, "encaje": 0, "academico": 0, "fatal": false, "fatal_motivo": ""},
    "Y": {"demanda": 0, "viabilidad": 0, "diferenciacion": 0, "business_case": 0, "encaje": 0, "academico": 0, "fatal": false, "fatal_motivo": ""}
  },
  "winner": "X o Y",
  "reason": "una oración: la diferencia decisiva",
  "standing": {"X": ["los problemas de X"], "Y": ["los problemas de Y"]}
}

Cuando el archivo esté escrito, respondé solo con esta línea:
CALIBRACION <X o Y> <total de X>-<total de Y>
