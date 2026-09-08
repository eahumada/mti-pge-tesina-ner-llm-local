# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 1.7236
- **p-Value:** 1.9050e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gpt-oss:20b_baseline | 120 | 0.5239 | 0.4885 | 0.5594 | 0.1961 |
| gpt-oss:20b_kb_rag | 120 | 0.5567 | 0.5222 | 0.5912 | 0.1910 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gpt-oss:20b_baseline vs gpt-oss:20b_kb_rag | 0.0328 | 1.9050e-01 | ❌ No | [-0.0164, 0.0820] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 2610.3 characters.
- **Outlier Records Identified:** 14 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gpt-oss:20b_baseline | 0.5239 | 0.5169 | -0.0070 | 📉 Decreased |
| gpt-oss:20b_kb_rag | 0.5567 | 0.5417 | -0.0150 | 📉 Decreased |