# CURRENT-TASKS — Coordinación entre Agentes

> **Documento vivo de coordinación.** Varios agentes (Claude Code, Claude Desktop, Antigravity) trabajan
> sobre este repositorio, a veces simultáneamente. Este archivo declara **quién está haciendo qué y sobre
> qué archivos**, para evitar que dos agentes se pisen.

**Última actualización:** 2026-09-05 22:00 · **Actualizado por:** Claude Code

---

## Protocolo obligatorio

Para **cada tarea** que ejecutes:

1. **LEER** este documento antes de empezar. Comprobar que ningún otro agente declara estar trabajando
   sobre los archivos que vas a tocar.
2. **ESCRIBIR** tu entrada en la sección de tu agente: tarea, estado `EN CURSO`, archivos que vas a tocar
   y hora de inicio.
3. Ejecutar la tarea.
4. **ACTUALIZAR** tu entrada al terminar: estado `COMPLETADA` o `FALLIDA`, con el resultado.
5. **VOLVER A LEER** el documento, por si otro agente escribió mientras trabajabas.

**Reglas:**
- Si un archivo aparece declarado por otro agente como `EN CURSO`, **no lo toques**. Espera o elige otro.
- Al **reanudar** una tarea interrumpida, actualiza también su entrada (estado, motivo de la interrupción).
- Escribe siempre por **append** dentro de tu sección; nunca reescribas las entradas de otro agente.
- Todo **workflow** debe tener su propia subsección en §4 y mantenerla actualizada.
- Toda tarea de **subagente** debe quedar reflejada bajo la tarea padre que lo lanzó.

---

## 1. Claude Code

### 1.0 ✅ CERRADA — Resultados parciales del equipo remoto (cerrada 2026-09-07)
> **Cierre (2026-09-07):** el remoto entregó **todo** lo encargado y declaró ejecución 100 % completa
> (`remote_48g/REPORTE-FINAL.md`). El estudio tiene **14 modelos** con los 240 registros completos bajo una
> sola convención de puntuación, y el ANOVA conjunto está en `results/ANALISIS_CONJUNTO_20260907/`
> (F = 36.3696, p = 1.4321e-164). **Lo único que queda de esta tarea es la decisión de alcance del autor
> (14 modelos o los 12 que declara el informe)**, y esperar el test `think=off` de §3.bis.10 antes de
> congelar cifras.
#### Contexto original — 1.0 EN ESPERA — Resultados parciales del equipo remoto
- **Decisión del autor (2026-09-06):** esperar los resultados parciales del equipo de 48 GB antes de
  decidir el alcance final del estudio.
- **La corrida local sigue viva como red de seguridad**, sin bloquear nada. Ver 1.1.
- **Motivo:** con latencias ya medidas (no estimadas), la proyección local es de **~518 h ≈ 21 días**.
  `qwen3:8b` mide **1360 s/artículo** frente a los 192 s que se habían estimado desde su histórico N=15:
  los artículos de N=120 son mucho más largos y la máquina pagina.
- **Qué se espera del remoto:** la tarea de prioridad 3 del encargo es exactamente esta corrida.

### 1.0.bis ✅ COMPLETADA — Unificar convención de scoring y recalcular ANOVA (2026-09-07 11:45→12:05)
- **Autorizado por el autor:** «hacer pull y realizar todo lo recomendado».
- **Archivos:** `results/benchmark_balanced_120_*` (re-puntaje), `CORRECCION-B1-SUMMARIES-20260907.md` (nuevo),
  `results/ANALISIS_CONJUNTO_*` (salida del ANOVA). **No toca** ningún fichero del equipo remoto.
- **Pasos:** (1) re-puntuar las 3 corridas legacy con `tools/rescore_saved.py` (deja `.bak_prescore`);
  (2) avisar al remoto de que B1 estaba invertido y de que los `benchmark_summary.json` /
  `statistical_report.md` de las 8 corridas son anteriores al re-puntaje; (3) ANOVA conjunto con
  `src/merge_and_analyze.py` sobre los CSV (única fuente válida).
- **Resultado:** legacy re-puntuadas (backups `.bak_prescore`). Barrido global: **8 927 filas, 0 violaciones
  `F1 ≤ (P+R)/2`, 0 degeneradas, 0 filas perdidas.** ANOVA conjunto en `results/ANALISIS_CONJUNTO_20260907/`:
  **14 modelos × 2 modos = 28 grupos, 3 360 filas, F = 36.3696, p = 1.4321e-164**.
- **Aviso publicado:** `results/AVISO-SUMMARIES-OBSOLETOS.md` — el CSV es la única fuente válida; los
  `summary`/`statistical_report.md` por corrida y el campo `f1` de `detailed_results.json` son pre-fix.
- **Enviado al remoto:** `CORRECCION-B1-SUMMARIES-20260907.md` (B1 invertido + summaries obsoletos).

### 1.0.ter ✅ COMPLETADA — Cerrar el desfase de `summary`/`detailed` en las corridas legacy (2026-09-07 12:35)
- **Origen:** el commit `17c17fc` del remoto extendió `tools/rescore_saved.py` para reescribir también
  `detailed_results.json` y `benchmark_summary.json`, pero **solo lo aplicó a sus propias corridas**. Las tres
  legacy quedaron con summary y detailed pre-fix pese a tener el CSV ya corregido en `3796218`.
- **Hecho:** herramienta aplicada a las 3 legacy (`e7eb541`). **Precaución tomada:** el respaldo real pre-fix se
  preservó como `.bak_prefix_ORIGINAL` **antes** de correrla, porque su `.bak_prescore` habría sobrescrito el
  backup bueno con el CSV ya corregido.
- **Verificado:** 0 grupos cambian respecto al re-puntaje de `3796218` (las «filas cambiadas» que reporta la
  herramienta son el redondeo a 6 decimales). **`summary == CSV` en las 15 corridas del estudio.**
- **Nota:** los `detailed_results.json` legacy están en `.gitignore` → corregidos en local, no versionados.
- **ANOVA:** no requiere recálculo; los valores no se movieron.

### 1.4 ▶️ EN CURSO — Revisión del informe pedida por el profesor guía (2026-09-07)
- **Origen:** correo del profesor guía con cuatro reparos: bloques en blanco y saltos de página, ficha del
  estudiante en portada, poco desarrollo general y marco conceptual pobre sin comparación de alternativas.
- **Hecho en el `.md` canónico:** cabecera conforme a plantilla (ficha fuera) · 12 separadores eliminados ·
  resumen 270→201 palabras (límite 200) · capítulo 2 reescrito 697→1631 con 5 familias de técnicas comparadas
  y criterios **C1-C5** · capítulo 3 consolidado 6→4 secciones abriendo con la justificación frente a esos
  criterios · capítulo 6 consolidado 5→2 · §5.6 consolidada 7→3 · introducción 645→1117 con enfoque de
  solución y metodología de validación · §5.3 reescrita 125→382 palabras con los datos nuevos de N=30.
- **Verificación de los reparos:** 1, 2 y 4 ✅ cumplidos; el 3 **parcialmente** — quedan secciones cortas
  (§4.5 con 76 palabras, §5.5 con 92, §5.4 con 104).
- **Extensión:** cuerpo ≈ **22,3 páginas de texto** frente al límite de **25 sin anexos**
  (`tesinas-finales-2026.pdf`). **Los anexos no computan** y tienen hasta 25 páginas propias.
- **Fuente de las reglas:** `plantilla_final-2026.docx` (resumen ≤200 palabras, cabecera, estilos) y
  `tesinas-finales-2026.pdf` (25 páginas, introducción ≤3). Calibrado contra las tesinas de ejemplo del MTI.
- **Handoff:** `PROMPT-CLAUDE-DESKTOP-PROFESOR-20260907.md` y §2.8.

### 1.1 🔒 CERRADA — Benchmark N=120 (7 modelos locales)
> **Cerrada por decisión del autor (2026-09-06):** todo lo pendiente pasa al equipo remoto para no duplicar
> esfuerzo. La máquina local queda libre. Sus grupos completos y válidos (`mistral-nemo`) siguen siendo
> aprovechables para la fusión; `gemma4:12b-mlx` y `qwen3:8b` los re-ejecuta el remoto con el fix.
> **No reanudar todavía.** Los bugs de *thinking* (`FINDINGS.md §F40-F41`) invalidan los resultados de
> `gemma4:12b-mlx` y `qwen3:8b` producidos antes del fix `743054d`. Al retomarla habrá que **relanzar esos
> dos modelos desde cero**; el resto de grupos completos (`mistral-nemo`) sí son aprovechables.
> Se espera la respuesta del equipo remoto para no duplicar esfuerzo.

#### Detalle original de la tarea
- **Estado:** ▶️ EN CURSO desde 2026-09-03 16:08
- **Archivos bloqueados:** `repos/ner-llm-entity-benchmark/results/benchmark_balanced_120_kbrag_9models/**`
- **Progreso:** 126 / 1680 filas · `gemma4:12b-mlx_baseline` COMPLETADO (40/40), `_kb_rag` en curso
- **Configuración:** `--rag-mode kb_combined --num-workers 9 --batch-size 3 --results-dir <fijo>`
  (compatible con la corrida de referencia del 2026-09-01, 9 parámetros verificados)
- **Modelos:** gemma4:12b-mlx, qwen3:8b, mistral-nemo, nuextract, llama3.1:8b, nemotron-mini:4b, deepseek-r1:1.5b
- **Excluidos:**`gpt-oss:20b` (13 GB) por RAM de 16 GB; `gemma4:31b-cloud` (HTTP 429)
  y `minimax-m3:cloud` (HTTP 402)
- **ETA:** ~66 h de cómputo neto (más el tiempo perdido en suspensiones).
- **Ejecución (2026-09-04):** migrada a **LaunchAgent de macOS** `local.tesina.benchmark`
  (`~/Library/LaunchAgents/local.tesina.benchmark.plist`) con `KeepAlive`, tras 7 interrupciones del
  ejecutor lanzado desde la sesión. macOS lo reinicia solo y `--resume` retoma desde el checkpoint.
  Para detenerlo: `launchctl unload ~/Library/LaunchAgents/local.tesina.benchmark.plist`
- ⚠️ **Calidad de datos:** 8 suspensiones del equipo (~4.6 h) contaminaron 2 de 48 latencias con valores
  imposibles (9548 s y 15860 s). Media con anómalas 1245 s vs 747 s sin ellas. Requiere `sudo pmset -a
  disablesleep 1` o filtrar los outliers y documentarlo.

### 1.2 🔒 CERRADA — Descarga de modelos 31B para recuperar N=30 (cerrada 2026-09-07)
> **Cierre:** la descarga **se completó** — `gemma4:31b` y `gemma4:31b-mlx` están presentes localmente (19 GB
> cada uno). Pero **no pueden ejecutarse aquí**: su footprint operativo (~24,7 GB) excede el techo de VRAM de
> una máquina de 16 GB. La re-ejecución de N=30 pasa por tanto al equipo remoto (§3.bis.12). Esta tarea deja
> de tener objeto local.

#### Contexto original — 1.2 PAUSADA
- **Estado:** ⏸️ PAUSADA 2026-09-03 16:05 (liberar RAM e I/O para el benchmark; `ollama` reanuda parciales)
- **Pendiente:** `gemma4:31b` (19 GB), `gemma4:31b-mlx` (19.4 GB)
- **Reanudar cuando:** termine la tarea 1.1
- ⚠️ Ambos **exceden la RAM de 16 GB**: se espera swap intenso (~1200 s/artículo según el histórico)

### 1.3 COMPLETADAS
| Tarea | Resultado |
|:---|:---|
| Reparación del `venv` | ✅ Rutas repuntadas, 41 shebangs, sin reinstalar |
| Corrección del flag `--resume` | ✅ Añadido `--results-dir`; era inoperante |
| Guardarraíl anti-sobrescritura de `results/` | ✅ 15 tests pasan |
| `src/merge_and_analyze.py` | ✅ Validado: reproduce F=10.2096, p=2.8730e-15 |
| Auditoría de consistencia | ✅ 115 hallazgos confirmados, 17 descartados |
| Corrección documental | ✅ 84 correcciones aplicadas |
| Reparación de 5 regresiones del workflow | ✅ Verificadas |
| `FINDINGS.md`, `LEARNING.md`, `TODO-INFORME-FINAL.md` | ✅ Creados |
| `tools/docx_replace_terms.py` | ✅ Validado sobre copias; originales intactos |

---

## 2. Claude Desktop

