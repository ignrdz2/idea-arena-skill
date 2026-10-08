# Red social con IA para recomendar restaurantes en Montevideo

**Problema.** Decidir donde comer lleva tiempo y las resenas disponibles son poco confiables o estan infladas. La gente termina rotando entre los mismos lugares y los restaurantes nuevos cuesta que se conozcan. No encontramos ninguna medicion de cuanto cuesta este problema a un usuario ni a un restaurante uruguayo: no hay encuestas locales, ni estudios de camaras del sector, ni reportes publicos que lo cuantifiquen. La justificacion disponible es de sentido comun y conversaciones informales con amigos.

**Usuario.** Lo usa cualquier persona de entre 20 y 45 anos que sale a comer en Montevideo. Pagaria el restaurante, por aparecer destacado o por comisiones de reservas. El usuario final no paga nada.

**Solución.** Aplicacion movil donde cada persona arma su perfil de gustos, puntua lo que come, sigue a amigos y recibe recomendaciones personalizadas generadas por un modelo de lenguaje que combina el historial propio, el de la red de contactos y las resenas de la plataforma. Incluye mapa, filtros por precio y tipo de cocina, chat para coordinar salidas y un chatbot que responde preguntas tipo "donde ceno barato cerca del Parque Rodo un martes".

## Alcance del MVP

**Semestre 1 (2027)**
- App movil con registro, perfil de gustos, buscador y mapa de restaurantes de Montevideo.
- Carga inicial del catalogo de locales y sus datos basicos.
- Sistema de resenas y puntuaciones, con seguimiento entre usuarios.
- Chatbot de recomendaciones sobre el catalogo cargado.

**Semestre 2 (2027)**
- Motor de recomendacion personalizado con filtrado colaborativo mas senales del grafo social.
- Panel para restaurantes con metricas de visualizaciones y resenas.
- Gamificacion: insignias, rankings de usuarios y desafios.
- Campana de lanzamiento para llegar a una masa inicial de usuarios y de locales.

## Stack propuesto

React Native para iOS y Android; backend en Node.js con PostgreSQL; Google Maps Platform para mapas, busqueda de lugares y geocodificacion; almacenamiento de fotos en S3; modelo de lenguaje via API para el chatbot y los resumenes de resenas; notificaciones push con Firebase; despliegue en contenedores sobre una instancia chica.

## Costo de infraestructura (anual)

| Concepto | USD/año | Supuesto | Fuente de precio |
| --- | --- | --- | --- |
| Google Maps Platform (mapas, Places, geocoding) | 180 | Uso por encima del credito mensual gratuito con unos pocos miles de cargas de mapa y busquedas | [Google Maps Platform pricing](https://mapsplatform.google.com/pricing/) |
| Cuenta de desarrollador Apple | 99 | Obligatoria para publicar en la App Store | [Apple Developer Program](https://developer.apple.com/support/compare-memberships/) |
| Cuenta de desarrollador Google Play | 25 | Pago unico, imputado al primer ano | [Google Play Console](https://support.google.com/googleplay/android-developer/answer/6112435) |
| Servidor de aplicacion | 90 | 1 instancia de 2 vCPU y 4 GB, 24/7 | [Hetzner Cloud](https://www.hetzner.com/cloud/) |
| Almacenamiento de fotos de usuarios | 25 | 100 GB de imagenes mas trafico de salida | [AWS S3](https://aws.amazon.com/s3/pricing/) |
| Chatbot y resumenes con LLM | 60 | Consultas conversacionales de usuarios gratuitos, sin tope natural de uso | [OpenAI API pricing](https://openai.com/api/pricing/) |
| Dominio y correo | 25 | 1 dominio y correo transaccional | [Namecheap](https://www.namecheap.com/domains/) |

**Total: USD 504 por año.**

Queda bastante por encima del techo de USD 300 del equipo, y el costo crece con la cantidad de usuarios gratuitos, que es justo lo contrario de lo que conviene cuando nadie paga.

## Competidores

- Google Maps: resenas, fotos, horarios, mapa y reservas, gratis y ya instalado en el telefono de todos. No deja hueco visible mas alla de la personalizacion social ([maps.google.com](https://maps.google.com/)).
- TripAdvisor: resenas con masa critica consolidada, fuerte en turismo ([tripadvisor.com](https://www.tripadvisor.com/)).
- Instagram y TikTok: hoy son el canal real de descubrimiento gastronomico informal, con recomendacion algoritmica y contenido gratuito.
- PedidosYa y plataformas de delivery, que ya concentran catalogo, resenas y la relacion comercial con los restaurantes ([pedidosya.com.uy](https://www.pedidosya.com.uy/)).
- Guias y cuentas locales de gastronomia en redes.

## Monetización

Restaurantes pagando por destacarse, por un perfil verificado o por comisiones de reserva, con una hipotesis de USD 30 a USD 60 mensuales por local. Ningun restaurante fue consultado todavia. El modelo requiere primero una base grande de usuarios activos para que la visibilidad valga algo, de modo que no hay ingresos posibles durante todo el desarrollo de la tesis.

## Riesgos

- Problema de arranque en frio por partida doble: sin usuarios no hay resenas, sin resenas no hay recomendaciones utiles, y sin audiencia ningun restaurante paga. Es el riesgo que hunde a casi todos los proyectos de este tipo.
- Competencia con productos gratuitos, universales y con una decada de datos acumulados.
- El catalogo de locales hay que construirlo y mantenerlo, y copiarlo de un tercero puede violar sus terminos de uso.
- La parte de IA es un envoltorio sobre un modelo de lenguaje mientras no haya datos propios suficientes, de modo que el aporte tecnico de la tesis queda flaco.
- Costo creciente con usuarios que no pagan.
- Contenido generado por usuarios: resenas falsas, difamacion, moderacion y responsabilidad legal.
- Datos personales de gustos, ubicacion y relaciones sociales, con perfilamiento incluido, lo que implica evaluacion de impacto bajo el Decreto 64/020 sin ningun ingreso que lo justifique.
- Sin contraparte natural que valide: no hay una gremial ni un cliente institucional claro.

## Supuestos declarados (sin evidencia)

- Que elegir restaurante es un problema suficientemente molesto como para instalar una aplicacion nueva.
- Que la gente va a escribir resenas en una plataforma sin audiencia.
- Que las recomendaciones basadas en amigos son mejores que las de Google Maps.
- Que un restaurante pagaria por aparecer destacado ante una base chica de usuarios locales.
- Que podemos conseguir y sostener una masa critica de usuarios en Montevideo durante 2027 sin presupuesto de marketing.
- Que el catalogo de locales se puede construir y mantener de forma legal y barata.
- Que el equipo puede competir en producto con aplicaciones de consumo masivo que tienen cientos de ingenieros.