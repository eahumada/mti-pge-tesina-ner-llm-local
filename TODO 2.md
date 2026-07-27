# Comprehensive Project TODO List (User Story Mapped)

This document tracks the detailed tasks and acceptance criteria derived from all 18 User Stories, categorized by project phase. Checked items denote completed features.

## Phase 1: Foundation & Data Ingestion
### HU01: Dataset Ingestion & Validation *(Reqs: FR1.1, FR5.1, FR5.3)*
- [x] Adapt and load Kleptotrace dataset format (`article_id`, `text`, `name_entities`, `organizations`) into the internal unified structure.
- [x] The system loads JSONL/CSV records matching FollowTheMoney schemas.
- [x] Schema validation rejects records missing ID, schema, caption, or properties.
- [x] Each record maintains data provenance including timestamp and source ID.

### HU02: Ground Truth & Inter-Annotator Agreement *(Reqs: FR1.2, FR1.3)*
- [x] Support importing IOB/XML annotated compliance ground truth datasets of 100-200 representative news articles.
- [x] Calculate Cohen's Kappa score between two human annotators.
- [x] Generate warning if Cohen's Kappa is below 0.75.

## Phase 2: Core Execution & Prompting
### HU03: Single-Context RAG & local LLM Runner *(Reqs: FR2.1, FR2.2, FR2.4, NFR1.1, NFR1.2, NFR5.1)*
- [x] Execute local inference queries using Ollama API client.
- [x] Enforce single-context RAG prompt template to ground model extraction and prevent hallucinations.
- [x] Enforce structured JSON output format and parse output with key normalizations.

### HU04: VRAM weight management *(Reqs: NFR3.3, FR5.2)*
- [x] Query Ollama API to set model `keep_alive` parameter to 0.
- [x] Unload current model weights before loading the next benchmark candidate.
- [x] Gracefully sanitize malformed model JSON outputs without crashing execution.

### HU13: Cost & Resource Optimization *(Reqs: NFR3.2, RNF2.2)*
- [x] System executes benchmark sweeps locally on standard VRAM limits (under 16GB).
- [x] Verify CPU/GPU utilization logs do not trigger memory leaks or swap crashes.
- [x] Calculate and log cost comparison estimation (local vs. external API equivalents).

### HU15: Spanish & Latin American Localization *(Reqs: NFR5.1, RNF5.1)*
- [x] Verify prompt templates instruct models to process local Latin American terms (e.g., RUT, fraud contexts).
- [x] Evaluate Spanish language context entities correctly without dropping accents or casing.
- [x] Support localized metrics reporting.

## Phase 3: Pub/Sub & Queueing
### HU05: Thread-Safe InMemory Queue & Batch Processing *(Reqs: FR1.4, FR1.5, NFR4.2)*
- [x] Decouple batch publisher from subscriber execution node.
- [x] Implement a thread-safe InMemoryTaskQueue implementing abstract queue interfaces.
- [x] Ensure multiple batches can be scheduled and executed sequentially.

### HU06: Redis Integration & Crash Resumability *(Reqs: FR1.6, NFR4.3)*
- [x] Support RedisTaskQueue connection configuration.
- [x] Acknowledge tasks only after successful execution.
- [x] Load checkpoint states at launch to skip completed batches when --resume flag is active.

### HU14: Performance & Processing Speed Bounds *(Reqs: NFR3.1, RNF2.1)*
- [x] Ingestion and LLM extraction latency is tracked per article in detailed metrics.
- [x] Ensure batch sizes are configurable to maximize hardware throughput.
- [x] Validate that 100+ articles can be processed sequentially within an overnight window (latency statistics shown in dashboard).

## Phase 4: Metrics & Evaluation
### HU07: Fuzzy Entity Matching & Typed Metrics *(Reqs: FR3.1, FR3.2, FR3.3, RF3.2)*
- [x] Utilize Levenshtein fuzzy string matching ratio above 85% to verify extracted names against ground truth.
- [x] Report separate Precision, Recall, and F1 metrics for Persons, Organizations, and Locations.
- [x] Report macro-averaged overall metric stats.

