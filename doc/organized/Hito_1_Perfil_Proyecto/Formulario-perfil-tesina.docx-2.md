PERFIL DE PROYECTO DE TESINA PROPUESTO
(para postulación a PGE-25)
I.​

ANTECEDENTES

1.1 Identificación del proponente y candidato a magíster
Nombre del estudiante

EDUARDO MAURICIO AHUMADA GALLARDO

Año de ingreso al Programa

2025

Título del tema propuesto (tentativo)

Clasificación y Extracción de Entidades Nombradas
(NER) en Noticias de Cumplimiento Normativo en
Empresas Mediante RAG y un Modelo de Lenguaje
Grande (LLM) usando ollama

Profesor guía propuesto (tentativo)

JOSE LUIS MARTI LARA

Organización vinculada al proyecto​
(opcional)

LEANSTACK SPA

¿Su propuesta se basa en una
aprobaba anteriormente? (S/N)

S

Si su respuesta es afirmativa, indicar
año de aprobación, título del tema y
profesor guía asociado.

Clasificación automática de noticias con nombres
mediante técnicas CRF (Custom Random Fields)
en un proyecto de minería de datos.

II.​

RESUMEN DE LA PROPUESTA

Defina el contexto y el problema, propuesta de solución, objetivos del trabajo, método(s) de validación y
resultados esperados (máximo 200 palabras). Finalmente, agregue palabras claves (máximo 5 palabras).
RESUMEN:
El contexto del proyecto es la necesidad de instituciones financieras de automatizar el cumplimiento
normativo (KYC, PEP). El gran volumen de noticias, obtenidas por suscripción a fuentes públicas (ej. listas
de Google), exige una revisión manual ineficiente, elevando costos y riesgos. El problema central es la
dificultad para extraer entidades precisas y contextualizadas de cada artículo.
La solución propuesta es un sistema distribuido que emplea la técnica de Generación Aumentada por
Recuperación (RAG), tratando cada noticia individualmente como fuente de contexto. Esto facilita que un
Modelo de Lenguaje Grande (LLM) de código abierto (vía Ollama) realice el Reconocimiento de
Entidades Nombradas (NER) (personas, lugares, organizaciones). Las noticias son luego disponibilizadas
con las entidades vinculadas, permitiendo a las instituciones financieras compararlas con sus bases de
datos para identificar riesgos de cumplimiento.

1
​

Plan de Graduación Especial - 2025​

Los objetivos son: (1) Diseñar la arquitectura RAG/LLM para el análisis de noticias en español; (2) Evaluar y
comparar el desempeño de al menos tres LLMs de Ollama (ej. DeepSeek, Gemma) en la tarea de NER; y
(3) Demostrar que el rendimiento de los modelos supera la línea base de extracción humana.
La validación se basará en la evaluación cuantitativa del F1-Score y la Precisión de los LLMs. Los resultados
esperados son una extracción de NER de alta calidad y la validación de la utilidad de los LLMs de código
abierto en tareas de compliance en el mundo real.
PALABRAS CLAVES: NER, COMPLIANCE, CRF, LLM, OLLAMA

2
​

Plan de Graduación Especial - 2025​

III.​

FORMULACIÓN DEL PERFIL DE LA PROPUESTA

a)​ Describa brevemente el contexto organizacional y técnico asociado al trabajo, su experiencia
profesional en el tema y defina el problema que se intentará resolver (40 líneas o ½ página)

Contexto Organizacional y Definición del Problema
El trabajo de tesina se enmarca en el sector de Tecnologías de la Información (TI) para el cumplimiento
normativo (Compliance), vinculado a la empresa LeanStack Spa y la produccion de informacion
relacionada con noticias contingentes.
Tener accesibilidad a esta información publica es crucial para bancos e instituciones financieras, ya que
les permite cumplir con regulaciones como KYC (Know Your Customer) y la administración de Personas
Políticamente Expuestas (PEP). La esencia del compliance en este contexto es la identificación y la
gestión de riesgos asociados a clientes y entidades.
Contexto Técnico: El flujo de datos inicia con la suscripción a fuentes de noticias públicas (ej. listas de
correo de Google) para obtener un gran volumen de artículos. Estos deben ser procesados por un
sistema distribuido robusto y escalable. El núcleo técnico del proyecto es la aplicación de Modelos de
Lenguaje Grandes (LLMs) de código abierto (vía Ollama), integrados mediante una arquitectura de
Generación Aumentada por Recuperación (RAG). La arquitectura RAG es fundamental porque trata
cada noticia individualmente como la única fuente de contexto, forzando al LLM a fundamentar la
extracción de entidades directamente en el texto del artículo.
Experiencia Profesional del Candidato: Mi formación como candidato del Magíster en Tecnologías de la
Información (MTI) y mi experiencia profesional se centran en la aplicación de sistemas distribuidos,
Machine Learning y análisis de datos. Este background es esencial para el diseño de la arquitectura
distribuida (necesaria para manejar el volumen de noticias) y la comprensión de las técnicas avanzadas
de Procesamiento del Lenguaje Natural (PLN), lo que me permite seleccionar, implementar y validar de
forma rigurosa los LLMs de código abierto para una aplicación de alto impacto regulatorio.
Definición del Problema a Resolver:
El problema principal es la ineficiencia operativa y el alto riesgo que implica la revisión manual de
noticias para identificar vínculos de compliance. El desafío técnico es lograr el Reconocimiento de
Entidades Nombradas (NER) —identificación de personas, organizaciones, lugares, etc.— con un nivel de
precisión y contextualización que lo haga útil para la toma de decisiones financieras. Los métodos
tradicionales han demostrado ser insuficientes o requerir una inversión prohibitiva en etiquetado. Por lo
tanto, el problema se define como la necesidad de superar la precisión y exhaustividad de la extracción
humana mediante el uso de LLMs asistidos por RAG, garantizando que las entidades extraídas sean lo
suficientemente confiables para ser comparadas automáticamente con las bases de datos internas de las
instituciones financieras.

