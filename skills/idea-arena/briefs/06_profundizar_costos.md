<!-- Profundización: modelo de costos. Placeholders: reglas_comunes, idea_id, page, fichas, constraints, budget, schema_ficha, ficha_prefix, out_md, out_fichas. -->
Profundizás una idea de tesis de /idea-arena: escribís el modelo de costos de infraestructura del MVP para 2027, para que el equipo sepa si de verdad entra en el presupuesto.

{{reglas_comunes}}

La idea: {{page}}
La evidencia verificada: {{fichas}}

Escribí en {{out_md}}, en markdown:
1. Una tabla mes a mes de 2027 (o por trimestre) con cada servicio: concepto, unidad de cobro, cantidad supuesta, precio unitario, costo, y la fuente oficial del precio.
2. Tres escenarios: mínimo (solo desarrollo), esperado (desarrollo más piloto con usuarios reales) y estrés (el doble del uso esperado). El total anual de cada uno, contra el tope de USD {{budget}}.
3. Capas gratuitas y créditos: cuáles usa, cuánto duran, qué pasa cuando terminan. Solo los que la fuente documenta.
4. Lo que no es infraestructura pero cuesta: dominios, APIs pagas, licencias, tiendas de aplicaciones. Restricción R5 de {{constraints}}.
5. Las palancas para bajar el costo si se pasa del tope.
6. Los supuestos, todos a la vista.

Cada precio sale de una página oficial que abriste con WebFetch. Cada fuente va como ficha en {{out_fichas}} con el esquema {{schema_ficha}}, source_type "precios", IDs que empiecen con {{ficha_prefix}} (por ejemplo {{ficha_prefix}}001) y sector "transversal". Citala por ID en la tabla. Python las verifica igual que las demás.
Escribí en {{out_fichas}}: {"nuevas_fichas": [ ... ]}

Cuando los dos archivos estén escritos, respondé solo con esta línea:
COSTOS {{idea_id}} esperado USD <total anual> de {{budget}}
