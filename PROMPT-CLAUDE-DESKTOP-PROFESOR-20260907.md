# Encargo para Claude Desktop — propagar la revisión pedida por el profesor guía

El profesor guía devolvió el informe con cuatro reparos: demasiados bloques en blanco y saltos de página
entre capítulos, la ficha del estudiante en la primera hoja, poco desarrollo general —«muchas secciones no
son más que un título y un breve párrafo»— y un marco conceptual pobre que no compara alternativas antes de
elegir una. Ya atendí los cuatro en el Markdown canónico,
[`doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md`](./doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md).
El respaldo del estado anterior está junto a él, con sufijo `.bak_profesor_20260907`.

Quité la ficha del estudiante y la sustituí por la cabecera que prescribe `plantilla_final-2026.docx`: título,
autor, dirección institucional y correo. Eliminé los doce separadores que el `.docx` renderizaba como bloques
en blanco. Reduje el resumen de 270 a 201 palabras, porque la plantilla fija un máximo de 200, y lo reescribí
en el orden prescrito. Reescribí el capítulo 2 comparando cinco familias de técnicas, las variantes de RAG y
los entornos de ejecución local, y lo cerré con cinco criterios de selección; el capítulo 3 ahora abre
justificando cada decisión frente a esos criterios, que era lo que el profesor pedía explícitamente. Consolidé
el capítulo 3 de seis secciones a cuatro, el 6 de cinco a dos y §5.6 de siete subsecciones a tres, y desarrollé
la introducción incorporando el enfoque de solución y la metodología de validación, que las instrucciones
exigen y no estaban.

Lo que necesito de ti es propagar todo eso a los tres `.docx` con el procedimiento habitual —edición
estructural del XML, **nunca pandoc**— y, sobre todo, **medir las páginas reales**. Mis cuentas son
estimaciones sobre el texto: el cuerpo ronda las 21,9 páginas de texto y la restricción institucional es de
**25 páginas sin anexos**, verificada en `tesinas-finales-2026.pdf`. Si al maquetar te pasas, avísame antes de
recortar: prefiero decidir qué se comprime a que se pierda desarrollo recién añadido. Ten en cuenta que los
**anexos no computan** y disponen de hasta 25 páginas propias, así que son el destino natural de cualquier
material que sobre en el cuerpo.

**Una cosa por encima de todas: el anexo de declaración de uso de inteligencia artificial se conserva
íntegro.** Es el Anexo G del `.docx` canónico y no se toca, ni se resume, ni se suaviza, ni se reubica. Fue
redactado sobre el historial real de commits y sobre ambos worklogs, y describe con honestidad qué se hizo con
asistencia de IA y cómo se verificó. Esa honestidad es un valor del trabajo, no un trámite: si al recolocar
anexos cambia su letra, mantén la G para él y desplaza los demás. Lo mismo vale para el Anexo H, que documenta
el defecto de codificación del corpus y la corrección de una conclusión que habíamos publicado mal; ambos
anexos existen para que un lector pueda auditar el trabajo, no para adornarlo.

Cuando termines, declara el resultado en `CURRENT-TASKS.md` §2 con el conteo de páginas medido, congela la
versión que corresponda en `doc/versions/informe_final/` según `VERSIONES.md` y deja la copia del `.docx`
canónico en la raíz.
