<!-- Profundización: bosquejo de arquitectura. Placeholders: reglas_comunes, idea_id, page, fichas, constraints, budget, schema_ficha, ficha_prefix, out_md, out_fichas. -->
Profundizás una idea de tesis de /idea-arena: escribís el bosquejo de arquitectura del MVP, para que el equipo decida si la presenta.

{{reglas_comunes}}

La idea: {{page}}
La evidencia verificada: {{fichas}}

Escribí en {{out_md}}, en markdown:
1. Componentes del MVP y cómo se conectan, con un diagrama en texto (bloques y flechas, o Mermaid).
2. Por cada componente: tecnología concreta, por qué esa y no una alternativa obvia, y quién del equipo lo podría tomar según el perfil de {{constraints}}.
3. Datos: qué datos usa, de dónde salen (y si requieren permiso o un socio), cómo se guardan y qué datos personales toca (Ley 18.331).
4. El desafío de ingeniería principal: qué es difícil, cómo se va a medir si funciona.
5. Qué se construye en cada semestre de 2027 y qué se muestra en cada entrega intermedia.
6. Riesgos técnicos, con un plan B por cada uno.
7. Todo tiene que entrar en USD {{budget}} por año de infraestructura.

Si buscás en la web (documentación, límites de servicios), cada fuente que uses va como ficha en {{out_fichas}} con el esquema {{schema_ficha}}, IDs que empiecen con {{ficha_prefix}} (por ejemplo {{ficha_prefix}}001) y sector "transversal". Citala por ID en el markdown. Python las verifica igual que las demás.
Escribí en {{out_fichas}}: {"nuevas_fichas": [ ... ]} (la lista puede ir vacía).

Cuando los dos archivos estén escritos, respondé solo con esta línea:
ARQUITECTURA {{idea_id}} <cantidad de componentes>
