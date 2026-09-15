# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 1.2631
- **p-Value:** 2.9585e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 15 | 0.7002 | 0.5695 | 0.8308 | 0.2360 |
| zs-es | 15 | 0.7660 | 0.6965 | 0.8355 | 0.1255 |
| fs-es | 15 | 0.8091 | 0.7576 | 0.8606 | 0.0930 |
| fs-en | 15 | 0.6990 | 0.5665 | 0.8315 | 0.2392 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | 0.1101 | 3.7160e-01 | ❌ No | [-0.0690, 0.2893] |
| fs-en vs zs-en | 0.0012 | 1.0000e+00 | ❌ No | [-0.1780, 0.1803] |
| fs-en vs zs-es | 0.0670 | 7.5560e-01 | ❌ No | [-0.1121, 0.2461] |
| fs-es vs zs-en | -0.1090 | 3.8100e-01 | ❌ No | [-0.2881, 0.0702] |
| fs-es vs zs-es | -0.0431 | 9.1940e-01 | ❌ No | [-0.2223, 0.1360] |
| zs-en vs zs-es | 0.0658 | 7.6520e-01 | ❌ No | [-0.1133, 0.2450] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 13483.0 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.6990 | 0.6990 | +0.0000 | ⚖️ Stable |
| fs-es | 0.8091 | 0.8091 | +0.0000 | ⚖️ Stable |
| zs-en | 0.7002 | 0.7002 | +0.0000 | ⚖️ Stable |
| zs-es | 0.7660 | 0.7660 | +0.0000 | ⚖️ Stable |