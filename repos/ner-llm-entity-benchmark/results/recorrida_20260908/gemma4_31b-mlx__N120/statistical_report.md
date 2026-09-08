# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.2905
- **p-Value:** 5.9046e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:31b-mlx_baseline | 113 | 0.8147 | 0.7889 | 0.8406 | 0.1387 |
| gemma4:31b-mlx_kb_rag | 113 | 0.8244 | 0.7997 | 0.8491 | 0.1324 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b-mlx_baseline vs gemma4:31b-mlx_kb_rag | 0.0097 | 5.9050e-01 | ❌ No | [-0.0258, 0.0453] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 7 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b-mlx_baseline | 0.8147 | 0.8172 | +0.0025 | 📈 Improved |
| gemma4:31b-mlx_kb_rag | 0.8244 | 0.8263 | +0.0019 | 📈 Improved |