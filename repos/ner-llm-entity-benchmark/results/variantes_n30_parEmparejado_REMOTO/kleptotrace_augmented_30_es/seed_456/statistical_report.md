# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.1738
- **p-Value:** 9.1394e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 30 | 0.8802 | 0.8294 | 0.9309 | 0.1359 |
| zs-es | 30 | 0.8796 | 0.8326 | 0.9265 | 0.1258 |
| fs-es | 30 | 0.8637 | 0.8147 | 0.9128 | 0.1313 |
| fs-en | 30 | 0.8615 | 0.8121 | 0.9108 | 0.1322 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | 0.0022 | 9.9990e-01 | ❌ No | [-0.0862, 0.0906] |
| fs-en vs zs-en | 0.0187 | 9.4630e-01 | ❌ No | [-0.0697, 0.1071] |
| fs-en vs zs-es | 0.0181 | 9.5090e-01 | ❌ No | [-0.0703, 0.1065] |
| fs-es vs zs-en | 0.0164 | 9.6250e-01 | ❌ No | [-0.0720, 0.1048] |
| fs-es vs zs-es | 0.0158 | 9.6620e-01 | ❌ No | [-0.0726, 0.1042] |
| zs-en vs zs-es | -0.0006 | 1.0000e+00 | ❌ No | [-0.0890, 0.0878] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 362.6 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.8615 | 0.8615 | +0.0000 | ⚖️ Stable |
| fs-es | 0.8637 | 0.8637 | +0.0000 | ⚖️ Stable |
| zs-en | 0.8802 | 0.8802 | +0.0000 | ⚖️ Stable |
| zs-es | 0.8796 | 0.8796 | +0.0000 | ⚖️ Stable |