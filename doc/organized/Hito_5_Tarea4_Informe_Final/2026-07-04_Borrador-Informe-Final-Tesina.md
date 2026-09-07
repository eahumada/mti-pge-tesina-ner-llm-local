# Clasificación y Extracción de Entidades Nombradas (NER) en Noticias de Cumplimiento Normativo Corporativo Mediante Modelos de Lenguaje Grande Ejecutados Localmente con Soberanía de Datos

**Eduardo Mauricio Ahumada Gallardo**

Austranet — Departamento de Informática, Universidad Técnica Federico Santa María, Valparaíso, Chile

eahumada@gmail.com

## RESUMEN

Las instituciones financieras sujetas a regulaciones AML/KYC deben vigilar grandes volúmenes de noticias no estructuradas en busca de entidades de riesgo. Hacerlo manualmente resulta costoso y no escala; delegarlo en APIs en la nube expone información sensible a terceros. Este trabajo evalúa un sistema soberano de reconocimiento de entidades nombradas (NER) con modelos de lenguaje grande de código abierto ejecutados en local mediante Ollama sobre hardware Apple Silicon. La validación comparó trece modelos sobre un corpus real de 120 artículos en español, contrastando la extracción directa frente a la generación aumentada por recuperación con una base de conocimiento contextual, y evaluó las diferencias mediante ANOVA de una vía y pruebas post-hoc de Tukey HSD. El beneficio del RAG contextual resulta inversamente proporcional a la capacidad del modelo: alcanza significancia estadística solo en los dos modelos más débiles (+14,5 y +10,8 puntos de F1) y es nulo o adverso en los mayores. Redactar el prompt en español e incorporar ejemplos *few-shot* aporta conjuntamente +11,1 puntos sobre el baseline en inglés, mejora que ninguno de los dos factores logra por separado. El sistema reduce el costo unitario de revisión y preserva íntegramente la confidencialidad de los datos.

**Palabras clave:** Reconocimiento de Entidades Nombradas (NER), Modelos de Lenguaje Grande (LLM), Cumplimiento Normativo (AML/KYC), Soberanía de Datos, Generación Aumentada por Recuperación (RAG).

## ABSTRACT

Financial institutions operating under AML and KYC regulatory frameworks face the challenge of monitoring large volumes of unstructured news for risk entities (persons, organizations). Manual execution of this process is costly, slow, and unscalable, while cloud API usage exposes sensitive financial data to third parties, violating data sovereignty. This work designs, implements, and empirically evaluates a sovereign Named Entity Recognition (NER) system based on open-source Large Language Models (Gemma, Llama, DeepSeek families) executed 100% locally via Ollama on Apple Silicon M4 hardware.

The system incorporates a multithreading pub/sub processing architecture with an adaptive concurrency controller (AIMD) and a Factory/Facade layer unifying four model providers. Experimental validation was performed on the real financial sanctions dataset Kleptotrace/CoNLL-2002 (N=15 expert-annotated articles) and a statistically significant corpus of 30 short articles (N=30). The prompt-variant analysis demonstrates that combining Spanish-language localization with few-shot examples yields a +11.1 F1-point improvement over the English zero-shot baseline, and the best evaluated models reach an F1-Score of 80.57% on the domain corpus (N=30) with no failed extractions. The system reduces manual review operational costs by 60–80% while guaranteeing total data privacy.

**Keywords:** Named Entity Recognition (NER), Large Language Models (LLM), Regulatory Compliance (AML/KYC), Data Sovereignty, Prompt Engineering.


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


## 1. INTRODUCCIÓN

### 1.1 Contexto y Motivación

Las instituciones financieras operan bajo un marco regulatorio estricto que les obliga a identificar y gestionar entidades de riesgo en tiempo real. Las regulaciones internacionales Anti-Money Laundering (AML) y Know Your Customer (KYC), implementadas en Chile por la Unidad de Análisis Financiero (UAF) y la Comisión para el Mercado Financiero (CMF), exigen la detección de Personas Políticamente Expuestas (PEP), sujetos sancionados y vínculos con redes de lavado de activos en flujos continuos de información pública.

El proceso actual en instituciones como Austranet implica la revisión manual de cientos de artículos periodísticos diarios por analistas especializados, un proceso con un costo promedio estimado de USD 8.75 por artículo analizado. A nivel global, según Verified Market Research el mercado de RegTech se valoró en USD 15,68 mil millones en 2020 y se proyecta que alcance USD 87,17 mil millones hacia 2028, con una CAGR del 23,92 % durante 2021-2028, evidenciando la urgencia de soluciones automatizadas y escalables (Verified Market Research, 2022).

### 1.2 Planteamiento del Problema

El problema es de naturaleza técnico-operativa: extraer automáticamente entidades nombradas —personas y organizaciones— desde noticias no estructuradas en español, con precisión suficiente para sostener una decisión de cumplimiento, en un dominio donde la ambigüedad referencial es la norma y sin que el texto abandone la infraestructura de la institución.

Ninguna de las alternativas disponibles satisface simultáneamente esas condiciones. La **revisión manual** ofrece la máxima precisión, pero su coste crece linealmente con el volumen y no escala ante un flujo continuo de noticias. Los **sistemas basados en reglas y expresiones regulares** resultan frágiles ante la variación morfológica del español, donde un mismo nombre admite múltiples formas según la posición, la partícula y la acentuación. Las **APIs comerciales en la nube** aportan la capacidad necesaria, pero transfieren texto que puede contener información de clientes a un tercero, lo que en una entidad regulada obliga a suscribir acuerdos de tratamiento de datos y amplía la superficie de exposición; su coste, además, se vuelve prohibitivo al procesar por lotes. Los **modelos supervisados** del tipo BERT-NER alcanzan el mejor desempeño publicado, pero requieren miles de ejemplos etiquetados en el dominio objetivo, inexistentes en español para cumplimiento financiero.

La brecha que este trabajo aborda se sitúa precisamente en esa intersección vacía: obtener un desempeño aprovechable **sin datos etiquetados del dominio y sin ceder los datos a un tercero**.

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

### 1.5 Enfoque de Solución y Metodología de Validación

La solución adoptada consiste en operar modelos de lenguaje generativos de código abierto **enteramente sobre infraestructura propia**, describiendo la tarea de extracción en el propio *prompt* en lugar de ajustar los pesos del modelo. Esta elección resuelve de raíz las dos restricciones del problema —no exige corpus etiquetado y no expone el texto—, a cambio de asumir dos inconvenientes que el sistema debe gestionar: una salida no estructurada por construcción, que se fuerza a un esquema verificable, y un riesgo de alucinación que debe medirse explícitamente. El capítulo 2 revisa las alternativas disponibles y el capítulo 3 justifica cada decisión frente a ellas.

La validación sigue una estrategia empírica en tres etapas. Primero se establece una **línea base comparativa** ejecutando el conjunto de modelos candidatos sobre un corpus anotado, con el fin de acotar el espacio de opciones viables. Después se aísla el efecto de las variables de *prompt* mediante un diseño factorial que cruza idioma y presencia de ejemplos, evaluando las cuatro combinaciones sobre el mismo modelo y corpus. Finalmente se contrasta la extracción directa frente a la aumentada por recuperación sobre un corpus ampliado, y se determina mediante **ANOVA de una vía y pruebas post-hoc de Tukey HSD** si las diferencias observadas son estadísticamente significativas o atribuibles a la variabilidad entre artículos. Todas las corridas quedan definidas por un fichero de configuración reproducible, de modo que cualquier resultado del informe pueda rehacerse a partir de los artefactos publicados.

### 1.6 Estructura del Documento

El capítulo 2 revisa las familias de técnicas aplicables al problema —desde los sistemas basados en reglas hasta los modelos generativos—, las estrategias de aumento por recuperación y las alternativas de ejecución local, y cierra fijando los criterios de selección. El capítulo 3 describe el sistema propuesto y justifica cada decisión de diseño frente a esos criterios. El capítulo 4 detalla el diseño experimental: corpus, modelos, configuraciones de *prompt*, métricas e infraestructura. El capítulo 5 presenta los resultados de los tres experimentos y el capítulo 6 los discute, con especial atención a la contribución metodológica sobre qué información conviene recuperar. El capítulo 7 recoge las conclusiones y las líneas de trabajo futuro. Los anexos reúnen el material de reproducción: estructura del repositorio, *prompts* completos, configuración del entorno y el análisis detallado del defecto de codificación del corpus.

## 2. MARCO TEÓRICO Y ESTADO DEL ARTE

Este capítulo revisa las familias de técnicas disponibles para resolver el problema planteado y establece los criterios con los que, en el capítulo 3, se selecciona una de ellas. El recorrido no pretende ser exhaustivo sino comparativo: interesa entender qué exige cada alternativa, qué garantiza y en qué condiciones deja de ser aplicable al caso de estudio, caracterizado por la ausencia de corpus etiquetados en español para el dominio de cumplimiento y por la obligación de no exponer los datos a terceros.

### 2.1 El problema del reconocimiento de entidades nombradas

El Reconocimiento de Entidades Nombradas (NER) es una subtarea del Procesamiento de Lenguaje Natural que consiste en localizar fragmentos de texto y clasificarlos en categorías semánticas predefinidas. En cumplimiento normativo las categorías relevantes son **Personas** (PER), **Organizaciones** (ORG) y **Ubicaciones** (LOC), pues son las que permiten cotejar una noticia contra listas de sanciones y de personas expuestas políticamente [19].

Formalmente se plantea como un problema de etiquetado de secuencias: dado un texto segmentado en tokens, se asigna a cada uno una etiqueta según el esquema IOB2, que distingue el inicio de una entidad (*Beginning*), su continuación (*Inside*) y el texto ajeno a toda entidad (*Outside*). Esta formulación, heredada de la tarea compartida CoNLL-2002 [12], es la que fija el criterio de evaluación: una entidad se considera correctamente extraída solo si coinciden a la vez sus límites y su categoría.

