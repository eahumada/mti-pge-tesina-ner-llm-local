# Non-Functional Requirements

This document outlines the non-functional requirements (NFRs) for the Sanctions Entity Extraction Evaluator (NER-LLM-Entity-Benchmark), aligning with the objectives of the MTI thesis and the operational needs of LeanStack SpA.

## 1. Privacy, Security & Regulatory Compliance
- **NFR1.1 Zero Data Leakage:** Due to the extreme sensitivity of financial compliance data (KYC, PEP), the architecture must strictly enforce local execution of the LLMs. No article text or entity data can be transmitted to external proprietary APIs (like OpenAI GPT, Google Cloud NLP, or AWS).
- **NFR1.2 Open Source Sovereignty:** The system must rely entirely on open-source weights (Gemma, DeepSeek, LLaMA) and frameworks (Ollama, LangChain) to guarantee data sovereignty and compliance with international banking regulations.

## 2. Accuracy & Quality Targets
- **NFR2.1 Baseline Superiority:** The chosen model and architecture must strive to achieve an F1-Score of at least 85%, with a primary goal of demonstrating a statistically significant improvement in Precision and Recall over the manual human extraction baseline (which sits around 75-80%).
- **NFR2.2 Low Hallucination Tolerance:** The system's prompt engineering and RAG architecture must minimize the hallucination rate to under 5%. In compliance, false positives (alerting on innocent parties) create high operational friction, while false negatives (missing risks) expose the business to massive regulatory fines.

## 3. Performance & Operational Efficiency
- **NFR3.1 Processing Speed (Latency):** The system must reduce the analysis turnaround time from hours/days (manual review) to minutes. Batch processing optimizations should enable the processing of hundreds of news articles systematically within standard operational windows (e.g., overnight batching).
- **NFR3.2 Cost Efficiency:** The architecture must be designed to run on standard modern hardware or affordable local GPU instances, demonstrating an estimated 60-80% operational cost saving compared to maintaining a team of dedicated manual compliance analysts.
- **NFR3.3 Hardware Utilization:** The system must efficiently manage GPU/CPU memory boundaries during inference to prevent Out-Of-Memory (OOM) crashes when cycling between multiple LLMs (e.g., unloading weights appropriately in Ollama).

## 4. Scalability, Resumability & Modularity
- **NFR4.1 Pluggable LLM Architecture:** The software must use abstract interfaces (such as LangChain wrappers) so that adding, removing, or updating underlying local LLMs requires only configuration changes rather than extensive code rewrites.
- **NFR4.2 Horizontal Scalability via Pub/Sub:** The system's processing capacity must be horizontally scalable. By using a local Pub/Sub queue, additional worker processes can be spun up on the same machine (or network) to consume pending articles concurrently, strictly limited by available hardware (GPU/CPU).
- **NFR4.3 Fault Tolerance & Resumability:** The system must guarantee fault tolerance. In the event of a power failure, OOM crash, or manual termination, the queue must persist the state so the process can be safely resumed without data corruption or redundant re-execution.

## 5. Usability & Localization
- **NFR5.1 Spanish Language Dominance & Multilingual Extraction:** All prompt engineering templates must be elaborated in Spanish since the target audience consists of Latin American compliance analysts (specifically Chilean compliance officers). However, the final evaluation metrics and extraction results must be tested on English and multilingual news feeds (such as Kleptotrace/CoNLL-2002) to evaluate cross-lingual NER precision and robustness.
- **NFR5.2 Reproducibility for Research:** As an academic MTI thesis project, all configurations, hyper-parameters (temperature, max_tokens, seeds), and datasets must be fully documented and version-controlled to guarantee the scientific reproducibility of the benchmark results.
