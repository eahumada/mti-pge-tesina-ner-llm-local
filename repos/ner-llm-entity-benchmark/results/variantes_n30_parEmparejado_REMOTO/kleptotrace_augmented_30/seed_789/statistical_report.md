# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.3010
- **p-Value:** 8.2465e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 30 | 0.8714 | 0.8267 | 0.9161 | 0.1197 |
| zs-es | 30 | 0.8482 | 0.7908 | 0.9055 | 0.1535 |
| fs-es | 30 | 0.8699 | 0.8190 | 0.9208 | 0.1362 |
| fs-en | 30 | 0.8819 | 0.8245 | 0.9394 | 0.1538 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | -0.0120 | 9.8770e-01 | ❌ No | [-0.1073, 0.0832] |
| fs-en vs zs-en | -0.0105 | 9.9170e-01 | ❌ No | [-0.1057, 0.0848] |
| fs-en vs zs-es | -0.0338 | 7.9210e-01 | ❌ No | [-0.1290, 0.0615] |
| fs-es vs zs-en | 0.0015 | 1.0000e+00 | ❌ No | [-0.0937, 0.0968] |
| fs-es vs zs-es | -0.0217 | 9.3340e-01 | ❌ No | [-0.1170, 0.0735] |
| zs-en vs zs-es | -0.0233 | 9.1980e-01 | ❌ No | [-0.1185, 0.0720] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 286.2 characters.
- **Outlier Records Identified:** 1 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.8819 | 0.8778 | -0.0041 | 📉 Decreased |
| fs-es | 0.8699 | 0.8723 | +0.0024 | 📈 Improved |
| zs-en | 0.8714 | 0.8670 | -0.0044 | 📉 Decreased |
| zs-es | 0.8482 | 0.8429 | -0.0052 | 📉 Decreased |