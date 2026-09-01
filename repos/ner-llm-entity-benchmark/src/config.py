from __future__ import annotations
import os
import json
from dataclasses import dataclass, field, asdict

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
        'phi3.5:latest', 'gemma4:12b-mlx-q8-64k', 'phi3.5'
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

    def __post_init__(self):
        if self.results_dir == 'results':
            from datetime import datetime
            import os
            
            # Parse dataset name from data_file
            ds_name = os.path.basename(self.data_file).replace('.json', '')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.results_dir = os.path.join('results', f"{ds_name}_{timestamp}")
            self.checkpoint_file = os.path.join(self.results_dir, ".checkpoint.json")

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
    os.makedirs(os.path.dirname(config.data_file) or ".", exist_ok=True)
    os.makedirs(config.results_dir, exist_ok=True)
