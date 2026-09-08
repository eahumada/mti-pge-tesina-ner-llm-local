# No rehagáis `gemma4:31b-cloud` ni `gemma4:12b-mlx` en N=120: usan ya el corpus corregido

**Del equipo principal al equipo de 48 GB. 2026-09-08, urgente.**
Responde a vuestra entrada de `CURRENT-TASKS.md`:

> «Barrido detenido: los N=120 hechos (cloud, 12b-mlx, 31b-mlx parcial) usaban el corpus sin las 63
> embebidas y se rehacen.»

**Eso no es cierto para los dos que ya habéis commiteado.** Rehacerlos gastaría horas de máquina en repetir
un trabajo que está bien.

## La comprobación

El corpus corregido tiene **545** localizaciones en los 120 artículos, de las cuales **28** caen en los 7
artículos contaminados que se descuentan de la métrica. Quedan **517** en los 113 puntuados, y como cada
corrida evalúa dos modos, la matriz de confusión debe registrar **1 034** localizaciones de referencia.

Es exactamente lo que registran vuestras corridas, y no solo en localizaciones:

| Categoría | Esperado con el corpus corregido | Medido en `recorrida_20260908` |
|:---|---:|---:|
| Personas | 549 × 2 = **1 098** | **1 098** |
| Organizaciones | 750 × 2 = **1 500** | **1 500** |
| Localizaciones | 517 × 2 = **1 034** | **1 034** |

Las tres coinciden al entero. **Si el corpus no tuviera las 63 embebidas**, las localizaciones de referencia
serían **908** y no 1 034: la diferencia es inconfundible y no admite otra lectura.

Coincide además con vuestro propio mensaje de commit de `5b7ce84`, que dice «Re-corrida con corpus corregido
(63 locations embebidas aplicadas)», y con el orden de los hechos: `f49c03c` aplicó las localizaciones a las
16:41 y la primera entrega de datos es de las 16:57.

## Qué conservar y qué rehacer

- **`gemma4:31b-cloud` N=120: válida.** No la rehagáis. `82,13` baseline y `82,94` KB RAG sobre 113
  registros, verificada aquí con las cinco comprobaciones del protocolo.
- **`gemma4:12b-mlx` N=120: válida.** Tampoco. `77,67` y `79,96`.
- **`gemma4:31b-mlx` N=120 parcial: no la hemos podido comprobar**, porque no está commiteada. Si su corrida
  empezó **antes de las 16:41**, entonces sí usa el corpus viejo y hay que rehacerla. La comprobación es la
  misma: mirad si su matriz de confusión da 1 034 localizaciones de referencia o 908.
- Las de N=15 y N=30 no estaban afectadas, como bien decís.

## Cómo comprobarlo vosotros mismos, en cualquier corrida futura

Antes de dar una corrida por buena o por mala, abrid su `confusion_matrix.json` y sumad `TP + FN` de cada
categoría. Con el corpus corregido y los 7 contaminados descontados, cada corrida de N=120 en sus dos modos
debe dar **1 098 / 1 500 / 1 034**. Cualquier otra cosa indica un corpus distinto, y el número dice cuál.

Es más fiable que fiarse de la hora en que se lanzó, porque no depende de recordar cuándo se aplicó cada
cambio: el dato lo lleva el propio resultado.
