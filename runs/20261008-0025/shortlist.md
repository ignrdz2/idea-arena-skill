# Shortlist de ideas de tesis

Run `20261008-0025`, modo completo, semilla 7, creado 2026-10-08T00:25:49. Generado por /idea-arena.

Cómo leer esto:
- El puesto 1 ganó todos sus cruces y el 2 perdió solo la final. Más abajo, el orden de una eliminación simple es ruidoso: dos ideas eliminadas en la misma ronda se ordenan por el puntaje que sacaron al perder, contra rivales distintos.
- Cada idea es la última versión revisada que tuvo en el torneo.
- Nada de esto reemplaza hablar con el mercado: para eso están las preguntas y el guion de cada idea.
- Una idea que perdió su último cruce con un fallo fatal verificado (viola una restricción dura o se apoya en una afirmación sin evidencia) no se recomienda. Fuera por eso: Seguimiento de pacientes tras un intento de autoeliminación para equipos de salud mental (i002).

## Resumen

| # | Idea | Resultado en el torneo | Costo USD/año | Fichas citadas (ok / bloqueadas) |
| --- | --- | --- | --- | --- |
| 1 | Conciliación bancaria y precontabilización aprendida para estudios contables (i009) | campeona | 144 | 8 / 0 |
| 2 | Cartera digital para corredores de seguros chicos (i027) | eliminada en la ronda 4 por Conciliación bancaria y precontabiliz... | 178 | 8 / 0 |
| 3 | Prediccion de espera para retirar contenedores en el puerto de Montevideo (i028) | eliminada en la ronda 3 por Cartera digital para corredores de se... | 164 | 9 / 0 |
| 4 | Alertas tempranas de ausentismo y desvinculación para liceos privados (i010) | eliminada en la ronda 3 por Conciliación bancaria y precontabiliz... | 131 | 9 / 0 |
| 5 | Medición de tiempos de espera desde el pedido para prestadores de salud chicos (i006) | eliminada en la ronda 2 por Prediccion de espera para retirar con... | 109 | 7 / 0 |
| 6 | Consultas en lenguaje natural sobre los datos dispersos de un colegio (i011) | eliminada en la ronda 2 por Conciliación bancaria y precontabiliz... | 189 | 6 / 0 |
| 7 | Verificador de estafas por WhatsApp para vendedores online (i015) | eliminada en la ronda 2 por Alertas tempranas de ausentismo y des... | 115.08 | 12 / 1 |
| 8 | Prediagnóstico energético de mipymes a partir de sus facturas de UTE (i021) | eliminada en la ronda 2 por Cartera digital para corredores de se... | 169 | 4 / 0 |

## 1. Conciliación bancaria y precontabilización aprendida para estudios contables (i009)

Página completa: [tournament/r4/r4-m01.i009.solution.md](tournament/r4/r4-m01.i009.solution.md). Resultado: campeona.

**Problema.** Un aviso de estudio contable de Montevideo pide un asistente que registre asientos y concilie bancos con Excel intermedio (F-legal-contable-005): señal de tarea repetitiva, no de pago. Un proveedor de ERP (fuente interesada) estima que conciliar 200 a 500 movimientos lleva un día y que los bancos entregan PDF o formatos propios (F-defensa-r3-m02-i009-002). Una SRL pequeña paga honorarios fijos de $U 18.000 a 25.000 por mes (F-legal-contable-001). CFE a asiento ya está cubierto (F-ataque-r1-m05-i009-cliente-001, F-ataque-r1-m05-i009-cliente-002) y Conty declara conciliar banco y contabilidad (F-defensa-r3-m02-i009-003).

**Usuario.** Asistentes y contadores de estudios contables de 2 a 20 personas que llevan la contabilidad de pymes. Paga el estudio.

**Solución.** Lee extractos PDF de BROU e Itaú (F-defensa-r3-m02-i009-002; a confirmar) y propone la cuenta de cada movimiento aprendiendo de las imputaciones previas de cada cliente (reglas y embeddings locales), con cola de excepciones humana. Cruza con los XML de CFE y exporta un formato importable a Conty, destino de Contafácil y Contable.CFE. Datos reales solo en el piloto, en Docker dentro del equipo del propio estudio, en Uruguay; la nube recibe solo datos sintéticos, sin transferencia internacional (art. 23, F-ataque-r1-m05-i009-cliente-004).

**Costo de infraestructura.** USD 144 por año (tope USD 300).

### Rastro de veredictos

| Ronda | Rival | Persona | Puntaje | Resultado | Motivo del juez |
| --- | --- | --- | --- | --- | --- |
| 1 | Stock único que se descuenta leyendo los CFE que la pyme ya emite (i018) | Cliente real de una empresa uruguaya | 60 a 54.5 | ganó | X apunta a un hueco concreto (conciliación bancaria e imputación aprendida) que las fichas de Contafácil y Contable.CFE no cubren, frente a un comprador que ya paga por herramientas del rubro, mientras Y queda reducida a un segmento angosto, las pymes que no migran ni activan el módulo de stock de su proveedor, frente a gestionUltimate, Facture ERP y Fixed. |
| 2 | Consultas en lenguaje natural sobre los datos dispersos de un colegio (i011) | Competidor | 62 a 53 | ganó | X tiene demanda local verificada (tres avisos de estudios de Montevideo que contratan personal para conciliar bancos, dos ok y uno bloqueado, más honorarios y planes pagos de herramientas vecinas), mientras que el dolor de Y solo tiene respaldo en una ficha colombiana y su cliente uruguayo está en crisis y sin ancla de precio. |
| 3 | Alertas tempranas de ausentismo y desvinculación para liceos privados (i010) | Inversor escéptico | 62 a 54.5 | ganó | Y muestra el dolor en estudios contables uruguayos con fichas locales verificadas (avisos que piden conciliar bancos y el tiempo de conciliar a mano con extractos PDF), mientras X no tiene ninguna ficha de que el ausentismo sea un problema que los colegios privados paguen por resolver y su hueco frente a Appoderado, SInIDE y los incumbentes locales es más débil. |
| 4 | Cartera digital para corredores de seguros chicos (i027) | Tutor académico | 55.5 a 51 | ganó | X compite contra Nexura, que según las fichas ya hace en Uruguay lo mismo (PDF a datos con IA, avisos por WhatsApp, Ley 18.331), y su componente de IA depende de cláusulas de transferencia no confirmadas, mientras Y procesa localmente sin dependencia regulatoria ni de API externa y su hueco frente a Conty, aunque apoyado en silencio, no está tan cubierto. |

Ataques que quedaron en pie:

- ronda 1: Demanda delgada: una sola oferta laboral sobre conciliación, sin ficha de cantidad de estudios ni de pago por conciliación; el precio plano de $U 3.000 a 6.000 queda por encima del plan más caro de Contafácil
- ronda 2: el hueco frente a Contafácil y Contable.CFE se apoya en el silencio de sus páginas, sin ficha de pago por conciliación
- ronda 2: un incumbente con clientes y CFE de DGI puede copiar la conciliación rápido; la ventaja es solo de tiempo
- ronda 2: flujo con XML subido a mano y exportación genérica, sin importar a Conty o Zureo: dos herramientas para el estudio
- ronda 3: el pago por conciliar sigue siendo un supuesto sin señal de pago ni cantidad de estudios
- ronda 3: Conty ya declara conciliación bancaria automática; el hueco (PDF de bancos y cuenta aprendida) se apoya en silencio de su página y es copiable
- ronda 3: el producto agrega una herramienta y un paso de carga, sin evidencia de que el estudio lo tolere
- ronda 3: sin estudio voluntario el acierto real de la imputación aprendida no se demuestra
- ronda 3: costo de adquisición sin medir
- ronda 4: Demanda apoyada en un aviso laboral y un blog interesado, sin señal de pago por conciliar ni tamaño de mercado
- ronda 4: Hueco frente a Conty (PDF y cuenta aprendida) solo por silencio de su página; copiable por Contafácil
- ronda 4: Sin estudio piloto, el aprendizaje se mide solo sobre historial sintético, con validez limitada

