# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 2.8389
- **p-Value:** 9.3320e-02

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| qwen3:8b_baseline | 120 | 0.4904 | 0.4577 | 0.5231 | 0.1808 |
| qwen3:8b_kb_rag | 120 | 0.5313 | 0.4961 | 0.5664 | 0.1943 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| qwen3:8b_baseline vs qwen3:8b_kb_rag | 0.0408 | 9.3300e-02 | ❌ No | [-0.0069, 0.0886] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 2610.3 characters.
- **Outlier Records Identified:** 14 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| qwen3:8b_baseline | 0.4904 | 0.4764 | -0.0141 | 📉 Decreased |
| qwen3:8b_kb_rag | 0.5313 | 0.5195 | -0.0118 | 📉 Decreased |