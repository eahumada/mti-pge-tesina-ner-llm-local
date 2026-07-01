FORMULACIÓN DE UNA PROPUESTA DE PROYECTO DE TESINA
para optar al grado de

Magíster en Tecnologías de la Información
I. IDENTIFICACIÓN Y RESUMEN DEL PROYECTO
1.1 Identificación del proponente y candidato a magíster
Nombre del estudiante

Jose Miguel Catalán Gutierrez

RUT

16119206-6

Ciudad y región de residencia

Santiago, RM

Ciudad y región de trabajo

Santiago, RM

E-mail y teléfono de contacto

Jose.catalang@usm.cl, +56 9 5256 9230

Fecha de ingreso al MTI

2021

1.2 Identificación del Proyecto de tesina propuesto
Título del proyecto

Sistema evaluador de riesgos en proyectos de desarrollo de
software utilizando Machine Learning.

Área principal de TI

Gerencia de Operaciones

Profesor guía (o Supervisor de
tesina) propuesto

Mauricio Solar

Organización/empresa a la que se
vincula el proyecto

Flagare SPA

Persona y cargo del contacto

Javier Oporto, CEO

E-mail y teléfono del contacto

joporto@flagare.cl, +56 9 7650 9114

…………………………………
FIRMA

MTI-401 Seminario de Investigación Aplicada 2023

1

1.3 Resumen del Proyecto de tesina propuesto
El resumen de una propuesta de un Proyecto de tesina debe ser suficientemente informativo,
presentado como un trabajo de investigación, que contenga: (1) una definición del problema,
describiendo el contexto y la problemática general en la cual surge el problema, (2) principales
aspectos técnicos propios de la disciplina de TI involucrados, (3) solución propuesta y objetivos
planteados para el proyecto, (4) metodología de trabajo para validar la propuesta, como resultados
esperados y (5) su posible impacto en el medio industrial de TI (al menos a nivel nacional).
(Máximo 30 líneas, 300 palabras)
En Flagare SPA, empresa dedicada al desarrollo de software, la gestión de proyectos se ha vuelto
una tarea cade vez más compleja debido a diversas tecnologías y metodologías de desarrollo de
software en los cuales participa la compañía, lo que ha llevado a reiteradas desviaciones de
objetivos y resultados negativos en el desarrollo de proyectos. La falta de indicadores precisos
para anticipar problemas y desviaciones, junto con errores en la gestión, ha impactado en el éxito
de los proyectos. El desarrollo de esta tesina busca generar una innovación y un diferenciador en la
gestión actual de proyectos mediante el uso de información histórica para entrenar un modelo de
machine learning, generando métricas predictivas que permitan corregir proyectos en curso a
tiempo. El propósito es mejorar tanto el desarrollo como los aspectos económicos de los proyectos
como en los indicadores de gestión, aspirando a un incremento del 10% en los resultados
absolutos con la implementación de Inteligencia Artificial en proyectos de desarrollo de software
en esta empresa de desarrollo de Software, la metodología de validación propuesta se basa en
contrastar los indicadores de los proyectos donde se utiliza esta tecnología con proyectos
históricos y que se encuentren en ejecución donde no ha sido aplicada esta innovación.

1.4 Palabras claves
Use no más de 5 conceptos claves, pudiendo algún concepto requerir más de una palabra (por
ejemplo: modelo de madurez, agilidad, gestión de proyectos).
Desarrollo de software, gestión de proyectos, machine learning, rentabilidad, innovación.

MTI-401 Seminario de Investigación Aplicada 2023

2

II.

FORMULACION GENERAL DEL PROYECTO

