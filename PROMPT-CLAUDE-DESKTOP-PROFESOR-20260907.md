# Encargo para Claude Desktop — revisión del profesor guía y datos nuevos

*Actualizado el 2026-09-07 a las 16:45. Sustituye a la versión anterior de este mismo archivo.*

El profesor guía devolvió el informe con cuatro reparos: demasiados bloques en blanco y saltos de página entre
capítulos, la ficha del estudiante en la primera hoja, poco desarrollo general —«muchas secciones no son más
que un título y un breve párrafo»— y un marco conceptual pobre que no compara alternativas antes de elegir
una. Los cuatro están atendidos en el Markdown canónico,
[`doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md`](./doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md).
El respaldo previo está junto a él con sufijo `.bak_profesor_20260907`. Respecto de tu propagación anterior, el
Markdown acumula **+212 / −165 líneas**.

## Lo que cambió, y por qué conviene separarlo en dos tandas

Hay dos clases de cambio y no tienen la misma urgencia ni la misma estabilidad.

**Los cambios estructurales ya están firmes** y puedes propagarlos con confianza. Quité la ficha del estudiante
y la sustituí por la cabecera que prescribe `plantilla_final-2026.docx` —título, autor, dirección institucional
y correo—; eliminé los doce separadores que el `.docx` renderizaba como bloques en blanco; reduje el resumen de
270 a 201 palabras, porque la plantilla fija un máximo de 200, y lo reescribí en el orden prescrito. Reescribí
el capítulo 2 comparando cinco familias de técnicas, las variantes de RAG y los entornos de ejecución local, y
lo cerré con cinco criterios de selección; el capítulo 3 abre ahora justificando cada decisión frente a esos
criterios, que era la petición explícita del profesor. Consolidé el capítulo 3 de seis secciones a cuatro, el 6
de cinco a dos y §5.6 de siete subsecciones a tres, desarrollé la introducción incorporando el enfoque de
solución y la metodología de validación —que las instrucciones exigen y no figuraban— y reescribí §5.3, que
eran cuatro apartados de entre 25 y 35 palabras, el ejemplo más literal del reparo del profesor.

**Los cambios de datos aún no están cerrados.** La re-corrida del corpus N=30 sí llegó completa y verificada, y
está incorporada: `gemma4:31b-mlx` 80,57 % y `gemma4:31b` 78,55 %, con ANOVA recalculado (F=0,2235, p=0,6382) y
las cinco referencias a la cifra de julio actualizadas. Pero **la re-ejecución de `gpt-oss:20b` está a
201 de 240 registros** y va a mover cifras: su F1 baseline ya subió de 0,4384 a **0,5239** confirmado, y cuando
cierre el modo con RAG cambiarán la tabla de §5.3.5, el §6.1, el §6.2 y la sexta conclusión.

Mi recomendación es que **propagues ahora la tanda estructural**, que es la que responde al profesor y no
depende de ningún dato pendiente, y que **no congeles todavía una versión como definitiva**. Habrá una segunda
pasada, breve y acotada a cifras, en cuanto termine esa corrida —unas nueve o diez horas al ritmo actual—.

## Lo que necesito de ti

Propagar a los tres `.docx` con el procedimiento habitual, edición estructural del XML y **nunca pandoc**. Y,
por encima de todo, **medir las páginas reales**: mis cifras son estimaciones sobre el texto y sitúan el cuerpo
en unas 22,3 páginas, contra una restricción institucional de **25 páginas sin anexos** verificada en
`tesinas-finales-2026.pdf`. Si al maquetar te pasas, **avísame antes de recortar**: prefiero decidir qué se
comprime a que se pierda desarrollo recién añadido para atender al profesor. Ten presente que los **anexos no
computan** y disponen de hasta 25 páginas propias, así que son el destino natural de lo que sobre en el cuerpo,
nunca el sitio de donde quitar.

## Lo intocable

**El anexo de declaración de uso de inteligencia artificial se conserva íntegro.** Es el Anexo G del `.docx`
canónico y no se toca, ni se resume, ni se suaviza, ni se reubica. Fue redactado sobre el historial real de
commits y sobre ambos worklogs, y describe con honestidad qué se hizo con asistencia de IA y cómo se verificó.
Esa honestidad es un valor del trabajo, no un trámite: si al recolocar anexos cambiara su letra, mantén la G
para él y desplaza los demás. El mismo criterio vale para el **Anexo H**, que documenta el defecto de
codificación del corpus y la corrección de una conclusión que habíamos publicado mal. Ambos existen para que un
lector pueda auditar el trabajo, no para adornarlo.

Cuando termines, declara el resultado en `CURRENT-TASKS.md` §2 **con el conteo de páginas medido** y deja la
copia del `.docx` canónico en la raíz. La congelación de versión en `doc/versions/informe_final/` déjala para
después de la segunda tanda.

## Regla permanente: nada de arte ASCII

Ningún diagrama debe emitirse como bloque de texto monoespaciado. El arte ASCII se descuadra en Word, donde la
tipografía es proporcional, y produce exactamente el tipo de defecto visual que el profesor señaló. **Todo
esquema va como tabla de Word y todo gráfico como imagen real**, generada electrónicamente y legible, según
pide la plantilla; el bloque monoespaciado queda reservado al **código fuente real**.

La corrección debe hacerse **siempre primero en el `.md` canónico** y solo después reconstruir los `.docx`. Si
se arregla únicamente en el documento de Word, la siguiente reconstrucción desde el Markdown vuelve a
introducir el arte ASCII — que es precisamente lo que ocurrió el 2026-09-07 y obligó a repetir el trabajo.
Esta regla queda también recogida en `CLAUDE.md`.
