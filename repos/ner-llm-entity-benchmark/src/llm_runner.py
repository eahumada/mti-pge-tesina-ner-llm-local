from __future__ import annotations
import json
import logging
import re
import time
import requests
import ollama

import os
import subprocess
from src.system_monitor import SystemMonitor

logger = logging.getLogger("ner_benchmark.llm_runner")

def load_system_prompt(prompt_file: str = "SYSTEM_PROMPT.md") -> str:
    """Reads system prompt file and isolates the content under the [SYSTEM] section."""
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if "[SYSTEM]" in content:
            system_part = content.split("[SYSTEM]")[1]
            if "[USER]" in system_part:
                system_part = system_part.split("[USER]")[0]
            return system_part.strip()
        return content.strip()
    except Exception as e:
        logger.warning(f"Error loading system prompt file {prompt_file}: {e}. Using fallback.")
        return (
            "You are an expert compliance and anti-money laundering (AML) analyst. "
            "Perform Named Entity Recognition (NER) on news. Extract entities into: "
            "Persons, Organizations, Locations. Return ONLY valid JSON with keys: "
            "\"Persons\", \"Organizations\", \"Locations\"."
        )

def build_messages(system_prompt: str, news_text: str) -> list[dict]:
    """Builds the structured chat messages list."""
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"News text:\n{news_text}"}
    ]

def build_nuextract_messages(news_text: str) -> list[dict]:
    """
    Builds NuExtract-format prompt using its required template structure.
    NuExtract is purely extractive — no system prompt, uses a template block instead.
    """
    template = json.dumps({"Persons": [], "Organizations": [], "Locations": []}, indent=2)
    content = (
        f"### Template:\n{template}\n\n"
        f"### Text:\n{news_text}\n\n"
        f"### Expected Output:"
    )
    return [{"role": "user", "content": content}]

# Models that need special routing
_NUEXTRACT_MODELS = {"nuextract", "nuextract:latest", "nuextract:3.8b", "nuextract:8b"}
_QWEN3_THINKING_MODELS = {"qwen3:8b", "qwen3:14b", "qwen3:32b", "qwen3:latest"}

# Cloud-hosted Ollama models (executed remotely, no local VRAM, rate-limit aware)
# These models use standard Ollama chat API but are served by Ollama cloud infrastructure.
def is_cloud_model(model_name: str) -> bool:
    """Returns True if model is a cloud-hosted Ollama model (e.g. gemma4:31b-cloud, minimax-m3:cloud)."""
    key = model_name.lower()
    return "-cloud" in key or "minimax" in key

def parse_llm_response(raw_response: str) -> dict:
    """
    Parses LLM outputs with a multi-strategy cascade:
    1. Direct JSON parse (clean responses)
    2. Markdown codeblock extraction (greedy — handles large payloads)
    3. Brace-scanner: find outermost {...} by counting braces (handles preamble/postamble text)
    4. Truncation repair: attempt to close open JSON structures from cut-off responses
    5. Regex key extraction fallback: salvage entities even from malformed JSON
    """
    cleaned = raw_response.strip()

    # Strategy 1: Direct parse
    try:
        parsed = json.loads(cleaned)
        logger.debug("Successfully parsed LLM response directly as JSON.")
        return _normalize_keys(parsed)
    except json.JSONDecodeError:
        pass

    # Strategy 2: Markdown codeblock — greedy to capture full large JSON payloads
    codeblock_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", cleaned, re.DOTALL)
    if codeblock_match:
        try:
            parsed = json.loads(codeblock_match.group(1))
            logger.debug("Successfully parsed markdown code block JSON.")
            return _normalize_keys(parsed)
        except json.JSONDecodeError:
            pass

    # Strategy 3: Brace-scanner — find the outermost {...} ignoring any preamble/postamble
    start = cleaned.find("{")
    if start != -1:
        depth = 0
        end = -1
        for i, ch in enumerate(cleaned[start:], start):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end != -1:
            candidate = cleaned[start:end]
            try:
                parsed = json.loads(candidate)
                logger.debug("Successfully parsed JSON via brace-scanner.")
                return _normalize_keys(parsed)
            except json.JSONDecodeError:
                pass

            # Strategy 4: Truncation repair — model cut off the response mid-list
            # Remove trailing incomplete items and attempt to close open structures
            repaired = re.sub(r',\s*"[^"]*$', '', candidate)  # remove incomplete trailing string
            repaired = re.sub(r',\s*$', '', repaired)          # remove trailing comma
            # Count unclosed brackets/braces and close them
            open_brackets = repaired.count('[') - repaired.count(']')
            open_braces = repaired.count('{') - repaired.count('}')
            repaired += ']' * max(0, open_brackets) + '}' * max(0, open_braces)
            try:
                parsed = json.loads(repaired)
                logger.debug("Successfully parsed JSON after truncation repair.")
                return _normalize_keys(parsed)
            except json.JSONDecodeError:
                pass

    # Strategy 5: Regex key extraction — salvage entities directly from malformed JSON
    fallback = {"Persons": [], "Organizations": [], "Locations": []}
    for key, target in [("Persons", "Persons"), ("Organizations", "Organizations"), ("Locations", "Locations"),
                        ("persons", "Persons"), ("people", "Persons"), ("organizations", "Organizations"),
                        ("companies", "Organizations"), ("locations", "Locations"), ("places", "Locations")]:
        pattern = rf'"{key}"\s*:\s*\[(.*?)\]'
        m = re.search(pattern, cleaned, re.DOTALL | re.IGNORECASE)
        if m:
            items = re.findall(r'"([^"]+)"', m.group(1))
            fallback[target].extend(items)
    if any(fallback.values()):
        logger.debug("Successfully extracted entities via regex key fallback.")
        return fallback

    logger.warning(f"Failed to parse JSON from raw response: {cleaned[:200]}...")
    return {"Persons": [], "Organizations": [], "Locations": []}

