<!-- Profundización: tabla de competidores. Placeholders: reglas_comunes, idea_id, page, fichas, constraints, budget, schema_ficha, ficha_prefix, out_md, out_fichas. -->
Profundizás una idea de tesis de /idea-arena: escribís la tabla de competidores, para que el equipo sepa contra quién compite de verdad.

{{reglas_comunes}}

La idea: {{page}}
La evidencia verificada: {{fichas}}

Empezá por los competidores que la idea ya cita y buscá en la web los que falten: en Uruguay primero, después en LATAM, y los referentes globales que un cliente uruguayo podría usar igual. Incluí las alternativas no tecnológicas (planillas, WhatsApp, una persona dedicada, un estudio contable): muchas veces son el competidor real.

Escribí en {{out_md}}, en markdown:
1. Una tabla: competidor, país, a quién le vende, precio (si es público), qué hace bien, qué hueco deja, y la ficha que lo respalda.
2. El posicionamiento de la idea frente a ellos: en qué gana, en qué pierde, y qué tan rápido la podrían copiar.
3. Lo que no encontraste y habría que preguntar en las entrevistas.

Cada fuente que uses va como ficha en {{out_fichas}} con el esquema {{schema_ficha}}, source_type "competidor" cuando corresponda, IDs que empiecen con {{ficha_prefix}} (por ejemplo {{ficha_prefix}}001) y sector "transversal". Citala por ID en la tabla. Python las verifica igual que las demás; una fila sin ficha verificable se marca como no verificada.
Escribí en {{out_fichas}}: {"nuevas_fichas": [ ... ]}

Cuando los dos archivos estén escritos, respondé solo con esta línea:
COMPETIDORES {{idea_id}} <cantidad de competidores>
