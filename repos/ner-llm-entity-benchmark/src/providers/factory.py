"""
src/providers/factory.py
--------------------------
LLMProviderFactory — Factory Pattern implementation.

Routing rules (matched in order, case-insensitive):
  gpt-*         → OpenAIProvider
  claude-*      → AnthropicProvider
  gemini-*      → VertexAIProvider
  gliner:*      → GlinerProvider
  gliner_*      → GlinerProvider  (HuggingFace path fragment)
  urchade/gliner* → GlinerProvider  (full HuggingFace repo ID)
  <anything>    → OllamaProvider  (default, covers all local / cloud-Ollama models)

Usage
-----
    from src.providers.factory import LLMProviderFactory

    provider = LLMProviderFactory.create("gpt-4o", config)
    result = provider.extract_entities(text, system_prompt)
"""
from __future__ import annotations

import logging
from typing import Any

from src.providers.base import LLMProvider

logger = logging.getLogger("ner_benchmark.providers.factory")

# Registry of (prefix_match_fn, provider_class_import_path) pairs.
# Evaluated in order; first match wins.
# Imports are deferred so missing optional SDKs don't break the import chain.
def _is_gliner_model(name: str) -> bool:
    """Return True for any GLiNER model identifier (case-insensitive)."""
    return (
        name.startswith("gliner:")
        or name.startswith("gliner_")
        or name == "gliner"
        or "urchade/gliner" in name
    )


_ROUTING_TABLE: list[tuple[Any, str]] = [
    # (predicate, dotted import path to class)
    (lambda name: name.startswith("gpt-"),     "src.providers.openai_provider.OpenAIProvider"),
    (lambda name: name.startswith("claude-"),  "src.providers.anthropic_provider.AnthropicProvider"),
    (lambda name: name.startswith("gemini-"),  "src.providers.vertexai_provider.VertexAIProvider"),
    (_is_gliner_model,                         "src.providers.gliner_provider.GlinerProvider"),
]

# Fallback (Ollama) — handles all unmatched names
_OLLAMA_CLASS_PATH = "src.providers.ollama_provider.OllamaProvider"


def _import_class(dotted_path: str) -> type:
    """Dynamically import and return a class by its dotted module path."""
    module_path, _, class_name = dotted_path.rpartition(".")
    import importlib
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


class LLMProviderFactory:
    """
    Factory that creates the correct LLMProvider subclass for a given model name.

    Methods
    -------
    create(model_name, config=None, **kwargs) -> LLMProvider
        Return an instantiated provider ready to call extract_entities().
    detect_provider_name(model_name) -> str
        Return the provider label ('openai', 'anthropic', 'vertexai', 'ollama')
        without constructing a provider instance.
    """

    @staticmethod
    def create(
        model_name: str,
        config: Any = None,
        **kwargs: Any,
    ) -> LLMProvider:
        """
        Instantiate and return the appropriate LLMProvider for *model_name*.

        Parameters
        ----------
        model_name : str
            The model identifier (e.g. "gpt-4o", "claude-3-5-sonnet-20241022",
            "gemini-1.5-pro", "llama3.2:latest").
        config : BenchmarkConfig | None
            Passed through to the provider constructor.
        **kwargs
            Extra keyword arguments forwarded to the provider constructor
            (e.g. api_key, base_url, ollama_base_url).

        Returns
        -------
        LLMProvider
            Concrete provider instance.
        """
        name_lower = model_name.lower()

        for predicate, class_path in _ROUTING_TABLE:
            if predicate(name_lower):
                cls = _import_class(class_path)
                logger.debug(
                    "Factory: routing model '%s' → %s", model_name, cls.__name__
                )
                import inspect
                sig = inspect.signature(cls.__init__)
                valid_params = sig.parameters.keys()
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_params}
                return cls(model_name, config, **filtered_kwargs)

        # Default: Ollama
        cls = _import_class(_OLLAMA_CLASS_PATH)
        logger.debug(
            "Factory: model '%s' → OllamaProvider (default)", model_name
        )
        import inspect
        sig = inspect.signature(cls.__init__)
        valid_params = sig.parameters.keys()
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_params}
        return cls(model_name, config, **filtered_kwargs)

    @staticmethod
    def detect_provider_name(model_name: str) -> str:
        """
        Return a provider label string without constructing an instance.

        Useful for logging, metrics tagging, or conditional logic.

        Returns one of: 'openai', 'anthropic', 'vertexai', 'gliner', 'ollama'
        """
        name_lower = model_name.lower()
        labels = {
            "src.providers.openai_provider.OpenAIProvider": "openai",
            "src.providers.anthropic_provider.AnthropicProvider": "anthropic",
            "src.providers.vertexai_provider.VertexAIProvider": "vertexai",
            "src.providers.gliner_provider.GlinerProvider": "gliner",
        }
        for predicate, class_path in _ROUTING_TABLE:
            if predicate(name_lower):
                return labels.get(class_path, "unknown")
        return "ollama"
