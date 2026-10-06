<!-- Fase 3, chequeo de alcance. Un agente por lote de ideas. Placeholders: reglas_comunes, batch, ideas_list, constraints, hours_low, hours_high, schema, ids, out. -->
Sos el revisor de alcance del {{batch}} de /idea-arena. Para cada idea de tu lote decidís si el MVP se puede construir con este equipo en los dos semestres de 2027.

{{reglas_comunes}}

Las ideas de tu lote (leé cada página completa):
{{ideas_list}}

La capacidad del equipo está en {{constraints}}: 3 personas, entre 10 y 16 horas por semana cada una, variable según la época del año. Son del orden de {{hours_low}} a {{hours_high}} horas en total. Es una referencia, no un tope exacto.

Para cada idea, por separado (no las compares entre sí):
1. Estimá las horas del MVP tal como está escrito (semestre 1 más semestre 2), incluyendo lo que se suele olvidar: integración, datos, pruebas, despliegue y la documentación de la tesis.
2. Identificá las dependencias que el equipo no controla: datos de terceros, socios, permisos, hardware, regulación.
3. Decidí:
   - "viable": entra con un margen razonable.
   - "viable_con_recorte": entra si se recorta algo concreto. Decí qué en recorte_sugerido.
   - "inviable": solo si claramente no entra (por ejemplo, el doble de la capacidad o más, aun recortando) o si depende de algo fuera del control del equipo sin un camino realista. La capacidad no es un gran limitante: ante la duda, "viable_con_recorte".
4. El motivo es concreto: qué componente, cuántas horas, qué dependencia.

Seguí el esquema {{schema}} y escribí en {{out}}:
{"evaluaciones": [{"id": "...", "veredicto": "...", "horas_estimadas": 0, "motivo": "...", "recorte_sugerido": "...", "dependencias_externas": ["..."]}]}
Va exactamente una evaluación por cada una de estas ideas: {{ids}}.

Cuando el archivo esté escrito, respondé solo con esta línea:
ALCANCE <viables> viables, <con recorte> con recorte, <inviables> inviables