En un máximo de 5 páginas, formule en forma general su Proyecto de tesina, donde usted debe al
menos referirse a los siguientes aspectos (aunque no sea en este orden).
1. Definición del problema y solución propuesta. (a) Defina el contexto y el problema que se
pretende abordar en el marco de este proyecto. Refiérase al tipo de organización al que se vincula
este proyecto y la importancia que tiene su resolución para ésta. (b) Identifique alternativas de
solución al problema y describa/compare con el enfoque adoptado por usted para resolverlo. (c)
Destaque la contribución más importante que pretende lograr con su trabajo y el grado de
originalidad que éste tiene. Refiérase a cómo los resultados esperados de su proyecto pueden ser
de interés público y para otras organizaciones que presentan realidades similares. Compare
también con las realidades de otros países, especialmente desarrollados. (d) Identifique las
materias en las cuales su trabajo profundizará y los cursos relacionados del programa (MTI) que
usted considera relevantes como base de conocimiento para el desarrollo del Proyecto de tesina.
2. Marco teórico, estado del arte y propuesta de solución. (a) Explique los conceptos técnicos y
teorías fundamentales sobre los cuales se sustenta el trabajo, y especifique/precise sobre esta
base el problema planteado, destacando aquellos aspectos relacionados con tecnologías de la
información. (b) Relacione su propuesta de trabajo con otros trabajos que han abordado
problemas similares, referenciándolos y relacionándolos con su propuesta de trabajo,
estableciendo similitudes y diferencias. Perfile en este contexto su trabajo, definiendo su ámbito
de acción y los objetivos generales que pretende lograr. (c) Defina con precisión su propuesta de
investigación, la estrategia de solución que pretende aplicar, y qué innovaciones tecnológicas y/o
metodológicas son los más relevantes de la propuesta. Fundamente en base a lo expuesto
anteriormente.
3. Hipótesis y metodología de validación. En base a la propuesta técnica del punto anterior: (a)
Formule al menos una hipótesis de trabajo, especificando las expectativas de mejora y/o
innovación que se pretende lograr como resultado del desarrollo del Proyecto de tesina.
Identifique variables independientes y dependientes asociadas a la hipótesis. (b) Especifique la
metodología que aplicará para probar esta(s) hipótesis. Refiérase a posibles métodos de
investigación que pretende aplicar para recopilar datos, tales como estudio de caso(s), juicio de
expertos, encuestas, desarrollo de prototipos, pruebas de concepto, diseño de experimentos,
entre otros.
4. Referencias bibliográficas. En todos los puntos anteriores, cite todas las referencias usadas en
la formulación de su proyecto, para facilitar encontrar las fuentes de información y fundamentar
adecuadamente su propuesta. Use un número significativo de referencias recientes (últimos 3
años). El formato usado para citar y referenciar es el de la IEEE.

MTI-401 Seminario de Investigación Aplicada 2023

3

(Máximo 5 páginas)
1

Definición del problema y solución propuesta:

La consultora tecnológica se enfrenta a un desafío en la gestión de múltiples proyectos simultáneos
para diferentes clientes y tecnologías. Actualmente, carece de una herramienta tecnológica que
brinde una evaluación precisa del progreso de estos proyectos en desarrollo. Esta carencia se debe
a la existencia de diversas metodologías de gestión, como cascada y ágil, lo que dificulta la
implementación de una metodología transversal para evaluar de manera temprana los resultados
esperados en cada proyecto.
En este contexto, definimos un proyecto como fracasado o poco rentable cuando no cumple con los
indicadores clave, como tiempo, esfuerzo o costo. A menudo, los proyectos pueden parecer
exitosos desde la perspectiva del cliente, pero los análisis posteriores revelan ineficiencias, como la
asignación de recursos adicionales a la planificación original o períodos de inactividad debido a
elementos faltantes proporcionados por el cliente. Estos análisis indican que algunos proyectos
pueden costar el doble de lo presupuestado, lo que se traduce en pérdidas para la compañía. Estos
fracasos suelen evaluarse retrospectivamente en lo que se conoce como un análisis "post mortem".
En la siguiente imagen se presentan los problemas más comunes que pueden llevar al fracaso de
un proyecto. Es importante destacar que un proyecto puede verse afectado por uno o varios de
estos problemas. A partir de esta información, se identificarán algunas de las variables de
entrenamiento para el modelo propuesto.

Ilustración 1 - Problemas en proyecto Fuente: Árbol de Problemas, DISEÑO DE UN MODELO DE
EVALUACIÓN DE PROYECTOS

MTI-401 Seminario de Investigación Aplicada 2023

4

