# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.2235
- **p-Value:** 6.3816e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:31b | 30 | 0.7855 | 0.7259 | 0.8452 | 0.1597 |
| gemma4:31b-mlx | 30 | 0.8057 | 0.7422 | 0.8692 | 0.1701 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b vs gemma4:31b-mlx | 0.0201 | 6.3820e-01 | ❌ No | [-0.0651, 0.1054] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 702.0 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b | 0.7855 | 0.7855 | +0.0000 | ⚖️ Stable |
| gemma4:31b-mlx | 0.8057 | 0.8057 | +0.0000 | ⚖️ Stable |