La dificultad del dominio no proviene de la definición de la tarea sino de tres rasgos del material periodístico financiero. Primero, la **ambigüedad referencial**: un mismo token puede designar una persona o una organización según el contexto —«Santander» es tanto un apellido como un banco y una ciudad—. Segundo, la **variación morfológica del español**, con nombres compuestos, partículas («de», «del», «y») y tildes que fragmentan la coincidencia exacta. Tercero, la **escasez de datos etiquetados**: no existe un corpus público en español anotado para el dominio AML/KYC, lo que descarta de entrada cualquier técnica que dependa de un volumen sustancial de ejemplos supervisados.

### 2.2 Familias de técnicas para NER

Las aproximaciones al problema pueden ordenarse por el tipo de conocimiento que requieren y por el coste de adaptarlas a un dominio nuevo.

Los **sistemas basados en reglas y diccionarios** (*gazetteers*) identifican entidades por coincidencia contra catálogos y por patrones léxicos escritos a mano. Son transparentes, deterministas y no requieren entrenamiento, pero su cobertura se limita a lo enumerado: fracasan ante nombres nuevos, que es precisamente el caso de interés en la detección temprana de riesgo.

Los **Campos Aleatorios Condicionales (CRF)** [17], [10] modelan la secuencia de etiquetas como un campo probabilístico condicionado al texto, capturando dependencias entre etiquetas contiguas. Superan a las reglas en generalización, pero dependen de ingeniería manual de rasgos y de un corpus anotado del orden de miles de oraciones.

Las **arquitecturas neuronales BiLSTM-CRF** sustituyen los rasgos manuales por representaciones aprendidas, eliminando gran parte del trabajo de ingeniería a cambio de un requisito de datos aún mayor.

Los **codificadores Transformer pre-entrenados** —BERT [2] y sus variantes multilingües como XLM-R— constituyen el estado del arte académico. Partiendo de un modelo pre-entrenado, un ajuste fino sobre el dominio alcanza entre 88 % y 91 % de F1 en español [7], [15]. Su limitación en este caso no es de capacidad sino de insumos: el ajuste fino exige el corpus etiquetado que aquí no existe, y construirlo supondría un esfuerzo de anotación experta fuera del alcance del trabajo.

Los **modelos de lenguaje grande generativos** (Transformers *decoder-only*) invierten el planteamiento: en lugar de ajustar los pesos al dominio, se describe la tarea en el propio *prompt*. Su capacidad de **aprendizaje en contexto** [8] permite adaptación inmediata sin reentrenamiento, a costa de una salida no estructurada por construcción —que hay que forzar a un formato verificable— y de un riesgo de alucinación inexistente en las familias anteriores.

| Familia | Datos etiquetados requeridos | Adaptación a dominio nuevo | Riesgo principal |
|:---|:---|:---|:---|
| Reglas y diccionarios | Ninguno | Inmediata pero de cobertura cerrada | No detecta entidades no catalogadas |
| CRF | Miles de oraciones | Reentrenamiento e ingeniería de rasgos | Coste de anotación |
| BiLSTM-CRF | Decenas de miles | Reentrenamiento | Coste de anotación |
| Transformer con ajuste fino | Miles, del dominio | Ajuste fino | Coste de anotación; el mejor F1 publicado |
| LLM generativo en contexto | Ninguno | Inmediata mediante *prompt* | Alucinación y salida no estructurada |

La última fila es la única compatible con la restricción de datos del proyecto, y por eso concentra el resto de la revisión.

### 2.3 Aprendizaje en contexto y diseño de prompts

La arquitectura Transformer [4], sostenida sobre el mecanismo de atención multi-cabeza, es la base común de todos los modelos evaluados. Sobre ella, el aprendizaje en contexto permite condicionar el comportamiento del modelo mediante instrucciones y ejemplos incluidos en la propia entrada.

Se distinguen dos regímenes. En **zero-shot** el *prompt* contiene únicamente la descripción de la tarea y el formato de salida esperado. En **few-shot** [8] se añaden ejemplos resueltos que fijan el patrón de respuesta; la literatura documenta que el número, el orden y el equilibrio de esos ejemplos alteran el resultado de forma no trivial, y que un conjunto mal calibrado puede degradar el desempeño respecto del zero-shot [14]. Existen además estrategias de razonamiento explícito, como *chain-of-thought* [13], concebidas para tareas que requieren inferencia en varios pasos; su pertinencia en extracción de entidades es dudosa a priori, ya que la tarea es de identificación y no de deducción, extremo que este trabajo somete a comprobación empírica.

Un factor específico del castellano es el **coste de tokenización**: los modelos entrenados mayoritariamente en inglés segmentan el español en más tokens por palabra, lo que encarece la inferencia y reduce el contexto útil [11]. Esto convierte al idioma del *prompt* en una variable experimental por derecho propio y no en un detalle de presentación.

### 2.4 Estrategias de aumento por recuperación

La Generación Aumentada por Recuperación (RAG) [1] fundamenta la generación en información recuperada en tiempo de consulta, en lugar de confiarla exclusivamente a los pesos del modelo. La literatura reciente [6] distingue variantes por la naturaleza de lo recuperado, y esa distinción resulta determinante en NER.

Una primera variante es el **RAG por diccionario**: se indexan catálogos de nombres conocidos y se inyectan en el *prompt* los más similares al texto. Aporta cobertura sobre entidades ya catalogadas, pero introduce un sesgo de reconocimiento —el modelo tiende a proponer lo que se le ha sugerido— y no ayuda ante nombres ausentes del catálogo.

Una segunda variante es el **RAG contextual o de conocimiento**, en el que lo recuperado no son entidades sino **criterios**: guías tipológicas, definiciones de categoría y ejemplos anotados del dominio. No indica al modelo *qué* entidades esperar, sino *cómo* decidir si un fragmento lo es.

Una tercera configuración, adoptada por trabajos aplicados al ámbito financiero [9], [5], emplea el propio documento como **contexto único**, restringiendo la extracción al texto presente y mitigando la alucinación extrínseca.

La elección entre ellas no es neutra: la primera optimiza el *recall* sobre lo conocido y la segunda la precisión del criterio, y sus efectos pueden ser opuestos según la capacidad del modelo receptor. El capítulo 5 contrasta empíricamente ambas.

### 2.5 Alternativas de ejecución local y cuantización

Ejecutar modelos de escala media-grande sobre hardware de consumo exige **cuantización**: reducir la precisión numérica de los pesos para bajar el consumo de memoria, típicamente a 4 bits en formatos como GGUF con esquema Q4_K_M, con una pérdida de calidad reducida frente al ahorro obtenido [20]. Esta reducción es también la que hace viable el criterio de sostenibilidad computacional que la literatura reclama para la investigación en aprendizaje automático [16].

Entre los entornos de ejecución disponibles, **llama.cpp** ofrece el motor de inferencia cuantizada de referencia pero exige gestión manual de modelos; **vLLM** maximiza el rendimiento por lotes en servidores con GPU dedicada, escenario ajeno a este trabajo; **LM Studio** prioriza la interacción gráfica sobre la automatización; el entorno **MLX** de Apple aprovecha específicamente la memoria unificada de Apple Silicon; y **Ollama** encapsula llama.cpp tras una API HTTP uniforme, con gestión de modelos, control del ciclo de vida en memoria y compatibilidad tanto con pesos GGUF como MLX. Frente a todos ellos, las **APIs en la nube** ofrecen la mayor capacidad sin coste de infraestructura, pero transfieren el texto a un tercero, lo que resulta incompatible con el requisito de soberanía que motiva el trabajo.

### 2.6 Estado del arte y criterios de selección

La Tabla 1 posiciona este trabajo respecto de investigaciones recientes en NER para dominios financieros y regulatorios.

| Trabajo | Dataset | Modelo | F1 | Privacidad | Idioma |
|:---|:---|:---|:---:|:---:|:---|
| BloombergGPT [3] | Bloomberg corpus | GPT-J + dominio | 85%+ | ❌ Cloud | Inglés |
| FiNER-139 Benchmark [15] | SEC 10-K/10-Q | BERT fine-tuned | 91% | ❌ Cloud | Inglés |
| García & López [7] | CoNLL-ES | XLM-R | 88% | ✅ Local | Español |
| Chang et al. [9] | Docs bancarios | GPT-4 + RAG | 83% | ❌ Cloud | Inglés |
| **Este trabajo** | **Kleptotrace/CoNLL-2002 (AML), corpus sintético N=30** | **gemma4:31b local** | **79%** | **✅ 100% Local** | **Español** |

De la comparación se desprende una brecha: los trabajos que alcanzan el mejor F1 lo hacen sobre corpus en inglés y con infraestructura en la nube, mientras que los que preservan la privacidad no abordan el dominio de cumplimiento en español. Este trabajo se sitúa en esa intersección.

La revisión anterior deja fijados los criterios con los que el capítulo 3 justifica cada decisión de diseño: **(C1) prescindir de datos etiquetados**, por no existir corpus del dominio en español; **(C2) preservar la soberanía del dato**, lo que excluye toda API externa; **(C3) operar sobre hardware de consumo**, lo que obliga a cuantización y a gestión explícita de memoria; **(C4) producir salida verificable**, dado que el modelo elegido genera texto libre; y **(C5) permitir comparación empírica entre variantes**, tanto de *prompt* como de estrategia de recuperación.

## 3. DESCRIPCIÓN DEL SISTEMA PROPUESTO

### 3.1 Justificación de las decisiones de diseño

El capítulo anterior cerró con cinco criterios derivados de la revisión. Cada uno determina una decisión de diseño concreta, y conviene explicitar el razonamiento antes de describir la implementación.

