# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 8.7714
- **p-Value:** 3.3896e-03

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| llama3.2:latest_baseline | 113 | 0.6325 | 0.5991 | 0.6660 | 0.1796 |
| llama3.2:latest_kb_rag | 113 | 0.6998 | 0.6697 | 0.7299 | 0.1615 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| llama3.2:latest_baseline vs llama3.2:latest_kb_rag | 0.0673 | 3.4000e-03 | ✅ Yes | [0.0225, 0.1121] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 7 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| llama3.2:latest_baseline | 0.6325 | 0.6297 | -0.0028 | 📉 Decreased |
| llama3.2:latest_kb_rag | 0.6998 | 0.6993 | -0.0006 | 📉 Decreased |