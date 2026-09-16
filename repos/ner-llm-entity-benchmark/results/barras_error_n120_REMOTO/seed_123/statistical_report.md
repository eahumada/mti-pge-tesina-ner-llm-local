# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 87.4278
- **p-Value:** 7.7186e-279

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline | 113 | 0.4859 | 0.4061 | 0.5658 | 0.4285 |
| gemma4:31b-cloud_kb_rag | 113 | 0.5860 | 0.5121 | 0.6599 | 0.3966 |
| gemma4:31b-mlx_baseline | 113 | 0.8157 | 0.7894 | 0.8419 | 0.1407 |
| gemma4:31b-mlx_kb_rag | 113 | 0.8252 | 0.8004 | 0.8500 | 0.1331 |
| gemma4:12b-mlx_baseline | 113 | 0.7813 | 0.7549 | 0.8077 | 0.1416 |
| gemma4:12b-mlx_kb_rag | 113 | 0.7982 | 0.7730 | 0.8233 | 0.1351 |
| gemma4:latest_baseline | 113 | 0.7541 | 0.7261 | 0.7822 | 0.1504 |
| gemma4:latest_kb_rag | 113 | 0.7822 | 0.7556 | 0.8088 | 0.1426 |
| qwen3:8b_baseline | 113 | 0.6904 | 0.6608 | 0.7200 | 0.1587 |
| qwen3:8b_kb_rag | 113 | 0.6920 | 0.6639 | 0.7201 | 0.1509 |
| gpt-oss:20b_baseline | 113 | 0.7550 | 0.7254 | 0.7845 | 0.1585 |
| gpt-oss:20b_kb_rag | 113 | 0.7728 | 0.7462 | 0.7994 | 0.1427 |
| mistral-nemo:latest_baseline | 113 | 0.6064 | 0.5729 | 0.6399 | 0.1798 |
| mistral-nemo:latest_kb_rag | 113 | 0.5751 | 0.5409 | 0.6092 | 0.1832 |
| llama3.2:latest_baseline | 113 | 0.6255 | 0.5918 | 0.6591 | 0.1807 |
| llama3.2:latest_kb_rag | 113 | 0.6947 | 0.6644 | 0.7251 | 0.1626 |
| llama3.1:8b_baseline | 113 | 0.6996 | 0.6713 | 0.7280 | 0.1521 |
| llama3.1:8b_kb_rag | 113 | 0.7117 | 0.6824 | 0.7411 | 0.1576 |
| nemotron-mini:4b_baseline | 113 | 0.2756 | 0.2367 | 0.3145 | 0.2087 |
| nemotron-mini:4b_kb_rag | 113 | 0.4005 | 0.3656 | 0.4355 | 0.1874 |
| deepseek-r1:1.5b_baseline | 113 | 0.2811 | 0.2471 | 0.3151 | 0.1823 |
| deepseek-r1:1.5b_kb_rag | 113 | 0.3196 | 0.2852 | 0.3539 | 0.1843 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline vs deepseek-r1:1.5b_kb_rag | 0.0385 | 9.9830e-01 | ❌ No | [-0.0568, 0.1337] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_baseline | 0.5002 | 0.0000e+00 | ✅ Yes | [0.4049, 0.5955] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_kb_rag | 0.5171 | 0.0000e+00 | ✅ Yes | [0.4218, 0.6123] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_baseline | 0.2048 | 0.0000e+00 | ✅ Yes | [0.1095, 0.3001] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_kb_rag | 0.3049 | 0.0000e+00 | ✅ Yes | [0.2096, 0.4002] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_baseline | 0.5346 | 0.0000e+00 | ✅ Yes | [0.4393, 0.6298] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_kb_rag | 0.5441 | 0.0000e+00 | ✅ Yes | [0.4488, 0.6394] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_baseline | 0.4730 | 0.0000e+00 | ✅ Yes | [0.3778, 0.5683] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_kb_rag | 0.5011 | 0.0000e+00 | ✅ Yes | [0.4058, 0.5963] |
| deepseek-r1:1.5b_baseline vs gpt-oss:20b_baseline | 0.4739 | 0.0000e+00 | ✅ Yes | [0.3786, 0.5691] |
| deepseek-r1:1.5b_baseline vs gpt-oss:20b_kb_rag | 0.4917 | 0.0000e+00 | ✅ Yes | [0.3964, 0.5869] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_baseline | 0.4185 | 0.0000e+00 | ✅ Yes | [0.3232, 0.5138] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_kb_rag | 0.4306 | 0.0000e+00 | ✅ Yes | [0.3353, 0.5259] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_baseline | 0.3444 | 0.0000e+00 | ✅ Yes | [0.2491, 0.4396] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_kb_rag | 0.4136 | 0.0000e+00 | ✅ Yes | [0.3184, 0.5089] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_baseline | 0.3253 | 0.0000e+00 | ✅ Yes | [0.2300, 0.4205] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_kb_rag | 0.2940 | 0.0000e+00 | ✅ Yes | [0.1987, 0.3892] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_baseline | -0.0055 | 1.0000e+00 | ❌ No | [-0.1008, 0.0897] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_kb_rag | 0.1194 | 1.4000e-03 | ✅ Yes | [0.0242, 0.2147] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_baseline | 0.4093 | 0.0000e+00 | ✅ Yes | [0.3140, 0.5045] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_kb_rag | 0.4109 | 0.0000e+00 | ✅ Yes | [0.3156, 0.5062] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_baseline | 0.4617 | 0.0000e+00 | ✅ Yes | [0.3665, 0.5570] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_kb_rag | 0.4786 | 0.0000e+00 | ✅ Yes | [0.3833, 0.5739] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-cloud_baseline | 0.1664 | 0.0000e+00 | ✅ Yes | [0.0711, 0.2616] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-cloud_kb_rag | 0.2664 | 0.0000e+00 | ✅ Yes | [0.1712, 0.3617] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-mlx_baseline | 0.4961 | 0.0000e+00 | ✅ Yes | [0.4008, 0.5914] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-mlx_kb_rag | 0.5056 | 0.0000e+00 | ✅ Yes | [0.4104, 0.6009] |
| deepseek-r1:1.5b_kb_rag vs gemma4:latest_baseline | 0.4346 | 0.0000e+00 | ✅ Yes | [0.3393, 0.5298] |
| deepseek-r1:1.5b_kb_rag vs gemma4:latest_kb_rag | 0.4626 | 0.0000e+00 | ✅ Yes | [0.3673, 0.5579] |
| deepseek-r1:1.5b_kb_rag vs gpt-oss:20b_baseline | 0.4354 | 0.0000e+00 | ✅ Yes | [0.3401, 0.5307] |
| deepseek-r1:1.5b_kb_rag vs gpt-oss:20b_kb_rag | 0.4532 | 0.0000e+00 | ✅ Yes | [0.3580, 0.5485] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_baseline | 0.3800 | 0.0000e+00 | ✅ Yes | [0.2848, 0.4753] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_kb_rag | 0.3922 | 0.0000e+00 | ✅ Yes | [0.2969, 0.4874] |
| deepseek-r1:1.5b_kb_rag vs llama3.2:latest_baseline | 0.3059 | 0.0000e+00 | ✅ Yes | [0.2106, 0.4012] |
| deepseek-r1:1.5b_kb_rag vs llama3.2:latest_kb_rag | 0.3752 | 0.0000e+00 | ✅ Yes | [0.2799, 0.4704] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_baseline | 0.2868 | 0.0000e+00 | ✅ Yes | [0.1915, 0.3821] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_kb_rag | 0.2555 | 0.0000e+00 | ✅ Yes | [0.1602, 0.3508] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_baseline | -0.0440 | 9.9030e-01 | ❌ No | [-0.1393, 0.0513] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_kb_rag | 0.0810 | 2.3120e-01 | ❌ No | [-0.0143, 0.1762] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_baseline | 0.3708 | 0.0000e+00 | ✅ Yes | [0.2756, 0.4661] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_kb_rag | 0.3724 | 0.0000e+00 | ✅ Yes | [0.2772, 0.4677] |
| gemma4:12b-mlx_baseline vs gemma4:12b-mlx_kb_rag | 0.0169 | 1.0000e+00 | ❌ No | [-0.0784, 0.1121] |
| gemma4:12b-mlx_baseline vs gemma4:31b-cloud_baseline | -0.2954 | 0.0000e+00 | ✅ Yes | [-0.3907, -0.2001] |
| gemma4:12b-mlx_baseline vs gemma4:31b-cloud_kb_rag | -0.1953 | 0.0000e+00 | ✅ Yes | [-0.2906, -0.1000] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_baseline | 0.0344 | 9.9970e-01 | ❌ No | [-0.0609, 0.1296] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_kb_rag | 0.0439 | 9.9050e-01 | ❌ No | [-0.0514, 0.1392] |
| gemma4:12b-mlx_baseline vs gemma4:latest_baseline | -0.0272 | 1.0000e+00 | ❌ No | [-0.1224, 0.0681] |
| gemma4:12b-mlx_baseline vs gemma4:latest_kb_rag | 0.0009 | 1.0000e+00 | ❌ No | [-0.0944, 0.0961] |
| gemma4:12b-mlx_baseline vs gpt-oss:20b_baseline | -0.0263 | 1.0000e+00 | ❌ No | [-0.1216, 0.0689] |
| gemma4:12b-mlx_baseline vs gpt-oss:20b_kb_rag | -0.0085 | 1.0000e+00 | ❌ No | [-0.1038, 0.0867] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_baseline | -0.0817 | 2.1620e-01 | ❌ No | [-0.1770, 0.0136] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_kb_rag | -0.0696 | 5.3130e-01 | ❌ No | [-0.1649, 0.0257] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_baseline | -0.1558 | 0.0000e+00 | ✅ Yes | [-0.2511, -0.0606] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_kb_rag | -0.0866 | 1.3470e-01 | ❌ No | [-0.1818, 0.0087] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_baseline | -0.1749 | 0.0000e+00 | ✅ Yes | [-0.2702, -0.0797] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.2062 | 0.0000e+00 | ✅ Yes | [-0.3015, -0.1110] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_baseline | -0.5057 | 0.0000e+00 | ✅ Yes | [-0.6010, -0.4105] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_kb_rag | -0.3808 | 0.0000e+00 | ✅ Yes | [-0.4760, -0.2855] |
| gemma4:12b-mlx_baseline vs qwen3:8b_baseline | -0.0909 | 8.3900e-02 | ❌ No | [-0.1862, 0.0043] |
| gemma4:12b-mlx_baseline vs qwen3:8b_kb_rag | -0.0893 | 1.0040e-01 | ❌ No | [-0.1846, 0.0060] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-cloud_baseline | -0.3122 | 0.0000e+00 | ✅ Yes | [-0.4075, -0.2170] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-cloud_kb_rag | -0.2122 | 0.0000e+00 | ✅ Yes | [-0.3074, -0.1169] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_baseline | 0.0175 | 1.0000e+00 | ❌ No | [-0.0778, 0.1128] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_kb_rag | 0.0270 | 1.0000e+00 | ❌ No | [-0.0682, 0.1223] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_baseline | -0.0440 | 9.9010e-01 | ❌ No | [-0.1393, 0.0512] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0160 | 1.0000e+00 | ❌ No | [-0.1113, 0.0793] |
| gemma4:12b-mlx_kb_rag vs gpt-oss:20b_baseline | -0.0432 | 9.9220e-01 | ❌ No | [-0.1385, 0.0521] |
| gemma4:12b-mlx_kb_rag vs gpt-oss:20b_kb_rag | -0.0254 | 1.0000e+00 | ❌ No | [-0.1206, 0.0699] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_baseline | -0.0986 | 3.2900e-02 | ✅ Yes | [-0.1938, -0.0033] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_kb_rag | -0.0864 | 1.3660e-01 | ❌ No | [-0.1817, 0.0088] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_baseline | -0.1727 | 0.0000e+00 | ✅ Yes | [-0.2680, -0.0774] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.1034 | 1.7000e-02 | ✅ Yes | [-0.1987, -0.0082] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.1918 | 0.0000e+00 | ✅ Yes | [-0.2871, -0.0965] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.2231 | 0.0000e+00 | ✅ Yes | [-0.3184, -0.1278] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_baseline | -0.5226 | 0.0000e+00 | ✅ Yes | [-0.6179, -0.4273] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | -0.3976 | 0.0000e+00 | ✅ Yes | [-0.4929, -0.3024] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_baseline | -0.1078 | 9.0000e-03 | ✅ Yes | [-0.2030, -0.0125] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.1062 | 1.1400e-02 | ✅ Yes | [-0.2014, -0.0109] |
| gemma4:31b-cloud_baseline vs gemma4:31b-cloud_kb_rag | 0.1001 | 2.6900e-02 | ✅ Yes | [0.0048, 0.1953] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_baseline | 0.3297 | 0.0000e+00 | ✅ Yes | [0.2345, 0.4250] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_kb_rag | 0.3393 | 0.0000e+00 | ✅ Yes | [0.2440, 0.4345] |
| gemma4:31b-cloud_baseline vs gemma4:latest_baseline | 0.2682 | 0.0000e+00 | ✅ Yes | [0.1729, 0.3635] |
| gemma4:31b-cloud_baseline vs gemma4:latest_kb_rag | 0.2962 | 0.0000e+00 | ✅ Yes | [0.2010, 0.3915] |
| gemma4:31b-cloud_baseline vs gpt-oss:20b_baseline | 0.2691 | 0.0000e+00 | ✅ Yes | [0.1738, 0.3643] |
| gemma4:31b-cloud_baseline vs gpt-oss:20b_kb_rag | 0.2869 | 0.0000e+00 | ✅ Yes | [0.1916, 0.3821] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_baseline | 0.2137 | 0.0000e+00 | ✅ Yes | [0.1184, 0.3089] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_kb_rag | 0.2258 | 0.0000e+00 | ✅ Yes | [0.1305, 0.3211] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_baseline | 0.1395 | 0.0000e+00 | ✅ Yes | [0.0443, 0.2348] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_kb_rag | 0.2088 | 0.0000e+00 | ✅ Yes | [0.1135, 0.3041] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_baseline | 0.1205 | 1.2000e-03 | ✅ Yes | [0.0252, 0.2157] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_kb_rag | 0.0891 | 1.0230e-01 | ❌ No | [-0.0061, 0.1844] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_baseline | -0.2103 | 0.0000e+00 | ✅ Yes | [-0.3056, -0.1151] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_kb_rag | -0.0854 | 1.5190e-01 | ❌ No | [-0.1807, 0.0099] |
| gemma4:31b-cloud_baseline vs qwen3:8b_baseline | 0.2045 | 0.0000e+00 | ✅ Yes | [0.1092, 0.2997] |
| gemma4:31b-cloud_baseline vs qwen3:8b_kb_rag | 0.2061 | 0.0000e+00 | ✅ Yes | [0.1108, 0.3013] |
| gemma4:31b-cloud_kb_rag vs gemma4:31b-mlx_baseline | 0.2297 | 0.0000e+00 | ✅ Yes | [0.1344, 0.3249] |
| gemma4:31b-cloud_kb_rag vs gemma4:31b-mlx_kb_rag | 0.2392 | 0.0000e+00 | ✅ Yes | [0.1439, 0.3345] |
| gemma4:31b-cloud_kb_rag vs gemma4:latest_baseline | 0.1681 | 0.0000e+00 | ✅ Yes | [0.0729, 0.2634] |
| gemma4:31b-cloud_kb_rag vs gemma4:latest_kb_rag | 0.1962 | 0.0000e+00 | ✅ Yes | [0.1009, 0.2914] |
| gemma4:31b-cloud_kb_rag vs gpt-oss:20b_baseline | 0.1690 | 0.0000e+00 | ✅ Yes | [0.0737, 0.2643] |
| gemma4:31b-cloud_kb_rag vs gpt-oss:20b_kb_rag | 0.1868 | 0.0000e+00 | ✅ Yes | [0.0915, 0.2821] |
| gemma4:31b-cloud_kb_rag vs llama3.1:8b_baseline | 0.1136 | 3.7000e-03 | ✅ Yes | [0.0183, 0.2089] |
| gemma4:31b-cloud_kb_rag vs llama3.1:8b_kb_rag | 0.1257 | 5.0000e-04 | ✅ Yes | [0.0305, 0.2210] |
| gemma4:31b-cloud_kb_rag vs llama3.2:latest_baseline | 0.0395 | 9.9760e-01 | ❌ No | [-0.0558, 0.1347] |
| gemma4:31b-cloud_kb_rag vs llama3.2:latest_kb_rag | 0.1087 | 7.8000e-03 | ✅ Yes | [0.0135, 0.2040] |
| gemma4:31b-cloud_kb_rag vs mistral-nemo:latest_baseline | 0.0204 | 1.0000e+00 | ❌ No | [-0.0749, 0.1156] |
| gemma4:31b-cloud_kb_rag vs mistral-nemo:latest_kb_rag | -0.0109 | 1.0000e+00 | ❌ No | [-0.1062, 0.0843] |
| gemma4:31b-cloud_kb_rag vs nemotron-mini:4b_baseline | -0.3104 | 0.0000e+00 | ✅ Yes | [-0.4057, -0.2151] |
| gemma4:31b-cloud_kb_rag vs nemotron-mini:4b_kb_rag | -0.1855 | 0.0000e+00 | ✅ Yes | [-0.2807, -0.0902] |
| gemma4:31b-cloud_kb_rag vs qwen3:8b_baseline | 0.1044 | 1.4800e-02 | ✅ Yes | [0.0091, 0.1997] |
| gemma4:31b-cloud_kb_rag vs qwen3:8b_kb_rag | 0.1060 | 1.1700e-02 | ✅ Yes | [0.0107, 0.2013] |
| gemma4:31b-mlx_baseline vs gemma4:31b-mlx_kb_rag | 0.0095 | 1.0000e+00 | ❌ No | [-0.0857, 0.1048] |
| gemma4:31b-mlx_baseline vs gemma4:latest_baseline | -0.0615 | 7.6280e-01 | ❌ No | [-0.1568, 0.0337] |
| gemma4:31b-mlx_baseline vs gemma4:latest_kb_rag | -0.0335 | 9.9980e-01 | ❌ No | [-0.1288, 0.0618] |
| gemma4:31b-mlx_baseline vs gpt-oss:20b_baseline | -0.0607 | 7.8400e-01 | ❌ No | [-0.1560, 0.0346] |
| gemma4:31b-mlx_baseline vs gpt-oss:20b_kb_rag | -0.0429 | 9.9290e-01 | ❌ No | [-0.1381, 0.0524] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_baseline | -0.1161 | 2.5000e-03 | ✅ Yes | [-0.2113, -0.0208] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_kb_rag | -0.1039 | 1.5800e-02 | ✅ Yes | [-0.1992, -0.0087] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_baseline | -0.1902 | 0.0000e+00 | ✅ Yes | [-0.2855, -0.0949] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_kb_rag | -0.1209 | 1.1000e-03 | ✅ Yes | [-0.2162, -0.0257] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_baseline | -0.2093 | 0.0000e+00 | ✅ Yes | [-0.3046, -0.1140] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.2406 | 0.0000e+00 | ✅ Yes | [-0.3359, -0.1453] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_baseline | -0.5401 | 0.0000e+00 | ✅ Yes | [-0.6354, -0.4448] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_kb_rag | -0.4151 | 0.0000e+00 | ✅ Yes | [-0.5104, -0.3199] |
| gemma4:31b-mlx_baseline vs qwen3:8b_baseline | -0.1253 | 5.0000e-04 | ✅ Yes | [-0.2205, -0.0300] |
| gemma4:31b-mlx_baseline vs qwen3:8b_kb_rag | -0.1237 | 7.0000e-04 | ✅ Yes | [-0.2189, -0.0284] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_baseline | -0.0711 | 4.8720e-01 | ❌ No | [-0.1663, 0.0242] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0430 | 9.9260e-01 | ❌ No | [-0.1383, 0.0522] |
| gemma4:31b-mlx_kb_rag vs gpt-oss:20b_baseline | -0.0702 | 5.1250e-01 | ❌ No | [-0.1655, 0.0251] |
| gemma4:31b-mlx_kb_rag vs gpt-oss:20b_kb_rag | -0.0524 | 9.3490e-01 | ❌ No | [-0.1477, 0.0429] |
| gemma4:31b-mlx_kb_rag vs llama3.1:8b_baseline | -0.1256 | 5.0000e-04 | ✅ Yes | [-0.2209, -0.0303] |
| gemma4:31b-mlx_kb_rag vs llama3.1:8b_kb_rag | -0.1135 | 3.7000e-03 | ✅ Yes | [-0.2087, -0.0182] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_baseline | -0.1997 | 0.0000e+00 | ✅ Yes | [-0.2950, -0.1045] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.1305 | 2.0000e-04 | ✅ Yes | [-0.2257, -0.0352] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.2188 | 0.0000e+00 | ✅ Yes | [-0.3141, -0.1235] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.2501 | 0.0000e+00 | ✅ Yes | [-0.3454, -0.1549] |
| gemma4:31b-mlx_kb_rag vs nemotron-mini:4b_baseline | -0.5496 | 0.0000e+00 | ✅ Yes | [-0.6449, -0.4543] |
| gemma4:31b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | -0.4247 | 0.0000e+00 | ✅ Yes | [-0.5199, -0.3294] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_baseline | -0.1348 | 1.0000e-04 | ✅ Yes | [-0.2301, -0.0395] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.1332 | 1.0000e-04 | ✅ Yes | [-0.2285, -0.0379] |
| gemma4:latest_baseline vs gemma4:latest_kb_rag | 0.0280 | 1.0000e+00 | ❌ No | [-0.0672, 0.1233] |
| gemma4:latest_baseline vs gpt-oss:20b_baseline | 0.0008 | 1.0000e+00 | ❌ No | [-0.0944, 0.0961] |
| gemma4:latest_baseline vs gpt-oss:20b_kb_rag | 0.0187 | 1.0000e+00 | ❌ No | [-0.0766, 0.1139] |
| gemma4:latest_baseline vs llama3.1:8b_baseline | -0.0545 | 9.0640e-01 | ❌ No | [-0.1498, 0.0407] |
| gemma4:latest_baseline vs llama3.1:8b_kb_rag | -0.0424 | 9.9380e-01 | ❌ No | [-0.1377, 0.0529] |
| gemma4:latest_baseline vs llama3.2:latest_baseline | -0.1287 | 3.0000e-04 | ✅ Yes | [-0.2239, -0.0334] |
| gemma4:latest_baseline vs llama3.2:latest_kb_rag | -0.0594 | 8.1440e-01 | ❌ No | [-0.1547, 0.0359] |
| gemma4:latest_baseline vs mistral-nemo:latest_baseline | -0.1478 | 0.0000e+00 | ✅ Yes | [-0.2430, -0.0525] |
| gemma4:latest_baseline vs mistral-nemo:latest_kb_rag | -0.1791 | 0.0000e+00 | ✅ Yes | [-0.2743, -0.0838] |
| gemma4:latest_baseline vs nemotron-mini:4b_baseline | -0.4786 | 0.0000e+00 | ✅ Yes | [-0.5738, -0.3833] |
| gemma4:latest_baseline vs nemotron-mini:4b_kb_rag | -0.3536 | 0.0000e+00 | ✅ Yes | [-0.4489, -0.2583] |
| gemma4:latest_baseline vs qwen3:8b_baseline | -0.0637 | 7.0360e-01 | ❌ No | [-0.1590, 0.0315] |
| gemma4:latest_baseline vs qwen3:8b_kb_rag | -0.0621 | 7.4700e-01 | ❌ No | [-0.1574, 0.0331] |
| gemma4:latest_kb_rag vs gpt-oss:20b_baseline | -0.0272 | 1.0000e+00 | ❌ No | [-0.1225, 0.0681] |
| gemma4:latest_kb_rag vs gpt-oss:20b_kb_rag | -0.0094 | 1.0000e+00 | ❌ No | [-0.1046, 0.0859] |
| gemma4:latest_kb_rag vs llama3.1:8b_baseline | -0.0826 | 1.9990e-01 | ❌ No | [-0.1778, 0.0127] |
| gemma4:latest_kb_rag vs llama3.1:8b_kb_rag | -0.0704 | 5.0580e-01 | ❌ No | [-0.1657, 0.0248] |
| gemma4:latest_kb_rag vs llama3.2:latest_baseline | -0.1567 | 0.0000e+00 | ✅ Yes | [-0.2520, -0.0614] |
| gemma4:latest_kb_rag vs llama3.2:latest_kb_rag | -0.0874 | 1.2320e-01 | ❌ No | [-0.1827, 0.0078] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_baseline | -0.1758 | 0.0000e+00 | ✅ Yes | [-0.2711, -0.0805] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.2071 | 0.0000e+00 | ✅ Yes | [-0.3024, -0.1118] |
| gemma4:latest_kb_rag vs nemotron-mini:4b_baseline | -0.5066 | 0.0000e+00 | ✅ Yes | [-0.6019, -0.4113] |
| gemma4:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.3816 | 0.0000e+00 | ✅ Yes | [-0.4769, -0.2864] |
| gemma4:latest_kb_rag vs qwen3:8b_baseline | -0.0918 | 7.6100e-02 | ❌ No | [-0.1870, 0.0035] |
| gemma4:latest_kb_rag vs qwen3:8b_kb_rag | -0.0902 | 9.1400e-02 | ❌ No | [-0.1854, 0.0051] |
| gpt-oss:20b_baseline vs gpt-oss:20b_kb_rag | 0.0178 | 1.0000e+00 | ❌ No | [-0.0775, 0.1131] |
| gpt-oss:20b_baseline vs llama3.1:8b_baseline | -0.0554 | 8.9300e-01 | ❌ No | [-0.1507, 0.0399] |
| gpt-oss:20b_baseline vs llama3.1:8b_kb_rag | -0.0433 | 9.9210e-01 | ❌ No | [-0.1385, 0.0520] |
| gpt-oss:20b_baseline vs llama3.2:latest_baseline | -0.1295 | 2.0000e-04 | ✅ Yes | [-0.2248, -0.0342] |
| gpt-oss:20b_baseline vs llama3.2:latest_kb_rag | -0.0602 | 7.9470e-01 | ❌ No | [-0.1555, 0.0350] |
| gpt-oss:20b_baseline vs mistral-nemo:latest_baseline | -0.1486 | 0.0000e+00 | ✅ Yes | [-0.2439, -0.0533] |
| gpt-oss:20b_baseline vs mistral-nemo:latest_kb_rag | -0.1799 | 0.0000e+00 | ✅ Yes | [-0.2752, -0.0846] |
| gpt-oss:20b_baseline vs nemotron-mini:4b_baseline | -0.4794 | 0.0000e+00 | ✅ Yes | [-0.5747, -0.3841] |
| gpt-oss:20b_baseline vs nemotron-mini:4b_kb_rag | -0.3545 | 0.0000e+00 | ✅ Yes | [-0.4497, -0.2592] |
| gpt-oss:20b_baseline vs qwen3:8b_baseline | -0.0646 | 6.7970e-01 | ❌ No | [-0.1599, 0.0307] |
| gpt-oss:20b_baseline vs qwen3:8b_kb_rag | -0.0630 | 7.2440e-01 | ❌ No | [-0.1583, 0.0323] |
| gpt-oss:20b_kb_rag vs llama3.1:8b_baseline | -0.0732 | 4.2500e-01 | ❌ No | [-0.1685, 0.0221] |
| gpt-oss:20b_kb_rag vs llama3.1:8b_kb_rag | -0.0611 | 7.7460e-01 | ❌ No | [-0.1563, 0.0342] |
| gpt-oss:20b_kb_rag vs llama3.2:latest_baseline | -0.1473 | 0.0000e+00 | ✅ Yes | [-0.2426, -0.0521] |
| gpt-oss:20b_kb_rag vs llama3.2:latest_kb_rag | -0.0781 | 2.9630e-01 | ❌ No | [-0.1733, 0.0172] |
| gpt-oss:20b_kb_rag vs mistral-nemo:latest_baseline | -0.1664 | 0.0000e+00 | ✅ Yes | [-0.2617, -0.0711] |
| gpt-oss:20b_kb_rag vs mistral-nemo:latest_kb_rag | -0.1977 | 0.0000e+00 | ✅ Yes | [-0.2930, -0.1024] |
| gpt-oss:20b_kb_rag vs nemotron-mini:4b_baseline | -0.4972 | 0.0000e+00 | ✅ Yes | [-0.5925, -0.4019] |
| gpt-oss:20b_kb_rag vs nemotron-mini:4b_kb_rag | -0.3723 | 0.0000e+00 | ✅ Yes | [-0.4675, -0.2770] |
| gpt-oss:20b_kb_rag vs qwen3:8b_baseline | -0.0824 | 2.0300e-01 | ❌ No | [-0.1777, 0.0129] |
| gpt-oss:20b_kb_rag vs qwen3:8b_kb_rag | -0.0808 | 2.3470e-01 | ❌ No | [-0.1761, 0.0145] |
| llama3.1:8b_baseline vs llama3.1:8b_kb_rag | 0.0121 | 1.0000e+00 | ❌ No | [-0.0831, 0.1074] |
| llama3.1:8b_baseline vs llama3.2:latest_baseline | -0.0741 | 3.9830e-01 | ❌ No | [-0.1694, 0.0211] |
| llama3.1:8b_baseline vs llama3.2:latest_kb_rag | -0.0049 | 1.0000e+00 | ❌ No | [-0.1001, 0.0904] |
| llama3.1:8b_baseline vs mistral-nemo:latest_baseline | -0.0932 | 6.4100e-02 | ❌ No | [-0.1885, 0.0020] |
| llama3.1:8b_baseline vs mistral-nemo:latest_kb_rag | -0.1245 | 6.0000e-04 | ✅ Yes | [-0.2198, -0.0293] |
| llama3.1:8b_baseline vs nemotron-mini:4b_baseline | -0.4240 | 0.0000e+00 | ✅ Yes | [-0.5193, -0.3288] |
| llama3.1:8b_baseline vs nemotron-mini:4b_kb_rag | -0.2991 | 0.0000e+00 | ✅ Yes | [-0.3943, -0.2038] |
| llama3.1:8b_baseline vs qwen3:8b_baseline | -0.0092 | 1.0000e+00 | ❌ No | [-0.1045, 0.0861] |
| llama3.1:8b_baseline vs qwen3:8b_kb_rag | -0.0076 | 1.0000e+00 | ❌ No | [-0.1029, 0.0877] |
| llama3.1:8b_kb_rag vs llama3.2:latest_baseline | -0.0863 | 1.3910e-01 | ❌ No | [-0.1815, 0.0090] |
| llama3.1:8b_kb_rag vs llama3.2:latest_kb_rag | -0.0170 | 1.0000e+00 | ❌ No | [-0.1123, 0.0783] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_baseline | -0.1054 | 1.2900e-02 | ✅ Yes | [-0.2006, -0.0101] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_kb_rag | -0.1367 | 1.0000e-04 | ✅ Yes | [-0.2319, -0.0414] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_baseline | -0.4361 | 0.0000e+00 | ✅ Yes | [-0.5314, -0.3409] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_kb_rag | -0.3112 | 0.0000e+00 | ✅ Yes | [-0.4065, -0.2159] |
| llama3.1:8b_kb_rag vs qwen3:8b_baseline | -0.0213 | 1.0000e+00 | ❌ No | [-0.1166, 0.0739] |
| llama3.1:8b_kb_rag vs qwen3:8b_kb_rag | -0.0197 | 1.0000e+00 | ❌ No | [-0.1150, 0.0755] |
| llama3.2:latest_baseline vs llama3.2:latest_kb_rag | 0.0693 | 5.4060e-01 | ❌ No | [-0.0260, 0.1645] |
| llama3.2:latest_baseline vs mistral-nemo:latest_baseline | -0.0191 | 1.0000e+00 | ❌ No | [-0.1144, 0.0762] |
| llama3.2:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0504 | 9.5550e-01 | ❌ No | [-0.1457, 0.0449] |
| llama3.2:latest_baseline vs nemotron-mini:4b_baseline | -0.3499 | 0.0000e+00 | ✅ Yes | [-0.4452, -0.2546] |
| llama3.2:latest_baseline vs nemotron-mini:4b_kb_rag | -0.2249 | 0.0000e+00 | ✅ Yes | [-0.3202, -0.1297] |
| llama3.2:latest_baseline vs qwen3:8b_baseline | 0.0649 | 6.7000e-01 | ❌ No | [-0.0303, 0.1602] |
| llama3.2:latest_baseline vs qwen3:8b_kb_rag | 0.0665 | 6.2310e-01 | ❌ No | [-0.0287, 0.1618] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_baseline | -0.0884 | 1.1150e-01 | ❌ No | [-0.1836, 0.0069] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.1197 | 1.3000e-03 | ✅ Yes | [-0.2149, -0.0244] |
| llama3.2:latest_kb_rag vs nemotron-mini:4b_baseline | -0.4192 | 0.0000e+00 | ✅ Yes | [-0.5144, -0.3239] |
| llama3.2:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.2942 | 0.0000e+00 | ✅ Yes | [-0.3895, -0.1989] |
| llama3.2:latest_kb_rag vs qwen3:8b_baseline | -0.0043 | 1.0000e+00 | ❌ No | [-0.0996, 0.0909] |
| llama3.2:latest_kb_rag vs qwen3:8b_kb_rag | -0.0027 | 1.0000e+00 | ❌ No | [-0.0980, 0.0925] |
| mistral-nemo:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0313 | 9.9990e-01 | ❌ No | [-0.1266, 0.0640] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_baseline | -0.3308 | 0.0000e+00 | ✅ Yes | [-0.4261, -0.2355] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_kb_rag | -0.2058 | 0.0000e+00 | ✅ Yes | [-0.3011, -0.1106] |
| mistral-nemo:latest_baseline vs qwen3:8b_baseline | 0.0840 | 1.7410e-01 | ❌ No | [-0.0113, 0.1793] |
| mistral-nemo:latest_baseline vs qwen3:8b_kb_rag | 0.0856 | 1.4850e-01 | ❌ No | [-0.0097, 0.1809] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_baseline | -0.2995 | 0.0000e+00 | ✅ Yes | [-0.3948, -0.2042] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.1745 | 0.0000e+00 | ✅ Yes | [-0.2698, -0.0793] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_baseline | 0.1153 | 2.8000e-03 | ✅ Yes | [0.0200, 0.2106] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_kb_rag | 0.1169 | 2.1000e-03 | ✅ Yes | [0.0217, 0.2122] |
| nemotron-mini:4b_baseline vs nemotron-mini:4b_kb_rag | 0.1250 | 5.0000e-04 | ✅ Yes | [0.0297, 0.2202] |
| nemotron-mini:4b_baseline vs qwen3:8b_baseline | 0.4148 | 0.0000e+00 | ✅ Yes | [0.3195, 0.5101] |
| nemotron-mini:4b_baseline vs qwen3:8b_kb_rag | 0.4164 | 0.0000e+00 | ✅ Yes | [0.3211, 0.5117] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_baseline | 0.2899 | 0.0000e+00 | ✅ Yes | [0.1946, 0.3851] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_kb_rag | 0.2915 | 0.0000e+00 | ✅ Yes | [0.1962, 0.3867] |
| qwen3:8b_baseline vs qwen3:8b_kb_rag | 0.0016 | 1.0000e+00 | ❌ No | [-0.0937, 0.0969] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 7 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline | 0.2811 | 0.2872 | +0.0061 | 📈 Improved |
| deepseek-r1:1.5b_kb_rag | 0.3196 | 0.3163 | -0.0032 | 📉 Decreased |
| gemma4:12b-mlx_baseline | 0.7813 | 0.7837 | +0.0024 | 📈 Improved |
| gemma4:12b-mlx_kb_rag | 0.7982 | 0.8003 | +0.0022 | 📈 Improved |
| gemma4:31b-cloud_baseline | 0.4859 | 0.4950 | +0.0090 | 📈 Improved |
| gemma4:31b-cloud_kb_rag | 0.5860 | 0.5870 | +0.0010 | 📈 Improved |
| gemma4:31b-mlx_baseline | 0.8157 | 0.8179 | +0.0022 | 📈 Improved |
| gemma4:31b-mlx_kb_rag | 0.8252 | 0.8271 | +0.0019 | 📈 Improved |
| gemma4:latest_baseline | 0.7541 | 0.7539 | -0.0003 | 📉 Decreased |
| gemma4:latest_kb_rag | 0.7822 | 0.7813 | -0.0009 | 📉 Decreased |
| gpt-oss:20b_baseline | 0.7550 | 0.7553 | +0.0003 | 📈 Improved |
| gpt-oss:20b_kb_rag | 0.7728 | 0.7733 | +0.0006 | 📈 Improved |
| llama3.1:8b_baseline | 0.6996 | 0.7006 | +0.0010 | 📈 Improved |
| llama3.1:8b_kb_rag | 0.7117 | 0.7120 | +0.0002 | 📈 Improved |
| llama3.2:latest_baseline | 0.6255 | 0.6234 | -0.0021 | 📉 Decreased |
| llama3.2:latest_kb_rag | 0.6947 | 0.6944 | -0.0003 | 📉 Decreased |
| mistral-nemo:latest_baseline | 0.6064 | 0.6066 | +0.0002 | 📈 Improved |
| mistral-nemo:latest_kb_rag | 0.5751 | 0.5724 | -0.0026 | 📉 Decreased |
| nemotron-mini:4b_baseline | 0.2756 | 0.2699 | -0.0057 | 📉 Decreased |
| nemotron-mini:4b_kb_rag | 0.4005 | 0.4021 | +0.0016 | 📈 Improved |
| qwen3:8b_baseline | 0.6904 | 0.6928 | +0.0024 | 📈 Improved |
| qwen3:8b_kb_rag | 0.6920 | 0.6923 | +0.0003 | 📈 Improved |