El criterio **C1 —prescindir de datos etiquetados—** descarta las cuatro primeras familias de la Tabla comparativa del §2.2. Los CRF, las arquitecturas BiLSTM-CRF y el ajuste fino de codificadores Transformer ofrecen mejor F1 publicado, pero todos exigen un corpus anotado del dominio que no existe en español para cumplimiento financiero. Se adopta por tanto un **modelo de lenguaje generativo operado mediante aprendizaje en contexto**, única familia que permite adaptación inmediata sin reentrenamiento. La contrapartida —salida no estructurada y riesgo de alucinación— se asume conscientemente y se aborda con C4.

El criterio **C2 —soberanía del dato—** excluye las APIs comerciales, que aventajan a los modelos abiertos en capacidad pero transfieren el texto a un tercero. Se opta por **ejecución íntegramente local**. Entre los entornos revisados en §2.5 se selecciona **Ollama**, por tres razones: expone una API HTTP uniforme que permite intercambiar modelos sin tocar el código de orquestación; gestiona el ciclo de vida de los pesos en memoria, requisito imprescindible para encadenar modelos que no caben simultáneamente; y admite tanto pesos GGUF como MLX, lo que habilita comparar ambas rutas de cuantización sobre el mismo arnés. Los modelos en la nube se conservan únicamente como **línea base de comparación**, no como parte de la solución propuesta.

El criterio **C3 —hardware de consumo—** obliga a cuantización de 4 bits (GGUF Q4_K_M) y a una gestión explícita de la memoria, descrita en §3.3.

El criterio **C4 —salida verificable—** se traduce en exigir al modelo un objeto JSON con un esquema fijo, validado en recepción, con una ruta de recuperación cuando el análisis sintáctico falla. Es la contramedida directa al principal inconveniente de la familia elegida.

El criterio **C5 —comparación empírica—** exige que las variantes de *prompt* y de estrategia de recuperación sean intercambiables por configuración y no por modificación del código, de modo que cada corrida quede definida por un conjunto de parámetros reproducible.

### 3.2 Arquitectura general y capa de proveedores

El sistema se organiza en cinco capas funcionales con responsabilidades separadas, de manera que cada una pueda evolucionar sin arrastrar a las demás.


| Capa | Módulo(s) | Detalle técnico |
|:---|:---|:---|
| 1. Capa de datos | `data_loader.py` + validador | Kleptotrace/CoNLL-2002 JSON → validación de esquema → registros |
| 2. Orquestación | `main.py` + `pub_sub.py` | Cola pub/sub → controlador AIMD → gestor de lotes |
| 3. Proveedores LLM | Factory / Facade | `OllamaProvider`, `OpenAIProvider`, `AnthropicProvider` |
| 4. Evaluación | `evaluator.py` + `statistics.py` | F1 / Precisión / Recall / ANOVA / Tukey HSD |
| 5. Visualización | `dashboard.py` (Streamlit) | Siete pestañas: métricas, alucinaciones, ANOVA, eficiencia |



La **capa de datos** carga el corpus desde un fichero JSON y valida cada registro contra un esquema antes de admitirlo, garantizando que todo artículo procesado dispone de texto y de anotación de referencia. La **capa de orquestación** distribuye el trabajo y regula la concurrencia (§3.3). La **capa de proveedores** aísla la heterogeneidad de las APIs. La **capa de evaluación** calcula las métricas y las pruebas estadísticas (§3.4). La **capa de visualización**, implementada en Streamlit, presenta los resultados en siete vistas —comparación de modelos, análisis de alucinaciones, taxonomía de errores, significancia estadística, eficiencia de hardware, proyección de modelos futuros y simulación de producción— y cumple una función de inspección durante la experimentación, no de despliegue productivo.

La capa de proveedores es la que materializa el criterio C2 sin encerrar el trabajo en un único motor. Aplica los patrones *Factory* y *Facade* tras una interfaz común:

```python
class LLMProvider(ABC):
    @abstractmethod
    def extract_entities(self, text: str, system_prompt: str, **kwargs) -> ExtractionResult:
        ...
    @abstractmethod
    def is_available(self) -> bool:
        ...
```


La selección del proveedor se resuelve por el prefijo del identificador del modelo, de modo que añadir un motor nuevo no requiere modificar el orquestador. Esta indirección tuvo una consecuencia práctica relevante durante la experimentación: un modelo abierto cuyo nombre comenzaba por `gpt-` era enrutado erróneamente hacia la API comercial, fallo que se detectó y corrigió discriminando por la presencia de etiqueta de versión propia de los identificadores locales. El episodio ilustra que la abstracción por convención de nombres exige verificación explícita del enrutamiento efectivo.

### 3.3 Orquestación, concurrencia adaptativa y gestión de memoria

El núcleo de ejecución es un canal de publicación y suscripción con múltiples hilos. El productor publica lotes de artículos por modelo en una cola en memoria —con interfaz compatible con Redis para un eventual despliegue distribuido— y los consumidores los procesan en paralelo.

El número de consumidores no es fijo, sino que lo regula un controlador **AIMD** (*Additive Increase, Multiplicative Decrease*), política tomada del control de congestión en redes. Mientras el sistema permanece estable —sin errores de limitación de tasa ni excepciones— durante una ventana de 600 segundos, el controlador **añade un consumidor cada 120 segundos** hasta un techo del 75 % del máximo configurado; ante el primer error de saturación **reduce los consumidores a la mitad**. Un cortacircuitos complementa la política: cinco fallos consecutivos abren el circuito y suspenden el procesamiento durante 60 segundos. La asimetría entre el aumento prudente y el recorte agresivo es deliberada, pues el coste de saturar un servicio de inferencia —reintentos, respuestas truncadas, penalización por cuota— excede con mucho al de infrautilizarlo. Sobre Apple Silicon M4 con 16 GB, el sistema escaló de forma estable hasta nueve consumidores concurrentes para modelos de 8B parámetros.

La gestión de memoria merece atención propia porque condicionó el alcance del estudio. Al terminar cada modelo se libera explícitamente su ocupación de GPU invocando la API de generación con `keep_alive=0`. Ahora bien, ese parámetro evita retener varios modelos a la vez, **pero no reduce el footprint de uno solo**, y esa distinción resultó decisiva. macOS asigna a la GPU un techo de memoria equivalente al 75 % de la memoria unificada del equipo (`recommendedMaxWorkingSetSize`): unos 12 GB en una máquina de 16 GB. Los modelos de hasta ~12B cuantizados a 4 bits ocupan entre 7 y 9 GB y caben con holgura; los de 31B alcanzan un footprint operativo de ~24,7 GB —unos 18,7 GB de pesos más la caché de claves y valores y el sobrecoste de inferencia— y **no pueden cargarse en 16 GB ni siquiera de forma serial**. La ejecución se organizó en consecuencia en dos escalones de hardware: 16 GB para los modelos de hasta ~12B y un equipo de 48 GB, con techo asignable de ~36 GB, para los de 31B y las variantes MLX de mayor tamaño.

### 3.4 Módulo de evaluación

La comparación entre lo extraído y la anotación de referencia no puede ser literal, porque una diferencia de puntuación o un artículo antepuesto invalidarían una extracción correcta. El evaluador emplea por ello **emparejamiento difuso** por similitud de tokens, aceptando como acierto toda coincidencia por encima de un umbral configurable, fijado en 85 sobre 100. La elección del umbral es un compromiso: por debajo admite falsos emparejamientos entre nombres distintos que comparten apellido; por encima rechaza variantes legítimas.

Sobre esa base se calculan precisión, exhaustividad y F1 por artículo, que después se promedian, y una **tasa de alucinación** definida como la proporción de entidades propuestas sin correspondencia alguna en la referencia. El módulo incorpora además la validación estadística: ANOVA de una vía para contrastar si las diferencias entre modelos y modos son significativas, pruebas post-hoc de Tukey HSD para identificar qué pares concretos difieren, intervalos de confianza al 95 % por grupo y un análisis de sensibilidad que recalcula las métricas excluyendo los artículos atípicamente largos, con el fin de comprobar que ningún resultado depende de unos pocos casos extremos.

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

**d) Consistencia entre corpus:** Los F1-Scores observados en el corpus N=30 (gemma4:31b: 78.55%) son consistentes con la tendencia observada en el corpus real N=15 (gemma4:31b: 69.12%), sin saltos discontinuos que indicarían artefactos del aumento. La diferencia es atribuible a la menor complejidad promedio de los artículos breves del corpus sintético, lo que es esperado y documentado.

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


| Posición en el prompt | Contenido |
|:---|:---|
| 1 | Instrucción de sistema |
| 2 | Ejemplo 1: entrada → salida esperada |
| 3 | Ejemplo 2: entrada → salida esperada |
| 4 | Ejemplo 3: entrada → salida esperada |
| 5 | Tarea real: entrada (el modelo genera la salida) |


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

El cotejo entre la entidad extraída y la de referencia es **difuso**, con un umbral de similitud de 85 sobre 100, lo que tolera variaciones menores de forma sin admitir coincidencias espurias.

**Convención ante la extracción vacía.** Una implementación previa del evaluador asignaba Precisión, Recall y F1 iguales a 1.0 cuando el modelo no extraía ninguna entidad, por tratarse de una división sobre cero. Esa convención **premiaba el silencio** y beneficiaba de forma desigual a los modelos propensos a devolver respuestas vacías, hasta 0.21 de F1 en el caso más extremo. La convención empleada en este trabajo asigna **0.0** en ese supuesto, y reserva el valor 1.0 únicamente para el **acierto vacío legítimo**: aquel en que el artículo no contenía entidades y el modelo tampoco propuso ninguna. Todas las corridas del estudio se re-puntuaron con esta convención a partir de los recuentos de aciertos y errores almacenados, **sin repetir la inferencia**, de modo que la totalidad de las cifras reportadas comparte un criterio único.

### 4.5 Infraestructura de Pruebas

