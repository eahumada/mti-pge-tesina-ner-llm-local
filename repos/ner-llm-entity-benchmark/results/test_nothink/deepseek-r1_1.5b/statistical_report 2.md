# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.4452
- **p-Value:** 5.1006e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline | 15 | 0.2942 | 0.2163 | 0.3720 | 0.1406 |
| deepseek-r1:1.5b_kb_rag | 15 | 0.3445 | 0.2027 | 0.4863 | 0.2561 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline vs deepseek-r1:1.5b_kb_rag | 0.0503 | 5.1010e-01 | ❌ No | [-0.1042, 0.2049] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 2305.3 characters.
- **Outlier Records Identified:** 2 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline | 0.2942 | 0.2918 | -0.0024 | 📉 Decreased |
| deepseek-r1:1.5b_kb_rag | 0.3445 | 0.3182 | -0.0264 | 📉 Decreased |