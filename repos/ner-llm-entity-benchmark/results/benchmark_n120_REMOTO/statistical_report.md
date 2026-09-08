# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 21.2697
- **p-Value:** 2.6541e-47

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:12b-mlx_baseline | 120 | 0.2731 | 0.2131 | 0.3331 | 0.3319 |
| gemma4:12b-mlx_kb_rag | 120 | 0.1121 | 0.0679 | 0.1562 | 0.2443 |
| qwen3:8b_baseline | 120 | 0.4483 | 0.4035 | 0.4930 | 0.2475 |
| qwen3:8b_kb_rag | 120 | 0.4425 | 0.3900 | 0.4950 | 0.2904 |
| mistral-nemo:latest_baseline | 120 | 0.4505 | 0.4122 | 0.4889 | 0.2122 |
| mistral-nemo:latest_kb_rag | 120 | 0.4826 | 0.4446 | 0.5205 | 0.2100 |
| llama3.1:8b_baseline | 120 | 0.4959 | 0.4625 | 0.5294 | 0.1852 |
| llama3.1:8b_kb_rag | 120 | 0.5491 | 0.5107 | 0.5876 | 0.2128 |
| nemotron-mini:4b_baseline | 120 | 0.3630 | 0.3063 | 0.4197 | 0.3138 |
| nemotron-mini:4b_kb_rag | 120 | 0.4399 | 0.3957 | 0.4842 | 0.2449 |
| deepseek-r1:1.5b_baseline | 120 | 0.3400 | 0.2923 | 0.3877 | 0.2637 |
| deepseek-r1:1.5b_kb_rag | 120 | 0.3394 | 0.2877 | 0.3910 | 0.2858 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline vs deepseek-r1:1.5b_kb_rag | -0.0006 | 1.0000e+00 | ❌ No | [-0.1139, 0.1127] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_baseline | -0.0669 | 7.7820e-01 | ❌ No | [-0.1802, 0.0464] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_kb_rag | -0.2279 | 0.0000e+00 | ✅ Yes | [-0.3412, -0.1146] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_baseline | 0.1559 | 3.0000e-04 | ✅ Yes | [0.0426, 0.2692] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_kb_rag | 0.2091 | 0.0000e+00 | ✅ Yes | [0.0959, 0.3224] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_baseline | 0.1105 | 6.4300e-02 | ❌ No | [-0.0028, 0.2238] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_kb_rag | 0.1426 | 2.0000e-03 | ✅ Yes | [0.0293, 0.2559] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_baseline | 0.0230 | 1.0000e+00 | ❌ No | [-0.0903, 0.1363] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_kb_rag | 0.0999 | 1.5280e-01 | ❌ No | [-0.0133, 0.2132] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_baseline | 0.1083 | 7.8300e-02 | ❌ No | [-0.0050, 0.2215] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_kb_rag | 0.1025 | 1.2530e-01 | ❌ No | [-0.0107, 0.2158] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_baseline | -0.0663 | 7.8960e-01 | ❌ No | [-0.1796, 0.0470] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_kb_rag | -0.2273 | 0.0000e+00 | ✅ Yes | [-0.3406, -0.1140] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_baseline | 0.1566 | 3.0000e-04 | ✅ Yes | [0.0433, 0.2699] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_kb_rag | 0.2098 | 0.0000e+00 | ✅ Yes | [0.0965, 0.3231] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_baseline | 0.1111 | 6.0800e-02 | ❌ No | [-0.0021, 0.2244] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_kb_rag | 0.1432 | 1.9000e-03 | ✅ Yes | [0.0299, 0.2565] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_baseline | 0.0237 | 1.0000e+00 | ❌ No | [-0.0896, 0.1369] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_kb_rag | 0.1006 | 1.4580e-01 | ❌ No | [-0.0127, 0.2139] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_baseline | 0.1089 | 7.4200e-02 | ❌ No | [-0.0044, 0.2222] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_kb_rag | 0.1032 | 1.1920e-01 | ❌ No | [-0.0101, 0.2165] |
| gemma4:12b-mlx_baseline vs gemma4:12b-mlx_kb_rag | -0.1610 | 2.0000e-04 | ✅ Yes | [-0.2743, -0.0477] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_baseline | 0.2228 | 0.0000e+00 | ✅ Yes | [0.1095, 0.3361] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_kb_rag | 0.2760 | 0.0000e+00 | ✅ Yes | [0.1628, 0.3893] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_baseline | 0.1774 | 0.0000e+00 | ✅ Yes | [0.0641, 0.2907] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_kb_rag | 0.2095 | 0.0000e+00 | ✅ Yes | [0.0962, 0.3228] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_baseline | 0.0899 | 2.9980e-01 | ❌ No | [-0.0234, 0.2032] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_kb_rag | 0.1668 | 1.0000e-04 | ✅ Yes | [0.0536, 0.2801] |
| gemma4:12b-mlx_baseline vs qwen3:8b_baseline | 0.1752 | 0.0000e+00 | ✅ Yes | [0.0619, 0.2884] |
| gemma4:12b-mlx_baseline vs qwen3:8b_kb_rag | 0.1694 | 0.0000e+00 | ✅ Yes | [0.0562, 0.2827] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_baseline | 0.3839 | 0.0000e+00 | ✅ Yes | [0.2706, 0.4971] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_kb_rag | 0.4371 | 0.0000e+00 | ✅ Yes | [0.3238, 0.5504] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_baseline | 0.3384 | 0.0000e+00 | ✅ Yes | [0.2252, 0.4517] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | 0.3705 | 0.0000e+00 | ✅ Yes | [0.2572, 0.4838] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_baseline | 0.2509 | 0.0000e+00 | ✅ Yes | [0.1377, 0.3642] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | 0.3279 | 0.0000e+00 | ✅ Yes | [0.2146, 0.4412] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_baseline | 0.3362 | 0.0000e+00 | ✅ Yes | [0.2229, 0.4495] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_kb_rag | 0.3305 | 0.0000e+00 | ✅ Yes | [0.2172, 0.4438] |
| llama3.1:8b_baseline vs llama3.1:8b_kb_rag | 0.0532 | 9.5180e-01 | ❌ No | [-0.0601, 0.1665] |
| llama3.1:8b_baseline vs mistral-nemo:latest_baseline | -0.0454 | 9.8730e-01 | ❌ No | [-0.1587, 0.0679] |
| llama3.1:8b_baseline vs mistral-nemo:latest_kb_rag | -0.0134 | 1.0000e+00 | ❌ No | [-0.1267, 0.0999] |
| llama3.1:8b_baseline vs nemotron-mini:4b_baseline | -0.1329 | 6.5000e-03 | ✅ Yes | [-0.2462, -0.0196] |
| llama3.1:8b_baseline vs nemotron-mini:4b_kb_rag | -0.0560 | 9.2940e-01 | ❌ No | [-0.1693, 0.0573] |
| llama3.1:8b_baseline vs qwen3:8b_baseline | -0.0477 | 9.8050e-01 | ❌ No | [-0.1610, 0.0656] |
| llama3.1:8b_baseline vs qwen3:8b_kb_rag | -0.0534 | 9.5060e-01 | ❌ No | [-0.1667, 0.0599] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_baseline | -0.0986 | 1.6830e-01 | ❌ No | [-0.2119, 0.0147] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_kb_rag | -0.0666 | 7.8400e-01 | ❌ No | [-0.1799, 0.0467] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_baseline | -0.1861 | 0.0000e+00 | ✅ Yes | [-0.2994, -0.0728] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_kb_rag | -0.1092 | 7.2200e-02 | ❌ No | [-0.2225, 0.0041] |
| llama3.1:8b_kb_rag vs qwen3:8b_baseline | -0.1009 | 1.4240e-01 | ❌ No | [-0.2142, 0.0124] |
| llama3.1:8b_kb_rag vs qwen3:8b_kb_rag | -0.1066 | 9.0100e-02 | ❌ No | [-0.2199, 0.0067] |
| mistral-nemo:latest_baseline vs mistral-nemo:latest_kb_rag | 0.0321 | 9.9960e-01 | ❌ No | [-0.0812, 0.1453] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_baseline | -0.0875 | 3.4500e-01 | ❌ No | [-0.2008, 0.0258] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_kb_rag | -0.0106 | 1.0000e+00 | ❌ No | [-0.1239, 0.1027] |
| mistral-nemo:latest_baseline vs qwen3:8b_baseline | -0.0023 | 1.0000e+00 | ❌ No | [-0.1155, 0.1110] |
| mistral-nemo:latest_baseline vs qwen3:8b_kb_rag | -0.0080 | 1.0000e+00 | ❌ No | [-0.1213, 0.1053] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_baseline | -0.1195 | 2.7400e-02 | ✅ Yes | [-0.2328, -0.0063] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.0426 | 9.9290e-01 | ❌ No | [-0.1559, 0.0707] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_baseline | -0.0343 | 9.9920e-01 | ❌ No | [-0.1476, 0.0790] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_kb_rag | -0.0400 | 9.9610e-01 | ❌ No | [-0.1533, 0.0733] |
| nemotron-mini:4b_baseline vs nemotron-mini:4b_kb_rag | 0.0769 | 5.6980e-01 | ❌ No | [-0.0364, 0.1902] |
| nemotron-mini:4b_baseline vs qwen3:8b_baseline | 0.0852 | 3.8970e-01 | ❌ No | [-0.0280, 0.1985] |
| nemotron-mini:4b_baseline vs qwen3:8b_kb_rag | 0.0795 | 5.1220e-01 | ❌ No | [-0.0338, 0.1928] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_baseline | 0.0083 | 1.0000e+00 | ❌ No | [-0.1050, 0.1216] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_kb_rag | 0.0026 | 1.0000e+00 | ❌ No | [-0.1107, 0.1159] |
| qwen3:8b_baseline vs qwen3:8b_kb_rag | -0.0057 | 1.0000e+00 | ❌ No | [-0.1190, 0.1076] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 2610.3 characters.
- **Outlier Records Identified:** 14 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline | 0.3400 | 0.3339 | -0.0061 | 📉 Decreased |
| deepseek-r1:1.5b_kb_rag | 0.3394 | 0.3409 | +0.0015 | 📈 Improved |
| gemma4:12b-mlx_baseline | 0.2731 | 0.2973 | +0.0242 | 📈 Improved |
| gemma4:12b-mlx_kb_rag | 0.1121 | 0.1269 | +0.0148 | 📈 Improved |
| llama3.1:8b_baseline | 0.4959 | 0.4872 | -0.0088 | 📉 Decreased |
| llama3.1:8b_kb_rag | 0.5491 | 0.5375 | -0.0116 | 📉 Decreased |
| mistral-nemo:latest_baseline | 0.4505 | 0.4349 | -0.0156 | 📉 Decreased |
| mistral-nemo:latest_kb_rag | 0.4826 | 0.4705 | -0.0120 | 📉 Decreased |
| nemotron-mini:4b_baseline | 0.3630 | 0.3681 | +0.0050 | 📈 Improved |
| nemotron-mini:4b_kb_rag | 0.4399 | 0.4353 | -0.0047 | 📉 Decreased |
| qwen3:8b_baseline | 0.4483 | 0.4336 | -0.0146 | 📉 Decreased |
| qwen3:8b_kb_rag | 0.4425 | 0.4573 | +0.0147 | 📈 Improved |