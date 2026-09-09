# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.0459
- **p-Value:** 8.3117e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline | 30 | 0.5729 | 0.4853 | 0.6604 | 0.2345 |
| deepseek-r1:1.5b_kb_rag | 30 | 0.5845 | 0.5165 | 0.6524 | 0.1819 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline vs deepseek-r1:1.5b_kb_rag | 0.0116 | 8.3120e-01 | ❌ No | [-0.0969, 0.1201] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 286.2 characters.
- **Outlier Records Identified:** 1 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline | 0.5729 | 0.5738 | +0.0009 | 📈 Improved |
| deepseek-r1:1.5b_kb_rag | 0.5845 | 0.5965 | +0.0120 | 📈 Improved |