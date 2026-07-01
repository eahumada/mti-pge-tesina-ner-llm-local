"""
src/providers/base.py
---------------------
Abstract base class (ABC) for all LLM provider implementations.

Defines the interface contract that every provider must fulfill:
  - extract_entities(): performs NER on raw text
  - is_available(): checks if the provider is properly configured and reachable

All providers return a standardized result dict matching the shape expected
by main.py / evaluator.py, ensuring drop-in compatibility.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


# ---------------------------------------------------------------------------
# Custom exception hierarchy
# ---------------------------------------------------------------------------

class ProviderError(Exception):
    """Base class for all provider-related errors."""


class ProviderNotConfiguredError(ProviderError):
    """
    Raised when a provider's required dependencies or credentials are missing.

    The `setup_instructions` attribute contains a human-readable guide so the
    developer can quickly fix the configuration.
    """

    def __init__(self, provider_name: str, setup_instructions: str) -> None:
        self.provider_name = provider_name
        self.setup_instructions = setup_instructions
        super().__init__(
            f"Provider '{provider_name}' is not available.\n\n"
            f"Setup instructions:\n{setup_instructions}"
        )


class ProviderInferenceError(ProviderError):
    """Raised when a provider call fails after exhausting all retries."""


# ---------------------------------------------------------------------------
# Standardised result type alias (documentation only)
# ---------------------------------------------------------------------------

#: Every provider's extract_entities() must return a dict with at least:
#:   entities         dict  – {"Persons": [...], "Organizations": [...], "Locations": [...]}
#:   entities_raw     str   – raw LLM response text
#:   latency          float – wall-clock inference time in seconds
#:   tokens_per_sec   float – generation throughput estimate
#:   model            str   – canonical model name used
#:   parse_method     str   – how the JSON was extracted ("direct_json", "codeblock", "fallback", "failed")
#:   retries          int   – number of retry attempts consumed
#:   sys_metrics      dict  – optional hardware telemetry (may be empty {})
ExtractionResult = dict[str, Any]


# ---------------------------------------------------------------------------
# Abstract base class
# ---------------------------------------------------------------------------

class LLMProvider(ABC):
    """
    Abstract provider that all concrete LLM integrations must implement.

    Parameters
    ----------
    model_name : str
        The exact model identifier to use (e.g. "llama3.2:latest", "gpt-4o").
    config : object | None
        A BenchmarkConfig (or compatible) object carrying global run settings
        such as temperature, max_tokens, seed, max_retries.
    """

    def __init__(self, model_name: str, config: Any = None) -> None:
        self.model_name = model_name
        self.config = config

    # ------------------------------------------------------------------
    # Abstract interface
    # ------------------------------------------------------------------

    @abstractmethod
    def extract_entities(
        self,
        text: str,
        system_prompt: str = "",
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        seed: int | None = None,
        max_retries: int | None = None,
    ) -> ExtractionResult:
        """
        Run NER inference on *text* and return a standardised result dict.

        Parameters
        ----------
        text : str
            The news article or raw text to annotate.
        system_prompt : str
            The system-role message to prepend (empty string falls back to
            provider's built-in default).
        temperature : float | None
            Override config temperature for this call.
        max_tokens : int | None
            Override config max_tokens for this call.
        seed : int | None
            Override config seed for this call.
        max_retries : int | None
            Override config max_retries for this call.

        Returns
        -------
        ExtractionResult
            A dict conforming to the ExtractionResult specification above.
        """
        raise NotImplementedError

    @abstractmethod
    def is_available(self) -> bool:
        """
        Return True if this provider can currently be used.

        Checks may include:
          - Required Python package installed
          - API key present in environment
          - Ollama server reachable
          - Model pulled locally
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Helpers shared by subclasses
    # ------------------------------------------------------------------

    def _resolve(self, override: Any, attr: str, default: Any) -> Any:
        """Return *override* if not None, else config.<attr>, else *default*."""
        if override is not None:
            return override
        if self.config is not None:
            return getattr(self.config, attr, default)
        return default

    def __repr__(self) -> str:  # pragma: no cover
        return f"{self.__class__.__name__}(model={self.model_name!r})"
