# 🗂️ RUNS_INDEX — Índice histórico de corridas del benchmark

> **Archivo nuevo (2026-09-03).** Cataloga TODAS las corridas del benchmark encontradas en el
> repositorio, para poder distinguirlas sin ambigüedad por **corpus + N**, **modo** (baseline /
> RAG), **tipo de prompt** (zs-en / zs-es / fs-en / fs-es), **fecha** y **conjunto de modelos**.
>
> **Política de mantenimiento: ESTRICTAMENTE ADITIVA** (ver `CLAUDE.md` / `AGENTS.md`).
> Nunca se borra ni se reescribe una fila existente. Cada corrida nueva se **agrega al final** de
> la tabla §2. Si una corrida se reinterpreta, se añade una nota nueva en §6 citando su `run_id`;
> la fila original se conserva intacta.
>
> ⚠️ `results/` está en `.gitignore` (ver §7): este índice **no queda versionado en git** salvo
> que se lo añada explícitamente (`git add -f results/RUNS_INDEX.md`).

---

## 1. Resumen ejecutivo

| Dimensión | Estado a 2026-09-03 |
| :--- | :--- |
| Corridas con directorio de resultados propio | **7** (`results/<dataset>_<timestamp>/`) — *conteo corregido el 2026-09-03: eran 5 al crear el índice; ver nota N4 en §6 y filas #14 y #15* |
| Corridas "planas" heredadas (escribieron en `results/` raíz, sobrescribiéndose entre sí) | **2** conjuntos de archivos recuperables |
| Corridas con evidencia **solo en log** (resultados perdidos por sobrescritura) | **6** |
| Corpus efectivamente ejecutados | `kleptotrace.json` (N=15), `kleptotrace_augmented_30.json` (N=30), `benchmark_balanced_120.json` (N=120) |
| Modos ejecutados | `baseline`, `rag_study` legacy (`entities`), `rag_study` KB (`kb_combined`), `ablation` (4 prompts) |
| Combinaciones **nunca ejecutadas** | N=30 con RAG, N=30 con análisis de variantes de prompts, N=120 con `kb_guidelines` / `kb_fewshot`, análisis de variantes de prompts cruzado con RAG |

**Hallazgo crítico:** el resultado titular de la tesina (`gemma4:31b`, **F1 = 79.03 %**, 0 % de
alucinaciones, corpus **N=30**) proviene de la corrida `2026-07-01 17:27` cuyos archivos de
resultados **fueron sobrescritos** por corridas posteriores que también escribieron en `results/`
raíz. Su única evidencia superviviente es `benchmark_augmented_30.log`. Este hecho es la
justificación principal del esquema de versionado propuesto en §4.

---

## 2. Catálogo de corridas (orden cronológico)

Leyenda de **Modo**: `baseline` = sin RAG · `rag-entities` = `--rag-study` con `rag_mode=entities`
(dict-RAG legacy; condiciones `*_baseline` + `*_rag_enhanced`) · `rag-kb-<modo>` = `--rag-study`
con base de conocimientos (condiciones `*_baseline` + `*_kb_rag`) · `ablation` = `--ablation`,
que ejecuta la **Análisis de Variantes de Prompts** (término principal del proyecto;
sinónimos glosados: *análisis de variantes de prompts*, *diseño factorial 2x2*) recorriendo los 4 prompts sobre
1 modelo. `ablation` se conserva como etiqueta corta porque es el nombre del flag CLI y del campo
`BenchmarkConfig.ablation`; los identificadores de código no se renombran.

Leyenda de **Prompt**: `zs-en` = `SYSTEM_PROMPT.md` · `zs-es` = `SYSTEM_PROMPT_ES.md` ·
`fs-en` = `SYSTEM_PROMPT_EN_FEWSHOT.md` · `fs-es` = `SYSTEM_PROMPT_ES_FEWSHOT.md` ·
`4-prompts` = las cuatro condiciones en la misma corrida.

