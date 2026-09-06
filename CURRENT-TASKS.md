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

### 1.0 ⏳ EN ESPERA — Resultados parciales del equipo remoto
- **Decisión del autor (2026-09-06):** esperar los resultados parciales del equipo de 48 GB antes de
  decidir el alcance final del estudio.
- **La corrida local sigue viva como red de seguridad**, sin bloquear nada. Ver 1.1.
- **Motivo:** con latencias ya medidas (no estimadas), la proyección local es de **~518 h ≈ 21 días**.
  `qwen3:8b` mide **1360 s/artículo** frente a los 192 s que se habían estimado desde su histórico N=15:
  los artículos de N=120 son mucho más largos y la máquina pagina.
- **Qué se espera del remoto:** la tarea de prioridad 3 del encargo es exactamente esta corrida.

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
- **Excluidos:** `sonct988` (16 GB) y `gpt-oss:20b` (13 GB) por RAM de 16 GB; `gemma4:31b-cloud` (HTTP 429)
  y `minimax-m3:cloud` (HTTP 402)
- **ETA:** ~66 h de cómputo neto (más el tiempo perdido en suspensiones).
- **Ejecución (2026-09-04):** migrada a **LaunchAgent de macOS** `local.tesina.benchmark`
  (`~/Library/LaunchAgents/local.tesina.benchmark.plist`) con `KeepAlive`, tras 7 interrupciones del
  ejecutor lanzado desde la sesión. macOS lo reinicia solo y `--resume` retoma desde el checkpoint.
  Para detenerlo: `launchctl unload ~/Library/LaunchAgents/local.tesina.benchmark.plist`
- ⚠️ **Calidad de datos:** 8 suspensiones del equipo (~4.6 h) contaminaron 2 de 48 latencias con valores
  imposibles (9548 s y 15860 s). Media con anómalas 1245 s vs 747 s sin ellas. Requiere `sudo pmset -a
  disablesleep 1` o filtrar los outliers y documentarlo.

### 1.2 PAUSADA — Descarga de modelos 31B para recuperar N=30
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

> **Encargo completo:** [`PROMPT-EQUIPO-REMOTO-48GB.md`](./PROMPT-EQUIPO-REMOTO-48GB.md)
> **Motivo:** la máquina de desarrollo tiene 16 GB y varios modelos no caben (ver `FINDINGS.md §F36`).
> **Protocolo:** el equipo remoto debe **leer este documento antes de empezar**, escribir su entrada al
> iniciar cada tarea, actualizarla al terminar y **volver a leerlo** por si otro agente escribió mientras.

### 3.bis.0 🔴 URGENTE — Re-corrida de `gemma4:12b-mlx` (SUBIR DE PRIORIDAD)
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
- **`sonct988/gemma4-26b-a4b-it-q4km-256k` ✅:** 240 filas, tasa de fallo 0.
  baseline F1=0.5627 P=0.5233 R=0.7171 · kb_rag F1=0.5964 P=0.5297 R=0.7608. RAG `kb_combined` confirmado.
- **`gpt-oss:20b` ❌ BLOQUEADO:** 0 filas. **Bug de enrutado**, no de RAM: `factory.py:46` manda todo
  `gpt-*` a `OpenAIProvider`; `gpt-oss:20b` es Ollama local. Error:
  `OpenAIProvider.extract_entities() got an unexpected keyword argument 'rag_context'`.
  AGENTS.md §8.2 lo clasifica «Local/Active» (contradice la fila `gpt-*→OpenAI` de la misma tabla).
- **Efecto actual:** estudio de 12 → **13** modelos (con sonct988). Falta gpt-oss para llegar a 14.
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

### 3.bis.7 🔍 PARA INVESTIGAR — dos anomalías detectadas en P3
Detectadas por el equipo principal al analizar `benchmark_n120_REMOTO`. **El equipo remoto investiga.**

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
| 2026-09-03 16:24 | Claude Code | Exclusión de `sonct988` y `gpt-oss:20b` documentada en `FINDINGS.md §F23-F24`, `LEARNING.md §L14-L15`, `TODO-INFORME-FINAL.md §8` y `research/rag/WORKLOG.md` |
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
| 2026-09-06 02:19 | Equipo Remoto 48 GB (Claude Code) | P2 §3.bis.2 PARCIAL: `sonct988` OK (fallo 0, F1 0.5627/0.5964). `gpt-oss:20b` bloqueado por bug de routing (`gpt-*`→OpenAIProvider). Estudio 12→13 |
| 2026-09-06 02:25 | Equipo Remoto 48 GB (Claude Code) | Fix aprobado por el autor: `factory.py:46` ahora excluye tags Ollama (`:`) de la regla `gpt-*` → `gpt-oss:20b` rutea a Ollama. Backup `factory.py.bak_gptoss_routing_20260906`. Verificado (gpt-4o sigue OpenAI). Re-run de gpt-oss encolado tras P3/P4 con `--resume` |
| 2026-09-06 09:04 | Equipo Remoto 48 GB (Claude Code) | Leída ALERTA-EQUIPO-REMOTO-20260906: bug thinking invalida `gemma4:12b-mlx` (recall=0 66-94/120) y `qwen3:8b` en P3. Fix `743054d` ya en árbol. Decisión del autor: dejar P3 terminar (5 modelos válidos) y re-correr los 2 afectados con el fix en `results/afectados_thinking_n120_REMOTO/` (encolado tras gpt-oss). Analizado también INFORME-AVANCE-20260906 (ANOVA 9 modelos F=64.06; sonct988 lidera) |
| 2026-09-06 09:54 | Equipo Remoto 48 GB (Claude Code) | Tarea nueva §3.bis.6 `gemma4:31b-cloud` N=120 lanzada EN PARALELO. Implementado rate limit: flags `--max-workers` + `--request-delay` (`ollama_provider.py` gate por `OLLAMA_REQUEST_DELAY_SEC`). Con 1 worker + 3s: **0× 429** (vs 172 sin límite). Wrapper resiliente `--resume` (429=espera, 402=avisa). Backups `*.bak_ratelimit_20260906` |
| 2026-09-06 10:08 | Equipo Remoto 48 GB (Claude Code) | P3 §3.bis.3 COMPLETADA: 1680/1680, fallo 8/1680 (solo nemotron-mini baseline). `gemma4:12b-mlx`+`qwen3:8b` inválidos (bug thinking) → re-corrida aparte. P4 (ablación) arrancó. Cloud 234/240 |
| 2026-09-06 10:08 | Equipo Remoto 48 GB (Claude Code) | §3.bis.6 COMPLETADA: `gemma4:31b-cloud` N=120, 240/240, **fallo 0%**, F1 0.6238/0.6268. 10º modelo del ANOVA. Rate limit efectivo (0× 429 vs 79% fallo previo). Entregado en `results/gemma4_31b_cloud_n120_REMOTO/`. P4 en curso |
| 2026-09-06 10:35 | Equipo Remoto 48 GB (Claude Code) | P4 §3.bis.4 COMPLETADA: ablación 60/60, fallo 0. fs-es 0.7444 / zs-es 0.6843 / zs-en 0.6405 / fs-en 0.6332. CADENA local COMPLETA (P2-P4). gpt-oss:20b arrancó con el fix de routing (200 OK). Sigue re-corrida de afectados |
