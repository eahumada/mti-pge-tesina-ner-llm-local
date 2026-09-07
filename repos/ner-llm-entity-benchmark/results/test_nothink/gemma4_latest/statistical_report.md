# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.1326
- **p-Value:** 9.4029e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 15 | 0.6750 | 0.5934 | 0.7566 | 0.1473 |
| zs-es | 15 | 0.7045 | 0.6249 | 0.7841 | 0.1437 |
| fs-es | 15 | 0.6937 | 0.6198 | 0.7675 | 0.1334 |
| fs-en | 15 | 0.6993 | 0.6316 | 0.7670 | 0.1223 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | -0.0056 | 9.9950e-01 | ❌ No | [-0.1381, 0.1268] |
| fs-en vs zs-en | -0.0243 | 9.6180e-01 | ❌ No | [-0.1568, 0.1081] |
| fs-en vs zs-es | 0.0052 | 9.9960e-01 | ❌ No | [-0.1273, 0.1377] |
| fs-es vs zs-en | -0.0187 | 9.8200e-01 | ❌ No | [-0.1512, 0.1138] |
| fs-es vs zs-es | 0.0108 | 9.9640e-01 | ❌ No | [-0.1216, 0.1433] |
| zs-en vs zs-es | 0.0295 | 9.3460e-01 | ❌ No | [-0.1029, 0.1620] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 5332.9 characters.
- **Outlier Records Identified:** 6 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.6993 | 0.7176 | +0.0183 | 📈 Improved |
| fs-es | 0.6937 | 0.7084 | +0.0148 | 📈 Improved |
| zs-en | 0.6750 | 0.6796 | +0.0047 | 📈 Improved |
| zs-es | 0.7045 | 0.7024 | -0.0021 | 📉 Decreased |