### Preguntas para validar con el mercado

1. Pensando en el último cierre de mes: ¿cuántos movimientos bancarios conciliaron para su cliente con más movimientos, quién lo hizo, cuántas horas le llevó y en qué formato les llegó el extracto de cada banco? (a quién: asistente contable que concilia bancos en un estudio contable de 2 a 20 personas de Montevideo que lleva la contabilidad de pymes; valida: Cuánto cuesta hoy el problema (horas por cierre) y el supuesto de que los extractos llegan en PDF o formatos propios por banco; responde al ataque de demanda apoyada solo en un aviso laboral y un blog interesado.)
2. La última vez que el estudio empezó a pagar un software nuevo (por ejemplo, para bajar comprobantes o llevar la contabilidad): ¿quién lo propuso, quién aprobó el gasto, cuánto pagan por mes y lo absorbe el estudio o lo trasladan a los honorarios de los clientes? (a quién: socio o director de un estudio contable de 2 a 20 personas de Montevideo; valida: Quién decide y paga, y si hay presupuesto real para herramientas en la banda de $U 1.500 a 2.500 por mes; responde al ataque de que el pago por conciliar es un supuesto sin señal de pago.)
3. En el último cierre que hicieron, ¿con qué programa conciliaron los bancos, qué parte terminó haciéndose a mano o en Excel por fuera del programa y por qué motivo? (a quién: contador responsable de cierres mensuales en un estudio contable de Montevideo que usa Conty u otro sistema contable local; valida: El hueco frente a Conty y Contafácil, que hoy se apoya solo en el silencio de sus páginas: si la conciliación automática que declaran ya cubre extractos de BROU e Itaú o si queda trabajo manual.)
4. El mes pasado, en los movimientos bancarios sin comprobante asociado, ¿cómo decidieron a qué cuenta imputar cada uno, cuántos quedaron dudosos o hubo que corregir después, y quién los revisó? (a quién: asistente o contador que registra asientos de varias pymes clientes en un estudio contable de Montevideo; valida: El supuesto de que la imputación sigue patrones repetibles por cliente y que el historial de asientos sirve como base; responde al ataque de que sin estudio real el acierto solo se mide sobre datos sintéticos.)
5. La última vez que probaron una herramienta nueva en el estudio: ¿cuánto duró la prueba, qué datos de clientes tuvieron que cargar o exportar, quién revisó las condiciones de manejo de esos datos y por qué la dejaron o la siguieron usando? (a quién: socio o encargado de sistemas de un estudio contable de 2 a 20 personas de Montevideo; valida: Si el estudio tolera sumar una herramienta y un paso de carga, y si un piloto con datos reales y acuerdo bajo la Ley 18.331 es realista; responde a los ataques de dos herramientas para el estudio y piloto sin estudio voluntario.)

### Guion de entrevista

[shortlist/guiones/i009.md](shortlist/guiones/i009.md)

### Profundizar

`python3 skills/idea-arena/idea_arena.py deepen i009`

## 2. Cartera digital para corredores de seguros chicos (i027)

Página completa: [tournament/r4/r4-m01.i027.solution.md](tournament/r4/r4-m01.i027.solution.md). Resultado: eliminada en la ronda 4 por Conciliación bancaria y precontabiliz....

**Problema.** En Uruguay la distribución de seguros depende de corredores y productores asesores (F-fintech-seguros-008). Nexura y Figuro venden software de cartera, con precios contradictorios: Nexura desde USD 49 (F-ataque-r1-m04-i027-cliente-001) o USD 197 (F-ataque-r2-m02-i027-competidor-003); Figuro desde USD 5 (F-ataque-r2-m02-i027-competidor-002). Que perder vencimientos cueste renovaciones y que paguen USD 19 son supuestos.

**Usuario.** Corredores y productores asesores independientes, con 100 a 300 pólizas activas, en Uruguay. Ellos pagan.

**Solución.** Aplicación web donde el corredor sube pólizas PDF o importa su planilla. Un paso local seudonimiza datos personales y no envía nada al modelo si la confianza del enmascarado es baja. Un modelo extrae compañía, ramo, coberturas, prima y vencimiento; el corredor revisa solo campos de baja confianza. Un tablero muestra vencimientos a 60 días, con avisos por email y renovaciones por WhatsApp (wa.me) con un clic.

**Costo de infraestructura.** USD 178 por año (tope USD 300).

### Rastro de veredictos

| Ronda | Rival | Persona | Puntaje | Resultado | Motivo del juez |
| --- | --- | --- | --- | --- | --- |
| 1 | Registro unico de viaje y margen para fleteros con uno a tres camiones (i026) | Cliente real de una empresa uruguaya | 61.5 a 56.5 | ganó | Y tiene una señal de pago local (Nexura cobra desde USD 49 por mes a corredores uruguayos), un canal con tamaño verificado (A.PRO.A.SE., más de 500 corredores) y un costo de USD 106 con plan B de datos, mientras que la demanda de X descansa en una declaración de 2020 y un estudio de digitalización sin ninguna señal de que el fletero pague. |
| 2 | Prediagnóstico energético de mipymes a partir de sus facturas de UTE (i021) | Competidor | 61 a 47 | ganó | X tiene señales locales de pago (Nexura y Figuro cobran unos USD 50 por mes por este flujo) y un canal concreto con A.PRO.A.SE., mientras Y no tiene ninguna ficha de dolor ni de pago, compite con el asesoramiento gratuito de UTE y depende de vender leads sin validar. |
| 3 | Prediccion de espera para retirar contenedores en el puerto de Montevideo (i028) | Inversor escéptico | 57.5 a 57 | ganó | X tiene un MVP de bajo costo con plan B tecnico (parsers por plantilla) y un mercado local donde ya se paga por software de cartera, mientras Y depende de que choferes poco digitalizados generen los datos sin los cuales no hay producto y su business case no tiene precio ni tamano de flota con respaldo; eso pesa mas que la mejor diferenciacion de Y. |
| 4 | Conciliación bancaria y precontabilización aprendida para estudios contables (i009) | Tutor académico | 51 a 55.5 | perdió | X compite contra Nexura, que según las fichas ya hace en Uruguay lo mismo (PDF a datos con IA, avisos por WhatsApp, Ley 18.331), y su componente de IA depende de cláusulas de transferencia no confirmadas, mientras Y procesa localmente sin dependencia regulatoria ni de API externa y su hueco frente a Conty, aunque apoyado en silencio, no está tan cubierto. |

Ataques que quedaron en pie:

