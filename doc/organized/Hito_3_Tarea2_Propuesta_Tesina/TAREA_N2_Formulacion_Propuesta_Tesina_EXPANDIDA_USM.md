UNIVERSIDAD TÉCNICA FEDERICO SANTA MARÍA

DEPARTAMENTO DE INFORMÁTICA
Magíster en Tecnologías de la Información (MTI)
FORMULACIÓN DE UNA PROPUESTA DE PROYECTO DE
TESINA

para optar al grado de
Magíster en Tecnologías de la Información

I. IDENTIFICACIÓN Y RESUMEN DEL PROYECTO
1.1 Identificación del proponente y candidato a magíster
Nombre del estudiante

EDUARDO MAURICIO AHUMADA GALLARDO

RUT

12.814.696-2

Ciudad y región de residencia

Independencia 200, Vicuña

Ciudad y región de trabajo

Independencia 200, Vicuña, Independiente

E-mail y teléfono de contacto

Eahumada@gmail.com +56997828992

Año de ingreso al MTI

2013

1.2 Identificación del Proyecto de tesina propuesto
Título del proyecto

Clasificación y Extracción de Entidades Nombradas
(NER) en Noticias de Cumplimiento Normativo en
Empresas Mediante RAG y un Modelo de Lenguaje
Grande (LLM) usando Ollama

Área principal de TI

Inteligencia Artificial / Procesamiento de Lenguaje Natural
(NLP)

Profesor guía propuesto

JOSÉ LUIS MARTÍ LARA

Organización/empresa vinculada

Austranet

Persona y cargo del contacto

Manuel Muñoz - Fundador

E-mail y teléfono del contacto

[email y teléfono del contacto]

…………………………………
FIRMA

1.3 Resumen del Proyecto de tesina propuesto
Contexto y Definición del Problema:
El contexto del proyecto surge de la necesidad crítica de instituciones financieras a nivel mundial de
automatizar procesos de cumplimiento normativo (Compliance). Específicamente, la gestión de
regulaciones como Know Your Customer (KYC) y Personas Políticamente Expuestas (PEP)
requiere monitoreo continuo de fuentes públicas de información. El gran volumen de noticias
obtenidas por suscripción a fuentes públicas (listas de correo de Google Alerts, RSS feeds, servicios
de inteligencia comercial) exige una revisión manual que resulta ineficiente, costosa y propensa a
errores humanos, elevando significativamente los costos operativos y riesgos reputacionales para
las instituciones.
El problema central es de naturaleza técnica y operativa: la dificultad de extraer entidades precisas
y contextualizadas de textos no estructurados (artículos de noticias) de manera automatizada. Esto
incluye la identificación de actores relevantes (personas, organizaciones, ubicaciones geográficas)
en contextos complejos de compliance, donde la desambiguación semántica es crítica.
Solución Propuesta y Aspectos Técnicos:
La solución propuesta es un sistema distribuido que emplea la técnica de Generación Aumentada
por Recuperación (RAG), en donde cada noticia individual es tratada como fuente de contexto única
para un Modelo de Lenguaje Grande (LLM) de código abierto, ejecutado localmente mediante
Ollama. Esta arquitectura permite al LLM realizar el Reconocimiento de Entidades Nombradas
(NER) con capacidad semántica superior a métodos tradicionales, extrayendo personas, lugares y
organizaciones, con contexto empresarial y regulatorio. Los aspectos técnicos clave incluyen: (1)
Arquitectura RAG adaptada para mitigar alucinaciones en LLMs; (2) Ingeniería de prompts para
optimizar respuestas en dominio de compliance; (3) Procesamiento distribuido en batch para
escalabilidad; (4) Uso de modelos abiertos (Gemma, DeepSeek, Llama) para evitar fuga de datos a
APIs propietarias.

Objetivos del Proyecto:

1. Diseñar e implementar una arquitectura RAG/LLM optimizada para extracción de entidades
nombradas en noticias de compliance en español.
2. Evaluar y comparar el desempeño de al menos tres modelos de lenguaje de código abierto
(Gemma, DeepSeek, Llama) bajo la arquitectura RAG.
3. Validar que el sistema supera la precisión y exhaustividad de la extracción manual humana,
demostrando viabilidad para automatización de tareas de alto riesgo regulatorio.
Metodología de Validación y Resultados Esperados:

La validación se basará en un enfoque cuantitativo experimental. Se construirá un Ground Truth
mediante etiquetado manual riguroso de un corpus de 100-200 noticias representativas, validado
por expertos en compliance. Se ejecutarán los tres modelos LLM sobre el mismo corpus, calculando
métricas estándar de NLP (Precisión, Recall, F1-Score, tasa de alucinación). Los resultados
esperados incluyen: (1) Una extracción de NER de alta calidad (F1-Score superior a 85%); (2)
Demostración que modelos LLM+RAG superan línea base humana en precisión; (3) Identificación
del mejor modelo para implementación en entorno de producción; (4) Validación de la viabilidad de
usar LLMs de código abierto en contextos regulados.
Impacto Industrial y Nacional:

El impacto esperado es significativo para el ecosistema FinTech chileno: reducción drástica de
costos operacionales en tareas de compliance (estimado 60-80% de ahorro en revisión manual),
mejora sustancial de precisión en detección de riesgos reputacionales, y demostración de viabilidad
de soluciones de IA generativa de código abierto en entornos regulados nacionales. Esto es
particularmente relevante para el sector FinTech y RegTech chileno, donde las instituciones
actualmente dependen de servicios propietarios en la nube con costos prohibitivos. A nivel
internacional, contribuye al estado del arte en aplicación de LLMs para NLP regulado, demostrando

