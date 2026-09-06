# Agent Instructions for NER-LLM-Entity-Benchmark

**IMPORTANT**: Do not remove or modify existing content in documentation or codebase files without explicit user confirmation. Maintain consistency with all previous work.

Welcome! If you are an AI agent (like Claude, Gemini, or Antigravity) working on this project, please adhere to the following guidelines and consult the referenced documents before writing code or altering the architecture.

## 1. Project Context
This project is an automated batch-processing system designed to evaluate the Named Entity Recognition (NER) capabilities of local open-source Large Language Models (Gemma, DeepSeek, LLaMA) on compliance and sanctions-related news in English (sourced from OpenSanctions).

- **Main Architecture & Overview:** Read [`PROJECT_PROMPT.md`](./PROJECT_PROMPT.md)
- **Functional Requirements:** Read [`doc/REQUERIMENTS/functional_requirements.md`](./doc/REQUERIMENTS/functional_requirements.md)
- **Non-Functional Requirements:** Read [`doc/REQUERIMENTS/non_functional_requirements.md`](./doc/REQUERIMENTS/non_functional_requirements.md)
- **LLM Prompt Engineering:** Read [`SYSTEM_PROMPT.md`](./SYSTEM_PROMPT.md)

## 2. Architectural Guidelines & Guardrails
- **Pub/Sub Required:** Do NOT implement synchronous sequential batching. The project strictly requires a local Pub/Sub architecture (e.g., Redis, Celery, ZeroMQ) to decouple ingestion from LLM execution, allowing for scalability and fault tolerance/resumability.
- **Privacy Constraints:** NEVER send news data to external APIs (e.g., OpenAI, Google Cloud NLP) for NER processing. The system must operate with zero-data-leakage using strictly local execution (Ollama/vLLM).
  - **Excepción autorizada (2026-09-03, autorizada explícitamente por el autor):** Se habilita el uso de los modelos *Ollama Cloud* `gemma4:31b-cloud` y `minimax-m3:cloud` **exclusivamente como línea base de comparación** en el benchmark académico sobre `data/benchmark_balanced_120.json`. Implicancia explícita: los 120 artículos del corpus se transmiten a servidores remotos de Ollama. Esta excepción **no deroga** la regla anterior, que sigue vigente para todo dato productivo, de clientes o de la Compañía; aplica sólo al corpus público de evaluación (Kleptotrace + CoNLL-2002), que no contiene datos personales ni confidenciales. Cualquier otro uso de APIs externas sigue prohibido.
- **GPU Memory Management:** Explicitly manage model lifecycles (unloading weights) when switching between models to prevent OOM crashes.
- **JSON Fallbacks:** Always implement regex fallbacks and automatic retries for LLM outputs, as JSON hallucination is an identified critical risk.

## 3. Workflow
Always ensure that modifications align with the metrics targets: F1-Score > 85% and Hallucination Rate < 5%. Verify changes against the existing functional and non-functional requirements.

## 4. Key Implementation Findings
Below is a summary of findings and updates developed during the final integration phase:

- **Adaptive Dataset Loader (US01 / Phase 1):** The data loader in `src/data_loader.py` now automatically detects and adapts standard JSON structures (such as Kleptotrace/CoNLL-2002) alongside the FollowTheMoney (FtM) JSONL format, as well as TSV/IOB column structures and XML schemas (with `<PER>`, `<ORG>`, and `<LOC>` tags).
- **Inter-Annotator Agreement (US02 / Phase 1):** Implemented Cohen's Kappa score for annotations. Running `python src/main.py --compare-annotators file1.json file2.json` aligns categorizations and calculates agreement, logging warnings if Kappa is below 0.75.
- **Spanish & LatAm Localization (US15 / Phase 2):** Created `SYSTEM_PROMPT_ES.md` specifically structured for Spanish compliance context and Latin American identifiers (e.g. RUT, RFC, RUN). It can be loaded using `--system-prompt-file SYSTEM_PROMPT_ES.md`.
- **Sensitivity Analysis (US17 / Phase 5):** Evaluated outlier robustness in statistical testing. Outliers (texts where length is greater than mean + 500 characters) are isolated. During a run with `gemma4` on Kleptotrace/CoNLL-2002:
  * Standard F1: **42.41%**
  * Cleaned F1 (Filtered Outliers): **50.84%**
  * Performance Delta: **+8.43 percentage points** (50.84 - 42.41); expressed as a relative gain that is **+19.9%**. *(Corrected 2026-09-03: the previous text read "+8.42%", an arithmetic slip that also mislabelled percentage points as percent.)*
