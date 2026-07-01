from __future__ import annotations
import os
import json
from dataclasses import dataclass, asdict

@dataclass
class BenchmarkConfig:
    models: list[str] = None
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

    def __post_init__(self):
            self.models = [
                'gemini-1.5-flash-lite', 'gemini-2.0-flash-lite', 'gemini-flash-lite-latest',
                'gemma4:31b-cloud',
                'minimax-m3:cloud',
                'gemma4:31b', 'sonct988/gemma4-26b-a4b-it-q4km-256k:latest',
                'gpt-oss:20b',
                'gemma4:latest', 'gemma:latest',
                'qwen3:8b', 'qwen2.5:14b', 'mistral-nemo:latest', 'nuextract:latest',
                'llama3.1:8b', 'llama3.2:latest', 'nemotron-mini:4b', 'deepseek-r1:1.5b',
                'phi3.5:latest', 'phi3.5'
            ]

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
