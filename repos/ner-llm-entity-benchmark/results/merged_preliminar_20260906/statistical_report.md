# 🔗 Merged Benchmark Analysis — Provenance & Integrity

- **Corpus:** `data/benchmark_balanced_120.json`
- **Registros esperados por modelo+modo:** 120
- **Corridas combinadas:** 3
- **Grupos (modelo+modo) analizados:** 18
- **Filas totales tras el merge:** 2160

## Fuentes
| # | Corrida | CSV | Filas | Modelos aportados |
| :---: | :--- | :--- | :---: | :---: |
| 1 | benchmark_balanced_120_20260901_140421 | `results/benchmark_balanced_120_20260901_140421/benchmark_results.csv` | 1200 | 10 |
| 2 | excluidos_n120_REMOTO | `/Users/eahumada/Documents/Personal/MTI/mti-pge-tesina-ner-llm-local/remote_48g/results/excluidos_n120_REMOTO/benchmark_results.csv` | 240 | 2 |
| 3 | merge_parcial | `/tmp/merge_parcial/benchmark_results.csv` | 720 | 6 |

## Integridad por grupo (modelo + modo)
| Modelo | Filas | record_id unicos | Esperados | f1 NaN | Estado |
| :--- | :---: | :---: | :---: | :---: | :---: |
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
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
| gemma4:12b-mlx_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| gemma4:12b-mlx_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
| qwen3:8b_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| qwen3:8b_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |
| mistral-nemo:latest_baseline | 120 | 120 | 120 | 0 | ✅ OK |
| mistral-nemo:latest_kb_rag | 120 | 120 | 120 | 0 | ✅ OK |

## Advertencias
- Ninguna. Corpus consistente, sin duplicados y todos los grupos completos.

---
# 📈 Statistical Validation Report

## 1. Analysis of Variance (ANOVA) - F1-Score
- **F-Statistic:** 64.0586
- **p-Value:** 7.2649e-177

> [!IMPORTANT]
> **Verdict:** The difference in performance between the evaluated models is **statistically significant** ($p < 0.05$). Pairwise post-hoc comparisons are required to identify the best model.

## 2. Model Performance Intervals (95% Confidence)
| Model | Sample Size (N) | Mean F1-Score | 95% CI Lower | 95% CI Upper | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| llama3.2:latest_baseline | 120 | 0.3945 | 0.3534 | 0.4355 | 0.2269 |
| llama3.2:latest_kb_rag | 120 | 0.4943 | 0.4566 | 0.5321 | 0.2087 |
| gemma4:latest_baseline | 120 | 0.5591 | 0.5229 | 0.5953 | 0.2004 |
| gemma4:latest_kb_rag | 120 | 0.5558 | 0.5181 | 0.5935 | 0.2085 |
| gemma4:31b-mlx_baseline | 120 | 0.5925 | 0.5575 | 0.6276 | 0.1937 |
| gemma4:31b-mlx_kb_rag | 120 | 0.5907 | 0.5516 | 0.6299 | 0.2167 |
| qwen2.5:14b_baseline | 120 | 0.5189 | 0.4849 | 0.5528 | 0.1879 |
| qwen2.5:14b_kb_rag | 120 | 0.5651 | 0.5309 | 0.5992 | 0.1890 |
| gemma:latest_baseline | 120 | 0.4734 | 0.4310 | 0.5157 | 0.2345 |
| gemma:latest_kb_rag | 120 | 0.5303 | 0.4919 | 0.5687 | 0.2126 |
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 120 | 0.5627 | 0.5278 | 0.5976 | 0.1932 |
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 120 | 0.5964 | 0.5624 | 0.6305 | 0.1881 |
| gemma4:12b-mlx_baseline | 120 | 0.0987 | 0.0523 | 0.1451 | 0.2568 |
| gemma4:12b-mlx_kb_rag | 120 | 0.0392 | 0.0083 | 0.0701 | 0.1710 |
| qwen3:8b_baseline | 120 | 0.4587 | 0.4196 | 0.4978 | 0.2165 |
| qwen3:8b_kb_rag | 120 | 0.4358 | 0.3831 | 0.4886 | 0.2917 |
| mistral-nemo:latest_baseline | 120 | 0.4651 | 0.4271 | 0.5032 | 0.2104 |
| mistral-nemo:latest_kb_rag | 120 | 0.4901 | 0.4511 | 0.5291 | 0.2157 |

