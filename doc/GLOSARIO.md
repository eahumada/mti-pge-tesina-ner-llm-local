# Glosario del estudio

Definiciones de referencia de los términos técnicos empleados en la tesina y en su desarrollo. Es un
documento de trabajo del proyecto —como `FINDINGS.md` o `LEARNING.md`—, no uno de los entregables
finales listados en `CLAUDE.md`; su propósito es fijar un uso consistente del vocabulario a lo largo
del informe, los anexos y los documentos de seguimiento, y servir de referencia rápida para quien
retome el trabajo. Si el autor decide incorporarlo como anexo del informe, es una decisión aparte
que este documento no da por hecha.

Cada entrada remite a la sección del informe donde el término se introduce o se usa con más detalle
(`§` para el Informe Final de Tesina, `Anexo` para sus anexos), y a la referencia bibliográfica
cuando el informe cita una. Las definiciones siguen la redacción del informe; no son una fuente
independiente.

---

## A. Entidades, categorías y evaluación

**NER (Reconocimiento de Entidades Nombradas).** Subtarea del Procesamiento de Lenguaje Natural que
localiza fragmentos de texto y los clasifica en categorías semánticas predefinidas. §2.1.

**PER, ORG, LOC.** Las tres categorías de entidad que este trabajo evalúa: **Personas** (PER),
**Organizaciones** (ORG) y **Ubicaciones** (LOC). Son las que permiten cotejar una noticia contra
listas de sanciones [19] y de personas políticamente expuestas [38]. §2.1.

**Localizaciones / Ubicaciones (LOC).** El informe usa **«Ubicaciones»** en su primera mención
(§2.1) y **«localizaciones»** en el resto del texto (§3.3, Anexo H, Anexo I) para la misma
categoría — una inconsistencia terminológica menor, no corregida, documentada como candidata en
`LEARNING.md §L80` (punto 4).

Sobre el corpus real (`data/benchmark_balanced_120.json`), la categoría anota **545 entidades**
(339 valores únicos) que son mayoritariamente **topónimos** a distintas escalas — países
(`España`, `Francia`, `Alemania`, `Marruecos`), comunidades autónomas (`Andalucía`, `Cataluña`,
`Galicia`, `Asturias`) y ciudades (`Madrid`, `Bilbao`, `Sevilla`, `Toledo`, `Córdoba`) — pero
**también incluye lugares institucionales** que no son topónimos en sentido estricto: `Universidad
de Deusto`, `Universidad del País Vasco`, `Hospital Virgen del Rocío`, `Palacio de la Moncloa`,
`Palacio de la Magdalena`, `Forum Deusto`, `Museo Extremeño e Iberoamericano de Arte Contemporáneo`.
No se observan direcciones postales (calle y número) en ningún ejemplo del corpus.

Esa composición mixta es relevante para elegir el nombre de la categoría: **«topónimos»** describiría
con precisión la mayoría de los casos pero dejaría fuera los lugares institucionales; **«ubicaciones»**
los cubre a todos, con el coste de ser un término más genérico; **«direcciones»** no encaja con
ningún ejemplo real del corpus y sería la opción menos apropiada de las tres que se barajaron.
**Candidato a decidir con el profesor guía**, no ejecutado: cuál de los términos usar de forma
consistente en todo el informe (hoy conviven dos). Ver `LEARNING.md §L80`.

**IOB2.** Esquema de etiquetado de secuencias que distingue el inicio de una entidad (*Beginning*),
su continuación (*Inside*) y el texto ajeno a toda entidad (*Outside*). Heredado de la tarea
compartida CoNLL-2002 [12]. §2.1.

**Emparejamiento difuso / distancia de Indel.** Criterio de coincidencia entre una entidad extraída
y la de referencia, implementado con la función `ratio` de RapidFuzz [33]. La distancia de Indel es
el número mínimo de inserciones y supresiones para transformar una cadena en otra —una variante de
la distancia de Levenshtein que excluye las sustituciones—, normalizada a una escala de 0 a 100. Se
acepta como acierto una similitud ≥ **85**. Es sensible al orden de las palabras y penaliza las
omisiones proporcionalmente a la longitud. §2.1, §3.3.

**Tasa de alucinación.** Métrica que no compara con la anotación de referencia sino con el **texto
de origen**: una entidad se considera alucinada si no aparece literalmente en el artículo y su mejor
similitud contra las ventanas deslizantes del texto queda por debajo de **70** (umbral más laxo que
el 85 del emparejamiento). Una entidad correcta pero ausente de la referencia es falso positivo, no
alucinación. §3.3.

**F1, precisión, exhaustividad (*recall*).** Las tres métricas de desempeño estándar de NER,
calculadas por artículo y promediadas. F1 es la media armónica de precisión y exhaustividad; nunca
puede superar la media aritmética de ambas, propiedad que el verificador del informe comprueba fila
por fila. §3.3, §5.

---

## B. Modelos de lenguaje y aprendizaje en contexto

**LLM (modelo de lenguaje grande).** En este trabajo, modelos *decoder-only* ejecutados en local vía
Ollama, evaluados sin ajuste de pesos. §2.1, §2.2.

**Aprendizaje en contexto (*in-context learning*).** Capacidad de adaptar el comportamiento de un
LLM mediante instrucciones y ejemplos incluidos en el propio *prompt*, sin reentrenar el modelo [8].
§2.2.

**Zero-shot / few-shot.** Dos regímenes de *prompt*: en zero-shot el *prompt* solo describe la tarea
y el formato de salida; en few-shot [8] se añaden ejemplos resueltos que fijan el patrón de
respuesta. §2.2.