- ronda 1: La demanda sigue en buena parte como supuesto: ninguna ficha muestra que el corredor chico pierda renovaciones ni cuánto le cuesta; solo la existencia de Nexura y Figuro sugiere pago
- ronda 2: Nexura ya extrae del PDF con IA en 43 aseguradoras: el diferencial (precisión publicada y precio) es copiable
- ronda 2: El dolor (vencimientos perdidos) y la disposición a pagar USD 19 siguen sin ficha, solo como supuestos
- ronda 2: WhatsApp manual por wa.me queda por debajo de Nexura
- ronda 2: Sin contacto confirmado con corredores ni con A.PRO.A.SE.; la conversión de 5 a 10% no tiene base
- ronda 3: Nexura ya cubre el mismo segmento con extraccion de PDF por IA y avisos; el diferencial es precio y precision publicada, copiable
- ronda 3: No hay ficha del dolor ni de la disposicion a pagar del corredor de 100 a 300 polizas
- ronda 3: Sin contactos confirmados; las cartas de intencion son senal de pago debil
- ronda 3: El envio por wa.me de un clic sigue siendo mas debil que el WhatsApp automatico de Nexura
- ronda 4: Piloto y validación de pago dependen de corredores sin contacto; el plan B no prueba disposición a pagar
- ronda 4: Diferencia frente a Nexura es precio y una precisión medida, copiable, con anclas de precio contradictorias
- ronda 4: Demanda del segmento de 100 a 300 pólizas sin evidencia y solapado con Nexura desde 150
- ronda 4: Sin cláusulas de transferencia el componente de IA queda fuera de producción y la tesis se reduce a comparar parsers

### Preguntas para validar con el mercado

1. Pensando en los últimos 12 meses, ¿cuántas pólizas de su cartera no se renovaron con usted porque el vencimiento se le pasó o el cliente renovó por otro lado antes de que lo contactara? ¿Qué comisión aproximada representó eso? (a quién: corredor o productor asesor de seguros independiente en Uruguay con entre 100 y 300 pólizas activas; valida: Supuesto de que perder vencimientos cuesta renovaciones y cuánto cuesta hoy el problema (ataques en pie de rondas 1, 2 y 3: dolor sin ficha))
2. Contame cómo controló los vencimientos del último mes: ¿dónde tenía anotados los datos de cada póliza, cuánto tiempo le llevó cargar una póliza nueva desde el PDF de la aseguradora y quién hizo ese trabajo? (a quién: corredor o productor asesor de seguros independiente en Uruguay con entre 100 y 300 pólizas activas; valida: Supuesto de que los corredores chicos usan planillas y PDF, y tiempo actual de carga manual como costo del problema)
3. ¿Qué herramientas pagas usa hoy para su cartera o sus clientes (software, CRM, planillas compartidas, alguien que le haga la carga)? ¿Cuánto paga por mes, quién tomó la decisión de contratarlas y alguna vez probó o dejó un software de gestión de cartera? ¿Por qué? (a quién: corredor o productor asesor de seguros independiente en Uruguay con entre 100 y 300 pólizas activas; valida: Quién decide y paga, y disposición a pagar USD 19 por mes frente a Nexura (desde USD 49) y Figuro (desde USD 5) (ataques en pie de rondas 2, 3 y 4: pago sin ficha y anclas de precio contradictorias))
4. La última vez que se puso en contacto con un cliente por una renovación, ¿por qué medio lo hizo, cuántos mensajes intercambiaron hasta cerrarla y qué parte del proceso le resultó más lenta o más propensa a errores? (a quién: corredor o productor asesor de seguros independiente en Uruguay con entre 100 y 300 pólizas activas; valida: Ataque en pie de rondas 2 y 3: si el aviso de renovación por WhatsApp manual alcanza o si el diferencial real está en otra parte del flujo frente a Nexura)
5. Entre sus asociados, ¿cuántos trabajan con carteras de 100 a 300 pólizas, y en los últimos dos años qué proveedores de software les presentaron algo a los socios a través de la asociación y cuántos lo terminaron contratando? (a quién: integrante de la comisión directiva de A.PRO.A.SE. o de Faprosu; valida: Tamaño del segmento de 100 a 300 pólizas y acceso al canal A.PRO.A.SE. con conversión real (ataques en pie de rondas 2 y 4: segmento sin evidencia, conversión de 5 a 10% sin base, sin contacto confirmado))

### Guion de entrevista

[shortlist/guiones/i027.md](shortlist/guiones/i027.md)

### Profundizar

`python3 skills/idea-arena/idea_arena.py deepen i027`

## 3. Prediccion de espera para retirar contenedores en el puerto de Montevideo (i028)

Página completa: [tournament/r3/r3-m01.i028.solution.md](tournament/r3/r3-m01.i028.solution.md). Resultado: eliminada en la ronda 3 por Cartera digital para corredores de se....

**Problema.** La Intergremial denuncio que retirar un contenedor del puerto de Montevideo puede demorar hasta 9 horas, cuando deberia tomar 1,5 a 2; la ANP dice que son demoras normales (F-logistica-transporte-001). Es un maximo: ninguna ficha da la espera tipica, y medirla es el primer entregable. Choques: buque atrasado (F-logistica-transporte-002), paros (F-logistica-transporte-004), caidas de sistemas (F-logistica-transporte-005); no se predicen, ahi sirve la espera reportada en vivo.

**Usuario.** Usan choferes; paga la empresa, foco en flotas de 5 o mas camiones. Se supone que muchas empresas son de 1 a 3 camiones (F-logistica-transporte-009, dato de 2020) y poco digitalizadas (F-logistica-transporte-008); se mide en entrevistas.

**Solución.** PWA donde el chofer marca llegada a la fila, ingreso y salida de cada terminal con un toque (hora corregible); la ubicacion en primer plano verifica una zona amplia de acceso. Se estima la espera por terminal y franja con cuantiles historicos e intervalo. El chofer ve la espera reciente reportada por otros; el aviso de fila anomala exige un minimo de reportes. La empresa ve panel historico y horas perdidas. La terminal muestra fila y camara, no esperas (F-ataque-r3-m01-i028-inversor-001).

**Costo de infraestructura.** USD 164 por año (tope USD 300).

### Rastro de veredictos

| Ronda | Rival | Persona | Puntaje | Resultado | Motivo del juez |
| --- | --- | --- | --- | --- | --- |
| 1 | Registro offline de tratamientos veterinarios con retiro calculado, listo para declarar al SNIG (i012) | Cliente real de una empresa uruguaya | 58 a 45.5 | ganó | X tiene un dolor local repetido y con pérdidas en dólares (F-001, F-002) sin competidor directo en las fichas, mientras que en Y el bloqueo gratuito del SNIG ya cubre el núcleo del problema, Gecos queda como copia rápida y no hay precio ni señal de pago. |
| 2 | Medición de tiempos de espera desde el pedido para prestadores de salud chicos (i006) | Competidor | 59 a 58.5 | ganó | Con demanda pareja y mejor viabilidad y business case en X, Y gana por poco porque su hueco no choca con un sistema gratuito del regulador que arranca en 2027 y porque su estimador con error medido contra linea base aporta un desafio de ingenieria y un uso del perfil de datos que X, casi un CRUD con Text-to-SQL opcional, no tiene. |
| 3 | Cartera digital para corredores de seguros chicos (i027) | Inversor escéptico | 57 a 57.5 | perdió | X tiene un MVP de bajo costo con plan B tecnico (parsers por plantilla) y un mercado local donde ya se paga por software de cartera, mientras Y depende de que choferes poco digitalizados generen los datos sin los cuales no hay producto y su business case no tiene precio ni tamano de flota con respaldo; eso pesa mas que la mejor diferenciacion de Y. |

