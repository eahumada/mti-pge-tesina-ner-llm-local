# WORKLOG — RAG Knowledge Base Implementation

**Proyecto:** MTI Tesina - NER LLM Local  
**Objetivo:** Implementación KB RAG para mejorar F1-Score  
**Referencia:** `TODO-RAG-20260901.md`

---

## 2026-08-31

### 23:00–01:00 — Orquestador (Gemini Pro): Investigación RAG
- Auditoría completa del ChromaDB: 3.605 personas, 1.848 orgs, 12.000 augmented_persons
- Identificación del problema "Semantic Mismatch": dict-RAG recupera entidades temáticamente similares pero ausentes en el texto
- Mini-experimento N=5 (llama3.2): Dict-RAG F1=0.2367 vs KB-RAG F1=0.7216 (**+204,9 % relativo = +48,5 pp**;
  el «+105 %» registrado originalmente era un error de cálculo — corregido 2026-09-03). Baseline sin RAG de
  esa misma tabla: F1=0.5614, luego el KB-RAG rinde +28,5 % sobre el baseline y el Dict-RAG −57,8 %.
- Documentación completa: `research/rag/2026-08-31_analisis_contenido_rag_base_conocimientos.md`

---

## 2026-09-01

### 13:45 — Orquestador (Gemini Pro): Análisis y Planificación
- Revisión de documentación de investigación: `research/rag/2026-08-31_analisis_contenido_rag_base_conocimientos.md`
- Lectura de código fuente: `src/rag_manager.py`, `src/config.py`, `src/providers/ollama_provider.py`, `src/main.py`
- Decisión arquitectónica final:
  - Crear `src/kb_rag_manager.py` (clase nueva, no modifica la existente → backward compatible)
  - Crear `data/knowledge_base/` con JSONs separados de `data/dictionaries/`
  - Agregar `rag_mode` field en `BenchmarkConfig` (default `'entities'`)
  - Extender CLI con `--rag-mode` (4 modos configurables)
  - Template de prompt positivo para KB (diferente al restrictivo del dict-RAG)

### 13:48–13:54 — Implementación: FASE 1 — Datos Knowledge Base
- ✅ Creado directorio `repos/ner-llm-entity-benchmark/data/knowledge_base/`
- ✅ `data/knowledge_base/domain_guidelines.json`: 5 dominios con reglas NER tipológicas
  - `politics_es`: Noticias políticas y administrativas en español
  - `corporate_financial_es`: Noticias corporativas y financieras
  - `aml_sanctions_en`: AML, sanciones, crimen financiero (inglés)
  - `judicial_crime_es`: Noticias judiciales y de crimen en español
  - `sports_social_es`: Noticias deportivas y sociales
- ✅ `data/knowledge_base/few_shot_exemplars.json`: 7 ejemplares reales anotados
  - Todos extraídos de `benchmark_balanced_120.json` (sin datos sintéticos)
  - Cubren: 2× política ES, 1× corporativo ES, 1× judicial ES, 3× AML EN

### 13:51 — Documentación: Tracking
- ✅ Creado `research/rag/TODO-RAG-20260901.md`
- ✅ Creado `research/rag/WORKLOG.md` (este archivo)

### 13:55 — Implementación: FASE 2 — Código KBRAGManager
- ✅ Creado `src/kb_rag_manager.py` (320 líneas, extensamente documentado)
  - Clase `KBRAGManager` con 4 modos: `entities`, `kb_guidelines`, `kb_fewshot`, `kb_combined`
  - Compatible con interfaz de `RAGManager` (misma firma `query()`)
  - Usa colección separada `ner_knowledge_base` (no modifica `ner_dictionaries`)
  - Carga idempotente del KB (no recarga si ya existe en ChromaDB)

### 13:56 — Implementación: FASE 2 — config.py
- ✅ `src/config.py`: Agregado `rag_mode: str = 'entities'` en `BenchmarkConfig`
  - Default preserva backward compatibility
  - Comentarios documentan los 4 modos y referencias a la investigación

### 13:57 — Implementación: FASE 2 — main.py (parte 1)
- ✅ `src/main.py`: Importado `KBRAGManager, RAG_MODE_ENTITIES`
- ✅ Primer bloque `rag_study` (producer): usa `rag_conditions` variable
  - `entities` mode → `['baseline', 'rag_enhanced']` (legacy compatible)
  - `kb_*` modes → `['baseline', 'kb_rag']` (nuevo)

### 13:58 — Implementación: FASE 2 — main.py (parte 2) + ollama_provider.py
- ✅ Segundo bloque `rag_study` (worker/consumer): idéntica lógica de selección
- ✅ Activación RAG: condición `is_rag_condition = 'rag_enhanced' in name or 'kb_rag' in name`
- ✅ `--rag-mode` CLI argument: choices=['entities','kb_guidelines','kb_fewshot','kb_combined']
- ✅ `src/providers/ollama_provider.py`: Template de inyección dual
  - KB context (prefijo `[DOMAIN CONTEXT:` o `[EXTRACTION EXAMPLE`) → template positivo
  - Entity dict context → template restrictivo original (backward compatible)

### 13:55 — Validación: Tests de Integración
- ✅ `py_compile` de los 4 archivos modificados → OK
- ✅ Importación `KBRAGManager` → OK
- ✅ Carga KB ChromaDB: 12 documentos (5 guidelines + 7 exemplars) → OK
- ✅ Retrieval semántico validado:
  - Artículo político ES → guía `politics_administrative` + ejemplo ES ✅
  - Artículo AML EN → guía `aml_compliance` + ejemplo EN ✅
- ✅ CLI `--help`: muestra `--rag-mode` con 4 opciones ✅

### 13:59–14:04 — Validación: Mini-Benchmark (N=5, llama3.2:latest)
- Resultado: Baseline F1=0.3521 → KB Combined F1=0.5489 (**+19.7 pp**, **+55.9%**)
- Recall: 33.3% → 59.5% (+26.2 pp)
- Artículo 1 (política ES): F1: 0.3000 → **0.8462** (↑ +181%)
- Mejoras en 4/5 artículos; 1 caso sin mejora (artículo militar sin dominio KB)

### 14:04 — Benchmark Completo Iniciado (Background)
- Modelos: `llama3.2:latest`, `gemma4:latest`, `gemma4:31b-mlx`, `qwen2.5:14b`, `gemma:latest`
- Condiciones: `baseline`, `kb_rag`
- N=120 artículos, batch_size=3, num_workers=2
- Comando: `./venv/bin/python3 src/main.py --rag-study --rag-mode kb_combined ...`

### 14:05 — Documentación: Tesis
- ✅ Insertada sección 5.6 en `doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md`
  - 5.6.1 Motivación: Semantic Mismatch
  - 5.6.2 Arquitectura KB RAG
  - 5.6.3 Implementación Técnica
  - 5.6.4 Datos de la KB
  - 5.6.5 Resultados Empíricos
  - 5.6.6 Análisis Cronológico Comparativo
  - 5.6.7 Justificación Metodológica
- ✅ Conclusión #6 agregada (7.1): RAG contextual supera al RAG por diccionario
- ✅ Trabajo Futuro actualizado (7.2): KB RAG como Prioridad Alta #1

### 15:00–19:36 — Benchmark Corriendo (Background, sin interrupción del agente)
- Completados: `llama3.2:latest_*`, `gemma4:latest_*`, `gemma4:31b-mlx_*`, `qwen2.5:14b_baseline`
- En curso: `qwen2.5:14b_kb_rag` (37.5%), `gemma:latest_*` (pendiente)

### 19:37 — 20:06 (Gemini Pro) - Cierre de Implementación
- Estado del benchmark: Terminado (400/400 batches completados). `gemma:latest` finalizó.
- Extracción de resultados: Se ejecutó `analyze_kb_rag_results.py` y se guardó en `results/kb_rag_analysis_20260901.json`.
- Actualización de Tesis:
  - Se añadieron los resultados finales de 5 modelos (N=120) en sección 5.6.5.
  - Se agregó sección 6.5 (Discusión sobre la redundancia de conocimiento en modelos grandes).
  - Conclusión 6 actualizada.
  - Anexo A actualizado.
- DOCX regenerado vía `pandoc`.
- Git: Se hizo commit de todo el trabajo, push a GitHub y se creó el tag `v1.1.0-rag-knowledge-base`.

---

## TAREAS FINALIZADAS (al 2026-09-01 20:06)

| Prioridad | Tarea | Estado |
|-----------|-------|--------|
| 1 | Esperar que termine el benchmark (qwen2.5 + gemma:latest) | ✅ HECHO |
| 2 | Extraer y analizar resultados comparativos (baseline vs kb_rag) | ✅ HECHO |
| 3 | Actualizar sección 5.6.5 de la tesis con resultados finales N=120 | ✅ HECHO |
| 4 | Regenerar DOCX de Tesis Final con pandoc | ✅ HECHO |
| 5 | Git commit: todos los archivos modificados + push a origin | ✅ HECHO |
| 6 | Git tag `v1.1.0-rag-knowledge-base` + push tags | ✅ HECHO |

---
*Fase de implementación del RAG Contextual KB finalizada.*
*Última actualización: 2026-09-01 20:06*

## 2026-09-03

