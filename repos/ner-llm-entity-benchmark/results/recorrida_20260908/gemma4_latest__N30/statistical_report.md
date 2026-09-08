# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.2777
- **p-Value:** 6.0020e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:latest_baseline | 30 | 0.8730 | 0.8279 | 0.9180 | 0.1207 |
| gemma4:latest_kb_rag | 30 | 0.8556 | 0.8056 | 0.9056 | 0.1339 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:latest_baseline vs gemma4:latest_kb_rag | -0.0173 | 6.0020e-01 | ❌ No | [-0.0832, 0.0485] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 286.2 characters.
- **Outlier Records Identified:** 1 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:latest_baseline | 0.8730 | 0.8686 | -0.0044 | 📉 Decreased |
| gemma4:latest_kb_rag | 0.8556 | 0.8576 | +0.0019 | 📈 Improved |