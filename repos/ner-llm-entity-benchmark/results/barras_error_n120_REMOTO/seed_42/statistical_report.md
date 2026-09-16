# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 292.4758
- **p-Value:** 0.0000e+00

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline | 113 | 0.0088 | -0.0087 | 0.0264 | 0.0941 |
| gemma4:31b-cloud_kb_rag | 113 | 0.0088 | -0.0087 | 0.0264 | 0.0941 |
| gemma4:31b-mlx_baseline | 113 | 0.8147 | 0.7887 | 0.8408 | 0.1399 |
| gemma4:31b-mlx_kb_rag | 113 | 0.8250 | 0.8001 | 0.8499 | 0.1335 |
| gemma4:12b-mlx_baseline | 113 | 0.7785 | 0.7521 | 0.8050 | 0.1419 |
| gemma4:12b-mlx_kb_rag | 113 | 0.7984 | 0.7734 | 0.8235 | 0.1344 |
| gemma4:latest_baseline | 113 | 0.7533 | 0.7257 | 0.7809 | 0.1479 |
| gemma4:latest_kb_rag | 113 | 0.7761 | 0.7494 | 0.8029 | 0.1433 |
| qwen3:8b_baseline | 113 | 0.6903 | 0.6607 | 0.7199 | 0.1586 |
| qwen3:8b_kb_rag | 113 | 0.6898 | 0.6614 | 0.7182 | 0.1523 |
| gpt-oss:20b_baseline | 113 | 0.7462 | 0.7162 | 0.7763 | 0.1612 |
| gpt-oss:20b_kb_rag | 113 | 0.7708 | 0.7450 | 0.7967 | 0.1387 |
| mistral-nemo:latest_baseline | 113 | 0.6063 | 0.5720 | 0.6406 | 0.1840 |
| mistral-nemo:latest_kb_rag | 113 | 0.5635 | 0.5288 | 0.5982 | 0.1862 |
| llama3.2:latest_baseline | 113 | 0.6325 | 0.5991 | 0.6660 | 0.1796 |
| llama3.2:latest_kb_rag | 113 | 0.6997 | 0.6696 | 0.7298 | 0.1614 |
| llama3.1:8b_baseline | 113 | 0.6917 | 0.6637 | 0.7197 | 0.1503 |
| llama3.1:8b_kb_rag | 113 | 0.7148 | 0.6854 | 0.7442 | 0.1576 |
| nemotron-mini:4b_baseline | 113 | 0.2829 | 0.2425 | 0.3233 | 0.2167 |
| nemotron-mini:4b_kb_rag | 113 | 0.4077 | 0.3729 | 0.4425 | 0.1868 |
| deepseek-r1:1.5b_baseline | 113 | 0.2873 | 0.2578 | 0.3168 | 0.1583 |
| deepseek-r1:1.5b_kb_rag | 113 | 0.3081 | 0.2755 | 0.3408 | 0.1753 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline vs deepseek-r1:1.5b_kb_rag | 0.0208 | 1.0000e+00 | ❌ No | [-0.0543, 0.0959] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_baseline | 0.4912 | 0.0000e+00 | ✅ Yes | [0.4161, 0.5662] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_kb_rag | 0.5111 | 0.0000e+00 | ✅ Yes | [0.4360, 0.5862] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_baseline | -0.2785 | 0.0000e+00 | ✅ Yes | [-0.3535, -0.2034] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_kb_rag | -0.2785 | 0.0000e+00 | ✅ Yes | [-0.3535, -0.2034] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_baseline | 0.5274 | 0.0000e+00 | ✅ Yes | [0.4523, 0.6024] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_kb_rag | 0.5377 | 0.0000e+00 | ✅ Yes | [0.4626, 0.6127] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_baseline | 0.4660 | 0.0000e+00 | ✅ Yes | [0.3909, 0.5410] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_kb_rag | 0.4888 | 0.0000e+00 | ✅ Yes | [0.4138, 0.5639] |
| deepseek-r1:1.5b_baseline vs gpt-oss:20b_baseline | 0.4589 | 0.0000e+00 | ✅ Yes | [0.3838, 0.5340] |
| deepseek-r1:1.5b_baseline vs gpt-oss:20b_kb_rag | 0.4835 | 0.0000e+00 | ✅ Yes | [0.4084, 0.5585] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_baseline | 0.4044 | 0.0000e+00 | ✅ Yes | [0.3293, 0.4794] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_kb_rag | 0.4275 | 0.0000e+00 | ✅ Yes | [0.3524, 0.5025] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_baseline | 0.3452 | 0.0000e+00 | ✅ Yes | [0.2701, 0.4203] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_kb_rag | 0.4124 | 0.0000e+00 | ✅ Yes | [0.3373, 0.4874] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_baseline | 0.3190 | 0.0000e+00 | ✅ Yes | [0.2439, 0.3940] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_kb_rag | 0.2761 | 0.0000e+00 | ✅ Yes | [0.2011, 0.3512] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_baseline | -0.0045 | 1.0000e+00 | ❌ No | [-0.0795, 0.0706] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_kb_rag | 0.1204 | 0.0000e+00 | ✅ Yes | [0.0453, 0.1954] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_baseline | 0.4030 | 0.0000e+00 | ✅ Yes | [0.3279, 0.4780] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_kb_rag | 0.4025 | 0.0000e+00 | ✅ Yes | [0.3274, 0.4775] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_baseline | 0.4704 | 0.0000e+00 | ✅ Yes | [0.3953, 0.5454] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_kb_rag | 0.4903 | 0.0000e+00 | ✅ Yes | [0.4152, 0.5654] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-cloud_baseline | -0.2993 | 0.0000e+00 | ✅ Yes | [-0.3744, -0.2242] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-cloud_kb_rag | -0.2993 | 0.0000e+00 | ✅ Yes | [-0.3744, -0.2242] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-mlx_baseline | 0.5066 | 0.0000e+00 | ✅ Yes | [0.4315, 0.5816] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-mlx_kb_rag | 0.5168 | 0.0000e+00 | ✅ Yes | [0.4418, 0.5919] |
| deepseek-r1:1.5b_kb_rag vs gemma4:latest_baseline | 0.4452 | 0.0000e+00 | ✅ Yes | [0.3701, 0.5202] |
| deepseek-r1:1.5b_kb_rag vs gemma4:latest_kb_rag | 0.4680 | 0.0000e+00 | ✅ Yes | [0.3929, 0.5431] |
| deepseek-r1:1.5b_kb_rag vs gpt-oss:20b_baseline | 0.4381 | 0.0000e+00 | ✅ Yes | [0.3630, 0.5132] |
| deepseek-r1:1.5b_kb_rag vs gpt-oss:20b_kb_rag | 0.4627 | 0.0000e+00 | ✅ Yes | [0.3876, 0.5377] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_baseline | 0.3836 | 0.0000e+00 | ✅ Yes | [0.3085, 0.4586] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_kb_rag | 0.4066 | 0.0000e+00 | ✅ Yes | [0.3316, 0.4817] |
| deepseek-r1:1.5b_kb_rag vs llama3.2:latest_baseline | 0.3244 | 0.0000e+00 | ✅ Yes | [0.2493, 0.3995] |
| deepseek-r1:1.5b_kb_rag vs llama3.2:latest_kb_rag | 0.3916 | 0.0000e+00 | ✅ Yes | [0.3165, 0.4666] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_baseline | 0.2982 | 0.0000e+00 | ✅ Yes | [0.2231, 0.3732] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_kb_rag | 0.2553 | 0.0000e+00 | ✅ Yes | [0.1803, 0.3304] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_baseline | -0.0253 | 9.9990e-01 | ❌ No | [-0.1003, 0.0498] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_kb_rag | 0.0996 | 4.0000e-04 | ✅ Yes | [0.0245, 0.1746] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_baseline | 0.3822 | 0.0000e+00 | ✅ Yes | [0.3071, 0.4572] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_kb_rag | 0.3816 | 0.0000e+00 | ✅ Yes | [0.3066, 0.4567] |
| gemma4:12b-mlx_baseline vs gemma4:12b-mlx_kb_rag | 0.0199 | 1.0000e+00 | ❌ No | [-0.0551, 0.0950] |
| gemma4:12b-mlx_baseline vs gemma4:31b-cloud_baseline | -0.7697 | 0.0000e+00 | ✅ Yes | [-0.8447, -0.6946] |
| gemma4:12b-mlx_baseline vs gemma4:31b-cloud_kb_rag | -0.7697 | 0.0000e+00 | ✅ Yes | [-0.8447, -0.6946] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_baseline | 0.0362 | 9.8370e-01 | ❌ No | [-0.0389, 0.1113] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_kb_rag | 0.0465 | 8.2360e-01 | ❌ No | [-0.0286, 0.1215] |
| gemma4:12b-mlx_baseline vs gemma4:latest_baseline | -0.0252 | 9.9990e-01 | ❌ No | [-0.1003, 0.0498] |
| gemma4:12b-mlx_baseline vs gemma4:latest_kb_rag | -0.0024 | 1.0000e+00 | ❌ No | [-0.0774, 0.0727] |
| gemma4:12b-mlx_baseline vs gpt-oss:20b_baseline | -0.0323 | 9.9600e-01 | ❌ No | [-0.1073, 0.0428] |
| gemma4:12b-mlx_baseline vs gpt-oss:20b_kb_rag | -0.0077 | 1.0000e+00 | ❌ No | [-0.0828, 0.0674] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_baseline | -0.0868 | 6.3000e-03 | ✅ Yes | [-0.1619, -0.0118] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_kb_rag | -0.0637 | 2.3290e-01 | ❌ No | [-0.1388, 0.0113] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_baseline | -0.1460 | 0.0000e+00 | ✅ Yes | [-0.2210, -0.0709] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_kb_rag | -0.0788 | 2.7000e-02 | ✅ Yes | [-0.1539, -0.0038] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_baseline | -0.1722 | 0.0000e+00 | ✅ Yes | [-0.2473, -0.0971] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.2151 | 0.0000e+00 | ✅ Yes | [-0.2901, -0.1400] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_baseline | -0.4956 | 0.0000e+00 | ✅ Yes | [-0.5707, -0.4206] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_kb_rag | -0.3708 | 0.0000e+00 | ✅ Yes | [-0.4459, -0.2957] |
| gemma4:12b-mlx_baseline vs qwen3:8b_baseline | -0.0882 | 4.8000e-03 | ✅ Yes | [-0.1633, -0.0132] |
| gemma4:12b-mlx_baseline vs qwen3:8b_kb_rag | -0.0887 | 4.3000e-03 | ✅ Yes | [-0.1638, -0.0137] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-cloud_baseline | -0.7896 | 0.0000e+00 | ✅ Yes | [-0.8647, -0.7145] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-cloud_kb_rag | -0.7896 | 0.0000e+00 | ✅ Yes | [-0.8647, -0.7145] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_baseline | 0.0163 | 1.0000e+00 | ❌ No | [-0.0588, 0.0913] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_kb_rag | 0.0265 | 9.9980e-01 | ❌ No | [-0.0485, 0.1016] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_baseline | -0.0451 | 8.5890e-01 | ❌ No | [-0.1202, 0.0299] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0223 | 1.0000e+00 | ❌ No | [-0.0974, 0.0528] |
| gemma4:12b-mlx_kb_rag vs gpt-oss:20b_baseline | -0.0522 | 6.3090e-01 | ❌ No | [-0.1273, 0.0229] |
| gemma4:12b-mlx_kb_rag vs gpt-oss:20b_kb_rag | -0.0276 | 9.9960e-01 | ❌ No | [-0.1027, 0.0474] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_baseline | -0.1067 | 1.0000e-04 | ✅ Yes | [-0.1818, -0.0317] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_kb_rag | -0.0837 | 1.1400e-02 | ✅ Yes | [-0.1587, -0.0086] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_baseline | -0.1659 | 0.0000e+00 | ✅ Yes | [-0.2410, -0.0908] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.0987 | 5.0000e-04 | ✅ Yes | [-0.1738, -0.0237] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.1921 | 0.0000e+00 | ✅ Yes | [-0.2672, -0.1171] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.2350 | 0.0000e+00 | ✅ Yes | [-0.3100, -0.1599] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_baseline | -0.5156 | 0.0000e+00 | ✅ Yes | [-0.5906, -0.4405] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | -0.3907 | 0.0000e+00 | ✅ Yes | [-0.4658, -0.3157] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_baseline | -0.1081 | 1.0000e-04 | ✅ Yes | [-0.1832, -0.0331] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.1087 | 0.0000e+00 | ✅ Yes | [-0.1837, -0.0336] |
| gemma4:31b-cloud_baseline vs gemma4:31b-cloud_kb_rag | 0.0000 | 1.0000e+00 | ❌ No | [-0.0751, 0.0751] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_baseline | 0.8059 | 0.0000e+00 | ✅ Yes | [0.7308, 0.8809] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_kb_rag | 0.8161 | 0.0000e+00 | ✅ Yes | [0.7411, 0.8912] |
| gemma4:31b-cloud_baseline vs gemma4:latest_baseline | 0.7445 | 0.0000e+00 | ✅ Yes | [0.6694, 0.8195] |
| gemma4:31b-cloud_baseline vs gemma4:latest_kb_rag | 0.7673 | 0.0000e+00 | ✅ Yes | [0.6922, 0.8424] |
| gemma4:31b-cloud_baseline vs gpt-oss:20b_baseline | 0.7374 | 0.0000e+00 | ✅ Yes | [0.6623, 0.8124] |
| gemma4:31b-cloud_baseline vs gpt-oss:20b_kb_rag | 0.7620 | 0.0000e+00 | ✅ Yes | [0.6869, 0.8370] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_baseline | 0.6829 | 0.0000e+00 | ✅ Yes | [0.6078, 0.7579] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_kb_rag | 0.7059 | 0.0000e+00 | ✅ Yes | [0.6309, 0.7810] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_baseline | 0.6237 | 0.0000e+00 | ✅ Yes | [0.5486, 0.6988] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_kb_rag | 0.6908 | 0.0000e+00 | ✅ Yes | [0.6158, 0.7659] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_baseline | 0.5975 | 0.0000e+00 | ✅ Yes | [0.5224, 0.6725] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_kb_rag | 0.5546 | 0.0000e+00 | ✅ Yes | [0.4796, 0.6297] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_baseline | 0.2740 | 0.0000e+00 | ✅ Yes | [0.1990, 0.3491] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_kb_rag | 0.3989 | 0.0000e+00 | ✅ Yes | [0.3238, 0.4739] |
| gemma4:31b-cloud_baseline vs qwen3:8b_baseline | 0.6815 | 0.0000e+00 | ✅ Yes | [0.6064, 0.7565] |
| gemma4:31b-cloud_baseline vs qwen3:8b_kb_rag | 0.6809 | 0.0000e+00 | ✅ Yes | [0.6059, 0.7560] |
| gemma4:31b-cloud_kb_rag vs gemma4:31b-mlx_baseline | 0.8059 | 0.0000e+00 | ✅ Yes | [0.7308, 0.8809] |
| gemma4:31b-cloud_kb_rag vs gemma4:31b-mlx_kb_rag | 0.8161 | 0.0000e+00 | ✅ Yes | [0.7411, 0.8912] |
| gemma4:31b-cloud_kb_rag vs gemma4:latest_baseline | 0.7445 | 0.0000e+00 | ✅ Yes | [0.6694, 0.8195] |
| gemma4:31b-cloud_kb_rag vs gemma4:latest_kb_rag | 0.7673 | 0.0000e+00 | ✅ Yes | [0.6922, 0.8424] |
| gemma4:31b-cloud_kb_rag vs gpt-oss:20b_baseline | 0.7374 | 0.0000e+00 | ✅ Yes | [0.6623, 0.8124] |
| gemma4:31b-cloud_kb_rag vs gpt-oss:20b_kb_rag | 0.7620 | 0.0000e+00 | ✅ Yes | [0.6869, 0.8370] |
| gemma4:31b-cloud_kb_rag vs llama3.1:8b_baseline | 0.6829 | 0.0000e+00 | ✅ Yes | [0.6078, 0.7579] |
| gemma4:31b-cloud_kb_rag vs llama3.1:8b_kb_rag | 0.7059 | 0.0000e+00 | ✅ Yes | [0.6309, 0.7810] |
| gemma4:31b-cloud_kb_rag vs llama3.2:latest_baseline | 0.6237 | 0.0000e+00 | ✅ Yes | [0.5486, 0.6988] |
| gemma4:31b-cloud_kb_rag vs llama3.2:latest_kb_rag | 0.6908 | 0.0000e+00 | ✅ Yes | [0.6158, 0.7659] |
| gemma4:31b-cloud_kb_rag vs mistral-nemo:latest_baseline | 0.5975 | 0.0000e+00 | ✅ Yes | [0.5224, 0.6725] |
| gemma4:31b-cloud_kb_rag vs mistral-nemo:latest_kb_rag | 0.5546 | 0.0000e+00 | ✅ Yes | [0.4796, 0.6297] |
| gemma4:31b-cloud_kb_rag vs nemotron-mini:4b_baseline | 0.2740 | 0.0000e+00 | ✅ Yes | [0.1990, 0.3491] |
| gemma4:31b-cloud_kb_rag vs nemotron-mini:4b_kb_rag | 0.3989 | 0.0000e+00 | ✅ Yes | [0.3238, 0.4739] |
| gemma4:31b-cloud_kb_rag vs qwen3:8b_baseline | 0.6815 | 0.0000e+00 | ✅ Yes | [0.6064, 0.7565] |
| gemma4:31b-cloud_kb_rag vs qwen3:8b_kb_rag | 0.6809 | 0.0000e+00 | ✅ Yes | [0.6059, 0.7560] |
| gemma4:31b-mlx_baseline vs gemma4:31b-mlx_kb_rag | 0.0103 | 1.0000e+00 | ❌ No | [-0.0648, 0.0853] |
| gemma4:31b-mlx_baseline vs gemma4:latest_baseline | -0.0614 | 2.9890e-01 | ❌ No | [-0.1365, 0.0136] |
| gemma4:31b-mlx_baseline vs gemma4:latest_kb_rag | -0.0386 | 9.6700e-01 | ❌ No | [-0.1136, 0.0365] |
| gemma4:31b-mlx_baseline vs gpt-oss:20b_baseline | -0.0685 | 1.2990e-01 | ❌ No | [-0.1435, 0.0066] |
| gemma4:31b-mlx_baseline vs gpt-oss:20b_kb_rag | -0.0439 | 8.8750e-01 | ❌ No | [-0.1190, 0.0312] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_baseline | -0.1230 | 0.0000e+00 | ✅ Yes | [-0.1981, -0.0480] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_kb_rag | -0.0999 | 4.0000e-04 | ✅ Yes | [-0.1750, -0.0249] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_baseline | -0.1822 | 0.0000e+00 | ✅ Yes | [-0.2572, -0.1071] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_kb_rag | -0.1150 | 0.0000e+00 | ✅ Yes | [-0.1901, -0.0400] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_baseline | -0.2084 | 0.0000e+00 | ✅ Yes | [-0.2835, -0.1333] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.2513 | 0.0000e+00 | ✅ Yes | [-0.3263, -0.1762] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_baseline | -0.5318 | 0.0000e+00 | ✅ Yes | [-0.6069, -0.4568] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_kb_rag | -0.4070 | 0.0000e+00 | ✅ Yes | [-0.4821, -0.3319] |
| gemma4:31b-mlx_baseline vs qwen3:8b_baseline | -0.1244 | 0.0000e+00 | ✅ Yes | [-0.1995, -0.0493] |
| gemma4:31b-mlx_baseline vs qwen3:8b_kb_rag | -0.1249 | 0.0000e+00 | ✅ Yes | [-0.2000, -0.0499] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_baseline | -0.0717 | 8.3300e-02 | ❌ No | [-0.1467, 0.0034] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0488 | 7.5080e-01 | ❌ No | [-0.1239, 0.0262] |
| gemma4:31b-mlx_kb_rag vs gpt-oss:20b_baseline | -0.0788 | 2.7300e-02 | ✅ Yes | [-0.1538, -0.0037] |
| gemma4:31b-mlx_kb_rag vs gpt-oss:20b_kb_rag | -0.0542 | 5.5630e-01 | ❌ No | [-0.1292, 0.0209] |
| gemma4:31b-mlx_kb_rag vs llama3.1:8b_baseline | -0.1333 | 0.0000e+00 | ✅ Yes | [-0.2083, -0.0582] |
| gemma4:31b-mlx_kb_rag vs llama3.1:8b_kb_rag | -0.1102 | 0.0000e+00 | ✅ Yes | [-0.1853, -0.0351] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_baseline | -0.1924 | 0.0000e+00 | ✅ Yes | [-0.2675, -0.1174] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.1253 | 0.0000e+00 | ✅ Yes | [-0.2004, -0.0502] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.2187 | 0.0000e+00 | ✅ Yes | [-0.2937, -0.1436] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.2615 | 0.0000e+00 | ✅ Yes | [-0.3366, -0.1865] |
| gemma4:31b-mlx_kb_rag vs nemotron-mini:4b_baseline | -0.5421 | 0.0000e+00 | ✅ Yes | [-0.6172, -0.4671] |
| gemma4:31b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | -0.4173 | 0.0000e+00 | ✅ Yes | [-0.4923, -0.3422] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_baseline | -0.1347 | 0.0000e+00 | ✅ Yes | [-0.2097, -0.0596] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.1352 | 0.0000e+00 | ✅ Yes | [-0.2103, -0.0601] |
| gemma4:latest_baseline vs gemma4:latest_kb_rag | 0.0228 | 1.0000e+00 | ❌ No | [-0.0522, 0.0979] |
| gemma4:latest_baseline vs gpt-oss:20b_baseline | -0.0071 | 1.0000e+00 | ❌ No | [-0.0821, 0.0680] |
| gemma4:latest_baseline vs gpt-oss:20b_kb_rag | 0.0175 | 1.0000e+00 | ❌ No | [-0.0575, 0.0926] |
| gemma4:latest_baseline vs llama3.1:8b_baseline | -0.0616 | 2.9300e-01 | ❌ No | [-0.1367, 0.0135] |
| gemma4:latest_baseline vs llama3.1:8b_kb_rag | -0.0385 | 9.6750e-01 | ❌ No | [-0.1136, 0.0365] |
| gemma4:latest_baseline vs llama3.2:latest_baseline | -0.1208 | 0.0000e+00 | ✅ Yes | [-0.1958, -0.0457] |
| gemma4:latest_baseline vs llama3.2:latest_kb_rag | -0.0536 | 5.7760e-01 | ❌ No | [-0.1287, 0.0214] |
| gemma4:latest_baseline vs mistral-nemo:latest_baseline | -0.1470 | 0.0000e+00 | ✅ Yes | [-0.2220, -0.0719] |
| gemma4:latest_baseline vs mistral-nemo:latest_kb_rag | -0.1898 | 0.0000e+00 | ✅ Yes | [-0.2649, -0.1148] |
| gemma4:latest_baseline vs nemotron-mini:4b_baseline | -0.4704 | 0.0000e+00 | ✅ Yes | [-0.5455, -0.3954] |
| gemma4:latest_baseline vs nemotron-mini:4b_kb_rag | -0.3456 | 0.0000e+00 | ✅ Yes | [-0.4206, -0.2705] |
| gemma4:latest_baseline vs qwen3:8b_baseline | -0.0630 | 2.5250e-01 | ❌ No | [-0.1381, 0.0121] |
| gemma4:latest_baseline vs qwen3:8b_kb_rag | -0.0635 | 2.3850e-01 | ❌ No | [-0.1386, 0.0115] |
| gemma4:latest_kb_rag vs gpt-oss:20b_baseline | -0.0299 | 9.9860e-01 | ❌ No | [-0.1050, 0.0451] |
| gemma4:latest_kb_rag vs gpt-oss:20b_kb_rag | -0.0053 | 1.0000e+00 | ❌ No | [-0.0804, 0.0697] |
| gemma4:latest_kb_rag vs llama3.1:8b_baseline | -0.0844 | 9.9000e-03 | ✅ Yes | [-0.1595, -0.0094] |
| gemma4:latest_kb_rag vs llama3.1:8b_kb_rag | -0.0614 | 3.0060e-01 | ❌ No | [-0.1364, 0.0137] |
| gemma4:latest_kb_rag vs llama3.2:latest_baseline | -0.1436 | 0.0000e+00 | ✅ Yes | [-0.2187, -0.0685] |
| gemma4:latest_kb_rag vs llama3.2:latest_kb_rag | -0.0765 | 4.0000e-02 | ✅ Yes | [-0.1515, -0.0014] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_baseline | -0.1698 | 0.0000e+00 | ✅ Yes | [-0.2449, -0.0948] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.2127 | 0.0000e+00 | ✅ Yes | [-0.2877, -0.1376] |
| gemma4:latest_kb_rag vs nemotron-mini:4b_baseline | -0.4933 | 0.0000e+00 | ✅ Yes | [-0.5683, -0.4182] |
| gemma4:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.3684 | 0.0000e+00 | ✅ Yes | [-0.4435, -0.2934] |
| gemma4:latest_kb_rag vs qwen3:8b_baseline | -0.0858 | 7.6000e-03 | ✅ Yes | [-0.1609, -0.0108] |
| gemma4:latest_kb_rag vs qwen3:8b_kb_rag | -0.0864 | 6.8000e-03 | ✅ Yes | [-0.1614, -0.0113] |
| gpt-oss:20b_baseline vs gpt-oss:20b_kb_rag | 0.0246 | 9.9990e-01 | ❌ No | [-0.0505, 0.0996] |
| gpt-oss:20b_baseline vs llama3.1:8b_baseline | -0.0545 | 5.4260e-01 | ❌ No | [-0.1296, 0.0205] |
| gpt-oss:20b_baseline vs llama3.1:8b_kb_rag | -0.0314 | 9.9720e-01 | ❌ No | [-0.1065, 0.0436] |
| gpt-oss:20b_baseline vs llama3.2:latest_baseline | -0.1137 | 0.0000e+00 | ✅ Yes | [-0.1888, -0.0386] |
| gpt-oss:20b_baseline vs llama3.2:latest_kb_rag | -0.0465 | 8.2170e-01 | ❌ No | [-0.1216, 0.0285] |
| gpt-oss:20b_baseline vs mistral-nemo:latest_baseline | -0.1399 | 0.0000e+00 | ✅ Yes | [-0.2150, -0.0649] |
| gpt-oss:20b_baseline vs mistral-nemo:latest_kb_rag | -0.1828 | 0.0000e+00 | ✅ Yes | [-0.2578, -0.1077] |
| gpt-oss:20b_baseline vs nemotron-mini:4b_baseline | -0.4634 | 0.0000e+00 | ✅ Yes | [-0.5384, -0.3883] |
| gpt-oss:20b_baseline vs nemotron-mini:4b_kb_rag | -0.3385 | 0.0000e+00 | ✅ Yes | [-0.4136, -0.2635] |
| gpt-oss:20b_baseline vs qwen3:8b_baseline | -0.0559 | 4.8940e-01 | ❌ No | [-0.1310, 0.0191] |
| gpt-oss:20b_baseline vs qwen3:8b_kb_rag | -0.0564 | 4.7000e-01 | ❌ No | [-0.1315, 0.0186] |
| gpt-oss:20b_kb_rag vs llama3.1:8b_baseline | -0.0791 | 2.5700e-02 | ✅ Yes | [-0.1542, -0.0041] |
| gpt-oss:20b_kb_rag vs llama3.1:8b_kb_rag | -0.0560 | 4.8550e-01 | ❌ No | [-0.1311, 0.0190] |
| gpt-oss:20b_kb_rag vs llama3.2:latest_baseline | -0.1383 | 0.0000e+00 | ✅ Yes | [-0.2133, -0.0632] |
| gpt-oss:20b_kb_rag vs llama3.2:latest_kb_rag | -0.0711 | 9.0200e-02 | ❌ No | [-0.1462, 0.0039] |
| gpt-oss:20b_kb_rag vs mistral-nemo:latest_baseline | -0.1645 | 0.0000e+00 | ✅ Yes | [-0.2396, -0.0894] |
| gpt-oss:20b_kb_rag vs mistral-nemo:latest_kb_rag | -0.2074 | 0.0000e+00 | ✅ Yes | [-0.2824, -0.1323] |
| gpt-oss:20b_kb_rag vs nemotron-mini:4b_baseline | -0.4879 | 0.0000e+00 | ✅ Yes | [-0.5630, -0.4129] |
| gpt-oss:20b_kb_rag vs nemotron-mini:4b_kb_rag | -0.3631 | 0.0000e+00 | ✅ Yes | [-0.4382, -0.2880] |
| gpt-oss:20b_kb_rag vs qwen3:8b_baseline | -0.0805 | 2.0200e-02 | ✅ Yes | [-0.1556, -0.0055] |
| gpt-oss:20b_kb_rag vs qwen3:8b_kb_rag | -0.0810 | 1.8400e-02 | ✅ Yes | [-0.1561, -0.0060] |
| llama3.1:8b_baseline vs llama3.1:8b_kb_rag | 0.0231 | 1.0000e+00 | ❌ No | [-0.0520, 0.0981] |
| llama3.1:8b_baseline vs llama3.2:latest_baseline | -0.0592 | 3.7210e-01 | ❌ No | [-0.1342, 0.0159] |
| llama3.1:8b_baseline vs llama3.2:latest_kb_rag | 0.0080 | 1.0000e+00 | ❌ No | [-0.0671, 0.0830] |
| llama3.1:8b_baseline vs mistral-nemo:latest_baseline | -0.0854 | 8.3000e-03 | ✅ Yes | [-0.1604, -0.0103] |
| llama3.1:8b_baseline vs mistral-nemo:latest_kb_rag | -0.1282 | 0.0000e+00 | ✅ Yes | [-0.2033, -0.0532] |
| llama3.1:8b_baseline vs nemotron-mini:4b_baseline | -0.4088 | 0.0000e+00 | ✅ Yes | [-0.4839, -0.3338] |
| llama3.1:8b_baseline vs nemotron-mini:4b_kb_rag | -0.2840 | 0.0000e+00 | ✅ Yes | [-0.3590, -0.2089] |
| llama3.1:8b_baseline vs qwen3:8b_baseline | -0.0014 | 1.0000e+00 | ❌ No | [-0.0765, 0.0737] |
| llama3.1:8b_baseline vs qwen3:8b_kb_rag | -0.0019 | 1.0000e+00 | ❌ No | [-0.0770, 0.0731] |
| llama3.1:8b_kb_rag vs llama3.2:latest_baseline | -0.0822 | 1.4800e-02 | ✅ Yes | [-0.1573, -0.0072] |
| llama3.1:8b_kb_rag vs llama3.2:latest_kb_rag | -0.0151 | 1.0000e+00 | ❌ No | [-0.0902, 0.0600] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_baseline | -0.1085 | 0.0000e+00 | ✅ Yes | [-0.1835, -0.0334] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_kb_rag | -0.1513 | 0.0000e+00 | ✅ Yes | [-0.2264, -0.0763] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_baseline | -0.4319 | 0.0000e+00 | ✅ Yes | [-0.5070, -0.3569] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_kb_rag | -0.3071 | 0.0000e+00 | ✅ Yes | [-0.3821, -0.2320] |
| llama3.1:8b_kb_rag vs qwen3:8b_baseline | -0.0245 | 9.9990e-01 | ❌ No | [-0.0995, 0.0506] |
| llama3.1:8b_kb_rag vs qwen3:8b_kb_rag | -0.0250 | 9.9990e-01 | ❌ No | [-0.1001, 0.0501] |
| llama3.2:latest_baseline vs llama3.2:latest_kb_rag | 0.0672 | 1.5440e-01 | ❌ No | [-0.0079, 0.1422] |
| llama3.2:latest_baseline vs mistral-nemo:latest_baseline | -0.0262 | 9.9980e-01 | ❌ No | [-0.1013, 0.0488] |
| llama3.2:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0691 | 1.1990e-01 | ❌ No | [-0.1441, 0.0060] |
| llama3.2:latest_baseline vs nemotron-mini:4b_baseline | -0.3497 | 0.0000e+00 | ✅ Yes | [-0.4247, -0.2746] |
| llama3.2:latest_baseline vs nemotron-mini:4b_kb_rag | -0.2248 | 0.0000e+00 | ✅ Yes | [-0.2999, -0.1498] |
| llama3.2:latest_baseline vs qwen3:8b_baseline | 0.0578 | 4.2140e-01 | ❌ No | [-0.0173, 0.1328] |
| llama3.2:latest_baseline vs qwen3:8b_kb_rag | 0.0572 | 4.4020e-01 | ❌ No | [-0.0178, 0.1323] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_baseline | -0.0934 | 1.6000e-03 | ✅ Yes | [-0.1684, -0.0183] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.1362 | 0.0000e+00 | ✅ Yes | [-0.2113, -0.0612] |
| llama3.2:latest_kb_rag vs nemotron-mini:4b_baseline | -0.4168 | 0.0000e+00 | ✅ Yes | [-0.4919, -0.3418] |
| llama3.2:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.2920 | 0.0000e+00 | ✅ Yes | [-0.3670, -0.2169] |
| llama3.2:latest_kb_rag vs qwen3:8b_baseline | -0.0094 | 1.0000e+00 | ❌ No | [-0.0844, 0.0657] |
| llama3.2:latest_kb_rag vs qwen3:8b_kb_rag | -0.0099 | 1.0000e+00 | ❌ No | [-0.0850, 0.0652] |
| mistral-nemo:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0429 | 9.0830e-01 | ❌ No | [-0.1179, 0.0322] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_baseline | -0.3234 | 0.0000e+00 | ✅ Yes | [-0.3985, -0.2484] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_kb_rag | -0.1986 | 0.0000e+00 | ✅ Yes | [-0.2737, -0.1235] |
| mistral-nemo:latest_baseline vs qwen3:8b_baseline | 0.0840 | 1.0700e-02 | ✅ Yes | [0.0089, 0.1590] |
| mistral-nemo:latest_baseline vs qwen3:8b_kb_rag | 0.0835 | 1.1800e-02 | ✅ Yes | [0.0084, 0.1585] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_baseline | -0.2806 | 0.0000e+00 | ✅ Yes | [-0.3556, -0.2055] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.1557 | 0.0000e+00 | ✅ Yes | [-0.2308, -0.0807] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_baseline | 0.1268 | 0.0000e+00 | ✅ Yes | [0.0518, 0.2019] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_kb_rag | 0.1263 | 0.0000e+00 | ✅ Yes | [0.0513, 0.2014] |
| nemotron-mini:4b_baseline vs nemotron-mini:4b_kb_rag | 0.1248 | 0.0000e+00 | ✅ Yes | [0.0498, 0.1999] |
| nemotron-mini:4b_baseline vs qwen3:8b_baseline | 0.4074 | 0.0000e+00 | ✅ Yes | [0.3324, 0.4825] |
| nemotron-mini:4b_baseline vs qwen3:8b_kb_rag | 0.4069 | 0.0000e+00 | ✅ Yes | [0.3319, 0.4820] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_baseline | 0.2826 | 0.0000e+00 | ✅ Yes | [0.2075, 0.3576] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_kb_rag | 0.2821 | 0.0000e+00 | ✅ Yes | [0.2070, 0.3571] |
| qwen3:8b_baseline vs qwen3:8b_kb_rag | -0.0005 | 1.0000e+00 | ❌ No | [-0.0756, 0.0745] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 7 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline | 0.2873 | 0.2865 | -0.0008 | 📉 Decreased |
| deepseek-r1:1.5b_kb_rag | 0.3081 | 0.3095 | +0.0014 | 📈 Improved |
| gemma4:12b-mlx_baseline | 0.7785 | 0.7809 | +0.0024 | 📈 Improved |
| gemma4:12b-mlx_kb_rag | 0.7984 | 0.8003 | +0.0019 | 📈 Improved |
| gemma4:31b-cloud_baseline | 0.0088 | 0.0094 | +0.0006 | 📈 Improved |
| gemma4:31b-cloud_kb_rag | 0.0088 | 0.0094 | +0.0006 | 📈 Improved |
| gemma4:31b-mlx_baseline | 0.8147 | 0.8167 | +0.0020 | 📈 Improved |
| gemma4:31b-mlx_kb_rag | 0.8250 | 0.8269 | +0.0019 | 📈 Improved |
| gemma4:latest_baseline | 0.7533 | 0.7548 | +0.0015 | 📈 Improved |
| gemma4:latest_kb_rag | 0.7761 | 0.7745 | -0.0017 | 📉 Decreased |
| gpt-oss:20b_baseline | 0.7462 | 0.7532 | +0.0070 | 📈 Improved |
| gpt-oss:20b_kb_rag | 0.7708 | 0.7704 | -0.0004 | 📉 Decreased |
| llama3.1:8b_baseline | 0.6917 | 0.6922 | +0.0004 | 📈 Improved |
| llama3.1:8b_kb_rag | 0.7148 | 0.7146 | -0.0002 | 📉 Decreased |
| llama3.2:latest_baseline | 0.6325 | 0.6297 | -0.0028 | 📉 Decreased |
| llama3.2:latest_kb_rag | 0.6997 | 0.6991 | -0.0006 | 📉 Decreased |
| mistral-nemo:latest_baseline | 0.6063 | 0.6067 | +0.0004 | 📈 Improved |
| mistral-nemo:latest_kb_rag | 0.5635 | 0.5595 | -0.0040 | 📉 Decreased |
| nemotron-mini:4b_baseline | 0.2829 | 0.2787 | -0.0041 | 📉 Decreased |
| nemotron-mini:4b_kb_rag | 0.4077 | 0.4062 | -0.0015 | 📉 Decreased |
| qwen3:8b_baseline | 0.6903 | 0.6927 | +0.0024 | 📈 Improved |
| qwen3:8b_kb_rag | 0.6898 | 0.6900 | +0.0002 | 📈 Improved |