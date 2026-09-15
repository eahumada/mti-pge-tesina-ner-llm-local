# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.6352
- **p-Value:** 5.9262e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 120 | 0.7411 | 0.7139 | 0.7683 | 0.1505 |
| zs-es | 120 | 0.7558 | 0.7295 | 0.7821 | 0.1456 |
| fs-es | 120 | 0.7486 | 0.7236 | 0.7737 | 0.1386 |
| fs-en | 120 | 0.7654 | 0.7411 | 0.7897 | 0.1344 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | -0.0167 | 7.9950e-01 | ❌ No | [-0.0641, 0.0307] |
| fs-en vs zs-en | -0.0243 | 5.4930e-01 | ❌ No | [-0.0717, 0.0231] |
| fs-en vs zs-es | -0.0096 | 9.5420e-01 | ❌ No | [-0.0570, 0.0378] |
| fs-es vs zs-en | -0.0076 | 9.7640e-01 | ❌ No | [-0.0550, 0.0398] |
| fs-es vs zs-es | 0.0072 | 9.7990e-01 | ❌ No | [-0.0402, 0.0546] |
| zs-en vs zs-es | 0.0147 | 8.5360e-01 | ❌ No | [-0.0327, 0.0621] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 10 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.7654 | 0.7627 | -0.0027 | 📉 Decreased |
| fs-es | 0.7486 | 0.7441 | -0.0046 | 📉 Decreased |
| zs-en | 0.7411 | 0.7440 | +0.0029 | 📈 Improved |
| zs-es | 0.7558 | 0.7587 | +0.0029 | 📈 Improved |