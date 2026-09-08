# Estado de la re-corrida completa

**Actualizado: 2026-09-08 20:52.** Regenerar con `python3 tools/estado_recorrida.py`; no editar a mano.

Todas las corridas listadas han pasado las cinco verificaciones del protocolo —cero
`parse_method='failed'`, cero violaciones de `F1 ≤ (P+R)/2`, cero rechazos de infraestructura— y
llevan la firma del corpus corregido **1098 / 1500 / 1034** en N=120. Las cifras se toman de
`benchmark_summary.json`, que publica sobre **113** registros: los siete artículos contaminados se
descuentan (`FINDINGS §F65`).

## N=120, frente a lo publicado

| Modelo | Publicado base / RAG | Re-corrida base / RAG | Δ publicado | Δ re-corrida | Signo |
|:---|:---|:---|---:|---:|:---:|
| `gemma4:31b-cloud` | 62.38 / 61.85 | **82.13 / 82.94** | -0.53 | +0.81 | **cambia** |
| `gemma4:31b-mlx` | 59.25 / 59.07 | **81.47 / 82.44** | -0.18 | +0.97 | **cambia** |
| `gemma4:12b-mlx` | 56.18 / 58.46 | **77.67 / 79.96** | +2.28 | +2.29 | igual |
| `gemma4:latest` | 55.91 / 54.74 | **75.33 / 77.86** | -1.17 | +2.53 | **cambia** |
| `gpt-oss:20b` | 52.39 / 55.67 | *pendiente* | +3.28 | — | — |
| `qwen2.5:14b` | 50.22 / 54.84 | **69.61 / 70.31** | +4.62 | +0.69 | igual |
| `llama3.1:8b` | 48.76 / 50.75 | **69.17 / 71.48** | +1.99 | +2.31 | igual |
| `qwen3:8b` | 48.21 / 51.46 | **69.03 / 68.98** | +3.25 | -0.05 | **cambia** |
| `gemma:latest` | 44.00 / 51.36 | *pendiente* | +7.36 | — | — |
| `mistral-nemo:latest` | 43.38 / 45.76 | *pendiente* | +2.38 | — | — |
| `llama3.2:latest` | 36.11 / 46.93 | *pendiente* | +10.82 | — | — |
| `deepseek-r1:1.5b` | 24.83 / 23.94 | *pendiente* | -0.89 | — | — |
| `nemotron-mini:4b` | 22.59 / 37.12 | *pendiente* | +14.53 | — | — |

**7 de 13 modelos** rehechos en N=120. **4 cambian el signo** del efecto del RAG.

## N=30 y N=15

| Modelo | N=30 base / RAG | N=15 base / RAG |
|:---|:---|:---|
| `gemma4:31b-cloud` | 88.04 / 85.73 | 77.45 / 80.51 |
| `gemma4:31b-mlx` | 85.60 / 85.51 | 77.92 / 80.31 |
| `gemma4:12b-mlx` | 89.83 / 86.30 | 73.62 / 76.84 |
| `gemma4:latest` | 87.30 / 85.56 | 71.77 / 79.59 |
| `qwen2.5:14b` | 84.46 / 86.62 | 68.41 / 70.00 |
| `llama3.1:8b` | 80.96 / 82.67 | 68.60 / 73.34 |
| `qwen3:8b` | 76.85 / 79.97 | 67.68 / 73.04 |

## Avance del barrido

Según `results/recorrida_20260908/_sweep_progress.log`, congelado en el último commit del equipo
de 48 GB:

```
[16:42:23] ===== MASTER SWEEP START =====
[16:42:23] START gemma4:12b-mlx N120
[17:00:35] END   gemma4:12b-mlx N120 rc=0
[17:00:35] SKIP gemma4:12b-mlx N30 (ya existe)
[17:00:35] SKIP gemma4:12b-mlx N15 (ya existe)
[17:00:35] START gemma4:31b-mlx N120
[17:45:57] END   gemma4:31b-mlx N120 rc=0
[17:45:57] START gemma4:31b-mlx N30
[17:49:15] END   gemma4:31b-mlx N30 rc=0
[17:49:15] START gemma4:31b-mlx N15
[17:58:48] END   gemma4:31b-mlx N15 rc=0
[17:58:48] START gemma4:latest N120
[19:13:17] END   gemma4:latest N120 rc=0
[19:13:17] START gemma4:latest N30
[19:16:24] END   gemma4:latest N30 rc=0
[19:16:24] START gemma4:latest N15
[19:27:54] END   gemma4:latest N15 rc=0
[19:27:54] START qwen2.5:14b N120
[19:55:26] END   qwen2.5:14b N120 rc=0
[19:55:26] START qwen2.5:14b N30
[19:58:11] END   qwen2.5:14b N30 rc=0
[19:58:11] START qwen2.5:14b N15
[20:03:38] END   qwen2.5:14b N15 rc=0
[20:03:38] START llama3.1:8b N120
[20:20:40] END   llama3.1:8b N120 rc=0
[20:20:40] START llama3.1:8b N30
[20:22:38] END   llama3.1:8b N30 rc=0
[20:22:38] START llama3.1:8b N15
[20:26:08] END   llama3.1:8b N15 rc=0
[20:26:08] START qwen3:8b N120
[20:44:30] END   qwen3:8b N120 rc=0
[20:44:30] START qwen3:8b N30
[20:46:22] END   qwen3:8b N30 rc=0
[20:46:22] START qwen3:8b N15
[20:49:57] END   qwen3:8b N15 rc=0
[20:49:57] START gemma:latest N120
```

## Salvedades vigentes

- **Las latencias no son comparables** con las publicadas: los factores van de ×0,02 a ×2,58 sin
  dirección consistente, y la causa solo está explicada a medias (`FINDINGS §F71` y `§F71.bis`).
  La Tabla 8 del informe no debe rehacerse hasta entenderlo.
- **El consolidado no se rehace hasta tener los trece**, para no mezclar modelos medidos con
  localizaciones anotadas y sin ellas.
- Si el cambio de signo se confirma, **§5.3.1 habrá de reformularse** (`FINDINGS §F68`).
