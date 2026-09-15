# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 1.4086
- **p-Value:** 2.4985e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 15 | 0.6471 | 0.5206 | 0.7736 | 0.2284 |
| zs-es | 15 | 0.7152 | 0.6159 | 0.8145 | 0.1794 |
| fs-es | 15 | 0.7973 | 0.7212 | 0.8734 | 0.1374 |
| fs-en | 15 | 0.6640 | 0.4973 | 0.8307 | 0.3011 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | 0.1333 | 3.5520e-01 | ❌ No | [-0.0795, 0.3461] |
| fs-en vs zs-en | -0.0169 | 9.9670e-01 | ❌ No | [-0.2297, 0.1960] |
| fs-en vs zs-es | 0.0512 | 9.1950e-01 | ❌ No | [-0.1616, 0.2641] |
| fs-es vs zs-en | -0.1502 | 2.5330e-01 | ❌ No | [-0.3630, 0.0627] |
| fs-es vs zs-es | -0.0821 | 7.3780e-01 | ❌ No | [-0.2949, 0.1308] |
| zs-en vs zs-es | 0.0681 | 8.3160e-01 | ❌ No | [-0.1447, 0.2809] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 13483.0 characters.
- **Outlier Records Identified:** 0 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.6640 | 0.6640 | +0.0000 | ⚖️ Stable |
| fs-es | 0.7973 | 0.7973 | +0.0000 | ⚖️ Stable |
| zs-en | 0.6471 | 0.6471 | +0.0000 | ⚖️ Stable |
| zs-es | 0.7152 | 0.7152 | +0.0000 | ⚖️ Stable |