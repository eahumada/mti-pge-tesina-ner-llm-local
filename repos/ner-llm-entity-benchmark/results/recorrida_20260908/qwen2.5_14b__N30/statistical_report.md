# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.3495
- **p-Value:** 5.5668e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| qwen2.5:14b_baseline | 30 | 0.8446 | 0.7872 | 0.9019 | 0.1536 |
| qwen2.5:14b_kb_rag | 30 | 0.8662 | 0.8181 | 0.9144 | 0.1289 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| qwen2.5:14b_baseline vs qwen2.5:14b_kb_rag | 0.0216 | 5.5670e-01 | ❌ No | [-0.0516, 0.0949] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 286.2 characters.
- **Outlier Records Identified:** 1 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| qwen2.5:14b_baseline | 0.8446 | 0.8461 | +0.0015 | 📈 Improved |
| qwen2.5:14b_kb_rag | 0.8662 | 0.8685 | +0.0023 | 📈 Improved |