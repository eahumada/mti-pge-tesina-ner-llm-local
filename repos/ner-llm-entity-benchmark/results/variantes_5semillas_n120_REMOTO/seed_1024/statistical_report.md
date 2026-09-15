# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.6092
- **p-Value:** 6.0929e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 120 | 0.7429 | 0.7168 | 0.7691 | 0.1446 |
| zs-es | 120 | 0.7540 | 0.7269 | 0.7811 | 0.1500 |
| fs-es | 120 | 0.7573 | 0.7325 | 0.7821 | 0.1373 |
| fs-en | 120 | 0.7675 | 0.7429 | 0.7921 | 0.1360 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | -0.0102 | 9.4470e-01 | ❌ No | [-0.0575, 0.0371] |
| fs-en vs zs-en | -0.0246 | 5.3830e-01 | ❌ No | [-0.0719, 0.0227] |
| fs-en vs zs-es | -0.0135 | 8.8180e-01 | ❌ No | [-0.0608, 0.0338] |
| fs-es vs zs-en | -0.0144 | 8.6240e-01 | ❌ No | [-0.0616, 0.0329] |
| fs-es vs zs-es | -0.0033 | 9.9790e-01 | ❌ No | [-0.0506, 0.0440] |
| zs-en vs zs-es | 0.0110 | 9.3150e-01 | ❌ No | [-0.0363, 0.0583] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 10 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.7675 | 0.7645 | -0.0030 | 📉 Decreased |
| fs-es | 0.7573 | 0.7525 | -0.0048 | 📉 Decreased |
| zs-en | 0.7429 | 0.7464 | +0.0035 | 📈 Improved |
| zs-es | 0.7540 | 0.7537 | -0.0003 | 📉 Decreased |