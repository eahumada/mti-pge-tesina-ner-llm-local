# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.0868
- **p-Value:** 7.7050e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| mistral-nemo:latest_baseline | 15 | 0.6081 | 0.5434 | 0.6728 | 0.1169 |
| mistral-nemo:latest_kb_rag | 15 | 0.6220 | 0.5439 | 0.7001 | 0.1411 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| mistral-nemo:latest_baseline vs mistral-nemo:latest_kb_rag | 0.0139 | 7.7050e-01 | ❌ No | [-0.0830, 0.1108] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 13483.0 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| mistral-nemo:latest_baseline | 0.6081 | 0.6081 | +0.0000 | ⚖️ Stable |
| mistral-nemo:latest_kb_rag | 0.6220 | 0.6220 | +0.0000 | ⚖️ Stable |