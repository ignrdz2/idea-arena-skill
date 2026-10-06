<!-- Fase 5, preguntas de validación. Una por idea del top. Placeholders: reglas_comunes, idea_id, n_questions, page, trail, schema, out. -->
Preparás la validación de una idea de tesis que quedó en el top de /idea-arena. El equipo va a hablar con gente del mercado y necesita {{n_questions}} preguntas que confirmen o descarten la idea rápido.

{{reglas_comunes}}

La idea: {{page}}
Su paso por el torneo (los ataques que quedaron en pie y los veredictos): {{trail}}

Escribí exactamente {{n_questions}} preguntas:
- Sobre hechos y comportamiento pasado, no sobre hipótesis: "¿Cómo lo resolvieron la última vez que pasó?", no "¿Usarías una app que...?".
- Cada una apunta a un supuesto de la idea o a un ataque que quedó en pie. Decí cuál en que_valida.
- a_quien: el rol concreto al que se la hacen (por ejemplo, "encargado de compras de una cadena de supermercados mediana de Montevideo").
- Sin describir la solución en la pregunta, para no sesgar la respuesta.
- Al menos una sobre cuánto cuesta hoy el problema y al menos una sobre quién decide y paga.

Escribí en {{out}} (esquema {{schema}}):
{"idea": "{{idea_id}}", "preguntas": [{"pregunta": "...", "a_quien": "...", "que_valida": "..."}]}

Cuando el archivo esté escrito, respondé solo con esta línea:
PREGUNTAS {{idea_id}} {{n_questions}}
