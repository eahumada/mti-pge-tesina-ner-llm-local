# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 1.4002
- **p-Value:** 2.5231e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 15 | 0.6705 | 0.5035 | 0.8376 | 0.3017 |
| zs-es | 15 | 0.7788 | 0.7252 | 0.8324 | 0.0968 |
| fs-es | 15 | 0.8014 | 0.7521 | 0.8507 | 0.0890 |
| fs-en | 15 | 0.7048 | 0.5767 | 0.8330 | 0.2314 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | 0.0965 | 5.5780e-01 | ❌ No | [-0.0979, 0.2910] |
| fs-en vs zs-en | -0.0343 | 9.6600e-01 | ❌ No | [-0.2288, 0.1602] |
| fs-en vs zs-es | 0.0740 | 7.4570e-01 | ❌ No | [-0.1205, 0.2685] |
| fs-es vs zs-en | -0.1308 | 2.9300e-01 | ❌ No | [-0.3253, 0.0637] |
| fs-es vs zs-es | -0.0225 | 9.8990e-01 | ❌ No | [-0.2170, 0.1719] |
| zs-en vs zs-es | 0.1083 | 4.5960e-01 | ❌ No | [-0.0862, 0.3028] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 13483.0 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.7048 | 0.7048 | +0.0000 | ⚖️ Stable |
| fs-es | 0.8014 | 0.8014 | +0.0000 | ⚖️ Stable |
| zs-en | 0.6705 | 0.6705 | +0.0000 | ⚖️ Stable |
| zs-es | 0.7788 | 0.7788 | +0.0000 | ⚖️ Stable |