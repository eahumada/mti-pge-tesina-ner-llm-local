#!/usr/bin/env python3
"""
Reconciliador de resultados R2 con suite Cloud.
Sustituye los registros de gemma4:31b-cloud de una semilla con los resultados
limpios y certificados previamente obtenidos en seed_{s}_cloud/ para certificar failed == 0.
"""

import sys
import json
import argparse
import pandas as pd
from pathlib import Path

def reconciliar_semilla(seed: int, repo_root: Path):
    base = repo_root / "repos" / "ner-llm-entity-benchmark" / "results" / "barras_error_n120_REMOTO"
    dir_target = base / f"seed_{seed}"
    dir_cloud = base / f"seed_{seed}_cloud"

    if not dir_target.exists():
        print(f"Error: No existe directorio target {dir_target}")
        return False
    if not dir_cloud.exists():
        print(f"Error: No existe directorio cloud {dir_cloud}")
        return False

    # 1. Cargar detailed results cloud
    with open(dir_cloud / "detailed_results.json", "r", encoding="utf-8") as f:
        cloud_detailed = json.load(f)
    cloud_recs = cloud_detailed if isinstance(cloud_detailed, list) else cloud_detailed.get("results", cloud_detailed.get("records", []))

    # 2. Cargar detailed results target
    with open(dir_target / "detailed_results.json", "r", encoding="utf-8") as f:
        target_detailed = json.load(f)
    target_is_dict = isinstance(target_detailed, dict)
    target_recs = target_detailed.get("results", target_detailed.get("records", [])) if target_is_dict else target_detailed

    # Filtrar cloud fallido o parcial en target
    filtered_recs = [r for r in target_recs if not (r.get("model", "").startswith("gemma4:31b-cloud"))]
    merged_recs = filtered_recs + cloud_recs

    if target_is_dict:
        target_detailed["results"] = merged_recs
        with open(dir_target / "detailed_results.json", "w", encoding="utf-8") as f:
            json.dump(target_detailed, f, indent=2)
    else:
        with open(dir_target / "detailed_results.json", "w", encoding="utf-8") as f:
            json.dump(merged_recs, f, indent=2)

    # 3. CSV merge
    df_target = pd.read_csv(dir_target / "benchmark_results.csv")
    df_cloud = pd.read_csv(dir_cloud / "benchmark_results.csv")
    df_filtered = df_target[~df_target["model"].str.startswith("gemma4:31b-cloud")]
    df_merged = pd.concat([df_filtered, df_cloud], ignore_index=True)
    df_merged.to_csv(dir_target / "benchmark_results.csv", index=False)

    print(f"Semilla {seed} reconciliada con éxito ({len(merged_recs)} registros detallados, {len(df_merged)} filas CSV).")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("seed", type=int, help="Número de semilla (ej: 42, 123)")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    reconciliar_semilla(args.seed, repo_root)
