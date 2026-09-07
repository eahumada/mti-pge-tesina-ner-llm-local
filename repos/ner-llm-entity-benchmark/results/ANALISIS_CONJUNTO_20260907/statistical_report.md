# 🔗 Merged Benchmark Analysis — Provenance & Integrity

- **Corpus:** `data/benchmark_balanced_120.json`
- **Registros esperados por modelo+modo:** 120
- **Corridas combinadas:** 8
- **Grupos (modelo+modo) analizados:** 26
- **Filas totales tras el merge:** 3120

## Fuentes
| # | Corrida | CSV | Filas | Modelos aportados |
| :---: | :--- | :--- | :---: | :---: |
| 1 | 00_gptoss_rerun | `/private/tmp/claude-501/-Users-eahumada-Documents-Personal-MTI-mti-pge-tesina-ner-llm-local/87e8505b-1ba9-4f7a-8204-01d63aa41522/scratchpad/anova_stage/00_gptoss_rerun/benchmark_results.csv` | 240 | 2 |
| 2 | 01_qwen3_nothink | `/private/tmp/claude-501/-Users-eahumada-Documents-Personal-MTI-mti-pge-tesina-ner-llm-local/87e8505b-1ba9-4f7a-8204-01d63aa41522/scratchpad/anova_stage/01_qwen3_nothink/benchmark_results.csv` | 240 | 2 |
| 3 | 02_gemma4_12b_mlx | `/private/tmp/claude-501/-Users-eahumada-Documents-Personal-MTI-mti-pge-tesina-ner-llm-local/87e8505b-1ba9-4f7a-8204-01d63aa41522/scratchpad/anova_stage/02_gemma4_12b_mlx/benchmark_results.csv` | 240 | 2 |
| 4 | 03_nemotron_rerun | `/private/tmp/claude-501/-Users-eahumada-Documents-Personal-MTI-mti-pge-tesina-ner-llm-local/87e8505b-1ba9-4f7a-8204-01d63aa41522/scratchpad/anova_stage/03_nemotron_rerun/benchmark_results.csv` | 240 | 2 |
| 5 | 04_cloud | `/private/tmp/claude-501/-Users-eahumada-Documents-Personal-MTI-mti-pge-tesina-ner-llm-local/87e8505b-1ba9-4f7a-8204-01d63aa41522/scratchpad/anova_stage/04_cloud/benchmark_results.csv` | 240 | 2 |
| 6 | 05_excluidos | `/private/tmp/claude-501/-Users-eahumada-Documents-Personal-MTI-mti-pge-tesina-ner-llm-local/87e8505b-1ba9-4f7a-8204-01d63aa41522/scratchpad/anova_stage/05_excluidos/benchmark_results.csv` | 240 | 2 |
| 7 | 06_P3 | `/private/tmp/claude-501/-Users-eahumada-Documents-Personal-MTI-mti-pge-tesina-ner-llm-local/87e8505b-1ba9-4f7a-8204-01d63aa41522/scratchpad/anova_stage/06_P3/benchmark_results.csv` | 1440 | 12 |
| 8 | 07_legacy_kbrag | `/private/tmp/claude-501/-Users-eahumada-Documents-Personal-MTI-mti-pge-tesina-ner-llm-local/87e8505b-1ba9-4f7a-8204-01d63aa41522/scratchpad/anova_stage/07_legacy_kbrag/benchmark_results.csv` | 1200 | 10 |

## Integridad por grupo (modelo + modo)
| Modelo | Filas | record_id unicos | Esperados | f1 NaN | Estado |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gpt-oss:20b_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| gpt-oss:20b_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
| qwen3:8b_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| qwen3:8b_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
| gemma4:12b-mlx_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| gemma4:12b-mlx_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
| nemotron-mini:4b_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| nemotron-mini:4b_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
| gemma4:31b-cloud_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| gemma4:31b-cloud_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
| mistral-nemo:latest_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| mistral-nemo:latest_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
| llama3.1:8b_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| llama3.1:8b_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
| deepseek-r1:1.5b_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| deepseek-r1:1.5b_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
| llama3.2:latest_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| llama3.2:latest_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
| gemma4:latest_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| gemma4:latest_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
| gemma4:31b-mlx_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| gemma4:31b-mlx_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
| qwen2.5:14b_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| qwen2.5:14b_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
| gemma:latest_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| gemma:latest_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |

## Advertencias
- ⚠️ DUPLICADO: 'gpt-oss:20b_baseline' aparece en '00_gptoss_rerun' y en '05_excluidos'. Se conservan las filas de '00_gptoss_rerun' (--on-duplicate=first).
- ⚠️ DUPLICADO: 'gpt-oss:20b_kb_rag' aparece en '00_gptoss_rerun' y en '05_excluidos'. Se conservan las filas de '00_gptoss_rerun' (--on-duplicate=first).
- ⚠️ DUPLICADO: 'gemma4:12b-mlx_baseline' aparece en '02_gemma4_12b_mlx' y en '06_P3'. Se conservan las filas de '02_gemma4_12b_mlx' (--on-duplicate=first).
- ⚠️ DUPLICADO: 'gemma4:12b-mlx_kb_rag' aparece en '02_gemma4_12b_mlx' y en '06_P3'. Se conservan las filas de '02_gemma4_12b_mlx' (--on-duplicate=first).
- ⚠️ DUPLICADO: 'qwen3:8b_baseline' aparece en '01_qwen3_nothink' y en '06_P3'. Se conservan las filas de '01_qwen3_nothink' (--on-duplicate=first).
- ⚠️ DUPLICADO: 'qwen3:8b_kb_rag' aparece en '01_qwen3_nothink' y en '06_P3'. Se conservan las filas de '01_qwen3_nothink' (--on-duplicate=first).
- ⚠️ DUPLICADO: 'nemotron-mini:4b_baseline' aparece en '03_nemotron_rerun' y en '06_P3'. Se conservan las filas de '03_nemotron_rerun' (--on-duplicate=first).
- ⚠️ DUPLICADO: 'nemotron-mini:4b_kb_rag' aparece en '03_nemotron_rerun' y en '06_P3'. Se conservan las filas de '03_nemotron_rerun' (--on-duplicate=first).

