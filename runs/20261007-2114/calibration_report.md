# Calibración del juez

Run `20261007-2114`, semilla 741514.

## Resultado

- Acuerdo por pares con tu ranking: **3 de 3**.
- Tau de Kendall entre tu orden y el del juez: **1.0** (1 = mismo orden, -1 = invertido).
- Tu orden: idea_A > idea_B > idea_C. El del juez: idea_A > idea_B > idea_C.
- Pares en los que los dos órdenes de presentación dieron el mismo ganador: 3 de 3.
- La idea mostrada primero (X) ganó el 50% de las veces. Lejos del 50% indica sesgo de posición.

## Por par

| Tu preferida | La otra | El juez prefiere | Coincide | Órdenes coinciden | Criterios en contra de tu preferida |
| --- | --- | --- | --- | --- | --- |
| idea_A | idea_B | idea_A | sí | sí | diferenciacion -1.5, viabilidad -1 |
| idea_A | idea_C | idea_A | sí | sí | - |
| idea_B | idea_C | idea_B | sí | sí | - |

## Puntaje medio por criterio

| Idea | demanda | viabilidad | diferenciacion | business_case | encaje | academico |
| --- | --- | --- | --- | --- | --- | --- |
| idea_A | 7 | 5.5 | 4.25 | 5.5 | 8.5 | 8 |
| idea_B | 4 | 6 | 5.25 | 5.25 | 6.75 | 8.25 |
| idea_C | 1 | 1 | 1 | 2.75 | 4.75 | 3.75 |

## Cómo usar esto

- Si el juez no coincide con vos, mirá la columna de criterios en contra: son los criterios en los que tu idea preferida puntuó menos. Si creés que ese criterio no debería pesar tanto, ajustá su peso (en rubric.md, constraints.md y CRITERIA en ia_tournament.py) o sus anclas en rubric.md.
- Si los dos órdenes no coinciden seguido, o X gana mucho más del 50%, activá tournament.judge_both_orders en config.json.
- Con 3 ideas la señal es gruesa: un desacuerdo puede ser ruido. Agregá ideas en calibration/ideas/ si querés más señal.
- Corré la calibración de nuevo después de cada ajuste.