### HU08: Hallucination Detection & Confusion Matrix *(Reqs: FR4.1, RF3.1)*
- [x] Compare extracted entities against the original source text using a lower fuzzy ratio to identify invented entities.
- [x] Calculate overall hallucination rate (hallucinated / total extracted).
- [x] Aggregate overall TP, FP, FN elements into a confusion matrix for Persons, Organizations, and Locations.

## Phase 5: Academic Reporting
### HU09: ANOVA & Tukey Post-Hoc Analysis *(Reqs: FR3.4, RF3.3)*
- [x] Execute one-way ANOVA across different model result groups.
- [x] Perform pairwise Tukey HSD post-hoc comparisons to calculate adjusted p-values.
- [x] Highlight statistically significant changes ($p < 0.05$).

### HU10: Auditable Run Configs & Logs *(Reqs: NFR5.2, NFR6.2, NFR6.1)*
- [x] Generate structured logs in results/benchmark.log detailing processing phases.
- [x] Save run configuration (seed, temperature, bounds) in results/run_config.json.
- [x] Include detailed metadata (timestamp, model version, system prompt hash) on every evaluation record.

### HU17: Sensitivity Analysis *(Reqs: FR3.4)*
- [x] Implement a mechanism to identify and exclude "outlier" or "difficult" records from the evaluation.
- [x] Re-calculate F1-Score, Precision, and Recall after excluding high-difficulty samples.
- [x] Document the performance delta to determine if specific text patterns (e.g., extremely long articles) disproportionately affect accuracy.

### HU19: Fine-Grained Error Taxonomy *(Reqs: REQ40)*
- [x] Parse extracted name strings to detect partial matches (Boundary Errors).
- [x] Flag correct extractions that are mapped to incorrect categories (Type Confusion).
- [x] Measure missed regional compliance acronyms (Abbreviation Misses).

### HU20: Few-Shot Ablation Study *(Reqs: REQ41)*
- [x] Run benchmark sweeps across three distinct prompt templates.
- [x] Calculate one-way ANOVA on the F1 outcomes of the prompt templates.
- [x] Document statistical significance of prompt adjustments in the statistical report.

## Phase 6: Stakeholder Visualization
### HU11: Streamlit Interactive Dashboard *(Reqs: FR4.2, FR4.3)*
- [x] Launch a web application using Streamlit.
- [x] Display card metrics for best model, F1, precision, and lowest hallucination.
- [x] Provide bar charts comparing F1, precision, and recall across evaluated configurations.

### HU12: Detailed Trace Explorer *(Reqs: FR4.4, NFR6.1)*
- [x] Display a detailed interactive data table containing all processed records.
- [x] Provide selectors to filter records by model and entity category.
- [x] Plot latency distributions and sum of retry warnings per model.

### HU16: Automated System Acceptance Tests *(Reqs: NFR7.1)*
- [x] A summary JSON output lists overall F1 and hallucination rates.
- [x] The dashboard tab highlights whether target F1-Score of 85% is met.
- [x] The dashboard tab flags warning notices if hallucination rate is above 5%.

### HU18: Simulated Production Validation & Stakeholder Feedback *(Reqs: FR4.2, FR4.3)*
- [x] Simulate a realistic daily batch processing flow of news articles.
- [x] Present results to compliance stakeholders via the Streamlit dashboard.
- [x] Capture and document qualitative feedback on whether the extractions are "actionable" and reduce manual workload.
- [x] Validate that the end-to-end turnaround time (ingestion to extraction) meets the operational window (minutes vs. days).

### HU21: Hardware Efficiency Index *(Reqs: REQ42)*
- [x] Measure generation tokens-per-second latency during Ollama runner loops.
- [x] Calculate efficiency ratios normalized by model parameter scale (e.g. 9B, 26B).
- [x] Render efficiency matrix sweeps on the Streamlit dashboard.
