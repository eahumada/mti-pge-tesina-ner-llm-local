# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.4630
- **p-Value:** 4.9895e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma:latest_baseline | 30 | 0.8008 | 0.7391 | 0.8625 | 0.1652 |
| gemma:latest_kb_rag | 30 | 0.7715 | 0.7086 | 0.8344 | 0.1685 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma:latest_baseline vs gemma:latest_kb_rag | -0.0293 | 4.9900e-01 | ❌ No | [-0.1155, 0.0569] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 286.2 characters.
- **Outlier Records Identified:** 1 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma:latest_baseline | 0.8008 | 0.7960 | -0.0048 | 📉 Decreased |
| gemma:latest_kb_rag | 0.7715 | 0.7766 | +0.0051 | 📈 Improved |