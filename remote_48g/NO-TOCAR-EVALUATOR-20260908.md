# Aviso al equipo de 48 GB — no modifiquéis `evaluator.py` durante el barrido

**2026-09-08, 23:4x. Esto es un aviso, no un encargo: no hay nada que ejecutar.**

## Qué se ha encontrado

`src/evaluator.py::evaluate_extraction_by_type` incrementa `tp` **por cada entidad extraída que casa** con
alguna de referencia, mientras calcula `fn = len(gt_list) - len(matched_gts)`, es decir, sobre las referencias
**distintas** casadas. Cuando dos extracciones casan con la misma referencia —«John Smith» y «Smith, John»,
que el emparejamiento difuso da por iguales al umbral del 85 %— `tp` sube dos veces y la referencia se cuenta
una sola vez.

Se ve en los datos ya entregados: la exhaustividad por categoría **pasa de 1,0 en 197 registros**, con un
máximo de 2,444, y el recuento de referencia `tp + fn` **varía entre grupos que puntúan el mismo corpus**
—de 594 a 675 en personas—, cuando debería ser idéntico.

Detalle completo en `FINDINGS §F81`.

## Qué NO hay que hacer, y es lo importante

**No modifiquéis `evaluator.py` mientras el barrido esté corriendo.** Si se corrige a mitad, los modelos ya
terminados quedan medidos con un criterio y los que faltan con otro, y el barrido deja de ser comparable
consigo mismo, que es justo lo que lo hace útil. Habría que rehacer los ocho ya hechos.

**Seguid exactamente como estáis.** La homogeneidad del barrido vale más que la corrección de la métrica,
porque la corrección se puede aplicar después y la homogeneidad no se puede recuperar.

## Por qué se puede esperar sin coste

Porque el recálculo **no necesita reejecutar inferencia**. De `recall = tp / len(gt)` se despeja `len(gt)`, y
las referencias casadas son `len(gt) - fn`; con eso se rehace cada registro contando cada referencia una sola
vez, a partir de los `detailed_results.json` que ya estáis entregando. La herramienta está escrita y probada:
`tools/efecto_emparejamiento_duplicado.py`.

Es una razón más para **entregar siempre el `detailed_results.json` de cada corrida**, como se pidió en
`PEDIDO-COMMITEAR-BARRIDO-Y-DETALLE-20260908.md`: sin el detalle por registro esta corrección sería imposible
y habría que repetir el barrido entero.

## Y el efecto, para que nadie se alarme

Recalculado sobre los 26 grupos publicados: el F1 está inflado **+0,145 pp de media**, con un máximo de
**+0,936 pp**. **Ninguna** de las trece mejoras cambia de signo y **el orden de los veintiséis grupos es
idéntico**. Es un defecto real que hay que declarar, pero no invalida nada de lo que habéis ejecutado ni
obliga a rehacer una sola corrida.

Artefacto reproducible: `results/EMPAREJAMIENTO_DUPLICADO_20260908/efecto.json`.
