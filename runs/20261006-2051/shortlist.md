# Shortlist de ideas de tesis

Run `20261006-2051`, modo piloto, semilla 7, creado 2026-10-06T20:51:02. Generado por /idea-arena.

Cómo leer esto:
- El puesto 1 ganó todos sus cruces y el 2 perdió solo la final. Más abajo, el orden de una eliminación simple es ruidoso: dos ideas eliminadas en la misma ronda se ordenan por el puntaje que sacaron al perder, contra rivales distintos.
- Cada idea es la última versión revisada que tuvo en el torneo.
- Nada de esto reemplaza hablar con el mercado: para eso están las preguntas y el guion de cada idea.
- Una idea que perdió su último cruce con un fallo fatal verificado (viola una restricción dura o se apoya en una afirmación sin evidencia) no se recomienda. Fuera por eso: ninguna.

## Resumen

| # | Idea | Resultado en el torneo | Costo USD/año | Fichas citadas (ok / bloqueadas) |
| --- | --- | --- | --- | --- |
| 1 | Libreta ganadera por voz y sin señal para productores chicos, con datos listos para el SNIG (i002) | campeona | 149 | 9 / 0 |
| 2 | Stock al día a partir de los comprobantes electrónicos que el comercio ya tiene (i005) | eliminada en la ronda 3 por Libreta ganadera por voz y sin señal... | 259.8 | 4 / 0 |
| 3 | Chequeo previo de zonas sensibles y cobertura estimada para aplicadores con drones (i006) | eliminada en la ronda 2 por Stock al día a partir de los comproba... | 159 | 7 / 0 |
| 4 | Portal de devoluciones con clasificación automática para tiendas online pyme (i009) | eliminada en la ronda 2 por Libreta ganadera por voz y sin señal... | 158 | 10 / 1 |
| 5 | Proyección de caja para pymes con cheques diferidos y facturas electrónicas (i004) | eliminada en la ronda 1 por Chequeo previo de zonas sensibles y c... | 159 | 5 / 0 |

## 1. Libreta ganadera por voz y sin señal para productores chicos, con datos listos para el SNIG (i002)

Página completa: [tournament/r3/r3-m01.i002.solution.md](tournament/r3/r3-m01.i002.solution.md). Resultado: campeona.

**Problema.** Todo productor ganadero debe notificar al SNIG eventos de cada bovino (F-agro-002); el MGAP digitaliza guías (F-agro-004) y su app SNIG (F-ataque-r2-m01-i002-competidor-001) cubre trámites puntuales. Hay más de 8.000 unidades familiares con ganadería de carne (F-defensa-r3-m01-i002-001). Costo de registrar y disposición a pagar: supuestos a medir.

**Usuario.** Productor ganadero pastoril chico de Uruguay y su personal de campo; segundo canal: veterinarios.

**Solución.** PWA sin señal. El peón dicta un audio (vacunamos 38 terneros). Al reconectar, se transcribe y un LLM propone eventos que el peón confirma con un toque; si la IA duda, deja el campo vacío. Valor central: captura de campo por voz; subproducto: exporta pendientes del SNIG para cargar a mano. No declara por el productor.

**Costo de infraestructura.** USD 149 por año (tope USD 300).

### Rastro de veredictos

| Ronda | Rival | Persona | Puntaje | Resultado | Motivo del juez |
| --- | --- | --- | --- | --- | --- |
| 1 | Alerta temprana de sitios clonados para entidades financieras uruguayas (i007) | Cliente real de una empresa uruguaya | 64 a 56.5 | ganó | Con demanda igual de débil en ambas (el pagador es un supuesto), X tiene un costo más holgado (USD 164 contra 198), un hueco concreto frente a competidores locales de las fichas (miTambo solo tambos, Cattler feedlots) y un ancla de precio local, mientras Y solo opone marcas locales, español y precio fijo a plataformas globales, sin señal de pago ni tamaño de mercado. |
| 2 | Portal de devoluciones con clasificación automática para tiendas online pyme (i009) | Competidor | 59 a 52 | ganó | Y conserva un hueco real según las fichas (captura por voz y sin señal para el productor pastoril, que no muestran Gecos, la app SNIG ni miTambo), mientras que X queda como un subconjunto de Boris y Undo, gratuitos o freemium y con logística, más un clasificador con IA que la propia idea admite copiable. |
| 3 | Stock al día a partir de los comprobantes electrónicos que el comercio ya tiene (i005) | Tutor académico | 63 a 58.5 | ganó | X es más viable (USD 149 con precios oficiales y voz demostrable en la entrega 1, contra USD 259,8 con poco margen y un alcance cargado) y tiene un business case con mercado inicial respaldado por ficha, mientras Y depende de que los facturadores exporten las ventas, sin plan B para ellas. |

Ataques que quedaron en pie:

