"""
src/providers/ollama_provider.py
--------------------------------
Ollama provider implementation.

All NER logic previously living in llm_runner.extract_entities_with_ollama()
has been migrated here while keeping the original function as a shim for
backward compatibility.

Supports:
  - Standard local Ollama models
  - Cloud-hosted Ollama models (e.g. gemma4:31b-cloud, minimax-m3:cloud)
  - NuExtract template format
  - Qwen3 chain-of-thought thinking mode
"""
from __future__ import annotations

import logging
import time
from typing import Any

import requests

from src.providers.base import (
    LLMProvider,
    ExtractionResult,
    ProviderNotConfiguredError,
    ProviderInferenceError,
)

logger = logging.getLogger("ner_benchmark.providers.ollama")

# ---------------------------------------------------------------------------
# Model routing constants (mirrors llm_runner constants)
# ---------------------------------------------------------------------------

_NUEXTRACT_MODELS: set[str] = {
    "nuextract", "nuextract:latest", "nuextract:3.8b", "nuextract:8b"
}
_QWEN3_THINKING_MODELS: set[str] = {
    "qwen3:8b", "qwen3:14b", "qwen3:32b", "qwen3:latest"
}

_FALLBACK_SYSTEM_PROMPT = (
    "You are an expert compliance and anti-money laundering (AML) analyst. "
    "Perform Named Entity Recognition (NER) on news. Extract entities into: "
    "Persons, Organizations, Locations. Return ONLY valid JSON with keys: "
    '"Persons", "Organizations", "Locations".'
)


# ---------------------------------------------------------------------------
# Helper functions (formerly module-level in llm_runner.py)
# ---------------------------------------------------------------------------

def _is_cloud_model(model_name: str) -> bool:
    key = model_name.lower()
    return "-cloud" in key or "minimax" in key


def _build_messages(system_prompt: str, news_text: str) -> list[dict]:
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"News text:\n{news_text}"},
    ]


def _build_nuextract_messages(news_text: str) -> list[dict]:
    import json
    template = json.dumps(
        {"Persons": [], "Organizations": [], "Locations": []}, indent=2
    )
    content = (
        f"### Template:\n{template}\n\n"
        f"### Text:\n{news_text}\n\n"
        f"### Expected Output:"
    )
    return [{"role": "user", "content": content}]


# ---------------------------------------------------------------------------
# OllamaProvider
# ---------------------------------------------------------------------------

