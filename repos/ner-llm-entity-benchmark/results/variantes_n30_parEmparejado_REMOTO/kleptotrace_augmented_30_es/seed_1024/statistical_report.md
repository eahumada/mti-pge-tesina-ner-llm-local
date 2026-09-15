# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.0391
- **p-Value:** 9.8964e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 30 | 0.8709 | 0.8229 | 0.9189 | 0.1286 |
| zs-es | 30 | 0.8789 | 0.8342 | 0.9237 | 0.1198 |
| fs-es | 30 | 0.8812 | 0.8354 | 0.9271 | 0.1228 |
| fs-en | 30 | 0.8761 | 0.8306 | 0.9216 | 0.1218 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | 0.0051 | 9.9850e-01 | ❌ No | [-0.0779, 0.0881] |
| fs-en vs zs-en | -0.0052 | 9.9840e-01 | ❌ No | [-0.0882, 0.0778] |
| fs-en vs zs-es | 0.0028 | 9.9980e-01 | ❌ No | [-0.0802, 0.0858] |
| fs-es vs zs-en | -0.0103 | 9.8810e-01 | ❌ No | [-0.0933, 0.0727] |
| fs-es vs zs-es | -0.0023 | 9.9990e-01 | ❌ No | [-0.0853, 0.0807] |
| zs-en vs zs-es | 0.0080 | 9.9440e-01 | ❌ No | [-0.0750, 0.0910] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 362.6 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.8761 | 0.8761 | +0.0000 | ⚖️ Stable |
| fs-es | 0.8812 | 0.8812 | +0.0000 | ⚖️ Stable |
| zs-en | 0.8709 | 0.8709 | +0.0000 | ⚖️ Stable |
| zs-es | 0.8789 | 0.8789 | +0.0000 | ⚖️ Stable |