1.1 Solucion Propuesta:
La propuesta de solución consiste en desarrollar un sistema basado en machine learning que
permita evaluar de manera precisa y anticipada los riesgos en proyectos de desarrollo de software.
El objetivo principal es mejorar la gestión de riesgos en dichos proyectos, identificando
tempranamente posibles desviaciones y permitiendo la toma de decisiones informadas para
mitigar o prevenir impactos negativos.
Objetivos específicos:
• Diseñar y entrenar un modelo de machine learning que analice datos históricos de proyectos
de desarrollo de software y pronostique riesgos potenciales.
• Desarrollar una interfaz intuitiva que permita a los usuarios cargar datos de proyectos,
ejecutar el modelo y visualizar los resultados de la evaluación de riesgos.
• Validar la efectividad del modelo utilizando datos reales de proyectos y comparando sus
predicciones con los resultados reales.
• Demostrar cómo la implementación del sistema puede mejorar la toma de decisiones en la
gestión de riesgos y contribuir al éxito de los proyectos de desarrollo de software.
• La principal innovación tecnológica radica en la implementación de técnicas avanzadas de
machine learning para la evaluación de riesgos en proyectos de desarrollo de software. Al
utilizar datos históricos y patrones de proyectos anteriores, el modelo puede identificar
riesgos potenciales antes de que se materialicen, permitiendo que los equipos de gestión
tomen medidas proactivas. Esta capacidad de predicción temprana es la clave para mitigar los
riesgos y mejorar la calidad y el éxito general de los proyectos de desarrollo de software.
• Las materias y cursos que son considerados relevantes para el desarrollo de este proyecto son
los siguientes:
o Analitica de Datos
o Inteligencia Artificial y Aprendizaje Automatico
o Gestion de Proyectos
o Gestión de Procesos de Negocios y TI
2

Marco teórico, estado del arte y propuesta de solución

El marco teórico de esta investigación en machine learning se centra en la evaluación de proyectos
tecnológicos de una empresa de Desarrollo de Software, se basa en una serie de conceptos técnicos
y teorías fundamentales utilizadas tanto en el desarrollo de proyectos de machine learning como
en la gestión de proyectos. A continuación, se identifican los principales conceptos y se
proporcionan referencias bibliográficas relevantes asociadas:
Machine Learning [1]:
Definición: Machine Learning se refiere al desarrollo de algoritmos y modelos que permiten a las
computadoras aprender patrones y tomar decisiones basadas en datos.
Evaluación de Proyectos Tecnológicos [2]:
Definición: Evaluación de proyectos tecnológicos se refiere a la aplicación de métodos y técnicas
para medir el rendimiento y el éxito de proyectos relacionados con tecnología.
Algoritmos de Machine Learning para Clasificación y Regresión [3]:
Definición: Estos algoritmos son utilizados para predecir o clasificar datos en función de
características específicas.

MTI-401 Seminario de Investigación Aplicada 2023

5

Evaluación de Modelos de Machine Learning [4]:
Definición: La evaluación de modelos implica medir su rendimiento y generalización utilizando
métricas como precisión, recall, F1-score, y curvas ROC.
Validación Cruzada (Cross-Validation) [5]:
Definición: La validación cruzada es una técnica para evaluar el rendimiento de un modelo
dividiendo los datos en conjuntos de entrenamiento y prueba de manera iterativa.
Selección de Características (Feature Selection) [6]:
Definición: La selección de características es el proceso de identificar las características más
relevantes para mejorar la precisión del modelo.
Curvas de Aprendizaje (Learning Curves) [7]:
Definición: Las curvas de aprendizaje representan gráficamente cómo mejora el rendimiento del
modelo a medida que se incrementa el tamaño del conjunto de datos de entrenamiento.
Imputación de Datos (Data Imputation) [8]:
Definición: La imputación de datos se refiere a técnicas para llenar valores faltantes en conjuntos
de datos.
Estos conceptos técnicos y teorías son esenciales para la comprensión y aplicación efectiva de
machine learning en la evaluación de proyectos tecnológicos. La literatura citada proporciona una
base sólida para el desarrollo y la implementación de la investigación.
2.1 Estado del Arte
El estado del arte de la gestión de proyectos predictiva utilizando machine learning se encuentra
en un momento de rápido desarrollo. En los últimos años, se han desarrollado una serie de
técnicas de machine learning que pueden utilizarse para predecir el éxito o el fracaso de un
proyecto, así como para identificar los riesgos y oportunidades clave.
A continuación, se presentan algunos ejemplos específicos de cómo se ha utilizado el machine
learning en la gestión de proyectos:
• IBM utilizó el aprendizaje automático para predecir el éxito de los proyectos de
desarrollo de software. El modelo de aprendizaje automático de IBM fue capaz de
predecir con éxito el éxito de los proyectos con un 90% de precisión.
•

