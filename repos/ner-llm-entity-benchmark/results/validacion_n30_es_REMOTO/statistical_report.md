# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 3.1631
- **p-Value:** 9.2824e-03

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:latest_baseline | 30 | 0.8753 | 0.8239 | 0.9266 | 0.1375 |
| gemma4:latest_kb_rag | 30 | 0.8843 | 0.8418 | 0.9268 | 0.1138 |
| llama3.1:8b_baseline | 30 | 0.7562 | 0.6977 | 0.8147 | 0.1567 |
| llama3.1:8b_kb_rag | 30 | 0.8378 | 0.7853 | 0.8903 | 0.1406 |
| mistral-nemo:latest_baseline | 30 | 0.8301 | 0.7742 | 0.8860 | 0.1497 |
| mistral-nemo:latest_kb_rag | 30 | 0.8446 | 0.7929 | 0.8962 | 0.1383 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:latest_baseline vs gemma4:latest_kb_rag | 0.0090 | 9.9990e-01 | ❌ No | [-0.0952, 0.1133] |
| gemma4:latest_baseline vs llama3.1:8b_baseline | -0.1191 | 1.4900e-02 | ✅ Yes | [-0.2234, -0.0149] |
| gemma4:latest_baseline vs llama3.1:8b_kb_rag | -0.0375 | 9.0500e-01 | ❌ No | [-0.1417, 0.0667] |
| gemma4:latest_baseline vs mistral-nemo:latest_baseline | -0.0452 | 8.1160e-01 | ❌ No | [-0.1494, 0.0590] |
| gemma4:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0307 | 9.5760e-01 | ❌ No | [-0.1349, 0.0735] |
| gemma4:latest_kb_rag vs llama3.1:8b_baseline | -0.1282 | 6.6000e-03 | ✅ Yes | [-0.2324, -0.0240] |
| gemma4:latest_kb_rag vs llama3.1:8b_kb_rag | -0.0465 | 7.9210e-01 | ❌ No | [-0.1507, 0.0577] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_baseline | -0.0542 | 6.6500e-01 | ❌ No | [-0.1584, 0.0500] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.0398 | 8.8110e-01 | ❌ No | [-0.1440, 0.0645] |
| llama3.1:8b_baseline vs llama3.1:8b_kb_rag | 0.0817 | 2.1720e-01 | ❌ No | [-0.0226, 0.1859] |
| llama3.1:8b_baseline vs mistral-nemo:latest_baseline | 0.0739 | 3.2160e-01 | ❌ No | [-0.0303, 0.1782] |
| llama3.1:8b_baseline vs mistral-nemo:latest_kb_rag | 0.0884 | 1.4680e-01 | ❌ No | [-0.0158, 0.1926] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_baseline | -0.0077 | 9.9990e-01 | ❌ No | [-0.1119, 0.0965] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_kb_rag | 0.0068 | 1.0000e+00 | ❌ No | [-0.0974, 0.1110] |
| mistral-nemo:latest_baseline vs mistral-nemo:latest_kb_rag | 0.0145 | 9.9870e-01 | ❌ No | [-0.0897, 0.1187] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 362.6 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:latest_baseline | 0.8753 | 0.8753 | +0.0000 | ⚖️ Stable |
| gemma4:latest_kb_rag | 0.8843 | 0.8843 | +0.0000 | ⚖️ Stable |
| llama3.1:8b_baseline | 0.7562 | 0.7562 | +0.0000 | ⚖️ Stable |
| llama3.1:8b_kb_rag | 0.8378 | 0.8378 | +0.0000 | ⚖️ Stable |
| mistral-nemo:latest_baseline | 0.8301 | 0.8301 | +0.0000 | ⚖️ Stable |
| mistral-nemo:latest_kb_rag | 0.8446 | 0.8446 | +0.0000 | ⚖️ Stable |