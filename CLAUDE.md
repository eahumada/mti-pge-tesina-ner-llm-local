# NER Benchmark Project Directives
## RAG Integration Policy
- **Strict Additive Documentation**: Never overwrite or delete existing documentation when adding new session findings. All documents (`BENCHMARKS.md`, `TODO.md`, `ROADMAP.md`, etc.) must be strictly additive. Verify via git history that no previous content is lost.
- **Comparative Study Value**: A difference of up to 0.02 in F1 Score when comparing Baseline vs RAG is tolerable and considered highly relevant information. Always preserve the RAG infrastructure and indexing work to allow alternate runs (with and without RAG) side-by-side.
- **Metric Degradation Rule**: A drop of up to 0.02 in F1 score is acceptable for the sake of comparison. However, continue evaluating whether further lists degrade precision. The goal is to accurately present the results of the study with and without RAG.
- **Optimal Analysis**: Always analyze the optimal configuration carefully before rolling out to the full benchmark sweep. *(Nota 2026-09-05: el barrido se planificó con 16 modelos; el alcance entonces previsto era de **12** — ver
`TODO-INFORME-FINAL.md §8`.)* **Actualización 2026-09-07:** el estudio cerró con **13 modelos** sobre N=120,
tras incorporar `gemma4:12b-mlx` y `gpt-oss:20b` y retirar `sonct988/gemma4-26b` por no ser reproducible.
El análisis conjunto definitivo está en `results/ANALISIS_CONJUNTO_20260907/` (F=38,2222, p=3,4453e-160) y el
cierre en `CIERRE-BENCHMARKS-20260907.md`.

---

## Entregables Finales

Estos son los artefactos que constituyen la entrega. Deben mantenerse **sincronizados entre sí**;
cualquier corrección se aplica primero al Markdown canónico y luego se propaga a los `.docx`.

| Rol | Artefacto | Ruta |
|:---|:---|:---|
| **Fuente canónica (Markdown)** | Informe Final de Tesina | `doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md` |
| **Entregable canónico (DOCX)** | Informe Final con plantilla UTFSM/MTI | `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx` (raíz) |
| DOCX del borrador Hito 5 | Versión sin plantilla institucional | `doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.docx` |
| Informe standalone | Sin plantilla | `Informe_Final_Tesina_NER.docx` (raíz) |
| Seguimiento de cierre | Estado y pendientes del informe | `TODO-INFORME-FINAL.md` |
| Historial consolidado | Trazabilidad de decisiones y versiones | `HISTORIAL-CONSOLIDADO.md` |

**Reglas de los entregables:**
- Debe existir siempre una copia del `.docx` canónico **en la raíz** del proyecto.
- **Restricción institucional:** el cuerpo del informe no puede exceder **25 páginas**, excluyendo anexos.
  Toda corrección debe ser neutra en extensión o reducirla; verificar el conteo tras cada cambio.
- **Resumen y abstract van fundidos, sincronizados y en la primera página.** Deben decir exactamente lo mismo
  en ambos idiomas, seguir el orden que fija la plantilla —contexto y problema, propuesta y objetivos, método
  de validación, resultados e impacto— y no exceder las **200 palabras** cada uno. Toda corrección de fondo en
  uno se replica en el otro **en el mismo commit**; si divergen, el documento deja de ser coherente para un
  lector que compare ambas versiones. En el `.docx` y en el PDF los dos bloques han de caber en la **página
  inicial**, con el espacio entre el título y su párrafo reducido a nivel de estilo.
- **Los espacios en blanco se recortan por estilo, nunca por contenido.** Ante un desbordamiento de página, se
  ajustan los espaciados de `Heading`, `abstract` y `table caption`, el interlineado y el cuerpo de letra de
  los bloques de código —hasta 7 pt si hace falta—, y solo entonces se considera tocar el texto. Suprimir
  párrafos para ganar espacio requiere autorización expresa del autor.