***Chain-of-thought*.** Estrategia de razonamiento explícito paso a paso en el *prompt* [13],
concebida para tareas de inferencia en varios pasos; su pertinencia en NER (tarea de identificación,
no de deducción) se somete a comprobación empírica en este trabajo. §2.2.

**Cuantización.** Reducción de la precisión numérica de los pesos de un modelo para bajar el consumo
de memoria, típicamente a 4 bits (formato GGUF, esquema Q4_K_M [30]), con una pérdida de calidad
acotada frente al ahorro obtenido [20]. §2.3.

**Ollama, llama.cpp, MLX, vLLM, LM Studio.** Entornos de ejecución de inferencia local comparados en
§2.3: Ollama [29] encapsula llama.cpp [30] tras una API HTTP uniforme; MLX [31] aprovecha la memoria
unificada de Apple Silicon; vLLM [28] maximiza rendimiento por lotes en GPU dedicada; LM Studio
prioriza la interacción gráfica.

---

## C. Recuperación aumentada (RAG)

**RAG (*Retrieval-Augmented Generation*).** Fundamenta la generación en información recuperada en
tiempo de consulta en lugar de confiarla solo a los pesos del modelo [1], [5]. §2.3.

**RAG por diccionario (*dict-RAG*).** Variante que indexa catálogos de nombres conocidos e inyecta en
el *prompt* los más similares al texto; introduce sesgo de reconocimiento hacia lo catalogado. §2.3,
§5.6.

**RAG contextual / KB RAG (Base de Conocimientos).** Variante que recupera **criterios** —guías
tipológicas, definiciones de categoría, ejemplos anotados— en vez de entidades. §2.3, Anexo D.

**RAG de documento único.** Configuración que usa el propio documento como contexto único,
restringiendo la extracción al texto presente [9]. §2.3.

**Embeddings.** Representaciones vectoriales de longitud fija en las que textos semánticamente
próximos quedan cerca en el espacio vectorial, incluso sin compartir palabras. Reducen la búsqueda
de lo más relevante a una búsqueda por vecino más próximo. §2.3.

**Base de datos vectorial.** Índice que hace eficiente la búsqueda por vecino más próximo sobre
*embeddings* a la escala de miles de documentos candidatos; ChromaDB [32] en este trabajo. §2.3.

---

## D. Arquitectura de ejecución

**Publicador/suscriptor (*pub/sub*).** Arquitectura que desacopla la ingesta de artículos (que los
deposita en una cola) de su consumo (a cargo de un número variable de trabajadores), permitiendo
ajustar el paralelismo en tiempo de ejecución. §2.4.

**AIMD (*Additive Increase, Multiplicative Decrease*).** Política de control de concurrencia que
crece de a uno mientras el sistema permanece estable y recorta a la mitad ante la primera señal de
saturación; es la que sostiene el control de congestión en TCP [26]. §2.4, §3.2.

**Factory / Facade.** Patrones de diseño que aíslan el código llamador de las diferencias entre
proveedores de inferencia: Factory centraliza la construcción del proveedor correcto; Facade expone
una interfaz uniforme (`LLMProvider`) que oculta las diferencias de implementación. §2.4, Anexo A.1.

---

## E. Validación estadística

**ANOVA (análisis de varianza) de una vía [42].** Contrasta la hipótesis nula de que todos los
grupos comparados proceden de la misma población; indica que alguna diferencia existe, no cuál.
§2.5.

**Tukey HSD (*Honestly Significant Difference*) [25].** Prueba post-hoc que controla la tasa de
error por familia en comparaciones múltiples, sustituyendo la distribución t por la del rango
estudentizado. §2.5.

**Homocedasticidad.** Supuesto de que la varianza es homogénea entre los grupos comparados; se
contrasta con la prueba de Levene [44], en su variante centrada en la mediana (Brown-Forsythe [45]).
§2.5.

**Friedman [43].** Prueba no paramétrica de rangos, análoga al ANOVA de medidas repetidas cuando no
puede asumirse normalidad; sirve de control de robustez cuando el apareamiento de observaciones se
ignora. §2.5.

**Pearson [40] / Spearman [41].** Coeficientes de correlación entre dos variables. Pearson mide
asociación lineal y es sensible a valores atípicos; Spearman, calculado sobre los rangos, capta
cualquier relación monótona sin asumir linealidad. §2.5, Anexo J.

**d de Cohen [46].** Tamaño de efecto estandarizado, usado en el análisis de potencia estadística
para distinguir «no hay diferencia» de «los datos no permiten distinguir». §5.3.

---

## F. Dominio de cumplimiento normativo

**AML/KYC.** *Anti-Money Laundering* / *Know Your Customer*: el marco regulatorio que obliga a
identificar y gestionar entidades de riesgo (personas sancionadas, PEP) en flujos de información
pública. §1.1.

**PEP.** Persona Políticamente Expuesta. §1.1.

**SDN (OFAC).** Lista de Nacionales Especialmente Designados del Departamento del Tesoro de EE.UU.
[19], la fuente de sanciones empleada en este trabajo.

**UAF / CMF.** Unidad de Análisis Financiero y Comisión para el Mercado Financiero, los organismos
chilenos de referencia regulatoria. §1.1.

**RegTech.** Tecnología aplicada al cumplimiento normativo. §1.1.

---

*Este glosario se construyó revisando las definiciones ya presentes en el Informe Final de Tesina;
no introduce conceptos nuevos. Si una definición aquí diverge de la del informe, el informe es la
fuente correcta y este documento debe corregirse para seguirlo, no al revés.*
