# Requerimientos de Software y Proyecto (Enriquecidos para Tesis Final)

Este documento contiene los requerimientos técnicos del proyecto, ahora alineados con la estructura y estándares de la tesis final del Magíster en TI.

## 1. Contexto y Definición del Problema
El proyecto aborda la necesidad crítica en el sector financiero (Compliance/KYC) de automatizar la extracción de entidades (Personas, Organizaciones, Ubicaciones) de noticias en español para mitigar riesgos regulatorios.

## 2. Requerimientos Funcionales (RF)

### 2.1 Gestión de Datos e Ingesta
- **RF1.1 Carga de Datasets:** Capacidad de cargar datasets en formato JSONL/CSV (ej. OpenSanctions).
- **RF1.2 Gestión de Ground Truth:** Soporte para corpus anotado con esquemas IOB/XML.
- **RF1.3 Validación de Acuerdo:** Implementación de métricas de acuerdo inter-anotador (Cohen's Kappa).
- **RF1.4 Procesamiento en Batch y Paralelo:** Ejecución eficiente mediante arquitectura Pub/Sub (Redis/ZeroMQ) para escalabilidad industrial.

### 2.2 Extracción con LLM y RAG
- **RF2.1 Ejecución Local (Privacidad):** Integración vía API con motores locales (Ollama) para evitar fuga de datos (GDPR/Compliance).
- **RF2.2 Arquitectura RAG de Contexto Único:** Implementación de técnica donde cada noticia es el único contexto para prevenir alucinaciones.
- **RF2.3 Extracción Estructurada:** Obligatoriedad de salida en formato JSON estandarizado para facilitar el parsing automático.

### 2.3 Evaluación y Métricas (KPIs)
- **RF3.1 Comparación Automatizada:** Algoritmos para comparar resultados vs. Ground Truth.
- **RF3.2 Métricas de Performance (NLP):** Cálculo de Precision, Recall, F1-Score y Hallucination Rate.
- **RF3.3 Análisis Estadístico:** Generación de datos para pruebas ANOVA y Tukey post-hoc.

### 2.4 Reporting y Visualización
- **RF4.1 Confusion Matrix:** Generación segmentada por tipo de entidad.
- **RF4.2 Dashboard Streamlit:** Interfaz para visualización, filtrado y validación cualitativa.

### 2.5 Error Handling & Data Integrity (New Section - Enhancement)
- **FR5.1 Schema Validation:** The system must validate the schema of incoming news articles and ground truth datasets before processing to prevent pipeline breaks.
- **FR5.2 Model Output Sanitization:** In case of malformed JSON from LLMs, the system must attempt to recover or log a specific "Extraction Error" event without terminating the batch process.
- **FR5.3 Data Provenance:** Every extraction result must be linked back to its source article ID and model version for auditability.

## 4. Requerimientos No Funcionales (RNF)

### 4.1 Seguridad y Cumplimiento
- **RNF1.1 Zero Data Leakage:** Ejecución local estricta; prohibición de uso de APIs externas propietarias (OpenAI/Google).
- **RNF1.2 Auditoría:** Generación de logs estructurados para trazable del proceso.

### 4	2 Eficiencia Operacional
- **RNF2.1 Rendimiento de Latencia:** Reducción del tiempo de análisis de horas a minutos/segundos por noticia.
- **RNF2.2 Uso de Recursos:** Gestión eficiente de memoria GPU/CPU para prevenir fallos OOM durante el ciclo de modelos.

## 5. Criterios de Aceptación (Para la Tesis Final)
Una vez completado el desarrollo, se considerarán cumplidos los objetivos si:
1. El sistema demuestra un **F1-Score ≥ 85%** en el corpus de prueba.
2. La **Tasa de Alucinación es < 5%**.
3. Se ha demostrado estadísticamente la superioridad del método LLM+RAG sobre la línea base humana ($p < 0.05$).
4. El prototipo Streamlit permite la inspección cualitativa y el filtrado por modelo de forma fluida.
