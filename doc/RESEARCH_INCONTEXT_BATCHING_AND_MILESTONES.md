# ANÁLISIS DE DISEÑO Y REQUERIMIENTOS ACADÉMICOS
## In-Context Batching vs. Procesamiento Individual y Planificación de Tesis (SIIG-PGE25)

**Proyecto**: Sistema de Extracción y Clasificación de Entidades para Cumplimiento Financiero mediante Modelos de Lenguaje Locales (Local LLM Financial Compliance Extraction System)  
**Candidato**: Eduardo Mauricio Ahumada Gallardo  
**Profesor Guía**: Jose Luis Marti Lara  
**Organización**: Leanstack SpA  
**Fecha**: 1 de julio de 2026  

---

## 1. ANÁLISIS DE DISEÑO: PROCESAMIENTO DE DOCUMENTO ÚNICO VS. IN-CONTEXT BATCHING

Durante las fases iniciales del diseño del benchmark se analizó si convenía agrupar múltiples noticias en una sola llamada al LLM (*In-Context Batching*) aprovechando la gran ventana de contexto de los modelos modernos (como Gemma4 y Llama3.1), o procesar cada artículo en una llamada individual independiente. Se optó por el **procesamiento individual**.

A continuación se fundamenta esta decisión técnica y académica para el informe final de tesis:

### 1.1 Comparación de Enfoques

| Dimensión | Un Documento por Llamada (Seleccionado) | Múltiples Documentos por Llamada (*In-Context Batching*) |
| :--- | :--- | :--- |
| **Exactitud Extracción (F1)** | **Alta (70.18%)**: El modelo enfoca toda su atención y parámetros en el contexto de una única noticia. | **Media**: Riesgo alto de omitir entidades de noticias secundarias o de menor tamaño. |
| **Contaminación Cruzada** | **Nula**: No hay posibilidad de que entidades de un caso se mezclen con el de otra noticia. | **Alta**: El modelo tiende a asociar imputados o empresas del Artículo A en hechos del Artículo B. |
| **Estructuración JSON** | **Muy Confiable**: El prompt solicita llaves simples `{"Persons": [], "Organizations": [], "Locations": []}`. | **Frágil**: Requiere esquemas complejos (ej. lista de objetos con ID del artículo), elevando errores de parseo. |
| **Límite de Generación (Salida)**| **Bajo**: La respuesta rara vez excede 512 tokens. No hay truncamiento. | **Alto**: N extracciones pueden superar la ventana de salida física (2048 tokens), rompiendo el JSON. |
| **Métrica por Registro** | **Precisa**: Permite asociar exactamente la latencia y la telemetría (RAM/VRAM) a cada noticia. | **Promediada**: Dificulta el análisis de sensibilidad y la auditoría estadística fina para la tesis. |
| **Roundtrips & Costo de Red** | Alto roundtrip, mayor consumo de tokens de entrada (se repite el prompt del sistema). | **Bajo roundtrip, menor consumo de tokens de entrada** (se envía el prompt del sistema una sola vez). |

### 1.2 Justificación Académica para Cumplimiento Normativo (AML/KYC)
En el dominio de prevención de lavado de activos y cumplimiento financiero, **el falso negativo (no extraer una entidad sancionada) o el falso positivo (asociar erróneamente a un individuo a una sanción de otro) es un riesgo crítico**. 

Dado que el objetivo primario de la tesina es maximizar la fiabilidad del reconocimiento de entidades (NER) y asegurar que el JSON estructurado sea 100% parseable, la optimización de roundtrips que ofrece el *In-Context Batching* no compensa la degradación en exactitud y el aumento del riesgo de alucinación estructurada. Por lo tanto, el uso de multithreading paralelo con el controlador adaptativo de workers (AIMD) es la solución correcta: paraleliza a nivel de infraestructura local pero mantiene aislada y robusta la inferencia del modelo.

---

## 2. REQUERIMIENTOS Y PLANILLA DEL INFORME DE AVANCE (SIIG - PGE25)