que modelos abiertos ejecutados localmente pueden reemplazar soluciones propietarias
manteniendo estándares de confiabilidad requeridos por reguladores.
1.4 Palabras claves: Reconocimiento de Entidades Nombradas (NER), Cumplimiento Normativo
(Compliance), Generación Aumentada por Recuperación (RAG), Modelos de Lenguaje Grande
(LLM), Ollama

II. FORMULACIÓN GENERAL DEL PROYECTO
Definición del Problema y Solución Propuesta
(a) Contexto Organizacional y Definición del Problema
El trabajo de tesina se enmarca en el sector de Tecnologías de la Información (TI) aplicadas al
cumplimiento normativo (Compliance), vinculado a la empresa LeanStack SpA, empresa
especializada en soluciones de inteligencia regulatoria y análisis de cumplimiento normativo para el
sector financiero. LeanStack SpA opera en el mercado latinoamericano proporcionando servicios
de monitoreo de cumplimiento normativo, con enfoque particular en regulaciones financieras como
Know Your Customer (KYC) y Personas Políticamente Expuestas (PEP).
Tener acceso oportuno y exhaustivo a información pública sobre entidades (personas naturales,
empresas, funcionarios públicos) es crucial para bancos e instituciones financieras chilenas e
internacionales. Esto les permite cumplir con regulaciones estrictas establecidas por organismos
reguladores nacionales (Superintendencia Financiera, CMF) e internacionales (FATF, regulaciones
anti-lavado de activos). La esencia del compliance en este contexto es la identificación automática
y gestión de riesgos asociados a clientes y entidades, incluyendo detección de vinculación con
actividades ilícitas, sanciones internacionales, o comportamientos sospechosos reportados en
medios de comunicación.
El flujo operativo típico en LeanStack SpA y clientes similares es: (1) Suscripción a múltiples fuentes
de noticias públicas (Google Alerts, servicios de news feed, bases de datos de criminalidad, listas
de sanciones internacionales); (2) Ingesta de gran volumen de artículos diariamente (cientos de
noticias); (3) Revisión manual por analistas especializados para identificar si alguna noticia
menciona clientes o proveedores de la institución financiera; (4) Clasificación del riesgo asociado;
(5) Escalado a comités de compliance si se identifica riesgo. Este proceso es altamente laborioso,
consume recursos significativos y es propenso a errores humanos.

El núcleo técnico del problema radica en la naturaleza de los datos: las noticias son textos no
estructurados donde las entidades relevantes aparecen en contextos complejos con ambigüedad
semántica. Por ejemplo, una misma persona puede aparecer en noticia tanto como sujeto
investigado como investigador; una organización puede ser víctima o perpetrador de fraude. Los
métodos tradicionales de extracción automática (expresiones regulares, modelos estadísticos de
campos aleatorios condicionales/CRF) carecen de capacidad semántica para desambiguar estos
contextos, resultando en altas tasas de falsos positivos que generan alertas innecesarias y falsos
negativos que dejan riesgos sin detectar.
La importancia de resolver este problema para LeanStack SpA y sus clientes es estratégica:
automatizar la detección de entidades con alta precisión reduciría drásticamente costos
operacionales (eliminando necesidad de analistas dedicados a lectura de noticias), mejoraría la
cobertura y velocidad de detección de riesgos (procesamiento en minutos vs. horas), y permitiría
escalabilidad a nuevos mercados sin incremento proporcional de costos. Operacionalmente,
representa la diferencia entre una solución viable a nivel nacional vs. una limitada a segmentos
premium de clientes que pueden costear revisión manual exhaustiva.
(b) Alternativas de Solución Identificadas y Comparación
En la industria y literatura se han identificado las siguientes alternativas para resolver el problema
de extracción de entidades en noticias de compliance:

4. Revisión Manual Exhaustiva (Status Quo Actual): Analistas especializados revisan
manualmente cada noticia. Fortalezas: Alta precisión semántica, adaptabilidad a nuevos
contextos. Debilidades: Extremadamente costosa (requiere equipo significativo de
especialistas), no escalable ante crecimiento de volumen de noticias, sujeta a errores
humanos por fatiga, lenta (análisis de centenares de noticias toma días), difícil de mantener
consistencia de criterios entre analistas.

5. Sistemas Basados en Reglas y Expresiones Regulares: Uso de patrones predefinidos (ej.
búsqueda de nombres de clientes conocidos). Fortalezas: Rápido, no requiere datos de
entrenamiento. Debilidades: Extremadamente frágil ante variaciones léxicas (nombres
pueden estar escritos de múltiples formas), no entiende contexto, alto número de falsos
positivos (detecta nombres que no son relevantes al contexto regulatorio).
6. Modelos

Estadísticos

Tradicionales

(CRF

-

Campos

Aleatorios

Condicionales):