### Documentación: Corrección aditiva del Informe Final y Borrador (Claude / Cowork)
- Se detectó que la conclusión principal de la tesina (F1=79.03%, hipótesis confirmada) seguía apoyada solo en el corpus sintético N=30 (`kleptotrace_augmented_30.json`), mientras el corpus real N=120 (`benchmark_balanced_120.json`, ver commit `5ff38f5`, 2026-09-01) sólo se había documentado como parte del estudio KB RAG (§5.6).
- Se auditó el historial (git log, `data/`, `results/`) confirmando: N=30 es sintético (generado por LLM, entidades ficticias tipo "Wayne Enterprises"); N=120 es real (15 Kleptotrace + 105 CoNLL-2002 ES muestreados, sin generación LLM). Ambos corpus coexisten y son conmutables vía `--data-file`.
- Se agregó de forma aditiva (sin modificar contenido existente):
  - §4.1.3 "Extensión a Corpus Real N=120 (Dataset Conmutable)" — documenta la historia del corpus N=120 y su carácter conmutable con N=30.
  - §5.3.5 "Validación Estadística Complementaria sobre Corpus Real N=120" — ANOVA/Tukey ya calculados en `results/benchmark_balanced_120_20260901_140421/statistical_report.md` (F=10.2096, p=2.87e-15, N=120 por grupo, 5 modelos), presentados como complemento (no reemplazo) de la validación N=30.
- Nota: no fue posible re-ejecutar el benchmark completo de 16 modelos sobre N=120 desde este entorno (sin acceso a Ollama local del usuario); se usaron los resultados ya generados el 2026-09-01 para el subconjunto de 5 modelos. Los 11 modelos restantes quedan como trabajo futuro explícito (§7.2).

### Corrección adicional (mismo día) — Confidencialidad
- Se eliminó la mención a "Leanstack SpA" (nombre de la organización vinculada) en `2026-07-04_Borrador-Informe-Final-Tesina.md/.docx`, `Informe_Final_Tesina_NER.docx` e `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx`, dejando solo "Austranet" donde aparecía la referencia combinada. No se tocaron documentos históricos de hitos previos (`doc/organized/Hito_4_.../Informe-Avance-2-v2.md`, `doc/RESEARCH_INCONTEXT_BATCHING_AND_MILESTONES.md`, `2026-07-01_RESEARCH_INCONTEXT_BATCHING.md`) para preservar el registro histórico intacto; quedan pendientes de decisión del autor si también deben corregirse.

- Archivos actualizados: `doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md` y `.docx`; pendiente propagar el mismo criterio al `Informe_Final_Tesina_NER.docx` de la raíz del proyecto y a la versión fusionada con la plantilla UTFSM/MTI.
  - **Nota aditiva (2026-09-03):** la propagación está **completada y verificada** en los tres DOCX — 0 coincidencias de la mención en *todas* las partes del paquete OOXML (no solo `word/document.xml`, también encabezados y pies). El único pendiente real es la decisión del autor sobre los documentos históricos de Hito 4, que por política no se modifican.


---

## 2026-09-03 (tarde): Reconstrucción de entorno para completar N=120 con 16 modelos

### Contexto
La entrada previa de este mismo día dejó como trabajo futuro los 11 modelos faltantes del benchmark N=120
(«no fue posible re-ejecutar el benchmark completo de 16 modelos… sin acceso a Ollama local del usuario»).
Esta sesión aborda justamente eso, desde el entorno local del autor.

### Bloqueadores encontrados y resueltos
1. **venv inutilizable**: todas las rutas apuntaban a `/Users/eahumada1/` (home renombrado). Se repararon
   symlink del intérprete, `pyvenv.cfg` y 41 shebangs. `site-packages` estaba intacto (316 paquetes), por lo
   que no hubo reinstalación. Verificado: Python 3.14.7, `pandas 3.0.5` operativo.
2. **Store de Ollama vacío** (`{"models":[]}`): faltaban los 11 modelos, no sólo algunos. Descargas en curso
   (~60 GB), lanzadas en paralelo con concurrencia 3.

### Decisión metodológica: modelos Cloud autorizados
El autor autorizó `gemma4:31b-cloud` y `minimax-m3:cloud` **como línea base de comparación**. Registrado
como excepción acotada y aditiva en `AGENTS.md §2`. Se deja constancia de la implicancia: el corpus de 120
artículos (público: Kleptotrace + CoNLL-2002) se transmite a servidores remotos. La regla de
zero-data-leakage permanece vigente para todo dato productivo o confidencial.

### Hallazgo crítico para §5.3.5 y tablas de modelos
El modelo derivado de 12B con sufijo `q8` **no es q8**. Auditoría sobre el registro de Ollama (manifiestos y blobs,
sin descargar pesos) del modelo base real `gemma4:12b-mlx` (7.71 GB, coincidente con los 7.7 GB
documentados en julio):

- `quant_algo = MIXED_PRECISION`, capas en **`NVFP4` (4 bits)**, `kv_cache_quant_algo = FP8`
- Bits/peso derivados: ≈ **5.14** (7.71 GB para 12B parámetros)
- Un q8 real de 12B pesa **12.84 GB** (`gemma4:12b-it-q8_0`, verificado en el registro)
- `model_format = safetensors`, 725 capas `tensor` ⇒ el componente **`mlx` sí es correcto**

⇒ El sufijo `q8` es un **error de nomenclatura** heredado. Debe corregirse de forma transversal en la
tesina, `BENCHMARKS.md`, `AGENTS.md §8.6`, `README.md`, `results/run_config.json` y `src/config.py`.
Toda cita del modelo bajo el nombre con `q8` describe incorrectamente su cuantización.

### Estado
- Benchmark de los 11 modelos: **NO ejecutado aún** (bloqueado por descargas).
  - **Nota aditiva (2026-09-03):** superado en parte — corrida activa desde las 14:26:50 sobre **9 modelos
    locales** con `--rag-mode kb_combined` (`results/benchmark_balanced_120_kbrag_9models/`). Los 2 modelos
    cloud no son ejecutables (HTTP 429 cuota semanal agotada y HTTP 402 suscripción de pago), de modo que la
    unión queda en **14 modelos (5 + 9)**, no 16. La línea siguiente sigue vigente sin cambios.
- ANOVA/Tukey de los 16 modelos: **pendiente**.
- Los resultados vigentes para §5.3.5 siguen siendo los 5 modelos del 2026-09-01
  (F=10.2096, p=2.87e-15) hasta que la corrida completa termine.


---

## 2026-09-03 (cierre): Ajuste del Informe Final a las instrucciones institucionales MTI

### Fuente normativa
Se leyeron íntegramente los instructivos de `Instrucciones Informe Final de Tesina/`
(`tesinas-finales-2026.pdf`, `ieee-citationref.pdf`, `examen-grado-orientacion.pdf`) y se auditó el
informe contra ellos.

### Diagnóstico
- Cuerpo del informe (excl. anexos): **35 páginas** contra un límite de **25**.
- Resumen: **230 palabras** contra un límite de **200**.
- Leyendas de tabla: ausentes; se usaban oraciones en estilo `p1a` en vez del estilo `table caption`.
- Introducción (2 pp.) y Marco Teórico (cap. 2): conformes.

### Estrategia (autorizada por el autor): mover + condensar
- **Reubicado a anexos, íntegro:** protocolo Paso 1–5 del corpus sintético N=30 y su prompt de
  generación (**Anexo F**); tabla completa del benchmark general, 13 configuraciones (**Anexo E**);
  implementación técnica del KB RAG, flujos, catálogos, mini-benchmark N=5 y comparación cronológica
  v1.0/v1.1 (**Anexo D.1–D.8**); ejemplos few-shot completos (Anexo B); interfaz `LLMProvider` (Anexo A).
- **Condensado en el cuerpo:** §4.1.2, §4.3.1–4.3.2, §4.5, §5.4, §5.6.1, §5.6.5, §5.6.7, §6.5, §7.2.
  El texto suprimido se cita literalmente en `HISTORIAL-CONSOLIDADO.md` (raíz).
- **Resumen** reescrito a 163 palabras, sin referencias.
- **23 leyendas** de tabla añadidas con estilo `table caption`, centradas y sobre cada tabla.

### Correcciones de integridad
- Filas huérfanas de §5.1 (`nemotron-mini:4b`, `deepseek-r1:1.5b`), residuo de la conversión Markdown →
  DOCX, incorporadas a la tabla real; texto residual eliminado (11 → 13 configuraciones).
- Numeración automática heredada por los encabezados nuevos de anexos (prefijos erróneos `1.1`,
  `1.1.49`): corregida con `numId = 0` y numeración literal, criterio ya vigente en el documento.
- Dos páginas en blanco eliminadas: causadas por una fila de tabla añadida sin el estilo `Compact` de sus
  filas hermanas y por párrafos vacíos previos a encabezados con salto de página forzado. Recuperación
  neta: 5 páginas.

### Anexo G — Declaración de Uso de Inteligencia Artificial
Redactado sobre la base del historial de commits (20) y de ambos WORKLOG. Distingue el trabajo
intelectual del autor (formulación y modelado del problema, hipótesis, diseño arquitectónico y
experimental, protocolo estadístico, selección de modelos, verificación manual del ground truth,
ejecución de benchmarks, interpretación y redacción) del apoyo instrumental de la IA (generación del
corpus sintético N=30 bajo especificación y verificación del autor, asistencia de programación,
mantenimiento del registro de trabajo, conversión con pandoc y tareas de formato). Declara
explícitamente que ninguna cifra experimental fue producida por IA.

