# Project Prompt: Sanctions Entity Extraction Evaluator

## Repository Name
- `ner-llm-entity-benchmark` (as requested)


## Overview
The objective of this project is to build an automated batch-processing system that evaluates the Named Entity Recognition (NER) capabilities of various local Large Language Models (LLMs). The system will use sanctions-related news data from [OpenSanctions.org](https://www.opensanctions.org) as the ground truth. It will extract entities using local models such as **Gemma 3**, **DeepSeek**, and **LLaMA**, and then compare the model outputs against the verified entities in the dataset.

## System Architecture and Workflow

### 1. Data Ingestion & Batching
- **Dataset:** OpenSanctions.org dataset containing news, reports, and identified entities.
- **Process:** The system will process the data in batches. It will fetch a small subset of $n$ sanction records at a time to manage memory and computational load efficiently. 
- **Pub/Sub Architecture & Scalability:** To guarantee that the process is highly scalable, the architecture will integrate a simple local Publish/Subscribe (Pub/Sub) system (e.g., using Redis, RabbitMQ, o ZeroMQ local). The ingestion script will act as a *Publisher* that encolates batches of news, while the LLM processing nodes act as *Subscribers* (workers) that consume these messages.
- **Resilience & Resumability:** Thanks to the Pub/Sub queue and state checkpointing, the system must be completely resumable. If the process is halted or crashes, it can simply restart and pick up processing from the exact unacknowledged message in the queue without duplicating work or losing data.

### 2. LLM Entity Extraction
- **Models:** Local deployments of Gemma 3, DeepSeek, and LLaMA (running via Ollama, vLLM, or similar local inference engines).
- **Process:**
  - For a given batch of $n$ records, the system will pass the text to the first LLM (e.g., Gemma 3). The instruction passed to the LLM is tightly controlled by the `SYSTEM_PROMPT.md` file, which explicitly enforces strict JSON output and zero hallucinations.
  - **Asynchronous Execution:** To maximize GPU/CPU utilization, the queries within a batch should be executed asynchronously.
  - **Model Lifecycle:** The system must explicitly unload weights of one model before loading the next to prevent GPU Out-of-Memory (OOM) errors.
  - Once completed, the exact same batch will be processed by the next model (e.g., DeepSeek), and then the next (e.g., LLaMA).
  - The system iterates over the entire dataset in this manner until all batches are processed by all models.

### 3. Comparison & Evaluation
- **Matching:** The entities extracted by the LLMs are parsed, normalized, and compared against the original ground-truth entities provided by the OpenSanctions dataset. *(As implemented, "normalized" means lower-casing both strings before comparison — `src/evaluator.py:87`; no accent folding, token sorting or word reordering is applied.)*
- **Evaluation Metrics:**
  - **Precision:** The percentage of correctly extracted entities out of all entities extracted by the model.
  - **Recall:** The percentage of correctly extracted entities out of all actual ground-truth entities in the dataset.
  - **F1-Score:** The harmonic mean of precision and recall, providing a balanced measure of the model's accuracy.
- **Suggested Additional Tools/Metrics:**
  - **Fuzzy Matching:** Implement fuzzy string comparison via `RapidFuzz` to handle minor spelling variations or transliteration differences between the LLM output and the dataset. *(As implemented: `rapidfuzz.fuzz.ratio` — normalized **Indel** similarity × 100, a Levenshtein variant with insertions and deletions only, `100 × (1 − d / (|a| + |b|))`, computed over **characters, not tokens**, with an acceptance threshold of 85. Jaro-Winkler was not used.)*
  - **Latency Tracking:** Measure the extraction time per record for each model to compare computational efficiency.
  - **Entity Type Accuracy:** Break down the F1-score by entity type (e.g., how well it detects 'Person' vs 'Organization').

### 4. Statistics & Reporting
- Upon finishing the batch processing, the system will aggregate the results.
- It will generate a final statistical report (e.g., CSV, JSON, or a Markdown table) comparing the F1-Scores, Precision, Recall, and processing times of Gemma 3, DeepSeek, and LLaMA.
- Optionally, generate visualizations (bar charts, scatter plots) to clearly present the benchmark results.

### 5. Batch Process Improvements
- **Context Management:** Implementing token counting and text truncation/chunking before sending text to the LLM to prevent dropped contexts.
- **Error Handling:** Implementing robust fallback parsing (e.g., Regex) and automatic retry mechanisms for malformed JSON outputs from the LLMs.
- **Pub/Sub Scalability:** Utilizing Redis/Celery to decouple ingestion from inference, allowing the system to pause, resume, and scale horizontally across multiple local workers.

## 6. Risk Analysis Matrix
| Risk Category | Risk Description | Probability | Impact | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Hardware** | **GPU OOM (Out of Memory):** Loading multiple models or excessively large batches causes GPU crashes. | High | Critical | Enforce strict model lifecycle (unload before load). Tune batch size dynamically based on VRAM. |
| **Data/Quality** | **Context Window Overflow:** Very long compliance articles get truncated, losing entities at the end of the text. | Medium | High | Implement chunking algorithms. If an article exceeds $X$ tokens, split it into two overlapping RAG queries. |
| **Operational** | **Malformed JSON Output:** LLMs fail to follow output format, breaking the evaluation pipeline. | High | High | Tightly engineered `SYSTEM_PROMPT.md`. Implement Regex fallback parsers and a maximum of 2 auto-retries. |
| **Operational** | **Data Loss on Crash:** Process dies halfway through a 10,000 article dataset, losing hours of computation. | Low | Critical | Local Pub/Sub architecture ensures unacknowledged messages are persisted and can resume exactly where left off. |
| **Performance** | **Inference Bottlenecks:** Local LLM execution is too slow to process daily news volumes. | Medium | Medium | Use `asyncio` for concurrent local requests. Design Pub/Sub to allow adding more local workers easily. |

## Suggested Technology Stack
- **Language:** Python
- **Pub/Sub System:** `Redis` (con `rq` o `celery`), o `ZeroMQ` para encolamiento local y escalabilidad.
- **LLM Interface:** `ollama-python`, `langchain`, or direct API calls to local endpoints.
- **Data Manipulation:** `pandas` for handling the dataset and calculating metrics.
- **Evaluation Tools:** `scikit-learn` (used only for Cohen's Kappa, `src/statistics.py:12`; Precision/Recall/F1 are computed directly in `src/evaluator.py`, and ANOVA/Tukey come from `scipy.stats` and `statsmodels`), `rapidfuzz` (for string matching).
