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
El equipo de evaluación tiene **16 GB de RAM**. Los modelos `sonct988/gemma4-26b-a4b-it-q4km-256k` (16 GB)
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
