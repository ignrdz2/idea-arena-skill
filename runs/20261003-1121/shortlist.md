# Shortlist de ideas de tesis

Run `20261003-1121`, modo piloto, semilla 7, creado 2026-10-03T11:21:12. Generado por /idea-arena.

Cómo leer esto:
- El puesto 1 ganó todos sus cruces y el 2 perdió solo la final. Más abajo, el orden de una eliminación simple es ruidoso: dos ideas eliminadas en la misma ronda se ordenan por el puntaje que sacaron al perder, contra rivales distintos.
- Cada idea es la última versión revisada que tuvo en el torneo.
- Nada de esto reemplaza hablar con el mercado: para eso están las preguntas y el guion de cada idea.
- Una idea que perdió su último cruce con un fallo fatal verificado (viola una restricción dura o se apoya en una afirmación sin evidencia) no se recomienda. Fuera por eso: ninguna.

## Resumen

| # | Idea | Resultado en el torneo | Costo USD/año | Fichas citadas (ok / bloqueadas) |
| --- | --- | --- | --- | --- |
| 1 | Auditor de comisiones de cobro para pequeños comercios (i007) | campeona | 111.08 | 5 / 0 |
| 2 | Lector de coberturas de cotizaciones y renovaciones para corredores de seguros (i010) | eliminada en la ronda 2 por Auditor de comisiones de cobro para p... | 161.08 | 4 / 0 |
| 3 | Cobros por transferencia confirmados al instante para microcomercios (i002) | eliminada en la ronda 1 por Lector de coberturas de cotizaciones... | 113.08 | 6 / 0 |

## 1. Auditor de comisiones de cobro para pequeños comercios (i007)

Página completa: [tournament/r2/r2-m01.i007.solution.md](tournament/r2/r2-m01.i007.solution.md). Resultado: campeona.

**Problema.** Un comercio chico uruguayo paga por venta con tarjeta entre 1,15% (débito) y 3,55% (crédito), más $ 465 a $ 1.500 mensuales más IVA de POS; con MercadoPago, 4,99% a 5,99% según el plazo de acreditación (F-fintech-seguros-005, nota de 2022). Con $ 200.000 mensuales, un punto de plazo son $ 2.000 al mes. Las transferencias instantáneas crecen (F-fintech-seguros-002). Hay unas 188.000 microempresas (F-comercio-retail-002); cuántas cobran con POS o MercadoPago no se sabe: es un techo.

**Usuario.** Comercio minorista o gastronómico chico que cobra con POS y MercadoPago. Paga el comercio o, a validar, su estudio contable.

**Solución.** Web donde el comercio o su contador sube cada mes sus liquidaciones y carga una vez su tarifa contratada. Calcula el costo efectivo por canal (comisión, POS e IVA) verificando que las líneas sumen el total, marca cargos sobre la tarifa y simula otro plazo de acreditación o plan, con su efecto en costo y caja. Un LLM propone el mapeo de formatos nuevos y un lector determinístico lo aplica.

**Costo de infraestructura.** USD 111.08 por año (tope USD 300).

### Rastro de veredictos

| Ronda | Rival | Persona | Puntaje | Resultado | Motivo del juez |
| --- | --- | --- | --- | --- | --- |
| 1 | (bye) | - | - | pasa sin cruce | - |
| 2 | Lector de coberturas de cotizaciones y renovaciones para corredores de seguros (i010) | Competidor | 58 a 53 | ganó | Con demanda igual de débil en las dos, Y compite en Uruguay contra Nexura y Softseguros, que ya cotizan, comparan en PDF y leen pólizas, y admite no tener barrera propia, mientras X no tiene en las fichas un competidor que audite comisiones de forma neutral y además cuesta menos y tiene un plan B de datos más realista. |

Ataques que quedaron en pie:

- ronda 2: Disposición a pagar $ 390 por mes sin ninguna señal en las fichas
- ronda 2: El comparador es aritmética copiable por un software contable o de facturación; la neutralidad no es barrera técnica
- ronda 2: El ahorro por plazo, plan y cargos de más puede ser menor al precio y no hay ninguna cifra real de ahorro

### Preguntas para validar con el mercado

