# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.0152
- **p-Value:** 9.0212e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline | 120 | 0.6238 | 0.5895 | 0.6582 | 0.1902 |
| gemma4:31b-cloud_kb_rag | 120 | 0.6268 | 0.5938 | 0.6598 | 0.1825 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline vs gemma4:31b-cloud_kb_rag | 0.0030 | 9.0210e-01 | ❌ No | [-0.0444, 0.0504] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 2610.3 characters.
- **Outlier Records Identified:** 14 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline | 0.6238 | 0.6165 | -0.0073 | 📉 Decreased |
| gemma4:31b-cloud_kb_rag | 0.6268 | 0.6160 | -0.0109 | 📉 Decreased |