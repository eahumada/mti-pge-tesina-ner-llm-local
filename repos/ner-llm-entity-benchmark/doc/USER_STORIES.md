# User Stories: Parallelization & Performance Optimization

This document captures the user stories required to solve the architectural inconsistencies and improve the processing throughput of the NER-LLM benchmark.

## 1. Architectural Integrity (The "True Pub/Sub" Goal)

### US-PAR-01: Decoupled Batch Production
**As a** researcher, 
**I want** the system to publish all batches for a model to the queue without waiting for each one to finish, 
**So that** I can utilize the full capacity of the LLM server and avoid idle CPU time.
- **Acceptance Criteria**:
    - The loop in `main.py` publishes tasks to the queue and does not block on `process_batch`.
    - The system can handle a burst of published tasks without crashing.

### US-PAR-02: Concurrent Batch Consumption
**As a** system operator, 
**I want** the system to process multiple batches simultaneously using a thread pool, 
**So that** I can significantly reduce the total time required to complete a benchmark run.
- **Acceptance Criteria**:
    - Multiple threads are actively calling the Ollama API concurrently.
    - The total execution time is measurably lower than the sequential version.
    - All results are correctly aggregated and matched to their original record IDs.

### US-PAR-03: Horizontal Scaling (Distributed Workers)
**As a** lead researcher, 
**I want** to be able to run separate worker processes on different GPU nodes, 
**So that** I can scale the benchmark to massive datasets that would be too slow for a single machine.
- **Acceptance Criteria**:
    - A standalone `worker.py` exists and can be launched independently.
    - `RedisTaskQueue` is used to coordinate tasks between the Producer (`main.py`) and multiple Consumers (`worker.py`).
    - Results from different workers are correctly consolidated into the final reports.

## 3. Thesis-Grade Quality Enhancements

### US-PAR-06: Scientific Consistency Proof
**As a** thesis validator, 
**I want** a dedicated script to compare sequential and parallel execution outputs, 
**So that** I can prove mathematically that parallelization did not introduce any data corruption or variance in the final metrics.
- **Acceptance Criteria**:
    - Script executes a "Sequential vs Parallel" run on the same dataset.
    - Asserts that F1, Precision, and Recall are identical to the 4th decimal place.

### US-PAR-07: Dynamic Memory Scaling
**As a** system operator, 
**I want** the system to probe VRAM availability and adjust the number of workers dynamically, 
**So that** the system remains stable when switching between small and large models without manual config changes.
- **Acceptance Criteria**:
    - Implementation of a VRAM probe before worker launch.
    - `num_workers` is automatically capped based on the active model's memory requirements.

### US-PAR-08: Efficient Prompt Batching
**As a** researcher, 
**I want** to group multiple records into a single LLM request using a `batch_prompting_enabled` flag, 
**So that** I can further reduce HTTP overhead and increase total throughput.
- **Acceptance Criteria**:
    - Configuration allows enabling/disabling batch prompting.
    - LLM requests contain multiple articles and return a structured list of JSON results.

### US-PAR-09: Advanced Performance Visualization
**As an** analyst, 
**I want** to see a distribution of response times (box-plots) rather than just a mean average, 
**So that** I can identify if specific records or models cause significant latency spikes.
- **Acceptance Criteria**:
    - Latency box-plots are generated in `statistics.py`.
    - Visualizations are integrated into the Streamlit dashboard.

---

## 4. Integridad de la Medición (añadido 2026-09-07)

*Historias derivadas de los hallazgos del cierre del estudio. Cada una nace de un defecto real observado y
documentado en `FINDINGS.md`; no son mejoras especulativas. Las secciones 1 a 3 se conservan sin cambios.*

### US-INT-01: Persistencia de las extracciones crudas
**Como** investigador que debe corregir un defecto de puntuación descubierto a posteriori,
**quiero** que cada corrida almacene las entidades extraídas por registro y no solo sus recuentos,
**para** poder re-puntuar sobre lo guardado sin repetir la inferencia.
- **Criterios de aceptación**:
    - `detailed_results.json` incluye la lista de entidades extraídas por registro y tipo.
    - Una herramienta de re-puntaje puede recalcular P/R/F1 con una regla de cotejo distinta sin invocar al modelo.
- **Motivación**: `FINDINGS.md §F48`. Corregir el *mojibake* del corpus habría exigido re-ejecutar las ~200 horas del estudio porque solo se conservaban `tp/fp/fn`; el defecto quedó declarado como limitación en lugar de corregido.

