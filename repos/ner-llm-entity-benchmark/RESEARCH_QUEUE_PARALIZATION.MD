# Research: Queue Parallelization and Thread Executor Analysis

## 1. Objective
Evaluate the feasibility and impact of introducing parallelization to the NER-LLM Entity Benchmark pipeline, specifically analyzing the use of thread executors to mitigate the LLM inference bottleneck.

## 2. Bottleneck Analysis
The system's primary bottleneck is **I/O Wait Time** during LLM inference. The current implementation processes records sequentially:
`Request LLM` $\rightarrow$ `Wait for Response` $\rightarrow$ `Parse` $\rightarrow$ `Next Record`.

Since the LLM inference happens in a separate process (Ollama server), the Python client spends most of its time idle, waiting for a network response.

## 3. Thread Executor Analysis: Will it benefit the system?

### 3.1 How it works
A `ThreadPoolExecutor` would allow the system to dispatch multiple inference requests simultaneously. Instead of waiting for one response before sending the next, the system can maintain $N$ active requests in flight.

### 3.2 Potential Benefits
- **Reduced Total Execution Time**: By overlapping the I/O wait times of multiple requests, the overall wall-clock time for a batch can be significantly reduced.
- **Increased Throughput**: If the Ollama server is configured to handle concurrent requests (via `OLLAMA_NUM_PARALLEL`), multiple inferences can happen truly in parallel on the GPU.
- **Low Implementation Overhead**: `concurrent.futures.ThreadPoolExecutor` is a standard library tool that can be integrated into the existing synchronous codebase more easily than a full transition to `asyncio`.

### 3.3 Constraints & Risks
- **GPU VRAM Contention**: If too many requests are sent in parallel, the LLM server might struggle with VRAM, leading to slower generation times or crashes.
- **Ollama Configuration**: The benefit is capped by Ollama's internal concurrency settings. If `OLLAMA_NUM_PARALLEL=1`, the server will queue requests anyway, though the client-side overhead is still slightly reduced.
- **GIL (Global Interpreter Lock)**: While the GIL limits CPU-bound tasks, it is released during I/O operations (like HTTP requests), making threads highly effective for this specific use case.

## 4. Proposed Implementation Approach
To implement this, the `process_batch` logic should be modified to:
1. Define a `max_workers` value based on the system's GPU capacity.
2. Wrap the `extract_entities_with_ollama` call in a `ThreadPoolExecutor.map` or `submit` loop.
3. Collect results and maintain the original record order for evaluation.

## 5. Conclusion
**Yes, a thread executor will provide a significant benefit.** 
Because the system is heavily I/O bound and the "work" (inference) happens externally, parallelizing the requests is the most effective way to increase throughput without changing the underlying LLM engine.

## 6. Path to "Thesis-Grade" System
To move beyond a functional prototype and meet the rigorous standards of an academic thesis, the following enhancements are proposed:

### 6.1 Scientific Validation Suite
The introduction of parallelization must be validated to ensure no race conditions or data corruption occurs. 
- **Proposal**: Implement a a "Reproducibility Check" script that executes the same dataset in Sequential (1 worker) vs Parallel (N workers) modes and asserts zero variance in the final F1, Precision, and Recall metrics to the 4th decimal place.

### 6.2 VRAM-Aware Dynamic Scaling
Static worker counts risk OOM crashes when switching between models of different sizes (e.g., Llama 3 8B vs DeepSeek).
- **Proposal**: Implement a **VRAM Probe** that checks available GPU memory at runtime and dynamically adjusts `num_workers` to fit the active model's footprint.

### 6.3 Prompt Batching Experimentation
Current overhead is driven by 1-record-per-request HTTP calls.
- **Proposal**: Introduce a `batch_prompting_enabled` flag to group multiple articles (e.g., 5 per request) into a single LLM call, reducing the total number of network round-trips and leveraging larger context windows.

### 6.4 Advanced Statistical Observability
Mean latency is an insufficient metric for academic analysis of LLM performance.
- **Proposal**: Expand `statistics.py` and the dashboard to include **Latency Distribution Box-plots**. This will allow for the analysis of variance and the identification of outlier records that cause performance degradation.

---

## 7. Comparison: Threads vs. Asyncio vs. Multiprocessing

| Method | Suitability | Reason |
| :--- | :--- | :--- |
| **ThreadPoolExecutor** | **High** | Perfect for I/O bound HTTP calls; easier to implement in sync code. |
| **Asyncio** | **Very High** | Most efficient for high concurrency, but requires a broader refactor to `async/await`. |
| **Multiprocessing** | **Low** | Overkill for I/O; adds memory overhead without solving the LLM latency. |

## 7. Architectural Inconsistency: The Synchronous Pub/Sub Facade

### 7.1 Current State Analysis
The system currently implements a "synchronous facade" of a Pub/Sub architecture. In `src/main.py`, the `run_benchmark` loop executes the following sequence in a single thread:
1. `task_queue.publish(task_msg)` $\rightarrow$ Task is put into the queue.
2. `task_queue.subscribe()` $\rightarrow$ The same thread immediately pulls the task back.
3. `process_batch(...)` $\rightarrow$ The thread blocks until the LLM responds.

### 7.2 Guardrail Violation
This implementation violates the architectural guardrails specified in `AGENTS.md` (Section 2), which strictly requires a decoupled Pub/Sub architecture to prevent synchronous sequential batching. The current flow is effectively a standard sequential loop with unnecessary queue overhead.

### 7.3 Proposed Structural Fixes
To resolve this inconsistency, the system must decouple the Producer from the Consumer:

- **Short-term Fix (Threaded Workers)**: 
  Introduce a `ThreadPoolExecutor` in `main.py`. The main thread continues to act as the **Producer** (publishing batches), while a set of worker threads act as **Consumers**, calling `subscribe()` and `process_batch()` concurrently. This allows multiple LLM requests to be in flight simultaneously.

- **Long-term Fix (Distributed Workers)**: 
  Full decoupling by creating a standalone `worker.py` script.
  - **Producer**: `main.py` only publishes tasks to the `RedisTaskQueue` and monitors progress.
  - **Consumer**: Multiple instances of `worker.py` run as independent processes (potentially on different GPUs/nodes), subscribing to Redis and writing results back to a shared state. This fulfills the scalability and fault-tolerance requirements of the project.

