# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.1451
- **p-Value:** 9.3281e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 120 | 0.5446 | 0.5072 | 0.5819 | 0.2066 |
| zs-es | 120 | 0.5562 | 0.5206 | 0.5918 | 0.1970 |
| fs-es | 120 | 0.5402 | 0.5049 | 0.5756 | 0.1958 |
| fs-en | 120 | 0.5450 | 0.5118 | 0.5783 | 0.1841 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | -0.0048 | 9.9760e-01 | ❌ No | [-0.0700, 0.0604] |
| fs-en vs zs-en | -0.0005 | 1.0000e+00 | ❌ No | [-0.0657, 0.0648] |
| fs-en vs zs-es | 0.0112 | 9.7120e-01 | ❌ No | [-0.0541, 0.0764] |
| fs-es vs zs-en | 0.0043 | 9.9820e-01 | ❌ No | [-0.0609, 0.0696] |
| fs-es vs zs-es | 0.0160 | 9.2190e-01 | ❌ No | [-0.0493, 0.0812] |
| zs-en vs zs-es | 0.0116 | 9.6770e-01 | ❌ No | [-0.0536, 0.0769] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 2610.3 characters.
- **Outlier Records Identified:** 14 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.5450 | 0.5325 | -0.0126 | 📉 Decreased |
| fs-es | 0.5402 | 0.5209 | -0.0193 | 📉 Decreased |
| zs-en | 0.5446 | 0.5370 | -0.0076 | 📉 Decreased |
| zs-es | 0.5562 | 0.5379 | -0.0183 | 📉 Decreased |