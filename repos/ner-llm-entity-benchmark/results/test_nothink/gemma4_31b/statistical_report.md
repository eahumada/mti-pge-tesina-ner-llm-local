# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.1337
- **p-Value:** 7.1742e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:31b_baseline | 15 | 0.6624 | 0.6024 | 0.7225 | 0.1085 |
| gemma4:31b_rag_enhanced | 15 | 0.6758 | 0.6253 | 0.7263 | 0.0911 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b_baseline vs gemma4:31b_rag_enhanced | 0.0134 | 7.1740e-01 | ❌ No | [-0.0616, 0.0883] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 5332.9 characters.
- **Outlier Records Identified:** 6 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b_baseline | 0.6624 | 0.6603 | -0.0022 | 📉 Decreased |
| gemma4:31b_rag_enhanced | 0.6758 | 0.6595 | -0.0163 | 📉 Decreased |