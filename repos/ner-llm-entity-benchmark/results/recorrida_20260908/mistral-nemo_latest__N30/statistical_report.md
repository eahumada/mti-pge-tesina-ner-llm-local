# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.1364
- **p-Value:** 7.1328e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| mistral-nemo:latest_baseline | 30 | 0.8433 | 0.7964 | 0.8902 | 0.1256 |
| mistral-nemo:latest_kb_rag | 30 | 0.8297 | 0.7709 | 0.8886 | 0.1577 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| mistral-nemo:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0136 | 7.1330e-01 | ❌ No | [-0.0873, 0.0601] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 286.2 characters.
- **Outlier Records Identified:** 1 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| mistral-nemo:latest_baseline | 0.8433 | 0.8429 | -0.0005 | 📉 Decreased |
| mistral-nemo:latest_kb_rag | 0.8297 | 0.8308 | +0.0010 | 📈 Improved |