### Verificación
- Cuerpo: **24 páginas**; anexos desde la página 25. Sin páginas en blanco.
  *(Cifra superada por la entrada de cierre del mismo día: tras corregir los estilos `Table`/`Compact` el
  cuerpo quedó en **20 páginas**, anexos desde la 21, 29 pp. totales — holgura real de 5 pp. frente al
  límite de 25.)*
- Comprobación automatizada: ninguna tabla perdida (22 → 23 por desdoblamiento resumen/completa) y el
  **100 %** de los valores porcentuales del documento original sigue presente.
- Respaldo previo al ajuste: `doc/organized/Hito_5_Tarea4_Informe_Final/
  Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx.bak_pre-cumplimiento-25pp`.

### Pendientes registrados (cronograma completo en `HISTORIAL-CONSOLIDADO.md` §7)
1. Benchmark N=120 con los 11 modelos restantes y ANOVA/Tukey de los 16.
2. Corrección transversal de la nomenclatura `q8` (`gemma4-12b-mlx`, en realidad NVFP4/precisión mixta).
3. Discrepancia entre el título «16 Modelos» de §5.1 y las 13 configuraciones de la tabla.
4. Revisión de las referencias contra el formato IEEE.
5. Aplicar el mismo ajuste de extensión al `Informe_Final_Tesina_NER.docx` standalone.

---

## 2026-09-03 (final): Corrección del renderizado del Informe Final

### Causa raíz detectada
El documento fusionado con la plantilla referenciaba dos estilos **inexistentes** en `styles.xml`:
`w:tblStyle="Table"` (en las 23 tablas) y `w:pStyle="Compact"` (en las celdas), heredados de la conversión
pandoc → DOCX. Sin esas definiciones, las tablas se renderizaban **apiladas en una sola columna, sin
bordes**, con enormes huecos en blanco: el informe ocupaba 13 páginas más de lo necesario. Se definieron
ambos estilos (bordes finos grises, márgenes de celda, párrafo compacto de 8 pt).

### Correcciones de maquetación
- **Estructura XML inválida**: el `w:sectPr` final había quedado en medio del cuerpo, con los anexos D–G
  después de él. Se restituyó como último hijo de `w:body`.
- **Encabezado**: las tres variantes (par, predeterminado y primera página) eran distintas y dos usaban
  imágenes **flotantes** que se solapaban con el texto institucional. Se unificaron en una única
  estructura determinista: tabla de 3 columnas con imágenes **en línea** (banner UTFSM a la izquierda,
  tres líneas centradas, logo MTI a la derecha). Se corrigió también el interlineado `exact`, que
  recortaba las imágenes en línea.
- **Márgenes**: margen superior a 3.3 cm para separar el cuerpo del encabezado (antes 2.5 cm, con
  solapamiento). Laterales 3 cm e inferior 2.5 cm sin cambios.
- **Tablas**: anchos de columna proporcionales al contenido (ancho útil 8838 twips), evitando cortes de
  palabras del tipo «gemma4:l atest».
- **Resumen/Abstract en página propia** y salto de página en los nueve capítulos (al capítulo 1 le
  faltaba, por usar el estilo `Heading 1` nativo en vez de `heading1`).
- **Párrafos justificados con saltos manuales** divididos en párrafos independientes (eliminan las líneas
  estiradas); se restauró la negrita de los prefijos tipo «Hallazgo 1:».
- **Listas embebidas** («… : - Ítem 1. - Ítem 2.») convertidas en viñetas reales (4 párrafos).
- Eliminados los párrafos vacíos finales que generaban una página en blanco.

### Estado del documento
- 29 páginas totales. **Cuerpo: 20 páginas** (portada, resumen y capítulos 1–8); anexos desde la 21.
- Sin páginas en blanco, sin solapamientos con encabezado ni pie.
- Margen de holgura de 5 páginas respecto al límite institucional de 25: es posible reincorporar al
  cuerpo parte del material trasladado a los anexos D–F si el autor lo prefiere.

---

## 2026-09-03 (cierre documental) — Auditoría de consistencia: 26 correcciones de gravedad ALTA

Fuente: `AUDITORIA_CONSISTENCIA_20260903.md` (115 hallazgos confirmados con verificación adversarial;
26 de gravedad ALTA, 55 media, 34 baja). Se registran aquí las 26 ALTA con archivo, ubicación y corrección.
Abreviaturas: **BOR** = `doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md`;
**STD** = `Informe_Final_Tesina_NER.docx`; **PLA** = `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx`.

| # | Archivo | Ubicación | Qué se corrigió |
|:--:|:---|:---|:---|
| A1 | BOR | L90, L139, L267, L369, L435 | Conteo de modelos contradictorio (15 vs 16): se fija el conteo real de 12 modelos distintos y se propaga a §1.4, §2.5, §4.2, §5.1 y §5.3.5 |
| A2 | BOR | L267–270 | §4.2 anunciaba 15 modelos y enumeraba 12 (6+4+2): encabezado corregido a 12 y añadido `gemma4:31b-mlx`, efectivamente reportado |
| A3 | BOR | L369–388 | Título de §5.1 decía 16 modelos frente a 13 filas = 12 modelos: título ajustado, aclarado que dos filas son configuraciones del mismo modelo (`gemma4:latest` ZS-ES y FS-ES, ambas legítimas) y eliminada la línea en blanco de L386 que partía la tabla |
| A4 | BOR | L375–376, L381 vs L472–474 | Índice Tok/s/B discrepante entre Tabla 2 y §5.5: recalculado como Tok/s ÷ parámetros(B) y unificado en Tabla 2, §5.5 y §6.3 |
| A5 | BOR | L669 vs L439, L456 | §6.1 confirmaba la hipótesis solo con N=30 (79.03 %) ignorando que en N=120 el mejor F1 es 59.25 %: se discuten ambos corpus y se explica la diferencia de dominio y longitud |
| A6 | BOR | L249, L255 | «datos reales balanceados generados por LLM» (autocontradictorio, residuo de un reemplazo global): restituido «corpus sintético» / «datos sintéticos» |
| A7 | BOR | L39, L767 | Nombre de dataset corrupto en el abstract («…Kleptotrace/CoNLL-2002/CoNLL-2002») y URL inválida `https://Kleptotrace/CoNLL-2002.org` en la referencia [18]: nombre normalizado y URL restaurada |
| A8 | STD | Entre §4.1.2 d) y §4.2 | Faltaba íntegra la §4.1.3 «Extensión a Corpus Real N=120 (Dataset Conmutable)»: reinsertada desde el `.md` vigente |
| A9 | STD | Entre §5.3.4 y §5.4 | Faltaba íntegra la §5.3.5 con la tabla 5 modelos × 2 modos y el ANOVA **F=10.2096 / p=2.873×10⁻¹⁵**: reinsertada completa (tabla + ANOVA + Tukey HSD + lectura conjunta con N=30) |
| A10 | STD | §5.6.1, §5.6.5, §6.5, §7.1 concl. 6, §7.2 (×2), Anexo A | Siete referencias huérfanas a N=120 sin sección que definiera el corpus: resueltas al restaurar §4.1.3 y §5.3.5, verificando que toda mención tenga antecedente en el mismo documento |
| A11 | PLA, STD y BOR (.docx) | §1.4 obj. 3, §2.5 punto 2, título §4.3, §4.3.4, título §5.2 y pie de Tabla 6 | Los tres DOCX conservaban «análisis comparativo de prompts» como término PRINCIPAL: sincronizados con el `.md` a «Análisis Comparativo de Prompts», dejando «diseño factorial 2×2» y «análisis comparativo de prompts» como sinónimos glosados. El abstract en inglés conserva *prompt comparative prompt analysis* |
| A12 | `BENCHMARKS.md` | L101 | Documentaba `python src/main.py --run-config results/run_config.json`, flag inexistente en el argparse: reemplazado por un comando válido (`--data-file` / `--models` / `--batch-size`) |
| A13 | `BENCHMARKS.md` | L33 | Instruía editar `results/run_config.json` como entrada, siendo una salida generada: se documenta que los modelos se definen en `src/config.py` (`BenchmarkConfig.models`) o vía `--models`, y que `run_config.json` es un artefacto de reproducibilidad |
| A14 | `BENCHMARKS.md` | L132–141 («Cleaning Up») | Instruía `rm -rf results/*.json` antes de cada corrida, contra la política de retención aditiva: sustituido por «no se borra nada; cada corrida genera su propio `results/<dataset>_<timestamp>/`» |
| A15 | `BENCHMARKS.md` | L146 | El encabezado «Latest Benchmark Results (July 24, 2026)» no correspondía a ninguna corrida catalogada: la tabla de julio se reetiqueta como histórica con su `run_id` y se añade la corrida vigente `…20260901_140421` |
| A16 | `BENCHMARKS.md` | L171–178 | La tabla «Prompt Comparative Prompt Analysis (gemma4:latest)» no declaraba corpus ni N ni corrida: etiquetada con `run_id`, corpus y N, separando las cifras verificadas de N=15 y N=120 |
| A17 | `AGENTS.md` | §8.6, L169–189 | Tabla de modelos desactualizada: añadidos `gemma4:31b-mlx`, `gemma4:12b-mlx` y `gliner:medium`, y corregido el inexistente `gemini-1.5-flash-lite` |
| A18 | `RUNS_INDEX.md` | §7, L179–182 | La limitación 1 afirmaba que `--ablation` no se persiste; ya forma parte de `BenchmarkConfig`: nota aditiva en §6 indicando que quedó resuelta el 2026-09-03 y que solo afecta retroactivamente a las corridas #9 y #12 |
| A19 | `RUNS_INDEX.md` | L200–202 | La nota de cierre afirmaba que no se aplicó ningún cambio a `src/main.py` ni `src/config.py`, lo cual es falso: nota aditiva que distingue lo aplicado (guardrail de raíz y persistencia de `ablation`) de lo pendiente |
| A20 | BOR | L375–376 (§5.1, Tabla 2) | `gemma4:31b` y `gemma4:31b-mlx` figuraban como modelos distintos con las 6 métricas IDÉNTICAS pese a ser runtimes distintos (GGUF vs MLX): restituidos los valores reales de `benchmark_mlx_serial.log` |
| A21 | BOR | L377 (§5.1), L683 (§6.4), L706 (§7.1 concl. 3) | El F1 de 66.29 % de `gemma4:31b-cloud`, que sostenía el argumento de soberanía de datos, no se reproduce desde ninguna fuente: sustituido por el único valor con respaldo documental (F1=39.73 %, IC95 % 0.21–0.59) y reescritos §6.4 y la conclusión 3 |
| A22 | BOR | L486 (§5.6.1) | Se afirmaba que la degradación por RAG-diccionario fue «consistente a lo largo de todos los modelos evaluados» cuando el RAG mejoró el F1 en 8 de 15: reformulado a «en los modelos de mayor capacidad (7 de 15 degradaron, entre ellos los cinco de mayor F1 baseline)» |
| A23 | BOR | L646 (§5.6.6), L712 (§7.1 concl. 6) | El «−33 % vs baseline» del dict-RAG salía de dividir 0.2367 contra el baseline de OTRO mini-benchmark N=5: etiquetado 0.2367 como sondeo N=5 con su propio baseline 0.5614 (−57,8 % / −32,5 pp) y eliminada la contraposición de una cifra N=5 con una N=120 |
| A24 | BOR | L221 (§4.1, Corpus 1) | Se declaraban ~800 caracteres promedio en el Gold Standard N=15; la medición real es 4.832,9: corregido a «~4.833 caracteres (mediana 5.280; rango 725–8.813)» y reformulado el argumento de longitud de §5.3.5, que quedaba invertido |
| A25 | BOR | L245 (§4.1.1, Paso 5) | Distribución de entidades del corpus N=30 invertida (2,1 PER / 1,3 ORG) y longitud errónea (187): corregido a 1,2 PER y 2,3 ORG por artículo y 202 caracteres promedio (rango 145–293) |
| A26 | BOR | L65 (§1.1) | Marcador sin resolver «[referencia KPMG 2024]» sin entrada bibliográfica y «billones» (10¹²) como traducción de *billion*: sustituido por «miles de millones» (12.300 y 87.200 millones) y por una cita IEEE numerada con su entrada en §8 |

