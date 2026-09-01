# Project Worklog

This worklog serves as the primary record of all technical decisions, research, and implementation steps for the academic thesis. Every entry must be detailed and mapped to the project sources in `doc/sources/`.

---

## 2026-06-28: Optimization Research and Source Documentation

### Goals
1. Analyze and propose optimizations for the NER processing pipeline.
2. Establish a structured repository for project sources.
3. Formalize worklog requirements for thesis evidence.
4. Implement a professional academic reference system for the thesis.

### Work Performed
- **Optimization Analysis**: Performed a deep dive into the current sequential processing model. Identified the primary bottleneck as I/O wait time during LLM inference.
- **Parallelization Research**: Created `RESEARCH_QUEUE_PARALIZATION.MD` proposing the use of `ThreadPoolExecutor` to overlap LLM request latency, which is expected to provide a significant speedup without the complexity of a full `asyncio` refactor.
- **Model Configuration**: Updated `src/config.py` to use the latest local models: `gemma3:latest`, `llama3:latest`, and `deepseek`.
- **Source Repository**: Created `doc/sources/` directory containing `README.md`, `CLAUDE.md`, and detailed documentation for `OpenSanctions`, `Kleptotrace/CoNLL-2002`, `FollowTheMoney`, and `Ollama`.
- **Academic Reference Framework**: Established a professional `doc/references/` directory. 
    - Categorized sources into Primary, Secondary, and Tertiary.
    - Conducted deep research on **OpenSanctions**, creating a formal justification for its use in the thesis (`opensanctions_justification.md`).
    - Performed an academic literature review on LLM-NER and AML compliance to provide a "State of the Art" baseline (`academic_literature_review.md`).
    - Created a central `REFERENCES.md` index distinguishing between a Reference List (cited) and a Bibliography (consulted).
- **Governance Update**: Modified `CLAUDE.md` and `AGENTS.md` to enforce strict, detailed worklog entries oriented towards the academic thesis.

### Relation to Sources
- The optimization research directly addresses the scalability and throughput requirements needed to process the full `Kleptotrace/CoNLL-2002` and `OpenSanctions` datasets efficiently.
- The source documentation and reference framework provide the necessary academic provenance, justification, and literature baseline required for the final thesis.

### Results
- Successfully mapped the technical bottleneck.
- Established a formal evidence trail and academic reference system.
- Configuration updated for target local LLMs.

---

## 2026-06-28: Architectural Alignment & Thesis-Grade Elevation

### Goals
1. Resolve the "Pub/Sub Facade" architectural inconsistency.
2. Elevate the project from a working prototype to a "thesis-grade" system through structured requirements.

### Work Performed
- **Architectural Fix**: Implemented a true decoupled producer-consumer model in `src/main.py`. The main thread now acts as a Producer publishing all batches to the `task_queue`, while a `ThreadPoolExecutor` manages multiple concurrent worker threads (Consumers).
- **Requirement Expansion**: Created `doc/REQUERIMENTS/parallelization_requirements.md` to formalize the needs for concurrent inference and decoupled processing.
- **User Story Mapping**: Created `doc/USER_STORIES.md` mapping architectural fixes to specific researcher and operator needs (US-PAR-01 to US-PAR-09).
- **Thesis-Grade Enhancement Planning**: 
    - Integrated a "Scientific Validation Suite" (Sequential vs. Parallel consistency check) as a high-priority requirement.
    - Added "VRAM-Aware Scaling" and "Batch Prompting" to the system's roadmap.
    - Proposed "Advanced Statistical Observability" (latency distribution box-plots).
- **TODO Alignment**: Updated `TODO.md` to prioritize scientific validation and distributed worker implementation.

### Relation to Sources
- These improvements align with the "Non-Functional Requirements" (NFR4.2 Horizontal Scalability) and provide the mathematical proof of correctness required for an academic thesis.

### Results
- System architecture now strictly adheres to the Pub/Sub guardrails.
- Implementation of record-level and batch-level parallelization.
- Formalized roadmap for the "Finalization & Validation" phase of the project.
- **Story Migration & Renaming (US -> HU):** Renamed all user stories from `US*.md` to `HU*.md` and repositioned them under `doc/USER_HISTORIES/` with a detailed index `README.md` tracking relationships.
- **Thesis-Grade Enhancements Integrated:** Created separate requirement files (`REQ40/41/42.md`) and individual histories (`HU19/20/21.md`) for:
  * Fine-Grained Error Taxonomy (Boundary mismatches, Type confusion, Abbreviations).
  * Few-Shot Ablation Study (ANOVA comparison across prompt types).
  * Hardware Efficiency Index (Parameter size vs. Latency tokens/sec).
