# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 14.0200
- **p-Value:** 8.6222e-09

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:12b-mlx_baseline | 120 | 0.5618 | 0.5296 | 0.5940 | 0.1783 |
| gemma4:12b-mlx_kb_rag | 120 | 0.5929 | 0.5583 | 0.6275 | 0.1915 |
| qwen3:8b_baseline | 141 | 0.4383 | 0.3975 | 0.4792 | 0.2455 |
| qwen3:8b_kb_rag | 126 | 0.4542 | 0.4031 | 0.5052 | 0.2895 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:12b-mlx_baseline vs gemma4:12b-mlx_kb_rag | 0.0311 | 7.2670e-01 | ❌ No | [-0.0461, 0.1083] |
| gemma4:12b-mlx_baseline vs qwen3:8b_baseline | -0.1235 | 1.0000e-04 | ✅ Yes | [-0.1978, -0.0492] |
| gemma4:12b-mlx_baseline vs qwen3:8b_kb_rag | -0.1076 | 1.7000e-03 | ✅ Yes | [-0.1839, -0.0314] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_baseline | -0.1546 | 0.0000e+00 | ✅ Yes | [-0.2289, -0.0804] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.1387 | 0.0000e+00 | ✅ Yes | [-0.2150, -0.0625] |
| qwen3:8b_baseline vs qwen3:8b_kb_rag | 0.0159 | 9.4440e-01 | ❌ No | [-0.0574, 0.0892] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 2610.3 characters.
- **Outlier Records Identified:** 14 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:12b-mlx_baseline | 0.5618 | 0.5515 | -0.0103 | 📉 Decreased |
| gemma4:12b-mlx_kb_rag | 0.5929 | 0.5779 | -0.0150 | 📉 Decreased |
| qwen3:8b_baseline | 0.4383 | 0.4256 | -0.0128 | 📉 Decreased |
| qwen3:8b_kb_rag | 0.4542 | 0.4723 | +0.0181 | 📈 Improved |