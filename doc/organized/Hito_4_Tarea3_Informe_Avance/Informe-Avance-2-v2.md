# INFORME DE AVANCE Nº2 DE PROYECTO DE TESINA
**Seminario Integrado de Investigación y Graduación (SIIG) — PGE-25**  
**Fecha de entrega:** 7 de julio de 2026  
**Programa:** Magíster en Tecnologías de la Información (MTI) — Universidad Técnica Federico Santa María  

---

## I. ANTECEDENTES GENERALES

### 1.1 Identificación del proponente y candidato a magíster

| Campo | Información |
| :--- | :--- |
| **Nombre del estudiante** | Eduardo Mauricio Ahumada Gallardo |
| **RUT** | 12.814.696-2 |
| **Contacto** | eahumada@gmail.com · +56 9 9782 8992 |
| **Título del trabajo** | Clasificación y Extracción de Entidades Nombradas (NER) en Noticias de Cumplimiento Normativo Corporativo Mediante un Modelo de Lenguaje Grande (LLM) Ejecutado Localmente con Soberanía de Datos |
| **Profesor guía** | José Luis Martí Lara |
| **Organización vinculada** | Leanstack SpA / Austranet (Contacto: Manuel Muñoz, Fundador) |
| **Programa** | Magíster en Tecnologías de la Información (MTI) — Año de ingreso 2013 |

---

## II. RESUMEN DE LA TESINA

Las instituciones financieras que deben cumplir regulaciones AML/KYC procesan manualmente grandes volúmenes de noticias sobre sanciones y lavado de activos, proceso que resulta costoso, lento y expone datos sensibles al usar APIs externas en la nube. Esta tesina diseña, implementa y evalúa un sistema soberano de extracción de Entidades Nombradas (NER) basado en modelos de lenguaje de gran tamaño (LLM) ejecutados 100% de forma local mediante Ollama en hardware Apple Silicon, eliminando toda fuga de datos confidenciales. La arquitectura emplea un pipeline pub/sub asíncrono con control adaptativo de concurrencia (AIMD) y una capa Factory/Facade que unifica 16 proveedores de modelos. La validación experimental se realizó sobre el dataset real de sanciones financieras Kleptotrace (15 artículos con anotación experta) y un corpus de 30 artículos breves diseñado para alcanzar significancia estadística (N ≥ 30). Los resultados demuestran que mediante la localización al español y el uso de prompts few-shot se alcanza un F1-Score de 79.0% con Gemma4-31B sobre el corpus ampliado, con tasa de alucinaciones del 0% y una reducción de costos operativos del 60–80% respecto a soluciones manuales o en la nube.

**Palabras clave:** Cumplimiento Normativo (AML/KYC), Reconocimiento de Entidades Nombradas (NER), LLM Local, Soberanía de Datos, Prompt Engineering.

---

## III. PLAN DE INVESTIGACIÓN

### a) Hipótesis definida y metodología de validación aplicada

La hipótesis de trabajo plantea que **es viable implementar un sistema soberano de extracción y clasificación de entidades financieras para cumplimiento corporativo (AML/KYC) utilizando modelos de lenguaje de código abierto de escala media-grande (8B–32B parámetros) ejecutados localmente**, alcanzando un desempeño competitivo en precisión y recall en idioma español (F1-Score ≥ 70%) mediante técnicas sistemáticas de prompt engineering y few-shot learning, eliminando simultáneamente la fuga de datos confidenciales y reduciendo los costos operativos en más del 60%.

La metodología de validación implementada comprende cuatro etapas:

1. **Ingestión y estructuración de datos reales:** Se procesaron noticias de lavado de activos y sanciones internacionales provenientes de la plataforma Kleptotrace, transformando sus claves nativas al esquema interno del pipeline con validación estricta de esquema y control de calidad de anotaciones mediante Cohen's Kappa.

2. **Arquitectura distribuida y control adaptativo:** Se diseñó un pipeline pub/sub multithreading con un controlador AIMD (Additive Increase Multiplicative Decrease) que regula los hilos de procesamiento en caliente según errores de rate-limiting (HTTP 429) y presión de VRAM, protegiendo el hardware local (Apple M4, 16 GB Metal) ante condiciones de desbordamiento.

3. **Estudio de ablación sistemático:** Se ejecutaron cuatro configuraciones controladas de prompt (zero-shot inglés, zero-shot español, few-shot inglés, few-shot español) sobre 16 modelos locales e híbridos integrados vía Factory/Facade, evaluando el impacto del idioma del prompt y la cantidad de ejemplos contextuales sobre el F1-Score, la precisión, el recall y la tasa de alucinaciones.

