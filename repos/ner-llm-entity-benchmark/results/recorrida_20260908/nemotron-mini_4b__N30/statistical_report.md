# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 9.6565
- **p-Value:** 2.9207e-03

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| nemotron-mini:4b_baseline | 30 | 0.4799 | 0.4134 | 0.5464 | 0.1781 |
| nemotron-mini:4b_kb_rag | 30 | 0.6247 | 0.5564 | 0.6930 | 0.1828 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| nemotron-mini:4b_baseline vs nemotron-mini:4b_kb_rag | 0.1448 | 2.9000e-03 | ✅ Yes | [0.0515, 0.2381] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 286.2 characters.
- **Outlier Records Identified:** 1 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| nemotron-mini:4b_baseline | 0.4799 | 0.4849 | +0.0051 | 📈 Improved |
| nemotron-mini:4b_kb_rag | 0.6247 | 0.6359 | +0.0112 | 📈 Improved |