Ataques que quedaron en pie:

- ronda 1: No hay evidencia de que saber la espera permita una decisión que ahorre plata; queda como supuesto central a probar en el piloto
- ronda 1: Adopción baja y arranque en frío: sin choferes que marquen no hay predicción, y no hay empresa piloto ni contactos
- ronda 1: Business case con precio hipotético de USD 5 por camión, sin tamaño de mercado ni contacto con el canal
- ronda 2: Arranque en frio y sustituto gratis del aviso informal entre choferes
- ronda 2: Terminales o ANP pueden publicar el indicador con datos exactos; cuantiles y panel son copiables
- ronda 2: Ticket chico en un sector de empresas de pocos camiones y tamano de mercado sin ningun numero
- ronda 3: No hay ficha de la espera tipica; el dolor citado es un maximo denunciado y shocks que no se predicen
- ronda 3: El segmento que paga (flotas de 5 o mas camiones) no tiene tamano conocido
- ronda 3: Precio y disposicion a pagar sin ninguna senal; canal sin contacto
- ronda 3: Arranque en frio: el valor depende de reportes manuales de choferes poco digitalizados y el plan B no entrega datos reales
- ronda 3: La terminal ya muestra LineUp y camara del acceso y podria agregar un indicador de espera

### Preguntas para validar con el mercado

1. Pensando en el último retiro de contenedor que hizo un camión suyo en el puerto de Montevideo: ¿a qué hora llegó a la fila, a qué hora salió de la terminal, y qué le costó a la empresa ese tiempo (horas de chofer, viajes que no se hicieron, multas o reclamos del cliente)? (a quién: Dueño o encargado de operaciones de una empresa de transporte uruguaya con 5 o más camiones que retira contenedores en el puerto de Montevideo; valida: Supuesto de que la espera típica (no solo el máximo de 9 horas denunciado) es relevante y cuánto cuesta hoy el problema; ataque de ronda 3 sobre la falta de ficha de la espera típica)
2. La última vez que uno de sus camiones encontró una espera larga en el acceso a una terminal, ¿qué hicieron? ¿Cambiaron la hora de salida, mandaron otro camión, reasignaron viajes o simplemente esperaron? ¿Con cuánta anticipación se enteraron? (a quién: Coordinador de tráfico o despachante de camiones de una empresa de transporte de contenedores que opera en el puerto de Montevideo; valida: Ataque de ronda 1: no hay evidencia de que saber la espera de antemano permita una decisión que ahorre plata)
3. ¿Qué software o servicio para la flota pagan hoy (rastreo, gestión de viajes u otro)? ¿Quién decidió contratarlo, cuánto pagan por mes, por cuántos camiones, y cómo se enteraron de que existía? (a quién: Dueño o gerente de una empresa de transporte de carga uruguaya con 5 o más camiones que trabaja con el puerto de Montevideo; valida: Quién decide y paga, precio y disposición a pagar (supuesto de USD 5 por camión), tamaño de flota del segmento que paga y canal de venta; ataques de rondas 1, 2 y 3 sobre business case sin señal de pago)
4. La última vez que fue a retirar un contenedor, ¿cómo supo cómo estaba la fila antes de llegar? ¿Por quién o por qué medio se enteró (grupo de WhatsApp, llamada, la página o cámara de la terminal, otro) y qué tan acertado resultó? (a quién: Chofer de camión que retira contenedores en las terminales del puerto de Montevideo al menos una vez por semana; valida: Ataques de rondas 2 y 3: sustituto gratis del aviso informal entre choferes y la información que ya publica la terminal (LineUp y cámara del acceso))
5. En el último mes, ¿qué registros les pidió la empresa a los choferes que hicieran en el celular durante el viaje (fotos de remitos, avisos de llegada, formularios)? ¿Cuántos lo hicieron siempre, cuántos a veces y qué pasó con los que no? (a quién: Encargado de operaciones o de choferes de una empresa de transporte de contenedores con 5 o más camiones en Montevideo; valida: Ataque de arranque en frío de rondas 1, 2 y 3: que choferes poco digitalizados registren datos de forma manual y constante)

### Guion de entrevista

[shortlist/guiones/i028.md](shortlist/guiones/i028.md)

### Profundizar

`python3 skills/idea-arena/idea_arena.py deepen i028`

## 4. Alertas tempranas de ausentismo y desvinculación para liceos privados (i010)

Página completa: [tournament/r3/r3-m02.i010.solution.md](tournament/r3/r3-m02.i010.solution.md). Resultado: eliminada en la ronda 3 por Conciliación bancaria y precontabiliz....

**Problema.** En Uruguay, de 100 adolescentes que ingresaron al liceo en 2017 solo 43 egresaron en ocho años y casi la mitad faltó al menos el 11% de los días (F-educacion-001). Son cifras de liceos en general: ninguna ficha muestra que apliquen a privados ni que alguien pague por resolverlo; es lo primero a validar. Los liceos privados suman 41.235 alumnos (F-defensa-r1-m03-i010-001).

**Usuario.** Adscriptos y coordinadores de liceos de colegios privados (Audec y Aidep: unos 220 colegios, F-educacion-004); paga la dirección.

**Solución.** Plataforma web que importa planillas CSV o Excel de asistencia y notas, sin depender de la API de ninguna suite. Calcula un puntaje de riesgo con reglas explicables más un modelo simple y genera una lista semanal priorizada con el motivo de cada alerta. Registra cada intervención y su resultado. Los avisos a familias salen de plantillas que el adscripto envía; el borrador con LLM es opcional y sintético.

**Costo de infraestructura.** USD 131 por año (tope USD 300).

### Rastro de veredictos

| Ronda | Rival | Persona | Puntaje | Resultado | Motivo del juez |
| --- | --- | --- | --- | --- | --- |
| 1 | Copiloto de obligaciones fiscales para unipersonales que empiezan (i001) | Cliente real de una empresa uruguaya | 65.5 a 53.5 | ganó | X apoya el dolor en varias fichas locales verificadas (ausentismo y desvinculación, matrícula privada, crisis del sector) y corre sin dependencias sobre datos sintéticos a USD 119, mientras Y admite que su dolor central es hipótesis y compite con un calendario gratuito local (Calculame) y con el contador. |
| 2 | Verificador de estafas por WhatsApp para vendedores online (i015) | Competidor | 57 a 52.5 | ganó | X tiene un cliente pagador acotado (unos 220 colegios, 41.235 alumnos de liceo privado) con precio y techo de mercado coherentes y un MVP demostrable sin dependencias, mientras Y compite contra verificadores gratuitos de WhatsApp ya existentes en LATAM, sin tamaño de mercado ni canal. |
| 3 | Conciliación bancaria y precontabilización aprendida para estudios contables (i009) | Inversor escéptico | 54.5 a 62 | perdió | Y muestra el dolor en estudios contables uruguayos con fichas locales verificadas (avisos que piden conciliar bancos y el tiempo de conciliar a mano con extractos PDF), mientras X no tiene ninguna ficha de que el ausentismo sea un problema que los colegios privados paguen por resolver y su hueco frente a Appoderado, SInIDE y los incumbentes locales es más débil. |

