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
4. **Model Pulling:** Retrieves the default model `gemma4` (Gemma 2 9B) locally.

---

## 🏃 Running the Pipeline

### 1. Activate the Virtual Environment
Before executing any scripts, ensure the `venv` is active:
```bash
source venv/bin/activate
```

### 2. Run the Benchmark Sweep
Evaluate a model sweep on the primary Kleptotrace dataset:
```bash
python src/main.py --models gemma4 --data-file data/kleptotrace.json --batch-size 3
```

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
