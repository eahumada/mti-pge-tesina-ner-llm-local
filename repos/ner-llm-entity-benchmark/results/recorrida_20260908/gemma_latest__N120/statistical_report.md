# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.0002
- **p-Value:** 9.8947e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma:latest_baseline | 113 | 0.5955 | 0.5610 | 0.6299 | 0.1850 |
| gemma:latest_kb_rag | 113 | 0.5958 | 0.5602 | 0.6313 | 0.1907 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma:latest_baseline vs gemma:latest_kb_rag | 0.0003 | 9.8950e-01 | ❌ No | [-0.0489, 0.0496] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 7 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma:latest_baseline | 0.5955 | 0.5891 | -0.0063 | 📉 Decreased |
| gemma:latest_kb_rag | 0.5958 | 0.5896 | -0.0062 | 📉 Decreased |