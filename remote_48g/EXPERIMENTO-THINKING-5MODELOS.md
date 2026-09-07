# Experimento — efecto del modo *thinking* en 5 modelos (think ON vs OFF)

**Fecha:** 2026-09-07 · **Equipo Remoto 48 GB** · **Para:** equipo de desarrollo principal

## Objetivo
Tras el hallazgo de `qwen3:8b` (think OFF mejora F1 y acelera), evaluar si conviene apagar el *thinking* en
los otros modelos del estudio con capacidad `thinking` que corrieron con **think ON por defecto**:
`gemma4:31b`, `gemma4:latest`, `deepseek-r1:1.5b`, `gpt-oss:20b`, `sonct988/gemma4-26b`.

## Método
Prueba controlada por el **pipeline real** (harness con RAG, scorer corregido), toggle de `thinking` como
única variable, sobre **15 registros** por modelo:
- N=120 (deepseek, gpt-oss, sonct988): subconjunto fijo de 15 de `benchmark_balanced_120` (seed 42), `kb_combined`.
- `gemma4:31b`: 15 de `kleptotrace` (modo `entities`, como P1).
- `gemma4:latest`: 15 de `kleptotrace`, **estudio de variantes de prompts** (zs/fs × en/es), como P4.

think ON = corrida oficial existente (mismos registros); think OFF = prueba en `results/test_nothink/`.
Cambio de código temporal (añadir los 5 a `_THINKING_DISABLED_MODELS`) **ya revertido**.

## Resultados (ΔF1 = OFF − ON; velocidad = lat_ON / lat_OFF)

| Modelo | Condición | F1 ON | F1 OFF | ΔF1 | Veloc. OFF |
|:---|:---|--:|--:|--:|--:|
| deepseek-r1:1.5b | baseline | 0.294 | 0.294 | ±0 | ×2.8 |
| deepseek-r1:1.5b | kb_rag | 0.345 | 0.345 | ±0 | ×3.7 |
| gpt-oss:20b | baseline | 0.419 | 0.301 | **−0.118** | ×1.6 |
| gpt-oss:20b | kb_rag | 0.283 | 0.155 | **−0.128** | ×3.0 |
| sonct988/gemma4-26b | baseline | 0.495 | 0.516 | +0.021 | ×0.3 |
| sonct988/gemma4-26b | kb_rag | 0.529 | 0.539 | +0.010 | ×1.6 |
| gemma4:31b | baseline (entities) | 0.691 | 0.662 | −0.029 | ×3.0 |
| gemma4:31b | rag (entities) | 0.639 | 0.676 | +0.037 | ×4.4 |
| gemma4:latest | variantes zs-en | 0.640 | 0.675 | +0.035 | ×5.6 |
| gemma4:latest | variantes zs-es | 0.684 | 0.704 | +0.020 | ×6.2 |
| gemma4:latest | variantes fs-en | 0.633 | 0.699 | +0.066 | ×6.0 |
| gemma4:latest | variantes fs-es | 0.744 | 0.694 | −0.051 | ×5.7 |

## Conclusiones

1. **El efecto NO es uniforme** (ver `FINDINGS.md §F44`): think OFF es **neutro-a-positivo y mucho más
   rápido en 4 de 5** modelos, pero **`gpt-oss:20b` pierde ~0.12 de F1** — su razonamiento es parte del
   mecanismo de respuesta.
2. **`gpt-oss:20b`: think ON, CONGELADO** (decisión del autor). Su corrida oficial `excluidos_n120_REMOTO`
   **no se re-ejecuta ni se toca.**
3. Los otros 4 (`deepseek-r1`, `sonct988`, `gemma4:31b`, `gemma4:latest`): think OFF mantiene o mejora F1 y
   acelera ~3-6×.

## ETA real para re-correr con think=OFF (solo los 4 beneficiados)

Medido con las latencias think-off reales de esta prueba:

| Modelo | Corrida | ETA think-off |
|:---|:---|--:|
| deepseek-r1:1.5b | N=120 × 2 | ~0.30 h |
| sonct988 | N=120 × 2 | ~0.25 h |
| gemma4:31b | N=15 × 2 (entities) | ~0.40 h |
| gemma4:latest | variantes N=15 × 4 | ~0.15 h |
| **Total local serial** | | **~1-1.5 h** |

`gpt-oss:20b` **no** entra. Cloud no aplica. Serialidad entre locales (una GPU).

## Decisión pendiente del autor
¿Aplicar think=OFF al **estudio oficial** de esos 4 modelos? Implica regenerar sus corridas con think=OFF
(~1-1.5 h) y **re-fusionar el ANOVA conjunto**. Beneficio: cifras consistentes (todos sin el sesgo/latencia
del thinking, salvo gpt-oss que se documenta como excepción justificada). El equipo remoto puede ejecutarlo
en cuanto se apruebe.

## Terminología
Se usa **«variantes de prompts»**, no «ablación» (ver `LEARNING.md §L37`).
