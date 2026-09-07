#!/usr/bin/env python3
"""Diagnostico gpt-oss:20b: reproduce el fallo y prueba repeat_penalty. Guarda la respuesta cruda integra.

5 registros baseline que fallaron (recall=0). Para cada uno: (1) tal cual (params oficiales) y
(2) con repeat_penalty=1.2. Detecta bucle de repeticion y si el JSON cierra. Salida JSON con raw completo.
"""
import json, time, re, collections
import ollama

IDS = ['real_mixed_9', 'real_mixed_21', 'real_mixed_22', 'real_mixed_23', 'real_mixed_27']
d = json.load(open('data/benchmark_balanced_120.json')); ds = d.get('dataset', d)
sp = open('SYSTEM_PROMPT.md').read()
cli = ollama.Client(host='http://localhost:11434')

def loops(txt):
    # heuristica: token repetido >=6 veces seguidas
    toks = txt.split()
    run = 1
    for i in range(1, len(toks)):
        run = run + 1 if toks[i] == toks[i-1] else 1
        if run >= 6:
            return True
    return False

def closes(txt):
    m = re.search(r'\{.*\}', txt, re.S)
    return m is not None

out = []
for rid in IDS:
    a = [x for x in ds if str(x.get('article_id')) == rid][0]
    msg = [{'role': 'system', 'content': sp}, {'role': 'user', 'content': f"News text:\n{a['text']}"}]
    row = {'record_id': rid}
    for label, opts in [('as_is', {'temperature': 0.1, 'seed': 42, 'num_predict': 2048}),
                        ('repeat_penalty_1.2', {'temperature': 0.1, 'seed': 42, 'num_predict': 2048, 'repeat_penalty': 1.2, 'repeat_last_n': 256})]:
        t = time.time()
        r = cli.chat(model='gpt-oss:20b', messages=msg, options=opts)
        lat = time.time() - t
        c = r['message']['content']
        row[label] = {'len': len(c), 'loop': loops(c), 'json_closes': closes(c),
                      'eval_count': r.get('eval_count'), 'lat': round(lat, 1), 'raw': c}
        print(f"  {rid} [{label}]: len={len(c)} loop={loops(c)} closes={closes(c)} eval={r.get('eval_count')} lat={lat:.0f}s")
    out.append(row)

json.dump(out, open('results/diag_gptoss.json', 'w'), ensure_ascii=False, indent=2)
n_loop = sum(1 for x in out if x['as_is']['loop'])
n_fixed = sum(1 for x in out if x['as_is']['loop'] and not x['repeat_penalty_1.2']['loop'])
print(f'>> bucle en {n_loop}/5 as_is ; repeat_penalty elimina el bucle en {n_fixed} de esos')
