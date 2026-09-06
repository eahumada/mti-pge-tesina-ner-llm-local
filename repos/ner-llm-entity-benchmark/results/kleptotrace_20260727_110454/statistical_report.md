# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 1.0248
- **p-Value:** 3.8864e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 15 | 0.6676 | 0.5396 | 0.7955 | 0.2310 |
| zs-es | 15 | 0.6793 | 0.5975 | 0.7611 | 0.1477 |
| fs-es | 15 | 0.6987 | 0.6296 | 0.7679 | 0.1249 |
| fs-en | 15 | 0.5817 | 0.4396 | 0.7237 | 0.2565 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | 0.1170 | 3.7580e-01 | ❌ No | [-0.0743, 0.3083] |
| fs-en vs zs-en | 0.0859 | 6.3620e-01 | ❌ No | [-0.1054, 0.2772] |
| fs-en vs zs-es | 0.0976 | 5.3480e-01 | ❌ No | [-0.0937, 0.2889] |
| fs-es vs zs-en | -0.0311 | 9.7290e-01 | ❌ No | [-0.2224, 0.1602] |
| fs-es vs zs-es | -0.0194 | 9.9310e-01 | ❌ No | [-0.2107, 0.1719] |
| zs-en vs zs-es | 0.0117 | 9.9850e-01 | ❌ No | [-0.1796, 0.2030] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 5332.9 characters.
- **Outlier Records Identified:** 6 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.5817 | 0.6166 | +0.0349 | 📈 Improved |
| fs-es | 0.6987 | 0.7067 | +0.0079 | 📈 Improved |
| zs-en | 0.6676 | 0.6185 | -0.0491 | 📉 Decreased |
| zs-es | 0.6793 | 0.6616 | -0.0178 | 📉 Decreased |