- **Agent Guidelines updated:** Appended explicit python/python3 execution authorization checks inside `AGENTS.md` to guarantee interactive user-gating.
- **Ablation Study Experiment Completed:**
  * Evaluated `gemma4:latest` model using the full 15-record Kleptotrace/CoNLL-2002 annotations feed.
  * *Zero-Shot English (`zs-en`):* **51.41% F1**
  * *Zero-Shot Spanish (`zs-es`):* **57.43% F1** (+6.02% gain)
  * *Few-Shot Spanish (`fs-es`):* **70.18% F1** (+18.77% gain over zero-shot baseline)
  * Calculated normalized Hardware Efficiency Ratios (Tokens/Sec/Billion params) showing optimal execution speed configurations.
  * Verified fine-grained error taxonomy outputs (Boundary errors, type confusion, abbreviation misses) successfully aggregated and mapped in the Streamlit dashboard logs.

---

## 2026-06-30: Factory + Facade Architecture for LLM Providers

### Goals
1. Implement a clean, extensible multi-provider architecture using Factory and Facade design patterns.
2. Enable OpenAI, Anthropic, and Vertex AI providers alongside existing Ollama support.
3. Maintain full backward compatibility so all existing code in `main.py` continues to work unchanged.

### Work Performed

#### Architecture Design

Implemented the **Factory + Facade** pattern in a new `src/providers/` package:

```
src/providers/
├── __init__.py           ← Facade: get_provider(model_name, config) — single public entry point
├── base.py               ← LLMProvider ABC + ProviderNotConfiguredError + ProviderInferenceError
├── factory.py            ← LLMProviderFactory.create(model_name, config) — routing engine
├── ollama_provider.py    ← OllamaProvider (migrated from llm_runner.py)
├── openai_provider.py    ← OpenAIProvider (gpt-* models)
├── anthropic_provider.py ← AnthropicProvider (claude-* models)
└── vertexai_provider.py  ← VertexAIProvider (gemini-* models, dual-SDK)
```

#### Routing Rules (Factory)

| Model prefix | Provider       | Notes                              |
|--------------|----------------|------------------------------------|
| `gpt-*`      | OpenAI         | Requires `OPENAI_API_KEY`          |
| `claude-*`   | Anthropic      | Requires `ANTHROPIC_API_KEY`       |
| `gemini-*`   | Vertex AI      | ADC or `GOOGLE_API_KEY`            |
| *(default)*  | Ollama         | Local daemon or cloud-hosted model |

#### Design Decisions

- **ABC Contract (`LLMProvider`)**: Forces every provider to implement `extract_entities()` and `is_available()`, ensuring the evaluator pipeline can work with any provider without modification.
- **ProviderNotConfiguredError**: Carries `setup_instructions` (human-readable string) so operator error messages are self-documenting.
- **Graceful degradation**: `is_available()` returns `False` when SDK or credentials are missing. Providers raise `ProviderNotConfiguredError` on use, not on import, so optional SDKs don't break the startup.
- **Deferred imports in Factory**: Provider classes are imported lazily via `importlib` so missing optional dependencies (openai, anthropic, google-cloud-aiplatform) never crash the import chain.
- **Vertex AI dual-SDK**: Auto-detects `google-cloud-aiplatform` (Vertex AI, ADC) or `google-generativeai` (AI Studio, API key), trying in that order.
- **Backward Compatibility**: `extract_entities_with_ollama()` in `llm_runner.py` is now a shim that delegates to `OllamaProvider` via `get_provider()`. The function signature is identical to the original; callers in `main.py` require zero changes.

#### Files Modified

- `src/llm_runner.py`: `extract_entities_with_ollama()` replaced with backward-compatible shim (46 lines → 12 lines of delegation code). All helper functions (`parse_llm_response`, `_normalize_keys`, `build_messages`, etc.) kept intact as they are still imported by providers.

#### Files Created

- `src/providers/base.py` — ABC + exceptions
- `src/providers/ollama_provider.py` — full Ollama implementation
- `src/providers/openai_provider.py` — OpenAI implementation
- `src/providers/anthropic_provider.py` — Anthropic implementation
- `src/providers/vertexai_provider.py` — Vertex AI / Gemini implementation
- `src/providers/factory.py` — routing factory
- `src/providers/__init__.py` — Facade (`get_provider`)
- `PROVIDERS.md` — operator configuration guide

### Relation to Sources

This refactoring enables the benchmark to evaluate commercial LLMs (GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro) alongside local Ollama models, directly supporting the thesis goal of a comprehensive multi-model NER comparison.  The extensible architecture (adding a new provider = 1 file + 1 routing entry) supports future expansion to Mistral AI, Cohere, etc.

### Results

- `src/providers/` package operational with 4 providers.
- `main.py`, `worker.py`, and all benchmark code unchanged.
- `get_provider("model-name")` is the canonical API for all new code.
- Full operator documentation in `PROVIDERS.md`.


---

## 2026-06-30: AIMD Adaptive Worker Concurrency Controller

