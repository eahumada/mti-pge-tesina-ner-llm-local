# Ollama
Ollama is a local LLM serving engine that allows running models like Llama, Gemma, and DeepSeek on local hardware.

**Relevance:** The core inference engine for the benchmark. The system interacts with Ollama via its API.
**Relationship to Requirements:** Ensures zero-data-leakage (NFR) by keeping all processing on-premises.