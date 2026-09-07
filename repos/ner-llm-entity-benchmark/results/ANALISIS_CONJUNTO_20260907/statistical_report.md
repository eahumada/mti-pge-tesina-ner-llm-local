# 🔗 Merged Benchmark Analysis — Provenance & Integrity

- **Corpus:** `data/benchmark_balanced_120.json`
- **Registros esperados por modelo+modo:** 120
- **Corridas combinadas:** 7
- **Grupos (modelo+modo) analizados:** 26
- **Filas totales tras el merge:** 3120

## Fuentes
| # | Corrida | CSV | Filas | Modelos aportados |
| :---: | :--- | :--- | :---: | :---: |
| 1 | 01_qwen3_nothink | `/private/tmp/claude-501/-Users-eahumada-Documents-Personal-MTI-mti-pge-tesina-ner-llm-local/87e8505b-1ba9-4f7a-8204-01d63aa41522/scratchpad/anova_stage/01_qwen3_nothink/benchmark_results.csv` | 240 | 2 |
| 2 | 02_gemma4_12b_mlx | `/private/tmp/claude-501/-Users-eahumada-Documents-Personal-MTI-mti-pge-tesina-ner-llm-local/87e8505b-1ba9-4f7a-8204-01d63aa41522/scratchpad/anova_stage/02_gemma4_12b_mlx/benchmark_results.csv` | 240 | 2 |
| 3 | 03_nemotron_rerun | `/private/tmp/claude-501/-Users-eahumada-Documents-Personal-MTI-mti-pge-tesina-ner-llm-local/87e8505b-1ba9-4f7a-8204-01d63aa41522/scratchpad/anova_stage/03_nemotron_rerun/benchmark_results.csv` | 240 | 2 |
| 4 | 04_cloud | `/private/tmp/claude-501/-Users-eahumada-Documents-Personal-MTI-mti-pge-tesina-ner-llm-local/87e8505b-1ba9-4f7a-8204-01d63aa41522/scratchpad/anova_stage/04_cloud/benchmark_results.csv` | 240 | 2 |
| 5 | 05_excluidos | `/private/tmp/claude-501/-Users-eahumada-Documents-Personal-MTI-mti-pge-tesina-ner-llm-local/87e8505b-1ba9-4f7a-8204-01d63aa41522/scratchpad/anova_stage/05_excluidos/benchmark_results.csv` | 240 | 2 |
| 6 | 06_P3 | `/private/tmp/claude-501/-Users-eahumada-Documents-Personal-MTI-mti-pge-tesina-ner-llm-local/87e8505b-1ba9-4f7a-8204-01d63aa41522/scratchpad/anova_stage/06_P3/benchmark_results.csv` | 1440 | 12 |
| 7 | 07_legacy_kbrag | `/private/tmp/claude-501/-Users-eahumada-Documents-Personal-MTI-mti-pge-tesina-ner-llm-local/87e8505b-1ba9-4f7a-8204-01d63aa41522/scratchpad/anova_stage/07_legacy_kbrag/benchmark_results.csv` | 1200 | 10 |

## Integridad por grupo (modelo + modo)
| Modelo | Filas | record_id unicos | Esperados | f1 NaN | Estado |
| :--- | :---: | :---: | :---: | :---: | :---: |
| qwen3:8b_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| qwen3:8b_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
| gemma4:12b-mlx_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| gemma4:12b-mlx_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
| nemotron-mini:4b_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| nemotron-mini:4b_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
| gemma4:31b-cloud_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| gemma4:31b-cloud_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
| gpt-oss:20b_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| gpt-oss:20b_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
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
- ⚠️ DUPLICADO: 'gemma4:12b-mlx_baseline' aparece en '02_gemma4_12b_mlx' y en '06_P3'. Se conservan las filas de '02_gemma4_12b_mlx' (--on-duplicate=first).
- ⚠️ DUPLICADO: 'gemma4:12b-mlx_kb_rag' aparece en '02_gemma4_12b_mlx' y en '06_P3'. Se conservan las filas de '02_gemma4_12b_mlx' (--on-duplicate=first).
- ⚠️ DUPLICADO: 'qwen3:8b_baseline' aparece en '01_qwen3_nothink' y en '06_P3'. Se conservan las filas de '01_qwen3_nothink' (--on-duplicate=first).
- ⚠️ DUPLICADO: 'qwen3:8b_kb_rag' aparece en '01_qwen3_nothink' y en '06_P3'. Se conservan las filas de '01_qwen3_nothink' (--on-duplicate=first).
- ⚠️ DUPLICADO: 'nemotron-mini:4b_baseline' aparece en '03_nemotron_rerun' y en '06_P3'. Se conservan las filas de '03_nemotron_rerun' (--on-duplicate=first).
- ⚠️ DUPLICADO: 'nemotron-mini:4b_kb_rag' aparece en '03_nemotron_rerun' y en '06_P3'. Se conservan las filas de '03_nemotron_rerun' (--on-duplicate=first).

