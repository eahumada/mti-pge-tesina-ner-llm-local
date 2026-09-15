# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 2.4463
- **p-Value:** 7.3286e-02

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 15 | 0.6345 | 0.5057 | 0.7633 | 0.2326 |
| zs-es | 15 | 0.7207 | 0.6348 | 0.8065 | 0.1551 |
| fs-es | 15 | 0.7970 | 0.7315 | 0.8624 | 0.1181 |
| fs-en | 15 | 0.7417 | 0.6642 | 0.8191 | 0.1398 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | 0.0553 | 8.0140e-01 | ❌ No | [-0.1062, 0.2169] |
| fs-en vs zs-en | -0.1072 | 3.0500e-01 | ❌ No | [-0.2687, 0.0544] |
| fs-en vs zs-es | -0.0210 | 9.8580e-01 | ❌ No | [-0.1825, 0.1405] |
| fs-es vs zs-en | -0.1625 | 4.8200e-02 | ✅ Yes | [-0.3240, -0.0009] |
| fs-es vs zs-es | -0.0763 | 5.9760e-01 | ❌ No | [-0.2379, 0.0852] |
| zs-en vs zs-es | 0.0862 | 4.9710e-01 | ❌ No | [-0.0754, 0.2477] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 13483.0 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.7417 | 0.7417 | +0.0000 | ⚖️ Stable |
| fs-es | 0.7970 | 0.7970 | +0.0000 | ⚖️ Stable |
| zs-en | 0.6345 | 0.6345 | +0.0000 | ⚖️ Stable |
| zs-es | 0.7207 | 0.7207 | +0.0000 | ⚖️ Stable |