Una empresa de construcción utilizó el aprendizaje automático para predecir el retraso
de los proyectos. El modelo de aprendizaje automático de la empresa de construcción
fue capaz de predecir con éxito los retrasos con un 80% de precisión.

2.2 Propuesta de solución
La estrategia de desarrollo de un modelo de machine learning que utilizara la historia de proyectos
de la compañía (sobre 500 proyectos) para su entrenamiento, la solución propuesta implica cuatro
etapas las cuales se integran y desarrollan en metodología de cascada, el siguiente diagrama
muestra la relación lógica que se presenta entre estas etapas:

MTI-401 Seminario de Investigación Aplicada 2023

6

Ilustración 2 – Etapas de la solución [Elaboración Propia]

Primera Etapa: Investigación
Se realiza una investigación sobre que tipos de herramientas se encuentran disponibles para el
entrenamiento del modelo y cuál es la factibilidad y complejidad de utilización de cada una de
estas herramientas, el resultado de esta etapa es seleccionar la herramienta que será utilizada para
llevar a cabo el desarrollo de la hipótesis.
Segunda Etapa: Recopilación y análisis de datos
El propósito de esta etapa es la de recopilación de los datos históricos de los proyectos de Flagare
SPA, la cantidad de proyectos disponibles debería ser de aproximadamente 500 dentro de los
cuales se deberá obtener información importante que nos permita ir entrenando el modelo, esta
etapa a su vez consta de 4 subetapas que permitirá como resultado final información fiable y
depurada.
Subetapas que componen la recopilación y estudio de datos:
• Recolección de datos
• Limpieza y depuración de datos
• Normalización de datos
• Análisis de datos
Tercera Etapa: Diseño y Entrenamiento del Modelo
En esta etapa se busca obtener como resultado la consolidación y el diseño del modelo de machine
learning, esta etapa también consta de tres subetapas las cuales son:
• Preparación de datos
• Desarrollo del modelo
• Entrenamiento del modelo
Cuarta Etapa: Evaluación del Modelo
En la cuarta etapa, se pretende realizar la carga de la información de prueba reservada en la
anterior etapa, con el objetivo de determinar la precisión de la predicción del modelo, para lo cual
es necesario llevar a cabo las siguientes subetapas:
• Inferencia o predicción datos de prueba.
• Evaluación del modelo con los datos de prueba

MTI-401 Seminario de Investigación Aplicada 2023

7

3

Hipótesis y metodología de validación

La implementación de un modelo de machine learning para evaluar riesgos en proyectos de
desarrollo de software mejorará la eficiencia en un 10% al anticipar y mitigar riesgos de manera
proactiva, permitiendo una toma de decisiones más informada y eficaz en la gestión de proyectos.
3.1 Identificación de Variables
En el contexto del objetivo de generar un incremento del 10% en los resultados absolutos con la
implementación de Inteligencia Artificial (IA) en proyectos de desarrollo de software en Flagare
SPA, podemos identificar las siguientes variables independientes y la variable dependiente
asociadas a la hipótesis:
Variable Independiente (Causal):
Implementación de Inteligencia Artificial (IA): Esta variable representa la introducción de
tecnologías de IA en los proyectos de desarrollo de software de Flagare SPA. Se considera como la
causa o factor de cambio en la hipótesis.
Variable Dependiente (Observable o de Efecto):
Resultados Absolutos de Proyectos: Esta variable dependiente refleja el rendimiento global de los
proyectos de desarrollo de software en términos de éxito, calidad, tiempos, costos y otros
indicadores clave. Es la variable que se busca mejorar mediante la implementación de IA.
3.2 Metodología de Validación:
Para validar la hipótesis y asegurar el cumplimiento de los objetivos planteados, se llevará a cabo
la siguiente metodología de validación:
• División de Datos: Se dividirá el conjunto de datos en un conjunto de entrenamiento y un
conjunto de prueba. El primero se utilizará para entrenar el modelo, mientras que el
segundo se reservará para evaluar la capacidad predictiva del modelo.
• Evaluación del Modelo: Se evaluará el modelo utilizando el conjunto de prueba. Se
compararán las predicciones del modelo con los resultados reales de los proyectos para
determinar su capacidad para anticipar y mitigar riesgos.
• Medición de Eficiencia: Se medirá la eficiencia mejorada en función de la capacidad del
modelo para identificar riesgos antes de que se manifiesten. Se compararán las decisiones
tomadas con la guía del modelo con los resultados obtenidos.
• Análisis Comparativo: Se compararán los resultados obtenidos con proyectos en los que
se utilizó el modelo con los resultados de proyectos sin su intervención. Se calculará el
porcentaje de mejora en la eficiencia en la gestión de riesgos.

