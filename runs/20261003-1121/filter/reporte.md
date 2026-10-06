# Reporte del filtro

Run `20261003-1121`.

## Embudo

- Fichas: 28 aceptadas (28 ok, 0 bloqueadas), 0 descartadas.
- Ideas: 10 recibidas, 10 con esquema válido, 4 pasan el filtro duro.
- Alcance: 4 siguen.
- Deduplicación: 1 fusionadas.
- Torneo: 3 ideas.

## Filtro duro

| Idea | Título | Pasa | Problemas |
| --- | --- | --- | --- |
| i001 | Alertas satelitales de pasturas por WhatsApp para ganaderos chicos y medianos | no | la fuente de precio de 'WhatsApp, plantillas de utilidad' no existe: https://developers.facebook.com/docs/whatsapp/pricing; la fuente de precio de 'Gemini 3.1 Flash-Lite' no existe: https://ai.google.dev/gemini-api/docs/pricing |
| i002 | Cobros por transferencia confirmados al instante para microcomercios | sí | - |
| i003 | Comparador de pólizas con citas verificables para corredores de seguros | no | la fuente de precio de 'API Gemini 3.1 Flash-Lite y Embedding 2' no existe: https://ai.google.dev/gemini-api/docs/pricing |
| i004 | Cuaderno de campo por voz para el registro de aplicaciones fitosanitarias | no | la fuente de precio de 'API de Gemini, nivel pago' no existe: https://ai.google.dev/gemini-api/docs/pricing |
| i005 | Control de caja desde la foto del cuaderno para almacenes y comercios chicos | no | la fuente de precio de 'Gemini 3.1 Flash-Lite, nivel pago' no existe: https://ai.google.dev/gemini-api/docs/pricing; la fuente de precio de 'WhatsApp, plantillas de utilidad' no existe: https://developers.facebook.com/docs/whatsapp/pricing |
| i006 | Asistente de cartera con IA para corredores de seguros independientes | sí | - |
| i007 | Auditor de comisiones de cobro para pequeños comercios | sí | - |
| i008 | Copiloto de cartera para corredores de seguros en Uruguay | no | la fuente de precio de 'API de Gemini, nivel pago' no existe: https://ai.google.dev/gemini-api/docs/pricing |
| i009 | Conciliación de cobros multicanal con consultas en lenguaje natural para microcomercios | no | la fuente de precio de 'API Gemini 3.1 Flash-Lite y Embedding 2' no existe: https://ai.google.dev/gemini-api/docs/pricing |
| i010 | Comparador de cotizaciones y renovaciones para corredores de seguros | sí | - |

## Alcance

