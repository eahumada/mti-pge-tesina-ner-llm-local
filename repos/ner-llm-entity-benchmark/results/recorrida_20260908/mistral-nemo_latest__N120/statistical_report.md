# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 3.0291
- **p-Value:** 8.3158e-02

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| mistral-nemo:latest_baseline | 113 | 0.6063 | 0.5720 | 0.6406 | 0.1840 |
| mistral-nemo:latest_kb_rag | 113 | 0.5635 | 0.5288 | 0.5982 | 0.1862 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| mistral-nemo:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0429 | 8.3200e-02 | ❌ No | [-0.0914, 0.0057] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 7 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| mistral-nemo:latest_baseline | 0.6063 | 0.6067 | +0.0004 | 📈 Improved |
| mistral-nemo:latest_kb_rag | 0.5635 | 0.5595 | -0.0040 | 📉 Decreased |