- **Automated System Acceptance Check (US16 / Phase 6):** Run outputs are validated against thresholds and saved in `results/acceptance_status.json`. If F1 target of 85% is unmet or hallucination rates exceed 5%, warning banners are dynamically flagged on top of the dashboard.
- **Simulated Production Batch Validation (US18 / Phase 6):** Developed `src/simulate_production.py` to process news article feeds through mock LLM workers. Reconstructed pipeline metrics and logged qualitative feedback are integrated in Tab 6 of the Streamlit dashboard (`src/dashboard.py`).
- **Strict Ingestion Validation & CSV Support (FR5.1 / Phase 1):** Built `validate_record_schema` checks in `data_loader.py` enforcing strict type, key, and length assertions. Added CSV parsing using Python's standard `csv` library.
- **Memory Stability Stress Test (NFR3.3 / RNF2.2 / Phase 2):** Developed `src/memory_stress_test.py` which loads/unloads Ollama model weights in loops. Process memory leak footprint measured at only `+0.20 MB` over 5 cycles, confirming engine lifecycle stability.

## 5. Pending Tasks & Next Steps
Future agents should prioritize the remaining pending items from the master `TODO.md` to finalize the system for the academic thesis:

1. **Large-Scale Experimentation:**
   - Expand evaluation sweeps from the 20-record prototype sample to the full financial compliance sanctions dataset.
   - Run benchmark sweeps across multiple local LLMs (Gemma, DeepSeek, LLaMA) using the local Ollama backend to produce statistical comparison traces.
   - Benchmark models against the manual F1 baseline (75-80%) to mathematically validate improvement.
2. **Academic Reporting & Stats:** Produce the final thesis validation report including pairwise Adjusted p-values from Tukey HSD and confusion matrices segmented by entity type (Person, Org, Loc) once large-scale results are fully generated.

> ✅ **Status update (2026-09-03).** Both items above are **already executed**; they are kept here for
> traceability, not as open work.
> - Item 1 — the sweep left the 20-record prototype long ago: run **#11**
>   (`balanced120_N120__rag-entities__zs-en__20260824_173036`, 15 models, 3600 rows) and run **#13**
>   (`balanced120_N120__rag-kb-combined__zs-en__20260901_140421`, 5 models, 1200 rows, ANOVA
>   F=10.2096, p=2.87e-15) both ran on `data/benchmark_balanced_120.json` (N=120).
> - Item 2 — `run_tukey_posthoc` is imported and executed in `src/main.py`, and every run writes
>   `confusion_matrix.json` into its own results directory.
> - The run catalogue is `results/RUNS_INDEX.md` (run ids referenced above).
> - ⚠️ The "master `TODO.md`" referenced in this section is **not** the repo's `TODO.md`: that file
>   tracks only the RAG implementation plan and contains none of these items.

## 6. Documentation & Thesis Evidence (WORKLOG)
The project requires a rigorous audit trail for academic validation.
- **Worklog Maintenance**: Every agent MUST update `WORKLOG.md` at the end of their task.
- **Content Requirements**: 
    - Summarize all changes, research, and experiments.
    - Map implementation decisions back to specific requirements (`doc/REQUERIMENTS/`) or project sources (`doc/sources/`).
    - Provide quantitative evidence (e.g., "F1 improved from X to Y") whenever possible.
- **Purpose**: This worklog is the foundational data for the thesis; it must be detailed enough for a third party to reconstruct the development process and validate the results.

## 7. Backlog Tracking (BACKLOG.md)
Every agent MUST log resolved issues, bugs, and performance optimization details inside `BACKLOG.md` located at the workspace root to ensure a transparent engineering history.

---

## 8. Model Management — Add / Remove Models

> **For agents**: This section is the single source of truth. Read this before touching any model list.

### 8.1 — The only file you need to edit

The canonical model list lives in **one file**:

```
src/config.py  →  BenchmarkConfig.models   (dataclass field, line ~59: models: list[str] = field(default_factory=lambda: [...]))
```