1. Pensando en el último mes cerrado, ¿cuánto pagaron en total por cobrar con tarjeta y con MercadoPago, sumando comisiones, alquiler del POS e IVA? ¿Cómo llegan a ese número: lo tienen calculado o lo están estimando ahora? (a quién: Dueño o encargado de administración de un comercio minorista o gastronómico chico de Montevideo que cobra con POS y MercadoPago; valida: Cuánto cuesta hoy el problema y el supuesto de que los comercios no calculan su costo por canal; da la base para ver si el ahorro posible supera el precio (ataque de ronda 2: el ahorro puede ser menor al precio y no hay cifra real).)
2. ¿Cuándo fue la última vez que revisaron una liquidación del POS o de MercadoPago contra la tarifa contratada, o que cambiaron de plazo de acreditación o de plan? ¿Qué los llevó a hacerlo, quién lo hizo, cuánto tiempo les llevó y qué diferencia en plata encontraron? (a quién: Dueño o encargado de administración de un comercio minorista o gastronómico chico de Montevideo que cobra con POS y MercadoPago; valida: Supuesto de que el ahorro sale de plazo, plan y cargos de más, y ataque de ronda 2 de que ese ahorro puede ser menor al precio: busca casos reales con cifra.)
3. La última vez que contrataron un servicio mensual para administrar el negocio (por ejemplo facturación electrónica, software de gestión o el estudio contable), ¿quién decidió contratarlo, quién lo paga y cuánto pagan hoy por mes? ¿Dieron de baja alguno por precio en el último año? (a quién: Dueño de un comercio minorista o gastronómico chico de Montevideo que cobra con POS y MercadoPago; valida: Quién decide y paga (el comercio o su estudio contable) y el ataque de ronda 2 de disposición a pagar $ 390 por mes sin señal: da un precio de referencia con lo que ya pagan.)
4. De los comercios chicos que llevan, ¿cuántos les entregaron el mes pasado las liquidaciones del POS o de MercadoPago, y en qué formato (PDF, planilla, acceso al portal)? ¿Qué hicieron con ellas, cuántas horas les llevó y ese trabajo se lo cobran al cliente aparte o va dentro del abono? (a quién: Contador socio de un estudio contable de Montevideo que lleva la contabilidad de comercios minoristas o gastronómicos chicos; valida: Canal de estudios contables a validar (quién paga), supuesto de que los comercios comparten sus liquidaciones y formatos reales para los lectores del semestre 1; si ya cobran por ese trabajo, es una señal de pago.)
5. La última vez que quisieron saber cuánto les costó cobrar con cada medio (débito, crédito, MercadoPago, transferencia), ¿cómo lo resolvieron? ¿Usaron una planilla, al contador, el software de facturación o gestión, o le preguntaron al proveedor del POS, y les dio el número? Si nunca lo hicieron, ¿por qué? (a quién: Dueño o encargado de administración de un comercio minorista o gastronómico chico de Montevideo que usa un software de facturación o gestión; valida: Ataque de ronda 2 de que el cálculo es copiable por un software contable o de facturación: muestra si las herramientas que ya usan lo resuelven y si el hueco es real. También el supuesto de que no calculan el costo por canal.)

### Guion de entrevista

[shortlist/guiones/i007.md](shortlist/guiones/i007.md)

### Profundizar

`python skills/idea-arena/idea_arena.py deepen i007`

## 2. Lector de coberturas de cotizaciones y renovaciones para corredores de seguros (i010)

Página completa: [tournament/r2/r2-m01.i010.solution.md](tournament/r2/r2-m01.i010.solution.md). Resultado: eliminada en la ronda 2 por Auditor de comisiones de cobro para p....

**Problema.** Ya hay software para corredores en Uruguay con multicotizador, avisos de renovación y OCR de pólizas, desde USD 49 por mes (F-ataque-r2-m01-i010-competidor-001), y Softseguros declara más de 900 agencias en LATAM (F-ataque-r2-m01-i010-competidor-002). Nexura describe su OCR para pólizas emitidas, no para cotizaciones recibidas. Que comparar coberturas y cambios de renovación a mano sea un dolor es una hipótesis sin ficha local, a validar con entrevistas.

**Usuario.** Corredores independientes y corretajes de 1 a 10 personas en Uruguay, empezando por automóvil. Paga el dueño del corretaje. Complemento de la herramienta que ya use.