Ataques que quedaron en pie:

- ronda 1: Ninguna ficha muestra ausentismo o desvinculación en colegios privados: el dolor en el cliente es un supuesto
- ronda 1: Las suites existentes (Asistente.uy, Colegium) podrían sumar alertas; el hueco se infiere de la ausencia de información
- ronda 1: Disposición a pagar y retención medible sin evidencia; el piloto mide detección, no ahorro
- ronda 2: hay competidores con alertas (Appoderado) o que pueden sumarlas (Asistente.uy, Trivium); el registro de intervenciones es copiable y no está validado
- ronda 2: ninguna ficha muestra que el ausentismo cueste cuotas a un colegio privado ni señales de pago: la demanda del pagador es supuesto
- ronda 3: no hay ninguna ficha de que el ausentismo cueste alumnos o cuotas a un colegio privado ni señal de pago
- ronda 3: el hueco (medir intervenciones) es copiable por Asistente.uy, Colegium o Trivium, ya hay alertas en Appoderado y SInIDE, y un trimestre no mide retención
- ronda 3: canal y costo de adquisición sin medir en un sector pagador en crisis
- ronda 3: sin colegio piloto el modelo de riesgo se valida solo sobre datos sintéticos

### Preguntas para validar con el mercado

1. Pensando en el último año, ¿cuántos alumnos de liceo dejaron el colegio a mitad de año o no se reinscribieron, y de esos casos, en cuántos hubo antes un período de faltas repetidas? ¿Cómo se enteraron ustedes de cada caso? (a quién: director o directora de liceo de un colegio privado de Montevideo afiliado a Audec o Aidep; valida: Ataque en pie (rondas 1 y 3): ninguna ficha muestra ausentismo o desvinculación en colegios privados; supuesto de que el ausentismo de liceos públicos se parece al de privados.)
2. La última vez que se fue un alumno de liceo por desvinculación, ¿qué le costó al colegio: cuántos meses de cuota se dejaron de cobrar, quedó la vacante sin cubrir, y cuántas horas de adscripción y dirección se dedicaron a ese caso antes de que se fuera? (a quién: director o administrador de un colegio privado mediano de Montevideo (unos 200 a 500 alumnos de liceo); valida: Cuánto cuesta hoy el problema. Ataque en pie (rondas 2 y 3): ninguna ficha muestra que el ausentismo cueste cuotas o alumnos a un colegio privado.)
3. Contame cómo detectaste el último caso de un alumno que empezaba a faltar seguido: ¿de dónde sacaste el dato, qué planilla o sistema usaste, cuánto tiempo pasó desde la primera falta hasta que actuaste, y qué hiciste después? ¿Quedó registrado en algún lado si funcionó? (a quién: adscripto o coordinador de liceo en un colegio privado de Montevideo; valida: Supuesto de que los colegios exportan asistencia y notas en planilla, y ataque en pie (rondas 1, 2 y 3): las suites existentes (Asistente.uy, Colegium, Trivium) ya cubren el seguimiento o pueden sumarlo; el registro de intervenciones como hueco.)
4. La última vez que el colegio contrató o renovó un software o servicio para el área de liceo (gestión, asistencia, comunicación con familias), ¿quién lo propuso, quién aprobó el gasto, de qué presupuesto salió, cuánto se paga por año y cuánto tardó la decisión? (a quién: director general o responsable administrativo financiero de un colegio privado afiliado a Audec o Aidep; valida: Quién decide y paga. Supuestos de precio (unos USD 3 por alumno de liceo por año) y ataque en pie (rondas 1, 2 y 3): disposición a pagar sin evidencia en un sector con caja ajustada.)
5. ¿Cómo llegó al colegio el último proveedor de software educativo que adoptaron: por recomendación de otro colegio, por Audec o Aidep, por un evento, por contacto directo del proveedor? ¿Qué otras herramientas evaluaron o probaron ese año y por qué las descartaron? (a quién: director de liceo o coordinador académico de un colegio privado de Montevideo o del interior; valida: Ataque en pie (ronda 3): canal y costo de adquisición sin medir; supuesto del canal vía Audec, Aidep y directores; competidores reales que el colegio ya considera.)

### Guion de entrevista

[shortlist/guiones/i010.md](shortlist/guiones/i010.md)

### Profundizar

`python3 skills/idea-arena/idea_arena.py deepen i010`

## 5. Medición de tiempos de espera desde el pedido para prestadores de salud chicos (i006)

Página completa: [tournament/r2/r2-m01.i006.solution.md](tournament/r2/r2-m01.i006.solution.md). Resultado: eliminada en la ronda 2 por Prediccion de espera para retirar con....

**Problema.** El decreto de 2026 fija plazos máximos de espera y un monitoreo nacional obligatorio (F-salud-001, F-ataque-r1-m01-i006-cliente-001). Las fuentes difieren: el MSP da 24 horas hábiles en medicina general y 30 días corridos para especialistas; Presidencia, 30 días con médico tratante y hasta 90 con especialista. En 2025 el MSP admitía que su cálculo no cuenta agenda cerrada (F-salud-002); en octubre de 2026 anunció un sistema de medición en todos los prestadores desde 2027 (F-ataque-r2-m01-i006-competidor-001).

**Usuario.** Dirección técnica y administración de prestadores integrales chicos o del interior y de policlínicas privadas. Paga el prestador; lo usan el administrativo de agenda y la dirección.

**Solución.** Herramienta de gestión interna: muestra el cumplimiento propio y alerta vencimientos mientras el prestador aún puede corregir. Mide la espera desde el pedido y la concilia con el turno. Importa CSV con plantilla propia y mapeo de columnas, sin identificar al paciente; si la agenda no guarda el pedido, un formulario registra fecha y hora. Los plazos van en una tabla versionada. Calcula la espera por especialidad, alerta y genera el reporte. Text-to-SQL es un hito final opcional.

**Costo de infraestructura.** USD 109 por año (tope USD 300).

### Rastro de veredictos

| Ronda | Rival | Persona | Puntaje | Resultado | Motivo del juez |
| --- | --- | --- | --- | --- | --- |
| 1 | Portal de cambios y devoluciones para tiendas online uruguayas (i005) | Cliente real de una empresa uruguaya | 62 a 45.5 | ganó | Y apoya el problema en un decreto local con plazos y monitoreo obligatorio y en la admision del MSP de que el calculo no cuenta la agenda cerrada, con un hueco que ninguna ficha de competidor cubre, mientras X compite contra Boris y Undo que ya hacen lo mismo y su dolor (volumen y costo de devoluciones) no tiene ficha. |
| 2 | Prediccion de espera para retirar contenedores en el puerto de Montevideo (i028) | Competidor | 58.5 a 59 | perdió | Con demanda pareja y mejor viabilidad y business case en X, Y gana por poco porque su hueco no choca con un sistema gratuito del regulador que arranca en 2027 y porque su estimador con error medido contra linea base aporta un desafio de ingenieria y un uso del perfil de datos que X, casi un CRUD con Text-to-SQL opcional, no tiene. |

Ataques que quedaron en pie:

