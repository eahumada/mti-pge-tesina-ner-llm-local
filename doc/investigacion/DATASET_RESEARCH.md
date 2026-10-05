# Dataset Recommendation: Sanctions Entity Extraction

## 1. Recommended Primary Dataset: Kleptotrace/CoNLL-2002
The **balanced Kleptotrace/CoNLL-2002/CoNLL-2002 dataset** is recommended as the primary "golden" benchmark for this project.

### Why it is suitable:
- **Domain Alignment**: Specifically designed for high-level corruption, sanctions evasion, and financial crime.
- **Content**: Combines unstructured news articles with ground truth entity labels (NER).
- **Format**: Provided in JSON, making it compatible with the project's current `JSONL/CSV` ingestion pipeline.
- **Academic Validity**: Used in recent (2024) peer-reviewed research for LLM-based entity extraction.

### Acquisition:
- **Data Source**: [Zenodo (Record 14027005)](https://zenodo.org/records/14027005)
- **Reference Implementation**: [GitHub (panagiotis-koletsis/Kleptotrace/CoNLL-2002Dataset)](https://github.com/panagiotis-koletsis/Kleptotrace/CoNLL-2002Dataset)

---

## 2. Complementary Resources for Pipeline Scaling

### For Large-Scale Domain Adaptation: **OFAC Recent Announcements**
- **Source**: [HuggingFace (`emperor-mew/ofac-recent`)](https://huggingface.co/datasets/emperor-mew/ofac-recent)
- **Purpose**: Provides ~4,600 official press releases. Use these as a high-volume corpus to fine-tune prompts or perform distant supervision before moving to the smaller "golden" Kleptotrace/CoNLL-2002 set.

### For Ground Truth Lists (The "Golden Lists"): **OpenSanctions / Trade Screening**
- **Source**: [HuggingFace (`emperor-mew/trade-screening`)](https://huggingface.co/datasets/emperor-mew/trade-screening) or OpenSanctions API.
- **Purpose**: Provides the official SDN and Consolidated Screening Lists. These are used to verify if an extracted entity actually exists on a sanctions list.

---

## 3. Architecture Integration (Mapping to User Stories)

| Dataset | Project Component | Mapped User Story | Integration Path |
| :--- | :--- | :--- | :--- |
| **Kleptotrace/CoNLL-2002** | `src/data_loader.py` | **US01** (Ingestion) & **US02** (Ground Truth) | Load JSON records as the primary evaluation corpus for F1/Precision/Recall calculations. |
| **OFAC Recent** | `src/llm_runner.py` | **US03** (RAG) & **US15** (Localization) | Use as a diverse set of examples for "few-shot" prompting to improve Spanish/English extraction. |
| **Trade Screening** | `src/evaluator.py` | **US07** (Fuzzy Matching) | Use as the master list for the fuzzy matching logic to verify "True Positives". |