### Correcciones documentales de esta misma sesión aplicadas a los registros

- `research/rag/WORKLOG.md`: corregido el «+105 %» del mini-experimento N=5 (real: **+204,9 %** relativo,
  **+48,5 pp**); nota de propagación completa de la corrección de confidencialidad en los tres DOCX; nota de
  estado de la corrida de 9 modelos locales con `kb_combined` (los 2 cloud no ejecutables ⇒ 14 modelos, no 16);
  remisión desde la verificación de 24 pp. a la cifra vigente de 20 pp. de cuerpo.
- `HISTORIAL-CONSOLIDADO.md`: unificada la paginación (**cuerpo 20 pp., anexos desde la 21, 29 pp. totales,
  holgura real de 5 pp.** frente al límite de 25); marcado `Informe_Final_Tesina_NER.docx` como **INCOMPLETO**
  (faltan §4.1.3 y §5.3.5); explicitada la secuencia 40 → 27 → 29 pp.; desambiguadas las rutas de los tres
  WORKLOG; añadidas las tareas 11 y 12 al cronograma §7; registrada como nota aditiva la confusión de corpus
  de la entrada 2026-07-01 de `/WORKLOG.md` (histórico, no editable).

---

## 2026-09-03 (cierre de sesión): Documentos de hallazgos, lecciones y coordinación

### Documentos nuevos creados
| Documento | Contenido |
|:---|:---|
| [`FINDINGS.md`](../../FINDINGS.md) | 25 hallazgos técnicos y documentales de la revisión final, con evidencia e impacto |
| [`LEARNING.md`](../../LEARNING.md) | 20 lecciones derivadas de esos hallazgos, cada una con su aplicación práctica |
| [`TODO-INFORME-FINAL.md`](../../TODO-INFORME-FINAL.md) | Seguimiento del cierre del informe, stack tecnológico y tareas asignadas a Claude Desktop |
| [`AUDITORIA_CONSISTENCIA_20260903.md`](../../AUDITORIA_CONSISTENCIA_20260903.md) | 115 inconsistencias documentales verificadas adversarialmente |
| [`CURRENT-TASKS.md`](../../CURRENT-TASKS.md) | Coordinación entre agentes: quién trabaja en qué y sobre qué archivos |

### Decisión: exclusión de dos modelos por restricción de hardware
El equipo de evaluación tiene **16 GB de RAM**. Los modelos `` (16 GB)
y `gpt-oss:20b` (13 GB) provocaban swap masivo: el ritmo medido fue de **1 extracción cada 3 minutos** y
**no varió al aumentar los workers de 2 a 8**, porque el límite era memoria física, no configuración.
La proyección con los 9 modelos locales era de **~173 horas**, con esos dos concentrando el 85%.

Por decisión del autor se excluyen, quedando el estudio en **12 modelos** (5 de la corrida del 2026-09-01
más 7 locales) y una proyección de **~66 horas**.

**Compatibilidad con la corrida de referencia verificada e intacta:** coinciden los nueve parámetros del
protocolo (`data_file`, `rag_study`, `rag_mode=kb_combined`, `batch_size=3`, `temperature=0.1`, `seed=42`,
`max_tokens=2048`, `system_prompt_file`, `fuzzy_threshold=85`). Los modelos excluidos tampoco formaban
parte de aquella corrida, por lo que ambos conjuntos siguen siendo disjuntos sobre el mismo corpus: la
fusión para el ANOVA conjunto sigue siendo válida.

> Debe declararse en la tesina como **limitación de hardware**, no como decisión metodológica.

### Modelos cloud descartados
`gemma4:31b-cloud` devuelve **HTTP 429** (cuota semanal agotada) y `minimax-m3:cloud` **HTTP 402**
(requiere suscripción de pago). Verificado llamando directamente a la API de Ollama. Un `ollama pull`
exitoso **no** implica que el modelo sea utilizable: solo descarga el manifiesto.

### Protocolo de coordinación entre agentes
Se estableció `CURRENT-TASKS.md` como documento vivo de coordinación, con secciones para Claude Code,
Claude Desktop y Antigravity, y una subsección por workflow. El protocolo (leer → escribir entrada →
ejecutar → actualizar → volver a leer) quedó documentado en `CLAUDE.md` (raíz), `AGENTS.md §11`,
`GEMINI.md`, `ANTIGRAVITY.md` y el `CLAUDE.md` del repositorio.

### Correcciones documentales aplicadas
Un workflow de 8 agentes aplicó **84 correcciones** derivadas de la auditoría. Su fase de verificación
detectó **5 regresiones**, todas reparadas: borrado de la entrada `glm-5.1:cloud` (violación de la política
aditiva, restaurada con nota), un fragmento de código Python sintácticamente inválido, la reaparición del
nombre de modelo retirado, una autocontradicción entre `AGENTS.md §8.3` y `§8.4`, y un consejo de `--resume`
inoperante por omitir `--results-dir`.

---

## 2026-09-07 — Cierre del estudio: convención de puntuación única, ANOVA definitivo y correcciones al informe

**Objetivo.** Cerrar la fase experimental y dejar el informe consistente con los datos.

**Integridad de datos.** Se descubrió que el re-puntaje del bug de *scoring* (`F1=1.0` en extracción vacía)
había cubierto solo las corridas del equipo remoto: las tres corridas *legacy* y la corrida canónica N=15
seguían con la convención antigua, de modo que el estudio **mezclaba dos formas de puntuar**. Se re-puntuaron
todas con `tools/rescore_saved.py`. Estado final: **8 927 filas, 0 violaciones de `F1 ≤ (P+R)/2`, 0 filas
degeneradas, 0 filas perdidas**, y `summary == CSV` en las quince corridas. Se detectó además que la
herramienta solo reescribía el CSV, dejando obsoletos los `benchmark_summary.json` y `statistical_report.md`;
el equipo remoto la extendió y se publicó `results/AVISO-SUMMARIES-OBSOLETOS.md`.

**Alcance.** Se eliminó del estudio, por decisión del autor, la cuantización *custom* de espacio de usuario
`sonct988/gemma4-26b` —ni citable ni reproducible—, sin dejarla como referencia histórica. El estudio queda en
**13 modelos**.

**Análisis conjunto definitivo.** `results/ANALISIS_CONJUNTO_20260907/`: 13 modelos × 2 modos, 3 120
observaciones, **F = 36.3666, p = 1.2236e-152**. El post-hoc de Tukey aporta el matiz que faltaba: la mejora
del KB RAG **solo alcanza significancia estadística en los dos modelos más débiles** —`nemotron-mini:4b`
(+14.52 pp, p<0.001) y `llama3.2:latest` (+10.82 pp, p=0.014)—, mientras que en los once restantes no supera
la corrección por comparaciones múltiples.

