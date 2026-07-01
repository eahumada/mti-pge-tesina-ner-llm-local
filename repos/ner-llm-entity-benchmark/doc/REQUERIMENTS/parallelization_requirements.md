# Parallelization & Scalability Requirements

This document supplements the main Functional and Non-Functional requirements, focusing specifically on the resolution of the synchronous processing bottleneck and the implementation of true parallel execution.

## 1. Objective
Transition the system from a "synchronous facade" of a Pub/Sub architecture to a truly decoupled, parallel processing pipeline to meet NFR4.2 (Horizontal Scalability) and FR1.5 (Pub/Sub Architecture).

## 3. Advanced Validation & Efficiency (Thesis-Grade Enhancements)

### 3.1 Scientific Reproducibility
- **REQ-PAR-09: Parallel Consistency Validation**: The system must include a validation suite that executes the same dataset in both Sequential Mode (1 worker) and Parallel Mode (N workers), asserting that final metrics (F1, Precision, Recall) are identical to the 4th decimal place. This ensures that concurrency does not introduce race conditions or data corruption.

### 3.2 Dynamic Resource Management
- **REQ-PAR-10: VRAM-Aware Scaling**: Instead of a static `num_workers` configuration, the system should implement a "VRAM Probe" to check available GPU memory before launching workers. The concurrency level must be dynamically adjusted based on the memory footprint of the active model to prevent Out-Of-Memory (OOM) crashes.

### 3.3 Throughput Optimization
- **REQ-PAR-11: Prompt Batching**: The system must support a `batch_prompting_enabled` mode where multiple records are grouped into a single structured LLM prompt (e.g., 5 articles per request). This is designed to reduce the total number of HTTP requests and minimize overhead.

### 3.4 Advanced Observability
- **REQ-PAR-12: Latency Distribution Analysis**: Beyond mean latency, the system must generate statistical distributions (box-plots) of response times per model to identify performance outliers and variance.