- **Las cifras económicas son estimaciones y deben declararse como tales.** El coste por artículo del sistema
  local no mide cómputo sino infraestructura amortizada, y no varía entre modelos; el de la revisión manual
  procede de valorar el tiempo de un analista. Ninguno es una medición, y presentarlos sin ese matiz es
  atacable en la defensa.
- **Sin emojis ni marcas de agua en los entregables.** El informe —su Markdown canónico, los tres `.docx` y el
  PDF— no lleva emojis ni pictogramas en ninguna parte: ni en el texto, ni en los encabezados, ni dentro de las
  tablas, donde a veces se cuelan como indicadores de estado (`✅`, `❌`, `⚠️`). Se sustituyen por palabras: «sí»,
  «no», «parcial». Tampoco lleva marcas de agua, sellos de borrador ni fondos: el documento se entrega limpio,
  con el encabezado y el pie que define `plantilla_final-2026.docx` y nada más. Al reconstruir el `.docx` hay
  que comprobar que el proceso no ha introducido ninguno de los dos.
  *Esta regla alcanza solo a los entregables.* Los documentos de coordinación y de trabajo —`CURRENT-TASKS.md`,
  `FINDINGS.md`, `LEARNING.md` y los encargos— sí usan emojis como marcadores de estado, y ahí son útiles: no
  se retiran.
- **Sobriedad tipográfica en el cuerpo del texto.** El guion largo y la negrita se reservan para lo excepcional.
  Un inciso se marca con comas o paréntesis, no con guiones largos; y la negrita se limita a los términos que
  se definen por primera vez y a las cifras que la tabla no recoge, nunca a frases enteras ni a la conclusión
  de un párrafo. Un texto con una negrita por párrafo deja de destacar nada y delata redacción asistida. Como
  referencia, el cuerpo del informe pasó de 113 guiones largos y 164 negritas a 19 y 108 sin perder una sola
  palabra. La regla se aplica **en el `.md`, que es la fuente**, y **su cumplimiento se verifica al generar**
  el `.docx` y el PDF: quien los produce cuenta guiones y resaltes del cuerpo del documento generado y los
  compara con los de la fuente, porque el renderizador no debe añadir énfasis al restituir estilos ni al
  aplicar la plantilla.
- **Ni emojis ni marcas de agua.** Los documentos del proyecto, empezando por el informe y sus derivados, no
  llevan emojis ni pictogramas decorativos, ni en el cuerpo ni en las tablas: donde un símbolo hace de valor
  (una marca de verificación por «Local», una cruz por «Cloud») se escribe la palabra, que es lo que un
  tribunal lee y lo que sobrevive a cualquier tipografía. Tampoco se añaden marcas de agua, sellos de borrador
  ni leyendas superpuestas de ninguna clase. Las flechas tipográficas (`→`) usadas para describir un flujo no
  son emojis y pueden quedarse. La regla rige en el `.md`, que es la fuente, y por tanto en el `.docx` y el PDF.
- **Nada de arte ASCII en los documentos.** Un diagrama dibujado con caracteres (`┌─┐`, `│`, `└┘`) se
  descuadra en Word, porque la tipografía es proporcional y no monoespaciada. Todo esquema va como **tabla de
  Word**, y todo gráfico como **imagen real** —generada electrónicamente, legible y a 300 puntos/cm como pide
  la plantilla—. Los bloques de código monoespaciado solo se reservan para **código real**. La regla aplica
  tanto al `.md` canónico como a los `.docx`: si el diagrama se corrige solo en el `.docx`, la siguiente
  reconstrucción desde el Markdown lo reintroduce.
- Los `.docx` **no deben regenerarse desde el Markdown con pandoc**: contienen correcciones manuales de
  numeración multinivel (`numId=0`), estilos de fila y saltos de página que una regeneración destruiría.
  Para cambios de texto usar `tools/docx_replace_terms.py`, que edita el XML preservando el formato.
- El registro de trabajo **vigente** es `research/rag/WORKLOG.md`. El `WORKLOG.md` de la raíz es
  **histórico: no modificar**.

