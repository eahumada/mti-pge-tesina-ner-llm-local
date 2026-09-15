# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.1047
- **p-Value:** 9.5717e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 30 | 0.8661 | 0.8190 | 0.9133 | 0.1263 |
| zs-es | 30 | 0.8795 | 0.8326 | 0.9265 | 0.1256 |
| fs-es | 30 | 0.8730 | 0.8233 | 0.9227 | 0.1331 |
| fs-en | 30 | 0.8618 | 0.8091 | 0.9146 | 0.1412 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | 0.0112 | 9.8770e-01 | ❌ No | [-0.0775, 0.0998] |
| fs-en vs zs-en | 0.0043 | 9.9930e-01 | ❌ No | [-0.0843, 0.0930] |
| fs-en vs zs-es | 0.0177 | 9.5390e-01 | ❌ No | [-0.0709, 0.1064] |
| fs-es vs zs-en | -0.0068 | 9.9710e-01 | ❌ No | [-0.0955, 0.0818] |
| fs-es vs zs-es | 0.0066 | 9.9740e-01 | ❌ No | [-0.0821, 0.0952] |
| zs-en vs zs-es | 0.0134 | 9.7920e-01 | ❌ No | [-0.0753, 0.1021] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 362.6 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.8618 | 0.8618 | +0.0000 | ⚖️ Stable |
| fs-es | 0.8730 | 0.8730 | +0.0000 | ⚖️ Stable |
| zs-en | 0.8661 | 0.8661 | +0.0000 | ⚖️ Stable |
| zs-es | 0.8795 | 0.8795 | +0.0000 | ⚖️ Stable |