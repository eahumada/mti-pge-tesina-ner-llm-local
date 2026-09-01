# Índice — Hito 5: Tarea 4 — Informe Final de Tesina

**Programa:** Magíster en Tecnologías de la Información (MTI) — PGE-25  
**Estudiante:** Eduardo Mauricio Ahumada Gallardo  
**Descripción:** Documentos de trabajo, reportes analíticos, historias de usuario, requisitos y referencias bibliográficas que sustentan la redacción del informe final de tesina. Entrega estimada: 31 de julio 2026.

---

## Documentos Analíticos del Proyecto

| Fecha Creación | Archivo | Tamaño | Descripción |
| :---: | :--- | :---: | :--- |
| 2026-06-28 | `2026-06-28_REQUIREMENTS_SUMMARY.md` | 6 KB | Resumen ejecutivo de los 42 requisitos funcionales (FR) y no funcionales (NFR/RNF) del sistema |
| 2026-06-28 | `2026-06-28_TRACEABILITY_MATRIX.md` | 8 KB | Matriz de trazabilidad que mapea código fuente con cada requisito y historia de usuario |
| 2026-06-28 | `2026-06-28_DATASET_RESEARCH.md` | 2 KB | Investigación y recomendación del dataset principal (Kleptotrace/CoNLL-2002) para evaluación NER |
| 2026-06-28 | `2026-06-28_INTEGRATION_RESULTS.md` | 3 KB | Resultados de integración y evaluación del pipeline sobre el dataset de sanciones financieras |
| 2026-06-28 | `2026-06-28_TODO.md` | 7 KB | Lista completa de tareas mapeadas a las 21 historias de usuario (117 tareas completadas) |
| 2026-06-28 | `2026-06-28_SPRINT_SCHEDULE.md` | 2 KB | Calendario de sprints del proyecto con fechas y entregables |
| 2026-07-01 | `2026-07-01_EXECUTIVE_SUMMARY.md` | 7 KB | Resumen ejecutivo del proyecto: métricas clave, contribuciones investigativas y pitch de defensa (5 min) |
| 2026-07-01 | `2026-07-01_THESIS_PROJECT_ANALYSIS_REPORT.md` | 55 KB | Informe de análisis completo del proyecto (~60 páginas): trazabilidad de requisitos, historias de usuario, tasa de completitud (117/117 tareas) y contribuciones de investigación |
| 2026-07-01 | `2026-07-01_DEFENSE_CHECKLIST.md` | 15 KB | Checklist de preparación para la defensa oral: plan de estudio 5 días, guión de demo, estructura de diapositivas y Q&A anticipado |
| 2026-07-01 | `2026-07-01_F1_IMPROVEMENT_ROADMAP.md` | 23 KB | Hoja de ruta para cerrar la brecha F1 (70% → 85%): 3 fases (quick wins, escalamiento de modelo, fine-tuning) con ganancias estimadas |
| 2026-07-01 | `2026-07-01_GEMMA_MODELS_INVESTIGATION.md` | 23 KB | Investigación comparativa de variantes del modelo Gemma (2B, 7B, 12B, 27B, 31B) y sus footprints de VRAM en Apple M4 |
| 2026-07-01 | `2026-07-01_GEMMA_QUICK_START.md` | 11 KB | Guía rápida de prueba de modelos Gemma en 30 minutos a 2 horas en hardware local |
| 2026-07-01 | `2026-07-01_REPORTS_INDEX.md` | 10 KB | Índice central de todos los reportes generados con estadísticas clave de referencia rápida |
| 2026-07-01 | `2026-07-01_WORKLOG.md` | 20 KB | Bitácora completa de actividades del proyecto (junio–julio 2026): implementaciones, correcciones de bugs, resultados de benchmark y decisiones técnicas |
| 2026-07-01 | `2026-07-01_BACKLOG.md` | 3 KB | Registro de mejoras, bugs resueltos y validaciones de arquitectura del pipeline NER |
| 2026-07-01 | `2026-07-01_RESEARCH_INCONTEXT_BATCHING.md` | 7 KB | Análisis técnico y académico de In-Context Batching vs. procesamiento individual para tesina |