---

## Orquestación de Workflows

**Regla: en todo workflow, las instrucciones que se entregan a los subagentes deben ser revisadas por un
orquestador Opus antes de despacharse.** El orquestador debe verificar, como mínimo:

1. Que ningún enunciado dirija a **eliminar contenido** (filas de tablas, secciones, párrafos). La política
   del proyecto es estrictamente aditiva: si un conteo no cuadra, se corrige el conteo, no los datos.
2. Que los **datos de referencia** incluidos en el prompt estén verificados contra la fuente primaria, y no
   arrastren interpretaciones de una etapa anterior.
3. Que los agentes que trabajan en paralelo tengan **archivos disjuntos**, para que no se pisen.
4. Que se exija **backup previo** a toda modificación.
5. Que exista una **etapa de verificación** posterior que compruebe que no se perdió contenido.

**Motivación (incidente real, 2026-09-03).** Una auditoría automatizada reportó que las filas
`gemma4:latest (ZS-ES)` y `gemma4:latest (FS-ES)` de la Tabla 2 eran un «duplicado». Esa interpretación se
propagó sin revisión al prompt del workflow de corrección. En realidad son **dos configuraciones de prompt
legítimas** del mismo modelo (zero-shot y few-shot en español) con resultados distintos y válidos. De no
haberse detectado a tiempo, un subagente habría eliminado una fila de resultados del informe para «cuadrar»
el conteo de modelos. El workflow fue detenido antes de modificar archivo alguno y relanzado con la
instrucción corregida y una prohibición explícita.

**Corolario:** un hallazgo de auditoría es una *hipótesis*, no un hecho. Antes de convertirlo en instrucción
de corrección debe validarse contra el documento y, si toca datos experimentales, contra el criterio del autor.

---

## Concurrencia entre Sesiones

**Otras sesiones (Claude Code, Claude Desktop u otro editor) pueden estar modificando estos archivos al
mismo tiempo.** Ya ocurrió: el 2026-09-03 a las 12:36 `HISTORIAL-CONSOLIDADO.md` apareció modificado por un
agente externo a la sesión que trabajaba en él.

**Antes de editar cualquier documento compartido:**
1. **Releer el archivo inmediatamente antes de escribir.** Nunca escribir sobre un contenido leído hace
   varios minutos: puede haber cambiado.
2. **Preferir `append` sobre reescritura completa.** La política aditiva del proyecto también protege
   frente a la concurrencia: añadir al final nunca destruye el trabajo de otra sesión.
3. **Snapshot previo** de los documentos críticos antes de una tanda de correcciones, para poder recuperar
   lo que otra sesión hubiera escrito y se perdiera.
4. **No lanzar varios agentes sobre el mismo archivo**, ni siquiera dentro del mismo workflow. Repartir
   por archivos disjuntos.
5. Si un archivo cambió de forma inesperada, **no revertirlo**: puede ser trabajo deliberado de otra
   sesión. Reportarlo y preguntar.

`ListAgents` enumera las sesiones de Claude Code, pero **no** las de Claude Desktop, así que su ausencia
en el listado no prueba que no haya nadie más editando.

---

## Coordinación entre Agentes — `CURRENT-TASKS.md`

Existe un documento vivo de coordinación en la raíz del proyecto: [`CURRENT-TASKS.md`](./CURRENT-TASKS.md).
Declara **qué agente está trabajando en qué y sobre qué archivos**, con secciones separadas para
**Claude Code**, **Claude Desktop**, **Antigravity** y **Equipo Remoto 48 GB** (§3.bis).

> ⚠️ **PRIORIDAD MÁXIMA: mantener `CURRENT-TASKS.md` actualizado en todo momento.** Es la única fuente de
> verdad sobre qué agente hace qué. Un `CURRENT-TASKS.md` desactualizado provoca solapamientos y pérdida de
> trabajo entre sesiones concurrentes. Actualizar la entrada propia **al iniciar** (`EN CURSO`), **al
> terminar** (`COMPLETADA`/`FALLIDA`) y en cada cambio de estado relevante, y añadir la fila correspondiente
> al **§6 Registro de actualizaciones**. Esto tiene prioridad sobre avanzar en la tarea: primero declarar,
> luego ejecutar.

