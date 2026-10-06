# Candidatos para deduplicar

## i002: Cobros por transferencia confirmados al instante para microcomercios

- Usuario: Dueños de almacenes, kioscos y otros microcomercios del interior: usan y pagan la app.
- Problema: Con tarjeta, el comercio paga de 1,15% a 3,55% por transacción y un alquiler de POS de 465 a 1.500 pesos por mes más IVA; con MercadoPago, de 4,99% a 5,99% (F-fintech-seguros-005). Las transferencias instantáneas crecieron 50% en el segundo semestre de 2025 (F-fintech-seguros-002), pero el almacén que las acepta no confirma al instante la llegada del dinero ni cuadra su caja, que muchos llevan en cuadernos (F-comercio-retail-006). Hay unas 188...
- Solución: PWA para el celular del comercio. 1) Pedido de cobro con monto y código de referencia; el cliente paga por transferencia. 2) El comercio reenvía automáticamente los avisos por email de su banco; el sistema verifica la firma DKIM (contra avisos falsos), extrae monto y referencia (parsers por banco, LLM de respaldo) y avisa 'cobro confirmado' en segundos. 3) Cierre de caja diario por medio de cobro, con comisiones pagadas. 4) Sin aviso por email...

## i006: Asistente de cartera con IA para corredores de seguros independientes

- Usuario: Corredores de seguros independientes y escritorios de 1 a 5 personas, en especial del interior. Paga el corredor.
- Problema: Corredores y aseguradoras dedican horas manuales a emails, pólizas y contratos; la startup de origen uruguayo que lo automatiza con IA levantó US$ 1 millón, pero opera sobre todo en España, no en Uruguay (F-fintech-seguros-008). El mercado local crece: US$ 2.889 millones en primas en 2024, +25,8% real (F-fintech-seguros-001), y aseguradoras como SURA buscan llegar al interior (F-fintech-seguros-006). El corredor independiente trabaja con varia...
- Solución: Web para el corredor. 1) Carga o reenvío de pólizas y cotizaciones en PDF; un LLM las lleva a un esquema común por ramo (auto y hogar): vigencia, suma asegurada, deducibles, coberturas y prima, con revisión humana de campos dudosos. 2) Cartera con vencimientos y recordatorios de renovación. 3) Comparador de cotizaciones normalizado. 4) Respuestas sobre condiciones generales ('¿cubre granizo?') con RAG que cita la cláusula. 5) Resumen para el c...

## i007: Auditor de comisiones de cobro para pequeños comercios

- Usuario: Comercio minorista o gastronómico chico que cobra con POS, MercadoPago y transferencias. Paga el comercio o su estudio contable.
- Problema: Un comercio chico uruguayo paga por venta con tarjeta entre 1,15% (débito) y 3,55% (crédito), más $ 465 a $ 1.500 mensuales más IVA de alquiler de POS; con MercadoPago, 4,99% a 5,99% según el plazo de acreditación (F-fintech-seguros-005). Por ejemplo, $ 200.000 mensuales al 4,99% cuestan $ 9.980; en débito, $ 2.300 más el POS. Cada canal, incluidas las transferencias instantáneas en alza (F-fintech-seguros-002), liquida aparte y el comercio de...
- Solución: Web donde el comercio o su contador sube cada mes sus liquidaciones de cobro y estado de cuenta (PDF, CSV o planilla). Normaliza cobros y cargos, calcula el costo efectivo por canal (comisión, POS e IVA) verificando que las líneas sumen el total, marca cargos sobre la tarifa contratada y simula otro plan, plazo de acreditación o canal, con su efecto en costo y caja. Ante formatos nuevos, un LLM propone el mapeo de columnas y un lector determin...

## i010: Comparador de cotizaciones y renovaciones para corredores de seguros

- Usuario: Corredores independientes y corretajes de 1 a 10 personas en Uruguay, empezando por automóvil. Paga el corretaje.
- Problema: Corredores y aseguradoras dedican horas manuales a emails, pólizas y contratos al cotizar, renovar y gestionar siniestros; una startup fundada por uruguayos levantó US$ 1 millón para automatizarlo, pero opera sobre todo en España, no en Uruguay (F-fintech-seguros-008). El mercado uruguayo emitió unos US$ 2.889 millones en primas en 2024 (+25,8% real, F-fintech-seguros-001), y una aseguradora grande busca el interior y segmentos no alcanzados (...
- Solución: Web donde el corredor sube las cotizaciones (PDF o correo) de varias aseguradoras para un mismo riesgo. Extrae premio, deducibles y coberturas a un esquema común, enlaza cada dato con su fragmento de origen y arma una comparación en lenguaje simple para el cliente. Responde preguntas sobre condiciones generales citando la cláusula. Importa la cartera, avisa 30 días antes de cada vencimiento y precarga la comparación de renovación.