### US-INT-02: Validación de la codificación del corpus
**Como** responsable de la calidad de los datos,
**quiero** que el cargador detecte y reporte texto con codificación corrupta antes de ejecutar,
**para** no descubrir el problema cuando los resultados ya están publicados.
- **Criterios de aceptación**:
    - Al cargar un corpus se comprueba, en el texto y en las entidades de referencia, si `s.encode('latin-1').decode('utf-8')` difiere de `s`.
    - La corrida se detiene o emite un aviso destacado indicando el porcentaje afectado.
- **Motivación**: `FINDINGS.md §F46` y `§F48`. El 20,1 % de las entidades de referencia del corpus N=120 y el 87 % de sus textos tenían *mojibake*, y el defecto se detectó cuando el estudio estaba cerrado.

### US-INT-03: Coherencia de la convención de puntuación
**Como** revisor de resultados,
**quiero** que todas las métricas del evaluador compartan la misma convención ante la ausencia de datos,
**para** que no queden rincones con el criterio antiguo tras una corrección.
- **Criterios de aceptación**:
    - Ninguna métrica devuelve 1,0 por ausencia de predicciones o de referencia, salvo el acierto vacío legítimo.
    - Existe una prueba que recorre todas las métricas del módulo y verifica la convención.
- **Motivación**: `FINDINGS.md §F49`. La corrección del 2026-09-06 dejó `oov_recall` con el valor por defecto 1,0 que el resto del *scoring* abandonó.

### US-INT-04: Conteo simétrico de aciertos y omisiones
**Como** investigador,
**quiero** que aciertos y omisiones se cuenten sobre la misma unidad,
**para** que la exhaustividad no pueda superar 1,0 ni inflarse cuando varias menciones casan con la misma entidad.
- **Criterios de aceptación**:
    - El acierto se contabiliza por entidad de referencia cubierta, no por entidad extraída que casa.
    - Una prueba con dos extracciones que emparejan con un mismo gold produce exhaustividad de 1,0, no de 2,0.
- **Motivación**: `FINDINGS.md §F50`. Entre el 2 % y el 6 % de los registros presentan exhaustividad inflada, con desviaciones de hasta +0,5.

### US-INT-05: Propagación efectiva de los parámetros configurados
**Como** operador,
**quiero** que un umbral fijado en la configuración llegue a todas las funciones que dicen usarlo,
**para** que la configuración describa lo que el sistema hace.
- **Criterios de aceptación**:
    - `calculate_hallucination_rate` recibe el umbral desde la configuración en lugar de su valor por defecto.
    - Si una métrica usa deliberadamente un umbral distinto, se declara como parámetro propio y no se hereda por omisión.
- **Motivación**: `FINDINGS.md §F50`. El umbral configurado de 85 se descarta en silencio y la tasa de alucinación usa siempre 70.

### US-INT-06: Detección de truncamiento por presupuesto de tokens
**Como** operador,
**quiero** que el sistema avise cuando una respuesta agota `num_predict` sin cerrar su estructura,
**para** distinguir un fallo del arnés de una limitación del modelo.
- **Criterios de aceptación**:
    - Se registra cuántas respuestas alcanzan el tope de tokens y cuántas caen al analizador de respaldo.
    - Un porcentaje alto de respaldo activa un aviso al finalizar la corrida.
- **Motivación**: el caso de `gpt-oss:20b`, cuyo desempeño parecía una limitación del modelo (ΔRAG −0,097) y resultó ser truncamiento: con `num_predict` ampliado pasó a +0,033 y los respaldos cayeron de 67 a 2.

### US-INT-07: Régimen de razonamiento declarado por corrida
**Como** investigador que compara modelos,
**quiero** que el `run_config.json` registre si cada modelo se ejecutó con el modo *thinking* activo,
**para** no comparar corridas con regímenes distintos sin saberlo.
- **Criterios de aceptación**:
    - El fichero de configuración de cada corrida incluye el estado efectivo del razonamiento por modelo.
    - Una fusión de corridas advierte si mezcla regímenes.
- **Motivación**: `FINDINGS.md §F44` y `§F45`. El parámetro viajaba dentro de `options` y Ollama lo descartaba, de modo que durante meses se creyó que un modelo corría sin razonamiento cuando corría con él.

### US-INT-08: Regeneración conjunta de todos los artefactos de una corrida
**Como** consumidor de los resultados,
**quiero** que al re-puntuar se actualicen también el resumen y el informe estadístico, no solo el CSV,
**para** que ningún artefacto quede con cifras obsoletas.
- **Criterios de aceptación**:
    - La herramienta de re-puntaje reescribe `benchmark_results.csv`, `detailed_results.json` y `benchmark_summary.json`.
    - Los artefactos que no se regeneren quedan marcados como obsoletos de forma visible.
- **Motivación**: el re-puntaje inicial solo alcanzó al CSV, y una auditoría posterior tomó cifras infladas de un `benchmark_summary.json` anterior a la corrección, creyéndolo fuente primaria.