> **Responsable de la edición y el formato de los `.docx`.** Detalle completo en
> [`TODO-INFORME-FINAL.md §7`](./TODO-INFORME-FINAL.md).
> ⚠️ **No regenerar los `.docx` con pandoc**: destruiría correcciones manuales de numeración multinivel,
> estilos de fila y saltos de página (ver `LEARNING.md §L12`).

### 2.0 COMPLETADA — Coordinación multiagente: archivos de instrucciones de la raíz
- **Estado:** ✅ COMPLETADA 2026-09-03 20:18 (iniciada 20:15) · **Agente:** Claude Desktop (Cowork)
- **Resultado:** `AGENT.md` y `ANTIGRAVITY.md` de la raíz actualizados por *append* con el protocolo;
  `GEMINI.md` creado en la raíz. `CLAUDE.md` ya lo incorporaba (Claude Code, 20:12) y no se tocó.
- **Archivos que voy a tocar:** `AGENT.md`, `ANTIGRAVITY.md`, `GEMINI.md` (los tres en la **raíz** del
  proyecto) y las secciones §2 y §6 de este documento.
- **Fuera de alcance (los cubre Claude Code):** `CLAUDE.md` raíz y todo `repos/ner-llm-entity-benchmark/**`
  (`AGENTS.md §11`, `CLAUDE.md`, `GEMINI.md`, `ANTIGRAVITY.md`), ya actualizados a las 20:12–20:13.
- **Objetivo:** que los cuatro puntos de entrada de agente de la raíz declaren el protocolo de
  `CURRENT-TASKS.md`, hoy presente solo en `CLAUDE.md`.

### 2.1 PENDIENTE — Reinserción de secciones faltantes (prioritario)
- **Estado:** ⬜ PENDIENTE
- **Archivo:** `Informe_Final_Tesina_NER.docx`
- **Tarea:** reinsertar íntegras **§4.1.3** y **§5.3.5** (con la tabla 5 modelos × 2 modos y las cifras
  ANOVA F=10.2096 / p=2.873e-15). Existen íntegras en el `.docx` del borrador y en el Markdown canónico.
- **Verificado:** cero ocurrencias de `4.1.3`, `5.3.5` y `10.2096` en su XML.

### 2.2 PENDIENTE — Propagar correcciones del Markdown a los `.docx`
- **Estado:** ⬜ PENDIENTE
- **Archivos:** los tres `.docx` de la tesina
- **Fuente:** `AUDITORIA_CONSISTENCIA_20260903.md` y el Markdown canónico ya corregido
- **Herramienta:** `tools/docx_replace_terms.py` para reemplazos de texto (no inserta secciones)

### 2.3 PENDIENTE — Formato y verificación final
- **Estado:** ⬜ PENDIENTE
- Glosas tipográficas (negrita/cursiva), verificación del límite de **25 páginas**, ausencia de páginas en
  blanco y tablas partidas, numeración multinivel correcta.
- Dejar copia del `.docx` canónico **en la raíz**.


### 2.4 Documentos producidos o actualizados por Claude Desktop en esta sesión
- **Estado:** ✅ REFERENCIA (no requiere acción)

| Documento | Rol |
|:---|:---|
| `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx` | Entregable canónico. Maquetación institucional completa: estilos `Table`/`Compact` definidos, encabezado unificado con imágenes en línea, márgenes 3,3/2,5/3 cm, resumen y capítulos en página propia, 23 leyendas `table caption`, anchos de columna proporcionales, `sectPr` restituido. Cuerpo **20 pp.** de 25; total 29 pp. |
| `doc/versions/informe_final/Informe_Final_Tesina_NER_v1.docx` | Versión congelada `_v1` (SHA-256 `6b53ebd4b1b7…`) |
| `doc/versions/informe_final/VERSIONES.md` | Convención `_v1/_v2/_v3` y registro de versiones |
| `PROMPT-PENDIENTE-INFORME-FINAL.md` | Pendientes con asunto y fecha + procedimiento de cierre de formato (bloque D) + prompt listo para pegar |
| `ANALISIS-ACTUALIZACIONES-INFORME-FINAL_20260903.md` | Análisis de las actualizaciones que requerirá el `.docx`, separadas por dependencia de datos |
| `HISTORIAL-CONSOLIDADO.md` | Historial consolidado: todo lo condensado o reubicado, con el texto suprimido citado literalmente, y §9 con la corrección de renderizado |
| `research/rag/WORKLOG.md` | Tres entradas aditivas: §4.1.3/§5.3.5, redacción de la organización vinculada, y cumplimiento institucional + corrección de renderizado |
| `doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md` y `.docx` | §4.1.3 (corpus N=120 conmutable) y §5.3.5 (validación complementaria) añadidas de forma aditiva |
| Anexo G del `.docx` canónico | Declaración de uso de IA, redactada sobre el historial de commits y ambos WORKLOG |
| Respaldos | `…docx.bak_pre-cumplimiento-25pp`, `HISTORIAL-CONSOLIDADO.md.bak_pre20260903` |
| `AGENT.md`, `ANTIGRAVITY.md`, `GEMINI.md` (raíz) | Protocolo de coordinación (esta tarea 2.0) |

### 2.8 ✅ TANDA ESTRUCTURAL COMPLETADA — Revisión pedida por el profesor guía (2026-09-07)
- **Cerrada la tanda estructural:** 2026-09-07 19:50 por Claude Desktop (Cowork). **Sin congelar versión**,
  a la espera de la segunda tanda (cifras de `gpt-oss:20b`).
- **📏 CONTEO MEDIDO (no estimado):** **cuerpo de 23 páginas de 25**; anexos desde la 24; 33 páginas totales.
  Los anexos ocupan 10 páginas de las 25 propias. **No hubo que recortar nada.** La estimación previa de
  22,3 páginas era buena.
- **Método:** el `.md` reescribía capítulos enteros (+212/−165 líneas), así que en vez de parchear párrafos
  **reconstruí el cuerpo del `.docx` desde el `.md`** con un renderizador propio sobre los estilos de la
  plantilla. **No es pandoc**: conserva `styles.xml`, encabezados, pies, márgenes y `sectPr`, y reaplica la
  numeración literal con `numId=0`, las leyendas sobre cada tabla, los anchos de columna proporcionales y la
  separación de los hallazgos en párrafos propios. Las referencias cruzadas «la Tabla N» se realinearon con la
  numeración real de las leyendas.
- **Los cuatro reparos del profesor, atendidos en los tres `.docx`:** sin ficha del estudiante (la portada es
  ahora título, autor, dirección institucional y correo, como prescribe la plantilla) · **sin saltos de página
  entre capítulos**, texto continuo · sin bloques en blanco (verificado: **cero páginas casi vacías**) ·
  capítulos 2, 3 y 6 y §5.6 con la redacción desarrollada que ya estaba en el `.md`.
- **Datos incorporados:** re-corrida N=30 (`gemma4:31b-mlx` 80,57 %, `gemma4:31b` 78,55 %; ANOVA F=0,2235,
  p=0,6382) y todo lo pendiente de la tarea **2.7** (mojibake): §4.4, conclusión 7, §7.2 punto 7 y el
  **Anexo H** completo. **La 2.7 queda cubierta por esta entrega.**
- **🔒 Anexo G íntegro**, con su letra G, sin resumir ni suavizar. El Anexo H va después, como pedía el encargo.
- **El `.docx` es ahora reflejo exacto del `.md`.** Para lograrlo, y siguiendo la instrucción del autor, llevé
  primero al `.md` los **anexos D, E, F y G**, que hasta ahora vivían solo en el `.docx` (respaldo previo en
  `…Borrador-Informe-Final-Tesina.md.bak_pre_anexosDEFG_20260907`). Los anexos quedan A–H en orden.
- **Respaldo del `.docx` anterior:** `doc/organized/Hito_5_Tarea4_Informe_Final/
  Informe_Final_Tesina_NER_plantilla.docx.bak_pre_profesor_20260907`.
- **Corrección posterior (2026-09-07 20:05) — diagramas como tablas de Word.** Al reconstruir desde el `.md`
  los diagramas de texto habían vuelto a emitirse como bloques `programcode`, contra la regla del proyecto de
  que **todo diagrama va como tabla de Word**, no como cuadro de texto. Se corrigió **primero en el `.md`**
  (respaldo `.bak_pre_diagramas_20260907`) y se reconstruyeron los tres `.docx`: arquitectura de cinco capas de
  §3.2, estructura canónica del prompt *few-shot* de §4.3.1, los dos flujos RAG de §5.6 —con el contexto de
  dominio inyectado como tabla aparte— y el árbol del repositorio del Anexo A. **Cero arte ASCII** en los tres
  documentos; las tablas pasan de 29 a 35. Los bloques de código que permanecen son código real: la interfaz
  `LLMProvider`, los prompts de generación, los tres ejemplos *few-shot* y las invocaciones CLI.
  **Cuerpo re-medido: 23 páginas de 25**, sin páginas en blanco.
- **Pendiente de la segunda tanda:** cuando cierre `gpt-oss:20b`, actualizar la tabla de §5.3.5, §6.1, §6.2 y
  la conclusión 6, volver a medir páginas y **entonces sí** congelar `_v3`.
- **Tomada por:** Claude Desktop (Cowork) · **Inicio:** 2026-09-07 19:45 · Cubre también la tarea **2.7**
  (mojibake), porque la fuente ya incorpora §4.4, §7.1-7, §7.2-7 y el Anexo H.
- **Archivos que voy a tocar:** los tres `.docx`, el `.md` canónico **solo para añadirle el Anexo G**
  (hoy vive únicamente en el `.docx` y la regla es que el `.docx` sea reflejo del `.md`), y esta entrada.
- **Método:** el `.md` acumula +212/−165 líneas y reescribe capítulos enteros, así que en vez de parchear
  párrafos **reconstruyo el cuerpo del `.docx` desde el `.md`** con un renderizador propio que usa los
  estilos de la plantilla (`heading1/2/3`, `p1a`, `table caption`, `Table`, `programcode`, `referenceitem`).
  **No es pandoc**: conserva `styles.xml`, encabezados, pies, márgenes y `sectPr`, y reaplica la numeración
  literal con `numId=0`, las leyendas sobre cada tabla y los anchos de columna proporcionales.
- **Sin saltos de página entre capítulos** (reparo 1 del profesor) y **sin la ficha del estudiante**.
- **No congelo versión.** Queda a la espera de la segunda tanda (cifras de `gpt-oss:20b`).
- **Encargo en prosa:** [`PROMPT-CLAUDE-DESKTOP-PROFESOR-20260907.md`](./PROMPT-CLAUDE-DESKTOP-PROFESOR-20260907.md)
- **Ya aplicado en el `.md`** (no rehacer): ficha del estudiante sustituida por la cabecera de plantilla ·
  12 separadores eliminados · resumen 270→201 palabras · capítulo 2 reescrito (697→1631) con comparación de
  familias de técnicas y criterios C1-C5 · capítulo 3 consolidado 6→4 secciones abriendo con la justificación
  frente a esos criterios · capítulo 6 consolidado 5→2 · §5.6 consolidada 7→3 · introducción desarrollada
  645→1117 palabras con enfoque de solución y metodología de validación.
- **Actualizado 16:45.** Dos tandas: la **estructural** (respuesta al profesor) está firme y puede propagarse ya;
  la **de datos** no, porque `gpt-oss:20b` va por 201/240 y su F1 baseline ya subió de 0.4384 a **0.5239**. Al
  cerrar moverá la tabla de §5.3.5, §6.1, §6.2 y la conclusión 6 → **habrá una segunda pasada breve**.
  **No congelar versión como definitiva todavía.**
- **Incorporado además:** re-corrida N=30 completa (`gemma4:31b-mlx` 80,57 % · `gemma4:31b` 78,55 %; ANOVA
  F=0,2235 p=0,6382) y §5.3 reescrita de cuatro apartados de 25-35 palabras a 382 en prosa.
- **Lo crítico:** **medir las páginas reales**. Cuerpo ≈ 22,3 páginas de texto; límite **25 sin anexos**
  (verificado en `tesinas-finales-2026.pdf`). Los **anexos no computan** y tienen hasta 25 páginas propias.
  **Si se excede, avisar antes de recortar.**
- **🔒 INTOCABLE:** el **Anexo G, declaración de uso de IA**, se conserva **íntegro** — no se resume, no se
  suaviza, no se reubica. Si al recolocar anexos cambiara su letra, se mantiene la G para él y se desplazan
  los demás. Igual criterio para el **Anexo H** (defecto de codificación).