def _normalize_keys(parsed: dict) -> dict:
    """Normalizes keys to 'Persons', 'Organizations', 'Locations'."""
    normalized = {"Persons": [], "Organizations": [], "Locations": []}
    
    # Map different possible casing/plural names
    mappings = {
        "persons": "Persons",
        "person": "Persons",
        "people": "Persons",
        "organizations": "Organizations",
        "organization": "Organizations",
        "companies": "Organizations",
        "company": "Organizations",
        "locations": "Locations",
        "location": "Locations",
        "places": "Locations"
    }
    
    for k, v in parsed.items():
        k_lower = k.lower()
        target_key = mappings.get(k_lower, None)
        
        # Ensure values are list of strings
        if isinstance(v, list):
            vals = [str(item) for item in v]
        else:
            vals = [str(v)] if v else []
            
        if target_key:
            normalized[target_key].extend(vals)
            
    # Deduplicate lists
    for k in normalized:
        normalized[k] = list(set(normalized[k]))
        
    return normalized

def extract_entities_with_ollama(
    text: str,
    model_name: str,
    system_prompt: str = "",
    temperature: float = 0.1,
    max_tokens: int = 2048,
    seed: int = 42,
    max_retries: int = 2,
    ollama_base_url: str = "http://localhost:11434"
) -> dict:
    """
    Backward-compatible shim.

    Prompts a local Ollama model to perform NER with retry logic and config
    options.  Internally delegates to OllamaProvider via the provider Facade
    (src.providers.get_provider) so all routing, parsing, and monitoring logic
    lives in a single place.

    Supports model-specific routing:
      - NuExtract family: uses template/text format instead of system prompt
      - Qwen3 family: enables chain-of-thought thinking mode for better entity
        disambiguation
      - Cloud-hosted models (e.g. gemma4:31b-cloud): bypasses local VRAM check

    Parameters mirror the original signature exactly so all existing callers
    in main.py continue to work without modification.
    """
    # Build a lightweight config-like namespace so OllamaProvider can read
    # the run parameters without requiring a full BenchmarkConfig import here.
    class _Cfg:  # noqa: N801
        pass

    cfg = _Cfg()
    cfg.temperature = temperature
    cfg.max_tokens = max_tokens
    cfg.seed = seed
    cfg.max_retries = max_retries
    cfg.ollama_base_url = ollama_base_url

    # Import here to avoid circular imports at module level
    from src.providers import get_provider  # noqa: PLC0415

    provider = get_provider(model_name, config=cfg, ollama_base_url=ollama_base_url)
    return provider.extract_entities(
        text,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        seed=seed,
        max_retries=max_retries,
    )

def manage_model_lifecycle(current_model: str, next_model: str | None, ollama_base_url: str = "http://localhost:11434") -> None:
    """Calls Ollama REST API to unload model from VRAM and load the next model if requested."""
    try:
        # Unload current model
        url = f"{ollama_base_url}/api/generate"
        payload = {"model": current_model, "keep_alive": 0}
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            logger.info(f"Successfully unloaded weights for {current_model} from VRAM.")
        else:
            logger.warning(f"Failed to unload {current_model}: HTTP {response.status_code}")
    except Exception as e:
        logger.error(f"Error unloading model {current_model}: {e}")
        
    time.sleep(2.0) # Wait for VRAM allocation updates

    if next_model:
        try:
            # Pre-load next model (call chat with empty prompt)
            client = ollama.Client(host=ollama_base_url)
            logger.info(f"Warming up model {next_model} into VRAM...")
            client.chat(model=next_model, messages=[{"role": "user", "content": "hello"}])
        except Exception as e:
            logger.error(f"Error warming up model {next_model}: {e}")

def check_model_available(model_name: str, ollama_base_url: str = "http://localhost:11434") -> bool:
    """Checks if model is pulled in local Ollama repository."""
    try:
        url = f"{ollama_base_url}/api/tags"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            models = [m.get("name") for m in response.json().get("models", [])]
            # Match direct names or with tags (e.g. llama3.2:latest)
            for m in models:
                if m == model_name or m.split(":")[0] == model_name:
                    return True
            return False
        return False
    except Exception as e:
        logger.error(f"Error checking model availability: {e}")
        return False