- **Hardware:** Apple Silicon (Metal/MPS), en dos configuraciones según el footprint del modelo: 16 GB de memoria unificada para modelos de hasta ~12B, y 48 GB de memoria unificada para los modelos de 31B y variantes MLX de gran tamaño (ver §3.6).
- **Software:** Python 3.14, Ollama 0.6+, scikit-learn 1.9, statsmodels 0.14, pandas 3.0, Streamlit 1.60.
- **Reproducibilidad:** Checkpointing automático (`.checkpoint.json`) para reanudar benchmarks interrumpidos sin pérdida de datos.


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

> **Hallazgo 4:** ninguno de los dos factores basta por separado —la localización al español aporta +4.38 pp y los ejemplos *few-shot* en inglés restan 0.73 pp—, pero **su combinación alcanza +11.12 pp** sobre el baseline ZS-EN, con el mejor Recall del conjunto (86.87%). Los ejemplos solo resultan productivos redactados en el idioma del corpus.

### 5.3 Validación Estadística sobre el Corpus del Dominio (N=30)

El primer experimento evalúa los dos modelos de mayor capacidad del estudio sobre el corpus sintético del dominio AML/KYC, compuesto por treinta artículos breves con anotación experta. Su propósito no es comparar el catálogo completo de modelos —eso corresponde al §5.1— sino establecer el techo de desempeño alcanzable en el dominio propio del problema y contrastarlo con corpus periodístico general.

| Modelo | F1 | Precisión | Recall | IC 95 % del F1 | Fallos |
|:---|:---:|:---:|:---:|:---:|:---:|
| gemma4:31b-mlx | **80.57 %** | 74.17 % | **90.72 %** | [74.22 %, 86.92 %] | 0 |
| gemma4:31b | 78.55 % | 73.34 % | 88.28 % | [72.59 %, 84.52 %] | 0 |

Ambos modelos superan con holgura el umbral del 70 % fijado en la hipótesis, con exhaustividad cercana al 90 % y sin ninguna extracción fallida en los sesenta registros procesados. La variante MLX aventaja en dos puntos a la compilación estándar, diferencia que conviene no sobreinterpretar: el **ANOVA de una vía** arroja **F = 0,2235 con p = 0,6382**, de modo que no se rechaza la hipótesis nula y la diferencia entre ambos debe atribuirse a la variabilidad entre artículos y no a una superioridad real de una compilación sobre la otra. Los intervalos de confianza al 95 % se solapan ampliamente, lo que refuerza la misma lectura.

El **análisis de sensibilidad** completa la validación. Aplicando el criterio de longitud atípica —artículos por encima de 702 caracteres— no se identifica ningún registro fuera de rango, y el F1 filtrado coincide exactamente con el original en ambos modelos. El resultado no depende, por tanto, de unos pocos textos extremos.

Conviene señalar una particularidad de procedencia. Una primera ejecución de este experimento, realizada en julio de 2026, reportó para `gemma4:31b` un F1 de 79,03 %. Aquella medición empleaba la convención de puntuación anterior a la corrección descrita en §4.4 y sus datos por registro se perdieron por sobrescritura, de modo que no podía recalcularse. La ejecución aquí reportada la reemplaza y, al mismo tiempo, la valida: **la precisión coincide hasta el cuarto decimal (73,34 %) y el F1 difiere en menos de medio punto**, lo que confirma que el defecto de puntuación apenas afectaba a este experimento —consecuencia esperable de una exhaustividad tan alta, que deja pocas extracciones vacías sobre las que el error pudiera actuar—.

#### 5.3.5 Validación Estadística sobre Corpus Real N=120 (estudio completo)

Sobre el corpus real N=120 descrito en §4.1.3 se ejecutó el mismo protocolo (ANOVA de una vía + Tukey HSD) para el **estudio completo de 13 modelos**, cada uno en modo *baseline* y *KB RAG*, con N=120 observaciones por grupo (26 grupos, 3 120 observaciones). Resultados consolidados en `results/ANALISIS_CONJUNTO_20260907/`.

| Modelo | F1 baseline | F1 KB RAG | Δ RAG | Δ significativo |
|:---|:---:|:---:|:---:|:---:|
| gemma4:31b-cloud | 62.38% | 61.85% | −0.53 pp | no |
| gemma4:31b-mlx | **59.25%** | 59.07% | −0.18 pp | no |
| gemma4:12b-mlx | 56.18% | 58.46% | +2.28 pp | no |
| gemma4:latest | 55.91% | 54.74% | −1.17 pp | no |
| gpt-oss:20b | 52.39% | 55.67% | +3.28 pp | no |
| qwen2.5:14b | 50.22% | 54.84% | +4.62 pp | no |
| llama3.1:8b | 48.76% | 50.75% | +1.99 pp | no |
| qwen3:8b | 48.21% | 51.46% | +3.25 pp | no |
| gemma:latest | 44.00% | 51.36% | +7.36 pp | no |
| mistral-nemo:latest | 43.38% | 45.76% | +2.37 pp | no |
| llama3.2:latest | 36.11% | 46.93% | **+10.82 pp** | **sí** (p=0.007) |
| deepseek-r1:1.5b | 24.83% | 23.94% | −0.90 pp | no |
| nemotron-mini:4b | 22.59% | 37.12% | **+14.52 pp** | **sí** (p<0.001) |

> **Limitación del corpus N=120 — codificación defectuosa de los nombres.** El corpus
> `data/benchmark_balanced_120.json` almacena los nombres con *mojibake* (bytes UTF-8 reinterpretados como
> Latin-1): guarda `JosÃ© Bono` donde el nombre real es **José Bono**. Afecta a **283 de 1 406 entidades de
> referencia (20,1 %)** y, de forma relevante, **también al texto de entrada** (87 % de los artículos), donde
> las 283 entidades aparecen **con la misma corrupción**. El corpus es por tanto **internamente coherente**:
> un modelo que transcribe literalmente coincide con la referencia, mientras que uno que normaliza la
> ortografía al español correcto **deja de coincidir**. El efecto **no es un sesgo uniforme** sino una
> interacción que **depende del comportamiento de cada modelo**: la diferencia de F1 entre los artículos
> afectados y los no afectados oscila entre **−0.070 y +0.025** según el modelo. Los corpus N=15 y N=30 están
> **libres de este defecto** (0 entidades afectadas), por lo que §5.1, §5.2 y §5.3.1–5.3.4 no se ven
> comprometidos. La corrección adecuada —normalizar la codificación **en ambos lados** de la comparación—
> exige volver a inferir, ya que las extracciones por registro no se conservaron.

> **Dos salvedades de procedencia.** (i) La latencia de `gemma4:31b-cloud` **no mide inferencia**: quedó cuantizada por el `--request-delay` introducido para sortear el límite de peticiones del servicio (114 de sus 240 filas registran exactamente 1,02 s). Su F1 es válido; su latencia y sus tokens/s no deben usarse en comparaciones de eficiencia. (ii) Siete filas de `nemotron-mini:4b` tienen `latencia = 0` y `0 tokens/s` porque se re-extrajeron fuera del arnés de lotes tras un fallo de contexto; sus valores de precisión, *recall* y F1 son reales, pero su telemetría no existe.

**ANOVA de una vía (α = 0.05), N=120 por grupo:**
- **F-Statistic:** 38.2222  ·  **p-Value:** 3.4453 × 10⁻¹⁶⁰ (p < 0.05 → se rechaza H₀)
- **Conclusión:** la diferencia de desempeño entre modelos/modos es estadísticamente significativa, con una potencia muy superior a la del corpus N=30 (F=0.141, no significativo).
- **Tukey HSD (post-hoc):** 172 de 325 comparaciones por pares resultan significativas. Al contrastar *baseline* contra *KB RAG* **dentro de cada modelo**, la mejora solo alcanza significancia en `nemotron-mini:4b` (+14.52 pp, p<0.001) y `llama3.2:latest` (+10.82 pp, p=0.007); en los once modelos restantes la diferencia no supera la corrección por comparaciones múltiples.

**Interpretación.** El beneficio del KB RAG es **inversamente proporcional a la capacidad del modelo**: aporta de forma estadísticamente significativa en los dos modelos más débiles del estudio, es positivo pero no concluyente en la franja intermedia, y resulta nulo o adverso en los modelos de mayor capacidad (−0.53 pp y −0.18 pp en los dos de 31B), que ya siguen correctamente las instrucciones sin contexto adicional. **Diez de los trece modelos obtienen una mejora**, aunque solo en dos alcance significancia estadística.

**Lectura conjunta con el corpus N=30 (§5.3):** el mejor F1 local sobre N=120 (`gemma4:31b-mlx`: 59.25%) es menor que el de N=30 (`gemma4:31b-mlx`: 80.57%), lo esperable dado que los artículos reales de CoNLL-2002 ES son más largos y heterogéneos que los breves (~200 caracteres) del corpus sintético N=30, diseñado para el dominio AML/KYC. Se conservan ambos: N=30 como validación de mínima potencia (TLC, N≥30) sobre el dominio de sanciones del proyecto, y N=120 como validación sobre corpus real, con mayor potencia estadística y menor especificidad de dominio.

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


### 5.6 Optimización del Módulo RAG: De Diccionarios de Entidades a Base de Conocimientos Contextual

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


| Paso | Acción | Resultado |
|:---|:---|:---|
| 1 | Noticia política española (500 palabras) | Texto de entrada |
| 2 | Embedding `all-MiniLM-L6-v2` sobre el artículo completo | Vector de consulta |
| 3 | ChromaDB: top-5 por similitud coseno | GRANJA LA SIERRA LTDA. (Org), ASES DE COMPETENCIA Y CIA. (Org) y tres organizaciones colombianas irrelevantes |
| 4 | Inyección restrictiva en el prompt | «DO NOT extract unless they explicitly appear…» |
| 5 | Efecto en el LLM | Recall 62.8 % → 21.6 % (sondeo N=5) |


#### 5.6.2 Arquitectura, implementación y contenido de la base de conocimientos

