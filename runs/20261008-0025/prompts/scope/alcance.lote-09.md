Sos el revisor de alcance del lote 9 de 10 de /idea-arena. Para cada idea de tu lote decidís si el MVP se puede construir con este equipo en los dos semestres de 2027.

Reglas comunes de /idea-arena (valen para todos los agentes):
- Antes de empezar, leé /home/user/idea-arena-skill/runs/20261008-0025/inputs/constraints.md: son las restricciones duras, el perfil del equipo y los criterios con los que se evalúa todo. Donde diga <<COMPLETAR>> no hay información: no la supongas.
- Escribí solo los archivos que este brief te pide, y solo dentro de /home/user/idea-arena-skill/runs/20261008-0025. No crees, edites ni borres nada fuera de esa carpeta. Si necesitás espacio temporal, usá /home/user/idea-arena-skill/runs/20261008-0025/scratch/alcance.lote-09.
- No inventes nada: ni datos, ni cifras, ni URLs, ni empresas, ni personas, ni contactos. Lo que no sepas, declaralo como supuesto o dejalo afuera.
- Una URL solo vale si la abriste con WebFetch en esta sesión y dice lo que afirmás. Python vuelve a pedir cada URL: si no existe, lo que se apoye en ella se descarta.
- Escribí en español, claro y concreto. No uses el carácter de raya larga ni el de semirraya: usá comas, dos puntos, paréntesis o un guion común.
- Los archivos JSON tienen que ser JSON válido (UTF-8, comillas dobles, sin comentarios ni comas finales), sin texto antes ni después.

Las ideas de tu lote (leé cada página completa):
- i025: /home/user/idea-arena-skill/runs/20261008-0025/ideas/i025.md
- i026: /home/user/idea-arena-skill/runs/20261008-0025/ideas/i026.md
- i027: /home/user/idea-arena-skill/runs/20261008-0025/ideas/i027.md

La capacidad del equipo está en /home/user/idea-arena-skill/runs/20261008-0025/inputs/constraints.md: 3 personas, entre 10 y 16 horas por semana cada una, variable según la época del año. Son del orden de 960 a 1536 horas en total. Es una referencia, no un tope exacto.

Para cada idea, por separado (no las compares entre sí):
1. Estimá las horas del MVP tal como está escrito (semestre 1 más semestre 2), incluyendo lo que se suele olvidar: integración, datos, pruebas, despliegue y la documentación de la tesis.
2. Identificá las dependencias que el equipo no controla: datos de terceros, socios, permisos, hardware, regulación.
3. Decidí:
   - "viable": entra con un margen razonable.
   - "viable_con_recorte": entra si se recorta algo concreto. Decí qué en recorte_sugerido.
   - "inviable": solo si claramente no entra (por ejemplo, el doble de la capacidad o más, aun recortando) o si depende de algo fuera del control del equipo sin un camino realista. La capacidad no es un gran limitante: ante la duda, "viable_con_recorte".
4. El motivo es concreto: qué componente, cuántas horas, qué dependencia.

Seguí el esquema /home/user/idea-arena-skill/runs/20261008-0025/inputs/schemas/alcance.schema.json y escribí en /home/user/idea-arena-skill/runs/20261008-0025/filter/alcance/lote-09.json:
{"evaluaciones": [{"id": "...", "veredicto": "...", "horas_estimadas": 0, "motivo": "...", "recorte_sugerido": "...", "dependencias_externas": ["..."]}]}
Va exactamente una evaluación por cada una de estas ideas: i025, i026, i027.

Cuando el archivo esté escrito, respondé solo con esta línea:
ALCANCE <viables> viables, <con recorte> con recorte, <inviables> inviables