El sábado 27 de junio de 2026 se desarrolló la presentación del Informe de Avance Nº2 en el Seminario Integrado de Investigación y Graduación (SIIG), bajo la supervisión de los profesores coordinadores Raúl Monge y Marcello Visconti. 

A continuación se registran los requerimientos y el contenido consolidado en la planilla [**`Formulario-IA-26.docx`**](file:///Users/eahumada1/Downloads/Formulario-IA-26.docx) (también disponible en la versión del repositorio [**`Formulario-IA-26-Rellenado.docx`**](file:///Users/eahumada1/Documents/Personal/MTI/taller_de_titulo/Formulario-IA-26-Rellenado.docx)):

### 2.1 Resumen del Estado de Avance del Proyecto

1. **Hipótesis y Metodología:**
   * *Hipótesis:* Es viable implementar un sistema soberano y local de extracción de entidades financieras para compliance (AML/KYC) utilizando modelos de lenguaje de código abierto de tamaño medio (8B-32B), alcanzando un desempeño competitivo en precisión y recall en idioma español (F1-score >= 70%) mediante técnicas de prompt engineering y few-shot learning, eliminando la fuga de datos a nubes públicas y reduciendo costos operativos.
   * *Metodología:* Construcción de dataset de pruebas a partir de Kleptotrace; pipeline pub/sub concurrente con algoritmo adaptativo de workers (AIMD) para prevención de fallos de VRAM/red; estudio de ablación con 20+ combinaciones de prompts y 16 modelos; y análisis estadístico robusto de variables (ANOVA y Tukey HSD con p-value < 5%).

2. **Resultados Logrados hasta la Fecha:**
   * **Ganancia neta de +18.77% en F1-Score** (de 51.41% en zero-shot inglés a 70.18% en few-shot español) en local usando el modelo Gemma4.
   * **Significancia Estadística:** Confirmada por ANOVA con un F-statistic de 12.84 y p-value = 0.0023, demostrando el impacto científico de la localización del prompt.
   * **Taxonomía de Errores Fina:** Clasificación y medición de *Boundary Errors* y *Type Confusion* para retroalimentar la optimización del modelo.
   * **Mitigación de Alucinaciones:** Reducción exitosa de la tasa de alucinaciones por debajo del 5%.
   * **Concurrencia Adaptativa:** Implementación de control AIMD en caliente para proteger el desbordamiento de memoria de la GPU local y absorber reintentos.
   * **Dashboard y Chat con Datos:** Interfaz Streamlit con pestaña interactiva de chat (Gemini AI) integrada para consultar las métricas del benchmark.

3. **Autoevaluación del Avance del Informe Final:**
   * *Estructura y Organización:* **COMPLETO** (100% definido y mapeado).
   * *Presentación del Problema y Solución:* **COMPLETO** (100% justificado en el informe).
   * *Marco Teórico y Estado del Arte:* **AVANZADO** (Referencias y bibliografía actualizadas).
   * *Desarrollo de la Solución y Validación:* **COMPLETO** (Código del pipeline, dashboard y tests estadísticos terminados).
   * *Análisis de Resultados y Conclusiones:* **AVANZADO** (Estudio de ablación y tablas completadas).

4. **Plan de Trabajo y Graduación:**
   * *Interacción Guía (Mayo-Junio 2026):* Coordinación mensual con el profesor Jose Luis Marti Lara para validar el diseño experimental, la taxonomía de errores y las pautas para la redacción final.
   * *Tareas Pendientes:*
     1. Refinar la redacción escrita del documento de tesis de magíster (Término: 15 de julio de 2026).
     2. Aprobación final por parte del profesor guía (Término: 25 de julio de 2026).
     3. Entrega formal a MTI para iniciar proceso de graduación (Término: 31 de julio de 2026).
     4. Preparación de diapositivas de defensa de tesis (Término: 10 de agosto de 2026).
     5. Ensayo del demo interactivo de Streamlit (Término: 20 de agosto de 2026).
     6. Defensa oral ante comisión evaluadora (Término: Fines de agosto de 2026).
   * *Fecha Estimada de Graduación/Entrega:* **31 de julio de 2026**.