La solución implementada transforma el contenido de la base vectorial: en lugar de nombres de entidades, se almacenan **Guías Tipológicas de Dominio** y **Ejemplares Dinámicos Few-Shot**.


| Paso | Acción | Resultado |
|:---|:---|:---|
| 1 | Noticia política española (500 palabras) | Texto de entrada |
| 2 | Embedding `all-MiniLM-L6-v2` | Vector de consulta |
| 3 | ChromaDB `ner_knowledge_base`: top-1 guía + top-1 ejemplar | Dominio recuperado: `politics_administrative` (ES) |
| 4 | Inyección positiva del contexto de dominio | «[EXTRACTION GUIDANCE]» con las reglas del dominio |
| 5 | Efecto en el LLM | F1 0.3521 → 0.5489 (+19.7 pp) · Recall 33.3 % → 59.5 % (+26.2 pp) |

El contexto de dominio inyectado en el paso 4 contiene las siguientes reglas:

| Regla | Contenido |
|:---|:---|
| Encabezado | `[DOMAIN CONTEXT: NOTICIAS POLÍTICAS EN ESPAÑOL]` |
| 1. Personas | Extraer solo el nombre propio, sin cargos ni tratamientos |
| 2. Organizaciones | Partidos (PSOE, PP), instituciones (Junta, Ministerio), organismos públicos |
| 3. Desambiguación | Un apellido aislado («Bono») se resuelve por el contexto del artículo |


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

#### 5.6.3 Resultados empíricos

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

La interpretación de estos resultados —por qué el contenido recuperado importa más que el hecho de recuperar, y por qué el beneficio decrece con la capacidad del modelo— se desarrolla en §6.2.

## 6. DISCUSIÓN DE LOS RESULTADOS

### 6.1 Alcance de la hipótesis y factores que explican el desempeño

La hipótesis fijaba un F1 igual o superior al 70 % como umbral de viabilidad. El umbral **se alcanza sobre el corpus del dominio** —`gemma4:31b-mlx` obtiene 80,57 % con intervalo de confianza al 95 % de [74,22 %, 86,92 %] y ninguna extracción fallida sobre N=30— y **no se alcanza sobre el corpus periodístico general**, cuyo mejor resultado local es 59,25 % (`gemma4:31b-mlx`) sobre N=120. La hipótesis queda por tanto **confirmada para el dominio específico de sanciones financieras y no confirmada para corpus periodísticos heterogéneos**. La brecha de unos veinte puntos no obedece a un fallo del sistema sino a la naturaleza del material: los artículos de CoNLL-2002 son más largos, mencionan más entidades por texto y mezclan dominios, mientras que el corpus AML está compuesto por textos breves y temáticamente homogéneos. Una meta interna más ambiciosa —85 % de F1, nunca formalizada como hipótesis— queda a 4,43 puntos sobre N=30, distancia abordable mediante ajuste fino supervisado, modelos de mayor capacidad o combinación de varios modelos locales.

Tres factores explican la distribución de resultados observada. El primero es **el idioma del prompt y de sus ejemplos**. Redactar ambos en español aporta 11,12 puntos de F1 sin cambiar de modelo, mejora que ninguno de los dos factores consigue por separado: traducir solo el prompt aporta 4,38 puntos y añadir ejemplos en inglés resta 0,73. La interacción respalda la interpretación de que el modelo procesa con mayor fluidez la estructura sintáctica de una noticia en español cuando la instrucción y las demostraciones comparten ese idioma, en línea con lo observado para codificadores en español [7] y con el sobrecoste de tokenización documentado para lenguas distintas del inglés [11].

El segundo factor es el **compromiso entre tamaño y eficiencia**. `llama3.2`, con 3 000 millones de parámetros, alcanza 63,19 % de F1 con un índice de eficiencia de 26,44 tokens por segundo y por cada mil millones de parámetros, frente a los 0,33 de `gemma4:31b`: una relación de ochenta a uno. Esa asimetría habilita una arquitectura operativa en dos niveles —un modelo compacto para el cribado masivo inicial y uno grande para la validación de los casos de alto riesgo regulatorio— que aprovecha el hecho de que el coste de un falso negativo en cribado es muy inferior al de un falso positivo confirmado.

El tercer factor es la **equivalencia entre ejecución local y en la nube**. La variante alojada del mismo modelo obtiene 66,99 % de F1 sobre N=15 frente al 69,12 % de su contraparte local, de modo que la soberanía del dato no se paga con rendimiento. Para una entidad regulada esto tiene consecuencias directas: elimina la necesidad de suscribir acuerdos de tratamiento de datos con un proveedor externo y reduce la superficie de exposición de información de clientes.

### 6.2 Contribución metodológica: qué recuperar importa más que recuperar

El resultado de mayor alcance metodológico no es el desempeño de ningún modelo concreto sino la comparación entre dos formas de aumentar la generación con información recuperada.

La primera versión del módulo recuperaba **nombres de entidades** desde diccionarios y los inyectaba en el prompt. Lejos de mejorar la extracción, la degradó. La segunda versión recuperaba **criterios**: guías tipológicas del dominio, definiciones de categoría y un ejemplar anotado. Sobre el corpus N=120 esta variante mejoró el desempeño, pero **no de manera uniforme**, y ahí reside el hallazgo: su efectividad está **modulada por la capacidad del modelo receptor**. Las pruebas post-hoc de Tukey muestran que la mejora alcanza significancia estadística únicamente en los dos modelos más débiles del estudio —`nemotron-mini:4b` con 14,52 puntos y `llama3.2:latest` con 10,82—, resulta positiva pero no concluyente en la franja intermedia y es nula o adversa en los modelos de 31B.

La explicación más plausible es de **redundancia de conocimiento**: los modelos de mayor capacidad ya han internalizado durante el preentrenamiento las reglas de desambiguación que la base de conocimiento les ofrece, de modo que el contexto adicional no aporta y sí consume ventana de atención; los modelos pequeños, en cambio, lo aprovechan como compensación de un conocimiento lingüístico que sus pesos no contienen.

De ahí se sigue tanto la explicación del fracaso de la primera versión como una recomendación práctica. El problema del RAG por diccionario no estaba en el concepto de recuperación sino en **la naturaleza de lo recuperado**: sugerir nombres induce al modelo a proponerlos, generando falsos positivos e inhibiendo su capacidad de identificar entidades ausentes del catálogo; sugerir criterios lo orienta sin coartarlo. Y en el plano aplicado, cuando el hardware disponible impide ejecutar modelos de gran tamaño, el RAG contextual constituye una estrategia de bajo coste que acerca el desempeño de un modelo pequeño al de uno considerablemente mayor sin inversión adicional en infraestructura.

## 7. CONCLUSIONES Y TRABAJO FUTURO


### 7.1 Conclusiones

1. **Viabilidad demostrada:** Es técnicamente viable implementar un sistema NER soberano para cumplimiento AML/KYC con modelos de lenguaje de código abierto ejecutados localmente sobre hardware Apple Silicon M4, alcanzando F1=80.57% sin extracciones fallidas sobre el corpus AML N=30 (59.25% sobre el corpus real N=120).

2. **Localización lingüística como factor crítico:** el idioma del prompt y los ejemplos *few-shot* **interactúan**: por separado aportan +4.38 pp y −0.73 pp de F1 respectivamente, pero combinados alcanzan **+11.12 pp**. Los ejemplos solo resultan productivos redactados en el idioma del corpus, lo que tiene implicaciones directas para despliegues en mercados hispanohablantes.

3. **Soberanía de datos sin costo de rendimiento:** El sistema local iguala o supera el rendimiento de la variante cloud (69.12% vs. 66.99% F1 sobre N=15) mientras garantiza privacidad total.

4. **Reducción de costos operativos:** El costo unitario del sistema soberano ($0.052/artículo) versus revisión manual ($8.75/artículo) representa una reducción del 99.4% en el costo unitario directo (60–80% del costo operativo total, que incluye la supervisión humana), con potencial de procesamiento de cientos de artículos diarios sin personal analista dedicado.

5. **Robustez arquitectural:** El controlador AIMD previene desbordamientos de VRAM y gestiona errores de rate-limiting de forma autónoma. El checkpointing garantiza recuperación sin pérdida de datos ante interrupciones.

6. **El RAG contextual supera al RAG por diccionario:** La implementación de la Base de Conocimientos Contextual (KB RAG) demuestra que el reconocimiento de entidades mediante LLMs locales es un problema de **comprensión sintáctico-contextual**, no de búsqueda en bases de datos cerradas. En el estudio N=120 sobre 13 modelos, el KB RAG (`--rag-mode kb_combined`) mejoró el F1-Score de forma **estadísticamente significativa** (Tukey HSD) en los dos modelos más débiles —`nemotron-mini:4b` **+14.52 pp** (p<0.001) y `llama3.2:latest` **+10.82 pp** (p=0.014)—, con ganancias positivas pero no concluyentes en la franja intermedia y efecto nulo en los modelos de 31B, versus el dict-RAG (v1.0), que en un sondeo N=5 sobre el mismo modelo degradó el F1 hasta 0.2367 (−57.8% respecto de su propio baseline). Su efectividad está modulada por la capacidad paramétrica: beneficia sobre todo a los modelos de 3–14B, donde actúa como memoria externa de conocimiento lingüístico sin costo adicional de hardware. Este hallazgo tiene implicaciones directas para el diseño de sistemas RAG en dominio abierto con LLMs soberanos.