---
# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 38.2222
- **p-Value:** 3.4453e-160

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| gpt-oss:20b_baseline | 120 | 0.5239 | 0.4885 | 0.5594 | 0.1961 |
| gpt-oss:20b_kb_rag | 120 | 0.5567 | 0.5222 | 0.5912 | 0.1910 |
| qwen3:8b_baseline | 120 | 0.4821 | 0.4495 | 0.5147 | 0.1802 |
| qwen3:8b_kb_rag | 120 | 0.5146 | 0.4791 | 0.5501 | 0.1963 |
| gemma4:12b-mlx_baseline | 120 | 0.5618 | 0.5296 | 0.5940 | 0.1783 |
| gemma4:12b-mlx_kb_rag | 120 | 0.5846 | 0.5493 | 0.6199 | 0.1953 |
| nemotron-mini:4b_baseline | 120 | 0.2259 | 0.1936 | 0.2582 | 0.1787 |
| nemotron-mini:4b_kb_rag | 120 | 0.3712 | 0.3321 | 0.4102 | 0.2161 |
| gemma4:31b-cloud_baseline | 120 | 0.6238 | 0.5895 | 0.6582 | 0.1902 |
| gemma4:31b-cloud_kb_rag | 120 | 0.6185 | 0.5845 | 0.6525 | 0.1881 |
| mistral-nemo:latest_baseline | 120 | 0.4338 | 0.3963 | 0.4714 | 0.2076 |
| mistral-nemo:latest_kb_rag | 120 | 0.4576 | 0.4203 | 0.4949 | 0.2064 |
| llama3.1:8b_baseline | 120 | 0.4876 | 0.4542 | 0.5210 | 0.1848 |
| llama3.1:8b_kb_rag | 120 | 0.5075 | 0.4680 | 0.5469 | 0.2183 |
| deepseek-r1:1.5b_baseline | 120 | 0.2483 | 0.2163 | 0.2804 | 0.1775 |
| deepseek-r1:1.5b_kb_rag | 120 | 0.2394 | 0.2036 | 0.2752 | 0.1979 |
| llama3.2:latest_baseline | 120 | 0.3611 | 0.3235 | 0.3987 | 0.2080 |
| llama3.2:latest_kb_rag | 120 | 0.4693 | 0.4320 | 0.5067 | 0.2065 |
| gemma4:latest_baseline | 120 | 0.5591 | 0.5229 | 0.5953 | 0.2004 |
| gemma4:latest_kb_rag | 120 | 0.5474 | 0.5094 | 0.5855 | 0.2106 |
| gemma4:31b-mlx_baseline | 120 | 0.5925 | 0.5575 | 0.6276 | 0.1937 |
| gemma4:31b-mlx_kb_rag | 120 | 0.5907 | 0.5516 | 0.6299 | 0.2167 |
| qwen2.5:14b_baseline | 120 | 0.5022 | 0.4681 | 0.5363 | 0.1888 |
| qwen2.5:14b_kb_rag | 120 | 0.5484 | 0.5133 | 0.5835 | 0.1940 |
| gemma:latest_baseline | 120 | 0.4400 | 0.3988 | 0.4813 | 0.2282 |
| gemma:latest_kb_rag | 120 | 0.5136 | 0.4749 | 0.5524 | 0.2143 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline vs deepseek-r1:1.5b_kb_rag | -0.0090 | 1.0000e+00 | ❌ No | [-0.1036, 0.0856] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_baseline | 0.3135 | 0.0000e+00 | ✅ Yes | [0.2189, 0.4081] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_kb_rag | 0.3363 | 0.0000e+00 | ✅ Yes | [0.2417, 0.4309] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_baseline | 0.3755 | 0.0000e+00 | ✅ Yes | [0.2809, 0.4701] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_kb_rag | 0.3701 | 0.0000e+00 | ✅ Yes | [0.2755, 0.4647] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_baseline | 0.3442 | 0.0000e+00 | ✅ Yes | [0.2496, 0.4388] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_kb_rag | 0.3424 | 0.0000e+00 | ✅ Yes | [0.2478, 0.4370] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_baseline | 0.3108 | 0.0000e+00 | ✅ Yes | [0.2162, 0.4054] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_kb_rag | 0.2991 | 0.0000e+00 | ✅ Yes | [0.2045, 0.3937] |
| deepseek-r1:1.5b_baseline vs gemma:latest_baseline | 0.1917 | 0.0000e+00 | ✅ Yes | [0.0971, 0.2863] |
| deepseek-r1:1.5b_baseline vs gemma:latest_kb_rag | 0.2653 | 0.0000e+00 | ✅ Yes | [0.1707, 0.3599] |
| deepseek-r1:1.5b_baseline vs gpt-oss:20b_baseline | 0.2756 | 0.0000e+00 | ✅ Yes | [0.1810, 0.3702] |
| deepseek-r1:1.5b_baseline vs gpt-oss:20b_kb_rag | 0.3084 | 0.0000e+00 | ✅ Yes | [0.2138, 0.4030] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_baseline | 0.2393 | 0.0000e+00 | ✅ Yes | [0.1447, 0.3339] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_kb_rag | 0.2591 | 0.0000e+00 | ✅ Yes | [0.1645, 0.3537] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_baseline | 0.1128 | 3.3000e-03 | ✅ Yes | [0.0182, 0.2074] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_kb_rag | 0.2210 | 0.0000e+00 | ✅ Yes | [0.1264, 0.3156] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_baseline | 0.1855 | 0.0000e+00 | ✅ Yes | [0.0909, 0.2801] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_kb_rag | 0.2092 | 0.0000e+00 | ✅ Yes | [0.1146, 0.3038] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_baseline | -0.0224 | 1.0000e+00 | ❌ No | [-0.1170, 0.0722] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_kb_rag | 0.1228 | 5.0000e-04 | ✅ Yes | [0.0282, 0.2174] |
| deepseek-r1:1.5b_baseline vs qwen2.5:14b_baseline | 0.2539 | 0.0000e+00 | ✅ Yes | [0.1593, 0.3485] |
| deepseek-r1:1.5b_baseline vs qwen2.5:14b_kb_rag | 0.3001 | 0.0000e+00 | ✅ Yes | [0.2055, 0.3947] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_baseline | 0.2338 | 0.0000e+00 | ✅ Yes | [0.1392, 0.3284] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_kb_rag | 0.2663 | 0.0000e+00 | ✅ Yes | [0.1717, 0.3609] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_baseline | 0.3225 | 0.0000e+00 | ✅ Yes | [0.2279, 0.4171] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_kb_rag | 0.3452 | 0.0000e+00 | ✅ Yes | [0.2506, 0.4398] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-cloud_baseline | 0.3845 | 0.0000e+00 | ✅ Yes | [0.2899, 0.4791] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-cloud_kb_rag | 0.3791 | 0.0000e+00 | ✅ Yes | [0.2845, 0.4737] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-mlx_baseline | 0.3532 | 0.0000e+00 | ✅ Yes | [0.2586, 0.4478] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-mlx_kb_rag | 0.3514 | 0.0000e+00 | ✅ Yes | [0.2568, 0.4460] |
| deepseek-r1:1.5b_kb_rag vs gemma4:latest_baseline | 0.3198 | 0.0000e+00 | ✅ Yes | [0.2252, 0.4144] |
| deepseek-r1:1.5b_kb_rag vs gemma4:latest_kb_rag | 0.3081 | 0.0000e+00 | ✅ Yes | [0.2135, 0.4027] |
| deepseek-r1:1.5b_kb_rag vs gemma:latest_baseline | 0.2007 | 0.0000e+00 | ✅ Yes | [0.1061, 0.2953] |
| deepseek-r1:1.5b_kb_rag vs gemma:latest_kb_rag | 0.2743 | 0.0000e+00 | ✅ Yes | [0.1797, 0.3689] |
| deepseek-r1:1.5b_kb_rag vs gpt-oss:20b_baseline | 0.2845 | 0.0000e+00 | ✅ Yes | [0.1899, 0.3791] |
| deepseek-r1:1.5b_kb_rag vs gpt-oss:20b_kb_rag | 0.3173 | 0.0000e+00 | ✅ Yes | [0.2227, 0.4119] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_baseline | 0.2482 | 0.0000e+00 | ✅ Yes | [0.1536, 0.3428] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_kb_rag | 0.2681 | 0.0000e+00 | ✅ Yes | [0.1735, 0.3627] |
| deepseek-r1:1.5b_kb_rag vs llama3.2:latest_baseline | 0.1217 | 7.0000e-04 | ✅ Yes | [0.0271, 0.2163] |
| deepseek-r1:1.5b_kb_rag vs llama3.2:latest_kb_rag | 0.2300 | 0.0000e+00 | ✅ Yes | [0.1354, 0.3246] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_baseline | 0.1945 | 0.0000e+00 | ✅ Yes | [0.0999, 0.2891] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_kb_rag | 0.2182 | 0.0000e+00 | ✅ Yes | [0.1236, 0.3128] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_baseline | -0.0134 | 1.0000e+00 | ❌ No | [-0.1081, 0.0812] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_kb_rag | 0.1318 | 1.0000e-04 | ✅ Yes | [0.0372, 0.2264] |
| deepseek-r1:1.5b_kb_rag vs qwen2.5:14b_baseline | 0.2628 | 0.0000e+00 | ✅ Yes | [0.1682, 0.3574] |
| deepseek-r1:1.5b_kb_rag vs qwen2.5:14b_kb_rag | 0.3090 | 0.0000e+00 | ✅ Yes | [0.2144, 0.4036] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_baseline | 0.2427 | 0.0000e+00 | ✅ Yes | [0.1481, 0.3373] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_kb_rag | 0.2752 | 0.0000e+00 | ✅ Yes | [0.1806, 0.3698] |
| gemma4:12b-mlx_baseline vs gemma4:12b-mlx_kb_rag | 0.0228 | 1.0000e+00 | ❌ No | [-0.0718, 0.1174] |
| gemma4:12b-mlx_baseline vs gemma4:31b-cloud_baseline | 0.0620 | 7.7690e-01 | ❌ No | [-0.0326, 0.1566] |
| gemma4:12b-mlx_baseline vs gemma4:31b-cloud_kb_rag | 0.0566 | 8.9420e-01 | ❌ No | [-0.0380, 0.1512] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_baseline | 0.0307 | 1.0000e+00 | ❌ No | [-0.0639, 0.1253] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_kb_rag | 0.0289 | 1.0000e+00 | ❌ No | [-0.0657, 0.1235] |
| gemma4:12b-mlx_baseline vs gemma4:latest_baseline | -0.0027 | 1.0000e+00 | ❌ No | [-0.0973, 0.0919] |
| gemma4:12b-mlx_baseline vs gemma4:latest_kb_rag | -0.0144 | 1.0000e+00 | ❌ No | [-0.1090, 0.0802] |
| gemma4:12b-mlx_baseline vs gemma:latest_baseline | -0.1218 | 7.0000e-04 | ✅ Yes | [-0.2164, -0.0272] |
| gemma4:12b-mlx_baseline vs gemma:latest_kb_rag | -0.0482 | 9.8170e-01 | ❌ No | [-0.1428, 0.0464] |
| gemma4:12b-mlx_baseline vs gpt-oss:20b_baseline | -0.0379 | 9.9940e-01 | ❌ No | [-0.1325, 0.0567] |
| gemma4:12b-mlx_baseline vs gpt-oss:20b_kb_rag | -0.0051 | 1.0000e+00 | ❌ No | [-0.0997, 0.0895] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_baseline | -0.0742 | 4.0640e-01 | ❌ No | [-0.1688, 0.0204] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_kb_rag | -0.0543 | 9.2910e-01 | ❌ No | [-0.1489, 0.0403] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_baseline | -0.2007 | 0.0000e+00 | ✅ Yes | [-0.2953, -0.1061] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_kb_rag | -0.0925 | 6.5500e-02 | ❌ No | [-0.1871, 0.0021] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_baseline | -0.1280 | 2.0000e-04 | ✅ Yes | [-0.2226, -0.0334] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.1043 | 1.2800e-02 | ✅ Yes | [-0.1989, -0.0097] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_baseline | -0.3359 | 0.0000e+00 | ✅ Yes | [-0.4305, -0.2413] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_kb_rag | -0.1907 | 0.0000e+00 | ✅ Yes | [-0.2853, -0.0961] |
| gemma4:12b-mlx_baseline vs qwen2.5:14b_baseline | -0.0596 | 8.3510e-01 | ❌ No | [-0.1542, 0.0350] |
| gemma4:12b-mlx_baseline vs qwen2.5:14b_kb_rag | -0.0134 | 1.0000e+00 | ❌ No | [-0.1080, 0.0812] |
| gemma4:12b-mlx_baseline vs qwen3:8b_baseline | -0.0797 | 2.5960e-01 | ❌ No | [-0.1743, 0.0149] |
| gemma4:12b-mlx_baseline vs qwen3:8b_kb_rag | -0.0472 | 9.8580e-01 | ❌ No | [-0.1418, 0.0474] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-cloud_baseline | 0.0392 | 9.9900e-01 | ❌ No | [-0.0554, 0.1338] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-cloud_kb_rag | 0.0339 | 9.9990e-01 | ❌ No | [-0.0607, 0.1285] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_baseline | 0.0080 | 1.0000e+00 | ❌ No | [-0.0866, 0.1026] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_kb_rag | 0.0062 | 1.0000e+00 | ❌ No | [-0.0884, 0.1008] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_baseline | -0.0255 | 1.0000e+00 | ❌ No | [-0.1201, 0.0691] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0372 | 9.9960e-01 | ❌ No | [-0.1318, 0.0574] |
| gemma4:12b-mlx_kb_rag vs gemma:latest_baseline | -0.1446 | 0.0000e+00 | ✅ Yes | [-0.2392, -0.0500] |
| gemma4:12b-mlx_kb_rag vs gemma:latest_kb_rag | -0.0710 | 5.0680e-01 | ❌ No | [-0.1656, 0.0236] |
| gemma4:12b-mlx_kb_rag vs gpt-oss:20b_baseline | -0.0607 | 8.1050e-01 | ❌ No | [-0.1553, 0.0339] |
| gemma4:12b-mlx_kb_rag vs gpt-oss:20b_kb_rag | -0.0279 | 1.0000e+00 | ❌ No | [-0.1225, 0.0667] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_baseline | -0.0970 | 3.6400e-02 | ✅ Yes | [-0.1916, -0.0024] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_kb_rag | -0.0771 | 3.2500e-01 | ❌ No | [-0.1717, 0.0175] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_baseline | -0.2235 | 0.0000e+00 | ✅ Yes | [-0.3181, -0.1289] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.1152 | 2.1000e-03 | ✅ Yes | [-0.2098, -0.0206] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.1507 | 0.0000e+00 | ✅ Yes | [-0.2453, -0.0561] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.1270 | 2.0000e-04 | ✅ Yes | [-0.2216, -0.0324] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_baseline | -0.3587 | 0.0000e+00 | ✅ Yes | [-0.4533, -0.2641] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | -0.2134 | 0.0000e+00 | ✅ Yes | [-0.3080, -0.1188] |
| gemma4:12b-mlx_kb_rag vs qwen2.5:14b_baseline | -0.0824 | 2.0210e-01 | ❌ No | [-0.1770, 0.0122] |
| gemma4:12b-mlx_kb_rag vs qwen2.5:14b_kb_rag | -0.0362 | 9.9970e-01 | ❌ No | [-0.1308, 0.0584] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_baseline | -0.1025 | 1.6700e-02 | ✅ Yes | [-0.1971, -0.0079] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.0700 | 5.3680e-01 | ❌ No | [-0.1646, 0.0246] |
| gemma4:31b-cloud_baseline vs gemma4:31b-cloud_kb_rag | -0.0054 | 1.0000e+00 | ❌ No | [-0.1000, 0.0892] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_baseline | -0.0313 | 1.0000e+00 | ❌ No | [-0.1259, 0.0633] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_kb_rag | -0.0331 | 9.9990e-01 | ❌ No | [-0.1277, 0.0615] |
| gemma4:31b-cloud_baseline vs gemma4:latest_baseline | -0.0647 | 7.0150e-01 | ❌ No | [-0.1593, 0.0299] |
| gemma4:31b-cloud_baseline vs gemma4:latest_kb_rag | -0.0764 | 3.4400e-01 | ❌ No | [-0.1710, 0.0182] |
| gemma4:31b-cloud_baseline vs gemma:latest_baseline | -0.1838 | 0.0000e+00 | ✅ Yes | [-0.2784, -0.0892] |
| gemma4:31b-cloud_baseline vs gemma:latest_kb_rag | -0.1102 | 5.0000e-03 | ✅ Yes | [-0.2048, -0.0156] |
| gemma4:31b-cloud_baseline vs gpt-oss:20b_baseline | -0.0999 | 2.4200e-02 | ✅ Yes | [-0.1945, -0.0053] |
| gemma4:31b-cloud_baseline vs gpt-oss:20b_kb_rag | -0.0671 | 6.2800e-01 | ❌ No | [-0.1617, 0.0275] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_baseline | -0.1362 | 0.0000e+00 | ✅ Yes | [-0.2308, -0.0416] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_kb_rag | -0.1164 | 1.8000e-03 | ✅ Yes | [-0.2110, -0.0218] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_baseline | -0.2627 | 0.0000e+00 | ✅ Yes | [-0.3573, -0.1681] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_kb_rag | -0.1545 | 0.0000e+00 | ✅ Yes | [-0.2491, -0.0599] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_baseline | -0.1900 | 0.0000e+00 | ✅ Yes | [-0.2846, -0.0954] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_kb_rag | -0.1663 | 0.0000e+00 | ✅ Yes | [-0.2609, -0.0717] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_baseline | -0.3979 | 0.0000e+00 | ✅ Yes | [-0.4925, -0.3033] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_kb_rag | -0.2527 | 0.0000e+00 | ✅ Yes | [-0.3473, -0.1581] |
| gemma4:31b-cloud_baseline vs qwen2.5:14b_baseline | -0.1216 | 7.0000e-04 | ✅ Yes | [-0.2162, -0.0270] |
| gemma4:31b-cloud_baseline vs qwen2.5:14b_kb_rag | -0.0754 | 3.7140e-01 | ❌ No | [-0.1700, 0.0192] |
| gemma4:31b-cloud_baseline vs qwen3:8b_baseline | -0.1417 | 0.0000e+00 | ✅ Yes | [-0.2363, -0.0471] |
| gemma4:31b-cloud_baseline vs qwen3:8b_kb_rag | -0.1093 | 5.9000e-03 | ✅ Yes | [-0.2039, -0.0147] |
| gemma4:31b-cloud_kb_rag vs gemma4:31b-mlx_baseline | -0.0259 | 1.0000e+00 | ❌ No | [-0.1205, 0.0687] |
| gemma4:31b-cloud_kb_rag vs gemma4:31b-mlx_kb_rag | -0.0277 | 1.0000e+00 | ❌ No | [-0.1223, 0.0669] |
| gemma4:31b-cloud_kb_rag vs gemma4:latest_baseline | -0.0593 | 8.4140e-01 | ❌ No | [-0.1539, 0.0353] |
| gemma4:31b-cloud_kb_rag vs gemma4:latest_kb_rag | -0.0710 | 5.0420e-01 | ❌ No | [-0.1656, 0.0236] |
| gemma4:31b-cloud_kb_rag vs gemma:latest_baseline | -0.1784 | 0.0000e+00 | ✅ Yes | [-0.2730, -0.0838] |
| gemma4:31b-cloud_kb_rag vs gemma:latest_kb_rag | -0.1048 | 1.1700e-02 | ✅ Yes | [-0.1994, -0.0102] |
| gemma4:31b-cloud_kb_rag vs gpt-oss:20b_baseline | -0.0946 | 5.0300e-02 | ❌ No | [-0.1892, 0.0000] |
| gemma4:31b-cloud_kb_rag vs gpt-oss:20b_kb_rag | -0.0618 | 7.8370e-01 | ❌ No | [-0.1564, 0.0328] |
| gemma4:31b-cloud_kb_rag vs llama3.1:8b_baseline | -0.1309 | 1.0000e-04 | ✅ Yes | [-0.2255, -0.0363] |
| gemma4:31b-cloud_kb_rag vs llama3.1:8b_kb_rag | -0.1110 | 4.4000e-03 | ✅ Yes | [-0.2056, -0.0164] |
| gemma4:31b-cloud_kb_rag vs llama3.2:latest_baseline | -0.2574 | 0.0000e+00 | ✅ Yes | [-0.3520, -0.1628] |
| gemma4:31b-cloud_kb_rag vs llama3.2:latest_kb_rag | -0.1491 | 0.0000e+00 | ✅ Yes | [-0.2437, -0.0545] |
| gemma4:31b-cloud_kb_rag vs mistral-nemo:latest_baseline | -0.1846 | 0.0000e+00 | ✅ Yes | [-0.2792, -0.0900] |
| gemma4:31b-cloud_kb_rag vs mistral-nemo:latest_kb_rag | -0.1609 | 0.0000e+00 | ✅ Yes | [-0.2555, -0.0663] |
| gemma4:31b-cloud_kb_rag vs nemotron-mini:4b_baseline | -0.3925 | 0.0000e+00 | ✅ Yes | [-0.4871, -0.2979] |
| gemma4:31b-cloud_kb_rag vs nemotron-mini:4b_kb_rag | -0.2473 | 0.0000e+00 | ✅ Yes | [-0.3419, -0.1527] |
| gemma4:31b-cloud_kb_rag vs qwen2.5:14b_baseline | -0.1163 | 1.8000e-03 | ✅ Yes | [-0.2109, -0.0217] |
| gemma4:31b-cloud_kb_rag vs qwen2.5:14b_kb_rag | -0.0701 | 5.3520e-01 | ❌ No | [-0.1647, 0.0245] |
| gemma4:31b-cloud_kb_rag vs qwen3:8b_baseline | -0.1364 | 0.0000e+00 | ✅ Yes | [-0.2310, -0.0418] |
| gemma4:31b-cloud_kb_rag vs qwen3:8b_kb_rag | -0.1039 | 1.3600e-02 | ✅ Yes | [-0.1985, -0.0093] |
| gemma4:31b-mlx_baseline vs gemma4:31b-mlx_kb_rag | -0.0018 | 1.0000e+00 | ❌ No | [-0.0964, 0.0928] |
| gemma4:31b-mlx_baseline vs gemma4:latest_baseline | -0.0334 | 9.9990e-01 | ❌ No | [-0.1280, 0.0612] |
| gemma4:31b-mlx_baseline vs gemma4:latest_kb_rag | -0.0451 | 9.9230e-01 | ❌ No | [-0.1397, 0.0495] |
| gemma4:31b-mlx_baseline vs gemma:latest_baseline | -0.1525 | 0.0000e+00 | ✅ Yes | [-0.2471, -0.0579] |
| gemma4:31b-mlx_baseline vs gemma:latest_kb_rag | -0.0789 | 2.7910e-01 | ❌ No | [-0.1735, 0.0157] |
| gemma4:31b-mlx_baseline vs gpt-oss:20b_baseline | -0.0686 | 5.8040e-01 | ❌ No | [-0.1632, 0.0260] |
| gemma4:31b-mlx_baseline vs gpt-oss:20b_kb_rag | -0.0358 | 9.9980e-01 | ❌ No | [-0.1304, 0.0588] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_baseline | -0.1049 | 1.1500e-02 | ✅ Yes | [-0.1996, -0.0103] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_kb_rag | -0.0851 | 1.5400e-01 | ❌ No | [-0.1797, 0.0095] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_baseline | -0.2314 | 0.0000e+00 | ✅ Yes | [-0.3260, -0.1368] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_kb_rag | -0.1232 | 5.0000e-04 | ✅ Yes | [-0.2178, -0.0286] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_baseline | -0.1587 | 0.0000e+00 | ✅ Yes | [-0.2533, -0.0641] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.1350 | 1.0000e-04 | ✅ Yes | [-0.2296, -0.0404] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_baseline | -0.3666 | 0.0000e+00 | ✅ Yes | [-0.4612, -0.2720] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_kb_rag | -0.2214 | 0.0000e+00 | ✅ Yes | [-0.3160, -0.1268] |
| gemma4:31b-mlx_baseline vs qwen2.5:14b_baseline | -0.0904 | 8.5000e-02 | ❌ No | [-0.1850, 0.0042] |
| gemma4:31b-mlx_baseline vs qwen2.5:14b_kb_rag | -0.0441 | 9.9430e-01 | ❌ No | [-0.1387, 0.0505] |
| gemma4:31b-mlx_baseline vs qwen3:8b_baseline | -0.1105 | 4.8000e-03 | ✅ Yes | [-0.2051, -0.0159] |
| gemma4:31b-mlx_baseline vs qwen3:8b_kb_rag | -0.0780 | 3.0290e-01 | ❌ No | [-0.1726, 0.0166] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_baseline | -0.0316 | 1.0000e+00 | ❌ No | [-0.1262, 0.0630] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0433 | 9.9560e-01 | ❌ No | [-0.1379, 0.0513] |
| gemma4:31b-mlx_kb_rag vs gemma:latest_baseline | -0.1507 | 0.0000e+00 | ✅ Yes | [-0.2453, -0.0561] |
| gemma4:31b-mlx_kb_rag vs gemma:latest_kb_rag | -0.0771 | 3.2510e-01 | ❌ No | [-0.1717, 0.0175] |
| gemma4:31b-mlx_kb_rag vs gpt-oss:20b_baseline | -0.0668 | 6.3700e-01 | ❌ No | [-0.1614, 0.0278] |
| gemma4:31b-mlx_kb_rag vs gpt-oss:20b_kb_rag | -0.0340 | 9.9990e-01 | ❌ No | [-0.1286, 0.0606] |
| gemma4:31b-mlx_kb_rag vs llama3.1:8b_baseline | -0.1031 | 1.5100e-02 | ✅ Yes | [-0.1977, -0.0085] |
| gemma4:31b-mlx_kb_rag vs llama3.1:8b_kb_rag | -0.0833 | 1.8530e-01 | ❌ No | [-0.1779, 0.0113] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_baseline | -0.2296 | 0.0000e+00 | ✅ Yes | [-0.3242, -0.1350] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.1214 | 7.0000e-04 | ✅ Yes | [-0.2160, -0.0268] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.1569 | 0.0000e+00 | ✅ Yes | [-0.2515, -0.0623] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.1332 | 1.0000e-04 | ✅ Yes | [-0.2278, -0.0386] |
| gemma4:31b-mlx_kb_rag vs nemotron-mini:4b_baseline | -0.3648 | 0.0000e+00 | ✅ Yes | [-0.4594, -0.2702] |
| gemma4:31b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | -0.2196 | 0.0000e+00 | ✅ Yes | [-0.3142, -0.1250] |
| gemma4:31b-mlx_kb_rag vs qwen2.5:14b_baseline | -0.0886 | 1.0490e-01 | ❌ No | [-0.1832, 0.0061] |
| gemma4:31b-mlx_kb_rag vs qwen2.5:14b_kb_rag | -0.0423 | 9.9690e-01 | ❌ No | [-0.1369, 0.0523] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_baseline | -0.1087 | 6.5000e-03 | ✅ Yes | [-0.2033, -0.0141] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.0762 | 3.5090e-01 | ❌ No | [-0.1708, 0.0184] |
| gemma4:latest_baseline vs gemma4:latest_kb_rag | -0.0117 | 1.0000e+00 | ❌ No | [-0.1063, 0.0829] |
| gemma4:latest_baseline vs gemma:latest_baseline | -0.1191 | 1.1000e-03 | ✅ Yes | [-0.2137, -0.0245] |
| gemma4:latest_baseline vs gemma:latest_kb_rag | -0.0455 | 9.9140e-01 | ❌ No | [-0.1401, 0.0491] |
| gemma4:latest_baseline vs gpt-oss:20b_baseline | -0.0352 | 9.9980e-01 | ❌ No | [-0.1298, 0.0594] |
| gemma4:latest_baseline vs gpt-oss:20b_kb_rag | -0.0024 | 1.0000e+00 | ❌ No | [-0.0970, 0.0922] |
| gemma4:latest_baseline vs llama3.1:8b_baseline | -0.0715 | 4.8880e-01 | ❌ No | [-0.1661, 0.0231] |
| gemma4:latest_baseline vs llama3.1:8b_kb_rag | -0.0516 | 9.5860e-01 | ❌ No | [-0.1462, 0.0430] |
| gemma4:latest_baseline vs llama3.2:latest_baseline | -0.1980 | 0.0000e+00 | ✅ Yes | [-0.2926, -0.1034] |
| gemma4:latest_baseline vs llama3.2:latest_kb_rag | -0.0898 | 9.0900e-02 | ❌ No | [-0.1844, 0.0048] |
| gemma4:latest_baseline vs mistral-nemo:latest_baseline | -0.1253 | 3.0000e-04 | ✅ Yes | [-0.2199, -0.0307] |
| gemma4:latest_baseline vs mistral-nemo:latest_kb_rag | -0.1016 | 1.9100e-02 | ✅ Yes | [-0.1962, -0.0070] |
| gemma4:latest_baseline vs nemotron-mini:4b_baseline | -0.3332 | 0.0000e+00 | ✅ Yes | [-0.4278, -0.2386] |
| gemma4:latest_baseline vs nemotron-mini:4b_kb_rag | -0.1880 | 0.0000e+00 | ✅ Yes | [-0.2826, -0.0934] |
| gemma4:latest_baseline vs qwen2.5:14b_baseline | -0.0569 | 8.8930e-01 | ❌ No | [-0.1515, 0.0377] |
| gemma4:latest_baseline vs qwen2.5:14b_kb_rag | -0.0107 | 1.0000e+00 | ❌ No | [-0.1053, 0.0839] |
| gemma4:latest_baseline vs qwen3:8b_baseline | -0.0770 | 3.2720e-01 | ❌ No | [-0.1716, 0.0176] |
| gemma4:latest_baseline vs qwen3:8b_kb_rag | -0.0445 | 9.9350e-01 | ❌ No | [-0.1391, 0.0501] |
| gemma4:latest_kb_rag vs gemma:latest_baseline | -0.1074 | 7.9000e-03 | ✅ Yes | [-0.2020, -0.0128] |
| gemma4:latest_kb_rag vs gemma:latest_kb_rag | -0.0338 | 9.9990e-01 | ❌ No | [-0.1284, 0.0608] |
| gemma4:latest_kb_rag vs gpt-oss:20b_baseline | -0.0235 | 1.0000e+00 | ❌ No | [-0.1181, 0.0711] |
| gemma4:latest_kb_rag vs gpt-oss:20b_kb_rag | 0.0093 | 1.0000e+00 | ❌ No | [-0.0853, 0.1039] |
| gemma4:latest_kb_rag vs llama3.1:8b_baseline | -0.0598 | 8.3050e-01 | ❌ No | [-0.1544, 0.0348] |
| gemma4:latest_kb_rag vs llama3.1:8b_kb_rag | -0.0400 | 9.9870e-01 | ❌ No | [-0.1346, 0.0546] |
| gemma4:latest_kb_rag vs llama3.2:latest_baseline | -0.1863 | 0.0000e+00 | ✅ Yes | [-0.2809, -0.0917] |
| gemma4:latest_kb_rag vs llama3.2:latest_kb_rag | -0.0781 | 2.9970e-01 | ❌ No | [-0.1727, 0.0165] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_baseline | -0.1136 | 2.9000e-03 | ✅ Yes | [-0.2082, -0.0190] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.0899 | 9.0000e-02 | ❌ No | [-0.1845, 0.0047] |
| gemma4:latest_kb_rag vs nemotron-mini:4b_baseline | -0.3215 | 0.0000e+00 | ✅ Yes | [-0.4161, -0.2269] |
| gemma4:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.1763 | 0.0000e+00 | ✅ Yes | [-0.2709, -0.0817] |
| gemma4:latest_kb_rag vs qwen2.5:14b_baseline | -0.0452 | 9.9200e-01 | ❌ No | [-0.1398, 0.0494] |
| gemma4:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0010 | 1.0000e+00 | ❌ No | [-0.0936, 0.0956] |
| gemma4:latest_kb_rag vs qwen3:8b_baseline | -0.0653 | 6.8300e-01 | ❌ No | [-0.1599, 0.0293] |
| gemma4:latest_kb_rag vs qwen3:8b_kb_rag | -0.0328 | 1.0000e+00 | ❌ No | [-0.1274, 0.0618] |
| gemma:latest_baseline vs gemma:latest_kb_rag | 0.0736 | 4.2480e-01 | ❌ No | [-0.0210, 0.1682] |
| gemma:latest_baseline vs gpt-oss:20b_baseline | 0.0839 | 1.7420e-01 | ❌ No | [-0.0107, 0.1785] |
| gemma:latest_baseline vs gpt-oss:20b_kb_rag | 0.1167 | 1.7000e-03 | ✅ Yes | [0.0221, 0.2113] |
| gemma:latest_baseline vs llama3.1:8b_baseline | 0.0476 | 9.8450e-01 | ❌ No | [-0.0470, 0.1422] |
| gemma:latest_baseline vs llama3.1:8b_kb_rag | 0.0675 | 6.1780e-01 | ❌ No | [-0.0271, 0.1621] |
| gemma:latest_baseline vs llama3.2:latest_baseline | -0.0789 | 2.7910e-01 | ❌ No | [-0.1735, 0.0157] |
| gemma:latest_baseline vs llama3.2:latest_kb_rag | 0.0293 | 1.0000e+00 | ❌ No | [-0.0653, 0.1239] |
| gemma:latest_baseline vs mistral-nemo:latest_baseline | -0.0062 | 1.0000e+00 | ❌ No | [-0.1008, 0.0884] |
| gemma:latest_baseline vs mistral-nemo:latest_kb_rag | 0.0175 | 1.0000e+00 | ❌ No | [-0.0771, 0.1121] |
| gemma:latest_baseline vs nemotron-mini:4b_baseline | -0.2141 | 0.0000e+00 | ✅ Yes | [-0.3087, -0.1195] |
| gemma:latest_baseline vs nemotron-mini:4b_kb_rag | -0.0689 | 5.7330e-01 | ❌ No | [-0.1635, 0.0257] |
| gemma:latest_baseline vs qwen2.5:14b_baseline | 0.0622 | 7.7280e-01 | ❌ No | [-0.0324, 0.1568] |
| gemma:latest_baseline vs qwen2.5:14b_kb_rag | 0.1084 | 6.7000e-03 | ✅ Yes | [0.0138, 0.2030] |
| gemma:latest_baseline vs qwen3:8b_baseline | 0.0421 | 9.9720e-01 | ❌ No | [-0.0525, 0.1367] |
| gemma:latest_baseline vs qwen3:8b_kb_rag | 0.0746 | 3.9660e-01 | ❌ No | [-0.0200, 0.1692] |
| gemma:latest_kb_rag vs gpt-oss:20b_baseline | 0.0103 | 1.0000e+00 | ❌ No | [-0.0843, 0.1049] |
| gemma:latest_kb_rag vs gpt-oss:20b_kb_rag | 0.0431 | 9.9600e-01 | ❌ No | [-0.0515, 0.1377] |
| gemma:latest_kb_rag vs llama3.1:8b_baseline | -0.0260 | 1.0000e+00 | ❌ No | [-0.1206, 0.0686] |
| gemma:latest_kb_rag vs llama3.1:8b_kb_rag | -0.0062 | 1.0000e+00 | ❌ No | [-0.1008, 0.0884] |
| gemma:latest_kb_rag vs llama3.2:latest_baseline | -0.1525 | 0.0000e+00 | ✅ Yes | [-0.2471, -0.0579] |
| gemma:latest_kb_rag vs llama3.2:latest_kb_rag | -0.0443 | 9.9400e-01 | ❌ No | [-0.1389, 0.0503] |
| gemma:latest_kb_rag vs mistral-nemo:latest_baseline | -0.0798 | 2.5820e-01 | ❌ No | [-0.1744, 0.0148] |
| gemma:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.0561 | 9.0380e-01 | ❌ No | [-0.1507, 0.0385] |
| gemma:latest_kb_rag vs nemotron-mini:4b_baseline | -0.2877 | 0.0000e+00 | ✅ Yes | [-0.3823, -0.1931] |
| gemma:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.1425 | 0.0000e+00 | ✅ Yes | [-0.2371, -0.0479] |
| gemma:latest_kb_rag vs qwen2.5:14b_baseline | -0.0114 | 1.0000e+00 | ❌ No | [-0.1060, 0.0832] |
| gemma:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0348 | 9.9990e-01 | ❌ No | [-0.0598, 0.1294] |
| gemma:latest_kb_rag vs qwen3:8b_baseline | -0.0315 | 1.0000e+00 | ❌ No | [-0.1261, 0.0631] |
| gemma:latest_kb_rag vs qwen3:8b_kb_rag | 0.0009 | 1.0000e+00 | ❌ No | [-0.0937, 0.0956] |
| gpt-oss:20b_baseline vs gpt-oss:20b_kb_rag | 0.0328 | 1.0000e+00 | ❌ No | [-0.0618, 0.1274] |
| gpt-oss:20b_baseline vs llama3.1:8b_baseline | -0.0363 | 9.9970e-01 | ❌ No | [-0.1309, 0.0583] |
| gpt-oss:20b_baseline vs llama3.1:8b_kb_rag | -0.0164 | 1.0000e+00 | ❌ No | [-0.1110, 0.0782] |
| gpt-oss:20b_baseline vs llama3.2:latest_baseline | -0.1628 | 0.0000e+00 | ✅ Yes | [-0.2574, -0.0682] |
| gpt-oss:20b_baseline vs llama3.2:latest_kb_rag | -0.0546 | 9.2610e-01 | ❌ No | [-0.1492, 0.0400] |
| gpt-oss:20b_baseline vs mistral-nemo:latest_baseline | -0.0901 | 8.7900e-02 | ❌ No | [-0.1847, 0.0045] |
| gpt-oss:20b_baseline vs mistral-nemo:latest_kb_rag | -0.0663 | 6.5220e-01 | ❌ No | [-0.1609, 0.0283] |
| gpt-oss:20b_baseline vs nemotron-mini:4b_baseline | -0.2980 | 0.0000e+00 | ✅ Yes | [-0.3926, -0.2034] |
| gpt-oss:20b_baseline vs nemotron-mini:4b_kb_rag | -0.1527 | 0.0000e+00 | ✅ Yes | [-0.2473, -0.0581] |
| gpt-oss:20b_baseline vs qwen2.5:14b_baseline | -0.0217 | 1.0000e+00 | ❌ No | [-0.1163, 0.0729] |
| gpt-oss:20b_baseline vs qwen2.5:14b_kb_rag | 0.0245 | 1.0000e+00 | ❌ No | [-0.0701, 0.1191] |
| gpt-oss:20b_baseline vs qwen3:8b_baseline | -0.0418 | 9.9740e-01 | ❌ No | [-0.1364, 0.0528] |
| gpt-oss:20b_baseline vs qwen3:8b_kb_rag | -0.0093 | 1.0000e+00 | ❌ No | [-0.1039, 0.0853] |
| gpt-oss:20b_kb_rag vs llama3.1:8b_baseline | -0.0691 | 5.6510e-01 | ❌ No | [-0.1637, 0.0255] |
| gpt-oss:20b_kb_rag vs llama3.1:8b_kb_rag | -0.0492 | 9.7620e-01 | ❌ No | [-0.1438, 0.0454] |
| gpt-oss:20b_kb_rag vs llama3.2:latest_baseline | -0.1956 | 0.0000e+00 | ✅ Yes | [-0.2902, -0.1010] |
| gpt-oss:20b_kb_rag vs llama3.2:latest_kb_rag | -0.0874 | 1.2000e-01 | ❌ No | [-0.1820, 0.0072] |
| gpt-oss:20b_kb_rag vs mistral-nemo:latest_baseline | -0.1229 | 5.0000e-04 | ✅ Yes | [-0.2175, -0.0283] |
| gpt-oss:20b_kb_rag vs mistral-nemo:latest_kb_rag | -0.0992 | 2.7000e-02 | ✅ Yes | [-0.1938, -0.0045] |
| gpt-oss:20b_kb_rag vs nemotron-mini:4b_baseline | -0.3308 | 0.0000e+00 | ✅ Yes | [-0.4254, -0.2362] |
| gpt-oss:20b_kb_rag vs nemotron-mini:4b_kb_rag | -0.1855 | 0.0000e+00 | ✅ Yes | [-0.2801, -0.0909] |
| gpt-oss:20b_kb_rag vs qwen2.5:14b_baseline | -0.0545 | 9.2670e-01 | ❌ No | [-0.1491, 0.0401] |
| gpt-oss:20b_kb_rag vs qwen2.5:14b_kb_rag | -0.0083 | 1.0000e+00 | ❌ No | [-0.1029, 0.0863] |
| gpt-oss:20b_kb_rag vs qwen3:8b_baseline | -0.0746 | 3.9480e-01 | ❌ No | [-0.1692, 0.0200] |
| gpt-oss:20b_kb_rag vs qwen3:8b_kb_rag | -0.0421 | 9.9710e-01 | ❌ No | [-0.1367, 0.0525] |
| llama3.1:8b_baseline vs llama3.1:8b_kb_rag | 0.0199 | 1.0000e+00 | ❌ No | [-0.0747, 0.1145] |
| llama3.1:8b_baseline vs llama3.2:latest_baseline | -0.1265 | 3.0000e-04 | ✅ Yes | [-0.2211, -0.0319] |
| llama3.1:8b_baseline vs llama3.2:latest_kb_rag | -0.0183 | 1.0000e+00 | ❌ No | [-0.1129, 0.0763] |
| llama3.1:8b_baseline vs mistral-nemo:latest_baseline | -0.0538 | 9.3660e-01 | ❌ No | [-0.1484, 0.0408] |
| llama3.1:8b_baseline vs mistral-nemo:latest_kb_rag | -0.0300 | 1.0000e+00 | ❌ No | [-0.1246, 0.0646] |
| llama3.1:8b_baseline vs nemotron-mini:4b_baseline | -0.2617 | 0.0000e+00 | ✅ Yes | [-0.3563, -0.1671] |
| llama3.1:8b_baseline vs nemotron-mini:4b_kb_rag | -0.1164 | 1.7000e-03 | ✅ Yes | [-0.2110, -0.0218] |
| llama3.1:8b_baseline vs qwen2.5:14b_baseline | 0.0146 | 1.0000e+00 | ❌ No | [-0.0800, 0.1092] |
| llama3.1:8b_baseline vs qwen2.5:14b_kb_rag | 0.0608 | 8.0740e-01 | ❌ No | [-0.0338, 0.1554] |
| llama3.1:8b_baseline vs qwen3:8b_baseline | -0.0055 | 1.0000e+00 | ❌ No | [-0.1001, 0.0891] |
| llama3.1:8b_baseline vs qwen3:8b_kb_rag | 0.0270 | 1.0000e+00 | ❌ No | [-0.0676, 0.1216] |
| llama3.1:8b_kb_rag vs llama3.2:latest_baseline | -0.1464 | 0.0000e+00 | ✅ Yes | [-0.2410, -0.0518] |
| llama3.1:8b_kb_rag vs llama3.2:latest_kb_rag | -0.0381 | 9.9940e-01 | ❌ No | [-0.1327, 0.0565] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_baseline | -0.0736 | 4.2410e-01 | ❌ No | [-0.1682, 0.0210] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_kb_rag | -0.0499 | 9.7200e-01 | ❌ No | [-0.1445, 0.0447] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_baseline | -0.2816 | 0.0000e+00 | ✅ Yes | [-0.3762, -0.1870] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_kb_rag | -0.1363 | 0.0000e+00 | ✅ Yes | [-0.2309, -0.0417] |
| llama3.1:8b_kb_rag vs qwen2.5:14b_baseline | -0.0053 | 1.0000e+00 | ❌ No | [-0.0999, 0.0893] |
| llama3.1:8b_kb_rag vs qwen2.5:14b_kb_rag | 0.0409 | 9.9810e-01 | ❌ No | [-0.0537, 0.1355] |
| llama3.1:8b_kb_rag vs qwen3:8b_baseline | -0.0254 | 1.0000e+00 | ❌ No | [-0.1200, 0.0692] |
| llama3.1:8b_kb_rag vs qwen3:8b_kb_rag | 0.0071 | 1.0000e+00 | ❌ No | [-0.0875, 0.1017] |
| llama3.2:latest_baseline vs llama3.2:latest_kb_rag | 0.1082 | 6.9000e-03 | ✅ Yes | [0.0136, 0.2028] |
| llama3.2:latest_baseline vs mistral-nemo:latest_baseline | 0.0727 | 4.5150e-01 | ❌ No | [-0.0219, 0.1673] |
| llama3.2:latest_baseline vs mistral-nemo:latest_kb_rag | 0.0964 | 3.9200e-02 | ✅ Yes | [0.0018, 0.1910] |
| llama3.2:latest_baseline vs nemotron-mini:4b_baseline | -0.1352 | 0.0000e+00 | ✅ Yes | [-0.2298, -0.0406] |
| llama3.2:latest_baseline vs nemotron-mini:4b_kb_rag | 0.0101 | 1.0000e+00 | ❌ No | [-0.0845, 0.1047] |
| llama3.2:latest_baseline vs qwen2.5:14b_baseline | 0.1411 | 0.0000e+00 | ✅ Yes | [0.0465, 0.2357] |
| llama3.2:latest_baseline vs qwen2.5:14b_kb_rag | 0.1873 | 0.0000e+00 | ✅ Yes | [0.0927, 0.2819] |
| llama3.2:latest_baseline vs qwen3:8b_baseline | 0.1210 | 8.0000e-04 | ✅ Yes | [0.0264, 0.2156] |
| llama3.2:latest_baseline vs qwen3:8b_kb_rag | 0.1535 | 0.0000e+00 | ✅ Yes | [0.0589, 0.2481] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_baseline | -0.0355 | 9.9980e-01 | ❌ No | [-0.1301, 0.0591] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.0118 | 1.0000e+00 | ❌ No | [-0.1064, 0.0828] |
| llama3.2:latest_kb_rag vs nemotron-mini:4b_baseline | -0.2434 | 0.0000e+00 | ✅ Yes | [-0.3380, -0.1488] |
| llama3.2:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.0982 | 3.0900e-02 | ✅ Yes | [-0.1928, -0.0036] |
| llama3.2:latest_kb_rag vs qwen2.5:14b_baseline | 0.0329 | 1.0000e+00 | ❌ No | [-0.0618, 0.1275] |
| llama3.2:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0791 | 2.7540e-01 | ❌ No | [-0.0155, 0.1737] |
| llama3.2:latest_kb_rag vs qwen3:8b_baseline | 0.0127 | 1.0000e+00 | ❌ No | [-0.0819, 0.1074] |
| llama3.2:latest_kb_rag vs qwen3:8b_kb_rag | 0.0452 | 9.9200e-01 | ❌ No | [-0.0494, 0.1398] |
| mistral-nemo:latest_baseline vs mistral-nemo:latest_kb_rag | 0.0237 | 1.0000e+00 | ❌ No | [-0.0709, 0.1183] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_baseline | -0.2079 | 0.0000e+00 | ✅ Yes | [-0.3025, -0.1133] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_kb_rag | -0.0627 | 7.5920e-01 | ❌ No | [-0.1573, 0.0319] |
| mistral-nemo:latest_baseline vs qwen2.5:14b_baseline | 0.0683 | 5.8950e-01 | ❌ No | [-0.0263, 0.1629] |
| mistral-nemo:latest_baseline vs qwen2.5:14b_kb_rag | 0.1146 | 2.4000e-03 | ✅ Yes | [0.0200, 0.2092] |
| mistral-nemo:latest_baseline vs qwen3:8b_baseline | 0.0482 | 9.8140e-01 | ❌ No | [-0.0464, 0.1428] |
| mistral-nemo:latest_baseline vs qwen3:8b_kb_rag | 0.0807 | 2.3670e-01 | ❌ No | [-0.0139, 0.1753] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_baseline | -0.2316 | 0.0000e+00 | ✅ Yes | [-0.3262, -0.1370] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.0864 | 1.3360e-01 | ❌ No | [-0.1810, 0.0082] |
| mistral-nemo:latest_kb_rag vs qwen2.5:14b_baseline | 0.0446 | 9.9330e-01 | ❌ No | [-0.0500, 0.1392] |
| mistral-nemo:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0908 | 8.0100e-02 | ❌ No | [-0.0038, 0.1854] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_baseline | 0.0245 | 1.0000e+00 | ❌ No | [-0.0701, 0.1191] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_kb_rag | 0.0570 | 8.8760e-01 | ❌ No | [-0.0376, 0.1516] |
| nemotron-mini:4b_baseline vs nemotron-mini:4b_kb_rag | 0.1452 | 0.0000e+00 | ✅ Yes | [0.0506, 0.2398] |
| nemotron-mini:4b_baseline vs qwen2.5:14b_baseline | 0.2763 | 0.0000e+00 | ✅ Yes | [0.1817, 0.3709] |
| nemotron-mini:4b_baseline vs qwen2.5:14b_kb_rag | 0.3225 | 0.0000e+00 | ✅ Yes | [0.2279, 0.4171] |
| nemotron-mini:4b_baseline vs qwen3:8b_baseline | 0.2562 | 0.0000e+00 | ✅ Yes | [0.1616, 0.3508] |
| nemotron-mini:4b_baseline vs qwen3:8b_kb_rag | 0.2887 | 0.0000e+00 | ✅ Yes | [0.1941, 0.3833] |
| nemotron-mini:4b_kb_rag vs qwen2.5:14b_baseline | 0.1310 | 1.0000e-04 | ✅ Yes | [0.0364, 0.2256] |
| nemotron-mini:4b_kb_rag vs qwen2.5:14b_kb_rag | 0.1772 | 0.0000e+00 | ✅ Yes | [0.0826, 0.2718] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_baseline | 0.1109 | 4.5000e-03 | ✅ Yes | [0.0163, 0.2055] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_kb_rag | 0.1434 | 0.0000e+00 | ✅ Yes | [0.0488, 0.2380] |
| qwen2.5:14b_baseline vs qwen2.5:14b_kb_rag | 0.0462 | 9.8930e-01 | ❌ No | [-0.0484, 0.1408] |
| qwen2.5:14b_baseline vs qwen3:8b_baseline | -0.0201 | 1.0000e+00 | ❌ No | [-0.1147, 0.0745] |
| qwen2.5:14b_baseline vs qwen3:8b_kb_rag | 0.0124 | 1.0000e+00 | ❌ No | [-0.0822, 0.1070] |
| qwen2.5:14b_kb_rag vs qwen3:8b_baseline | -0.0663 | 6.5320e-01 | ❌ No | [-0.1609, 0.0283] |
| qwen2.5:14b_kb_rag vs qwen3:8b_kb_rag | -0.0338 | 9.9990e-01 | ❌ No | [-0.1284, 0.0608] |
| qwen3:8b_baseline vs qwen3:8b_kb_rag | 0.0325 | 1.0000e+00 | ❌ No | [-0.0621, 0.1271] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 2610.3 characters.
- **Outlier Records Identified:** 14 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| deepseek-r1:1.5b_baseline | 0.2483 | 0.2490 | +0.0007 | 📈 Improved |
| deepseek-r1:1.5b_kb_rag | 0.2394 | 0.2277 | -0.0117 | 📉 Decreased |
| gemma4:12b-mlx_baseline | 0.5618 | 0.5515 | -0.0103 | 📉 Decreased |
| gemma4:12b-mlx_kb_rag | 0.5846 | 0.5684 | -0.0161 | 📉 Decreased |
| gemma4:31b-cloud_baseline | 0.6238 | 0.6165 | -0.0073 | 📉 Decreased |
| gemma4:31b-cloud_kb_rag | 0.6185 | 0.6065 | -0.0120 | 📉 Decreased |
| gemma4:31b-mlx_baseline | 0.5925 | 0.5813 | -0.0112 | 📉 Decreased |
| gemma4:31b-mlx_kb_rag | 0.5907 | 0.5836 | -0.0072 | 📉 Decreased |
| gemma4:latest_baseline | 0.5591 | 0.5434 | -0.0157 | 📉 Decreased |
| gemma4:latest_kb_rag | 0.5474 | 0.5370 | -0.0104 | 📉 Decreased |
| gemma:latest_baseline | 0.4400 | 0.4216 | -0.0185 | 📉 Decreased |
| gemma:latest_kb_rag | 0.5136 | 0.4945 | -0.0191 | 📉 Decreased |
| gpt-oss:20b_baseline | 0.5239 | 0.5169 | -0.0070 | 📉 Decreased |
| gpt-oss:20b_kb_rag | 0.5567 | 0.5417 | -0.0150 | 📉 Decreased |
| llama3.1:8b_baseline | 0.4876 | 0.4777 | -0.0099 | 📉 Decreased |
| llama3.1:8b_kb_rag | 0.5075 | 0.4903 | -0.0171 | 📉 Decreased |
| llama3.2:latest_baseline | 0.3611 | 0.3340 | -0.0271 | 📉 Decreased |
| llama3.2:latest_kb_rag | 0.4693 | 0.4549 | -0.0144 | 📉 Decreased |
| mistral-nemo:latest_baseline | 0.4338 | 0.4160 | -0.0178 | 📉 Decreased |
| mistral-nemo:latest_kb_rag | 0.4576 | 0.4422 | -0.0153 | 📉 Decreased |
| nemotron-mini:4b_baseline | 0.2259 | 0.2129 | -0.0131 | 📉 Decreased |
| nemotron-mini:4b_kb_rag | 0.3712 | 0.3598 | -0.0114 | 📉 Decreased |
| qwen2.5:14b_baseline | 0.5022 | 0.4873 | -0.0149 | 📉 Decreased |
| qwen2.5:14b_kb_rag | 0.5484 | 0.5315 | -0.0169 | 📉 Decreased |
| qwen3:8b_baseline | 0.4821 | 0.4669 | -0.0152 | 📉 Decreased |
| qwen3:8b_kb_rag | 0.5146 | 0.5006 | -0.0140 | 📉 Decreased |
