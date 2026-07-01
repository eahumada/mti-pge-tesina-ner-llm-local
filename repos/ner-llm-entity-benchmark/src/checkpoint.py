from __future__ import annotations
import json
import os
import time
from dataclasses import dataclass, field, asdict

@dataclass
class CheckpointState:
    completed_batches: dict[str, list[int]] = field(default_factory=dict)
    results: list[dict] = field(default_factory=list)
    timestamp: str = ""
    config_hash: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

def save_checkpoint(state: CheckpointState, filepath: str) -> None:
    """Saves checkpoint state to JSON."""
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    state.timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(state.to_dict(), f, indent=2)

def load_checkpoint(filepath: str) -> CheckpointState | None:
    """Loads checkpoint state from JSON, returning None if not found."""
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return CheckpointState(
            completed_batches=data.get("completed_batches", {}),
            results=data.get("results", []),
            timestamp=data.get("timestamp", ""),
            config_hash=data.get("config_hash", "")
        )
    except Exception as e:
        print(f"Error loading checkpoint: {e}")
        return None

def is_batch_completed(state: CheckpointState, model: str, batch_idx: int) -> bool:
    """Checks if a batch is marked completed for a specific model."""
    return batch_idx in state.completed_batches.get(model, [])

def mark_batch_completed(state: CheckpointState, model: str, batch_idx: int, batch_results: list[dict]) -> None:
    """Marks a batch completed and appends its results."""
    if model not in state.completed_batches:
        state.completed_batches[model] = []
    if batch_idx not in state.completed_batches[model]:
        state.completed_batches[model].append(batch_idx)
    state.results.extend(batch_results)
