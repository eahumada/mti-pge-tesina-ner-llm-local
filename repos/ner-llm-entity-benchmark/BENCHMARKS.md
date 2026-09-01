# NER‑LLM Entity Benchmark – How to Run

This document provides a quick‑start guide for running the benchmark suite located in this repository.

## Prerequisites

1. **Python 3.10+** – Ensure you have a compatible Python version installed.
2. **Ollama** – The benchmark uses local Ollama models. Make sure the Ollama server is running (`ollama serve`).
3. **Redis** – Required for the Pub/Sub coordination. Install via Homebrew:
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

Edit `results/run_config.json` to list the models you want to benchmark.  The file already contains a default list:

```json
{
  "models": [
    "gemma4-12b-mlx-q8-64k:latest",
    "sonct988/gemma4-26b-a4b-it-q4km-256k:latest",
    "gemma4:31b-mlx",
    "glm-5.1:cloud",
    "phi3.5:latest",
    "gemma:latest",
    "minimax-m3:cloud",
    "gemma4:31b-cloud",
    "llama3.1:8b",
    "nemotron-mini:4b",
    "gpt-oss:20b",
    "qwen2.5:14b",
    "mistral-nemo:latest",
    "qwen3:8b",
    "nuextract:latest",
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

*Feel free to add or remove model identifiers – they must match the names shown by `ollama list`. The configuration above tests the comprehensive list of all local/cloud models required for the baseline comparison.*

## Available Ollama Models (as of this run)

```
NAME                                           ID              SIZE      MODIFIED
gemma4-12b-mlx-q8-64k:latest                   5ceeaf26aced    7.7 GB    2 hours ago
gemma4:12b-mlx                                 117d0d84cf2a    7.7 GB    3 hours ago
gemma4:31b-mlx                                 637cc0ff1570    18 GB     3 weeks ago
gemma4:latest                                  c6eb396dbd59    9.6 GB    3 weeks ago
phi3.5:latest                                  61819fb370a3    2.2 GB    3 weeks ago
...
```
(Only the first few are shown; run `ollama list` for the full catalog.)

## Running the Benchmark

The repository ships a convenience script that launches the benchmark with the configuration above:

```bash
# Ensure the Redis server is running
redis-cli ping   # should return "PONG"

# Run the benchmark (this will start workers, publish tasks, and write results)
./run_benchmark.sh
```

Alternatively you can invoke the Python entry‑point directly:

```bash
python src/main.py --run-config results/run_config.json
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
- For each model, send prompts to the Ollama API, parse JSON responses, and store per‑record results in `results/detailed_results.json`.
- After all models finish, aggregated metrics are written to `results/summary_metrics.json`.

## Monitoring Progress

A cron job is set up to emit progress updates every minute.  You can also tail the log manually:

```bash
tail -f results/benchmark.log
```

## Post‑Processing

* **Metrics** – See `results/summary_metrics.json` for precision/recall/F1 per model.
* **Raw Results** – Detailed per‑record output is in `results/detailed_results.json`.
* **Visualization** – Use the `visualize_results.ipynb` notebook (included in `notebooks/`) to generate charts.

## Cleaning Up

To start a fresh run, delete the checkpoint file and previous results:

```bash
rm -f results/.checkpoint.json
rm -rf results/*.json
```

Then re‑run the benchmark.

---
*If you encounter model‑not‑found errors, make sure the model name matches exactly the string reported by `ollama list` and that the model is pulled (`ollama pull <model>`).*

## Latest Benchmark Results (July 24, 2026)

The following are the final benchmark performance results from the latest full sweep across all tested local models.

### Overall Performance Metrics

