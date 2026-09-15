#!/usr/bin/env python3
"""
tools/correr_cloud_todas_semillas.py
------------------------------------
Ejecuta gemma4:31b-cloud sobre Ollama Cloud para las 4 semillas restantes de R2 (N=120, kb_combined)
en paralelo al procesamiento local de GPU, sin consumir VRAM ni recursos locales.
Cada semilla produce su propio directorio certificado con verificar_corrida.py.
"""
import os
import sys
import time
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BENCHMARK_DIR = REPO_ROOT / "repos" / "ner-llm-entity-benchmark"
VENV_PYTHON = BENCHMARK_DIR / "venv" / "bin" / "python3"
VERIFY_SCRIPT = BENCHMARK_DIR / "tools" / "verificar_corrida.py"

SEEDS = [123, 456, 789, 1024]
RESULTS_BASE = BENCHMARK_DIR / "results" / "barras_error_n120_REMOTO"

def run_seed_cloud(seed: int):
    target_dir = RESULTS_BASE / f"seed_{seed}_cloud"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    csv_file = target_dir / "benchmark_results.csv"
    if csv_file.exists():
        print(f"[gemma4:31b-cloud | seed {seed}] YA EXISTE. Verificando...")
        v_proc = subprocess.run([str(VENV_PYTHON), str(VERIFY_SCRIPT), str(target_dir)], cwd=str(REPO_ROOT))
        if v_proc.returncode == 0:
            print(f"[gemma4:31b-cloud | seed {seed}] VÁLIDA y completa.")
            return True

    print(f"\n=======================================================")
    print(f"EJECUTANDO gemma4:31b-cloud (N=120) — SEED {seed}")
    print(f"=======================================================\n")
    
    cmd = [
        str(VENV_PYTHON), "src/main.py",
        "--models", "gemma4:31b-cloud",
        "--rag-study",
        "--rag-mode", "kb_combined",
        "--data-file", "data/benchmark_balanced_120.json",
        "--seed", str(seed),
        "--num-workers", "2",
        "--max-tokens", "4096",
        "--results-dir", str(target_dir)
    ]
    
    env = os.environ.copy()
    proc = subprocess.run(cmd, cwd=str(BENCHMARK_DIR), env=env)
    if proc.returncode != 0:
        print(f"ERROR: Falló gemma4:31b-cloud seed {seed} (código {proc.returncode})")
        return False
        
    v_proc = subprocess.run([str(VENV_PYTHON), str(VERIFY_SCRIPT), str(target_dir)], cwd=str(REPO_ROOT))
    if v_proc.returncode == 0:
        print(f"[gemma4:31b-cloud | seed {seed}] VÁLIDA y certificada.")
        return True
    else:
        print(f"ALERTA: verificar_corrida devolvió código {v_proc.returncode}")
        return False

def main():
    print("Iniciando suite en la nube para gemma4:31b-cloud (semillas 123, 456, 789, 1024)...")
    for seed in SEEDS:
        ok = run_seed_cloud(seed)
        if not ok:
            print(f"Deteniendo suite de nube tras error en seed {seed}")
            sys.exit(1)
        time.sleep(2)
    print("\n>>> TODAS LAS SEMILLAS DE gemma4:31b-cloud COMPLETADAS CON ÉXITO <<<")

if __name__ == "__main__":
    main()
