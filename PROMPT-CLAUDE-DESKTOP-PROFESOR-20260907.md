# Encargo vigente para Claude Desktop — informe final de tesina

*Reescrito el 2026-09-07 a las 19:30. Sustituye por completo a las versiones anteriores de este archivo, que
se habían ido apilando por tandas y eran difíciles de accionar. Aquí está solo lo que hay que hacer ahora.*

## Qué hay que hacer

Propagar a los tres `.docx` los cambios que el Markdown canónico acumula desde la versión `_v3`, volver a
medir la extensión y congelar una `_v4`. El Markdown es
[`doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md`](./doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md)
y hay respaldos con sufijo `.bak_prosa_20260907` y `.bak_cap23_20260907` por si necesitas ver el estado previo.

## Qué cambió desde la `_v3`

El profesor guía pedía un texto continuo, con más desarrollo y menos secciones que fueran «un título y un
breve párrafo». Sobre esa indicación se han hecho dos pasadas.

La primera convirtió en prosa las secciones que iban en listas o en bloques marcados en negrita: la
justificación de las decisiones de diseño, los modelos evaluados, la taxonomía de errores y los resultados del
ANOVA. El bloque §4.3 se consolidó por completo —sus cuatro subsecciones desaparecen—, §4.1.1 y §4.1.2 se
fundieron en una sola exposición, y la antigua §4.5 se integró al final de §4.4. Los tres ejemplos *few-shot* y
el *prompt* de generación del corpus se trasladaron al Anexo B, que es su sitio natural.

La segunda aplicó el mismo criterio al marco conceptual y a la propuesta. **El capítulo 2 pasa de seis
subsecciones a cuatro y el capítulo 3 de cuatro a tres.** Conviene subrayar que **los capítulos siguen siendo
nueve y ninguno desaparece**: lo que se consolidó fue el nivel de subsección, no la estructura que exige la
plantilla. Se añadió además al Anexo A la URL del repositorio público,
`https://github.com/eahumada/mti-pge-tesina-ner-llm-local`, con la nota de que cada corrida conserva su
`run_config.json` y su `benchmark_results.csv` —es lo que sostiene la replicabilidad que pedía el profesor—.
Por último se suavizaron una docena de construcciones rígidas, alternando las formas cultas con otras más
llanas, para que el texto suene a estudiante sin perder corrección académica.

## Lo que debes vigilar al reconstruir

**Las referencias cruzadas se renumeraron**: §2.2 pasó a §2.1, §2.5 a §2.3, §3.3 a §3.2 y §3.4 a §3.3. En el
Markdown están ya corregidas y verificadas —cero referencias rotas—, pero comprueba que las llamadas del
`.docx` siguen el mismo mapa. Es el fallo más probable de esta propagación.

**Mide la extensión y avísame antes de recortar.** La estimación sobre el texto da unas 19,9 páginas de cuerpo,
frente a las 20 que mediste en la `_v3`, así que debería haber margen sobre el límite de 25. Recuerda que los
anexos no computan y disponen de hasta 25 páginas propias: si algo sobra en el cuerpo, su destino es el anexo,
nunca la papelera.

## Lo intocable

**El Anexo G, la declaración de uso de inteligencia artificial, se conserva íntegro**: no se resume, no se
suaviza, no se reubica. Fue redactado sobre el historial real de commits y describe con honestidad qué se hizo
con asistencia de IA y cómo se verificó; esa honestidad es un valor del trabajo. Si al recolocar anexos
cambiara su letra, mantén la G para él y desplaza los demás. El mismo criterio vale para el **Anexo H**, que
documenta el defecto de codificación del corpus y la corrección de una conclusión que habíamos publicado mal.

**Las nueve tablas del cuerpo son deliberadas**: la comparativa de familias de técnicas (§2.1), el estado del
arte (§2.4), la arquitectura por capas (§3.2), las métricas (§4.4), **la comparativa con todos los modelos
(§5.1)**, las variantes de *prompt* (§5.2), el corpus del dominio (§5.3), **la tabla de los trece modelos
(§5.3.5)** y la eficiencia en hardware (§5.5). No añadas ni quites.

**Nada de arte ASCII.** Los esquemas van como tabla de Word y los gráficos como imagen real; el monoespaciado
se reserva al código. Y toda corrección se hace **primero en el `.md`**: si se arregla solo en el `.docx`, la
siguiente reconstrucción la deshace, como ya ocurrió con los diagramas y con el `&nbsp;` del Anexo A.

**Sin pandoc**, como siempre: edición estructural sobre los estilos de la plantilla.

## Al terminar

Declara el resultado en `CURRENT-TASKS.md` §2 **con el conteo de páginas medido**, congela la `_v4` en
`doc/versions/informe_final/` según `VERSIONES.md` y deja la copia del `.docx` canónico en la raíz.

---

## Cómo cerrar la versión definitiva

Esta propagación es la última prevista: no quedan corridas en ejecución ni cifras por llegar. Si al terminarla
la verificación sale limpia, **esa es la versión de entrega** y así conviene declararla.

**El número de versión da igual** —decisión del autor—. Usa el que corresponda por orden (`_v4`) o cualquier
otro; lo único importante es que quede registrada en `VERSIONES.md` con su SHA-256, su conteo de páginas y la
mención explícita de que es la versión de entrega. No dejes que la numeración te frene.

Antes de congelarla, comprueba una por una estas condiciones. Están tomadas de `plantilla_final-2026.docx`, de
`tesinas-finales-2026.pdf` y de los cuatro reparos del profesor guía; si alguna falla, avísame en lugar de
resolverla por tu cuenta.

**Extensión y formato.** Cuerpo de 25 páginas o menos sin contar anexos, sin tapas ni contratapas. Sin páginas
en blanco ni saltos de página al empezar capítulo. Resumen de 200 palabras como máximo e introducción que no
pase de tres páginas. Anexos empezando en página nueva, después de las referencias.

**Contenido.** Los nueve capítulos presentes y en orden, del 1 al 9. Los ocho anexos, de la A a la H, con la
**G íntegra**. Las nueve tablas del cuerpo, con leyenda encima y numeración correlativa, y las llamadas del
texto apuntando al número correcto. Sin arte ASCII: los esquemas son tablas de Word.

**Coherencia con la fuente.** Las referencias cruzadas siguiendo el mapa renumerado —§2.2→§2.1, §2.5→§2.3,
§3.3→§3.2, §3.4→§3.3—. Las citas en formato IEEE, numeradas y con su entrada en la bibliografía. Y la URL del
repositorio visible en el Anexo A.

**Entregables.** Los tres `.docx` sincronizados entre sí y con el Markdown, la copia del `.docx` canónico en la
raíz del proyecto —lo exige `CLAUDE.md`— y la `_v4` registrada en `VERSIONES.md` con su SHA-256, su conteo de
páginas y la mención de que es la versión de entrega.

Si algo no cuadra y la solución obliga a recortar texto, no lo recortes: dímelo. Los anexos no computan para el
límite y tienen hasta 25 páginas propias, así que casi siempre hay sitio donde mover en lugar de suprimir.