MTI-401 Seminario de Investigación Aplicada 2023

8

Referencias Bibliográficas:
[1] C. M. Bishop, "Pattern recognition and machine learning," in Information Science and
Statistics, Springer, 2006.
[2] K. P. Weber and A. G. Picard, "Visual project management: simplifying project execution to
deliver on time and on budget," in IEEE Transactions on Engineering Management, vol. 53,
no. 2, pp. 171-184, May 2006.
[3] J. D. Lee, H. Lee, J. M. Kim, and S. C. Kim, "Prediction of water quality parameters with machine
learning techniques: a comparative study," in IEEE Access, vol. 9, pp. 42595-42604, 2021.
[4] O. Tharwat, "Classification assessment methods," in Applied Computing and Informatics, vol.
16, no. 1, pp. 1-28, 2020.
[5] R. Kaur and S. Mittal, "Comparison of cross-validation techniques in classification algorithms
for software fault prediction," in IEEE Transactions on Reliability, vol. 70, no. 1, pp. 3-19,
2021.
[6] R. Kohavi and G. H. John, "Wrappers for feature subset selection," in Artificial Intelligence, vol.
97, no. 1-2, pp. 273-324, 1997.
[7] Y. Fu, W. Pan, and S. Shen, "Learning from learning curves: hierarchical clustering based on
empirical risk minimization," in IEEE Transactions on Neural Networks and Learning
Systems, vol. 29, no. 11, pp. 5575-5588, 2018.
[8] J. Kim and W. K. Cheong, "Iterative imputation of missing data in multivariate time series," in
IEEE Transactions on Knowledge and Data Engineering, vol. 33, no. 8, pp. 3325-3336, 2021.

MTI-401 Seminario de Investigación Aplicada 2023

9

III.

PLANIFICACIÓN DEL TRABAJO DEL PROYECTO

Los Objetivos específicos permiten dividir el trabajo del Proyecto de tesina en varias etapas o tareas,
que debieran ser coherentes con lograr la validación de la hipótesis y alcanzar los resultados
esperados, sin perder de vista la elaboración de un informe final que incluya las conclusiones del
trabajo. La Metodología de trabajo especifica los métodos o instrumentos que aplicará para lograr los
objetivos específicos. Finalmente, el Plan de trabajo establece tareas y plazos para concluir el
Proyecto de tesina.
i) Objetivos específicos y tareas. Según la metodología de investigación elegida y los alcances de
su tesina, especifique los objetivos específicos que se requieren para identificar tareas, planificar
el trabajo de su Proyecto de tesina y lograr alcanzar los resultados esperados.
(máximo 1/2 página)
Los objetivos específicos para cada etapa del proceso de Investigación son los siguientes:
Primera Etapa: Investigación
• Revisar la literatura académica y técnica relacionada con la evaluación y entrenamiento de
modelos de machine learning.
• Identificar casos de estudio y mejores prácticas utilizados en el desarrollo de proyectos de
similares características.
Segunda Etapa: Recopilación y análisis de datos
• Identificar fuentes confiables y disponibles de datos relacionados con proyectos de desarrollo de
software y sus historiales de riesgos.
• Levantamiento y entendimiento del modelo de gestión y operación de los proyectos.
• Evaluar la calidad y la integridad de los datos disponibles para garantizar la fiabilidad del modelo.
• Realizar un análisis exploratorio de datos (EDA) para comprender la distribución y las relaciones
entre las variables relacionadas con los riesgos en proyectos de desarrollo de software.
• Diseño y construcción de Modelo ETL.
Tercera Etapa: Diseño y Entrenamiento del Modelo
• Diseño de arquitectura del modelo de machine learning considerando la aplicación de la
tecnología necesaria para el desarrollo de la investigación.
• Definir y diseñar las características (features) relevantes del modelo, teniendo en cuenta la
información recopilada durante la investigación y el análisis de datos.
• Dividir el conjunto de datos en conjuntos de entrenamiento, validación y prueba para el
entrenamiento del modelo.
• Realizar el entrenamiento y validación del modelo de ML.
Cuarta Etapa: Evaluación del Modelo
• Realizar pruebas utilizando datos para evaluar la precisión y la robustez del modelo recopilando
la informacion de su fiabilidad respecto al resultado de proyecto ya ejecutados.
• Integración del Modelo en proyectos de la empresa para su validación y evaluación.

