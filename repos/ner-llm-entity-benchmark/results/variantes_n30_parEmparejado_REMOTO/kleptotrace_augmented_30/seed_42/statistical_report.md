# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.3171
- **p-Value:** 8.1295e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 30 | 0.8730 | 0.8279 | 0.9180 | 0.1207 |
| zs-es | 30 | 0.8370 | 0.7807 | 0.8932 | 0.1506 |
| fs-es | 30 | 0.8510 | 0.7958 | 0.9063 | 0.1479 |
| fs-en | 30 | 0.8585 | 0.7980 | 0.9191 | 0.1621 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | -0.0075 | 9.9720e-01 | ❌ No | [-0.1059, 0.0908] |
| fs-en vs zs-en | 0.0144 | 9.8080e-01 | ❌ No | [-0.0839, 0.1128] |
| fs-en vs zs-es | -0.0216 | 9.4030e-01 | ❌ No | [-0.1199, 0.0768] |
| fs-es vs zs-en | 0.0220 | 9.3720e-01 | ❌ No | [-0.0764, 0.1203] |
| fs-es vs zs-es | -0.0141 | 9.8230e-01 | ❌ No | [-0.1124, 0.0843] |
| zs-en vs zs-es | -0.0360 | 7.7530e-01 | ❌ No | [-0.1344, 0.0623] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 286.2 characters.
- **Outlier Records Identified:** 1 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.8585 | 0.8537 | -0.0049 | 📉 Decreased |
| fs-es | 0.8510 | 0.8528 | +0.0018 | 📈 Improved |
| zs-en | 0.8730 | 0.8686 | -0.0044 | 📉 Decreased |
| zs-es | 0.8370 | 0.8382 | +0.0013 | 📈 Improved |