### 2.7 🟡 PENDIENTE — Propagar los cambios de la codificación (mojibake) a los `.docx`
- **Ampliada 2026-09-07 18:10.** Lo que hay que propagar es ahora **cuatro cambios**, no uno:
  1. **§7.2, punto 7** — nueva línea de trabajo futuro (Fase 6): normalización de codificación.
  2. **§7.1, conclusión 7** — nueva conclusión sobre la codificación del corpus.
  3. **§4.4** — dos párrafos nuevos: el umbral de cotejo difuso (85) y la **convención ante la extracción
     vacía**, que documenta por primera vez en el informe la corrección del evaluador aplicada a todo el estudio.
  4. **Anexo H** — nuevo, «Codificación del corpus: análisis del *mojibake* y su efecto sobre la medición»
     (secciones H.1 a H.6). **Va después del Anexo G**, que es el último del `.docx`.
- **Extensión:** los tres primeros van al cuerpo (≈ media página en total) y el Anexo H **no computa** para el
  límite de 25 páginas. El cuerpo iba por **21 de 25**. Re-verificar igualmente.
- **Comprobar además** que los `.docx` llevan la lectura nueva del análisis de variantes en los tres pasajes
  alineados (resumen en inglés, Hallazgo 4 de §5.2 y discusión §6.2).
- **Origen:** decisión del autor del 2026-09-07 (`TODO-INFORME-FINAL.md §15.6`): la normalización de
  codificación del corpus N=120 **se declara como limitación y pasa a trabajo futuro**; no se re-ejecuta.
- **Cambio en el `.md` canónico posterior a tu propagación:** se añadió el **punto 7 a §7.2** («Normalización
  de codificación del corpus y re-evaluación (Fase 6)»). Es **un párrafo**.
- **Qué hacer:** propagarlo a los tres `.docx` con el procedimiento habitual (sin pandoc) y **re-verificar la
  extensión**. El cuerpo iba por **21 páginas de 25**, así que hay holgura.
- **Nada más cambió** en el `.md` desde tu entrega salvo los tres pasajes del análisis de variantes que ya
  alineé (resumen en inglés, Hallazgo 4 de §5.2 y discusión §6.2) — **conviene comprobar que tus `.docx` ya
  llevan la lectura nueva**, según indicaste.

### 2.6 ✅ COMPLETADA — Cierre documental del informe (encargo 2026-09-07)
- **Cerrada:** 2026-09-07 17:25 por Claude Desktop (Cowork). **Resultado:**
  - **Propagado a los tres `.docx` sin pandoc**, por edición estructural del XML: Tabla 2 (§5.1) reconstruida
    con las 13 configuraciones y las cifras nuevas · §5.2 con las mediciones limpias, su nota de procedencia y
    la lectura de **interacción** idioma × *few-shot* · **§5.3.5 reescrita** con el estudio completo de 13
    modelos (F=36.3666, p=1.2236e-152, Tukey) · tablas de eficiencia (§5.5), dict-RAG, Tabla 1, métricas y
    Anexo C actualizadas · terminología «Análisis de Variantes de Prompts» · citas IEEE numeradas y
    **referencia [12] repuesta** · §6.1–§6.5 y las seis conclusiones alineadas con los datos nuevos.
  - **§4.1.3 y §5.3.5 reinsertadas en `Informe_Final_Tesina_NER.docx`** (tarea 2.1 cerrada), tomando la
    **versión nueva** de §5.3.5.
  - **Las dos salvedades de datos quedan declaradas en el texto** de los tres documentos, junto a la
    limitación de *mojibake* del corpus N=120.
  - **Anexo E** reconvertido en tabla de procedencia (la tabla completa vive ahora en §5.1, sin duplicarla).
  - **Extensión verificada: cuerpo de 21 páginas de 25** en el canónico, sin páginas en blanco. No hizo falta
    comprimir prosa ni tocar filas de datos.
  - **Versión congelada `_v2` (2026-09-07)** en `doc/versions/informe_final/`, registrada en `VERSIONES.md`
    con su SHA-256, y **fila «Versión del documento» con la fecha añadida a la ficha** del informe.
  - **No decidido por cuenta propia:** el F1 titular de N=30 (79.03 %) se mantiene tal cual, a la espera del
    criterio del autor (`TODO-INFORME-FINAL.md §15.3`).
- ⚠️ **Discrepancia detectada en la fuente, no corregida por mí:** en el `.md` canónico, el «Hallazgo 4» de
  §5.2 conserva la lectura antigua («la localización al español fue el factor de mayor impacto, +7.4 % de F1»),
  que contradice la tabla nueva y el párrafo de interacción de esa misma sección. En los `.docx` propagué la
  lectura nueva. Conviene alinear el `.md`.
- 📄 Dos archivos temporales de sincronización quedaron en `_to_delete/` (`md_20260903.md`, `md_20260907.md`):
  el puente no tiene permiso de borrado.
- **Tomada por:** Claude Desktop (Cowork) · **Inicio:** 2026-09-07 17:15
- **Archivos que voy a tocar:** los tres `.docx` de la tesina, `doc/versions/informe_final/**`,
  `VERSIONES.md`, y las entradas §2.6 y §6 de este documento. **No toco** el `.md` canónico ni
  `results/**`.
- **Encargo en prosa:** [`PROMPT-CLAUDE-DESKTOP-20260907.md`](./PROMPT-CLAUDE-DESKTOP-20260907.md)
- **Contexto:** benchmarks cerrados (`CIERRE-BENCHMARKS-20260907.md`). **Ya no hay datos por generar.**
- **Ya aplicado por Claude Code en el `.md` canónico** (no rehacer): Tabla 2 §5.1 reconstruida desde los CSV
  re-puntuados · §5.2 con las mediciones limpias y la nueva lectura de **interacción** entre idioma y
  *few-shot* · §5.3.5 reescrita con los 13 modelos (F=36.3666, p=1.2236e-152) · renombrado terminológico ·
  aclaración de que el «12» es la Tabla 2 y el «13» el estudio N=120.
- **Pendiente de Claude Desktop:** propagar a los tres `.docx` (**sin pandoc**, con `tools/docx_replace_terms.py`)
  · **verificar el límite de 25 páginas** (el `.md` creció +66/−52) · reinsertar §4.1.3 y §5.3.5 en
  `Informe_Final_Tesina_NER.docx` tomando la **versión nueva** de §5.3.5 · declarar las dos salvedades de datos
  (latencia del cloud y 7 filas de nemotron) · congelar versiones y dejar copia del canónico en la raíz.
- **No decidir por cuenta propia:** el F1 titular de N=30 (79.03 %) requiere criterio del autor
  (`TODO-INFORME-FINAL.md §15.3`).

### 2.5 PENDIENTE — Cierre de formato, una vez terminados los benchmarks
- **Estado:** ⬜ PENDIENTE · **Bloqueada por:** tareas 1.1 (benchmark de 7 modelos) y 1.2 (N=30)
- **Procedimiento completo:** `PROMPT-PENDIENTE-INFORME-FINAL.md` §4 (pasos D-0 a D-9) y §5 (prompt)
- **Orden de ejecución:**
  1. Incorporar el resultado consolidado del benchmark: §5.3.5, §5.6.5, Anexo E y §7.2, con un **único**
     ANOVA/Tukey recalculado sobre la fusión de la corrida en curso con la del 2026-09-01.
  2. Fijar el alcance real del estudio (**12 modelos**) y la razón de la exclusión de los cloud.
  3. Sustituir el F1 titular de N=30 por el de la re-ejecución, según la decisión ya registrada del autor.
  4. Repetir el bloque de maquetación D-2…D-7 (estilos, encabezado, márgenes y saltos, tablas y leyendas,
     estructura XML, limpieza tipográfica).
  5. Verificación D-8: cuerpo ≤ 25 pp., resumen ≤ 200 palabras, introducción ≤ 3 pp., sin páginas en
     blanco, sin solapamiento con encabezado o pie, tablas con bordes y leyenda numerada, cifras
     trazables a `results/`, anexos A–G en orden.
  6. Congelar `_v2` (correcciones documentales), `_v3` (datos nuevos) y `_v4` (entrega) en
     `doc/versions/informe_final/`, registrando cada una en `VERSIONES.md`.
- ⚠️ **Aviso de Claude Code (2026-09-07 12:45), no reescribe nada de esta entrada:** **no propagar todavía al
  `.docx`.** El remoto está probando `think=off` en 5 modelos (§3.bis.10), 4 de ellos dentro del ANOVA. Si el
  efecto se parece al de `qwen3` (+4,2 pp), la tabla de resultados y el ANOVA cambian y habría que repetir la
  propagación. Además el `.md` canónico creció +18/−8 líneas con las correcciones B1-B4: **re-verificar el
  límite de 25 páginas**.
- **Advertencia:** el bloque de maquetación **no sobrevive** a una regeneración con pandoc. Si el `.docx`
  se regenera desde el Markdown, hay que repetirlo íntegro.

---

## 3. Antigravity

### 3.1 Sin tareas activas
- **Estado:** ⬜ SIN ASIGNACIÓN
- **Instrucciones aplicables:** `repos/ner-llm-entity-benchmark/ANTIGRAVITY.md` → `AGENTS.md`
- Si se le asignan tareas, declararlas aquí antes de empezar.

---

## 3.bis Equipo Remoto (48 GB RAM)

> 🔒 **FASE DE EJECUCIÓN CERRADA (2026-09-07, decisión del autor).** Se conservan los **13 modelos actuales**
> y **no se lanzan más corridas**. Documento de cierre: [`CIERRE-BENCHMARKS-20260907.md`](./CIERRE-BENCHMARKS-20260907.md).
> Alcance final: 13 modelos × 2 modos, F = 36.3666, p = 1.2236e-152. Todo lo que queda es documental.
> Las tareas de §3.bis quedan **cerradas**; solo siguen vivos los dos encargos documentales de
> `CORRECCION-QWEN3-THINKING-20260906.md §4.6-4.7`, útiles únicamente si el estudio se amplía en el futuro.

> **Encargo completo:** [`PROMPT-EQUIPO-REMOTO-48GB.md`](./PROMPT-EQUIPO-REMOTO-48GB.md)
> **Motivo:** la máquina de desarrollo tiene 16 GB y varios modelos no caben (ver `FINDINGS.md §F36`).
> **Protocolo:** el equipo remoto debe **leer este documento antes de empezar**, escribir su entrada al
> iniciar cada tarea, actualizarla al terminar y **volver a leerlo** por si otro agente escribió mientras.

### 3.bis.0 🔴 URGENTE — Re-corrida de `gemma4:12b-mlx` (SUBIR DE PRIORIDAD)
> ✅ **Cerrada (nota de Claude Code, 2026-09-07 17:00; no se altera el texto original).** Completada el
> 2026-09-06: 120+120, 0 `failed`, F1 **0,5618 / 0,5846**. Es la fuente oficial del modelo en el estudio.

- **Estado:** 🔴 PEDIDO · **Encargo:** [`URGENTE-REMOTO-RECORRIDA-20260906.md`](./URGENTE-REMOTO-RECORRIDA-20260906.md)
- **Por qué sube:** es el **único modelo del barrido cuyos datos hay que descartar íntegros**, y bloquea el
  ANOVA definitivo. Estaba encolado tras P4 y `gpt-oss`; se pide adelantarlo.
- **Magnitud confirmada en los datos del remoto:** `recall=0` en **66/120 (baseline)** y **94/120 (kb_rag)**;
  **203 de 206 respuestas crudas vacías** en su `benchmark.log`.
- **Causa:** bug de *thinking* (`FINDINGS.md §F40`). El razonamiento agota `num_predict=2048` antes de emitir
  la respuesta. `kb_rag` falla más porque el contexto RAG alarga el prompt (**+22 % de latencia**).
- **Fix:** commit `743054d`, ya en el árbol. **Requiere `git pull` antes de relanzar.**
- **Criterio de aceptación:** `recall=0` debe ser **residual**, no decenas. Si reaparecen, parar y avisar.

