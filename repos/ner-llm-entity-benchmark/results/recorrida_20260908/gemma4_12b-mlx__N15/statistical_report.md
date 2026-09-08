# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.7065
- **p-Value:** 4.0774e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:12b-mlx_baseline | 15 | 0.7362 | 0.6794 | 0.7930 | 0.1026 |
| gemma4:12b-mlx_kb_rag | 15 | 0.7684 | 0.7090 | 0.8278 | 0.1072 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:12b-mlx_baseline vs gemma4:12b-mlx_kb_rag | 0.0322 | 4.0770e-01 | ❌ No | [-0.0463, 0.1107] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 13483.0 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:12b-mlx_baseline | 0.7362 | 0.7362 | +0.0000 | ⚖️ Stable |
| gemma4:12b-mlx_kb_rag | 0.7684 | 0.7684 | +0.0000 | ⚖️ Stable |