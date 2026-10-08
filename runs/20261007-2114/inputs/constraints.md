# Restricciones y contexto del equipo

Todos los agentes de /idea-arena leen este archivo: investigadores, generadores, revisores,
atacantes, defensores y jueces. Tiene tres partes:

1. **Restricciones duras.** Eliminan ideas. En el torneo, violar una es un fallo fatal.
2. **Perfil del equipo.** Contexto para generar ideas y juzgar el encaje. Tiene placeholders
   `<<COMPLETAR: ...>>` para que cada integrante agregue lo suyo.
3. **Criterios blandos con pesos.** Los mismos que usa el juez (`rubric.md`).

Cómo editarlo:
- Cada restricción dura tiene un ID (**R1**, **R2**, ...) que los jueces citan. Para agregar una,
  usá el número siguiente. Si escribís `[A CONFIRMAR]` en la misma línea, el juez la trata como
  criterio blando hasta que saques la marca.
- `300`, `200`, `960` y `1536` se
  completan solos con los valores de `config.json` en la copia de cada run. Para cambiar el tope,
  cambiá `infra_budget_usd` en `config.json`, no el texto.
- Mientras un placeholder diga `<<COMPLETAR`, los agentes tienen instrucción de tratarlo como "sin
  información" y no suponer nada. `python skills/idea-arena/idea_arena.py doctor` lista los que
  faltan.
- Si cambiás los pesos de la parte 3, cambiá también `rubric.md` y `CRITERIA` en
  `ia_tournament.py`: un test verifica que los tres coincidan.
- No uses los caracteres de raya larga ni de semirraya: un test del repo los prohíbe en todos los
  archivos.

## Contexto

- Tesis de ingeniería informática, modalidad proyecto de emprendedurismo.
- Equipo de 3 estudiantes de informática de nivel avanzado; 2 con experiencia laboral.
- Calendario: la propuesta se presenta en diciembre de 2026. Si se aprueba, el desarrollo ocupa los
  dos semestres de 2027, con 2 entregas intermedias a un profesor tutor.
- Objetivo principal: aprobar con un buen MVP más un business case. Seguir con el proyecto después
  no está descartado, pero no es el objetivo central. Hay que evitar costos altos.
- Mercado inicial: Uruguay y LATAM, no global.
- No hay ninguna idea elegida de antemano, ni un sector preferido.

## 1. Restricciones duras

- **R1** (presupuesto): el costo de infraestructura del MVP no supera USD 300 por año
  durante 2027 (desarrollo, pruebas y demo), sin financiamiento de la facultad. Cada costo declara su
  supuesto (volumen, horas, usuarios) y, si se pudo abrir, una fuente oficial de precios. Sin fuente,
  vale una estimación por encima, declarada como tal: no viola R1 mientras el total con la estimación
  entre en el tope. Una capa gratuita o un crédito cuenta solo si la fuente lo documenta y el supuesto
  dice cuánto dura.
- **R2** (plazo): un MVP funcional se puede construir con este equipo en los dos semestres de 2027,
  con algo demostrable en cada una de las 2 entregas intermedias. La capacidad de referencia está en
  la parte 2: es una guía, no un tope exacto; solo es inviable lo que claramente no entra.
- **R3** (modalidad): es un proyecto de emprendedurismo: producto más business case, con un cliente
  identificable, una propuesta de valor y un modelo de ingresos. Una investigación sin producto o un
  servicio de consultoría no califica.
- **R4** (mercado): el mercado inicial es Uruguay o LATAM, con usuarios o clientes que el equipo
  puede contactar desde Uruguay para validar la idea antes de diciembre de 2026.
- **R5** (otros costos): no requiere licencias de software, datos pagos, hardware ni servicios que
  superen el presupuesto o que tenga que pagar la facultad.
- **R6** (regulación): el MVP no requiere una licencia o habilitación regulatoria imposible de
  obtener por un equipo de estudiantes en el plazo; por ejemplo, operar como entidad financiera
  supervisada o certificar un dispositivo médico. Usar datos personales está permitido si hay un
  camino de cumplimiento realista con la Ley 18.331 de Protección de Datos Personales.