- ronda 1: la disposicion a pagar del prestador chico sigue sin ficha: el decreto no le exige herramienta propia y el monitoreo lo hace el MSP
- ronda 1: un software de agenda que ya tiene los turnos podria agregar el indicador desde el pedido con poco desarrollo
- ronda 2: El sistema gratuito del MSP desde 2027 deja poco margen al diferencial de alerta previa
- ronda 2: Cualquier agenda (Zalon, CliniGest) puede agregar el indicador sobre datos que ya tiene
- ronda 2: Precio de USD 60 a 150 sin senal de pago frente a una agenda completa de $25 al mes y mercado de pocas decenas de prestadores

### Preguntas para validar con el mercado

1. La última vez que tuvieron que informar o revisar tiempos de espera (al MSP, a la dirección o por un reclamo), ¿desde qué fecha contaron la espera, de dónde sacaron los datos, quién hizo el cálculo y con qué herramienta? (a quién: administrativo o jefe de agenda de un prestador integral chico del interior de Uruguay; valida: Supuesto de que el prestador chico no mide la espera desde el pedido, y que la carencia que el MSP admitía en 2025 (no contar agenda cerrada) sigue vigente)
2. Desde que rige el decreto de plazos de 2026, ¿cuál fue el último caso de espera fuera de plazo que tuvieron? ¿Cómo y cuándo se enteraron, qué consecuencia tuvo (reclamo, observación del MSP, gasto en derivar) y cuántas horas de qué personas llevó resolverlo? (a quién: director técnico de un prestador integral chico o de una policlínica privada de Uruguay; valida: Cuánto cuesta hoy el problema y si detectar el vencimiento antes tiene valor; ataque en pie: el decreto no exige herramienta propia y la disposición a pagar no tiene ficha)
3. La última vez que contrataron un software para administración o agenda, ¿quién lo propuso, quién aprobó el gasto, de qué presupuesto salió, cuánto pagan por mes y cuánto tiempo pasó entre la primera reunión y la firma? (a quién: gerente administrativo o de finanzas de un prestador integral chico o de una policlínica privada de Montevideo o del interior; valida: Quién decide y paga, y si el precio de USD 60 a 150 al mes es sostenible frente a agendas de $25 al mes; ataque en pie sobre precio sin señal de pago y ciclo de venta largo)
4. ¿Qué sistema de agenda usan hoy y registra la fecha en que el paciente pidió la hora? La última vez que necesitaron un dato o reporte que ese sistema no daba, ¿cómo lo consiguieron (exportación, planilla, pedido al proveedor) y cuánto tardó? (a quién: responsable de sistemas o de agenda de una policlínica privada o prestador chico de Uruguay; valida: Supuestos de que las agendas exportan CSV y no guardan el pedido; ataque en pie: el proveedor de agenda (Zalon, CliniGest) puede agregar el indicador con los datos que ya tiene)
5. ¿Qué les comunicó el MSP hasta ahora sobre el sistema de medición de tiempos de espera que anunció para 2027: qué datos les pidió, en qué formato, con qué frecuencia y quién en la institución quedó a cargo de prepararlos? (a quién: director técnico o responsable de calidad de un prestador integral chico del interior de Uruguay; valida: Ataque en pie: el sistema gratuito del MSP desde 2027 puede dejar sin margen a la gestión interna con alertas previas, o en cambio generar trabajo nuevo de preparación de datos)

### Guion de entrevista

[shortlist/guiones/i006.md](shortlist/guiones/i006.md)

### Profundizar

`python3 skills/idea-arena/idea_arena.py deepen i006`

## 6. Consultas en lenguaje natural sobre los datos dispersos de un colegio (i011)

Página completa: [tournament/r2/r2-m03.i011.solution.md](tournament/r2/r2-m03.i011.solution.md). Resultado: eliminada en la ronda 2 por Conciliación bancaria y precontabiliz....

**Problema.** Los colegios privados uruguayos están en crisis: más de 300, tres cierres a fines de 2023 y el MEC analizando fusiones (F-educacion-004). Para decidir precios, becas y grupos, la dirección necesita cruzar matrícula, cobranza y asistencia. En Colombia cerca de dos tercios usan plataformas no integradas (F-educacion-007); mide integración, no consultas, y en Uruguay es un supuesto.

**Usuario.** Directores y administradores de colegios privados con varios sistemas; paga el colegio.

**Solución.** Capa de datos que consolida exportaciones de los sistemas del colegio (facturación, gestión académica, planillas) en una base única con catálogo semántico, y un asistente Text-to-SQL en español: familias con cuotas atrasadas por nivel, matrícula por grado. Al modelo solo viajan esquema, glosario y pregunta, nunca filas: la consulta corre en el servidor propio. Cada respuesta muestra consulta, tabla, gráfico y fecha del último dato.

**Costo de infraestructura.** USD 189 por año (tope USD 300).

### Rastro de veredictos

| Ronda | Rival | Persona | Puntaje | Resultado | Motivo del juez |
| --- | --- | --- | --- | --- | --- |
| 1 | Reclamos vecinales por WhatsApp para municipios chicos, con implantación liviana (i017) | Cliente real de una empresa uruguaya | 56 a 52.5 | ganó | Con demanda igual de débil en las dos (contexto local más supuestos de pago), X gana por encaje directo con la especialidad Text-to-SQL del equipo, un desafío académico medible y un business case algo más cuantificado, mientras Y enfrenta un sustituto gratuito con respaldo estatal (Agesic) y un comprador que la ficha 008 muestra reacio a pagar. |
| 2 | Conciliación bancaria y precontabilización aprendida para estudios contables (i009) | Competidor | 53 a 62 | perdió | X tiene demanda local verificada (tres avisos de estudios de Montevideo que contratan personal para conciliar bancos, dos ok y uno bloqueado, más honorarios y planes pagos de herramientas vecinas), mientras que el dolor de Y solo tiene respaldo en una ficha colombiana y su cliente uruguayo está en crisis y sin ancla de precio. |

Ataques que quedaron en pie:

- ronda 1: La demanda uruguaya no tiene ficha: el dolor viene de una ficha colombiana y queda como supuesto
- ronda 1: Sin señal de pago y con colegios en crisis; quién decide la compra sigue desconocido
- ronda 1: El hueco frente a las suites y a las hojas de cálculo con IA se apoya en lo que las fichas no dicen y es copiable
- ronda 1: La carga manual de exportar CSV y mantener el glosario sigue sin resolverse
- ronda 2: un incumbente con los datos en su base puede sumar consultas en lenguaje natural sin migración
- ronda 2: el dolor de sistemas no integrados solo tiene ficha colombiana; en Uruguay es supuesto, sin señal de pago
- ronda 2: el segmento objetivo está en crisis y el precio de USD 60 a 120 no tiene ancla
- ronda 2: importadores y exactitud solo probados con datos sintéticos, sin formatos de exportación reales
- ronda 2: BI genérico e IA de planillas son la alternativa real y la diferencia es copiable

### Preguntas para validar con el mercado