**Solución.** Web donde el corredor sube cotizaciones de automóvil recibidas (PDF o correo) de varias aseguradoras. Extrae premio, deducibles, coberturas y exclusiones a un esquema común, marca campos de baja confianza, enlaza cada dato con su origen y compara coberturas en un PDF para el cliente. En renovación, lista qué cambió contra la póliza vigente. Consulta cláusulas con cita.

**Costo de infraestructura.** USD 161.08 por año (tope USD 300).

### Rastro de veredictos

| Ronda | Rival | Persona | Puntaje | Resultado | Motivo del juez |
| --- | --- | --- | --- | --- | --- |
| 1 | Cobros por transferencia confirmados al instante para microcomercios (i002) | Cliente real de una empresa uruguaya | 59 a 43.5 | ganó | X construye su MVP sin dependencias externas críticas (set propio y sintético, costo de USD 161) y su dolor tiene al menos evidencia directa aunque extranjera (Foliume, F-fintech-seguros-008), mientras que el valor central de Y depende de que los bancos avisen por email con DKIM, algo no probado, y su dolor no tiene ficha frente a un sustituto gratuito que la propia idea reconoce (la notificación |
| 2 | Auditor de comisiones de cobro para pequeños comercios (i007) | Competidor | 53 a 58 | perdió | Con demanda igual de débil en las dos, Y compite en Uruguay contra Nexura y Softseguros, que ya cotizan, comparan en PDF y leen pólizas, y admite no tener barrera propia, mientras X no tiene en las fichas un competidor que audite comisiones de forma neutral y además cuesta menos y tiene un plan B de datos más realista. |

Ataques que quedaron en pie:

- ronda 1: El dolor del corredor uruguayo sigue sin ficha local: solo hay evidencia extranjera (Foliume en España) y el resto es hipótesis
- ronda 1: Diferenciación débil: Foliume, de fundadores uruguayos y con US$ 1 millón, cierra el hueco si entra, y las 21 insurtech locales siguen sin relevar
- ronda 1: Precio, cantidad de corretajes y horas ahorradas sin medir: el business case depende de lo que mida el piloto, frente a una alternativa de costo cero
- ronda 2: Diferencia sin barrera: Nexura o Foliume pueden agregar lectura de cotizaciones y comparación de cláusulas
- ronda 2: No resuelve obtener las cotizaciones, y los multicotizadores existentes ya comparan en un PDF
- ronda 2: Demanda local sin ficha: el dolor solo se apoya en una empresa que opera en España

### Preguntas para validar con el mercado

1. La última vez que cotizaste un seguro de automóvil con más de una aseguradora, ¿por qué vía te llegó cada cotización (portal, multicotizador, PDF por correo, WhatsApp u otra) y qué hiciste con ellas, paso a paso, hasta mandarle algo al cliente? (a quién: Corredor de seguros independiente en Uruguay que vende seguros de automóvil con varias aseguradoras; valida: Supuesto: los corredores reciben cotizaciones en PDF o correo y las comparan a mano. Ataque en pie (ronda 2): no resuelve obtener las cotizaciones y los multicotizadores existentes ya comparan en un PDF.)
2. En el último mes, ¿cuántas comparaciones de seguro de automóvil entre aseguradoras armaron en el corretaje, quién las hizo y cuánto tiempo llevó la más reciente desde que llegaron las cotizaciones hasta que el cliente recibió la comparación? (a quién: Dueño de un corretaje de seguros de 1 a 10 personas en Montevideo con cartera de automóvil; valida: Cuánto cuesta hoy el problema: horas y volumen de comparaciones, hoy hipótesis sin dato local. Ataque en pie (ronda 1): horas ahorradas sin medir frente a una alternativa de costo cero.)
3. ¿Cuándo fue la última vez que un cliente tuvo un siniestro o un reclamo en el que una cobertura, un deducible o una exclusión no era lo que había entendido al contratar? ¿Qué pasó, cómo se detectó y qué le costó al corretaje (tiempo, devoluciones, pérdida del cliente)? (a quién: Corredor de seguros independiente o dueño de un corretaje pequeño en Uruguay con al menos un año de cartera de automóvil; valida: Ataque en pie (rondas 1 y 2): el dolor del corredor uruguayo no tiene ficha local. Supuesto: comparar coberturas y exclusiones a mano produce errores con un costo real para el corretaje.)
4. En la última renovación de una póliza de automóvil que gestionaste, ¿cómo supiste qué había cambiado frente a la póliza vigente (premio, deducible, coberturas, exclusiones), cuánto tiempo te llevó revisarlo y cómo se lo comunicaste al cliente? (a quién: Empleado administrativo o corredor de un corretaje de seguros pequeño en Uruguay que gestiona renovaciones de automóvil; valida: Supuesto: revisar a mano los cambios de una renovación contra la póliza vigente es un dolor. Riesgo declarado: si las aseguradoras abren portal o API, el valor que queda es comparar cláusulas y renovaciones.)
5. ¿Qué software pagan hoy en el corretaje para cotizar, gestionar pólizas o avisar vencimientos, quién decidió contratarlo, cuánto pagan por mes y qué pasó la última vez que evaluaron, contrataron o dieron de baja una herramienta de ese tipo? (a quién: Dueño de un corretaje de seguros de 1 a 10 personas en Uruguay que decide las compras de software; valida: Quién decide y paga, y cuánto: precio hipotético de USD 25 por mes frente a Nexura desde USD 49. Ataque en pie (rondas 1 y 2): diferenciación sin barrera frente a herramientas ya instaladas como Nexura o Softseguros.)

### Guion de entrevista

[shortlist/guiones/i010.md](shortlist/guiones/i010.md)

### Profundizar

`python skills/idea-arena/idea_arena.py deepen i010`

## 3. Cobros por transferencia confirmados al instante para microcomercios (i002)

Página completa: [tournament/r1/r1-m01.i002.solution.md](tournament/r1/r1-m01.i002.solution.md). Resultado: eliminada en la ronda 1 por Lector de coberturas de cotizaciones....

**Problema.** Con tarjeta, el comercio paga de 1,15% a 3,55% por transacción y un alquiler de POS de 465 a 1.500 pesos por mes más IVA; con MercadoPago, de 4,99% a 5,99% (F-fintech-seguros-005, de 2022). Las transferencias instantáneas crecieron 50% en el segundo semestre de 2025 a escala nacional (F-fintech-seguros-002), y fuera de Montevideo persiste el efectivo y los comercios chicos necesitan incentivos para adoptar pagos digitales (F-fintech-seguros-003). La ficha sobre pequeños comercios solo documenta cuadernos y comprobantes perdidos (F-comercio-retail-006, marketing de un competidor): que confirmar una transferencia y cuadrar la caja sea un dolor pagable es una hipótesis que las entrevistas de las primeras semanas deben validar o descartar.

**Usuario.** Dueños de almacenes, kioscos y otros microcomercios del interior que ya reciben transferencias y llevan la caja a mano: usan y pagan la app.

**Solución.** PWA para el celular del comercio. 1) Pedido de cobro con monto y código de referencia (opcional: sin código se casa por monto y hora). 2) El comercio activa una sola vez el reenvío de los avisos de su banco a una casilla propia; el sistema verifica DKIM, extrae monto y referencia (parsers por banco, LLM de respaldo) y avisa 'cobro confirmado' en segundos. 3) Cierre de caja diario por medio de cobro. 4) Sin aviso por email, concilia con el extracto CSV. El producto sigue siendo útil por 3 y 4 si el aviso en tiempo real no es viable en algún banco.

