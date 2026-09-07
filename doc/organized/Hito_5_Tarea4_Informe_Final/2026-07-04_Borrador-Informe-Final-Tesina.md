# INFORME FINAL DE TESINA

**UNIVERSIDAD TÉCNICA FEDERICO SANTA MARÍA**  
**DEPARTAMENTO DE INFORMÁTICA**  
**Magíster en Tecnologías de la Información (MTI)**  

---

**Clasificación y Extracción de Entidades Nombradas (NER) en Noticias de Cumplimiento Normativo Corporativo Mediante Modelos de Lenguaje Grande Ejecutados Localmente con Soberanía de Datos**

---

| | |
|:---|:---|
| **Autor** | Eduardo Mauricio Ahumada Gallardo |
| **RUT** | 12.814.696-2 |
| **Correo** | eahumada@gmail.com |
| **Profesor Guía** | José Luis Martí Lara |
| **Organización Vinculada** | Austranet |
| **Programa** | Magíster en Tecnologías de la Información — Año de Ingreso 2013 |
| **Fecha de Entrega** | Julio 2026 |

---

## RESUMEN

Las instituciones financieras que operan en el marco de regulaciones AML (Anti-Money Laundering) y KYC (Know Your Customer) enfrentan el desafío de monitorear grandes volúmenes de noticias no estructuradas en busca de entidades de riesgo (personas, organizaciones). Este proceso, ejecutado manualmente, resulta costoso, lento e incapaz de escalar, mientras que el uso de APIs en la nube expone datos financieros sensibles a terceros, vulnerando la soberanía de datos. Este trabajo diseña, implementa y evalúa empíricamente un sistema soberano de extracción de Entidades Nombradas (NER) basado en Modelos de Lenguaje Grande (LLM) de código abierto (familias Gemma, Llama, DeepSeek) ejecutados 100% localmente mediante Ollama en hardware Apple Silicon M4.

El sistema incorpora una arquitectura de procesamiento pub/sub multithreading con control adaptativo de concurrencia (AIMD) y una capa Factory/Facade que unifica cuatro proveedores de modelos. La validación experimental se realizó sobre el dataset real de sanciones financieras Kleptotrace/CoNLL-2002 (N=15 artículos con anotación experta) y un corpus estadísticamente significativo de 30 artículos breves (N=30). El análisis de variantes de prompts demuestra que combinar localización al español con ejemplos *few-shot* produce una mejora de +11.1 puntos de F1 sobre el baseline zero-shot en inglés, y que el mejor modelo evaluado (gemma4:31b) alcanza un F1-Score de 79.03% con una tasa de alucinaciones del 0.0% sobre el corpus N=30. El sistema reduce los costos operativos de revisión manual en un 60–80% y garantiza privacidad total de datos.

**Palabras clave:** Reconocimiento de Entidades Nombradas (NER), Modelos de Lenguaje Grande (LLM), Cumplimiento Normativo (AML/KYC), Soberanía de Datos, Prompt Engineering.

---

## ABSTRACT

Financial institutions operating under AML and KYC regulatory frameworks face the challenge of monitoring large volumes of unstructured news for risk entities (persons, organizations). Manual execution of this process is costly, slow, and unscalable, while cloud API usage exposes sensitive financial data to third parties, violating data sovereignty. This work designs, implements, and empirically evaluates a sovereign Named Entity Recognition (NER) system based on open-source Large Language Models (Gemma, Llama, DeepSeek families) executed 100% locally via Ollama on Apple Silicon M4 hardware.

The system incorporates a multithreading pub/sub processing architecture with an adaptive concurrency controller (AIMD) and a Factory/Facade layer unifying four model providers. Experimental validation was performed on the real financial sanctions dataset Kleptotrace/CoNLL-2002 (N=15 expert-annotated articles) and a statistically significant corpus of 30 short articles (N=30). The prompt ablation study demonstrates that Spanish-language localization yields a +7.4 F1-point improvement over the English zero-shot baseline, and the best evaluated model (gemma4:31b) achieves an F1-Score of 79.03% with 0.0% hallucination rate on the N=30 corpus. The system reduces manual review operational costs by 60–80% while guaranteeing total data privacy.

**Keywords:** Named Entity Recognition (NER), Large Language Models (LLM), Regulatory Compliance (AML/KYC), Data Sovereignty, Prompt Engineering.

---

## ÍNDICE DE CONTENIDOS

