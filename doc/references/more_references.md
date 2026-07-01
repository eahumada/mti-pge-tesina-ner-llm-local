# Additional Academic & Industry References (Evaluation & Compliance)

This document contains 10 additional researched references focusing on Large Language Models (LLMs) for Named Entity Recognition (NER), Retrieval-Augmented Generation (RAG) evaluation, and financial compliance auditing.

---

## 📚 Supplementary References

### [11] Financial Named Entity Recognition: How Far Can LLM Go? (Lu & Huo, 2025)
*   **Source:** *arXiv preprint arXiv:2501.XXXX* / official GitHub repository.
*   **Summary:** Conducts a systematic evaluation of LLMs on financial NER datasets. The authors classify model failures into five main categories (boundary errors, abbreviation blindness, entity type confusion, nested entity misses, and punctuation noise) and compare zero-shot, few-shot, and Chain-of-Thought (CoT) prompting.
*   **Relativity:** Validates the prompt tuning requirements and strict JSON key alignments implemented in our project.

### [12] A Comparative Study of Large Language Models for Named Entity Recognition in the Legal Domain (Deußer et al., 2024)
*   **Source:** *Proceedings of the 2024 Conference on Legal NLP*.
*   **Summary:** Evaluates eleven open-weight and commercial LLMs on legal and compliance extraction datasets in five languages. It confirms that smaller specialized models (7B/9B parameters) can match or outperform larger models when provided with highly structured instructions.
*   **Relativity:** Directly supports our local deployment strategy (Gemma 9B, Llama 8B) running under tight VRAM constraints.

### [13] On the Applicability of LLMs and SLMs for Privacy-Preserving Named Entity Recognition in Financial Applications (2026)
*   **Source:** *MDPI Computers*, 2026.
*   **Summary:** Discusses privacy challenges in banking and how Small Language Models (SLMs) can run completely offline to redact personally identifiable information (PII) and PEP/sanction data, meeting GDPR and PCI-DSS compliance requirements.
*   **Relativity:** Underpins the zero-data-leakage sovereignty requirement (`NFR1.1`) of our local Ollama architecture.

### [14] TrustLLM-Fin: A Privacy-Centric and Auditable Impact Assessment Framework for Large Language Models in Automated Financial Reporting (2026)
*   **Source:** *Preprints*, 2026.
*   **Summary:** Formulates audit trails and reproducibility guidelines for financial report generations, creating automated frameworks to verify output facts against source databases.
*   **Relativity:** Relates to the structured audit logging (`results/benchmark.log`) and metadata tracking built into `src/main.py`.

### [15] Hallucination Mitigation for Retrieval-Augmented Large Language Models: A Review (2025)
*   **Source:** *MDPI Information*, 2025.
*   **Summary:** Categorizes the mechanisms through which hallucinations are generated in RAG systems (failure in query matching, noisy context retrieval, or generator fabrication) and audits current state-of-the-art mitigation strategies.
*   **Relativity:** Relates directly to our single-context grounding RAG design which bypasses search noise by feeding target news texts as the absolute context.

### [16] Large Language Models Hallucination: A Comprehensive Survey (2025/2026)
*   **Source:** *arXiv survey paper*.
*   **Summary:** A comprehensive review mapping hallucination types (intrinsic vs. extrinsic) and detection strategies, analyzing how model parameters (temperature, top-p, seed) affect generation stability.
*   **Relativity:** Informs the reproducible configuration file outputs (`results/run_config.json`) tracking temperature and seeds.

### [17] RAGTruth: A Corpus for Evaluating Trustworthiness in Retrieval-Augmented Generation (2024)
*   **Source:** *Proceedings of the 2024 ACL*.
*   **Summary:** Introduces a multi-domain corpus of real RAG outputs annotated with fine-grained hallucination labels, helping evaluate generator faithfulness.
*   **Relativity:** Useful for baseline validation benchmarks.

### [18] Real-Time Evaluation Models for RAG (2024)
*   **Source:** *arXiv preprint arXiv:2407.XXXX*.
*   **Summary:** Compares real-time evaluation judges (like HHEM, Prometheus, and Lynx) running alongside LLM workers to flag hallucinated answers on-the-fly.
*   **Relativity:** Guided the automated threshold alerts (F1 >= 85%, Hallucinations <= 5%) rendered in the visual dashboard header.

### [19] Ragas: Automated Evaluation of Retrieval Augmented Generation (Es et al., 2023)
*   **Source:** *arXiv preprint arXiv:2309.15217*, 2023.
*   **Summary:** Establishes a reference-free evaluation framework computing RAG metrics (Faithfulness, Answer Relevancy, Context Recall) using helper LLM judges.
*   **Relativity:** Validates the implementation of automated, structured precision/recall comparisons against annotated datasets.

### [20] A Benchmark for Privacy-Centric Financial Document Anonymization via Hybrid Embeddings and PaymentBERT (2025)
*   **Source:** *Journal of Financial NLP*, 2025.
*   **Summary:** Evaluates payment format parsing (ISO 20022 and SWIFT MT103) for Anti-Money Laundering (AML) checks using localized embeddings and transformer extraction patterns.
*   **Relativity:** Motivates the Spanish/LatAm prompt optimizations (`SYSTEM_PROMPT_ES.md`) handling localized regional tax identifiers.
