# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.2267
- **p-Value:** 8.7785e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 120 | 0.7439 | 0.7164 | 0.7715 | 0.1524 |
| zs-es | 120 | 0.7551 | 0.7290 | 0.7812 | 0.1445 |
| fs-es | 120 | 0.7564 | 0.7315 | 0.7813 | 0.1377 |
| fs-en | 120 | 0.7575 | 0.7320 | 0.7829 | 0.1408 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | -0.0011 | 9.9990e-01 | ❌ No | [-0.0490, 0.0468] |
| fs-en vs zs-en | -0.0135 | 8.8630e-01 | ❌ No | [-0.0614, 0.0344] |
| fs-en vs zs-es | -0.0023 | 9.9930e-01 | ❌ No | [-0.0503, 0.0456] |
| fs-es vs zs-en | -0.0124 | 9.0910e-01 | ❌ No | [-0.0603, 0.0355] |
| fs-es vs zs-es | -0.0012 | 9.9990e-01 | ❌ No | [-0.0492, 0.0467] |
| zs-en vs zs-es | 0.0112 | 9.3170e-01 | ❌ No | [-0.0367, 0.0591] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 10 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.7575 | 0.7545 | -0.0030 | 📉 Decreased |
| fs-es | 0.7564 | 0.7524 | -0.0040 | 📉 Decreased |
| zs-en | 0.7439 | 0.7455 | +0.0015 | 📈 Improved |
| zs-es | 0.7551 | 0.7586 | +0.0035 | 📈 Improved |