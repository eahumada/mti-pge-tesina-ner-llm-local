#!/usr/bin/env python3
"""
tools/corregir_acceptance_status.py
-----------------------------------
§3.bis.18 — Actualiza los acceptance_status.json desfasados calculándolos
desde el benchmark_summary.json corregido de cada corrida, tal como pide
CURRENT-TASKS.md §3.bis.18 (FINDINGS §F89).

No toca los benchmark.log ni los *.bak_prescore.
Verifica con tools/derivados_desfasados.py antes y después.
"""
import json
import os
import sys

DIRS = [
    'repos/ner-llm-entity-benchmark/results/afectados_thinking_n120_REMOTO',
    'repos/ner-llm-entity-benchmark/results/benchmark_balanced_120_20260824_173017',
    'repos/ner-llm-entity-benchmark/results/benchmark_n120_REMOTO',
    'repos/ner-llm-entity-benchmark/results/excluidos_n120_REMOTO',
    'repos/ner-llm-entity-benchmark/results/gemma4_31b_cloud_n120_REMOTO',
    'repos/ner-llm-entity-benchmark/results/nemotron_rerun_n120_REMOTO',
    'repos/ner-llm-entity-benchmark/results/qwen3_nothink_n120_REMOTO',
]


def update_acceptance_status(dry_run: bool = False):
    actualizados = 0
    for d in DIRS:
        s_path = os.path.join(d, 'benchmark_summary.json')
        a_path = os.path.join(d, 'acceptance_status.json')
        if not (os.path.exists(s_path) and os.path.exists(a_path)):
            print(f"⚠️  Omitiendo {d}: falta summary o acceptance")
            continue

        with open(s_path, 'r', encoding='utf-8') as f:
            summary = json.load(f)
        with open(a_path, 'r', encoding='utf-8') as f:
            old_acc = json.load(f)

        best_model = None
        best_f1 = -1.0
        for model, metrics in summary.items():
            f1 = metrics.get('f1')
            if f1 is not None and f1 > best_f1:
                best_f1 = f1
                best_model = model

        best_hall = (
            summary.get(best_model, {}).get('hallucination_rate', 0.0)
            if best_model
            else 0.0
        )

        new_acc = {
            'target_f1_met': bool(best_f1 >= 0.85),
            'overall_f1': float(best_f1),
            'best_model': best_model,
            'hallucination_rate': float(best_hall),
            'hallucination_warning': bool(best_hall > 0.05),
        }

        print(f"Actualizando {os.path.basename(d)}:")
        print(f"  overall_f1: {old_acc.get('overall_f1')} -> {new_acc['overall_f1']}")
        print(f"  best_model: {old_acc.get('best_model')} -> {new_acc['best_model']}")

        if not dry_run:
            with open(a_path, 'w', encoding='utf-8') as f:
                json.dump(new_acc, f, indent=2)
            actualizados += 1

    print(f"\nTotal ficheros actualizados: {actualizados}/{len(DIRS)}")


if __name__ == '__main__':
    dry = '--dry-run' in sys.argv
    update_acceptance_status(dry_run=dry)
