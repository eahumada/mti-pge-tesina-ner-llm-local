# 🟠 CORRECCIÓN para el equipo remoto 48 GB — B1 está invertido y los `summary` están obsoletos

**Fecha:** 2026-09-07 · **De:** equipo de desarrollo principal
**Sobre:** `remote_48g/INVESTIGACION-B1-B4.md` (commit `494dacf`)

---

## Resumen en una línea

Vuestra auditoría B1–B4 es buena y B2/B3/B4 se sostienen. Pero **B1 pide reconciliar una discrepancia que no
existe**: el `benchmark_summary.json` que citáis como «fuente primaria» es **anterior al re-puntaje** y
conserva las cifras infladas. Y eso **no es un caso aislado**: los `summary` y `statistical_report.md` de
**las ocho corridas** están en la misma situación.

---

## 1. B1 — la discrepancia de `llama3.1:8b`

Vuestra nota dice: «el informe cita 0.4876/0.5075 — **no coinciden** con el summary primario
(0.4959/0.5491). Reconciliar cuál es la fuente oficial antes de reemplazar».

| Fuente | baseline | kb_rag | Veredicto |
|:---|--:|--:|:---|
| `benchmark_summary.json` (mtime **10:08**) | 0.4959 | 0.5491 | **pre-fix, inflado** |
| Recálculo desde `metrics.overall.tp/fp/fn` | **0.4876** | **0.5075** | correcto |
| `benchmark_results.csv` (mtime **18:09**) | 0.4876 | 0.5075 | ✅ coincide |

**No hay nada que reconciliar: 0.4876 / 0.5075 es el valor correcto.** El re-puntaje del bug de scoring se
aplicó a las 18:09 y el summary es de las 10:08.

## 2. El problema de fondo — `rescore_saved.py` solo reescribe el CSV

Vuestra herramienta hace exactamente lo que documenta, pero **solo toca `benchmark_results.csv`**. En las
ocho corridas re-puntuadas, `benchmark_summary.json` y `statistical_report.md` son **todos anteriores** al
re-puntaje de las 18:09 (los mtime van de las 01:55 a las 17:56).

Y hay un caso peor: **`detailed_results.json` quedó internamente inconsistente.** Sus
`metrics.overall.tp/fp/fn` son correctos, pero el campo `f1` de cada fila sigue siendo el viejo. Quien
promedie `f1` leyendo el JSON obtiene el valor inflado — que es exactamente lo que os pasó en B1.

> **Regla operativa:** hoy **`benchmark_results.csv` es la única fuente válida** de P/R/F1. Ningún otro
> artefacto de `results/` debe citarse sin re-puntuar antes.

## 3. Qué hemos hecho por nuestra parte (ya empujado)

1. **Re-puntuadas las tres corridas legacy** con vuestra propia herramienta — no estaban incluidas y
   arrastraban **199 filas degeneradas**. Backups en `.bak_prescore`. Tras ello: **8 927 filas, 0
   violaciones de `F1 ≤ (P+R)/2`, 0 degeneradas, 0 filas perdidas.** Todo el estudio comparte ya una sola
   convención de puntuación.
2. **ANOVA conjunto recalculado** sobre los CSV: `results/ANALISIS_CONJUNTO_20260907/`.
   **14 modelos × 2 modos = 28 grupos, 3 360 filas, F = 36.3696, p = 1.4321e-164.**
3. **`results/AVISO-SUMMARIES-OBSOLETOS.md`** — aviso permanente para que nadie vuelva a citar un summary.

## 4. Qué os pedimos

1. **Corregir B1 de forma aditiva** en `INVESTIGACION-B1-B4.md`: el valor a usar es **0.4876 / 0.5075**, sin
   reconciliación pendiente.
2. **Regenerar los `benchmark_summary.json` y `statistical_report.md`** de las ocho corridas desde los CSV
   re-puntuados, **o** marcarlos explícitamente como obsoletos en cada directorio.
3. **Extender `rescore_saved.py`** para que reescriba también el campo `f1` de `detailed_results.json` y el
   summary. Mientras no lo haga, cualquier auditoría futura repetirá este error.
4. **Sigue pendiente lo de `CORRECCION-QWEN3-THINKING-20260906.md §4.6-4.7`**: revisar
   `qwen3:14b/32b/latest` y enumerar los modelos del estudio con capacidad `thinking`.

## 5. Lo que sí queda confirmado de vuestra investigación

- **B1 (las dos filas imposibles):** correcto — `llama3.2:latest_rag` 0.8783 y `llama3.1:8b_baseline` 0.7667
  no existen en ningún CSV y no son recuperables.
- **B2:** no hemos verificado la fuente externa, pero vuestro argumento aritmético es sólido: 12.300 → 87.200 M
  en cuatro años implica una CAGR del ~63 %, incompatible con el 23,92 % que documentáis.
- **B3:** coherente con lo ya establecido (techo de Metal ~75 % de la RAM unificada).
- **B4:** la única fila reproducible de §5.5 es `gemma4:31b-mlx` (22.80 tok/s / 24 607 MB).