3
​

Plan de Graduación Especial - 2025​

b)​ Defina los objetivos del trabajo y la propuesta técnica de solución (40 líneas o ½ página)

Objetivos del Trabajo
Los objetivos específicos del proyecto de tesina se centran en el diseño, la implementación y la
validación de un sistema de extracción de información basado en tecnologías de lenguaje avanzado para
el sector regulado:
1.​ Diseñar la Arquitectura RAG/LLM: Establecer la arquitectura distribuida completa que integre la
Generación Aumentada por Recuperación (RAG) con el Modelo de Lenguaje Grande (LLM) para
el análisis automatizado de noticias en español dentro del dominio de compliance.
2.​ Evaluar el Desempeño de LLMs: Evaluar y comparar rigurosamente el rendimiento de al menos
tres LLMs de código abierto accesibles mediante Ollama (como DeepSeek y Gemma) en la tarea
de Reconocimiento de Entidades Nombradas (NER).
3.​ Superar la Línea Base Humana: Demostrar cuantitativamente que el rendimiento de los
modelos seleccionados supera la línea base de extracción manual/humana en términos de
precisión y exhaustividad (F1-Score), validando la solución para un entorno de alto riesgo.

Propuesta Técnica de Solución
La solución propuesta es un sistema distribuido que procesa grandes volúmenes de noticias (obtenidas
por suscripción a fuentes públicas) para generar datos estructurados y contextualizados.
1.​ Herramientas Centrales: La implementación se basará en el lenguaje de programación Python
(el estándar para el desarrollo de LLMs y RAG) para construir el pipeline de procesamiento.
2.​ Integración de LLM con Ollama: Se utilizará Ollama como plataforma ligera para descargar,
gestionar y ejecutar múltiples Modelos de Lenguaje Grande (LLMs) de código abierto, facilitando
la comparativa de modelos.
3.​ Mecanismo RAG: La estrategia clave es la Generación Aumentada por Recuperación (RAG).
Cada noticia se trata individualmente como el único documento de referencia para el LLM. Este
enfoque garantiza que el LLM solo extraiga entidades (personas, lugares, organizaciones) que
están explícitamente contextualizadas dentro de ese artículo, lo cual es vital para la precisión
del compliance.
4.​ Entrega de Resultados: Las noticias procesadas serán disponibilizadas con sus entidades NER ya
vinculadas. Esto permitirá que las instituciones financieras puedan automatizar la comparación
de estas entidades con sus bases de datos internas para la identificación de riesgos de
cumplimiento (ej. determinar si un cliente está asociado a una noticia de lavado de activos).

4
​

Plan de Graduación Especial - 2025​

IV.​

PLAN DE TRABAJO