**Protocolo obligatorio para cada tarea:**

1. **LEER** `CURRENT-TASKS.md` antes de empezar. Comprobar que ningún otro agente declara estar trabajando
   sobre los archivos que se van a tocar.
2. **ESCRIBIR** la entrada propia en la sección del agente correspondiente: tarea, estado `EN CURSO`,
   archivos afectados y hora de inicio.
3. Ejecutar la tarea.
4. **ACTUALIZAR** la entrada al terminar: `COMPLETADA` o `FALLIDA`, con el resultado.
5. **VOLVER A LEER** el documento, por si otro agente escribió mientras tanto.

**Reglas:**
- Si un archivo figura como `EN CURSO` por otro agente, **no tocarlo**: esperar o elegir otro.
- Al **reanudar** una tarea interrumpida, actualizar también su entrada (estado y motivo de la interrupción).
- Escribir siempre por **append** dentro de la propia sección; nunca reescribir entradas ajenas.
- **Todo workflow** debe tener su subsección en §4 de `CURRENT-TASKS.md` (objetivo, fases, agentes,
  archivos tocados y resultado) y mantenerla actualizada.
- **Todo subagente** debe quedar reflejado bajo la tarea padre que lo lanzó.

Este protocolo es la contrapartida operativa de la sección *Concurrencia entre Sesiones*: aquella describe
cómo escribir sin destruir trabajo ajeno; ésta, cómo evitar el solapamiento antes de que ocurra.

---

## Integridad de la medición

Estas reglas se añaden el 2026-09-08, después de que una segunda pasada de revisión independiente encontrara
que el 65 % de los falsos positivos del estudio procedía de una categoría que ningún corpus anotaba. El
defecto sobrevivió dos meses porque las cifras eran internamente coherentes: bajas, pero consistentes entre
sí. Ver `FINDINGS.md §F53` y `LEARNING.md §L44`.

- **Toda categoría que se puntúe debe existir en la anotación de referencia.** Si el prompt pide una
  categoría que el corpus no anota, cada acierto del modelo se contabiliza como error. El indicador barato
  es el **`fn` agregado por categoría**: si vale cero mientras `fp` crece, esa categoría está puntuando
  contra el vacío. Comprobarlo antes de dar por buena cualquier métrica nueva.
- **Una cifra baja pero estable no acredita que la medición sea correcta.** Acredita que el defecto es
  sistemático. La coherencia interna de un conjunto de resultados no es prueba de validez.
- **Cuando existan varias corridas del mismo experimento, el informe declara todas.** Se explica cuál se
  toma como referencia y por qué. Citar la más favorable sin mencionar las demás es indistinguible de
  seleccionar el resultado, aunque no haya intención de hacerlo, y es lo que un tribunal juzga. La política
  aditiva ya obliga a conservarlas; esta regla obliga a **mencionarlas**. Antes de escribir una cifra, buscar
  en `results/` si hay más corridas del mismo experimento.
- **Ninguna cifra entra en una tabla comparativa sin que su fuente esté abierta y leída**, y ninguna columna
  agrupa métricas de tareas distintas bajo un mismo encabezado. Si las filas miden cosas distintas, la
  columna se titula de forma neutra y una glosa advierte que no son comparables.
- **El idioma del corpus se comprueba, no se supone.** Los dos corpus del dominio de este trabajo resultaron
  estar íntegramente en inglés mientras el informe declaraba validación en español (`§F54`).

## Verificación antes de comprometer un cambio en el informe

Comprobaciones mecánicas que hay que pasar sobre el Markdown canónico antes de cada commit. Todas surgieron
de defectos reales encontrados en la revisión final:

