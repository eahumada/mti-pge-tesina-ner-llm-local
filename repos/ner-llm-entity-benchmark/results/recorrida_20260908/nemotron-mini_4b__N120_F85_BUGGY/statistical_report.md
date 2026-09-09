# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 26.6263
- **p-Value:** 5.4337e-07

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| nemotron-mini:4b_baseline | 113 | 0.2631 | 0.2208 | 0.3055 | 0.2273 |
| nemotron-mini:4b_kb_rag | 113 | 0.4055 | 0.3709 | 0.4400 | 0.1853 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| nemotron-mini:4b_baseline vs nemotron-mini:4b_kb_rag | 0.1423 | 0.0000e+00 | ✅ Yes | [0.0880, 0.1967] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 7 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| nemotron-mini:4b_baseline | 0.2631 | 0.2577 | -0.0055 | 📉 Decreased |
| nemotron-mini:4b_kb_rag | 0.4055 | 0.4038 | -0.0016 | 📉 Decreased |