- ronda 1: Dolor no demostrado: F-agro-002 prueba la obligación de notificar al SNIG, no cuánto le cuesta al productor chico
- ronda 1: Doble carga: la app exporta los pendientes pero el productor igual tiene que declararlos en el canal oficial
- ronda 1: Diferenciación copiable: miTambo podría extenderse a carne y la voz con LLM se copia, sin explicar por qué no lo hicieron
- ronda 2: Voz más LLM es copiable por Gecos o miTambo; el corpus de audios es una ventaja moderada, no un foso
- ronda 2: La disposición a pagar del productor chico no tiene ficha propia: el único ancla es miTambo, de lechería y de 2020, y el tamaño de mercado no está medido
- ronda 3: Ataque 1 (parcial): el corpus de habla real y la medición de minutos por evento siguen dependiendo de conseguir productores sin contactos declarados; los guiones propios no miden habla espontánea rural
- ronda 3: Ataque 3: las fichas prueban la obligación ante el SNIG y el tamaño del segmento, no el costo de registrar ni la disposición a pagar del productor de carne
- ronda 3: Ataque 4: la diferencia es una capa de voz que Gecos podría tener o sumar rápido; su ausencia solo surge de lo que no dice su página

### Preguntas para validar con el mercado

1. Pensando en la última vez que trabajaron con el rodeo (vacunación, señalada, destete o pesaje): ¿cómo quedó registrado lo que se hizo, quién lo pasó en limpio y cuántas horas llevó en total, desde la manga hasta tener los datos ordenados? En el último año, ¿faltó o estuvo mal algún dato y qué le costó arreglarlo? (a quién: productor ganadero de carne de una unidad familiar del interior de Uruguay (rodeo chico, pastoril) que lleva él mismo los registros; valida: Ataque en pie (rondas 1 y 3): el costo de registrar para el productor chico no está medido. También el supuesto de que los productores chicos registran hoy en papel o WhatsApp.)
2. Hoy, ¿qué paga para llevar los registros del rodeo y cumplir con el SNIG: algún programa, el veterinario, un escritorio rural o un gestor? ¿Cuánto paga por mes o por trámite, quién tomó la decisión de contratarlo y cuándo fue la última vez que empezó, dejó o cambió de pagar algo así, y por qué? (a quién: productor ganadero de carne de una unidad familiar del interior de Uruguay que decide los gastos del establecimiento; valida: Quién decide y paga. Ataque en pie (rondas 2 y 3): la disposición a pagar del productor de carne no tiene ficha propia y el precio de USD 6 a 10 por mes sale de un solo ancla (miTambo, lechería, 2020).)
3. La última vez que tuvo que comunicar al SNIG un evento del rodeo (nacimientos, muertes, movimientos o cambios de caravana): ¿por qué canal lo hizo, quién lo cargó, de dónde sacó los datos y cuántas veces se copió el mismo dato de un papel o planilla a otro lugar antes de quedar declarado? (a quién: productor ganadero de carne o la persona que le hace los trámites del SNIG (familiar, escritorio rural o veterinario); valida: Ataque en pie (ronda 1), doble carga: aunque se exporten los pendientes, el productor igual declara por el canal oficial. Mide cuántas copias manuales del dato hay hoy y si quitar una ahorra trabajo real.)
4. La última vez que trabajaron en la manga o el potrero (vacunación, pesaje, señalada), ¿quién anotaba lo que se iba haciendo y con qué: cuaderno, celular, planilla o de memoria? ¿Había señal de celular en ese lugar? ¿Cuándo y cómo llegó ese dato al productor o al programa que usan, si usan alguno (por ejemplo, Gecos o la app del SNIG)? (a quién: capataz o peón de campo de un establecimiento ganadero de carne chico del interior de Uruguay; valida: Supuestos sin evidencia: la señal en el campo es intermitente y el registro lo hace el personal de campo. Ataques en pie (rondas 2 y 3): si ya usan Gecos u otro programa en el campo, el hueco frente a ellos se achica.)
5. En sus clientes ganaderos chicos, ¿quién registra hoy los tratamientos y vacunaciones que usted indica o aplica, y cómo le llegan esos datos? En el último año, ¿le cobró a algún cliente por ordenar registros o hacer trámites del SNIG, cuánto, y paga usted hoy algún programa para seguir a su cartera de clientes? (a quién: veterinario de libre ejercicio que atiende establecimientos ganaderos de carne chicos en el interior de Uruguay; valida: Supuesto sin evidencia: los veterinarios pagarían por cartera (USD 35 por mes), el canal de pivote si menos de 5 de 10 productores ven valor pagable. También quién decide y paga en ese canal.)

### Guion de entrevista

[shortlist/guiones/i002.md](shortlist/guiones/i002.md)

### Profundizar

`python skills/idea-arena/idea_arena.py deepen i002`

## 2. Stock al día a partir de los comprobantes electrónicos que el comercio ya tiene (i005)

Página completa: [tournament/r3/r3-m01.i005.solution.md](tournament/r3/r3-m01.i005.solution.md). Resultado: eliminada en la ronda 3 por Libreta ganadera por voz y sin señal....

