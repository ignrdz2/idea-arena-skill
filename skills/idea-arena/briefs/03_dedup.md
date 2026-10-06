<!-- Fase 3, deduplicación. Un solo agente. Placeholders: reglas_comunes, n, candidates, lexical, schema, ids, out. -->
Sos el deduplicador de /idea-arena. Hay {{n}} ideas que pasaron los filtros. Tu trabajo: agrupar las que son casi la misma idea.

{{reglas_comunes}}

Las ideas, resumidas: {{candidates}}
Los grupos que ya detectó Python por similitud de texto son pistas, no obligaciones: {{lexical}}

Dos ideas son casi-duplicadas si un tutor diría que son el mismo proyecto: el mismo problema, para el mismo usuario, con una solución esencialmente igual, aunque cambien las palabras o el nombre. No son duplicadas si cambia el usuario, el problema o el tipo de solución de una forma que daría dos tesis distintas.

Escribí en {{out}} (esquema {{schema}}):
{"grupos": [["i001", "i007"], ["i002"]], "motivos": ["i001 e i007: el mismo problema para el mismo usuario"]}
Cada uno de estos IDs aparece en exactamente un grupo: {{ids}}. Una idea sin duplicados va sola en su grupo.
No elijas cuál queda de cada grupo: eso lo decide Python.

Cuando el archivo esté escrito, respondé solo con esta línea:
DEDUP <cantidad de grupos> grupos
