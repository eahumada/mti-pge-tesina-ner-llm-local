# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 1.4136
- **p-Value:** 2.4445e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| qwen3:8b_baseline | 15 | 0.6768 | 0.6159 | 0.7376 | 0.1098 |
| qwen3:8b_kb_rag | 15 | 0.7304 | 0.6551 | 0.8058 | 0.1361 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| qwen3:8b_baseline vs qwen3:8b_kb_rag | 0.0537 | 2.4450e-01 | ❌ No | [-0.0388, 0.1462] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 13483.0 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| qwen3:8b_baseline | 0.6768 | 0.6768 | +0.0000 | ⚖️ Stable |
| qwen3:8b_kb_rag | 0.7304 | 0.7304 | +0.0000 | ⚖️ Stable |