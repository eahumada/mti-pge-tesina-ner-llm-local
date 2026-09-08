# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 1.1784
- **p-Value:** 2.8218e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:12b-mlx_baseline | 30 | 0.8983 | 0.8534 | 0.9432 | 0.1202 |
| gemma4:12b-mlx_kb_rag | 30 | 0.8630 | 0.8140 | 0.9121 | 0.1313 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:12b-mlx_baseline vs gemma4:12b-mlx_kb_rag | -0.0353 | 2.8220e-01 | ❌ No | [-0.1003, 0.0298] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 286.2 characters.
- **Outlier Records Identified:** 1 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:12b-mlx_baseline | 0.8983 | 0.8948 | -0.0035 | 📉 Decreased |
| gemma4:12b-mlx_kb_rag | 0.8630 | 0.8652 | +0.0022 | 📈 Improved |