"""
src/providers/__init__.py
--------------------------
Public Facade for the providers package.

Exposes a single function — `get_provider()` — that abstracts away the
Factory internals and serves as the canonical entry point for obtaining
an LLM provider anywhere in the codebase.

Quick usage
-----------
    from src.providers import get_provider

    provider = get_provider("gpt-4o")
    result   = provider.extract_entities(text, system_prompt)

    # With full config
    provider = get_provider("llama3.2:latest", config=benchmark_config)

Re-exports
----------
For code that needs the lower-level types:
    from src.providers import LLMProvider, ProviderNotConfiguredError
    from src.providers import LLMProviderFactory
"""
from __future__ import annotations

from typing import Any

from src.providers.base import (  # noqa: F401 — public re-exports
    LLMProvider,
    ExtractionResult,
    ProviderError,
    ProviderNotConfiguredError,
    ProviderInferenceError,
)
from src.providers.factory import LLMProviderFactory  # noqa: F401
from src.providers.gliner_provider import GlinerProvider  # noqa: F401

__all__ = [
    # Facade function
    "get_provider",
    # Re-exported types
    "LLMProvider",
    "ExtractionResult",
    "LLMProviderFactory",
    "ProviderError",
    "ProviderNotConfiguredError",
    "ProviderInferenceError",
    # Concrete providers (optional direct import)
    "GlinerProvider",
]


def get_provider(
    model_name: str,
    config: Any = None,
    **kwargs: Any,
) -> LLMProvider:
    """
    Facade: obtain the correct LLMProvider for *model_name*.

    Routing rules (applied in order, case-insensitive):
      • gpt-*      → OpenAIProvider
      • claude-*   → AnthropicProvider
      • gemini-*   → VertexAIProvider
      • gliner:*   → GlinerProvider  (zero-shot encoder NER)
      • <other>    → OllamaProvider

    Parameters
    ----------
    model_name : str
        Model identifier, e.g. "gpt-4o", "claude-3-5-sonnet-20241022",
        "gemini-1.5-pro", "llama3.2:latest".
    config : BenchmarkConfig | None
        Optional global configuration object.  When provided, the provider
        reads temperature, max_tokens, seed, max_retries, and
        ollama_base_url from it.
    **kwargs
        Provider-specific overrides forwarded to the constructor:
          - api_key       (OpenAI / Anthropic)
          - base_url      (OpenAI proxy / Azure)
          - ollama_base_url  (Ollama)

    Returns
    -------
    LLMProvider
        A configured, ready-to-use provider instance.

    Raises
    ------
    ProviderNotConfiguredError
        If extract_entities() is called on a provider whose dependencies
        or credentials are missing.  Check provider.is_available() first.

    Examples
    --------
    >>> provider = get_provider("gpt-4o")
    >>> if provider.is_available():
    ...     result = provider.extract_entities("John met Apple in NYC.")
    """
    return LLMProviderFactory.create(model_name, config, **kwargs)
