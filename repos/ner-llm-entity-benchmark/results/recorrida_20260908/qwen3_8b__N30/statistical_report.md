# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.5388
- **p-Value:** 4.6590e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| qwen3:8b_baseline | 30 | 0.7685 | 0.7093 | 0.8277 | 0.1586 |
| qwen3:8b_kb_rag | 30 | 0.7997 | 0.7360 | 0.8634 | 0.1706 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| qwen3:8b_baseline vs qwen3:8b_kb_rag | 0.0312 | 4.6590e-01 | ❌ No | [-0.0539, 0.1163] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 286.2 characters.
- **Outlier Records Identified:** 1 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| qwen3:8b_baseline | 0.7685 | 0.7674 | -0.0011 | 📉 Decreased |
| qwen3:8b_kb_rag | 0.7997 | 0.8026 | +0.0029 | 📈 Improved |