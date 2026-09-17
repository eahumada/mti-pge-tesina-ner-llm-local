# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 91.1717
- **p-Value:** 1.9546e-288

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline | 113 | 0.4038 | 0.3247 | 0.4829 | 0.4244 |
| gemma4:31b-cloud_kb_rag | 113 | 0.5119 | 0.4349 | 0.5888 | 0.4127 |
| gemma4:31b-mlx_baseline | 113 | 0.8150 | 0.7888 | 0.8411 | 0.1402 |
| gemma4:31b-mlx_kb_rag | 113 | 0.8251 | 0.8004 | 0.8499 | 0.1327 |
| gemma4:12b-mlx_baseline | 113 | 0.7794 | 0.7530 | 0.8058 | 0.1415 |
| gemma4:12b-mlx_kb_rag | 113 | 0.7981 | 0.7728 | 0.8234 | 0.1358 |
| gemma4:latest_baseline | 113 | 0.7451 | 0.7170 | 0.7731 | 0.1505 |
| gemma4:latest_kb_rag | 113 | 0.7829 | 0.7576 | 0.8083 | 0.1360 |
| qwen3:8b_baseline | 113 | 0.6884 | 0.6587 | 0.7180 | 0.1590 |
| qwen3:8b_kb_rag | 113 | 0.6923 | 0.6640 | 0.7205 | 0.1517 |
| gpt-oss:20b_baseline | 113 | 0.7613 | 0.7352 | 0.7874 | 0.1400 |
| gpt-oss:20b_kb_rag | 113 | 0.7759 | 0.7508 | 0.8010 | 0.1347 |
| mistral-nemo:latest_baseline | 113 | 0.5961 | 0.5618 | 0.6303 | 0.1837 |
| mistral-nemo:latest_kb_rag | 113 | 0.5727 | 0.5374 | 0.6080 | 0.1895 |
| llama3.2:latest_baseline | 113 | 0.6167 | 0.5835 | 0.6499 | 0.1782 |
| llama3.2:latest_kb_rag | 113 | 0.6976 | 0.6671 | 0.7281 | 0.1636 |
| llama3.1:8b_baseline | 113 | 0.6978 | 0.6688 | 0.7268 | 0.1558 |
| llama3.1:8b_kb_rag | 113 | 0.7201 | 0.6907 | 0.7494 | 0.1574 |
| nemotron-mini:4b_baseline | 113 | 0.2734 | 0.2346 | 0.3122 | 0.2083 |
| nemotron-mini:4b_kb_rag | 113 | 0.4177 | 0.3850 | 0.4503 | 0.1751 |
| deepseek-r1:1.5b_baseline | 113 | 0.2961 | 0.2630 | 0.3291 | 0.1774 |
| deepseek-r1:1.5b_kb_rag | 113 | 0.3196 | 0.2839 | 0.3553 | 0.1917 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline vs deepseek-r1:1.5b_kb_rag | 0.0235 | 1.0000e+00 | ❌ No | [-0.0718, 0.1188] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_baseline | 0.4833 | 0.0000e+00 | ✅ Yes | [0.3880, 0.5786] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_kb_rag | 0.5020 | 0.0000e+00 | ✅ Yes | [0.4067, 0.5974] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_baseline | 0.1077 | 9.1000e-03 | ✅ Yes | [0.0124, 0.2031] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_kb_rag | 0.2158 | 0.0000e+00 | ✅ Yes | [0.1205, 0.3111] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_baseline | 0.5189 | 0.0000e+00 | ✅ Yes | [0.4236, 0.6142] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_kb_rag | 0.5291 | 0.0000e+00 | ✅ Yes | [0.4338, 0.6244] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_baseline | 0.4490 | 0.0000e+00 | ✅ Yes | [0.3537, 0.5443] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_kb_rag | 0.4869 | 0.0000e+00 | ✅ Yes | [0.3915, 0.5822] |
| deepseek-r1:1.5b_baseline vs gpt-oss:20b_baseline | 0.4652 | 0.0000e+00 | ✅ Yes | [0.3699, 0.5605] |
| deepseek-r1:1.5b_baseline vs gpt-oss:20b_kb_rag | 0.4798 | 0.0000e+00 | ✅ Yes | [0.3845, 0.5752] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_baseline | 0.4017 | 0.0000e+00 | ✅ Yes | [0.3064, 0.4970] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_kb_rag | 0.4240 | 0.0000e+00 | ✅ Yes | [0.3287, 0.5193] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_baseline | 0.3206 | 0.0000e+00 | ✅ Yes | [0.2253, 0.4159] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_kb_rag | 0.4015 | 0.0000e+00 | ✅ Yes | [0.3062, 0.4968] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_baseline | 0.3000 | 0.0000e+00 | ✅ Yes | [0.2047, 0.3953] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_kb_rag | 0.2766 | 0.0000e+00 | ✅ Yes | [0.1813, 0.3719] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_baseline | -0.0227 | 1.0000e+00 | ❌ No | [-0.1180, 0.0726] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_kb_rag | 0.1216 | 1.0000e-03 | ✅ Yes | [0.0263, 0.2169] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_baseline | 0.3923 | 0.0000e+00 | ✅ Yes | [0.2970, 0.4876] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_kb_rag | 0.3962 | 0.0000e+00 | ✅ Yes | [0.3009, 0.4915] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_baseline | 0.4598 | 0.0000e+00 | ✅ Yes | [0.3645, 0.5551] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_kb_rag | 0.4785 | 0.0000e+00 | ✅ Yes | [0.3832, 0.5738] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-cloud_baseline | 0.0842 | 1.7140e-01 | ❌ No | [-0.0111, 0.1795] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-cloud_kb_rag | 0.1923 | 0.0000e+00 | ✅ Yes | [0.0970, 0.2876] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-mlx_baseline | 0.4954 | 0.0000e+00 | ✅ Yes | [0.4001, 0.5907] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-mlx_kb_rag | 0.5055 | 0.0000e+00 | ✅ Yes | [0.4102, 0.6009] |
| deepseek-r1:1.5b_kb_rag vs gemma4:latest_baseline | 0.4255 | 0.0000e+00 | ✅ Yes | [0.3301, 0.5208] |
| deepseek-r1:1.5b_kb_rag vs gemma4:latest_kb_rag | 0.4633 | 0.0000e+00 | ✅ Yes | [0.3680, 0.5587] |
| deepseek-r1:1.5b_kb_rag vs gpt-oss:20b_baseline | 0.4417 | 0.0000e+00 | ✅ Yes | [0.3464, 0.5370] |
| deepseek-r1:1.5b_kb_rag vs gpt-oss:20b_kb_rag | 0.4563 | 0.0000e+00 | ✅ Yes | [0.3610, 0.5516] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_baseline | 0.3782 | 0.0000e+00 | ✅ Yes | [0.2829, 0.4735] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_kb_rag | 0.4005 | 0.0000e+00 | ✅ Yes | [0.3052, 0.4958] |
| deepseek-r1:1.5b_kb_rag vs llama3.2:latest_baseline | 0.2971 | 0.0000e+00 | ✅ Yes | [0.2018, 0.3924] |
| deepseek-r1:1.5b_kb_rag vs llama3.2:latest_kb_rag | 0.3780 | 0.0000e+00 | ✅ Yes | [0.2827, 0.4733] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_baseline | 0.2765 | 0.0000e+00 | ✅ Yes | [0.1812, 0.3718] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_kb_rag | 0.2531 | 0.0000e+00 | ✅ Yes | [0.1578, 0.3484] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_baseline | -0.0462 | 9.8270e-01 | ❌ No | [-0.1415, 0.0491] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_kb_rag | 0.0981 | 3.5200e-02 | ✅ Yes | [0.0028, 0.1934] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_baseline | 0.3688 | 0.0000e+00 | ✅ Yes | [0.2735, 0.4641] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_kb_rag | 0.3727 | 0.0000e+00 | ✅ Yes | [0.2774, 0.4680] |
| gemma4:12b-mlx_baseline vs gemma4:12b-mlx_kb_rag | 0.0187 | 1.0000e+00 | ❌ No | [-0.0766, 0.1140] |
| gemma4:12b-mlx_baseline vs gemma4:31b-cloud_baseline | -0.3756 | 0.0000e+00 | ✅ Yes | [-0.4709, -0.2803] |
| gemma4:12b-mlx_baseline vs gemma4:31b-cloud_kb_rag | -0.2675 | 0.0000e+00 | ✅ Yes | [-0.3629, -0.1722] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_baseline | 0.0356 | 9.9950e-01 | ❌ No | [-0.0597, 0.1309] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_kb_rag | 0.0457 | 9.8460e-01 | ❌ No | [-0.0496, 0.1411] |
| gemma4:12b-mlx_baseline vs gemma4:latest_baseline | -0.0343 | 9.9970e-01 | ❌ No | [-0.1297, 0.0610] |
| gemma4:12b-mlx_baseline vs gemma4:latest_kb_rag | 0.0035 | 1.0000e+00 | ❌ No | [-0.0918, 0.0988] |
| gemma4:12b-mlx_baseline vs gpt-oss:20b_baseline | -0.0181 | 1.0000e+00 | ❌ No | [-0.1134, 0.0772] |
| gemma4:12b-mlx_baseline vs gpt-oss:20b_kb_rag | -0.0035 | 1.0000e+00 | ❌ No | [-0.0988, 0.0918] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_baseline | -0.0816 | 2.1920e-01 | ❌ No | [-0.1769, 0.0137] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_kb_rag | -0.0593 | 8.1650e-01 | ❌ No | [-0.1546, 0.0360] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_baseline | -0.1627 | 0.0000e+00 | ✅ Yes | [-0.2580, -0.0674] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_kb_rag | -0.0818 | 2.1460e-01 | ❌ No | [-0.1771, 0.0135] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_baseline | -0.1833 | 0.0000e+00 | ✅ Yes | [-0.2786, -0.0880] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.2067 | 0.0000e+00 | ✅ Yes | [-0.3020, -0.1114] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_baseline | -0.5060 | 0.0000e+00 | ✅ Yes | [-0.6013, -0.4107] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_kb_rag | -0.3617 | 0.0000e+00 | ✅ Yes | [-0.4570, -0.2664] |
| gemma4:12b-mlx_baseline vs qwen3:8b_baseline | -0.0910 | 8.3300e-02 | ❌ No | [-0.1863, 0.0043] |
| gemma4:12b-mlx_baseline vs qwen3:8b_kb_rag | -0.0871 | 1.2760e-01 | ❌ No | [-0.1825, 0.0082] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-cloud_baseline | -0.3943 | 0.0000e+00 | ✅ Yes | [-0.4896, -0.2990] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-cloud_kb_rag | -0.2863 | 0.0000e+00 | ✅ Yes | [-0.3816, -0.1909] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_baseline | 0.0169 | 1.0000e+00 | ❌ No | [-0.0784, 0.1122] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_kb_rag | 0.0270 | 1.0000e+00 | ❌ No | [-0.0683, 0.1223] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_baseline | -0.0531 | 9.2710e-01 | ❌ No | [-0.1484, 0.0423] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0152 | 1.0000e+00 | ❌ No | [-0.1105, 0.0801] |
| gemma4:12b-mlx_kb_rag vs gpt-oss:20b_baseline | -0.0368 | 9.9910e-01 | ❌ No | [-0.1321, 0.0585] |
| gemma4:12b-mlx_kb_rag vs gpt-oss:20b_kb_rag | -0.0222 | 1.0000e+00 | ❌ No | [-0.1175, 0.0731] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_baseline | -0.1003 | 2.6200e-02 | ✅ Yes | [-0.1956, -0.0050] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_kb_rag | -0.0780 | 2.9740e-01 | ❌ No | [-0.1734, 0.0173] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_baseline | -0.1814 | 0.0000e+00 | ✅ Yes | [-0.2767, -0.0861] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.1005 | 2.5400e-02 | ✅ Yes | [-0.1959, -0.0052] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.2020 | 0.0000e+00 | ✅ Yes | [-0.2973, -0.1067] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.2254 | 0.0000e+00 | ✅ Yes | [-0.3207, -0.1301] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_baseline | -0.5247 | 0.0000e+00 | ✅ Yes | [-0.6200, -0.4294] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | -0.3804 | 0.0000e+00 | ✅ Yes | [-0.4757, -0.2851] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_baseline | -0.1097 | 6.8000e-03 | ✅ Yes | [-0.2051, -0.0144] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.1058 | 1.2100e-02 | ✅ Yes | [-0.2012, -0.0105] |
| gemma4:31b-cloud_baseline vs gemma4:31b-cloud_kb_rag | 0.1080 | 8.7000e-03 | ✅ Yes | [0.0127, 0.2034] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_baseline | 0.4112 | 0.0000e+00 | ✅ Yes | [0.3159, 0.5065] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_kb_rag | 0.4213 | 0.0000e+00 | ✅ Yes | [0.3260, 0.5166] |
| gemma4:31b-cloud_baseline vs gemma4:latest_baseline | 0.3412 | 0.0000e+00 | ✅ Yes | [0.2459, 0.4366] |
| gemma4:31b-cloud_baseline vs gemma4:latest_kb_rag | 0.3791 | 0.0000e+00 | ✅ Yes | [0.2838, 0.4744] |
| gemma4:31b-cloud_baseline vs gpt-oss:20b_baseline | 0.3575 | 0.0000e+00 | ✅ Yes | [0.2622, 0.4528] |
| gemma4:31b-cloud_baseline vs gpt-oss:20b_kb_rag | 0.3721 | 0.0000e+00 | ✅ Yes | [0.2768, 0.4674] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_baseline | 0.2940 | 0.0000e+00 | ✅ Yes | [0.1987, 0.3893] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_kb_rag | 0.3163 | 0.0000e+00 | ✅ Yes | [0.2209, 0.4116] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_baseline | 0.2129 | 0.0000e+00 | ✅ Yes | [0.1176, 0.3082] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_kb_rag | 0.2938 | 0.0000e+00 | ✅ Yes | [0.1984, 0.3891] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_baseline | 0.1923 | 0.0000e+00 | ✅ Yes | [0.0970, 0.2876] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_kb_rag | 0.1689 | 0.0000e+00 | ✅ Yes | [0.0736, 0.2642] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_baseline | -0.1304 | 2.0000e-04 | ✅ Yes | [-0.2257, -0.0351] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_kb_rag | 0.0139 | 1.0000e+00 | ❌ No | [-0.0814, 0.1092] |
| gemma4:31b-cloud_baseline vs qwen3:8b_baseline | 0.2846 | 0.0000e+00 | ✅ Yes | [0.1892, 0.3799] |
| gemma4:31b-cloud_baseline vs qwen3:8b_kb_rag | 0.2885 | 0.0000e+00 | ✅ Yes | [0.1931, 0.3838] |
| gemma4:31b-cloud_kb_rag vs gemma4:31b-mlx_baseline | 0.3031 | 0.0000e+00 | ✅ Yes | [0.2078, 0.3984] |
| gemma4:31b-cloud_kb_rag vs gemma4:31b-mlx_kb_rag | 0.3133 | 0.0000e+00 | ✅ Yes | [0.2180, 0.4086] |
| gemma4:31b-cloud_kb_rag vs gemma4:latest_baseline | 0.2332 | 0.0000e+00 | ✅ Yes | [0.1379, 0.3285] |
| gemma4:31b-cloud_kb_rag vs gemma4:latest_kb_rag | 0.2711 | 0.0000e+00 | ✅ Yes | [0.1758, 0.3664] |
| gemma4:31b-cloud_kb_rag vs gpt-oss:20b_baseline | 0.2494 | 0.0000e+00 | ✅ Yes | [0.1541, 0.3447] |
| gemma4:31b-cloud_kb_rag vs gpt-oss:20b_kb_rag | 0.2641 | 0.0000e+00 | ✅ Yes | [0.1687, 0.3594] |
| gemma4:31b-cloud_kb_rag vs llama3.1:8b_baseline | 0.1859 | 0.0000e+00 | ✅ Yes | [0.0906, 0.2813] |
| gemma4:31b-cloud_kb_rag vs llama3.1:8b_kb_rag | 0.2082 | 0.0000e+00 | ✅ Yes | [0.1129, 0.3035] |
| gemma4:31b-cloud_kb_rag vs llama3.2:latest_baseline | 0.1048 | 1.4000e-02 | ✅ Yes | [0.0095, 0.2001] |
| gemma4:31b-cloud_kb_rag vs llama3.2:latest_kb_rag | 0.1857 | 0.0000e+00 | ✅ Yes | [0.0904, 0.2810] |
| gemma4:31b-cloud_kb_rag vs mistral-nemo:latest_baseline | 0.0842 | 1.7120e-01 | ❌ No | [-0.0111, 0.1795] |
| gemma4:31b-cloud_kb_rag vs mistral-nemo:latest_kb_rag | 0.0608 | 7.8090e-01 | ❌ No | [-0.0345, 0.1562] |
| gemma4:31b-cloud_kb_rag vs nemotron-mini:4b_baseline | -0.2385 | 0.0000e+00 | ✅ Yes | [-0.3338, -0.1431] |
| gemma4:31b-cloud_kb_rag vs nemotron-mini:4b_kb_rag | -0.0942 | 5.7500e-02 | ❌ No | [-0.1895, 0.0011] |
| gemma4:31b-cloud_kb_rag vs qwen3:8b_baseline | 0.1765 | 0.0000e+00 | ✅ Yes | [0.0812, 0.2718] |
| gemma4:31b-cloud_kb_rag vs qwen3:8b_kb_rag | 0.1804 | 0.0000e+00 | ✅ Yes | [0.0851, 0.2757] |
| gemma4:31b-mlx_baseline vs gemma4:31b-mlx_kb_rag | 0.0102 | 1.0000e+00 | ❌ No | [-0.0852, 0.1055] |
| gemma4:31b-mlx_baseline vs gemma4:latest_baseline | -0.0699 | 5.2200e-01 | ❌ No | [-0.1652, 0.0254] |
| gemma4:31b-mlx_baseline vs gemma4:latest_kb_rag | -0.0320 | 9.9990e-01 | ❌ No | [-0.1274, 0.0633] |
| gemma4:31b-mlx_baseline vs gpt-oss:20b_baseline | -0.0537 | 9.1880e-01 | ❌ No | [-0.1490, 0.0416] |
| gemma4:31b-mlx_baseline vs gpt-oss:20b_kb_rag | -0.0391 | 9.9790e-01 | ❌ No | [-0.1344, 0.0562] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_baseline | -0.1172 | 2.1000e-03 | ✅ Yes | [-0.2125, -0.0219] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_kb_rag | -0.0949 | 5.2600e-02 | ❌ No | [-0.1902, 0.0004] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_baseline | -0.1983 | 0.0000e+00 | ✅ Yes | [-0.2936, -0.1030] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_kb_rag | -0.1174 | 2.0000e-03 | ✅ Yes | [-0.2127, -0.0221] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_baseline | -0.2189 | 0.0000e+00 | ✅ Yes | [-0.3142, -0.1236] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.2423 | 0.0000e+00 | ✅ Yes | [-0.3376, -0.1470] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_baseline | -0.5416 | 0.0000e+00 | ✅ Yes | [-0.6369, -0.4463] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_kb_rag | -0.3973 | 0.0000e+00 | ✅ Yes | [-0.4926, -0.3020] |
| gemma4:31b-mlx_baseline vs qwen3:8b_baseline | -0.1266 | 4.0000e-04 | ✅ Yes | [-0.2219, -0.0313] |
| gemma4:31b-mlx_baseline vs qwen3:8b_kb_rag | -0.1227 | 8.0000e-04 | ✅ Yes | [-0.2180, -0.0274] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_baseline | -0.0801 | 2.5060e-01 | ❌ No | [-0.1754, 0.0152] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0422 | 9.9420e-01 | ❌ No | [-0.1375, 0.0531] |
| gemma4:31b-mlx_kb_rag vs gpt-oss:20b_baseline | -0.0639 | 7.0140e-01 | ❌ No | [-0.1592, 0.0315] |
| gemma4:31b-mlx_kb_rag vs gpt-oss:20b_kb_rag | -0.0492 | 9.6520e-01 | ❌ No | [-0.1445, 0.0461] |
| gemma4:31b-mlx_kb_rag vs llama3.1:8b_baseline | -0.1273 | 4.0000e-04 | ✅ Yes | [-0.2227, -0.0320] |
| gemma4:31b-mlx_kb_rag vs llama3.1:8b_kb_rag | -0.1051 | 1.3500e-02 | ✅ Yes | [-0.2004, -0.0098] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_baseline | -0.2085 | 0.0000e+00 | ✅ Yes | [-0.3038, -0.1131] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.1276 | 3.0000e-04 | ✅ Yes | [-0.2229, -0.0323] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.2291 | 0.0000e+00 | ✅ Yes | [-0.3244, -0.1337] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.2524 | 0.0000e+00 | ✅ Yes | [-0.3478, -0.1571] |
| gemma4:31b-mlx_kb_rag vs nemotron-mini:4b_baseline | -0.5517 | 0.0000e+00 | ✅ Yes | [-0.6471, -0.4564] |
| gemma4:31b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | -0.4075 | 0.0000e+00 | ✅ Yes | [-0.5028, -0.3121] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_baseline | -0.1368 | 1.0000e-04 | ✅ Yes | [-0.2321, -0.0415] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.1329 | 1.0000e-04 | ✅ Yes | [-0.2282, -0.0376] |
| gemma4:latest_baseline vs gemma4:latest_kb_rag | 0.0379 | 9.9860e-01 | ❌ No | [-0.0574, 0.1332] |
| gemma4:latest_baseline vs gpt-oss:20b_baseline | 0.0162 | 1.0000e+00 | ❌ No | [-0.0791, 0.1116] |
| gemma4:latest_baseline vs gpt-oss:20b_kb_rag | 0.0309 | 9.9990e-01 | ❌ No | [-0.0645, 0.1262] |
| gemma4:latest_baseline vs llama3.1:8b_baseline | -0.0472 | 9.7770e-01 | ❌ No | [-0.1426, 0.0481] |
| gemma4:latest_baseline vs llama3.1:8b_kb_rag | -0.0250 | 1.0000e+00 | ❌ No | [-0.1203, 0.0703] |
| gemma4:latest_baseline vs llama3.2:latest_baseline | -0.1284 | 3.0000e-04 | ✅ Yes | [-0.2237, -0.0331] |
| gemma4:latest_baseline vs llama3.2:latest_kb_rag | -0.0475 | 9.7640e-01 | ❌ No | [-0.1428, 0.0478] |
| gemma4:latest_baseline vs mistral-nemo:latest_baseline | -0.1490 | 0.0000e+00 | ✅ Yes | [-0.2443, -0.0537] |
| gemma4:latest_baseline vs mistral-nemo:latest_kb_rag | -0.1724 | 0.0000e+00 | ✅ Yes | [-0.2677, -0.0770] |
| gemma4:latest_baseline vs nemotron-mini:4b_baseline | -0.4716 | 0.0000e+00 | ✅ Yes | [-0.5670, -0.3763] |
| gemma4:latest_baseline vs nemotron-mini:4b_kb_rag | -0.3274 | 0.0000e+00 | ✅ Yes | [-0.4227, -0.2321] |
| gemma4:latest_baseline vs qwen3:8b_baseline | -0.0567 | 8.7090e-01 | ❌ No | [-0.1520, 0.0386] |
| gemma4:latest_baseline vs qwen3:8b_kb_rag | -0.0528 | 9.3050e-01 | ❌ No | [-0.1481, 0.0425] |
| gemma4:latest_kb_rag vs gpt-oss:20b_baseline | -0.0216 | 1.0000e+00 | ❌ No | [-0.1170, 0.0737] |
| gemma4:latest_kb_rag vs gpt-oss:20b_kb_rag | -0.0070 | 1.0000e+00 | ❌ No | [-0.1023, 0.0883] |
| gemma4:latest_kb_rag vs llama3.1:8b_baseline | -0.0851 | 1.5660e-01 | ❌ No | [-0.1804, 0.0102] |
| gemma4:latest_kb_rag vs llama3.1:8b_kb_rag | -0.0629 | 7.2860e-01 | ❌ No | [-0.1582, 0.0325] |
| gemma4:latest_kb_rag vs llama3.2:latest_baseline | -0.1663 | 0.0000e+00 | ✅ Yes | [-0.2616, -0.0709] |
| gemma4:latest_kb_rag vs llama3.2:latest_kb_rag | -0.0854 | 1.5300e-01 | ❌ No | [-0.1807, 0.0100] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_baseline | -0.1869 | 0.0000e+00 | ✅ Yes | [-0.2822, -0.0915] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.2102 | 0.0000e+00 | ✅ Yes | [-0.3056, -0.1149] |
| gemma4:latest_kb_rag vs nemotron-mini:4b_baseline | -0.5095 | 0.0000e+00 | ✅ Yes | [-0.6048, -0.4142] |
| gemma4:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.3653 | 0.0000e+00 | ✅ Yes | [-0.4606, -0.2699] |
| gemma4:latest_kb_rag vs qwen3:8b_baseline | -0.0946 | 5.4800e-02 | ❌ No | [-0.1899, 0.0008] |
| gemma4:latest_kb_rag vs qwen3:8b_kb_rag | -0.0907 | 8.6800e-02 | ❌ No | [-0.1860, 0.0046] |
| gpt-oss:20b_baseline vs gpt-oss:20b_kb_rag | 0.0146 | 1.0000e+00 | ❌ No | [-0.0807, 0.1099] |
| gpt-oss:20b_baseline vs llama3.1:8b_baseline | -0.0635 | 7.1160e-01 | ❌ No | [-0.1588, 0.0318] |
| gpt-oss:20b_baseline vs llama3.1:8b_kb_rag | -0.0412 | 9.9570e-01 | ❌ No | [-0.1365, 0.0541] |
| gpt-oss:20b_baseline vs llama3.2:latest_baseline | -0.1446 | 0.0000e+00 | ✅ Yes | [-0.2399, -0.0493] |
| gpt-oss:20b_baseline vs llama3.2:latest_kb_rag | -0.0637 | 7.0510e-01 | ❌ No | [-0.1590, 0.0316] |
| gpt-oss:20b_baseline vs mistral-nemo:latest_baseline | -0.1652 | 0.0000e+00 | ✅ Yes | [-0.2605, -0.0699] |
| gpt-oss:20b_baseline vs mistral-nemo:latest_kb_rag | -0.1886 | 0.0000e+00 | ✅ Yes | [-0.2839, -0.0933] |
| gpt-oss:20b_baseline vs nemotron-mini:4b_baseline | -0.4879 | 0.0000e+00 | ✅ Yes | [-0.5832, -0.3926] |
| gpt-oss:20b_baseline vs nemotron-mini:4b_kb_rag | -0.3436 | 0.0000e+00 | ✅ Yes | [-0.4389, -0.2483] |
| gpt-oss:20b_baseline vs qwen3:8b_baseline | -0.0729 | 4.3380e-01 | ❌ No | [-0.1682, 0.0224] |
| gpt-oss:20b_baseline vs qwen3:8b_kb_rag | -0.0690 | 5.4920e-01 | ❌ No | [-0.1643, 0.0263] |
| gpt-oss:20b_kb_rag vs llama3.1:8b_baseline | -0.0781 | 2.9590e-01 | ❌ No | [-0.1734, 0.0172] |
| gpt-oss:20b_kb_rag vs llama3.1:8b_kb_rag | -0.0558 | 8.8580e-01 | ❌ No | [-0.1512, 0.0395] |
| gpt-oss:20b_kb_rag vs llama3.2:latest_baseline | -0.1592 | 0.0000e+00 | ✅ Yes | [-0.2545, -0.0639] |
| gpt-oss:20b_kb_rag vs llama3.2:latest_kb_rag | -0.0783 | 2.9030e-01 | ❌ No | [-0.1737, 0.0170] |
| gpt-oss:20b_kb_rag vs mistral-nemo:latest_baseline | -0.1798 | 0.0000e+00 | ✅ Yes | [-0.2751, -0.0845] |
| gpt-oss:20b_kb_rag vs mistral-nemo:latest_kb_rag | -0.2032 | 0.0000e+00 | ✅ Yes | [-0.2985, -0.1079] |
| gpt-oss:20b_kb_rag vs nemotron-mini:4b_baseline | -0.5025 | 0.0000e+00 | ✅ Yes | [-0.5978, -0.4072] |
| gpt-oss:20b_kb_rag vs nemotron-mini:4b_kb_rag | -0.3582 | 0.0000e+00 | ✅ Yes | [-0.4535, -0.2629] |
| gpt-oss:20b_kb_rag vs qwen3:8b_baseline | -0.0875 | 1.2230e-01 | ❌ No | [-0.1829, 0.0078] |
| gpt-oss:20b_kb_rag vs qwen3:8b_kb_rag | -0.0836 | 1.8110e-01 | ❌ No | [-0.1790, 0.0117] |
| llama3.1:8b_baseline vs llama3.1:8b_kb_rag | 0.0223 | 1.0000e+00 | ❌ No | [-0.0730, 0.1176] |
| llama3.1:8b_baseline vs llama3.2:latest_baseline | -0.0811 | 2.2880e-01 | ❌ No | [-0.1764, 0.0142] |
| llama3.1:8b_baseline vs llama3.2:latest_kb_rag | -0.0002 | 1.0000e+00 | ❌ No | [-0.0955, 0.0951] |
| llama3.1:8b_baseline vs mistral-nemo:latest_baseline | -0.1017 | 2.1600e-02 | ✅ Yes | [-0.1970, -0.0064] |
| llama3.1:8b_baseline vs mistral-nemo:latest_kb_rag | -0.1251 | 5.0000e-04 | ✅ Yes | [-0.2204, -0.0298] |
| llama3.1:8b_baseline vs nemotron-mini:4b_baseline | -0.4244 | 0.0000e+00 | ✅ Yes | [-0.5197, -0.3291] |
| llama3.1:8b_baseline vs nemotron-mini:4b_kb_rag | -0.2801 | 0.0000e+00 | ✅ Yes | [-0.3754, -0.1848] |
| llama3.1:8b_baseline vs qwen3:8b_baseline | -0.0094 | 1.0000e+00 | ❌ No | [-0.1047, 0.0859] |
| llama3.1:8b_baseline vs qwen3:8b_kb_rag | -0.0055 | 1.0000e+00 | ❌ No | [-0.1009, 0.0898] |
| llama3.1:8b_kb_rag vs llama3.2:latest_baseline | -0.1034 | 1.7200e-02 | ✅ Yes | [-0.1987, -0.0081] |
| llama3.1:8b_kb_rag vs llama3.2:latest_kb_rag | -0.0225 | 1.0000e+00 | ❌ No | [-0.1178, 0.0728] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_baseline | -0.1240 | 6.0000e-04 | ✅ Yes | [-0.2193, -0.0287] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_kb_rag | -0.1474 | 0.0000e+00 | ✅ Yes | [-0.2427, -0.0521] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_baseline | -0.4467 | 0.0000e+00 | ✅ Yes | [-0.5420, -0.3514] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_kb_rag | -0.3024 | 0.0000e+00 | ✅ Yes | [-0.3977, -0.2071] |
| llama3.1:8b_kb_rag vs qwen3:8b_baseline | -0.0317 | 9.9990e-01 | ❌ No | [-0.1270, 0.0636] |
| llama3.1:8b_kb_rag vs qwen3:8b_kb_rag | -0.0278 | 1.0000e+00 | ❌ No | [-0.1231, 0.0675] |
| llama3.2:latest_baseline vs llama3.2:latest_kb_rag | 0.0809 | 2.3360e-01 | ❌ No | [-0.0144, 0.1762] |
| llama3.2:latest_baseline vs mistral-nemo:latest_baseline | -0.0206 | 1.0000e+00 | ❌ No | [-0.1159, 0.0747] |
| llama3.2:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0440 | 9.9030e-01 | ❌ No | [-0.1393, 0.0513] |
| llama3.2:latest_baseline vs nemotron-mini:4b_baseline | -0.3433 | 0.0000e+00 | ✅ Yes | [-0.4386, -0.2480] |
| llama3.2:latest_baseline vs nemotron-mini:4b_kb_rag | -0.1990 | 0.0000e+00 | ✅ Yes | [-0.2943, -0.1037] |
| llama3.2:latest_baseline vs qwen3:8b_baseline | 0.0717 | 4.6950e-01 | ❌ No | [-0.0236, 0.1670] |
| llama3.2:latest_baseline vs qwen3:8b_kb_rag | 0.0756 | 3.5980e-01 | ❌ No | [-0.0197, 0.1709] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_baseline | -0.1015 | 2.2400e-02 | ✅ Yes | [-0.1968, -0.0062] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.1249 | 5.0000e-04 | ✅ Yes | [-0.2202, -0.0296] |
| llama3.2:latest_kb_rag vs nemotron-mini:4b_baseline | -0.4242 | 0.0000e+00 | ✅ Yes | [-0.5195, -0.3289] |
| llama3.2:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.2799 | 0.0000e+00 | ✅ Yes | [-0.3752, -0.1846] |
| llama3.2:latest_kb_rag vs qwen3:8b_baseline | -0.0092 | 1.0000e+00 | ❌ No | [-0.1045, 0.0861] |
| llama3.2:latest_kb_rag vs qwen3:8b_kb_rag | -0.0053 | 1.0000e+00 | ❌ No | [-0.1006, 0.0900] |
| mistral-nemo:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0234 | 1.0000e+00 | ❌ No | [-0.1187, 0.0719] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_baseline | -0.3227 | 0.0000e+00 | ✅ Yes | [-0.4180, -0.2274] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_kb_rag | -0.1784 | 0.0000e+00 | ✅ Yes | [-0.2737, -0.0831] |
| mistral-nemo:latest_baseline vs qwen3:8b_baseline | 0.0923 | 7.2000e-02 | ❌ No | [-0.0030, 0.1876] |
| mistral-nemo:latest_baseline vs qwen3:8b_kb_rag | 0.0962 | 4.4900e-02 | ✅ Yes | [0.0009, 0.1915] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_baseline | -0.2993 | 0.0000e+00 | ✅ Yes | [-0.3946, -0.2040] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.1550 | 0.0000e+00 | ✅ Yes | [-0.2503, -0.0597] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_baseline | 0.1157 | 2.6000e-03 | ✅ Yes | [0.0204, 0.2110] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_kb_rag | 0.1196 | 1.4000e-03 | ✅ Yes | [0.0243, 0.2149] |
| nemotron-mini:4b_baseline vs nemotron-mini:4b_kb_rag | 0.1443 | 0.0000e+00 | ✅ Yes | [0.0490, 0.2396] |
| nemotron-mini:4b_baseline vs qwen3:8b_baseline | 0.4150 | 0.0000e+00 | ✅ Yes | [0.3197, 0.5103] |
| nemotron-mini:4b_baseline vs qwen3:8b_kb_rag | 0.4189 | 0.0000e+00 | ✅ Yes | [0.3235, 0.5142] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_baseline | 0.2707 | 0.0000e+00 | ✅ Yes | [0.1754, 0.3660] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_kb_rag | 0.2746 | 0.0000e+00 | ✅ Yes | [0.1793, 0.3699] |
| qwen3:8b_baseline vs qwen3:8b_kb_rag | 0.0039 | 1.0000e+00 | ❌ No | [-0.0914, 0.0992] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 7 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline | 0.2961 | 0.2967 | +0.0006 | 📈 Improved |
| deepseek-r1:1.5b_kb_rag | 0.3196 | 0.3222 | +0.0026 | 📈 Improved |
| gemma4:12b-mlx_baseline | 0.7794 | 0.7818 | +0.0023 | 📈 Improved |
| gemma4:12b-mlx_kb_rag | 0.7981 | 0.8003 | +0.0022 | 📈 Improved |
| gemma4:31b-cloud_baseline | 0.4038 | 0.3932 | -0.0106 | 📉 Decreased |
| gemma4:31b-cloud_kb_rag | 0.5119 | 0.5167 | +0.0048 | 📈 Improved |
| gemma4:31b-mlx_baseline | 0.8150 | 0.8176 | +0.0027 | 📈 Improved |
| gemma4:31b-mlx_kb_rag | 0.8251 | 0.8270 | +0.0019 | 📈 Improved |
| gemma4:latest_baseline | 0.7451 | 0.7431 | -0.0019 | 📉 Decreased |
| gemma4:latest_kb_rag | 0.7829 | 0.7807 | -0.0022 | 📉 Decreased |
| gpt-oss:20b_baseline | 0.7613 | 0.7632 | +0.0019 | 📈 Improved |
| gpt-oss:20b_kb_rag | 0.7759 | 0.7774 | +0.0015 | 📈 Improved |
| llama3.1:8b_baseline | 0.6978 | 0.6970 | -0.0008 | 📉 Decreased |
| llama3.1:8b_kb_rag | 0.7201 | 0.7209 | +0.0009 | 📈 Improved |
| llama3.2:latest_baseline | 0.6167 | 0.6128 | -0.0039 | 📉 Decreased |
| llama3.2:latest_kb_rag | 0.6976 | 0.6969 | -0.0006 | 📉 Decreased |
| mistral-nemo:latest_baseline | 0.5961 | 0.5952 | -0.0009 | 📉 Decreased |
| mistral-nemo:latest_kb_rag | 0.5727 | 0.5689 | -0.0038 | 📉 Decreased |
| nemotron-mini:4b_baseline | 0.2734 | 0.2667 | -0.0067 | 📉 Decreased |
| nemotron-mini:4b_kb_rag | 0.4177 | 0.4183 | +0.0006 | 📈 Improved |
| qwen3:8b_baseline | 0.6884 | 0.6905 | +0.0021 | 📈 Improved |
| qwen3:8b_kb_rag | 0.6923 | 0.6928 | +0.0006 | 📈 Improved |