# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.1829
- **p-Value:** 9.0800e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 120 | 0.7581 | 0.7321 | 0.7841 | 0.1438 |
| zs-es | 120 | 0.7496 | 0.7236 | 0.7756 | 0.1439 |
| fs-es | 120 | 0.7538 | 0.7296 | 0.7780 | 0.1336 |
| fs-en | 120 | 0.7623 | 0.7370 | 0.7876 | 0.1400 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | -0.0085 | 9.6600e-01 | ❌ No | [-0.0552, 0.0383] |
| fs-en vs zs-en | -0.0042 | 9.9570e-01 | ❌ No | [-0.0509, 0.0426] |
| fs-en vs zs-es | -0.0127 | 8.9650e-01 | ❌ No | [-0.0594, 0.0340] |
| fs-es vs zs-en | 0.0043 | 9.9520e-01 | ❌ No | [-0.0424, 0.0511] |
| fs-es vs zs-es | -0.0042 | 9.9550e-01 | ❌ No | [-0.0510, 0.0425] |
| zs-en vs zs-es | -0.0086 | 9.6520e-01 | ❌ No | [-0.0553, 0.0382] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 10 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.7623 | 0.7616 | -0.0007 | 📉 Decreased |
| fs-es | 0.7538 | 0.7485 | -0.0053 | 📉 Decreased |
| zs-en | 0.7581 | 0.7583 | +0.0002 | 📈 Improved |
| zs-es | 0.7496 | 0.7529 | +0.0034 | 📈 Improved |