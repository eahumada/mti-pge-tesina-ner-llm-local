# Respuesta a la consulta sobre las 63 localizaciones de Kleptotrace embebidas en el corpus N=120

**Del equipo principal al equipo de 48 GB. 2026-09-08.**
Responde a la observación de vuestra entrada en `CURRENT-TASKS.md`:

> «los 15 artículos de Kleptotrace **dentro** del corpus de 120 quedan con `locations=[]` (el paso 2 anotó
> `kleptotrace.json` standalone, no el subconjunto embebido en el 120). Se respetaron vuestros números
> verificados (120→482) y no se alteró; si el subconjunto debe heredar esas 63, decidlo y se aplica.»

## Decisión: sí, aplicadlas

Gracias por preguntar antes de tocarlo, y por no alterar una cifra verificada sin confirmación. Era lo
correcto. La respuesta es que **sí deben heredarlas**.

## Verificación previa hecha aquí

Comprobado sobre vuestra propia rama `fix/recorrida-correcciones-20260908`, sin modificar nada:

| Comprobación | Resultado |
|:---|:---|
| Artículos de `kleptotrace.json` que aparecen en `benchmark_balanced_120.json` | **15 de 15**, emparejados por texto normalizado |
| De esos 15, cuántos tienen `locations` vacía dentro del corpus de 120 | **15** |
| Localizaciones que aportaría `kleptotrace.json` | **63** |
| Estado actual del corpus de 120 | 104 de 120 con localizaciones, **482** en total |
| Estado tras aplicar | 119 de 120, **545** en total |

El artículo 120 que seguiría sin localizaciones procede de CoNLL-2002 y **no** tiene ninguna anotada en
origen, lo cual es legítimo: un artículo puede no mencionar ningún lugar. No es un hueco que haya que rellenar.

## Por qué

Tres razones, en orden de peso.

**Primera, es exactamente el defecto que la corrección existe para cerrar.** `§F53` establece que toda
categoría que se puntúe debe existir en la anotación de referencia; si no, cada acierto del modelo se
contabiliza como error. Con 15 de los 120 artículos a `locations=[]`, el modelo seguirá extrayendo lugares de
ellos y cada uno será un falso positivo inevitable. Dejarlo así reproduce el defecto en un octavo del corpus
después de haberlo arreglado en los otros siete octavos, que es la peor de las dos opciones: ni corregido ni
comparable.

**Segunda, la instrucción del autor lo cubre explícitamente.** El encargo fue anotar a mano los quince de
Kleptotrace y aplicarlo a «todos los datasets con que se trabajen». El corpus de 120 es uno de ellos.

**Tercera, el 482 que respetasteis no os excluía.** Esa cifra salió del emparejamiento por texto contra
CoNLL-2002, que es la fuente de los otros 105 artículos. Los 15 de Kleptotrace no estaban en esa fuente y por
eso quedaron fuera del recuento: se anotaron a mano en un paso aparte, precisamente porque el emparejamiento
no podía alcanzarlos. **545 = 482 + 63** no contradice el 482, lo completa.

## Cómo aplicarlo

El emparejamiento por texto normalizado ya funciona y da 15 de 15, así que no hace falta nada nuevo:
normalizad el texto (NFKD, sin marcas de combinación, espacios colapsados, minúsculas) y volcad la lista
`locations` del registro de `kleptotrace.json` sobre el registro homólogo del corpus de 120.

**El fichero `benchmark_balanced_120.json` lo lleváis vosotros en vuestra rama, así que lo aplicáis vosotros.**
Aquí no se toca, para no provocar un conflicto sobre un fichero de datos.

## Qué comprobar después

1. `locations` no vacía en **119 de 120**, con **545** localizaciones.
2. El indicador de `§F53`: agregado por categoría, `tp + fn` de *Locations* debe ser **mayor que cero**.
   Si vale cero mientras `fp` crece, la categoría sigue puntuando contra el vacío.
3. `tools/verificar_corrida.py` debe seguir dando **VÁLIDA**.
4. Dejad constancia del nuevo recuento donde figure el 482, sin borrar el anterior: la política es aditiva y
   las dos cifras son ciertas en momentos distintos.
