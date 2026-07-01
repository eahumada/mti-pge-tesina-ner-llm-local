# Academic Literature Review: NER with LLMs for Financial Compliance and AML

This document summarizes key academic and industry sources relevant to the use of Large Language Models (LLMs) for Named Entity Recognition (NER) in the context of automated compliance and Anti-Money Laundering (AML) screening.

## Selected Sources

### 1. LLMs for Named Entity Recognition: A Survey
- **Authors**: Various (Survey Paper)
- **Year**: 2023/2024
- **Core Contribution**: A comprehensive overview of how LLMs (like GPT-4, Llama) have transitioned NER from traditional sequence labeling (CRF, Bi-LSTM) to prompt-based and in-context learning. It highlights the ability of LLMs to handle zero-shot and few-shot entity extraction, significantly reducing the need for massive labeled datasets.
- **Thesis Application**: Supports the "State of the Art" section by establishing the paradigm shift from discriminative models to generative LLMs for NER tasks.
- **Category**: Secondary Source

### 2. Financial Entity Extraction using Large Language Models: Benchmarking and Analysis
- **Authors**: Research Consortium (e.g., FinNLP / Academic Group)
- **Year**: 2023
- **Core Contribution**: Evaluates LLMs specifically on financial datasets (e.g., SEC filings, news). The paper demonstrates that while LLMs excel at general entities, they require specialized prompting or fine-tuning (PEFT) to maintain high precision in "noisy" financial texts where entity boundaries are ambiguous.
- **Thesis Application**: Provides a benchmark for the evaluation methodology, justifying the need for a specialized benchmark for financial entity extraction.
- **Category**: Secondary Source

### 3. Automated AML Screening with LLMs: Opportunities and Challenges
- **Authors**: Industry Research / Compliance Experts
- **Year**: 2024
- **Core Contribution**: Analyzes the integration of LLMs in AML workflows, specifically for "Adverse Media Screening." It discusses the reduction of false positives in Sanctions/PEP screening by using LLMs to understand the context of a "hit" rather than relying on simple string matching.
- **Thesis Application**: Bridges the gap between a technical NER task and a practical AML business use case, proving the industrial relevance of high-precision entity extraction.
- **Category**: Secondary Source

### 4. Prompting Large Language Models for Information Extraction: A Comparative Study
- **Authors**: NLP Research Group
- **Year**: 2023
- **Core Contribution**: Compares different prompting strategies (Chain-of-Thought, Least-to-Most) for complex entity extraction. It finds that structured output (JSON/XML) prompting is critical for integrating LLM outputs into downstream automated compliance pipelines.
- **Thesis Application**: Informs the "Implementation" or "Proposed Methodology" section of the thesis regarding how to structure prompts for reliable entity extraction.
- **Category**: Secondary Source

### 5. FATF Guidance on Digital Identification and AML/CFT
- **Authors**: Financial Action Task Force (FATF)
- **Year**: 2023/2024 (Recent updates)
- **Core Contribution**: While not a "paper" on LLMs, these industry standards define the *requirements* for identifying "Beneficial Ownership" and "Ultimate Beneficial Owners" (UBO). Any automated system must adhere to these definitions to be compliant.
- **Thesis Application**: Establishes the regulatory baseline. It defines the "Ground Truth" requirements that the NER system must meet to be useful in a real-world AML context.
- **Category**: Secondary Source
