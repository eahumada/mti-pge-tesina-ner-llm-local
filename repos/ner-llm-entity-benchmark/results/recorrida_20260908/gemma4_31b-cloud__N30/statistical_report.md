# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.3523
- **p-Value:** 5.5510e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline | 30 | 0.8804 | 0.8243 | 0.9365 | 0.1502 |
| gemma4:31b-cloud_kb_rag | 30 | 0.8573 | 0.8011 | 0.9136 | 0.1507 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline vs gemma4:31b-cloud_kb_rag | -0.0231 | 5.5510e-01 | ❌ No | [-0.1008, 0.0547] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 286.2 characters.
- **Outlier Records Identified:** 1 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline | 0.8804 | 0.8832 | +0.0028 | 📈 Improved |
| gemma4:31b-cloud_kb_rag | 0.8573 | 0.8593 | +0.0020 | 📈 Improved |