| Idea | Veredicto | Horas | Motivo | Recorte sugerido |
| --- | --- | --- | --- | --- |
| i002 | viable_con_recorte | 1170 | Unas 1.170 horas: ingesta de email con Cloudflare Worker y verificación DKIM 80, parsers de 3 bancos 60, backend con pedidos de cobro y cruce por monto y referencia 90, PWA con push 110, parser de respaldo con LLM 50, conciliación por extracto CSV 60, cierre de caja y reporte de comisiones 70, integración y pruebas 90, despliegue 40, entrevistas y relevamiento de avisos 60, piloto de 8 semanas 130, business case y registro URCDP 65, documentación de tesis 180, gestión y guía de reenvío para comercios 85. Supera apenas las 1.152 horas declaradas (36 por semana en 32 semanas): entra en el rango, sin margen. El riesgo mayor es que el núcleo depende de avisos bancarios por email con DKIM, monto y referencia, un supuesto sin evidencia. | Pasar el parser de respaldo con LLM a opcional (con 3 parsers deterministas y una alerta de formato fallido alcanza para el piloto) y reducir el piloto a 5 o 6 comercios durante 6 semanas. Ahorra unas 100 horas y deja el total cerca de 1.070. Si el relevamiento del semestre 1 muestra que menos de 3 bancos avisan por email con monto y referencia, la conciliación por extracto CSV pasa a ser el camino principal y la confirmación instantánea queda para los bancos que sí avisan. |
| i006 | viable_con_recorte | 1300 | Unas 1.300 horas: obtener, anonimizar y etiquetar 100 pólizas de auto 100, extractor PDF a JSON y evaluación por campo 105, backend con carga y reenvío por email 100, frontend 80, cartera con vencimientos y recordatorios 50, ramo hogar (esquema, etiquetado y ajuste) 70, comparador 60, RAG con cita de cláusula y su evaluación 110, revisión humana de campos dudosos 50, resúmenes para el cliente 25, integración y pruebas 90, despliegue 40, entrevistas 35, piloto de 8 semanas 80, business case y cumplimiento de la Ley 18.331 70, documentación de tesis 180, gestión 55. Supera en 13% las 1.152 horas declaradas (36 por semana en 32 semanas): entra en el rango (hasta 1.536), sin margen. Dependencia crítica: 100 pólizas reales de 4 aseguradoras sin contactos en el sector. | Dejar el ramo hogar fuera del MVP (solo auto), limitar el RAG a las condiciones generales de auto de las 4 aseguradoras del semestre 1 y pasar los resúmenes para el cliente a opcional. Ahorra unas 130 horas y deja el total cerca de 1.170. Si no se consiguen 100 pólizas reales en el semestre 1, bajar a 40 o 50 y medir la precisión por campo sobre esas, sin frenar el resto del cronograma. |
| i007 | viable_con_recorte | 1120 | Unas 1.120 horas: entrevistas y obtención de liquidaciones de 5 comercios 65, modelo de datos y lectores de MercadoPago y de un adquirente de POS 130, costo por canal con control de totales 40, backend y carga de archivos 70, panel web 80, validación manual de 3 comercios 25, mapeo asistido por LLM con exactitud por campo 110, alertas sobre tarifa contratada 40, simulador con efecto en caja 70, integración y pruebas 80, despliegue 35, piloto de 6 semanas 90, business case y cumplimiento de la Ley 18.331 60, documentación de tesis 180, gestión 50. Casi igual a las 1.152 horas declaradas (36 por semana en 32 semanas): entra, sin margen. Riesgo: conseguir liquidaciones sin contactos; 6 semanas de piloto dan 1 o 2 liquidaciones por comercio, poco para medir ahorro real. | Limitar el simulador a cambios de plan y de plazo de acreditación dentro de los 2 proveedores ya leídos, sin simular el traspaso de ventas entre canales (el panel ya muestra el costo por canal), y medir en el piloto el ahorro estimado y la disposición a pagar, no el ahorro realizado. Ahorra unas 40 horas y deja margen para imprevistos. |
| i010 | viable_con_recorte | 1330 | MVP tal como está escrito: unas 1.330 h. S1: conseguir, anonimizar y etiquetar 80 cotizaciones de 3 aseguradoras (140 h), extracción LLM más reglas desde PDF y correo con enlace al fragmento de origen (200 h), comparación y PDF para el cliente (120 h), medición de exactitud por campo (40 h). S2: RAG con cita de cláusula y su evaluación (150 h), cartera, alertas y renovación precargada (120 h), cuentas multiusuario por corretaje (80 h), piloto de 6 semanas (80 h). Transversal: despliegue, integración y pruebas (130 h), cumplimiento de la Ley 18.331 (30 h), tesis y business case (180 h), coordinación (60 h). Las horas declaradas (16 + 10 + 10 por 32 semanas) dan unas 1.150 h: se pasa en un 15%, entra recortando. El riesgo mayor es el set de 80 cotizaciones, sin contactos en la tabla. | Sacar las cuentas multiusuario (un usuario por corretaje en el piloto, unas 80 h); limitar la entrada a PDF y dejar el parseo de correos afuera (unas 30 h); reducir la renovación precargada a reutilizar la última comparación de la póliza más la alerta por email, sin flujo propio (unas 40 h). Queda en unas 1.180 h. Si en marzo de 2027 no hay cotizaciones de corredores, arrancar con el plan B de la idea (cotizar vehículos propios en los canales públicos de las aseguradoras) para no bloquear la entrega del semestre 1. |

## Duplicados

- Queda i010; salen i006.

## Al torneo

- i002: Cobros por transferencia confirmados al instante para microcomercios
- i010: Comparador de cotizaciones y renovaciones para corredores de seguros
- i007: Auditor de comisiones de cobro para pequeños comercios
