<!-- Fase 4, defensa y revisión. Una por idea en cada cruce. Placeholders: reglas_comunes, round, match, idea_id, own_page, own_json, attacks, fichas, rubric, schema_idea, schema_defense, search_rule, budget, max_words, word_check, defense_out, idea_out. -->
Defendés una idea de tesis en el torneo de /idea-arena, ronda {{round}}, cruce {{match}}. La atacaron. Ahora respondés cada ataque y escribís la versión revisada de la idea. Un juez va a comparar tu idea revisada con la del otro lado del cruce.

{{reglas_comunes}}

Tu idea, como la ve el juez: {{own_page}}
Tu idea en JSON, que es lo que vas a revisar: {{own_json}}
Los ataques que recibió: {{attacks}}
La evidencia verificada: {{fichas}}
La rúbrica: {{rubric}}

Tu papel: sos quien defiende esta idea. El juez revisa cada ataque por su cuenta, así que no te sirve negar lo que es cierto ni conceder por cortesía lo que no lo es. Que un ataque suene convincente no le da la razón: la tiene si resiste un chequeo.

Hacé esto:
1. Antes de decidir, chequeá cada ataque contra el material que tenés:
   - Si cita fichas, buscalas en el archivo de evidencia: ¿dicen lo que el ataque afirma?
   - Si dice que una afirmación no tiene respaldo, buscala en la idea: ¿ya está declarada en supuestos, o la respalda una ficha citada?
   - Si invoca una restricción dura, leela en las restricciones: ¿la idea de verdad la viola, o el ataque le pide más de lo que la restricción dice?
   - Si es una opinión sin evidencia: ¿qué la sostiene? Una opinión que la idea ya contempla, o que una ficha contradice, se rebate.
   - ¿Ataca algo que la idea dice, o algo que no dice?
2. Respondé cada ataque por su número con una de tres decisiones:
   - CONCEDE: tiene razón entera. Lo arreglás en la idea y decís cómo.
   - PARCIAL: tiene razón en una parte. Decí qué parte aceptás y cómo la arreglás, y qué parte no y por qué, con la misma clase de prueba que un REBUT. Es PARCIAL solo si rechazás algo que el ataque de verdad afirma; si aceptás todo y solo agregás contexto, es CONCEDE.
   - REBUT: está equivocado. Mostrás por qué con algo que el juez pueda chequear: una ficha (por ID), el texto de la idea, la rúbrica, las restricciones o una cuenta concreta. Un REBUT que solo insiste no vale nada.
   Conceder no suma por sí mismo. Un ataque correcto y bien arreglado deja de pesar, pero conceder uno equivocado debilita la idea sin motivo y suele llevar a recortar lo que la hacía valiosa. Un REBUT correcto vale tanto como un buen arreglo.
3. Escribí la idea revisada completa, con el mismo esquema ({{schema_idea}}). Arreglá lo concedido, la parte aceptada de cada PARCIAL y lo que los ataques te hicieron notar: recortá alcance, bajá costos o pasá afirmaciones a supuestos si hace falta. No toques lo que rebatiste. No empieces de cero: es la misma idea, mejorada, y no copies a la idea rival. Si un ataque muestra que una restricción dura no se puede cumplir, decilo en la defensa; no lo escondas.
4. {{search_rule}}
5. Seguí respetando: costo total hasta USD {{budget}}, solo IDs de fichas existentes, una página (hasta {{max_words}} palabras). Arreglar un ataque no justifica pasarse de una página: recortá lo repetido. Con la idea revisada escrita, corré `{{word_check}}`, que cuenta las palabras igual que el filtro; si dice MAL, recortá y volvé a correrlo hasta que diga OK.
6. Si el archivo de ataques dice que no hubo ataques, escribí "respuestas": [] y reenviá la idea con solo los arreglos que sepas que necesita.
7. En el texto de la idea no menciones el torneo, la ronda ni quién atacó.

Escribí la defensa en {{defense_out}} (esquema {{schema_defense}}):
{"idea": "{{idea_id}}", "respuestas": [{"ataque": 1, "decision": "CONCEDE", "detalle": "...", "evidencia": []}], "nuevas_fichas": []}

Escribí la idea revisada en {{idea_out}}: el JSON completo de la idea, con los mismos campos que {{own_json}}.

Cuando los dos archivos estén escritos, respondé solo con esta línea:
DEFENSA {{idea_id}} concedidos <n> parciales <n> rebatidos <n>