1. La última vez que la dirección necesitó un dato que cruzaba cobranza, matrícula y asistencia (por ejemplo, para decidir becas o cuotas), ¿de qué sistemas o planillas salió cada parte y cómo lo armaron? (a quién: administrador o secretario administrativo de un colegio privado de Montevideo; valida: Supuesto de que los colegios uruguayos usan sistemas no integrados y planillas; ataque de que ese dolor solo tiene ficha colombiana y en Uruguay es supuesto)
2. En el último cierre de mes, ¿cuántas horas y cuántas personas dedicaron a preparar los reportes de morosidad y matrícula que pide la dirección, y alguna vez se tomó una decisión con un dato que después resultó estar mal? (a quién: administrador o contador interno de un colegio privado de Montevideo; valida: Cuánto cuesta hoy el problema; supuesto de que morosidad y matrícula son consultas frecuentes)
3. La última vez que el colegio contrató un software o servicio de gestión, ¿quién lo propuso, quién aprobó el gasto, de qué presupuesto salió y cuánto pagan hoy por mes por esas herramientas? (a quién: director o representante legal de un colegio privado asociado a Audec o Aidep; valida: Quién decide y paga; ataque de que el precio de USD 60 a 120 por mes no tiene ancla y el segmento está en crisis)
4. La última vez que necesitaron sacar datos de su sistema de facturación o de gestión académica, ¿cómo lo hicieron, en qué formato salió y cuánto trabajo manual hubo que hacer después? (a quién: encargado de sistemas o de secretaría de un colegio privado de Montevideo que usa un sistema de gestión escolar; valida: Supuesto de que los sistemas exportan a CSV; ataques de carga manual de exportaciones e importadores probados solo con datos sintéticos)
5. Cuando la dirección pidió un número que el sistema de gestión no muestra, ¿qué hicieron: lo pidieron al proveedor del sistema, armaron una tabla dinámica o un tablero, o quedó sin responder? ¿Qué pasó con ese pedido? (a quién: director o administrador de un colegio privado de Montevideo que usa una suite de gestión escolar; valida: Ataques de que un incumbente puede sumar consultas sin migración y de que BI genérico e IA de planillas son la alternativa real)

### Guion de entrevista

[shortlist/guiones/i011.md](shortlist/guiones/i011.md)

### Profundizar

`python3 skills/idea-arena/idea_arena.py deepen i011`

## 7. Verificador de estafas por WhatsApp para vendedores online (i015)

Página completa: [tournament/r2/r2-m04.i015.solution.md](tournament/r2/r2-m04.i015.solution.md). Resultado: eliminada en la ronda 2 por Alertas tempranas de ausentismo y des....

**Problema.** Las denuncias por estafa en Uruguay pasaron de 1.872 en 2015 a 25.116 en 2024 (F-fintech-seguros-004). El BCU lista phishing, suplantación y estafas de Marketplace (F-fintech-seguros-006). Se reportan comprobantes con capturas adulteradas por WhatsApp, Marketplace e Instagram (F-defensa-r1-m08-i015-002). La pérdida del vendedor no está medida: se mide en entrevistas y piloto.

**Usuario.** Emprendedores y pymes que venden por WhatsApp, Instagram o marketplaces en Uruguay. Pagan los del plan negocio.

**Solución.** Un número de WhatsApp al que el vendedor reenvía un mensaje de comprador, un link o la captura de un comprobante. Un modelo con visión analiza texto e imagen, revisa el dominio y contrasta con la tipología del BCU. Responde con señales y qué verificar; nunca dice 'seguro'. Antes de enviar al modelo se enmascaran teléfonos, cuentas y cédulas; las capturas exigen consentimiento, y si el camino legal no se confirma, el MVP queda en texto y links. El plan negocio suma capturas, historial y un panel con avisos de dominios y textos (nunca personas); sin mensajes proactivos.

**Costo de infraestructura.** USD 115.08 por año (tope USD 300).

### Rastro de veredictos

| Ronda | Rival | Persona | Puntaje | Resultado | Motivo del juez |
| --- | --- | --- | --- | --- | --- |
| 1 | Seguimiento de pacientes tras un intento de autoeliminación para equipos de salud mental (i002) | Cliente real de una empresa uruguaya | 61.5 a 54 | ganó | Y apoya su argumento de demanda en una ficha que no existe (fallo fatal) y además encaja peor con el perfil de IA del equipo, mientras X arregló sus ataques con evidencia local verificada y un costo de USD 115 bien sustentado. |
| 2 | Alertas tempranas de ausentismo y desvinculación para liceos privados (i010) | Competidor | 52.5 a 57 | perdió | X tiene un cliente pagador acotado (unos 220 colegios, 41.235 alumnos de liceo privado) con precio y techo de mercado coherentes y un MVP demostrable sin dependencias, mientras Y compite contra verificadores gratuitos de WhatsApp ya existentes en LATAM, sin tamaño de mercado ni canal. |

Ataques que quedaron en pie:

- ronda 1: Disposición a pagar y tamaño de mercado sin base: 100 pymes es una hipótesis, sin canal ni contactos
- ronda 2: existen verificadores gratuitos por WhatsApp en LATAM (Mediavox, ScamZero, Truecaller en camino) y la diferencia restante es foco Uruguay y capturas
- ronda 2: el plan de USD 6 compite contra opciones gratis sin ninguna ficha de disposición a pagar
- ronda 2: el dolor específico del vendedor (comprobante falso) se resuelve gratis mirando la cuenta; frecuencia y pérdida no medidas
- ronda 2: sin tamaño de mercado de vendedores ni canal: 100 pymes es un escenario ilustrativo
- ronda 2: sin foso: modelo de terceros más un set propio que se puede replicar

Notas de Python:

- ronda 1: fatal determinístico de i002: evidencia_inexistente

### Preguntas para validar con el mercado

1. Contame la última vez que un comprador te mandó un comprobante de pago o un mensaje que resultó falso o te hizo dudar: ¿cuándo fue, por qué canal llegó y cuántas veces te pasó algo así en los últimos 3 meses? (a quién: emprendedor o dueño de una pyme uruguaya que vende por WhatsApp, Instagram o Mercado Libre y cobra por transferencia; valida: Supuesto de que los vendedores reciben comprobantes falsos o phishing con frecuencia suficiente, y el ataque de ronda 2 de que la frecuencia no está medida)
2. En el último caso de estafa o intento de estafa que tuviste vendiendo, ¿cuánto perdiste en plata, mercadería o envío, y cuánto tiempo por semana le dedicás hoy a revisar pagos y compradores antes de despachar? (a quién: emprendedor o dueño de una pyme uruguaya que vende por WhatsApp, Instagram o Mercado Libre y cobra por transferencia; valida: Cuánto cuesta hoy el problema: el ataque de ronda 2 de que la pérdida del vendedor no está medida)
3. La última vez que dudaste de un pago o de un mensaje de un comprador, ¿cómo lo verificaste paso a paso: miraste la cuenta del banco, consultaste a alguien, usaste alguna app o página? ¿Cuánto tardaste y te quedó alguna duda? (a quién: emprendedor o dueño de una pyme uruguaya que vende por WhatsApp, Instagram o Mercado Libre y cobra por transferencia; valida: Ataques de ronda 2: el comprobante falso se resuelve gratis mirando la cuenta y ya existen verificadores gratuitos; muestra si queda un hueco real sin resolver)
4. ¿Qué herramientas o servicios pagás hoy todos los meses para el negocio (para cobrar, publicar, atender clientes o gestionar ventas), cuánto pagás por cada uno, quién decidió contratarlos y cuál dejaste de pagar en el último año y por qué? (a quién: dueño o socio que maneja los gastos de una pyme uruguaya que vende por redes sociales o marketplaces; valida: Quién decide y paga, y el ataque de ronda 2 de que el plan de USD 6 por mes compite contra opciones gratis sin evidencia de disposición a pagar)
5. En el último año, ¿cuántos emprendedores de tu comunidad o red te consultaron o contaron que sufrieron una estafa al vender, y por qué medios se enteraron de la última herramienta nueva que empezaron a usar varios de ellos? (a quién: coordinador de una comunidad, grupo o programa de apoyo a emprendedores que venden online en Uruguay; valida: Ataques de ronda 1 y 2 de falta de tamaño de mercado y de canal: 100 pymes es solo un escenario ilustrativo y no hay contactos)

