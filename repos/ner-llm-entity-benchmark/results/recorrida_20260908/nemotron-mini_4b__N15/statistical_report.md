# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.0474
- **p-Value:** 8.2919e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| nemotron-mini:4b_baseline | 15 | 0.4259 | 0.3287 | 0.5231 | 0.1755 |
| nemotron-mini:4b_kb_rag | 15 | 0.4416 | 0.3218 | 0.5613 | 0.2162 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| nemotron-mini:4b_baseline vs nemotron-mini:4b_kb_rag | 0.0157 | 8.2920e-01 | ❌ No | [-0.1316, 0.1630] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 13483.0 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| nemotron-mini:4b_baseline | 0.4259 | 0.4259 | +0.0000 | ⚖️ Stable |
| nemotron-mini:4b_kb_rag | 0.4416 | 0.4416 | +0.0000 | ⚖️ Stable |