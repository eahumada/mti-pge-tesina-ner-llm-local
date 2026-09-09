#!/usr/bin/env python3
"""Cuantifica el efecto del emparejamiento duplicado en las metricas publicadas.

`evaluator.py::evaluate_extraction_by_type` incrementa `tp` **por cada entidad
extraida que casa** con alguna de referencia, mientras calcula
`fn = len(gt) - len(matched_gts)` sobre el conjunto de referencias DISTINTAS
casadas. Si dos extracciones casan con la misma referencia —«John Smith» y
«Smith, John», que el emparejamiento difuso da por iguales al 85 %— `tp` sube dos
veces y la referencia se cuenta una. De ahi que `tp + fn` no valga `len(gt)`, que
el recuento de referencia varie entre grupos que puntuan el mismo corpus, y que
la exhaustividad por categoria llegue a pasar de 1,0.

La precision NO esta afectada: cada entidad extraida contribuye como mucho una
vez, que es lo que su denominador cuenta.

El recalculo no necesita reejecutar inferencia: de `recall = tp / len(gt)` se
despeja `len(gt)`, y de ahi las referencias casadas son `len(gt) - fn`.

    python3 tools/efecto_emparejamiento_duplicado.py [--json <salida>]
"""
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BENCH = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark')
CONS = os.path.join(BENCH, 'results/ANALISIS_CONJUNTO_20260907')

_cache = {}


def registros(rel):
    if rel not in _cache:
        p = os.path.join(BENCH, rel, 'detailed_results.json')
        _cache[rel] = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else []
    return _cache[rel]


def recalcula(r):
    """Devuelve (f1_corregido, emparejamientos_duplicados) de un registro."""
    pt = ((r.get('metrics') or {}).get('per_type')) or {}
    tp_t = fp_t = fn_t = casadas = 0
    for v in pt.values():
        tp, fp, fn = v.get('tp', 0) or 0, v.get('fp', 0) or 0, v.get('fn', 0) or 0
        rec = v.get('recall')
        n_gt = round(tp / rec) if (tp > 0 and rec) else fn
        tp_t += tp
        fp_t += fp
        fn_t += fn
        casadas += max(n_gt - fn, 0)
    p = tp_t / (tp_t + fp_t) if tp_t + fp_t else 0.0
    r_ = casadas / (casadas + fn_t) if casadas + fn_t else 0.0
    f = 2 * p * r_ / (p + r_) if p + r_ else 0.0
    if tp_t == 0 and fp_t == 0 and fn_t == 0:
        f = 1.0
    return f, tp_t - casadas


def main():
    man = json.load(open(os.path.join(CONS, 'merge_manifest.json'), encoding='utf-8'))
    # El consolidado resuelve los grupos repetidos con --on-duplicate=first: gana la PRIMERA
    # fuente que los trae, y el manifiesto lo documenta en `duplicate_notes`. Ocho de los 26
    # grupos aparecen en dos fuentes. Una comprension de diccionario deja ganar a la ultima,
    # que es la superada: asi se leyo `gpt-oss:20b` desde '05_excluidos' en lugar de desde
    # '00_gptoss_rerun', y `gemma4:12b-mlx` desde '06_P3' en lugar de '02_gemma4_12b_mlx'.
    # `setdefault` reproduce la politica del consolidado.
    origen = {}
    for s in man['sources']:
        for g in s.get('models', []):
            origen.setdefault(g, os.path.dirname(s['csv_path']))

    # Control: la media del detalle tiene que reproducir la del CSV consolidado. Si no lo hace,
    # el grupo se esta leyendo de otra corrida y sus cifras no son las publicadas.
    import csv as _csv
    from collections import defaultdict as _dd
    pub = _dd(list)
    with open(os.path.join(CONS, 'merged_results.csv'), encoding='utf-8') as fh:
        for r in _csv.DictReader(fh):
            try:
                pub[r['model']].append(float(r['f1']))
            except (TypeError, ValueError):
                pass
    descuadres = []

    grupos = {}
    for g in sorted(origen):
        R = [x for x in registros(origen[g]) if x.get('model') == g]
        if not R:
            continue
        pub_med = sum(x['f1'] for x in R) / len(R) * 100
        vals = [recalcula(x) for x in R]
        cor = sum(v[0] for v in vals) / len(vals) * 100
        ref = pub.get(g)
        if ref and abs(sum(ref) / len(ref) * 100 - pub_med) > 0.05:
            descuadres.append('%s: detalle %.2f vs consolidado %.2f'
                              % (g, pub_med, sum(ref) / len(ref) * 100))
        grupos[g] = {'n': len(R), 'f1_publicado': round(pub_med, 4),
                     'f1_corregido': round(cor, 4), 'delta': round(pub_med - cor, 4),
                     'duplicados': sum(v[1] for v in vals)}

    modelos, cambian = {}, 0
    for mo in sorted({g.rsplit('_', 1)[0] for g in grupos}):
        b, k = grupos.get(mo + '_baseline'), grupos.get(mo + '_kb_rag')
        if not b or not k:
            continue
        dp = k['f1_publicado'] - b['f1_publicado']
        dc = k['f1_corregido'] - b['f1_corregido']
        if (dp > 0) != (dc > 0):
            cambian += 1
        modelos[mo] = {'delta_publicado': round(dp, 4), 'delta_corregido': round(dc, 4)}

    orden_pub = sorted(grupos, key=lambda g: -grupos[g]['f1_publicado'])
    orden_cor = sorted(grupos, key=lambda g: -grupos[g]['f1_corregido'])

    salida = {
        'nota': ('Efecto del emparejamiento duplicado de evaluator.py sobre las metricas '
                 'publicadas. Recalculado desde detailed_results.json, sin reejecutar inferencia.'),
        'consolidado': os.path.relpath(CONS, RAIZ),
        'grupos_examinados': len(grupos),
        'duplicados_totales': sum(v['duplicados'] for v in grupos.values()),
        'delta_medio_pp': round(sum(v['delta'] for v in grupos.values()) / len(grupos), 4),
        'delta_maximo_pp': round(max(v['delta'] for v in grupos.values()), 4),
        'grupo_mas_afectado': max(grupos, key=lambda g: grupos[g]['delta']),
        'mejoras_que_cambian_de_signo': cambian,
        'orden_de_grupos_identico': orden_pub == orden_cor,
        'grupos_que_no_reproducen_el_consolidado': descuadres,
        'por_grupo': grupos,
        'por_modelo': modelos,
    }

    j = None
    if '--json' in sys.argv:
        j = sys.argv[sys.argv.index('--json') + 1]
        os.makedirs(os.path.dirname(j), exist_ok=True)
        json.dump(salida, open(j, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    print(f"  grupos examinados: {salida['grupos_examinados']}")
    print(f"  emparejamientos duplicados: {salida['duplicados_totales']}")
    print(f"  delta medio: +{salida['delta_medio_pp']} pp · maximo: +{salida['delta_maximo_pp']} pp "
          f"({salida['grupo_mas_afectado']})")
    print(f"  mejoras que cambian de signo: {salida['mejoras_que_cambian_de_signo']}")
    print(f"  orden de los grupos identico: {'si' if salida['orden_de_grupos_identico'] else 'NO'}")
    if j:
        print(f'  escrito: {os.path.relpath(j, RAIZ)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
