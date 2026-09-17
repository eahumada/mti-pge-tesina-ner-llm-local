# R2 — Intervalos de confianza consolidados (5 semillas), N=120 filtrado a N=113

Consolidado de las 5 semillas de R2 (`barras_error_n120_REMOTO/seed_{42,123,456,789,1024}/`),
pedido por Antigravity en `CURRENT-TASKS.md §3.AGY.19` tras el cierre al 100 % del encargo remoto.

## Metodología

- Fuente: `benchmark_results.csv` de cada semilla (dato crudo por artículo), **no**
  `benchmark_summary.json` — ver `FINDINGS.md §F187`: el agregado de `gemma4:31b-cloud` está
  corrompido en las 5 semillas (quedó desactualizado tras la reconciliación de la suite cloud);
  el CSV crudo es correcto y coincide con lo certificado por separado en `§3.AGY.15`.
- Se excluyen los mismos 7 artículos con codificación contaminada que excluye el estudio
  principal (`results/ANALISIS_CONJUNTO_20260909_FIX/`): `real_mixed_1, real_mixed_101,
  real_mixed_21, real_mixed_27, real_mixed_41, real_mixed_59, real_mixed_79`. Quedan 113
  artículos por semilla y configuración, igual que la Tabla 7 vigente.
- Por semilla se calcula la media simple del F1 por artículo sobre esos 113 registros. Se
  verificó que este método reproduce exactamente la cifra publicada (`gemma4:31b-mlx_baseline`
  semilla 42 → 81,47 %, idéntico al valor citado en el cuerpo del informe para N=120).
- Sobre las 5 medias por semilla se calcula el intervalo de confianza al 95 % con distribución
  t de Student, 4 grados de libertad (t=2,776).

## Reproducir

```
python3 calcular_intervalos_confianza.py
```

Genera `intervalos_confianza_95.json` con `mean_f1`, `sd`, `ci95_lo`, `ci95_hi` y `per_seed`
(las 5 medias, en el orden 42, 123, 456, 789, 1024) para las 22 configuraciones.

## Resultado relevante para la Tabla 7

`gemma4:31b-mlx_baseline` (mejor modelo local, cifra citada en el cuerpo como 81,47 %):
media de 5 semillas 81,56 %, IC95 % [81,45 %, 81,67 %]. La cifra puntual del cuerpo (semilla 42)
cae dentro de este intervalo — el punto ya publicado es representativo del consolidado, no un
valor atípico.

No se ha modificado el cuerpo del informe con estos números: la decisión de si y cómo incorporar
barras de error a la Tabla 7 queda pendiente de confirmación del autor.
