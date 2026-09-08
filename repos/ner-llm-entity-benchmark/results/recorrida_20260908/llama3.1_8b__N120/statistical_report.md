# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 1.2698
- **p-Value:** 2.6100e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| llama3.1:8b_baseline | 113 | 0.6917 | 0.6637 | 0.7197 | 0.1503 |
| llama3.1:8b_kb_rag | 113 | 0.7148 | 0.6854 | 0.7442 | 0.1576 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| llama3.1:8b_baseline vs llama3.1:8b_kb_rag | 0.0231 | 2.6100e-01 | ❌ No | [-0.0173, 0.0635] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 7 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| llama3.1:8b_baseline | 0.6917 | 0.6922 | +0.0004 | 📈 Improved |
| llama3.1:8b_kb_rag | 0.7148 | 0.7146 | -0.0002 | 📉 Decreased |