> ⚠️ **Corrected 2026-09-03.** This section previously pointed at
> `BenchmarkConfig.__post_init__ → self.models = [...]`. `__post_init__` does **not** define the
> model list: it only derives `results_dir` / `checkpoint_file` and calls `assert_not_results_root()`.
>
> ⚠️ **"No other file needs to be changed" is false.** `run_benchmark.sh` (lines 25-40) hardcodes its
> own model list and passes it via `--models`, which **overrides** `config.models`
> (`src/main.py`: `if args.models: config.models = args.models`). Keep both in sync, or the sweep will
> silently ignore your edit to `src/config.py`. The pipeline auto-routes each name to its provider.

---

### 8.2 — Model type classification (MUST determine before adding)

| Type | Name pattern | Pulled locally? | VRAM managed? | Needs `ollama pull`? |
|------|-------------|-----------------|---------------|----------------------|
| **Local** | any Ollama name that does NOT contain `-cloud` nor `minimax` | ✅ Yes | ✅ Yes (unloaded after run) | ✅ Yes |
| **Cloud (Ollama)** | name **contains** `-cloud` OR **contains** `minimax` (substring, any position) | ❌ No (served remotely) | ❌ No (skip VRAM ops) | ❌ **No** — served remotely, nothing to pull |
| **NuExtract** | `nuextract`, `nuextract:*` | ✅ Yes | ✅ Yes | ✅ Yes |
| **Qwen3 (thinking)** | `qwen3:*` | ✅ Yes | ✅ Yes | ✅ Yes |
| **Gemini (Vertex/AI Studio)** | `gemini-*`, `vertexai:*` → `VertexAIProvider` | ❌ No (remote API) | ❌ No | ❌ No (needs `GEMINI_API_KEY`) |
| **OpenAI** | `gpt-*`, `openai:*` → `OpenAIProvider` | ❌ No (remote API) | ❌ No | ❌ No (needs `OPENAI_API_KEY`) |
| **Anthropic** | `claude-*`, `anthropic:*` → `AnthropicProvider` | ❌ No (remote API) | ❌ No | ❌ No (needs `ANTHROPIC_API_KEY`) |
| **GLiNER (encoder NER)** | `gliner:*`, `gliner_*`, `urchade/gliner*` → `GlinerProvider` | ✅ Yes (HF weights) | ✅ Yes | ❌ No (`pip install gliner`) |

> ⚠️ **Corrected 2026-09-03 (two fixes).** (1) The cloud pattern is **substring containment**, not
> "ends in / starts with": `is_cloud_model()` (`src/llm_runner.py:61-64`) does
> `key = model_name.lower(); return "-cloud" in key or "minimax" in key`. (2) The row previously
> claimed cloud models need `ollama pull`, contradicting §8.3 step 1 — they do **not**.
> The last four rows were missing entirely: without them `gemini-*` / `gpt-*` / `claude-*` /
> `gliner:*` fall into "Local" here, while `src/providers/factory.py:45-49` routes them elsewhere.

The routing logic lives in `src/llm_runner.py` and `src/providers/factory.py`:
- `is_cloud_model(name)` → detects cloud models
- `_NUEXTRACT_MODELS` set → detects NuExtract template format
- `_QWEN3_THINKING_MODELS` set → enables chain-of-thought

---

### 8.3 — ADD a model (3 steps)

**Step 1 — Pull the model locally** (skip for cloud models):
```bash
ollama pull <model_name>
# Example: ollama pull llama3.3:70b
# Cloud models are already available, no pull needed.
```

**Step 2 — Add to `src/config.py`**:
```python
# src/config.py  →  BenchmarkConfig.models  (dataclass field, ~line 59)
models: list[str] = field(default_factory=lambda: [
    'gemma4:31b-cloud',    # cloud models FIRST (run while local models load)
    'minimax-m3:cloud',
    'gemma4:31b',
    'llama3.3:70b',        # <-- ADD HERE, any position in the list
    ...
])
```

**Step 3 — If the model is a special type**, register it in `src/llm_runner.py`:

| Condition | Where to add |
|-----------|-------------|
| NuExtract variant | Add to `_NUEXTRACT_MODELS` set (line ~56) |
| Qwen3 thinking variant | Add to `_QWEN3_THINKING_MODELS` set (line ~57) |
| New cloud pattern (not `-cloud` suffix) | Update `is_cloud_model()` function body |
| Standard local model | **Nothing else needed** |

---

### 8.4 — REMOVE a model (1 step)

Delete the model name string from the list in `src/config.py`:
```python
# src/config.py  →  BenchmarkConfig.models  (dataclass field)
models: list[str] = field(default_factory=lambda: [
    'gemma4:31b-cloud',
    # 'minimax-m3:cloud',   # <-- commented out = disabled, not deleted from Ollama
    'gemma4:31b',
])
```