### Guion de entrevista

[shortlist/guiones/i015.md](shortlist/guiones/i015.md)

### Profundizar

`python3 skills/idea-arena/idea_arena.py deepen i015`

## 8. Prediagnóstico energético de mipymes a partir de sus facturas de UTE (i021)

Página completa: [tournament/r2/r2-m02.i021.solution.md](tournament/r2/r2-m02.i021.solution.md). Resultado: eliminada en la ronda 2 por Cartera digital para corredores de se....

**Problema.** Las mipymes son el 80% de las empresas; el MIEM lanzó en 2020 un simulador y un reintegro de hasta USD 3.000 para estudios de eficiencia (F-energia-ambiente-001). La tarifa General Simple (hasta 40 kW) cobra potencia contratada y cargo fijo, con opción Hora-Estacional (F-defensa-r1-m02-i021-001); elegir exige leer la factura. Que paguen de más y paguen por saberlo son hipótesis a medir.

**Usuario.** Dueño o administrador de una mipyme con factura de UTE no residencial. Segundo cliente: consultores e instaladores.

**Solución.** Asesor independiente de UTE: la mipyme sube 12 facturas en PDF o foto. Un extractor con LLM y validación por reglas arma la serie de consumo, potencia y cargos. Un motor de reglas basado en el decreto estima, como rango, ahorros por ajustar potencia o pasar a Hora-Estacional (sin recomendar bajar potencia sin demanda medida) y un escenario solar editable. UTE gana si el cliente cambia de plan; este informe no.

**Costo de infraestructura.** USD 169 por año (tope USD 300).

### Rastro de veredictos

| Ronda | Rival | Persona | Puntaje | Resultado | Motivo del juez |
| --- | --- | --- | --- | --- | --- |
| 1 | Inteligencia de demanda por mercado de origen para posadas y cabañas del interior (i003) | Cliente real de una empresa uruguaya | 55.5 a 53 | ganó | Con demanda igual de floja en las dos (dolor y pago declarados como supuestos), X ofrece algo que la mipyme no obtiene gratis (leer sus facturas y calcular el ahorro con el decreto 339/2025 verificado), mientras que la capa base de Y se reduce a datos trimestrales nacionales y al tipo de cambio públicos, con un hueco débil frente a esa alternativa gratuita. |
| 2 | Cartera digital para corredores de seguros chicos (i027) | Competidor | 47 a 61 | perdió | X tiene señales locales de pago (Nexura y Figuro cobran unos USD 50 por mes por este flujo) y un canal concreto con A.PRO.A.SE., mientras Y no tiene ninguna ficha de dolor ni de pago, compite con el asesoramiento gratuito de UTE y depende de vender leads sin validar. |

Ataques que quedaron en pie:

- ronda 1: Ninguna ficha muestra que una mipyme pague de más ni que alguien pague por prediagnósticos o leads (queda como hipótesis)
- ronda 1: Diferenciación copiable: UTE o un instalador pueden extender el simulador por factura a comercios
- ronda 2: Ninguna ficha muestra que la mipyme pague de más ni que pague por saberlo
- ronda 2: UTE asesora gratis sobre tarifa y potencia; el hueco (inmediatez, solar, sin incentivo) es copiable
- ronda 2: El ahorro se corrige una vez y el segmento de bajo consumo puede no pagar
- ronda 2: El ingreso principal (USD 20 por lead a consultores e instaladores) no tiene ficha ni validación

### Preguntas para validar con el mercado

1. ¿Cuánto pagaron en promedio por mes de factura de UTE en los últimos 12 meses? ¿Alguna vez revisaron o cambiaron la potencia contratada o el tipo de tarifa? Si lo hicieron, ¿qué los llevó a hacerlo y cuánto cambió la factura siguiente? (a quién: Dueño o administrador de un comercio o taller de Montevideo con tarifa General Simple de UTE (por ejemplo, panadería, almacén o taller mecánico); valida: Costo actual del problema: supuesto sin ficha de que las mipymes pagan de más (ataque en pie de rondas 1 y 2) y tamaño del ahorro posible en el segmento de bajo consumo.)
2. ¿Alguna vez pidieron asesoramiento sobre su tarifa o su consumo eléctrico, a UTE o a otro técnico? ¿Cómo lo pidieron, cuánto tardó la respuesta, qué les recomendaron y qué terminaron aplicando? (a quién: Dueño o administrador de una mipyme uruguaya con factura de UTE no residencial; valida: Ataque en pie de ronda 2: UTE asesora gratis sobre tarifa y potencia. Valida si esa alternativa se usa y si el hueco de inmediatez y falta de incentivo es real.)
3. La última vez que la empresa pagó por un estudio, un diagnóstico o un presupuesto relacionado con energía (eficiencia, paneles solares, instalación eléctrica), ¿quién propuso hacerlo, quién aprobó el gasto, cuánto pagaron y de qué presupuesto salió? (a quién: Dueño o gerente administrativo de una pyme uruguaya de comercio o servicios que haya hecho alguna mejora eléctrica o solar en los últimos 3 años; valida: Quién decide y paga del lado de la mipyme: supuesto sin ficha de que pagan por un ahorro estimado (informe de unos USD 15) y ataque de que el segmento de bajo consumo puede no pagar.)
4. ¿Cómo consiguieron sus últimos 5 clientes pyme? ¿Cuánto les costó conseguir cada uno, sumando publicidad, comisiones a terceros y visitas o presupuestos que no se cerraron? ¿Alguna vez pagaron a alguien por un contacto o una recomendación, y cuánto? (a quién: Dueño o responsable comercial de una empresa instaladora de paneles solares o de una consultora de eficiencia energética que trabaje con pymes en Uruguay; valida: Quién decide y paga el ingreso principal: ataque en pie de ronda 2 de que el cobro de unos USD 20 por contacto calificado a consultores e instaladores no tiene ficha ni validación.)
5. En las últimas visitas o consultas de pymes chicas, ¿cuánto tiempo les llevó juntar y leer las facturas de UTE para el diagnóstico inicial, cuántas de esas consultas terminaron en un trabajo pago y por qué se cayeron las demás? (a quién: Técnico o consultor en eficiencia energética que hace diagnósticos para mipymes en Uruguay, o instalador solar que prepara presupuestos a partir de facturas; valida: Costo hoy del diagnóstico para el segundo cliente y tasa de conversión del segmento chico: ataques de que el ahorro es chico, se corrige una vez y el segmento puede no pagar.)

### Guion de entrevista

[shortlist/guiones/i021.md](shortlist/guiones/i021.md)

### Profundizar

`python3 skills/idea-arena/idea_arena.py deepen i021`

## El embudo

- Fichas: 85 aceptadas (82 ok, 3 bloqueadas), 6 descartadas.
- Ideas: 29 recibidas, 29 pasan el filtro duro, 29 pasan el alcance.
- Torneo: 16 ideas, 4 ronda(s).
- Detalle del filtro: [filter/reporte.md](filter/reporte.md).
