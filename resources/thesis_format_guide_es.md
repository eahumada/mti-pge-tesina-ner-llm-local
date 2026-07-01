# Guía de Formato para la Tesis Final (MTI - USM)

Este documento sirve como referencia estructural y estilística para la redacción del informe final de tesis (tesina) para el Magíster en Tecnologías de la Información (MTI). Su objetivo es asegurar la consistencia con los estándares exigidos por la Universidad Técnica Federico Santa María.

## 1. Estructura General de la Tesis

La tesis debe seguir una progresión lógica, reflejando el ciclo de vida del proyecto de investigación-desarrollo:

| Sección | Contenido Principal | Referencia en Proyecto |
| :--- | :--- | :---        |
| **Resumen (Abstract)** | Resumen informativo (máx. 300 palabras) con contexto, problema, solución, metodología y resultados esperados. | `doc/organizado/Instructions/propuesta_tesina-formulario-2025.md` |
| **Introducción / Contexto** | Definición del problema de negocio o técnico (ej. Compliance), impacto en la industria e importancia tecnológica. | `doc/organizado/Tasks/TAREA_N2_Formulacion...md` (Secc. 1.3) |
| **Marco Teórico y Estado del Arte** | Conceptos clave (RAG, LLMs, NER), revisión de literatura técnica y comparación con soluciones existentes (propietarias vs. abiertas). | `doc/organizado/Tasks/TAREA_N2_Formulacion...md` (Secc. II) |
| **Propuesta Técnica** | Descripción detallada de la arquitectura (Pipeline RAG, Ollama), ingeniería de prompts y metodología de implementación. | `doc/organizado/Tasks/TAREA_N2_Formulacion...md` (Secc. II.c) |
| **Metodología de Investigación** | Diseño experimental, definición de variables (Precisión, Recall, F1), proceso de etiquetado y análisis estadístico. | `doc/organizado/Tasks/TAREA_N2_Formulacion...md` (Secc. II.b) |
| **Resultación y Discusión** | Presentación de experimentos, métricas obtenidas (F1-Score, Hallucination Rate), comparación estadística con la línea base humana. | Implementado en fases finales del cronograma. |
- **Conclusiones y Trabajo Futuro** | Resumen de hallazgos, cumplimiento de objetivos y propuestas para escalabilidad o nuevos modelos. | - |
| **Referencias Bibliográficas** | Listado completo de fuentes citadas siguiendo el formato IEEE. | `doc/organizado/Tasks/TAREA_N2_Formulacion...md` (Secc. II) |

## 2. Estilo y Redacción

- **Idioma:** El cuerpo del texto debe escribirse en **Español**, pero es fundamental mantener la precisión terminológica técnica.
  - Términos técnicos en Inglés que se deben usar sin traducir: *Recall, Precision, F1-Score, Hallucination Rate, RAG (Retrie_Augmented_Generation), Prompt Engineering, Pipeline, Batch Processing, Ground Truth, One-shot/Few-shot learning*.
  - Las fuentes de datos y literaturas citadas (ej. Papers en inglés) deben referenciarse respetando su idioma original en la bibliografía.
- **Tono:** Académico, objetivo e impersonal. Se prefiere el uso de la tercera persona ("Se realizó...", "El sistema permite...") o la primera persona del plural ("Realizamos...").

## 3. Estándares de Cita y Referencia

**IMPORTANTE:** El formato obligatorio para todas las citas y referencias bibliográficas es **IEEE**.

- **Cita en texto:** Se utiliza un número entre corchetes, por ejemplo: `[1]`, `[2]-[4]`.
- **Lista de Referencias:** Debe ser numerada y contener los elementos mínimos: Autores, Título del artículo/libro, Nombre de la revista/conferencia, Volumen, Páginas y Año.

## 4. Consideraciones para el Desarrollo (Contexto de Datos)

A pesar de que la tesis se redacta en Español, el investigador debe ser capaz de procesar y reportar datos provenientes de fuentes en Inglés:
- Los resultados técnicos deben presentar métricas estandarizadas globalmente (ej. *Accuracy*, *Latency*).
- Las conclusiones sobre el desempeño del modelo deben integrar tanto la capacidad lingüística española (contexto local) como el conocimiento técnico derivado de literatura técnica internacional.

---
*Documento generado para asegurar la coherencia entre la propuesta de tesina y el informe final de grado.*