> **Tip**: Prefer commenting out (`#`) over deleting — preserves history for the thesis WORKLOG.

To also free disk space:
```bash
ollama rm <model_name>
```

---

### 8.5 — Verify after any change

```bash
# Quick smoke test — replace with your model name
cd repos/ner-llm-entity-benchmark && source venv/bin/activate
python3 -c "
from src.llm_runner import extract_entities_with_ollama, is_cloud_model
model = 'YOUR_MODEL_NAME'
print('Cloud?', is_cloud_model(model))
r = extract_entities_with_ollama(
    text='OFAC sanctioned Roman Abramovich and Millhouse LLC in Moscow.',
    model_name=model, max_tokens=128, max_retries=0
)
print('Entities:', r['entities'])
print('OK' if r['parse_method'] != 'failed' else 'FAILED')
"
```

Expected output: `Entities:` dict with `Persons`, `Organizations`, `Locations` all non-empty.

---

### 8.6 — Current model list (as of 2026-06-30; reviewed and completed 2026-09-03)

| Model | Type | Ollama Status | Benchmark Status | Note |
|-------|------|---------------|-----------------|------|
| `gemma4:31b-cloud` | Cloud (Ollama) | ✅ Pulled | ✅ Active | |
| `minimax-m3:cloud` | Cloud (Ollama) | ✅ Pulled | ✅ Active | |
| `gemini-3.1-flash-lite` | Cloud (AI Studio) | ☁️ API Cloud | ✅ Active | *Name corrected 2026-09-03: was written `gemini-1.5-flash-lite`, a model that exists in no config and no run. `src/config.py:60` declares `gemini-3.1-flash-lite`; it is the model of run #4 (F1 0.6547).* |
| `gemini-3.5-flash` | Cloud (AI Studio) | ☁️ API Cloud | ⚪ Declared, not run | *Added 2026-09-03: present in `src/config.py:60`, no catalogued run.* |
| `gemma4:31b` | Local | ✅ Pulled (19 GB) | ✅ Active | |
| `sonct988/gemma4-26b-a4b-it-q4km-256k:latest` | Local | ✅ Pulled (16 GB) | ✅ Active | |
| `gpt-oss:20b` | Local | ✅ Pulled (13 GB) | ✅ Active | |
| `gemma4:latest` | Local | ✅ Pulled (9.6 GB) | ✅ Active | |
| `gemma:latest` | Local | ✅ Pulled (5.0 GB) | ✅ Active | |
| `qwen3:8b` | Local + Thinking | ✅ Pulled (5.2 GB) | ✅ Active | |
| `qwen2.5:14b` | Local | ✅ Pulled (9.0 GB) | ✅ Active | |
| `mistral-nemo:latest` | Local | ✅ Pulled (7.1 GB) | ✅ Active | |
| `nuextract:latest` | Local + Template | ✅ Pulled (2.2 GB) | ✅ Active | |
| `llama3.1:8b` | Local | ✅ Pulled (4.9 GB) | ✅ Active | |
| `llama3.2:latest` | Local | ✅ Pulled (2.0 GB) | ✅ Active | |
| `phi3.5` | Local | ✅ Pulled (2.2 GB) | ✅ Active | |
| `nemotron-mini:4b` | Local | ✅ Pulled (2.7 GB) | ✅ Active | |
| `deepseek-r1:1.5b` | Local | ✅ Pulled (1.1 GB) | ✅ Active | |
| `gemma4:31b-mlx` | Local (MLX) | ✅ Pulled (18 GB) | ✅ Active | *Added 2026-09-03: best F1 of the N=120 run #13 (baseline 0.5925) and second model of the headline N=30 result (F1 0.7747).* |
| `gemma4:12b-mlx` | Local (MLX) | ✅ Pulled (7.7 GB) | ✅ Active | *Added 2026-09-03: in `src/config.py` and `run_benchmark.sh:25`. Canonical name. The previous label for this artefact carried a false `q8` suffix (the model is 4-bit NVFP4) and was retired project-wide; see `FINDINGS.md §F4`.* |
| `gliner:medium` | Local encoder (GlinerProvider) | ✅ Pulled (HF weights) | ✅ Active | *Added 2026-09-03: run #3 of `results/RUNS_INDEX.md`, F1 0.4767. Has its own provider (`src/providers/gliner_provider.py`).* |

