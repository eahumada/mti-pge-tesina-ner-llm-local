# 🔗 Merged Benchmark Analysis — Provenance & Integrity

- **Corpus:** `data/benchmark_balanced_120.json`
- **Registros esperados por modelo+modo:** 113
- **Corridas combinadas:** 13
- **Grupos (modelo+modo) analizados:** 26
- **Filas totales tras el merge:** 2938

## Fuentes
| # | Corrida | CSV | Filas | Modelos aportados |
| :---: | :--- | :--- | :---: | :---: |
| 1 | deepseek-r1_1.5b__N120 | `results/recorrida_20260908/deepseek-r1_1.5b__N120/benchmark_results.csv` | 240 | 2 |
| 2 | gemma4_12b-mlx__N120 | `results/recorrida_20260908/gemma4_12b-mlx__N120/benchmark_results.csv` | 240 | 2 |
| 3 | gemma4_31b-cloud__N120 | `results/recorrida_20260908/gemma4_31b-cloud__N120/benchmark_results.csv` | 240 | 2 |
| 4 | gemma4_31b-mlx__N120 | `results/recorrida_20260908/gemma4_31b-mlx__N120/benchmark_results.csv` | 240 | 2 |
| 5 | gemma4_latest__N120 | `results/recorrida_20260908/gemma4_latest__N120/benchmark_results.csv` | 240 | 2 |
| 6 | gemma_latest__N120 | `results/recorrida_20260908/gemma_latest__N120/benchmark_results.csv` | 240 | 2 |
| 7 | gpt-oss_20b__N120 | `results/recorrida_20260908/gpt-oss_20b__N120/benchmark_results.csv` | 240 | 2 |
| 8 | llama3.1_8b__N120 | `results/recorrida_20260908/llama3.1_8b__N120/benchmark_results.csv` | 240 | 2 |
| 9 | llama3.2_latest__N120 | `results/recorrida_20260908/llama3.2_latest__N120/benchmark_results.csv` | 240 | 2 |
| 10 | mistral-nemo_latest__N120 | `results/recorrida_20260908/mistral-nemo_latest__N120/benchmark_results.csv` | 240 | 2 |
| 11 | nemotron-mini_4b__N120 | `results/recorrida_20260908/nemotron-mini_4b__N120/benchmark_results.csv` | 240 | 2 |
| 12 | qwen2.5_14b__N120 | `results/recorrida_20260908/qwen2.5_14b__N120/benchmark_results.csv` | 240 | 2 |
| 13 | qwen3_8b__N120 | `results/recorrida_20260908/qwen3_8b__N120/benchmark_results.csv` | 240 | 2 |

## Integridad por grupo (modelo + modo)
| Modelo | Filas | record_id unicos | Esperados | f1 NaN | Estado |
| :--- | :---: | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline | 113 | 113 | 113 | 0 | ✅ OK |
| deepseek-r1:1.5b_kb_rag | 113 | 113 | 113 | 0 | ✅ OK |
| gemma4:12b-mlx_baseline | 113 | 113 | 113 | 0 | ✅ OK |
| gemma4:12b-mlx_kb_rag | 113 | 113 | 113 | 0 | ✅ OK |
| gemma4:31b-cloud_baseline | 113 | 113 | 113 | 0 | ✅ OK |
| gemma4:31b-cloud_kb_rag | 113 | 113 | 113 | 0 | ✅ OK |
| gemma4:31b-mlx_baseline | 113 | 113 | 113 | 0 | ✅ OK |
| gemma4:31b-mlx_kb_rag | 113 | 113 | 113 | 0 | ✅ OK |
| gemma4:latest_baseline | 113 | 113 | 113 | 0 | ✅ OK |
| gemma4:latest_kb_rag | 113 | 113 | 113 | 0 | ✅ OK |
| gemma:latest_baseline | 113 | 113 | 113 | 0 | ✅ OK |
| gemma:latest_kb_rag | 113 | 113 | 113 | 0 | ✅ OK |
| gpt-oss:20b_baseline | 113 | 113 | 113 | 0 | ✅ OK |
| gpt-oss:20b_kb_rag | 113 | 113 | 113 | 0 | ✅ OK |
| llama3.1:8b_baseline | 113 | 113 | 113 | 0 | ✅ OK |
| llama3.1:8b_kb_rag | 113 | 113 | 113 | 0 | ✅ OK |
| llama3.2:latest_baseline | 113 | 113 | 113 | 0 | ✅ OK |
| llama3.2:latest_kb_rag | 113 | 113 | 113 | 0 | ✅ OK |
| mistral-nemo:latest_baseline | 113 | 113 | 113 | 0 | ✅ OK |
| mistral-nemo:latest_kb_rag | 113 | 113 | 113 | 0 | ✅ OK |
| nemotron-mini:4b_baseline | 113 | 113 | 113 | 0 | ✅ OK |
| nemotron-mini:4b_kb_rag | 113 | 113 | 113 | 0 | ✅ OK |
| qwen2.5:14b_baseline | 113 | 113 | 113 | 0 | ✅ OK |
| qwen2.5:14b_kb_rag | 113 | 113 | 113 | 0 | ✅ OK |
| qwen3:8b_baseline | 113 | 113 | 113 | 0 | ✅ OK |
| qwen3:8b_kb_rag | 113 | 113 | 113 | 0 | ✅ OK |

## Advertencias
- Ninguna. Corpus consistente, sin duplicados y todos los grupos completos.