a) Defina al menos una hipótesis de trabajo y método de validación propuesto (30 líneas)
Hipótesis de Trabajo
La tesis central del proyecto afirma la superioridad de los modelos avanzados y contextualizados:
Hipótesis: "La implementación de un sistema de Generación Aumentada por Recuperación (RAG)
con un Modelo de Lenguaje Grande (LLM), utilizando cada noticia como fuente de contexto, logrará
una precisión y confiabilidad en la Extracción de Entidades Nombradas (NER) que es superior a la
obtenida por los métodos de extracción manual humana, haciendo viable la automatización de alto
riesgo en tareas de compliance."
Método de Validación Propuesto
La validación se centrará en la prueba empírica y la comparación directa de la calidad de la
información extraída.
Establecimiento de la Línea Base: Se definirá el rendimiento base al hacer que analistas expertos
realicen la extracción de entidades en un conjunto de prueba. Este resultado humano será el
estándar que los modelos deben superar.
Prueba de Modelos LLM: Se evaluará el desempeño de al menos tres LLMs diferentes (accedidos
mediante Ollama) bajo la arquitectura RAG, aplicándolos al mismo conjunto de noticias utilizadas
por los humanos.
Comparación de Resultados: La validación se enfocará en demostrar que el modelo LLM+RAG de
mejor desempeño ofrece una calidad de datos consistentemente mayor y más completa que la
extracción manual.
Confirmación de Fiabilidad: Se verificará que la arquitectura RAG reduce drásticamente los
errores de invención (alucinaciones) del LLM, asegurando que solo se extraiga información
explicitamente contenida en la noticia.
Este enfoque proporcionará la evidencia necesaria para justificar el uso de la tecnología LLM+RAG
en el exigente entorno del compliance.
​
​
​
​
​
​
​
​

5
​

Plan de Graduación Especial - 2025​

b) Defina trabajo adelantado y principales tareas que pretende desarrollar próximamente, definiendo
plazos que no excedan el 30 de septiembre de 2026 (30 líneas)
El trabajo de tesina ya cuenta con un avance significativo en la fase de exploración
tecnológica. A continuación, se define el trabajo adelantado y las principales tareas a
desarrollar, con plazos definidos que no excedan el 30 de septiembre de 2026.

Trabajo Adelantado y Próximas Tareas
Trabajo Adelantado (Exploración Tecnológica y Prototipado)
El proyecto ha superado la etapa inicial de pruebas de concepto, demostrando la viabilidad de
la plataforma técnica:
1.​ Viabilidad de la Plataforma: Se ha confirmado la capacidad de ejecución nativa de
Modelos de Lenguaje Grande (LLMs) —específicamente Gemma, DeepSeek y
Llama— a través de Ollama en un entorno de alto rendimiento (Apple M4). Esto valida
la estrategia de escalabilidad y bajos costos operativos.
2.​ Pruebas de Concepto (PoC) de NER: Se ha desarrollado código Python standalone
para realizar el Reconocimiento de Entidades Nombradas (NER) en noticias públicas
genéricas, estableciendo la base del código que será adaptado al pipeline RAG.
3.​ Investigación de Despliegue: Se ha experimentado con Streamlit para la
visualización potencial de resultados (interfaz) y con procesos batch para asegurar que
el sistema pueda manejar grandes volúmenes de noticias de manera eficiente,
sentando las bases del prototipo distribuido.

Próximas Tareas y Plazos (Hasta Septiembre 2026)
Plazo

Tarea Principal

Foco

Ene
2026
Mar
2026

Preparación
del <ul><li>Definir y estructurar el corpus de noticias para las
- Contexto y Datos
pruebas.</li><li>Establecer el "Ground Truth" y la Línea
Base Humana para la validación.</li><li>Diseñar la
arquitectura
final
RAG/LLM
para
el
dominio
compliance.</li></ul>

Abr
2026

Implementación
y <ul><li>Implementar el pipeline completo RAG en
- Optimización LLM
Python/Ollama.</li><li>Optimizar
los
prompts
y
configuraciones de los tres modelos (Gemma,

6
​

Plan de Graduación Especial - 2025​

May
2026

DeepSeek, Llama) para la extracción de entidades de
compliance.</li></ul>

Jun
Evaluación
y <ul><li>Ejecutar la evaluación comparativa de los tres
2026 - Validación Rigurosa modelos
LLM+RAG
contra
el
Ground
Truth
Jul 2026
humano.</li><li>Validar la hipótesis principal y demostrar
la superioridad del mejor modelo en la extracción de
entidades.</li></ul>

Ago
2026
Sep
2026

Integración
- Documentación
Final

y

<ul><li>Integrar el modelo LLM ganador en un prototipo
funcional
(utilizando
la
base
batch/Streamlit).</li><li>Redacción final, conclusiones y
entrega de la tesina.</li></ul>

Nota: Este plan asegura la transición de la experimentación genérica a una solución validada
y específica para el sector de compliance, con el objetivo de entregar la tesina antes del 30 de
septiembre de 2026.

Observación: Si considera necesario, agregue algunas referencias bibliográficas para documentar mejor su perfil de
proyecto de tesina. Que no excede al orden de tres referencias.
Implementación de RAG y Uso de Datos Privados:
●​ Bourne, K. (2024). Unlocking Data with Generative AI and RAG 2024.
●​ Relevancia: Proporciona un marco práctico y contemporáneo para la implementación de
arquitecturas RAG, directamente relevante para la integración de fuentes de datos (noticias) en el
pipeline del LLM.

7
​

Plan de Graduación Especial - 2025​

