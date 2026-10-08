# Pronóstico de demanda y plan de producción diario para panaderías

**Problema.** Una panaderia decide cada madrugada cuanto producir de articulos que duran horas. Si se pasa, tira o remata; si se queda corta, pierde ventas en las franjas de mayor margen. La demanda es volatil y depende del clima, el dia, los feriados y los eventos: antes de un partido de la seleccion las panaderias se preparan para vender el doble de bizcochos ([El Observador](https://www.elobservador.com.uy/tag/panaderias)). El rubro tiene margenes finos: el presidente del Centro de Industriales Panaderos del Uruguay vinculo la caida de ventas a la competencia de productos argentinos y a los altos costos productivos ([La Mañana](https://xn--lamaana-7za.uy/actualidad/panaderias-en-uruguay-entre-problemas-de-ventas-y-el-desarrollo-profesional-de-primer-nivel)). A nivel pais, entre 2011 y 2016 se perdio o desperdicio en promedio un millon de toneladas de alimentos por ano, cerca del 10% de la oferta disponible ([FAO Uruguay](https://www.fao.org/uruguay/noticias/detail/es/c/1118190)). Hay que ser honestos con ese numero: alrededor del 70% de esas perdidas ocurre en produccion y poscosecha, no en el comercio ([Ministerio de Ambiente](https://www.gub.uy/ministerio-ambiente/politicas-y-gestion/situacion-uruguay-acciones-desarrolladas)), asi que el argumento de venta es el margen del local y no la cifra nacional. No encontramos ninguna medicion publica de sobrante en panaderias uruguayas.

**Usuario.** Lo usa el dueno o el encargado de produccion de una panaderia, rotiseria o confiteria de barrio, que hoy decide de memoria. Paga el mismo local, con una suscripcion mensual baja. Canal posible de venta: la gremial del sector y los proveedores de software de punto de venta.

**Solución.** Servicio liviano, con web y bot de WhatsApp, que importa las ventas historicas del punto de venta o de los comprobantes fiscales electronicos, permite registrar en diez segundos el sobrante de cada dia, y devuelve cada tarde el plan de produccion del dia siguiente por producto y franja horaria, con una explicacion corta del porque (lluvia, feriado, evento). Sugiere ademas rebajas de ultima hora o donacion del excedente y reporta cuanto se ahorro contra el mes anterior.

## Alcance del MVP

**Semestre 1 (2027)**
- Importacion de ventas desde CSV del punto de venta y desde comprobantes fiscales electronicos en XML.
- Registro diario de produccion y sobrante por producto, en web y por WhatsApp.
- Modelo de pronostico v1 por producto y dia, con covariables de calendario y clima, evaluado con backtesting contra baselines ingenuos (media movil y mismo dia de la semana anterior).
- Piloto de recoleccion de datos con 2 o 3 locales durante al menos 10 semanas.

**Semestre 2 (2027)**
- Pronostico probabilistico y conversion a cantidad a producir con criterio de costo de sobrar contra costo de faltar.
- Modelo global entrenado entre clientes para resolver el arranque en frio de productos y locales nuevos.
- Plan de produccion por franja horaria y por horneada, con explicacion generada.
- Panel de ahorro (sobrante evitado, quiebres de stock evitados) y piloto pago con 5 locales.

## Stack propuesto

Python con FastAPI; PostgreSQL con esquema de series temporales particionado por cliente; modelos de gradient boosting (LightGBM) y comparacion con modelos globales de series; pronostico de clima desde una API publica; jobs nocturnos de reentrenamiento y prediccion con cron; bot sobre la API de WhatsApp Cloud; frontend minimo en React; todo en un unico servidor con Docker Compose, porque el volumen de datos es chico.

## Costo de infraestructura (anual)

| Concepto | USD/año | Supuesto | Fuente de precio |
| --- | --- | --- | --- |
| Servidor de aplicacion y jobs (VPS compartido) | 55 | 1 instancia de 2 vCPU y 4 GB, 24/7 | [Hetzner Cloud](https://www.hetzner.com/cloud/) |
| Base de datos gestionada | 0 | Plan gratuito, menos de 500 MB durante el MVP | [Supabase pricing](https://supabase.com/pricing) |
| API de clima | 0 | Plan gratuito de uso no comercial durante el piloto; licencia comercial al salir a produccion | [Open-Meteo pricing](https://open-meteo.com/en/pricing) |
| Mensajeria WhatsApp | 40 | Respuestas dentro de la ventana de servicio mas plantillas de recordatorio para 10 locales | [WhatsApp Business pricing](https://developers.facebook.com/docs/whatsapp/pricing/) |
| LLM para las explicaciones en texto | 15 | 1 explicacion corta por local por dia, modelo chico | [OpenAI API pricing](https://openai.com/api/pricing/) |
| Dominio | 15 | 1 dominio anual | [Namecheap](https://www.namecheap.com/domains/) |

**Total: USD 125 por año.**

## Competidores

- Delicious Data (Alemania): pronostico de demanda para panaderias y comedores; no opera en la region ni en espanol ([delicious-data.com](https://www.delicious-data.com/)).
- Foodforecast (Alemania): mismo nicho de panaderias, foco europeo ([foodforecast.com](https://www.foodforecast.com/)).
- Winnow y Leanpath: miden desperdicio en cocinas grandes con balanzas y camaras; hardware caro y pensado para hoteles y catering ([winnowsolutions.com](https://www.winnowsolutions.com/)).
- Too Good To Go: vende el excedente en lugar de evitarlo; hay que verificar si opera en Uruguay ([toogoodtogo.com](https://www.toogoodtogo.com/)).
- Los propios sistemas de punto de venta locales, que dan reportes historicos pero no pronostican.

## Monetización

Suscripcion mensual por local, hipotesis de USD 25 a USD 45, justificada contra el valor del sobrante evitado. Dos complicaciones conocidas: el ticket es chico, asi que hacen falta decenas de clientes para que el negocio exista, y el ahorro hay que demostrarlo con datos del propio local antes de que paguen. Alternativa a explorar: licenciar el motor de pronostico a un proveedor de punto de venta y cobrar por local activo.

## Riesgos

- Muchas panaderias chicas no registran ventas desagregadas por producto, asi que no hay insumo para el modelo. Mitigacion: el registro de produccion y sobrante es la primera funcionalidad del producto y genera los datos.
- Disposicion a pagar baja en un rubro con margenes golpeados.
- El pronostico puede no superar de forma clara la intuicion de un panadero con veinte anos de oficio, y si no lo supera el producto no tiene caso.
- Adopcion operativa: alguien tiene que cargar el sobrante todos los dias a las 20 horas.
- Mercado nacional chico y poco concentrado, con venta uno a uno y cara en relacion al ticket.
- Donacion de excedentes sujeta a requisitos bromatologicos departamentales.

## Supuestos declarados (sin evidencia)

- Que el sobrante diario de una panaderia esta entre el 5% y el 15% de la produccion: no hay dato publico uruguayo y el modelo de ahorro depende de esta cifra.
- Que al menos la mitad de las panaderias con las que hablemos tiene punto de venta con detalle por producto exportable.
- Que el clima y el calendario explican una parte significativa de la varianza diaria en Montevideo.
- Que el dueno acepta delegar la decision de produccion en una recomendacion de software.
- Que la gremial del sector sirve como canal de venta y no solo como contacto de validacion.