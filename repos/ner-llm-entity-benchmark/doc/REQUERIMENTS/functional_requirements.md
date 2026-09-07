# Functional Requirements

This document outlines the functional requirements for the Sanctions Entity Extraction Evaluator (NER-LLM-Entity-Benchmark) project, designed for compliance news analysis, as detailed in the MTI thesis proposal.

## 1. Data Ingestion & Management
- **FR1.1 Dataset Loading:** The system must load sanctions-related news and ground-truth entity data from the OpenSanctions dataset (JSONL/CSV format).
- **FR1.2 Ground Truth Corpus:** The system must support the ingestion and management of a representative manually annotated corpus of 100-200 news articles, labeled using standard schemes like IOB (Inside-Outside-Beginning) or XML.
- **FR1.3 Inter-Annotator Agreement:** The system must include a utility to calculate Cohen's Kappa coefficient to validate the agreement between two human experts when building the Ground Truth.
- **FR1.4 Batch & Parallel Processing:** The system must process data in configurable batch sizes and support parallel processing.
- **FR1.5 Pub/Sub Architecture:** The system must implement a Publish/Subscribe (Pub/Sub) pattern using a local queue (e.g., Redis, ZeroMQ). The data ingestion module acts as the publisher (producing batches of articles), and the LLM execution modules act as subscribers (workers consuming the batches).
- **FR1.6 Resumability:** The system must be capable of pausing and resuming execution. Using the Pub/Sub state, if the process crashes, it must resume from the last unacknowledged message without reprocessing previously completed batches.

## 2. LLM Integration & Entity Extraction
- **FR2.1 Local Model Execution:** The system must interface via API (e.g., Ollama, LangChain) with local inference engines to execute queries against models like Gemma (7B, 14B), DeepSeek Coder, and LLaMA 2/3.
- **FR2.2 Single-Context RAG:** The system must employ a specialized Retrieval-Augmented Generation (RAG) approach where exactly one specific news article is injected as the sole context into the prompt, explicitly instructing the LLM to ground its extraction only on that text.
- **FR2.3 Entity Types:** The system must extract entities categorized specifically into: Persons, Organizations, and Locations (Geographic).
- **FR2.4 Structured Output Enforcement:** The system must enforce JSON structured output from the LLMs containing the extracted entity arrays for seamless parsing.

## 3. Evaluation & Matching
- **FR3.1 Automated Comparison:** The system must programmatically compare LLM-extracted entities against the Ground Truth entities.
- **FR3.2 Fuzzy String Matching:** The system must utilize fuzzy string matching to account for minor spelling or transliteration variations when scoring matches. *Implementation (verified against `src/evaluator.py:29-38` and `:87`):* `rapidfuzz.fuzz.ratio`, i.e. the normalized **Indel** similarity × 100 — a Levenshtein variant that admits only insertions and deletions, no substitutions, scored as `100 × (1 − d / (|a| + |b|))`. It operates on **characters, not tokens**: `fuzz.ratio("juan pérez", "pérez juan")` returns **50** (measured with the project venv, rapidfuzz), well under the acceptance threshold, whereas a token-based comparison such as `fuzz.token_sort_ratio` would return 100. Both strings are lower-cased before comparison, and nothing else is normalized (no accent folding, no token reordering). The acceptance threshold is `fuzzy_threshold = 85` (`src/config.py:72`). Jaro-Winkler is **not** used.
- **FR3.3 Metrics Calculation:** The system must calculate and store the following per model:
  - **Precision:** True Positives / (True Positives + False Positives).
  - **Recall (Exhaustividad):** True Positives / (True Positives + False Negatives).
  - **F1-Score:** Harmonic mean of Precision and Recall.
  - **Hallucination Rate:** Proportion of extracted entities not found in the source text. *Implementation (`src/evaluator.py:152-197`):* an entity counts as hallucinated when it is not a literal substring of the whitespace-normalized, lower-cased text **and** the best `fuzz.ratio` against any sliding window of the text of the same word count stays below **70** — a threshold distinct from the 85 used for ground-truth matching.
  - *Aggregation (verified against `src/evaluator.py:130-138` and `:361-363`):* Precision, Recall and F1 are computed **per record**, micro-averaged over the three entity types; the per-model figure written to `benchmark_summary.json` is the arithmetic **mean of the per-record values**, not a corpus-level micro F1.
- **FR3.4 Statistical Validation:** The system must support generating data arrays compatible with statistical testing (ANOVA of one way, Tukey's post-hoc test) to validate the statistical significance of the models' performance differences against the manual baseline.

## 4. Reporting & Visualization
- **FR4.1 Confusion Matrix:** The system must generate a confusion matrix segmented by entity type (Person vs. Organization vs. Location).
- **FR4.2 Latency Tracking:** The system must record extraction latency (in seconds) per article for each LLM to evaluate operational efficiency.
- **FR4.3 Streamlit Dashboard (Prototyping):** The system must include a functional web prototype (built with Streamlit) to display evaluation results, allow stakeholders to filter by model/date, and perform qualitative validation of the extracted entities in a simulated production environment.
- **FR4.4 Result Export:** The system must export all metrics and evaluation traces to structured files (CSV, JSON) for archival and external statistical analysis.
