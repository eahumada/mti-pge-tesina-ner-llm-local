# MTI Thesis: Project Sprint Schedule

This document outlines the bi-weekly sprint schedule to track progress toward final thesis deadlines.

## Sprint 1: Requirements Mapping & Setup (July 1 - July 14, 2026)
*   **Goal:** Establish Traceability Matrix and map manual baseline dataset.
*   **Tasks:**
    *   Complete `doc/TRACEABILITY_MATRIX.md` mapping implemented features to functional requirements.
    *   Assemble and document the manual baseline (75-80% F1 score) dataset targets.

## Sprint 2: Stress Testing & Stability (July 15 - July 28, 2026)
*   **Goal:** Conduct reliability and VRAM stress testing.
*   **Tasks:**
    *   Develop long-run memory utilization stress test scripts.
    *   Verify VRAM model weight unloading lifecycles and optimize Ollama model cycling under low-resource environments.

## Sprint 3: Large-Scale Dataset Expansion (July 29 - August 11, 2026)
*   **Goal:** Expand testing from the 20-record prototype sample to the full compliance news corpus.
*   **Tasks:**
    *   Ingest the full sanctions news dataset.
    *   Verify strict schema validation performance under higher load.

## Sprint 4: Benchmarking & Academic reporting (August 12 - August 25, 2026)
*   **Goal:** Complete multi-model sweeps and finalize thesis statistical validation.
*   **Tasks:**
    *   Execute full evaluations across Gemma, LLaMA, and DeepSeek.
    *   Process ANOVA and Tukey HSD Adjusted p-values.
    *   Export final segment confusion matrices and compile the final research report.
