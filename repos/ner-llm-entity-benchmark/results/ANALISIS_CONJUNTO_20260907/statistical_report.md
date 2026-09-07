# 🔗 Merged Benchmark Analysis — Provenance & Integrity

- **Corpus:** `data/benchmark_balanced_120.json`
- **Registros esperados por modelo+modo:** 120
- **Corridas combinadas:** 7
- **Grupos (modelo+modo) analizados:** 28
- **Filas totales tras el merge:** 3360

## Fuentes
| # | Corrida | CSV | Filas | Modelos aportados |
| :---: | :--- | :--- | :---: | :---: |
| 1 | 01_qwen3_nothink | `/private/tmp/claude-501/-Users-eahumada-Documents-Personal-MTI-mti-pge-tesina-ner-llm-local/87e8505b-1ba9-4f7a-8204-01d63aa41522/scratchpad/anova_stage/01_qwen3_nothink/benchmark_results.csv` | 240 | 2 |
| 2 | 02_gemma4_12b_mlx | `/private/tmp/claude-501/-Users-eahumada-Documents-Personal-MTI-mti-pge-tesina-ner-llm-local/87e8505b-1ba9-4f7a-8204-01d63aa41522/scratchpad/anova_stage/02_gemma4_12b_mlx/benchmark_results.csv` | 240 | 2 |
| 3 | 03_nemotron_rerun | `/private/tmp/claude-501/-Users-eahumada-Documents-Personal-MTI-mti-pge-tesina-ner-llm-local/87e8505b-1ba9-4f7a-8204-01d63aa41522/scratchpad/anova_stage/03_nemotron_rerun/benchmark_results.csv` | 240 | 2 |
| 4 | 04_cloud | `/private/tmp/claude-501/-Users-eahumada-Documents-Personal-MTI-mti-pge-tesina-ner-llm-local/87e8505b-1ba9-4f7a-8204-01d63aa41522/scratchpad/anova_stage/04_cloud/benchmark_results.csv` | 240 | 2 |
| 5 | 05_excluidos | `/private/tmp/claude-501/-Users-eahumada-Documents-Personal-MTI-mti-pge-tesina-ner-llm-local/87e8505b-1ba9-4f7a-8204-01d63aa41522/scratchpad/anova_stage/05_excluidos/benchmark_results.csv` | 480 | 4 |
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
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
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
- **F-Statistic:** 36.3696
- **p-Value:** 1.4321e-164

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
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 120 | 0.5627 | 0.5278 | 0.5976 | 0.1932 |
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 120 | 0.5964 | 0.5624 | 0.6305 | 0.1881 |
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
| deepseek-r1:1.5b_baseline vs deepseek-r1:1.5b_kb_rag | -0.0090 | 1.0000e+00 | ❌ No | [-0.1081, 0.0902] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_baseline | 0.3135 | 0.0000e+00 | ✅ Yes | [0.2143, 0.4126] |
| deepseek-r1:1.5b_baseline vs gemma4:12b-mlx_kb_rag | 0.3363 | 0.0000e+00 | ✅ Yes | [0.2371, 0.4354] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_baseline | 0.3755 | 0.0000e+00 | ✅ Yes | [0.2764, 0.4747] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-cloud_kb_rag | 0.3701 | 0.0000e+00 | ✅ Yes | [0.2710, 0.4693] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_baseline | 0.3442 | 0.0000e+00 | ✅ Yes | [0.2451, 0.4434] |
| deepseek-r1:1.5b_baseline vs gemma4:31b-mlx_kb_rag | 0.3424 | 0.0000e+00 | ✅ Yes | [0.2433, 0.4416] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_baseline | 0.3108 | 0.0000e+00 | ✅ Yes | [0.2116, 0.4099] |
| deepseek-r1:1.5b_baseline vs gemma4:latest_kb_rag | 0.2991 | 0.0000e+00 | ✅ Yes | [0.1999, 0.3982] |
| deepseek-r1:1.5b_baseline vs gemma:latest_baseline | 0.1917 | 0.0000e+00 | ✅ Yes | [0.0925, 0.2908] |
| deepseek-r1:1.5b_baseline vs gemma:latest_kb_rag | 0.2653 | 0.0000e+00 | ✅ Yes | [0.1662, 0.3645] |
| deepseek-r1:1.5b_baseline vs gpt-oss:20b_baseline | 0.1900 | 0.0000e+00 | ✅ Yes | [0.0909, 0.2892] |
| deepseek-r1:1.5b_baseline vs gpt-oss:20b_kb_rag | 0.0935 | 9.7900e-02 | ❌ No | [-0.0056, 0.1927] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_baseline | 0.2393 | 0.0000e+00 | ✅ Yes | [0.1401, 0.3384] |
| deepseek-r1:1.5b_baseline vs llama3.1:8b_kb_rag | 0.2591 | 0.0000e+00 | ✅ Yes | [0.1600, 0.3583] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_baseline | 0.1128 | 7.3000e-03 | ✅ Yes | [0.0136, 0.2119] |
| deepseek-r1:1.5b_baseline vs llama3.2:latest_kb_rag | 0.2210 | 0.0000e+00 | ✅ Yes | [0.1219, 0.3202] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_baseline | 0.1855 | 0.0000e+00 | ✅ Yes | [0.0864, 0.2847] |
| deepseek-r1:1.5b_baseline vs mistral-nemo:latest_kb_rag | 0.2092 | 0.0000e+00 | ✅ Yes | [0.1101, 0.3084] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_baseline | -0.0224 | 1.0000e+00 | ❌ No | [-0.1216, 0.0767] |
| deepseek-r1:1.5b_baseline vs nemotron-mini:4b_kb_rag | 0.1228 | 1.4000e-03 | ✅ Yes | [0.0237, 0.2220] |
| deepseek-r1:1.5b_baseline vs qwen2.5:14b_baseline | 0.2539 | 0.0000e+00 | ✅ Yes | [0.1547, 0.3530] |
| deepseek-r1:1.5b_baseline vs qwen2.5:14b_kb_rag | 0.3001 | 0.0000e+00 | ✅ Yes | [0.2009, 0.3992] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_baseline | 0.2338 | 0.0000e+00 | ✅ Yes | [0.1346, 0.3329] |
| deepseek-r1:1.5b_baseline vs qwen3:8b_kb_rag | 0.2663 | 0.0000e+00 | ✅ Yes | [0.1671, 0.3654] |
| deepseek-r1:1.5b_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.3143 | 0.0000e+00 | ✅ Yes | [0.2152, 0.4135] |
| deepseek-r1:1.5b_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.3481 | 0.0000e+00 | ✅ Yes | [0.2490, 0.4473] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_baseline | 0.3225 | 0.0000e+00 | ✅ Yes | [0.2233, 0.4216] |
| deepseek-r1:1.5b_kb_rag vs gemma4:12b-mlx_kb_rag | 0.3452 | 0.0000e+00 | ✅ Yes | [0.2461, 0.4444] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-cloud_baseline | 0.3845 | 0.0000e+00 | ✅ Yes | [0.2853, 0.4836] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-cloud_kb_rag | 0.3791 | 0.0000e+00 | ✅ Yes | [0.2800, 0.4782] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-mlx_baseline | 0.3532 | 0.0000e+00 | ✅ Yes | [0.2540, 0.4523] |
| deepseek-r1:1.5b_kb_rag vs gemma4:31b-mlx_kb_rag | 0.3514 | 0.0000e+00 | ✅ Yes | [0.2522, 0.4505] |
| deepseek-r1:1.5b_kb_rag vs gemma4:latest_baseline | 0.3198 | 0.0000e+00 | ✅ Yes | [0.2206, 0.4189] |
| deepseek-r1:1.5b_kb_rag vs gemma4:latest_kb_rag | 0.3081 | 0.0000e+00 | ✅ Yes | [0.2089, 0.4072] |
| deepseek-r1:1.5b_kb_rag vs gemma:latest_baseline | 0.2007 | 0.0000e+00 | ✅ Yes | [0.1015, 0.2998] |
| deepseek-r1:1.5b_kb_rag vs gemma:latest_kb_rag | 0.2743 | 0.0000e+00 | ✅ Yes | [0.1751, 0.3734] |
| deepseek-r1:1.5b_kb_rag vs gpt-oss:20b_baseline | 0.1990 | 0.0000e+00 | ✅ Yes | [0.0999, 0.2982] |
| deepseek-r1:1.5b_kb_rag vs gpt-oss:20b_kb_rag | 0.1025 | 3.2300e-02 | ✅ Yes | [0.0034, 0.2017] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_baseline | 0.2482 | 0.0000e+00 | ✅ Yes | [0.1491, 0.3474] |
| deepseek-r1:1.5b_kb_rag vs llama3.1:8b_kb_rag | 0.2681 | 0.0000e+00 | ✅ Yes | [0.1690, 0.3673] |
| deepseek-r1:1.5b_kb_rag vs llama3.2:latest_baseline | 0.1217 | 1.7000e-03 | ✅ Yes | [0.0226, 0.2209] |
| deepseek-r1:1.5b_kb_rag vs llama3.2:latest_kb_rag | 0.2300 | 0.0000e+00 | ✅ Yes | [0.1308, 0.3291] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_baseline | 0.1945 | 0.0000e+00 | ✅ Yes | [0.0953, 0.2936] |
| deepseek-r1:1.5b_kb_rag vs mistral-nemo:latest_kb_rag | 0.2182 | 0.0000e+00 | ✅ Yes | [0.1190, 0.3173] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_baseline | -0.0134 | 1.0000e+00 | ❌ No | [-0.1126, 0.0857] |
| deepseek-r1:1.5b_kb_rag vs nemotron-mini:4b_kb_rag | 0.1318 | 3.0000e-04 | ✅ Yes | [0.0327, 0.2309] |
| deepseek-r1:1.5b_kb_rag vs qwen2.5:14b_baseline | 0.2628 | 0.0000e+00 | ✅ Yes | [0.1637, 0.3620] |
| deepseek-r1:1.5b_kb_rag vs qwen2.5:14b_kb_rag | 0.3090 | 0.0000e+00 | ✅ Yes | [0.2099, 0.4082] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_baseline | 0.2427 | 0.0000e+00 | ✅ Yes | [0.1436, 0.3419] |
| deepseek-r1:1.5b_kb_rag vs qwen3:8b_kb_rag | 0.2752 | 0.0000e+00 | ✅ Yes | [0.1761, 0.3744] |
| deepseek-r1:1.5b_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.3233 | 0.0000e+00 | ✅ Yes | [0.2242, 0.4225] |
| deepseek-r1:1.5b_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.3571 | 0.0000e+00 | ✅ Yes | [0.2579, 0.4562] |
| gemma4:12b-mlx_baseline vs gemma4:12b-mlx_kb_rag | 0.0228 | 1.0000e+00 | ❌ No | [-0.0764, 0.1219] |
| gemma4:12b-mlx_baseline vs gemma4:31b-cloud_baseline | 0.0620 | 8.5960e-01 | ❌ No | [-0.0371, 0.1612] |
| gemma4:12b-mlx_baseline vs gemma4:31b-cloud_kb_rag | 0.0566 | 9.4230e-01 | ❌ No | [-0.0425, 0.1558] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_baseline | 0.0307 | 1.0000e+00 | ❌ No | [-0.0684, 0.1299] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_kb_rag | 0.0289 | 1.0000e+00 | ❌ No | [-0.0702, 0.1281] |
| gemma4:12b-mlx_baseline vs gemma4:latest_baseline | -0.0027 | 1.0000e+00 | ❌ No | [-0.1018, 0.0965] |
| gemma4:12b-mlx_baseline vs gemma4:latest_kb_rag | -0.0144 | 1.0000e+00 | ❌ No | [-0.1135, 0.0848] |
| gemma4:12b-mlx_baseline vs gemma:latest_baseline | -0.1218 | 1.7000e-03 | ✅ Yes | [-0.2209, -0.0226] |
| gemma4:12b-mlx_baseline vs gemma:latest_kb_rag | -0.0482 | 9.9250e-01 | ❌ No | [-0.1473, 0.0510] |
| gemma4:12b-mlx_baseline vs gpt-oss:20b_baseline | -0.1234 | 1.3000e-03 | ✅ Yes | [-0.2226, -0.0243] |
| gemma4:12b-mlx_baseline vs gpt-oss:20b_kb_rag | -0.2200 | 0.0000e+00 | ✅ Yes | [-0.3191, -0.1208] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_baseline | -0.0742 | 5.2530e-01 | ❌ No | [-0.1734, 0.0249] |
| gemma4:12b-mlx_baseline vs llama3.1:8b_kb_rag | -0.0543 | 9.6390e-01 | ❌ No | [-0.1535, 0.0448] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_baseline | -0.2007 | 0.0000e+00 | ✅ Yes | [-0.2999, -0.1016] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_kb_rag | -0.0925 | 1.1020e-01 | ❌ No | [-0.1916, 0.0067] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_baseline | -0.1280 | 6.0000e-04 | ✅ Yes | [-0.2271, -0.0288] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.1043 | 2.5500e-02 | ✅ Yes | [-0.2034, -0.0051] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_baseline | -0.3359 | 0.0000e+00 | ✅ Yes | [-0.4351, -0.2368] |
| gemma4:12b-mlx_baseline vs nemotron-mini:4b_kb_rag | -0.1907 | 0.0000e+00 | ✅ Yes | [-0.2898, -0.0915] |
| gemma4:12b-mlx_baseline vs qwen2.5:14b_baseline | -0.0596 | 9.0230e-01 | ❌ No | [-0.1588, 0.0395] |
| gemma4:12b-mlx_baseline vs qwen2.5:14b_kb_rag | -0.0134 | 1.0000e+00 | ❌ No | [-0.1126, 0.0857] |
| gemma4:12b-mlx_baseline vs qwen3:8b_baseline | -0.0797 | 3.6300e-01 | ❌ No | [-0.1789, 0.0194] |
| gemma4:12b-mlx_baseline vs qwen3:8b_kb_rag | -0.0472 | 9.9440e-01 | ❌ No | [-0.1464, 0.0519] |
| gemma4:12b-mlx_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.0009 | 1.0000e+00 | ❌ No | [-0.0983, 0.1000] |
| gemma4:12b-mlx_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0346 | 1.0000e+00 | ❌ No | [-0.0645, 0.1338] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-cloud_baseline | 0.0392 | 9.9970e-01 | ❌ No | [-0.0599, 0.1384] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-cloud_kb_rag | 0.0339 | 1.0000e+00 | ❌ No | [-0.0653, 0.1330] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_baseline | 0.0080 | 1.0000e+00 | ❌ No | [-0.0912, 0.1071] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_kb_rag | 0.0062 | 1.0000e+00 | ❌ No | [-0.0930, 0.1053] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_baseline | -0.0255 | 1.0000e+00 | ❌ No | [-0.1246, 0.0737] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0372 | 9.9990e-01 | ❌ No | [-0.1363, 0.0620] |
| gemma4:12b-mlx_kb_rag vs gemma:latest_baseline | -0.1446 | 0.0000e+00 | ✅ Yes | [-0.2437, -0.0454] |
| gemma4:12b-mlx_kb_rag vs gemma:latest_kb_rag | -0.0710 | 6.2600e-01 | ❌ No | [-0.1701, 0.0282] |
| gemma4:12b-mlx_kb_rag vs gpt-oss:20b_baseline | -0.1462 | 0.0000e+00 | ✅ Yes | [-0.2454, -0.0471] |
| gemma4:12b-mlx_kb_rag vs gpt-oss:20b_kb_rag | -0.2427 | 0.0000e+00 | ✅ Yes | [-0.3419, -0.1436] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_baseline | -0.0970 | 6.5300e-02 | ❌ No | [-0.1961, 0.0022] |
| gemma4:12b-mlx_kb_rag vs llama3.1:8b_kb_rag | -0.0771 | 4.3770e-01 | ❌ No | [-0.1763, 0.0220] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_baseline | -0.2235 | 0.0000e+00 | ✅ Yes | [-0.3226, -0.1243] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.1152 | 5.0000e-03 | ✅ Yes | [-0.2144, -0.0161] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.1507 | 0.0000e+00 | ✅ Yes | [-0.2499, -0.0516] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.1270 | 7.0000e-04 | ✅ Yes | [-0.2262, -0.0279] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_baseline | -0.3587 | 0.0000e+00 | ✅ Yes | [-0.4578, -0.2595] |
| gemma4:12b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | -0.2134 | 0.0000e+00 | ✅ Yes | [-0.3126, -0.1143] |
| gemma4:12b-mlx_kb_rag vs qwen2.5:14b_baseline | -0.0824 | 2.9370e-01 | ❌ No | [-0.1815, 0.0168] |
| gemma4:12b-mlx_kb_rag vs qwen2.5:14b_kb_rag | -0.0362 | 9.9990e-01 | ❌ No | [-0.1353, 0.0630] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_baseline | -0.1025 | 3.2400e-02 | ✅ Yes | [-0.2016, -0.0033] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.0700 | 6.5460e-01 | ❌ No | [-0.1692, 0.0291] |
| gemma4:12b-mlx_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | -0.0219 | 1.0000e+00 | ❌ No | [-0.1211, 0.0772] |
| gemma4:12b-mlx_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0119 | 1.0000e+00 | ❌ No | [-0.0873, 0.1110] |
| gemma4:31b-cloud_baseline vs gemma4:31b-cloud_kb_rag | -0.0054 | 1.0000e+00 | ❌ No | [-0.1045, 0.0938] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_baseline | -0.0313 | 1.0000e+00 | ❌ No | [-0.1304, 0.0679] |
| gemma4:31b-cloud_baseline vs gemma4:31b-mlx_kb_rag | -0.0331 | 1.0000e+00 | ❌ No | [-0.1322, 0.0661] |
| gemma4:31b-cloud_baseline vs gemma4:latest_baseline | -0.0647 | 7.9990e-01 | ❌ No | [-0.1639, 0.0344] |
| gemma4:31b-cloud_baseline vs gemma4:latest_kb_rag | -0.0764 | 4.5870e-01 | ❌ No | [-0.1756, 0.0227] |
| gemma4:31b-cloud_baseline vs gemma:latest_baseline | -0.1838 | 0.0000e+00 | ✅ Yes | [-0.2830, -0.0847] |
| gemma4:31b-cloud_baseline vs gemma:latest_kb_rag | -0.1102 | 1.0900e-02 | ✅ Yes | [-0.2094, -0.0111] |
| gemma4:31b-cloud_baseline vs gpt-oss:20b_baseline | -0.1855 | 0.0000e+00 | ✅ Yes | [-0.2846, -0.0863] |
| gemma4:31b-cloud_baseline vs gpt-oss:20b_kb_rag | -0.2820 | 0.0000e+00 | ✅ Yes | [-0.3811, -0.1828] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_baseline | -0.1362 | 1.0000e-04 | ✅ Yes | [-0.2354, -0.0371] |
| gemma4:31b-cloud_baseline vs llama3.1:8b_kb_rag | -0.1164 | 4.2000e-03 | ✅ Yes | [-0.2155, -0.0172] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_baseline | -0.2627 | 0.0000e+00 | ✅ Yes | [-0.3619, -0.1636] |
| gemma4:31b-cloud_baseline vs llama3.2:latest_kb_rag | -0.1545 | 0.0000e+00 | ✅ Yes | [-0.2536, -0.0553] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_baseline | -0.1900 | 0.0000e+00 | ✅ Yes | [-0.2891, -0.0908] |
| gemma4:31b-cloud_baseline vs mistral-nemo:latest_kb_rag | -0.1663 | 0.0000e+00 | ✅ Yes | [-0.2654, -0.0671] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_baseline | -0.3979 | 0.0000e+00 | ✅ Yes | [-0.4971, -0.2988] |
| gemma4:31b-cloud_baseline vs nemotron-mini:4b_kb_rag | -0.2527 | 0.0000e+00 | ✅ Yes | [-0.3518, -0.1535] |
| gemma4:31b-cloud_baseline vs qwen2.5:14b_baseline | -0.1216 | 1.7000e-03 | ✅ Yes | [-0.2208, -0.0225] |
| gemma4:31b-cloud_baseline vs qwen2.5:14b_kb_rag | -0.0754 | 4.8830e-01 | ❌ No | [-0.1746, 0.0237] |
| gemma4:31b-cloud_baseline vs qwen3:8b_baseline | -0.1417 | 0.0000e+00 | ✅ Yes | [-0.2409, -0.0426] |
| gemma4:31b-cloud_baseline vs qwen3:8b_kb_rag | -0.1093 | 1.2500e-02 | ✅ Yes | [-0.2084, -0.0101] |
| gemma4:31b-cloud_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | -0.0612 | 8.7600e-01 | ❌ No | [-0.1603, 0.0380] |
| gemma4:31b-cloud_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | -0.0274 | 1.0000e+00 | ❌ No | [-0.1265, 0.0718] |
| gemma4:31b-cloud_kb_rag vs gemma4:31b-mlx_baseline | -0.0259 | 1.0000e+00 | ❌ No | [-0.1251, 0.0732] |
| gemma4:31b-cloud_kb_rag vs gemma4:31b-mlx_kb_rag | -0.0277 | 1.0000e+00 | ❌ No | [-0.1269, 0.0714] |
| gemma4:31b-cloud_kb_rag vs gemma4:latest_baseline | -0.0593 | 9.0680e-01 | ❌ No | [-0.1585, 0.0398] |
| gemma4:31b-cloud_kb_rag vs gemma4:latest_kb_rag | -0.0710 | 6.2340e-01 | ❌ No | [-0.1702, 0.0281] |
| gemma4:31b-cloud_kb_rag vs gemma:latest_baseline | -0.1784 | 0.0000e+00 | ✅ Yes | [-0.2776, -0.0793] |
| gemma4:31b-cloud_kb_rag vs gemma:latest_kb_rag | -0.1048 | 2.3600e-02 | ✅ Yes | [-0.2040, -0.0057] |
| gemma4:31b-cloud_kb_rag vs gpt-oss:20b_baseline | -0.1801 | 0.0000e+00 | ✅ Yes | [-0.2792, -0.0809] |
| gemma4:31b-cloud_kb_rag vs gpt-oss:20b_kb_rag | -0.2766 | 0.0000e+00 | ✅ Yes | [-0.3757, -0.1774] |
| gemma4:31b-cloud_kb_rag vs llama3.1:8b_baseline | -0.1309 | 3.0000e-04 | ✅ Yes | [-0.2300, -0.0317] |
| gemma4:31b-cloud_kb_rag vs llama3.1:8b_kb_rag | -0.1110 | 9.7000e-03 | ✅ Yes | [-0.2101, -0.0118] |
| gemma4:31b-cloud_kb_rag vs llama3.2:latest_baseline | -0.2574 | 0.0000e+00 | ✅ Yes | [-0.3565, -0.1582] |
| gemma4:31b-cloud_kb_rag vs llama3.2:latest_kb_rag | -0.1491 | 0.0000e+00 | ✅ Yes | [-0.2483, -0.0500] |
| gemma4:31b-cloud_kb_rag vs mistral-nemo:latest_baseline | -0.1846 | 0.0000e+00 | ✅ Yes | [-0.2838, -0.0855] |
| gemma4:31b-cloud_kb_rag vs mistral-nemo:latest_kb_rag | -0.1609 | 0.0000e+00 | ✅ Yes | [-0.2601, -0.0618] |
| gemma4:31b-cloud_kb_rag vs nemotron-mini:4b_baseline | -0.3925 | 0.0000e+00 | ✅ Yes | [-0.4917, -0.2934] |
| gemma4:31b-cloud_kb_rag vs nemotron-mini:4b_kb_rag | -0.2473 | 0.0000e+00 | ✅ Yes | [-0.3464, -0.1482] |
| gemma4:31b-cloud_kb_rag vs qwen2.5:14b_baseline | -0.1163 | 4.2000e-03 | ✅ Yes | [-0.2154, -0.0171] |
| gemma4:31b-cloud_kb_rag vs qwen2.5:14b_kb_rag | -0.0701 | 6.5310e-01 | ❌ No | [-0.1692, 0.0291] |
| gemma4:31b-cloud_kb_rag vs qwen3:8b_baseline | -0.1364 | 1.0000e-04 | ✅ Yes | [-0.2355, -0.0372] |
| gemma4:31b-cloud_kb_rag vs qwen3:8b_kb_rag | -0.1039 | 2.6800e-02 | ✅ Yes | [-0.2030, -0.0047] |
| gemma4:31b-cloud_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | -0.0558 | 9.5130e-01 | ❌ No | [-0.1549, 0.0434] |
| gemma4:31b-cloud_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | -0.0220 | 1.0000e+00 | ❌ No | [-0.1212, 0.0771] |
| gemma4:31b-mlx_baseline vs gemma4:31b-mlx_kb_rag | -0.0018 | 1.0000e+00 | ❌ No | [-0.1009, 0.0973] |
| gemma4:31b-mlx_baseline vs gemma4:latest_baseline | -0.0334 | 1.0000e+00 | ❌ No | [-0.1326, 0.0657] |
| gemma4:31b-mlx_baseline vs gemma4:latest_kb_rag | -0.0451 | 9.9720e-01 | ❌ No | [-0.1443, 0.0540] |
| gemma4:31b-mlx_baseline vs gemma:latest_baseline | -0.1525 | 0.0000e+00 | ✅ Yes | [-0.2517, -0.0534] |
| gemma4:31b-mlx_baseline vs gemma:latest_kb_rag | -0.0789 | 3.8570e-01 | ❌ No | [-0.1781, 0.0202] |
| gemma4:31b-mlx_baseline vs gpt-oss:20b_baseline | -0.1542 | 0.0000e+00 | ✅ Yes | [-0.2533, -0.0550] |
| gemma4:31b-mlx_baseline vs gpt-oss:20b_kb_rag | -0.2507 | 0.0000e+00 | ✅ Yes | [-0.3498, -0.1515] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_baseline | -0.1049 | 2.3200e-02 | ✅ Yes | [-0.2041, -0.0058] |
| gemma4:31b-mlx_baseline vs llama3.1:8b_kb_rag | -0.0851 | 2.3270e-01 | ❌ No | [-0.1842, 0.0141] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_baseline | -0.2314 | 0.0000e+00 | ✅ Yes | [-0.3306, -0.1323] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_kb_rag | -0.1232 | 1.3000e-03 | ✅ Yes | [-0.2224, -0.0241] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_baseline | -0.1587 | 0.0000e+00 | ✅ Yes | [-0.2578, -0.0596] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.1350 | 2.0000e-04 | ✅ Yes | [-0.2341, -0.0358] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_baseline | -0.3666 | 0.0000e+00 | ✅ Yes | [-0.4658, -0.2675] |
| gemma4:31b-mlx_baseline vs nemotron-mini:4b_kb_rag | -0.2214 | 0.0000e+00 | ✅ Yes | [-0.3205, -0.1222] |
| gemma4:31b-mlx_baseline vs qwen2.5:14b_baseline | -0.0904 | 1.3860e-01 | ❌ No | [-0.1895, 0.0088] |
| gemma4:31b-mlx_baseline vs qwen2.5:14b_kb_rag | -0.0441 | 9.9800e-01 | ❌ No | [-0.1433, 0.0550] |
| gemma4:31b-mlx_baseline vs qwen3:8b_baseline | -0.1105 | 1.0500e-02 | ✅ Yes | [-0.2096, -0.0113] |
| gemma4:31b-mlx_baseline vs qwen3:8b_kb_rag | -0.0780 | 4.1290e-01 | ❌ No | [-0.1771, 0.0212] |
| gemma4:31b-mlx_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | -0.0299 | 1.0000e+00 | ❌ No | [-0.1290, 0.0693] |
| gemma4:31b-mlx_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0039 | 1.0000e+00 | ❌ No | [-0.0952, 0.1030] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_baseline | -0.0316 | 1.0000e+00 | ❌ No | [-0.1308, 0.0675] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0433 | 9.9850e-01 | ❌ No | [-0.1425, 0.0558] |
| gemma4:31b-mlx_kb_rag vs gemma:latest_baseline | -0.1507 | 0.0000e+00 | ✅ Yes | [-0.2499, -0.0516] |
| gemma4:31b-mlx_kb_rag vs gemma:latest_kb_rag | -0.0771 | 4.3780e-01 | ❌ No | [-0.1763, 0.0220] |
| gemma4:31b-mlx_kb_rag vs gpt-oss:20b_baseline | -0.1524 | 0.0000e+00 | ✅ Yes | [-0.2515, -0.0532] |
| gemma4:31b-mlx_kb_rag vs gpt-oss:20b_kb_rag | -0.2489 | 0.0000e+00 | ✅ Yes | [-0.3480, -0.1497] |
| gemma4:31b-mlx_kb_rag vs llama3.1:8b_baseline | -0.1031 | 2.9600e-02 | ✅ Yes | [-0.2023, -0.0040] |
| gemma4:31b-mlx_kb_rag vs llama3.1:8b_kb_rag | -0.0833 | 2.7280e-01 | ❌ No | [-0.1824, 0.0159] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_baseline | -0.2296 | 0.0000e+00 | ✅ Yes | [-0.3288, -0.1305] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.1214 | 1.8000e-03 | ✅ Yes | [-0.2205, -0.0223] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.1569 | 0.0000e+00 | ✅ Yes | [-0.2560, -0.0578] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.1332 | 2.0000e-04 | ✅ Yes | [-0.2323, -0.0340] |
| gemma4:31b-mlx_kb_rag vs nemotron-mini:4b_baseline | -0.3648 | 0.0000e+00 | ✅ Yes | [-0.4640, -0.2657] |
| gemma4:31b-mlx_kb_rag vs nemotron-mini:4b_kb_rag | -0.2196 | 0.0000e+00 | ✅ Yes | [-0.3187, -0.1204] |
| gemma4:31b-mlx_kb_rag vs qwen2.5:14b_baseline | -0.0886 | 1.6680e-01 | ❌ No | [-0.1877, 0.0106] |
| gemma4:31b-mlx_kb_rag vs qwen2.5:14b_kb_rag | -0.0423 | 9.9900e-01 | ❌ No | [-0.1415, 0.0568] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_baseline | -0.1087 | 1.3700e-02 | ✅ Yes | [-0.2078, -0.0095] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.0762 | 4.6610e-01 | ❌ No | [-0.1753, 0.0230] |
| gemma4:31b-mlx_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | -0.0281 | 1.0000e+00 | ❌ No | [-0.1272, 0.0711] |
| gemma4:31b-mlx_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0057 | 1.0000e+00 | ❌ No | [-0.0934, 0.1048] |
| gemma4:latest_baseline vs gemma4:latest_kb_rag | -0.0117 | 1.0000e+00 | ❌ No | [-0.1108, 0.0875] |
| gemma4:latest_baseline vs gemma:latest_baseline | -0.1191 | 2.7000e-03 | ✅ Yes | [-0.2182, -0.0200] |
| gemma4:latest_baseline vs gemma:latest_kb_rag | -0.0455 | 9.9680e-01 | ❌ No | [-0.1446, 0.0537] |
| gemma4:latest_baseline vs gpt-oss:20b_baseline | -0.1207 | 2.0000e-03 | ✅ Yes | [-0.2199, -0.0216] |
| gemma4:latest_baseline vs gpt-oss:20b_kb_rag | -0.2173 | 0.0000e+00 | ✅ Yes | [-0.3164, -0.1181] |
| gemma4:latest_baseline vs llama3.1:8b_baseline | -0.0715 | 6.0850e-01 | ❌ No | [-0.1707, 0.0276] |
| gemma4:latest_baseline vs llama3.1:8b_kb_rag | -0.0516 | 9.8070e-01 | ❌ No | [-0.1508, 0.0475] |
| gemma4:latest_baseline vs llama3.2:latest_baseline | -0.1980 | 0.0000e+00 | ✅ Yes | [-0.2972, -0.0989] |
| gemma4:latest_baseline vs llama3.2:latest_kb_rag | -0.0898 | 1.4710e-01 | ❌ No | [-0.1889, 0.0094] |
| gemma4:latest_baseline vs mistral-nemo:latest_baseline | -0.1253 | 9.0000e-04 | ✅ Yes | [-0.2244, -0.0261] |
| gemma4:latest_baseline vs mistral-nemo:latest_kb_rag | -0.1016 | 3.6600e-02 | ✅ Yes | [-0.2007, -0.0024] |
| gemma4:latest_baseline vs nemotron-mini:4b_baseline | -0.3332 | 0.0000e+00 | ✅ Yes | [-0.4324, -0.2341] |
| gemma4:latest_baseline vs nemotron-mini:4b_kb_rag | -0.1880 | 0.0000e+00 | ✅ Yes | [-0.2871, -0.0888] |
| gemma4:latest_baseline vs qwen2.5:14b_baseline | -0.0569 | 9.3910e-01 | ❌ No | [-0.1561, 0.0422] |
| gemma4:latest_baseline vs qwen2.5:14b_kb_rag | -0.0107 | 1.0000e+00 | ❌ No | [-0.1099, 0.0884] |
| gemma4:latest_baseline vs qwen3:8b_baseline | -0.0770 | 4.4010e-01 | ❌ No | [-0.1762, 0.0221] |
| gemma4:latest_baseline vs qwen3:8b_kb_rag | -0.0445 | 9.9770e-01 | ❌ No | [-0.1437, 0.0546] |
| gemma4:latest_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.0036 | 1.0000e+00 | ❌ No | [-0.0956, 0.1027] |
| gemma4:latest_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0373 | 9.9990e-01 | ❌ No | [-0.0618, 0.1365] |
| gemma4:latest_kb_rag vs gemma:latest_baseline | -0.1074 | 1.6400e-02 | ✅ Yes | [-0.2066, -0.0083] |
| gemma4:latest_kb_rag vs gemma:latest_kb_rag | -0.0338 | 1.0000e+00 | ❌ No | [-0.1329, 0.0654] |
| gemma4:latest_kb_rag vs gpt-oss:20b_baseline | -0.1090 | 1.2900e-02 | ✅ Yes | [-0.2082, -0.0099] |
| gemma4:latest_kb_rag vs gpt-oss:20b_kb_rag | -0.2056 | 0.0000e+00 | ✅ Yes | [-0.3047, -0.1064] |
| gemma4:latest_kb_rag vs llama3.1:8b_baseline | -0.0598 | 8.9910e-01 | ❌ No | [-0.1590, 0.0393] |
| gemma4:latest_kb_rag vs llama3.1:8b_kb_rag | -0.0400 | 9.9960e-01 | ❌ No | [-0.1391, 0.0592] |
| gemma4:latest_kb_rag vs llama3.2:latest_baseline | -0.1863 | 0.0000e+00 | ✅ Yes | [-0.2855, -0.0872] |
| gemma4:latest_kb_rag vs llama3.2:latest_kb_rag | -0.0781 | 4.0930e-01 | ❌ No | [-0.1772, 0.0211] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_baseline | -0.1136 | 6.5000e-03 | ✅ Yes | [-0.2127, -0.0144] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.0899 | 1.4580e-01 | ❌ No | [-0.1890, 0.0093] |
| gemma4:latest_kb_rag vs nemotron-mini:4b_baseline | -0.3215 | 0.0000e+00 | ✅ Yes | [-0.4207, -0.2224] |
| gemma4:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.1763 | 0.0000e+00 | ✅ Yes | [-0.2754, -0.0771] |
| gemma4:latest_kb_rag vs qwen2.5:14b_baseline | -0.0452 | 9.9710e-01 | ❌ No | [-0.1444, 0.0539] |
| gemma4:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0010 | 1.0000e+00 | ❌ No | [-0.0982, 0.1001] |
| gemma4:latest_kb_rag vs qwen3:8b_baseline | -0.0653 | 7.8460e-01 | ❌ No | [-0.1645, 0.0338] |
| gemma4:latest_kb_rag vs qwen3:8b_kb_rag | -0.0328 | 1.0000e+00 | ❌ No | [-0.1320, 0.0663] |
| gemma4:latest_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.0153 | 1.0000e+00 | ❌ No | [-0.0839, 0.1144] |
| gemma4:latest_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0490 | 9.9040e-01 | ❌ No | [-0.0501, 0.1482] |
| gemma:latest_baseline vs gemma:latest_kb_rag | 0.0736 | 5.4430e-01 | ❌ No | [-0.0255, 0.1728] |
| gemma:latest_baseline vs gpt-oss:20b_baseline | -0.0016 | 1.0000e+00 | ❌ No | [-0.1008, 0.0975] |
| gemma:latest_baseline vs gpt-oss:20b_kb_rag | -0.0982 | 5.6600e-02 | ❌ No | [-0.1973, 0.0010] |
| gemma:latest_baseline vs llama3.1:8b_baseline | 0.0476 | 9.9370e-01 | ❌ No | [-0.0516, 0.1467] |
| gemma:latest_baseline vs llama3.1:8b_kb_rag | 0.0675 | 7.2860e-01 | ❌ No | [-0.0317, 0.1666] |
| gemma:latest_baseline vs llama3.2:latest_baseline | -0.0789 | 3.8580e-01 | ❌ No | [-0.1781, 0.0202] |
| gemma:latest_baseline vs llama3.2:latest_kb_rag | 0.0293 | 1.0000e+00 | ❌ No | [-0.0698, 0.1285] |
| gemma:latest_baseline vs mistral-nemo:latest_baseline | -0.0062 | 1.0000e+00 | ❌ No | [-0.1053, 0.0930] |
| gemma:latest_baseline vs mistral-nemo:latest_kb_rag | 0.0175 | 1.0000e+00 | ❌ No | [-0.0816, 0.1167] |
| gemma:latest_baseline vs nemotron-mini:4b_baseline | -0.2141 | 0.0000e+00 | ✅ Yes | [-0.3133, -0.1150] |
| gemma:latest_baseline vs nemotron-mini:4b_kb_rag | -0.0689 | 6.8850e-01 | ❌ No | [-0.1680, 0.0303] |
| gemma:latest_baseline vs qwen2.5:14b_baseline | 0.0622 | 8.5650e-01 | ❌ No | [-0.0370, 0.1613] |
| gemma:latest_baseline vs qwen2.5:14b_kb_rag | 0.1084 | 1.4200e-02 | ✅ Yes | [0.0092, 0.2075] |
| gemma:latest_baseline vs qwen3:8b_baseline | 0.0421 | 9.9910e-01 | ❌ No | [-0.0571, 0.1412] |
| gemma:latest_baseline vs qwen3:8b_kb_rag | 0.0746 | 5.1500e-01 | ❌ No | [-0.0246, 0.1737] |
| gemma:latest_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.1227 | 1.5000e-03 | ✅ Yes | [0.0235, 0.2218] |
| gemma:latest_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.1564 | 0.0000e+00 | ✅ Yes | [0.0573, 0.2556] |
| gemma:latest_kb_rag vs gpt-oss:20b_baseline | -0.0753 | 4.9370e-01 | ❌ No | [-0.1744, 0.0239] |
| gemma:latest_kb_rag vs gpt-oss:20b_kb_rag | -0.1718 | 0.0000e+00 | ✅ Yes | [-0.2709, -0.0726] |
| gemma:latest_kb_rag vs llama3.1:8b_baseline | -0.0260 | 1.0000e+00 | ❌ No | [-0.1252, 0.0731] |
| gemma:latest_kb_rag vs llama3.1:8b_kb_rag | -0.0062 | 1.0000e+00 | ❌ No | [-0.1053, 0.0930] |
| gemma:latest_kb_rag vs llama3.2:latest_baseline | -0.1525 | 0.0000e+00 | ✅ Yes | [-0.2517, -0.0534] |
| gemma:latest_kb_rag vs llama3.2:latest_kb_rag | -0.0443 | 9.9790e-01 | ❌ No | [-0.1434, 0.0549] |
| gemma:latest_kb_rag vs mistral-nemo:latest_baseline | -0.0798 | 3.6140e-01 | ❌ No | [-0.1789, 0.0194] |
| gemma:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.0561 | 9.4840e-01 | ❌ No | [-0.1552, 0.0431] |
| gemma:latest_kb_rag vs nemotron-mini:4b_baseline | -0.2877 | 0.0000e+00 | ✅ Yes | [-0.3869, -0.1886] |
| gemma:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.1425 | 0.0000e+00 | ✅ Yes | [-0.2416, -0.0433] |
| gemma:latest_kb_rag vs qwen2.5:14b_baseline | -0.0114 | 1.0000e+00 | ❌ No | [-0.1106, 0.0877] |
| gemma:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0348 | 1.0000e+00 | ❌ No | [-0.0644, 0.1339] |
| gemma:latest_kb_rag vs qwen3:8b_baseline | -0.0315 | 1.0000e+00 | ❌ No | [-0.1307, 0.0676] |
| gemma:latest_kb_rag vs qwen3:8b_kb_rag | 0.0009 | 1.0000e+00 | ❌ No | [-0.0982, 0.1001] |
| gemma:latest_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.0490 | 9.9040e-01 | ❌ No | [-0.0501, 0.1482] |
| gemma:latest_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0828 | 2.8370e-01 | ❌ No | [-0.0163, 0.1820] |
| gpt-oss:20b_baseline vs gpt-oss:20b_kb_rag | -0.0965 | 6.9200e-02 | ❌ No | [-0.1957, 0.0026] |
| gpt-oss:20b_baseline vs llama3.1:8b_baseline | 0.0492 | 9.8990e-01 | ❌ No | [-0.0499, 0.1484] |
| gpt-oss:20b_baseline vs llama3.1:8b_kb_rag | 0.0691 | 6.8170e-01 | ❌ No | [-0.0301, 0.1682] |
| gpt-oss:20b_baseline vs llama3.2:latest_baseline | -0.0773 | 4.3310e-01 | ❌ No | [-0.1764, 0.0219] |
| gpt-oss:20b_baseline vs llama3.2:latest_kb_rag | 0.0310 | 1.0000e+00 | ❌ No | [-0.0682, 0.1301] |
| gpt-oss:20b_baseline vs mistral-nemo:latest_baseline | -0.0045 | 1.0000e+00 | ❌ No | [-0.1037, 0.0946] |
| gpt-oss:20b_baseline vs mistral-nemo:latest_kb_rag | 0.0192 | 1.0000e+00 | ❌ No | [-0.0800, 0.1183] |
| gpt-oss:20b_baseline vs nemotron-mini:4b_baseline | -0.2125 | 0.0000e+00 | ✅ Yes | [-0.3116, -0.1133] |
| gpt-oss:20b_baseline vs nemotron-mini:4b_kb_rag | -0.0672 | 7.3510e-01 | ❌ No | [-0.1664, 0.0319] |
| gpt-oss:20b_baseline vs qwen2.5:14b_baseline | 0.0638 | 8.2110e-01 | ❌ No | [-0.0353, 0.1630] |
| gpt-oss:20b_baseline vs qwen2.5:14b_kb_rag | 0.1100 | 1.1200e-02 | ✅ Yes | [0.0109, 0.2092] |
| gpt-oss:20b_baseline vs qwen3:8b_baseline | 0.0437 | 9.9830e-01 | ❌ No | [-0.0554, 0.1429] |
| gpt-oss:20b_baseline vs qwen3:8b_kb_rag | 0.0762 | 4.6490e-01 | ❌ No | [-0.0229, 0.1754] |
| gpt-oss:20b_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.1243 | 1.1000e-03 | ✅ Yes | [0.0251, 0.2234] |
| gpt-oss:20b_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.1581 | 0.0000e+00 | ✅ Yes | [0.0589, 0.2572] |
| gpt-oss:20b_kb_rag vs llama3.1:8b_baseline | 0.1457 | 0.0000e+00 | ✅ Yes | [0.0466, 0.2449] |
| gpt-oss:20b_kb_rag vs llama3.1:8b_kb_rag | 0.1656 | 0.0000e+00 | ✅ Yes | [0.0665, 0.2648] |
| gpt-oss:20b_kb_rag vs llama3.2:latest_baseline | 0.0192 | 1.0000e+00 | ❌ No | [-0.0799, 0.1184] |
| gpt-oss:20b_kb_rag vs llama3.2:latest_kb_rag | 0.1275 | 6.0000e-04 | ✅ Yes | [0.0283, 0.2266] |
| gpt-oss:20b_kb_rag vs mistral-nemo:latest_baseline | 0.0920 | 1.1650e-01 | ❌ No | [-0.0072, 0.1911] |
| gpt-oss:20b_kb_rag vs mistral-nemo:latest_kb_rag | 0.1157 | 4.7000e-03 | ✅ Yes | [0.0165, 0.2148] |
| gpt-oss:20b_kb_rag vs nemotron-mini:4b_baseline | -0.1160 | 4.5000e-03 | ✅ Yes | [-0.2151, -0.0168] |
| gpt-oss:20b_kb_rag vs nemotron-mini:4b_kb_rag | 0.0293 | 1.0000e+00 | ❌ No | [-0.0699, 0.1284] |
| gpt-oss:20b_kb_rag vs qwen2.5:14b_baseline | 0.1603 | 0.0000e+00 | ✅ Yes | [0.0612, 0.2595] |
| gpt-oss:20b_kb_rag vs qwen2.5:14b_kb_rag | 0.2065 | 0.0000e+00 | ✅ Yes | [0.1074, 0.3057] |
| gpt-oss:20b_kb_rag vs qwen3:8b_baseline | 0.1402 | 1.0000e-04 | ✅ Yes | [0.0411, 0.2394] |
| gpt-oss:20b_kb_rag vs qwen3:8b_kb_rag | 0.1727 | 0.0000e+00 | ✅ Yes | [0.0736, 0.2719] |
| gpt-oss:20b_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.2208 | 0.0000e+00 | ✅ Yes | [0.1217, 0.3200] |
| gpt-oss:20b_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.2546 | 0.0000e+00 | ✅ Yes | [0.1554, 0.3537] |
| llama3.1:8b_baseline vs llama3.1:8b_kb_rag | 0.0199 | 1.0000e+00 | ❌ No | [-0.0793, 0.1190] |
| llama3.1:8b_baseline vs llama3.2:latest_baseline | -0.1265 | 8.0000e-04 | ✅ Yes | [-0.2256, -0.0273] |
| llama3.1:8b_baseline vs llama3.2:latest_kb_rag | -0.0183 | 1.0000e+00 | ❌ No | [-0.1174, 0.0809] |
| llama3.1:8b_baseline vs mistral-nemo:latest_baseline | -0.0538 | 9.6830e-01 | ❌ No | [-0.1529, 0.0454] |
| llama3.1:8b_baseline vs mistral-nemo:latest_kb_rag | -0.0300 | 1.0000e+00 | ❌ No | [-0.1292, 0.0691] |
| llama3.1:8b_baseline vs nemotron-mini:4b_baseline | -0.2617 | 0.0000e+00 | ✅ Yes | [-0.3608, -0.1625] |
| llama3.1:8b_baseline vs nemotron-mini:4b_kb_rag | -0.1164 | 4.1000e-03 | ✅ Yes | [-0.2156, -0.0173] |
| llama3.1:8b_baseline vs qwen2.5:14b_baseline | 0.0146 | 1.0000e+00 | ❌ No | [-0.0846, 0.1137] |
| llama3.1:8b_baseline vs qwen2.5:14b_kb_rag | 0.0608 | 8.8240e-01 | ❌ No | [-0.0383, 0.1600] |
| llama3.1:8b_baseline vs qwen3:8b_baseline | -0.0055 | 1.0000e+00 | ❌ No | [-0.1047, 0.0936] |
| llama3.1:8b_baseline vs qwen3:8b_kb_rag | 0.0270 | 1.0000e+00 | ❌ No | [-0.0722, 0.1261] |
| llama3.1:8b_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.0751 | 4.9890e-01 | ❌ No | [-0.0241, 0.1742] |
| llama3.1:8b_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.1088 | 1.3300e-02 | ✅ Yes | [0.0097, 0.2080] |
| llama3.1:8b_kb_rag vs llama3.2:latest_baseline | -0.1464 | 0.0000e+00 | ✅ Yes | [-0.2455, -0.0472] |
| llama3.1:8b_kb_rag vs llama3.2:latest_kb_rag | -0.0381 | 9.9980e-01 | ❌ No | [-0.1373, 0.0610] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_baseline | -0.0736 | 5.4360e-01 | ❌ No | [-0.1728, 0.0255] |
| llama3.1:8b_kb_rag vs mistral-nemo:latest_kb_rag | -0.0499 | 9.8770e-01 | ❌ No | [-0.1491, 0.0492] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_baseline | -0.2816 | 0.0000e+00 | ✅ Yes | [-0.3807, -0.1824] |
| llama3.1:8b_kb_rag vs nemotron-mini:4b_kb_rag | -0.1363 | 1.0000e-04 | ✅ Yes | [-0.2355, -0.0372] |
| llama3.1:8b_kb_rag vs qwen2.5:14b_baseline | -0.0053 | 1.0000e+00 | ❌ No | [-0.1044, 0.0939] |
| llama3.1:8b_kb_rag vs qwen2.5:14b_kb_rag | 0.0409 | 9.9940e-01 | ❌ No | [-0.0582, 0.1401] |
| llama3.1:8b_kb_rag vs qwen3:8b_baseline | -0.0254 | 1.0000e+00 | ❌ No | [-0.1245, 0.0738] |
| llama3.1:8b_kb_rag vs qwen3:8b_kb_rag | 0.0071 | 1.0000e+00 | ❌ No | [-0.0920, 0.1063] |
| llama3.1:8b_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.0552 | 9.5670e-01 | ❌ No | [-0.0439, 0.1544] |
| llama3.1:8b_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0890 | 1.5990e-01 | ❌ No | [-0.0102, 0.1881] |
| llama3.2:latest_baseline vs llama3.2:latest_kb_rag | 0.1082 | 1.4500e-02 | ✅ Yes | [0.0091, 0.2074] |
| llama3.2:latest_baseline vs mistral-nemo:latest_baseline | 0.0727 | 5.7150e-01 | ❌ No | [-0.0264, 0.1719] |
| llama3.2:latest_baseline vs mistral-nemo:latest_kb_rag | 0.0964 | 6.9700e-02 | ❌ No | [-0.0027, 0.1956] |
| llama3.2:latest_baseline vs nemotron-mini:4b_baseline | -0.1352 | 2.0000e-04 | ✅ Yes | [-0.2343, -0.0360] |
| llama3.2:latest_baseline vs nemotron-mini:4b_kb_rag | 0.0101 | 1.0000e+00 | ❌ No | [-0.0891, 0.1092] |
| llama3.2:latest_baseline vs qwen2.5:14b_baseline | 0.1411 | 0.0000e+00 | ✅ Yes | [0.0419, 0.2402] |
| llama3.2:latest_baseline vs qwen2.5:14b_kb_rag | 0.1873 | 0.0000e+00 | ✅ Yes | [0.0881, 0.2864] |
| llama3.2:latest_baseline vs qwen3:8b_baseline | 0.1210 | 2.0000e-03 | ✅ Yes | [0.0218, 0.2201] |
| llama3.2:latest_baseline vs qwen3:8b_kb_rag | 0.1535 | 0.0000e+00 | ✅ Yes | [0.0543, 0.2526] |
| llama3.2:latest_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.2016 | 0.0000e+00 | ✅ Yes | [0.1024, 0.3007] |
| llama3.2:latest_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.2353 | 0.0000e+00 | ✅ Yes | [0.1362, 0.3345] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_baseline | -0.0355 | 1.0000e+00 | ❌ No | [-0.1346, 0.0637] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.0118 | 1.0000e+00 | ❌ No | [-0.1109, 0.0874] |
| llama3.2:latest_kb_rag vs nemotron-mini:4b_baseline | -0.2434 | 0.0000e+00 | ✅ Yes | [-0.3426, -0.1443] |
| llama3.2:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.0982 | 5.6500e-02 | ❌ No | [-0.1973, 0.0010] |
| llama3.2:latest_kb_rag vs qwen2.5:14b_baseline | 0.0329 | 1.0000e+00 | ❌ No | [-0.0663, 0.1320] |
| llama3.2:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0791 | 3.8140e-01 | ❌ No | [-0.0201, 0.1782] |
| llama3.2:latest_kb_rag vs qwen3:8b_baseline | 0.0127 | 1.0000e+00 | ❌ No | [-0.0864, 0.1119] |
| llama3.2:latest_kb_rag vs qwen3:8b_kb_rag | 0.0452 | 9.9710e-01 | ❌ No | [-0.0539, 0.1444] |
| llama3.2:latest_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.0933 | 1.0020e-01 | ❌ No | [-0.0058, 0.1925] |
| llama3.2:latest_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.1271 | 7.0000e-04 | ✅ Yes | [0.0280, 0.2262] |
| mistral-nemo:latest_baseline vs mistral-nemo:latest_kb_rag | 0.0237 | 1.0000e+00 | ❌ No | [-0.0754, 0.1229] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_baseline | -0.2079 | 0.0000e+00 | ✅ Yes | [-0.3071, -0.1088] |
| mistral-nemo:latest_baseline vs nemotron-mini:4b_kb_rag | -0.0627 | 8.4600e-01 | ❌ No | [-0.1618, 0.0365] |
| mistral-nemo:latest_baseline vs qwen2.5:14b_baseline | 0.0683 | 7.0330e-01 | ❌ No | [-0.0308, 0.1675] |
| mistral-nemo:latest_baseline vs qwen2.5:14b_kb_rag | 0.1146 | 5.6000e-03 | ✅ Yes | [0.0154, 0.2137] |
| mistral-nemo:latest_baseline vs qwen3:8b_baseline | 0.0482 | 9.9230e-01 | ❌ No | [-0.0509, 0.1474] |
| mistral-nemo:latest_baseline vs qwen3:8b_kb_rag | 0.0807 | 3.3590e-01 | ❌ No | [-0.0184, 0.1799] |
| mistral-nemo:latest_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.1288 | 5.0000e-04 | ✅ Yes | [0.0297, 0.2280] |
| mistral-nemo:latest_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.1626 | 0.0000e+00 | ✅ Yes | [0.0635, 0.2617] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_baseline | -0.2316 | 0.0000e+00 | ✅ Yes | [-0.3308, -0.1325] |
| mistral-nemo:latest_kb_rag vs nemotron-mini:4b_kb_rag | -0.0864 | 2.0580e-01 | ❌ No | [-0.1855, 0.0128] |
| mistral-nemo:latest_kb_rag vs qwen2.5:14b_baseline | 0.0446 | 9.9760e-01 | ❌ No | [-0.0545, 0.1438] |
| mistral-nemo:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0908 | 1.3160e-01 | ❌ No | [-0.0083, 0.1900] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_baseline | 0.0245 | 1.0000e+00 | ❌ No | [-0.0746, 0.1237] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_kb_rag | 0.0570 | 9.3810e-01 | ❌ No | [-0.0421, 0.1562] |
| mistral-nemo:latest_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.1051 | 2.2600e-02 | ✅ Yes | [0.0060, 0.2043] |
| mistral-nemo:latest_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.1389 | 1.0000e-04 | ✅ Yes | [0.0397, 0.2380] |
| nemotron-mini:4b_baseline vs nemotron-mini:4b_kb_rag | 0.1452 | 0.0000e+00 | ✅ Yes | [0.0461, 0.2444] |
| nemotron-mini:4b_baseline vs qwen2.5:14b_baseline | 0.2763 | 0.0000e+00 | ✅ Yes | [0.1771, 0.3754] |
| nemotron-mini:4b_baseline vs qwen2.5:14b_kb_rag | 0.3225 | 0.0000e+00 | ✅ Yes | [0.2233, 0.4216] |
| nemotron-mini:4b_baseline vs qwen3:8b_baseline | 0.2562 | 0.0000e+00 | ✅ Yes | [0.1570, 0.3553] |
| nemotron-mini:4b_baseline vs qwen3:8b_kb_rag | 0.2887 | 0.0000e+00 | ✅ Yes | [0.1895, 0.3878] |
| nemotron-mini:4b_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.3368 | 0.0000e+00 | ✅ Yes | [0.2376, 0.4359] |
| nemotron-mini:4b_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.3705 | 0.0000e+00 | ✅ Yes | [0.2714, 0.4697] |
| nemotron-mini:4b_kb_rag vs qwen2.5:14b_baseline | 0.1310 | 3.0000e-04 | ✅ Yes | [0.0319, 0.2302] |
| nemotron-mini:4b_kb_rag vs qwen2.5:14b_kb_rag | 0.1772 | 0.0000e+00 | ✅ Yes | [0.0781, 0.2764] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_baseline | 0.1109 | 9.8000e-03 | ✅ Yes | [0.0118, 0.2101] |
| nemotron-mini:4b_kb_rag vs qwen3:8b_kb_rag | 0.1434 | 0.0000e+00 | ✅ Yes | [0.0443, 0.2426] |
| nemotron-mini:4b_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.1915 | 0.0000e+00 | ✅ Yes | [0.0924, 0.2907] |
| nemotron-mini:4b_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.2253 | 0.0000e+00 | ✅ Yes | [0.1261, 0.3244] |
| qwen2.5:14b_baseline vs qwen2.5:14b_kb_rag | 0.0462 | 9.9590e-01 | ❌ No | [-0.0529, 0.1454] |
| qwen2.5:14b_baseline vs qwen3:8b_baseline | -0.0201 | 1.0000e+00 | ❌ No | [-0.1192, 0.0790] |
| qwen2.5:14b_baseline vs qwen3:8b_kb_rag | 0.0124 | 1.0000e+00 | ❌ No | [-0.0868, 0.1115] |
| qwen2.5:14b_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.0605 | 8.8810e-01 | ❌ No | [-0.0387, 0.1596] |
| qwen2.5:14b_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0943 | 9.0300e-02 | ❌ No | [-0.0049, 0.1934] |
| qwen2.5:14b_kb_rag vs qwen3:8b_baseline | -0.0663 | 7.5940e-01 | ❌ No | [-0.1655, 0.0328] |
| qwen2.5:14b_kb_rag vs qwen3:8b_kb_rag | -0.0338 | 1.0000e+00 | ❌ No | [-0.1330, 0.0653] |
| qwen2.5:14b_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.0143 | 1.0000e+00 | ❌ No | [-0.0849, 0.1134] |
| qwen2.5:14b_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0480 | 9.9280e-01 | ❌ No | [-0.0511, 0.1472] |
| qwen3:8b_baseline vs qwen3:8b_kb_rag | 0.0325 | 1.0000e+00 | ❌ No | [-0.0667, 0.1316] |
| qwen3:8b_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.0806 | 3.3990e-01 | ❌ No | [-0.0186, 0.1797] |
| qwen3:8b_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.1144 | 5.8000e-03 | ✅ Yes | [0.0152, 0.2135] |
| qwen3:8b_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.0481 | 9.9270e-01 | ❌ No | [-0.0511, 0.1472] |
| qwen3:8b_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0819 | 3.0700e-01 | ❌ No | [-0.0173, 0.1810] |
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0338 | 1.0000e+00 | ❌ No | [-0.0654, 0.1329] |

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
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.5627 | 0.5541 | -0.0085 | 📉 Decreased |
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.5964 | 0.5857 | -0.0108 | 📉 Decreased |