### 3.bis.1 ✅ COMPLETADA — `gemma4:31b` sobre N=15 (PRIORIDAD 1)
- **Ejecutada:** 2026-09-05 23:40 → 2026-09-06 01:55 (reanudada con `--resume` tras pausa) · **Equipo:** Remoto 48 GB (Claude Code)
- **Hardware:** 48 GB · VRAM/modelo 18.8 GB (el de 19 GB cupo; imposible en 16 GB) · sin suspensiones: sí (`caffeinate -dimsu`)
- **Resultados:** baseline F1=0.6912 P=0.5883 R=0.8680 (aluc. 0.16%) · rag_enhanced F1=0.6391 P=0.6080 R=0.8119 (aluc. 0%)
- **Tasa de fallo:** 0/30 · `parse_method`: 29 `direct_json` + 1 `fallback` (recuperación blanda, no `failed`)
- **Protocolo:** `--rag-mode entities` (correcto N=15), `--results-dir` explícito, batch 3 / workers 4. Sin desviaciones.
- **Pre-checks previos (OK):** corpus 15/120 · diccionarios 3605/1848/12000 · diccionarios NO regenerados
- **Entregado en:** `results/gemma4_31b_n15_REMOTO/` (CSV, JSON, statistical_report.md, benchmark.log, run_config.json)
- **Respalda:** la fila de `gemma4:31b` en la Tabla 2 (que citaba F1=67.83% sin dato crudo alguno)
- **Archivos que producirá:** `results/gemma4_31b_n15_REMOTO/`
- **Bloquea:** la fila de `gemma4:31b` en la Tabla 2 del informe, hoy sin respaldo alguno
- **Reportar aquí:** fecha de inicio/fin · F1, P, R obtenidos · **tasa de fallo (debe ser 0)** · RAM pico

### 3.bis.2 🟡 PARCIAL — Modelos excluidos por RAM sobre N=120 (PRIORIDAD 2)
- **Estado:** 🟡 PARCIAL 2026-09-06 02:19 — 1 de 2 modelos OK · **Equipo:** Remoto 48 GB (Claude Code)
- **`` ✅:** 240 filas, tasa de fallo 0.
  baseline F1=0.5627 P=0.5233 R=0.7171 · kb_rag F1=0.5964 P=0.5297 R=0.7608. RAG `kb_combined` confirmado.
- **`gpt-oss:20b` ❌ BLOQUEADO:** 0 filas. **Bug de enrutado**, no de RAM: `factory.py:46` manda todo
  `gpt-*` a `OpenAIProvider`; `gpt-oss:20b` es Ollama local. Error:
  `OpenAIProvider.extract_entities() got an unexpected keyword argument 'rag_context'`.
  AGENTS.md §8.2 lo clasifica «Local/Active» (contradice la fila `gpt-*→OpenAI` de la misma tabla).
- **Efecto actual:** estudio de 12 modelos. Falta gpt-oss para completarlo.
- **Pendiente:** decisión del autor sobre parche de routing (`gpt-oss` → Ollama) para re-correr solo gpt-oss.
- **Archivos:** `results/excluidos_n120_REMOTO/`

### 3.bis.3 ✅ COMPLETADA — Benchmark principal N=120, 7 modelos (PRIORIDAD 3)
- **Estado:** ✅ COMPLETADA 2026-09-06 10:08 (equipo remoto 48 GB) — **1680/1680** · `kb_combined`, workers 8
- **Tasa de fallo:** 8/1680 (0,5%), todos en `nemotron-mini:4b_baseline` (6,7% de ese grupo; residual, sin thinking).
- **F1 modelos válidos (media baseline/kb_rag):** llama3.1:8b 0.496/0.549 · mistral-nemo 0.451/0.483 ·
  nuextract 0.446/0.432 · nemotron-mini 0.363/0.440 · deepseek-r1 0.340/0.339.
- 🔴 **INVÁLIDOS (bug thinking, se re-corren aparte):** `gemma4:12b-mlx` (0.273/0.112) y `qwen3:8b` (0.448/0.443).
- **Entregado:** `results/benchmark_n120_REMOTO/`. Detalle EN CURSO original abajo.
- **Detalle histórico:** arrancó 2026-09-06 02:18, 921/1680 al 09:04.
- **Archivos:** `results/benchmark_n120_REMOTO/`
- **Completos y válidos:** `mistral-nemo`, `nuextract` (en curso), `llama3.1:8b`, `nemotron-mini:4b`,
  `deepseek-r1:1.5b` (ninguno usa *thinking*).
- 🔴 **AFECTADOS por el bug thinking (ALERTA-EQUIPO-REMOTO-20260906):** `gemma4:12b-mlx` (recall=0 en 66-94/120,
  respuestas vacías) y `qwen3:8b` (thinking nunca se activó). El fix (`ollama_provider.py`, commit `743054d`)
  ya está en el árbol, pero **P3 corre con el código viejo cargado** → esos 2 no se salvan en esta corrida.
- **Decisión del autor (aprobada):** dejar P3 terminar (5 modelos válidos) y **re-correr solo los 2 afectados**
  con el fix en `results/afectados_thinking_n120_REMOTO/` (encolado tras P4/gpt-oss). El equipo principal fusiona.

### 3.bis.4 ✅ COMPLETADA — Configuraciones de prompt (PRIORIDAD 4)
- **Estado:** ✅ COMPLETADA 2026-09-06 10:35 (equipo remoto 48 GB) — 60/60, **fallo 0**
- **Archivos:** `results/ablacion_n15_REMOTO/`
- **4 cifras regeneradas (F1, gemma4:latest, N=15):** fs-es **0.7444** (mejor) · zs-es 0.6843 · zs-en 0.6405 · fs-en 0.6332
- **Hallazgo confirmado:** el español mejora; few-shot español es el óptimo. Las cifras que la tesina citaba
  (0.7169/0.6640/0.6482/0.5874) no existían en datos; ahora hay medición trazable.

### 3.bis.6 ✅ COMPLETADA — `gemma4:31b-cloud` sobre N=120 (EN PARALELO)
- **Estado:** ✅ COMPLETADA 2026-09-06 10:08 (iniciada 09:46, equipo remoto 48 GB) · **Encargo:** [`ADENDA-EQUIPO-REMOTO-20260906.md`](./ADENDA-EQUIPO-REMOTO-20260906.md)
- **Resultados:** 240/240 · **tasa de fallo 0/240 (0.0%)**, todo `direct_json`. F1 baseline **0.6238** / kb_rag **0.6268**.
- **Cumple §4.3 del ADENDA** (0 fallo). Es el **10º modelo** del ANOVA. Antes fallaba al 79% por cuota.
- **Entregado:** `results/gemma4_31b_cloud_n120_REMOTO/` (copiado a `remote_48g/`).
- **Ejecución:** wrapper resiliente `run_cloud_resilient.sh` — `--rag-mode kb_combined`, workers 3, `--resume`.
  Corre **en paralelo** con la cadena local (no consume RAM local). Auth OK tras signin del autor + `OLLAMA_API_KEY`.
- **Rate limit implementado (2026-09-06):** flags nuevos `--max-workers` (topa el AIMD) y `--request-delay`
  (intervalo mínimo global entre requests, vía `OLLAMA_REQUEST_DELAY_SEC` en `ollama_provider.py`).
  Corrida cloud lanzada con **`--num-workers 1 --max-workers 1 --request-delay 3.0`**.
  - Sin rate limit (workers 3): **172× HTTP 429**. Con rate limit (1 worker + 3s): **0× 429**, 28× 200 OK. ✅
- **Resiliencia:** wrapper `run_cloud_resilient.sh` con `--resume` — continúa tras cortes; espera 15 min en
  429; se detiene en 402 (barrera de plan) o al completar 240 filas.
- **Criterio de parada (ADENDA):** comprobar fallo a mitad; parar si >10%. 429=esperar, 402=avisar.
- **Archivos que producirá:** `results/gemma4_31b_cloud_n120_REMOTO/`
- **Por qué:** su única corrida sobre N=120 es inservible — **190 de 240 fallos (79 %)** por cuota, y con
  modo RAG legacy `entities` en vez de `kb_combined`. Su dato limpio (F1 0,6699) es de N=15 y no sirve
  para el estudio N=120.
- **No consume RAM local** ⇒ no cuenta para la serialidad; puede lanzarse ya, solapado con lo demás.
- ⚠️ **Criterio de parada:** comprobar la tasa de fallo **a mitad de corrida**. Si supera el **10 %**, parar.
  429 = esperar a que renueve la cuota. 402 = avisar, es barrera de plan.

### 3.bis.7 ✅ RESUELTA — dos anomalías detectadas en P3
Detectadas por el equipo principal al analizar `benchmark_n120_REMOTO`. **Investigadas por el equipo remoto (2026-09-06 16:46).**

> **Conclusión a):** `nemotron-mini:4b_baseline` — los 8 `failed` son **respuestas vacías** (len 0, 2 reintentos),
> pero **NO es thinking** (el modelo no la declara) y **NO correlaciona con longitud** (fallidos mediana 1471
> chars vs OK 1856; procesó bien uno de 8813). Son **vacíos esporádicos inherentes al 4B**. Re-corrida en
> `results/nemotron_rerun_n120_REMOTO/` → siguen 7/240 → confirmado no corregible. **Acción:** excluir esas filas.
> **Conclusión b):** `mistral-nemo` — confirmado benigno: el RAG le altera el formato (69 `fallback`) pero el
> respaldo rescata (recall=0 solo 4). Sin acción; documentado.

#### a) `nemotron-mini:4b_baseline` — los únicos `failed` de toda la corrida
- **8 `parse_method: failed`** y **26 `recall=0`** de 120.
- Su condición `kb_rag` solo tiene **9 `recall=0`** y **cero `failed`** — el baseline falla 3× más.
- Son los **únicos 8 `failed` de las 1680 filas** de P3. Todo lo demás resuelve por `direct_json`,
  `codeblock` o `fallback`.
- **Qué mirar:** ¿respuestas vacías (firma del bug de *thinking*) o malformadas? El diagnóstico es el mismo
  que usamos en `gemma4:12b-mlx`: `grep "Failed to parse JSON from raw response:" benchmark.log` y comprobar
  si lo que sigue está vacío. Si lo está, y `nemotron-mini` declarara capacidad `thinking`, sería el mismo
  caso y bastaría añadirlo a `_THINKING_DISABLED_MODELS`.
- **Impacto:** F1 baseline 0,3630 frente a 0,4399 en kb_rag. Si los 8 fallos y parte de los 26 ceros son
  espurios, su cifra de baseline está subestimada.

#### b) `mistral-nemo:latest` — salto de `fallback` con RAG
- `baseline`: 9 `fallback` de 120 · `kb_rag`: **69 de 120**.
- El respaldo **sí rescata contenido** (recall=0 se mantiene en 3 y 4), así que no es el caso de
  `gemma4:12b-mlx`. Pero un salto de 9 a 69 indica que **el contexto RAG le altera el formato de salida**.
- **Qué mirar:** si el modelo, al recibir contexto RAG, envuelve la respuesta de otro modo (bloque de código,
  preámbulo) que el parser directo no acepta. No invalida sus cifras, pero conviene entenderlo antes de
  citarlas.

> **Método sugerido** (el que funcionó con `gemma4:12b-mlx`): cruzar `parse_method` con `recall` distingue un
> respaldo que funciona de uno que encubre un fallo. Y `latency_sec` con tokens generados distingue un
> rechazo de infraestructura (latencia 0) de que el arnés pierda la respuesta (latencia alta, `content` vacío).

### 3.bis.8 ▶️ EN CURSO — re-corridas de modelos afectados por bug thinking
> ✅ **Cerrada (nota de Claude Code, 2026-09-07 17:00; no se altera el texto original).** Ambas re-corridas
> terminaron: `gemma4:12b-mlx` limpio y `qwen3:8b` sustituido por la corrida `think=false`
> (`qwen3_nothink_n120_REMOTO`, F1 0,4821 / 0,5146), que es la fuente oficial.

- **`gemma4:12b-mlx` ✅ LIMPIO:** `results/afectados_thinking_n120_REMOTO/` — 120+120, 0 failed,
  F1 0.5618/0.5929 (reemplaza P3 inválido 0.27/0.11).
- **`qwen3:8b` ▶️ RE-CORRIDA LIMPIA:** `results/qwen3_clean_n120_REMOTO/` (dir fresco, sin reinicios, workers 6).
  Motivo: los reinicios para optimizar concurrencia corrompieron la cobertura en la corrida de afectados
  (baseline 99/120 únicos). **Usar `qwen3_clean_n120_REMOTO`, no la de afectados.** ETA ~1.5-2 h.

### 3.bis.9 🟠 ENVIADA — Corrección del hallazgo qwen3 thinking (instrucciones nuevas)
- **Documento:** [`CORRECCION-QWEN3-THINKING-20260906.md`](./CORRECCION-QWEN3-THINKING-20260906.md)
- **Qué corrige:** `HALLAZGO-QWEN3-THINKING.md` da P3 como *think OFF*; era **think ON**. Antes del fix
  `743054d`, `think` iba dentro de `options` y Ollama lo descartaba, dejando **el default (thinking ON)**.
- **Evidencia:** P3 vs corrida limpia = **120/120 filas con (F1,P,R) idénticos** y 0/120 con latencia igual;
  P3 corrió 05:07-06:19, el fix llegó 09:08. Latencia mediana 789 s / 517 s / **67 s** (nothink).
