# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.3424
- **p-Value:** 7.9468e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 30 | 0.8667 | 0.8218 | 0.9116 | 0.1202 |
| zs-es | 30 | 0.8865 | 0.8456 | 0.9274 | 0.1095 |
| fs-es | 30 | 0.8771 | 0.8262 | 0.9281 | 0.1365 |
| fs-en | 30 | 0.8552 | 0.8041 | 0.9063 | 0.1369 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | 0.0219 | 9.0710e-01 | ❌ No | [-0.0631, 0.1070] |
| fs-en vs zs-en | 0.0115 | 9.8470e-01 | ❌ No | [-0.0735, 0.0965] |
| fs-en vs zs-es | 0.0313 | 7.7190e-01 | ❌ No | [-0.0537, 0.1163] |
| fs-es vs zs-en | -0.0104 | 9.8870e-01 | ❌ No | [-0.0954, 0.0746] |
| fs-es vs zs-es | 0.0094 | 9.9170e-01 | ❌ No | [-0.0756, 0.0944] |
| zs-en vs zs-es | 0.0198 | 9.2970e-01 | ❌ No | [-0.0652, 0.1048] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 362.6 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.8552 | 0.8552 | +0.0000 | ⚖️ Stable |
| fs-es | 0.8771 | 0.8771 | +0.0000 | ⚖️ Stable |
| zs-en | 0.8667 | 0.8667 | +0.0000 | ⚖️ Stable |
| zs-es | 0.8865 | 0.8865 | +0.0000 | ⚖️ Stable |