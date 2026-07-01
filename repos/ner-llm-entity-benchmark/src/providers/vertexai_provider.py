"""
src/providers/vertexai_provider.py
------------------------------------
Google Vertex AI / Gemini provider implementation.

Supports models matched by "gemini-*" prefix:
  - gemini-1.5-pro, gemini-1.5-flash
  - gemini-pro (legacy alias)
  - gemini-2.0-flash-exp, etc.

Requires:
  - pip install google-cloud-aiplatform>=1.60 OR google-generativeai>=0.5
  - GOOGLE_CLOUD_PROJECT environment variable (for Vertex AI)
    OR GOOGLE_API_KEY (for Gemini AI Studio)
  - Application Default Credentials (ADC) configured:
      gcloud auth application-default login

Authentication modes (auto-detected):
  1. Vertex AI SDK (google-cloud-aiplatform) + ADC     [preferred for GCP]
  2. Google Generative AI SDK (google-generativeai) + API key  [AI Studio]
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

logger = logging.getLogger("ner_benchmark.providers.vertexai")

_FALLBACK_SYSTEM_PROMPT = (
    "You are an expert compliance and anti-money laundering (AML) analyst. "
    "Perform Named Entity Recognition (NER) on news. Extract entities into: "
    "Persons, Organizations, Locations. Return ONLY valid JSON with keys: "
    '"Persons", "Organizations", "Locations".'
)

_SETUP_INSTRUCTIONS = """\
To use Google Vertex AI / Gemini models:

Option A — Vertex AI (recommended for GCP projects):
  1. Install the SDK:
     pip install google-cloud-aiplatform>=1.60

  2. Set your GCP project:
     export GOOGLE_CLOUD_PROJECT="your-project-id"
     export GOOGLE_CLOUD_LOCATION="us-central1"   # optional, default us-central1

  3. Authenticate with ADC:
     gcloud auth application-default login

Option B — Gemini AI Studio (quick local testing):
  1. Install the SDK:
     pip install google-generativeai>=0.5

  2. Set your API key:
     export GOOGLE_API_KEY="AIza..."

Supported model prefixes: gemini-*
Example models: gemini-1.5-pro, gemini-1.5-flash, gemini-pro
"""


def _try_vertex_ai(model_name: str, messages: list[dict], temperature: float, max_tokens: int) -> str:
    """Attempt inference via google-cloud-aiplatform Vertex AI SDK."""
    import vertexai
    from vertexai.generative_models import GenerativeModel, GenerationConfig

    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    if not project:
        raise EnvironmentError("GOOGLE_CLOUD_PROJECT not set")

    vertexai.init(project=project, location=location)

    # Build contents list from messages
    contents = []
    system_instruction = None
    for msg in messages:
        if msg["role"] == "system":
            system_instruction = msg["content"]
        else:
            contents.append({"role": "user", "parts": [{"text": msg["content"]}]})

    model = GenerativeModel(
        model_name,
        system_instruction=system_instruction,
    )
    generation_config = GenerationConfig(
        temperature=temperature,
        max_output_tokens=max_tokens,
    )
    response = model.generate_content(contents, generation_config=generation_config)
    return response.text or ""


def _try_generativeai(model_name: str, messages: list[dict], temperature: float, max_tokens: int) -> str:
    """Attempt inference via google-generativeai (AI Studio) SDK, falling back to HTTP REST if needed."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("Neither GEMINI_API_KEY nor GOOGLE_API_KEY is set")

    system_prompt = ""
    user_text = ""
    for msg in messages:
        if msg["role"] == "system":
            system_prompt = msg["content"]
        else:
            user_text = msg["content"]

    # Try SDK first
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt or None,
        )
        response = model.generate_content(
            user_text,
            generation_config=genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            ),
        )
        if response.text:
            return response.text
    except Exception as sdk_err:
        logger.warning("GenerativeAI SDK failed: %s. Attempting direct HTTP REST fallback.", sdk_err)

    # Fallback: Direct HTTP REST call to Gemini API
    import requests
    # Ensure correct models prefix
    model_id = model_name
    if not model_id.startswith("models/"):
        model_id = f"models/{model_id}"
    
    url = f"https://generativelanguage.googleapis.com/v1/{model_id}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "contents": [{"parts": [{"text": user_text}]}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens
        }
    }
    if system_prompt:
        payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    if resp.status_code == 200:
        data = resp.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as parse_err:
            raise RuntimeError(f"Failed to parse Gemini REST response: {parse_err}. Response was: {data}")
    else:
        raise RuntimeError(f"Gemini API REST fallback failed with HTTP {resp.status_code}: {resp.text}")


