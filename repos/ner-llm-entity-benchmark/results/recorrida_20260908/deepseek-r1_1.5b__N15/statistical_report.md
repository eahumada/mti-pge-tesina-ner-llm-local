# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.2777
- **p-Value:** 6.0236e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline | 15 | 0.3223 | 0.2134 | 0.4311 | 0.1966 |
| deepseek-r1:1.5b_kb_rag | 15 | 0.3586 | 0.2585 | 0.4586 | 0.1807 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline vs deepseek-r1:1.5b_kb_rag | 0.0363 | 6.0240e-01 | ❌ No | [-0.1049, 0.1775] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 13483.0 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline | 0.3223 | 0.3223 | +0.0000 | ⚖️ Stable |
| deepseek-r1:1.5b_kb_rag | 0.3586 | 0.3586 | +0.0000 | ⚖️ Stable |