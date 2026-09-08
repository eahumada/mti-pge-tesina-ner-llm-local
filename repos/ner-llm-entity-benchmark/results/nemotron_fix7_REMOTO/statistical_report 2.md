# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 31.9597
- **p-Value:** 1.0672e-04

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| nemotron-mini:4b_baseline | 7 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| nemotron-mini:4b_kb_rag | 7 | 0.4192 | 0.2378 | 0.6007 | 0.1962 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| nemotron-mini:4b_baseline vs nemotron-mini:4b_kb_rag | 0.4192 | 1.0000e-04 | ✅ Yes | [0.2577, 0.5808] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 2010.9 characters.
- **Outlier Records Identified:** 1 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| nemotron-mini:4b_baseline | 0.0000 | 0.0000 | +0.0000 | ⚖️ Stable |
| nemotron-mini:4b_kb_rag | 0.4192 | 0.4601 | +0.0409 | 📈 Improved |