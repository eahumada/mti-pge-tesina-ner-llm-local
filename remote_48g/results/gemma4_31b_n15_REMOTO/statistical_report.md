# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.7395
- **p-Value:** 3.9713e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:31b_baseline | 15 | 0.6912 | 0.6296 | 0.7529 | 0.1114 |
| gemma4:31b_rag_enhanced | 15 | 0.6391 | 0.5248 | 0.7535 | 0.2065 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b_baseline vs gemma4:31b_rag_enhanced | -0.0521 | 3.9710e-01 | ❌ No | [-0.1762, 0.0720] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 5332.9 characters.
- **Outlier Records Identified:** 6 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b_baseline | 0.6912 | 0.6771 | -0.0141 | 📉 Decreased |
| gemma4:31b_rag_enhanced | 0.6391 | 0.5888 | -0.0503 | 📉 Decreased |