**Problema.** Los comercios chicos tienen stock desactualizado, venden agotados y cargan datos dos veces cuando facturación e inventario van separados; lo describe YoFacturo, que vende la integración (F-comercio-retail-006) y no mide el costo (supuesto). Hay pago por stock dentro del facturador: Fixed lo cobra en su plan más caro, UYU 2.140 por mes contra 980 (F-defensa-r1-m01-i005-001). Pagar por una capa externa no está probado (supuesto).

**Usuario.** Paga y usa el dueño de un comercio chico que compra a varios proveedores, factura con un sistema que no quiere cambiar y vende en local y online.

**Solución.** Arma el stock sin cambiar de facturador ni cargar productos a mano. El comercio sube comprobantes de compra y ventas (XML o CSV) con la frecuencia que elija: semanal por defecto, diaria si vende online; el stock muestra la fecha del último lote y se marca no confiable tras 14 días sin cargas (supuesto). Los PDF o fotos son solo de compras a proveedores, sin datos de consumidores; un modelo de visión extrae las líneas. Cada línea se asocia a un producto con embeddings en Qdrant y reglas por proveedor; lo dudoso se confirma con un clic. Un libro de movimientos calcula existencias, marca faltantes y publica la disponibilidad como CSV descargable y API JSON, sin conectores a plataformas.

**Costo de infraestructura.** USD 259.8 por año (tope USD 300).

### Rastro de veredictos

| Ronda | Rival | Persona | Puntaje | Resultado | Motivo del juez |
| --- | --- | --- | --- | --- | --- |
| 1 | Verificador de estafas por WhatsApp para clientes de entidades financieras (i008) | Cliente real de una empresa uruguaya | 68 a 57.5 | ganó | Y cobra al mismo comercio que sufre el problema, ancla precio y señal de pago en ofertas locales verificadas (el escalón de stock de Fixed, UYU 2.140 contra 980, y gestionUltimate) con un costo de USD 173,4, mientras X prueba bien el dolor del usuario final pero cobra a una entidad cuyo costo, disposición a pagar y alternativas actuales son solo supuestos. |
| 2 | Chequeo previo de zonas sensibles y cobertura estimada para aplicadores con drones (i006) | Competidor | 61 a 52.5 | ganó | X tiene una señal de pago local por control de stock (el escalón de Fixed y tres competidores que lo venden) sobre un universo de comercios mucho mayor, más encaje y un desafío medible de emparejamiento, mientras Y apunta a un parque de decenas de drones que la propia idea admite que no sostiene un negocio y no tiene ninguna señal de pago. |
| 3 | Libreta ganadera por voz y sin señal para productores chicos, con datos listos para el SNIG (i002) | Tutor académico | 58.5 a 63 | perdió | X es más viable (USD 149 con precios oficiales y voz demostrable en la entrega 1, contra USD 259,8 con poco margen y un alcance cargado) y tiene un business case con mercado inicial respaldado por ficha, mientras Y depende de que los facturadores exporten las ventas, sin plan B para ellas. |

Ataques que quedaron en pie:

- ronda 1: Ataque 1 (en parte): el segmento que no quiere migrar de facturador sigue sin medir, y un cliente de Fixed puede sumar stock sin migrar, así que frente a Fixed la diferencia es sobre todo precio
- ronda 1: Ataque 3: subir comprobantes periódicamente es trabajo nuevo para el dueño; la idea lo marca y lo mide en el piloto, pero no lo resuelve
- ronda 2: El hueco depende de comercios que no migran de facturador, un segmento sin medir
- ronda 2: La función es copiable por Fixed, YoFacturo o gestionUltimate; la ventaja del corpus por proveedor es un supuesto
- ronda 2: No hay ficha de demanda para una capa de stock externa: el dolor sale del blog de un competidor y la disposición a pagar es supuesto
- ronda 3: Ataque 1 (parcial): subir comprobantes a diario sigue siendo una rutina manual y la hipótesis de menos de 15 minutos por semana se prueba recién con comercios reales
- ronda 3: Ataque 2 (parcial): el formato CFE es público, pero que los facturadores dejen exportar los comprobantes es supuesto y el plan B de PDF y fotos cubre solo compras, no ventas
- ronda 3: Ataque 3: la demanda del nicho que no migra de facturador no tiene ficha; la señal de pago de Fixed es por stock integrado al facturador, no por una capa externa
- ronda 3: Ataque 4 (parcial): sin contactos, el piloto y la medición contra conteo físico pueden quedar en comprobantes anonimizados y datos sintéticos
- ronda 3: Ataque 7 (parcial): la base legal de la transferencia de PDF y fotos sigue sin verificar y la página no se recortó (992 palabras contra un máximo de 700)

### Preguntas para validar con el mercado

