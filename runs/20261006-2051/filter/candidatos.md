# Candidatos para deduplicar

## i001: Portal de cambios y devoluciones con pago por uso para pymes online

- Usuario: Paga la pyme que vende online (indumentaria, calzado, accesorios) por tienda, plataforma o redes. Lo usan el dueño (panel) y el comprador (portal, sin cuenta).
- Problema: 56% de los compradores online uruguayos cita la dificultad para devolver como barrera, y 62% investiga en redes pero solo un tercio compra (F-comercio-retail-002). Según un estudio de UTEC, solo 8% de las pymes gestiona devoluciones y ninguna mide sus procesos (F-comercio-retail-003). Con un ticket medio de unos USD 33 (F-comercio-retail-005), cada compra frenada por ese miedo, y cada devolución que termina en reembolso y no en cambio, es una...
- Solución: Un portal de devoluciones independiente del canal de venta, enlazable desde la tienda, Instagram o WhatsApp. La pyme configura su política (plazos, exclusiones, envío) y la publica antes de la venta. El comprador carga pedido, motivo y fotos, y elige cambio o reembolso; el sistema ofrece primero el cambio. Reglas configurables aprueban lo que cumple la política. Un clasificador agrupa los motivos (talle, defecto, no coincide con la foto, arrep...

## i002: Libreta ganadera por voz y sin señal para productores chicos, con pendientes del SNIG

- Usuario: Productor ganadero pastoril chico de Uruguay y su personal de campo. Paga el productor; segundo canal: veterinarios con varios clientes.
- Problema: Todo productor ganadero debe notificar al SNIG movimientos, cambios de propiedad y eventos productivos y sanitarios de cada bovino (más de 12 millones identificados): una carga administrativa recurrente (F-agro-002), mientras el MGAP digitaliza las guías de tránsito (F-agro-004). Ninguna opción de las fichas encaja con el ganadero pastoril chico: Albor cuesta desde USD 115 por mes (F-agro-007), miTambo es barata y sin internet pero solo para t...
- Solución: PWA que funciona sin señal. El peón dicta un audio (vacunamos 38 terneros del potrero 4) o usa un formulario corto. Al reconectar, el audio se transcribe y un LLM lo convierte en eventos (nacimiento, vacunación, muerte, movimiento, venta), resuelve caravanas y lotes contra el inventario y pide confirmación si duda. Mantiene el stock por lote y lista los pendientes del SNIG con los datos listos para declarar por el canal oficial.

## i003: Facturas de proveedores al stock sin tipeo para comercios chicos

- Usuario: Comercio minorista con cientos de artículos y varios proveedores (ferretería, bazar, librería), con o sin tienda online; el dueño usa y paga.
- Problema: Los comercios chicos uruguayos trabajan con stock desactualizado, venden productos agotados y cargan dos veces los datos cuando facturación e inventario están separados (F-comercio-retail-006). Muchas pymes carecen de herramientas digitales completas (F-comercio-retail-004) y la venta online crece 35% interanual (F-comercio-retail-005): el error se publica y se vende. Suponemos que buena parte es tipear facturas de proveedores con descripcione...
- Solución: El comercio fotografía o sube la factura o remito. Si es el XML del comprobante electrónico se lee directo; si no, un modelo con visión extrae producto, cantidad y costo. Cada línea se empareja con el catálogo por códigos, embeddings en Qdrant y, si hay duda, validación del modelo. El encargado confirma lo incierto y cada corrección queda como sinónimo del proveedor. Luego envía el ajuste de stock a Tiendanube o en CSV y avisa de márgenes que...

## i004: Proyección de caja para pymes con cheques diferidos y facturas electrónicas

- Usuario: Usa: el dueño o administrativo de una pyme que vende a plazo, y su contador. Paga: la pyme o el estudio contable.
- Problema: Las pymes uruguayas necesitan liquidez antes de cobrar: MiFinanzas declara más de 100.000 operaciones adelantando cheques diferidos y facturas (F-fintech-seguros-007) y PedidosYa Créditos prestó US$6,4 millones a más de 1.000 pymes desde 2025 (F-fintech-seguros-008). Separar sistemas genera cargas duplicadas y datos desactualizados (F-comercio-retail-006, sobre facturación e inventario); con facturas, cheques y bancos dispersos, el dueño ve el...
- Solución: Web que arma la caja futura con datos que la pyme ya tiene: CFE emitidos y recibidos en XML, extractos bancarios CSV o PDF y cheques diferidos cargados por foto (visión extrae fecha, monto y banco). Proyecta 13 semanas en pesos y dólares, aprende el atraso de cada cliente, simula escenarios y avisa por correo semanas antes de un faltante. Compara el costo de cubrirlo con las opciones que cargue la pyme, sin intermediar ni prestar. Responde pre...

## i005: Stock al día a partir de los comprobantes electrónicos que el comercio ya tiene

- Usuario: Paga y usa el dueño de un comercio chico que compra a varios proveedores, factura con cualquier sistema y vende en local y online.
- Problema: Los comercios chicos trabajan con stock desactualizado, venden productos agotados y cargan dos veces los datos porque facturación e inventario van por separado; así lo describe YoFacturo, que vende la integración de ambos (F-comercio-retail-006). Muchas pymes carecen de herramientas digitales completas (F-comercio-retail-004) y las mipymes son 97% de las empresas (F-comercio-retail-010). Con el e-commerce creciendo 32% en 2025 (F-comercio-reta...
- Solución: Arma y mantiene el stock sin cambiar de facturador ni cargar productos a mano. El comercio sube los comprobantes de compra y la exportación de ventas de su facturador (XML o CSV); de PDF o fotos, un modelo de visión extrae las líneas. Cada línea ('REM ALG NEG T-M X12') se asocia a un producto con embeddings en Qdrant y reglas por proveedor; lo dudoso se confirma con un clic y queda como regla. Un libro de movimientos calcula existencias, marca...

## i006: Chequeo de zonas sensibles y reporte de cobertura para aplicadores con drones

- Usuario: Contratistas y productores que aplican con 1 a 3 drones. Paga el operador; su cliente recibe el reporte gratis.
- Problema: Los drones aplicadores crecen en Uruguay: 30 vendidos en 2022 y 30 solo en el primer trimestre de 2023, a USD 35.000 a 45.000 cada uno, con datos de vuelo y aplicación por gestionar (F-agro-008). El Estado vigila dónde se aplica: el sistema GMA se probó sobre 100.000 hectáreas en Soriano para alertar conflictos con centros urbanos, poblaciones rurales y escuelas (F-agro-005). El operador chico carga ese riesgo y debe demostrar a su cliente qué...
- Solución: Web y PWA para el operador. Antes de volar: importa el lote y PostGIS chequea la distancia a escuelas y centros poblados de capas abiertas, con zonas de exclusión configurables. Después: importa el registro de vuelo, reconstruye las franjas aplicadas y calcula hectáreas cubiertas, solapes, faltantes e invasiones de zonas sensibles. Un LLM con visión lee la etiqueta y precarga producto y dosis. Sale un reporte PDF por aplicación e historial por...

## i007: Alerta temprana de sitios clonados para entidades financieras uruguayas

- Usuario: Áreas de seguridad o fraude de entidades financieras medianas de Uruguay (cooperativas, financieras, fintech, aseguradoras). Paga la entidad.
- Problema: Las denuncias por estafa en Uruguay pasaron de 1.872 en 2015 a 25.116 en 2024; el phishing es la técnica digital más frecuente y la prevención depende más de cada persona que de la policía (F-fintech-seguros-001). Los delincuentes clonan sitios bancarios con IA en segundos y las transferencias instantáneas eliminan la ventana de recupero (F-fintech-seguros-002, F-fintech-seguros-003): si el clon no se detecta antes de circular, la pérdida es c...
- Solución: Vigila los logs públicos de Certificate Transparency y variantes del dominio de cada marca cliente. Un navegador sin interfaz visita cada candidato y guarda captura, HTML y DNS. Un filtro barato lo compara con el sitio oficial (similitud visual y de estructura, formularios de clave); solo los dudosos pasan a un modelo de lenguaje que clasifica y explica. Ante un clon, alerta por correo y arma la evidencia para pedir la baja. Los clientes de la...

## i008: Verificador de estafas por WhatsApp para clientes de entidades financieras

- Usuario: Usan: clientes de fintech, insurtech, financieras y cooperativas uruguayas. Paga: la entidad, que ofrece el verificador con su marca.
- Problema: Las denuncias por estafa en Uruguay pasaron de 1.872 en 2015 a 25.116 en 2024; el phishing es la técnica digital más frecuente y la prevención depende sobre todo de cada persona (F-fintech-seguros-001). Con IA se clonan sitios bancarios en segundos y las transferencias instantáneas eliminan la ventana de recupero (F-fintech-seguros-002, F-fintech-seguros-003). Quien duda no tiene a quién consultar antes de transferir, y la entidad imitada no v...
- Solución: Un número de WhatsApp al que se reenvía el mensaje, link o captura. Se extraen URLs y teléfonos (visión en capturas) y cada dominio se contrasta con una lista blanca de dominios oficiales uruguayos, su antigüedad (RDAP) y sus certificados recientes (Certificate Transparency). Un LLM con RAG sobre casos públicos de estafas locales responde en segundos, en español rioplatense, con riesgo, razones y qué hacer; nunca afirma que algo es seguro. La...

## i009: Portal de devoluciones con clasificación automática para tiendas online pyme

- Usuario: Paga y usa el panel el dueño de una tienda online pyme uruguaya (Tiendanube, otra plataforma o venta por redes). El comprador usa el portal gratis.
- Problema: En Uruguay, 56% de los compradores online cita la dificultad para devolver productos como barrera de compra (F-comercio-retail-002). Solo 8% de las pymes con e-commerce gestiona devoluciones y ninguna mide la eficiencia de sus procesos; operar así es costoso e impracticable (F-comercio-retail-003). El canal superó los 100.000 millones de pesos en 2025, +32% (F-comercio-retail-001). El costo por tienda no está cuantificado: se medirá en entrevi...
- Solución: Portal con la marca de la tienda donde el comprador indica su pedido, describe el problema y sube fotos. Un modelo de lenguaje con visión clasifica el motivo (talle, defecto, no coincide con la publicación, arrepentimiento), lo contrasta con la política de la tienda y propone cambio, crédito, reembolso o rechazo, justificado. El comercio aprueba con un clic y el comprador recibe un email. Un panel muestra motivos por producto y la tienda publi...

## i010: Comparativos y renovaciones automáticas para corredores de seguros

- Usuario: Corredores y corredurías chicas de seguros de Uruguay (1 a 10 personas). Paga la correduría; sus clientes reciben el comparativo.
- Problema: Aseguradoras y corredores cotizan, renuevan y gestionan siniestros procesando PDFs y correos no estructurados; Foliume levantó US$1 millón para automatizarlo, pero vende en España, Alemania y Portugal (F-fintech-seguros-005). Las pólizas están dispersas y en lenguaje difícil (F-fintech-seguros-004). Uruguay tiene 21 insurtech registradas (F-fintech-seguros-006), pero suponemos que el corredor sigue armando comparativos copiando a mano primas,...
- Solución: El corredor sube cotizaciones y pólizas en PDF. El sistema extrae a un esquema común aseguradora, ramo, vigencia, suma asegurada, prima, deducibles y coberturas, con la página de origen y la confianza de cada dato para revisión humana. Arma un comparativo lado a lado, exportable en PDF con la marca del corredor y las diferencias explicadas en lenguaje simple. Lleva la cartera con alertas de vencimiento y redacta el pedido de recotización.