| # | run_id (propuesto) | Fecha (inicio) | Corpus | N | Modo | Prompt | Nº modelos | Condiciones | Filas CSV | Ruta / evidencia | Estado | Notas |
| :-: | :--- | :--- | :--- | :-: | :--- | :--- | :-: | :-: | :-: | :--- | :--- | :--- |
| 1 | `klepto_N15__baseline__zs-en__20260630_2110` | 2026-06-30 21:10 | `kleptotrace.json` | 15 | baseline | zs-en | 3 | 3 | 45 | `results/benchmark_results 2.csv`, `results/statistical_report 2.md` | ⚠️ Parcial | Corrida plana temprana. Modelos: `llama3.1:8b`, `minimax-m3:cloud` (F1 0.0), `nemotron-mini:4b`. Sin `run_config.json` propio. El sufijo " 2" proviene de una copia de Finder/iCloud, no del pipeline. |
| 2 | `klepto_N15__baseline__zs-en__20260701_0637` | 2026-07-01 06:37 | `kleptotrace.json` | 15 | baseline | zs-en | n/d | n/d | — | `benchmark_console.log` (246 KB) | ❌ Resultados perdidos | Escribió en `results/` raíz; sobrescrita. Incluye ejecución de `simulate_production.py` (F1 medio 72.12 % sobre 5 artículos). |
| 3 | `klepto_N15__baseline__zs-en__20260701_1248` | 2026-07-01 12:48 | `kleptotrace.json` | 15 | baseline | zs-en | 2 | 2 | — | `benchmark_gemini_gliner.log` | ❌ Resultados perdidos | `gemini-1.5-flash` (F1 0.0, fallo de acceso) y `gliner:medium` (F1 0.4767). |
| 4 | `klepto_N15__baseline__zs-en__20260701_1251` | 2026-07-01 12:51 | `kleptotrace.json` | 15 | baseline | zs-en | 1 | 1 | — | `benchmark_gemini_active.log` | ❌ Resultados perdidos | `gemini-3.1-flash-lite`: F1 0.6547, latencia 1.69 s. |
| 5 | `klepto_N15__baseline__zs-en__20260701_1436` | 2026-07-01 14:36 | `kleptotrace.json` | 15 | baseline | zs-en | 1 | 0 | 0 | `benchmark_mlx.log` | ❌ Fallida | `gemma4:31b-mlx` no disponible en Ollama → *No benchmark results generated*. |
| 6 | `klepto_N15__baseline__zs-en__20260701_1445` | 2026-07-01 14:45 | `kleptotrace.json` | 15 | baseline | zs-en | 2 | 2 | — | `benchmark_mlx_serial.log` | ❌ Resultados perdidos | `gemma4:31b` F1 0.6830 / `gemma4:31b-mlx` F1 0.6852 (modo serial). Es la referencia N=15 citada en la tesina (67.83 %). |
| 7 | **`kleptoaug_N30__baseline__zs-en__20260701_1727`** | 2026-07-01 17:27 | `kleptotrace_augmented_30.json` | **30** | baseline | zs-en | 2 | 2 | — | `benchmark_augmented_30.log` | ❌ **Resultados perdidos** | 🔴 **Corrida titular de la tesina.** `gemma4:31b` F1 **0.790303** / P 0.7334 / R 0.8911 / halluc. 0.0 / 160.23 s; `gemma4:31b-mlx` F1 0.774740. Escribió en `results/` raíz y fue sobrescrita el 2026-07-27. **Única corrida N=30 jamás ejecutada.** Reproducirla es prioridad (§5). |
| 8 | `klepto_N15__rag-entities__zs-en__20260727_1104` | 2026-07-27 (fin 11:04) | `kleptotrace.json` | 15 | rag-entities | zs-en | 15 | 30 | 450 | `results/benchmark_results.csv`, `results/detailed_results.json`, `results/statistical_report.md`, `results/benchmark_summary.json`, `results/acceptance_status.json`, `results/confusion_matrix.json`, `results/benchmark.log` | ⚠️ Plana (raíz) | Estudio RAG legacy: 15 modelos × {baseline, rag_enhanced}. Mejor: `gemma4:31b-mlx_rag_enhanced` F1 0.6897. ANOVA F=7.0450, p=3.51e-22. ⚠️ **`results/run_config.json` NO corresponde a esta corrida** (está fechado 2026-08-24 y apunta a `benchmark_balanced_120.json`): la metadata de raíz está desincronizada de los datos de raíz. |
| 9 | `klepto_N15__ablation__4-prompts__20260727_110454` | 2026-07-27 11:04:54 | `kleptotrace.json` | 15 | ablation | 4-prompts | 1 (`gemma4:latest`) | 4 | 60 | `results/kleptotrace_20260727_110454/` | ✅ Completa | Ablación de prompts sobre N=15: `fs-es` 0.6987 (mejor) > `zs-es` 0.6793 > `zs-en` 0.6676 > `fs-en` 0.5817. ANOVA F=1.0248, p=0.3886 (no significativo). ⚠️ Su `run_config.json` dice `system_prompt_file: SYSTEM_PROMPT.md` y **no registra el flag `--ablation`** (ver §3). |
| 10 | `balanced120_N120__baseline__zs-en__20260824_173017` | 2026-08-24 17:30:17 | `benchmark_balanced_120.json` | 120 | baseline | zs-en | 1 (`llama3.2:latest`) | 1 | 120 | `results/benchmark_balanced_120_20260824_173017/` | ✅ Completa | Corrida de humo previa al barrido grande. F1 0.3945, halluc. 0.0274. ANOVA F=0.0 (un solo grupo). |
| 11 | `balanced120_N120__rag-entities__zs-en__20260824_173036` | 2026-08-24 17:30:36 → 2026-08-25 07:12 | `benchmark_balanced_120.json` | 120 | rag-entities | zs-en | 15 (de 16 pedidos) | 30 | 3600 | `results/benchmark_balanced_120_20260824_173036/` | ✅ Completa | Barrido mayor N=120 baseline vs. RAG legacy. Mejor: `gemma4:31b-mlx_baseline` F1 0.5983. ANOVA F=38.3239, p=1.07e-185. `gpt-oss:20b` fue solicitado pero **omitido** (no disponible) — el `run_config.json` lista 16 modelos y el CSV solo contiene 15. Sin campo `rag_mode` (anterior a su introducción ⇒ equivale a `entities`). |
| 12 | `balanced120_N120__ablation__4-prompts__20260825_071207` | 2026-08-25 07:12:07 → 10:14 | `benchmark_balanced_120.json` | 120 | ablation | 4-prompts | 1 (`gemma4:latest`) | 4 | 480 | `results/benchmark_balanced_120_20260825_071207/` | ✅ Completa | Ablación sobre corpus real: `zs-es` 0.5562 (mejor) > `fs-en` 0.5450 > `zs-en` 0.5446 > `fs-es` 0.5402. ANOVA F=0.1451, p=0.9328 (no significativo con N=120). Mismo defecto de metadata que #9: el `run_config.json` es indistinguible de un baseline. |
| 13 | `balanced120_N120__rag-kb-combined__zs-en__20260901_140421` | 2026-09-01 14:04:21 → 20:04 | `benchmark_balanced_120.json` | 120 | rag-kb-combined | zs-en | 5 | 10 | 1200 | `results/benchmark_balanced_120_20260901_140421/` + `results/kb_rag_analysis_20260901.json` | ✅ Completa | KB RAG contextual v1.1.0 (`rag_mode: kb_combined`). Modelos: `llama3.2:latest`, `gemma4:latest`, `gemma4:31b-mlx`, `qwen2.5:14b`, `gemma:latest`. Δ F1 (kb_rag − baseline): `llama3.2` **+9.98 pp**, `gemma:latest` **+5.69 pp**, `qwen2.5:14b` **+4.62 pp**, `gemma4:latest` −0.33 pp, `gemma4:31b-mlx` −0.18 pp. ANOVA F=10.2096, p=2.87e-15. Único artefacto de `results/` versionado en git. |
| 14 | `balanced120_N120__rag-entities__zs-en__20260903_140628__DESCARTADA` | 2026-09-03 14:06:28 | `benchmark_balanced_120.json` | 120 | rag-entities (`rag_mode` por defecto) | zs-en | n/d (incluye `gemma4:31b-cloud`, `minimax-m3:cloud`) | n/d | 0 | `results/DESCARTADA_ragmode_incorrecto_142604/` (solo `.checkpoint.json` 956 KB + `benchmark.log` 1.0 MB) | ❌ **Descartada / abortada** | 🪤 **Trampa del flag `--rag-mode`**: se lanzó con `--rag-study` **sin** `--rag-mode`, por lo que tomó el default `entities` y cargó el dict-RAG legacy (`src/rag_manager: Vector DB already populated with 17453 entities`) en vez de la base de conocimientos. Descartada por el autor a los ~19 min. Sin `run_config.json`, sin CSV. *(Fila añadida el 2026-09-03.)* |

