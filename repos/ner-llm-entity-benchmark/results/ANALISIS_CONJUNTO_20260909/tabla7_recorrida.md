# Tabla 7 con los datos de la re-corrida completa (13 modelos)

Desde `results/ANALISIS_CONJUNTO_20260909/merged_results.csv`, verificado el 2026-09-09:
reproduce F = 121,5602 con 2 938 filas y 26 grupos ejecutando `merge_and_analyze.py` de forma
independiente. **No sustituye a la Tabla 7 del informe**: es el material para hacerlo cuando el
autor decida y cuando se resuelva `FINDINGS §F85`.

| Modelo | Base publ. | Base nueva | RAG publ. | RAG nuevo | Δ publ. | Δ nuevo | Signo |
|:---|---:|---:|---:|---:|---:|---:|:---:|
| `gemma4:31b-cloud` | 62.38 | 82.13 | 61.85 | 82.94 | -0.53 | +0.81 | **cambia** |
| `gemma4:31b-mlx` | 59.25 | 81.47 | 59.07 | 82.44 | -0.18 | +0.97 | **cambia** |
| `gemma4:12b-mlx` | 56.18 | 77.67 | 58.46 | 79.96 | +2.28 | +2.29 | igual |
| `gpt-oss:20b` | 52.39 | 75.41 | 55.67 | 77.08 | +3.28 | +1.67 | igual |
| `gemma4:latest` | 55.91 | 75.33 | 54.74 | 77.86 | -1.17 | +2.53 | **cambia** |
| `qwen2.5:14b` | 50.22 | 69.61 | 54.84 | 70.31 | +4.62 | +0.69 | igual |
| `llama3.1:8b` | 48.76 | 69.17 | 50.75 | 71.48 | +1.99 | +2.31 | igual |
| `qwen3:8b` | 48.21 | 69.03 | 51.46 | 68.98 | +3.25 | -0.05 | **cambia** |
| `llama3.2:latest` | 36.11 | 63.25 | 46.93 | 69.98 | +10.82 | +6.73 | igual |
| `mistral-nemo:latest` | 43.38 | 60.63 | 45.76 | 56.35 | +2.38 | -4.29 | **cambia** |
| `gemma:latest` | 44.00 | 59.55 | 51.36 | 59.58 | +7.36 | +0.03 | igual |
| `deepseek-r1:1.5b` | 24.83 | 28.73 | 23.94 | 30.80 | -0.89 | +2.07 | **cambia** |
| `nemotron-mini:4b` | 22.59 | 26.31 | 37.12 | 40.55 | +14.53 | +14.23 | igual |

## Salvedad obligatoria sobre `nemotron-mini:4b`

Su línea base incluye **17 registros que puntúan 0,00 por un `TypeError` del arnés**, no por el
modelo (`FINDINGS §F85`). Descontándolos, su base sube de **26.31 a 30.97** y su Δ baja de
**+14.23 a +9.58 pp**. La fila de arriba es la que sale del consolidado tal cual; **la buena exige
volver a ejecutar ese brazo**, porque descontar filas deja el diseño en 96 registros y debilita todo lo demás.

## Recuento

- **6 de 13** modelos cambian el signo del efecto del RAG.
- El mayor efecto sigue siendo `nemotron-mini:4b`; el segundo, `llama3.2:latest`.
- El ANOVA conjunto da **F = 121,5602** con p prácticamente cero, frente al F = 38,2222 publicado.
