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
- **F-Statistic:** 119.7502
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
| nemotron-mini:4b_baseline | 113 | 0.2829 | 0.2425 | 0.3233 | 0.2167 |
| nemotron-mini:4b_kb_rag | 113 | 0.4055 | 0.3709 | 0.4400 | 0.1853 |
| qwen2.5:14b_baseline | 113 | 0.6961 | 0.6681 | 0.7242 | 0.1503 |
| qwen2.5:14b_kb_rag | 113 | 0.7031 | 0.6732 | 0.7329 | 0.1601 |
| qwen3:8b_baseline | 113 | 0.6903 | 0.6607 | 0.7199 | 0.1586 |
| qwen3:8b_kb_rag | 113 | 0.6898 | 0.6614 | 0.7182 | 0.1523 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline vs deepseek-r1:1.5b_kb_rag | 0.0207 | 1.0000e+00 | ❌ No | [-0.0580, 0.0994] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_baseline | 0.4894 | 0.0000e+00 | ✅ Yes | [0.4107, 0.5681] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_kb_rag | 0.5123 | 0.0000e+00 | ✅ Yes | [0.4336, 0.5910] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_baseline | 0.5340 | 0.0000e+00 | ✅ Yes | [0.4553, 0.6127] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_kb_rag | 0.5421 | 0.0000e+00 | ✅ Yes | [0.4634, 0.6208] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_baseline | 0.5274 | 0.0000e+00 | ✅ Yes | [0.4487, 0.6061] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_kb_rag | 0.5371 | 0.0000e+00 | ✅ Yes | [0.4584, 0.6158] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_baseline | 0.4660 | 0.0000e+00 | ✅ Yes | [0.3873, 0.5447] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_kb_rag | 0.4913 | 0.0000e+00 | ✅ Yes | [0.4126, 0.5700] |
| deepseek-r1:1.5b_baseline vs gemma:latest_baseline | 0.3081 | 0.0000e+00 | ✅ Yes | [0.2294, 0.3868] |
| deepseek-r1:1.5b_baseline vs gemma:latest_kb_rag | 0.3085 | 0.0000e+00 | ✅ Yes | [0.2298, 0.3872] |
| deepseek-r1:1.5b_baseline vs gpt-oss:20b_baseline | 0.4668 | 0.0000e+00 | ✅ Yes | [0.3881, 0.5455] |
| deepseek-r1:1.5b_baseline vs gpt-oss:20b_kb_rag | 0.4834 | 0.0000e+00 | ✅ Yes | [0.4047, 0.5621] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_baseline | 0.4044 | 0.0000e+00 | ✅ Yes | [0.3257, 0.4831] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_kb_rag | 0.4275 | 0.0000e+00 | ✅ Yes | [0.3488, 0.5062] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_baseline | 0.3452 | 0.0000e+00 | ✅ Yes | [0.2665, 0.4239] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_kb_rag | 0.4125 | 0.0000e+00 | ✅ Yes | [0.3338, 0.4912] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_baseline | 0.3190 | 0.0000e+00 | ✅ Yes | [0.2403, 0.3977] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_kb_rag | 0.2761 | 0.0000e+00 | ✅ Yes | [0.1974, 0.3548] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_baseline | -0.0045 | 1.0000e+00 | ❌ No | [-0.0832, 0.0742] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_kb_rag | 0.1181 | 0.0000e+00 | ✅ Yes | [0.0394, 0.1968] |
| deepseek-r1:1.5b_baseline vs qwen2.5:14b_baseline | 0.4088 | 0.0000e+00 | ✅ Yes | [0.3301, 0.4875] |
| deepseek-r1:1.5b_baseline vs qwen2.5:14b_kb_rag | 0.4157 | 0.0000e+00 | ✅ Yes | [0.3370, 0.4944] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_baseline | 0.4030 | 0.0000e+00 | ✅ Yes | [0.3243, 0.4817] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_kb_rag | 0.4025 | 0.0000e+00 | ✅ Yes | [0.3238, 0.4812] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_baseline | 0.4687 | 0.0000e+00 | ✅ Yes | [0.3900, 0.5474] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_kb_rag | 0.4916 | 0.0000e+00 | ✅ Yes | [0.4129, 0.5703] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-cloud_baseline | 0.5133 | 0.0000e+00 | ✅ Yes | [0.4346, 0.5920] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-cloud_kb_rag | 0.5214 | 0.0000e+00 | ✅ Yes | [0.4427, 0.6001] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-mlx_baseline | 0.5067 | 0.0000e+00 | ✅ Yes | [0.4280, 0.5854] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-mlx_kb_rag | 0.5164 | 0.0000e+00 | ✅ Yes | [0.4377, 0.5951] |
| deepseek-r1:1.5b_kb_rag vs gemma4:latest_baseline | 0.4453 | 0.0000e+00 | ✅ Yes | [0.3666, 0.5240] |
| deepseek-r1:1.5b_kb_rag vs gemma4:latest_kb_rag | 0.4706 | 0.0000e+00 | ✅ Yes | [0.3919, 0.5493] |
| deepseek-r1:1.5b_kb_rag vs gemma:latest_baseline | 0.2874 | 0.0000e+00 | ✅ Yes | [0.2087, 0.3661] |
| deepseek-r1:1.5b_kb_rag vs gemma:latest_kb_rag | 0.2878 | 0.0000e+00 | ✅ Yes | [0.2091, 0.3665] |
| deepseek-r1:1.5b_kb_rag vs gpt-oss:20b_baseline | 0.4461 | 0.0000e+00 | ✅ Yes | [0.3674, 0.5248] |
| deepseek-r1:1.5b_kb_rag vs gpt-oss:20b_kb_rag | 0.4627 | 0.0000e+00 | ✅ Yes | [0.3840, 0.5414] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_baseline | 0.3837 | 0.0000e+00 | ✅ Yes | [0.3050, 0.4624] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_kb_rag | 0.4068 | 0.0000e+00 | ✅ Yes | [0.3281, 0.4855] |
| deepseek-r1:1.5b_kb_rag vs llama3.2:latest_baseline | 0.3245 | 0.0000e+00 | ✅ Yes | [0.2458, 0.4032] |
| deepseek-r1:1.5b_kb_rag vs llama3.2:latest_kb_rag | 0.3918 | 0.0000e+00 | ✅ Yes | [0.3131, 0.4705] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_baseline | 0.2983 | 0.0000e+00 | ✅ Yes | [0.2196, 0.3770] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_kb_rag | 0.2554 | 0.0000e+00 | ✅ Yes | [0.1767, 0.3341] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_baseline | -0.0252 | 1.0000e+00 | ❌ No | [-0.1038, 0.0535] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_kb_rag | 0.0974 | 1.5000e-03 | ✅ Yes | [0.0187, 0.1761] |
| deepseek-r1:1.5b_kb_rag vs qwen2.5:14b_baseline | 0.3881 | 0.0000e+00 | ✅ Yes | [0.3094, 0.4668] |
| deepseek-r1:1.5b_kb_rag vs qwen2.5:14b_kb_rag | 0.3950 | 0.0000e+00 | ✅ Yes | [0.3163, 0.4737] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_baseline | 0.3823 | 0.0000e+00 | ✅ Yes | [0.3036, 0.4610] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_kb_rag | 0.3818 | 0.0000e+00 | ✅ Yes | [0.3031, 0.4605] |
| gemma4:12b-mlx_baseline vs gemma4:12b-mlx_kb_rag | 0.0229 | 1.0000e+00 | ❌ No | [-0.0558, 0.1016] |
| gemma4:12b-mlx_baseline vs gemma4:31b-cloud_baseline | 0.0446 | 9.3800e-01 | ❌ No | [-0.0341, 0.1233] |
| gemma4:12b-mlx_baseline vs gemma4:31b-cloud_kb_rag | 0.0527 | 7.3980e-01 | ❌ No | [-0.0260, 0.1314] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_baseline | 0.0380 | 9.9090e-01 | ❌ No | [-0.0407, 0.1167] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_kb_rag | 0.0477 | 8.8130e-01 | ❌ No | [-0.0310, 0.1264] |
| gemma4:12b-mlx_baseline vs gemma4:latest_baseline | -0.0234 | 1.0000e+00 | ❌ No | [-0.1021, 0.0553] |
| gemma4:12b-mlx_baseline vs gemma4:latest_kb_rag | 0.0019 | 1.0000e+00 | ❌ No | [-0.0768, 0.0806] |
| gemma4:12b-mlx_baseline vs gemma:latest_baseline | -0.1813 | 0.0000e+00 | ✅ Yes | [-0.2599, -0.1026] |
| gemma4:12b-mlx_baseline vs gemma:latest_kb_rag | -0.1809 | 0.0000e+00 | ✅ Yes | [-0.2596, -0.1022] |
| gemma4:12b-mlx_baseline vs gpt-oss:20b_baseline | -0.0226 | 1.0000e+00 | ❌ No | [-0.1013, 0.0561] |
| gemma4:12b-mlx_baseline vs gpt-oss:20b_kb_rag | -0.0059 | 1.0000e+00 | ❌ No | [-0.0846, 0.0728] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_baseline | -0.0850 | 1.7500e-02 | ✅ Yes | [-0.1637, -0.0063] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_kb_rag | -0.0619 | 4.0020e-01 | ❌ No | [-0.1406, 0.0168] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_baseline | -0.1442 | 0.0000e+00 | ✅ Yes | [-0.2229, -0.0655] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_kb_rag | -0.0769 | 6.6000e-02 | ❌ No | [-0.1556, 0.0018] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_baseline | -0.1704 | 0.0000e+00 | ✅ Yes | [-0.2491, -0.0917] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.2133 | 0.0000e+00 | ✅ Yes | [-0.2919, -0.1346] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_baseline | -0.4938 | 0.0000e+00 | ✅ Yes | [-0.5725, -0.4151] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_kb_rag | -0.3713 | 0.0000e+00 | ✅ Yes | [-0.4500, -0.2926] |
| gemma4:12b-mlx_baseline vs qwen2.5:14b_baseline | -0.0806 | 3.7100e-02 | ✅ Yes | [-0.1593, -0.0019] |
| gemma4:12b-mlx_baseline vs qwen2.5:14b_kb_rag | -0.0737 | 1.0510e-01 | ❌ No | [-0.1524, 0.0050] |
| gemma4:12b-mlx_baseline vs qwen3:8b_baseline | -0.0864 | 1.3600e-02 | ✅ Yes | [-0.1651, -0.0077] |
| gemma4:12b-mlx_baseline vs qwen3:8b_kb_rag | -0.0869 | 1.2400e-02 | ✅ Yes | [-0.1656, -0.0082] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-cloud_baseline | 0.0217 | 1.0000e+00 | ❌ No | [-0.0570, 0.1004] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-cloud_kb_rag | 0.0298 | 9.9980e-01 | ❌ No | [-0.0489, 0.1085] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_baseline | 0.0151 | 1.0000e+00 | ❌ No | [-0.0636, 0.0938] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_kb_rag | 0.0248 | 1.0000e+00 | ❌ No | [-0.0539, 0.1035] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_baseline | -0.0463 | 9.0990e-01 | ❌ No | [-0.1250, 0.0324] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0210 | 1.0000e+00 | ❌ No | [-0.0997, 0.0577] |
| gemma4:12b-mlx_kb_rag vs gemma:latest_baseline | -0.2042 | 0.0000e+00 | ✅ Yes | [-0.2829, -0.1255] |
| gemma4:12b-mlx_kb_rag vs gemma:latest_kb_rag | -0.2038 | 0.0000e+00 | ✅ Yes | [-0.2825, -0.1251] |
| gemma4:12b-mlx_kb_rag vs gpt-oss:20b_baseline | -0.0455 | 9.2420e-01 | ❌ No | [-0.1242, 0.0332] |
| gemma4:12b-mlx_kb_rag vs gpt-oss:20b_kb_rag | -0.0289 | 9.9990e-01 | ❌ No | [-0.1076, 0.0498] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_baseline | -0.1079 | 1.0000e-04 | ✅ Yes | [-0.1866, -0.0292] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_kb_rag | -0.0848 | 1.8000e-02 | ✅ Yes | [-0.1635, -0.0061] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_baseline | -0.1671 | 0.0000e+00 | ✅ Yes | [-0.2458, -0.0884] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.0998 | 9.0000e-04 | ✅ Yes | [-0.1785, -0.0211] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.1933 | 0.0000e+00 | ✅ Yes | [-0.2720, -0.1146] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.2362 | 0.0000e+00 | ✅ Yes | [-0.3149, -0.1575] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_baseline | -0.5168 | 0.0000e+00 | ✅ Yes | [-0.5954, -0.4381] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | -0.3942 | 0.0000e+00 | ✅ Yes | [-0.4729, -0.3155] |
| gemma4:12b-mlx_kb_rag vs qwen2.5:14b_baseline | -0.1035 | 4.0000e-04 | ✅ Yes | [-0.1822, -0.0248] |
| gemma4:12b-mlx_kb_rag vs qwen2.5:14b_kb_rag | -0.0966 | 1.9000e-03 | ✅ Yes | [-0.1753, -0.0179] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_baseline | -0.1093 | 1.0000e-04 | ✅ Yes | [-0.1880, -0.0306] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.1098 | 1.0000e-04 | ✅ Yes | [-0.1885, -0.0311] |
| gemma4:31b-cloud_baseline vs gemma4:31b-cloud_kb_rag | 0.0081 | 1.0000e+00 | ❌ No | [-0.0706, 0.0868] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_baseline | -0.0066 | 1.0000e+00 | ❌ No | [-0.0853, 0.0721] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_kb_rag | 0.0031 | 1.0000e+00 | ❌ No | [-0.0756, 0.0818] |
| gemma4:31b-cloud_baseline vs gemma4:latest_baseline | -0.0680 | 2.1490e-01 | ❌ No | [-0.1467, 0.0107] |
| gemma4:31b-cloud_baseline vs gemma4:latest_kb_rag | -0.0427 | 9.6110e-01 | ❌ No | [-0.1214, 0.0360] |
| gemma4:31b-cloud_baseline vs gemma:latest_baseline | -0.2259 | 0.0000e+00 | ✅ Yes | [-0.3046, -0.1472] |
| gemma4:31b-cloud_baseline vs gemma:latest_kb_rag | -0.2255 | 0.0000e+00 | ✅ Yes | [-0.3042, -0.1468] |
| gemma4:31b-cloud_baseline vs gpt-oss:20b_baseline | -0.0672 | 2.3570e-01 | ❌ No | [-0.1459, 0.0115] |
| gemma4:31b-cloud_baseline vs gpt-oss:20b_kb_rag | -0.0505 | 8.0840e-01 | ❌ No | [-0.1292, 0.0281] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_baseline | -0.1296 | 0.0000e+00 | ✅ Yes | [-0.2083, -0.0509] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_kb_rag | -0.1065 | 2.0000e-04 | ✅ Yes | [-0.1852, -0.0278] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_baseline | -0.1888 | 0.0000e+00 | ✅ Yes | [-0.2675, -0.1101] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_kb_rag | -0.1215 | 0.0000e+00 | ✅ Yes | [-0.2002, -0.0428] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_baseline | -0.2150 | 0.0000e+00 | ✅ Yes | [-0.2937, -0.1363] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_kb_rag | -0.2579 | 0.0000e+00 | ✅ Yes | [-0.3366, -0.1792] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_baseline | -0.5384 | 0.0000e+00 | ✅ Yes | [-0.6171, -0.4597] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_kb_rag | -0.4159 | 0.0000e+00 | ✅ Yes | [-0.4946, -0.3372] |
| gemma4:31b-cloud_baseline vs qwen2.5:14b_baseline | -0.1252 | 0.0000e+00 | ✅ Yes | [-0.2039, -0.0465] |
| gemma4:31b-cloud_baseline vs qwen2.5:14b_kb_rag | -0.1183 | 0.0000e+00 | ✅ Yes | [-0.1970, -0.0396] |
| gemma4:31b-cloud_baseline vs qwen3:8b_baseline | -0.1310 | 0.0000e+00 | ✅ Yes | [-0.2097, -0.0523] |
| gemma4:31b-cloud_baseline vs qwen3:8b_kb_rag | -0.1315 | 0.0000e+00 | ✅ Yes | [-0.2102, -0.0528] |
| gemma4:31b-cloud_kb_rag vs gemma4:31b-mlx_baseline | -0.0147 | 1.0000e+00 | ❌ No | [-0.0934, 0.0640] |
| gemma4:31b-cloud_kb_rag vs gemma4:31b-mlx_kb_rag | -0.0050 | 1.0000e+00 | ❌ No | [-0.0837, 0.0737] |
| gemma4:31b-cloud_kb_rag vs gemma4:latest_baseline | -0.0761 | 7.3900e-02 | ❌ No | [-0.1548, 0.0026] |
| gemma4:31b-cloud_kb_rag vs gemma4:latest_kb_rag | -0.0508 | 8.0010e-01 | ❌ No | [-0.1295, 0.0279] |
| gemma4:31b-cloud_kb_rag vs gemma:latest_baseline | -0.2340 | 0.0000e+00 | ✅ Yes | [-0.3127, -0.1553] |
| gemma4:31b-cloud_kb_rag vs gemma:latest_kb_rag | -0.2336 | 0.0000e+00 | ✅ Yes | [-0.3123, -0.1549] |
| gemma4:31b-cloud_kb_rag vs gpt-oss:20b_baseline | -0.0753 | 8.3200e-02 | ❌ No | [-0.1540, 0.0034] |
| gemma4:31b-cloud_kb_rag vs gpt-oss:20b_kb_rag | -0.0587 | 5.2070e-01 | ❌ No | [-0.1374, 0.0200] |
| gemma4:31b-cloud_kb_rag vs llama3.1:8b_baseline | -0.1377 | 0.0000e+00 | ✅ Yes | [-0.2164, -0.0590] |
| gemma4:31b-cloud_kb_rag vs llama3.1:8b_kb_rag | -0.1146 | 0.0000e+00 | ✅ Yes | [-0.1933, -0.0359] |
| gemma4:31b-cloud_kb_rag vs llama3.2:latest_baseline | -0.1969 | 0.0000e+00 | ✅ Yes | [-0.2756, -0.1182] |
| gemma4:31b-cloud_kb_rag vs llama3.2:latest_kb_rag | -0.1296 | 0.0000e+00 | ✅ Yes | [-0.2083, -0.0509] |
| gemma4:31b-cloud_kb_rag vs mistral-nemo:latest_baseline | -0.2231 | 0.0000e+00 | ✅ Yes | [-0.3018, -0.1444] |
| gemma4:31b-cloud_kb_rag vs mistral-nemo:latest_kb_rag | -0.2660 | 0.0000e+00 | ✅ Yes | [-0.3447, -0.1873] |
| gemma4:31b-cloud_kb_rag vs nemotron-mini:4b_baseline | -0.5466 | 0.0000e+00 | ✅ Yes | [-0.6253, -0.4679] |
| gemma4:31b-cloud_kb_rag vs nemotron-mini:4b_kb_rag | -0.4240 | 0.0000e+00 | ✅ Yes | [-0.5027, -0.3453] |
| gemma4:31b-cloud_kb_rag vs qwen2.5:14b_baseline | -0.1333 | 0.0000e+00 | ✅ Yes | [-0.2120, -0.0546] |
| gemma4:31b-cloud_kb_rag vs qwen2.5:14b_kb_rag | -0.1264 | 0.0000e+00 | ✅ Yes | [-0.2051, -0.0477] |
| gemma4:31b-cloud_kb_rag vs qwen3:8b_baseline | -0.1391 | 0.0000e+00 | ✅ Yes | [-0.2178, -0.0604] |
| gemma4:31b-cloud_kb_rag vs qwen3:8b_kb_rag | -0.1396 | 0.0000e+00 | ✅ Yes | [-0.2183, -0.0609] |
| gemma4:31b-mlx_baseline vs gemma4:31b-mlx_kb_rag | 0.0097 | 1.0000e+00 | ❌ No | [-0.0690, 0.0884] |
| gemma4:31b-mlx_baseline vs gemma4:latest_baseline | -0.0614 | 4.1870e-01 | ❌ No | [-0.1401, 0.0173] |
| gemma4:31b-mlx_baseline vs gemma4:latest_kb_rag | -0.0361 | 9.9550e-01 | ❌ No | [-0.1148, 0.0426] |
| gemma4:31b-mlx_baseline vs gemma:latest_baseline | -0.2192 | 0.0000e+00 | ✅ Yes | [-0.2979, -0.1406] |
| gemma4:31b-mlx_baseline vs gemma:latest_kb_rag | -0.2189 | 0.0000e+00 | ✅ Yes | [-0.2976, -0.1402] |
| gemma4:31b-mlx_baseline vs gpt-oss:20b_baseline | -0.0606 | 4.4840e-01 | ❌ No | [-0.1393, 0.0181] |
| gemma4:31b-mlx_baseline vs gpt-oss:20b_kb_rag | -0.0439 | 9.4720e-01 | ❌ No | [-0.1226, 0.0348] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_baseline | -0.1230 | 0.0000e+00 | ✅ Yes | [-0.2017, -0.0443] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_kb_rag | -0.0999 | 9.0000e-04 | ✅ Yes | [-0.1786, -0.0212] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_baseline | -0.1822 | 0.0000e+00 | ✅ Yes | [-0.2609, -0.1035] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_kb_rag | -0.1149 | 0.0000e+00 | ✅ Yes | [-0.1936, -0.0362] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_baseline | -0.2084 | 0.0000e+00 | ✅ Yes | [-0.2871, -0.1297] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.2512 | 0.0000e+00 | ✅ Yes | [-0.3299, -0.1726] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_baseline | -0.5318 | 0.0000e+00 | ✅ Yes | [-0.6105, -0.4531] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_kb_rag | -0.4093 | 0.0000e+00 | ✅ Yes | [-0.4880, -0.3306] |
| gemma4:31b-mlx_baseline vs qwen2.5:14b_baseline | -0.1186 | 0.0000e+00 | ✅ Yes | [-0.1973, -0.0399] |
| gemma4:31b-mlx_baseline vs qwen2.5:14b_kb_rag | -0.1116 | 1.0000e-04 | ✅ Yes | [-0.1903, -0.0330] |
| gemma4:31b-mlx_baseline vs qwen3:8b_baseline | -0.1244 | 0.0000e+00 | ✅ Yes | [-0.2031, -0.0457] |
| gemma4:31b-mlx_baseline vs qwen3:8b_kb_rag | -0.1249 | 0.0000e+00 | ✅ Yes | [-0.2036, -0.0462] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_baseline | -0.0711 | 1.4710e-01 | ❌ No | [-0.1498, 0.0076] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0458 | 9.1870e-01 | ❌ No | [-0.1245, 0.0329] |
| gemma4:31b-mlx_kb_rag vs gemma:latest_baseline | -0.2290 | 0.0000e+00 | ✅ Yes | [-0.3077, -0.1503] |
| gemma4:31b-mlx_kb_rag vs gemma:latest_kb_rag | -0.2286 | 0.0000e+00 | ✅ Yes | [-0.3073, -0.1499] |
| gemma4:31b-mlx_kb_rag vs gpt-oss:20b_baseline | -0.0703 | 1.6310e-01 | ❌ No | [-0.1490, 0.0084] |
| gemma4:31b-mlx_kb_rag vs gpt-oss:20b_kb_rag | -0.0537 | 7.0760e-01 | ❌ No | [-0.1324, 0.0250] |
| gemma4:31b-mlx_kb_rag vs llama3.1:8b_baseline | -0.1327 | 0.0000e+00 | ✅ Yes | [-0.2114, -0.0540] |
| gemma4:31b-mlx_kb_rag vs llama3.1:8b_kb_rag | -0.1096 | 1.0000e-04 | ✅ Yes | [-0.1883, -0.0309] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_baseline | -0.1919 | 0.0000e+00 | ✅ Yes | [-0.2706, -0.1132] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.1246 | 0.0000e+00 | ✅ Yes | [-0.2033, -0.0459] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.2181 | 0.0000e+00 | ✅ Yes | [-0.2968, -0.1394] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.2610 | 0.0000e+00 | ✅ Yes | [-0.3397, -0.1823] |
| gemma4:31b-mlx_kb_rag vs nemotron-mini:4b_baseline | -0.5416 | 0.0000e+00 | ✅ Yes | [-0.6203, -0.4629] |
| gemma4:31b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | -0.4190 | 0.0000e+00 | ✅ Yes | [-0.4977, -0.3403] |
| gemma4:31b-mlx_kb_rag vs qwen2.5:14b_baseline | -0.1283 | 0.0000e+00 | ✅ Yes | [-0.2070, -0.0496] |
| gemma4:31b-mlx_kb_rag vs qwen2.5:14b_kb_rag | -0.1214 | 0.0000e+00 | ✅ Yes | [-0.2001, -0.0427] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_baseline | -0.1341 | 0.0000e+00 | ✅ Yes | [-0.2128, -0.0554] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.1346 | 0.0000e+00 | ✅ Yes | [-0.2133, -0.0559] |
| gemma4:latest_baseline vs gemma4:latest_kb_rag | 0.0253 | 1.0000e+00 | ❌ No | [-0.0534, 0.1040] |
| gemma4:latest_baseline vs gemma:latest_baseline | -0.1578 | 0.0000e+00 | ✅ Yes | [-0.2365, -0.0792] |
| gemma4:latest_baseline vs gemma:latest_kb_rag | -0.1575 | 0.0000e+00 | ✅ Yes | [-0.2362, -0.0788] |
| gemma4:latest_baseline vs gpt-oss:20b_baseline | 0.0008 | 1.0000e+00 | ❌ No | [-0.0779, 0.0795] |
| gemma4:latest_baseline vs gpt-oss:20b_kb_rag | 0.0175 | 1.0000e+00 | ❌ No | [-0.0612, 0.0962] |
| gemma4:latest_baseline vs llama3.1:8b_baseline | -0.0616 | 4.1140e-01 | ❌ No | [-0.1403, 0.0171] |
| gemma4:latest_baseline vs llama3.1:8b_kb_rag | -0.0385 | 9.8900e-01 | ❌ No | [-0.1172, 0.0402] |
| gemma4:latest_baseline vs llama3.2:latest_baseline | -0.1208 | 0.0000e+00 | ✅ Yes | [-0.1995, -0.0421] |
| gemma4:latest_baseline vs llama3.2:latest_kb_rag | -0.0535 | 7.1400e-01 | ❌ No | [-0.1322, 0.0252] |
| gemma4:latest_baseline vs mistral-nemo:latest_baseline | -0.1470 | 0.0000e+00 | ✅ Yes | [-0.2257, -0.0683] |
| gemma4:latest_baseline vs mistral-nemo:latest_kb_rag | -0.1898 | 0.0000e+00 | ✅ Yes | [-0.2685, -0.1112] |
| gemma4:latest_baseline vs nemotron-mini:4b_baseline | -0.4704 | 0.0000e+00 | ✅ Yes | [-0.5491, -0.3917] |
| gemma4:latest_baseline vs nemotron-mini:4b_kb_rag | -0.3479 | 0.0000e+00 | ✅ Yes | [-0.4266, -0.2692] |
| gemma4:latest_baseline vs qwen2.5:14b_baseline | -0.0572 | 5.7780e-01 | ❌ No | [-0.1359, 0.0215] |
| gemma4:latest_baseline vs qwen2.5:14b_kb_rag | -0.0502 | 8.1700e-01 | ❌ No | [-0.1289, 0.0284] |
| gemma4:latest_baseline vs qwen3:8b_baseline | -0.0630 | 3.6280e-01 | ❌ No | [-0.1417, 0.0157] |
| gemma4:latest_baseline vs qwen3:8b_kb_rag | -0.0635 | 3.4550e-01 | ❌ No | [-0.1422, 0.0152] |
| gemma4:latest_kb_rag vs gemma:latest_baseline | -0.1831 | 0.0000e+00 | ✅ Yes | [-0.2618, -0.1044] |
| gemma4:latest_kb_rag vs gemma:latest_kb_rag | -0.1828 | 0.0000e+00 | ✅ Yes | [-0.2615, -0.1041] |
| gemma4:latest_kb_rag vs gpt-oss:20b_baseline | -0.0245 | 1.0000e+00 | ❌ No | [-0.1032, 0.0542] |
| gemma4:latest_kb_rag vs gpt-oss:20b_kb_rag | -0.0078 | 1.0000e+00 | ❌ No | [-0.0865, 0.0709] |
| gemma4:latest_kb_rag vs llama3.1:8b_baseline | -0.0869 | 1.2400e-02 | ✅ Yes | [-0.1656, -0.0082] |
| gemma4:latest_kb_rag vs llama3.1:8b_kb_rag | -0.0638 | 3.3580e-01 | ❌ No | [-0.1425, 0.0149] |
| gemma4:latest_kb_rag vs llama3.2:latest_baseline | -0.1461 | 0.0000e+00 | ✅ Yes | [-0.2248, -0.0674] |
| gemma4:latest_kb_rag vs llama3.2:latest_kb_rag | -0.0788 | 4.9400e-02 | ✅ Yes | [-0.1575, -0.0001] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_baseline | -0.1723 | 0.0000e+00 | ✅ Yes | [-0.2510, -0.0936] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.2151 | 0.0000e+00 | ✅ Yes | [-0.2938, -0.1364] |
| gemma4:latest_kb_rag vs nemotron-mini:4b_baseline | -0.4957 | 0.0000e+00 | ✅ Yes | [-0.5744, -0.4170] |
| gemma4:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.3732 | 0.0000e+00 | ✅ Yes | [-0.4518, -0.2945] |
| gemma4:latest_kb_rag vs qwen2.5:14b_baseline | -0.0825 | 2.7100e-02 | ✅ Yes | [-0.1612, -0.0038] |
| gemma4:latest_kb_rag vs qwen2.5:14b_kb_rag | -0.0755 | 8.0400e-02 | ❌ No | [-0.1542, 0.0032] |
| gemma4:latest_kb_rag vs qwen3:8b_baseline | -0.0883 | 9.6000e-03 | ✅ Yes | [-0.1670, -0.0096] |
| gemma4:latest_kb_rag vs qwen3:8b_kb_rag | -0.0888 | 8.7000e-03 | ✅ Yes | [-0.1675, -0.0101] |
| gemma:latest_baseline vs gemma:latest_kb_rag | 0.0003 | 1.0000e+00 | ❌ No | [-0.0784, 0.0790] |
| gemma:latest_baseline vs gpt-oss:20b_baseline | 0.1587 | 0.0000e+00 | ✅ Yes | [0.0800, 0.2374] |
| gemma:latest_baseline vs gpt-oss:20b_kb_rag | 0.1753 | 0.0000e+00 | ✅ Yes | [0.0966, 0.2540] |
| gemma:latest_baseline vs llama3.1:8b_baseline | 0.0962 | 2.0000e-03 | ✅ Yes | [0.0175, 0.1749] |
| gemma:latest_baseline vs llama3.1:8b_kb_rag | 0.1193 | 0.0000e+00 | ✅ Yes | [0.0406, 0.1980] |
| gemma:latest_baseline vs llama3.2:latest_baseline | 0.0371 | 9.9340e-01 | ❌ No | [-0.0416, 0.1158] |
| gemma:latest_baseline vs llama3.2:latest_kb_rag | 0.1044 | 3.0000e-04 | ✅ Yes | [0.0257, 0.1831] |
| gemma:latest_baseline vs mistral-nemo:latest_baseline | 0.0109 | 1.0000e+00 | ❌ No | [-0.0678, 0.0896] |
| gemma:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0320 | 9.9930e-01 | ❌ No | [-0.1107, 0.0467] |
| gemma:latest_baseline vs nemotron-mini:4b_baseline | -0.3126 | 0.0000e+00 | ✅ Yes | [-0.3913, -0.2339] |
| gemma:latest_baseline vs nemotron-mini:4b_kb_rag | -0.1900 | 0.0000e+00 | ✅ Yes | [-0.2687, -0.1113] |
| gemma:latest_baseline vs qwen2.5:14b_baseline | 0.1007 | 8.0000e-04 | ✅ Yes | [0.0220, 0.1794] |
| gemma:latest_baseline vs qwen2.5:14b_kb_rag | 0.1076 | 2.0000e-04 | ✅ Yes | [0.0289, 0.1863] |
| gemma:latest_baseline vs qwen3:8b_baseline | 0.0948 | 2.7000e-03 | ✅ Yes | [0.0162, 0.1735] |
| gemma:latest_baseline vs qwen3:8b_kb_rag | 0.0943 | 2.9000e-03 | ✅ Yes | [0.0156, 0.1730] |
| gemma:latest_kb_rag vs gpt-oss:20b_baseline | 0.1583 | 0.0000e+00 | ✅ Yes | [0.0796, 0.2370] |
| gemma:latest_kb_rag vs gpt-oss:20b_kb_rag | 0.1750 | 0.0000e+00 | ✅ Yes | [0.0963, 0.2537] |
| gemma:latest_kb_rag vs llama3.1:8b_baseline | 0.0959 | 2.1000e-03 | ✅ Yes | [0.0172, 0.1746] |
| gemma:latest_kb_rag vs llama3.1:8b_kb_rag | 0.1190 | 0.0000e+00 | ✅ Yes | [0.0403, 0.1977] |
| gemma:latest_kb_rag vs llama3.2:latest_baseline | 0.0368 | 9.9420e-01 | ❌ No | [-0.0419, 0.1155] |
| gemma:latest_kb_rag vs llama3.2:latest_kb_rag | 0.1040 | 4.0000e-04 | ✅ Yes | [0.0253, 0.1827] |
| gemma:latest_kb_rag vs mistral-nemo:latest_baseline | 0.0105 | 1.0000e+00 | ❌ No | [-0.0682, 0.0892] |
| gemma:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.0323 | 9.9920e-01 | ❌ No | [-0.1110, 0.0464] |
| gemma:latest_kb_rag vs nemotron-mini:4b_baseline | -0.3129 | 0.0000e+00 | ✅ Yes | [-0.3916, -0.2342] |
| gemma:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.1903 | 0.0000e+00 | ✅ Yes | [-0.2690, -0.1116] |
| gemma:latest_kb_rag vs qwen2.5:14b_baseline | 0.1004 | 8.0000e-04 | ✅ Yes | [0.0217, 0.1791] |
| gemma:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.1073 | 2.0000e-04 | ✅ Yes | [0.0286, 0.1860] |
| gemma:latest_kb_rag vs qwen3:8b_baseline | 0.0945 | 2.8000e-03 | ✅ Yes | [0.0158, 0.1732] |
| gemma:latest_kb_rag vs qwen3:8b_kb_rag | 0.0940 | 3.2000e-03 | ✅ Yes | [0.0153, 0.1727] |
| gpt-oss:20b_baseline vs gpt-oss:20b_kb_rag | 0.0167 | 1.0000e+00 | ❌ No | [-0.0620, 0.0954] |
| gpt-oss:20b_baseline vs llama3.1:8b_baseline | -0.0624 | 3.8280e-01 | ❌ No | [-0.1411, 0.0163] |
| gpt-oss:20b_baseline vs llama3.1:8b_kb_rag | -0.0393 | 9.8560e-01 | ❌ No | [-0.1180, 0.0394] |
| gpt-oss:20b_baseline vs llama3.2:latest_baseline | -0.1216 | 0.0000e+00 | ✅ Yes | [-0.2003, -0.0429] |
| gpt-oss:20b_baseline vs llama3.2:latest_kb_rag | -0.0543 | 6.8510e-01 | ❌ No | [-0.1330, 0.0244] |
| gpt-oss:20b_baseline vs mistral-nemo:latest_baseline | -0.1478 | 0.0000e+00 | ✅ Yes | [-0.2265, -0.0691] |
| gpt-oss:20b_baseline vs mistral-nemo:latest_kb_rag | -0.1907 | 0.0000e+00 | ✅ Yes | [-0.2694, -0.1120] |
| gpt-oss:20b_baseline vs nemotron-mini:4b_baseline | -0.4712 | 0.0000e+00 | ✅ Yes | [-0.5499, -0.3925] |
| gpt-oss:20b_baseline vs nemotron-mini:4b_kb_rag | -0.3487 | 0.0000e+00 | ✅ Yes | [-0.4274, -0.2700] |
| gpt-oss:20b_baseline vs qwen2.5:14b_baseline | -0.0580 | 5.4670e-01 | ❌ No | [-0.1367, 0.0207] |
| gpt-oss:20b_baseline vs qwen2.5:14b_kb_rag | -0.0511 | 7.9300e-01 | ❌ No | [-0.1298, 0.0276] |
| gpt-oss:20b_baseline vs qwen3:8b_baseline | -0.0638 | 3.3580e-01 | ❌ No | [-0.1425, 0.0149] |
| gpt-oss:20b_baseline vs qwen3:8b_kb_rag | -0.0643 | 3.1910e-01 | ❌ No | [-0.1430, 0.0144] |
| gpt-oss:20b_kb_rag vs llama3.1:8b_baseline | -0.0791 | 4.7200e-02 | ✅ Yes | [-0.1578, -0.0004] |
| gpt-oss:20b_kb_rag vs llama3.1:8b_kb_rag | -0.0560 | 6.2250e-01 | ❌ No | [-0.1347, 0.0227] |
| gpt-oss:20b_kb_rag vs llama3.2:latest_baseline | -0.1382 | 0.0000e+00 | ✅ Yes | [-0.2169, -0.0595] |
| gpt-oss:20b_kb_rag vs llama3.2:latest_kb_rag | -0.0709 | 1.5060e-01 | ❌ No | [-0.1496, 0.0078] |
| gpt-oss:20b_kb_rag vs mistral-nemo:latest_baseline | -0.1645 | 0.0000e+00 | ✅ Yes | [-0.2431, -0.0858] |
| gpt-oss:20b_kb_rag vs mistral-nemo:latest_kb_rag | -0.2073 | 0.0000e+00 | ✅ Yes | [-0.2860, -0.1286] |
| gpt-oss:20b_kb_rag vs nemotron-mini:4b_baseline | -0.4879 | 0.0000e+00 | ✅ Yes | [-0.5666, -0.4092] |
| gpt-oss:20b_kb_rag vs nemotron-mini:4b_kb_rag | -0.3653 | 0.0000e+00 | ✅ Yes | [-0.4440, -0.2866] |
| gpt-oss:20b_kb_rag vs qwen2.5:14b_baseline | -0.0746 | 9.1700e-02 | ❌ No | [-0.1533, 0.0041] |
| gpt-oss:20b_kb_rag vs qwen2.5:14b_kb_rag | -0.0677 | 2.2230e-01 | ❌ No | [-0.1464, 0.0110] |
| gpt-oss:20b_kb_rag vs qwen3:8b_baseline | -0.0805 | 3.7700e-02 | ✅ Yes | [-0.1592, -0.0018] |
| gpt-oss:20b_kb_rag vs qwen3:8b_kb_rag | -0.0810 | 3.4700e-02 | ✅ Yes | [-0.1597, -0.0023] |
| llama3.1:8b_baseline vs llama3.1:8b_kb_rag | 0.0231 | 1.0000e+00 | ❌ No | [-0.0556, 0.1018] |
| llama3.1:8b_baseline vs llama3.2:latest_baseline | -0.0592 | 5.0160e-01 | ❌ No | [-0.1379, 0.0195] |
| llama3.1:8b_baseline vs llama3.2:latest_kb_rag | 0.0081 | 1.0000e+00 | ❌ No | [-0.0706, 0.0868] |
| llama3.1:8b_baseline vs mistral-nemo:latest_baseline | -0.0854 | 1.6300e-02 | ✅ Yes | [-0.1641, -0.0067] |
| llama3.1:8b_baseline vs mistral-nemo:latest_kb_rag | -0.1282 | 0.0000e+00 | ✅ Yes | [-0.2069, -0.0495] |
| llama3.1:8b_baseline vs nemotron-mini:4b_baseline | -0.4088 | 0.0000e+00 | ✅ Yes | [-0.4875, -0.3301] |
| llama3.1:8b_baseline vs nemotron-mini:4b_kb_rag | -0.2863 | 0.0000e+00 | ✅ Yes | [-0.3649, -0.2076] |
| llama3.1:8b_baseline vs qwen2.5:14b_baseline | 0.0044 | 1.0000e+00 | ❌ No | [-0.0743, 0.0831] |
| llama3.1:8b_baseline vs qwen2.5:14b_kb_rag | 0.0114 | 1.0000e+00 | ❌ No | [-0.0673, 0.0900] |
| llama3.1:8b_baseline vs qwen3:8b_baseline | -0.0014 | 1.0000e+00 | ❌ No | [-0.0801, 0.0773] |
| llama3.1:8b_baseline vs qwen3:8b_kb_rag | -0.0019 | 1.0000e+00 | ❌ No | [-0.0806, 0.0768] |
| llama3.1:8b_kb_rag vs llama3.2:latest_baseline | -0.0822 | 2.8100e-02 | ✅ Yes | [-0.1609, -0.0036] |
| llama3.1:8b_kb_rag vs llama3.2:latest_kb_rag | -0.0150 | 1.0000e+00 | ❌ No | [-0.0937, 0.0637] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_baseline | -0.1085 | 1.0000e-04 | ✅ Yes | [-0.1872, -0.0298] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_kb_rag | -0.1513 | 0.0000e+00 | ✅ Yes | [-0.2300, -0.0726] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_baseline | -0.4319 | 0.0000e+00 | ✅ Yes | [-0.5106, -0.3532] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_kb_rag | -0.3093 | 0.0000e+00 | ✅ Yes | [-0.3880, -0.2306] |
| llama3.1:8b_kb_rag vs qwen2.5:14b_baseline | -0.0186 | 1.0000e+00 | ❌ No | [-0.0973, 0.0600] |
| llama3.1:8b_kb_rag vs qwen2.5:14b_kb_rag | -0.0117 | 1.0000e+00 | ❌ No | [-0.0904, 0.0670] |
| llama3.1:8b_kb_rag vs qwen3:8b_baseline | -0.0245 | 1.0000e+00 | ❌ No | [-0.1032, 0.0542] |
| llama3.1:8b_kb_rag vs qwen3:8b_kb_rag | -0.0250 | 1.0000e+00 | ❌ No | [-0.1037, 0.0537] |
| llama3.2:latest_baseline vs llama3.2:latest_kb_rag | 0.0673 | 2.3340e-01 | ❌ No | [-0.0114, 0.1460] |
| llama3.2:latest_baseline vs mistral-nemo:latest_baseline | -0.0262 | 1.0000e+00 | ❌ No | [-0.1049, 0.0525] |
| llama3.2:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0691 | 1.8950e-01 | ❌ No | [-0.1478, 0.0096] |
| llama3.2:latest_baseline vs nemotron-mini:4b_baseline | -0.3497 | 0.0000e+00 | ✅ Yes | [-0.4284, -0.2710] |
| llama3.2:latest_baseline vs nemotron-mini:4b_kb_rag | -0.2271 | 0.0000e+00 | ✅ Yes | [-0.3058, -0.1484] |
| llama3.2:latest_baseline vs qwen2.5:14b_baseline | 0.0636 | 3.4270e-01 | ❌ No | [-0.0151, 0.1423] |
| llama3.2:latest_baseline vs qwen2.5:14b_kb_rag | 0.0705 | 1.5900e-01 | ❌ No | [-0.0082, 0.1492] |
| llama3.2:latest_baseline vs qwen3:8b_baseline | 0.0578 | 5.5480e-01 | ❌ No | [-0.0209, 0.1365] |
| llama3.2:latest_baseline vs qwen3:8b_kb_rag | 0.0572 | 5.7460e-01 | ❌ No | [-0.0214, 0.1359] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_baseline | -0.0935 | 3.5000e-03 | ✅ Yes | [-0.1722, -0.0148] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.1364 | 0.0000e+00 | ✅ Yes | [-0.2151, -0.0577] |
| llama3.2:latest_kb_rag vs nemotron-mini:4b_baseline | -0.4170 | 0.0000e+00 | ✅ Yes | [-0.4957, -0.3383] |
| llama3.2:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.2944 | 0.0000e+00 | ✅ Yes | [-0.3731, -0.2157] |
| llama3.2:latest_kb_rag vs qwen2.5:14b_baseline | -0.0037 | 1.0000e+00 | ❌ No | [-0.0824, 0.0750] |
| llama3.2:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0032 | 1.0000e+00 | ❌ No | [-0.0755, 0.0819] |
| llama3.2:latest_kb_rag vs qwen3:8b_baseline | -0.0095 | 1.0000e+00 | ❌ No | [-0.0882, 0.0692] |
| llama3.2:latest_kb_rag vs qwen3:8b_kb_rag | -0.0100 | 1.0000e+00 | ❌ No | [-0.0887, 0.0687] |
| mistral-nemo:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0429 | 9.5960e-01 | ❌ No | [-0.1216, 0.0358] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_baseline | -0.3234 | 0.0000e+00 | ✅ Yes | [-0.4021, -0.2447] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_kb_rag | -0.2009 | 0.0000e+00 | ✅ Yes | [-0.2796, -0.1222] |
| mistral-nemo:latest_baseline vs qwen2.5:14b_baseline | 0.0898 | 7.2000e-03 | ✅ Yes | [0.0111, 0.1685] |
| mistral-nemo:latest_baseline vs qwen2.5:14b_kb_rag | 0.0967 | 1.8000e-03 | ✅ Yes | [0.0180, 0.1754] |
| mistral-nemo:latest_baseline vs qwen3:8b_baseline | 0.0840 | 2.0900e-02 | ✅ Yes | [0.0053, 0.1627] |
| mistral-nemo:latest_baseline vs qwen3:8b_kb_rag | 0.0835 | 2.2800e-02 | ✅ Yes | [0.0048, 0.1622] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_baseline | -0.2806 | 0.0000e+00 | ✅ Yes | [-0.3593, -0.2019] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.1580 | 0.0000e+00 | ✅ Yes | [-0.2367, -0.0793] |
| mistral-nemo:latest_kb_rag vs qwen2.5:14b_baseline | 0.1327 | 0.0000e+00 | ✅ Yes | [0.0540, 0.2114] |
| mistral-nemo:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.1396 | 0.0000e+00 | ✅ Yes | [0.0609, 0.2183] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_baseline | 0.1268 | 0.0000e+00 | ✅ Yes | [0.0482, 0.2055] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_kb_rag | 0.1263 | 0.0000e+00 | ✅ Yes | [0.0476, 0.2050] |
| nemotron-mini:4b_baseline vs nemotron-mini:4b_kb_rag | 0.1226 | 0.0000e+00 | ✅ Yes | [0.0439, 0.2013] |
| nemotron-mini:4b_baseline vs qwen2.5:14b_baseline | 0.4133 | 0.0000e+00 | ✅ Yes | [0.3346, 0.4920] |
| nemotron-mini:4b_baseline vs qwen2.5:14b_kb_rag | 0.4202 | 0.0000e+00 | ✅ Yes | [0.3415, 0.4989] |
| nemotron-mini:4b_baseline vs qwen3:8b_baseline | 0.4074 | 0.0000e+00 | ✅ Yes | [0.3287, 0.4861] |
| nemotron-mini:4b_baseline vs qwen3:8b_kb_rag | 0.4069 | 0.0000e+00 | ✅ Yes | [0.3282, 0.4856] |
| nemotron-mini:4b_kb_rag vs qwen2.5:14b_baseline | 0.2907 | 0.0000e+00 | ✅ Yes | [0.2120, 0.3694] |
| nemotron-mini:4b_kb_rag vs qwen2.5:14b_kb_rag | 0.2976 | 0.0000e+00 | ✅ Yes | [0.2189, 0.3763] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_baseline | 0.2849 | 0.0000e+00 | ✅ Yes | [0.2062, 0.3636] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_kb_rag | 0.2843 | 0.0000e+00 | ✅ Yes | [0.2056, 0.3630] |
| qwen2.5:14b_baseline vs qwen2.5:14b_kb_rag | 0.0069 | 1.0000e+00 | ❌ No | [-0.0718, 0.0856] |
| qwen2.5:14b_baseline vs qwen3:8b_baseline | -0.0058 | 1.0000e+00 | ❌ No | [-0.0845, 0.0729] |
| qwen2.5:14b_baseline vs qwen3:8b_kb_rag | -0.0064 | 1.0000e+00 | ❌ No | [-0.0851, 0.0723] |
| qwen2.5:14b_kb_rag vs qwen3:8b_baseline | -0.0127 | 1.0000e+00 | ❌ No | [-0.0914, 0.0659] |
| qwen2.5:14b_kb_rag vs qwen3:8b_kb_rag | -0.0133 | 1.0000e+00 | ❌ No | [-0.0920, 0.0654] |
| qwen3:8b_baseline vs qwen3:8b_kb_rag | -0.0005 | 1.0000e+00 | ❌ No | [-0.0792, 0.0782] |

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
| nemotron-mini:4b_baseline | 0.2829 | 0.2787 | -0.0041 | 📉 Decreased |
| nemotron-mini:4b_kb_rag | 0.4055 | 0.4038 | -0.0016 | 📉 Decreased |
| qwen2.5:14b_baseline | 0.6961 | 0.6973 | +0.0012 | 📈 Improved |
| qwen2.5:14b_kb_rag | 0.7031 | 0.7027 | -0.0003 | 📉 Decreased |
| qwen3:8b_baseline | 0.6903 | 0.6927 | +0.0024 | 📈 Improved |
| qwen3:8b_kb_rag | 0.6898 | 0.6900 | +0.0002 | 📈 Improved |