1. ¿Con qué sistema facturan hoy y cómo llevan el control de stock? ¿Alguna vez cambiaron de facturador, evaluaron hacerlo o pasar a un plan más caro del mismo? Contame la última vez: qué miraron, qué decidieron y por qué. (a quién: dueño de un comercio minorista chico de Montevideo que compra a varios proveedores, emite factura electrónica y vende en local y online; valida: Supuesto de que hay comercios que no quieren migrar de facturador y ataques de rondas 1, 2 y 3: ese segmento no está medido y un cliente de Fixed puede sumar stock sin migrar, así que la diferencia sería solo de precio.)
2. Pensá en la última vez que vendieron algo que no tenían, o que el stock del sistema no coincidía con lo que había en el local. ¿Qué pasó, cómo lo resolvieron, cuánto les costó (venta perdida, devolución, horas de recuento) y cuántas veces pasó en los últimos tres meses? (a quién: dueño o encargado de un comercio minorista chico de Montevideo que vende en local y por tienda online o redes sociales; valida: Cuánto cuesta hoy el problema: el costo del faltante es supuesto y el dolor solo sale del blog de YoFacturo (ataque de ronda 2: no hay ficha de demanda propia).)
3. La última vez que juntó las facturas de compra y de venta del mes de un comercio chico cliente, ¿cómo las obtuvo, de qué facturador salían, en qué formato le llegaron (archivo del sistema, planilla, PDF o papel) y qué parte de las ventas no tenía comprobante? (a quién: contador de un estudio que lleva la contabilidad de comercios minoristas chicos en Uruguay; valida: Supuestos de que el comercio puede sacar sus CFE emitidos y recibidos del facturador y de que la mayoría de sus ventas tiene CFE; ataque de ronda 3: exportar es supuesto y el plan B de PDF y fotos no cubre ventas.)
4. En la última semana, ¿quién cargó las compras a proveedores y ajustó el stock, cómo lo hizo (sistema, planilla, cuaderno) y cuántos minutos le llevó en total? ¿Hubo semanas en que no se hizo? ¿Qué pasó en esas semanas? (a quién: persona que carga las compras y lleva el stock en un comercio minorista chico de Montevideo (dueño o empleado administrativo); valida: Ataques de rondas 1 y 3: subir comprobantes es una rutina manual nueva. Da la línea de base de minutos de carga frente a la meta supuesta de menos de 15 minutos por semana y muestra si la carga se abandona.)
5. La última vez que empezaron a pagar o dieron de baja un software para el comercio (facturación, stock, tienda online u otro), ¿quién lo decidió, quién lo paga, cuánto pagan hoy por mes por cada uno y qué los llevó a contratarlo o cancelarlo? (a quién: dueño de un comercio minorista chico de Uruguay que paga su facturador electrónico por suscripción mensual; valida: Quién decide y paga, y los supuestos de precio (USD 12 a 20 por mes) y de disposición a pagar por una capa externa además del facturador; ataque de ronda 3: la señal de pago de Fixed es por stock integrado, no por una capa aparte.)

### Guion de entrevista

[shortlist/guiones/i005.md](shortlist/guiones/i005.md)

### Profundizar

`python skills/idea-arena/idea_arena.py deepen i005`

## 3. Chequeo previo de zonas sensibles y cobertura estimada para aplicadores con drones (i006)

Página completa: [tournament/r2/r2-m02.i006.solution.md](tournament/r2/r2-m02.i006.solution.md). Resultado: eliminada en la ronda 2 por Stock al día a partir de los comproba....

**Problema.** Los drones aplicadores crecen en Uruguay: 30 vendidos en 2022 y 30 solo en el primer trimestre de 2023, a USD 35.000 a 45.000 cada uno, con datos de vuelo y aplicación por gestionar (F-agro-008). Quien aplica con drones debe respetar zonas buffer y registrar cada aplicación en el RAPF, que ya permite consultar, bajar o imprimir los registros (F-defensa-r1-m02-i006-001, F-defensa-r1-m02-i006-003); la aplicación aérea no puede ser a menos de 500 m de un centro educativo (F-defensa-r1-m02-i006-002). Ninguna ficha muestra una herramienta que verifique esas distancias antes de volar; que el operador chico lo hace a ojo es supuesto.

**Usuario.** Contratistas y productores que aplican con 1 a 3 drones. Paga el operador; su cliente recibe el reporte gratis.

**Solución.** Web y PWA para el operador. Antes de volar (núcleo, el RAPF no lo cubre): importa el lote y PostGIS chequea la distancia a escuelas y centros poblados con capas abiertas. Después: importa el registro de vuelo (KML o traza manual), reconstruye franjas con el ancho declarado y estima hectáreas cubiertas, solapes y faltantes, con margen de error medido contra trazas simuladas. Sale un PDF de cobertura estimada para el cliente y un borrador de registro para copiar al RAPF. No reemplaza ni se integra al RAPF ni prueba cumplimiento. Producto y dosis se eligen de una lista.

**Costo de infraestructura.** USD 159 por año (tope USD 300).

### Rastro de veredictos