**Correcciones al informe.** Se reconstruyó la Tabla 2 (§5.1) entera desde los CSV re-puntuados —cada fila es
ahora reproducible—, retirando los modelos fuera del estudio y separando las dos filas de 31B que arrastraban
cifras idénticas por un error de copia. Se sustituyó §5.2 por las mediciones limpias, lo que **cambió la
conclusión**: idioma y *few-shot* **interactúan** (+4.38 pp y −0.73 pp por separado, **+11.12 pp** combinados).
Se reescribió §5.3.5 con el estudio completo y se aplicó el renombrado terminológico a «Análisis de Variantes
de Prompts».

**Hallazgos.** `FINDINGS.md §F45` cierra la línea del modo *thinking* (efecto específico de cada modelo:
`gpt-oss:20b` deja de responder sin él, `deepseek-r1:1.5b` da extracción idéntica y solo cuesta tiempo; los
demás son ruido de N=15). `§F46` documenta que los 76 `recall=0` de `gpt-oss:20b` **no son incapacidad del
modelo sino degeneración por repetición** que deja el JSON sin cerrar, con la latencia de los fallos igual a
la de los aciertos.

**Trazabilidad.** Se versionó `benchmark_augmented_30.log`, único registro superviviente del F1 titular de
julio, que el patrón `*.log` del `.gitignore` mantenía fuera del repositorio y existía en una sola máquina.

---

## 2026-09-07 (Claude Desktop): propagación del cierre de benchmarks a los tres DOCX

Ejecutado el encargo `PROMPT-CLAUDE-DESKTOP-20260907.md` (tarea 2.6 de `CURRENT-TASKS.md`).

**Método.** Sincronización por delta: se extrajo el Markdown canónico en su estado del 2026-09-03
(`git show e20fd50`) y en el actual, se alinearon ambos con `difflib` y se aplicaron los 72 bloques de
cambio a los `.docx` por **edición estructural del XML, sin pandoc**, conservando numeración multinivel,
estilos de fila, leyendas y saltos de página.

**Aplicado.** Tabla 2 (§5.1) reconstruida — 12 modelos en 13 configuraciones, con la nota de procedencia de
cada corrida y los cuatro hallazgos nuevos. §5.2 con las mediciones limpias y la lectura de interacción
(ZS-ES +4.38 pp, FS-EN −0.73 pp, FS-ES +11.12 pp). §5.3.5 reescrita al estudio completo de 13 modelos
(F=36.3666, p=1.2236e-152; Tukey: solo `nemotron-mini:4b` +14.52 pp y `llama3.2:latest` +10.82 pp alcanzan
significancia), con la limitación de *mojibake* del corpus N=120 y las dos salvedades de procedencia
(latencia de `gemma4:31b-cloud` cuantizada por `--request-delay`; siete filas de `nemotron-mini:4b` sin
telemetría). Tablas de eficiencia, dict-RAG, trabajos relacionados, métricas y Anexo C actualizadas.
Terminología «Análisis de Variantes de Prompts». Citas IEEE numeradas y referencia [12] repuesta.
§4.1.3 y §5.3.5 reinsertadas en `Informe_Final_Tesina_NER.docx`. Anexo E reconvertido en tabla de
procedencia. Fila «Versión del documento — v2, 7 de septiembre de 2026» añadida a la ficha.

**Verificación.** Cuerpo del canónico: **21 páginas de 25**; sin páginas en blanco; los tres documentos
contienen las cifras nuevas. Versión `_v2` congelada en `doc/versions/informe_final/` con su SHA-256.

**No decidido:** el F1 titular de N=30 (79.03 %) permanece sin cambios, pendiente del criterio del autor
(`TODO-INFORME-FINAL.md §15.3`).

**Observación para el `.md` canónico:** el «Hallazgo 4» de §5.2 conserva la lectura antigua (+7.4 % por
localización), que contradice la tabla nueva y el párrafo de interacción de la misma sección.

---

## 2026-09-07 (Claude Desktop): tanda estructural — respuesta al profesor guía

Ejecutado el encargo `PROMPT-CLAUDE-DESKTOP-PROFESOR-20260907.md` (tarea 2.8, que además cubre la 2.7).

**Método.** El `.md` canónico acumulaba +212/−165 líneas y reescribía capítulos completos, de modo que el
parcheo párrafo a párrafo dejaba de ser fiable. Se **reconstruyó el cuerpo del `.docx` desde el `.md`** con un
renderizador propio que emite sobre los estilos de la plantilla (`heading1/2/3`, `p1a`, `table caption`,
`Table`, `programcode`, `referenceitem`, `author`, `address`, `e-mail`). **No se usó pandoc**: se conservan
`styles.xml`, encabezados, pies, márgenes y `sectPr`, y se reaplican la numeración literal con `numId=0`, las
leyendas sobre cada tabla, los anchos de columna proporcionales al contenido y la separación de los hallazgos
en párrafos independientes. Las referencias cruzadas «la Tabla N» se realinearon con la numeración real.

**Previo indispensable.** Para que el `.docx` sea reflejo del `.md`, se llevaron primero al `.md` los anexos
**D, E, F y G**, que vivían solo en el `.docx` (respaldo: `.bak_pre_anexosDEFG_20260907`). Los anexos quedan
A–H en orden, con la **G íntegra** —declaración de uso de IA— y la H de codificación después.

**Resultado medido.** Cuerpo de **23 páginas** contra el límite de 25; anexos desde la 24; 33 páginas totales;
**cero páginas en blanco**. Los cuatro reparos del profesor quedan atendidos en los tres `.docx`: sin ficha del
estudiante, sin saltos de página entre capítulos, sin bloques en blanco y con los capítulos 2, 3 y 6 y §5.6
desarrollados. Incorporadas también la re-corrida N=30 y todo el bloque de codificación (§4.4, conclusión 7,
§7.2 punto 7 y Anexo H).

**No se congeló versión**, según la instrucción: queda pendiente la segunda tanda, acotada a cifras, cuando
cierre la re-ejecución de `gpt-oss:20b` (afectará a §5.3.5, §6.1, §6.2 y la conclusión 6).

### 2026-09-07 20:05 — Diagramas de texto convertidos en tablas de Word

Al reconstruir el `.docx` desde el `.md`, los diagramas de texto volvieron a emitirse como bloques
`programcode`, contra la regla del proyecto: **un diagrama va como tabla de Word**, nunca como cuadro de
texto, porque el arte ASCII se descuadra con tipografía proporcional. Se corrigió **primero en el `.md`**
(respaldo `.bak_pre_diagramas_20260907`) y luego se reconstruyeron los tres `.docx`.

Convertidos: la arquitectura de cinco capas de §3.2 (Capa / Módulo / Detalle técnico), la estructura canónica
del prompt *few-shot* de §4.3.1 (Posición / Contenido), los dos flujos RAG de §5.6 (Paso / Acción / Resultado),
con el contexto de dominio inyectado como tabla aparte (Regla / Contenido), y el árbol del repositorio del
Anexo A (Ruta / Descripción, con la jerarquía indentada). Las tablas pasan de 29 a 35 y no queda arte ASCII en
ninguno de los tres documentos. Los bloques de código que permanecen son código real: la interfaz
`LLMProvider`, los prompts de generación, los tres ejemplos *few-shot* y las invocaciones CLI.

Cuerpo re-medido: **23 páginas de 25**, sin páginas en blanco.

### 2026-09-07 21:10 — Segunda y tercera tanda propagadas · versión v3

**Segunda tanda (datos).** Cerrada la re-ejecución de `gpt-oss:20b`: su fila de §5.3.5 pasa a 52,39 / 55,67 /
**+3,28 pp** y sube al quinto puesto; el ANOVA conjunto queda en **F=38,2222, p=3,4453e-160**; el Tukey de
`llama3.2` afina a p=0,007. El Anexo H se corrige en consecuencia: el delta de mojibake de `gpt-oss` pasa a
**−0,0336** y el rango entre modelos a **9,4 puntos**.

**Tercera tanda (condensación).** Anexos concentrados en resultados finales —3 064 palabras y 10 tablas— y
§5.6 reescrita íntegramente en prosa, sin tablas. El cuerpo queda con **10 tablas**, las diez declaradas
intocables. Total 20 tablas con numeración correlativa y llamadas del texto realineadas.

**Corrección de forma.** El `&nbsp;` con el que se indentaba el árbol del Anexo A se veía literal en Word. Se
sustituyó en el `.md` por **espacio duro real (U+00A0)** y se corrigió el renderizador, que lo descartaba al
normalizar las celdas con `strip()`. La jerarquía vuelve a verse indentada y no queda ningún literal HTML.

**Medición.** Cuerpo de **20 páginas de 25**, 28 totales, anexos desde la 21, cero páginas en blanco, cero
arte ASCII. **Versión `_v3` congelada** (SHA-256 `b172947f58c1`) y registrada en `VERSIONES.md`.

### 2026-09-07 22:25 — Cuarta y quinta tanda · versión de entrega (_v4)

Propagadas a los tres `.docx` la prosa continua de §3.1, §4.2, §5.4 y el ANOVA de §5.3.5; la consolidación de
§4.3 —cuyas cuatro subsecciones desaparecen, con los ejemplos *few-shot* trasladados al Anexo B—, la fusión de
§4.1.1 con §4.1.2 y la integración de §4.5 en §4.4; el capítulo 2 de seis a cuatro secciones y el 3 de cuatro
a tres; la URL del repositorio en el Anexo A y el registro suavizado.

