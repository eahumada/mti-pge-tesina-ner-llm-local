# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 26.8847
- **p-Value:** 4.4500e-16

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gpt-oss:20b_baseline | 120 | 0.4467 | 0.3980 | 0.4954 | 0.2695 |
| gpt-oss:20b_kb_rag | 120 | 0.3419 | 0.2862 | 0.3976 | 0.3082 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gpt-oss:20b_baseline vs gpt-oss:20b_kb_rag | -0.1048 | 5.5000e-03 | ✅ Yes | [-0.1864, -0.0233] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 2610.3 characters.
- **Outlier Records Identified:** 14 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gpt-oss:20b_baseline | 0.4467 | 0.4467 | -0.0000 | ⚖️ Stable |
| gpt-oss:20b_kb_rag | 0.3419 | 0.3699 | +0.0280 | 📈 Improved |