---

## Referencias Bibliográficas (`referencias/`)

| Fecha Creación | Archivo | Tamaño | Descripción |
| :---: | :--- | :---: | :--- |
| 2026-06-28 | `referencias/2026-06-28_annotated_references.md` | 6 KB | 10 referencias anotadas y mapeadas a módulos del codebase (Lewis RAG, Devlin BERT, BloombergGPT, etc.) |
| 2026-06-28 | `referencias/2026-06-28_more_references.md` | 5 KB | 10 referencias adicionales sobre LLMs para NER, evaluación RAG y auditoría de cumplimiento financiero |
| 2026-06-28 | `referencias/2026-06-28_bibliography.bib` | 5 KB | Archivo BibTeX con todas las citas académicas del proyecto para uso en LaTeX |

---

## Historias de Usuario (`historias_de_usuario/`)

21 historias de usuario completadas — todas creadas el 2026-06-28.

| Archivo | Descripción |
| :--- | :--- |
| `2026-06-28_HU01.md` | HU01 — Ingestión y adaptación del dataset balanceado Kleptotrace/CoNLL-2002/CoNLL-2002 |
| `2026-06-28_HU02.md` | HU02 — Control de calidad de anotaciones (Cohen's Kappa) |
| `2026-06-28_HU03.md` | HU03 — Ejecución de LLM local con Ollama |
| `2026-06-28_HU04.md` | HU04 — Rotación de modelos con liberación de VRAM |
| `2026-06-28_HU05.md` | HU05 — Cola Pub/Sub multithreading |
| `2026-06-28_HU06.md` | HU06 — Resumabilidad con checkpoint Redis-ready |
| `2026-06-28_HU07.md` | HU07 — Matching difuso de entidades (Fuzzy Matching) |
| `2026-06-28_HU08.md` | HU08 — Tasa de alucinaciones (Hallucination Rate) |
| `2026-06-28_HU09.md` | HU09 — Validación estadística ANOVA y Tukey HSD |
| `2026-06-28_HU10.md` | HU10 — Logs auditables y trazabilidad completa |
| `2026-06-28_HU11.md` | HU11 — Dashboard Streamlit interactivo |
| `2026-06-28_HU12.md` | HU12 — Explorador de trazas de extracción |
| `2026-06-28_HU13.md` | HU13 — Descarga de pesos VRAM entre modelos |
| `2026-06-28_HU14.md` | HU14 — Métricas de latencia por artículo |
| `2026-06-28_HU15.md` | HU15 — Localización al español (prompts y UI) |
| `2026-06-28_HU16.md` | HU16 — Verificaciones de aceptación automáticas |
| `2026-06-28_HU17.md` | HU17 — Análisis de sensibilidad con outliers |
| `2026-06-28_HU18.md` | HU18 — Simulación de producción diaria |
| `2026-06-28_HU19.md` | HU19 — Taxonomía fina de errores NER |
| `2026-06-28_HU20.md` | HU20 — Estudio de ablación de prompts few-shot |
| `2026-06-28_HU21.md` | HU21 — Índice de eficiencia de hardware (Tok/s/B) |
| `2026-06-28_README.md` | Índice general de historias de usuario |

---

## Requisitos Formales (`requisitos/`)

42 requisitos (FR + NFR + RNF) — REQ01–REQ39 creados el 2026-06-27; REQ40–REQ42 creados el 2026-06-28.

| Rango | Tipo | Descripción |
| :--- | :---: | :--- |
| REQ01–REQ20 | FR | Requisitos Funcionales del pipeline NER-LLM |
| REQ21–REQ37 | NFR | Requisitos No Funcionales (rendimiento, VRAM, latencia) |
| REQ38–REQ39 | RNF | Requisitos Regulatorios/No Funcionales (privacidad, reproducibilidad) |
| REQ40 | FR | Taxonomía de errores NER (Boundary, Type Confusion, Extrinsic Hallucination) |
| REQ41 | FR | Estudio de ablación de prompts few-shot |
| REQ42 | NFR | Índice de eficiencia de hardware normalizado (Tok/s/B) |
