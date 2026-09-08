# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.1583
- **p-Value:** 6.9378e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline | 15 | 0.6699 | 0.6116 | 0.7282 | 0.1053 |
| gemma4:31b-cloud_rag_enhanced | 15 | 0.6850 | 0.6284 | 0.7415 | 0.1021 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline vs gemma4:31b-cloud_rag_enhanced | 0.0151 | 6.9380e-01 | ❌ No | [-0.0625, 0.0926] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 5332.9 characters.
- **Outlier Records Identified:** 6 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline | 0.6699 | 0.6685 | -0.0014 | 📉 Decreased |
| gemma4:31b-cloud_rag_enhanced | 0.6850 | 0.6752 | -0.0097 | 📉 Decreased |