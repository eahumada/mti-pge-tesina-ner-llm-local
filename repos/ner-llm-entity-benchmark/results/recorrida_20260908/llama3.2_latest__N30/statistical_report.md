# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.0714
- **p-Value:** 7.9023e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| llama3.2:latest_baseline | 30 | 0.8500 | 0.7925 | 0.9076 | 0.1542 |
| llama3.2:latest_kb_rag | 30 | 0.8390 | 0.7771 | 0.9009 | 0.1657 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| llama3.2:latest_baseline vs llama3.2:latest_kb_rag | -0.0110 | 7.9020e-01 | ❌ No | [-0.0938, 0.0717] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 286.2 characters.
- **Outlier Records Identified:** 1 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| llama3.2:latest_baseline | 0.8500 | 0.8449 | -0.0052 | 📉 Decreased |
| llama3.2:latest_kb_rag | 0.8390 | 0.8449 | +0.0059 | 📈 Improved |