| Ronda | Rival | Persona | Puntaje | Resultado | Motivo del juez |
| --- | --- | --- | --- | --- | --- |
| 1 | Proyección de caja para pymes con cheques diferidos y facturas electrónicas (i004) | Cliente real de una empresa uruguaya | 61 a 59.5 | ganó | Con demanda pareja (las dos dejan la disposición a pagar como supuesto), X gana por viabilidad y diferenciación: su MVP se demuestra con registros KML reales o simulados sin depender de terceros y su chequeo contra la normativa del MGAP es un hueco concreto, mientras que Y argumenta su hueco por ausencia frente a un software de facturación que ya tiene los CFE y su piloto depende de datos financie |
| 2 | Stock al día a partir de los comprobantes electrónicos que el comercio ya tiene (i005) | Competidor | 52.5 a 61 | perdió | X tiene una señal de pago local por control de stock (el escalón de Fixed y tres competidores que lo venden) sobre un universo de comercios mucho mayor, más encaje y un desafío medible de emparejamiento, mientras Y apunta a un parque de decenas de drones que la propia idea admite que no sostiene un negocio y no tiene ninguna señal de pago. |

Ataques que quedaron en pie:

- ronda 1: Disposición a pagar y costo del dolor sin ficha: que el operador pague USD 250 o pierda algo sin el reporte sigue siendo supuesto
- ronda 1: Mercado diminuto: 60 drones vendidos hasta 2023, el escenario de 40 drones da USD 10.000 por año y crecer exige Argentina o Brasil sin ficha
- ronda 1: Sin contacto con operadores de un nicho chico para validar antes de diciembre de 2026
- ronda 1: Capas abiertas de escuelas y centros poblados sin verificar, y distancia a centros poblados sin relevar
- ronda 1: Diferencial angosto y copiable por los fabricantes
- ronda 2: La disposición a pagar USD 250 por drone no tiene ficha y el chequeo previo se puede hacer con un mapa gratuito
- ronda 2: El hueco se afirma por ausencia de ficha y es copiable por el fabricante o las herramientas de registros de vuelo
- ronda 2: Mercado de decenas de drones: 20 drones dan USD 5.000 por año y la idea admite que no sostiene un negocio

### Preguntas para validar con el mercado

1. Pensá en el último lote nuevo donde aplicaron con drone: ¿cómo averiguaron si había escuelas, centros poblados o cursos de agua cerca y a qué distancia estaban? ¿Qué herramienta o mapa usaron, quién lo hizo y cuánto tiempo les llevó? (a quién: contratista o productor uruguayo que aplica fitosanitarios con 1 a 3 drones propios; valida: Supuesto de que el operador chico verifica hoy las zonas a ojo o con un mapa genérico, y ataque de ronda 2 de que el chequeo previo se hace con un mapa gratuito o que la app del fabricante ya lo cubre.)
2. Contame la última vez que una aplicación con drone les trajo un problema después de hacerla: un reclamo del cliente o de vecinos, una inspección o intimación del MGAP, o tener que volver a aplicar. ¿Qué pasó, cómo lo resolvieron y cuánto les costó en plata, horas de trabajo o clientes perdidos? (a quién: contratista o productor uruguayo que aplica fitosanitarios con 1 a 3 drones propios; valida: Costo actual del problema: ataque de ronda 1 de que el costo del dolor no tiene ficha y supuesto de que se desconoce el costo de una multa. Si nunca pasó o costó poco, no hay dolor que justifique pagar.)
3. ¿Qué software o suscripciones pagan hoy para trabajar con los drones, aparte del equipo? Por la última que contrataron: ¿quién decidió contratarla, quién la paga, cuánto pagan por año y por qué la pagaron en vez de seguir con algo gratis? (a quién: dueño o socio de una empresa contratista que aplica fitosanitarios con drones para terceros en Uruguay; valida: Quién decide y paga, y disposición a pagar: supuesto de que el operador paga USD 250 por año por drone y ataques de ronda 1 y 2 de que esa cifra no tiene ficha y compite con herramientas gratuitas.)
4. La última vez que contrataste una aplicación con drone, ¿qué te entregó el aplicador al terminar para mostrarte qué se aplicó, dónde y en cuántas hectáreas? ¿Lo pediste vos, lo usaste para algo y te pasó alguna vez que lo facturado no coincidiera con lo aplicado? (a quién: productor agrícola uruguayo que contrató a un tercero una aplicación de fitosanitarios con drone en la última zafra; valida: Supuesto de que los clientes del operador valoran un reporte de cobertura (ninguna ficha lo muestra) y de que lo reciben sin pagar: si hoy no piden ni usan nada, el reporte no suma valor a la venta.)
5. En los últimos 12 meses, ¿cuántos drones aplicadores vendieron y de qué marcas? De esos compradores, ¿cuántos son contratistas que aplican para terceros y cuántos productores que aplican en su propio campo, y cuántos drones tiene cada uno? (a quién: vendedor o responsable comercial de un distribuidor de drones agrícolas en Uruguay; valida: Ataque de mercado diminuto (60 drones vendidos hasta el primer trimestre de 2023, sin total acumulado), supuesto de que la marca dominante se desconoce y viabilidad del canal por distribuidores.)