- **Comparación válida** (78 artículos comunes, P3 think ON vs nothink think OFF):
  F1 **0.4606 → 0.5122** (+5,2 pp) · `recall=0` **10 → 1** · latencia **688 s → 66,5 s** (10,3×).
- **Decisión `think=False`: se mantiene** (mejor respaldada de lo que se argumentó).
- **Pedidos al remoto:** nota de corrección aditiva en su hallazgo; terminar `qwen3_nothink_n120_REMOTO`;
  marcar inválidas las filas qwen3 de P3/limpia; publicar los `run_config.json` que faltan; revisar
  `qwen3:14b/32b/latest`; enumerar modelos con capacidad `thinking`; no tocar `real_mixed_64`.

### 3.bis.10 ▶️ EN CURSO — Test `think=off` sobre 5 modelos + verificación de las entregas B1-B4
> ✅ **Cerrada (nota de Claude Code, 2026-09-07 17:00).** El experimento concluyó y su resultado está en
> `FINDINGS.md §F44` y **§F45**: efecto específico de cada modelo, `gpt-oss` se congela con thinking ON y los
> otros cuatro no se re-ejecutan por ser ruido de N=15.

- **Confirmado por el autor (2026-09-07):** el remoto está evaluando muestras de **5 modelos con
  `thinking=off`**. Se corresponde con la modificación sin commitear de `src/providers/ollama_provider.py`
  (`# TEST think-off 2026-09-07`): `gemma4:31b`, `gemma4:latest`, `deepseek-r1:1.5b`, `gpt-oss:20b` y
  `…`. **No tocar ese archivo desde otra sesión.**
- **Por qué importa:** **cuatro de esos cinco están dentro del ANOVA conjunto** y el quinto (`gemma4:31b`)
  alimenta la tabla §5.5. Si el efecto se parece al de `qwen3` (+4,2 pp, `recall=0` de 15 → 1), **habrá que
  rehacer tabla y ANOVA**. Caso a vigilar: `gpt-oss:20b` es hoy el único ΔRAG muy negativo (−0.097); si corría
  con thinking activo, esa cifra puede no estar midiendo el RAG.
- **Entregas verificadas por el equipo principal:**
  - `38b20da` (B1-B4 al `.md` canónico + `BENCHMARKS.md`): **B4 reproduce exacto** — `gemma4:31b-mlx`
    24 607/22.80 y `llama3.2` 4 018/79.35 salen de `results/benchmark_results.csv` (N=15 canónico, 450 filas);
    `gemma4:31b` 18 795/10.23 de `gemma4_31b_n15_REMOTO`. B1 adopta 0.4876/0.5075 ✅.
  - `17c17fc` (rescore extendido): **`summary == CSV` sin discrepancias** en sus corridas.
- **Dos avisos abiertos:**
  1. El `.md` canónico creció **+18/−8 líneas** (sobre todo el párrafo de B3). **Re-verificar el límite de
     25 páginas** al propagar al `.docx`.
  2. `BENCHMARKS.md` rotula la resolución B1 como «decisión del autor, 2026-09-07». **El autor no tomó esa
     decisión**: salió de `CORRECCION-B1-SUMMARIES-20260907.md`. El fondo es correcto; corregir la atribución.
- **Sigue pendiente de `CORRECCION-QWEN3-THINKING-20260906.md §4.6-4.7`:** revisar `qwen3:14b/32b/latest` y
  **enumerar todos los modelos del estudio con capacidad `thinking`**.

### 3.bis.11 📌 HALLAZGO FINAL — Política de *thinking* y reglas para ejecuciones futuras
- **Documento canónico:** [`RECOMENDACIONES-EJECUCIONES-FUTURAS.md`](./RECOMENDACIONES-EJECUCIONES-FUTURAS.md)
  · **Evidencia:** `FINDINGS.md §F44` (vuestro experimento) y **§F45** (verificación del equipo principal)
  · **Anexo de tareas futuras:** `TODO-INFORME-FINAL.md §14`.
- **Vuestro experimento queda verificado:** las 12 filas reproducen exactamente desde los CSV, 0 `failed`,
  0 violaciones aritméticas. Método correcto.
- **Se refuerzan dos resultados:** `gpt-oss:20b` no razona peor sin *thinking*, **deja de responder**
  (`recall=0` en 7/15 y 10/15) → ON congelado; `deepseek-r1:1.5b` da los **15 registros idénticos**
  (dif. máx. 4.4e-07, puro formato) → su razonamiento no cambia ni una entidad.
- **No sostienen cambio de régimen:** `gemma4:latest` cambia de signo entre sus propias condiciones
  (+0.066 `fs-en` / −0.051 `fs-es`) y `gemma4:31b` igual (−0.029 / +0.037): ruido, no efecto. La latencia con
  *thinking* apagado (×0.3), lo que contradice el modelo causal.
- **🔴 DECISIÓN CERRADA: NO re-ejecutar** los 4 modelos con `think=OFF`. Se apoyaría en ruido de N=15 e
  introduciría un **segundo eje de inconsistencia** en el estudio. El valor del experimento es documental y
  ya está capturado.
- **Para el futuro (aplicar siempre):** no generalizar entre modelos · `think` es kwarg de primer nivel,
  nunca dentro de `options` · medir con el pipeline real antes de cambiar · exigir signo estable en todas las
  condiciones y |ΔF1| ≥ 0.05 con N=15 · exigir mecanismo (`recall=0`, latencia) · la latencia debe corroborar
  la hipótesis · declarar el régimen en `run_config.json` · si dos corridas dan métricas idénticas fila a
  fila, no han comparado nada.
- **Pendiente vuestro:** evaluar `qwen3:14b/32b/latest`, **enumerar los modelos con capacidad `thinking`** y
  el censo de modelos con capacidad `thinking`.

### 3.bis.12 ✅ COMPLETADA — Re-ejecutar la corrida N=30 (2026-09-07)
- **Entregada y verificada:** `results/n30_rerun_REMOTO/` — protocolo correcto, **30/30 registros únicos por
  modelo, 0 `failed`, 0 `recall=0`, 0 violaciones aritméticas**. `gemma4:31b-mlx` **80,57 %** (P 74,17 · R 90,72)
  y `gemma4:31b` **78,55 %** (P 73,34 · R 88,28). ANOVA recalculado **F=0,2235 · p=0,6382** (misma conclusión
  que el F=0,141 previo: diferencia no significativa). Sensibilidad: 0 registros atípicos.
- **Resuelve la duda de fondo:** frente al 79,03 % de julio, **la precisión coincide hasta el cuarto decimal**
  y el F1 difiere en <0,5 pp → la cifra de julio queda **validada además de reemplazada**.
- **Incorporado al informe:** §5.3 reescrita; cinco referencias a 79,03 % actualizadas.

#### Detalle original del encargo
- **Encargo completo:** [`ENCARGO-REMOTO-N30-20260907.md`](./ENCARGO-REMOTO-N30-20260907.md)
- **Decisión del autor (2026-09-07):** re-ejecutar. **Excepción explícita al cierre de benchmarks**; se reabre
  la ejecución **solo para esta corrida**, ninguna otra.
- **Motivo:** el F1 titular de N=30 (`gemma4:31b` 79.03 %) es **la única cifra del estudio aún calculada con el
  *scorer* defectuoso**, y no se puede re-puntuar porque el dato por registro se perdió por sobrescritura.
  Solo sobrevive el agregado en `benchmark_augmented_30.log`.
- **Por qué al remoto:** los dos modelos pesan 19 GB en disco y ~24,7 GB operativos; no caben en los 16 GB
  de la máquina de desarrollo.
- **Qué:** `gemma4:31b` y `gemma4:31b-mlx` · corpus `data/kleptotrace_augmented_30.json` (verificado: 30
  registros) · **baseline sin RAG** · `--batch-size 5 --seed 42` · `--results-dir results/n30_rerun_REMOTO`.
  **Régimen de *thinking* sin cambios** (statu quo de `FINDINGS.md §F45`).
- **ETA:** ~9 h en serie (5,1 h + 3,6 h, una GPU).
- **Entregar:** el directorio completo, el **ANOVA entre los dos modelos** (reemplaza el F=0.141 de §5.3.2) y
  el reporte con las verificaciones estándar.
- **Prohibido:** re-ejecutar cualquier otra corrida, tocar `ANALISIS_CONJUNTO_20260907/` o las corridas
  N=120/N=15, y borrar `benchmark_augmented_30.log`.

### 3.bis.13 ✅ COMPLETADA — Re-ejecución de `gpt-oss:20b` (2026-09-07)
- **Entregada y verificada:** 120+120, **0 `failed`**, **238 de 240 filas en `direct_json`** (antes 67
  `fallback`), 0 violaciones aritméticas. **F1 0,5239 / 0,5567** frente a 0,4384 / 0,3419 originales.
- **ΔRAG pasa de −0,097 a +0,033:** desaparece el único descenso grande del estudio, que era un **artefacto
  del arnés** —truncamiento por `num_predict`— y no una conducta del modelo.
- **ANOVA conjunto rehecho:** `results/ANALISIS_CONJUNTO_20260907/` → **F=38,2222 · p=3,4453e-160**
  (antes 36,3666 / 1,2236e-152). **10 de 13 modelos** con ΔRAG positivo.
- **Efecto colateral en el Anexo H:** el delta de mojibake de `gpt-oss` pasa de **+0,0914 a −0,0336**; el
  rango entre modelos baja de 16 a **9,4 puntos**. La cautela que se había dejado escrita sobre esa fila
  resultó acertada.

#### Detalle original del encargo
- **Diagnóstico COMPLETADO** (`remote_48g/DIAGNOSTICO-GPTOSS-20260907.md`): descartó el bucle de repetición
  (0/5) y apuntó al agotamiento de `num_predict`. **La hipótesis del equipo principal era incorrecta**; la
  causa real es truncamiento por presupuesto de tokens.
- **Re-ejecución con `num_predict=4096` — 201/240 al 2026-09-07 16:30.** Verificado: **baseline 120/120 con
  F1 0,5239** (antes 0,4384), `recall=0` **6** (antes 27), **200 de 201 filas en `direct_json`** frente a 67
  `fallback` en la corrida original, **0 avisos de truncado**. El arreglo funciona.
- **`kb_rag` 81/120 — cifra provisional, NO citar** (lección de `qwen3`: 0,5147 parcial → 0,4904 completo).
- **Al cerrar:** rehacer el ANOVA conjunto y actualizar tabla de §5.3.5, §6.1, §6.2 y conclusión 6 del informe.
- **Parte A del encargo (rescate de N=30 en la máquina remota):** superada — la re-corrida se completó igualmente.

#### Detalle original del encargo
- **Encargo completo:** [`ENCARGO-REMOTO-GPTOSS-20260907.md`](./ENCARGO-REMOTO-GPTOSS-20260907.md)
- **Parte A — antes de re-ejecutar N=30:** buscar en la máquina remota si sobreviven los datos por registro
  de la corrida sobre `data/kleptotrace_augmented_30.json`. En la de desarrollo se perdieron por
  sobrescritura, **pero puede que allí no**. Si aparecen, se re-puntúan con `tools/rescore_saved.py`
  **sin re-inferir** y nos ahorramos las 9 h de §3.bis.12.
- **Parte B — `gpt-oss:20b`:** 76 filas con `recall=0` (27 baseline + 49 kb_rag). **67 son `fallback`** y el
  log registra **69 × «Failed to parse JSON from raw response»**. **45 de las 49 de kb_rag** quedan en
  `tp=0, fp=0`. **No es rechazo de infraestructura:** latencia mediana 838 s frente a 854 s de los aciertos,
  con volumen de tokens equivalente — el modelo trabaja y produce salida.
- **Hipótesis:** **degeneración por repetición**. Las dos respuestas crudas legibles del log extraen entidades
  correctas y luego entran en bucle (`way, way, way…` / `[Note: This [Note: This…`), dejando el JSON sin
  cerrar. El log trunca, así que **no sabemos en qué proporción de los 69 ocurre**: eso es lo que deben medir.
- **Qué ejecutar:** 10 registros que fallaron (5 + 5), guardando la respuesta cruda íntegra, en dos
  condiciones: tal cual, y con `repeat_penalty` >1.1 (1.15–1.3). **~2,5 h.**
- **Extra crítico:** verificar el **mojibake** (`CorÃ­n Tellado` en el log). Si la doble codificación afecta al
  texto comparado con el *ground truth* y no solo al fichero de log, **ningún nombre español con tilde casaría
  nunca, en todos los modelos**.