**Artefactos auxiliares en `results/` sin corrida propia:**

| Archivo | Fecha | Origen |
| :--- | :--- | :--- |
| `results/run_config.json` | 2026-08-24 15:08 | Config suelta de raíz con `results_dir: "results"`; **no** corresponde a los CSV de raíz (#8). |
| `results/simulation_summary.json` | 2026-08-25 10:16 | Salida de `src/simulate_production.py` (5 artículos, F1 medio 58.82 % sobre N=120). |
| `results/.checkpoint.json` | 2026-07-27 11:04 | Checkpoint de la corrida #8 (raíz). |
| `results/kb_rag_analysis_20260901.json` | 2026-09-01 20:05 | Análisis derivado de #13 (único archivo de `results/` en git). |

---

## 3. Matriz de cobertura corpus × modo × prompt

`✅` = ejecutada y conservada · `🟡` = ejecutada pero resultados perdidos · `⬜` = nunca ejecutada.

| Corpus (N) | baseline zs-en | baseline zs-es | rag-entities | rag-kb-combined | rag-kb-guidelines | rag-kb-fewshot | Comparación de Config. de Prompt — `ablation` (4 prompts) |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| `kleptotrace.json` (N=15) | 🟡 (#2,#6) | ⬜ | ⚠️ #8 (plana) | ⬜ | ⬜ | ⬜ | ✅ #9 |
| `kleptotrace_augmented_30.json` (N=30) | 🟡 **#7** | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `kleptotrace_augmented_60.json` (N=60) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `kleptotrace_augmented_120.json` (N=120 sint.) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| `benchmark_balanced_120.json` (N=120 real) | ✅ #10 | ⬜ | ✅ #11 | ✅ #13 | ⬜ | ⬜ | ✅ #12 |
| `conll2002_es.json` (N=833) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

**Brecha principal para el requisito del autor** ("poder hacer pruebas con N=30 y N=120, con y sin
RAG, y para los distintos shots"): el corpus **N=30 solo tiene una corrida baseline zs-en, y sus
resultados no se conservan**. Toda la columna RAG y la de Análisis de Variantes de Prompts
(análisis de variantes de prompts) están vacías para N=30.

---

## 4. Esquema de versionado propuesto (a partir de 2026-09-03)

> **Estado 2026-09-03:** la regla 1 de §4.3 ya está **IMPLEMENTADA** en código; el resto de §4
> sigue siendo propuesta. Ver notas N1 y N3 en §6.

### 4.1 Convención de nombres de directorio

```
results/<corpus>_N<n>__<modo>__<prompt>__<YYYYMMDD>_<HHMMSS>[__<tag>]/
```

| Componente | Valores | Origen |
| :--- | :--- | :--- |
| `<corpus>` | `klepto`, `kleptoaug`, `balanced120`, `conll2002es` | slug de `basename(data_file)` |
| `N<n>` | `N15`, `N30`, `N60`, `N120`, `N833` | nº **real** de registros cargados, no el del nombre de archivo |
| `<modo>` | `baseline`, `rag-entities`, `rag-kb-guidelines`, `rag-kb-fewshot`, `rag-kb-combined`, `ablation` | `rag_study` + `rag_mode` + `ablation` |
| `<prompt>` | `zs-en`, `zs-es`, `fs-en`, `fs-es`, `4-prompts` | `system_prompt_file`; `4-prompts` cuando `--ablation` |
| timestamp | `YYYYMMDD_HHMMSS` local | igual que hoy |
| `<tag>` | libre, opcional (`smoke`, `rerun`, `tesina-v2`) | nuevo flag `--run-tag` |

Ejemplos:

```
results/kleptoaug_N30__baseline__zs-en__20260903_101500/
results/kleptoaug_N30__rag-kb-combined__zs-es__20260903_143000/
results/balanced120_N120__ablation__4-prompts__20260903_190000__rerun/
```

El doble guion bajo `__` separa dimensiones y el simple `_` va dentro de cada dimensión, de modo
que el nombre es parseable con `split("__")` sin ambigüedad.

### 4.2 Campos que debe registrar `run_config.json` (o un `run_meta.json` hermano)

Todos **aditivos**: ninguna clave actual se renombra ni se elimina, de modo que los 5 directorios
históricos siguen siendo legibles.

**Identidad**: `run_id`, `run_tag`, `schema_version` (`"2"`).
**Tiempo**: `started_at_utc`, `finished_at_utc`, `duration_sec`.
**Corpus**: `data_file` (ya existe), `dataset_n_records`, `dataset_sha256`, `dataset_kind`
(`synthetic` / `real` / `mixed`).
**Modo**: `rag_study` (ya existe), `rag_mode` (ya existe), **`ablation`** (hoy NO se persiste),
`conditions` (lista literal de condiciones generadas, p. ej. `["zs-en","zs-es","fs-en","fs-es"]`
o `["gemma4:latest_baseline","gemma4:latest_kb_rag", …]`).
**Prompt**: `system_prompt_file` (ya existe), `prompt_variant` (`zs-en`…), `prompt_files`
(mapa condición → archivo), `prompt_sha256` (mapa condición → hash del texto efectivo).
**Modelos**: `models` (ya existe = solicitados), `models_available`, `models_skipped`.
**Reproducibilidad**: `git_commit`, `git_branch`, `git_dirty`, `python_version`,
`platform`, `hostname`, `ollama_version`, `key_package_versions`.
**Resultado**: `status` (`completed` / `partial` / `failed`), `n_rows`, `notes`.

### 4.3 Reglas de operación

1. ✅ **[IMPLEMENTADA — 2026-09-03]** **Nunca escribir en `results/` raíz.** Si `results_dir`
   termina siendo literalmente `results`, abortar con error en vez de sobrescribir (causa raíz de
   las 6 corridas perdidas). Implementado como `assert_not_results_root()` en `src/config.py`, que
   lanza `ResultsDirRootError` y se invoca en `BenchmarkConfig.__post_init__` y de nuevo en
   `ensure_directories()` como segunda línea de defensa. Ninguna corrida puede ya escribir en la raíz.
2. **Un directorio = una combinación** (corpus, N, modo, prompt, fecha). Reejecutar no reutiliza
   directorio: el timestamp lo hace único.
3. **Índice aditivo**: al terminar una corrida, se agrega una fila a §2 de este archivo (nunca se
   edita una existente) y una entrada al `results/runs_index.json` machine-readable.
4. **Retención**: los directorios históricos no se borran. Si hace falta espacio, se comprime el
   directorio (`tar.zst`) conservando `run_config.json`, `statistical_report.md`,
   `benchmark_summary.json` y `acceptance_status.json` sin comprimir.

---

## 5. Corridas recomendadas para cerrar la matriz (§3)

Prioridad descendente. **No ejecutar mientras haya descargas de modelos en curso.**

| Prioridad | Comando | Motivo |
| :-: | :--- | :--- |
| 🔴 1 | `python src/main.py --data-file data/kleptotrace_augmented_30.json --models gemma4:31b gemma4:31b-mlx` | Reproducir la corrida #7 (F1 79.03 %), el resultado titular de la tesina hoy sin respaldo de datos. |
| 🟠 2 | `python src/main.py --data-file data/kleptotrace_augmented_30.json --rag-study --rag-mode kb_combined --models <5 modelos de #13>` | Habilitar la comparación baseline vs. KB RAG sobre N=30, hoy inexistente. |
| 🟠 3 | `python src/main.py --ablation --data-file data/kleptotrace_augmented_30.json --models gemma4:latest` | Ablación de prompts sobre N=30, para comparar con #9 (N=15) y #12 (N=120). |
| 🟡 4 | `python src/main.py --data-file data/benchmark_balanced_120.json --rag-study --rag-mode kb_guidelines …` y `--rag-mode kb_fewshot` | Aislar el aporte de guidelines vs. few-shot dentro de `kb_combined` (#13). |
| 🟡 5 | `python src/main.py --data-file data/benchmark_balanced_120.json --rag-study --rag-mode kb_combined --models gpt-oss:20b …` | Completar los 11 modelos que quedaron sin re-evaluar sobre N=120 (§7.2 de la tesina). |

---

## 6. Notas y correcciones posteriores

> Sección aditiva: aquí se agregan reinterpretaciones o correcciones de filas de §2 **sin
> modificarlas**. Cada nota indica fecha, `run_id` afectado y el cambio de lectura.

- *(2026-09-03)* Creación del índice. Sin correcciones pendientes.
- **N1 · *(2026-09-03)* La regla 1 de §4.3 dejó de ser una propuesta: está implementada.**
  `src/config.py::assert_not_results_root()` aborta cualquier corrida cuyo `results_dir` resuelva a
  la raíz `results/`, invocada desde `__post_init__` y desde `ensure_directories()`. Las reglas 2-4
  de §4.3 siguen siendo propuestas.
- **N2 · *(2026-09-03)* La limitación 1 de §7 (`--ablation` no se persiste) quedó RESUELTA.**
  `ablation: bool = False` es hoy un campo de `BenchmarkConfig` (`src/config.py`), `src/main.py` lo
  pasa al constructor (`ablation=args.ablation`) y `run_benchmark()` lo reconcilia antes de escribir
  `run_config.json`. La limitación solo aplica **retroactivamente** a las corridas #9 y #12, cuyos
  `run_config.json` siguen siendo indistinguibles de un baseline. El texto de §7 se conserva sin
  modificar por política aditiva.
- **N3 · *(2026-09-03)* Corrección a la nota de cierre del documento.** La nota final afirmaba que
  «no se aplicó ningún cambio a `src/main.py` ni a `src/config.py`». Eso dejó de ser cierto el mismo
  2026-09-03: ya están aplicados el guardrail de raíz (N1) y la persistencia de `ablation` (N2).
  Siguen **pendientes**: la convención de nombres de directorio (§4.1), `dataset_sha256`,
  `models_skipped` y el `results/runs_index.json` machine-readable (§4.2, reglas 2-4 de §4.3).
- **N4 · *(2026-09-03)* El conteo de «corridas con directorio propio» del §1 pasó de 5 a 7.**
  Al crear el índice existían 5 subdirectorios en `results/`; el mismo día aparecieron dos más, hoy
  catalogados como **#14** (`DESCARTADA_ragmode_incorrecto_142604`, descartada) y **#15**
  (`benchmark_balanced_120_kbrag_9models`, en ejecución). El conteo del §1 se corrigió en el sitio;
  ninguna fila fue eliminada.
- **N5 · 🪤 *(2026-09-03)* Trampa documentada: el default de `--rag-mode` NO es el modo de la
  corrida de referencia.** `src/main.py` declara `--rag-mode` con
  `default="entities"` y `choices=["entities","kb_guidelines","kb_fewshot","kb_combined"]`; el mismo
  default vive en `BenchmarkConfig.rag_mode`. La corrida de referencia de la tesina (#13) usó
  `kb_combined`. Por tanto `--rag-study` **sin** `--rag-mode` NO reproduce #13: ejecuta el dict-RAG
  legacy y produce condiciones `*_rag_enhanced` en vez de `*_kb_rag`. Es exactamente el error que
  obligó a descartar la corrida #14. Comando correcto en §5 y en `README.md` §2b.
- **N6 · *(2026-09-03)* Flag `--results-dir`.** Existe en `src/main.py` (default `None`). Sin él,
  cada corrida crea `results/<dataset>_<timestamp>/`. Es **obligatorio** junto con `--resume` para
  que el checkpoint se encuentre, y pasar `--results-dir results` aborta por la regla 1 de §4.3.

---

## 7. Limitaciones conocidas del versionado actual (estado al 2026-09-03)

1. **`--ablation` no se persiste.** El flag viaja como argumento de `run_benchmark()` y no forma
   parte de `BenchmarkConfig`, por lo que `run_config.json` de una corrida de configuraciones de prompt (#9, #12)
   es indistinguible de un baseline: dice `rag_study: false` y `system_prompt_file:
   SYSTEM_PROMPT.md`. Hoy solo se detecta leyendo la columna `model` del CSV.
2. **El nombre del directorio solo codifica dataset + timestamp** (`__post_init__` en
   `src/config.py`), no el modo ni el prompt.
3. **`rag_mode` es posterior a #11**: las corridas anteriores carecen del campo y deben leerse
   como `entities`.
4. **Corridas planas sobrescritas**: cuando `results_dir` era `results` (antes del esquema con
   timestamp) cada corrida pisaba a la anterior. Seis corridas del 2026-06/07 solo sobreviven
   como `.log` en la raíz del repo, incluida la N=30 titular.
5. **`results/` está en `.gitignore`** (junto con `data/` y `*.csv`), por lo que el histórico no
   está versionado. Solo `results/kb_rag_analysis_20260901.json` fue añadido con `git add -f`.
   Recomendación: excepciones explícitas para los artefactos livianos
   (`!results/RUNS_INDEX.md`, `!results/**/run_config.json`, `!results/**/statistical_report.md`,
   `!results/**/benchmark_summary.json`, `!results/**/acceptance_status.json`).
6. **Sin checksum del corpus**: si `data/benchmark_balanced_120.json` cambia, las corridas viejas
   dejan de ser comparables y nada lo delata.
7. **Modelos solicitados ≠ ejecutados**: `run_config.json` guarda la lista pedida; los omitidos
   (p. ej. `gpt-oss:20b` en #11) solo constan en `benchmark.log`.

> El diseño detallado de los cambios de código que resuelven estos siete puntos está en
> `doc/RUNS_VERSIONING_DESIGN.md`.
>
> ⚠️ **Corregido el 2026-09-03** (ver nota N3 de §6): este párrafo decía «documento de diseño; **no**
> se aplicó ningún cambio a `src/main.py` ni a `src/config.py`», lo cual ya no es cierto.
> **Aplicado**: guardrail `assert_not_results_root()` en `src/config.py` (resuelve la regla 1 de
> §4.3) y persistencia del campo `ablation` en `BenchmarkConfig` + `src/main.py` (resuelve la
> limitación 1 de arriba, salvo retroactivamente para #9 y #12).
> **Pendiente**: nomenclatura de directorios (§4.1), `dataset_sha256`, `models_skipped` y
> `results/runs_index.json` (§4.2 y reglas 2-4 de §4.3).

---

## Corridas del cierre (2026-09-06 / 2026-09-07)

Añadido de forma aditiva al cerrarse el estudio. El catálogo anterior llegaba hasta la corrida #13.

| Directorio | N | Modo RAG | Contenido |
|:---|:---:|:---|:---|
| `benchmark_n120_REMOTO` | 120 | `kb_combined` | Corrida principal del equipo remoto (P3), 7 modelos |
| `excluidos_n120_REMOTO` | 120 | `kb_combined` | `gpt-oss:20b` (recuperado tras el fix de routing) |
| `afectados_thinking_n120_REMOTO` | 120 | `kb_combined` | Re-corrida limpia de `gemma4:12b-mlx` tras el fix de *thinking* |
| `qwen3_nothink_n120_REMOTO` | 120 | `kb_combined` | `qwen3:8b` con `think=false` — **fuente oficial** del modelo |
| `nemotron_rerun_n120_REMOTO` | 120 | `kb_combined` | `nemotron-mini:4b`, 0 `failed` |
| `nemotron_fix7_REMOTO` | 7 | `kb_combined` | Parcheo de las 7 filas vacías (telemetría en cero, ver informe §5.3.5) |
| `gemma4_31b_cloud_n120_REMOTO` | 120 | `kb_combined` | `gemma4:31b-cloud` limpio, sin contaminación de cuota |
| `gemma4_31b_n15_REMOTO` | 15 | `entities` | `gemma4:31b` — fuente de su fila en la Tabla 2 |
| `cloud_n15_limpio_20260905` | 15 | `entities` | `gemma4:31b-cloud` — fuente de su fila en la Tabla 2 |
| `ablacion_n15_REMOTO` | 15 | `entities` | **Análisis de Variantes de Prompts** — fuente de §5.2 |
| `test_nothink/` | 15 | mixto | Experimento *thinking* ON/OFF de 4 modelos (`FINDINGS.md §F44-F45`) |
| **`ANALISIS_CONJUNTO_20260907`** | 120 | `kb_combined` | **Análisis conjunto definitivo: 13 modelos × 2 modos, F=36.3666, p=1.2236e-152.** Generado con `src/merge_and_analyze.py` |

> **Fuente válida de P/R/F1: `benchmark_results.csv`.** Todas las corridas se re-puntuaron tras corregir el bug
> del *scorer* (`F1=1.0` en extracción vacía). Ver `results/AVISO-SUMMARIES-OBSOLETOS.md`.
>
> **Alcance final del estudio: 13 modelos** — ver `CIERRE-BENCHMARKS-20260907.md`.
