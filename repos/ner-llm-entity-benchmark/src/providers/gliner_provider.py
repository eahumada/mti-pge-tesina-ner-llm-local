"""
src/providers/gliner_provider.py
---------------------------------
GLiNER provider implementation.

GLiNER (Generalist and Lightweight model for Named Entity Recognition) is a
zero-shot NER model based on bidirectional encoders (BERT-like). Unlike LLMs,
it receives the raw text *and* a list of entity-type labels, and returns
spans directly — no prompt engineering required.

Supported model aliases (canonical → HuggingFace path):
  gliner:small   → urchade/gliner_small-v2.1    (~70 MB)
  gliner:medium  → urchade/gliner_medium-v2.1   (~170 MB)  ← default
  gliner:large   → urchade/gliner_large-v2.1    (~340 MB)
  gliner:multitask → urchade/gliner-multitask-large-v0.5

Full HuggingFace paths (e.g. "urchade/gliner_medium-v2.1") are also accepted.

Requires:
  pip install gliner        (already installed in the project venv)

Reference: https://github.com/urchade/GLiNER
"""
from __future__ import annotations

import logging
import threading
import time
from typing import Any

from src.providers.base import (
    LLMProvider,
    ExtractionResult,
    ProviderNotConfiguredError,
)

logger = logging.getLogger("ner_benchmark.providers.gliner")

# ---------------------------------------------------------------------------
# Canonical alias → HuggingFace model ID
# ---------------------------------------------------------------------------

_ALIAS_MAP: dict[str, str] = {
    "gliner:small":       "urchade/gliner_small-v2.1",
    "gliner:medium":      "urchade/gliner_medium-v2.1",
    "gliner:large":       "urchade/gliner_large-v2.1",
    "gliner:multitask":   "urchade/gliner-multitask-large-v0.5",
    # shorthand without prefix
    "gliner_small":       "urchade/gliner_small-v2.1",
    "gliner_medium":      "urchade/gliner_medium-v2.1",
    "gliner_large":       "urchade/gliner_large-v2.1",
    "gliner_multitask":   "urchade/gliner-multitask-large-v0.5",
}

_DEFAULT_HF_MODEL = "urchade/gliner_medium-v2.1"

# NER labels expected by the benchmark (maps to ExtractionResult keys)
_ENTITY_LABELS: list[str] = ["person", "organization", "location"]

_LABEL_TO_KEY: dict[str, str] = {
    "person":       "Persons",
    "organization": "Organizations",
    "location":     "Locations",
}

_SETUP_INSTRUCTIONS = """\
To use GLiNER models:

1. Install the package (if not already installed):
   pip install gliner

2. On first use the model weights are downloaded from HuggingFace (~70–340 MB).
   Make sure you have an internet connection OR pre-cache the model:
   python -c "from gliner import GLiNER; GLiNER.from_pretrained('urchade/gliner_medium-v2.1')"

Supported model names:
  gliner:small / gliner:medium (default) / gliner:large / gliner:multitask
  or any full HuggingFace path such as 'urchade/gliner_medium-v2.1'
"""


def _resolve_hf_model(model_name: str) -> str:
    """
    Convert a user-facing model name to its HuggingFace repo ID.

    Resolution order:
    1. Exact match in _ALIAS_MAP (case-insensitive key)
    2. Already looks like a HuggingFace path (contains '/')
    3. Falls back to _DEFAULT_HF_MODEL
    """
    key = model_name.lower().strip()
    if key in _ALIAS_MAP:
        return _ALIAS_MAP[key]
    if "/" in model_name:
        # Treat as a raw HuggingFace repo ID (e.g. "urchade/gliner_small-v2.1")
        return model_name
    logger.warning(
        "GlinerProvider: unrecognised model name '%s', falling back to default '%s'.",
        model_name, _DEFAULT_HF_MODEL,
    )
    return _DEFAULT_HF_MODEL


# ---------------------------------------------------------------------------
# GlinerProvider
# ---------------------------------------------------------------------------