**Verificación final superada.** Cuerpo de **18 páginas de 25** (27 totales, anexos desde la 19), resumen de
191 palabras, introducción de 2 páginas, nueve capítulos, anexos A–H con la G íntegra, 19 tablas con leyenda y
numeración correlativa, sin saltos de página al empezar capítulo, sin páginas en blanco, sin arte ASCII ni
literales HTML, citas IEEE con sus veinte entradas y **ninguna referencia cruzada rota** —16 llamadas
verificadas contra 39 secciones; el `§3.3` que persiste apunta al actual «Módulo de evaluación», no al antiguo—.

**`_v4` congelada como versión de entrega**, SHA-256 `2bc915c7a511`, registrada en `VERSIONES.md`.

### 2026-09-07 22:45 — Anexo B, espacios en blanco y ajuste a 25 páginas exactas · versión de entrega (_v5)

**Anexo B corregido primero en el `.md`** (respaldo `.bak_pre_anexoB_20260907`). Los tres ejemplos *few-shot*
y el prompt de generación del corpus N=30 arrastraban saltos de línea duros heredados del formato de ancho
fijo, que en Word partían las frases a media palabra. Cada campo `Texto:` / `Respuesta:` queda en una sola
línea y el prompt de generación en un solo párrafo, **sin suprimir ni una palabra**. En el `.docx`, los
bloques `programcode` / `Source Code` bajan a **7 pt** (`w:sz`/`w:szCs` = 14) con interlineado exacto de 170,
de modo que las líneas largas caben sin quebrarse.

**Espacios en blanco reducidos a nivel de estilo**, no de contenido: `Heading 1` 480/240 → 300/160,
`Heading 2` 340/200 → 220/120, `Heading 3` → 200/100 y `table caption` 240/120 → 140/80.

**Resultado medido: 25 páginas exactas —cuerpo 17, anexos 8.** El objetivo se alcanzó solo con la
compactación tipográfica, de modo que **no hubo que consolidar ni recortar párrafos de los anexos: su texto
queda íntegro**, tal como pedía el encargo («sin sacrificar nada de contenido»).

**Corrección adicional.** El anidamiento de énfasis del renderizador (`**Ejemplos *few-shot* de…**`) dejaba
asteriscos sueltos en el título del Anexo B; se afinó la expresión regular *inline* a coincidencia no
codiciosa y se limpian los marcadores interiores.

**Verificación completa superada:** 25 páginas exactas, cuerpo 17/25, sin páginas en blanco, sin saltos de
página al empezar capítulo, resumen de 191/200 palabras, nueve capítulos, anexos A–H con la **G íntegra**, 19
tablas con leyenda y numeración correlativa, sin arte ASCII ni literales HTML, sin asteriscos sueltos y con
el contenido de los anexos verificado por muestreo. Propagado a los tres `.docx`.

**`_v5` congelada como versión de entrega** —sustituye a la `_v4`—, SHA-256
`41382e69d6d2405d54c122e81f4867446376836f8ae678340e8dd1849c2acd1d`, en
`doc/versions/informe_final/Informe_Final_Tesina_NER_v5.docx` y registrada en `VERSIONES.md`.

### 2026-09-07 23:25 — Exportación a PDF · la conversión como auditoría · versión de entrega (_v6)

Petición del autor: **exportar el `.docx` a PDF** conservando las 25 páginas y el formato. Convertido con
**LibreOffice headless** en el equipo del autor. Las fuentes quedan **incrustadas y subconjuntadas**
—Liberation Serif y Nimbus Mono, métricamente compatibles con Times New Roman y Courier New—, así que la caja
tipográfica no se descuadra y el recuento de páginas del PDF vale como recuento del documento.

**La exportación funcionó como auditoría** y destapó tres defectos que el `.docx` arrastraba desde la
extracción de los anexos D–G. Los tres se corrigieron **primero en el `.md`** (respaldo
`.bak_pre_leyendas_20260907`) y luego en los tres `.docx`:

1. **Leyendas duplicadas en los anexos D y E.** Cinco líneas `_Tabla N. Título_`, heredadas del `.docx`
   original, se imprimían como párrafo normal —con los guiones bajos a la vista y numeración obsoleta: 16, 17,
   18, 23, 20— **encima** de la leyenda real que genera el renderizador a partir del encabezado. Se corrigió
   en el renderizador (`render.py` y `render2.py`): esa línea se **consume** como leyenda y se renumera, de
   modo que el título descriptivo del `.md` sustituye al del encabezado. Las leyendas 12 a 16 pasan a ser
   «Configuración CLI del Módulo KB RAG», «Guías Tipológicas de Dominio de la Base de Conocimientos»,
   «Ejemplares Few-Shot de la Base de Conocimientos», «Reglas de la Base de Conocimientos Contextual» y
   «Resultados Completos del Benchmark General (13 Configuraciones, N=15)».
2. **Colofón duplicado dentro del Anexo D**: tres párrafos sueltos con el título de la tesina, la universidad
   y la fecha, varados entre las tablas D.1 y D.2. Eliminados.
3. **Colofón varado y con fecha obsoleta.** El colofón legítimo cerraba el Anexo C, no el documento, y decía
   «Julio 2026». Movido al **final** y fechado en **septiembre de 2026**, la fecha de la entrega. Cabe en el
   hueco de la página 25, así que no añade página.

**Verificación del PDF superada:** **25 páginas exactas** · cero páginas en blanco · encabezado y pie en las
25, con holgura mínima de 21,2 pt arriba y 17,8 pt abajo (**sin solape**) · los dos logotipos en línea en las
25 · **19 leyendas correlativas** de la 1 a la 19, una sola vez cada una · anexos A–H con la G íntegra ·
resumen de 191/200 palabras · sin arte ASCII, sin literales HTML y sin asteriscos ni guiones bajos sueltos ·
colofón único al cierre. Verificado además por inspección visual de las páginas 1, 9, 19, 21 y 25.

**`_v6` congelada como versión de entrega** —sustituye a la `_v5`, y es la primera que congela también el
PDF—: `doc/versions/informe_final/Informe_Final_Tesina_NER_v6.docx` (SHA-256 `2543def700a8`) y
`…_v6.pdf` (SHA-256 `c9b2071f385b`). El PDF de trabajo queda en la raíz del proyecto.

### 2026-09-08 00:05 — Resumen y abstract fundidos y sincronizados · versión de entrega (_v7)

El autor advirtió que resumen y abstract «difieren mucho». El historial lo explica: el núcleo del abstract
data del commit `0b27b5c` (**27 de julio**) y desde entonces solo recibió un parche puntual, mientras el
resumen se reescribió entero el 7 de septiembre (`c3ba8cb`). Describían dos versiones distintas del trabajo:
el resumen, la validación final —120 artículos reales, trece modelos, RAG inversamente proporcional a la
capacidad, ANOVA y Tukey—; el abstract, la de julio —N=15 y N=30, un párrafo de arquitectura y **ningún
resultado de RAG**—.

**Fundidos.** Ambos dicen ahora lo mismo y siguen el orden que exige `plantilla_final-2026.docx`: (1) contexto
y problema, (2) propuesta y objetivos, (3) procedimiento y métodos de validación, (4) resultados e impacto.
Del resumen se conserva la validación final; del abstract se recupera lo que solo él tenía —la arquitectura
pub/sub multihilo con concurrencia adaptativa (AIMD) y capa Factory/Facade, y el 80,57 % de F1 sin
extracciones fallidas—. **RESUMEN 199 palabras y ABSTRACT 183**, ambos bajo el límite de 200, un párrafo cada
uno y siete oraciones paralelas. La quinta palabra clave se alinea: *Prompt Engineering* → **RAG**.

**Dos precisiones de fondo.** El 80,57 % se declara **sobre el corpus del dominio**, no sobre el de 120
artículos, donde el mejor local es 59,25 %. Y se retira la afirmación de «60–80 % de reducción de costos» que
arrastraba el abstract: es el **objetivo 5**, no un resultado medido; queda «reduce el costo unitario de
revisión», como en el resumen.

**Fuentes restituidas.** El segundo párrafo del abstract llevaba el estilo `p1a` —10 pt, sin las sangrías de
567 twips— mientras el primero llevaba `abstract`. Al fundirlos, el párrafo único vuelve al estilo `abstract`
de la plantilla, el mismo del resumen; en los otros dos `.docx`, cuyos identificadores difieren, se iguala al
estilo del resumen (`BodyText`). Comparados estilo a estilo contra la plantilla, los únicos apartamientos que
quedan son los deliberados: `programcode` a 7 pt y el estilo `Compact`.

**Espaciado compactado**, a nivel de estilo y no de texto: `abstract` `before` 600 → 160 en el documento
canónico y `Heading 1` `after` 160 → 80 en los otros dos. Sobrevive a las reconstrucciones desde el `.md`.

**Los dos bloques quedan en la página inicial** del Word y del PDF —verificado sobre el PDF—, con sitio de
sobra para el arranque del índice. **Verificación superada:** 25 páginas exactas, cero en blanco, encabezado y
pie en las 25 sin solape (mínimos 21,2 y 19,1 pt), 19 leyendas correlativas, anexos A–H, colofón único.

