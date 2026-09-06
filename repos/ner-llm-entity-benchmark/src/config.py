from __future__ import annotations
import os
import json
from dataclasses import dataclass, field, asdict

RESULTS_ROOT = 'results'


class ResultsDirRootError(RuntimeError):
    """Raised when a benchmark run would write into the results ROOT directory."""


def _is_results_root(path: str) -> bool:
    """True if `path` points at the results ROOT (not a subdirectory of it).

    Normalizes the usual equivalent spellings — 'results', 'results/',
    './results', 'results/.', 'results/sub/..' and any absolute form of the
    same location — so none of them can slip through.
    """
    if path is None:
        return True
    candidate = str(path).strip()
    if candidate == '':
        return True
    normalized = os.path.normpath(candidate)
    if normalized in (RESULTS_ROOT, os.path.join('.', RESULTS_ROOT)):
        return True
    return os.path.abspath(normalized) == os.path.abspath(RESULTS_ROOT)


def assert_not_results_root(results_dir: str) -> None:
    """Abort the run if `results_dir` resolves to the results ROOT directory.

    INCIDENT (2026-07-01 -> 2026-07-27): the N=30 augmented corpus run wrote
    its artifacts directly into `results/`. A later run overwrote them and the
    per-record data of the run backing the thesis' headline figure
    (F1 = 79.03%) was lost permanently; only the aggregated metrics in
    `benchmark_augmented_30.log` survived.

    A subdirectory of results/ (e.g. 'results/benchmark_x_16models', or the
    auto-generated 'results/<dataset>_<timestamp>') is legitimate and passes.
    """
    if _is_results_root(results_dir):
        raise ResultsDirRootError(
            "ABORT: refusing to run with results_dir="
            f"{results_dir!r}, which resolves to the results ROOT directory "
            f"({os.path.abspath(RESULTS_ROOT)}).\n"
            "Writing to the root overwrites previous runs and has already "
            "caused permanent data loss (2026-07-01 N=30 run, clobbered on "
            "2026-07-27).\n"
            "Fix: omit --results-dir to get an auto-generated timestamped "
            "subdirectory, or pass an explicit SUBdirectory such as "
            "--results-dir results/my_run_name."
        )


@dataclass
class BenchmarkConfig:
    models: list[str] = field(default_factory=lambda: [
        'gemini-3.1-flash-lite', 'gemini-3.5-flash',
        'gemma4:31b-cloud',
        'minimax-m3:cloud',
        'gemma4:31b', 'sonct988/gemma4-26b-a4b-it-q4km-256k:latest',
        'gpt-oss:20b',
        'gemma4:latest', 'gemma:latest',
        'qwen3:8b', 'qwen2.5:14b', 'mistral-nemo:latest', 'nuextract:latest',
        'llama3.1:8b', 'llama3.2:latest', 'nemotron-mini:4b', 'deepseek-r1:1.5b',
        'phi3.5:latest', 'gemma4:12b-mlx', 'phi3.5'
    ])
    batch_size: int = 5
    num_workers: int = 2
    max_retries: int = 2
    fuzzy_threshold: int = 85
    redis_url: str = 'redis://localhost:6379'
    data_file: str = 'data/sample_sanctions.json'
    results_dir: str = 'results'
    checkpoint_file: str = 'results/.checkpoint.json'
    system_prompt_file: str = 'SYSTEM_PROMPT.md'
    ollama_base_url: str = 'http://localhost:11434'
    temperature: float = 0.1
    max_tokens: int = 2048
    seed: int = 42
    rag_study: bool = False
    # RAG mode selector — controls Knowledge Base vs. legacy entity dict retrieval.
    # 'entities'      : Legacy mode (original dict-RAG behavior, default). Backward compatible.
    # 'kb_guidelines' : Inject domain-specific NER disambiguation rules from KB.
    # 'kb_fewshot'    : Inject a semantically similar annotated few-shot example from KB.
    # 'kb_combined'   : Inject both guidelines + one exemplar (recommended, best F1).
    # See: research/rag/2026-08-31_analisis_contenido_rag_base_conocimientos.md
    # See: src/kb_rag_manager.py
    rag_mode: str = 'entities'
    # Prompt Ablation Study flag (REQ41). Persisted so that a run's
    # `run_config.json` records whether it was an ablation sweep instead of
    # being indistinguishable from a plain baseline run.
    # See: src/main.py::run_benchmark(ablation=...)
    ablation: bool = False

    def __post_init__(self):
        if self.results_dir == 'results':
            from datetime import datetime
            import os
            
            # Parse dataset name from data_file
            ds_name = os.path.basename(self.data_file).replace('.json', '')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.results_dir = os.path.join('results', f"{ds_name}_{timestamp}")
            self.checkpoint_file = os.path.join(self.results_dir, ".checkpoint.json")

        # DATA-LOSS GUARDRAIL: never let a run write into the results ROOT.
        # (see assert_not_results_root docstring for the incident this prevents)
        assert_not_results_root(self.results_dir)

    def to_dict(self) -> dict:
        return asdict(self)

def load_system_prompt(prompt_file: str = 'SYSTEM_PROMPT.md') -> str:
    """Reads the SYSTEM_PROMPT.md file and parses content under the [SYSTEM] tag."""
    if not os.path.exists(prompt_file):
        # Return fallback if not found
        return (
            "You are an expert compliance and anti-money laundering (AML) analyst. "
            "Perform Named Entity Recognition (NER) on news. Extract entities into: "
            "Persons, Organizations, Locations. Return ONLY valid JSON with keys: "
            "\"Persons\", \"Organizations\", \"Locations\"."
        )
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if '[SYSTEM]' in content:
        parts = content.split('[SYSTEM]')
        system_content = parts[1]
        if '[USER]' in system_content:
            system_content = system_content.split('[USER]')[0]
        return system_content.strip()
    return content.strip()

def ensure_directories(config: BenchmarkConfig) -> None:
    """Creates the data and results directories if they don't exist."""
    # DATA-LOSS GUARDRAIL (second line of defence): __post_init__ already
    # checks this, but results_dir can also be mutated after construction —
    # this is the last choke point before anything is written to disk.
    assert_not_results_root(config.results_dir)
    os.makedirs(os.path.dirname(config.data_file) or ".", exist_ok=True)
    os.makedirs(config.results_dir, exist_ok=True)
