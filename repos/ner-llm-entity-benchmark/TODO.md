# Project TODO List

This file tracks all pending tasks for the NER-LLM Entity Benchmark project. Tasks are organized by priority and phase.

## 🔴 High Priority: Finalization & Validation (The "Thesis Ready" Phase)
- [x] **Fix Synchronous Pub/Sub Facade (US-PAR-01/02)**:
    - [x] Implement `ThreadPoolExecutor` in `main.py` to decouple producer and consumer.
    - [x] Refactor `run_benchmark` to allow the main thread to publish while workers process.
    - [x] Verify result aggregation for parallel runs.
- [ ] **Scientific Reproducibility Validation (US-PAR-06)**:
    - [ ] Create `tests/test_parallel_consistency.py` to compare sequential vs. parallel output metrics.
    - [ ] Assert zero-variance (4th decimal) in F1/Precision/Recall.
    - [ ] Document results in `WORKLOG.md` as formal thesis proof.
- [ ] **VRAM-Aware Scaling (US-PAR-07)**:
    - [ ] Implement VRAM probe to dynamically adjust `num_workers` based on model footprint.
    - [ ] Implement more aggressive model rotation and pre-loading to avoid repeated `manage_model_lifecycle` overhead.
- [ ] **Distributed Worker Implementation (US-PAR-03)**:
    - [ ] Create standalone `worker.py` for independent consumption of `RedisTaskQueue`.
    - [ la l la ] Implement result-writing mechanism for distributed workers (e.g., shared JSON/DB).
    - [ ] Validate horizontal scaling across multiple Ollama nodes.

## 🟡 Medium Priority: Dataset & Metric Expansion
- [ ] **Large-Scale Experimentation**:
    - [ ] Expand evaluation from 20-record sample to full financial compliance sanctions dataset.
    - [ ] Run benchmark sweeps across `gemma3:latest`, `llama3:latest`, and `deepseek`.
    - [ ] Benchmark against the manual F1 baseline (75-80%).
- [ ] **Academic Reporting**:
    - [ ] Generate final thesis validation report with pairwise Adjusted p-values (Tukey HSD).
    - [ ] Create confusion matrices segmented by entity type (Person, Org, Loc).
- [ ] **Prompt Optimization (US-PAR-08)**:
    - [ ] Implement `batch_prompting_enabled` flag in `BenchmarkConfig`.
    - [ ] Develop prompt logic for multi-record processing per LLM call.

## 🟢 Low Priority: Refinements & Dashboard
- [ ] **Advanced Observability (US-PAR-09)**:
    - [ la l la ] Implement latency distribution box-plots in `statistics.py`.
    - [ ] Integrate box-plots into the Streamlit dashboard.
    - [ ] Improve qualitative validation UI in Streamlit.
- [ ] **Source Documentation**:
    - [ ] Expand `doc/references/` as new academic papers are consulted.

## 🛠️ Technical Debt & Maintenance
- [ ] **Schema Validation**: Expand `validate_record_schema` to handle more edge cases in the Kleptotrace dataset.
- [x] **Logging**: Improve trace logging to include worker ID in parallel execution logs.
