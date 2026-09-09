# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.8669
- **p-Value:** 3.5283e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline | 113 | 0.2873 | 0.2578 | 0.3168 | 0.1583 |
| deepseek-r1:1.5b_kb_rag | 113 | 0.3080 | 0.2753 | 0.3407 | 0.1754 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline vs deepseek-r1:1.5b_kb_rag | 0.0207 | 3.5280e-01 | ❌ No | [-0.0231, 0.0645] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 7 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline | 0.2873 | 0.2865 | -0.0008 | 📉 Decreased |
| deepseek-r1:1.5b_kb_rag | 0.3080 | 0.3094 | +0.0014 | 📈 Improved |