class GlinerProvider(LLMProvider):
    """
    Concrete provider for GLiNER zero-shot NER models.

    The underlying GLiNER model is loaded **lazily** (only on the first call to
    ``extract_entities``), which means instantiation is always fast even if the
    weights have not been cached yet.  The lazy load is protected by a
    ``threading.Lock`` so concurrent workers don't race to download the model.

    Parameters
    ----------
    model_name : str
        Canonical alias (e.g. ``"gliner:medium"``) or a full HuggingFace repo
        ID (e.g. ``"urchade/gliner_medium-v2.1"``).
    config : BenchmarkConfig | None
        Global run configuration.  GLiNER ignores temperature / seed / retries
        (they don't apply to encoder-based NER), but reads ``threshold`` if
        present via ``config.gliner_threshold``.
    threshold : float
        Minimum confidence score to accept a predicted span (default 0.5).
    """

    def __init__(
        self,
        model_name: str,
        config: Any = None,
        threshold: float = 0.5,
    ) -> None:
        super().__init__(model_name, config)
        self._hf_model_id: str = _resolve_hf_model(model_name)
        self._threshold: float = threshold
        self._model: Any = None          # lazy-loaded GLiNER instance
        self._lock: threading.Lock = threading.Lock()

    # ------------------------------------------------------------------
    # is_available
    # ------------------------------------------------------------------

    def is_available(self) -> bool:
        """
        Returns True if the ``gliner`` package is importable.

        No network call is made here; the model weights are downloaded on
        first use inside ``extract_entities``.
        """
        try:
            import gliner  # noqa: F401
            return True
        except ImportError:
            raise ProviderNotConfiguredError("GLiNER", _SETUP_INSTRUCTIONS)

    # ------------------------------------------------------------------
    # _load_model  (lazy, thread-safe)
    # ------------------------------------------------------------------

    def _load_model(self) -> Any:
        """Load and cache the GLiNER model (thread-safe, idempotent)."""
        if self._model is not None:
            return self._model

        with self._lock:
            # Double-checked locking: re-test inside the lock
            if self._model is not None:
                return self._model

            try:
                from gliner import GLiNER  # noqa
            except ImportError as exc:
                raise ProviderNotConfiguredError("GLiNER", _SETUP_INSTRUCTIONS) from exc

            logger.info(
                "GlinerProvider: loading model '%s' (first call — may download weights).",
                self._hf_model_id,
            )
            load_start = time.time()
            self._model = GLiNER.from_pretrained(self._hf_model_id)
            load_elapsed = time.time() - load_start
            logger.info(
                "GlinerProvider: model '%s' loaded in %.2fs.",
                self._hf_model_id, load_elapsed,
            )

        return self._model

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
        """
        Run GLiNER NER inference on *text*.

        The ``system_prompt``, ``temperature``, ``max_tokens``, ``seed``, and
        ``max_retries`` parameters are accepted for interface compatibility but
        are intentionally ignored — GLiNER is an encoder model and does not use
        generative decoding parameters.

        Returns
        -------
        ExtractionResult
            Standard result dict with:
              - ``entities``      → ``{"Persons": [...], "Organizations": [...], "Locations": [...]}``
              - ``entities_raw``  → JSON-like string representation of the raw spans
              - ``latency``       → wall-clock inference time in seconds
              - ``tokens_per_sec`` → 0.0 (not applicable for encoder models)
              - ``model``         → the HuggingFace repo ID used
              - ``parse_method``  → ``"gliner_native"``
              - ``retries``       → 0 (encoder models don't retry on JSON errors)
              - ``sys_metrics``   → ``{}``
              - ``provider``      → ``"gliner"``
        """
        # Ensure package + model are available
        try:
            model = self._load_model()
        except ProviderNotConfiguredError:
            raise
        except Exception as exc:
            logger.error("GlinerProvider: failed to load model — %s", exc)
            raise ProviderNotConfiguredError("GLiNER", _SETUP_INSTRUCTIONS) from exc

        # Resolve threshold (config override → constructor default)
        threshold = (
            getattr(self.config, "gliner_threshold", None) or self._threshold
        )

        start_time = time.time()

        try:
            raw_spans: list[dict] = model.predict_entities(
                text,
                _ENTITY_LABELS,
                threshold=threshold,
            )
        except Exception as exc:
            latency = time.time() - start_time
            logger.error(
                "GlinerProvider: predict_entities failed for model '%s': %s",
                self._hf_model_id, exc,
            )
            return {
                "entities": {"Persons": [], "Organizations": [], "Locations": []},
                "entities_raw": f"ERROR: {exc}",
                "latency": latency,
                "tokens_per_sec": 0.0,
                "model": self._hf_model_id,
                "parse_method": "failed",
                "retries": 0,
                "sys_metrics": {},
                "provider": "gliner",
            }

        latency = time.time() - start_time

        # Convert GLiNER spans → standardised entity dict
        entities: dict[str, list[str]] = {
            "Persons": [],
            "Organizations": [],
            "Locations": [],
        }
        for span in raw_spans:
            label: str = span.get("label", "").lower()
            text_value: str = span.get("text", "").strip()
            if not text_value:
                continue
            bucket = _LABEL_TO_KEY.get(label)
            if bucket and text_value not in entities[bucket]:
                entities[bucket].append(text_value)

        # Build a human-readable raw representation
        entities_raw = str(raw_spans)

        logger.debug(
            "GlinerProvider: extracted %d entities in %.3fs (model=%s, threshold=%.2f).",
            sum(len(v) for v in entities.values()),
            latency,
            self._hf_model_id,
            threshold,
        )

        return {
            "entities": entities,
            "entities_raw": entities_raw,
            "latency": round(latency, 4),
            "tokens_per_sec": 0.0,
            "model": self._hf_model_id,
            "parse_method": "gliner_native",
            "retries": 0,
            "sys_metrics": {},
            "provider": "gliner",
        }

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"GlinerProvider(alias={self.model_name!r}, "
            f"hf_model={self._hf_model_id!r}, "
            f"loaded={self._model is not None})"
        )
