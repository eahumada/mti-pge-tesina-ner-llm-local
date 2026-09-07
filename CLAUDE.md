# NER Benchmark Project Directives
## RAG Integration Policy
- **Strict Additive Documentation**: Never overwrite or delete existing documentation when adding new session findings. All documents (`BENCHMARKS.md`, `TODO.md`, `ROADMAP.md`, etc.) must be strictly additive. Verify via git history that no previous content is lost.
- **Comparative Study Value**: A difference of up to 0.02 in F1 Score when comparing Baseline vs RAG is tolerable and considered highly relevant information. Always preserve the RAG infrastructure and indexing work to allow alternate runs (with and without RAG) side-by-side.
- **Metric Degradation Rule**: A drop of up to 0.02 in F1 score is acceptable for the sake of comparison. However, continue evaluating whether further lists degrade precision. The goal is to accurately present the results of the study with and without RAG.
- **Optimal Analysis**: Always analyze the optimal configuration carefully before rolling out to the full benchmark sweep. *(Nota 2026-09-05: el barrido se planificó con 16 modelos; el alcance final es de **12** — ver `TODO-INFORME-FINAL.md §8`.)*

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
