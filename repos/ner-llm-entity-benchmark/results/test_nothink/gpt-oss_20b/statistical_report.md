# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 1.9662
- **p-Value:** 1.7184e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gpt-oss:20b_baseline | 15 | 0.3010 | 0.1266 | 0.4754 | 0.3149 |
| gpt-oss:20b_kb_rag | 15 | 0.1549 | 0.0152 | 0.2945 | 0.2522 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gpt-oss:20b_baseline vs gpt-oss:20b_kb_rag | -0.1461 | 1.7180e-01 | ❌ No | [-0.3595, 0.0673] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 2305.3 characters.
- **Outlier Records Identified:** 2 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gpt-oss:20b_baseline | 0.3010 | 0.2978 | -0.0031 | 📉 Decreased |
| gpt-oss:20b_kb_rag | 0.1549 | 0.1293 | -0.0256 | 📉 Decreased |