class VertexAIProvider(LLMProvider):
    """
    Concrete provider for Google Vertex AI / Gemini generative models.

    Authentication is attempted in this order:
      1. google-cloud-aiplatform + Application Default Credentials (ADC)
      2. google-generativeai + GOOGLE_API_KEY

    Parameters
    ----------
    model_name : str
        Gemini model identifier (e.g. "gemini-1.5-pro", "gemini-pro").
    config : BenchmarkConfig | None
        Global run configuration.
    """

    def __init__(self, model_name: str, config: Any = None) -> None:
        super().__init__(model_name, config)

    # ------------------------------------------------------------------
    # is_available
    # ------------------------------------------------------------------

    def is_available(self) -> bool:
        """
        Returns True if either Vertex AI SDK or google-generativeai is
        installed and credentials are present.
        """
        # Check Vertex AI path
        try:
            import vertexai  # noqa: F401
            if os.environ.get("GOOGLE_CLOUD_PROJECT"):
                return True
        except ImportError:
            pass

        # Check Gemini AI Studio path
        try:
            import google.generativeai  # noqa: F401
            if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
                return True
        except ImportError:
            pass

        return False

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
        """Call Vertex AI / Gemini and parse NER entities."""
        if not self.is_available():
            raise ProviderNotConfiguredError("VertexAI", _SETUP_INSTRUCTIONS)

        # Resolve parameters
        temperature = self._resolve(temperature, "temperature", 0.1)
        max_tokens = self._resolve(max_tokens, "max_tokens", 2048)
        max_retries = self._resolve(max_retries, "max_retries", 2)

        system_prompt = system_prompt or _FALLBACK_SYSTEM_PROMPT
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"News text:\n{text}"},
        ]

        last_error: str | None = None
        for attempt in range(max_retries + 1):
            start_time = time.time()
            try:
                raw_content: str = ""

                # Try Vertex AI SDK first, fall back to generativeai
                sdk_errors: list[str] = []
                for fn, sdk_name in [
                    (_try_vertex_ai, "vertexai"),
                    (_try_generativeai, "generativeai"),
                ]:
                    try:
                        raw_content = fn(self.model_name, messages, temperature, max_tokens)
                        break
                    except (ImportError, EnvironmentError) as sdk_exc:
                        sdk_errors.append(f"{sdk_name}: {sdk_exc}")
                        continue
                else:
                    raise ProviderNotConfiguredError("VertexAI", _SETUP_INSTRUCTIONS)

                latency = time.time() - start_time

                from src.llm_runner import parse_llm_response
                parsed_entities = parse_llm_response(raw_content)

                stripped = raw_content.strip()
                if stripped.startswith("{") and stripped.endswith("}"):
                    method = "direct_json"
                elif "```" in raw_content:
                    method = "codeblock"
                else:
                    method = "fallback"

                tokens_per_sec = len(raw_content.split()) * 1.3 / latency if latency > 0 else 0.0

                return {
                    "entities": parsed_entities,
                    "entities_raw": raw_content,
                    "latency": latency,
                    "tokens_per_sec": round(tokens_per_sec, 2),
                    "model": self.model_name,
                    "parse_method": method,
                    "retries": attempt,
                    "sys_metrics": {},
                    "provider": "vertexai",
                }

            except ProviderNotConfiguredError:
                raise
            except Exception as exc:
                last_error = str(exc)
                logger.warning(
                    "VertexAI attempt %d/%d failed for '%s': %s",
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
            "provider": "vertexai",
        }