4. **Validación estadística rigurosa:** Los resultados por artículo se contrastaron mediante ANOVA de una vía y pruebas post-hoc de Tukey HSD con α = 0.05, calculando intervalos de confianza del 95% y un análisis de sensibilidad con filtrado de outliers para verificar la estabilidad de las conclusiones sobre ambos corpus (N=15 y N=30).

### b) Principales resultados y hallazgos hasta la fecha

A continuación se detallan los hallazgos más relevantes del trabajo experimental a la fecha de este informe:

1. **Viabilidad demostrada de la ejecución local soberana:** El sistema procesó artículos de cumplimiento de forma completamente local sobre Apple Silicon M4 utilizando modelos de hasta 31B parámetros (19 GB en disco), sin transmitir ningún dato a servicios externos. Esto valida la hipótesis de soberanía de datos como viable en hardware comercial de gama alta.

2. **Ganancia por localización lingüística:** La adaptación del prompt al español produjo una mejora de +7.40 puntos de F1 respecto al baseline zero-shot en inglés (62.41% → 69.81%), impulsada fundamentalmente por una mejora del 10.28% en Recall. Esto demuestra que los LLMs comprenden mejor la estructura semántica de noticias en español cuando reciben instrucciones en el mismo idioma.

3. **Ganancia adicional por few-shot learning:** La inyección de ejemplos financieros contextuales elevó el Recall máximo a 84.55% (few-shot español), aumentando la estabilidad semántica de las extracciones de nombres de Personas y Organizaciones en el dominio AML.

4. **Benchmark de 15 modelos generativos sobre Kleptotrace (15 artículos):** El mejor desempeño en el dataset original fue alcanzado por `gemma4:31b` local con un F1-Score de 67.83% y recall de 86.78%, con tasa de alucinaciones del 0.15%. El modelo compacto `llama3.2` (3B) destacó en velocidad con latencia 4.5× menor y F1 de 61.29%, evidenciando el trade-off entre calidad y eficiencia computacional.

5. **Validación sobre corpus de significancia estadística (N=30):** Se construyó el dataset `kleptotrace_augmented_30.json` (30 artículos breves anotados) para satisfacer el criterio del Teorema del Límite Central (N ≥ 30). El benchmark serial sobre este corpus produjo:
   - `gemma4:31b`: **F1 = 79.03%**, Precisión = 73.3%, Recall = 89.1%, Hallucination Rate = 0.0%.
   - `gemma4:31b-mlx`: **F1 = 77.47%**, Precisión = 73.0%, Recall = 87.2%, Hallucination Rate = 0.0%.
   - El ANOVA arrojó F = 0.141, p = 0.708, con intervalos de confianza al 95% solapados, confirmando la robustez estadística de los resultados.

6. **Control de alucinaciones bajo el umbral del 5%:** Mediante delimitadores estrictos de JSON y una cadena de parseo en cascada de 5 estrategias (JSON directo → bloque de código → escáner de llaves → reparación de truncado → fallback por regex), se mantuvo la tasa de alucinaciones extrínsecas en 0.0% en el corpus ampliado.

7. **Arquitectura extensible y reproducible:** La capa Factory/Facade permite agregar nuevos proveedores (OpenAI, Anthropic, Vertex AI) sin modificar el pipeline principal. El sistema incluye checkpointing automático para reanudar benchmarks interrumpidos sin pérdida de datos, garantizando la reproducibilidad de los experimentos.

---

## IV. ESTADO DE AVANCE DEL INFORME FINAL

*Se evalúa el estado de avance del documento escrito de la tesina (no del sistema computacional).*

| Componente del Informe | Nulo | Bajo | Medio | Avanzado | Completo |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Definición de la estructura y organización de contenidos | | | | | **X** |
| Presentación del problema y la solución | | | | | **X** |
| Marco teórico y estado del arte (con bibliografía actualizada) | | | **X** | | |
| Desarrollo de la solución y trabajo de validación | | | | **X** | |
| Análisis de resultados y conclusiones | | | | **X** | |

> **Nota aclaratoria:** La estructura completa del informe final está definida y el capítulo de presentación del problema está redactado en su versión definitiva. El capítulo de marco teórico tiene avance medio (referencias bibliográficas compiladas y anotadas, estructura definida, pero redacción académica incompleta). Los capítulos de desarrollo y análisis de resultados están en estado avanzado, con la documentación técnica generada (requisitos, historias de usuario, WORKLOG, reporte consolidado de benchmark). Falta consolidar la redacción final académica e incorporar los resultados del corpus N=30.

---

## V. PLAN DE TRABAJO

### a) Interacción con el profesor guía

