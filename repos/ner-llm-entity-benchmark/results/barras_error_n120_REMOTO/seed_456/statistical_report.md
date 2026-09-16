# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 83.3155
- **p-Value:** 4.2441e-268

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud_baseline | 113 | 0.5483 | 0.4731 | 0.6235 | 0.4035 |
| gemma4:31b-cloud_kb_rag | 113 | 0.5765 | 0.5010 | 0.6521 | 0.4051 |
| gemma4:31b-mlx_baseline | 113 | 0.8170 | 0.7911 | 0.8429 | 0.1390 |
| gemma4:31b-mlx_kb_rag | 113 | 0.8250 | 0.8003 | 0.8498 | 0.1328 |
| gemma4:12b-mlx_baseline | 113 | 0.7782 | 0.7521 | 0.8044 | 0.1403 |
| gemma4:12b-mlx_kb_rag | 113 | 0.7991 | 0.7742 | 0.8241 | 0.1340 |
| gemma4:latest_baseline | 113 | 0.7472 | 0.7191 | 0.7752 | 0.1504 |
| gemma4:latest_kb_rag | 113 | 0.7741 | 0.7459 | 0.8024 | 0.1515 |
| qwen3:8b_baseline | 113 | 0.6876 | 0.6580 | 0.7172 | 0.1588 |
| qwen3:8b_kb_rag | 113 | 0.6910 | 0.6629 | 0.7191 | 0.1509 |
| gpt-oss:20b_baseline | 113 | 0.7473 | 0.7198 | 0.7747 | 0.1474 |
| gpt-oss:20b_kb_rag | 113 | 0.7781 | 0.7536 | 0.8025 | 0.1313 |
| mistral-nemo:latest_baseline | 113 | 0.6078 | 0.5737 | 0.6419 | 0.1831 |
| mistral-nemo:latest_kb_rag | 113 | 0.5561 | 0.5213 | 0.5910 | 0.1868 |
| llama3.2:latest_baseline | 113 | 0.6191 | 0.5852 | 0.6530 | 0.1817 |
| llama3.2:latest_kb_rag | 113 | 0.6973 | 0.6668 | 0.7278 | 0.1636 |
| llama3.1:8b_baseline | 113 | 0.6981 | 0.6700 | 0.7261 | 0.1506 |
| llama3.1:8b_kb_rag | 113 | 0.7121 | 0.6828 | 0.7414 | 0.1573 |
| nemotron-mini:4b_baseline | 113 | 0.2687 | 0.2290 | 0.3084 | 0.2130 |
| nemotron-mini:4b_kb_rag | 113 | 0.4172 | 0.3836 | 0.4508 | 0.1804 |
| deepseek-r1:1.5b_baseline | 113 | 0.3034 | 0.2698 | 0.3369 | 0.1799 |
| deepseek-r1:1.5b_kb_rag | 113 | 0.3325 | 0.2969 | 0.3681 | 0.1909 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline vs deepseek-r1:1.5b_kb_rag | 0.0291 | 1.0000e+00 | ❌ No | [-0.0653, 0.1235] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_baseline | 0.4749 | 0.0000e+00 | ✅ Yes | [0.3805, 0.5693] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_kb_rag | 0.4958 | 0.0000e+00 | ✅ Yes | [0.4014, 0.5902] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_baseline | 0.2450 | 0.0000e+00 | ✅ Yes | [0.1506, 0.3394] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_kb_rag | 0.2732 | 0.0000e+00 | ✅ Yes | [0.1788, 0.3676] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_baseline | 0.5137 | 0.0000e+00 | ✅ Yes | [0.4193, 0.6081] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_kb_rag | 0.5217 | 0.0000e+00 | ✅ Yes | [0.4273, 0.6161] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_baseline | 0.4438 | 0.0000e+00 | ✅ Yes | [0.3494, 0.5382] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_kb_rag | 0.4708 | 0.0000e+00 | ✅ Yes | [0.3764, 0.5652] |
| deepseek-r1:1.5b_baseline vs gpt-oss:20b_baseline | 0.4439 | 0.0000e+00 | ✅ Yes | [0.3495, 0.5383] |
| deepseek-r1:1.5b_baseline vs gpt-oss:20b_kb_rag | 0.4747 | 0.0000e+00 | ✅ Yes | [0.3803, 0.5691] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_baseline | 0.3947 | 0.0000e+00 | ✅ Yes | [0.3003, 0.4891] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_kb_rag | 0.4087 | 0.0000e+00 | ✅ Yes | [0.3143, 0.5031] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_baseline | 0.3157 | 0.0000e+00 | ✅ Yes | [0.2213, 0.4101] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_kb_rag | 0.3939 | 0.0000e+00 | ✅ Yes | [0.2995, 0.4883] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_baseline | 0.3044 | 0.0000e+00 | ✅ Yes | [0.2100, 0.3988] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_kb_rag | 0.2528 | 0.0000e+00 | ✅ Yes | [0.1584, 0.3472] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_baseline | -0.0346 | 9.9960e-01 | ❌ No | [-0.1291, 0.0598] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_kb_rag | 0.1139 | 3.0000e-03 | ✅ Yes | [0.0194, 0.2083] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_baseline | 0.3842 | 0.0000e+00 | ✅ Yes | [0.2898, 0.4787] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_kb_rag | 0.3877 | 0.0000e+00 | ✅ Yes | [0.2933, 0.4821] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_baseline | 0.4458 | 0.0000e+00 | ✅ Yes | [0.3513, 0.5402] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_kb_rag | 0.4667 | 0.0000e+00 | ✅ Yes | [0.3723, 0.5611] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-cloud_baseline | 0.2159 | 0.0000e+00 | ✅ Yes | [0.1214, 0.3103] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-cloud_kb_rag | 0.2441 | 0.0000e+00 | ✅ Yes | [0.1497, 0.3385] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-mlx_baseline | 0.4845 | 0.0000e+00 | ✅ Yes | [0.3901, 0.5789] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-mlx_kb_rag | 0.4925 | 0.0000e+00 | ✅ Yes | [0.3981, 0.5870] |
| deepseek-r1:1.5b_kb_rag vs gemma4:latest_baseline | 0.4147 | 0.0000e+00 | ✅ Yes | [0.3203, 0.5091] |
| deepseek-r1:1.5b_kb_rag vs gemma4:latest_kb_rag | 0.4417 | 0.0000e+00 | ✅ Yes | [0.3472, 0.5361] |
| deepseek-r1:1.5b_kb_rag vs gpt-oss:20b_baseline | 0.4148 | 0.0000e+00 | ✅ Yes | [0.3204, 0.5092] |
| deepseek-r1:1.5b_kb_rag vs gpt-oss:20b_kb_rag | 0.4456 | 0.0000e+00 | ✅ Yes | [0.3512, 0.5400] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_baseline | 0.3656 | 0.0000e+00 | ✅ Yes | [0.2712, 0.4600] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_kb_rag | 0.3796 | 0.0000e+00 | ✅ Yes | [0.2852, 0.4740] |
| deepseek-r1:1.5b_kb_rag vs llama3.2:latest_baseline | 0.2866 | 0.0000e+00 | ✅ Yes | [0.1922, 0.3810] |
| deepseek-r1:1.5b_kb_rag vs llama3.2:latest_kb_rag | 0.3648 | 0.0000e+00 | ✅ Yes | [0.2704, 0.4592] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_baseline | 0.2753 | 0.0000e+00 | ✅ Yes | [0.1809, 0.3697] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_kb_rag | 0.2237 | 0.0000e+00 | ✅ Yes | [0.1292, 0.3181] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_baseline | -0.0638 | 6.8640e-01 | ❌ No | [-0.1582, 0.0306] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_kb_rag | 0.0847 | 1.5030e-01 | ❌ No | [-0.0097, 0.1791] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_baseline | 0.3551 | 0.0000e+00 | ✅ Yes | [0.2607, 0.4495] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_kb_rag | 0.3585 | 0.0000e+00 | ✅ Yes | [0.2641, 0.4529] |
| gemma4:12b-mlx_baseline vs gemma4:12b-mlx_kb_rag | 0.0209 | 1.0000e+00 | ❌ No | [-0.0735, 0.1153] |
| gemma4:12b-mlx_baseline vs gemma4:31b-cloud_baseline | -0.2299 | 0.0000e+00 | ✅ Yes | [-0.3243, -0.1355] |
| gemma4:12b-mlx_baseline vs gemma4:31b-cloud_kb_rag | -0.2017 | 0.0000e+00 | ✅ Yes | [-0.2961, -0.1073] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_baseline | 0.0388 | 9.9790e-01 | ❌ No | [-0.0556, 0.1332] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_kb_rag | 0.0468 | 9.7770e-01 | ❌ No | [-0.0476, 0.1412] |
| gemma4:12b-mlx_baseline vs gemma4:latest_baseline | -0.0311 | 9.9990e-01 | ❌ No | [-0.1255, 0.0634] |
| gemma4:12b-mlx_baseline vs gemma4:latest_kb_rag | -0.0041 | 1.0000e+00 | ❌ No | [-0.0985, 0.0903] |
| gemma4:12b-mlx_baseline vs gpt-oss:20b_baseline | -0.0310 | 9.9990e-01 | ❌ No | [-0.1254, 0.0634] |
| gemma4:12b-mlx_baseline vs gpt-oss:20b_kb_rag | -0.0002 | 1.0000e+00 | ❌ No | [-0.0946, 0.0942] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_baseline | -0.0802 | 2.3250e-01 | ❌ No | [-0.1746, 0.0142] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_kb_rag | -0.0662 | 6.1630e-01 | ❌ No | [-0.1606, 0.0283] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_baseline | -0.1591 | 0.0000e+00 | ✅ Yes | [-0.2536, -0.0647] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_kb_rag | -0.0810 | 2.1660e-01 | ❌ No | [-0.1754, 0.0135] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_baseline | -0.1704 | 0.0000e+00 | ✅ Yes | [-0.2649, -0.0760] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.2221 | 0.0000e+00 | ✅ Yes | [-0.3165, -0.1277] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_baseline | -0.5095 | 0.0000e+00 | ✅ Yes | [-0.6039, -0.4151] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_kb_rag | -0.3610 | 0.0000e+00 | ✅ Yes | [-0.4554, -0.2666] |
| gemma4:12b-mlx_baseline vs qwen3:8b_baseline | -0.0906 | 7.8900e-02 | ❌ No | [-0.1850, 0.0038] |
| gemma4:12b-mlx_baseline vs qwen3:8b_kb_rag | -0.0872 | 1.1570e-01 | ❌ No | [-0.1816, 0.0072] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-cloud_baseline | -0.2508 | 0.0000e+00 | ✅ Yes | [-0.3452, -0.1564] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-cloud_kb_rag | -0.2226 | 0.0000e+00 | ✅ Yes | [-0.3170, -0.1282] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_baseline | 0.0179 | 1.0000e+00 | ❌ No | [-0.0765, 0.1123] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_kb_rag | 0.0259 | 1.0000e+00 | ❌ No | [-0.0685, 0.1203] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_baseline | -0.0520 | 9.3440e-01 | ❌ No | [-0.1464, 0.0424] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0250 | 1.0000e+00 | ❌ No | [-0.1194, 0.0694] |
| gemma4:12b-mlx_kb_rag vs gpt-oss:20b_baseline | -0.0519 | 9.3540e-01 | ❌ No | [-0.1463, 0.0425] |
| gemma4:12b-mlx_kb_rag vs gpt-oss:20b_kb_rag | -0.0211 | 1.0000e+00 | ❌ No | [-0.1155, 0.0733] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_baseline | -0.1011 | 2.0700e-02 | ✅ Yes | [-0.1955, -0.0067] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_kb_rag | -0.0871 | 1.1770e-01 | ❌ No | [-0.1815, 0.0073] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_baseline | -0.1801 | 0.0000e+00 | ✅ Yes | [-0.2745, -0.0856] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.1019 | 1.8500e-02 | ✅ Yes | [-0.1963, -0.0075] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.1914 | 0.0000e+00 | ✅ Yes | [-0.2858, -0.0969] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.2430 | 0.0000e+00 | ✅ Yes | [-0.3374, -0.1486] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_baseline | -0.5304 | 0.0000e+00 | ✅ Yes | [-0.6248, -0.4360] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | -0.3819 | 0.0000e+00 | ✅ Yes | [-0.4763, -0.2875] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_baseline | -0.1115 | 4.3000e-03 | ✅ Yes | [-0.2060, -0.0171] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.1081 | 7.4000e-03 | ✅ Yes | [-0.2025, -0.0137] |
| gemma4:31b-cloud_baseline vs gemma4:31b-cloud_kb_rag | 0.0282 | 1.0000e+00 | ❌ No | [-0.0662, 0.1226] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_baseline | 0.2687 | 0.0000e+00 | ✅ Yes | [0.1743, 0.3631] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_kb_rag | 0.2767 | 0.0000e+00 | ✅ Yes | [0.1823, 0.3711] |
| gemma4:31b-cloud_baseline vs gemma4:latest_baseline | 0.1988 | 0.0000e+00 | ✅ Yes | [0.1044, 0.2933] |
| gemma4:31b-cloud_baseline vs gemma4:latest_kb_rag | 0.2258 | 0.0000e+00 | ✅ Yes | [0.1314, 0.3202] |
| gemma4:31b-cloud_baseline vs gpt-oss:20b_baseline | 0.1989 | 0.0000e+00 | ✅ Yes | [0.1045, 0.2933] |
| gemma4:31b-cloud_baseline vs gpt-oss:20b_kb_rag | 0.2297 | 0.0000e+00 | ✅ Yes | [0.1353, 0.3241] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_baseline | 0.1497 | 0.0000e+00 | ✅ Yes | [0.0553, 0.2441] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_kb_rag | 0.1637 | 0.0000e+00 | ✅ Yes | [0.0693, 0.2582] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_baseline | 0.0708 | 4.7710e-01 | ❌ No | [-0.0237, 0.1652] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_kb_rag | 0.1489 | 0.0000e+00 | ✅ Yes | [0.0545, 0.2434] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_baseline | 0.0595 | 8.0050e-01 | ❌ No | [-0.0350, 0.1539] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_kb_rag | 0.0078 | 1.0000e+00 | ❌ No | [-0.0866, 0.1022] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_baseline | -0.2796 | 0.0000e+00 | ✅ Yes | [-0.3740, -0.1852] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_kb_rag | -0.1311 | 1.0000e-04 | ✅ Yes | [-0.2255, -0.0367] |
| gemma4:31b-cloud_baseline vs qwen3:8b_baseline | 0.1393 | 0.0000e+00 | ✅ Yes | [0.0449, 0.2337] |
| gemma4:31b-cloud_baseline vs qwen3:8b_kb_rag | 0.1427 | 0.0000e+00 | ✅ Yes | [0.0483, 0.2371] |
| gemma4:31b-cloud_kb_rag vs gemma4:31b-mlx_baseline | 0.2405 | 0.0000e+00 | ✅ Yes | [0.1461, 0.3349] |
| gemma4:31b-cloud_kb_rag vs gemma4:31b-mlx_kb_rag | 0.2485 | 0.0000e+00 | ✅ Yes | [0.1541, 0.3429] |
| gemma4:31b-cloud_kb_rag vs gemma4:latest_baseline | 0.1706 | 0.0000e+00 | ✅ Yes | [0.0762, 0.2650] |
| gemma4:31b-cloud_kb_rag vs gemma4:latest_kb_rag | 0.1976 | 0.0000e+00 | ✅ Yes | [0.1032, 0.2920] |
| gemma4:31b-cloud_kb_rag vs gpt-oss:20b_baseline | 0.1707 | 0.0000e+00 | ✅ Yes | [0.0763, 0.2651] |
| gemma4:31b-cloud_kb_rag vs gpt-oss:20b_kb_rag | 0.2015 | 0.0000e+00 | ✅ Yes | [0.1071, 0.2959] |
| gemma4:31b-cloud_kb_rag vs llama3.1:8b_baseline | 0.1215 | 8.0000e-04 | ✅ Yes | [0.0271, 0.2159] |
| gemma4:31b-cloud_kb_rag vs llama3.1:8b_kb_rag | 0.1355 | 1.0000e-04 | ✅ Yes | [0.0411, 0.2299] |
| gemma4:31b-cloud_kb_rag vs llama3.2:latest_baseline | 0.0425 | 9.9280e-01 | ❌ No | [-0.0519, 0.1370] |
| gemma4:31b-cloud_kb_rag vs llama3.2:latest_kb_rag | 0.1207 | 9.0000e-04 | ✅ Yes | [0.0263, 0.2151] |
| gemma4:31b-cloud_kb_rag vs mistral-nemo:latest_baseline | 0.0312 | 9.9990e-01 | ❌ No | [-0.0632, 0.1257] |
| gemma4:31b-cloud_kb_rag vs mistral-nemo:latest_kb_rag | -0.0204 | 1.0000e+00 | ❌ No | [-0.1148, 0.0740] |
| gemma4:31b-cloud_kb_rag vs nemotron-mini:4b_baseline | -0.3078 | 0.0000e+00 | ✅ Yes | [-0.4022, -0.2134] |
| gemma4:31b-cloud_kb_rag vs nemotron-mini:4b_kb_rag | -0.1593 | 0.0000e+00 | ✅ Yes | [-0.2537, -0.0649] |
| gemma4:31b-cloud_kb_rag vs qwen3:8b_baseline | 0.1111 | 4.7000e-03 | ✅ Yes | [0.0166, 0.2055] |
| gemma4:31b-cloud_kb_rag vs qwen3:8b_kb_rag | 0.1145 | 2.7000e-03 | ✅ Yes | [0.0201, 0.2089] |
| gemma4:31b-mlx_baseline vs gemma4:31b-mlx_kb_rag | 0.0080 | 1.0000e+00 | ❌ No | [-0.0864, 0.1024] |
| gemma4:31b-mlx_baseline vs gemma4:latest_baseline | -0.0698 | 5.0460e-01 | ❌ No | [-0.1642, 0.0246] |
| gemma4:31b-mlx_baseline vs gemma4:latest_kb_rag | -0.0429 | 9.9200e-01 | ❌ No | [-0.1373, 0.0515] |
| gemma4:31b-mlx_baseline vs gpt-oss:20b_baseline | -0.0698 | 5.0720e-01 | ❌ No | [-0.1642, 0.0247] |
| gemma4:31b-mlx_baseline vs gpt-oss:20b_kb_rag | -0.0389 | 9.9770e-01 | ❌ No | [-0.1334, 0.0555] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_baseline | -0.1190 | 1.3000e-03 | ✅ Yes | [-0.2134, -0.0245] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_kb_rag | -0.1049 | 1.1900e-02 | ✅ Yes | [-0.1993, -0.0105] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_baseline | -0.1979 | 0.0000e+00 | ✅ Yes | [-0.2923, -0.1035] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_kb_rag | -0.1197 | 1.1000e-03 | ✅ Yes | [-0.2141, -0.0253] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_baseline | -0.2092 | 0.0000e+00 | ✅ Yes | [-0.3036, -0.1148] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.2609 | 0.0000e+00 | ✅ Yes | [-0.3553, -0.1665] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_baseline | -0.5483 | 0.0000e+00 | ✅ Yes | [-0.6427, -0.4539] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_kb_rag | -0.3998 | 0.0000e+00 | ✅ Yes | [-0.4942, -0.3054] |
| gemma4:31b-mlx_baseline vs qwen3:8b_baseline | -0.1294 | 2.0000e-04 | ✅ Yes | [-0.2238, -0.0350] |
| gemma4:31b-mlx_baseline vs qwen3:8b_kb_rag | -0.1260 | 4.0000e-04 | ✅ Yes | [-0.2204, -0.0316] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_baseline | -0.0779 | 2.8430e-01 | ❌ No | [-0.1723, 0.0166] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0509 | 9.4630e-01 | ❌ No | [-0.1453, 0.0435] |
| gemma4:31b-mlx_kb_rag vs gpt-oss:20b_baseline | -0.0778 | 2.8630e-01 | ❌ No | [-0.1722, 0.0166] |
| gemma4:31b-mlx_kb_rag vs gpt-oss:20b_kb_rag | -0.0470 | 9.7680e-01 | ❌ No | [-0.1414, 0.0475] |
| gemma4:31b-mlx_kb_rag vs llama3.1:8b_baseline | -0.1270 | 3.0000e-04 | ✅ Yes | [-0.2214, -0.0326] |
| gemma4:31b-mlx_kb_rag vs llama3.1:8b_kb_rag | -0.1129 | 3.5000e-03 | ✅ Yes | [-0.2074, -0.0185] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_baseline | -0.2059 | 0.0000e+00 | ✅ Yes | [-0.3003, -0.1115] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.1277 | 3.0000e-04 | ✅ Yes | [-0.2222, -0.0333] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.2172 | 0.0000e+00 | ✅ Yes | [-0.3116, -0.1228] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.2689 | 0.0000e+00 | ✅ Yes | [-0.3633, -0.1745] |
| gemma4:31b-mlx_kb_rag vs nemotron-mini:4b_baseline | -0.5563 | 0.0000e+00 | ✅ Yes | [-0.6507, -0.4619] |
| gemma4:31b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | -0.4078 | 0.0000e+00 | ✅ Yes | [-0.5022, -0.3134] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_baseline | -0.1374 | 0.0000e+00 | ✅ Yes | [-0.2318, -0.0430] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.1340 | 1.0000e-04 | ✅ Yes | [-0.2284, -0.0396] |
| gemma4:latest_baseline vs gemma4:latest_kb_rag | 0.0270 | 1.0000e+00 | ❌ No | [-0.0675, 0.1214] |
| gemma4:latest_baseline vs gpt-oss:20b_baseline | 0.0001 | 1.0000e+00 | ❌ No | [-0.0943, 0.0945] |
| gemma4:latest_baseline vs gpt-oss:20b_kb_rag | 0.0309 | 9.9990e-01 | ❌ No | [-0.0635, 0.1253] |
| gemma4:latest_baseline vs llama3.1:8b_baseline | -0.0491 | 9.6250e-01 | ❌ No | [-0.1435, 0.0453] |
| gemma4:latest_baseline vs llama3.1:8b_kb_rag | -0.0351 | 9.9950e-01 | ❌ No | [-0.1295, 0.0593] |
| gemma4:latest_baseline vs llama3.2:latest_baseline | -0.1281 | 2.0000e-04 | ✅ Yes | [-0.2225, -0.0337] |
| gemma4:latest_baseline vs llama3.2:latest_kb_rag | -0.0499 | 9.5590e-01 | ❌ No | [-0.1443, 0.0445] |
| gemma4:latest_baseline vs mistral-nemo:latest_baseline | -0.1394 | 0.0000e+00 | ✅ Yes | [-0.2338, -0.0450] |
| gemma4:latest_baseline vs mistral-nemo:latest_kb_rag | -0.1910 | 0.0000e+00 | ✅ Yes | [-0.2854, -0.0966] |
| gemma4:latest_baseline vs nemotron-mini:4b_baseline | -0.4785 | 0.0000e+00 | ✅ Yes | [-0.5729, -0.3841] |
| gemma4:latest_baseline vs nemotron-mini:4b_kb_rag | -0.3300 | 0.0000e+00 | ✅ Yes | [-0.4244, -0.2356] |
| gemma4:latest_baseline vs qwen3:8b_baseline | -0.0596 | 7.9770e-01 | ❌ No | [-0.1540, 0.0348] |
| gemma4:latest_baseline vs qwen3:8b_kb_rag | -0.0562 | 8.7050e-01 | ❌ No | [-0.1506, 0.0382] |
| gemma4:latest_kb_rag vs gpt-oss:20b_baseline | -0.0269 | 1.0000e+00 | ❌ No | [-0.1213, 0.0675] |
| gemma4:latest_kb_rag vs gpt-oss:20b_kb_rag | 0.0039 | 1.0000e+00 | ❌ No | [-0.0905, 0.0983] |
| gemma4:latest_kb_rag vs llama3.1:8b_baseline | -0.0761 | 3.2800e-01 | ❌ No | [-0.1705, 0.0183] |
| gemma4:latest_kb_rag vs llama3.1:8b_kb_rag | -0.0621 | 7.3430e-01 | ❌ No | [-0.1565, 0.0324] |
| gemma4:latest_kb_rag vs llama3.2:latest_baseline | -0.1550 | 0.0000e+00 | ✅ Yes | [-0.2495, -0.0606] |
| gemma4:latest_kb_rag vs llama3.2:latest_kb_rag | -0.0769 | 3.0840e-01 | ❌ No | [-0.1713, 0.0176] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_baseline | -0.1663 | 0.0000e+00 | ✅ Yes | [-0.2608, -0.0719] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.2180 | 0.0000e+00 | ✅ Yes | [-0.3124, -0.1236] |
| gemma4:latest_kb_rag vs nemotron-mini:4b_baseline | -0.5054 | 0.0000e+00 | ✅ Yes | [-0.5998, -0.4110] |
| gemma4:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.3569 | 0.0000e+00 | ✅ Yes | [-0.4513, -0.2625] |
| gemma4:latest_kb_rag vs qwen3:8b_baseline | -0.0865 | 1.2460e-01 | ❌ No | [-0.1809, 0.0079] |
| gemma4:latest_kb_rag vs qwen3:8b_kb_rag | -0.0831 | 1.7650e-01 | ❌ No | [-0.1775, 0.0113] |
| gpt-oss:20b_baseline vs gpt-oss:20b_kb_rag | 0.0308 | 9.9990e-01 | ❌ No | [-0.0636, 0.1252] |
| gpt-oss:20b_baseline vs llama3.1:8b_baseline | -0.0492 | 9.6180e-01 | ❌ No | [-0.1436, 0.0452] |
| gpt-oss:20b_baseline vs llama3.1:8b_kb_rag | -0.0352 | 9.9950e-01 | ❌ No | [-0.1296, 0.0592] |
| gpt-oss:20b_baseline vs llama3.2:latest_baseline | -0.1282 | 2.0000e-04 | ✅ Yes | [-0.2226, -0.0338] |
| gpt-oss:20b_baseline vs llama3.2:latest_kb_rag | -0.0500 | 9.5510e-01 | ❌ No | [-0.1444, 0.0444] |
| gpt-oss:20b_baseline vs mistral-nemo:latest_baseline | -0.1395 | 0.0000e+00 | ✅ Yes | [-0.2339, -0.0451] |
| gpt-oss:20b_baseline vs mistral-nemo:latest_kb_rag | -0.1911 | 0.0000e+00 | ✅ Yes | [-0.2855, -0.0967] |
| gpt-oss:20b_baseline vs nemotron-mini:4b_baseline | -0.4786 | 0.0000e+00 | ✅ Yes | [-0.5730, -0.3841] |
| gpt-oss:20b_baseline vs nemotron-mini:4b_kb_rag | -0.3301 | 0.0000e+00 | ✅ Yes | [-0.4245, -0.2356] |
| gpt-oss:20b_baseline vs qwen3:8b_baseline | -0.0597 | 7.9570e-01 | ❌ No | [-0.1541, 0.0348] |
| gpt-oss:20b_baseline vs qwen3:8b_kb_rag | -0.0562 | 8.6890e-01 | ❌ No | [-0.1507, 0.0382] |
| gpt-oss:20b_kb_rag vs llama3.1:8b_baseline | -0.0800 | 2.3590e-01 | ❌ No | [-0.1744, 0.0144] |
| gpt-oss:20b_kb_rag vs llama3.1:8b_kb_rag | -0.0660 | 6.2120e-01 | ❌ No | [-0.1604, 0.0284] |
| gpt-oss:20b_kb_rag vs llama3.2:latest_baseline | -0.1590 | 0.0000e+00 | ✅ Yes | [-0.2534, -0.0646] |
| gpt-oss:20b_kb_rag vs llama3.2:latest_kb_rag | -0.0808 | 2.1990e-01 | ❌ No | [-0.1752, 0.0136] |
| gpt-oss:20b_kb_rag vs mistral-nemo:latest_baseline | -0.1703 | 0.0000e+00 | ✅ Yes | [-0.2647, -0.0759] |
| gpt-oss:20b_kb_rag vs mistral-nemo:latest_kb_rag | -0.2219 | 0.0000e+00 | ✅ Yes | [-0.3163, -0.1275] |
| gpt-oss:20b_kb_rag vs nemotron-mini:4b_baseline | -0.5094 | 0.0000e+00 | ✅ Yes | [-0.6038, -0.4149] |
| gpt-oss:20b_kb_rag vs nemotron-mini:4b_kb_rag | -0.3609 | 0.0000e+00 | ✅ Yes | [-0.4553, -0.2664] |
| gpt-oss:20b_kb_rag vs qwen3:8b_baseline | -0.0905 | 8.0400e-02 | ❌ No | [-0.1849, 0.0039] |
| gpt-oss:20b_kb_rag vs qwen3:8b_kb_rag | -0.0871 | 1.1780e-01 | ❌ No | [-0.1815, 0.0074] |
| llama3.1:8b_baseline vs llama3.1:8b_kb_rag | 0.0140 | 1.0000e+00 | ❌ No | [-0.0804, 0.1084] |
| llama3.1:8b_baseline vs llama3.2:latest_baseline | -0.0790 | 2.5860e-01 | ❌ No | [-0.1734, 0.0154] |
| llama3.1:8b_baseline vs llama3.2:latest_kb_rag | -0.0008 | 1.0000e+00 | ❌ No | [-0.0952, 0.0936] |
| llama3.1:8b_baseline vs mistral-nemo:latest_baseline | -0.0903 | 8.2300e-02 | ❌ No | [-0.1847, 0.0041] |
| llama3.1:8b_baseline vs mistral-nemo:latest_kb_rag | -0.1419 | 0.0000e+00 | ✅ Yes | [-0.2363, -0.0475] |
| llama3.1:8b_baseline vs nemotron-mini:4b_baseline | -0.4293 | 0.0000e+00 | ✅ Yes | [-0.5238, -0.3349] |
| llama3.1:8b_baseline vs nemotron-mini:4b_kb_rag | -0.2808 | 0.0000e+00 | ✅ Yes | [-0.3753, -0.1864] |
| llama3.1:8b_baseline vs qwen3:8b_baseline | -0.0105 | 1.0000e+00 | ❌ No | [-0.1049, 0.0840] |
| llama3.1:8b_baseline vs qwen3:8b_kb_rag | -0.0070 | 1.0000e+00 | ❌ No | [-0.1015, 0.0874] |
| llama3.1:8b_kb_rag vs llama3.2:latest_baseline | -0.0930 | 5.9600e-02 | ❌ No | [-0.1874, 0.0014] |
| llama3.1:8b_kb_rag vs llama3.2:latest_kb_rag | -0.0148 | 1.0000e+00 | ❌ No | [-0.1092, 0.0796] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_baseline | -0.1043 | 1.3100e-02 | ✅ Yes | [-0.1987, -0.0099] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_kb_rag | -0.1559 | 0.0000e+00 | ✅ Yes | [-0.2503, -0.0615] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_baseline | -0.4434 | 0.0000e+00 | ✅ Yes | [-0.5378, -0.3490] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_kb_rag | -0.2949 | 0.0000e+00 | ✅ Yes | [-0.3893, -0.2005] |
| llama3.1:8b_kb_rag vs qwen3:8b_baseline | -0.0245 | 1.0000e+00 | ❌ No | [-0.1189, 0.0699] |
| llama3.1:8b_kb_rag vs qwen3:8b_kb_rag | -0.0211 | 1.0000e+00 | ❌ No | [-0.1155, 0.0733] |
| llama3.2:latest_baseline vs llama3.2:latest_kb_rag | 0.0782 | 2.7640e-01 | ❌ No | [-0.0162, 0.1726] |
| llama3.2:latest_baseline vs mistral-nemo:latest_baseline | -0.0113 | 1.0000e+00 | ❌ No | [-0.1057, 0.0831] |
| llama3.2:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0630 | 7.0970e-01 | ❌ No | [-0.1574, 0.0315] |
| llama3.2:latest_baseline vs nemotron-mini:4b_baseline | -0.3504 | 0.0000e+00 | ✅ Yes | [-0.4448, -0.2560] |
| llama3.2:latest_baseline vs nemotron-mini:4b_kb_rag | -0.2019 | 0.0000e+00 | ✅ Yes | [-0.2963, -0.1075] |
| llama3.2:latest_baseline vs qwen3:8b_baseline | 0.0685 | 5.4480e-01 | ❌ No | [-0.0259, 0.1629] |
| llama3.2:latest_baseline vs qwen3:8b_kb_rag | 0.0719 | 4.4260e-01 | ❌ No | [-0.0225, 0.1663] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_baseline | -0.0895 | 9.0000e-02 | ❌ No | [-0.1839, 0.0049] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.1411 | 0.0000e+00 | ✅ Yes | [-0.2355, -0.0467] |
| llama3.2:latest_kb_rag vs nemotron-mini:4b_baseline | -0.4286 | 0.0000e+00 | ✅ Yes | [-0.5230, -0.3342] |
| llama3.2:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.2801 | 0.0000e+00 | ✅ Yes | [-0.3745, -0.1857] |
| llama3.2:latest_kb_rag vs qwen3:8b_baseline | -0.0097 | 1.0000e+00 | ❌ No | [-0.1041, 0.0847] |
| llama3.2:latest_kb_rag vs qwen3:8b_kb_rag | -0.0063 | 1.0000e+00 | ❌ No | [-0.1007, 0.0881] |
| mistral-nemo:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0517 | 9.3810e-01 | ❌ No | [-0.1461, 0.0428] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_baseline | -0.3391 | 0.0000e+00 | ✅ Yes | [-0.4335, -0.2447] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_kb_rag | -0.1906 | 0.0000e+00 | ✅ Yes | [-0.2850, -0.0962] |
| mistral-nemo:latest_baseline vs qwen3:8b_baseline | 0.0798 | 2.4020e-01 | ❌ No | [-0.0146, 0.1742] |
| mistral-nemo:latest_baseline vs qwen3:8b_kb_rag | 0.0832 | 1.7470e-01 | ❌ No | [-0.0112, 0.1776] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_baseline | -0.2874 | 0.0000e+00 | ✅ Yes | [-0.3818, -0.1930] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.1389 | 0.0000e+00 | ✅ Yes | [-0.2333, -0.0445] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_baseline | 0.1315 | 1.0000e-04 | ✅ Yes | [0.0371, 0.2259] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_kb_rag | 0.1349 | 1.0000e-04 | ✅ Yes | [0.0405, 0.2293] |
| nemotron-mini:4b_baseline vs nemotron-mini:4b_kb_rag | 0.1485 | 0.0000e+00 | ✅ Yes | [0.0541, 0.2429] |
| nemotron-mini:4b_baseline vs qwen3:8b_baseline | 0.4189 | 0.0000e+00 | ✅ Yes | [0.3245, 0.5133] |
| nemotron-mini:4b_baseline vs qwen3:8b_kb_rag | 0.4223 | 0.0000e+00 | ✅ Yes | [0.3279, 0.5167] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_baseline | 0.2704 | 0.0000e+00 | ✅ Yes | [0.1760, 0.3648] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_kb_rag | 0.2738 | 0.0000e+00 | ✅ Yes | [0.1794, 0.3682] |
| qwen3:8b_baseline vs qwen3:8b_kb_rag | 0.0034 | 1.0000e+00 | ❌ No | [-0.0910, 0.0978] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 7 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline | 0.3034 | 0.2999 | -0.0034 | 📉 Decreased |
| deepseek-r1:1.5b_kb_rag | 0.3325 | 0.3362 | +0.0037 | 📈 Improved |
| gemma4:12b-mlx_baseline | 0.7782 | 0.7807 | +0.0024 | 📈 Improved |
| gemma4:12b-mlx_kb_rag | 0.7991 | 0.8011 | +0.0020 | 📈 Improved |
| gemma4:31b-cloud_baseline | 0.5483 | 0.5566 | +0.0082 | 📈 Improved |
| gemma4:31b-cloud_kb_rag | 0.5765 | 0.5697 | -0.0069 | 📉 Decreased |
| gemma4:31b-mlx_baseline | 0.8170 | 0.8192 | +0.0021 | 📈 Improved |
| gemma4:31b-mlx_kb_rag | 0.8250 | 0.8269 | +0.0019 | 📈 Improved |
| gemma4:latest_baseline | 0.7472 | 0.7445 | -0.0027 | 📉 Decreased |
| gemma4:latest_kb_rag | 0.7741 | 0.7732 | -0.0010 | 📉 Decreased |
| gpt-oss:20b_baseline | 0.7473 | 0.7511 | +0.0039 | 📈 Improved |
| gpt-oss:20b_kb_rag | 0.7781 | 0.7765 | -0.0015 | 📉 Decreased |
| llama3.1:8b_baseline | 0.6981 | 0.6971 | -0.0010 | 📉 Decreased |
| llama3.1:8b_kb_rag | 0.7121 | 0.7124 | +0.0003 | 📈 Improved |
| llama3.2:latest_baseline | 0.6191 | 0.6166 | -0.0025 | 📉 Decreased |
| llama3.2:latest_kb_rag | 0.6973 | 0.6959 | -0.0014 | 📉 Decreased |
| mistral-nemo:latest_baseline | 0.6078 | 0.6062 | -0.0016 | 📉 Decreased |
| mistral-nemo:latest_kb_rag | 0.5561 | 0.5513 | -0.0048 | 📉 Decreased |
| nemotron-mini:4b_baseline | 0.2687 | 0.2597 | -0.0090 | 📉 Decreased |
| nemotron-mini:4b_kb_rag | 0.4172 | 0.4205 | +0.0033 | 📈 Improved |
| qwen3:8b_baseline | 0.6876 | 0.6895 | +0.0018 | 📈 Improved |
| qwen3:8b_kb_rag | 0.6910 | 0.6912 | +0.0002 | 📈 Improved |