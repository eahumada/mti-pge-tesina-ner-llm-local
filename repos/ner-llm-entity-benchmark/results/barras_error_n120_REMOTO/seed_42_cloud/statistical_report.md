# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.5284
- **p-Value:** 4.6805e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline | 113 | 0.8162 | 0.7908 | 0.8416 | 0.1365 |
| gemma4:31b-cloud_kb_rag | 113 | 0.8292 | 0.8045 | 0.8539 | 0.1323 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline vs gemma4:31b-cloud_kb_rag | 0.0130 | 4.6800e-01 | ❌ No | [-0.0222, 0.0482] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 7 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline | 0.8162 | 0.8191 | +0.0029 | 📈 Improved |
| gemma4:31b-cloud_kb_rag | 0.8292 | 0.8324 | +0.0032 | 📈 Improved |