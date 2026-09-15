# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.3133
- **p-Value:** 8.1572e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 30 | 0.8753 | 0.8239 | 0.9266 | 0.1375 |
| zs-es | 30 | 0.8581 | 0.8054 | 0.9107 | 0.1411 |
| fs-es | 30 | 0.8848 | 0.8332 | 0.9363 | 0.1382 |
| fs-en | 30 | 0.8549 | 0.8032 | 0.9066 | 0.1384 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | 0.0298 | 8.3890e-01 | ❌ No | [-0.0636, 0.1233] |
| fs-en vs zs-en | 0.0204 | 9.4120e-01 | ❌ No | [-0.0731, 0.1138] |
| fs-en vs zs-es | 0.0031 | 9.9980e-01 | ❌ No | [-0.0903, 0.0966] |
| fs-es vs zs-en | -0.0095 | 9.9350e-01 | ❌ No | [-0.1029, 0.0840] |
| fs-es vs zs-es | -0.0267 | 8.7860e-01 | ❌ No | [-0.1201, 0.0667] |
| zs-en vs zs-es | -0.0172 | 9.6310e-01 | ❌ No | [-0.1107, 0.0762] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 362.6 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.8549 | 0.8549 | +0.0000 | ⚖️ Stable |
| fs-es | 0.8848 | 0.8848 | +0.0000 | ⚖️ Stable |
| zs-en | 0.8753 | 0.8753 | +0.0000 | ⚖️ Stable |
| zs-es | 0.8581 | 0.8581 | +0.0000 | ⚖️ Stable |