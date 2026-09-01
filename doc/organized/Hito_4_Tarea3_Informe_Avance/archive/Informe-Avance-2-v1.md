# INFORME DE AVANCE Nº2 DE PROYECTO DE TESINA
**Seminario Integrado de Investigación y Graduación (SIIG) - PGE-25**  
**Fecha de entrega**: 7 de julio 2026  
**Profesor Coordinador**: Raúl Monge Anwandter & Marcello Visconti Zamora  

---

## I. ANTECEDENTES GENERALES

### 1.1 Identificación del proponente y candidato a magíster

| Campo | Información |
| :--- | :--- |
| **Nombre del estudiante** | EDUARDO MAURICIO AHUMADA GALLARDO |
| **RUT** | 12.814.696-2 |
| **E-mail y teléfono de contacto** | Eahumada@gmail.com | +56997828992 |
| **Título del trabajo** | Clasificación y Extracción de Entidades Nombradas (NER) en Noticias de Cumplimiento Normativo en Empresas Mediante RAG y un Modelo de Lenguaje Grande (LLM) usando Ollama |
| **Profesor guía** | JOSÉ LUIS MARTÍ LARA |
| **Organización vinculada** | LEANSTACK SPA / AUSTRANET (Contacto: Manuel Muñoz, Fundador) |
| **Programa** | Magíster en Tecnologías de la Información (MTI) - Año de Ingreso 2013 |

---

## II. RESUMEN DE LA TESINA

**Defina el contexto y el problema, propuesta de solución, objetivos del trabajo, método(s) de validación y resultados esperados (máximo 200 palabras). Finalmente, agregue a lo más 5 palabras claves.**

### Resumen
El presente proyecto de tesina aborda la problemática que enfrentan las instituciones financieras ante la necesidad de automatizar el monitoreo y cumplimiento normativo (KYC, PEP, AML) en grandes volúmenes de noticias no estructuradas. El proceso manual tradicional resulta sumamente ineficiente y costoso, mientras que el uso de APIs en la nube expone datos sensibles y vulnera la confidencialidad. Para solucionar este vacío, se diseñó e implementó un sistema distribuido y soberano de ejecución 100% local. El pipeline emplea una arquitectura de procesamiento pub/sub asíncrona que interactúa localmente con Ollama para realizar el Reconocimiento de Entidades Nombradas (NER). Mediante un estudio de ablación sistemático sobre el dataset de sanciones financieras reales Kleptotrace/CoNLL-2002, la localización al español y la optimización de prompts few-shot elevaron el F1-Score a 70.18% con el modelo Gemma4, con una tasa de alucinaciones inferior al 5% y una reducción de costos de 60-80%, validado mediante pruebas estadísticas de significancia ANOVA y Tukey HSD.

**Palabras Clave:** Cumplimiento Normativo, Procesamiento de Lenguaje Natural (NLP), LLM Local, Reconocimiento de Entidades Nombradas (NER), Soberanía de Datos.

---

## III. PLAN DE INVESTIGACIÓN

**Actualice la hipótesis de trabajo y la metodología de validación aplicada, como también los resultados logrados, resaltando los hallazgos más relevantes de su trabajo de investigación.**

### a) Hipótesis definida y metodología de validación aplicada (20 líneas)
La hipótesis planteada sostiene que es viable implementar un sistema de extracción y clasificación de entidades financieras para cumplimiento corporativo (AML/KYC) utilizando modelos de lenguaje de código abierto de tamaño medio (8B-32B) ejecutados localmente de forma soberana, alcanzando un desempeño competitivo en precisión y recall en idioma español (F1-score >= 70%) a través de técnicas sistemáticas de prompt engineering y few-shot learning, eliminando la fuga de datos confidenciales y reduciendo los costos operativos en más de un 60%.

La metodología de validación aplicada comprende:
1. Ingestión y estructuración de noticias reales de lavado de activos y sanciones internacionales provenientes de la plataforma Kleptotrace/CoNLL-2002.
2. Definición de un pipeline pub/sub multithreading con control adaptativo de concurrencia AIMD (TCP-like congestion control) para regular los hilos de procesamiento en caliente, protegiendo la GPU local ante desbordes de VRAM y absorbiendo errores de red (HTTP 429) en endpoints externos.
3. Ejecución de un análisis de sensibilidad y estudio de ablación sobre 20+ combinaciones de prompts en 16 modelos locales e híbridos (Factory/Facade).
4. Validación estadística rigurosa contrastando hipótesis nulas de rendimiento mediante ANOVA de una vía y pruebas post-hoc de Tukey HSD con una confianza del 95% (alfa=0.05).

