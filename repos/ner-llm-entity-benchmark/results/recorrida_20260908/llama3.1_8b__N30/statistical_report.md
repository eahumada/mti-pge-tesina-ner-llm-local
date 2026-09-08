# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.2039
- **p-Value:** 6.5325e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| llama3.1:8b_baseline | 30 | 0.8096 | 0.7535 | 0.8657 | 0.1502 |
| llama3.1:8b_kb_rag | 30 | 0.8267 | 0.7728 | 0.8807 | 0.1444 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| llama3.1:8b_baseline vs llama3.1:8b_kb_rag | 0.0172 | 6.5330e-01 | ❌ No | [-0.0590, 0.0933] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 286.2 characters.
- **Outlier Records Identified:** 1 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| llama3.1:8b_baseline | 0.8096 | 0.8099 | +0.0003 | 📈 Improved |
| llama3.1:8b_kb_rag | 0.8267 | 0.8277 | +0.0009 | 📈 Improved |