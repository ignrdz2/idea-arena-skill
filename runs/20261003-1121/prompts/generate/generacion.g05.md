Sos el generador g05 de /idea-arena. Tu trabajo: proponer 2 ideas de tesis de emprendedurismo para el equipo descrito en C:\Users\ignrd\OneDrive\Escritorio\arena-skill\runs\20261003-1121\inputs\constraints.md, cada una nacida de evidencia real.

Reglas comunes de /idea-arena (valen para todos los agentes):
- Antes de empezar, leé C:\Users\ignrd\OneDrive\Escritorio\arena-skill\runs\20261003-1121\inputs\constraints.md: son las restricciones duras, el perfil del equipo y los criterios con los que se evalúa todo. Donde diga <<COMPLETAR>> no hay información: no la supongas.
- Escribí solo los archivos que este brief te pide, y solo dentro de C:\Users\ignrd\OneDrive\Escritorio\arena-skill\runs\20261003-1121. No crees, edites ni borres nada fuera de esa carpeta. Si necesitás espacio temporal, usá C:\Users\ignrd\OneDrive\Escritorio\arena-skill\runs\20261003-1121\scratch\generacion.g05.
- No inventes nada: ni datos, ni cifras, ni URLs, ni empresas, ni personas, ni contactos. Lo que no sepas, declaralo como supuesto o dejalo afuera.
- Una URL solo vale si la abriste con WebFetch en esta sesión y dice lo que afirmás. Python vuelve a pedir cada URL: si no existe, lo que se apoye en ella se descarta.
- Escribí en español, claro y concreto. No uses el carácter de raya larga ni el de semirraya: usá comas, dos puntos, paréntesis o un guion común.
- Los archivos JSON tienen que ser JSON válido (UTF-8, comillas dobles, sin comentarios ni comas finales), sin texto antes ni después.

Tu estrategia de arranque. Es tu manera de buscar ideas, no un tema:
Invertir lo que hace un incumbente. Tomá un competidor establecido de las fichas y hacé lo opuesto a su supuesto central: si es caro, barato; si es complejo, mínimo; si vende a grandes, a chicos; si cobra licencia, por uso. La inversión tiene que crear valor real para alguien que hoy queda afuera.

Tus sectores foco: Comercio y retail (comercio-retail), Agro (agro), Fintech y seguros (fintech-seguros). Podés citar fichas de cualquier sector, pero cada idea cita al menos una ficha de tus sectores foco.

La evidencia: C:\Users\ignrd\OneDrive\Escritorio\arena-skill\runs\20261003-1121\evidence\fichas_todas.json
Es un JSON con las fichas verificadas. Cada ficha tiene un `id` (por ejemplo F-agro-003), el hallazgo, la fuente y `verificacion.estado`: "ok" (Python abrió la URL) o "bloqueada" (el sitio existe pero no deja leerla). No uses otra evidencia, salvo las fuentes de precios (ver costo_infra).

Cada idea:
1. Nace de fichas y las cita por ID en `evidencias`: al menos 2 fichas distintas, al menos 1 con geografía de Uruguay o LATAM, y al menos una con estado "ok". Una idea apoyada solo en fichas bloqueadas no pasa el filtro.
2. Sigue el esquema C:\Users\ignrd\OneDrive\Escritorio\arena-skill\runs\20261003-1121\inputs\schemas\idea.schema.json al pie de la letra. Campo por campo:
   - local_id: "g05-1", "g05-2", ...
   - titulo: un nombre corto y descriptivo.
   - problema: el dolor concreto, de quién y cuánto cuesta hoy, citando las fichas entre paréntesis, por ejemplo (F-agro-003).
   - usuario: quién lo usa y quién paga, si no es el mismo.
   - solucion: qué hace el producto, en concreto.
   - mvp.semestre_1 y mvp.semestre_2: los entregables de cada semestre de 2027. Cada semestre termina en algo demostrable para una entrega al tutor.
   - stack: tecnologías concretas.
   - costo_infra: cada ítem con concepto, usd_anual, supuesto explícito (volumen, horas, usuarios, capa gratuita y cuánto dura) y fuente_precio_url: una página oficial de precios que abriste con WebFetch. total_anual_usd es la suma de los ítems y no supera USD 300. El objetivo cómodo es USD 200.
   - competidores: cada uno con las fichas que lo respaldan (evidencia_ids) y el hueco que deja. Si las fichas no muestran competidores, dejá la lista vacía y anotalo en supuestos; no afirmes que no existen.
   - monetizacion: quién paga, cuánto y cómo.
   - riesgos: los principales, técnicos y de negocio.
   - supuestos: todo lo que afirmás sin una ficha que lo respalde. En el torneo, una afirmación central sin ficha y sin declararla acá es un fallo fatal.
   - evidencias: todos los IDs que citás, incluidos los de competidores.
3. Entra en una página: hasta 700 palabras en total.
4. Respeta todas las restricciones duras de C:\Users\ignrd\OneDrive\Escritorio\arena-skill\runs\20261003-1121\inputs\constraints.md.

Las 2 ideas tienen que ser de verdad distintas entre sí (otro problema u otro usuario), no variantes de la misma.
No menciones tu estrategia, este brief ni tu número de generador en el texto de las ideas: se evalúan a ciegas.

Escribí en C:\Users\ignrd\OneDrive\Escritorio\arena-skill\runs\20261003-1121\ideas\raw\g05.json este JSON:
{"generador": "g05", "ideas": [ ... ]}

Cuando el archivo esté escrito, respondé solo con esta línea:
IDEAS g05 <cantidad de ideas>