**Costo de infraestructura.** USD 113.08 por año (tope USD 300).

### Rastro de veredictos

| Ronda | Rival | Persona | Puntaje | Resultado | Motivo del juez |
| --- | --- | --- | --- | --- | --- |
| 1 | Lector de coberturas de cotizaciones y renovaciones para corredores de seguros (i010) | Cliente real de una empresa uruguaya | 43.5 a 59 | perdió | X construye su MVP sin dependencias externas críticas (set propio y sintético, costo de USD 161) y su dolor tiene al menos evidencia directa aunque extranjera (Foliume, F-fintech-seguros-008), mientras que el valor central de Y depende de que los bancos avisen por email con DKIM, algo no probado, y su dolor no tiene ficha frente a un sustituto gratuito que la propia idea reconoce (la notificación |

Ataques que quedaron en pie:

- ronda 1: El dolor de confirmar transferencias y cuadrar la caja no tiene ficha, y la app del banco ya notifica gratis
- ronda 1: Pedir al microcomercio que reenvíe avisos bancarios a un tercero sigue sin validar, en un segmento que según F-fintech-seguros-003 necesita incentivos para adoptar lo digital
- ronda 1: La base técnica (avisos por email con DKIM de los bancos) no está verificada y el plan B, conciliación por extracto, pierde la inmediatez que da nombre al producto
- ronda 1: Diferenciación débil: los competidores citados no atacan el problema, el sustituto es la notificación bancaria gratuita y bancos o pagos interoperables pueden copiarlo

### Preguntas para validar con el mercado

1. La última vez que el cierre de caja no les dio (faltó o sobró plata), ¿cuánta era la diferencia, quién la buscó y cuánto tiempo les llevó encontrarla? ¿Tenía que ver con transferencias, con efectivo o con otro medio de pago? ¿Cuántas veces les pasó en el último mes? (a quién: dueño o encargado de caja de un almacén o kiosco del interior de Uruguay que ya recibe transferencias de clientes; valida: Cuánto cuesta hoy el problema: el supuesto de que cuadrar la caja con transferencias es un dolor frecuente y con costo en tiempo o dinero, y el ataque que quedó en pie de que ese dolor no tiene ninguna ficha que lo respalde.)
2. La última vez que un cliente les pagó por transferencia en el mostrador, ¿cómo comprobaron que la plata había entrado antes de entregarle la mercadería: quién lo miró, en qué celular o equipo y cuánto tardó? ¿Recuerdan alguna vez que la transferencia no llegó o el comprobante era falso? ¿Qué pasó? (a quién: persona que atiende el mostrador (dueño o empleado) de un almacén o kiosco del interior de Uruguay que recibe transferencias; valida: El ataque de que la app del banco ya notifica gratis y la diferenciación es débil: si la forma actual de confirmar alcanza o genera demoras, dependencia del celular personal del dueño o pérdidas por transferencias que no llegaron.)
3. ¿En qué banco o bancos reciben las transferencias del negocio y cómo se enteran hoy de que entró una (email, SMS, notificación de la app, mirando el saldo)? En el último aviso que recibieron, ¿por qué medio llegó y cuánto tardó desde que el cliente transfirió? (a quién: dueño de un almacén, kiosco u otro microcomercio del interior de Uruguay que recibe transferencias de clientes; valida: El supuesto de que al menos 2 o 3 bancos avisan por email y con poca demora, y el ataque de que esa base técnica no está verificada (la firma DKIM se comprueba aparte, con cuentas del equipo).)
4. ¿Hoy alguien fuera del negocio (contador, socio, familiar, empleado o algún sistema) recibe o ve los movimientos o avisos de la cuenta bancaria del comercio? ¿Cómo se le dio ese acceso (extracto, clave, reenvío, capturas)? La última vez que alguien les pidió ver esos datos, ¿qué decidieron y por qué? (a quién: dueño de un almacén o kiosco del interior de Uruguay que maneja la cuenta bancaria del negocio; valida: El ataque que quedó en pie de que pedir al microcomercio que comparta sus avisos bancarios con un tercero no está validado, en un segmento que según F-fintech-seguros-003 necesita incentivos para adoptar lo digital.)
5. ¿Qué fue lo último que contrataron para el negocio con pago mensual (facturación, POS, contador u otro servicio)? ¿Quién decidió contratarlo, quién lo paga y de qué plata sale, cuánto pagan por mes y cómo se enteraron de que existía? ¿Dieron de baja alguno en el último año, y por qué? (a quién: dueño de un almacén, kiosco u otro microcomercio del interior de Uruguay; valida: Quién decide y paga: el supuesto de que decide el dueño y paga de su presupuesto operativo, la referencia de gasto mensual frente al precio hipotético de 350 pesos más IVA, y el canal de venta, hoy sin contactos.)

### Guion de entrevista

[shortlist/guiones/i002.md](shortlist/guiones/i002.md)

### Profundizar

`python skills/idea-arena/idea_arena.py deepen i002`

## El embudo

- Fichas: 28 aceptadas (28 ok, 0 bloqueadas), 0 descartadas.
- Ideas: 10 recibidas, 4 pasan el filtro duro, 4 pasan el alcance.
- Torneo: 3 ideas, 2 ronda(s).
- Detalle del filtro: [filter/reporte.md](filter/reporte.md).
