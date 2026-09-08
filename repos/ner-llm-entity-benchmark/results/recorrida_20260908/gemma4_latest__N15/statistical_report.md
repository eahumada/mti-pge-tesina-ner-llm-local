# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 2.7553
- **p-Value:** 1.0809e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:latest_baseline | 15 | 0.7177 | 0.6426 | 0.7928 | 0.1356 |
| gemma4:latest_kb_rag | 15 | 0.7959 | 0.7283 | 0.8635 | 0.1221 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:latest_baseline vs gemma4:latest_kb_rag | 0.0782 | 1.0810e-01 | ❌ No | [-0.0183, 0.1747] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 13483.0 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:latest_baseline | 0.7177 | 0.7177 | +0.0000 | ⚖️ Stable |
| gemma4:latest_kb_rag | 0.7959 | 0.7959 | +0.0000 | ⚖️ Stable |