### Guion de entrevista

[shortlist/guiones/i006.md](shortlist/guiones/i006.md)

### Profundizar

`python skills/idea-arena/idea_arena.py deepen i006`

## 4. Portal de devoluciones con clasificación automática para tiendas online pyme (i009)

Página completa: [tournament/r2/r2-m01.i009.solution.md](tournament/r2/r2-m01.i009.solution.md). Resultado: eliminada en la ronda 2 por Libreta ganadera por voz y sin señal....

**Problema.** En Uruguay, 56% de los compradores online cita la dificultad para devolver como barrera de compra (F-comercio-retail-002). Solo 8% de las pymes con e-commerce gestiona devoluciones y ninguna mide su eficiencia (F-comercio-retail-003). El canal superó los 100.000 millones de pesos en 2025, +32% (F-comercio-retail-001). El volumen y costo de devoluciones por tienda no está en las fichas: se mide en entrevistas.

**Usuario.** Paga y usa el panel el dueño de una tienda online pyme uruguaya con 20 o más devoluciones por mes. Foco inicial: tiendas por redes o en plataformas distintas de Tiendanube, adonde no llegan las apps de su tienda (hipótesis a validar). El comprador usa el portal gratis.

**Solución.** Portal con la marca de la tienda donde el comprador indica su pedido, describe el problema y sube fotos. Un modelo de lenguaje con visión clasifica el motivo, lo contrasta con la política de la tienda y propone cambio, crédito, reembolso o rechazo, justificado. El comercio aprueba con un clic. Un panel muestra motivos por producto y la tienda publica su política. Lo que el MVP mide es cuánto ahorra el clasificador: porcentaje de sugerencias aceptadas sin cambios. Datos mínimos: sin dirección ni documento.

**Costo de infraestructura.** USD 158 por año (tope USD 300).

### Rastro de veredictos

| Ronda | Rival | Persona | Puntaje | Resultado | Motivo del juez |
| --- | --- | --- | --- | --- | --- |
| 1 | Comparativos y renovaciones automáticas para corredores de seguros (i010) | Cliente real de una empresa uruguaya | 54 a 51 | ganó | Y apoya el dolor en dos fichas locales verificadas de fuentes distintas (56% de compradores frena por devoluciones y solo 8% de las pymes las gestiona, F-comercio-retail-002 y 003), mientras que en X el dolor del corredor uruguayo es un supuesto sin ninguna ficha y Foliume ya hace el mismo flujo; X compensa en encaje y valor académico, pero no alcanza. |
| 2 | Libreta ganadera por voz y sin señal para productores chicos, con datos listos para el SNIG (i002) | Competidor | 52 a 59 | perdió | Y conserva un hueco real según las fichas (captura por voz y sin señal para el productor pastoril, que no muestran Gecos, la app SNIG ni miTambo), mientras que X queda como un subconjunto de Boris y Undo, gratuitos o freemium y con logística, más un clasificador con IA que la propia idea admite copiable. |

Ataques que quedaron en pie:

- ronda 1: el costo de las devoluciones para la tienda no está probado; el 8% de F-comercio-retail-003 puede indicar poco volumen
- ronda 1: el MVP deja afuera el envío de vuelta y resuelve una decisión administrativa con ahorro posiblemente chico
- ronda 1: no se buscaron herramientas de devoluciones locales o regionales y Tiendanube podría sumar la función
- ronda 2: El único diferencial, la clasificación con IA, es copiable por Boris o Undo y la idea lo admite; el foco en tiendas fuera de Tiendanube es una hipótesis sin ficha
- ronda 2: No hay evidencia de que la tienda pague y los competidores son gratuitos o freemium
- ronda 2: El tamaño del segmento con 20 o más devoluciones por mes es desconocido y el plan B gratuito deja la tesis sin ingresos demostrables
- ronda 2: El envío de vuelta, señalado como desafío en F-comercio-retail-004, queda fuera del MVP mientras los competidores ya lo cubren

### Preguntas para validar con el mercado

