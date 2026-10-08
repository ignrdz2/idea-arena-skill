# Calibración del juez

Run `20261007-2053`, semilla 9853.

## Resultado

- Acuerdo por pares con tu ranking: **2 de 3**.
- Tau de Kendall entre tu orden y el del juez: **0.333** (1 = mismo orden, -1 = invertido).
- Tu orden: idea_A > idea_B > idea_C. El del juez: idea_B > idea_A > idea_C.
- Pares en los que los dos órdenes de presentación dieron el mismo ganador: 3 de 3.
- La idea mostrada primero (X) ganó el 50% de las veces. Lejos del 50% indica sesgo de posición.

## Por par

| Tu preferida | La otra | El juez prefiere | Coincide | Órdenes coinciden | Criterios en contra de tu preferida |
| --- | --- | --- | --- | --- | --- |
| idea_A | idea_B | idea_B | no | sí | viabilidad -4, diferenciacion -2 |
| idea_A | idea_C | idea_A | sí | sí | - |
| idea_B | idea_C | idea_B | sí | sí | - |

## Puntaje medio por criterio

| Idea | demanda | viabilidad | diferenciacion | business_case | encaje | academico |
| --- | --- | --- | --- | --- | --- | --- |
| idea_A | 6.75 | 3 | 3.25 | 5 | 8.75 | 8.5 |
| idea_B | 4.5 | 6.25 | 5 | 5.25 | 6.75 | 8.25 |
| idea_C | 1 | 1 | 1.5 | 2.75 | 5 | 4 |

## Cómo usar esto

- Si el juez no coincide con vos, mirá la columna de criterios en contra: son los criterios en los que tu idea preferida puntuó menos. Si creés que ese criterio no debería pesar tanto, ajustá su peso (en rubric.md, constraints.md y CRITERIA en ia_tournament.py) o sus anclas en rubric.md.
- Si los dos órdenes no coinciden seguido, o X gana mucho más del 50%, activá tournament.judge_both_orders en config.json.
- Con 3 ideas la señal es gruesa: un desacuerdo puede ser ruido. Agregá ideas en calibration/ideas/ si querés más señal.
- Corré la calibración de nuevo después de cada ajuste.
