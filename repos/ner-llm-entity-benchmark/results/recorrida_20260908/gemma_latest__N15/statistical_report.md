# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.3563
- **p-Value:** 5.5535e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma:latest_baseline | 15 | 0.6572 | 0.5614 | 0.7529 | 0.1729 |
| gemma:latest_kb_rag | 15 | 0.6888 | 0.6274 | 0.7502 | 0.1109 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma:latest_baseline vs gemma:latest_kb_rag | 0.0317 | 5.5540e-01 | ❌ No | [-0.0770, 0.1403] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 13483.0 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma:latest_baseline | 0.6572 | 0.6572 | +0.0000 | ⚖️ Stable |
| gemma:latest_kb_rag | 0.6888 | 0.6888 | +0.0000 | ⚖️ Stable |