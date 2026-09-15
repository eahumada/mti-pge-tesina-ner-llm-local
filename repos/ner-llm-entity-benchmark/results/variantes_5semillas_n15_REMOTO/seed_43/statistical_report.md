# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 1.7135
- **p-Value:** 1.7465e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 15 | 0.6863 | 0.5711 | 0.8015 | 0.2081 |
| zs-es | 15 | 0.8083 | 0.7519 | 0.8647 | 0.1018 |
| fs-es | 15 | 0.7932 | 0.7258 | 0.8606 | 0.1217 |
| fs-en | 15 | 0.7097 | 0.5750 | 0.8445 | 0.2434 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | 0.0834 | 5.7990e-01 | ❌ No | [-0.0893, 0.2562] |
| fs-en vs zs-en | -0.0235 | 9.8390e-01 | ❌ No | [-0.1962, 0.1493] |
| fs-en vs zs-es | 0.0985 | 4.3820e-01 | ❌ No | [-0.0742, 0.2713] |
| fs-es vs zs-en | -0.1069 | 3.6580e-01 | ❌ No | [-0.2796, 0.0658] |
| fs-es vs zs-es | 0.0151 | 9.9560e-01 | ❌ No | [-0.1577, 0.1878] |
| zs-en vs zs-es | 0.1220 | 2.5260e-01 | ❌ No | [-0.0508, 0.2947] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 13483.0 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.7097 | 0.7097 | +0.0000 | ⚖️ Stable |
| fs-es | 0.7932 | 0.7932 | +0.0000 | ⚖️ Stable |
| zs-en | 0.6863 | 0.6863 | +0.0000 | ⚖️ Stable |
| zs-es | 0.8083 | 0.8083 | +0.0000 | ⚖️ Stable |