#!/usr/bin/env python3
"""
Pipeline Maestro de Re-corridas para el Equipo 48 GB.
Ejecuta de extremo a extremo:
1. Espera a que culmine R5 (Variantes N=30 par emparejado) si está en ejecución.
2. R1 Fase 2: Variantes 2x2 sobre N=120 con 5 semillas (gemma4:latest).
3. R2: Barra de error del titular en N=120 (11/13 modelos x 5 semillas x kb_combined).
Con verificación rigurosa (verificar_corrida.py) y commit/push incremental por semilla.
"""

import os
import sys
import time
import subprocess
import pandas as pd
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BENCHMARK_DIR = REPO_ROOT / "repos" / "ner-llm-entity-benchmark"
VENV_PYTHON = BENCHMARK_DIR / "venv" / "bin" / "python3"
VERIFY_SCRIPT = BENCHMARK_DIR / "tools" / "verificar_corrida.py"

SEEDS = [42, 123, 456, 789, 1024]

R2_MODELS = [
    "gemma4:31b-cloud", "gemma4:31b-mlx", "gemma4:12b-mlx", "gemma4:latest",
    "qwen3:8b", "gpt-oss:20b", "mistral-nemo:latest", "llama3.2:latest",
    "llama3.1:8b", "nemotron-mini:4b", "deepseek-r1:1.5b"
]

def git_commit_push(msg: str):
    subprocess.run(["git", "add", "results/", "CURRENT-TASKS.md", "remote_48g/"], cwd=str(REPO_ROOT))
    res = subprocess.run(["git", "commit", "-m", msg], cwd=str(REPO_ROOT), capture_output=True, text=True)
    print(res.stdout)
    subprocess.run(["git", "pull", "--rebase"], cwd=str(REPO_ROOT))
    subprocess.run(["git", "push", "origin", "main"], cwd=str(REPO_ROOT))

def is_r1_n120_complete(results_dir: Path) -> bool:
    csv_file = results_dir / "benchmark_results.csv"
    if not csv_file.exists():
        return False
    try:
        df = pd.read_csv(csv_file)
        if len(df) == 480 and not (df["parse_method"] == "failed").any():
            return True
    except Exception:
        pass
    return False

def is_r2_complete(results_dir: Path, n_models: int) -> bool:
    csv_file = results_dir / "benchmark_results.csv"
    if not csv_file.exists():
        return False
    try:
        df = pd.read_csv(csv_file)
        expected_rows = n_models * 2 * 120 # 11 * 2 * 120 = 2640
        if len(df) == expected_rows and not (df["parse_method"] == "failed").any():
            return True
    except Exception:
        pass
    return False

def wait_for_r5():
    print("\n=======================================================")
    print("VERIFICANDO ESTADO DE R5...")
    print("=======================================================\n")
    
    # Comprobar si el script de R5 sigue corriendo en el sistema
    while True:
        res = subprocess.run(["pgrep", "-f", "correr_r5_variantes_n30.py"], capture_output=True, text=True)
        pids = [p for p in res.stdout.strip().split() if p and int(p) != os.getpid()]
        if not pids:
            print("R5 no tiene procesos activos en ejecución.")
            break
        print(f"R5 sigue activo (PID {pids}). Esperando 30s...")
        time.sleep(30)
    print("Fase R5 completada o finalizada.\n")

def run_r1_fase2():
    print("\n=======================================================")
    print("INICIANDO R1 FASE 2: N=120 (Variantes 2x2 x 5 semillas)")
    print("=======================================================\n")
    
    results_base = BENCHMARK_DIR / "results" / "variantes_5semillas_n120_REMOTO"
    
    for seed in SEEDS:
        target_dir = results_base / f"seed_{seed}"
        target_dir.mkdir(parents=True, exist_ok=True)
        
        if is_r1_n120_complete(target_dir):
            print(f"[R1 N=120 | seed {seed}] YA COMPLETADA (480 filas, 0 fallos).")
            continue
            
        print(f"\n--- Ejecutando R1 N=120: Seed {seed} ---")
        cmd = [
            str(VENV_PYTHON), "src/main.py",
            "--models", "gemma4:latest",
            "--ablation",
            "--data-file", "data/benchmark_balanced_120.json",
            "--seed", str(seed),
            "--num-workers", "4",
            "--results-dir", str(target_dir)
        ]
        
        env = os.environ.copy()
        proc = subprocess.run(cmd, cwd=str(BENCHMARK_DIR), env=env)
        if proc.returncode != 0:
            print(f"ERROR: Falló R1 N=120 seed {seed} (código {proc.returncode})")
            return False
            
        # Verificar corrida
        v_proc = subprocess.run([str(VENV_PYTHON), str(VERIFY_SCRIPT), str(target_dir)], cwd=str(REPO_ROOT))
        if v_proc.returncode == 0:
            print(f"[R1 N=120 | seed {seed}] VÁLIDA y certificada.")
            git_commit_push(f"feat(remoto): R1 Fase 2 N=120 semilla {seed} completada")
        else:
            print(f"ALERTA: verificar_corrida devolvió código {v_proc.returncode}")
            
    return True

def run_r2():
    print("\n=======================================================")
    print("INICIANDO R2: Barra de error del titular N=120 (11 modelos x 5 semillas)")
    print("=======================================================\n")
    
    results_base = BENCHMARK_DIR / "results" / "barras_error_n120_REMOTO"
    
    for seed in SEEDS:
        target_dir = results_base / f"seed_{seed}"
        target_dir.mkdir(parents=True, exist_ok=True)
        
        if is_r2_complete(target_dir, len(R2_MODELS)):
            print(f"[R2 | seed {seed}] YA COMPLETADA.")
            continue
            
        print(f"\n--- Ejecutando R2: Seed {seed} ---")
        cmd = [
            str(VENV_PYTHON), "src/main.py",
            "--models", *R2_MODELS,
            "--rag-study",
            "--rag-mode", "kb_combined",
            "--data-file", "data/benchmark_balanced_120.json",
            "--seed", str(seed),
            "--num-workers", "4",
            "--max-tokens", "4096",
            "--results-dir", str(target_dir)
        ]
        
        env = os.environ.copy()
        proc = subprocess.run(cmd, cwd=str(BENCHMARK_DIR), env=env)
        if proc.returncode != 0:
            print(f"ERROR: Falló R2 seed {seed} (código {proc.returncode})")
            return False
            
        # Verificar corrida
        v_proc = subprocess.run([str(VENV_PYTHON), str(VERIFY_SCRIPT), str(target_dir)], cwd=str(REPO_ROOT))
        if v_proc.returncode == 0:
            print(f"[R2 | seed {seed}] VÁLIDA y certificada.")
            git_commit_push(f"feat(remoto): R2 barra error N=120 semilla {seed} completada")
        else:
            print(f"ALERTA: verificar_corrida devolvió código {v_proc.returncode}")
            
    return True

def main():
    wait_for_r5()
    r1_ok = run_r1_fase2()
    if r1_ok:
        print("\n>>> R1 FASE 2 (N=120) FINALIZADA CON ÉXITO <<<\n")
    else:
        print("\n>>> R1 FASE 2 REPORTÓ ERRORES <<<\n")
        
    r2_ok = run_r2()
    if r2_ok:
        print("\n>>> R2 (BARRA DE ERROR) FINALIZADA CON ÉXITO <<<\n")
    else:
        print("\n>>> R2 REPORTÓ ERRORES <<<\n")

if __name__ == "__main__":
    main()
