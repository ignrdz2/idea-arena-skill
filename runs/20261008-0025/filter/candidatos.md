# Candidatos para deduplicar

## i001: Copiloto de obligaciones fiscales para unipersonales que empiezan

- Usuario: Unipersonales y monotributistas que recién empiezan o facturan poco, sobre todo servicios. Pagan ellos; contadores asociados pueden pagar por recibir clientes ordenados.
- Problema: Un negocio nuevo en Uruguay debe facturar electrónicamente desde el primer día (F-legal-contable-002) y, si factura como contribuyente de IVA, necesita certificado digital y un CAE que vence a los 2 años (F-comercio-retail-009). El costo de entender esto lo paga en honorarios: un contador cobra $U 2.200 a 3.000 por mes a un monotributista (F-legal-contable-001), y elegir mal el proveedor de CFE trae rechazos, caídas y un plan por comprobante m...
- Solución: App web para autónomos, al estilo de las apps españolas de gestión para autónomos, adaptada al régimen uruguayo. Un asistente pregunta actividad, ingresos y clientes, y arma un calendario personalizado de obligaciones DGI y BPS con alertas; controla vencimiento del CAE y del certificado; importa los CFE emitidos y recibidos en XML para llevar ingresos y gastos; avisa cuando conviene revisar el régimen o el plan del proveedor de CFE según volum...

## i002: Seguimiento de pacientes tras un intento de autoeliminación para equipos de salud mental

