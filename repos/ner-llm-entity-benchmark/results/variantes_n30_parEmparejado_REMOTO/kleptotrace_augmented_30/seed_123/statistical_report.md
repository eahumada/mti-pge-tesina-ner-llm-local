# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.4064
- **p-Value:** 7.4867e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 30 | 0.8730 | 0.8279 | 0.9180 | 0.1207 |
| zs-es | 30 | 0.8430 | 0.7879 | 0.8981 | 0.1475 |
| fs-es | 30 | 0.8573 | 0.8018 | 0.9128 | 0.1486 |
| fs-en | 30 | 0.8805 | 0.8226 | 0.9385 | 0.1552 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | -0.0232 | 9.2320e-01 | ❌ No | [-0.1199, 0.0734] |
| fs-en vs zs-en | -0.0075 | 9.9700e-01 | ❌ No | [-0.1042, 0.0891] |
| fs-en vs zs-es | -0.0375 | 7.4300e-01 | ❌ No | [-0.1341, 0.0591] |
| fs-es vs zs-en | 0.0157 | 9.7430e-01 | ❌ No | [-0.0809, 0.1124] |
| fs-es vs zs-es | -0.0143 | 9.8060e-01 | ❌ No | [-0.1109, 0.0824] |
| zs-en vs zs-es | -0.0300 | 8.5040e-01 | ❌ No | [-0.1266, 0.0667] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 286.2 characters.
- **Outlier Records Identified:** 1 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.8805 | 0.8764 | -0.0041 | 📉 Decreased |
| fs-es | 0.8573 | 0.8592 | +0.0020 | 📈 Improved |
| zs-en | 0.8730 | 0.8686 | -0.0044 | 📉 Decreased |
| zs-es | 0.8430 | 0.8445 | +0.0015 | 📈 Improved |