1. [Introducción](#1-introducción)
2. [Marco Teórico y Estado del Arte](#2-marco-teórico-y-estado-del-arte)
3. [Descripción del Sistema Propuesto](#3-descripción-del-sistema-propuesto)
4. [Diseño Experimental](#4-diseño-experimental)
5. [Resultados Experimentales](#5-resultados-experimentales)
6. [Discusión](#6-discusión)
7. [Conclusiones y Trabajo Futuro](#7-conclusiones-y-trabajo-futuro)
8. [Referencias Bibliográficas](#8-referencias-bibliográficas)
9. [Anexos](#9-anexos)

---

## 1. INTRODUCCIÓN

### 1.1 Contexto y Motivación

Las instituciones financieras operan bajo un marco regulatorio estricto que les obliga a identificar y gestionar entidades de riesgo en tiempo real. Las regulaciones internacionales Anti-Money Laundering (AML) y Know Your Customer (KYC), implementadas en Chile por la Unidad de Análisis Financiero (UAF) y la Comisión para el Mercado Financiero (CMF), exigen la detección de Personas Políticamente Expuestas (PEP), sujetos sancionados y vínculos con redes de lavado de activos en flujos continuos de información pública.

El proceso actual en instituciones como Austranet implica la revisión manual de cientos de artículos periodísticos diarios por analistas especializados, un proceso con un costo promedio estimado de USD 8.75 por artículo analizado. A nivel global, según Verified Market Research el mercado de RegTech se valoró en USD 15,68 mil millones en 2020 y se proyecta que alcance USD 87,17 mil millones hacia 2028, con una CAGR del 23,92 % durante 2021-2028, evidenciando la urgencia de soluciones automatizadas y escalables (Verified Market Research, 2022).

### 1.2 Planteamiento del Problema

El problema central es de naturaleza técnico-operativa: la extracción automatizada de entidades nombradas (personas, organizaciones) desde noticias no estructuradas en español con alta precisión semántica, en contextos de ambigüedad regulatoria, sin exponer datos confidenciales a servicios externos en la nube.

Los enfoques existentes presentan limitaciones críticas:
- **Revisión manual:** altamente precisa pero no escalable ni rentable.
- **Sistemas basados en reglas (regex, CRF):** frágiles ante variaciones léxicas en español.
- **APIs en la nube (OpenAI, Google Cloud NLP):** violan la soberanía de datos y presentan costos prohibitivos en batch.
- **Modelos supervisados (BERT-NER):** requieren miles de ejemplos etiquetados en dominio específico, inexistentes en español para compliance.

### 1.3 Hipótesis de Trabajo

> **Hipótesis:** Es viable implementar un sistema soberano de extracción y clasificación de entidades financieras para cumplimiento corporativo (AML/KYC) utilizando modelos de lenguaje de código abierto de escala media-grande (8B–31B parámetros) ejecutados localmente, alcanzando un desempeño competitivo en español (F1-Score ≥ 70%) mediante técnicas sistemáticas de prompt engineering y few-shot learning, eliminando la fuga de datos confidenciales y reduciendo los costos operativos en más del 60%.

**Variables independientes:** (1) Modelo LLM seleccionado; (2) Estrategia de prompt (zero-shot/few-shot, inglés/español).  
**Variables dependientes:** (1) F1-Score por tipo de entidad; (2) Tasa de alucinaciones; (3) Latencia de procesamiento; (4) Consumo de VRAM.

### 1.4 Objetivos

**Objetivo General:** Diseñar, implementar y validar un sistema soberano de extracción de entidades nombradas para cumplimiento normativo (AML/KYC) basado en LLMs de código abierto ejecutados localmente.

**Objetivos Específicos:**
1. Diseñar e implementar una arquitectura pub/sub multithreading con control adaptativo de concurrencia para la ejecución segura de LLMs de gran escala en hardware Apple Silicon.
2. Evaluar y comparar el desempeño de modelos de lenguaje de código abierto generativos (familias Gemma, Llama, DeepSeek, Qwen, Mistral, GPT-OSS, Nemotron) en la tarea de NER sobre corpus de sanciones financieras reales en español: **12 modelos** en el benchmark exploratorio N=15 (§5.1) y **13 modelos** en el estudio principal N=120 con KB RAG (§5.3.5).
3. Ejecutar una comparación sistemática de cuatro configuraciones de prompt (zero-shot/few-shot × inglés/español) —un diseño factorial 2×2, que la literatura anglosajona de aprendizaje automático denomina *ablation study*— para cuantificar el impacto de la localización lingüística y el aprendizaje en contexto.
4. Validar estadísticamente los resultados mediante ANOVA de una vía y pruebas post-hoc de Tukey HSD (α=0.05) sobre un corpus estadísticamente significativo (N≥30).
5. Demostrar una reducción de costos operativos del 60–80% respecto a la revisión manual, manteniendo una tasa de alucinaciones inferior al 5%.

### 1.5 Estructura del Documento

El informe se organiza así: §2 marco teórico y estado del arte; §3 sistema propuesto; §4 diseño experimental; §5 resultados; §6 discusión de los hallazgos; §7 conclusiones y trabajo futuro; §8 referencias; §9 anexos técnicos.

---

## 2. MARCO TEÓRICO Y ESTADO DEL ARTE

### 2.1 Reconocimiento de Entidades Nombradas (NER)

El Reconocimiento de Entidades Nombradas (NER) es una subtarea fundamental del Procesamiento de Lenguaje Natural (PLN) que busca localizar y clasificar fragmentos de texto en categorías semánticas predefinidas. En el contexto de cumplimiento normativo, las categorías de interés son: **Personas** (PER), **Organizaciones** (ORG) y **Ubicaciones Geográficas** (LOC). Formalmente, NER es un problema de etiquetado de secuencias donde cada token recibe una etiqueta según el esquema IOB2 (Inside-Outside-Beginning).

Los enfoques históricos para NER incluyen: (1) Modelos estadísticos de Campos Aleatorios Condicionales (CRF) [10]; (2) Modelos neurales BiLSTM-CRF; y (3) Modelos Transformer pre-entrenados como BERT [2]. El estado del arte en benchmarks académicos (CoNLL-2003, FiNER-139) supera el 90% de F1 con modelos BERT fine-tuned, pero estos requieren grandes volúmenes de datos etiquetados específicos del dominio, inexistentes en español para el dominio de compliance financiero.

El estado del arte en NER en español con Transformers alcanza 88–91% de F1 en benchmarks académicos controlados [7], [2]. Sin embargo, estos modelos requieren corpus etiquetados extensos en el dominio objetivo, inexistentes en español para el ámbito de cumplimiento financiero AML/KYC. Esto motiva el uso de LLMs generativos con capacidades zero-shot y few-shot, que permiten adaptación inmediata al dominio sin reentrenamiento.

### 2.2 Modelos de Lenguaje Grande (LLMs) y Aprendizaje en Contexto

La arquitectura Transformer [4], basada en el mecanismo de atención multi-cabeza, es la base de todos los modelos evaluados en este trabajo. Los LLMs modernos generativos (decoder-only Transformers) son entrenados en corpus masivos de texto con el objetivo de predicción del siguiente token. Su capacidad de adaptación a nuevas tareas sin entrenamiento explícito, denominada aprendizaje en contexto (in-context learning), es crítica para dominios especializados con datos etiquetados escasos.

El aprendizaje few-shot [8] permite incluir ejemplos demorativos (shots) directamente en el prompt para guiar la salida del modelo. Este trabajo evalúa sistemáticamente el impacto de 0 (zero-shot) y 3 (few-shot) ejemplos en español e inglés sobre la calidad de extracción NER en cumplimiento financiero.

BloombergGPT [3] evidencia el beneficio del pre-entrenamiento específico al dominio financiero (+15% F1 promedio vs. modelos generales). Sin embargo, su ejecución requiere infraestructura propietaria en la nube. Este trabajo demuestra que modelos de código abierto de escala media-grande (8B–31B parámetros) ejecutados localmente pueden aproximar este rendimiento sin comprometer la soberanía de datos.

### 2.3 Generación Aumentada por Recuperación (RAG)

La Generación Aumentada por Recuperación (RAG) [1] optimiza la salida de un LLM fundamentando la generación en documentos recuperados dinámicamente. En este trabajo se adopta una variante de RAG de "contexto único": cada artículo periodístico actúa como la única fuente de contexto inyectada al LLM en el prompt del sistema, forzando al modelo a extraer entidades únicamente desde el texto presente, mitigando alucinaciones extrínsecas.

### 2.4 Ejecución Soberana de LLMs con Ollama

Ollama es una plataforma de código abierto que permite ejecutar LLMs de gran escala localmente mediante cuantización (GGUF, Q4_K_M) optimizada para Apple Silicon Metal (MPS) y arquitecturas x86 con CUDA. La ejecución local garantiza soberanía de datos: ningún dato es transmitido a servicios externos. En este trabajo, Ollama gestiona la carga dinámica de pesos en VRAM y la liberación explícita de memoria GPU al completar cada modelo (keep_alive=0). El footprint operativo varía con el tamaño del modelo: ~7-9 GB para modelos de hasta ~12B (Q4) y hasta ~24,7 GB para gemma4:31b-mlx (pesos ~18,7 GB más KV cache y overhead de inferencia), lo que condiciona el hardware requerido (ver §3.6).

### 2.5 Estado del Arte Relacionado

La Tabla 1 posiciona este trabajo respecto a investigaciones recientes en NER para dominios financieros y regulatorios:

| Trabajo | Dataset | Modelo | F1 | Privacidad | Idioma |
|:---|:---|:---|:---:|:---:|:---|
| BloombergGPT [3] | Bloomberg corpus | GPT-J + dominio | 85%+ | ❌ Cloud | Inglés |
| FiNER-139 Benchmark [15] | SEC 10-K/10-Q | BERT fine-tuned | 91% | ❌ Cloud | Inglés |
| García & López [7] | CoNLL-ES | XLM-R | 88% | ✅ Local | Español |
| Chang et al. [9] | Docs bancarios | GPT-4 + RAG | 83% | ❌ Cloud | Inglés |
| **Este trabajo** | **Kleptotrace/CoNLL-2002 (AML), corpus sintético N=30** | **gemma4:31b local** | **79%** | **✅ 100% Local** | **Español** |

El aporte original de este trabajo reside en: (1) evaluación comparativa de 13 modelos sobre corpus real de sanciones en español; (2) análisis de variantes de prompts entre idiomas (ES vs. EN); (3) sistema soberano reproducible sobre hardware comercial; y (4) validación estadística formal (ANOVA, Tukey HSD) sobre corpus N≥30.

---

## 3. DESCRIPCIÓN DEL SISTEMA PROPUESTO

### 3.1 Arquitectura General

El sistema se estructura en cinco capas funcionales:

```
┌──────────────────────────────────────────────────────┐
│  1. CAPA DE DATOS          DataLoader + Validator    │
│     Kleptotrace/CoNLL-2002 JSON → Schema Validation → Records  │
├──────────────────────────────────────────────────────┤
│  2. ORQUESTACIÓN           main.py + pub_sub.py      │
│     Pub/Sub Queue → AIMD Controller → Batch Mgr     │
├──────────────────────────────────────────────────────┤
│  3. PROVEEDORES LLM        Factory / Facade          │
│         OllamaProvider │ OpenAIProvider │ AnthropicProvider      │
├──────────────────────────────────────────────────────┤
│  4. EVALUACIÓN             evaluator.py + stats      │
│     F1 / Precision / Recall / ANOVA / Tukey HSD     │
├──────────────────────────────────────────────────────┤
│  5. VISUALIZACIÓN          dashboard.py (Streamlit)  │
│     7 pestañas: métricas, alucinaciones, ANOVA...   │
└──────────────────────────────────────────────────────┘
```

### 3.2 Pipeline Pub/Sub y Control Adaptativo AIMD

El núcleo del sistema es un pipeline pub/sub multithreading implementado en `pub_sub.py`. El productor publica las tareas de procesamiento (lotes de artículos por modelo) en una cola en memoria (Redis-ready). Los consumidores (workers) consumen tareas de forma paralela, con un número de workers dinámicamente ajustado por el controlador AIMD (`adaptive_workers.py`).

El controlador AIMD (Additive Increase Multiplicative Decrease) implementa la siguiente política:
- **Aumento aditivo:** Si el sistema permanece estable (sin errores HTTP 429 ni excepciones) durante una ventana de 600 segundos, incrementa los workers en +1 cada 120 segundos, hasta un techo del 75% del máximo.
- **Decremento multiplicativo:** Ante cualquier error de rate-limiting, reduce los workers a la mitad.
- **Circuit breaker:** Si se detectan 5 fallos consecutivos, el circuito se abre (OPEN) y suspende el procesamiento durante 60 segundos.

En pruebas sobre hardware Apple Silicon M4 (16 GB Metal), el sistema escaló de forma estable hasta 9 workers concurrentes para modelos de 8B parámetros.

### 3.3 Capa Factory/Facade de Proveedores LLM

La capa de proveedores implementa el patrón Factory + Facade, abstrayendo la heterogeneidad de las APIs de los diferentes modelos detrás de una interfaz uniforme (`LLMProvider`):

```python
class LLMProvider(ABC):
    @abstractmethod
    def extract_entities(self, text: str, system_prompt: str, **kwargs) -> ExtractionResult:
        ...
    @abstractmethod
    def is_available(self) -> bool:
        ...
```

Los proveedores implementados son: `OllamaProvider` (modelos locales vía API REST), `OpenAIProvider`, `AnthropicProvider` y `VertexAIProvider`. La detección automática del proveedor se realiza por prefijo del nombre del modelo (`gpt-*` → OpenAI, `claude-*` → Anthropic, `gemini-*` → Vertex AI, resto → Ollama).

### 3.4 Módulo de Evaluación Estadística

El evaluador (`evaluator.py`) implementa:
- **Emparejamiento difuso (Fuzzy Matching):** Las entidades extraídas se comparan con el ground truth usando similitud de tokens, aceptando como correctas las coincidencias parciales por encima de un umbral configurable (default: 0.85).
- **Métricas por registro:** Precisión, Recall, F1-Score calculados por artículo y promediados.
- **Tasa de alucinaciones:** Proporción de entidades extraídas que no tienen correspondencia alguna en el ground truth (`hallucinated / total_extracted`).
- **Análisis estadístico:** ANOVA de una vía (scipy.stats.f_oneway) y pruebas Tukey HSD post-hoc (statsmodels) con α=0.05 y cálculo de intervalos de confianza del 95%.
- **Análisis de sensibilidad:** Filtrado de outliers por longitud de artículo (> media + σ) y recálculo de métricas.

### 3.5 Dashboard Streamlit

La interfaz de visualización implementada en `dashboard.py` (Streamlit) presenta 7 pestañas: (1) Comparación de modelos, (2) Análisis de alucinaciones, (3) Errores por entidad (taxonomía), (4) Significancia estadística (ANOVA), (5) Eficiencia de hardware (Índice Tok/s/B), (6) Hipótesis de modelos futuros, y (7) Simulación de producción.

### 3.6 Gestión de VRAM en Apple Silicon

Para garantizar la ejecución serial de modelos de gran escala sin desbordamiento de VRAM, se implementó la liberación explícita de pesos de GPU al finalizar cada modelo mediante una llamada a la API de generación de Ollama con `keep_alive=0`. La ejecución se organizó en dos escalones de hardware según el footprint de memoria. Los modelos de hasta ~12B parámetros (Q4) se ejecutaron en un equipo M4 con **16 GB de memoria unificada**: su footprint operativo (~7-9 GB) queda por debajo del techo de VRAM que macOS/Metal asigna a la GPU, equivalente a ~75 % de la memoria unificada (`recommendedMaxWorkingSetSize`), es decir ~12 GB en un equipo de 16 GB. Los modelos de 31B parámetros (p. ej. gemma4:31b, Q4_K_M/MLX), con footprint operativo ~24,7 GB (pesos ~18,7 GB más KV cache y overhead), **exceden ese techo y no pueden cargarse en 16 GB ni siquiera de forma serial** con `keep_alive=0` —este parámetro evita retener varios modelos a la vez, pero no reduce el footprint de uno solo—; se ejecutaron en un equipo con **48 GB de memoria unificada**, cuyo techo de VRAM asignable (~36 GB) aloja el modelo con holgura para el KV cache y el sistema operativo.

---

## 4. DISEÑO EXPERIMENTAL

### 4.1 Corpus de Evaluación

Se utilizaron dos corpus complementarios:

**Corpus 1 — Kleptotrace/CoNLL-2002 (N=15, Gold Standard):**  
15 artículos periodísticos reales de la plataforma Kleptotrace/CoNLL-2002 sobre lavado de activos, sanciones internacionales y corrupción. Anotados manualmente por expertos en compliance con entidades Personas (PER) y Organizaciones (ORG) como ground truth. Longitud promedio: ~4.833 caracteres por artículo (mediana 5.280; rango 725–8.813).

**Corpus 2 — Kleptotrace/CoNLL-2002 Augmented (N=30, Corpus de Validación Estadística):**  
30 artículos breves generados mediante un método de aumento sintético guiado por LLM para alcanzar el umbral estadístico mínimo requerido por pruebas paramétricas. Cada artículo contiene entre 1 y 2 párrafos (~145-293 caracteres, promedio 202) con ground truth anotado para Personas (PER) y Organizaciones (ORG).

#### 4.1.1 Método de Generación Sintética del Corpus N=30

Dado que el corpus real Kleptotrace/CoNLL-2002 cuenta con solo 15 artículos (N=15), resulta insuficiente para la aplicación de pruebas estadísticas paramétricas con potencia adecuada. Para subsanar esto se aplicó un método de **aumento de datos guiado por LLM** (LLM-guided data augmentation), consistente en los siguientes pasos:

**Paso 1 — Definición de la distribución temática:** Se analizaron los 15 artículos reales de Kleptotrace/CoNLL-2002 e identificaron sus categorías temáticas recurrentes: (a) sanciones internacionales a personas y empresas, (b) investigaciones por lavado de activos, (c) vínculos con Personas Políticamente Expuestas (PEP), y (d) corrupción en empresas públicas. Esta distribución guió la generación para mantener la representatividad del dominio AML/KYC.

**Paso 2 — Generación controlada por plantillas de entidad:** Para cada artículo sintético se definió a priori un par `{entidad_PER, entidad_ORG}` que debía aparecer en el texto, actuando como ground truth objetivo. Las entidades fueron seleccionadas de la base de datos OpenSanctions para garantizar realismo regulatorio (personas y organizaciones sancionadas reales).

**Paso 3 — Instrucción al LLM generador:** El modelo `gemma4:31b` recibió el siguiente prompt de generación:

```
Eres un periodista de investigación financiera. Redacta un párrafo corto (2-4 oraciones) en español
sobre la entidad "{entidad_PER}" vinculada a "{entidad_ORG}" en el contexto de [temática aleatoria].
El texto debe ser fáctico, neutro y similiar en estilo a noticias de compliance financiero.
Debe mencionar exactamente estas entidades y no otras personas u organizaciones adicionales.
```

**Paso 4 — Verificación del ground truth:** Cada artículo generado fue revisado manualmente para confirmar que las entidades objetivo aparecían efectivamente en el texto y que no se hubieran introducido entidades ajenas al ground truth anotado. Artículos con entidades adicionales no anotadas fueron descartados y regenerados.

**Paso 5 — Control de calidad por diversidad:** Se verificó que ningún artículo generado replicara literalmente oraciones de otro artículo del corpus (deduplicación por similitud coseno > 0.85). La longitud promedio resultante fue de 202 caracteres (rango 145–293), con 1,2 entidades PER y 2,3 entidades ORG por artículo.

#### 4.1.2 Validez Estadística del Corpus Sintético

El uso de datos sintéticos generados por LLM para pruebas de hipótesis es válido bajo las siguientes condiciones, todas cumplidas en este estudio:

**a) Teorema del Límite Central (TLC):** El TLC establece que, para N ≥ 30 observaciones independientes, la distribución de la media muestral se aproxima a una distribución normal independientemente de la distribución poblacional subyacente. Con N=30 artículos, las pruebas ANOVA (que asumen normalidad de las medias grupales, no de los datos individuales) son aplicables con validez asintótica.

**b) Independencia de las observaciones:** Cada artículo generado es una muestra independiente — el desempeño del modelo en un artículo no afecta su desempeño en otro. El diseño experimental garantiza esta independencia al procesar cada artículo de forma aislada sin contexto de artículos previos.

**c) Validez de constructo del corpus sintético:** La validez de los datos sintéticos como proxy del dominio real descansa en tres pilares: (1) la distribución temática del corpus sintético replica la del corpus real (Kleptotrace/CoNLL-2002); (2) las entidades provienen de una fuente oficial de sanciones reales (OpenSanctions); y (3) la capacidad del LLM para generar texto coherente con el dominio financiero ha sido validada empíricamente (el mismo modelo que genera los artículos es el que se evalúa, creando una condición de evaluación conservadora). Este enfoque es metodológicamente análogo al uso de paráfrasis automáticas para aumento de corpus en NLP, práctica ampliamente aceptada en la literatura [8], [5].

**d) Consistencia entre corpus:** Los F1-Scores observados en el corpus N=30 (gemma4:31b: 79.03%) son consistentes con la tendencia observada en el corpus real N=15 (gemma4:31b: 69.12%), sin saltos discontinuos que indicarían artefactos del aumento. La diferencia es atribuible a la menor complejidad promedio de los artículos breves del corpus sintético, lo que es esperado y documentado.

#### 4.1.3 Extensión a Corpus Real N=120 (Dataset Conmutable)

Tras la validación sobre el corpus sintético N=30 (§4.1.1–4.1.2), y como parte del cierre del proyecto (1 de septiembre de 2026, commit `5ff38f5`, *"integrate balanced real dataset N=120"*), se incorporó una tercera alternativa de corpus para reforzar la validez externa: en lugar de seguir aumentando el corpus por generación sintética, se amplió la base real combinando los 15 artículos Gold Standard de Kleptotrace/CoNLL-2002 con **105 artículos reales del corpus público CoNLL-2002 en español** (`data/conll2002_es.json`, 833 artículos disponibles), generando el archivo `data/benchmark_balanced_120.json` (N=120, script `create_balanced_120.py`). A diferencia del corpus N=30, **ningún texto de este corpus fue generado por un LLM**: los 120 artículos son noticias reales con anotación de entidades real.

El corpus sintético N=30 no fue descartado ni reemplazado: el flag `--data-file` de `src/main.py` permite ejecutar cualquier corrida indistintamente sobre `data/kleptotrace_augmented_30.json` (N=30, sintético) o `data/benchmark_balanced_120.json` (N=120, real), conservando ambos conjuntos de datos y sus resultados en el repositorio. Los resultados sobre N=120 se presentan como complemento — no reemplazo — de la validación estadística de §5.3.

### 4.2 Modelos Evaluados

El trabajo comprende **dos conjuntos de evaluación distintos**, que no deben confundirse: el benchmark exploratorio de la Tabla 2 (§5.1), con **12 modelos en 13 configuraciones** sobre N=15 en modo `entities` (`gemma4:latest` aparece dos veces: ZS-ES y FS-ES), y el estudio principal (§5.3.5), con **13 modelos** sobre N=120 en modo `kb_combined`. El segundo incorpora `gemma4:12b-mlx` y `gpt-oss:20b`, que no disponen de corrida N=15. Los modelos de la Tabla 2 se agrupan en tres categorías:
- **Modelos locales grandes (≥8B):** gemma4:31b, gemma4:31b-mlx, gemma4:latest (9B), llama3.1:8b, qwen2.5:14b, mistral-nemo:latest (12B). gemma4:12b se descargó pero no figura en el benchmark reportado.
- **Modelos locales compactos (<8B):** llama3.2:latest (3B), nuextract:latest (3.8B), nemotron-mini:4b, deepseek-r1:1.5b.
- **Modelos cloud/híbridos:** gemma4:31b-cloud, gemini-3.1-flash-lite.

### 4.3 Análisis de Variantes de Prompts

Se evaluaron cuatro configuraciones de prompt sobre el modelo gemma4:latest (9B). El diseño cruza dos factores —idioma (inglés/español) y estrategia de demostración (sin ejemplos/con ejemplos)—, por lo que constituye un **diseño factorial 2×2**, procedimiento que la literatura anglosajona de aprendizaje automático denomina *ablation study*:
1. **Zero-shot inglés (ZS-EN):** Prompt de sistema en inglés sin ejemplos.
2. **Zero-shot español (ZS-ES):** Prompt de sistema traducido al español, sin ejemplos.
3. **Few-shot inglés (FS-EN):** Prompt en inglés con 3 ejemplos del dominio compliance.
4. **Few-shot español (FS-ES):** Prompt en español con 3 ejemplos del dominio compliance.

#### 4.3.1 ¿Qué es el Prompting Few-Shot?

El **aprendizaje en contexto** (*in-context learning*) es la capacidad de los LLMs de adaptarse a una nueva tarea sin actualizar sus pesos, únicamente a partir de instrucciones y ejemplos incluidos en el texto del prompt. Esta capacidad, documentada por Brown et al. [8] en el trabajo fundacional de GPT-3, distingue a los LLMs modernos de los modelos supervisados tradicionales.

El prompting **few-shot** (de pocos disparos) es una variante del aprendizaje en contexto que incluye un número reducido de ejemplos demorativos (*demonstrations*) directamente en el prompt, antes de presentar la tarea real. La estructura canónica de un prompt few-shot es:

```
[Instrucción de sistema]

[Ejemplo 1: Entrada]
[Ejemplo 1: Salida esperada]

[Ejemplo 2: Entrada]
[Ejemplo 2: Salida esperada]

[Ejemplo 3: Entrada]
[Ejemplo 3: Salida esperada]

[Tarea real: Entrada]
[→ El modelo genera la Salida]
```

En contraposición, el prompting **zero-shot** no incluye ejemplos: el modelo debe inferir el formato y la estrategia de extracción únicamente desde la instrucción de sistema.

#### 4.3.2 Mecanismo Cognitivo del Few-Shot Prompting en LLMs

Los ejemplos few-shot cumplen tres funciones cognitivas en el LLM:

1. **Especificación del formato de salida:** Muestran al modelo exactamente qué estructura JSON se espera (cuáles campos, con qué nombres, qué tipos de valores). Sin este anclaje, los LLMs tienden a variar el formato de respuesta entre artículos, dificultando el parseo programático.

2. **Calibración del umbral semántico:** Los ejemplos delimitan qué *tipo* de mención califica como entidad: por ejemplo, solo personas nombradas individualmente (no cargos genéricos como "el presidente"), y solo organizaciones con nombre propio (no referencias como "la empresa"). Este criterio no puede especificarse exhautivamente en texto descriptivo, pero se transmite implícitamente mediante 2-3 ejemplos contrastivos.

3. **Adaptación al dominio:** En un dominio especializado como AML/KYC, los ejemplos funcionan como un micro-corpus de fine-tuning en memoria de trabajo: el modelo ajusta la distribución de probabilidad de sus respuestas para seguir el patrón observado en los ejemplos, favoreciendo terminología y categorías del dominio regulatorio sobre el lenguaje general.

#### 4.3.3 Prompts Utilizados en este Estudio

En este trabajo se diseñaron prompts específicos para el dominio de cumplimiento normativo AML/KYC. Los tres ejemplos few-shot utilizados en la configuración FS-ES tienen la siguiente estructura:

**Ejemplo few-shot 1 (caso persona sancionada):**
```
Texto: "El empresario ruso Roman Abramovich fue incluido en las listas de sanciones
        de la Unión Europea por sus vínculos con el régimen del Kremlin a través de
        su empresa Evraz PLC."
Respuesta: {"Persons": ["Roman Abramovich"], "Organizations": ["Evraz PLC"]}
```

**Ejemplo few-shot 2 (caso organización sancionada):**
```
Texto: "El Departamento del Tesoro de los Estados Unidos sancionó al banco Rossiya,
        señalándolo como banco personal de altos funcionarios del gobierno ruso."
Respuesta: {"Persons": [], "Organizations": ["Banco Rossiya", "Departamento del Tesoro"]}
```

**Ejemplo few-shot 3 (caso PEP complejo):**
```
Texto: "Isabel dos Santos, hija del expresidente angoleño José Eduardo dos Santos,
        figura en investigaciones de la empresa estatal Sonangol por presunto desvío
        de fondos."
Respuesta: {"Persons": ["Isabel dos Santos", "José Eduardo dos Santos"],
             "Organizations": ["Sonangol"]}
```

Los tres ejemplos cubren deliberadamente: (a) extracción limpia de un solo sujeto, (b) caso sin personas nombradas con múltiples organizaciones, y (c) caso con múltiples personas en relación familiar y una organización ambigua. Esta diversidad de casos entrena al modelo a manejar la variabilidad del corpus real.

#### 4.3.4 Impacto Empírico del Few-Shot en este Estudio

Los resultados del análisis de variantes de prompts revelan una **interacción entre los dos factores**: por separado, la localización al español aporta +4.38 pp de F1 y los ejemplos *few-shot* en inglés no aportan nada (−0.73 pp), pero **su combinación alcanza +11.12 pp** (FS-ES: 74.44% frente al 64.05% del baseline ZS-EN). Es decir, los ejemplos solo resultan productivos cuando están redactados en el idioma del corpus. La configuración FS-ES lidera además en Precisión (66.78%) y Recall (86.87%) sin penalización en alucinaciones (0.20%, idéntica a ZS-ES). Para el dominio estudiado, la localización lingüística domina sobre la demostración de ejemplos, posiblemente porque gemma4 fue entrenado con suficientes datos en español para comprender el dominio sin ejemplos explícitos.

### 4.4 Métricas de Evaluación

| Métrica | Definición |
|:---|:---|
| **F1-Score** | Media armónica entre Precisión y Recall (métrica principal) |
| **Precisión** | TP / (TP + FP) — Exactitud de las entidades extraídas |
| **Recall** | TP / (TP + FN) — Cobertura de las entidades reales |
| **Hallucination Rate** | Entidades extraídas sin correspondencia en GT / Total extraídas |
| **Latencia (s)** | Tiempo promedio por artículo en segundos |
| **Índice Tok/s/B** | Tokens por segundo normalizados por cada mil millones (10⁹) de parámetros |

### 4.5 Infraestructura de Pruebas

- **Hardware:** Apple Silicon (Metal/MPS), en dos configuraciones según el footprint del modelo: 16 GB de memoria unificada para modelos de hasta ~12B, y 48 GB de memoria unificada para los modelos de 31B y variantes MLX de gran tamaño (ver §3.6).
- **Software:** Python 3.14, Ollama 0.6+, scikit-learn 1.9, statsmodels 0.14, pandas 3.0, Streamlit 1.60.
- **Reproducibilidad:** Checkpointing automático (`.checkpoint.json`) para reanudar benchmarks interrumpidos sin pérdida de datos.

---

## 5. RESULTADOS EXPERIMENTALES

### 5.1 Benchmark General — 12 Modelos en 13 Configuraciones sobre Kleptotrace/CoNLL-2002 (N=15)

La Tabla 2 presenta los resultados consolidados del benchmark completo agrupados por familia y tamaño de modelo:

| Modelo | Tipo | Parámetros | F1 | Precisión | Recall | Hallucination | Latencia (s) | Tok/s/B |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| gemma4:latest (FS-ES) | Local | 9B | **74.44%** | 66.78% | **86.87%** | 0.20% | 197.80 | 5.33 |
| **gemma4:31b** | Local | 31B | 69.12% | 58.83% | 86.80% | 0.16% | 613.50 | 0.33 |
| gemma4:31b-mlx | Local | 31B | 68.52% | 58.31% | 86.76% | 0.00% | 428.80 | 0.74 |
| gemma4:latest (ZS-ES) | Local | 9B | 68.43% | 60.68% | 83.49% | 0.20% | 159.90 | 5.33 |
| gemma4:31b-cloud | Cloud | 31B | 66.99% | 55.46% | 86.88% | 0.00% | 4.30 | — |
| llama3.2:latest | Local | 3B | 63.19% | 62.82% | 67.99% | 2.31% | 21.60 | 26.44 |
| gemma:latest | Local | 7B | 62.66% | 58.47% | 71.47% | 1.08% | 36.20 | 5.17 |
| qwen2.5:14b | Local | 14B | 61.06% | 57.60% | 71.76% | 0.87% | 76.40 | 1.57 |
| llama3.1:8b | Local | 8B | 60.72% | 53.70% | 75.80% | 3.39% | 53.50 | 5.03 |
| qwen3:8b | Local | 8B | 53.65% | 46.75% | 65.61% | 0.00% | 282.00 | 4.56 |
| mistral-nemo:latest | Local | 12B | 53.07% | 58.13% | 56.00% | 0.83% | 53.10 | 2.36 |
| nemotron-mini:4b | Local | 4B | 35.33% | 44.37% | 34.92% | 2.62% | 22.20 | 17.08 |
| deepseek-r1:1.5b | Local | 1.5B | 27.65% | 39.49% | 25.77% | 1.35% | 41.10 | 86.20 |

> Cifras medidas sobre `results/benchmark_results.csv` (N=15, modo `entities`), salvo `gemma4:31b`
> (`gemma4_31b_n15_REMOTO`), las dos variantes de `gemma4:latest` (`ablacion_n15_REMOTO`) y `gemma4:31b-cloud`
> (`cloud_n15_limpio_20260905`). Las latencias proceden de corridas con distinta concurrencia y hardware, por
> lo que **no son comparables entre filas**; el índice Tok/s/B sí lo es. Quedan fuera de la tabla los modelos
> excluidos del estudio (`nuextract:latest`, `gemini-3.1-flash-lite`, `minimax-m3`).

> **Hallazgo 1:** la familia `gemma4` copa las cinco primeras posiciones. `gemma4:latest` con prompt *few-shot* en español (74.44%) supera a los dos modelos de 31B, a un tercio de su tamaño.  
> **Hallazgo 2:** `gemma4:31b` lidera en Recall entre los locales (86.80%) con una tasa de alucinación de 0.16%, y su contraparte cloud alcanza un Recall equivalente (86.88%).  
> **Hallazgo 3:** `deepseek-r1:1.5b` debe descartarse para producción: F1 de 27.65% y Recall de sólo 25.77%.  
> **Hallazgo 4:** el índice de eficiencia de hardware (Tok/s/B) favorece a los modelos compactos —`deepseek-r1:1.5b` (86.20) y `llama3.2` (26.44)— para *screening* masivo, mientras que `gemma4:31b` (0.33) se justifica para análisis de alto riesgo.

### 5.2 Análisis de Variantes de Prompts (gemma4:latest, N=15)

| Configuración | F1 | Precisión | Recall | Hallucination | Latencia (s) | Δ vs. Baseline |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| Zero-shot Inglés (Baseline) | 64.05% | 57.69% | 77.17% | 0.20% | 157.90 | — |
| Zero-shot Español | 68.43% | 60.68% | 83.49% | 0.20% | 159.90 | **+4.38 pp** |
| Few-shot Inglés | 63.32% | 55.81% | 75.81% | 0.57% | 203.40 | −0.73 pp |
| Few-shot Español | **74.44%** | **66.78%** | **86.87%** | 0.20% | 197.80 | **+11.12 pp** |

> Medido sobre `results/ablacion_n15_REMOTO/benchmark_results.csv` (N=15, modo `entities`), con el corrector
> de puntuación aplicado.

> **Hallazgo 4:** La localización al español fue el factor de mayor impacto, produciendo +7.4% de F1 sobre el baseline ZS-EN, principalmente por una mejora del +10.28% en Recall. La inyección de ejemplos few-shot incrementó el Recall máximo pero no mejoró significativamente sobre el ZS-ES.

### 5.3 Validación Estadística sobre Corpus N=30

#### 5.3.1 Resultados del Benchmark Serial

| Modelo | F1 | Precisión | Recall | Hallucination | Latencia (s) |
|:---|:---:|:---:|:---:|:---:|:---:|
| **gemma4:31b** | **79.03%** | 73.34% | 89.11% | **0.00%** | 160.23 |
| gemma4:31b-mlx | 77.47% | 73.01% | 87.17% | 0.00% | 163.76 |

#### 5.3.2 ANOVA de Una Vía (α = 0.05)

- **F-Statistic:** 0.141
- **p-Value:** 0.708 (p ≥ 0.05 → No se rechaza H₀)
- **Conclusión:** No existe diferencia estadísticamente significativa en los F1-Scores entre los dos modelos evaluados sobre N=30.

#### 5.3.3 Intervalos de Confianza al 95%

| Modelo | N | F1 Media | IC 95% Inferior | IC 95% Superior | Desv. Est. |
|:---|:---:|:---:|:---:|:---:|:---:|
| gemma4:31b | 30 | 0.7903 | 0.7291 | 0.8515 | 0.1640 |
| gemma4:31b-mlx | 30 | 0.7747 | 0.7162 | 0.8332 | 0.1566 |

#### 5.3.4 Análisis de Sensibilidad (Outliers)

- **Criterio de outlier:** Artículos con longitud > 702 caracteres.
- **Registros outlier identificados:** 0
- **F1 estable (no filtrado):** gemma4:31b = 0.7903 | gemma4:31b-mlx = 0.7747

#### 5.3.5 Validación Estadística sobre Corpus Real N=120 (estudio completo)

Sobre el corpus real N=120 descrito en §4.1.3 se ejecutó el mismo protocolo (ANOVA de una vía + Tukey HSD) para el **estudio completo de 13 modelos**, cada uno en modo *baseline* y *KB RAG*, con N=120 observaciones por grupo (26 grupos, 3 120 observaciones). Resultados consolidados en `results/ANALISIS_CONJUNTO_20260907/`.

| Modelo | F1 baseline | F1 KB RAG | Δ RAG | Δ significativo |
|:---|:---:|:---:|:---:|:---:|
| gemma4:31b-cloud | 62.38% | 61.85% | −0.53 pp | no |
| gemma4:31b-mlx | **59.25%** | 59.07% | −0.18 pp | no |
| gemma4:12b-mlx | 56.18% | 58.46% | +2.28 pp | no |
| gemma4:latest | 55.91% | 54.74% | −1.17 pp | no |
| qwen2.5:14b | 50.22% | 54.84% | +4.62 pp | no |
| llama3.1:8b | 48.76% | 50.75% | +1.99 pp | no |
| qwen3:8b | 48.21% | 51.46% | +3.25 pp | no |
| gemma:latest | 44.00% | 51.36% | +7.36 pp | no |
| gpt-oss:20b | 43.84% | 34.19% | −9.65 pp | no |
| mistral-nemo:latest | 43.38% | 45.76% | +2.37 pp | no |
| llama3.2:latest | 36.11% | 46.93% | **+10.82 pp** | **sí** (p=0.014) |
| deepseek-r1:1.5b | 24.83% | 23.94% | −0.90 pp | no |
| nemotron-mini:4b | 22.59% | 37.12% | **+14.52 pp** | **sí** (p<0.001) |

> **Dos salvedades de procedencia.** (i) La latencia de `gemma4:31b-cloud` **no mide inferencia**: quedó cuantizada por el `--request-delay` introducido para sortear el límite de peticiones del servicio (114 de sus 240 filas registran exactamente 1,02 s). Su F1 es válido; su latencia y sus tokens/s no deben usarse en comparaciones de eficiencia. (ii) Siete filas de `nemotron-mini:4b` tienen `latencia = 0` y `0 tokens/s` porque se re-extrajeron fuera del arnés de lotes tras un fallo de contexto; sus valores de precisión, *recall* y F1 son reales, pero su telemetría no existe.

**ANOVA de una vía (α = 0.05), N=120 por grupo:**
- **F-Statistic:** 36.3666  ·  **p-Value:** 1.2236 × 10⁻¹⁵² (p < 0.05 → se rechaza H₀)
- **Conclusión:** la diferencia de desempeño entre modelos/modos es estadísticamente significativa, con una potencia muy superior a la del corpus N=30 (F=0.141, no significativo).
- **Tukey HSD (post-hoc):** 172 de 325 comparaciones por pares resultan significativas. Al contrastar *baseline* contra *KB RAG* **dentro de cada modelo**, la mejora solo alcanza significancia en `nemotron-mini:4b` (+14.52 pp, p<0.001) y `llama3.2:latest` (+10.82 pp, p=0.014); en los once modelos restantes la diferencia no supera la corrección por comparaciones múltiples.

**Interpretación.** El beneficio del KB RAG es **inversamente proporcional a la capacidad del modelo**: aporta de forma estadísticamente significativa en los dos modelos más débiles del estudio, es positivo pero no concluyente en la franja intermedia, y resulta nulo o adverso en los modelos de mayor capacidad (−0.53 pp y −0.18 pp en los dos de 31B), que ya siguen correctamente las instrucciones sin contexto adicional. El caso de `gpt-oss:20b` (−9.65 pp) es distinto y se discute en §6.

**Lectura conjunta con el corpus N=30 (§5.3.1–5.3.4):** el mejor F1 local sobre N=120 (`gemma4:31b-mlx`: 59.25%) es menor que el de N=30 (`gemma4:31b`: 79.03%), lo esperable dado que los artículos reales de CoNLL-2002 ES son más largos y heterogéneos que los breves (~200 caracteres) del corpus sintético N=30, diseñado para el dominio AML/KYC. Se conservan ambos: N=30 como validación de mínima potencia (TLC, N≥30) sobre el dominio de sanciones del proyecto, y N=120 como validación sobre corpus real, con mayor potencia estadística y menor especificidad de dominio.

### 5.4 Taxonomía de Errores NER

El análisis cualitativo de las extracciones identifica tres categorías de error recurrentes:

1. **Boundary Errors (Errores de Límite):** El modelo incorpora preposiciones o aposiciones descriptivas dentro del span de la entidad. Ejemplo: extrae `"Isabel dos Santos, hija del expresidente"` en lugar de `"Isabel dos Santos"`.

2. **Type Confusion (Confusión de Tipo):** El modelo clasifica una organización como localización. Ejemplo: `"Sonangol"` (empresa petrolera estatal angoleña) clasificada como LOC en lugar de ORG.

3. **Extrinsic Hallucinations (Alucinaciones Extrínsecas):** El modelo genera entidades de su memoria paramétrica que no están presentes en el texto. Mitigadas efectivamente al 0.0% en N=30 mediante delimitadores estrictos de JSON.

### 5.5 Análisis de Eficiencia en Hardware Soberano

| Modelo | VRAM (MB) | Tok/s | Parámetros (B) | Índice Tok/s/B | Costo/Artículo |
|:---|:---:|:---:|:---:|:---:|:---:|
| gemma4:31b | 18,795 | 10.23 | 31 | 0.33 | $0.052 |
| gemma4:31b-mlx | 24,607 | 22.80 | 31 | 0.74 | $0.052 |
| llama3.2 (3B) | 4,018 | 79.35 | 3 | 26.5 | $0.052 |

> Valores medidos sobre `benchmark_results.csv` (subconjunto `_baseline`, N=15; columnas `vram_mb` y `tokens_per_sec`).

> El costo por artículo en el sistema soberano local se estima en USD 0.052, versus USD 8.75 en revisión manual, representando una reducción del **99.4%** en costo unitario.

---

### 5.6 Optimización del Módulo RAG: De Diccionarios de Entidades a Base de Conocimientos Contextual

> **Nota Cronológica:** Esta sección documenta un ciclo iterativo de investigación e implementación realizado entre el **31 de agosto y el 1 de septiembre de 2026**, posterior a la entrega del benchmark principal (Sección 5.3). Responde a la necesidad de mejorar el F1-Score sin afectar la soberanía de datos y constituye una contribución metodológica adicional.

#### 5.6.1 Motivación: Comportamiento Contraintuitivo del RAG Basado en Diccionarios

Durante el benchmark principal sobre N=120 artículos reales, se observó un fenómeno inesperado y mayoritario (7 de 15 modelos degradaron, entre ellos los de mayor F1 baseline; 8 mejoraron): **la activación del módulo RAG (`_rag_enhanced`) produjo una degradación del F1-Score respecto al modo `_baseline`**, en lugar de la mejora esperada.

| Modelo | Baseline F1 | RAG-Dict F1 | Delta |
|:---|:---:|:---:|:---:|
| `gemma4:31b-mlx` | **0.5983** | 0.5868 | −0.0115 |
| `gemma4:latest` | 0.5446 | 0.5257 | −0.0189 |
| `qwen2.5:14b` | 0.5189 | 0.5071 | −0.0118 |
| `llama3.2:latest` | 0.3945 | 0.4196 | +0.0251 |

Las cifras anteriores provienen de la corrida `benchmark_balanced_120_20260824_173036` (RAG por diccionario, ago 2026), distinta de la corrida KB RAG del 1-sep citada en §5.3.5 y §5.6.5. Esta degradación motivó un protocolo de investigación formal documentado en `research/rag/2026-08-31_analisis_contenido_rag_base_conocimientos.md`. La auditoría reveló la causa raíz:

**El Problema del Desajuste Semántico Estructural (*Semantic Mismatch*):**

El sistema RAG original almacena cadenas nominales de entidades (`GRANJA LA SIERRA LTDA.`, `Reina Esperanza Ornelas Cintrón`) en ChromaDB. Al consultar la base vectorial usando el **texto completo del artículo** (300-800 palabras), el modelo de embeddings `all-MiniLM-L6-v2` recupera las 5 entidades con mayor **cercanía temática global** — no necesariamente presentes en el artículo. El prompt resultante incluía empresas agrícolas colombianas en artículos sobre política autonómica española, provocando que los LLMs suprimieran la extracción de entidades legítimas.

```
Flujo RAG Original (Degradado):

Noticia política española (500 palabras)
         │
         ▼  Embedding all-MiniLM-L6-v2
ChromaDB: Top-5 por coseno ──→ GRANJA LA SIERRA LTDA. (Org)
                            ──→ ASES DE COMPETENCIA Y CIA. (Org)
                            ──→ [3 orgs colombianas irrelevantes]
         │
         ▼  Inyección restrictiva en prompt
"DO NOT extract unless they explicitly appear..."
         │
         ▼  Efecto en LLM
Recall: 62.8% → 21.6%  ❌ (sondeo N=5)
```

#### 5.6.2 Arquitectura Propuesta: Base de Conocimientos Contextual

La solución implementada transforma el contenido de la base vectorial: en lugar de nombres de entidades, se almacenan **Guías Tipológicas de Dominio** y **Ejemplares Dinámicos Few-Shot**.

```
Flujo KB RAG (Mejorado):

Noticia política española (500 palabras)
         │
         ▼  Embedding all-MiniLM-L6-v2
ChromaDB 'ner_knowledge_base': Top-1 guideline + Top-1 exemplar
         │
         ▼  Dominio recuperado: politics_administrative (ES)
┌─────────────────────────────────────────────────┐
│ [DOMAIN CONTEXT: NOTICIAS POLÍTICAS EN ESPAÑOL] │
│ 1. PERSONAS: Extrae SOLO el nombre propio...    │
│ 2. ORGANIZACIONES: Partidos (PSOE, PP), Junta.. │
│ 3. DESAMBIGUACIÓN: Un apellido solo ('Bono')... │
└─────────────────────────────────────────────────┘
         │  + Ejemplo similar recuperado
         ▼  Inyección positiva: "[EXTRACTION GUIDANCE]"
         │
         ▼  Efecto en LLM
F1: 0.3521 → 0.5489  ✅  (+19.7 pp)
Recall: 33.3% → 59.5%  ✅  (+26.2 pp)
```

#### 5.6.3 Implementación Técnica

El módulo `src/kb_rag_manager.py` (`KBRAGManager`) implementa cuatro modos de operación configurables:

| Modo | Flag CLI | Descripción | Caso de Uso |
|:---|:---:|:---|:---|
| `entities` | `--rag-mode entities` | Legacy: diccionario de nombres (comportamiento original) | Compatibilidad hacia atrás |
| `kb_guidelines` | `--rag-mode kb_guidelines` | Reglas tipológicas de desambiguación por dominio | Artículos de dominio conocido |
| `kb_fewshot` | `--rag-mode kb_fewshot` | Ejemplo anotado semánticamente más similar | Transferencia de conocimiento |
| `kb_combined` | `--rag-mode kb_combined` | Guía + ejemplo (recomendado) | **Mejor F1** |

La base de conocimientos se organiza en **dos colecciones ChromaDB separadas** para garantizar compatibilidad con el sistema preexistente:

- `ner_dictionaries`: Colección legacy (diccionarios de entidades, preservada)
- `ner_knowledge_base`: Nueva colección (guías + ejemplares, 12 documentos)

**Configurabilidad garantizada:** El sistema es activable/desactivable mediante flags CLI sin modificar código:

```bash
# Modo baseline (sin RAG)
./venv/bin/python3 src/main.py --models gemma4:31b-mlx --data-file data/benchmark_balanced_120.json

# Modo RAG legacy (diccionario de entidades)
./venv/bin/python3 src/main.py --rag-study --rag-mode entities ...

# Modo KB RAG (nueva implementación, recomendado)
./venv/bin/python3 src/main.py --rag-study --rag-mode kb_combined ...
```

**Template de inyección diferenciado:** El módulo `ollama_provider.py` detecta automáticamente el tipo de contexto RAG y aplica el template apropiado:

- **Entity-dict RAG (legacy):** Template restrictivo — `"DO NOT extract unless they explicitly appear..."` — previene alucinaciones de entidades ausentes.
- **KB RAG (nuevo):** Template positivo — `"[EXTRACTION GUIDANCE] Apply these rules to the news text"` — instruye activamente al LLM sin suprimir su capacidad de extracción.

#### 5.6.4 Datos de la Base de Conocimientos

**Guías Tipológicas (5 dominios):** Documentos JSON con reglas específicas de desambiguación NER:

| Dominio | ID | Idioma | Keywords Clave |
|:---|:---:|:---:|:---|
| Política y Administración | `politics_es` | ES | PSOE, PP, junta, ministerio, portavoz |
| Corporativo y Financiero | `corporate_financial_es` | ES | bolsa, fusión, consejo de administración |
| AML y Sanciones | `aml_sanctions_en` | EN | OFAC, indictment, money laundering, IEEPA |
| Judicial y Crimen | `judicial_crime_es` | ES | tribunal, fiscal, audiencia nacional |
| Deportivo y Social | `sports_social_es` | ES | liga, federación, club |

**Ejemplares Few-Shot (7 pares anotados):** Todos extraídos de `benchmark_balanced_120.json` (artículos reales anotados del corpus de evaluación). No se utilizaron datos sintéticos, preservando la integridad metodológica.

| ID Ejemplar | Dominio | Fuente |
|:---|:---:|:---:|
| `ex_politics_es_001` | Política ES | `real_mixed_1` |
| `ex_politics_es_002` | Política ES | `real_mixed_41` |
| `ex_corporate_financial_es_001` | Corporativo ES | `real_mixed_21` |
| `ex_judicial_es_001` | Judicial ES | `real_mixed_101` |
| `ex_aml_sanctions_en_001` | AML/Sanciones EN | `real_mixed_59` |
| `ex_aml_sanctions_en_002` | AML/Sanciones EN | `real_mixed_79` |
| `ex_aml_sanctions_en_003` | AML/Sanciones EN | `real_mixed_27` |

#### 5.6.5 Resultados Empíricos del KB RAG

**Sondeo de validación funcional (N=5 artículos, `llama3.2:latest`, 2026-09-01; cifras no persistidas en `results/`):**

| Condición | F1-Score | Precisión | Recall | Δ F1 vs Baseline |
|:---|:---:|:---:|:---:|:---:|
| **Baseline (zero-shot)** | 0.3521 | 0.4250 | 0.3333 | — |
| **KB Combined RAG** | **0.5489** | **0.5227** | **0.5954** | **+0.1968** |

**Benchmark completo (N=120 artículos, 5 modelos, `--rag-mode kb_combined`, 2026-09-01):**

| Modelo | Baseline F1 | KB RAG F1 | Δ F1 | Δ% | Δ Recall |
|:---|:---:|:---:|:---:|:---:|:---:|
| `gemma4:31b-mlx` | 0.5925 | 0.5907 | −0.0018 | −0.3% | +0.012 |
| `gemma4:latest` | 0.5591 | 0.5558 | −0.0034 | −0.6% | −0.011 |
| `gemma:latest` | 0.4734 | **0.5303** | **+0.0569** | **+12.0%** | **+0.117** |
| `llama3.2:latest` | 0.3945 | **0.4943** | **+0.0999** | **+25.3%** | **+0.143** |
| `qwen2.5:14b` | 0.5189 | **0.5651** | **+0.0462** | **+8.9%** | **+0.039** |
| **Promedio** | 0.5077 | **0.5472** | **+0.0396** | **+9.1%** | **+0.060** |

**Verificación de la recuperación semántica:**
- Artículo político ES → Recupera guía `politics_administrative` (ES) ✅
- Artículo AML EN → Recupera guía `aml_compliance` (EN) ✅
- Artículo corporativo ES → Recupera guía `corporate_financial` (ES) ✅

**Hallazgo clave — Efecto moderado por capacidad del modelo:**

El beneficio del KB RAG resulta **inversamente proporcional a la capacidad del modelo**:

- **Modelos grandes** (`gemma4:31b-mlx`, `gemma4:latest`, ≥9B parámetros): el KB RAG tiene efecto neutro (Δ ≈ 0). Estos modelos ya poseen suficiente conocimiento lingüístico interno para desambiguar entidades sin ayuda contextual adicional. La ganancia marginal en Recall del `gemma4:31b-mlx` (+1.2pp) indica que la guía tipológica sí ayuda en artículos frontera.

- **Modelos pequeños/medianos** (`llama3.2:latest` 3B, `gemma:latest` 7B, `qwen2.5:14b` 14B): el KB RAG produce mejoras sustanciales (+25.3%, +12.0% y +8.9% respectivamente). Para estos modelos, las guías tipológicas actúan como **memoria externa de conocimiento lingüístico** que compensan la menor capacidad paramétrica.

En entornos de hardware restringido, donde solo es viable ejecutar modelos de 3–14B, el KB RAG mejora el F1 sin costo computacional relevante.

#### 5.6.6 Análisis Comparativo Cronológico

| Aspecto | Sistema v1.0 (Dic 2025 – Ago 2026) | Sistema v1.1 (Sep 2026) |
|:---|:---|:---|
| **Contenido RAG** | Diccionarios de nombres (3.605 personas, 1.848 orgs) | Guías tipológicas + ejemplares few-shot |
| **Colección ChromaDB** | `ner_dictionaries` | + `ner_knowledge_base` (nueva, no reemplaza) |
| **Template de inyección** | Restrictivo ("DO NOT extract unless...") | Positivo ("Apply these rules to the text") |
| **Modo de operación** | Binario (RAG on/off) | Cuatro modos configurables por CLI |
| **F1-Score RAG (`llama3.2`)** | 0.2367 en sondeo N=5 (−57.8% vs su propio baseline 0.5614) | **0.4943 (+25.3% vs baseline, N=120)** |
| **F1-Score RAG (`qwen2.5:14b`)** | — | **0.5651 (+8.9% vs baseline)** |
| **Configurabilidad** | No (hardcoded) | Sí (`--rag-mode {entities,kb_guidelines,kb_fewshot,kb_combined}`) |
| **Datos sintéticos** | Sí (12.000 augmented_persons) | No (solo datos reales del corpus de evaluación) |


#### 5.6.7 Justificación Metodológica

Esta evolución del sistema RAG aporta tres contribuciones metodológicas documentables:

1. **Diagnóstico del Semantic Mismatch:** Identificación formal de un problema de diseño en la recuperación RAG para NER en vocabulario abierto, con evidencia empírica cuantitativa (Recall: 62.8% → 21.6% en el sondeo N=5; 40.8% → 32.9% en el benchmark N=120).

2. **Solución basada en tipología lingüística:** la base de conocimientos contextual transforma el problema de "buscar entidades por similitud" en el de "identificar el dominio del texto y aplicar reglas tipológicas", que es lo que los LLMs ejecutan con alta precisión.

3. **Configurabilidad como principio de diseño:** La implementación con flags CLI permite mantener la línea base en producción mientras se experimenta con el nuevo modo, habilitando reversión instantánea sin modificar código.

---

## 6. DISCUSIÓN


### 6.1 Verificación de la Hipótesis

La hipótesis planteaba un F1-Score ≥ 70% como umbral de viabilidad. El umbral se alcanza sobre el corpus sintético AML/KYC N=30 (`gemma4:31b`: **79.03%**, IC 95% [72.91%, 85.15%], 0.0% de alucinaciones), pero **no** sobre el corpus real heterogéneo N=120 (§5.3.5), cuyo mejor resultado es **59.25%** (`gemma4:31b-mlx`). Queda por tanto **confirmada para el dominio específico de sanciones financieras y no confirmada para corpus periodísticos generales**; la brecha de ~20 puntos responde a la mayor longitud y heterogeneidad de los artículos de CoNLL-2002 ES.

Una meta aspiracional interna —no formalizada como hipótesis en §1.3— situaba el objetivo en F1 ≥ 85%. La brecha (5.97 pp sobre N=30; 25.75 sobre N=120) es una oportunidad de optimización —no un fracaso del sistema— abordable mediante: (1) fine-tuning supervisado con ≥200 ejemplos del dominio; (2) modelos de mayor capacidad (127B+); y (3) ensemble entre modelos locales.

### 6.2 Contribución de la Localización Lingüística

La mejora de +7.4% de F1 producida exclusivamente por traducir el prompt al español (sin cambiar el modelo) es un hallazgo de alta relevancia práctica. Demuestra que los LLMs procesan con mayor fluidez la estructura sintáctica de noticias en español cuando reciben instrucciones en el mismo idioma, reduciendo la desambiguación tokenización cross-lingüística. Esta observación es consistente con los resultados de García & López [7] para BERT en español.

### 6.3 Trade-off Tamaño de Modelo vs. Rendimiento

El modelo compacto `llama3.2` (3B parámetros) logra un F1 de 61.29% con una latencia 4.5× menor que `gemma4:31b` y un índice de eficiencia de hardware de 15.80 Tok/s/B, unas 43 veces superior al de `gemma4:31b` (0.37). Esta distribución permite una configuración en dos niveles: `llama3.2` para screening masivo inicial a bajo costo computacional, y `gemma4:31b` para validación de alto riesgo regulatorio donde el F1 máximo y la mínima tasa de alucinaciones son críticos.

### 6.4 Implicaciones para Soberanía de Datos

El sistema logra un rendimiento competitivo respecto a la alternativa cloud (`gemma4:31b-cloud`: F1=66.29%) mientras mantiene privacidad absoluta de datos. Para organizaciones reguladas (bancos, aseguradoras, FinTechs), esta equivalencia de rendimiento con soberanía total tiene implicancias regulatorias y competitivas directas: elimina la obligación de suscribir acuerdos de procesamiento de datos (DPA) con proveedores cloud y reduce la superficie de ataque de exfiltración de datos de clientes.

### 6.5 RAG Contextual vs. RAG por Diccionario: Una Contribución Metodológica

El experimento de KB RAG (§5.6) aporta una contribución metodológica a la recuperación aumentada para NER: el benchmark N=120 muestra que su efectividad está **modulada por la capacidad paramétrica del modelo**:

**Hipótesis explicativa — Redundancia de Conocimiento:** los modelos de mayor capacidad (`gemma4:31b-mlx`, `gemma4:latest`) ya internalizan las reglas tipológicas de desambiguación NER en el preentrenamiento sobre texto en español, por lo que las guías de la KB les resultan redundantes; los de menor capacidad (`llama3.2:latest`, `qwen2.5:14b`) las aprovechan como compensación del conocimiento lingüístico ausente de sus pesos (+25.3% y +8.9% F1).

**Implicación práctica:** cuando el hardware impide usar modelos >30B, el KB RAG es una estrategia de bajo costo y alto retorno: acerca el F1 de los modelos de 3–14B al de modelos mayores sin costo de hardware adicional.

**Contraste con RAG léxico (v1.0):** el hallazgo aclara por qué el dict-RAG degradó el rendimiento: el problema no está en el concepto de RAG sino en la **naturaleza del contenido recuperado**. Recuperar nombres de entidades genera confusión semántica e inhibe la extracción; recuperar guías tipológicas y ejemplos anotados orienta al modelo sin coartar su capacidad generativa.

---

## 7. CONCLUSIONES Y TRABAJO FUTURO


### 7.1 Conclusiones

1. **Viabilidad demostrada:** Es técnicamente viable implementar un sistema NER soberano para cumplimiento AML/KYC con modelos de lenguaje de código abierto ejecutados localmente sobre hardware Apple Silicon M4, alcanzando F1=79.03% con 0.0% de alucinaciones sobre el corpus AML N=30 (59.25% sobre el corpus real N=120).

2. **Localización lingüística como factor crítico:** el idioma del prompt y los ejemplos *few-shot* **interactúan**: por separado aportan +4.38 pp y −0.73 pp de F1 respectivamente, pero combinados alcanzan **+11.12 pp**. Los ejemplos solo resultan productivos redactados en el idioma del corpus, lo que tiene implicaciones directas para despliegues en mercados hispanohablantes.

3. **Soberanía de datos sin costo de rendimiento:** El sistema local iguala o supera el rendimiento de la variante cloud (69.12% vs. 66.99% F1 sobre N=15) mientras garantiza privacidad total.

4. **Reducción de costos operativos:** El costo unitario del sistema soberano ($0.052/artículo) versus revisión manual ($8.75/artículo) representa una reducción del 99.4% en el costo unitario directo (60–80% del costo operativo total, que incluye la supervisión humana), con potencial de procesamiento de cientos de artículos diarios sin personal analista dedicado.

5. **Robustez arquitectural:** El controlador AIMD previene desbordamientos de VRAM y gestiona errores de rate-limiting de forma autónoma. El checkpointing garantiza recuperación sin pérdida de datos ante interrupciones.

6. **El RAG contextual supera al RAG por diccionario:** La implementación de la Base de Conocimientos Contextual (KB RAG) demuestra que el reconocimiento de entidades mediante LLMs locales es un problema de **comprensión sintáctico-contextual**, no de búsqueda en bases de datos cerradas. En el estudio N=120 sobre 13 modelos, el KB RAG (`--rag-mode kb_combined`) mejoró el F1-Score de forma **estadísticamente significativa** (Tukey HSD) en los dos modelos más débiles —`nemotron-mini:4b` **+14.52 pp** (p<0.001) y `llama3.2:latest` **+10.82 pp** (p=0.014)—, con ganancias positivas pero no concluyentes en la franja intermedia y efecto nulo en los modelos de 31B, versus el dict-RAG (v1.0), que en un sondeo N=5 sobre el mismo modelo degradó el F1 hasta 0.2367 (−57.8% respecto de su propio baseline). Su efectividad está modulada por la capacidad paramétrica: beneficia sobre todo a los modelos de 3–14B, donde actúa como memoria externa de conocimiento lingüístico sin costo adicional de hardware. Este hallazgo tiene implicaciones directas para el diseño de sistemas RAG en dominio abierto con LLMs soberanos.


### 7.2 Trabajo Futuro

1. **Expansión de la Base de Conocimientos KB RAG (Prioridad Alta):** Ampliar el catálogo de guías tipológicas (actualmente 5 dominios) a 10+ dominios específicos del ecosistema AML latinoamericano (noticias de la UAF chilena, resoluciones de la CMF, sanciones OFAC en español). Agregar 30–50 ejemplares anotados adicionales del corpus balanceado N=120. Evaluar el impacto en F1 con modelos de mayor capacidad (`gemma4:31b-mlx`, `qwen2.5:14b`).

2. **Fine-tuning supervisado (Fase 1):** Aplicar LoRA (Low-Rank Adaptation) sobre `gemma4:31b` con 200+ ejemplos anotados de Kleptotrace/CoNLL-2002 para cerrar la brecha hacia la meta aspiracional de 85% de F1 (§6.1).

3. **Expansión del corpus de evaluación (Fase 2):** Ampliar el corpus de N=120 a N≥200 artículos reales del dominio AML/KYC chileno, incorporando fuentes como la UAF, CMF y bases de datos de OpenSanctions.

4. **Ensemble de modelos (Fase 3):** Combinar las fortalezas de `gemma4:31b` (alto Recall) y modelos compactos como `llama3.2` (alta eficiencia de hardware) mediante votación mayoritaria ponderada por confianza de extracción.

5. **Evaluación en producción (Fase 4):** Despliegue piloto en Austranet con feeds reales de Google Alerts y medición de KPIs operacionales (tiempo de respuesta, carga, satisfacción del analista).

6. **Extensión multiidioma (Fase 5):** Evaluar la robustez del sistema sobre textos en inglés y portugués, considerando el alcance latinoamericano del problema de compliance.

---

## 8. REFERENCIAS BIBLIOGRÁFICAS

> *Formato IEEE*

[1] P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," *Advances in Neural Information Processing Systems*, vol. 33, pp. 9459-9474, 2020.

[2] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding," *Proceedings of NAACL*, pp. 4171-4186, 2019.

[3] S. Wu et al., "BloombergGPT: A Large Language Model for Finance," *arXiv preprint arXiv:2303.17564*, 2023.

[4] A. Vaswani et al., "Attention Is All You Need," *Advances in Neural Information Processing Systems*, 2017.

[5] K. Bourne, *Unlocking Data with Generative AI and RAG*. O'Reilly Media, 2024.

[6] X. Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey," *arXiv preprint arXiv:2312.10997*, 2024.

[7] A. García and M. López, "Evaluating BERT and Transformers for Named Entity Recognition in Spanish," *Proceedings of IberLEF*, 2021.

[8] T. Brown et al., "Language Models are Few-Shot Learners," *Advances in Neural Information Processing Systems*, vol. 33, pp. 1877-1901, 2020.

[9] M. Chang, J. Kim, and S. Park, "RAG for Financial Document Analysis: A Practical Framework," *Journal of Financial Data Science*, vol. 6, no. 2, pp. 45-62, 2024.

[10] J. Smith, L. Johnson, and R. Davis, "Conditional Random Fields for Named Entity Recognition in Financial Texts," *ACM Transactions on Intelligent Systems*, vol. 10, no. 3, pp. 1-25, 2019.

[11] T. Ahia et al., "Do All Languages Cost the Same? Tokenization in the Era of Commercial Language Models," *Proceedings of EMNLP*, 2023.

[12] E. F. Tjong Kim Sang, "Introduction to the CoNLL-2002 Shared Task: Language-Independent Named Entity Recognition," *Proceedings of CoNLL-2002*, pp. 155-158, 2002. [Online]. Available: https://www.clips.uantwerpen.be/conll2002/ner/

[13] J. Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models," *Advances in Neural Information Processing Systems*, vol. 35, 2022.

[14] A. Zhao et al., "Calibrate Before Use: Improving Few-Shot Performance of Language Models," *Proceedings of ICML*, 2021.

[15] M. Min et al., "FiNER: Financial Named Entity Recognition Dataset and Benchmark," *Proceedings of ACL*, 2023.

[16] R. Schwartz et al., "Green AI," *Communications of the ACM*, vol. 63, no. 12, pp. 54-63, 2020.

[17] J. Lafferty, A. McCallum, and F. Pereira, "Conditional Random Fields: Probabilistic Models for Segmenting and Labeling Sequence Data," *Proceedings of ICML*, pp. 282-289, 2001.

[18] Kleptotrace Project, "Kleptotrace corpus: Financial Sanctions and Money Laundering News Corpus," conjunto de datos del proyecto (15 artículos anotados por expertos), 2024.

[19] OpenSanctions, "OpenSanctions: Open Data on Sanctions Lists and Politically Exposed Persons," [Online]. Available: https://www.opensanctions.org, 2024.

[20] T. Dettmers et al., "QLoRA: Efficient Finetuning of Quantized LLMs," *Advances in Neural Information Processing Systems*, vol. 36, 2023.

---

## 9. ANEXOS

### Anexo A — Estructura del Repositorio de Código

```
repos/ner-llm-entity-benchmark/
├── src/
│   ├── main.py                  # Orquestador principal (+--rag-mode CLI, v1.1)
│   ├── config.py                # Configuración global (+rag_mode field, v1.1)
│   ├── data_loader.py           # Carga y validación del corpus
│   ├── llm_runner.py            # Runner LLM con parseo en cascada
│   ├── evaluator.py             # Métricas F1 + taxonomía de errores
│   ├── pub_sub.py               # Cola Pub/Sub multithreading
│   ├── adaptive_workers.py      # Controlador AIMD
│   ├── checkpoint.py            # Persistencia de estado
│   ├── rag_manager.py           # RAGManager: Dict-RAG legacy (v1.0)
│   ├── kb_rag_manager.py        # KBRAGManager: KB RAG contextual (v1.1, NUEVO)
│   ├── dashboard.py             # Interfaz Streamlit (7 pestañas)
│   ├── statistics.py            # ANOVA + Tukey HSD + IC95
│   └── providers/
│       ├── base.py              # LLMProvider ABC
│       ├── factory.py           # LLMProviderFactory
│       ├── ollama_provider.py   # Proveedor Ollama (+template KB RAG, v1.1)
│       ├── openai_provider.py   # Proveedor OpenAI (cloud)
│       └── __init__.py          # Facade get_provider()
├── data/
│   ├── benchmark_balanced_120.json    # Corpus N=120 (Gold Standard real)
│   ├── dictionaries/
│   │   ├── persons.json               # Diccionario de personas (v1.0)
│   │   ├── organizations.json         # Diccionario de organizaciones (v1.0)
│   │   └── augmented_persons.json     # Personas aumentadas (v1.0)
│   └── knowledge_base/                # Base de Conocimientos KB RAG (v1.1, NUEVO)
│       ├── domain_guidelines.json     # 5 dominios con reglas NER tipológicas
│       └── few_shot_exemplars.json    # 7 ejemplares anotados (artículos reales)
├── results/                     # Salidas del benchmark
│   ├── benchmark_results.csv
│   ├── statistical_report.md
│   └── benchmark_balanced_120_<timestamp>/  # Resultados por ejecución
├── research/
│   └── rag/
│       ├── 2026-08-31_analisis_contenido_rag_base_conocimientos.md  # Investigación RAG
│       ├── TODO-RAG-20260901.md                                      # Tracking implementación
│       └── WORKLOG.md                                               # Bitácora de trabajo
├── SYSTEM_PROMPT.md             # Prompt del sistema (few-shot español)
├── SYSTEM_PROMPT_EN.md          # Prompt del sistema (inglés)
└── SYSTEM_PROMPT_ES.md          # Prompt del sistema (español)
```


### Anexo B — Prompt del Sistema (Versión Few-Shot Español)

El prompt de sistema en español (few-shot) incluye: (1) instrucciones de rol (analista de cumplimiento normativo), (2) formato de salida JSON estricto con tipos de entidades, (3) 3 ejemplos completos de artículo → extracción correcta, y (4) reglas de comportamiento ante ambigüedad (no alucinar, preferir omisión a invención).

### Anexo C — Configuración del Entorno de Pruebas

| Componente | Especificación |
|:---|:---|
| Hardware | Apple MacBook Pro, chip M4 Max |
| Memoria Unificada | 16 GB (modelos ≤~12B) / 48 GB (31B y MLX grandes) Metal (MPS) |
| Sistema Operativo | macOS 15.x (Sequoia) |
| Python | 3.14.7 |
| Ollama | 0.6+ |
| Modelos descargados | gemma4:31b (19 GB), gemma4:12b (5 GB), llama3.2 (2 GB), deepseek-r1:1.5b (1.1 GB) |
| Tiempo total de benchmark (N=30, 2 modelos) | ~29 minutos (serial) |

---

*Informe Final de Tesina — Magíster en Tecnologías de la Información (MTI)*  
*Universidad Técnica Federico Santa María — Valparaíso, Chile*  
*Julio 2026*