MTI-401 Seminario de Investigación Aplicada 2023

10

ii) Metodología de trabajo. Según los objetivos específicos anteriores, describa los métodos o
instrumentos que aplicará en el desarrollo del Proyecto de tesina.
(máximo 1/2 página)
Metodología Utilizada:
• El proyecto de tesina se llevará a cabo mediante una metodología mixta que fusiona
enfoques cascada y ágiles para lograr una investigación exhaustiva y el desarrollo efectivo
del modelo de machine learning.
• Enfoque Metodología Cascada: Esta metodología se divide en fases claramente definidas,
cada una de las cuales se inicia una vez que la fase anterior ha sido completada y revisada.
• Enfoque Metodología Agile: En la finalización e Inicio de una nueva etapa se realizar una
reunión de seguimiento realizando una revisión del avance de los objetivos planteados.
Instrumentos:
•
•
•
•
•
•

En cada etapa se generará la documentación con los resultados y hallazgos del desarrollo de
la investigación.
Reuniones con el cliente para el levantamiento de Informacion y Procesos
Reuniones de control en cada etapa con el profesor guía para un seguimiento y control del
avance de la investigación.
Se generarán pruebas iterativas para evaluar la precisión y robustez del modelo.
Integración progresiva del modelo en proyectos de la empresa.
Recopilación continua de información sobre la fiabilidad del modelo y sus resultados para la
validación de la hipótesis planteada.

MTI-401 Seminario de Investigación Aplicada 2023

11

iii) Plan de trabajo. Señale las principales etapas, actividades y plazos establecidos para la
ejecución del Proyecto de tesina (por ejemplo: carta Gantt con fechas esperadas). No pierda de
vista las fechas esperadas para graduarse a tiempo.
(máximo 1/2 página)

Notas:
• Etapas correspondientes a etapas se encuentran comprimidas por visualización.
• Se adjunta Anexo con Gantt completa ([ANEXO]Plan_Trabajo_JC_2023.pdf)

MTI-401 Seminario de Investigación Aplicada 2023

12

V.

RECURSOS REQUERIDOS Y COMPROMISOS

Señale los recursos que requiere y/o dispone para realizar el proyecto (libros, software, equipos,
etc.). Si requiere el apoyo o compromiso de otras personas u organizaciones, o depende de otros
proyectos para la realización de este Proyecto de tesina, señalarlo explícitamente.
(máximo ½ página)
Recursos Requeridos:
• Investigación:
o Acceso a Información de Investigación (Biblioteca USM, Internet)
o Acceso a literatura relacionada (Biblioteca USM, Internet)
•

Recursos Tecnológicos:
o Servidores Cloud IBM – Créditos Disponibles Partner IBM
o Licencia Google Colab Pro – Licenciamiento Propio
o ETL Talend - Free

Compromisos:
• NDA (Acuerdo Confidencialidad): Al ser información sensible se firmará un NDA entre
Alumno y Empresa.
• Empresa Flagare SPA:
o Disponer de las fuentes de Información necesarias para le generación del modelo
de ML.
o Disponer de los recursos humanos necesarios para el levantamiento de
información y procesos de gestión.
o Disponer de los recursos humanos requeridos para la evaluación del modelo
generado y su aplicación en proyectos en curso.
Financiamiento Propio

MTI-401 Seminario de Investigación Aplicada 2023

13

