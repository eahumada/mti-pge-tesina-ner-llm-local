# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 7.0450
- **p-Value:** 3.5080e-22

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline | 15 | 0.3973 | 0.2054 | 0.5892 | 0.3466 |
| gemma4:31b-cloud_rag_enhanced | 15 | 0.4272 | 0.2248 | 0.6296 | 0.3654 |
| minimax-m3:cloud_baseline | 15 | 0.2011 | 0.0321 | 0.3702 | 0.3052 |
| minimax-m3:cloud_rag_enhanced | 15 | 0.3718 | 0.1685 | 0.5751 | 0.3671 |
| gemma4:31b-mlx_baseline | 15 | 0.6852 | 0.6189 | 0.7515 | 0.1197 |
| gemma4:31b-mlx_rag_enhanced | 15 | 0.6897 | 0.6304 | 0.7489 | 0.1070 |
| gemma4:latest_baseline | 15 | 0.6676 | 0.5396 | 0.7955 | 0.2310 |
| gemma4:latest_rag_enhanced | 15 | 0.6048 | 0.4463 | 0.7634 | 0.2863 |
| gemma:latest_baseline | 15 | 0.6266 | 0.5156 | 0.7376 | 0.2004 |
| gemma:latest_rag_enhanced | 15 | 0.6346 | 0.5320 | 0.7371 | 0.1852 |
| qwen3:8b_baseline | 15 | 0.5365 | 0.3771 | 0.6959 | 0.2879 |
| qwen3:8b_rag_enhanced | 15 | 0.5012 | 0.3172 | 0.6851 | 0.3321 |
| qwen2.5:14b_baseline | 15 | 0.6106 | 0.5284 | 0.6928 | 0.1485 |
| qwen2.5:14b_rag_enhanced | 15 | 0.6290 | 0.5712 | 0.6867 | 0.1043 |
| mistral-nemo:latest_baseline | 15 | 0.5307 | 0.4465 | 0.6149 | 0.1521 |
| mistral-nemo:latest_rag_enhanced | 15 | 0.5586 | 0.4846 | 0.6326 | 0.1337 |
| nuextract:latest_baseline | 15 | 0.5415 | 0.4148 | 0.6682 | 0.2288 |
| nuextract:latest_rag_enhanced | 15 | 0.3596 | 0.2257 | 0.4934 | 0.2417 |
| llama3.1:8b_baseline | 15 | 0.6072 | 0.5429 | 0.6715 | 0.1161 |
| llama3.1:8b_rag_enhanced | 15 | 0.6342 | 0.5562 | 0.7121 | 0.1407 |
| llama3.2:latest_baseline | 15 | 0.6319 | 0.5246 | 0.7392 | 0.1937 |
| llama3.2:latest_rag_enhanced | 15 | 0.5758 | 0.4584 | 0.6932 | 0.2120 |
| nemotron-mini:4b_baseline | 15 | 0.4199 | 0.2919 | 0.5479 | 0.2311 |
| nemotron-mini:4b_rag_enhanced | 15 | 0.4055 | 0.2915 | 0.5196 | 0.2060 |
| deepseek-r1:1.5b_baseline | 15 | 0.3431 | 0.2239 | 0.4624 | 0.2153 |
| deepseek-r1:1.5b_rag_enhanced | 15 | 0.2749 | 0.1918 | 0.3580 | 0.1500 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline vs deepseek-r1:1.5b_rag_enhanced | -0.0682 | 1.0000e+00 | ❌ No | [-0.3853, 0.2488] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_baseline | 0.0542 | 1.0000e+00 | ❌ No | [-0.2628, 0.3712] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_rag_enhanced | 0.0841 | 1.0000e+00 | ❌ No | [-0.2330, 0.4011] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_baseline | 0.3421 | 1.7500e-02 | ✅ Yes | [0.0251, 0.6592] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_rag_enhanced | 0.3466 | 1.4400e-02 | ✅ Yes | [0.0295, 0.6636] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_baseline | 0.3245 | 3.7100e-02 | ✅ Yes | [0.0074, 0.6415] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_rag_enhanced | 0.2617 | 3.0700e-01 | ❌ No | [-0.0553, 0.5788] |
| deepseek-r1:1.5b_baseline vs gemma:latest_baseline | 0.2835 | 1.6470e-01 | ❌ No | [-0.0336, 0.6005] |
| deepseek-r1:1.5b_baseline vs gemma:latest_rag_enhanced | 0.2915 | 1.2700e-01 | ❌ No | [-0.0256, 0.6085] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_baseline | 0.2640 | 2.8890e-01 | ❌ No | [-0.0530, 0.5811] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_rag_enhanced | 0.2911 | 1.2880e-01 | ❌ No | [-0.0260, 0.6081] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_baseline | 0.2888 | 1.3880e-01 | ❌ No | [-0.0282, 0.6058] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_rag_enhanced | 0.2327 | 5.7130e-01 | ❌ No | [-0.0844, 0.5497] |
| deepseek-r1:1.5b_baseline vs minimax-m3:cloud_baseline | -0.1420 | 9.9810e-01 | ❌ No | [-0.4590, 0.1750] |
| deepseek-r1:1.5b_baseline vs minimax-m3:cloud_rag_enhanced | 0.0287 | 1.0000e+00 | ❌ No | [-0.2883, 0.3457] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_baseline | 0.1876 | 9.1910e-01 | ❌ No | [-0.1295, 0.5046] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_rag_enhanced | 0.2154 | 7.3240e-01 | ❌ No | [-0.1016, 0.5325] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_baseline | 0.0768 | 1.0000e+00 | ❌ No | [-0.2402, 0.3939] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_rag_enhanced | 0.0624 | 1.0000e+00 | ❌ No | [-0.2547, 0.3794] |
| deepseek-r1:1.5b_baseline vs nuextract:latest_baseline | 0.1984 | 8.6130e-01 | ❌ No | [-0.1186, 0.5154] |
| deepseek-r1:1.5b_baseline vs nuextract:latest_rag_enhanced | 0.0165 | 1.0000e+00 | ❌ No | [-0.3006, 0.3335] |
| deepseek-r1:1.5b_baseline vs qwen2.5:14b_baseline | 0.2675 | 2.6360e-01 | ❌ No | [-0.0496, 0.5845] |
| deepseek-r1:1.5b_baseline vs qwen2.5:14b_rag_enhanced | 0.2859 | 1.5270e-01 | ❌ No | [-0.0312, 0.6029] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_baseline | 0.1934 | 8.9050e-01 | ❌ No | [-0.1237, 0.5104] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_rag_enhanced | 0.1580 | 9.9010e-01 | ❌ No | [-0.1590, 0.4751] |
| deepseek-r1:1.5b_rag_enhanced vs gemma4:31b-cloud_baseline | 0.1224 | 9.9990e-01 | ❌ No | [-0.1946, 0.4395] |
| deepseek-r1:1.5b_rag_enhanced vs gemma4:31b-cloud_rag_enhanced | 0.1523 | 9.9420e-01 | ❌ No | [-0.1647, 0.4694] |
| deepseek-r1:1.5b_rag_enhanced vs gemma4:31b-mlx_baseline | 0.4103 | 6.0000e-04 | ✅ Yes | [0.0933, 0.7274] |
| deepseek-r1:1.5b_rag_enhanced vs gemma4:31b-mlx_rag_enhanced | 0.4148 | 4.0000e-04 | ✅ Yes | [0.0977, 0.7318] |
| deepseek-r1:1.5b_rag_enhanced vs gemma4:latest_baseline | 0.3927 | 1.5000e-03 | ✅ Yes | [0.0757, 0.7097] |
| deepseek-r1:1.5b_rag_enhanced vs gemma4:latest_rag_enhanced | 0.3299 | 2.9600e-02 | ✅ Yes | [0.0129, 0.6470] |
| deepseek-r1:1.5b_rag_enhanced vs gemma:latest_baseline | 0.3517 | 1.1400e-02 | ✅ Yes | [0.0347, 0.6687] |
| deepseek-r1:1.5b_rag_enhanced vs gemma:latest_rag_enhanced | 0.3597 | 7.8000e-03 | ✅ Yes | [0.0427, 0.6767] |
| deepseek-r1:1.5b_rag_enhanced vs llama3.1:8b_baseline | 0.3323 | 2.6800e-02 | ✅ Yes | [0.0152, 0.6493] |
| deepseek-r1:1.5b_rag_enhanced vs llama3.1:8b_rag_enhanced | 0.3593 | 8.0000e-03 | ✅ Yes | [0.0423, 0.6763] |
| deepseek-r1:1.5b_rag_enhanced vs llama3.2:latest_baseline | 0.3570 | 8.9000e-03 | ✅ Yes | [0.0400, 0.6741] |
| deepseek-r1:1.5b_rag_enhanced vs llama3.2:latest_rag_enhanced | 0.3009 | 9.1700e-02 | ❌ No | [-0.0161, 0.6179] |
| deepseek-r1:1.5b_rag_enhanced vs minimax-m3:cloud_baseline | -0.0738 | 1.0000e+00 | ❌ No | [-0.3908, 0.2433] |
| deepseek-r1:1.5b_rag_enhanced vs minimax-m3:cloud_rag_enhanced | 0.0969 | 1.0000e+00 | ❌ No | [-0.2201, 0.4140] |
| deepseek-r1:1.5b_rag_enhanced vs mistral-nemo:latest_baseline | 0.2558 | 3.5530e-01 | ❌ No | [-0.0612, 0.5729] |
| deepseek-r1:1.5b_rag_enhanced vs mistral-nemo:latest_rag_enhanced | 0.2837 | 1.6360e-01 | ❌ No | [-0.0334, 0.6007] |
| deepseek-r1:1.5b_rag_enhanced vs nemotron-mini:4b_baseline | 0.1451 | 9.9730e-01 | ❌ No | [-0.1720, 0.4621] |
| deepseek-r1:1.5b_rag_enhanced vs nemotron-mini:4b_rag_enhanced | 0.1306 | 9.9950e-01 | ❌ No | [-0.1864, 0.4477] |
| deepseek-r1:1.5b_rag_enhanced vs nuextract:latest_baseline | 0.2666 | 2.6970e-01 | ❌ No | [-0.0504, 0.5837] |
| deepseek-r1:1.5b_rag_enhanced vs nuextract:latest_rag_enhanced | 0.0847 | 1.0000e+00 | ❌ No | [-0.2324, 0.4017] |
| deepseek-r1:1.5b_rag_enhanced vs qwen2.5:14b_baseline | 0.3357 | 2.3200e-02 | ✅ Yes | [0.0187, 0.6527] |
| deepseek-r1:1.5b_rag_enhanced vs qwen2.5:14b_rag_enhanced | 0.3541 | 1.0200e-02 | ✅ Yes | [0.0370, 0.6711] |
| deepseek-r1:1.5b_rag_enhanced vs qwen3:8b_baseline | 0.2616 | 3.0770e-01 | ❌ No | [-0.0554, 0.5787] |
| deepseek-r1:1.5b_rag_enhanced vs qwen3:8b_rag_enhanced | 0.2263 | 6.3300e-01 | ❌ No | [-0.0908, 0.5433] |
| gemma4:31b-cloud_baseline vs gemma4:31b-cloud_rag_enhanced | 0.0299 | 1.0000e+00 | ❌ No | [-0.2872, 0.3469] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_baseline | 0.2879 | 1.4290e-01 | ❌ No | [-0.0291, 0.6050] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_rag_enhanced | 0.2924 | 1.2330e-01 | ❌ No | [-0.0247, 0.6094] |
| gemma4:31b-cloud_baseline vs gemma4:latest_baseline | 0.2703 | 2.4400e-01 | ❌ No | [-0.0468, 0.5873] |
| gemma4:31b-cloud_baseline vs gemma4:latest_rag_enhanced | 0.2075 | 7.9760e-01 | ❌ No | [-0.1095, 0.5246] |
| gemma4:31b-cloud_baseline vs gemma:latest_baseline | 0.2293 | 6.0420e-01 | ❌ No | [-0.0878, 0.5463] |
| gemma4:31b-cloud_baseline vs gemma:latest_rag_enhanced | 0.2373 | 5.2650e-01 | ❌ No | [-0.0798, 0.5543] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_baseline | 0.2098 | 7.7920e-01 | ❌ No | [-0.1072, 0.5269] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_rag_enhanced | 0.2369 | 5.3040e-01 | ❌ No | [-0.0802, 0.5539] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_baseline | 0.2346 | 5.5240e-01 | ❌ No | [-0.0824, 0.5516] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_rag_enhanced | 0.1785 | 9.5290e-01 | ❌ No | [-0.1386, 0.4955] |
| gemma4:31b-cloud_baseline vs minimax-m3:cloud_baseline | -0.1962 | 8.7470e-01 | ❌ No | [-0.5132, 0.1208] |
| gemma4:31b-cloud_baseline vs minimax-m3:cloud_rag_enhanced | -0.0255 | 1.0000e+00 | ❌ No | [-0.3425, 0.2915] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_baseline | 0.1334 | 9.9930e-01 | ❌ No | [-0.1837, 0.4504] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_rag_enhanced | 0.1612 | 9.8690e-01 | ❌ No | [-0.1558, 0.4783] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_baseline | 0.0226 | 1.0000e+00 | ❌ No | [-0.2944, 0.3397] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_rag_enhanced | 0.0082 | 1.0000e+00 | ❌ No | [-0.3089, 0.3252] |
| gemma4:31b-cloud_baseline vs nuextract:latest_baseline | 0.1442 | 9.9750e-01 | ❌ No | [-0.1729, 0.4612] |
| gemma4:31b-cloud_baseline vs nuextract:latest_rag_enhanced | -0.0377 | 1.0000e+00 | ❌ No | [-0.3548, 0.2793] |
| gemma4:31b-cloud_baseline vs qwen2.5:14b_baseline | 0.2133 | 7.5100e-01 | ❌ No | [-0.1038, 0.5303] |
| gemma4:31b-cloud_baseline vs qwen2.5:14b_rag_enhanced | 0.2317 | 5.8110e-01 | ❌ No | [-0.0854, 0.5487] |
| gemma4:31b-cloud_baseline vs qwen3:8b_baseline | 0.1392 | 9.9860e-01 | ❌ No | [-0.1779, 0.4562] |
| gemma4:31b-cloud_baseline vs qwen3:8b_rag_enhanced | 0.1038 | 1.0000e+00 | ❌ No | [-0.2132, 0.4209] |
| gemma4:31b-cloud_rag_enhanced vs gemma4:31b-mlx_baseline | 0.2580 | 3.3660e-01 | ❌ No | [-0.0590, 0.5751] |
| gemma4:31b-cloud_rag_enhanced vs gemma4:31b-mlx_rag_enhanced | 0.2625 | 3.0100e-01 | ❌ No | [-0.0546, 0.5795] |
| gemma4:31b-cloud_rag_enhanced vs gemma4:latest_baseline | 0.2404 | 4.9630e-01 | ❌ No | [-0.0766, 0.5574] |
| gemma4:31b-cloud_rag_enhanced vs gemma4:latest_rag_enhanced | 0.1776 | 9.5540e-01 | ❌ No | [-0.1394, 0.4947] |
| gemma4:31b-cloud_rag_enhanced vs gemma:latest_baseline | 0.1994 | 8.5500e-01 | ❌ No | [-0.1177, 0.5164] |
| gemma4:31b-cloud_rag_enhanced vs gemma:latest_rag_enhanced | 0.2074 | 7.9860e-01 | ❌ No | [-0.1097, 0.5244] |
| gemma4:31b-cloud_rag_enhanced vs llama3.1:8b_baseline | 0.1800 | 9.4820e-01 | ❌ No | [-0.1371, 0.4970] |
| gemma4:31b-cloud_rag_enhanced vs llama3.1:8b_rag_enhanced | 0.2070 | 8.0160e-01 | ❌ No | [-0.1101, 0.5240] |
| gemma4:31b-cloud_rag_enhanced vs llama3.2:latest_baseline | 0.2047 | 8.1850e-01 | ❌ No | [-0.1123, 0.5218] |
| gemma4:31b-cloud_rag_enhanced vs llama3.2:latest_rag_enhanced | 0.1486 | 9.9600e-01 | ❌ No | [-0.1685, 0.4656] |
| gemma4:31b-cloud_rag_enhanced vs minimax-m3:cloud_baseline | -0.2261 | 6.3490e-01 | ❌ No | [-0.5431, 0.0910] |
| gemma4:31b-cloud_rag_enhanced vs minimax-m3:cloud_rag_enhanced | -0.0554 | 1.0000e+00 | ❌ No | [-0.3724, 0.2617] |
| gemma4:31b-cloud_rag_enhanced vs mistral-nemo:latest_baseline | 0.1035 | 1.0000e+00 | ❌ No | [-0.2135, 0.4205] |
| gemma4:31b-cloud_rag_enhanced vs mistral-nemo:latest_rag_enhanced | 0.1314 | 9.9950e-01 | ❌ No | [-0.1857, 0.4484] |
| gemma4:31b-cloud_rag_enhanced vs nemotron-mini:4b_baseline | -0.0073 | 1.0000e+00 | ❌ No | [-0.3243, 0.3098] |
| gemma4:31b-cloud_rag_enhanced vs nemotron-mini:4b_rag_enhanced | -0.0217 | 1.0000e+00 | ❌ No | [-0.3387, 0.2953] |
| gemma4:31b-cloud_rag_enhanced vs nuextract:latest_baseline | 0.1143 | 1.0000e+00 | ❌ No | [-0.2027, 0.4314] |
| gemma4:31b-cloud_rag_enhanced vs nuextract:latest_rag_enhanced | -0.0676 | 1.0000e+00 | ❌ No | [-0.3847, 0.2494] |
| gemma4:31b-cloud_rag_enhanced vs qwen2.5:14b_baseline | 0.1834 | 9.3620e-01 | ❌ No | [-0.1336, 0.5004] |
| gemma4:31b-cloud_rag_enhanced vs qwen2.5:14b_rag_enhanced | 0.2018 | 8.3920e-01 | ❌ No | [-0.1153, 0.5188] |
| gemma4:31b-cloud_rag_enhanced vs qwen3:8b_baseline | 0.1093 | 1.0000e+00 | ❌ No | [-0.2077, 0.4263] |
| gemma4:31b-cloud_rag_enhanced vs qwen3:8b_rag_enhanced | 0.0740 | 1.0000e+00 | ❌ No | [-0.2431, 0.3910] |
| gemma4:31b-mlx_baseline vs gemma4:31b-mlx_rag_enhanced | 0.0044 | 1.0000e+00 | ❌ No | [-0.3126, 0.3215] |
| gemma4:31b-mlx_baseline vs gemma4:latest_baseline | -0.0176 | 1.0000e+00 | ❌ No | [-0.3347, 0.2994] |
| gemma4:31b-mlx_baseline vs gemma4:latest_rag_enhanced | -0.0804 | 1.0000e+00 | ❌ No | [-0.3974, 0.2366] |
| gemma4:31b-mlx_baseline vs gemma:latest_baseline | -0.0586 | 1.0000e+00 | ❌ No | [-0.3757, 0.2584] |
| gemma4:31b-mlx_baseline vs gemma:latest_rag_enhanced | -0.0507 | 1.0000e+00 | ❌ No | [-0.3677, 0.2664] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_baseline | -0.0781 | 1.0000e+00 | ❌ No | [-0.3951, 0.2390] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_rag_enhanced | -0.0511 | 1.0000e+00 | ❌ No | [-0.3681, 0.2660] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_baseline | -0.0533 | 1.0000e+00 | ❌ No | [-0.3704, 0.2637] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_rag_enhanced | -0.1095 | 1.0000e+00 | ❌ No | [-0.4265, 0.2076] |
| gemma4:31b-mlx_baseline vs minimax-m3:cloud_baseline | -0.4841 | 0.0000e+00 | ✅ Yes | [-0.8011, -0.1671] |
| gemma4:31b-mlx_baseline vs minimax-m3:cloud_rag_enhanced | -0.3134 | 5.7600e-02 | ❌ No | [-0.6305, 0.0036] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_baseline | -0.1545 | 9.9280e-01 | ❌ No | [-0.4716, 0.1625] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_rag_enhanced | -0.1267 | 9.9970e-01 | ❌ No | [-0.4437, 0.1904] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_baseline | -0.2653 | 2.7950e-01 | ❌ No | [-0.5823, 0.0517] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_rag_enhanced | -0.2797 | 1.8500e-01 | ❌ No | [-0.5968, 0.0373] |
| gemma4:31b-mlx_baseline vs nuextract:latest_baseline | -0.1437 | 9.9770e-01 | ❌ No | [-0.4608, 0.1733] |
| gemma4:31b-mlx_baseline vs nuextract:latest_rag_enhanced | -0.3257 | 3.5400e-02 | ✅ Yes | [-0.6427, -0.0086] |
| gemma4:31b-mlx_baseline vs qwen2.5:14b_baseline | -0.0746 | 1.0000e+00 | ❌ No | [-0.3917, 0.2424] |
| gemma4:31b-mlx_baseline vs qwen2.5:14b_rag_enhanced | -0.0563 | 1.0000e+00 | ❌ No | [-0.3733, 0.2608] |
| gemma4:31b-mlx_baseline vs qwen3:8b_baseline | -0.1487 | 9.9600e-01 | ❌ No | [-0.4658, 0.1683] |
| gemma4:31b-mlx_baseline vs qwen3:8b_rag_enhanced | -0.1841 | 9.3360e-01 | ❌ No | [-0.5011, 0.1330] |
| gemma4:31b-mlx_rag_enhanced vs gemma4:latest_baseline | -0.0221 | 1.0000e+00 | ❌ No | [-0.3391, 0.2950] |
| gemma4:31b-mlx_rag_enhanced vs gemma4:latest_rag_enhanced | -0.0848 | 1.0000e+00 | ❌ No | [-0.4019, 0.2322] |
| gemma4:31b-mlx_rag_enhanced vs gemma:latest_baseline | -0.0631 | 1.0000e+00 | ❌ No | [-0.3801, 0.2540] |
| gemma4:31b-mlx_rag_enhanced vs gemma:latest_rag_enhanced | -0.0551 | 1.0000e+00 | ❌ No | [-0.3721, 0.2620] |
| gemma4:31b-mlx_rag_enhanced vs llama3.1:8b_baseline | -0.0825 | 1.0000e+00 | ❌ No | [-0.3995, 0.2345] |
| gemma4:31b-mlx_rag_enhanced vs llama3.1:8b_rag_enhanced | -0.0555 | 1.0000e+00 | ❌ No | [-0.3725, 0.2616] |
| gemma4:31b-mlx_rag_enhanced vs llama3.2:latest_baseline | -0.0578 | 1.0000e+00 | ❌ No | [-0.3748, 0.2593] |
| gemma4:31b-mlx_rag_enhanced vs llama3.2:latest_rag_enhanced | -0.1139 | 1.0000e+00 | ❌ No | [-0.4309, 0.2031] |
| gemma4:31b-mlx_rag_enhanced vs minimax-m3:cloud_baseline | -0.4885 | 0.0000e+00 | ✅ Yes | [-0.8056, -0.1715] |
| gemma4:31b-mlx_rag_enhanced vs minimax-m3:cloud_rag_enhanced | -0.3179 | 4.8400e-02 | ✅ Yes | [-0.6349, -0.0008] |
| gemma4:31b-mlx_rag_enhanced vs mistral-nemo:latest_baseline | -0.1590 | 9.8930e-01 | ❌ No | [-0.4760, 0.1581] |
| gemma4:31b-mlx_rag_enhanced vs mistral-nemo:latest_rag_enhanced | -0.1311 | 9.9950e-01 | ❌ No | [-0.4481, 0.1859] |
| gemma4:31b-mlx_rag_enhanced vs nemotron-mini:4b_baseline | -0.2697 | 2.4770e-01 | ❌ No | [-0.5868, 0.0473] |
| gemma4:31b-mlx_rag_enhanced vs nemotron-mini:4b_rag_enhanced | -0.2842 | 1.6110e-01 | ❌ No | [-0.6012, 0.0329] |
| gemma4:31b-mlx_rag_enhanced vs nuextract:latest_baseline | -0.1482 | 9.9620e-01 | ❌ No | [-0.4652, 0.1689] |
| gemma4:31b-mlx_rag_enhanced vs nuextract:latest_rag_enhanced | -0.3301 | 2.9400e-02 | ✅ Yes | [-0.6471, -0.0131] |
| gemma4:31b-mlx_rag_enhanced vs qwen2.5:14b_baseline | -0.0791 | 1.0000e+00 | ❌ No | [-0.3961, 0.2380] |
| gemma4:31b-mlx_rag_enhanced vs qwen2.5:14b_rag_enhanced | -0.0607 | 1.0000e+00 | ❌ No | [-0.3777, 0.2563] |
| gemma4:31b-mlx_rag_enhanced vs qwen3:8b_baseline | -0.1532 | 9.9370e-01 | ❌ No | [-0.4702, 0.1639] |
| gemma4:31b-mlx_rag_enhanced vs qwen3:8b_rag_enhanced | -0.1885 | 9.1490e-01 | ❌ No | [-0.5056, 0.1285] |
| gemma4:latest_baseline vs gemma4:latest_rag_enhanced | -0.0628 | 1.0000e+00 | ❌ No | [-0.3798, 0.2543] |
| gemma4:latest_baseline vs gemma:latest_baseline | -0.0410 | 1.0000e+00 | ❌ No | [-0.3580, 0.2760] |
| gemma4:latest_baseline vs gemma:latest_rag_enhanced | -0.0330 | 1.0000e+00 | ❌ No | [-0.3501, 0.2840] |
| gemma4:latest_baseline vs llama3.1:8b_baseline | -0.0604 | 1.0000e+00 | ❌ No | [-0.3775, 0.2566] |
| gemma4:latest_baseline vs llama3.1:8b_rag_enhanced | -0.0334 | 1.0000e+00 | ❌ No | [-0.3505, 0.2836] |
| gemma4:latest_baseline vs llama3.2:latest_baseline | -0.0357 | 1.0000e+00 | ❌ No | [-0.3527, 0.2814] |
| gemma4:latest_baseline vs llama3.2:latest_rag_enhanced | -0.0918 | 1.0000e+00 | ❌ No | [-0.4089, 0.2252] |
| gemma4:latest_baseline vs minimax-m3:cloud_baseline | -0.4665 | 0.0000e+00 | ✅ Yes | [-0.7835, -0.1494] |
| gemma4:latest_baseline vs minimax-m3:cloud_rag_enhanced | -0.2958 | 1.0970e-01 | ❌ No | [-0.6128, 0.0213] |
| gemma4:latest_baseline vs mistral-nemo:latest_baseline | -0.1369 | 9.9900e-01 | ❌ No | [-0.4539, 0.1801] |
| gemma4:latest_baseline vs mistral-nemo:latest_rag_enhanced | -0.1090 | 1.0000e+00 | ❌ No | [-0.4261, 0.2080] |
| gemma4:latest_baseline vs nemotron-mini:4b_baseline | -0.2477 | 4.2780e-01 | ❌ No | [-0.5647, 0.0694] |
| gemma4:latest_baseline vs nemotron-mini:4b_rag_enhanced | -0.2621 | 3.0400e-01 | ❌ No | [-0.5791, 0.0550] |
| gemma4:latest_baseline vs nuextract:latest_baseline | -0.1261 | 9.9980e-01 | ❌ No | [-0.4431, 0.1910] |
| gemma4:latest_baseline vs nuextract:latest_rag_enhanced | -0.3080 | 7.0700e-02 | ❌ No | [-0.6251, 0.0090] |
| gemma4:latest_baseline vs qwen2.5:14b_baseline | -0.0570 | 1.0000e+00 | ❌ No | [-0.3740, 0.2600] |
| gemma4:latest_baseline vs qwen2.5:14b_rag_enhanced | -0.0386 | 1.0000e+00 | ❌ No | [-0.3557, 0.2784] |
| gemma4:latest_baseline vs qwen3:8b_baseline | -0.1311 | 9.9950e-01 | ❌ No | [-0.4481, 0.1859] |
| gemma4:latest_baseline vs qwen3:8b_rag_enhanced | -0.1664 | 9.8000e-01 | ❌ No | [-0.4835, 0.1506] |
| gemma4:latest_rag_enhanced vs gemma:latest_baseline | 0.0218 | 1.0000e+00 | ❌ No | [-0.2953, 0.3388] |
| gemma4:latest_rag_enhanced vs gemma:latest_rag_enhanced | 0.0298 | 1.0000e+00 | ❌ No | [-0.2873, 0.3468] |
| gemma4:latest_rag_enhanced vs llama3.1:8b_baseline | 0.0023 | 1.0000e+00 | ❌ No | [-0.3147, 0.3194] |
| gemma4:latest_rag_enhanced vs llama3.1:8b_rag_enhanced | 0.0293 | 1.0000e+00 | ❌ No | [-0.2877, 0.3464] |
| gemma4:latest_rag_enhanced vs llama3.2:latest_baseline | 0.0271 | 1.0000e+00 | ❌ No | [-0.2900, 0.3441] |
| gemma4:latest_rag_enhanced vs llama3.2:latest_rag_enhanced | -0.0291 | 1.0000e+00 | ❌ No | [-0.3461, 0.2880] |
| gemma4:latest_rag_enhanced vs minimax-m3:cloud_baseline | -0.4037 | 8.0000e-04 | ✅ Yes | [-0.7207, -0.0867] |
| gemma4:latest_rag_enhanced vs minimax-m3:cloud_rag_enhanced | -0.2330 | 5.6780e-01 | ❌ No | [-0.5501, 0.0840] |
| gemma4:latest_rag_enhanced vs mistral-nemo:latest_baseline | -0.0741 | 1.0000e+00 | ❌ No | [-0.3912, 0.2429] |
| gemma4:latest_rag_enhanced vs mistral-nemo:latest_rag_enhanced | -0.0463 | 1.0000e+00 | ❌ No | [-0.3633, 0.2708] |
| gemma4:latest_rag_enhanced vs nemotron-mini:4b_baseline | -0.1849 | 9.3040e-01 | ❌ No | [-0.5019, 0.1321] |
| gemma4:latest_rag_enhanced vs nemotron-mini:4b_rag_enhanced | -0.1993 | 8.5540e-01 | ❌ No | [-0.5164, 0.1177] |
| gemma4:latest_rag_enhanced vs nuextract:latest_baseline | -0.0633 | 1.0000e+00 | ❌ No | [-0.3804, 0.2537] |
| gemma4:latest_rag_enhanced vs nuextract:latest_rag_enhanced | -0.2453 | 4.5000e-01 | ❌ No | [-0.5623, 0.0718] |
| gemma4:latest_rag_enhanced vs qwen2.5:14b_baseline | 0.0058 | 1.0000e+00 | ❌ No | [-0.3113, 0.3228] |
| gemma4:latest_rag_enhanced vs qwen2.5:14b_rag_enhanced | 0.0241 | 1.0000e+00 | ❌ No | [-0.2929, 0.3412] |
| gemma4:latest_rag_enhanced vs qwen3:8b_baseline | -0.0683 | 1.0000e+00 | ❌ No | [-0.3854, 0.2487] |
| gemma4:latest_rag_enhanced vs qwen3:8b_rag_enhanced | -0.1037 | 1.0000e+00 | ❌ No | [-0.4207, 0.2134] |
| gemma:latest_baseline vs gemma:latest_rag_enhanced | 0.0080 | 1.0000e+00 | ❌ No | [-0.3090, 0.3250] |
| gemma:latest_baseline vs llama3.1:8b_baseline | -0.0194 | 1.0000e+00 | ❌ No | [-0.3365, 0.2976] |
| gemma:latest_baseline vs llama3.1:8b_rag_enhanced | 0.0076 | 1.0000e+00 | ❌ No | [-0.3094, 0.3246] |
| gemma:latest_baseline vs llama3.2:latest_baseline | 0.0053 | 1.0000e+00 | ❌ No | [-0.3117, 0.3224] |
| gemma:latest_baseline vs llama3.2:latest_rag_enhanced | -0.0508 | 1.0000e+00 | ❌ No | [-0.3679, 0.2662] |
| gemma:latest_baseline vs minimax-m3:cloud_baseline | -0.4255 | 2.0000e-04 | ✅ Yes | [-0.7425, -0.1084] |
| gemma:latest_baseline vs minimax-m3:cloud_rag_enhanced | -0.2548 | 3.6420e-01 | ❌ No | [-0.5718, 0.0623] |
| gemma:latest_baseline vs mistral-nemo:latest_baseline | -0.0959 | 1.0000e+00 | ❌ No | [-0.4129, 0.2211] |
| gemma:latest_baseline vs mistral-nemo:latest_rag_enhanced | -0.0680 | 1.0000e+00 | ❌ No | [-0.3851, 0.2490] |
| gemma:latest_baseline vs nemotron-mini:4b_baseline | -0.2066 | 8.0420e-01 | ❌ No | [-0.5237, 0.1104] |
| gemma:latest_baseline vs nemotron-mini:4b_rag_enhanced | -0.2211 | 6.8170e-01 | ❌ No | [-0.5381, 0.0960] |
| gemma:latest_baseline vs nuextract:latest_baseline | -0.0851 | 1.0000e+00 | ❌ No | [-0.4021, 0.2320] |
| gemma:latest_baseline vs nuextract:latest_rag_enhanced | -0.2670 | 2.6690e-01 | ❌ No | [-0.5841, 0.0500] |
| gemma:latest_baseline vs qwen2.5:14b_baseline | -0.0160 | 1.0000e+00 | ❌ No | [-0.3330, 0.3010] |
| gemma:latest_baseline vs qwen2.5:14b_rag_enhanced | 0.0024 | 1.0000e+00 | ❌ No | [-0.3147, 0.3194] |
| gemma:latest_baseline vs qwen3:8b_baseline | -0.0901 | 1.0000e+00 | ❌ No | [-0.4071, 0.2270] |
| gemma:latest_baseline vs qwen3:8b_rag_enhanced | -0.1254 | 9.9980e-01 | ❌ No | [-0.4425, 0.1916] |
| gemma:latest_rag_enhanced vs llama3.1:8b_baseline | -0.0274 | 1.0000e+00 | ❌ No | [-0.3445, 0.2896] |
| gemma:latest_rag_enhanced vs llama3.1:8b_rag_enhanced | -0.0004 | 1.0000e+00 | ❌ No | [-0.3174, 0.3166] |
| gemma:latest_rag_enhanced vs llama3.2:latest_baseline | -0.0027 | 1.0000e+00 | ❌ No | [-0.3197, 0.3144] |
| gemma:latest_rag_enhanced vs llama3.2:latest_rag_enhanced | -0.0588 | 1.0000e+00 | ❌ No | [-0.3758, 0.2582] |
| gemma:latest_rag_enhanced vs minimax-m3:cloud_baseline | -0.4335 | 2.0000e-04 | ✅ Yes | [-0.7505, -0.1164] |
| gemma:latest_rag_enhanced vs minimax-m3:cloud_rag_enhanced | -0.2628 | 2.9870e-01 | ❌ No | [-0.5798, 0.0543] |
| gemma:latest_rag_enhanced vs mistral-nemo:latest_baseline | -0.1039 | 1.0000e+00 | ❌ No | [-0.4209, 0.2132] |
| gemma:latest_rag_enhanced vs mistral-nemo:latest_rag_enhanced | -0.0760 | 1.0000e+00 | ❌ No | [-0.3931, 0.2410] |
| gemma:latest_rag_enhanced vs nemotron-mini:4b_baseline | -0.2146 | 7.3930e-01 | ❌ No | [-0.5317, 0.1024] |
| gemma:latest_rag_enhanced vs nemotron-mini:4b_rag_enhanced | -0.2291 | 6.0600e-01 | ❌ No | [-0.5461, 0.0880] |
| gemma:latest_rag_enhanced vs nuextract:latest_baseline | -0.0931 | 1.0000e+00 | ❌ No | [-0.4101, 0.2240] |
| gemma:latest_rag_enhanced vs nuextract:latest_rag_enhanced | -0.2750 | 2.1300e-01 | ❌ No | [-0.5921, 0.0420] |
| gemma:latest_rag_enhanced vs qwen2.5:14b_baseline | -0.0240 | 1.0000e+00 | ❌ No | [-0.3410, 0.2931] |
| gemma:latest_rag_enhanced vs qwen2.5:14b_rag_enhanced | -0.0056 | 1.0000e+00 | ❌ No | [-0.3227, 0.3114] |
| gemma:latest_rag_enhanced vs qwen3:8b_baseline | -0.0981 | 1.0000e+00 | ❌ No | [-0.4151, 0.2190] |
| gemma:latest_rag_enhanced vs qwen3:8b_rag_enhanced | -0.1334 | 9.9930e-01 | ❌ No | [-0.4505, 0.1836] |
| llama3.1:8b_baseline vs llama3.1:8b_rag_enhanced | 0.0270 | 1.0000e+00 | ❌ No | [-0.2900, 0.3441] |
| llama3.1:8b_baseline vs llama3.2:latest_baseline | 0.0247 | 1.0000e+00 | ❌ No | [-0.2923, 0.3418] |
| llama3.1:8b_baseline vs llama3.2:latest_rag_enhanced | -0.0314 | 1.0000e+00 | ❌ No | [-0.3484, 0.2857] |
| llama3.1:8b_baseline vs minimax-m3:cloud_baseline | -0.4060 | 7.0000e-04 | ✅ Yes | [-0.7231, -0.0890] |
| llama3.1:8b_baseline vs minimax-m3:cloud_rag_enhanced | -0.2354 | 5.4510e-01 | ❌ No | [-0.5524, 0.0817] |
| llama3.1:8b_baseline vs mistral-nemo:latest_baseline | -0.0765 | 1.0000e+00 | ❌ No | [-0.3935, 0.2406] |
| llama3.1:8b_baseline vs mistral-nemo:latest_rag_enhanced | -0.0486 | 1.0000e+00 | ❌ No | [-0.3656, 0.2684] |
| llama3.1:8b_baseline vs nemotron-mini:4b_baseline | -0.1872 | 9.2060e-01 | ❌ No | [-0.5043, 0.1298] |
| llama3.1:8b_baseline vs nemotron-mini:4b_rag_enhanced | -0.2017 | 8.4000e-01 | ❌ No | [-0.5187, 0.1154] |
| llama3.1:8b_baseline vs nuextract:latest_baseline | -0.0657 | 1.0000e+00 | ❌ No | [-0.3827, 0.2514] |
| llama3.1:8b_baseline vs nuextract:latest_rag_enhanced | -0.2476 | 4.2830e-01 | ❌ No | [-0.5646, 0.0694] |
| llama3.1:8b_baseline vs qwen2.5:14b_baseline | 0.0034 | 1.0000e+00 | ❌ No | [-0.3136, 0.3205] |
| llama3.1:8b_baseline vs qwen2.5:14b_rag_enhanced | 0.0218 | 1.0000e+00 | ❌ No | [-0.2952, 0.3388] |
| llama3.1:8b_baseline vs qwen3:8b_baseline | -0.0707 | 1.0000e+00 | ❌ No | [-0.3877, 0.2464] |
| llama3.1:8b_baseline vs qwen3:8b_rag_enhanced | -0.1060 | 1.0000e+00 | ❌ No | [-0.4231, 0.2110] |
| llama3.1:8b_rag_enhanced vs llama3.2:latest_baseline | -0.0023 | 1.0000e+00 | ❌ No | [-0.3193, 0.3148] |
| llama3.1:8b_rag_enhanced vs llama3.2:latest_rag_enhanced | -0.0584 | 1.0000e+00 | ❌ No | [-0.3754, 0.2586] |
| llama3.1:8b_rag_enhanced vs minimax-m3:cloud_baseline | -0.4331 | 2.0000e-04 | ✅ Yes | [-0.7501, -0.1160] |
| llama3.1:8b_rag_enhanced vs minimax-m3:cloud_rag_enhanced | -0.2624 | 3.0190e-01 | ❌ No | [-0.5794, 0.0547] |
| llama3.1:8b_rag_enhanced vs mistral-nemo:latest_baseline | -0.1035 | 1.0000e+00 | ❌ No | [-0.4205, 0.2136] |
| llama3.1:8b_rag_enhanced vs mistral-nemo:latest_rag_enhanced | -0.0756 | 1.0000e+00 | ❌ No | [-0.3927, 0.2414] |
| llama3.1:8b_rag_enhanced vs nemotron-mini:4b_baseline | -0.2142 | 7.4280e-01 | ❌ No | [-0.5313, 0.1028] |
| llama3.1:8b_rag_enhanced vs nemotron-mini:4b_rag_enhanced | -0.2287 | 6.0990e-01 | ❌ No | [-0.5457, 0.0884] |
| llama3.1:8b_rag_enhanced vs nuextract:latest_baseline | -0.0927 | 1.0000e+00 | ❌ No | [-0.4097, 0.2244] |
| llama3.1:8b_rag_enhanced vs nuextract:latest_rag_enhanced | -0.2746 | 2.1550e-01 | ❌ No | [-0.5916, 0.0424] |
| llama3.1:8b_rag_enhanced vs qwen2.5:14b_baseline | -0.0236 | 1.0000e+00 | ❌ No | [-0.3406, 0.2935] |
| llama3.1:8b_rag_enhanced vs qwen2.5:14b_rag_enhanced | -0.0052 | 1.0000e+00 | ❌ No | [-0.3223, 0.3118] |
| llama3.1:8b_rag_enhanced vs qwen3:8b_baseline | -0.0977 | 1.0000e+00 | ❌ No | [-0.4147, 0.2194] |
| llama3.1:8b_rag_enhanced vs qwen3:8b_rag_enhanced | -0.1330 | 9.9940e-01 | ❌ No | [-0.4501, 0.1840] |
| llama3.2:latest_baseline vs llama3.2:latest_rag_enhanced | -0.0561 | 1.0000e+00 | ❌ No | [-0.3732, 0.2609] |
| llama3.2:latest_baseline vs minimax-m3:cloud_baseline | -0.4308 | 2.0000e-04 | ✅ Yes | [-0.7478, -0.1137] |
| llama3.2:latest_baseline vs minimax-m3:cloud_rag_enhanced | -0.2601 | 3.1980e-01 | ❌ No | [-0.5771, 0.0569] |
| llama3.2:latest_baseline vs mistral-nemo:latest_baseline | -0.1012 | 1.0000e+00 | ❌ No | [-0.4183, 0.2158] |
| llama3.2:latest_baseline vs mistral-nemo:latest_rag_enhanced | -0.0733 | 1.0000e+00 | ❌ No | [-0.3904, 0.2437] |
| llama3.2:latest_baseline vs nemotron-mini:4b_baseline | -0.2120 | 7.6190e-01 | ❌ No | [-0.5290, 0.1051] |
| llama3.2:latest_baseline vs nemotron-mini:4b_rag_enhanced | -0.2264 | 6.3160e-01 | ❌ No | [-0.5435, 0.0906] |
| llama3.2:latest_baseline vs nuextract:latest_baseline | -0.0904 | 1.0000e+00 | ❌ No | [-0.4074, 0.2266] |
| llama3.2:latest_baseline vs nuextract:latest_rag_enhanced | -0.2723 | 2.3010e-01 | ❌ No | [-0.5894, 0.0447] |
| llama3.2:latest_baseline vs qwen2.5:14b_baseline | -0.0213 | 1.0000e+00 | ❌ No | [-0.3384, 0.2957] |
| llama3.2:latest_baseline vs qwen2.5:14b_rag_enhanced | -0.0029 | 1.0000e+00 | ❌ No | [-0.3200, 0.3141] |
| llama3.2:latest_baseline vs qwen3:8b_baseline | -0.0954 | 1.0000e+00 | ❌ No | [-0.4125, 0.2216] |
| llama3.2:latest_baseline vs qwen3:8b_rag_enhanced | -0.1308 | 9.9950e-01 | ❌ No | [-0.4478, 0.1863] |
| llama3.2:latest_rag_enhanced vs minimax-m3:cloud_baseline | -0.3747 | 3.8000e-03 | ✅ Yes | [-0.6917, -0.0576] |
| llama3.2:latest_rag_enhanced vs minimax-m3:cloud_rag_enhanced | -0.2040 | 8.2400e-01 | ❌ No | [-0.5210, 0.1131] |
| llama3.2:latest_rag_enhanced vs mistral-nemo:latest_baseline | -0.0451 | 1.0000e+00 | ❌ No | [-0.3621, 0.2720] |
| llama3.2:latest_rag_enhanced vs mistral-nemo:latest_rag_enhanced | -0.0172 | 1.0000e+00 | ❌ No | [-0.3343, 0.2998] |
| llama3.2:latest_rag_enhanced vs nemotron-mini:4b_baseline | -0.1558 | 9.9190e-01 | ❌ No | [-0.4729, 0.1612] |
| llama3.2:latest_rag_enhanced vs nemotron-mini:4b_rag_enhanced | -0.1703 | 9.7320e-01 | ❌ No | [-0.4873, 0.1468] |
| llama3.2:latest_rag_enhanced vs nuextract:latest_baseline | -0.0343 | 1.0000e+00 | ❌ No | [-0.3513, 0.2828] |
| llama3.2:latest_rag_enhanced vs nuextract:latest_rag_enhanced | -0.2162 | 7.2580e-01 | ❌ No | [-0.5332, 0.1008] |
| llama3.2:latest_rag_enhanced vs qwen2.5:14b_baseline | 0.0348 | 1.0000e+00 | ❌ No | [-0.2822, 0.3519] |
| llama3.2:latest_rag_enhanced vs qwen2.5:14b_rag_enhanced | 0.0532 | 1.0000e+00 | ❌ No | [-0.2638, 0.3702] |
| llama3.2:latest_rag_enhanced vs qwen3:8b_baseline | -0.0393 | 1.0000e+00 | ❌ No | [-0.3563, 0.2778] |
| llama3.2:latest_rag_enhanced vs qwen3:8b_rag_enhanced | -0.0746 | 1.0000e+00 | ❌ No | [-0.3917, 0.2424] |
| minimax-m3:cloud_baseline vs minimax-m3:cloud_rag_enhanced | 0.1707 | 9.7240e-01 | ❌ No | [-0.1464, 0.4877] |
| minimax-m3:cloud_baseline vs mistral-nemo:latest_baseline | 0.3296 | 3.0100e-02 | ✅ Yes | [0.0125, 0.6466] |
| minimax-m3:cloud_baseline vs mistral-nemo:latest_rag_enhanced | 0.3574 | 8.7000e-03 | ✅ Yes | [0.0404, 0.6745] |
| minimax-m3:cloud_baseline vs nemotron-mini:4b_baseline | 0.2188 | 7.0250e-01 | ❌ No | [-0.0982, 0.5359] |
| minimax-m3:cloud_baseline vs nemotron-mini:4b_rag_enhanced | 0.2044 | 8.2100e-01 | ❌ No | [-0.1127, 0.5214] |
| minimax-m3:cloud_baseline vs nuextract:latest_baseline | 0.3404 | 1.8900e-02 | ✅ Yes | [0.0233, 0.6574] |
| minimax-m3:cloud_baseline vs nuextract:latest_rag_enhanced | 0.1584 | 9.8970e-01 | ❌ No | [-0.1586, 0.4755] |
| minimax-m3:cloud_baseline vs qwen2.5:14b_baseline | 0.4095 | 6.0000e-04 | ✅ Yes | [0.0924, 0.7265] |
| minimax-m3:cloud_baseline vs qwen2.5:14b_rag_enhanced | 0.4278 | 2.0000e-04 | ✅ Yes | [0.1108, 0.7449] |
| minimax-m3:cloud_baseline vs qwen3:8b_baseline | 0.3354 | 2.3500e-02 | ✅ Yes | [0.0183, 0.6524] |
| minimax-m3:cloud_baseline vs qwen3:8b_rag_enhanced | 0.3000 | 9.4500e-02 | ❌ No | [-0.0170, 0.6171] |
| minimax-m3:cloud_rag_enhanced vs mistral-nemo:latest_baseline | 0.1589 | 9.8930e-01 | ❌ No | [-0.1582, 0.4759] |
| minimax-m3:cloud_rag_enhanced vs mistral-nemo:latest_rag_enhanced | 0.1867 | 9.2270e-01 | ❌ No | [-0.1303, 0.5038] |
| minimax-m3:cloud_rag_enhanced vs nemotron-mini:4b_baseline | 0.0481 | 1.0000e+00 | ❌ No | [-0.2689, 0.3652] |
| minimax-m3:cloud_rag_enhanced vs nemotron-mini:4b_rag_enhanced | 0.0337 | 1.0000e+00 | ❌ No | [-0.2834, 0.3507] |
| minimax-m3:cloud_rag_enhanced vs nuextract:latest_baseline | 0.1697 | 9.7430e-01 | ❌ No | [-0.1473, 0.4867] |
| minimax-m3:cloud_rag_enhanced vs nuextract:latest_rag_enhanced | -0.0122 | 1.0000e+00 | ❌ No | [-0.3293, 0.3048] |
| minimax-m3:cloud_rag_enhanced vs qwen2.5:14b_baseline | 0.2388 | 5.1190e-01 | ❌ No | [-0.0783, 0.5558] |
| minimax-m3:cloud_rag_enhanced vs qwen2.5:14b_rag_enhanced | 0.2572 | 3.4400e-01 | ❌ No | [-0.0599, 0.5742] |
| minimax-m3:cloud_rag_enhanced vs qwen3:8b_baseline | 0.1647 | 9.8260e-01 | ❌ No | [-0.1524, 0.4817] |
| minimax-m3:cloud_rag_enhanced vs qwen3:8b_rag_enhanced | 0.1293 | 9.9960e-01 | ❌ No | [-0.1877, 0.4464] |
| mistral-nemo:latest_baseline vs mistral-nemo:latest_rag_enhanced | 0.0279 | 1.0000e+00 | ❌ No | [-0.2892, 0.3449] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_baseline | -0.1108 | 1.0000e+00 | ❌ No | [-0.4278, 0.2063] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_rag_enhanced | -0.1252 | 9.9980e-01 | ❌ No | [-0.4422, 0.1918] |
| mistral-nemo:latest_baseline vs nuextract:latest_baseline | 0.0108 | 1.0000e+00 | ❌ No | [-0.3062, 0.3279] |
| mistral-nemo:latest_baseline vs nuextract:latest_rag_enhanced | -0.1711 | 9.7150e-01 | ❌ No | [-0.4882, 0.1459] |
| mistral-nemo:latest_baseline vs qwen2.5:14b_baseline | 0.0799 | 1.0000e+00 | ❌ No | [-0.2371, 0.3969] |
| mistral-nemo:latest_baseline vs qwen2.5:14b_rag_enhanced | 0.0983 | 1.0000e+00 | ❌ No | [-0.2188, 0.4153] |
| mistral-nemo:latest_baseline vs qwen3:8b_baseline | 0.0058 | 1.0000e+00 | ❌ No | [-0.3112, 0.3228] |
| mistral-nemo:latest_baseline vs qwen3:8b_rag_enhanced | -0.0295 | 1.0000e+00 | ❌ No | [-0.3466, 0.2875] |
| mistral-nemo:latest_rag_enhanced vs nemotron-mini:4b_baseline | -0.1386 | 9.9870e-01 | ❌ No | [-0.4557, 0.1784] |
| mistral-nemo:latest_rag_enhanced vs nemotron-mini:4b_rag_enhanced | -0.1531 | 9.9380e-01 | ❌ No | [-0.4701, 0.1640] |
| mistral-nemo:latest_rag_enhanced vs nuextract:latest_baseline | -0.0171 | 1.0000e+00 | ❌ No | [-0.3341, 0.3000] |
| mistral-nemo:latest_rag_enhanced vs nuextract:latest_rag_enhanced | -0.1990 | 8.5750e-01 | ❌ No | [-0.5160, 0.1180] |
| mistral-nemo:latest_rag_enhanced vs qwen2.5:14b_baseline | 0.0520 | 1.0000e+00 | ❌ No | [-0.2650, 0.3691] |
| mistral-nemo:latest_rag_enhanced vs qwen2.5:14b_rag_enhanced | 0.0704 | 1.0000e+00 | ❌ No | [-0.2466, 0.3874] |
| mistral-nemo:latest_rag_enhanced vs qwen3:8b_baseline | -0.0221 | 1.0000e+00 | ❌ No | [-0.3391, 0.2950] |
| mistral-nemo:latest_rag_enhanced vs qwen3:8b_rag_enhanced | -0.0574 | 1.0000e+00 | ❌ No | [-0.3745, 0.2596] |
| nemotron-mini:4b_baseline vs nemotron-mini:4b_rag_enhanced | -0.0144 | 1.0000e+00 | ❌ No | [-0.3315, 0.3026] |
| nemotron-mini:4b_baseline vs nuextract:latest_baseline | 0.1216 | 9.9990e-01 | ❌ No | [-0.1955, 0.4386] |
| nemotron-mini:4b_baseline vs nuextract:latest_rag_enhanced | -0.0604 | 1.0000e+00 | ❌ No | [-0.3774, 0.2567] |
| nemotron-mini:4b_baseline vs qwen2.5:14b_baseline | 0.1907 | 9.0470e-01 | ❌ No | [-0.1264, 0.5077] |
| nemotron-mini:4b_baseline vs qwen2.5:14b_rag_enhanced | 0.2090 | 7.8570e-01 | ❌ No | [-0.1080, 0.5261] |
| nemotron-mini:4b_baseline vs qwen3:8b_baseline | 0.1166 | 9.9990e-01 | ❌ No | [-0.2005, 0.4336] |
| nemotron-mini:4b_baseline vs qwen3:8b_rag_enhanced | 0.0812 | 1.0000e+00 | ❌ No | [-0.2358, 0.3983] |
| nemotron-mini:4b_rag_enhanced vs nuextract:latest_baseline | 0.1360 | 9.9910e-01 | ❌ No | [-0.1810, 0.4530] |
| nemotron-mini:4b_rag_enhanced vs nuextract:latest_rag_enhanced | -0.0459 | 1.0000e+00 | ❌ No | [-0.3630, 0.2711] |
| nemotron-mini:4b_rag_enhanced vs qwen2.5:14b_baseline | 0.2051 | 8.1580e-01 | ❌ No | [-0.1120, 0.5221] |
| nemotron-mini:4b_rag_enhanced vs qwen2.5:14b_rag_enhanced | 0.2235 | 6.5950e-01 | ❌ No | [-0.0936, 0.5405] |
| nemotron-mini:4b_rag_enhanced vs qwen3:8b_baseline | 0.1310 | 9.9950e-01 | ❌ No | [-0.1860, 0.4480] |
| nemotron-mini:4b_rag_enhanced vs qwen3:8b_rag_enhanced | 0.0957 | 1.0000e+00 | ❌ No | [-0.2214, 0.4127] |
| nuextract:latest_baseline vs nuextract:latest_rag_enhanced | -0.1819 | 9.4150e-01 | ❌ No | [-0.4990, 0.1351] |
| nuextract:latest_baseline vs qwen2.5:14b_baseline | 0.0691 | 1.0000e+00 | ❌ No | [-0.2480, 0.3861] |
| nuextract:latest_baseline vs qwen2.5:14b_rag_enhanced | 0.0875 | 1.0000e+00 | ❌ No | [-0.2296, 0.4045] |
| nuextract:latest_baseline vs qwen3:8b_baseline | -0.0050 | 1.0000e+00 | ❌ No | [-0.3221, 0.3120] |
| nuextract:latest_baseline vs qwen3:8b_rag_enhanced | -0.0404 | 1.0000e+00 | ❌ No | [-0.3574, 0.2767] |
| nuextract:latest_rag_enhanced vs qwen2.5:14b_baseline | 0.2510 | 3.9720e-01 | ❌ No | [-0.0660, 0.5681] |
| nuextract:latest_rag_enhanced vs qwen2.5:14b_rag_enhanced | 0.2694 | 2.5000e-01 | ❌ No | [-0.0476, 0.5864] |
| nuextract:latest_rag_enhanced vs qwen3:8b_baseline | 0.1769 | 9.5740e-01 | ❌ No | [-0.1401, 0.4940] |
| nuextract:latest_rag_enhanced vs qwen3:8b_rag_enhanced | 0.1416 | 9.9820e-01 | ❌ No | [-0.1755, 0.4586] |
| qwen2.5:14b_baseline vs qwen2.5:14b_rag_enhanced | 0.0184 | 1.0000e+00 | ❌ No | [-0.2987, 0.3354] |
| qwen2.5:14b_baseline vs qwen3:8b_baseline | -0.0741 | 1.0000e+00 | ❌ No | [-0.3911, 0.2429] |
| qwen2.5:14b_baseline vs qwen3:8b_rag_enhanced | -0.1094 | 1.0000e+00 | ❌ No | [-0.4265, 0.2076] |
| qwen2.5:14b_rag_enhanced vs qwen3:8b_baseline | -0.0925 | 1.0000e+00 | ❌ No | [-0.4095, 0.2246] |
| qwen2.5:14b_rag_enhanced vs qwen3:8b_rag_enhanced | -0.1278 | 9.9970e-01 | ❌ No | [-0.4449, 0.1892] |
| qwen3:8b_baseline vs qwen3:8b_rag_enhanced | -0.0353 | 1.0000e+00 | ❌ No | [-0.3524, 0.2817] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 5332.9 characters.
- **Outlier Records Identified:** 6 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline | 0.3431 | 0.3108 | -0.0323 | 📉 Decreased |
| deepseek-r1:1.5b_rag_enhanced | 0.2749 | 0.3160 | +0.0411 | 📈 Improved |
| gemma4:31b-cloud_baseline | 0.3973 | 0.2848 | -0.1125 | 📉 Decreased |
| gemma4:31b-cloud_rag_enhanced | 0.4272 | 0.4579 | +0.0307 | 📈 Improved |
| gemma4:31b-mlx_baseline | 0.6852 | 0.6681 | -0.0172 | 📉 Decreased |
| gemma4:31b-mlx_rag_enhanced | 0.6897 | 0.6718 | -0.0178 | 📉 Decreased |
| gemma4:latest_baseline | 0.6676 | 0.6185 | -0.0491 | 📉 Decreased |
| gemma4:latest_rag_enhanced | 0.6048 | 0.6971 | +0.0923 | 📈 Improved |
| gemma:latest_baseline | 0.6266 | 0.6646 | +0.0380 | 📈 Improved |
| gemma:latest_rag_enhanced | 0.6346 | 0.6577 | +0.0231 | 📈 Improved |
| llama3.1:8b_baseline | 0.6072 | 0.6076 | +0.0004 | 📈 Improved |
| llama3.1:8b_rag_enhanced | 0.6342 | 0.6418 | +0.0077 | 📈 Improved |
| llama3.2:latest_baseline | 0.6319 | 0.6455 | +0.0136 | 📈 Improved |
| llama3.2:latest_rag_enhanced | 0.5758 | 0.5608 | -0.0150 | 📉 Decreased |
| minimax-m3:cloud_baseline | 0.2011 | 0.1234 | -0.0778 | 📉 Decreased |
| minimax-m3:cloud_rag_enhanced | 0.3718 | 0.3209 | -0.0509 | 📉 Decreased |
| mistral-nemo:latest_baseline | 0.5307 | 0.4921 | -0.0386 | 📉 Decreased |
| mistral-nemo:latest_rag_enhanced | 0.5586 | 0.5274 | -0.0311 | 📉 Decreased |
| nemotron-mini:4b_baseline | 0.4199 | 0.4233 | +0.0034 | 📈 Improved |
| nemotron-mini:4b_rag_enhanced | 0.4055 | 0.4308 | +0.0253 | 📈 Improved |
| nuextract:latest_baseline | 0.5415 | 0.5443 | +0.0028 | 📈 Improved |
| nuextract:latest_rag_enhanced | 0.3596 | 0.3461 | -0.0135 | 📉 Decreased |
| qwen2.5:14b_baseline | 0.6106 | 0.6102 | -0.0004 | 📉 Decreased |
| qwen2.5:14b_rag_enhanced | 0.6290 | 0.6282 | -0.0007 | 📉 Decreased |
| qwen3:8b_baseline | 0.5365 | 0.6046 | +0.0681 | 📈 Improved |
| qwen3:8b_rag_enhanced | 0.5012 | 0.5327 | +0.0315 | 📈 Improved |