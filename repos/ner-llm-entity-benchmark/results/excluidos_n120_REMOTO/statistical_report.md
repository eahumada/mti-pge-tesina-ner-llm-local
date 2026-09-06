# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 1.8810
- **p-Value:** 1.7152e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 120 | 0.5627 | 0.5278 | 0.5976 | 0.1932 |
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 120 | 0.5964 | 0.5624 | 0.6305 | 0.1881 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0338 | 1.7150e-01 | ❌ No | [-0.0147, 0.0823] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 2610.3 characters.
- **Outlier Records Identified:** 14 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.5627 | 0.5541 | -0.0085 | 📉 Decreased |
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.5964 | 0.5857 | -0.0108 | 📉 Decreased |