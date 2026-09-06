# Proyecto RAG NER - Plan de Implementación

Este documento detalla todas las tareas a realizar para integrar un sistema RAG (Retrieval-Augmented Generation) basado en diccionarios para mejorar el desempeño de los modelos NER locales.

## 1. Configuración Inicial y Exploración (Graphify)
- [x] Instalar la herramienta `graphifyy` (Graphify).
- [x] Indexar el repositorio con `graphify` para generar el grafo de conocimiento del proyecto y poder consultarlo.
- [x] Investigate Graphify and how it relates to vector databases (Graphify maps structural relationships rather than semantic vector embeddings).

## 2. Preparación de Diccionarios y Vector DB
- [x] Create generic entity dictionaries (`persons.json`, `organizations.json`)
- [x] Search for dictionaries on the internet and ingest them.
- [x] Create a `RAGManager` using ChromaDB to index the dictionaries (ensure it's small, fast, and local).
- [x] Ensure indexing happens once at the start of the benchmark (reuse indexes).

## 3. Integración de RAG en el Flujo de NER
- [x] Integrate RAG vector search into the model inference pipeline (`extract_entities_with_ollama`) so context is prepended to the prompt without expanding the context window too much.

## 4. Orquestación de Pruebas (Dos Ciclos)
- [x] Ajustar el script `src/main.py` para soportar la bandera `--rag-study`.
- [x] Crear un ciclo de evaluación que corra dos veces sobre todos los modelos (Ciclo 1: Línea base sin RAG, Ciclo 2: Con inyección RAG).

## 5. Documentación y Optimización Final
- [x] Refactorizar los resultados agregados y actualizar `BENCHMARKS.md` para mostrar las tablas comparativas de F1 Score con y sin RAG.
- [x] Explicar en `BENCHMARKS.md` cómo el RAG interactúa con el Prompt System.
- [x] Incorporar listas extendidas del Censo de USA, Brasil, México, Venezuela, Chile, China y otros, manteniendo el tamaño por debajo de 10MB y conservando metadata de procedencia.
- [x] Crear agent skills (`~/.gemini/config/skills/ner-entity-extraction/SKILL.md`) que sirvan como contexto avanzado para modelos evaluadores. pruebas completo utilizando los modelos definidos.
- [x] Analizar si el RAG mejora la recuperación (Recall) y la puntuación F1 sin degradar severamente la precisión ni aumentar demasiado la latencia.
- [x] Actualizar `BENCHMARKS.md` detallando los resultados de ambos ciclos y explicando la arquitectura de integración RAG-LLM.
- [x] Documentar la incapacidad de subir >0.10 de F1 iterando sobre diccionarios (el Recall llega a 1.0 pero la Precisión penaliza el F1 general, sugiriendo que se requieren Few-Shot prompting o un corpus de testeo más masivo).
- [x] Agregar métrica de capacidad OOV (Out of Vocabulary) para probar extracción de entidades fuera de los diccionarios.

## 6. Creación de Agent Skills
- [x] Crear un nuevo Skill (documento markdown estructurado) para agentes/modelos que defina heurísticas avanzadas para la identificación de entidades complejas (personas y organizaciones), basándose en la experimentación.

## 7. Próximos Pasos Recomendados (Post-RAG)
- [x] Implementar In-Context Learning (Few-Shot Prompting) inyectando no solo las entidades del RAG sino ejemplos estructurados. **(Cerrado 2026-09-03)** Implementado en `src/kb_rag_manager.py` y expuesto como `--rag-mode kb_fewshot` (ejemplo anotado dinámico) y `--rag-mode kb_combined` (guidelines + ejemplar). La corrida de referencia #13 usó `kb_combined`.
- [x] Aumentar el dataset `benchmark_balanced_120.json` a >100 records para obtener métricas OOV y de F1 más estables. **(Cerrado 2026-09-03)** El corpus tiene **120 registros** y ya se ejecutaron dos barridos completos sobre él: #11 (`balanced120_N120__rag-entities__zs-en__20260824_173036`, 3600 filas) y #13 (`balanced120_N120__rag-kb-combined__zs-en__20260901_140421`, 1200 filas).
- [x] Experimentar con modelos más grandes (Gemma 31B o Qwen 14B) con el RAG para comparar si su capacidad de seguimiento de instrucciones previene los Falsos Positivos mejor que Llama3.1:8B. **(Cerrado 2026-09-03)** Ejecutado en la corrida #13 (N=120, KB RAG `kb_combined`): `gemma4:31b-mlx` baseline 0.5925 / kb_rag 0.5907 (**-0.18 pp**) y `qwen2.5:14b` baseline 0.5189 / kb_rag 0.5651 (**+4.62 pp**). Resultado: el modelo grande NO se beneficia del RAG (ya sigue bien las instrucciones), mientras que los modelos pequeños sí (`llama3.2:latest` **+9.98 pp**, `gemma:latest` **+5.69 pp**).

> **Nota de trazabilidad (2026-09-03).** Los `run_id` citados en esta sección corresponden al catálogo `results/RUNS_INDEX.md`. Las tres tareas anteriores estaban marcadas como pendientes pese a estar ejecutadas; se marcan cerradas con su evidencia, sin eliminar el texto original.
