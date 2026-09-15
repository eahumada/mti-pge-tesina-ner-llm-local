# R5: Análisis de Variantes de Prompts 2×2 sobre Par Emparejado N=30
**Generado:** 2026-09-15 · **Modelo:** `gemma4:latest` · **Semillas:** [42, 123, 456, 789, 1024]

## Resumen Comparativo (Media ± Desviación Estándar)

| Corpus (Idioma Texto) | Condición Prompt | F1 (μ ± σ) | Precisión | Exhaustividad |
|:---|:---|:---:|:---:|:---:|
| Inglés (kleptotrace_augmented_30) | `fs-es` | **0.8603 ± 0.0071** | 0.8256 | 0.9330 |
| Inglés (kleptotrace_augmented_30) | `zs-es` | **0.8406 ± 0.0070** | 0.8299 | 0.8849 |
| Inglés (kleptotrace_augmented_30) | `fs-en` | **0.8753 ± 0.0095** | 0.8357 | 0.9477 |
| Inglés (kleptotrace_augmented_30) | `zs-en` | **0.8735 ± 0.0015** | 0.8701 | 0.9135 |
| Español (kleptotrace_augmented_30_es) | `fs-es` | **0.8760 ± 0.0081** | 0.8434 | 0.9414 |
| Español (kleptotrace_augmented_30_es) | `zs-es` | **0.8765 ± 0.0108** | 0.8735 | 0.9129 |
| Español (kleptotrace_augmented_30_es) | `fs-en` | **0.8619 ± 0.0086** | 0.8353 | 0.9240 |
| Español (kleptotrace_augmented_30_es) | `zs-en` | **0.8718 ± 0.0059** | 0.8726 | 0.9065 |

## Matriz Factorial 2×2×2 (Idioma Texto × Idioma Prompt × Exemplars)

| Texto | Prompt Lang | Modo | F1 Promedio |
|:---|:---:|:---:|---:|
| Inglés | Español | Few-Shot | 0.8603 |
| Inglés | Español | Zero-Shot | 0.8406 |
| Inglés | Inglés | Few-Shot | 0.8753 |
| Inglés | Inglés | Zero-Shot | 0.8735 |
| Español | Español | Few-Shot | 0.8760 |
| Español | Español | Zero-Shot | 0.8765 |
| Español | Inglés | Few-Shot | 0.8619 |
| Español | Inglés | Zero-Shot | 0.8718 |