"""
src/providers/anthropic_provider.py
------------------------------------
Anthropic Claude provider implementation.

Supports models matched by "claude-*" prefix:
  - claude-3-5-sonnet-20241022 (claude-3-5-sonnet)
  - claude-3-5-haiku-20241022  (claude-3-5-haiku)
  - claude-3-opus-20240229     (claude-3-opus)
  - claude-3-sonnet-20240229   (claude-3-sonnet)
  - claude-3-haiku-20240307    (claude-3-haiku)

Requires:
  - pip install anthropic>=0.25
  - ANTHROPIC_API_KEY environment variable
"""
from __future__ import annotations

import logging
import os
import time
from typing import Any

from src.providers.base import (
    LLMProvider,
    ExtractionResult,
    ProviderNotConfiguredError,
)

logger = logging.getLogger("ner_benchmark.providers.anthropic")

_FALLBACK_SYSTEM_PROMPT = (
    "You are an expert compliance and anti-money laundering (AML) analyst. "
    "Perform Named Entity Recognition (NER) on news. Extract entities into: "
    "Persons, Organizations, Locations. Return ONLY valid JSON with keys: "
    '"Persons", "Organizations", "Locations".'
)

_SETUP_INSTRUCTIONS = """\
To use Anthropic Claude models:

1. Install the SDK:
   pip install anthropic>=0.25

2. Set your API key:
   export ANTHROPIC_API_KEY="sk-ant-..."

Supported model prefixes: claude-*
Example models: claude-3-5-sonnet-20241022, claude-3-opus-20240229
"""

# Anthropic max_tokens must be > 0; default for Claude models
_DEFAULT_MAX_TOKENS = 2048


class AnthropicProvider(LLMProvider):
    """
    Concrete provider for Anthropic Claude chat-completion models.

    Parameters
    ----------
    model_name : str
        Exact Anthropic model ID (e.g. "claude-3-5-sonnet-20241022").
    config : BenchmarkConfig | None
        Global run configuration.
    api_key : str | None
        Override for ANTHROPIC_API_KEY env var.
    """

    def __init__(
        self,
        model_name: str,
        config: Any = None,
        api_key: str | None = None,
    ) -> None:
        super().__init__(model_name, config)
        self._api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")

    # ------------------------------------------------------------------
    # is_available
    # ------------------------------------------------------------------

    def is_available(self) -> bool:
        """Returns True if `anthropic` is installed and API key is set."""
        try:
            import anthropic  # noqa: F401
        except ImportError:
            return False
        return bool(self._api_key)

    # ------------------------------------------------------------------
    # extract_entities
    # ------------------------------------------------------------------

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
        """Call Anthropic Messages API and parse NER entities."""
        try:
            import anthropic
        except ImportError as exc:
            raise ProviderNotConfiguredError("Anthropic", _SETUP_INSTRUCTIONS) from exc

        if not self._api_key:
            raise ProviderNotConfiguredError("Anthropic", _SETUP_INSTRUCTIONS)

        # Resolve parameters
        temperature = self._resolve(temperature, "temperature", 0.1)
        max_tokens = self._resolve(max_tokens, "max_tokens", _DEFAULT_MAX_TOKENS)
        max_retries = self._resolve(max_retries, "max_retries", 2)
        # Note: Anthropic API does not support `seed`; parameter accepted but ignored

        system_prompt = system_prompt or _FALLBACK_SYSTEM_PROMPT
        client = anthropic.Anthropic(api_key=self._api_key)

        last_error: str | None = None
        for attempt in range(max_retries + 1):
            start_time = time.time()
            try:
                response = client.messages.create(
                    model=self.model_name,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": f"News text:\n{text}"}
                    ],
                )
                latency = time.time() - start_time

                # Extract text from first content block
                raw_content = ""
                if response.content:
                    block = response.content[0]
                    raw_content = getattr(block, "text", "") or ""

                from src.llm_runner import parse_llm_response
                parsed_entities = parse_llm_response(raw_content)

                # Throughput estimate
                usage = response.usage
                out_tokens = getattr(usage, "output_tokens", 0)
                tokens_per_sec = out_tokens / latency if latency > 0 and out_tokens else 0.0

                method = "direct_json"
                stripped = raw_content.strip()
                if stripped.startswith("{") and stripped.endswith("}"):
                    method = "direct_json"
                elif "```" in raw_content:
                    method = "codeblock"
                else:
                    method = "fallback"

                return {
                    "entities": parsed_entities,
                    "entities_raw": raw_content,
                    "latency": latency,
                    "tokens_per_sec": round(tokens_per_sec, 2),
                    "model": self.model_name,
                    "parse_method": method,
                    "retries": attempt,
                    "sys_metrics": {},
                    "provider": "anthropic",
                }

            except ProviderNotConfiguredError:
                raise
            except Exception as exc:
                last_error = str(exc)
                logger.warning(
                    "Anthropic attempt %d/%d failed for '%s': %s",
                    attempt + 1, max_retries + 1, self.model_name, exc,
                )
                if attempt < max_retries:
                    time.sleep(2 ** attempt)

        return {
            "entities": {"Persons": [], "Organizations": [], "Locations": []},
            "entities_raw": f"ERROR: {last_error}",
            "latency": 0.0,
            "tokens_per_sec": 0.0,
            "model": self.model_name,
            "parse_method": "failed",
            "retries": max_retries,
            "sys_metrics": {},
            "provider": "anthropic",
        }
