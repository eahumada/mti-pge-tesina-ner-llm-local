import csv, statistics, math, json, os

SEEDS = [42, 123, 456, 789, 1024]
_HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(_HERE, '..', 'barras_error_n120_REMOTO', 'seed_{}', 'benchmark_results.csv')
EXCLUDED = {'real_mixed_1','real_mixed_101','real_mixed_21','real_mixed_27','real_mixed_41','real_mixed_59','real_mixed_79'}

per_seed_means = {}  # config -> [f1_seed42, f1_seed123, ...]
for s in SEEDS:
    with open(BASE.format(s), newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    by_cfg = {}
    for r in rows:
        if r.get('record_id') in EXCLUDED:
            continue
        by_cfg.setdefault(r['model'], []).append(float(r['f1']))
    for cfg, f1s in by_cfg.items():
        assert len(f1s) == 113, f"{cfg} seed {s}: n={len(f1s)}"
        per_seed_means.setdefault(cfg, []).append(statistics.mean(f1s))

def ci95(vals):
    n = len(vals)
    m = statistics.mean(vals)
    sd = statistics.stdev(vals) if n > 1 else 0.0
    tcrit = 2.776  # df=4, 95% two-tailed
    half = tcrit * sd / math.sqrt(n) if n > 1 else 0.0
    return m, sd, m - half, m + half

results = {}
print(f"{'config':32s} {'mean_f1':>8s} {'sd':>6s} {'ci95_lo':>8s} {'ci95_hi':>8s}   valores_por_semilla(42,123,456,789,1024)")
for cfg in sorted(per_seed_means):
    vals = per_seed_means[cfg]
    m, sd, lo, hi = ci95(vals)
    results[cfg] = {"mean_f1": m, "sd": sd, "ci95_lo": lo, "ci95_hi": hi, "per_seed": vals}
    print(f"{cfg:32s} {m*100:7.2f}% {sd*100:5.2f}% {lo*100:7.2f}% {hi*100:7.2f}%   " + ", ".join(f"{v*100:.2f}" for v in vals))

with open(os.path.join(_HERE, 'intervalos_confianza_95.json'), 'w') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print()
print("Referencia puntual del cuerpo (recorrida_20260908 / ANALISIS_CONJUNTO_20260909_FIX, N=113):")
print("  gemma4:31b-mlx_baseline: 81.47% (single point)")
print(f"  R2 5-seed mean: {per_seed_means['gemma4:31b-mlx_baseline'][0]*100:.2f}% es seed 42; consolidado 5 semillas mean={statistics.mean(per_seed_means['gemma4:31b-mlx_baseline'])*100:.2f}%")