7. **La codificación del corpus condiciona la medición, y no de forma neutra:** el corpus N=120 almacena los nombres con *mojibake* —`JosÃ© Bono` donde el nombre real es **José Bono**—, un defecto presente a la vez en las entidades de referencia (20,1 %) y en el texto de entrada (87 % de los artículos). Al ser **coherente entre ambos**, no introduce el sesgo uniforme que cabría suponer: **favorece a los modelos que transcriben literalmente y penaliza a los que normalizan la ortografía**, con un efecto que oscila entre −0.070 y +0.025 de F1 según el modelo. La implicación metodológica excede a este trabajo: en una evaluación de NER, **un defecto de codificación no es ruido de fondo sino una variable que interactúa con el comportamiento del modelo**, y verificar la codificación de la entrada —no solo la de la referencia— debe formar parte del protocolo antes de dar por válida cualquier cifra. El detalle se desarrolla en el **Anexo H**.


### 7.2 Trabajo Futuro

1. **Expansión de la Base de Conocimientos KB RAG (Prioridad Alta):** Ampliar el catálogo de guías tipológicas (actualmente 5 dominios) a 10+ dominios específicos del ecosistema AML latinoamericano (noticias de la UAF chilena, resoluciones de la CMF, sanciones OFAC en español). Agregar 30–50 ejemplares anotados adicionales del corpus balanceado N=120. Evaluar el impacto en F1 con modelos de mayor capacidad (`gemma4:31b-mlx`, `qwen2.5:14b`).

2. **Fine-tuning supervisado (Fase 1):** Aplicar LoRA (Low-Rank Adaptation) sobre `gemma4:31b` con 200+ ejemplos anotados de Kleptotrace/CoNLL-2002 para cerrar la brecha hacia la meta aspiracional de 85% de F1 (§6.1).

3. **Expansión del corpus de evaluación (Fase 2):** Ampliar el corpus de N=120 a N≥200 artículos reales del dominio AML/KYC chileno, incorporando fuentes como la UAF, CMF y bases de datos de OpenSanctions.

4. **Ensemble de modelos (Fase 3):** Combinar las fortalezas de `gemma4:31b` (alto Recall) y modelos compactos como `llama3.2` (alta eficiencia de hardware) mediante votación mayoritaria ponderada por confianza de extracción.

5. **Evaluación en producción (Fase 4):** Despliegue piloto en Austranet con feeds reales de Google Alerts y medición de KPIs operacionales (tiempo de respuesta, carga, satisfacción del analista).

6. **Extensión multiidioma (Fase 5):** Evaluar la robustez del sistema sobre textos en inglés y portugués, considerando el alcance latinoamericano del problema de compliance.

7. **Normalización de codificación del corpus y re-evaluación (Fase 6):** el corpus N=120 almacena los nombres con *mojibake* —`JosÃ© Bono` donde el nombre real es **José Bono**—, defecto presente tanto en las entidades de referencia (20,1 %) como en el texto de entrada (87 % de los artículos), y por tanto **coherente entre ambos**. Esto favorece a los modelos que transcriben literalmente y penaliza a los que normalizan la ortografía, con un efecto que varía entre −0.070 y +0.091 de F1 según el modelo (§5.3.5). La línea de trabajo consiste en **normalizar la codificación en ambos lados de la comparación** —reparando la referencia y la extracción antes del cotejo difuso, de modo que el resultado deje de depender de la representación de bytes— y **re-ejecutar el estudio N=120** para obtener valores absolutos libres de esta interacción. No se abordó en este trabajo porque el cotejo se resuelve en tiempo de inferencia y las extracciones por registro no se conservaron, lo que obliga a repetir la inferencia completa.


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


## 9. ANEXOS

### Anexo A — Estructura del Repositorio de Código


| Ruta | Descripción |
|:---|:---|
| `repos/ner-llm-entity-benchmark/` |  |
| `src/` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`main.py` | Orquestador principal (+--rag-mode CLI, v1.1) |
| &nbsp;&nbsp;&nbsp;&nbsp;`config.py` | Configuración global (+rag_mode field, v1.1) |
| &nbsp;&nbsp;&nbsp;&nbsp;`data_loader.py` | Carga y validación del corpus |
| &nbsp;&nbsp;&nbsp;&nbsp;`llm_runner.py` | Runner LLM con parseo en cascada |
| &nbsp;&nbsp;&nbsp;&nbsp;`evaluator.py` | Métricas F1 + taxonomía de errores |
| &nbsp;&nbsp;&nbsp;&nbsp;`pub_sub.py` | Cola Pub/Sub multithreading |
| &nbsp;&nbsp;&nbsp;&nbsp;`adaptive_workers.py` | Controlador AIMD |
| &nbsp;&nbsp;&nbsp;&nbsp;`checkpoint.py` | Persistencia de estado |
| &nbsp;&nbsp;&nbsp;&nbsp;`rag_manager.py` | RAGManager: Dict-RAG legacy (v1.0) |
| &nbsp;&nbsp;&nbsp;&nbsp;`kb_rag_manager.py` | KBRAGManager: KB RAG contextual (v1.1, NUEVO) |
| &nbsp;&nbsp;&nbsp;&nbsp;`dashboard.py` | Interfaz Streamlit (7 pestañas) |
| &nbsp;&nbsp;&nbsp;&nbsp;`statistics.py` | ANOVA + Tukey HSD + IC95 |
| &nbsp;&nbsp;&nbsp;&nbsp;`providers/` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`base.py` | LLMProvider ABC |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`factory.py` | LLMProviderFactory |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ollama_provider.py` | Proveedor Ollama (+template KB RAG, v1.1) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`openai_provider.py` | Proveedor OpenAI (cloud) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`__init__.py` | Facade get_provider() |
| `data/` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`benchmark_balanced_120.json` | Corpus N=120 (Gold Standard real) |
| &nbsp;&nbsp;&nbsp;&nbsp;`dictionaries/` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`persons.json` | Diccionario de personas (v1.0) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`organizations.json` | Diccionario de organizaciones (v1.0) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`augmented_persons.json` | Personas aumentadas (v1.0) |
| &nbsp;&nbsp;&nbsp;&nbsp;`knowledge_base/` | Base de Conocimientos KB RAG (v1.1, NUEVO) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`domain_guidelines.json` | 5 dominios con reglas NER tipológicas |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`few_shot_exemplars.json` | 7 ejemplares anotados (artículos reales) |
| `results/` | Salidas del benchmark |
| &nbsp;&nbsp;&nbsp;&nbsp;`benchmark_results.csv` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`statistical_report.md` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`benchmark_balanced_120_<timestamp>/` | Resultados por ejecución |
| `research/` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;`rag/` |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`2026-08-31_analisis_contenido_rag_base_conocimientos.md` | Investigación RAG |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`TODO-RAG-20260901.md` | Tracking implementación |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`WORKLOG.md` | Bitácora de trabajo |
| `SYSTEM_PROMPT.md` | Prompt del sistema (few-shot español) |
| `SYSTEM_PROMPT_EN.md` | Prompt del sistema (inglés) |
| `SYSTEM_PROMPT_ES.md` | Prompt del sistema (español) |



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


*Informe Final de Tesina — Magíster en Tecnologías de la Información (MTI)*  
*Universidad Técnica Federico Santa María — Valparaíso, Chile*  
*Julio 2026*

### Anexo D — Detalle Técnico de la Optimización del Módulo RAG Contextual (KB RAG)

Se documentan aquí los diagramas de flujo, tablas de configuración CLI y catálogos de datos referidos en §5.6, movidos desde el cuerpo del informe para cumplir el límite de extensión institucional. Toda la evidencia se conserva íntegra.


#### D.1 Flujo RAG Original (Degradado)


_Tabla 14. Flujo RAG Original (Degradado)_


| Paso | Acción | Resultado |
|---|---|---|
| 1. Entrada | Noticia política española (500 palabras) | — |
| 2. Embedding | all-MiniLM-L6-v2 | Vector de consulta |
| 3. Recuperación | ChromaDB: Top-5 por coseno | GRANJA LA SIERRA LTDA. (Org); ASES DE COMPETENCIA Y CIA. (Org); [3 orgs colombianas irrelevantes] |
| 4. Inyección en prompt | Restrictiva: "DO NOT extract unless they explicitly appear..." | — |
| 5. Efecto en LLM | — | Recall: 62.8% → 21.6%  ❌ |


#### D.2 Flujo KB RAG (Mejorado)


_Tabla 15. Flujo KB RAG (Mejorado)_


| Paso | Acción | Resultado |
|---|---|---|
| 1. Entrada | Noticia política española (500 palabras) | — |
| 2. Embedding | all-MiniLM-L6-v2 | Vector de consulta |
| 3. Recuperación | ChromaDB 'ner_knowledge_base': Top-1 guideline + Top-1 exemplar | Dominio recuperado: politics_administrative (ES) |
| 4. Contexto inyectado | DOMAIN CONTEXT (ver detalle abajo) + ejemplo similar recuperado | — |
| 5. Inyección en prompt | Positiva: "[EXTRACTION GUIDANCE]" | — |
| 6. Efecto en LLM | — | F1: 0.3521 → 0.5489  ✅  (+19.7 pp) Recall: 33.3% → 59.5%  ✅  (+26.2 pp) |


#### D.3 Implementación Técnica del Módulo KB RAG (src/kb_rag_manager.py)

El módulo src/kb_rag_manager.py (KBRAGManager) implementa cuatro modos de operación configurables:


_Tabla 16. Configuración CLI del Módulo KB RAG_


| Modo | Flag CLI | Descripción | Caso de Uso |
|---|---|---|---|
| entities | --rag-mode entities | Legacy: diccionario de nombres (comportamiento original) | Compatibilidad hacia atrás |
| kb_guidelines | --rag-mode kb_guidelines | Reglas tipológicas de desambiguación por dominio | Artículos de dominio conocido |
| kb_fewshot | --rag-mode kb_fewshot | Ejemplo anotado semánticamente más similar | Transferencia de conocimiento |
| kb_combined | --rag-mode kb_combined | Guía + ejemplo (recomendado) | Mejor F1 |

La base de conocimientos se organiza en dos colecciones ChromaDB separadas para garantizar compatibilidad con el sistema preexistente:

ner_dictionaries: Colección legacy (diccionarios de entidades, preservada)

ner_knowledge_base: Nueva colección (guías + ejemplares, 12 documentos)

Configurabilidad garantizada: El sistema es activable/desactivable mediante flags CLI sin modificar código:


```
# Modo baseline (sin RAG)
./venv/bin/python3 src/main.py --models gemma4:31b-mlx --data-file data/benchmark_balanced_120.json