### 8.7 — Run-flag traps (added 2026-09-03; verified against `src/main.py`)

Before quoting or reusing any run command, check it against the real argparse of `src/main.py`.
The parser accepts exactly: `--models`, `--batch-size`, `--data-file`, `--resume`, `--results-dir`,
`--generate-sample-data`, `--temperature`, `--max-tokens`, `--seed`, `--system-prompt-file`,
`--compare-annotators`, `--ablation`, `--rag-study`, `--rag-mode`, `--num-workers`. There is **no**
`--run-config` flag, and `results/<run_dir>/run_config.json` is an **output** artefact, never an input.

| Trap | What actually happens |
|------|----------------------|
| 🪤 **`--rag-mode` defaults to `entities`, not to `kb_combined`** | `--rag-study` alone runs the *legacy dictionary RAG* and emits `*_rag_enhanced` conditions. The thesis' reference run #13 used `--rag-mode kb_combined` and emits `*_kb_rag`. A run launched on 2026-09-03 without the flag had to be discarded (`results/DESCARTADA_ragmode_incorrecto_142604/`, catalogued as #14). |
| `--results-dir` is optional but load-bearing | Omitted → a fresh `results/<dataset>_<timestamp>/` per run. **`--resume` needs it** to locate the checkpoint. `--results-dir results` (the ROOT) **aborts** with `ResultsDirRootError`. |
| `--models` overrides `src/config.py` | Whatever `run_benchmark.sh` passes wins over `BenchmarkConfig.models` (see §8.1). |
| `--ablation` is the *Prompt Configuration Comparison* | Same experiment the thesis calls "Comparación de Configuraciones de Prompt" (a.k.a. prompt ablation study / 2x2 factorial design). The flag name stays as-is; it is a code identifier. |

---

## 9. Adaptive Worker Concurrency (AIMD)

> **File**: `src/adaptive_workers.py`  
> **Integrated in**: `src/main.py` (both standard sweep and ablation branches)

The benchmark uses **AIMD (Additive Increase / Multiplicative Decrease)** — the same algorithm underlying TCP congestion control — adapted for LLM rate-limit scenarios.

### How it works

| Event | Action |
|-------|--------|
| Rate-limit error (HTTP 429/503, "quota exceeded", etc.) | **Multiplicative Decrease**: `workers = max(min, ⌊workers/2⌋)` |
| 10 min without any error | **Additive Increase**: `workers += 1` every 2 min |
| AI increase ceiling | Hard cap at **75% of `max_workers`** (never reaches full max again) |
| 5 consecutive failures | **Circuit Breaker OPENS**: pins to 1 worker, 5-min cooldown |
| Recovery after cooldown | HALF_OPEN probe → if success: CLOSED, resume AI |

**Bounds**: `min=1`, `max=os.cpu_count()-2` (auto-detected, min 1).

### Circuit Breaker FSM

```
CLOSED ──(5 consecutive fails)──► OPEN ──(5 min cooldown)──► HALF_OPEN
  ▲                                                                │
  └────────────────(1 success)────────────────────────────────────┘
```

### Reading the logs

```
[AIMD] ⬇  MULTIPLICATIVE DECREASE | rate-limit event #3 | workers 4 → 2
[AIMD] ⚡ CIRCUIT BREAKER OPENED after 5 consecutive failures. Workers pinned to 1.
[AIMD] 🔄 CIRCUIT BREAKER → HALF_OPEN: probing recovery after 301s.
[AIMD] ✅ CIRCUIT BREAKER → CLOSED: system healthy again.
[AIMD] ⬆  ADDITIVE INCREASE | stable for 602s | workers 2 → 3 | ceiling=9 (75% of max=12)
```

### Tuning parameters (passed to `AdaptiveWorkerController`)

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `stable_window_sec` | 600 | Seconds clean before AI starts |
| `increase_interval_sec` | 120 | Seconds between each +1 step |
| `ai_ceiling_fraction` | 0.75 | Max % of `max_workers` reachable via AI |
| `circuit_failure_threshold` | 5 | Consecutive failures to open circuit |
| `circuit_recovery_sec` | 300 | Cooldown before HALF_OPEN probe |

---

## 10. LLM Provider Interface (Factory + Facade)

> **Package**: `src/providers/`  
> **Facade entry point**: `from src.providers import get_provider`

All LLM interaction goes through a **single unified interface** regardless of backend.

### Architecture

