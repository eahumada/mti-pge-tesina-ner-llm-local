# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.1120
- **p-Value:** 7.3819e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| qwen2.5:14b_baseline | 113 | 0.6961 | 0.6681 | 0.7242 | 0.1503 |
| qwen2.5:14b_kb_rag | 113 | 0.7031 | 0.6732 | 0.7329 | 0.1601 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| qwen2.5:14b_baseline vs qwen2.5:14b_kb_rag | 0.0069 | 7.3820e-01 | ❌ No | [-0.0338, 0.0476] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 7 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| qwen2.5:14b_baseline | 0.6961 | 0.6973 | +0.0012 | 📈 Improved |
| qwen2.5:14b_kb_rag | 0.7031 | 0.7027 | -0.0003 | 📉 Decreased |