# Encargo para Claude Desktop — cierre documental del Informe Final

**Fecha:** 2026-09-07 · **De:** Claude Code (equipo principal) · **Estado del proyecto:** benchmarks cerrados

---

## Contexto

La fase de ejecución terminó. No quedan corridas pendientes ni datos por generar: el estudio quedó fijado en
**13 modelos** sobre N=120 y su cierre está documentado en [`CIERRE-BENCHMARKS-20260907.md`](./CIERRE-BENCHMARKS-20260907.md).
Yo ya apliqué al **Markdown canónico** todas las correcciones de contenido que dependían de los datos. Lo que
queda es tuyo: **propagar al `.docx` y cerrar el formato.**

La fuente de verdad es
[`doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md`](./doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md).
El respaldo del estado anterior está en el mismo directorio como `…_Borrador-Informe-Final-Tesina.md.bak_A1A4_20260907`,
por si necesitas ver qué cambió exactamente.

## Lo que ya está hecho en el Markdown (no lo rehagas)

Reconstruí la **Tabla 2 (§5.1)** entera desde los CSV re-puntuados: cada fila es ahora reproducible. Retiré
`nuextract:latest` y `gemini-3.1-flash-lite`, que están fuera del estudio, y añadí `gemma:latest` y `qwen3:8b`,
que sí forman parte y faltaban. Las dos filas de 31B que aparecían con cifras idénticas (67.83 %) ahora tienen
sus valores reales y distintos: `gemma4:31b` 69.12 % y `gemma4:31b-mlx` 68.52 %. La tabla sigue siendo de
**12 modelos en 13 configuraciones**, así que ese enunciado del texto continúa siendo correcto.

Sustituí también la tabla de **§5.2 (Análisis de Variantes de Prompts)** por las mediciones limpias, y eso
**cambió la conclusión**: antes se decía que la localización al español pesaba más que los ejemplos few-shot;
los datos nuevos muestran una **interacción** entre ambos factores —por separado dan +4.38 pp y −0.73 pp, pero
combinados +11.12 pp—. Propagué esa lectura al resumen, a §4.3, a §5.2 y a la conclusión 2.

Reescribí **§5.3.5** con el estudio completo: 13 modelos × 2 modos, **F = 36.3666, p = 1.2236e-152**, y el
resultado de Tukey de que la mejora del KB RAG solo es significativa en `nemotron-mini:4b` (+14.52 pp) y
`llama3.2:latest` (+10.82 pp). Antes esa sección describía un subconjunto de 5 modelos con F = 10.2096.

Y apliqué el **renombrado terminológico** a «Análisis de Variantes de Prompts» en el informe, en
`BENCHMARKS.md` y en `RUNS_INDEX.md`.

## Lo que te toca

**1. Propagar al `.docx`.** Los tres archivos son
`Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx` (el canónico, en la raíz),
`Informe_Final_Tesina_NER.docx` y
`doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.docx`.
Recuerda la regla del proyecto: **nada de regenerar con pandoc**, porque se pierden las correcciones manuales
de numeración multinivel, estilos de fila y saltos de página. Para texto, `tools/docx_replace_terms.py`. Las dos
tablas (§5.1 y §5.2) y la sección §5.3.5 cambiaron de contenido, no solo de cifras, así que ahí necesitarás
edición estructural.

**2. Verificar el límite de 25 páginas.** El Markdown creció en **+66/−52 líneas** con mis correcciones, y antes
ya había crecido con las correcciones B1-B4 del equipo remoto. El cuerpo iba por **20 páginas de 25**, así que
debería caber, pero **hay que medirlo**. Si te pasas, comprime prosa; no elimines filas de datos.

**3. Reinsertar §4.1.3 y §5.3.5 en `Informe_Final_Tesina_NER.docx`** (tarea 2.1, que sigue abierta): ese archivo
no las contiene. Ambas existen íntegras en el Markdown canónico. Ojo: **§5.3.5 acaba de reescribirse**, así que
toma la versión nueva, no la del `.docx` del borrador.

**4. Dos salvedades de datos que hay que declarar en el texto.** Están explicadas en el §2 de
`CIERRE-BENCHMARKS-20260907.md`. La primera: la latencia de `gemma4:31b-cloud` **no mide inferencia** —está
cuantizada por el `--request-delay` que resolvió el *rate limit*, con 114 filas en exactamente 1,02 s—, así que
su F1 vale pero su latencia no puede sostener ninguna comparación de eficiencia. La segunda: siete filas de
`nemotron-mini:4b` tienen `latency=0` y `tok/s=0` porque se re-extrajeron fuera del arnés; sus P/R/F1 son reales,
pero coinciden con la firma de un fallo de infraestructura y hay que decirlo para que nadie las lea como error.

**5. Una decisión del autor que sigue abierta:** el F1 titular de N=30 (**79.03 %**) aparece en el resumen, en
§4.1 y en la conclusión 1. Está registrado que «el nuevo resultado es el oficial y el de julio queda en el
WORKLOG», pero **no hay una corrida N=30 limpia que lo reemplace**. No lo cambies por tu cuenta: pregúntale al
autor si se mantiene con una nota de procedencia o si se retira.

## Reglas que no puedes saltarte

El proyecto es **estrictamente aditivo**: si un conteo no cuadra, se corrige el conteo, nunca los datos. Haz
**backup antes de cada tanda** de cambios. Puede haber **otras sesiones editando a la vez**, así que relee cada
archivo justo antes de escribirlo y prefiere *append* a reescritura. Y declara tu trabajo en
[`CURRENT-TASKS.md`](./CURRENT-TASKS.md) §2 antes de empezar y al terminar: es la única fuente de verdad sobre
qué agente está tocando qué.

Cuando termines, congela las versiones en `doc/versions/informe_final/` según la convención de `VERSIONES.md` y
deja una copia del `.docx` canónico en la raíz.
