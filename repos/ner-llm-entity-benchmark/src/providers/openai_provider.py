"""
src/providers/openai_provider.py
---------------------------------
OpenAI provider implementation.

Supports models matched by "gpt-*" prefix:
  - gpt-4o, gpt-4o-mini
  - gpt-4, gpt-4-turbo
  - gpt-3.5-turbo

Requires:
  - pip install openai>=1.0
  - OPENAI_API_KEY environment variable

Optional per-call override via OPENAI_BASE_URL for proxies / Azure-compatible
endpoints.
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
    ProviderInferenceError,
)

logger = logging.getLogger("ner_benchmark.providers.openai")

_FALLBACK_SYSTEM_PROMPT = (
    "You are an expert compliance and anti-money laundering (AML) analyst. "
    "Perform Named Entity Recognition (NER) on news. Extract entities into: "
    "Persons, Organizations, Locations. Return ONLY valid JSON with keys: "
    '"Persons", "Organizations", "Locations".'
)

_SETUP_INSTRUCTIONS = """\
To use OpenAI models:

1. Install the SDK:
   pip install openai>=1.0

2. Set your API key:
   export OPENAI_API_KEY="sk-..."

3. (Optional) override the base URL for Azure / proxy:
   export OPENAI_BASE_URL="https://your-endpoint.openai.azure.com/"

Supported model prefixes: gpt-*
"""


class OpenAIProvider(LLMProvider):
    """
    Concrete provider for OpenAI chat-completion models.

    Parameters
    ----------
    model_name : str
        Exact OpenAI model identifier (e.g. "gpt-4o", "gpt-3.5-turbo").
    config : BenchmarkConfig | None
        Global run configuration (temperature, max_tokens, seed, max_retries).
    api_key : str | None
        Override for OPENAI_API_KEY env var.
    base_url : str | None
        Override for OPENAI_BASE_URL env var (Azure / proxy support).
    """

    def __init__(
        self,
        model_name: str,
        config: Any = None,
        api_key: str | None = None,
        base_url: str | None = None,
    ) -> None:
        super().__init__(model_name, config)
        self._api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self._base_url = base_url or os.environ.get("OPENAI_BASE_URL", None)

    # ------------------------------------------------------------------
    # is_available
    # ------------------------------------------------------------------

    def is_available(self) -> bool:
        """
        Returns True if:
          1. `openai` package is installed.
          2. OPENAI_API_KEY is non-empty.
        """
        try:
            import openai  # noqa: F401
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
        """Call OpenAI chat completion and parse NER entities."""
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ProviderNotConfiguredError("OpenAI", _SETUP_INSTRUCTIONS) from exc

        if not self._api_key:
            raise ProviderNotConfiguredError("OpenAI", _SETUP_INSTRUCTIONS)

        # Resolve parameters
        temperature = self._resolve(temperature, "temperature", 0.1)
        max_tokens = self._resolve(max_tokens, "max_tokens", 2048)
        seed = self._resolve(seed, "seed", 42)
        max_retries = self._resolve(max_retries, "max_retries", 2)

        system_prompt = system_prompt or _FALLBACK_SYSTEM_PROMPT

        client_kwargs: dict[str, Any] = {"api_key": self._api_key}
        if self._base_url:
            client_kwargs["base_url"] = self._base_url
        client = OpenAI(**client_kwargs)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"News text:\n{text}"},
        ]

        last_error: str | None = None
        for attempt in range(max_retries + 1):
            start_time = time.time()
            try:
                response = client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    seed=seed,
                )
                latency = time.time() - start_time
                raw_content = response.choices[0].message.content or ""

                from src.llm_runner import parse_llm_response
                parsed_entities = parse_llm_response(raw_content)

                usage = response.usage
                if usage and usage.completion_tokens and latency > 0:
                    tokens_per_sec = usage.completion_tokens / latency
                else:
                    tokens_per_sec = len(raw_content.split()) * 1.3 / latency if latency > 0 else 0.0

                method = "direct_json"
                if raw_content.strip().startswith("{") and raw_content.strip().endswith("}"):
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
                    "provider": "openai",
                }

            except ProviderNotConfiguredError:
                raise
            except Exception as exc:
                last_error = str(exc)
                logger.warning(
                    "OpenAI attempt %d/%d failed for '%s': %s",
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
            "provider": "openai",
        }