## 3. Pairwise Post-Hoc Analysis (Tukey HSD / Pairwise t-test)
| Comparison | Mean Difference | Adjusted p-Value | Statistically Significant? | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:12b-mlx_baseline vs gemma4:12b-mlx_kb_rag | -0.0595 | 7.8350e-01 | ❌ No | [-0.1561, 0.0370] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_baseline | 0.4938 | 0.0000e+00 | ✅ Yes | [0.3973, 0.5904] |
| gemma4:12b-mlx_baseline vs gemma4:31b-mlx_kb_rag | 0.4920 | 0.0000e+00 | ✅ Yes | [0.3955, 0.5886] |
| gemma4:12b-mlx_baseline vs gemma4:latest_baseline | 0.4604 | 0.0000e+00 | ✅ Yes | [0.3639, 0.5569] |
| gemma4:12b-mlx_baseline vs gemma4:latest_kb_rag | 0.4570 | 0.0000e+00 | ✅ Yes | [0.3605, 0.5536] |
| gemma4:12b-mlx_baseline vs gemma:latest_baseline | 0.3746 | 0.0000e+00 | ✅ Yes | [0.2781, 0.4712] |
| gemma4:12b-mlx_baseline vs gemma:latest_kb_rag | 0.4316 | 0.0000e+00 | ✅ Yes | [0.3350, 0.5281] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_baseline | 0.2957 | 0.0000e+00 | ✅ Yes | [0.1992, 0.3923] |
| gemma4:12b-mlx_baseline vs llama3.2:latest_kb_rag | 0.3956 | 0.0000e+00 | ✅ Yes | [0.2991, 0.4922] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_baseline | 0.3664 | 0.0000e+00 | ✅ Yes | [0.2699, 0.4629] |
| gemma4:12b-mlx_baseline vs mistral-nemo:latest_kb_rag | 0.3914 | 0.0000e+00 | ✅ Yes | [0.2948, 0.4879] |
| gemma4:12b-mlx_baseline vs qwen2.5:14b_baseline | 0.4201 | 0.0000e+00 | ✅ Yes | [0.3236, 0.5167] |
| gemma4:12b-mlx_baseline vs qwen2.5:14b_kb_rag | 0.4663 | 0.0000e+00 | ✅ Yes | [0.3698, 0.5629] |
| gemma4:12b-mlx_baseline vs qwen3:8b_baseline | 0.3600 | 0.0000e+00 | ✅ Yes | [0.2634, 0.4565] |
| gemma4:12b-mlx_baseline vs qwen3:8b_kb_rag | 0.3371 | 0.0000e+00 | ✅ Yes | [0.2406, 0.4336] |
| gemma4:12b-mlx_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.4640 | 0.0000e+00 | ✅ Yes | [0.3674, 0.5605] |
| gemma4:12b-mlx_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.4977 | 0.0000e+00 | ✅ Yes | [0.4012, 0.5943] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_baseline | 0.5534 | 0.0000e+00 | ✅ Yes | [0.4568, 0.6499] |
| gemma4:12b-mlx_kb_rag vs gemma4:31b-mlx_kb_rag | 0.5516 | 0.0000e+00 | ✅ Yes | [0.4550, 0.6481] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_baseline | 0.5199 | 0.0000e+00 | ✅ Yes | [0.4234, 0.6165] |
| gemma4:12b-mlx_kb_rag vs gemma4:latest_kb_rag | 0.5166 | 0.0000e+00 | ✅ Yes | [0.4200, 0.6131] |
| gemma4:12b-mlx_kb_rag vs gemma:latest_baseline | 0.4342 | 0.0000e+00 | ✅ Yes | [0.3376, 0.5307] |
| gemma4:12b-mlx_kb_rag vs gemma:latest_kb_rag | 0.4911 | 0.0000e+00 | ✅ Yes | [0.3946, 0.5877] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_baseline | 0.3553 | 0.0000e+00 | ✅ Yes | [0.2587, 0.4518] |
| gemma4:12b-mlx_kb_rag vs llama3.2:latest_kb_rag | 0.4552 | 0.0000e+00 | ✅ Yes | [0.3586, 0.5517] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_baseline | 0.4259 | 0.0000e+00 | ✅ Yes | [0.3294, 0.5225] |
| gemma4:12b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | 0.4509 | 0.0000e+00 | ✅ Yes | [0.3544, 0.5475] |
| gemma4:12b-mlx_kb_rag vs qwen2.5:14b_baseline | 0.4797 | 0.0000e+00 | ✅ Yes | [0.3831, 0.5762] |
| gemma4:12b-mlx_kb_rag vs qwen2.5:14b_kb_rag | 0.5259 | 0.0000e+00 | ✅ Yes | [0.4293, 0.6224] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_baseline | 0.4195 | 0.0000e+00 | ✅ Yes | [0.3230, 0.5161] |
| gemma4:12b-mlx_kb_rag vs qwen3:8b_kb_rag | 0.3966 | 0.0000e+00 | ✅ Yes | [0.3001, 0.4932] |
| gemma4:12b-mlx_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.5235 | 0.0000e+00 | ✅ Yes | [0.4270, 0.6200] |
| gemma4:12b-mlx_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.5573 | 0.0000e+00 | ✅ Yes | [0.4607, 0.6538] |
| gemma4:31b-mlx_baseline vs gemma4:31b-mlx_kb_rag | -0.0018 | 1.0000e+00 | ❌ No | [-0.0983, 0.0947] |
| gemma4:31b-mlx_baseline vs gemma4:latest_baseline | -0.0334 | 9.9930e-01 | ❌ No | [-0.1300, 0.0631] |
| gemma4:31b-mlx_baseline vs gemma4:latest_kb_rag | -0.0368 | 9.9760e-01 | ❌ No | [-0.1333, 0.0598] |
| gemma4:31b-mlx_baseline vs gemma:latest_baseline | -0.1192 | 2.3000e-03 | ✅ Yes | [-0.2157, -0.0226] |
| gemma4:31b-mlx_baseline vs gemma:latest_kb_rag | -0.0622 | 7.1790e-01 | ❌ No | [-0.1588, 0.0343] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_baseline | -0.1981 | 0.0000e+00 | ✅ Yes | [-0.2946, -0.1016] |
| gemma4:31b-mlx_baseline vs llama3.2:latest_kb_rag | -0.0982 | 4.1100e-02 | ✅ Yes | [-0.1947, -0.0017] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_baseline | -0.1274 | 6.0000e-04 | ✅ Yes | [-0.2240, -0.0309] |
| gemma4:31b-mlx_baseline vs mistral-nemo:latest_kb_rag | -0.1025 | 2.4300e-02 | ✅ Yes | [-0.1990, -0.0059] |
| gemma4:31b-mlx_baseline vs qwen2.5:14b_baseline | -0.0737 | 4.0510e-01 | ❌ No | [-0.1702, 0.0229] |
| gemma4:31b-mlx_baseline vs qwen2.5:14b_kb_rag | -0.0275 | 9.9990e-01 | ❌ No | [-0.1240, 0.0691] |
| gemma4:31b-mlx_baseline vs qwen3:8b_baseline | -0.1338 | 2.0000e-04 | ✅ Yes | [-0.2304, -0.0373] |
| gemma4:31b-mlx_baseline vs qwen3:8b_kb_rag | -0.1567 | 0.0000e+00 | ✅ Yes | [-0.2533, -0.0602] |
| gemma4:31b-mlx_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | -0.0299 | 9.9980e-01 | ❌ No | [-0.1264, 0.0667] |
| gemma4:31b-mlx_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0039 | 1.0000e+00 | ❌ No | [-0.0926, 0.1004] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_baseline | -0.0316 | 9.9960e-01 | ❌ No | [-0.1282, 0.0649] |
| gemma4:31b-mlx_kb_rag vs gemma4:latest_kb_rag | -0.0350 | 9.9870e-01 | ❌ No | [-0.1315, 0.0616] |
| gemma4:31b-mlx_kb_rag vs gemma:latest_baseline | -0.1174 | 3.0000e-03 | ✅ Yes | [-0.2139, -0.0208] |
| gemma4:31b-mlx_kb_rag vs gemma:latest_kb_rag | -0.0604 | 7.6240e-01 | ❌ No | [-0.1570, 0.0361] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_baseline | -0.1963 | 0.0000e+00 | ✅ Yes | [-0.2928, -0.0998] |
| gemma4:31b-mlx_kb_rag vs llama3.2:latest_kb_rag | -0.0964 | 5.0800e-02 | ❌ No | [-0.1929, 0.0001] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_baseline | -0.1256 | 8.0000e-04 | ✅ Yes | [-0.2222, -0.0291] |
| gemma4:31b-mlx_kb_rag vs mistral-nemo:latest_kb_rag | -0.1006 | 3.0500e-02 | ✅ Yes | [-0.1972, -0.0041] |
| gemma4:31b-mlx_kb_rag vs qwen2.5:14b_baseline | -0.0719 | 4.5330e-01 | ❌ No | [-0.1684, 0.0247] |
| gemma4:31b-mlx_kb_rag vs qwen2.5:14b_kb_rag | -0.0257 | 1.0000e+00 | ❌ No | [-0.1222, 0.0709] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_baseline | -0.1320 | 3.0000e-04 | ✅ Yes | [-0.2286, -0.0355] |
| gemma4:31b-mlx_kb_rag vs qwen3:8b_kb_rag | -0.1549 | 0.0000e+00 | ✅ Yes | [-0.2515, -0.0584] |
| gemma4:31b-mlx_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | -0.0281 | 9.9990e-01 | ❌ No | [-0.1246, 0.0685] |
| gemma4:31b-mlx_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0057 | 1.0000e+00 | ❌ No | [-0.0908, 0.1022] |
| gemma4:latest_baseline vs gemma4:latest_kb_rag | -0.0034 | 1.0000e+00 | ❌ No | [-0.0999, 0.0932] |
| gemma4:latest_baseline vs gemma:latest_baseline | -0.0858 | 1.5520e-01 | ❌ No | [-0.1823, 0.0108] |
| gemma4:latest_baseline vs gemma:latest_kb_rag | -0.0288 | 9.9990e-01 | ❌ No | [-0.1254, 0.0677] |
| gemma4:latest_baseline vs llama3.2:latest_baseline | -0.1647 | 0.0000e+00 | ✅ Yes | [-0.2612, -0.0681] |
| gemma4:latest_baseline vs llama3.2:latest_kb_rag | -0.0648 | 6.5080e-01 | ❌ No | [-0.1613, 0.0318] |
| gemma4:latest_baseline vs mistral-nemo:latest_baseline | -0.0940 | 6.6800e-02 | ❌ No | [-0.1905, 0.0025] |
| gemma4:latest_baseline vs mistral-nemo:latest_kb_rag | -0.0690 | 5.3240e-01 | ❌ No | [-0.1656, 0.0275] |
| gemma4:latest_baseline vs qwen2.5:14b_baseline | -0.0403 | 9.9330e-01 | ❌ No | [-0.1368, 0.0563] |
| gemma4:latest_baseline vs qwen2.5:14b_kb_rag | 0.0059 | 1.0000e+00 | ❌ No | [-0.0906, 0.1025] |
| gemma4:latest_baseline vs qwen3:8b_baseline | -0.1004 | 3.1400e-02 | ✅ Yes | [-0.1970, -0.0039] |
| gemma4:latest_baseline vs qwen3:8b_kb_rag | -0.1233 | 1.2000e-03 | ✅ Yes | [-0.2198, -0.0268] |
| gemma4:latest_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.0036 | 1.0000e+00 | ❌ No | [-0.0930, 0.1001] |
| gemma4:latest_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0373 | 9.9720e-01 | ❌ No | [-0.0592, 0.1339] |
| gemma4:latest_kb_rag vs gemma:latest_baseline | -0.0824 | 2.1000e-01 | ❌ No | [-0.1789, 0.0141] |
| gemma4:latest_kb_rag vs gemma:latest_kb_rag | -0.0255 | 1.0000e+00 | ❌ No | [-0.1220, 0.0711] |
| gemma4:latest_kb_rag vs llama3.2:latest_baseline | -0.1613 | 0.0000e+00 | ✅ Yes | [-0.2579, -0.0648] |
| gemma4:latest_kb_rag vs llama3.2:latest_kb_rag | -0.0614 | 7.3880e-01 | ❌ No | [-0.1580, 0.0351] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_baseline | -0.0906 | 9.6000e-02 | ❌ No | [-0.1872, 0.0059] |
| gemma4:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.0657 | 6.2650e-01 | ❌ No | [-0.1622, 0.0309] |
| gemma4:latest_kb_rag vs qwen2.5:14b_baseline | -0.0369 | 9.9750e-01 | ❌ No | [-0.1334, 0.0596] |
| gemma4:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0093 | 1.0000e+00 | ❌ No | [-0.0872, 0.1059] |
| gemma4:latest_kb_rag vs qwen3:8b_baseline | -0.0970 | 4.7100e-02 | ✅ Yes | [-0.1936, -0.0005] |
| gemma4:latest_kb_rag vs qwen3:8b_kb_rag | -0.1199 | 2.0000e-03 | ✅ Yes | [-0.2165, -0.0234] |
| gemma4:latest_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.0069 | 1.0000e+00 | ❌ No | [-0.0896, 0.1035] |
| gemma4:latest_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0407 | 9.9240e-01 | ❌ No | [-0.0559, 0.1372] |
| gemma:latest_baseline vs gemma:latest_kb_rag | 0.0569 | 8.3870e-01 | ❌ No | [-0.0396, 0.1535] |
| gemma:latest_baseline vs llama3.2:latest_baseline | -0.0789 | 2.7940e-01 | ❌ No | [-0.1755, 0.0176] |
| gemma:latest_baseline vs llama3.2:latest_kb_rag | 0.0210 | 1.0000e+00 | ❌ No | [-0.0756, 0.1175] |
| gemma:latest_baseline vs mistral-nemo:latest_baseline | -0.0082 | 1.0000e+00 | ❌ No | [-0.1048, 0.0883] |
| gemma:latest_baseline vs mistral-nemo:latest_kb_rag | 0.0167 | 1.0000e+00 | ❌ No | [-0.0798, 0.1133] |
| gemma:latest_baseline vs qwen2.5:14b_baseline | 0.0455 | 9.7560e-01 | ❌ No | [-0.0510, 0.1420] |
| gemma:latest_baseline vs qwen2.5:14b_kb_rag | 0.0917 | 8.5600e-02 | ❌ No | [-0.0048, 0.1883] |
| gemma:latest_baseline vs qwen3:8b_baseline | -0.0146 | 1.0000e+00 | ❌ No | [-0.1112, 0.0819] |
| gemma:latest_baseline vs qwen3:8b_kb_rag | -0.0375 | 9.9700e-01 | ❌ No | [-0.1341, 0.0590] |
| gemma:latest_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.0893 | 1.0980e-01 | ❌ No | [-0.0072, 0.1859] |
| gemma:latest_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.1231 | 1.2000e-03 | ✅ Yes | [0.0265, 0.2196] |
| gemma:latest_kb_rag vs llama3.2:latest_baseline | -0.1359 | 1.0000e-04 | ✅ Yes | [-0.2324, -0.0393] |
| gemma:latest_kb_rag vs llama3.2:latest_kb_rag | -0.0360 | 9.9820e-01 | ❌ No | [-0.1325, 0.0606] |
| gemma:latest_kb_rag vs mistral-nemo:latest_baseline | -0.0652 | 6.4020e-01 | ❌ No | [-0.1617, 0.0314] |
| gemma:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.0402 | 9.9340e-01 | ❌ No | [-0.1367, 0.0563] |
| gemma:latest_kb_rag vs qwen2.5:14b_baseline | -0.0114 | 1.0000e+00 | ❌ No | [-0.1080, 0.0851] |
| gemma:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0348 | 9.9880e-01 | ❌ No | [-0.0618, 0.1313] |
| gemma:latest_kb_rag vs qwen3:8b_baseline | -0.0716 | 4.6140e-01 | ❌ No | [-0.1681, 0.0250] |
| gemma:latest_kb_rag vs qwen3:8b_kb_rag | -0.0945 | 6.3300e-02 | ❌ No | [-0.1910, 0.0021] |
| gemma:latest_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.0324 | 9.9950e-01 | ❌ No | [-0.0642, 0.1289] |
| gemma:latest_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0661 | 6.1330e-01 | ❌ No | [-0.0304, 0.1627] |
| llama3.2:latest_baseline vs llama3.2:latest_kb_rag | 0.0999 | 3.3500e-02 | ✅ Yes | [0.0034, 0.1964] |
| llama3.2:latest_baseline vs mistral-nemo:latest_baseline | 0.0707 | 4.8620e-01 | ❌ No | [-0.0259, 0.1672] |
| llama3.2:latest_baseline vs mistral-nemo:latest_kb_rag | 0.0956 | 5.5400e-02 | ❌ No | [-0.0009, 0.1922] |
| llama3.2:latest_baseline vs qwen2.5:14b_baseline | 0.1244 | 1.0000e-03 | ✅ Yes | [0.0279, 0.2210] |
| llama3.2:latest_baseline vs qwen2.5:14b_kb_rag | 0.1706 | 0.0000e+00 | ✅ Yes | [0.0741, 0.2672] |
| llama3.2:latest_baseline vs qwen3:8b_baseline | 0.0643 | 6.6480e-01 | ❌ No | [-0.0323, 0.1608] |
| llama3.2:latest_baseline vs qwen3:8b_kb_rag | 0.0414 | 9.9090e-01 | ❌ No | [-0.0552, 0.1379] |
| llama3.2:latest_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.1682 | 0.0000e+00 | ✅ Yes | [0.0717, 0.2648] |
| llama3.2:latest_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.2020 | 0.0000e+00 | ✅ Yes | [0.1055, 0.2985] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_baseline | -0.0292 | 9.9990e-01 | ❌ No | [-0.1258, 0.0673] |
| llama3.2:latest_kb_rag vs mistral-nemo:latest_kb_rag | -0.0042 | 1.0000e+00 | ❌ No | [-0.1008, 0.0923] |
| llama3.2:latest_kb_rag vs qwen2.5:14b_baseline | 0.0245 | 1.0000e+00 | ❌ No | [-0.0720, 0.1211] |
| llama3.2:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0707 | 4.8490e-01 | ❌ No | [-0.0258, 0.1673] |
| llama3.2:latest_kb_rag vs qwen3:8b_baseline | -0.0356 | 9.9840e-01 | ❌ No | [-0.1322, 0.0609] |
| llama3.2:latest_kb_rag vs qwen3:8b_kb_rag | -0.0585 | 8.0610e-01 | ❌ No | [-0.1551, 0.0380] |
| llama3.2:latest_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.0683 | 5.5190e-01 | ❌ No | [-0.0282, 0.1649] |
| llama3.2:latest_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.1021 | 2.5400e-02 | ✅ Yes | [0.0056, 0.1986] |
| mistral-nemo:latest_baseline vs mistral-nemo:latest_kb_rag | 0.0250 | 1.0000e+00 | ❌ No | [-0.0716, 0.1215] |
| mistral-nemo:latest_baseline vs qwen2.5:14b_baseline | 0.0537 | 8.9460e-01 | ❌ No | [-0.0428, 0.1503] |
| mistral-nemo:latest_baseline vs qwen2.5:14b_kb_rag | 0.0999 | 3.3300e-02 | ✅ Yes | [0.0034, 0.1965] |
| mistral-nemo:latest_baseline vs qwen3:8b_baseline | -0.0064 | 1.0000e+00 | ❌ No | [-0.1030, 0.0901] |
| mistral-nemo:latest_baseline vs qwen3:8b_kb_rag | -0.0293 | 9.9990e-01 | ❌ No | [-0.1259, 0.0672] |
| mistral-nemo:latest_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.0975 | 4.4400e-02 | ✅ Yes | [0.0010, 0.1941] |
| mistral-nemo:latest_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.1313 | 3.0000e-04 | ✅ Yes | [0.0348, 0.2279] |
| mistral-nemo:latest_kb_rag vs qwen2.5:14b_baseline | 0.0288 | 9.9990e-01 | ❌ No | [-0.0678, 0.1253] |
| mistral-nemo:latest_kb_rag vs qwen2.5:14b_kb_rag | 0.0750 | 3.7190e-01 | ❌ No | [-0.0216, 0.1715] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_baseline | -0.0314 | 9.9970e-01 | ❌ No | [-0.1279, 0.0652] |
| mistral-nemo:latest_kb_rag vs qwen3:8b_kb_rag | -0.0543 | 8.8610e-01 | ❌ No | [-0.1508, 0.0423] |
| mistral-nemo:latest_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.0726 | 4.3430e-01 | ❌ No | [-0.0240, 0.1691] |
| mistral-nemo:latest_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.1063 | 1.4600e-02 | ✅ Yes | [0.0098, 0.2029] |
| qwen2.5:14b_baseline vs qwen2.5:14b_kb_rag | 0.0462 | 9.7160e-01 | ❌ No | [-0.0503, 0.1428] |
| qwen2.5:14b_baseline vs qwen3:8b_baseline | -0.0601 | 7.6950e-01 | ❌ No | [-0.1567, 0.0364] |
| qwen2.5:14b_baseline vs qwen3:8b_kb_rag | -0.0830 | 1.9870e-01 | ❌ No | [-0.1796, 0.0135] |
| qwen2.5:14b_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.0438 | 9.8330e-01 | ❌ No | [-0.0527, 0.1404] |
| qwen2.5:14b_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0776 | 3.0900e-01 | ❌ No | [-0.0190, 0.1741] |
| qwen2.5:14b_kb_rag vs qwen3:8b_baseline | -0.1064 | 1.4600e-02 | ✅ Yes | [-0.2029, -0.0098] |
| qwen2.5:14b_kb_rag vs qwen3:8b_kb_rag | -0.1293 | 4.0000e-04 | ✅ Yes | [-0.2258, -0.0327] |
| qwen2.5:14b_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | -0.0024 | 1.0000e+00 | ❌ No | [-0.0989, 0.0941] |
| qwen2.5:14b_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0314 | 9.9970e-01 | ❌ No | [-0.0652, 0.1279] |
| qwen3:8b_baseline vs qwen3:8b_kb_rag | -0.0229 | 1.0000e+00 | ❌ No | [-0.1194, 0.0736] |
| qwen3:8b_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.1040 | 2.0000e-02 | ✅ Yes | [0.0074, 0.2005] |
| qwen3:8b_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.1377 | 1.0000e-04 | ✅ Yes | [0.0412, 0.2343] |
| qwen3:8b_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.1269 | 7.0000e-04 | ✅ Yes | [0.0303, 0.2234] |
| qwen3:8b_kb_rag vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.1606 | 0.0000e+00 | ✅ Yes | [0.0641, 0.2572] |
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline vs sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.0338 | 9.9920e-01 | ❌ No | [-0.0628, 0.1303] |

