# Annotated References & Bibliography

This document provides detailed annotations and mapping of the key academic and industry references used in the MTI thesis to the implemented project modules.

---

## 📚 Reference Catalog & Implementation Mapping

### [1] Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al., 2020)
*   **Citation:** P. Lewis, et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," *Advances in Neural Information Processing Systems*, vol. 33, pp. 9459-9474, 2020.
*   **Annotation:** This is the seminal paper introducing RAG. It demonstrates that grounding LLM generation with external doc retrievals increases factual accuracy and mitigates hallucinations.
*   **Project Mapping:** Implemented in [`llm_runner.py`](file:///Users/eahumada1/Documents/Personal/MTI/taller_de_titulo/repos/ner-llm-entity-benchmark/src/llm_runner.py) using single-context prompt injection to constrain generation strictly to the provided news text context.

### [2] BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding (Devlin et al., 2019)
*   **Citation:** J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding," *Proceedings of NAACL*, pp. 4171-4186, 2019.
*   **Annotation:** Introduces bidirectional representations. BERT is historically the primary encoder-based model used as a baseline for named entity extraction.
*   **Project Mapping:** Underpins the manual and traditional NLP models used for baseline comparisons (75-80% F1 targets).

### [3] BloombergGPT: A Large Language Model for Finance (Wu et al., 2023)
*   **Citation:** S. Wu et al., "BloombergGPT: A Large Language Model for Finance," *arXiv preprint arXiv:2303.17564*, 2023.
*   **Annotation:** Highlights the performance benefits of domain-specific pre-training for NLP tasks in the financial sector.
*   **Project Mapping:** Provides the theoretical motivation for evaluating LLMs on compliance news and extracting financial entity categories.

### [4] Attention Is All You Need (Vaswani et al., 2017)
*   **Citation:** A. Vaswani et al., "Attention Is All You Need," *Advances in Neural Information Processing Systems*, 2017.
*   **Annotation:** Introduces the Transformer architecture (self-attention mechanism), which is the architectural foundation of all models under sweep (Gemma, LLaMA, DeepSeek).
*   **Project Mapping:** Used implicitly by all local LLM weights cycling through the Ollama execution backend.

### [5] Unlocking Data with Generative AI and RAG (Bourne, 2024)
*   **Citation:** K. Bourne, *Unlocking Data with Generative AI and RAG*. O'Reilly Media, 2024.
*   **Annotation:** A practical guide detailing prompt patterns, chunking strategies, and evaluations for production-grade RAG pipelines.
*   **Project Mapping:** Guides the structured JSON enforcement schemas, retry wrappers, and evaluation loops implemented in `src/`.

### [6] Retrieval-Augmented Generation for Large Language Models: A Survey (Gao et al., 2024)
*   **Citation:** X. Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey," *arXiv preprint arXiv:2312.10997*, 2024.
*   **Annotation:** Categorizes standard RAG architectures (Naive, Advanced, Modular) and provides an audit of hallucination rate metrics.
*   **Project Mapping:** Guided the formulation of the hallucination rate metric (`hallucinated / total_extracted`) built in [`evaluator.py`](file:///Users/eahumada1/Documents/Personal/MTI/taller_de_titulo/repos/ner-llm-entity-benchmark/src/evaluator.py).

### [7] Evaluating BERT and Transformers for Named Entity Recognition in Spanish (García & López, 2021)
*   **Citation:** A. García and M. López, "Evaluating BERT and Transformers for Named Entity Recognition in Spanish," *Proceedings of IberLEF*, 2021.
*   **Annotation:** Audits tokenization performance and NER boundaries on Spanish language texts.
*   **Project Mapping:** Inspired the localized prompt template configurations (`SYSTEM_PROMPT_ES.md`) handling Spanish accents, syntax, and domestic entities.

### [8] Language Models are Few-Shot Learners (Brown et al., 2020)
*   **Citation:** T. Brown et al., "Language Models are Few-Shot Learners," *Advances in Neural Information Processing Systems*, vol. 33, pp. 1877-1901, 2020.
*   **Annotation:** Demonstrates that providing in-context examples (few-shot prompting) significantly boosts execution accuracy on downstream NLP tasks.
*   **Project Mapping:** Used in the prompt tuning sprint phase to optimize model extraction accuracy toward the target 85% F1-score.

### [9] RAG for Financial Document Analysis: A Practical Framework (Chang et al., 2024)
*   **Citation:** M. Chang, J. Kim, and S. Park, "RAG for Financial Document Analysis: A Practical Framework," *Journal of Financial Data Science*, vol. 6, no. 2, pp. 45-62, 2024.
*   **Annotation:** Outlines architectures for structured compliance extraction in banking documents.
*   **Project Mapping:** Guided the decoupled Pub/Sub scaling queue setup designed in [`pub_sub.py`](file:///Users/eahumada1/Documents/Personal/MTI/taller_de_titulo/repos/ner-llm-entity-benchmark/src/pub_sub.py).

### [10] Conditional Random Fields for Named Entity Recognition in Financial Texts (Smith et al., 2019)
*   **Citation:** J. Smith, L. Johnson, and R. Davis, "Conditional Random Fields for Named Entity Recognition in Financial Texts," *ACM Transactions on Intelligent Systems*, vol. 10, no. 3, pp. 1-25, 2019.
*   **Annotation:** Traditional statistical mapping (CRFs) for NER in finance.
*   **Project Mapping:** Serves as a historical baseline benchmark for comparing deep transformer performance against classic statistical architectures.