```
get_provider(model_name)          ← Facade (public API)
      │
      ▼
LLMProviderFactory.create()       ← Factory (routing logic)
      │
      ├── "gpt-*"      → OpenAIProvider
      ├── "claude-*"   → AnthropicProvider
      ├── "gemini-*"   → VertexAIProvider
      ├── "gliner:*"   → GlinerProvider    ← zero-shot encoder NER
      └── everything else → OllamaProvider   ← default
```

### Supported providers

| Provider | Model patterns | Needs env var | Install |
|----------|---------------|---------------|---------|
| **Ollama** | any (default) | none | `ollama` (already installed) |
| **OpenAI** | `gpt-*`, `openai:*` | `OPENAI_API_KEY` | `pip install openai` |
| **Anthropic** | `claude-*`, `anthropic:*` | `ANTHROPIC_API_KEY` | `pip install anthropic` |
| **Vertex AI / Gemini** | `gemini-*`, `vertexai:*` | `GEMINI_API_KEY` or `GOOGLE_API_KEY` | `pip install google-generativeai` |
| **GLiNER** | `gliner:*`, `gliner_*`, `urchade/gliner*` | none | `pip install gliner` (already installed) |

### Using the Facade

```python
from src.providers import get_provider

# Auto-routes to correct backend by model name
provider = get_provider("gemma4:31b-cloud")   # → OllamaProvider
provider = get_provider("gpt-4o")             # → OpenAIProvider (needs OPENAI_API_KEY)
provider = get_provider("claude-3-5-sonnet")  # → AnthropicProvider
provider = get_provider("gliner:medium")      # → GlinerProvider (no key, local inference)

result = provider.extract_entities(
    text="News article text here...",
    system_prompt="You are an NER expert...",
)
# result keys: entities, entities_raw, latency, tokens_per_sec, model, parse_method, retries, sys_metrics
```

### Adding a new provider

1. Create `src/providers/myprovider_provider.py` inheriting `LLMProvider` from `base.py`
2. Implement `extract_entities()` and `is_available()`
3. Add routing rule in `src/providers/factory.py` → `LLMProviderFactory.create()`
4. Export from `src/providers/__init__.py`
5. Document in `PROVIDERS.md`

### Backward compatibility

`src/llm_runner.extract_entities_with_ollama()` continues to work unchanged — it internally delegates to `OllamaProvider` via the Facade. No existing code breaks.

---

## 11. Agent Coordination — `CURRENT-TASKS.md`

Multiple agents (Claude Code, Claude Desktop, Antigravity, Gemini) work on this project, sometimes
concurrently. A living coordination document at the project root declares **who is doing what, on which
files**: [`../../CURRENT-TASKS.md`](../../CURRENT-TASKS.md).

### 11.1 Mandatory protocol — for every task

1. **READ** `CURRENT-TASKS.md` before starting. Check that no other agent declares work on the files you
   intend to touch.
2. **WRITE** your entry under your agent's section: task, status `EN CURSO`, affected files, start time.
3. Execute the task.
4. **UPDATE** your entry when done: `COMPLETADA` or `FALLIDA`, with the outcome.
5. **RE-READ** the document, in case another agent wrote while you were working.

### 11.2 Rules

- If a file is declared `EN CURSO` by another agent, **do not touch it**. Wait, or pick another.
- When **resuming** an interrupted task, update its entry too (status and reason for the interruption).
- Always **append** within your own section; never rewrite another agent's entries.
- **Every workflow** must own a subsection under §4 of `CURRENT-TASKS.md` (objective, phases, agents, files
  touched, outcome) and keep it current.
- **Every subagent** must be reflected under the parent task that spawned it.

### 11.3 Sections

| Section | Owner | Scope |
|---------|-------|-------|
| §1 Claude Code | Claude Code (CLI) | Pipeline, benchmarks, orchestration, statistical verification |
| §2 Claude Desktop | Claude Desktop | `.docx` editing and formatting (see `TODO-INFORME-FINAL.md §7`) |
| §3 Antigravity | Antigravity / Gemini | IDE-side development assistance |
| §4 Workflows | whoever launches them | One subsection per workflow |

> **Why this exists.** On 2026-09-03, `HISTORIAL-CONSOLIDADO.md` was modified by an agent outside the
> session working on it. `ListAgents` enumerates Claude Code sessions but **not** Claude Desktop, so the
> absence of a peer in that listing does not prove nobody else is editing.