| Model | F1 | Precision | Recall | Hallucination % | Latency s | Throughput req/s |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| gemma4:31b-cloud | 0.6754 | 0.5659 | 0.8613 | 0.00% | 4.99 | 0.200 |
| gemma4:latest | 0.6676 | 0.6791 | 0.7852 | 0.00% | 29.57 | 0.034 |
| sonct988/gemma4-26b-a4b-it-q4km-256k:latest | 0.6525 | 0.5341 | 0.8595 | 0.91% | 74.93 | 0.013 |
| gemma4:31b-mlx | 0.6456 | 0.6149 | 0.8136 | 0.00% | 165.48 | 0.006 |
| minimax-m3:cloud | 0.6321 | 0.5948 | 0.8123 | 0.26% | 11.91 | 0.084 |
| llama3.2:latest | 0.6319 | 0.6282 | 0.6799 | 2.31% | 27.42 | 0.036 |
| gemma:latest | 0.6266 | 0.5847 | 0.7147 | 1.08% | 7.84 | 0.128 |
| qwen2.5:14b | 0.6106 | 0.5760 | 0.7176 | 0.87% | 86.14 | 0.012 |
| llama3.1:8b | 0.6072 | 0.5370 | 0.7580 | 3.39% | 55.70 | 0.018 |
| nuextract:latest | 0.5415 | 0.4869 | 0.4180 | 6.29% | 154.29 | 0.006 |
| qwen3:8b | 0.5365 | 0.6675 | 0.6561 | 0.00% | 63.76 | 0.016 |
| mistral-nemo:latest | 0.5307 | 0.5813 | 0.5600 | 0.83% | 54.34 | 0.018 |
| nemotron-mini:4b | 0.4199 | 0.4437 | 0.3492 | 2.62% | 22.42 | 0.045 |
| deepseek-r1:1.5b | 0.3431 | 0.3949 | 0.2577 | 1.35% | 43.76 | 0.023 |
| gemma4-12b-mlx-q8-64k:latest | 0.1206 | 0.9019 | 0.1528 | 0.00% | 148.55 | 0.007 |

*(Note: Throughput req/s is calculated as `1 / Latency_s`)*

### Prompt Ablation Study (gemma4:latest)

| Prompt Configuration | F1 | Precision | Recall | Hallucination % | Latency s | Throughput req/s |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| fs-en (Few-shot English) | 0.5874 | 0.6535 | 0.7073 | 0.74% | 256.61 | 0.004 |
| fs-es (Few-shot Spanish) | 0.7169 | 0.6320 | 0.8500 | 0.00% | 191.87 | 0.005 |
| zs-en (Zero-shot English) | 0.6482 | 0.6601 | 0.7810 | 0.00% | 84.70 | 0.012 |
| zs-es (Zero-shot Spanish) | 0.6640 | 0.5817 | 0.8108 | 0.19% | 84.56 | 0.012 |

### RAG Integration Study (llama3.2:latest & llama3.1:8b)

Injecting vector-retrieved context from local organizational and personal dictionaries improves overall model F1 without extending the context window significantly. 

**Proceso de Iteración para llama3.1:latest (8b):**
1. **Línea Base:** Se evaluó el modelo sin diccionarios externos, resultando en un Recall aceptable (0.90) pero con Precision baja (0.56) y F1 de ~0.76.
2. **Primera Iteración (SDN OFAC + Fortune 500):** Se incorporaron diccionarios de sanciones (OFAC) y nombres comunes/Fortune 500. Se logró un Recall perfecto de 1.0, subiendo la precisión a 0.66, lo que mejoró el F1 ligeramente a 0.775. No obstante, surgieron falsos positivos (alucinaciones) dado que el modelo asumió que cualquier entidad en el RAG debía ser extraída.
3. **Segunda Iteración (Mejora del Prompt y Nuevos Diccionarios):** Se ajustó el sistema RAG para incluir instrucciones más estrictas ("STRICT INSTRUCTION: DO NOT extract them unless they explicitly appear in the text"). Esto redujo las alucinaciones a ~4%, con F1 estabilizado en ~0.75 y Precision en 0.63. 
4. **Capacidad Out-Of-Vocabulary (OOV):** En todas las pruebas, la métrica `oov_recall` evaluó la capacidad del modelo de extraer entidades fuera de los diccionarios inyectados. En nuestro corpus de prueba de 20 records, la tasa de OOV final tendió a cero, lo cual indica que el modelo no fue forzado significativamente a reconocer entidades no sancionadas o genéricas debido a la cobertura de los diccionarios, pero también revela que su desempeño general F1 (+0.01 mejora real frente a la meta del +0.10) está limitado por la falta de un corpus de prueba más extenso y/o necesidad de afinamiento (Fine-Tuning/Few-Shot).

| Modelo y Configuración | F1 | Precision | Recall | Hallucination % | Latency s | Throughput req/s | OOV Recall |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| llama3.2:latest_baseline | 0.8250 | 0.8417 | 0.8500 | 0.00% | 1.02 | 0.98 | 0.00 |
| llama3.2:latest_rag | 0.8783 | 0.6792 | 0.8500 | 5.42% | 1.02 | 0.98 | 0.00 |
| llama3.1:8b_baseline | 0.7667 | 0.5667 | 0.9000 | 0.00% | 15.21 | 0.06 | 0.00 |
| llama3.1:8b_rag_enhanced | 0.7750 | 0.6667 | 1.0000 | 7.50% | 3.85 | 0.25 | 0.00 |
| llama3.1:8b_rag_strict_prompt | 0.7500 | 0.6333 | 1.0000 | 4.16% | 3.23 | 0.30 | 0.00 |
