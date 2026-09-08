# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.1223
- **p-Value:** 7.2918e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| qwen2.5:14b_baseline | 15 | 0.6841 | 0.6135 | 0.7547 | 0.1274 |
| qwen2.5:14b_kb_rag | 15 | 0.7000 | 0.6331 | 0.7669 | 0.1208 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| qwen2.5:14b_baseline vs qwen2.5:14b_kb_rag | 0.0159 | 7.2920e-01 | ❌ No | [-0.0770, 0.1087] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 13483.0 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| qwen2.5:14b_baseline | 0.6841 | 0.6841 | +0.0000 | ⚖️ Stable |
| qwen2.5:14b_kb_rag | 0.7000 | 0.7000 | +0.0000 | ⚖️ Stable |