# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.2095
- **p-Value:** 6.4758e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline | 113 | 0.8213 | 0.7962 | 0.8464 | 0.1346 |
| gemma4:31b-cloud_kb_rag | 113 | 0.8294 | 0.8049 | 0.8540 | 0.1317 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline vs gemma4:31b-cloud_kb_rag | 0.0081 | 6.4760e-01 | ❌ No | [-0.0268, 0.0430] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 7 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline | 0.8213 | 0.8241 | +0.0028 | 📈 Improved |
| gemma4:31b-cloud_kb_rag | 0.8294 | 0.8318 | +0.0024 | 📈 Improved |