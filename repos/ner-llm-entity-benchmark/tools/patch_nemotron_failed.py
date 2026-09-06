#!/usr/bin/env python3
"""Parchea las 7 filas baseline vacías de nemotron-mini:4b (fallo de contexto batch, no del modelo).

Re-extrae esos registros con OllamaProvider usando los MISMOS params del estudio (temp 0.1, seed 42,
max_tokens 2048, mismo SYSTEM_PROMPT.md), los puntúa con el evaluator corregido, y actualiza las filas
correspondientes en el CSV destino (backup .bak_prepatch). Sólo toca las filas 'failed' de baseline.
"""
import csv, json, os, shutil, sys
from src.providers.ollama_provider import OllamaProvider
from src.evaluator import evaluate_extraction_by_type

CSV = 'results/nemotron_rerun_n120_REMOTO/benchmark_results.csv'
MODEL = 'nemotron-mini:4b'
COND = 'nemotron-mini:4b_baseline'

d = json.load(open('data/benchmark_balanced_120.json'))
ds = d.get('dataset', d)
sp = open('SYSTEM_PROMPT.md').read()
prov = OllamaProvider(model_name=MODEL, ollama_base_url='http://localhost:11434')

rows = list(csv.DictReader(open(CSV)))
failed = [x for x in rows if x['model'] == COND and x.get('parse_method') == 'failed']
print('filas failed a parchear:', len(failed))

def gold_of(rid):
    a = [x for x in ds if str(x.get('article_id')) == str(rid)][0]
    return {'Persons': a.get('name_entities') or [], 'Organizations': a.get('organizations') or [],
            'Locations': a.get('locations') or []}, a['text']

patched = 0
for row in rows:
    if row['model'] == COND and row.get('parse_method') == 'failed':
        rid = row['record_id']
        gt, text = gold_of(rid)
        res = prov.extract_entities(text, sp, temperature=0.1, max_tokens=2048, seed=42)
        ents = res.entities if hasattr(res, 'entities') else res.get('entities')
        m = evaluate_extraction_by_type(ents, gt)['overall']
        row['precision'] = f"{m['precision']:.6f}"
        row['recall'] = f"{m['recall']:.6f}"
        row['f1'] = f"{m['f1']:.6f}"
        row['parse_method'] = 'direct_json'
        n = sum(len(v) for v in ents.values())
        print(f"  {rid}: ents={n} F1={m['f1']:.4f} (tp={m['tp']} fp={m['fp']} fn={m['fn']})")
        patched += 1

if patched:
    shutil.copy(CSV, CSV + '.bak_prepatch')
    with open(CSV, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    print(f'CSV actualizado ({patched} filas), backup .bak_prepatch')
