# Encargo para Claude Desktop — propagar la corrección de métricas a Word y PDF

**Fecha:** 2026-09-07 · **De:** Claude Code (equipo principal)

## Qué se corrigió y por qué importa

El informe describía el emparejamiento entre la entidad extraída y la de referencia como **«similitud de
tokens»**. Es incorrecto, y afecta a cómo un lector técnico interpreta todos los resultados.

Verificado contra `repos/ner-llm-entity-benchmark/src/evaluator.py` y comprobado empíricamente: el evaluador usa
`rapidfuzz.fuzz.ratio`, que coincide **exactamente** con `Indel.normalized_similarity × 100`. La distancia de
Indel es una variante de Levenshtein que **solo admite inserciones y supresiones**, sin sustituciones, y se
normaliza como `100 × (1 − d / (|a| + |b|))`. Opera sobre **caracteres, no sobre tokens**, y ambas cadenas se
pasan a minúsculas antes de comparar.

La diferencia no es terminológica. Si fuera por tokens, «Juan Pérez» y «Pérez Juan» darían 100 y casarían; con
`ratio` dan **50** y no casan. Y «Banco Santander» frente a «Santander» da **75**, por debajo del umbral de 85,
así que una extracción parcialmente correcta cuenta como error completo. Ambos efectos empujan las cifras **a la
baja**, nunca al alza: el desempeño reportado es conservador, y eso ahora se dice explícitamente en el texto.

Las secciones afectadas son **§3.3** (módulo de evaluación), donde está la descripción completa con la fórmula y
los dos límites de la métrica, y **§4.4** (métricas), con la mención breve. Puede que haya más correcciones de
la misma clase en camino: hay una auditoría en curso que contrasta contra el código todos los enunciados sobre
umbrales, parámetros del controlador AIMD, similitud coseno del módulo RAG, tamaños de modelo y cifras
estadísticas. Si aparecen, te las envío antes de que propagues.

## Qué hay que hacer

Propagar los cambios del Markdown canónico a **los tres `.docx` y al PDF**, y congelar una versión nueva. El
PDF es ahora parte de la entrega, así que la verificación debe hacerse **sobre el PDF**, que es donde se ve la
paginación real.

**Mantén las 25 páginas.** La `_v7` las cumple, y la corrección de §3.3 añade unas ocho líneas. Si el documento
se desborda, compacta a nivel de **estilo** —espaciados, interlineado—, como ya hiciste con acierto en la `_v5`,
y **no recortes texto**. Si aun así no cabe, avísame antes de suprimir nada: los anexos no computan para el
límite y disponen de sus propias 25 páginas, de modo que casi siempre hay sitio donde mover en lugar de quitar.

## Lo que no cambia

Sin pandoc. Corregir **siempre primero el `.md`**. Nada de arte ASCII: esquemas como tabla de Word y gráficos
como imagen real. **Anexo G y Anexo H íntegros.** Nueve capítulos y ocho anexos de la A a la H. Citas IEEE sin
crear ni eliminar entradas. Resumen de 200 palabras como máximo e introducción de 3 páginas como máximo.

## Al terminar

Declara el resultado en `CURRENT-TASKS.md` §2 con el **conteo de páginas medido sobre el PDF**, congela la
versión en `doc/versions/informe_final/` registrando en `VERSIONES.md` los SHA-256 **del `.docx` y del `.pdf`**,
y deja las copias de ambos en la raíz del proyecto.

---

## Nota de atribución

Mi commit `bdb3337` arrastró, por un `git add -A` demasiado amplio, tus versiones **`_v6` y `_v7`** —las
primeras que incluyen PDF— bajo un mensaje que solo hablaba de la corrección de la métrica. No se perdió nada,
pero el historial atribuye mal ese trabajo. Queda constancia aquí y en el registro de `CURRENT-TASKS`.

---

## Instrucciones permanentes para Word y PDF

Estas reglas quedan registradas también en `CLAUDE.md` y rigen para toda propagación futura, no solo para esta.

**Resumen y abstract.** Van **fundidos, sincronizados y en la página inicial**, tanto del `.docx` como del PDF.
Deben decir exactamente lo mismo en ambos idiomas y no pasar de **200 palabras** cada uno. El espacio entre el
título y su párrafo se reduce **a nivel de estilo** —el espaciado `before` del estilo `abstract`—, nunca
eliminando líneas del texto. Si una corrección de fondo entra en uno, entra en el otro en la misma pasada.

**Fuentes originales.** Cada bloque debe llevar el estilo que le corresponde de la plantilla: `abstract` para
resumen y abstract —no `p1a`, que trae otro cuerpo y otras sangrías—, `heading1` a `heading4` para los títulos,
`p1a` solo para el primer párrafo tras un título, `Normal` para el resto, `table caption` para las leyendas y
`programcode` para el código. Si al reconstruir un bloque pierde su estilo, restitúyelo antes de congelar.

**Espacios en blanco y paginación.** El objetivo son **25 páginas exactas**. Se alcanza recortando **por
estilo**: espaciados de `Heading 1`, `Heading 2`, `Heading 3`, `abstract` y `table caption`, interlineado, y
cuerpo de letra de los bloques de código, que pueden bajar a 7 pt. **No se suprime texto para ganar espacio**
sin autorización expresa. Los anexos no computan para el límite de 25 páginas del cuerpo.

**Anexo B.** Los *prompts* no deben arrastrar saltos de línea duros del formato de ancho fijo: en Word parten
las frases a media palabra. Cada campo va en una sola línea y con cuerpo de letra reducido, y la corrección se
hace **primero en el `.md`** para que la siguiente reconstrucción no la deshaga.

**Anexos.** Se recortan sus espacios en blanco y se consolidan párrafos, **sin sacrificar contenido**: son el
material que permite replicar el trabajo, que es justo lo que el profesor guía pide conservar.

**PDF.** Es parte de la entrega. La verificación de paginación se hace **sobre el PDF**, no sobre el `.docx`, y
en `VERSIONES.md` se registran los SHA-256 de ambos.

**Los cuatro reparos del profesor guía siguen vigentes** en cada propagación: sin bloques en blanco ni saltos
de página al empezar capítulo, sin ficha del estudiante, con desarrollo suficiente en cada sección y con un
marco conceptual que compara alternativas antes de que el capítulo 3 elija entre ellas. Ninguna compactación
puede deshacerlos.

**Sobriedad tipográfica.** En el cuerpo de las descripciones, el guion largo y la negrita quedan reservados
para lo excepcional. Los incisos se marcan con comas o paréntesis, no con guiones largos, y la negrita se
limita a los términos que se definen por primera vez y a las cifras que la tabla no recoge; nunca a frases
enteras ni a la conclusión de un párrafo. Una negrita por párrafo no destaca nada y delata redacción asistida.
El Markdown ya viene depurado —el cuerpo pasó de 113 guiones largos y 164 negritas a 19 y 108, sin perder una
palabra—, así que al reconstruir **no reintroduzcas resaltes**: si un bloque pierde su estilo y lo restituyes,
restituye el estilo, no el énfasis. Esta regla no alcanza a las tablas, donde la negrita sigue marcando el
mejor valor de cada columna, ni a los encabezados.
