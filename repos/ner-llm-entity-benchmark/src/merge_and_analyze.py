#!/usr/bin/env python3
"""
merge_and_analyze.py
====================

Combina los `benchmark_results.csv` de VARIAS corridas del benchmark sobre el
MISMO corpus y re-ejecuta un unico ANOVA + Tukey HSD sobre el conjunto
combinado, reutilizando las funciones estadisticas ya existentes en
`src/statistics.py` (no se reimplementa nada de la estadistica).

Uso tipico
----------
    ./venv/bin/python -m src.merge_and_analyze \
        results/benchmark_balanced_120_20260901_140421 \
        results/benchmark_balanced_120_<corrida_B> \
        --output-dir results/merged_16models

Cada argumento posicional puede ser:
  * un directorio de resultados (se buscara `benchmark_results.csv` dentro), o
  * la ruta directa a un `benchmark_results.csv`.

El script:
  1. Valida que todas las corridas provengan del mismo corpus (via
     `run_config.json` y via el conjunto de `record_id`).
  2. Detecta modelos (model+modo) duplicados entre corridas y AVISA, sin
     duplicar silenciosamente las filas.
  3. Verifica integridad: cada grupo model+modo debe tener el numero esperado
     de registros (por defecto el tamano del corpus, p.ej. 120).
  4. Re-ejecuta ANOVA + Tukey HSD + intervalos de confianza + analisis de
     sensibilidad importando `src.statistics.generate_statistical_report`.
  5. Escribe `statistical_report.md` (y `merged_results.csv` +
     `merge_manifest.json`) en el directorio de salida.

IMPORTANTE: ejecutar desde la raiz del repositorio, porque el analisis de
sensibilidad resuelve `data_file` como ruta relativa.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import OrderedDict

import pandas as pd

# Permite `python src/merge_and_analyze.py` ademas de `python -m src.merge_and_analyze`
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from src.statistics import generate_statistical_report  # noqa: E402

# Columnas minimas que debe traer cada CSV de resultados
REQUIRED_COLUMNS = ["record_id", "model", "precision", "recall", "f1"]

# Columnas que consume `generate_statistical_report` (ANOVA/Tukey/sensibilidad)
STAT_COLUMNS = ["record_id", "model", "precision", "recall", "f1"]


# --------------------------------------------------------------------------- #
# Utilidades de entrada
# --------------------------------------------------------------------------- #
def resolve_input(path: str) -> tuple[str, str | None]:
    """Devuelve (ruta_csv, ruta_directorio_o_None) para un argumento de entrada."""
    if os.path.isdir(path):
        csv_path = os.path.join(path, "benchmark_results.csv")
        if not os.path.isfile(csv_path):
            raise FileNotFoundError(
                f"No se encontro 'benchmark_results.csv' dentro del directorio: {path}"
            )
        return csv_path, path
    if os.path.isfile(path):
        return path, os.path.dirname(os.path.abspath(path))
    raise FileNotFoundError(f"Ruta de entrada inexistente: {path}")


def read_run_config(run_dir: str | None) -> dict:
    """Lee `run_config.json` del directorio de la corrida (si existe)."""
    if not run_dir:
        return {}
    cfg_path = os.path.join(run_dir, "run_config.json")
    if not os.path.isfile(cfg_path):
        return {}
    try:
        with open(cfg_path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:  # pragma: no cover - defensivo
        print(f"[WARN] No se pudo leer {cfg_path}: {exc}")
        return {}


def load_source(csv_path: str, run_dir: str | None) -> dict:
    """Carga un CSV de resultados y lo devuelve como descriptor de fuente."""
    df = pd.read_csv(csv_path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"{csv_path}: faltan columnas obligatorias {missing}")

    cfg = read_run_config(run_dir)
    label = os.path.basename(run_dir.rstrip(os.sep)) if run_dir else os.path.basename(csv_path)

    return {
        "label": label,
        "csv_path": os.path.abspath(csv_path),
        "run_dir": run_dir,
        "config": cfg,
        "data_file": cfg.get("data_file"),
        "df": df,
        "models": list(OrderedDict.fromkeys(df["model"].astype(str).tolist())),
        "record_ids": set(df["record_id"].astype(str).tolist()),
        "n_rows": len(df),
    }


# --------------------------------------------------------------------------- #
# Validaciones
# --------------------------------------------------------------------------- #
def validate_same_corpus(sources: list[dict], strict: bool) -> tuple[str | None, list[str]]:
    """
    Verifica que todas las corridas usen el mismo corpus.

    Comprueba (a) el `data_file` declarado en run_config.json y (b) el conjunto
    de `record_id` presentes. Devuelve (data_file_resuelto, lista_de_problemas).
    """
    problems: list[str] = []

    declared = [s["data_file"] for s in sources if s["data_file"]]
    distinct_declared = list(OrderedDict.fromkeys(declared))
    if len(distinct_declared) > 1:
        problems.append(
            "Las corridas declaran corpus DISTINTOS en run_config.json: "
            + ", ".join(distinct_declared)
        )
    data_file = distinct_declared[0] if distinct_declared else None

    if len(sources) > 1:
        ref = sources[0]
        for other in sources[1:]:
            only_ref = ref["record_ids"] - other["record_ids"]
            only_other = other["record_ids"] - ref["record_ids"]
            if only_ref or only_other:
                problems.append(
                    f"Los record_id de '{ref['label']}' y '{other['label']}' no coinciden: "
                    f"{len(only_ref)} solo en el primero, {len(only_other)} solo en el segundo. "
                    f"Ejemplos: {sorted(only_ref)[:3]} / {sorted(only_other)[:3]}"
                )

    for p in problems:
        print(f"[{'ERROR' if strict else 'WARN'}] {p}")
    if problems and strict:
        raise SystemExit(
            "Abortado: las corridas no comparten el mismo corpus. "
            "Use --allow-corpus-mismatch para continuar de todos modos."
        )
    return data_file, problems


def detect_duplicates(sources: list[dict], on_duplicate: str) -> tuple[dict[str, str], list[str]]:
    """
    Detecta grupos model+modo presentes en mas de una corrida.

    Devuelve (owner_por_modelo, notas). `owner_por_modelo` mapea cada modelo a
    la etiqueta de la corrida cuyas filas se conservaran, de modo que ninguna
    fila se duplique silenciosamente.
    """
    seen: dict[str, str] = {}
    notes: list[str] = []
    dup_models: list[str] = []

    for src in sources:
        for model in src["models"]:
            if model in seen:
                dup_models.append(model)
                previous = seen[model]
                base = f"DUPLICADO: '{model}' aparece en '{previous}' y en '{src['label']}'."
                if on_duplicate == "error":
                    notes.append(base + " Politica --on-duplicate=error: se aborta.")
                elif on_duplicate == "last":
                    seen[model] = src["label"]
                    notes.append(
                        base + f" Se conservan las filas de '{src['label']}' (--on-duplicate=last)."
                    )
                else:
                    notes.append(
                        base + f" Se conservan las filas de '{previous}' (--on-duplicate=first)."
                    )
            else:
                seen[model] = src["label"]

    for n in notes:
        print(f"[{'ERROR' if on_duplicate == 'error' else 'WARN'}] {n}")

    if dup_models and on_duplicate == "error":
        raise SystemExit(
            "Abortado por modelos duplicados entre corridas: "
            + ", ".join(sorted(set(dup_models)))
            + ". Use --on-duplicate=first|last para resolverlo."
        )

    return seen, notes


def check_integrity(df: pd.DataFrame, expected_n: int) -> tuple[list[str], pd.DataFrame]:
    """Verifica que cada grupo model+modo tenga `expected_n` registros unicos."""
    problems: list[str] = []
    rows = []

    for model, group in df.groupby("model", sort=False):
        n_rows = len(group)
        n_unique = group["record_id"].nunique()
        n_dup_records = n_rows - n_unique
        n_nan_f1 = int(group["f1"].isna().sum())

        status = "OK"
        if n_rows != expected_n:
            status = "INCOMPLETO" if n_rows < expected_n else "EXCEDIDO"
            problems.append(
                f"'{model}': {n_rows} filas (esperadas {expected_n}) -> {status}"
            )
        if n_dup_records:
            status = "DUPLICADOS"
            problems.append(
                f"'{model}': {n_dup_records} record_id repetidos dentro del mismo grupo"
            )
        if n_nan_f1:
            problems.append(f"'{model}': {n_nan_f1} valores de f1 vacios/NaN")

        rows.append(
            {
                "model": model,
                "rows": n_rows,
                "unique_records": n_unique,
                "expected": expected_n,
                "nan_f1": n_nan_f1,
                "status": status,
            }
        )

    for p in problems:
        print(f"[WARN] Integridad: {p}")

    return problems, pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# Analisis
# --------------------------------------------------------------------------- #
def build_model_results(df: pd.DataFrame) -> "OrderedDict[str, list[dict]]":
    """
    Agrupa el DataFrame combinado en el formato que espera
    `generate_statistical_report`: {model: [ {record_id, f1, precision, ...}, ... ]}.

    El orden de insercion replica el orden de aparicion en los CSV, tal como lo
    hace `src/main.py`, para que el reporte combinado sea comparable con los
    reportes originales de cada corrida.
    """
    cols = [c for c in STAT_COLUMNS if c in df.columns]
    model_results: "OrderedDict[str, list[dict]]" = OrderedDict()
    for record in df[cols].to_dict(orient="records"):
        model_results.setdefault(str(record["model"]), []).append(record)
    return model_results


def build_header(
    sources: list[dict],
    data_file: str | None,
    expected_n: int,
    integrity_df: pd.DataFrame,
    duplicate_notes: list[str],
    corpus_problems: list[str],
    integrity_problems: list[str],
) -> str:
    """Cabecera de procedencia que se antepone al reporte estadistico."""
    lines = ["# 🔗 Merged Benchmark Analysis — Provenance & Integrity\n"]
    lines.append(f"- **Corpus:** `{data_file or 'desconocido'}`")
    lines.append(f"- **Registros esperados por modelo+modo:** {expected_n}")
    lines.append(f"- **Corridas combinadas:** {len(sources)}")
    lines.append(f"- **Grupos (modelo+modo) analizados:** {len(integrity_df)}")
    lines.append(f"- **Filas totales tras el merge:** {int(integrity_df['rows'].sum()) if not integrity_df.empty else 0}")

    lines.append("\n## Fuentes")
    lines.append("| # | Corrida | CSV | Filas | Modelos aportados |")
    lines.append("| :---: | :--- | :--- | :---: | :---: |")
    for i, s in enumerate(sources, 1):
        rel = os.path.relpath(s["csv_path"], _REPO_ROOT)
        if rel.startswith(".."):  # fuera del repo: mostrar ruta absoluta
            rel = s["csv_path"]
        lines.append(f"| {i} | {s['label']} | `{rel}` | {s['n_rows']} | {len(s['models'])} |")

    lines.append("\n## Integridad por grupo (modelo + modo)")
    lines.append("| Modelo | Filas | record_id unicos | Esperados | f1 NaN | Estado |")
    lines.append("| :--- | :---: | :---: | :---: | :---: | :---: |")
    for _, r in integrity_df.iterrows():
        mark = "✅" if r["status"] == "OK" else "⚠️"
        lines.append(
            f"| {r['model']} | {r['rows']} | {r['unique_records']} | {r['expected']} | "
            f"{r['nan_f1']} | {mark} {r['status']} |"
        )

    warnings = corpus_problems + duplicate_notes + integrity_problems
    lines.append("\n## Advertencias")
    if warnings:
        for w in warnings:
            lines.append(f"- ⚠️ {w}")
    else:
        lines.append("- Ninguna. Corpus consistente, sin duplicados y todos los grupos completos.")

    lines.append("\n---\n")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Combina resultados de varias corridas del benchmark sobre el mismo "
            "corpus y re-ejecuta ANOVA + Tukey HSD sobre el conjunto combinado."
        )
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="Directorios de resultados o rutas a benchmark_results.csv",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        required=True,
        help="Directorio donde escribir statistical_report.md y artefactos del merge",
    )
    parser.add_argument(
        "--data-file",
        default=None,
        help=(
            "Corpus a usar en el analisis de sensibilidad. Por defecto se toma "
            "el 'data_file' declarado en run_config.json de las corridas."
        ),
    )
    parser.add_argument(
        "--expected-n",
        type=int,
        default=None,
        help=(
            "Registros esperados por modelo+modo. Por defecto se infiere del "
            "numero de record_id unicos del corpus combinado (p.ej. 120)."
        ),
    )
    parser.add_argument(
        "--on-duplicate",
        choices=["first", "last", "error"],
        default="first",
        help=(
            "Que hacer si un mismo modelo+modo aparece en dos corridas: "
            "conservar la primera (default), la ultima, o abortar."
        ),
    )
    parser.add_argument(
        "--allow-corpus-mismatch",
        action="store_true",
        help="No abortar si las corridas no comparten corpus (solo advertir).",
    )
    parser.add_argument(
        "--report-name",
        default="statistical_report.md",
        help="Nombre del archivo de reporte (default: statistical_report.md)",
    )
    parser.add_argument(
        "--no-merged-csv",
        action="store_true",
        help="No escribir merged_results.csv en el directorio de salida.",
    )
    args = parser.parse_args(argv)

    # 1. Cargar fuentes -----------------------------------------------------
    sources: list[dict] = []
    for raw in args.inputs:
        csv_path, run_dir = resolve_input(raw)
        src = load_source(csv_path, run_dir)
        print(
            f"[INFO] Cargado '{src['label']}': {src['n_rows']} filas, "
            f"{len(src['models'])} grupos modelo+modo, "
            f"{len(src['record_ids'])} record_id unicos"
        )
        sources.append(src)

    # 2. Validar corpus comun ----------------------------------------------
    data_file, corpus_problems = validate_same_corpus(
        sources, strict=not args.allow_corpus_mismatch
    )
    data_file = args.data_file or data_file
    if not data_file:
        print("[WARN] No se pudo determinar el corpus; el analisis de sensibilidad quedara vacio.")
        data_file = ""

    # 3. Detectar duplicados de modelo+modo entre corridas ------------------
    owner, duplicate_notes = detect_duplicates(sources, args.on_duplicate)

    # 4. Concatenar conservando solo las filas de la corrida "duena" --------
    frames = []
    for src in sources:
        keep = [m for m in src["models"] if owner.get(m) == src["label"]]
        dropped = [m for m in src["models"] if owner.get(m) != src["label"]]
        if dropped:
            print(f"[INFO] '{src['label']}': se descartan {len(dropped)} grupos duplicados: {dropped}")
        if not keep:
            continue
        sub = src["df"][src["df"]["model"].astype(str).isin(keep)].copy()
        sub["source_run"] = src["label"]
        frames.append(sub)

    if not frames:
        print("[ERROR] No quedaron filas tras el merge.")
        return 2

    merged = pd.concat(frames, ignore_index=True)
    merged["model"] = merged["model"].astype(str)
    merged["record_id"] = merged["record_id"].astype(str)

    # 5. Integridad ---------------------------------------------------------
    expected_n = args.expected_n or merged["record_id"].nunique()
    integrity_problems, integrity_df = check_integrity(merged, expected_n)

    n_models = merged["model"].nunique()
    print(
        f"[INFO] Merge final: {len(merged)} filas | {n_models} grupos modelo+modo | "
        f"{merged['record_id'].nunique()} record_id unicos | esperados/grupo: {expected_n}"
    )
    if n_models < 2:
        print("[ERROR] Se requieren al menos 2 grupos para ANOVA/Tukey.")
        return 2

    # 6. Estadistica (reutiliza src/statistics.py) --------------------------
    model_results = build_model_results(merged)
    print("[INFO] Ejecutando ANOVA + Tukey HSD + analisis de sensibilidad...")
    stat_report = generate_statistical_report(model_results, data_file)

    header = build_header(
        sources,
        data_file,
        expected_n,
        integrity_df,
        duplicate_notes,
        corpus_problems,
        integrity_problems,
    )

    # 7. Escribir artefactos ------------------------------------------------
    os.makedirs(args.output_dir, exist_ok=True)
    report_path = os.path.join(args.output_dir, args.report_name)
    with open(report_path, "w", encoding="utf-8") as fh:
        fh.write(header + stat_report + "\n")
    print(f"[OK] Reporte estadistico combinado -> {report_path}")

    if not args.no_merged_csv:
        merged_csv = os.path.join(args.output_dir, "merged_results.csv")
        merged.to_csv(merged_csv, index=False)
        print(f"[OK] CSV combinado -> {merged_csv}")

    manifest = {
        "corpus": data_file,
        "expected_n_per_group": expected_n,
        "num_sources": len(sources),
        "sources": [
            {
                "label": s["label"],
                "csv_path": s["csv_path"],
                "rows": s["n_rows"],
                "models": s["models"],
                "data_file": s["data_file"],
            }
            for s in sources
        ],
        "merged_rows": int(len(merged)),
        "merged_groups": sorted(merged["model"].unique().tolist()),
        "integrity": integrity_df.to_dict(orient="records"),
        "duplicate_notes": duplicate_notes,
        "corpus_problems": corpus_problems,
        "integrity_problems": integrity_problems,
        "on_duplicate_policy": args.on_duplicate,
    }
    manifest_path = os.path.join(args.output_dir, "merge_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
    print(f"[OK] Manifiesto del merge -> {manifest_path}")

    # 8. Eco de las cifras clave del ANOVA ----------------------------------
    for line in stat_report.splitlines():
        if line.startswith("- **F-Statistic:**") or line.startswith("- **p-Value:**"):
            print(f"[RESULT] {line.replace('- **', '').replace('**', '')}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