### b) Destaque principales resultados y hallazgos de su trabajo hasta la fecha (20 líneas)
Los principales resultados y hallazgos alcanzados a la fecha son:
1. **Ganancia de Rendimiento por Prompting y Localización:** Se constató un F1-score inicial de 51.41% en zero-shot inglés. La localización cultural y lingüística al español elevó la métrica a 57.43% (+6.02%). La inyección de ejemplos contextuales few-shot del dominio financiero de sanciones culminó en un F1-score final de 70.18% con Gemma4 local, logrando una mejora total de +18.77% y validando la viabilidad de modelos locales de menor tamaño.
2. **Significancia Estadística:** El ANOVA sobre la varianza de los prompts arrojó un F-statistic de 12.84 y un p-value de 0.0023, rechazando la hipótesis nula con alta significancia científica y demostrando que la ganancia no es producto del azar.
3. **Mitigación de Alucinaciones:** La tasa de alucinación estructurada se redujo a menos de un 5% mediante prompts con delimitadores estrictos de JSON y formateadores semánticos en el runner.
4. **Robustez de la Infraestructura Concurrente:** El controlador adaptativo AIMD estabilizó la concurrencia en 4 workers sin interrupciones por desbordamientos de memoria local (VRAM) en macOS (Apple Silicon M4) y reguló eficazmente las fallas por rate-limiting de la API de Google AI Studio (Gemini 2.0 Flash-Lite).
5. **Implementación del Dashboard y Chat con Datos:** Se completó la interfaz visual en Streamlit para stakeholders de cumplimiento, incorporando gráficos interactivos de métricas, análisis ANOVA en vivo y un panel de chat interactivo que aprovecha el SDK de Gemini para consultar e interrogar las métricas acumuladas del benchmark.

---

## IV. ESTADO DE AVANCE DEL INFORME FINAL

**Evalúe el estado de avance el informe final (lo que tiene realmente escrito en un documento).**

| Componente del Informe | Nulo | Bajo | Medio | Avanzado | Completo |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Definición de la estructura y organización de contenidos | | | | | **X** |
| Presentación del problema y la solución | | | | | **X** |
| Marco teórico y estado del arte (con bibliografía actualizada) | | | | **X** | |
| Desarrollo de la solución y trabajo de validación | | | | | **X** |
| Análisis de resultados y conclusiones | | | | **X** | |

---

## V. PLAN TRABAJO

**Resuma las tareas principales que le quedan pendientes, fechas estimadas de término, como también la interacción que ha tenido con su profesor guía.**

### a) Interacción con el profesor guía (15 líneas)
Durante los meses de mayo y junio de 2026, la interacción periódica con el profesor guía José Luis Martí Lara se centró en:
1. Sesiones de coordinación mensual para revisar el progreso del desarrollo de software y validar la metodología experimental.
2. Revisión y validación del diseño de pruebas estadísticas (ANOVA/Tukey HSD) sobre el dataset balanceado Kleptotrace/CoNLL-2002/CoNLL-2002.
3. Definición de la taxonomía de errores del NER (Boundary Errors y Type Confusion) y de las estrategias de mitigación de alucinaciones en el runner.
4. Revisión y visado del plan de trabajo de cara a la redacción y entrega final de la tesina para optar al grado de Magíster en Tecnologías de la Información (MTI).

### b) Tareas pendientes y fechas tentativas (30 líneas)
El plan de trabajo restante contempla las siguientes actividades finales conducentes al examen de grado:
1. **Fase 1: Refinamiento del informe final de tesina** (Término: 15 de julio de 2026). Incorporación en el marco de la tesina de la discusión metodológica sobre el procesamiento de documento único vs. In-Context Batching y el análisis de rendimiento de GLiNER.
2. **Fase 2: Entrega y aprobación final de la tesina escrita** (Término: 25 de julio de 2026). Entrega del borrador completo de la tesina para revisión y visado del profesor guía.
3. **Fase 3: Entrega del informe final a coordinación MTI** (Término: 31 de julio de 2026). Entrega formal y administrativa para el inicio del proceso de graduación y constitución de la comisión.
4. **Fase 4: Preparación de la presentación y demo oral** (Término: 20 de agosto de 2026). Elaboración del set de diapositivas (5 láminas principales) y ensayos de la demostración interactiva en vivo del Dashboard en Streamlit.
5. **Fase 5: Defensa oral de tesis** (Término: Fines de agosto de 2026). Exposición oral del proyecto de tesina ante la comisión examinadora del programa para la obtención del grado de Magíster.

### c) Fecha estimada de entrega del informe final
**31 de julio de 2026** (para iniciar proceso de graduación en agosto de 2026).
