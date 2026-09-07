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

### 2.12 🟡 ÚNICA TAREA VIGENTE — Propagar a los `.docx` y congelar `_v4`
> **Sustituye y agrupa a §2.7, §2.10 y §2.11**, que se conservan abajo como registro. El encargo completo, ya
> reescrito como documento único, está en
> [`PROMPT-CLAUDE-DESKTOP-PROFESOR-20260907.md`](./PROMPT-CLAUDE-DESKTOP-PROFESOR-20260907.md).

- **Qué:** llevar a los tres `.docx` todo lo que el `.md` acumula desde la `_v3`, **medir** y congelar `_v4`.
- **Contenido a propagar:** conversión a prosa de §3.1, §4.2, §5.4 y el ANOVA de §5.3.5 · consolidación de
  §4.3 (4 subsecciones → 0), de §4.1.1+§4.1.2 y de §4.5 dentro de §4.4 · **capítulo 2 de 6 a 4 subsecciones y
  capítulo 3 de 4 a 3** · URL del repositorio en el Anexo A · registro suavizado.
- ⚠️ **Los nueve capítulos siguen existiendo.** Solo se consolidó el nivel de subsección; la estructura que
  exige la plantilla se mantiene intacta.
- ⚠️ **Referencias renumeradas — verificar en el `.docx`:** §2.2→§2.1 · §2.5→§2.3 · §3.3→§3.2 · §3.4→§3.3.
  En el `.md` están corregidas y verificadas (0 rotas).
- **Estado del `.md`:** cuerpo **10 937 palabras · 9 tablas · ≈19,9 páginas** (medidas en `_v3`: 20) ·
  anexos 3 151 palabras y 10 tablas · resumen 198 palabras de 200.
- **Intocables:** **Anexo G** (declaración de uso de IA) y **Anexo H**, íntegros · las **nueve tablas** del
  cuerpo, incluidas §5.1 y §5.3.5 · **nada de arte ASCII** · **sin pandoc** · corregir **siempre primero el
  `.md`**.
- **Al terminar:** conteo de páginas medido en §2, `_v4` congelada en `doc/versions/informe_final/` y copia
  del `.docx` canónico en la raíz.

### 2.11 🟡 PENDIENTE — Quinta tanda: capítulos 2 y 3 consolidados + URL del repositorio
> 📎 *Agrupada en §2.12; se conserva como registro.*
| 2026-09-07 19:30 | Claude Code (equipo principal) | Encargo a Claude Desktop **reescrito como documento único** (llevaba cinco tandas apiladas) y tareas agrupadas en **§2.12, la única vigente**: propagar lo acumulado desde la `_v3`, medir y congelar `_v4`. §2.7, §2.10 y §2.11 quedan como registro. Aclarado que **los nueve capítulos siguen existiendo**: solo se consolidó el nivel de subsección |
