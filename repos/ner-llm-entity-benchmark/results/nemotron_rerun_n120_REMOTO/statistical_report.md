# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 4.0551
- **p-Value:** 4.5164e-02

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| nemotron-mini:4b_baseline | 120 | 0.3650 | 0.3085 | 0.4214 | 0.3123 |
| nemotron-mini:4b_kb_rag | 120 | 0.4378 | 0.3937 | 0.4819 | 0.2440 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| nemotron-mini:4b_baseline vs nemotron-mini:4b_kb_rag | 0.0729 | 4.5200e-02 | ✅ Yes | [0.0016, 0.1441] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 2610.3 characters.
- **Outlier Records Identified:** 14 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| nemotron-mini:4b_baseline | 0.3650 | 0.3703 | +0.0053 | 📈 Improved |
| nemotron-mini:4b_kb_rag | 0.4378 | 0.4353 | -0.0026 | 📉 Decreased |