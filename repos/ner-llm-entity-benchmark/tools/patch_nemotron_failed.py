#!/usr/bin/env python3
"""Parchea las filas baseline vacías de nemotron-mini:4b (fallo de contexto batch, no del modelo).

Re-extrae los 7 registros del subcorpus con OllamaProvider (mismos params del estudio: temp 0.1, seed 42,
max_tokens 2048, SYSTEM_PROMPT.md), los puntúa con el evaluator corregido y actualiza CSV Y
detailed_results.json (metrics.overall + f1/p/r). Idempotente: matchea por record_id (no por parse_method),
así un re-score posterior no lo revierte. Backups .bak_prepatch.
"""
import csv, json, os, shutil
from src.providers.ollama_provider import OllamaProvider
from src.evaluator import evaluate_extraction_by_type

DIR = 'results/nemotron_rerun_n120_REMOTO'
CSV = DIR + '/benchmark_results.csv'
DET = DIR + '/detailed_results.json'
COND = 'nemotron-mini:4b_baseline'

sub = json.load(open('data/nemotron_failed_subset.json'))
sub = sub.get('dataset', sub) if isinstance(sub, dict) else sub
ids = [str(a.get('article_id')) for a in sub]
full = json.load(open('data/benchmark_balanced_120.json'))
ds = full.get('dataset', full)
sp = open('SYSTEM_PROMPT.md').read()
prov = OllamaProvider(model_name='nemotron-mini:4b', ollama_base_url='http://localhost:11434')

# re-extraer y puntuar los 7
fixed = {}
for rid in ids:
    a = [x for x in ds if str(x.get('article_id')) == rid][0]
    gt = {'Persons': a.get('name_entities') or [], 'Organizations': a.get('organizations') or [], 'Locations': a.get('locations') or []}
    res = prov.extract_entities(a['text'], sp, temperature=0.1, max_tokens=2048, seed=42)
    ents = res.entities if hasattr(res, 'entities') else res.get('entities')
    m = evaluate_extraction_by_type(ents, gt)['overall']
    fixed[rid] = m
    print(f"  {rid}: F1={m['f1']:.4f} tp={m['tp']} fp={m['fp']} fn={m['fn']}")

# CSV
rows = list(csv.DictReader(open(CSV)))
shutil.copy(CSV, CSV + '.bak_prepatch')
for row in rows:
    if row['model'] == COND and str(row.get('record_id')) in fixed:
        m = fixed[str(row['record_id'])]
        row['precision'], row['recall'], row['f1'] = f"{m['precision']:.6f}", f"{m['recall']:.6f}", f"{m['f1']:.6f}"
        row['parse_method'] = 'direct_json'
with open(CSV, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(f'CSV actualizado ({len(fixed)} filas)')

# detailed_results.json (metrics.overall + f1/p/r) para que el rescore sea consistente
data = json.load(open(DET))
drows = data if isinstance(data, list) else data.get('results', [])
shutil.copy(DET, DET + '.bak_prepatch')
n = 0
for x in drows:
    if x.get('model') == COND and str(x.get('record_id')) in fixed:
        m = fixed[str(x['record_id'])]
        x.setdefault('metrics', {})['overall'] = m
        x['precision'], x['recall'], x['f1'] = m['precision'], m['recall'], m['f1']
        x['parse_method'] = 'direct_json'
        n += 1
json.dump(data, open(DET, 'w'), ensure_ascii=False, indent=2)
print(f'detailed_results.json actualizado ({n} filas)')
