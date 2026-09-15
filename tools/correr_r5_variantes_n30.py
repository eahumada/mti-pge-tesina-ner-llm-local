#!/usr/bin/env python3
"""
Orquestador R5: Variantes de Prompt 2x2 sobre Par Emparejado N=30 (EN/ES) con 5 semillas.
Evalúa gemma4:latest en:
  - data/kleptotrace_augmented_30.json (Inglés)
  - data/kleptotrace_augmented_30_es.json (Español)
Bajo 4 condiciones: fs-es, zs-es, fs-en, zs-en
Semillas: 42, 123, 456, 789, 1024
"""

import os
import sys
import json
import subprocess
import numpy as np
import pandas as pd
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BENCHMARK_DIR = REPO_ROOT / "repos" / "ner-llm-entity-benchmark"
VENV_PYTHON = BENCHMARK_DIR / "venv" / "bin" / "python3"
RESULTS_BASE = BENCHMARK_DIR / "results" / "variantes_n30_parEmparejado_REMOTO"

CORPORA = [
    ("kleptotrace_augmented_30", "data/kleptotrace_augmented_30.json"),
    ("kleptotrace_augmented_30_es", "data/kleptotrace_augmented_30_es.json")
]

SEEDS = [42, 123, 456, 789, 1024]

def is_run_complete(results_dir: Path) -> bool:
    csv_file = results_dir / "benchmark_results.csv"
    if not csv_file.exists():
        return False
    try:
        df = pd.read_csv(csv_file)
        if len(df) == 120 and (df["failed"] == 0).all():
            return True
    except Exception:
        pass
    return False

def run_seed(corpus_key: str, corpus_rel_path: str, seed: int):
    target_dir = RESULTS_BASE / corpus_key / f"seed_{seed}"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    if is_run_complete(target_dir):
        print(f"[{corpus_key} | seed {seed}] YA COMPLETADA (120 filas, 0 fallos). Saltando.")
        return True
        
    print(f"\n=======================================================")
    print(f"EJECUTANDO R5: {corpus_key} | SEED {seed}")
    print(f"Directorio: {target_dir}")
    print(f"=======================================================\n")
    
    cmd = [
        str(VENV_PYTHON), "src/main.py",
        "--models", "gemma4:latest",
        "--ablation",
        "--data-file", corpus_rel_path,
        "--seed", str(seed),
        "--num-workers", "4",
        "--results-dir", str(target_dir)
    ]
    
    env = os.environ.copy()
    proc = subprocess.run(cmd, cwd=str(BENCHMARK_DIR), env=env)
    if proc.returncode != 0:
        print(f"ERROR: Falló ejecución para {corpus_key} seed {seed} (código {proc.returncode})")
        return False
        
    # Verificar corrida
    verify_cmd = [str(VENV_PYTHON), str(REPO_ROOT / "tools" / "verificar_corrida.py"), str(target_dir)]
    v_proc = subprocess.run(verify_cmd, cwd=str(REPO_ROOT))
    if v_proc.returncode != 0:
        print(f"ADVERTENCIA: verificar_corrida reportó incidencia en {target_dir}")
        
    return is_run_complete(target_dir)

def generate_report():
    print("\n=======================================================")
    print("GENERANDO REPORTE ESTADÍSTICO CONSOLIDADO R5...")
    print("=======================================================\n")
    
    data = [] # corpus, seed, condition, f1, precision, recall
    
    for corpus_key, _ in CORPORA:
        for seed in SEEDS:
            seed_dir = RESULTS_BASE / corpus_key / f"seed_{seed}"
            csv_file = seed_dir / "benchmark_results.csv"
            if not csv_file.exists():
                print(f"Falta CSV: {csv_file}")
                continue
            df = pd.read_csv(csv_file)
            for cond in ["fs-es", "zs-es", "fs-en", "zs-en"]:
                df_c = df[df["model"] == cond]
                if len(df_c) > 0:
                    data.append({
                        "corpus": corpus_key,
                        "seed": seed,
                        "condition": cond,
                        "f1": df_c["f1"].mean(),
                        "precision": df_c["precision"].mean(),
                        "recall": df_c["recall"].mean()
                    })
                    
    df_all = pd.DataFrame(data)
    if df_all.empty:
        print("No se encontraron datos para generar reporte.")
        return
        
    md_lines = [
        "# R5: Análisis de Variantes de Prompts 2×2 sobre Par Emparejado N=30",
        f"**Generado:** 2026-09-15 · **Modelo:** `gemma4:latest` · **Semillas:** {SEEDS}",
        "",
        "## Resumen Comparativo (Media ± Desviación Estándar)",
        "",
        "| Corpus (Idioma Texto) | Condición Prompt | F1 (μ ± σ) | Precisión | Exhaustividad |",
        "|:---|:---|:---:|:---:|:---:|"
    ]
    
    for corpus_key, _ in CORPORA:
        c_name = "Inglés (kleptotrace_augmented_30)" if "es" not in corpus_key else "Español (kleptotrace_augmented_30_es)"
        for cond in ["fs-es", "zs-es", "fs-en", "zs-en"]:
            sub = df_all[(df_all["corpus"] == corpus_key) & (df_all["condition"] == cond)]
            if len(sub) > 0:
                m_f1 = sub["f1"].mean()
                s_f1 = sub["f1"].std()
                m_p = sub["precision"].mean()
                m_r = sub["recall"].mean()
                md_lines.append(f"| {c_name} | `{cond}` | **{m_f1:.4f} ± {s_f1:.4f}** | {m_p:.4f} | {m_r:.4f} |")
                
    md_lines.extend([
        "",
        "## Matriz Factorial 2×2×2 (Idioma Texto × Idioma Prompt × Exemplars)",
        "",
        "| Texto | Prompt Lang | Modo | F1 Promedio |",
        "|:---|:---:|:---:|---:|"
    ])
    
    for corpus_key, _ in CORPORA:
        t_lang = "Inglés" if "es" not in corpus_key else "Español"
        for cond, p_lang, p_mode in [
            ("fs-es", "Español", "Few-Shot"),
            ("zs-es", "Español", "Zero-Shot"),
            ("fs-en", "Inglés", "Few-Shot"),
            ("zs-en", "Inglés", "Zero-Shot")
        ]:
            sub = df_all[(df_all["corpus"] == corpus_key) & (df_all["condition"] == cond)]
            if len(sub) > 0:
                md_lines.append(f"| {t_lang} | {p_lang} | {p_mode} | {sub['f1'].mean():.4f} |")
                
    report_file = REPO_ROOT / "remote_48g" / "ANALISIS-R5-PAR-EMPAREJADO-N30.md"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"\nReporte guardado exitosamente en: {report_file}")

def main():
    all_ok = True
    for corpus_key, corpus_rel_path in CORPORA:
        for seed in SEEDS:
            ok = run_seed(corpus_key, corpus_rel_path, seed)
            if not ok:
                all_ok = False
                print(f"ALERTA: Corrida falló en {corpus_key} seed {seed}")
                
    generate_report()
    if all_ok:
        print("\n>>> R5 COMPLETADO CON ÉXITO EN TODAS LAS SEMILLAS Y CORPORA <<<")
        sys.exit(0)
    else:
        print("\n>>> R5 TERMINÓ CON INCIDENCIAS <<<")
        sys.exit(1)

if __name__ == "__main__":
    main()