La coordinación con el profesor guía José Luis Martí Lara ha sido continua durante el período de desarrollo del proyecto. A la fecha de este informe (julio 2026), las principales instancias de coordinación realizadas y planificadas son las siguientes:

1. **Julio 2026 (semana 1) — Sesión de validación metodológica:** Revisión del diseño del estudio de ablación de prompts y la selección del dataset Kleptotrace como corpus de evaluación con anotación experta de sanciones financieras reales. Se acordará complementar con un corpus de N ≥ 30 artículos para satisfacer los requisitos de significancia estadística del ANOVA y el Teorema del Límite Central.

2. **Julio 2026 (semana 1) — Definición de la taxonomía de errores:** Se discutirá y validará la clasificación de los errores de extracción NER en tres categorías (Boundary Errors, Type Confusion, Extrinsic Hallucinations), con ejemplos concretos extraídos del dataset Kleptotrace. Esta taxonomía quedará incorporada en los requisitos formales de la tesina (REQ40).

3. **Julio 2026 (semana 2) — Revisión del estado de implementación:** Sesión de revisión del avance técnico del pipeline, incluyendo la arquitectura pub/sub, el controlador AIMD y la capa Factory/Facade de proveedores LLM. Se validará la estrategia de control de alucinaciones mediante delimitadores estrictos de JSON y el mecanismo de checkpointing resumible.

4. **Julio 2026 (semana 3) — Orientación para la redacción final y visado del informe:** El profesor guía entregará orientaciones sobre la estructura del informe final de tesina, los requisitos formales del programa PGE-25, y la estrategia de presentación de la brecha de rendimiento (F1 actual vs. objetivo 85%) en el capítulo de conclusiones y trabajo futuro. Se enviará el borrador completo para revisión y visado académico antes del 29 de julio de 2026.

### b) Tareas pendientes y fechas tentativas

Las siguientes tareas constituyen el plan de trabajo final conducente a la defensa oral y al proceso de graduación:

| # | Tarea | Descripción | Fecha Estimada |
|:---:|:---|:---|:---:|
| 1 | Redacción del Marco Teórico completo | Incorporar referencias actualizadas (BERT, RAG, BloombergGPT), describir la arquitectura de Transformers, el prompting few-shot y el paradigma de modelos de lenguaje local con aumento de datos sintético. | **18 julio 2026** |
| 2 | Redacción del Capítulo de Desarrollo y Arquitectura | Documentar formalmente la arquitectura del sistema: pipeline pub/sub, Factory/Facade, AIMD, módulo de evaluación estadística y dashboard Streamlit. Incluir diagramas de componentes y secuencia. | **21 julio 2026** |
| 3 | Redacción del Capítulo de Resultados y Análisis | Incorporar las tablas finales del benchmark de 16 modelos (Kleptotrace), los resultados del corpus ampliado (N=30), el análisis estadístico (ANOVA p=0.708, IC 95%) y la taxonomía de errores. | **24 julio 2026** |
| 4 | Redacción del Capítulo de Conclusiones y Trabajo Futuro | Sintetizar los hallazgos principales, discutir la brecha F1 (79% vs. 85% objetivo) como oportunidad de optimización, y proponer líneas de trabajo futuro (fine-tuning, modelos mayores, corpus más amplio). | **27 julio 2026** |
| 5 | Revisión y visado del informe final por profesor guía | Envío del borrador completo al profesor José Luis Martí para revisión académica, correcciones de fondo y aprobación formal. | **29 julio 2026** |
| 6 | Entrega formal del informe final a coordinación MTI | Entrega administrativa del informe final para el inicio del proceso de graduación y constitución de la comisión examinadora. | **31 julio 2026** |
| 7 | Elaboración de presentación oral (slides + demo) | Preparación del set de diapositivas de defensa (~15 láminas) y ensayo de la demostración interactiva en vivo del Dashboard en Streamlit con datos reales del benchmark. | **18 agosto 2026** |
| 8 | Ensayos de defensa oral con feedback | Realización de al menos dos ensayos cronometrados de la presentación, incluyendo simulación de preguntas del comité sobre la brecha de F1, la soberanía de datos y la metodología estadística. | **22 agosto 2026** |
| 9 | **Defensa oral de tesina** | Exposición formal ante la comisión examinadora del programa para la obtención del grado de Magíster en Tecnologías de la Información. | **Fines agosto 2026** |

### c) Fecha estimada de entrega del informe final

**31 de julio de 2026**, para entrega formal y administrativa al programa, con el objetivo de iniciar el proceso de graduación durante agosto de 2026 y completar la defensa oral antes del cierre del semestre académico.

---

*Seminario Integrado de Investigación y Graduación (SIIG) — PGE-25*  
*Universidad Técnica Federico Santa María*
