# Named Entity Recognition (NER) Compliance Benchmark Pipeline

This repository implements a high-performance, secure, and sovereign batch-processing system to evaluate local open-source Large Language Models (Gemma, DeepSeek, LLaMA) on sanctions-related compliance news.

---

## 🚀 Environment Setup & Installation

The project uses a unified shell script to set up all native dependencies, the Python virtual environment (`venv`), and pull necessary models:

```bash
./setup.sh
```

### Script Actions
1. **OS Detection:** Automatically identifies Linux, macOS, or Windows/WSL environments.
2. **Native dependencies:** Installs the local `ollama` backend via Homebrew (Mac) or official installer script (Linux).
3. **Virtual Environment:** Configures a dedicated Python `venv` to enforce isolated library installations.
4. **Model Pulling:** Retrieves the default model locally — `setup.sh` runs `ollama pull gemma4`, which resolves to the tag **`gemma4:latest`** (9.6 GB). *(Corrected 2026-09-03: this line used to gloss it as "Gemma 2 9B", a different family from the `gemma4` artefacts — 12b/31b included — used throughout this project.)*

---

## 🏃 Running the Pipeline

### 1. Activate the Virtual Environment
Before executing any scripts, ensure the `venv` is active:
```bash
source venv/bin/activate
```

### 2. Run the Benchmark Sweep
Evaluate a model sweep on the primary balanced Kleptotrace/CoNLL-2002 dataset:
```bash
python src/main.py --models gemma4 --data-file data/benchmark_balanced_120.json --batch-size 3
```

### 2b. Run the RAG study (baseline vs. Knowledge-Base RAG)

`--rag-study` runs every model **twice** (without and with retrieval). The retrieval strategy is
chosen with `--rag-mode`.

> ⚠️ **Flag trap — `--rag-mode` defaults to `entities`, NOT to the mode of the reference run.**
> `entities` is the legacy dictionary-RAG kept for backward compatibility. The thesis' reference run
> (`results/benchmark_balanced_120_20260901_140421`, catalogued as **#13** in
> `results/RUNS_INDEX.md`) used **`kb_combined`**. Omitting `--rag-mode` reproduces a *different*
> experiment that silently looks the same on the command line. A run started on 2026-09-03 was
> discarded for exactly this reason (`results/DESCARTADA_ragmode_incorrecto_142604/`).

Exact command of the reference run #13 (5 models x {baseline, kb_rag} x N=120 = 1200 rows):

```bash
python src/main.py --data-file data/benchmark_balanced_120.json \
  --rag-study --rag-mode kb_combined \
  --models llama3.2:latest gemma4:latest gemma4:31b-mlx qwen2.5:14b gemma:latest \
  --batch-size 3 --num-workers 9
```

Valid values: `entities` (legacy dict), `kb_guidelines`, `kb_fewshot`, `kb_combined` (best F1).

### 2c. Run the Prompt Configuration Comparison (`--ablation`)

Also referred to as the 2x2 factorial design / prompt ablation study. One model is swept across the
four prompt conditions (zs-en, zs-es, fs-en, fs-es) in a single run:

```bash
python src/main.py --ablation --data-file data/benchmark_balanced_120.json \
  --models gemma4:latest --batch-size 3
```

### 2d. Where results are written (`--results-dir`)

By default **no flag is needed**: each run creates its own `results/<dataset>_<timestamp>/`
directory. Pass `--results-dir` only to name the directory yourself, and note the two rules:

- `--resume` needs `--results-dir` pointing at the previous run's directory, otherwise the run
  starts fresh in a new timestamped directory instead of picking up its checkpoint.
- Passing `--results-dir results` (the ROOT) **aborts** with `ResultsDirRootError`. Writing to the
  root is what destroyed the per-record data of the N=30 headline run in 2026-07. Always use a
  subdirectory.

### 3. Run simulated daily batches
Simulate production compliance feeds:
```bash
python src/simulate_production.py
```

### 4. Run Inter-Annotator Agreement Check
Evaluate Cohen's Kappa score on ground truth classifications:
```bash
python src/main.py --compare-annotators data/sample_an1.json data/sample_an2.json
```

### 5. Run Memory Stability Stress Test
Cycle model loading and unloading to verify footprint bounds:
```bash
python src/memory_stress_test.py
```

### 6. Launch the Streamlit Dashboard
Visualize KPIs, ANOVA significance tests, sensitivity analysis, and qualitative feedback panels:
```bash
streamlit run src/dashboard.py
```