- **Prohibido:** parchear solo las filas que fallan (sesgaría la media al alza; es el 32 % de la corrida). Si
  se confirma causa corregible, lo correcto es re-ejecutar `gpt-oss:20b` completo — **y esa decisión la toma
  el autor**.

### 3.bis.14 🔮 TAREA FUTURA — corregir mojibake del gold N=120 y re-inferir el estudio
> **Nota (Claude Code, 2026-09-07 17:00):** esta entrada se registró como «§3.bis.9», número ya ocupado por la
> corrección del hallazgo qwen3. Se renumera a **§3.bis.14** por ser posterior; no se altera su contenido.
> Matiz importante añadido después: el sesgo **no es uniforme** entre modelos (ver `FINDINGS.md §F48`).
- **Estado:** ⬜ FUTURA · **Asignada al:** Equipo Remoto 48 GB (NVRAM unificada) · **Decisión del autor (2026-09-07)**
- **Motivo:** el ground truth de `data/benchmark_balanced_120.json` tiene **mojibake** (UTF-8 leído como
  Latin-1): 283/1406 entidades (20 %), **66 (4.7 %) irrecuperables** → recall subestimado en **todos** los
  modelos del N=120 por igual (ver `FINDINGS.md §F46`). `kleptotrace` (N=15) y `augmented_30` (N=30) **limpios**.
- **Por qué es futura y pesada:** corregir el gold (`encode('latin-1').decode('utf-8')`) **exige RE-INFERIR**
  todo el N=120 — las extracciones crudas por registro no se persistieron (solo `tp/fp/fn`), así que el
  matching no se puede rehacer sobre datos guardados. Implica re-correr los ~14 modelos N=120 y **re-fusionar
  el ANOVA conjunto**.
- **Pasos:** (1) de-mojibake del corpus gold; (2) re-run N=120 de todos los modelos (con sus regímenes de
  thinking ya decididos); (3) re-puntuar y re-fusionar ANOVA; (4) actualizar §5.3.5/§5.6.5/Anexo E del informe.
- **Requiere 48 GB** por los modelos 31B (~24.7 GB, no caben en 16 GB).

### 3.bis.5 Plantilla de reporte
Al terminar cada tarea, sustituid su bloque por:

```
### 3.bis.N ✅ COMPLETADA — <tarea>
- **Ejecutada:** <inicio> → <fin>  ·  **Equipo/persona:** <nombre>
- **Hardware:** <RAM total> · pico de uso <X GB> · sin suspensiones: <sí/no>
- **Resultados:** F1=<x> P=<x> R=<x>  (por modelo y condición)
- **Tasa de fallo:** <n>/<total>  ← debe ser 0; si no, indicar causa (429/402/parseo)
- **Protocolo:** <confirmar --rag-mode usado y cualquier desviación>
- **Entregado en:** results/<dir>/  (CSV, JSON, statistical_report.md, benchmark.log)
```

Y añadid una fila al **§6 Registro de actualizaciones** con fecha, agente y cambio.

---

## 4. Workflows

> Todo workflow debe declarar aquí su subsección: objetivo, fases, agentes, archivos tocados y resultado.

### 4.1 `auditoria-consistencia-tesina` — ✅ COMPLETADO
- **Cuándo:** 2026-09-03, ~65 min · **Agentes:** 10 (5 auditores + 5 verificadores adversariales)
- **Archivos:** solo lectura (no modificó nada)
- **Resultado:** 115 hallazgos confirmados (26 altos, 55 medios, 34 bajos), 17 descartados
- **Salida:** `AUDITORIA_CONSISTENCIA_20260903.md`

### 4.2 `correccion-consistencia-tesina` — ✅ COMPLETADO (con regresiones reparadas)
- **Cuándo:** 2026-09-03, ~18 min · **Agentes:** 8 (4 correctores + 4 verificadores de integridad)
- **Archivos:** informe `.md`, `BENCHMARKS.md`, `AGENTS.md`, `README.md`, `TODO.md`, `RUNS_INDEX.md`,
  `HISTORIAL-CONSOLIDADO.md`, `research/rag/WORKLOG.md`
- **Resultado:** 84 correcciones aplicadas
- ⚠️ **5 regresiones detectadas por la fase de verificación y reparadas por Claude Code**: borrado de
  `glm-5.1:cloud` (violación de la política aditiva), snippet Python inválido, reaparición del nombre de
  modelo retirado, autocontradicción entre §8.3 y §8.4, y consejo de `--resume` inoperante.
- **Nota:** una primera ejecución fue **detenida antes de tocar archivo alguno** porque su prompt contenía
  una premisa errónea que habría eliminado una fila de datos experimentales. Ver `CLAUDE.md §Orquestación`.

---

## 5. Procesos de fondo activos

| Proceso | Función |
|:---|:---|
| `caffeinate -dimsu` | Impide la suspensión del equipo (`pmset` tiene `sleep 1`) |
| Ejecutor resiliente | Reintentos con `--resume` para el benchmark |
| Watchdog | Detecta suspensiones, caídas de red y muerte de `caffeinate` |
| Detector de concurrencia | Registra cambios externos en los documentos críticos cada 45 s |

---

## 6. Registro de actualizaciones