1. Pensando en el último mes: ¿cuántos pedidos terminaron en cambio o devolución, cuántas horas le dedicó alguien de la tienda a atenderlos y cuánto se perdió en envíos, reembolsos o mercadería que no se pudo volver a vender? (a quién: Dueño de una tienda online pyme uruguaya que vende por redes sociales o por una plataforma distinta de Tiendanube; valida: Ataque en pie: el costo de las devoluciones para la tienda no está probado y el tamaño del segmento con 20 o más devoluciones por mes es desconocido (el 8% de F-comercio-retail-003 puede indicar poco volumen).)
2. Contame la última devolución o cambio que tuvieron: ¿por qué canal llegó el pedido del cliente, quién lo atendió, qué le pidieron para comprobar el problema, cómo decidieron qué hacer y cuánto tiempo pasó hasta cerrarlo? (a quién: Persona que atiende los reclamos y devoluciones (dueño o encargado de atención al cliente) de una tienda online pyme uruguaya; valida: Supuesto declarado: las devoluciones llegan hoy por WhatsApp o email y se resuelven a mano. También si decidir qué hacer con cada caso consume tiempo real o es un paso trivial.)
3. ¿Qué herramientas, apps o servicios usaron alguna vez para manejar cambios y devoluciones, incluidas las que ofrece su plataforma de venta? ¿Cuál fue la última que probaron y por qué la siguen usando o la dejaron? (a quién: Dueño de una tienda online pyme uruguaya; hacerla tanto a tiendas en Tiendanube como a tiendas en otras plataformas o que venden solo por redes, para comparar; valida: Ataques en pie: no se buscaron herramientas locales o regionales, Boris y Undo ya cubren Tiendanube con planes gratis o freemium, y que las tiendas fuera de Tiendanube no tengan opciones equivalentes es una hipótesis sin ficha.)
4. La última vez que la tienda empezó a pagar un servicio o app mensual para la operación (envíos, cobros, stock o atención), ¿quién lo encontró, quién aprobó el gasto, cuánto pagan por mes y qué tuvo que pasar para que lo contrataran? (a quién: Dueño o socio que maneja los gastos de una tienda online pyme uruguaya con 20 o más devoluciones por mes; valida: Quién decide y paga, y el supuesto sin evidencia de disposición a pagar USD 15 a 35 por mes. Ataque en pie: no hay evidencia de que la tienda pague y los competidores son gratuitos o freemium.)
5. En la última devolución que se complicó o se demoró, ¿en qué paso se trabó: en decidir si correspondía, en coordinar el envío de vuelta con el cliente o el correo, o en devolver la plata? ¿Cuánto tardó en cerrarse, cuánto costó ese envío y quién lo pagó? (a quién: Encargado de logística o despacho de una tienda online pyme uruguaya que envía pedidos al interior del país; valida: Ataque en pie: el MVP deja afuera el envío de vuelta, señalado como desafío en F-comercio-retail-004, y resuelve una decisión administrativa cuyo ahorro puede ser chico frente al costo logístico.)

### Guion de entrevista

[shortlist/guiones/i009.md](shortlist/guiones/i009.md)

### Profundizar

`python skills/idea-arena/idea_arena.py deepen i009`

## 5. Proyección de caja para pymes con cheques diferidos y facturas electrónicas (i004)

Página completa: [tournament/r1/r1-m02.i004.solution.md](tournament/r1/r1-m02.i004.solution.md). Resultado: eliminada en la ronda 1 por Chequeo previo de zonas sensibles y c....

**Problema.** Las pymes uruguayas tienen flujos de caja irregulares que generan necesidad de recursos extra para pagar proveedores, tributos y seguridad social (F-defensa-r1-m02-i004-001, de 2018). Hay oferta y uso de financiación sobre cuentas por cobrar: MiFinanzas declara más de 100.000 operaciones adelantando cheques diferidos y facturas (F-fintech-seguros-007) y PedidosYa Créditos prestó US$6,4 millones a más de 1.000 pymes desde 2025 (F-fintech-seguros-008). Esas fichas prueban uso de crédito, no que la falta de proyección sea su causa: eso es una hipótesis a validar (ver supuestos), a saber, que con facturas, cheques y bancos dispersos el dueño ve el faltante tarde y se financia de urgencia sin comparar costos. Las mipymes son 97% de las empresas (F-comercio-retail-010): solo mide el tamaño del segmento, no la demanda.

**Usuario.** Usa: el dueño o administrativo de una pyme que vende a plazo (con facturas a crédito o cheques diferidos, no una microempresa que cobra al contado), y su contador. Paga: la pyme o el estudio contable.

**Solución.** Web que arma la caja futura con datos que la pyme ya tiene: CFE emitidos y recibidos en XML, extractos bancarios CSV y cheques diferidos cargados por foto (visión extrae fecha, monto y banco, con corrección manual). Proyecta 13 semanas en pesos y dólares, estima el atraso de cada cliente, simula escenarios y avisa por correo semanas antes de un faltante, solo si los datos tienen menos de 7 días; si están viejos, el panel lo marca y no alerta. Compara el costo de cubrir el faltante con las opciones que cargue la pyme, sin intermediar ni prestar. Al LLM solo se envía la imagen del cheque o el texto del extracto, con nombres de contrapartes enmascarados.

**Costo de infraestructura.** USD 159 por año (tope USD 300).

### Rastro de veredictos

