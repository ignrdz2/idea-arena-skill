# Copiloto de licitaciones públicas para PyMEs (preparar y ganar, no solo encontrar)

**Problema.** Venderle al Estado uruguayo obliga a una PyME a monitorear el portal de Compras Estatales, leer pliegos largos y heterogéneos, cumplir requisitos formales (RUPE activo, certificados vigentes, garantías) y decidir en pocos dias si se presenta. El costo de equivocarse es perder la oferta por un requisito formal o cotizar a ciegas. Hay señales publicas de que el proceso es dificil de navegar: en su memoria anual 2021 la ARCE reporta haber atendido cerca de 30.000 consultas, de las cuales unas 21.500 fueron de proveedores ([Memoria anual 2021, ARCE](https://www.gub.uy/agencia-reguladora-compras-estatales/sites/agencia-reguladora-compras-estatales/files/2022-03/Memoria%20anual%202021.pdf)). Dos emprendedores uruguayos describieron el mismo dolor al fundar una plataforma del rubro: no encontraron software que automatizara la postulacion ([El Observador, julio 2026](https://www.elobservador.com.uy/cafe-y-negocios/dos-jovenes-canelones-crearon-una-plataforma-facilitar-el-acceso-pequenas-empresas-las-licitaciones-n6049993)). En Chile, donde el mercado publico mueve unos USD 10.000 millones al ano, solo el 4% de las empresas se adjudica mas del 80% de los montos ([Diario Financiero](https://www.df.cl/df-lab/innovacion-y-startups/licitalab-alista-expansion-a-colombia-y-en-noviembre-lanzara-nuevo)). El universo potencial local: las mipymes son el 99% de las empresas uruguayas ([Presidencia](https://www.gub.uy/presidencia/comunicacion/noticias/99-empresas-uruguayas-son-mipymes)); el subconjunto que vende o puede vender al Estado se mide con el dataset abierto del RUPE ([datos abiertos ARCE](https://www.gub.uy/agencia-reguladora-compras-estatales/datos-y-estadisticas/datos-abiertos)).

**Usuario.** Lo usa la persona que arma las ofertas en una PyME proveedora del Estado (dueno, administrativo o tecnico comercial) y los consultores que preparan licitaciones para terceros. Paga la empresa proveedora, con suscripcion mensual; el consultor paga por volumen de empresas gestionadas.

**Solución.** Plataforma que ingiere los llamados publicados en formato OCDS y los pliegos adjuntos, y entrega cuatro cosas: (1) un radar de oportunidades rankeadas segun el perfil real de la empresa, construido a partir de su historial de adjudicaciones; (2) un lector de pliegos que devuelve un checklist de requisitos excluyentes, documentacion, garantias, plazos y criterios de ponderacion, con cita a la pagina de origen; (3) inteligencia de precios y competencia sobre las adjudicaciones historicas, consultable en lenguaje natural; (4) una boveda de documentos de la empresa con control de vencimientos, que se cruza automaticamente contra el checklist del pliego. Los datos son publicos y estan estandarizados: la ARCE publica el historico en OCDS desde 2002 y ofrece servicios REST ([Open Contracting en ARCE](https://www.gub.uy/agencia-reguladora-compras-estatales/datos-y-estadisticas/datos/open-contracting)).

## Alcance del MVP

**Semestre 1 (2027)**
- ETL completo de la API OCDS mas los dumps historicos, cargados en PostgreSQL con modelo normalizado (llamado, item, adjudicacion, proveedor).
- Descarga y parsing de pliegos (PDF nativo y escaneado con OCR), indexados en base vectorial.
- Lector de pliegos v1: extraccion con esquema de requisitos excluyentes, plazos, garantias y criterios, con cita a pagina y score de confianza.
- Conjunto de evaluacion anotado a mano (50 pliegos) y metricas de precision y recall publicadas en la entrega.
- Radar de oportunidades basico: perfil de empresa, busqueda hibrida, alertas por correo.

**Semestre 2 (2027)**
- Inteligencia de precios: precios adjudicados por item y organismo, con resolucion de entidades sobre descripciones libres.
- Consultas en lenguaje natural sobre el historico (Text-to-SQL con validacion de consultas).
- Boveda documental multi-tenant con vencimientos y verificacion automatica contra el checklist del pliego.
- Piloto con 3 a 5 PyMEs midiendo horas por oferta y requisitos detectados contra omitidos.
- Endurecimiento: aislamiento por tenant, defensa contra inyeccion de prompt desde pliegos, pruebas de regresion de extraccion en CI.

## Stack propuesto

Python con FastAPI para el backend y los workers; PostgreSQL para el modelo OCDS y las vistas analiticas; Qdrant para los embeddings de pliegos y descripciones de items; PyMuPDF mas Tesseract para parsing y OCR; modelos de lenguaje chicos via Azure OpenAI con salidas estructuradas validadas contra esquema; frontend en Next.js; contenedores Docker sobre una instancia EC2 con S3 para los PDF; Terraform para infraestructura y GitHub Actions para CI, incluyendo la suite de evaluacion que corta el build si cae la exactitud de extraccion.

## Costo de infraestructura (anual)

| Concepto | USD/año | Supuesto | Fuente de precio |
| --- | --- | --- | --- |
| Instancia de aplicacion y ETL (EC2 t4g.small, 24/7) | 150 | 1 instancia on demand, 2 vCPU y 2 GB, sin reserva | [AWS EC2 On-Demand](https://aws.amazon.com/ec2/pricing/on-demand/) |
| Almacenamiento de pliegos (S3 Standard) | 12 | 30 GB de PDF mas requests de lectura | [AWS S3](https://aws.amazon.com/s3/pricing/) |
| Base vectorial (Qdrant Cloud, tier gratuito) | 0 | Menos de 1 GB de vectores durante el MVP | [Qdrant pricing](https://qdrant.tech/pricing/) |
| Procesamiento de pliegos con LLM chico | 120 | Cada pliego se procesa una sola vez y se comparte entre clientes: unos 1.500 pliegos por mes a 20k tokens de entrada | [Azure OpenAI pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/) |
| Dominio y correo transaccional | 25 | 1 dominio anual, menos de 3.000 correos por mes dentro del plan gratuito | [Namecheap](https://www.namecheap.com/domains/) y [Resend](https://resend.com/pricing) |

**Total: USD 307 por año.**

Queda apenas por encima del techo de USD 300 del equipo. Mitigaciones: creditos de estudiante de Azure o AWS, y procesar solo llamados nuevos mas una ventana historica de tres anos en lugar de todo el historico.

## Competidores

- Gubly (Uruguay): organiza y segmenta los llamados del portal por rubro, resume con IA y envia alertas. Deja el hueco de la preparacion de la oferta y la inteligencia de precios ([El Observador](https://www.elobservador.com.uy/cafe-y-negocios/dos-jovenes-canelones-crearon-una-plataforma-facilitar-el-acceso-pequenas-empresas-las-licitaciones-n6049993)).
- LicitaLAB (Chile y Peru): mas de 1.500 clientes activos y una ronda de USD 450.000; prueba que el modelo de suscripcion se paga, pero no opera en Uruguay ni sobre la normativa local ([Forbes Peru](https://forbes.pe/negocios/2025-07-22/startup-chilena-licitalab-cerro-ronda-de-inversion-por-450-000-dolares-buscara-fortalecer-su-presencia-en-peru/)).
- Monitor de Compras Publicas de FCEA, Udelar: visualiza el historico por mecanismo y proveedor; es analitico y academico, no operativo ([Monitor](https://shiny.fcea.udelar.edu.uy/compras_publicas/)).
- Alertas del propio portal de Compras Estatales: filtros por rubro, sin lectura de pliegos ni checklist ([Compras Estatales](https://www.gub.uy/agencia-reguladora-compras-estatales/)).

## Monetización

Suscripcion mensual SaaS por empresa, con tres planes: radar y alertas en el plan base, lector de pliegos y boveda en el intermedio, inteligencia de precios y consultas en el superior. Hipotesis de precio a validar en entrevistas: entre USD 40 y USD 120 por mes segun plan, justificado contra el costo de las horas que hoy dedica un administrativo a leer pliegos. Plan para consultores de licitaciones: precio por cantidad de empresas gestionadas. La licencia de datos abiertos de Uruguay habilita el uso comercial citando la fuente ([licencia de datos abiertos](https://catalogodatos.gub.uy/)).

## Riesgos

- Competidor local ya lanzado (Gubly). Mitigacion: diferenciarse en preparacion de oferta y precios, no en alertas, y probar su producto como cliente antes de definir el alcance.
- Mercado uruguayo chico. Mitigacion: construir sobre el estandar OCDS para que sumar otro pais publicador sea un conector y no un rediseno.
- Requisitos extraidos con errores. Mitigacion: cita verificable por requisito, score de confianza y la regla de que el sistema nunca presenta ofertas.
- Pliegos escaneados o mal estructurados. Mitigacion: OCR y recorte del MVP a los tipos de procedimiento mas frecuentes.
- Cobertura parcial de los datos: no es obligatorio publicar compras por debajo del 20% del tope de compra directa del organismo, asi que el historico subestima las compras chicas ([politica de publicacion OCDS](https://www.gub.uy/agencia-reguladora-compras-estatales/politicas-y-gestion/politica-publicacion-para-estandar-open-contracting)).
- Cambios normativos del regimen de compras, como el Decreto 169/026 sobre el Plan de Compras. Mitigacion: versionar el modulo normativo.

## Supuestos declarados (sin evidencia)

- Que una PyME proveedora esta dispuesta a pagar entre USD 40 y USD 120 por mes: no hay dato publico, hay que validarlo en las entrevistas.
- Que el tiempo promedio de armado de una oferta justifica la suscripcion: no encontramos una medicion local.
- Que los pliegos adjuntos son descargables de forma estable y mayoritariamente en PDF con texto, no escaneados.
- Que el historial de adjudicaciones por RUT es suficiente para rankear oportunidades sin feedback inicial del usuario.
- Que Gubly no cubre hoy la preparacion de oferta ni la inteligencia de precios (a confirmar usando el producto).