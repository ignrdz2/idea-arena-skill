Preparás la validación de una idea de tesis que quedó en el top de /idea-arena. El equipo va a hablar con gente del mercado y necesita 5 preguntas que confirmen o descarten la idea rápido.

Reglas comunes de /idea-arena (valen para todos los agentes):
- Antes de empezar, leé /home/user/idea-arena-skill/runs/20261008-0025/inputs/constraints.md: son las restricciones duras, el perfil del equipo y los criterios con los que se evalúa todo. Donde diga <<COMPLETAR>> no hay información: no la supongas.
- Escribí solo los archivos que este brief te pide, y solo dentro de /home/user/idea-arena-skill/runs/20261008-0025. No crees, edites ni borres nada fuera de esa carpeta. Si necesitás espacio temporal, usá /home/user/idea-arena-skill/runs/20261008-0025/scratch/preguntas.i015.
- No inventes nada: ni datos, ni cifras, ni URLs, ni empresas, ni personas, ni contactos. Lo que no sepas, declaralo como supuesto o dejalo afuera.
- Una URL solo vale si la abriste con WebFetch en esta sesión y dice lo que afirmás. Python vuelve a pedir cada URL: si no existe, lo que se apoye en ella se descarta.
- Escribí en español, claro y concreto. No uses el carácter de raya larga ni el de semirraya: usá comas, dos puntos, paréntesis o un guion común.
- Los archivos JSON tienen que ser JSON válido (UTF-8, comillas dobles, sin comentarios ni comas finales), sin texto antes ni después.

La idea: /home/user/idea-arena-skill/runs/20261008-0025/tournament/r2/r2-m04.i015.solution.md
Su paso por el torneo (los ataques que quedaron en pie y los veredictos): /home/user/idea-arena-skill/runs/20261008-0025/shortlist/rastro/i015.md

Escribí exactamente 5 preguntas:
- Sobre hechos y comportamiento pasado, no sobre hipótesis: "¿Cómo lo resolvieron la última vez que pasó?", no "¿Usarías una app que...?".
- Cada una apunta a un supuesto de la idea o a un ataque que quedó en pie. Decí cuál en que_valida.
- a_quien: el rol concreto al que se la hacen (por ejemplo, "encargado de compras de una cadena de supermercados mediana de Montevideo").
- Sin describir la solución en la pregunta, para no sesgar la respuesta.
- Al menos una sobre cuánto cuesta hoy el problema y al menos una sobre quién decide y paga.

Escribí en /home/user/idea-arena-skill/runs/20261008-0025/shortlist/preguntas/i015.json (esquema /home/user/idea-arena-skill/runs/20261008-0025/inputs/schemas/preguntas.schema.json):
{"idea": "i015", "preguntas": [{"pregunta": "...", "a_quien": "...", "que_valida": "..."}]}

Cuando el archivo esté escrito, respondé solo con esta línea:
PREGUNTAS i015 5
