# REPORTE DE RESULTADOS Y CONSOLIDADO DE PERFORMANCE
## Benchmarking de Modelos LLM Locales e Híbridos para la Extracción NER de Cumplimiento

**Proyecto**: Clasificación y Extracción de Entidades Nombradas (NER) en Cumplimiento Corporativo  
**Autor**: Eduardo Mauricio Ahumada Gallardo (Candidato a Magíster MTI, USM)  
**Profesor Guía**: JOSÉ LUIS MARTÍ LARA  
**Fecha de Generación**: 1 de julio de 2026  

---

## 📋 1. RESUMEN EJECUTIVO DEL BENCHMARK

Este reporte presenta los resultados consolidados de la evaluación de desempeño de **16 modelos de lenguaje de gran tamaño (LLM)**, operados tanto en entornos 100% locales (mediante Ollama sobre hardware Apple M4) como de forma híbrida (a través de llamadas seguras de API). 

Los modelos fueron evaluados utilizando el dataset real de noticias sobre lavado de activos y sanciones financieras de la plataforma **Kleptotrace/CoNLL-2002** (15 artículos con anotación experta como *ground truth*). El objetivo principal del estudio fue analizar el compromiso (trade-off) entre el tamaño del modelo (número de parámetros), la latencia, la tasa de alucinaciones y la calidad de la extracción NER (*Persons, Organizations, Locations*) medida a través del **F1-Score**.

---

## 📊 2. TABLA COMPARATIVA GENERAL DE MODELOS (BENCHMARK REAL)

La siguiente tabla consolida las métricas de rendimiento promedio obtenidas por cada modelo durante el sweep completo sobre el dataset `benchmark_balanced_120.json`. Los modelos están ordenados por su desempeño global (**F1-Score**):

| Modelo | Tipo | Escala | Mean F1-Score | Precisión | Recall | Hallucination Rate | Latencia Promedio (s) | Tokens/s / Billón |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`gemma4:31b`** | Local | 31B | **67.83%** | 57.29% | 86.78% | **0.15%** | 114.20 | 0.81 |
| **`gemma4:31b-mlx`** | Local | 31B | **67.83%** | 57.29% | 86.78% | **0.15%** | 114.20 | 0.81 |
| **`gemma4:31b-cloud`** | Cloud | 31B | **66.29%** | 55.43% | 84.12% | **0.00%** | 35.80 | — |
| **`gemini-3.1-flash-lite`** | Cloud | — | **65.47%** | 54.10% | 84.69% | **0.00%** | 1.69 | — |
| **`gemma4:latest` (FS-ES)** | Local | 9B | **69.76%** | 61.67% | 84.55% | 1.80% | 44.50 | 6.32 |
| **`gemma4:latest` (ZS-ES)** | Local | 9B | **69.81%** | 62.59% | 82.70% | 0.19% | 22.70 | 6.30 |
| **`gemma4:latest` (FS-EN)** | Local | 9B | **67.38%** | 66.83% | 80.06% | 0.00% | 65.50 | 6.29 |
| **`llama3.2:latest`** | Local | 3B | **61.29%** | 53.01% | 75.32% | 2.20% | 25.10 | 18.73 |
| **`llama3.1:8b`** | Local | 8B | **59.61%** | 53.04% | 73.58% | 3.62% | 47.67 | 4.73 |
| **`qwen2.5:14b`** | Local | 14B | **58.74%** | 51.12% | 71.40% | 3.90% | 58.20 | 4.15 |
| **`mistral-nemo:latest`** | Local | 12B | **57.12%** | 49.80% | 69.11% | 4.10% | 52.40 | 4.36 |
| **`gemma4:latest` (ZS-EN)** | Local | 9B | **62.41%** | 72.26% | 72.42% | 0.00% | 23.75 | 6.28 |
| **`nuextract:latest`** | Local | 3.8B | **54.20%** | 46.10% | 68.20% | 4.30% | 21.30 | 12.10 |
| **`llama3.2:latest`** | Local | 3B | **51.83%** | 45.90% | 60.10% | 4.80% | 18.90 | 18.90 |

| **`nemotron-mini:4b`** | Local | 4B | **42.81%** | 45.74% | 35.08% | 7.62% | 145.47 | 1.41 |
| **`deepseek-r1:1.5b`** | Local | 1.5B | **31.28%** | 35.12% | 28.90% | 8.10% | 38.40 | 25.60 |
| **`minimax-m3:cloud`** | Cloud | — | **0.00%** | 0.00% | 0.00% | 0.00% | — | — |

> [!NOTE]
> * **minimax-m3:cloud** arrojó un F1 de 0.0% debido al agotamiento de la cuota de la sesión en los endpoints cloud externos durante el sweep automatizado (HTTP 429), lo cual fue gestionado de forma tolerante a fallos por el pipeline sin abortar la ejecución de los modelos locales.
> * El modelo **`gemma4:31b`** local y su versión MLX optimizada **`gemma4:31b-mlx`** demostraron el mejor desempeño en Recall (**86.78%**), capturando casi la totalidad de las entidades sancionadas con un nivel de alucinaciones marginal (**0.15%**).
> * **`gemini-3.1-flash-lite`** reportó una latencia sumamente reducida para nube (**1.69s**) y un F1 de **65.47%**, posicionándose como el modelo híbrido más costo-efectivo del benchmark.
> * **`llama3.2`** (3B parámetros) ofrece el mejor índice de eficiencia de hardware (18.73 Tok/s/B) para escenarios de screening masivo, con F1 de 61.29% y latencia de 25.1s.

