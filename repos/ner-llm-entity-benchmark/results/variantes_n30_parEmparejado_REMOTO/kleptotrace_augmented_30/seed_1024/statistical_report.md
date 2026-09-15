# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.7408
- **p-Value:** 5.2984e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 30 | 0.8750 | 0.8311 | 0.9189 | 0.1176 |
| zs-es | 30 | 0.8302 | 0.7784 | 0.8820 | 0.1386 |
| fs-es | 30 | 0.8636 | 0.8134 | 0.9138 | 0.1344 |
| fs-en | 30 | 0.8770 | 0.8182 | 0.9358 | 0.1575 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | -0.0134 | 9.8180e-01 | ❌ No | [-0.1061, 0.0793] |
| fs-en vs zs-en | -0.0020 | 9.9990e-01 | ❌ No | [-0.0947, 0.0907] |
| fs-en vs zs-es | -0.0468 | 5.5530e-01 | ❌ No | [-0.1395, 0.0459] |
| fs-es vs zs-en | 0.0114 | 9.8860e-01 | ❌ No | [-0.0813, 0.1041] |
| fs-es vs zs-es | -0.0334 | 7.8370e-01 | ❌ No | [-0.1261, 0.0593] |
| zs-en vs zs-es | -0.0448 | 5.9050e-01 | ❌ No | [-0.1375, 0.0479] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 286.2 characters.
- **Outlier Records Identified:** 1 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.8770 | 0.8727 | -0.0042 | 📉 Decreased |
| fs-es | 0.8636 | 0.8658 | +0.0022 | 📈 Improved |
| zs-en | 0.8750 | 0.8707 | -0.0043 | 📉 Decreased |
| zs-es | 0.8302 | 0.8313 | +0.0010 | 📈 Improved |