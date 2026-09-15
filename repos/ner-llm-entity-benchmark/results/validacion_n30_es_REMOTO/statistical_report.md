# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 1.7446
- **p-Value:** 1.2685e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:latest_baseline | 30 | 0.8402 | 0.7788 | 0.9016 | 0.1645 |
| gemma4:latest_kb_rag | 30 | 0.8527 | 0.7980 | 0.9073 | 0.1463 |
| llama3.1:8b_baseline | 30 | 0.7446 | 0.6859 | 0.8032 | 0.1570 |
| llama3.1:8b_kb_rag | 30 | 0.8186 | 0.7633 | 0.8740 | 0.1481 |
| mistral-nemo:latest_baseline | 30 | 0.8250 | 0.7673 | 0.8826 | 0.1544 |
| mistral-nemo:latest_kb_rag | 30 | 0.8247 | 0.7609 | 0.8885 | 0.1709 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:latest_baseline vs gemma4:latest_kb_rag | 0.0125 | 9.9960e-01 | ❌ No | [-0.1044, 0.1294] |
| gemma4:latest_baseline vs llama3.1:8b_baseline | -0.0956 | 1.7750e-01 | ❌ No | [-0.2125, 0.0213] |
| gemma4:latest_baseline vs llama3.1:8b_kb_rag | -0.0216 | 9.9480e-01 | ❌ No | [-0.1385, 0.0954] |
| gemma4:latest_baseline vs mistral-nemo:latest_baseline | -0.0152 | 9.9900e-01 | ❌ No | [-0.1321, 0.1017] |
| gemma4:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0155 | 9.9890e-01 | ❌ No | [-0.1324, 0.1014] |
| gemma4:latest_kb_rag vs llama3.1:8b_baseline | -0.1081 | 8.7800e-02 | ❌ No | [-0.2250, 0.0088] |
| gemma4:latest_kb_rag vs llama3.1:8b_kb_rag | -0.0340 | 9.5980e-01 | ❌ No | [-0.1509, 0.0829] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_baseline | -0.0277 | 9.8370e-01 | ❌ No | [-0.1446, 0.0892] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.0280 | 9.8290e-01 | ❌ No | [-0.1449, 0.0889] |
| llama3.1:8b_baseline vs llama3.1:8b_kb_rag | 0.0741 | 4.5200e-01 | ❌ No | [-0.0428, 0.1910] |
| llama3.1:8b_baseline vs mistral-nemo:latest_baseline | 0.0804 | 3.5700e-01 | ❌ No | [-0.0365, 0.1973] |
| llama3.1:8b_baseline vs mistral-nemo:latest_kb_rag | 0.0801 | 3.6140e-01 | ❌ No | [-0.0368, 0.1970] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_baseline | 0.0063 | 1.0000e+00 | ❌ No | [-0.1106, 0.1232] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_kb_rag | 0.0060 | 1.0000e+00 | ❌ No | [-0.1109, 0.1229] |
| mistral-nemo:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0003 | 1.0000e+00 | ❌ No | [-0.1172, 0.1166] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 362.6 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:latest_baseline | 0.8402 | 0.8402 | +0.0000 | ⚖️ Stable |
| gemma4:latest_kb_rag | 0.8527 | 0.8527 | +0.0000 | ⚖️ Stable |
| llama3.1:8b_baseline | 0.7446 | 0.7446 | +0.0000 | ⚖️ Stable |
| llama3.1:8b_kb_rag | 0.8186 | 0.8186 | +0.0000 | ⚖️ Stable |
| mistral-nemo:latest_baseline | 0.8250 | 0.8250 | +0.0000 | ⚖️ Stable |
| mistral-nemo:latest_kb_rag | 0.8247 | 0.8247 | +0.0000 | ⚖️ Stable |