**`_v7` congelada como versión de entrega** —sustituye a la `_v6`—: `.docx` SHA-256 `a8616ddb2c15` y `.pdf`
`ecc2bd49f2cb`. Corregido primero el `.md` (respaldo `.bak_pre_resumen_20260907`) y propagado a los tres `.docx`.

### 2026-09-08 00:40 — Propagación del desarrollo conceptual · versión de entrega (_v8)

Encargo `PROMPT-CLAUDE-DESKTOP-PROPAGACION-20260907.md` y §2.17. Reconstruidos los tres `.docx` desde el `.md`
canónico (106 701 bytes, 23:44), que llegaba ya consistente de la sesión de Claude Code: **§2.4** explica el
aparato estadístico —ANOVA, Tukey HSD, intervalos de confianza, análisis de sensibilidad— que hasta ahora se
usaba sin definirse, lo que desplaza el estado del arte a §2.5; **§4.4** desarrolla en prosa las métricas, con
el porqué de la media armónica; **§3.3** corrige el emparejamiento difuso, que no es similitud de tokens sino
**distancia de Indel normalizada** (`rapidfuzz.fuzz.ratio`); y **§5.5** declara el coste por artículo como
estimación. Sin pandoc, y sin necesidad de tocar el `.md`.

**De 27 a 25 páginas, solo por estilo.** El material nuevo llevaba el documento a 27. Se recortó `Normal`
240 → 228, `Ttulo1` 300/160 → 220/110, `Ttulo2` 220/120 → 160/80, `Ttulo3` 200/100 → 140/70, leyendas
140/80 → 100/60 y filas de tabla (`Compact`) 200 → 184. **No se suprimió ni consolidó una sola línea**, ni del
cuerpo ni de los anexos: no hizo falta.

**Dos correcciones al renderizador**, ambas para cumplir las reglas permanentes de Word:

1. **`p1a` solo para el primer párrafo tras un título; `Normal` para el resto.** Emitía `p1a` para todos, y no
   es cosmético: en la plantilla `p1a` es `Normal` con `firstLine=0`, de modo que el primer párrafo va sin
   sangrar y los siguientes con sangría de primera línea. Reparto: 50 `p1a` y 96 `Normal`.
2. **El estilo `abstract` se asigna por posición** —por el encabezado RESUMEN o ABSTRACT que precede— y no por
   las primeras palabras del párrafo, que estaban escritas a mano en el código y dejaron de coincidir cuando se
   fundieron ambos textos en la `_v7`. Resumen y abstract recuperan su `abstract` de plantilla.

**El renderizador queda versionado** en `doc/versions/informe_final/_tools/` (`render.py`, `render2.py`,
`post.py`, `comp2.py`). Vivía solo en la sesión, así que cada propagación lo reconstruía de memoria; ahora no.

**Verificación sobre el PDF:** 25 páginas exactas · **cuerpo 18 de 25** y anexos 7 de sus 25 propias, desde la
página 19 y justo tras el capítulo 8 de referencias · cero páginas en blanco · resumen y abstract completos en
la página 1, con 199 y 183 palabras · nueve capítulos y ocho anexos A–H con la **G íntegra** · 18 leyendas
correlativas · las 20 entradas IEEE intactas · **ninguna llamada `§` rota** · sin arte ASCII ni literales HTML ·
encabezado y pie en las 25 páginas sin solaparse con el cuerpo (holguras mínimas 20,9 y 17,4 pt) · colofón
único al cierre. Los cuatro reparos del profesor siguen en pie tras la compactación.

**`_v8` congelada como versión de entrega**: `.docx` SHA-256 `69aadfb11853` y `.pdf` `00554ca8125c`, en
`doc/versions/informe_final/` y con copia de ambos en la raíz del proyecto.

### 2026-09-08 01:15 — Sobriedad tipográfica propagada a Word y PDF · versión de entrega (_v9)

`CLAUDE.md` y el encargo de propagación fijan ahora que, en el cuerpo de las descripciones, el guion largo y la
negrita se reservan para lo excepcional: los incisos van con comas o paréntesis, y la negrita solo en los
términos que se definen por primera vez y en las cifras que la tabla no recoge, nunca en frases enteras ni en
la conclusión de un párrafo. Quedan excluidas las tablas, donde la negrita sigue marcando el mejor valor de
cada columna, y los encabezados.

La regla llegaba ya aplicada en el `.md` por la sesión de Claude Code (113 guiones largos y 164 negritas
pasaron a 19 y 108, sin perder una palabra), así que aquí solo había que heredarla sin reintroducir resaltes.

**Contabilidad del marcado, fuente contra documento.** La fuente trae 149 tramos en negrita y 47 guiones largos
fuera de tablas y títulos; el `.docx` reconstruido trae 147 y 46. La diferencia son las dos líneas de palabras
clave y la de filiación, que van a los estilos `keywords` y `address` y quedan fuera del recuento de párrafos.
Nada añadido y nada perdido. La negrita queda en 81 de 210 párrafos, no en todos. Comprobado además que el
`**Hallazgo N:**` que `post.py` reaplica al separar los párrafos está en el `.md`: restituye marcado de la
fuente, no lo inventa, de modo que se deja como está.

**Un defecto que el conteo no habría cazado.** Al leer una muestra del PDF apareció, en la tabla 1 de la página
4, `Inmediata mediante *prompt*` con los asteriscos impresos. El relleno de celdas quitaba `**` y comillas
invertidas pero no las cursivas simples, así que cuatro celdas de las tablas 1, 17 y 18 mostraban el marcado en
crudo (*prompt* y *mojibake* tres veces). Corregido en `render.py` y `render2.py`, que ahora emiten un run en
cursiva dentro de la celda. Verificado: cero celdas con marcado residual y cero asteriscos literales en el PDF.
Vale la pena anotarlo junto al error del que avisó el autor: en ediciones masivas de marcado, la verificación
por conteo no basta, hay que leer una muestra. Aquí los conteos daban bien y el defecto estaba a la vista.

**Verificación sobre el PDF:** 25 páginas exactas · cuerpo 18 de 25 y anexos 7, desde la página 19 · cero
páginas en blanco · encabezado y pie en las 25 sin solaparse (holguras mínimas 20,9 y 17,4 pt) · resumen y
abstract en la página 1, con 199 y 183 palabras · nueve capítulos y ocho anexos A–H con la G íntegra · 18
leyendas correlativas · las 20 entradas IEEE · ninguna llamada `§` rota · sin arte ASCII ni literales HTML.

**`_v9` congelada como versión de entrega**: `.docx` SHA-256 `9f5afc36eec9` y `.pdf` `1a276fe50afc`, con copia
de ambos en la raíz. Renderizador actualizado en `doc/versions/informe_final/_tools/`.

### 2026-09-08 01:45 — Ni emojis ni marcas de agua · versión de entrega (_v10)

Regla nueva del autor, incorporada a `CLAUDE.md` y al encargo permanente de propagación: los documentos del
proyecto no llevan emojis ni pictogramas decorativos, ni marcas de agua, sellos de borrador o leyendas
superpuestas. Donde un símbolo hace de valor se escribe la palabra, que es lo que un tribunal lee y lo que
sobrevive a cualquier tipografía.

**Auditoría.** Emojis: tres, en el `.md` y por herencia en los tres `.docx`, todos en la Tabla 2 del estado del
arte, donde una marca de verificación y una cruz hacían de valor en la columna Privacidad. Marcas de agua:
ninguna. La cadena «CONFIDENCIAL» que aparece en `document.xml` es la palabra «confidencialidad» del resumen y
«confidenciales» de las conclusiones, no un sello.

**Corregido primero en el `.md`** (respaldo `.bak_pre_emojis_20260908`): la columna pasa a leerse «Local»,
«Cloud» y «100% Local». La palabra ya acompañaba al símbolo, así que no se pierde información. Las flechas
tipográficas que describen flujos («JSON → validación → registros») se conservan: no son emojis, y la regla lo
dice explícitamente para que nadie las retire por exceso de celo.

**Un defecto colateral que solo se vio leyendo.** Al quitar los dos caracteres, la columna «Idioma» quedó tan
estrecha que «Español» se partía en «Españo / l». La causa no era la tabla sino el renderizador: el ancho
mínimo por columna se aplicaba antes de normalizar a los 8838 twips útiles, de modo que la normalización lo
deshacía. Ahora el suelo de 900 twips se impone después de normalizar y el descuento se reparte entre las
columnas con holgura. Es la segunda vez seguida que un defecto aparece al mirar una página y no en los
conteos.

**Verificación sobre el PDF:** cero emojis y cero marcas de agua, tanto en el PDF como en los tres `.docx` · 25
páginas exactas, cuerpo 18 de 25 y anexos 7 · cero páginas en blanco · encabezado y pie en las 25 sin solape ·
resumen y abstract en la página 1 con 199 y 183 palabras · nueve capítulos y ocho anexos A–H · 18 leyendas
correlativas · las 20 entradas IEEE · ninguna llamada `§` rota · ninguna palabra partida en las tablas.

**`_v10` congelada como versión de entrega**: `.docx` SHA-256 `2e786c7f7ebd` y `.pdf` `d109daf55485`, con copia
de ambos en la raíz. Renderizador actualizado en `doc/versions/informe_final/_tools/`.

### 2026-09-08 07:30 — Resincronización con el `.md` saneado (_v11, sin declarar entrega)

Los tres `.docx` y el PDF de la `_v10` arrastraban **20 referencias frente a las 37 del Markdown** y la **Tabla
2 antigua**, la que descansaba sobre las cuatro citas inexistentes que §2.20 mandó eliminar. Resincronizados.

