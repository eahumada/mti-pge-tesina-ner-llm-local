# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 0.8279
- **p-Value:** 4.7894e-01

> [!NOTE]
> **Verdict:** There is **no statistically significant difference** in F1-Scores between the evaluated models ($p \ge 0.05$).

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| zs-en | 120 | 0.7382 | 0.7107 | 0.7657 | 0.1522 |
| zs-es | 120 | 0.7543 | 0.7271 | 0.7815 | 0.1504 |
| fs-es | 120 | 0.7623 | 0.7378 | 0.7867 | 0.1354 |
| fs-en | 120 | 0.7650 | 0.7394 | 0.7905 | 0.1414 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| fs-en vs fs-es | -0.0027 | 9.9890e-01 | ❌ No | [-0.0510, 0.0456] |
| fs-en vs zs-en | -0.0268 | 4.8100e-01 | ❌ No | [-0.0750, 0.0215] |
| fs-en vs zs-es | -0.0107 | 9.4080e-01 | ❌ No | [-0.0589, 0.0376] |
| fs-es vs zs-en | -0.0241 | 5.7210e-01 | ❌ No | [-0.0723, 0.0242] |
| fs-es vs zs-es | -0.0080 | 9.7390e-01 | ❌ No | [-0.0562, 0.0403] |
| zs-en vs zs-es | 0.0161 | 8.2560e-01 | ❌ No | [-0.0322, 0.0644] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 10 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| fs-en | 0.7650 | 0.7632 | -0.0018 | 📉 Decreased |
| fs-es | 0.7623 | 0.7580 | -0.0042 | 📉 Decreased |
| zs-en | 0.7382 | 0.7351 | -0.0031 | 📉 Decreased |
| zs-es | 0.7543 | 0.7537 | -0.0006 | 📉 Decreased |