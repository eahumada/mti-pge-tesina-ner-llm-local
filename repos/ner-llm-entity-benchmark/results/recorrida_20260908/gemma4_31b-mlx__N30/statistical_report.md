# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.0005
- **p-Value:** 9.8239e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:31b-mlx_baseline | 30 | 0.8560 | 0.7996 | 0.9123 | 0.1509 |
| gemma4:31b-mlx_kb_rag | 30 | 0.8551 | 0.7996 | 0.9106 | 0.1486 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b-mlx_baseline vs gemma4:31b-mlx_kb_rag | -0.0009 | 9.8240e-01 | ❌ No | [-0.0783, 0.0766] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 286.2 characters.
- **Outlier Records Identified:** 1 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b-mlx_baseline | 0.8560 | 0.8579 | +0.0019 | 📈 Improved |
| gemma4:31b-mlx_kb_rag | 0.8551 | 0.8570 | +0.0019 | 📈 Improved |