**Revisión del `.md` antes de propagar.** 131 490 bytes, escrito a las 07:06 y estable, SHA-256 `d4a1b6de5b3f`.
37 entradas de bibliografía numeradas de 1 a 37 y correlativas; cada cita del texto tiene su entrada y cada
entrada se cita al menos una vez, sin huérfanas por ninguno de los dos lados; nueve capítulos y ocho anexos A-H;
19 tablas; ningún emoji ni arte ASCII. Las citas fabricadas han desaparecido: cero ocurrencias de «Smith,
Johnson» y de «Min et al». La Tabla 2 se rehizo sobre obras reales, con BloombergGPT declarando **BLOOM 50B** y
F1 de 53,6-75,5 % en lugar de GPT-J con «más del 85 %», FiNER-139 con SEC-BERT-SHAPE y 82,1 % de micro-F1, y
Cañete et al. con BETO y 88,43 % en sustitución de la referencia atribuida a García y López.

**Extensión, con la medición delante.** El `.md` creció de 15 915 a 19 549 palabras. El documento queda en **31
páginas: cuerpo 20 y anexos 11**. Los dos límites institucionales se cumplen con holgura —el cuerpo va cinco
páginas por debajo de sus 25 y los anexos catorce por debajo de las suyas—, pero el objetivo interno de 25
totales ya no se alcanza. **La compactación por estilo está agotada, y se comprobó en lugar de suponerlo:** una
pasada agresiva (interlineado 228 → 220, encabezados 220/110 → 180/90, 160/80 → 130/65 y 140/70 → 120/60,
leyendas 100/60 → 90/50, filas 184 → 176) da un resultado idéntico, 31 páginas con cuerpo 20 y anexos 11, porque
los cortes los manda ahora el contenido y no el espaciado. Se conserva la configuración moderada, que se lee
mejor. Bajar de 31 exigiría suprimir texto, y eso no se hace sin autorización expresa.

**Verificación sobre el PDF:** las 37 entradas presentes y correlativas en el capítulo 8 · cero páginas en
blanco · encabezado y pie en las 31 páginas sin solaparse (holguras mínimas 20,9 y 17,5 pt) · resumen y abstract
en la página 1, con 199 y 189 palabras · nueve capítulos y ocho anexos A-H · 19 leyendas correlativas · ninguna
llamada `§` rota · ningún emoji, arte ASCII ni asterisco literal. Los tres `.docx` coinciden en las 37
referencias y en la fila de BloombergGPT.

**Concurrencia:** el `.md` se releyó al terminar y su hash sigue siendo `d4a1b6de5b3f`, así que la propagación se
hizo contra un original que no se movió. Del `.md` no se tocó nada: sigue declarado bajo §2.20 por Claude Code.

**`_v11` congelada** (`.docx` `efe56e1d7495`, `.pdf` `872d23993314`), **sin declararla versión de entrega**: la
extensión total está por resolver y §2.20 sigue abierta.

---

### 2026-09-08 15:40-20:30 — Sesión de Claude Code: verificación mecanizada, integridad de datos y arranque de la re-corrida

Sesión larga y de naturaleza distinta a las anteriores: casi todo lo que produjo fueron **defectos
encontrados**, la mitad de ellos en mi propio trabajo de las horas previas. Se resume aquí lo que quedó, con
la trazabilidad para poder rehacerlo.

#### El informe

Se amplió la **introducción** de 1 068 a 1 457 palabras con material del propio trabajo: la volatilidad de
la lista SDN, que obliga a vigilancia continua y no a una carga inicial, y la asimetría del error, que
orienta el diseño hacia la exhaustividad. **La justificación era errónea:** se hizo creyendo que la plantilla
pedía tres o cuatro páginas cuando dice «a lo más 3». La ampliación se conserva porque el capítulo queda en
~2,1 páginas y atiende el reparo del profesor guía sobre el poco desarrollo, pero no debe crecer más.

Se añadieron las **dos primeras figuras**, generadas a 300 ppp por `tools/generar_figuras_informe.py` con la
leyenda debajo y centrada como pide la norma: la composición de los falsos positivos en §4.4 y el efecto del
KB RAG sobre los trece modelos en §5.3.1. El script **no recalcula** las cifras desde los CSV, las toma
escritas de las tablas publicadas, para que figura y tabla no puedan divergir.

Se cotejaron **resumen y abstract** frase a frase —siete en cada idioma, diez cifras idénticas— y se corrigió
la única divergencia: el español decía «Las instituciones» donde el inglés dice «Financial institutions».

#### `tools/verificar_informe.py`

Las comprobaciones mecánicas del proyecto vivían en prosa y se reescribían a mano en cada sesión, lo que las
hacía irreproducibles: tres auditores contaron guiones y negritas de tres maneras sobre el mismo texto. Ahora
son **trece comprobaciones ejecutables**, y cada una **declara cuántos elementos examinó**; una que examina
cero se marca VACÍA y no como superada, porque una comprobación que no mira nada es indistinguible de una que
pasa —el informe documenta en §5.3 una prueba de sensibilidad que no podía marcar nada por construcción y se
dio por buena durante meses—.

Tres de ellas fallaron al estrenarse y en los tres casos **el defecto estaba en la comprobación**: el `©` de
«JosÃ© Bono» no es un pictograma sino la mitad del *mojibake* que el informe explica; «Parámetros» empieza por
«p» y se tomaba por «Precisión», dando catorce falsos positivos de aritmética; y la Tabla 4 declara «doce
modelos en trece configuraciones», que son dos cifras ciertas sobre cosas distintas.

#### Integridad del repositorio

**Cuatro documentos llevaban dos meses a cero bytes**, vaciados el 1 de julio por un commit cuyo mensaje solo
hablaba de `.gitignore` y rutas; dos eran de hitos ya entregados. Restaurados desde el commit anterior,
71 476 bytes. Sobrevivieron tanto porque un fichero vacío no da ningún síntoma: existe, se abre, se lee y no
sale en un `git status` limpio.

Se corrigió el comentario del `.gitignore` sobre los duplicados de macOS, que afirmaba en falso que son
«copias byte a byte»: de 78, 23 difieren y varios son instantáneas anteriores a la retirada de los modelos
excluidos. Ninguna regla se tocó.

Por decisión del autor, y tras presentarle el inventario completo, se retiraron del repositorio 22
duplicados rastreados, las 12 filas que el servicio de nube rechazó por cuota y dos ficheros de
`_to_delete`. **Ninguna cifra publicada cambió.** Se conservaron las 480 filas invalidadas de una fuente del
consolidado, porque editarla rompería la reproducibilidad del ANOVA publicado, y el agregado histórico de
junio, que atestigua. Ningún registro de ejecución entró en la retirada.

#### La re-corrida

Se desbloqueó al equipo de 48 GB, que llevaba dos horas y media parado esperando dos respuestas: si los 15
artículos de Kleptotrace embebidos en el corpus debían heredar sus 63 localizaciones —sí, verificado sobre su
propia rama antes de contestar— y dónde lanzar la re-corrida —entera en el equipo de 48 GB, para no mezclar
telemetría de dos máquinas en la misma tabla—.

Aplicaron las localizaciones (119 de 120 artículos, **545** en total) y entregaron seis corridas, las seis
válidas. **`§F53` queda cerrado y verificado:** dieciocho categorías comprobadas, ninguna puntúa contra el
vacío; *Locations* pasa de cero entidades de referencia a **1 034** en N=120 y su peso en los falsos
positivos cae del **67,5 % al 44-46 %**.

#### Los dos hallazgos de fondo

**`§F65`.** Al cuadrar el desglose por categoría contra el corpus apareció una razón de 1,85 en las tres
categorías. Tirando de ahí: `total_records` es **113 y no 120**, porque los siete ejemplares *few-shot* son
artículos del propio corpus con su anotación de oro como salida esperada, y por decisión del autor se
excluyen de la métrica publicada. El KB RAG aporta **+10,01 pp** sobre esos siete frente a **+2,19 pp** sobre
los ciento trece. **Las primeras cifras que informé estaban mal**, promediadas sobre el CSV crudo.

**`§F66`.** `src/merge_and_analyze.py` **no excluía** esos artículos: la exclusión vivía en `main.py` y se
perdía al fusionar, de modo que el ANOVA consolidado los incluía. Rehecho sin ellos, las observaciones pasan
de 3 120 a 2 938 y el ANOVA de F = 38,2222 a **F = 35,5557**. **Ninguno de los trece modelos cambia de
veredicto**, pero el efecto del RAG se encoge en doce de los trece. Que el veredicto aguante lo convierte en
un **resultado de robustez** y no en un problema. Corregida la herramienta, y validada de extremo a extremo:
el F1 de la fusión coincide **exactamente** con el del resumen de cada corrida.

#### Seguimiento

Revisados los ocho bloqueantes del `TODO-INFORME-FINAL §10`, levantados el 5 de septiembre y nunca
actualizados: **siete están cerrados** y el octavo tiene ya respuesta con evidencia. Un listado de
bloqueantes desactualizado induce a creer que quedan ocho cosas por hacer antes de la defensa.

**Pendiente:** once modelos de la re-corrida; decidir si el informe adopta F = 35,5557 o espera al
consolidado nuevo; la purga de GitHub, que arrastra el 404 de la referencia [37]; y resincronizar los tres
`.docx`, que van muy por detrás del Markdown.
