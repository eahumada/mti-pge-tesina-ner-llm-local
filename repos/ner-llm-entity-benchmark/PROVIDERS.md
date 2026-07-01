# Provider Configuration Guide

This document explains how to configure each LLM provider supported by the
NER-LLM Entity Benchmark.  The system uses a **Factory + Facade** pattern:
call `get_provider(model_name)` and the correct driver is selected automatically.

---

## Quick Start

```python
from src.providers import get_provider

provider = get_provider("gpt-4o")          # → OpenAIProvider
provider = get_provider("claude-3-5-sonnet-20241022")  # → AnthropicProvider
provider = get_provider("gemini-1.5-pro")  # → VertexAIProvider
provider = get_provider("gliner:medium")   # → GlinerProvider
provider = get_provider("llama3.2:latest") # → OllamaProvider (default)

if provider.is_available():
    result = provider.extract_entities(text, system_prompt)
```

---

## Provider Routing Rules

| Model name prefix | Provider selected  | Class                  |
|-------------------|--------------------|------------------------|
| `gpt-*`           | OpenAI             | `OpenAIProvider`       |
| `claude-*`        | Anthropic          | `AnthropicProvider`    |
| `gemini-*`        | Vertex AI / Gemini | `VertexAIProvider`     |
| `gliner:*`, `gliner_*`, `urchade/gliner*` | GLiNER | `GlinerProvider` |
| *(anything else)* | Ollama             | `OllamaProvider`       |

---

## 1. Ollama (local / cloud-hosted)

**Default provider** — no API key required for local models.

### Install

```bash
# Install Ollama daemon (macOS/Linux)
curl -fsSL https://ollama.com/install.sh | sh

# Install Python client
pip install ollama>=0.4
```

### Configuration

```bash
# Optional — override default URL
export OLLAMA_BASE_URL="http://localhost:11434"
```

Or pass via `BenchmarkConfig`:
```python
config = BenchmarkConfig(ollama_base_url="http://my-ollama-server:11434")
```

### Pull a model

```bash
ollama pull llama3.2:latest
ollama pull gemma3:latest
ollama pull qwen3:8b
```

### Cloud-hosted Ollama models

Models with `-cloud` suffix or `minimax` in the name are served remotely and
skip the local availability check:

```
gemma4:31b-cloud
minimax-m3:cloud
```

### Special model behaviours

| Model family    | Behaviour                                                 |
|-----------------|-----------------------------------------------------------|
| `nuextract*`    | Uses template/text extractive format (no system prompt)   |
| `qwen3:*`       | Enables chain-of-thought `think` mode for better NER      |
| `*-cloud`       | Bypasses local VRAM / availability check                  |

---

## 2. OpenAI

### Install

```bash
pip install openai>=1.0
```

### Configuration

```bash
export OPENAI_API_KEY="sk-..."
```

Optional — for Azure OpenAI or compatible proxies:
```bash
export OPENAI_BASE_URL="https://your-resource.openai.azure.com/"
```

### Supported models

```
gpt-4o              # recommended — best accuracy
gpt-4o-mini         # faster, cheaper
gpt-4
gpt-4-turbo
gpt-3.5-turbo
```

### Verify configuration

```python
from src.providers import get_provider
p = get_provider("gpt-4o")
print(p.is_available())  # True if key is set
```

---

## 3. Anthropic

### Install

```bash
pip install anthropic>=0.25
```

### Configuration

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Supported models

```
claude-3-5-sonnet-20241022  # recommended — best accuracy
claude-3-5-haiku-20241022   # faster, cheaper
claude-3-opus-20240229      # most capable (legacy)
claude-3-sonnet-20240229
claude-3-haiku-20240307
```

### Verify configuration

```python
from src.providers import get_provider
p = get_provider("claude-3-5-sonnet-20241022")
print(p.is_available())  # True if key is set
```

---

## 4. Vertex AI / Gemini

Two authentication methods are supported (auto-detected in order):

### Option A — Vertex AI SDK (recommended for GCP)

```bash
pip install google-cloud-aiplatform>=1.60
```

```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"   # optional, defaults to us-central1

# Authenticate with Application Default Credentials (ADC)
gcloud auth application-default login
```

### Option B — Gemini AI Studio (quick local testing)

```bash
pip install google-generativeai>=0.5
```

