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
