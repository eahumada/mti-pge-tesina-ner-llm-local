#!/usr/bin/env python3
"""Re-puntúa corridas ya guardadas SIN re-inferir.

Recalcula precision/recall/f1 por registro desde los tp/fp/fn persistidos en
`detailed_results.json` (`metrics.overall`), con la convención corregida:
  - tp+fp+fn == 0  -> 1.0 (no había nada que extraer y el modelo no inventó: match vacío legítimo)
  - resto          -> P=tp/(tp+fp) [0 si no hay predicciones], R=tp/(tp+fn), F1=2PR/(P+R)

Corrige el bug de `evaluator.py` (default 1.0) que daba F1=1.0 a extracción vacía sobre gold no-vacío.
Reescribe `benchmark_results.csv` (con backup .bak_prescore) y emite un resumen por modelo.

Uso: python3 tools/rescore_saved.py results/<dir> [results/<dir> ...]
"""
import csv, json, os, sys, statistics, collections, shutil


def correct(tp, fp, fn):
    if tp + fp + fn == 0:
        return 1.0, 1.0, 1.0
    P = tp / (tp + fp) if (tp + fp) else 0.0
    R = tp / (tp + fn) if (tp + fn) else 0.0
    F = 2 * P * R / (P + R) if (P + R) else 0.0
    return P, R, F


def rescore_dir(d):
    det = os.path.join(d, 'detailed_results.json')
    csvp = os.path.join(d, 'benchmark_results.csv')
    if not os.path.exists(det):
        print(f'[skip] {d}: sin detailed_results.json')
        return
    data = json.load(open(det))
    rows = data if isinstance(data, list) else data.get('results', [])
    # índice (model, record_id) -> (P,R,F) corregido
    idx = {}
    for x in rows:
        o = (x.get('metrics') or {}).get('overall') or {}
        if not o:
            continue
        idx[(x.get('model'), str(x.get('record_id')))] = correct(o.get('tp', 0), o.get('fp', 0), o.get('fn', 0))
    if not os.path.exists(csvp):
        print(f'[warn] {d}: sin CSV; solo resumen desde detailed')
    else:
        shutil.copy(csvp, csvp + '.bak_prescore')
        r = list(csv.DictReader(open(csvp)))
        changed = 0
        for row in r:
            k = (row['model'], str(row.get('record_id')))
            if k in idx:
                P, R, F = idx[k]
                if abs(float(row.get('f1') or 0) - F) > 1e-9:
                    changed += 1
                row['precision'], row['recall'], row['f1'] = f'{P:.6f}', f'{R:.6f}', f'{F:.6f}'
        with open(csvp, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=r[0].keys()); w.writeheader(); w.writerows(r)
        print(f'[ok] {d}: CSV re-puntuado ({changed} filas cambiadas, backup .bak_prescore)')
    # resumen
    by = collections.defaultdict(list)
    for (m, rid), (P, R, F) in idx.items():
        by[m].append(F)
    for m in sorted(by):
        print(f'    {m}: F1_corregido={statistics.mean(by[m]):.4f} n={len(by[m])}')


if __name__ == '__main__':
    for d in sys.argv[1:]:
        rescore_dir(d)
