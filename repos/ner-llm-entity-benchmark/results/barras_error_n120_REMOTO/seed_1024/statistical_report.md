# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 88.5358
- **p-Value:** 1.0711e-281

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline | 113 | 0.4660 | 0.3879 | 0.5441 | 0.4190 |
| gemma4:31b-cloud_kb_rag | 113 | 0.5466 | 0.4707 | 0.6225 | 0.4070 |
| gemma4:31b-mlx_baseline | 113 | 0.8155 | 0.7895 | 0.8415 | 0.1394 |
| gemma4:31b-mlx_kb_rag | 113 | 0.8239 | 0.7990 | 0.8489 | 0.1339 |
| gemma4:12b-mlx_baseline | 113 | 0.7807 | 0.7543 | 0.8070 | 0.1415 |
| gemma4:12b-mlx_kb_rag | 113 | 0.7979 | 0.7727 | 0.8230 | 0.1350 |
| gemma4:latest_baseline | 113 | 0.7568 | 0.7305 | 0.7831 | 0.1410 |
| gemma4:latest_kb_rag | 113 | 0.7838 | 0.7579 | 0.8098 | 0.1392 |
| qwen3:8b_baseline | 113 | 0.6895 | 0.6599 | 0.7191 | 0.1588 |
| qwen3:8b_kb_rag | 113 | 0.6916 | 0.6634 | 0.7198 | 0.1515 |
| gpt-oss:20b_baseline | 113 | 0.7652 | 0.7378 | 0.7926 | 0.1470 |
| gpt-oss:20b_kb_rag | 113 | 0.7752 | 0.7493 | 0.8011 | 0.1389 |
| mistral-nemo:latest_baseline | 113 | 0.6028 | 0.5684 | 0.6371 | 0.1844 |
| mistral-nemo:latest_kb_rag | 113 | 0.5793 | 0.5467 | 0.6118 | 0.1747 |
| llama3.2:latest_baseline | 113 | 0.6292 | 0.5955 | 0.6629 | 0.1809 |
| llama3.2:latest_kb_rag | 113 | 0.6942 | 0.6643 | 0.7240 | 0.1600 |
| llama3.1:8b_baseline | 113 | 0.6957 | 0.6677 | 0.7238 | 0.1506 |
| llama3.1:8b_kb_rag | 113 | 0.7127 | 0.6833 | 0.7421 | 0.1576 |
| nemotron-mini:4b_baseline | 113 | 0.2834 | 0.2434 | 0.3233 | 0.2142 |
| nemotron-mini:4b_kb_rag | 113 | 0.4132 | 0.3789 | 0.4476 | 0.1843 |
| deepseek-r1:1.5b_baseline | 113 | 0.2910 | 0.2587 | 0.3234 | 0.1735 |
| deepseek-r1:1.5b_kb_rag | 113 | 0.3198 | 0.2874 | 0.3522 | 0.1738 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline vs deepseek-r1:1.5b_kb_rag | 0.0287 | 1.0000e+00 | ❌ No | [-0.0656, 0.1231] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_baseline | 0.4896 | 0.0000e+00 | ✅ Yes | [0.3952, 0.5840] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_kb_rag | 0.5068 | 0.0000e+00 | ✅ Yes | [0.4125, 0.6012] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_baseline | 0.1750 | 0.0000e+00 | ✅ Yes | [0.0806, 0.2694] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_kb_rag | 0.2556 | 0.0000e+00 | ✅ Yes | [0.1612, 0.3499] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_baseline | 0.5244 | 0.0000e+00 | ✅ Yes | [0.4301, 0.6188] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_kb_rag | 0.5329 | 0.0000e+00 | ✅ Yes | [0.4385, 0.6273] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_baseline | 0.4658 | 0.0000e+00 | ✅ Yes | [0.3714, 0.5601] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_kb_rag | 0.4928 | 0.0000e+00 | ✅ Yes | [0.3984, 0.5872] |
| deepseek-r1:1.5b_baseline vs gpt-oss:20b_baseline | 0.4741 | 0.0000e+00 | ✅ Yes | [0.3798, 0.5685] |
| deepseek-r1:1.5b_baseline vs gpt-oss:20b_kb_rag | 0.4842 | 0.0000e+00 | ✅ Yes | [0.3898, 0.5786] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_baseline | 0.4047 | 0.0000e+00 | ✅ Yes | [0.3103, 0.4991] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_kb_rag | 0.4217 | 0.0000e+00 | ✅ Yes | [0.3273, 0.5161] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_baseline | 0.3382 | 0.0000e+00 | ✅ Yes | [0.2438, 0.4325] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_kb_rag | 0.4031 | 0.0000e+00 | ✅ Yes | [0.3087, 0.4975] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_baseline | 0.3117 | 0.0000e+00 | ✅ Yes | [0.2174, 0.4061] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_kb_rag | 0.2882 | 0.0000e+00 | ✅ Yes | [0.1938, 0.3826] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_baseline | -0.0077 | 1.0000e+00 | ❌ No | [-0.1020, 0.0867] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_kb_rag | 0.1222 | 7.0000e-04 | ✅ Yes | [0.0278, 0.2166] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_baseline | 0.3985 | 0.0000e+00 | ✅ Yes | [0.3041, 0.4928] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_kb_rag | 0.4005 | 0.0000e+00 | ✅ Yes | [0.3062, 0.4949] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_baseline | 0.4609 | 0.0000e+00 | ✅ Yes | [0.3665, 0.5552] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_kb_rag | 0.4781 | 0.0000e+00 | ✅ Yes | [0.3837, 0.5725] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-cloud_baseline | 0.1462 | 0.0000e+00 | ✅ Yes | [0.0519, 0.2406] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-cloud_kb_rag | 0.2268 | 0.0000e+00 | ✅ Yes | [0.1324, 0.3212] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-mlx_baseline | 0.4957 | 0.0000e+00 | ✅ Yes | [0.4013, 0.5901] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-mlx_kb_rag | 0.5041 | 0.0000e+00 | ✅ Yes | [0.4098, 0.5985] |
| deepseek-r1:1.5b_kb_rag vs gemma4:latest_baseline | 0.4370 | 0.0000e+00 | ✅ Yes | [0.3426, 0.5314] |
| deepseek-r1:1.5b_kb_rag vs gemma4:latest_kb_rag | 0.4641 | 0.0000e+00 | ✅ Yes | [0.3697, 0.5584] |
| deepseek-r1:1.5b_kb_rag vs gpt-oss:20b_baseline | 0.4454 | 0.0000e+00 | ✅ Yes | [0.3510, 0.5398] |
| deepseek-r1:1.5b_kb_rag vs gpt-oss:20b_kb_rag | 0.4554 | 0.0000e+00 | ✅ Yes | [0.3611, 0.5498] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_baseline | 0.3759 | 0.0000e+00 | ✅ Yes | [0.2816, 0.4703] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_kb_rag | 0.3929 | 0.0000e+00 | ✅ Yes | [0.2986, 0.4873] |
| deepseek-r1:1.5b_kb_rag vs llama3.2:latest_baseline | 0.3094 | 0.0000e+00 | ✅ Yes | [0.2150, 0.4038] |
| deepseek-r1:1.5b_kb_rag vs llama3.2:latest_kb_rag | 0.3744 | 0.0000e+00 | ✅ Yes | [0.2800, 0.4688] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_baseline | 0.2830 | 0.0000e+00 | ✅ Yes | [0.1886, 0.3774] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_kb_rag | 0.2595 | 0.0000e+00 | ✅ Yes | [0.1651, 0.3538] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_baseline | -0.0364 | 9.9910e-01 | ❌ No | [-0.1308, 0.0580] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_kb_rag | 0.0934 | 5.6100e-02 | ❌ No | [-0.0009, 0.1878] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_baseline | 0.3697 | 0.0000e+00 | ✅ Yes | [0.2754, 0.4641] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_kb_rag | 0.3718 | 0.0000e+00 | ✅ Yes | [0.2774, 0.4662] |
| gemma4:12b-mlx_baseline vs gemma4:12b-mlx_kb_rag | 0.0172 | 1.0000e+00 | ❌ No | [-0.0771, 0.1116] |
| gemma4:12b-mlx_baseline vs gemma4:31b-cloud_baseline | -0.3146 | 0.0000e+00 | ✅ Yes | [-0.4090, -0.2203] |
| gemma4:12b-mlx_baseline vs gemma4:31b-cloud_kb_rag | -0.2341 | 0.0000e+00 | ✅ Yes | [-0.3284, -0.1397] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_baseline | 0.0348 | 9.9950e-01 | ❌ No | [-0.0595, 0.1292] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_kb_rag | 0.0433 | 9.9100e-01 | ❌ No | [-0.0511, 0.1376] |
| gemma4:12b-mlx_baseline vs gemma4:latest_baseline | -0.0239 | 1.0000e+00 | ❌ No | [-0.1182, 0.0705] |
| gemma4:12b-mlx_baseline vs gemma4:latest_kb_rag | 0.0032 | 1.0000e+00 | ❌ No | [-0.0912, 0.0976] |
| gemma4:12b-mlx_baseline vs gpt-oss:20b_baseline | -0.0155 | 1.0000e+00 | ❌ No | [-0.1099, 0.0789] |
| gemma4:12b-mlx_baseline vs gpt-oss:20b_kb_rag | -0.0054 | 1.0000e+00 | ❌ No | [-0.0998, 0.0889] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_baseline | -0.0849 | 1.4680e-01 | ❌ No | [-0.1793, 0.0094] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_kb_rag | -0.0679 | 5.6160e-01 | ❌ No | [-0.1623, 0.0264] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_baseline | -0.1515 | 0.0000e+00 | ✅ Yes | [-0.2458, -0.0571] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_kb_rag | -0.0865 | 1.2460e-01 | ❌ No | [-0.1809, 0.0079] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_baseline | -0.1779 | 0.0000e+00 | ✅ Yes | [-0.2722, -0.0835] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.2014 | 0.0000e+00 | ✅ Yes | [-0.2958, -0.1070] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_baseline | -0.4973 | 0.0000e+00 | ✅ Yes | [-0.5917, -0.4029] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_kb_rag | -0.3674 | 0.0000e+00 | ✅ Yes | [-0.4618, -0.2731] |
| gemma4:12b-mlx_baseline vs qwen3:8b_baseline | -0.0911 | 7.4000e-02 | ❌ No | [-0.1855, 0.0032] |
| gemma4:12b-mlx_baseline vs qwen3:8b_kb_rag | -0.0891 | 9.4000e-02 | ❌ No | [-0.1834, 0.0053] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-cloud_baseline | -0.3319 | 0.0000e+00 | ✅ Yes | [-0.4262, -0.2375] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-cloud_kb_rag | -0.2513 | 0.0000e+00 | ✅ Yes | [-0.3457, -0.1569] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_baseline | 0.0176 | 1.0000e+00 | ❌ No | [-0.0768, 0.1120] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_kb_rag | 0.0260 | 1.0000e+00 | ❌ No | [-0.0683, 0.1204] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_baseline | -0.0411 | 9.9530e-01 | ❌ No | [-0.1355, 0.0533] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0140 | 1.0000e+00 | ❌ No | [-0.1084, 0.0803] |
| gemma4:12b-mlx_kb_rag vs gpt-oss:20b_baseline | -0.0327 | 9.9980e-01 | ❌ No | [-0.1271, 0.0617] |
| gemma4:12b-mlx_kb_rag vs gpt-oss:20b_kb_rag | -0.0227 | 1.0000e+00 | ❌ No | [-0.1170, 0.0717] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_baseline | -0.1022 | 1.7700e-02 | ✅ Yes | [-0.1965, -0.0078] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_kb_rag | -0.0852 | 1.4330e-01 | ❌ No | [-0.1795, 0.0092] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_baseline | -0.1687 | 0.0000e+00 | ✅ Yes | [-0.2631, -0.0743] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.1037 | 1.4100e-02 | ✅ Yes | [-0.1981, -0.0093] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.1951 | 0.0000e+00 | ✅ Yes | [-0.2895, -0.1007] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.2186 | 0.0000e+00 | ✅ Yes | [-0.3130, -0.1243] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_baseline | -0.5145 | 0.0000e+00 | ✅ Yes | [-0.6089, -0.4201] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | -0.3847 | 0.0000e+00 | ✅ Yes | [-0.4790, -0.2903] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_baseline | -0.1084 | 7.1000e-03 | ✅ Yes | [-0.2027, -0.0140] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.1063 | 9.7000e-03 | ✅ Yes | [-0.2007, -0.0119] |
| gemma4:31b-cloud_baseline vs gemma4:31b-cloud_kb_rag | 0.0806 | 2.2370e-01 | ❌ No | [-0.0138, 0.1749] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_baseline | 0.3495 | 0.0000e+00 | ✅ Yes | [0.2551, 0.4438] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_kb_rag | 0.3579 | 0.0000e+00 | ✅ Yes | [0.2635, 0.4523] |
| gemma4:31b-cloud_baseline vs gemma4:latest_baseline | 0.2908 | 0.0000e+00 | ✅ Yes | [0.1964, 0.3851] |
| gemma4:31b-cloud_baseline vs gemma4:latest_kb_rag | 0.3178 | 0.0000e+00 | ✅ Yes | [0.2234, 0.4122] |
| gemma4:31b-cloud_baseline vs gpt-oss:20b_baseline | 0.2991 | 0.0000e+00 | ✅ Yes | [0.2048, 0.3935] |
| gemma4:31b-cloud_baseline vs gpt-oss:20b_kb_rag | 0.3092 | 0.0000e+00 | ✅ Yes | [0.2148, 0.4036] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_baseline | 0.2297 | 0.0000e+00 | ✅ Yes | [0.1353, 0.3241] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_kb_rag | 0.2467 | 0.0000e+00 | ✅ Yes | [0.1523, 0.3411] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_baseline | 0.1632 | 0.0000e+00 | ✅ Yes | [0.0688, 0.2575] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_kb_rag | 0.2281 | 0.0000e+00 | ✅ Yes | [0.1338, 0.3225] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_baseline | 0.1368 | 0.0000e+00 | ✅ Yes | [0.0424, 0.2311] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_kb_rag | 0.1132 | 3.3000e-03 | ✅ Yes | [0.0189, 0.2076] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_baseline | -0.1827 | 0.0000e+00 | ✅ Yes | [-0.2770, -0.0883] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_kb_rag | -0.0528 | 9.2370e-01 | ❌ No | [-0.1472, 0.0416] |
| gemma4:31b-cloud_baseline vs qwen3:8b_baseline | 0.2235 | 0.0000e+00 | ✅ Yes | [0.1291, 0.3179] |
| gemma4:31b-cloud_baseline vs qwen3:8b_kb_rag | 0.2256 | 0.0000e+00 | ✅ Yes | [0.1312, 0.3199] |
| gemma4:31b-cloud_kb_rag vs gemma4:31b-mlx_baseline | 0.2689 | 0.0000e+00 | ✅ Yes | [0.1745, 0.3633] |
| gemma4:31b-cloud_kb_rag vs gemma4:31b-mlx_kb_rag | 0.2773 | 0.0000e+00 | ✅ Yes | [0.1830, 0.3717] |
| gemma4:31b-cloud_kb_rag vs gemma4:latest_baseline | 0.2102 | 0.0000e+00 | ✅ Yes | [0.1158, 0.3046] |
| gemma4:31b-cloud_kb_rag vs gemma4:latest_kb_rag | 0.2372 | 0.0000e+00 | ✅ Yes | [0.1429, 0.3316] |
| gemma4:31b-cloud_kb_rag vs gpt-oss:20b_baseline | 0.2186 | 0.0000e+00 | ✅ Yes | [0.1242, 0.3129] |
| gemma4:31b-cloud_kb_rag vs gpt-oss:20b_kb_rag | 0.2286 | 0.0000e+00 | ✅ Yes | [0.1343, 0.3230] |
| gemma4:31b-cloud_kb_rag vs llama3.1:8b_baseline | 0.1491 | 0.0000e+00 | ✅ Yes | [0.0548, 0.2435] |
| gemma4:31b-cloud_kb_rag vs llama3.1:8b_kb_rag | 0.1661 | 0.0000e+00 | ✅ Yes | [0.0717, 0.2605] |
| gemma4:31b-cloud_kb_rag vs llama3.2:latest_baseline | 0.0826 | 1.8500e-01 | ❌ No | [-0.0118, 0.1770] |
| gemma4:31b-cloud_kb_rag vs llama3.2:latest_kb_rag | 0.1476 | 0.0000e+00 | ✅ Yes | [0.0532, 0.2419] |
| gemma4:31b-cloud_kb_rag vs mistral-nemo:latest_baseline | 0.0562 | 8.6970e-01 | ❌ No | [-0.0382, 0.1506] |
| gemma4:31b-cloud_kb_rag vs mistral-nemo:latest_kb_rag | 0.0327 | 9.9980e-01 | ❌ No | [-0.0617, 0.1270] |
| gemma4:31b-cloud_kb_rag vs nemotron-mini:4b_baseline | -0.2632 | 0.0000e+00 | ✅ Yes | [-0.3576, -0.1689] |
| gemma4:31b-cloud_kb_rag vs nemotron-mini:4b_kb_rag | -0.1334 | 1.0000e-04 | ✅ Yes | [-0.2277, -0.0390] |
| gemma4:31b-cloud_kb_rag vs qwen3:8b_baseline | 0.1429 | 0.0000e+00 | ✅ Yes | [0.0485, 0.2373] |
| gemma4:31b-cloud_kb_rag vs qwen3:8b_kb_rag | 0.1450 | 0.0000e+00 | ✅ Yes | [0.0506, 0.2394] |
| gemma4:31b-mlx_baseline vs gemma4:31b-mlx_kb_rag | 0.0084 | 1.0000e+00 | ❌ No | [-0.0859, 0.1028] |
| gemma4:31b-mlx_baseline vs gemma4:latest_baseline | -0.0587 | 8.1770e-01 | ❌ No | [-0.1531, 0.0357] |
| gemma4:31b-mlx_baseline vs gemma4:latest_kb_rag | -0.0316 | 9.9990e-01 | ❌ No | [-0.1260, 0.0627] |
| gemma4:31b-mlx_baseline vs gpt-oss:20b_baseline | -0.0503 | 9.5190e-01 | ❌ No | [-0.1447, 0.0441] |
| gemma4:31b-mlx_baseline vs gpt-oss:20b_kb_rag | -0.0403 | 9.9640e-01 | ❌ No | [-0.1346, 0.0541] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_baseline | -0.1198 | 1.1000e-03 | ✅ Yes | [-0.2141, -0.0254] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_kb_rag | -0.1028 | 1.6200e-02 | ✅ Yes | [-0.1971, -0.0084] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_baseline | -0.1863 | 0.0000e+00 | ✅ Yes | [-0.2807, -0.0919] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_kb_rag | -0.1213 | 8.0000e-04 | ✅ Yes | [-0.2157, -0.0270] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_baseline | -0.2127 | 0.0000e+00 | ✅ Yes | [-0.3071, -0.1183] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.2362 | 0.0000e+00 | ✅ Yes | [-0.3306, -0.1419] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_baseline | -0.5321 | 0.0000e+00 | ✅ Yes | [-0.6265, -0.4377] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_kb_rag | -0.4023 | 0.0000e+00 | ✅ Yes | [-0.4966, -0.3079] |
| gemma4:31b-mlx_baseline vs qwen3:8b_baseline | -0.1260 | 4.0000e-04 | ✅ Yes | [-0.2203, -0.0316] |
| gemma4:31b-mlx_baseline vs qwen3:8b_kb_rag | -0.1239 | 5.0000e-04 | ✅ Yes | [-0.2183, -0.0295] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_baseline | -0.0671 | 5.8590e-01 | ❌ No | [-0.1615, 0.0272] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0401 | 9.9660e-01 | ❌ No | [-0.1345, 0.0543] |
| gemma4:31b-mlx_kb_rag vs gpt-oss:20b_baseline | -0.0588 | 8.1620e-01 | ❌ No | [-0.1531, 0.0356] |
| gemma4:31b-mlx_kb_rag vs gpt-oss:20b_kb_rag | -0.0487 | 9.6550e-01 | ❌ No | [-0.1431, 0.0457] |
| gemma4:31b-mlx_kb_rag vs llama3.1:8b_baseline | -0.1282 | 2.0000e-04 | ✅ Yes | [-0.2226, -0.0338] |
| gemma4:31b-mlx_kb_rag vs llama3.1:8b_kb_rag | -0.1112 | 4.5000e-03 | ✅ Yes | [-0.2056, -0.0168] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_baseline | -0.1947 | 0.0000e+00 | ✅ Yes | [-0.2891, -0.1004] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.1298 | 2.0000e-04 | ✅ Yes | [-0.2241, -0.0354] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.2212 | 0.0000e+00 | ✅ Yes | [-0.3155, -0.1268] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.2447 | 0.0000e+00 | ✅ Yes | [-0.3391, -0.1503] |
| gemma4:31b-mlx_kb_rag vs nemotron-mini:4b_baseline | -0.5406 | 0.0000e+00 | ✅ Yes | [-0.6349, -0.4462] |
| gemma4:31b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | -0.4107 | 0.0000e+00 | ✅ Yes | [-0.5051, -0.3163] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_baseline | -0.1344 | 1.0000e-04 | ✅ Yes | [-0.2288, -0.0400] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.1323 | 1.0000e-04 | ✅ Yes | [-0.2267, -0.0380] |
| gemma4:latest_baseline vs gemma4:latest_kb_rag | 0.0270 | 1.0000e+00 | ❌ No | [-0.0673, 0.1214] |
| gemma4:latest_baseline vs gpt-oss:20b_baseline | 0.0084 | 1.0000e+00 | ❌ No | [-0.0860, 0.1028] |
| gemma4:latest_baseline vs gpt-oss:20b_kb_rag | 0.0184 | 1.0000e+00 | ❌ No | [-0.0759, 0.1128] |
| gemma4:latest_baseline vs llama3.1:8b_baseline | -0.0611 | 7.5980e-01 | ❌ No | [-0.1554, 0.0333] |
| gemma4:latest_baseline vs llama3.1:8b_kb_rag | -0.0441 | 9.8880e-01 | ❌ No | [-0.1384, 0.0503] |
| gemma4:latest_baseline vs llama3.2:latest_baseline | -0.1276 | 3.0000e-04 | ✅ Yes | [-0.2220, -0.0332] |
| gemma4:latest_baseline vs llama3.2:latest_kb_rag | -0.0626 | 7.1780e-01 | ❌ No | [-0.1570, 0.0317] |
| gemma4:latest_baseline vs mistral-nemo:latest_baseline | -0.1540 | 0.0000e+00 | ✅ Yes | [-0.2484, -0.0596] |
| gemma4:latest_baseline vs mistral-nemo:latest_kb_rag | -0.1775 | 0.0000e+00 | ✅ Yes | [-0.2719, -0.0832] |
| gemma4:latest_baseline vs nemotron-mini:4b_baseline | -0.4734 | 0.0000e+00 | ✅ Yes | [-0.5678, -0.3791] |
| gemma4:latest_baseline vs nemotron-mini:4b_kb_rag | -0.3436 | 0.0000e+00 | ✅ Yes | [-0.4379, -0.2492] |
| gemma4:latest_baseline vs qwen3:8b_baseline | -0.0673 | 5.8150e-01 | ❌ No | [-0.1617, 0.0271] |
| gemma4:latest_baseline vs qwen3:8b_kb_rag | -0.0652 | 6.4380e-01 | ❌ No | [-0.1596, 0.0292] |
| gemma4:latest_kb_rag vs gpt-oss:20b_baseline | -0.0187 | 1.0000e+00 | ❌ No | [-0.1130, 0.0757] |
| gemma4:latest_kb_rag vs gpt-oss:20b_kb_rag | -0.0086 | 1.0000e+00 | ❌ No | [-0.1030, 0.0858] |
| gemma4:latest_kb_rag vs llama3.1:8b_baseline | -0.0881 | 1.0460e-01 | ❌ No | [-0.1825, 0.0063] |
| gemma4:latest_kb_rag vs llama3.1:8b_kb_rag | -0.0711 | 4.6550e-01 | ❌ No | [-0.1655, 0.0233] |
| gemma4:latest_kb_rag vs llama3.2:latest_baseline | -0.1546 | 0.0000e+00 | ✅ Yes | [-0.2490, -0.0603] |
| gemma4:latest_kb_rag vs llama3.2:latest_kb_rag | -0.0897 | 8.7700e-02 | ❌ No | [-0.1841, 0.0047] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_baseline | -0.1811 | 0.0000e+00 | ✅ Yes | [-0.2754, -0.0867] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.2046 | 0.0000e+00 | ✅ Yes | [-0.2990, -0.1102] |
| gemma4:latest_kb_rag vs nemotron-mini:4b_baseline | -0.5005 | 0.0000e+00 | ✅ Yes | [-0.5948, -0.4061] |
| gemma4:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.3706 | 0.0000e+00 | ✅ Yes | [-0.4650, -0.2762] |
| gemma4:latest_kb_rag vs qwen3:8b_baseline | -0.0943 | 5.0300e-02 | ❌ No | [-0.1887, 0.0000] |
| gemma4:latest_kb_rag vs qwen3:8b_kb_rag | -0.0923 | 6.4900e-02 | ❌ No | [-0.1866, 0.0021] |
| gpt-oss:20b_baseline vs gpt-oss:20b_kb_rag | 0.0101 | 1.0000e+00 | ❌ No | [-0.0843, 0.1044] |
| gpt-oss:20b_baseline vs llama3.1:8b_baseline | -0.0694 | 5.1560e-01 | ❌ No | [-0.1638, 0.0249] |
| gpt-oss:20b_baseline vs llama3.1:8b_kb_rag | -0.0525 | 9.2820e-01 | ❌ No | [-0.1468, 0.0419] |
| gpt-oss:20b_baseline vs llama3.2:latest_baseline | -0.1360 | 1.0000e-04 | ✅ Yes | [-0.2303, -0.0416] |
| gpt-oss:20b_baseline vs llama3.2:latest_kb_rag | -0.0710 | 4.6860e-01 | ❌ No | [-0.1654, 0.0234] |
| gpt-oss:20b_baseline vs mistral-nemo:latest_baseline | -0.1624 | 0.0000e+00 | ✅ Yes | [-0.2568, -0.0680] |
| gpt-oss:20b_baseline vs mistral-nemo:latest_kb_rag | -0.1859 | 0.0000e+00 | ✅ Yes | [-0.2803, -0.0915] |
| gpt-oss:20b_baseline vs nemotron-mini:4b_baseline | -0.4818 | 0.0000e+00 | ✅ Yes | [-0.5762, -0.3874] |
| gpt-oss:20b_baseline vs nemotron-mini:4b_kb_rag | -0.3519 | 0.0000e+00 | ✅ Yes | [-0.4463, -0.2576] |
| gpt-oss:20b_baseline vs qwen3:8b_baseline | -0.0757 | 3.3800e-01 | ❌ No | [-0.1700, 0.0187] |
| gpt-oss:20b_baseline vs qwen3:8b_kb_rag | -0.0736 | 3.9410e-01 | ❌ No | [-0.1680, 0.0208] |
| gpt-oss:20b_kb_rag vs llama3.1:8b_baseline | -0.0795 | 2.4610e-01 | ❌ No | [-0.1739, 0.0149] |
| gpt-oss:20b_kb_rag vs llama3.1:8b_kb_rag | -0.0625 | 7.2120e-01 | ❌ No | [-0.1569, 0.0319] |
| gpt-oss:20b_kb_rag vs llama3.2:latest_baseline | -0.1460 | 0.0000e+00 | ✅ Yes | [-0.2404, -0.0517] |
| gpt-oss:20b_kb_rag vs llama3.2:latest_kb_rag | -0.0811 | 2.1370e-01 | ❌ No | [-0.1754, 0.0133] |
| gpt-oss:20b_kb_rag vs mistral-nemo:latest_baseline | -0.1725 | 0.0000e+00 | ✅ Yes | [-0.2668, -0.0781] |
| gpt-oss:20b_kb_rag vs mistral-nemo:latest_kb_rag | -0.1960 | 0.0000e+00 | ✅ Yes | [-0.2904, -0.1016] |
| gpt-oss:20b_kb_rag vs nemotron-mini:4b_baseline | -0.4919 | 0.0000e+00 | ✅ Yes | [-0.5862, -0.3975] |
| gpt-oss:20b_kb_rag vs nemotron-mini:4b_kb_rag | -0.3620 | 0.0000e+00 | ✅ Yes | [-0.4564, -0.2676] |
| gpt-oss:20b_kb_rag vs qwen3:8b_baseline | -0.0857 | 1.3530e-01 | ❌ No | [-0.1801, 0.0087] |
| gpt-oss:20b_kb_rag vs qwen3:8b_kb_rag | -0.0836 | 1.6710e-01 | ❌ No | [-0.1780, 0.0107] |
| llama3.1:8b_baseline vs llama3.1:8b_kb_rag | 0.0170 | 1.0000e+00 | ❌ No | [-0.0774, 0.1114] |
| llama3.1:8b_baseline vs llama3.2:latest_baseline | -0.0665 | 6.0430e-01 | ❌ No | [-0.1609, 0.0278] |
| llama3.1:8b_baseline vs llama3.2:latest_kb_rag | -0.0016 | 1.0000e+00 | ❌ No | [-0.0959, 0.0928] |
| llama3.1:8b_baseline vs mistral-nemo:latest_baseline | -0.0929 | 5.9600e-02 | ❌ No | [-0.1873, 0.0014] |
| llama3.1:8b_baseline vs mistral-nemo:latest_kb_rag | -0.1165 | 1.9000e-03 | ✅ Yes | [-0.2108, -0.0221] |
| llama3.1:8b_baseline vs nemotron-mini:4b_baseline | -0.4124 | 0.0000e+00 | ✅ Yes | [-0.5067, -0.3180] |
| llama3.1:8b_baseline vs nemotron-mini:4b_kb_rag | -0.2825 | 0.0000e+00 | ✅ Yes | [-0.3769, -0.1881] |
| llama3.1:8b_baseline vs qwen3:8b_baseline | -0.0062 | 1.0000e+00 | ❌ No | [-0.1006, 0.0882] |
| llama3.1:8b_baseline vs qwen3:8b_kb_rag | -0.0041 | 1.0000e+00 | ❌ No | [-0.0985, 0.0902] |
| llama3.1:8b_kb_rag vs llama3.2:latest_baseline | -0.0835 | 1.6910e-01 | ❌ No | [-0.1779, 0.0109] |
| llama3.1:8b_kb_rag vs llama3.2:latest_kb_rag | -0.0186 | 1.0000e+00 | ❌ No | [-0.1129, 0.0758] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_baseline | -0.1099 | 5.5000e-03 | ✅ Yes | [-0.2043, -0.0156] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_kb_rag | -0.1335 | 1.0000e-04 | ✅ Yes | [-0.2278, -0.0391] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_baseline | -0.4294 | 0.0000e+00 | ✅ Yes | [-0.5237, -0.3350] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_kb_rag | -0.2995 | 0.0000e+00 | ✅ Yes | [-0.3939, -0.2051] |
| llama3.1:8b_kb_rag vs qwen3:8b_baseline | -0.0232 | 1.0000e+00 | ❌ No | [-0.1176, 0.0712] |
| llama3.1:8b_kb_rag vs qwen3:8b_kb_rag | -0.0211 | 1.0000e+00 | ❌ No | [-0.1155, 0.0732] |
| llama3.2:latest_baseline vs llama3.2:latest_kb_rag | 0.0650 | 6.5110e-01 | ❌ No | [-0.0294, 0.1593] |
| llama3.2:latest_baseline vs mistral-nemo:latest_baseline | -0.0264 | 1.0000e+00 | ❌ No | [-0.1208, 0.0680] |
| llama3.2:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0499 | 9.5530e-01 | ❌ No | [-0.1443, 0.0444] |
| llama3.2:latest_baseline vs nemotron-mini:4b_baseline | -0.3458 | 0.0000e+00 | ✅ Yes | [-0.4402, -0.2515] |
| llama3.2:latest_baseline vs nemotron-mini:4b_kb_rag | -0.2160 | 0.0000e+00 | ✅ Yes | [-0.3103, -0.1216] |
| llama3.2:latest_baseline vs qwen3:8b_baseline | 0.0603 | 7.7900e-01 | ❌ No | [-0.0341, 0.1547] |
| llama3.2:latest_baseline vs qwen3:8b_kb_rag | 0.0624 | 7.2460e-01 | ❌ No | [-0.0320, 0.1568] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_baseline | -0.0914 | 7.2000e-02 | ❌ No | [-0.1858, 0.0030] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.1149 | 2.5000e-03 | ✅ Yes | [-0.2093, -0.0205] |
| llama3.2:latest_kb_rag vs nemotron-mini:4b_baseline | -0.4108 | 0.0000e+00 | ✅ Yes | [-0.5052, -0.3164] |
| llama3.2:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.2809 | 0.0000e+00 | ✅ Yes | [-0.3753, -0.1866] |
| llama3.2:latest_kb_rag vs qwen3:8b_baseline | -0.0046 | 1.0000e+00 | ❌ No | [-0.0990, 0.0897] |
| llama3.2:latest_kb_rag vs qwen3:8b_kb_rag | -0.0026 | 1.0000e+00 | ❌ No | [-0.0969, 0.0918] |
| mistral-nemo:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0235 | 1.0000e+00 | ❌ No | [-0.1179, 0.0708] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_baseline | -0.3194 | 0.0000e+00 | ✅ Yes | [-0.4138, -0.2250] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_kb_rag | -0.1896 | 0.0000e+00 | ✅ Yes | [-0.2839, -0.0952] |
| mistral-nemo:latest_baseline vs qwen3:8b_baseline | 0.0867 | 1.2150e-01 | ❌ No | [-0.0076, 0.1811] |
| mistral-nemo:latest_baseline vs qwen3:8b_kb_rag | 0.0888 | 9.6800e-02 | ❌ No | [-0.0056, 0.1832] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_baseline | -0.2959 | 0.0000e+00 | ✅ Yes | [-0.3903, -0.2015] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.1660 | 0.0000e+00 | ✅ Yes | [-0.2604, -0.0717] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_baseline | 0.1103 | 5.3000e-03 | ✅ Yes | [0.0159, 0.2046] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_kb_rag | 0.1123 | 3.8000e-03 | ✅ Yes | [0.0180, 0.2067] |
| nemotron-mini:4b_baseline vs nemotron-mini:4b_kb_rag | 0.1299 | 2.0000e-04 | ✅ Yes | [0.0355, 0.2242] |
| nemotron-mini:4b_baseline vs qwen3:8b_baseline | 0.4061 | 0.0000e+00 | ✅ Yes | [0.3118, 0.5005] |
| nemotron-mini:4b_baseline vs qwen3:8b_kb_rag | 0.4082 | 0.0000e+00 | ✅ Yes | [0.3138, 0.5026] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_baseline | 0.2763 | 0.0000e+00 | ✅ Yes | [0.1819, 0.3707] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_kb_rag | 0.2784 | 0.0000e+00 | ✅ Yes | [0.1840, 0.3727] |
| qwen3:8b_baseline vs qwen3:8b_kb_rag | 0.0021 | 1.0000e+00 | ❌ No | [-0.0923, 0.0964] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 7 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline | 0.2910 | 0.2853 | -0.0057 | 📉 Decreased |
| deepseek-r1:1.5b_kb_rag | 0.3198 | 0.3189 | -0.0008 | 📉 Decreased |
| gemma4:12b-mlx_baseline | 0.7807 | 0.7830 | +0.0024 | 📈 Improved |
| gemma4:12b-mlx_kb_rag | 0.7979 | 0.8000 | +0.0021 | 📈 Improved |
| gemma4:31b-cloud_baseline | 0.4660 | 0.4669 | +0.0009 | 📈 Improved |
| gemma4:31b-cloud_kb_rag | 0.5466 | 0.5395 | -0.0071 | 📉 Decreased |
| gemma4:31b-mlx_baseline | 0.8155 | 0.8177 | +0.0022 | 📈 Improved |
| gemma4:31b-mlx_kb_rag | 0.8239 | 0.8257 | +0.0018 | 📈 Improved |
| gemma4:latest_baseline | 0.7568 | 0.7556 | -0.0012 | 📉 Decreased |
| gemma4:latest_kb_rag | 0.7838 | 0.7851 | +0.0012 | 📈 Improved |
| gpt-oss:20b_baseline | 0.7652 | 0.7667 | +0.0016 | 📈 Improved |
| gpt-oss:20b_kb_rag | 0.7752 | 0.7776 | +0.0023 | 📈 Improved |
| llama3.1:8b_baseline | 0.6957 | 0.6965 | +0.0008 | 📈 Improved |
| llama3.1:8b_kb_rag | 0.7127 | 0.7116 | -0.0011 | 📉 Decreased |
| llama3.2:latest_baseline | 0.6292 | 0.6232 | -0.0060 | 📉 Decreased |
| llama3.2:latest_kb_rag | 0.6942 | 0.6941 | -0.0001 | ⚖️ Stable |
| mistral-nemo:latest_baseline | 0.6028 | 0.6040 | +0.0012 | 📈 Improved |
| mistral-nemo:latest_kb_rag | 0.5793 | 0.5773 | -0.0020 | 📉 Decreased |
| nemotron-mini:4b_baseline | 0.2834 | 0.2766 | -0.0067 | 📉 Decreased |
| nemotron-mini:4b_kb_rag | 0.4132 | 0.4143 | +0.0010 | 📈 Improved |
| qwen3:8b_baseline | 0.6895 | 0.6918 | +0.0023 | 📈 Improved |
| qwen3:8b_kb_rag | 0.6916 | 0.6921 | +0.0005 | 📈 Improved |