```bash
# Supports either GEMINI_API_KEY or GOOGLE_API_KEY
export GEMINI_API_KEY="AIza..."
```

### Supported models

```
gemini-2.0-flash-lite   # recommended — fast, lightweight extraction
gemini-1.5-flash        # fast, efficient
gemini-1.5-pro          # recommended for complex reasoning — long context
gemini-2.0-flash        # standard 2.0 version
```

### Verify configuration

```python
from src.providers import get_provider
p = get_provider("gemini-2.0-flash-lite")
print(p.is_available())  # True if either ADC or GEMINI_API_KEY/GOOGLE_API_KEY is set
```

---

## 5. GLiNER (zero-shot encoder NER)

GLiNER is a **Generalist and Lightweight model for Named Entity Recognition**
based on bidirectional encoders (BERT-like architecture).  Unlike LLMs, it
doesn't generate text — it directly predicts entity spans given a list of
labels.  This makes it deterministic, fast, and free of JSON-hallucination
problems.

- Paper: [arXiv:2311.08526](https://arxiv.org/abs/2311.08526)
- Repo: <https://github.com/urchade/GLiNER>

### Install

```bash
pip install gliner
```

> The `gliner` package is already present in the project venv; no extra setup
> is needed.

### Supported model aliases

| Alias | HuggingFace repo | Size |
|-------|-----------------|------|
| `gliner:small` | `urchade/gliner_small-v2.1` | ~70 MB |
| `gliner:medium` *(default)* | `urchade/gliner_medium-v2.1` | ~170 MB |
| `gliner:large` | `urchade/gliner_large-v2.1` | ~340 MB |
| `gliner:multitask` | `urchade/gliner-multitask-large-v0.5` | multilingual |

You can also pass a raw HuggingFace repo ID directly:
```python
provider = get_provider("urchade/gliner_small-v2.1")
```

### Usage

```python
from src.providers import get_provider

provider = get_provider("gliner:medium")
if provider.is_available():
    result = provider.extract_entities(
        "OFAC sanctioned Roman Abramovich and Millhouse LLC in Moscow."
    )
    print(result["entities"])
    # {"Persons": ["Roman Abramovich"], "Organizations": ["Millhouse LLC"], "Locations": ["Moscow"]}
```

### Configuration

No API key or daemon required.  Weights are automatically downloaded from
HuggingFace Hub on the **first call** and cached locally.

Optional threshold override via `BenchmarkConfig`:
```python
config = BenchmarkConfig()          # add gliner_threshold = 0.5 to your config
provider = get_provider("gliner:medium", config=config)
```

### Differences from LLM providers

| Aspect | LLM providers (Ollama, OpenAI…) | GLiNER |
|--------|--------------------------------|--------|
| Inference style | Generative (token-by-token) | Discriminative (span classification) |
| `system_prompt` used? | ✅ Yes | ❌ No (ignored) |
| `temperature` / `seed` | ✅ Yes | ❌ No (deterministic) |
| `tokens_per_sec` | ✅ Measured | `0.0` (not applicable) |
| `parse_method` value | `direct_json`, `codeblock`, `fallback` | `gliner_native` |
| JSON hallucination risk | Medium–High | None (direct span output) |

### Verify configuration

```python
from src.providers import get_provider
p = get_provider("gliner:medium")
print(p.is_available())  # True if gliner package is installed
```

---

## Error Handling

If a provider is not configured, calling `extract_entities()` raises
`ProviderNotConfiguredError` with detailed setup instructions:

```python
from src.providers import get_provider, ProviderNotConfiguredError

provider = get_provider("gpt-4o")
try:
    result = provider.extract_entities(text)
except ProviderNotConfiguredError as e:
    print(e.setup_instructions)
```

Always check `provider.is_available()` before calling `extract_entities()` in
non-interactive pipelines to gracefully skip unavailable providers.

---

## Adding a new Provider

1. Create `src/providers/<name>_provider.py` with a class extending `LLMProvider`.
2. Implement `is_available()` and `extract_entities()`.
3. Add a routing entry in `src/providers/factory.py`:
   ```python
   (lambda name: name.startswith("my-prefix-"), "src.providers.my_provider.MyProvider"),
   ```
4. Re-export the class in `src/providers/__init__.py` if needed.
5. Document it in this file.
