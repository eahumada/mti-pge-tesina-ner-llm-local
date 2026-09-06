# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.0000
- **p-Value:** 1.0000e+00

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| llama3.2:latest | 120 | 0.3945 | 0.3534 | 0.4355 | 0.2269 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
No comparisons run (insufficient models or samples).

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 2610.3 characters.
- **Outlier Records Identified:** 14 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| llama3.2:latest | 0.3945 | 0.3718 | -0.0227 | 📉 Decreased |