- Usuario: Equipos de salud mental de prestadores chicos, policlínicas del interior y organizaciones que hoy siguen casos con planillas. Paga la institución; lo usan psicólogos, psiquiatras y referentes de seguimiento.
- Problema: En 2025 el MSP registró 668 suicidios y 6.140 intentos de 5.144 personas: casi mil intentos fueron de personas que ya habían intentado ese mismo año (F-salud-009). La continuidad entre instituciones es limitada: la historia clínica interoperable cubre 14 de 43 prestadores integrales y deja fuera a más de 100 organizaciones potenciales (F-salud-004), y el MSP reconoce falta de sistemas de información para seguir plazos asistenciales (F-salud-00...
- Solución: Una herramienta de gestión de casos: al ingresar un paciente tras un intento se crea un plan de contactos con fechas (por ejemplo, a los 7, 30 y 90 días), el sistema asigna responsable, avisa al equipo cuando un contacto vence sin registrarse y manda al paciente, con su consentimiento, un recordatorio de consulta por WhatsApp. Permite derivar el caso a otra institución con un resumen exportable. No calcula riesgo ni diagnostica: organiza el se...

## i003: Inteligencia de demanda por mercado de origen para posadas y cabañas del interior

- Usuario: Dueños de posadas, hostels y complejos de cabañas de 5 a 30 unidades en Rocha, Maldonado y Colonia, sin área comercial. Paga el alojamiento; también podría pagar una liga o asociación de turismo departamental para sus socios.
- Problema: El turismo uruguayo depende de pocos mercados y del tipo de cambio: en el verano 2025 cayeron los brasileños en algunos destinos y los compensaron los argentinos, y en Rocha la ocupación de febrero rondó 50% a 60% (F-turismo-007). La diferencia de precios con Argentina bajó a 47%, el mínimo en cinco años, y Brasil pasó a ser más barato (F-turismo-008). Una posada o un complejo de cabañas del interior se entera de estos cambios tarde, por la pr...
- Solución: Tablero web y resumen semanal por email que cruza los datos abiertos de turismo receptivo por origen y destino con el tipo de cambio y la ocupación propia que carga el alojamiento. Muestra qué mercado está creciendo o cayendo, alerta cuando Uruguay se encarece frente a Argentina o Brasil, permite preguntar en lenguaje natural (por ejemplo: cuántos brasileños vinieron a Rocha el último enero contra el anterior) y propone acciones concretas, com...

## i004: Cumplimiento antilavado para escribanías y estudios contables chicos

- Usuario: Escribanos, contadores y abogados independientes o en estudios de 1 a 10 personas en Uruguay. Paga el titular del estudio.
- Problema: La Ley 20.469 de marzo de 2026 endurece el régimen antilavado para abogados, escribanos y contadores: baja el umbral de efectivo de 1.000.000 UI a 200.000 UI y obliga a actualizar matrices de riesgo y manuales (F-legal-contable-009). Más operaciones quedan alcanzadas y cada profesional debe documentar la debida diligencia de sus clientes. A la vez crecen las estafas y la suplantación de identidad (F-fintech-seguros-004, F-fintech-seguros-006),...
- Solución: Plataforma web de cumplimiento antilavado adaptada al régimen uruguayo, siguiendo el modelo de las herramientas de verificación de clientes para estudios jurídicos del Reino Unido. Hace cuatro cosas: (1) legajo de debida diligencia por cliente con formulario que el cliente completa desde el celular, carga de cédula y declaración de beneficiario final; (2) cruce automático con listas públicas de sanciones; (3) registro de operaciones con alerta...

## i005: Portal de cambios y devoluciones para tiendas online uruguayas

- Usuario: Tienda online pyme de Uruguay (indumentaria, calzado, hogar) que paga la suscripción; su cliente final usa el portal para pedir el cambio.
- Problema: Las pymes de e-commerce uruguayas casi no gestionan devoluciones: solo el 8% lo hace y ninguna mide la eficiencia de su logística (F-comercio-retail-007). El volumen es alto: 96,3 millones de transacciones en 2025 (F-comercio-retail-001) y casi siete de cada diez uruguayos compran online, 93% en comercios nacionales (F-comercio-retail-011). Del lado logístico, el 26% no usa indicadores de entrega (F-logistica-transporte-010) y la última milla...
- Solución: Portal de autoservicio con la marca de la tienda: el cliente ingresa su número de pedido, elige el producto, el motivo y adjunta foto; el sistema aplica las reglas de la tienda (plazos, productos excluidos) y ofrece primero cambio por otro talle o crédito en la tienda antes que reembolso. Un modelo de lenguaje clasifica motivos y fotos. La tienda ve una bandeja con estados, coordina retiro o entrega en local, y obtiene los datos para emitir la...

## i006: Medición de tiempos de espera para prestadores de salud chicos

- Usuario: Dirección técnica y administración de prestadores integrales chicos o del interior y de policlínicas privadas. Paga el prestador; lo usan el administrativo de agenda y la dirección.
- Problema: La Política Nacional de Garantía de Acceso Oportuno fija plazos máximos (24 horas hábiles medicina general, 48 cirugía general, 30 días especialistas) y obliga a los prestadores a medirlos y cumplirlos (F-salud-001). Pero el propio MSP admite que faltan sistemas de información: el cálculo empieza cuando se registra la demanda, sin contar días de agenda cerrada (F-salud-002). Los prestadores con menos recursos, con presión financiera como la do...
- Solución: Un servicio web que registra cada pedido de consulta en el momento en que el usuario lo hace, incluso si no hay agenda abierta, y lo concilia con el turno finalmente dado. Importa los turnos desde una exportación CSV de la agenda existente, calcula el tiempo de espera por especialidad contra el plazo del decreto, alerta los pedidos por vencer y genera el reporte de cumplimiento. La dirección puede consultar en lenguaje natural (por ejemplo, qu...

## i007: Radar de exposición del catálogo frente a compras por franquicia

- Usuario: Dueño o comprador de una tienda minorista de juguetes, indumentaria, calzado u hogar en Uruguay; paga el comercio. Podría pagar también una cámara o asociación del rubro para sus socios.
- Problema: El comercio minorista uruguayo pierde ventas frente a plataformas extranjeras: la Cámara de Comercio estima unos 15 millones de dólares por mes, sobre todo en indumentaria, calzado, juguetes y hogar (F-comercio-retail-003). Los envíos por franquicia pasaron de 304.870 a 957.633 en un semestre (F-comercio-retail-004) y cerraron unas 40 jugueterías en 2025 (F-comercio-retail-005), mientras el volumen vendido se estanca (F-comercio-retail-002). E...
- Solución: El comercio sube su catálogo (planilla o exportación del sistema). El sistema busca productos equivalentes en páginas públicas de plataformas extranjeras con embeddings de texto e imagen, calcula el costo puesto en Uruguay para el consumidor con las reglas de franquicia (tres compras anuales de hasta US$ 200 y 20 kilos, F-comercio-retail-004), el tipo de cambio y el plazo de entrega, y clasifica cada SKU: expuesto, defendible o sin equivalente...

## i008: Tutor de práctica para la prueba de matemática de ingreso a Ingeniería

- Usuario: Estudiantes de último año de liceo y recién ingresados a Ingeniería en Uruguay; pagan ellos o sus familias, y en una segunda etapa institutos preparatorios.
- Problema: En la prueba de matemática de Ingeniería del primer semestre solo aprobó el 25% de los inscriptos (F-educacion-002). Quien no la aprueba arranca la carrera con atraso, y el egreso de educación media ya es bajo (F-educacion-001). Las herramientas adaptativas que llegan a la región, como Aleks, son genéricas y no están alineadas a esa prueba (F-educacion-010). Hoy la alternativa son clases particulares.
- Solución: Aplicación web: un banco de ejercicios etiquetados por tema, generado y revisado a partir de material público de la prueba, con diagnóstico inicial, plan de estudio adaptativo según errores y un tutor con RAG que explica paso a paso citando el material de curso en lugar de dar solo el resultado. El docente o el estudiante ve un mapa de temas dominados y pendientes.

## i009: Precontabilización automática de comprobantes y extractos para estudios contables

- Usuario: Asistentes y contadores de estudios contables de 2 a 20 personas que llevan la contabilidad de pymes. Paga el estudio.
- Problema: Los estudios contables de Montevideo contratan asistentes para registrar asientos, conciliar bancos y cuentas de clientes y proveedores, con Excel intermedio (F-legal-contable-005). El estudio cobra honorarios fijos de $U 18.000 a 25.000 por mes por SRL pequeña (F-legal-contable-001): cada hora de carga se come margen. Los comprobantes ya son electrónicos para casi todos los contribuyentes (F-legal-contable-002), pero los dolores siguen: doble...
- Solución: Captura y precontabilización multi-cliente, al estilo de herramientas británicas para estudios, adaptada a Uruguay. El estudio sube o reenvía por correo los XML de CFE recibidos y emitidos, PDFs y extractos bancarios de sus clientes. El sistema extrae RUT, tipo de CFE, montos e IVA; propone la cuenta contable aprendiendo de las imputaciones anteriores de cada cliente (embeddings y reglas); concilia movimientos bancarios contra comprobantes y d...

## i010: Alertas tempranas de ausentismo y desvinculación para liceos privados

- Usuario: Adscriptos y coordinadores de colegios privados (Audec, Aidep) lo usan a diario; paga la dirección del colegio.
- Problema: En Uruguay, de 100 adolescentes que ingresaron al liceo en 2017 solo 43 egresaron en ocho años y casi la mitad faltó al menos el 11% de los días (F-educacion-001). En primer año solo 4 de cada 10 alumnos asisten más del 80% de los días (F-educacion-002), y la promoción en Media Superior cayó 4,3 puntos en 2023 (F-educacion-003). Para un colegio privado cada alumno que se desvincula es además una cuota que se pierde, en un sector con cierres y...
- Solución: Plataforma web que importa asistencia y calificaciones (planilla o registro propio en la app), calcula un puntaje de riesgo por alumno con reglas explicables más un modelo simple entrenado con los datos del propio colegio, y genera una lista semanal priorizada. Para cada alumno en riesgo un asistente con LLM resume el historial (faltas, notas, observaciones) y propone un borrador de mensaje a la familia que el adscripto revisa antes de enviar....

## i011: Consultas en lenguaje natural sobre los datos dispersos de un colegio

- Usuario: Directores y administradores de colegios privados pequeños y medianos; paga el colegio.
- Problema: Los colegios privados uruguayos atraviesan una crisis: más de 300 instituciones, tres cierres a fines de 2023 y el MEC analizando fusiones (F-educacion-004). Para decidir (precios, becas, grupos, personal) la dirección necesita cruzar matrícula, cobranza y asistencia, pero esos datos viven en plataformas que no se hablan: en Colombia cerca de dos tercios de los colegios privados usan plataformas no integradas y el 85% duplica tareas administra...
- Solución: Capa de datos que consolida exportaciones de los sistemas que el colegio ya usa (facturación, gestión académica, planillas) en una base única con un catálogo semántico, y un asistente Text-to-SQL que responde en español preguntas como cuántas familias tienen cuotas atrasadas por nivel o cómo cambió la matrícula por grado. Cada respuesta muestra la consulta, la tabla y un gráfico, y las preguntas útiles se guardan como tablero mensual. No reemp...

## i012: Semáforo de retiro: registro de tratamientos veterinarios y control antes de embarcar a faena

- Usuario: Usa: el productor ganadero o su capataz, y el veterinario que indica los tratamientos. Paga: el productor, por establecimiento; el veterinario puede revenderlo a sus clientes.
- Problema: Si un animal tratado con un medicamento veterinario va a faena antes de cumplir el período de retiro, el residuo aparece en el muestreo del frigorífico y el productor enfrenta un expediente. El MGAP informó 499 expedientes por residuos iniciados en 2025 y 2026, con 52 resoluciones sancionatorias, y el muestreo en frigoríficos subió cerca de 20% desde octubre de 2025 (F-agro-001). Los eventos sanitarios de cada bovino ya se asientan en el SNIG...
- Solución: App móvil que funciona sin señal: al tratar un animal o lote se registra caravana, producto, dosis y fecha, y la app calcula el fin de retiro con el dato que el veterinario toma del prospecto. Al armar un embarque se escanean las caravanas de la tropa y se ve un semáforo por animal: apto, en retiro (con fecha de liberación) o sin datos. Exporta el historial de tratamientos por establecimiento, útil como respaldo ante un expediente y para carga...

## i013: Reportes ciudadanos de contenedores para planificar la recolección y el rediseño de la red

- Usuario: Usan: vecinos que reportan y operadores de limpieza de intendencias o municipios. Paga la intendencia o el municipio.
- Problema: Montevideo tiene 11.800 contenedores públicos y planea bajar a menos de 4.000 hacia fines de 2028, con contenedores de llave digital, para atacar vandalismo, hurgado y acumulación de basura (F-energia-ambiente-004). El 72% de los montevideanos califica mal o muy mal la limpieza y el 62% la recolección, y un caso de contenedores cerrados en Buenos Aires fracasó por vandalismo (F-energia-ambiente-005). Decidir dónde dejar cada contenedor y detec...
- Solución: Cada contenedor lleva un código QR que abre una web sin instalar nada: el vecino reporta con foto si está lleno, roto o con basura afuera. Un modelo de visión clasifica la foto y descarta duplicados. El operador ve un mapa de calor de desbordes y fallas por zona y horario, y un módulo de análisis sugiere qué contenedores consolidar o reubicar al reducir la red, cruzando reportes con densidad de puntos.

## i014: Tours cortos con regreso garantizado para cruceristas, vendidos por guías independientes

- Usuario: Guías turísticos independientes de Montevideo y Colonia (paga el guía) y cruceristas hispanohablantes, lusohablantes y angloparlantes (usuario final, paga el tour).
- Problema: En la temporada 2024-2025 Montevideo recibió 234.865 cruceristas, el 75% del total, y el gasto promedio por persona en tierra fue de solo USD 59,1 (F-turismo-005). El crucerista tiene pocas horas y debe volver al barco a tiempo. Los guías independientes llegan a él sobre todo vía plataformas de free tour donde el viajero paga lo que quiere al final (F-turismo-006): el guía no sabe cuánto va a cobrar ni cuántos van a venir. Ni el guía capta par...
- Solución: Plataforma donde cada guía publica tours cortos de precio fijo cargados sobre las escalas de cruceros de la temporada: el crucerista elige su barco y ve solo los tours que terminan con margen antes de la hora de embarque. Reserva con prepago, recordatorios y punto de encuentro en el puerto. Un asistente traduce la descripción del tour a portugués e inglés y recalcula el itinerario si el barco cambia el horario, avisando al guía y a los inscrip...

## i015: Verificador de estafas por WhatsApp para vendedores online

- Usuario: Emprendedores y pymes que venden por WhatsApp, Instagram o marketplaces en Uruguay. Pagan los que usan el plan de negocio; el uso básico personal es gratuito.
- Problema: Las denuncias por estafa en Uruguay pasaron de 1.872 en 2015 a 25.116 en 2024, tercer delito más denunciado (F-fintech-seguros-004). El BCU identifica como tipos comunes el phishing y smishing, la suplantación de identidad, las estafas de Marketplace y las falsas ofertas de crédito (F-fintech-seguros-006). El comercio online local superó 96 millones de transacciones en 2025 (F-comercio-retail-001). Quien vende por redes recibe a diario mensaje...
- Solución: Un número de WhatsApp al que el vendedor reenvía un mensaje sospechoso, un link o la captura de un comprobante de transferencia. El sistema analiza el texto y la imagen con un modelo de lenguaje con visión, revisa el dominio del link (antigüedad, parecido con marcas bancarias) y lo contrasta con una base de patrones armada sobre la tipología del BCU. Responde en segundos con un nivel de riesgo, el tipo de estafa probable y qué verificar antes...

## i016: Libreta de stock bovino conciliada con la trazabilidad obligatoria

- Usuario: Usa: el productor ganadero chico o mediano, su capataz y el contador o escritorio rural que lo asiste. Paga: el productor, o el escritorio rural que lo ofrece a varios clientes.
- Problema: Todo productor bovino debe asentar en el SNIG los movimientos, cambios de propiedad y eventos sanitarios de cada animal, sobre la base de DICOSE y la Ley 17.997 (F-agro-002). Mantener el stock por caravana, potrero y categoría coincidiendo con lo declarado es trabajo administrativo del productor o su escritorio. En otros rubros del agro, el papeleo de traslados ya se percibe como un costo que paga el productor (F-logistica-transporte-003), y l...
- Solución: App offline para registrar en el campo nacimientos, caravaneos, muertes, ventas, compras y pases entre potreros, por caravana o por lote. Mantiene el stock por categoría y potrero y lo concilia contra el listado que el productor exporta del registro oficial: marca caravanas que faltan, sobran o cambiaron de categoría y arma pendientes a regularizar antes de un embarque. Panel web para el escritorio rural con el estado de cada cliente.

## i017: Reclamos vecinales por WhatsApp para municipios chicos, sin implantación

- Usuario: Usan: vecinos (reportan por WhatsApp) y funcionarios municipales (gestionan en un tablero web). Paga: el municipio o la intendencia.
- Problema: El gobierno digital departamental en Uruguay es muy desigual (F-sector-publico-001). Las soluciones existentes son proyectos grandes: un sistema común para 14 intendencias costó USD 4,5 millones (F-sector-publico-005) y una plataforma municipal de la región tardó cerca de seis meses en implantarse (F-sector-publico-007). Muchos gobiernos ven la tecnología como gasto (F-sector-publico-008) y solo el 34% de los encuestados completó un trámite en...
- Solución: Un canal de reclamos que se activa en un día: el vecino escribe al WhatsApp del municipio, un asistente con LLM pide lo mínimo (tipo, ubicación, foto), lo clasifica y lo asigna a una cuadrilla. El funcionario ve una bandeja web con mapa, estados y plazos; el vecino recibe el cierre por el mismo chat. Sin instalación ni migración, con catálogo configurable desde una planilla y reporte mensual de tiempos de respuesta.

## i018: Stock único que se descuenta leyendo los CFE que la pyme ya emite

- Usuario: Dueño o encargado de una pyme uruguaya que vende en local y online y ya factura con un proveedor de CFE. Paga el mismo comercio.
- Problema: El 92% de las pymes uruguayas de e-commerce no gestiona inventario con un sistema y solo el 31% usa código de barras (F-comercio-retail-006); les cuesta controlar stock y compras (F-comercio-retail-007). Con la factura electrónica obligatoria (F-legal-contable-002), cargan cada venta dos veces: en el software de CFE y en la planilla (F-comercio-retail-009, F-legal-contable-003). Resultado: vender lo que no hay y horas de carga manual, en un ca...
- Solución: PWA que mantiene un stock único. No emite comprobantes: lee los CFE que la pyme ya emite (XML exportado o reenviado por correo) y descuenta stock; un modelo de lenguaje empareja las descripciones de cada línea con los SKU y pide confirmación solo si duda. El celular lee códigos de barras para recepción y conteos. Alerta quiebres y sugiere reposición. Se monta encima del proveedor de CFE, no compite con él.

## i019: Consultas en lenguaje natural sobre los datos de gestión de un organismo

- Usuario: Usa: el funcionario o jefe de área que necesita una cifra (por ejemplo, expedientes atrasados por oficina). Paga: el organismo o la intendencia, desde su área de TI o de gestión.
- Problema: En Uruguay no existe un marco de competencias digitales para funcionarios, los relevamientos muestran capacidades analíticas limitadas y se pide formación en análisis de datos y Excel (F-sector-publico-004). El volumen de trabajo es alto: Presidencia, el Ministerio del Interior y el Tribunal de Cuentas gestionan más de 500 expedientes diarios cada uno (F-sector-publico-003). La respuesta hoy es capacitar: INEFOP formó a más de 25.000 personas...
- Solución: El funcionario sube las planillas o exportaciones que ya maneja (expedientes, reclamos, compras) o conecta datos abiertos, y pregunta en español. El sistema genera SQL, muestra la consulta explicada en palabras, la tabla y un gráfico, y guarda las preguntas frecuentes como indicadores. Cada respuesta es auditable y los datos personales se detectan y enmascaran antes de enviar nada al LLM, que solo ve el esquema y muestras anonimizadas.

## i020: Ruteo y prueba de entrega para pymes de e-commerce y mensajerias chicas

- Usuario: Pymes de e-commerce con reparto propio y mensajerias chicas que reparten para varias tiendas; paga la empresa. El repartidor usa la app movil y el cliente final recibe el aviso.
- Problema: En Montevideo, 32,5% de las empresas de e-commerce entrevistadas no tiene sistema de ruteo, 26% no usa indicadores para monitorear la entrega y 88% de los proveedores logisticos sufrio problemas de seguridad en entregas (F-logistica-transporte-010). Ninguna pyme consultada por UTEC mide la eficiencia de su logistica (F-comercio-retail-007). Mientras tanto el e-commerce crece (F-comercio-retail-001) y la ultima milla, sobre todo fuera de Montev...
- Solución: La pyme sube los pedidos del dia (CSV o planilla) y el sistema geocodifica direcciones, arma rutas optimizadas por vehiculo respetando ventanas horarias, y las envia a la app del repartidor. La prueba de entrega guarda foto, firma y ubicacion, y marca entregas fuera de zona o anomalas como alerta de seguridad. El panel muestra indicadores: entregas a tiempo, costo por entrega y kilometros, y permite preguntar en lenguaje natural sobre esos datos.

## i021: Prediagnóstico energético de mipymes a partir de sus facturas de UTE

- Usuario: Dueño o administrador de una mipyme (comercio, taller, pequeña industria). Pagan la mipyme (plan mensual) y, como segundo cliente, consultores e instaladores de eficiencia o solar que compran prediagnósticos calificados.
- Problema: Las mipymes son el 80% de las empresas de Uruguay y más del 60% del empleo, y el MIEM las empuja a mejorar su eficiencia energética: reintegra hasta USD 3.000 (75% del costo) de un estudio de oportunidades de mejora, lo que implica estudios de hasta unos USD 4.000, y ofrece un simulador de autodiagnóstico genérico (F-energia-ambiente-001). Para un comercio chico, pagar un estudio sin saber si vale la pena es una barrera. La microgeneración est...
- Solución: Web donde la mipyme sube 12 facturas de UTE en PDF o foto. Un extractor con LLM y validación por reglas arma la serie de consumo, potencia y cargos. Un motor de reglas basado en el pliego tarifario público estima ahorros por ajustar la potencia contratada o cambiar de tarifa, y un simulador estima la viabilidad de microgeneración solar. Entrega un informe de prediagnóstico en lenguaje claro que indica si vale la pena pedir el estudio subsidiado.

## i022: Agenda por WhatsApp con lista de espera para consultorios independientes del interior

- Usuario: Profesionales de salud que atienden solos o en consultorios de 1 a 3 personas en ciudades del interior (odontólogos, psicólogos, fisioterapeutas, nutricionistas). Usa y paga el profesional; el paciente solo interactúa por WhatsApp.
- Problema: Los profesionales de salud independientes siguen mayormente con agenda de papel: la fundadora de una agenda local detectó que 18 de cada 20 la usaban, y esa oferta se concentra en Montevideo y el este (F-salud-006). El ausentismo puede costar hasta 14% de los ingresos mensuales de un consultorio privado, y recordatorios con lista de espera lo bajan 30% a 50% según un proveedor extranjero (F-salud-008).
- Solución: Un asistente de WhatsApp que el profesional configura en 15 minutos: los pacientes piden, confirman o cambian turno escribiendo en lenguaje natural; el sistema manda recordatorio 24 horas antes y, si alguien cancela, ofrece el hueco automáticamente a la lista de espera en orden. Panel web con agenda, ausentismo y huecos recuperados. Sin historia clínica.

## i023: Carpeta crediticia portable para pymes a partir de su factura electrónica

- Usuario: Pymes y unipersonales uruguayas que facturan electrónicamente y buscan crédito o mejores condiciones. Paga la pyme por cada carpeta; en una segunda etapa pagan los financiadores por recibir carpetas estandarizadas.
- Problema: PedidosYa Créditos prestó más de US$ 6,4 millones a más de 1.000 pymes uruguayas desde mediados de 2025, evaluándolas con las ventas que pasan por su propia app (F-fintech-seguros-005): las pymes toman crédito cuando alguien las evalúa con sus ventas reales, pero ese dato queda encerrado en una plataforma. Casi todo contribuyente uruguayo ya emite factura electrónica (F-legal-contable-002), así que la pyme tiene su historial de ventas en CFE,...
- Solución: La pyme sube sus CFE en XML o el export de su proveedor de facturación. El sistema los normaliza y genera una carpeta: ventas mensuales, estacionalidad, concentración de clientes, ticket promedio y tendencia, con un resumen en lenguaje claro generado por IA que cita cada dato. La carpeta es de la pyme: la comparte con un link con vencimiento y consentimiento registrado. No presta ni da un puntaje oficial: entrega información verificable para q...

## i024: Gestión y prorrateo de cargadores de autos eléctricos compartidos en edificios

- Usuario: Usan: copropietarios con auto eléctrico y el administrador del edificio. Paga el edificio (gastos comunes) o la administradora que gestiona varios edificios.
- Problema: En 2025 se vendieron 14.387 autos eléctricos en Uruguay (+147%, unos 39 por día) y la ACAU advierte que la cobertura de carga se queda corta; además, el precio de carga de UTE subió cerca de 9,2% en dos meses (F-energia-ambiente-003). La electrificación del transporte es parte de la política energética (F-energia-ambiente-006). Quien vive en un edificio necesita cargar en el garaje común, pero un cargador compartido obliga al administrador a r...
- Solución: Plataforma que se conecta por OCPP a cargadores comerciales compatibles. Cada usuario se identifica con app o tarjeta RFID, reserva turnos, el sistema mide kWh por sesión y genera la liquidación mensual por unidad lista para sumar a los gastos comunes. Sugiere cargar en horas de menor precio según la tarifa que cargue el administrador y avisa cuando la demanda supera la capacidad del cargador.

## i025: Registro y reporte de incidentes de ciberseguridad en 24 horas para entidades chicas

- Usuario: Usa: el responsable de TI o de seguridad (a menudo una sola persona) de una intendencia, un organismo chico o una entidad privada de sector crítico. Paga: la entidad.
- Problema: CERTuy registró 14.264 incidentes en 2024, 42.768 en 2025 y 32.399 solo en el primer semestre de 2026, y el Decreto 66/025 obliga a las entidades de sectores críticos a reportar incidentes en 24 horas (F-sector-publico-006). Las organizaciones con pocas capacidades digitales lo sufren más: en el Estado no hay un marco de competencias digitales y las capacidades analíticas son limitadas (F-sector-publico-004), y la madurez digital de las intend...
- Solución: Una herramienta mínima de cumplimiento: el responsable describe el incidente en lenguaje natural o por formulario guiado; un LLM propone tipo y severidad, pide los datos que faltan y arranca un reloj de 24 horas con avisos. Genera el borrador del reporte, guarda una bitácora con evidencias y línea de tiempo, y sugiere pasos de contención básicos desde guías cargadas por la entidad. No es un SOC: no monitorea redes, ordena y documenta la respue...

## i026: Asistente de papeleo por viaje para fleteros con uno a tres camiones

- Usuario: El dueno de una empresa de uno a tres camiones, que paga y suele manejar; su contador recibe los datos exportados.
- Problema: Entre 80 y 90% del transporte profesional son empresas de uno a tres camiones (F-logistica-transporte-009). Desde 2026 transportistas y arroceros reclaman que la Guia Electronica de Carga suma carga administrativa que encarece el flete (F-logistica-transporte-003), y ademas casi todo emisor debe facturar electronicamente (F-legal-contable-002), con doble carga de datos como dolor tipico (F-legal-contable-003). Las empresas logisticas chicas ti...
- Solución: El fletero carga cada viaje una sola vez: foto del remito o un audio. Un modelo de lenguaje con vision extrae origen, destino, carga, cliente y precio, y el usuario confirma. Con ese registro unico la app prepara los datos listos para copiar en la Guia Electronica de Carga y para el comprobante electronico, registra gasoil y peajes, y calcula el margen por viaje. Se puede preguntar en lenguaje natural, por ejemplo cuanto gane con un cliente en...

## i027: Cartera digital para corredores de seguros chicos

- Usuario: Corredores y productores asesores independientes o con oficinas de 1 a 5 personas en Uruguay. Ellos usan y pagan; sus clientes reciben avisos y resúmenes.
- Problema: En Uruguay operan 16 aseguradoras y la distribución depende de corredores y productores asesores, con competencia fuerte y canales directos como bots de WhatsApp de las aseguradoras (F-fintech-seguros-008). El mercado emitió US$ 2.889 millones en primas en 2024 con ratio combinado de 106,2% (F-fintech-seguros-003): las aseguradoras pierden en lo técnico y empujan canales digitales propios, como la contratación inmediata de MetLife con Klimber...
- Solución: Aplicación web donde el corredor sube pólizas en PDF de cualquier aseguradora. Un modelo de lenguaje extrae asegurado, compañía, ramo, coberturas, prima y vencimiento a una ficha que el corredor valida. Un tablero muestra vencimientos de los próximos 60 días y clientes sin contacto reciente. Envía avisos de renovación por email y responde por WhatsApp las consultas que inicia el cliente sobre su propia póliza, derivando al corredor lo que no s...

## i028: Prediccion de espera para retirar contenedores en el puerto de Montevideo

- Usuario: Lo usan transportistas y despachantes que retiran contenedores; paga la empresa de transporte. La mayoria son empresas de uno a tres camiones (F-logistica-transporte-009), por lo que se apunta a un precio bajo y a acuerdos con la gremial.
- Problema: Retirar un contenedor del puerto de Montevideo puede demorar hasta 9 horas cuando deberia tomar 1,5 a 2 (F-logistica-transporte-001). Las esperas se agravan con atrasos de buques, como los mas de 150 camiones varados diez dias con perdidas estimadas de US$ 750.000 (F-logistica-transporte-002), con paros que dejaron casi 500 camiones esperando (F-logistica-transporte-004) y con caidas de sistemas de la terminal (F-logistica-transporte-005). El...
- Solución: Una app web instalable (PWA) donde el chofer marca llegada, ingreso y salida de cada terminal; el registro se completa solo por geocerca cuando da permiso de ubicacion. Con esos tiempos, mas datos publicos de arribos de buques y avisos de paro cargados por el equipo, un modelo estima la espera por terminal y franja horaria y avisa cuando la fila se dispara. Un panel muestra a la empresa la espera historica por terminal y las horas de camion pe...

## i029: Registro y reporte de huéspedes para anfitriones particulares de vivienda turística

- Usuario: Propietarios particulares con 1 a 5 viviendas de alquiler turístico en balnearios de Maldonado y Rocha, y pequeñas inmobiliarias que administran viviendas de terceros. Paga el propietario o la inmobiliaria.
- Problema: La regulación de vivienda turística obliga a registrar cada vivienda, mostrar un número único en cada oferta, y las plataformas solo podrán publicar alojamientos registrados, con 180 días para adecuarse (F-turismo-001). Además, el texto aprobado en el Senado exige informar al Ministerio del Interior la identidad de cada huésped y reportar anualmente turistas y días de alojamiento (F-turismo-002). Lo sufre el particular que alquila pocas vivien...
- Solución: Aplicación web en español y portugués que guía la inscripción y guarda el número de registro de cada vivienda; genera un enlace de check-in que el huésped completa desde el celular antes de llegar; guarda esos datos cifrados y con plazo de borrado; arma el reporte de huéspedes y el resumen anual listos para cargar; y revisa los anuncios para avisar si falta el número de registro.
