# NER‑LLM Entity Benchmark – How to Run

This document provides a quick‑start guide for running the benchmark suite located in this repository.

## Prerequisites

1. **Python 3.10+** – Ensure you have a compatible Python version installed.
2. **Ollama** – The benchmark uses local Ollama models. Make sure the Ollama server is running (`ollama serve`).
3. **Redis** – *Opcional*. Solo se usa si se activa `RedisTaskQueue` (`src/pub_sub.py:86`): las cuatro rutas de `src/main.py` llaman `create_task_queue(use_redis=False)`, así que ninguna corrida catalogada lo requiere. Si se activa:
   ```bash
   brew install redis
   brew services start redis
   ```
4. **Git** – To fetch the repository if you haven't already.

## Setup the Project

```bash
# Clone the repository (if not already cloned)
git clone https://github.com/your-org/ner-llm-entity-benchmark.git
cd ner-llm-entity-benchmark

# Create a virtual environment and activate it
python -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

## Configure the Benchmark

La lista de modelos se define en `src/config.py` (campo `BenchmarkConfig.models`, línea 59) o se sobreescribe en la invocación con `--models`. **`results/<run_dir>/run_config.json` no es un archivo de entrada**: `src/main.py:190` lo *escribe* al arrancar la corrida como artefacto de reproducibilidad y ningún módulo lo lee. La configuración efectiva equivale a:

```json
{
  "models": [
    "sonct988/gemma4-26b-a4b-it-q4km-256k:latest",
    "gemma4:31b-mlx",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash",
    "phi3.5:latest",
    "gemma4:latest",
    "gemma:latest",
    "gemma4:31b-cloud",
    "llama3.1:8b",
    "nemotron-mini:4b",
    "gpt-oss:20b",
    "qwen2.5:14b",
    "mistral-nemo:latest",
    "qwen3:8b",
    "deepseek-r1:1.5b",
    "llama3.2:latest",
    "gemma4:12b-mlx"
  ],
  "batch_size": 3,
  "num_workers": 1,
  "max_retries": 2,
  "fuzzy_threshold": 85,
  "redis_url": "redis://localhost:6379",
  "data_file": "data/benchmark_balanced_120.json",
  "results_dir": "results",
  "checkpoint_file": "results/.checkpoint.json",
  "system_prompt_file": "SYSTEM_PROMPT.md",
  "ollama_base_url": "http://localhost:11434",
  "temperature": 0.1,
  "max_tokens": 2048,
  "seed": 42
}
```

*Feel free to add or remove model identifiers – they must match the names shown by `ollama list`. The configuration above tests the comprehensive list of all local/cloud models required for the baseline comparison. La lista canónica vive en `src/config.py:59` y en AGENTS.md §8.6; `run_benchmark.sh` lleva además su propia lista fija (líneas 25-40) que, al pasarse por `--models`, sobreescribe a `config.models`. Esta lista no coincide una a una con las filas de las tablas de resultados: cada tabla declara abajo su propio `run_id`, corpus, N y conjunto de modelos.*

## Available Ollama Models (as of this run)

```
NAME                                           ID              SIZE      MODIFIED
gemma4:12b-mlx                                 117d0d84cf2a    7.7 GB    3 hours ago
gemma4:31b-mlx                                 637cc0ff1570    18 GB     3 weeks ago
gemma4:latest                                  c6eb396dbd59    9.6 GB    3 weeks ago
phi3.5:latest                                  61819fb370a3    2.2 GB    3 weeks ago
...
```
(Only the first few are shown; run `ollama list` for the full catalog.)

## Running the Benchmark

The repository ships a convenience script. **`./run_benchmark.sh` no lee la configuración de arriba**: encadena tres pasos con listas propias (`run_benchmark.sh:22-47`):

1. Barrido `--rag-study` sobre `data/benchmark_balanced_120.json` con 16 modelos fijos vía `--models` y `--batch-size 3` (el `echo` de la línea 21 dice "15 models"; son 16).
2. Análisis comparativo de prompts: `--ablation` sobre `gemma4:latest`, mismo corpus y `--batch-size 3`.
3. Simulación de flujo productivo: `src/simulate_production.py`.

```bash
# Run the benchmark (this will start workers, publish tasks, and write results)
./run_benchmark.sh
```

Alternatively you can invoke the Python entry‑point directly:

```bash
python src/main.py --data-file data/benchmark_balanced_120.json --models gemma4:latest --batch-size 3
```

**Testing RAG Integration:**
To evaluate the impact of Retrieval-Augmented Generation (RAG) using local entity dictionaries:
```bash
python src/main.py --rag-study
```
This automatically runs all models for two cycles: a baseline cycle without RAG, and a second cycle where context from ChromaDB is injected into the prompt.

The script will:
- Load the system prompt (`SYSTEM_PROMPT.md`).
- Split the dataset into batches (as defined by `batch_size`).
- Spin up the number of worker threads specified by `num_workers`.
- For each model, send prompts to the Ollama API, parse JSON responses, and store per‑record results in `results/<dataset>_<timestamp>/detailed_results.json`.
- After all models finish, aggregated metrics are written to `results/<dataset>_<timestamp>/benchmark_summary.json` (`src/main.py:178`).

## Monitoring Progress

A cron job is set up to emit progress updates every minute.  You can also tail the log manually:

```bash
tail -f results/<dataset>_<timestamp>/benchmark.log
```

## Post‑Processing

* **Metrics** – See `results/<dataset>_<timestamp>/benchmark_summary.json` for precision/recall/F1 per model.
* **Raw Results** – Detailed per‑record output is in `results/<dataset>_<timestamp>/detailed_results.json` y `benchmark_results.csv`.
* **Visualization** – `streamlit run src/dashboard.py` (lee `benchmark_summary.json`; ver README §6). El notebook `visualize_results.ipynb` que citaba esta línea nunca existió en el repositorio.

## Cleaning Up

**No se borra nada.** Cada corrida crea su propio directorio `results/<dataset>_<timestamp>/` con su checkpoint (`src/config.py:98-107`) y `assert_not_results_root` (líneas 31-54) aborta cualquier intento de escribir en la raíz, así que no queda estado que limpiar entre corridas.

Los comandos `rm -f results/.checkpoint.json` y `rm -rf results/*.json` que documentaba esta sección quedan **derogados**: borrarían evidencia histórica, incluido `results/kb_rag_analysis_20260901.json`, único artefacto de `results/` versionado en git (RUNS_INDEX.md §4.3, regla 4: los directorios históricos no se borran).

Para retomar una corrida interrumpida, use `--resume --results-dir <dir>`. El flag `--results-dir`
es **obligatorio** junto a `--resume`: sin él, cada ejecución crea un directorio nuevo con timestamp
y el checkpoint nunca se encuentra, reiniciando la corrida desde cero en silencio (ver `FINDINGS.md §F2`).

---
*If you encounter model‑not‑found errors, make sure the model name matches exactly the string reported by `ollama list` and that the model is pulled (`ollama pull <model>`).*

## Historical Benchmark Results — corrida #8 (2026-07-27)

Tabla histórica. Su origen trazable es la corrida `klepto_N15__rag-entities__zs-en__20260727_1104` (RUNS_INDEX.md #8, corpus `kleptotrace.json`, **N=15**, prompt `zs-en`, evidencia plana en `results/`), de la que reproduce las condiciones `_baseline`. No corresponde al 24 de julio (RUNS_INDEX.md no cataloga ninguna corrida de esa fecha) ni al último barrido: el vigente es la corrida #13, más abajo.

### Overall Performance Metrics (corrida #8, N=15, condiciones `_baseline`)

| Model | F1 | Precision | Recall | Hallucination % | Latency s | Throughput req/s |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud ⚠️ | 0.6754 | 0.5659 | 0.8613 | 0.00% | 4.99 | 0.200 |
| gemma4:latest | 0.6676 | 0.6791 | 0.7852 | 0.00% | 29.57 | 0.034 |
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest | 0.6525 | 0.5341 | 0.8595 | 0.91% | 74.93 | 0.013 |
| gemma4:31b-mlx ⚠️ | 0.6456 | 0.6149 | 0.8136 | 0.00% | 165.48 | 0.006 |
| llama3.2:latest | 0.6319 | 0.6282 | 0.6799 | 2.31% | 27.42 | 0.036 |
| gemma:latest | 0.6266 | 0.5847 | 0.7147 | 1.08% | 7.84 | 0.128 |
| qwen2.5:14b | 0.6106 | 0.5760 | 0.7176 | 0.87% | 86.14 | 0.012 |
| llama3.1:8b | 0.6072 | 0.5370 | 0.7580 | 3.39% | 55.70 | 0.018 |
| qwen3:8b | 0.5365 | 0.6675 | 0.6561 | 0.00% | 63.76 | 0.016 |
| mistral-nemo:latest | 0.5307 | 0.5813 | 0.5600 | 0.83% | 54.34 | 0.018 |
| nemotron-mini:4b | 0.4199 | 0.4437 | 0.3492 | 2.62% | 22.42 | 0.045 |
| deepseek-r1:1.5b | 0.3431 | 0.3949 | 0.2577 | 1.35% | 43.76 | 0.023 |

*(Note: Throughput req/s is calculated as `1 / Latency_s`)*

> **Retirado del estudio (2026-09-05, decisión del autor).** `minimax-m3:cloud` se elimina del
> benchmark: su única medición tenía **9 de 15 extracciones fallidas por cuota** (N efectiva = 6) y
> **no es re-ejecutable** — devuelve HTTP 402 por requerir plan de pago. Un resultado con 60 % de
> fallo y sin posibilidad de repetición no es defendible. Ver `FINDINGS.md §F38`.

> **Retirado del estudio (2026-09-06, decisión del autor).** `nuextract:latest` se elimina del
> benchmark. Es un extractor de plantilla, no un modelo generalista: **109 de 120 extracciones**
> requirieron el parser de respaldo por su formato propio. Aunque ese respaldo rescataba contenido
> con F1 normal, se retira para que el barrido compare modelos generalistas en igualdad de
> condiciones de formato de salida. Ver `FINDINGS.md §F43`.

> ⚠️ **Trazabilidad.** Once de las catorce filas reproducen exactamente (F1/Precision/Recall) las condiciones `_baseline` de `results/benchmark_summary.json` (corrida #8). Las tres marcadas ⚠️ no: el archivo crudo da `gemma4:31b-cloud` F1 0.3973 / P 0.7284 / R 0.5233, `gemma4:31b-mlx` F1 0.6852 / P 0.5831 / R 0.8676 y `minimax-m3:cloud` F1 0.2011 / P 0.8396 / R 0.2434. Las latencias tampoco coinciden fila a fila con el crudo. Se conservan tal cual y se marcan; su corrección requiere decisión del autor sobre cuál es la fuente válida. Los dos modelos *cloud* ya no son re-ejecutables (cuota semanal 429 y suscripción de pago 402).

### Latest Benchmark Results — corrida #13 `balanced120_N120__rag-kb-combined__zs-en__20260901_140421`

Barrido vigente: corpus `data/benchmark_balanced_120.json`, **N=120**, prompt `zs-en`, `rag_mode: kb_combined` (KB RAG contextual v1.1.0), 5 modelos × {`baseline`, `kb_rag`} = 10 condiciones y 1200 filas. Evidencia: `results/benchmark_balanced_120_20260901_140421/` y `results/kb_rag_analysis_20260901.json`. ANOVA **F=10.2096, p=2.8730e-15**.

| Modelo y Configuración | F1 | Precision | Recall | Hallucination % | Latency s | Throughput req/s |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| gemma4:31b-mlx_baseline | 0.5925 | 0.5373 | 0.7569 | 0.49% | 1066.21 | 0.0009 |
| gemma4:31b-mlx_kb_rag | 0.5907 | 0.5501 | 0.7692 | 0.41% | 1408.55 | 0.0007 |
| qwen2.5:14b_kb_rag | 0.5651 | 0.5548 | 0.6124 | 0.72% | 173.83 | 0.0058 |
| gemma4:latest_baseline | 0.5591 | 0.5291 | 0.6720 | 0.85% | 98.03 | 0.0102 |
| gemma4:latest_kb_rag | 0.5558 | 0.5212 | 0.6609 | 0.53% | 489.56 | 0.0020 |
| gemma:latest_kb_rag | 0.5303 | 0.5231 | 0.5995 | 5.96% | 103.36 | 0.0097 |
| qwen2.5:14b_baseline | 0.5189 | 0.5029 | 0.5735 | 1.32% | 159.39 | 0.0063 |
| llama3.2:latest_kb_rag | 0.4943 | 0.4892 | 0.5514 | 3.83% | 5.88 | 0.1700 |
| gemma:latest_baseline | 0.4734 | 0.4983 | 0.4831 | 0.84% | 93.63 | 0.0107 |
| llama3.2:latest_baseline | 0.3945 | 0.4018 | 0.4081 | 2.74% | 5.17 | 0.1933 |

Δ F1 (`kb_rag` − `baseline`): `llama3.2:latest` +9.98 pp, `gemma:latest` +5.69 pp, `qwen2.5:14b` +4.62 pp, `gemma4:latest` −0.33 pp, `gemma4:31b-mlx` −0.18 pp. Mejor F1 absoluto: `gemma4:31b-mlx_baseline` 0.5925.

### Análisis Comparativo de Prompts (gemma4:latest) — cifras sin corrida de origen

⚠️ Las cuatro filas siguientes no son trazables a ningún artefacto del repositorio (`0.7169`, `0.6482` y `0.5874` solo aparecen aquí). Se conservan como registro y se contrastan con las dos corridas de configuraciones de prompt catalogadas, que sí tienen evidencia completa.

| Prompt Configuration | F1 | Precision | Recall | Hallucination % | Latency s | Throughput req/s |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| fs-en (Few-shot English) | 0.5874 | 0.6535 | 0.7073 | 0.74% | 256.61 | 0.004 |
| fs-es (Few-shot Spanish) | 0.7169 | 0.6320 | 0.8500 | 0.00% | 191.87 | 0.005 |
| zs-en (Zero-shot English) | 0.6482 | 0.6601 | 0.7810 | 0.00% | 84.70 | 0.012 |
| zs-es (Zero-shot Spanish) | 0.6640 | 0.5817 | 0.8108 | 0.19% | 84.56 | 0.012 |

**Cifras verificadas** (leídas de `benchmark_summary.json` de cada corrida; `gemma4:latest`, 4 configuraciones de prompt):

| Corrida | Prompt | F1 | Precision | Recall | Hallucination % | Latency s | Throughput req/s |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| #9 `klepto_N15__ablation__4-prompts__20260727_110454` (N=15) | fs-es | 0.6987 | 0.6162 | 0.8416 | 0.86% | 185.80 | 0.0054 |
| #9 (N=15) | zs-es | 0.6793 | 0.6055 | 0.8180 | 0.19% | 87.78 | 0.0114 |
| #9 (N=15) | zs-en | 0.6676 | 0.6791 | 0.7852 | 0.00% | 80.41 | 0.0124 |
| #9 (N=15) | fs-en | 0.5817 | 0.6436 | 0.7076 | 1.04% | 248.27 | 0.0040 |
| #12 `balanced120_N120__ablation__4-prompts__20260825_071207` (N=120) | zs-es | 0.5562 | 0.5190 | 0.6786 | 0.77% | 506.72 | 0.0020 |
| #12 (N=120) | fs-en | 0.5450 | 0.5161 | 0.6528 | 1.10% | 493.92 | 0.0020 |
| #12 (N=120) | zs-en | 0.5446 | 0.5247 | 0.6539 | 0.73% | 99.95 | 0.0100 |
| #12 (N=120) | fs-es | 0.5402 | 0.5135 | 0.6459 | 0.76% | 492.51 | 0.0020 |

ANOVA: #9 F=1.0248, p=0.3886; #12 F=0.1451, p=0.9328 — en ninguna de las dos la configuración de prompt resulta significativa.

### RAG Integration Study (llama3.2:latest & llama3.1:8b)

Injecting vector-retrieved context from local organizational and personal dictionaries improves overall model F1 without extending the context window significantly. 

**Proceso de Iteración para llama3.1:8b:**
1. **Línea Base:** Se evaluó el modelo sin diccionarios externos, resultando en un Recall aceptable (0.90) pero con Precision baja (0.56) y F1 de ~0.76.
2. **Primera Iteración (SDN OFAC + Fortune 500):** Se incorporaron diccionarios de sanciones (OFAC) y nombres comunes/Fortune 500. Se logró un Recall perfecto de 1.0, subiendo la precisión a 0.66, lo que mejoró el F1 ligeramente a 0.775. No obstante, surgieron falsos positivos (alucinaciones) dado que el modelo asumió que cualquier entidad en el RAG debía ser extraída.
3. **Segunda Iteración (Mejora del Prompt y Nuevos Diccionarios):** Se ajustó el sistema RAG para incluir instrucciones más estrictas ("STRICT INSTRUCTION: DO NOT extract them unless they explicitly appear in the text"). Esto redujo las alucinaciones a ~4%, con F1 estabilizado en ~0.75 y Precision en 0.63. 
4. **Capacidad Out-Of-Vocabulary (OOV):** En todas las pruebas, la métrica `oov_recall` evaluó la capacidad del modelo de extraer entidades fuera de los diccionarios inyectados. En nuestro corpus de prueba de 20 records, la tasa de OOV final tendió a cero, lo cual indica que el modelo no fue forzado significativamente a reconocer entidades no sancionadas o genéricas debido a la cobertura de los diccionarios, pero también revela que su desempeño general F1 (+0.01 mejora real frente a la meta del +0.10) está limitado por la falta de un corpus de prueba más extenso y/o necesidad de afinamiento (Fine-Tuning/Few-Shot).

| Modelo y Configuración | F1 | Precision | Recall | Hallucination % | Latency s | Throughput req/s | OOV Recall |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| llama3.2:latest_baseline | 0.8250 | 0.8417 | 0.8500 | 0.00% | 1.02 | 0.98 | 0.00 |
| llama3.2:latest_rag ⚠️ | 0.8783 | 0.6792 | 0.8500 | 5.42% | 1.02 | 0.98 | 0.00 |
| llama3.1:8b_baseline ⚠️ | 0.7667 | 0.5667 | 0.9000 | 0.00% | 15.21 | 0.06 | 0.00 |
| llama3.1:8b_rag_enhanced | 0.7750 | 0.6667 | 1.0000 | 7.50% | 3.85 | 0.25 | 0.00 |
| llama3.1:8b_rag_strict_prompt | 0.7500 | 0.6333 | 1.0000 | 4.16% | 3.23 | 0.30 | 0.00 |

> ⚠️ **Consistencia aritmética.** El F1 de esta tabla es la media de los F1 por registro (`src/evaluator.py:357-359` promedia f1, precision y recall por separado), no un F1 derivado de la P y la R agregadas. Aun así, como `f1_i ≤ (p_i+r_i)/2` para todo registro, se cumple `mean(F1) ≤ (mean(P)+mean(R))/2`. Las dos filas marcadas ⚠️ violan esa cota: `llama3.2:latest_rag` (cota 0.7646 < 0.8783) y `llama3.1:8b_baseline` (cota 0.7334 < 0.7667). `llama3.1:8b_rag_enhanced` sí es consistente (cota 0.8334 ≥ 0.7750). Estas cifras corresponden a prototipos tempranos sobre el sample de 20 registros (`data/sample_sanctions.json`), cuyo CSV no sobrevive; no se pueden recalcular y quedan pendientes de decisión del autor. La tabla tampoco declara `run_id` ni figura en RUNS_INDEX.md.
