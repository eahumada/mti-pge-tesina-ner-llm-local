# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 65.9428
- **p-Value:** 1.1033e-13

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| llama3.1:8b | 15 | 0.5961 | 0.5307 | 0.6614 | 0.1179 |
| nemotron-mini:4b | 15 | 0.4281 | 0.3036 | 0.5526 | 0.2248 |
| minimax-m3:cloud | 15 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| llama3.1:8b vs minimax-m3:cloud | -0.5961 | 0.0000e+00 | ✅ Yes | [-0.7261, -0.4660] |
| llama3.1:8b vs nemotron-mini:4b | -0.1679 | 8.6000e-03 | ✅ Yes | [-0.2980, -0.0379] |
| minimax-m3:cloud vs nemotron-mini:4b | 0.4281 | 0.0000e+00 | ✅ Yes | [0.2981, 0.5582] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 5332.9 characters.
- **Outlier Records Identified:** 6 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| llama3.1:8b | 0.5961 | 0.5891 | -0.0070 | 📉 Decreased |
| minimax-m3:cloud | 0.0000 | 0.0000 | +0.0000 | ⚖️ Stable |
| nemotron-mini:4b | 0.4281 | 0.4425 | +0.0144 | 📈 Improved |