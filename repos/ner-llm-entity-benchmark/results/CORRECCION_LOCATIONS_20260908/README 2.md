# Puntuación restringida a personas y organizaciones (N=120)

Recalculada el 2026-09-08 desde los `detailed_results.json` ya existentes, **sin reejecutar inferencia**.
Una corrida por grupo: la más reciente que aporta exactamente 120 registros.

El corpus no anota localizaciones —`fn_Locations` agregado = **0**— mientras los cuatro prompts las piden,
de modo que toda localización extraída era un falso positivo inevitable: **20946 de 32201 falsos positivos (65.0 %)**.
Como la exhaustividad de esa categoría no podía fallar, **el recall no varía**: la corrección es solo de precisión.

| Grupo | Corrida | P pub. | R | F1 pub. | P s/Loc | F1 s/Loc | Δ F1 |
|:--|:--|--:|--:|--:|--:|--:|--:|
| gemma4:31b-cloud_baseline | gemma4_31b_cloud_n120_REMOTO | 58.58 | 76.80 | 66.46 | 86.70 | 81.45 | +14.99 |
| gemma4:31b-cloud_kb_rag | gemma4_31b_cloud_n120_REMOTO | 57.29 | 76.50 | 65.52 | 83.19 | 79.71 | +14.19 |
| gemma4:31b-mlx_baseline | benchmark_balanced_120_20260901_140421 | 55.41 | 72.11 | 62.67 | 82.25 | 76.85 | +14.18 |
| gemma4:31b-mlx_kb_rag | benchmark_balanced_120_20260901_140421 | 55.77 | 72.77 | 63.15 | 80.72 | 76.54 | +13.39 |
| gemma4:31b-mlx_rag_enhanced | benchmark_balanced_120_20260824_173036 | 55.02 | 70.51 | 61.81 | 82.67 | 76.11 | +14.30 |
| zs-es | benchmark_balanced_120_20260825_071207 | 56.86 | 67.67 | 61.80 | 81.25 | 73.84 | +12.05 |
| gpt-oss:20b_kb_rag | gptoss_rerun_REMOTO | 51.89 | 70.04 | 59.61 | 77.81 | 73.72 | +14.11 |
| gemma4:latest_baseline | benchmark_balanced_120_20260901_140421 | 57.52 | 66.65 | 61.75 | 80.33 | 72.85 | +11.10 |
| gemma4:latest_kb_rag | benchmark_balanced_120_20260901_140421 | 55.07 | 64.71 | 59.50 | 82.55 | 72.55 | +13.05 |
| zs-en | benchmark_balanced_120_20260825_071207 | 56.75 | 64.47 | 60.36 | 80.39 | 71.56 | +11.20 |
| fs-es | benchmark_balanced_120_20260825_071207 | 54.37 | 62.29 | 58.06 | 83.37 | 71.30 | +13.24 |
| fs-en | benchmark_balanced_120_20260825_071207 | 54.38 | 62.33 | 58.09 | 81.98 | 70.82 | +12.73 |
| gemma4:latest_rag_enhanced | benchmark_balanced_120_20260824_173036 | 57.27 | 61.01 | 59.08 | 82.87 | 70.28 | +11.20 |
| gpt-oss:20b_baseline | gptoss_rerun_REMOTO | 49.19 | 64.92 | 55.97 | 76.21 | 70.11 | +14.14 |
| qwen2.5:14b_kb_rag | benchmark_balanced_120_20260901_140421 | 56.92 | 59.74 | 58.30 | 84.38 | 69.96 | +11.66 |
| qwen2.5:14b_baseline | benchmark_balanced_120_20260901_140421 | 53.54 | 55.26 | 54.39 | 85.59 | 67.16 | +12.77 |
| llama3.1:8b_baseline | benchmark_n120_REMOTO | 51.31 | 56.60 | 53.83 | 82.05 | 66.99 | +13.17 |
| llama3.1:8b_kb_rag | benchmark_n120_REMOTO | 54.66 | 57.06 | 55.83 | 79.45 | 66.42 | +10.59 |
| qwen3:8b_kb_rag | qwen3_nothink_n120_REMOTO | 49.82 | 60.35 | 54.59 | 72.80 | 65.99 | +11.41 |
| qwen3:8b_baseline | qwen3_nothink_n120_REMOTO | 48.49 | 56.41 | 52.15 | 76.29 | 64.86 | +12.71 |
| qwen2.5:14b_rag_enhanced | benchmark_balanced_120_20260824_173036 | 53.45 | 51.28 | 52.34 | 86.97 | 64.52 | +12.18 |
| llama3.2:latest_kb_rag | benchmark_balanced_120_20260901_140421 | 49.62 | 54.84 | 52.10 | 76.30 | 63.82 | +11.72 |
| llama3.1:8b_rag_enhanced | benchmark_balanced_120_20260824_173036 | 52.17 | 49.72 | 50.92 | 87.30 | 63.36 | +12.44 |
| gemma:latest_kb_rag | benchmark_balanced_120_20260901_140421 | 53.14 | 57.59 | 55.28 | 64.04 | 60.64 | +5.37 |
| mistral-nemo:latest_baseline | benchmark_n120_REMOTO | 56.28 | 43.58 | 49.12 | 84.92 | 57.60 | +8.48 |
| nuextract:latest_baseline | benchmark_n120_REMOTO | 49.92 | 45.30 | 47.50 | 78.35 | 57.41 | +9.91 |
| qwen3:8b_rag_enhanced | benchmark_balanced_120_20260824_173036 | 51.98 | 43.71 | 47.48 | 82.62 | 57.17 | +9.69 |
| mistral-nemo:latest_kb_rag | benchmark_n120_REMOTO | 60.16 | 43.14 | 50.25 | 83.61 | 56.92 | +6.67 |
| gemma:latest_baseline | benchmark_balanced_120_20260901_140421 | 49.51 | 46.42 | 47.91 | 68.63 | 55.38 | +7.46 |
| llama3.2:latest_baseline | benchmark_balanced_120_20260901_140421 | 43.29 | 38.91 | 40.98 | 82.54 | 52.89 | +11.91 |
| llama3.2:latest | benchmark_balanced_120_20260824_173017 | 43.29 | 38.91 | 40.98 | 82.54 | 52.89 | +11.91 |
| gemma:latest_rag_enhanced | benchmark_balanced_120_20260824_173036 | 49.87 | 40.04 | 44.42 | 71.36 | 51.30 | +6.88 |
| gemma4-12b-mlx-q8-64k:latest_baseline | benchmark_balanced_120_20260824_173036 | 58.14 | 30.98 | 40.42 | 85.52 | 45.48 | +5.06 |
| nemotron-mini:4b_kb_rag | nemotron_rerun_n120_REMOTO | 41.06 | 36.90 | 38.87 | 55.48 | 44.32 | +5.46 |
| llama3.2:latest_rag_enhanced | benchmark_balanced_120_20260824_173036 | 41.63 | 30.46 | 35.18 | 78.10 | 43.83 | +8.65 |
| gemma4:12b-mlx_baseline | benchmark_n120_REMOTO | 57.66 | 26.08 | 35.91 | 86.21 | 40.04 | +4.13 |
| mistral-nemo:latest_rag_enhanced | benchmark_balanced_120_20260824_173036 | 48.59 | 25.82 | 33.72 | 87.05 | 39.82 | +6.10 |
| gemma4:31b-cloud_rag_enhanced | benchmark_balanced_120_20260824_173036 | 62.47 | 20.78 | 31.19 | 92.14 | 33.91 | +2.73 |
| deepseek-r1:1.5b_baseline | benchmark_n120_REMOTO | 28.78 | 21.82 | 24.82 | 39.29 | 28.05 | +3.23 |
| gemma4-12b-mlx-q8-64k:latest_rag_enhanced | benchmark_balanced_120_20260824_173036 | 51.42 | 16.64 | 25.15 | 83.99 | 27.78 | +2.63 |
| deepseek-r1:1.5b_kb_rag | benchmark_n120_REMOTO | 27.63 | 22.15 | 24.59 | 37.06 | 27.73 | +3.14 |
| nemotron-mini:4b_baseline | nemotron_rerun_n120_REMOTO | 26.69 | 18.21 | 21.65 | 44.85 | 25.91 | +4.26 |
| nuextract:latest_kb_rag | benchmark_n120_REMOTO | 19.85 | 26.22 | 22.59 | 24.92 | 25.55 | +2.96 |
| nemotron-mini:4b_rag_enhanced | benchmark_balanced_120_20260824_173036 | 28.71 | 14.72 | 19.46 | 41.15 | 21.69 | +2.22 |
| nuextract:latest_rag_enhanced | benchmark_balanced_120_20260824_173036 | 21.20 | 16.68 | 18.67 | 30.10 | 21.46 | +2.79 |
| deepseek-r1:1.5b_rag_enhanced | benchmark_balanced_120_20260824_173036 | 21.48 | 14.74 | 17.48 | 29.07 | 19.56 | +2.08 |
| minimax-m3:cloud_baseline | benchmark_balanced_120_20260824_173036 | 48.44 | 8.63 | 14.65 | 76.54 | 15.51 | +0.86 |
| gemma4:12b-mlx_kb_rag | benchmark_n120_REMOTO | 51.72 | 8.50 | 14.60 | 83.92 | 15.43 | +0.84 |
| minimax-m3:cloud_rag_enhanced | benchmark_balanced_120_20260824_173036 | 51.93 | 6.65 | 11.79 | 81.74 | 12.30 | +0.51 |