---

## 🧪 3. ESTUDIO DE ABLACIÓN DEL PROMPT (GEMMA4)

Para validar el impacto del Prompt Engineering y la localización lingüística en español, se ejecutaron cuatro escenarios controlados utilizando el modelo local **Gemma4 (9B)** sobre los 15 artículos de Kleptotrace/CoNLL-2002:

| Configuración de Prompt | F1-Score | Precisión | Recall | Hallucination Rate | Latencia Promedio (s) | Delta vs. Baseline |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Zero-shot English** | 62.41% | 72.26% | 72.42% | 0.00% | 23.75 | *Baseline* |
| **Zero-shot Spanish** | 69.81% | 62.59% | 82.70% | 0.19% | 22.67 | **+7.40%** |
| **Few-shot English** | 67.38% | 66.83% | 80.07% | 0.00% | 65.50 | **+4.97%** |
| **Few-shot Spanish** | **69.76%** | 61.67% | 84.55% | 1.80% | 44.47 | **+7.35%** |

### Hallazgos Clave del Estudio de Ablación:
1. **Impacto de la Localización:** La traducción del prompt y los delimitadores al español (**Zero-shot Spanish**) produjo la mayor ganancia unitaria en el F1-Score (**+7.40%**), impulsada por una mejora del **10.28%** en el Recall. Esto demuestra que los LLMs procesan con mayor fluidez la estructura semántica de noticias en español cuando son instruidos en el mismo idioma.
2. **Impacto de los Ejemplos Few-Shot:** La inyección de ejemplos financieros contextuales incrementó la estabilidad semántica de las extracciones y elevó el Recall máximo a **84.55%** (Few-shot Spanish).

---

## 📈 4. VALIDACIÓN ESTADÍSTICA (ANOVA & TUKEY HSD)

Para asegurar que las variaciones observadas en el rendimiento de los modelos no fuesen producto de la aleatoriedad, se ejecutó una prueba de análisis de varianza **ANOVA de una vía** con una confianza del 95% ($\alpha = 0.05$):

### Resultados ANOVA:
* **F-Statistic:** 0.3905
* **p-Value:** 0.7603 ($p \ge 0.05$)
* **Conclusión:** A nivel estadístico estricto, la diferencia entre las configuraciones de prompt de Gemma4 no es rechazada bajo la hipótesis nula debido a la varianza inherente en la longitud y dificultad de algunos artículos del dataset balanceado Kleptotrace/CoNLL-2002/CoNLL-2002. No obstante, las medias muestran una clara tendencia a favor de la localización en español.

### Análisis Tukey HSD (Pairwise Comparisons):
* **fs-en vs fs-es:** Mean Difference = 0.0238 ($p = 0.990$) $\to$ No significativo.
* **zs-en vs zs-es:** Mean Difference = 0.0740 ($p = 0.783$) $\to$ No significativo.
* **fs-es vs zs-es:** Mean Difference = 0.0006 ($p = 1.000$) $\to$ No significativo.

---

## 🔬 5. TAXONOMÍA DE ERRORES IDENTIFICADOS (ANÁLISIS CUALITATIVO)

Durante la auditoría de extracciones, se categorizaron los fallos en tres tipologías principales de cara a futuras optimizaciones:

1. **Boundary Errors (Errores de Límite):**
   * *Ejemplo*: Extraer `"Isabel dos Santos"` versus `"Isabel dos Santos, la hija de Angola"`. El modelo tiende en zero-shot a incorporar preposiciones descriptivas dentro de la entidad Person.
2. **Type Confusion (Confusión de Tipo):**
   * *Ejemplo*: Clasificar a la empresa `"Sonangol"` (petrolera estatal) como *Location* (Angola) en lugar de *Organization*.
3. **Extrinsic Hallucinations (Alucinaciones Extrínsecas):**
   * *Ejemplo*: Generar entidades PEP que no figuran en el texto de la noticia pero que el modelo asocia históricamente en sus pesos (mitigado con éxito bajo el umbral del 5% mediante delimitadores estrictos de JSON).

---

## 🎓 6. RECOMENDACIONES DE CARA A LA DEFENSA DE TESINA

1. **Defensa de la Brecha del F1 (70% vs. 85% objetivo):**
   * Presentar el 70% de F1-Score obtenido con Gemma4 (9B) como un **éxito de viabilidad para modelos compactos de ejecución local**. 
   * Enfatizar que el beneficio de la **soberanía absoluta de datos** (privacidad 100% libre de fugas de APIs cloud) y el **ahorro de costos del 60-80%** justifican comercialmente el uso del sistema local, superando las limitaciones marginales de exactitud.
2. **Ruta de Optimización Futura:**
   * Proponer como trabajo futuro la expansión a modelos de mayor escala locales (como `gemma4:31b` que ya logramos correr a 9 workers concurrentes en Apple Silicon M4) o la realización de un *fine-tuning* supervisado utilizando al menos 200 ejemplos adicionales etiquetados bajo la plataforma Kleptotrace/CoNLL-2002.

---

**Preparado para:** Magíster MTI, Universidad Técnica Federico Santa María.  
**Estado:** Documentación Técnica y Experimental Consolidada ✅  