| Ronda | Rival | Persona | Puntaje | Resultado | Motivo del juez |
| --- | --- | --- | --- | --- | --- |
| 1 | Chequeo previo de zonas sensibles y cobertura estimada para aplicadores con drones (i006) | Cliente real de una empresa uruguaya | 59.5 a 61 | perdió | Con demanda pareja (las dos dejan la disposición a pagar como supuesto), X gana por viabilidad y diferenciación: su MVP se demuestra con registros KML reales o simulados sin depender de terceros y su chequeo contra la normativa del MGAP es un hueco concreto, mientras que Y argumenta su hueco por ausencia frente a un software de facturación que ya tiene los CFE y su piloto depende de datos financie |

Ataques que quedaron en pie:

- ronda 1: Demanda de proyección sin ficha: las fichas muestran uso de crédito, no que la falta de proyección cause la financiación de urgencia
- ronda 1: Disposición a pagar USD 15 a 30 por mes y canal por contadores sin ninguna señal
- ronda 1: Carga manual recurrente de XML, extractos y cheques: el aviso de datos viejos mitiga pero no resuelve
- ronda 1: Diferenciación argumentada por ausencia: YoFacturo ya tiene los CFE y puede sumar un tablero de caja

### Preguntas para validar con el mercado

1. Pensá en la última vez que tuvieron que adelantar cheques, descontar facturas, pedir un préstamo o usar sobregiro para pagar sueldos, BPS, DGI o proveedores. ¿Cuántos días antes se dieron cuenta de que iba a faltar plata, cómo se enteraron y compararon el costo de más de una opción antes de elegir? (a quién: dueño de una pyme de Montevideo que vende a otras empresas a plazo, con facturas a crédito o cheques diferidos; valida: Ataque en pie de ronda 1 y supuesto declarado: que la falta de proyección cause la financiación de urgencia. Si se enteran con tiempo o ya comparan costos, la causa no es la falta de visibilidad y la idea pierde su base.)
2. En los últimos 12 meses, ¿cuántas veces tuvieron que cubrir un faltante de caja y cuánto les costó en total, sumando intereses, descuento de cheques, comisiones y recargos o multas por pagar tarde a DGI, BPS o proveedores? ¿De dónde sale ese número? (a quién: dueño de una pyme de Montevideo que vende a otras empresas a plazo, con facturas a crédito o cheques diferidos; valida: Cuánto cuesta hoy el problema. Es el techo de la disposición a pagar USD 15 a 30 por mes (ataque en pie de ronda 1): si el costo anual es bajo o nadie lo conoce, ese precio no se sostiene.)
3. La última vez que la empresa empezó a pagar un software o servicio para la administración (facturación, contabilidad, banca, cobranzas), ¿quién lo propuso, quién decidió contratarlo, quién lo paga, cuánto pagan por mes y qué papel tuvo el contador en esa decisión? (a quién: dueño de una pyme de Montevideo que vende a otras empresas a plazo, con facturas a crédito o cheques diferidos; valida: Quién decide y quién paga (la pyme o el estudio contable), con un precio de referencia de lo que ya pagan. Responde el ataque en pie de ronda 1 sobre disposición a pagar USD 15 a 30 por mes y canal por contadores sin ninguna señal.)
4. ¿Dónde llevan hoy los cheques diferidos y las facturas pendientes de cobro y de pago (software de facturación, planilla, cuaderno)? ¿Quién lo actualiza y cada cuánto? Contame la última vez que ese registro estaba atrasado o con errores: cómo se dieron cuenta y qué pasó. (a quién: administrativo o encargado de cobranzas y pagos de una pyme de Montevideo que vende a plazo con cheques diferidos; valida: Ataque en pie de ronda 1 sobre la carga manual recurrente: si hoy nadie mantiene ese registro al día, tampoco va a cargar datos cada semana. También muestra si el software de facturación que usan ya cubre el seguimiento de cobros (ataque de diferenciación frente a YoFacturo).)
5. La última vez que un cliente pyme te consultó porque no le alcanzaba la plata para pagar sueldos, BPS, DGI o a un proveedor, ¿qué hiciste, con qué herramienta o planilla, cuánto tiempo te llevó y se lo cobraste aparte? ¿A cuántos de tus clientes les pasó algo así en el último año? (a quién: contador socio de un estudio contable de Montevideo que lleva la contabilidad de varias pymes que venden a plazo; valida: Ataque en pie de ronda 1 sobre el canal por contadores sin señal: si el contador ya atiende este problema, con qué herramienta y si lo cobra. También estima cuántos clientes por estudio lo sufren, base del plan para estudios (USD 12 por pyme).)

### Guion de entrevista

[shortlist/guiones/i004.md](shortlist/guiones/i004.md)

### Profundizar

`python skills/idea-arena/idea_arena.py deepen i004`

## El embudo

- Fichas: 26 aceptadas (25 ok, 1 bloqueadas), 0 descartadas.
- Ideas: 10 recibidas, 10 pasan el filtro duro, 10 pasan el alcance.
- Torneo: 8 ideas, 3 ronda(s).
- Detalle del filtro: [filter/reporte.md](filter/reporte.md).
