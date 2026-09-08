# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 1.1379
- **p-Value:** 3.4172e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 15 | 0.6405 | 0.5103 | 0.7706 | 0.2350 |
| zs-es | 15 | 0.6843 | 0.6019 | 0.7667 | 0.1488 |
| fs-es | 15 | 0.7444 | 0.6704 | 0.8185 | 0.1337 |
| fs-en | 15 | 0.6332 | 0.5188 | 0.7477 | 0.2067 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | 0.1112 | 3.6470e-01 | ❌ No | [-0.0683, 0.2908] |
| fs-en vs zs-en | 0.0072 | 9.9960e-01 | ❌ No | [-0.1723, 0.1868] |
| fs-en vs zs-es | 0.0511 | 8.7500e-01 | ❌ No | [-0.1285, 0.2306] |
| fs-es vs zs-en | -0.1040 | 4.2460e-01 | ❌ No | [-0.2835, 0.0755] |
| fs-es vs zs-es | -0.0602 | 8.1140e-01 | ❌ No | [-0.2397, 0.1194] |
| zs-en vs zs-es | 0.0438 | 9.1640e-01 | ❌ No | [-0.1357, 0.2234] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 5332.9 characters.
- **Outlier Records Identified:** 6 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.6332 | 0.6896 | +0.0564 | 📈 Improved |
| fs-es | 0.7444 | 0.7361 | -0.0084 | 📉 Decreased |
| zs-en | 0.6405 | 0.6667 | +0.0262 | 📈 Improved |
| zs-es | 0.6843 | 0.6974 | +0.0131 | 📈 Improved |