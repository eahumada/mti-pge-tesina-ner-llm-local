# Índice Maestro del Proyecto — Tesina MTI & Banco de Pruebas NER-LLM

**Proyecto:** Clasificación y Extracción de Entidades Nombradas (NER) en Noticias de Cumplimiento Normativo Corporativo Mediante Modelos de Lenguaje Grande Ejecutados Localmente con Soberanía de Datos  
**Autor:** Eduardo Mauricio Ahumada Gallardo  
**Institución:** Departamento de Informática, Universidad Técnica Federico Santa María (UTFSM) — Magíster en Tecnologías de la Información (MTI)  
**Fecha de Actualización:** 2026-10-04  

---

## Propósito de este Índice

Este documento constituye la **referencia canónica y directorio cruzado** de todos los artefactos, documentación, herramientas, código y resultados del repositorio. Permite tanto a evaluadores humanos como a sistemas de IA autónomos (Claude Code, Claude Desktop, Antigravity, Gemini) localizar con precisión cada componente del ecosistema de investigación.

---

## Tabla de Contenidos

1. [Tesina e Informes Académicos](#1-tesina-e-informes-académicos)
2. [Dashboard de Visualización Interactiva (Streamlit)](#2-dashboard-de-visualización-interactiva-streamlit)
3. [Banco de Pruebas Experimental y Benchmarks](#3-banco-de-pruebas-experimental-y-benchmarks)
4. [Herramientas de Auditoría, Verificación y Manipulación DOCX](#4-herramientas-de-auditoría-verificación-y-manipulación-docx)
5. [Coordinación Multi-Agente y Directivas de IA](#5-coordinación-multi-agente-y-directivas-de-ia)
6. [Investigación, RAG y Datasets](#6-investigación-rag-y-datasets)
7. [Defensa de Grado y Presentaciones](#7-defensa-de-grado-y-presentaciones)
8. [Seguridad, Soberanía de Datos y Gobernanza](#8-seguridad-soberanía-de-datos-y-gobernanza)
9. [Histórico de Revisiones, Encargos y Auditorías](#9-histórico-de-revisiones-encargos-y-auditorías)
10. [Requisitos, Historias de Usuario y Gestión Ágil](#10-requisitos-historias-de-usuario-y-gestión-ágil)

---

## 1. Tesina e Informes Académicos

Esta categoría agrupa los manuscritos oficiales de la tesina en sus formatos de entrega (.docx, .pdf) y su fuente textual canónica (.md).

| Documento / Artefacto | Ruta | Descripción y Rol |
|:---|:---|:---|
| **Fuente Canónica Texto (Markdown)** | [`doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md`](./doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md) | Texto completo y actualizado del informe final de tesina. Es la referencia textual que leen los agentes. |
| **Entregable Canónico (DOCX con plantilla UTFSM)** | [`Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx`](./Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx) | Versión oficial formateada en plantilla institucional MTI con estilos multinivel y numeración formal. |
| **Versión PDF Oficial Generada** | [`Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.pdf`](./Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.pdf) | Salida congelada en PDF lista para lectura y presentación. |
| **Documento Standalone de Trabajo** | [`Informe_Final_Tesina_NER.docx`](./Informe_Final_Tesina_NER.docx) | Copia de trabajo sin plantilla institucional usada en ciclos rápidos de edición. |
| **Versión Enviada al Profesor Guía** | [`doc/versions/enviados/2026-09-08_Informe_Final_Tesina_NER_ENVIADO-AL-PROFESOR-GUIA.pdf`](./doc/versions/enviados/2026-09-08_Informe_Final_Tesina_NER_ENVIADO-AL-PROFESOR-GUIA.pdf) | Registro inmutable de la entrega remitida formalmente el 2026-09-08 (disponible en PDF y DOCX). |
| **Historial Completo de Versiones** | [`doc/versions/informe_final/`](./doc/versions/informe_final/) | Contiene todas las versiones congeladas desde `v1` hasta `v16` junto a su bitácora de cambios. |
| **Glosario Oficial de Términos** | [`GLOSARIO.md`](./GLOSARIO.md) | Glosario unificado de conceptos (NER, RAG, Zero-Shot, Few-Shot, AML/KYC, Métricas, Soberanía). |
| **Formulario Informe de Avance (Hito 4)** | [`Formulario-IA-26-Rellenado.docx`](./Formulario-IA-26-Rellenado.docx) | Formulario oficial de avance curricular del hito previo debidamente cumplimentado. |
| **Guía de Formato Académico** | [`resources/thesis_format_guide_es.md`](./resources/thesis_format_guide_es.md) | Reglas tipográficas, estructura de capítulos y directivas de estilo para la tesina MTI. |

---

## 2. Dashboard de Visualización Interactiva (Streamlit)

El Dashboard es el prototipo interactivo para visualización de KPIs, análisis inferencial y validación cualitativa por parte de stakeholders.

| Componente / Documentación | Ruta | Descripción y Contenido |
|:---|:---|:---|
| **Código Fuente Principal** | [`repos/ner-llm-entity-benchmark/src/dashboard.py`](./repos/ner-llm-entity-benchmark/src/dashboard.py) | Aplicación web en Streamlit (9 pestañas interactivas, selección multi-corrida con fallback resiliente, chat local Ollama MLX con `gemma4:e2b-mlx`, cálculo estadístico al vuelo). |
| **Manual de Uso y Lanzamiento** | [`repos/ner-llm-entity-benchmark/README.md`](./repos/ner-llm-entity-benchmark/README.md) | Sección *6. Launch the Streamlit Dashboard*. Detalla el comando `streamlit run src/dashboard.py` y pre-requisitos. |
| **Documentación Arquitectónica** | [`THESIS_PROJECT_ANALYSIS_REPORT.md`](./THESIS_PROJECT_ANALYSIS_REPORT.md) | Detalle funcional y arquitectónico del Dashboard: pestañas, líneas de código (~450 LOC iniciales), cumplimiento de Criterios de Aceptación (F1 ≥ 85%, Hallucination ≤ 5%). |
| **Requisito Funcional Formal (RF4.3)** | [`repos/ner-llm-entity-benchmark/doc/REQUERIMENTS/functional_requirements.md`](./repos/ner-llm-entity-benchmark/doc/REQUERIMENTS/functional_requirements.md) | Especifica el requerimiento de prototipo web interactivo para validación de stakeholders en ambiente simulado. |
| **Requisito Enriquecido (RF4.2)** | [`repos/ner-llm-entity-benchmark/doc/REQUERIMENTS_UPDATED/functional_requirements_enriched.md`](./repos/ner-llm-entity-benchmark/doc/REQUERIMENTS_UPDATED/functional_requirements_enriched.md) | Define capacidades de filtrado por corrida, exportación y análisis cualitativo. |
| **Historia de Usuario (HU11)** | [`repos/ner-llm-entity-benchmark/doc/USER_STORIES.md`](./repos/ner-llm-entity-benchmark/doc/USER_STORIES.md) | Historia de Usuario *HU11: Streamlit Interactive Dashboard* y criterios de validación. |
| **Captura de Feedback de Stakeholders** | [`repos/ner-llm-entity-benchmark/results/ANALISIS_CONJUNTO_20260909_FIX/stakeholder_feedback.json`](./repos/ner-llm-entity-benchmark/results/ANALISIS_CONJUNTO_20260909_FIX/stakeholder_feedback.json) | Registro de evaluaciones y comentarios cualitativos ingresados desde la pestaña de feedback del Dashboard. |

### Pestañas del Dashboard (`src/dashboard.py`):
1. **📊 Comparación de Modelos:** Barras y métricas globales de F1, Precision y Recall.
2. **🧬 Análisis de Alucinaciones:** Tasas de alucinación y distribución por modelo y modo RAG.
3. **🏷️ Errores por Entidad:** Desglose de aciertos y errores por categoría (PER, ORG, LOC, MISC).
4. **📈 Significancia Estadística:** Pruebas ANOVA unidireccional y comparaciones múltiples Tukey HSD.
5. **⏱️ Eficiencia de Hardware:** Rendimiento en inferencia (tokens/segundo, consumo de memoria VRAM/RAM y CPU).
6. **🎯 Criterios de Aceptación:** Verificación visual automática de hipótesis de tesina (F1 ≥ 70% viabilidad / ≥ 85% meta) y límites seguros.
7. **🏭 Simulación Productiva:** Evaluación de latencias extremas y control de concurrencia AIMD.
8. **📝 Feedback Stakeholders:** Formulario para registrar utilidad operativa y reducción de carga de trabajo.
9. **💬 Chat con Resultados (Local):** Agente de consulta conversacional en lenguaje natural conectado a Ollama local (`gemma4:e2b-mlx`).

---

## 3. Banco de Pruebas Experimental y Benchmarks

El subproyecto `repos/ner-llm-entity-benchmark/` es el motor experimental del estudio.

| Componente | Ruta | Descripción |
|:---|:---|:---|
| **Catálogo Experimental** | [`repos/ner-llm-entity-benchmark/BENCHMARKS.md`](./repos/ner-llm-entity-benchmark/BENCHMARKS.md) | Registro de modelos evaluados (13 modelos finales), configuraciones, parámetros e historia experimental. |
| **Especificación de Arquitectura** | [`repos/ner-llm-entity-benchmark/PROJECT_PROMPT.md`](./repos/ner-llm-entity-benchmark/PROJECT_PROMPT.md) | Diseño de arquitectura desacoplada pub/sub multihilo con Factory/Facade y control de saturación. |
| **Motor de Ejecución (Main)** | [`repos/ner-llm-entity-benchmark/src/main.py`](./repos/ner-llm-entity-benchmark/src/main.py) | Punto de entrada principal para inferencia, evaluación, cálculo de F1 macro/micro y guardado de resultados. |
| **Conectores de Modelos** | [`repos/ner-llm-entity-benchmark/src/providers/`](./repos/ner-llm-entity-benchmark/src/providers/) | Conectores para Ollama local (`ollama_provider.py`), vLLM, y adaptadores cloud controlados. |
| **Corpus y Datos de Prueba** | [`repos/ner-llm-entity-benchmark/data/`](./repos/ner-llm-entity-benchmark/data/) | Conjuntos de datos: `benchmark_balanced_120.json` (N=120), corpus CoNLL-2002, diccionarios OFAC y sanciones. |
| **Scripts de Ejecución Automatizada** | `repos/ner-llm-entity-benchmark/run_*.sh` | `run_benchmark.sh`, `run_remoto_chain.sh`, `run_cloud_resilient.sh` para corridas desatendidas. |

### Corridas de Resultados Clave (`repos/ner-llm-entity-benchmark/results/`):
- 🏆 **`ANALISIS_CONJUNTO_20260909_FIX/`**: **Corrida Canónica Principal (Tabla 7)**. Contiene `merged_results.csv` con los 13 modelos evaluados sobre N=113 artículos limpios (después de excluir los 7 artículos con mojibake). F1 macro global de 82.94% para el modelo líder (`gemma4:31b-cloud_kb_rag`).
- 📊 **`R2_CONSOLIDADO_5SEMILLAS_20260916/`**: **Consolidado de Robustez de 5 Semillas (Anexo K)**. 12.430 registros de inferencia consolidados con intervalos de confianza al 95%. F1 medio de 82.97%.
- 🔬 **`barras_error_n120_REMOTO/`**: Desglose por semilla individual (`seed_42`, `seed_123`, `seed_456`, `seed_789`, `seed_1024`).
- 🔬 **`validacion_n30_es_REMOTO/`**: Validación en español sobre N=30 con variantes de prompt R4/R5 (F1 hasta 88.43%).
- 🔬 **`n30_rerun_REMOTO/`**: Validación de dominio AML/KYC sobre 30 artículos en inglés (F1 80.57% baseline / 90.16% RAG).

---

## 4. Herramientas de Auditoría, Verificación y Manipulación DOCX

Colección de scripts utilitarios en Python desarrollados para garantizar la rigurosidad científica y la integridad de los entregables.

| Script / Herramienta | Ruta | Finalidad y Operación |
|:---|:---|:---|
| **Verificador Integral del Informe** | [`tools/verificar_informe.py`](./tools/verificar_informe.py) | Herramienta pre-commit que audita consistencia de cifras, citas de tablas, conteos y sincronización de datos con resultados. |
| **Auditor de Afirmaciones** | [`tools/auditar_afirmaciones.py`](./tools/auditar_afirmaciones.py) | Verifica que ninguna afirmación en `FINDINGS.md` o bitácoras contradiga los archivos de datos reales. |
| **Detector de Desfases DOCX** | [`tools/desfase_cifras_docx.py`](./tools/desfase_cifras_docx.py) | Extrae valores numéricos de las tablas del `.docx` y los compara contra los CSVs/JSONs de resultados. |
| **Reescritura Quirúrgica de Celdas** | [`tools/docx_reescribir_celdas.py`](./tools/docx_reescribir_celdas.py) | Actualiza celdas específicas en tablas DOCX preservando estilos, fuentes y propiedades de párrafo intactas. |
| **Reemplazo de Terminología DOCX** | [`tools/docx_replace_terms.py`](./tools/docx_replace_terms.py) | Aplica correcciones léxicas uniformes a través de diccionarios JSON controlados sin dañar el documento. |
| **Generador de Tabla 7** | [`tools/generar_tabla7.py`](./tools/generar_tabla7.py) | Genera y recalcula los datos de la Tabla 7 canónica directamente desde los archivos CSV de resultados. |
| **Pruebas de Robustez Estadística** | [`tools/robustez_estadistica.py`](./tools/robustez_estadistica.py) | Calcula intervalos de confianza de Student, varianzas y contrastes pareados. |
| **Propagación de Anexos J y K** | [`tools/propagar_anexos_jk_20260917.py`](./tools/propagar_anexos_jk_20260917.py) | Propaga los análisis de 5 semillas e intervalos de confianza a las tablas del informe final. |
| **Scripts de Generación de Requisitos** | [`doc/scripts/`](./doc/scripts/) | Scripts históricos para análisis de historias de usuario y matrices de trazabilidad. |

---

## 5. Coordinación Multi-Agente y Directivas de IA

Documentos maestros que regulan el trabajo colaborativo concurrente entre humanos y diferentes modelos de lenguaje.

| Documento | Ruta | Rol y Contenido |
|:---|:---|:---|
| **Coordinación Viva de Tareas** | [`CURRENT-TASKS.md`](./CURRENT-TASKS.md) | **Documento obligatorio de bloqueo y coordinación**. Declara qué agente está activo, sobre qué archivos y estado de tareas (Claude Code, Claude Desktop, Antigravity, Workflows). |
| **Evidencias Empíricas (Hallazgos)** | [`FINDINGS.md`](./FINDINGS.md) | Base de conocimiento viva estrictamente aditiva con más de 180 hallazgos certificados (§F1 a §F187). |
| **Lecciones Aprendidas** | [`LEARNING.md`](./LEARNING.md) | Registro de incidentes técnicos, lecciones de depuración y patrones de consistencia aprendidos (§L1 a §L70+). |
| **Seguimiento de Tareas de Cierre** | [`TODO-INFORME-FINAL.md`](./TODO-INFORME-FINAL.md) | Checklist exhaustivo de revisión editorial, pendientes del DOCX y del PDF. |
| **Directivas Claude Code / Desktop** | [`CLAUDE.md`](./CLAUDE.md) | Reglas de orquestación, políticas de RAG, protocolos de sincronización y tabla de entregables canónicos. |
| **Directivas Gemini y Antigravity** | [`GEMINI.md`](./GEMINI.md) / [`ANTIGRAVITY.md`](./ANTIGRAVITY.md) | Instrucciones de contexto y puntos de entrada para modelos Gemini y el entorno Antigravity CLI. |
| **Directivas Generales de Agentes** | [`AGENT.md`](./AGENT.md) / [`repos/ner-llm-entity-benchmark/AGENTS.md`](./repos/ner-llm-entity-benchmark/AGENTS.md) | Directivas de bajo nivel para el banco de pruebas: gestión de memoria de GPUs, formatos JSON y guardrails. |
| **Bitácoras y Backlogs Activos** | [`TODO.md`](./TODO.md), [`WORKLOG.md`](./WORKLOG.md), [`BACKLOG.md`](./BACKLOG.md) | Bitácoras generales de seguimiento y registros cronológicos de trabajo en el workspace. |

---

## 6. Investigación, RAG y Datasets

Documentación técnica y analítica de los módulos auxiliares de recuperación de información y optimización de prompts.

| Recurso | Ruta | Descripción |
|:---|:---|:---|
| **Investigación de RAG y Base de Conocimientos** | [`research/rag/`](./research/rag/) | Análisis de indexación en ChromaDB, recuperación semántica y experimentos de integración contextual. |
| **Roadmap de Mejora de F1** | [`doc/investigacion/F1_IMPROVEMENT_ROADMAP.md`](./doc/investigacion/F1_IMPROVEMENT_ROADMAP.md) | Estrategias evaluadas para elevar el F1-Score hacia el umbral aspiracional de 85%. |
| **Investigación de Modelos Gemma** | [`doc/investigacion/GEMMA_MODELS_INVESTIGATION.md`](./doc/investigacion/GEMMA_MODELS_INVESTIGATION.md) | Estudio de cuantizaciones, tamaños (4B, 12B, 31B) y rendimiento específico en inferencia local con MLX. |
| **Investigación del Dataset** | [`doc/investigacion/DATASET_RESEARCH.md`](./doc/investigacion/DATASET_RESEARCH.md) | Caracterización de corpus (Kleptotrace, CoNLL-2002) y distribución de entidades nombradas. |
| **Referencias Bibliográficas** | [`resources/research_references.md`](./resources/research_references.md) | Fuentes teóricas sobre NER, RAG, evaluación estadística y LLMs locales. |

---

## 7. Defensa de Grado y Presentaciones

Materiales dedicados a la sustentación oral y examen de grado ante la comisión evaluadora.

| Material | Ruta | Descripción |
|:---|:---|:---|
| **Banco de Preguntas y Respuestas** | [`DEFENSA-PREGUNTAS-Y-RESPUESTAS.md`](./DEFENSA-PREGUNTAS-Y-RESPUESTAS.md) | Guía exhaustiva de preparación ante consultas metodológicas, estadísticas, de soberanía y arquitectura. |
| **Checklist de Defensa** | [`DEFENSE_CHECKLIST.md`](./DEFENSE_CHECKLIST.md) | Lista de verificación operativa y académica previa a la sesión de examen. |
| **Presentación Oficial (PPTX y PDF)** | [`doc/presentaciones/Tesina_MTI_IA_Aplicada.pptx`](./doc/presentaciones/Tesina_MTI_IA_Aplicada.pptx) / [`.pdf`](./doc/presentaciones/Tesina_MTI_IA_Aplicada.pdf) | Diapositivas preparadas para la exposición final. |
| **Herramientas de Apoyo a la Presentación** | [`doc/presentaciones/_tools/`](./doc/presentaciones/_tools/) | Scripts para renderizado y diagramación de diapositivas complementarias. |

---

## 8. Seguridad, Soberanía de Datos y Gobernanza

Directivas que sustentan la justificación empresarial de la tesina (evitar fuga de información sensible).

| Aspecto | Ruta / Referencia | Definición y Acciones |
|:---|:---|:---|
| **Principio de Soberanía Local** | `CLAUDE.md`, `AGENTS.md`, `PROJECT_PROMPT.md` | Prohibición estricta de remitir datos de entidades de clientes o sanciones a APIs externas en entornos productivos. |
| **Excepción Académica Controlada** | `AGENTS.md §2` | Uso puntual y autorizado de endpoints cloud exclusivamente sobre corpus públicos de benchmark para contraste académico. |
| **Protocolo de Purga y Saneamiento** | [`doc/seguridad/SEGURIDAD-CLAVE-GOOGLE-20260908.md`](./doc/seguridad/SEGURIDAD-CLAVE-GOOGLE-20260908.md) | Registro del tratamiento y neutralización de credenciales de prueba expuestas en git. |
| **Solicitud Formal de Purga** | [`doc/seguridad/SOLICITUD-GITHUB-PURGA-20260908.md`](./doc/seguridad/SOLICITUD-GITHUB-PURGA-20260908.md) | Procedimiento de limpieza del historial de versiones. |

---

## 9. Histórico de Revisiones, Encargos y Auditorías

Memoria documental categorizada que preserva la evolución del proyecto sin saturar el espacio de trabajo activo.

- 📁 **`doc/equipo_remoto/`**:
  - `ADENDA-EQUIPO-REMOTO-20260906.md`, `ALERTA-EQUIPO-REMOTO-20260906.md`
  - `ENCARGO-CIERRE-EQUIPO-48GB-20260910.md`, `ENCARGO-EQUIPO-48GB-SOLO-CORRIDAS-VALIDAS-20260909.md`
  - `PROMPT-EQUIPO-REMOTO-48GB.md`, `PROMPT-EQUIPO-REMOTO-RECORRIDA-COMPLETA-20260908.md`
  - Encargos específicos de re-ejecución para modelos GPT-OSS y corridas N=30.
- 📁 **`doc/revisiones_y_entregas/`**:
  - `CAMBIOS-DESDE-ENVIO-PROFESOR-20260908.md`: Registro de refinamientos posteriores al primer envío.
  - `AUDITORIA_CONSISTENCIA_20260903.md`, `CIERRE-BENCHMARKS-20260907.md`, `CIERRE-RECORRIDA-PROCEDIMIENTO.md`
  - Decisiones estadísticas del autor, inventarios de erratas corregidas y estados de recorridas.
- 📁 **`doc/prompts/`**:
  - Colección de prompts especializados para Claude Desktop durante las etapas de diagramación y corrección de estilo.
- 📁 **`doc/historico/`**:
  - `HISTORIAL-CONSOLIDADO.md`: Cronología integral de hitos y decisiones técnicas.
  - Backlogs e informes de avance tempranos.

---

## 10. Requisitos, Historias de Usuario y Gestión Ágil

Documentación de ingeniería de software que valida la metodología de desarrollo del proyecto.

| Artefacto | Ruta | Descripción |
|:---|:---|:---|
| **Historias de Usuario (HUs)** | [`doc/USER_HISTORIES/`](./doc/USER_HISTORIES/) y [`doc/organized/Hito_5_Tarea4_Informe_Final/historias_de_usuario/`](./doc/organized/Hito_5_Tarea4_Informe_Final/historias_de_usuario/) | Historias de usuario HU1 a HU21 con criterios de aceptación (ACs). |
| **Requisitos del Sistema** | [`doc/REQUERIMENTS/`](./doc/REQUERIMENTS/) y [`repos/ner-llm-entity-benchmark/doc/REQUERIMENTS/`](./repos/ner-llm-entity-benchmark/doc/REQUERIMENTS/) | Especificaciones funcionales (RF) y no funcionales (RNF). |
| **Tableros y Sprints** | [`doc/KANBAN/`](./doc/KANBAN/), [`doc/SPRINTS/`](./doc/SPRINTS/) | Seguimiento de iteraciones ágiles durante la construcción del banco de pruebas. |
| **Matriz de Trazabilidad** | [`doc/historico/TRACEABILITY_MATRIX.md`](./doc/historico/TRACEABILITY_MATRIX.md) | Relación cruzada entre requisitos, historias de usuario, componentes de código y pruebas. |

---

*Nota de Gobernanza:* Cualquier nuevo documento o script significativo que se agregue al repositorio debe ser indexado en este archivo bajo su categoría correspondiente, manteniendo el principio de documentación estrictamente aditiva y trazabilidad total.
