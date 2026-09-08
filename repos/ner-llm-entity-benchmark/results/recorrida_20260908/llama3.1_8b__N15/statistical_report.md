# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 1.1208
- **p-Value:** 2.9880e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| llama3.1:8b_baseline | 15 | 0.6860 | 0.6172 | 0.7547 | 0.1241 |
| llama3.1:8b_kb_rag | 15 | 0.7334 | 0.6662 | 0.8006 | 0.1214 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| llama3.1:8b_baseline vs llama3.1:8b_kb_rag | 0.0475 | 2.9880e-01 | ❌ No | [-0.0444, 0.1393] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 13483.0 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| llama3.1:8b_baseline | 0.6860 | 0.6860 | +0.0000 | ⚖️ Stable |
| llama3.1:8b_kb_rag | 0.7334 | 0.7334 | +0.0000 | ⚖️ Stable |