# Project Requirements Document: Local LLM Financial Compliance Extraction System

## 1. Executive Summary
The objective of this project is to develop a high-performance, secure, and sovereign system for extracting entities from financial compliance news. The system leverages local Large Language Models (LLMs) to ensure zero data leakage, utilizing a Retrieval-Augmented Generation (RAG) architecture to minimize hallucinations. The pipeline is designed for industrial scalability through a Pub/Sub architecture, ensuring fault tolerance, reproducibility for academic research, and rigorous statistical validation against human baselines.

---

## 2. Data Management and Ingestion

### 2.1 Data Ingestion
*   **Dataset Loading (RF1.1):** The system must support loading datasets in JSONL and CSV formats (e.g., OpenSanctions).
*   **Schema Validation (FR5.1):** Incoming news articles and ground truth datasets must be validated against a predefined schema before processing to ensure data integrity.
*   **Data Provenance (FR5.3):** Every extraction result must be linked back to its source article ID and model version to maintain a complete audit trail.

### 2.2 Ground Truth and Annotation
*   **Annotation Support (RF1.2):** The system must support annotated corpora using IOB and XML schemas for ground truth management.
*   **Inter-Annotator Agreement (RF1.3):** Implementation of Cohen's Kappa metrics to validate agreement between different human annotators.

---

## 3. System Architecture and Infrastructure

### 3.1 Execution Environment & Sovereignty
*   **Zero Data Leakage (NFR1.1 / RNF1.1):** All LLMs must be executed strictly locally. No sensitive data (KYC, PEP) or article text may be transmitted to external proprietary APIs (e.g., OpenAI, Google, AWS).
*   **Open Source Sovereignty (NFR1.2):** The system must be built exclusively using open-source weights (e.g., Gemma, DeepSeek, LLaMA) and frameworks (e.g., Ollama, LangChain).
*   **Hardware Efficiency (NFR3.2):** The architecture must run on standard modern hardware or affordable local GPU instances, targeting a 60-80% reduction in operational costs compared to manual analysis.

### 3.2 Scalability and Fault Tolerance
*   **Pub/Sub Architecture (RF1.4 / FR1.5 / NFR4.2):** Implementation of a local queue (Redis or ZeroMQ) to decouple data ingestion (publisher) from LLM execution (subscribers/workers), enabling horizontal scalability.
*   **Resumability and Fault Tolerance (FR1.6 / NFR4.3):** The system must guarantee that operations can resume after a crash (OOM, power failure, or manual termination) using the Pub/Sub state. Previously completed batches must not be reprocessed.
*   **Memory Management (RNF2.2 / NFR3.3):** Implementation of efficient GPU/CPU memory boundary management to prevent Out-Of-Memory (OOM) failures, specifically ensuring model weights are unloaded appropriately during model cycling.

---

## 4. Local AI and LLM Implementation

### 4.1 Model Integration
*   **Local Engine Integration (RF2.1):** Integration with local AI engines (specifically Ollama) via API.
*   **Pluggable Architecture (NFR4.1):** Use of abstract interfaces (e.g., LangChain wrappers) to allow adding, removing, or updating LLMs via configuration without modifying core code.
*   **Language Optimization (NFR5.1):** Prompt engineering, tokenization, and evaluation metrics must be optimized for the Spanish language and the regulatory nuances of Latin America.

### 4.2 Generation Strategy
*   **Single-Context RAG (RF2.2):** Each news item is treated as the sole context for the model to ensure generation is strictly grounded in the source text and to prevent hallucinations.
*   **Structured Output Enforcement (RF2.3 / FR2.4):** LLMs must produce output in a standardized JSON format containing extracted entity arrays for automated parsing.
*   **Output Sanitization (FR5.2):** The system must handle malformed JSON outputs by attempting data recovery or logging a specific "Extraction Error" event without terminating the batch process.

---

## 5. Evaluation and Statistical Validation

### 5.1 Performance Metrics
*   **NLP Metrics (RF3.2):** The system must calculate Precision, Recall, F1-Score, and Hallucination Rate.
*   **Quality Benchmarks (NFR2.1 / NFR2.2):** 
    *   Target F1-Score of $\ge 85\%$.
    *   Demonstrated statistically significant improvement over the manual baseline (75-80%).
    *   Hallucination rate must be strictly below 5%.
*   **Latency (RNF2.1):** Reduction of analysis time per news item from hours to minutes or seconds.

### 5.2 Validation Framework
*   **Automated Comparison (RF3.1):** Algorithms to automatically compare system results against the defined ground truth.
*   **Statistical Testing (RF3.3 / FR3.4):** Generation of data arrays compatible with One-Way ANOVA and Tukey's post-hoc tests to validate performance differences between models and baselines.
*   **Error Analysis (RF4.1):** Generation of confusion matrices segmented by entity type.

---

## 6. Interface and Reporting

### 6.1 Visualization
*   **Streamlit Dashboard (RF4.2 / FR4.3):** A functional web prototype for visualizing, filtering (by model and date), and qualitatively validating extracted entities in a simulated production environment.

### 6.2 Export and Archiving
*   **Result Export (FR4.4):** All metrics and evaluation traces must be exportable to structured CSV and JSON files for external statistical analysis and archival.

---

## 7. Audit and Research Integrity

### 7.1 Traceability and Logging
*   **Structured Logging (RNF1.2 / NFR6.1):** Implementation of structured JSON logs across all extraction phases for automated monitoring and post-mortem analysis.
*   **Audit Trail (NFR6.2):** Maintenance of an immutable record for every benchmark run, including:
    *   Model Version
    *   Prompt Template
    *   Dataset Hash

### 7.2 Reproducibility
*   **Research Standards (NFR5.2):** All configurations, hyperparameters (temperature, max\_tokens, seeds), and datasets must be fully documented and version-controlled to ensure scientific reproducibility for the MTI thesis.