### Goals
1. Replace the hardcoded `num_queue_workers = 4` constant with a self-tuning, rate-limit-aware concurrency controller.
2. Apply TCP congestion-control principles (AIMD) to LLM API back-pressure management.
3. Integrate a Circuit Breaker pattern to protect the pipeline from cascading failures.

### Motivation
The previous hardcoded value of 4 workers was chosen arbitrarily. When cloud-hosted LLM endpoints (e.g. `gemma4:31b-cloud`, `minimax-m3:cloud`) experience rate limiting (HTTP 429) or service overload (HTTP 503), the system continued to hammer the endpoint with the same number of workers, escalating the problem. An adaptive controller that backs off aggressively and recovers gracefully was required for both reliability and thesis-grade engineering robustness.

### Algorithm Design (src/adaptive_workers.py)

#### AIMD — Additive Increase / Multiplicative Decrease
Inspired by **Jacobson (1988)** TCP congestion control and adapted to API rate-limit scenarios:

| Event | Action | Rationale |
|-------|--------|-----------|
| Rate-limit / 429 / 503 error | `workers = max(min, ⌊workers / 2⌋)` | **Multiplicative Decrease**: react aggressively to back-pressure |
| 10 min without any error | `workers += 1` (every 2 min) | **Additive Increase**: probe capacity slowly and safely |
| AI ceiling | `workers ≤ 75% of max_workers` | Prevents starvation of host OS resources |

#### Circuit Breaker (three-state FSM)
Prevents repeated futile requests to a degraded endpoint:

```
CLOSED ──(≥5 consecutive failures)──► OPEN ──(5 min cool-down)──► HALF_OPEN
  ▲                                                                    │
  └────────────────────(1 successful probe)────────────────────────────┘
```

- **CLOSED**: Normal operation.
- **OPEN**: Workers pinned to `min_workers=1`. No new AI increase attempts.
- **HALF_OPEN**: One success restores CLOSED state and resumes normal AIMD operation.

#### Thread Safety
All state mutations (`_workers`, `_consecutive_failures`, timestamps) are protected by a single `threading.Lock`. All public methods (`report_success`, `report_rate_limit_error`, `report_error`, `current_workers`) are fully re-entrant.

#### `is_rate_limit_exception(exc)` helper
Inspects exception message strings for known rate-limit signals across Ollama's native API and cloud endpoints:
`429`, `too many requests`, `rate limit`, `quota`, `overloaded`, `capacity`, `503`, `service unavailable`, `exceeded`.

### Integration in src/main.py

- **Removed**: `num_queue_workers = 4` and `config.num_workers = 4` hardcoded constants.
- **Added**: `AdaptiveWorkerController` instantiated once per `run_benchmark()` call, shared across all model/condition iterations.
- **`worker_consumer` (both ablation and standard branches)**: Wrapped `process_batch()` in try/except. On success → `adaptive_ctrl.report_success()`. On exception → `is_rate_limit_exception(exc)` routes to either full MD step or circuit-breaker counter increment.
- **Post-model logging**: `adaptive_ctrl.get_status()` snapshot logged after each model/condition completes for observability and thesis evidence collection.
- **CLI preserved**: `--num-workers` argument still accepted as the `initial_workers` seed value for the controller.

### Parameters (defaults)
| Parameter | Value | Description |
|-----------|-------|-------------|
| `min_workers` | 1 | Absolute floor |
| `max_workers` | `max(1, cpu_count - 2)` | Auto-detected |
| `initial_workers` | `config.num_workers` (CLI) | Starting point |
| `stable_window_sec` | 600 s (10 min) | Silence window before AI phase |
| `increase_interval_sec` | 120 s (2 min) | Cadence of +1 steps |
| `ai_ceiling_fraction` | 0.75 | 75 % of max_workers |
| `circuit_failure_threshold` | 5 | Consecutive failures to open circuit |
| `circuit_recovery_sec` | 300 s (5 min) | Cool-down before HALF_OPEN probe |

### Files Modified
- `src/adaptive_workers.py` — **NEW** (AdaptiveWorkerController, CircuitState, is_rate_limit_exception)
- `src/main.py` — Integration: import, instantiation, worker_consumer hooks, status logging

### References
- Jacobson, V. (1988). *Congestion avoidance and control*. ACM SIGCOMM Computer Communication Review.
- Brooker, M. (2022). *Retry Strategies in Distributed Systems*. AWS Blog.
- Netflix Hystrix / Resilience4j circuit-breaker pattern documentation.
- Ha, S., Rhee, I., & Xu, L. (2008). *CUBIC: a new TCP-friendly high-speed TCP variant*. ACM SIGOPS.

### Results
- Hardcoded `num_queue_workers = 4` fully removed from production path.
- AIMD controller provides automatic, evidence-driven concurrency tuning for LLM API workloads.
- Circuit breaker prevents runaway retries against degraded cloud endpoints.
- All changes are backward-compatible: `--num-workers` CLI flag still sets the initial concurrency seed.
- Ready for thesis chapter on *System Resilience and Adaptive Concurrency*.

