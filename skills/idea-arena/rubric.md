# La rúbrica de /idea-arena

Cada cruce del torneo se puntúa con esta página. El juez puntúa las dos ideas, `ia_tournament.py`
hace la cuenta y la de mayor total ponderado sigue. La otra queda eliminada.

## Los seis criterios

Cada criterio va de 0 a 10. El peso es cuánto vale sobre el total de 100. La primera columna es la
clave que el juez usa en el JSON del veredicto.

| criterio | peso | la pregunta |
| --- | --- | --- |
| demanda | 25 | Evidencia de demanda: ¿las fichas muestran que alguien concreto en Uruguay o LATAM tiene este problema, que hoy le cuesta, y que pagaría o usaría una solución? |
| viabilidad | 25 | Viabilidad con este presupuesto y este plazo: ¿el MVP se construye con 3 personas en los dos semestres de 2027, con algo demostrable en cada entrega, y la infraestructura entra en el tope anual? |
| diferenciacion | 20 | Diferenciación: ¿qué hace distinto a lo que ya existe (según las fichas), y ese hueco es real o es un segmento que nadie atiende porque no paga? |
| business_case | 15 | Calidad del business case: ¿está claro quién paga, cuánto, cuántos son, cómo se llega a ellos, y los supuestos están declarados? |
| encaje | 10 | Encaje con el equipo: ¿aprovecha lo que el equipo sabe hacer y sus contactos, sin depender de capacidades que no tiene? |
| academico | 5 | Valor académico: ¿hay un desafío de ingeniería que justifique una tesis, más allá de integrar servicios? |

Total ponderado = (demanda x 25 + viabilidad x 25 + diferenciacion x 20 + business_case x 15 +
encaje x 10 + academico x 5) / 10. Da un número de 0 a 100.

## Anclas

Usá toda la escala. Un 7 no es un default amable.

**Demanda**
- 10: varias fichas verificadas, de fuentes distintas y locales, muestran el dolor, quién lo sufre y
  cuánto cuesta; hay señales de pago (gente pagando por algo peor, ofertas laborales, presupuestos).
- 7: el dolor está bien respaldado, pero la disposición a pagar es un supuesto declarado.
- 4: una sola ficha, o fichas genéricas ("el sector enfrenta desafíos"), o evidencia solo extranjera.
- 0 a 2: la demanda es una opinión del que escribió la idea.

**Viabilidad**
- 10: alcance realista con margen; cada semestre termina en algo demostrable; costo con supuestos
  verificables, cómodo por debajo del objetivo de USD 200; sin dependencias externas críticas.
- 7: entra con un recorte claro, o el costo está entre el objetivo y el tope, o hay una dependencia
  externa con plan B.
- 4: alcance inflado o una dependencia externa sin plan B (datos, socio, permiso).
- 0 a 2: no entra en dos semestres, o el costo real supera el tope.

**Diferenciacion**
- 10: el hueco frente a los competidores de las fichas es concreto y defendible por un tiempo.
- 7: hay diferencia real, pero un competidor la podría copiar rápido.
- 4: "más barato" o "más fácil" sin explicar por qué el competidor no lo hace.
- 0 a 2: ya existe igual en el mercado local, o ignora competidores obvios.

**Business_case**
- 10: cliente, precio, tamaño del mercado inicial, canal y costos coherentes entre sí, con los
  supuestos a la vista.
- 7: coherente, con uno de esos elementos flojo.
- 4: "modelo freemium" o "suscripción" sin quién paga ni cuánto.
- 0 a 2: no hay modelo de ingresos.

**Encaje**
- 10: usa de lleno el perfil del equipo y, si los hay, sus contactos.
- 7: usa parte del perfil; lo que falta se aprende en el plazo.
- 4: depende de una capacidad central que el equipo no tiene.
- 0 a 2: no tiene relación con el equipo.

**Academico**
- 10: un problema técnico no trivial, con algo que medir o comparar.
- 7: ingeniería sólida pero conocida.
- 4: casi todo es integración de servicios.
- 0 a 2: no hay componente de ingeniería.

## La evidencia y los ataques

- Al pie de cada idea hay una tabla de evidencias armada por Python a partir de las fichas
  verificadas, y un chequeo automático. Usalos para comprobar las citas.
- Una ficha con verificación `bloqueada` existe (el servidor respondió) pero no se pudo leer:
  vale menos que una `ok`. Una idea apoyada solo en fichas bloqueadas no pasa el filtro.
- Un ataque marcado como opinión pesa menos que uno con evidencia, pero si es correcto, cuenta.
- Afirmar algo que no está en las fichas y no declararlo en supuestos es grave (ver abajo).
- Un ítem de costo sin fuente de precio verificada aparece como estimación, con un aviso en el
  chequeo automático. No descarta la idea: en viabilidad, mirá si la estimación es razonable y
  conservadora, y si el total seguiría bajo el tope aunque el precio real fuera bastante mayor.

## La regla del fallo fatal

Marcá una idea como `fatal` solo cuando verificaste uno de estos dos casos, y escribí
`fatal_motivo` exactamente con una de estas formas:

- `restriccion_dura:R<n>: <qué la viola>`: viola una restricción dura de `constraints.md`. Las
  restricciones marcadas `[A CONFIRMAR]` no cuentan como fatales.
- `afirmacion_sin_evidencia: <la afirmación, citada>`: sostiene una afirmación central (sobre la
  demanda, la disposición a pagar, el tamaño del mercado, la ausencia de competidores, los precios o
  la regulación) sin una ficha que la respalde y sin declararla en supuestos.

Cualquier otro motivo no cuenta como fatal. Además, Python marca como fatal, sin importar lo que
diga el juez, una idea revisada que rompe el filtro duro: costo sobre el tope, ítems de costo que no
suman el total, citas a fichas que no existen, menos evidencia que el mínimo, sin evidencia local, o
solo evidencia bloqueada. Un precio estimado sin fuente no es fatal: se pesa en viabilidad.

Una idea con fallo fatal no le puede ganar a una sin él, digan lo que digan los totales. Si las dos
tienen fallo fatal, deciden los totales.

## Empates

No hay empates. Con el mismo total exacto gana la idea con menos ataques en pie; si siguen iguales,
la de mayor puntaje en demanda; después, la de mayor viabilidad; después, la que el juez elija, con
el motivo.

## Lo que el juez no premia

- **La extensión.** Más largo no es mejor.
- **La confianza.** Que la defensa diga "arreglado" no prueba nada: mirá la idea revisada.
- **La tecnología de moda.** IA, agentes o blockchain no suman por sí mismos; suman si resuelven el
  problema de las fichas mejor que algo más simple.
- **El método.** El juez no sabe con qué estrategia se generó la idea ni quién la generó, y no lo
  adivina. El orden X e Y no significa nada.
- **Los adjetivos.** "Una solución innovadora y escalable" no suma nada. La idea tiene que serlo.
