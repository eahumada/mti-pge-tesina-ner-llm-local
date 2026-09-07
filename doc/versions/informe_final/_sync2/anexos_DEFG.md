
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
