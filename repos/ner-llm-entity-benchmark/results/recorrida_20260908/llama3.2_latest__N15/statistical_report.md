# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.8075
- **p-Value:** 3.7652e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| llama3.2:latest_baseline | 15 | 0.6522 | 0.5583 | 0.7461 | 0.1695 |
| llama3.2:latest_kb_rag | 15 | 0.6973 | 0.6447 | 0.7499 | 0.0950 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| llama3.2:latest_baseline vs llama3.2:latest_kb_rag | 0.0451 | 3.7650e-01 | ❌ No | [-0.0577, 0.1479] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 13483.0 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| llama3.2:latest_baseline | 0.6522 | 0.6522 | +0.0000 | ⚖️ Stable |
| llama3.2:latest_kb_rag | 0.6973 | 0.6973 | +0.0000 | ⚖️ Stable |