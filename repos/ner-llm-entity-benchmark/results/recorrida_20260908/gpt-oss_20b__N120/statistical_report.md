# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.7841
- **p-Value:** 3.7684e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gpt-oss:20b_baseline | 113 | 0.7541 | 0.7268 | 0.7815 | 0.1466 |
| gpt-oss:20b_kb_rag | 113 | 0.7708 | 0.7454 | 0.7961 | 0.1359 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gpt-oss:20b_baseline vs gpt-oss:20b_kb_rag | 0.0167 | 3.7680e-01 | ❌ No | [-0.0204, 0.0537] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 7 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gpt-oss:20b_baseline | 0.7541 | 0.7544 | +0.0003 | 📈 Improved |
| gpt-oss:20b_kb_rag | 0.7708 | 0.7708 | +0.0001 | ⚖️ Stable |