---
# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 121.5602
- **p-Value:** 0.0000e+00

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline | 113 | 0.2873 | 0.2578 | 0.3168 | 0.1583 |
| deepseek-r1:1.5b_kb_rag | 113 | 0.3080 | 0.2753 | 0.3407 | 0.1754 |
| gemma4:12b-mlx_baseline | 113 | 0.7767 | 0.7503 | 0.8031 | 0.1418 |
| gemma4:12b-mlx_kb_rag | 113 | 0.7996 | 0.7743 | 0.8249 | 0.1358 |
| gemma4:31b-cloud_baseline | 113 | 0.8213 | 0.7962 | 0.8464 | 0.1346 |
| gemma4:31b-cloud_kb_rag | 113 | 0.8294 | 0.8049 | 0.8540 | 0.1317 |
| gemma4:31b-mlx_baseline | 113 | 0.8147 | 0.7889 | 0.8406 | 0.1387 |
| gemma4:31b-mlx_kb_rag | 113 | 0.8244 | 0.7997 | 0.8491 | 0.1324 |
| gemma4:latest_baseline | 113 | 0.7533 | 0.7257 | 0.7809 | 0.1479 |
| gemma4:latest_kb_rag | 113 | 0.7786 | 0.7522 | 0.8050 | 0.1416 |
| gemma:latest_baseline | 113 | 0.5955 | 0.5610 | 0.6299 | 0.1850 |
| gemma:latest_kb_rag | 113 | 0.5958 | 0.5602 | 0.6313 | 0.1907 |
| gpt-oss:20b_baseline | 113 | 0.7541 | 0.7268 | 0.7815 | 0.1466 |
| gpt-oss:20b_kb_rag | 113 | 0.7708 | 0.7454 | 0.7961 | 0.1359 |
| llama3.1:8b_baseline | 113 | 0.6917 | 0.6637 | 0.7197 | 0.1503 |
| llama3.1:8b_kb_rag | 113 | 0.7148 | 0.6854 | 0.7442 | 0.1576 |
| llama3.2:latest_baseline | 113 | 0.6325 | 0.5991 | 0.6660 | 0.1796 |
| llama3.2:latest_kb_rag | 113 | 0.6998 | 0.6697 | 0.7299 | 0.1615 |
| mistral-nemo:latest_baseline | 113 | 0.6063 | 0.5720 | 0.6406 | 0.1840 |
| mistral-nemo:latest_kb_rag | 113 | 0.5635 | 0.5288 | 0.5982 | 0.1862 |
| nemotron-mini:4b_baseline | 113 | 0.2631 | 0.2208 | 0.3055 | 0.2273 |
| nemotron-mini:4b_kb_rag | 113 | 0.4055 | 0.3709 | 0.4400 | 0.1853 |
| qwen2.5:14b_baseline | 113 | 0.6961 | 0.6681 | 0.7242 | 0.1503 |
| qwen2.5:14b_kb_rag | 113 | 0.7031 | 0.6732 | 0.7329 | 0.1601 |
| qwen3:8b_baseline | 113 | 0.6903 | 0.6607 | 0.7199 | 0.1586 |
| qwen3:8b_kb_rag | 113 | 0.6898 | 0.6614 | 0.7182 | 0.1523 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline vs deepseek-r1:1.5b_kb_rag | 0.0207 | 1.0000e+00 | ❌ No | [-0.0583, 0.0997] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_baseline | 0.4894 | 0.0000e+00 | ✅ Yes | [0.4104, 0.5683] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_kb_rag | 0.5123 | 0.0000e+00 | ✅ Yes | [0.4333, 0.5913] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_baseline | 0.5340 | 0.0000e+00 | ✅ Yes | [0.4550, 0.6130] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_kb_rag | 0.5421 | 0.0000e+00 | ✅ Yes | [0.4631, 0.6211] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_baseline | 0.5274 | 0.0000e+00 | ✅ Yes | [0.4484, 0.6063] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_kb_rag | 0.5371 | 0.0000e+00 | ✅ Yes | [0.4581, 0.6161] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_baseline | 0.4660 | 0.0000e+00 | ✅ Yes | [0.3870, 0.5449] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_kb_rag | 0.4913 | 0.0000e+00 | ✅ Yes | [0.4123, 0.5702] |
| deepseek-r1:1.5b_baseline vs gemma:latest_baseline | 0.3081 | 0.0000e+00 | ✅ Yes | [0.2292, 0.3871] |
| deepseek-r1:1.5b_baseline vs gemma:latest_kb_rag | 0.3085 | 0.0000e+00 | ✅ Yes | [0.2295, 0.3874] |
| deepseek-r1:1.5b_baseline vs gpt-oss:20b_baseline | 0.4668 | 0.0000e+00 | ✅ Yes | [0.3878, 0.5458] |
| deepseek-r1:1.5b_baseline vs gpt-oss:20b_kb_rag | 0.4834 | 0.0000e+00 | ✅ Yes | [0.4045, 0.5624] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_baseline | 0.4044 | 0.0000e+00 | ✅ Yes | [0.3254, 0.4833] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_kb_rag | 0.4275 | 0.0000e+00 | ✅ Yes | [0.3485, 0.5064] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_baseline | 0.3452 | 0.0000e+00 | ✅ Yes | [0.2662, 0.4242] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_kb_rag | 0.4125 | 0.0000e+00 | ✅ Yes | [0.3335, 0.4915] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_baseline | 0.3190 | 0.0000e+00 | ✅ Yes | [0.2400, 0.3980] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_kb_rag | 0.2761 | 0.0000e+00 | ✅ Yes | [0.1972, 0.3551] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_baseline | -0.0242 | 1.0000e+00 | ❌ No | [-0.1032, 0.0547] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_kb_rag | 0.1181 | 0.0000e+00 | ✅ Yes | [0.0391, 0.1971] |
| deepseek-r1:1.5b_baseline vs qwen2.5:14b_baseline | 0.4088 | 0.0000e+00 | ✅ Yes | [0.3298, 0.4878] |
| deepseek-r1:1.5b_baseline vs qwen2.5:14b_kb_rag | 0.4157 | 0.0000e+00 | ✅ Yes | [0.3368, 0.4947] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_baseline | 0.4030 | 0.0000e+00 | ✅ Yes | [0.3240, 0.4819] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_kb_rag | 0.4025 | 0.0000e+00 | ✅ Yes | [0.3235, 0.4814] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_baseline | 0.4687 | 0.0000e+00 | ✅ Yes | [0.3897, 0.5477] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_kb_rag | 0.4916 | 0.0000e+00 | ✅ Yes | [0.4126, 0.5706] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-cloud_baseline | 0.5133 | 0.0000e+00 | ✅ Yes | [0.4343, 0.5923] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-cloud_kb_rag | 0.5214 | 0.0000e+00 | ✅ Yes | [0.4424, 0.6004] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-mlx_baseline | 0.5067 | 0.0000e+00 | ✅ Yes | [0.4277, 0.5856] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-mlx_kb_rag | 0.5164 | 0.0000e+00 | ✅ Yes | [0.4374, 0.5954] |
| deepseek-r1:1.5b_kb_rag vs gemma4:latest_baseline | 0.4453 | 0.0000e+00 | ✅ Yes | [0.3663, 0.5242] |
| deepseek-r1:1.5b_kb_rag vs gemma4:latest_kb_rag | 0.4706 | 0.0000e+00 | ✅ Yes | [0.3916, 0.5495] |
| deepseek-r1:1.5b_kb_rag vs gemma:latest_baseline | 0.2874 | 0.0000e+00 | ✅ Yes | [0.2085, 0.3664] |
| deepseek-r1:1.5b_kb_rag vs gemma:latest_kb_rag | 0.2878 | 0.0000e+00 | ✅ Yes | [0.2088, 0.3667] |
| deepseek-r1:1.5b_kb_rag vs gpt-oss:20b_baseline | 0.4461 | 0.0000e+00 | ✅ Yes | [0.3671, 0.5251] |
| deepseek-r1:1.5b_kb_rag vs gpt-oss:20b_kb_rag | 0.4627 | 0.0000e+00 | ✅ Yes | [0.3838, 0.5417] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_baseline | 0.3837 | 0.0000e+00 | ✅ Yes | [0.3047, 0.4626] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_kb_rag | 0.4068 | 0.0000e+00 | ✅ Yes | [0.3278, 0.4857] |
| deepseek-r1:1.5b_kb_rag vs llama3.2:latest_baseline | 0.3245 | 0.0000e+00 | ✅ Yes | [0.2455, 0.4035] |
| deepseek-r1:1.5b_kb_rag vs llama3.2:latest_kb_rag | 0.3918 | 0.0000e+00 | ✅ Yes | [0.3128, 0.4708] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_baseline | 0.2983 | 0.0000e+00 | ✅ Yes | [0.2193, 0.3773] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_kb_rag | 0.2554 | 0.0000e+00 | ✅ Yes | [0.1765, 0.3344] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_baseline | -0.0449 | 9.3580e-01 | ❌ No | [-0.1239, 0.0341] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_kb_rag | 0.0974 | 1.7000e-03 | ✅ Yes | [0.0185, 0.1764] |
| deepseek-r1:1.5b_kb_rag vs qwen2.5:14b_baseline | 0.3881 | 0.0000e+00 | ✅ Yes | [0.3091, 0.4671] |
| deepseek-r1:1.5b_kb_rag vs qwen2.5:14b_kb_rag | 0.3950 | 0.0000e+00 | ✅ Yes | [0.3161, 0.4740] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_baseline | 0.3823 | 0.0000e+00 | ✅ Yes | [0.3033, 0.4612] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_kb_rag | 0.3818 | 0.0000e+00 | ✅ Yes | [0.3028, 0.4607] |
| gemma4:12b-mlx_baseline vs gemma4:12b-mlx_kb_rag | 0.0229 | 1.0000e+00 | ❌ No | [-0.0561, 0.1019] |
| gemma4:12b-mlx_baseline vs gemma4:31b-cloud_baseline | 0.0446 | 9.4020e-01 | ❌ No | [-0.0344, 0.1236] |
| gemma4:12b-mlx_baseline vs gemma4:31b-cloud_kb_rag | 0.0527 | 7.4600e-01 | ❌ No | [-0.0262, 0.1317] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_baseline | 0.0380 | 9.9130e-01 | ❌ No | [-0.0410, 0.1170] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_kb_rag | 0.0477 | 8.8500e-01 | ❌ No | [-0.0312, 0.1267] |
| gemma4:12b-mlx_baseline vs gemma4:latest_baseline | -0.0234 | 1.0000e+00 | ❌ No | [-0.1024, 0.0556] |
| gemma4:12b-mlx_baseline vs gemma4:latest_kb_rag | 0.0019 | 1.0000e+00 | ❌ No | [-0.0771, 0.0809] |
| gemma4:12b-mlx_baseline vs gemma:latest_baseline | -0.1813 | 0.0000e+00 | ✅ Yes | [-0.2602, -0.1023] |
| gemma4:12b-mlx_baseline vs gemma:latest_kb_rag | -0.1809 | 0.0000e+00 | ✅ Yes | [-0.2599, -0.1020] |
| gemma4:12b-mlx_baseline vs gpt-oss:20b_baseline | -0.0226 | 1.0000e+00 | ❌ No | [-0.1016, 0.0564] |
| gemma4:12b-mlx_baseline vs gpt-oss:20b_kb_rag | -0.0059 | 1.0000e+00 | ❌ No | [-0.0849, 0.0730] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_baseline | -0.0850 | 1.8400e-02 | ✅ Yes | [-0.1640, -0.0060] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_kb_rag | -0.0619 | 4.0780e-01 | ❌ No | [-0.1409, 0.0171] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_baseline | -0.1442 | 0.0000e+00 | ✅ Yes | [-0.2231, -0.0652] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_kb_rag | -0.0769 | 6.8700e-02 | ❌ No | [-0.1558, 0.0021] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_baseline | -0.1704 | 0.0000e+00 | ✅ Yes | [-0.2494, -0.0914] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.2133 | 0.0000e+00 | ✅ Yes | [-0.2922, -0.1343] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_baseline | -0.5136 | 0.0000e+00 | ✅ Yes | [-0.5926, -0.4346] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_kb_rag | -0.3713 | 0.0000e+00 | ✅ Yes | [-0.4502, -0.2923] |
| gemma4:12b-mlx_baseline vs qwen2.5:14b_baseline | -0.0806 | 3.8800e-02 | ✅ Yes | [-0.1595, -0.0016] |
| gemma4:12b-mlx_baseline vs qwen2.5:14b_kb_rag | -0.0737 | 1.0880e-01 | ❌ No | [-0.1526, 0.0053] |
| gemma4:12b-mlx_baseline vs qwen3:8b_baseline | -0.0864 | 1.4300e-02 | ✅ Yes | [-0.1654, -0.0074] |
| gemma4:12b-mlx_baseline vs qwen3:8b_kb_rag | -0.0869 | 1.3100e-02 | ✅ Yes | [-0.1659, -0.0080] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-cloud_baseline | 0.0217 | 1.0000e+00 | ❌ No | [-0.0573, 0.1007] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-cloud_kb_rag | 0.0298 | 9.9980e-01 | ❌ No | [-0.0492, 0.1088] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_baseline | 0.0151 | 1.0000e+00 | ❌ No | [-0.0639, 0.0940] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_kb_rag | 0.0248 | 1.0000e+00 | ❌ No | [-0.0542, 0.1038] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_baseline | -0.0463 | 9.1280e-01 | ❌ No | [-0.1253, 0.0326] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0210 | 1.0000e+00 | ❌ No | [-0.1000, 0.0579] |
| gemma4:12b-mlx_kb_rag vs gemma:latest_baseline | -0.2042 | 0.0000e+00 | ✅ Yes | [-0.2831, -0.1252] |
| gemma4:12b-mlx_kb_rag vs gemma:latest_kb_rag | -0.2038 | 0.0000e+00 | ✅ Yes | [-0.2828, -0.1249] |
| gemma4:12b-mlx_kb_rag vs gpt-oss:20b_baseline | -0.0455 | 9.2670e-01 | ❌ No | [-0.1245, 0.0335] |
| gemma4:12b-mlx_kb_rag vs gpt-oss:20b_kb_rag | -0.0289 | 9.9990e-01 | ❌ No | [-0.1078, 0.0501] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_baseline | -0.1079 | 2.0000e-04 | ✅ Yes | [-0.1869, -0.0290] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_kb_rag | -0.0848 | 1.8900e-02 | ✅ Yes | [-0.1638, -0.0059] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_baseline | -0.1671 | 0.0000e+00 | ✅ Yes | [-0.2461, -0.0881] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.0998 | 1.0000e-03 | ✅ Yes | [-0.1788, -0.0208] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.1933 | 0.0000e+00 | ✅ Yes | [-0.2723, -0.1143] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.2362 | 0.0000e+00 | ✅ Yes | [-0.3151, -0.1572] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_baseline | -0.5365 | 0.0000e+00 | ✅ Yes | [-0.6155, -0.4575] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | -0.3942 | 0.0000e+00 | ✅ Yes | [-0.4731, -0.3152] |
| gemma4:12b-mlx_kb_rag vs qwen2.5:14b_baseline | -0.1035 | 4.0000e-04 | ✅ Yes | [-0.1825, -0.0245] |
| gemma4:12b-mlx_kb_rag vs qwen2.5:14b_kb_rag | -0.0966 | 2.0000e-03 | ✅ Yes | [-0.1755, -0.0176] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_baseline | -0.1093 | 1.0000e-04 | ✅ Yes | [-0.1883, -0.0304] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.1098 | 1.0000e-04 | ✅ Yes | [-0.1888, -0.0309] |
| gemma4:31b-cloud_baseline vs gemma4:31b-cloud_kb_rag | 0.0081 | 1.0000e+00 | ❌ No | [-0.0709, 0.0871] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_baseline | -0.0066 | 1.0000e+00 | ❌ No | [-0.0856, 0.0724] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_kb_rag | 0.0031 | 1.0000e+00 | ❌ No | [-0.0759, 0.0821] |
| gemma4:31b-cloud_baseline vs gemma4:latest_baseline | -0.0680 | 2.2080e-01 | ❌ No | [-0.1470, 0.0110] |
| gemma4:31b-cloud_baseline vs gemma4:latest_kb_rag | -0.0427 | 9.6260e-01 | ❌ No | [-0.1217, 0.0363] |
| gemma4:31b-cloud_baseline vs gemma:latest_baseline | -0.2259 | 0.0000e+00 | ✅ Yes | [-0.3048, -0.1469] |
| gemma4:31b-cloud_baseline vs gemma:latest_kb_rag | -0.2255 | 0.0000e+00 | ✅ Yes | [-0.3045, -0.1466] |
| gemma4:31b-cloud_baseline vs gpt-oss:20b_baseline | -0.0672 | 2.4190e-01 | ❌ No | [-0.1462, 0.0118] |
| gemma4:31b-cloud_baseline vs gpt-oss:20b_kb_rag | -0.0505 | 8.1350e-01 | ❌ No | [-0.1295, 0.0284] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_baseline | -0.1296 | 0.0000e+00 | ✅ Yes | [-0.2086, -0.0506] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_kb_rag | -0.1065 | 2.0000e-04 | ✅ Yes | [-0.1855, -0.0276] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_baseline | -0.1888 | 0.0000e+00 | ✅ Yes | [-0.2677, -0.1098] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_kb_rag | -0.1215 | 0.0000e+00 | ✅ Yes | [-0.2005, -0.0425] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_baseline | -0.2150 | 0.0000e+00 | ✅ Yes | [-0.2940, -0.1360] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_kb_rag | -0.2579 | 0.0000e+00 | ✅ Yes | [-0.3368, -0.1789] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_baseline | -0.5582 | 0.0000e+00 | ✅ Yes | [-0.6372, -0.4792] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_kb_rag | -0.4159 | 0.0000e+00 | ✅ Yes | [-0.4948, -0.3369] |
| gemma4:31b-cloud_baseline vs qwen2.5:14b_baseline | -0.1252 | 0.0000e+00 | ✅ Yes | [-0.2041, -0.0462] |
| gemma4:31b-cloud_baseline vs qwen2.5:14b_kb_rag | -0.1183 | 0.0000e+00 | ✅ Yes | [-0.1972, -0.0393] |
| gemma4:31b-cloud_baseline vs qwen3:8b_baseline | -0.1310 | 0.0000e+00 | ✅ Yes | [-0.2100, -0.0520] |
| gemma4:31b-cloud_baseline vs qwen3:8b_kb_rag | -0.1315 | 0.0000e+00 | ✅ Yes | [-0.2105, -0.0526] |
| gemma4:31b-cloud_kb_rag vs gemma4:31b-mlx_baseline | -0.0147 | 1.0000e+00 | ❌ No | [-0.0937, 0.0642] |
| gemma4:31b-cloud_kb_rag vs gemma4:31b-mlx_kb_rag | -0.0050 | 1.0000e+00 | ❌ No | [-0.0840, 0.0740] |
| gemma4:31b-cloud_kb_rag vs gemma4:latest_baseline | -0.0761 | 7.6800e-02 | ❌ No | [-0.1551, 0.0028] |
| gemma4:31b-cloud_kb_rag vs gemma4:latest_kb_rag | -0.0508 | 8.0530e-01 | ❌ No | [-0.1298, 0.0281] |
| gemma4:31b-cloud_kb_rag vs gemma:latest_baseline | -0.2340 | 0.0000e+00 | ✅ Yes | [-0.3129, -0.1550] |
| gemma4:31b-cloud_kb_rag vs gemma:latest_kb_rag | -0.2336 | 0.0000e+00 | ✅ Yes | [-0.3126, -0.1547] |
| gemma4:31b-cloud_kb_rag vs gpt-oss:20b_baseline | -0.0753 | 8.6300e-02 | ❌ No | [-0.1543, 0.0037] |
| gemma4:31b-cloud_kb_rag vs gpt-oss:20b_kb_rag | -0.0587 | 5.2850e-01 | ❌ No | [-0.1376, 0.0203] |
| gemma4:31b-cloud_kb_rag vs llama3.1:8b_baseline | -0.1377 | 0.0000e+00 | ✅ Yes | [-0.2167, -0.0588] |
| gemma4:31b-cloud_kb_rag vs llama3.1:8b_kb_rag | -0.1146 | 0.0000e+00 | ✅ Yes | [-0.1936, -0.0357] |
| gemma4:31b-cloud_kb_rag vs llama3.2:latest_baseline | -0.1969 | 0.0000e+00 | ✅ Yes | [-0.2759, -0.1179] |
| gemma4:31b-cloud_kb_rag vs llama3.2:latest_kb_rag | -0.1296 | 0.0000e+00 | ✅ Yes | [-0.2086, -0.0506] |
| gemma4:31b-cloud_kb_rag vs mistral-nemo:latest_baseline | -0.2231 | 0.0000e+00 | ✅ Yes | [-0.3021, -0.1441] |
| gemma4:31b-cloud_kb_rag vs mistral-nemo:latest_kb_rag | -0.2660 | 0.0000e+00 | ✅ Yes | [-0.3449, -0.1870] |
| gemma4:31b-cloud_kb_rag vs nemotron-mini:4b_baseline | -0.5663 | 0.0000e+00 | ✅ Yes | [-0.6453, -0.4874] |
| gemma4:31b-cloud_kb_rag vs nemotron-mini:4b_kb_rag | -0.4240 | 0.0000e+00 | ✅ Yes | [-0.5029, -0.3450] |
| gemma4:31b-cloud_kb_rag vs qwen2.5:14b_baseline | -0.1333 | 0.0000e+00 | ✅ Yes | [-0.2123, -0.0543] |
| gemma4:31b-cloud_kb_rag vs qwen2.5:14b_kb_rag | -0.1264 | 0.0000e+00 | ✅ Yes | [-0.2053, -0.0474] |
| gemma4:31b-cloud_kb_rag vs qwen3:8b_baseline | -0.1391 | 0.0000e+00 | ✅ Yes | [-0.2181, -0.0602] |
| gemma4:31b-cloud_kb_rag vs qwen3:8b_kb_rag | -0.1396 | 0.0000e+00 | ✅ Yes | [-0.2186, -0.0607] |
| gemma4:31b-mlx_baseline vs gemma4:31b-mlx_kb_rag | 0.0097 | 1.0000e+00 | ❌ No | [-0.0692, 0.0887] |
| gemma4:31b-mlx_baseline vs gemma4:latest_baseline | -0.0614 | 4.2640e-01 | ❌ No | [-0.1404, 0.0176] |
| gemma4:31b-mlx_baseline vs gemma4:latest_kb_rag | -0.0361 | 9.9570e-01 | ❌ No | [-0.1151, 0.0429] |
| gemma4:31b-mlx_baseline vs gemma:latest_baseline | -0.2192 | 0.0000e+00 | ✅ Yes | [-0.2982, -0.1403] |
| gemma4:31b-mlx_baseline vs gemma:latest_kb_rag | -0.2189 | 0.0000e+00 | ✅ Yes | [-0.2979, -0.1399] |
| gemma4:31b-mlx_baseline vs gpt-oss:20b_baseline | -0.0606 | 4.5610e-01 | ❌ No | [-0.1396, 0.0184] |
| gemma4:31b-mlx_baseline vs gpt-oss:20b_kb_rag | -0.0439 | 9.4910e-01 | ❌ No | [-0.1229, 0.0350] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_baseline | -0.1230 | 0.0000e+00 | ✅ Yes | [-0.2020, -0.0440] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_kb_rag | -0.0999 | 1.0000e-03 | ✅ Yes | [-0.1789, -0.0209] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_baseline | -0.1822 | 0.0000e+00 | ✅ Yes | [-0.2611, -0.1032] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_kb_rag | -0.1149 | 0.0000e+00 | ✅ Yes | [-0.1938, -0.0359] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_baseline | -0.2084 | 0.0000e+00 | ✅ Yes | [-0.2874, -0.1294] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.2512 | 0.0000e+00 | ✅ Yes | [-0.3302, -0.1723] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_baseline | -0.5516 | 0.0000e+00 | ✅ Yes | [-0.6306, -0.4726] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_kb_rag | -0.4093 | 0.0000e+00 | ✅ Yes | [-0.4882, -0.3303] |
| gemma4:31b-mlx_baseline vs qwen2.5:14b_baseline | -0.1186 | 0.0000e+00 | ✅ Yes | [-0.1975, -0.0396] |
| gemma4:31b-mlx_baseline vs qwen2.5:14b_kb_rag | -0.1116 | 1.0000e-04 | ✅ Yes | [-0.1906, -0.0327] |
| gemma4:31b-mlx_baseline vs qwen3:8b_baseline | -0.1244 | 0.0000e+00 | ✅ Yes | [-0.2034, -0.0454] |
| gemma4:31b-mlx_baseline vs qwen3:8b_kb_rag | -0.1249 | 0.0000e+00 | ✅ Yes | [-0.2039, -0.0459] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_baseline | -0.0711 | 1.5180e-01 | ❌ No | [-0.1501, 0.0078] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0458 | 9.2140e-01 | ❌ No | [-0.1248, 0.0331] |
| gemma4:31b-mlx_kb_rag vs gemma:latest_baseline | -0.2290 | 0.0000e+00 | ✅ Yes | [-0.3079, -0.1500] |
| gemma4:31b-mlx_kb_rag vs gemma:latest_kb_rag | -0.2286 | 0.0000e+00 | ✅ Yes | [-0.3076, -0.1497] |
| gemma4:31b-mlx_kb_rag vs gpt-oss:20b_baseline | -0.0703 | 1.6810e-01 | ❌ No | [-0.1493, 0.0087] |
| gemma4:31b-mlx_kb_rag vs gpt-oss:20b_kb_rag | -0.0537 | 7.1410e-01 | ❌ No | [-0.1326, 0.0253] |
| gemma4:31b-mlx_kb_rag vs llama3.1:8b_baseline | -0.1327 | 0.0000e+00 | ✅ Yes | [-0.2117, -0.0538] |
| gemma4:31b-mlx_kb_rag vs llama3.1:8b_kb_rag | -0.1096 | 1.0000e-04 | ✅ Yes | [-0.1886, -0.0307] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_baseline | -0.1919 | 0.0000e+00 | ✅ Yes | [-0.2709, -0.1129] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.1246 | 0.0000e+00 | ✅ Yes | [-0.2036, -0.0456] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.2181 | 0.0000e+00 | ✅ Yes | [-0.2971, -0.1391] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.2610 | 0.0000e+00 | ✅ Yes | [-0.3399, -0.1820] |
| gemma4:31b-mlx_kb_rag vs nemotron-mini:4b_baseline | -0.5613 | 0.0000e+00 | ✅ Yes | [-0.6403, -0.4824] |
| gemma4:31b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | -0.4190 | 0.0000e+00 | ✅ Yes | [-0.4979, -0.3400] |
| gemma4:31b-mlx_kb_rag vs qwen2.5:14b_baseline | -0.1283 | 0.0000e+00 | ✅ Yes | [-0.2073, -0.0493] |
| gemma4:31b-mlx_kb_rag vs qwen2.5:14b_kb_rag | -0.1214 | 0.0000e+00 | ✅ Yes | [-0.2003, -0.0424] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_baseline | -0.1341 | 0.0000e+00 | ✅ Yes | [-0.2131, -0.0552] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.1346 | 0.0000e+00 | ✅ Yes | [-0.2136, -0.0557] |
| gemma4:latest_baseline vs gemma4:latest_kb_rag | 0.0253 | 1.0000e+00 | ❌ No | [-0.0537, 0.1043] |
| gemma4:latest_baseline vs gemma:latest_baseline | -0.1578 | 0.0000e+00 | ✅ Yes | [-0.2368, -0.0789] |
| gemma4:latest_baseline vs gemma:latest_kb_rag | -0.1575 | 0.0000e+00 | ✅ Yes | [-0.2365, -0.0785] |
| gemma4:latest_baseline vs gpt-oss:20b_baseline | 0.0008 | 1.0000e+00 | ❌ No | [-0.0782, 0.0798] |
| gemma4:latest_baseline vs gpt-oss:20b_kb_rag | 0.0175 | 1.0000e+00 | ❌ No | [-0.0615, 0.0964] |
| gemma4:latest_baseline vs llama3.1:8b_baseline | -0.0616 | 4.1910e-01 | ❌ No | [-0.1406, 0.0174] |
| gemma4:latest_baseline vs llama3.1:8b_kb_rag | -0.0385 | 9.8950e-01 | ❌ No | [-0.1175, 0.0405] |
| gemma4:latest_baseline vs llama3.2:latest_baseline | -0.1208 | 0.0000e+00 | ✅ Yes | [-0.1997, -0.0418] |
| gemma4:latest_baseline vs llama3.2:latest_kb_rag | -0.0535 | 7.2040e-01 | ❌ No | [-0.1324, 0.0255] |
| gemma4:latest_baseline vs mistral-nemo:latest_baseline | -0.1470 | 0.0000e+00 | ✅ Yes | [-0.2260, -0.0680] |
| gemma4:latest_baseline vs mistral-nemo:latest_kb_rag | -0.1898 | 0.0000e+00 | ✅ Yes | [-0.2688, -0.1109] |
| gemma4:latest_baseline vs nemotron-mini:4b_baseline | -0.4902 | 0.0000e+00 | ✅ Yes | [-0.5692, -0.4112] |
| gemma4:latest_baseline vs nemotron-mini:4b_kb_rag | -0.3479 | 0.0000e+00 | ✅ Yes | [-0.4268, -0.2689] |
| gemma4:latest_baseline vs qwen2.5:14b_baseline | -0.0572 | 5.8530e-01 | ❌ No | [-0.1361, 0.0218] |
| gemma4:latest_baseline vs qwen2.5:14b_kb_rag | -0.0502 | 8.2200e-01 | ❌ No | [-0.1292, 0.0287] |
| gemma4:latest_baseline vs qwen3:8b_baseline | -0.0630 | 3.7020e-01 | ❌ No | [-0.1420, 0.0160] |
| gemma4:latest_baseline vs qwen3:8b_kb_rag | -0.0635 | 3.5280e-01 | ❌ No | [-0.1425, 0.0155] |
| gemma4:latest_kb_rag vs gemma:latest_baseline | -0.1831 | 0.0000e+00 | ✅ Yes | [-0.2621, -0.1042] |
| gemma4:latest_kb_rag vs gemma:latest_kb_rag | -0.1828 | 0.0000e+00 | ✅ Yes | [-0.2618, -0.1038] |
| gemma4:latest_kb_rag vs gpt-oss:20b_baseline | -0.0245 | 1.0000e+00 | ❌ No | [-0.1035, 0.0545] |
| gemma4:latest_kb_rag vs gpt-oss:20b_kb_rag | -0.0078 | 1.0000e+00 | ❌ No | [-0.0868, 0.0711] |
| gemma4:latest_kb_rag vs llama3.1:8b_baseline | -0.0869 | 1.3100e-02 | ✅ Yes | [-0.1659, -0.0079] |
| gemma4:latest_kb_rag vs llama3.1:8b_kb_rag | -0.0638 | 3.4310e-01 | ❌ No | [-0.1428, 0.0152] |
| gemma4:latest_kb_rag vs llama3.2:latest_baseline | -0.1461 | 0.0000e+00 | ✅ Yes | [-0.2250, -0.0671] |
| gemma4:latest_kb_rag vs llama3.2:latest_kb_rag | -0.0788 | 5.1600e-02 | ❌ No | [-0.1577, 0.0002] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_baseline | -0.1723 | 0.0000e+00 | ✅ Yes | [-0.2513, -0.0933] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.2151 | 0.0000e+00 | ✅ Yes | [-0.2941, -0.1362] |
| gemma4:latest_kb_rag vs nemotron-mini:4b_baseline | -0.5155 | 0.0000e+00 | ✅ Yes | [-0.5945, -0.4365] |
| gemma4:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.3732 | 0.0000e+00 | ✅ Yes | [-0.4521, -0.2942] |
| gemma4:latest_kb_rag vs qwen2.5:14b_baseline | -0.0825 | 2.8500e-02 | ✅ Yes | [-0.1614, -0.0035] |
| gemma4:latest_kb_rag vs qwen2.5:14b_kb_rag | -0.0755 | 8.3500e-02 | ❌ No | [-0.1545, 0.0034] |
| gemma4:latest_kb_rag vs qwen3:8b_baseline | -0.0883 | 1.0200e-02 | ✅ Yes | [-0.1673, -0.0093] |
| gemma4:latest_kb_rag vs qwen3:8b_kb_rag | -0.0888 | 9.2000e-03 | ✅ Yes | [-0.1678, -0.0098] |
| gemma:latest_baseline vs gemma:latest_kb_rag | 0.0003 | 1.0000e+00 | ❌ No | [-0.0786, 0.0793] |
| gemma:latest_baseline vs gpt-oss:20b_baseline | 0.1587 | 0.0000e+00 | ✅ Yes | [0.0797, 0.2376] |
| gemma:latest_baseline vs gpt-oss:20b_kb_rag | 0.1753 | 0.0000e+00 | ✅ Yes | [0.0963, 0.2543] |
| gemma:latest_baseline vs llama3.1:8b_baseline | 0.0962 | 2.1000e-03 | ✅ Yes | [0.0173, 0.1752] |
| gemma:latest_baseline vs llama3.1:8b_kb_rag | 0.1193 | 0.0000e+00 | ✅ Yes | [0.0404, 0.1983] |
| gemma:latest_baseline vs llama3.2:latest_baseline | 0.0371 | 9.9370e-01 | ❌ No | [-0.0419, 0.1161] |
| gemma:latest_baseline vs llama3.2:latest_kb_rag | 0.1044 | 4.0000e-04 | ✅ Yes | [0.0254, 0.1833] |
| gemma:latest_baseline vs mistral-nemo:latest_baseline | 0.0109 | 1.0000e+00 | ❌ No | [-0.0681, 0.0898] |
| gemma:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0320 | 9.9930e-01 | ❌ No | [-0.1110, 0.0470] |
| gemma:latest_baseline vs nemotron-mini:4b_baseline | -0.3323 | 0.0000e+00 | ✅ Yes | [-0.4113, -0.2534] |
| gemma:latest_baseline vs nemotron-mini:4b_kb_rag | -0.1900 | 0.0000e+00 | ✅ Yes | [-0.2690, -0.1110] |
| gemma:latest_baseline vs qwen2.5:14b_baseline | 0.1007 | 8.0000e-04 | ✅ Yes | [0.0217, 0.1797] |
| gemma:latest_baseline vs qwen2.5:14b_kb_rag | 0.1076 | 2.0000e-04 | ✅ Yes | [0.0286, 0.1866] |
| gemma:latest_baseline vs qwen3:8b_baseline | 0.0948 | 2.8000e-03 | ✅ Yes | [0.0159, 0.1738] |
| gemma:latest_baseline vs qwen3:8b_kb_rag | 0.0943 | 3.2000e-03 | ✅ Yes | [0.0154, 0.1733] |
| gemma:latest_kb_rag vs gpt-oss:20b_baseline | 0.1583 | 0.0000e+00 | ✅ Yes | [0.0794, 0.2373] |
| gemma:latest_kb_rag vs gpt-oss:20b_kb_rag | 0.1750 | 0.0000e+00 | ✅ Yes | [0.0960, 0.2540] |
| gemma:latest_kb_rag vs llama3.1:8b_baseline | 0.0959 | 2.3000e-03 | ✅ Yes | [0.0169, 0.1749] |
| gemma:latest_kb_rag vs llama3.1:8b_kb_rag | 0.1190 | 0.0000e+00 | ✅ Yes | [0.0400, 0.1980] |
| gemma:latest_kb_rag vs llama3.2:latest_baseline | 0.0368 | 9.9450e-01 | ❌ No | [-0.0422, 0.1157] |
| gemma:latest_kb_rag vs llama3.2:latest_kb_rag | 0.1040 | 4.0000e-04 | ✅ Yes | [0.0251, 0.1830] |
| gemma:latest_kb_rag vs mistral-nemo:latest_baseline | 0.0105 | 1.0000e+00 | ❌ No | [-0.0684, 0.0895] |
| gemma:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.0323 | 9.9920e-01 | ❌ No | [-0.1113, 0.0466] |
| gemma:latest_kb_rag vs nemotron-mini:4b_baseline | -0.3327 | 0.0000e+00 | ✅ Yes | [-0.4117, -0.2537] |
| gemma:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.1903 | 0.0000e+00 | ✅ Yes | [-0.2693, -0.1114] |
| gemma:latest_kb_rag vs qwen2.5:14b_baseline | 0.1004 | 9.0000e-04 | ✅ Yes | [0.0214, 0.1793] |
| gemma:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.1073 | 2.0000e-04 | ✅ Yes | [0.0283, 0.1862] |
| gemma:latest_kb_rag vs qwen3:8b_baseline | 0.0945 | 3.0000e-03 | ✅ Yes | [0.0155, 0.1735] |
| gemma:latest_kb_rag vs qwen3:8b_kb_rag | 0.0940 | 3.4000e-03 | ✅ Yes | [0.0150, 0.1730] |
| gpt-oss:20b_baseline vs gpt-oss:20b_kb_rag | 0.0167 | 1.0000e+00 | ❌ No | [-0.0623, 0.0956] |
| gpt-oss:20b_baseline vs llama3.1:8b_baseline | -0.0624 | 3.9030e-01 | ❌ No | [-0.1414, 0.0166] |
| gpt-oss:20b_baseline vs llama3.1:8b_kb_rag | -0.0393 | 9.8620e-01 | ❌ No | [-0.1183, 0.0396] |
| gpt-oss:20b_baseline vs llama3.2:latest_baseline | -0.1216 | 0.0000e+00 | ✅ Yes | [-0.2005, -0.0426] |
| gpt-oss:20b_baseline vs llama3.2:latest_kb_rag | -0.0543 | 6.9180e-01 | ❌ No | [-0.1333, 0.0247] |
| gpt-oss:20b_baseline vs mistral-nemo:latest_baseline | -0.1478 | 0.0000e+00 | ✅ Yes | [-0.2268, -0.0688] |
| gpt-oss:20b_baseline vs mistral-nemo:latest_kb_rag | -0.1907 | 0.0000e+00 | ✅ Yes | [-0.2696, -0.1117] |
| gpt-oss:20b_baseline vs nemotron-mini:4b_baseline | -0.4910 | 0.0000e+00 | ✅ Yes | [-0.5700, -0.4120] |
| gpt-oss:20b_baseline vs nemotron-mini:4b_kb_rag | -0.3487 | 0.0000e+00 | ✅ Yes | [-0.4276, -0.2697] |
| gpt-oss:20b_baseline vs qwen2.5:14b_baseline | -0.0580 | 5.5430e-01 | ❌ No | [-0.1369, 0.0210] |
| gpt-oss:20b_baseline vs qwen2.5:14b_kb_rag | -0.0511 | 7.9840e-01 | ❌ No | [-0.1300, 0.0279] |
| gpt-oss:20b_baseline vs qwen3:8b_baseline | -0.0638 | 3.4300e-01 | ❌ No | [-0.1428, 0.0152] |
| gpt-oss:20b_baseline vs qwen3:8b_kb_rag | -0.0643 | 3.2620e-01 | ❌ No | [-0.1433, 0.0146] |
| gpt-oss:20b_kb_rag vs llama3.1:8b_baseline | -0.0791 | 4.9200e-02 | ✅ Yes | [-0.1580, -0.0001] |
| gpt-oss:20b_kb_rag vs llama3.1:8b_kb_rag | -0.0560 | 6.2980e-01 | ❌ No | [-0.1350, 0.0230] |
| gpt-oss:20b_kb_rag vs llama3.2:latest_baseline | -0.1382 | 0.0000e+00 | ✅ Yes | [-0.2172, -0.0593] |
| gpt-oss:20b_kb_rag vs llama3.2:latest_kb_rag | -0.0709 | 1.5540e-01 | ❌ No | [-0.1499, 0.0080] |
| gpt-oss:20b_kb_rag vs mistral-nemo:latest_baseline | -0.1645 | 0.0000e+00 | ✅ Yes | [-0.2434, -0.0855] |
| gpt-oss:20b_kb_rag vs mistral-nemo:latest_kb_rag | -0.2073 | 0.0000e+00 | ✅ Yes | [-0.2863, -0.1283] |
| gpt-oss:20b_kb_rag vs nemotron-mini:4b_baseline | -0.5077 | 0.0000e+00 | ✅ Yes | [-0.5866, -0.4287] |
| gpt-oss:20b_kb_rag vs nemotron-mini:4b_kb_rag | -0.3653 | 0.0000e+00 | ✅ Yes | [-0.4443, -0.2864] |
| gpt-oss:20b_kb_rag vs qwen2.5:14b_baseline | -0.0746 | 9.5100e-02 | ❌ No | [-0.1536, 0.0043] |
| gpt-oss:20b_kb_rag vs qwen2.5:14b_kb_rag | -0.0677 | 2.2830e-01 | ❌ No | [-0.1467, 0.0113] |
| gpt-oss:20b_kb_rag vs qwen3:8b_baseline | -0.0805 | 3.9500e-02 | ✅ Yes | [-0.1594, -0.0015] |
| gpt-oss:20b_kb_rag vs qwen3:8b_kb_rag | -0.0810 | 3.6300e-02 | ✅ Yes | [-0.1600, -0.0020] |
| llama3.1:8b_baseline vs llama3.1:8b_kb_rag | 0.0231 | 1.0000e+00 | ❌ No | [-0.0559, 0.1021] |
| llama3.1:8b_baseline vs llama3.2:latest_baseline | -0.0592 | 5.0940e-01 | ❌ No | [-0.1381, 0.0198] |
| llama3.1:8b_baseline vs llama3.2:latest_kb_rag | 0.0081 | 1.0000e+00 | ❌ No | [-0.0708, 0.0871] |
| llama3.1:8b_baseline vs mistral-nemo:latest_baseline | -0.0854 | 1.7200e-02 | ✅ Yes | [-0.1644, -0.0064] |
| llama3.1:8b_baseline vs mistral-nemo:latest_kb_rag | -0.1282 | 0.0000e+00 | ✅ Yes | [-0.2072, -0.0493] |
| llama3.1:8b_baseline vs nemotron-mini:4b_baseline | -0.4286 | 0.0000e+00 | ✅ Yes | [-0.5076, -0.3496] |
| llama3.1:8b_baseline vs nemotron-mini:4b_kb_rag | -0.2863 | 0.0000e+00 | ✅ Yes | [-0.3652, -0.2073] |
| llama3.1:8b_baseline vs qwen2.5:14b_baseline | 0.0044 | 1.0000e+00 | ❌ No | [-0.0745, 0.0834] |
| llama3.1:8b_baseline vs qwen2.5:14b_kb_rag | 0.0114 | 1.0000e+00 | ❌ No | [-0.0676, 0.0903] |
| llama3.1:8b_baseline vs qwen3:8b_baseline | -0.0014 | 1.0000e+00 | ❌ No | [-0.0804, 0.0776] |
| llama3.1:8b_baseline vs qwen3:8b_kb_rag | -0.0019 | 1.0000e+00 | ❌ No | [-0.0809, 0.0771] |
| llama3.1:8b_kb_rag vs llama3.2:latest_baseline | -0.0822 | 2.9500e-02 | ✅ Yes | [-0.1612, -0.0033] |
| llama3.1:8b_kb_rag vs llama3.2:latest_kb_rag | -0.0150 | 1.0000e+00 | ❌ No | [-0.0939, 0.0640] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_baseline | -0.1085 | 1.0000e-04 | ✅ Yes | [-0.1874, -0.0295] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_kb_rag | -0.1513 | 0.0000e+00 | ✅ Yes | [-0.2303, -0.0724] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_baseline | -0.4517 | 0.0000e+00 | ✅ Yes | [-0.5307, -0.3727] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_kb_rag | -0.3093 | 0.0000e+00 | ✅ Yes | [-0.3883, -0.2304] |
| llama3.1:8b_kb_rag vs qwen2.5:14b_baseline | -0.0186 | 1.0000e+00 | ❌ No | [-0.0976, 0.0603] |
| llama3.1:8b_kb_rag vs qwen2.5:14b_kb_rag | -0.0117 | 1.0000e+00 | ❌ No | [-0.0907, 0.0672] |
| llama3.1:8b_kb_rag vs qwen3:8b_baseline | -0.0245 | 1.0000e+00 | ❌ No | [-0.1035, 0.0545] |
| llama3.1:8b_kb_rag vs qwen3:8b_kb_rag | -0.0250 | 1.0000e+00 | ❌ No | [-0.1040, 0.0540] |
| llama3.2:latest_baseline vs llama3.2:latest_kb_rag | 0.0673 | 2.3950e-01 | ❌ No | [-0.0117, 0.1463] |
| llama3.2:latest_baseline vs mistral-nemo:latest_baseline | -0.0262 | 1.0000e+00 | ❌ No | [-0.1052, 0.0527] |
| llama3.2:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0691 | 1.9500e-01 | ❌ No | [-0.1481, 0.0099] |
| llama3.2:latest_baseline vs nemotron-mini:4b_baseline | -0.3694 | 0.0000e+00 | ✅ Yes | [-0.4484, -0.2905] |
| llama3.2:latest_baseline vs nemotron-mini:4b_kb_rag | -0.2271 | 0.0000e+00 | ✅ Yes | [-0.3061, -0.1481] |
| llama3.2:latest_baseline vs qwen2.5:14b_baseline | 0.0636 | 3.5000e-01 | ❌ No | [-0.0154, 0.1426] |
| llama3.2:latest_baseline vs qwen2.5:14b_kb_rag | 0.0705 | 1.6390e-01 | ❌ No | [-0.0085, 0.1495] |
| llama3.2:latest_baseline vs qwen3:8b_baseline | 0.0578 | 5.6240e-01 | ❌ No | [-0.0212, 0.1367] |
| llama3.2:latest_baseline vs qwen3:8b_kb_rag | 0.0572 | 5.8210e-01 | ❌ No | [-0.0217, 0.1362] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_baseline | -0.0935 | 3.7000e-03 | ✅ Yes | [-0.1725, -0.0145] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.1364 | 0.0000e+00 | ✅ Yes | [-0.2153, -0.0574] |
| llama3.2:latest_kb_rag vs nemotron-mini:4b_baseline | -0.4367 | 0.0000e+00 | ✅ Yes | [-0.5157, -0.3578] |
| llama3.2:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.2944 | 0.0000e+00 | ✅ Yes | [-0.3733, -0.2154] |
| llama3.2:latest_kb_rag vs qwen2.5:14b_baseline | -0.0037 | 1.0000e+00 | ❌ No | [-0.0827, 0.0753] |
| llama3.2:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0032 | 1.0000e+00 | ❌ No | [-0.0757, 0.0822] |
| llama3.2:latest_kb_rag vs qwen3:8b_baseline | -0.0095 | 1.0000e+00 | ❌ No | [-0.0885, 0.0694] |
| llama3.2:latest_kb_rag vs qwen3:8b_kb_rag | -0.0100 | 1.0000e+00 | ❌ No | [-0.0890, 0.0689] |
| mistral-nemo:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0429 | 9.6120e-01 | ❌ No | [-0.1218, 0.0361] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_baseline | -0.3432 | 0.0000e+00 | ✅ Yes | [-0.4222, -0.2642] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_kb_rag | -0.2009 | 0.0000e+00 | ✅ Yes | [-0.2798, -0.1219] |
| mistral-nemo:latest_baseline vs qwen2.5:14b_baseline | 0.0898 | 7.6000e-03 | ✅ Yes | [0.0109, 0.1688] |
| mistral-nemo:latest_baseline vs qwen2.5:14b_kb_rag | 0.0967 | 1.9000e-03 | ✅ Yes | [0.0178, 0.1757] |
| mistral-nemo:latest_baseline vs qwen3:8b_baseline | 0.0840 | 2.2000e-02 | ✅ Yes | [0.0050, 0.1630] |
| mistral-nemo:latest_baseline vs qwen3:8b_kb_rag | 0.0835 | 2.4000e-02 | ✅ Yes | [0.0045, 0.1624] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_baseline | -0.3003 | 0.0000e+00 | ✅ Yes | [-0.3793, -0.2214] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.1580 | 0.0000e+00 | ✅ Yes | [-0.2370, -0.0790] |
| mistral-nemo:latest_kb_rag vs qwen2.5:14b_baseline | 0.1327 | 0.0000e+00 | ✅ Yes | [0.0537, 0.2117] |
| mistral-nemo:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.1396 | 0.0000e+00 | ✅ Yes | [0.0606, 0.2186] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_baseline | 0.1268 | 0.0000e+00 | ✅ Yes | [0.0479, 0.2058] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_kb_rag | 0.1263 | 0.0000e+00 | ✅ Yes | [0.0474, 0.2053] |
| nemotron-mini:4b_baseline vs nemotron-mini:4b_kb_rag | 0.1423 | 0.0000e+00 | ✅ Yes | [0.0634, 0.2213] |
| nemotron-mini:4b_baseline vs qwen2.5:14b_baseline | 0.4330 | 0.0000e+00 | ✅ Yes | [0.3541, 0.5120] |
| nemotron-mini:4b_baseline vs qwen2.5:14b_kb_rag | 0.4399 | 0.0000e+00 | ✅ Yes | [0.3610, 0.5189] |
| nemotron-mini:4b_baseline vs qwen3:8b_baseline | 0.4272 | 0.0000e+00 | ✅ Yes | [0.3482, 0.5062] |
| nemotron-mini:4b_baseline vs qwen3:8b_kb_rag | 0.4267 | 0.0000e+00 | ✅ Yes | [0.3477, 0.5057] |
| nemotron-mini:4b_kb_rag vs qwen2.5:14b_baseline | 0.2907 | 0.0000e+00 | ✅ Yes | [0.2117, 0.3697] |
| nemotron-mini:4b_kb_rag vs qwen2.5:14b_kb_rag | 0.2976 | 0.0000e+00 | ✅ Yes | [0.2186, 0.3766] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_baseline | 0.2849 | 0.0000e+00 | ✅ Yes | [0.2059, 0.3638] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_kb_rag | 0.2843 | 0.0000e+00 | ✅ Yes | [0.2054, 0.3633] |
| qwen2.5:14b_baseline vs qwen2.5:14b_kb_rag | 0.0069 | 1.0000e+00 | ❌ No | [-0.0721, 0.0859] |
| qwen2.5:14b_baseline vs qwen3:8b_baseline | -0.0058 | 1.0000e+00 | ❌ No | [-0.0848, 0.0731] |
| qwen2.5:14b_baseline vs qwen3:8b_kb_rag | -0.0064 | 1.0000e+00 | ❌ No | [-0.0853, 0.0726] |
| qwen2.5:14b_kb_rag vs qwen3:8b_baseline | -0.0127 | 1.0000e+00 | ❌ No | [-0.0917, 0.0662] |
| qwen2.5:14b_kb_rag vs qwen3:8b_kb_rag | -0.0133 | 1.0000e+00 | ❌ No | [-0.0922, 0.0657] |
| qwen3:8b_baseline vs qwen3:8b_kb_rag | -0.0005 | 1.0000e+00 | ❌ No | [-0.0795, 0.0785] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 3471.2 characters.
- **Outlier Records Identified:** 7 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline | 0.2873 | 0.2865 | -0.0008 | 📉 Decreased |
| deepseek-r1:1.5b_kb_rag | 0.3080 | 0.3094 | +0.0014 | 📈 Improved |
| gemma4:12b-mlx_baseline | 0.7767 | 0.7791 | +0.0024 | 📈 Improved |
| gemma4:12b-mlx_kb_rag | 0.7996 | 0.8017 | +0.0020 | 📈 Improved |
| gemma4:31b-cloud_baseline | 0.8213 | 0.8241 | +0.0028 | 📈 Improved |
| gemma4:31b-cloud_kb_rag | 0.8294 | 0.8318 | +0.0024 | 📈 Improved |
| gemma4:31b-mlx_baseline | 0.8147 | 0.8172 | +0.0025 | 📈 Improved |
| gemma4:31b-mlx_kb_rag | 0.8244 | 0.8263 | +0.0019 | 📈 Improved |
| gemma4:latest_baseline | 0.7533 | 0.7548 | +0.0015 | 📈 Improved |
| gemma4:latest_kb_rag | 0.7786 | 0.7771 | -0.0015 | 📉 Decreased |
| gemma:latest_baseline | 0.5955 | 0.5891 | -0.0063 | 📉 Decreased |
| gemma:latest_kb_rag | 0.5958 | 0.5896 | -0.0062 | 📉 Decreased |
| gpt-oss:20b_baseline | 0.7541 | 0.7544 | +0.0003 | 📈 Improved |
| gpt-oss:20b_kb_rag | 0.7708 | 0.7708 | +0.0001 | ⚖️ Stable |
| llama3.1:8b_baseline | 0.6917 | 0.6922 | +0.0004 | 📈 Improved |
| llama3.1:8b_kb_rag | 0.7148 | 0.7146 | -0.0002 | 📉 Decreased |
| llama3.2:latest_baseline | 0.6325 | 0.6297 | -0.0028 | 📉 Decreased |
| llama3.2:latest_kb_rag | 0.6998 | 0.6993 | -0.0006 | 📉 Decreased |
| mistral-nemo:latest_baseline | 0.6063 | 0.6067 | +0.0004 | 📈 Improved |
| mistral-nemo:latest_kb_rag | 0.5635 | 0.5595 | -0.0040 | 📉 Decreased |
| nemotron-mini:4b_baseline | 0.2631 | 0.2577 | -0.0055 | 📉 Decreased |
| nemotron-mini:4b_kb_rag | 0.4055 | 0.4038 | -0.0016 | 📉 Decreased |
| qwen2.5:14b_baseline | 0.6961 | 0.6973 | +0.0012 | 📈 Improved |
| qwen2.5:14b_kb_rag | 0.7031 | 0.7027 | -0.0003 | 📉 Decreased |
| qwen3:8b_baseline | 0.6903 | 0.6927 | +0.0024 | 📈 Improved |
| qwen3:8b_kb_rag | 0.6898 | 0.6900 | +0.0002 | 📈 Improved |
