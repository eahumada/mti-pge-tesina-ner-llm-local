# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.3721
- **p-Value:** 7.7325e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 30 | 0.8750 | 0.8311 | 0.9189 | 0.1176 |
| zs-es | 30 | 0.8444 | 0.7868 | 0.9021 | 0.1544 |
| fs-es | 30 | 0.8596 | 0.8039 | 0.9154 | 0.1494 |
| fs-en | 30 | 0.8783 | 0.8278 | 0.9288 | 0.1353 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | -0.0187 | 9.5470e-01 | ❌ No | [-0.1128, 0.0754] |
| fs-en vs zs-en | -0.0033 | 9.9970e-01 | ❌ No | [-0.0975, 0.0908] |
| fs-en vs zs-es | -0.0339 | 7.8410e-01 | ❌ No | [-0.1280, 0.0602] |
| fs-es vs zs-en | 0.0154 | 9.7400e-01 | ❌ No | [-0.0788, 0.1095] |
| fs-es vs zs-es | -0.0152 | 9.7480e-01 | ❌ No | [-0.1093, 0.0789] |
| zs-en vs zs-es | -0.0306 | 8.3200e-01 | ❌ No | [-0.1247, 0.0636] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 286.2 characters.
- **Outlier Records Identified:** 1 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.8783 | 0.8741 | -0.0042 | 📉 Decreased |
| fs-es | 0.8596 | 0.8548 | -0.0048 | 📉 Decreased |
| zs-en | 0.8750 | 0.8707 | -0.0043 | 📉 Decreased |
| zs-es | 0.8444 | 0.8391 | -0.0054 | 📉 Decreased |