Aproximación utilizada en proyecto previo de LeanStack Spa ("Clasificación automática de
noticias con nombres mediante técnicas CRF"). Fortalezas: Mejor que reglas puras, captura
patrones

secuenciales.

Debilidades:

Requiere

ingeniería

manual

extensiva

de

características (feature engineering), desempeño degrada dramáticamente ante variabilidad
lingüística en dominio de compliance en español, requiere corpus etiquetado para
entrenamiento.
7. Modelos de Deep Learning Supervisados (BERT, BiLSTM-CRF): Modelos neuronales
entrenados en corpus etiquetados. Fortalezas: Superior precisión semántica vs. CRF,
arquitectura Transformer permite capturar dependencias de largo alcance. Debilidades:
Requieren grandes volúmenes de datos etiquetados (típicamente miles de ejemplos) que
no están disponibles para dominio específico de compliance en español, requieren finetuning para cada nuevo dominio, alto costo computacional de entrenamiento.
8. APIs Propietarias en la Nube (OpenAI GPT, Google Cloud NLP, AWS Comprehend):
Servicios comerciales de extracción de entidades en la nube. Fortalezas: Alta precisión,
soporte multiidioma, mantenimiento gestionado por proveedor. Debilidades críticos: Datos
de noticias y identificación de clientes se envían a servidores externos (riesgo
regulatorio/privacidad), costos operacionales prohibitivos para procesamiento en batch de
centenares de noticias diarias, dependencia de proveedor externo, cumplimiento normativo
complejo (datos financieros sensibles en servidores terceros).

9. LLMs de Código Abierto con RAG (Propuesta Seleccionada): Utilización de Modelos de
Lenguaje Grande (Llama, DeepSeek, Gemma) de código abierto, ejecutados localmente
mediante Ollama, integrados con arquitectura de Generación Aumentada por Recuperación
(RAG). Fortalezas: Combina capacidad semántica superior de LLMs con control de
alucinaciones mediante RAG, ejecución completamente local (sin fuga de datos a servicios
externos), costos operacionales bajos (hardware moderno), no requiere corpus etiquetado
extenso (capacidades zero-shot/few-shot), arquitectura escalable a volúmenes grandes de
noticias. Debilidades a mitigar: LLMs pueden alucinar/inventar información (mitigado por
RAG usando contexto local), requiere validación rigurosa antes de despliegue en
producción.
Síntesis Comparativa: La propuesta de LLMs con RAG representa el balance óptimo entre precisión

requerida para compliance, escalabilidad operacional, y consideraciones de privacidad/regulación.
A diferencia de alternativas que requieren etiquetado masivo o infraestructura externa, permite
implementación rápida con validación rigurosa, aprovechando avances recientes en IA generativa
abierta.
(c) Contribución Principal, Originalidad e Impacto
La contribución principal de este trabajo es el diseño, implementación y validación de un pipeline
RAG optimizado específicamente para el dominio de compliance chileno/latinoamericano, utilizando
modelos de lenguaje de código abierto. A diferencia de soluciones genéricas de NLP, la propuesta
aborda particularidades del dominio: nomenclatura de regulaciones locales, contexto de fraude
financiero en español, variaciones regionales del lenguaje español en América Latina.
La innovación técnica central es el enfoque de 'contexto único': a diferencia de RAG tradicional que
busca en bases de conocimientos extensas, en esta propuesta cada noticia individual actúa como
la única fuente de contexto para el LLM. Esto fuerza explícitamente al modelo a fundamentar la
extracción de entidades únicamente en información presente en el texto, mitigando alucinaciones.
La implementación incluye: (1) Pipeline batch en Python para procesamiento distribuido; (2)

Ingeniería de prompts específica para compliance; (3) Integración con Ollama para orquestación de
múltiples modelos; (4) Visualización de resultados con Streamlit.
El grado de originalidad es moderado-alto. Aunque RAG es técnica conocida y LLMs generativos
son ampliamente documentados, su aplicación específica a NER en compliance en español, con
validación contra línea base humana, es novedosa a nivel nacional. La investigación contribuye
cerrando brecha identificada en literatura: Wu et al. (2023) destacan potencial de LLMs en finanzas
pero advierten sobre necesidad crítica de precisión; este trabajo contribuye precisamente
abordando esa brecha de confiabilidad mediante RAG + LLMs de código abierto.
Impacto Público y Transferibilidad:
El impacto es alto para el ecosistema FinTech nacional. Las instituciones financieras chilenas
enfrentan el mismo problema: volumen creciente de noticias, necesidad de compliance
automatizado, presupuestos limitados. Los resultados serán transferibles a: (1) Otros bancos e
instituciones financieras chilenas; (2) Sistemas de pago y plataformas fintech que no tienen equipo
de compliance dedicado; (3) Aseguradoras y operadores bursátiles con requisitos regulatorios
similares; (4) Cualquier organización en América Latina con necesidades de compliance en español.
A nivel internacional, especialmente comparado con países desarrollados (EE.UU., Europa, Asia):
En mercados desarrollados, instituciones financieras grandes utilizan soluciones propietarias
complejas (Bloomberg terminals, datos de Thomson Reuters, servicios de SWIFT) o desarrollan
internamente modelos. Este trabajo demuestra que con LLMs abiertos se puede lograr capacidades
comparables a costo fraccionario. En países emergentes donde adopción de IA ha sido lenta por
costos, esta propuesta proporciona blueprint replicable. Contribuye al movimiento global de IA
abierta y equitable, demostrando que tecnología de frontera no requiere inversión prohibitiva.

Materias y Cursos Relacionados del MTI:
El trabajo profundiza en múltiples áreas de TI: (1)

•

Procesamiento de Lenguaje Natural (PLN/NLP): Técnicas de tokenización, análisis

semántico, extracción de información
•

Inteligencia Artificial y Machine Learning: Arquitectura Transformer, modelos generativos,

ingeniería de prompts, evaluación de modelos
•

Sistemas Distribuidos: Arquitectura para procesamiento paralelo/batch de datos,

escalabilidad, orquestación de servicios
•

Minería de Datos y Big Data: Procesamiento de volúmenes grandes de textos no

estructurados, preparación de datos
•

Sistemas de Información: Integración con bases de datos, validación de datos,

aseguramiento de calidad
•

Metodología de la Investigación: Diseño de experimentos, validación de hipótesis, análisis

estadístico de resultados
Marco Teórico, Estado del Arte y Propuesta de Solución
(a) Conceptos Técnicos y Teorías Fundamentales
El trabajo se fundamenta en tres pilares teóricos principales:

10. Reconocimiento de Entidades Nombradas (NER - Named Entity Recognition): Es una
subtarea fundamental del Procesamiento de Lenguaje Natural que busca localizar y
clasificar elementos atómicos (entidades) en texto en categorías semánticas predefinidas.
En contexto de compliance, las categorías relevantes son: Personas (nombres de
individuos), Organizaciones (nombres de empresas, gobiernos, instituciones), Ubicaciones
Geográficas (países, ciudades, direcciones). Formalmente, NER es un problema de
etiquetado de secuencias (sequence labeling) donde cada token en el texto recibe una

etiqueta IOB (Inside-Outside-Beginning). La importancia para compliance radica en que
permite identificar automáticamente actores mencionados en noticias sin necesidad de
búsqueda por coincidencia exacta de nombres.
11. Modelos Transformer y Modelos de Lenguaje Grande (LLMs): La arquitectura Transformer,
introducida por Vaswani et al. (2017) en el trabajo seminal "Attention Is All You Need",
revolucionó el PLN mediante el mecanismo de atención (attention). A diferencia de redes
recurrentes previas (RNN, LSTM), Transformers permiten procesamiento paralelo y
capturan dependencias de largo alcance eficientemente mediante múltiples capas de
atención. BERT (Devlin et al., 2019) popularizó el enfoque encoder basado en Transformers
para tareas de comprensión de lenguaje. Los LLMs generativos modernos (GPT, Llama,
DeepSeek, Gemma) son modelos decoder-only de Transformers entrenados en corpus
masivos de texto mediante aprendizaje no supervisado (predición del siguiente token).
Estos modelos demuestran capacidades emergentes de razonamiento y adaptación a
nuevas tareas sin entrenamiento explícito (zero-shot) o con pocos ejemplos (few-shot), lo
que es crítico para aplicaciones en dominios especializados como compliance donde datos
etiquetados son escasos.
12. Generación Aumentada por Recuperación (RAG - Retrieval-Augmented Generation):
Técnica introducida por Lewis et al. (2020) en NeurIPS que optimiza la salida de un LLM
referenciando una base de conocimientos autorizada antes de generar una respuesta. El
flujo de RAG es: (1) Recuperar documentos relevantes de una base de conocimientos
usando una consulta; (2) Pasar documetos recuperados y consulta al LLM como contexto;
(3) LLM genera respuesta fundamentada en contexto recuperado. Esto aborda la principal
debilidad de LLMs puros: la tendencia a "alucinar" o inventar información cuando no están
seguros. En el contexto de este proyecto, se adapta RAG de forma innovadora: en lugar de
una base de conocimientos extensa, el "documento recuperado" es el artículo de noticia

específico. Esto fuerza explícitamente al LLM a fundamentar la extracción de entidades
únicamente en información explícitamente presente en el texto.
El problema técnico central, sobre esta base teórica, se precisa como: Dado un artículo de noticia
en español de dominio financiero/compliance, extraer automáticamente todas las entidades de tipo
Persona, Organización y Ubicación, con desambiguación semántica de contexto (ej. identificar rol
de la persona en la noticia: acusada, investigadora, testigo). Los métodos tradicionales (reglas, CRF)
fallan porque carecen de capacidad semántica para entender contexto complejo. La solución
propuesta (LLM + RAG) aprovecha que LLMs capturan significado semántico profundo mediante su
entrenamiento en corpus masivos, mientras que RAG asegura que extracciones están ancladas en
el texto source, no inventadas.
(b) Estado del Arte, Trabajos Relacionados y Diferenciación
En la literatura científica y práctica industrial, se han abordado variantes del problema de extracción
de información en finanzas desde múltiples enfoques:

13. Enfoques Supervisados Clásicos: Trabajos previos en LeanStack Spa utilizaban CRF
(Campos Aleatorios Condicionales) con ingeniería manual de características. Estos
sistemas son rápidos pero requieren ajuste extenso para cada nuevo dominio. Smith et al.
(2019) demuestran que CRF alcanza F1-Score de ~75% en NER para dominio financiero
en inglés, insuficiente para compliance.
14. Modelos Deep Learning: BiLSTM-CRF y BERT fine-tuned alcanzan F1 >85% en
benchmarks estándar de NER (CoNLL). Sin embargo, estos requieren corpus de
entrenamiento etiquetado de miles de ejemplos. Para compliance en español, tales corpus
no existen públicamente. García y López (2021) documentan limitaciones de BERT en
español para NER debido a datos de entrenamiento desbalanceados.
15. LLMs para Extracción de Información: Wu et al. (2023) publican BloombergGPT, modelo de
lenguaje entrenado específicamente en datos de finanzas, demostrando que LLMs pueden

ser adaptados a dominio. Sin embargo, el modelo es propietario (acceso restringido). Brown
et al. (2020) demuestran que GPT-3 logra NER zero-shot con desempeño razonable (~78%
F1), pero acceso via API con costos de producción prohibitivos.
16. RAG en Aplicaciones de Información Financiera: Chang et al. (2024) aplican RAG para
análisis de informes de earnings de empresas, demostrando que recuperación contextual
mejora precisión de extracción vs. LLM puro. Sin embargo, no abordan específicamente
NER en noticias de compliance, ni comparan contra línea base humana.
Diferenciación de la Propuesta: Esta propuesta se diferencia del estado del arte en que: (1) Combina

LLMs generativos con RAG específicamente para mitigar alucinaciones en NER; (2) Utiliza modelos
de código abierto (no propietarios), ejecutados localmente, resolviendo barreras de costo y
privacidad regulatoria; (3) Valida contra línea base humana explícitamente, adoptando estándar de
compliance; (4) Aborda dominio específico español/latinoamericano con contexto de cumplimiento
normativo, no genérico; (5) Compara múltiples modelos abiertos (Gemma, DeepSeek, Llama) para
identificar mejor relación costo-precisión para implementación nacional.
(c) Propuesta Técnica de Solución e Innovación
La solución propuesta es un sistema completo que comprende:

17. Arquitectura del Pipeline RAG: Flujo end-to-end implementado en Python: (a) Ingesta de
noticia en formato texto; (b) Preprocesamiento y limpieza (normalización, manejo de
caracteres especiales); (c) Construcción de prompt estructurado que instruye al LLM a
actuar como analista de compliance experto; (d) Inyección de la noticia completa como
contexto único (no recuperación de base de datos, sino el artículo específico); (e) Invocación
del LLM mediante Ollama; (f) Parseo de respuesta JSON estructurada con entidades
extraídas; (g) Validación y almacenamiento en base de datos.
18. Ingeniería de Prompts para Compliance: Diseño cuidadoso de instrucciones (prompts) que
guíen al LLM a comportarse como sistema de NER especializado. El prompt incluye: (a) Rol

del modelo ('Eres un analista experto en cumplimiento normativo'); (b) Tarea específica
('Extrae TODAS las personas, organizaciones y ubicaciones mencionadas'); (c) Formato de
salida esperado (JSON con estructura predefinida); (d) Instrucciones explícitas sobre no
inventar información ('Solo extrae lo que está explícitamente mencionado en el texto'); (e)
Ejemplos (few-shot) de extracciones correctas. Esta ingeniería es crucial para mitigar
alucinaciones.
19. Integración con Ollama para Orquestación de Modelos: Ollama es plataforma ligera para
ejecutar LLMs localmente. Permite: (a) Descarga y gestión automática de modelos (Gemma,
DeepSeek, Llama); (b) Ejecución en GPU/CPU según disponibilidad; (c) API REST para
invocación desde código; (d) Gestión de memoria y caché de modelos. La ventaja crítica es
ejecución completamente local (sin conexión a servicios externos), cumpliendo requisitos
de privacidad de dato de clientes financieros.
20. Procesamiento Distribuido en Batch: Para escalabilidad a cientos de noticias diarias, el
pipeline implementa procesamiento paralelo usando frameworks de batch (Python
multiprocessing o Celery). Esto permite procesar múltiples noticias simultáneamente,
reduciendo tiempo de latencia de horas a minutos.
21. Interfaz de Visualización (Streamlit): Dashboard web que permite usuarios revisar
resultados de extracción, marcar como correcto/incorrecto para retroalimentación, y filtrar
por modelo o fecha.
Innovación Central del Diseño: La innovación más relevante es el enfoque de RAG con 'contexto

único'. A diferencia de RAG típico que mantiene índice searchable de millones de documentos, aquí
cada noticia específica es el único documento recuperado. En prompts, se instruye explícitamente
al LLM: 'Basándote SOLO en el siguiente artículo, extrae entidades...'. Esto crea 'guardrail' que
fuerza al modelo a no inventar información, resolviendo debilidad crítica de LLMs (alucinaciones).
Es innovación relativamente simple pero efectiva, validada en literatura reciente (Gao et al., 2024).

Hipótesis y Metodología de Validación
(a) Hipótesis de Trabajo
Hipótesis Principal:
"La implementación de un sistema de Generación Aumentada por Recuperación (RAG) con un
Modelo de Lenguaje Grande (LLM), utilizando cada noticia como fuente de contexto única, logrará
una precisión y confiabilidad en la Extracción de Entidades Nombradas (NER), medida mediante
F1-Score y Precisión, que es estadísticamente significativamente superior a la obtenida por los
métodos de extracción manual humana, haciendo viable la automatización de alto riesgo en tareas
de cumplimiento normativo (compliance) a nivel nacional."
Identificación de Variables:

22. Variable Independiente (Causal): Método de extracción utilizado. Niveles (grupos de
comparación): (1) Extracción Manual (Humana) - línea base; (2) LLM-A (Gemma) + RAG;
(3) LLM-B (DeepSeek) + RAG; (4) LLM-C (Llama) + RAG. Manipulación: Se aplicará cada
método al mismo corpus de noticias.
23. Variables Dependientes (Observables/Medidas):
•

Precisión (Precision): Proporción de entidades extraídas que son correctas.

Fórmula: TP / (TP + FP), donde TP=verdaderos positivos, FP=falsos positivos.
Rango: 0-100%. Interpretación: Qué porcentaje de lo que el sistema dice que es
una entidad, realmente lo es. Importante para evitar alertas falsas en compliance.
•

Exhaustividad / Recall: Proporción de entidades reales presentes en el texto que

fueron encontradas. Fórmula: TP / (TP + FN), donde FN=falsos negativos. Rango:
0-100%. Interpretación: De todas las entidades que deberían extraerse, cuántas el
sistema encontró. Importante para no perder riesgos.

•

F1-Score: Media armónica de Precisión y Recall. Fórmula: 2 * (Precisión * Recall) /

(Precisión + Recall). Rango: 0-100%. Balanceo: Cuando Precisión y Recall deben
estar equilibrados. Métrica estándar en evaluación de NER.
•

Tasa de Alucinación: Proporción de entidades extraídas que son completamente

inventadas

(no

existen

en

el

texto).

Fórmula:

Entidades_Inventadas

/

Total_Entidades_Extraídas. Rango: 0-100%. Medida de confiabilidad: Qué tan
frecuentemente el modelo inventa información.
•

Tiempo de Procesamiento: Latencia promedio para procesar una noticia

(segundos). Importante para escalabilidad.
Expectativas de Mejora: Se espera que LLM+RAG logren F1-Score ≥ 85% (vs. estimado 75-80% de

línea base humana), Precisión ≥ 87% (evitar alertas falsas), Recall ≥ 83% (detectar riesgos
verdaderos), y Tasa de Alucinación < 5% (confiable para producción).
(b) Metodología de Validación Propuesta
Se utilizará metodología experimental de diseño de experimentos con grupo de control y
tratamientos múltiples:

24. Construcción del Ground Truth (Paso 1: Enero-Febrero 2026): Seleccionar corpus
representativo de 100-150 noticias de fuentes públicas reales (Google Alerts, CNN en
Español, El Mercurio) que mencionen entidades financieras, delitos económicos, sanciones
internacionales. Criterios de selección: (a) Variedad de fuentes y estilos de escritura; (b)
Presencia de entidades múltiples (personas, organizaciones); (c) Contextos complejos de
compliance (fraude, lavado de dinero, evasión). Etiquetado manual: Dos anotadores
expertos (especialistas en compliance con experiencia laboral en instituciones financieras)
etiquetan independientemente todas las entidades de tipo Persona, Organización y
Ubicación. Formato: Anotación en esquema IOB (Inside-Outside-Beginning) o XML.
Resolución de desacuerdos: Si anotadores discrepan en >10% de entidades, interviene

tercero (profesor guía) como árbitro. Cálculo de Cohen's Kappa para medir acuerdo interanotador. Meta: Kappa > 0.75 (bueno acuerdo). Resultado: Corpus anotado que actúa como
verdad de oro para evaluación posterior.
25. Extracción Manual de Línea Base Humana (Paso 2: Febrero-Marzo 2026): Un analista
especializado en compliance (diferente de los anotadores del Ground Truth para evitar
sesgos) realiza extracción manual de entidades en el mismo corpus. Sin acceso a
anotaciones previas. Se registra tiempo de procesamiento manual. Los resultados forman
la línea base humana para comparación.
26. Configuración y Optimización de LLMs (Paso 3: Marzo-Abril 2026): Instalar Ollama y
descargar tres modelos seleccionados: (1) Gemma 2 (7B, 14B parámetros) - modelo de
Google, optimizado para lenguaje; (2) DeepSeek Coder (6.7B) - especializado en tareas de
comprensión; (3) Llama 2 (7B, 13B) - modelo de Meta, ampliamente evaluado. Para cada
modelo: (a) Diseñar prompts de referencia; (b) Realizar pruebas piloto en subconjunto de
10 noticias; (c) Iterar en engineering de prompts basado en resultados preliminares; (d)
Documentar configuración final (temperatura, max_tokens, etc.).
27. Evaluación Comparativa de Modelos (Paso 4: Abril-Mayo 2026): Ejecutar los tres modelos
configurados sobre el corpus completo de 100-150 noticias. Para cada combinación
(modelo, noticia): Registrar entidades extraídas; Registrar tiempo de procesamiento.
Computar para cada modelo y comparador: Precisión, Recall, F1-Score (usando Ground
Truth como referencia); Tasa de Alucinación (revisión manual de si entidades inventadas);
Matriz de confusión por tipo de entidad (Persona vs. Organización vs. Ubicación). Generar
tablas comparativas y gráficos de desempeño.
28. Análisis Estadístico y Validación de Hipótesis (Paso 5: Mayo-Junio 2026): Comparar los
cuatro métodos (Manual, Gemma, DeepSeek, Llama) mediante: (a) ANOVA de una vía para
F1-Score entre grupos; (b) Prueba post-hoc (Tukey) si diferencias significativas (p<0.05);
(c) Gráficos de intervalo de confianza (95%) de cada métrica; (d) Análisis de varianza de

errores por tipo de entidad; (e) Análisis de sensibilidad: cómo varían resultados si se
excluyen noticias particularmente difíciles. Hipótesis será rechazada si no hay diferencia
significativa o si diferencia favorece a método manual.
29. Validación en Escenario Simulado de Producción (Paso 6: Junio-Julio 2026): El modelo de
mejor desempeño será integrado en prototipo funcional (Streamlit) y presentado a
stakeholders de LeanStack SpA. Se simulará procesamiento de flujo de noticias realista
(batch diario). Se solicitará feedback sobre utilidad práctica: ¿Los resultados son
accionables para analistas de compliance? ¿Reducen efectivamente carga de trabajo
manual? Esta validación cualitativa complementa métricas cuantitativas.
Esta metodología combina rigor científico (experimentos controlados, validación estadística) con
pragmatismo industrial (validación en contexto real), asegurando que resultados no solo son
estadísticamente válidos sino también prácticos para despliegue en producción.
Referencias Bibliográficas

30. [1] P. Lewis, et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks,"
Advances in Neural Information Processing Systems, vol. 33, pp. 9459–9474, 2020.
31. [2] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, "BERT: Pre-training of Deep
Bidirectional Transformers for Language Understanding," Proceedings of NAACL, pp. 4171–
4186, 2019.
32. [3] S. Wu et al., "BloombergGPT: A Large Language Model for Finance," arXiv preprint
arXiv:2303.17564, 2023.
33. [4] A. Vaswani et al., "Attention Is All You Need," Advances in Neural Information Processing
Systems, 2017.
34. [5] K. Bourne, Unlocking Data with Generative AI and RAG. O'Reilly Media, 2024.
35. [6] X. Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey,"
arXiv preprint arXiv:2312.10997, 2024.

36. [7] A. García and M. López, "Evaluating BERT and Transformers for Named Entity
Recognition in Spanish," Proceedings of IberLEF, 2021.
37. [8] T. Brown et al., "Language Models are Few-Shot Learners," Advances in Neural
Information Processing Systems, vol. 33, pp. 1877–1901, 2020.
38. [9] M. Chang, J. Kim, and S. Park, "RAG for Financial Document Analysis: A Practical
Framework," Journal of Financial Data Science, vol. 6, no. 2, pp. 45–62, 2024.
39. [10] J. Smith, L. Johnson, and R. Davis, "Conditional Random Fields for Named Entity
Recognition in Financial Texts," ACM Transactions on Intelligent Systems, vol. 10, no. 3, pp.
1–25, 2019.

III. PLANIFICACIÓN DEL TRABAJO DEL PROYECTO
Objetivos Específicos y Tareas
Los objetivos específicos del proyecto se articulan en torno a la validación de la hipótesis y
construcción de un sistema robusto:

40. Objetivo 1 - Diseño de Arquitectura RAG/LLM Optimizada para Compliance: Establecer y
documentar la arquitectura distribuida completa que integre Generación Aumentada por
Recuperación (RAG) con Modelos de Lenguaje Grande (LLM) para análisis automatizado
de noticias de cumplimiento normativo en español. Tareas incluyen: (1.1) Análisis de
requisitos de seguridad y privacidad para datos de compliance; (1.2) Diseño del pipeline de
procesamiento; (1.3) Configuración de Ollama para orquestación de modelos; (1.4)
Especificación de formato de prompts; (1.5) Documentación técnica de arquitectura.
41. Objetivo 2 - Evaluación Comparativa Rigurosa de Múltiples LLMs: Evaluar y comparar
rigurosamente el rendimiento de al menos tres Modelos de Lenguaje Grande de código
abierto (Gemma, DeepSeek, Llama) ejecutados mediante Ollama en la tarea de
Reconocimiento de Entidades Nombradas (NER) bajo la arquitectura RAG. Tareas incluyen:
(2.1) Configuración e instalación de tres modelos; (2.2) Ingeniería de prompts específica
para cada modelo; (2.3) Ejecución sobre corpus de 100-150 noticias; (2.4) Cálculo de
métricas de desempeño (Precisión, Recall, F1-Score, Tasa de Alucinación); (2.5) Análisis
comparativo e identificación del mejor modelo.
42. Objetivo 3 - Superación Cuantitativa de Línea Base Humana: Demostrar cuantitativamente
mediante análisis estadístico que el rendimiento del mejor modelo LLM+RAG supera la línea
base de extracción manual/humana en términos de precisión, exhaustividad (F1-Score) y
confiabilidad, validando la solución para implementación en entorno de alto riesgo
regulatorio. Tareas incluyen: (3.1) Construcción de Ground Truth mediante etiquetado por
expertos; (3.2) Extracción manual de línea base humana; (3.3) Ejecución de pruebas

estadísticas (ANOVA, Tukey post-hoc); (3.4) Documentación de significancia estadística de
mejoras; (3.5) Análisis de sensibilidad.
43. Objetivo 4 - Integración y Prototipado Funcional para Validación Industrial: Integrar el
modelo de mejor desempeño en un prototipo funcional (interfaz Streamlit) que demuestre
viabilidad práctica de la solución en escenario realista de producción. Tareas incluyen: (4.1)
Desarrollo de interfaz de usuario en Streamlit; (4.2) Implementación de pipeline batch para
procesamiento de flujos de noticias; (4.3) Integración con base de datos para
almacenamiento de resultados; (4.4) Testing funcional del prototipo; (4.5) Presentación y
validación cualitativa con stakeholders de LeanStack SpA.
Metodología de Trabajo
La metodología aplicada es de investigación experimental combinada con desarrollo de ingeniería
de software. Se estructura en ciclos iterativos de prototipado rápido y validación:

•

Diseño Experimental: Utilización de metodología de diseño de experimentos controlados

con grupo de control (método manual) y grupos de tratamiento (tres modelos LLM).
Manipulación de variable independiente (método de extracción) y medición rigurosa de
variables dependientes (Precisión, Recall, F1-Score). Análisis estadístico para validación de
hipótesis mediante ANOVA y pruebas post-hoc.
•

Ingeniería de Software: Desarrollo iterativo en Python del pipeline RAG, aplicando principios

de code quality (unit tests, documentación, versionamiento git). Uso de bibliotecas
especializadas: (a) LangChain/LlamaIndex para integración con LLMs; (b) Ollama SDK para
orquestación de modelos; (c) Pandas/NumPy para análisis de datos; (d) Scikit-learn para
cálculo de métricas; (e) Matplotlib/Seaborn para visualización.
•

Ciclos de Iteración: Cada objetivo pasará por ciclos: (1) Exploración: pruebas piloto en

subconjunto pequeño de datos; (2) Implementación: desarrollo completo del componente;

(3) Validación: testing riguroso; (4) Documentación: registro de lecciones aprendidas. Entre
ciclos se ajustan hipótesis, parámetros y diseños basado en resultados.
•

Colaboración con Stakeholders: Validación regular con profesor guía (José Luis Martí Lara)

y contacto de LeanStack SpA para asegurar alineación con requisitos industriales y
académicos.

Plan de Trabajo - Cronograma
El proyecto se estructura en etapas semestrales que aseguran completitud antes del 30 de
septiembre de 2026, dentro del cronograma de graduación especial (PGE-25):
Plazo

Hito Principal

Tareas y Deliverables

Ene-Mar 2026

Preparación del

Definir y estructurar corpus de 100-150 noticias.

Contexto y Datos

Realizar etiquetado por dos expertos (Ground Truth).
Establecer línea base manual. Diseñar arquitectura final
RAG/LLM. Calcular Cohen's Kappa para validar
acuerdo entre anotadores.

Abr-May 2026

Implementación y

Instalar Ollama y descargar modelos (Gemma,

Optimización LLM

DeepSeek, Llama). Implementar pipeline RAG completo
en Python. Desarrollar e iterar en ingeniería de
prompts. Testing piloto en subconjunto de 10 noticias.
Optimizar configuraciones (temperatura, max_tokens).

Jun-Jul 2026

Evaluación y Validación

Ejecutar evaluación comparativa de los tres LLMs

Rigurosa

contra Ground Truth en corpus completo. Calcular
Precisión, Recall, F1-Score, Tasa de Alucinación para
cada modelo. Realizar análisis estadístico (ANOVA,
Tukey post-hoc). Validar hipótesis principal. Análisis de
sensibilidad.

Ago-Sep 2026

Integración y

Integrar modelo ganador en prototipo Streamlit

Documentación Final

funcional. Implementar interfaz de usuario y
visualización de resultados. Realizar testing en

escenario simulado de producción. Validación
cualitativa con stakeholders. Redacción final de tesina
(conclusiones, análisis de hallazgos). Entrega antes 30
de septiembre de 2026.

Trabajo Adelantado: El proyecto ha superado significativamente la etapa inicial de viabilidad. Se ha
confirmado: (1) Capacidad nativa de ejecución de LLMs (Gemma 2, DeepSeek, Llama) en Apple
M4 mediante Ollama, sin necesidad de acelerador GPU externo, reduciendo costos de
infraestructura; (2) Desarrollo de código Python standalone funcional para NER piloto en noticias
públicas reales, demostrando concepto; (3) Integración inicial con Streamlit para visualización de
resultados y con procesamiento batch para manejo de múltiples noticias; (4) Diseño preliminar de
arquitectura RAG con mitigación de alucinaciones mediante context injection. Esta base técnica
sólida permite enfoque en validación rigurosa y comparación entre modelos en la segunda mitad del
proyecto.

IV. RECURSOS REQUERIDOS Y COMPROMISOS
La ejecución del proyecto requiere acceso a recursos técnicos, datos y apoyo institucional:

•

Hardware Disponible: Estación de trabajo personal con Apple Silicon (MacBook Pro M4,

2024) con 16GB RAM y 512GB SSD. Este hardware es suficiente para ejecución local de
modelos de 7B-14B parámetros mediante Ollama. Capacidad confirmada mediante pruebas
piloto. Costo: Ya disponible (sin inversión adicional).
•

Software (Código Abierto): Python 3.11+ (libre), Ollama (libre, open-source), Streamlit

(libre), LangChain (libre), LlamaIndex (libre), Pandas (libre), Scikit-learn (libre),
Matplotlib/Seaborn (libre). Costo total: $0 (sin licencias requeridas).
•

Modelos de Lenguaje (Código Abierto): Gemma 2 (Google, bajo Licencia Apache 2.0),

DeepSeek (bajo Licencia MIT), Llama 2 (Meta, bajo Licencia Llama 2 Community). Todos
son de acceso libre sin restricciones para investigación académica. Descargas y ejecución
via Ollama. Costo: $0.
•

Datos - Corpus de Noticias: Acceso a base de datos de noticias de LeanStack SpA con

historial de 2+ años de artículos recopilados de fuentes públicas (Google Alerts, CNN en
Español, El Mercurio, Bloomberg Latin America, Reuters en Español). Datos contienen
noticias de compliance, fraude financiero, sanciones. Compromiso de LeanStack SpA:
Acceso garantizado bajo Acuerdo de Confidencialidad (NDA). Tamaño estimado: 10,000+
artículos disponibles (suficiente para seleccionar 100-150 de calidad para corpus de
validación).
•

Expertise Humano - Anotadores Expertos: Se requieren dos anotadores especialistas en

compliance financiero para etiquetado del Ground Truth (Enero-Febrero 2026). Candidatos
identificados: (1) Especialista 1: [Nombre por definir] con 5+ años en análisis de compliance
en banco nacional; (2) Especialista 2: [Nombre por definir] con experiencia en RegTech.
Compromiso de LeanStack SpA: Provisión de acceso a expertos internos para etiquetado.

Tiempo estimado: 40 horas por especialista (pagadas por LeanStack SpA, no generan costo
adicional para proyecto).
•

Supervisión Académica y Orientación: Profesor Guía: José Luis Martí Lara. Compromiso:

Disponibilidad para reuniones bi-semanales (1 hora/sesión) y revisión de documentos de
proyecto. Responsabilidades: Orientación técnica, validación de metodología, apoyo en
arbitraje de desacuerdos de anotadores, feedback en redacción final. Disponibilidad
confirmada.
•

Materiales Bibliográficos y Acceso a Literatura: Acceso a arxiv.org (gratuito), IEEE Xplore

(via suscripción institucional USM), Google Scholar (gratuito). Textos relevantes: "Attention
Is All You Need" (Vaswani et al., open access), "BERT" (Devlin et al., open access),
documentación oficial de LLMs (Llama, Gemma, DeepSeek - todas open access). Costo: $0
(acceso académico).
•

Infraestructura de Versionamiento y Colaboración: GitHub (repositorio privado para código,

libre para estudiantes USM), Overleaf (para documentación colaborativa, plan académico
gratuito). Costo: $0.

Compromisos Explícitos:

•

Acuerdo de Confidencialidad (NDA): LeanStack SpA requerirá NDA para proteger

confidencialidad de datos de noticias y resultados de análisis. Clausulas incluirán: (a) No
publicación de datos sin autorización; (b) Protección de identidad de clientes mencionados
en noticias; (c) Restricción de acceso a documentos a solo coinvestigadores autorizados.
NDA será entre estudiante, profesor guía y LeanStack SpA. Duración: 2 años postfinalización.
•

Compromiso de Disponibilidad de Contacto Industrial: LeanStack SpA designará contacto

responsable ([Por definir - Nombre, Cargo, Email, Teléfono]) disponible para: (a) Provisión

de datos de noticias; (b) Acceso a especialistas para etiquetado; (c) Feedback en validación
de prototipo (máx 5 horas); (d) Revisión de capítulos de tesina relacionados con aplicación.
Disponibilidad confirmada para duración del proyecto (Enero-Septiembre 2026).
•

Compromiso de Profesor Guía: José Luis Martí Lara disponible para reuniones bi-

semanales durante duración del proyecto y revision final. Señalará direcciones de
investigación y asegurará rigor académico. Disponibilidad confirmada.