---
# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 36.3666
- **p-Value:** 1.2236e-152

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| qwen3:8b_baseline | 120 | 0.4821 | 0.4495 | 0.5147 | 0.1802 |
| qwen3:8b_kb_rag | 120 | 0.5146 | 0.4791 | 0.5501 | 0.1963 |
| gemma4:12b-mlx_baseline | 120 | 0.5618 | 0.5296 | 0.5940 | 0.1783 |
| gemma4:12b-mlx_kb_rag | 120 | 0.5846 | 0.5493 | 0.6199 | 0.1953 |
| nemotron-mini:4b_baseline | 120 | 0.2259 | 0.1936 | 0.2582 | 0.1787 |
| nemotron-mini:4b_kb_rag | 120 | 0.3712 | 0.3321 | 0.4102 | 0.2161 |
| gemma4:31b-cloud_baseline | 120 | 0.6238 | 0.5895 | 0.6582 | 0.1902 |
| gemma4:31b-cloud_kb_rag | 120 | 0.6185 | 0.5845 | 0.6525 | 0.1881 |
| gpt-oss:20b_baseline | 120 | 0.4384 | 0.3900 | 0.4868 | 0.2677 |
| gpt-oss:20b_kb_rag | 120 | 0.3419 | 0.2862 | 0.3976 | 0.3082 |
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
| deepseek-r1:1.5b_baseline vs deepseek-r1:1.5b_kb_rag | -0.0090 | 1.0000e+00 | ❌ No | [-0.1077, 0.0898] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_baseline | 0.3135 | 0.0000e+00 | ✅ Yes | [0.2148, 0.4122] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_kb_rag | 0.3363 | 0.0000e+00 | ✅ Yes | [0.2375, 0.4350] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_baseline | 0.3755 | 0.0000e+00 | ✅ Yes | [0.2768, 0.4742] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_kb_rag | 0.3701 | 0.0000e+00 | ✅ Yes | [0.2714, 0.4689] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_baseline | 0.3442 | 0.0000e+00 | ✅ Yes | [0.2455, 0.4429] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_kb_rag | 0.3424 | 0.0000e+00 | ✅ Yes | [0.2437, 0.4411] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_baseline | 0.3108 | 0.0000e+00 | ✅ Yes | [0.2121, 0.4095] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_kb_rag | 0.2991 | 0.0000e+00 | ✅ Yes | [0.2004, 0.3978] |
| deepseek-r1:1.5b_baseline vs gemma:latest_baseline | 0.1917 | 0.0000e+00 | ✅ Yes | [0.0930, 0.2904] |
| deepseek-r1:1.5b_baseline vs gemma:latest_kb_rag | 0.2653 | 0.0000e+00 | ✅ Yes | [0.1666, 0.3640] |
| deepseek-r1:1.5b_baseline vs gpt-oss:20b_baseline | 0.1900 | 0.0000e+00 | ✅ Yes | [0.0913, 0.2888] |
| deepseek-r1:1.5b_baseline vs gpt-oss:20b_kb_rag | 0.0935 | 9.2600e-02 | ❌ No | [-0.0052, 0.1923] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_baseline | 0.2393 | 0.0000e+00 | ✅ Yes | [0.1405, 0.3380] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_kb_rag | 0.2591 | 0.0000e+00 | ✅ Yes | [0.1604, 0.3579] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_baseline | 0.1128 | 7.1000e-03 | ✅ Yes | [0.0141, 0.2115] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_kb_rag | 0.2210 | 0.0000e+00 | ✅ Yes | [0.1223, 0.3197] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_baseline | 0.1855 | 0.0000e+00 | ✅ Yes | [0.0868, 0.2842] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_kb_rag | 0.2092 | 0.0000e+00 | ✅ Yes | [0.1105, 0.3080] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_baseline | -0.0224 | 1.0000e+00 | ❌ No | [-0.1211, 0.0763] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_kb_rag | 0.1228 | 1.4000e-03 | ✅ Yes | [0.0241, 0.2216] |
| deepseek-r1:1.5b_baseline vs qwen2.5:14b_baseline | 0.2539 | 0.0000e+00 | ✅ Yes | [0.1551, 0.3526] |
| deepseek-r1:1.5b_baseline vs qwen2.5:14b_kb_rag | 0.3001 | 0.0000e+00 | ✅ Yes | [0.2014, 0.3988] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_baseline | 0.2338 | 0.0000e+00 | ✅ Yes | [0.1350, 0.3325] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_kb_rag | 0.2663 | 0.0000e+00 | ✅ Yes | [0.1675, 0.3650] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_baseline | 0.3225 | 0.0000e+00 | ✅ Yes | [0.2237, 0.4212] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_kb_rag | 0.3452 | 0.0000e+00 | ✅ Yes | [0.2465, 0.4439] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-cloud_baseline | 0.3845 | 0.0000e+00 | ✅ Yes | [0.2857, 0.4832] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-cloud_kb_rag | 0.3791 | 0.0000e+00 | ✅ Yes | [0.2804, 0.4778] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-mlx_baseline | 0.3532 | 0.0000e+00 | ✅ Yes | [0.2545, 0.4519] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-mlx_kb_rag | 0.3514 | 0.0000e+00 | ✅ Yes | [0.2527, 0.4501] |
| deepseek-r1:1.5b_kb_rag vs gemma4:latest_baseline | 0.3198 | 0.0000e+00 | ✅ Yes | [0.2210, 0.4185] |
| deepseek-r1:1.5b_kb_rag vs gemma4:latest_kb_rag | 0.3081 | 0.0000e+00 | ✅ Yes | [0.2093, 0.4068] |
| deepseek-r1:1.5b_kb_rag vs gemma:latest_baseline | 0.2007 | 0.0000e+00 | ✅ Yes | [0.1019, 0.2994] |
| deepseek-r1:1.5b_kb_rag vs gemma:latest_kb_rag | 0.2743 | 0.0000e+00 | ✅ Yes | [0.1755, 0.3730] |
| deepseek-r1:1.5b_kb_rag vs gpt-oss:20b_baseline | 0.1990 | 0.0000e+00 | ✅ Yes | [0.1003, 0.2977] |
| deepseek-r1:1.5b_kb_rag vs gpt-oss:20b_kb_rag | 0.1025 | 3.0700e-02 | ✅ Yes | [0.0038, 0.2012] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_baseline | 0.2482 | 0.0000e+00 | ✅ Yes | [0.1495, 0.3470] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_kb_rag | 0.2681 | 0.0000e+00 | ✅ Yes | [0.1694, 0.3668] |
| deepseek-r1:1.5b_kb_rag vs llama3.2:latest_baseline | 0.1217 | 1.7000e-03 | ✅ Yes | [0.0230, 0.2205] |
| deepseek-r1:1.5b_kb_rag vs llama3.2:latest_kb_rag | 0.2300 | 0.0000e+00 | ✅ Yes | [0.1313, 0.3287] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_baseline | 0.1945 | 0.0000e+00 | ✅ Yes | [0.0958, 0.2932] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_kb_rag | 0.2182 | 0.0000e+00 | ✅ Yes | [0.1195, 0.3169] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_baseline | -0.0134 | 1.0000e+00 | ❌ No | [-0.1122, 0.0853] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_kb_rag | 0.1318 | 3.0000e-04 | ✅ Yes | [0.0331, 0.2305] |
| deepseek-r1:1.5b_kb_rag vs qwen2.5:14b_baseline | 0.2628 | 0.0000e+00 | ✅ Yes | [0.1641, 0.3616] |
| deepseek-r1:1.5b_kb_rag vs qwen2.5:14b_kb_rag | 0.3090 | 0.0000e+00 | ✅ Yes | [0.2103, 0.4078] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_baseline | 0.2427 | 0.0000e+00 | ✅ Yes | [0.1440, 0.3415] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_kb_rag | 0.2752 | 0.0000e+00 | ✅ Yes | [0.1765, 0.3739] |
| gemma4:12b-mlx_baseline vs gemma4:12b-mlx_kb_rag | 0.0228 | 1.0000e+00 | ❌ No | [-0.0760, 0.1215] |
| gemma4:12b-mlx_baseline vs gemma4:31b-cloud_baseline | 0.0620 | 8.3960e-01 | ❌ No | [-0.0367, 0.1607] |
| gemma4:12b-mlx_baseline vs gemma4:31b-cloud_kb_rag | 0.0566 | 9.2990e-01 | ❌ No | [-0.0421, 0.1554] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_baseline | 0.0307 | 1.0000e+00 | ❌ No | [-0.0680, 0.1294] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_kb_rag | 0.0289 | 1.0000e+00 | ❌ No | [-0.0698, 0.1276] |
| gemma4:12b-mlx_baseline vs gemma4:latest_baseline | -0.0027 | 1.0000e+00 | ❌ No | [-0.1014, 0.0960] |
| gemma4:12b-mlx_baseline vs gemma4:latest_kb_rag | -0.0144 | 1.0000e+00 | ❌ No | [-0.1131, 0.0843] |
| gemma4:12b-mlx_baseline vs gemma:latest_baseline | -0.1218 | 1.7000e-03 | ✅ Yes | [-0.2205, -0.0231] |
| gemma4:12b-mlx_baseline vs gemma:latest_kb_rag | -0.0482 | 9.8940e-01 | ❌ No | [-0.1469, 0.0505] |
| gemma4:12b-mlx_baseline vs gpt-oss:20b_baseline | -0.1234 | 1.3000e-03 | ✅ Yes | [-0.2222, -0.0247] |
| gemma4:12b-mlx_baseline vs gpt-oss:20b_kb_rag | -0.2200 | 0.0000e+00 | ✅ Yes | [-0.3187, -0.1212] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_baseline | -0.0742 | 5.0150e-01 | ❌ No | [-0.1729, 0.0245] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_kb_rag | -0.0543 | 9.5470e-01 | ❌ No | [-0.1531, 0.0444] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_baseline | -0.2007 | 0.0000e+00 | ✅ Yes | [-0.2994, -0.1020] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_kb_rag | -0.0925 | 1.0420e-01 | ❌ No | [-0.1912, 0.0062] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_baseline | -0.1280 | 6.0000e-04 | ✅ Yes | [-0.2267, -0.0293] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.1043 | 2.4300e-02 | ✅ Yes | [-0.2030, -0.0055] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_baseline | -0.3359 | 0.0000e+00 | ✅ Yes | [-0.4346, -0.2372] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_kb_rag | -0.1907 | 0.0000e+00 | ✅ Yes | [-0.2894, -0.0919] |
| gemma4:12b-mlx_baseline vs qwen2.5:14b_baseline | -0.0596 | 8.8560e-01 | ❌ No | [-0.1584, 0.0391] |
| gemma4:12b-mlx_baseline vs qwen2.5:14b_kb_rag | -0.0134 | 1.0000e+00 | ❌ No | [-0.1121, 0.0853] |
| gemma4:12b-mlx_baseline vs qwen3:8b_baseline | -0.0797 | 3.4440e-01 | ❌ No | [-0.1785, 0.0190] |
| gemma4:12b-mlx_baseline vs qwen3:8b_kb_rag | -0.0472 | 9.9190e-01 | ❌ No | [-0.1460, 0.0515] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-cloud_baseline | 0.0392 | 9.9950e-01 | ❌ No | [-0.0595, 0.1380] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-cloud_kb_rag | 0.0339 | 1.0000e+00 | ❌ No | [-0.0648, 0.1326] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_baseline | 0.0080 | 1.0000e+00 | ❌ No | [-0.0908, 0.1067] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_kb_rag | 0.0062 | 1.0000e+00 | ❌ No | [-0.0926, 0.1049] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_baseline | -0.0255 | 1.0000e+00 | ❌ No | [-0.1242, 0.0733] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0372 | 9.9980e-01 | ❌ No | [-0.1359, 0.0616] |
| gemma4:12b-mlx_kb_rag vs gemma:latest_baseline | -0.1446 | 0.0000e+00 | ✅ Yes | [-0.2433, -0.0458] |
| gemma4:12b-mlx_kb_rag vs gemma:latest_kb_rag | -0.0710 | 6.0070e-01 | ❌ No | [-0.1697, 0.0278] |
| gemma4:12b-mlx_kb_rag vs gpt-oss:20b_baseline | -0.1462 | 0.0000e+00 | ✅ Yes | [-0.2449, -0.0475] |
| gemma4:12b-mlx_kb_rag vs gpt-oss:20b_kb_rag | -0.2427 | 0.0000e+00 | ✅ Yes | [-0.3414, -0.1440] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_baseline | -0.0970 | 6.1800e-02 | ❌ No | [-0.1957, 0.0017] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_kb_rag | -0.0771 | 4.1620e-01 | ❌ No | [-0.1758, 0.0216] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_baseline | -0.2235 | 0.0000e+00 | ✅ Yes | [-0.3222, -0.1248] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.1152 | 4.8000e-03 | ✅ Yes | [-0.2140, -0.0165] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.1507 | 0.0000e+00 | ✅ Yes | [-0.2495, -0.0520] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.1270 | 7.0000e-04 | ✅ Yes | [-0.2258, -0.0283] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_baseline | -0.3587 | 0.0000e+00 | ✅ Yes | [-0.4574, -0.2600] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | -0.2134 | 0.0000e+00 | ✅ Yes | [-0.3121, -0.1147] |
| gemma4:12b-mlx_kb_rag vs qwen2.5:14b_baseline | -0.0824 | 2.7800e-01 | ❌ No | [-0.1811, 0.0163] |
| gemma4:12b-mlx_kb_rag vs qwen2.5:14b_kb_rag | -0.0362 | 9.9990e-01 | ❌ No | [-0.1349, 0.0625] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_baseline | -0.1025 | 3.0800e-02 | ✅ Yes | [-0.2012, -0.0038] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.0700 | 6.2930e-01 | ❌ No | [-0.1687, 0.0287] |
| gemma4:31b-cloud_baseline vs gemma4:31b-cloud_kb_rag | -0.0054 | 1.0000e+00 | ❌ No | [-0.1041, 0.0934] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_baseline | -0.0313 | 1.0000e+00 | ❌ No | [-0.1300, 0.0674] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_kb_rag | -0.0331 | 1.0000e+00 | ❌ No | [-0.1318, 0.0656] |
| gemma4:31b-cloud_baseline vs gemma4:latest_baseline | -0.0647 | 7.7700e-01 | ❌ No | [-0.1634, 0.0340] |
| gemma4:31b-cloud_baseline vs gemma4:latest_kb_rag | -0.0764 | 4.3660e-01 | ❌ No | [-0.1751, 0.0223] |
| gemma4:31b-cloud_baseline vs gemma:latest_baseline | -0.1838 | 0.0000e+00 | ✅ Yes | [-0.2825, -0.0851] |
| gemma4:31b-cloud_baseline vs gemma:latest_kb_rag | -0.1102 | 1.0400e-02 | ✅ Yes | [-0.2089, -0.0115] |
| gemma4:31b-cloud_baseline vs gpt-oss:20b_baseline | -0.1855 | 0.0000e+00 | ✅ Yes | [-0.2842, -0.0867] |
| gemma4:31b-cloud_baseline vs gpt-oss:20b_kb_rag | -0.2820 | 0.0000e+00 | ✅ Yes | [-0.3807, -0.1832] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_baseline | -0.1362 | 1.0000e-04 | ✅ Yes | [-0.2350, -0.0375] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_kb_rag | -0.1164 | 4.0000e-03 | ✅ Yes | [-0.2151, -0.0176] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_baseline | -0.2627 | 0.0000e+00 | ✅ Yes | [-0.3614, -0.1640] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_kb_rag | -0.1545 | 0.0000e+00 | ✅ Yes | [-0.2532, -0.0558] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_baseline | -0.1900 | 0.0000e+00 | ✅ Yes | [-0.2887, -0.0913] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_kb_rag | -0.1663 | 0.0000e+00 | ✅ Yes | [-0.2650, -0.0676] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_baseline | -0.3979 | 0.0000e+00 | ✅ Yes | [-0.4966, -0.2992] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_kb_rag | -0.2527 | 0.0000e+00 | ✅ Yes | [-0.3514, -0.1539] |
| gemma4:31b-cloud_baseline vs qwen2.5:14b_baseline | -0.1216 | 1.7000e-03 | ✅ Yes | [-0.2204, -0.0229] |
| gemma4:31b-cloud_baseline vs qwen2.5:14b_kb_rag | -0.0754 | 4.6540e-01 | ❌ No | [-0.1742, 0.0233] |
| gemma4:31b-cloud_baseline vs qwen3:8b_baseline | -0.1417 | 0.0000e+00 | ✅ Yes | [-0.2405, -0.0430] |
| gemma4:31b-cloud_baseline vs qwen3:8b_kb_rag | -0.1093 | 1.2000e-02 | ✅ Yes | [-0.2080, -0.0105] |
| gemma4:31b-cloud_kb_rag vs gemma4:31b-mlx_baseline | -0.0259 | 1.0000e+00 | ❌ No | [-0.1246, 0.0728] |
| gemma4:31b-cloud_kb_rag vs gemma4:31b-mlx_kb_rag | -0.0277 | 1.0000e+00 | ❌ No | [-0.1264, 0.0710] |
| gemma4:31b-cloud_kb_rag vs gemma4:latest_baseline | -0.0593 | 8.9050e-01 | ❌ No | [-0.1581, 0.0394] |
| gemma4:31b-cloud_kb_rag vs gemma4:latest_kb_rag | -0.0710 | 5.9820e-01 | ❌ No | [-0.1698, 0.0277] |
| gemma4:31b-cloud_kb_rag vs gemma:latest_baseline | -0.1784 | 0.0000e+00 | ✅ Yes | [-0.2772, -0.0797] |
| gemma4:31b-cloud_kb_rag vs gemma:latest_kb_rag | -0.1048 | 2.2400e-02 | ✅ Yes | [-0.2036, -0.0061] |
| gemma4:31b-cloud_kb_rag vs gpt-oss:20b_baseline | -0.1801 | 0.0000e+00 | ✅ Yes | [-0.2788, -0.0814] |
| gemma4:31b-cloud_kb_rag vs gpt-oss:20b_kb_rag | -0.2766 | 0.0000e+00 | ✅ Yes | [-0.3753, -0.1779] |
| gemma4:31b-cloud_kb_rag vs llama3.1:8b_baseline | -0.1309 | 3.0000e-04 | ✅ Yes | [-0.2296, -0.0321] |
| gemma4:31b-cloud_kb_rag vs llama3.1:8b_kb_rag | -0.1110 | 9.3000e-03 | ✅ Yes | [-0.2097, -0.0123] |
| gemma4:31b-cloud_kb_rag vs llama3.2:latest_baseline | -0.2574 | 0.0000e+00 | ✅ Yes | [-0.3561, -0.1586] |
| gemma4:31b-cloud_kb_rag vs llama3.2:latest_kb_rag | -0.1491 | 0.0000e+00 | ✅ Yes | [-0.2478, -0.0504] |
| gemma4:31b-cloud_kb_rag vs mistral-nemo:latest_baseline | -0.1846 | 0.0000e+00 | ✅ Yes | [-0.2833, -0.0859] |
| gemma4:31b-cloud_kb_rag vs mistral-nemo:latest_kb_rag | -0.1609 | 0.0000e+00 | ✅ Yes | [-0.2596, -0.0622] |
| gemma4:31b-cloud_kb_rag vs nemotron-mini:4b_baseline | -0.3925 | 0.0000e+00 | ✅ Yes | [-0.4913, -0.2938] |
| gemma4:31b-cloud_kb_rag vs nemotron-mini:4b_kb_rag | -0.2473 | 0.0000e+00 | ✅ Yes | [-0.3460, -0.1486] |
| gemma4:31b-cloud_kb_rag vs qwen2.5:14b_baseline | -0.1163 | 4.1000e-03 | ✅ Yes | [-0.2150, -0.0175] |
| gemma4:31b-cloud_kb_rag vs qwen2.5:14b_kb_rag | -0.0701 | 6.2770e-01 | ❌ No | [-0.1688, 0.0287] |
| gemma4:31b-cloud_kb_rag vs qwen3:8b_baseline | -0.1364 | 1.0000e-04 | ✅ Yes | [-0.2351, -0.0376] |
| gemma4:31b-cloud_kb_rag vs qwen3:8b_kb_rag | -0.1039 | 2.5600e-02 | ✅ Yes | [-0.2026, -0.0052] |
| gemma4:31b-mlx_baseline vs gemma4:31b-mlx_kb_rag | -0.0018 | 1.0000e+00 | ❌ No | [-0.1005, 0.0969] |
| gemma4:31b-mlx_baseline vs gemma4:latest_baseline | -0.0334 | 1.0000e+00 | ❌ No | [-0.1321, 0.0653] |
| gemma4:31b-mlx_baseline vs gemma4:latest_kb_rag | -0.0451 | 9.9580e-01 | ❌ No | [-0.1438, 0.0536] |
| gemma4:31b-mlx_baseline vs gemma:latest_baseline | -0.1525 | 0.0000e+00 | ✅ Yes | [-0.2512, -0.0538] |
| gemma4:31b-mlx_baseline vs gemma:latest_kb_rag | -0.0789 | 3.6620e-01 | ❌ No | [-0.1776, 0.0198] |
| gemma4:31b-mlx_baseline vs gpt-oss:20b_baseline | -0.1542 | 0.0000e+00 | ✅ Yes | [-0.2529, -0.0554] |
| gemma4:31b-mlx_baseline vs gpt-oss:20b_kb_rag | -0.2507 | 0.0000e+00 | ✅ Yes | [-0.3494, -0.1520] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_baseline | -0.1049 | 2.2100e-02 | ✅ Yes | [-0.2037, -0.0062] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_kb_rag | -0.0851 | 2.2000e-01 | ❌ No | [-0.1838, 0.0137] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_baseline | -0.2314 | 0.0000e+00 | ✅ Yes | [-0.3302, -0.1327] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_kb_rag | -0.1232 | 1.3000e-03 | ✅ Yes | [-0.2219, -0.0245] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_baseline | -0.1587 | 0.0000e+00 | ✅ Yes | [-0.2574, -0.0600] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.1350 | 2.0000e-04 | ✅ Yes | [-0.2337, -0.0363] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_baseline | -0.3666 | 0.0000e+00 | ✅ Yes | [-0.4654, -0.2679] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_kb_rag | -0.2214 | 0.0000e+00 | ✅ Yes | [-0.3201, -0.1227] |
| gemma4:31b-mlx_baseline vs qwen2.5:14b_baseline | -0.0904 | 1.3090e-01 | ❌ No | [-0.1891, 0.0084] |
| gemma4:31b-mlx_baseline vs qwen2.5:14b_kb_rag | -0.0441 | 9.9690e-01 | ❌ No | [-0.1429, 0.0546] |
| gemma4:31b-mlx_baseline vs qwen3:8b_baseline | -0.1105 | 1.0000e-02 | ✅ Yes | [-0.2092, -0.0117] |
| gemma4:31b-mlx_baseline vs qwen3:8b_kb_rag | -0.0780 | 3.9230e-01 | ❌ No | [-0.1767, 0.0208] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_baseline | -0.0316 | 1.0000e+00 | ❌ No | [-0.1303, 0.0671] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0433 | 9.9770e-01 | ❌ No | [-0.1420, 0.0554] |
| gemma4:31b-mlx_kb_rag vs gemma:latest_baseline | -0.1507 | 0.0000e+00 | ✅ Yes | [-0.2494, -0.0520] |
| gemma4:31b-mlx_kb_rag vs gemma:latest_kb_rag | -0.0771 | 4.1640e-01 | ❌ No | [-0.1758, 0.0216] |
| gemma4:31b-mlx_kb_rag vs gpt-oss:20b_baseline | -0.1524 | 0.0000e+00 | ✅ Yes | [-0.2511, -0.0536] |
| gemma4:31b-mlx_kb_rag vs gpt-oss:20b_kb_rag | -0.2489 | 0.0000e+00 | ✅ Yes | [-0.3476, -0.1502] |
| gemma4:31b-mlx_kb_rag vs llama3.1:8b_baseline | -0.1031 | 2.8200e-02 | ✅ Yes | [-0.2019, -0.0044] |
| gemma4:31b-mlx_kb_rag vs llama3.1:8b_kb_rag | -0.0833 | 2.5810e-01 | ❌ No | [-0.1820, 0.0155] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_baseline | -0.2296 | 0.0000e+00 | ✅ Yes | [-0.3284, -0.1309] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.1214 | 1.8000e-03 | ✅ Yes | [-0.2201, -0.0227] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.1569 | 0.0000e+00 | ✅ Yes | [-0.2556, -0.0582] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.1332 | 2.0000e-04 | ✅ Yes | [-0.2319, -0.0345] |
| gemma4:31b-mlx_kb_rag vs nemotron-mini:4b_baseline | -0.3648 | 0.0000e+00 | ✅ Yes | [-0.4636, -0.2661] |
| gemma4:31b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | -0.2196 | 0.0000e+00 | ✅ Yes | [-0.3183, -0.1209] |
| gemma4:31b-mlx_kb_rag vs qwen2.5:14b_baseline | -0.0886 | 1.5750e-01 | ❌ No | [-0.1873, 0.0102] |
| gemma4:31b-mlx_kb_rag vs qwen2.5:14b_kb_rag | -0.0423 | 9.9840e-01 | ❌ No | [-0.1411, 0.0564] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_baseline | -0.1087 | 1.3100e-02 | ✅ Yes | [-0.2074, -0.0099] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.0762 | 4.4390e-01 | ❌ No | [-0.1749, 0.0226] |
| gemma4:latest_baseline vs gemma4:latest_kb_rag | -0.0117 | 1.0000e+00 | ❌ No | [-0.1104, 0.0870] |
| gemma4:latest_baseline vs gemma:latest_baseline | -0.1191 | 2.6000e-03 | ✅ Yes | [-0.2178, -0.0204] |
| gemma4:latest_baseline vs gemma:latest_kb_rag | -0.0455 | 9.9520e-01 | ❌ No | [-0.1442, 0.0532] |
| gemma4:latest_baseline vs gpt-oss:20b_baseline | -0.1207 | 2.0000e-03 | ✅ Yes | [-0.2195, -0.0220] |
| gemma4:latest_baseline vs gpt-oss:20b_kb_rag | -0.2173 | 0.0000e+00 | ✅ Yes | [-0.3160, -0.1185] |
| gemma4:latest_baseline vs llama3.1:8b_baseline | -0.0715 | 5.8340e-01 | ❌ No | [-0.1703, 0.0272] |
| gemma4:latest_baseline vs llama3.1:8b_kb_rag | -0.0516 | 9.7470e-01 | ❌ No | [-0.1504, 0.0471] |
| gemma4:latest_baseline vs llama3.2:latest_baseline | -0.1980 | 0.0000e+00 | ✅ Yes | [-0.2967, -0.0993] |
| gemma4:latest_baseline vs llama3.2:latest_kb_rag | -0.0898 | 1.3900e-01 | ❌ No | [-0.1885, 0.0089] |
| gemma4:latest_baseline vs mistral-nemo:latest_baseline | -0.1253 | 9.0000e-04 | ✅ Yes | [-0.2240, -0.0266] |
| gemma4:latest_baseline vs mistral-nemo:latest_kb_rag | -0.1016 | 3.4800e-02 | ✅ Yes | [-0.2003, -0.0028] |
| gemma4:latest_baseline vs nemotron-mini:4b_baseline | -0.3332 | 0.0000e+00 | ✅ Yes | [-0.4319, -0.2345] |
| gemma4:latest_baseline vs nemotron-mini:4b_kb_rag | -0.1880 | 0.0000e+00 | ✅ Yes | [-0.2867, -0.0892] |
| gemma4:latest_baseline vs qwen2.5:14b_baseline | -0.0569 | 9.2630e-01 | ❌ No | [-0.1557, 0.0418] |
| gemma4:latest_baseline vs qwen2.5:14b_kb_rag | -0.0107 | 1.0000e+00 | ❌ No | [-0.1094, 0.0880] |
| gemma4:latest_baseline vs qwen3:8b_baseline | -0.0770 | 4.1860e-01 | ❌ No | [-0.1758, 0.0217] |
| gemma4:latest_baseline vs qwen3:8b_kb_rag | -0.0445 | 9.9650e-01 | ❌ No | [-0.1433, 0.0542] |
| gemma4:latest_kb_rag vs gemma:latest_baseline | -0.1074 | 1.5700e-02 | ✅ Yes | [-0.2061, -0.0087] |
| gemma4:latest_kb_rag vs gemma:latest_kb_rag | -0.0338 | 1.0000e+00 | ❌ No | [-0.1325, 0.0649] |
| gemma4:latest_kb_rag vs gpt-oss:20b_baseline | -0.1090 | 1.2400e-02 | ✅ Yes | [-0.2078, -0.0103] |
| gemma4:latest_kb_rag vs gpt-oss:20b_kb_rag | -0.2056 | 0.0000e+00 | ✅ Yes | [-0.3043, -0.1068] |
| gemma4:latest_kb_rag vs llama3.1:8b_baseline | -0.0598 | 8.8200e-01 | ❌ No | [-0.1586, 0.0389] |
| gemma4:latest_kb_rag vs llama3.1:8b_kb_rag | -0.0400 | 9.9930e-01 | ❌ No | [-0.1387, 0.0588] |
| gemma4:latest_kb_rag vs llama3.2:latest_baseline | -0.1863 | 0.0000e+00 | ✅ Yes | [-0.2850, -0.0876] |
| gemma4:latest_kb_rag vs llama3.2:latest_kb_rag | -0.0781 | 3.8890e-01 | ❌ No | [-0.1768, 0.0206] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_baseline | -0.1136 | 6.3000e-03 | ✅ Yes | [-0.2123, -0.0149] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.0899 | 1.3780e-01 | ❌ No | [-0.1886, 0.0089] |
| gemma4:latest_kb_rag vs nemotron-mini:4b_baseline | -0.3215 | 0.0000e+00 | ✅ Yes | [-0.4202, -0.2228] |
| gemma4:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.1763 | 0.0000e+00 | ✅ Yes | [-0.2750, -0.0775] |
| gemma4:latest_kb_rag vs qwen2.5:14b_baseline | -0.0452 | 9.9560e-01 | ❌ No | [-0.1440, 0.0535] |
| gemma4:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0010 | 1.0000e+00 | ❌ No | [-0.0977, 0.0997] |
| gemma4:latest_kb_rag vs qwen3:8b_baseline | -0.0653 | 7.6120e-01 | ❌ No | [-0.1641, 0.0334] |
| gemma4:latest_kb_rag vs qwen3:8b_kb_rag | -0.0328 | 1.0000e+00 | ❌ No | [-0.1316, 0.0659] |
| gemma:latest_baseline vs gemma:latest_kb_rag | 0.0736 | 5.2010e-01 | ❌ No | [-0.0251, 0.1723] |
| gemma:latest_baseline vs gpt-oss:20b_baseline | -0.0016 | 1.0000e+00 | ❌ No | [-0.1004, 0.0971] |
| gemma:latest_baseline vs gpt-oss:20b_kb_rag | -0.0982 | 5.3600e-02 | ❌ No | [-0.1969, 0.0006] |
| gemma:latest_baseline vs llama3.1:8b_baseline | 0.0476 | 9.9110e-01 | ❌ No | [-0.0512, 0.1463] |
| gemma:latest_baseline vs llama3.1:8b_kb_rag | 0.0675 | 7.0380e-01 | ❌ No | [-0.0313, 0.1662] |
| gemma:latest_baseline vs llama3.2:latest_baseline | -0.0789 | 3.6620e-01 | ❌ No | [-0.1776, 0.0198] |
| gemma:latest_baseline vs llama3.2:latest_kb_rag | 0.0293 | 1.0000e+00 | ❌ No | [-0.0694, 0.1280] |
| gemma:latest_baseline vs mistral-nemo:latest_baseline | -0.0062 | 1.0000e+00 | ❌ No | [-0.1049, 0.0925] |
| gemma:latest_baseline vs mistral-nemo:latest_kb_rag | 0.0175 | 1.0000e+00 | ❌ No | [-0.0812, 0.1163] |
| gemma:latest_baseline vs nemotron-mini:4b_baseline | -0.2141 | 0.0000e+00 | ✅ Yes | [-0.3128, -0.1154] |
| gemma:latest_baseline vs nemotron-mini:4b_kb_rag | -0.0689 | 6.6330e-01 | ❌ No | [-0.1676, 0.0299] |
| gemma:latest_baseline vs qwen2.5:14b_baseline | 0.0622 | 8.3630e-01 | ❌ No | [-0.0366, 0.1609] |
| gemma:latest_baseline vs qwen2.5:14b_kb_rag | 0.1084 | 1.3600e-02 | ✅ Yes | [0.0097, 0.2071] |
| gemma:latest_baseline vs qwen3:8b_baseline | 0.0421 | 9.9850e-01 | ❌ No | [-0.0567, 0.1408] |
| gemma:latest_baseline vs qwen3:8b_kb_rag | 0.0746 | 4.9140e-01 | ❌ No | [-0.0242, 0.1733] |
| gemma:latest_kb_rag vs gpt-oss:20b_baseline | -0.0753 | 4.7070e-01 | ❌ No | [-0.1740, 0.0235] |
| gemma:latest_kb_rag vs gpt-oss:20b_kb_rag | -0.1718 | 0.0000e+00 | ✅ Yes | [-0.2705, -0.0730] |
| gemma:latest_kb_rag vs llama3.1:8b_baseline | -0.0260 | 1.0000e+00 | ❌ No | [-0.1248, 0.0727] |
| gemma:latest_kb_rag vs llama3.1:8b_kb_rag | -0.0062 | 1.0000e+00 | ❌ No | [-0.1049, 0.0926] |
| gemma:latest_kb_rag vs llama3.2:latest_baseline | -0.1525 | 0.0000e+00 | ✅ Yes | [-0.2512, -0.0538] |
| gemma:latest_kb_rag vs llama3.2:latest_kb_rag | -0.0443 | 9.9680e-01 | ❌ No | [-0.1430, 0.0544] |
| gemma:latest_kb_rag vs mistral-nemo:latest_baseline | -0.0798 | 3.4270e-01 | ❌ No | [-0.1785, 0.0189] |
| gemma:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.0561 | 9.3680e-01 | ❌ No | [-0.1548, 0.0427] |
| gemma:latest_kb_rag vs nemotron-mini:4b_baseline | -0.2877 | 0.0000e+00 | ✅ Yes | [-0.3864, -0.1890] |
| gemma:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.1425 | 0.0000e+00 | ✅ Yes | [-0.2412, -0.0437] |
| gemma:latest_kb_rag vs qwen2.5:14b_baseline | -0.0114 | 1.0000e+00 | ❌ No | [-0.1102, 0.0873] |
| gemma:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0348 | 9.9990e-01 | ❌ No | [-0.0640, 0.1335] |
| gemma:latest_kb_rag vs qwen3:8b_baseline | -0.0315 | 1.0000e+00 | ❌ No | [-0.1303, 0.0672] |
| gemma:latest_kb_rag vs qwen3:8b_kb_rag | 0.0009 | 1.0000e+00 | ❌ No | [-0.0978, 0.0997] |
| gpt-oss:20b_baseline vs gpt-oss:20b_kb_rag | -0.0965 | 6.5500e-02 | ❌ No | [-0.1952, 0.0022] |
| gpt-oss:20b_baseline vs llama3.1:8b_baseline | 0.0492 | 9.8610e-01 | ❌ No | [-0.0495, 0.1479] |
| gpt-oss:20b_baseline vs llama3.1:8b_kb_rag | 0.0691 | 6.5640e-01 | ❌ No | [-0.0296, 0.1678] |
| gpt-oss:20b_baseline vs llama3.2:latest_baseline | -0.0773 | 4.1190e-01 | ❌ No | [-0.1760, 0.0215] |
| gpt-oss:20b_baseline vs llama3.2:latest_kb_rag | 0.0310 | 1.0000e+00 | ❌ No | [-0.0678, 0.1297] |
| gpt-oss:20b_baseline vs mistral-nemo:latest_baseline | -0.0045 | 1.0000e+00 | ❌ No | [-0.1033, 0.0942] |
| gpt-oss:20b_baseline vs mistral-nemo:latest_kb_rag | 0.0192 | 1.0000e+00 | ❌ No | [-0.0795, 0.1179] |
| gpt-oss:20b_baseline vs nemotron-mini:4b_baseline | -0.2125 | 0.0000e+00 | ✅ Yes | [-0.3112, -0.1137] |
| gpt-oss:20b_baseline vs nemotron-mini:4b_kb_rag | -0.0672 | 7.1040e-01 | ❌ No | [-0.1659, 0.0315] |
| gpt-oss:20b_baseline vs qwen2.5:14b_baseline | 0.0638 | 7.9910e-01 | ❌ No | [-0.0349, 0.1625] |
| gpt-oss:20b_baseline vs qwen2.5:14b_kb_rag | 0.1100 | 1.0700e-02 | ✅ Yes | [0.0113, 0.2087] |
| gpt-oss:20b_baseline vs qwen3:8b_baseline | 0.0437 | 9.9730e-01 | ❌ No | [-0.0550, 0.1424] |
| gpt-oss:20b_baseline vs qwen3:8b_kb_rag | 0.0762 | 4.4270e-01 | ❌ No | [-0.0225, 0.1749] |
| gpt-oss:20b_kb_rag vs llama3.1:8b_baseline | 0.1457 | 0.0000e+00 | ✅ Yes | [0.0470, 0.2445] |
| gpt-oss:20b_kb_rag vs llama3.1:8b_kb_rag | 0.1656 | 0.0000e+00 | ✅ Yes | [0.0669, 0.2643] |
| gpt-oss:20b_kb_rag vs llama3.2:latest_baseline | 0.0192 | 1.0000e+00 | ❌ No | [-0.0795, 0.1180] |
| gpt-oss:20b_kb_rag vs llama3.2:latest_kb_rag | 0.1275 | 6.0000e-04 | ✅ Yes | [0.0287, 0.2262] |
| gpt-oss:20b_kb_rag vs mistral-nemo:latest_baseline | 0.0920 | 1.1010e-01 | ❌ No | [-0.0067, 0.1907] |
| gpt-oss:20b_kb_rag vs mistral-nemo:latest_kb_rag | 0.1157 | 4.5000e-03 | ✅ Yes | [0.0170, 0.2144] |
| gpt-oss:20b_kb_rag vs nemotron-mini:4b_baseline | -0.1160 | 4.3000e-03 | ✅ Yes | [-0.2147, -0.0172] |
| gpt-oss:20b_kb_rag vs nemotron-mini:4b_kb_rag | 0.0293 | 1.0000e+00 | ❌ No | [-0.0694, 0.1280] |
| gpt-oss:20b_kb_rag vs qwen2.5:14b_baseline | 0.1603 | 0.0000e+00 | ✅ Yes | [0.0616, 0.2590] |
| gpt-oss:20b_kb_rag vs qwen2.5:14b_kb_rag | 0.2065 | 0.0000e+00 | ✅ Yes | [0.1078, 0.3053] |
| gpt-oss:20b_kb_rag vs qwen3:8b_baseline | 0.1402 | 1.0000e-04 | ✅ Yes | [0.0415, 0.2389] |
| gpt-oss:20b_kb_rag vs qwen3:8b_kb_rag | 0.1727 | 0.0000e+00 | ✅ Yes | [0.0740, 0.2714] |
| llama3.1:8b_baseline vs llama3.1:8b_kb_rag | 0.0199 | 1.0000e+00 | ❌ No | [-0.0788, 0.1186] |
| llama3.1:8b_baseline vs llama3.2:latest_baseline | -0.1265 | 7.0000e-04 | ✅ Yes | [-0.2252, -0.0278] |
| llama3.1:8b_baseline vs llama3.2:latest_kb_rag | -0.0183 | 1.0000e+00 | ❌ No | [-0.1170, 0.0805] |
| llama3.1:8b_baseline vs mistral-nemo:latest_baseline | -0.0538 | 9.5980e-01 | ❌ No | [-0.1525, 0.0450] |
| llama3.1:8b_baseline vs mistral-nemo:latest_kb_rag | -0.0300 | 1.0000e+00 | ❌ No | [-0.1288, 0.0687] |
| llama3.1:8b_baseline vs nemotron-mini:4b_baseline | -0.2617 | 0.0000e+00 | ✅ Yes | [-0.3604, -0.1630] |
| llama3.1:8b_baseline vs nemotron-mini:4b_kb_rag | -0.1164 | 4.0000e-03 | ✅ Yes | [-0.2152, -0.0177] |
| llama3.1:8b_baseline vs qwen2.5:14b_baseline | 0.0146 | 1.0000e+00 | ❌ No | [-0.0841, 0.1133] |
| llama3.1:8b_baseline vs qwen2.5:14b_kb_rag | 0.0608 | 8.6390e-01 | ❌ No | [-0.0379, 0.1595] |
| llama3.1:8b_baseline vs qwen3:8b_baseline | -0.0055 | 1.0000e+00 | ❌ No | [-0.1042, 0.0932] |
| llama3.1:8b_baseline vs qwen3:8b_kb_rag | 0.0270 | 1.0000e+00 | ❌ No | [-0.0717, 0.1257] |
| llama3.1:8b_kb_rag vs llama3.2:latest_baseline | -0.1464 | 0.0000e+00 | ✅ Yes | [-0.2451, -0.0476] |
| llama3.1:8b_kb_rag vs llama3.2:latest_kb_rag | -0.0381 | 9.9970e-01 | ❌ No | [-0.1369, 0.0606] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_baseline | -0.0736 | 5.1940e-01 | ❌ No | [-0.1724, 0.0251] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_kb_rag | -0.0499 | 9.8330e-01 | ❌ No | [-0.1486, 0.0488] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_baseline | -0.2816 | 0.0000e+00 | ✅ Yes | [-0.3803, -0.1828] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_kb_rag | -0.1363 | 1.0000e-04 | ✅ Yes | [-0.2350, -0.0376] |
| llama3.1:8b_kb_rag vs qwen2.5:14b_baseline | -0.0053 | 1.0000e+00 | ❌ No | [-0.1040, 0.0934] |
| llama3.1:8b_kb_rag vs qwen2.5:14b_kb_rag | 0.0409 | 9.9900e-01 | ❌ No | [-0.0578, 0.1397] |
| llama3.1:8b_kb_rag vs qwen3:8b_baseline | -0.0254 | 1.0000e+00 | ❌ No | [-0.1241, 0.0733] |
| llama3.1:8b_kb_rag vs qwen3:8b_kb_rag | 0.0071 | 1.0000e+00 | ❌ No | [-0.0916, 0.1058] |
| llama3.2:latest_baseline vs llama3.2:latest_kb_rag | 0.1082 | 1.3900e-02 | ✅ Yes | [0.0095, 0.2070] |
| llama3.2:latest_baseline vs mistral-nemo:latest_baseline | 0.0727 | 5.4680e-01 | ❌ No | [-0.0260, 0.1715] |
| llama3.2:latest_baseline vs mistral-nemo:latest_kb_rag | 0.0964 | 6.6000e-02 | ❌ No | [-0.0023, 0.1952] |
| llama3.2:latest_baseline vs nemotron-mini:4b_baseline | -0.1352 | 2.0000e-04 | ✅ Yes | [-0.2339, -0.0365] |
| llama3.2:latest_baseline vs nemotron-mini:4b_kb_rag | 0.0101 | 1.0000e+00 | ❌ No | [-0.0887, 0.1088] |
| llama3.2:latest_baseline vs qwen2.5:14b_baseline | 0.1411 | 0.0000e+00 | ✅ Yes | [0.0424, 0.2398] |
| llama3.2:latest_baseline vs qwen2.5:14b_kb_rag | 0.1873 | 0.0000e+00 | ✅ Yes | [0.0886, 0.2860] |
| llama3.2:latest_baseline vs qwen3:8b_baseline | 0.1210 | 1.9000e-03 | ✅ Yes | [0.0223, 0.2197] |
| llama3.2:latest_baseline vs qwen3:8b_kb_rag | 0.1535 | 0.0000e+00 | ✅ Yes | [0.0547, 0.2522] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_baseline | -0.0355 | 9.9990e-01 | ❌ No | [-0.1342, 0.0632] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.0118 | 1.0000e+00 | ❌ No | [-0.1105, 0.0869] |
| llama3.2:latest_kb_rag vs nemotron-mini:4b_baseline | -0.2434 | 0.0000e+00 | ✅ Yes | [-0.3421, -0.1447] |
| llama3.2:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.0982 | 5.3500e-02 | ❌ No | [-0.1969, 0.0005] |
| llama3.2:latest_kb_rag vs qwen2.5:14b_baseline | 0.0329 | 1.0000e+00 | ❌ No | [-0.0659, 0.1316] |
| llama3.2:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0791 | 3.6200e-01 | ❌ No | [-0.0197, 0.1778] |
| llama3.2:latest_kb_rag vs qwen3:8b_baseline | 0.0127 | 1.0000e+00 | ❌ No | [-0.0860, 0.1115] |
| llama3.2:latest_kb_rag vs qwen3:8b_kb_rag | 0.0452 | 9.9560e-01 | ❌ No | [-0.0535, 0.1440] |
| mistral-nemo:latest_baseline vs mistral-nemo:latest_kb_rag | 0.0237 | 1.0000e+00 | ❌ No | [-0.0750, 0.1224] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_baseline | -0.2079 | 0.0000e+00 | ✅ Yes | [-0.3067, -0.1092] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_kb_rag | -0.0627 | 8.2520e-01 | ❌ No | [-0.1614, 0.0360] |
| mistral-nemo:latest_baseline vs qwen2.5:14b_baseline | 0.0683 | 6.7820e-01 | ❌ No | [-0.0304, 0.1671] |
| mistral-nemo:latest_baseline vs qwen2.5:14b_kb_rag | 0.1146 | 5.4000e-03 | ✅ Yes | [0.0158, 0.2133] |
| mistral-nemo:latest_baseline vs qwen3:8b_baseline | 0.0482 | 9.8930e-01 | ❌ No | [-0.0505, 0.1470] |
| mistral-nemo:latest_baseline vs qwen3:8b_kb_rag | 0.0807 | 3.1830e-01 | ❌ No | [-0.0180, 0.1795] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_baseline | -0.2316 | 0.0000e+00 | ✅ Yes | [-0.3304, -0.1329] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.0864 | 1.9440e-01 | ❌ No | [-0.1851, 0.0123] |
| mistral-nemo:latest_kb_rag vs qwen2.5:14b_baseline | 0.0446 | 9.9640e-01 | ❌ No | [-0.0541, 0.1434] |
| mistral-nemo:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0908 | 1.2430e-01 | ❌ No | [-0.0079, 0.1896] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_baseline | 0.0245 | 1.0000e+00 | ❌ No | [-0.0742, 0.1233] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_kb_rag | 0.0570 | 9.2510e-01 | ❌ No | [-0.0417, 0.1557] |
| nemotron-mini:4b_baseline vs nemotron-mini:4b_kb_rag | 0.1452 | 0.0000e+00 | ✅ Yes | [0.0465, 0.2440] |
| nemotron-mini:4b_baseline vs qwen2.5:14b_baseline | 0.2763 | 0.0000e+00 | ✅ Yes | [0.1776, 0.3750] |
| nemotron-mini:4b_baseline vs qwen2.5:14b_kb_rag | 0.3225 | 0.0000e+00 | ✅ Yes | [0.2238, 0.4212] |
| nemotron-mini:4b_baseline vs qwen3:8b_baseline | 0.2562 | 0.0000e+00 | ✅ Yes | [0.1575, 0.3549] |
| nemotron-mini:4b_baseline vs qwen3:8b_kb_rag | 0.2887 | 0.0000e+00 | ✅ Yes | [0.1899, 0.3874] |
| nemotron-mini:4b_kb_rag vs qwen2.5:14b_baseline | 0.1310 | 3.0000e-04 | ✅ Yes | [0.0323, 0.2298] |
| nemotron-mini:4b_kb_rag vs qwen2.5:14b_kb_rag | 0.1772 | 0.0000e+00 | ✅ Yes | [0.0785, 0.2760] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_baseline | 0.1109 | 9.4000e-03 | ✅ Yes | [0.0122, 0.2097] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_kb_rag | 0.1434 | 0.0000e+00 | ✅ Yes | [0.0447, 0.2421] |
| qwen2.5:14b_baseline vs qwen2.5:14b_kb_rag | 0.0462 | 9.9400e-01 | ❌ No | [-0.0525, 0.1449] |
| qwen2.5:14b_baseline vs qwen3:8b_baseline | -0.0201 | 1.0000e+00 | ❌ No | [-0.1188, 0.0786] |
| qwen2.5:14b_baseline vs qwen3:8b_kb_rag | 0.0124 | 1.0000e+00 | ❌ No | [-0.0863, 0.1111] |
| qwen2.5:14b_kb_rag vs qwen3:8b_baseline | -0.0663 | 7.3520e-01 | ❌ No | [-0.1650, 0.0324] |
| qwen2.5:14b_kb_rag vs qwen3:8b_kb_rag | -0.0338 | 1.0000e+00 | ❌ No | [-0.1325, 0.0649] |
| qwen3:8b_baseline vs qwen3:8b_kb_rag | 0.0325 | 1.0000e+00 | ❌ No | [-0.0662, 0.1312] |

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
| gpt-oss:20b_baseline | 0.4384 | 0.4373 | -0.0011 | 📉 Decreased |
| gpt-oss:20b_kb_rag | 0.3419 | 0.3699 | +0.0280 | 📈 Improved |
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