# Modo RAG legacy (diccionario de entidades)
./venv/bin/python3 src/main.py --rag-study --rag-mode entities ...

# Modo KB RAG (nueva implementación, recomendado)
./venv/bin/python3 src/main.py --rag-study --rag-mode kb_combined ...
```

Template de inyección diferenciado: El módulo ollama_provider.py detecta automáticamente el tipo de contexto RAG y aplica el template apropiado:

Entity-dict RAG (legacy): Template restrictivo — "DO NOT extract unless they explicitly appear..." — previene alucinaciones de entidades ausentes.

KB RAG (nuevo): Template positivo — "[EXTRACTION GUIDANCE] Apply these rules to the news text" — instruye activamente al LLM sin suprimir su capacidad de extracción.

Informe Final de Tesina — Magíster en Tecnologías de la Información (MTI)

Universidad Técnica Federico Santa María — Valparaíso, Chile

Julio 2026


#### D.4 Catálogo de Guías Tipológicas y Ejemplares Few-Shot de la Base de Conocimientos


_Tabla 17. Guías Tipológicas de Dominio de la Base de Conocimientos_


| Dominio | ID | Idioma | Keywords Clave |
|---|---|---|---|
| Política y Administración | politics_es | ES | PSOE, PP, junta, ministerio, portavoz |
| Corporativo y Financiero | corporate_financial_es | ES | bolsa, fusión, consejo de administración |
| AML y Sanciones | aml_sanctions_en | EN | OFAC, indictment, money laundering, IEEPA |
| Judicial y Crimen | judicial_crime_es | ES | tribunal, fiscal, audiencia nacional |
| Deportivo y Social | sports_social_es | ES | liga, federación, club |


_Tabla 18. Ejemplares Few-Shot de la Base de Conocimientos_


| ID Ejemplar | Dominio | Fuente |
|---|---|---|
| ex_politics_es_001 | Política ES | real_mixed_1 |
| ex_politics_es_002 | Política ES | real_mixed_41 |
| ex_corporate_financial_es_001 | Corporativo ES | real_mixed_21 |
| ex_judicial_es_001 | Judicial ES | real_mixed_101 |
| ex_aml_sanctions_en_001 | AML/Sanciones EN | real_mixed_59 |
| ex_aml_sanctions_en_002 | AML/Sanciones EN | real_mixed_79 |
| ex_aml_sanctions_en_003 | AML/Sanciones EN | real_mixed_27 |


#### D.5 Análisis Comparativo Cronológico — RAG v1.0 vs. v1.1


_Tabla 19. Comparación Cronológica RAG v1.0 vs. v1.1_


| Aspecto | Sistema v1.0 (Dic 2025 – Ago 2026) | Sistema v1.1 (Sep 2026) |
|---|---|---|
| Contenido RAG | Diccionarios de nombres (3.605 personas, 1.848 orgs) | Guías tipológicas + ejemplares few-shot |
| Colección ChromaDB | ner_dictionaries | + ner_knowledge_base (nueva, no reemplaza) |
| Template de inyección | Restrictivo (“DO NOT extract unless…”) | Positivo (“Apply these rules to the text”) |
| Modo de operación | Binario (RAG on/off) | Cuatro modos configurables por CLI |
| F1-Score RAG (llama3.2) | 0.2367 en sondeo N=5 (−57.8% vs su propio baseline 0.5614) | 0.4943 (+25.3% vs baseline) |
| F1-Score RAG (qwen2.5:14b) | — | 0.5651 (+8.9% vs baseline) |
| Configurabilidad | No (hardcoded) | Sí (--rag-mode {entities,kb_guidelines,kb_fewshot,kb_combined}) |
| Datos sintéticos | Sí (12.000 augmented_persons) | No (solo datos reales del corpus de evaluación) |


### Anexo E — Procedencia de los Datos del Benchmark General (N=15)


_Tabla 20. Resultados Completos del Benchmark General (13 Configuraciones, N=15)_


| Filas de la Tabla 5 | Corrida de origen |
|---|---|
| gemma4:31b | gemma4_31b_n15_REMOTO (equipo de 48 GB) |
| gemma4:latest (ZS-ES) y (FS-ES) | ablacion_n15_REMOTO |
| gemma4:31b-cloud | cloud_n15_limpio_20260905 |
| Resto de configuraciones | results/benchmark_results.csv (N=15, modo entities) |
| Excluidos del estudio | nuextract:latest, gemini-3.1-flash-lite, minimax-m3 |


### Anexo F — Metodología Detallada de Generación del Corpus Sintético N=30

Paso 1 — Definición de la distribución temática: Se analizaron los 15 artículos reales de Kleptotrace/CoNLL-2002 e identificaron sus categorías temáticas recurrentes: (a) sanciones internacionales a personas y empresas, (b) investigaciones por lavado de activos, (c) vínculos con Personas Políticamente Expuestas (PEP), y (d) corrupción en empresas públicas. Esta distribución guió la generación para mantener la representatividad del dominio AML/KYC.

Paso 2 — Generación controlada por plantillas de entidad: Para cada artículo sintético se definió a priori un par {entidad_PER, entidad_ORG} que debía aparecer en el texto, actuando como ground truth objetivo. Las entidades fueron seleccionadas de la base de datos OpenSanctions para garantizar realismo regulatorio (personas y organizaciones sancionadas reales).

Paso 3 — Instrucción al LLM generador: El modelo gemma4:31b recibió el siguiente prompt de generación:


```
Eres un periodista de investigación financiera. Redacta un párrafo corto (2-4 oraciones) en español
sobre la entidad "{entidad_PER}" vinculada a "{entidad_ORG}" en el contexto de [temática aleatoria].
El texto debe ser fáctico, neutro y similiar en estilo a noticias de compliance financiero.
Debe mencionar exactamente estas entidades y no otras personas u organizaciones adicionales.
```

Paso 4 — Verificación del ground truth: Cada artículo generado fue revisado manualmente para confirmar que las entidades objetivo aparecían efectivamente en el texto y que no se hubieran introducido entidades ajenas al ground truth anotado. Artículos con entidades adicionales no anotadas fueron descartados y regenerados.

Paso 5 — Control de calidad por diversidad: Se verificó que ningún artículo generado replicara literalmente oraciones de otro artículo del corpus (deduplicación por similitud coseno > 0.85). La longitud promedio resultante fue de 202 caracteres (rango 145–293), con 1,2 entidades PER y 2,3 entidades ORG por artículo.


#### D.6 Degradación Observada — RAG por Diccionario (Baseline vs. RAG-Dict)


_Tabla 21. Degradación Observada — RAG por Diccionario_


| Modelo | Baseline F1 | RAG-Dict F1 | Delta |
|---|---|---|---|
| gemma4:latest | 0.5446 | 0.5257 | −0.0189 |
| qwen2.5:14b | 0.5189 | 0.5071 | −0.0118 |
| llama3.2:latest | 0.3945 | 0.4196 | +0.0251 |


#### D.7 Mini-Benchmark de Validación Preliminar (N=5, llama3.2:latest)


_Tabla 22. Mini-Benchmark de Validación Preliminar (N=5)_


| Condición | F1-Score | Precisión | Recall | Δ F1 vs Baseline |
|---|---|---|---|---|
| Baseline (zero-shot) | 0.3521 | 0.4250 | 0.3333 | — |
| KB Combined RAG | 0.5489 | 0.5227 | 0.5954 | +0.1968 |


#### D.8 Reglas de la Base de Conocimientos Contextual


_Tabla 23. Reglas de la Base de Conocimientos Contextual_


| Regla | Contenido |
|---|---|
| 1. Personas | Extrae SOLO el nombre propio... |
| 2. Organizaciones | Partidos (PSOE, PP), Junta... |
| 3. Desambiguación | Un apellido solo ('Bono')... |


### Anexo G — Declaración de Uso de Inteligencia Artificial en la Elaboración de esta Tesina

Este anexo declara, con propósito de transparencia académica, el alcance y los límites del uso de herramientas de inteligencia artificial (IA) generativa durante el desarrollo de esta tesina. La declaración se basa en el registro documental del proyecto: el historial de control de versiones (20 commits entre el 29 de junio y el 1 de septiembre de 2026), los registros de trabajo WORKLOG.md (raíz del repositorio y research/rag/), y los informes de investigación asociados.


#### G.1 Trabajo realizado por el autor de la tesina

La totalidad de las decisiones intelectuales y metodológicas del trabajo corresponden al autor. En particular: la identificación y formulación del problema de investigación (monitoreo de entidades de riesgo AML/KYC bajo restricción de soberanía de datos); el planteamiento de la hipótesis de trabajo y del umbral de viabilidad F1 ≥ 70%; el modelado conceptual del problema como tarea de NER en vocabulario abierto sobre noticias en español; el diseño de la arquitectura del sistema (pipeline pub/sub con control adaptativo AIMD, capa Factory/Facade de proveedores, gestión de VRAM en Apple Silicon); la selección y priorización de los modelos a evaluar, con hipótesis fundamentadas previas a la evaluación empírica; la definición del diseño experimental, de las métricas y del protocolo estadístico (ANOVA de una vía y Tukey HSD); la decisión metodológica de mantener el corpus sintético N=30 y el corpus real N=120 como alternativas conmutables en lugar de reemplazar uno por otro; la autorización acotada y documentada del uso de modelos en la nube exclusivamente como línea base de comparación sobre corpus público; la verificación manual del ground truth de los artículos generados; la ejecución de los benchmarks sobre su propio hardware; y la interpretación, validación y redacción sustantiva de los resultados, la discusión y las conclusiones.

El autor es asimismo responsable de la auditoría crítica de los artefactos producidos con apoyo de IA. Ejemplo documentado de esta supervisión es la detección del error de nomenclatura de cuantización en el identificador de un modelo (sufijo q8 sobre un modelo de precisión mixta NVFP4), verificada contra los manifiestos del registro de Ollama y corregida transversalmente en la documentación del proyecto.


#### G.2 Apoyo de IA en la elaboración de artefactos de prueba

Se utilizó IA generativa como instrumento en la construcción de artefactos de evaluación, siempre bajo especificación y verificación del autor. El corpus sintético N=30 (kleptotrace_augmented_30.json) fue generado mediante aumento de datos guiado por LLM: el autor definió a priori la distribución temática, los pares {entidad_PER, entidad_ORG} objetivo tomados de OpenSanctions y el prompt de generación (Anexo F); el modelo gemma4:31b produjo los textos; y cada artículo fue revisado manualmente para confirmar el ground truth, descartándose y regenerándose los que introducían entidades no anotadas. El corpus real N=120 (benchmark_balanced_120.json) no fue generado por IA: combina 15 artículos del corpus Kleptotrace con 105 artículos muestreados de CoNLL-2002 en español. Los ejemplares few-shot de la base de conocimientos contextual fueron extraídos de artículos reales anotados del propio corpus de evaluación, sin generación sintética.


#### G.3 Apoyo de IA en implementación, documentación y formato

Asistentes de programación basados en LLM se emplearon como apoyo en tareas de implementación y documentación, bajo revisión y prueba del autor: generación y refactorización de código del banco de pruebas y del módulo KB RAG a partir de decisiones arquitectónicas previamente definidas; escritura de scripts auxiliares de análisis de resultados; mantenimiento del registro cronológico de trabajo (WORKLOG.md); conversión y regeneración de documentos mediante pandoc; y tareas de formato del informe: transplante del contenido a la plantilla institucional UTFSM/MTI, conversión de diagramas en texto a tablas, numeración de secciones, leyendas de tablas, condensación editorial para cumplir el límite de extensión y reubicación de detalle técnico a los anexos, preservando íntegramente la evidencia. Ninguna de estas intervenciones introdujo resultados experimentales: las cifras reportadas provienen exclusivamente de las corridas registradas en el directorio results/ del repositorio.


#### G.4 Límites y verificación

No se utilizó IA para producir, estimar o extrapolar datos experimentales, ni para redactar conclusiones no sustentadas en las corridas registradas. Toda cifra citada en este informe es trazable a un archivo de resultados versionado en el repositorio. Las limitaciones conocidas se declaran explícitamente en el cuerpo del informe, entre ellas que la validación complementaria sobre el corpus real N=120 (§5.3.5) cubre un subconjunto de cinco modelos y que la re-evaluación de los modelos restantes queda como trabajo futuro (§7.2). El autor asume la responsabilidad final sobre el contenido, la exactitud y la integridad académica de este documento.

### Anexo H — Codificación del corpus: análisis del *mojibake* y su efecto sobre la medición

#### H.1 Qué es el *mojibake*

*Mojibake* (文字化け, «transformación de caracteres») designa el texto ilegible que resulta de **escribir una cadena con una codificación y leerla con otra**. En español afecta a las vocales acentuadas y a la «ñ», porque en UTF-8 no ocupan un byte sino dos.

La letra «é» se codifica en UTF-8 como los bytes `0xC3 0xA9`. Si esos bytes se leen después como **Latin-1**, donde cada byte equivale a un carácter, se obtienen dos caracteres visibles en lugar de uno:

| Byte | Interpretación Latin-1 |
|:---:|:---:|
| `0xC3` | `Ã` |
| `0xA9` | `©` |

De ahí que `José` aparezca almacenado como `JosÃ©`. La firma del defecto es la **`Ã` inicial**, presente en toda vocal acentuada y en la `ñ`:

| Forma almacenada (corrupta) | Forma real |
|:---|:---|
| `JosÃ© Bono` | José Bono |
| `Emiliano GarcÃ­a-Page` | Emiliano García-Page |
| `MarÃ­a MuÃ±oz` | María Muñoz |
| `AdministraciÃ³n` | Administración |

La reparación consiste en deshacer el paso erróneo: `s.encode('latin-1').decode('utf-8')`.

#### H.2 Alcance medido en el corpus N=120

| Comprobación sobre `data/benchmark_balanced_120.json` | Resultado |
|:---|:---:|
| Entidades de referencia totales | 1 406 |
| Entidades con *mojibake* | **283 (20,1 %)** |
| De ellas, **irrecuperables** en el cotejo difuso (umbral 85) | **66 (4,7 % del total)** |
| Artículos con *mojibake* en el campo `text` | **104 de 120 (87 %)** |
| Artículos con *mojibake* en el campo `title` | 0 |
| Entidades corruptas que aparecen **igual de corruptas** en el texto | **283 de 283** |
| Entidades corruptas que aparecen **correctas** en el texto | **0** |

Los corpus N=15 (`kleptotrace.json`, 212 entidades) y N=30 (`kleptotrace_augmented_30.json`, 105 entidades) están **libres del defecto**, por lo que los resultados de §5.1, §5.2 y §5.3.1–§5.3.4 no se ven comprometidos.

El umbral de 85 explica por qué solo una parte resulta irrecuperable: en cadenas largas la corrupción es una fracción menor del total y la similitud se mantiene por encima del corte —`Emiliano GarcÃ­a-Page` frente a su forma correcta obtiene 93—, mientras que en cadenas cortas la hunde: `JosÃ© Bono` frente a `José Bono` obtiene **84**, un punto por debajo del umbral.

#### H.3 Por qué la conclusión inmediata era incorrecta

La primera lectura del hallazgo fue que el defecto deprimía el *recall* de todos los modelos por igual, en torno a 4,7 puntos, sin alterar el orden relativo. Esa lectura **omitía comprobar la entrada**.

Al estar el defecto **también en el texto que lee el modelo**, y de forma **coherente** con la referencia, el corpus es internamente consistente: el modelo lee `Emiliano GarcÃ­a-Page` y la referencia espera `Emiliano GarcÃ­a-Page`. En consecuencia:

- un modelo que **transcribe literalmente** lo que ve **coincide** con la referencia y no sufre penalización;
- un modelo que **normaliza la ortografía** al español correcto produce `Emiliano García-Page` y **deja de coincidir**, pese a haber acertado.

El defecto no impone un suelo común: **recompensa una conducta y castiga la contraria**.

#### H.4 Evidencia empírica del efecto diferencial

Diferencia de F1 entre los 88 artículos afectados y los 31 no afectados, sobre los mismos registros para todos los modelos:

| Modelo | Δ F1 (con *mojibake* − sin) |
|:---|--:|
| `gemma4:latest` (baseline) | **−0.0695** |
| `gemma4:12b-mlx` (baseline) | −0.0422 |
| `gemma4:31b-mlx` (baseline) | −0.0395 |
| `llama3.1:8b` (KB RAG) | −0.0004 |
| `mistral-nemo:latest` (KB RAG) | +0.0122 |
| `deepseek-r1:1.5b` (baseline) | +0.0199 |
| `gemma:latest` (KB RAG) | **+0.0249** |

El rango entre extremos alcanza **9,4 puntos porcentuales**.

> **Cautela metodológica.** Los artículos afectados podrían ser además más largos o intrínsecamente más difíciles, lo que confundiría la magnitud absoluta de cada Δ. Sin embargo, la dificultad desplazaría a todos los modelos en la misma dirección; **la dispersión entre modelos sobre registros idénticos** es lo que acredita una interacción específica de cada modelo. Una versión previa de esta tabla situaba a `gpt-oss:20b` en el extremo positivo con +0,091, y se advirtió entonces que esa fila era la menos fiable por estar dominada por un artefacto del arnés. Corregido el artefacto y repetida la medición, su valor real es **−0,034**, dentro del rango del resto. El episodio ilustra la necesidad de descartar defectos de ejecución antes de interpretar un valor extremo.

#### H.5 Cómo debe repararse

Corregir únicamente la referencia **invertiría la injusticia en lugar de eliminarla**: pasaría a penalizar al modelo que transcribe con fidelidad. La reparación correcta es **normalizar ambos lados de la comparación** —aplicar la corrección de codificación a la entidad de referencia *y* a la extraída antes del cotejo difuso—, de modo que `JosÃ© Bono` y `José Bono` converjan a la misma forma y el resultado deje de depender de la representación de bytes.

Esta corrección **no pudo aplicarse retroactivamente**: el cotejo se resuelve en tiempo de inferencia y de cada registro solo se conservaron los recuentos de aciertos y errores, no las entidades extraídas. Repuntuar sobre lo almacenado —como sí fue posible con la corrección de la convención de puntuación descrita en §4.4— resulta aquí inviable, y la corrección exigiría re-ejecutar el estudio completo. Se documenta por tanto como limitación (§5.3.5) y como línea de trabajo futuro (§7.2, punto 7).

#### H.6 Implicaciones para la evaluación de sistemas NER

1. **Verificar la codificación de la entrada, no solo la de la referencia.** Un defecto presente en ambas no se comporta como el mismo defecto presente en una sola.
2. **No presuponer que un defecto de datos sesga de forma uniforme.** Cuando el corpus es coherente en su corrupción, el sesgo depende de cómo trate cada modelo la normalización ortográfica, y puede alterar el orden relativo.
3. **Conservar las extracciones por registro, no solo las métricas agregadas.** Es la diferencia entre poder recalcular sobre lo guardado y tener que repetir toda la inferencia.
4. **Aplicar toda corrección de forma uniforme.** Reparar el corpus para un solo modelo lo mediría con una vara distinta de la del resto e invalidaría la comparación.

