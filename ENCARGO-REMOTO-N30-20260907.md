# 🔴 Encargo al equipo remoto 48 GB — re-ejecutar la corrida N=30

**Fecha:** 2026-09-07 · **De:** equipo de desarrollo principal · **Decisión del autor:** re-ejecutar.
**Excepción explícita al cierre de benchmarks** de `CIERRE-BENCHMARKS-20260907.md`: se reabre la ejecución
**solo para esta corrida**. Ninguna otra.

---

## Por qué

El F1 titular del informe sobre el corpus N=30 —`gemma4:31b`: **79.03 %**— es **la única cifra del estudio
que sigue calculada con el *scorer* defectuoso**. Todo lo demás se re-puntuó tras corregir el `F1=1.0` en
extracción vacía, pero esta no se puede corregir: **el dato por registro se perdió por sobrescritura** y solo
sobrevive el agregado en `repos/ner-llm-entity-benchmark/benchmark_augmented_30.log`:

```
gemma4:31b   f1=0.790303  precision=0.733413  recall=0.891111  hallucination=0.0  latency=160.23
```

Es aritméticamente consistente (0.7903 ≤ (0.7334+0.8911)/2 = 0.8123) y con un *recall* del 89 % hubo pocas
extracciones vacías, así que el sesgo probablemente sea pequeño — **pero eso es una inferencia, no una
medición**. La cifra sostiene §5.3.1–5.3.4 y la verificación de la hipótesis en §6.1, así que necesita un
respaldo verificable.

## Por qué os toca a vosotros

`gemma4:31b` y `gemma4:31b-mlx` pesan **19 GB en disco** y ~24,7 GB operativos. La máquina de desarrollo tiene
**16 GB** y su techo de VRAM asignable ronda los 12 GB: no caben, ni siquiera en serie con `keep_alive=0`.

## Qué hay que ejecutar

**Corpus:** `data/kleptotrace_augmented_30.json` — verificado íntegro, **30 registros**, mismo esquema que el
corpus N=120 (`article_id`, `title`, `text`, `name_entities`, `organizations`).

**Modelos:** `gemma4:31b` y `gemma4:31b-mlx` — los dos que aparecen en la Tabla de §5.3.1.

**Modo:** **baseline, sin RAG.** La corrida original de julio fue un benchmark serial sin RAG; §5.3.1 solo
tiene esas dos filas. **No uséis `--rag-study`**: duplicaría el tiempo sin aportar nada al informe.

**Protocolo original** (leído del log de julio, para que la cifra sea comparable): 30 artículos en **6 lotes**
(`--batch-size 5`), controlador AIMD arrancando en 2 workers con techo 9, `--seed 42`, `temperature 0.1`,
`num_predict 2048`.

```bash
venv/bin/python src/main.py \
  --models gemma4:31b gemma4:31b-mlx \
  --data-file data/kleptotrace_augmented_30.json \
  --batch-size 5 --seed 42 \
  --results-dir results/n30_rerun_REMOTO
```

**Régimen de *thinking*:** `gemma4:31b-mlx` está en `_THINKING_DISABLED_MODELS` (correcto, no lo toquéis).
`gemma4:31b` corre con thinking **ON**, que es el statu quo decidido en `FINDINGS.md §F45`. **No lo cambiéis**:
la corrida de julio también fue con el comportamiento por defecto, y cambiarlo ahora rompería la comparación.

**ETA estimada:** ~5,1 h para `gemma4:31b` (613 s/artículo medidos) + ~3,6 h para `gemma4:31b-mlx` (429 s/artículo)
≈ **9 h en serie**. Una GPU, sin paralelismo entre modelos.

## Qué entregar

1. El directorio `results/n30_rerun_REMOTO/` completo (CSV, `detailed_results.json`, `run_config.json`,
   `benchmark_summary.json`, `statistical_report.md`, logs).
2. **El ANOVA entre los dos modelos**, que reemplaza el actual de §5.3.2 (F=0.141, p=0.708).
3. Un reporte breve con las verificaciones de siempre: **tasa de fallo por modelo** (`parse_method='failed'`
   y cuántos `recall=0`), **protocolo** (que el `run_config.json` refleje lo pedido), **consistencia
   aritmética** (ninguna fila con `F1 > (P+R)/2`) y **causa de cualquier anomalía** (latencia 0 y 0 tokens =
   rechazo de infraestructura; latencia alta con `content` vacío = el arnés perdió la respuesta).

**Al promediar desde JSON usad `if x.get('k') is not None`, nunca `if x.get('k')`:** `0.0` es *falsy* y
descartaría las filas en cero, inflando la media. Nos costó un informe equivocado una vez.

## Lo que NO hay que hacer

- **No re-ejecutar ninguna otra corrida.** El resto del estudio está cerrado y verificado.
- **No tocar** `results/ANALISIS_CONJUNTO_20260907/` ni ninguna corrida N=120 o N=15.
- **No borrar** `benchmark_augmented_30.log`: es el único registro del valor de julio y debe conservarse para
  trazabilidad, gane o pierda la comparación.
- **No ajustar el régimen de *thinking*** de ninguno de los dos modelos.

## Cuando terminéis

Declaradlo en `CURRENT-TASKS.md` §3.bis y avisad por *push*. Nosotros decidiremos entonces si la cifra nueva
sustituye a 79.03 % en el cuerpo del informe o si ambas conviven con nota de procedencia. **Reportad el
resultado sea cual sea**, incluso si es sensiblemente más bajo: el objetivo es tener un número verificable,
no confirmar el anterior.
