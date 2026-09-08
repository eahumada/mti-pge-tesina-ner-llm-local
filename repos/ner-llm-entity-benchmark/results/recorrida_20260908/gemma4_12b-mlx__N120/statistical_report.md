# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 1.5394
- **p-Value:** 2.1600e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:12b-mlx_baseline | 113 | 0.7767 | 0.7503 | 0.8031 | 0.1418 |
| gemma4:12b-mlx_kb_rag | 113 | 0.7996 | 0.7743 | 0.8249 | 0.1358 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:12b-mlx_baseline vs gemma4:12b-mlx_kb_rag | 0.0229 | 2.1600e-01 | ❌ No | [-0.0135, 0.0593] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 7 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:12b-mlx_baseline | 0.7767 | 0.7791 | +0.0024 | 📈 Improved |
| gemma4:12b-mlx_kb_rag | 0.7996 | 0.8017 | +0.0020 | 📈 Improved |