| Fecha/hora | Agente | Cambio |
|:---|:---|:---|
| 2026-09-03 16:15 | Claude Code | Creación del documento con el estado inicial |
| 2026-09-03 16:22 | Claude Code | Protocolo documentado en `CLAUDE.md` (raíz y repo), `AGENTS.md §11`, `GEMINI.md` y `ANTIGRAVITY.md` |
| 2026-09-03 16:24 | Claude Code | Reparadas 5 regresiones introducidas por el workflow de corrección (ver §4.2) |
| 2026-09-03 16:32 | Claude Code | `glm-5.1:cloud` eliminado globalmente (cero resultados, HTTP 402). Criterio adoptado: un modelo cloud se conserva si tiene resultados, se elimina si no. Ver `TODO-INFORME-FINAL.md §9` |
| 2026-09-04 14:00 | Claude Code | Benchmark migrado a LaunchAgent tras 7 interrupciones. Bug corregido: bajo launchd faltaba `/opt/homebrew/bin` en el `PATH` y la lista de modelos salía vacía |
| 2026-09-04 14:00 | Claude Code | 🔴 SEGURIDAD: 2 credenciales filtradas — API key de Google en `test_flash.py` **publicada en GitHub** (commits `0b27b5c`, `0cc973b`), y PAT de GitHub en `.git/config` |
| 2026-09-05 22:00 | Claude Code | Workflow ronda 2 completado: 12 correcciones, 57 ya hechas, **integridad OK en los 4 archivos** (sin pérdida de contenido ni tablas rotas) |
| 2026-09-05 22:00 | Claude Code | 🔴 Detectados 8 BLOQUEANTES de integridad numérica que requieren decisión del autor. Ver `TODO-INFORME-FINAL.md §10` y `FINDINGS.md §F27-F30`. El más grave: 2 valores de F1 **aritméticamente imposibles** |
| 2026-09-05 21:50 | Claude Code | 🟡 SEGURIDAD (parcial): claves fuera del código — `test_flash.py` lee del entorno, todos los secretos en `.setenv.sh` (600, gitignored), PAT retirado de `.git/config`. Espejo con historia reescrita listo y verificado (0 blobs con la key), pero **el `push --force` sigue sin ejecutar**. ⚠️ **La revocación de ambas credenciales sigue pendiente y es lo único que mitiga la exposición ya ocurrida** |
| 2026-09-05 21:45 | Claude Code | Commit `33ddb00` en rama `sesion/revision-final-20260905`: 45 archivos, 5405 inserciones. Verificado sin secretos ni backups |
| 2026-09-05 21:45 | Claude Code | Todos los secretos consolidados en `.setenv.sh` (raíz, permisos 600, gitignored). Token retirado de `.git/config`; credential helper lee `GITHUB_TOKEN` del entorno |
| 2026-09-05 21:45 | Claude Code | `gemma4:12b-mlx_baseline` COMPLETADO (40/40 lotes). Descarga de `gemma4:31b-mlx` reanudada; `gemma4:31b` ya estaba local |
| 2026-09-06 04:35 | Claude Code | Progreso 348/1680 (20,7%). `gemma4:12b-mlx` COMPLETO (baseline y kb_rag 40/40). Contaminadas congeladas en 36 tras desactivar la suspensión: 22% → 10% |
| 2026-09-06 04:35 | Claude Code | Proyección revisada con latencias MEDIDAS: ~518 h (21 días). La estimación previa de 66 h partía de extrapolar el histórico N=15 y era 7× optimista |
| 2026-09-06 17:10 | Autor | Se aceptan **ambas formulaciones**: «Test de Variación de los Prompts» (títulos de sección) y «Análisis de Variantes de Prompts» (prosa corrida). Intercambiables; lo esencial es que ninguna use «ablación» |
| 2026-09-06 17:00 | Autor | Término definitivo **refinado**: **«Test de Variación de los Prompts»** (sustituye a «Análisis de Variantes de Prompt»). Prohibido en adelante «test de ablación de los prompts» y cualquier variante en español de ese término. Se aplica globalmente al final. Ver `TODO-INFORME-FINAL.md §13` |
| 2026-09-06 15:00 | Autor | Término definitivo elegido: **«Análisis de Variantes de Prompt»**. Se aplicará **globalmente al final**, cuando toda la evidencia esté generada. Registrado como tarea diferida en `TODO-INFORME-FINAL.md §13` |
| 2026-09-06 14:10 | Claude Code | Analizadas las 5 entregas remotas. **`gemma4:31b-cloud` es ahora el mejor modelo en N=120** (F1 0,6268, 240/240 `direct_json`, cero fallos). La **ablación regenera las 4 cifras que no existían en ningún dato**: fs-es 0,7444 · zs-es 0,6843 · zs-en 0,6405 · fs-en 0,6332 — el ranking de la tesina se mantiene |
| 2026-09-06 14:10 | Claude Code | Dos anomalías pasadas al remoto para investigar (§3.bis.7): `nemotron-mini:4b_baseline` con los únicos 8 `failed` de las 1680 filas, y `mistral-nemo` con salto de 9 a 69 `fallback` al activar RAG |
| 2026-09-06 13:00 | Claude Code | 🔴 Analizado a fondo el P3 remoto: bug de *thinking* confirmado con la misma firma (**203/206 respuestas vacías**). `kb_rag` falla más (78 %) que `baseline` (55 %) porque el contexto RAG alarga el prompt: **+22 % de latencia**. Su máquina de 48 GB alivia el síntoma (55 % vs nuestro 84 %) pero no lo cura |
| 2026-09-06 13:00 | Claude Code | Pedido **adelantar** la re-corrida de `gemma4:12b-mlx`: único modelo con datos a descartar íntegros, bloquea el ANOVA. Ver `URGENTE-REMOTO-RECORRIDA-20260906.md` |
| 2026-09-06 10:15 | Autor | Decisión: **delegar TODO lo pendiente al equipo remoto**. El equipo principal no ejecuta más corridas; su máquina queda libre y la corrida local se cierra donde está |
| 2026-09-06 10:15 | Claude Code | Tarea nueva para el remoto: `gemma4:31b-cloud` sobre N=120. Su corrida existente tiene **190/240 fallos (79 %)** y modo RAG legacy. Ver `ADENDA-EQUIPO-REMOTO-20260906.md` |
| 2026-09-06 09:30 | Autor | Decisión: **esperar la respuesta del equipo remoto** antes de relanzar nada en local, para no duplicar esfuerzo |
| 2026-09-06 09:30 | Claude Code | 🔴 Bugs de *thinking* corregidos y alerta enviada (`743054d`). La corrida local queda **DETENIDA a propósito**: reanudarla produciría datos inválidos para `gemma4:12b-mlx` y `qwen3:8b` |
| 2026-09-06 09:30 | Claude Code | Estado remoto al último pull: P1 y P2 completas (fallo 0), **P3 al 53% (885/1680)**, P2-gpt-oss y P4 en cola. Su último commit es anterior a la alerta |
| 2026-09-06 05:10 | Claude Code | Entrega remota integrada y verificada (0% fallo, protocolo correcto). ANOVA conjunto **9 modelos**: **F=64.0586, p=7.26e-177** (antes 5 modelos: F=10.21, p=2.87e-15). Ver `INFORME-AVANCE-20260906.md` |
| 2026-09-06 05:10 | Claude Code | 🔴 Bloqueante resuelto: `gemma4:31b` N=15 con dato propio (F1=0.6912), a 1.3 pp del 0.6783 que la Tabla 2 afirmaba sin respaldo |
| 2026-09-06 05:10 | Claude Code | Hallazgo nuevo: el KB RAG **beneficia a los modelos pequeños y perjudica a los grandes** (5 mejoran, 4 empeoran). `llama3.2` +0.0999; `gemma4:31b-mlx` −0.0018 |
| 2026-09-06 05:10 | Claude Code | Anomalía de `gemma4:12b-mlx` explicada: F1=0.0987 por **fallo de formato de salida**, no de comprensión (104/120 `fallback`, P=0.93 / R=0.14) |
| 2026-09-06 04:35 | Autor | Decisión: **esperar resultados parciales del equipo remoto**. La corrida local continúa como red de seguridad |
| 2026-09-05 21:45 | Claude Code | Suite de guardarraíles: 15/15 tests OK. `src/memory_stress_test.py` pospuesto para no competir por RAM con el benchmark |
| 2026-09-04 14:00 | Claude Code | Ref git inválida `refs/remotes/origin/main 2` eliminada: rompía `git log --all` y causó 2 escaneos de seguridad con falso negativo |
| 2026-09-03 16:38 | Claude Code | Inventario completo de resultados cloud: `gemma4:31b-cloud` y `minimax-m3:cloud` conservados en sus 2 corridas cada uno (N=15 y N=120). Detectado que ambas son de modo RAG legacy `entities`, no comparables con `kb_combined`. Ver `TODO-INFORME-FINAL.md §9.4-9.5` |
| 2026-09-03 20:18 | Claude Desktop | Tarea 2.0: protocolo añadido a `AGENT.md`, `ANTIGRAVITY.md` y `GEMINI.md` de la raíz; §2.4 (documentos de la sesión) y §2.5 (cierre de formato tras los benchmarks) |
| 2026-09-06 01:55 | Equipo Remoto 48 GB (Claude Code) | P1 §3.bis.1 COMPLETADA: `gemma4:31b` N=15. Pre-checks OK (15/120, 3605/1848/12000). Tasa de fallo 0/30. baseline F1=0.6912 / rag F1=0.6391. VRAM 18.8 GB. Entregado en `results/gemma4_31b_n15_REMOTO/`. P2 en curso. Al cerrar las 4: copiar a `remote_48g/results/` + push |
| 2026-09-06 02:25 | Equipo Remoto 48 GB (Claude Code) | Fix aprobado por el autor: `factory.py:46` ahora excluye tags Ollama (`:`) de la regla `gpt-*` → `gpt-oss:20b` rutea a Ollama. Backup `factory.py.bak_gptoss_routing_20260906`. Verificado (gpt-4o sigue OpenAI). Re-run de gpt-oss encolado tras P3/P4 con `--resume` |
| 2026-09-06 09:54 | Equipo Remoto 48 GB (Claude Code) | Tarea nueva §3.bis.6 `gemma4:31b-cloud` N=120 lanzada EN PARALELO. Implementado rate limit: flags `--max-workers` + `--request-delay` (`ollama_provider.py` gate por `OLLAMA_REQUEST_DELAY_SEC`). Con 1 worker + 3s: **0× 429** (vs 172 sin límite). Wrapper resiliente `--resume` (429=espera, 402=avisa). Backups `*.bak_ratelimit_20260906` |
| 2026-09-06 10:08 | Equipo Remoto 48 GB (Claude Code) | P3 §3.bis.3 COMPLETADA: 1680/1680, fallo 8/1680 (solo nemotron-mini baseline). `gemma4:12b-mlx`+`qwen3:8b` inválidos (bug thinking) → re-corrida aparte. P4 (ablación) arrancó. Cloud 234/240 |
| 2026-09-06 10:08 | Equipo Remoto 48 GB (Claude Code) | §3.bis.6 COMPLETADA: `gemma4:31b-cloud` N=120, 240/240, **fallo 0%**, F1 0.6238/0.6268. 10º modelo del ANOVA. Rate limit efectivo (0× 429 vs 79% fallo previo). Entregado en `results/gemma4_31b_cloud_n120_REMOTO/`. P4 en curso |
| 2026-09-06 10:35 | Equipo Remoto 48 GB (Claude Code) | P4 §3.bis.4 COMPLETADA: ablación 60/60, fallo 0. fs-es 0.7444 / zs-es 0.6843 / zs-en 0.6405 / fs-en 0.6332. CADENA local COMPLETA (P2-P4). gpt-oss:20b arrancó con el fix de routing (200 OK). Sigue re-corrida de afectados |
| 2026-09-06 16:46 | Equipo Remoto 48 GB (Claude Code) | §3.bis.7 RESUELTA: nemotron 8 failed = vacíos esporádicos inherentes del 4B (no thinking, no longitud; re-run deja 7/240 → excluir); mistral-nemo benigno. §3.bis.8: gemma4:12b-mlx re-run LIMPIO (F1 0.5618/0.5929); qwen3:8b re-corrida limpia en curso (los reinicios corrompieron cobertura). REPORTE-COMPLETO.md publicado en remote_48g/ |
| 2026-09-06 17:00 | Equipo Remoto 48 GB (Claude Code) | 🔴 HALLAZGO scoring: `evaluator.py:126-134` da F1=1.0 a extracción vacía sobre gold no-vacío (default 1.0 sin predicciones). Infla F1 de modelos débiles hasta +0.208 (nuextract kb_rag) / +0.150 (nemotron). No uniforme → sesga ranking. Afecta TODAS las corridas. Decisión del autor: documentar, no tocar scorer. Detalle: `remote_48g/HALLAZGO-SCORING-F1.md` |
| 2026-09-06 17:40 | Equipo Remoto 48 GB (Claude Code) | Hallazgo qwen3 thinking: comparación N=120 (P3 think OFF vs run limpio think ON) → F1 baseline idéntico 0.4483, kb_rag no mejor con think, solo más lento/vacíos. Decisión del autor: qwen3:8b a `think=False` (`ollama_provider.py`, backup `.bak_qwen3nothink_20260906`). Corrida limpia think=false en `results/qwen3_nothink_n120_REMOTO/`. Detalle: `remote_48g/HALLAZGO-QWEN3-THINKING.md` |
| 2026-09-06 17:55 | Claude Code (equipo principal) | 🟠 CORRECCIÓN enviada al remoto: el hallazgo qwen3 tenía la evidencia invertida (P3 era think **ON**, no OFF; 120/120 filas idénticas lo prueban). Efecto real de `think=False`: F1 +5,2 pp, `recall=0` 10→1, 10,3× más rápido. Decisión mantenida. Instrucciones en `CORRECCION-QWEN3-THINKING-20260906.md`; detalle en §3.bis.9 |
| 2026-09-06 17:58 | Equipo Remoto 48 GB (Claude Code) | §3.bis.8 COMPLETADA: qwen3:8b think=false 240/240, 0 failed, F1 0.4904/0.5313 (supera think=on y ~10× más rápido). Fuente de verdad definitiva en `results/qwen3_nothink_n120_REMOTO/`. TODOS los modelos N=120 completos y verificados. Set listo para merge+ANOVA |
| 2026-09-06 18:10 | Equipo Remoto 48 GB (Claude Code) | Bug scoring CORREGIDO sin re-inferir: `evaluator.py:126-134` (default 0.0; F1=1.0 solo si tp+fp+fn==0) + `tools/rescore_saved.py` re-puntúa desde tp/fp/fn guardados. Todas las corridas re-puntuadas (CSVs corregidos, backup .bak_prescore). Tabla F1 corregida en `remote_48g/HALLAZGO-SCORING-F1.md`. Cambios: nuextract kb_rag 0.43→0.22, nemotron 0.36→0.21; modelos limpios casi igual |
| 2026-09-06 18:15 | Equipo Remoto 48 GB (Claude Code) | CIERRE: revisión de integridad final OK (todas las corridas completas, 0 F1 anómalos, 0 dups, fallos solo nemotron esporádicos). Reporte final en `remote_48g/REPORTE-FINAL.md` con tabla F1 corregida definitiva. Ejecución 100% + scoring corregido. Set listo para merge+ANOVA. Pendientes solo decisiones de redacción del autor (§10 #1/#4/#6/#7) |
| 2026-09-06 18:25 | Equipo Remoto 48 GB (Claude Code) | nemotron 7 vacíos RESUELTOS: no era longitud/thinking/concurrencia/seed/framing sino artefacto del contexto batch (SystemMonitor). Re-extraídos vía OllamaProvider (params idénticos) con `tools/patch_nemotron_failed.py`, puntuados y parcheados en el CSV (backup .bak_prepatch). nemotron baseline 0.2150→0.2259, **0 failed en todas las corridas**. `data/nemotron_failed_subset.json` creado |
| 2026-09-06 18:35 | Equipo Remoto 48 GB (Claude Code) | Reporte de decisiones de redacción pendientes del autor en `remote_48g/DECISIONES-PENDIENTES-AUTOR.md`: A) sustituciones con dato limpio (Tabla 2 gemma4:31b 0.6912, variantes de prompt fs-es 0.7444, cloud 0.6238/0.6185); B) criterio/fuente (F1 legacy imposibles, cita KPMG, hardware §2.4, eficiencia §5.5). Ejecución 100% cerrada |
| 2026-09-07 00:15 | Equipo Remoto 48 GB (Claude Code) | Investigación B1-B4 (workflow 4 agentes, interno+web) en `remote_48g/INVESTIGACION-B1-B4.md`. B1: 2 F1 imposibles no recuperables (marcar/retirar; llama3.1:8b real N=120 0.4959/0.5491). B2: cifras RegTech no son KPMG sino Verified Market Research (15.68→87.17 mil M, CAGR 23.92%). B3: 31B (~24.7 GB) IMPOSIBLE en 16 GB (techo Metal ~75%=12 GB); 48 GB necesario y confirmado. B4: tabla §5.5 no reproducible; CSV canónico gemma4:31b-mlx=22.80/24607. Todo requiere decisión del autor salvo B3 |
| 2026-09-07 12:05 | Claude Code (equipo principal) | Convención de scoring UNIFICADA: re-puntuadas las 3 corridas legacy (199 filas degeneradas) con `tools/rescore_saved.py`. Barrido global: 8 927 filas, 0 violaciones, 0 degeneradas, 0 perdidas. **ANOVA conjunto** `results/ANALISIS_CONJUNTO_20260907/`: 14 modelos × 2 modos, F=36.3696, p=1.4321e-164. Publicado `results/AVISO-SUMMARIES-OBSOLETOS.md`. Corrección al remoto: B1 invertido (llama3.1:8b es 0.4876/0.5075, no 0.4959/0.5491) en `CORRECCION-B1-SUMMARIES-20260907.md` |
| 2026-09-07 00:30 | Equipo Remoto 48 GB (Claude Code) | Correcciones B1-B4 aplicadas al `.md` canónico + BENCHMARKS.md (backups .bak_B1B4/.bak_B1_20260907). B1: filas imposibles marcadas NO VERIFICABLES; llama3.1:8b oficial N=120 0.4876/0.5075. B2: cita RegTech → Verified Market Research 2022 (15.68→87.17 mil M, CAGR 23.92%; VMR verificado en web, no KPMG). B3: §2.4/§3.6/hardware reformulado a 16GB(≤12B)/48GB(31B). B4: tabla §5.5 reemplazada por valores CSV (gemma4:31b-mlx 22.80/24607). ⚠️ PENDIENTE Claude Desktop: propagar a .docx con docx_replace_terms.py y verificar 25pp |
| 2026-09-07 12:35 | Claude Code (equipo principal) | Aplicado el rescore extendido (`17c17fc`) a las 3 corridas legacy, que el remoto no cubrió (`e7eb541`). Backup real preservado como `.bak_prefix_ORIGINAL`. Verificado: 0 grupos cambian y `summary == CSV` en las 15 corridas. ANOVA sin recálculo |
| 2026-09-07 12:40 | Claude Code (equipo principal) | Verificadas las entregas `38b20da` (B1-B4) y `17c17fc` (rescore extendido): las 3 filas de §5.5 reproducen exacto; B1 adopta 0.4876/0.5075. Dos avisos: el `.md` creció +18/−8 líneas (re-verificar 25 pp) y la atribución del B1 a «decisión del autor» es incorrecta. Registrado el test `think=off` de 5 modelos en §3.bis.10 |
| 2026-09-07 13:20 | Claude Code (equipo principal) | 📌 HALLAZGO FINAL sobre *thinking*: verificado el experimento del remoto (§F44) y añadido `FINDINGS.md §F45`. `gpt-oss` ON congelado (deja de responder sin razonamiento) y `qwen3` OFF son los únicos casos sólidos; los otros 4 son ruido de N=15. **Decisión cerrada: no re-ejecutar.** Reglas para ejecuciones futuras en `RECOMENDACIONES-EJECUCIONES-FUTURAS.md` y anexo `TODO-INFORME-FINAL.md §14`. Instrucciones al remoto en §3.bis.11 |
| 2026-09-07 13:50 | Claude Code (equipo principal) | 🔒 **CIERRE DE BENCHMARKS** (decisión del autor): se conservan los 13 modelos y se cierra la ejecución. Alcance final 13 modelos × 2 modos, F=36.3666, p=1.2236e-152. Integridad: 0 violaciones, 0 degeneradas, 0 failed, summary==CSV. Documento `CIERRE-BENCHMARKS-20260907.md` y `TODO-INFORME-FINAL.md §15`. Aviso: el «12» del informe es la Tabla 2 (N=15), no el estudio N=120 |
| 2026-09-07 14:30 | Claude Code (equipo principal) | Aplicadas A1-A3 y la reconstrucción de la Tabla 2 al `.md` canónico; §5.2 con las cifras limpias (nueva lectura: interacción idioma × few-shot, +11.12 pp); §5.3.5 reescrita con los 13 modelos (F=36.3666, p=1.2236e-152, Tukey: RAG significativo solo en nemotron y llama3.2); renombrado terminológico ejecutado (§13 cerrado); aclarado 12 (Tabla 2) vs 13 (estudio N=120). Encargo a Claude Desktop en `PROMPT-CLAUDE-DESKTOP-20260907.md` y §2.6 |
| 2026-09-07 14:55 | Claude Code (equipo principal) | 🔴 §3.bis REABIERTA solo para la corrida N=30 (decisión del autor): el F1 titular 79.03 % es la única cifra aún bajo el scorer defectuoso y su dato por registro se perdió. Encargo en `ENCARGO-REMOTO-N30-20260907.md` y §3.bis.12. ETA ~9 h. Ninguna otra corrida se reabre |
| 2026-09-07 15:25 | Claude Code (equipo principal) | 🔬 §3.bis.13: diagnóstico de `gpt-oss:20b` encargado al remoto. Los 76 `recall=0` NO son rechazo de infraestructura: 67 son `fallback`, 69 avisos de parseo JSON fallido y latencia normal. Hipótesis: degeneración por repetición que deja el JSON sin cerrar (2 muestras del log lo muestran). Se pide además buscar allí los datos perdidos de N=30 y verificar el mojibake, que podría afectar a todos los modelos. Encargo: `ENCARGO-REMOTO-GPTOSS-20260907.md` |
| 2026-09-07 14:00 | Equipo Remoto 48 GB (Claude Code) | Encargos nuevos recibidos (N30 + GPTOSS). Parte A: NO sobreviven datos N=30 por registro → re-run necesario. 🔴 F46: mojibake en gold N=120 (283/1406 con mojibake, 66=4.7% irrecuperables → recall subestimado en TODOS los modelos; kleptotrace/N30 limpios). GPT-OSS es PRIORITARIO (autor): diagnóstico en curso (bucle de repetición + repeat_penalty + mojibake). N30 pausado (reanudable) hasta cerrar gpt-oss. L38: logs con fecha/hora. Push tras gpt-oss para actualizar tesina |
| 2026-09-07 15:50 | Claude Code (equipo principal) | Tareas locales de cierre: salvedades de procedencia añadidas a §5.3.5 del informe (latencia del cloud y telemetría de nemotron), `FINDINGS.md §F46` (gpt-oss: degeneración por repetición, no incapacidad), `RUNS_INDEX.md` con las 12 corridas del cierre y el análisis conjunto, entrada de sesión en `research/rag/WORKLOG.md`, casillas superadas marcadas en TODO y §1.2 cerrada (los 31B están descargados pero no caben en 16 GB) |
| 2026-09-07 14:35 | Equipo Remoto 48 GB (Claude Code) | §3.bis GPTOSS diagnóstico COMPLETO: bucle de repetición NO reproducido (0/5), repeat_penalty irrelevante. Las 5 filas recall=0 recuperan output válido al re-ejecutar → artefacto de corrida (posible truncación por thinking), no del modelo. Mojibake (F46) contribuye y afecta a TODO el N=120. Recomendación: re-ejecutar gpt-oss completo con thinking ON + num_predict 4096 + parser tolerante + gold sin mojibake; ETA ~1-1.5h. Decisión del autor. Reporte: `remote_48g/DIAGNOSTICO-GPTOSS-20260907.md` + raw en `results/diag_gptoss.json` |
| 2026-09-07 16:35 | Claude Code (equipo principal) | Analizado a fondo el mojibake: **el defecto está también en el texto de entrada** (87 % de artículos) y de forma coherente con el gold → el sesgo **no es uniforme**, premia la transcripción literal y penaliza la normalización (Δ por modelo de −0.070 a +0.091). `FINDINGS §F48`, `LEARNING §L39 y §L40`, nota de verificación bajo el §F46 del remoto, y corrección de la limitación en §5.3.5 del informe (ya no afirma uniformidad). Adenda al encargo de gpt-oss: re-ejecutar con `num_predict=4096` **sin tocar gold ni evaluador**, para que el cambio quede aislado a ese modelo. Decisiones en `TODO §15.5`. Forma corrupta `JosÃ© Bono` → correcta **`José Bono`** |
| 2026-09-07 17:25 | Claude Desktop | Tarea 2.6 completada: los tres `.docx` sincronizados con el `.md` sin pandoc, §4.1.3/§5.3.5 reinsertadas en el standalone, salvedades declaradas, cuerpo verificado en 21 pp. y versión `_v2` congelada |
| 2026-09-07 17:40 | Claude Code (equipo principal) | Commiteado el trabajo de Claude Desktop (§2.6, su puente no tiene permiso de escritura en git). **Atendida su observación**: el `.md` conservaba la lectura antigua del análisis de variantes en **tres** sitios —resumen en inglés, Hallazgo 4 de §5.2 y discusión §6.2— y no en uno; los tres alineados con la tabla nueva (+11.12 pp por interacción). Cero ocurrencias restantes de la cifra antigua. `.md` y `.docx` quedan coherentes |
| 2026-09-07 17:55 | Claude Code (equipo principal) | ✅ Decisión del autor: **el mojibake se declara como limitación y su normalización pasa a TRABAJO FUTURO**; no se re-ejecuta el estudio. Añadido el punto 7 a §7.2 del informe (Fase 6), resueltas §15.4/§15.5 y registrada §15.6. Reglas operativas R9-R12 en `RECOMENDACIONES-EJECUCIONES-FUTURAS.md`. Nueva tarea §2.7 para Claude Desktop: propagar ese único párrafo |
| 2026-09-07 14:08 | Equipo Remoto 48 GB (Claude Code) | Decisiones del autor: (1) gpt-oss re-run completo APROBADO — encolado tras N30 (`gptoss_rerun_REMOTO`, N=120 kb_combined, thinking ON, num_predict 4096 para evitar truncación). (2) Corrección de mojibake N=120 (F46) = TAREA FUTURA (exige re-inferir). Orden: N30 (en curso) → gpt-oss re-run. Logs fechados (L38) |
| 2026-09-07 14:12 | Equipo Remoto 48 GB (Claude Code) | §3.bis.9 registrada como TAREA FUTURA del equipo remoto 48 GB: corregir mojibake del gold N=120 (F46) y RE-INFERIR el estudio + re-fusionar ANOVA (las extracciones crudas no se persistieron). Requiere 48 GB por los 31B. N30 en curso; gpt-oss re-run encolado |
| 2026-09-07 14:43 | Equipo Remoto 48 GB (Claude Code) | N30 re-run COMPLETADO (0 failed, direct_json): gemma4:31b F1=0.7855 (P0.733 R0.883), gemma4:31b-mlx F1=0.8057. Reemplaza el titular 79.03% con scorer corregido y dato por registro. gpt-oss re-run arrancó (tras N30). L39+zip: estudio completo archivado en `remote_48g/estudio_completo_20260907.zip` (versionado, no gitignored) para evitar re-inferir en el futuro |
| 2026-09-07 15:01 | Equipo Remoto 48 GB (Claude Code) | gpt-oss re-run EN CURSO 42/240, **0 failed, recall0=2** (vs 76 en la oficial) — el num_predict 4096 confirma que el recall=0 era truncación por thinking, no bucle. Snapshot parcial en remote_48g/ |
| 2026-09-07 18:10 | Claude Code (equipo principal) | Hallazgo de codificación elevado al informe: **conclusión 7** en §7.1 y **Anexo H** completo (H.1-H.6: qué es el mojibake a nivel de bytes, alcance medido, por qué la lectura inicial era incorrecta, evidencia diferencial por modelo, cómo repararlo y cuatro implicaciones para evaluar NER). Detectado de paso que la **corrección de la convención de puntuación no estaba documentada** en el informe pese a afectar a todas las cifras: añadida a §4.4 junto con el umbral de cotejo difuso. §2.7 ampliada a cuatro cambios |
| 2026-09-07 19:10 | Claude Code (equipo principal) | Atendidos los 4 reparos del profesor guía en el `.md`: ficha fuera, 12 separadores eliminados, resumen a 201 palabras, capítulo 2 reescrito con comparación de familias y criterios C1-C5, capítulo 3 justificando la elección frente a ellos, capítulos 3/6 y §5.6 consolidados, introducción desarrollada. Encargo a Desktop en `PROMPT-CLAUDE-DESKTOP-PROFESOR-20260907.md` y §2.8, con el Anexo G (uso de IA) declarado INTOCABLE y la medición real de páginas como tarea crítica |
| 2026-09-07 16:45 | Claude Code (equipo principal) | Actualizado el encargo a Claude Desktop (`PROMPT-CLAUDE-DESKTOP-PROFESOR-20260907.md`, §2.8): separado en tanda **estructural** —firme, propagable ya— y tanda **de datos** —pendiente de que `gpt-oss` cierre 201/240—. Incorporada la re-corrida N=30 y reescrita §5.3. Instrucción explícita de **no congelar versión** hasta la segunda pasada |
| 2026-09-07 17:00 | Claude Code (equipo principal) | Puesta al día de CURRENT-TASKS: §3.bis.12 (N=30) **COMPLETADA** y verificada · §3.bis.13 pasa a re-ejecución de `gpt-oss` en curso (201/240, baseline 0.4384→0.5239, 1 `fallback` de 201) · notas de cierre en §3.bis.0, §3.bis.8 y §3.bis.10 sin alterar su texto original · resuelta la **colisión de numeración**: el §3.bis.9 del mojibake pasa a **§3.bis.14** · declarada §1.4, la revisión pedida por el profesor guía |
| 2026-09-07 19:50 | Claude Desktop | Tarea 2.8 (tanda estructural) y 2.7 propagadas a los tres `.docx` reconstruyendo el cuerpo desde el `.md`; anexos D–G llevados al `.md`; **cuerpo medido: 23 páginas de 25**; sin congelar versión |
| 2026-09-07 20:05 | Claude Desktop | Diagramas de texto convertidos en tablas de Word en el `.md` y propagados a los tres `.docx` (§3.2, §4.3.1, flujos RAG de §5.6, árbol del Anexo A); cuerpo re-medido en 23 páginas |
| 2026-09-07 17:02 | Equipo Remoto 48 GB (Claude Code) | gpt-oss re-run COMPLETO (num_predict 4096, thinking ON): 240/240, 0 failed, F1 baseline 0.5239 / kb_rag 0.5567 (vs oficial 0.4467/0.3419), recall0 11 (vs 76), ΔRAG +0.033 (era −0.097). Confirma truncación. `gptoss_rerun_REMOTO` = fuente de verdad; requiere re-fusionar ANOVA. Entregado en remote_48g/ |
| 2026-09-07 17:25 | Claude Code (equipo principal) | `gpt-oss` COMPLETO y verificado (0 failed, 238/240 `direct_json`): ΔRAG −0,097 → **+0,033**, era artefacto de truncamiento. **ANOVA rehecho: F=38,2222 · p=3,4453e-160**, 10 de 13 modelos con ΔRAG positivo. Actualizados §5.3.5, Tukey, y el **Anexo H** (delta de `gpt-oss` +0,0914 → −0,0336; rango 16 → 9,4 pp). Commiteada la tanda estructural de Claude Desktop: **cuerpo de 23 páginas de 25 medidas**, anexos A-H, Anexo G íntegro, 0 arte ASCII. Documentada la **regla de no usar arte ASCII** en `CLAUDE.md` y en el encargo. Abierta §2.9 para la segunda tanda |
