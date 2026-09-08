# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 1.7239
- **p-Value:** 1.9054e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:latest_baseline | 113 | 0.7533 | 0.7257 | 0.7809 | 0.1479 |
| gemma4:latest_kb_rag | 113 | 0.7786 | 0.7522 | 0.8050 | 0.1416 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:latest_baseline vs gemma4:latest_kb_rag | 0.0253 | 1.9050e-01 | ❌ No | [-0.0127, 0.0633] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 7 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:latest_baseline | 0.7533 | 0.7548 | +0.0015 | 📈 Improved |
| gemma4:latest_kb_rag | 0.7786 | 0.7771 | -0.0015 | 📉 Decreased |