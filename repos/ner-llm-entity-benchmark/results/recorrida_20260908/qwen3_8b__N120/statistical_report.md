# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.0006
- **p-Value:** 9.8005e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| qwen3:8b_baseline | 113 | 0.6903 | 0.6607 | 0.7199 | 0.1586 |
| qwen3:8b_kb_rag | 113 | 0.6898 | 0.6614 | 0.7182 | 0.1523 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| qwen3:8b_baseline vs qwen3:8b_kb_rag | -0.0005 | 9.8010e-01 | ❌ No | [-0.0413, 0.0403] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 7 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| qwen3:8b_baseline | 0.6903 | 0.6927 | +0.0024 | 📈 Improved |
| qwen3:8b_kb_rag | 0.6898 | 0.6900 | +0.0002 | 📈 Improved |