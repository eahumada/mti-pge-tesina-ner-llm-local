# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 38.3239
- **p-Value:** 1.0726e-185

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline | 120 | 0.1395 | 0.0860 | 0.1929 | 0.2958 |
| gemma4:31b-cloud_rag_enhanced | 120 | 0.1852 | 0.1258 | 0.2446 | 0.3286 |
| minimax-m3:cloud_baseline | 120 | 0.0837 | 0.0408 | 0.1266 | 0.2373 |
| minimax-m3:cloud_rag_enhanced | 120 | 0.0883 | 0.0439 | 0.1327 | 0.2458 |
| gemma4:31b-mlx_baseline | 120 | 0.5983 | 0.5645 | 0.6321 | 0.1869 |
| gemma4:31b-mlx_rag_enhanced | 120 | 0.5868 | 0.5503 | 0.6234 | 0.2021 |
| gemma4:latest_baseline | 120 | 0.5446 | 0.5072 | 0.5819 | 0.2066 |
| gemma4:latest_rag_enhanced | 120 | 0.5257 | 0.4862 | 0.5652 | 0.2187 |
| gemma:latest_baseline | 120 | 0.4734 | 0.4310 | 0.5157 | 0.2345 |
| gemma:latest_rag_enhanced | 120 | 0.4259 | 0.3812 | 0.4705 | 0.2470 |
| qwen3:8b_baseline | 120 | 0.4483 | 0.4035 | 0.4930 | 0.2475 |
| qwen3:8b_rag_enhanced | 120 | 0.4484 | 0.4052 | 0.4916 | 0.2390 |
| qwen2.5:14b_baseline | 120 | 0.5189 | 0.4849 | 0.5528 | 0.1879 |
| qwen2.5:14b_rag_enhanced | 120 | 0.5071 | 0.4714 | 0.5429 | 0.1976 |
| mistral-nemo:latest_baseline | 120 | 0.4505 | 0.4122 | 0.4889 | 0.2122 |
| mistral-nemo:latest_rag_enhanced | 120 | 0.3935 | 0.3417 | 0.4454 | 0.2868 |
| nuextract:latest_baseline | 120 | 0.4455 | 0.4095 | 0.4815 | 0.1990 |
| nuextract:latest_rag_enhanced | 120 | 0.5085 | 0.4394 | 0.5776 | 0.3822 |
| llama3.1:8b_baseline | 120 | 0.4959 | 0.4625 | 0.5294 | 0.1852 |
| llama3.1:8b_rag_enhanced | 120 | 0.4623 | 0.4256 | 0.4990 | 0.2031 |
| llama3.2:latest_baseline | 120 | 0.3945 | 0.3534 | 0.4355 | 0.2269 |
| llama3.2:latest_rag_enhanced | 120 | 0.4196 | 0.3674 | 0.4719 | 0.2892 |
| nemotron-mini:4b_baseline | 120 | 0.3650 | 0.3085 | 0.4214 | 0.3123 |
| nemotron-mini:4b_rag_enhanced | 120 | 0.4704 | 0.4057 | 0.5352 | 0.3583 |
| deepseek-r1:1.5b_baseline | 120 | 0.3400 | 0.2923 | 0.3877 | 0.2637 |
| deepseek-r1:1.5b_rag_enhanced | 120 | 0.3516 | 0.2904 | 0.4127 | 0.3381 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline vs deepseek-r1:1.5b_rag_enhanced | 0.0116 | 1.0000e+00 | ❌ No | [-0.1129, 0.1360] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_baseline | -0.2005 | 0.0000e+00 | ✅ Yes | [-0.3250, -0.0761] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_rag_enhanced | -0.1548 | 1.2000e-03 | ✅ Yes | [-0.2792, -0.0303] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_baseline | 0.2583 | 0.0000e+00 | ✅ Yes | [0.1339, 0.3827] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_rag_enhanced | 0.2468 | 0.0000e+00 | ✅ Yes | [0.1224, 0.3712] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_baseline | 0.2046 | 0.0000e+00 | ✅ Yes | [0.0802, 0.3290] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_rag_enhanced | 0.1857 | 0.0000e+00 | ✅ Yes | [0.0613, 0.3101] |
| deepseek-r1:1.5b_baseline vs gemma:latest_baseline | 0.1334 | 1.8900e-02 | ✅ Yes | [0.0089, 0.2578] |
| deepseek-r1:1.5b_baseline vs gemma:latest_rag_enhanced | 0.0859 | 7.1600e-01 | ❌ No | [-0.0385, 0.2103] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_baseline | 0.1559 | 1.0000e-03 | ✅ Yes | [0.0315, 0.2804] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_rag_enhanced | 0.1223 | 6.2100e-02 | ❌ No | [-0.0022, 0.2467] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_baseline | 0.0544 | 9.9900e-01 | ❌ No | [-0.0700, 0.1789] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_rag_enhanced | 0.0796 | 8.4300e-01 | ❌ No | [-0.0448, 0.2040] |
| deepseek-r1:1.5b_baseline vs minimax-m3:cloud_baseline | -0.2563 | 0.0000e+00 | ✅ Yes | [-0.3807, -0.1319] |
| deepseek-r1:1.5b_baseline vs minimax-m3:cloud_rag_enhanced | -0.2517 | 0.0000e+00 | ✅ Yes | [-0.3761, -0.1273] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_baseline | 0.1105 | 1.7830e-01 | ❌ No | [-0.0139, 0.2349] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_rag_enhanced | 0.0535 | 9.9920e-01 | ❌ No | [-0.0709, 0.1780] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_baseline | 0.0250 | 1.0000e+00 | ❌ No | [-0.0994, 0.1494] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_rag_enhanced | 0.1304 | 2.6300e-02 | ✅ Yes | [0.0060, 0.2549] |
| deepseek-r1:1.5b_baseline vs nuextract:latest_baseline | 0.1055 | 2.6060e-01 | ❌ No | [-0.0189, 0.2299] |
| deepseek-r1:1.5b_baseline vs nuextract:latest_rag_enhanced | 0.1685 | 2.0000e-04 | ✅ Yes | [0.0440, 0.2929] |
| deepseek-r1:1.5b_baseline vs qwen2.5:14b_baseline | 0.1789 | 0.0000e+00 | ✅ Yes | [0.0544, 0.3033] |
| deepseek-r1:1.5b_baseline vs qwen2.5:14b_rag_enhanced | 0.1671 | 2.0000e-04 | ✅ Yes | [0.0427, 0.2916] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_baseline | 0.1083 | 2.1250e-01 | ❌ No | [-0.0162, 0.2327] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_rag_enhanced | 0.1084 | 2.1080e-01 | ❌ No | [-0.0161, 0.2328] |
| deepseek-r1:1.5b_rag_enhanced vs gemma4:31b-cloud_baseline | -0.2121 | 0.0000e+00 | ✅ Yes | [-0.3365, -0.0877] |
| deepseek-r1:1.5b_rag_enhanced vs gemma4:31b-cloud_rag_enhanced | -0.1663 | 2.0000e-04 | ✅ Yes | [-0.2907, -0.0419] |
| deepseek-r1:1.5b_rag_enhanced vs gemma4:31b-mlx_baseline | 0.2467 | 0.0000e+00 | ✅ Yes | [0.1223, 0.3711] |
| deepseek-r1:1.5b_rag_enhanced vs gemma4:31b-mlx_rag_enhanced | 0.2353 | 0.0000e+00 | ✅ Yes | [0.1108, 0.3597] |
| deepseek-r1:1.5b_rag_enhanced vs gemma4:latest_baseline | 0.1930 | 0.0000e+00 | ✅ Yes | [0.0686, 0.3174] |
| deepseek-r1:1.5b_rag_enhanced vs gemma4:latest_rag_enhanced | 0.1742 | 1.0000e-04 | ✅ Yes | [0.0497, 0.2986] |
| deepseek-r1:1.5b_rag_enhanced vs gemma:latest_baseline | 0.1218 | 6.5000e-02 | ❌ No | [-0.0026, 0.2462] |
| deepseek-r1:1.5b_rag_enhanced vs gemma:latest_rag_enhanced | 0.0743 | 9.1890e-01 | ❌ No | [-0.0501, 0.1987] |
| deepseek-r1:1.5b_rag_enhanced vs llama3.1:8b_baseline | 0.1444 | 5.0000e-03 | ✅ Yes | [0.0200, 0.2688] |
| deepseek-r1:1.5b_rag_enhanced vs llama3.1:8b_rag_enhanced | 0.1107 | 1.7550e-01 | ❌ No | [-0.0137, 0.2351] |
| deepseek-r1:1.5b_rag_enhanced vs llama3.2:latest_baseline | 0.0429 | 1.0000e+00 | ❌ No | [-0.0815, 0.1673] |
| deepseek-r1:1.5b_rag_enhanced vs llama3.2:latest_rag_enhanced | 0.0681 | 9.7050e-01 | ❌ No | [-0.0564, 0.1925] |
| deepseek-r1:1.5b_rag_enhanced vs minimax-m3:cloud_baseline | -0.2678 | 0.0000e+00 | ✅ Yes | [-0.3923, -0.1434] |
| deepseek-r1:1.5b_rag_enhanced vs minimax-m3:cloud_rag_enhanced | -0.2633 | 0.0000e+00 | ✅ Yes | [-0.3877, -0.1388] |
| deepseek-r1:1.5b_rag_enhanced vs mistral-nemo:latest_baseline | 0.0990 | 3.9710e-01 | ❌ No | [-0.0255, 0.2234] |
| deepseek-r1:1.5b_rag_enhanced vs mistral-nemo:latest_rag_enhanced | 0.0420 | 1.0000e+00 | ❌ No | [-0.0824, 0.1664] |
| deepseek-r1:1.5b_rag_enhanced vs nemotron-mini:4b_baseline | 0.0134 | 1.0000e+00 | ❌ No | [-0.1110, 0.1378] |
| deepseek-r1:1.5b_rag_enhanced vs nemotron-mini:4b_rag_enhanced | 0.1189 | 8.6100e-02 | ❌ No | [-0.0055, 0.2433] |
| deepseek-r1:1.5b_rag_enhanced vs nuextract:latest_baseline | 0.0939 | 5.1910e-01 | ❌ No | [-0.0305, 0.2183] |
| deepseek-r1:1.5b_rag_enhanced vs nuextract:latest_rag_enhanced | 0.1569 | 9.0000e-04 | ✅ Yes | [0.0325, 0.2813] |
| deepseek-r1:1.5b_rag_enhanced vs qwen2.5:14b_baseline | 0.1673 | 2.0000e-04 | ✅ Yes | [0.0429, 0.2917] |
| deepseek-r1:1.5b_rag_enhanced vs qwen2.5:14b_rag_enhanced | 0.1556 | 1.1000e-03 | ✅ Yes | [0.0312, 0.2800] |
| deepseek-r1:1.5b_rag_enhanced vs qwen3:8b_baseline | 0.0967 | 4.5050e-01 | ❌ No | [-0.0277, 0.2211] |
| deepseek-r1:1.5b_rag_enhanced vs qwen3:8b_rag_enhanced | 0.0968 | 4.4790e-01 | ❌ No | [-0.0276, 0.2212] |
| gemma4:31b-cloud_baseline vs gemma4:31b-cloud_rag_enhanced | 0.0458 | 1.0000e+00 | ❌ No | [-0.0786, 0.1702] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_baseline | 0.4588 | 0.0000e+00 | ✅ Yes | [0.3344, 0.5832] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_rag_enhanced | 0.4474 | 0.0000e+00 | ✅ Yes | [0.3229, 0.5718] |
| gemma4:31b-cloud_baseline vs gemma4:latest_baseline | 0.4051 | 0.0000e+00 | ✅ Yes | [0.2807, 0.5295] |
| gemma4:31b-cloud_baseline vs gemma4:latest_rag_enhanced | 0.3862 | 0.0000e+00 | ✅ Yes | [0.2618, 0.5107] |
| gemma4:31b-cloud_baseline vs gemma:latest_baseline | 0.3339 | 0.0000e+00 | ✅ Yes | [0.2095, 0.4583] |
| gemma4:31b-cloud_baseline vs gemma:latest_rag_enhanced | 0.2864 | 0.0000e+00 | ✅ Yes | [0.1620, 0.4108] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_baseline | 0.3565 | 0.0000e+00 | ✅ Yes | [0.2320, 0.4809] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_rag_enhanced | 0.3228 | 0.0000e+00 | ✅ Yes | [0.1984, 0.4472] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_baseline | 0.2550 | 0.0000e+00 | ✅ Yes | [0.1306, 0.3794] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_rag_enhanced | 0.2802 | 0.0000e+00 | ✅ Yes | [0.1557, 0.4046] |
| gemma4:31b-cloud_baseline vs minimax-m3:cloud_baseline | -0.0557 | 9.9850e-01 | ❌ No | [-0.1802, 0.0687] |
| gemma4:31b-cloud_baseline vs minimax-m3:cloud_rag_enhanced | -0.0512 | 9.9970e-01 | ❌ No | [-0.1756, 0.0732] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_baseline | 0.3110 | 0.0000e+00 | ✅ Yes | [0.1866, 0.4355] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_rag_enhanced | 0.2541 | 0.0000e+00 | ✅ Yes | [0.1297, 0.3785] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_baseline | 0.2255 | 0.0000e+00 | ✅ Yes | [0.1011, 0.3499] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_rag_enhanced | 0.3310 | 0.0000e+00 | ✅ Yes | [0.2066, 0.4554] |
| gemma4:31b-cloud_baseline vs nuextract:latest_baseline | 0.3060 | 0.0000e+00 | ✅ Yes | [0.1816, 0.4304] |
| gemma4:31b-cloud_baseline vs nuextract:latest_rag_enhanced | 0.3690 | 0.0000e+00 | ✅ Yes | [0.2446, 0.4934] |
| gemma4:31b-cloud_baseline vs qwen2.5:14b_baseline | 0.3794 | 0.0000e+00 | ✅ Yes | [0.2550, 0.5038] |
| gemma4:31b-cloud_baseline vs qwen2.5:14b_rag_enhanced | 0.3677 | 0.0000e+00 | ✅ Yes | [0.2432, 0.4921] |
| gemma4:31b-cloud_baseline vs qwen3:8b_baseline | 0.3088 | 0.0000e+00 | ✅ Yes | [0.1844, 0.4332] |
| gemma4:31b-cloud_baseline vs qwen3:8b_rag_enhanced | 0.3089 | 0.0000e+00 | ✅ Yes | [0.1845, 0.4333] |
| gemma4:31b-cloud_rag_enhanced vs gemma4:31b-mlx_baseline | 0.4130 | 0.0000e+00 | ✅ Yes | [0.2886, 0.5375] |
| gemma4:31b-cloud_rag_enhanced vs gemma4:31b-mlx_rag_enhanced | 0.4016 | 0.0000e+00 | ✅ Yes | [0.2772, 0.5260] |
| gemma4:31b-cloud_rag_enhanced vs gemma4:latest_baseline | 0.3593 | 0.0000e+00 | ✅ Yes | [0.2349, 0.4838] |
| gemma4:31b-cloud_rag_enhanced vs gemma4:latest_rag_enhanced | 0.3405 | 0.0000e+00 | ✅ Yes | [0.2160, 0.4649] |
| gemma4:31b-cloud_rag_enhanced vs gemma:latest_baseline | 0.2881 | 0.0000e+00 | ✅ Yes | [0.1637, 0.4125] |
| gemma4:31b-cloud_rag_enhanced vs gemma:latest_rag_enhanced | 0.2406 | 0.0000e+00 | ✅ Yes | [0.1162, 0.3651] |
| gemma4:31b-cloud_rag_enhanced vs llama3.1:8b_baseline | 0.3107 | 0.0000e+00 | ✅ Yes | [0.1863, 0.4351] |
| gemma4:31b-cloud_rag_enhanced vs llama3.1:8b_rag_enhanced | 0.2770 | 0.0000e+00 | ✅ Yes | [0.1526, 0.4014] |
| gemma4:31b-cloud_rag_enhanced vs llama3.2:latest_baseline | 0.2092 | 0.0000e+00 | ✅ Yes | [0.0848, 0.3336] |
| gemma4:31b-cloud_rag_enhanced vs llama3.2:latest_rag_enhanced | 0.2344 | 0.0000e+00 | ✅ Yes | [0.1100, 0.3588] |
| gemma4:31b-cloud_rag_enhanced vs minimax-m3:cloud_baseline | -0.1015 | 3.3990e-01 | ❌ No | [-0.2259, 0.0229] |
| gemma4:31b-cloud_rag_enhanced vs minimax-m3:cloud_rag_enhanced | -0.0969 | 4.4460e-01 | ❌ No | [-0.2214, 0.0275] |
| gemma4:31b-cloud_rag_enhanced vs mistral-nemo:latest_baseline | 0.2653 | 0.0000e+00 | ✅ Yes | [0.1409, 0.3897] |
| gemma4:31b-cloud_rag_enhanced vs mistral-nemo:latest_rag_enhanced | 0.2083 | 0.0000e+00 | ✅ Yes | [0.0839, 0.3327] |
| gemma4:31b-cloud_rag_enhanced vs nemotron-mini:4b_baseline | 0.1797 | 0.0000e+00 | ✅ Yes | [0.0553, 0.3042] |
| gemma4:31b-cloud_rag_enhanced vs nemotron-mini:4b_rag_enhanced | 0.2852 | 0.0000e+00 | ✅ Yes | [0.1608, 0.4096] |
| gemma4:31b-cloud_rag_enhanced vs nuextract:latest_baseline | 0.2602 | 0.0000e+00 | ✅ Yes | [0.1358, 0.3847] |
| gemma4:31b-cloud_rag_enhanced vs nuextract:latest_rag_enhanced | 0.3232 | 0.0000e+00 | ✅ Yes | [0.1988, 0.4476] |
| gemma4:31b-cloud_rag_enhanced vs qwen2.5:14b_baseline | 0.3336 | 0.0000e+00 | ✅ Yes | [0.2092, 0.4580] |
| gemma4:31b-cloud_rag_enhanced vs qwen2.5:14b_rag_enhanced | 0.3219 | 0.0000e+00 | ✅ Yes | [0.1975, 0.4463] |
| gemma4:31b-cloud_rag_enhanced vs qwen3:8b_baseline | 0.2630 | 0.0000e+00 | ✅ Yes | [0.1386, 0.3874] |
| gemma4:31b-cloud_rag_enhanced vs qwen3:8b_rag_enhanced | 0.2631 | 0.0000e+00 | ✅ Yes | [0.1387, 0.3875] |
| gemma4:31b-mlx_baseline vs gemma4:31b-mlx_rag_enhanced | -0.0115 | 1.0000e+00 | ❌ No | [-0.1359, 0.1130] |
| gemma4:31b-mlx_baseline vs gemma4:latest_baseline | -0.0537 | 9.9920e-01 | ❌ No | [-0.1781, 0.0707] |
| gemma4:31b-mlx_baseline vs gemma4:latest_rag_enhanced | -0.0726 | 9.3720e-01 | ❌ No | [-0.1970, 0.0518] |
| gemma4:31b-mlx_baseline vs gemma:latest_baseline | -0.1249 | 4.7500e-02 | ✅ Yes | [-0.2493, -0.0005] |
| gemma4:31b-mlx_baseline vs gemma:latest_rag_enhanced | -0.1724 | 1.0000e-04 | ✅ Yes | [-0.2968, -0.0480] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_baseline | -0.1024 | 3.2220e-01 | ❌ No | [-0.2268, 0.0221] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_rag_enhanced | -0.1360 | 1.3900e-02 | ✅ Yes | [-0.2604, -0.0116] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_baseline | -0.2038 | 0.0000e+00 | ✅ Yes | [-0.3283, -0.0794] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_rag_enhanced | -0.1787 | 0.0000e+00 | ✅ Yes | [-0.3031, -0.0542] |
| gemma4:31b-mlx_baseline vs minimax-m3:cloud_baseline | -0.5146 | 0.0000e+00 | ✅ Yes | [-0.6390, -0.3901] |
| gemma4:31b-mlx_baseline vs minimax-m3:cloud_rag_enhanced | -0.5100 | 0.0000e+00 | ✅ Yes | [-0.6344, -0.3856] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_baseline | -0.1478 | 3.2000e-03 | ✅ Yes | [-0.2722, -0.0233] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_rag_enhanced | -0.2047 | 0.0000e+00 | ✅ Yes | [-0.3292, -0.0803] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_baseline | -0.2333 | 0.0000e+00 | ✅ Yes | [-0.3577, -0.1089] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_rag_enhanced | -0.1278 | 3.4900e-02 | ✅ Yes | [-0.2523, -0.0034] |
| gemma4:31b-mlx_baseline vs nuextract:latest_baseline | -0.1528 | 1.6000e-03 | ✅ Yes | [-0.2772, -0.0284] |
| gemma4:31b-mlx_baseline vs nuextract:latest_rag_enhanced | -0.0898 | 6.2190e-01 | ❌ No | [-0.2142, 0.0346] |
| gemma4:31b-mlx_baseline vs qwen2.5:14b_baseline | -0.0794 | 8.4650e-01 | ❌ No | [-0.2038, 0.0450] |
| gemma4:31b-mlx_baseline vs qwen2.5:14b_rag_enhanced | -0.0912 | 5.8850e-01 | ❌ No | [-0.2156, 0.0333] |
| gemma4:31b-mlx_baseline vs qwen3:8b_baseline | -0.1500 | 2.4000e-03 | ✅ Yes | [-0.2744, -0.0256] |
| gemma4:31b-mlx_baseline vs qwen3:8b_rag_enhanced | -0.1499 | 2.4000e-03 | ✅ Yes | [-0.2743, -0.0255] |
| gemma4:31b-mlx_rag_enhanced vs gemma4:latest_baseline | -0.0422 | 1.0000e+00 | ❌ No | [-0.1667, 0.0822] |
| gemma4:31b-mlx_rag_enhanced vs gemma4:latest_rag_enhanced | -0.0611 | 9.9330e-01 | ❌ No | [-0.1855, 0.0633] |
| gemma4:31b-mlx_rag_enhanced vs gemma:latest_baseline | -0.1135 | 1.3980e-01 | ❌ No | [-0.2379, 0.0110] |
| gemma4:31b-mlx_rag_enhanced vs gemma:latest_rag_enhanced | -0.1609 | 5.0000e-04 | ✅ Yes | [-0.2854, -0.0365] |
| gemma4:31b-mlx_rag_enhanced vs llama3.1:8b_baseline | -0.0909 | 5.9510e-01 | ❌ No | [-0.2153, 0.0335] |
| gemma4:31b-mlx_rag_enhanced vs llama3.1:8b_rag_enhanced | -0.1246 | 4.9300e-02 | ✅ Yes | [-0.2490, -0.0001] |
| gemma4:31b-mlx_rag_enhanced vs llama3.2:latest_baseline | -0.1924 | 0.0000e+00 | ✅ Yes | [-0.3168, -0.0680] |
| gemma4:31b-mlx_rag_enhanced vs llama3.2:latest_rag_enhanced | -0.1672 | 2.0000e-04 | ✅ Yes | [-0.2916, -0.0428] |
| gemma4:31b-mlx_rag_enhanced vs minimax-m3:cloud_baseline | -0.5031 | 0.0000e+00 | ✅ Yes | [-0.6275, -0.3787] |
| gemma4:31b-mlx_rag_enhanced vs minimax-m3:cloud_rag_enhanced | -0.4985 | 0.0000e+00 | ✅ Yes | [-0.6229, -0.3741] |
| gemma4:31b-mlx_rag_enhanced vs mistral-nemo:latest_baseline | -0.1363 | 1.3400e-02 | ✅ Yes | [-0.2607, -0.0119] |
| gemma4:31b-mlx_rag_enhanced vs mistral-nemo:latest_rag_enhanced | -0.1933 | 0.0000e+00 | ✅ Yes | [-0.3177, -0.0689] |
| gemma4:31b-mlx_rag_enhanced vs nemotron-mini:4b_baseline | -0.2218 | 0.0000e+00 | ✅ Yes | [-0.3463, -0.0974] |
| gemma4:31b-mlx_rag_enhanced vs nemotron-mini:4b_rag_enhanced | -0.1164 | 1.0830e-01 | ❌ No | [-0.2408, 0.0080] |
| gemma4:31b-mlx_rag_enhanced vs nuextract:latest_baseline | -0.1413 | 7.3000e-03 | ✅ Yes | [-0.2658, -0.0169] |
| gemma4:31b-mlx_rag_enhanced vs nuextract:latest_rag_enhanced | -0.0784 | 8.6410e-01 | ❌ No | [-0.2028, 0.0461] |
| gemma4:31b-mlx_rag_enhanced vs qwen2.5:14b_baseline | -0.0680 | 9.7110e-01 | ❌ No | [-0.1924, 0.0565] |
| gemma4:31b-mlx_rag_enhanced vs qwen2.5:14b_rag_enhanced | -0.0797 | 8.4190e-01 | ❌ No | [-0.2041, 0.0447] |
| gemma4:31b-mlx_rag_enhanced vs qwen3:8b_baseline | -0.1386 | 1.0200e-02 | ✅ Yes | [-0.2630, -0.0141] |
| gemma4:31b-mlx_rag_enhanced vs qwen3:8b_rag_enhanced | -0.1385 | 1.0400e-02 | ✅ Yes | [-0.2629, -0.0140] |
| gemma4:latest_baseline vs gemma4:latest_rag_enhanced | -0.0189 | 1.0000e+00 | ❌ No | [-0.1433, 0.1055] |
| gemma4:latest_baseline vs gemma:latest_baseline | -0.0712 | 9.4920e-01 | ❌ No | [-0.1956, 0.0532] |
| gemma4:latest_baseline vs gemma:latest_rag_enhanced | -0.1187 | 8.7600e-02 | ❌ No | [-0.2431, 0.0057] |
| gemma4:latest_baseline vs llama3.1:8b_baseline | -0.0487 | 9.9990e-01 | ❌ No | [-0.1731, 0.0758] |
| gemma4:latest_baseline vs llama3.1:8b_rag_enhanced | -0.0823 | 7.9280e-01 | ❌ No | [-0.2067, 0.0421] |
| gemma4:latest_baseline vs llama3.2:latest_baseline | -0.1501 | 2.3000e-03 | ✅ Yes | [-0.2746, -0.0257] |
| gemma4:latest_baseline vs llama3.2:latest_rag_enhanced | -0.1250 | 4.7300e-02 | ✅ Yes | [-0.2494, -0.0005] |
| gemma4:latest_baseline vs minimax-m3:cloud_baseline | -0.4609 | 0.0000e+00 | ✅ Yes | [-0.5853, -0.3364] |
| gemma4:latest_baseline vs minimax-m3:cloud_rag_enhanced | -0.4563 | 0.0000e+00 | ✅ Yes | [-0.5807, -0.3319] |
| gemma4:latest_baseline vs mistral-nemo:latest_baseline | -0.0941 | 5.1540e-01 | ❌ No | [-0.2185, 0.0304] |
| gemma4:latest_baseline vs mistral-nemo:latest_rag_enhanced | -0.1510 | 2.1000e-03 | ✅ Yes | [-0.2755, -0.0266] |
| gemma4:latest_baseline vs nemotron-mini:4b_baseline | -0.1796 | 0.0000e+00 | ✅ Yes | [-0.3040, -0.0552] |
| gemma4:latest_baseline vs nemotron-mini:4b_rag_enhanced | -0.0741 | 9.2090e-01 | ❌ No | [-0.1986, 0.0503] |
| gemma4:latest_baseline vs nuextract:latest_baseline | -0.0991 | 3.9370e-01 | ❌ No | [-0.2235, 0.0253] |
| gemma4:latest_baseline vs nuextract:latest_rag_enhanced | -0.0361 | 1.0000e+00 | ❌ No | [-0.1605, 0.0883] |
| gemma4:latest_baseline vs qwen2.5:14b_baseline | -0.0257 | 1.0000e+00 | ❌ No | [-0.1501, 0.0987] |
| gemma4:latest_baseline vs qwen2.5:14b_rag_enhanced | -0.0375 | 1.0000e+00 | ❌ No | [-0.1619, 0.0870] |
| gemma4:latest_baseline vs qwen3:8b_baseline | -0.0963 | 4.5980e-01 | ❌ No | [-0.2207, 0.0281] |
| gemma4:latest_baseline vs qwen3:8b_rag_enhanced | -0.0962 | 4.6240e-01 | ❌ No | [-0.2206, 0.0282] |
| gemma4:latest_rag_enhanced vs gemma:latest_baseline | -0.0523 | 9.9950e-01 | ❌ No | [-0.1768, 0.0721] |
| gemma4:latest_rag_enhanced vs gemma:latest_rag_enhanced | -0.0998 | 3.7720e-01 | ❌ No | [-0.2242, 0.0246] |
| gemma4:latest_rag_enhanced vs llama3.1:8b_baseline | -0.0298 | 1.0000e+00 | ❌ No | [-0.1542, 0.0946] |
| gemma4:latest_rag_enhanced vs llama3.1:8b_rag_enhanced | -0.0634 | 9.8850e-01 | ❌ No | [-0.1879, 0.0610] |
| gemma4:latest_rag_enhanced vs llama3.2:latest_baseline | -0.1313 | 2.4000e-02 | ✅ Yes | [-0.2557, -0.0068] |
| gemma4:latest_rag_enhanced vs llama3.2:latest_rag_enhanced | -0.1061 | 2.4960e-01 | ❌ No | [-0.2305, 0.0183] |
| gemma4:latest_rag_enhanced vs minimax-m3:cloud_baseline | -0.4420 | 0.0000e+00 | ✅ Yes | [-0.5664, -0.3176] |
| gemma4:latest_rag_enhanced vs minimax-m3:cloud_rag_enhanced | -0.4374 | 0.0000e+00 | ✅ Yes | [-0.5618, -0.3130] |
| gemma4:latest_rag_enhanced vs mistral-nemo:latest_baseline | -0.0752 | 9.0860e-01 | ❌ No | [-0.1996, 0.0492] |
| gemma4:latest_rag_enhanced vs mistral-nemo:latest_rag_enhanced | -0.1322 | 2.1700e-02 | ✅ Yes | [-0.2566, -0.0078] |
| gemma4:latest_rag_enhanced vs nemotron-mini:4b_baseline | -0.1607 | 5.0000e-04 | ✅ Yes | [-0.2851, -0.0363] |
| gemma4:latest_rag_enhanced vs nemotron-mini:4b_rag_enhanced | -0.0553 | 9.9870e-01 | ❌ No | [-0.1797, 0.0691] |
| gemma4:latest_rag_enhanced vs nuextract:latest_baseline | -0.0802 | 8.3240e-01 | ❌ No | [-0.2047, 0.0442] |
| gemma4:latest_rag_enhanced vs nuextract:latest_rag_enhanced | -0.0172 | 1.0000e+00 | ❌ No | [-0.1417, 0.1072] |
| gemma4:latest_rag_enhanced vs qwen2.5:14b_baseline | -0.0068 | 1.0000e+00 | ❌ No | [-0.1313, 0.1176] |
| gemma4:latest_rag_enhanced vs qwen2.5:14b_rag_enhanced | -0.0186 | 1.0000e+00 | ❌ No | [-0.1430, 0.1058] |
| gemma4:latest_rag_enhanced vs qwen3:8b_baseline | -0.0774 | 8.7800e-01 | ❌ No | [-0.2019, 0.0470] |
| gemma4:latest_rag_enhanced vs qwen3:8b_rag_enhanced | -0.0773 | 8.7950e-01 | ❌ No | [-0.2018, 0.0471] |
| gemma:latest_baseline vs gemma:latest_rag_enhanced | -0.0475 | 9.9990e-01 | ❌ No | [-0.1719, 0.0769] |
| gemma:latest_baseline vs llama3.1:8b_baseline | 0.0226 | 1.0000e+00 | ❌ No | [-0.1018, 0.1470] |
| gemma:latest_baseline vs llama3.1:8b_rag_enhanced | -0.0111 | 1.0000e+00 | ❌ No | [-0.1355, 0.1133] |
| gemma:latest_baseline vs llama3.2:latest_baseline | -0.0789 | 8.5500e-01 | ❌ No | [-0.2033, 0.0455] |
| gemma:latest_baseline vs llama3.2:latest_rag_enhanced | -0.0537 | 9.9920e-01 | ❌ No | [-0.1782, 0.0707] |
| gemma:latest_baseline vs minimax-m3:cloud_baseline | -0.3896 | 0.0000e+00 | ✅ Yes | [-0.5141, -0.2652] |
| gemma:latest_baseline vs minimax-m3:cloud_rag_enhanced | -0.3851 | 0.0000e+00 | ✅ Yes | [-0.5095, -0.2606] |
| gemma:latest_baseline vs mistral-nemo:latest_baseline | -0.0228 | 1.0000e+00 | ❌ No | [-0.1473, 0.1016] |
| gemma:latest_baseline vs mistral-nemo:latest_rag_enhanced | -0.0798 | 8.3960e-01 | ❌ No | [-0.2042, 0.0446] |
| gemma:latest_baseline vs nemotron-mini:4b_baseline | -0.1084 | 2.1060e-01 | ❌ No | [-0.2328, 0.0160] |
| gemma:latest_baseline vs nemotron-mini:4b_rag_enhanced | -0.0029 | 1.0000e+00 | ❌ No | [-0.1273, 0.1215] |
| gemma:latest_baseline vs nuextract:latest_baseline | -0.0279 | 1.0000e+00 | ❌ No | [-0.1523, 0.0965] |
| gemma:latest_baseline vs nuextract:latest_rag_enhanced | 0.0351 | 1.0000e+00 | ❌ No | [-0.0893, 0.1595] |
| gemma:latest_baseline vs qwen2.5:14b_baseline | 0.0455 | 1.0000e+00 | ❌ No | [-0.0789, 0.1699] |
| gemma:latest_baseline vs qwen2.5:14b_rag_enhanced | 0.0338 | 1.0000e+00 | ❌ No | [-0.0906, 0.1582] |
| gemma:latest_baseline vs qwen3:8b_baseline | -0.0251 | 1.0000e+00 | ❌ No | [-0.1495, 0.0993] |
| gemma:latest_baseline vs qwen3:8b_rag_enhanced | -0.0250 | 1.0000e+00 | ❌ No | [-0.1494, 0.0994] |
| gemma:latest_rag_enhanced vs llama3.1:8b_baseline | 0.0700 | 9.5810e-01 | ❌ No | [-0.0544, 0.1945] |
| gemma:latest_rag_enhanced vs llama3.1:8b_rag_enhanced | 0.0364 | 1.0000e+00 | ❌ No | [-0.0880, 0.1608] |
| gemma:latest_rag_enhanced vs llama3.2:latest_baseline | -0.0314 | 1.0000e+00 | ❌ No | [-0.1559, 0.0930] |
| gemma:latest_rag_enhanced vs llama3.2:latest_rag_enhanced | -0.0063 | 1.0000e+00 | ❌ No | [-0.1307, 0.1182] |
| gemma:latest_rag_enhanced vs minimax-m3:cloud_baseline | -0.3422 | 0.0000e+00 | ✅ Yes | [-0.4666, -0.2177] |
| gemma:latest_rag_enhanced vs minimax-m3:cloud_rag_enhanced | -0.3376 | 0.0000e+00 | ✅ Yes | [-0.4620, -0.2132] |
| gemma:latest_rag_enhanced vs mistral-nemo:latest_baseline | 0.0246 | 1.0000e+00 | ❌ No | [-0.0998, 0.1490] |
| gemma:latest_rag_enhanced vs mistral-nemo:latest_rag_enhanced | -0.0323 | 1.0000e+00 | ❌ No | [-0.1568, 0.0921] |
| gemma:latest_rag_enhanced vs nemotron-mini:4b_baseline | -0.0609 | 9.9360e-01 | ❌ No | [-0.1853, 0.0635] |
| gemma:latest_rag_enhanced vs nemotron-mini:4b_rag_enhanced | 0.0446 | 1.0000e+00 | ❌ No | [-0.0799, 0.1690] |
| gemma:latest_rag_enhanced vs nuextract:latest_baseline | 0.0196 | 1.0000e+00 | ❌ No | [-0.1048, 0.1440] |
| gemma:latest_rag_enhanced vs nuextract:latest_rag_enhanced | 0.0826 | 7.8740e-01 | ❌ No | [-0.0418, 0.2070] |
| gemma:latest_rag_enhanced vs qwen2.5:14b_baseline | 0.0930 | 5.4270e-01 | ❌ No | [-0.0314, 0.2174] |
| gemma:latest_rag_enhanced vs qwen2.5:14b_rag_enhanced | 0.0812 | 8.1360e-01 | ❌ No | [-0.0432, 0.2057] |
| gemma:latest_rag_enhanced vs qwen3:8b_baseline | 0.0224 | 1.0000e+00 | ❌ No | [-0.1020, 0.1468] |
| gemma:latest_rag_enhanced vs qwen3:8b_rag_enhanced | 0.0225 | 1.0000e+00 | ❌ No | [-0.1019, 0.1469] |
| llama3.1:8b_baseline vs llama3.1:8b_rag_enhanced | -0.0337 | 1.0000e+00 | ❌ No | [-0.1581, 0.0908] |
| llama3.1:8b_baseline vs llama3.2:latest_baseline | -0.1015 | 3.4070e-01 | ❌ No | [-0.2259, 0.0229] |
| llama3.1:8b_baseline vs llama3.2:latest_rag_enhanced | -0.0763 | 8.9420e-01 | ❌ No | [-0.2007, 0.0481] |
| llama3.1:8b_baseline vs minimax-m3:cloud_baseline | -0.4122 | 0.0000e+00 | ✅ Yes | [-0.5366, -0.2878] |
| llama3.1:8b_baseline vs minimax-m3:cloud_rag_enhanced | -0.4076 | 0.0000e+00 | ✅ Yes | [-0.5321, -0.2832] |
| llama3.1:8b_baseline vs mistral-nemo:latest_baseline | -0.0454 | 1.0000e+00 | ❌ No | [-0.1698, 0.0790] |
| llama3.1:8b_baseline vs mistral-nemo:latest_rag_enhanced | -0.1024 | 3.2130e-01 | ❌ No | [-0.2268, 0.0220] |
| llama3.1:8b_baseline vs nemotron-mini:4b_baseline | -0.1309 | 2.4900e-02 | ✅ Yes | [-0.2554, -0.0065] |
| llama3.1:8b_baseline vs nemotron-mini:4b_rag_enhanced | -0.0255 | 1.0000e+00 | ❌ No | [-0.1499, 0.0989] |
| llama3.1:8b_baseline vs nuextract:latest_baseline | -0.0505 | 9.9970e-01 | ❌ No | [-0.1749, 0.0740] |
| llama3.1:8b_baseline vs nuextract:latest_rag_enhanced | 0.0125 | 1.0000e+00 | ❌ No | [-0.1119, 0.1370] |
| llama3.1:8b_baseline vs qwen2.5:14b_baseline | 0.0229 | 1.0000e+00 | ❌ No | [-0.1015, 0.1474] |
| llama3.1:8b_baseline vs qwen2.5:14b_rag_enhanced | 0.0112 | 1.0000e+00 | ❌ No | [-0.1132, 0.1356] |
| llama3.1:8b_baseline vs qwen3:8b_baseline | -0.0477 | 9.9990e-01 | ❌ No | [-0.1721, 0.0767] |
| llama3.1:8b_baseline vs qwen3:8b_rag_enhanced | -0.0476 | 9.9990e-01 | ❌ No | [-0.1720, 0.0769] |
| llama3.1:8b_rag_enhanced vs llama3.2:latest_baseline | -0.0678 | 9.7180e-01 | ❌ No | [-0.1922, 0.0566] |
| llama3.1:8b_rag_enhanced vs llama3.2:latest_rag_enhanced | -0.0426 | 1.0000e+00 | ❌ No | [-0.1671, 0.0818] |
| llama3.1:8b_rag_enhanced vs minimax-m3:cloud_baseline | -0.3785 | 0.0000e+00 | ✅ Yes | [-0.5030, -0.2541] |
| llama3.1:8b_rag_enhanced vs minimax-m3:cloud_rag_enhanced | -0.3740 | 0.0000e+00 | ✅ Yes | [-0.4984, -0.2496] |
| llama3.1:8b_rag_enhanced vs mistral-nemo:latest_baseline | -0.0118 | 1.0000e+00 | ❌ No | [-0.1362, 0.1127] |
| llama3.1:8b_rag_enhanced vs mistral-nemo:latest_rag_enhanced | -0.0687 | 9.6670e-01 | ❌ No | [-0.1931, 0.0557] |
| llama3.1:8b_rag_enhanced vs nemotron-mini:4b_baseline | -0.0973 | 4.3660e-01 | ❌ No | [-0.2217, 0.0271] |
| llama3.1:8b_rag_enhanced vs nemotron-mini:4b_rag_enhanced | 0.0082 | 1.0000e+00 | ❌ No | [-0.1163, 0.1326] |
| llama3.1:8b_rag_enhanced vs nuextract:latest_baseline | -0.0168 | 1.0000e+00 | ❌ No | [-0.1412, 0.1076] |
| llama3.1:8b_rag_enhanced vs nuextract:latest_rag_enhanced | 0.0462 | 1.0000e+00 | ❌ No | [-0.0782, 0.1706] |
| llama3.1:8b_rag_enhanced vs qwen2.5:14b_baseline | 0.0566 | 9.9800e-01 | ❌ No | [-0.0678, 0.1810] |
| llama3.1:8b_rag_enhanced vs qwen2.5:14b_rag_enhanced | 0.0449 | 1.0000e+00 | ❌ No | [-0.0796, 0.1693] |
| llama3.1:8b_rag_enhanced vs qwen3:8b_baseline | -0.0140 | 1.0000e+00 | ❌ No | [-0.1384, 0.1104] |
| llama3.1:8b_rag_enhanced vs qwen3:8b_rag_enhanced | -0.0139 | 1.0000e+00 | ❌ No | [-0.1383, 0.1105] |
| llama3.2:latest_baseline vs llama3.2:latest_rag_enhanced | 0.0252 | 1.0000e+00 | ❌ No | [-0.0992, 0.1496] |
| llama3.2:latest_baseline vs minimax-m3:cloud_baseline | -0.3107 | 0.0000e+00 | ✅ Yes | [-0.4351, -0.1863] |
| llama3.2:latest_baseline vs minimax-m3:cloud_rag_enhanced | -0.3062 | 0.0000e+00 | ✅ Yes | [-0.4306, -0.1817] |
| llama3.2:latest_baseline vs mistral-nemo:latest_baseline | 0.0561 | 9.9830e-01 | ❌ No | [-0.0684, 0.1805] |
| llama3.2:latest_baseline vs mistral-nemo:latest_rag_enhanced | -0.0009 | 1.0000e+00 | ❌ No | [-0.1253, 0.1235] |
| llama3.2:latest_baseline vs nemotron-mini:4b_baseline | -0.0295 | 1.0000e+00 | ❌ No | [-0.1539, 0.0950] |
| llama3.2:latest_baseline vs nemotron-mini:4b_rag_enhanced | 0.0760 | 8.9850e-01 | ❌ No | [-0.0484, 0.2004] |
| llama3.2:latest_baseline vs nuextract:latest_baseline | 0.0510 | 9.9970e-01 | ❌ No | [-0.0734, 0.1754] |
| llama3.2:latest_baseline vs nuextract:latest_rag_enhanced | 0.1140 | 1.3330e-01 | ❌ No | [-0.0104, 0.2384] |
| llama3.2:latest_baseline vs qwen2.5:14b_baseline | 0.1244 | 5.0000e-02 | ❌ No | [-0.0000, 0.2488] |
| llama3.2:latest_baseline vs qwen2.5:14b_rag_enhanced | 0.1127 | 1.4930e-01 | ❌ No | [-0.0117, 0.2371] |
| llama3.2:latest_baseline vs qwen3:8b_baseline | 0.0538 | 9.9920e-01 | ❌ No | [-0.0706, 0.1782] |
| llama3.2:latest_baseline vs qwen3:8b_rag_enhanced | 0.0539 | 9.9910e-01 | ❌ No | [-0.0705, 0.1783] |
| llama3.2:latest_rag_enhanced vs minimax-m3:cloud_baseline | -0.3359 | 0.0000e+00 | ✅ Yes | [-0.4603, -0.2115] |
| llama3.2:latest_rag_enhanced vs minimax-m3:cloud_rag_enhanced | -0.3313 | 0.0000e+00 | ✅ Yes | [-0.4558, -0.2069] |
| llama3.2:latest_rag_enhanced vs mistral-nemo:latest_baseline | 0.0309 | 1.0000e+00 | ❌ No | [-0.0935, 0.1553] |
| llama3.2:latest_rag_enhanced vs mistral-nemo:latest_rag_enhanced | -0.0261 | 1.0000e+00 | ❌ No | [-0.1505, 0.0983] |
| llama3.2:latest_rag_enhanced vs nemotron-mini:4b_baseline | -0.0546 | 9.9890e-01 | ❌ No | [-0.1791, 0.0698] |
| llama3.2:latest_rag_enhanced vs nemotron-mini:4b_rag_enhanced | 0.0508 | 9.9970e-01 | ❌ No | [-0.0736, 0.1752] |
| llama3.2:latest_rag_enhanced vs nuextract:latest_baseline | 0.0259 | 1.0000e+00 | ❌ No | [-0.0986, 0.1503] |
| llama3.2:latest_rag_enhanced vs nuextract:latest_rag_enhanced | 0.0888 | 6.4570e-01 | ❌ No | [-0.0356, 0.2133] |
| llama3.2:latest_rag_enhanced vs qwen2.5:14b_baseline | 0.0992 | 3.9060e-01 | ❌ No | [-0.0252, 0.2237] |
| llama3.2:latest_rag_enhanced vs qwen2.5:14b_rag_enhanced | 0.0875 | 6.7800e-01 | ❌ No | [-0.0369, 0.2119] |
| llama3.2:latest_rag_enhanced vs qwen3:8b_baseline | 0.0286 | 1.0000e+00 | ❌ No | [-0.0958, 0.1531] |
| llama3.2:latest_rag_enhanced vs qwen3:8b_rag_enhanced | 0.0287 | 1.0000e+00 | ❌ No | [-0.0957, 0.1532] |
| minimax-m3:cloud_baseline vs minimax-m3:cloud_rag_enhanced | 0.0046 | 1.0000e+00 | ❌ No | [-0.1198, 0.1290] |
| minimax-m3:cloud_baseline vs mistral-nemo:latest_baseline | 0.3668 | 0.0000e+00 | ✅ Yes | [0.2424, 0.4912] |
| minimax-m3:cloud_baseline vs mistral-nemo:latest_rag_enhanced | 0.3098 | 0.0000e+00 | ✅ Yes | [0.1854, 0.4342] |
| minimax-m3:cloud_baseline vs nemotron-mini:4b_baseline | 0.2813 | 0.0000e+00 | ✅ Yes | [0.1568, 0.4057] |
| minimax-m3:cloud_baseline vs nemotron-mini:4b_rag_enhanced | 0.3867 | 0.0000e+00 | ✅ Yes | [0.2623, 0.5111] |
| minimax-m3:cloud_baseline vs nuextract:latest_baseline | 0.3618 | 0.0000e+00 | ✅ Yes | [0.2373, 0.4862] |
| minimax-m3:cloud_baseline vs nuextract:latest_rag_enhanced | 0.4247 | 0.0000e+00 | ✅ Yes | [0.3003, 0.5492] |
| minimax-m3:cloud_baseline vs qwen2.5:14b_baseline | 0.4351 | 0.0000e+00 | ✅ Yes | [0.3107, 0.5596] |
| minimax-m3:cloud_baseline vs qwen2.5:14b_rag_enhanced | 0.4234 | 0.0000e+00 | ✅ Yes | [0.2990, 0.5478] |
| minimax-m3:cloud_baseline vs qwen3:8b_baseline | 0.3645 | 0.0000e+00 | ✅ Yes | [0.2401, 0.4890] |
| minimax-m3:cloud_baseline vs qwen3:8b_rag_enhanced | 0.3646 | 0.0000e+00 | ✅ Yes | [0.2402, 0.4891] |
| minimax-m3:cloud_rag_enhanced vs mistral-nemo:latest_baseline | 0.3622 | 0.0000e+00 | ✅ Yes | [0.2378, 0.4866] |
| minimax-m3:cloud_rag_enhanced vs mistral-nemo:latest_rag_enhanced | 0.3052 | 0.0000e+00 | ✅ Yes | [0.1808, 0.4297] |
| minimax-m3:cloud_rag_enhanced vs nemotron-mini:4b_baseline | 0.2767 | 0.0000e+00 | ✅ Yes | [0.1523, 0.4011] |
| minimax-m3:cloud_rag_enhanced vs nemotron-mini:4b_rag_enhanced | 0.3821 | 0.0000e+00 | ✅ Yes | [0.2577, 0.5066] |
| minimax-m3:cloud_rag_enhanced vs nuextract:latest_baseline | 0.3572 | 0.0000e+00 | ✅ Yes | [0.2328, 0.4816] |
| minimax-m3:cloud_rag_enhanced vs nuextract:latest_rag_enhanced | 0.4202 | 0.0000e+00 | ✅ Yes | [0.2958, 0.5446] |
| minimax-m3:cloud_rag_enhanced vs qwen2.5:14b_baseline | 0.4306 | 0.0000e+00 | ✅ Yes | [0.3061, 0.5550] |
| minimax-m3:cloud_rag_enhanced vs qwen2.5:14b_rag_enhanced | 0.4188 | 0.0000e+00 | ✅ Yes | [0.2944, 0.5433] |
| minimax-m3:cloud_rag_enhanced vs qwen3:8b_baseline | 0.3600 | 0.0000e+00 | ✅ Yes | [0.2355, 0.4844] |
| minimax-m3:cloud_rag_enhanced vs qwen3:8b_rag_enhanced | 0.3601 | 0.0000e+00 | ✅ Yes | [0.2357, 0.4845] |
| mistral-nemo:latest_baseline vs mistral-nemo:latest_rag_enhanced | -0.0570 | 9.9780e-01 | ❌ No | [-0.1814, 0.0674] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_baseline | -0.0855 | 7.2400e-01 | ❌ No | [-0.2100, 0.0389] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_rag_enhanced | 0.0199 | 1.0000e+00 | ❌ No | [-0.1045, 0.1443] |
| mistral-nemo:latest_baseline vs nuextract:latest_baseline | -0.0050 | 1.0000e+00 | ❌ No | [-0.1295, 0.1194] |
| mistral-nemo:latest_baseline vs nuextract:latest_rag_enhanced | 0.0580 | 9.9710e-01 | ❌ No | [-0.0665, 0.1824] |
| mistral-nemo:latest_baseline vs qwen2.5:14b_baseline | 0.0683 | 9.6890e-01 | ❌ No | [-0.0561, 0.1928] |
| mistral-nemo:latest_baseline vs qwen2.5:14b_rag_enhanced | 0.0566 | 9.9800e-01 | ❌ No | [-0.0678, 0.1810] |
| mistral-nemo:latest_baseline vs qwen3:8b_baseline | -0.0023 | 1.0000e+00 | ❌ No | [-0.1267, 0.1222] |
| mistral-nemo:latest_baseline vs qwen3:8b_rag_enhanced | -0.0021 | 1.0000e+00 | ❌ No | [-0.1266, 0.1223] |
| mistral-nemo:latest_rag_enhanced vs nemotron-mini:4b_baseline | -0.0286 | 1.0000e+00 | ❌ No | [-0.1530, 0.0959] |
| mistral-nemo:latest_rag_enhanced vs nemotron-mini:4b_rag_enhanced | 0.0769 | 8.8600e-01 | ❌ No | [-0.0475, 0.2013] |
| mistral-nemo:latest_rag_enhanced vs nuextract:latest_baseline | 0.0519 | 9.9960e-01 | ❌ No | [-0.0725, 0.1764] |
| mistral-nemo:latest_rag_enhanced vs nuextract:latest_rag_enhanced | 0.1149 | 1.2320e-01 | ❌ No | [-0.0095, 0.2394] |
| mistral-nemo:latest_rag_enhanced vs qwen2.5:14b_baseline | 0.1253 | 4.5600e-02 | ✅ Yes | [0.0009, 0.2497] |
| mistral-nemo:latest_rag_enhanced vs qwen2.5:14b_rag_enhanced | 0.1136 | 1.3820e-01 | ❌ No | [-0.0108, 0.2380] |
| mistral-nemo:latest_rag_enhanced vs qwen3:8b_baseline | 0.0547 | 9.9890e-01 | ❌ No | [-0.0697, 0.1791] |
| mistral-nemo:latest_rag_enhanced vs qwen3:8b_rag_enhanced | 0.0548 | 9.9880e-01 | ❌ No | [-0.0696, 0.1792] |
| nemotron-mini:4b_baseline vs nemotron-mini:4b_rag_enhanced | 0.1055 | 2.6110e-01 | ❌ No | [-0.0190, 0.2299] |
| nemotron-mini:4b_baseline vs nuextract:latest_baseline | 0.0805 | 8.2760e-01 | ❌ No | [-0.0439, 0.2049] |
| nemotron-mini:4b_baseline vs nuextract:latest_rag_enhanced | 0.1435 | 5.6000e-03 | ✅ Yes | [0.0191, 0.2679] |
| nemotron-mini:4b_baseline vs qwen2.5:14b_baseline | 0.1539 | 1.4000e-03 | ✅ Yes | [0.0295, 0.2783] |
| nemotron-mini:4b_baseline vs qwen2.5:14b_rag_enhanced | 0.1421 | 6.6000e-03 | ✅ Yes | [0.0177, 0.2666] |
| nemotron-mini:4b_baseline vs qwen3:8b_baseline | 0.0833 | 7.7310e-01 | ❌ No | [-0.0411, 0.2077] |
| nemotron-mini:4b_baseline vs qwen3:8b_rag_enhanced | 0.0834 | 7.7090e-01 | ❌ No | [-0.0410, 0.2078] |
| nemotron-mini:4b_rag_enhanced vs nuextract:latest_baseline | -0.0250 | 1.0000e+00 | ❌ No | [-0.1494, 0.0995] |
| nemotron-mini:4b_rag_enhanced vs nuextract:latest_rag_enhanced | 0.0380 | 1.0000e+00 | ❌ No | [-0.0864, 0.1625] |
| nemotron-mini:4b_rag_enhanced vs qwen2.5:14b_baseline | 0.0484 | 9.9990e-01 | ❌ No | [-0.0760, 0.1728] |
| nemotron-mini:4b_rag_enhanced vs qwen2.5:14b_rag_enhanced | 0.0367 | 1.0000e+00 | ❌ No | [-0.0877, 0.1611] |
| nemotron-mini:4b_rag_enhanced vs qwen3:8b_baseline | -0.0222 | 1.0000e+00 | ❌ No | [-0.1466, 0.1022] |
| nemotron-mini:4b_rag_enhanced vs qwen3:8b_rag_enhanced | -0.0221 | 1.0000e+00 | ❌ No | [-0.1465, 0.1024] |
| nuextract:latest_baseline vs nuextract:latest_rag_enhanced | 0.0630 | 9.8960e-01 | ❌ No | [-0.0614, 0.1874] |
| nuextract:latest_baseline vs qwen2.5:14b_baseline | 0.0734 | 9.2920e-01 | ❌ No | [-0.0510, 0.1978] |
| nuextract:latest_baseline vs qwen2.5:14b_rag_enhanced | 0.0617 | 9.9240e-01 | ❌ No | [-0.0628, 0.1861] |
| nuextract:latest_baseline vs qwen3:8b_baseline | 0.0028 | 1.0000e+00 | ❌ No | [-0.1216, 0.1272] |
| nuextract:latest_baseline vs qwen3:8b_rag_enhanced | 0.0029 | 1.0000e+00 | ❌ No | [-0.1215, 0.1273] |
| nuextract:latest_rag_enhanced vs qwen2.5:14b_baseline | 0.0104 | 1.0000e+00 | ❌ No | [-0.1140, 0.1348] |
| nuextract:latest_rag_enhanced vs qwen2.5:14b_rag_enhanced | -0.0013 | 1.0000e+00 | ❌ No | [-0.1258, 0.1231] |
| nuextract:latest_rag_enhanced vs qwen3:8b_baseline | -0.0602 | 9.9470e-01 | ❌ No | [-0.1846, 0.0642] |
| nuextract:latest_rag_enhanced vs qwen3:8b_rag_enhanced | -0.0601 | 9.9480e-01 | ❌ No | [-0.1845, 0.0643] |
| qwen2.5:14b_baseline vs qwen2.5:14b_rag_enhanced | -0.0117 | 1.0000e+00 | ❌ No | [-0.1362, 0.1127] |
| qwen2.5:14b_baseline vs qwen3:8b_baseline | -0.0706 | 9.5410e-01 | ❌ No | [-0.1950, 0.0538] |
| qwen2.5:14b_baseline vs qwen3:8b_rag_enhanced | -0.0705 | 9.5490e-01 | ❌ No | [-0.1949, 0.0539] |
| qwen2.5:14b_rag_enhanced vs qwen3:8b_baseline | -0.0589 | 9.9620e-01 | ❌ No | [-0.1833, 0.0655] |
| qwen2.5:14b_rag_enhanced vs qwen3:8b_rag_enhanced | -0.0588 | 9.9630e-01 | ❌ No | [-0.1832, 0.0657] |
| qwen3:8b_baseline vs qwen3:8b_rag_enhanced | 0.0001 | 1.0000e+00 | ❌ No | [-0.1243, 0.1245] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 2610.3 characters.
- **Outlier Records Identified:** 14 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline | 0.3400 | 0.3339 | -0.0061 | 📉 Decreased |
| deepseek-r1:1.5b_rag_enhanced | 0.3516 | 0.3495 | -0.0021 | 📉 Decreased |
| gemma4:31b-cloud_baseline | 0.1395 | 0.1500 | +0.0106 | 📈 Improved |
| gemma4:31b-cloud_rag_enhanced | 0.1852 | 0.1908 | +0.0055 | 📈 Improved |
| gemma4:31b-mlx_baseline | 0.5983 | 0.5873 | -0.0110 | 📉 Decreased |
| gemma4:31b-mlx_rag_enhanced | 0.5868 | 0.5712 | -0.0156 | 📉 Decreased |
| gemma4:latest_baseline | 0.5446 | 0.5370 | -0.0076 | 📉 Decreased |
| gemma4:latest_rag_enhanced | 0.5257 | 0.5267 | +0.0010 | 📈 Improved |
| gemma:latest_baseline | 0.4734 | 0.4593 | -0.0141 | 📉 Decreased |
| gemma:latest_rag_enhanced | 0.4259 | 0.4049 | -0.0209 | 📉 Decreased |
| llama3.1:8b_baseline | 0.4959 | 0.4872 | -0.0088 | 📉 Decreased |
| llama3.1:8b_rag_enhanced | 0.4623 | 0.4501 | -0.0122 | 📉 Decreased |
| llama3.2:latest_baseline | 0.3945 | 0.3718 | -0.0227 | 📉 Decreased |
| llama3.2:latest_rag_enhanced | 0.4196 | 0.4002 | -0.0195 | 📉 Decreased |
| minimax-m3:cloud_baseline | 0.0837 | 0.0840 | +0.0003 | 📈 Improved |
| minimax-m3:cloud_rag_enhanced | 0.0883 | 0.0931 | +0.0048 | 📈 Improved |
| mistral-nemo:latest_baseline | 0.4505 | 0.4349 | -0.0156 | 📉 Decreased |
| mistral-nemo:latest_rag_enhanced | 0.3935 | 0.3775 | -0.0161 | 📉 Decreased |
| nemotron-mini:4b_baseline | 0.3650 | 0.3703 | +0.0053 | 📈 Improved |
| nemotron-mini:4b_rag_enhanced | 0.4704 | 0.4874 | +0.0169 | 📈 Improved |
| nuextract:latest_baseline | 0.4455 | 0.4383 | -0.0072 | 📉 Decreased |
| nuextract:latest_rag_enhanced | 0.5085 | 0.5257 | +0.0172 | 📈 Improved |
| qwen2.5:14b_baseline | 0.5189 | 0.5062 | -0.0127 | 📉 Decreased |
| qwen2.5:14b_rag_enhanced | 0.5071 | 0.4935 | -0.0136 | 📉 Decreased |
| qwen3:8b_baseline | 0.4483 | 0.4336 | -0.0146 | 📉 Decreased |
| qwen3:8b_rag_enhanced | 0.4484 | 0.4357 | -0.0127 | 📉 Decreased |