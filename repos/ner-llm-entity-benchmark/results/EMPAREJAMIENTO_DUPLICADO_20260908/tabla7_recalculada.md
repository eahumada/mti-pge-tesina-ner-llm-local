# Tabla 7 recalculada contando cada referencia una sola vez

Generado por `tools/efecto_emparejamiento_duplicado.py` desde `efecto.json`, en este mismo
directorio. No reejecuta inferencia: despeja `len(gt)` de `recall = tp/len(gt)` y cuenta cada
referencia una vez. Ver `FINDINGS §F81` y `§F81.bis`.

**Esto no es una propuesta de sustitución.** Es el material para tomar la decisión 8 de
`DECISIONES-PENDIENTES-20260908.md` mirando cifras en lugar de en abstracto.

| Modelo | Base publ. | Base corr. | RAG publ. | RAG corr. | Δ publ. | Δ corr. | Dupl. | Δ signif. |
|:---|---:|---:|---:|---:|---:|---:|---:|:---:|
| `gemma4:31b-cloud` | 62.38 | 62.35 | 61.85 | 61.79 | -0.54 | -0.56 | 23 | no |
| `gemma4:31b-mlx` | 59.26 | 59.21 | 59.07 | 58.92 | -0.18 | -0.28 | 29 | no |
| `gemma4:12b-mlx` | 56.18 | 56.17 | 58.46 | 58.34 | +2.28 | +2.17 | 37 | no |
| `gemma4:latest` | 55.91 | 54.98 | 54.74 | 54.72 | -1.17 | -0.25 | 143 | no |
| `gpt-oss:20b` | 52.39 | 52.37 | 55.67 | 55.65 | +3.28 | +3.28 | 11 | no |
| `qwen2.5:14b` | 50.22 | 50.21 | 54.84 | 54.81 | +4.62 | +4.60 | 7 | no |
| `llama3.1:8b` | 48.76 | 48.33 | 50.75 | 50.74 | +1.99 | +2.41 | 51 | no |
| `qwen3:8b` | 48.21 | 48.16 | 51.46 | 51.42 | +3.25 | +3.26 | 18 | no |
| `gemma:latest` | 44.00 | 43.96 | 51.36 | 51.25 | +7.36 | +7.29 | 7 | no |
| `mistral-nemo:latest` | 43.38 | 43.37 | 45.76 | 45.76 | +2.37 | +2.39 | 4 | no |
| `llama3.2:latest` | 36.11 | 36.02 | 46.93 | 46.93 | +10.82 | +10.91 | 37 | sí** (p=0.007) |
| `deepseek-r1:1.5b` | 24.83 | 24.60 | 23.94 | 23.61 | -0.90 | -0.98 | 31 | no |
| `nemotron-mini:4b` | 22.59 | 21.31 | 37.12 | 37.06 | +14.52 | +15.75 | 11 | sí** (p<0.001) |

## Lo que cambia y lo que no

- **Ningún Δ cambia de signo.** Los negativos siguen negativos y los positivos, positivos.
- La mayor variación de un Δ es **+1.23 pp**, en `nemotron-mini:4b`.
- El grupo más afectado en valor absoluto es `nemotron-mini:4b_baseline`, que pasa de 22.59 a 21.31.
- El F1 corregido es **siempre menor o igual** que el publicado, como predice el mecanismo:
  contar dos veces una referencia solo puede inflar la exhaustividad.
- El orden de los veintiséis grupos cambia en **un puesto**, entre dos separados por 0,24 pp,
  y el informe no publica una ordenación de grupos.

## Si se adopta

Habría que rehacer, además de la Tabla 7: el Anexo I, la Figura 2, el ANOVA y el post-hoc, y las
cifras de §5.3.1 que citan valores concretos. **No se ha hecho nada de eso**, porque la decisión es
del autor y porque la re-corrida en marcha sustituirá estos datos de todos modos.