## 4. Sensitivity Analysis (Outlier Filtering)
- **Difficulty Criteria:** Article length > 2610.3 characters.
- **Outlier Records Identified:** 14 records.

| Model | Standard F1 | Cleaned F1 (Filtered Outliers) | F1-Score Delta | Status |
| :--- | :---: | :---: | :---: | :---: |
| gemma4:12b-mlx_baseline | 0.0987 | 0.1118 | +0.0130 | 📈 Improved |
| gemma4:12b-mlx_kb_rag | 0.0392 | 0.0444 | +0.0052 | 📈 Improved |
| gemma4:31b-mlx_baseline | 0.5925 | 0.5813 | -0.0112 | 📉 Decreased |
| gemma4:31b-mlx_kb_rag | 0.5907 | 0.5836 | -0.0072 | 📉 Decreased |
| gemma4:latest_baseline | 0.5591 | 0.5434 | -0.0157 | 📉 Decreased |
| gemma4:latest_kb_rag | 0.5558 | 0.5464 | -0.0093 | 📉 Decreased |
| gemma:latest_baseline | 0.4734 | 0.4593 | -0.0141 | 📉 Decreased |
| gemma:latest_kb_rag | 0.5303 | 0.5134 | -0.0169 | 📉 Decreased |
| llama3.2:latest_baseline | 0.3945 | 0.3718 | -0.0227 | 📉 Decreased |
| llama3.2:latest_kb_rag | 0.4943 | 0.4832 | -0.0111 | 📉 Decreased |
| mistral-nemo:latest_baseline | 0.4651 | 0.4474 | -0.0178 | 📉 Decreased |
| mistral-nemo:latest_kb_rag | 0.4901 | 0.4738 | -0.0163 | 📉 Decreased |
| qwen2.5:14b_baseline | 0.5189 | 0.5062 | -0.0127 | 📉 Decreased |
| qwen2.5:14b_kb_rag | 0.5651 | 0.5504 | -0.0147 | 📉 Decreased |
| qwen3:8b_baseline | 0.4587 | 0.4614 | +0.0027 | 📈 Improved |
| qwen3:8b_kb_rag | 0.4358 | 0.4476 | +0.0117 | 📈 Improved |
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest_baseline | 0.5627 | 0.5541 | -0.0085 | 📉 Decreased |
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest_kb_rag | 0.5964 | 0.5857 | -0.0108 | 📉 Decreased |
