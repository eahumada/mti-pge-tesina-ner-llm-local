# Project Backlog, Improvements & Fixes Track (BACKLOG.md)

This backlog logs all identified architectural bottlenecks, bugs, improvements, and validation outcomes resolved during the NER-LLM compliance entity extraction benchmarking.

---

## 🛠️ Resolved Issues & Fixes

### 1. Concurrency GIL & Decoupled Task Processing
*   **Issue:** The initial implementation processed batches sequentially on the main thread, causing severe thread-blocking and idle GPU cycles.
*   **Fix:** Refactored `src/main.py` using `ThreadPoolExecutor` (dynamic workers count). Decoupled the Publisher (main thread queue seeding) from parallel Queue Workers subscribing asynchronously.
*   **Status:** `VERIFIED & CLOSED`

### 2. Model Rotation & VRAM Keep-Alive
*   **Issue:** Switching between local models (e.g. `gemma4:latest` and `llama3.2`) resulted in unified memory (VRAM) overhead/OOM crashes on Apple M4 hardware.
*   **Fix:** Configured Ollama's `keep_alive` payload to 0 in `src/llm_runner.py` and implemented model lifecycle unload logic before loading a new candidate.
*   **Status:** `VERIFIED & CLOSED`

### 3. Prompt Ablation Parameter Mapping
*   **Issue:** Ablation study mode passed the condition name (`zs-en`, `zs-es`, `fs-es`) directly as the physical model parameter to Ollama, causing `404 model not found` HTTP errors.
*   **Fix:** Decoupled physical model names from statistical display labels by adding a `condition_name` mapping parameter inside the `TaskMessage` queue object.
*   **Status:** `VERIFIED & CLOSED`

---

## 📈 Resolved Thesis Improvements

### 1. Fine-Grained Error Classification (REQ40 / HU19)
*   **Details:** Classify errors into Boundary Errors, Type Confusion, and Abbreviation Misses to provide a rich qualitative section for the thesis report.
*   **Status:** `VERIFIED & CLOSED`

### 2. Prompt Ablation Significance Testing (REQ41 / HU20)
*   **Details:** Run statistical significance tests (ANOVA) directly comparing prompt structures (Zero-shot vs. Few-shot Spanish localized) to prove prompt engineering impact.
*   **Validation Outcomes (F1 Scores using gemma4:latest):**
    *   *Zero-Shot English (`zs-en`):* **51.41%**
    *   *Zero-Shot Spanish (`zs-es`):* **57.43%**
    *   *Few-Shot Spanish (`fs-es`):* **70.18%** (Demonstrates massive F1 gain of **+18.77%** over the zero-shot baseline, validating the optimization hypothesis).
*   **Status:** `VERIFIED & CLOSED`

### 3. Hardware Resource Efficiency Index (REQ42 / HU21)
*   **Details:** Normalise token generation speed (tokens/sec) against model parameter scale (Billion scale) to calculate efficiency scores for production scoping.
*   **Status:** `VERIFIED & CLOSED`
