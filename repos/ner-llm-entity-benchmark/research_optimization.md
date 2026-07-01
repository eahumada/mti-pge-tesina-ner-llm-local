# NER-LLM Entity Benchmark: Processing Analysis & Optimization Proposal

## 1. Current State Analysis

### 1.1 Core Processes and Data Pipelines
The system is designed as a benchmarking pipeline for Named Entity Recognition (NER) focusing on compliance and anti-money laundering (AML) sanctions data. 

**Primary Pipeline Flow:**
1. **Data Loading:** Loads JSON datasets (`data/*.json`) containing news captions and ground truth entities (Persons, Organizations, Locations).
2. **Inference (LLM NER):** For each model in the configuration, the system iterates through batches of records and prompts a local LLM via the Ollama API to extract entities.
3. **Evaluation:** Compares LLM-extracted entities against ground truth using fuzzy matching to calculate Precision, Recall, and F1-score, as well as hallucination rates.
4. **Statistical Analysis:** Performs ANOVA and Tukey post-hoc tests to determine statistical significance between model performances.
5. **Export:** Generates detailed CSV traces, JSON summaries, and a Markdown statistical report.

**Datasets Processed:**
- Input: JSON files containing record IDs, source text (`caption`), and ground truth lists.
- Output: `benchmark_results.csv`, `detailed_results.json`, `benchmark_summary.json`, `confusion_matrix.json`, and `statistical_report.md`.

### 1.2 Processing Model Evaluation
The current processing model is **strictly sequential and synchronous**.

- **Model Iteration:** Models are processed one by one.
- **Batch Processing:** While the system uses a "batch" concept, batches are processed sequentially.
- **Request Pattern:** LLM requests are made using a synchronous client. The system waits for each individual LLM response before moving to the next record.
- **Queue Implementation:** The system implements a Pub/Sub pattern (`InMemoryTaskQueue` and `RedisTaskQueue`), but it is used synchronously within a single thread. The main loop publishes a task and then immediately subscribes to it, effectively nullifying the benefit of the queue.

### 1.3 Bottlenecks
The primary bottleneck is **I/O Wait Time (LLM Latency)**. 

1. **Synchronous LLM Calls:** The `extract_entities_with_ollama` function blocks the execution thread until the LLM generates a response. Given the nature of LLMs, this is the slowest part of the pipeline.
2. **Single-Threaded Execution:** Only one record is processed at a time across the entire system.
3. **VRAM Management:** The system unloads and re-loads models sequentially (`manage_model_lifecycle`), adding overhead between model evaluations.
4. **Sequential Dataset Traversal:** The `DatasetIterator` is used in a linear loop, preventing any parallel exploration of the corpus.

---

## 2. Optimization Proposals

### 2.1 Parallelization Strategies

#### A. Asynchronous LLM Inference (Short-term)
Transition from synchronous `ollama` calls to an asynchronous approach using `asyncio` and `httpx` or the asynchronous capabilities of the Ollama API.
- **Mechanism:** Use `asyncio.gather` to dispatch multiple requests to the Ollama server simultaneously.
- **Expected Impact:** Significant reduction in total wall-clock time, especially when the Ollama server is configured to handle multiple concurrent requests (via `OLLAMA_NUM_PARALLEL`).

#### B. Distributed Worker Model (Mid-term)
Activate the existing `RedisTaskQueue` and deploy independent worker processes.
- **Mechanism:**
    - **Producer:** The `main.py` script acts as a producer, publishing batch tasks to Redis.
    - **Consumers:** Multiple worker processes (possibly on different machines/GPUs) subscribe to the Redis queue, process batches, and write results to a shared database or result file.
- **Expected Impact:** Linear scaling of throughput based on the number of available GPUs/nodes.

#### C. Multiprocessing for Evaluation (Low Impact)
While the LLM call is the bottleneck, the evaluation logic (fuzzy matching, statistics) can be offloaded to a `ProcessPoolExecutor` if the dataset grows to millions of records.

### 2.2 Batch Processing Optimizations

#### A. Prompt Batching (Input Level)
Instead of one request per news article, group multiple articles into a single structured prompt.
- **Mechanism:** Modify the prompt to: "Extract entities for the following 5 articles. Return a JSON list of 5 objects."
- **Expected Impact:** Reduces the overhead of multiple HTTP requests and takes advantage of the LLM's ability to process context in bulk.

#### B. Vectorized Evaluation (Output Level)
Use `pandas` or `numpy` vectorized operations for calculating aggregate metrics (F1, Precision, Recall) across the entire results dataframe instead of iterating through lists of dictionaries.

---

## 3. Expected Impact & Roadmap

### 3.1 Performance Impact Matrix

| Optimization | Target Bottleneck | Expected Speedup | Complexity |
| :--- | :--- | :--- | :--- |
| **Asyncio Inference** | LLM Latency | 2x - 5x | Low |
| **Redis Workers** | Throughput / Scale | Linear (per GPU) | Medium |
| **Prompt Batching** | Request Overhead | 1.5x - 3x | Medium |
| **Vectorized Eval** | Post-processing | Minimal (unless $\text{N} > 10^5$) | Low |

### 3.2 Implementation Roadmap

1. **Phase 1: Async Transition**
   - Replace `ollama.Client` with an async alternative.
   - Wrap `process_batch` in an `async` function.
   - Implement `asyncio.gather` for records within a batch.

2. **Phase 2: True Pub/Sub Implementation**
   - Enable `use_redis=True` in configuration.
   - Decouple the "Producer" loop from the "Worker" logic.
   - Create a standalone `worker.py` script that can be scaled horizontally.

3. **Phase 3: Prompt Engineering for Batching**
   - Experiment with "Multi-record prompts" to find the optimal number of records per request without degrading NER quality.
   - Update the `parse_llm_response` logic to handle lists of JSON objects.

4. **Phase 4: VRAM Optimization**
   - Implement a more sophisticated model rotation strategy to avoid frequent unloading/loading if multiple models fit in VRAM.
