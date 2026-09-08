#!/usr/bin/env python3
"""Calcula la composición de los falsos positivos de un consolidado, por categoría.

Sostiene la cifra que el informe publica en §3.3 y §7.2 y que dibuja la Figura 1. Se calculó una vez a
mano el 2026-09-08 y quedó como artefacto suelto; esto lo hace repetible, que es lo que hará falta
cuando la re-corrida sustituya los datos.

Toma, para cada grupo del consolidado, la corrida que el manifiesto de fusión declara como suya, y suma
`tp`, `fp` y `fn` por categoría desde `detailed_results.json`. **Declara cuántos grupos ha cubierto**: si
alguno se queda fuera, el total no vale y hay que verlo, no deducirlo (FINDINGS §F69).

Uso:
    python3 tools/composicion_fp.py [dir_consolidado] > salida.json
    python3 tools/composicion_fp.py --resumen        # solo las cifras, legible
"""
import collections
import csv
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BENCH = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark')
POR_DEFECTO = os.path.join(BENCH, 'results/ANALISIS_CONJUNTO_20260907')


def calcular(dir_cons):
    man = json.load(open(os.path.join(dir_cons, 'merge_manifest.json'), encoding='utf-8'))
    dueno = {}
    for s in man['sources']:
        for g in s.get('models', []):
            dueno.setdefault(g, os.path.dirname(s['csv_path']))
    with open(os.path.join(dir_cons, 'merged_results.csv'), encoding='utf-8') as fh:
        grupos = sorted({r['model'] for r in csv.DictReader(fh)})

    cache = {}

    def registros(d):
        if d not in cache:
            p = os.path.join(BENCH, d, 'detailed_results.json')
            j = json.load(open(p, encoding='utf-8'))
            cache[d] = j if isinstance(j, list) else j.get('results', j.get('records', []))
        return cache[d]

    fp = collections.Counter()
    tp = collections.Counter()
    fn = collections.Counter()
    detalle, sin_cubrir = {}, []
    for g in grupos:
        d = dueno.get(g)
        if not d or not os.path.exists(os.path.join(BENCH, d, 'detailed_results.json')):
            sin_cubrir.append(g)
            continue
        R = [r for r in registros(d) if r.get('model') == g]
        if not R:
            sin_cubrir.append(g)
            continue
        gg = collections.Counter()
        for r in R:
            for c, v in ((r.get('metrics') or {}).get('per_type') or {}).items():
                fp[c] += v.get('fp', 0)
                tp[c] += v.get('tp', 0)
                fn[c] += v.get('fn', 0)
                gg[c] += v.get('fp', 0)
        detalle[g] = {'corrida': d.split('/')[-1], 'registros': len(R), 'fp_por_categoria': dict(gg)}

    total = sum(fp.values())
    return {
        'nota': ('Composicion de los falsos positivos de los grupos que sostienen la Tabla 7, cada uno '
                 'desde la corrida que el consolidado usa. Calculado desde los detailed_results.json, '
                 'sin reejecutar inferencia.'),
        'consolidado': os.path.relpath(dir_cons, RAIZ),
        'grupos': len(grupos), 'grupos_cubiertos': len(detalle), 'grupos_sin_cubrir': sin_cubrir,
        'fp_por_categoria': dict(fp), 'tp_por_categoria': dict(tp), 'fn_por_categoria': dict(fn),
        'fp_total': total, 'fp_locations': fp.get('Locations', 0),
        'pct_fp_locations': round(100 * fp.get('Locations', 0) / total, 1) if total else None,
        'locations_tp_mas_fn': tp.get('Locations', 0) + fn.get('Locations', 0),
        'detalle': detalle,
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    r = calcular(args[0] if args else POR_DEFECTO)
    if '--resumen' in sys.argv:
        print('  consolidado: %s' % r['consolidado'])
        print('  grupos: %d cubiertos de %d%s'
              % (r['grupos_cubiertos'], r['grupos'],
                 '' if not r['grupos_sin_cubrir'] else '  SIN CUBRIR: %s' % r['grupos_sin_cubrir']))
        for c in sorted(r['fp_por_categoria']):
            print('   %-16s fp=%6d  tp=%6d  fn=%6d  (tp+fn=%d)'
                  % (c, r['fp_por_categoria'][c], r['tp_por_categoria'].get(c, 0),
                     r['fn_por_categoria'].get(c, 0),
                     r['tp_por_categoria'].get(c, 0) + r['fn_por_categoria'].get(c, 0)))
        print('  TOTAL fp=%d · Locations=%d (%s %%)'
              % (r['fp_total'], r['fp_locations'], r['pct_fp_locations']))
        if r['locations_tp_mas_fn'] == 0:
            print('  AVISO: Locations tiene tp+fn=0 — puntua contra el vacio (FINDINGS §F53)')
        else:
            print('  Locations tiene %d entidades de referencia: ya NO puntua contra el vacio,'
                  % r['locations_tp_mas_fn'])
            print('         de modo que la lectura de la Figura 1 cambia: sus falsos positivos pasan a')
            print('         ser errores reales y no aciertos imposibles. Hay que reescribir la leyenda.')
        return 0
    print(json.dumps(r, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
