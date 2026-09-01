# Project Integration & Evaluation Results

This document presents the implementation findings and results from the local LLM compliance evaluation run on the primary golden benchmark dataset.

## 1. System Integration Status
All core functional and non-functional requirements mapped from the MTI thesis goals are fully implemented and integrated. Below is the confirmation status:

| Project Component | Target Mapped Requirement | Verification & Status |
| :--- | :--- | :--- |
| **Data Ingestion** | `RF1.1`, `FR5.1`, `FR5.3` | **Pass:** Loads JSON, JSONL, XML, CSV, and IOB files dynamically. Rejects malformed structures via `validate_record_schema`. Links every record trace to model version, prompt hash, and timestamp. |
| **Cohen's Kappa Tool** | `RF1.2`, `RF1.3` | **Pass:** Computes categorization agreement via CLI option `--compare-annotators FILE1 FILE2`. Logs warning banners if Kappa agreement score falls below `0.75`. |
| **Spanish Prompting** | `NFR5.1` | **Pass:** Deployed `SYSTEM_PROMPT_ES.md` optimized for Latin American tax identifiers (e.g. RUT, RFC, RUN) and regional domestic fraud. |
| **VRAM Model Rotation** | `NFR3.3`, `FR5.2` | **Pass:** Rotates LLM lifecycle parameters dynamically. Unloads previous model weights from VRAM before loading the next sweep candidate. |
| **Sensitivity Analysis** | `FR3.4` | **Pass:** Dynamically filters outlier articles (length > average + 500 characters) and evaluates performance delta to verify robustness. |
| **Acceptance Banners** | `NFR7.1` | **Pass:** Compares F1 scores and hallucination rates against target criteria (F1 >= 85%, Hallucination <= 5%) and outputs warnings on top of the dashboard. |
| **Production Simulation** | `FR4.2`, `FR4.3` | **Pass:** Runs batch flow simulation (`simulate_production.py`) and collects qualitative stakeholder feedback (Tab 6 in dashboard). |

---

## 2. Benchmark Sweep Results (`gemma4` on Kleptotrace/CoNLL-2002)
A full benchmark sweep was run on the **Kleptotrace/CoNLL-2002** primary dataset using the local Ollama backend with model `gemma4`. Below are the metrics compiled:

* **Evaluation Dataset:** `data/benchmark_balanced_120.json` (15 representative compliance articles)
* **LLM Temperature:** 0.1
* **VRAM footprint limit:** under 16GB (local execution check)

### Overall Performance Metrics
| Model | Overall F1-Score | Precision | Recall | Hallucination Rate | Avg Latency / Art |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **gemma4** | **42.41%** | 69.20% | 54.49% | **0.20%** | 25.27 seconds |

*Verdict:* The local `gemma4` model demonstrated extreme sovereignty and hallucination control (**0.20% rate**, far below the target 5% limit), but the overall F1-Score (**42.41%**) did not meet the target acceptance threshold of 85%. This indicates prompt adjustments or larger model sweeps (e.g. LLaMA 70B) are needed.

---

## 3. Sensitivity Analysis Output
Outliers (length > 1856.2 characters) were isolated to measure model robustness under noisy contexts:

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Robustness Status |
| :--- | :---: | :---: | :---: | :---: |
| **gemma4** | 0.4241 | **0.5084** | **+0.0842** | 📈 Improved |

*Verdict:* Excluding outlier long articles significantly increased the F1 score by **+8.42%**, demonstrating that article length/complexity is a strong performance inhibitor for the local model.