1. **Referencias cruzadas**: ninguna llamada a `§x.y`, a `Tabla N` o a `Anexo X` puede apuntar a algo que no
   exista. Atención al escribir: al añadir una referencia se contrae la obligación de crear su destino en el
   mismo commit. Los encabezados del informe llegan al **cuarto nivel** (`#### 5.3.5`), de modo que un patrón
   que solo busque `##` y `###` da falsos positivos.
2. **Tablas**: numeradas de forma contigua **en orden de aparición**, cada una con su leyenda
   `_Tabla N. Texto._` **inmediatamente encima** —a dos líneas o menos, sin párrafos interpuestos—, y con un
   texto que describa lo que la tabla contiene. Una leyenda heredada puede describir otra tabla.
3. **Bibliografía**: entradas contiguas desde `[1]`, toda cita con entrada y toda entrada citada, y **URL
   verificada** en cada una. Una URL no abierta no cuenta como verificada; si el servidor la bloquea (ACM
   devuelve 403 al lector automático), se acredita por resolución del DOI y se deja constancia.
4. **Resumen y abstract**: por debajo de 200 palabras cada uno y corregidos **en el mismo commit**.
5. **Higiene del entregable**: cero emojis, cero arte ASCII, y recuento de guiones largos y negritas del
   cuerpo. Los recuentos absolutos anotados en este documento **no son reproducibles entre métodos de conteo
   distintos**: tres auditores dieron 19/108, 28/127 y 31/150 sobre el mismo texto, según incluyeran o no
   tablas, citas y encabezados. Lo que importa es que el documento generado no añada énfasis respecto de la
   fuente, no acertar con una cifra concreta.
6. **Identificadores**: antes de escribir `§F<n>`, `§L<n>` o `§<n>.<n>`, comprobar que el número no está
   usado. Ha habido **tres colisiones**, dos de ellas posteriores a escribir la lección que advierte de
   ellas, de modo que el recordatorio no basta: hay que comprobarlo con un `grep` en el mismo turno.

## Secretos y publicación del repositorio

- **Reescribir el historial de git no borra un secreto de GitHub.** `git filter-repo` purgó una clave de API
  de los veinte commits afectados y el force-push dejó el remoto limpio, pero el commit antiguo seguía
  respondiendo HTTP 200 y su versión del fichero **todavía contenía la clave en claro**: los objetos quedan
  sin referencia y GitHub los sigue sirviendo por SHA directo. Ver `LEARNING.md §L43`.
- **El remedio es revocar la credencial, y va primero.** Después se pide a GitHub Support la purga de objetos
  inalcanzables. La reescritura es mitigación, no remedio.
- **No hacer público un repositorio que tuvo un secreto** sin haber completado los dos pasos anteriores.
  Publicar convierte una clave recuperable-si-conoces-el-SHA en una clave indexable.
- **Antes de cualquier `--force` sobre el remoto**: respaldo en `git bundle --all`, comprobar que los refs
  remotos coinciden con los locales —para no destruir trabajo de otra sesión— y avisar de que los clones
  existentes quedan incompatibles.
- Los secretos viven en `.setenv.sh`, que está en `.gitignore`. **Ese fichero no está en git**, de modo que
  un clon nuevo no lo tiene.

## Concurrencia: el directorio de trabajo puede cambiar de nombre

El 2026-09-08 a las 03:49 el directorio del proyecto apareció renombrado a `…​.old.bak` por un agente externo
a la sesión que trabajaba en él. **No revertirlo sin comprobar antes qué se perdería.** El repositorio tenía
**274 entradas no rastreadas o ignoradas** que un clon nuevo no habría recuperado, entre ellas `.setenv.sh`
con las credenciales y el directorio `Instrucciones Informe Final de Tesina/` con las normas institucionales.
Renombrar de vuelta conserva todo; clonar de cero, no. El orden correcto es: comprobar que el contenido está
íntegro y sincronizado con el remoto, enumerar lo que no está en git, y solo entonces decidir.