- **R7** (datos): no depende de datos a los que el equipo no tiene acceso legal, salvo que haya un
  socio identificado en la tabla de contactos de la parte 2 que los provea. Datos abiertos, públicos
  o generados por el propio producto están permitidos.

## 2. Perfil del equipo

### Capacidad de referencia

- 3 personas, entre 10 y 16 horas por semana cada una, y puede variar según la época del año
  (parciales, trabajo). Con unas 32 semanas lectivas en 2027, da del orden de 960 a
  1536 horas en total.
- No es un gran limitante: sirve para detectar alcances claramente imposibles, no para afinar.
- Semanas efectivas por semestre según el calendario de la facultad: 16

### Perfil técnico común

- Desarrollo full-stack avanzado, con foco en IA, backend y datos.
- IA aplicada: RAG, Text-to-SQL, embeddings, bases vectoriales (Qdrant) y orquestación de agentes.
- Nube: Azure y AWS (EC2, IAM).
- Contenedores: Docker.
- Facilidad con temas relacionados dentro del área y capacidad para aprender cosas nuevas.

### Integrante 1

- Nombre o rol: JuanR
- Fortalezas técnicas propias (además del perfil común): integración de IA, desarrollo full-stack
- Experiencia laboral (rubro, rol, años): No
- Intereses (sectores o problemas que le motivan): IA, datos
- Horas por semana en 2027, si difiere de 10 a 16: 16

### Integrante 2

- Nombre o rol: JuanC
- Fortalezas técnicas propias (además del perfil común): desarrollo full-stack
- Experiencia laboral (rubro, rol, años): desarrollo de software, developer, +4 años
- Intereses (sectores o problemas que le motivan): no se sabe
- Horas por semana en 2027, si difiere de 10 a 16: 10

### Integrante 3

- Nombre o rol: Gastón
- Fortalezas técnicas propias (además del perfil común): IA, AWS, desarrollo full-stack
- Experiencia laboral (rubro, rol, años): desarrollo de software, developer, +4 años
- Intereses (sectores o problemas que le motivan): no se sabe
- Horas por semana en 2027, si difiere de 10 a 16: 10

### Contactos en industrias concretas

Personas u organizaciones a las que el equipo puede llegar para entrevistas, datos o un piloto.
Sirven para el criterio de encaje y para la restricción R7. Si una fila dice `<<COMPLETAR>>`, no hay
contacto: los agentes no lo suponen.

| Sector | Organización | Persona o rol | Qué puede aportar (entrevistas, datos, piloto) | Quién del equipo lo conoce |
| --- | --- | --- | --- | --- |
| <<COMPLETAR>> | <<COMPLETAR>> | <<COMPLETAR>> | <<COMPLETAR>> | <<COMPLETAR>> |
| <<COMPLETAR>> | <<COMPLETAR>> | <<COMPLETAR>> | <<COMPLETAR>> | <<COMPLETAR>> |

### Preferencias del equipo

- Sectores o problemas que el equipo preferiría (no obligatorio, no elimina ideas):
  sin preferencias
- Sectores o tipos de proyecto que el equipo preferiría evitar (no elimina ideas, baja el encaje):
  sin preferencias

## 3. Criterios blandos con pesos

Los mismos seis criterios y pesos que usa el juez. Las anclas de cada puntaje están en `rubric.md`.

| criterio | peso | qué mira |
| --- | --- | --- |
| demanda | 25 | Evidencia de demanda en Uruguay o LATAM: el dolor, quién lo sufre, cuánto cuesta, señales de pago. |
| viabilidad | 25 | Viabilidad con el presupuesto y el plazo: alcance para dos semestres, entregas demostrables, costo cómodo (objetivo USD 200 por año; hasta USD 300 es válido pero puntúa menos). |
| diferenciacion | 20 | Diferenciación frente a los competidores de las fichas, y si el hueco es real. |
| business_case | 15 | Calidad del business case: quién paga, cuánto, cuántos, canal, supuestos a la vista. |
| encaje | 10 | Encaje con el perfil, los intereses y los contactos del equipo. |
| academico | 5 | Valor académico: un desafío de ingeniería que justifique una tesis. |