class OllamaProvider(LLMProvider):
    """
    Concrete provider for local and cloud-hosted Ollama models.

    Parameters
    ----------
    model_name : str
        Ollama model tag, e.g. "llama3.2:latest", "gemma4:31b-cloud".
    config : BenchmarkConfig | None
        Global run configuration.
    ollama_base_url : str
        Base URL for the Ollama REST API (overrides config.ollama_base_url).
    """

    def __init__(
        self,
        model_name: str,
        config: Any = None,
        ollama_base_url: str | None = None,
    ) -> None:
        super().__init__(model_name, config)
        # URL precedence: explicit kwarg > config attr > default
        self.ollama_base_url = (
            ollama_base_url
            or (getattr(config, "ollama_base_url", None) if config else None)
            or "http://localhost:11434"
        )

    # ------------------------------------------------------------------
    # is_available
    # ------------------------------------------------------------------

    def is_available(self) -> bool:
        """
        Returns True if:
          1. The `ollama` Python package is installed.
          2. The Ollama HTTP endpoint responds.
          3. The model is pulled locally (or is a cloud-hosted model).
        """
        try:
            import ollama  # noqa: F401
        except ImportError:
            return False

        try:
            resp = requests.get(f"{self.ollama_base_url}/api/tags", timeout=5)
            if resp.status_code != 200:
                return False
        except Exception:
            return False

        if _is_cloud_model(self.model_name):
            return True  # cloud models are not in local repo

        models = [m.get("name") for m in resp.json().get("models", [])]
        return any(
            m == self.model_name or m.split(":")[0] == self.model_name
            for m in models
        )

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
        rag_context: list[str] | None = None,
    ) -> ExtractionResult:
        """Run NER with the configured Ollama model."""
        # Lazy import so the package stays importable even without `ollama`
        try:
            import ollama as ollama_lib
        except ImportError as exc:
            raise ProviderNotConfiguredError(
                "Ollama",
                (
                    "Install the Ollama Python client:\n"
                    "  pip install ollama>=0.4\n\n"
                    "Then start the Ollama daemon:\n"
                    "  ollama serve"
                ),
            ) from exc

        # Resolve parameters
        temperature = self._resolve(temperature, "temperature", 0.1)
        max_tokens = self._resolve(max_tokens, "max_tokens", 2048)
        seed = self._resolve(seed, "seed", 42)
        max_retries = self._resolve(max_retries, "max_retries", 2)

        model_key = self.model_name.lower()
        is_nuextract = any(k in model_key for k in _NUEXTRACT_MODELS)
        is_qwen3_thinking = any(k in model_key for k in _QWEN3_THINKING_MODELS)
        is_cloud = _is_cloud_model(self.model_name)

        # Inject RAG context if provided.
        #
        # Two injection strategies depending on context type:
        #   1. Entity-dict RAG (legacy): uses a restrictive warning template.
        #      These are entity name strings like "GRANJA LA SIERRA LTDA. (Organization)".
        #      The warning prevents the LLM from hallucinating listed entities that are
        #      absent from the article text.
        #
        #   2. Knowledge-Base RAG (new): uses a positive instructive template.
        #      These are domain guidelines and few-shot examples from KBRAGManager.
        #      They begin with known KB prefixes:
        #        - "[DOMAIN CONTEXT:" — domain NER disambiguation rules
        #        - "[EXTRACTION EXAMPLE" — annotated few-shot example
        #      A positive template is required: the restrictive warning would cause
        #      the LLM to suppress legitimate extraction (root cause of the semantic
        #      mismatch problem documented in
        #      research/rag/2026-08-31_analisis_contenido_rag_base_conocimientos.md).
        rag_injection = ""
        if rag_context:
            _KB_PREFIXES = ("[DOMAIN CONTEXT:", "[EXTRACTION EXAMPLE")
            _is_kb_context = any(
                isinstance(ctx, str) and ctx.strip().startswith(_KB_PREFIXES)
                for ctx in rag_context
            )
            if _is_kb_context:
                # ── Knowledge-Base RAG: positive, instructive injection ──────────
                rag_injection = (
                    "\n\n[EXTRACTION GUIDANCE]\n"
                    "The following domain-specific guidelines and/or example will help "
                    "you extract entities accurately. Apply these rules to the news text:\n\n"
                )
                rag_injection += "\n\n".join(str(ctx) for ctx in rag_context)
            else:
                # ── Legacy entity-dict RAG: restrictive injection (original) ────
                rag_injection = (
                    "\n\n[RAG CONTEXT]\n"
                    "The following entities from our AML database MIGHT be present in the "
                    "text. STRICT INSTRUCTION: DO NOT extract them unless they explicitly "
                    "appear in the News text. They are provided only as hints for correct "
                    "spelling and recognition:\n"
                )
                rag_injection += "\n".join(f"- {ctx}" for ctx in rag_context)

        # Build prompt
        if is_nuextract:
            if rag_injection:
                text = f"{rag_injection}\n\n{text}"
            messages = _build_nuextract_messages(text)
            logger.debug("Using NuExtract template format for '%s'.", self.model_name)
        else:
            if not system_prompt:
                system_prompt = _FALLBACK_SYSTEM_PROMPT
            if rag_injection:
                system_prompt += rag_injection
            messages = _build_messages(system_prompt, text)

        client = ollama_lib.Client(host=self.ollama_base_url)
        options: dict[str, Any] = {
            "temperature": temperature,
            "num_predict": max_tokens,
            "seed": seed,
        }
        if is_qwen3_thinking and not is_cloud:
            options["think"] = True
            logger.debug("Qwen3 thinking mode enabled for '%s'.", self.model_name)
        if is_cloud:
            logger.debug("Cloud-hosted Ollama model '%s': using cloud endpoint.", self.model_name)

        # SystemMonitor import is optional (graceful degradation)
        try:
            from src.system_monitor import SystemMonitor
            _has_monitor = True
        except ImportError:
            _has_monitor = False

        last_error: str | None = None
        for attempt in range(max_retries + 1):
            start_time = time.time()
            try:
                if _has_monitor:
                    with SystemMonitor(
                        model_name=self.model_name,
                        sample_interval=0.5,
                        ollama_base_url=self.ollama_base_url,
                    ) as monitor:
                        response = client.chat(
                            model=self.model_name,
                            messages=messages,
                            options=options,
                        )
                    sys_metrics = monitor.metrics.to_dict()
                else:
                    response = client.chat(
                        model=self.model_name,
                        messages=messages,
                        options=options,
                    )
                    sys_metrics = {}

                latency = time.time() - start_time
                raw_content = (
                    response.message.content
                    if hasattr(response, "message")
                    else ""
                )

                # Import parse utilities from llm_runner (single source of truth)
                from src.llm_runner import parse_llm_response
                parsed_entities = parse_llm_response(raw_content)

                # Determine parse method label
                if raw_content.strip().startswith("{") and raw_content.strip().endswith("}"):
                    method = "direct_json"
                elif "```" in raw_content:
                    method = "codeblock"
                else:
                    method = "fallback"

                # Token throughput
                eval_count = getattr(response, "eval_count", None)
                eval_duration = getattr(response, "eval_duration", None)
                if eval_count and eval_duration:
                    tokens_per_sec = eval_count / (eval_duration / 1e9)
                else:
                    tokens_count = len(raw_content.split()) * 1.3
                    tokens_per_sec = tokens_count / latency if latency > 0 else 0.0

                return {
                    "entities": parsed_entities,
                    "entities_raw": raw_content,
                    "latency": latency,
                    "tokens_per_sec": round(tokens_per_sec, 2),
                    "model": self.model_name,
                    "parse_method": method,
                    "retries": attempt,
                    "sys_metrics": sys_metrics,
                    "provider": "ollama",
                }

            except ProviderNotConfiguredError:
                raise
            except Exception as exc:
                last_error = str(exc)
                # Soft fallback for gemma4:31b-mlx if not found locally in Ollama
                if "gemma4:31b-mlx" in self.model_name.lower() and ("not found" in last_error.lower() or "404" in last_error):
                    logger.warning("Model 'gemma4:31b-mlx' not found in Ollama. Activating soft fallback to 'gemma4:31b'...")
                    fallback_model = "gemma4:31b"
                    try:
                        start_time = time.time()
                        if _has_monitor:
                            with SystemMonitor(
                                model_name=fallback_model,
                                sample_interval=0.5,
                                ollama_base_url=self.ollama_base_url,
                            ) as monitor:
                                response = client.chat(
                                    model=fallback_model,
                                    messages=messages,
                                    options=options,
                                )
                            sys_metrics = monitor.metrics.to_dict()
                        else:
                            response = client.chat(
                                model=fallback_model,
                                messages=messages,
                                options=options,
                            )
                            sys_metrics = {}

                        latency = time.time() - start_time
                        raw_content = response.message.content if hasattr(response, "message") else ""
                        from src.llm_runner import parse_llm_response
                        parsed_entities = parse_llm_response(raw_content)
                        method = "direct_json" if raw_content.strip().startswith("{") and raw_content.strip().endswith("}") else "fallback"
                        eval_count = getattr(response, "eval_count", None)
                        eval_duration = getattr(response, "eval_duration", None)
                        tokens_per_sec = eval_count / (eval_duration / 1e9) if eval_count and eval_duration else 0.0

                        return {
                            "entities": parsed_entities,
                            "entities_raw": raw_content,
                            "latency": latency,
                            "tokens_per_sec": round(tokens_per_sec, 2),
                            "model": self.model_name,
                            "parse_method": method,
                            "retries": attempt,
                            "sys_metrics": sys_metrics,
                            "provider": "ollama",
                        }
                    except Exception as fallback_exc:
                        last_error = f"Fallback failed: {fallback_exc}"

                logger.warning(
                    "Attempt %d/%d failed for model '%s': %s",
                    attempt + 1, max_retries + 1, self.model_name, last_error,
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
            "provider": "ollama",
        }
