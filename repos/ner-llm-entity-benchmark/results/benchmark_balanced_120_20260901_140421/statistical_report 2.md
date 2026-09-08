# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 10.2096
- **p-Value:** 2.8730e-15

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| llama3.2:latest_baseline | 120 | 0.3945 | 0.3534 | 0.4355 | 0.2269 |
| llama3.2:latest_kb_rag | 120 | 0.4943 | 0.4566 | 0.5321 | 0.2087 |
| gemma4:latest_baseline | 120 | 0.5591 | 0.5229 | 0.5953 | 0.2004 |
| gemma4:latest_kb_rag | 120 | 0.5558 | 0.5181 | 0.5935 | 0.2085 |
| gemma4:31b-mlx_baseline | 120 | 0.5925 | 0.5575 | 0.6276 | 0.1937 |
| gemma4:31b-mlx_kb_rag | 120 | 0.5907 | 0.5516 | 0.6299 | 0.2167 |
| qwen2.5:14b_baseline | 120 | 0.5189 | 0.4849 | 0.5528 | 0.1879 |
| qwen2.5:14b_kb_rag | 120 | 0.5651 | 0.5309 | 0.5992 | 0.1890 |
| gemma:latest_baseline | 120 | 0.4734 | 0.4310 | 0.5157 | 0.2345 |
| gemma:latest_kb_rag | 120 | 0.5303 | 0.4919 | 0.5687 | 0.2126 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b-mlx_baseline vs gemma4:31b-mlx_kb_rag | -0.0018 | 1.0000e+00 | ❌ No | [-0.0871, 0.0835] |
| gemma4:31b-mlx_baseline vs gemma4:latest_baseline | -0.0334 | 9.6540e-01 | ❌ No | [-0.1187, 0.0519] |
| gemma4:31b-mlx_baseline vs gemma4:latest_kb_rag | -0.0368 | 9.3690e-01 | ❌ No | [-0.1221, 0.0485] |
| gemma4:31b-mlx_baseline vs gemma:latest_baseline | -0.1192 | 4.0000e-04 | ✅ Yes | [-0.2045, -0.0339] |
| gemma4:31b-mlx_baseline vs gemma:latest_kb_rag | -0.0622 | 3.8080e-01 | ❌ No | [-0.1475, 0.0230] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_baseline | -0.1981 | 0.0000e+00 | ✅ Yes | [-0.2834, -0.1128] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_kb_rag | -0.0982 | 1.0200e-02 | ✅ Yes | [-0.1835, -0.0129] |
| gemma4:31b-mlx_baseline vs qwen2.5:14b_baseline | -0.0737 | 1.5950e-01 | ❌ No | [-0.1590, 0.0116] |
| gemma4:31b-mlx_baseline vs qwen2.5:14b_kb_rag | -0.0275 | 9.9100e-01 | ❌ No | [-0.1128, 0.0578] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_baseline | -0.0316 | 9.7600e-01 | ❌ No | [-0.1169, 0.0537] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0350 | 9.5370e-01 | ❌ No | [-0.1203, 0.0503] |
| gemma4:31b-mlx_kb_rag vs gemma:latest_baseline | -0.1174 | 6.0000e-04 | ✅ Yes | [-0.2027, -0.0321] |
| gemma4:31b-mlx_kb_rag vs gemma:latest_kb_rag | -0.0604 | 4.2530e-01 | ❌ No | [-0.1457, 0.0248] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_baseline | -0.1963 | 0.0000e+00 | ✅ Yes | [-0.2816, -0.1110] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.0964 | 1.3000e-02 | ✅ Yes | [-0.1817, -0.0111] |
| gemma4:31b-mlx_kb_rag vs qwen2.5:14b_baseline | -0.0719 | 1.8640e-01 | ❌ No | [-0.1572, 0.0134] |
| gemma4:31b-mlx_kb_rag vs qwen2.5:14b_kb_rag | -0.0257 | 9.9450e-01 | ❌ No | [-0.1110, 0.0596] |
| gemma4:latest_baseline vs gemma4:latest_kb_rag | -0.0034 | 1.0000e+00 | ❌ No | [-0.0886, 0.0819] |
| gemma4:latest_baseline vs gemma:latest_baseline | -0.0858 | 4.7400e-02 | ✅ Yes | [-0.1710, -0.0005] |
| gemma4:latest_baseline vs gemma:latest_kb_rag | -0.0288 | 9.8730e-01 | ❌ No | [-0.1141, 0.0565] |
| gemma4:latest_baseline vs llama3.2:latest_baseline | -0.1647 | 0.0000e+00 | ✅ Yes | [-0.2500, -0.0794] |
| gemma4:latest_baseline vs llama3.2:latest_kb_rag | -0.0648 | 3.2190e-01 | ❌ No | [-0.1501, 0.0205] |
| gemma4:latest_baseline vs qwen2.5:14b_baseline | -0.0403 | 8.9370e-01 | ❌ No | [-0.1255, 0.0450] |
| gemma4:latest_baseline vs qwen2.5:14b_kb_rag | 0.0059 | 1.0000e+00 | ❌ No | [-0.0793, 0.0912] |
| gemma4:latest_kb_rag vs gemma:latest_baseline | -0.0824 | 6.8300e-02 | ❌ No | [-0.1677, 0.0029] |
| gemma4:latest_kb_rag vs gemma:latest_kb_rag | -0.0255 | 9.9490e-01 | ❌ No | [-0.1107, 0.0598] |
| gemma4:latest_kb_rag vs llama3.2:latest_baseline | -0.1613 | 0.0000e+00 | ✅ Yes | [-0.2466, -0.0760] |
| gemma4:latest_kb_rag vs llama3.2:latest_kb_rag | -0.0614 | 4.0100e-01 | ❌ No | [-0.1467, 0.0239] |
| gemma4:latest_kb_rag vs qwen2.5:14b_baseline | -0.0369 | 9.3570e-01 | ❌ No | [-0.1222, 0.0484] |
| gemma4:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0093 | 1.0000e+00 | ❌ No | [-0.0760, 0.0946] |
| gemma:latest_baseline vs gemma:latest_kb_rag | 0.0569 | 5.1610e-01 | ❌ No | [-0.0283, 0.1422] |
| gemma:latest_baseline vs llama3.2:latest_baseline | -0.0789 | 9.7700e-02 | ❌ No | [-0.1642, 0.0064] |
| gemma:latest_baseline vs llama3.2:latest_kb_rag | 0.0210 | 9.9880e-01 | ❌ No | [-0.0643, 0.1063] |
| gemma:latest_baseline vs qwen2.5:14b_baseline | 0.0455 | 8.0060e-01 | ❌ No | [-0.0398, 0.1308] |
| gemma:latest_baseline vs qwen2.5:14b_kb_rag | 0.0917 | 2.3500e-02 | ✅ Yes | [0.0064, 0.1770] |
| gemma:latest_kb_rag vs llama3.2:latest_baseline | -0.1359 | 0.0000e+00 | ✅ Yes | [-0.2211, -0.0506] |
| gemma:latest_kb_rag vs llama3.2:latest_kb_rag | -0.0360 | 9.4510e-01 | ❌ No | [-0.1212, 0.0493] |
| gemma:latest_kb_rag vs qwen2.5:14b_baseline | -0.0114 | 1.0000e+00 | ❌ No | [-0.0967, 0.0738] |
| gemma:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0348 | 9.5540e-01 | ❌ No | [-0.0505, 0.1201] |
| llama3.2:latest_baseline vs llama3.2:latest_kb_rag | 0.0999 | 8.1000e-03 | ✅ Yes | [0.0146, 0.1852] |
| llama3.2:latest_baseline vs qwen2.5:14b_baseline | 0.1244 | 2.0000e-04 | ✅ Yes | [0.0391, 0.2097] |
| llama3.2:latest_baseline vs qwen2.5:14b_kb_rag | 0.1706 | 0.0000e+00 | ✅ Yes | [0.0853, 0.2559] |
| llama3.2:latest_kb_rag vs qwen2.5:14b_baseline | 0.0245 | 9.9610e-01 | ❌ No | [-0.0608, 0.1098] |
| llama3.2:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0707 | 2.0520e-01 | ❌ No | [-0.0146, 0.1560] |
| qwen2.5:14b_baseline vs qwen2.5:14b_kb_rag | 0.0462 | 7.8550e-01 | ❌ No | [-0.0391, 0.1315] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 2610.3 characters.
- **Outlier Records Identified:** 14 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:31b-mlx_baseline | 0.5925 | 0.5813 | -0.0112 | 📉 Decreased |
| gemma4:31b-mlx_kb_rag | 0.5907 | 0.5836 | -0.0072 | 📉 Decreased |
| gemma4:latest_baseline | 0.5591 | 0.5434 | -0.0157 | 📉 Decreased |
| gemma4:latest_kb_rag | 0.5558 | 0.5464 | -0.0093 | 📉 Decreased |
| gemma:latest_baseline | 0.4734 | 0.4593 | -0.0141 | 📉 Decreased |
| gemma:latest_kb_rag | 0.5303 | 0.5134 | -0.0169 | 📉 Decreased |
| llama3.2:latest_baseline | 0.3945 | 0.3718 | -0.0227 | 📉 Decreased |
| llama3.2:latest_kb_rag | 0.4943 | 0.4832 | -0.0111 | 📉 Decreased |
| qwen2.5:14b_baseline | 0.5189 | 0.5062 | -0.0127 | 📉 Decreased |
| qwen2.5:14b_kb_rag | 0.5651 | 0.5504 | -0.0147 | 📉 Decreased |